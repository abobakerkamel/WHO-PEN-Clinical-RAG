# Deployment Roadmap

The Colab + Gradio notebook is the current demonstration runtime. The recommended production target is:

```text
Client
  ↓
React / Next.js or Gradio
  ↓
FastAPI
  ↓
RAG service
  ├── Qdrant
  ├── BM25 / sparse index
  ├── Redis cache
  ├── embedding model
  ├── reranker
  └── LLM provider
```

## Before public deployment

1. Finish RAGAS on a stable judge provider.
2. Freeze a fresh held-out clinical set.
3. Run numeric safety, citation validity, unsupported-claim tests.
4. Add request authentication / rate limiting.
5. Add structured logs and traces.
6. Add Redis caching for repeated retrieval/query plans.
7. Move Qdrant from local embedded mode to a server/service.
8. Containerize backend.
9. Add CI/CD and rollback.
10. Record latency, token cost, failure rate, and successful-task cost.

## Observability

Track:
- retrieval latency,
- reranker latency,
- generation latency,
- verification latency,
- total tokens,
- evidence count,
- refusal / review rate,
- citation verification failure,
- numeric mismatch failure,
- provider 429/5xx errors.

## Security

- secrets from environment / secret manager only,
- no API keys in notebooks, manifests, logs, Git history,
- audit all tool/provider calls,
- pin dependencies,
- use least-privilege credentials.
