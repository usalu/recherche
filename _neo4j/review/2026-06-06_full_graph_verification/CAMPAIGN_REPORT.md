# Campaign Report — Full-Graph Verification (15-Agent Proof + Agent 06b)

**Agent:** 15b (post-06b merge) · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Merged ledger:** `VERIFICATION_LEDGER.csv` — **8,284 rows** from 15 shards (01–14 + 06b).
**Coverage:** see `COVERAGE_PROOF.md` (element-level 6,365/15,457 rels + 1,264/2,304 nodes; **0 genuine gaps**).

---

## 1. Verdict distribution (all 8,284 ledger rows)

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 6,025 | 72.7 % |
| MISSING_EVIDENCE | 931 | 11.2 % |
| PARTIAL | 890 | 10.7 % |
| SCHEMA_VIOLATION | 228 | 2.8 % |
| UNVERIFIABLE | 127 | 1.5 % |
| DEAD_LINK | 53 | 0.6 % |
| CONTRADICTION | 23 | 0.3 % |
| UNSUPPORTED | 5 | 0.06 % |
| *(parse artifact: blank/`false`)* | 2 | — |

**Post-06b shift:** +42 PROVEN (06b node existence checks), +145 MISSING_EVIDENCE, +103 UNVERIFIABLE,
+67 SCHEMA_VIOLATION on the actor-network layer — expected because 06b adjudicated previously unverified edges
with zero on-graph evidence.

## 2. Proposed-action distribution

| Action | Count | Nature |
|---|---:|---|
| KEEP | 6,536 | no change |
| ADD_SOURCE | 780 | non-destructive (set node/rel source) |
| RESOURCE | 453 | find a correct URL |
| ESCALATE_HUMAN | 228 | judgment needed |
| MERGE_DUPLICATE | 195 | dedup (88 Agent-14 pairs + 63 Agent-06b reverse legs + node dupes) |
| RELABEL | 70 | downgrade confidence/label |
| FIX_PROPERTY | 16 | schema/property cleanup |
| DELETE | 4 | destructive — gated only (+1 Agent-06b self-loop) |

## 3. "Where the mistakes happened" — heatmap

### 3.1 By verifier shard (verdict mix)

| Agent | Scope | PROVEN | PARTIAL | MISSING | SCHEMA | DEAD | UNVER | CONTRA | UNSUP |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 CH | bubble | 40 | 2 | 42 | – | 1 | – | – | – |
| 02 BE/Rotor | bubble | 30 | 3 | 15 | – | – | – | – | 1 |
| 03 DE | bubble | 28 | 3 | 17 | – | – | – | – | – |
| 04 FR | bubble | 14 | – | – | – | – | – | – | – |
| 05 NL | bubble | 11 | – | 4 | 1 | – | – | – | – |
| 06 cross-border | bubble | 15 | – | – | – | – | – | – | 2 |
| **06b actor networks** | **386** | **42** | **29** | **145** | **67** | – | **103** | – | – |
| 07 regulation URLs | 3,691 | 3,542 | 86 | – | – | 52 | 11 | – | – |
| 08 unsourced actors | 477 | 17 | – | 431 | 20 | – | 9 | – | – |
| 09 places/projects | 2,576 | 1,645 | 751 | 175 | – | – | – | 5 | – |
| 10 software/depots | 175 | 22 | 15 | 101 | 31 | – | 4 | – | 2 |
| 11 law nodes | 559 | 559 | – | – | – | – | – | – | – |
| 12 vocab (agg) | 32 | 21 | – | – | 11 | – | – | – | – |
| 13 process (agg) | 47 | 28 | – | – | – | – | – | 18 | – |
| 14 hygiene (meta) | 112 | 11 | 1 | 1 | 98 | – | – | – | – |

### 3.2 By source / run / type — where errors concentrate

1. **Cross-border reuse-bubble actor edges (Agents 02, 06)** — the **only fabrication / UNSUPPORTED** locus (3 edges).
2. **Non-bubble actor networks (Agent 06b)** — **0 on-graph evidence** on 218 gap edges; 12 RecReate-cluster edges
   corroborated off-graph (PARTIAL → `consortium_co_membership` relabel drafted); 63 bidirectional reverse legs
   flagged MERGE_DUPLICATE; 1 self-loop DELETE (`Werner_Sobek→Werner_Sobek`).
