// ==========================================================================
// mig_q1_url_extract.cypher
//
// Phase Q1 — Extract every URL out of :Quelle.text_content (dossier markdown)
// and from :Quelle :ResearchDocument text into first-class :Quelle :ExternalLink
// nodes connected via :ZITIERT_QUELLE.
//
// Plan ref:   _neo4j/QUELLE_REMEDIATION_PLAN.md §5 Q1
// Author:     orchestrator (Claude)
// Database:   mit-bestand
//
// This file is a TEMPLATE — the runner script (quelle_remediation_runner.py)
// reads it as parameterised statements and invokes each with one row per URL
// extracted from each dossier's text_content (via Python regex). The runner
// passes:
//   $url             — the canonical URL (normalised: trailing slash removed,
//                      scheme+host lowercased, common UTM params stripped)
//   $url_hash        — apoc.text.md5([$url])
//   $title           — human-readable label (from the [label] part of
//                      [label](url), or empty if a bare URL)
//   $sref_label      — 'S1', 'S2', 'P1', or 'bare'
//   $surrounding_text — ~120 chars around the link for excerpt
//   $dossier_id      — the source :Quelle.id (case_markdown or research markdown)
//
// Idempotent. Re-running with the same parameters is a no-op.
// ==========================================================================

// ---------- Q1.A — MERGE the :ExternalLink target node ---------------------
// The id is deterministic on URL hash so MERGE is idempotent.
MERGE (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
ON CREATE SET
  ext.url = $url,
  ext.title = $title,
  ext.quelltyp = 'external_link',
  ext.first_seen_in_dossier = $dossier_id,
  ext.source_scope = 'q1_url_extract',
  ext.evidence_origin = 'source_curated',
  ext.evidence_basis = 'markdown_link_extraction',
  ext.evidence_source_id = $dossier_id,
  ext.evidence_confidence = 'belegt',
  ext.migration_origin = 'mig_q1_url_extract',
  ext.created_at = date()
ON MATCH SET
  // Track every dossier that cites this URL — duplicates are deduplicated by toSet
  ext.also_in_dossier = apoc.coll.toSet(
    coalesce(ext.also_in_dossier, []) + [$dossier_id]
  );

// ---------- Q1.B — MERGE the :ZITIERT_QUELLE edge -------------------------
// (Dossier or ResearchDocument) → ExternalLink
MATCH (source:Quelle {id: $dossier_id})
MATCH (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
MERGE (source)-[z:ZITIERT_QUELLE]->(ext)
ON CREATE SET
  z.locator = $sref_label,
  z.evidence_origin = 'source_curated',
  z.evidence_basis = 'markdown_link_extraction',
  z.evidence_source_id = $dossier_id,
  z.evidence_confidence = 'belegt',
  z.evidence_excerpt = $surrounding_text,
  z.migration_origin = 'mig_q1_url_extract',
  z.created_at = date();

// ==========================================================================
// Audits — runner asserts each AFTER all per-URL invocations complete.
// These are separate, parameterless queries.
// ==========================================================================

// A1 — Every :ExternalLink has non-null .url
MATCH (e:ExternalLink) WHERE e.url IS NULL
RETURN 'q1_a1_external_link_without_url' AS rule, count(e) AS violations;

// A2 — Every :ExternalLink created by Q1 is reachable from at least one source
MATCH (e:ExternalLink) WHERE e.migration_origin = 'mig_q1_url_extract'
  AND NOT exists{(:Quelle)-[:ZITIERT_QUELLE]->(e)}
RETURN 'q1_a2_orphan_external_link' AS rule, count(e) AS violations;

// A3 — Coverage report (informational): how many distinct URLs by dossier
MATCH (d:Quelle {quelltyp:'case_markdown'})
OPTIONAL MATCH (d)-[:ZITIERT_QUELLE]->(e:ExternalLink)
WHERE e.migration_origin = 'mig_q1_url_extract'
WITH d, count(DISTINCT e) AS new_url_count
RETURN d.id AS dossier, new_url_count
ORDER BY new_url_count DESC LIMIT 20;

// A4 — How many URLs were created in total
MATCH (e:ExternalLink) WHERE e.migration_origin = 'mig_q1_url_extract'
RETURN 'q1_a4_urls_created_by_q1' AS check, count(e) AS c;

// A5 — How many ZITIERT_QUELLE edges were created
MATCH ()-[z:ZITIERT_QUELLE]->() WHERE z.migration_origin = 'mig_q1_url_extract'
RETURN 'q1_a5_zitiert_quelle_created' AS check, count(z) AS c;
