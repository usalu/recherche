// ==========================================================================
// mig_s4_b_text_strip.cypher
//
// Remove :Dossier.text_content after S1 extraction. The runner executes the
// pre-strip gate first and aborts if violations > 0.
// ==========================================================================

// S4.B.1 - Pre-strip gate
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
  AND NOT exists{(d)-[:ZITIERT_QUELLE]->(:ExternalLink)}
RETURN 's4_b1_pre_strip_gate' AS rule,
       count(d) AS violations,
       collect(d.id)[..20] AS sample;

// S4.B.2 - Capture pre-strip statistics
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
WITH d, size(d.text_content) AS char_count
SET d.text_content_chars_pre_strip = char_count,
    d.text_content_stripped_at = date(),
    d.migration_origin = coalesce(d.migration_origin, '') +
        CASE WHEN d.migration_origin IS NULL OR d.migration_origin = ''
             THEN 'mig_s4_b_text_strip'
             ELSE ' | mig_s4_b_text_strip' END
RETURN 's4_b2_dossiers_about_to_strip' AS check,
       count(d) AS c,
       sum(char_count) AS total_chars;

// S4.B.3 - Strip text content
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
REMOVE d.text_content;

// S4.B.4 - Audit
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
RETURN 's4_b4_dossiers_with_text_remaining' AS rule,
       count(d) AS violations,
       collect(d.id)[..20] AS sample;

MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL
RETURN 's4_b4_dossiers_stripped' AS check,
       count(d) AS c,
       sum(d.text_content_chars_pre_strip) AS total_chars_removed;
