// =============================================================================
//
//  Verification + exploration Cypher — round 002 followup
//  All queries tested against mit-bestand on 2026-05-17.
//
//  PART A — VERIFICATION (table output)
//    Scalar counts that confirm each phase landed as expected.
//    Run these to sanity-check the graph at any point.
//
//  PART B — EXPLORATION (graph output, renders visually in Neo4j Browser)
//    Returns Nodes / Relationships / Paths so the Browser draws a subgraph
//    instead of a table. Best way to *see* what the recent phases unlocked.
//
//  PART C — SHARP CROSS-CUTS (mostly graph output)
//    Combinations that pull together multiple phases — gap finders, fingerprints,
//    cross-tabs as subgraphs.
//
//  Removal / rollback happens via prompting + selective DETACH DELETE.
//  Full per-phase backups under _neo4j/review/backups/<phase>_pre_apply/.
//
// =============================================================================


// =============================================================================
// PART A — VERIFICATION (table output)
// =============================================================================

// A0. Top-level health: total nodes + relationships.
//     Expected after all phases A–K + Round 003: 2 296 nodes / 16 822 rels.
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;

// A1. Count per label (top 30)
MATCH (n) UNWIND labels(n) AS lab
RETURN lab, count(*) AS n ORDER BY n DESC LIMIT 30;

// A2. Count per relationship type (full list)
MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n ORDER BY n DESC;

// A3. Phase A — Schadstoff seeded (8 expected), with Material + Era grounding
MATCH (s:Schadstoff) RETURN count(s) AS schadstoff_total;
MATCH ()-[r:TYPISCH_BEI_MATERIAL]->() RETURN count(r) AS typisch_material_total;
MATCH ()-[r:TYPISCH_BEI_ERA]->() RETURN count(r) AS typisch_era_total;

// A4. Phase A — Land asbestos-ban year coverage (11 expected)
MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL
RETURN l.id, l.name, l.asbest_verbot_jahr ORDER BY l.asbest_verbot_jahr;

// A5. Phase B — Bauproduktstatus + country defaults
MATCH (b:Bauproduktstatus) RETURN count(b) AS bauproduktstatus_total;  // 15
MATCH ()-[r:HAT_TYPISCHEN_BAUPRODUKTSTATUS]->() RETURN count(r) AS country_status_rels;  // 19
MATCH (:Bauteilgruppe)-[r:HAT_BAUPRODUKTSTATUS]->() RETURN count(r) AS bg_status_rels;  // 37

// A6. Phase B — Norms in force per country (28 expected)
MATCH (:Norm)-[r:GILT_IN_LAND]->(:Land) RETURN count(r) AS norm_country_rels;

// A7. Phase C — PruefungNachweis + Verbindungstechnik
MATCH (p:PruefungNachweis) RETURN count(p) AS pruefung_total;  // 20
MATCH (v:Verbindungstechnik) RETURN count(v) AS verbindung_total;  // 12

// A8. Phase D — Aufbereitungsverfahren tree (45 + 19 sub-procedure rels)
MATCH (a:Aufbereitungsverfahren) RETURN count(a) AS aufbereitung_total;
MATCH ()-[r:IST_UNTERVERFAHREN_VON]->() RETURN count(r) AS sub_procedure_rels;

// A9. Phase E — LebenszyklusModul + Layer + Marktmodell seed
MATCH (l:LebenszyklusModul) RETURN count(l) AS lz_total;  // 5
MATCH ()-[r:METHODENGRUNDLAGE_NORM]->() RETURN count(r) AS lz_norm_rels;  // 8
MATCH ()-[r:BERECHNET_NACH_MODUL]->() RETURN count(r) AS project_lca_rels;  // 8 across 6 projects
MATCH (l:Layer) RETURN count(l) AS layer_total;  // 6
MATCH ()-[r:TEILT_LAYER]->() RETURN count(r) AS teilt_layer_rels;  // 15

// A10. Phase F — Defekt + MatchingQualitaet seed
MATCH (d:Defekt) RETURN count(d) AS defekt_total;  // 10
MATCH (m:MatchingQualitaet) RETURN count(m) AS mq_total;  // 9

// A11. Phase G — project-level archive-scan tags
MATCH (p:Projekt)-[r:HAT_DEFEKT_BEFUND]->() RETURN count(r) AS rels, count(DISTINCT p) AS projects;        // 22 / 19
MATCH (p:Projekt)-[r:HAT_MATCHINGQUALITAET]->() RETURN count(r) AS rels, count(DISTINCT p) AS projects;   // 165 / 75
MATCH (p:Projekt)-[r:HAT_DOMINANT_MARKTMODELL]->() RETURN count(r) AS rels, count(DISTINCT p) AS projects; // 89 / 54

