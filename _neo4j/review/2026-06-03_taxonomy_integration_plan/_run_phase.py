"""
Lightweight Cypher runner for the taxonomy integration phases.

Handles:
  - `:param NAME => { ... };` blocks (cypher-shell client-side parameters)
    -> collected into a params dict and passed to every subsequent session.run()
  - Statement splitting on `;` (with // comments stripped)
  - LOAD CSV is NOT supported here — convert to UNWIND with inline data first

Usage:
  python _run_phase.py --cypher phase0_4_relabel_prog_projects.cypher
  python _run_phase.py --cypher phase5_evidence.cypher --quiet
"""
from __future__ import annotations
import argparse
import re
import sys
import time
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[3] / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def parse_params_and_statements(text: str) -> tuple[dict, list[str]]:
    """Extract `:param NAME => VALUE;` blocks; return (params_dict, remaining_statements).
    VALUE can be a {...} map literal or a [...] list literal; we eval it as Python."""
    params = {}

    # Match :param NAME => VALUE; where VALUE balances braces/brackets across lines
    pat = re.compile(
        r":param\s+(\w+)\s*=>\s*(\{.*?\}|\[.*?\])\s*;",
        re.DOTALL,
    )
    text_no_params = text
    for m in pat.finditer(text):
        name = m.group(1)
        val_str = m.group(2)
        # Convert Cypher map literal to Python dict-literal:
        # { key: 'val', key: 'val' }  ->  { 'key': 'val', 'key': 'val' }
        # but only the first key of each `key: ` pair needs quoting.
        if val_str.startswith("{"):
            # quote unquoted keys
            quoted = re.sub(r"([\{,]\s*)([a-zA-Z_][\w]*)\s*:", r"\1'\2':", val_str)
            try:
                params[name] = eval(quoted)
            except Exception as e:
                print(f"  WARN: could not parse :param {name}: {e}", file=sys.stderr)
        else:
            try:
                params[name] = eval(val_str)
            except Exception as e:
                print(f"  WARN: could not parse :param {name}: {e}", file=sys.stderr)

    text_no_params = pat.sub("", text)
    return params, text_no_params


def strip_comments(text: str) -> str:
    """Strip // line comments while preserving // inside single-quoted strings (e.g. URLs)."""
    # Match a single-quoted string (with \\' escapes) OR a // comment-to-EOL.
    # Replace comments with empty string, preserve strings as-is.
    pattern = re.compile(r"'(?:[^'\\]|\\.)*'|(//[^\n]*)", re.DOTALL)
    def repl(m):
        return "" if m.group(1) else m.group(0)
    return pattern.sub(repl, text)


def split_statements(text: str) -> list[str]:
    """Split on `;` boundaries, ignoring `;` inside single-quoted strings."""
    text = strip_comments(text)
    parts: list[str] = []
    buf: list[str] = []
    in_str = False
    i = 0
    while i < len(text):
        c = text[i]
        if in_str:
            if c == "\\" and i + 1 < len(text):
                buf.append(c); buf.append(text[i+1]); i += 2; continue
            if c == "'":
                in_str = False
            buf.append(c)
        else:
            if c == "'":
                in_str = True; buf.append(c)
            elif c == ";":
                parts.append("".join(buf).strip())
                buf = []
            else:
                buf.append(c)
        i += 1
    if buf:
        parts.append("".join(buf).strip())
    return [p for p in parts if p]


def format_counters(c) -> str:
    parts = []
    if c.nodes_created:      parts.append(f"+{c.nodes_created}n")
    if c.nodes_deleted:      parts.append(f"-{c.nodes_deleted}n")
    if c.relationships_created: parts.append(f"+{c.relationships_created}r")
    if c.relationships_deleted: parts.append(f"-{c.relationships_deleted}r")
    if c.properties_set:     parts.append(f"~{c.properties_set}p")
    if c.labels_added:       parts.append(f"+{c.labels_added}L")
    if c.labels_removed:     parts.append(f"-{c.labels_removed}L")
    if c.constraints_added:  parts.append(f"+{c.constraints_added}C")
    if c.constraints_removed: parts.append(f"-{c.constraints_removed}C")
    if c.indexes_added:      parts.append(f"+{c.indexes_added}I")
    return " ".join(parts) if parts else "no_changes"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cypher", required=True, type=Path)
    ap.add_argument("--quiet", action="store_true", help="Suppress per-statement detail")
    ap.add_argument("--show-rows", type=int, default=10,
                    help="Max RETURN rows to show per statement (0 = hide)")
    args = ap.parse_args()

    text = args.cypher.read_text(encoding="utf-8")
    params, text_no_params = parse_params_and_statements(text)
    statements = split_statements(text_no_params)

    print(f"=== {args.cypher.name} ===")
    print(f"Parsed {len(statements)} statements, {len(params)} :param blocks: {list(params.keys())}")
    print()

    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password), connection_timeout=30)

    ok = 0
    err = 0
    start = time.time()
    try:
        with driver.session(database=database) as session:
            for i, stmt in enumerate(statements, 1):
                try:
                    result = session.run(stmt, params)
                    rows = list(result)
                    summary = result.consume()
                    counters = format_counters(summary.counters)
                    short = stmt[:80].replace("\n", " ").strip()
                    if not args.quiet:
                        print(f"  [{i:>3}/{len(statements)}] OK  {counters:<25}  rows={len(rows):<4}  {short}...")
                        if args.show_rows and rows:
                            for r in rows[:args.show_rows]:
                                print(f"      -> {dict(r)}")
                            if len(rows) > args.show_rows:
                                print(f"      -> ... +{len(rows) - args.show_rows} more rows")
                    ok += 1
                except Exception as exc:
                    err += 1
                    short = stmt[:200].replace("\n", " ").strip()
                    print(f"  [{i:>3}/{len(statements)}] FAIL: {type(exc).__name__}: {str(exc)[:200]}")
                    print(f"      stmt: {short}...")
    finally:
        driver.close()
    elapsed = time.time() - start
    print()
    print(f"Done: {ok} ok, {err} failed in {elapsed:.1f}s")
    return 0 if err == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
