// ==========================================================================
// mig_s5_visibility.cypher
// Agent S5 — denormalise source quality/freshness summaries onto
// Projekt, Bauwerk, Akteur nodes for one-click visibility in Neo4j Browser.
//
// NOTE: this file is the reference / rollback record.
//       The runner (agent_s5_runner.py) executes equivalent logic via
//       parameterised Python writes for performance — this file is NOT
//       executed directly by the runner.
//
// Actual graph topology (verified 2026-05-22):
//   Projekt  -[:BELEGT_IN]->  :ExternalLink        (2 756 edges)
//   Projekt  -[:BELEGT_IN]->  :Dossier
//              -[:ZITIERT_QUELLE]-> :ExternalLink   (94 → ~1 950 ext)
//   Projekt  -[:ZITIERT_QUELLE]-> :ExternalLink     (1 edge)
//   Bauwerk  -[:BELEGT_IN]->  :Dossier
//              -[:ZITIERT_QUELLE]-> :ExternalLink   (190 dossiers)
//   Akteur   -[:BELEGT_IN]->  :ExternalLink         (361 edges)
//   Akteur   -[:BELEGT_IN]->  :Dossier
//              -[:ZITIERT_QUELLE]-> :ExternalLink   (437 dossiers)
//   Akteur   -[:ZITIERT_QUELLE]-> :ExternalLink     (366 edges)
//   HAS_SOURCE_LINK only exists on :ReuseRule (not Projekt/Bauwerk/Akteur)
// ==========================================================================

// --------------------------------------------------------------------------
// ROLLBACK — run this to undo all S5 changes
// --------------------------------------------------------------------------
// MATCH (n) WHERE n.migration_origin CONTAINS 'mig_s5_visibility'
// REMOVE n.source_urls, n.source_count,
//        n.source_quality_summary, n.source_freshness_summary,
//        n.source_trust_score, n.source_urls_updated_at;
// MATCH (i:DataIssue) WHERE i.found_by = 's5_visibility' DETACH DELETE i;
// --------------------------------------------------------------------------

// ==========================================================================
// S5.D — :DataIssue for nodes with > 50 source URLs
// (run AFTER the Python runner has set source_count on all nodes)
// ==========================================================================
MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur) AND n.source_count > 50
MERGE (i:DataIssue {id: 'di_excessive_sources__' + n.id})
ON CREATE SET
  i.kind             = 'excessive_sources_on_node',
  i.severity         = 'low',
  i.ref_label        = labels(n)[0],
  i.ref_id           = n.id,
  i.found_at         = date(),
  i.found_by         = 's5_visibility',
  i.status           = 'open',
  i.resolution_note  = 'Node has ' + toString(n.source_count) +
                       ' source URLs. Review whether all are warranted.'
MERGE (i)-[:CONCERNS]->(n);
