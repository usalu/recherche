# Migration Report — Digitale-Wiederverwendungs-Hürden-Taxonomie

**Date:** 2026-08-06 · **Branch:** agent_s4/schema-cleanup · **DB:** mit-bestand · **review_run:** `digital_barriers_2026_08_06`
**Status:** APPLIED and verified green.

## What changed
| | Before | After |
|---|---:|---:|
| Nodes | 2263 | **2670** (+409 taxonomy, −2 dropped) |
| Relationships | 14571 | **14948** (+401 hierarchy, +9 classify, −33 dropped) |

- **+409 framework nodes** (8 domains A–H `:HuerdeKategorie`, 66 categories, 343 leaves `:Huerde`), all marked `:BarriereReferenz`, carrying `barriere_code`, `name`, `name_en`, `definition_de`, `review_run`, `source_*`.
- **+401 `HAT_HUERDEKATEGORIE`** hierarchy edges (child→parent).
- **9 observed live hurdles reclassified** under their natural family (+9 `HAT_HUERDEKATEGORIE`, `category` string removed). They keep their real project/BG `HAT_HUERDE` edges and are NOT marked (invariant: `barriere_code` ⟺ `:BarriereReferenz`).
- **2 hurdles dropped** (`Entwurfsbindung` 28 edges, `Ausschreibungsproblem` 5 edges = 33) — no natural home in this taxonomy, approved data loss.

## Deviation from approved plan
`Fehlende_Lagerflaeche` was **classified under `H5 Lagerfähigkeit`** as its own observed leaf instead of **merged** into the framework leaf `H5.1`. Rationale: avoids `merge_node` property-union reintroducing the English `category`/name onto `H5.1`; keeps a clean observed/framework invariant. Net data effect identical (its 14 edges sit under storage). `H5.1 Keine Lagerkapazität` remains a marked reference leaf. Approved by user before apply.

## Verification (live, all pass)
domains=8 · framework_nodes=409 · unmarked_framework=0 · parent_anomalies=0 · HAT_HUERDE total=204 · targeting_category=0 · dropped nodes gone · Fehlende_Lagerflaeche present w/ category removed · 9 reclassified (category removed, 1 parent each, 0 wrongly marked).

## Artifacts
`taxonomy_source*.tsv` · `build_taxonomy.py` · `taxonomy_de.kg.jsonl` · `code_id_map.csv` · `classify_and_drop.patch.jsonl` · `verify_taxonomy.cypher` · apply reports in `_neo4j/review/apply_reports/classify_and_drop.patch.apply_report.{json,md}`

## Backups / rollback
- Pre:  `_neo4j/review/backups/20260806T104607Z-mit-bestand` (2263 / 14571)
- Post: `_neo4j/review/backups/20260806T113610Z-mit-bestand` (2670 / 14948)
- Additive rollback: `MATCH (n {review_run:'digital_barriers_2026_08_06'}) DETACH DELETE n` (removes taxonomy nodes + all review_run edges incl. the 9 classify edges).
- Full rollback (incl. the 2 dropped hurdles + 33 edges): restore the PRE backup via `restore_neo4j_graph_backup.py --confirm "RESTORE mit-bestand FROM 20260806T104607Z-mit-bestand"`.

## Out of scope (next evidenced pass)
Cross-links (`VERURSACHT`/`VERSTAERKT`…), `:Plattformfunktion`, `:Massnahme`, and `:Prozessphase`/`:Akteurrolle`/`:Norm` links — all require per-edge sourcing.
