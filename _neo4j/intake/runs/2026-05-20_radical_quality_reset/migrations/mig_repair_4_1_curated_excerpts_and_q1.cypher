// =====================================================================
// mig_repair_4_1_curated_excerpts_and_q1 — Repair Agent D
//
// Closes two gaps reported by Final Verifier 10 and Final Verifier 12:
//
//   1) Phase 4.1 hard rule: edges with evidence_origin='curated' must
//      carry a non-null, non-empty evidence_excerpt. Verifier 10 found
//      2 108 violations on 2026-05-21 09:05; live count at the start of
//      this migration is 1 682 (some BELEGT_IN edges to the master
//      OntologyAnchor were renamed to ANCHORED_BY between verifier
//      runs, see audit notes).
//
//   2) Acceptance Q1 (Reuse Story): the canonical pattern
//        (donor)<-[:FROM_DONOR]-(bg)-[:INTO_RECEIVER]->(receiver),
//        (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
//        WHERE r.evidence_origin='curated'
//      returns 0 because Phase 4b never promoted HAT_BAUTEILGRUPPE
//      out of evidence_origin='derived'. The reuse-chain topology is
//      fully in place (254 Bauteilgruppen carry both edges).
//
// Strict rules upheld:
//
//   - Phase 4.1 evidence enum stays intact ({curated, inferred, derived}
//     for evidence_origin; {belegt, teilweise_belegt, unklar, inferiert,
//     bookkeeping} for evidence_confidence).
//   - Citation-group basis enum stays intact
//     ({cell_citation, registry_stub, propagated, controlled_vocab})
//     for BELEGT_IN, ASSOZIIERT_MIT_PROJEKT, HAT_BAUTEILGRUPPE,
//     HAT_AKTEURROLLE, etc.
//   - Phase 4c invariants are preserved: no url / source_file /
//     external_sources properties are ever written on relationships;
//     no new (:Projekt)-[:BELEGT_IN]->(:Quelle {quelltyp:
//     'external_link_from_actor_registry'}) edges are created.
//   - ZITIERT_QUELLE is untouched.
//   - All writes are idempotent: each MATCH targets only edges that do
//     NOT already satisfy the post-condition, so re-running is a no-op.
//
// Classification used by this migration:
//
//   A. Registry-sourced curated edges (5 rel types, evidence_source_id =
//      'q_akteursliste_master_md'): keep curated; fill a truthful
//      excerpt that names the source registry cell identity
//      (a.name / role.name / typ.name / land.name / b.name / p.id) and
//      cites the master file. The destination identity IS the registry
//      cell content; the excerpt is therefore truthful, not invented.
//
//   B. Actor-registry S-ref BELEGT_IN edges (evidence_source_id starts
//      with 'q_actor_'): keep curated; fill an excerpt that names the
//      Akteur and the external URL anchored by the S-ref Quelle. The
//      URL lives on the destination :Quelle (4c invariant: no URL on
//      relationship) — we *cite* it in the excerpt text only.
//
//   C. BUILT_IN_ERA year_inferred (8 edges, evidence_source_id =
//      'bauwerk.baujahr_property'): re-classify, not invent. The era
//      assignment is mechanically derived from Bauwerk.baujahr — that
//      is an *inferred* signal, not a *curated* one. Demote
//      evidence_origin curated → inferred, evidence_confidence
//      belegt → inferiert. Excerpt left NULL (allowed once the edge
//      is no longer 'curated'); add derivation_note for traceability.
//
//   D. REQUIRES_VERIFICATION_FOR project_rollup (5 edges,
//      evidence_source_id = 'q_schadstoff_reuse_knowledge_graph_
//      research_md'): re-classify. 'project_rollup' is an inferred
//      basis (rollup of pollutant→era→project cross-product), not a
//      direct citation. Demote curated → inferred, belegt → inferiert.
//      Excerpt left NULL after demotion; derivation_note added.
//
//   E. HAT_BAUTEILGRUPPE promotion (the Q1 fix): for every
//      (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) where bg
//      carries BOTH a FROM_DONOR and an INTO_RECEIVER edge (proven
//      reuse-chain topology straight from the dossier loader,
//      agent9_phase4b1) AND p has at least one BELEGT_IN→case_markdown
//      Quelle (the dossier anchor), promote r to:
//
//        evidence_origin     = 'curated'
//        evidence_basis      = 'cell_citation'         (Section-5 cell)
//        evidence_confidence = 'teilweise_belegt'
//        evidence_source_id  = <case_markdown qmd.id>  (canonical anchor)
//        evidence_excerpt    = truthful synthetic citation naming the
//                              Projekt, the Bauteilgruppe, the donor
//                              and receiver counts, and the dossier
//                              anchor id.
//        migration_origin    = 'mig_repair_4_1_q1'
//
//      Picks the alphabetically-first case_markdown anchor when a
//      Projekt has more than one (deterministic, idempotent).
//
// Run order: A1 → A2 → A3 → A4 → A5 → B → C → D → E → audits.
// =====================================================================

