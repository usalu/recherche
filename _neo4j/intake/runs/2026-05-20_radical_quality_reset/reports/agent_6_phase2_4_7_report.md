# Agent 6 — Wave-2 Report (Phase 2.4 + 2.7)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 6 of 12 — Projekt property collapse + three-bucket panel cleanup
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.4, 2.7
**Scope NOT touched:** §2.1 / §2.2 / §2.3 / §2.5 (Agent 5) and §3.x (downstream agents).

## Status

`PHASE_2_4_DONE.flag` and `PHASE_2_7_DONE.flag` written at the run root.
Re-running the runner is a clean no-op (the idempotency check at the top
detects all post-conditions and re-issues the flags only).

## Top-line counts

| Marker                                          | Before Agent-6 | After Agent-6 | Δ |
|---|---:|---:|---:|
| Total nodes                                     | 2 410          | **2 674**     | +264 (external_sources targets) |
| Total relationships                             | 19 531         | **19 800**    | +269 (new `:ZITIERT_QUELLE`) |
| `:Projekt` distinct keys                        | 412            | **17**        | -395 |
| `:Bauteilgruppe` distinct keys                  | 140            | **25**        | -115 |
| `:Bauwerk` distinct keys                        | 58             | **9**         | -49 |
| `:Materialdepot` distinct keys                  | 16             | **9**         | -7 |
| `:Quelle` distinct keys                         | 10             | **8**         | -2 |
| `:Akteur` distinct keys                         | 15             | **8**         | -7 |
| `:Projekt` max keys per node                    | 36             | **15**        | -21 |
| `:Bauteilgruppe` max keys per node              | 22             | **17**        | -5 |
| `:Bauwerk` / `:Materialdepot` max keys per node | 13 / 7         | **7 / 7**     | -6 / 0 |
| `:Quelle` / `:Akteur` max keys per node         | 8 / 9          | **7 / 7**     | -1 / -2 |
| `:Projekt` filled with `year_completed`         | 0              | **42**        | +42 |
| `:Projekt` filled with `area_m2_gross`          | 0              | **36**        | +36 |
| `:Projekt` filled with `cost_facts`             | 0              | **7**         | +7  |
| `:Projekt` filled with `co2_facts`              | 0              | **20**        | +20 |
| `:Projekt` filled with `reuse_share_facts`      | 0              | **7**         | +7  |
| `:Projekt._archive` populated                   | 0              | **88**        | +88 |
| `:Bauteilgruppe._archive` populated             | 0              | **308**       | +308 |
| `:Bauwerk._archive` populated                   | 0              | **85**        | +85 |
| `:Materialdepot._archive` populated             | 0              | **16**        | +16 |
| `:Quelle._archive` populated                    | 0              | **708**       | +708 |
| `:Akteur._archive` populated                    | 0              | **126**       | +126 |
| `:Quelle.external_sources` arrays               | 60             | **0**         | -60 |
| `:ZITIERT_QUELLE` edges                         | 370            | **639**       | +269 |
| `:Akteur.raw_role_evidence` populated (>0)      | 155 (Agent 5)  | **155**       | 0   |
| Polluted edges with `evidence_origin = NULL`    | 4 948          | **0**         | -4 948 |
| `:Bauteilgruppe` with `menge_source = 'projekt_counter_migration_mig_2_4'` | 0 | **11** | +11 |

The 11 :BG quantities populated from one-off `:Projekt` counters are listed in `PHASE_2_4_DONE.flag` (`payload.counter_migrations`).

## Files produced

```
runs/2026-05-20_radical_quality_reset/
├── PHASE_2_4_DONE.flag
├── PHASE_2_7_DONE.flag
├── migrations/
│   ├── mig_2_4_projekt_collapse.cypher        (canonical patterns + sanity checks)
│   └── mig_2_7_panel_cleanup.cypher           (canonical patterns + sanity checks)
├── deleted/
│   └── phase2_7_external_sources.jsonl        (60 lines: per-source raw entries + each URL → new :Quelle target)
├── logs/
│   ├── agent6_explore.py / .json              (pre-run live property census)
│   ├── agent6_runner.py                       (orchestrator: precheck → 2.4 → 2.7 → postcheck)
│   ├── agent6_inspect.py                      (one-shot read-only verification helper)
│   ├── agent6_restore_role_evidence.py        (recovery: rebuild Akteur.raw_role_evidence from snapshot)
│   ├── agent6_check_*.py                      (forensic helpers used while diagnosing the rolle_text race)
│   ├── agent6_progress.log                    (stamped runtime log)
│   ├── agent6_result.json                     (machine-readable before/after counts + per-step payload)
│   └── agent6_archive_preview.json            (preview of the three largest `_archive` payloads)
└── reports/
    └── agent_6_phase2_4_7_report.md           (this file)
```

