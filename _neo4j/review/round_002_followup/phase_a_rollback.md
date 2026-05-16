# Phase A — apply summary + rollback procedure

**Applied:** 2026-05-16
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
├── phase_a_rollback.md                (this file)
├── patches/
│   └── phase_a.patch.jsonl             (102 records, idempotent)
└── apply_reports/
    └── phase_a.patch.apply_report.json (full record of what happened)

_neo4j/review/backups/
└── phase_a_pre_apply/                  (full graph state before Phase A)
    ├── backup_manifest.json
    ├── checksums.sha256
    ├── counts.json
    ├── live_graph.backup.jsonl         (2147 nodes + 15834 rels)
    └── schema_snapshot.json
```

## What's next

Phase A complete. Phase B/C/D are queued in [reuse_schema_proposals.md](reuse_schema_proposals.md). Recommended next step is **Phase B** (P-15 Bauproduktstatus + P-16 new Norm hubs incl. CEN/TS 1090-201), ~60 ops, same safe-apply pattern.

Reminders parked: **#1 stub-Akteur** (15 no-archive-match + 2 multi-file) and **#2 stub-Projekt** (24 promote-or-drop) — still on the worklist.
