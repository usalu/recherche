"""Verify no bubble quellen remain and rel evidence is on properties."""
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
out: dict = {"database": db}
try:
    with driver.session(database=db) as s:
        out["counts"] = {
            "nodes": s.run("MATCH (n) RETURN count(n) AS c").single()["c"],
            "relationships": s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
        }
        out["bubble_quellen_remaining"] = s.run(
            "MATCH (q:Quelle) WHERE q.review_run IN $runs RETURN count(q) AS c",
            runs=RUNS,
        ).single()["c"]
        out["bubble_belegt_remaining"] = s.run(
            """
            MATCH ()-[r:BELEGT_IN]->()
            WHERE r.review_run IN $runs
            RETURN count(r) AS c
            """,
            runs=RUNS,
        ).single()["c"]
        out["pointer_props_remaining"] = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.review_run IN $runs
              AND (r.evidence_source_id IS NOT NULL OR r.metadata_sidecar_key IS NOT NULL)
            RETURN count(r) AS c
            """,
            runs=RUNS,
        ).single()["c"]
        out["rels_missing_evidence_url"] = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.review_run IN $runs AND r.evidence_url IS NULL
            RETURN count(r) AS c
            """,
            runs=RUNS,
        ).single()["c"]
        out["sample_actor_urls"] = [
            dict(x)
            for x in s.run(
                """
                MATCH (a:Akteur)
                WHERE a.primary_source_url IS NOT NULL
                RETURN a.id AS id, a.primary_source_url AS primary_source_url,
                       a.source_urls AS source_urls
                ORDER BY a.id
                LIMIT 15
                """
            )
        ]
        out["dangling_evidence_source_id"] = s.run(
            """
            MATCH ()-[r]->()
            WHERE r.evidence_source_id IS NOT NULL
            OPTIONAL MATCH (q:Quelle {id: r.evidence_source_id})
            WITH r, q WHERE q IS NULL
            RETURN count(r) AS c
            """
        ).single()["c"]
finally:
    driver.close()

path = Path(__file__).resolve().parent / "post_cleanup_verify.json"
path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(path)
print(json.dumps({k: out[k] for k in out if k != "sample_actor_urls"}, indent=2))