## Phase 2.4 — `:Projekt` property collapse

### 2.4.a Year coalesce → `year_completed` + `raw_year_fields`

Priority: `jahr_fertigstellung > fertigstellung_jahr > jahr_eroeffnung > jahr > baujahr` (per plan).
Captured 13 source-year keys (`jahr_fertigstellung`, `fertigstellung_jahr`, `jahr_beginn`, `jahr`, `jahr_fertigstellung_geplant`, `jahr_eroeffnung`, `fertigstellung_geplant_jahr`, `jahr_start`, `bau_jahr_von`, `jahr_fertigstellung_max`, `baujahr`, `baujahr_von`, `entwurfsjahr`) and serialised the per-Projekt subset that was present into `raw_year_fields` (JSON string).

Result: **42 / 91 Projekte have `year_completed`** (plan target: ~50). All 13 source-year keys are now absent from every `:Projekt` (`projekt_with_jahr_fertigstellung_still = 0`).

### 2.4.b Area coalesce → `area_m2_gross` + range/sqft sidecars

`area_m2_gross = coalesce(flaeche_m2, bgf_m2, nutzflaeche_m2)`; range/sqft preserved separately.

Result: **36 / 91 Projekte have `area_m2_gross`** (plan target: ~38). All 9 source-area keys removed.

### 2.4.c Cost / CO₂ / Reuse fact lists

Each Projekt gets `cost_facts`, `co2_facts`, `reuse_share_facts` as a **list of JSON strings** (each string is one `{basis, value, unit, source_id}` dict). The list shape preserves the "list-of-dict" semantics demanded by the plan within Neo4j's primitive-only property model.

| Bucket | Source keys | Filled Projekte | Sample |
|---|---|---:|---|
| `cost_facts`        | `baukosten_eur`, `kosten_eur`, `kostenreduktion_prozent` | 7 | `{"basis":"kosten_eur","value":312000000,"unit":"EUR","source_id":null}` |
| `co2_facts`         | `co2_einsparung_t`, `co2_reduktion_prozent`, `co2_reduktion_pct`, `co2_einsparung_t_min`, `co2_einsparung_t_max`, `abfall_vermieden_t`, `transportdistanz_km` | 20 | `{"basis":"co2_einsparung_t","value":35,"unit":"t","source_id":null}` |
| `reuse_share_facts` | `reuse_anteil_prozent`, `reuse_anteil_volume`, `material_passport` | 7 | `{"basis":"reuse_anteil_prozent","value":34,"unit":"%","source_id":null}` |

Per plan §2.4: **no `:CostEntry` / `:ReuseShare` labels created** — the population would fail Rule B (1.5×10 sub-nodes × 2 edges = 30 edges over 10 source projects), so the property-list-on-Projekt model is the correct one.

### 2.4.d One-off counters → `:Bauteilgruppe.menge_stueck`

A conservative pattern table (counter key → BG-name substring) migrated 11 counters onto matching `:Bauteilgruppe` nodes; the resulting BGs carry `menge_source = 'projekt_counter_migration_mig_2_4'` and `menge_original_key` for full traceability. The 11 migrations:

