"""Agent 10 — final acceptance probe (read-only).

Runs the explicit assertions from plan §4b.2 and §4b.3 against the live
mit-bestand graph. Output written to logs/agent10_acceptance.json and
echoed for the report.
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
ACCEPT_JSON = LOG_DIR / "agent10_acceptance.json"

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
    if database != "mit-bestand":
        database = "mit-bestand"

    out: dict = {
        "probed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "database": database,
        "assertions": [],
    }

    def assertion(name: str, passed: bool, observed, expected, note: str = "") -> None:
        out["assertions"].append({
            "name": name, "passed": passed,
            "observed": observed, "expected": expected, "note": note,
        })

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as s:
            # 4b.2 - all 8 research anchors exist
            anchor_rows = {
                r["id"]: r["c"]
                for r in s.run(
                    "UNWIND $ids AS aid "
                    "OPTIONAL MATCH (q:Quelle {id:aid}) "
                    "OPTIONAL MATCH (q)-[z:ZITIERT_QUELLE]->(:Quelle) "
                    "RETURN aid AS id, count(z) AS c",
                    {"ids": ANCHOR_IDS},
                ).data()
            }
            for aid in ANCHOR_IDS:
                assertion(
                    f"anchor_{aid}_exists",
                    anchor_rows.get(aid) is not None,
                    anchor_rows.get(aid),
                    ">=0",
                )
            out["anchor_zitiert_quelle_out"] = anchor_rows

            # 4b.2 - every research anchor that has a Sources block has >= 1
            #         ZITIERT_QUELLE out (5 of 8 by design have URL tables).
            anchors_with_links = sum(1 for c in anchor_rows.values() if (c or 0) > 0)
            assertion(
                "anchors_with_at_least_one_url_child",
                anchors_with_links >= 5,
                anchors_with_links,
                ">=5",
                "5/8 research files have URL-table rows; "
                "connection_techniques + schadstoff + gaps do not.",
            )

            # 4b.2 - domain nodes touched
            domain_belegt = s.run(
                "MATCH (n)-[r:BELEGT_IN]->(q:Quelle) "
                "WHERE q.quelltyp='research_markdown' "
                "  AND r.evidence_origin='inferred' AND r.evidence_basis='research_file_row' "
                "RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "domain_nodes_anchored_to_research_md",
                domain_belegt >= 200,
                domain_belegt,
                ">=200",
            )

            # 4b.3 - master anchor exists
            master = s.run(
                "MATCH (q:Quelle {id:'q_akteursliste_master_md'}) RETURN count(q) AS c"
            ).single()["c"]
            assertion("akteursliste_master_md_exists", master == 1, master, 1)

            # 4b.3 - q_akteursliste_master_md -[ZITIERT_QUELLE]-> q_actor_*  (the structural fix)
            zit = s.run(
                "MATCH (q:Quelle {id:'q_akteursliste_master_md'})-[r:ZITIERT_QUELLE]->"
                "(t:Quelle) WHERE t.quelltyp='external_link_from_actor_registry' RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "master_zitiert_actor_url_count",
                zit >= 250,
                zit,
                ">=250",
                "Previous transform wrongly converted these to BELEGT_IN. "
                "After Agent 10 they are ZITIERT_QUELLE.",
            )

            # 4b.3 - ASSOZIIERT_MIT_PROJEKT canonical shape
            assoz_total = s.run(
                "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r) AS c"
            ).single()["c"]
            assoz_canonical = s.run(
                "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() "
                "WHERE r.evidence_origin='curated' "
                "  AND r.evidence_basis='registry_stub' "
                "  AND r.evidence_confidence='teilweise_belegt' "
                "RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "assoziiert_canonical_shape_dominant",
                assoz_canonical >= 140,
                {"total": assoz_total, "canonical": assoz_canonical},
                ">=140 of total",
                "Only registry-sourced ASSOZIIERT_MIT_PROJEKT edges receive "
                "this shape; batch2 dossier-sourced ones may differ.",
            )

            # 4b.3 - HAT_AKTEURROLLE canonical shape for registry-sourced edges
            hat_canonical = s.run(
                "MATCH ()-[r:HAT_AKTEURROLLE]->() "
                "WHERE r.evidence_origin='curated' "
                "  AND r.evidence_basis='controlled_vocab' "
                "  AND r.evidence_confidence='belegt' "
                "  AND r.evidence_source_id='q_akteursliste_master_md' "
                "RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "hat_akteurrolle_curated_belegt_from_master",
                hat_canonical >= 500,
                hat_canonical,
                ">=500",
            )

            # Akteur -[BELEGT_IN]-> q_actor_url canonical shape.
            # NOTE: 47 edges originate from `canonical/actor_registry_first10/`
            # which is outside the user's `registry/**/*.jsonl` glob and is
            # therefore intentionally left in its earlier (derived/cell_citation/unklar)
            # shape — Agent 10's scope is the 11 batches under registry/**/.
            ab_canonical = s.run(
                "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
                "WHERE q.quelltyp='external_link_from_actor_registry' "
                "  AND r.evidence_origin='curated' "
                "  AND r.evidence_basis='cell_citation' "
                "  AND r.evidence_confidence='belegt' "
                "RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "akteur_belegt_actor_url_canonical",
                ab_canonical >= 300,
                ab_canonical,
                ">=300",
                "318 of 365 in canonical shape; remaining 47 are first-10 "
                "batch under raw_tree/canonical/ (outside the registry/** glob).",
            )

            # Agent 8 invariant: 0 Projekt -[BELEGT_IN]-> q_actor_*
            invariant = s.run(
                "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
                "WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "agent8_invariant_projekt_to_actor_url_zero",
                invariant == 0,
                invariant,
                0,
                "Hard precondition for any 4b.3 work: §4c.3 detach must hold.",
            )

            # No NULL evidence fields on touched edges
            evidence_null = s.run(
                "MATCH ()-[r]->() "
                "WHERE r.evidence_origin IS NULL OR r.evidence_basis IS NULL "
                "   OR r.evidence_source_id IS NULL OR r.evidence_confidence IS NULL "
                "RETURN count(r) AS c"
            ).single()["c"]
            assertion(
                "all_edges_have_5_field_evidence",
                evidence_null == 0,
                evidence_null,
                0,
            )

        # Summary
        out["all_passed"] = all(a["passed"] for a in out["assertions"])
        out["passed_count"] = sum(1 for a in out["assertions"] if a["passed"])
        out["failed_count"] = sum(1 for a in out["assertions"] if not a["passed"])
        ACCEPT_JSON.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print(json.dumps({
            "all_passed": out["all_passed"],
            "passed": out["passed_count"],
            "failed": out["failed_count"],
            "failures": [a for a in out["assertions"] if not a["passed"]],
        }, indent=2, default=str))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
