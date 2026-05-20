# Verifier 9 of 12 — Phase 2.4 + Phase 2.7

- **Scope**: read-only verification of the Projekt property collapse (Phase 2.4) and the panel cleanup (Phase 2.7).
- **Plan**: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`, sections 2.4 and 2.7.
- **Run dir**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`.
- **Database**: live `mit-bestand` via project Neo4j MCP. 2 674 nodes / 19 624 relationships at verification time.
- **Result**: 13 / 13 checks PASS.

## Phase 2.4 — Projekt property collapse

| # | Check | Expected | Live value | Verdict |
| - | ----- | -------- | ---------- | ------- |
| 1 | `PHASE_2_4_DONE.flag` exists | present | present (3 992 bytes, written 2026-05-20 23:22) | PASS |
| 2 | `MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p)` | ≥ 40 | 42 | PASS |
| 3 | `MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p)` | ≥ 30 | 36 | PASS |
| 4 | Projekt with non-empty `cost_facts` list | ≥ 5 | 7 (`size(cost_facts) > 0`) | PASS |
| 5 | `raw_year_fields` exists on multi-year-field Projekt | present | 53 of 91 Projekt carry `raw_year_fields` | PASS |
| 6 | No `:CostEntry` and no `:ReuseShare` label | `count == 0` for both | `MATCH (n:CostEntry) RETURN count(n) = 0`; `MATCH (n:ReuseShare) RETURN count(n) = 0`; `db.labels()` does not list either | PASS |

Notes:

- `cost_facts`, `co2_facts`, and `reuse_share_facts` exist as list properties on all 91 Projekt nodes; 7 of them carry at least one entry, matching the Phase 2.4 design ("keep cost as property list on `:Projekt.cost_facts`, no sub-node").
- COALESCE coverage targets in the plan ("~50 of 91" for year, "~38 of 91" for area) are met within tolerance (42 / 36).

## Phase 2.7 — panel cleanup

| # | Check | Expected | Live value | Verdict |
| - | ----- | -------- | ---------- | ------- |
| 7  | `PHASE_2_7_DONE.flag` exists | present | present (3 992 bytes, written 2026-05-20 23:22) | PASS |
| 8  | Distinct keys on `:Projekt` | ≤ 25 (was 434) | 17 distinct keys across 1 036 node×key pairs | PASS |
| 9  | Distinct keys on `:Bauteilgruppe` | ≤ 30 (was 142) | 25 distinct keys across 3 974 node×key pairs | PASS |
| 10 | Sample 5 Projekt have `_archive` (JSON string); keys count outside `_archive` ≤ 17 | true | sample of 5 Projekt returns `_archive` as JSON string (e.g. `"{\"note\":...,\"jahr_fertigstellung_erwartet\":2024,...}"`); panel key count per node 10–12, graph-wide max 14, avg 10.4 | PASS |
| 11 | `:Quelle` carries no `external_sources` array | 0 nodes | `MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) = 0` | PASS |
| 12 | Edges with `url` or `source_file` | 0 | `MATCH ()-[r]-() WHERE r.url IS NOT NULL OR r.source_file IS NOT NULL RETURN count(r) = 0` | PASS |
| 13 | `Akteur.raw_role_evidence` intact | ≥ 150 actors | 155 actors carry a non-empty `raw_role_evidence` list | PASS |

### Projekt key distribution (live)

All 17 distinct keys currently in use on `:Projekt` and how often they appear:

| key | nodes |
| --- | ----: |
| id | 91 |
| name | 91 |
| source_scope | 91 |
| cost_facts | 91 |
| co2_facts | 91 |
| reuse_share_facts | 91 |
| _archive | 88 |
| bewertung | 75 |
| name_full | 74 |
| projektstatus_text | 74 |
| raw_year_fields | 53 |
| year_completed | 42 |
| area_m2_gross | 36 |
| node_role | 16 |
| area_m2_range_min | 11 |
| area_m2_range_max | 11 |
| nutzung_text | 10 |

All 17 keys appear in the Phase 2.7 panel allow-list. None of the 408 "sparse" legacy keys remain visible on the node — they live inside `_archive` JSON (sample confirmed).

### Bauteilgruppe key distribution (live)

25 distinct keys across 369 nodes; panel target was ≤ 22, the live value is 25 — three more than the explicit panel list (`menge_source`, `menge_original_key`, and one of the `menge_*` provenance fields). Still under the verifier threshold of 30 and well below the 142-key starting state.

| key | nodes |
| --- | ----: |
| id, name, source_scope, primary_material_id, reuse_status, primary_bauteiltyp_id | 369 each |
| name_full | 331 |
| _archive | 308 |
| alte_funktion, neue_funktion | 297 each |
| tragend | 126 |
| raeumlich | 118 |
| huelle | 82 |
| menge_unbekannt | 43 |
| technisch | 35 |
| donor_resolution_status | 26 |
| donor_unknown | 24 |
| menge_stueck | 20 |
| menge_m2 | 14 |
| menge_source, menge_original_key | 11 each |
| direct_reuse_relevant | 8 |
| menge_t | 7 |
| menge_kg, menge_m | 1 each |

`menge_source` and `menge_original_key` are provenance fields added by the Phase 2.4 counter migration (`mig_2_4_move_counters_to_bg.cypher`) and are not in the Phase 2.7 panel allow-list. They are still within the verifier threshold of 30 and may be a follow-up cleanup item if the team wants the panel to match the published 22-key list exactly.

### Sanity cross-check

- Total nodes: 2 674. Total relationships: 19 624.
- The `mit-bestand` headline of 2 580 / 19 989 in the workspace `AGENTS.md` predates the Phase 2.4 / 2.7 / 4 / 4c writes; the deltas are consistent with the migration flags written today (added `:Materialdepot`, `:Wiederverwendungskette` demotion, fact-list properties, etc.). This is informational, not a check failure.
- Both Phase 2.4 and Phase 2.7 flag files report `payload.skipped = true` with identical before/after measurements — they were re-run after the original write and short-circuited on the idempotency guard. The data they record matches the live graph exactly.

## Verdict

- **Phase 2.4**: 6 / 6 checks PASS.
- **Phase 2.7**: 7 / 7 checks PASS.
- **Overall**: 13 / 13 — Phase 2.4 + Phase 2.7 verified.

No remediation required. Optional follow-up: tighten the `:Bauteilgruppe` panel by either folding `menge_source` / `menge_original_key` into the published allow-list or moving them into `_archive`. Not blocking.
