# Rollback ledger — round 002 followup applied phases

**Purpose.** A running record of every applied phase, with the exact ops, before/after counts, the backup path, and a verification procedure. Each new phase appends here.

**Convention.** Every apply:
1. Takes a fresh backup under `_neo4j/review/backups/<phase>_pre_apply/`.
2. Generates a JSONL patch under `_neo4j/review/round_002_followup/patches/<phase>.patch.jsonl`.
3. Dry-runs first; only applies live after dry-run is clean.
4. Verifies with post-apply queries — full set in [`VERIFICATION_QUERIES.cypher`](VERIFICATION_QUERIES.cypher).
5. Appends a section to this doc.

**Verification, not destruction.** The Cypher snippets in each phase section below are **read-only sanity checks** that confirm the phase landed. Actual removal/rollback is done case-by-case via prompting + selective `DETACH DELETE`. Full backups live under `_neo4j/review/backups/<phase>_pre_apply/` if a full restore is ever needed.

**Apply order so far:** Phase A → B → C → D → E → F → G → H → I → J → Round 003 → Phase K (audit) → contract drift → Phase L → Phase M → Phase N.

**Combined effect:**

| | Before A | After R003 | After L | After M | After N |
|---|---:|---:|---:|---:|---:|
| Nodes | 2 147 | 2 296 | 2 296 | 2 296 | **2 296** |
| Relationships | 15 834 | 16 822 | 16 822 | 16 822 | **16 822** |

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
