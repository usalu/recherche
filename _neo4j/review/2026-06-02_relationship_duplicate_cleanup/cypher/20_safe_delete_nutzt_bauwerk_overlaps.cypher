// Safe delete of redundant NUTZT_BAUWERK edges on Projekt -> Bauwerk.
// Canonical edge: HAS_BAUWERK.

MATCH (p:Projekt)-[r:NUTZT_BAUWERK]->(b:Bauwerk)
WHERE EXISTS { MATCH (p)-[:HAS_BAUWERK]->(b) }
DELETE r;