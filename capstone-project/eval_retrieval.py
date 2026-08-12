import json
from rag import retrieve_vector, retrieve_bm25, retrieve_hybrid

# Load ground truth dataset
with open("eval_data.json", "r") as f:
    ground_truth = json.load(f)

def match_chunk(expected_id: str, retrieved_chunk: dict) -> bool:
    """Match by the chunk's unique ID directly — far more reliable than
    reconstructing a formatted string, which breaks on whitespace/punctuation
    differences between ground truth and retrieved metadata."""
    return expected_id == retrieved_chunk["chunk_id"]

def evaluate(retrieval_fn, name: str, k: int = 5):
    hit_count = 0
    mrr_sum = 0.0
    
    for item in ground_truth:
        q = item["question"]
        expected_id = item["chunk_id"]
        
        results = retrieval_fn(q, top_k=k)
        
        # Check rank position of correct chunk
        hit_found = False
        for rank_idx, doc in enumerate(results):
            if match_chunk(expected_id, doc):
                hit_count += 1
                mrr_sum += 1.0 / (rank_idx + 1)
                hit_found = True
                break

    total = len(ground_truth)
    hit_rate = hit_count / total
    mrr = mrr_sum / total
    
    print(f"=== {name} (k={k}) ===")
    print(f"Hit Rate: {hit_rate:.4f} ({hit_count}/{total})")
    print(f"MRR:      {mrr:.4f}\n")

if __name__ == "__main__":
    print("Starting Retrieval Evaluation...\n")
    evaluate(retrieve_vector, "Vector Search (FAISS)", k=5)
    evaluate(retrieve_bm25, "Keyword Search (BM25)", k=5)
    evaluate(retrieve_hybrid, "Hybrid Search (RRF)", k=5)