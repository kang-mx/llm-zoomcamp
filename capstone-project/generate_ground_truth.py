"""
Generates ground-truth (question, chunk_id) pairs by asking the LLM to
produce questions that each chunk would answer. Used later to evaluate
retrieval hit-rate / MRR.

Usage:
    python generate_ground_truth.py
"""

import json
import os
import pickle
import random
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

METADATA_PATH = "handbook_metadata.pkl"
OUTPUT_PATH = "eval_data.json" 
CHAT_MODEL = "gemini-3.1-flash-lite"
SAMPLE_SIZE = 180        
QUESTIONS_PER_CHUNK = 2  
CHUNKS_PER_CALL = 8      
RANDOM_SEED = 42

client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

BATCH_PROMPT_TEMPLATE = """You are generating evaluation questions for a retrieval system.
Below are {n_chunks} numbered text passages from an engineering statistics handbook.
For EACH passage, write {n_q} short, specific questions that passage directly answers.
A person asking these questions should be looking for exactly that passage.

Respond with ONLY a JSON object mapping each passage number (as a string) to a
list of questions. No other text. Example:
{{"0": ["question one?", "question two?"], "1": ["question three?", "question four?"]}}

PASSAGES:
{passages}
"""


def generate_questions_batch(chunks_batch, n_q: int, retries: int = 3):
    passages = "\n\n".join(
        f"[{i}]\n{c['text']}" for i, c in enumerate(chunks_batch)
    )
    prompt = BATCH_PROMPT_TEMPLATE.format(
        n_chunks=len(chunks_batch), n_q=n_q, passages=passages
    )
    for attempt in range(retries):
        try:
            resp = client.chat.completions.create(
                model=CHAT_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.strip("`")
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw
                raw = raw.replace("json", "", 1).strip()
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, dict) else {}
        except Exception as e:
            if attempt == retries - 1:
                print(f"  FAILED batch after {retries} attempts: {e}")
                return {}
            time.sleep(2 ** attempt)
    return {}


def main():
    with open(METADATA_PATH, "rb") as f:
        chunks = pickle.load(f)

    random.seed(RANDOM_SEED)
    sample = [c for c in random.sample(chunks, min(SAMPLE_SIZE, len(chunks)))
              if len(c["text"]) >= 200]  # skip near-empty chunks upfront

    ground_truth = []
    for i in range(0, len(sample), CHUNKS_PER_CALL):
        batch = sample[i:i + CHUNKS_PER_CALL]
        result = generate_questions_batch(batch, QUESTIONS_PER_CHUNK)
        for idx_str, questions in result.items():
            try:
                chunk = batch[int(idx_str)]
            except (ValueError, IndexError):
                continue
            for q in questions:
                ground_truth.append({
                    "question": q,
                    "chunk_id": chunk["chunk_id"],
                    "source_doc": chunk["source_doc"],
                    "section_title": chunk["section_title"],
                })
        print(f"  processed {min(i + CHUNKS_PER_CALL, len(sample))}/{len(sample)} chunks, "
              f"{len(ground_truth)} questions so far "
              f"({(i // CHUNKS_PER_CALL) + 1} API calls used)")

    with open(OUTPUT_PATH, "w") as f:
        json.dump(ground_truth, f, indent=2)

    print(f"\nDone. {len(ground_truth)} ground-truth questions saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()