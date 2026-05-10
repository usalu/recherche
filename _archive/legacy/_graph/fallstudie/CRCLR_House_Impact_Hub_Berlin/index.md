---
id: "CRCLR_House_Impact_Hub_Berlin"
entity: "fallstudie"
node_kind: "core"
migration_status: "migrated_phase4_case_graph"
title: "CRCLR House / Impact Hub Berlin – Fallstudie Direct Reuse"
bauobjekt:
  - "CRCLR_House_Impact_Hub_Berlin"
legacy_paths:
  - "Gebäude\\CRCLR_House_Impact_Hub_Berlin.md"
projekt:
  - "CRCLR_House_Impact_Hub_Berlin"
reuse_chain_detected: "False"
---
# CRCLR House / Impact Hub Berlin – Fallstudie Direct Reuse

## Migration

- Fallstudie ID: CRCLR_House_Impact_Hub_Berlin
- Legacy source count: 1
- Generated project: CRCLR_House_Impact_Hub_Berlin
- Generated bauobjekt: CRCLR_House_Impact_Hub_Berlin
- Extracted reuse_einsatz rows: 7
- Extracted datenpunkt rows: 9
- Extracted entity mapping rows: 14
- Reuse chain detected: False

## Legacy Content

### Legacy Source: Gebäude\CRCLR_House_Impact_Hub_Berlin.md

- Map action: split_into_case_graph
- Primary target: fallstudie/CRCLR_House_Impact_Hub_Berlin
- Secondary targets: projekt/CRCLR_House_Impact_Hub_Berlin; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# CRCLR House / Impact Hub Berlin – Fallstudie Direct Reuse

Hinweis: Angaben wurden quellenkritisch übernommen. Nicht belegte Felder sind als „unbekannt“ markiert; normale Sanierung/Bestandserhalt wird nicht als Direct Reuse gezählt.

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Relevanter gebauter Transformationsfall mit tatsächlicher Wiederverwendung fester Bau- und Tragwerkselemente. Besonders relevant sind die aus dem Hallendach gewonnenen Stahlpfetten/-träger, die als Treppenwangen bzw. tragende Elemente wieder eingesetzt wurden. Der reine Erhalt der ehemaligen Halle wird nicht als Direct Reuse gewertet.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
| --- | --- | --- | --- | --- | --- |
| Fallstudie | CRCLR House / Impact Hub Berlin | untersuchter Fall | CMS; ZRS; LXSY | belegt | Transformation und Aufstockung |
| Ort | Berlin-Neukölln, Rollbergstraße 26 / 28a | Standort | CMS; ZRS; AK Berlin | teilweise belegt | Quellen nennen teils 26, teils 28a |
| Gebäude | ehemalige Lager-/Fassladehalle auf dem Kindl-Areal | Bestandsgebäude | ZRS; BauNetz Wissen | belegt | Bestandserhalt allein nicht gezählt |
| Projekt | Umbau, Aufstockung und Impact Hub-Ausbau | neue Nutzung | CMS; LXSY; ZRS | belegt | Mixed use: Coworking, Workshops, Wohnen |
| People | TRNSFRM eG; Die Zusammenarbeiter; LXSY; ZRS; Solares Bauen; eZeit; brandkontrolle; Akustik-Ingenieurbüro Moll | Akteure | ZRS; CMS; LXSY | belegt |  |
| Bauteil | Stahlpfetten/-träger aus dem Hallendach | wiederverwendete tragende Bauteile | ZRS; BauNetz Wissen; nbau | belegt | als Treppenwangen; Gewächshausnutzung quellenabhängig |
| Bauteil | Holz-Alu-Fenster / Außenfenster | wiederverwendete Hüllbauteile | nbau; CMS | teilweise belegt | neu verglast; genaue Anzahl unbekannt |
| Bauteil | Sanitärobjekte, Vorhangfassadenelemente, Blech/Glas, Türen, Bodenplatten | weitere wiederverwendete Bauteile | CMS; nbau; LXSY | teilweise belegt | Einbauumfang nicht überall eindeutig |
| Prüfung | Zugversuche, chemische Analyse, Schweißbarkeit, Korrosionsschutz | Qualifizierung Stahlreuse | nbau; BauNetz Wissen; CMS | belegt | jeder vierte Träger als Laborprobe laut BauNetz Wissen |
| Hürde | Gewährleistung / fehlendes Werkszeugnis | rechtlich-technische Hürde | nbau; CMS | belegt | Rechtsrahmen als Datenlücke |
| Methode | Materialjagd, Materialpässe, reversible Fügung, sichtbare TGA | zirkulärer Planungsprozess | CMS; LXSY; nbau | belegt |  |
| Kennwert | 120 Stahlträger bis 18 m | Bauteilumfang | BauNetz Wissen | teilweise belegt | nicht alle wurden installiert |
| Kennwert | ca. 70 % reused/recycled/upcycled im Innenausbau | Innenausbau | CMS | teilweise belegt | nicht vollständig Direct Reuse |
| Kennwert | BGF 6.600 m² / 7.603 m² / Größe 4.871 m² | Flächenangabe | ZRS; ZAB; CMS | unklar | Quellenkonflikt |


### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
| --- | --- | --- | --- |
| Quellenkonflikt | Mehrere belastbare Quellen geben unterschiedliche Flächen/Umfänge an. | BGF 6.600 m², 7.603 m², 4.871 m² | Kennwert, Dokument |
| Reuse-Gewährleistung | Für geprüfte Altbauteile fehlt oft ein eindeutiger Rechts-/Haftungsrahmen. | Stahlträger ohne Werkszeugnis | Recht, Prüfung, Wirtschaft |
| Self-Harvesting | Bauteile stammen aus dem eigenen Bestandsrückbau und werden im selben Projekt neu eingesetzt. | Dachstahl als Treppenwange | Abbruchmethode, Bauteil, Reuse-Strategie |


## 3. FALLSTUDIE

- **Name:** CRCLR House / Impact Hub Berlin
- **Ort:** Berlin-Neukölln, Rollbergstraße 26 / 28a
- **Gebäude:** ehemalige Lager-/Fassladehalle auf dem Kindl-Areal
- **Projekt:** Umbau, Aufstockung und Ausbau zu Coworking, Werkstätten, Events und Wohnen
- **Beteiligte People / Akteure:** TRNSFRM eG; Die Zusammenarbeiter; LXSY Architektur; ZRS Ingenieure; Solares Bauen; eZeit; brandkontrolle; Akustik-Ingenieurbüro Moll
- **Architekt:** Die Zusammenarbeiter GmbH; LXSY Architektur für Impact-Hub-Innenausbau; TRNSFRM eG in Quellen ebenfalls als Architektur/Bauherr genannt
- **Tragwerksplaner:** ZRS Ingenieure
- **Bauherr:** TRNSFRM eG
- **Zeitraum:** Bauzeit 2020–2023; Impact Hub seit 2022/2023 in Nutzung je nach Quelle
- **Ursprüngliche Nutzung:** Lager-/Fassladehalle, ehemaliges Kindl-Brauerei-Areal
- **Neue Nutzung:** Coworking, Werkstätten, Studios, Events, Wohnen
- **Fläche / Maßstab:** Quellenkonflikt: 4.871 m², 6.600 m² BGF, 7.603 m² BGF; ZRS nennt 4.690 m² Nutzfläche
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Akteure, Reuse-Strategie und Stahlprüfungen; unsicher bei exakten Mengen, Flächen und realisiertem Gewächshaus-/Balkonumfang

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; in-situ transformiert; Bauteilwiederverwendung; adaptive reuse; Design for Disassembly ergänzend
- **Hauptniveau:** Tragwerk / räumlicher Innenausbau / Gebäudehülle / technische Gebäudeausrüstung
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der Bestandserhalt der Halle zählt nicht als Wiederverwendung im engeren Sinn. Gezählt werden nur demontierte und neu eingesetzte Bauteile wie Stahlpfetten als Treppenwangen, wiederverwendete Fenster, Sanitär- und Fassadenelemente.
- **Warum ist der Fall relevant?** Er zeigt die Schnittstelle von Bestandsumbau, Bauteilprüfung, Materialpässen, Reuse-Innenausbau und tragender Wiederverwendung von Altstahl.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Stahlpfetten / I-Träger | Baustahl | Bestandsdach der Halle | Dachtragwerk | Treppenwangen / tragende Treppenstruktur; teils Gewächshausdach geplant/angegeben | 120 Träger bis 18 m laut BauNetz Wissen; installierter Anteil unbekannt | ja | ja | nein | nein | demontiert, Proben, Zugversuch, chemische Analyse, entrostet, Korrosionsschutz | geschweißt/verschraubt: unbekannt | Zugversuche, chemische Analyse, Schweißbarkeit | Tragfähigkeit; Schweißbarkeit; Korrosionsschutz | unbekannt | fehlendes Werkszeugnis; Gewährleistung; Zeit/Kosten | ZRS; BauNetz Wissen; nbau | installierte Menge, genaue Stahlgüte |
| Stahlfachwerkträger | Baustahl | Bestandsdach der Halle | Dachtragwerk | Gewächshausdach laut CMS/nbau; laut BauNetz Wissen wurden Zusatzbauten gestrichen | unbekannt | teilweise/unbekannt | ja | nein | nein | demontiert und geprüft | unbekannt | Zugversuche/chemische Analyse allgemein | Tragfähigkeit | unbekannt | Quellenkonflikt zum realisierten Umfang | CMS; ZRS; BauNetz Wissen | Realisierungsstand |
| Holz-Alu-Fenster / Außenfenster | Holz-Alu/Glas | demontierte Fenster aus Versicherungsschaden / externe Quelle | Fenster | Fassade / Belichtung | unbekannt | nein | nein | ja | nein | neu verglast laut nbau | unbekannt | unbekannt | Wärmeschutz, Schallschutz, Dichtigkeit | unbekannt | Brandschutz/Energieanforderungen komplizierter als Sanitär | nbau; CMS | Anzahl, U-Wert |
| Sanitärobjekte / Duschtassen | Keramik/Sanitärmaterial | Standardisierte Rückbauware | Sanitär | Sanitär | unbekannt | nein | nein | nein | ja | Reinigung/Aufbereitung unbekannt | Standardanschlüsse vermutet | unbekannt | Hygiene, Funktion | unbekannt | geringer als Fenster/Türen | CMS; nbau | Anzahl |
| Vorhangfassadenelemente, Blech, Glas | Metall/Glas | Rückbau/Bestand | Fassadenelemente | Fassade/Innenausbau | unbekannt | nein | teilweise | ja | nein | unbekannt | lösbar geplant | unbekannt | Brand/Energie/Schallschutz | unbekannt | unbekannt | nbau; CMS | Einbauort |
| Holzgalerie / Innenausbau | Holz, teils Reststücke/wiederverwendet | Abrissbaustellen, Messen, Museen, Lagerbestände, Schreinereireste | diverse | Galerie/Innenausbau Impact Hub | ca. 70 % reused/recycled/upcycled laut CMS; direkte Reuse-Anteile unbekannt | teilweise | ja | nein | nein | Zuschnitt; Holzständerraster 62,5 cm | lösbar/einfache Standards | unbekannt | Brandschutz; Nutzung; Robustheit | unbekannt | Materialverfügbarkeit | LXSY; BauNetz Wissen; CMS | exakte Bauteile |
| TGA sichtbar geführt | diverse | neu/Bestand unbekannt | Gebäudetechnik | wartbare, demontierbare TGA | unbekannt | nein | nein | nein | ja | auf Putz/sichtbar | zugänglich | unbekannt | Wartung, Brandschutz | unbekannt | Koordination | nbau; ZRS | Reuse-Anteil |


## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bestandsaufnahme | Bestandshalle und Dachstahl als Ressource identifiziert | TRNSFRM eG; Die Zusammenarbeiter; ZRS | Materialjagd / Gebäudestock als Materialbank | Materialpässe erwähnt | unbekannt | unbekannt | unbekannt | vor Ort | Bestand beschädigt/belastet | Verstärkung und selektive Wiederverwendung | CMS; BauNetz Wissen |
| Bauteilinventar | Wiederverwendungsregeln für Fenster, Stahl, Fassadenteile, Sanitär festgelegt | Planungsteam | zirkuläre Planungsregeln | Materialpässe | unbekannt | unbekannt | unbekannt | Baustellenlagerung | Verfügbarkeit | frühe Beschaffung | nbau; LXSY |
| Schadstoffprüfung | eingebautes Holz belastet und nicht wiederverwendbar | Planungsteam | Prüfung Bestand | unbekannt | unbekannt | Aussortierung | unbekannt | unbekannt | belastetes Holz | nicht wiederverwenden | BauNetz Wissen |
| Rückbau | Stahldach demontiert; Mauerwerk teils ergänzt | Bau / Planung | selektiver Rückbau | unbekannt | Demontage Dachtragwerk | unbekannt | visuelle/technische Prüfung | Baustellenlogistik | Bauteilschonung | Demontage vor Neuplanung | ZRS; nbau |
| Ausbau | Stahlträger ausgebaut, Proben entnommen | Planung; Labor | Probe jedes vierten Trägers laut BauNetz | Laborprüfung | selektiv | Entrostung/Korrosionsschutz | Zugversuch, chemische Analyse | Labortransport | Zeit/Kosten | standardisierte Prüfstrategie | BauNetz Wissen; nbau |
| Transport | externe Fenster/Fassadenteile zur Baustelle gebracht | TRNSFRM/Projektteam | Materialbeschaffung | unbekannt | unbekannt | Refurbishment | unbekannt | unbekannt | Transport-/Lagerbedarf | frühe Materialjagd | CMS |
| Lagerung | demontierte/gebrauchte Bauteile vor Wiedereinbau gelagert | Projektteam | Baustellenlager | unbekannt | unbekannt | unbekannt | unbekannt | vor Ort/unbekannt | Platzbedarf | unbekannt | CMS; LXSY |
| Aufbereitung | Stahl entrostet; Fenster neu verglast; Innenausbauteile angepasst | Planer; Handwerk; Labor | Reparatur/Refurbishment | unbekannt | unbekannt | Entrostung; Neuverglasung; Zuschnitt | Schweißbarkeit/Festigkeit | unbekannt | Gewährleistung | Prüfungen statt Werkszeugnis | nbau; BauNetz Wissen |
| Planung | Aufstockung an Bestandstragwerk angepasst; lösbare Verbindungen | Die Zusammenarbeiter; ZRS | Design for disassembly + Direct Reuse | unbekannt | unbekannt | unbekannt | Brandschutzkonzept | unbekannt | Gebäudeklasse/Brandschutz | zwei Baukörper, zwei Rettungswege, keine innere Brandwand | ZRS; nbau |
| Genehmigung | F90/Brandschutzanforderung ohne Kapselung gelöst | Brandschutzplanung; ZRS | organisatorisch/konstruktiv | unbekannt | unbekannt | unbekannt | Brandschutznachweis | unbekannt | Brandschutz im Holzbau | Abbrandbemessung tragender Hölzer | ZRS |
| Wiedereinbau | Stahl als Treppenwangen; Fenster/Fassade/Innenausbau eingesetzt | Bauunternehmen/Handwerk | sichtbares, additiv gefügtes Bauen | Materialpässe | unbekannt | Montage | Abnahmen unbekannt | Baustelle | Schnittstellen | einfache Standards | ZRS; LXSY; CMS |
| Monitoring | Materialpässe für spätere Wiederverwendung erwähnt | LXSY/Projektteam | Dokumentation | Materialpässe | unbekannt | unbekannt | unbekannt | digital/analog unbekannt | Datenpflege | Bauteile repurposable nach Demontage | LXSY |


## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Tragwerkssystem | Bestandshalle verstärkt; Aufstockung Holzrahmen/BSH/BSP; neue Stahlbetonstützen/Decke; wiederverwendeter Stahl als Treppentragwerk | Tragfähigkeit Bestand + Aufstockung | unbekannt | statische Planung; Zugversuche | Altstahl ohne Werkszeugnis | Laborprüfung; Korrosionsschutz | ZRS; nbau; BauNetz Wissen |
| Lastabtragung | Neue Aufstockung passt sich an vorhandene Tragstruktur an; teils Holzstützen ungünstig platziert | Lastpfade aus Bestand und Neubau | unbekannt | Tragwerksplanung | Bestandsraster schränkt Entwurf ein | Anpassung der Grundrisse und Stützenpositionen | BauNetz Wissen; ZRS |
| Verbindung | Neue Bauteile mit lösbaren Verbindungen; nicht kleben/additiv fügen als Planungsregel | Demontierbarkeit | unbekannt | unbekannt | konventionelle Details nicht immer zirkulär | reversible Fügungen | nbau; ZRS |
| Brandschutz | F90-Anforderung; Holzteile nicht gekapselt, sondern auf Abbrand bemessen; zwei Rettungswege | F90, Rettungswege | unbekannt | Brandschutzplanung | Sonderbau/GK5 | zwei Baukörper, Gewächshaus/Trennung, keine innere Brandwand | ZRS; nbau |
| Schallschutz | Akustikplanung durch Akustik-Ingenieurbüro Moll; Details unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | ZRS |
| Feuchte | Strohballen-/Holzbau erfordert Feuchteschutz; Details unbekannt | unbekannt | unbekannt | unbekannt | Feuchterisiko biogener Materialien | unbekannt | ZRS |
| Wärmeschutz | Wiederverwendete Fenster neu verglast; Holz-/Strohfassade | Energieanforderungen | unbekannt | unbekannt | Altfenster erfüllen Anforderungen nicht automatisch | Neuverglasung | nbau; ZRS |
| Wärmebrücken | Details unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Luftdichtheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| TGA-Integration | Technik sichtbar/auf Putz und zugänglich verlegt | Wartung, Austauschbarkeit | unbekannt | unbekannt | Koordination mit Bestand | zugängliche Führung | nbau; ZAB |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Altstahl entrostet und korrosionsgeschützt; Fenster neu verglast | Dauerhaftigkeit Reuse-Bauteile | unbekannt | chemische Analyse, Zugversuche | unbekannte Restlebensdauer | Aufbereitung und Prüfung | nbau |
| Wartung | sichtbare TGA erleichtert Wartung | Zugänglichkeit | unbekannt | unbekannt | unbekannt | auf Putz | nbau; ZAB |
| Zulassung | Altstahl ohne Werkszeugnis; Materialprüfungen ersetzen Nachweis teilweise | Bauaufsichtliche Akzeptanz | unbekannt | Laborprüfung | fehlender Standardprozess | Prüfung/Einzelnachweis | nbau; CMS |
| Haftung | Gewährleistung für wiederverwendete Stahlbauteile nicht klar geregelt | Haftungsrahmen | unbekannt | unbekannt | rechtliche Unsicherheit | Rechtsrahmen nötig | nbau; CMS |


## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
| --- | --- | --- | --- | --- | --- | --- |
| BGF / Fläche | 6.600 / 7.603 / 4.871 | m² | Projektangaben verschiedener Quellen | Gebäude | ZRS / ZAB / CMS | unklar |
| Nutzfläche | 4.690; davon 2.521 Bestand, 2.169 Aufstockung | m² | Projektangabe | Gebäude | ZRS | belegt |
| Grundstücksgröße | 2.158 | m² | Projektangabe | Grundstück | ZRS | belegt |
| Bauzeit | 2020–2023 | Jahre | Projektangabe | Bauphase | ZRS | belegt |
| Stahlträger aus Dachrückbau | 120; bis 18 m Länge | Stück / m | Fallbericht | Dachstahl | BauNetz Wissen | teilweise belegt |
| Wiederverwendete Masse | unbekannt | t | unbekannt | unbekannt | unbekannt | unbekannt |
| Innenausbau reuse/recycled/upcycled | ca. 70 | % | Projektangabe | Innenausbau Impact Hub | CMS | teilweise belegt |
| Eingesparter Beton | 120 | m³ | Fallbericht | neue Hallendecke | BauNetz Wissen | teilweise belegt |
| CO₂-Einsparung | unbekannt | t CO₂e | unbekannt | unbekannt | ZAB nennt CO2 reduced ohne Zahl | unbekannt |


