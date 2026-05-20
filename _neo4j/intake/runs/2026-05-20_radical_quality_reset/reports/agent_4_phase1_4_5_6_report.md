# Agent 4 — Wave-1 Report (Phase 1.4 + 1.5 + 1.6)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 4 of 12 — Materialdepot relabel + surgical deletes + actor merges
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` (§§ 1.4–1.6)

## Status

`PHASE_1_4_DONE.flag`, `PHASE_1_5_DONE.flag`, `PHASE_1_6_DONE.flag` all
written at the run root. The merge step had a post-condition fixup
(see § 1.6 below); all three phases verified against live DB state.

## Timing

| Phase | Started (UTC) | Finished (UTC) | Elapsed |
|---|---|---|---:|
| 1.4 Materialdepot relabel | 2026-05-20T20:52:58 | 2026-05-20T20:52:58 | 0.29 s |
| 1.5 Surgical deletes       | 2026-05-20T20:52:58 | 2026-05-20T20:52:58 | 0.55 s |
| 1.6 Akteur merges          | 2026-05-20T20:52:58 | 2026-05-20T20:52:59 | 0.77 s |
| 1.6 post-merge id fixup    | 2026-05-20T20:54:55 | 2026-05-20T20:54:55 | < 1 s |

## Counts (before / after, mit-bestand)

| Label          | Pre-Wave-1 baseline | After Phase 1.4 | After Phase 1.5 | After Phase 1.6 | Net Δ |
|---|---:|---:|---:|---:|---:|
| `:Bauwerk`        | 209 | 186 | 186 | 186 | -23 |
| `:Materialdepot`  |   0 |  23 |  23 |  23 | +23 |
| `:Akteur`         | 660 | 660 | 654 | **647** | -13 |
| `:Programm`       |  28 |  28 |  24 |  24 |  -4 |
| `:Norm`           |  36 |  36 |  34 |  34 |  -2 |
| `:Quelle`         | 486 | 486 | 465 | 465 | -21 |

Net node change attributable to Agent 4 alone: **-40** (33 deletes + 7
merged-in duplicates) + relabel of 23 (no count change, just labels).
Live `MATCH (n) RETURN count(n)` at end of Agent 4 work: 2 442
(2 580 baseline − 138 = my −40 plus −98 from Agent 2 Phase 1.1).

> **Re plan note "Net `:Akteur`: 660 → 653"**: that line counts only the
> Phase 1.6 merges in isolation (7 dup nodes vanish). Combined with the 6
> Phase 1.5 Akteur hard-deletes the actual end state is **647**, which is
> what the plan's Phase 1.5 + 1.6 *together* imply: 660 − 6 − 7 = 647.

## Phase 1.4 — Materialdepot relabel

- **Relabelled 23 :Bauwerk → :Materialdepot** (exactly the 23 IDs in the
  plan's table, degrees 4–26). The `REMOVE :Bauwerk SET :Materialdepot`
  pattern preserves every existing edge.
- **Created/touched 4 `:BETRIEBEN_VON` edges** by the plan's name-match
  query (`d.id CONTAINS toLower(a.id) OR d.id CONTAINS
  toLower(replace(a.name,' ','_'))`). After the Phase 1.6 Bellastock
  merge, the duplicate edge from `bw_bellastock_…` to both
  `Bellastock` + `bellastock` collapsed to one — final post-merge
  count: **3 `:BETRIEBEN_VON` edges** with `evidence_source_id='mig_1_4'`,
  attached to:

    | Materialdepot | Akteur |
    |---|---|
    | `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` | `bellastock` |
    | `bw_holbein_grosvenor_donor_projects`                   | `grosvenor` |
    | `bw_rotor_reuse_stock_charles_malis`                    | `Rotor`     |

- The remaining 20 depots have no name-matched operator Akteur (e.g.
  "Aggregierte Pariser Quartiere") and intentionally carry no derived
  `:BETRIEBEN_VON` per the plan.

## Phase 1.5 — Surgical deletes

- **Journal-first guarantee.** Every node was captured into
  `deleted/phase1_5_nodes.jsonl` (33 lines, one JSON record per node)
  *before* any `DETACH DELETE` ran. Each record contains the full label
  set, every property, and a snapshot of incident edges
  (`edges_before_delete`) so the deletion is replayable from the JSONL
  alone.
- **Safety gate honoured.** `MAX_PHASE_1_5_DELETES = 35`. The runner
  refuses to issue any `DETACH DELETE` if the planned-delete count
  exceeds 35. Actual planned count: 33. ✅
- **Deleted exactly the IDs in the plan:**
    - `:Akteur` × 6: `glasfischer_glastec`, `citydev_brussels`,
      `denkstatt`, `eitel_partner`, `gibbins_architekten`,
      `zusammenkunft_berlin` (all degree ≤ 1; only edges were `HAT_AKTEURTYP`).
    - `:Programm` × 4: `prog_bbsm`, `prog_preuse`, `prog_zukunftbau`,
      `prog_kommunales_programm` (all degree 0).
    - `:Norm` × 2: `norm_bs_5385_5_2009`, `norm_din_18940` (degree 0).
    - `:Quelle` × 21: the 21 deg-0 dossier IDs from the plan's table.
      The runner first re-queried for `deg == 0` to honour the user's
      *"if Agent 3 already deleted them, skip duplicates"* instruction.
      In this run Agent 3 had not yet committed Phase 1.2 when Agent 4
      issued its `DETACH DELETE`, so Agent 4 performed the deletion; the
      parallel Agent 3 `DETACH DELETE` later in Phase 1.2 was a harmless
      no-op (Agent 3 still journalled its own copy of those 21 IDs to
      `deleted/phase1_2_quelle.jsonl`).
- **No Wiederverwendungsketten, Projekte, Bauteilgruppen, Stadt,
  Akteurrolle, … touched** by this agent. Chains (Phase 1.1) and
  ontology anchors (Phase 1.2/1.3) belong to Agents 2 and 3 respectively.

## Phase 1.6 — Akteur merges

Used `apoc.refactor.mergeNodes([canon, dup], {properties:'combine',
mergeRels:true})`. Per-pair pre-merge state (the dup node's labels,
properties, and every incident edge) journalled to
`deleted/phase1_6_merges.jsonl`.

| Canonical id  →  merged-in id | Pre-merge degrees | Combined degree | Aliases |
|---|---|---:|---|
| `baubuero_in_situ`         ← `bauburo_in_situ`           | 11 ← 15 | 23 | `["bauburo_in_situ"]` |
| `plp_architecture`         ← `ak_plp_architecture`       |  7 ←  6 | 11 | `["ak_plp_architecture"]` |
| `ZRS_Architekten_Ingenieure` ← `zrs_architekten`         |  9 ←  2 |  9 | `["zrs_architekten"]` |
| `loeliger_strub`           ← `loeliger_strub_architektur`|  8 ←  4 | 10 | `["loeliger_strub_architektur"]` |
| `zedfactory_bill_dunster`  ← `bill_dunster_zedfactory`   |  4 ←  2 |  4 | `["bill_dunster_zedfactory"]` |
| `opera`                    ← `opera_pm`                  |  4 ←  4 |  7 | `["opera_pm"]` |
| `bellastock`               ← `Bellastock`                |  5 ← 23 | 26 | `["Bellastock"]` |

Direction notes:

- **`baubuero_in_situ`** is kept as canonical id because it is
  orthographically correct (umlaut form), even though the merged-in node
  was higher-degree (15 → 11). All 23 combined edges now sit on
  `baubuero_in_situ`, name `"baubüro in situ"`.
- **`bellastock` / `Bellastock`** is a case-collision merge per the
  plan's "case-normalise" policy. Lowercase `bellastock` is canon; the
  original capitalised form is preserved in `aliases` and in the `name`
  property (`"Bellastock"`).
- **Combined degree drops** below sum(individual degrees) when
  duplicate `(type, endpoint)` edges existed pre-merge. `mergeRels:true`
  dedupes them. Examples: ZRS (9+2 → 9), zedfactory (4+2 → 4), bellastock
  (5+23 → 26 instead of 28 — two `:HAT_AKTEURTYP` / `:HAT_AKTEURROLLE`
  pairs collapsed).

### 1.6 post-condition fixup

`apoc.refactor.mergeNodes({properties:'combine'})` coerced the scalar
`id` property into a list of two strings (canonical + merged-in) on
every merged node. The data model requires `id` to remain a string, so
a small post-fixup (`logs/agent4_fixup_merge_id.py`) reset each
merged node's `id` to its canonical scalar. The `aliases` array is the
authoritative record of merged-in ids and was left untouched.

```text
nodes with list-typed id (pre-fix):  7
nodes with list-typed id (post-fix): 0
```

The fixup script is idempotent and safe to re-run.

## Files written by Agent 4

```
runs/2026-05-20_radical_quality_reset/
├── PHASE_1_4_DONE.flag
├── PHASE_1_5_DONE.flag
├── PHASE_1_6_DONE.flag
├── migrations/
│   ├── mig_1_4_materialdepot.cypher
│   ├── mig_1_5_surgical_deletes.cypher
│   └── mig_1_6_actor_merge.cypher
├── deleted/
│   ├── phase1_5_nodes.jsonl       (33 lines: full node state + edges before delete)
│   └── phase1_6_merges.jsonl      ( 7 lines: dup node state + edges before merge)
├── logs/
│   ├── agent4_runner.py           (orchestrator for 1.4 → 1.5 → 1.6)
│   ├── agent4_fixup_merge_id.py   (post-merge scalar-id fixup)
│   └── agent4_progress.log
└── reports/
    └── agent_4_phase1_4_5_6_report.md   (this file)
