from who_pen_rag.metrics import (
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)


def test_retrieval_metrics():
    retrieved = ["a", "b", "c", "d"]
    relevant = {"b", "d"}

    assert precision_at_k(retrieved, relevant, 2) == 0.5
    assert recall_at_k(retrieved, relevant, 2) == 0.5
    assert reciprocal_rank(retrieved, relevant) == 0.5
    assert 0.0 < ndcg_at_k(retrieved, relevant, 4) <= 1.0
