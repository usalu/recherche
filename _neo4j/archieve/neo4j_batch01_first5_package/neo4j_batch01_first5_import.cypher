// Neo4j import script generated from first five transformed source files
// Run after creating optional uniqueness constraints on id properties.

CREATE CONSTRAINT akteur_id IF NOT EXISTS FOR (n:Akteur) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT akteurrolle_id IF NOT EXISTS FOR (n:Akteurrolle) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT akteurtyp_id IF NOT EXISTS FOR (n:Akteurtyp) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT aufbereitungsverfahren_id IF NOT EXISTS FOR (n:Aufbereitungsverfahren) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauobjektklasse_id IF NOT EXISTS FOR (n:Bauobjektklasse) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauobjektrolle_id IF NOT EXISTS FOR (n:Bauobjektrolle) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bausystem_id IF NOT EXISTS FOR (n:Bausystem) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauteilebene_id IF NOT EXISTS FOR (n:Bauteilebene) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauteilgruppe_id IF NOT EXISTS FOR (n:Bauteilgruppe) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauteiltyp_id IF NOT EXISTS FOR (n:Bauteiltyp) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauweise_id IF NOT EXISTS FOR (n:Bauweise) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT bauwerk_id IF NOT EXISTS FOR (n:Bauwerk) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT beschaffungsweg_id IF NOT EXISTS FOR (n:Beschaffungsweg) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT huerde_id IF NOT EXISTS FOR (n:Huerde) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT huerdekategorie_id IF NOT EXISTS FOR (n:HuerdeKategorie) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT land_id IF NOT EXISTS FOR (n:Land) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT leistungsanforderung_id IF NOT EXISTS FOR (n:Leistungsanforderung) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT logistik_id IF NOT EXISTS FOR (n:Logistik) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT material_id IF NOT EXISTS FOR (n:Material) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT materialgruppe_id IF NOT EXISTS FOR (n:Materialgruppe) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT methode_id IF NOT EXISTS FOR (n:Methode) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT norm_id IF NOT EXISTS FOR (n:Norm) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT nutzung_id IF NOT EXISTS FOR (n:Nutzung) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT projekt_id IF NOT EXISTS FOR (n:Projekt) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT prozessphase_id IF NOT EXISTS FOR (n:Prozessphase) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT pruefungnachweis_id IF NOT EXISTS FOR (n:PruefungNachweis) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT quelle_id IF NOT EXISTS FOR (n:Quelle) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT ressourcenquelle_id IF NOT EXISTS FOR (n:Ressourcenquelle) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT rueckbauverfahren_id IF NOT EXISTS FOR (n:Rueckbauverfahren) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT stadt_id IF NOT EXISTS FOR (n:Stadt) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT status_id IF NOT EXISTS FOR (n:Status) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT tragwerksprinzip_id IF NOT EXISTS FOR (n:Tragwerksprinzip) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT verbindungstechnik_id IF NOT EXISTS FOR (n:Verbindungstechnik) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT wiederverwendungsart_id IF NOT EXISTS FOR (n:WiederverwendungsArt) REQUIRE n.id IS UNIQUE;

