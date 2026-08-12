"""
Reads chunks from DuckDB, embeds them locally using sentence-transformers,
and builds a FAISS index.
"""
import os
import pickle
import duckdb
import faiss
import numpy as np

# Silence Hugging Face Hub download warnings
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_VERBOSITY"] = "error"

from sentence_transformers import SentenceTransformer

DUCKDB_PATH = "handbook_ingestion.duckdb"
INDEX_PATH = "handbook.index"
METADATA_PATH = "handbook_metadata.pkl"

# 'all-MiniLM-L6-v2' is lightweight (80MB), fast on CPU, and yields 384-dim vectors
MODEL_NAME = "all-MiniLM-L6-v2"


def load_chunks():
    con = duckdb.connect(DUCKDB_PATH)
    rows = con.execute(
        "SELECT chunk_id, source_doc, page, section_title, text "
        "FROM handbook_data.handbook_chunks"
    ).fetchall()
    con.close()
    return [
        {
            "chunk_id": r[0],
            "source_doc": r[1],
            "page": r[2],
            "section_title": r[3],
            "text": r[4],
        }
        for r in rows
    ]


def main():
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks")

    texts = [c["text"] for c in chunks]

    print(f"Loading local embedding model ({MODEL_NAME})...")
    model = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings...")
    # encode() automatically handles batching locally
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32)

    matrix = np.array(embeddings, dtype="float32")
    faiss.normalize_L2(matrix)  # so inner product == cosine similarity

    dim = matrix.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(matrix)

    faiss.write_index(index, INDEX_PATH)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(chunks, f)

    print(f"Index built: {index.ntotal} vectors, dim={dim}")
    print(f"Saved to {INDEX_PATH} and {METADATA_PATH}")


if __name__ == "__main__":
    main()