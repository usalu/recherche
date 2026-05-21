"""Agent 12 — Phase 5 probe.

Snapshot of relevant state before computing quality_tier and relabeling
4 programmes.
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
LOGS_DIR = RUN_ROOT / "logs"
OUT = LOGS_DIR / "agent12_probe.json"


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore
    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    out: dict[str, Any] = {}
    try:
        uri, user, pw, db = _resolve()
        drv = GraphDatabase.driver(uri, auth=(user, pw))
        with drv.session(database=db) as session:
            def one(q, **p):
                r = session.run(q, **p).single()
                return r.value() if r else None

            def rows(q, **p):
                return [dict(r) for r in session.run(q, **p)]

            out["counts"] = {
                "total_nodes": one("MATCH (n) RETURN count(n)"),
                "total_rels": one("MATCH ()-[r]->() RETURN count(r)"),
                "projekt_total": one("MATCH (p:Projekt) RETURN count(p)"),
                "programm_total": one("MATCH (p:Programm) RETURN count(p)"),
                "projekt_already_tier": one(
                    "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL RETURN count(p)"
                ),
                "projekt_with_year_completed": one(
                    "MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p)"
                ),
                "projekt_with_liegt_in_land": one(
                    "MATCH (p:Projekt) WHERE exists{(p)-[:LIEGT_IN_LAND]->()} RETURN count(p)"
                ),
                "bauteilgruppe_total": one("MATCH (b:Bauteilgruppe) RETURN count(b)"),
                "hat_bauteilgruppe_total": one(
                    "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r)"
                ),
                "belegt_in_total": one(
                    "MATCH ()-[r:BELEGT_IN]->() RETURN count(r)"
                ),
                "belegt_in_curated_excerpt_belegt_or_teil": one(
                    "MATCH ()-[r:BELEGT_IN]->() "
                    "WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NOT NULL "
                    "AND r.evidence_confidence IN ['belegt','teilweise_belegt'] "
                    "RETURN count(r)"
                ),
                "referenziert_norm_total": one(
                    "MATCH ()-[r:REFERENZIERT_NORM]->() RETURN count(r)"
                ),
                "referenziert_norm_mittel": one(
                    "MATCH ()-[r:REFERENZIERT_NORM]->() "
                    "WHERE r.evidence_confidence='mittel' RETURN count(r)"
                ),
            }

            out["target_programm_ids"] = rows(
                "MATCH (p:Projekt) "
                "WHERE p.id IN ['p_reuse_logistics','p_vandkunsten_component_reuse',"
                "'p_architecture_of_reuse_brussels','p_reuse_in_construction_zhaw',"
                "'p_circle_house'] "
                "RETURN p.id AS id, labels(p) AS labels, p.name AS name, "
                "p.year_completed AS year_completed, p.quality_tier AS quality_tier, "
                "p.migration_origin AS migration_origin, p.original_label AS original_label, "
                "size([(p)-[:HAT_BAUTEILGRUPPE]->() | 1]) AS n_bg, "
                "exists{(p)-[:LIEGT_IN_LAND]->()} AS has_land"
            )

            out["projekt_label_unique_check"] = rows(
                "MATCH (p:Projekt) RETURN labels(p) AS labs, count(p) AS c "
                "ORDER BY c DESC"
            )

            out["projekt_with_id_null"] = one(
                "MATCH (p:Projekt) WHERE p.id IS NULL RETURN count(p)"
            )

            out["projekt_with_dual_labels"] = rows(
                "MATCH (p:Projekt) WHERE size(labels(p)) > 1 "
                "RETURN p.id AS id, labels(p) AS labs LIMIT 20"
            )

            out["mittel_referenziert_norm_sample"] = rows(
                "MATCH (a)-[r:REFERENZIERT_NORM]->(b) "
                "WHERE r.evidence_confidence='mittel' "
                "RETURN a.id AS src, labels(a) AS src_labs, b.id AS tgt, "
                "r.evidence_origin AS origin, r.evidence_basis AS basis, "
                "r.evidence_excerpt AS excerpt, r.evidence_source_id AS src_id, "
                "r.derivation_note AS derivation_note LIMIT 20"
            )

            out["tier_input_sample"] = rows(
                "MATCH (p:Projekt) "
                "OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
                "WITH p, count(DISTINCT bg) AS n_bg, "
                " sum(CASE WHEN bg.menge_t IS NOT NULL OR bg.menge_stueck IS NOT NULL "
                "      OR bg.menge_m2 IS NOT NULL OR bg.menge_kg IS NOT NULL "
                "      OR bg.menge_m IS NOT NULL THEN 1 ELSE 0 END) AS n_bg_q "
                "OPTIONAL MATCH (p)-[bel:BELEGT_IN]->() "
                "WITH p, n_bg, n_bg_q, "
                " sum(CASE WHEN bel.evidence_origin='curated' "
                "          AND bel.evidence_excerpt IS NOT NULL "
                "          AND bel.evidence_confidence IN ['belegt','teilweise_belegt'] "
                "       THEN 1 ELSE 0 END) AS n_curated_evidence "
                "RETURN p.id AS id, p.name AS name, p.year_completed AS yc, "
                " exists{(p)-[:LIEGT_IN_LAND]->()} AS has_land, "
                " n_bg, n_bg_q, "
                " size(coalesce(p.reuse_share_facts,[])) AS n_rs, "
                " size(coalesce(p.co2_facts,[])) AS n_co2, "
                " n_curated_evidence "
                "ORDER BY id"
            )

            out["belegt_in_via_anchored_by_check"] = one(
                "MATCH ()-[r:ANCHORED_BY]->() RETURN count(r)"
            )

            out["projekt_relevant_to_acceptance"] = rows(
                "MATCH (p:Projekt) "
                "RETURN p.import_status AS import_status, count(p) AS c "
                "ORDER BY c DESC"
            )

            out["sample_curated_evidence_confidence_distribution"] = rows(
                "MATCH (p:Projekt)-[r:BELEGT_IN]->() "
                "WHERE r.evidence_origin='curated' "
                "RETURN r.evidence_confidence AS conf, "
                "(r.evidence_excerpt IS NULL) AS excerpt_null, "
                "count(r) AS c ORDER BY c DESC"
            )

        drv.close()
        out["status"] = "ok"
    except Exception:
        out["status"] = "error"
        out["error"] = traceback.format_exc()
    finally:
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        print(f"wrote {OUT}")
    return 0 if out.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
