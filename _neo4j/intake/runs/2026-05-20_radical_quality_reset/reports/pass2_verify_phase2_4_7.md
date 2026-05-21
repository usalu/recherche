# Pass-2 Detailed Verification — Phase 2.4 + Phase 2.7 (incl. panel cleanup repair)

- **Verifier:** Pass-2 Detailed Verifier 7 of 12 (read-only)
- **Date:** 2026-05-21
- **Workspace:** `E:\recherche`
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`
- **Database:** `mit-bestand` on `bolt://localhost:7687`
- **Driver creds:** `E:\recherche\.cursor\mcp.json` → user `neo4j`
- **Plan reference:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.4, 2.7
- **Inputs reviewed:**
  - `reports/agent_6_phase2_4_7_report.md` (Wave-2 Agent 6 report)
  - `reports/final_verify_phase2_4_7.md` (Final Verifier 6/12 — Pass 1)
  - `reports/repair_phase2_7_5_1_panel_tier.md` (Repair Agent E)
  - `migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher`
  - `migrations/mig_2_4_projekt_collapse.cypher`
  - `logs/agent6_runner.py` (panel & legacy-key authority)
  - `PHASE_2_4_DONE.flag`, `PHASE_2_7_DONE.flag`, `PHASE_2_7_5_1_REPAIR_DONE.flag`
- **Live verifier script:** `logs/pass2_verify_phase2_4_7.py`
- **Live verifier JSON:**  `logs/pass2_verify_phase2_4_7.json`

## Verdict

**STATUS: PASS** (16 / 16 checks pass on the live graph.)

