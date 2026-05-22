// Review-only Cypher draft. Only run after confirming anchor IDs and relationship semantics in mit-bestand.
// belegt claims are separated from wahrscheinlich/unsicher in MATERIAL_BAUTEILTYP_MATRIX.csv.


// backacia -> mat_holz evidence: https://opalis.eu/fr/fournisseurs/backacia
MATCH (a:Akteur {id:'backacia'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// backacia -> bt_ausbau evidence: https://backacia.com/collections/autres
MATCH (a:Akteur {id:'backacia'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// backacia -> bt_boden evidence: https://opalis.eu/fr/fournisseurs/backacia
MATCH (a:Akteur {id:'backacia'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// backacia -> bt_technik evidence: https://opalis.eu/fr/fournisseurs/backacia
MATCH (a:Akteur {id:'backacia'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// baticycle -> bt_boden evidence: https://baticycle.fr/materiaux-second-oeuvre/
MATCH (a:Akteur {id:'baticycle'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);



// baukarussell -> mat_beton evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(m:Material {id:'mat_beton'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// baukarussell -> mat_holz evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// baukarussell -> mat_keramik evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// baukarussell -> mat_naturstein evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(m:Material {id:'mat_naturstein'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// baukarussell -> mat_ziegel evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(m:Material {id:'mat_ziegel'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// baukarussell -> bt_ausbau evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_boden evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_dach evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_fenster evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_gelaender evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_gelaender'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_stuetze evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_stuetze'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_technik evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_traeger evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_traeger'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_treppe evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_treppe'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// baukarussell -> bt_tuer evidence: https://www.ak-umwelt.at/betrieb/?issue=2018-02
MATCH (a:Akteur {id:'baukarussell'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// bauteilboerse_bremen -> mat_glas evidence: https://www.bauteilboerse-bremen.de/katalog
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(m:Material {id:'mat_glas'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// bauteilboerse_bremen -> mat_holz evidence: https://www.bauteilboerse-bremen.de/katalog
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// bauteilboerse_bremen -> bt_ausbau evidence: https://www.bauteilboerse-bremen.de/katalog
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// bauteilboerse_bremen -> bt_boden evidence: https://www.bauteilboerse-bremen.de/katalog
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// bauteilboerse_bremen -> bt_fenster evidence: https://www.bauteilboerse-bremen.de/katalog
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// bauteilboerse_bremen -> bt_tuer evidence: https://www.bauteilboerse-bremen.de/katalog/tueren
MATCH (a:Akteur {id:'bauteilboerse_bremen'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);






// cycle_zero -> mat_daemmstoff evidence: https://www.constructionbtp.com/environnement/article/2025/05/22/152917/cycle-zero-des-materiaux-chantier-gratuits-aux-particuliers
MATCH (a:Akteur {id:'cycle_zero'}),(m:Material {id:'mat_daemmstoff'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// cycle_zero -> mat_holz evidence: https://www.iledefrance.fr/toutes-les-actualites/cycle-zero-la-revolution-numerique-anti-gaspillage-dans-le-btp
MATCH (a:Akteur {id:'cycle_zero'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// cycle_zero -> mat_keramik evidence: https://www.iledefrance.fr/toutes-les-actualites/cycle-zero-la-revolution-numerique-anti-gaspillage-dans-le-btp
MATCH (a:Akteur {id:'cycle_zero'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// cycle_zero -> bt_daemmung evidence: https://www.constructionbtp.com/environnement/article/2025/05/22/152917/cycle-zero-des-materiaux-chantier-gratuits-aux-particuliers
MATCH (a:Akteur {id:'cycle_zero'}),(b:Bauteiltyp {id:'bt_daemmung'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// cycle_zero -> bt_fenster evidence: https://www.iledefrance.fr/toutes-les-actualites/cycle-zero-la-revolution-numerique-anti-gaspillage-dans-le-btp
MATCH (a:Akteur {id:'cycle_zero'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// cycle_zero -> bt_technik evidence: https://www.iledefrance.fr/toutes-les-actualites/cycle-zero-la-revolution-numerique-anti-gaspillage-dans-le-btp
MATCH (a:Akteur {id:'cycle_zero'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// cycle_zero -> bt_tuer evidence: https://www.iledefrance.fr/toutes-les-actualites/cycle-zero-la-revolution-numerique-anti-gaspillage-dans-le-btp
MATCH (a:Akteur {id:'cycle_zero'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);


// gebruiktebouwmaterialen -> mat_aluminium evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(m:Material {id:'mat_aluminium'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// gebruiktebouwmaterialen -> mat_daemmstoff evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(m:Material {id:'mat_daemmstoff'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// gebruiktebouwmaterialen -> mat_holz evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// gebruiktebouwmaterialen -> mat_kunststoff evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(m:Material {id:'mat_kunststoff'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// gebruiktebouwmaterialen -> bt_ausbau evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// gebruiktebouwmaterialen -> bt_daemmung evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(b:Bauteiltyp {id:'bt_daemmung'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// gebruiktebouwmaterialen -> bt_fenster evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// gebruiktebouwmaterialen -> bt_tuer evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// gebruiktebouwmaterialen -> bt_wand evidence: https://gebruiktebouwmaterialen.com/
MATCH (a:Akteur {id:'gebruiktebouwmaterialen'}),(b:Bauteiltyp {id:'bt_wand'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// genbyg -> mat_glas evidence: https://genbyg.dk/
MATCH (a:Akteur {id:'genbyg'}),(m:Material {id:'mat_glas'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// genbyg -> bt_ausbau evidence: https://genbyg.dk/
MATCH (a:Akteur {id:'genbyg'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// genbyg -> bt_fenster evidence: https://genbyg.dk/
MATCH (a:Akteur {id:'genbyg'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// genbyg -> bt_technik evidence: https://genbyg.dk/
MATCH (a:Akteur {id:'genbyg'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// genbyg -> bt_tuer evidence: https://genbyg.dk/
MATCH (a:Akteur {id:'genbyg'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);



// loopfront -> bt_ausbau evidence: https://www.loopfront.com/
MATCH (a:Akteur {id:'loopfront'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// material_index -> mat_holz evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// material_index -> mat_stahl evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(m:Material {id:'mat_stahl'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// material_index -> mat_ziegel evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(m:Material {id:'mat_ziegel'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// material_index -> bt_ausbau evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// material_index -> bt_boden evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// material_index -> bt_technik evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// material_index -> bt_traeger evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_traeger'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// material_index -> bt_tuer evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// material_index -> bt_wand evidence: https://material-index.co.uk/
MATCH (a:Akteur {id:'material_index'}),(b:Bauteiltyp {id:'bt_wand'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);


// materialenbank_leuven_atelier_circuler -> mat_keramik evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// materialenbank_leuven_atelier_circuler -> mat_naturstein evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(m:Material {id:'mat_naturstein'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// materialenbank_leuven_atelier_circuler -> mat_stahl evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(m:Material {id:'mat_stahl'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// materialenbank_leuven_atelier_circuler -> bt_ausbau evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// materialenbank_leuven_atelier_circuler -> bt_dach evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// materialenbank_leuven_atelier_circuler -> bt_traeger evidence: https://ateliercirculer.be/materialenbank/
MATCH (a:Akteur {id:'materialenbank_leuven_atelier_circuler'}),(b:Bauteiltyp {id:'bt_traeger'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);



// r_place -> mat_beton evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(m:Material {id:'mat_beton'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// r_place -> mat_holz evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// r_place -> mat_naturstein evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(m:Material {id:'mat_naturstein'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// r_place -> mat_stahl evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(m:Material {id:'mat_stahl'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// r_place -> bt_ausbau evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_boden evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_dach evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_fenster evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_technik evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_traeger evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_traeger'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// r_place -> bt_tuer evidence: https://r-place.fr/
MATCH (a:Akteur {id:'r_place'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);



// reempro -> bt_ausbau evidence: https://www.reempro.com/marketplace/
MATCH (a:Akteur {id:'reempro'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// reempro -> bt_boden evidence: https://www.reempro.com/marketplace/
MATCH (a:Akteur {id:'reempro'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// reempro -> bt_dach evidence: https://www.reempro.com/marketplace/
MATCH (a:Akteur {id:'reempro'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// reempro -> bt_technik evidence: https://www.reempro.com/marketplace/
MATCH (a:Akteur {id:'reempro'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);



// rotordc -> mat_glas evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(m:Material {id:'mat_glas'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// rotordc -> mat_holz evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// rotordc -> mat_keramik evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// rotordc -> bt_ausbau evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// rotordc -> bt_boden evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// rotordc -> bt_fenster evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// rotordc -> bt_technik evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// rotordc -> bt_tuer evidence: https://rotordc.com/
MATCH (a:Akteur {id:'rotordc'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// salvoweb -> mat_naturstein evidence: https://www.salvoweb.com/
MATCH (a:Akteur {id:'salvoweb'}),(m:Material {id:'mat_naturstein'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// salvoweb -> mat_ziegel evidence: https://www.salvoweb.com/
MATCH (a:Akteur {id:'salvoweb'}),(m:Material {id:'mat_ziegel'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// salvoweb -> bt_ausbau evidence: https://www.salvoweb.com/
MATCH (a:Akteur {id:'salvoweb'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// salvoweb -> bt_boden evidence: https://www.salvoweb.com/
MATCH (a:Akteur {id:'salvoweb'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);


// skop_marketplace -> mat_daemmstoff evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(m:Material {id:'mat_daemmstoff'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// skop_marketplace -> mat_holz evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// skop_marketplace -> bt_ausbau evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// skop_marketplace -> bt_boden evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// skop_marketplace -> bt_daemmung evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(b:Bauteiltyp {id:'bt_daemmung'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// skop_marketplace -> bt_technik evidence: https://marketplace.skop.app/
MATCH (a:Akteur {id:'skop_marketplace'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// software_restado -> mat_beton evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(m:Material {id:'mat_beton'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// software_restado -> mat_holz evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// software_restado -> mat_naturstein evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(m:Material {id:'mat_naturstein'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// software_restado -> mat_ziegel evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(m:Material {id:'mat_ziegel'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// software_restado -> bt_ausbau evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_dach evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_fassade evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_fassade'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_fenster evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_technik evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_tuer evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// software_restado -> bt_wand evidence: https://restado.de/
MATCH (a:Akteur {id:'software_restado'}),(b:Bauteiltyp {id:'bt_wand'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// surplus_building_and_plumbing_materials -> mat_beton evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(m:Material {id:'mat_beton'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// surplus_building_and_plumbing_materials -> mat_holz evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// surplus_building_and_plumbing_materials -> mat_ziegel evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(m:Material {id:'mat_ziegel'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// surplus_building_and_plumbing_materials -> bt_ausbau evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// surplus_building_and_plumbing_materials -> bt_dach evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(b:Bauteiltyp {id:'bt_dach'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// surplus_building_and_plumbing_materials -> bt_fenster evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// surplus_building_and_plumbing_materials -> bt_technik evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// surplus_building_and_plumbing_materials -> bt_wand evidence: https://surplusbuildingsupplies.co.uk/building-materials.html
MATCH (a:Akteur {id:'surplus_building_and_plumbing_materials'}),(b:Bauteiltyp {id:'bt_wand'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// sustainability_yard -> mat_holz evidence: https://sustainabilityyard.com/
MATCH (a:Akteur {id:'sustainability_yard'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// sustainability_yard -> mat_keramik evidence: https://sustainabilityyard.com/
MATCH (a:Akteur {id:'sustainability_yard'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// sustainability_yard -> bt_ausbau evidence: https://sustainabilityyard.com/
MATCH (a:Akteur {id:'sustainability_yard'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// sustainability_yard -> bt_technik evidence: https://sustainabilityyard.com/
MATCH (a:Akteur {id:'sustainability_yard'}),(b:Bauteiltyp {id:'bt_technik'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);

// useagain_bauteilclick -> mat_holz evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(m:Material {id:'mat_holz'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// useagain_bauteilclick -> mat_keramik evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(m:Material {id:'mat_keramik'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// useagain_bauteilclick -> mat_stahl evidence: https://library-of-reuse.ch/pioneers/useagain
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(m:Material {id:'mat_stahl'}) MERGE (a)-[:NUTZT_MATERIAL {confidence:'belegt'}]->(m);
// useagain_bauteilclick -> bt_ausbau evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(b:Bauteiltyp {id:'bt_ausbau'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// useagain_bauteilclick -> bt_boden evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(b:Bauteiltyp {id:'bt_boden'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// useagain_bauteilclick -> bt_fenster evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(b:Bauteiltyp {id:'bt_fenster'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// useagain_bauteilclick -> bt_traeger evidence: https://library-of-reuse.ch/pioneers/useagain
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(b:Bauteiltyp {id:'bt_traeger'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);
// useagain_bauteilclick -> bt_tuer evidence: https://www.useagain.ch/de/
MATCH (a:Akteur {id:'useagain_bauteilclick'}),(b:Bauteiltyp {id:'bt_tuer'}) MERGE (a)-[:HAT_BAUTEILTYP {confidence:'belegt'}]->(b);


