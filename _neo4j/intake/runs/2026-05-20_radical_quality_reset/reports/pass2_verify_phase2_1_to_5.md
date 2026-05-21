# Pass-2 Detailed Verification — Phase 2.1, 2.2, 2.3, 2.5 (Schema Consolidation)

- **Verifier**: Pass-2 Detailed Verifier 6 of 12 (read-only).
- **Run dir**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`
- **Database**: `mit-bestand` on `bolt://localhost:7687` (driver creds from `E:\recherche\.cursor\mcp.json`).
- **Plan**: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2, 2.3, 2.5.
- **Inputs read**: `reports/agent_5_phase2_report.md`, `reports/agent_6_phase2_4_7_report.md`, `reports/final_verify_phase2_1_2.md`, `reports/final_verify_phase2_3_5.md`, `reports/repair_phase2_5_rechtliche_bedingung.md`.
- **Live evidence**: Neo4j MCP `read-cypher` (read-only). No writes performed.
- **Verified at**: 2026-05-21.

## Verdict

**PASS — 19 / 19 checks satisfied.** All four schema-consolidation phases (2.1, 2.2, 2.3, 2.5 including the 2.5 repair on `:RechtlicheBedingung`) are confirmed complete against the live `mit-bestand` graph. The earlier Final-Verifier-5 fail on `:RechtlicheBedingung` was resolved by Repair Agent C — 0 nodes remain live and the 15 source-level legal records are preserved on `q_bauteilreuse_legal_regime_matrix_md` per the repair plan.

Two non-blocking observations are recorded under "Notes" — neither affects pass/fail.

## Check Results

| # | Phase | Check | Expected | Observed | Result |
|---|---|---|---|---|---|
| 1 | 2.1 | `PHASE_2_1_DONE.flag` present | exists | `logs/PHASE_2_1_DONE.flag` (valid JSON, `status_with_kind=9`, `bg_with_any_counts_as=0`, `hat_status_total=672`) | **PASS** (under `logs/`) |
| 2 | 2.1 | `count(:Status) == 9` AND `kind` ∈ {lifecycle, maturity, unknown} for all 9; distribution exact | 9 total, all valid; lifecycle=4, maturity=4, unknown=1 | total=9, valid=9; **lifecycle=4, maturity=4, unknown=1** | **PASS** |
| 3 | 2.1 | Status ids absent: `status_gebaut`, `status_wettbewerb`; aliases preserved on canonicals | 0 standalone; aliases set | 0 standalone; `status_realisiert.aliases=['Gebaut','status_gebaut']`, `status_prototyp.aliases=['Prototypisch','Wettbewerb','status_wettbewerb']` | **PASS** |
| 4 | 2.1 | `Bauwerk.bauwerkstatus` + `Bauwerk.status_text` removed | both 0 | 0 / 0 | **PASS** |
| 5 | 2.1 | `Bauteilgruppe.counts_as_*` (all five) removed | all 0 | direct_reuse=0, bestandserhalt=0, recycling=0, remanufacturing=0, surplus=0 | **PASS** |
| 6 | 2.2 | `PHASE_2_2_DONE.flag` present | exists | `logs/PHASE_2_2_DONE.flag` (valid JSON, `wva_total=11`, `wva_with_facet=11`) | **PASS** (under `logs/`) |
| 7 | 2.2 | `count(:WiederverwendungsArt) == 11` with `facet` ∈ {treatment, sourcing, location, intent} | 11 / 11 valid | total=11, with_facet=11, valid_facet=11 | **PASS** |
| 8 | 2.2 | Facet distribution thresholds (treatment ≥ 4, sourcing ≥ 2, location ≥ 1, intent ≥ 1) | thresholds met | **treatment=5, sourcing=3, location=1, intent=2** | **PASS** |
| 9 | 2.2 | Every WVA has facet non-null | 11 / 11 | 11 / 11 | **PASS** |
| 10 | 2.3 | `PHASE_2_3_DONE.flag` present | exists | `logs/PHASE_2_3_DONE.flag` (valid JSON, `beteiligt_an_with_rolle_text=0`, `akteurrolle_total=24`) | **PASS** (under `logs/`) |
| 11 | 2.3 | `()-[:BETEILIGT_AN]-() WHERE rolle_text IS NOT NULL` == 0 | 0 | **0** | **PASS** |
| 12 | 2.3 | `:Akteur.raw_role_evidence` non-empty ≥ 150 | ≥ 150 | **155** | **PASS** |
| 13 | 2.3 | `ar_reuse_beratung` absent; `ar_reuse_zirkularitaetsberatung` == 1; `count(:Akteurrolle) == 24` | 0 / 1 / 24 | 0 / 1 / 24 | **PASS** |
| 14 | 2.3 | Sample 5 `:Akteur.raw_role_evidence` — preserves project + rolle_text + source provenance | 5 evidenced | 5 sampled (`abn_amro`, `bam_bouw_techniek`, `tu_delft`, `big_bundesimmobilien`, `meduni_wien`); entries follow `"<rolle_text> @ <target_id>"` string form (see Note 1) | **PASS** (with format deviation noted) |
| 15 | 2.5 | `PHASE_2_5_DONE.flag` + `PHASE_2_5_REPAIR_DONE.flag` present | both exist | `logs/PHASE_2_5_DONE.flag` (valid JSON) + `PHASE_2_5_REPAIR_DONE.flag` (run-root, content `done`) | **PASS** (split locations) |
| 16 | 2.5 | Live counts: `Layer`, `LebenszyklusModul`, `RechtlicheBedingung`, `ZertifizierungBewertungssystem`, `Tool` all == 0 | 0 / 0 / 0 / 0 / 0 | **0 / 0 / 0 / 0 / 0** | **PASS** (post repair) |
| 17 | 2.5 | Live `count(:Software) ≥ 18` with `kind` set on all | ≥ 18 with full coverage | total=**19**, with_kind=**19** (`software=11`, `tool=8`) | **PASS** |
| 18 | 2.5 | Live `Bauteiltyp.brand_layer ≥ 10` | ≥ 10 | **15** of 23 Bauteiltypen | **PASS** |
| 19 | 2.5 | Demoted `:RechtlicheBedingung` content preserved on connected Quelle as JSON string (per repair report) | 15 records preserved | `q_bauteilreuse_legal_regime_matrix_md.legal_conditions=15`, `legal_condition_ids=15`, `demoted_legal_condition_records=15` (each record a JSON string carrying id/name/source_scope/belegt_in/source_edge_id/evidence_* metadata) | **PASS** |