Phase 2.4 (`:Projekt` property collapse) and Phase 2.7 (three-bucket panel cleanup) are both fully complete on `mit-bestand`. The Phase 2.7 panel residual that Pass-1 Final Verifier 6 had flagged (`:Projekt` distinct keys = 30, max per-node = 26 due to Phase 5.1's 9 `quality_tier_*` audit scalars) has been repaired by Repair Agent E (`mig_repair_2_7_5_1_quality_tier_panel.cypher`, `PHASE_2_7_5_1_REPAIR_DONE.flag`). Distinct `:Projekt` keys are now **22** (≤ 25, exact target), max per-node keys are **18** (≤ 18, exact target), all 101 `:Projekt` carry the new `quality_tier_facts` JSON string, and 0 of them still carry any of the 9 legacy `quality_tier_*` scalars.

## Phase 2.4 — `:Projekt` property collapse (deep checks 1–7)

| # | Check | Expected | Live result | Result |
|---|---|---|---|---|
| 1 | `PHASE_2_4_DONE.flag` present in run dir | present | present, 3 992 B | PASS |
| 2 | `:Projekt` with `year_completed IS NOT NULL` | ≥ 35 | **42** | PASS |
| 3 | `:Projekt` with `area_m2_gross IS NOT NULL` | ≥ 30 | **36** | PASS |
| 4 | `:Projekt` with non-empty `cost_facts` (size > 0) | ≥ 50 | **73** | PASS |
| 5 | `count(:CostEntry) == 0` AND `count(:ReuseShare) == 0` | both 0 | CostEntry=0, ReuseShare=0 | PASS |
| 6 | `:Projekt` with non-empty `reuse_share_facts` (Q3 baseline) | ≥ 4 | **23** | PASS |
| 7 | No `:Projekt` carries any of 13 legacy year fields, 11 legacy area fields, 30 legacy counter fields | 0 of each | 0 / 0 / 0 + structural pattern residual 0 | PASS |

### Check 7 — legacy property residuals (zero on all three groups)

The verifier ran one explicit `WHERE p.<k> IS NOT NULL` count per individual legacy key (per-key counts in `logs/pass2_verify_phase2_4_7.json`) *and* a structural pattern check that catches any property whose key matches `^(jahr|baujahr|fertigstellung|entwurfsjahr|bau_jahr)(_|$).*`, `^(flaeche|bgf|nutzflaeche|grundstueck|hoehe|breite)(_|$).*`, `.*_anzahl$`, `^anzahl_.*`, or `^volumen_.*`. The structural query returns **zero keys**, so no legacy property survives even outside the explicit lists.

| Group | Keys checked | `:Projekt` with any | Structural-pattern residual |
|---|---|---:|---:|
| 13 legacy year fields | `jahr_fertigstellung`, `fertigstellung_jahr`, `jahr_beginn`, `jahr`, `jahr_fertigstellung_geplant`, `jahr_eroeffnung`, `fertigstellung_geplant_jahr`, `jahr_start`, `bau_jahr_von`, `jahr_fertigstellung_max`, `baujahr`, `baujahr_von`, `entwurfsjahr` | **0** | 0 |
| 11 legacy area fields | `flaeche_m2`, `flaeche_m2_min`, `flaeche_m2_max`, `bgf_m2`, `flaeche_m2_alternative`, `nutzflaeche_m2`, `grundstueck_m2`, `flaeche_sqft_min`, `flaeche_sqft_max`, `hoehe_m`, `breite_m` | **0** | 0 |
| 30 legacy counter fields | 22 patterns from `agent6_runner.COUNTER_TO_BG_PATTERNS` + 8 unmatched one-off counters listed in `agent_6_phase2_4_7_report.md` (`wohnungen_anzahl`, `donor_bauwerke_anzahl`, `videokassetten_anzahl`, `elemente_anzahl`, `module_anzahl`, `tueren_anzahl`, `stuetzen_anzahl`, `tragwerk_komponenten_anzahl`) | **0** | 0 |

Notes:
- 5 of the 30 explicit counter keys (`stuetzen_anzahl`, `tragwerk_komponenten_anzahl`, `tueren_anzahl`, `elemente_anzahl`, `module_anzahl`) are **not in the property registry at all** (driver emits `UnknownPropertyKeyWarning`), which is even stronger than "absent from every node" — they were never persisted and are not in the live schema. The remaining 25 keys exist in the registry but are present on 0 :Projekt nodes (already migrated into `raw_year_fields` / `_facts` / `:Bauteilgruppe.menge_stueck` / `_archive`).
- `bewertung` is a legitimate panel key on `:Projekt` and is *not* a legacy field; it represents the curator's evaluation score.

### Live Cypher (Phase 2.4)

```cypher
// Check 2
MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p);                   // 42
// Check 3
MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p);                    // 36
// Check 4
MATCH (p:Projekt) WHERE p.cost_facts IS NOT NULL AND size(p.cost_facts) > 0
RETURN count(p);                                                                         // 73
// Check 5
MATCH (n:CostEntry)  RETURN count(n);                                                    // 0
MATCH (n:ReuseShare) RETURN count(n);                                                    // 0
// Check 6
MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0
RETURN count(p);                                                                         // 23
// Check 7 (structural pattern residual; explicit per-key counts in the JSON)
MATCH (p:Projekt) UNWIND keys(p) AS k WITH DISTINCT k
WHERE k =~ '^(jahr|baujahr|fertigstellung|entwurfsjahr|bau_jahr)(_|$).*'
   OR k =~ '^(flaeche|bgf|nutzflaeche|grundstueck|hoehe|breite)(_|$).*'
   OR k =~ '.*_anzahl$' OR k =~ '^anzahl_.*' OR k =~ '^volumen_.*'
RETURN k;                                                                                // (no rows)
```

## Phase 2.7 — three-bucket panel cleanup (deep checks 8–17)

| # | Check | Expected | Live result | Result |
|---|---|---|---|---|
| 8 | `PHASE_2_7_DONE.flag` AND `PHASE_2_7_5_1_REPAIR_DONE.flag` present | both | PHASE_2_7_DONE.flag = 3 992 B; PHASE_2_7_5_1_REPAIR_DONE.flag = 1 714 B | PASS |
| 9 | `:Projekt` distinct property keys | ≤ 25 (exact 22) | **22** (exact target hit) | PASS |
| 10 | `:Projekt` max per-node key count; sample top 10 | ≤ 18; all sample ≤ 18 | max = **18**; sample 10 nodes all ≤ 18 | PASS |
| 11 | `:Bauteilgruppe` distinct property keys | ≤ 30 | **25** | PASS |
| 12 | `:Projekt` with `quality_tier_facts IS NOT NULL` | == 101 | **101 of 101** | PASS |
| 13 | `:Projekt` with any of the 9 legacy `quality_tier_*` scalars | == 0 | **0** | PASS |
| 14 | `:Quelle.external_sources IS NOT NULL` | == 0 | **0** | PASS |
| 15 | Relationships with property key containing `url`/`http`/`source_file`/`external_sources` | == 0 | **0** (offending key list: empty) | PASS |
| 16 | `:Akteur.raw_role_evidence` non-empty | ≥ 150 | **155** (of 648 total) | PASS |
| 17 | Sample 5 `:Projekt` carry `_archive` JSON string + `quality_tier_facts` JSON string + panel scalars | yes, all 5 | yes, all 5 (n_keys = 13, 13, 13, 14, 15) | PASS |

### Check 9 — the 22 panel keys on `:Projekt` (verbatim, live)

```text
 1. _archive                         (JSON string — Phase 2.7 archive bucket)
 2. actor_registry_loader_seen       (Phase 4b.3 actor-registry residual)
 3. actor_registry_mentioned         (Phase 4b.3 actor-registry residual)
 4. area_m2_gross                    (Phase 2.4.b)
 5. area_m2_range_max                (Phase 2.4.b sidecar)
 6. area_m2_range_min                (Phase 2.4.b sidecar)
 7. bewertung                        (curator evaluation score; panel)
 8. co2_facts                        (Phase 2.4.c list of JSON strings)
 9. cost_facts                       (Phase 2.4.c list of JSON strings)
10. id                               (identity)
11. name                             (panel)
12. name_full                        (panel)
13. node_role                        (panel)
14. nutzung_text                     (panel)
15. project_category                 (Phase 4b.3 residual)
16. projektstatus_text               (panel)
17. quality_tier                     (Phase 5.1 — directly-visible tier label)
18. quality_tier_facts               (Phase 5.1 + repair — single folded JSON string)
19. raw_year_fields                  (Phase 2.4.a JSON-string sidecar)
20. reuse_share_facts                (Phase 2.4.c list of JSON strings)
21. source_scope                     (panel)
22. year_completed                   (Phase 2.4.a)
```

This is the canonical 18-key panel from plan §2.7 (`id`, `name`, `name_full`, `quality_tier`, `year_completed`, `raw_year_fields`, `area_m2_gross`, `area_m2_range_min`, `area_m2_range_max`, `bewertung`, `projektstatus_text`, `nutzung_text`, `node_role`, `cost_facts`, `reuse_share_facts`, `co2_facts`, `source_scope`, `_archive`) plus 4 keys explicitly accounted for by Repair Agent E in `repair_phase2_7_5_1_panel_tier.md` §1.3:

- `quality_tier_facts` — Repair Agent E's folded JSON-string replacement for the 9 Phase-5.1 audit scalars (one panel key in place of 9; matches Pass-1 verifier's recommended remediation).
- `actor_registry_loader_seen`, `actor_registry_mentioned`, `project_category` — additive Phase 4b.3 actor-registry seed flags carried in by Agent 9 / Agent 10 loaders; documented in `agent_12_phase5_report.md` as an additive Phase 4b residual, not a Phase 2.7 regression.

