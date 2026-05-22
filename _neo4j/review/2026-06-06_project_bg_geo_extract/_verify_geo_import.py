"""Post-apply verification for geo import."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent

QUERIES = {
    "projekte_adresse": "MATCH (p:Projekt) WHERE p.adresse IS NOT NULL RETURN count(p) AS n",
    "projekte_coords": "MATCH (p:Projekt) WHERE p.latitude IS NOT NULL AND p.longitude IS NOT NULL RETURN count(p) AS n",
    "bauwerke_adresse": "MATCH (bw:Bauwerk) WHERE bw.adresse IS NOT NULL RETURN count(bw) AS n",
    "bauwerke_coords": "MATCH (bw:Bauwerk) WHERE bw.latitude IS NOT NULL RETURN count(bw) AS n",
    "staedte_coords": "MATCH (s:Stadt) WHERE s.latitude IS NOT NULL RETURN count(s) AS n",
    "graph_counts": "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels",
    "low_confidence": "MATCH (p:Projekt) WHERE p.geo_confidence = 'low' RETURN collect(p.id) AS ids",
    "donor_without_coords": """
        MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER]->(bw:Bauwerk)
        WHERE bw.adresse IS NOT NULL AND bw.latitude IS NULL
        RETURN count(DISTINCT bw) AS n
    """,
}


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    report: dict = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "checks": {},
    }
    with driver.session(database=database) as session:
        for name, q in QUERIES.items():
            row = session.run(q).single()
            report["checks"][name] = dict(row) if row else None
    driver.close()

    counts = report["checks"]["graph_counts"]
    cov = report["checks"]
    report["acceptance"] = {
        "projekte_adresse_ok": cov["projekte_adresse"]["n"] >= 80,
        "bauwerke_adresse_ok": cov["bauwerke_adresse"]["n"] >= 160,
        "staedte_coords_ok": cov["staedte_coords"]["n"] >= 70,
        "structure_unchanged": counts["nodes"] == 2304 and counts["rels"] == 15527,
    }
    report["passed"] = all(report["acceptance"].values())

    out = OUT / "verify_report.json"
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
