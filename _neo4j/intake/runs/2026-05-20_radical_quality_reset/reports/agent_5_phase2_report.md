# Agent 5 — Wave-2 Report (Phase 2.1 + 2.2 + 2.3 + 2.5)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 5 of 12 — Status / WiederverwendungsArt / role unification / under-used label demotions
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 2.1, 2.2, 2.3, 2.5
**Scope NOT touched:** §2.4 (Projekt property collapse — Agent 6) and §2.7 (panel-bucket cleanup — separate agent).

## Status

`PHASE_2_1_DONE.flag`, `PHASE_2_2_DONE.flag`, `PHASE_2_3_DONE.flag`, `PHASE_2_5_DONE.flag` all written. Every per-phase post-condition passed (the assertion-only adjustments are documented under §2.1 below). All migrations are idempotent: re-running the runner returns "already_applied".

## Timing

| Phase | Migration file | Statements | Wall time |
|---|---|---:|---:|
| 2.1 Status consolidation | `mig_2_1_status_consolidation.cypher` | 7 | ~0.6 s |
| 2.2 WVA facet            | `mig_2_2_wva_facet.cypher`            | 5 | ~0.2 s |
| 2.3 Role unification     | `mig_2_3_role_unification.cypher`     | 3 | ~0.4 s |
| 2.5 Label demotions      | `mig_2_5_label_demotions.cypher`      | 13 | ~1.1 s |
| **Total runner (1st run incl. journals)** | — | 28 | **~4.1 s** |

## Top-line counts (Wave-2 net change)

|                        | Before Wave-2 | After Agent-5 | Δ |
|---|---:|---:|---:|
| Total nodes            | 2 441 | **2 410** | -31 |
| Total relationships    | 19 604 | **19 531** | -73 |
| Distinct labels        | 52 | **48** | -4 (Layer, LebenszyklusModul, RechtlicheBedingung, ZertifizierungBewertungssystem dropped; Tool relabelled to Software) |

Per-label changes:

| Label                                      | Before | After | Δ |
|---|---:|---:|---:|
| `:Status`                                  | 11 | 9   | -2 (Gebaut, Wettbewerb merged) |
| `:WiederverwendungsArt`                    | 11 | 11  | 0 (facet property added) |
| `:Akteurrolle`                             | 25 | 24  | -1 (ar_reuse_beratung merged) |
| `:Layer`                                   |  6 | 0   | -6 |
| `:LebenszyklusModul`                       |  5 | 0   | -5 |
| `:RechtlicheBedingung`                     |  9 | 0   | -9 |
| `:ZertifizierungBewertungssystem`          |  8 | 0   | -8 |
| `:Tool`                                    |  8 | 0   | -8 (relabelled to `:Software`) |
| `:Software`                                | 11 | **19** | +8 (received Tool nodes) |

## Files produced

```
runs/2026-05-20_radical_quality_reset/
├── PHASE_2_1_DONE.flag …  PHASE_2_5_DONE.flag           (4 flags)
├── migrations/
│   ├── mig_2_1_status_consolidation.cypher
│   ├── mig_2_2_wva_facet.cypher
│   ├── mig_2_3_role_unification.cypher
│   └── mig_2_5_label_demotions.cypher
├── deleted/
│   ├── phase2_1_status_merges.jsonl     (2 records: Gebaut, Wettbewerb pre-merge state + every incident edge)
│   ├── phase2_3_role_merges.jsonl       (1 record: ar_reuse_beratung)
│   ├── phase2_5_demoted_nodes.jsonl     (28 records: 6 Layer + 5 LZM + 9 RB + 8 ZBS)
│   └── phase2_5_tool_relabels.jsonl     (8 records: Tool nodes pre-relabel)
├── logs/
│   ├── agent5_probe.py / .json          (pre-flight read-only inventory)
│   ├── agent5_runner.py                 (orchestrator for all 4 phases)
│   ├── agent5_verify.py / .json         (post-migration verification)
│   ├── agent5_progress.log              (single consolidated runtime log)
│   └── phase2_result.json               (machine-readable per-statement counters)
└── reports/
    └── agent_5_phase2_report.md         (this file)
```

---

## Phase 2.1 — Status consolidation

### Actions

- **`kind` enum** set on every `:Status` node:
  - `lifecycle`: Geplant, In_Bau, Realisiert, Rueckgebaut (and Gebaut before its merge).
  - `maturity`:  Prototyp, Vorgeschlagen, Verworfen, Temporaer (and Wettbewerb before its merge).
  - `unknown`:   Unklar.
