# Cross-bubble extension — apply summary

**Run:** `cross_bubble_extension_2026_06_06`  
**Database:** `mit-bestand`  
**Applied:** 2026-06-06 (phase 1 + phase 2)

## Counts

| | Nodes | Relationships |
|---|---:|---:|
| Before | 2 304 | 15 527 |
| After phase 1 | 2 304 | 15 538 |
| After phase 2 | 2 304 | **15 556** |
| Total delta | 0 | **+29** |

## Changes

| Op | Target | Effect |
|---|---|---|
| upgrade | `insert_marketplace` ↔ `madaster` | teilweise_belegt → **belegt** (formal partnership) |
| enrich | `software_restado` | first-party URL `restado.de/ueber-restado` |
| new | `madaster` ↔ `madaster_epea` | platform-family mesh (belegt) |
| new | `concular` ↔ `software_restado` | marketplace brand operator (belegt) |
| new | `opalis` → `prog_preuse` | maintained under PREUSE (belegt) |
| new | `software_restado` ↔ `opalis` | European reuse peer (teilweise_belegt) |
| new | `software_restado` ↔ `insert_marketplace` | DE ↔ NL marketplace peer (teilweise_belegt) |
| new | `cirkla` ↔ `software_restado` | CH ↔ DE reuse infrastructure peer (teilweise_belegt) |

## Phase 2 (Swiss hub + HdM + Rotor-DC)

| Op | Target | Effect |
|---|---|---|
| new | `sumami` ↔ `cirkla`, `eth_zuerich`, `circular_hub_zurich` | Swiss reuse hub enrichment (belegt) |
| new | `kunst_stoffe_ev` ↔ `material_mafia` / `circular_berlin` | HdM DBU consortium mesh (belegt) |
| new | `rotordc` ↔ `whitewood` / `immobel` | OXY project commissioner links (belegt) |
| new | `brussels_environment` ↔ `opalis` | PREUSE funder ↔ platform (belegt) |
| new | `useagain_bauteilclick` ↔ `software_restado` | CH ↔ DE marketplace peer (teilweise_belegt) |
| upgrade | `city_of_utrecht` ↔ `madaster` | PREUSE Utrecht pilot evidence (belegt) |

## Cross-bubble bridges now at 1–2 hops

- Germany (`concular` / `software_restado`) ↔ Belgium/France (`opalis` / `prog_preuse`)
- Germany ↔ Netherlands (`software_restado` ↔ `insert_marketplace`)
- Switzerland (`cirkla` / `useagain`) ↔ Germany (`software_restado`) — **1 hop** via useagain
- Switzerland (`sumami` / `eth_zuerich`) ↔ European mesh via `cirkla` → `software_restado` → `opalis`
- Netherlands (`madaster`) ↔ Germany (`madaster_epea`) direct
- NL ↔ BE programme: `city_of_utrecht` → `prog_preuse` → `opalis` → `brussels_environment`

## Import both patches (confirmed 2026-06-06)

```powershell
python _neo4j/review/2026-06-06_cross_bubble_extension/apply_cross_bubble_both.py --commit
```

Re-run result: **34 records noop** (11+18 existing rels, 3 property upgrades already applied). Graph stable at **2 304 / 15 556**.

## Artifacts

- Plan: [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md)
- Evidence: [`EVIDENCE_REGISTER.csv`](EVIDENCE_REGISTER.csv)
- Patches: [`patches/cross_bubble_extension.patch.jsonl`](patches/cross_bubble_extension.patch.jsonl), [`patches/cross_bubble_extension_phase2.patch.jsonl`](patches/cross_bubble_extension_phase2.patch.jsonl)
- Combined apply: [`apply_cross_bubble_both.py`](apply_cross_bubble_both.py), [`apply_both_summary.json`](apply_both_summary.json)
- Reports: [`apply_reports/`](apply_reports/)