3. **Process-requirement layer (Agent 13)** — **18 CONTRADICTION** dangling `Nachweisforderung`.
4. **Geo / participation (Agent 09)** — **751 PARTIAL** weak geo URLs → RESOURCE.
5. **Provenance long tail (Agents 08, 10)** — **532 MISSING_EVIDENCE** incl. all 22 `Materialdepot` nodes.
6. **Regulation URLs (Agent 07)** — 3,542/3,691 PROVEN; 52 dead + 11 paywalled.
7. **Schema hygiene (Agent 14)** — 88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs + key drift.

## 4. Residual unverifiable / unresolved set

- **127 UNVERIFIABLE** (+103 from 06b deferred re-fetch of already-sourced actors).
- **931 MISSING_EVIDENCE** (+145 from 06b unsourced actor-network edges).
- **0 unverified graph elements** — actor-network coverage gap **closed** at ledger level.

## 5. Patch apply ledger (2026-06-06)

| Patch | Ops | Dry-run | Live apply |
|---|---:|---|---|
| `agent15_add_node_sources.patch.jsonl` | 17 `set_node_properties` | ✅ 17/0 errors | ✅ **applied** |
| `agent06b_add_node_sources.patch.jsonl` | 42 `set_node_properties` | ✅ 42/0 errors | ✅ **applied** |
| `agent06b_relabel_connection_kind.patch.jsonl` | 12 `set_rel_properties` | ✅ 12/0 errors | ✅ **applied** |
| `agent06b_delete_self_loop.patch.jsonl` | 1 `delete_rel` | ✅ 1 would_delete | ✅ **applied** (1 deleted) |
| `agent06b_merge_duplicate_reverse.patch.jsonl` | 63 `delete_rel` | ✅ 63 would_delete | ✅ **applied** (63 deleted) |
| `delete_unsupported.patch.jsonl` | 3 `delete_rel` | ✅ 3 would_delete | ✅ **applied** (3 deleted) |
| `fix_property.patch.jsonl` | 16 ops | ✅ 16/0 errors | ✅ **applied** |
| `merge_duplicate_edges_remaining.patch.jsonl` | 23 `delete_rel` | ✅ 23 would_delete | ✅ **applied** (23 deleted) |
| `merge_duplicate_nodes_high_confidence.patch.jsonl` | 8 `merge_node` | ✅ 8 would_merge | ✅ **applied** (8 merged) |

Apply reports: `apply_reports/*.apply_report.{md,json}`.

**Bidirectional `VERBUNDEN_MIT_AKTEUR` dedup total:** 86 reverse legs deleted (63 + 23); **2 pairs remain**
(`madaster↔rau`, `madaster↔thomas_rau`) — escalated pending `rau` vs `thomas_rau` identity decision.

## 6. Verdict

- **Coverage DoD (actor networks):** met — every `VERBUNDEN_MIT_AKTEUR` edge and every sourced `Akteur` has a
  ledger row; REL uncovered count is **0**.
- **Evidence DoD:** not met on-graph for the 06b gap edges — provenance remediation partially applied (59 node
  sources + 12 connection_kind relabels); 218 gap edges still lack on-graph evidence URLs.
- **Fabrication containment:** **0 UNSUPPORTED** bubble edges remain (3 deleted 2026-06-06); no resurrection of the purged 29.
- **Outstanding:** 2 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs (`madaster`/`rau`/`thomas_rau`), 36 deferred node
  dupes (ZRS triple, composites, harvestmap), `A14-LAND-001` (add `LIEGT_IN_LAND` before dropping scalar `land`),
  `prog_mas_dfab` relabel, RESOURCE/ADD_SOURCE batches after fresh fetches (**not touched this pass**),
  dangling requirements (18), Materialdepot sourcing (22), key re-baseline, optional Tier-C re-run (R2/R3).
  Post-remediation graph: **2 296 nodes / 15 338 rels** (−119 rels, −8 nodes from pre-remediation 2 304 / 15 390).

See `REMEDIATION_PLAN.md` for grouped actions and `reports/agent_15b.md` for merge details.
