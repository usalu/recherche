# Rotor DC reuse bubble — apply summary

**Date:** 2026-06-05  
**Database:** `mit-bestand`  
**Review run:** `rotor_dc_reuse_bubble_2026_06_05`

## Result: applied successfully

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 2 335 | 2 356 | **+21** |
| Relationships | 15 451 | 15 477 | **+26** |

## Phases

| Phase | New nodes | New rels | Upgraded rels |
|---|---:|---:|---:|
| 0 — sources + dossier | 19 | 0 | 0 |
| 1 — ecosystem spine | 1 (`prog_preuse`) | 13 | 3 |
| 1b — publication hub | 0 | 1 | 2 |
| 2 — OXY hub | 1 (`p_oxy_centre_monnaie`) | 7 | 0 |
| 3 — material path | 0 | 5 | 2 |
| **Total** | **21** | **26** | **7** |

Note: phase 0 added **5 canonical quellen** that were missing from live graph despite June export (`q_url_150bfa71…`, `q_url_4a94cddf…`, `q_url_714d4c31…`, `q_chiro_…_s5`, `q_multi_…_s5`).

## Connectivity targets (post-apply)

| Test | Before | After | Target |
|---|---|---|---|
| `opalis` VERBUNDEN degree | 2 | **4** | ≥4 |
| `prog_preuse` partners | 0 | **4** (Rotor, bellastock, city_of_utrecht, brussels_environment) | ≥3 |
| opalis↔rotordc↔bellastock mesh | broken | **connected** | connected |
| `p_oxy_centre_monnaie` actors | — | **4** (Rotor, rotordc, whitewood, immobel) | ≥4 |
| Multi←Generale donor path | 0 | **1** (`HAT_BAUWERK`) | 1 |
| Evidence-tagged rels (`review_run`) | 0 | **33** | — |

## New graph entities

- `prog_preuse` (`:Programm`)
- `p_oxy_centre_monnaie` (`:Projekt`)
- `q_research_rotor_dc_reuse_bubble_v2_md` + 17 `ExternalLink` quellen

## Key new edges

- `opalis` ↔ `rotordc`, `opalis` ↔ `bellastock`
- `Rotor` / `bellastock` / `city_of_utrecht` / `brussels_environment` → `prog_preuse`
- `Rotor` / `rotordc` / `whitewood` / `immobel` → `p_oxy_centre_monnaie`
- `p_multi_brussels_reuse_in_multi` → `bw_generale_de_banque_brussels` (`HAT_BAUWERK`)
- `rotordc` → `bw_generale_de_banque_brussels` (`NUTZT_BAUWERK`)

## Reports

- [`apply_summary.json`](apply_summary.json)
- [`connectivity_report.json`](connectivity_report.json)
- Per-phase: [`apply_reports/`](apply_reports/)
- Post-apply centrality: [`centrality_report.json`](centrality_report.json)

## Re-run

```bash
# dry-run
python _neo4j/intake/runs/2026-06-05_rotor_dc_reuse_bubble/apply_rotor_dc_reuse_bubble.py

# apply (already done)
python _neo4j/intake/runs/2026-06-05_rotor_dc_reuse_bubble/apply_rotor_dc_reuse_bubble.py --commit
```
