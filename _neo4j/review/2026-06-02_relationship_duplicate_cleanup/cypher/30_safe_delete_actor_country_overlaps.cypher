// Safe delete of redundant GEHÖRT_ZU actor-country edges.
// Canonical edge: LIEGT_IN_LAND.

MATCH (a:Akteur)-[r:GEHÖRT_ZU]->(l:Land)
WHERE coalesce(r.rolle, '') = 'land'
  AND EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
DELETE r;