## 9. HÜRDEN-MATRIX

| Hürde | Kategorie: technisch/rechtlich/wirtschaftlich/logistisch/gestalterisch/sozial | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Altstahl ohne Werkszeugnis | technisch/rechtlich | demontierte Bauteile haben keine heutigen Produktnachweise | Laborprüfungen nötig; Zeit/Kosten | Bauteil, Prüfung, Recht, Wirtschaft | Zugversuche, chemische Analyse, Schweißbarkeitsnachweis | Prüfpfad früh einplanen | nbau; BauNetz Wissen; CMS |
| Gewährleistung | rechtlich/wirtschaftlich | unklarer Haftungsrahmen für Reuse-Stahl | Risiko für Planer/Bauherr | Recht, Wirtschaft, Prüfung | Einzelnachweis; rechtlicher Rahmen gefordert | Reuse braucht standardisierte Haftungsmodelle | nbau; CMS |
| Bestandsraster | gestalterisch/technisch | Aufstockung muss auf vorhandenes Tragwerk reagieren | Stützen stehen teils entwerferisch ungünstig | Tragwerkssystem, Verbindung | Entwurf an Lastpfade angepasst | Bestand als Entwurfsparameter akzeptieren | BauNetz Wissen |
| Brandschutz | technisch/rechtlich | Gebäudeklasse/Sonderbau und Holzbau | hohe Nachweisanforderungen | Leistungsanforderung, Recht | zwei Baukörper, zwei Rettungswege, Abbrandbemessung | Brandschutz früh mit Reuse verknüpfen | ZRS; nbau |
| Materialverfügbarkeit | logistisch/gestalterisch | Bauteile müssen gefunden, gelagert und angepasst werden | Design muss flexibel bleiben | Logistik, Bauteil, Methode | Materialjagd und Materialpässe | Design follows availability | CMS; LXSY |


## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Materialjagd aus Bestand, Rückbauquellen, Messen, Museen, Lagerbeständen und Baustellen; teilweise Self-Harvesting.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; projektbezogene Materialbeschaffung.
- **Kostenwirkung:** unbekannt; Laborprüfung und Wiederverwendung erzeugten zusätzlichen Zeit- und Kostenaufwand.
- **Zeitwirkung:** zusätzlicher Aufwand für Prüfung, Demontage, Lagerung und Anpassung belegt; Dauer unbekannt.
- **Versicherung / Haftung:** Gewährleistung für wiederverwendete Stahlbauteile rechtlich unklar.
- **Gewährleistung:** unbekannt; als Hürde benannt.
- **Arbeitsaufwand:** erhöht durch Materialprüfung, Demontage, Aufbereitung und Innenausbau aus heterogenen Restmaterialien.
- **Lagerung:** Bauteile wurden vor Ort/baustellennah gelagert; Details unbekannt.
- **Marktbarrieren:** fehlende Standards, fehlende Produktnachweise, Planungsaufwand.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch; Stahl, sichtbare TGA und einfache Fügungen sind Teil des Ausdrucks.
- **räumliche Transformation:** eingeschossige Halle mit Galerie; Aufstockung für Wohnen und Arbeiten.
- **Atmosphäre / Ausdruck:** robust, experimentell, werkstattartig.
- **Umgang mit Spuren:** sichtbar belassene Materialbiografien; genaue konservatorische Strategie unbekannt.
- **sozialer Wert:** Hub für zirkuläre Wirtschaft, Impact-Unternehmen und gemeinschaftliches Wohnen.
- **Denkmal- oder Bestandswert:** historischer Hallenbestand als Ressource; formaler Schutz unbekannt.
- **Kritik / Grenzen:** hoher Sonderaufwand; nicht alle geplanten Reuse-Anwendungen offenbar realisiert; Quellenkonflikte.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Nicht gefunden:** Normnummern, genaue Stahlgüten, exakte Anzahl eingebauter Fenster/Sanitärteile, genaue Massen, genaue CO₂-Bilanz, Kosten, Versicherungslösung.
- **Neue Entitäten sinnvoll:** Quellenkonflikt; Reuse-Gewährleistung; Self-Harvesting.
- **Fehlende Daten:** geprüfte Bauteilliste, Materialpässe, Prüfberichte, Genehmigungsunterlagen, Gewährleistungsverträge.
- **Zu prüfende Quellen:** nbau Heft/Artikel, DBZ 05/2023, db 10/2023, Jahrbuch der Ingenieurbaukunst 2024, interne Materialpässe.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja
- **5 wichtigste Fakten:**
  1. Gebauter Umbau und Aufstockung einer ehemaligen Halle in Berlin-Neukölln.
  2. Wiederverwendete Stahlpfetten/-träger aus dem Hallendach wurden tragend als Treppenwangen genutzt.
  3. Stahlbauteile wurden durch Zugversuche und chemische Analysen qualifiziert.
  4. Innenausbau enthält hohe Anteile wiederverwendeter/recycelter/upgecycelter Materialien.
  5. Der reine Erhalt der Halle ist Bestandserhalt und nicht der Bewertungsgrund.
- **5 wichtigste Bauteile:** Stahlpfetten/I-Träger; Stahlfachwerkträger; Holz-Alu-Fenster; Sanitärobjekte; Innenausbau-/Galerieelemente.
- **5 wichtigste Hürden:** Werkszeugnis/Prüfung; Gewährleistung; Brandschutz; Bestandsraster; Materiallogistik.
- **5 wichtigste übertragbare Erkenntnisse:** Altstahl braucht Prüfstrategie; Reuse muss früh entworfen werden; Bestand ist Materialbank und Zwangspunkt; einfache Fügungen helfen; Haftungsmodelle fehlen.
- **5 offene Fragen:** Wie viele Stahlträger wurden wirklich eingebaut? Wurde das Gewächshausdach mit Reuse-Stahl realisiert? Welche Fensteranzahl/U-Werte? Welche CO₂-Einsparung nur durch Direct Reuse? Wie wurde Gewährleistung vertraglich gelöst?

## Quellen

- Circular Material Systems – CRCLR / Impact Hub Berlin: https://circularmaterialsystems.com/en/case/impact-hub-berlin-crclr-house/
- ZRS Ingenieure – CRCLR House: https://www.zrs.berlin/en/project/crclr-house-2/
- BauNetz Wissen – CRCLR-Haus in Berlin: https://www.baunetzwissen.de/controlling-und-management/objekte/case-studies---bueromanagement/crclr-haus-in-berlin-9821591
- nbau – Transformation bauen – das CRCLR-Haus in Berlin: https://www.nbau.org/2022/12/08/transformation-bauen-das-crclr-haus-in-berlin
- LXSY Architektur – Impact Hub Berlin at CRCLR-House: https://lxsy.de/en/projects/impact-hub-berlin-at-crclr-house
- Zukunftsagentur Bau – CRCLR-Haus: https://www.zukunft-bau.at/projekt/buero-gewerbe/crclr-haus
- Architektenkammer Berlin – CRCLR-Haus: https://www.ak-berlin.de/baukultur/da-architektur-in-und-aus-berlin/projekte-da-2024/projekte-detailseite/crclr-haus-1/