The exact distinct-key count `22` matches the task's documented target.

### Check 10 — sample 10 `:Projekt` ordered by per-node key count (live)

```text
| p.id                                            | n_keys |
|-------------------------------------------------|-------:|
| p_crclr_house_impact_hub_berlin                 |     18 |  ← max
| p_bluecity_offices_rotterdam                    |     17 |
| p_biopartner_5_leiden_oegstgeest                |     17 |
| p_kindergarten_moeoeslistrasse_manegg_zuerich   |     16 |
| p_k118_kopfbau_halle_118_winterthur             |     16 |
| p_big_dig_house_lexington_massachusetts         |     16 |
| p_elys_kultur_gewerbehaus_basel                 |     16 |
| p_chiro_d_itterbeek_dilbeek                     |     16 |
| p_impact_hub_berlin_crclr_fitout                |     16 |
| p_peoples_pavilion_eindhoven                    |     16 |
```

All 10 sampled nodes are ≤ 18 (the explicit panel cap from plan §2.7). The maximum across the whole label is exactly 18, hitting the cap precisely as intended by Repair Agent E (`p_crclr_house_impact_hub_berlin` was the worst-case node carrying all 18 panel-eligible keys including all area / cost / co2 / reuse / actor-registry residuals).

### Check 17 — sample 5 `:Projekt` full panel dump

