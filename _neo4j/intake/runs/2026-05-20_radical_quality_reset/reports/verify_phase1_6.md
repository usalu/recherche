# Verify Phase 1.6 — Akteur merges (Verifier 6 of 12)

- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Database:** `mit-bestand` (read-only Bolt session via `.cursor\mcp.json`)
- **Verified at:** 2026-05-20 (Wednesday)
- **Verdict:** **PASS** — all 8 checks green.

## Summary

| # | Check | Expected | Actual | Status |
|---|-------|----------|--------|--------|
| 1 | `migrations\mig_1_6_actor_merge.cypher` exists | present | present (template + parameterised pattern, 28 lines) | PASS |
| 2 | `PHASE_1_6_DONE.flag` exists | present | present (2 500 bytes, includes `fixup_note` for scalar-id reset) | PASS |
| 3 | `deleted\phase1_6_merges.jsonl` has 7 lines | 7 | **7** | PASS |
| 4 | Live `count(:Akteur)` ≈ 647 (±2) | 647 | **647** | PASS |
| 5 | All 7 merge-in IDs gone | 0 hits | **0 hits** | PASS |
| 6 | Each canonical carries merge-in id in `aliases` | 7/7 | **7/7** | PASS |
| 7 | No case-collision Akteur pairs | 0 | **0** | PASS |
| 8 | `a.id` is scalar `STRING` on all merged actors | true / non-list | **true** on 7/7; no Akteur with non-STRING id | PASS |

Net `:Akteur` delta vs `before_akteur` in flag: 654 → 647 (Δ = −7), matching the seven journalled merges.

## Check 1 — Migration file

`E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\migrations\mig_1_6_actor_merge.cypher`
exists. It documents the seven canonical ← merge-in pairs and the
parameterised `apoc.refactor.mergeNodes([canon, dup], {properties:'combine',
mergeRels:true})` pattern executed per pair by the Python runner. The file is a
documentation/spec template; the actual writes were issued by the runner against
the live database and journalled to `deleted\phase1_6_merges.jsonl`.

## Check 2 — Done-flag

`PHASE_1_6_DONE.flag` (2 500 bytes) carries:

- `phase: "1.6"`, `completed_at: 2026-05-20T20:52:59+00:00`,
  `fixed_up_at: 2026-05-20T20:55:00+00:00`,
- explicit `fixup_note`: `apoc.refactor.mergeNodes({properties:'combine'})`
  coerced the scalar `id` into a list; `logs/agent4_fixup_merge_id.py` reset
  each merged node's `id` to the canonical scalar. The `aliases` array is the
  authoritative record of merged-in ids.
- `summary.before_akteur: 654`, `summary.after_akteur: 647`,
  `delta_akteur: -7`, `expected_after: 647`,
- `summary.merged_pairs[]` — 7 entries, each with `canonical_id`, `merge_id`,
  `status: "merged"`, `resulting_id`, `combined_degree`, and a single-element
  `aliases` list.

## Check 3 — Journal line count

`(Get-Content phase1_6_merges.jsonl | Measure-Object -Line).Lines = 7`. Each
line is a full pre-merge dump of one merged-in Akteur (labels, properties, every
incident edge with direction + other-node id + properties), allowing the merge
to be undone deterministically.

## Check 4 — Live Akteur count

```cypher
MATCH (a:Akteur) RETURN count(a) AS count;
// => 647
```

Exact match with `expected_after` in the flag (no ±tolerance needed).

## Check 5 — Merge-in IDs gone

```cypher
UNWIND ['bauburo_in_situ','ak_plp_architecture','zrs_architekten',
        'loeliger_strub_architektur','bill_dunster_zedfactory',
        'opera_pm','Bellastock'] AS id
MATCH (a:Akteur {id: id})
RETURN id, a.id AS found_id, labels(a) AS labels;
// => [] (zero rows)
```

None of the seven merged-in node ids resolve to a live `:Akteur`. The
Bellastock case-collision is resolved with `bellastock` (lowercase) as the
surviving canonical, exactly as specified in the plan.

Direction reversal vs. the layer-2 guess is intentional: for `baubuero_in_situ`,
`plp_architecture`, `ZRS_Architekten_Ingenieure`, `loeliger_strub`,
`zedfactory_bill_dunster`, `opera`, and `bellastock`, the canonical is the
higher-degree (or orthographically preferred) form, per plan §1.6.

