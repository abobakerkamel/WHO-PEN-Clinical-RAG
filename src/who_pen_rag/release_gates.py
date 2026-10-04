from __future__ import annotations

from typing import Any

PRODUCTION_GATES = {
    "recall@10": 0.85,
    "precision@5": 0.65,
    "context_precision": 0.80,
    "context_recall": 0.80,
    "faithfulness": 0.80,
    "critical_numeric_mismatches": 0,
    "invalid_citations": 0,
    "unsupported_clinical_claims": 0,
}


def evaluate_release_state(
    *,
    retrieval_means: dict[str, float] | None,
    ragas_means: dict[str, float] | None,
    critical_numeric_mismatches: int = 0,
    invalid_citations: int = 0,
    unsupported_clinical_claims: int = 0,
) -> dict[str, Any]:
    """Fail/pending-closed release gate.

    Missing mandatory evidence is PENDING, never silently PASS.
    """
    failures: list[str] = []
    pending: list[str] = []

    if not retrieval_means:
        pending.append("retrieval_metrics_missing")
    else:
        for metric in ("recall@10", "precision@5"):
            if metric not in retrieval_means:
                pending.append(f"{metric}_missing")
            elif retrieval_means[metric] < PRODUCTION_GATES[metric]:
                failures.append(
                    f"{metric}={retrieval_means[metric]:.3f} "
                    f"< {PRODUCTION_GATES[metric]}"
                )

    if not ragas_means:
        pending.append("ragas_metrics_missing")
    else:
        for metric in ("context_precision", "context_recall", "faithfulness"):
            if metric not in ragas_means:
                pending.append(f"{metric}_missing")
            elif ragas_means[metric] < PRODUCTION_GATES[metric]:
                failures.append(
                    f"{metric}={ragas_means[metric]:.3f} "
                    f"< {PRODUCTION_GATES[metric]}"
                )

    if critical_numeric_mismatches:
        failures.append(
            f"critical_numeric_mismatches={critical_numeric_mismatches}"
        )
    if invalid_citations:
        failures.append(f"invalid_citations={invalid_citations}")
    if unsupported_clinical_claims:
        failures.append(
            f"unsupported_clinical_claims={unsupported_clinical_claims}"
        )

    status = "failed" if failures else ("pending" if pending else "passed")
    return {
        "status": status,
        "passed": status == "passed",
        "failures": failures,
        "pending": pending,
    }
