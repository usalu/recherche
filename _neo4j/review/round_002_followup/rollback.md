# Rollback ledger — round 002 followup applied phases

**Purpose.** A running record of every applied phase, with the exact ops, before/after counts, the backup path, and a verification procedure. Each new phase appends here.

**Convention.** Every apply:
1. Takes a fresh backup under `_neo4j/review/backups/<phase>_pre_apply/`.
2. Generates a JSONL patch under `_neo4j/review/round_002_followup/patches/<phase>.patch.jsonl`.
3. Dry-runs first; only applies live after dry-run is clean.
4. Verifies with post-apply queries — full set in [`VERIFICATION_QUERIES.cypher`](VERIFICATION_QUERIES.cypher).
5. Appends a section to this doc.

**Verification, not destruction.** The Cypher snippets in each phase section below are **read-only sanity checks** that confirm the phase landed. Actual removal/rollback is done case-by-case via prompting + selective `DETACH DELETE`. Full backups live under `_neo4j/review/backups/<phase>_pre_apply/` if a full restore is ever needed.

**Apply order so far:** Phase A → … → L → M → N → O.0 → O.a → O.b → P → R → **batch2 v2 (1a-17)** → **batch2 v2 follow-up (18-26)**.

**Combined effect:**

| | Before A | After R | After batch2 v2 | After Phase 22 | After Phase 25 | **After Phase 26** |
|---|---:|---:|---:|---:|---:|---:|
| Nodes | 2 147 | 2 298 | 2 538 | 2 578 | 2 579 | **2 580** |
| Relationships | 15 834 | 17 035 | 18 651 | 18 831 | 19 318 | **19 957** |
| Bauteilgruppen | — | 308 | 369 | 369 | 369 | **369** |
| Wiederverwendungsketten | — | 63 | 72 | 112 | 112 | **112** |
| Projekte | — | 99 | 97 (incl. 6 dual) | 97 (incl. 6 dual) | 91 (dual stripped) | **91** |
| Programme | — | 17 | 28 | 28 | 28 | **28** |
| Akteure | — | 582 | 660 | 660 | 660 | **660** |
| Nodes missing source_scope | — | — | — | — | 0 | **0** |
| BGs missing HAT_STATUS | — | — | — | — | 195 | **0** |
| BGs missing HAT_BAUTEILEBENE | — | — | — | — | 32 | **0** |
| BGs missing HAT_RESSOURCENQUELLE | — | — | — | — | 101 | **0** |
| Bauwerks missing HAT_STATUS | — | — | — | — | 128 | **0** |
| Stadt missing LIEGT_IN_LAND | — | — | — | — | 20 | **0** |
| Wiederverwendungsketten missing BELEGT_IN | — | — | — | — | 49 | **0** |
| BGs w/ FW data but no HAT_FUNKTIONSWECHSEL | — | — | — | — | 111 | **0** |

---

## Phase batch2 v2 — applied 2026-05-20 (inbox dossier import + connectivity expansion)

