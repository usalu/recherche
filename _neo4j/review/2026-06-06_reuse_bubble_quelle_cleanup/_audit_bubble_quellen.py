"""Audit bubble-run Quelle nodes and BELEGT_IN edges in mit-bestand."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

RUNS = [
    "swiss_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
]

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
out: dict = {"database": db, "by_review_run": {}}
try:
    with driver.session(database=db) as s:
        for run in RUNS:
            quellen = s.run(
                """
                MATCH (q:Quelle)
                WHERE q.review_run = $run
                RETURN q.id AS id, labels(q) AS labels, q.url AS url, q.name AS name,
                       q.quelltyp AS quelltyp
                ORDER BY q.id
                """,
                run=run,
            )
            belegt = s.run(
                """
                MATCH (n)-[r:BELEGT_IN]->(q:Quelle)
                WHERE r.review_run = $run OR q.review_run = $run
                RETURN n.id AS from_id, labels(n) AS from_labels, r.id AS rid,
                       q.id AS quelle_id, r.evidence_url AS evidence_url
                ORDER BY from_id, quelle_id
                """,
                run=run,
            )
            rels_with_source_id = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.review_run = $run AND r.evidence_source_id IS NOT NULL
                RETURN count(r) AS c
                """,
                run=run,
            ).single()["c"]
            sidecar = s.run(
                """
                MATCH ()-[r]->()
                WHERE r.review_run = $run AND r.metadata_sidecar_key IS NOT NULL
                RETURN count(r) AS c
                """,
                run=run,
            ).single()["c"]
            out["by_review_run"][run] = {
                "quellen": [dict(x) for x in quellen],
                "belegt_in": [dict(x) for x in belegt],
                "rels_with_evidence_source_id": rels_with_source_id,
                "rels_with_metadata_sidecar_key": sidecar,
            }
        out["totals"] = {
            "quellen": sum(len(v["quellen"]) for v in out["by_review_run"].values()),
            "belegt_in": sum(len(v["belegt_in"]) for v in out["by_review_run"].values()),
        }
finally:
    driver.close()

path = Path(__file__).resolve().parent / "audit_report.json"
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(path)
print(json.dumps(out["totals"], indent=2))