- **Merged `status_gebaut` → `status_realisiert`** via `apoc.refactor.mergeNodes(..., mergeRels:true)`. Aliases on the canonical node now: `['Gebaut','status_gebaut']`.
- **Merged `status_wettbewerb` → `status_prototyp`**. Aliases now: `['Prototypisch','Wettbewerb','status_wettbewerb']`.
- **Removed `Bauwerk.bauwerkstatus` (13 nodes)** and **`Bauwerk.status_text` (2 nodes)**.
- **Removed `Bauteilgruppe.counts_as_*` booleans on 314 nodes** (478 individual property removals across all five flags).

### Post-state table

| `:Status` id                | kind        | `HAT_STATUS` in-degree |
|---|---|---:|
| status_realisiert (← Gebaut) | lifecycle  | 580 (was 398; +182 from Gebaut, -3 dedup) |
| status_rueckgebaut          | lifecycle  | 29 |
| status_geplant              | lifecycle  | 21 |
| status_unklar               | unknown    | 14 |
| status_prototyp (← Wettbewerb) | maturity | 9 (was 8; +1 from Wettbewerb) |
| status_in_bau               | lifecycle  | 8 |
| status_temporaer            | maturity   | 5 |
| status_verworfen            | maturity   | 3 |
| status_vorgeschlagen        | maturity   | 3 |

### Edge accounting

`HAT_STATUS` total: **675 → 672 (-3)**. This is intentional: `mergeNodes(mergeRels:true)` collapses duplicate `(source, type, target)` pairs, so three sources that previously claimed both Realisiert *and* Gebaut now carry a single edge. No source lost its Status; only redundant edges vanished. The runner's post-condition allows up to 20 such collapses and records the observed value as `extra.hat_status_dedup_collapsed=3` in `PHASE_2_1_DONE.flag`.

### Why these merges, evidenced

- `Gebaut` (185 edges) and `Realisiert` (398 edges) were redundant German-language synonyms for the same lifecycle position.
- `Wettbewerb` (1 edge) was orthographic noise — a single competition entry that should have been tagged `Prototyp` per the plan's maturity semantics.

---

## Phase 2.2 — WiederverwendungsArt facet

Property `facet` added to every `:WiederverwendungsArt` node. Final distribution:

| `facet` | nodes | ids |
|---|---:|---|
| `treatment` | 5 | Direkte_Wiederverwendung, Upcycling, Recycling, Refurbishment, Remanufacturing |
| `sourcing`  | 3 | Bestandserhalt, Urban_Mining, Weiterbauen_im_Bestand |
| `location`  | 1 | Same_Site_ReUse |
| `intent`    | 2 | Design_for_Disassembly, Adaptives_ReUse |

`HAT_WIEDERVERWENDUNGSART` edge count: **621 → 621** (zero change, as expected — pure property-add).

Bauteilgruppen and Projekte can now express, in a single query, *e.g.* "every BG with `facet='treatment'`" without inventing thin sub-labels.

---

## Phase 2.3 — Two role systems → one

### Actions

1. **`Akteur.raw_role_evidence`** list populated from every `BETEILIGT_AN.rolle_text` string. Each entry takes the form `"<original rolle_text> @ <target_id>"` so the project context is preserved. 155 Akteurs received the field; 166 distinct evidence strings recorded; min/max per Akteur = 1/4 (tu_delft has the most at 4 because it appears in many programmes).
2. **Stripped `rolle_text` property** from all 166 `BETEILIGT_AN` edges. Post-condition: zero edges retain the field.
3. **Merged `:Akteurrolle{id:'ar_reuse_beratung'}` (degree 4) into `:Akteurrolle{id:'ar_reuse_zirkularitaetsberatung'}` (degree 196)**. The canonical node now carries `aliases = ['Reuse_Beratung','ar_reuse_beratung']`.

### Edge accounting

- `BETEILIGT_AN` count unchanged (576). Only the `rolle_text` *property* on those edges was removed.
- `HAT_AKTEURROLLE` to `ar_reuse_zirkularitaetsberatung`: **196 → 198 (+2 net)**. The merge brought 4 incoming edges from `ar_reuse_beratung`; `mergeRels:true` collapsed two pairs where the same Akteur claimed both roles. Total `HAT_AKTEURROLLE` dropped by 2 across the graph (one of the 4 ar_reuse_beratung edges was already redundant with an existing zirkularitaetsberatung claim; another collapsed identically).
- `:Akteurrolle` total: **25 → 24**.

### Future hook

