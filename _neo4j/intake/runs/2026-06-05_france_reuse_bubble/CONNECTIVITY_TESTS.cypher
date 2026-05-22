// France reuse bubble — post-apply connectivity gate
// Review run: france_reuse_bubble_2026_06_05

// T0: bellastock ecosystem VERBUNDEN (excl. people) — target >= 4
MATCH (b:Akteur {id: 'bellastock'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
WHERE NOT a.id IN ['hugo_topalov', 'sarah_westerfeld', 'frederic_denise']
RETURN count(DISTINCT a) AS degree, collect(DISTINCT a.id) AS neighbors;

// T1: opalis ecosystem VERBUNDEN (excl. maarten_gielen) — target >= 5
MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
WHERE NOT a.id IN ['maarten_gielen']
RETURN count(DISTINCT a) AS degree, collect(DISTINCT a.id) AS neighbors;

// T2: cycle_up spine — target >= 4
MATCH (c:Akteur {id: 'cycle_up'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T3: backacia spine — target >= 3
MATCH (b:Akteur {id: 'backacia'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T4: mobius spine (excl. people) — target >= 2 + cstb
MATCH (m:Akteur {id: 'mobius_reemploi'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
WHERE NOT a.id IN ['frederic_denise']
RETURN collect(DISTINCT a.id) AS neighbors;

// T5: opalis <-> backacia (A evidence)
MATCH (o:Akteur {id: 'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(b:Akteur {id: 'backacia'})
RETURN count(r) AS linked;

// T6: mobius <-> cstb (SPIROU)
MATCH (m:Akteur {id: 'mobius_reemploi'})-[r:VERBUNDEN_MIT_AKTEUR]-(c:Akteur {id: 'cstb'})
RETURN count(r) AS linked;

// T7: association_reavie <-> bellastock (IDF)
MATCH (r:Akteur {id: 'association_reavie'})-[x:VERBUNDEN_MIT_AKTEUR]-(b:Akteur {id: 'bellastock'})
RETURN count(x) AS linked;

// T8: bubble-tagged rels
MATCH ()-[r]->()
WHERE r.review_run = 'france_reuse_bubble_2026_06_05'
RETURN count(r) AS bubble_rels;

// Mesh path: bellastock -> opalis -> backacia -> cycle_up
MATCH p = shortestPath(
  (b:Akteur {id: 'bellastock'})-[:VERBUNDEN_MIT_AKTEUR*..6]-(c:Akteur {id: 'cycle_up'})
)
RETURN length(p) AS hops, [n IN nodes(p) | n.id] AS path;
