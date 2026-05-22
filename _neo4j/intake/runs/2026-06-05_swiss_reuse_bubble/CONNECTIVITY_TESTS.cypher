// Swiss reuse bubble — connectivity tests
// Run before/after each phase; record counts in connectivity_report.json

// T0.1 — Cirkla ecosystem degree
MATCH (c:Akteur {id: 'cirkla'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN count(DISTINCT a) AS cirkla_verbunden_degree,
       collect(DISTINCT a.id) AS neighbors
ORDER BY cirkla_verbunden_degree DESC;

// T0.2 — Cirkla BELEGT_IN coverage
MATCH (c:Akteur {id: 'cirkla'})-[:BELEGT_IN]->(q:Quelle)
RETURN count(q) AS cirkla_belegt_in_count, collect(q.url) AS urls;

// T0.3 — K.118 participation (stubs vs confirmed)
MATCH (p:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})<-[r]-(a:Akteur)
RETURN type(r) AS rel_type, a.id AS actor_id, r.evidence_confidence AS confidence
ORDER BY rel_type, actor_id;

// T0.4 — ELYS participation
MATCH (p:Projekt {id: 'p_elys_kultur_gewerbehaus_basel'})<-[r]-(a:Akteur)
RETURN type(r) AS rel_type, a.id AS actor_id, r.evidence_confidence AS confidence
ORDER BY rel_type, actor_id;

// T1 — Gruner → Basel → useagain supply chain path
MATCH p = shortestPath(
  (g:Akteur {id: 'gruner_reuse'})-[:VERBUNDEN_MIT_AKTEUR*..6]-(u:Akteur {id: 'useagain_bauteilclick'})
)
RETURN length(p) AS path_length, [n IN nodes(p) | n.id] AS path_ids
LIMIT 5;

// T2 — Practice triangle (cirkla, zirkular, baubuero)
MATCH (c:Akteur {id: 'cirkla'})-[r1:VERBUNDEN_MIT_AKTEUR]-(z:Akteur {id: 'zirkular'})
MATCH (c)-[r2:VERBUNDEN_MIT_AKTEUR]-(b:Akteur {id: 'baubuero_in_situ'})
RETURN r1.evidence_confidence AS cirkla_zirkular_conf,
       r2.evidence_confidence AS cirkla_baubuero_conf;

// T3 — Data / policy layer reachability from Cirkla
MATCH (c:Akteur {id: 'cirkla'})
OPTIONAL MATCH (c)-[:VERBUNDEN_MIT_AKTEUR*1..2]-(sw:Programm {id: 'prog_swircular'})
OPTIONAL MATCH (c)-[:VERBUNDEN_MIT_AKTEUR*1..2]-(lf:Programm {id: 'prog_innosuisse_reuse_legal_framework_ch'})
OPTIONAL MATCH (c)-[:VERBUNDEN_MIT_AKTEUR*1..2]-(pl:Software {id: 'software_planular'})
RETURN sw.id IS NOT NULL AS reaches_swircular,
       lf.id IS NOT NULL AS reaches_legal_framework,
       pl.id IS NOT NULL AS reaches_planular;

// T4 — Evidence completeness on new edges (sample)
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN count(r) AS new_edges,
       sum(CASE WHEN r.evidence_url IS NULL THEN 1 ELSE 0 END) AS missing_url,
       sum(CASE WHEN r.evidence_quote IS NULL OR r.evidence_quote = '' THEN 1 ELSE 0 END) AS missing_quote;
