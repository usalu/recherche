// Neo4j Browser — select database: mit-bestand
//
// ═══════════════════════════════════════════════════════════════════════════
// RUN THIS FIRST IN NEO4J BROWSER: it only READS the graph and RETURNS rows
// whose "cypher" column holds each query — copy from the TABLE view.
// ═══════════════════════════════════════════════════════════════════════════

RETURN 1 AS nr, 'edge count' AS name,
'MATCH ()-[r]->() RETURN count(r) AS relationship_count;' AS cypher
UNION ALL RETURN 2 AS nr, 'sample edges' AS name,
'MATCH (a)-[r]->(b) RETURN labels(a)[0] AS from_label, a.id AS from_id, type(r) AS rel_type, labels(b)[0] AS to_label, b.id AS to_id LIMIT 50;' AS cypher
UNION ALL RETURN 3 AS nr, 'graph sample' AS name,
'MATCH p = (a)-[r]->(b) RETURN p LIMIT 25;' AS cypher
UNION ALL RETURN 4 AS nr, 'akteur family + projekt (all touching rels)' AS name,
'MATCH (a)-[r]-(b) WHERE (a:akteur OR a:akteur_beteiligung OR a:akteurrolle OR a:projekt OR b:akteur OR b:akteur_beteiligung OR b:akteurrolle OR b:projekt) RETURN a, r, b;' AS cypher
UNION ALL RETURN 5 AS nr, 'akteur family + projekt (tabular per rel)' AS name,
'MATCH (a)-[r]-(b) WHERE (a:akteur OR a:akteur_beteiligung OR a:akteurrolle OR a:projekt OR b:akteur OR b:akteur_beteiligung OR b:akteurrolle OR b:projekt) WITH r, startNode(r) AS s, endNode(r) AS e RETURN s AS from_node, type(r) AS rel_type, e AS to_node, r AS rel_props ORDER BY rel_type, from_node.id, to_node.id;' AS cypher
UNION ALL RETURN 6 AS nr, 'bauweise material projekt (undirected)' AS name,
'MATCH (a)-[r]-(b) WHERE (a:bauweise OR a:material OR a:projekt) AND (b:bauweise OR b:material OR b:projekt) RETURN a, r, b;' AS cypher
UNION ALL RETURN 7 AS nr, 'bauweise material projekt (directed)' AS name,
'MATCH (a)-[r]->(b) WHERE (a:bauweise OR a:material OR a:projekt) AND (b:bauweise OR b:material OR b:projekt) RETURN a, type(r), b;' AS cypher
UNION ALL RETURN 8 AS nr, 'material projekt Quelle (datenpunkt)' AS name,
'MATCH (re:reuse_einsatz)-[:belongs_to_projekt]->(p:projekt) MATCH (re)-[:uses_material]->(m:material) MATCH (d:datenpunkt)-[:belongs_to_projekt]->(p) WHERE toLower(d.id) CONTAINS ''quelle'' OR toLower(d.ref) CONTAINS ''quelle'' RETURN m, re, p, d;' AS cypher
UNION ALL RETURN 9 AS nr, 'material projekt rel props Quelle' AS name,
'MATCH (a)-[r]-(b) WHERE (a:material OR b:material OR a:projekt OR b:projekt) AND ANY(k IN keys(r) WHERE toLower(toString(r[k])) CONTAINS ''quelle'') RETURN a, r, b LIMIT 100;' AS cypher
ORDER BY nr;

// ───────────────────────────────────────────────────────────────────────────
// Below: run each block separately (not the catalog above at the same time).
// ───────────────────────────────────────────────────────────────────────────

// --- sanity: edges exist ---
MATCH ()-[r]->()
RETURN count(r) AS relationship_count;

// --- sample edges (tabular) ---
MATCH (a)-[r]->(b)
RETURN labels(a)[0] AS from_label, a.id AS from_id,
       type(r) AS rel_type,
       labels(b)[0] AS to_label, b.id AS to_id
LIMIT 50;

// --- graph sample ---
MATCH p = (a)-[r]->(b)
RETURN p
LIMIT 25;

// --- akteur / akteur_beteiligung / akteurrolle / projekt: every rel touching any of them ---
MATCH (a)-[r]-(b)
WHERE (a:akteur OR a:akteur_beteiligung OR a:akteurrolle OR a:projekt
    OR b:akteur OR b:akteur_beteiligung OR b:akteurrolle OR b:projekt)
RETURN a, r, b;

// --- same, one row per relationship ---
MATCH (a)-[r]-(b)
WHERE (a:akteur OR a:akteur_beteiligung OR a:akteurrolle OR a:projekt
    OR b:akteur OR b:akteur_beteiligung OR b:akteurrolle OR b:projekt)
WITH r, startNode(r) AS s, endNode(r) AS e
RETURN s AS from_node, type(r) AS rel_type, e AS to_node, r AS rel_props
ORDER BY rel_type, from_node.id, to_node.id;

// --- bauweise, material, projekt: edges only between these labels (undirected match) ---
MATCH (a)-[r]-(b)
WHERE (a:bauweise OR a:material OR a:projekt)
  AND (b:bauweise OR b:material OR b:projekt)
RETURN a, r, b;

// --- same, directed ---
MATCH (a)-[r]->(b)
WHERE (a:bauweise OR a:material OR a:projekt)
  AND (b:bauweise OR b:material OR b:projekt)
RETURN a, type(r), b;

// --- material + projekt + "Quelle" (datenpunkt id/ref on same projekt) ---
MATCH (re:reuse_einsatz)-[:belongs_to_projekt]->(p:projekt)
MATCH (re)-[:uses_material]->(m:material)
MATCH (d:datenpunkt)-[:belongs_to_projekt]->(p)
WHERE toLower(d.id) CONTAINS 'quelle' OR toLower(d.ref) CONTAINS 'quelle'
RETURN m, re, p, d;

// --- material or projekt: any adjacent rel whose props contain "quelle" ---
MATCH (a)-[r]-(b)
WHERE (a:material OR b:material OR a:projekt OR b:projekt)
  AND ANY(k IN keys(r) WHERE toLower(toString(r[k])) CONTAINS 'quelle')
RETURN a, r, b
LIMIT 100;
