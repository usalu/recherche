"""Run pre_flight_validation.cypher against the live graph and emit results JSON.

Parses the validation file into named blocks (separated by `// ----` lines plus
section headers `// SXX --`), runs each block, and captures the result rows
alongside the inline `// EXPECTED:` comment for diffability.

Outputs to a JSON file alongside the Cypher input; prints a short summary to
stdout indicating which sections returned unexpected counts.

Example:
  python _scripts/run_preflight_validation.py \\
      --cypher _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_validation.cypher \\
      --out    _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_results.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


_SECTION_HEADER = re.compile(r"^//\s*(S\d+)\s*[—-]+\s*(.*)$")
_EXPECTED = re.compile(r"^//\s*EXPECTED:\s*(.*)$", re.IGNORECASE)


def parse_blocks(text: str) -> list[dict]:
    """Split the cypher file into block dicts: {section_id, title, cypher, expected}."""
    blocks: list[dict] = []
    current_section_id: str | None = None
    current_title: str | None = None
    buffer: list[str] = []
    expected: list[str] = []

    def flush() -> None:
        if current_section_id is None:
            return
        cypher = "\n".join(
            line for line in buffer
            if not line.strip().startswith("//") and line.strip()
        ).strip()
        if cypher:
            blocks.append({
                "section_id": current_section_id,
                "title": current_title or "",
                "cypher": cypher,
                "expected": " ".join(expected).strip(),
            })

    for raw_line in text.splitlines():
        header_match = _SECTION_HEADER.match(raw_line.strip())
        if header_match:
            flush()
            current_section_id = header_match.group(1)
            current_title = header_match.group(2).strip()
            buffer = []
            expected = []
            continue
        expected_match = _EXPECTED.match(raw_line.strip())
        if expected_match:
            expected.append(expected_match.group(1).strip())
            continue
        buffer.append(raw_line)

    flush()
    return blocks


def run_blocks(blocks: list[dict]) -> list[dict]:
    """Execute each block; capture rows or error."""
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    results: list[dict] = []

    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            for block in blocks:
                result_entry = {
                    "section_id": block["section_id"],
                    "title": block["title"],
                    "expected": block["expected"],
                    "cypher": block["cypher"],
                    "rows": [],
                    "row_count": 0,
                    "error": None,
                }
                try:
                    # Some blocks contain multiple top-level statements
                    # separated by ; -- split and run each
                    statements = [
                        s.strip()
                        for s in block["cypher"].split(";")
                        if s.strip()
                    ]
                    all_rows: list[dict] = []
                    for stmt in statements:
                        rec_list = list(session.run(stmt))
                        for rec in rec_list:
                            all_rows.append({k: rec[k] for k in rec.keys()})
                    result_entry["rows"] = all_rows
                    result_entry["row_count"] = len(all_rows)
                except Exception as exc:
                    result_entry["error"] = f"{type(exc).__name__}: {exc}"
                results.append(result_entry)
    finally:
        driver.close()

    return results


def summarize(results: list[dict]) -> str:
    out: list[str] = []
    errors = [r for r in results if r["error"]]
    if errors:
        out.append(f"!! {len(errors)} block(s) errored:")
        for r in errors:
            out.append(f"   {r['section_id']} — {r['title']}: {r['error']}")
        out.append("")
    out.append(f"Total blocks: {len(results)}")
    out.append(f"  - succeeded: {len(results) - len(errors)}")
    out.append(f"  - errored:   {len(errors)}")
    out.append("")
    out.append("Per-section row counts (sanity check vs 'EXPECTED' inline comments):")
    out.append("")
    for r in results:
        if r["error"]:
            mark = "!!"
        else:
            mark = "  "
        out.append(f"  {mark} {r['section_id']:<5}  rows={r['row_count']:>4}  {r['title']}")
        if r["expected"]:
            out.append(f"              expected: {r['expected'][:90]}")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cypher", required=True, type=Path,
                    help="Path to pre_flight_validation.cypher")
    ap.add_argument("--out", required=True, type=Path,
                    help="Path to write results JSON")
    args = ap.parse_args()

    text = args.cypher.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    if not blocks:
        print("No parseable blocks found in", args.cypher, file=sys.stderr)
        return 2

    print(f"Parsed {len(blocks)} blocks from {args.cypher.name}")
    results = run_blocks(blocks)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {args.out}")
    print()
    print(summarize(results))
    return 0


if __name__ == "__main__":
    sys.exit(main())
