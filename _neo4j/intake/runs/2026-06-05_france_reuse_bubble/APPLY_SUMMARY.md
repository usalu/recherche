# France reuse bubble — apply summary

**Date:** 2026-06-05  
**Database:** `mit-bestand`  
**Review run:** `france_reuse_bubble_2026_06_05`

## Result: applied successfully (incl. phase 1c hardening)

| Metric | Before | After initial | After 1c | Total delta |
|---|---:|---:|---:|---:|
| Nodes | 2 384 | 2 402 | **2 412** | **+28** |
| Relationships | 15 529 | 15 569 | **15 583** | **+54 net** |

## Phases

| Phase | New nodes | New rels | Notes |
|---|---:|---:|---|
| 0 — sources + dossier | 18 | 0 | 1 dossier + 17 `ExternalLink` quellen |
| 1 — French marketplace spine | 0 | 35 | bellastock ↔ opalis ↔ backacia ↔ cycle_up ↔ mobius mesh |
| 2 — Île-de-France civic links | 0 | 5 | `association_reavie` ↔ bellastock / mobius |
| **1c — evidence hardening** | **1** (`mineka`) + 9 quellen | **+14 net** | −6 weak edges; 11 upgrades |
| **Total** | **28** | **+54 net** | see [`EVIDENCE_DEEP_RESEARCH.md`](EVIDENCE_DEEP_RESEARCH.md) |

## Connectivity targets (post-apply)

| Test | Before | After | Target |
|---|---|---|---|
| `bellastock` ecosystem `VERBUNDEN` (excl. people) | 1 (`opalis`) | **6** | ≥4 |
| `opalis` ecosystem `VERBUNDEN` (excl. `maarten_gielen`) | 3 | **7** (+ `backacia`, `cycle_up`, `association_reavie`, `mineka`) | ≥5 |
| `cycle_up` spine | 0 | **4** | ≥4 |
| `backacia` spine | 0 | **4** | ≥3 |
| `mobius_reemploi` spine (excl. people) | 0 | **4** (+ `cstb`) | ≥2 |
| `opalis` ↔ `backacia` | 0 | **linked** (A evidence) | yes |
| `mobius_reemploi` ↔ `cstb` (SPIROU) | 0 | **linked** | yes |
| `association_reavie` ↔ `bellastock` | 0 | **linked** | yes |
| `opalis` ↔ `association_reavie` | 0 | **linked** | yes |
| `mineka` spine | — | **4** (opalis, bellastock, cycle_up, backacia) | ≥4 |
| Evidence-tagged rels (`review_run`) | 0 | **54** | — |

## Phase 1c — dropped weak edges

- `mobius_reemploi` ↔ `cycle_up` (independent reconditioners, no co-project)
- `raedificare` ↔ `backacia` (RAEDIFICARE not on Opalis)
- `association_reavie` ↔ `mobius_reemploi` (regional inference only)

## Phase 1c — upgrades and new entity

- **Upgraded to `belegt`:** opalis↔cycle_up, bellastock↔backacia/cycle_up/association_reavie, cycle_up↔backacia
- **New:** `mineka` (`:Akteur`) via Opalis + ADEME 40-reseller study
- **New A edges:** opalis↔association_reavie; BELEGT_IN Fabrique du Clos on bellastock

## Enriched actors (no duplicates)

Existing isolated French actors connected to EU spine:

- `cycle_up`, `backacia`, `mobius_reemploi`, `raedificare` — marketplace / reconditioning layer
- `cstb` — SPIROU + REPAR BELEGT_IN
- `association_reavie` — Île-de-France civic cluster (not new `reavie` id)

## Key new edges

- `opalis` ↔ `backacia` — Opalis supplier directory (belegt)
- `mobius_reemploi` ↔ `cstb` — SPIROU consortium (belegt)
- `bellastock` ↔ `cstb` — REPAR programme (belegt)
- `cycle_up` ↔ `backacia` / `opalis` / `bellastock` — French marketplace mesh
- BELEGT_IN on bellastock, opalis, cycle_up, backacia, mobius, cstb, raedificare

## Still deferred (sidecar)

See [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md): `mineka`, `booster_du_reemploi`, demonstrator projects, `prog_spirou` as node.

## Reports

- [`apply_summary.json`](apply_summary.json)
- [`connectivity_report.json`](connectivity_report.json)
- Per-phase: [`apply_reports/`](apply_reports/)
- Plan: [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md)
- Tests: [`CONNECTIVITY_TESTS.cypher`](CONNECTIVITY_TESTS.cypher)

## Re-run

```bash
# dry-run (initial phases)
python _neo4j/intake/runs/2026-06-05_france_reuse_bubble/apply_france_reuse_bubble.py

# hardening only (already done)
python _neo4j/intake/runs/2026-06-05_france_reuse_bubble/apply_france_reuse_bubble.py --hardening-only --commit
```