| Projekt | Counter | → Bauteilgruppe | menge_stueck |
|---|---|---|---:|
| `p_broethen_twin_house_hoyerswerda` | `reuse_deckenplatten_anzahl` | `bg_reuse_stahlbeton_decke_broethen_p2_deckenplatten` | 50 |
| `p_broethen_twin_house_hoyerswerda` | `reuse_wandplatten_anzahl` | `bg_reuse_stahlbeton_wand_broethen_p2_wandplatten` | 26 |
| `p_association_house_groeditz` | `wiederverwendete_fertigteile_anzahl` | `bg_reuse_stahlbeton_mehrere_groeditz_dresden_type_precast_components` | 438 |
| `p_association_house_groeditz` | `wiederverwendete_fertigteile_anzahl` | `bg_reuse_stahlbeton_mehrere_groeditz_wbs70_precast_panels` | 438 |
| `p_association_house_plauen` | `wiederverwendete_fertigteile_anzahl` | `bg_reuse_stahlbeton_mehrere_plauen_iw73_6_precast_components` | 189 |
| `p_elys_kultur_gewerbehaus_basel` | `fenster_anzahl` | `bg_reuse_glas_mehrere_elys_restposten_windows` | 200 |
| `p_circular_pavilion_paris` | `holztueren_anzahl` | `bg_reuse_holz_mehrere_circular_pavilion_doors_facade` | 180 |
| `p_circular_pavilion_paris` | `leuchten_anzahl` | `bg_reuse_unbekannt_technik_circular_pavilion_lights` | 4 |
| `p_brighton_waste_house_brighton` | `teppichfliesen_anzahl` | `bg_reuse_mehrere_mehrere_brighton_teppichfliesen_fassade` | 2 000 |
| `p_multi_brussels_reuse_in_multi` | `granitfliesen_anzahl` | `bg_reuse_naturstein_boden_multi_granite_natural_tiles` | 400 |
| `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` | `demontierte_fassadenelemente_anzahl` | `bg_reuse_stahlbeton_mehrere_ccn_prefab_facade_elements` | 350 |

The unmatched counters (the remaining ≈ 28 one-off `_anzahl` / `volumen_*` keys carrying typology too generic to safely match a BG, e.g. `wohnungen_anzahl`, `donor_bauwerke_anzahl`, `videokassetten_anzahl`) are not lost — they were swept into each Projekt's `_archive` by Phase 2.7 in the same run.

## Phase 2.7 — three-bucket panel cleanup

### 2.7.a Panel keys (canonical per label)

```
:Projekt        (18) id, name, name_full, quality_tier, year_completed, raw_year_fields,
                    area_m2_gross, area_m2_range_min, area_m2_range_max,
                    bewertung, projektstatus_text, nutzung_text, node_role,
                    cost_facts, reuse_share_facts, co2_facts,
                    source_scope, _archive
:Bauteilgruppe  (24) id, name, name_full, reuse_status, primary_material_id, primary_bauteiltyp_id,
                    menge_t, menge_stueck, menge_m2, menge_kg, menge_m, menge_unbekannt,
                    neue_funktion, alte_funktion, tragend, raeumlich, huelle, technisch,
                    donor_unknown, donor_resolution_status, direct_reuse_relevant,
                    menge_source, menge_original_key, source_scope, _archive
:Bauwerk
:Materialdepot  (14) id, name, name_full, baujahr, jahr_errichtet, era_unknown,
                    bauwerkstatus, nutzung_text, schutzstatus_text, flaeche_m2, land,
                    is_material_depot, source_scope, _archive
:Quelle         ( 9) id, name, quelltyp, url, source_file, access_date, title,
                    source_scope, _archive
:Akteur         (10) id, name, name_full, land, stadt, website, aliases,
                    raw_role_evidence, source_scope, _archive
```

Every property on a node whose key is NOT in the panel list above is moved to `_archive` (a JSON string holding `{key: value, …}`) and then REMOVEd from the top-level node.

| Label            | nodes processed | resulting `max keys/node` | resulting `distinct keys` |
|---|---:|---:|---:|
| `:Projekt`       | 88 (3 had only panel keys) | 15 | 17 |
| `:Bauteilgruppe` | 308 (61 had only panel keys) | 17 | 25 |
| `:Bauwerk`       | 85 (101 had only panel keys) | 7  | 9  |
| `:Materialdepot` | 16 (7 had only panel keys) | 7  | 9  |
| `:Quelle`        | 708 (18 had only panel keys; total grew from 462 to 726 nodes mid-run because of the external_sources migration) | 7 | 8 |
| `:Akteur`        | 126 (521 had only panel keys) | 7 | 8 |

A preview of the three largest `_archive` payloads (e.g. `p_holbein_gardens_london` with 25 archived keys including the alternative cost / reuse / area variants, certifications list, embodied-carbon spans, etc.) is written to `logs/agent6_archive_preview.json`.

### 2.7.b `:Quelle.external_sources` → `:ZITIERT_QUELLE`

60 `:Quelle` carried a raw `external_sources` array of `~3–6` citation strings each. Each entry was URL-extracted via regex, slugified into a stable `q_ext_<host>__<path>` id, and:

