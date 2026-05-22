# Coverage Addendum — Agent 06b (2026-06-06)

**Status:** Re-dispatch complete · READ-ONLY · no graph mutations.

Agent 15 flagged **319** unverified actor-network elements (~152 edges + ~167 nodes). Agent 06b
recomputed the gap deterministically from the live graph and adjudicated **386 claims**:

| Surface | Agent 15 estimate | Agent 06b actual | Delta |
|---|---:|---:|---|
| `VERBUNDEN_MIT_AKTEUR` (untagged, not in shards 01–06) | ~152 | **218** | +66 (reverse legs of bidirectional pairs) |
| Sourced `Akteur` nodes | ~167 | **168** | +1 |
| **Total claims** | ~319 | **386** | +67 |

**Element-level coverage after 06b:** the 386 previously unverified actor-network elements now have
per-element ledger rows in `ledger/agent_06b.csv`. ✅ **Merged** into `VERIFICATION_LEDGER.csv` by
Agent 15b (`_agent15b_aggregate.py`, 2026-06-06).

**Headline finding:** **0 / 218** gap edges carry on-graph `evidence_url` or `source_url` — the
actor-network layer is sourceless on-graph and cannot pass the Evidence Gate without off-graph
recovery or fresh fetches.

**06b verdicts (386 rows):** PROVEN 42 · PARTIAL 29 · UNVERIFIABLE 103 · MISSING_EVIDENCE 145 ·
SCHEMA_VIOLATION 67.

**06b actions:** KEEP 162 · RESOURCE 147 · RELABEL 76 · DELETE 1 (self-loop `Werner_Sobek→Werner_Sobek`).

**Definition of Done (plan §9):** item 1 (actor-network element coverage) is **met** at ledger level;
items requiring remediation application and aggregate-shard expansion (Agents 12/13) remain open.

See `reports/agent_06b.md` for full methodology and `REMEDIATION_PLAN.md` §7 for next gated steps.