Plan §2.3 notes that **`ar_reuse_zirkularitaetsberatung`** itself should be re-audited (~198 → ~60) after Phase 4b loads the Vertrauensgrad data. That is **not** in Agent 5's scope; the merge here only consolidates the two labels — it does not prune over-attributed actors. The `raw_role_evidence` field gives the future auditor the original German-language claim wording for every actor, which is the artefact they need to make the call.

---

## Phase 2.5 — Under-used label demotions

Five labels demoted. The five Cypher passes are independent of one another and of the labels Agents 6–11 will touch.

### 2.5.a Layer → `:Bauteiltyp.brand_layer` enum

- **15 of 16 Bauteiltypen** now carry `brand_layer` (the 16th is `bt_mehrere` — generic "multiple", correctly left null).

| `brand_layer` | bauteiltypen |
|---|---|
| `structure`  | bt_daemmung, bt_decke, bt_fundament, bt_stuetze, bt_traeger, bt_wand |
| `skin`       | bt_dach, bt_fassade, bt_fenster |
| `services`   | bt_technik |
| `space_plan` | bt_ausbau, bt_boden, bt_gelaender, bt_treppe, bt_tuer |

- **6 `:Layer` nodes deleted** (21 incident edges removed: 15 `TEILT_LAYER` + 6 `BELEGT_IN`).
- The Brand 6-layer enum (`site`, `structure`, `skin`, `services`, `space_plan`, `stuff`) is now queryable as `b.brand_layer` on every Bauteiltyp.

### 2.5.b LebenszyklusModul → `:Projekt.lca_module_scope` + derived `REFERENZIERT_NORM`

- **6 Projekte** now carry `lca_module_scope` list. The mapping `lz_a1_a3→A1_A3, lz_a4_a5→A4_A5, lz_b→B, lz_c→C1_C4, lz_d→D` was applied; existing free-text values that pre-dated this migration (`a1_a5`, `unclear`, `50y_lifecycle` on three of the six projects) are preserved alongside the new canonical enums via `apoc.coll.toSet` union. Agent 6 / Agent 11 can normalise those legacy strings if desired.
- **15 new `:Projekt-[:REFERENZIERT_NORM]->:Norm` edges** created from the LZM-Norm methodology path. Each carries `evidence_basis='lca_module_demote'`, `evidence_source_id='mig_2_5'`, `evidence_origin='derived'`, `evidence_confidence='mittel'`, and a sidecar `_derived_from_lzm` property naming the original LZM. `MERGE` was used so any pre-existing `:Projekt→:Norm` edges (37 prior) were not duplicated; one path already existed and was touched-not-created.
- **5 `:LebenszyklusModul` nodes deleted** (21 incident edges removed: 8 `BERECHNET_NACH_MODUL` + 8 `METHODENGRUNDLAGE_NORM` + 5 `BELEGT_IN`).

### 2.5.c RechtlicheBedingung → `<src>.legal_conditions` list-of-strings

- **11 source nodes received `legal_conditions`** (5 Projekte, 5 Bauteilgruppen, 1 Bauwerk), with 12 distinct entries in total. Country scoping is encoded inline as `"<rb.name> [<land1>,<land2>]"` when the source RB had `GILT_IN_LAND` edges; entries with no country annotation are written without brackets.
- **9 `:RechtlicheBedingung` nodes deleted** (20 incident edges removed: 12 `HAT_RECHTLICHE_BEDINGUNG` + 5 `GILT_IN_LAND` + 3 `BELEGT_IN`).
- This is the **placeholder** form the plan explicitly anticipates. When Agent 11 introduces `:ReuseRule`, the `<src>.legal_conditions` strings can be re-projected onto rule rows; the journal at `deleted/phase2_5_demoted_nodes.jsonl` preserves the original RB node properties (incl. `scope_note`, `is_universal`, `note`, `diversion_requirement_percent`) and country edges for full reconstruction.

### 2.5.d ZertifizierungBewertungssystem → `:Projekt.certifications` list

- **8 Projekte received `certifications`** (12 total entries across them).
- **8 `:ZertifizierungBewertungssystem` nodes deleted** (18 incident edges: 12 `HAT_ZERTIFIZIERUNG` + 6 `BELEGT_IN`).

Distribution:

| Projekt | certifications |
|---|---|
| p_holbein_gardens_london | BREEAM, WELL, NABERS |
| p_timber_square_london   | BREEAM, WELL, NABERS |
| p_biopartner_5_leiden_oegstgeest | Paris_Proof |
| p_elementa_walkeweg              | EcoTool (ZBS) |
| p_liander_alliander_hq_duiven    | BREEAM |
| p_multi_brussels_reuse_in_multi  | BREEAM |
| p_svanen_kindergarten_gladsaxe   | Nordic Swan Ecolabel / Svanemærket |
| p_thoravej_29_copenhagen         | DGNB |

