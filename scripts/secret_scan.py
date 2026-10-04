from __future__ import annotations

import argparse
import re
from pathlib import Path

PATTERNS = (
    ("Groq-like API key", re.compile(r"\bgsk_[A-Za-z0-9_-]{20,}\b")),
    ("OpenAI project key", re.compile(r"\bsk-proj-[A-Za-z0-9_-]{20,}\b")),
)

SKIP_PARTS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
}

BINARY_SUFFIXES = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".zip",
    ".parquet", ".npy", ".joblib",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root)
    findings = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() in BINARY_SUFFIXES:
            continue

        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        for label, pattern in PATTERNS:
            if pattern.search(text):
                findings.append((path, label))

    if findings:
        for path, label in findings:
            print(f"SECRET-SCAN FAIL: {label}: {path}")
        raise SystemExit(1)

    print("Secret scan: PASS")


if __name__ == "__main__":
    main()
