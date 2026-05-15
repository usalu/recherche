# Neo4j-Schema — flache Tabellen (`NEO4J_SCHEMA_MAP`)

**Normativ:** [`.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md`](../../.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) und die geplante Ergänzung in [`NEO4J_SCHEMA.md`](NEO4J_SCHEMA.md).

Diese Datei soll später **nur Tabellen** enthalten: je Label die erlaubten Properties; je Relationship-Typ erlaubte Quell-/Ziel-Labels, Kardinalität, Kanten-Properties — ohne erneute Prosa.

Bis der Tabellen-Port fertig ist, Kataloge aus dem Inventar aktualisieren mit:

`python _scripts/build_node_catalogs.py`
