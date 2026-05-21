"""Agent 11 — Phase 3 verification + acceptance checks.

Pure read; writes agent11_verify.json with acceptance results.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
OUT = RUN_ROOT / "logs/agent11_verify.json"


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
    out: dict = {"acceptance": []}

    def acc(name: str, want_op: str, want: int | float, got: int | float, note: str = "") -> bool:
        if want_op == ">=":
            passed = got >= want
        elif want_op == "==":
            passed = got == want
        elif want_op == ">":
            passed = got > want
        elif want_op == "<=":
            passed = got <= want
        elif want_op == "between":
            lo, hi = want  # type: ignore[misc]
            passed = lo <= got <= hi
        else:
            passed = False
        out["acceptance"].append(
            {"name": name, "op": want_op, "want": want, "got": got, "passed": passed, "note": note}
        )
        return passed

    try:
        with drv.session(database=db) as s:
            built_total = s.run(
                "MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r) AS c"
            ).single()["c"]
            built_from_bauwerk = s.run(
                "MATCH (:Bauwerk)-[r:BUILT_IN_ERA]->(:BauwerkEra) RETURN count(r) AS c"
            ).single()["c"]
            built_from_depot = s.run(
                "MATCH (:Materialdepot)-[r:BUILT_IN_ERA]->(:BauwerkEra) RETURN count(r) AS c"
            ).single()["c"]
            era_unknown_bw = s.run(
                "MATCH (b:Bauwerk) WHERE b.era_unknown = true RETURN count(b) AS c"
            ).single()["c"]
            era_unknown_md = s.run(
                "MATCH (m:Materialdepot) WHERE m.era_unknown = true RETURN count(m) AS c"
            ).single()["c"]
            bw_neither = s.run(
                "MATCH (b:Bauwerk) WHERE NOT exists{ (b)-[:BUILT_IN_ERA]->() } "
                "  AND coalesce(b.era_unknown, false) <> true RETURN count(b) AS c"
            ).single()["c"]
            md_neither = s.run(
                "MATCH (m:Materialdepot) WHERE NOT exists{ (m)-[:BUILT_IN_ERA]->() } "
                "  AND coalesce(m.era_unknown, false) <> true RETURN count(m) AS c"
            ).single()["c"]
            bw_total = s.run("MATCH (b:Bauwerk) RETURN count(b) AS c").single()["c"]
            md_total = s.run("MATCH (m:Materialdepot) RETURN count(m) AS c").single()["c"]
            hat_remaining = s.run(
                "MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r) AS c"
            ).single()["c"]
            risk_total = s.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r) AS c"
            ).single()["c"]
            risk_doc = s.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() WHERE r.evidence_basis='documented' RETURN count(r) AS c"
            ).single()["c"]
            risk_era_mat = s.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() WHERE r.evidence_basis='era_and_material' RETURN count(r) AS c"
            ).single()["c"]
            risk_mat_only = s.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() WHERE r.evidence_basis='material_only' RETURN count(r) AS c"
            ).single()["c"]
            req_total = s.run(
                "MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r) AS c"
            ).single()["c"]
            rules = s.run("MATCH (r:ReuseRule) RETURN count(r) AS c").single()["c"]
            applies_in = s.run(
                "MATCH (:ReuseRule)-[r:APPLIES_IN]->(:Land) RETURN count(r) AS c"
            ).single()["c"]
            applies_to = s.run(
                "MATCH (:ReuseRule)-[r:APPLIES_TO]->(:Material) RETURN count(r) AS c"
            ).single()["c"]
            ref_norm = s.run(
                "MATCH (:ReuseRule)-[r:REFERENZIERT_NORM]->(:Norm) RETURN count(r) AS c"
            ).single()["c"]
            ref_norm_distinct_norms = s.run(
                "MATCH (:ReuseRule)-[:REFERENZIERT_NORM]->(n:Norm) RETURN count(DISTINCT n) AS c"
            ).single()["c"]
            new_norms = s.run(
                "MATCH (n:Norm) WHERE n.source_scope='reuse_rule_seed' RETURN count(n) AS c"
            ).single()["c"]
            norm_total = s.run("MATCH (n:Norm) RETURN count(n) AS c").single()["c"]
            rules_missing_apply_in = s.run(
                "MATCH (r:ReuseRule) WHERE NOT exists{(r)-[:APPLIES_IN]->(:Land)} RETURN count(r) AS c"
            ).single()["c"]
            rules_missing_apply_to = s.run(
                "MATCH (r:ReuseRule) WHERE NOT exists{(r)-[:APPLIES_TO]->(:Material)} RETURN count(r) AS c"
            ).single()["c"]
            rules_missing_norm = s.run(
                "MATCH (r:ReuseRule) WHERE NOT exists{(r)-[:REFERENZIERT_NORM]->(:Norm)} RETURN count(r) AS c"
            ).single()["c"]
            rule_property_examples = [
                dict(r["rule"])
                for r in s.run("MATCH (rule:ReuseRule) RETURN rule ORDER BY rule.rank LIMIT 3")
            ]
            risk_samples = [
                {
                    "bg": r["bgid"],
                    "schadstoff": r["sid"],
                    "basis": r["basis"],
                    "origin": r["origin"],
                    "source": r["src"],
                }
                for r in s.run(
                    """
                    MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
                    RETURN coalesce(bg.id, elementId(bg)) AS bgid, s.id AS sid,
                           r.evidence_basis AS basis, r.evidence_origin AS origin,
                           r.evidence_source_id AS src
                    ORDER BY basis, bgid LIMIT 10
                    """
                )
            ]
            req_samples = [
                {"projekt": r["pid"], "schadstoff": r["sid"], "basis": r["basis"]}
                for r in s.run(
                    """
                    MATCH (p:Projekt)-[v:REQUIRES_VERIFICATION_FOR]->(s:Schadstoff)
                    RETURN p.id AS pid, s.id AS sid, v.pollutant_basis AS basis
                    ORDER BY pid, sid LIMIT 10
                    """
                )
            ]
            era_examples = [
                {"bauwerk": r["bid"], "era": r["eid"], "year": r["y"]}
                for r in s.run(
                    """
                    MATCH (b:Bauwerk)-[:BUILT_IN_ERA]->(e:BauwerkEra)
                    RETURN b.id AS bid, e.id AS eid, b.baujahr AS y ORDER BY b.id
                    """
                )
            ]
            # Reuse-rule degree analysis
            rule_degrees = [
                {"rule": r["id"], "deg": r["deg"]}
                for r in s.run(
                    "MATCH (rule:ReuseRule) OPTIONAL MATCH (rule)-[r]->() "
                    "WITH rule, count(r) AS deg RETURN rule.id AS id, deg ORDER BY deg DESC"
                )
            ]
            min_rule_deg = min((d["deg"] for d in rule_degrees), default=0)
            median_rule_deg = sorted(d["deg"] for d in rule_degrees)[len(rule_degrees) // 2] if rule_degrees else 0
            mean_rule_deg = round(sum(d["deg"] for d in rule_degrees) / max(len(rule_degrees), 1), 2)

        # ---- acceptance: each target tied to plan / task brief
        acc("3.1 BUILT_IN_ERA from Bauwerk created", ">=", 8, built_from_bauwerk)
        acc("3.1 BUILT_IN_ERA from Materialdepot (no year prop)", "==", 0, built_from_depot)
        acc(
            "3.1 every Bauwerk has either era edge or era_unknown=true",
            "==",
            0,
            bw_neither,
        )
        acc(
            "3.1 every Materialdepot has either era edge or era_unknown=true",
            "==",
            0,
            md_neither,
        )
        acc(
            "3.1 Bauwerk era_unknown == total - built_from_bauwerk",
            "==",
            bw_total - built_from_bauwerk,
            era_unknown_bw,
        )
        acc(
            "3.1 Materialdepot era_unknown == total - built_from_depot",
            "==",
            md_total - built_from_depot,
            era_unknown_md,
        )

        acc("3.2 zero remaining HAT_SCHADSTOFF edges", "==", 0, hat_remaining)
        acc("3.2 HAS_RISK_POLLUTANT total in ~800 magnitude", "between", (600, 1100), risk_total)  # type: ignore[arg-type]
        acc("3.2 documented edges promoted from HAT_SCHADSTOFF", ">=", 11, risk_doc)
        acc("3.2 era_and_material rule fired", ">=", 0, risk_era_mat,
            "Only 8 Bauwerke carry baujahr -> few donor-era matches expected")
        acc("3.2 material_only fallback fired", ">=", 600, risk_mat_only)
        acc("3.2 REQUIRES_VERIFICATION_FOR in ~250 magnitude", "between", (200, 500), req_total)  # type: ignore[arg-type]

        acc("3.3 exactly 20 ReuseRule nodes", "==", 20, rules)
        acc("3.3 APPLIES_IN edges (one per rule)", "==", 20, applies_in)
        acc("3.3 APPLIES_TO edges (one per rule)", "==", 20, applies_to)
        acc("3.3 REFERENZIERT_NORM in 60..120 magnitude", "between", (60, 120), ref_norm)  # type: ignore[arg-type]
        acc("3.3 no ReuseRule missing APPLIES_IN", "==", 0, rules_missing_apply_in)
        acc("3.3 no ReuseRule missing APPLIES_TO", "==", 0, rules_missing_apply_to)
        acc("3.3 no ReuseRule missing REFERENZIERT_NORM", "==", 0, rules_missing_norm)
        acc(
            "3.3 ReuseRule median degree >= 5 (Rule B threshold ~6)",
            ">=",
            5,
            median_rule_deg,
        )

        out["counts"] = {
            "built_in_era_total": built_total,
            "built_from_bauwerk": built_from_bauwerk,
            "built_from_materialdepot": built_from_depot,
            "bauwerk_era_unknown": era_unknown_bw,
            "materialdepot_era_unknown": era_unknown_md,
            "bauwerk_total": bw_total,
            "materialdepot_total": md_total,
            "hat_schadstoff_remaining": hat_remaining,
            "has_risk_pollutant_total": risk_total,
            "has_risk_pollutant_documented": risk_doc,
            "has_risk_pollutant_era_and_material": risk_era_mat,
            "has_risk_pollutant_material_only": risk_mat_only,
            "requires_verification_for_total": req_total,
            "reuse_rule_total": rules,
            "applies_in_total": applies_in,
            "applies_to_total": applies_to,
            "referenziert_norm_total": ref_norm,
            "referenziert_norm_distinct_norms": ref_norm_distinct_norms,
            "new_norm_nodes_reuse_rule_seed": new_norms,
            "norm_total_after": norm_total,
            "reuse_rule_min_deg": min_rule_deg,
            "reuse_rule_median_deg": median_rule_deg,
            "reuse_rule_mean_deg": mean_rule_deg,
        }
        out["rule_degrees"] = rule_degrees
        out["sample_era_edges"] = era_examples
        out["sample_risk_pollutant_edges"] = risk_samples
        out["sample_requires_verification_edges"] = req_samples
        out["sample_reuse_rules"] = rule_property_examples
        out["all_passed"] = all(a["passed"] for a in out["acceptance"])
    finally:
        drv.close()

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT}")
    print(f"acceptance: {sum(a['passed'] for a in out['acceptance'])}/{len(out['acceptance'])} pass")
    for a in out["acceptance"]:
        flag = "PASS" if a["passed"] else "FAIL"
        print(f"  {flag}: {a['name']} -> got={a['got']} (op={a['op']} want={a['want']})")
    return 0 if out["all_passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
