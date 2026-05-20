// Phase 2.5 — Under-used label demotions (Agent 5, Wave-2)
//   a–b. :Layer → :Bauteiltyp.brand_layer enum, delete 6 Layer nodes.
//   c–e. :LebenszyklusModul → :Projekt.lca_module_scope enum list +
//        derived :Projekt-[:REFERENZIERT_NORM]->:Norm edges; delete 5 LZM nodes.
//   f–g. :RechtlicheBedingung → src.legal_conditions list-of-strings
//        (placeholder for the future :ReuseRule.legal_conditions field);
//        delete 9 RB nodes.
//   h–i. :ZertifizierungBewertungssystem → :Projekt.certifications list;
//        delete 8 ZBS nodes.
//   j–m. :Tool → :Software with `kind='tool'`; rewire NUTZT_TOOL → NUTZT_SOFTWARE.
//
// Net: 6 + 5 + 9 + 8 + 8 = 36 fewer label-distinct nodes; -8 from total node
// count is just the Tool merge (Tool relabelled, not deleted, so node count
// drops only by Layer+LZM+RB+ZBS = 28).

// 2.5.a — set brand_layer enum on Bauteiltyp from existing TEILT_LAYER edges
MATCH (b:Bauteiltyp)-[:TEILT_LAYER]->(l:Layer)
WITH b, head(collect(DISTINCT
  CASE l.id
    WHEN 'layer_site'        THEN 'site'
    WHEN 'layer_structure'   THEN 'structure'
    WHEN 'layer_skin'        THEN 'skin'
    WHEN 'layer_services'    THEN 'services'
    WHEN 'layer_space_plan'  THEN 'space_plan'
    WHEN 'layer_stuff'       THEN 'stuff'
    ELSE NULL
  END)) AS brand_layer
SET b.brand_layer = brand_layer
RETURN count(b) AS bauteiltypen_set,
       collect({bt_id: b.id, brand_layer: brand_layer}) AS assignments;

// 2.5.b — delete all :Layer nodes (DETACH drops TEILT_LAYER + BELEGT_IN edges)
MATCH (l:Layer)
WITH collect(l) AS layers, count(l) AS c
UNWIND layers AS l
DETACH DELETE l
RETURN c AS layer_nodes_deleted;

// 2.5.c — set Projekt.lca_module_scope list from BERECHNET_NACH_MODUL edges
MATCH (p:Projekt)-[:BERECHNET_NACH_MODUL]->(m:LebenszyklusModul)
WITH p, collect(DISTINCT
  CASE m.id
    WHEN 'lz_a1_a3' THEN 'A1_A3'
    WHEN 'lz_a4_a5' THEN 'A4_A5'
    WHEN 'lz_b'     THEN 'B'
    WHEN 'lz_c'     THEN 'C1_C4'
    WHEN 'lz_d'     THEN 'D'
    ELSE m.id
  END) AS modules
WITH p, apoc.coll.toSet(coalesce(p.lca_module_scope, []) + modules) AS combined
SET p.lca_module_scope = combined
RETURN count(p) AS projekte_set,
       sum(size(combined)) AS total_module_entries;

// 2.5.d — derive :Projekt-[:REFERENZIERT_NORM]->:Norm from the LZM-method path
MATCH (p:Projekt)-[:BERECHNET_NACH_MODUL]->(m:LebenszyklusModul)-[:METHODENGRUNDLAGE_NORM]->(n:Norm)
WITH p, m, n
MERGE (p)-[r:REFERENZIERT_NORM]->(n)
  ON CREATE SET r.evidence_origin     = 'derived',
                r.evidence_basis      = 'lca_module_demote',
                r.evidence_source_id  = 'mig_2_5',
                r.evidence_confidence = 'mittel',
                r.id                  = 'r_' + p.id + '__REFERENZIERT_NORM__' + n.id,
                r._derived_from_lzm   = m.id
RETURN count(r) AS norm_edges_touched;

// 2.5.e — delete all :LebenszyklusModul nodes (drops BERECHNET_NACH_MODUL + METHODENGRUNDLAGE_NORM)
MATCH (m:LebenszyklusModul)
WITH collect(m) AS modules, count(m) AS c
UNWIND modules AS m
DETACH DELETE m
RETURN c AS lzm_nodes_deleted;

// 2.5.f — accumulate legal_conditions list on each src of HAT_RECHTLICHE_BEDINGUNG
MATCH (src)-[:HAT_RECHTLICHE_BEDINGUNG]->(rb:RechtlicheBedingung)
OPTIONAL MATCH (rb)-[:GILT_IN_LAND]->(land:Land)
WITH src, rb, [c IN collect(DISTINCT land.id) WHERE c IS NOT NULL] AS country_ids
WITH src, rb,
     rb.name + CASE
       WHEN size(country_ids) > 0
         THEN ' [' + apoc.text.join(country_ids, ',') + ']'
       ELSE ''
     END AS entry
WITH src, collect(DISTINCT entry) AS new_legal
WITH src, apoc.coll.toSet(coalesce(src.legal_conditions, []) + new_legal) AS combined
SET src.legal_conditions = combined
RETURN count(src) AS sources_updated,
       sum(size(combined)) AS total_legal_entries;

// 2.5.g — delete all :RechtlicheBedingung nodes
MATCH (rb:RechtlicheBedingung)
WITH collect(rb) AS rbs, count(rb) AS c
UNWIND rbs AS rb
DETACH DELETE rb
RETURN c AS rb_nodes_deleted;

// 2.5.h — accumulate certifications list on each Projekt from HAT_ZERTIFIZIERUNG edges
MATCH (p:Projekt)-[:HAT_ZERTIFIZIERUNG]->(z:ZertifizierungBewertungssystem)
WITH p, collect(DISTINCT z.name) AS certs
WITH p, apoc.coll.toSet(coalesce(p.certifications, []) + certs) AS combined
SET p.certifications = combined
RETURN count(p) AS projekte_set,
       sum(size(combined)) AS total_certifications;

// 2.5.i — delete all :ZertifizierungBewertungssystem nodes
MATCH (z:ZertifizierungBewertungssystem)
WITH collect(z) AS zs, count(z) AS c
UNWIND zs AS z
DETACH DELETE z
RETURN c AS zert_deleted;

// 2.5.j — relabel :Tool → :Software with kind='tool'
MATCH (t:Tool)
WITH collect(t) AS tools
UNWIND tools AS t
REMOVE t:Tool
SET   t:Software, t.kind = 'tool'
RETURN size(tools) AS tools_relabelled;

// 2.5.k — backfill kind='software' on the pre-existing :Software nodes
MATCH (s:Software) WHERE s.kind IS NULL
SET s.kind = 'software'
RETURN count(s) AS software_kind_default_set;

// 2.5.l — rewire every NUTZT_TOOL relationship to NUTZT_SOFTWARE
MATCH ()-[r:NUTZT_TOOL]->()
WITH collect(r) AS rels
UNWIND rels AS r
CALL apoc.refactor.setType(r, 'NUTZT_SOFTWARE') YIELD output
RETURN size(collect(output)) AS edges_rewired;

// 2.5.m — patch id property of rewired edges so the string reflects the new type
MATCH ()-[r:NUTZT_SOFTWARE]->()
WHERE r.id IS NOT NULL AND r.id CONTAINS '__NUTZT_TOOL__'
WITH collect(r) AS rels
UNWIND rels AS r
SET r.id = replace(r.id, '__NUTZT_TOOL__', '__NUTZT_SOFTWARE__')
RETURN size(rels) AS id_props_fixed;