The 5 alphabetically-first `:Projekt` that carry both `_archive` and `quality_tier_facts` are dumped in full to `logs/pass2_verify_phase2_4_7.json` (`phase_2_7.check_17_sample_5_full_dump.sample_5`). All 5 satisfy: `_archive` is a `STRING` (JSON-encoded), `quality_tier_facts` is a `STRING` (JSON-encoded), `quality_tier` is a `STRING`, and the per-node key count is **13–15** (well under the 18 cap).

Per-node summary:

| id | n_keys | `_archive` | `quality_tier_facts` | `quality_tier` |
|---|---:|---|---|---|
| `p_55_great_suffolk_street_london` | 14 | JSON string (8 archived keys: `note`, `jahr_fertigstellung_erwartet`, `lca_module_scope`, `embodied_carbon_a1_a5_kg_per_m2`, `quantitative_quellen_konflikt`, `co2_einsparung_stahl_t`, `upfront_embodied_carbon_kgco2e_m2_a1_a5`, `property_source`) | JSON: `{computed_by, has_year=true, has_land=true, has_components=false, has_metric=true, has_evidence=false, n_bg=1, n_bg_quantified=1, n_curated_evidence=0, repaired_by, repaired_at}` | `tier_2_documentation_only` |
| `p_association_house_groeditz` | 13 | JSON string (1 archived key: `note`) | JSON: `has_year=true, has_land=true, has_components=false, has_metric=true, has_evidence=true, n_bg=2, n_bg_quantified=2, n_curated_evidence=23` | `tier_2_documentation_only` |
| `p_association_house_plauen` | 13 | JSON string (1 archived key: `note`) | JSON: `has_year=true, has_land=true, has_components=false, has_metric=true, has_evidence=true, n_bg=1, n_bg_quantified=1, n_curated_evidence=28` | `tier_2_documentation_only` |
| `p_awm_muenster_circular_office` | 15 | JSON string (5 archived keys: `abfallvermeidung_t`, `wiedergewonnene_materialien_t`, `circular_or_reuse_products_prozent`, `wasser_einsparung_prozent`, `note`) | JSON: `has_year=true, has_land=true, has_components=true, has_metric=true, has_evidence=false, n_bg=5, n_bg_quantified=0, n_curated_evidence=0` | `tier_2_documentation_only` |
| `p_bedzed_london_hackbridge` | 13 | JSON string (8 archived keys incl. `wohnungen_anzahl=82`, `wiederverwendete_recycelte_materialien_t=3404`, `flaeche_arbeitsbereich_m2_min/max`, `lokale_materialien_prozent=52`, `transport_co2_einsparung_t=120`, …) | JSON: `has_year=true, has_land=true, has_components=true, has_metric=true, has_evidence=false, n_bg=3, n_bg_quantified=1, n_curated_evidence=0` | `tier_2_documentation_only` |

Panel scalars observable on all 5 samples (with appropriate non-null subset): `id`, `name`, `name_full`, `year_completed`, `raw_year_fields`, `source_scope`, `bewertung`, `cost_facts`, `reuse_share_facts`, `co2_facts`. Where `area_m2_gross` is non-null it is panel-visible (e.g. `p_55_great_suffolk_street_london = 1412`, `p_awm_muenster_circular_office = 250`); where the original record had no area it stays absent (no NULL pollution). `_archive` correctly carries the value of every non-panel key on the original node as a JSON-encoded `STRING`, exactly as plan §2.7 requires.

The Repair Agent E fold is visible end-to-end inside each `quality_tier_facts` payload: every value carries the original Phase 5.1 derivation inputs (`has_year`, `has_land`, `has_components`, `has_metric`, `has_evidence`, `n_bg`, `n_bg_quantified`, `n_curated_evidence`, `computed_by`) plus the audit fields (`repaired_by`, `repaired_at`).

### Live Cypher (Phase 2.7)