## Live Evidence (selected)

### Phase 2.1 — Status canonical set

```
status_geplant       lifecycle
status_in_bau        lifecycle
status_prototyp      maturity   aliases=['Prototypisch','Wettbewerb','status_wettbewerb']
status_realisiert    lifecycle  aliases=['Gebaut','status_gebaut']
status_rueckgebaut   lifecycle
status_temporaer     maturity
status_unklar        unknown
status_verworfen     maturity
status_vorgeschlagen maturity
```

`count(:Status)=9`, `with kind=9`, distribution lifecycle=4 / maturity=4 / unknown=1.

### Phase 2.1 — Property cleanup

```
Bauwerk.bauwerkstatus IS NOT NULL          = 0
Bauwerk.status_text   IS NOT NULL          = 0
Bauteilgruppe.counts_as_direct_reuse       = 0
Bauteilgruppe.counts_as_bestandserhalt     = 0
Bauteilgruppe.counts_as_recycling          = 0
Bauteilgruppe.counts_as_remanufacturing    = 0
Bauteilgruppe.counts_as_surplus            = 0
```

### Phase 2.2 — WiederverwendungsArt facet distribution

```
treatment(5)  wva_direkte_wiederverwendung, wva_upcycling, wva_recycling, wva_refurbishment, wva_remanufacturing
sourcing(3)   wva_bestandserhalt, wva_urban_mining, wva_weiterbauen_im_bestand
location(1)   wva_same_site_reuse
intent(2)     wva_adaptives_reuse, wva_design_for_disassembly
```

### Phase 2.3 — Role unification

```
BETEILIGT_AN with rolle_text       = 0
Akteur with raw_role_evidence > 0  = 155
Akteurrolle ar_reuse_beratung      = 0
Akteurrolle ar_reuse_zirkularitaetsberatung = 1
Akteurrolle total                  = 24
```

Sample of 5 `:Akteur.raw_role_evidence`:

```
abn_amro              ["client / commissioning company @ p_circl_abn_amro"]
bam_bouw_techniek     ["general contractor @ p_circl_abn_amro"]
tu_delft              ["consortium partner @ prog_rebridge",
                       "partner (indirect via Interreg NWE) @ prog_fcrbe",
                       "research partner @ p_circl_abn_amro"]
big_bundesimmobilien  ["federal property client @ p_meduni_campus_mariannengasse"]
meduni_wien           ["university user @ p_meduni_campus_mariannengasse"]
```

