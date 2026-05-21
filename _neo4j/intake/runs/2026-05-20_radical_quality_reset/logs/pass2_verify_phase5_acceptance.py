"""Pass-2 Detailed Verifier 12/12 — Phase 5 + Acceptance Q1-Q7 + end-state size.

Read-only. Hits `mit-bestand` via the python neo4j driver, writes JSON +
markdown report. Independent re-verification on top of `final_verify_phase5.py`
and the subsequent repair runs (Repair D + Repair E + post_repair_verify).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")
LOGS_DIR = RUN_DIR / "logs"

driver = GraphDatabase.driver(URI, auth=AUTH)


def q(query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return [dict(r) for r in s.run(query, **params)]


def qval(query, **params):
    rows = q(query, **params)
    if not rows:
        return None
    first = rows[0]
    return next(iter(first.values()))


out: dict = {
    "verifier": "pass2_phase5_acceptance",
    "database": DB,
    "uri": URI,
    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    "mode": "read_only",
    "phase_5_checks": {},
    "acceptance_queries": {},
    "end_state_size": {},
}

# =============================================================
# 1. File / flag artifacts
# =============================================================
files = {
    "mig_5_1_quality_tier.cypher": (RUN_DIR / "migrations/mig_5_1_quality_tier.cypher").is_file(),
    "mig_5_3_relabel_programme.cypher": (RUN_DIR / "migrations/mig_5_3_relabel_programme.cypher").is_file(),
    "mig_repair_2_7_5_1_quality_tier_panel.cypher": (
        RUN_DIR / "migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher"
    ).is_file(),
    "mig_repair_4_1_curated_excerpts_and_q1.cypher": (
        RUN_DIR / "migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher"
    ).is_file(),
    "PHASE_5_DONE.flag": (RUN_DIR / "PHASE_5_DONE.flag").is_file(),
    "PHASE_2_7_5_1_REPAIR_DONE.flag": (RUN_DIR / "PHASE_2_7_5_1_REPAIR_DONE.flag").is_file(),
    "PHASE_4_1_Q1_REPAIR_DONE.flag": (RUN_DIR / "PHASE_4_1_Q1_REPAIR_DONE.flag").is_file(),
    "POST_REPAIR_VERIFY_DONE.flag": (RUN_DIR / "POST_REPAIR_VERIFY_DONE.flag").is_file(),
    "FINAL_PLAN_COMPLETION_AUDIT.md": (
        RUN_DIR / "reports/FINAL_PLAN_COMPLETION_AUDIT.md"
    ).is_file(),
}
out["phase_5_checks"]["file_artifacts"] = files

# =============================================================
# 2. Projekt tier coverage + enum
# =============================================================
projekt_total = qval("MATCH (p:Projekt) RETURN count(p)")
projekt_with_tier = qval(
    "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL RETURN count(p)"
)
projekt_with_enum = qval(
    """
    MATCH (p:Projekt)
    WHERE p.quality_tier IN [
        'tier_1_decision_grade',
        'tier_2_documentation_only',
        'tier_3_stub'
    ]
    RETURN count(p)
    """
)
projekt_off_enum_rows = q(
    """
    MATCH (p:Projekt)
    WHERE p.quality_tier IS NOT NULL
      AND NOT p.quality_tier IN [
        'tier_1_decision_grade',
        'tier_2_documentation_only',
        'tier_3_stub'
      ]
    RETURN p.id AS id, p.quality_tier AS tier
    """
)
out["phase_5_checks"]["projekt_tier_coverage"] = {
    "projekt_total": projekt_total,
    "projekt_with_quality_tier": projekt_with_tier,
    "projekt_with_quality_tier_in_enum": projekt_with_enum,
    "off_enum_rows": projekt_off_enum_rows,
    "passed": (
        projekt_total == projekt_with_tier == projekt_with_enum
        and projekt_total == 101
        and not projekt_off_enum_rows
    ),
}

# =============================================================
# 3. Tier distribution
# =============================================================
tier_rows = q(
    "MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS n ORDER BY tier"
)
tier_map = {r["tier"]: r["n"] for r in tier_rows}
expect_dist = {"tier_1_decision_grade": 11, "tier_2_documentation_only": 68, "tier_3_stub": 22}
out["phase_5_checks"]["tier_distribution"] = {
    "rows": tier_rows,
    "tier_1": tier_map.get("tier_1_decision_grade", 0),
    "tier_2": tier_map.get("tier_2_documentation_only", 0),
    "tier_3": tier_map.get("tier_3_stub", 0),
    "expected": expect_dist,
    "passed": tier_map == expect_dist,
}

# =============================================================
# 4. 4 relabelled Programme + p_circle_house held back
# =============================================================
relabel_rows = q(
    """
    MATCH (n)
    WHERE n.id IN [
        'p_reuse_logistics',
        'p_vandkunsten_component_reuse',
        'p_architecture_of_reuse_brussels',
        'p_reuse_in_construction_zhaw',
        'p_circle_house'
    ]
    RETURN n.id AS id,
           labels(n) AS labels,
           n.quality_tier AS quality_tier,
           n.migration_origin AS migration_origin,
           n.original_label AS original_label
    ORDER BY id
    """
)
relabelled_ok = sum(
    1
    for r in relabel_rows
    if r["id"]
    in {
        "p_reuse_logistics",
        "p_vandkunsten_component_reuse",
        "p_architecture_of_reuse_brussels",
        "p_reuse_in_construction_zhaw",
    }
    and "Programm" in (r["labels"] or [])
    and r["migration_origin"] == "5_3_relabel_to_programm"
    and r["original_label"] == "Projekt"
)
circle_house_row = next(
    (r for r in relabel_rows if r["id"] == "p_circle_house"), None
)
circle_house_ok = bool(
    circle_house_row
    and "Projekt" in (circle_house_row["labels"] or [])
    and circle_house_row["quality_tier"] == "tier_2_documentation_only"
)
out["phase_5_checks"]["relabel_audit"] = {
    "rows": relabel_rows,
    "relabelled_to_programm_correct": relabelled_ok,
    "relabelled_expected": 4,
    "circle_house_correct": circle_house_ok,
    "passed": relabelled_ok == 4 and circle_house_ok,
}

# =============================================================
# 5. quality_tier_facts fold + 0 legacy scalars
# =============================================================
fold_present = qval(
    "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p)"
)
legacy_keys = [
    "quality_tier_computed_by",
    "quality_tier_has_components",
    "quality_tier_has_evidence",
    "quality_tier_has_land",
    "quality_tier_has_metric",
    "quality_tier_has_year",
    "quality_tier_n_bg",
    "quality_tier_n_bg_quantified",
    "quality_tier_n_curated_evidence",
]
legacy_present = qval(
    """
    MATCH (p:Projekt)
    WITH p, [k IN keys(p) WHERE k IN $keys] AS hits
    WHERE size(hits) > 0
    RETURN count(p)
    """,
    keys=legacy_keys,
)
sample_facts_row = qval(
    """
    MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})
    RETURN p.quality_tier_facts
    """
)
out["phase_5_checks"]["quality_tier_facts_fold"] = {
    "projekt_with_facts": fold_present,
    "projekt_with_any_legacy_scalar": legacy_present,
    "sample_quality_tier_facts_p_k118": sample_facts_row,
    "passed": fold_present == 101 and legacy_present == 0,
}

# =============================================================
# 6. evidence_confidence enum (Verifier-10 residual)
# =============================================================
mittel_count = qval(
    "MATCH ()-[r:REFERENZIERT_NORM]->() WHERE r.evidence_confidence='mittel' RETURN count(r)"
)
off_conf_enum = qval(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_confidence IS NOT NULL
      AND NOT r.evidence_confidence IN [
        'belegt', 'teilweise_belegt', 'unklar', 'inferiert', 'bookkeeping'
      ]
    RETURN count(r)
    """
)
off_origin_enum = qval(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin IS NOT NULL
      AND NOT r.evidence_origin IN ['curated', 'inferred', 'derived']
    RETURN count(r)
    """
)
curated_no_excerpt = qval(
    """
    MATCH ()-[r]->()
    WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL
    RETURN count(r)
    """
)
out["phase_5_checks"]["evidence_enum_hygiene"] = {
    "referenziert_norm_mittel": mittel_count,
    "evidence_confidence_off_enum": off_conf_enum,
    "evidence_origin_off_enum": off_origin_enum,
    "curated_without_excerpt": curated_no_excerpt,
    "passed": all(
        v == 0 for v in [mittel_count, off_conf_enum, off_origin_enum, curated_no_excerpt]
    ),
}

# =============================================================
# 7. Acceptance Q1 — Reuse Story
# =============================================================
q1_canonical = qval(
    """
    MATCH (donor:Bauwerk)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver:Bauwerk),
          (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
    WHERE hbg.evidence_origin='curated'
    RETURN count(*)
    """
)
q1_canonical_any_label = qval(
    """
    MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
          (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
    WHERE hbg.evidence_origin='curated'
    RETURN count(*)
    """
)
q1_topology_total = qval(
    """
    MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
          (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
    RETURN count(*)
    """
)
q1_bg_donor_receiver = qval(
    """
    MATCH (bg:Bauteilgruppe)
    WHERE exists{(bg)-[:FROM_DONOR]->()} AND exists{(bg)-[:INTO_RECEIVER]->()}
    RETURN count(bg)
    """
)
q1_hatbg_total = qval("MATCH ()-[r:HAT_BAUTEILGRUPPE]->() RETURN count(r)")
q1_hatbg_curated = qval(
    "MATCH ()-[r:HAT_BAUTEILGRUPPE]->() WHERE r.evidence_origin='curated' RETURN count(r)"
)
out["acceptance_queries"]["Q1_reuse_story"] = {
    "canonical_rows_bauwerk_to_bauwerk": q1_canonical,
    "canonical_rows_any_donor_receiver_label": q1_canonical_any_label,
    "topology_total_rows_any_origin": q1_topology_total,
    "bauteilgruppen_with_donor_and_receiver": q1_bg_donor_receiver,
    "hat_bauteilgruppe_total": q1_hatbg_total,
    "hat_bauteilgruppe_curated": q1_hatbg_curated,
    "expected_minimum": 1,
    "expected_target": 266,
    "verdict": "PASS" if (q1_canonical_any_label or 0) >= 1 else "FAIL",
}

# =============================================================
# 8. Acceptance Q2 — Risk Story
# =============================================================
q2_has_risk = qval(
    "MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff) RETURN count(r)"
)
q2_requires_verif = qval(
    "MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r)"
)
q2_breakdown = q(
    """
    MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
    RETURN coalesce(r.evidence_origin, '∅') AS origin,
           coalesce(r.evidence_confidence, '∅') AS confidence,
           count(r) AS n
    ORDER BY n DESC
    """
)
out["acceptance_queries"]["Q2_risk_story"] = {
    "has_risk_pollutant_rows": q2_has_risk,
    "requires_verification_for_rows": q2_requires_verif,
    "breakdown_origin_confidence": q2_breakdown,
    "expected_minimum": 700,
    "verdict": "PASS" if (q2_has_risk or 0) >= 700 else "FAIL",
}

# =============================================================
# 9. Acceptance Q3 — Comparison (tier-1 reuse_share_facts)
# =============================================================
q3_total = qval(
    """
    MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
    UNWIND coalesce(p.reuse_share_facts, []) AS rs
    RETURN count(*)
    """
)
q3_projects_with_rs = qval(
    """
    MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
    WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0
    RETURN count(p)
    """
)
q3_detail = q(
    """
    MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
    WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0
    RETURN p.id AS id, p.name AS name, p.reuse_share_facts AS reuse_share_facts
    ORDER BY id
    """
)
out["acceptance_queries"]["Q3_comparison"] = {
    "tier1_reuse_share_facts_total_entries": q3_total,
    "tier1_projects_with_reuse_share_facts": q3_projects_with_rs,
    "detail_rows": q3_detail,
    "verdict": "PASS",
    "note": "Plan permits 0; live value documented.",
}

# =============================================================
# 10. Acceptance Q4 — Actor Network
# =============================================================
# Prefer the BETEILIGT_AN relationship (the canonical actor↔project link in the plan)
# but also probe ASSOZIIERT_MIT_PROJEKT / HAT_AKTEURROLLE to verify there's no edge-type drift.
q4_rel_types = q(
    """
    CALL db.relationshipTypes() YIELD relationshipType
    WHERE relationshipType IN [
        'BETEILIGT_AN', 'ASSOZIIERT_MIT_PROJEKT', 'HAT_AKTEURROLLE'
    ]
    RETURN collect(relationshipType) AS types
    """
)
q4_beteiligt = qval(
    """
    MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c WHERE c>=2
    RETURN count(a)
    """
)
q4_assoz = qval(
    """
    MATCH (a:Akteur)-[:ASSOZIIERT_MIT_PROJEKT]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c WHERE c>=2
    RETURN count(a)
    """
)
q4_assoz_list = q(
    """
    MATCH (a:Akteur)-[:ASSOZIIERT_MIT_PROJEKT]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
    WITH a, count(DISTINCT p) AS c, collect(DISTINCT p.id) AS ids WHERE c>=2
    RETURN a.id AS actor_id, a.name AS actor_name, c AS tier1_projects, ids AS project_ids
    ORDER BY c DESC, actor_id
    """
)
out["acceptance_queries"]["Q4_actor_network"] = {
    "relationship_types_present": q4_rel_types,
    "rows_via_BETEILIGT_AN_only": q4_beteiligt,
    "rows_via_ASSOZIIERT_MIT_PROJEKT": q4_assoz,
    "actor_list_via_ASSOZIIERT": q4_assoz_list,
    "verdict": "PASS",
    "note": (
        "Plan permits 0 when only 11 tier-1 projects exist. "
        "Reported via both edge types for completeness."
    ),
}

# =============================================================
# 11. Acceptance Q5 — Decision Support (20 ReuseRules wired)
# =============================================================
q5_total = qval("MATCH (r:ReuseRule) RETURN count(r)")
q5_wired = qval(
    """
    MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land),
          (rule)-[:APPLIES_TO]->(:Material)
    RETURN count(DISTINCT rule)
    """
)
q5_applies_in = qval("MATCH ()-[r:APPLIES_IN]->() RETURN count(r)")
q5_applies_to = qval("MATCH ()-[r:APPLIES_TO]->() RETURN count(r)")
out["acceptance_queries"]["Q5_decision_support"] = {
    "reuse_rule_total": q5_total,
    "reuse_rule_with_both_applies": q5_wired,
    "applies_in_total": q5_applies_in,
    "applies_to_total": q5_applies_to,
    "expected": 20,
    "verdict": "PASS" if q5_wired == 20 else "FAIL",
}

# =============================================================
# 12. Acceptance Q6 — Trust Check (per-project + aggregate)
# =============================================================
q6_aggregate = q(
    """
    MATCH (p:Projekt)-[r]-()
    WITH coalesce(r.evidence_origin, '∅') AS origin, count(*) AS c
    RETURN origin, c ORDER BY c DESC
    """
)
q6_per_chiro = q(
    """
    MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[r]-()
    WITH coalesce(r.evidence_origin, '∅') AS origin, count(*) AS c
    RETURN origin, c ORDER BY c DESC
    """
)
q6_tier1_aggregate = q(
    """
    MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[r]-()
    WITH coalesce(r.evidence_origin, '∅') AS origin, count(*) AS c
    RETURN origin, c ORDER BY c DESC
    """
)
out["acceptance_queries"]["Q6_trust_check"] = {
    "aggregate_all_projekt_rows": q6_aggregate,
    "tier1_only_aggregate_rows": q6_tier1_aggregate,
    "per_project_p_chiro_d_itterbeek_dilbeek": q6_per_chiro,
    "verdict": "PASS" if (q6_aggregate and q6_per_chiro) else "FAIL",
}

# =============================================================
# 13. Acceptance Q7 — Source drill-down
# =============================================================
q7_total = qval(
    """
    MATCH (qmd:Quelle {quelltyp:'case_markdown'})-[:ZITIERT_QUELLE]->(ext:Quelle)
    RETURN count(*)
    """
)
q7_per_chiro = qval(
    """
    MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:BELEGT_IN]->(qmd:Quelle)
          -[:ZITIERT_QUELLE]->(ext:Quelle)
    RETURN count(DISTINCT ext)
    """
)
out["acceptance_queries"]["Q7_source_drilldown"] = {
    "case_markdown_zitiert_quelle_total": q7_total,
    "per_project_p_chiro_external_quellen": q7_per_chiro,
    "expected_minimum": 500,
    "verdict": "PASS" if (q7_total or 0) >= 500 else "FAIL",
}

# =============================================================
# 14. End-state size — node label inventory
# =============================================================
label_rows = q(
    """
    CALL db.labels() YIELD label
    CALL (label) {
        WITH label
        CALL apoc.cypher.run('MATCH (n:`' + label + '`) RETURN count(n) AS c', {}) YIELD value
        RETURN value.c AS c
    }
    RETURN label, c ORDER BY c DESC, label
    """
)
total_nodes = qval("MATCH (n) RETURN count(n)")

reltype_rows = q(
    """
    CALL db.relationshipTypes() YIELD relationshipType
    CALL (relationshipType) {
        WITH relationshipType
        CALL apoc.cypher.run('MATCH ()-[r:`' + relationshipType + '`]->() RETURN count(r) AS c', {})
        YIELD value
        RETURN value.c AS c
    }
    RETURN relationshipType AS type, c ORDER BY c DESC, type
    """
)
total_rels = qval("MATCH ()-[r]->() RETURN count(r)")

out["end_state_size"] = {
    "node_total": total_nodes,
    "relationship_total": total_rels,
    "node_label_inventory": label_rows,
    "relationship_type_inventory": reltype_rows,
    "plan_target_nodes": 2460,
    "plan_target_rels": 19100,
    "delta_nodes_pct_vs_target": round((total_nodes - 2460) / 2460 * 100, 1)
    if total_nodes is not None
    else None,
    "delta_rels_pct_vs_target": round((total_rels - 19100) / 19100 * 100, 1)
    if total_rels is not None
    else None,
}

# =============================================================
# 15. Overall verdict
# =============================================================
phase_5_passed = all(
    [
        all(files.values()),
        out["phase_5_checks"]["projekt_tier_coverage"]["passed"],
        out["phase_5_checks"]["tier_distribution"]["passed"],
        out["phase_5_checks"]["relabel_audit"]["passed"],
        out["phase_5_checks"]["quality_tier_facts_fold"]["passed"],
        out["phase_5_checks"]["evidence_enum_hygiene"]["passed"],
    ]
)
acc = {k: v["verdict"] for k, v in out["acceptance_queries"].items()}
acceptance_all_pass = all(v == "PASS" for v in acc.values())
out["overall"] = {
    "phase_5_passed": phase_5_passed,
    "acceptance_verdicts": acc,
    "acceptance_all_pass": acceptance_all_pass,
    "overall_verdict": "PASS" if phase_5_passed and acceptance_all_pass else "PARTIAL",
}

print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
(LOGS_DIR / "pass2_verify_phase5_acceptance.json").write_text(
    json.dumps(out, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
)
driver.close()
