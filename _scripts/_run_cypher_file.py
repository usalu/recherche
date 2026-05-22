"""Run a multi-statement Cypher file against the live database.

Splits on `;` boundaries (ignoring `;` inside `//` comments) and executes each
statement. Captures result row counts per statement. Idempotent for MERGE-based
scripts like Phase 15 GEHÖRT_ZU.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


def strip_comments(text: str) -> str:
    # Remove // single-line comments
    return re.sub(r'//[^\n]*', '', text)


def split_statements(text: str) -> list[str]:
    """Split Cypher text on ; that ends a statement, ignoring blank lines."""
    text = strip_comments(text)
    parts = [p.strip() for p in text.split(';')]
    return [p for p in parts if p]


def format_counters(counters) -> str:
    parts: list[str] = []
    if counters.nodes_created:
        parts.append(f'nodes_created={counters.nodes_created}')
    if counters.nodes_deleted:
        parts.append(f'nodes_deleted={counters.nodes_deleted}')
    if counters.relationships_created:
        parts.append(f'rels_created={counters.relationships_created}')
    if counters.relationships_deleted:
        parts.append(f'rels_deleted={counters.relationships_deleted}')
    if counters.properties_set:
        parts.append(f'properties_set={counters.properties_set}')
    if counters.labels_added:
        parts.append(f'labels_added={counters.labels_added}')
    if counters.labels_removed:
        parts.append(f'labels_removed={counters.labels_removed}')
    return '  '.join(parts) if parts else 'no_changes'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--cypher', required=True, type=Path)
    args = ap.parse_args()

    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    text = args.cypher.read_text(encoding='utf-8')
    statements = split_statements(text)
    print(f'Parsed {len(statements)} statements from {args.cypher.name}')

    ok = 0
    err = 0
    try:
        with driver.session(database=database) as session:
            for i, stmt in enumerate(statements, 1):
                try:
                    result = session.run(stmt)
                    summary = result.consume()
                    counters = summary.counters
                    print(f'  [{i}/{len(statements)}] OK  {format_counters(counters)}')
                    ok += 1
                except Exception as exc:
                    err += 1
                    print(f'  [{i}/{len(statements)}] FAIL: {type(exc).__name__}: {str(exc)[:200]}')
    finally:
        driver.close()

    print()
    print(f'Done: {ok} ok, {err} failed.')
    return 0 if err == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
