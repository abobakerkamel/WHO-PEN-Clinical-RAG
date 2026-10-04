from __future__ import annotations

import argparse
import hashlib
import shutil
from pathlib import Path

EXPECTED_SHA256 = "25c2761500d7c839aa3622a96481542f53f3b56348cc429931cc4c963ef17b1d"
EXPECTED_NAME = "9789290226666-eng.pdf"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument(
        "--dest",
        type=Path,
        default=Path("data/source") / EXPECTED_NAME,
    )
    parser.add_argument(
        "--allow-hash-mismatch",
        action="store_true",
        help="Copy even if the source hash differs from the development source.",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"Missing source file: {args.pdf}")

    digest = sha256(args.pdf)
    print("SHA-256:", digest)

    if digest != EXPECTED_SHA256 and not args.allow_hash_mismatch:
        raise SystemExit(
            "Source hash differs from the development source. "
            "Use --allow-hash-mismatch only if this is intentional."
        )

    args.dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.pdf, args.dest)
    print("Copied to:", args.dest)


if __name__ == "__main__":
    main()
