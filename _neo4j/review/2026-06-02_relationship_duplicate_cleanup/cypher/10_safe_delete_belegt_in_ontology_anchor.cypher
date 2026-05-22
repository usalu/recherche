// Safe delete of redundant BELEGT_IN edges to OntologyAnchor.
// Canonical edge: ANCHORED_BY.

MATCH (n)-[r:BELEGT_IN]->(a:OntologyAnchor)
WHERE EXISTS { MATCH (n)-[:ANCHORED_BY]->(a) }
DELETE r;