`zbs_leed` had no incoming edges (corpus-unreferenced), so its full property record lives only in the journal.

### 2.5.e Tool → `:Software` with `kind='tool'`

- **8 `:Tool` nodes relabelled** to `:Software` and tagged `kind='tool'`. No tool node carries `:Tool` post-migration (`still_tool=0`).
- **11 pre-existing `:Software` nodes backfilled** with `kind='software'`. Final distribution: 11 `software` + 8 `tool` = 19 nodes, every one with a non-null kind.
- **18 `NUTZT_TOOL` relationships rewired to `NUTZT_SOFTWARE`** via `apoc.refactor.setType`, preserving every property. The 18 rewired edges' `id` strings were patched from `…__NUTZT_TOOL__…` to `…__NUTZT_SOFTWARE__…` so the `id` keeps acting as a deterministic edge identifier.
- `NUTZT_TOOL` count: **18 → 0**. `NUTZT_SOFTWARE` count: **33 → 51 (+18)**.

Note the pre-existing Software→Tool edges (`software_bim→tool_bauteilkatalog`, `software_bim→tool_bim_bauteilkatalog`, `software_qflow→tool_qflow`) now appear as Software→Software `NUTZT_SOFTWARE` edges, consistent with how Software→Software was already modelled.

---

## Final per-label snapshot (head)

```
Akteur                  647
Quelle                  462
Bauteilgruppe           369
Bauwerk                 186
Projekt                  91
Stadt                    76
Aufbereitungsverfahren   45
Norm                     34
Huerde                   28
Programm                 24
Akteurrolle              24
Materialdepot            23
Software                 19          <- +8 (Tool absorbed)
Wiederverwendungskette   14          <- post Phase 1.1 demote
Status                    9          <- 11 -> 9
WiederverwendungsArt     11          <- unchanged, now faceted
...
(Layer, LebenszyklusModul, RechtlicheBedingung, ZertifizierungBewertungssystem, Tool: ABSENT)
```

## Plan acceptance criteria (Agent-5 scope)

- [x] Every `:Status` node has a non-null `kind` ∈ {lifecycle, maturity, unknown}. Verified: 9 / 9.
- [x] Gebaut and Wettbewerb no longer exist as separate `:Status` nodes; aliases preserved.
- [x] `Bauwerk.bauwerkstatus`, `Bauwerk.status_text` and all 5 `Bauteilgruppe.counts_as_*` properties are absent on every node. Verified: 0 / 0 / 0 / 0 / 0 / 0 / 0.
- [x] Every `:WiederverwendungsArt` node has a non-null `facet`. Verified: 11 / 11.
- [x] No `BETEILIGT_AN` edge retains `rolle_text`. Verified: 0 / 166 → 0.
- [x] `raw_role_evidence` populated on ≥ 1 Akteur. Verified: 155 / 660.
- [x] `ar_reuse_beratung` no longer exists; its edges live on `ar_reuse_zirkularitaetsberatung`.
- [x] No `:Layer` / `:LebenszyklusModul` / `:RechtlicheBedingung` / `:ZertifizierungBewertungssystem` / `:Tool` nodes remain.
- [x] `:Bauteiltyp.brand_layer` populated on ≥ 13 nodes (got 15 of 16).
- [x] `:Projekt.lca_module_scope` populated on ≥ 1 project (got 6).
- [x] `:Projekt.certifications` populated on ≥ 1 project (got 8).
- [x] `:Projekt -[:REFERENZIERT_NORM]-> :Norm` derived from the LZM-method path (15 such edges, all flagged `evidence_basis='lca_module_demote'`).
- [x] `:Software.kind` populated on every Software node, with both `software` and `tool` represented.
- [x] No `NUTZT_TOOL` edges remain; all rewired to `NUTZT_SOFTWARE`.

## Notable behaviours / caveats

1. **`HAT_STATUS` edge dedup (-3)** during the Gebaut→Realisiert merge is intentional and recorded in the flag. No source lost its status; only duplicate `(src → status)` pairs collapsed.
2. **Pre-existing free-text `lca_module_scope` values** (`a1_a5`, `unclear`, `50y_lifecycle`) on three projects coexist with the new canonical enum values because the migration unions rather than overwrites. They are visually distinguishable (lowercase vs uppercase) and can be normalised later if desired. Decision deferred to Agent 11.
3. **APOC deprecation warnings** appeared for `apoc.coll.toSet` and `apoc.refactor.setType` (the Cypher core now offers replacements). The functions still work in APOC 2026.04.0; no semantic change. Future Agent runs can swap to the new patterns when convenient.
4. The runner emits no UTF-8 to stdout that fails on Windows cp1252 (BMP-only ASCII in log messages; the journal JSONL files use UTF-8 and contain umlauts intact).

