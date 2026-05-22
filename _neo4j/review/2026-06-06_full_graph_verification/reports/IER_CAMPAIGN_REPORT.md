# IER Campaign Report — Internet Evidence Recovery

**Agent:** IER-AGG (Aggregator)
**Date:** 2026-06-07
**Database:** `mit-bestand` (read-only; patch dry-run only)
**Baseline:** `VERIFICATION_LEDGER_ELEMENT.csv`
**Output:** `VERIFICATION_LEDGER_ELEMENT_v2.csv`

---

## 1. Campaign outcome

| Criterion | Status |
|---|---|
| D1 — every shard row merged | **1,504** unique in-scope rows (1,520 raw) |
| D2 — disjointness on element_id | ⚠️ 16 B2/C5 overlaps (resolved) |
| D4 — P0 gate violations addressed | ✅ (12/12 in `ier_p0.csv`) |
| D5 — v2 ledger + PROVEN% | **16,038 / 17,109 = 93.74%** |
| D6 — patch JSONL (not applied) | ✅ dry-run: **PASS** |
| D7 — no empty-quote PROVEN in v2 | ✅ |

## 2. PROVEN% lift — actual vs expected

| Metric | Baseline | v2 actual | Expected (mid) | Δ actual | Δ vs expected |
|---|---:|---:|---:|---:|---:|
| Element rows | 17,323 | 17,109 | ~17,170 | -214 | — |
| PROVEN rows | 15,499 | 16,038 | — | +539 | — |
| PROVEN % | 89.47% | **93.74%** | **92.5%** | **+4.27 pp** | +1.24 pp |
| In-scope upgrades → PROVEN | — | 542 | ~549 | — | -7 |
| Row removals (DELETE) | — | 214 | ~150 | — | +64 |

**Headline:** **93.74% PROVEN** (+4.27 pp vs baseline) vs plan mid-case **92.5%**.

## 3. Verdict distribution

| Verdict | Baseline | v2 | Δ |
|---|---:|---:|---:|
| PROVEN | 15,499 | 16,038 | +539 |
| UNVERIFIABLE | 102 | 357 | +255 |
| MISSING_EVIDENCE | 877 | 323 | -554 |
| PARTIAL | 807 | 316 | -491 |
| CONTRADICTION | 5 | 42 | +37 |
| SCHEMA_VIOLATION | 33 | 33 | +0 |

## 4. IER shard inputs

| Agent | Ledger rows |
|---|---:|
| IER-P0 | 12 |
| IER-A1 | 165 |
| IER-A2 | 162 |
| IER-B1 | 197 |
| IER-B2 | 41 |
| IER-C12 | 292 |
| IER-C3 | 164 |
| IER-C4 | 362 |
| IER-C5 | 125 |
| **Σ raw** | **1,520** |
| **Σ unique (deduped)** | **1,504** |

**Note:** IER-B1 shard has **197** rows (plan cited 223; 26 tier-D inferred `BETEILIGT_AN` excluded per disjointness rules — see `ier_b1_report.md`).

## 5. Overlay statistics

| Metric | Count |
|---|---:|
| Baseline rows in IER scope (matched) | 1,324 |
| IER overlays applied | 1,324 |
| Upgrades to PROVEN | 542 |
| From MISSING_EVIDENCE → PROVEN | 185 |
| From PARTIAL → PROVEN | 357 |
| Rows pruned (DELETE action) | 214 |
| Gate auto-downgrades (empty quote) | 0 |

## Shard overlaps (16 element_id collisions)

Disjointness rule D2 violated between **IER-B2** and **IER-C5** on `HAT_BAUWERK` rows (16 element_ids).
Aggregator resolved by wave priority (**IER-B2** wins over **IER-C5**).

| element_id | shards | verdicts |
|---|---|---|
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['UNSUPPORTED', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11530875308…` | IER-B2, IER-C5 | ['PARTIAL', 'MISSING_EVIDENCE'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11553393306…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11553393306…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11553393306…` | IER-B2, IER-C5 | ['PROVEN', 'PARTIAL'] |
| `5:5f542910-8dcf-46a9-a77c-dfff0c64ee65:11553393306…` | IER-B2, IER-C5 | ['PARTIAL', 'PARTIAL'] |

## 6. Patch consolidation

| File | Ops |
|---|---:|
| `patches/ier_evidence_recovery.patch.jsonl` | 184 |
| `patches/ier_evidence_recovery_deletes.patch.jsonl` | 214 (human-gated) |

### Evidence patch op breakdown

| Operation | Count |
|---|---:|
| `set_node_properties` | 172 |
| `set_rel_properties` | 12 |

**Sources merged:** `ier_p0.patch.jsonl`, `ier_a1_fix_node_sources.patch.jsonl`, `ier_c12_fix_node_sources.patch.jsonl`

### Dry-run result (`apply_neo4j_review_patch.py`, no `--confirm`)

```
"
          ]
        }
      },
      "id": "workspot",
      "line": 174,
      "op": "set_node_properties",
      "status": "would_update"
    },
    {
      "after": {
        "labels": [
          "Akteur"
        ],
        "properties": {
          "id": "bioregional",
          "name": "BioRegional",
          "primary_source_url": "https://www.bioregional.com",
          "review_run": "ier_c12_2026_06_06",
          "source_quote": "Purpose-led sustainability consultancy \u2013 Bioregional Back to home About About Bioregional About us Careers - we're hiring!",
          "source_titles": [
            "BedZED_London_Hackbridge\u2026"
          ]
        }
      },
      "before": {
        "labels": [
          "Akteur"
        ],
        "properties": {
          "id": "bioregional",
          "name": "BioRegional",
          "source_titles": [
            "BedZED_London_Hackbridge\u2026"
          ]
        }
      },
      "id": "bioregional",
      "line": 175,
      "op": "set_node_properties",
      "status": "would_update"
    },
    {
      "after": {
        "labels": [
          "Akteur"
        ],
        "properties": {
          "id": "icon_real_estate",
          "name": "Icon Real Estate",
          "primary_source_url": "https://www.icon-real-estate.com",
          "review_run": "ier_c12_2026_06_06",
          "source_quote": "ICON Real Estate BUY/RENT/SELL Expert Guidance for Every Step of Your Journey Find Your Dream Property Today!"
        }
      },
      "before": {
        "labels": [
          "Akteur"
        ],
        "properties": {
          "id": "icon_real_estate",
          "name": "Icon Real Estate"
        }
      },
      "id": "icon_real_estate",
      "line": 176,
      "op": "set_node_properties",
      "status": "would_update"
    },
    {
      "after": {
        "labels": [
          "Akteur"
        ],
        "properties": {
          "id": "2hs",
          "name": "2hs",
          "primary_source_url": "https://www
…
```

Exit code: **0** — **PASS**

## 7. Output paths

| Artifact | Path |
|---|---|
| v2 ledger | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\VERIFICATION_LEDGER_ELEMENT_v2.csv` |
| Merged IER shard | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\ier_merged.csv` |
| Evidence patch | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\ier_evidence_recovery.patch.jsonl` |
| DELETE patch (gated) | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\ier_evidence_recovery_deletes.patch.jsonl` |
| Synthesis JSON | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_ier_aggregate_work\synthesis.json` |
| Disjointness JSON | `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_ier_aggregate_work\disjointness.json` |

---

*IER aggregator — read-only Neo4j export not required; patch dry-run only.*
