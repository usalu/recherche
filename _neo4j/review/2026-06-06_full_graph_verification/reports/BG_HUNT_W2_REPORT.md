# BG Hunt Wave 2 Report

**Generated:** 2026-06-07T14:32:35Z · **Database:** `mit-bestand`

## Fleet summary

| Agent | processed |
|---|---:|
| BG-W2-01 | 150 |
| BG-W2-02 | 150 |
| BG-W2-03 | 2 |

**Merged rows:** 302
**Conflicts:** 0

## Verdict outcomes (hunted edges)

| verdict_after | count |
|---|---:|
| UNSUPPORTED | 156 |
| PARTIAL | 131 |
| PROVEN | 15 |

## Upgrade metrics
- PROVEN upgrades (patch-eligible): **15**
- W2 patch ops emitted: **15**
- Dry-run status: **ok**
- W2 apply status: **ok** · ops applied: **15**

## v7 → v8 bg_ UNSUPPORTED
- v7 UNSUPPORTED bg_ rels: **702**
- v8 UNSUPPORTED bg_ rels: **556**
- Reduction (wave 2 hunt overlay): **146**

## v8 PROVEN % (bg_ rels)
- bg_ rel rows: **6684**
- PROVEN: **5797** (86.73%)

## Graph counts (final)
- Nodes: **2263**
- Relationships: **14571**

## Artifacts
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\bg_hunt_w2_merged.csv`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\bg_hunt_upgrades_w2.patch.jsonl`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\bg_hunt_upgrades_all.patch.jsonl`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\VERIFICATION_LEDGER_ELEMENT_v8.csv`
