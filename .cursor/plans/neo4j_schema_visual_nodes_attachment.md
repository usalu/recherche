# Neo4j-Visualisierung — konkreter Knotenkatalog (Modus A)

Eine geplante **Graph-Vertex** pro Zeile, die mit `(:<Label>` beginnt und ein `{...}` trägt (siehe [neo4j_schema_catalogue_3bc01035.plan.md](e:/recherche/.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) § „Autoritativer vertikaler Gesamtbaum“). Abschnitt **A** des Visual-Plans listet nur die **45 Label-Typen**; **dieses Dokument** ist die Vertex-Menge für den Typgraphen mit **Instanz**-Mustern.

```text
:Fallbeispiel
  (:Fallbeispiel {id: "Berlin_Schildow_Pilot_Haus", art: "Fallstudie_Projekt"})
  (:Fallbeispiel {id: "55_Great_Suffolk_Street_London", art: "Projekt"})
  (:Fallbeispiel {id: "K118_Halle_118_Winterthur", art: "Fallstudie"})
  (:Fallbeispiel {id: "AWM_Muenster_Circular_Office", art: "Fallstudie_Projekt"})

:Bauwerk
  (:Bauwerk {id: "Berlin_Schildow_Pilot_Haus_Gebaeude", art: "Gebaeude"})
  (:Bauwerk {id: "55_Great_Suffolk_Street_London_Lager", art: "Lager"})
  (:Bauwerk {id: "K118_Halle_118_Winterthur", art: "Halle"})
  (:Bauwerk {id: "AWM_Muenster_Circular_Office", art: "Innenausbau"})

:Bauteilgruppe
  (:Bauteilgruppe {id: "K118_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "K118_C02_Treppe"})
  (:Bauteilgruppe {id: "ELYS_C01_Fenster"})
  (:Bauteilgruppe {id: "Plattenpalast_C01_Wandplatten"})
  (:Bauteilgruppe {id: "55GSS_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "CRCLR_C02_Wandpaneele"})
  (:Bauteilgruppe {id: "Werkhof29_C01_Fassadenbleche"})

:ReuseEinsatz
  (:ReuseEinsatz {id: "K118_C01_Traeger_Stuetzen"})
  (:ReuseEinsatz {id: "K118_C02_Treppe"})

:Akteur
  (:Akteur {id: "Circular_Berlin"})
  (:Akteur {id: "Circular_Structural_Design"})
  (:Akteur {id: "Bellastock"})
  (:Akteur {id: "Arup"})
  (:Akteur {id: "Dirk_Hebel"})
  (:Akteur {id: "Bauteilboerse_Hannover"})
  (:Akteur {id: "Bauteilboerse_Bremen"})

:Quelle
  (:Quelle {id: "BBSR_Zukunft_Bau_foerderprogramm", art: "Website"})
  (:Quelle {id: "Circular_Berlin_marktstudie_wiederverwendung", art: "Bericht"})
  (:Quelle {id: "Bellastock_research_note", art: "Paper"})

:Software
  (:Software {id: "Madaster", title: "Madaster", softwaretyp: "Materialdatenbank"})
  (:Software {id: "Concular", title: "Concular", softwaretyp: "Bauteilplattform"})
  (:Software {id: "Restado", title: "Restado"})
  (:Software {id: "Loopfront", title: "Loopfront"})
  (:Software {id: "Revit", title: "Autodesk Revit", softwaretyp: "CAD"})
  (:Software {id: "Rhino", title: "Rhino", softwaretyp: "CAD"})
  (:Software {id: "OneClickLCA", title: "One Click LCA", softwaretyp: "LCA_Software"})
  (:Software {id: "Excel", title: "Microsoft Excel", softwaretyp: "Tabellenkalkulation"})
  (:Software {id: "QGIS", title: "QGIS", softwaretyp: "GIS"})

:Tool
  (:Tool {id: "Grasshopper_Material_Matching_Skript", title: "Grasshopper-Skript Material-Matching", tooltyp: "Skript", funktion: "Matching"})
  (:Tool {id: "Revit_Materialpass_Plugin", title: "Revit-Materialpass-Plug-in", tooltyp: "Plugin"})
  (:Tool {id: "CO2_Rechner_Spreadsheet", title: "CO2-Rechner (Tabellenblatt)", tooltyp: "Rechner"})
  (:Tool {id: "CSV_Import_Skript", title: "CSV-Import-Skript", tooltyp: "Skript"})
  (:Tool {id: "API_Connector", title: "API-Connector", tooltyp: "API"})
  (:Tool {id: "Material_Matching_Algorithmus", title: "Material-Matching-Algorithmus", tooltyp: "Modul"})

:Wiederverwendungskette
  (:Wiederverwendungskette {id: "55_Great_Suffolk_Street_London"})
  (:Wiederverwendungskette {id: "K118_Halle_118_Winterthur"})
  (:Wiederverwendungskette {id: "House_of_Fraser_Oxford_Street_London_reuse_chain"})

:Bauteiltyp
  (:Bauteiltyp {id: "Ausbau"})
  (:Bauteiltyp {id: "Boden"})
  (:Bauteiltyp {id: "Dach"})
  (:Bauteiltyp {id: "Daemmung"})
  (:Bauteiltyp {id: "Decke"})
  (:Bauteiltyp {id: "Fassade"})
  (:Bauteiltyp {id: "Fenster"})
  (:Bauteiltyp {id: "Fundament"})
  (:Bauteiltyp {id: "Gelaender"})
  (:Bauteiltyp {id: "Stuetze"})
  (:Bauteiltyp {id: "Technik"})
  (:Bauteiltyp {id: "Traeger"})
  (:Bauteiltyp {id: "Treppe"})
  (:Bauteiltyp {id: "Tuer"})
  (:Bauteiltyp {id: "Wand"})

:Material
  (:Material {id: "Aluminium"})
  (:Material {id: "Beton"})
  (:Material {id: "Daemmstoff"})
  (:Material {id: "Glas"})
  (:Material {id: "Gusseisen"})
  (:Material {id: "Holz"})
  (:Material {id: "Keramik"})
  (:Material {id: "Kunststoff"})
  (:Material {id: "Lehm"})
  (:Material {id: "Naturstein"})
  (:Material {id: "Recyclingbeton"})
  (:Material {id: "Stahl"})
  (:Material {id: "Stahlbeton"})
  (:Material {id: "Stroh"})
  (:Material {id: "Ziegel"})

:Bauteilebene
  (:Bauteilebene {id: "Bauteilgruppe"})
  (:Bauteilebene {id: "Einzelbauteil"})
  (:Bauteilebene {id: "Gebaeudeteil"})
  (:Bauteilebene {id: "Materialcharge"})
  (:Bauteilebene {id: "Oberflaechenschicht"})
  (:Bauteilebene {id: "System"})

:Bauteilzustand
  (:Bauteilzustand {id: "Beschaedigt"})
  (:Bauteilzustand {id: "Geprueft"})
  (:Bauteilzustand {id: "Intakt"})
  (:Bauteilzustand {id: "Kontaminiert"})
  (:Bauteilzustand {id: "Korrodiert"})
  (:Bauteilzustand {id: "Patiniert"})
  (:Bauteilzustand {id: "Restlebensdauer_Bekannt"})
  (:Bauteilzustand {id: "Restlebensdauer_Unklar"})
  (:Bauteilzustand {id: "Ungeprueft"})

:Funktionswechsel
  (:Funktionswechsel {id: "Dekorative_Funktion"})
  (:Funktionswechsel {id: "Gleiche_Funktion"})
  (:Funktionswechsel {id: "Konstruktive_Funktion"})
  (:Funktionswechsel {id: "Neue_Funktion"})
  (:Funktionswechsel {id: "Technische_Funktion"})
  (:Funktionswechsel {id: "Unbekannt"})

:Verbindungstechnik
  (:Verbindungstechnik {id: "Geschraubt"})
  (:Verbindungstechnik {id: "Geschweisst"})
  (:Verbindungstechnik {id: "Gesteckt"})
  (:Verbindungstechnik {id: "Geklebt"})
  (:Verbindungstechnik {id: "Vergossen"})
  (:Verbindungstechnik {id: "Klemmverbindung"})

:Bauweise
  (:Bauweise {id: "Fertigteilbauweise"})
  (:Bauweise {id: "Holzbauweise"})
  (:Bauweise {id: "Hybridbauweise"})
  (:Bauweise {id: "Massivbauweise"})
  (:Bauweise {id: "Ortbetonbauweise"})
  (:Bauweise {id: "Stahlbauweise"})

:Bausystem
  (:Bausystem {id: "Betonfertigteil_System"})
  (:Bausystem {id: "Holzrahmenbau"})
  (:Bausystem {id: "Holz_Skelettbau"})
  (:Bausystem {id: "Plattenbau"})
  (:Bausystem {id: "Stahl_Skelettbau"})

:Tragwerksprinzip
  (:Tragwerksprinzip {id: "Fachwerk"})
  (:Tragwerksprinzip {id: "Skeletttragwerk"})
  (:Tragwerksprinzip {id: "Wandtragwerk"})
  (:Tragwerksprinzip {id: "Wand_Kern_Tragwerk"})

:Reversibilitaet
  (:Reversibilitaet {id: "Reversibel"})
  (:Reversibilitaet {id: "Teilweise_reversibel"})
  (:Reversibilitaet {id: "Irreversibel"})
  (:Reversibilitaet {id: "Unbekannt"})

:Status
  (:Status {id: "Geplant"})
  (:Status {id: "In_Bau"})
  (:Status {id: "Realisiert"})
  (:Status {id: "Prototyp"})
  (:Status {id: "Rueckgebaut"})
  (:Status {id: "Nicht_Realisiert"})
  (:Status {id: "Unklar"})

:WiederverwendungsArt
  (:WiederverwendungsArt {id: "Bestandserhalt_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Kein_Direct_Reuse_Nachweis", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Moebel_Dekoration_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Recycling_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Reuse_Anteil_Unklar", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Ungebaut_Nicht_Realisierte_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt {id: "wiederverwendet", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "original", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "hybrid", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "Bestandserhalt_Weiterbauen", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "In_situ_Wiederverwendung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Direkte_Wiederverwendung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Wiederverwendung_nach_Aufarbeitung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Umnutzung_Repurposing", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Kaskade_Downcycling_Bauteilebene", axis: "reuse_strategie"})

:Ressourcenquelle
  (:Ressourcenquelle {id: "Baustelle"})
  (:Ressourcenquelle {id: "Bauteilboerse"})
  (:Ressourcenquelle {id: "Donorgebaeude"})
  (:Ressourcenquelle {id: "Donor_Infrastruktur"})
  (:Ressourcenquelle {id: "Haendler"})
  (:Ressourcenquelle {id: "Lager"})
  (:Ressourcenquelle {id: "Materialstockpile"})
  (:Ressourcenquelle {id: "Produktionsueberschuss"})
  (:Ressourcenquelle {id: "Unbekannt"})

:Beschaffungsweg
  (:Beschaffungsweg {id: "Ausschreibung"})
  (:Beschaffungsweg {id: "Bauteilboerse"})
  (:Beschaffungsweg {id: "Digitale_Plattform"})
  (:Beschaffungsweg {id: "Direktvermittlung"})
  (:Beschaffungsweg {id: "Eigenbestand"})
  (:Beschaffungsweg {id: "Informelles_Netzwerk"})
  (:Beschaffungsweg {id: "Rueckbauprojekt"})
  (:Beschaffungsweg {id: "Spende"})

:Prozessphase
  (:Prozessphase {id: "Aufbereitung"})
  (:Prozessphase {id: "Betrieb"})
  (:Prozessphase {id: "Dokumentation"})
  (:Prozessphase {id: "Identifikation"})
  (:Prozessphase {id: "Lagerung"})
  (:Prozessphase {id: "Planung"})
  (:Prozessphase {id: "Pruefung"})
  (:Prozessphase {id: "Rueckbau"})
  (:Prozessphase {id: "Transport"})
  (:Prozessphase {id: "Wiedereinbau"})

:Rueckbauverfahren
  (:Rueckbauverfahren {id: "Ausbau_von_Bauteilen"})
  (:Rueckbauverfahren {id: "Betonfraesen"})
  (:Rueckbauverfahren {id: "Demontage"})
  (:Rueckbauverfahren {id: "Selektiver_Rueckbau"})
  (:Rueckbauverfahren {id: "Zerstoerungsarme_Bergung"})

:Aufbereitungsverfahren
  (:Aufbereitungsverfahren {id: "Drahtglasschneiden"})
  (:Aufbereitungsverfahren {id: "Entmoertelung_von_Fliesen"})
  (:Aufbereitungsverfahren {id: "Holzaufbereitung"})
  (:Aufbereitungsverfahren {id: "Leuchten_Refurbishment"})
  (:Aufbereitungsverfahren {id: "Qualitaetssicherung"})
  (:Aufbereitungsverfahren {id: "Reinigung"})
  (:Aufbereitungsverfahren {id: "Rekonditionierung"})
  (:Aufbereitungsverfahren {id: "Remanufacturing"})
  (:Aufbereitungsverfahren {id: "Reparatur"})
  (:Aufbereitungsverfahren {id: "Verstaerkung"})
  (:Aufbereitungsverfahren {id: "Zuschnitt"})

:Logistik
  (:Logistik {id: "Bauteiltracking"})
  (:Logistik {id: "Just_in_Time"})
  (:Logistik {id: "Lagerflaeche"})
  (:Logistik {id: "Lagerung"})
  (:Logistik {id: "Lokale_Wiederverwendung"})
  (:Logistik {id: "Materialmatching"})
  (:Logistik {id: "Materialverfuegbarkeit"})
  (:Logistik {id: "Transport"})
  (:Logistik {id: "Transportdistanz"})
  (:Logistik {id: "Zwischenlagerung"})

:Methode
  (:Methode {id: "Abrissmonitoring"})
  (:Methode {id: "Bauteilkatalogisierung"})
  (:Methode {id: "Building_Material_Scouting"})
  (:Methode {id: "Design_for_Disassembly"})
  (:Methode {id: "Form_Follows_Availability"})
  (:Methode {id: "Materialinventur"})
  (:Methode {id: "Pre_Deconstruction_Audit"})
  (:Methode {id: "ReUse_Assessment"})
  (:Methode {id: "ReUse_Ausschreibung"})
  (:Methode {id: "Reversibilitaet"})
  (:Methode {id: "Urban_Mining"})
  (:Methode {id: "Wiederverwendungskriterien"})
  (:Methode {id: "Zirkulaere_Ausschreibung"})

:Huerde
  (:Huerde {id: "Akzeptanzproblem"})
  (:Huerde {id: "Anschlussproblem"})
  (:Huerde {id: "Aufbereitungsaufwand"})
  (:Huerde {id: "Ausschreibungsproblem"})
  (:Huerde {id: "Bauproduktstatus"})
  (:Huerde {id: "Brandschutzkonflikt"})
  (:Huerde {id: "Bruch_Beschaedigungsrisiko"})
  (:Huerde {id: "Datenluecke"})
  (:Huerde {id: "Dauerhaftigkeit_Restlebensdauer"})
  (:Huerde {id: "Entwurfsbindung"})
  (:Huerde {id: "Fehlende_Datenstandards"})
  (:Huerde {id: "Fehlende_Lagerflaeche"})
  (:Huerde {id: "Fehlende_Standardisierung"})
  (:Huerde {id: "Haftung"})
  (:Huerde {id: "Heterogenitaet_Chargen"})
  (:Huerde {id: "Hygieneanforderung"})
  (:Huerde {id: "Kompatibilitaetsproblem"})
  (:Huerde {id: "Materialqualitaet_Unklar"})
  (:Huerde {id: "Mengenunsicherheit"})
  (:Huerde {id: "Schadstoffbelastung"})
  (:Huerde {id: "Technische_Freigabe"})
  (:Huerde {id: "Terminunsicherheit"})
  (:Huerde {id: "Toleranzen"})
  (:Huerde {id: "Unkonventionelles_Material"})
  (:Huerde {id: "Verfuegbarkeitsproblem"})
  (:Huerde {id: "Witterung_Feuchte"})
  (:Huerde {id: "Zustand_Unklar"})
  (:Huerde {id: "Asbest", kategorie: "Schadstoff"})
  (:Huerde {id: "Bleifarbe", kategorie: "Schadstoff"})
  (:Huerde {id: "Holzschutzmittel", kategorie: "Schadstoff"})
  (:Huerde {id: "PAK", kategorie: "Schadstoff"})
  (:Huerde {id: "PCB", kategorie: "Schadstoff"})

:PruefungNachweis
  (:PruefungNachweis {id: "Abbrandbemessung"})
  (:PruefungNachweis {id: "Brandschutznachweis"})
  (:PruefungNachweis {id: "Eignungspruefung_Baulehm"})
  (:PruefungNachweis {id: "Geometrische_Vermessung"})
  (:PruefungNachweis {id: "Materialpruefung"})
  (:PruefungNachweis {id: "Schadstoffscreening"})
  (:PruefungNachweis {id: "Schweissbarkeitspruefung"})
  (:PruefungNachweis {id: "Sichtpruefung"})
  (:PruefungNachweis {id: "Statische_Nachweisfuehrung"})
  (:PruefungNachweis {id: "Zugversuch"})
  (:PruefungNachweis {id: "Zustandsbewertung"})

:Leistungsanforderung
  (:Leistungsanforderung {id: "Brandschutz"})
  (:Leistungsanforderung {id: "Brandschutzanforderung"})
  (:Leistungsanforderung {id: "Dauerhaftigkeit"})
  (:Leistungsanforderung {id: "F90"})
  (:Leistungsanforderung {id: "Feuchteschutz"})
  (:Leistungsanforderung {id: "Feuerwiderstand"})
  (:Leistungsanforderung {id: "R90"})
  (:Leistungsanforderung {id: "REI90"})
  (:Leistungsanforderung {id: "Rueckbaubarkeit"})
  (:Leistungsanforderung {id: "Schadstofffreiheit"})
  (:Leistungsanforderung {id: "Schallschutz"})
  (:Leistungsanforderung {id: "Tragfaehigkeit"})
  (:Leistungsanforderung {id: "Waermeschutz"})

:Norm
  (:Norm {id: "DIN_18940"})
  (:Norm {id: "DIN_EN_15804"})
  (:Norm {id: "DIN_EN_15978"})
  (:Norm {id: "EN_1090"})
  (:Norm {id: "ISO_14040"})
  (:Norm {id: "ISO_14044"})
  (:Norm {id: "ISO_20887"})

:RechtlicheBedingung
  (:RechtlicheBedingung {id: "Bauordnungsrecht"})
  (:RechtlicheBedingung {id: "EU_Taxonomie"})
  (:RechtlicheBedingung {id: "Gewaehrleistung"})
  (:RechtlicheBedingung {id: "Produkthaftung"})
  (:RechtlicheBedingung {id: "Vergaberecht"})
  (:RechtlicheBedingung {id: "Zulassung_im_Einzelfall"})

:Nutzung
  (:Nutzung {id: "Buero"})
  (:Nutzung {id: "Gewerbe"})
  (:Nutzung {id: "Infrastruktur"})
  (:Nutzung {id: "Kultur"})
  (:Nutzung {id: "Lager_Depot"})
  (:Nutzung {id: "Mischnutzung"})
  (:Nutzung {id: "Schule_Bildung"})
  (:Nutzung {id: "Sozialbau"})
  (:Nutzung {id: "Wohnen"})

:BauaufgabeIntervention
  (:BauaufgabeIntervention {id: "Aufstockung"})
  (:BauaufgabeIntervention {id: "Erweiterung"})
  (:BauaufgabeIntervention {id: "Fit_out"})
  (:BauaufgabeIntervention {id: "Neubau"})
  (:BauaufgabeIntervention {id: "Rueckbau"})
  (:BauaufgabeIntervention {id: "Sanierung"})
  (:BauaufgabeIntervention {id: "Translozierung"})
  (:BauaufgabeIntervention {id: "Umbau"})
  (:BauaufgabeIntervention {id: "Umnutzung"})
  (:BauaufgabeIntervention {id: "Wiederaufbau"})

:Entwurfsentscheidung
  (:Entwurfsentscheidung {id: "Etagenhoehe_durch_Bauteilmass"})
  (:Entwurfsentscheidung {id: "Fassadenschicht_als_Toleranzpuffer"})
  (:Entwurfsentscheidung {id: "Doppelfenster_als_Kastenfenster"})
  (:Entwurfsentscheidung {id: "Achsraster_nach_Bestand"})
  (:Entwurfsentscheidung {id: "Grundriss_nach_Bauteillaenge"})
  (:Entwurfsentscheidung {id: "Deckenhoehe_nach_Traegerhoehe"})
  (:Entwurfsentscheidung {id: "Anschlussdetail_angepasst"})
  (:Entwurfsentscheidung {id: "Erschliessungskern_verschoben"})

:Land
  (:Land {id: "Schweiz", iso_country: "CH"})
  (:Land {id: "Deutschland", iso_country: "DE"})

:Stadt
  (:Stadt {id: "Winterthur"})
  (:Stadt {id: "Muenster"})

:Akteurrolle
  (:Akteurrolle {id: "Bauherrschaft_Nutzung"})
  (:Akteurrolle {id: "Planung_Gestaltung"})
  (:Akteurrolle {id: "Tragwerk_Fassade"})
  (:Akteurrolle {id: "TGA_Sicherheit"})
  (:Akteurrolle {id: "Ausfuehrung_Logistik"})
  (:Akteurrolle {id: "Beratung_Forschung"})
  (:Akteurrolle {id: "Qualitaetssicherung"})
  (:Akteurrolle {id: "Koordination"})

:Datenqualitaet
  (:Datenqualitaet {id: "Belegt"})
  (:Datenqualitaet {id: "Geschaetzt"})
  (:Datenqualitaet {id: "Nicht_Belegt"})
  (:Datenqualitaet {id: "Primaerquelle"})
  (:Datenqualitaet {id: "Sekundaerquelle"})
  (:Datenqualitaet {id: "Unbekannt"})
  (:Datenqualitaet {id: "Widerspruechlich"})

:Datenmodell
  (:Datenmodell {id: "Bauteil_ID"})
  (:Datenmodell {id: "IFC"})
  (:Datenmodell {id: "Klassifikation"})
  (:Datenmodell {id: "Materialdatenbank"})
  (:Datenmodell {id: "Materialpass_Schema"})
  (:Datenmodell {id: "Ontologie"})
  (:Datenmodell {id: "Taxonomie"})

:Tooltyp
  (:Tooltyp {id: "Bauteilboerse"})
  (:Tooltyp {id: "Materialdatenbank"})
  (:Tooltyp {id: "Materialkataster"})

:ZertifizierungBewertungssystem
  (:ZertifizierungBewertungssystem {id: "BREEAM"})
  (:ZertifizierungBewertungssystem {id: "DGNB"})
  (:ZertifizierungBewertungssystem {id: "LEED"})
  (:ZertifizierungBewertungssystem {id: "Paris_Proof"})
  (:ZertifizierungBewertungssystem {id: "WELL"})

:Wirtschaft
  (:Wirtschaft {id: "Finanzierung"})
  (:Wirtschaft {id: "Geschaeftsmodell"})
  (:Wirtschaft {id: "Kostenvergleich"})
  (:Wirtschaft {id: "Lebenszykluskosten"})
  (:Wirtschaft {id: "Preisbildung"})
  (:Wirtschaft {id: "Restwert"})

:Programm
  (:Programm {id: "BBSM", programm_typ: "foerderung"})
  (:Programm {id: "FCRBE", programm_typ: "foerderung"})
  (:Programm {id: "PREUSE", programm_typ: "foerderung"})
  (:Programm {id: "Reallabor_Be_Ware", programm_typ: "foerderung"})
  (:Programm {id: "Zukunftbau", programm_typ: "foerderung"})
  (:Programm {id: "Foerderprogramm", programm_typ: "forschungskontext"})
  (:Programm {id: "Forschungsprojekt", programm_typ: "forschungskontext"})
  (:Programm {id: "Kommunales_Programm", programm_typ: "forschungskontext"})
  (:Programm {id: "Pilotprojekt", programm_typ: "forschungskontext"})
  (:Programm {id: "Reallabor", programm_typ: "forschungskontext"})
  (:Programm {id: "Wettbewerb", programm_typ: "forschungskontext"})
```
