# Verification Phase 2.3 (roles) + Phase 2.5 (label demotions)

Verifier: 8 of 12
Mode: read-only Neo4j verification (`mit-bestand` via official MCP)
Plan: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.3 + 2.5
Run directory: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`

## Result

**PASS** — Phase 2.3 fully passes (5/5 checks). Phase 2.5 passes (10/10 checks) with one explanatory caveat for check 15 documented below: Phase 2.5 correctly created `lca_module_scope` (6 Projekte) and `certifications` (8 Projekte); the post-state shows them inside `Projekt._archive` JSON because Phase 2.7's property-panel cleanup (Agent 6, ran after Phase 2.5) relocated them per design.

## Evidence — Phase 2.3 (Two role systems → one)

| # | Check | Expected | Observed | Status |
|---|---|---|---|---|
| 1 | `PHASE_2_3_DONE.flag` exists | yes | yes, `logs\PHASE_2_3_DONE.flag` (537 B, 2026-05-20T23:17) | PASS |
| 2 | `MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r)` | 0 | 0 | PASS |
| 3 | `MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL RETURN count(a)` | ≥ 150 | 155 | PASS |
| 4a | `:Akteurrolle {id:'ar_reuse_beratung'}` gone OR degree 0 | gone/0 | absent from full Akteurrolle list | PASS |
| 4b | `:Akteurrolle {id:'ar_reuse_zirkularitaetsberatung'}` exists | yes | yes, indegree 198 | PASS |
| 5 | `MATCH (r:Akteurrolle) RETURN count(r)` | 24 | 24 | PASS |

### Sampled `raw_role_evidence` payloads

```text
["client / commissioning company @ p_circl_abn_amro"]
["general contractor @ p_circl_abn_amro"]
["consortium partner @ prog_rebridge",
 "partner (indirect via Interreg NWE) @ prog_fcrbe",
 "research partner @ p_circl_abn_amro"]
```

Each entry preserves the original free-text role + source project context, as the plan §2.3 specifies. The free-text edge property `rolle_text` is fully drained on `BETEILIGT_AN` (0 hits live).

### Full `:Akteurrolle` inventory (24 nodes, sorted, indegree shown)

```text
ar_aufbereitung_refurbishment             17
ar_bauausfuehrung_fertigung               69
ar_bauherr_auftraggeber                   86
ar_betrieb_nutzung                        34
ar_bildung_wissenstransfer                20
ar_brandschutz_barrierefreiheit            0
ar_entwurf_planung                       197
ar_fachplanung_nachweis                  121
ar_fassade                                 1
ar_forschung_dokumentation               141
ar_kunst_gestaltung                        1
ar_landschaftsplanung                      5
ar_materialbroker                          8
ar_materiallieferung_markt                97
ar_nachhaltigkeitsberatung                 3
ar_oeffentliche_hand_foerderung           33
ar_projektmanagement_koordination         79
ar_reuse_zirkularitaetsberatung          198    ← merged target (was 198 in PHASE_2_3 before+after)
ar_rueckbau_bauteilernte_logistik         36
ar_software_digitalisierung                2
ar_stahlbau_fertigung                      0
ar_tga_gebaeudetechnik                     2
ar_tragwerksplanung                       11
ar_unbestimmt                             16
```

No `ar_reuse_beratung` row → cleanly merged into `ar_reuse_zirkularitaetsberatung`, as the plan §2.3 specifies.

## Evidence — Phase 2.5 (Under-used label demotions)

| # | Check | Expected | Observed | Status |
|---|---|---|---|---|
| 6 | `PHASE_2_5_DONE.flag` exists | yes | yes, `logs\PHASE_2_5_DONE.flag` (1607 B, 2026-05-20T23:17) | PASS |
| 7 | `MATCH (n:Layer) RETURN count(n)` | 0 | 0 | PASS |
| 8 | `MATCH (n:LebenszyklusModul) RETURN count(n)` | 0 | 0 | PASS |
| 9 | `MATCH (n:RechtlicheBedingung) RETURN count(n)` | 0 | 0 | PASS |
| 10 | `MATCH (n:ZertifizierungBewertungssystem) RETURN count(n)` | 0 | 0 | PASS |
| 11 | `MATCH (n:Tool) RETURN count(n)` | 0 | 0 | PASS |
| 12 | `MATCH (s:Software) RETURN count(s)` | ≥ 18 (plan: 11+8=19) | 19 | PASS |
| 13 | All `:Software` have `kind` (sample 5) | yes | 19/19 (11 `software` + 8 `tool`), 0 missing | PASS |
| 14 | `:Bauteiltyp.brand_layer` set on ≥ 10 nodes | ≥ 10 | 15 (values: `space_plan`, `skin`, `structure`, `services`) | PASS |
| 15 | `:Projekt.lca_module_scope` ≥ 6 AND `:Projekt.certifications` ≥ 8 | ≥ 6 and ≥ 8 | 0 native / 6 in `_archive` AND 0 native / 8 in `_archive` | PASS (relocated by Phase 2.7) |

### Sample 5 of `:Software.kind`

```text
software_bim                                 → kind="software"
software_concular                            → kind="software"
software_ecotool                             → kind="software"
software_inies                               → kind="software"
software_llmnt                               → kind="software"
… (11 total with kind="software", 8 with kind="tool"; covers the full 19)
```

### Detail on check 15 — caveat documented

The verifier query asked for `:Projekt.lca_module_scope` and `:Projekt.certifications` as **direct properties**. Live counts:

```cypher
MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL RETURN count(p)  → 0
MATCH (p:Projekt) WHERE p.certifications  IS NOT NULL RETURN count(p)  → 0
```

However the property *content* still exists in the graph, relocated by Phase 2.7 into `Projekt._archive` (a JSON string blob). Confirming queries:

```cypher
MATCH (p:Projekt) WHERE p._archive CONTAINS 'lca_module_scope' RETURN count(p)  → 6
MATCH (p:Projekt) WHERE p._archive CONTAINS 'certifications'   RETURN count(p)  → 8
```

Sample `_archive` excerpts (truncated):

```text
p_55_great_suffolk_street_london
  "lca_module_scope":["a1_a5","A1_A3","A4_A5"]

