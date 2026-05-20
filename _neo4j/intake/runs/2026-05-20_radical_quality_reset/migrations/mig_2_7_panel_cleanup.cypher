// =========================================================================
// Migration 2.7 — three-bucket property panel cleanup
//
//   bucket 1  panel     — finite list of human-readable keys per label
//   bucket 2  facts     — list-of-dict structured metrics (cost/co2/reuse)
//   bucket 3  _archive  — JSON string sidecar holding every other property
//
// Plus:
//   - :Quelle.external_sources arrays → :ZITIERT_QUELLE edges + target :Quelle
//   - :Akteur.raw_role_evidence rolled up from BETEILIGT_AN.rolle_text
//   - Edge source pollution stripped to canonical 5-field shape
//     where evidence_origin is still NULL (Agent 7 finishes the remainder)
//
// Reversibility: snapshot/nodes.jsonl + snapshot/relationships.jsonl
//   carry the pre-state for every node/edge; _archive itself is a JSON
//   string from which the original (key, value) pairs can be restored.
// =========================================================================

// --- 2.7.a Three-bucket cleanup pattern (executed per-label by runner)
//
// MATCH (n:<LABEL>)
// WITH n, [k IN keys(n) WHERE NOT k IN $PANEL_KEYS] AS archive_keys
// WITH n, archive_keys,
//   apoc.convert.toJson(apoc.map.fromPairs([k IN archive_keys | [k, n[k]]])) AS archive_json
// CALL apoc.create.removeProperties(n, archive_keys) YIELD node
// SET node._archive = archive_json
// RETURN count(node);
//
// PANEL_KEYS lists (see runner for authoritative source):
//
// :Projekt (18):
//   id, name, name_full, quality_tier,
//   year_completed, raw_year_fields,
//   area_m2_gross, area_m2_range_min, area_m2_range_max,
//   bewertung, projektstatus_text, nutzung_text, node_role,
//   cost_facts, reuse_share_facts, co2_facts,
//   source_scope, _archive
//
// :Bauteilgruppe (22 + source_scope + _archive = 24):
//   id, name, name_full, reuse_status,
//   primary_material_id, primary_bauteiltyp_id,
//   menge_t, menge_stueck, menge_m2, menge_kg, menge_m, menge_unbekannt,
//   neue_funktion, alte_funktion,
//   tragend, raeumlich, huelle, technisch,
//   donor_unknown, donor_resolution_status, direct_reuse_relevant,
//   menge_source, menge_original_key,
//   source_scope, _archive
//
// :Bauwerk / :Materialdepot (14):
//   id, name, name_full,
//   baujahr, jahr_errichtet, era_unknown,
//   bauwerkstatus, nutzung_text, schutzstatus_text,
//   flaeche_m2, land, is_material_depot,
//   source_scope, _archive
//
// :Quelle (7 + source_scope + _archive = 9):
//   id, name, quelltyp, url, source_file, access_date, title,
//   source_scope, _archive
//
// :Akteur (10):
//   id, name, name_full, land, stadt, website, aliases,
//   raw_role_evidence,
//   source_scope, _archive

// --- 2.7.b Quelle.external_sources → :ZITIERT_QUELLE
//
// 60 :Quelle nodes carry an `external_sources` list of raw citation strings
// (e.g. "[S1] Küpfer, C. (2023): …, https://…").  Each entry is parsed for
// a URL; the URL is slugified into a stable target id and a target :Quelle
// is MERGEd.  A :ZITIERT_QUELLE edge is then MERGEd from the original
// :Quelle to the target with the canonical 5-field evidence shape.
//
// MERGE (target:Quelle {id: $target_id})
// ON CREATE SET target.url = $url,
//               target.quelltyp = 'external_link',
//               target.name = $title,
//               target.source_scope = 'mig_2_7_external_sources',
//               target._created_by  = 'mig_2_7'
// MERGE (q)-[r:ZITIERT_QUELLE]->(target)
// ON CREATE SET r.evidence_origin     = 'derived',
//               r.evidence_basis      = 'external_sources_array',
//               r.evidence_source_id  = 'mig_2_7',
//               r.evidence_confidence = 'unklar',
//               r.evidence_excerpt    = $raw_string;
//
// After all entries are migrated for a given source :Quelle, the
// `external_sources` property is REMOVEd from that source node.

// --- 2.7.c Akteur.raw_role_evidence (rollup from BETEILIGT_AN.rolle_text)
//
// MATCH (a:Akteur)
// OPTIONAL MATCH (a)-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL
// WITH a, collect(DISTINCT r.rolle_text) AS roles
// SET a.raw_role_evidence = roles;

// --- 2.7.d Edge source pollution → canonical 5-field shape (partial)
//
// Plan §2.7: any relationship still carrying `source`, `evidence`,
// `source_excerpt` or `datenqualitaet` AND no `evidence_origin` yet is
// migrated to:
//   evidence_origin     = 'derived'
//   evidence_basis      = coalesce(existing, 'legacy_migration')
//   evidence_source_id  = coalesce(existing, r.source)
//   evidence_confidence = coalesce(existing, 'unklar')
//   evidence_excerpt    = coalesce(r.evidence_excerpt, r.source_excerpt, r.evidence)
// and the four legacy properties are REMOVEd.
//
// Agent 7 owns the full migration; this run only touches the unambiguous
// edges where evidence_origin is currently NULL.
//
// MATCH ()-[r]->()
// WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL
//        OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL)
//   AND r.evidence_origin IS NULL
// WITH r,
//   coalesce(r.evidence_excerpt, r.source_excerpt, r.evidence) AS excerpt,
//   coalesce(r.evidence_source_id, r.source) AS src_id
// SET r.evidence_origin     = 'derived',
//     r.evidence_basis      = coalesce(r.evidence_basis, 'legacy_migration'),
//     r.evidence_source_id  = src_id,
//     r.evidence_confidence = coalesce(r.evidence_confidence, 'unklar'),
//     r.evidence_excerpt    = excerpt
// REMOVE r.source, r.evidence, r.source_excerpt, r.datenqualitaet;

// --- 2.7.e Sanity checks
// MATCH (p:Projekt)              WHERE size(keys(p)) > 25 RETURN p.id, size(keys(p));
// MATCH (bg:Bauteilgruppe)       WHERE size(keys(bg)) > 30 RETURN bg.id, size(keys(bg));
// MATCH (b:Bauwerk)              WHERE size(keys(b)) > 20 RETURN b.id, size(keys(b));
// MATCH (q:Quelle)               WHERE q.external_sources IS NOT NULL RETURN count(q);
// MATCH ()-[r]->()               WHERE r.source IS NOT NULL OR r.evidence IS NOT NULL
//                                   OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL
//                                RETURN count(r);
