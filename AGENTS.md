Sie sind ein Assistent, der hilft Wissen zu strukturieren und zu vernetzen.

Daraus wird der **Research-Graph in Neo4j** importiert (Quelle der Wahrheit: [`.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`](.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md), Import: `_scripts/import_database_folder_to_neo4j.py`). Optional kann lokal noch eine **SQLite**-Datei aus dem gleichen Baum gebaut werden; sie gehört nicht zwingend ins Repository (siehe `.gitignore`).

**Kanonisches Arbeitsverzeichnis:** `research/` — nicht die Archivkopien unter `_archive/`. Vokabular und Kantenregeln: `research/_system/SCHEMA.md`, Neo4j-Faltung: `_scripts/neo4j_relation_fold.py`.

Ordnerstruktur (unter `research/`):

- ENTITÄT
  - ID
    - index.md # Alle Informationen zu der Entität
      - # UNTERTHEMA // Titel des Unterthemas mit Inhalt
    - DATEIEN
