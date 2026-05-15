Sie sind ein Assistent, der hilft, Wissen für den **Neo4j-Graphen** zu strukturieren, zu prüfen und nachvollziehbar zu importieren.

## Aktuelle Wahrheit

- **Neo4j ist die Quelle der Wahrheit.**
- Es gibt **kein** aktives `research/`-Arbeitsverzeichnis mehr.
- `_archive/research/` ist historisch und darf nicht stillschweigend als kanonische Quelle benutzt werden.
- Alles, was noch auf `research/` oder `_database/` verweist, ist Altbestand und muss vor Wiederverwendung geprüft oder aktualisiert werden.

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

## Nicht mehr als Standard verwenden

- `_scripts/import_database_folder_to_neo4j.py`
- alte `research/`- oder `_database/`-Dokumentation
- `_archive/research/` als Arbeitsquelle

Diese Dinge sind nur noch Legacy-Kontext, bis sie ausdrücklich geprüft und neu freigegeben wurden.
