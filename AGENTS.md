Sie sind ein Assistent, der hilft, Wissen für den **Neo4j-Graphen** zu strukturieren, zu prüfen und nachvollziehbar zu importieren.

## Aktuelle Wahrheit

- **Neo4j ist die Quelle der Wahrheit.**
- Es gibt **kein** aktives `research/`-Arbeitsverzeichnis mehr.
- `_archive/research/` ist historisch und darf nicht stillschweigend als kanonische Quelle benutzt werden.
- Alles, was noch auf `research/` oder `_database/` verweist, ist Altbestand und muss vor Wiederverwendung geprüft oder aktualisiert werden.

## Wissens-Korpus vs. Neo4j-Maschinerie

- Menschlich lesbare Forschung (Dossiers, Themen, Synthese) liegt jetzt unter `_knowledge/` —
  siehe [`_knowledge/README.md`](_knowledge/README.md).
- `_neo4j/` enthält nur noch Graph-Maschinerie: Transport, Import, Audits, Provenienz, Schemata.
- `_archive/research/` bleibt unveränderter **Kaltbestand** und darf **nicht** in `_knowledge/` einfließen.

## Aktuelle Arbeitslogik unter `_neo4j/`

- `processed/` — bereinigte, importierbare Artefakte und Provenienz aus bereits bearbeiteten Intakes; **nicht** die Quelle der Wahrheit.
- `intake/inbox/` — neue Rohlieferungen werden hier abgelegt.
- `intake/archive/` — unveränderte historische Rohlieferungen nach der Verarbeitung.
- `intake/runs/` — Berichte je Verarbeitungslauf.
- `contracts/` — gültige Eingabeformate, Schemata und Vorlagen.
- `review/` — Prüfprotokolle für Altbestand und unsichere Ableitungen.

## Wichtige Regeln

1. Import-Chunks und Batches sind Transportformen, keine dauerhaften semantischen Einheiten.
2. Beim Zusammenführen muss Provenienz erhalten bleiben: Quelle, Lauf, Merge-Art, Review-Status.
3. Ähnlichkeit von Namen ist **kein** ausreichender Grund für automatisches Mergen.
4. Rohdaten aus archivierten Altstrukturen dürfen nur nach expliziter Prüfung wieder in aktuelle Neo4j-Workflows einfließen.
5. Neue Agenten lesen zuerst `_neo4j/README.md` und `_neo4j/review/LEGACY_LINEAGE_AUDIT.md`.

## Intake evidence (reuse bubbles and new intakes)

- **URLs and evidence live only on graph node/relationship properties** — not in sidecar JSONL, not as extra `:Quelle:ExternalLink` intake nodes.
- **Entity nodes:** `primary_source_url`, `source_urls` (list).
- **Relationships:** `evidence_url`, `evidence_quote`, `evidence_confidence`, `evidence_basis`, `review_run`.
- **Do not import:** `BELEGT_IN` → synthetic `q_url_*` quellen, `evidence_source_id`, `archive_source_id`, `metadata_sidecar_key`, `evidence_claim_ids`.
- Dossier markdown stays in `intake/inbox/`; not mirrored as `:Quelle:ResearchDocument` unless legacy graph already requires it.
- Cleanup reference: [`_neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/CLEANUP_SUMMARY.md`](_neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/CLEANUP_SUMMARY.md).

## Sidecar metadata (property cleanup 4b/5b only)

- Offloaded rel QA metadata and filtered `source_titles` live under `_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/`.
- Graph pointer property: `metadata_sidecar_key` on nodes and relationships (**legacy cleanup scope only** — not for new intakes).
- Drop-list for titles: `source_title_drop_patterns.txt` in the same review folder.

## Nicht mehr als Standard verwenden

- `_scripts/import_database_folder_to_neo4j.py`
- alte `research/`- oder `_database/`-Dokumentation
- `_archive/research/` als Arbeitsquelle

Diese Dinge sind nur noch Legacy-Kontext, bis sie ausdrücklich geprüft und neu freigegeben wurden.

## Aktueller Stand (2026-06-06)

Der Regulation-Graph-Vocabulary-Cleanup (Plan:
[`_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md))
ist bis Phase 8 + **Phase B (Variant B, 11 typed law labels)** angewendet, danach Abschluss-OP S1–S5
([`LAST_SURGERY_REPORT.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/LAST_SURGERY_REPORT.md)):
alle Schadstoff-/Regelungskanten belegt, 30 Bauteilgruppen verbunden, Dubletten/Waisen bereinigt.
Aktiver Graph-Stand in `mit-bestand`: **2,263 Knoten / 15,060 Relationen** (nach Final-Cleanup F1–F3
2026-06-06: `rau` merge, redirect re-proofs, externals pass; Aggregator F10: **17,323 Element-Zeilen**, **89.36 % PROVEN** — Details
[`CAMPAIGN_CLOSEOUT_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/CAMPAIGN_CLOSEOUT_REPORT.md),
[`FINAL_COVERAGE_PROOF.md`](_neo4j/review/2026-06-06_full_graph_verification/FINAL_COVERAGE_PROOF.md)).
Vor Final Cleanup (P6-06): 2,264 / 15,063 — **89.27 % PROVEN** auf 17,327 Zeilen —
[`POST_QUALITY_CAMPAIGN_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/POST_QUALITY_CAMPAIGN_REPORT.md).
Property-Cleanup 2026-06-05: **57 Knoten-Property-Keys** (war 107), **22 Rel-Property-Keys** (war 63) —
[`CLEANUP_APPLY_SUMMARY.md`](_neo4j/review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md);
live property-key drift (**81** node / **50** rel) dokumentiert in F6 closeout.
Remediation-Details: [`REMEDIATION_PLAN.md`](_neo4j/review/2026-06-06_full_graph_verification/REMEDIATION_PLAN.md).