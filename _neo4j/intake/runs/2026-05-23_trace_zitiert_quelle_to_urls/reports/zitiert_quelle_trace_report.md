# Trace `:ZITIERT_QUELLE` to concrete URLs

Completed UTC: 2026-05-23T10:52:08.057158+00:00
Database: mit-bestand
Migration: `mig_trace_zitiert_quelle_to_urls_2026_05_23`

## Result

- Pre-existing `:ZITIERT_QUELLE` inventory rows: 8229
- Resolved URL legacy rows: 8219
- Non-URL legacy rows retired/review-marked: 10
- `:ZITIERT_QUELLE` deleted: 8229
- `:ZITIERT_QUELLE` remaining: 0
- Source nodes stamped from legacy URL hops: 1978
- Direct URL endpoint relationships stamped: 6699
- `evidence_source_id` single-URL relationships stamped: 64
- `evidence_source_id` multi-URL relationships stamped: 3693
- Relationships marked for source URL review: 17278
- Source trace `DataIssue` nodes: 17281
- Bad `:CITED_FROM_DOSSIER` URL/locator rows: 0

## Review Queue By Relationship Type

- HAT_HUERDE: 1068
- HAT_PROZESSPHASE: 812
- HAS_RISK_POLLUTANT: 803
- HAT_STATUS: 672
- HAT_AKTEURROLLE: 632
- HAT_WIEDERVERWENDUNGSART: 621
- HAT_BAUTEILTYP: 607
- HAT_METHODE: 602
- BETEILIGT_AN: 576
- HAT_RESSOURCENQUELLE: 567
- HAT_LEISTUNGSANFORDERUNG: 561
- HAT_MATERIALGRUPPE: 516
- HAT_LOGISTIK: 500
- NUTZT_MATERIAL: 475
- HAT_AKTEURTYP: 465
- ANCHORED_BY: 443
- HAT_AUFBEREITUNG: 426
- HAT_MARKTMODELL: 384
- HAT_BAUTEILEBENE: 372
- INTO_RECEIVER: 349
- REQUIRES_VERIFICATION_FOR: 347
- HAT_PRUEFUNG: 347
- LIEGT_IN_LAND: 319
- HAT_RUECKBAUVERFAHREN: 301
- HAT_FUNKTIONSWECHSEL: 299
- FROM_DONOR: 286
- HAT_BESCHAFFUNGSWEG: 285
- LIEGT_IN_STADT: 261
- GEHÖRT_ZU: 255
- HAT_BAUOBJEKTROLLE: 230

## Ledgers

- `_neo4j\intake\runs\2026-05-23_trace_zitiert_quelle_to_urls\logs\zitiert_quelle_edge_inventory.jsonl`
- `_neo4j\intake\runs\2026-05-23_trace_zitiert_quelle_to_urls\logs\zitiert_quelle_resolution_ledger.jsonl`
- `_neo4j\intake\runs\2026-05-23_trace_zitiert_quelle_to_urls\logs\information_source_url_ledger.jsonl`
- `_neo4j\intake\runs\2026-05-23_trace_zitiert_quelle_to_urls\logs\source_url_unresolved_review.jsonl`

## Backup

- `_neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls`

## Post-Migration Marker Pass

Completed after the main migration:

- Source-trace `DataIssue` nodes with `source_scope`: 17,281
- New source-trace `CONCERNS` relationships given IDs: 34,561
- URL-less domain/source nodes marked for review: 299
- Node URL gaps without review marker: 0
- Final `:ZITIERT_QUELLE` relationships: 0

Supplementary report:
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/post_migration_review_markers.json`

## Strict Binding Cleanup

User requirement: never imply a URL supports a fact unless the binding is exact.

The first migration had stored document-level multi-URL sets on 3,693
relationships as `source_urls` with a review status. That was too easy to
misread as factual support. The strict cleanup moved them to
`candidate_source_urls` and removed them from trusted source fields.

- Candidate URL-set relationships demoted: 3,693
- Trusted relationship URL bindings remaining: 12,913
- Domain/source nodes recomputed from trusted incident `source_url` only: 355
- Nodes with candidate URL sets needing review: 1,765
- Nodes marked as lacking trusted source URL: 1,809
- Candidate URL sets still in trusted `source_urls`: 0
- Final `:ZITIERT_QUELLE` relationships: 0

Strict cleanup artefacts:
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_source_url_binding_cleanup.json`
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/strict_candidate_source_url_review.jsonl`

Backup before strict cleanup:
- `_neo4j/review/backups/2026-05-23_pre_strict_source_url_binding_cleanup`

## Invalid URL Cleanup

Additional anti-hallucination gates found malformed/truncated URL strings that
must not be exposed as source evidence.

- Malformed relationship `source_url` values demoted: 72
- Malformed trusted relationship URLs remaining: 0
- Malformed node `source_urls` entries filtered: 39
- Malformed node `source_url` values removed: 32
- Malformed node trusted URLs remaining: 0
- Malformed candidate URL entries filtered from relationships: 1,392
- Malformed candidate URL entries filtered from nodes: 1,088
- Malformed candidate URLs remaining: 0
- Trusted relationship URL bindings after cleanup: 12,841
- Candidate relationship URL sets after cleanup: 3,693

Invalid cleanup artefacts:
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_invalid_url_cleanup.json`
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_node_url_array_cleanup.json`
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_candidate_url_array_cleanup.json`
- `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/strict_invalid_source_url_review.jsonl`
