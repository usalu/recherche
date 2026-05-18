// =============================================================================
//
//  Twenty most-interesting exploration queries — full graph
//  All tested 2026-05-18.
//
//  Every query returns Node / Relationship / Path objects so Neo4j Browser
//  renders them as a subgraph (not a table). LIMITs are deliberately large
//  (1 000–5 000) so the Browser sees enough of the structure — it will still
//  cap visualisation to its own per-result node ceiling (default ~300, raise
//  via :config initialNodeDisplay).
//
//  Each query has a short note saying WHAT it shows + WHY it is interesting.
//  All ids in the queries (project ids, material ids, country ids, role ids)
//  can be swapped to explore a different slice.
//
//  Last-tested sizes (rows / distinct nodes) shown at the end of each note.
//
// =============================================================================


// -----------------------------------------------------------------------------
// Q1 — Top hubs: the most-connected projects + their full 1-hop neighborhood.
//      Picks the 15 highest-degree projects and dumps every neighbor.
//      Best first-pass "where is the gravity" view.
//      [976 rows / 524 nodes]
// -----------------------------------------------------------------------------
MATCH (p:Projekt) WHERE p.node_role IS NULL OR p.node_role = 'full_projekt'
OPTIONAL MATCH (p)-[]-()
WITH p, count(*) AS deg ORDER BY deg DESC LIMIT 15
MATCH path = (p)-[]-()
RETURN path LIMIT 5000;


// -----------------------------------------------------------------------------
// Q2 — Project ecosystem (2-hop) — K.118 as the seed.
//      Two-hop variable-length traversal from one project. Catches actors,
//      buildings, BGs, the BGs' materials/processing/testing/sourcing, the
//      country, the sources cited. Swap the id to explore other projects.
//      [2 000 rows / 1 106 nodes]
// -----------------------------------------------------------------------------
MATCH path = (p:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})-[*1..2]-(neighbor)
RETURN path LIMIT 2000;


// -----------------------------------------------------------------------------
// Q3 — Actor collaboration network — every pair of actors that share a project.
//      Bipartite via the shared Projekt. Clusters reveal recurring teams
//      (architect + structural engineer + reuse planner combinations).
//      [1 276 rows / 453 nodes]
// -----------------------------------------------------------------------------
MATCH (a1:Akteur)-[:BETEILIGT_AN]->(p:Projekt)<-[:BETEILIGT_AN]-(a2:Akteur)
WHERE id(a1) < id(a2)
  AND (p.node_role IS NULL OR p.node_role = 'full_projekt')
RETURN a1, p, a2 LIMIT 3000;


// -----------------------------------------------------------------------------
// Q4 — Architect portfolios. Design firms (ar_entwurf_planung) with ≥ 2
//      projects, expanded through their projects to the materials each project
//      reuses. Reveals which firms have a coherent material focus vs. a
//      generalist portfolio.
//      [181 rows / 130 nodes]
// -----------------------------------------------------------------------------
MATCH (a:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle {id: 'ar_entwurf_planung'})
WITH a MATCH (a)-[:BETEILIGT_AN]->(p:Projekt)
WITH a, count(DISTINCT p) AS pc WHERE pc >= 2
MATCH path = (a)-[:BETEILIGT_AN]->(proj:Projekt)-[:HAT_BAUTEILGRUPPE]
             ->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 3000;


