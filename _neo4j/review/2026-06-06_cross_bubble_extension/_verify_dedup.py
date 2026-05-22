"""Post-dedup verification on mit-bestand."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
report = {}

with driver.session(database="mit-bestand") as s:
    report["counts"] = s.run(
        "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"
    ).single().data()

    report["parallel_betrieben"] = s.run(
        """
        MATCH (a)-[r1:BETRIEBEN_VON]->(b)
        MATCH (a)-[r2:VERBUNDEN_MIT_AKTEUR]->(b)
        WHERE r2.evidence_url IS NOT NULL
        RETURN count(r1) AS c
        """
    ).single()["c"]

    report["bidirectional_pairs"] = s.run(
        """
        MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]-(b)
        WHERE r.review_run IS NOT NULL AND a.id < b.id
        WITH a, b, count(r) AS c
        RETURN sum(CASE WHEN c = 2 THEN 1 ELSE 0 END) AS still_bidir,
               sum(CASE WHEN c > 2 THEN 1 ELSE 0 END) AS gt2,
               sum(CASE WHEN c = 1 THEN 1 ELSE 0 END) AS canonical
        """
    ).single().data()

    report["missing_evidence"] = s.run(
        """
        MATCH ()-[r]->()
        WHERE (r.review_run CONTAINS 'reuse_bubble' OR r.review_run CONTAINS 'cross_bubble')
          AND (r.evidence_url IS NULL OR r.evidence_confidence IS NULL)
        RETURN count(r) AS c
        """
    ).single()["c"]

    report["restado_nodes"] = [
        dict(r)
        for r in s.run(
            """
            MATCH (a)
            WHERE toLower(coalesce(a.id,'')) CONTAINS 'restado'
            RETURN a.id AS id, labels(a) AS labels
            """
        )
    ]
    rid = report["restado_nodes"][0]["id"] if report["restado_nodes"] else "software_restado"
    report["restado_edges"] = [
        dict(r)
        for r in s.run(
            """
            MATCH (a {id:$rid})-[r]-(b)
            RETURN type(r) AS t, startNode(r).id AS from_id, endNode(r).id AS to_id,
                   labels(b) AS b_labels, r.evidence_url AS url, r.evidence_confidence AS conf
            ORDER BY t, from_id
            """,
            rid=rid,
        )
    ]

    report["concular_restado_rel"] = s.run(
        """
        MATCH (a {id:'concular'})-[r:VERBUNDEN_MIT_AKTEUR]->(b {id:'software_restado'})
        RETURN r.evidence_url AS url, r.evidence_quote AS quote, r.evidence_confidence AS conf
        """
    ).single().data()

    report["superuse_verbunden"] = [
        dict(r)
        for r in s.run(
            """
            MATCH (a {id:'superuse_studios_2012architecten'})-[r:VERBUNDEN_MIT_AKTEUR]-(b)
            RETURN startNode(r).id AS from_id, endNode(r).id AS to_id,
                   r.evidence_url AS url, r.evidence_confidence AS conf
            ORDER BY from_id, to_id
            """
        )
    ]

driver.close()
out = Path(__file__).resolve().parent / "dedup_verify.json"
out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report, indent=2, ensure_ascii=False))
