# Remediation R02 — Dangling Nachweisforderung (Agent 13)

**Agent:** R02 · **Date:** 2026-06-06 · **Database:** `mit-bestand` (READ-ONLY audit; patch dry-run only)
**Input:** [`ledger/agent_13.csv`](../ledger/agent_13.csv) rows `A13-nf-dangle-0001`…`0018`
**Output ledger:** [`ledger/remediation_r02.csv`](../ledger/remediation_r02.csv)
**Patch (high-confidence only):** [`patches/remediation_r02_erfuellt_nachweis.patch.jsonl`](../patches/remediation_r02_erfuellt_nachweis.patch.jsonl)

## Executive summary

All **18** dangling `Nachweisforderung` nodes are **valid regulatory requirements** — each has
`ERFORDERT_NACHWEIS` demand edges (4–67) and `GESTUETZT_AUF_REGELWERK` legal backing (1–9 instruments).
The gap is **coverage**: Phase 5 `pruef_to_nf()` heuristic wired all 118 `PruefungNachweis` nodes to only
**9** of 27 requirement types, leaving 18 unsatisfiable.

- **High-confidence `ERFUELLT_NACHWEIS` patches drafted:** 10 edges covering **7** requirement types
- **Deferred (new `PruefungNachweis` needed):** 5
- **Deferred (medium-confidence only):** 6
- **DELETE / DEPRECATE proposed:** 0 (demands are sourced and structurally valid)

## Remediation status

| Status | Count |
|---|---:|
| DEFERRED_MEDIUM | 6 |
| DEFERRED_NEW_PN | 5 |
| PATCH_DRAFTED | 7 |

## Per-requirement decisions

| Nachweisforderung | Demands | R02 action | High-conf PN | Medium PN | New PN? |
|---|---:|---|---|---|---|
| `nf_oekobilanz_epd` | 67 | ADD_PRUEFUNGNACHWEIS | — | — | pn_epd_oder_lca_nachweis |
| `nf_materialpass_ressourcenpass` | 54 | ADD_PRUEFUNGNACHWEIS | — | — | pn_materialpass_oder_dpp |
| `nf_bauteilidentifikation` | 50 | ADD_ERFUELLT_NACHWEIS | pn_bauteilpass (belegt) | — | — |
| `nf_befestigungsnachweis` | 48 | ESCALATE_HUMAN | — | pn_ankerpruefung (teilweise_belegt) | — |
| `nf_schadstoffkataster_erkundung` | 39 | ESCALATE_HUMAN | — | pr_dokumentenpruefung_bestand (teilweise_belegt) | — |
| `nf_dauerhaftigkeit_restlebensdauer` | 35 | ESCALATE_HUMAN | — | pr_zustandsbewertung (teilweise_belegt) | — |
| `nf_holzschutzmittel_check` | 29 | ADD_ERFUELLT_NACHWEIS | pn_schadstoffanalyse_holz (belegt); pn_biozid_screening (belegt) | — | — |
| `nf_bauphysiknachweis` | 28 | ADD_ERFUELLT_NACHWEIS | pn_lambda_wert (belegt); pn_ug_wert (belegt); pn_ug_uw_wert (belegt) | — | — |
| `nf_genehmigungs_oder_zustimmungsbedarf` | 27 | ESCALATE_HUMAN | — | pn_approval_process (teilweise_belegt) | — |
| `nf_rc_gesteinskoernung_eignung` | 25 | ESCALATE_HUMAN | — | pn_petrografie (teilweise_belegt); pr_eignungspruefung_baulehm (teilweise_belegt) | — |
| `nf_barrierefreiheit_nachweis` | 18 | ADD_PRUEFUNGNACHWEIS | — | — | pn_barrierefreiheitsaudit |
| `nf_absturzsicherung` | 14 | ADD_ERFUELLT_NACHWEIS | pn_rutschhemmung (belegt) | — | — |
| `nf_asbest_check` | 10 | ADD_ERFUELLT_NACHWEIS | pr_schadstoffscreening (belegt) | — | — |
| `nf_elektrosicherheitsnachweis` | 7 | ADD_PRUEFUNGNACHWEIS | — | — | pn_elektrosicherheitspruefung |
| `nf_hygiene_und_reinigungsnachweis` | 7 | ADD_PRUEFUNGNACHWEIS | — | — | pn_trinkwasser_hygiene_nachweis |
| `nf_schwermetall_oder_bleifarbe_check` | 6 | ADD_ERFUELLT_NACHWEIS | pn_schwermetalle (belegt) | — | — |
| `nf_formaldehyd_oder_emissionsnachweis` | 5 | ADD_ERFUELLT_NACHWEIS | pn_schadstoffanalyse_kleber (belegt) | — | — |
| `nf_mineralische_ersatzbaustoff_guete` | 4 | ESCALATE_HUMAN | — | pr_eignungspruefung_baulehm (teilweise_belegt) | — |

## High-confidence patch ops