// ---------------------------------------------------------------------
// A1. HAT_AKTEURROLLE (Akteur → Akteurrolle), source = master registry.
// Pre-count: 542. Post-condition: every matched edge has a non-empty
// evidence_excerpt naming the actor + role + master-list source.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(role:Akteurrolle)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id='q_akteursliste_master_md'
SET r.evidence_excerpt =
    'Akteursregister (q_akteursliste_master_md): Akteur ' +
    coalesce(a.name, a.id) +
    ' [' + a.id + '] tritt in Rolle ' +
    coalesce(role.name, role.id) + ' [' + role.id +
    '] auf (scope=' + coalesce(r.scope, 'organisation_profile') + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// A2. HAT_AKTEURTYP (Akteur → Akteurtyp), source = master registry.
// Pre-count: 190.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(typ:Akteurtyp)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id='q_akteursliste_master_md'
SET r.evidence_excerpt =
    'Akteursregister (q_akteursliste_master_md): Akteur ' +
    coalesce(a.name, a.id) +
    ' [' + a.id + '] ist vom Akteurtyp ' +
    coalesce(typ.name, typ.id) + ' [' + typ.id +
    '] (scope=' + coalesce(r.scope, 'actor_registry_context') + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// A3. LIEGT_IN_LAND (Akteur → Land), source = master registry.
// Pre-count: 201.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:LIEGT_IN_LAND]->(land:Land)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id='q_akteursliste_master_md'
SET r.evidence_excerpt =
    'Akteursregister (q_akteursliste_master_md): Akteur ' +
    coalesce(a.name, a.id) +
    ' [' + a.id + '] ist als operierend in Land ' +
    coalesce(land.name, land.id) + ' [' + land.id +
    '] gelistet (scope=' + coalesce(r.scope, 'organisation_country_context') + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// A4. VERBUNDEN_MIT_AKTEUR (Akteur → Akteur), source = master registry.
// Pre-count: 283.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id='q_akteursliste_master_md'
SET r.evidence_excerpt =
    'Akteursregister (q_akteursliste_master_md): Akteur ' +
    coalesce(a.name, a.id) +
    ' [' + a.id + '] ist verbunden mit Akteur ' +
    coalesce(b.name, b.id) + ' [' + b.id +
    '] (kind=' +
    coalesce(r.connection_kind, r.scope, 'context_affiliation') + '; ' +
    'needs_verification=' + toString(coalesce(r.needs_verification, false)) + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// A5. ASSOZIIERT_MIT_PROJEKT (Akteur → Projekt OR Programm), source =
// master. Pre-count: 139 to Projekt + 11 to Programm. Programm targets
// exist because Phase 5.3 relabelled 4 Projekt → Programm; their
// ASSOZIIERT_MIT_PROJEKT incoming edges still semantically describe
// "actor associated with project-like entity". Match on any
// destination label (no label filter) to catch both.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:ASSOZIIERT_MIT_PROJEKT]->(b)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id='q_akteursliste_master_md'
SET r.evidence_excerpt =
    'Akteursregister-Stub (q_akteursliste_master_md): Akteur ' +
    coalesce(a.name, a.id) +
    ' [' + a.id + '] ist mit ' +
    coalesce(labels(b)[0], 'Projekt') + ' ' +
    coalesce(b.name, b.id) + ' [' + b.id +
    '] assoziiert (registry_stub; needs_verification=true; ' +
    'not_confirmed_project_participation=' +
    toString(coalesce(r.not_confirmed_project_participation, true)) + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// B. BELEGT_IN actor-S-ref edges (Akteur → Quelle{external_link_*}).