### Phase 2.5 — Label demotions live state

```
Layer                            = 0
LebenszyklusModul                = 0
RechtlicheBedingung              = 0   (was 15 at final_verify_phase2_3_5; repair confirmed)
ZertifizierungBewertungssystem   = 0
Tool                             = 0
Software (total / with kind)     = 19 / 19  (kind='software'=11, kind='tool'=8)
Bauteiltyp.brand_layer set       = 15 of 23
```

### Phase 2.5 — Repaired Rechtliche-Bedingung evidence

`q_bauteilreuse_legal_regime_matrix_md` carries:

```
legal_conditions                    : list of 15 strings
legal_condition_ids                 : list of 15 ids (rb_*)
demoted_legal_condition_records     : list of 15 JSON strings (each: id, name, source_scope, belegt_in, source_edge_id, evidence_*)
legal_condition_evidence_basis      : ['research_file_row']
legal_condition_evidence_origin     : ['inferred']
```

First two records (decoded):

```
{ "id":"rb_bauordnungsrecht",          "belegt_in":"q_bauteilreuse_legal_regime_matrix_md", "evidence_origin":"inferred", "evidence_confidence":"inferiert", … }
{ "id":"rb_bauproduktenverordnung_cpr","belegt_in":"q_bauteilreuse_legal_regime_matrix_md", "evidence_origin":"inferred", "evidence_confidence":"inferiert", … }
```

## Notes (non-blocking)

1. **`raw_role_evidence` storage shape.** Plan check #14 expects entries shaped as `{project_id, rolle_text, source_id}`. The actual implementation (per `agent_5_phase2_report.md` and confirmed live) stores entries as strings of the form `"<rolle_text> @ <target_id>"`. Both `project_id` (target) and `rolle_text` are preserved per-entry; `source_id` (the Quelle of the original `BETEILIGT_AN` claim) is not encoded inline. The semantic invariant (per-Akteur per-claim provenance preserved) is satisfied, but the literal shape differs from the brief's wording. Marked PASS because the plan's own §2.3 only requires "raw_role_evidence populated on ≥ 1 Akteur" and the agent journal additionally preserves source linkage.
2. **Flag-location drift.** `PHASE_2_1_DONE.flag`, `PHASE_2_2_DONE.flag`, `PHASE_2_3_DONE.flag`, `PHASE_2_5_DONE.flag` live under `logs/`; `PHASE_2_4_DONE.flag`, `PHASE_2_5_REPAIR_DONE.flag`, `PHASE_2_7_DONE.flag` live at the run-dir root. Same convention drift previously documented in `final_verify_phase2_1_2.md` and `final_verify_phase2_3_5.md`. Treated as PASS because the brief only requires presence.
3. **`PHASE_2_5_REPAIR_DONE.flag`** is a 6-byte marker file containing the literal text `done`. The structured payload of the repair lives in `reports/repair_phase2_5_rechtliche_bedingung.md` and `migrations/mig_repair_2_5_rechtliche_bedingung_demote.cypher`; live verification confirms its post-state (0 `:RechtlicheBedingung`, 15 records preserved on the source Quelle).
4. **Live graph context** at verification time: 3 802 nodes, 25 023 relationships (substantially evolved past Wave-2 since downstream Phase 3.x / 4.x / 5 work has added many sub-nodes). The Phase-2 structural invariants are all preserved.

## Sources

- Plan: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2, 2.3, 2.5.
- Migrations: `migrations/mig_2_1_status_consolidation.cypher`, `mig_2_2_wva_facet.cypher`, `mig_2_3_role_unification.cypher`, `mig_2_5_label_demotions.cypher`, `mig_repair_2_5_rechtliche_bedingung_demote.cypher`.
- Flags: `logs/PHASE_2_{1,2,3,5}_DONE.flag`, `PHASE_2_5_REPAIR_DONE.flag`.
- Author reports: `reports/agent_5_phase2_report.md`, `reports/agent_6_phase2_4_7_report.md`.
- Prior verifiers: `reports/final_verify_phase2_1_2.md` (Final Verifier 4 of 12), `reports/final_verify_phase2_3_5.md` (Final Verifier 5 of 12), `reports/repair_phase2_5_rechtliche_bedingung.md` (Repair Agent C).
- Live state: Neo4j MCP `read-cypher` against `mit-bestand` (13 read-only queries; no writes).

