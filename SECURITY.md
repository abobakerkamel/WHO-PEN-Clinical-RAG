# Security Policy

## Secrets

Never commit API keys, provider tokens, `.env`, checkpoints containing secrets, or raw run manifests that serialize secret-bearing configuration.

The notebook writes a redacted manifest and performs a secret-safety check before checkpoint promotion.

Before every public push:

```bash
python scripts/secret_scan.py .
```

If a credential is ever exposed in chat, logs, notebook output, or Git history:
1. revoke it,
2. issue a new credential,
3. remove it from history if it reached Git,
4. do not reuse it.
