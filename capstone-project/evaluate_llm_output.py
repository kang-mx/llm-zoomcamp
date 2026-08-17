"""
Compares two RAG approaches — with and without query rewriting — by
generating answers for a sample of ground-truth questions and scoring
both with an LLM judge. Serves as both the LLM Evaluation criterion
(multiple approaches evaluated) and the query rewriting best-practice.

Usage:
    python evaluate_llm_output.py
"""

import json
import random
import time

from rag import answer_question, safe_chat_completion, CHAT_MODEL

EVAL_DATA_PATH = "eval_data.json"
OUTPUT_PATH = "llm_eval_results.json"
SAMPLE_SIZE = 10
RANDOM_SEED = 7

JUDGE_PROMPT = """You are judging two AI-generated answers to the same question,
based on a handbook of engineering statistics. Score each answer from 1-5 on:
- faithfulness: does it stick to what would be in the source material, no fabrication
- relevance: does it actually answer the question asked
- clarity: is it well-written and easy to follow

QUESTION: {question}

ANSWER A (no query rewriting):
{answer_a}

ANSWER B (with query rewriting):
{answer_b}

Respond with ONLY a JSON object in this exact format:
{{"a_score": {{"faithfulness": X, "relevance": X, "clarity": X}},
  "b_score": {{"faithfulness": X, "relevance": X, "clarity": X}},
  "reasoning": "one sentence on why"}}
"""


def judge_pair(question, answer_a, answer_b, retries=3):
    prompt = JUDGE_PROMPT.format(question=question, answer_a=answer_a, answer_b=answer_b)
    for attempt in range(retries):
        try:
            resp = safe_chat_completion(
                model=CHAT_MODEL,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.choices[0].message.content.strip()
            if raw.startswith("```"):
                raw = raw.strip("`")
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw
                raw = raw.replace("json", "", 1).strip()
            return json.loads(raw)
        except Exception as e:
            if attempt == retries - 1:
                print(f"    judge FAILED: {e}")
                return None
            time.sleep(2 ** attempt)


def avg_score(score_dict):
    return sum(score_dict.values()) / len(score_dict)


def main():
    with open(EVAL_DATA_PATH) as f:
        eval_data = json.load(f)

    random.seed(RANDOM_SEED)
    sample = random.sample(eval_data, min(SAMPLE_SIZE, len(eval_data)))

    results = []
    a_totals, b_totals = [], []

    for i, item in enumerate(sample):
        q = item["question"]
        print(f"[{i + 1}/{len(sample)}] {q[:60]}...")
        time.sleep(3)

        result_a = answer_question(q, use_rewrite=False)
        result_b = answer_question(q, use_rewrite=True)

        judgment = judge_pair(q, result_a["answer"], result_b["answer"])
        if judgment is None:
            continue

        a_avg = avg_score(judgment["a_score"])
        b_avg = avg_score(judgment["b_score"])
        a_totals.append(a_avg)
        b_totals.append(b_avg)

        results.append({
            "question": q,
            "rewritten_query": result_b["retrieval_query"],
            "answer_a": result_a["answer"],
            "answer_b": result_b["answer"],
            "a_score": judgment["a_score"],
            "b_score": judgment["b_score"],
            "reasoning": judgment.get("reasoning", ""),
        })

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Results over {len(results)} questions ===")
    print(f"No rewriting  (A): avg score = {sum(a_totals)/len(a_totals):.2f}")
    print(f"With rewriting (B): avg score = {sum(b_totals)/len(b_totals):.2f}")
    winner = "With query rewriting" if sum(b_totals) > sum(a_totals) else "Without query rewriting"
    print(f"Winner: {winner}")
    print(f"Full results saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()