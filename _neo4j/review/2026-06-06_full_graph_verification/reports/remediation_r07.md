# Remediation R07 — Agent-14 `needs_source_url_review` backlog (rel sources)

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/remediation_r07.csv`](../ledger/remediation_r07.csv)
**Patch (dry-run):** [`patches/remediation_r07_add_rel_sources.patch.jsonl`](../patches/remediation_r07_add_rel_sources.patch.jsonl)

## Scope

Agent 14 backlog A14-BACKLOG-001 subset routed to R07:

| rel_type | backlog rows |
|---|---:|
| `BETEILIGT_AN` | 63 |
| `HAT_BAUTEILTYP` | 142 |
| `NUTZT_MATERIAL` | 103 |
| **Total** | **308** |

**Coverage:** 308/308 rows processed (100.0%). 0 backlog keys absent from live graph.

## Method

1. Filter `needs_source_url_review.csv` to HAT_BAUTEILTYP / NUTZT_MATERIAL / BETEILIGT_AN.
2. Cross-check live Neo4j (no on-graph `source_url` / `evidence_url`).
3. Recover candidate URLs from dossiers: `bauteilboersen_*.enrichment.json`, `project_part_actor_edges_extended.json`, actor/project `source_urls`.
4. Prioritize non-placeholder HTTP URLs; fetch each unique URL once (108 fetches).
5. PROVEN when stored/dossier quote tokens match fetched page, or (BETEILIGT_AN) actor + component on page.

## Verdict summary

| verdict | count | share |
|---|---:|---:|
| PARTIAL | 165 | 53.6% |
| PROVEN | 137 | 44.5% |
| MISSING_EVIDENCE | 6 | 1.9% |

### By relationship type

| rel_type | PROVEN | PARTIAL | MISSING | other |
|---|---:|---:|---:|---:|
| `BETEILIGT_AN` | 38 | 22 | 3 | 0 |
| `HAT_BAUTEILTYP` | 57 | 83 | 2 | 0 |
| `NUTZT_MATERIAL` | 42 | 60 | 1 | 0 |

### Proposed actions

| action | count |
|---|---:|
| RESOURCE | 171 |
| ADD_SOURCE | 137 |

**High-confidence patch ops drafted:** 137 `set_rel_properties` (evidence_url + quote + review_run `remediation_r07_2026_06_06`).

**Dry-run:** `apply_reports/remediation_r07_add_rel_sources.patch.apply_report.md` — **137/137 would_update_rel, 0 errors**.

✅ **Applied** 2026-06-06: **137 `set_rel_properties` / 0 errors** (live apply). Graph unchanged at **2 284 / 15 312**.

## Residual (6 MISSING_EVIDENCE)

| from | to | type | note |
|---|---|---|---|
| `new_horizon_urban_mining` | 3× CIRCL Bauteilgruppen | `BETEILIGT_AN` | 8 candidate URLs fetched; actor/component co-mention not found |
| `tool_hts_stockmatcher` | `bt_stuetze`, `bt_traeger`, `mat_stahl` | HAT/NUTZT | software tool homepage only; no catalog vocabulary proof |

171 rows remain `RESOURCE` (mostly PARTIAL: page fetched but dossier quote or overlap proof weak).

## Notes

- These rel types use **`evidence_url`** (reuse/catalog/participation), not regulation `source_url`.
- BETEILIGT_AN rows are overlap-derived candidates; PROVEN requires actor + component/project mention on page.
- Rows still `RESOURCE` need manual dossier review or stronger project-level proof.

## Apply

```bash
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r07_add_rel_sources.patch.jsonl
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r07_add_rel_sources.patch.jsonl --confirm "APPLY remediation_r07_add_rel_sources.patch.jsonl TO mit-bestand"
```
