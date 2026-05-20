"""Agent 9 — post-loader audit.

Confirms:
  - >=85 case_markdown :Quelle anchors have >=1 ZITIERT_QUELLE child
  - mig_4_1 hard rules still hold (curated requires excerpt, etc.)
  - per-project curated-edge counts (top 20)
  - cost_facts / reuse_share_facts / co2_facts populated where expected
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
    / "agent9_verify.json"
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
            out["case_markdown_total"] = s.run(
                "MATCH (q:Quelle) WHERE q.quelltyp='case_markdown' RETURN count(q) AS c"
            ).single()["c"]
            out["case_markdown_with_zitiert_child"] = s.run(
                """
                MATCH (q:Quelle) WHERE q.quelltyp='case_markdown'
                AND size([(q)-[:ZITIERT_QUELLE]->() | 1]) >= 1
                RETURN count(q) AS c
                """
            ).single()["c"]
            out["case_markdown_without_zitiert_child"] = [
                r["id"] for r in s.run(
                    """
                    MATCH (q:Quelle) WHERE q.quelltyp='case_markdown'
                    AND NOT EXISTS((q)-[:ZITIERT_QUELLE]->())
                    RETURN q.id AS id ORDER BY q.id
                    """
                )
            ]
            # mig_4_1 audits
            out["mig_4_1_audits"] = {
                "viol_curated_no_excerpt": s.run(
                    "MATCH ()-[r]->() WHERE r.evidence_origin='curated' "
                    "AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='') "
                    "RETURN count(r) AS c"
                ).single()["c"],
                "viol_bk_not_derived": s.run(
                    "MATCH ()-[r]->() WHERE r.evidence_confidence='bookkeeping' "
                    "AND coalesce(r.evidence_origin,'')<>'derived' "
                    "RETURN count(r) AS c"
                ).single()["c"],
                "viol_excerpt_propagated": s.run(
                    "MATCH ()-[r]->() WHERE r.evidence_excerpt IS NOT NULL "
                    "AND toLower(r.evidence_excerpt) CONTAINS 'propagated from' "
                    "RETURN count(r) AS c"
                ).single()["c"],
                "viol_missing_field": s.run(
                    "MATCH ()-[r]->() WHERE r.evidence_origin IS NULL "
                    "OR r.evidence_basis IS NULL OR r.evidence_source_id IS NULL "
                    "OR r.evidence_confidence IS NULL RETURN count(r) AS c"
                ).single()["c"],
                "viol_citation_basis_enum": s.run(
                    """
                    MATCH ()-[r]->()
                    WHERE type(r) IN ['BELEGT_IN','BETEILIGT_AN',
                       'ASSOZIIERT_MIT_PROJEKT','AUS_BAUWERK','FROM_DONOR',
                       'EINGEBAUT_IN','INTO_RECEIVER','HAT_BAUTEILGRUPPE',
                       'HAT_HUERDE','HAT_AKTEURROLLE']
                    AND NOT r.evidence_basis IN
                       ['cell_citation','registry_stub','propagated','controlled_vocab']
                    RETURN count(r) AS c
                    """
                ).single()["c"],
            }
            out["belegt_in_curated_total"] = s.run(
                "MATCH ()-[r:BELEGT_IN]->() WHERE r.evidence_origin='curated' "
                "RETURN count(r) AS c"
            ).single()["c"]
            out["belegt_in_curated_with_excerpt"] = s.run(
                "MATCH ()-[r:BELEGT_IN]->() WHERE r.evidence_origin='curated' "
                "AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt<>'' "
                "RETURN count(r) AS c"
            ).single()["c"]
            out["belegt_in_loader_managed"] = s.run(
                "MATCH ()-[r:BELEGT_IN]->() WHERE r._created_by='agent9_phase4b1' "
                "RETURN count(r) AS c"
            ).single()["c"]
            out["zitiert_quelle_total"] = s.run(
                "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
            ).single()["c"]
            out["external_reference_quelle_total"] = s.run(
                "MATCH (q:Quelle) WHERE q.quelltyp='external_reference' "
                "RETURN count(q) AS c"
            ).single()["c"]
            out["top_projects_by_curated_belegt"] = [
                {"pid": r["pid"], "n": r["n"]}
                for r in s.run(
                    """
                    MATCH (p:Projekt)-[r:BELEGT_IN]->()
                    WHERE r.evidence_origin='curated'
                    RETURN p.id AS pid, count(r) AS n
                    ORDER BY n DESC LIMIT 20
                    """
                )
            ]
            out["projects_with_cost_facts"] = s.run(
                "MATCH (p:Projekt) WHERE size(coalesce(p.cost_facts, [])) > 0 "
                "RETURN count(p) AS c"
            ).single()["c"]
            out["projects_with_co2_facts"] = s.run(
                "MATCH (p:Projekt) WHERE size(coalesce(p.co2_facts, [])) > 0 "
                "RETURN count(p) AS c"
            ).single()["c"]
            out["projects_with_reuse_share_facts"] = s.run(
                "MATCH (p:Projekt) WHERE size(coalesce(p.reuse_share_facts, [])) > 0 "
                "RETURN count(p) AS c"
            ).single()["c"]
            sample = s.run(
                """
                MATCH (p:Projekt {id:'p_resilience_la_ferme_des_possibles_stains'})
                RETURN p.cost_facts AS cost, p.reuse_share_facts AS share,
                       p.co2_facts AS co2
                """
            ).single()
            if sample:
                out["sample_resilience_cost_facts_count"] = len(sample["cost"] or [])
                out["sample_resilience_first_cost_entry"] = (
                    (sample["cost"] or [None])[0]
                )
                out["sample_resilience_co2_entries"] = sample["co2"] or []
    finally:
        drv.close()
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({
        "case_md_total": out["case_markdown_total"],
        "case_md_with_zit": out["case_markdown_with_zitiert_child"],
        "acceptance_pass": out["case_markdown_with_zitiert_child"] >= 85,
        "mig_4_1_audits": out["mig_4_1_audits"],
        "belegt_in_curated_total": out["belegt_in_curated_total"],
        "belegt_in_curated_with_excerpt": out["belegt_in_curated_with_excerpt"],
        "belegt_in_loader_managed": out["belegt_in_loader_managed"],
        "zitiert_quelle_total": out["zitiert_quelle_total"],
        "external_reference_quelle_total": out["external_reference_quelle_total"],
        "projects_with_cost_facts": out["projects_with_cost_facts"],
        "projects_with_co2_facts": out["projects_with_co2_facts"],
        "projects_with_reuse_share_facts": out["projects_with_reuse_share_facts"],
    }, indent=2))
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