| PruefungNachweis → Nachweisforderung | Basis |
|---|---|
| `pn_schwermetalle` → `nf_schwermetall_oder_bleifarbe_check` | rewire_map SCHADSTOFF_TO_NF s_schwermetalle; pn_schwermetalle tests heavy metals/lead pain… |
| `pn_schadstoffanalyse_holz` → `nf_holzschutzmittel_check` | rewire_map SCHADSTOFF_TO_NF s_holzschutzmittel; wood preservative analysis… |
| `pn_biozid_screening` → `nf_holzschutzmittel_check` | biozid screening covers wood preservative / biocide residues (DIN 68800 AltholzV context)… |
| `pr_schadstoffscreening` → `nf_asbest_check` | IST_UNTERVERFAHREN_VON pr_schadstoffpruefung; screening is first-line pollutant check incl… |
| `pn_schadstoffanalyse_kleber` → `nf_formaldehyd_oder_emissionsnachweis` | rewire_map SCHADSTOFF_TO_NF s_formaldehyd; adhesive VOC/formaldehyde emissions… |
| `pn_rutschhemmung` → `nf_absturzsicherung` | la_rutschhemmung maps_to nf_absturzsicherung; slip-resistance test (DIN 51130 family)… |
| `pn_bauteilpass` → `nf_bauteilidentifikation` | Bauteilpass is component identification passport (DIN SPEC 91484 / Madaster / CDW protocol… |
| `pn_lambda_wert` → `nf_bauphysiknachweis` | la_waermeschutz maps_to nf_bauphysiknachweis; lambda value is thermal building-physics pro… |
| `pn_ug_wert` → `nf_bauphysiknachweis` | U-value measurement satisfies Bauphysiknachweis (GEG/MuKEn)… |
| `pn_ug_uw_wert` → `nf_bauphysiknachweis` | Ug/Uw thermal transmittance is Bauphysiknachweis evidence… |

## Root cause

Phase 5 `add_erfuellt_edges()` used `rewire_map.pruef_to_nf()` keyword heuristics that map test methods
to a **9-type** subset (`nf_materialpruefung`, `nf_schadstoffpruefung`, …). Pollutant-specific checks
(`nf_asbest_check`, …), documentation types (`nf_bauteilidentifikation`, `nf_oekobilanz_epd`), and
performance proofs (`nf_bauphysiknachweis`, `nf_befestigungsnachweis`) were never linked despite valid
`GESTUETZT_AUF_REGELWERK` + `ERFORDERT_NACHWEIS` demand.

## Medium-confidence candidates (not patched — human gate)

- `pn_ankerpruefung` → `nf_befestigungsnachweis` (teilweise_belegt): anchor pull-out test supports fastening proof (EN 1992-4 / facade anchorage)
- `pn_approval_process` → `nf_genehmigungs_oder_zustimmungsbedarf` (teilweise_belegt): approval / ZIE-ABZ pathway documentation (DIBt Zulassung)
- `pn_petrografie` → `nf_rc_gesteinskoernung_eignung` (teilweise_belegt): petrographic analysis for recycled aggregate suitability (DAfStb RC concrete)
- `pr_dokumentenpruefung_bestand` → `nf_schadstoffkataster_erkundung` (teilweise_belegt): pre-demolition document review / building pollutant register (VDI 6210 / ATV DIN 18459)
- `pr_eignungspruefung_baulehm` → `nf_rc_gesteinskoernung_eignung` (teilweise_belegt): suitability testing for mineral secondary aggregates / RC materials
- `pr_eignungspruefung_baulehm` → `nf_mineralische_ersatzbaustoff_guete` (teilweise_belegt): EBV Ersatzbaustoff suitability / quality assessment
- `pr_zustandsbewertung` → `nf_dauerhaftigkeit_restlebensdauer` (teilweise_belegt): condition assessment informs remaining service life (DIN SPEC 91525 PUC)

## Deferred — new PruefungNachweis required

- **`nf_oekobilanz_epd`** → propose `pn_epd_oder_lca_nachweis`: 67 demands; 9 GESTUETZT_AUF_REGELWERK (EN 15804/15978, EU Taxonomy). No EPD/LCA PruefungNachweis in catalog.
- **`nf_materialpass_ressourcenpass`** → propose `pn_materialpass_oder_dpp`: 54 demands; ESPR DPP / EU Level(s) backed. No material-passport / DPP procedure node.
- **`nf_elektrosicherheitsnachweis`** → propose `pn_elektrosicherheitspruefung`: 7 demands; rw_dguv_v3_vde. No electrical safety test procedure in PruefungNachweis vocab.
- **`nf_hygiene_und_reinigungsnachweis`** → propose `pn_trinkwasser_hygiene_nachweis`: 7 demands; rw_vdi_6023_6022 drinking-water hygiene. No matching procedure.
- **`nf_barrierefreiheit_nachweis`** → propose `pn_barrierefreiheitsaudit`: 18 demands; DIN 18040 backed. No accessibility audit procedure in catalog.

## Apply (human-gated)

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r02_erfuellt_nachweis.patch.jsonl
# then:
python _scripts/apply_neo4j_review_patch.py --patch ... --confirm "APPLY remediation_r02_erfuellt_nachweis.patch.jsonl TO mit-bestand"
```

## Dry-run output

```
el_check"
    },
    {
      "from": "pn_biozid_screening",
      "line": 3,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_holzschutzmittel_check"
    },
    {
      "from": "pr_schadstoffscreening",
      "line": 4,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_asbest_check"
    },
    {
      "from": "pn_schadstoffanalyse_kleber",
      "line": 5,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_formaldehyd_oder_emissionsnachweis"
    },
    {
      "from": "pn_rutschhemmung",
      "line": 6,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_absturzsicherung"
    },
    {
      "from": "pn_bauteilpass",
      "line": 7,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_bauteilidentifikation"
    },
    {
      "from": "pn_lambda_wert",
      "line": 8,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_bauphysiknachweis"
    },
    {
      "from": "pn_ug_wert",
      "line": 9,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_bauphysiknachweis"
    },
    {
      "from": "pn_ug_uw_wert",
      "line": 10,
      "op": "add_rel",
      "rel_type": "ERFUELLT_NACHWEIS",
      "status": "would_create_rel",
      "to": "nf_bauphysiknachweis"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\remediation_r02_erfuellt_nachweis.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\remediation_r02_erfuellt_nachweis.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "records": 10,
    "would_create_rel": 10
  }
}
```

Generated 2026-06-06 16:54 UTC.