```cypher
// Check 9 — distinct keys and the full key list
MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k);                          // 22
MATCH (p:Projekt) UNWIND keys(p) AS k RETURN DISTINCT k ORDER BY k;                      // 22-row list
// Check 10
MATCH (p:Projekt) RETURN max(size(keys(p))) AS m;                                        // 18
MATCH (p:Projekt) RETURN p.id, size(keys(p)) ORDER BY size(keys(p)) DESC LIMIT 10;       // 18,17,17,16,…
// Check 11
MATCH (bg:Bauteilgruppe) UNWIND keys(bg) AS k RETURN count(DISTINCT k);                  // 25
MATCH (bg:Bauteilgruppe) RETURN max(size(keys(bg))) AS m;                                // 17
// Check 12
MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL RETURN count(p);                // 101
// Check 13
MATCH (p:Projekt)
WHERE p.quality_tier_computed_by IS NOT NULL OR p.quality_tier_has_components IS NOT NULL
   OR p.quality_tier_has_evidence IS NOT NULL OR p.quality_tier_has_land IS NOT NULL
   OR p.quality_tier_has_metric IS NOT NULL OR p.quality_tier_has_year IS NOT NULL
   OR p.quality_tier_n_bg IS NOT NULL OR p.quality_tier_n_bg_quantified IS NOT NULL
   OR p.quality_tier_n_curated_evidence IS NOT NULL
RETURN count(p);                                                                          // 0
// Check 14
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q);                    // 0
// Check 15
MATCH ()-[r]->()
WHERE any(k IN keys(r) WHERE toLower(k) CONTAINS 'url'
                            OR toLower(k) CONTAINS 'http'
                            OR k = 'source_file' OR k = 'external_sources')
RETURN count(r);                                                                          // 0
MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k
WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
   OR k = 'source_file' OR k = 'external_sources'
RETURN k ORDER BY k;                                                                       // (empty)
// Check 16
MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL AND size(a.raw_role_evidence) > 0
RETURN count(a);                                                                           // 155
```

## Counts summary

| metric | live value |
|---|---:|
| `:Projekt` total | **101** |
| `:Projekt` with `year_completed` | 42 |
| `:Projekt` with `area_m2_gross` | 36 |
| `:Projekt` with non-empty `cost_facts` | 73 |
| `:Projekt` with non-empty `reuse_share_facts` | 23 |
| `:Projekt` distinct property keys | **22** (≤ 25, target hit exactly) |
| `:Projekt` max per-node key count | **18** (≤ 18, target hit exactly) |
| `:Projekt` with `quality_tier_facts` | **101** (= total) |
| `:Projekt` with any legacy `quality_tier_*` scalar | **0** |
| `:Bauteilgruppe` distinct property keys | 25 (≤ 30) |
| `:Bauteilgruppe` max per-node key count | 17 |
| `:Quelle.external_sources` non-null | 0 |
| Edges with `url`/`http`/`source_file`/`external_sources` property keys | 0 |
| `:Akteur.raw_role_evidence` non-empty | 155 (of 648 total) |
| `count(:CostEntry)` | 0 |
| `count(:ReuseShare)` | 0 |

## Sample 5 `:Projekt` (full property dump — abbreviated)

Full per-sample dumps with original `_archive` / `quality_tier_facts` / `raw_year_fields` JSON content (truncated to ~800 chars where verbose) live in `logs/pass2_verify_phase2_4_7.json` → `phase_2_7.check_17_sample_5_full_dump.sample_5`. Top-level fields per sample:

```text
1. p_55_great_suffolk_street_london   — 14 keys; tier_2; year_completed=2024; area_m2_gross=1412
2. p_association_house_groeditz       — 13 keys; tier_2; year_completed=2007
3. p_association_house_plauen         — 13 keys; tier_2; year_completed=2007
4. p_awm_muenster_circular_office     — 15 keys; tier_2; year_completed=2023; area_m2_gross=250;
                                        actor_registry_loader_seen='agent10' (Phase 4b.3)
5. p_bedzed_london_hackbridge         — 13 keys; tier_2; year_completed=2002;
                                        raw_year_fields includes jahr_fertigstellung=2002 AND jahr_beginn=2000;
                                        _archive includes legacy wohnungen_anzahl=82 (correctly archived)
```

All 5 carry: `_archive` (STRING, JSON-encoded), `quality_tier_facts` (STRING, JSON-encoded), `quality_tier` (STRING `tier_2_documentation_only`), plus the panel scalars `id`/`name`/`name_full`/`year_completed`/`raw_year_fields`/`source_scope`/`bewertung`/`cost_facts`/`reuse_share_facts`/`co2_facts`. Per-node key count is 13–15, well under the 18 cap.

## JSON verdict (returned)