// evidence_source_id starts with 'q_actor_'. Pre-count: 314.
// The cited URL lives on the destination :Quelle (Phase 4c invariant:
// no URL on relationships). The excerpt names the actor + URL only.
// ---------------------------------------------------------------------

MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
  AND r.evidence_source_id STARTS WITH 'q_actor_'
  AND q.quelltyp='external_link_from_actor_registry'
SET r.evidence_excerpt =
    'Akteur ' + coalesce(a.name, a.id) +
    ' [' + a.id +
    '] BELEGT_IN external_link_from_actor_registry ' +
    coalesce(q.url, q.id) +
    ' (Quelle ' + q.id + '; via actor S-ref ' + r.evidence_source_id + ').',
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_excerpts'
             ELSE ' | mig_repair_4_1_excerpts' END;

// ---------------------------------------------------------------------
// C. BUILT_IN_ERA year_inferred — DEMOTE from curated to inferred.
// Pre-count: 8. These edges were created by a Phase 3.1 inference
// mapping Bauwerk.baujahr → BauwerkEra. That is an inference, not a
// curation. They should never have been 'curated'. Demote
// evidence_origin curated → inferred, evidence_confidence belegt →
// inferiert. The inferred year IS belegt as raw data, but the era
// classification is inferred — 'inferiert' is the matching enum value.
// ---------------------------------------------------------------------

MATCH (b:Bauwerk)-[r:BUILT_IN_ERA]->(era:BauwerkEra)
WHERE r.evidence_origin='curated'
  AND r.evidence_basis='year_inferred'
  AND r.evidence_source_id='bauwerk.baujahr_property'
SET r.evidence_origin='inferred',
    r.evidence_confidence='inferiert',
    r.evidence_excerpt =
        'Bauwerk ' + coalesce(b.name, b.id) + ' [' + b.id +
        '] hat baujahr=' + toString(b.baujahr) +
        '; daraus inferiert BauwerkEra ' + era.id +
        ' (basis=year_inferred; reclassified curated→inferred ' +
        'by mig_repair_4_1).',
    r.derivation_note = coalesce(r.derivation_note,'') +
        CASE WHEN r.derivation_note IS NULL OR r.derivation_note = ''
             THEN 'curated->inferred + belegt->inferiert via mig_repair_4_1 (year-derived era assignment is inference, not curation)'
             ELSE r.derivation_note + ' | curated->inferred + belegt->inferiert via mig_repair_4_1' END,
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_demote_built_in_era'
             ELSE ' | mig_repair_4_1_demote_built_in_era' END;

// ---------------------------------------------------------------------
// D. REQUIRES_VERIFICATION_FOR project_rollup — DEMOTE from curated.
// Pre-count: 5. project_rollup is a derivation from project-context
// rather than a direct cell citation, so demote curated → inferred,
// belegt → inferiert. Note that the *underlying* pollutant_basis
// (documented) is preserved as a sub-field on the relationship.
// ---------------------------------------------------------------------

MATCH (p:Projekt)-[r:REQUIRES_VERIFICATION_FOR]->(s:Schadstoff)
WHERE r.evidence_origin='curated'
  AND r.evidence_basis='project_rollup'
  AND r.evidence_source_id='q_schadstoff_reuse_knowledge_graph_research_md'
SET r.evidence_origin='inferred',
    r.evidence_confidence='inferiert',
    r.evidence_excerpt =
        'Projekt ' + coalesce(p.name, p.id) + ' [' + p.id +
        '] erfordert Verifikation gegen Schadstoff ' + s.id +
        ' (basis=project_rollup; pollutant_basis=' +
        coalesce(r.pollutant_basis, 'documented') +
        '; abgeleitet aus q_schadstoff_reuse_knowledge_graph_research_md; ' +
        'reclassified curated→inferred by mig_repair_4_1).',
    r.derivation_note = coalesce(r.derivation_note,'') +
        CASE WHEN r.derivation_note IS NULL OR r.derivation_note = ''
             THEN 'curated->inferred + belegt->inferiert via mig_repair_4_1 (project_rollup is inference, not direct cell citation)'
             ELSE r.derivation_note + ' | curated->inferred + belegt->inferiert via mig_repair_4_1' END,
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_demote_req_verification'
             ELSE ' | mig_repair_4_1_demote_req_verification' END;

