"""Post-apply acceptance checks for entwurfsqualitaet v2."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

SKIP = [
    "p_maison_dna_asse",
    "p_schaerenmoosstrasse_zuerich",
    "p_maison_des_canaux_paris",
]


def main() -> int:
    uri, user, pw, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pw))
    checks: dict = {}
    with driver.session(database=db) as s:
        checks["nodes"] = s.run("MATCH (n) RETURN count(n)").single()[0]
        checks["rels"] = s.run("MATCH ()-[r]->() RETURN count(r)").single()[0]
        checks["em_active"] = s.run(
            "MATCH (em:Entwurfsmethodik) WHERE NOT em:DEPRECATED RETURN count(em)"
        ).single()[0]
        checks["ae_active"] = s.run(
            "MATCH (ae:Architekturergebnis) WHERE NOT ae:DEPRECATED RETURN count(ae)"
        ).single()[0]
        checks["em_deprecated"] = s.run(
            "MATCH (em:Entwurfsmethodik:DEPRECATED) RETURN count(em)"
        ).single()[0]
        checks["ae_deprecated"] = s.run(
            "MATCH (ae:Architekturergebnis:DEPRECATED) RETURN count(ae)"
        ).single()[0]
        checks["em_edges"] = s.run(
            "MATCH ()-[r:HAT_ENTWURFSMETHODIK]->() RETURN count(r)"
        ).single()[0]
        checks["ae_edges"] = s.run(
            "MATCH ()-[r:HAT_ARCHITEKTURERGEBNIS]->() RETURN count(r)"
        ).single()[0]
        checks["projekte_mit_beschreibung"] = s.run(
            """
            MATCH (p:Projekt)
            WHERE p.entwurfsbeschreibung IS NOT NULL
              AND trim(p.entwurfsbeschreibung) <> ''
            RETURN count(p)
            """
        ).single()[0]
        checks["skip_no_edges"] = [
            dict(
                s.run(
                    """
                    MATCH (p:Projekt {id: $id})
                    OPTIONAL MATCH (p)-[e:HAT_ENTWURFSMETHODIK|HAT_ARCHITEKTURERGEBNIS]->()
                    RETURN p.id AS id, count(e) AS edges
                    """,
                    id=pid,
                ).single()
            )
            for pid in SKIP
        ]
        missing = [
            dict(r)
            for r in s.run(
                """
                MATCH (n)
                WHERE (n:Entwurfsmethodik OR n:Architekturergebnis)
                  AND NOT n:DEPRECATED
                  AND (n.beschreibung IS NULL OR trim(n.beschreibung) = '')
                RETURN n.id AS id
                """
            )
        ]
        checks["missing_beschreibung"] = missing
        checks["all_beschreibung"] = len(missing) == 0
        max_em = s.run(
            """
            MATCH (em:Entwurfsmethodik)
            WHERE NOT em:DEPRECATED
            OPTIONAL MATCH ()-[:HAT_ENTWURFSMETHODIK]->(em)
            WITH em, count(*) AS c
            RETURN max(c) AS m
            """
        ).single()["m"]
        max_ae = s.run(
            """
            MATCH (ae:Architekturergebnis)
            WHERE NOT ae:DEPRECATED
            OPTIONAL MATCH ()-[:HAT_ARCHITEKTURERGEBNIS]->(ae)
            WITH ae, count(*) AS c
            RETURN max(c) AS m
            """
        ).single()["m"]
        checks["max_em_pct"] = round(100 * max_em / 79, 1)
        checks["max_ae_pct"] = round(100 * max_ae / 79, 1)
        checks["pass"] = (
            checks["em_active"] == 8
            and checks["ae_active"] == 8
            and checks["em_edges"] == 79
            and checks["ae_edges"] == 79
            and checks["em_deprecated"] == 8
            and checks["ae_deprecated"] == 8
            and checks["all_beschreibung"]
            and all(r["edges"] == 0 for r in checks["skip_no_edges"])
        )
    driver.close()

    out = Path(__file__).resolve().parent / "verify_v2_report.json"
    out.write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0 if checks["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
