// Germany reuse bubble — post-apply connectivity checks
// Review run: germany_reuse_bubble_2026_06_05

// T0: concular ecosystem VERBUNDEN (exclude dominik_campanella person cluster)
MATCH (c:Akteur {id: 'concular'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
WHERE a.id <> 'dominik_campanella'
RETURN count(DISTINCT a) AS concular_ecosystem_degree,
       collect(DISTINCT a.id) AS neighbors;

// T1: bremen marketplace mesh
MATCH (b:Akteur {id:'bauteilboerse_bremen'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS bremen_neighbors;

// T2: hannover spine
MATCH (h:Akteur {id:'bauteilboerse_hannover'})-[r:VERBUNDEN_MIT_AKTEUR]-(a)
RETURN collect(DISTINCT a.id) AS hannover_neighbors;

// T3: Haus der Materialisierung hub
MATCH (h:Akteur {id:'haus_der_materialisierung'})-[r:VERBUNDEN_MIT_AKTEUR]-(a)
RETURN collect(DISTINCT a.id) AS hdm_neighbors;

// T4: evidence-tagged edges from this run
MATCH ()-[r]->()
WHERE r.review_run = 'germany_reuse_bubble_2026_06_05'
RETURN count(r) AS bubble_edge_count;

// T5: concular ↔ restado ↔ bremen ↔ hannover path exists
MATCH p = shortestPath(
  (c:Akteur {id:'concular'})-[:VERBUNDEN_MIT_AKTEUR*..6]-(h:Akteur {id:'bauteilboerse_hannover'})
)
RETURN length(p) AS path_length, [n IN nodes(p) | n.id] AS path_ids
LIMIT 1;
