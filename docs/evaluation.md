# Evaluation Report

## Retrieval baseline

Corrected development baseline:

| Metric | Score |
|---|---:|
| Hit@1 | 0.740 |
| Hit@3 | 0.940 |
| Hit@5 | 0.970 |
| Hit@10 | 0.970 |
| MRR | 0.830333 |
| nDCG@10 | 0.857029 |

## Evidence-pack coverage

| Metric | Score |
|---|---:|
| ParentHit@1 | 0.760 |
| ParentHit@3 | 0.920 |
| ParentHit@5 | 0.950 |
| AnchorCoverage | 0.930 |

## Important interpretation

Leaf-level retrieval misses are not always generation-level failures. Parent expansion can still deliver clinically adequate evidence.

Examples observed during development:
- household air pollution retrieved highly relevant biomass-fuel parent evidence even when the exact leaf anchor did not match,
- acute stroke retrieval delivered the management algorithm and emergency transfer instructions even when the exact phrase anchor was absent.

## Failure categories observed

- reranker demotion,
- final top-K dropout,
- rerank-input cutoff,
- weak relevance signal,
- incomplete relevance labels,
- overly aggressive metadata filtering,
- exact-anchor false negatives,
- provider quota / rate-limit interruption during LLM-judge evaluation.

## Ablation result

A global hybrid final-score variant improved a few hard cases but introduced regressions elsewhere. It was rejected because coverage degraded.

A focused lexical-query variant was coverage-safe but produced only a tiny aggregate gain, so it was not treated as a meaningful production win.

## Release position

The architecture is frozen for now. Further retrieval tuning should only resume if fresh held-out evaluation demonstrates a material problem.