## Check 6 — Aliases preserve merge-in IDs

```cypher
UNWIND ['baubuero_in_situ','plp_architecture','ZRS_Architekten_Ingenieure',
        'loeliger_strub','zedfactory_bill_dunster','opera','bellastock'] AS id
MATCH (a:Akteur {id: id})
RETURN id AS expected_id, a.id AS actual_id, a.aliases AS aliases,
       a.name AS name, size([(a)--() | 1]) AS degree;
```

| expected_id | actual_id | aliases | name | degree |
|---|---|---|---|---|
| baubuero_in_situ | baubuero_in_situ | [bauburo_in_situ] | baubüro in situ | 23 |
| plp_architecture | plp_architecture | [ak_plp_architecture] | PLP Architecture | 11 |
| ZRS_Architekten_Ingenieure | ZRS_Architekten_Ingenieure | [zrs_architekten] | ZRS Architekten Ingenieure | 9 |
| loeliger_strub | loeliger_strub | [loeliger_strub_architektur] | Loeliger Strub | 10 |
| zedfactory_bill_dunster | zedfactory_bill_dunster | [bill_dunster_zedfactory] | Bill Dunster / ZEDfactory | 4 |
| opera | opera | [opera_pm] | Opera | 7 |
| bellastock | bellastock | [Bellastock] | Bellastock | 26 |

7/7 canonicals carry the merge-in id in `aliases`. Live degrees match (or
exceed) the `combined_degree` recorded in the done-flag.

Side note (not part of the eight checks): 16 `:Akteur` carry an `aliases`
property — 7 from the merges, 9 from the case-normalisation of the
typology-backbone IDs (`CITYFOERSTER`, `Lendager`, etc.) that the plan
explicitly says should be normalised without merging.

## Check 7 — No case-only collisions

```cypher
MATCH (a1:Akteur),(a2:Akteur)
WHERE a1.id <> a2.id AND toLower(a1.id) = toLower(a2.id)
RETURN count(*) AS case_collisions;
// => 0
```

Also confirmed via `MATCH (a:Akteur) WITH toLower(a.id) AS lid, count(*) AS n
WHERE n > 1 RETURN lid, n` → empty.

## Check 8 — `a.id` is scalar STRING

```cypher
UNWIND ['baubuero_in_situ','plp_architecture','ZRS_Architekten_Ingenieure',
        'loeliger_strub','zedfactory_bill_dunster','opera','bellastock'] AS id
MATCH (a:Akteur {id: id})
RETURN id AS expected_id, a.id AS actual_id,
       a.id IS :: STRING    AS id_is_string,
       a.id IS :: LIST<ANY> AS id_is_list;
```

All seven rows: `id_is_string = true`, `id_is_list = false`.

Graph-wide:

```cypher
MATCH (a:Akteur) WHERE NOT a.id IS :: STRING
RETURN a.id AS id, labels(a) AS labels LIMIT 10;
// => []
```

No `:Akteur` has a non-STRING id. The `fixup_note` in the flag is corroborated:
`apoc.refactor.mergeNodes(... properties:'combine')` did coerce the id into a
list during the merge, but the post-merge `logs/agent4_fixup_merge_id.py` reset
each merged node's `id` to its canonical scalar.

## Phase-acceptance side-checks (plan §"Phase 1 acceptance criteria")

These are not part of the verifier's eight checks but were trivially observable
during the read-only session and are reported for completeness:

- **No two `:Akteur` IDs differ only by case** — confirmed (Check 7).
- **Net `:Akteur` count** — 647, matches the plan's projected 647 after merges
  (`660 − 6 hard-delete − 7 merges = 647`).

## Methodology

Read-only Bolt session against `mit-bestand` using credentials from
`E:\recherche\.cursor\mcp.json` (`NEO4J_READ_ONLY=true`). All queries executed
against the live database; no mutations issued. JSON/JSONL artefacts inspected
verbatim with the file-system read tool. Journal line count verified with
`Get-Content | Measure-Object -Line`.

## Verdict

**PASS.** All eight required checks succeed with no caveats. Phase 1.6 is
complete and the artefacts on disk faithfully describe the live state of the
graph.
