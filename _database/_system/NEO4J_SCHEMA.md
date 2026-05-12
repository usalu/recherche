# Neo4j-Schema (Research-Graph)

**Normativer Katalog:** [`.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`](../../.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) — 52 Primär-Labels, fünf Kantentypen, §6.1 Organisation-Akteure, §5.4 ohne bestimmte Inventar-Knoten, §7.1 Relation-Folding.

Diese Datei ist die geplante **narrative** Spiegelung des Plans (Knotentypen, Eigenschaften, Kanten, Anhänge A–G). Solange der vollständige Text hier noch ausgebaut wird, gilt **ausschließlich** der verlinkte Plan als Quelle der Wahrheit.

**Import:** `_scripts/import_database_folder_to_neo4j.py` (Inventar + Kanten), optional `_scripts/export_visual_attachment_to_neo4j.py` (Demo-Knoten aus `neo4j_schema_visual_nodes_attachment.md`). **Preflight-Reihenfolge:** siehe `HANDOFF.md` Abschnitt *Neo4j import preflight*. Label-Helfer: `_scripts/akteur_org_neo4j_label.py`, `_scripts/ort_geo_label.py`, `_scripts/software_tool_label.py`.

**Abhängigkeiten:** `requirements-neo4j.txt` im Repository-Root.

## CSV-Ontologie vs. Neo4j-Kantentypen

Die Spalte **`relation`** in `_database/_edges/clean_confirmed_edges.csv` (Vollständige Token-Liste, Zählungen und Neo4j-Faltung: `_database/_system/RELATION_CATALOG_NEO4J.md`; narrative Regeln: `SCHEMA.md` §9) enthält **viele** snake_case-Prädikate (`has_*`, `belongs_to_*`, …). Das sind **Ontologie-/CSV-Schicht**-Namen, **keine** Neo4j-Relationship-Typen.

Der Research-Graph verwendet genau **fünf** Typen: **`IST`**, **`HAT`**, **`BENUTZT`**, **`GEHÖRT_ZU`**, **`BELEGT_IN`**. Lifecycle-Zuordnungen zu **`(:Status)`** sind ebenfalls **`HAT`**, mit **`art: "status"`** (kein eigener Relationship-Typ). Beim Import mappt **`_scripts/neo4j_relation_fold.py`** jede erlaubte CSV-`relation` auf einen dieser Typen und setzt die Kanten-Properties (`art`, `rolle`, `axis`, …); CSV-only Relationen ohne Graph-Kante (`has_tooltyp`, `has_projekt`, …) werden übersprungen. Zusätzlich steht auf jeder importierten Kante die Audit-Property **`csv_relation`** (Original-Token).
