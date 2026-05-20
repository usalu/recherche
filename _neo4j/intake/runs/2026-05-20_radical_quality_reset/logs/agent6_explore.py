"""Agent 6 — exploration pass for Phase 2.4 + 2.7.

Pulls live mit-bestand state so the migrations can be authored against the
real key distribution and not against memory. Output is written to
`logs/agent6_explore.json` and is read by the runner / report.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
OUT_FILE = LOG_DIR / "agent6_explore.json"


def _resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection missing.")
    if database != "mit-bestand":
        database = "mit-bestand"
    return uri, user, password, database


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = _resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    out: dict = {"captured_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}

    with driver.session(database=database) as ses:
        # 1. Per-label distinct key counts + sum(key-pairs)
        label_keys = {}
        for lbl in [
            "Projekt",
            "Bauteilgruppe",
            "Bauwerk",
            "Materialdepot",
            "Quelle",
            "Akteur",
        ]:
            res = ses.run(
                f"""
                MATCH (n:{lbl})
                WITH n
                UNWIND keys(n) AS k
                WITH k, count(*) AS c
                RETURN k, c ORDER BY c DESC
                """
            )
            rows = [{"key": r["k"], "fill_count": r["c"]} for r in res]
            label_keys[lbl] = {
                "node_count": ses.run(
                    f"MATCH (n:{lbl}) RETURN count(n) AS c"
                ).single()["c"],
                "distinct_keys": len(rows),
                "keys": rows,
            }
        out["label_keys"] = label_keys

        # 2. Edge-with-source pollution counts
        edge_pollution = ses.run(
            """
            MATCH ()-[r]->()
            WHERE r.source IS NOT NULL
               OR r.evidence IS NOT NULL
               OR r.source_excerpt IS NOT NULL
               OR r.datenqualitaet IS NOT NULL
            RETURN type(r) AS rt, count(r) AS c ORDER BY c DESC
            """
        )
        out["edge_pollution_by_type"] = [
            {"rel_type": r["rt"], "count": r["c"]} for r in edge_pollution
        ]
        out["edge_pollution_total"] = ses.run(
            """
            MATCH ()-[r]->()
            WHERE (r.source IS NOT NULL
               OR r.evidence IS NOT NULL
               OR r.source_excerpt IS NOT NULL
               OR r.datenqualitaet IS NOT NULL)
              AND r.evidence_origin IS NULL
            RETURN count(r) AS c
            """
        ).single()["c"]

        # 3. Quelle.external_sources sample
        ext_sources = ses.run(
            """
            MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
            RETURN q.id AS id, q.external_sources AS extsrc LIMIT 5
            """
        )
        out["external_sources_sample"] = [
            {"id": r["id"], "value": r["extsrc"]} for r in ext_sources
        ]
        out["external_sources_count"] = ses.run(
            "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
        ).single()["c"]

        # 4. Sample Projekt with cost / co2 / reuse / counter keys to validate
        # field choices.
        cost_keys = [
            "baukosten_eur",
            "kosten_eur",
            "kostenreduktion_prozent",
        ]
        co2_keys = [
            "co2_einsparung_t",
            "co2_reduktion_prozent",
            "co2_reduktion_pct",
            "co2_einsparung_t_min",
            "co2_einsparung_t_max",
            "abfall_vermieden_t",
            "transportdistanz_km",
        ]
        reuse_keys = [
            "reuse_anteil_prozent",
            "reuse_anteil_volume",
            "material_passport",
        ]
        year_keys = [
            "jahr_fertigstellung",
            "fertigstellung_jahr",
            "jahr_beginn",
            "jahr",
            "jahr_fertigstellung_geplant",
            "jahr_eroeffnung",
            "fertigstellung_geplant_jahr",
            "jahr_start",
            "bau_jahr_von",
            "jahr_fertigstellung_max",
            "baujahr",
            "baujahr_von",
            "entwurfsjahr",
        ]
        area_keys = [
            "flaeche_m2",
            "flaeche_m2_min",
            "flaeche_m2_max",
            "bgf_m2",
            "flaeche_m2_alternative",
            "nutzflaeche_m2",
            "grundstueck_m2",
            "hoehe_m",
            "breite_m",
            "flaeche_sqft_min",
            "flaeche_sqft_max",
        ]
        per_field_fill = {}
        for field_group, keys in [
            ("year", year_keys),
            ("area", area_keys),
            ("cost", cost_keys),
            ("co2", co2_keys),
            ("reuse", reuse_keys),
        ]:
            counts = []
            for k in keys:
                c = ses.run(
                    f"MATCH (p:Projekt) WHERE p.`{k}` IS NOT NULL RETURN count(p) AS c"
                ).single()["c"]
                counts.append({"key": k, "fill": c})
            per_field_fill[field_group] = counts
        out["projekt_field_fill"] = per_field_fill

        # 5. One-off counter keys ending with _anzahl on Projekt
        anzahl_keys = ses.run(
            """
            MATCH (p:Projekt)
            UNWIND keys(p) AS k
            WITH k WHERE k ENDS WITH '_anzahl'
                 OR k STARTS WITH 'anzahl_'
                 OR k CONTAINS '_volumen_'
                 OR k STARTS WITH 'volumen_'
            WITH k, count(*) AS c
            RETURN k, c ORDER BY c DESC
            """
        )
        out["projekt_counter_keys"] = [
            {"key": r["k"], "fill": r["c"]} for r in anzahl_keys
        ]

        # 6. Bauteilgruppe names with menge_stueck NULL — to verify the
        # counter→BG name match heuristic has a population.
        bg_name_samples = ses.run(
            """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
            RETURN p.id AS pid, bg.id AS bgid, bg.name AS bgname,
                   bg.menge_stueck AS menge_stueck
            ORDER BY pid LIMIT 200
            """
        )
        out["bg_name_sample"] = [
            {
                "pid": r["pid"],
                "bgid": r["bgid"],
                "bgname": r["bgname"],
                "menge_stueck": r["menge_stueck"],
            }
            for r in bg_name_samples
        ]

        # 7. APOC presence test
        try:
            apoc_ver = ses.run(
                "RETURN apoc.version() AS v"
            ).single()["v"]
            out["apoc_version"] = apoc_ver
        except Exception as exc:  # noqa: BLE001
            out["apoc_version"] = None
            out["apoc_error"] = str(exc)

        # 8. Total node/rel counts
        out["total_nodes"] = ses.run("MATCH (n) RETURN count(n) AS c").single()["c"]
        out["total_rels"] = ses.run(
            "MATCH ()-[r]->() RETURN count(r) AS c"
        ).single()["c"]

        # 9. Sample Projekt to inspect typical _archive payload size we'd
        # produce
        sample_projekt = ses.run(
            """
            MATCH (p:Projekt)
            RETURN p.id AS id, size(keys(p)) AS n_keys
            ORDER BY n_keys DESC LIMIT 5
            """
        )
        out["projekt_top_key_count_nodes"] = [
            {"id": r["id"], "n_keys": r["n_keys"]} for r in sample_projekt
        ]

        # 10. counts of edges that match each pollution flavour
        out["edge_pollution_breakdown"] = {
            "with_source_only": ses.run(
                "MATCH ()-[r]->() WHERE r.source IS NOT NULL AND r.evidence IS NULL AND r.source_excerpt IS NULL RETURN count(r) AS c"
            ).single()["c"],
            "with_evidence_only": ses.run(
                "MATCH ()-[r]->() WHERE r.evidence IS NOT NULL AND r.source IS NULL AND r.source_excerpt IS NULL RETURN count(r) AS c"
            ).single()["c"],
            "with_source_excerpt": ses.run(
                "MATCH ()-[r]->() WHERE r.source_excerpt IS NOT NULL RETURN count(r) AS c"
            ).single()["c"],
            "with_evidence_origin_already": ses.run(
                "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL RETURN count(r) AS c"
            ).single()["c"],
            "with_datenqualitaet": ses.run(
                "MATCH ()-[r]->() WHERE r.datenqualitaet IS NOT NULL RETURN count(r) AS c"
            ).single()["c"],
        }

        # 11. Akteur — rolle_text on BETEILIGT_AN to inform raw_role_evidence
        out["beteiligt_an_rolle_count"] = ses.run(
            "MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r) AS c"
        ).single()["c"]

        # 12. counts_as_* on BG and similar — to drop into _archive
        bg_counts_as = ses.run(
            """
            MATCH (bg:Bauteilgruppe)
            UNWIND keys(bg) AS k
            WITH k WHERE k STARTS WITH 'counts_as_'
            WITH k, count(*) AS c RETURN k, c ORDER BY c DESC
            """
        )
        out["bg_counts_as_keys"] = [
            {"key": r["k"], "fill": r["c"]} for r in bg_counts_as
        ]

    driver.close()

    OUT_FILE.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT_FILE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
