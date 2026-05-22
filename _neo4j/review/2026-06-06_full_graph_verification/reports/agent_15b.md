# Agent 15b — Merge Agent 06b & Post-Gap Coverage Report

**Date:** 2026-06-06 · **Database:** `mit-bestand` · **Mode:** ledger merge + one live patch apply.

## Scope

Re-ran the Agent 15 aggregator (`_agent15b_aggregate.py`) to append `ledger/agent_06b.csv` (386 claims) to the
14-shard merged ledger, recompute coverage/synthesis, and close the actor-network gap flagged by Agent 15.

## Artifacts

| File | Change |
|---|---|
| `VERIFICATION_LEDGER.csv` | **8,284 rows** (+386 from 06b); `source_agent=06b` on new rows |
| `_agent15_work/coverage.json` | REL uncovered **0**; `VERBUNDEN_MIT_AKTEUR` 341/341 element-covered |
| `_agent15_work/synthesis.json` | Post-06b verdict/action totals |
| `COVERAGE_PROOF.md` | Headline updated — actor-network gaps closed |
| `patches/agent06b_*.patch.jsonl` | Four gated remediation drafts (dry-run documented) |

## Coverage delta (vs Agent 15)

| Surface | Before (Agent 15) | After (15b) |
|---|---:|---:|
| Ledger rows | 7,898 | **8,284** |
| Rel element-covered | 6,213 (40.2 %) | **6,365 (41.2 %)** |
| Rel uncovered | 152 | **0** |
| Node element-covered | 1,097 (47.6 %) | **1,264 (54.9 %)** |
| Node uncovered (`Akteur` gap) | 167 | **0** |

## Post-06b verdict mix (386 rows, agent 06b only)

PROVEN 42 · PARTIAL 29 · UNVERIFIABLE 103 · MISSING_EVIDENCE 145 · SCHEMA_VIOLATION 67.

Actions: KEEP 162 · ADD_SOURCE 144 · MERGE_DUPLICATE 63 · ESCALATE_HUMAN 13 · RESOURCE 3 · DELETE 1.

## Patch apply status

| Patch | Records | Dry-run | Applied |
|---|---:|---|---|
| `agent15_add_node_sources.patch.jsonl` | 17 | ✅ clean | ✅ **live** (17 nodes) |
| `agent06b_add_node_sources.patch.jsonl` | 42 | ✅ 42 would_update | ⏸ pending |
| `agent06b_relabel_connection_kind.patch.jsonl` | 12 | ✅ 12 would_update_rel | ⏸ pending |
| `agent06b_delete_self_loop.patch.jsonl` | 1 | ✅ 1 would_delete_rel | ⏸ **human gate** |
| `agent06b_merge_duplicate_reverse.patch.jsonl` | 63 | ✅ 63 would_delete_rel | ⏸ **human gate** |

## One-paragraph summary

Agent 06b closes the campaign's actor-network coverage gap: all 341 `VERBUNDEN_MIT_AKTEUR` edges and every
sourced `Akteur` now have per-element ledger rows. The graph is still provenance-thin on that class (0/218 gap
edges had on-graph evidence at audit), so remediation is drafted but mostly pending human gate. The first safe
apply tranche — 17 Agent-08 node sources from `agent15_add_node_sources` — is now live on `mit-bestand`.