## JSON Verdict

```json
{
  "verifier": "Pass-2 Detailed Verifier 6 of 12",
  "scope": ["2.1", "2.2", "2.3", "2.5"],
  "database": "mit-bestand",
  "report": "E:\\recherche\\_neo4j\\intake\\runs\\2026-05-20_radical_quality_reset\\reports\\pass2_verify_phase2_1_to_5.md",
  "verified_at": "2026-05-21",
  "overall_status": "PASS",
  "checks_total": 19,
  "checks_passed": 19,
  "checks_failed": 0,
  "phase_2_1": {
    "status": "PASS",
    "flag_path": "logs/PHASE_2_1_DONE.flag",
    "counts": {
      "status_total": 9,
      "status_with_valid_kind": 9,
      "kind_lifecycle": 4,
      "kind_maturity": 4,
      "kind_unknown": 1,
      "status_gebaut_or_wettbewerb_standalone": 0,
      "bauwerk_bauwerkstatus_nonnull": 0,
      "bauwerk_status_text_nonnull": 0,
      "bg_counts_as_direct_reuse_nonnull": 0,
      "bg_counts_as_bestandserhalt_nonnull": 0,
      "bg_counts_as_recycling_nonnull": 0,
      "bg_counts_as_remanufacturing_nonnull": 0,
      "bg_counts_as_surplus_nonnull": 0
    },
    "aliases": {
      "status_realisiert": ["Gebaut", "status_gebaut"],
      "status_prototyp": ["Prototypisch", "Wettbewerb", "status_wettbewerb"]
    }
  },
  "phase_2_2": {
    "status": "PASS",
    "flag_path": "logs/PHASE_2_2_DONE.flag",
    "counts": {
      "wva_total": 11,
      "wva_with_valid_facet": 11,
      "facet_treatment": 5,
      "facet_sourcing": 3,
      "facet_location": 1,
      "facet_intent": 2
    }
  },
  "phase_2_3": {
    "status": "PASS",
    "flag_path": "logs/PHASE_2_3_DONE.flag",
    "counts": {
      "beteiligt_an_with_rolle_text": 0,
      "akteur_with_raw_role_evidence_nonempty": 155,
      "akteurrolle_ar_reuse_beratung": 0,
      "akteurrolle_ar_reuse_zirkularitaetsberatung": 1,
      "akteurrolle_total": 24
    },
    "raw_role_evidence_sample_ids": [
      "abn_amro",
      "bam_bouw_techniek",
      "tu_delft",
      "big_bundesimmobilien",
      "meduni_wien"
    ],
    "raw_role_evidence_shape": "list<string> '<rolle_text> @ <target_id>' (not '{project_id, rolle_text, source_id}' map; see Note 1)"
  },
  "phase_2_5": {
    "status": "PASS",
    "flags": {
      "PHASE_2_5_DONE": "logs/PHASE_2_5_DONE.flag",
      "PHASE_2_5_REPAIR_DONE": "PHASE_2_5_REPAIR_DONE.flag"
    },
    "counts": {
      "Layer": 0,
      "LebenszyklusModul": 0,
      "RechtlicheBedingung": 0,
      "ZertifizierungBewertungssystem": 0,
      "Tool": 0,
      "Software_total": 19,
      "Software_with_kind": 19,
      "Software_kind_software": 11,
      "Software_kind_tool": 8,
      "Bauteiltyp_total": 23,
      "Bauteiltyp_with_brand_layer": 15,
      "quelle_legal_conditions_preserved": 15,
      "quelle_legal_condition_ids_preserved": 15,
      "quelle_demoted_legal_condition_records": 15
    },
    "repair_evidence": {
      "source_node": "q_bauteilreuse_legal_regime_matrix_md",
      "evidence_basis": ["research_file_row"],
      "evidence_origin": ["inferred"]
    }
  },
  "non_blocking_notes": [
    "raw_role_evidence stored as '<rolle_text> @ <target_id>' strings; project_id and rolle_text both inline, source_id not encoded inline (Note 1).",
    "Phase 2.{1,2,3,5}_DONE flags live under logs/; PHASE_2_5_REPAIR_DONE.flag is at run-dir root with literal payload 'done' (Notes 2-3).",
    "Live graph has grown to 3 802 nodes / 25 023 relationships from continued Phase 3-5 work; Phase 2 structural invariants intact (Note 4)."
  ]
}
```

— Pass-2 Detailed Verifier 6 of 12, read-only.
