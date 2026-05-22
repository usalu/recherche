// Post-apply connectivity checks — rotor_dc_reuse_bubble_2026_06_05

// T0 — opalis ecosystem degree (target >= 4)
MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN count(DISTINCT a) AS verbunden_degree, collect(DISTINCT a.id) AS neighbors;

// T1 — PREUSE partner stack
MATCH (p:Programm {id: 'prog_preuse'})<-[r:BETEILIGT_AN]-(a)
RETURN collect(a.id) AS partners, count(a) AS partner_count;

// T2 — spine mesh (opalis ↔ rotordc ↔ bellastock)
MATCH (opalis:Akteur {id:'opalis'})
OPTIONAL MATCH (opalis)-[r1:VERBUNDEN_MIT_AKTEUR]-(rotordc:Akteur {id:'rotordc'})
OPTIONAL MATCH (opalis)-[r2:VERBUNDEN_MIT_AKTEUR]-(bellastock:Akteur {id:'bellastock'})
RETURN r1.id AS opalis_rotordc, r2.id AS opalis_bellastock;

// T3 — OXY commissioner cluster
MATCH (p:Projekt {id:'p_oxy_centre_monnaie'})<-[:BETEILIGT_AN]-(a)
RETURN collect(a.id) AS actors ORDER BY actors;

// T4 — Generale → Multi donor path
MATCH path = (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:HAT_BAUWERK]->(bw:Bauwerk {id:'bw_generale_de_banque_brussels'})
OPTIONAL MATCH (rotordc:Akteur {id:'rotordc'})-[s:NUTZT_BAUWERK]->(bw)
RETURN p.id AS project, bw.id AS donor, s.id AS rotordc_salvage_rel;

// T5 — import-only bubble view
UNWIND [
  'Rotor','rotordc','opalis','bellastock',
  'prog_fcrbe','prog_preuse',
  'p_multi_brussels_reuse_in_multi','p_oxy_centre_monnaie',
  'p_architecture_of_reuse_brussels',
  'bw_generale_de_banque_brussels',
  'whitewood','immobel','city_of_utrecht','brussels_environment'
] AS sid
MATCH (n {id: sid})
OPTIONAL MATCH (n)-[r]-(m)
WHERE m.id IN [
  'Rotor','rotordc','opalis','bellastock',
  'prog_fcrbe','prog_preuse',
  'p_multi_brussels_reuse_in_multi','p_oxy_centre_monnaie',
  'p_architecture_of_reuse_brussels',
  'bw_generale_de_banque_brussels',
  'whitewood','immobel','city_of_utrecht','brussels_environment'
]
AND coalesce(r.review_run, '') = 'rotor_dc_reuse_bubble_2026_06_05'
RETURN n.id AS node, type(r) AS rel_type, m.id AS neighbor, r.evidence_confidence AS conf
ORDER BY node, rel_type, neighbor;