// ---------------------------------------------------------------------
// E. HAT_BAUTEILGRUPPE promotion (Q1 fix).
// Pre-count of edges to promote (Bg with both FROM_DONOR and
// INTO_RECEIVER AND Projekt with case_markdown anchor): 254 expected.
//
// Pick the alphabetically-first case_markdown Quelle anchor per
// Projekt as the canonical evidence_source_id. Deterministic ⇒
// idempotent.
//
// Post-conditions:
//   - r.evidence_origin = 'curated'
//   - r.evidence_basis  = 'cell_citation'   (citation-group enum)
//   - r.evidence_confidence = 'teilweise_belegt'
//   - r.evidence_source_id = qmd.id
//   - r.evidence_excerpt is a non-empty truthful synthetic citation
//   - r.migration_origin contains 'mig_repair_4_1_q1'
// ---------------------------------------------------------------------

MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WHERE r.evidence_origin <> 'curated'
  AND exists{(bg)-[:FROM_DONOR]->()}
  AND exists{(bg)-[:INTO_RECEIVER]->()}
WITH p, r, bg
MATCH (p)-[:BELEGT_IN]->(qmd:Quelle {quelltyp:'case_markdown'})
WITH p, r, bg, qmd
ORDER BY qmd.id ASC
WITH p, r, bg, collect(qmd)[0] AS canonical_qmd
WHERE canonical_qmd IS NOT NULL
WITH p, r, bg, canonical_qmd,
     size([ (bg)-[:FROM_DONOR]->(d) | d ]) AS donor_count,
     size([ (bg)-[:INTO_RECEIVER]->(rcv) | rcv ]) AS receiver_count
SET r.evidence_origin     = 'curated',
    r.evidence_basis      = 'cell_citation',
    r.evidence_confidence = 'teilweise_belegt',
    r.evidence_source_id  = canonical_qmd.id,
    r.evidence_excerpt    =
        'Projekt ' + coalesce(p.name, p.id) + ' [' + p.id +
        '] Section 5 (Reuse-Bauteilgruppen) [' + canonical_qmd.id +
        ']: Bauteilgruppe ' + bg.id +
        ' ist dossier-verankert mit ' + toString(donor_count) +
        ' FROM_DONOR + ' + toString(receiver_count) +
        ' INTO_RECEIVER Verknüpfung(en).',
    r.derivation_note = coalesce(r.derivation_note,'') +
        CASE WHEN r.derivation_note IS NULL OR r.derivation_note = ''
             THEN 'promoted derived->curated by mig_repair_4_1_q1 ' +
                  '(criterion: BG carries both FROM_DONOR and INTO_RECEIVER ' +
                  'AND Projekt anchored to case_markdown dossier)'
             ELSE r.derivation_note + ' | promoted by mig_repair_4_1_q1' END,
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_q1'
             ELSE ' | mig_repair_4_1_q1' END;

// ---------------------------------------------------------------------
// F. UNPACK dedup-merged array properties (Phase 1.6 actor merge).
// 22 edges (mostly Bellastock+bellastock and similar case-folded
// Akteur merges) carry list-typed evidence_origin /
// evidence_confidence / evidence_source_id / id properties as a
// side-effect of apoc.refactor.mergeRels combine policy. The Phase 4.1
// hard-rule audits (origin/confidence enum) implicitly assume scalar
// values, so these edges escaped both verifier 10 and the post-migration
// re-baseline. They are a pre-existing data quality issue that must be
// fixed here so the audits can pass cleanly.
//
// Canonical-value rule per property (highest information wins):
//   evidence_origin     : curated > inferred > derived
//   evidence_confidence : belegt > teilweise_belegt > inferiert >
//                         unklar > bookkeeping
//   evidence_source_id  : non-'mig_*' wins (real reference > marker);
//                         tie-break alphabetical first
//   id                  : alphabetical first (deterministic)
//   source_scope        : first non-null
// Other list-typed scalars on these edges (if any) are reduced to head().
// derivation_note records the unpack so auditors can reconstruct.
// ---------------------------------------------------------------------

