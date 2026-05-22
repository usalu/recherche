// Read-only post-cleanup validation queries.
// Run these in Neo4j Browser or through MCP read-cypher.

MATCH (n)-[:BELEGT_IN]->(a:OntologyAnchor)
WHERE EXISTS { MATCH (n)-[:ANCHORED_BY]->(a) }
RETURN count(*) AS remaining_ontology_anchor_overlaps;

MATCH (p:Projekt)-[:NUTZT_BAUWERK]->(b:Bauwerk)
WHERE EXISTS { MATCH (p)-[:HAS_BAUWERK]->(b) }
RETURN count(*) AS remaining_project_bauwerk_overlaps;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(l:Land)
WHERE coalesce(g.rolle, '') = 'land'
  AND EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
RETURN count(*) AS remaining_actor_country_overlaps;

MATCH (a:Akteur)-[:STUB_PROJECT_LINK]->(x)
WHERE EXISTS { MATCH (a)-[:BETEILIGT_AN]->(x) }
RETURN count(*) AS remaining_stub_beteiligt_overlaps;

MATCH (a:Akteur)-[:GEHÖRT_ZU]->(b:Akteur)
WHERE EXISTS { MATCH (a)-[:VERBUNDEN_MIT_AKTEUR]->(b) }
RETURN count(*) AS remaining_membership_generic_overlaps;

MATCH (p:Projekt)-[:NUTZT_BAUWERK]->(b:Bauwerk)
WHERE NOT EXISTS { MATCH (p)-[:HAS_BAUWERK]->(b) }
RETURN count(*) AS remaining_nutzt_bauwerk_residuals;

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(l:Land)
WHERE coalesce(g.rolle, '') = 'land'
  AND NOT EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
RETURN count(*) AS remaining_actor_country_residuals;