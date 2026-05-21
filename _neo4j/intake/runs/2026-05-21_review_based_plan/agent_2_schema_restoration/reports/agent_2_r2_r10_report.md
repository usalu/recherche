# Agent 2 — R2 + R10 Migration Report

**Run:** 2026-05-21  
**Stage:** 2 (R2) + 3 (R10)  
**Graph:** `mit-bestand`

---

## Summary

| Phase | Status | Nodes created | Edges created |
|-------|--------|---------------|---------------|
| R2.a  | PASS   | 6 Layer       | 15 TEILT_LAYER |
| R2.b  | PASS   | 5 LCAModule   | 8 BERECHNET_NACH_MODUL, 8 METHODENGRUNDLAGE_NORM |
| R2.c  | PASS   | 9 RB (journal) + 6 stubs = 15 | 12 HAT_RECHTLICHE_BEDINGUNG, 5 GILT_IN_LAND, 18 BELEGT_IN |
| R2.d  | PASS   | 8 Zertifizierungssystem | 12 HAT_ZERTIFIZIERUNG, 6 BELEGT_IN |
| R2.e  | PASS   | 0 (secondary label) | 0 (8 :Tool labels added) |
| R10   | PASS   | 13 DeprecatedType | — |

**Pre-R2:**  `3 802 nodes / 25 023 rels`  
**Post-R2:** `3 836 nodes / 25 107 rels`  
**Post-R10:** `3 849 nodes / 25 107 rels`

---

## R2 Acceptance Gates (all 12 PASS)

| Gate | Expected | Actual |
|------|----------|--------|
| `:Layer` count | exact=6 | 6 |
| `TEILT_LAYER` count | min=15 | 15 |
| `:LCAModule` count | exact=5 | 5 |
| `BERECHNET_NACH_MODUL` count | min=5 | 8 |
| `:RechtlicheBedingung` count | min=9 | 15 |
| `HAT_RECHTLICHE_BEDINGUNG` count | min=5 | 12 |
| `GILT_IN_LAND` from RB | min=3 | 5 |
| `:Zertifizierungssystem` count | exact=8 | 8 |
| `HAT_ZERTIFIZIERUNG` count | min=5 | 12 |
| `:Tool` count | exact=8 | 8 |
| `:Tool` without `:Software` | zero | 0 |
| `Bauteiltyp.brand_layer` without TEILT_LAYER | zero | 0 |

---

## R10 Acceptance Gates (2 PASS)

| Gate | Expected | Actual |
|------|----------|--------|
| `:DeprecatedType` count | min=12 | 13 |
| distinct kinds | info | label=3, rel_type=10 |

---

## Implementation Notes

### R2.c: Extra stubs
6 `RechtlicheBedingung` nodes had no journal entry but appear in `q_bauteilreuse_legal_regime_matrix_md.legal_conditions`:
- `rb_bauproduktenverordnung_cpr`, `rb_denkmalschutz`, `rb_dibt_zustimmung`
- `rb_kreislaufwirtschaftsgesetz_krwg`, `rb_materialpass`, `rb_schweizer_bauproduktegesetz`

Created as stubs with `evidence_basis='registry_stub'`, `evidence_confidence='unklar'`. All 15 RB nodes get `BELEGT_IN → q_bauteilreuse_legal_regime_matrix_md`.

### R2.d: `ZertifizierungBewertungssystem` alias
Old label name preserved as a string alias in `z.aliases` property. `:DeprecatedType` record (id: `dep_label__ZertifizierungBewertungssystem`) points to new label `Zertifizierungssystem`.

### R2.b: LCA IDs
Original journal IDs (`lz_*` prefix) kept intact. The brief's `lcm_*` prefix was NOT in the journal and was not used.

### R2.e: Secondary label pattern
`:Tool` added as a secondary label on all `:Software {kind:'tool'}` nodes (8 nodes). All 8 remain `:Software` nodes — no orphan `:Tool` violations.

### R10: Semicolons in string literals
R10 Cypher initially failed because `reason` strings contained `;` which the statement splitter interpreted as statement boundaries. Fixed by replacing internal semicolons with ` —`.

---

## Files

| File | Purpose |
|------|---------|
| `migrations/mig_r2_a_restore_layer.cypher` | Layer nodes + TEILT_LAYER from brand_layer |
| `migrations/mig_r2_b_restore_lca_module.cypher` | LCAModule nodes (edges via runner) |
| `migrations/mig_r2_c_restore_legal.cypher` | RB stubs + BELEGT_IN to matrix Quelle |
| `migrations/mig_r2_d_restore_certifications.cypher` | Zertifizierungssystem nodes (edges via runner) |
| `migrations/mig_r2_e_restore_tool_label.cypher` | :Tool secondary label |
| `migrations/mig_r10_deprecated_type_seed.cypher` | 13 DeprecatedType audit nodes |
| `logs/agent_2_runner.py` | Orchestrator (parameterized journal-edge restoration) |
| `PHASE_R2_DONE.flag` | Written by runner, verified=true |
| `PHASE_R10_DONE.flag` | Written by runner, verified=true |
