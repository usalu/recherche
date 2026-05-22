# Git Provenance — Agent G5 (SCHEMA_VIOLATION residuals)

**Agent:** G5  
**Date:** 2026-06-06  
**Database:** `mit-bestand` (read-only)  
**Canonical ledger:** `VERIFICATION_LEDGER_ELEMENT.csv` — **33** `SCHEMA_VIOLATION` rows (0.19% of 17,323 elements)  
**Outputs:** [`ledger/provenance_g05.csv`](../ledger/provenance_g05.csv) · generator [`_g05_git_provenance.py`](../_g05_git_provenance.py)

---

## Summary

All **33** post–final-cleanup `SCHEMA_VIOLATION` rows trace to **pre-regulation** import layers (project batches, actor registry, reuse-bubble mesh, legacy `_database` edges). **None** were introduced by `build_vocabulary_graph.py`, regulation cleanup phases 1–8, or Phase B (Variant B typed-law reimport).

| Violation class | Count | Primary git origin | Import / run pipeline |
|---|---:|---|---|
| `teil_von_generic_programm` | 20 | `15222140` (2026-05-13) | Project batch `*.kg.jsonl` + `controlled_vocabulary.seed.kg.jsonl` |
| `generic_programm_vocab` | 5 | `15222140` (2026-05-13) | Same seed — category words as `:Programm` nodes |
| `orphan_actor` | 3 | `1344fced` / `ed1d81d9` | Actor registry + CH reuse-bubble v2 (mesh deletion left orphans) |
| `stadt_zuerich_domain` | 2 | `15222140` + Phase R-C backfill | Geo `:Stadt` node wired with `HAT_AKTEURROLLE` (not `:Akteur`) |
| `duplicate_actor` | 2 | `1344fced` / `ada4dd86` | Early entity mesh + actor-registry expansion |
| `software_self_wiring` | 1 | `d71b13fd` (2026-05-11) | Legacy `_database` → `controlled_terms.delta.jsonl` |

**EP-02 `stadt_zuerich` note:** `EP02-rel-00562` (`stadt_zuerich` —[`HAT_AKTEURTYP`]→ `at_oeffentliche_institution`) was **deleted** in quality pass Q01. The **two remaining** Stadt violations are **`HAT_AKTEURROLLE`** edges (`A12-rel-0001`, `A12-rel-0002`) — a different reltype, same domain breach (geographic `:Stadt` vs actor-only domain).

**Orphan vocab stubs note:** The eight `bt_*` / `mat_*` stubs from `build_vocabulary_graph.py` `TYPE_BY_RW` / `MAT_BY_RW` were **merged away** in Q01 (EP08). They are **not** among the final 33 violations; `build_vocabulary_graph.py` line 679 still lists `bt_fassadenelement` as documentation debt only.

---

## 1. Method

1. Filter `VERIFICATION_LEDGER_ELEMENT.csv` for `verdict=SCHEMA_VIOLATION` (33 rows).
2. Classify each row by violation pattern (orphan, generic programme, Stadt domain, etc.).
3. `git log --reverse -S <id>` pickaxe on `*.jsonl`, `*.csv`, `*.py`, `*.patch.jsonl` to find first introducing commit.
4. `git grep -l` for current repo file pointers (processed records, contracts, archive batches).
5. Cross-walk import pipelines: project batches, actor registry, regulation run (exclusion proof), Q01 remediation log.

---

## 2. Pipeline trace (what did **not** create these rows)

### `build_vocabulary_graph.py` (regulation_graph_vocab_2026_06_04)

- **Scope:** `rf_*`, `nf_*`, `rw_*` nodes and regulation backbone edges (`TRIGGERS_REGULIERUNGSFRAGE`, `ERFORDERT_NACHWEIS`, `BETRIFFT_*`, …).
- **Stub ids:** `TYPE_BY_RW` / `MAT_BY_RW` once emitted duplicate Bauteiltyp/Material stubs (`bt_fassadenelement`, `mat_spannbeton`, …). Q01 merged all eight into curated targets ([`quality_pass_q01.md`](quality_pass_q01.md) §2).
- **Final 33:** **0** rows originate from this generator on the live graph.