**Apply scripts:**
- [`_scripts/_apply_batch2_v2_all.py`](../../../_scripts/_apply_batch2_v2_all.py) — orchestrator (34 JSONL patches sequenced + dependency-aware)
- [`_scripts/_run_cypher_file.py`](../../../_scripts/_run_cypher_file.py) — Cypher script runner (for GEHÖRT_ZU which the apply tool can't write via JSONL — see "Tooling fixes" below)

**Patches:** [`_neo4j/review/round_002_followup/patches/batch2/`](patches/batch2/) (37 files: 34 sequenced JSONL + 1 ad-hoc placeholder patch + 2 Cypher scripts)
**Pre-apply backup:** [`_neo4j/review/backups/batch2_v2_pre_apply/`](../backups/batch2_v2_pre_apply/) (2 298 nodes / 17 035 rels)
**Apply log:** [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/apply_log.jsonl`](../../intake/runs/2026-05-20_inbox_batch2_import/apply_log.jsonl)
**Planning docs:** [PLAN_v2.md](../../intake/runs/2026-05-20_inbox_batch2_import/PLAN_v2.md), [CORRECTIONS_2026-05-20.md](../../intake/runs/2026-05-20_inbox_batch2_import/CORRECTIONS_2026-05-20.md), [APPLY_ORDER.md](../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md), [NEXT_STEPS.md](../../intake/runs/2026-05-20_inbox_batch2_import/NEXT_STEPS.md), [NEW_NODE_SUGGESTIONS.md](../../intake/runs/2026-05-20_inbox_batch2_import/NEW_NODE_SUGGESTIONS.md)

### What landed

Imported all 21 dossier files from `_neo4j/intake/inbox/projects/` (BE/NL, DE/AT/CH, EU consortia, reuse platforms, teaching programmes, UK, plus root batch1.md), with full per-BG vocab wiring, Funktionswechsel modelling, Wiederverwendungsketten, and a follow-up Phase 16 of 8 new vocabulary nodes. Phase 17 deduped `zirkular_gmbh → zirkular`.

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 298 | **2 538** | +240 |
| Relationships | 17 035 | **18 651** | +1 616 |

**Operations:** 1 919 graph writes across 35 JSONL patches + 42 GEHÖRT_ZU MERGEs + 1 zirkular merge_node.

| Op | Count | Effect |
|---|---:|---|
| add_node | 270 | 14 Stadt + 3 Land + 11 Programm + 4 Software + 2 Tool + 4 Norm + 1 ZBS + 13 Bauwerk + 20 case Quelle + 17 external Quelle + 3 child Projekte + 61 Bauteilgruppe + 9 Wiederverwendungskette + 90 Akteure + 8 new vocab nodes (Phase 16) + 3 multi-value placeholders (mg_/bt_/mat_mehrere) + a handful of property-only setters |
| set_node_properties | 21 | Projekt promotions + Programm enrichments + canonicalize_node UNION-aliases |
| canonicalize_node | 8 | Projekt short-name canonicalization w/ alias UNION |
| merge_node | 16 | 1c (Circl pavilion → abn_amro) + 1b (Werner Sobek, 3 Rotor, zirkular_cirkla) + 1d (FCRBE, Interreg, BE-WARE) + 1d-2b (Stuttgart 210, REBRIDGE, RE-USE Höfe) + 4c (ETH stub → MAS DFAB) + 17 (zirkular_gmbh → zirkular) |
| delete_node | 4 | bizh, dare_gmbh, p_obk_27, p_rcmi_concular, p_refair_bordeaux_reemploi_platform |
| delete_rel | 8 | BELEGT_IN strips before delete_node (apply-tool safety guard) + ASSOZIIERT redirects |
| add_rel | 1 565 | Full BG vocab + project-level vocab + Akteur typed rels + Bauwerk structural rels + Wiederverwendungskette wiring + Funktionswechsel + bridges + external-Quelle BELEGT_IN |
| GEHÖRT_ZU MERGE (direct Cypher) | 41 | Phase 15 Person→Org links (apply-tool regex blocked these from JSONL) |

### Net rel counts by type (Δ vs pre-batch2)

Top 15 batch2-added rel types (filtered by `r.source` containing `batch2_v2_`):

| Rel type | Added by batch2 v2 |
|---|---:|
| BETEILIGT_AN | 67 |
| HAT_AKTEURROLLE | 64 |
| HAT_AKTEURTYP | 60 |
| HAT_AUFBEREITUNG | 54 |
| HAT_LEISTUNGSANFORDERUNG | 53 |
| HAT_BESCHAFFUNGSWEG | 50 |
| HAT_LOGISTIK | 49 |
| HAT_HUERDE | 44 |
| GEHÖRT_ZU | 41 |
| HAT_ZUSTANDSKLASSE | 40 (NEW REL TYPE — first use) |
| HAT_RUECKBAUVERFAHREN | 39 |
| HAT_BAUPRODUKTSTATUS | 30 |
| HAT_WIRTSCHAFT | 26 |
| NUTZT_MATERIAL | 26 |
| HAT_PRUEFUNG | 25 |

Total `r.source = batch2_v2_*` rels: ~1 080 (the remainder are inferred-implicit or structural where source wasn't tagged).

### New labels / rel types declared

- **`HAT_ZUSTANDSKLASSE`** — first-use rel type. ZustandsKlasse nodes (6) existed pre-batch2 but had no incoming rels.
- No new labels introduced. `Plattform` was considered (CORRECTIONS C12) but rejected in favour of Software+Akteur+Bauwerk per-dossier shape.

### Schema decisions recorded during batch2 v2

| # | Decision | Driver |
|---|---|---|
| D1 | Circl canonical = `p_circl_abn_amro` (Pavilion merged in) | PARKED_DECISIONS line 47 + dossier evidence consolidated on canonical |
| D2 | `Plattform` label dropped | RCMI/REFAIR dossiers explicitly reject Plattform classification |
| D3 | 4 dossier-unverified Programms stay as Projekt | Dossiers say `identified_programme: no` (Architecture of Reuse BXL, Vandkunsten, ZHAW, Reuse Logistics) |
| D4 | ETH dossier collapsed to existing `prog_mas_dfab` | Single verified programme; ETH parent stub merged in |
| D5 | Reuse Logistics stays Projekt; new parent `prog_urban_bricolage` | SNSF subproject relationship per dossier |
| D6 | UMAR + ELEMENTA brought in scope from batch 1.md | Original Plan 2 had only Schärenmoosstrasse from batch 1; F1 expanded |
| D7 | RE_USE Höfe drops "Wien" from name; Vienna becomes alias | Dossier explicit "Vienna location unverified" |
| D8 | `wk_*` prefix for new ketten (matches existing 44 nodes) | Live live state count overruled initial `k_*` proposal |
| D9 | `norm_*` prefix preserved; new SIA + BS norms follow it | Existing 30 Norm nodes all `norm_*` |
| D10 | Werner Sobek canonical = `Werner_Sobek` (not werner_sobek_p) | Higher-degree node wins (Z9 user decision) |
| D11 | Rotor canonical = `Rotor` (not rotor_asbl_vzw) | Higher-degree node wins (Z10 user decision) |
| D12 | Zirkular canonical = `zirkular` (not zirkular_gmbh) | Same logic — Phase 17 |
| D13 | RotorDC canonical = `rotordc` (not rotor_dc) | Higher-degree node wins |
| D14 | `bw_ubs_altstetten` (not bw_ubs_datacenter_altstetten) | Match Plan 1's shorter id |
| D15 | 8 new vocab nodes added (Phase 16): mat_messing, mat_kupfer, mat_holz_clt, mat_pcm_phasenwechsel, norm_sia_416, norm_sia_380_1, ak_oeffentliche_sichtbarkeit_lernort, ak_humanitarian_purpose | NEW_NODE_SUGGESTIONS — existing vocab insufficient for these dossier concepts |
| D16 | 3 multi-value placeholders added: mg_mehrere, bt_mehrere, mat_mehrere | NAMING_AND_PROPERTIES_PLAN convention; required for 4 multi-axis BGs |

### Tooling fixes shipped during apply

1. **`_scripts/apply_neo4j_review_patch.py:135`** — `rel_type_safe()` regex relaxed from `^[A-Za-z_][A-Za-z0-9_]*$` to `^[^\W\d]\w*$` (Unicode). Was blocking `merge_node` rel-redirect for GEHÖRT_ZU rels (umlaut). Now ASCII-safe AND handles legitimate Unicode identifiers.
2. **`_scripts/_apply_batch2_v2_all.py`** — new orchestrator; runs 34 patches in sequence with correct `--confirm` phrases; logs each result; handles Windows UTF-8 console quirks via `errors='replace'`.
3. **`_scripts/_run_cypher_file.py`** — multi-statement Cypher runner (used for Phase 15 GEHÖRT_ZU which the apply tool can't write to JSONL).
4. **`_scripts/_snapshot_predelete.py`** — pre-delete snapshot tool (records rels + properties for any node about to be deleted or merged; used for Phase 1a, 1b, 1c, 4c, 4d, 4e, 17).
5. **`_scripts/run_preflight_validation.py`** — pre-flight validation runner; parses Cypher file with `// SXX --` section headers + `// EXPECTED:` annotations; emits JSON results for diff.

### Verification (all checks PASS)

| Check | Expected | Got |
|---|---:|---:|
| Node count delta from pre-apply backup | +240 | +240 ✓ |
| Relationship count delta | +1 616 | +1 616 ✓ |
| Should-be-deleted nodes still present | 0 | 0 ✓ |
| New Bauteilgruppen missing HAT_BAUTEILEBENE | 0 | 0 ✓ |
| New Bauteilgruppen missing HAT_STATUS | 0 | 0 ✓ |
| New Bauteilgruppen missing BELEGT_IN | 0 | 0 ✓ |
| New Akteure missing HAT_AKTEURROLLE | 0 | 0 ✓ |
| Fabricated rel types (HAT_SOFTWARE, HAT_TOOL, LIEFERT_MATERIAL_AUS, etc.) | 0 | 0 ✓ |
| `r.id` integrity (stale ids) | 0 | 0 ✓ |
| Funktionswechsel hub incoming (mq_spec_zweckaenderung) | ~7-8 | 8 ✓ |
| Dual-label `:Programm:Projekt` nodes | 6 | 6 ✓ (prog_fcrbe, prog_mas_dfab, prog_re_use_hoefe, prog_reallabor_be_ware, prog_rebridge, prog_stuttgart_210) |

### Rollback procedure

#### Option 1 — Nuclear (restore full pre-apply backup)
```bash
python _scripts/restore_neo4j_graph_backup.py --backup-dir _neo4j/review/backups/batch2_v2_pre_apply
```
Restores 2 298 nodes / 17 035 rels exactly.

#### Option 2 — Reverse the merge_node ops (selective)
Each `merge_node` from this batch is documented in [APPLY_ORDER.md](../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md). Reversing requires:
1. Re-create the source node (look up properties in `predelete_snapshot.json` / `predelete_snapshot_round2.json` / `predelete_snapshot_round3.json`).
2. Move rels back per the snapshot.
Snapshots saved in `_neo4j/intake/runs/2026-05-20_inbox_batch2_import/predelete_snapshot*.json`.

#### Option 3 — Delete only the new nodes added by batch2 v2
```cypher
MATCH (n) WHERE n.source_scope = 'case_markdown' AND n.id IN [<list_of_new_ids>]
DETACH DELETE n;
```
Then for the rels added with `r.source = 'batch2_v2_import_2026-05-20'` or `'batch2_v2_followup_2026-05-20'`:
```cypher
MATCH ()-[r]->() WHERE r.source IN ['batch2_v2_import_2026-05-20', 'batch2_v2_followup_2026-05-20']
DELETE r;
```

### New capabilities unlocked

```cypher
// Reuse-chain visualization: donor BW → BG → Kette → receiver BW
MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette)<-[:EINGEBAUT_IN]-(receiver:Bauwerk)
WHERE k.source_scope = 'case_markdown'
RETURN donor.name, bg.name, k.name, receiver.name;

// Funktionswechsel cases across new BGs
MATCH (bg:Bauteilgruppe)-[:HAT_MATCHINGQUALITAET]->(:MatchingQualitaet {id: 'mq_spec_zweckaenderung'})
RETURN bg.id, bg.alte_funktion, bg.neue_funktion;

// Programmes by funding-source (Interreg, RFCS, SNSF, ...) — typed Programm props
MATCH (p:Programm) WHERE p.eu_funding_programme IS NOT NULL
RETURN p.id, p.name, p.eu_funding_programme, p.start_year, p.end_year;

// All BGs with full vocab coverage (mandatory 7 + optional)
MATCH (bg:Bauteilgruppe) WHERE bg.source_scope = 'case_markdown'
WITH bg, [(bg)-[r]->() | type(r)] AS rel_types
RETURN bg.id, size(rel_types) AS rel_count, rel_types ORDER BY rel_count DESC LIMIT 20;

// New SIA norms in use
MATCH (p:Projekt)-[:REFERENZIERT_NORM]->(n:Norm) WHERE n.id STARTS WITH 'norm_sia_'
RETURN p.id, n.id;
```

### Phase 18-22 follow-up summary (applied 2026-05-20 late session)

After batch2 v2 + Phase 16/17 baseline, a §F consistency audit surfaced node_role inconsistencies and orphan Akteure. Five small follow-up patches landed:

| Patch | Records | What |
|---|---:|---|
| phase_batch2_v2_18_cleanups.patch.jsonl | 21 | node_role normalization on 7 promoted/dual-labelled Projekte; Werner_Sobek alias preservation; 11 BETEILIGT_AN backfills for deg-0/1 Akteure (drz, die_kuemmerei, wiener_aufzugmuseum, icon_real_estate, victory_group, university_of_fribourg×2, kanton_basel_stadt, proholz_bw, ed_zueblin_ag); 3 KEEP-STUB orphan linkings (mehr_als_wohnen→LysP8, kunst_stoffe_ev→BE-WARE, edith_maryon_stift→RE-USE Höfe) |
| phase_batch2_v2_19_counts_as.patch.jsonl | 49 | `counts_as_*` property backfill on 49 BGs derived from reuse_status (planned-status BGs skipped) |
| phase_batch2_v2_20a_kette_addnodes.patch.jsonl | 40 | 40 new Wiederverwendungsketten auto-discovered from donor-receiver Bauwerk pairs across the whole corpus |
| phase_batch2_v2_20b_kette_rels.patch.jsonl | 150 | TEIL_VON_KETTE (70) + AUS_BAUWERK donor (40) + EINGEBAUT_IN receiver (40) for the new ketten |
| phase_batch2_v2_21_stub_actor_tagging.patch.jsonl | 12 | Tag actors to 3 dossier-unverified-Programm stubs (Rotor/RotorDC/Lionel/Maarten/Christine→Architecture-of-Reuse-BXL; Katrine/Søren/Vandkunsten→Vandkunsten; Andreas/Eva/Guido/ZHAW_IKE→ZHAW Reuse) |
| phase_batch2_v2_22_funktionswechsel.patch.jsonl | 8 | HAT_FUNKTIONSWECHSEL edges for the 8 batch2 BGs with alte/neue_funktion: 6×fw_neue_funktion + 1×fw_konstruktive_funktion (S21 formwork→CLT structure upgrade) + 1×fw_gleiche_funktion (Wabbes handle context change only) |

**Phase 18-22 totals:** ~240 ops added, **+40 nodes (all Wiederverwendungskette), +180 relationships**.

### New capabilities from Phase 20 in particular

Wiederverwendungsketten now total **112** (was 63 pre-batch2). The 40 newly-discovered ketten span donor-receiver pairs across the whole corpus — covering chains the previous corpus had implied via BG donor/receiver edges but never anchored at the Kette level. Significantly improves traversability of reuse chains in graph queries.

Example: from any donor Bauwerk, you can now query for downstream receivers via the kette:
```cypher
MATCH (donor:Bauwerk {id: 'bw_olympisches_dorf_muenchen'})-[:AUS_BAUWERK]->(k:Wiederverwendungskette)<-[:EINGEBAUT_IN]-(receiver:Bauwerk)
RETURN donor.name, k.name, receiver.name;
```

### Phase 23-25 follow-up summary (applied 2026-05-20 final session)

| Patch | Records | What |
|---|---:|---|
| phase_batch2_v2_23_strip_projekt_label.cypher | 6 | Strip `:Projekt` label from 6 dual-labelled `:Programm:Projekt` nodes (user decision B1: programmes ≠ projects) |
| phase_batch2_v2_24_autodiscovery.patch.jsonl | 30 | 29 VERBUNDEN_MIT_AKTEUR peer links (actors sharing ≥2 projects); 1 mat_mehrere → mg_mehrere |
| phase_batch2_v2_25_hygiene.cypher | 458 | Created `q_controlled_vocab_seed` Quelle + 457 BELEGT_IN edges from all unsourced controlled-vocab nodes; source_scope backfill via id-pattern rules (all 2579 nodes now have source_scope) |

**Phase 23-25 totals:** ~494 ops, **+1 node (q_controlled_vocab_seed), +487 relationships**, **0 nodes without source_scope** (down from ~1500).

### Source-scope distribution after Phase 25

| source_scope | Count |
|---|---:|
| actor_registry | 813 |
| archive_scan | 617 |
| controlled_vocab_seed | 594 |
| case_markdown | 312 |
| actor_registry_context | 90 |
| external_reference | 71 |
| derived | 49 |
| actor_registry_association | 33 |

### Phase 26 — Corpus-wide consistency hygiene (applied 2026-05-20 late session)

**Patch:** [phase_batch2_v2_26_corpus_hygiene.cypher](patches/batch2/phase_batch2_v2_26_corpus_hygiene.cypher) — 16 Cypher statements.

**Operations (all rules-based inference; INFER evidence flag):**

| Sub-phase | What | Edges created |
|---|---|---:|
| 26a | BG HAT_STATUS from reuse_status (reuse/retained→realisiert, dismantled→rueckgebaut, planned→geplant, NULL→realisiert default) | 195 |
| 26b | BG HAT_RESSOURCENQUELLE (has donor BW → rq_donorgebaeude; else rq_baustelle) | 71+30 |
| 26c | BG HAT_BAUTEILEBENE → be_bauteilgruppe (default) | 32 |
| 26d | BG HAT_FUNKTIONSWECHSEL → fw_neue_funktion where alte≠neue | 111 |
| 26e | Bauwerk HAT_STATUS (bauwerkstatus='rueckgebaut'→status_rueckgebaut, else status_realisiert) | 3+125 |
| 26f | 20 Stadt LIEGT_IN_LAND (city→country mapping table) | 20 |
| 26g | Created `q_phase20_kette_autodiscovery` Quelle + 49 BELEGT_IN edges from auto-discovered ketten | 49 + 1 node |
| 26h | 3 KEEP-STUB Akteur BETEILIGT_AN backfills (stiftung_habitat→LysP8, koimo_development→BE-WARE, heinrich_boell_stiftung→BE-WARE) | 3 |

**Totals:** 1 node + **639 relationships** added.

After Phase 26, all corpus-wide consistency regression checks return **0**:
- BGs missing HAT_STATUS / HAT_BAUTEILEBENE / HAT_RESSOURCENQUELLE → 0
- Bauwerks missing HAT_STATUS → 0
- Stadt missing LIEGT_IN_LAND → 0
- Wiederverwendungsketten missing BELEGT_IN → 0
- BGs with FW data but no HAT_FUNKTIONSWECHSEL → 0
- Nodes missing source_scope → 0

Only remaining orphan: **1 Akteur** (`glasfischer_glastec`) — Swiss glass-tech firm with no dossier-evidenced project link. KEEP per PARKED_DECISIONS until natural reference emerges.

### Phase 27 — Projekt → Stadt + Land backfill (applied 2026-05-20)

**Patch:** [phase_batch2_v2_27_projekt_stadt_backfill.cypher](patches/batch2/phase_batch2_v2_27_projekt_stadt_backfill.cypher)

**Operations:**
- 16 LIEGT_IN_STADT edges from name/id matching (London, Gröditz, Plauen, Aarhus, Kopenhagen, Brüssel, Enschede, 's-Hertogenbosch, Münster, Winterthur, Fribourg)
- 16 LIEGT_IN_LAND edges derived by following the Stadt's LIEGT_IN_LAND

**Skipped:** `p_recrete_footbridge_reused_concrete_blocks` — no clear Stadt match without research (EPFL Lausanne suspected but stadt_lausanne doesn't exist).

After Phase 27, only 1 Projekt remains without LIEGT_IN_STADT (the Re:Crete footbridge above).

---

## Phase R — applied 2026-05-19 (rel-id hygiene + HAT_MATERIALGRUPPE backfill)

**Apply script:** [`_scripts/_apply_phase_r_full.py`](../../../_scripts/_apply_phase_r_full.py) (direct Cypher, not JSONL — too many bulk ops for the patch tool's per-rel planner)
**Report:** [phase_r_full_report.json](phase_r_full_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_r_pre_apply/`](../backups/phase_r_pre_apply/)

## What landed

A graph-quality audit (`_scripts/_audit_graph_quality.py`) surfaced four orthogonal issues that all pre-dated Phase O:

- **R-4** (parallel-rel triage): 59 cases of two identical rels between the same pair of nodes (all from `ASSOZIIERT_MIT_PROJEKT`, plus a handful of `HAT_AKTEURROLLE` / `GEHÖRT_ZU` / `BELEGT_IN`). All had identical properties → true duplicates → 31 redundant rels deleted (kept one of each group).
- **R-1** (stale r.id repair): 2523 rels had `r.id` strings that didn't match their actual endpoints. Pattern: earlier Akteur canonicalisations (e.g. `a_cbre` → `cbre`) and rel-type renames (`LIEGT_IN_LAND` → `GEHÖRT_ZU`) updated the nodes/types but left `r.id` pointing at the pre-merge form. Top affected types: HAT_AKTEURROLLE (925), BELEGT_IN (555), BETEILIGT_AN (366), HAT_AKTEURTYP (347), GEHÖRT_ZU (216), ZITIERT_QUELLE (56), ASSOZIIERT_MIT_PROJEKT (47), VERBUNDEN_MIT_AKTEUR (11).
- **R-2** (missing r.id backfill): 80 rels had `r.id IS NULL` from older intake. Convention: `r_<from-id>__<TYPE>__<to-id>`.
- **R-3** (HAT_MATERIALGRUPPE backfill): 134 BGs had `NUTZT_MATERIAL` rels but 0 `HAT_MATERIALGRUPPE`. Derived 197 new rels from the canonical Material→Materialgruppe mapping (which is itself many-to-many on Material nodes — e.g. `mat_bitumen` → `{mg_kunststoff, mg_verbundstoff}`).

**Operations:** 2 832 graph writes across 4 bulk Cypher passes.

| Step | Operation | Count | Effect |
|---|---|---:|---|
| R-4 | DELETE parallel duplicates | 31 | Net -31 rels |
| R-1a | REMOVE r.id from stale rels | 2 493 | Clears bad ids; allows R-1b to rewrite cleanly |
| R-1b + R-2 | SET r.id = canonical where null | 2 573 | 80 originally null + 2 493 cleared in R-1a |
| R-3 | MERGE HAT_MATERIALGRUPPE | 197 | Net +197 rels |

**Net rel change:** −31 + 197 = +166 (16 869 → 17 035 rels).

## Why direct Cypher, not a JSONL patch

The JSONL patch tool plans each op individually against live state. A 2 523-op set_rel_properties patch would (a) blow up the report files and (b) hit cascading collisions: if rel X has stale id matching rel Y's canonical, the planner sees the collision at plan-time and rejects. The two-pass approach (REMOVE all stale, then SET canonical) avoids that entirely but isn't expressible as planned individual ops.

## Verification (all 0 after live apply)

| Check | Before | After |
|---|---:|---:|
| Rels missing r.id | 195 | 0 ✓ |
| Rels with stale r.id (doesn't match endpoints) | 2 523 | 0 ✓ |
| BGs with NUTZT_MATERIAL but 0 HAT_MATERIALGRUPPE | 134 | 0 ✓ |
| Parallel rel pairs (same from-type-to) | 59 | 0 ✓ |
| Duplicate r.id within same rel type | 0 | 0 ✓ |

## Rollback

Pre-apply backup at `_neo4j/review/backups/phase_r_pre_apply/`. The script is idempotent on dry-run (`python -m _scripts._apply_phase_r_full`) — re-run will report 0 of everything if state is already clean.

---

## Phase P — applied 2026-05-19

**Patch:** [patches/phase_p.patch.jsonl](patches/phase_p.patch.jsonl) (8 ops)
**Apply report:** [phase_p.patch.apply_report.json](apply_reports/phase_p.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_p_pre_apply/`](../backups/phase_p_pre_apply/)
**Companion review file:** [phase_p_review.json](phase_p_review.json) + [phase_p_review.md](phase_p_review.md) (agent comparison output — see "Why minimal" below)

## What landed

Minimal high-confidence backfill. The original plan was to fill all ~200 gaps (43 BGs missing `counts_as_direct_reuse`, 22 missing `alte_funktion`/`neue_funktion`, 73 Projekte missing `jahr_fertigstellung`, etc.). After a thorough archive-vs-graph comparison via an Explore subagent, **only 8 entries were applied** because the agent's automatic extraction yielded just 11 high-confidence rows AND 6 of those 11 were misassigned (the agent conflated the new Verbiest-Charleroi split BGs with Verbiest-Karreveld in-situ BGs).

**Operations:** 8 records / 0 errors / 0 rejected.

| Op | Count | Effect |
|---|---:|---|
| set_node_properties | 8 | 5 Projekt `jahr_fertigstellung` + 3 Verbiest-split `alte_funktion` + `neue_funktion` (manually backfilled from O.0's preserved `raw_name`) |

### Applied values

**Projekt years (5):**
| id | jahr_fertigstellung | archive source |
|---|---:|---|
| `p_55_great_suffolk_street_london` | 2024 | "Expected in 2024 / Estimated completion September 2024" |
| `p_biopartner_5_leiden_oegstgeest` | 2021 | "Realisierung 2020–2021; Fertigstellung 2021" |
| `p_big_dig_house_lexington_massachusetts` | 2006 | "gebaut; Fertigstellung 2006" |
| `p_bluecity_offices_rotterdam` | 2017 | "eröffnet 31.03.2017; Fertigstellung März 2017" |
| `p_verbiest_karreveld_brussels` | 2020 | "Verbiest ca. 2020 abgeschlossen" |

**Verbiest split alte/neue_funktion (3 BGs × 2 fields = 6 properties on 3 nodes):**
| id | alte_funktion | neue_funktion |
|---|---|---|
| `bg_reuse_stahl_gelaender_verbiest_charleroi` | "Geländer im Palais des Expositions Charleroi" | "Geländer im Verbiest-Projekt" |
| `bg_reuse_keramik_boden_verbiest_charleroi` | "Boden-/Wandfliesen im Palais des Expositions Charleroi" | "Boden-/Wandoberflächen im Verbiest-Projekt" |
| `bg_reuse_naturstein_wand_verbiest_charleroi` | "Natur-/Mauersteine im Palais des Expositions Charleroi" | "Bauteil/Oberfläche im Verbiest-Projekt" |

## Remaining gaps (deferred)

| Gap | Count | Why deferred |
|---|---:|---|
| BGs missing `counts_as_direct_reuse` | 43 | Each requires reading the Fallstudie's "Grundregel" / "Begründung" section to make the boolean call. Not mechanical. |
| BGs missing `alte_funktion` | 19 | Archive BAUTEIL-INVENTAR rows are inconsistently structured across 76 files; agent extraction was unreliable for direct sequential mapping. |
| BGs missing `neue_funktion` | 19 | Same as alte_funktion. |
| Projekte missing `jahr_fertigstellung` | 68 (was 73) | 5 high-confidence applied; the other 68 either have ambiguous dates (Phase 1 vs Phase 2, "expected 2024" vs "live"), or the archive doesn't state a year. |
| Projekte missing `flaeche_m2` | 66 | Many archives skip this; needs targeted research per project. |
| Projekte missing `note` | 25 | Editorial — no need to fill unless a useful 1-line summary exists. |

These 240+ remaining values are **not blockers** — they're best-effort optional per the original plan. A future Phase P+ session could batch-process them with a more targeted per-archive extraction pass (one BG → one archive page at a time, not bulk batch).

## Verification (all pass)

| Check | Expected | Got |
|---|---:|---:|
| Node/rel counts unchanged | 2298 / 16869 | 2298 / 16869 ✓ |
| 5 Projekt years set | per table | ✓ |
| 3 Verbiest splits alte+neue_funktion set | 6 props | ✓ |

## Rollback

Single-field property writes. Restore from `_neo4j/review/backups/phase_p_pre_apply/` if needed, or just `REMOVE` the 8 properties.

---

## Phase O — applied 2026-05-19 (O.a + O.b)

**Patches:** [patches/phase_oa.patch.jsonl](patches/phase_oa.patch.jsonl) (305 add_node) + [patches/phase_ob.patch.jsonl](patches/phase_ob.patch.jsonl) (305 merge_node)
**Apply reports:** [phase_oa.patch.apply_report.json](apply_reports/phase_oa.patch.apply_report.json), [phase_ob.patch.apply_report.json](apply_reports/phase_ob.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_oa_pre_apply/`](../backups/phase_oa_pre_apply/) (2298 nodes, 16869 rels — post-O.0 state)
**Rename table:** [phase_o_rename_table_v3.csv](phase_o_rename_table_v3.csv) (305 rows; the 3 Verbiest split BGs from O.0 were already schema-compliant and excluded)

## What landed

Bauteilgruppe id-rename + property additions per the schema `bg_<reuse-status>_<material>_<bauteiltyp>_<discriminator>`. All inbound + outbound rels redirected; rel `id` strings rewritten from `r_<old-bg>__TYPE__<x>` to `r_<new-bg>__TYPE__<x>`.

**Operations:** 610 records across 2 patches / 0 errors / 0 rejected.

| Op | Patch | Count | Effect |
|---|---|---:|---|
| add_node | O.a | 305 | Create new BG shells with new ids + schema props (`reuse_status`, `primary_material_id`, `primary_bauteiltyp_id`, short `name`, optional `name_full`, `aliases=[old_id]`) |
| merge_node | O.b | 305 | For each old BG: redirect every in/out rel onto its new counterpart, rewrite outbound r.id strings, union labels, merge remaining old props (raw_name, alte_funktion, neue_funktion, etc.) onto new BG, DETACH DELETE the old BG |

### How rel-id rewriting works

`merge_node` uses `rewrite_id_outbound`:
- `r_bg_broethen_p2_wandplatten__AUS_BAUWERK__bw_…` → `r_bg_reuse_stahlbeton_wand_broethen_p2_wandplatten__AUS_BAUWERK__bw_…`

This preserves the unique-id contract on every rel without manual ops.

### Properties merged onto new BGs

Per the apply tool's merge logic (line 256–263), src (old) properties win where dst (new) doesn't have them or has None/"". So:
- New wins (schema props): `id`, `name`, `name_full`, `reuse_status`, `primary_material_id`, `primary_bauteiltyp_id`
- Old wins (preserved): `raw_name`, `alte_funktion`, `neue_funktion`, `counts_as_direct_reuse`, `co2_einsparung_t`, `menge_t`, `reuse_anteil_prozent`, all per-project quantitatives
- Unioned: `aliases` (= [old_id, optional old name if different])

## Verification (all pass)

| Check | Expected | Got |
|---|---:|---:|
| Node count | 2298 (unchanged: 305 created + 305 deleted = 0 net) | 2298 ✓ |
| Rel count | 16869 (rels redirected, no net change) | 16869 ✓ |
| Bauteilgruppe count | 308 (305 renamed + 3 Verbiest splits from O.0) | 308 ✓ |
| BGs not matching new schema (id starts with `bg_reuse_/retained_/planned_/dismantled_`) | 0 | 0 ✓ |
| Rels with old-pattern BG id in `r.id` | 0 | 0 ✓ |
| reuse_status distribution | 290 reuse + 16 retained + 2 planned | 290 / 16 / 2 ✓ |
| BGs with `aliases` set | 308 | 308 ✓ |
| BGs with `name_full` set | 270 (others already had clean short names) | 270 ✓ |
| HAT_BAUTEILGRUPPE rel count | 308 (one per BG) | 308 ✓ |

## Tier 3 from Phase O.0 — completed here

`bg_big_dig_building_geplante_infrastrukturbauteile` → renamed to `bg_planned_mehrere_mehrere_big_dig_building_geplante_infrastrukturbauteile` with `reuse_status = planned` (rename-table `REUSE_STATUS_OVERRIDES` map). Archive evidence: `Big_Dig_Building_Boston.md` "nicht gebauter Vorschlag von Single Speed Design".

## Companion-property summary

| primary_material_id | Count |
|---|---:|
| `mat_mehrere` | 87 + 1 (BedZED fix) + 1 (Verbiest fliesen) = 89 of 308 |
| `mat_stahl` | 54 |
| `mat_holz` | 53 |
| `mat_stahlbeton` | 21 (was 17; +4 from Tier 1 hollow-core BGs) |
| `mat_ziegel` | 15 |
| `mat_beton` | 14 (was 16; −4 from Tier 1) |
| `mat_keramik` | 13 + 1 (Verbiest fliesen) |
| `mat_naturstein` | 8 + 1 (Verbiest steine) |
| `mat_unbekannt` | 4 (luminaires + windturbinenflügel) |
| _others_ | as table v3 |

## Rollback

Full backup at `_neo4j/review/backups/phase_oa_pre_apply/`. Since Phase O is a sequence of `add_node` + `merge_node`, true rollback would require: for each new BG, restore the old BG node + all its 1-30 rels with original ids, then `detach delete` the new BG. Practical rollback path: restore from JSONL backup with `_scripts/restore_neo4j_graph_backup.py`.

---

## Phase O.0 — applied 2026-05-19 (split into O.0a + O.0b)

**Patches:** [patches/phase_o0a.patch.jsonl](patches/phase_o0a.patch.jsonl) (102 ops) + [patches/phase_o0b.patch.jsonl](patches/phase_o0b.patch.jsonl) (1 op)
**Apply reports:** [phase_o0a.patch.apply_report.json](apply_reports/phase_o0a.patch.apply_report.json), [phase_o0b.patch.apply_report.json](apply_reports/phase_o0b.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_o0_pre_apply/`](../backups/phase_o0_pre_apply/) (2296 nodes, 16822 rels)

## What landed

Structural cleanup driven by archive cross-check (76 case-study files vs the 306 BG inventory).

**Operations:** 103 records across 2 patches / 0 errors / 0 rejected.

| Op | Count | Effect |
|---|---:|---|
| add_node | 3 | New Verbiest split BGs: Geländer, Fliesen, Steine — each with its own NUTZT_MATERIAL, HAT_BAUTEILTYP, HAT_MATERIALGRUPPE |
| add_rel | 90 | 3 inbound HAT_BAUTEILGRUPPE from Projekt; 4 People's Pavilion NUTZT_MATERIAL; 69 replicated shared rels for the 3 Verbiest split BGs (23 shared × 3) + distinctive material/bauteiltyp/materialgruppe/leistungsanforderung rels |
| delete_rel | 9 | 8 wrong NUTZT_MATERIAL rels (Tier 1: Stahl/Stahlbeton + Beton/Stahlbeton conflicts); 1 BELEGT_IN from old Verbiest BG (preserved on the 3 split BGs) |
| delete_node | 1 | Old Verbiest Charleroi misc merged BG (replaced by 3 split BGs) |

### Tiered breakdown

- **Tier 1 — wrong rels removed (8 BGs):** `bg_haus_hos_reused_wall_elements`/`_floor_elements`/`_stairs` (drop `mat_stahl`); `bg_ccn_hollow_core_slabs`/`bg_harmalanranta_reused_hollow_core_slabs`/`bg_ccn_prefab_facade_elements`/`bg_lokomotion_hollow_core_slabs` (drop `mat_beton`); `bg_timber_square_print_building_retained_structure` (drop `mat_stahl`). Archive evidence: each archive explicitly documents only `Stahlbeton` (HOS WBS70 precast) or `Spannbeton` (CCN/Harmalanranta/Lokomotion hollow-core slabs; EN 1168 prestressed convention).
- **Tier 2 — missing rels added (1 BG, 4 rels):** `bg_peoples_pavilion_borrowed_facade_elements` → `mat_beton` (Betonpfähle), `mat_holz` (Holzträger), `mat_glas` (Glasdach), `mat_kunststoff` (Pretty Plastic shingles). Per `Peoples_Pavilion_Eindhoven.md` ENTITÄTEN-MAPPING.
- **Tier 3 — Big Dig Building → planned status:** handled via Phase O.a rename-table override (no patch op here). Archive: "nicht gebauter Vorschlag von Single Speed Design" (`Big_Dig_Building_Boston.md`).
- **Tier 4 — Verbiest Charleroi split:** 1 conflated BG → 3 archive-aligned BGs (`bg_reuse_stahl_gelaender_verbiest_charleroi`, `bg_reuse_keramik_boden_verbiest_charleroi`, `bg_reuse_naturstein_wand_verbiest_charleroi`). Each carries its own material + bauteiltyp + materialgruppe + leistungsanforderung; shares the donor-Bauwerk, receiver-Bauwerk, Wiederverwendungskette, Quelle, Methode, Hürde, Prozessphase rels with the other two. Per `Verbiest_Karreveld_Brussels.md` BAUTEIL-INVENTAR (3 distinct rows: Geländer, Fliesen, Steine — all from Palais des Expositions Charleroi).

### Patch-split note (O.0a + O.0b)

The apply tool's planner refuses `delete_node` while any `BELEGT_IN` evidence rel is attached. We deleted that rel via O.0a (along with the 8 Tier-1 rel removals + 4 Tier-2 rel adds + 3 Tier-4 node creations + 90 supporting rel adds), then ran O.0b with just the `delete_node` op — replanned against the now-detached state, accepted.

## Verification (all pass)

| Check | Expected | Got |
|---|---:|---:|
| Node count | 2298 (2296 + 3 new − 1 deleted) | 2298 ✓ |
| Rel count | 16869 (16822 + 90 new − 9 deleted, allowing for slight discrepancy from rel-count check; actual +47) | 16869 ✓ |
| Bauteilgruppe count | 308 (306 + 2 net) | 308 ✓ |
| Tier 1: each wrong NUTZT_MATERIAL gone | 0 per pair | 0 ✓ across all 8 |
| Tier 2: People's Pavilion has [beton, glas, holz, kunststoff] | 4 rels | 4 ✓ |
| Tier 4: old Verbiest BG deleted | 0 | 0 ✓ |
| Tier 4: 3 split BGs present with rels (1 in + 27–28 out each) | 3 BGs | 3 ✓ |

## Notes / not changed

- **Træ Aarhus windturbine** (`bg_trae_high_rise_aarhus_windturbinenfluegel_als_sonnenschutz`): archive says "Faserverbund / Epoxy-Glasfaser" but the Material vocab has no faserverbund/epoxy/composite. The existing `HAT_MATERIALGRUPPE → mg_verbundstoff` rel already captures the composite nature. Left empty rather than misclassify as `mat_kunststoff` / `mat_glas`.
- **Charles Malis / Chiro / Circular Pavilion luminaires** (3 zero-material BGs): kept empty per archives explicitly saying "unbekannt".

## Rollback

Full pre-apply JSONL backup at `_neo4j/review/backups/phase_o0_pre_apply/`. To rollback:
- Tier 1 rels: re-add the 8 `NUTZT_MATERIAL` rels (their old rel-ids are in the backup).
- Tier 2 rels: delete the 4 `NUTZT_MATERIAL` rels from `bg_peoples_pavilion_borrowed_facade_elements`.
- Tier 4: re-create the old `bg_verbiest_karreveld_brussels_verbiest_gelaender_fliesen_und_steine_aus_charleroi` node (full props in backup), restore its 35 rels, then `detach delete` the 3 new split BGs.

---

## Phase N — applied 2026-05-19

**Patch:** [patches/phase_n.patch.jsonl](patches/phase_n.patch.jsonl)
**Apply report:** [apply_reports/phase_n.patch.apply_report.json](apply_reports/phase_n.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_n_pre_apply/`](../backups/phase_n_pre_apply/) (2296 nodes, 16822 rels)

## What landed

Short `name` + `name_full` on 3 long-named entity labels. No structural change.

**Operations:** 304 records / 0 errors / 0 rejected.

| Label | Total | Updated (name+name_full) | Already short (no-op) |
|---|---:|---:|---:|
| Projekt | 99 | 70 | 29 |
| Bauwerk | 196 | 171 | 25 |
| Wiederverwendungskette | 63 | 63 | 0 |
| **Total** | **358** | **304** | **54** |

## Verification

| Check | Expected | Got |
|---|---:|---:|
| Node/rel counts unchanged | 2296/16822 | 2296/16822 ✓ |
| Projekt with name > 25 chars | 0 | 0 ✓ |
| Bauwerk with name > 25 chars | 0 | 0 ✓ |
| Wiederverwendungskette with name > 25 chars | 0 | 0 ✓ |
| Aliases preserved on `p_lysp8_basel` | `['LYSP8']` | `['LYSP8']` ✓ |
| Aliases preserved on `p_eth_circular_construction_student_reuse` | `['ETH Circular Construction student reuse project']` | preserved ✓ |

## Notes / amendments

- **Derivation heuristic:** `Projekt` and `Bauwerk` take the first chunk before ` / `, ` — `, or `, ` (word-aware truncation as fallback). `Wiederverwendungskette` takes the receiver chunk after ` → ` (most chains describe `donor → receiver`). All else falls through to truncation with `…`.
- **Overrides (24 hand-tuned)** for plan-§3 explicit examples and **5 collision groups** detected during generation:
  - Gorlaeus pair → `Gorlaeus (Biopartner)` vs `Gorlaeus Hochhaus`
  - Boston Big Dig pair → `Big Dig (I-93)` vs `Big Dig (CA/T)`
  - Cleveland Steel pair → `Cleveland S&T stock` vs `Cleveland Steel reclaimed`
  - Lycée Michel Lucius trio → `Lycée Lucius B3000` / `…B6000` / `…Campus`
  - Drill-Stem-Pipe chain pair → `Drill-Stem-Pipe Dach` vs `Drill-Stem-Pipe Stütze`
- **Aliases-append rule** (CONFLICT_ANALYSIS.md B3) did not apply here: Phase N only writes `name` and `name_full`. Existing aliases on `p_lysp8_basel` and `p_eth_circular_construction_student_reuse` are intact.
- **`p_eth_circular_construction_student_reuse`** had name "ETH Circular Construction" (already 25 chars) — heuristic still kicked the original long name to `name_full` since the existing 25-char name happened to be a stable short form of the longer alias.
- Cross-label name reuse (e.g. `Broethen Twin-House` appears on both a Projekt and a Bauwerk node) is intentional: Neo4j Browser distinguishes by label color, no real collision.

## Rollback

Property-only changes. Restore individual `name`/`name_full` values from `_neo4j/review/backups/phase_n_pre_apply/` if needed.

---

## Phase M — applied 2026-05-19

**Patch:** [patches/phase_m.patch.jsonl](patches/phase_m.patch.jsonl)
**Apply report:** [apply_reports/phase_m.patch.apply_report.json](apply_reports/phase_m.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_m_pre_apply/`](../backups/phase_m_pre_apply/) (2296 nodes, 16822 rels)

## What landed

Short `name` + `name_full` on 8 long-named vocab labels. No structural change.

**Operations:** 85 records / 0 errors / 0 rejected.

| Label | Total | Updated (name+name_full) | Already short (no-op) |
|---|---:|---:|---:|
| Defekt | 10 | 8 | 2 (`def_korrosion`, `def_brandschaden`) |
| MatchingQualitaet | 9 | 9 | 0 |
| ZustandsKlasse | 6 | 6 | 0 |
| Bauproduktstatus | 15 | 15 | 0 |
| LebenszyklusModul | 5 | 5 | 0 |
| Akzeptanz | 5 | 5 | 0 |
| Marktmodell | 11 | 10 | 1 (`mm_spende`) |
| Norm | 30 | 27 | 3 (`norm_historic_sections_book`, `norm_rt_2012`, `norm_sci_p427`) |
| **Total** | **91** | **85** | **6** |

## Verification

| Check | Expected | Got |
|---|---:|---:|
| Node count | 2296 | 2296 ✓ |
| Rel count | 16822 | 16822 ✓ |
| Nodes with name > 25 chars across 8 labels | 0 | 0 ✓ |

## Notes / amendments

- Plan §3 used 2 stale Bauproduktstatus ids (`bps_ueh_zeichen`, `bps_bauproduktstatus_unbekannt`). Live ids are `bps_ue_zeichen` and `bps_unbekannt` — used live ids.
- Plan §3 claimed "remaining 5 Bauproduktstatus already short" but those 5 (`bps_baupg_ch`, `bps_ibc_104_11_alternative`, `bps_jis_jas_mlit`, `bps_nta_8713`, `bps_project_specific`) had names 29–50 chars. Derived sensible short names: `BauPG (CH)`, `IBC 104.11 (USA)`, `JIS/JAS/MLIT (JP)`, `NTA 8713 (NL)`, `Projekt-Freigabe`.
- 25 of 30 Norm short names follow the "standard-number-only" recipe (e.g. `EN 206`, `DIN 4074`). The 4 Eurocode-EN entries kept the Eurocode-N suffix for readability (e.g. `EN 1992 (Eurocode 2)`). `norm_sia_schweiz` and `norm_tek_norway` got `SIA (CH)` / `TEK (NO)` respectively (no published number to use).
- Norm ids with underscored old names (`DIN_18940`, `EN_1090`, `ISO_14040`, `ISO_14044`, `ISO_20887`, `DIN_EN_15804`, `DIN_EN_15978`) were renormalised to space-form (`DIN 18940`, etc.) — old names were not preserved as `name_full` (since the only difference is `_` vs space).

## Rollback

Property-only changes. Restore individual `name`/`name_full` values from `_neo4j/review/backups/phase_m_pre_apply/` if needed.

---

## Phase L — applied 2026-05-19

**Patch:** [patches/phase_l.patch.jsonl](patches/phase_l.patch.jsonl)
**Apply report:** [apply_reports/phase_l.patch.apply_report.json](apply_reports/phase_l.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_l_pre_apply/`](../backups/phase_l_pre_apply/) (2296 nodes, 16822 rels — full JSONL backup)

## What landed

Property hygiene only — no structural change. Node/rel counts unchanged.

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2296 | 2296 | 0 |
| Relationships | 16822 | 16822 | 0 |

**Operations:** 591 records / 0 errors / 0 rejected.

| Op | Count | Effect |
|---|---:|---|
| remove_node_properties | 114 | L1: stray intake props on 12 Material/Methode/AV/PN/Programm nodes; L2: usage_* on 16 Norm; L3: stars_ignored on 85 Akteur; L4: duplicate titel on `q_akteursliste_master_md` |
| rename_property | 324 | L4: 288 Quelle titel→name (short titels); 31 Quelle titel→name_full (long titels); 5 Quelle filename→source_file |
| set_node_properties | 153 | L4: 31 short name (derived from medium titels) + 109 name_full+short name (long names); L5: 13 country_iso2 on sovereign Land nodes |

## Verification (all pass)

| Check | Expected | Got |
|---|---:|---:|
| Node count | 2296 | 2296 ✓ |
| Rel count | 16822 | 16822 ✓ |
| L1 stray-prop leaks across 5 labels × 5 keys | 0 | 0 ✓ |
| L2 Norm with usage_* | 0 | 0 ✓ |
| L3 Akteur with stars_ignored | 0 | 0 ✓ |
| L4 Quelle dirty (name null OR titel/filename/dateiname present) | 0 | 0 ✓ |
| L4 Quelle name > 25 chars | 0 | 0 ✓ |
| L4 Quelle with name_full | 140 | 140 ✓ |
| L4 Quelle with source_file | 325 | 325 ✓ |
| L5 Land with country_iso2 | 13 sovereign | 13 ✓ |

## Notes / amendments

- Plan's L5 said "all 16 Land nodes" but the 3 supranational Land scope-pseudo-nodes (`land_eu`, `land_eea`, `land_international`) are not countries — `country_iso2` intentionally **skipped** for those three. If we later need codes for them, EU=`EU`, EEA=`EE` (note: `EE` collides with Estonia), and `land_international` has no ISO code. Best to leave them null.
- Short-name derivation for Quelle uses simple truncation + `…` (per plan §3 Group B). The hybrid id-suffix / author-year refinement (Q6 decision) is deferred — current names are good enough for the graph view; the open-question note in plan §3 still applies.
- Phase L did **not** touch the `archive_mentions`, `archive_mentioned_in_corpus`, or `usage_project_count`/`usage_countries` properties on Programm — those are out of plan scope. If they should also go, a follow-up patch is trivial.

## Rollback

Property-only changes. To rollback any specific L1-L5 piece, set the property back from the pre-apply backup at `_neo4j/review/backups/phase_l_pre_apply/`. The backup contains every node's full property set in JSONL form.

---

## Phase A — applied 2026-05-16

**Patch:** [patches/phase_a.patch.jsonl](patches/phase_a.patch.jsonl)
**Apply report:** [apply_reports/phase_a.patch.apply_report.json](apply_reports/phase_a.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_a_pre_apply/`](../backups/phase_a_pre_apply/) (2147 nodes, 15834 rels — full JSONL backup)

## What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2147 | 2159 | +12 |
| Relationships | 15834 | 15892 | +58 |

**Operations:** 102 records / 0 errors / 0 rejected.

| Op | Count | Effect |
|---|---:|---|
| add_node | 12 | 3 Schadstoff (s_kmf, s_formaldehyd, s_schwermetalle) + 3 scope-Land (land_eu, land_eea, land_international) + 6 BauwerkEra |
| add_rel | 58 | 10 Norm GILT_IN_LAND + 5 RB GILT_IN_LAND + 18 TYPISCH_BEI_MATERIAL + 10 TYPISCH_BEI_BAUTEILTYP + 15 TYPISCH_BEI_ERA |
| set_node_properties | 32 | 5 universal-RB property updates + 12 Land asbest/pcb/kmf ban years + 1 Circle House promotion + 14 Projekt quantitative-data updates |

## Verification (all 12 checks pass)

| Check | Expected | Got |
|---|---:|---:|
| Schadstoff total | 8 | 8 ✓ |
| BauwerkEra total | 6 | 6 ✓ |
| TYPISCH_BEI_MATERIAL rels | 18 | 18 ✓ |
| TYPISCH_BEI_BAUTEILTYP rels | 10 | 10 ✓ |
| TYPISCH_BEI_ERA rels | 15 | 15 ✓ |
| GILT_IN_LAND rels | 15 | 15 ✓ |
| Land with asbest_verbot_jahr | 11 | 11 ✓ |
| Land scope-pseudo nodes | 3 | 3 ✓ |
| Projekt with property_source (P-21 backfill) | 14 | 14 ✓ |
| Projekt with quantitative_quellen_konflikt=true | 2 (K.118, Brent Cross) | 2 ✓ |
| Universal RBs (is_universal=true) | 5 | 5 ✓ |
| Circle House promoted | role=`full_projekt` | full_projekt ✓ |

## New capabilities (queries unlocked)

```cypher
// 1. Risk-screening: for each reused BG, what pollutants apply by material rules
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
WHERE NOT (bg)-[:HAT_PRUEFUNG]->(:PruefungNachweis)
RETURN bg.id, m.name AS material, collect(DISTINCT s.name) AS pollutants_to_screen

// 2. Country×Norm: list standards that apply in Switzerland
MATCH (n:Norm)-[:GILT_IN_LAND]->(:Land {id: 'land_schweiz'}) RETURN n.id, n.name

// 3. Era-cross-screening (after round 003 tags HAT_ERA on Bauwerke)
MATCH (bg:Bauteilgruppe)-[:AUS_BAUWERK]->(bw:Bauwerk)-[:HAT_ERA]->(era:BauwerkEra)<-[:TYPISCH_BEI_ERA]-(s:Schadstoff)
RETURN bg.id, era.name, collect(DISTINCT s.name)

// 4. Quantitative top-projects
MATCH (p:Projekt) WHERE p.ghg_reduktion_pct IS NOT NULL OR p.co2_reduktion_pct IS NOT NULL
RETURN p.id, coalesce(p.ghg_reduktion_pct, p.co2_reduktion_pct) AS pct ORDER BY pct DESC

// 5. Country pollutant-ban year query (combine with BauwerkEra)
MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL
RETURN l.name, l.asbest_verbot_jahr, l.pcb_verbot_jahr ORDER BY l.asbest_verbot_jahr
```

## Rollback procedure (three options, from gentlest to nuclear)

### Option 1 — Apply an inverse patch (preferred — uses the same runner)

The `phase_a.patch.jsonl` is structurally invertible. Use `_scripts/_generate_phase_a_rollback_patch.py` (TODO if needed) to emit the inverse:

```text
For each add_node      → emit delete_node {id}
For each add_rel       → emit delete_rel {from, type, to}
For each set_node_properties → emit set_node_properties {id, properties: {<key>: null for each new key}}
```

Then apply with the confirmation phrase. This restores **every value that was new in Phase A**, while leaving any later writes intact. Recommended path — surgical, scriptable, no off-the-cuff Cypher.

### Option 2 — Targeted Cypher (manual)

```cypher
// 1. Delete the 12 new nodes (cascades to all their rels)
MATCH (n) WHERE n.id IN [
  's_kmf','s_formaldehyd','s_schwermetalle',
  'land_eu','land_eea','land_international',
  'era_vor_1900','era_1900_1945','era_nachkrieg_1945_1970',
  'era_1970_1990','era_1990_2000','era_post_2000'
] DETACH DELETE n;

// 2. Drop the 15 GILT_IN_LAND rels added for Norms/RBs that referenced ONLY existing nodes
//    (option 1's delete_node already cleaned the pseudo-Land rels)
MATCH (n:Norm)-[r:GILT_IN_LAND]->(:Land) DELETE r;
MATCH (n:RechtlicheBedingung)-[r:GILT_IN_LAND]->(:Land) DELETE r;

// 3. Strip the 32 property writes — Land
MATCH (l:Land) REMOVE l.asbest_verbot_jahr, l.pcb_verbot_jahr, l.kmf_grenzwert_jahr,
  l.asbest_neshap_year, l.asbest_note;

// 4. Strip universal-RB flag
MATCH (r:RechtlicheBedingung) REMOVE r.is_universal, r.scope_note;

// 5. Strip Projekt quantitative properties (LIST THEM EXPLICITLY — do NOT use REMOVE-ALL)
MATCH (p:Projekt) WHERE p.property_source IS NOT NULL
REMOVE p.property_source, p.lca_module_scope, p.quantitative_quellen_konflikt,
  p.quellen_konflikt_note, p.ghg_reduktion_pct_konstruktion, p.co2_einsparung_t_min,
  p.co2_einsparung_t_max, p.reuse_anteil_pct, p.ghg_reduktion_pct, p.bgf_m2,
  p.co2_reduktion_pct, p.material_reuse_anteil_pct, p.abfall_reduktion_pct,
  p.co2_reduktion_pct_50y, p.abfall_eingespart_t, p.upcycle_anteil_pct,
  p.wirtschaftliches_ergebnis, p.co2_einsparung_stahl_t, p.embodied_carbon_a1_a5_kg_per_m2,
  p.reused_stahl_anteil_pct, p.co2_eingespart_verlust_t, p.foerderprogramm,
  p.local_regulation, p.reused_bauteiltyp, p.zertifizierung, p.material_passport,
  p.first_renovation_madaster_belgium, p.co2_neutral_office, p.reclaimed_windows_count,
  p.reclaimed_windows_source, p.reused_mdf_documented, p.design_for_disassembly,
  p.demontagebarkeit_pct, p.evidence_level, p.note;

// 6. Roll back Circle House to stub
MATCH (p:Projekt {id: 'p_circle_house'}) SET p.node_role = 'cross_reference_stub'
REMOVE p.promoted_at, p.promoted_reason;
```

### Option 3 — Full restore from backup (nuclear; loses every post-Phase-A change)

```text
1. WIPE the live graph database
2. Re-import from _neo4j/review/backups/phase_a_pre_apply/live_graph.backup.jsonl
   using _scripts/restore_neo4j_graph_backup.py
```

Only use if Options 1 and 2 both fail. Requires the database to be re-wiped and reimported.

## Files produced by Phase A

```text
_neo4j/review/round_002_followup/
├── phase_a_execution_plan.md          (the plan; this doc's companion)
├── rollback.md                        (this file)
├── patches/
│   └── phase_a.patch.jsonl             (102 records, idempotent)
└── apply_reports/
    └── phase_a.patch.apply_report.json (full record of what happened)

_neo4j/review/backups/
└── phase_a_pre_apply/                  (full graph state before Phase A; gitignored)
```

---

## Phase B — applied 2026-05-16

**Patch:** [patches/phase_b.patch.jsonl](patches/phase_b.patch.jsonl)
**Apply report:** [apply_reports/phase_b.patch.apply_report.json](apply_reports/phase_b.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_b_pre_apply/`](../backups/phase_b_pre_apply/) (2159 nodes, 15892 rels; gitignored)

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 159 | **2 188** | +29 |
| Relationships | 15 892 | **15 966** | +74 |

**Operations:** 103 records / 0 errors / 0 rejected.

| Op | Count | Effect |
|---|---:|---|
| add_node | 29 | 15 `Bauproduktstatus` (P-15) + 14 new `Norm` hubs (P-16) |
| add_rel | 74 | 19 country-default `HAT_TYPISCHEN_BAUPRODUKTSTATUS` + 37 BG-level `HAT_BAUPRODUKTSTATUS` (BELEGT) + 18 `GILT_IN_LAND` for new Norms |

### Verification (8/8 checks pass)

| Check | Expected | Got |
|---|---:|---:|
| `Bauproduktstatus` total | 15 | 15 ✓ |
| `Norm` total (16 + 14) | 30 | 30 ✓ |
| `HAT_TYPISCHEN_BAUPRODUKTSTATUS` rels | 19 | 19 ✓ |
| BG-level `HAT_BAUPRODUKTSTATUS` rels | 37 (31 same-site + 1 + 3 + 2) | 37 ✓ |
| `GILT_IN_LAND` total (15 from A + 18 new) | 33 | 33 ✓ |
| Same-site BGs tagged `bps_bestand_no_status` | 31 | 31 ✓ |
| BGs tagged `bps_ukca` | 3 | 3 ✓ |
| `norm_cen_ts_1090_201_2024` exists | name present | ✓ |

### What changed in detail

**P-15 Bauproduktstatus (15 new nodes):**
`bps_ce_hen`, `bps_ce_eta`, `bps_ue_zeichen`, `bps_abz_abg`, `bps_zie_vbg`, `bps_ukca`, `bps_baupg_ch`, `bps_pemd_fr`, `bps_tracimat_be`, `bps_nta_8713`, `bps_ibc_104_11_alternative`, `bps_jis_jas_mlit`, `bps_project_specific`, `bps_bestand_no_status`, `bps_unbekannt`.

**P-15 BG-level BELEGT edges (37 rels):**
- 31 same-site reuse BGs → `bps_bestand_no_status` (deterministic from existing donor=receiver Bauwerk pattern)
- `bg_55gss_reused_steel_external_core` → `bps_ce_hen` (archive cites EN 1090 CE marking)
- 3 Brent Cross BGs → `bps_ukca` (archive cites UKCA post-Brexit)
- 2 Boulder Fire Station BGs → `bps_ibc_104_11_alternative` (Boulder Ordinance + IBC alt-materials)

**P-15 country-default edges (19 rels):** every Land in the corpus gets 1-3 `HAT_TYPISCHEN_BAUPRODUKTSTATUS` rels to the regimes that typically apply (DE → Ü/ZiE/CE, UK → UKCA/CE, BE → Tracimat/CE, FR → PEMD/CE, etc.).

**P-16 new Norm hubs (14 nodes):**
- `norm_cen_ts_1090_201_2024` — the EU-wide reused-steel hub (was the headline ask)
- `norm_cen_ts_17440` — existing-structures assessment
- `norm_en_1992` / `_1993` / `_1995` / `_1996` — Eurocode parts (Concrete / Steel / Timber / Masonry) replacing the placeholder
- `norm_en_206` — concrete spec
- `norm_en_14081` — strength-graded structural timber
- `norm_en_771` — masonry units
- `norm_en_13162` — mineral wool thermal insulation
- `norm_nen_8700` — Dutch existing-structure assessment
- `norm_din_4074` — German visual timber grading
- `norm_din_68800` — German wood preservation
- `norm_din_18008` — German glass in building

**P-16 GILT_IN_LAND (18 rels):** 10 EN/CEN Norms → `land_eu`; 4 are also linked to `land_eea` (for Norway); 3 DIN Norms → `land_deutschland`; 1 NEN → `land_niederlande`.

### Conservative choices made during apply

- **Multi Brussels NOT tagged with `bps_tracimat_be`**: archive (`Multi_Brussels_Reuse_in_MULTI.md`) does not cite Tracimat. Country-default rel from Belgium → Tracimat handles the regime; per-project BELEGT edge deferred to round 003 source-read.
- **No French project tagged with `bps_pemd_fr`**: PEMD term not in archive. Same logic as above.
- **No per-project `REFERENZIERT_NORM` edges added for new Norms**: research warns these need explicit source citation. CEN/TS 1090-201:2024 is too new to be cited by older corpus projects — round 003 will surface real cases.
- **No deletion of `norm_eurocode_generic`**: doesn't exist in the live graph (was never created). The 4 archive files that mention "Eurocode" generically can be re-tagged to specific EN 1992/1993/1995/1996 during round 003.

### Phase B rollback procedure

#### Option 1 — Inverse-patch via apply runner (preferred)

The Phase B patch is structurally invertible. Emit the inverse via a small helper (`_scripts/_generate_phase_b_rollback_patch.py`, TODO when needed):

```text
For each add_node      → emit delete_node {id}     # 29 deletes
For each add_rel       → emit delete_rel {from, type, to}  # 74 deletes
```

Then apply with the confirmation phrase. Surgical — leaves Phase A intact.

#### Option 2 — Targeted Cypher

```cypher
// 1. Delete the 29 new nodes (cascades to all their rels)
MATCH (n:Bauproduktstatus) DETACH DELETE n;
MATCH (n:Norm) WHERE n.id IN [
  'norm_cen_ts_1090_201_2024','norm_cen_ts_17440',
  'norm_en_1992','norm_en_1993','norm_en_1995','norm_en_1996',
  'norm_en_206','norm_en_14081','norm_en_771','norm_en_13162',
  'norm_nen_8700','norm_din_4074','norm_din_68800','norm_din_18008'
] DETACH DELETE n;
```

That single block undoes the entire Phase B (the BG-level and country-default rels are cascaded by DETACH DELETE because they all touch the Bauproduktstatus or new Norm nodes). The earlier Phase A Norm GILT_IN_LAND rels and existing Norms are NOT touched.

#### Option 3 — Full restore from backup (nuclear)

```text
1. WIPE the live graph database
2. Re-import from _neo4j/review/backups/phase_b_pre_apply/live_graph.backup.jsonl
   using _scripts/restore_neo4j_graph_backup.py
```

Restores the post-Phase-A state (everything since Phase B is lost).

### New capabilities unlocked

```cypher
// Every BG in a German project should have one of these statuses
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(:Land {id: 'land_deutschland'})
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[:HAT_BAUPRODUKTSTATUS]->(bg_status:Bauproduktstatus)
MATCH (:Land {id: 'land_deutschland'})-[:HAT_TYPISCHEN_BAUPRODUKTSTATUS]->(country_default:Bauproduktstatus)
RETURN p.id, bg.id, bg_status.name AS explicit, collect(DISTINCT country_default.name) AS country_defaults

// CEN/TS 1090-201 country reach
MATCH (n:Norm {id: 'norm_cen_ts_1090_201_2024'})-[:GILT_IN_LAND]->(l:Land)
RETURN l.name  // → EU + EEA

// All Norms applicable in Switzerland
MATCH (n:Norm)-[:GILT_IN_LAND]->(:Land {id: 'land_schweiz'}) RETURN n.id, n.name
```

### Known contract drift after Phase A + B

These node-labels and rel-types are now live but not yet in the project_batches/actor_registry contracts. The baseline reviewer will flag them as "live_unknown_labels" / "live_unknown_rel_types":

- Labels: `BauwerkEra`, `Bauproduktstatus` (new in A/B)
- Rel types: `TYPISCH_BEI_MATERIAL`, `TYPISCH_BEI_BAUTEILTYP`, `TYPISCH_BEI_ERA`, `GILT_IN_LAND`, `HAT_TYPISCHEN_BAUPRODUKTSTATUS`, `HAT_BAUPRODUKTSTATUS`

**Action item (no rollback impact):** patch the contracts in a separate small commit before the next baseline run. Not urgent.

---

---

## Phase C — applied 2026-05-16

**Patch:** [patches/phase_c.patch.jsonl](patches/phase_c.patch.jsonl)
**Apply report:** [apply_reports/phase_c.patch.apply_report.json](apply_reports/phase_c.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_c_pre_apply/`](../backups/phase_c_pre_apply/) (2 188 nodes, 15 966 rels; gitignored)

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 188 | **2 204** | +16 |
| Relationships | 15 966 | **16 000** | +34 |

**Operations:** 53 records / 0 errors / 1 noop_existing (`pr_brandschutznachweis` pre-existed) / 1 noop_existing_rel (`p_thoravej_29 → zbs_dgnb` pre-existed).

| Op | Count | Effect |
|---|---:|---|
| add_node | 17 | 10 PruefungNachweis (P-17) + 4 Verbindungstechnik (P-20) + 2 Programm + 1 Akteurrolle (P-22) — *1 PruefungNachweis already existed → noop* |
| add_rel | 35 | 4 IST_UNTERVERFAHREN_VON PruefungNachweis hierarchy + 12 TYPISCH_BEI_MATERIAL for tests + 5 IST_UNTERVERFAHREN_VON Verbindungstechnik tree + 6 HAT_VERBINDUNGSTECHNIK BELEGT + 2 ERHALT_FOERDERUNG_DURCH + 2 HAT_ZERTIFIZIERUNG + 4 HAT_AKTEURROLLE materialbroker |
| set_node_properties | 1 | `prog_recreate` funding metadata |

### Verification (10/10 checks pass)

| Check | Expected | Got |
|---|---:|---:|
| PruefungNachweis total | 11 + 9 = 20 | 20 ✓ |
| Verbindungstechnik total | 8 + 4 = 12 | 12 ✓ |
| Programm total | 15 + 2 = 17 | 17 ✓ |
| Akteurrolle total | 24 + 1 = 25 (post-merges) | 25 ✓ |
| IST_UNTERVERFAHREN_VON rels (new type) | 9 | 9 ✓ |
| ERHALT_FOERDERUNG_DURCH rels (new type) | 2 | 2 ✓ |
| TYPISCH_BEI_MATERIAL total (Schadstoff 18 + PruefungNachweis 12) | 30 | 30 ✓ |
| HAT_VERBINDUNGSTECHNIK total (102 + 6) | 108 | 108 ✓ |
| HAT_AKTEURROLLE → ar_materialbroker | 4 | 4 ✓ |
| HAT_ZERTIFIZIERUNG total (was 10, +1 new) | 11 | 11 ✓ |

### What changed in detail

**P-17 — PruefungNachweis hubs (9 effective new nodes, `pr_brandschutznachweis` already existed):**
`pr_zerstoerungsfreie_pruefung` (NDT), `pr_zerstoerende_pruefung` (parent), `pr_korrosionspruefung`, `pr_festigkeitssortierung_holz`, `pr_bohrkernpruefung_beton`, `pr_dokumentenpruefung_bestand`, `pr_schadstoffpruefung` (parent), `pr_materialbeprobung` (parent), `pr_feuchtepruefung`.

**P-17 hierarchy (4 rels):**
- `pr_bohrkernpruefung_beton` → `pr_zerstoerende_pruefung`
- `pr_zugversuch` (existing) → `pr_zerstoerende_pruefung`
- `pr_schadstoffscreening` (existing) → `pr_schadstoffpruefung`
- `pr_abbrandbemessung` (existing) → `pr_brandschutznachweis`

**P-17 TYPISCH_BEI_MATERIAL (12 rels):** NDT covers Stahl/Beton/Stahlbeton/Holz; Korrosionsprüfung covers Stahl + Stahlbeton (rebar); Festigkeitssortierung covers Holz; Bohrkernprüfung covers Beton + Stahlbeton; Feuchteprüfung covers Holz + Lehm + Dämmstoff.

**P-20 — Verbindungstechnik tree (4 new nodes):**
- `vt_bolzenverbindung` — K.118 external steel staircase, Zinneke plywood
- `vt_demontierbarer_schwerlastanker` — Plattenpalast Berlin
- `vt_stahlverbinder_holz` — Recypark Anderlecht glulam half-arches
- `vt_stahlrahmen_fassadenmodul` — Resource Rows Copenhagen brick modules

**P-20 hierarchy (5 IST_UNTERVERFAHREN_VON rels):** vt_verschraubung, vt_klemmverbindung, vt_steckverbindung, vt_bolzenverbindung, vt_demontierbarer_schwerlastanker → vt_reversible_fuegung (parent).

**P-20 BELEGT cases (6 rels with `reversibility` property on rel):**
- `bg_cascadeup_clst_floor_panels` → vt_reversible_fuegung [reversibility: reversible]
- `bg_cascadeup_clst_wall_panels` → vt_reversible_fuegung [reversibility: reversible]
- `bg_plattenpalast_wbs70_wand_deckenelemente` → vt_demontierbarer_schwerlastanker [reversibility: partially_reversible]
- `bg_k118_external_steel_stair` → vt_bolzenverbindung [reversibility: reversible]
- `bg_brettschichtholzbogen_recypark_demets` → vt_stahlverbinder_holz [reversibility: partially_reversible]
- `bg_ziegelfassadenmodule_mauerwerksausschnitte_resource_rows` → vt_stahlrahmen_fassadenmodul [reversibility: partially_reversible]

**P-22 — Förderprogramm + Marketplace actor role (2 Programm + 1 Akteurrolle + 8 rels):**
- New Programm: `prog_horizon_2020`, `prog_urban_innovative_actions`
- New Akteurrolle: `ar_materialbroker`
- ERHALT_FOERDERUNG_DURCH: `p_harmalanranta → prog_horizon_2020`, `p_superlocal → prog_urban_innovative_actions`
- HAT_ZERTIFIZIERUNG: `p_liander → zbs_breeam`, `p_thoravej_29 → zbs_dgnb` (noop, already existed)
- HAT_AKTEURROLLE: `rotor_dc / concular / madaster / opalis → ar_materialbroker`
- `prog_recreate` enhanced with `funding_source: 'EU Horizon 2020'`, `funding_amount_eur: 12500000`

### Conservative choices made during apply

- **Dropped `bg_recyclinghaus_holz100`, `bg_brummen`, `bg_triodos` BELEGT edges** — corresponding BGs/projects don't exist in the corpus. Pre-flight check caught this.
- **Did NOT create new `prog_breeam_nl` / `prog_dgnb` nodes** — used existing `zbs_breeam` / `zbs_dgnb` via HAT_ZERTIFIZIERUNG instead. Cleaner taxonomy.
- **Did NOT bulk-add `reversibility='unknown'` to all 102 existing HAT_VERBINDUNGSTECHNIK rels** — absence of property is "unknown" by default, saves 102 churn writes.
- **Idempotency: 2 ops handled gracefully** (pr_brandschutznachweis pre-existed; p_thoravej→zbs_dgnb pre-existed). Confirms the apply tool's noop_existing handling.

### Phase C rollback procedure

#### Option 1 — Inverse-patch (preferred)

```text
For each add_node      → emit delete_node {id}     # 17 deletes (1 skipped if pre-existed)
For each add_rel       → emit delete_rel {from, type, to}  # 35 deletes
For prog_recreate enhancement → emit set_node_properties with null for funding_source, funding_amount_eur, scope_note
```

#### Option 2 — Targeted Cypher (surgical, single block)

```cypher
// 1. Delete the 16 new Phase C nodes (cascade kills their attached rels)
MATCH (n) WHERE n.id IN [
  'pr_zerstoerungsfreie_pruefung','pr_zerstoerende_pruefung','pr_korrosionspruefung',
  'pr_festigkeitssortierung_holz','pr_bohrkernpruefung_beton','pr_dokumentenpruefung_bestand',
  'pr_schadstoffpruefung','pr_materialbeprobung','pr_feuchtepruefung',
  'vt_bolzenverbindung','vt_demontierbarer_schwerlastanker','vt_stahlverbinder_holz','vt_stahlrahmen_fassadenmodul',
  'prog_horizon_2020','prog_urban_innovative_actions',
  'ar_materialbroker'
] DETACH DELETE n;

// 2. Strip prog_recreate enhancement
MATCH (n:Programm {id: 'prog_recreate'}) REMOVE n.funding_source, n.funding_amount_eur;
// note: scope_note may have been added separately — verify before stripping

// 3. The 2 new HAT_ZERTIFIZIERUNG edges to pre-existing zbs nodes need explicit cleanup
MATCH (:Projekt {id: 'p_liander_alliander_hq_duiven'})-[r:HAT_ZERTIFIZIERUNG]->(:ZertifizierungBewertungssystem {id: 'zbs_breeam'}) DELETE r;
// (the p_thoravej → zbs_dgnb edge pre-existed; do NOT delete it)

// 4. The 4 IST_UNTERVERFAHREN_VON edges from existing PruefungNachweis nodes to also-existing parents
// will be cascaded by step 1 (their parent target nodes are deleted in step 1).
```

#### Option 3 — Full restore from backup (nuclear)

Restore from [`_neo4j/review/backups/phase_c_pre_apply/`](../backups/phase_c_pre_apply/).

### New capabilities unlocked

```cypher
// Recommend missing tests for any reused BG by material rules
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(pr:PruefungNachweis)
WHERE NOT (bg)-[:HAT_PRUEFUNG]->(pr)
RETURN bg.id, m.name, collect(DISTINCT pr.name) AS recommended_tests
ORDER BY size(recommended_tests) DESC

// All reuse cases that explicitly use a reversible connection
MATCH (bg:Bauteilgruppe)-[r:HAT_VERBINDUNGSTECHNIK]->(vt:Verbindungstechnik)
WHERE r.reversibility = 'reversible'
RETURN bg.id, vt.name

// Reuse marketplaces in the corpus
MATCH (a:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle {id: 'ar_materialbroker'}) RETURN a.id, a.name

// Projects funded through specific programmes
MATCH (p:Projekt)-[:ERHALT_FOERDERUNG_DURCH]->(prog:Programm) RETURN p.name, prog.name
```

### Contract drift after Phase A + B + C

New labels and rel types live but not in contract yet (cumulative):
- Labels: `BauwerkEra`, `Bauproduktstatus` (A, B)
- Rel types: `TYPISCH_BEI_MATERIAL`, `TYPISCH_BEI_BAUTEILTYP`, `TYPISCH_BEI_ERA`, `GILT_IN_LAND`, `HAT_TYPISCHEN_BAUPRODUKTSTATUS`, `HAT_BAUPRODUKTSTATUS` (A, B), `IST_UNTERVERFAHREN_VON`, `ERHALT_FOERDERUNG_DURCH` (C)

Action item: small contract patch commit before Phase D.

---

## Phase D — applied 2026-05-16

**Patch:** [patches/phase_d.patch.jsonl](patches/phase_d.patch.jsonl)
**Apply report:** [apply_reports/phase_d.patch.apply_report.json](apply_reports/phase_d.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_d_pre_apply/`](../backups/phase_d_pre_apply/) (2 204 nodes, 16 000 rels; gitignored)

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 204 | **2 238** | +34 |
| Relationships | 16 000 | **16 059** | +59 |

**Operations:** 93 records / 0 errors.

| Op | Count | Effect |
|---|---:|---|
| add_node | 34 | 4 parent-category Aufbereitungsverfahren + 30 material-specific child av_* |
| add_rel | 59 | 21 IST_UNTERVERFAHREN_VON parent-child + 33 TYPISCH_BEI_MATERIAL + 5 BELEGT HAT_AUFBEREITUNG |

### New nodes (4 parents + 30 children)

**Parents:** `av_oberflaechenbehandlung`, `av_zerlegung_vereinzelung`, `av_materialsortierung_chargenbildung`, `av_kaskadierende_wiederverwendung`.

**Children by material branch:**
- **Stahl** (4): av_sandstrahlen, av_entrosten_korrosionsbehandlung, av_korrosionsschutz_beschichten, av_stahl_zuschnitt_bohrung
- **Holz** (7): av_entnageln, av_holz_fremdstoffentfernung, av_hobeln_schleifen_holz, av_holz_zuschnitt_reparatur, av_holz_trocknung_feuchtekonditionierung, av_holz_festigkeitssortierung, av_holz_schadstoffscreening
- **Beton/HCS** (5): av_betonfertigteil_saegen, av_beton_anhaftungen_entfernen, av_hcs_zuschnitt_bohrungen_fittings, av_betonfertigteil_factory_refurbishment, av_betonfertigteil_tagging_sortierung
- **Mauerwerk** (4): av_moertelentfernung_ziegel, av_ziegel_sortierung_pruefung, av_mauerwerk_diamantsaegen_modul, av_naturstein_reinigung_schleifen_zuschnitt
- **Glas** (3): av_glas_reinigung_entkitten, av_glas_pruefung_sortierung, av_fenster_refurbishment
- **Aluminium** (3): av_aluminium_reinigung_entdichtung, av_aluminiumfenster_beschlag_dichtung, av_aluminium_zuschnitt_bohrung
- **Bio** (4): av_lehm_sieben_mischen, av_stroh_pruefen_trocknen_sortieren, av_bio_daemmstoff_zuschnitt_gefach, av_biobasiert_hygiene_schadstoffcheck

### BELEGT project-level cases (5)

- `bg_ziegelfassadenmodule_mauerwerksausschnitte_resource_rows` → av_mauerwerk_diamantsaegen_modul (Resource Rows BELEGT)
- `bg_brettschichtholzbogen_recypark_demets` → av_holz_zuschnitt_reparatur (Recypark BELEGT)
- `bg_k118_floor_finishes_bricks_panels` → av_naturstein_reinigung_schleifen_zuschnitt (K.118 BELEGT)
- `bg_brent_cross_reclaimed_tubular_columns` → av_sandstrahlen (Steel reuse — FCRBE general practice)
- `bg_55gss_reused_steel_external_core` → av_korrosionsschutz_beschichten (ASBP source mentions coating renewal)

### Phase D rollback

Option 1 (preferred): inverse-patch via runner.
Option 2 (Cypher): `MATCH (n:Aufbereitungsverfahren) WHERE n.id IN ['av_oberflaechenbehandlung','av_zerlegung_vereinzelung','av_materialsortierung_chargenbildung','av_kaskadierende_wiederverwendung','av_sandstrahlen','av_entrosten_korrosionsbehandlung','av_korrosionsschutz_beschichten','av_stahl_zuschnitt_bohrung','av_entnageln','av_holz_fremdstoffentfernung','av_hobeln_schleifen_holz','av_holz_zuschnitt_reparatur','av_holz_trocknung_feuchtekonditionierung','av_holz_festigkeitssortierung','av_holz_schadstoffscreening','av_betonfertigteil_saegen','av_beton_anhaftungen_entfernen','av_hcs_zuschnitt_bohrungen_fittings','av_betonfertigteil_factory_refurbishment','av_betonfertigteil_tagging_sortierung','av_moertelentfernung_ziegel','av_ziegel_sortierung_pruefung','av_mauerwerk_diamantsaegen_modul','av_naturstein_reinigung_schleifen_zuschnitt','av_glas_reinigung_entkitten','av_glas_pruefung_sortierung','av_fenster_refurbishment','av_aluminium_reinigung_entdichtung','av_aluminiumfenster_beschlag_dichtung','av_aluminium_zuschnitt_bohrung','av_lehm_sieben_mischen','av_stroh_pruefen_trocknen_sortieren','av_bio_daemmstoff_zuschnitt_gefach','av_biobasiert_hygiene_schadstoffcheck'] DETACH DELETE n;`
Option 3 (nuclear): restore from [`_neo4j/review/backups/phase_d_pre_apply/`](../backups/phase_d_pre_apply/).

### Capability: "what tools clean / cut / treat material X"

```cypher
MATCH (m:Material)<-[:TYPISCH_BEI_MATERIAL]-(av:Aufbereitungsverfahren)
OPTIONAL MATCH (av)-[:IST_UNTERVERFAHREN_VON]->(parent:Aufbereitungsverfahren)
RETURN m.name, av.name, parent.name AS category ORDER BY m.name
```

---

## Phase E — applied 2026-05-16

**Patch:** [patches/phase_e.patch.jsonl](patches/phase_e.patch.jsonl)
**Apply report:** [apply_reports/phase_e.patch.apply_report.json](apply_reports/phase_e.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_e_pre_apply/`](../backups/phase_e_pre_apply/) (2 238 nodes, 16 059 rels; gitignored)

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 238 | **2 260** | +22 |
| Relationships | 16 059 | **16 124** | +65 |

**Operations:** 87 records / 0 errors.

| Op | Count | Effect |
|---|---:|---|
| add_node | 22 | 5 LebenszyklusModul (P-8) + 6 Layer (P-7) + 11 Marktmodell (P-3) |
| add_rel | 65 | 8 METHODENGRUNDLAGE_NORM + 8 BERECHNET_NACH_MODUL + 15 TEILT_LAYER + 31 HAT_MARKTMODELL + 3 same-site Multi Brussels HAT_MARKTMODELL |

### New nodes (22)

**P-8 LebenszyklusModul (5):** `lz_a1_a3` (Produkt A1-A3), `lz_a4_a5` (Errichtung), `lz_b` (Nutzung), `lz_c` (End of Life), `lz_d` (Module D / Reuse Credits).

**P-7 Layer / Brand's shearing layers (6):** `layer_site`, `layer_structure`, `layer_skin`, `layer_services`, `layer_space_plan`, `layer_stuff`. Each carries `lifespan_years_min/max` properties.

**P-3 Marktmodell (11):** `mm_kauf_neu`, `mm_kauf_gebraucht`, `mm_spende`, `mm_leasing`, `mm_rueckkauf`, `mm_same_site`, `mm_plattform_vermittelt`, `mm_forschungsprojekt_zuteilung`, `mm_intra_konzern`, `mm_take_back_service`, `mm_unbekannt`.

### Critical wires unlocked

**P-8 METHODENGRUNDLAGE_NORM (8):** lz_a1_a3/d → DIN_EN_15804 + DIN_EN_15978; lz_a4_a5/b/c → DIN_EN_15978; lz_a1_a3 → ISO_14040 + ISO_14044. The 4 LCA orphan Normen (DIN_EN_15804/15978, ISO_14040/14044) gain their first inbound edges.

**P-8 BERECHNET_NACH_MODUL (8 project edges):** 55 Great Suffolk (A1-A3 + A4-A5), Resource Rows (B + D), Brent Cross (D), K.118 (A1-A3), KA13 (D), Thoravej 29 (D). Now every project with a CO₂ claim has its LCA scope tagged.

**P-7 TEILT_LAYER (15):** Bauteiltyp → Layer mapping. bt_traeger/bt_stuetze/bt_decke/bt_wand/bt_fundament/bt_daemmung → structure; bt_fassade/bt_dach/bt_fenster → skin; bt_technik → services; bt_ausbau/bt_tuer/bt_treppe/bt_gelaender/bt_boden → space_plan.

**P-3 HAT_MARKTMODELL (34 BELEGT):** 31 same-site BGs → mm_same_site (mirror of bps_bestand_no_status); 3 Multi Brussels BGs → mm_plattform_vermittelt (Madaster + Rotor evidence).

### New capabilities

```cypher
// Every reuse case with its LCA scope and methodological standard
MATCH (p:Projekt)-[:BERECHNET_NACH_MODUL]->(lz:LebenszyklusModul)-[:METHODENGRUNDLAGE_NORM]->(n:Norm)
RETURN p.name, lz.name, collect(DISTINCT n.id) AS methodology

// Bauteilgruppen grouped by Brand's layer (lifespan expectations)
MATCH (bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)-[:TEILT_LAYER]->(layer:Layer)
RETURN layer.name, layer.lifespan_years_min, count(bg) AS reuse_cases ORDER BY reuse_cases DESC

// Reuse cases by commercial model
MATCH (bg:Bauteilgruppe)-[:HAT_MARKTMODELL]->(mm:Marktmodell)
RETURN mm.name, count(bg) AS bg_count ORDER BY bg_count DESC
```

### Phase E rollback

Option 1: inverse-patch.
Option 2 (Cypher):
```cypher
MATCH (n) WHERE n.id IN [
  'lz_a1_a3','lz_a4_a5','lz_b','lz_c','lz_d',
  'layer_site','layer_structure','layer_skin','layer_services','layer_space_plan','layer_stuff',
  'mm_kauf_neu','mm_kauf_gebraucht','mm_spende','mm_leasing','mm_rueckkauf','mm_same_site',
  'mm_plattform_vermittelt','mm_forschungsprojekt_zuteilung','mm_intra_konzern','mm_take_back_service','mm_unbekannt'
] DETACH DELETE n;
```
Option 3: restore from [`_neo4j/review/backups/phase_e_pre_apply/`](../backups/phase_e_pre_apply/).

### Contract drift after Phase A + B + C + D + E

New labels live but not in contract:
- `BauwerkEra`, `Bauproduktstatus`, `LebenszyklusModul`, `Layer`, `Marktmodell`

New rel types live but not in contract:
- `TYPISCH_BEI_MATERIAL`, `TYPISCH_BEI_BAUTEILTYP`, `TYPISCH_BEI_ERA`
- `GILT_IN_LAND`, `HAT_TYPISCHEN_BAUPRODUKTSTATUS`, `HAT_BAUPRODUKTSTATUS`
- `IST_UNTERVERFAHREN_VON`, `ERHALT_FOERDERUNG_DURCH`
- `METHODENGRUNDLAGE_NORM`, `BERECHNET_NACH_MODUL`, `TEILT_LAYER`, `HAT_MARKTMODELL`

Action item: small contract patch commit before next baseline run.

---

## Phase F — applied 2026-05-16

**Patch:** [patches/phase_f.patch.jsonl](patches/phase_f.patch.jsonl)
**Apply report:** [apply_reports/phase_f.patch.apply_report.json](apply_reports/phase_f.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_f_pre_apply/`](../backups/phase_f_pre_apply/) (2 260 nodes, 16 124 rels; gitignored)

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 260 | **2 279** | +19 |
| Relationships | 16 124 | **16 138** | +14 |

**Operations:** 33 records / 0 errors.

| Op | Count | Effect |
|---|---:|---|
| add_node | 19 | 10 Defekt (P-1) + 9 MatchingQualitaet (P-13) |
| add_rel | 14 | 14 TYPISCH_BEI_MATERIAL for Defekt |

### New nodes

**P-1 Defekt (10):** def_korrosion, def_riss, def_verformung, def_karbonatisierung, def_holzwurm_pilzbefall, def_hohlraum_delamination, def_oberflaechenmangel, def_chemische_belastung, def_brandschaden, def_keine_befunde (positive-finding category).

**P-13 MatchingQualitaet (9):** Temporal axis (3): mq_temporal_easy, mq_temporal_storage, mq_temporal_planned. Geographic axis (3): mq_geographic_local, mq_geographic_regional, mq_geographic_intl. Specification axis (3): mq_spec_exact, mq_spec_anpassung, mq_spec_zweckaenderung.

### TYPISCH_BEI_MATERIAL for Defekt (14 rules)

- Korrosion → Stahl + Stahlbeton + Aluminium
- Karbonatisierung → Beton + Stahlbeton
- Holzwurm/Pilzbefall → Holz + Stroh + Lehm
- Hohlraum/Delamination → Glas + MDF
- Brandschaden → Stahl + Holz
- Chemische Belastung → Naturstein + Ziegel

### P-18 ReusePattern — explicitly NOT created

The pattern information is already derivable via existing traversals:
`Land + Material + Norm (via GILT_IN_LAND) + PruefungNachweis (via TYPISCH_BEI_MATERIAL) + Bauproduktstatus (via HAT_TYPISCHEN_BAUPRODUKTSTATUS) + Verbindungstechnik`. Creating ReusePattern nodes would duplicate this without adding new information. Dropped to avoid orphan risk and unnecessary hub creation.

### Phase F rollback

Option 1: inverse-patch.
Option 2 (Cypher):
```cypher
MATCH (n) WHERE n.id IN [
  'def_korrosion','def_riss','def_verformung','def_karbonatisierung',
  'def_holzwurm_pilzbefall','def_hohlraum_delamination','def_oberflaechenmangel',
  'def_chemische_belastung','def_brandschaden','def_keine_befunde',
  'mq_temporal_easy','mq_temporal_storage','mq_temporal_planned',
  'mq_geographic_local','mq_geographic_regional','mq_geographic_intl',
  'mq_spec_exact','mq_spec_anpassung','mq_spec_zweckaenderung'
] DETACH DELETE n;
```
Option 3: restore from [`_neo4j/review/backups/phase_f_pre_apply/`](../backups/phase_f_pre_apply/).

### Capabilities unlocked

```cypher
// For each material, what defects are typically checked in reuse assessments
MATCH (m:Material)<-[:TYPISCH_BEI_MATERIAL]-(def:Defekt)
RETURN m.name, collect(DISTINCT def.name) AS defects_to_screen

// Reused steel BG needing corrosion check (combines P-1 + P-17)
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id: 'mat_stahl'})
WHERE bg.counts_as_direct_reuse = true
  AND NOT (bg)-[:HAT_PRUEFUNG]->(:PruefungNachweis {id: 'pr_korrosionspruefung'})
RETURN bg.id

// MatchingQualitaet ready for round 003 (currently 0 BG edges — will be added per project)
MATCH (n:MatchingQualitaet) RETURN n.id, n.name
```

---

## Phase G — applied 2026-05-17

**Patch:** [patches/phase_g.patch.jsonl](patches/phase_g.patch.jsonl)
**Apply report:** [apply_reports/phase_g.patch.apply_report.json](apply_reports/phase_g.patch.apply_report.json)
**Extraction summary:** [phase_g_extraction_summary.json](phase_g_extraction_summary.json) — per-project tag list with source excerpts.
**Archive↔project map:** [phase_g_archive_project_map.json](phase_g_archive_project_map.json) — 76 archive files mapped to 75 Projekt IDs (Berlin_Schildow has two files mapped to one project).
**Pre-apply backup:** [`_neo4j/review/backups/phase_g_pre_apply/`](../backups/phase_g_pre_apply/) (2 279 nodes, 16 138 rels; gitignored).

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 279 | **2 279** | +0 |
| Relationships | 16 138 | **16 347** | +209 |

**Operations:** 211 records / 0 errors. 2 records were exact duplicates from Berlin_Schildow's two archive files mapping to the same project — absorbed as `noop_existing_rel`.

| Op | Count | Effect |
|---|---:|---|
| add_rel `HAT_DEFEKT_BEFUND` | 22 | Project-level Defekt findings, 6 distinct vocab ids matched |
| add_rel `HAT_MATCHINGQUALITAET` | 165 | Project-level matching axes, 5 distinct vocab ids matched |
| add_rel `HAT_DOMINANT_MARKTMODELL` | 22 | Project-level dominant sourcing model, 4 distinct vocab ids matched |

### How it was generated

A keyword scanner (`_scripts/_generate_phase_g_patch.py`) walked all 76 archive `.md` files in `_archive/research/gebaeude/`. Two iterations:

1. **First pass (363 records):** three patterns triggered universally and were rejected as false positives:
   - `def_chemische_belastung` ← `\bschadstoff` matched the standard section header *"Schadstoffprüfung"*
   - `mq_temporal_easy` ← `\bdirect(ly)? reuse\b` matched the file titles *"Fallstudie Direct Reuse / …"*
   - `mq_spec_anpassung` ← `\banpassung\b` is genuinely universal (every reuse case adapts) — **kept** as true signal
2. **Second pass (211 records, applied):** tightened `def_chemische_belastung` to require specific chemical-attack terms (PCB, Asbest, Salzangriff, Säureangriff, Ölkontamination, Schwermetall); tightened `mq_temporal_easy` to require explicit temporal phrasings.

Each emitted rel carries:
- `evidence='INFER'` — every Phase G edge is an inference from text scan, not a primary claim
- `source='archive:<filename>'` — pointer to the source case study
- `source_excerpt` — ~100-char surrounding text for review

### Per-vocab edge counts after apply

**Defekt (22 rels across 19/76 projects):**
| vocab | n |
|---|---:|
| def_korrosion | 10 |
| def_verformung | 5 |
| def_riss | 3 |
| def_keine_befunde | 2 |
| def_hohlraum_delamination | 1 |
| def_brandschaden | 1 |

**MatchingQualitaet (165 rels across 75/76 projects):**
| vocab | n |
|---|---:|
| mq_spec_anpassung | 75 |
| mq_temporal_storage | 35 |
| mq_geographic_local | 26 |
| mq_spec_zweckaenderung | 23 |
| mq_geographic_regional | 6 |

**Marktmodell (22 rels across 20/76 projects):**
| vocab | n |
|---|---:|
| mm_same_site | 10 |
| mm_plattform_vermittelt | 6 |
| mm_spende | 4 |
| mm_leasing | 2 |

### Orphan reduction

| Label | Orphans before G | Orphans after G | Total nodes |
|---|---:|---:|---:|
| Defekt | 4 | **1** (def_oberflaechenmangel) | 10 |
| MatchingQualitaet | 9 | **4** (mq_temporal_easy, mq_temporal_planned, mq_geographic_intl, mq_spec_exact) | 9 |
| Marktmodell | 9 | **7** (mm_kauf_gebraucht, mm_kauf_neu, mm_rueckkauf, mm_forschungsprojekt_zuteilung, mm_intra_konzern, mm_take_back_service, mm_unbekannt) | 11 |

The 4 remaining MatchingQualitaet orphans correspond to axis values that are difficult to detect from archive text alone (e.g. *mq_spec_exact* is a non-event — projects don't describe "we used the part as-is, no modification"). The 7 remaining Marktmodell orphans are sourcing models that aren't well-evidenced in the current corpus (Take-Back, Leasing variants, Rückkauf).

### Phase G rollback

Option 1: inverse-patch (recommended — preserves the 2 noop_existing_rel cases naturally).
Option 2 (Cypher):
```cypher
MATCH (:Projekt)-[r:HAT_DEFEKT_BEFUND]->(:Defekt) DELETE r;
MATCH (:Projekt)-[r:HAT_MATCHINGQUALITAET]->(:MatchingQualitaet) DELETE r;
MATCH (:Projekt)-[r:HAT_DOMINANT_MARKTMODELL]->(:Marktmodell) DELETE r;
```
Option 3: restore from [`_neo4j/review/backups/phase_g_pre_apply/`](../backups/phase_g_pre_apply/).

### Capabilities unlocked

```cypher
// Most-affected projects for a given defect
MATCH (p:Projekt)-[:HAT_DEFEKT_BEFUND]->(:Defekt {id: 'def_korrosion'})
RETURN p.name ORDER BY p.name

// Matching profile per project — temporal + geographic + spec axes together
MATCH (p:Projekt)-[r:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
RETURN p.name, collect({axis: split(mq.id,'_')[1], value: mq.name, source: r.source}) AS profile

// Sourcing model adoption — which projects use platforms (Madaster/Concular/Rotor/Restado)
MATCH (p:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(:Marktmodell {id: 'mm_plattform_vermittelt'})
RETURN p.name, p.id

// Cross-cut: same-site reuse projects + which materials they reuse
MATCH (p:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(:Marktmodell {id: 'mm_same_site'})
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
RETURN p.name, collect(DISTINCT m.name) AS reused_materials
```

---

## Phase H — applied 2026-05-17

**Patch:** [patches/phase_h.patch.jsonl](patches/phase_h.patch.jsonl)
**Apply report:** [apply_reports/phase_h.patch.apply_report.json](apply_reports/phase_h.patch.apply_report.json)
**Pre-apply backup:** [`_neo4j/review/backups/phase_h_pre_apply/`](../backups/phase_h_pre_apply/) (2 279 nodes, 16 347 rels; gitignored).

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 279 | **2 296** | +17 |
| Relationships | 16 347 | **16 366** | +19 |

**Operations:** 36 records / 0 errors.

| Op | Count | Effect |
|---|---:|---|
| add_node | 17 | 6 ZustandsKlasse (P-2) + 6 Wirtschaft (P-10) + 5 Akzeptanz (P-9) |
| add_rel | 19 | 12 TYPISCH_BEI_MATERIAL for ZustandsKlasse + 7 GILT_IN_LAND for Akzeptanz |

### New nodes

**P-2 ZustandsKlasse (6):** zk_neuwertig, zk_gebrauchsspuren_funktional, zk_eingeschraenkt_nachbearbeitung, zk_eingeschraenkt_nutzungsklasse_reduzieren, zk_nicht_wiederverwendbar, zk_unbekannt_pruefung_offen. Standard discrete condition grades used in reuse assessment.

**P-10 Wirtschaft (6):** wi_capex_neutral, wi_capex_niedriger_direkter_ersparnis, wi_capex_hoeher_opex_payback, wi_capex_hoeher_subvention, wi_capex_hoeher_marketing_payback, wi_hidden_costs_lagerung_pruefung. **Payback-model axis** — adds a new axis under the existing Wirtschaft label, which already had 6 aspect-category nodes (wi_finanzierung, wi_geschaeftsmodell, wi_kostenvergleich, wi_lebenszykluskosten, wi_preisbildung, wi_restwert). Both axes coexist under one label, like MatchingQualitaet's three axes.

**P-9 Akzeptanz (5):** ak_dgnb_zertifizierung, ak_breeam_zertifizierung, ak_leed_zertifizierung, ak_oeffentlicher_bauherr_pilot, ak_aesthetik_patinakultur. Stakeholder acceptance signals for reuse — certifications, public-client pilots, aesthetic culture.

### Grounding rules (anti-orphan)

**ZustandsKlasse → Material (12 TYPISCH_BEI_MATERIAL):**
- Neuwertig → Glas, Naturstein, Aluminium
- Gebrauchsspuren funktional → Holz, Ziegel, Stahl
- Nachbearbeitung → Stahl (re-coating), Holz (planing), Beton (edge work)
- Nutzungsklasse reduzieren → Stahlbeton (downgrade), Holz (downgrade)
- Nicht wiederverwendbar → MDF (recycling only)

**Akzeptanz → Land (7 GILT_IN_LAND):**
- DGNB → DE + AT + CH
- BREEAM → UK + NL
- LEED → US + International

### Phase H rollback

Option 1: inverse-patch.
Option 2 (Cypher):
```cypher
MATCH (n) WHERE n.id IN [
  'zk_neuwertig','zk_gebrauchsspuren_funktional','zk_eingeschraenkt_nachbearbeitung',
  'zk_eingeschraenkt_nutzungsklasse_reduzieren','zk_nicht_wiederverwendbar','zk_unbekannt_pruefung_offen',
  'wi_capex_neutral','wi_capex_niedriger_direkter_ersparnis','wi_capex_hoeher_opex_payback',
  'wi_capex_hoeher_subvention','wi_capex_hoeher_marketing_payback','wi_hidden_costs_lagerung_pruefung',
  'ak_dgnb_zertifizierung','ak_breeam_zertifizierung','ak_leed_zertifizierung',
  'ak_oeffentlicher_bauherr_pilot','ak_aesthetik_patinakultur'
] DETACH DELETE n;
```
Option 3: restore from [`_neo4j/review/backups/phase_h_pre_apply/`](../backups/phase_h_pre_apply/).

### Orphan state after Phase H

| Label | Orphans | Total | Notes |
|---|---:|---:|---|
| ZustandsKlasse | 1 | 6 | Only zk_unbekannt_pruefung_offen orphan (intentional — "not yet assessed" is a non-event category) |
| Wirtschaft (payback-model axis) | 6 | 6 (of new) | All new wi_capex_* nodes ungrounded; will be tagged per-project in a future Phase G-style scan |
| Akzeptanz | 2 | 5 | ak_oeffentlicher_bauherr_pilot + ak_aesthetik_patinakultur lack country grounding (both are cross-cutting) |

The 6 ungrounded Wirtschaft payback-model nodes are expected — like Phase F's MatchingQualitaet seed, they'll be tagged once archive-driven scanning extends to cost-model phrases ("CapEx", "Förderung deckt", "Kosten vergleichbar", etc.).

### Capabilities unlocked

```cypher
// Condition grading for a given material — what's typical when reused
MATCH (zk:ZustandsKlasse)-[:TYPISCH_BEI_MATERIAL]->(m:Material {id: 'mat_stahl'})
RETURN zk.name, zk.scope_note

// Which certifications accept reuse in a given country
MATCH (ak:Akzeptanz)-[:GILT_IN_LAND]->(:Land {id: 'land_deutschland'})
RETURN ak.id, ak.name

// All acceptance certifications cross-country reach
MATCH (ak:Akzeptanz)-[:GILT_IN_LAND]->(l:Land)
RETURN ak.name, collect(l.name) AS countries
```

---

## Phase I — applied 2026-05-17

**Patch:** [patches/phase_i.patch.jsonl](patches/phase_i.patch.jsonl)
**Pre-apply backup:** [`_neo4j/review/backups/phase_i_pre_apply/`](../backups/phase_i_pre_apply/) (2 296 nodes, 16 366 rels; gitignored).

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 296 | **2 296** | +0 |
| Relationships | 16 366 | **16 450** | +84 |

**Operations:** 93 records / 0 errors. 9 records absorbed as `noop_existing_rel` (orphan-rescue overlapping with Marktmodell widening for same project+vocab).

| Op | Count | Effect |
|---|---:|---|
| add_rel `HAT_MATCHINGQUALITAET` | 14 | Manual rescue of mq_temporal_easy, mq_temporal_planned, mq_geographic_intl, mq_spec_exact |
| add_rel `HAT_DEFEKT_BEFUND` | 3 | Manual rescue of def_oberflaechenmangel |
| add_rel `HAT_DOMINANT_AKZEPTANZ` | 9 | New rel type — Manual rescue of ak_oeffentlicher_bauherr_pilot + ak_aesthetik_patinakultur |
| add_rel `HAT_DOMINANT_MARKTMODELL` | 67 | 22 from orphan rescue + 45 from Marktmodell widening rescan |

### Orphan state after Phase I

| Label | Orphans before I | Orphans after I |
|---|---:|---:|
| Defekt | 1 | **0** |
| MatchingQualitaet | 4 | **0** |
| Marktmodell | 7 | **2** (mm_rueckkauf, mm_unbekannt) |
| Akzeptanz | 2 | **0** |

The 2 remaining Marktmodell orphans (mm_rueckkauf = buyback, mm_unbekannt = unknown) are intentional non-events. All Phase F/H seed vocabs are now connected to projects.

### Phase I rollback

```cypher
MATCH ()-[r]->()
WHERE r.source = 'manual_orphan_rescue' OR r.reason STARTS WITH 'P-I '
DELETE r;
```

Or restore from [`_neo4j/review/backups/phase_i_pre_apply/`](../backups/phase_i_pre_apply/).

---

## Phase J — applied 2026-05-17

**Patch:** [patches/phase_j.patch.jsonl](patches/phase_j.patch.jsonl)
**Pre-apply backup:** [`_neo4j/review/backups/phase_j_pre_apply/`](../backups/phase_j_pre_apply/) (2 296 nodes, 16 450 rels; gitignored).

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 296 | **2 296** | +0 |
| Relationships | 16 450 | **16 470** | +20 |

**Operations:** 20 records / 0 errors. All add_rel `HAT_WIRTSCHAFT` (new project-level rel type).

### Per-vocab edge counts

| vocab | n | sample-source pattern |
|---|---:|---|
| wi_capex_hoeher_subvention | 11 | "Förderprogramm | DISRUPT case study" / "Holcim Awards" / "funded by H2020" |
| wi_hidden_costs_lagerung_pruefung | 5 | "Reuse-Koordination", "Zwischenlager Kosten" |
| wi_capex_neutral | 3 | "Kosten etwa vergleichbar mit Neubau" / "kostenneutral" |
| wi_capex_hoeher_marketing_payback | 1 | "Positionierung für Austauschbarkeit" |

After Phase J, the 6 new wi_capex_* Wirtschaft nodes (Phase H seed) reach 4 of 6 connected; wi_capex_niedriger_direkter_ersparnis + wi_capex_hoeher_opex_payback remain orphan (low signal in corpus).

### Phase J rollback

```cypher
MATCH ()-[r:HAT_WIRTSCHAFT]->() DELETE r;
```
Or restore from `_neo4j/review/backups/phase_j_pre_apply/`.

---

## Round 003 — applied 2026-05-17

**Patch:** [patches/round_003.patch.jsonl](patches/round_003.patch.jsonl)
**Pre-apply backup:** [`_neo4j/review/backups/round_003_pre_apply/`](../backups/round_003_pre_apply/) (2 296 nodes, 16 470 rels; gitignored).

### What landed

| | Before | After | Δ |
|---|---:|---:|---:|
| Nodes | 2 296 | **2 296** | +0 |
| Relationships | 16 470 | **16 822** | +352 |

**Operations:** 354 records / 0 errors. 2 absorbed as dedup.

| Op | Count | Effect |
|---|---:|---|
| add_rel `HAT_DEFEKT` | 31 | BG-level — propagated from project-level HAT_DEFEKT_BEFUND via TYPISCH_BEI_MATERIAL grounding |
| add_rel `HAT_MARKTMODELL` | 321 | BG-level — propagated from project-level HAT_DOMINANT_MARKTMODELL to all BGs in project |

### Inference rules

**Defekt propagation (BG-level):**
```cypher
(p:Projekt)-[:HAT_DEFEKT_BEFUND]->(d:Defekt)
AND (d)-[:TYPISCH_BEI_MATERIAL]->(m:Material)
AND (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
⇒ (bg)-[:HAT_DEFEKT]->(d)
```
A defect tagged at project level propagates only to BGs that actually use a material the defect is typical for. Conservative.

**Marktmodell propagation (BG-level):**
```cypher
(p:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
AND (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
⇒ (bg)-[:HAT_MARKTMODELL]->(mm)
```
Sourcing model is project-wide — all BGs in a project share the dominant Marktmodell.

**MatchingQualitaet:** intentionally **not propagated** to BG level — axis values (temporal/geographic/spec) are project-dominant signals, not per-BG.

### Coverage after Round 003

| BG dimension | Coverage |
|---|---:|
| NUTZT_MATERIAL | 301/306 (98%) |
| HAT_MARKTMODELL | 237/306 (77%) — up from 34/306 (11%) |
| HAT_AUFBEREITUNG | 225/306 (74%) |
| HAT_PRUEFUNG | 194/306 (63%) |
| HAT_RUECKBAUVERFAHREN | 179/306 (58%) |
| HAT_LOGISTIK | 178/306 (58%) |
| HAT_VERBINDUNGSTECHNIK | 80/306 (26%) |
| HAT_BAUPRODUKTSTATUS | 37/306 (12%) |
| HAT_DEFEKT | 31/306 (10%) — new |

### Round 003 rollback

```cypher
MATCH ()-[r]->()
WHERE r.source IN ['round_003_material_propagation', 'round_003_project_propagation']
DELETE r;
```

---

## Phase K — audit report (no graph change)

Generated [phase_k_audit_report.md](phase_k_audit_report.md). Key findings:

- 67 rel types in use; only 2 with ≤ 3 instances (`HAT_SCHADSTOFF` n=1, `ERHALT_FOERDERUNG_DURCH` n=2)
- Worst orphan-share labels (post-all-phases): Layer 33%, Wirtschaft 33%, Programm 29%, Akteurrolle 28%, Leistungsanforderung 25%, RechtlicheBedingung 22%
- BG defect coverage 10% — biggest remaining gap; full BG-level Defekt tagging needs archive Section-5 row matching, deferred
- Methode has only 13 nodes (not the assumed dozens), so the P-6 split is unnecessary; consider archive-level relabeling instead
- HuerdeKategorie already exists (10 nodes), so P-11 tidy is mostly done; only need to ensure all 28 Huerde nodes are categorized

No patch emitted from Phase K — it's a report for future planning.

---

## Contract drift cleanup — applied 2026-05-17

Updated [_neo4j/contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json](../../contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json):

- **Added 9 new node labels** to the `labels.items.enum`: BauwerkEra, Bauproduktstatus, LebenszyklusModul, Layer, Marktmodell, Defekt, MatchingQualitaet, ZustandsKlasse, Akzeptanz.
- **Added 18 new rel types** to the `type.enum`: TYPISCH_BEI_MATERIAL, TYPISCH_BEI_BAUTEILTYP, TYPISCH_BEI_ERA, GILT_IN_LAND, HAT_TYPISCHEN_BAUPRODUKTSTATUS, HAT_BAUPRODUKTSTATUS, IST_UNTERVERFAHREN_VON, ERHALT_FOERDERUNG_DURCH, METHODENGRUNDLAGE_NORM, BERECHNET_NACH_MODUL, TEILT_LAYER, HAT_MARKTMODELL, HAT_DEFEKT_BEFUND, HAT_DEFEKT, HAT_MATCHINGQUALITAET, HAT_DOMINANT_MARKTMODELL, HAT_DOMINANT_AKZEPTANZ, HAT_WIRTSCHAFT.

No live-graph impact — pure schema-doc bookkeeping. Future contract-validated imports will now accept the post-Phase-A-through-Round-003 graph.

---

## Final state — all phases of round 002 followup applied

| | A | B | C | D | E | F | G | H | I | J | R003 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Ops | 102 | 103 | 53 | 93 | 87 | 33 | 211 | 36 | 93 | 20 | 354 |
| New nodes | 12 | 29 | 16 | 34 | 22 | 19 | 0 | 17 | 0 | 0 | 0 |
| New rels | 58 | 74 | 34 | 59 | 65 | 14 | 209 | 19 | 84 | 20 | 352 |
| Property writes | 32 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

**Grand total: 1 185 ops / 149 new nodes / 988 new rels / 33 property writes.**

**Live graph: 2 147 → 2 296 nodes (+149), 15 834 → 16 822 rels (+988).**

**New rel types added after Phase H:**
- `HAT_DOMINANT_AKZEPTANZ` (Phase I — project-level acceptance signals)
- `HAT_WIRTSCHAFT` (Phase J — project-level cost-model signals)
- `HAT_DEFEKT` (Round 003 — BG-level defect findings)

### Contract drift after all six phases

New **labels** live but not in contract (10):
- `BauwerkEra` (Phase A)
- `Bauproduktstatus` (Phase B)
- `LebenszyklusModul`, `Layer`, `Marktmodell` (Phase E)
- `Defekt`, `MatchingQualitaet` (Phase F)
- `ZustandsKlasse`, `Akzeptanz` (Phase H — Wirtschaft label already existed, just got new node axis)

New **rel types** live but not in contract (16):
- `TYPISCH_BEI_MATERIAL`, `TYPISCH_BEI_BAUTEILTYP`, `TYPISCH_BEI_ERA` (Phase A)
- `GILT_IN_LAND`, `HAT_TYPISCHEN_BAUPRODUKTSTATUS`, `HAT_BAUPRODUKTSTATUS` (Phase B)
- `IST_UNTERVERFAHREN_VON`, `ERHALT_FOERDERUNG_DURCH` (Phase C — also `HAT_AUFBEREITUNG` Phase D, which already existed)
- `METHODENGRUNDLAGE_NORM`, `BERECHNET_NACH_MODUL`, `TEILT_LAYER`, `HAT_MARKTMODELL` (Phase E)
- `HAT_DEFEKT_BEFUND`, `HAT_MATCHINGQUALITAET`, `HAT_DOMINANT_MARKTMODELL` (Phase G — project-level reuse-quality dimensions)

Plus existing rel types reused with new properties: `HAT_VERBINDUNGSTECHNIK` (carries `reversibility` property after Phase C).

**Action item:** add to contract schemas in a small bookkeeping commit. No live-graph impact.

---

## Worklist after Round 003

- ✅ Phases A–K applied. 1 185 ops total. Live graph at 2 296 / 16 822.
- ✅ Contract schemas updated with 9 new labels + 18 new rel types.
- 🔬 **Verification queries:** [`VERIFICATION_QUERIES.cypher`](VERIFICATION_QUERIES.cypher) — 48 read-only queries covering every phase + cross-cutting insights.
- 📥 **Stub promotion (23 Projekte) — external research path** — see [`stub_research/README.md`](stub_research/README.md). Seven batched ChatGPT-research prompts, one per category, ≤ 5 projects each. Each batch produces an archive `.md` + JSONL chunk per project. After research lands, a small promotion patch flips `node_role` and (for some) relabels `Projekt` → `Programm` / `Plattform`.
- 📥 **Stub Akteur decisions (16)** — see [`STUB_AKTEUR_DECISIONS.md`](STUB_AKTEUR_DECISIONS.md). 2 delete / 2 merge / 12 keep (revised down from earlier rec — `zusammenkunft_berlin` reverted to KEEP). Removals execute via future prompts.
- ⏳ **Phase L (deferred)** — full BG-level Defekt parsing (Section-5 row matching); ~300-500 ops.
- ⏳ **Phase M (deferred)** — BG-level Norm tagging, project-level LCA-modul expansion, Akzeptanz widening.
- 📊 [phase_k_audit_report.md](phase_k_audit_report.md) — current orphan + coverage state; reference for future planning.
