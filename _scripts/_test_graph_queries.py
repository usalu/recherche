"""Run each Cypher block from a file, classify result, and report whether the
output is a GRAPH (contains Node / Relationship / Path values) or a TABLE
(scalars only)."""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path

# Force UTF-8 stdout so em-dashes / arrows in titles survive cp1252 console.
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


HEADER_RE = re.compile(r"^//\s*([GS]\d+)\s*[-—]+\s*(.+?)\s*$", re.MULTILINE)


def strip_inline_comments(text: str) -> str:
    return re.sub(r"//[^\n]*", "", text)


def split_blocks(text: str, prefix: str) -> list[tuple[str, str, str]]:
    """Return list of (label, title, cypher) for every Gn or Sn block in file."""
    headers = [
        (m.start(), m.group(1), m.group(2))
        for m in HEADER_RE.finditer(text)
        if m.group(1).startswith(prefix)
    ]
    out: list[tuple[str, str, str]] = []
    for i, (pos, label, title) in enumerate(headers):
        end = headers[i + 1][0] if i + 1 < len(headers) else len(text)
        body = text[pos:end]
        cleaned = strip_inline_comments(body).strip()
        cleaned = cleaned.strip(";").strip()
        if cleaned:
            out.append((label, title, cleaned + ";"))
    return out


def classify(record_values: list) -> tuple[str, dict]:
    """Inspect a result row and decide GRAPH vs TABLE."""
    from neo4j.graph import Node, Path, Relationship

    counts = {"nodes": 0, "rels": 0, "paths": 0, "scalars": 0, "lists": 0}
    for v in record_values:
        if isinstance(v, Node):
            counts["nodes"] += 1
        elif isinstance(v, Relationship):
            counts["rels"] += 1
        elif isinstance(v, Path):
            counts["paths"] += 1
        elif isinstance(v, list):
            counts["lists"] += 1
            for inner in v:
                if isinstance(inner, Node):
                    counts["nodes"] += 1
                elif isinstance(inner, Relationship):
                    counts["rels"] += 1
                elif isinstance(inner, Path):
                    counts["paths"] += 1
        else:
            counts["scalars"] += 1
    is_graph = counts["nodes"] + counts["rels"] + counts["paths"] > 0
    return ("GRAPH" if is_graph else "TABLE"), counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cypher", required=True, type=Path)
    ap.add_argument("--prefix", default="G", help="block label prefix (G or S)")
    ap.add_argument("--probe-limit", type=int, default=3,
                    help="rows per query to fetch for classification")
    args = ap.parse_args()

    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    text = args.cypher.read_text(encoding="utf-8")
    blocks = split_blocks(text, args.prefix)
    print(f"Parsed {len(blocks)} {args.prefix}* blocks from {args.cypher.name}\n")

    summary_rows: list[tuple[str, str, str, int, dict]] = []
    try:
        with driver.session(database=database) as session:
            for label, title, stmt in blocks:
                # Wrap query with a smaller LIMIT for the probe — we just need
                # to confirm output TYPE, not pull 5000 rows.
                probe_stmt = stmt.rstrip(";")
                # Strip trailing LIMIT clause if present, then add probe LIMIT.
                probe_stmt = re.sub(r"\bLIMIT\s+\d+\s*$", "", probe_stmt,
                                    flags=re.IGNORECASE).rstrip()
                probe_stmt = f"{probe_stmt}\nLIMIT {args.probe_limit}"
                try:
                    rows = list(session.run(probe_stmt))
                    if not rows:
                        kind, counts = "EMPTY", {}
                        n_rows = 0
                    else:
                        kind, counts = classify(list(rows[0].values()))
                        n_rows = len(rows)
                    # Also run the full LIMIT 5000 in COUNT mode to estimate volume.
                    full_count_stmt = (
                        f"CALL {{ {stmt.rstrip(';')} }} "
                        f"RETURN count(*) AS n"
                    )
                    try:
                        cn = session.run(full_count_stmt).single()
                        full_n = cn["n"] if cn else None
                    except Exception:
                        full_n = None
                    flag = "OK" if kind == "GRAPH" else ("EMPTY" if kind == "EMPTY" else "FAIL")
                    print(f"[{label}] {flag:5s} kind={kind:5s} probe_rows={n_rows} "
                          f"counts={counts} full_rows={full_n}  — {title}")
                    summary_rows.append((label, title, kind, full_n or 0, counts))
                except Exception as exc:
                    print(f"[{label}] ERROR  — {title}\n        {type(exc).__name__}: {str(exc)[:300]}")
                    summary_rows.append((label, title, "ERROR", 0, {}))
    finally:
        driver.close()

    print("\n=== SUMMARY ===")
    graph = sum(1 for r in summary_rows if r[2] == "GRAPH")
    table = sum(1 for r in summary_rows if r[2] == "TABLE")
    empty = sum(1 for r in summary_rows if r[2] == "EMPTY")
    error = sum(1 for r in summary_rows if r[2] == "ERROR")
    print(f"GRAPH:{graph}  TABLE:{table}  EMPTY:{empty}  ERROR:{error}  (of {len(summary_rows)})")
    return 0 if (table == 0 and error == 0 and empty == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