MERGE (n:Quelle {id: "quelle_55_great_suffolk_street_london_md"})
SET n.name = "55_Great_Suffolk_Street_London.md", n.titel = "55 Great Suffolk Street, London", n.quelltyp = "case_markdown"
;
MERGE (n:Quelle {id: "quelle_association_house_groeditz_md"})
SET n.name = "Association_house_Groeditz.md", n.titel = "Association house, Gröditz", n.quelltyp = "case_markdown"
;
MERGE (n:Quelle {id: "quelle_association_house_plauen_md"})
SET n.name = "Association_house_Plauen.md", n.titel = "Association house, Plauen", n.quelltyp = "case_markdown"
;
MERGE (n:Quelle {id: "quelle_awm_muenster_circular_office_md"})
SET n.name = "AWM_Muenster_Circular_Office.md", n.titel = "AWM Münster, zirkulärer Büroausbau 3. OG", n.quelltyp = "case_markdown"
;
MERGE (n:Quelle {id: "quelle_bedzed_london_hackbridge_md"})
SET n.name = "BedZED_London_Hackbridge.md", n.titel = "BedZED, London / Hackbridge", n.quelltyp = "case_markdown"
;
MERGE (n:Projekt {id: "projekt_55_great_suffolk_street"})
SET n.name = "55 Great Suffolk Street", n.bewertung = 4, n.flaeche_m2 = 1412, n.jahr_beginn = 2021, n.jahr_fertigstellung_geplant = 2024, n.reused_steel_intended_t = 20.35, n.kern_stahl_gesamt_t = 20.98, n.kern_stahl_reuse_anteil_prozent = 97, n.co2_einsparung_t = 50, n.upfront_embodied_carbon_kgco2e_m2 = 386, n.raw_summary = "Retrofit / Conservation / Extension mit neuem außenliegendem Stahlkern aus wiederverwendetem Stahl.", n.note = "Bestandserhalt des denkmalgeschützten Lagerhauses nicht als Direct Reuse gezählt; Fertigstellungsstatus öffentlich unklar."
;
MERGE (n:Stadt {id: "stadt_london"})
SET n.name = "London"
;
MERGE (n:Land {id: "land_vereinigtes_koenigreich"})
SET n.name = "Vereinigtes Koenigreich"
;
MERGE (n:Status {id: "status_unklar_live"})
SET n.name = "Unklar_Live"
;
MERGE (n:Nutzung {id: "nutzung_arbeitsplatz"})
SET n.name = "Arbeitsplatz"
;
MERGE (n:Nutzung {id: "nutzung_buero"})
SET n.name = "Buero"
;
MERGE (n:Nutzung {id: "nutzung_retail"})
SET n.name = "Retail"
;
MERGE (n:Bauwerk {id: "bauwerk_55_great_suffolk_existing_warehouse"})
SET n.name = "Grade II Listed Victorian warehouse, 55 Great Suffolk Street", n.adresse = "55 Great Suffolk St, London SE1", n.raw_description = "denkmalgeschütztes viktorianisches Lagerhaus; Bestandserhalt ist nicht der Reuse-Score"
;
MERGE (n:Bauobjektklasse {id: "bauobjektklasse_gebaeude"})
SET n.name = "Gebaeude"
;
MERGE (n:Bauobjektrolle {id: "bauobjektrolle_bestandsobjekt"})
SET n.name = "Bestandsobjekt"
;
MERGE (n:Bauobjektrolle {id: "bauobjektrolle_empfaengerobjekt"})
SET n.name = "Empfaengerobjekt"
;
MERGE (n:Bauwerk {id: "bauwerk_55_great_suffolk_external_core"})
SET n.name = "Neuer externer Service- und Erschliessungskern", n.raw_description = "Neuer außenliegender Stahlkern mit WCs, Lift, Bike store, showers und step-free access"
;
MERGE (n:Bauobjektklasse {id: "bauobjektklasse_gebaeudeteil"})
SET n.name = "Gebaeudeteil"
;
MERGE (n:Nutzung {id: "nutzung_erschliessung"})
SET n.name = "Erschliessung"
;
MERGE (n:Bauwerk {id: "bauwerk_1_broadgate_donor"})
SET n.name = "1 Broadgate donor site", n.raw_description = "Donor site für einen Teil des wiederverwendeten Stahls"
;
MERGE (n:Bauobjektrolle {id: "bauobjektrolle_donorobjekt"})
SET n.name = "Donorobjekt"
;
MERGE (n:Status {id: "status_rueckbau_demontage"})
SET n.name = "Rueckbau_Demontage"
;
MERGE (n:Material {id: "material_baustahl"})
SET n.name = "Baustahl"
;
MERGE (n:Materialgruppe {id: "materialgruppe_metall"})
SET n.name = "Metall"
;
MERGE (n:Bauteilgruppe {id: "btg_55_steel_from_1_broadgate"})
SET n.name = "Wiederverwendete Stahlprofile aus 1 Broadgate", n.counts_as_direct_reuse = true, n.menge_t = 8.3, n.reuse_anteil_prozent = 43, n.alte_funktion = "Tragwerk eines donor building", n.neue_funktion = "Teil des neuen externen Kerntragwerks"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_traeger"})
SET n.name = "Traeger"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_stuetze"})
SET n.name = "Stuetze"
;
MERGE (n:Bauteilebene {id: "bauteilebene_tragwerk"})
SET n.name = "Tragwerk"
;
MERGE (n:Bauteilebene {id: "bauteilebene_raumstruktur"})
SET n.name = "Raumstruktur"
;
MERGE (n:WiederverwendungsArt {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
SET n.name = "Ex-situ Bauteilwiederverwendung"
;
MERGE (n:WiederverwendungsArt {id: "wiederverwendungsart_urban_mining"})
SET n.name = "Urban Mining"
;
MERGE (n:Status {id: "status_eingebaut"})
SET n.name = "Eingebaut"
;
MERGE (n:Tragwerksprinzip {id: "tragwerksprinzip_stahlrahmen"})
SET n.name = "Stahlrahmen"
;
MERGE (n:Bauweise {id: "bauweise_stahlbau"})
SET n.name = "Stahlbau"
;
MERGE (n:Methode {id: "methode_design_follows_availability"})
SET n.name = "Design follows availability"
;
MERGE (n:Prozessphase {id: "prozessphase_rueckbau"})
SET n.name = "Rueckbau"
;
MERGE (n:Prozessphase {id: "prozessphase_transport"})
SET n.name = "Transport"
;
MERGE (n:Prozessphase {id: "prozessphase_aufbereitung"})
SET n.name = "Aufbereitung"
;
MERGE (n:Prozessphase {id: "prozessphase_planung"})
SET n.name = "Planung"
;
MERGE (n:Prozessphase {id: "prozessphase_wiedereinbau"})
SET n.name = "Wiedereinbau"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_testing"})
SET n.name = "Testing"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_ce_marking"})
SET n.name = "CE Marking"
;
MERGE (n:Norm {id: "norm_en_1090"})
SET n.name = "EN 1090"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_tragfaehigkeit"})
SET n.name = "Tragfaehigkeit"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_schweissbarkeit"})
SET n.name = "Schweissbarkeit"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_nachweisbarkeit"})
SET n.name = "Nachweisbarkeit"
;
MERGE (n:Huerde {id: "huerde_profilverfuegbarkeit"})
SET n.name = "Profilverfuegbarkeit"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_technisch"})
SET n.name = "Technisch"
;
MERGE (n:Huerde {id: "huerde_donor_receiver_timing"})
SET n.name = "Donor-Receiver-Timing"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_logistisch"})
SET n.name = "Logistisch"
;
MERGE (n:Huerde {id: "huerde_zertifizierung"})
SET n.name = "Zertifizierung"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_rechtlich"})
SET n.name = "Rechtlich"
;
MERGE (n:Huerde {id: "huerde_services_koordination"})
SET n.name = "Services-Koordination"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_planerisch"})
SET n.name = "Planerisch"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_anbauteile_entfernen"})
SET n.name = "Anbauteile entfernen"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_loecher_fuellen"})
SET n.name = "Loecher fuellen"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_testen"})
SET n.name = "Testen"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_ce_markieren"})
SET n.name = "CE markieren"
;
MERGE (n:Rueckbauverfahren {id: "rueckbauverfahren_deconstruction_donor_site"})
SET n.name = "Deconstruction donor site"
;
MERGE (n:Rueckbauverfahren {id: "rueckbauverfahren_demolition_donor_site"})
SET n.name = "Demolition donor site"
;
MERGE (n:Beschaffungsweg {id: "beschaffungsweg_direktdeal_mit_rueckbauprojekt"})
SET n.name = "Direktdeal mit Rueckbauprojekt"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_donor_building"})
SET n.name = "Donor building"
;
MERGE (n:Logistik {id: "logistik_vorausbeschaffung"})
SET n.name = "Vorausbeschaffung"
;
MERGE (n:Bauteilgruppe {id: "btg_55_steel_from_cleveland_stock"})
SET n.name = "Wiederverwendete Stahlprofile aus Cleveland Stock", n.counts_as_direct_reuse = true, n.menge_t = 11.1, n.reuse_anteil_prozent = 57, n.alte_funktion = "reclaimed stock / surplus", n.neue_funktion = "Teil des neuen externen Kerntragwerks"
;
MERGE (n:WiederverwendungsArt {id: "wiederverwendungsart_reuse_stockholder_modell"})
SET n.name = "Reuse-Stockholder-Modell"
;
MERGE (n:Prozessphase {id: "prozessphase_lagerung"})
SET n.name = "Lagerung"
;
MERGE (n:Huerde {id: "huerde_marktliquiditaet"})
SET n.name = "Marktliquiditaet"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_wirtschaftlich"})
SET n.name = "Wirtschaftlich"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_restaurierung"})
SET n.name = "Restaurierung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_rezertifizierung"})
SET n.name = "Rezertifizierung"
;
MERGE (n:Beschaffungsweg {id: "beschaffungsweg_reuse_stockholder"})
SET n.name = "Reuse Stockholder"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_reclaimed_stockholder"})
SET n.name = "Reclaimed stockholder"
;
MERGE (n:Logistik {id: "logistik_lagerung_bei_stockholder"})
SET n.name = "Lagerung bei Stockholder"
;
MERGE (n:Akteur {id: "akteur_fabrix"})
SET n.name = "Fabrix", n.raw_name = "Fabrix"
;
MERGE (n:Akteurrolle {id: "akteurrolle_bauherr_auftraggeber"})
SET n.name = "Bauherr_Auftraggeber"
;
MERGE (n:Akteurrolle {id: "akteurrolle_developer"})
SET n.name = "Developer"
;
MERGE (n:Akteurtyp {id: "akteurtyp_unternehmen"})
SET n.name = "Unternehmen"
;
MERGE (n:Akteur {id: "akteur_hawkins_brown"})
SET n.name = "Hawkins\\Brown", n.raw_name = "Hawkins\\Brown"
;
MERGE (n:Akteurrolle {id: "akteurrolle_architektur"})
SET n.name = "Architektur"
;
MERGE (n:Akteurtyp {id: "akteurtyp_planungsbuero"})
SET n.name = "Planungsbuero"
;
MERGE (n:Akteur {id: "akteur_symmetrys"})
SET n.name = "Symmetrys", n.raw_name = "Symmetrys"
;
MERGE (n:Akteurrolle {id: "akteurrolle_tragwerksplanung"})
SET n.name = "Tragwerksplanung"
;
MERGE (n:Akteurtyp {id: "akteurtyp_ingenieurbuero"})
SET n.name = "Ingenieurbuero"
;
MERGE (n:Akteur {id: "akteur_akt_ii"})
SET n.name = "AKT II", n.raw_name = "AKT II"
;
MERGE (n:Akteurrolle {id: "akteurrolle_engineering_consultant"})
SET n.name = "Engineering_Consultant"
;
MERGE (n:Akteurrolle {id: "akteurrolle_reuse_beratung"})
SET n.name = "Reuse_Beratung"
;
MERGE (n:Akteur {id: "akteur_cbre"})
SET n.name = "CBRE", n.raw_name = "CBRE"
;
MERGE (n:Akteurrolle {id: "akteurrolle_nachhaltigkeitsberatung"})
SET n.name = "Nachhaltigkeitsberatung"
;
MERGE (n:Akteurrolle {id: "akteurrolle_embodied_carbon_beratung"})
SET n.name = "Embodied_Carbon_Beratung"
;
MERGE (n:Akteur {id: "akteur_opera"})
SET n.name = "Opera", n.raw_name = "Opera"
;
MERGE (n:Akteurrolle {id: "akteurrolle_projektmanagement"})
SET n.name = "Projektmanagement"
;
MERGE (n:Akteur {id: "akteur_gardiner_theobald"})
SET n.name = "Gardiner & Theobald", n.raw_name = "Gardiner & Theobald"
;
MERGE (n:Akteurrolle {id: "akteurrolle_reuse_beschaffung"})
SET n.name = "Reuse_Beschaffung"
;
MERGE (n:Akteur {id: "akteur_cantillon"})
SET n.name = "Cantillon", n.raw_name = "Cantillon"
;
MERGE (n:Akteurrolle {id: "akteurrolle_rueckbau_demontage"})
SET n.name = "Rueckbau_Demontage"
;
MERGE (n:Akteurtyp {id: "akteurtyp_rueckbauunternehmen"})
SET n.name = "Rueckbauunternehmen"
;
MERGE (n:Akteur {id: "akteur_cleveland_steel_and_tubes"})
SET n.name = "Cleveland Steel and Tubes", n.raw_name = "Cleveland Steel and Tubes"
;
MERGE (n:Akteurrolle {id: "akteurrolle_materiallieferant"})
SET n.name = "Materiallieferant"
;
MERGE (n:Akteurrolle {id: "akteurrolle_reuse_stockholder"})
SET n.name = "Reuse_Stockholder"
;
MERGE (n:Akteurrolle {id: "akteurrolle_aufbereitung_pruefung"})
SET n.name = "Aufbereitung_Pruefung"
;
MERGE (n:Akteurtyp {id: "akteurtyp_materialhaendler"})
SET n.name = "Materialhaendler"
;
MERGE (n:Projekt {id: "projekt_association_house_groeditz"})
SET n.name = "Association house, Gröditz", n.bewertung = 4, n.jahr_fertigstellung = 2007, n.anzahl_wiederverwendete_bauteile = 438, n.transportdistanz_km = 2.5, n.raw_summary = "Neubau eines Sport-/Vereinshauses mit wiederverwendeten Betonfertigteilen aus mindestens zwei Spendergebäuden.", n.note = "Architekt, Tragwerksplaner und Bauherr öffentlich nicht belastbar gefunden."
;
MERGE (n:Stadt {id: "stadt_groeditz"})
SET n.name = "Groeditz"
;
MERGE (n:Land {id: "land_deutschland"})
SET n.name = "Deutschland"
;
MERGE (n:Status {id: "status_gebaut"})
SET n.name = "Gebaut"
;
MERGE (n:Nutzung {id: "nutzung_sport_verein"})
SET n.name = "Sport_Verein"
;
MERGE (n:Bauwerk {id: "bauwerk_groeditz_association_house"})
SET n.name = "Sport-/Vereinshaus Gröditz"
;
MERGE (n:Bauwerk {id: "bauwerk_groeditz_donor_school_dresden_type"})
SET n.name = "Spendergebäude Schule Typ Dresden", n.raw_description = "Spendergebäude für 279 Betonfertigteile; genaue Adresse unbekannt"
;
MERGE (n:Nutzung {id: "nutzung_schule"})
SET n.name = "Schule"
;
MERGE (n:Bauwerk {id: "bauwerk_groeditz_donor_wbs70"})
SET n.name = "Spendergebäude WBS70", n.raw_description = "Weiteres Spendergebäude für 159 WBS70-Paneele; genaue Nutzung und Adresse unbekannt"
;
MERGE (n:Material {id: "material_stahlbetonfertigteil"})
SET n.name = "Stahlbetonfertigteil"
;
MERGE (n:Materialgruppe {id: "materialgruppe_mineralisch"})
SET n.name = "Mineralisch"
;
MERGE (n:Bauteilgruppe {id: "btg_groeditz_dresden_type_precast_parts"})
SET n.name = "Betonfertigteile aus Schule Typ Dresden", n.counts_as_direct_reuse = true, n.anzahl = 279, n.alte_funktion = "Außenwand, Innenwand, Rahmen, Decke, Sockel/Plinthe, Treppe in Schule Typ Dresden", n.neue_funktion = "Wand, Decke, Fassade, Raumstruktur und Erschließung im Sport-/Vereinshaus"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_wand"})
SET n.name = "Wand"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_decke"})
SET n.name = "Decke"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_treppe"})
SET n.name = "Treppe"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_fassade"})
SET n.name = "Fassade"
;
MERGE (n:Bauteilebene {id: "bauteilebene_huelle"})
SET n.name = "Huelle"
;
MERGE (n:Tragwerksprinzip {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
SET n.name = "Fertigteil-Wand-Deckensystem"
;
MERGE (n:Bauweise {id: "bauweise_betonfertigteilbau"})
SET n.name = "Betonfertigteilbau"
;
MERGE (n:Bausystem {id: "bausystem_dresden_typ"})
SET n.name = "Dresden-Typ"
;
MERGE (n:Methode {id: "methode_bauteilinventar"})
SET n.name = "Bauteilinventar"
;
MERGE (n:Methode {id: "methode_bauteilgerechte_planung"})
SET n.name = "Bauteilgerechte Planung"
;
MERGE (n:Prozessphase {id: "prozessphase_bauteilinventar"})
SET n.name = "Bauteilinventar"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_brandschutz"})
SET n.name = "Brandschutz"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_schallschutz"})
SET n.name = "Schallschutz"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_feuchteschutz"})
SET n.name = "Feuchteschutz"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_waermeschutz"})
SET n.name = "Waermeschutz"
;
MERGE (n:Huerde {id: "huerde_systemmix"})
SET n.name = "Systemmix"
;
MERGE (n:Huerde {id: "huerde_hoehenausgleich"})
SET n.name = "Hoehenausgleich"
;
MERGE (n:Huerde {id: "huerde_anschlussdetails"})
SET n.name = "Anschlussdetails"
;
MERGE (n:Huerde {id: "huerde_tragwerksnachweis"})
SET n.name = "Tragwerksnachweis"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_ziegelschicht_zum_hoehenausgleich"})
SET n.name = "Ziegelschicht zum Hoehenausgleich"
;
MERGE (n:Rueckbauverfahren {id: "rueckbauverfahren_selektiver_rueckbau"})
SET n.name = "Selektiver Rueckbau"
;
MERGE (n:Rueckbauverfahren {id: "rueckbauverfahren_demontage"})
SET n.name = "Demontage"
;
MERGE (n:Logistik {id: "logistik_kurze_lokale_transportdistanz"})
SET n.name = "Kurze lokale Transportdistanz"
;
MERGE (n:Bauteilgruppe {id: "btg_groeditz_wbs70_panels"})
SET n.name = "WBS70-Paneele aus weiterem Spendergebäude", n.counts_as_direct_reuse = true, n.anzahl = 159, n.alte_funktion = "Wand/Decke unbekannt im WBS70-Gebäude", n.neue_funktion = "Wand, Decke oder Fassade im Sport-/Vereinshaus"
;
MERGE (n:Bausystem {id: "bausystem_wbs70"})
SET n.name = "WBS70"
;
MERGE (n:Huerde {id: "huerde_logistik_schwerer_bauteile"})
SET n.name = "Logistik schwerer Bauteile"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_ueberlappende_fassaden_fertigteile"})
SET n.name = "Ueberlappende Fassaden-Fertigteile"
;
MERGE (n:Projekt {id: "projekt_association_house_plauen"})
SET n.name = "Association house, Plauen", n.bewertung = 4, n.jahr_fertigstellung = 2007, n.anzahl_wiederverwendete_bauteile = 189, n.transportdistanz_km = 7, n.raw_summary = "Neubau eines Sport-/Vereinshauses aus wiederverwendeten Stahlbetonfertigteilen des Systems IW73/6.", n.note = "Architekt, Tragwerksplaner und Bauherr öffentlich nicht belastbar gefunden; Prüfberichte nicht öffentlich gefunden."
;
MERGE (n:Stadt {id: "stadt_plauen"})
SET n.name = "Plauen"
;
MERGE (n:Bauwerk {id: "bauwerk_plauen_association_house"})
SET n.name = "Sport-/Vereinshaus Plauen"
;
MERGE (n:Bauwerk {id: "bauwerk_plauen_donor_iw73_6"})
SET n.name = "Spendergebäude IW73/6-Wohnungsbau", n.raw_description = "Herkunft der wiederverwendeten Fertigteile; industrieller Wohnungsbau / mass housing"
;
MERGE (n:Nutzung {id: "nutzung_wohnen"})
SET n.name = "Wohnen"
;
MERGE (n:Bauteilgruppe {id: "btg_plauen_floor_ceiling_slabs"})
SET n.name = "Decken-/Bodenplatten IW73/6", n.counts_as_direct_reuse = true, n.anzahl = 145, n.alte_funktion = "Decke/Boden im IW73/6-Wohnungsbau", n.neue_funktion = "Decke/Boden oder tragendes Bauteil im Vereinshaus"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_boden"})
SET n.name = "Boden"
;
MERGE (n:Bausystem {id: "bausystem_iw73_6"})
SET n.name = "IW73/6"
;
MERGE (n:Methode {id: "methode_bauteilidentifikation"})
SET n.name = "Bauteilidentifikation"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_gebrauchstauglichkeit"})
SET n.name = "Gebrauchstauglichkeit"
;
MERGE (n:Huerde {id: "huerde_bauteilgeometrie_rasterbindung"})
SET n.name = "Bauteilgeometrie Rasterbindung"
;
MERGE (n:Huerde {id: "huerde_nachweisfaehigkeit"})
SET n.name = "Nachweisfaehigkeit"
;
MERGE (n:Huerde {id: "huerde_fehlende_primaerdaten"})
SET n.name = "Fehlende Primaerdaten"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_daten_evidenz"})
SET n.name = "Daten_Evidenz"
;
MERGE (n:Bauteilgruppe {id: "btg_plauen_exterior_wall_elements"})
SET n.name = "Außenwandelemente IW73/6", n.counts_as_direct_reuse = true, n.anzahl = 19, n.alte_funktion = "Außenwand im IW73/6-Wohnungsbau", n.neue_funktion = "Wand/Hülle im Vereinshaus"
;
MERGE (n:Huerde {id: "huerde_waermebruecken"})
SET n.name = "Waermebruecken"
;
MERGE (n:Bauteilgruppe {id: "btg_plauen_interior_wall_elements"})
SET n.name = "Innenwandelemente IW73/6", n.counts_as_direct_reuse = true, n.anzahl = 14, n.alte_funktion = "Innenwand im IW73/6-Wohnungsbau", n.neue_funktion = "Innen-/Tragwand im Vereinshaus"
;
MERGE (n:Bauteilgruppe {id: "btg_plauen_basement_wall_elements"})
SET n.name = "Kellerwandelemente IW73/6", n.counts_as_direct_reuse = true, n.anzahl = 11, n.alte_funktion = "Kellerwand im IW73/6-Wohnungsbau", n.neue_funktion = "Wand/Sockel/Kellerbereich im Vereinshaus"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_dauerhaftigkeit"})
SET n.name = "Dauerhaftigkeit"
;
MERGE (n:Huerde {id: "huerde_feuchteschutz"})
SET n.name = "Feuchteschutz"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_umwelt_gesundheit"})
SET n.name = "Umwelt_Gesundheit"
;
MERGE (n:Projekt {id: "projekt_awm_muenster_circular_office"})
SET n.name = "AWM Münster, zirkulärer Büroausbau 3. OG", n.bewertung = 2, n.jahr_fertigstellung = 2023, n.flaeche_m2 = 250, n.wiedergewonnene_materialien_t = 6.9, n.abfallvermeidung_t = 6.9, n.co2_einsparung_t = 13.32, n.co2_reduktion_prozent = 82, n.c2c_oder_reuse_produktanteil_prozent = 95.6, n.raw_summary = "Zirkulärer Innenausbau des dritten Obergeschosses mit fest eingebauten Reuse-Elementen.", n.note = "Vergleichsfall/Anhang: kleiner Innenausbau; lose Möbel und Bestandserhalt nicht als Direct Reuse gezählt."
;
MERGE (n:Stadt {id: "stadt_muenster"})
SET n.name = "Muenster"
;
MERGE (n:Nutzung {id: "nutzung_verwaltung"})
SET n.name = "Verwaltung"
;
MERGE (n:Nutzung {id: "nutzung_workshop"})
SET n.name = "Workshop"
;
MERGE (n:Nutzung {id: "nutzung_besprechung"})
SET n.name = "Besprechung"
;
MERGE (n:Nutzung {id: "nutzung_kueche"})
SET n.name = "Kueche"
;
MERGE (n:Bauwerk {id: "bauwerk_awm_muenster_3og"})
SET n.name = "AWM Verwaltungsgebäude, 3. Obergeschoss Rösnerstraße", n.raw_description = "Umgebautes drittes Obergeschoss im alten Verwaltungsgebäude der Abfallwirtschaftsbetriebe Münster"
;
MERGE (n:Material {id: "material_glas"})
SET n.name = "Glas"
;
MERGE (n:Material {id: "material_metall"})
SET n.name = "Metall"
;
MERGE (n:Material {id: "material_holz"})
SET n.name = "Holz"
;
MERGE (n:Materialgruppe {id: "materialgruppe_biobasiert"})
SET n.name = "Biobasiert"
;
MERGE (n:Material {id: "material_mischmaterial_innenausbau"})
SET n.name = "Mischmaterial Innenausbau"
;
MERGE (n:Materialgruppe {id: "materialgruppe_gemischt"})
SET n.name = "Gemischt"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_glass_partitions_doors"})
SET n.name = "Glastrennwände und Türen aus Behrensbau Düsseldorf", n.counts_as_direct_reuse = true, n.co2_einsparung_t = 4.39, n.alte_funktion = "Büro-/Gebäudetrennwände", n.neue_funktion = "Trennwände und Türen im AWM-Office"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_tuer"})
SET n.name = "Tuer"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_ausbau"})
SET n.name = "Ausbau"
;
MERGE (n:Bauteilebene {id: "bauteilebene_innenausbau"})
SET n.name = "Innenausbau"
;
MERGE (n:WiederverwendungsArt {id: "wiederverwendungsart_fester_innenausbau"})
SET n.name = "Fester Innenausbau"
;
MERGE (n:Methode {id: "methode_reuse_first"})
SET n.name = "ReUse first"
;
MERGE (n:Prozessphase {id: "prozessphase_monitoring"})
SET n.name = "Monitoring"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_sicherheit"})
SET n.name = "Sicherheit"
;
MERGE (n:Huerde {id: "huerde_passung_zustand"})
SET n.name = "Passung Zustand"
;
MERGE (n:Huerde {id: "huerde_brandschutz_nicht_oeffentlich"})
SET n.name = "Brandschutz nicht oeffentlich"
;
MERGE (n:Huerde {id: "huerde_interior_grenzfall"})
SET n.name = "Interior Grenzfall"
;
MERGE (n:Beschaffungsweg {id: "beschaffungsweg_concular_materialplattform"})
SET n.name = "Concular Materialplattform"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_behrensbau_dusseldorf"})
SET n.name = "Behrensbau Düsseldorf"
;
MERGE (n:Logistik {id: "logistik_urban_mining_aus_oeffentlichen_gebaeuden"})
SET n.name = "Urban Mining aus oeffentlichen Gebaeuden"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_wc_partitions"})
SET n.name = "Reuse-WC-Trennwände aus Behrensbau Düsseldorf", n.counts_as_direct_reuse = true, n.alte_funktion = "Sanitärtrennwand", n.neue_funktion = "WC-Trennwand"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_hygiene"})
SET n.name = "Hygiene"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_stabilitaet"})
SET n.name = "Stabilitaet"
;
MERGE (n:Huerde {id: "huerde_hygiene_feuchte"})
SET n.name = "Hygiene Feuchte"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_cable_trays_shelves"})
SET n.name = "Kabeltrassen als Regale", n.counts_as_direct_reuse = true, n.alte_funktion = "Kabeltrasse", n.neue_funktion = "Regal / Ablage"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_technik"})
SET n.name = "Technik"
;
MERGE (n:Bauteilebene {id: "bauteilebene_technische_ausstattung"})
SET n.name = "Technische_Ausstattung"
;
MERGE (n:WiederverwendungsArt {id: "wiederverwendungsart_funktionswechsel"})
SET n.name = "Funktionswechsel"
;
MERGE (n:Methode {id: "methode_upcycling"})
SET n.name = "Upcycling"
;
MERGE (n:Huerde {id: "huerde_neue_lastfunktion"})
SET n.name = "Neue Lastfunktion"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_umnutzung"})
SET n.name = "Umnutzung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_3d_gedruckte_halterungen"})
SET n.name = "3D-gedruckte Halterungen"
;
MERGE (n:Verbindungstechnik {id: "verbindungstechnik_spezialhalterungen"})
SET n.name = "Spezialhalterungen"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_cable_trays_led_lighting"})
SET n.name = "Kabeltrassen und ReUse-LED-Leuchten als Allgemeinbeleuchtung", n.counts_as_direct_reuse = true, n.alte_funktion = "Kabeltrasse / Leuchte", n.neue_funktion = "Allgemeinbeleuchtung"
;
MERGE (n:Methode {id: "methode_reaktivierung"})
SET n.name = "Reaktivierung"
;
MERGE (n:Methode {id: "methode_aufputzfuhrung"})
SET n.name = "Aufputzführung"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_elektrosicherheit"})
SET n.name = "Elektrosicherheit"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_wartbarkeit"})
SET n.name = "Wartbarkeit"
;
MERGE (n:Huerde {id: "huerde_elektrosicherheit_tga"})
SET n.name = "Elektrosicherheit TGA"
;
MERGE (n:Huerde {id: "huerde_technische_reaktivierung"})
SET n.name = "Technische Reaktivierung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_reaktivierung"})
SET n.name = "Reaktivierung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_montage"})
SET n.name = "Montage"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_chair_parts_wall_cladding"})
SET n.name = "Wandverkleidung aus alten Schul- und Theaterstühlen", n.counts_as_direct_reuse = true, n.anzahl_min = 500, n.alte_funktion = "Möbel / Stuhlteile", n.neue_funktion = "feste Wandverkleidung"
;
MERGE (n:Methode {id: "methode_spuren_als_gestaltung"})
SET n.name = "Spuren als Gestaltung"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_oberflaeche"})
SET n.name = "Oberflaeche"
;
MERGE (n:Huerde {id: "huerde_akzeptanz_gebrauchsspuren"})
SET n.name = "Akzeptanz Gebrauchsspuren"
;
MERGE (n:HuerdeKategorie {id: "huerdekategorie_sozial_organisatorisch"})
SET n.name = "Sozial_Organisatorisch"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_demontage"})
SET n.name = "Demontage"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_zuschnitt"})
SET n.name = "Zuschnitt"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_wandmontage"})
SET n.name = "Wandmontage"
;
MERGE (n:Bauteilgruppe {id: "btg_awm_reused_wood_built_ins"})
SET n.name = "Wiederverwendetes Holz für feste Einbauten", n.counts_as_direct_reuse = true, n.alte_funktion = "Deckenkonstruktion / Ladenbauholz", n.neue_funktion = "Sideboard, Küche, Wand-/Unterkonstruktion, feste Einbauten"
;
MERGE (n:Huerde {id: "huerde_herkunft_sortierung"})
SET n.name = "Herkunft Sortierung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_rueckbau"})
SET n.name = "Rueckbau"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_tischlerische_aufbereitung"})
SET n.name = "Tischlerische Aufbereitung"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_deckenkonstruktion_supermarkt"})
SET n.name = "Deckenkonstruktion Supermarkt"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_discounter_aufloesung"})
SET n.name = "Discounter-Aufloesung"
;
MERGE (n:Akteur {id: "akteur_awm_muenster"})
SET n.name = "Abfallwirtschaftsbetriebe Münster", n.raw_name = "Abfallwirtschaftsbetriebe Münster"
;
MERGE (n:Akteurrolle {id: "akteurrolle_nutzer"})
SET n.name = "Nutzer"
;
MERGE (n:Akteurtyp {id: "akteurtyp_oeffentliche_institution"})
SET n.name = "Oeffentliche_Institution"
;
MERGE (n:Akteur {id: "akteur_urselmann_interior"})
SET n.name = "urselmann interior", n.raw_name = "urselmann interior"
;
MERGE (n:Akteurrolle {id: "akteurrolle_innenarchitektur"})
SET n.name = "Innenarchitektur"
;
MERGE (n:Akteurrolle {id: "akteurrolle_design_build"})
SET n.name = "Design_Build"
;
MERGE (n:Akteur {id: "akteur_concular"})
SET n.name = "Concular", n.raw_name = "Concular"
;
MERGE (n:Akteurrolle {id: "akteurrolle_materialplattform"})
SET n.name = "Materialplattform"
;
MERGE (n:Akteurrolle {id: "akteurrolle_oekobilanzierung"})
SET n.name = "Oekobilanzierung"
;
MERGE (n:Akteurtyp {id: "akteurtyp_materialplattform"})
SET n.name = "Materialplattform"
;
MERGE (n:Akteur {id: "akteur_petra_jablonicka"})
SET n.name = "Petra Jablonická", n.raw_name = "Petra Jablonická"
;
MERGE (n:Akteurtyp {id: "akteurtyp_person"})
SET n.name = "Person"
;
MERGE (n:Akteur {id: "akteur_sven_urselmann"})
SET n.name = "Sven Urselmann", n.raw_name = "Sven Urselmann"
;
MERGE (n:Akteurrolle {id: "akteurrolle_projektleitung"})
SET n.name = "Projektleitung"
;
MERGE (n:Projekt {id: "projekt_bedzed"})
SET n.name = "BedZED / Beddington Zero Energy Development", n.bewertung = 5, n.jahr_beginn = 2000, n.jahr_fertigstellung = 2002, n.wohnungen_anzahl = 82, n.arbeitsflaeche_m2_min = 1405, n.arbeitsflaeche_m2_max = 2500, n.wiederverwendeter_struktureller_stahl_t = 98, n.tragender_stahl_reuse_anteil_prozent = 95, n.reclaimed_recycled_materials_t = 3404, n.reclaimed_recycled_anteil_gewicht_prozent = 15, n.transport_co2_einsparung_t = 120, n.raw_summary = "Gemischt genutztes Ökoquartier mit tragender Stahlwiederverwendung und weiteren festen Reuse-Bauteilen.", n.note = "Bewertung fokussiert Direct Reuse, nicht allgemeine Energie-/Recyclingstrategie."
;
MERGE (n:Nutzung {id: "nutzung_arbeiten"})
SET n.name = "Arbeiten"
;
MERGE (n:Nutzung {id: "nutzung_gemeinschaftsnutzung"})
SET n.name = "Gemeinschaftsnutzung"
;
MERGE (n:Bauwerk {id: "bauwerk_bedzed_quarter"})
SET n.name = "BedZED Wohn- und Arbeitsquartier", n.raw_description = "Gemischt genutztes Quartier in Hackbridge/Wallington, London Borough of Sutton"
;
MERGE (n:Bauobjektklasse {id: "bauobjektklasse_quartier_areal"})
SET n.name = "Quartier_Areal"
;
MERGE (n:Material {id: "material_naturstein_betonstein"})
SET n.name = "Naturstein_Betonstein"
;
MERGE (n:Bauteilgruppe {id: "btg_bedzed_reclaimed_structural_steel"})
SET n.name = "Wiederverwendete Stahlprofile / Stahlrahmen", n.counts_as_direct_reuse = true, n.menge_t = 98, n.reuse_anteil_prozent = 95, n.alte_funktion = "Tragende Stahlbauteile in früheren Gebäuden", n.neue_funktion = "Tragende Stahlrahmen, vor allem Workspaces"
;
MERGE (n:Methode {id: "methode_flexible_querschnittsspezifikation"})
SET n.name = "Flexible Querschnittsspezifikation"
;
MERGE (n:Prozessphase {id: "prozessphase_bestandsaufnahme"})
SET n.name = "Bestandsaufnahme"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_sichtpruefung"})
SET n.name = "Sichtpruefung"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_herstellungsdatum"})
SET n.name = "Herstellungsdatum"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_materialzustand"})
SET n.name = "Materialzustand"
;
MERGE (n:PruefungNachweis {id: "pruefungnachweis_fabrikationseignung"})
SET n.name = "Fabrikationseignung"
;
MERGE (n:Norm {id: "norm_historic_sections_book"})
SET n.name = "Historic Sections Book"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_korrosionsschutz"})
SET n.name = "Korrosionsschutz"
;
MERGE (n:Huerde {id: "huerde_passende_stahlprofile_schwer_verfuegbar"})
SET n.name = "Passende Stahlprofile schwer verfuegbar"
;
MERGE (n:Huerde {id: "huerde_qualitaetsnachweis_historischer_profile"})
SET n.name = "Qualitaetsnachweis historischer Profile"
;
MERGE (n:Huerde {id: "huerde_zusatzaufbereitung"})
SET n.name = "Zusatzaufbereitung"
;
MERGE (n:Huerde {id: "huerde_gebogene_profile_nicht_reused"})
SET n.name = "Gebogene Profile nicht reused"
;
MERGE (n:Huerde {id: "huerde_lagerbedarf"})
SET n.name = "Lagerbedarf"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_sandstrahlen"})
SET n.name = "Sandstrahlen"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_fertigung"})
SET n.name = "Fertigung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_lackierung"})
SET n.name = "Lackierung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_zinkreiche_beschichtung"})
SET n.name = "Zinkreiche Beschichtung"
;
MERGE (n:Beschaffungsweg {id: "beschaffungsweg_aktive_materialsuche"})
SET n.name = "Aktive Materialsuche"
;
MERGE (n:Beschaffungsweg {id: "beschaffungsweg_free_issue_material"})
SET n.name = "Free-Issue-Material"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_lokale_abbruchstandorte"})
SET n.name = "Lokale Abbruchstandorte"
;
MERGE (n:Ressourcenquelle {id: "ressourcenquelle_brighton_railway_station"})
SET n.name = "Brighton Railway Station"
;
MERGE (n:Logistik {id: "logistik_35_mile_zielradius"})
SET n.name = "35-mile-Zielradius"
;
MERGE (n:Logistik {id: "logistik_lange_vorlaufzeit"})
SET n.name = "Lange Vorlaufzeit"
;
MERGE (n:Logistik {id: "logistik_lagerpuffer"})
SET n.name = "Lagerpuffer"
;
MERGE (n:Verbindungstechnik {id: "verbindungstechnik_anschlussdetails_fuer_profilvarianten"})
SET n.name = "Anschlussdetails fuer Profilvarianten"
;
MERGE (n:Bauteilgruppe {id: "btg_bedzed_softwood_wall_studs"})
SET n.name = "Wiederverwendete Holzständer / softwood walling studs", n.counts_as_direct_reuse = true, n.laenge_km = 54, n.alte_funktion = "unbekanntes Holz aus Rückbau-/Reclaim-Quellen", n.neue_funktion = "Unterkonstruktion für Gipskartonwände"
;
MERGE (n:Methode {id: "methode_lokale_beschaffung"})
SET n.name = "Lokale Beschaffung"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_wandaufbau"})
SET n.name = "Wandaufbau"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_innenausbau"})
SET n.name = "Innenausbau"
;
MERGE (n:Huerde {id: "huerde_aufbereitung_zuschnitt"})
SET n.name = "Aufbereitung Zuschnitt"
;
MERGE (n:Huerde {id: "huerde_lieferkettenkoordination"})
SET n.name = "Lieferkettenkoordination"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_instandsetzung"})
SET n.name = "Instandsetzung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_behandlung"})
SET n.name = "Behandlung"
;
MERGE (n:Aufbereitungsverfahren {id: "aufbereitungsverfahren_zuschnitt_im_saegewerk"})
SET n.name = "Zuschnitt im Saegewerk"
;
MERGE (n:Bauteilgruppe {id: "btg_bedzed_scaffold_tube_railings"})
SET n.name = "Gerüstrohre als Geländer/Balustraden", n.counts_as_direct_reuse = true, n.alte_funktion = "Gerüstrohr", n.neue_funktion = "Geländer / Balustrade"
;
MERGE (n:Bauteiltyp {id: "bauteiltyp_gelaender"})
SET n.name = "Gelaender"
;
MERGE (n:Bauteilebene {id: "bauteilebene_aussenraum"})
SET n.name = "Aussenraum"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_absturzsicherung"})
SET n.name = "Absturzsicherung"
;
MERGE (n:Bauteilgruppe {id: "btg_bedzed_reclaimed_doors"})
SET n.name = "Wiederverwendete Türen", n.counts_as_direct_reuse = true, n.alte_funktion = "Tür", n.neue_funktion = "Tür"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_nutzbarkeit"})
SET n.name = "Nutzbarkeit"
;
MERGE (n:Huerde {id: "huerde_komplexe_lieferketten_turen"})
SET n.name = "Komplexe Lieferketten Türen"
;
MERGE (n:Bauteilgruppe {id: "btg_bedzed_reclaimed_kerbs_paving"})
SET n.name = "Wiederverwendete Bordsteine und Natursteinplatten", n.counts_as_direct_reuse = true, n.alte_funktion = "Straßen-/Außenraumelement", n.neue_funktion = "Außenraumkante / Boden-/Außenbelag"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_rutschfestigkeit"})
SET n.name = "Rutschfestigkeit"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_frostbestaendigkeit"})
SET n.name = "Frostbestaendigkeit"
;
MERGE (n:Leistungsanforderung {id: "leistungsanforderung_aussenraumtauglichkeit"})
SET n.name = "Aussenraumtauglichkeit"
;
MERGE (n:Huerde {id: "huerde_komplexe_lieferketten_pflaster"})
SET n.name = "Komplexe Lieferketten Pflaster"
;
MERGE (n:Huerde {id: "huerde_reuse_recycling_abgrenzung"})
SET n.name = "Reuse Recycling Abgrenzung"
;
MERGE (n:Akteur {id: "akteur_peabody_trust"})
SET n.name = "Peabody Trust", n.raw_name = "Peabody Trust"
;
MERGE (n:Akteurrolle {id: "akteurrolle_entwicklung"})
SET n.name = "Entwicklung"
;
MERGE (n:Akteurtyp {id: "akteurtyp_bauherr_traeger"})
SET n.name = "Bauherr_Traeger"
;
MERGE (n:Akteurtyp {id: "akteurtyp_organisation"})
SET n.name = "Organisation"
;
MERGE (n:Akteur {id: "akteur_bill_dunster_zedfactory"})
SET n.name = "Bill Dunster / ZEDfactory", n.raw_name = "Bill Dunster / ZEDfactory"
;
MERGE (n:Akteur {id: "akteur_bioregional"})
SET n.name = "BioRegional", n.raw_name = "BioRegional"
;
MERGE (n:Akteurrolle {id: "akteurrolle_beratung"})
SET n.name = "Beratung"
;
MERGE (n:Akteurrolle {id: "akteurrolle_materialbeschaffung"})
SET n.name = "Materialbeschaffung"
;
MERGE (n:Akteurrolle {id: "akteurrolle_monitoring"})
SET n.name = "Monitoring"
;
MERGE (n:Akteurtyp {id: "akteurtyp_ngo_netzwerk"})
SET n.name = "NGO_Netzwerk"
;
MERGE (n:Akteur {id: "akteur_arup"})
SET n.name = "Arup", n.raw_name = "Arup"
;
MERGE (n:Akteur {id: "akteur_ellis_moore"})
SET n.name = "Ellis & Moore Consulting Engineers", n.raw_name = "Ellis & Moore Consulting Engineers"
;
MERGE (n:Akteur {id: "akteur_gardiner_theobald_bedzed"})
SET n.name = "Gardiner & Theobald", n.raw_name = "Gardiner & Theobald"
;
MERGE (n:Akteurrolle {id: "akteurrolle_mengen_kostenschaetzung"})
SET n.name = "Mengen_Kostenschaetzung"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "stadt_london"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "land_vereinigtes_koenigreich"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "stadt_london"})
MATCH (b {id: "land_vereinigtes_koenigreich"})
MERGE (a)-[rel:LIEGT_IN_LAND]->(b)
;
MATCH (a {id: "status_unklar_live"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "status_unklar_live"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "nutzung_arbeitsplatz"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "nutzung_arbeitsplatz"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_buero"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "nutzung_buero"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_retail"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "nutzung_retail"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_gebaeude"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_bestandsobjekt"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "bauobjektrolle_bestandsobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauobjektrolle_empfaengerobjekt"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "nutzung_arbeitsplatz"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "nutzung_buero"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "nutzung_retail"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MATCH (b {id: "status_unklar_live"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_gebaeudeteil"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "bauobjektklasse_gebaeudeteil"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "nutzung_erschliessung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "nutzung_erschliessung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "nutzung_arbeitsplatz"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_55_great_suffolk_external_core"})
MATCH (b {id: "status_unklar_live"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_donorobjekt"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "bauobjektrolle_donorobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "nutzung_buero"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "status_rueckbau_demontage"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_1_broadgate_donor"})
MATCH (b {id: "status_rueckbau_demontage"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "bauwerk_55_great_suffolk_existing_warehouse"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "bauwerk_55_great_suffolk_external_core"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "bauwerk_1_broadgate_donor"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "material_baustahl"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_metall"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_baustahl"})
MATCH (b {id: "materialgruppe_metall"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "btg_55_steel_from_1_broadgate"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "material_baustahl"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_traeger"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauteiltyp_traeger"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_stuetze"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauteiltyp_stuetze"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_tragwerk"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_raumstruktur"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "wiederverwendungsart_urban_mining"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "wiederverwendungsart_urban_mining"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "status_eingebaut"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "tragwerksprinzip_stahlrahmen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "tragwerksprinzip_stahlrahmen"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "bauweise_stahlbau"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauweise_stahlbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "methode_design_follows_availability"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "methode_design_follows_availability"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_rueckbau"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_transport"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_aufbereitung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_planung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_wiedereinbau"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "pruefungnachweis_testing"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "pruefungnachweis_testing"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "pruefungnachweis_ce_marking"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "pruefungnachweis_ce_marking"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "norm_en_1090"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "norm_en_1090"})
MERGE (a)-[rel:REFERENZIERT_NORM]->(b)
;
MATCH (a {id: "leistungsanforderung_tragfaehigkeit"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_schweissbarkeit"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "leistungsanforderung_schweissbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_nachweisbarkeit"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "leistungsanforderung_nachweisbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_profilverfuegbarkeit"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_technisch"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_profilverfuegbarkeit"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "huerde_profilverfuegbarkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_donor_receiver_timing"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_logistisch"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_donor_receiver_timing"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "huerde_donor_receiver_timing"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_zertifizierung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_rechtlich"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_zertifizierung"})
MATCH (b {id: "huerdekategorie_rechtlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "huerde_zertifizierung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_services_koordination"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_planerisch"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_services_koordination"})
MATCH (b {id: "huerdekategorie_planerisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "huerde_services_koordination"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_anbauteile_entfernen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "aufbereitungsverfahren_anbauteile_entfernen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_loecher_fuellen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "aufbereitungsverfahren_loecher_fuellen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_testen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "aufbereitungsverfahren_testen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_ce_markieren"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "aufbereitungsverfahren_ce_markieren"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "rueckbauverfahren_deconstruction_donor_site"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "rueckbauverfahren_deconstruction_donor_site"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "rueckbauverfahren_demolition_donor_site"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "rueckbauverfahren_demolition_donor_site"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "beschaffungsweg_direktdeal_mit_rueckbauprojekt"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "beschaffungsweg_direktdeal_mit_rueckbauprojekt"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "ressourcenquelle_donor_building"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "ressourcenquelle_donor_building"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "logistik_vorausbeschaffung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "logistik_vorausbeschaffung"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauwerk_1_broadgate_donor"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_55_steel_from_1_broadgate"})
MATCH (b {id: "bauwerk_55_great_suffolk_external_core"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_55_great_suffolk_street"})
MATCH (b {id: "btg_55_steel_from_cleveland_stock"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "material_baustahl"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauteiltyp_traeger"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauteiltyp_stuetze"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "wiederverwendungsart_reuse_stockholder_modell"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "wiederverwendungsart_reuse_stockholder_modell"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "tragwerksprinzip_stahlrahmen"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauweise_stahlbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "methode_design_follows_availability"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_lagerung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "prozessphase_lagerung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "pruefungnachweis_testing"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "pruefungnachweis_ce_marking"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "norm_en_1090"})
MERGE (a)-[rel:REFERENZIERT_NORM]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "leistungsanforderung_schweissbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "leistungsanforderung_nachweisbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_marktliquiditaet"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_wirtschaftlich"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_marktliquiditaet"})
MATCH (b {id: "huerdekategorie_wirtschaftlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "huerde_marktliquiditaet"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "huerde_zertifizierung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "huerde_profilverfuegbarkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_restaurierung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "aufbereitungsverfahren_restaurierung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_rezertifizierung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "aufbereitungsverfahren_rezertifizierung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "aufbereitungsverfahren_testen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "aufbereitungsverfahren_ce_markieren"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "beschaffungsweg_reuse_stockholder"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "beschaffungsweg_reuse_stockholder"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "ressourcenquelle_reclaimed_stockholder"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "ressourcenquelle_reclaimed_stockholder"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "logistik_lagerung_bei_stockholder"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "logistik_lagerung_bei_stockholder"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_55_steel_from_cleveland_stock"})
MATCH (b {id: "bauwerk_55_great_suffolk_external_core"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "akteur_fabrix"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_fabrix"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_bauherr_auftraggeber"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_fabrix"})
MATCH (b {id: "akteurrolle_bauherr_auftraggeber"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_developer"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_fabrix"})
MATCH (b {id: "akteurrolle_developer"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_unternehmen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_fabrix"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_hawkins_brown"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_hawkins_brown"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_architektur"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_hawkins_brown"})
MATCH (b {id: "akteurrolle_architektur"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_planungsbuero"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_hawkins_brown"})
MATCH (b {id: "akteurtyp_planungsbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_symmetrys"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_symmetrys"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_tragwerksplanung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_symmetrys"})
MATCH (b {id: "akteurrolle_tragwerksplanung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_ingenieurbuero"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_symmetrys"})
MATCH (b {id: "akteurtyp_ingenieurbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_akt_ii"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_akt_ii"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_engineering_consultant"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_akt_ii"})
MATCH (b {id: "akteurrolle_engineering_consultant"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_reuse_beratung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_akt_ii"})
MATCH (b {id: "akteurrolle_reuse_beratung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_akt_ii"})
MATCH (b {id: "akteurtyp_ingenieurbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_cbre"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cbre"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_nachhaltigkeitsberatung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cbre"})
MATCH (b {id: "akteurrolle_nachhaltigkeitsberatung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_embodied_carbon_beratung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cbre"})
MATCH (b {id: "akteurrolle_embodied_carbon_beratung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_cbre"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_opera"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_opera"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_projektmanagement"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_opera"})
MATCH (b {id: "akteurrolle_projektmanagement"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_opera"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_gardiner_theobald"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteur_gardiner_theobald"})
MATCH (b {id: "akteurrolle_projektmanagement"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_reuse_beschaffung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald"})
MATCH (b {id: "akteurrolle_reuse_beschaffung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_gardiner_theobald"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_cantillon"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cantillon"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_rueckbau_demontage"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cantillon"})
MATCH (b {id: "akteurrolle_rueckbau_demontage"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_rueckbauunternehmen"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cantillon"})
MATCH (b {id: "akteurtyp_rueckbauunternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "projekt_55_great_suffolk_street"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_materiallieferant"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "akteurrolle_materiallieferant"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_reuse_stockholder"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "akteurrolle_reuse_stockholder"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_aufbereitung_pruefung"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "akteurrolle_aufbereitung_pruefung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteurtyp_materialhaendler"})
MATCH (b {id: "quelle_55_great_suffolk_street_london_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_cleveland_steel_and_tubes"})
MATCH (b {id: "akteurtyp_materialhaendler"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "stadt_groeditz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "land_deutschland"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "stadt_groeditz"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "stadt_groeditz"})
MATCH (b {id: "land_deutschland"})
MERGE (a)-[rel:LIEGT_IN_LAND]->(b)
;
MATCH (a {id: "status_gebaut"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "nutzung_sport_verein"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "nutzung_sport_verein"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "stadt_groeditz"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_gebaeude"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_empfaengerobjekt"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "nutzung_sport_verein"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_groeditz_association_house"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "stadt_groeditz"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_donorobjekt"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "bauobjektrolle_donorobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "nutzung_schule"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "nutzung_schule"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "status_rueckbau_demontage"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_donor_school_dresden_type"})
MATCH (b {id: "status_rueckbau_demontage"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_wbs70"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_groeditz_donor_wbs70"})
MATCH (b {id: "stadt_groeditz"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_wbs70"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_wbs70"})
MATCH (b {id: "bauobjektrolle_donorobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_groeditz_donor_wbs70"})
MATCH (b {id: "status_rueckbau_demontage"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "bauwerk_groeditz_association_house"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "bauwerk_groeditz_donor_school_dresden_type"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "bauwerk_groeditz_donor_wbs70"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "material_stahlbetonfertigteil"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_mineralisch"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_stahlbetonfertigteil"})
MATCH (b {id: "materialgruppe_mineralisch"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "btg_groeditz_dresden_type_precast_parts"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_wand"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_decke"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteiltyp_decke"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_treppe"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteiltyp_treppe"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_fassade"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteiltyp_fassade"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_tragwerk"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_huelle"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteilebene_huelle"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_raumstruktur"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "status_eingebaut"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "bauweise_betonfertigteilbau"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "bausystem_dresden_typ"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bausystem_dresden_typ"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "methode_bauteilinventar"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "methode_bauteilinventar"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_bauteilgerechte_planung"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_bauteilinventar"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_rueckbau"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_transport"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_planung"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_wiedereinbau"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_tragfaehigkeit"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_brandschutz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_schallschutz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "leistungsanforderung_schallschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_feuchteschutz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "leistungsanforderung_feuchteschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_waermeschutz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "leistungsanforderung_waermeschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_systemmix"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_technisch"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_systemmix"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "huerde_systemmix"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_hoehenausgleich"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_hoehenausgleich"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "huerde_hoehenausgleich"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_anschlussdetails"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_anschlussdetails"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_tragwerksnachweis"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_rechtlich"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_tragwerksnachweis"})
MATCH (b {id: "huerdekategorie_rechtlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "huerde_tragwerksnachweis"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_ziegelschicht_zum_hoehenausgleich"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "aufbereitungsverfahren_ziegelschicht_zum_hoehenausgleich"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "rueckbauverfahren_selektiver_rueckbau"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "rueckbauverfahren_demontage"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "logistik_kurze_lokale_transportdistanz"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauwerk_groeditz_donor_school_dresden_type"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_groeditz_dresden_type_precast_parts"})
MATCH (b {id: "bauwerk_groeditz_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_groeditz"})
MATCH (b {id: "btg_groeditz_wbs70_panels"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteiltyp_decke"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteiltyp_fassade"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteilebene_huelle"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "bausystem_wbs70"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bausystem_wbs70"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "methode_bauteilinventar"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "leistungsanforderung_feuchteschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "leistungsanforderung_waermeschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "huerde_systemmix"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "huerde_hoehenausgleich"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_logistik_schwerer_bauteile"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_logistisch"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_logistik_schwerer_bauteile"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "huerde_logistik_schwerer_bauteile"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "aufbereitungsverfahren_ziegelschicht_zum_hoehenausgleich"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_ueberlappende_fassaden_fertigteile"})
MATCH (b {id: "quelle_association_house_groeditz_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "aufbereitungsverfahren_ueberlappende_fassaden_fertigteile"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauwerk_groeditz_donor_wbs70"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_groeditz_wbs70_panels"})
MATCH (b {id: "bauwerk_groeditz_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "stadt_plauen"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "land_deutschland"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "stadt_plauen"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "stadt_plauen"})
MATCH (b {id: "land_deutschland"})
MERGE (a)-[rel:LIEGT_IN_LAND]->(b)
;
MATCH (a {id: "status_gebaut"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "nutzung_sport_verein"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "nutzung_sport_verein"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "stadt_plauen"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_gebaeude"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_empfaengerobjekt"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "nutzung_sport_verein"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_plauen_association_house"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "stadt_plauen"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "bauobjektklasse_gebaeude"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_donorobjekt"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "bauobjektrolle_donorobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "nutzung_wohnen"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "nutzung_wohnen"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "status_rueckbau_demontage"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_plauen_donor_iw73_6"})
MATCH (b {id: "status_rueckbau_demontage"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "bauwerk_plauen_association_house"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "bauwerk_plauen_donor_iw73_6"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "material_stahlbetonfertigteil"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_mineralisch"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "btg_plauen_floor_ceiling_slabs"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_decke"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauteiltyp_decke"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_boden"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauteiltyp_boden"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_tragwerk"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_raumstruktur"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "status_eingebaut"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "bauweise_betonfertigteilbau"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "bausystem_iw73_6"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bausystem_iw73_6"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "methode_bauteilidentifikation"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "methode_bauteilidentifikation"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_bauteilgerechte_planung"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_bauteilinventar"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_rueckbau"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_transport"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_planung"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_wiedereinbau"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_tragfaehigkeit"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_gebrauchstauglichkeit"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "leistungsanforderung_gebrauchstauglichkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_brandschutz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_bauteilgeometrie_rasterbindung"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_planerisch"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_bauteilgeometrie_rasterbindung"})
MATCH (b {id: "huerdekategorie_planerisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "huerde_bauteilgeometrie_rasterbindung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_anschlussdetails"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_technisch"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_nachweisfaehigkeit"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_rechtlich"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_nachweisfaehigkeit"})
MATCH (b {id: "huerdekategorie_rechtlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "huerde_nachweisfaehigkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_fehlende_primaerdaten"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_daten_evidenz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_fehlende_primaerdaten"})
MATCH (b {id: "huerdekategorie_daten_evidenz"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "huerde_fehlende_primaerdaten"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "rueckbauverfahren_selektiver_rueckbau"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "rueckbauverfahren_demontage"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "logistik_kurze_lokale_transportdistanz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauwerk_plauen_donor_iw73_6"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_plauen_floor_ceiling_slabs"})
MATCH (b {id: "bauwerk_plauen_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "btg_plauen_exterior_wall_elements"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_wand"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_fassade"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauteiltyp_fassade"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_huelle"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauteilebene_huelle"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bausystem_iw73_6"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "methode_bauteilidentifikation"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_waermeschutz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "leistungsanforderung_waermeschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_feuchteschutz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "leistungsanforderung_feuchteschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "huerde_bauteilgeometrie_rasterbindung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "huerde_nachweisfaehigkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "huerde_fehlende_primaerdaten"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_waermebruecken"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_waermebruecken"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "huerde_waermebruecken"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauwerk_plauen_donor_iw73_6"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_plauen_exterior_wall_elements"})
MATCH (b {id: "bauwerk_plauen_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "btg_plauen_interior_wall_elements"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bausystem_iw73_6"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "methode_bauteilidentifikation"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_schallschutz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "leistungsanforderung_schallschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "huerde_bauteilgeometrie_rasterbindung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "huerde_nachweisfaehigkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "huerde_fehlende_primaerdaten"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauwerk_plauen_donor_iw73_6"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_plauen_interior_wall_elements"})
MATCH (b {id: "bauwerk_plauen_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_association_house_plauen"})
MATCH (b {id: "btg_plauen_basement_wall_elements"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "material_stahlbetonfertigteil"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "tragwerksprinzip_fertigteil_wand_deckensystem"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauweise_betonfertigteilbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bausystem_iw73_6"})
MERGE (a)-[rel:HAT_BAUSYSTEM]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "methode_bauteilidentifikation"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "methode_bauteilgerechte_planung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "leistungsanforderung_feuchteschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_dauerhaftigkeit"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "leistungsanforderung_dauerhaftigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "huerde_bauteilgeometrie_rasterbindung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "huerde_anschlussdetails"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "huerde_nachweisfaehigkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "huerde_fehlende_primaerdaten"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_feuchteschutz"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_umwelt_gesundheit"})
MATCH (b {id: "quelle_association_house_plauen_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_feuchteschutz"})
MATCH (b {id: "huerdekategorie_umwelt_gesundheit"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "huerde_feuchteschutz"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "rueckbauverfahren_selektiver_rueckbau"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "rueckbauverfahren_demontage"})
MERGE (a)-[rel:HAT_RUECKBAUVERFAHREN]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "logistik_kurze_lokale_transportdistanz"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauwerk_plauen_donor_iw73_6"})
MERGE (a)-[rel:AUS_BAUWERK]->(b)
;
MATCH (a {id: "btg_plauen_basement_wall_elements"})
MATCH (b {id: "bauwerk_plauen_association_house"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "stadt_muenster"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "land_deutschland"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "stadt_muenster"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "stadt_muenster"})
MATCH (b {id: "land_deutschland"})
MERGE (a)-[rel:LIEGT_IN_LAND]->(b)
;
MATCH (a {id: "status_gebaut"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "nutzung_verwaltung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "nutzung_verwaltung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_buero"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "nutzung_buero"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_workshop"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "nutzung_workshop"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_besprechung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "nutzung_besprechung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_kueche"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "nutzung_kueche"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "stadt_muenster"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_gebaeudeteil"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "bauobjektklasse_gebaeudeteil"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_bestandsobjekt"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "bauobjektrolle_bestandsobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauobjektrolle_empfaengerobjekt"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "nutzung_verwaltung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "nutzung_buero"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_awm_muenster_3og"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "material_glas"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_mineralisch"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_glas"})
MATCH (b {id: "materialgruppe_mineralisch"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "material_metall"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_metall"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_metall"})
MATCH (b {id: "materialgruppe_metall"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "material_holz"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_biobasiert"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_holz"})
MATCH (b {id: "materialgruppe_biobasiert"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "material_mischmaterial_innenausbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_gemischt"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_mischmaterial_innenausbau"})
MATCH (b {id: "materialgruppe_gemischt"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_glass_partitions_doors"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "material_glas"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_wand"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_tuer"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauteiltyp_tuer"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_ausbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_innenausbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_raumstruktur"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "wiederverwendungsart_fester_innenausbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "status_eingebaut"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "methode_reuse_first"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "methode_reuse_first"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_design_follows_availability"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "methode_design_follows_availability"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_rueckbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_transport"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_planung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_wiedereinbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_monitoring"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "prozessphase_monitoring"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_brandschutz"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_schallschutz"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "leistungsanforderung_schallschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_sicherheit"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "leistungsanforderung_sicherheit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_passung_zustand"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_technisch"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_passung_zustand"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "huerde_passung_zustand"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_brandschutz_nicht_oeffentlich"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_rechtlich"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_brandschutz_nicht_oeffentlich"})
MATCH (b {id: "huerdekategorie_rechtlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "huerde_brandschutz_nicht_oeffentlich"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_interior_grenzfall"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_planerisch"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_interior_grenzfall"})
MATCH (b {id: "huerdekategorie_planerisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "huerde_interior_grenzfall"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "beschaffungsweg_concular_materialplattform"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "beschaffungsweg_concular_materialplattform"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "ressourcenquelle_behrensbau_dusseldorf"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "ressourcenquelle_behrensbau_dusseldorf"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "logistik_urban_mining_aus_oeffentlichen_gebaeuden"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "logistik_urban_mining_aus_oeffentlichen_gebaeuden"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "btg_awm_glass_partitions_doors"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_wc_partitions"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "material_mischmaterial_innenausbau"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "methode_reuse_first"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_hygiene"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "leistungsanforderung_hygiene"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_feuchteschutz"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "leistungsanforderung_feuchteschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_stabilitaet"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "leistungsanforderung_stabilitaet"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "huerde_passung_zustand"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_hygiene_feuchte"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_umwelt_gesundheit"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_hygiene_feuchte"})
MATCH (b {id: "huerdekategorie_umwelt_gesundheit"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "huerde_hygiene_feuchte"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "beschaffungsweg_concular_materialplattform"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "ressourcenquelle_behrensbau_dusseldorf"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "btg_awm_wc_partitions"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_cable_trays_shelves"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "material_metall"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_technik"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "bauteiltyp_technik"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_technische_ausstattung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "bauteilebene_technische_ausstattung"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_funktionswechsel"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "wiederverwendungsart_funktionswechsel"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "methode_upcycling"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "methode_upcycling"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "methode_design_follows_availability"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_aufbereitung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_tragfaehigkeit"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_neue_lastfunktion"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_neue_lastfunktion"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "huerde_neue_lastfunktion"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "huerde_interior_grenzfall"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_umnutzung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "aufbereitungsverfahren_umnutzung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_3d_gedruckte_halterungen"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "aufbereitungsverfahren_3d_gedruckte_halterungen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "verbindungstechnik_spezialhalterungen"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "verbindungstechnik_spezialhalterungen"})
MERGE (a)-[rel:HAT_VERBINDUNGSTECHNIK]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_shelves"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_cable_trays_led_lighting"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "material_metall"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "bauteiltyp_technik"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "bauteilebene_technische_ausstattung"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "wiederverwendungsart_funktionswechsel"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "methode_reaktivierung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "methode_reaktivierung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_aufputzfuhrung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "methode_aufputzfuhrung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_elektrosicherheit"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "leistungsanforderung_elektrosicherheit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_wartbarkeit"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "leistungsanforderung_wartbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_elektrosicherheit_tga"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_elektrosicherheit_tga"})
MATCH (b {id: "huerdekategorie_rechtlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "huerde_elektrosicherheit_tga"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_technische_reaktivierung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_technische_reaktivierung"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "huerde_technische_reaktivierung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_reaktivierung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "aufbereitungsverfahren_reaktivierung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_montage"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "aufbereitungsverfahren_montage"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_awm_cable_trays_led_lighting"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_chair_parts_wall_cladding"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "material_holz"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "wiederverwendungsart_funktionswechsel"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "methode_upcycling"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_spuren_als_gestaltung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "methode_spuren_als_gestaltung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_oberflaeche"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "leistungsanforderung_oberflaeche"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "huerde_interior_grenzfall"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "huerde_brandschutz_nicht_oeffentlich"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_akzeptanz_gebrauchsspuren"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_sozial_organisatorisch"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_akzeptanz_gebrauchsspuren"})
MATCH (b {id: "huerdekategorie_sozial_organisatorisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "huerde_akzeptanz_gebrauchsspuren"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_demontage"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "aufbereitungsverfahren_demontage"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_zuschnitt"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "aufbereitungsverfahren_zuschnitt"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_wandmontage"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "aufbereitungsverfahren_wandmontage"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_awm_chair_parts_wall_cladding"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_awm_muenster_circular_office"})
MATCH (b {id: "btg_awm_reused_wood_built_ins"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "material_holz"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "wiederverwendungsart_fester_innenausbau"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "methode_reuse_first"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "leistungsanforderung_stabilitaet"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "leistungsanforderung_hygiene"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_herkunft_sortierung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_logistisch"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_herkunft_sortierung"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "huerde_herkunft_sortierung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "huerde_passung_zustand"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_rueckbau"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "aufbereitungsverfahren_rueckbau"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "aufbereitungsverfahren_zuschnitt"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_tischlerische_aufbereitung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "aufbereitungsverfahren_tischlerische_aufbereitung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "ressourcenquelle_deckenkonstruktion_supermarkt"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "ressourcenquelle_deckenkonstruktion_supermarkt"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "ressourcenquelle_discounter_aufloesung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "ressourcenquelle_discounter_aufloesung"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "btg_awm_reused_wood_built_ins"})
MATCH (b {id: "bauwerk_awm_muenster_3og"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "akteur_awm_muenster"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_awm_muenster"})
MATCH (b {id: "projekt_awm_muenster_circular_office"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_bauherr_auftraggeber"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_awm_muenster"})
MATCH (b {id: "akteurrolle_bauherr_auftraggeber"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_nutzer"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_awm_muenster"})
MATCH (b {id: "akteurrolle_nutzer"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_oeffentliche_institution"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_awm_muenster"})
MATCH (b {id: "akteurtyp_oeffentliche_institution"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "projekt_awm_muenster_circular_office"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_innenarchitektur"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "akteurrolle_innenarchitektur"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_design_build"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "akteurrolle_design_build"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_planungsbuero"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "akteurtyp_planungsbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteurtyp_unternehmen"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_urselmann_interior"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "projekt_awm_muenster_circular_office"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_materialplattform"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "akteurrolle_materialplattform"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_oekobilanzierung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "akteurrolle_oekobilanzierung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_reuse_beschaffung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "akteurrolle_reuse_beschaffung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_materialplattform"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "akteurtyp_materialplattform"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_concular"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_petra_jablonicka"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_petra_jablonicka"})
MATCH (b {id: "projekt_awm_muenster_circular_office"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteur_petra_jablonicka"})
MATCH (b {id: "akteurrolle_innenarchitektur"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_person"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_petra_jablonicka"})
MATCH (b {id: "akteurtyp_person"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_sven_urselmann"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_sven_urselmann"})
MATCH (b {id: "projekt_awm_muenster_circular_office"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteur_sven_urselmann"})
MATCH (b {id: "akteurrolle_innenarchitektur"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_projektleitung"})
MATCH (b {id: "quelle_awm_muenster_circular_office_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_sven_urselmann"})
MATCH (b {id: "akteurrolle_projektleitung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_sven_urselmann"})
MATCH (b {id: "akteurtyp_person"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "stadt_london"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "land_vereinigtes_koenigreich"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "status_gebaut"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "nutzung_wohnen"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "nutzung_wohnen"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_arbeiten"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "nutzung_arbeiten"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "nutzung_gemeinschaftsnutzung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "nutzung_gemeinschaftsnutzung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "stadt_london"})
MERGE (a)-[rel:LIEGT_IN_STADT]->(b)
;
MATCH (a {id: "bauobjektklasse_quartier_areal"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "bauobjektklasse_quartier_areal"})
MERGE (a)-[rel:HAT_BAUOBJEKTKLASSE]->(b)
;
MATCH (a {id: "bauobjektrolle_empfaengerobjekt"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "bauobjektrolle_empfaengerobjekt"})
MERGE (a)-[rel:HAT_BAUOBJEKTROLLE]->(b)
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "nutzung_wohnen"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "nutzung_arbeiten"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "nutzung_gemeinschaftsnutzung"})
MERGE (a)-[rel:HAT_NUTZUNG]->(b)
;
MATCH (a {id: "bauwerk_bedzed_quarter"})
MATCH (b {id: "status_gebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:NUTZT_BAUWERK]->(b)
;
MATCH (a {id: "material_baustahl"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_metall"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_holz"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_biobasiert"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_naturstein_betonstein"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "materialgruppe_mineralisch"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "material_naturstein_betonstein"})
MATCH (b {id: "materialgruppe_mineralisch"})
MERGE (a)-[rel:HAT_MATERIALGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "btg_bedzed_reclaimed_structural_steel"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "material_baustahl"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_traeger"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "bauteiltyp_traeger"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_stuetze"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "bauteiltyp_stuetze"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_tragwerk"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "bauteilebene_tragwerk"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "wiederverwendungsart_urban_mining"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "wiederverwendungsart_urban_mining"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "status_eingebaut"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "tragwerksprinzip_stahlrahmen"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "tragwerksprinzip_stahlrahmen"})
MERGE (a)-[rel:HAT_TRAGWERKSPRINZIP]->(b)
;
MATCH (a {id: "bauweise_stahlbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "bauweise_stahlbau"})
MERGE (a)-[rel:HAT_BAUWEISE]->(b)
;
MATCH (a {id: "methode_flexible_querschnittsspezifikation"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "methode_flexible_querschnittsspezifikation"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "methode_design_follows_availability"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "methode_design_follows_availability"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "prozessphase_bestandsaufnahme"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_bestandsaufnahme"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_bauteilinventar"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_bauteilinventar"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_rueckbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_transport"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_lagerung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_lagerung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_aufbereitung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_planung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_planung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_wiedereinbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "prozessphase_monitoring"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "prozessphase_monitoring"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "pruefungnachweis_sichtpruefung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "pruefungnachweis_sichtpruefung"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "pruefungnachweis_herstellungsdatum"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "pruefungnachweis_herstellungsdatum"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "pruefungnachweis_materialzustand"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "pruefungnachweis_materialzustand"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "pruefungnachweis_fabrikationseignung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "pruefungnachweis_fabrikationseignung"})
MERGE (a)-[rel:HAT_PRUEFUNG]->(b)
;
MATCH (a {id: "norm_historic_sections_book"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "norm_historic_sections_book"})
MERGE (a)-[rel:REFERENZIERT_NORM]->(b)
;
MATCH (a {id: "leistungsanforderung_tragfaehigkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "leistungsanforderung_tragfaehigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_stabilitaet"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "leistungsanforderung_stabilitaet"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_korrosionsschutz"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "leistungsanforderung_korrosionsschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_nachweisbarkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "leistungsanforderung_nachweisbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_passende_stahlprofile_schwer_verfuegbar"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_logistisch"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_passende_stahlprofile_schwer_verfuegbar"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "huerde_passende_stahlprofile_schwer_verfuegbar"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_qualitaetsnachweis_historischer_profile"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_technisch"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_qualitaetsnachweis_historischer_profile"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "huerde_qualitaetsnachweis_historischer_profile"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_zusatzaufbereitung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_wirtschaftlich"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_zusatzaufbereitung"})
MATCH (b {id: "huerdekategorie_wirtschaftlich"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "huerde_zusatzaufbereitung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_gebogene_profile_nicht_reused"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_gebogene_profile_nicht_reused"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "huerde_gebogene_profile_nicht_reused"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_lagerbedarf"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_lagerbedarf"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "huerde_lagerbedarf"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_sandstrahlen"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "aufbereitungsverfahren_sandstrahlen"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_fertigung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "aufbereitungsverfahren_fertigung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_lackierung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "aufbereitungsverfahren_lackierung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_zinkreiche_beschichtung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "aufbereitungsverfahren_zinkreiche_beschichtung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "beschaffungsweg_aktive_materialsuche"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "beschaffungsweg_aktive_materialsuche"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "beschaffungsweg_free_issue_material"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "beschaffungsweg_free_issue_material"})
MERGE (a)-[rel:HAT_BESCHAFFUNGSWEG]->(b)
;
MATCH (a {id: "ressourcenquelle_lokale_abbruchstandorte"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "ressourcenquelle_lokale_abbruchstandorte"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "ressourcenquelle_brighton_railway_station"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "ressourcenquelle_brighton_railway_station"})
MERGE (a)-[rel:HAT_RESSOURCENQUELLE]->(b)
;
MATCH (a {id: "logistik_35_mile_zielradius"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "logistik_35_mile_zielradius"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "logistik_lange_vorlaufzeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "logistik_lange_vorlaufzeit"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "logistik_lagerpuffer"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "logistik_lagerpuffer"})
MERGE (a)-[rel:HAT_LOGISTIK]->(b)
;
MATCH (a {id: "verbindungstechnik_anschlussdetails_fuer_profilvarianten"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "verbindungstechnik_anschlussdetails_fuer_profilvarianten"})
MERGE (a)-[rel:HAT_VERBINDUNGSTECHNIK]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_structural_steel"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "btg_bedzed_softwood_wall_studs"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "material_holz"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_wand"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "bauteiltyp_wand"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteiltyp_ausbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_innenausbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "bauteilebene_raumstruktur"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "methode_lokale_beschaffung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "methode_lokale_beschaffung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_wandaufbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "leistungsanforderung_wandaufbau"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_innenausbau"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "leistungsanforderung_innenausbau"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_aufbereitung_zuschnitt"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_aufbereitung_zuschnitt"})
MATCH (b {id: "huerdekategorie_technisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "huerde_aufbereitung_zuschnitt"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_lieferkettenkoordination"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_lieferkettenkoordination"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "huerde_lieferkettenkoordination"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_instandsetzung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "aufbereitungsverfahren_instandsetzung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_behandlung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "aufbereitungsverfahren_behandlung"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "aufbereitungsverfahren_zuschnitt_im_saegewerk"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "aufbereitungsverfahren_zuschnitt_im_saegewerk"})
MERGE (a)-[rel:HAT_AUFBEREITUNG]->(b)
;
MATCH (a {id: "btg_bedzed_softwood_wall_studs"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "btg_bedzed_scaffold_tube_railings"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "material_baustahl"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_gelaender"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "bauteiltyp_gelaender"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "bauteilebene_aussenraum"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "bauteilebene_aussenraum"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "wiederverwendungsart_funktionswechsel"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "wiederverwendungsart_funktionswechsel"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "methode_lokale_beschaffung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "prozessphase_aufbereitung"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_absturzsicherung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "leistungsanforderung_absturzsicherung"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_dauerhaftigkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "leistungsanforderung_dauerhaftigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_nachweisfaehigkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_rechtlich"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "huerde_nachweisfaehigkeit"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_passung_zustand"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "huerde_passung_zustand"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_bedzed_scaffold_tube_railings"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "btg_bedzed_reclaimed_doors"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "material_holz"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_tuer"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "bauteiltyp_tuer"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "bauteilebene_innenausbau"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "bauteilebene_raumstruktur"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "methode_lokale_beschaffung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_nutzbarkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "leistungsanforderung_nutzbarkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_brandschutz"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "leistungsanforderung_brandschutz"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_komplexe_lieferketten_turen"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_komplexe_lieferketten_turen"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "huerde_komplexe_lieferketten_turen"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_brandschutz_nicht_oeffentlich"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "huerde_brandschutz_nicht_oeffentlich"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_doors"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "projekt_bedzed"})
MATCH (b {id: "btg_bedzed_reclaimed_kerbs_paving"})
MERGE (a)-[rel:HAT_BAUTEILGRUPPE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "material_naturstein_betonstein"})
MERGE (a)-[rel:NUTZT_MATERIAL]->(b)
;
MATCH (a {id: "bauteiltyp_boden"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "bauteiltyp_boden"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "bauteiltyp_ausbau"})
MERGE (a)-[rel:HAT_BAUTEILTYP]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "bauteilebene_aussenraum"})
MERGE (a)-[rel:HAT_BAUTEILEBENE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "wiederverwendungsart_ex_situ_bauteilwiederverwendung"})
MERGE (a)-[rel:HAT_WIEDERVERWENDUNGSART]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "status_eingebaut"})
MERGE (a)-[rel:HAT_STATUS]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "methode_lokale_beschaffung"})
MERGE (a)-[rel:HAT_METHODE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "prozessphase_rueckbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "prozessphase_transport"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "prozessphase_wiedereinbau"})
MERGE (a)-[rel:HAT_PROZESSPHASE]->(b)
;
MATCH (a {id: "leistungsanforderung_rutschfestigkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "leistungsanforderung_rutschfestigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_frostbestaendigkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "leistungsanforderung_frostbestaendigkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "leistungsanforderung_aussenraumtauglichkeit"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "leistungsanforderung_aussenraumtauglichkeit"})
MERGE (a)-[rel:HAT_LEISTUNGSANFORDERUNG]->(b)
;
MATCH (a {id: "huerde_komplexe_lieferketten_pflaster"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_komplexe_lieferketten_pflaster"})
MATCH (b {id: "huerdekategorie_logistisch"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "huerde_komplexe_lieferketten_pflaster"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "huerde_reuse_recycling_abgrenzung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerdekategorie_daten_evidenz"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "huerde_reuse_recycling_abgrenzung"})
MATCH (b {id: "huerdekategorie_daten_evidenz"})
MERGE (a)-[rel:HAT_HUERDEKATEGORIE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "huerde_reuse_recycling_abgrenzung"})
MERGE (a)-[rel:HAT_HUERDE]->(b)
;
MATCH (a {id: "btg_bedzed_reclaimed_kerbs_paving"})
MATCH (b {id: "bauwerk_bedzed_quarter"})
MERGE (a)-[rel:EINGEBAUT_IN]->(b)
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_bauherr_auftraggeber"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "akteurrolle_bauherr_auftraggeber"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_entwicklung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "akteurrolle_entwicklung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_bauherr_traeger"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "akteurtyp_bauherr_traeger"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteurtyp_organisation"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_peabody_trust"})
MATCH (b {id: "akteurtyp_organisation"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_bill_dunster_zedfactory"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bill_dunster_zedfactory"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_architektur"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bill_dunster_zedfactory"})
MATCH (b {id: "akteurrolle_architektur"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_planungsbuero"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bill_dunster_zedfactory"})
MATCH (b {id: "akteurtyp_planungsbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_beratung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "akteurrolle_beratung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_materialbeschaffung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "akteurrolle_materialbeschaffung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_monitoring"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "akteurrolle_monitoring"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_ngo_netzwerk"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "akteurtyp_ngo_netzwerk"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_bioregional"})
MATCH (b {id: "akteurtyp_organisation"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_arup"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_arup"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteur_arup"})
MATCH (b {id: "akteurrolle_beratung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_engineering_consultant"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_arup"})
MATCH (b {id: "akteurrolle_engineering_consultant"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_ingenieurbuero"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_arup"})
MATCH (b {id: "akteurtyp_ingenieurbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_ellis_moore"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_ellis_moore"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_tragwerksplanung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_ellis_moore"})
MATCH (b {id: "akteurrolle_tragwerksplanung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteur_ellis_moore"})
MATCH (b {id: "akteurtyp_ingenieurbuero"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;
MATCH (a {id: "akteur_gardiner_theobald_bedzed"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald_bedzed"})
MATCH (b {id: "projekt_bedzed"})
MERGE (a)-[rel:BETEILIGT_AN]->(b)
;
MATCH (a {id: "akteurrolle_mengen_kostenschaetzung"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald_bedzed"})
MATCH (b {id: "akteurrolle_mengen_kostenschaetzung"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurrolle_projektmanagement"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald_bedzed"})
MATCH (b {id: "akteurrolle_projektmanagement"})
MERGE (a)-[rel:HAT_AKTEURROLLE]->(b)
;
MATCH (a {id: "akteurtyp_unternehmen"})
MATCH (b {id: "quelle_bedzed_london_hackbridge_md"})
MERGE (a)-[rel:BELEGT_IN]->(b)
SET rel.datenqualitaet = "Belegt"
;
MATCH (a {id: "akteur_gardiner_theobald_bedzed"})
MATCH (b {id: "akteurtyp_unternehmen"})
MERGE (a)-[rel:HAT_AKTEURTYP]->(b)
;