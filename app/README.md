# Application Layer

The current demo UI is implemented directly inside the final Colab notebook using **Gradio Blocks**.

Why keep the demo there now?
- zero frontend/backend drift,
- direct access to the live retrieval objects,
- easy evidence and developer trace display,
- fast portfolio demo deployment.

The next production extraction should move the core pipeline to a service layer and expose:
- `POST /query`
- `GET /health`
- `GET /ready`
- structured trace IDs
- authentication / rate limiting
- observability hooks.

See `docs/deployment-roadmap.md`.