### Regulation cleanup phases 1–8 + Phase B (Variant B)

| Phase | Script | Touches SCHEMA_VIOLATION set? |
|---|---|---|
| 1–4 | case evidence, schadstoff, pruefung/leistung | No — regulation rel properties only |
| 5–7 | huerde reuse, axis consolidation, reltype dedup | No — normalizes existing regulation edges |
| 8 | reltype dedup normalize | No |
| **B** | `phaseB_reimport_typed_laws.py` | No — 91 typed law nodes + `GESTUETZT_AUF_REGELWERK` / `GILT_IN_LAND` only |

Phase B commit: `323cd19b` (2026-06-05). Pickaxe on all 33 element ids shows **no** first introduction on that date; violations predate the regulation vocabulary run.

---

## 3. Violation classes (detailed)

### 3.1 EP-02 / Agent 12 — `stadt_zuerich` domain (2 rels)

| claim_id | Edge | Ledger agent | Git first | Live source file |
|---|---|---|---|---|
| `A12-rel-0001` | `stadt_zuerich` —[`HAT_AKTEURROLLE`]→ `ar_bauherr_auftraggeber` | 12 | `15222140` 2026-05-13 | `p_juch_areal_recyclingzentrum_zuerich.kg.jsonl` (archive batch_007) |
| `A12-rel-0002` | `stadt_zuerich` —[`HAT_AKTEURROLLE`]→ `ar_oeffentliche_hand_foerderung` | 12 | `15222140` 2026-05-13 | same |

**Provenance chain**

1. `:Stadt` node `stadt_zuerich` introduced with Zürich project geo imports (batch_005–007, May 2025 migration).
2. Early dossiers used actor id `a_stadt_zuerich` on `HAT_AKTEURROLLE`; later dossiers correctly use `stadt_zuerich_amt_hochbauten` (`p_kindergarten_moeoeslistrasse_manegg_zuerich.kg.jsonl`).
3. Phase R-C (`_neo4j/review/round_002_followup/patches/phase_r.patch.jsonl` lines 124–125) **backfilled** `r.id` on the Stadt→role edges — preserving the domain error with stable ids.
4. Q01 deleted only `HAT_AKTEURTYP` (`EP02-rel-00562`); `HAT_AKTEURROLLE` pair survived.

**Remediation:** Re-point to `stadt_zuerich_amt_hochbauten` or delete (ledger: `ESCALATE_HUMAN`).

### 3.2 Generic `:Programm` category nodes (5 nodes)

| Node id | Name | Git first |
|---|---|---|
| `prog_foerderprogramm` | Foerderprogramm | `15222140` |
| `prog_forschungsprojekt` | Forschungsprojekt | `15222140` |
| `prog_pilotprojekt` | Pilotprojekt | `15222140` |
| `prog_reallabor` | Reallabor | `15222140` |
| `prog_wettbewerb` | Wettbewerb | `15222140` |

Canonical seed: `_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl` (mirrored in `_neo4j/processed/projects/vocabulary/`). These are **controlled vocabulary placeholders** — German category words, not named funding programmes. Agent 10 flagged them; P6-05 carried verdict forward.

### 3.3 `TEIL_VON_PROGRAMM` → generic programmes (20 rels)

All 20 edges link real `:Projekt` nodes to the five category `:Programm` nodes above. Each edge id matches `r_<projekt>__TEIL_VON_PROGRAMM__prog_*` in the corresponding `p_*.kg.jsonl` under `_neo4j/processed/projects/records/`.

**Git clusters**

| First commit | Date | Typical batches |
|---|---|---|
| `15222140` | 2026-05-13 | batch_001, batch_004, batch_005 (early migration) |
| `3fa49bd7` | 2026-05-13 | batch_008, batch_009 |
| `5dd44245` | 2026-05-13 | batch_010, batch_011 |
| `188ebdc5` | 2026-05-13 | batch_006, batch_007 |

