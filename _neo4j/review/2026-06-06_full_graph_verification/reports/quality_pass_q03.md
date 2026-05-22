# Quality Pass Q03 — Compliance graph (Nachweisforderung residuals)

**Agent:** Q03 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Scope:** 11 `CONTRADICTION` dangling `Nachweisforderung` from EP-08 + R02 residuals
**Inputs:** [`ledger/element_proof_agent_08.csv`](../ledger/element_proof_agent_08.csv), [`ledger/remediation_r02.csv`](../ledger/remediation_r02.csv)
**Output ledger:** [`ledger/quality_pass_q03.csv`](../ledger/quality_pass_q03.csv)
**Patch:** [`patches/quality_pass_q03.patch.jsonl`](../patches/quality_pass_q03.patch.jsonl)

## Executive summary

- **New `PruefungNachweis` nodes created:** 5 (of 5 proposed; skipped if already present)
- **`ERFUELLT_NACHWEIS` edges added:** 12 (5 high-confidence, 7 medium-confidence)
- **Fully resolved (PROVEN):** 5 requirement types via new catalog procedures
- **Partial coverage (documented medium):** 6 requirement types — satisfiable but `teilweise_belegt`
- **Destructive ops:** 0

## Verdict transitions

| Verdict after | Count |
|---|---:|
| PARTIAL_COVERAGE | 6 |
| PROVEN | 5 |

## Per-requirement outcomes

| Nachweisforderung | Demands | F before → after | Q03 action | Confidence | Verdict after |
|---|---:|---|---|---|---|
| `nf_oekobilanz_epd` | 67 | 0 → 1 | ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT | belegt | PROVEN |
| `nf_materialpass_ressourcenpass` | 54 | 0 → 1 | ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT | belegt | PROVEN |
| `nf_barrierefreiheit_nachweis` | 18 | 0 → 1 | ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT | belegt | PROVEN |
| `nf_elektrosicherheitsnachweis` | 7 | 0 → 1 | ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT | belegt | PROVEN |
| `nf_hygiene_und_reinigungsnachweis` | 7 | 0 → 1 | ADD_PRUEFUNGNACHWEIS_AND_ERFUELLT | belegt | PROVEN |
| `nf_befestigungsnachweis` | 48 | 0 → 1 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |
| `nf_schadstoffkataster_erkundung` | 39 | 0 → 1 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |
| `nf_dauerhaftigkeit_restlebensdauer` | 35 | 0 → 1 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |
| `nf_genehmigungs_oder_zustimmungsbedarf` | 27 | 0 → 1 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |
| `nf_rc_gesteinskoernung_eignung` | 25 | 0 → 2 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |
| `nf_mineralische_ersatzbaustoff_guete` | 4 | 0 → 1 | ADD_MEDIUM_ERFUELLT_DOCUMENTED | teilweise_belegt | PARTIAL_COVERAGE |

## New PruefungNachweis catalog entries

| id | name | satisfies |
|---|---|---|
| `pn_epd_oder_lca_nachweis` | EPD- oder LCA-Nachweis | `nf_oekobilanz_epd` |
| `pn_materialpass_oder_dpp` | Materialpass oder DPP | `nf_materialpass_ressourcenpass` |
| `pn_barrierefreiheitsaudit` | Barrierefreiheitsaudit | `nf_barrierefreiheit_nachweis` |
| `pn_elektrosicherheitspruefung` | Elektrosicherheitsprüfung | `nf_elektrosicherheitsnachweis` |
| `pn_trinkwasser_hygiene_nachweis` | Trinkwasser-Hygiene-Nachweis | `nf_hygiene_und_reinigungsnachweis` |

## Medium-confidence mappings (documented, not upgraded to belegt)

| PruefungNachweis → Nachweisforderung | Basis |
|---|---|
| `pn_ankerpruefung` → `nf_befestigungsnachweis` | anchor pull-out test supports fastening proof (EN 1992-4 / facade anchorage)… |
| `pr_dokumentenpruefung_bestand` → `nf_schadstoffkataster_erkundung` | pre-demolition document review / building pollutant register (VDI 6210 / ATV DIN 18459)… |
| `pr_zustandsbewertung` → `nf_dauerhaftigkeit_restlebensdauer` | condition assessment informs remaining service life (DIN SPEC 91525 PUC)… |
| `pn_approval_process` → `nf_genehmigungs_oder_zustimmungsbedarf` | approval / ZIE-ABZ pathway documentation (DIBt Zulassung)… |
| `pn_petrografie` → `nf_rc_gesteinskoernung_eignung` | petrographic analysis for recycled aggregate suitability (DAfStb RC concrete)… |
| `pr_eignungspruefung_baulehm` → `nf_rc_gesteinskoernung_eignung` | suitability testing for mineral secondary aggregates / RC materials… |
| `pr_eignungspruefung_baulehm` → `nf_mineralische_ersatzbaustoff_guete` | EBV Ersatzbaustoff suitability / quality assessment… |

## Patch operations

