# Project-Part-Actor Import All

Date: 2026-06-01

Decision: import all 91 Akteur -> Bauteilgruppe BETEILIGT_AN edges from the latest
`project_part_actor_edge_enrichment_existing_node_types_2026_06_01` slice now,
while keeping the imported relationships explicitly marked for later source review.

Files:

- `_run_import_all.py` - write-capable Neo4j importer keyed on semantic node IDs.
- `MUST_FIND_EVIDENCE.md` - short deferred-evidence packet for later delivery.

What the importer writes:

- `evidence_confidence = abgeleitet` for all 91 imported edges until user confirmation
- `import_original_evidence_confidence = <source slice value>` preserves `belegt` / `abgeleitet_belegt` / `abgeleitet` from the JSON
- `review_run = project_part_actor_import_all_2026_06_01`
- `import_decision = import_all_for_now`
- `review_status = needs_source_url_review`
- `source_resolution_status = needs_source_url_review`
- `source_status = candidate`
- `candidate_source_urls = evidence_urls`

Run from repo root:

```powershell
python _neo4j/intake/runs/2026-06-01_project_part_actor_import_all/_run_import_all.py
```

Connection defaults:

- `NEO4J_URI`: `neo4j://127.0.0.1:7687`
- `NEO4J_USER` or `NEO4J_USERNAME`: `neo4j`
- `NEO4J_DATABASE`: `mit-bestand`
- password: `NEO4J_PASSWORD` or `.neo4j_password`

Post-import lookup:

```cypher
MATCH (:Akteur)-[r:BETEILIGT_AN {review_run:'project_part_actor_import_all_2026_06_01'}]->(:Bauteilgruppe)
RETURN count(r) AS imported_edges;
```