# Final Verification: Phase 1.4 + 1.5 + 1.6

Verifier: Final Verifier 3 of 12  
Timestamp: 2026-05-21 09:01 UTC+2 context  
Database: `mit-bestand`  
Mode: read-only live graph verification

## Verdict

**FAIL** - Phase 1.4 passes, most Phase 1.5 artifact/delete checks pass, and Phase 1.6 artifact/count checks mostly pass, but the final live graph state does not satisfy all requested acceptance criteria.

Blocking failures:

- Phase 1.5: `norm_din_18940` still exists as a live `:Norm`.
- Phase 1.6: merge-in actor IDs `bauburo_in_situ` and `Bellastock` still exist as live `:Akteur` nodes.
- Phase 1.6: case-insensitive duplicate actor query returns `2`, from the ordered pair `bellastock` / `Bellastock`.

## Phase 1.4

| # | Check | Expected | Observed | Status |
|---|---|---:|---:|---|
| 1 | `migrations/mig_1_4_materialdepot.cypher` exists | exists | exists | PASS |
| 2 | `PHASE_1_4_DONE.flag` parseable | parseable JSON | parseable JSON | PASS |
| 3 | `MATCH (m:Materialdepot) RETURN count(m)` | 23 | 23 | PASS |
| 4 | `MATCH (m:Materialdepot) WHERE m:Bauwerk RETURN count(m)` | 0 | 0 | PASS |
| 5 | `BETRIEBEN_VON` edges with `evidence_source_id='mig_1_4'` | >= 3 | 3 | PASS |

Flag summary observed:

- `phase`: `1.4`
- `after_materialdepot`: `23`
- `relabelled`: `23`
- `betrieben_von_touched`: `4`

## Phase 1.5

| # | Check | Expected | Observed | Status |
|---|---|---:|---:|---|
| 6 | `migrations/mig_1_5_surgical_deletes.cypher` exists | exists | exists | PASS |
| 7 | `PHASE_1_5_DONE.flag` parseable | parseable JSON | parseable JSON | PASS |
| 8 | `deleted/phase1_5_nodes.jsonl` line count | 33 | 33 | PASS |
| 9 | Listed 6 Akteur IDs absent | 0 remain | 0 remain | PASS |
| 10 | Listed 4 Programm IDs absent | 0 remain | 0 remain | PASS |
| 11 | Listed 2 Norm IDs absent | 0 remain | 1 remains | FAIL |
| 12 | Sum of lines across `deleted/phase1_*.jsonl` | <= 200 | 161 | PASS |

Remaining `:Norm` ID:

- `norm_din_18940` (`degree`: 1, `name`: `DIN 18940`)

Phase-1 JSONL line counts:

- `deleted/phase1_1_chains.jsonl`: 98
- `deleted/phase1_2_quelle.jsonl`: 23
- `deleted/phase1_5_nodes.jsonl`: 33
- `deleted/phase1_6_merges.jsonl`: 7
- Total: 161

Note: `phase1_2_quelle.jsonl` contains 23 journal lines, including a header/preemption record and the collateral `q_phase20_kette_autodiscovery` entry.

## Phase 1.6

| # | Check | Expected | Observed | Status |
|---|---|---:|---:|---|
| 13 | `migrations/mig_1_6_actor_merge.cypher` exists | exists | exists | PASS |
| 14 | `PHASE_1_6_DONE.flag` parseable | parseable JSON | parseable JSON | PASS |
| 15 | `deleted/phase1_6_merges.jsonl` line count | 7 | 7 | PASS |
| 16 | `MATCH (a:Akteur) RETURN count(a)` | 640-650 | 650 | PASS |
| 17 | Listed 7 merge-in IDs absent | 0 remain | 2 remain | FAIL |
| 18 | Case-insensitive duplicate actor pairs | 0 | 2 | FAIL |

Remaining merge-in IDs:

- `bauburo_in_situ` (`degree`: 9, `name`: `bauburo in situ`)
- `Bellastock` (`degree`: 19, `name`: `Bellastock`)

Relevant duplicate/canonical nodes observed:

- `baubuero_in_situ` (`degree`: 23, `name`: `bauburo in situ`)
- `bauburo_in_situ` (`degree`: 9, `name`: `bauburo in situ`)
- `bellastock` (`degree`: 26, `name`: `Bellastock`)
- `Bellastock` (`degree`: 19, `name`: `Bellastock`)

Case-insensitive duplicate query result:

```cypher
MATCH (a1:Akteur),(a2:Akteur)
WHERE a1.id<>a2.id AND toLower(a1.id)=toLower(a2.id)
RETURN count(*)
```

Observed `count(*)`: `2`, representing the two ordered directions of `bellastock` / `Bellastock`.

## Live Query Summary

| Query / Check | Observed |
|---|---:|
| `MATCH (m:Materialdepot) RETURN count(m)` | 23 |
| `MATCH (m:Materialdepot) WHERE m:Bauwerk RETURN count(m)` | 0 |
| `MATCH (m:Materialdepot)-[r:BETRIEBEN_VON]->(a:Akteur) WHERE r.evidence_source_id='mig_1_4' RETURN count(r)` | 3 |
| Phase 1.5 Akteur delete IDs remaining | 0 |
| Phase 1.5 Programm delete IDs remaining | 0 |
| Phase 1.5 Norm delete IDs remaining | 1 |
| `MATCH (a:Akteur) RETURN count(a)` | 650 |
| Phase 1.6 merge-in IDs remaining | 2 |
| Case-insensitive Akteur duplicate ordered pairs | 2 |

## Final State

Phase 1.4 is confirmed final. Phase 1.5 and Phase 1.6 are **not** confirmed final because live graph acceptance checks 11, 17, and 18 fail.
