# BG Hunt Campaign Report

**Generated:** 2026-06-07T14:25:14Z · **Database:** `mit-bestand` · **Mode:** dry-run only

## Fleet summary

| Agent | processed |
|---|---:|
| BG-01 | 200 |
| BG-02 | 200 |
| BG-03 | 0 |
| BG-04 | 0 |
| BG-05 | 0 |
| BG-06 | 0 |

**Merged rows:** 400
**Conflicts (duplicate element_id):** 0

## Verdict outcomes (hunted edges)

| verdict_after | count |
|---|---:|
| UNSUPPORTED | 250 |
| PARTIAL | 136 |
| PROVEN | 14 |

## Upgrade metrics
- PROVEN upgrades (patch-eligible): **14**
- Patch ops emitted: **14**
- Dry-run status: **ok** (returncode=0)

## v6 → v7 bg_ UNSUPPORTED
- v6 UNSUPPORTED bg_ rels: **852**
- v7 UNSUPPORTED bg_ rels: **702**
- Reduction: **150** (17.6%)

## v7 PROVEN % (bg_ rels)
- bg_ rel rows: **6684**
- PROVEN: **5782** (86.51%)

## Artifacts
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\bg_hunt_merged.csv`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\patches\bg_hunt_upgrades.patch.jsonl`
- `E:\recherche\_neo4j\review\2026-06-06_full_graph_verification\VERIFICATION_LEDGER_ELEMENT_v7.csv`

## Dry-run tail
```
},
      "before": {
        "count": 1,
        "from": "bg_stahl_mehrere_tbc_repurposed_cleveland",
        "properties": {
          "id": "r_bg_reuse_stahl_mehrere_tbc_repurposed_cleveland__NUTZT_MATERIAL__mat_stahl"
        },
        "rel_internal_id": 1153001768955675092,
        "to": "mat_stahl",
        "type": "NUTZT_MATERIAL"
      },
      "from": "bg_stahl_mehrere_tbc_repurposed_cleveland",
      "line": 13,
      "op": "set_rel_properties",
      "status": "would_update_rel",
      "to": "mat_stahl",
      "type": "NUTZT_MATERIAL"
    },
    {
      "after_properties": {
        "evidence_basis": "bg_hunt_alias_match",
        "evidence_confidence": "high",
        "evidence_quote": "T\u00fcren, Fenster und Sanit\u00e4r im CRCLR-Gesamtprojekt mit unscharfer Fit-out-Zuordnung",
        "evidence_url": "https://www.buildingsocialecology.org/projects/crclr-house-berlin/",
        "id": "r_bg_reuse_mehrere_mehrere_impact_crclr_doors_windows_sanitary__HAT_BAUTEILTYP__bt_fenster",
        "review_run": "bg_hunt_2026_06_07"
      },
      "before": {
        "count": 1,
        "from": "bg_mehrere_mehrere_impact_crclr_doors_windows_sanitary",
        "properties": {
          "id": "r_bg_reuse_mehrere_mehrere_impact_crclr_doors_windows_sanitary__HAT_BAUTEILTYP__bt_fenster"
        },
        "rel_internal_id": 1152988574816141672,
        "to": "bt_fenster",
        "type": "HAT_BAUTEILTYP"
      },
      "from": "bg_mehrere_mehrere_impact_crclr_doors_windows_sanitary",
      "line": 14,
      "op": "set_rel_properties",
      "status": "would_update_rel",
      "to": "bt_fenster",
      "type": "HAT_BAUTEILTYP"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\bg_hunt_upgrades.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\bg_hunt_upgrades.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "records": 14,
    "would_update_rel": 14
  }
}

```