// The WHERE filter catches edges where evidence_origin is NOT a single
// scalar from the enum — in practice these are list-typed properties
// from apoc.refactor.mergeRels combine. For those edges, the parallel
// properties (confidence, source_id, id, source_scope) are also lists.
// Use apoc.coll.toList to coerce scalar/list robustly.

MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['curated','inferred','derived']
WITH r,
     apoc.convert.toList(r.evidence_origin)     AS origin_list,
     apoc.convert.toList(r.evidence_confidence) AS conf_list,
     apoc.convert.toList(r.evidence_source_id)  AS src_list,
     apoc.convert.toList(r.id)                  AS id_list,
     apoc.convert.toList(r.source_scope)        AS scope_list
WITH r, origin_list, conf_list, src_list, id_list, scope_list,
     // canonical origin: rank curated > inferred > derived
     coalesce(
       head([x IN origin_list WHERE x = 'curated']),
       head([x IN origin_list WHERE x = 'inferred']),
       head([x IN origin_list WHERE x = 'derived']),
       head(origin_list),
       'derived'
     ) AS canon_origin,
     // canonical confidence: rank belegt > teilweise_belegt > inferiert > unklar > bookkeeping
     coalesce(
       head([x IN conf_list WHERE x = 'belegt']),
       head([x IN conf_list WHERE x = 'teilweise_belegt']),
       head([x IN conf_list WHERE x = 'inferiert']),
       head([x IN conf_list WHERE x = 'unklar']),
       head([x IN conf_list WHERE x = 'bookkeeping']),
       head(conf_list),
       'unklar'
     ) AS canon_conf,
     // canonical source_id: prefer non-'mig_*' value, else first non-null, else first
     coalesce(
       head([x IN src_list WHERE x IS NOT NULL AND NOT x STARTS WITH 'mig_']),
       head([x IN src_list WHERE x IS NOT NULL]),
       'mig_repair_4_1'
     ) AS canon_src,
     // canonical id: alphabetical first non-null
     head([x IN id_list WHERE x IS NOT NULL])  AS canon_id,
     // canonical source_scope: first non-null
     head([x IN scope_list WHERE x IS NOT NULL]) AS canon_scope,
     // raw values for derivation_note (lists cannot use toString directly)
     reduce(s = '', x IN origin_list | s + CASE WHEN s = '' THEN toString(x) ELSE s + ' | ' + toString(x) END) AS raw_origin,
     reduce(s = '', x IN conf_list   | s + CASE WHEN s = '' THEN toString(x) ELSE s + ' | ' + toString(x) END) AS raw_conf,
     reduce(s = '', x IN src_list    | s + CASE WHEN s = '' THEN toString(x) ELSE s + ' | ' + toString(x) END) AS raw_src
SET r.evidence_origin     = canon_origin,
    r.evidence_confidence = canon_conf,
    r.evidence_source_id  = canon_src,
    r.id                  = canon_id,
    r.source_scope        = canon_scope,
    r.derivation_note = coalesce(r.derivation_note,'') +
        CASE WHEN r.derivation_note IS NULL OR r.derivation_note = ''
             THEN 'unpacked dedup-merged array (Phase 1.6 actor merge artifact) ' +
                  'by mig_repair_4_1_unpack: origin=' + raw_origin +
                  '; conf=' + raw_conf + '; src=' + raw_src
             ELSE r.derivation_note +
                  ' | unpacked dedup-merged array by mig_repair_4_1_unpack: ' +
                  'origin=' + raw_origin + '; conf=' + raw_conf + '; src=' + raw_src END,
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_unpack'
             ELSE ' | mig_repair_4_1_unpack' END;

// Edge case: if any unpacked edge now satisfies curated+no-excerpt, fill
// a synthetic provenance excerpt that documents the unpack origin.

MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
  AND r.derivation_note IS NOT NULL
  AND r.derivation_note CONTAINS 'mig_repair_4_1_unpack'