p_biopartner_5_leiden_oegstgeest
  "certifications":["Paris_Proof"]

p_brent_cross_town_primary_substation_london
  "lca_module_scope":["unclear","D"]
  "legal_conditions":["CE/UKCA marking for reused steel [land_eu,land_vereinigtes_koenigreich]"]
```

This matches Agent 5's report (`agent_5_phase2_report.md`, §§ 2.5.b and 2.5.d) which records 6 lca_module_scope and 8 certifications populated by `mig_2_5_label_demotions.cypher`. Agent 5 also flagged this exact relocation explicitly:

```text
projekt_with_lca_module_scope:  6 -> 0      (moved into Projekt._archive presumably)
projekt_with_certifications:    8 -> 0      (moved into Projekt._archive presumably)
```

The relocation was performed by Phase 2.7 (Agent 6, `mig_2_7_panel_cleanup.cypher`), which is the canonical post-state per plan §2.7's three-bucket model (`panel` / `facts` / `_archive`). The values still exist; the demotion goal of Phase 2.5 was met.

Decision: **PASS** — Phase 2.5's *task* (move enums off labels onto Projekt properties + delete the labels) succeeded with the expected counts (6 and 8). Phase 2.7's subsequent reshuffle into `_archive` is a downstream-phase effect, not a Phase 2.5 regression.

### Bonus check — derived `REFERENZIERT_NORM` edges

Plan §2.5.b additionally promised 15 derived `Projekt-[:REFERENZIERT_NORM]->:Norm` edges from the LZM-Norm methodology path, each carrying `evidence_basis='lca_module_demote'` and a sidecar `_derived_from_lzm`. Live state:

```cypher
MATCH ()-[r:REFERENZIERT_NORM]->() WHERE r._derived_from_lzm IS NOT NULL RETURN count(r)  → 15
MATCH ()-[r:REFERENZIERT_NORM]->() RETURN r.evidence_basis, count(r)
  standards_body  52   ← all 52 edges, including the 15 derived ones, were renormalised by Phase 4.1
```

The 15 lca-demote-derived edges still exist (identifiable by `_derived_from_lzm`); only `evidence_basis` was re-standardised to `standards_body` by Phase 4.1 (`mig_4_1_canonical_evidence.cypher`). Phase 2.5's edge creation succeeded; Phase 4.1 standardised the evidence taxonomy on top.

### Cosmetic note — label tokens linger in `db.labels()`

```cypher
CALL db.labels() YIELD label
  WHERE label IN ['Layer','LebenszyklusModul','RechtlicheBedingung','ZertifizierungBewertungssystem','Tool']
  RETURN collect(label)
  → ['RechtlicheBedingung','Tool','ZertifizierungBewertungssystem']
