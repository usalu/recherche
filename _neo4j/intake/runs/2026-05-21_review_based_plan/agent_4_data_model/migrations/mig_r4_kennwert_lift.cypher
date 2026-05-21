// ==========================================================================
// mig_r4_kennwert_lift
// Parameterized, idempotent lift from Projekt *_facts JSON properties into
// :Kennwert nodes and :HAT_KENNWERT edges.
// The runner normalizes heterogeneous JSON entries into $rows.
// ==========================================================================

UNWIND $rows AS row
MATCH (p:Projekt {id: row.project_id})
MERGE (kw:Kennwert {id: row.id})
SET kw.category = row.category,
    kw.kennwert = row.kennwert,
    kw.wert = row.wert,
    kw.wert_text = row.wert_text,
    kw.wert_min = row.wert_min,
    kw.wert_max = row.wert_max,
    kw.einheit = row.einheit,
    kw.method = row.method,
    kw.bilanzgrenze = row.bilanzgrenze,
    kw.loader = row.loader,
    kw.source_id = row.source_id,
    kw.fact_index = row.fact_index,
    kw.raw_property = row.raw_property,
    kw.migration_origin = row.node_migration_origin,
    kw.source_scope = row.source_scope
MERGE (p)-[r:HAT_KENNWERT]->(kw)
SET r.evidence_origin = row.evidence_origin,
    r.evidence_basis = row.evidence_basis,
    r.evidence_confidence = row.evidence_confidence,
    r.evidence_source_id = row.source_id,
    r.evidence_excerpt = row.evidence_excerpt,
    r.migration_origin = 'mig_r4_kennwert_lift'
RETURN count(row) AS rows_processed,
       count(DISTINCT kw) AS kennwert_touched,
       count(DISTINCT r) AS edges_touched;