// -----------------------------------------------------------------------------
// Q5 — Material reuse network. Materials reused by ≥ 3 projects, plus every
//      BG and project that uses them. The popular-materials hub map.
//      [443 rows / 384 nodes]
// -----------------------------------------------------------------------------
MATCH (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
WITH m, count(DISTINCT p) AS pc WHERE pc >= 3
MATCH path = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg2:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
RETURN path LIMIT 5000;


// -----------------------------------------------------------------------------
// Q6 — Material full reuse pipeline (steel as the example).
//      Material at the centre, every grounded vocab pointing at it (Defekt,
//      Aufbereitung, Pruefung, Schadstoff, ZustandsKlasse), every BG using
//      the material, every project owning those BGs. Swap mat_stahl to
//      mat_holz / mat_beton / mat_glas / mat_ziegel etc.
//      [1 332 rows / 170 nodes]
// -----------------------------------------------------------------------------
MATCH (m:Material {id: 'mat_stahl'})
OPTIONAL MATCH p1 = (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
OPTIONAL MATCH p2 = (m)<-[:TYPISCH_BEI_MATERIAL]-(vocab)
OPTIONAL MATCH p3 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN m, p1, p2, p3 LIMIT 3000;


// -----------------------------------------------------------------------------
// Q7 — Donor → Receiver building chains across the entire corpus.
//      Every component group sitting between a donor Bauwerk and a receiver
//      Bauwerk. The physical reuse flows.
//      [258 rows / 416 nodes]
// -----------------------------------------------------------------------------
MATCH path = (donor:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
RETURN path LIMIT 3000;


// -----------------------------------------------------------------------------
// Q8 — Circular buildings: Bauwerke acting as donor AND receiver.
//      Same building gave parts away and also received parts — the rare
//      truly-circular sites.
//      [103 rows / 89 nodes]
// -----------------------------------------------------------------------------
MATCH (bw:Bauwerk)
WHERE EXISTS { ()-[:AUS_BAUWERK]->(bw) }
  AND EXISTS { ()-[:EINGEBAUT_IN]->(bw) }
MATCH path = (bw)<-[:AUS_BAUWERK|EINGEBAUT_IN]-(bg:Bauteilgruppe)
RETURN bw, path LIMIT 2000;


// -----------------------------------------------------------------------------
// Q9 — Wiederverwendungskette explorer.
//      The explicit reuse-chain nodes (Wiederverwendungskette label), each
//      with its donor Bauwerk, receiver Bauwerk and the BGs that ride the chain.
//      [208 rows / 287 nodes]
// -----------------------------------------------------------------------------
MATCH (k:Wiederverwendungskette)
OPTIONAL MATCH p1 = (k)-[:AUS_BAUWERK]->(donor:Bauwerk)
OPTIONAL MATCH p2 = (k)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
OPTIONAL MATCH p3 = (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k)
RETURN k, p1, p2, p3 LIMIT 3000;


// -----------------------------------------------------------------------------
// Q10 — Multi-country reuse fingerprint. Five countries side-by-side, each
//       country expanded to its projects, their BGs and the materials reused.
//       Lets you visually compare DE / CH / NL / BE / UK reuse cultures.
//       [286 rows / 253 nodes]
// -----------------------------------------------------------------------------
MATCH (l:Land) WHERE l.id IN
  ['land_deutschland','land_schweiz','land_niederlande','land_belgien','land_vereinigtes_koenigreich']
MATCH path = (l)<-[:LIEGT_IN_LAND]-(p:Projekt)-[:HAT_BAUTEILGRUPPE]
             ->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 5000;


// -----------------------------------------------------------------------------
// Q11 — Norm hubs. Norms cited by ≥ 2 Bauteilgruppen — the load-bearing
//       standards. Each norm shown with its countries (GILT_IN_LAND), its
//       citing BGs, and the projects those BGs belong to.
//       [15 rows / 32 nodes]
// -----------------------------------------------------------------------------
MATCH (n:Norm)<-[:REFERENZIERT_NORM]-(bg:Bauteilgruppe)
WITH n, count(bg) AS bc WHERE bc >= 2
OPTIONAL MATCH p1 = (bg2:Bauteilgruppe)-[:REFERENZIERT_NORM]->(n)
OPTIONAL MATCH p2 = (n)-[:GILT_IN_LAND]->(l:Land)
OPTIONAL MATCH p3 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg2)
RETURN n, p1, p2, p3 LIMIT 2000;


// -----------------------------------------------------------------------------
// Q12 — Certification × projects + their reuse strategy.
//       Every sustainability-rating system as a hub, the projects that
//       certified under it, and what kind of reuse those projects performed.
//       [76 rows / 57 nodes]
// -----------------------------------------------------------------------------
MATCH (cert:ZertifizierungBewertungssystem)
OPTIONAL MATCH p1 = (cert)<-[:HAT_ZERTIFIZIERUNG]-(proj:Projekt)
OPTIONAL MATCH p2 = (proj)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
                    -[:HAT_WIEDERVERWENDUNGSART]->(wva:WiederverwendungsArt)
RETURN cert, p1, p2 LIMIT 3000;


// -----------------------------------------------------------------------------
// Q13 — Method × process phase × project. Design-time landscape.
//       Methodes (Form-Follows-Availability, Reuse-Assessment, Urban Mining,
//       Bauteilkatalogisierung, ...) connected through BGs to process phases
//       and projects. Shows which design methods own which project stage.
//       [949 rows / 288 nodes]
// -----------------------------------------------------------------------------
MATCH (m:Methode)
OPTIONAL MATCH p1 = (bg:Bauteilgruppe)-[:HAT_METHODE]->(m)
OPTIONAL MATCH p2 = (bg)-[:HAT_PROZESSPHASE]->(pp:Prozessphase)
OPTIONAL MATCH p3 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN m, p1, p2, p3 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q14 — Aufbereitungsverfahren tree + real-world usage.
//       The processing-method taxonomy (parent-child IST_UNTERVERFAHREN_VON)
//       overlaid with which BGs / projects actually used each method. Pure
//       vocab branches stay sparse; popular methods show big sub-clusters.
//       [398 rows / 337 nodes]
// -----------------------------------------------------------------------------
MATCH (av:Aufbereitungsverfahren)
OPTIONAL MATCH p1 = (av)-[:IST_UNTERVERFAHREN_VON]->(parent:Aufbereitungsverfahren)
OPTIONAL MATCH p2 = (bg:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(av)
OPTIONAL MATCH p3 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN av, p1, parent, p2, p3 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q15 — Era × pollutant × material × BG. Donor screening alert map.
//       For each construction era, which pollutants are typical, which
//       materials they sit in, and which existing BGs use those materials —
//       i.e. which BGs need that pollutant screened.
//       [1 112 rows / 255 nodes]
// -----------------------------------------------------------------------------
MATCH (era:BauwerkEra)
OPTIONAL MATCH p1 = (era)<-[:TYPISCH_BEI_ERA]-(s:Schadstoff)
OPTIONAL MATCH p2 = (s)-[:TYPISCH_BEI_MATERIAL]->(m:Material)
OPTIONAL MATCH p3 = (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
RETURN era, p1, s, p2, p3 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q16 — Reuse-quality clusters. Every pair of projects that share a
//       MatchingQualitaet axis value, plus each project's country. Clusters
//       reveal "reuse-style families" — interim-storage projects, same-site
//       projects, repurposing projects.
//       [3 981 rows / 96 nodes]
// -----------------------------------------------------------------------------
MATCH (p1:Projekt)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet)
      <-[:HAT_MATCHINGQUALITAET]-(p2:Projekt)
WHERE id(p1) < id(p2)
OPTIONAL MATCH (p1)-[:LIEGT_IN_LAND]->(l1:Land)
OPTIONAL MATCH (p2)-[:LIEGT_IN_LAND]->(l2:Land)
RETURN p1, mq, p2, l1, l2 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q17 — Reuse hub buildings. Bauwerke that supplied ≥ 3 component groups to
//       receiver projects. The donor-side gravity centres + the projects they
//       fed + their geographic location.
//       [304 rows / 246 nodes]
// -----------------------------------------------------------------------------
MATCH (bw:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)
WITH bw, count(bg) AS donor_count WHERE donor_count >= 3
MATCH path = (bw)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)<-[:HAT_BAUTEILGRUPPE]-(proj:Projekt)
OPTIONAL MATCH p2 = (bw)-[:LIEGT_IN_LAND|LIEGT_IN_STADT]->(loc)
RETURN bw, path, p2 LIMIT 3000;


// -----------------------------------------------------------------------------
// Q18 — Marktmodell ecosystem. Every sourcing-model node, the projects that
//       declared it dominant, the BGs tagged with it, and the materials those
//       BGs carry. Shows whether platforms / donations / same-site reuse map
//       to specific material families.
//       [5 000 rows / 157 nodes]
// -----------------------------------------------------------------------------
MATCH (mm:Marktmodell)
OPTIONAL MATCH p1 = (proj:Projekt)-[:HAT_DOMINANT_MARKTMODELL]->(mm)
OPTIONAL MATCH p2 = (bg:Bauteilgruppe)-[:HAT_MARKTMODELL]->(mm)
OPTIONAL MATCH p3 = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN mm, p1, p2, p3 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q19 — Hürde landscape. Every barrier node, its category, the BGs hitting
//       that barrier, the projects those BGs belong to. The "what holds reuse
//       back" map.
//       [974 rows / 418 nodes]
// -----------------------------------------------------------------------------
MATCH (h:Huerde)
OPTIONAL MATCH p1 = (h)-[:HAT_HUERDEKATEGORIE]->(hk:HuerdeKategorie)
OPTIONAL MATCH p2 = (bg:Bauteilgruppe)-[:HAT_HUERDE]->(h)
OPTIONAL MATCH p3 = (proj:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN h, p1, hk, p2, p3 LIMIT 5000;


// -----------------------------------------------------------------------------
// Q20 — Schadstoff full risk map. Each pollutant connected to the material(s),
//       era(s) and component-type(s) it is typical for, plus the BGs that use
//       the at-risk materials.
//       [2 846 rows / 284 nodes]
// -----------------------------------------------------------------------------
MATCH (s:Schadstoff)
OPTIONAL MATCH p1 = (s)-[:TYPISCH_BEI_MATERIAL]->(m:Material)
OPTIONAL MATCH p2 = (s)-[:TYPISCH_BEI_ERA]->(era:BauwerkEra)
OPTIONAL MATCH p3 = (s)-[:TYPISCH_BEI_BAUTEILTYP]->(bt:Bauteiltyp)
OPTIONAL MATCH p4 = (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
RETURN s, p1, p2, p3, p4 LIMIT 5000;