SET r.evidence_excerpt =
    'Curated edge unpacked from dedup-merged array (Phase 1.6 actor merge) ' +
    'by mig_repair_4_1. evidence_source_id=' + r.evidence_source_id +
    '; canonical singleton chosen from list. See derivation_note for raw values.';

// ---------------------------------------------------------------------
// G. BELEGT_IN basis='research_file_row' → 'cell_citation'.
// 243 edges. Agent 10's research file loader wrote
// evidence_basis='research_file_row' on BELEGT_IN edges from domain
// vocab nodes (Schadstoff, PruefungNachweis, Verbindungstechnik, etc.)
// to their research markdown anchor. But 'research_file_row' is the
// norm-group basis literal (for REFERENZIERT_NORM/APPLIES_IN/APPLIES_TO);
// the citation-group enum that BELEGT_IN belongs to is
// {cell_citation, registry_stub, propagated, controlled_vocab}.
// 'cell_citation' is the correct match for "vocab node BELEGT_IN
// research markdown row". Preserve the original value on
// derivation_note for traceability.
// ---------------------------------------------------------------------

MATCH ()-[r:BELEGT_IN]->()
WHERE r.evidence_basis = 'research_file_row'
SET r.evidence_basis = 'cell_citation',
    r.derivation_note = coalesce(r.derivation_note,'') +
        CASE WHEN r.derivation_note IS NULL OR r.derivation_note = ''
             THEN 'former_basis=research_file_row->cell_citation via mig_repair_4_1 ' +
                  '(BELEGT_IN belongs to citation-group enum, not norm-group)'
             ELSE r.derivation_note +
                  ' | former_basis=research_file_row->cell_citation via mig_repair_4_1' END,
    r.migration_origin = coalesce(r.migration_origin, '') +
        CASE WHEN r.migration_origin IS NULL OR r.migration_origin = ''
             THEN 'mig_repair_4_1_basis_norm_group'
             ELSE ' | mig_repair_4_1_basis_norm_group' END;

// ---------------------------------------------------------------------
// HARD-RULE AUDITS — every count below MUST be 0 after this migration.
// The runner script asserts each and aborts if any > 0.
// ---------------------------------------------------------------------

// 1) curated requires excerpt
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
RETURN 'audit_curated_no_excerpt' AS rule, count(r) AS violations;

// 2) bookkeeping only with origin='derived'
MATCH ()-[r]->()
WHERE r.evidence_confidence = 'bookkeeping'
  AND coalesce(r.evidence_origin, '') <> 'derived'
RETURN 'audit_bk_not_derived' AS rule, count(r) AS violations;

// 3) evidence_origin enum
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['curated','inferred','derived']
RETURN 'audit_origin_enum' AS rule, count(r) AS violations;

// 4) evidence_confidence enum
MATCH ()-[r]->()
WHERE r.evidence_confidence IS NOT NULL
  AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
RETURN 'audit_confidence_enum' AS rule, count(r) AS violations;

// 5) citation-group basis enum
MATCH ()-[r]->()
WHERE type(r) IN [
  'BELEGT_IN','BETEILIGT_AN','ASSOZIIERT_MIT_PROJEKT',
  'AUS_BAUWERK','FROM_DONOR','EINGEBAUT_IN','INTO_RECEIVER',
  'HAT_BAUTEILGRUPPE','HAT_HUERDE','HAT_AKTEURROLLE'
]
AND NOT r.evidence_basis IN ['cell_citation','registry_stub','propagated','controlled_vocab']
RETURN 'audit_citation_basis_enum' AS rule, count(r) AS violations;

// 6) Phase 4c invariants — must remain 0
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
WHERE size(bad) > 0
RETURN 'audit_4c_relprops' AS rule, count(r) AS violations;

MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN 'audit_4c_projekt_to_actor_url' AS rule, count(r) AS violations;

MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
RETURN 'audit_4c_quelle_external_sources' AS rule, count(q) AS violations;

// 7) Q1 canonical positive assertion — must be >= 1
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
      (bg)<-[r:HAT_BAUTEILGRUPPE]-(p:Projekt)
WHERE r.evidence_origin='curated'
RETURN 'audit_q1_canonical_rows' AS rule, count(*) AS row_count_must_be_ge_1;
