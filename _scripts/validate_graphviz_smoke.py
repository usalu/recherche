"""validate_graphviz_smoke.py — gate: render one small DOT graph to SVG and PDF.

Proves the installed Graphviz can produce both output formats this repo needs,
without any browser, screenshot or PDF-conversion library. Graphviz writes the
PDF directly.

    python _scripts/validate_graphviz_smoke.py

Artifacts land in the repo scratch area `_tmp/` (gitignored, regenerable):

    _tmp/graphviz-smoke-test.svg
    _tmp/graphviz-smoke-test.pdf

Exit codes: 0 = both artifacts valid, 1 = an artifact failed, 2 = Graphviz missing.
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from graphviz_env import GraphvizNotFoundError, render  # noqa: E402
from neo4j_env import repo_root  # noqa: E402

SMOKE_DOT = """digraph G {
  rankdir=LR;

  "neo4j" [
    label="Neo4j"
    shape=circle
    style=filled
  ];

  "graphviz" [
    label="Graphviz"
    shape=circle
    style=filled
  ];

  "neo4j" -> "graphviz" [
    label="EXPORTS TO"
  ];
}
"""

OUT_DIR = repo_root() / "_tmp"
SVG_PATH = OUT_DIR / "graphviz-smoke-test.svg"
PDF_PATH = OUT_DIR / "graphviz-smoke-test.pdf"


def check_svg(path: Path) -> list[str]:
    """Return a list of problems; empty means the SVG is valid."""
    problems: list[str] = []
    data = path.read_bytes()
    if not data:
        problems.append("SVG is empty")
        return problems
    text = data.decode("utf-8", errors="replace")
    if "<svg" not in text or "</svg>" not in text:
        problems.append("SVG has no <svg> root element")
    for expected in ("Neo4j", "Graphviz", "EXPORTS TO"):
        if expected not in text:
            problems.append(f"SVG is missing the label {expected!r}")
    return problems


def check_pdf(path: Path) -> list[str]:
    """Return a list of problems; empty means the PDF is valid."""
    problems: list[str] = []
    data = path.read_bytes()
    if not data:
        problems.append("PDF is empty")
        return problems
    if not data.startswith(b"%PDF-"):
        problems.append("PDF is missing the %PDF- header")
    if b"%%EOF" not in data[-2048:]:
        problems.append("PDF is missing the %%EOF trailer")
    return problems


def main() -> int:
    try:
        render(SMOKE_DOT, SVG_PATH, fmt="svg")
        render(SMOKE_DOT, PDF_PATH, fmt="pdf")
    except GraphvizNotFoundError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2
    except RuntimeError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    problems = check_svg(SVG_PATH) + check_pdf(PDF_PATH)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    print(f"OK: {SVG_PATH} ({SVG_PATH.stat().st_size} bytes)")
    print(f"OK: {PDF_PATH} ({PDF_PATH.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