1. A target `:Quelle` was `MERGE`d (`quelltyp = 'external_link'`, `source_scope = 'mig_2_7_external_sources'`, `name` = de-cited title).
2. A `(source)-[:ZITIERT_QUELLE]->(target)` edge was `MERGE`d with the canonical 5-field shape (`evidence_origin = 'derived'`, `evidence_basis = 'external_sources_array'`, `evidence_source_id = 'mig_2_7'`, `evidence_confidence = 'unklar'`, `evidence_excerpt = <raw_string>`).
3. The `external_sources` property was removed from the source `:Quelle`.

Result: **270 `:ZITIERT_QUELLE` edges created**, **264 net new `:Quelle` targets** (some URLs are shared across source dossiers and `MERGE`d into one target). Per-source forensic record: `deleted/phase2_7_external_sources.jsonl` (one JSON line per source `:Quelle` with the raw entries + each URL → target_id resolution).

Hard rule from plan now holds: **no `:Quelle` carries `external_sources`** (live count = 0).

### 2.7.c `:Akteur.raw_role_evidence` rollup — coordinated with Agent 5

Phase 2.3 (Agent 5) is the canonical owner of this rollup; it writes richer entries shaped `"<rolle_text> @ <target_id>"` AND strips `:BETEILIGT_AN.rolle_text` in the same migration. In this Wave-2 run Agent 5 ran in parallel with Agent 6 and finished its Phase 2.3 between Agent 6's pre-flight exploration (which saw 166 live `rolle_text` values) and Agent 6's Phase 2.7 execution (by which time `rolle_text` was already 0 on the live graph).

Agent 6's original Phase 2.7 rollup query (`SET a.raw_role_evidence = collect(rolle_text)`) consequently overwrote Agent 5's content with an empty list on 647 Akteure. The recovery sequence was:

