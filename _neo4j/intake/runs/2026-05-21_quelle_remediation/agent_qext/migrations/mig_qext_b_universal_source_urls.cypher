// ==========================================================================
// mig_qext_b_universal_source_urls.cypher
//
// Phase Q-EXT.B — Surface source_urls on every user-facing domain node.
//
// Plan ref: _neo4j/QUELLE_REMEDIATION/EXTENSION_universal_source_surfacing.md
//
// This file is INVOKED PER LABEL by the runner. The runner UNWINDs the
// label list and runs the body for each. The body uses apoc.cypher.run
// because Cypher doesn't allow parameterised labels.
//
// Idempotent. Re-running re-derives source_urls from current topology.
// ==========================================================================

// Driver invocation: pass $labels as the list of labels to process.

UNWIND $labels AS lbl
CALL apoc.cypher.doIt(
  'MATCH (n:`' + lbl + '`) ' +
  // Direct: node → :ExternalLink (rare but possible)
  'OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(direct:ExternalLink) ' +
  'WITH n, collect(DISTINCT direct.url) AS direct_urls ' +
  // Length 2: node → :Dossier|:ResearchDocument → :ZITIERT_QUELLE → :ExternalLink
  'OPTIONAL MATCH (n)-[:BELEGT_IN]->(d:Quelle)-[:ZITIERT_QUELLE]->(ext1:ExternalLink) ' +
  'WHERE (d:Dossier OR d:ResearchDocument) ' +
  'WITH n, direct_urls, collect(DISTINCT ext1.url) AS chain_urls ' +
  // Length 3: via Projekt (helpful for Bauteilgruppe → HAT_BAUTEILGRUPPE-ancestor → Dossier → URL)
  'OPTIONAL MATCH (n)<-[:HAT_BAUTEILGRUPPE|HAS_BAUWERK|BETEILIGT_AN|STUB_PROJECT_LINK]-(p:Projekt) ' +
  'WHERE p.source_urls IS NOT NULL ' +
  'WITH n, direct_urls, chain_urls, ' +
  '     collect(DISTINCT p.source_urls) AS via_projekt_lists ' +
  'WITH n, direct_urls + chain_urls + apoc.coll.flatten(via_projekt_lists) AS combined ' +
  'WITH n, [u IN combined WHERE u IS NOT NULL AND u <> ""] AS all_urls ' +
  'SET n.source_urls = apoc.coll.toSet(all_urls), ' +
  '    n.source_count = size(apoc.coll.toSet(all_urls)), ' +
  '    n.source_urls_updated_at = date(), ' +
  '    n.migration_origin = coalesce(n.migration_origin, "") + ' +
  '      CASE WHEN n.migration_origin IS NULL OR n.migration_origin = "" ' +
  '           THEN "mig_qext_b_source_urls" ' +
  '           ELSE " | mig_qext_b_source_urls" END ' +
  'RETURN count(n) AS nodes_updated',
  {}
) YIELD value
RETURN lbl AS label, value.nodes_updated AS nodes_updated;

// ==========================================================================
// Audits
// ==========================================================================

// QEXT-B.A1 — Every node in the target labels has source_urls set
// (Runner asserts per-label; this is a sample.)
MATCH (n:Material) WHERE n.source_urls IS NULL
RETURN 'qext_b_a1_material_no_source_urls' AS check, count(n) AS violations;

MATCH (n:Norm) WHERE n.source_urls IS NULL
RETURN 'qext_b_a1_norm_no_source_urls' AS check, count(n) AS violations;

MATCH (n:Bauteilgruppe) WHERE n.source_urls IS NULL
RETURN 'qext_b_a1_bg_no_source_urls' AS check, count(n) AS violations;

// QEXT-B.D1 — Distribution: source_count by label
MATCH (n) WHERE n.source_urls IS NOT NULL AND n.migration_origin CONTAINS 'mig_qext_b_source_urls'
UNWIND labels(n) AS lbl
RETURN lbl, count(n) AS nodes, avg(n.source_count) AS avg_sources,
       max(n.source_count) AS max_sources
ORDER BY nodes DESC;

// QEXT-B.S1 — Spot checks for user-named examples
MATCH (n:Material {id: 'mat_stahl'})
RETURN 'qext_b_s1_mat_stahl' AS check, n.source_count AS sources, n.source_urls AS urls;

MATCH (n:Bauteilgruppe) WHERE n.id STARTS WITH 'bg_stuttgart_21'
RETURN 'qext_b_s2_stuttgart_21_bg' AS check, n.id, n.source_count, n.source_urls
LIMIT 3;
