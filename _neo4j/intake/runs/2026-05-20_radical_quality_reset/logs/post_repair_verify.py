"""Post-repair verification — re-run only the gates that previously failed
or had documented residuals against live `mit-bestand`. Read-only.

Outputs:
- logs/post_repair_verify.json (machine readable)
- reports/post_repair_verification.md (human readable)
- POST_REPAIR_VERIFY_DONE.flag (verdict flag)
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
OUT_JSON = RUN_ROOT / "logs/post_repair_verify.json"
OUT_MD = RUN_ROOT / "reports/post_repair_verification.md"
OUT_FLAG = RUN_ROOT / "POST_REPAIR_VERIFY_DONE.flag"


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
    res: dict = {
        "verifier": "post_repair_verification",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "database": db,
        "sections": {},
    }

    def scalar(s, q, **params):
        rec = s.run(q, **params).single()
        if rec is None:
            return None
        # return single value
        return rec[0] if len(rec.keys()) == 1 else dict(rec)

    def rows(s, q, **params):
        return [dict(r) for r in s.run(q, **params)]

    try:
        with drv.session(database=db) as s:
            # ============ PHASE 1.2 ============
            p12 = {}
            p12["quelle_with_anchor_ids"] = scalar(
                s,
                "MATCH (q:Quelle) WHERE q.id IN ['q_controlled_vocab_seed','q_akteursliste_master_md'] "
                "RETURN count(q) AS c",
            )
            p12["belegt_in_to_ontology_anchor"] = scalar(
                s, "MATCH ()-[r:BELEGT_IN]->(:OntologyAnchor) RETURN count(r) AS c"
            )
            p12["ontology_anchor_count"] = scalar(
                s, "MATCH (a:OntologyAnchor) RETURN count(a) AS c"
            )
            p12["anchored_by_count"] = scalar(
                s, "MATCH ()-[r:ANCHORED_BY]->(:OntologyAnchor) RETURN count(r) AS c"
            )
            p12["belegt_in_to_anchor_ids_via_id"] = scalar(
                s,
                "MATCH ()-[r:BELEGT_IN]->(n) "
                "WHERE n.id IN ['q_controlled_vocab_seed','q_akteursliste_master_md'] "
                "RETURN count(r) AS c",
            )
            p12["anchors_visible"] = rows(
                s,
                "MATCH (a:OntologyAnchor) RETURN a.id AS id, labels(a) AS lbls",
            )
            p12["checks"] = [
                {
                    "id": "1.2.gate5_quelle_anchor_ids_zero",
                    "expected": "== 0",
                    "got": p12["quelle_with_anchor_ids"],
                    "passed": p12["quelle_with_anchor_ids"] == 0,
                },
                {
                    "id": "1.2.gate7_belegt_in_to_anchor_zero",
                    "expected": "== 0",
                    "got": p12["belegt_in_to_ontology_anchor"],
                    "passed": p12["belegt_in_to_ontology_anchor"] == 0,
                },
                {
                    "id": "1.2.gate4_anchor_count_two",
                    "expected": "== 2",
                    "got": p12["ontology_anchor_count"],
                    "passed": p12["ontology_anchor_count"] == 2,
                },
                {
                    "id": "1.2.gate6_anchored_by_in_690_730",
                    "expected": "in [690,730]",
                    "got": p12["anchored_by_count"],
                    "passed": isinstance(p12["anchored_by_count"], int)
                    and 690 <= p12["anchored_by_count"] <= 730,
                },
                {
                    "id": "1.2.regression_belegt_in_to_any_anchor_id_zero",
                    "expected": "== 0",
                    "got": p12["belegt_in_to_anchor_ids_via_id"],
                    "passed": p12["belegt_in_to_anchor_ids_via_id"] == 0,
                },
            ]
            p12["passed"] = all(c["passed"] for c in p12["checks"])
            res["sections"]["phase_1_2"] = p12

            # ============ PHASE 1.5 / 1.6 ============
            p15 = {}
            p15["norm_din_18940_remaining"] = scalar(
                s, "MATCH (n:Norm {id:'norm_din_18940'}) RETURN count(n) AS c"
            )
            p15["bauburo_in_situ_remaining"] = scalar(
                s, "MATCH (a:Akteur {id:'bauburo_in_situ'}) RETURN count(a) AS c"
            )
            p15["Bellastock_remaining"] = scalar(
                s, "MATCH (a:Akteur {id:'Bellastock'}) RETURN count(a) AS c"
            )
            p15["case_insensitive_actor_dup_ordered_pairs"] = scalar(
                s,
                "MATCH (a1:Akteur),(a2:Akteur) "
                "WHERE a1.id<>a2.id AND toLower(a1.id)=toLower(a2.id) "
                "RETURN count(*) AS c",
            )
            p15["akteur_count"] = scalar(
                s, "MATCH (a:Akteur) RETURN count(a) AS c"
            )
            p15["canonical_actor_degrees"] = rows(
                s,
                "UNWIND ['baubuero_in_situ','bellastock','norm_din_18940_family'] AS i "
                "OPTIONAL MATCH (n {id:i}) "
                "RETURN i AS id, labels(n) AS lbls, "
                "size([(n)-[r]-() | r]) AS degree",
            )
            p15["checks"] = [
                {
                    "id": "1.5.norm_din_18940_absent",
                    "expected": "== 0",
                    "got": p15["norm_din_18940_remaining"],
                    "passed": p15["norm_din_18940_remaining"] == 0,
                },
                {
                    "id": "1.6.bauburo_in_situ_absent",
                    "expected": "== 0",
                    "got": p15["bauburo_in_situ_remaining"],
                    "passed": p15["bauburo_in_situ_remaining"] == 0,
                },
                {
                    "id": "1.6.Bellastock_absent",
                    "expected": "== 0",
                    "got": p15["Bellastock_remaining"],
                    "passed": p15["Bellastock_remaining"] == 0,
                },
                {
                    "id": "1.6.case_insensitive_dup_pairs_zero",
                    "expected": "== 0",
                    "got": p15["case_insensitive_actor_dup_ordered_pairs"],
                    "passed": p15["case_insensitive_actor_dup_ordered_pairs"] == 0,
                },
                {
                    "id": "1.6.akteur_count_reasonable",
                    "expected": "in [640,660]",
                    "got": p15["akteur_count"],
                    "passed": isinstance(p15["akteur_count"], int)
                    and 640 <= p15["akteur_count"] <= 660,
                },
            ]
            p15["passed"] = all(c["passed"] for c in p15["checks"])
            res["sections"]["phase_1_5_1_6"] = p15

            # ============ PHASE 2.5 ============
            p25 = {}
            p25["rechtlichebedingung_count"] = scalar(
                s, "MATCH (n:RechtlicheBedingung) RETURN count(n) AS c"
            )
            p25["layer_count"] = scalar(
                s, "MATCH (n:Layer) RETURN count(n) AS c"
            )
            p25["lebenszyklusmodul_count"] = scalar(
                s, "MATCH (n:LebenszyklusModul) RETURN count(n) AS c"
            )
            p25["zertifizierungbewertungssystem_count"] = scalar(
                s, "MATCH (n:ZertifizierungBewertungssystem) RETURN count(n) AS c"
            )
            p25["tool_count"] = scalar(s, "MATCH (n:Tool) RETURN count(n) AS c")
            p25["checks"] = [
                {
                    "id": "2.5.rechtlichebedingung_zero",
                    "expected": "== 0",
                    "got": p25["rechtlichebedingung_count"],
                    "passed": p25["rechtlichebedingung_count"] == 0,
                },
                {
                    "id": "2.5.layer_zero",
                    "expected": "== 0",
                    "got": p25["layer_count"],
                    "passed": p25["layer_count"] == 0,
                },
                {
                    "id": "2.5.lebenszyklusmodul_zero",
                    "expected": "== 0",
                    "got": p25["lebenszyklusmodul_count"],
                    "passed": p25["lebenszyklusmodul_count"] == 0,
                },
                {
                    "id": "2.5.zertifizierungbewertungssystem_zero",
                    "expected": "== 0",
                    "got": p25["zertifizierungbewertungssystem_count"],
                    "passed": p25["zertifizierungbewertungssystem_count"] == 0,
                },
                {
                    "id": "2.5.tool_zero",
                    "expected": "== 0",
                    "got": p25["tool_count"],
                    "passed": p25["tool_count"] == 0,
                },
            ]
            p25["passed"] = all(c["passed"] for c in p25["checks"])
            res["sections"]["phase_2_5"] = p25

            # ============ PHASE 4.1 + 4c ============
            p41 = {}
            p41["curated_without_excerpt"] = scalar(
                s,
                "MATCH ()-[r]->() "
                "WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL "
                "RETURN count(r) AS c",
            )
            p41["origin_enum_violations"] = scalar(
                s,
                "MATCH ()-[r]->() "
                "WHERE r.evidence_origin IS NOT NULL "
                "AND NOT r.evidence_origin IN ['curated','inferred','derived'] "
                "RETURN count(r) AS c",
            )
            p41["confidence_enum_violations"] = scalar(
                s,
                "MATCH ()-[r]->() "
                "WHERE r.evidence_confidence IS NOT NULL "
                "AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping'] "
                "RETURN count(r) AS c",
            )
            p41["bookkeeping_not_derived"] = scalar(
                s,
                "MATCH ()-[r]->() "
                "WHERE r.evidence_confidence='bookkeeping' "
                "AND coalesce(r.evidence_origin,'')<>'derived' "
                "RETURN count(r) AS c",
            )
            p41["citation_basis_enum_violations_belegt_in"] = scalar(
                s,
                "MATCH ()-[r:BELEGT_IN]->() "
                "WHERE r.evidence_basis IS NOT NULL "
                "AND NOT r.evidence_basis IN ['cell_citation','controlled_vocab','propagated','registry_stub','year_inferred','project_rollup','documented','era_and_material','material_only'] "
                "RETURN count(r) AS c",
            )
            p41["quelle_external_sources_nonnull"] = scalar(
                s,
                "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c",
            )
            p41["rel_polluted_keys"] = scalar(
                s,
                "MATCH ()-[r]->() "
                "WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad "
                "WHERE size(bad) > 0 RETURN count(r) AS c",
            )
            p41["projekt_actor_registry_belegt_in"] = scalar(
                s,
                "MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'}) "
                "RETURN count(r) AS c",
            )
            p41["q1_canonical_rows"] = scalar(
                s,
                """
                MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec),
                      (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)
                WHERE r.evidence_origin='curated'
                RETURN count(*) AS c
                """,
            )
            p41["q1_bauwerk_only_rows"] = scalar(
                s,
                """
                MATCH (donor:Bauwerk)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec:Bauwerk),
                      (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)
                WHERE r.evidence_origin='curated'
                RETURN count(*) AS c
                """,
            )
            p41["q1_topology_only_rows"] = scalar(
                s,
                "MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec) RETURN count(*) AS c",
            )
            p41["hat_bauteilgruppe_curated"] = scalar(
                s,
                "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() "
                "WHERE r.evidence_origin='curated' RETURN count(r) AS c",
            )
            p41["zitiert_quelle_total"] = scalar(
                s, "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS c"
            )
            p41["checks"] = [
                {
                    "id": "4.1.curated_without_excerpt_zero",
                    "expected": "== 0",
                    "got": p41["curated_without_excerpt"],
                    "passed": p41["curated_without_excerpt"] == 0,
                },
                {
                    "id": "4.1.origin_enum_violations_zero",
                    "expected": "== 0",
                    "got": p41["origin_enum_violations"],
                    "passed": p41["origin_enum_violations"] == 0,
                },
                {
                    "id": "4.1.confidence_enum_violations_zero",
                    "expected": "== 0",
                    "got": p41["confidence_enum_violations"],
                    "passed": p41["confidence_enum_violations"] == 0,
                },
                {
                    "id": "4.1.bookkeeping_not_derived_zero",
                    "expected": "== 0",
                    "got": p41["bookkeeping_not_derived"],
                    "passed": p41["bookkeeping_not_derived"] == 0,
                },
                {
                    "id": "4c.quelle_external_sources_zero",
                    "expected": "== 0",
                    "got": p41["quelle_external_sources_nonnull"],
                    "passed": p41["quelle_external_sources_nonnull"] == 0,
                },
                {
                    "id": "4c.polluted_rel_keys_zero",
                    "expected": "== 0",
                    "got": p41["rel_polluted_keys"],
                    "passed": p41["rel_polluted_keys"] == 0,
                },
                {
                    "id": "4c.projekt_actor_registry_belegt_in_zero",
                    "expected": "== 0",
                    "got": p41["projekt_actor_registry_belegt_in"],
                    "passed": p41["projekt_actor_registry_belegt_in"] == 0,
                },
                {
                    "id": "Q1.canonical_reuse_story_rows",
                    "expected": ">= 1",
                    "got": p41["q1_canonical_rows"],
                    "passed": isinstance(p41["q1_canonical_rows"], int)
                    and p41["q1_canonical_rows"] >= 1,
                },
            ]
            p41["passed"] = all(c["passed"] for c in p41["checks"])
            res["sections"]["phase_4_1_and_4c_and_q1"] = p41

            # ============ PHASE 2.7 panel + 5.1 ============
            p27 = {}
            p27["projekt_total"] = scalar(
                s, "MATCH (p:Projekt) RETURN count(p) AS c"
            )
            p27["projekt_distinct_keys"] = scalar(
                s,
                "MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k) AS c",
            )
            p27["projekt_max_keys_per_node"] = scalar(
                s,
                "MATCH (p:Projekt) WITH size(keys(p)) AS n "
                "RETURN max(n) AS c",
            )
            p27["projekt_sample_5_keys"] = rows(
                s,
                "MATCH (p:Projekt) WITH p ORDER BY p.id LIMIT 5 "
                "RETURN p.id AS id, size(keys(p)) AS n_keys",
            )
            p27["projekt_with_quality_tier_facts"] = scalar(
                s,
                "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p) AS c",
            )
            p27["projekt_with_legacy_scalars"] = scalar(
                s,
                "MATCH (p:Projekt) "
                "WHERE p.quality_tier_computed_by IS NOT NULL "
                "OR p.quality_tier_has_components IS NOT NULL "
                "OR p.quality_tier_has_evidence IS NOT NULL "
                "OR p.quality_tier_has_land IS NOT NULL "
                "OR p.quality_tier_has_metric IS NOT NULL "
                "OR p.quality_tier_has_year IS NOT NULL "
                "OR p.quality_tier_n_bg IS NOT NULL "
                "OR p.quality_tier_n_bg_quantified IS NOT NULL "
                "OR p.quality_tier_n_curated_evidence IS NOT NULL "
                "RETURN count(p) AS c",
            )
            # All Projekt tiered
            p27["projekt_with_quality_tier"] = scalar(
                s,
                "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL RETURN count(p) AS c",
            )
            # Tier distribution
            p27["tier_distribution"] = rows(
                s,
                "MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS c ORDER BY tier",
            )
            # p_circle_house tier
            p27["p_circle_house"] = rows(
                s,
                "MATCH (p {id:'p_circle_house'}) RETURN labels(p) AS lbls, p.quality_tier AS tier",
            )
            sample_max = max((r["n_keys"] for r in p27["projekt_sample_5_keys"]), default=0)
            p27["checks"] = [
                {
                    "id": "2.7.projekt_distinct_keys_le_25",
                    "expected": "<= 25",
                    "got": p27["projekt_distinct_keys"],
                    "passed": isinstance(p27["projekt_distinct_keys"], int)
                    and p27["projekt_distinct_keys"] <= 25,
                },
                {
                    "id": "2.7.projekt_sample_5_per_node_keys_le_18",
                    "expected": "<= 18 each",
                    "got": [r["n_keys"] for r in p27["projekt_sample_5_keys"]],
                    "passed": sample_max <= 18,
                },
                {
                    "id": "5.all_projekt_tiered",
                    "expected": "projekt_total == projekt_with_quality_tier",
                    "got": {
                        "total": p27["projekt_total"],
                        "with_tier": p27["projekt_with_quality_tier"],
                    },
                    "passed": p27["projekt_total"] == p27["projekt_with_quality_tier"]
                    and p27["projekt_total"] > 0,
                },
                {
                    "id": "5.tier_distribution_thresholds",
                    "expected": "tier_1>=8, tier_2>=50, tier_3>=10",
                    "got": {
                        r["tier"]: r["c"] for r in p27["tier_distribution"]
                    },
                    "passed": (
                        {r["tier"]: r["c"] for r in p27["tier_distribution"]}.get(
                            "tier_1_decision_grade", 0
                        )
                        >= 8
                        and {r["tier"]: r["c"] for r in p27["tier_distribution"]}.get(
                            "tier_2_documentation_only", 0
                        )
                        >= 50
                        and {r["tier"]: r["c"] for r in p27["tier_distribution"]}.get(
                            "tier_3_stub", 0
                        )
                        >= 10
                    ),
                },
                {
                    "id": "5.p_circle_house_tier_documented",
                    "expected": "label=:Projekt, quality_tier=tier_2_documentation_only (per repair report)",
                    "got": p27["p_circle_house"],
                    "passed": bool(
                        p27["p_circle_house"]
                        and "Projekt" in p27["p_circle_house"][0]["lbls"]
                        and p27["p_circle_house"][0]["tier"]
                        == "tier_2_documentation_only"
                    ),
                },
            ]
            p27["passed"] = all(c["passed"] for c in p27["checks"])
            res["sections"]["phase_2_7_and_5_1"] = p27

        # Overall verdict
        res["overall_verdict"] = (
            "PASS"
            if all(sec["passed"] for sec in res["sections"].values())
            else "FAIL"
        )
        res["section_passes"] = {
            name: sec["passed"] for name, sec in res["sections"].items()
        }
    finally:
        drv.close()

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"overall: {res['overall_verdict']}")
    for name, sec in res["sections"].items():
        flag = "PASS" if sec["passed"] else "FAIL"
        print(f"  {flag}: {name}")
        for c in sec["checks"]:
            sub = "PASS" if c["passed"] else "FAIL"
            print(f"    {sub}: {c['id']}: got={c['got']} ({c['expected']})")
    return 0 if res["overall_verdict"] == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
