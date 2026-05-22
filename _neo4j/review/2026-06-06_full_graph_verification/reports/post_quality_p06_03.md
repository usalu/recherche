# Post Quality Pass P6-03 — Structural dedup + RAU merge

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/post_quality_p06_03.csv`](../ledger/post_quality_p06_03.csv)
**Patch:** [`patches/post_quality_p06_03.patch.jsonl`](../patches/post_quality_p06_03.patch.jsonl)
**Review run:** `post_quality_p06_03_2026_06_06`

## Live graph baseline

| Metric | Value |
|---|---:|
| Nodes | 2264 |
| Directed rels | 15063 |
| `VERBUNDEN_MIT_AKTEUR` (undirected count) | 496 |
| Live bidirectional VMA pairs | 0 |
| Degree-0 `Akteur` | 0 |

## Scope summary

| Scope | Topic | Ledger rows | Patch ops |
|---|---|---:|---:|
| A | Bidirectional `VERBUNDEN_MIT_AKTEUR` | 13 | 0 `delete_rel` |
| B | Q5 orphan `Akteur` SCHEMA | 3 | 0 (R05 already applied) |
| C | `rau` ↔ `rau_architects` merge | 1 | 1 `merge_node` |

## Verdicts

- **PROVEN:** 1
- **REMEDIATED:** 16

## Proposed actions

- **KEEP:** 16
- **MERGE_DUPLICATE:** 1

## Patch (evidence-gated: `merge_node` + `delete_rel` only)

```json
{"op": "merge_node", "from": "rau_architects", "to": "rau", "reason": "P6-03 P6-03-RAU-001: PROVEN duplicate firm — RAU Architects on Liander HQ = architectural firm RAU (thomasrau.eu/en/initiatives/rau)"}
```

## Dry-run apply

```
        },
        "to": {
          "labels": [
            "Akteur"
          ],
          "properties": {
            "id": "rau",
            "name": "RAU",
            "primary_source_url": "https://thomasrau.eu/en/initiatives/rau",
            "source_titles": [
              "Thomas Rau"
            ],
            "source_urls": [
              "https://thomasrau.eu/en/initiatives/rau"
            ]
          }
        }
      },
      "from": "rau_architects",
      "label_union": [
        "Akteur"
      ],
      "line": 1,
      "op": "merge_node",
      "rel_inbound_to_redirect": 0,
      "rel_outbound_to_redirect": 4,
      "status": "would_merge",
      "to": "rau"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\post_quality_p06_03.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\post_quality_p06_03.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "records": 1,
    "would_merge": 1
  }
}
```

## Notes

- Bidirectional VMA dedup from Agent 14/Q5 was applied across wave-1 (`merge_duplicate_edges_remaining.patch.jsonl`, 23 ops), Agent 06b (63 ops), and R04 (`remediation_r04_madaster_rau_harvestmap.patch.jsonl`).
- Q5 orphan `Akteur` nodes were connected via R05 `LIEGT_IN_LAND` — not re-patched here.
- `rau` vs `thomas_rau` remains **distinct** (firm vs person; R04 PROVEN).

## Apply (human gate)

```bash
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/post_quality_p06_03.patch.jsonl
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/post_quality_p06_03.patch.jsonl --confirm "APPLY post_quality_p06_03.patch.jsonl TO mit-bestand"
```
