"""Final independent verification of the 2.7 + 5.1 repair (read-only)."""
from __future__ import annotations

import json
from pathlib import Path

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"
RUN_DIR = Path(r"E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset")


def main() -> dict:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    out: dict = {}
    with driver.session(database=DB, default_access_mode="READ") as s:
        out["projekt_total"] = s.run(
            "MATCH (p:Projekt) RETURN count(p) AS c"
        ).single()["c"]

        out["projekt_distinct_keys"] = s.run(
            "MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k) AS c"
        ).single()["c"]

        out["projekt_distinct_keys_pass_25"] = out["projekt_distinct_keys"] <= 25

        out["max_per_node_keys"] = [
            dict(r)
            for r in s.run(
                "MATCH (p:Projekt) RETURN p.id AS id, size(keys(p)) AS n_keys "
                "ORDER BY n_keys DESC LIMIT 5"
            )
        ]
        out["max_per_node_keys_pass_18"] = (
            max(r["n_keys"] for r in out["max_per_node_keys"]) <= 18
        )

        out["sample_5_panel_keys"] = [
            dict(r)
            for r in s.run(
                "MATCH (p:Projekt) WITH p ORDER BY p.id LIMIT 5 "
                "RETURN p.id AS id, size(keys(p)) AS n_keys, "
                "(p._archive IS NOT NULL) AS has_archive, "
                "(p.quality_tier_facts IS NOT NULL) AS has_facts"
            )
        ]
        out["sample_5_pass_18"] = all(
            r["n_keys"] <= 18 for r in out["sample_5_panel_keys"]
        )

        out["all_tiered"] = s.run(
            "MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL "
            "RETURN count(p) AS c"
        ).single()["c"]
        out["all_tiered_pass_101"] = out["all_tiered"] == out["projekt_total"] == 101

        out["tier_distribution"] = [
            dict(r)
            for r in s.run(
                "MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS n "
                "ORDER BY tier"
            )
        ]
        tier_map = {r["tier"]: r["n"] for r in out["tier_distribution"]}
        out["tier_distribution_pass"] = (
            tier_map.get("tier_1_decision_grade", 0) >= 8
            and tier_map.get("tier_2_documentation_only", 0) >= 50
            and tier_map.get("tier_3_stub", 0) >= 10
        )

        out["facts_present"] = s.run(
            "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL "
            "RETURN count(p) AS c"
        ).single()["c"]
        out["facts_present_pass_101"] = out["facts_present"] == 101

        out["legacy_scalars_present_total"] = s.run(
            "MATCH (p:Projekt) "
            "WHERE p.quality_tier_computed_by IS NOT NULL "
            "   OR p.quality_tier_has_components IS NOT NULL "
            "   OR p.quality_tier_has_evidence IS NOT NULL "
            "   OR p.quality_tier_has_land IS NOT NULL "
            "   OR p.quality_tier_has_metric IS NOT NULL "
            "   OR p.quality_tier_has_year IS NOT NULL "
            "   OR p.quality_tier_n_bg IS NOT NULL "
            "   OR p.quality_tier_n_bg_quantified IS NOT NULL "
            "   OR p.quality_tier_n_curated_evidence IS NOT NULL "
            "RETURN count(p) AS c"
        ).single()["c"]
        out["legacy_scalars_present_pass_0"] = (
            out["legacy_scalars_present_total"] == 0
        )

        out["p_circle_house"] = dict(
            s.run(
                "MATCH (p:Projekt {id:'p_circle_house'}) "
                "RETURN labels(p) AS labels, p.quality_tier AS quality_tier, "
                "p.quality_tier_facts AS quality_tier_facts, "
                "size(keys(p)) AS n_keys"
            ).single()
        )

        out["q3"] = s.run(
            "MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) "
            "UNWIND p.reuse_share_facts AS rs RETURN count(*) AS rows"
        ).single()["rows"]
        out["q3_pass"] = out["q3"] >= 1

        q6 = [
            dict(r)
            for r in s.run(
                "MATCH (p:Projekt)-[r]-() "
                "WITH r.evidence_origin AS origin, count(*) AS c "
                "RETURN origin, c ORDER BY c DESC"
            )
        ]
        out["q6"] = q6
        origins = {r["origin"] for r in q6}
        out["q6_pass"] = {"derived", "curated", "inferred"}.issubset(origins)

        out["bauteilgruppe_distinct_keys"] = s.run(
            "MATCH (bg:Bauteilgruppe) UNWIND keys(bg) AS k "
            "RETURN count(DISTINCT k) AS c"
        ).single()["c"]
        out["bauteilgruppe_pass_30"] = out["bauteilgruppe_distinct_keys"] <= 30

        out["overall_pass"] = all(
            [
                out["projekt_distinct_keys_pass_25"],
                out["max_per_node_keys_pass_18"],
                out["sample_5_pass_18"],
                out["all_tiered_pass_101"],
                out["tier_distribution_pass"],
                out["facts_present_pass_101"],
                out["legacy_scalars_present_pass_0"],
                out["q3_pass"],
                out["q6_pass"],
                out["bauteilgruppe_pass_30"],
            ]
        )

    driver.close()
    return out


if __name__ == "__main__":
    data = main()
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
    (RUN_DIR / "logs" / "repair_2_7_5_1_verify.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str), encoding="utf-8"
    )
