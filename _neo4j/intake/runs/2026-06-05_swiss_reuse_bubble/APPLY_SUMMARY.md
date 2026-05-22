# Swiss reuse bubble — apply summary

**Database:** `mit-bestand`  
**Applied:** 2026-06-05 (phases 0–3)  
**Review run:** `swiss_reuse_bubble_2026_06_05`

## Graph delta

| Metric | Before | After | Δ |
|--------|-------:|------:|--:|
| Nodes | 2 287 | 2 335 | +48 |
| Relationships | 15 393 | 15 451 | +58 |

## Connectivity tests (post-apply)

| Test | Before | After | Target |
|------|--------|-------|--------|
| Cirkla `VERBUNDEN_MIT_AKTEUR` degree | 2 | **14** | ≥ 8 |
| Cirkla `BELEGT_IN` count | 0 | **4** | ≥ 4 |
| K.118 `BETEILIGT_AN` includes `baubuero_in_situ` | no | **yes** | yes |
| K.118 `BETEILIGT_AN` includes `zirkular` | no (stub absent) | **yes** | yes |
| Gruner → useagain shortest path | 0 | **1** | ≥ 1 |
| Edges with `review_run=swiss_reuse_bubble_2026_06_05` | 0 | **58** | — |

### Cirkla neighbors (14)

`baubuero_in_situ`, `useagain_bauteilclick`, `materiuum`, `wick_reuse_roto_baumarkt`, `bauteilladen_winterthur`, `reuzi_ch`, `gruner_reuse_platform`, `salza`, `zirkular`, `c33_circular_construction_catalyst`, `circular_hub_zurich`, `circular_economy_switzerland`, `urban_bricolage`, `pascal_flammer_architekten`

## Apply adjustments during import

1. **`gruner_reuse` → `gruner_reuse_platform`** — live graph has only the platform anchor.
2. **Added `q_url_45d7c6380377a9cec952dbf6c3f2ba8c`** (salza.ch/bauteil-plattform) to phase 0 for corroborating `BELEGT_IN`.
3. **Stub deletes** (`ASSOZIIERT_MIT_PROJEKT` K.118/ELYS) — `noop_missing` (stubs not present in live graph); `BETEILIGT_AN` edges created directly.

## New nodes (phase 2)

`software_planular`, `tool_swiss_inv`, `software_cirkla_scan`, `prog_swircular`, `prog_innosuisse_reuse_legal_framework_ch`, `c33_circular_construction_catalyst`, `circular_hub_zurich`, `circular_economy_switzerland`, `sumami`

## Reports

- Per-phase: `apply_reports/phase*.apply_report.json`
- Connectivity: `connectivity_report.json`, `apply_summary.json`
- Evidence sidecar unchanged on disk; graph edges carry `metadata_sidecar_key` + `evidence_claim_ids`

## Verify in Browser

```cypher
MATCH (c:Akteur {id:'cirkla'})-[r:VERBUNDEN_MIT_AKTEUR]-(n)
RETURN n.id, r.connection_kind, r.evidence_confidence, r.evidence_claim_ids
ORDER BY n.id;

MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})<-[r:BETEILIGT_AN]-(a)
RETURN a.id, r.evidence_quote, r.fact_label;
```