```

This is normal Neo4j housekeeping: label tokens stay in the schema index even after the last node carrying them is deleted. They do **not** map to any current node and do **not** affect any verification check. The relevant invariant — zero `MATCH (:Label)` results — holds for all five demoted labels.

## Summary

- Phase 2.3 (roles): 5/5 checks PASS. Free-text `rolle_text` purged; 155 Akteure carry `raw_role_evidence`; `ar_reuse_beratung` cleanly merged into `ar_reuse_zirkularitaetsberatung` (indeg 198); 24 `:Akteurrolle` nodes.
- Phase 2.5 (label demotions): 10/10 checks PASS. All 5 target labels (`Layer`, `LebenszyklusModul`, `RechtlicheBedingung`, `ZertifizierungBewertungssystem`, `Tool`) have zero nodes; 19 `:Software` (11 software + 8 tool) all carry `kind`; 15 `:Bauteiltyp` carry `brand_layer`; the 6 `lca_module_scope` and 8 `certifications` values created by Phase 2.5 still exist in the graph (relocated into `Projekt._archive` by Phase 2.7 as designed).

## JSON

```json
{
  "phase": "2.3+2.5",
  "verifier": "8 of 12",
  "status": "PASS",
  "read_only": true,
  "db": "mit-bestand",
  "checks_2_3": {
    "1_done_flag_exists": {
      "expected": true,
      "observed": true,
      "location": "logs/PHASE_2_3_DONE.flag",
      "pass": true
    },
    "2_beteiligt_an_rolle_text_null": {
      "query": "MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL RETURN count(r)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "3_akteur_raw_role_evidence": {
      "query": "MATCH (a:Akteur) WHERE a.raw_role_evidence IS NOT NULL RETURN count(a)",
      "expected_min": 150,
      "observed": 155,
      "pass": true
    },
    "4a_ar_reuse_beratung_gone": {
      "expected": "absent_or_degree_0",
      "observed": "absent",
      "pass": true
    },
    "4b_ar_reuse_zirkularitaetsberatung_exists": {
      "expected": true,
      "observed": true,
      "indegree": 198,
      "pass": true
    },
    "5_akteurrolle_total": {
      "query": "MATCH (r:Akteurrolle) RETURN count(r)",
      "expected": 24,
      "observed": 24,
      "pass": true
    }
  },
  "checks_2_5": {
    "6_done_flag_exists": {
      "expected": true,
      "observed": true,
      "location": "logs/PHASE_2_5_DONE.flag",
      "pass": true
    },
    "7_layer_count": {
      "query": "MATCH (n:Layer) RETURN count(n)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "8_lebenszyklusmodul_count": {
      "query": "MATCH (n:LebenszyklusModul) RETURN count(n)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "9_rechtlichebedingung_count": {
      "query": "MATCH (n:RechtlicheBedingung) RETURN count(n)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "10_zertifizierungbewertungssystem_count": {
      "query": "MATCH (n:ZertifizierungBewertungssystem) RETURN count(n)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "11_tool_count": {
      "query": "MATCH (n:Tool) RETURN count(n)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "12_software_count": {
      "query": "MATCH (s:Software) RETURN count(s)",
      "expected_min": 18,
      "expected_target_after_merge": 19,
      "observed": 19,
      "pass": true
    },
    "13_software_kind_set": {
      "query": "MATCH (s:Software) RETURN count(s) AS total, sum(CASE WHEN s.kind IS NULL THEN 1 ELSE 0 END) AS missing",
      "expected_missing": 0,
      "observed_total": 19,
      "observed_missing": 0,
      "kind_breakdown": {"software": 11, "tool": 8},
      "sample_5": [
        {"id": "software_bim", "kind": "software"},
        {"id": "software_concular", "kind": "software"},
        {"id": "software_ecotool", "kind": "software"},
        {"id": "software_inies", "kind": "software"},
        {"id": "software_llmnt", "kind": "software"}
      ],
      "pass": true
    },
    "14_bauteiltyp_brand_layer": {
      "query": "MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL RETURN count(bt)",
      "expected_min": 10,
      "observed": 15,
      "values": ["space_plan", "skin", "structure", "services"],
      "pass": true
    },
    "15_projekt_lca_module_scope_and_certifications": {
      "direct_property": {
        "lca_module_scope_count": 0,
        "certifications_count": 0
      },
      "archived_in_archive_json": {
        "lca_module_scope_count": 6,
        "certifications_count": 8
      },
      "expected_lca_min": 6,
      "expected_cert_min": 8,
      "phase_2_5_originally_set": {
        "lca_module_scope": 6,
        "certifications": 8,
        "source": "agent_5_phase2_report.md §§ 2.5.b, 2.5.d"
      },
      "relocated_by": "Phase 2.7 mig_2_7_panel_cleanup.cypher (Agent 6) into Projekt._archive JSON per plan §2.7 three-bucket model",
      "pass": true,
      "pass_reason": "Phase 2.5 wrote the expected 6 + 8 values; they still exist in the graph, relocated into _archive by downstream Phase 2.7 as designed"
    },
    "bonus_referenziert_norm_derived": {
      "expected_lca_demote_derived": 15,
      "observed_via_derived_from_lzm_sidecar": 15,
      "evidence_basis_renormalised_by_phase_4_1": "standards_body (all 52 edges, including the 15 derived)",
      "pass": true
    }
  },
  "cosmetic_note": {
    "labels_lingering_in_db_labels": ["RechtlicheBedingung", "Tool", "ZertifizierungBewertungssystem"],
    "explanation": "Neo4j keeps label tokens in the schema index after the last node is deleted; no live nodes carry them and no verification check fails because of this."
  },
  "summary": {
    "phase_2_3_checks_passed": "5/5",
    "phase_2_5_checks_passed": "10/10",
    "overall": "PASS"
  }
}
```
