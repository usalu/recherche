// Read-only validation and review queries for relationship duplicate cleanup.
// Run these in Neo4j Browser or through MCP read-cypher, not through _run_cypher_file.py,
// because you need the returned rows.

// Safe overlap counts
MATCH (n)-[:BELEGT_IN]->(a:OntologyAnchor)
WHERE EXISTS { MATCH (n)-[:ANCHORED_BY]->(a) }
RETURN count(*) AS overlapping_ontology_anchor_pairs;

MATCH (p:Projekt)-[:NUTZT_BAUWERK]->(b:Bauwerk)
WHERE EXISTS { MATCH (p)-[:HAS_BAUWERK]->(b) }
RETURN count(*) AS overlapping_project_bauwerk_pairs;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(l:Land)
WHERE coalesce(g.rolle, '') = 'land'
  AND EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
RETURN count(*) AS overlapping_actor_country_pairs;

// Residual review sets
MATCH (p:Projekt)-[nb:NUTZT_BAUWERK]->(b:Bauwerk)
WHERE NOT EXISTS { MATCH (p)-[:HAS_BAUWERK]->(b) }
RETURN p.id AS project_id,
       p.name AS project_name,
       b.id AS bauwerk_id,
       b.name AS bauwerk_name,
       nb.id AS nutzt_bauwerk_rel_id,
       nb.evidence_confidence AS nutzt_bauwerk_confidence
ORDER BY project_id, bauwerk_id;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(l:Land)
WHERE coalesce(g.rolle, '') = 'land'
  AND NOT EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
RETURN a.id AS actor_id,
       a.name AS actor_name,
       l.id AS land_id,
       l.name AS land_name,
       g.id AS gehoert_zu_rel_id,
       g.evidence_confidence AS gehoert_zu_confidence
ORDER BY actor_id, land_id;

MATCH (a:Akteur)-[s:STUB_PROJECT_LINK]->(x)
WHERE EXISTS { MATCH (a)-[:BETEILIGT_AN]->(x) }
RETURN a.id AS actor_id,
       a.name AS actor_name,
       labels(x) AS target_labels,
       x.id AS target_id,
       x.name AS target_name,
       s.id AS stub_rel_id,
       keys(s) AS stub_keys,
       s.not_confirmed_project_participation AS stub_not_confirmed_participation,
       s.association_basis AS stub_association_basis
ORDER BY actor_id, target_id;

MATCH (a:Akteur)-[s:STUB_PROJECT_LINK]->(x)
MATCH (a)-[b:BETEILIGT_AN]->(x)
RETURN sum(CASE WHEN coalesce(s.not_confirmed_project_participation, false) = true OR s.association_basis IS NOT NULL THEN 1 ELSE 0 END) AS stub_should_win_count,
       sum(CASE WHEN coalesce(s.not_confirmed_project_participation, false) = false AND s.association_basis IS NULL THEN 1 ELSE 0 END) AS beteiligt_should_win_count;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(b:Akteur)
MATCH (a)-[v:VERBUNDEN_MIT_AKTEUR]->(b)
RETURN a.id AS from_actor_id,
       a.name AS from_actor_name,
       b.id AS to_actor_id,
       b.name AS to_actor_name,
       g.id AS gehoert_zu_rel_id,
       v.id AS verbunden_rel_id,
       keys(v) AS verbunden_keys,
       v.connection_kind AS verbunden_connection_kind,
       v.inference_basis AS verbunden_inference_basis
ORDER BY from_actor_id, to_actor_id;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(b:Akteur)
MATCH (a)-[v:VERBUNDEN_MIT_AKTEUR]->(b)
RETURN sum(CASE WHEN coalesce(g.evidence_confidence, '') IN ['', 'unklar'] AND coalesce(v.evidence_confidence, '') = 'teilweise_belegt' THEN 1 ELSE 0 END) AS confidence_upgrades_from_verbunden,
       count(*) AS total_membership_overlaps;