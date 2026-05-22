// Netherlands reuse bubble — post-apply connectivity gate
// Review run: netherlands_reuse_bubble_2026_06_05

// T0: superuse spine — target >= 4
MATCH (s:Akteur {id: 'superuse_studios_2012architecten'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T1: new_horizon_urban_mining spine — target >= 4
MATCH (n:Akteur {id: 'new_horizon_urban_mining'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T2: madaster Dutch mesh — target >= 4 dutch actors
MATCH (m:Akteur {id: 'madaster'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
WHERE a.id IN ['superuse_studios_2012architecten','new_horizon_urban_mining','insert_marketplace','city_of_utrecht','repurpose']
RETURN collect(DISTINCT a.id) AS neighbors;

// T3: insert_marketplace spine — target >= 3
MATCH (i:Akteur {id: 'insert_marketplace'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T4: superuse <-> new_horizon (Oogstkaart lineage)
MATCH (s:Akteur {id: 'superuse_studios_2012architecten'})-[r:VERBUNDEN_MIT_AKTEUR]-(n:Akteur {id: 'new_horizon_urban_mining'})
RETURN count(r) AS linked;

// T5: repurpose spine — target >= 4
MATCH (p:Akteur {id: 'repurpose'})-[r:VERBUNDEN_MIT_AKTEUR]-(a:Akteur)
RETURN collect(DISTINCT a.id) AS neighbors;

// T6: bubble-tagged rels
MATCH ()-[r]->()
WHERE r.review_run = 'netherlands_reuse_bubble_2026_06_05'
RETURN count(r) AS bubble_rels;
