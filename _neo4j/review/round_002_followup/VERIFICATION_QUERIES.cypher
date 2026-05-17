// Verification Cypher — round 002 followup
//
// Purpose: read-only sanity queries to confirm each phase landed as expected.
// Run any of these against the live `mit-bestand` database at any time.
//
// Removal / rollback is done via prompting + selective DETACH DELETE — these
// queries are the safe inspection counterpart.
//
// ============================================================================
// SECTION 0 — Top-level health check (one number per phase)
// ============================================================================

// Total nodes + rels
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// Expected after all phases: 2 296 nodes / 16 822 rels.

// Count by label (top 20)
MATCH (n)
UNWIND labels(n) AS lab
RETURN lab, count(*) AS n
ORDER BY n DESC
LIMIT 20;

// Count by rel type
MATCH ()-[r]->()
RETURN type(r) AS rel, count(*) AS n
ORDER BY n DESC;

// ============================================================================
// SECTION A — Phase A: Schadstoff + BauwerkEra + Land properties
// ============================================================================

// 1. Schadstoff total (expected 8 after Phase A, still 8 after all later phases)
MATCH (s:Schadstoff) RETURN count(s) AS schadstoff_total;

// 2. Schadstoff-Material grounding (expected ≥ 18 after Phase A)
MATCH (:Schadstoff)-[r:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN count(r) AS schadstoff_material_rels;

// 3. Schadstoff-BauwerkEra grounding (expected 15)
MATCH (:Schadstoff)-[r:TYPISCH_BEI_ERA]->(:BauwerkEra)
RETURN count(r) AS schadstoff_era_rels;

// 4. Land Asbest ban-year coverage (expected 11)
MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL
RETURN l.id, l.name, l.asbest_verbot_jahr
ORDER BY l.asbest_verbot_jahr;

// 5. Project quantitative-backfill source tag (expected 14)
MATCH (p:Projekt) WHERE p.property_source IS NOT NULL
RETURN count(p) AS projects_with_property_source;

// ============================================================================
// SECTION B — Phase B: Bauproduktstatus + Norm country grounding
// ============================================================================

// 6. Bauproduktstatus total (expected 15)
MATCH (b:Bauproduktstatus) RETURN count(b) AS bauproduktstatus_total;

// 7. Country defaults — Land HAT_TYPISCHEN_BAUPRODUKTSTATUS (expected 19)
MATCH (l:Land)-[r:HAT_TYPISCHEN_BAUPRODUKTSTATUS]->(:Bauproduktstatus)
RETURN count(r) AS country_default_status_rels;

// 8. BG-level Bauproduktstatus (expected ≥ 37)
MATCH (:Bauteilgruppe)-[r:HAT_BAUPRODUKTSTATUS]->(:Bauproduktstatus)
RETURN count(r) AS bg_bauproduktstatus_rels;

// 9. Norms GILT_IN_LAND (expected ≥ 28)
MATCH (:Norm)-[r:GILT_IN_LAND]->(:Land)
RETURN count(r) AS norm_land_rels;

// 10. Norm total (expected ≥ 30)
MATCH (n:Norm) RETURN count(n) AS norm_total;

// ============================================================================
// SECTION C — Phase C: PruefungNachweis + Verbindungstechnik + Förderprogramm
// ============================================================================

// 11. PruefungNachweis total (expected 20)
MATCH (p:PruefungNachweis) RETURN count(p) AS pruefung_total;

// 12. PruefungNachweis Material grounding (expected 12)
MATCH (:PruefungNachweis)-[r:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN count(r) AS pruefung_material_rels;

// 13. Verbindungstechnik total (expected 12)
MATCH (v:Verbindungstechnik) RETURN count(v) AS verbindung_total;

// 14. ERHALT_FOERDERUNG_DURCH coverage (expected 2 after Phase C — known low)
MATCH ()-[r:ERHALT_FOERDERUNG_DURCH]->()
RETURN count(r) AS foerderprogramm_rels;

// ============================================================================
// SECTION D — Phase D: Aufbereitungsverfahren tree
// ============================================================================

// 15. Aufbereitungsverfahren total (expected 45)
MATCH (a:Aufbereitungsverfahren) RETURN count(a) AS aufbereitung_total;

// 16. Sub-procedure tree depth (expected ≥ 19 IST_UNTERVERFAHREN_VON)
MATCH (:Aufbereitungsverfahren)-[r:IST_UNTERVERFAHREN_VON]->(:Aufbereitungsverfahren)
RETURN count(r) AS sub_procedure_rels;

// 17. BG Aufbereitung coverage (expected 225/306)
MATCH (bg:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)
WITH count(DISTINCT bg) AS bgs_with
MATCH (bg2:Bauteilgruppe)
RETURN bgs_with, count(bg2) AS bg_total,
       round(100.0 * bgs_with / count(bg2), 1) AS pct;

// ============================================================================
// SECTION E — Phase E: LebenszyklusModul + Layer + Marktmodell seed
// ============================================================================

// 18. LebenszyklusModul + METHODENGRUNDLAGE_NORM (expected 5 modules + 8 rels)
MATCH (l:LebenszyklusModul) RETURN count(l) AS lebenszyklusmodul_total;
MATCH (:LebenszyklusModul)-[r:METHODENGRUNDLAGE_NORM]->(:Norm)
RETURN count(r) AS methodengrundlage_rels;

// 19. Projects with BERECHNET_NACH_MODUL (expected 6)
MATCH (p:Projekt)-[r:BERECHNET_NACH_MODUL]->(:LebenszyklusModul)
RETURN count(DISTINCT p) AS projects_with_lca;

// 20. Layer + TEILT_LAYER (expected 6 layers + 15 rels)
MATCH (l:Layer) RETURN count(l) AS layer_total;
MATCH (:Bauteiltyp)-[r:TEILT_LAYER]->(:Layer)
RETURN count(r) AS teilt_layer_rels;

// 21. Marktmodell seed (after Phase E: 11 nodes, some with BG edges)
MATCH (m:Marktmodell) RETURN count(m) AS marktmodell_total;

// ============================================================================
// SECTION F — Phase F: Defekt + MatchingQualitaet seed
// ============================================================================

// 22. Defekt total (expected 10)
MATCH (d:Defekt) RETURN count(d) AS defekt_total;

// 23. Defekt-Material grounding (expected 14)
MATCH (:Defekt)-[r:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN count(r) AS defekt_material_rels;

// 24. MatchingQualitaet total (expected 9)
MATCH (m:MatchingQualitaet) RETURN count(m) AS matchingqualitaet_total;

// ============================================================================
// SECTION G — Phase G: archive-scan project-level tagging
// ============================================================================

// 25. Project-level Defekt tags (expected ≥ 22; 19/76 projects covered)
MATCH (p:Projekt)-[r:HAT_DEFEKT_BEFUND]->(:Defekt)
RETURN count(r) AS rels, count(DISTINCT p) AS projects_covered;

// 26. Project-level MatchingQualitaet tags (expected ≥ 165 rels across 75/76 projects)
MATCH (p:Projekt)-[r:HAT_MATCHINGQUALITAET]->(:MatchingQualitaet)
RETURN count(r) AS rels, count(DISTINCT p) AS projects_covered;

// 27. Project-level Marktmodell tags (after Phase G + I: ≥ 89 rels across ≥ 50 projects)
MATCH (p:Projekt)-[r:HAT_DOMINANT_MARKTMODELL]->(:Marktmodell)
RETURN count(r) AS rels, count(DISTINCT p) AS projects_covered;

// 28. Phase G evidence trail — all tags carry source archive
MATCH (p:Projekt)-[r:HAT_DEFEKT_BEFUND|HAT_MATCHINGQUALITAET|HAT_DOMINANT_MARKTMODELL]->(x)
WHERE r.source IS NULL
RETURN count(r) AS rels_missing_source;  // expect 0

// ============================================================================
// SECTION H — Phase H: ZustandsKlasse + Wirtschaft (payback) + Akzeptanz
// ============================================================================

// 29. ZustandsKlasse total (expected 6)
MATCH (z:ZustandsKlasse) RETURN count(z) AS zustandsklasse_total;

// 30. ZustandsKlasse-Material grounding (expected 12)
MATCH (:ZustandsKlasse)-[r:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN count(r) AS zk_material_rels;

// 31. Akzeptanz + GILT_IN_LAND (expected 5 nodes + 7 country rels)
MATCH (a:Akzeptanz) RETURN count(a) AS akzeptanz_total;
MATCH (:Akzeptanz)-[r:GILT_IN_LAND]->(:Land)
RETURN count(r) AS akzeptanz_country_rels;

// 32. Wirtschaft (new payback-model axis added Phase H — 6 new nodes)
MATCH (w:Wirtschaft) WHERE w.id STARTS WITH 'wi_capex_' OR w.id = 'wi_hidden_costs_lagerung_pruefung'
RETURN count(w) AS wirtschaft_payback_total;

// ============================================================================
// SECTION I — Phase I: orphan rescue + Marktmodell widening
// ============================================================================

// 33. Orphan vocab check — all Phase F/H seed vocabs should now connect
MATCH (n) WHERE any(l IN labels(n) WHERE l IN ['Defekt','MatchingQualitaet','Marktmodell','Akzeptanz','ZustandsKlasse'])
OPTIONAL MATCH (n)-[r]-()
WITH n, count(r) AS deg
WHERE deg = 0
RETURN labels(n)[0] AS label, n.id, n.name
ORDER BY label, n.id;
// Expected remaining orphans (intentional non-events):
//   ZustandsKlasse: zk_unbekannt_pruefung_offen
//   Marktmodell:    mm_rueckkauf, mm_unbekannt

// 34. Akzeptanz project-level (added Phase I)
MATCH (p:Projekt)-[r:HAT_DOMINANT_AKZEPTANZ]->(:Akzeptanz)
RETURN count(r) AS rels, count(DISTINCT p) AS projects;

// ============================================================================
// SECTION J — Phase J: Wirtschaft per-project tagging
// ============================================================================

// 35. Project-level Wirtschaft tags (expected 20)
MATCH (p:Projekt)-[r:HAT_WIRTSCHAFT]->(:Wirtschaft)
RETURN count(r) AS rels, count(DISTINCT p) AS projects;

// 36. By payback-model breakdown
MATCH (p:Projekt)-[:HAT_WIRTSCHAFT]->(w:Wirtschaft)
RETURN w.id, w.name, count(DISTINCT p) AS projects
ORDER BY projects DESC;

// ============================================================================
// SECTION R003 — Round 003: BG-level propagation
// ============================================================================

// 37. BG-level Defekt (expected 31)
MATCH (:Bauteilgruppe)-[r:HAT_DEFEKT]->(:Defekt) RETURN count(r) AS bg_defekt_rels;

// 38. BG-level Marktmodell after Round 003 (expected 355 = 34 pre + 321 propagated)
MATCH (:Bauteilgruppe)-[r:HAT_MARKTMODELL]->(:Marktmodell) RETURN count(r) AS bg_marktmodell_rels;

// 39. Round-003 provenance audit — every propagated rel carries its source
MATCH ()-[r]->() WHERE r.source IN ['round_003_material_propagation', 'round_003_project_propagation']
RETURN r.source, type(r), count(*) ORDER BY count(*) DESC;

// ============================================================================
// SECTION K — Phase K: overall connectivity targets
// ============================================================================

// 40. Bauteilgruppe coverage of each reuse dimension
UNWIND [
  {dim: 'Material',           rel: 'NUTZT_MATERIAL'},
  {dim: 'Aufbereitung',       rel: 'HAT_AUFBEREITUNG'},
  {dim: 'Pruefung',           rel: 'HAT_PRUEFUNG'},
  {dim: 'Verbindungstechnik', rel: 'HAT_VERBINDUNGSTECHNIK'},
  {dim: 'Marktmodell',        rel: 'HAT_MARKTMODELL'},
  {dim: 'Defekt',             rel: 'HAT_DEFEKT'},
  {dim: 'Bauproduktstatus',   rel: 'HAT_BAUPRODUKTSTATUS'},
  {dim: 'Norm',               rel: 'REFERENZIERT_NORM'},
  {dim: 'Rückbau',            rel: 'HAT_RUECKBAUVERFAHREN'},
  {dim: 'Logistik',           rel: 'HAT_LOGISTIK'}
] AS d
CALL {
  WITH d
  MATCH (bg:Bauteilgruppe)
  WITH d, count(bg) AS total
  MATCH (bg2:Bauteilgruppe)
  WHERE EXISTS { MATCH (bg2)-[r]->() WHERE type(r) = d.rel }
  RETURN total, count(DISTINCT bg2) AS with_edge
}
RETURN d.dim AS dimension, d.rel AS rel_type,
       with_edge, total,
       round(100.0 * with_edge / total, 1) AS pct;

// 41. Projekt coverage (non-stub) of each project-level dimension
UNWIND [
  {dim: 'Land',          rel: 'LIEGT_IN_LAND'},
  {dim: 'Bauwerk',       rel: 'NUTZT_BAUWERK'},
  {dim: 'Bauteilgruppe', rel: 'HAT_BAUTEILGRUPPE'},
  {dim: 'Defekt-Befund', rel: 'HAT_DEFEKT_BEFUND'},
  {dim: 'Matching',      rel: 'HAT_MATCHINGQUALITAET'},
  {dim: 'Marktmodell',   rel: 'HAT_DOMINANT_MARKTMODELL'},
  {dim: 'Akzeptanz',     rel: 'HAT_DOMINANT_AKZEPTANZ'},
  {dim: 'Wirtschaft',    rel: 'HAT_WIRTSCHAFT'},
  {dim: 'LCA-Modul',     rel: 'BERECHNET_NACH_MODUL'},
  {dim: 'Norm',          rel: 'REFERENZIERT_NORM'}
] AS d
CALL {
  WITH d
  MATCH (p:Projekt) WHERE p.node_role IS NULL OR p.node_role = 'full_projekt'
  WITH d, count(p) AS total, collect(p) AS all_p
  UNWIND all_p AS p
  OPTIONAL MATCH (p)-[r]->() WHERE type(r) = d.rel
  WITH d, total, p, count(r) AS edges
  WITH d, total, sum(CASE WHEN edges > 0 THEN 1 ELSE 0 END) AS with_edge
  RETURN total, with_edge
}
RETURN d.dim AS dimension, d.rel AS rel_type,
       with_edge, total,
       round(100.0 * with_edge / total, 1) AS pct;

// ============================================================================
// SECTION SHARP — Combination queries: cross-cutting insights
// ============================================================================

// 42. Steel-reuse projects without corrosion-screening evidence
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id: 'mat_stahl'})
WHERE NOT EXISTS { (bg)-[:HAT_DEFEKT]->(:Defekt {id: 'def_korrosion'}) }
RETURN p.name, collect(DISTINCT bg.id) AS unguarded_bgs
LIMIT 20;

// 43. Projects combining same-site reuse + DGNB acceptance (high-prestige reuse)
MATCH (p:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(:Marktmodell {id: 'mm_same_site'})
MATCH (p)-[:HAT_DOMINANT_AKZEPTANZ]->(:Akzeptanz {id: 'ak_dgnb_zertifizierung'})
RETURN p.name;

// 44. Cost-model × matching-quality cross-tab
MATCH (p:Projekt)-[:HAT_WIRTSCHAFT]->(w:Wirtschaft)
MATCH (p)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
RETURN w.id AS cost_model, mq.id AS matching_axis, count(DISTINCT p) AS n
ORDER BY n DESC;

// 45. Per-country reuse-quality fingerprint
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
MATCH (p)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
RETURN l.name AS country,
       split(mq.id, '_')[1] AS axis,
       split(mq.id, '_')[2] AS value,
       count(DISTINCT p) AS n
ORDER BY country, axis;

// 46. Rare rel types (≤ 3 instances) — candidates for cleanup
CALL db.relationshipTypes() YIELD relationshipType
CALL { WITH relationshipType MATCH ()-[r]->() WHERE type(r) = relationshipType RETURN count(r) AS n }
WITH relationshipType, n WHERE n <= 3
RETURN relationshipType, n ORDER BY n;

// 47. Stub Projekt inventory (23 expected)
MATCH (p:Projekt {node_role: 'cross_reference_stub'})
OPTIONAL MATCH (p)<-[r]-()
RETURN p.id, p.name, count(r) AS deg ORDER BY deg DESC;

// 48. Stub Akteur inventory (16 expected — degree 0 or 1)
MATCH (a:Akteur)
OPTIONAL MATCH (a)-[r]-()
WITH a, count(r) AS deg WHERE deg <= 1
RETURN a.id, a.name, deg ORDER BY deg, a.id;