```json
{
  "verifier": "Pass-2 Detailed Verifier 7 of 12",
  "phase": "2.4 + 2.7 (incl. panel repair)",
  "database": "mit-bestand",
  "verdict": {
    "overall_pass": true,
    "n_checks_total": 16,
    "n_checks_passed": 16
  },
  "phase_2_4": {
    "check_1_flag_present": {"pass": true, "size_bytes": 3992},
    "check_2_year_completed": {"got": 42, "expected": ">= 35", "pass": true},
    "check_3_area_m2_gross": {"got": 36, "expected": ">= 30", "pass": true},
    "check_4_cost_facts_nonempty": {"got": 73, "expected": ">= 50", "pass": true},
    "check_5_no_costentry_no_reuseshare": {"CostEntry": 0, "ReuseShare": 0, "pass": true},
    "check_6_reuse_share_facts_nonempty": {"got": 23, "expected": ">= 4", "pass": true},
    "check_7_no_legacy_year_area_counter": {
      "13_year_fields_with_any": 0,
      "11_area_fields_with_any": 0,
      "30_counter_fields_with_any": 0,
      "structural_pattern_residual_keys_on_Projekt": [],
      "pass": true
    }
  },
  "phase_2_7": {
    "check_8_flags_present": {
      "PHASE_2_7_DONE.flag":           {"present": true, "size_bytes": 3992},
      "PHASE_2_7_5_1_REPAIR_DONE.flag":{"present": true, "size_bytes": 1714},
      "pass": true
    },
    "check_9_projekt_distinct_keys":              {"got": 22, "expected": "<= 25 (target 22)", "matches_22": true, "pass": true},
    "check_10_max_per_node_keys":                  {"max": 18, "expected": "<= 18", "all_sample_top10_le_18": true, "pass": true},
    "check_11_bauteilgruppe_distinct_keys":        {"got": 25, "max_per_node": 17, "expected": "<= 30", "pass": true},
    "check_12_quality_tier_facts_nonnull":         {"got": 101, "projekt_total": 101, "expected": "== 101", "pass": true},
    "check_13_legacy_quality_tier_scalars":        {"got": 0,   "expected": "== 0", "pass": true},
    "check_14_quelle_external_sources":            {"got": 0,   "expected": "== 0", "pass": true},
    "check_15_edges_with_url_http_source_file_external_sources": {"got": 0, "offending_edge_property_keys": [], "expected": "== 0", "pass": true},
    "check_16_akteur_raw_role_evidence":           {"got": 155, "akteur_total": 648, "expected": ">= 150", "pass": true},
    "check_17_sample_5_full_dump": {
      "all_have_archive_and_facts": true,
      "all_n_keys_le_18": true,
      "sample_5_ids": [
        "p_55_great_suffolk_street_london",
        "p_association_house_groeditz",
        "p_association_house_plauen",
        "p_awm_muenster_circular_office",
        "p_bedzed_london_hackbridge"
      ],
      "sample_5_n_keys": [14, 13, 13, 15, 13]
    }
  },
  "counts_summary": {
    "projekt_total": 101,
    "projekt_year_completed_filled": 42,
    "projekt_area_m2_gross_filled": 36,
    "projekt_cost_facts_nonempty": 73,
    "projekt_reuse_share_facts_nonempty": 23,
    "projekt_distinct_keys": 22,
    "projekt_max_per_node_keys": 18,
    "projekt_with_quality_tier_facts": 101,
    "projekt_with_legacy_quality_tier_scalar": 0,
    "bauteilgruppe_distinct_keys": 25,
    "quelle_external_sources_nonnull": 0,
    "edges_with_url_http_etc": 0,
    "akteur_raw_role_evidence_nonempty": 155,
    "akteur_total": 648,
    "cost_entry_label_count": 0,
    "reuse_share_label_count": 0
  }
}
```

## Sign-off

Phase 2.4 + Phase 2.7 + the Phase 2.7/5.1 panel cleanup repair are fully complete on `mit-bestand`. Every one of the 17 deep checks the task requested (16 numeric + 1 structural sample dump) succeeds against the live graph; both flag files and the repair flag are present and the live counts match (or exceed) the task's documented targets. The Pass-1 residual flagged by Final Verifier 6/12 has been fully addressed by Repair Agent E and is no longer present in the live graph.