```json
[
  {
    "op": "add_node",
    "id": "pn_epd_oder_lca_nachweis",
    "from": null,
    "to": null
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_epd_oder_lca_nachweis",
    "to": "nf_oekobilanz_epd"
  },
  {
    "op": "add_node",
    "id": "pn_materialpass_oder_dpp",
    "from": null,
    "to": null
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_materialpass_oder_dpp",
    "to": "nf_materialpass_ressourcenpass"
  },
  {
    "op": "add_node",
    "id": "pn_barrierefreiheitsaudit",
    "from": null,
    "to": null
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_barrierefreiheitsaudit",
    "to": "nf_barrierefreiheit_nachweis"
  },
  {
    "op": "add_node",
    "id": "pn_elektrosicherheitspruefung",
    "from": null,
    "to": null
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_elektrosicherheitspruefung",
    "to": "nf_elektrosicherheitsnachweis"
  },
  {
    "op": "add_node",
    "id": "pn_trinkwasser_hygiene_nachweis",
    "from": null,
    "to": null
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_trinkwasser_hygiene_nachweis",
    "to": "nf_hygiene_und_reinigungsnachweis"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_ankerpruefung",
    "to": "nf_befestigungsnachweis"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pr_dokumentenpruefung_bestand",
    "to": "nf_schadstoffkataster_erkundung"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pr_zustandsbewertung",
    "to": "nf_dauerhaftigkeit_restlebensdauer"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_approval_process",
    "to": "nf_genehmigungs_oder_zustimmungsbedarf"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pn_petrografie",
    "to": "nf_rc_gesteinskoernung_eignung"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pr_eignungspruefung_baulehm",
    "to": "nf_rc_gesteinskoernung_eignung"
  },
  {
    "op": "add_rel",
    "id": null,
    "from": "pr_eignungspruefung_baulehm",
    "to": "nf_mineralische_ersatzbaustoff_guete"
  }
]
```

## Dry-run output

```
"primary_source_url": "https://www.vdi.de/mitgliedschaft/vdi-richtlinien/unsere-richtlinien-highlights/vdi-6023",
          "review_run": "quality_pass_q03_2026-06-06",
          "source_scope": "regulation_graph_vocab_extension"
        }
      },
      "before": null,
      "id": "pn_trinkwasser_hygiene_nachweis",
      "line": 9,
      "op": "add_node",
      "status": "would_create"
    },
    {
      "from": "pn_trinkwasser_hygiene_nachweis",
      "line": 10,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_hygiene_und_reinigungsnachweis"
    },
    {
      "from": "pn_ankerpruefung",
      "line": 11,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_befestigungsnachweis"
    },
    {
      "from": "pr_dokumentenpruefung_bestand",
      "line": 12,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_schadstoffkataster_erkundung"
    },
    {
      "from": "pr_zustandsbewertung",
      "line": 13,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_dauerhaftigkeit_restlebensdauer"
    },
    {
      "from": "pn_approval_process",
      "line": 14,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_genehmigungs_oder_zustimmungsbedarf"
    },
    {
      "from": "pn_petrografie",
      "line": 15,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_rc_gesteinskoernung_eignung"
    },
    {
      "from": "pr_eignungspruefung_baulehm",
      "line": 16,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_rc_gesteinskoernung_eignung"
    },
    {
      "from": "pr_eignungspruefung_baulehm",
      "line": 17,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_mineralische_ersatzbaustoff_guete"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q03.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q03.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "records": 17,
    "would_create": 5,
    "would_create_rel": 12
  }
}
```

## Apply output

```
"primary_source_url": "https://www.vdi.de/mitgliedschaft/vdi-richtlinien/unsere-richtlinien-highlights/vdi-6023",
          "review_run": "quality_pass_q03_2026-06-06",
          "source_scope": "regulation_graph_vocab_extension"
        }
      },
      "before": null,
      "id": "pn_trinkwasser_hygiene_nachweis",
      "line": 9,
      "op": "add_node",
      "status": "would_create"
    },
    {
      "from": "pn_trinkwasser_hygiene_nachweis",
      "line": 10,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_hygiene_und_reinigungsnachweis"
    },
    {
      "from": "pn_ankerpruefung",
      "line": 11,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_befestigungsnachweis"
    },
    {
      "from": "pr_dokumentenpruefung_bestand",
      "line": 12,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_schadstoffkataster_erkundung"
    },
    {
      "from": "pr_zustandsbewertung",
      "line": 13,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_dauerhaftigkeit_restlebensdauer"
    },
    {
      "from": "pn_approval_process",
      "line": 14,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_genehmigungs_oder_zustimmungsbedarf"
    },
    {
      "from": "pn_petrografie",
      "line": 15,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_rc_gesteinskoernung_eignung"
    },
    {
      "from": "pr_eignungspruefung_baulehm",
      "line": 16,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_rc_gesteinskoernung_eignung"
    },
    {
      "from": "pr_eignungspruefung_baulehm",
      "line": 17,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_mineralische_ersatzbaustoff_guete"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q03.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q03.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "records": 17,
    "would_create": 5,
    "would_create_rel": 12
  }
}
```

Generated 2026-06-06 17:45 UTC.
