# Verify Phase 1.5 Surgical Deletes

Verifier: 5 of 12  
Phase: 1.5  
Run dir: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`  
Neo4j database: `mit-bestand` via read-only MCP/driver config from `E:\recherche\.cursor\mcp.json`

## Result

Overall status: **FAIL**

The direct Phase 1.5 surgical delete artifacts and the 12 targeted `:Akteur` / `:Programm` / `:Norm` removals are verified. The verification fails on the requested audit gate and the requested live `:Quelle` count band.

## Checks

| Check | Expected | Observed | Status |
| --- | ---: | ---: | --- |
| `migrations\mig_1_5_surgical_deletes.cypher` exists | yes | yes | PASS |
| `PHASE_1_5_DONE.flag` exists | yes | yes | PASS |
| `deleted\phase1_5_nodes.jsonl` line count | 33 | 33 | PASS |
| Target `:Akteur` IDs still present | 0 | 0 | PASS |
| Target `:Programm` IDs still present | 0 | 0 | PASS |
| Target `:Norm` IDs still present | 0 | 0 | PASS |
| Phase-1 deleted JSONL line total | <= 35 | 161 | FAIL |
| Live `:Akteur` count | 647 +/- 5 | 647 | PASS |
| Live `:Programm` count | 24 +/- 5 | 24 | PASS |
| Live `:Norm` count | 34 +/- 5 | 34 | PASS |
| Live `:Quelle` count | 465 +/- 5 | 726 | FAIL |

## Target ID Absence

Read-only Cypher returned no rows for these IDs:

- `glasfischer_glastec`
- `citydev_brussels`
- `denkstatt`
- `eitel_partner`
- `gibbins_architekten`
- `zusammenkunft_berlin`
- `prog_bbsm`
- `prog_preuse`
- `prog_zukunftbau`
- `prog_kommunales_programm`
- `norm_bs_5385_5_2009`
- `norm_din_18940`

## Deleted JSONL Audit

Phase-1 JSONL line counts:

| File | Lines |
| --- | ---: |
| `deleted\phase1_1_chains.jsonl` | 98 |
| `deleted\phase1_2_quelle.jsonl` | 23 |
| `deleted\phase1_5_nodes.jsonl` | 33 |
| `deleted\phase1_6_merges.jsonl` | 7 |
| **Phase-1 total** | **161** |

All `deleted/*.jsonl` line counts observed:

| File | Lines |
| --- | ---: |
| `deleted\phase1_1_chains.jsonl` | 98 |
| `deleted\phase1_2_quelle.jsonl` | 23 |
| `deleted\phase1_5_nodes.jsonl` | 33 |
| `deleted\phase1_6_merges.jsonl` | 7 |
| `deleted\phase2_1_status_merges.jsonl` | 2 |
| `deleted\phase2_3_role_merges.jsonl` | 1 |
| `deleted\phase2_5_demoted_nodes.jsonl` | 28 |
| `deleted\phase2_5_tool_relabels.jsonl` | 8 |
| `deleted\phase2_7_external_sources.jsonl` | 60 |
| `deleted\phase4c_3_projekt_actor_registry_belegt.jsonl` | 176 |
| **All deleted JSONL total** | **436** |

Note: `phase1_2_quelle.jsonl` includes a header/preemption note and many records marked `actually_deleted_in:"phase_1_5"`. The strict requested line-sum gate still evaluates to 161 for Phase-1 files.

## Live Label Counts

Read-only Cypher:

```cypher
CALL { MATCH (n:Akteur) RETURN count(n) AS Akteur }
CALL { MATCH (n:Programm) RETURN count(n) AS Programm }
CALL { MATCH (n:Norm) RETURN count(n) AS Norm }
CALL { MATCH (n:Quelle) RETURN count(n) AS Quelle }
RETURN Akteur, Programm, Norm, Quelle
```

Observed:

```json
{"Akteur":647,"Programm":24,"Norm":34,"Quelle":726}
```

## JSON

```json
{
  "phase": "1.5",
  "verifier": 5,
  "status": "FAIL",
  "checks": {
    "migration_exists": true,
    "done_flag_exists": true,
    "phase1_5_nodes_jsonl_exists": true,
    "phase1_5_nodes_jsonl_lines": 33,
    "target_akteur_ids_present": [],
    "target_programm_ids_present": [],
    "target_norm_ids_present": [],
    "target_ids_absent": true,
    "phase1_deleted_jsonl_line_total": 161,
    "phase1_deleted_jsonl_gate_max": 35,
    "phase1_deleted_jsonl_gate_pass": false,
    "all_deleted_jsonl_line_total": 436,
    "label_counts": {
      "Akteur": 647,
      "Programm": 24,
      "Norm": 34,
      "Quelle": 726
    },
    "label_count_expectations": {
      "Akteur": {"target": 647, "tolerance": 5, "pass": true},
      "Programm": {"target": 24, "tolerance": 5, "pass": true},
      "Norm": {"target": 34, "tolerance": 5, "pass": true},
      "Quelle": {"target": 465, "tolerance": 5, "pass": false}
    }
  },
  "notes": [
    "Direct Phase 1.5 artifacts and target ID absence pass.",
    "Strict Phase-1 deleted JSONL line-sum audit fails: 161 > 35.",
    "Live Quelle count fails requested Phase-1 band: 726 is outside 465 +/- 5."
  ]
}
```