// A12. Phase H — ZustandsKlasse + Akzeptanz + Wirtschaft (payback)
MATCH (z:ZustandsKlasse) RETURN count(z) AS zk_total;  // 6
MATCH (a:Akzeptanz) RETURN count(a) AS akzeptanz_total;  // 5
MATCH (w:Wirtschaft) WHERE w.id STARTS WITH 'wi_capex_' OR w.id = 'wi_hidden_costs_lagerung_pruefung'
RETURN count(w) AS wirtschaft_payback_total;  // 6

// A13. Phase I — orphan-rescue audit (remaining intentional non-event orphans)
MATCH (n) WHERE any(l IN labels(n) WHERE l IN
  ['Defekt','MatchingQualitaet','Marktmodell','Akzeptanz','ZustandsKlasse'])
OPTIONAL MATCH (n)-[r]-()
WITH n, count(r) AS deg WHERE deg = 0
RETURN labels(n)[0] AS label, n.id, n.name ORDER BY label, n.id;
// Expected remaining: zk_unbekannt_pruefung_offen, mm_rueckkauf, mm_unbekannt

// A14. Phase J — Wirtschaft per-project tags (20 rels / 19 projects)
MATCH (p:Projekt)-[r:HAT_WIRTSCHAFT]->() RETURN count(r) AS rels, count(DISTINCT p) AS projects;

// A15. Round 003 — BG-level Defekt + Marktmodell propagation
MATCH (:Bauteilgruppe)-[r:HAT_DEFEKT]->() RETURN count(r) AS bg_defekt;  // 31
MATCH (:Bauteilgruppe)-[r:HAT_MARKTMODELL]->() RETURN count(r) AS bg_marktmodell;  // 355

// A16. Round 003 — provenance audit: every propagated rel carries its source
MATCH ()-[r]->() WHERE r.source IN
  ['round_003_material_propagation', 'round_003_project_propagation']
RETURN r.source, type(r), count(*) AS n ORDER BY n DESC;

// A17. Phase G evidence trail: any HAT_*_BEFUND / MATCHINGQUALITAET / MARKTMODELL / WIRTSCHAFT
//      rel missing a source pointer (should be 0)
MATCH (p:Projekt)-[r:HAT_DEFEKT_BEFUND|HAT_MATCHINGQUALITAET|HAT_DOMINANT_MARKTMODELL|HAT_DOMINANT_AKZEPTANZ|HAT_WIRTSCHAFT]->()
WHERE r.source IS NULL
RETURN count(r) AS rels_missing_source;

// A18. Stub inventories
MATCH (p:Projekt {node_role: 'cross_reference_stub'})
RETURN count(p) AS stub_projekte;  // 23
MATCH (a:Akteur) OPTIONAL MATCH (a)-[r]-()
WITH a, count(r) AS deg WHERE deg <= 1
RETURN count(*) AS stub_akteure;  // 16


// =============================================================================
// PART B — EXPLORATION (graph output — renders as a subgraph in the Browser)
// =============================================================================

// B1. K.118 — what was reused (project → BG → material paths).
//     Smallest project subgraph, ideal for first-time exploration.
MATCH p = (proj:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})
          -[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)
          -[:NUTZT_MATERIAL]->(:Material)
RETURN p LIMIT 50;

// B2. K.118 — full reuse chain across all dimensions (project, BG, material,
//     processing, testing, sourcing model, defects).
//     This is the "everything we know about one project" subgraph.
MATCH (proj:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})
OPTIONAL MATCH (proj)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
OPTIONAL MATCH (bg)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)
OPTIONAL MATCH (bg)-[:HAT_PRUEFUNG]->(pn:PruefungNachweis)
OPTIONAL MATCH (bg)-[:HAT_MARKTMODELL]->(mm:Marktmodell)
OPTIONAL MATCH (bg)-[:HAT_DEFEKT]->(d:Defekt)
RETURN proj, bg, m, av, pn, mm, d LIMIT 200;

// B3. Steel-reuse fingerprint — every project + BG that touches reused steel.
//     Useful to see how many projects converge on the same material node.
MATCH p = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)
          -[:NUTZT_MATERIAL]->(:Material {id: 'mat_stahl'})
RETURN p LIMIT 100;

