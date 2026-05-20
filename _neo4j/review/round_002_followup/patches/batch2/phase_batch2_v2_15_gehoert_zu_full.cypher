// Phase 15 — GEHÖRT_ZU Person → Org edges (full set; supersedes Phase 5c template).
//
// The apply tool rejects rel types with umlauts. The live graph uses GEHÖRT_ZU
// (216 existing rels). Direct Cypher with MERGE is idempotent.
//
// PRECONDITION: Phases 5a + 13a applied (target Persons + Orgs exist).
//
// Run this once after Phase 13b. Re-running is safe (MERGE is idempotent).

// ============ Already-existing Persons → newly created Orgs ============

// hans_hammink → de_architekten_cie (already in graph)
MATCH (p {id:'hans_hammink'}), (o {id:'de_architekten_cie'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_hans_hammink__GEHÖRT_ZU__de_architekten_cie',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// lionel_billiet → rotor_asbl_vzw (which merges into Rotor in Phase 1b — re-write after merge)
MATCH (p {id:'lionel_billiet'}), (o {id:'Rotor'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_lionel_billiet__GEHÖRT_ZU__Rotor',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// sebastien_paulet → Rotor
MATCH (p {id:'sebastien_paulet'}), (o {id:'Rotor'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_sebastien_paulet__GEHÖRT_ZU__Rotor',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// michael_ghyoot → Rotor (FCRBE lead-partner contact at Rotor)
MATCH (p {id:'michael_ghyoot'}), (o {id:'Rotor'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_michael_ghyoot__GEHÖRT_ZU__Rotor',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// dominik_campanella → concular (CEO)
MATCH (p {id:'dominik_campanella'}), (o {id:'concular'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_dominik_campanella__GEHÖRT_ZU__concular',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// julius_schaeufele → concular
MATCH (p {id:'julius_schaeufele'}), (o {id:'concular'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_julius_schaeufele__GEHÖRT_ZU__concular',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// lenard_da_costa_kurek → concular
MATCH (p {id:'lenard_da_costa_kurek'}), (o {id:'concular'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_lenard_da_costa_kurek__GEHÖRT_ZU__concular',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// markus_meissner → baukarussell
MATCH (p {id:'markus_meissner'}), (o {id:'baukarussell'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_markus_meissner__GEHÖRT_ZU__baukarussell',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// thomas_romm → baukarussell
MATCH (p {id:'thomas_romm'}), (o {id:'baukarussell'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_thomas_romm__GEHÖRT_ZU__baukarussell',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// daniel_hoffmann → studio_trachsler_hoffmann (already in graph)
MATCH (p {id:'daniel_hoffmann'}), (o {id:'studio_trachsler_hoffmann'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_daniel_hoffmann__GEHÖRT_ZU__studio_trachsler_hoffmann',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// gian_trachsler → studio_trachsler_hoffmann
MATCH (p {id:'gian_trachsler'}), (o {id:'studio_trachsler_hoffmann'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_gian_trachsler__GEHÖRT_ZU__studio_trachsler_hoffmann',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// stefan_perez → perez_schmidlin_bauingenieure (new Phase 13)
MATCH (p {id:'stefan_perez'}), (o {id:'perez_schmidlin_bauingenieure'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_stefan_perez__GEHÖRT_ZU__perez_schmidlin_bauingenieure',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// michael_schmidlin → perez_schmidlin_bauingenieure
MATCH (p {id:'michael_schmidlin'}), (o {id:'perez_schmidlin_bauingenieure'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_michael_schmidlin__GEHÖRT_ZU__perez_schmidlin_bauingenieure',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// andreas_geser → andreas_geser_landschaftsarchitekten
MATCH (p {id:'andreas_geser'}), (o {id:'andreas_geser_landschaftsarchitekten'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_andreas_geser__GEHÖRT_ZU__andreas_geser_landschaftsarchitekten',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// martin_zeller → loeliger_strub_architektur
MATCH (p {id:'martin_zeller'}), (o {id:'loeliger_strub_architektur'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_martin_zeller__GEHÖRT_ZU__loeliger_strub_architektur',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// pascal_hentschel → zirkular_gmbh (canonical post-1b for zirkular_cirkla)
MATCH (p {id:'pascal_hentschel'}), (o {id:'zirkular_gmbh'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_pascal_hentschel__GEHÖRT_ZU__zirkular_gmbh',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// rebecca_brandmayer → zirkular_gmbh
MATCH (p {id:'rebecca_brandmayer'}), (o {id:'zirkular_gmbh'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_rebecca_brandmayer__GEHÖRT_ZU__zirkular_gmbh',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// laia_meier → zirkular_gmbh
MATCH (p {id:'laia_meier'}), (o {id:'zirkular_gmbh'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_laia_meier__GEHÖRT_ZU__zirkular_gmbh',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// mario_monotti → monotti_ingegneri
MATCH (p {id:'mario_monotti'}), (o {id:'monotti_ingegneri'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_mario_monotti__GEHÖRT_ZU__monotti_ingegneri',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// roger_keller → usus_la
MATCH (p {id:'roger_keller'}), (o {id:'usus_la'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_roger_keller__GEHÖRT_ZU__usus_la',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// ana_olalquiaga → parabase (already in graph)
MATCH (p {id:'ana_olalquiaga'}), (o {id:'parabase'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_ana_olalquiaga__GEHÖRT_ZU__parabase',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// will_shannon → granby_workshop_cic (also collaborator with assemble)
MATCH (p {id:'will_shannon'}), (o {id:'granby_workshop_cic'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_will_shannon__GEHÖRT_ZU__granby_workshop_cic',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// andreas_kretzer → hft_stuttgart (or arge_4k)
MATCH (p {id:'andreas_kretzer'}), (o {id:'hft_stuttgart'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_andreas_kretzer__GEHÖRT_ZU__hft_stuttgart',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// stefan_kroetsch → htwg_konstanz
MATCH (p {id:'stefan_kroetsch'}), (o {id:'htwg_konstanz'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_stefan_kroetsch__GEHÖRT_ZU__htwg_konstanz',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// roman_kreuzer → htwg_konstanz
MATCH (p {id:'roman_kreuzer'}), (o {id:'htwg_konstanz'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_roman_kreuzer__GEHÖRT_ZU__htwg_konstanz',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// thomas_stark → htwg_konstanz
MATCH (p {id:'thomas_stark'}), (o {id:'htwg_konstanz'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_thomas_stark__GEHÖRT_ZU__htwg_konstanz',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// michelle_schneider_zhaw → zhaw_ike
MATCH (p {id:'michelle_schneider_zhaw'}), (o {id:'zhaw_ike'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_michelle_schneider_zhaw__GEHÖRT_ZU__zhaw_ike',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// felix_dillmann → verein_re_win
MATCH (p {id:'felix_dillmann'}), (o {id:'verein_re_win'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_felix_dillmann__GEHÖRT_ZU__verein_re_win',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// madlen_kobi → university_of_fribourg
MATCH (p {id:'madlen_kobi'}), (o {id:'university_of_fribourg'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_madlen_kobi__GEHÖRT_ZU__university_of_fribourg',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// elena_sischarenco → university_of_fribourg
MATCH (p {id:'elena_sischarenco'}), (o {id:'university_of_fribourg'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_elena_sischarenco__GEHÖRT_ZU__university_of_fribourg',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// vanessa_feri → university_of_fribourg
MATCH (p {id:'vanessa_feri'}), (o {id:'university_of_fribourg'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_vanessa_feri__GEHÖRT_ZU__university_of_fribourg',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// adam_przywara → university_of_fribourg
MATCH (p {id:'adam_przywara'}), (o {id:'university_of_fribourg'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_adam_przywara__GEHÖRT_ZU__university_of_fribourg',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// rahel_jud → university_of_fribourg
MATCH (p {id:'rahel_jud'}), (o {id:'university_of_fribourg'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_rahel_jud__GEHÖRT_ZU__university_of_fribourg',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// orianne_scourzic → collectif_cancan
MATCH (p {id:'orianne_scourzic'}), (o {id:'collectif_cancan'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_orianne_scourzic__GEHÖRT_ZU__collectif_cancan',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// tiphaine_berthome → la_fabrique_de_bordeaux_metropole (AMO réemploi for La Fab)
MATCH (p {id:'tiphaine_berthome'}), (o {id:'la_fabrique_de_bordeaux_metropole'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_tiphaine_berthome__GEHÖRT_ZU__la_fabrique_de_bordeaux_metropole',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// valerie_jamet → la_fabrique_de_bordeaux_metropole
MATCH (p {id:'valerie_jamet'}), (o {id:'la_fabrique_de_bordeaux_metropole'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_valerie_jamet__GEHÖRT_ZU__la_fabrique_de_bordeaux_metropole',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// aurelie_heraut → la_fabrique_de_bordeaux_metropole
MATCH (p {id:'aurelie_heraut'}), (o {id:'la_fabrique_de_bordeaux_metropole'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_aurelie_heraut__GEHÖRT_ZU__la_fabrique_de_bordeaux_metropole',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// jerome_goze → la_fabrique_de_bordeaux_metropole
MATCH (p {id:'jerome_goze'}), (o {id:'la_fabrique_de_bordeaux_metropole'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_jerome_goze__GEHÖRT_ZU__la_fabrique_de_bordeaux_metropole',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// catherine_de_wolf → ETH Zürich (no eth_zurich Akteur in S27; flag for B6 follow-up)
// fabio_gramazio → ETH Zürich
// matthias_kohler → ETH Zürich
// — these 3 already linked to prog_mas_dfab via BETEILIGT_AN (Phase 9); GEHÖRT_ZU
//   to eth_zurich would require creating the Akteur first. Defer to a later patch.

// thornton_kay → salvo_ltd
MATCH (p {id:'thornton_kay'}), (o {id:'salvo_ltd'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_thornton_kay__GEHÖRT_ZU__salvo_ltd',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// duncan_baker_brown → university_of_brighton (existing alias 'Duncan Baker-Brown / BBM Sustainable Design')
MATCH (p {id:'duncan_baker_brown'}), (o {id:'university_of_brighton'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_duncan_baker_brown__GEHÖRT_ZU__university_of_brighton',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// hugo_topalov → bellastock
MATCH (p {id:'hugo_topalov'}), (o {id:'bellastock'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_hugo_topalov__GEHÖRT_ZU__bellastock',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';

// michel_baars → new_horizon_urban_mining
MATCH (p {id:'michel_baars'}), (o {id:'new_horizon_urban_mining'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_michel_baars__GEHÖRT_ZU__new_horizon_urban_mining',
              r.source = 'batch2_v2_followup_2026-05-20', r.evidence = 'BELEGT';


// === Verification ===
//
// MATCH ()-[r:`GEHÖRT_ZU`]->() WHERE r.source = 'batch2_v2_followup_2026-05-20'
// RETURN count(r);
// EXPECTED: ~35 (count of MERGE statements above that succeeded).
//
// MATCH (p:Akteur)-[:`GEHÖRT_ZU`]->(o:Akteur) RETURN count(*);
// EXPECTED: 216 (existing) + new (~35) = ~251.
