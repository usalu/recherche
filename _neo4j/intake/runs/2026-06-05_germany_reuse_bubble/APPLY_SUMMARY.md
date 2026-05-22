# Germany reuse bubble — apply summary

**Date:** 2026-06-05  
**Database:** `mit-bestand`  
**Review run:** `germany_reuse_bubble_2026_06_05`

## Result: applied successfully

| Metric | Before (initial) | After (incl. 1c) | Delta |
|---|---:|---:|---:|
| Nodes | 2 356 | 2 384 | **+28** |
| Relationships | 15 477 | 15 529 | **+52** |

## Phases

| Phase | New nodes | New rels | Notes |
|---|---:|---:|---|
| 0 — sources + dossier | 17 | 0 | |
| 1 — concular ecosystem spine | 0 | 16 | |
| 2 — Bauteilbörse Hannover | 1 (`bauteilboerse_hannover`) | 10 | |
| 2b — Haus der Materialisierung | 1 (`haus_der_materialisierung`) | 10 | |
| **1c — evidence hardening** | **2** (`material_mafia`, `circular_berlin`) | **+24 net** | −8 weak edges dropped |
| **Total** | **21** | **+52 net** | see [`EVIDENCE_DEEP_RESEARCH.md`](EVIDENCE_DEEP_RESEARCH.md) |

## Connectivity targets (post-apply)

| Test | Before | After | Target |
|---|---|---|---|
| `concular` ecosystem `VERBUNDEN` (excl. `dominik_campanella`) | 3 (people only) | **8** (incl. CDS, madaster, bremen, hannover) | ≥4 |
| `bauteilboerse_bremen` mesh | 2 | **5** (concular, hannover, hdM, …) | ≥2 |
| `bauteilboerse_hannover` spine | — | **5** (concular, restado, bremen, CDS, hdM) | ≥4 |
| `haus_der_materialisierung` hub | — | **4** (tu_berlin, kunst_stoffe_ev, material_mafia, circular_berlin) | ≥4 |
| `kunst_stoffe_ev` ↔ HdM | 0 | **linked** | operator |
| Hannover ↔ `bauteilnetz_deutschland` | — | **linked** | A evidence |
| Evidence-tagged rels (`review_run`) | 0 | **52** | — |

## New graph entities

- `bauteilboerse_hannover` (`:Akteur`)
- `haus_der_materialisierung` (`:Akteur`)
- `material_mafia` (`:Akteur`)
- `circular_berlin` (`:Akteur`)
- `q_research_germany_reuse_bubble_v1_md` + 23 `ExternalLink` quellen

## Phase 1c — dropped weak edges

- `circular_structural_design` ↔ `bauteilboerse_hannover` (no direct source)
- `haus_der_materialisierung` ↔ `bauteilboerse_bremen` / `hannover` (interpretive)
- `haus_der_materialisierung` ↔ `madaster_epea` (no co-project)

## Key new edges

- `concular` ↔ `circular_structural_design`, `madaster`, `madaster_epea`, `bauteilboerse_bremen`, `bauteilboerse_hannover`
- `concular` / `software_restado` / `bauteilboerse_bremen` / `bauteilboerse_hannover` / `circular_structural_design` — spine mesh
- `haus_der_materialisierung` ↔ `tu_berlin`, peer Bauteilbörsen, `madaster_epea`
- BELEGT_IN enrichment on concular, restado, bremen, CDS, madaster

## Still deferred (sidecar)

See [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md): Concular project cases, DIN tools as separate nodes.

## Reports

- [`apply_summary.json`](apply_summary.json)
- [`connectivity_report.json`](connectivity_report.json)
- Per-phase: [`apply_reports/`](apply_reports/)
- Plan: [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md)

## Re-run

```bash
# dry-run
python _neo4j/intake/runs/2026-06-05_germany_reuse_bubble/apply_germany_reuse_bubble.py

# apply (already done)
python _neo4j/intake/runs/2026-06-05_germany_reuse_bubble/apply_germany_reuse_bubble.py --commit
```
