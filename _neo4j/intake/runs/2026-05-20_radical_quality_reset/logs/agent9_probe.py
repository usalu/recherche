"""Agent 9 — pre-loader probe.

Inspect what already exists for Agent 9 / Phase 4b.1:
  - List all :Projekt ids (so we know what to MATCH on per dossier slug)
  - List all :Quelle case_markdown ids (to confirm manifest 'live_quelle_id')
  - Count today: case_markdown :Quelle with >=1 :ZITIERT_QUELLE child
  - Sample a couple of case_markdown :Quelle that DO have ZITIERT_QUELLE
    children to confirm the q_<slug>_sN convention

Output: agent9_probe.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
OUT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
    / "logs"
    / "agent9_probe.json"
)


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    uri, user, pw, db = _resolve()
    drv = GraphDatabase.driver(uri, auth=(user, pw))
    out: dict = {}
    try:
        with drv.session(database=db) as s:
            out["projekt_ids"] = sorted(
                r["id"] for r in s.run("MATCH (p:Projekt) RETURN p.id AS id")
            )
            out["case_markdown_quelle_ids"] = sorted(
                r["id"] for r in s.run(
                    "MATCH (q:Quelle) WHERE q.quelltyp='case_markdown' RETURN q.id AS id"
                )
            )
            out["case_markdown_with_citing_children"] = s.run(
                """
                MATCH (q:Quelle) WHERE q.quelltyp='case_markdown'
                WITH q
                WHERE size([(q)-[:ZITIERT_QUELLE]->() | 1]) >= 1
                RETURN count(q) AS c
                """
            ).single()["c"]
            out["case_markdown_total"] = s.run(
                "MATCH (q:Quelle) WHERE q.quelltyp='case_markdown' RETURN count(q) AS c"
            ).single()["c"]
            out["sref_pattern_examples"] = sorted(
                r["id"] for r in s.run(
                    "MATCH (q:Quelle) WHERE q.id ENDS WITH '_s1' OR q.id ENDS WITH '_s2' "
                    "RETURN q.id AS id LIMIT 30"
                )
            )
            out["all_quelltyp_counts"] = {
                r["t"]: r["c"]
                for r in s.run(
                    "MATCH (q:Quelle) RETURN q.quelltyp AS t, count(q) AS c "
                    "ORDER BY c DESC"
                )
            }
            out["projekt_count"] = len(out["projekt_ids"])
            out["case_markdown_count"] = len(out["case_markdown_quelle_ids"])
    finally:
        drv.close()

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"  Projekt: {out['projekt_count']}")
    print(f"  case_markdown Quelle: {out['case_markdown_count']}")
    print(f"  case_markdown w/ ZITIERT_QUELLE child: {out['case_markdown_with_citing_children']}")
    print(f"  quelltyp counts: {out['all_quelltyp_counts']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
