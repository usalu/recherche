# Rollback ledger — round 002 followup applied phases

**Purpose.** A running record of every applied phase, with the exact ops, before/after counts, the backup path, and a rollback procedure. Each new phase appends here.

**Convention.** Every apply:
1. Takes a fresh backup under `_neo4j/review/backups/<phase>_pre_apply/`.
2. Generates a JSONL patch under `_neo4j/review/round_002_followup/patches/<phase>.patch.jsonl`.
3. Dry-runs first; only applies live after dry-run is clean.
4. Verifies with post-apply queries (logged here).
5. Appends a section to this doc.

**Apply order so far:** Phase A → Phase B.

**Combined effect:**

| | Before A | After A | After B |
|---|---:|---:|---:|
| Nodes | 2 147 | 2 159 | **2 188** |
| Relationships | 15 834 | 15 892 | **15 966** |

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

## What's next

- **Phase C** (P-17 PruefungNachweis + P-19 Aufbereitungsverfahren + P-20 Verbindungstechnik + P-22 Förderprogramm), ~110 ops.
- **Reminder parked:** **#1 stub-Akteur** (15 no-archive-match + 2 multi-file) and **#2 stub-Projekt** (now 23, after Circle House promotion) — still on the worklist.
- **Contract drift cleanup** — add the 2 new labels + 6 new rel types to the contract schemas (small commit, no apply needed).
