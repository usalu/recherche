"""Agent 10 — read-only probe of mit-bestand before loader.

Surfaces the current state of:
  - the 8 research-file :Quelle anchors (4b.2 scope)
  - actor-registry :Akteur, :Quelle and projekt stub residue (4b.3 scope)
  - downstream invariants Agent 8 enforced (no Projekt -> actor_registry URL)

All probes are read-only. Result written to logs/agent10_probe.json.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
PROBE_JSON = LOG_DIR / "agent10_probe.json"

ANCHOR_IDS = [
    "q_aufbereitungsverfahren_reused_building_elements_md",
    "q_connection_techniques_bauteilreuse_md",
    "q_testing_verification_bauteilreuse_kg_md",
    "q_bauteilreuse_legal_regime_matrix_md",
    "q_schadstoff_reuse_knowledge_graph_research_md",
    "q_circular_construction_reuse_graph_gaps_md",
    "q_circular_construction_economics_kg_md",
    "q_energy_climate_reuse_research_md",
]


def main() -> int:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore
    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = resolve_connection()
    if not database or database == "neo4j":
        database = "mit-bestand"

    out: dict = {
        "probed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": database,
    }

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as s:
            out["totals"] = {
                "nodes": s.run("MATCH (n) RETURN count(n) AS c").single()["c"],
                "rels": s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"],
                "quelle": s.run("MATCH (q:Quelle) RETURN count(q) AS c").single()["c"],
                "akteur": s.run("MATCH (a:Akteur) RETURN count(a) AS c").single()["c"],
                "projekt": s.run("MATCH (p:Projekt) RETURN count(p) AS c").single()["c"],
            }
            out["anchors"] = []
            for aid in ANCHOR_IDS:
                row = s.run(
                    "MATCH (q:Quelle {id:$id}) "
                    "OPTIONAL MATCH (q)-[r:ZITIERT_QUELLE]->(:Quelle) "
                    "RETURN q.id AS id, q.quelltyp AS qt, q.name AS name, count(r) AS zit",
                    {"id": aid},
                ).single()
                if row is None:
                    out["anchors"].append({"id": aid, "exists": False})
                else:
                    out["anchors"].append({
                        "id": aid,
                        "exists": True,
                        "quelltyp": row["qt"],
                        "name": row["name"],
                        "zitiert_quelle_out": row["zit"],
                    })

            out["actor_registry"] = {
                "akteursliste_master": bool(
                    s.run(
                        "MATCH (q:Quelle {id:'q_akteursliste_master_md'}) RETURN count(q) AS c"
                    ).single()["c"]
                ),
                "q_actor_external_link": s.run(
                    "MATCH (q:Quelle) WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(q) AS c"
                ).single()["c"],
                "projekt_belegt_actor_registry_residual": s.run(
                    "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
                    "WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r) AS c"
                ).single()["c"],
                "akteur_belegt_actor_registry": s.run(
                    "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
                    "WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r) AS c"
                ).single()["c"],
                "akteur_belegt_master": s.run(
                    "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle {id:'q_akteursliste_master_md'}) "
                    "RETURN count(r) AS c"
                ).single()["c"],
                "assoziiert_mit_projekt_total": s.run(
                    "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r) AS c"
                ).single()["c"],
                "registry_stub_only_projects": s.run(
                    "MATCH (p:Projekt) WHERE p.import_status='registry_stub_only' RETURN count(p) AS c"
                ).single()["c"],
                "verbunden_mit_akteur_total": s.run(
                    "MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->() RETURN count(r) AS c"
                ).single()["c"],
                "hat_akteurrolle_total": s.run(
                    "MATCH ()-[r:HAT_AKTEURROLLE]->() RETURN count(r) AS c"
                ).single()["c"],
                "hat_akteurtyp_total": s.run(
                    "MATCH ()-[r:HAT_AKTEURTYP]->() RETURN count(r) AS c"
                ).single()["c"],
            }

            out["domain_nodes"] = {
                "aufbereitungsverfahren": s.run(
                    "MATCH (n:Aufbereitungsverfahren) RETURN count(n) AS c"
                ).single()["c"],
                "verbindungstechnik": s.run(
                    "MATCH (n:Verbindungstechnik) RETURN count(n) AS c"
                ).single()["c"],
                "pruefungnachweis": s.run(
                    "MATCH (n:PruefungNachweis) RETURN count(n) AS c"
                ).single()["c"],
            }

            # sample one Akteur evidence shape
            sample = s.run(
                "MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(:Akteurrolle) "
                "RETURN type(r) AS t, properties(r) AS p LIMIT 3"
            ).data()
            out["sample_akteurrolle"] = sample
            sample2 = s.run(
                "MATCH (a:Akteur)-[r:ASSOZIIERT_MIT_PROJEKT]->(:Projekt) "
                "RETURN type(r) AS t, properties(r) AS p LIMIT 3"
            ).data()
            out["sample_assoziiert"] = sample2

            # confirm akteur->BELEGT_IN->q_actor_*
            sample3 = s.run(
                "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle {quelltyp:'external_link_from_actor_registry'}) "
                "RETURN properties(r) AS p LIMIT 3"
            ).data()
            out["sample_akteur_belegt_actor_url"] = sample3
    finally:
        driver.close()

    PROBE_JSON.parent.mkdir(parents=True, exist_ok=True)
    PROBE_JSON.write_text(
        json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(out, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
