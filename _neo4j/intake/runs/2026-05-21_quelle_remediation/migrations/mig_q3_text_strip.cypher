// ==========================================================================
// mig_q3_text_strip.cypher
//
// Phase Q3 — Remove :Quelle.text_content from :Dossier nodes after Q1 has
// extracted URLs. Dossier .md files on disk remain the source of truth.
//
// Plan ref:   _neo4j/QUELLE_REMEDIATION_PLAN.md §5 Q3
// Author:     orchestrator (Claude)
// Database:   mit-bestand
//
// PRE-CONDITION: Q1 must have completed. Sanity check below MUST return 0
// violations before the strip proceeds.
//
// Idempotent: re-running is a no-op once text_content is removed.
// Reversible: the dossier .md files on disk can repopulate text_content; the
// runner's rollback procedure does exactly that.
// ==========================================================================

// ---------- Q3.A — Sanity gate: dossier with text_content must have ZQ ----
// Every :Dossier that currently has text_content MUST already be connected
// to at least one :ExternalLink via :ZITIERT_QUELLE (proving Q1 extracted its
// links). If this gate fails, the strip is aborted by the runner.
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
  AND NOT exists{(d)-[:ZITIERT_QUELLE]->(:ExternalLink)}
RETURN 'q3_pre_gate_dossier_text_but_no_external_link' AS rule,
       count(d) AS violations,
       collect(d.id)[..10] AS sample;

// ---------- Q3.B — Capture pre-strip statistics ---------------------------
// Records how much text we're about to remove for forensic audit and rollback.
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
WITH d, size(d.text_content) AS char_count
SET d.text_content_chars_pre_strip = char_count,
    d.text_content_stripped_at = date(),
    d.migration_origin = coalesce(d.migration_origin, '') +
        CASE WHEN d.migration_origin IS NULL OR d.migration_origin = ''
             THEN 'mig_q3_text_strip'
             ELSE ' | mig_q3_text_strip' END
RETURN 'q3_b_dossiers_about_to_strip' AS check, count(d) AS c,
       sum(char_count) AS total_chars;

// ---------- Q3.C — The strip itself ---------------------------------------
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
REMOVE d.text_content;

// ==========================================================================
// Audits
// ==========================================================================

// A1 — No :Dossier carries text_content after strip
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
RETURN 'q3_a1_dossier_with_text_content' AS rule, count(d) AS violations;

// A2 — Every dossier we stripped has the forensic marker
MATCH (d:Dossier) WHERE d.text_content_stripped_at IS NOT NULL
RETURN 'q3_a2_dossiers_stripped' AS check, count(d) AS c,
       sum(d.text_content_chars_pre_strip) AS total_chars_removed;

// A3 — Spot-check: pick one dossier, confirm it has ZITIERT_QUELLE edges
MATCH (d:Dossier {id:'q_stuttgart_210_md'})
OPTIONAL MATCH (d)-[:ZITIERT_QUELLE]->(e:ExternalLink)
RETURN 'q3_a3_stuttgart_210_external_links' AS check,
       d.id AS dossier,
       d.text_content IS NULL AS text_stripped,
       d.text_content_chars_pre_strip AS was_chars,
       count(e) AS external_links_now;
