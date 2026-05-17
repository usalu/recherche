// =============================================================================
//
//  Graph-output exploration queries — round 002 followup
//  All queries tested 2026-05-17, all return Node / Relationship / Path objects
//  so Neo4j Browser renders them as a subgraph (not a table).
//
//  Layout:
//    PART 1 — one query per recent change (Phases A through K + Round 003)
//             each shows the new layer connected to existing structure
//    PART 2 — cross-cutting combinations that pull together multiple phases
//             (cluster maps, gap finders, fingerprints, intersections)
//
//  Removal / rollback happens via prompting + selective DETACH DELETE.
//  Full per-phase backups under _neo4j/review/backups/<phase>_pre_apply/.
//
// =============================================================================


// =============================================================================
// PART 1 — One per recent change, each showing how the new layer connects
//          to the existing graph
// =============================================================================

// PA. Phase A — Schadstoff full grounding.
//     New Schadstoff nodes anchored to existing Material, BauwerkEra, Bauteiltyp.
//     Shows the three-axis screening map for each pollutant.
MATCH (s:Schadstoff)
OPTIONAL MATCH (s)-[r1:TYPISCH_BEI_MATERIAL]->(m:Material)
OPTIONAL MATCH (s)-[r2:TYPISCH_BEI_ERA]->(era:BauwerkEra)
OPTIONAL MATCH (s)-[r3:TYPISCH_BEI_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN s, r1, m, r2, era, r3, bt;


// PB. Phase B — Country regulatory stack (Germany).
//     New Norm + Bauproduktstatus + Akzeptanz nodes anchored to existing Land.
//     Swap the id 'land_deutschland' for any country slug to compare regimes.
MATCH (l:Land {id: 'land_deutschland'})
OPTIONAL MATCH (l)<-[r1:GILT_IN_LAND]-(n:Norm)
OPTIONAL MATCH (l)-[r2:HAT_TYPISCHEN_BAUPRODUKTSTATUS]->(bps:Bauproduktstatus)
OPTIONAL MATCH (l)<-[r3:GILT_IN_LAND]-(ak:Akzeptanz)
RETURN l, r1, n, r2, bps, r3, ak;


// PC. Phase C — Reuse-test recipe for steel.
//     New PruefungNachweis + Verbindungstechnik nodes shown via Material,
//     with Defekt grounding overlaid. Tells you what to test + how to join +
//     what can go wrong when reusing steel.
MATCH (m:Material {id: 'mat_stahl'})
OPTIONAL MATCH (m)<-[r1:TYPISCH_BEI_MATERIAL]-(pn:PruefungNachweis)
OPTIONAL MATCH (m)<-[r2:TYPISCH_BEI_MATERIAL]-(def:Defekt)
OPTIONAL MATCH (bg:Bauteilgruppe)-[r3:NUTZT_MATERIAL]->(m)
OPTIONAL MATCH (bg)-[r4:HAT_VERBINDUNGSTECHNIK]->(vt:Verbindungstechnik)
RETURN m, r1, pn, r2, def, r3, bg, r4, vt LIMIT 80;


// PD. Phase D — Aufbereitungsverfahren parent-child taxonomy.
//     The full processing-method tree as one path subgraph.
MATCH path = (child:Aufbereitungsverfahren)-[:IST_UNTERVERFAHREN_VON]->(parent:Aufbereitungsverfahren)
RETURN path;


// PE. Phase E — LCA modules anchored to their methodological norms (+ projects).
//     New LebenszyklusModul nodes connected to existing Norm + Projekt.
//     Shows DIN EN 15978 / 15804 family as the methodological backbone.
MATCH (lz:LebenszyklusModul)
OPTIONAL MATCH (lz)-[r1:METHODENGRUNDLAGE_NORM]->(n:Norm)
OPTIONAL MATCH (p:Projekt)-[r2:BERECHNET_NACH_MODUL]->(lz)
RETURN lz, r1, n, r2, p;


// PF. Phase F — Defekt grounding map.
//     New Defekt nodes anchored to existing Material via TYPISCH_BEI_MATERIAL.
//     The 14-edge map of "which defects to expect on which material".
MATCH path = (:Defekt)-[:TYPISCH_BEI_MATERIAL]->(:Material)
RETURN path;


// PG. Phase G — One project's full archive-scan fingerprint (K.118).
//     Project at the centre, with all archive-scan tags around it:
//     Defekt-Befund, MatchingQualitaet, dominant Marktmodell, dominant Akzeptanz,
//     Wirtschaft cost-model, plus the project's Land.
//     Swap the project id to fingerprint any other case study.
MATCH (p:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})
OPTIONAL MATCH (p)-[r1:HAT_DEFEKT_BEFUND]->(def:Defekt)
OPTIONAL MATCH (p)-[r2:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
OPTIONAL MATCH (p)-[r3:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
OPTIONAL MATCH (p)-[r4:HAT_DOMINANT_AKZEPTANZ]->(ak:Akzeptanz)
OPTIONAL MATCH (p)-[r5:HAT_WIRTSCHAFT]->(wi:Wirtschaft)
OPTIONAL MATCH (p)-[r6:LIEGT_IN_LAND]->(l:Land)
RETURN p, r1, def, r2, mq, r3, mm, r4, ak, r5, wi, r6, l;


// PH. Phase H — ZustandsKlasse + Akzeptanz together.
//     New condition-grade nodes shown via Material, alongside acceptance nodes
//     shown via Land. Two parallel Phase-H sub-vocabs in one view.
MATCH (zk:ZustandsKlasse) OPTIONAL MATCH (zk)-[r1:TYPISCH_BEI_MATERIAL]->(m:Material)
WITH collect({zk: zk, r1: r1, m: m}) AS zk_rows
MATCH (ak:Akzeptanz) OPTIONAL MATCH (ak)-[r2:GILT_IN_LAND]->(l:Land)
UNWIND zk_rows AS zr
RETURN zr.zk AS zk, zr.r1 AS r1, zr.m AS m, ak, r2, l;


// PI. Phase I — Orphan-rescue subgraph.
//     Every project-level rel created during manual orphan rescue, with its
//     vocab target. Shows which projects pulled which previously-orphan
//     vocab nodes into the connected graph.
MATCH (p:Projekt)-[r]->(v)
WHERE r.source = 'manual_orphan_rescue'
RETURN p, r, v LIMIT 100;


// PJ. Phase J — Cost-model × project × country (Wirtschaft per project).
//     New HAT_WIRTSCHAFT rels from project to payback-model node, plus the
//     country anchor. Shows where each cost story is told.
MATCH (p:Projekt)-[r1:HAT_WIRTSCHAFT]->(wi:Wirtschaft)
OPTIONAL MATCH (p)-[r2:LIEGT_IN_LAND]->(l:Land)
RETURN p, r1, wi, r2, l;


// R003. Round 003 — BG-level Defekt propagation evidence.
//       Shows the inference chain: project → BG → defect at BG level, plus
//       the material that justifies the propagation. Provenance tag
//       r.source = 'round_003_material_propagation' filters to only the
//       inferred edges (so the subgraph is auditable).
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[r:HAT_DEFEKT]->(d:Defekt)
WHERE r.source = 'round_003_material_propagation'
OPTIONAL MATCH (bg)-[r2:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(d)
RETURN p, bg, d, r, r2, m LIMIT 60;


// =============================================================================
// PART 2 — Cross-cutting combinations
// =============================================================================

// X1. Steel-reuse community — projects sharing reused steel via one Material node.
//     Each pair of projects that both reuse steel connects through `mat_stahl`,
//     creating a hub-and-spoke graph of the steel-reuse community.
MATCH (p1:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg1:Bauteilgruppe)
      -[:NUTZT_MATERIAL]->(m:Material {id: 'mat_stahl'})
WITH p1, bg1, m
MATCH (p2:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg2:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
WHERE id(p1) < id(p2)
RETURN p1, bg1, m, bg2, p2 LIMIT 40;


// X2. GAP FINDER — steel-reuse BGs without explicit corrosion screening.
//     Surfaces a real-world quality-assurance gap as a visible subgraph:
//     these projects reuse steel but have no recorded corrosion check on the BG.
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:NUTZT_MATERIAL]->(m:Material {id: 'mat_stahl'})
WHERE NOT EXISTS { (bg)-[:HAT_DEFEKT]->(:Defekt {id: 'def_korrosion'}) }
OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN p, bg, m, l LIMIT 50;


// X3. Aesthetic-acceptance × community-donation intersection.
//     The three projects in the corpus that combine visible-patina acceptance
//     with community-donation sourcing. A small but conceptually-rich cluster.
MATCH (p:Projekt)-[r1:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell {id: 'mm_spende'})
MATCH (p)-[r2:HAT_DOMINANT_AKZEPTANZ]->(ak:Akzeptanz {id: 'ak_aesthetik_patinakultur'})
OPTIONAL MATCH (p)-[r3:LIEGT_IN_LAND]->(l:Land)
RETURN p, r1, mm, r2, ak, r3, l;


// X4. Country fingerprint — Switzerland.
//     Every Swiss project plus its matching-quality axes and dominant sourcing
//     model. Replace 'land_schweiz' to fingerprint another country.
MATCH (p:Projekt)-[r1:LIEGT_IN_LAND]->(l:Land {id: 'land_schweiz'})
OPTIONAL MATCH (p)-[r2:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
OPTIONAL MATCH (p)-[r3:HAT_DOMINANT_MARKTMODELL]->(mm:Marktmodell)
RETURN p, r1, l, r2, mq, r3, mm LIMIT 100;


// X5. Norm hubs — norms cited by ≥ 2 Bauteilgruppen.
//     The load-bearing standards (the ones actually used by multiple components
//     across projects). Renders as a hub-and-spoke around each shared norm.
MATCH (n:Norm)<-[:REFERENZIERT_NORM]-(bg:Bauteilgruppe)
WITH n, count(bg) AS bg_count WHERE bg_count >= 2
MATCH path = (:Bauteilgruppe)-[:REFERENZIERT_NORM]->(n)
RETURN path LIMIT 80;


// X6. Era × pollutant × material screening alert map.
//     For each BauwerkEra, which pollutants are typical and which materials
//     they affect. Combined with Land.asbest_verbot_jahr (a Phase A property)
//     this is the basis for any donor-screening workflow.
MATCH (era:BauwerkEra)
OPTIONAL MATCH (era)<-[r1:TYPISCH_BEI_ERA]-(s:Schadstoff)
OPTIONAL MATCH (s)-[r2:TYPISCH_BEI_MATERIAL]->(m:Material)
RETURN era, r1, s, r2, m;


// X7. Material reuse-pipeline — Holz with every grounded vocab.
//     One material at the centre, all reuse-quality vocabs that point to it:
//     Defekt, Aufbereitungsverfahren, PruefungNachweis, Schadstoff, ZustandsKlasse.
//     This is the "what we know about reusing wood" subgraph.
MATCH (m:Material {id: 'mat_holz'})
OPTIONAL MATCH (m)<-[r1:TYPISCH_BEI_MATERIAL]-(def:Defekt)
OPTIONAL MATCH (m)<-[r2:TYPISCH_BEI_MATERIAL]-(av:Aufbereitungsverfahren)
OPTIONAL MATCH (m)<-[r3:TYPISCH_BEI_MATERIAL]-(pn:PruefungNachweis)
OPTIONAL MATCH (m)<-[r4:TYPISCH_BEI_MATERIAL]-(sch:Schadstoff)
OPTIONAL MATCH (m)<-[r5:TYPISCH_BEI_MATERIAL]-(zk:ZustandsKlasse)
RETURN m, r1, def, r2, av, r3, pn, r4, sch, r5, zk;
