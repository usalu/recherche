"""check_graphviz.py — report whether Graphviz is installed and usable.

Prints availability, version, executable path, the layout engines this repo relies
on, and whether SVG and PDF output actually work (rendered into a throwaway temp
directory, nothing is written into the repo).

    python _scripts/check_graphviz.py
    python _scripts/check_graphviz.py --json

Exit codes: 0 = usable, 1 = installed but SVG/PDF or an engine failed, 2 = not found.
Setup and troubleshooting: _scripts/GRAPHVIZ_SETUP.md
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from graphviz_env import (  # noqa: E402
    LAYOUT_ENGINES,
    GraphvizNotFoundError,
    probe_graphviz,
    render,
)

_PROBE_GRAPH = 'digraph G { "a" -> "b"; }'


def check_format(fmt: str) -> tuple[bool, str]:
    """Render a two-node graph to `fmt` in a temp dir; report success and detail."""
    try:
        with tempfile.TemporaryDirectory(prefix="graphviz-check-") as tmpdir:
            out = render(_PROBE_GRAPH, Path(tmpdir) / f"probe.{fmt}", fmt=fmt)
            size = out.stat().st_size
            if size == 0:
                return False, "rendered file is empty"
            return True, f"{size} bytes"
    except (GraphvizNotFoundError, RuntimeError, OSError) as exc:
        return False, str(exc)


def build_report() -> dict:
    report = probe_graphviz()
    if not report["available"]:
        report["formats"] = {}
        return report
    report["formats"] = {
        fmt: dict(zip(("ok", "detail"), check_format(fmt)))
        for fmt in ("svg", "pdf")
    }
    return report


def format_text(report: dict) -> str:
    lines: list[str] = []
    if not report["available"]:
        lines.append("Graphviz available: NO")
        lines.append("  dot executable: not found")
        lines.append("")
        lines.append("Install it and re-run — see _scripts/GRAPHVIZ_SETUP.md")
        return "\n".join(lines)

    lines.append("Graphviz available: YES")
    lines.append(f"  version:        {report['version']}")
    lines.append(f"  dot executable: {report['dot_path']}")
    lines.append(f"  resolved via:   {report['source']}")
    lines.append("")
    lines.append("Layout engines:")
    for engine in LAYOUT_ENGINES:
        info = report["engines"].get(engine, {})
        mark = "ok" if info.get("available") else "MISSING"
        lines.append(f"  {mark:<8} {engine:<6} {info.get('path') or ''}")
    lines.append("")
    lines.append("Output formats:")
    for fmt, info in report["formats"].items():
        mark = "ok" if info["ok"] else "FAIL"
        lines.append(f"  {mark:<8} {fmt:<6} {info['detail']}")
    return "\n".join(lines)


def exit_code(report: dict) -> int:
    if not report["available"]:
        return 2
    engines_ok = all(report["engines"][e]["available"] for e in LAYOUT_ENGINES)
    formats_ok = all(info["ok"] for info in report["formats"].values())
    return 0 if engines_ok and formats_ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Report Graphviz availability and capabilities.")
    ap.add_argument("--json", action="store_true", help="Emit the report as JSON")
    args = ap.parse_args()

    report = build_report()
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(format_text(report))
    return exit_code(report)


if __name__ == "__main__":
    sys.exit(main())
