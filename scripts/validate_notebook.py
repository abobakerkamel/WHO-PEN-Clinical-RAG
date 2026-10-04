from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> None:
    path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else "notebooks/WHO_PEN_Production_Clinical_RAG_v7_ProductionGUI.ipynb"
    )

    data = json.loads(path.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", []))
        for cell in data.get("cells", [])
    )

    required = [
        "BAAI/bge-m3",
        "BAAI/bge-reranker-v2-m3",
        "RRF",
        "run_ragas_eval",
        "Production acceptance gates",
        "Professional Gradio GUI helpers",
        "WHO PEN Clinical Evidence Assistant",
        "SECRET-SAFE",
    ]

    missing = [item for item in required if item not in source]
    if missing:
        raise SystemExit(f"Notebook validation failed; missing: {missing}")

    code_cells = [c for c in data["cells"] if c.get("cell_type") == "code"]
    with_outputs = [i for i, c in enumerate(code_cells) if c.get("outputs")]
    if with_outputs:
        raise SystemExit(
            f"Notebook contains committed cell outputs: {with_outputs[:10]}"
        )

    print("Notebook validation: PASS")


if __name__ == "__main__":
    main()
