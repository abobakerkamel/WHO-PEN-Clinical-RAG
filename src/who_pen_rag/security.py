from __future__ import annotations

import re
from typing import Any

_SECRET_KEY_NAMES = (
    "api_key",
    "apikey",
    "secret",
    "password",
    "access_token",
    "refresh_token",
    "private_key",
)

SECRET_PATTERNS = (
    re.compile(r"\bgsk_[A-Za-z0-9_-]{20,}\b"),
    re.compile(r"\bsk-proj-[A-Za-z0-9_-]{20,}\b"),
)


def redact_mapping(data: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in data.items():
        low = str(key).lower()
        if any(marker in low for marker in _SECRET_KEY_NAMES):
            safe[f"{key}_configured"] = bool(value)
        else:
            safe[key] = value
    return safe


def contains_secret(text: str) -> bool:
    return any(pattern.search(text) for pattern in SECRET_PATTERNS)
