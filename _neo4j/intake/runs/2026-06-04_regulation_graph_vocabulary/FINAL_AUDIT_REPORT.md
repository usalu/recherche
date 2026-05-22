# Final Audit Report - Regulation Graph Vocabulary Cleanup

- Generated: 2026-06-05T14:48:00+00:00
- Database: `mit-bestand`
- Final active graph: **2273 nodes / 15118 relationships / 51 active labels / 47 active relationship types**

## Scope

This report covers the executed cleanup phases 0-8 from `FINAL_PLAN_V2.md` plus **Phase B (Variant B typed law nodes)**:
encoding repair, source-node removal, property-only regulation overlay, legacy regulation retirement,
Schadstoff re-evidence, Pruefung/Leistungsanforderung consolidation, Huerde/reuse-chain cleanup, axis
demotion, relationship-type normalization, and re-import of 91 typed law nodes with overlay edges.

## Hard Acceptance Checks

- Quelle nodes: `0`
- Regelwerk nodes: `0`
- Status nodes: `0`
- HAT_STATUS rels: `0`
- Phase 8 retired rels: `0`
- Duplicate ERFORDERT_NACHWEIS pairs: `0`
- Duplicate HAT_BESCHAFFUNGSWEG pairs: `0`
- Typed law nodes (11-label Variant B): `91`
- GESTUETZT_AUF_REGELWERK: `167`
- GILT_IN_LAND (law → Land): `281`
- Duplicate GESTUETZT / GILT_IN_LAND pairs: `0`
- NF with active rechtsgrundlagen[]: `0`
- Legacy property → edge parity: `167/167`
- TRIGGERS_REGULIERUNGSFRAGE (unchanged): `1100`
- ERFORDERT_NACHWEIS (unchanged): `1483`
- Nodes with source_urls: `334` (+91 law nodes each with source_url)
- Nodes with legacy_internal_provenance_docs: `1442`
- NF with legacy_rechtsgrundlagen_from_variant_a[]: `27`
- Rels with source_url: `2981` (+448 Phase B overlay edges)

## Typed Law Labels (Phase B)

| Label | Nodes |
|---|---:|
| Tragwerksrecht | 26 |
| Bauproduktrecht | 23 |
| ReuseDokumentationsrecht | 18 |
| Schadstoffrecht | 17 |
| RueckbauUndAbbruchrecht | 16 |
| UmweltUndOekobilanzrecht | 13 |
| Bauphysikrecht | 10 |
| Brandschutzrecht | 8 |
| Genehmigungsrecht | 7 |
| HygieneElektroFunktionsrecht | 4 |
| Haftungsrecht | 3 |

48 law nodes carry multiple labels. Details: `VARIANT_B_TAXONOMY.md`.

## Retired Labels

- All planned retired labels are at `0` active nodes.
- `:Regelwerk` was never created in the live graph; Variant B uses typed `*recht` labels instead.

## Evidence Model

- `Quelle` is not an active node type.
- Case/project evidence remains on nodes and edges as properties (`source_url`, `source_quote`, etc.).
- Laws and standards are **typed navigable nodes** (`:Tragwerksrecht`, `:Schadstoffrecht`, …) linked via
  `GESTUETZT_AUF_REGELWERK` from `Nachweisforderung` and `GILT_IN_LAND` to `Land`.
- Variant A `rechtsgrundlagen[]` on `Nachweisforderung` is archived to `legacy_rechtsgrundlagen_from_variant_a[]`.
- URL-less internal markdown provenance remains as `legacy_internal_provenance_docs[]` (subordinate to web URLs).

## Rollback

- Phase B snapshot: `phaseB_before.json`
- Delete Phase B writes: `review_run = regulation_graph_vocab_2026_06_04_phaseB`
- Restore NF arrays from `legacy_*_from_variant_a[]` if needed

## Remaining Relationship Types

- `HAT_AKTEURROLLE`: 1496
- `ERFORDERT_NACHWEIS`: 1483
- `TRIGGERS_REGULIERUNGSFRAGE`: 1100
- `HAT_BAUTEILTYP`: 871
- `HAT_AKTEURTYP`: 701
- `HAT_PROZESSPHASE`: 679
- `LIEGT_IN_LAND`: 653
- `NUTZT_MATERIAL`: 633
- `HAT_BESCHAFFUNGSWEG`: 592
- `BETEILIGT_AN`: 584
- `HAT_LOGISTIK`: 434
- `HAT_MATERIALGRUPPE`: 403
- `HAT_BAUTEILGRUPPE`: 364
- `HAT_RUECKBAUVERFAHREN`: 308
- `VERBUNDEN_MIT_AKTEUR`: 295
- `HAT_ERGEBNIS`: 294
- `GILT_IN_LAND`: 281
- `IN_EMPFANGSOBJEKT`: 278
- `HAT_AUFBEREITUNG`: 267
- `HAT_RESSOURCENQUELLE`: 264
- `HAT_KENNWERT`: 255
- `LIEGT_IN_STADT`: 252
- `AUS_SPENDER`: 245
- `HAT_METHODE`: 244
- `HAT_HUERDE`: 237
- `HAT_NUTZUNG`: 235
- `HAT_BAUOBJEKTROLLE`: 225
- `HAT_BAUWERK`: 193
- `GESTUETZT_AUF_REGELWERK`: 167
- `HAT_INTERVENTION`: 144
- `HAT_BAUWEISE`: 124
- `ERFUELLT_NACHWEIS`: 118
- `HAT_VERBINDUNGSTECHNIK`: 110
- `HAT_SCHADSTOFFRISIKO`: 100
- `HAT_GESCHAEFTSMODELL`: 98
- `TYPISCH_BEI_MATERIAL`: 74
- `HAT_BAUSYSTEM`: 61
- `HAT_DEFEKT`: 57
- `NUTZT_SOFTWARE`: 54
- `ERFORDERT_SCHADSTOFFPRUEFUNG`: 37
- `TEIL_VON_PROGRAMM`: 35
- `HAT_ZUSTANDSKLASSE`: 18
- `TYPISCH_BEI_ERA`: 15
- `BETRIEBEN_VON`: 10
- `TYPISCH_BEI_BAUTEILTYP`: 10
- `IST_UNTERVERFAHREN_VON`: 9
- `GEBAUT_IN_ERA`: 8
- `ERHALT_FOERDERUNG_DURCH`: 3