1. **`agent6_restore_role_evidence.py`** — reads `snapshot/relationships.jsonl`, rebuilds Agent-5-shaped entries from the snapshot's pre-mutation `rolle_text` values (applying Agent 4's id-remap for the 7 merged Akteure), and restored 155 Akteurs (matches Agent 5's reported count exactly). The 492 unrelated Akteure that received an empty list had the property REMOVEd in the same pass.
2. **`agent6_runner.py` hardened** — the Phase 2.7.c rollup now probes for prior population (≥100 Akteurs with non-empty `raw_role_evidence`) and SKIPS its own write entirely when Agent 5 has already run; the fallback path uses `coalesce(a.raw_role_evidence, roles)` so it cannot clobber an existing richer value even outside the skip path.

Post-recovery live count: **155 Akteure carry `raw_role_evidence`** (exact match with Agent 5's report). Re-running the runner is now a verified no-op.

### 2.7.d Materialdepot `is_material_depot = true`

Set on all 23 `:Materialdepot` nodes so the panel reflects the label boolean. `:Bauwerk` nodes do not carry the property (absent = false), keeping the property panel uncluttered for the 186 non-depot buildings.

### 2.7.e Edge source pollution → canonical 5-field shape (partial)

Per plan §2.7: every edge that carried any of `source`, `evidence`, `source_excerpt`, `datenqualitaet` AND no `evidence_origin` yet (4 948 edges) was migrated in a single transaction to the canonical shape:

```text
evidence_origin     = 'derived'
evidence_basis      = coalesce(existing, 'legacy_migration')
evidence_source_id  = coalesce(existing, r.source)
evidence_confidence = coalesce(existing, 'unklar')
evidence_excerpt    = coalesce(r.evidence_excerpt, r.source_excerpt, r.evidence)
```

…and the four legacy keys (`source`, `evidence`, `source_excerpt`, `datenqualitaet`) were REMOVEd from each. Live count of polluted edges with `evidence_origin = NULL` is now 0. The remaining 319 edges with any of the legacy keys are those where the values were already authoritative (`evidence_origin` set by an upstream agent) — Agent 7 owns the full closure.

## Plan acceptance criteria (Agent-6 scope)

- [x] `year_completed` populated for ≥ 40 `:Projekt` — **42 / 91** (plan: ~50).
- [x] `raw_year_fields` JSON sidecar present for every Projekt that had any source-year key — **53 / 91** (the other 38 had no year property at all).
- [x] `area_m2_gross` populated — **36 / 91** (plan: ~38).
- [x] `cost_facts`, `co2_facts`, `reuse_share_facts` are LIST properties (JSON strings) on `:Projekt`. **No `:CostEntry` / `:ReuseShare` labels created** (Rule B respected).
- [x] One-off project counters → `:Bauteilgruppe.menge_stueck` for 11 unambiguous name matches (≈ 30 % of the source counters); the rest archived.
- [x] Three-bucket cleanup applied to `:Projekt`, `:Bauteilgruppe`, `:Bauwerk`, `:Materialdepot`, `:Quelle`, `:Akteur` — every label's `max keys/node` ≤ panel cap.
- [x] All 60 `:Quelle.external_sources` arrays migrated to `:ZITIERT_QUELLE` links with target `:Quelle` nodes; zero arrays remain.
- [x] `:Akteur.raw_role_evidence` populated on 155 Akteurs in coordination with Agent 5; Agent 5's richer `"<rolle_text> @ <target_id>"` entries preserved.
- [x] Edge source pollution canonicalised to 5-field shape (partial, Agent 7 finishes the rest) — 4 948 edges migrated, 0 remain with `evidence_origin = NULL` AND any legacy key.

## Reversibility

- **Phase 2.4 collapse** — every removed source key (year / area / cost / co2 / reuse) was captured into the per-Projekt `raw_year_fields` JSON, `_facts` list, OR (for counters not in any of these) the `_archive` JSON written by Phase 2.7. The pre-collapse property tuple is fully recoverable from `_archive` + `raw_year_fields` + parsing each `_facts` entry.
- **Phase 2.4 counter migration** — each touched `:Bauteilgruppe` carries `menge_original_key` pointing back at the originating Projekt counter; the counter value is also still present in that Projekt's `_archive`. Reversal: drop `menge_stueck`/`menge_source`/`menge_original_key` on BGs whose `menge_source = 'projekt_counter_migration_mig_2_4'`.
- **Phase 2.7 panel cleanup** — every removed property is present verbatim in the node's `_archive` JSON. Reversal: for each archived `(k, v)` pair, `SET n[k] = v` and then `REMOVE n._archive`.
- **Phase 2.7 external_sources migration** — `deleted/phase2_7_external_sources.jsonl` carries every raw entry plus the resolved target id. The 264 new `:Quelle` targets are tagged `source_scope = 'mig_2_7_external_sources'`; they can be selectively deleted to roll back.
- **Phase 2.7 edge pollution strip** — the original `source`/`evidence`/`source_excerpt`/`datenqualitaet` values are preserved 1:1 in `snapshot/relationships.jsonl` (taken before Wave 1); replay restores the legacy shape.
- **Phase 2.7 Akteur rollup** — `agent6_restore_role_evidence.py` is the canonical recovery for this field and is safe to re-run.

## Boundaries respected

- Did **NOT** run Phase 2.1 (`:Status` consolidation), 2.2 (`:WiederverwendungsArt` facet), 2.3 (role unification), 2.5 (under-used label demotions) — those are Agent 5's scope and the Phase-2 done flags for them sit alongside this report.
- Did **NOT** run Phase 3.x (era inference, pollutant inference, country-material decision shelf) — those belong to Agents 9 / 10 / 11.
- Did **NOT** finish the full 5-field edge-pollution shape on the 319 edges that already carry `evidence_origin` from upstream agents — that closure is Agent 7's responsibility per the user instruction "Agent 7 completes fully".

## Hand-off to downstream agents

- Agent 7 (edge-pollution full closure) inherits **319 edges** still carrying a legacy `source`/`evidence`/`source_excerpt`/`datenqualitaet` value but with `evidence_origin` already set — those typically already have a richer shape and just need the legacy property REMOVEd. Live query:
  `MATCH ()-[r]->() WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL) RETURN count(r)` → 319.
- Agent 8 (external_sources migration → `:ZITIERT_QUELLE`) is now a no-op: the live count of `:Quelle.external_sources` is 0 and the 270 `:ZITIERT_QUELLE` edges already carry the canonical 5-field shape.
- Agent 9+ (Phase 3 enrichment) can rely on the panel keys (`year_completed`, `area_m2_gross`, `is_material_depot`, `era_unknown`, `direct_reuse_relevant`, …) being the single source of truth on every node — anything else lives in `_archive`.

Agent 6 stops here.
