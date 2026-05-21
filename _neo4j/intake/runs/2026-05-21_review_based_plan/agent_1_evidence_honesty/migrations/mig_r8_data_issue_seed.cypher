// ==========================================================================
// mig_r8_data_issue_seed — populate :DataIssue audit nodes
//
// Run AFTER stage 3 is complete (R1, R2, R3, R4, R5, R7, R9, R10 all landed).
//
// Kinds:
//   - q1_topology_synthesis            (Repair D promotions)
//   - pollutant_inference              (HAS_RISK_POLLUTANT origin=inferred)
//   - registry_unverified_actor_stub   (STUB_PROJECT_LINK after R9)
//   - era_inference                    (BUILT_IN_ERA origin=inferred)
//   - dossier_section8_missing         (Projekt with no :Kennwert despite case_markdown)
//   - curated_no_excerpt               (defensive — after R1+R7.c should be 0)
//   - controlled_vocab_too_sparse      (vocab labels with < 10 nodes)
// ==========================================================================

// R8.a — Repair D Q1 promotions (254 expected)
MATCH ()-[r]->()
WHERE r.evidence_origin = 'topology_synthesized'
  AND r.migration_origin CONTAINS 'mig_repair_4_1_q1'
WITH r, startNode(r) AS s, endNode(r) AS t
MERGE (i:DataIssue {
  id: 'di_q1_promotion__' + type(r) + '__' + coalesce(s.id, toString(elementId(s))) +
       '__' + coalesce(t.id, toString(elementId(t)))
})
ON CREATE SET
  i.kind = 'q1_topology_synthesis',
  i.severity = 'high',
  i.ref_label = type(r),
  i.ref_id = r.id,
  i.rel_type = type(r),
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'HAT_BAUTEILGRUPPE edge promoted from derived to curated by Repair D without parsing a source-document cell. Requires per-edge dossier verification.'
MERGE (i)-[:CONCERNS]->(s);

// R8.b — Pollutant inference (799 expected)
MATCH ()-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
WHERE r.evidence_origin = 'inferred'
  AND r.evidence_basis IN ['era_and_material','material_only']
WITH r, startNode(r) AS bg, s
MERGE (i:DataIssue {
  id: 'di_pollutant_inference__' + coalesce(bg.id, toString(elementId(bg))) + '__' + s.id
})
ON CREATE SET
  i.kind = 'pollutant_inference',
  i.severity = 'medium',
  i.ref_label = 'HAS_RISK_POLLUTANT',
  i.ref_id = r.id,
  i.rel_type = 'HAS_RISK_POLLUTANT',
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'Inferred from era×material lookup; no source-cell citation. Requires donor-building dossier verification.'
MERGE (i)-[:CONCERNS]->(bg);

// R8.c — Registry actor stubs (after R9 rename: STUB_PROJECT_LINK)
MATCH (a:Akteur)-[r:STUB_PROJECT_LINK]->(p)
MERGE (i:DataIssue {
  id: 'di_actor_stub__' + a.id + '__' + coalesce(p.id, toString(elementId(p)))
})
ON CREATE SET
  i.kind = 'registry_unverified_actor_stub',
  i.severity = 'medium',
  i.ref_label = 'STUB_PROJECT_LINK',
  i.ref_id = r.id,
  i.rel_type = 'STUB_PROJECT_LINK',
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'Actor↔project link from master registry; not confirmed via dossier text.'
MERGE (i)-[:CONCERNS]->(a);

// R8.d — Era inference (8 expected; demoted in Repair D step C)
MATCH (b:Bauwerk)-[r:BUILT_IN_ERA]->(era:BauwerkEra)
WHERE r.evidence_origin = 'inferred'
MERGE (i:DataIssue {
  id: 'di_era_inference__' + b.id + '__' + era.id
})
ON CREATE SET
  i.kind = 'era_inference',
  i.severity = 'low',
  i.ref_label = 'BUILT_IN_ERA',
  i.ref_id = r.id,
  i.rel_type = 'BUILT_IN_ERA',
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'Era derived from Bauwerk.baujahr property. Mechanically correct but not curated.'
MERGE (i)-[:CONCERNS]->(b);

// R8.e — Dossier section-8 missing (project has case_markdown anchor but no :Kennwert)
MATCH (p:Projekt)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})
WHERE NOT exists{(p)-[:HAT_KENNWERT]->()}
MERGE (i:DataIssue {
  id: 'di_section8_missing__' + p.id
})
ON CREATE SET
  i.kind = 'dossier_section8_missing',
  i.severity = 'medium',
  i.ref_label = 'Projekt',
  i.ref_id = p.id,
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'Project has dossier anchor but no :Kennwert; Section 8 facts likely missed by loader.'
MERGE (i)-[:CONCERNS]->(p);

// R8.f — Defensive: source_curated edges without excerpts
//        Should be 0 after R1+R7.c. If non-zero, flag.
MATCH ()-[r]->()
WHERE r.evidence_origin = 'source_curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
WITH r, startNode(r) AS s
MERGE (i:DataIssue {
  id: 'di_curated_no_excerpt__' + type(r) + '__' + coalesce(s.id, toString(elementId(s)))
})
ON CREATE SET
  i.kind = 'curated_no_excerpt',
  i.severity = 'high',
  i.ref_label = type(r),
  i.ref_id = r.id,
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'source_curated edge without an excerpt. Should not occur after R1.'
MERGE (i)-[:CONCERNS]->(s);

// R8.g — Sparse vocab labels (< 10 nodes; informational, severity=low)
UNWIND ['Akteurtyp','Beschaffungsweg','HuerdeKategorie','BauaufgabeIntervention',
        'Defekt','Logistik','Prozessphase','Bausystem','MatchingQualitaet','Nutzung',
        'Schadstoff','Status','Bauobjektklasse','Akzeptanz','Bauobjektrolle',
        'Bauteilebene','Bauweise','BauwerkEra','Funktionswechsel','ZustandsKlasse',
        'Rueckbauverfahren','Tragwerksprinzip']
  AS sparse_label
CALL {
  WITH sparse_label
  CALL apoc.cypher.run('MATCH (n:`' + sparse_label + '`) RETURN count(n) AS c', {})
    YIELD value
  RETURN value.c AS c
}
WITH sparse_label, c
WHERE c < 10
MERGE (i:DataIssue {id: 'di_sparse_vocab__' + sparse_label})
ON CREATE SET
  i.kind = 'controlled_vocab_too_sparse',
  i.severity = 'low',
  i.ref_label = sparse_label,
  i.found_at = date(),
  i.found_by = 'r8_audit_seed',
  i.status = 'open',
  i.resolution_note = 'Label has fewer than 10 nodes. Consider widening with new ingestion or accepting as documentation-only.';

// ==========================================================================
// Audits
// ==========================================================================

MATCH (i:DataIssue) RETURN 'data_issue_total' AS check, count(i) AS c;
MATCH (i:DataIssue) RETURN i.kind AS kind, count(i) AS c ORDER BY c DESC;
MATCH (i:DataIssue) RETURN i.severity AS severity, count(i) AS c ORDER BY i.severity;