// B4. Country regulatory stack — Germany.
//     Norms in force + product-status options + acceptance frameworks, all in one view.
MATCH (l:Land {id: 'land_deutschland'})
OPTIONAL MATCH (l)<-[:GILT_IN_LAND]-(n:Norm)
OPTIONAL MATCH (l)-[:HAT_TYPISCHEN_BAUPRODUKTSTATUS]->(bps:Bauproduktstatus)
OPTIONAL MATCH (l)<-[:GILT_IN_LAND]-(ak:Akzeptanz)
RETURN l, n, bps, ak LIMIT 100;

// B5. Defekt grounding map — all Defekt nodes with the Material(s) they apply to.
MATCH p = (:Defekt)-[:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN p;

// B6. Reuse-quality fingerprint of one project (Resource Rows Copenhagen).
//     Shows MQ axes + defects + sourcing + acceptance + cost-model + country.
MATCH (proj:Projekt {id: 'p_resource_rows_copenhagen'})
OPTIONAL MATCH (proj)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
OPTIONAL MATCH (proj)-[:HAT_DEFEKT_BEFUND]->(def:Defekt)
OPTIONAL MATCH (proj)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
OPTIONAL MATCH (proj)-[:HAT_DOMINANT_AKZEPTANZ]->(ak:Akzeptanz)
OPTIONAL MATCH (proj)-[:HAT_WIRTSCHAFT]->(w:Wirtschaft)
OPTIONAL MATCH (proj)-[:LIEGT_IN_LAND]->(l:Land)
RETURN proj, mq, def, mm, ak, w, l;

// B7. Aufbereitungsverfahren parent–child tree.
//     The full processing-method taxonomy as one tree (19 IST_UNTERVERFAHREN_VON edges).
MATCH p = (:Aufbereitungsverfahren)-[:IST_UNTERVERFAHREN_VON]->(:Aufbereitungsverfahren)
RETURN p;

// B8. Schadstoff × BauwerkEra × Material — what pollutant occurs in what era and material.
//     Renders the era-and-material screening map.
MATCH (era:BauwerkEra)
OPTIONAL MATCH (s:Schadstoff)-[:TYPISCH_BEI_ERA]->(era)
OPTIONAL MATCH (s)-[:TYPISCH_BEI_MATERIAL]->(m:Material)
RETURN era, s, m;

// B9. Acceptance landscape — which certifications are accepted in which countries.
MATCH p = (:Akzeptanz)-[:GILT_IN_LAND]->(:Land)
RETURN p;

// B10. LCA modules + the norms they invoke.
//      Shows DIN_EN_15804, DIN_EN_15978 etc. anchored to A1–D modules.
MATCH p = (:LebenszyklusModul)-[:METHODENGRUNDLAGE_NORM]->(:Norm)
RETURN p;

// B11. Top-5 most-connected projects + their 1-hop neighborhood.
//      A first visual answer to "which projects are the hubs."
MATCH (proj:Projekt) WHERE proj.node_role IS NULL OR proj.node_role = 'full_projekt'
WITH proj
OPTIONAL MATCH (proj)-[r1]-()
WITH proj, count(r1) AS deg ORDER BY deg DESC LIMIT 5
MATCH p = (proj)-[]-()
RETURN p LIMIT 200;


// =============================================================================
// PART C — SHARP CROSS-CUTS (mostly graph output)
// =============================================================================

// C1. Cross-project material flow — which projects share the same reused steel.
//     Each pair is connected through one Material node — visualizes
//     "the steel-reuse community" as one subgraph.
MATCH (p1:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg1:Bauteilgruppe)
       -[:NUTZT_MATERIAL]->(m:Material {id: 'mat_stahl'})
WITH p1, bg1, m
MATCH (p2:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg2:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
WHERE id(p1) < id(p2)
RETURN p1, bg1, m, bg2, p2 LIMIT 40;

// C2. Same-site reuse projects with their reused materials.
//     Visualizes the in-situ-reuse cluster.
MATCH (proj:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell {id: 'mm_same_site'})
OPTIONAL MATCH (proj)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
RETURN proj, mm, bg, m LIMIT 100;

// C3. Aesthetic-acceptance × donation-based reuse intersection.
//     The "patina-culture + community-donation" projects (3 in current graph).
MATCH (proj:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell {id: 'mm_spende'})
MATCH (proj)-[:HAT_DOMINANT_AKZEPTANZ]->(ak:Akzeptanz {id: 'ak_aesthetik_patinakultur'})
OPTIONAL MATCH (proj)-[:LIEGT_IN_LAND]->(l:Land)
RETURN proj, mm, ak, l;

// C4. GAP FINDER — steel-reuse projects without explicit corrosion screening.
//     Surfaces a real-world quality-assurance gap as a visible subgraph.
MATCH (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
       -[:NUTZT_MATERIAL]->(m:Material {id: 'mat_stahl'})
WHERE NOT EXISTS { (bg)-[:HAT_DEFEKT]->(:Defekt {id: 'def_korrosion'}) }
OPTIONAL MATCH (proj)-[:LIEGT_IN_LAND]->(l:Land)
RETURN proj, bg, m, l LIMIT 50;

// C5. Cost-model × matching-axis as a graph.
//     Each project connects a cost-model node to a matching-axis node;
//     shared nodes show which combinations cluster.
MATCH (proj:Projekt)-[:HAT_WIRTSCHAFT]->(w:Wirtschaft)
MATCH (proj)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
RETURN proj, w, mq LIMIT 100;

// C6. Per-country reuse fingerprint — Switzerland.
//     Country + all its projects + their matching axes + their sourcing models.
MATCH (proj:Projekt)-[:LIEGT_IN_LAND]->(l:Land {id: 'land_schweiz'})
OPTIONAL MATCH (proj)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
OPTIONAL MATCH (proj)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
RETURN proj, l, mq, mm LIMIT 100;

// C7. Platform-mediated projects (Concular / Madaster / Rotor / Restado).
//     All projects whose dominant sourcing is platform-vermittelt — useful for
//     mapping who the early-adopter projects are.
MATCH (proj:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell {id: 'mm_plattform_vermittelt'})
OPTIONAL MATCH (proj)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN proj, mm, bg LIMIT 100;

// C8. Norm hubs — norms cited by more than one BG.
//     Shows which standards are actually load-bearing for many components.
MATCH (n:Norm)<-[:REFERENZIERT_NORM]-(bg:Bauteilgruppe)
WITH n, count(bg) AS bg_count WHERE bg_count > 1
MATCH p = (:Bauteilgruppe)-[:REFERENZIERT_NORM]->(n)
RETURN p LIMIT 80;

// C9. Reuse-pipeline coverage for one material (Holz).
//     Material at center; all Defekt / Aufbereitung / Pruefung / Schadstoff
//     nodes that the graph says are typical for it.
MATCH (m:Material {id: 'mat_holz'})
OPTIONAL MATCH (m)<-[:TYPISCH_BEI_MATERIAL]-(def:Defekt)
OPTIONAL MATCH (m)<-[:TYPISCH_BEI_MATERIAL]-(av:Aufbereitungsverfahren)
OPTIONAL MATCH (m)<-[:TYPISCH_BEI_MATERIAL]-(pn:PruefungNachweis)
OPTIONAL MATCH (m)<-[:TYPISCH_BEI_MATERIAL]-(sch:Schadstoff)
OPTIONAL MATCH (m)<-[:TYPISCH_BEI_MATERIAL]-(zk:ZustandsKlasse)
RETURN m, def, av, pn, sch, zk;

// C10. Donor-receiver Bauwerk subgraph for one donor.
//      Picks an active donor and shows the receiver-side BGs it supplied.
//      Replace the donor id with another to explore other reuse chains.
MATCH (bw:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)
WITH bw, count(bg) AS donor_bg_count
ORDER BY donor_bg_count DESC LIMIT 1
MATCH p = (bg:Bauteilgruppe)-[:AUS_BAUWERK]->(bw)
RETURN bw, p LIMIT 80;

// C11. Era × Pollutant × Country — screening alert map.
//      A BauwerkEra cluster shows which pollutants to screen for and which
//      countries have legal bans on which year (Land.asbest_verbot_jahr).
MATCH (era:BauwerkEra)
OPTIONAL MATCH (era)<-[:TYPISCH_BEI_ERA]-(s:Schadstoff)
OPTIONAL MATCH (l:Land) WHERE l.asbest_verbot_jahr IS NOT NULL
RETURN era, s, l LIMIT 80;

// C12. Project quality-profile clusters (HAT_MATCHINGQUALITAET sharing).
//      Projects that share a matching-axis node — clusters reveal "reuse-style families."
MATCH (p1:Projekt)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
       <-[:HAT_MATCHINGQUALITAET]-(p2:Projekt)
WHERE id(p1) < id(p2) AND mq.id IN ['mq_temporal_storage', 'mq_geographic_local', 'mq_spec_zweckaenderung']
RETURN p1, mq, p2 LIMIT 60;