**Root cause:** Project import template treated programme *type* (pilot, research, competition) as a shared `:Programm` entity instead of a property or typed edge to a named programme.

### 3.4 Orphan `:Akteur` nodes (3 nodes)

| claim_id | Node | Git first | Notes |
|---|---|---|---|
| `A14-ORPH-001` | `c33_circular_construction_catalyst` | `ed1d81d9` 2026-06-06 | CH actor from Swiss reuse-bubble v2 import; never wired |
| `A14-ORPH-002` | `circular_economy_switzerland` | `ed1d81d9` 2026-06-06 | Same pipeline |
| `A14-ORPH-003` | `repurpose` | `1344fced` 2026-05-08 | NL actor; Tier-1 Dutch mesh-edge deletion (Agent 05) left degree 0 |

### 3.5 Duplicate `:Akteur` identity (2 nodes)

| claim_id | Node | Git first | Canonical target |
|---|---|---|---|
| `A06B-node-0122` | `rau` | `1344fced` 2026-05-08 | `thomas_rau` (F1 merged `rau_architects` → `rau`; firm/person split remains) |
| `A06B-node-0157` | `tomas` | `ada4dd86` 2026-05-14 | `annabelle_von_reutern` / Concular cluster (identity unclear) |

### 3.6 Software self-wiring (1 rel)

| claim_id | Edge | Git first |
|---|---|---|
| `A10-R-047` | `software_bim` —[`NUTZT_SOFTWARE`]→ `tool_bauteilkatalog` | `d71b13fd` 2026-05-11 |

Origin: legacy `_database/_edges/clean_confirmed_edges.csv` → batch `controlled_terms.delta.jsonl` → `controlled_terms.merged.kg.jsonl`. Generic concept nodes wired to each other without factual basis.

---

## 4. Remediation map (ledger actions unchanged)

| Class | Count | Ledger `proposed_action` | Suggested patch owner |
|---|---:|---|---|
| Stadt domain | 2 | `ESCALATE_HUMAN` | Re-point/delete `HAT_AKTEURROLLE` from `:Stadt` |
| Generic programme nodes | 5 | `ESCALATE_HUMAN` | Deprecate nodes; migrate projects to named programmes or drop `TEIL_VON_PROGRAMM` |
| Programme edges | 20 | `ESCALATE_HUMAN` | Delete with parent node cleanup |
| Orphan actors | 3 | `ESCALATE_HUMAN` | Connect with sourced edge or `DEPRECATE_NODE` |
| Duplicate actors | 2 | `ESCALATE_HUMAN` | Merge (rau→thomas_rau pending human gate post-F1) |
| Software self-wiring | 1 | `ESCALATE_HUMAN` | Delete / merge generic tool nodes |

No graph mutations performed by G5 (read-only provenance pass).

---

## 5. Key git commits (reference)

| Commit | Date | Subject | Relevance |
|---|---|---|---|
| `1344fced` | 2026-05-08 | Updated entities,knots,connections | Early `rau`, `repurpose` in legacy mesh |
| `d71b13fd` | 2026-05-11 | added types and concrete edges | `software_bim` tooling edges |
| `15222140` | 2026-05-13 | migration ready | Bulk neo4j batch migration; `prog_*`, `stadt_zuerich`, most `TEIL_VON_PROGRAMM` |
| `ada4dd86` | 2026-05-14 | person/project3 | `tomas` actor-registry stub |
| `323cd19b` | 2026-06-05 | 4 | Regulation vocab Phase B docs (exclusion proof) |
| `ed1d81d9` | 2026-06-06 | 5 | CH reuse-bubble v2 — orphan CH actors |

---

## 6. Outputs

- **`ledger/provenance_g05.csv`** — 33 rows, one per `SCHEMA_VIOLATION` element: `g05_id`, `claim_id`, violation class, origin pipeline, git first-commit metadata, current repo file pointers.
- **`reports/provenance_g05.md`** — this report.
