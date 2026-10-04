from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    expected_pages: int = 644
    source_filename: str = "9789290226666-eng.pdf"
    source_sha256: str = (
        "25c2761500d7c839aa3622a96481542f53f3b56348cc429931cc4c963ef17b1d"
    )

    parent_max_tokens: int = 760
    parent_overlap_ratio: float = 0.12
    leaf_max_tokens: int = 220
    leaf_overlap_ratio: float = 0.12

    embedding_model: str = "BAAI/bge-m3"
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    dense_k: int = 60
    bm25_k: int = 60
    fusion_k: int = 50
    rerank_k: int = 30
    final_leaf_k: int = 10
    final_parent_k: int = 5
    max_leaves_per_parent: int = 3
    rrf_constant: int = 60
    max_context_tokens: int = 6000
    corrective_retrieval_loops: int = 2

    hard_filter_confidence: float = 0.92

    @property
    def drive_root(self) -> Path:
        return Path(
            os.getenv(
                "WHO_PEN_DRIVE_ROOT",
                "/content/drive/MyDrive/WHO_PEN_RAG",
            )
        )


CONFIG = ProjectConfig()
