# Phase L applied - denormalized payload extracted into edges

Goal: extract everything extractable from `ReuseRule`/`Land` properties into the
node structure, reusing existing nodes, creating new nodes only when necessary,
no data loss, no edge without clear evidence. Full per-token mapping recorded in
`MAPPING_PREVIEW.md`.

## Already-modeled redundancy dropped (no new edges needed)
- `material_id` / `material` == existing `APPLIES_TO -> Material` (20/20) -> dropped
- `country_iso` / `country_name` == existing `APPLIES_IN -> Land` (20/20) -> dropped
- `key_norms`: 92/93 tokens already had `REFERENZIERT_NORM` edges; added the 1
  missing (`rr_de_lehm -> DIN 18940 family`), then dropped the key.

## New edges created (reusing existing target nodes)
| edge | count | target |
| --- | --- | --- |
| `HAS_RISK_POLLUTANT` | 96 | `Schadstoff` |
| `HAT_PRUEFUNG` | 108 | `PruefungNachweis` |
| `HAT_AUFBEREITUNG` | 76 | `Aufbereitungsverfahren` |
| `HAT_RECHTLICHE_BEDINGUNG` | 15 | `RechtlicheBedingung` (new rel type, existing nodes) |
| `REFERENZIERT_NORM` | 1 | `Norm` |
| `REGULIERT` | 25 | `(Land)-[:REGULIERT {jahr,basis,note}]->(Schadstoff)` |

All 320 new edges received deterministic `r.id` (Phase J backfill); gap survey
`r.id NULL = 0`.

## New nodes (only the necessary, recurring real contaminants)
4 `Schadstoff`: `s_schimmel` (Mold), `s_chlorid` (Chlorides), `s_mineraloel`
(Oil), `s_salze` (Salts). Everything else mapped to pre-existing nodes.

## No data loss
Unmatched free-text tokens (133) were **kept** in their residual arrays on
`ReuseRule` (`required_tests`, `processing_methods`, `legal_conditions`,
`pollutant_risks`) - these are phrasings with no clear existing-node equivalent
(e.g. "Product-vs-waste status", "Tracimat inventory", "Frost", "Species",
"New bolted connections"). They were deliberately NOT linked (no edge without
clear evidence) and remain queryable.

## Land pollutant-years
`asbest_verbot_jahr`, `pcb_verbot_jahr`, `kmf_grenzwert_jahr`,
`asbest_neshap_year`, `asbest_note` -> moved onto `REGULIERT` edges, then dropped.
`country_iso2` / `country_short` kept (legitimate attributes).

## Outcome
- In-use node property keys: **60 -> 50**.
- Relationships: 23,990 -> 24,310 (+320 evidence-bearing edges).
- New nodes: +4 `Schadstoff` (5,450 -> 5,454).
- Gap survey: no new failures (the 4 BELEGT_IN / 1 MATERIALGRUPPE / 2
  WIEDERVERWENDUNGSART are pre-existing relationship gaps, untouched here).

## Still on ReuseRule (intentionally kept)
- `source_url` / `source_urls` / `primary_source_url`: 5 unique URLs not yet a
  `Quelle` (see `MANUAL_REMODEL_CANDIDATES.md` section 1).
- `rank`, `priority`, `project_cluster`: scalar attributes (not node-extractable).
- residual free-text arrays (above).

Backup: `_neo4j/review/backups/2026-06-01_pre_phaseL_remodel/`.
