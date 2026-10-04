# Architecture

## End-to-end flow

```text
WHO PEN PDF
   ↓
Source governance + SHA-256
   ↓
Layout-aware parsing
   ↓
Canonical elements + provenance
   ↓
Module/theme/content-role metadata
   ↓
L3 Parents (~760 tokens)
   ↓
L4 Leaves (~220 tokens)
   ↓
┌───────────────┬───────────────┐
│ BGE-M3 Dense  │ BM25 Sparse   │
└───────┬───────┴───────┬───────┘
        ↓               ↓
           RRF Fusion
               ↓
      BGE Cross-Encoder
               ↓
      Top leaf evidence
               ↓
 Parent / table expansion
               ↓
   Corrective retrieval
               ↓
  Grounded generation
               ↓
Citation + numeric checks
               ↓
 Entailment verification
               ↓
Answer / safe refusal / review
```

## Why hierarchical retrieval?

Small leaves are easier to retrieve precisely. Larger parents are better generation context.

This is the Small-to-Big pattern:

```text
Query
  ↓
Retrieve L4 leaves
  ↓
Rank precise evidence
  ↓
Resolve parent_id
  ↓
Expand selected L3 parents
  ↓
Generate from coherent context
```

## Core retrieval parameters

| Parameter | Value |
|---|---:|
| Dense K | 60 |
| BM25 K | 60 |
| RRF fusion K | 50 |
| Rerank K | 30 |
| Final leaves | 10 |
| Final parents | 5 |
| Max leaves per parent | 3 |
| RRF constant | 60 |
| Max context tokens | 6000 |
| Corrective loops | 2 |

## Model stack

- Embeddings: `BAAI/bge-m3`
- Reranker: `BAAI/bge-reranker-v2-m3`
- LLM API: OpenAI-compatible endpoint
- GUI: Gradio Blocks
- Vector DB: Qdrant
- Sparse search: BM25