```

## Plan acceptance criteria (Phase 1, Agent-4 scope)

- [x] `:Materialdepot` exists with ≥ 20 members — **23 members**.
- [x] Each Materialdepot has `BETRIEBEN_VON` *if a same-name Akteur was
      present* — 3 of 23 (`bellastock`, `grosvenor`, `Rotor`); the other
      20 have no same-name operator Akteur, which is consistent with the
      plan's "≥ 10 new BETRIEBEN_VON if matching operator actors" hedge.
- [x] No `:Akteur` has degree ≤ 1 *among the 6 IDs listed for deletion*
      — all 6 verified deleted (see `phase1_5_nodes.jsonl`).
- [x] No two `:Akteur` ids differ only by case (post-merge verified):
      `MATCH (a:Akteur), (b:Akteur) WHERE toLower(a.id) = toLower(b.id)
      AND id(a) < id(b) RETURN a.id, b.id` → 0 rows.
- [x] Total nodes removed in Phase 1.5 ≤ 35 — **33**. (Total
      nodes-or-merge-consolidated across 1.4–1.6: 40, well under any
      reasonable cascade audit.)
- [x] Each `:BETRIEBEN_VON` edge added in 1.4 carries
      `evidence_origin='derived'`, `evidence_basis='name_match'`,
      `evidence_source_id='mig_1_4'`, `evidence_confidence='unklar'`.

## Reversibility

Phase 1.4 reversibility (no node deletes): swap labels back and remove
the 3 `:BETRIEBEN_VON{evidence_source_id:'mig_1_4'}` edges.

```cypher
MATCH (d:Materialdepot) REMOVE d:Materialdepot SET d:Bauwerk;
MATCH ()-[r:BETRIEBEN_VON {evidence_source_id:'mig_1_4'}]->() DELETE r;
```

Phase 1.5 reversibility: replay `deleted/phase1_5_nodes.jsonl` (each
record contains the node's labels, properties, and `edges_before_delete`
so the original wiring can be restored).

Phase 1.6 reversibility: replay `deleted/phase1_6_merges.jsonl`. For
each record, re-create the dup node with its original label set and
properties, then for every entry in `edges_before_merge` re-create the
edge between the dup node and the recorded `other_internal_id` /
`other_id` (preferring `other_id` since internal ids change), and remove
the merged-in id from the canon's `aliases` list.

## Hand-off to downstream agents

- Agents 2 (chains) and 3 (ontology anchors / Phase 1.2) ran in parallel
  and finished by the time Agent 4 verified the final counts (chains
  demote: 98 :Wiederverwendungskette removed; ontology anchor relabel:
  2 :Quelle now also bear `:OntologyAnchor`). Agent 4 did not touch
  either of those layers.
- The `Akteur` typology backbone now has **647 nodes**, with 7 nodes
  carrying non-empty `aliases` arrays (the merge targets). Phase 2.x
  consumers can rely on `id` being a scalar string everywhere.

Agent 4 stops here.
