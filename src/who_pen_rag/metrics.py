from __future__ import annotations

import math
from collections.abc import Sequence, Set


def precision_at_k(retrieved: Sequence[str], relevant: Set[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    top = list(retrieved)[:k]
    if not top:
        return 0.0
    return sum(item in relevant for item in top) / k


def recall_at_k(retrieved: Sequence[str], relevant: Set[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    if not relevant:
        return 0.0
    top = list(retrieved)[:k]
    return sum(item in relevant for item in top) / len(relevant)


def reciprocal_rank(retrieved: Sequence[str], relevant: Set[str]) -> float:
    for rank, item in enumerate(retrieved, start=1):
        if item in relevant:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: Sequence[str], relevant: Set[str], k: int) -> float:
    if k <= 0:
        raise ValueError("k must be positive")
    if not relevant:
        return 0.0

    dcg = 0.0
    for i, item in enumerate(list(retrieved)[:k], start=1):
        if item in relevant:
            dcg += 1.0 / math.log2(i + 1)

    ideal_hits = min(k, len(relevant))
    idcg = sum(
        1.0 / math.log2(i + 1)
        for i in range(1, ideal_hits + 1)
    )
    return dcg / idcg if idcg else 0.0
