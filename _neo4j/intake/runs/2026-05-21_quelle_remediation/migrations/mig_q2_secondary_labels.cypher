// ==========================================================================
// mig_q2_secondary_labels.cypher
//
// Phase Q2 — Promote :Quelle.quelltyp discriminator to secondary labels.
//   :Quelle :Dossier            (was quelltyp='case_markdown')
//   :Quelle :ExternalLink       (was quelltyp ∈ {external_link,
//                                                external_link_from_actor_registry})
//   :Quelle :ResearchDocument   (was quelltyp='research_markdown' or
//                                research-file id pattern)
//   :Quelle :SectionRef         (S-ref children, id matches q_<slug>_s\d+)
//
// :OntologyAnchor stays as-is (it is NOT a :Quelle, was carved off in Phase 1.2).
//
// Idempotent: every SET label only fires if the secondary label is absent.
//
// Plan ref:   _neo4j/QUELLE_REMEDIATION_PLAN.md §5 Q2
// ==========================================================================

// ---------- Q2.a — :Dossier (case_markdown) -------------------------------
MATCH (q:Quelle {quelltyp: 'case_markdown'})
WHERE NOT q:Dossier
SET q:Dossier,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_q2_secondary_labels'
             ELSE ' | mig_q2_secondary_labels' END;

// ---------- Q2.b — :ExternalLink (both URL flavours) ----------------------
MATCH (q:Quelle)
WHERE q.quelltyp IN ['external_link', 'external_link_from_actor_registry']
  AND NOT q:ExternalLink
SET q:ExternalLink,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_q2_secondary_labels'
             ELSE ' | mig_q2_secondary_labels' END;

// ---------- Q2.c — :ResearchDocument --------------------------------------
// Match by explicit quelltyp OR by id pattern for research markdown anchors.
MATCH (q:Quelle)
WHERE (q.quelltyp = 'research_markdown'
       OR q.id ENDS WITH '_research_md'
       OR q.id STARTS WITH 'q_research_')
  AND NOT q:ResearchDocument
SET q:ResearchDocument,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_q2_secondary_labels'
             ELSE ' | mig_q2_secondary_labels' END;

// ---------- Q2.d — :SectionRef --------------------------------------------
// Matches S-ref ids like 'q_holbein_gardens_london_s1', 'q_ferme_du_rail_paris_s2'.
MATCH (q:Quelle)
WHERE q.id =~ 'q_.+_s\\d+'
  AND NOT q:SectionRef
SET q:SectionRef,
    q.migration_origin = coalesce(q.migration_origin, '') +
        CASE WHEN q.migration_origin IS NULL OR q.migration_origin = ''
             THEN 'mig_q2_secondary_labels'
             ELSE ' | mig_q2_secondary_labels' END;

// ==========================================================================
// Audits
// ==========================================================================

// A1 — Counts per new label
MATCH (d:Dossier) RETURN 'q2_a1_dossier_count' AS check, count(d) AS c;
MATCH (e:ExternalLink) RETURN 'q2_a1_external_link_count' AS check, count(e) AS c;
MATCH (r:ResearchDocument) RETURN 'q2_a1_research_document_count' AS check, count(r) AS c;
MATCH (s:SectionRef) RETURN 'q2_a1_section_ref_count' AS check, count(s) AS c;

// A2 — Sanity: every Dossier is also a :Quelle
MATCH (d:Dossier) WHERE NOT d:Quelle
RETURN 'q2_a2_dossier_without_quelle' AS rule, count(d) AS violations;

// A3 — Untyped Quelle (no secondary label)
// Allowed exceptions: nothing — every Quelle should classify.
MATCH (q:Quelle)
WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument OR q:SectionRef)
RETURN 'q2_a3_untyped_quelle' AS rule, count(q) AS violations,
       collect(q.id)[..20] AS sample;

// A4 — A :Quelle should not be more than one of {Dossier, ExternalLink,
//      ResearchDocument, SectionRef}. Multi-label is a bug.
MATCH (q:Quelle)
WITH q,
     toInteger(q:Dossier) + toInteger(q:ExternalLink)
     + toInteger(q:ResearchDocument) + toInteger(q:SectionRef) AS n_labels
WHERE n_labels > 1
RETURN 'q2_a4_quelle_multi_classified' AS rule, count(q) AS violations,
       collect(q.id)[..20] AS sample;
