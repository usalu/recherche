# Edges (`_database/_edges/`)

- **`clean_confirmed_edges.csv`** — canonical typed edges (`source`, `target`, `relation`, …). Imported into Neo4j via `_scripts/import_database_folder_to_neo4j.py` with folding from `_scripts/neo4j_relation_fold.py` (plan §7.1).
- **`clean_edge_review_queue.csv`** — optional manual-review queue (currently empty header only). Used by frozen `_migration/43_apply_manual_review_decisions.py` if repopulated.
- **`RELATION_CATALOG_NEO4J.md`** (under `_database/_system/`) — regenerate with `python _scripts/extract_database_relations.py`.

Before assuming import safety, run **`python _scripts/verify_plan_coverage.py`** (must exit 0).
