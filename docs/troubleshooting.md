# Troubleshooting and Engineering Log

| Problem | Root cause | Engineering response |
|---|---|---|
| Module metadata contamination | First internal "Annex 1" mention was mistaken for the final annex boundary | Rebuilt authoritative page ranges; true final annex begins at page 629 |
| Duplicate table columns / lost row semantics | Naive dataframe headers collapsed repeated column names | Lossless table ledger with safe internal column IDs and original headers |
| Colab RAM instability | Heavy global OCR / image inference on a 644-page document | Native text/layout/table pass; visual QA only where needed |
| Stale vector indexes | Hierarchy changed but old cache/index survived | Fingerprinted embeddings, BM25 and Qdrant artifacts |
| Qdrant local lock | Multiple local clients touching the same storage path | Explicit close/reopen discipline |
| NumPy binary incompatibility | Mixed binary wheels after in-place package upgrades | Deterministic environment bootstrap + one controlled runtime restart |
| RAGAS `ChatVertexAI` import failure | RAGAS 0.4.3 expected old LangChain import paths | Compatibility patch to `langchain-google-vertexai` |
| RAGAS 429 | LLM judge exceeded provider quota/rate limits | Resumable sequential evaluation with checkpointing and pending status |
| Planner role-filter risk | High-confidence `content_role` could exclude valid evidence | Treat role as advisory rather than sole hard-filter |
| Reranker score interpretation | Sigmoid(logit) was easy to misread as calibrated probability | Explicitly document it as uncalibrated; do not use as confidence |
| Gold-label incompleteness | Valid alternative evidence was missing from relevance labels | Manual/source-grounded label repair; no automatic expansion |
| Manifest leaked runtime secret | Raw dataclass serialization included API key | Secret-redacted manifest + secret scan before checkpoint |
| Overfitting risk | Same Gold-100 set was used for analysis and tuning | Freeze it as development set; require new held-out set |
