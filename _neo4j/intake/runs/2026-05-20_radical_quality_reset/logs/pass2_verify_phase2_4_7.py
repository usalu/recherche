"""Pass-2 Detailed Verifier 7/12 — Phase 2.4 + 2.7 (incl. panel repair).

Read-only against `mit-bestand`. Writes a JSON verdict alongside this script
and a Markdown report under reports/. Driver creds resolved from
E:/recherche/.cursor/mcp.json.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "runs"
    / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
REPORTS_DIR = RUN_ROOT / "reports"

MCP_JSON = REPO_ROOT / ".cursor" / "mcp.json"

# Legacy keys from agent6_runner.py.
LEGACY_YEAR_KEYS = [
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
]  # 13 keys

# Extend the runner's 9 to the canonical 11-field area set the task asks for
# (the runner explicitly excluded hoehe_m / breite_m because they aren't areas
# — they would normally land in _archive via Phase 2.7).
LEGACY_AREA_KEYS = [
    "flaeche_m2",
    "flaeche_m2_min",
    "flaeche_m2_max",
    "bgf_m2",
    "flaeche_m2_alternative",
    "nutzflaeche_m2",
    "grundstueck_m2",
    "flaeche_sqft_min",
    "flaeche_sqft_max",
    "hoehe_m",
    "breite_m",
]  # 11 keys (per the task's specification)

# Counter keys: the 22 explicit patterns in the runner plus the unmatched
# counters that the agent report listed; we additionally do a structural
# pattern check (`*_anzahl`, `anzahl_*`, `volumen_*`).
LEGACY_COUNTER_KEYS = [
    # The 22 actively-handled patterns
    "ursprungs_deckenplatten_anzahl",
    "reuse_deckenplatten_anzahl",
    "ursprungs_innenwandplatten_anzahl",
    "reuse_wandplatten_anzahl",
    "wiederverwendete_fertigteile_anzahl",
    "fenster_anzahl",
    "fensterrahmen_anzahl",
    "holztueren_anzahl",
    "leuchten_anzahl",
    "stahltraeger_anzahl",
    "anzahl_stuetzen",
    "anzahl_schalter",
    "pv_paneele_anzahl",
    "led_light_tubes_anzahl",
    "teppichfliesen_anzahl",
    "granitfliesen_anzahl",
    "demontierte_bodenelemente_anzahl",
    "demontierte_fassadenelemente_anzahl",
    "hcs_anzahl",
    "anzahl_reuse_slabs",
    "reuse_hohlkoerperdecken_anzahl",
    "hohlkoerperdecken_anzahl",
    # Additional one-off counters mentioned in agent_6 report as un-mapped
    "wohnungen_anzahl",
    "donor_bauwerke_anzahl",
    "videokassetten_anzahl",
    "elemente_anzahl",
    "module_anzahl",
    "tueren_anzahl",
    "stuetzen_anzahl",
    "tragwerk_komponenten_anzahl",
]  # 30 explicit counter keys per the task's count

LEGACY_QUALITY_TIER_SCALARS = [
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


def resolve_creds() -> tuple[str, str, str, str]:
    if MCP_JSON.exists():
        cfg = json.loads(MCP_JSON.read_text(encoding="utf-8"))
        env = (
            cfg.get("mcpServers", {})
            .get("Neo4j-Official", {})
            .get("env", {})
        )
        uri = env.get("NEO4J_URI", "bolt://localhost:7687")
        user = env.get("NEO4J_USERNAME", "neo4j")
        pw = env.get("NEO4J_PASSWORD", "")
        db = env.get("NEO4J_DATABASE", "mit-bestand")
        return uri, user, pw, db
    return ("bolt://localhost:7687", "neo4j", os.environ.get("NEO4J_PASSWORD", ""), "mit-bestand")


def main() -> dict[str, Any]:
    uri, user, pw, db = resolve_creds()
    driver = GraphDatabase.driver(uri, auth=(user, pw))
    out: dict[str, Any] = {
        "verifier": "Pass-2 Detailed Verifier 7 of 12",
        "phase": "2.4 + 2.7 (incl. panel repair)",
        "database": db,
        "driver_uri": uri,
        "run_dir": str(RUN_ROOT),
    }

    with driver.session(database=db, default_access_mode="READ") as s:
        # ============================================================
        # PHASE 2.4
        # ============================================================
        phase24: dict[str, Any] = {}

        # 1. PHASE_2_4_DONE.flag present
        flag24 = RUN_ROOT / "PHASE_2_4_DONE.flag"
        phase24["check_1_flag_present"] = {
            "expected": "present",
            "got": flag24.exists(),
            "size_bytes": flag24.stat().st_size if flag24.exists() else 0,
            "pass": flag24.exists(),
        }

        # 2. Projekt with year_completed >= 35
        n = s.run(
            "MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p) AS c"
        ).single()["c"]
        phase24["check_2_year_completed"] = {
            "expected": ">= 35",
            "got": n,
            "pass": n >= 35,
        }

        # 3. Projekt with area_m2_gross >= 30
        n = s.run(
            "MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p) AS c"
        ).single()["c"]
        phase24["check_3_area_m2_gross"] = {
            "expected": ">= 30",
            "got": n,
            "pass": n >= 30,
        }

        # 4. Projekt with non-empty cost_facts >= 50
        n = s.run(
            "MATCH (p:Projekt) WHERE p.cost_facts IS NOT NULL "
            "AND size(p.cost_facts) > 0 RETURN count(p) AS c"
        ).single()["c"]
        phase24["check_4_cost_facts_nonempty"] = {
            "expected": ">= 50",
            "got": n,
            "pass": n >= 50,
        }

        # 5. count(:CostEntry)==0, count(:ReuseShare)==0
        n_ce = s.run(
            "MATCH (n:CostEntry) RETURN count(n) AS c"
        ).single()["c"]
        n_rs = s.run(
            "MATCH (n:ReuseShare) RETURN count(n) AS c"
        ).single()["c"]
        phase24["check_5_no_costentry_no_reuseshare"] = {
            "expected": "CostEntry==0 AND ReuseShare==0",
            "CostEntry": n_ce,
            "ReuseShare": n_rs,
            "pass": n_ce == 0 and n_rs == 0,
        }

        # 6. Projekt with non-empty reuse_share_facts >= 4
        n = s.run(
            "MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL "
            "AND size(p.reuse_share_facts) > 0 RETURN count(p) AS c"
        ).single()["c"]
        phase24["check_6_reuse_share_facts_nonempty"] = {
            "expected": ">= 4 (Q3 baseline)",
            "got": n,
            "pass": n >= 4,
        }

        # 7. No Projekt has any of the 13 legacy year fields / 11 legacy
        # area fields / 30 legacy counter fields.
        # 7a: explicit-list check.
        def count_proj_with_any_of(keys: list[str]) -> tuple[int, list[dict[str, Any]]]:
            preds = " OR ".join(
                [f"p.`{k}` IS NOT NULL" for k in keys]
            )
            total = s.run(
                f"MATCH (p:Projekt) WHERE {preds} RETURN count(p) AS c"
            ).single()["c"]
            per_key = [
                dict(
                    k=k,
                    n=s.run(
                        f"MATCH (p:Projekt) WHERE p.`{k}` IS NOT NULL RETURN count(p) AS c"
                    ).single()["c"],
                )
                for k in keys
            ]
            return total, per_key

        n_year, per_year = count_proj_with_any_of(LEGACY_YEAR_KEYS)
        n_area, per_area = count_proj_with_any_of(LEGACY_AREA_KEYS)
        n_counter, per_counter = count_proj_with_any_of(LEGACY_COUNTER_KEYS)

        # 7b: structural pattern check (catches anything we didn't list).
        rows = list(
            s.run(
                """
                MATCH (p:Projekt)
                UNWIND keys(p) AS k
                WITH DISTINCT k
                WHERE k =~ '^(jahr|baujahr|fertigstellung|entwurfsjahr|bau_jahr)([_]|$).*'
                   OR k =~ '^(flaeche|bgf|nutzflaeche|grundstueck|hoehe|breite)([_]|$).*'
                   OR k =~ '.*_anzahl$'
                   OR k =~ '^anzahl_.*'
                   OR k =~ '^volumen_.*'
                RETURN k ORDER BY k
                """
            )
        )
        residual_pattern_keys = [r["k"] for r in rows]

        phase24["check_7_no_legacy_year_area_counter"] = {
            "13_year_fields": {
                "list": LEGACY_YEAR_KEYS,
                "projekt_with_any": n_year,
                "per_key_counts": per_year,
                "pass": n_year == 0,
            },
            "11_area_fields": {
                "list": LEGACY_AREA_KEYS,
                "projekt_with_any": n_area,
                "per_key_counts": per_area,
                "pass": n_area == 0,
            },
            "30_counter_fields": {
                "list": LEGACY_COUNTER_KEYS,
                "projekt_with_any": n_counter,
                "per_key_counts": per_counter,
                "pass": n_counter == 0,
            },
            "structural_pattern_residual_keys_on_Projekt": residual_pattern_keys,
            "structural_pass": len(residual_pattern_keys) == 0,
            "pass": (
                n_year == 0
                and n_area == 0
                and n_counter == 0
                and len(residual_pattern_keys) == 0
            ),
        }

        out["phase_2_4"] = phase24

        # ============================================================
        # PHASE 2.7 (incl. repair)
        # ============================================================
        phase27: dict[str, Any] = {}

        # 8. PHASE_2_7_DONE.flag + PHASE_2_7_5_1_REPAIR_DONE.flag
        flag27 = RUN_ROOT / "PHASE_2_7_DONE.flag"
        flag27_rep = RUN_ROOT / "PHASE_2_7_5_1_REPAIR_DONE.flag"
        phase27["check_8_flags_present"] = {
            "PHASE_2_7_DONE.flag": {
                "present": flag27.exists(),
                "size_bytes": flag27.stat().st_size if flag27.exists() else 0,
            },
            "PHASE_2_7_5_1_REPAIR_DONE.flag": {
                "present": flag27_rep.exists(),
                "size_bytes": flag27_rep.stat().st_size if flag27_rep.exists() else 0,
            },
            "pass": flag27.exists() and flag27_rep.exists(),
        }

        # 9. distinct property keys on :Projekt <= 25; document exact (=22)
        distinct = s.run(
            "MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k) AS c"
        ).single()["c"]
        distinct_list = sorted(
            r["k"]
            for r in s.run(
                "MATCH (p:Projekt) UNWIND keys(p) AS k "
                "RETURN DISTINCT k ORDER BY k"
            )
        )
        phase27["check_9_projekt_distinct_keys"] = {
            "expected": "<= 25 (target 22)",
            "got": distinct,
            "distinct_keys_list": distinct_list,
            "matches_22": distinct == 22,
            "pass": distinct <= 25,
        }

        # 10. max per-node keys on :Projekt <= 18; sample 10 nodes
        max_n = s.run(
            "MATCH (p:Projekt) RETURN max(size(keys(p))) AS m"
        ).single()["m"]
        sample10 = [
            dict(r)
            for r in s.run(
                "MATCH (p:Projekt) RETURN p.id AS id, size(keys(p)) AS n_keys "
                "ORDER BY n_keys DESC LIMIT 10"
            )
        ]
        phase27["check_10_max_per_node_keys"] = {
            "expected": "<= 18",
            "max_per_node_keys": max_n,
            "sample_top10_by_n_keys": sample10,
            "all_sample_le_18": all(r["n_keys"] <= 18 for r in sample10),
            "pass": max_n <= 18 and all(r["n_keys"] <= 18 for r in sample10),
        }

        # 11. :Bauteilgruppe distinct keys <= 30
        bg_distinct = s.run(
            "MATCH (bg:Bauteilgruppe) UNWIND keys(bg) AS k RETURN count(DISTINCT k) AS c"
        ).single()["c"]
        bg_max = s.run(
            "MATCH (bg:Bauteilgruppe) RETURN max(size(keys(bg))) AS m"
        ).single()["m"]
        phase27["check_11_bauteilgruppe_distinct_keys"] = {
            "expected": "<= 30",
            "got_distinct": bg_distinct,
            "max_per_node_keys": bg_max,
            "pass": bg_distinct <= 30,
        }

        # 12. count(:Projekt) with quality_tier_facts non-null == 101
        n_facts = s.run(
            "MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL "
            "RETURN count(p) AS c"
        ).single()["c"]
        n_projekt_total = s.run(
            "MATCH (p:Projekt) RETURN count(p) AS c"
        ).single()["c"]
        phase27["check_12_quality_tier_facts_nonnull"] = {
            "expected": "== 101",
            "got": n_facts,
            "projekt_total": n_projekt_total,
            "pass": n_facts == 101,
        }

        # 13. count(:Projekt) with any legacy quality_tier_* scalar == 0
        preds = " OR ".join(
            [f"p.`{k}` IS NOT NULL" for k in LEGACY_QUALITY_TIER_SCALARS]
        )
        n_legacy = s.run(
            f"MATCH (p:Projekt) WHERE {preds} RETURN count(p) AS c"
        ).single()["c"]
        per_legacy = [
            dict(
                k=k,
                n=s.run(
                    f"MATCH (p:Projekt) WHERE p.`{k}` IS NOT NULL RETURN count(p) AS c"
                ).single()["c"],
            )
            for k in LEGACY_QUALITY_TIER_SCALARS
        ]
        phase27["check_13_legacy_quality_tier_scalars"] = {
            "expected": "== 0",
            "got": n_legacy,
            "legacy_scalars_list": LEGACY_QUALITY_TIER_SCALARS,
            "per_key_counts": per_legacy,
            "pass": n_legacy == 0,
        }

        # 14. Quelle.external_sources non-null == 0
        n_ext = s.run(
            "MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) AS c"
        ).single()["c"]
        phase27["check_14_quelle_external_sources"] = {
            "expected": "== 0",
            "got": n_ext,
            "pass": n_ext == 0,
        }

        # 15. relationships with property name containing 'url', 'http',
        # 'source_file', 'external_sources' == 0
        n_edge_pol = s.run(
            """
            MATCH ()-[r]->()
            WHERE any(k IN keys(r) WHERE toLower(k) CONTAINS 'url'
                                        OR toLower(k) CONTAINS 'http'
                                        OR k = 'source_file'
                                        OR k = 'external_sources')
            RETURN count(r) AS c
            """
        ).single()["c"]
        # also enumerate which keys are present (should be empty)
        offending_keys = [
            r["k"]
            for r in s.run(
                """
                MATCH ()-[r]->()
                UNWIND keys(r) AS k
                WITH DISTINCT k
                WHERE toLower(k) CONTAINS 'url'
                   OR toLower(k) CONTAINS 'http'
                   OR k = 'source_file'
                   OR k = 'external_sources'
                RETURN k ORDER BY k
                """
            )
        ]
        phase27["check_15_edges_with_url_http_source_file_external_sources"] = {
            "expected": "== 0",
            "got": n_edge_pol,
            "offending_edge_property_keys": offending_keys,
            "pass": n_edge_pol == 0,
        }

        # 16. :Akteur.raw_role_evidence non-empty >= 150
        n_rre = s.run(
            "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL "
            "AND size(a.raw_role_evidence) > 0 RETURN count(a) AS c"
        ).single()["c"]
        n_akteur_total = s.run(
            "MATCH (a:Akteur) RETURN count(a) AS c"
        ).single()["c"]
        phase27["check_16_akteur_raw_role_evidence"] = {
            "expected": ">= 150",
            "got": n_rre,
            "akteur_total": n_akteur_total,
            "pass": n_rre >= 150,
        }

        # 17. Sample 5 Projekt with full property dump: _archive +
        # quality_tier_facts + panel scalars.
        sample5 = [
            dict(r)
            for r in s.run(
                """
                MATCH (p:Projekt)
                WHERE p._archive IS NOT NULL
                  AND p.quality_tier_facts IS NOT NULL
                WITH p ORDER BY p.id LIMIT 5
                RETURN p.id AS id,
                       size(keys(p)) AS n_keys,
                       keys(p) AS keys_on_node,
                       properties(p) AS props
                """
            )
        ]

        def shrink_sample(row: dict[str, Any]) -> dict[str, Any]:
            props = dict(row["props"])
            # truncate _archive / quality_tier_facts for readability but
            # keep the head so a human can see the JSON shape.
            for k in ("_archive", "quality_tier_facts", "raw_year_fields"):
                v = props.get(k)
                if isinstance(v, str) and len(v) > 800:
                    props[k] = v[:800] + "..."
            return {
                "id": row["id"],
                "n_keys": row["n_keys"],
                "keys_on_node": sorted(row["keys_on_node"]),
                "has_archive": "_archive" in row["keys_on_node"],
                "has_quality_tier_facts": "quality_tier_facts" in row["keys_on_node"],
                "has_quality_tier": "quality_tier" in row["keys_on_node"],
                "properties_truncated": props,
            }

        phase27["check_17_sample_5_full_dump"] = {
            "sample_5": [shrink_sample(r) for r in sample5],
            "all_have_archive_and_facts": all(
                "_archive" in r["keys_on_node"]
                and "quality_tier_facts" in r["keys_on_node"]
                for r in sample5
            ),
            "all_n_keys_le_18": all(r["n_keys"] <= 18 for r in sample5),
        }

        out["phase_2_7"] = phase27

        # ============================================================
        # Roll-up verdict
        # ============================================================
        checks: list[tuple[str, bool]] = []
        for k, v in phase24.items():
            if isinstance(v, dict) and "pass" in v:
                checks.append((f"phase_2_4.{k}", v["pass"]))
        for k, v in phase27.items():
            if isinstance(v, dict) and "pass" in v:
                checks.append((f"phase_2_7.{k}", v["pass"]))
        all_pass = all(p for _, p in checks)
        out["verdict"] = {
            "overall_pass": all_pass,
            "n_checks_total": len(checks),
            "n_checks_passed": sum(1 for _, p in checks if p),
            "per_check": [{"check": c, "pass": p} for c, p in checks],
        }

        # Counts summary
        out["counts_summary"] = {
            "projekt_total": n_projekt_total,
            "projekt_year_completed_filled": phase24["check_2_year_completed"]["got"],
            "projekt_area_m2_gross_filled": phase24["check_3_area_m2_gross"]["got"],
            "projekt_cost_facts_nonempty": phase24["check_4_cost_facts_nonempty"]["got"],
            "projekt_reuse_share_facts_nonempty": phase24["check_6_reuse_share_facts_nonempty"]["got"],
            "projekt_distinct_keys": phase27["check_9_projekt_distinct_keys"]["got"],
            "projekt_max_per_node_keys": phase27["check_10_max_per_node_keys"]["max_per_node_keys"],
            "projekt_with_quality_tier_facts": phase27["check_12_quality_tier_facts_nonnull"]["got"],
            "projekt_with_legacy_quality_tier_scalar": phase27["check_13_legacy_quality_tier_scalars"]["got"],
            "bauteilgruppe_distinct_keys": phase27["check_11_bauteilgruppe_distinct_keys"]["got_distinct"],
            "quelle_external_sources_nonnull": phase27["check_14_quelle_external_sources"]["got"],
            "edges_with_url_http_etc": phase27["check_15_edges_with_url_http_source_file_external_sources"]["got"],
            "akteur_raw_role_evidence_nonempty": phase27["check_16_akteur_raw_role_evidence"]["got"],
            "akteur_total": n_akteur_total,
            "cost_entry_label_count": phase24["check_5_no_costentry_no_reuseshare"]["CostEntry"],
            "reuse_share_label_count": phase24["check_5_no_costentry_no_reuseshare"]["ReuseShare"],
        }

    driver.close()
    return out


if __name__ == "__main__":
    data = main()
    out_json = LOG_DIR / "pass2_verify_phase2_4_7.json"
    out_json.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    print(json.dumps(data["verdict"], indent=2, ensure_ascii=False))
    print(f"\nFull JSON: {out_json}")
