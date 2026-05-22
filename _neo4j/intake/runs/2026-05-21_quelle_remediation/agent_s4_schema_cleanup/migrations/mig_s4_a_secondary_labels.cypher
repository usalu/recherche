// ==========================================================================
// mig_s4_a_secondary_labels.cypher
//
// Promote :Quelle.quelltyp discriminator values to secondary labels.
// Logic mirrors the legacy mig_q2_secondary_labels.cypher.
// ==========================================================================

// S4.A.1 - :Dossier (case_markdown)
MATCH (q:Quelle {quelltyp: 'case_markdown'})
WHERE NOT q:Dossier
SET q:Dossier,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_s4_a_secondary_labels'
             ELSE ' | mig_s4_a_secondary_labels' END;

// S4.A.2 - :ExternalLink
MATCH (q:Quelle)
WHERE q.quelltyp IN ['external_link', 'external_link_from_actor_registry']
  AND NOT q:ExternalLink
SET q:ExternalLink,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_s4_a_secondary_labels'
             ELSE ' | mig_s4_a_secondary_labels' END;

// S4.A.3 - :ResearchDocument
MATCH (q:Quelle)
WHERE (q.quelltyp = 'research_markdown'
       OR q.id ENDS WITH '_research_md'
       OR q.id STARTS WITH 'q_research_')
  AND NOT q:ResearchDocument
SET q:ResearchDocument,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_s4_a_secondary_labels'
             ELSE ' | mig_s4_a_secondary_labels' END;

// S4.A.4 - :SectionRef
MATCH (q:Quelle)
WHERE q.id =~ 'q_.+_s\\d+'
  AND NOT q:SectionRef
SET q:SectionRef,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_s4_a_secondary_labels'
             ELSE ' | mig_s4_a_secondary_labels' END;

// ==========================================================================
// Audits
// ==========================================================================

MATCH (d:Dossier)
RETURN 's4_a_dossier_count' AS check, count(d) AS c;

MATCH (e:ExternalLink)
RETURN 's4_a_external_link_count' AS check, count(e) AS c;

MATCH (r:ResearchDocument)
RETURN 's4_a_research_document_count' AS check, count(r) AS c;

MATCH (s:SectionRef)
RETURN 's4_a_section_ref_count' AS check, count(s) AS c;

MATCH (d:Dossier) WHERE NOT d:Quelle
RETURN 's4_a_dossier_without_quelle' AS rule, count(d) AS violations;

MATCH (q:Quelle)
WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument OR q:SectionRef OR q:OntologyAnchor)
RETURN 's4_a_untyped_quelle_residual' AS check, count(q) AS c,
       collect(q.id)[..20] AS sample;

MATCH (q:Quelle)
WITH q,
     toInteger(q:Dossier) + toInteger(q:ExternalLink)
     + toInteger(q:ResearchDocument) + toInteger(q:SectionRef) AS n_labels
WHERE n_labels > 1
RETURN 's4_a_quelle_multi_classified' AS rule, count(q) AS violations,
       collect(q.id)[..20] AS sample;
