// Schema-compatible Bauteilbörsen update generated 2026-06-01
// Copy the CSV files into Neo4j import/ first, then run this file.

// 1) Anchor nodes + required vocabulary edges
LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
WITH row
WHERE row.anchor_id IS NOT NULL AND row.anchor_id <> ''
MERGE (a:Akteur {id: row.anchor_id})
ON CREATE SET a.name = row.name,
              a.source_scope = row.source_scope,
              a.review_run = 'schema_compatible_bauteilboersen_update_2026_06_01'
ON MATCH SET a.name = coalesce(a.name, row.name),
             a.review_run = 'schema_compatible_bauteilboersen_update_2026_06_01';

LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
MATCH (a:Akteur {id: row.anchor_id})
MATCH (l:Land {id: row.land_id})
MERGE (a)-[:LIEGT_IN_LAND]->(l);

LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
MATCH (a:Akteur {id: row.anchor_id})
MATCH (m:Marktmodell {id: row.marktmodell_id})
MERGE (a)-[:HAT_MARKTMODELL]->(m);

LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
MATCH (a:Akteur {id: row.anchor_id})
UNWIND split(row.akteurtyp_ids,';') AS tid
WITH a, trim(tid) AS tid WHERE tid <> ''
MATCH (t:Akteurtyp {id: tid})
MERGE (a)-[:HAT_AKTEURTYP]->(t);

LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
MATCH (a:Akteur {id: row.anchor_id})
UNWIND split(row.geschaeftsmodell_ids,';') AS gid
WITH a, trim(gid) AS gid WHERE gid <> ''
MATCH (g:Geschaeftsmodell {id: gid})
MERGE (a)-[:HAT_GESCHAEFTSMODELL]->(g);

// 2) Evidence URL nodes. qid is precomputed, so APOC is not required.
LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_ACTORS_REQUIRED_EDGES.csv' AS row
MATCH (a:Akteur {id: row.anchor_id})
WITH a, split(row.evidence_urls,';') AS urls, split(row.evidence_qids,';') AS qids
UNWIND range(0, size(urls)-1) AS i
WITH a, trim(urls[i]) AS url, trim(qids[i]) AS qid
WHERE url <> '' AND qid <> ''
MERGE (q:Quelle {id: qid})
ON CREATE SET q.url = url, q.quelltyp = 'external_link'
ON MATCH SET q.url = coalesce(q.url, url), q.quelltyp = coalesce(q.quelltyp, 'external_link')
MERGE (a)-[:BELEGT_IN]->(q);

// 3) Auto-fingerprint roles and methods from Geschäftsmodell.
MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_shop_eigenstock'})
MATCH (r:Akteurrolle {id:'ar_materialbroker'})
MERGE (a)-[:HAT_AKTEURROLLE]->(r);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_marketplace_vermittlung'})
UNWIND ['ar_materialbroker','ar_software_digitalisierung'] AS rid
MATCH (r:Akteurrolle {id:rid})
MERGE (a)-[:HAT_AKTEURROLLE]->(r);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
UNWIND ['ar_rueckbau_bauteilernte_logistik','ar_aufbereitung_refurbishment','ar_materiallieferung_markt','ar_reuse_zirkularitaetsberatung'] AS rid
MATCH (r:Akteurrolle {id:rid})
MERGE (a)-[:HAT_AKTEURROLLE]->(r);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
UNWIND ['meth_urban_mining','meth_pre_deconstruction_audit','meth_bauteilkatalogisierung'] AS mid
MATCH (m:Methode {id:mid})
MERGE (a)-[:HAT_METHODE]->(m);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'})
UNWIND ['ar_software_digitalisierung','ar_forschung_dokumentation'] AS rid
MATCH (r:Akteurrolle {id:rid})
MERGE (a)-[:HAT_AKTEURROLLE]->(r);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'})
UNWIND ['meth_materialinventur','meth_bauteilkatalogisierung','meth_abrissmonitoring'] AS mid
MATCH (m:Methode {id:mid})
MERGE (a)-[:HAT_METHODE]->(m);

MATCH (a:Akteur)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_netzwerk_aggregator'})
UNWIND ['ar_bildung_wissenstransfer','ar_forschung_dokumentation','ar_materialbroker'] AS rid
MATCH (r:Akteurrolle {id:rid})
MERGE (a)-[:HAT_AKTEURROLLE]->(r);

// 4) Strict material/Bauteiltyp edges. This CSV has already been filtered to closed vocabulary IDs.
LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_STRICT_MATERIAL_BAUTEILTYP_EDGES.csv' AS row
WITH row WHERE row.rel_type = 'NUTZT_MATERIAL'
MATCH (a:Akteur {id: row.anchor_id})
MATCH (m:Material {id: row.target_id})
MERGE (a)-[r:NUTZT_MATERIAL]->(m)
ON CREATE SET r.evidence_confidence = 'belegt',
              r.review_run = 'schema_compatible_bauteilboersen_update_2026_06_01',
              r.evidence_url = row.canonical_evidence_url,
              r.evidence_quote = row.evidence_quote;

LOAD CSV WITH HEADERS FROM 'file:///GRAPH_IMPORT_STRICT_MATERIAL_BAUTEILTYP_EDGES.csv' AS row
WITH row WHERE row.rel_type = 'HAT_BAUTEILTYP'
MATCH (a:Akteur {id: row.anchor_id})
MATCH (b:Bauteiltyp {id: row.target_id})
MERGE (a)-[r:HAT_BAUTEILTYP]->(b)
ON CREATE SET r.evidence_confidence = 'belegt',
              r.review_run = 'schema_compatible_bauteilboersen_update_2026_06_01',
              r.evidence_url = row.canonical_evidence_url,
              r.evidence_quote = row.evidence_quote;

// 5) Validation quick checks.
MATCH (a:Akteur {review_run:'schema_compatible_bauteilboersen_update_2026_06_01'})
OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)         WITH a, count(t)  AS n_typ
OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)              WITH a, n_typ, count(l) AS n_land
OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m:Marktmodell)     WITH a, n_typ, n_land, count(m) AS n_mm
OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)            WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)     WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)                WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_evidence
RETURN a.id, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence,
       CASE WHEN n_typ>=1 AND n_land=1 AND n_mm=1 AND n_gm>=1 AND n_roles>=3 AND n_evidence>=2
            THEN 'OK' ELSE 'MISSING_REQUIRED' END AS schema_check
ORDER BY schema_check DESC, a.id;
