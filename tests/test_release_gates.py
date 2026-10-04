from who_pen_rag.release_gates import evaluate_release_state


def test_missing_ragas_is_pending_not_passed():
    result = evaluate_release_state(
        retrieval_means={"recall@10": 0.97, "precision@5": 0.8},
        ragas_means=None,
    )
    assert result["status"] == "pending"
    assert result["passed"] is False


def test_fail_on_numeric_mismatch():
    result = evaluate_release_state(
        retrieval_means={"recall@10": 0.97, "precision@5": 0.8},
        ragas_means={
            "context_precision": 0.9,
            "context_recall": 0.9,
            "faithfulness": 0.9,
        },
        critical_numeric_mismatches=1,
    )
    assert result["status"] == "failed"
