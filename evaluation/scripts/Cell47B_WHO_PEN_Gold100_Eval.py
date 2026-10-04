# Cell 47B — Deterministic 100-question source-anchor retrieval evaluation
# Run ONLY after Cell 46B resolves all 100 anchors.
#
# This evaluates source-anchor retrieval:
# HitRate@1/3/5/10 + MRR + nDCG@10.
# It intentionally does NOT treat Precision@5 as a production metric because the
# automatically resolved anchors are incomplete relevance judgements, not clinician-
# reviewed exhaustive relevant-leaf labels.

import math
import time
import pandas as pd
from tqdm.auto import tqdm

if "gold100_df" not in globals():
    raise RuntimeError("Run Cell 46B first.")

if len(gold100_df) != 100:
    raise RuntimeError(
        f"Only {len(gold100_df)}/100 anchors resolved. "
        "Fix unresolved anchors before running the 100-question evaluation."
    )

def _dcg_binary(retrieved_ids, relevant_ids, k=10):
    relevant = set(relevant_ids)
    score = 0.0
    for rank, leaf_id in enumerate(retrieved_ids[:k], start=1):
        rel = 1.0 if leaf_id in relevant else 0.0
        if rel:
            score += rel / math.log2(rank + 1)
    return score

def _ndcg_binary(retrieved_ids, relevant_ids, k=10):
    relevant = set(relevant_ids)
    if not relevant:
        return 0.0
    dcg = _dcg_binary(retrieved_ids, relevant, k=k)
    ideal_hits = min(len(relevant), k)
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0

_eval_rows = []
_t0 = time.perf_counter()

for item in tqdm(
    gold100_df.to_dict("records"),
    desc="Gold-100 deterministic retrieval eval"
):
    question = item["question"]
    relevant = set(item["relevant_leaf_ids"])

    # No LLM planner variability during retrieval benchmarking.
    plan = fallback_query_plan(question)
    result = retrieve_once(question, plan=plan)
    hits = result["reranked"][:10]
    retrieved = [str(x["leaf_id"]) for x in hits]

    first_rank = None
    for rank, leaf_id in enumerate(retrieved, start=1):
        if leaf_id in relevant:
            first_rank = rank
            break

    _eval_rows.append({
        "question_id": item["question_id"],
        "module_id": item["module_id"],
        "question_type": item["question_type"],
        "question": question,
        "n_relevant_anchor_leaves": len(relevant),
        "hit_at_1": bool(first_rank is not None and first_rank <= 1),
        "hit_at_3": bool(first_rank is not None and first_rank <= 3),
        "hit_at_5": bool(first_rank is not None and first_rank <= 5),
        "hit_at_10": bool(first_rank is not None and first_rank <= 10),
        "first_match_rank": first_rank,
        "reciprocal_rank": (1.0 / first_rank) if first_rank else 0.0,
        "ndcg_at_10": _ndcg_binary(retrieved, relevant, k=10),
        "top1_leaf_id": retrieved[0] if retrieved else None,
    })

gold100_eval_df = pd.DataFrame(_eval_rows)

metrics = {
    "N": len(gold100_eval_df),
    "HitRate@1": float(gold100_eval_df["hit_at_1"].mean()),
    "HitRate@3": float(gold100_eval_df["hit_at_3"].mean()),
    "HitRate@5": float(gold100_eval_df["hit_at_5"].mean()),
    "HitRate@10": float(gold100_eval_df["hit_at_10"].mean()),
    "MRR": float(gold100_eval_df["reciprocal_rank"].mean()),
    "nDCG@10": float(gold100_eval_df["ndcg_at_10"].mean()),
}

print("\n" + "=" * 90)
print("WHO PEN — GOLD-100 SOURCE-ANCHOR RETRIEVAL METRICS")
print("=" * 90)
for k, v in metrics.items():
    if k == "N":
        print(f"{k:<12}: {v}")
    else:
        print(f"{k:<12}: {v:.4f}")
print("=" * 90)

# Failures / weak ranks
weak = gold100_eval_df[
    (~gold100_eval_df["hit_at_3"])
].copy()

print("\nCases missing from Top-3:", len(weak))
if len(weak):
    display(
        weak[
            ["question_id", "module_id", "question_type", "question", "first_match_rank"]
        ].sort_values(["module_id", "question_id"])
    )

# Per-module QA
module_eval = (
    gold100_eval_df
    .groupby("module_id")
    .agg(
        questions=("question_id", "count"),
        hit1=("hit_at_1", "mean"),
        hit3=("hit_at_3", "mean"),
        hit10=("hit_at_10", "mean"),
        mrr=("reciprocal_rank", "mean"),
        ndcg10=("ndcg_at_10", "mean"),
    )
    .reset_index()
)

print("\nPer-module performance:")
display(module_eval)

OUT_PATH = CFG.root / "eval" / "gold100_source_anchor_eval.csv"
gold100_eval_df.to_csv(OUT_PATH, index=False)

SUMMARY_PATH = CFG.root / "eval" / "gold100_source_anchor_metrics.json"
import json
with SUMMARY_PATH.open("w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2)

print("\nSaved:")
print(" ", OUT_PATH)
print(" ", SUMMARY_PATH)
print(
    f"\n⏱ Gold-100 evaluation: "
    f"{(time.perf_counter() - _t0)/60:.2f} min"
)