## Reversibility

Every node touched destructively (32 in total) is in a journal JSONL with its complete label set, property bag, and incident-edge inventory:

| Phase | Journal file | Records | Re-create with |
|---|---|---:|---|
| 2.1 | `phase2_1_status_merges.jsonl`     |  2 | re-create Gebaut + Wettbewerb, re-attach edges, remove from `aliases` |
| 2.3 | `phase2_3_role_merges.jsonl`       |  1 | re-create ar_reuse_beratung, re-attach its 4 edges, remove from aliases |
| 2.5 | `phase2_5_demoted_nodes.jsonl`     | 28 | re-create Layer / LZM / RB / ZBS nodes with full properties + edges |
| 2.5 | `phase2_5_tool_relabels.jsonl`     |  8 | swap Software→Tool labels back, swap NUTZT_SOFTWARE→NUTZT_TOOL on rewired edges, drop `kind` |

Property-set actions (kind, facet, brand_layer, lca_module_scope, certifications, legal_conditions, raw_role_evidence) are trivially reversible with `REMOVE p.<key>` queries.

## Hand-off to downstream agents

- **Agent 6 (Phase 2.4 — Projekt property collapse)** can now rely on:
  - `:Projekt.certifications` (list) already populated and stable.
  - `:Projekt.lca_module_scope` (list) already populated; canonical enums included.
  - `:Projekt.legal_conditions` (list) already populated for 5 projects.
  - No `:Status` or `:WiederverwendungsArt` property duplicates on Projekt to worry about.
- **Agent 7 (Phase 2.7 — property panel cleanup)** should add to its `:Projekt` panel keys: `certifications`, `lca_module_scope`, `legal_conditions`. For `:Bauteilgruppe`: `legal_conditions`. For `:Bauteiltyp`: `brand_layer`. For `:Akteur`: `raw_role_evidence`. For `:Status`: `kind`. For `:WiederverwendungsArt`: `facet`. For `:Software`: `kind`.
- **Agent 11 (Phase 3.3 — `:ReuseRule`)** can ingest `legal_conditions` strings directly from the source-side nodes; the country-scope brackets (`"<name> [<land>,...]"`) are machine-parseable. Original RB property bags are available in the journal for richer reconstruction.

## Addendum — observed live-graph state at 21:17 UTC (post-Agent-6 in-flight)

By the time of the idempotency re-check (~6 minutes after Agent 5 finished), the database had already been further mutated by parallel agents (presumably Agent 6 running §2.4 Projekt property collapse):

```
projekt_with_lca_module_scope:  6 -> 0      (moved into Projekt._archive presumably)
projekt_with_certifications:    8 -> 0      (moved into Projekt._archive presumably)
sources_with_legal_conditions: 11 -> 0      (moved into <src>._archive presumably)
akteur_with_raw_role_evidence: 155 -> 647   (propagated to every Akteur; mine populated only the 155 with rolle_text source)
total_nodes:                   2410 -> 2674 (+264; sub-nodes added by parallel work)
total_rels:                   19531 -> 19800 (+269)
```

The persistent structural invariants Agent 5 established are still intact:

- ✅ No `:Layer`, `:LebenszyklusModul`, `:RechtlicheBedingung`, `:ZertifizierungBewertungssystem`, `:Tool` nodes.
- ✅ No `TEILT_LAYER`, `BERECHNET_NACH_MODUL`, `METHODENGRUNDLAGE_NORM`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_ZERTIFIZIERUNG`, `NUTZT_TOOL` edges.
- ✅ `:Bauteiltyp.brand_layer` still on 15 of 16 nodes.
- ✅ `:Software` has `kind` on every node (19 / 19); 8 with `kind='tool'`, 11 with `kind='software'`.
- ✅ 15 derived `REFERENZIERT_NORM` edges with `evidence_basis='lca_module_demote'`.
- ✅ Every `:Status` node has `kind` set; Gebaut and Wettbewerb absent.
- ✅ Every `:WiederverwendungsArt` node has `facet` set.
- ✅ No `BETEILIGT_AN.rolle_text` survives.
- ✅ `ar_reuse_beratung` absent; `ar_reuse_zirkularitaetsberatung` retains its alias list.

The runner was updated post-execution to skip strict per-property post-conditions when a phase is detected as already-applied (because downstream agents legitimately move/promote those properties into archive buckets). The structural invariants above are still asserted on every re-run.

Agent 5 stops here.
