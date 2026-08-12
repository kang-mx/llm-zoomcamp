import os
import pickle
import sys

import faiss
import numpy as np
import time
from openai import OpenAI
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

INDEX_PATH = "handbook.index"
METADATA_PATH = "handbook_metadata.pkl"
CHAT_MODEL = "gemini-3.1-flash-lite"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
TOP_K = 5

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

_last_call_time = [0.0]
MIN_CALL_INTERVAL = 4.5  # seconds between calls — keeps you safely under 15 RPM

def safe_chat_completion(retries=5, **kwargs):
    """Wraps every chat completion call with enforced spacing + retry on rate limits."""
    for attempt in range(retries):
        elapsed = time.monotonic() - _last_call_time[0]
        if elapsed < MIN_CALL_INTERVAL:
            time.sleep(MIN_CALL_INTERVAL - elapsed)
        try:
            resp = client.chat.completions.create(**kwargs)
            _last_call_time[0] = time.monotonic()
            return resp
        except Exception as e:
            _last_call_time[0] = time.monotonic()
            wait = 8 + (attempt * 5)
            print(f"    rate limited, waiting {wait}s (attempt {attempt + 1}/{retries})")
            time.sleep(wait)
    raise RuntimeError("Exceeded retries — check if this is a per-day quota, not per-minute")


_index = faiss.read_index(INDEX_PATH)
with open(METADATA_PATH, "rb") as f:
    _chunks = pickle.load(f)

# Assign an explicit unique integer ID to every chunk to prevent dictionary overwrites
for idx, chunk in enumerate(_chunks):
    chunk["unique_id"] = idx

_embed_model = SentenceTransformer(EMBED_MODEL_NAME)

# Tokenize corpus for BM25
tokenized_corpus = [chunk["text"].lower().split() for chunk in _chunks]
_bm25 = BM25Okapi(tokenized_corpus)


def embed_query(text: str):
    vec = _embed_model.encode([text], show_progress_bar=False)
    vec = np.array(vec, dtype="float32")
    faiss.normalize_L2(vec)
    return vec


def retrieve_vector(query: str, top_k: int = TOP_K):
    vec = embed_query(query)
    scores, indices = _index.search(vec, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue
        chunk = _chunks[idx]
        results.append({**chunk, "score": float(score)})
    return results


def retrieve_bm25(query: str, top_k: int = TOP_K):
    tokenized_query = query.lower().split()
    scores = _bm25.get_scores(tokenized_query)
    top_indices = np.argsort(scores)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        chunk = _chunks[idx]
        results.append({**chunk, "score": float(scores[idx])})
    return results


def retrieve_hybrid(query: str, top_k: int = TOP_K, alpha: float = 60.0):
    vector_docs = retrieve_vector(query, top_k=top_k * 2)
    bm25_docs = retrieve_bm25(query, top_k=top_k * 2)
    
    rrf_scores = {}
    doc_map = {}

    # Use unique_id as key instead of constructed metadata strings
    for rank, doc in enumerate(vector_docs):
        doc_id = doc["unique_id"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (alpha + rank + 1))

    for rank, doc in enumerate(bm25_docs):
        doc_id = doc["unique_id"]
        doc_map[doc_id] = doc
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (alpha + rank + 1))

    sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
    
    results = []
    for doc_id, score in sorted_docs:
        doc = doc_map[doc_id]
        results.append({**doc, "score": float(score)})
    return results


def build_prompt(query: str, retrieved_chunks):
    context = "\n\n---\n\n".join(
        f"[{c['source_doc']} p.{c['page']} – {c['section_title']}]\n{c['text']}"
        for c in retrieved_chunks
    )
    return f"""You are answering questions using the NIST/SEMATECH Engineering \
Statistics Handbook. Use ONLY the context below to answer. If the context \
doesn't contain the answer, say so clearly instead of guessing.

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""


REWRITE_PROMPT = """Rewrite the following user question to be more specific and \
retrieval-friendly for a search over an engineering statistics handbook. \
Expand abbreviations, add relevant technical terms if implied, but keep it \
a single question. Respond with ONLY the rewritten question, no other text.

ORIGINAL QUESTION: {query}
"""

def rewrite_query(query: str, retries: int = 4) -> str:
    for attempt in range(retries):
        try:
            resp = safe_chat_completion(
                model=CHAT_MODEL,
                messages=[{"role": "user", "content": REWRITE_PROMPT.format(query=query)}],
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt + 1)


def answer_question(query: str, top_k: int = TOP_K, search_type: str = "hybrid", use_rewrite: bool = False):
    retrieval_query = rewrite_query(query) if use_rewrite else query

    if search_type == "bm25":
        retrieved = retrieve_bm25(retrieval_query, top_k)
    elif search_type == "vector":
        retrieved = retrieve_vector(retrieval_query, top_k)
    else:
        retrieved = retrieve_hybrid(retrieval_query, top_k)

    prompt = build_prompt(query, retrieved)  # note: original query in the final prompt, not the rewritten one
    resp = safe_chat_completion(
        model=CHAT_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return {
        "query": query,
        "retrieval_query": retrieval_query,
        "answer": resp.choices[0].message.content,
        "retrieved_chunks": retrieved,
    }


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "When do we say that a process is out of control?"
    result = answer_question(q)
    print("QUESTION:", result["query"])
    print("\nANSWER:", result["answer"])
    print("\nSOURCES:")
    for c in result["retrieved_chunks"]:
        print(f"  - {c['source_doc']} p.{c['page']} [{c['section_title']}] (score={c['score']:.3f})")