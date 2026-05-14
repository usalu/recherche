---
entity: "bauteiltyp"
id: "Decke"
title: "Brettsperrholzdecke"
build_status: "promoted_phase42"
legacy_paths:
  - "bauteil\Brettsperrholzdecke.md"
node_kind: "knot"
legacy_type: "Bauteil"
---

# Brettsperrholzdecke

## Verknüpfungen

**Übergeordnete Themen**
- Massivholzbau, Holz-Hybridbau, zirkulärer Holzbau, Design for Disassembly
- Decken- und Dachtragwerke, Vorfertigung, trockene Montage, Materialpass
- Wiederverwendung tragender Holzbauteile und reversible Verbindungssysteme

**Verwandte Dateien**
- `bauteil/Deckenplatte.md` – generische horizontale Plattenfunktion, auch Beton- und Stahlverbunddecken
- `bauteil/Holzrahmenelement.md` – leichter Holztafelbau; im Gegensatz zur massiven Brettsperrholzplatte stärker schicht- und systemabhängig
- `bauteil/Wand.md` – Brettsperrholz als Wandtyp und aussteifendes Element
- `material/Brettsperrholz.md`, `material/Holz.md`, `material/Klebstoff.md`, `material/Stahl.md`
- `tragwerkssystem/Massivholzbau.md`, `tragwerkssystem/Holz-Hybridbau.md`, `tragwerkssystem/Scheibentragwerk.md`
- `pruefung/Holzprüfung.md`, `pruefung/Feuchtemessung.md`, `pruefung/Tragwerksnachweis.md`, `pruefung/Brandschutzbewertung.md`
- `verbindung/Holzschraube.md`, `verbindung/Winkelverbinder.md`, `verbindung/Stahlblech.md`, `verbindung/Bolzenverbindung.md`, `verbindung/Trockene_Fuge.md`
- `reuse_strategie/Design_for_Disassembly.md`, `reuse_strategie/Direkte_Wiederverwendung.md`, `reuse_strategie/Materialpass.md`, `reuse_strategie/Adaptiver_Grundriss.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Forschung: InFutURe Wood, COST/Timber-DfD-Forschung, Ottenhaus et al. zu reversiblen Holzverbindungen, JRC REUSE-Projekt zu wiederverwendbaren Holzpaneelen, Chalmers-Studien zu CLT-Verbindungen
- Standards: EN 16351:2021 Brettsperrholz, Eurocode 5 / EN 1995, nationale Holzbaurichtlinien, Brandschutz- und Schallschutzregelwerke, Produktzulassungen/ETA einzelner Hersteller
- Methoden: Feuchtekartierung, Sichtsortierung/maschinelle Festigkeitsannahmen, Verbindungserfassung, Delaminationsprüfung, Bohrwiderstand/Resistographie bei Verdacht, Demontageplanung, BIM-/Materialpass-Dokumentation

## Kurzdefinition

Eine **Brettsperrholzdecke** ist ein horizontales Decken- oder Dachbauteil aus kreuzweise miteinander verklebten Brettlagen. Die quer zueinander angeordneten Lagen erzeugen Plattenwirkung, Formstabilität und Lastabtragung in eine oder zwei Richtungen. Im Bauwerk wird die Platte meist mit Schrauben, Winkeln, Stahlblechen, Randträgern, Auflagern, Verguss-/Dichtbändern sowie Brand-, Schall- und Fußbodenaufbauten kombiniert.

Für Wiederverwendung ist die Brettsperrholzdecke nicht nur als Holzmenge zu betrachten, sondern als vorgefertigtes Tragbauteil mit definierter Geometrie, Lagenaufbau, Festigkeitsklasse, Klebstoffsystem, Anschlussbild, Öffnungen, Nutzungsgeschichte und bauphysikalischen Zusatzschichten.

## Relevanz für Wiederverwendung im Bauwesen

Brettsperrholzdecken sind für Wiederverwendung interessant, weil sie großformatig, trocken montierbar und oft mit mechanischen Verbindungsmitteln gefügt sind. Im Vergleich zu vielen Nassbauweisen können sie bei guter Detailplanung mit geringerem Zerstörungsgrad ausgebaut werden. Ihre Vorfertigung erzeugt klar identifizierbare Elemente; digitale Produktionsdaten, CNC-Abbundpläne und Montagedokumentation können die spätere Bauteilprüfung stark erleichtern.

Obwohl Holz biogenen Kohlenstoff speichert und gegenüber Stahlbeton häufig geringere Herstellungs-Emissionen hat, ist direkte Wiederverwendung ökologisch wertvoller als Downcycling, thermische Verwertung oder Ersatz durch neue Massivholzelemente. Die Wiederverwendung verlängert die Kohlenstoffspeicherung, erhält industrielle Wertschöpfung und vermeidet erneute Holzernte, Trocknung, Verklebung und Transport.

Das größte Potenzial entsteht bei Gebäuden, die von Anfang an mit demontierbaren CLT-Decken geplant wurden: trockene Fußbodenaufbauten, zugängliche Schrauben, getrennte Installationszonen, lösbare Randanschlüsse, klare Spannrichtungen und dokumentierte Verbindungsmittel. Bei Bestandsgebäuden ohne DfD ist Wiederverwendung möglich, aber stark abhängig von Beschichtungen, Verklebungen, Schraubbildern, Durchdringungen, Feuchteereignissen und Brandschutzbekleidungen.

## Fachinhalt

### Bauteilaufbau und reuse-relevante Merkmale

**Platte**
- Lagenanzahl, Plattendicke, Haupttragrichtung, Decklagenrichtung, Festigkeitsklasse, Holzart, Klebstoff, Hersteller, Produktionsnorm und Elementnummer bestimmen die Tragfähigkeit.
- Öffnungen, Aussparungen, Nuten, Installationsdurchbrüche und Kantenfräsungen sind kritische Schwächungen. Sie können im neuen Projekt nur genutzt werden, wenn sie geometrisch und statisch passen.
- Große Platten haben hohen Wiederverwendungswert, lassen aber weniger Entwurfsfreiheit. Zuschnitt ist möglich, reduziert aber Randabstände, Anschlusszonen und dokumentierte Tragfähigkeit.

**Bodenaufbau und Zusatzschichten**
- Estriche, Schüttungen, Trittschalldämmungen, Trockenestrich, Brandschutzplatten und Abdichtungen sind häufig nicht Bestandteil der wiederverwendeten Tragplatte, beeinflussen aber Demontageaufwand und Zustand.
- Nassestrich oder geklebte Schichten verschlechtern Demontierbarkeit, erhöhen Masse und Feuchte-/Schadensrisiken. Trockene, geschraubte oder lose geschüttete Aufbauten sind günstiger.
- Für Wiederverwendung als Decke müssen Schall- und Brandschutz im neuen System neu bewertet werden; die alte Einzelplatte erfüllt selten allein alle heutigen Anforderungen.

**Verbindungen**
- Häufige Anschlüsse: Vollgewindeschrauben, Teilgewindeschrauben, Winkelverbinder, Zuganker, Hold-downs, Stahlbleche, Schlitzbleche, Balkenschuhe, Auflagerwinkel, Randbalken, Schubverbinder in Holz-Beton-Verbundsystemen.
- Reuse-freundlich sind zugängliche, lösbare und ersetzbare Verbindungsmittel mit ausreichenden Randabständen. Problematisch sind Nägel, verdeckte Schrauben ohne Dokumentation, Klebungen, eingegossene Verbundsysteme und Verbindungen, bei denen beim Rückbau das Holz statt des Stahlteils versagt.
- Für zirkuläre Details sollte die Soll-Schädigung im austauschbaren Verbindungsteil liegen, nicht in der CLT-Platte.

### Prüfung und Bewertung

**1. Dokumentation**
- Erforderlich: Hersteller, Produktnorm/Zulassung, Lagenaufbau, Festigkeit, Produktionsdatum, Plattenplan, CNC-Dateien, Schraub- und Anschlussplan, statische Berechnung, Brandschutz- und Schallschutzaufbau, frühere Nutzung.
- Ohne Dokumentation kann eine Platte zwar genutzt werden, aber häufig nur mit konservativen Annahmen, reduzierter Tragfähigkeit oder in sekundärer Anwendung.

**2. Zustand Holz und Klebfuge**
- Prüfen: Feuchtegehalt, Feuchtehistorie, Wasserflecken, Verfärbungen, Schimmel, Fäule, Insektenbefall, Risse, Delamination, mechanische Kerben, Quetschungen an Auflagern, Brand-/Rauch-/Hitzeeinwirkung, chemische Belastungen.
- Dauerhaft günstige Feuchte liegt im beheizten Innenraum meist niedrig; wiederholte Durchfeuchtung, undichte Nassräume oder Dachschäden können die Wiederverwendung stark einschränken.
- Sichtbare Delamination, aufgequollene Kanten oder großflächige Feuchteschäden sind Ausschluss- oder Sonderprüfungsgründe.

**3. Tragwerksnachweis**
- Neue Nachweise müssen Lasten, Spannweiten, Lagerung, Schwingungen, Durchbiegung, Scheibenwirkung, Aussteifung, Brandfall und Montagezustand abdecken.
- Besonders relevant bei Decken: Gebrauchstauglichkeit, Schwingungskomfort, Trittschall, Durchbiegung unter Langzeitlast, Querdruck am Auflager und Rollschub in Querlagen.
- Bereits vorhandene Schraubenlöcher können die Tragfähigkeit lokal reduzieren und neue Anschlussbilder einschränken.

**4. Brandschutz und Schallschutz**
- CLT-Decken können durch Abbrand bemessen werden, doch die tatsächliche Feuerwiderstandsdauer hängt von Dicke, Lagenaufbau, Klebstoffverhalten, Bekleidung, Fugen und Anschlüssen ab.
- Wiederverwendung sichtbarer CLT-Decken erfordert besondere Prüfung der Oberfläche, früherer Beschichtungen und Anschlussfugen.
- Schallschutz ist meist systemabhängig. Eine wiederverwendete Rohplatte benötigt häufig neue entkoppelte Aufbauten oder Unterdecken.

**5. Schadstoffe und Oberflächen**
- Mögliche Themen: alte Beschichtungen, Flammschutzmittel, Holzschutzmittel, Klebstoffemissionen, Formaldehyd aus ergänzenden Holzwerkstoffen, kontaminierte Fußbodenaufbauten.
- Bei jüngeren CLT-Produkten sind klassische Holzschutzmittel im Innenraum meist weniger wahrscheinlich als bei älteren Holzbauteilen; dennoch muss die Nutzungsgeschichte geprüft werden.

### Entwurfs- und Detailprinzipien für Wiederverwendung

- **Design from stock:** Spannweiten und Raster des neuen Projekts an vorhandenen Plattenformaten ausrichten. Kleine Maßabweichungen mit Randstreifen, Auflagerleisten oder Zwischenstücken lösen.
- **Trockene Schichten:** Trittschall, Installation und Brandschutz möglichst trocken, verschraubt oder lose montiert ausführen.
- **Zugängliche Verbindungsmittel:** Schraubenköpfe sichtbar oder dokumentiert, keine überdeckten kritischen Demontagestellen.
- **Trennbare Funktionen:** Tragplatte, Schallschutz, Brandschutz, Installation und Oberfläche als getrennte Layer planen.
- **Robuste Anschlusszonen:** Neue Schrauben nicht beliebig in alte Löcher setzen; Randabstände und Mindestabstände berücksichtigen.
- **Materialpass:** Platten-ID, Lage im Gebäude, Orientierung, Lagenaufbau, Schraubbilder, Öffnungen, Prüfungen, Reparaturen und Rückbauanleitung dokumentieren.

### Wiederverwendungsoptionen

**Direkte Wiederverwendung als Decke**
- Höchster Werterhalt, aber höchste Anforderungen an Tragfähigkeit, Schallschutz, Brand und Geometrie.

**Wiederverwendung als Dachplatte**
- Möglich bei geringeren Lasten; jedoch Feuchte- und Abdichtungsrisiko im neuen Dachaufbau beachten.

**Wiederverwendung als Wand- oder Ausbauelement**
- Bei Degradierung oder unpassender Spannweite kann eine CLT-Deckenplatte als Wand, Innenausbau, Möbelelement oder Sekundärtragwerk genutzt werden. Trag- und Brandschutzanforderungen bleiben projektbezogen.

**Materialliche Verwertung / Zuschnitt**
- Zuschnitt in kleinere Elemente kann Lager- und Transportprobleme lösen, zerstört aber ursprüngliche Produktidentität und erfordert neue Nachweise.

## Praxisbezug / Beispiele

**Forschung zu reversiblen CLT-Verbindungen**
- Studien zu reversiblen Holzverbindungen zeigen, dass Verbindungstyp und Verbindungsmittel entscheidend für spätere Wiederverwendung sind. Größere Schrauben in Winkel- oder Stahlblechkonfigurationen können reuse-freundlicher sein als viele lange Schrauben oder Nägel, wenn die Demontage ohne Holzschädigung möglich ist.
- Wichtig ist die konstruktive Hierarchie: Stahlteil und Schrauben sollen austauschbar sein; die Platte selbst soll möglichst wenig beschädigt werden.

**JRC REUSE – wiederverwendbare Holzpaneele**
- Das Joint Research Centre der Europäischen Kommission entwickelt im Projekt REUSE modulare, wiederverwendbare Holzpaneele für sichere und nachhaltige Gebäude. Relevanz für CLT-Decken: modulare Tragpaneele, schnelle Montage/Demontage, Wiederaufbau in anderen Kontexten und Verbindung von struktureller Sicherheit mit Kreislauffähigkeit.

**InFutURe Wood / DfD-Holzbau**
- Forschungsarbeiten zu „Design for deconstruction and reuse of timber structures“ zeigen, dass Holzbau historisch und technisch gute Voraussetzungen hat, aber heutige Systeme oft durch Nägel, Klebungen, Verbundschichten und nicht dokumentierte Details an Wiederverwendung verlieren.

**Mass-Timber-Reuse-Fallstudien**
- Neuere Fallstudien zu Massivholz-Testbauten und modularen Holzgebäuden zeigen, dass Wiederverwendung technisch möglich ist, wenn Demontage, Verbindung und Dokumentation von Anfang an mitgedacht werden. Die Datenlage ist im Vergleich zu Stahl- oder Betonreuse jedoch noch jung und projektbezogen.

## Herausforderungen / offene Fragen

- **Systemnachweise statt Einzelplatte:** Schall-, Brand- und Tragwerksleistung entsteht durch Schichten und Fugen. Eine gebrauchte CLT-Platte allein ist selten „fertige Decke“.
- **Klebstoff- und Produktalterung:** Für viele moderne CLT-Produkte gibt es noch begrenzte Langzeiterfahrung über mehrere Lebenszyklen. Klebfugenqualität, Delamination und Feuchtehistorie müssen projektbezogen beurteilt werden.
- **Verbindungsschäden:** Schraubenlöcher, ausgerissene Fasern, Querdruckstellen und Kerben können Wiederverwendung einschränken.
- **Feuchte:** Unsichtbare Feuchteschäden sind ein zentrales Risiko. Zwischenlagerung muss trocken, belüftet und verformungsarm erfolgen.
- **Brandschutzanforderungen:** Sichtbare Holzdecken sind brandschutztechnisch sensibel. Wiederverwendung kann durch neue Bekleidungen einfacher werden, mindert aber gestalterischen Wert.
- **Markt und Haftung:** Gebrauchte CLT-Elemente besitzen selten standardisierte Leistungserklärungen für den zweiten Einsatz. Akzeptanz hängt stark von Prüfbarkeit und Verantwortungskette ab.
- **Planungszeitpunkt:** CLT-Reuse funktioniert am besten, wenn Spender- und Empfängerprojekt früh gekoppelt sind. Nachträgliche Suche nach passenden Platten führt oft zu Raster- und Terminproblemen.

## Quellen

- EN 16351:2021: Timber structures – Cross laminated timber – Requirements. https://standards.iteh.ai/catalog/standards/cen/3f9c8502-609e-4592-9cc2-219dc2ff3720/en-16351-2021
- BSI: BS EN 16351:2021 Timber structures. Cross laminated timber. Requirements. https://knowledge.bsigroup.com/products/timber-structures-cross-laminated-timber-requirements-1
- Ottenhaus, L.-M. et al.: Design for adaptability, disassembly and reuse – A review of reversible timber connection systems. Construction and Building Materials, 2023. https://www.sciencedirect.com/science/article/pii/S0950061823025394
- Ottenhaus, L.-M. et al.: A review of reversible timber connection systems, PDF. https://www.ndt.net/article/construction_and_building_materials/papers/1-s2.0-S0950061823025394-main.pdf
- Cristescu, C. et al.: Design for deconstruction and reuse of timber structures – state of the art review. InFutURe Wood, 2020. https://www.diva-portal.org/smash/get/diva2%3A1527414/FULLTEXT02.pdf
- Grüter, C. et al.: Design for and from disassembly with timber elements, 2023. https://elib.uni-stuttgart.de/bitstreams/6d97c6a9-5761-4c5c-877e-ca18e14be71d/download
- European Commission Joint Research Centre: Reusable timber panels for safe and sustainable buildings. https://joint-research-centre.ec.europa.eu/projects-and-activities/iresist-home/ongoing-projects/reusable-timber-panels-safe-and-sustainable-buildings_en
- Elmäng, E.: Optimizing Connections for the Reuse of CLT Elements, Chalmers, 2025. https://odr.chalmers.se/items/938d5da1-a3d1-4a14-8578-cb46ed7c8e47
- Cabrero, J. M. et al.: Disassembly and Reuse in Tall Timber Buildings, 2025. https://orbi.uliege.be/bitstream/2268/336287/1/Final.pdf
- Li, Z. et al.: Reusable timber modular buildings, material circularity and embodied carbon assessment, 2024. https://openaccess.city.ac.uk/id/eprint/33808/11/1-s2.0-S2352710224025336-main.pdf
- FCRBE: A guide for identifying the reuse potential of construction products, 2020. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- DGNB: Gebäuderessourcenpass / Building Resource Passport. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport

## Quelle: bauteiltyp_Deckenplatte.staging_index

## Verknüpfungen

**Übergeordnete Themen**
- Decken- und Dachtragwerke, horizontale Bauteile, Plattenwirkung, Scheibenwirkung
- Wiederverwendung tragender Bauteile, Rückbauplanung, Bemessung im Bestand
- Design from Available Stock, modulare Raster, toleranzfähige Fügung

**Verwandte Dateien**
- `bauteil/Betonfertigteil.md` – Fertigteilklasse; hier nur die horizontale Funktion der Deckenplatte
- `bauteil/Brettsperrholzdecke.md` – spezifische Massivholzplatte als Decke
- `bauteil/Wand.md` – vertikale Platten und Wandtafeln; bei Wiederverwendung teils Funktionswechsel Platte/Wand
- `material/Beton.md`, `material/Brettsperrholz.md`, `material/Stahl.md`, `material/Verbundwerkstoff.md`
- `tragwerkssystem/Plattenbau.md`, `tragwerkssystem/Skelettbau.md`, `tragwerkssystem/Holz-Hybridbau.md`, `tragwerkssystem/Scheibentragwerk.md`
- `pruefung/Tragwerksnachweis.md`, `pruefung/Betonprüfung.md`, `pruefung/Holzprüfung.md`, `pruefung/Zustandsbewertung.md`, `pruefung/Schallschutz.md`, `pruefung/Brandschutz.md`
- `verbindung/Auflager.md`, `verbindung/Fuge.md`, `verbindung/Vergussfuge.md`, `verbindung/Schraubverbindung.md`, `verbindung/Schubverbinder.md`
- `reuse_strategie/Direkte_Wiederverwendung.md`, `reuse_strategie/Zuschnitt.md`, `reuse_strategie/Selektiver_Rueckbau.md`, `reuse_strategie/Design_from_Available_Stock.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Fallstudien/Forschung: ReCreate Hohlplatten-Piloten, EPFL Atlas of Reused Concrete, Küpfer/Fivet zu zugeschnittenen Stahlbetonplatten, RE:SLAB, dänische Versuche zu wiederverwendeten Hohlplattenanschlüssen, JRC REUSE-Holzpaneele
- Normen/Regelwerke: Eurocode 2 / EN 1992, Eurocode 5 / EN 1995, EN 1168 Hohlplatten, EN 13747 Elementdecken/Floor plates, EN 16351 Brettsperrholz, EN 13369 Betonfertigteile, DIN SPEC 91484, nationale Brand- und Schallschutzanforderungen
- Methoden: Last- und Spannweitenklassifizierung, Bewehrungs-/Spanngliedortung, Schwingungsnachweis, Auflagerprüfung, Fugenschnitt, Kraneinhebung, Kantenreparatur, Restlebensdauerbewertung, Materialpass

## Kurzdefinition

Eine **Deckenplatte** ist ein horizontales oder leicht geneigtes Plattenbauteil, das Lasten aus Nutzung, Eigengewicht, Ausbau, Trennwänden und ggf. Dachlasten zu Wänden, Trägern, Stützen oder Randauflagern abträgt. Sie kann aus Betonfertigteilen, Ortbetonzuschnitten, Brettsperrholz, Stahl, Holz-Beton-Verbund, Stahlbetonrippensystemen oder anderen Plattenmaterialien bestehen.

Für Wiederverwendung ist „Deckenplatte“ eine funktionsbezogene Kategorie. Entscheidend sind Spannrichtung, Auflagerung, Tragreserven, Durchbiegung, Schwingung, Brand- und Schallschutz, Durchdringungen, Randzustand und Verbindung mit angrenzenden Bauteilen.

**Abgrenzung zu `bauteil/Betonfertigteil.md`:** Eine Betonhohlplatte ist dort ein Betonfertigteil; hier wird sie als Deckenplatte hinsichtlich horizontaler Lastabtragung, Auflagerung, Fuge, Scheibenwirkung und bauphysikalischer Deckenanforderungen behandelt.

## Relevanz für Wiederverwendung im Bauwesen

Deckenplatten enthalten in Gebäuden sehr große Materialmengen und prägen Tragwerksraster, Geschosshöhen und Nutzungsflexibilität. Bei Beton- und Verbunddecken ist der gebundene Kohlenstoff- und Ressourcenaufwand hoch; bei Holzdecken ist der industrielle Wert des vorgefertigten Elements hoch. Direkte Wiederverwendung ganzer Deckenplatten erhält deutlich mehr Wert als Recycling zu Gesteinskörnung, Altholz oder Stahlschrott.

Gleichzeitig gehören Deckenplatten zu den anspruchsvollsten Reuse-Bauteilen, weil sie in der Nutzung sicherheitsrelevant sind und viele Leistungen bündeln: Tragfähigkeit, Gebrauchstauglichkeit, Brandschutz, Schallschutz, Scheibenwirkung, Installationsführung und Oberflächenqualität. Die Wiederverwendung gelingt besonders gut, wenn eine Platte als separates Element demontiert werden kann, die neue Spannweite nicht größer ist als die alte, Auflagerlängen gesichert sind und Durchdringungen begrenzt bleiben.

## Fachinhalt

### Haupttypen und Wiederverwendungseignung

**1. Spannbeton-Hohlplatte**
- Typisches serielles Betonfertigteil mit Hohlräumen und vorgespannten Litzen; häufig in Wohn-, Büro-, Schul-, Park- und Industriebauten.
- Reuse-Vorteile: standardisierte Breite, hohe Tragfähigkeit, klare Spannrichtung, fabrikmäßige Qualität, oft trockene Montage mit Fugenverguss.
- Reuse-Risiken: unbekannte Spanngliedlage, Schnittverbote, beschädigte Auflagerzonen, Fugenschnitt, Aufbeton/Estrich, Brandschutzanforderungen, geringe Flexibilität für neue Öffnungen.
- Besonders geeignet, wenn Platten ungeschnitten bleiben und im neuen Projekt ähnliche oder geringere Spannweiten und Lasten erhalten.

**2. Vollfertigteil- oder Massivplatte aus Stahlbeton**
- Kann als Fertigteilplatte, Balkonplatte, Podest oder Sonderplatte vorkommen.
- Reuse-Vorteile: massive Geometrie, robuste Oberfläche, weniger Hohlraumrisiken.
- Reuse-Risiken: hohes Gewicht, Bewehrungslage oft unbekannt, Korrosion an Kanten/Auflagern, schwierige neue Befestigungen.

**3. Elementdecke / Halbfertigteil mit Ortbetonergänzung**
- Vorgefertigte dünne Betonplatte mit Gitterträgern und bauseitigem Aufbeton.
- Für direkte Wiederverwendung als ursprüngliches Element meist ungünstig, weil Aufbeton und Fertigteil zu einem Verbundquerschnitt werden. Trennung zerstört häufig System und Bewehrungsverbund.
- Wiederverwendung ist eher als zugeschnittener Gesamtquerschnitt oder nachrangig als Material möglich.

**4. Ortbetonplatte als ausgesägtes Bauteil**
- Kein Fertigteil im Ursprung, aber als „geerntete Platte“ wiederverwendbar, wenn größere Abschnitte kontrolliert gesägt, gehoben und neu gelagert werden.
- Reuse-Vorteile: großes vorhandenes Materiallager in Bestandsgebäuden; hohe CO₂-Einsparpotenziale, wenn Zuschnitt und neue Struktur passen.
- Reuse-Risiken: unbekannte Bewehrung, Schnittkanten, Hebepunkte, Rissbildung, fehlende Produktnorm, Nachweisaufwand, hoher Rückbauaufwand.
- Forschung und Fallstudien zeigen technische Machbarkeit, aber die Methode ist noch nicht standardisierte Massenpraxis.

**5. Brettsperrholz- oder Holzwerkstoffplatte**
- Leichter als Beton, oft trocken verschraubt, gut vorfertigbar.
- Reuse-Risiken: Feuchte, Brand-/Schallschutzsysteme, Schraubenlöcher, Oberflächen, Durchbrüche und Klebfugenqualität.
- Details stehen in `bauteil/Brettsperrholzdecke.md`.

**6. Stahl- oder Stahlverbundplatte**
- Trapezblechverbunddecken und Stahl-Beton-Verbunddecken sind wegen Verbund und Brandschutzaufbauten schwer als Platte wiederzuverwenden.
- Demontierbare Stahlrost- oder Kassettenplatten sind günstiger, vor allem in Industriebauten.

### Kriterien für Wiederverwendbarkeit

**Tragfähigkeit**
- Alte und neue Lastannahmen vergleichen: Eigengewicht, Nutzlast, Auflasten, Trennwände, Fassadenanschlüsse, Installationen, Dachlasten, außergewöhnliche Lasten.
- Spannweite und Lagerungsart sind zentrale Parameter. Eine Platte sollte im neuen Einsatz möglichst gleich oder kürzer spannen und ähnlich gelagert werden.
- Bei vorgespannter Platte sind Biege-, Schub-, Torsions- und Auflagertragfähigkeit sowie Zustand der Spannlitzen entscheidend.

**Gebrauchstauglichkeit**
- Durchbiegung, Rissbreite, Schwingung und Verformung sind oft maßgebend, auch wenn rechnerische Tragfähigkeit ausreicht.
- Leichtere Holzplatten und lange Hohlplatten können Schwingungsprobleme verursachen; neue Aufbauten verändern Masse und Dämpfung.

**Auflager und Fugen**
- Auflagerlänge, Kantenfestigkeit, Quetschschäden, Korrosion, Ausbrüche und lokale Druckspannungen prüfen.
- Fugen beeinflussen Scheibenwirkung, Schallschutz, Brandschutz und Luftdichtheit. Wiederverwendung sollte Fugen nicht nur statisch, sondern auch bauphysikalisch neu planen.
- Trockene oder mechanisch lösbare Auflager sind reuse-freundlicher als Ortbetonverguss, Mörtelverbund oder verdeckte Schweißanschlüsse.

**Durchdringungen und Zuschnitt**
- Öffnungen, Schächte und Aussparungen sind problematisch, weil sie Bewehrung, Spannglieder, Holzfasern oder Plattenstreifen schwächen.
- Neue Durchbrüche sollten vermieden oder nur nach zerstörungsfreier Ortung und Nachweis gesetzt werden.
- Zuschnitt kann Wiederverwendung ermöglichen, wandelt aber Standardelemente in projektspezifische Reststücke und erhöht Prüfaufwand.

**Brand- und Schallschutz**
- Decken sind brandschutzrelevante Geschossabschlüsse. Feuerwiderstand hängt von Plattendicke, Bewehrung/Abbrand, Fugen, Bekleidung und Durchdringungen ab.
- Schallschutz ist meistens nur durch kompletten Deckenaufbau erreichbar. Wiederverwendete Rohplatten benötigen neue schwimmende Estriche, Trockenaufbauten, Schüttungen oder Unterdecken.

**Schadstoffe und Oberflächen**
- Mögliche Schadstoffe: asbesthaltige Bodenbeläge/Kleber, PAK-haltige Kleber, PCB-haltige Fugenmassen, alte Beschichtungen, Holzschutzmittel, kontaminierte Estriche.
- Vor Rückbau muss geklärt sein, ob Oberbeläge getrennt, saniert oder mit der Platte entsorgt werden müssen.

### Prozess für Deckenplatten-Reuse

1. **Gebäudekartierung**: Deckentyp, Raster, Spannrichtung, Plattendicke, Auflager, Fugen, Schächte, Lastgeschichte.
2. **Dokumentensuche**: Statik, Schal-/Bewehrungspläne, Fertigteilpläne, Herstellerdaten, Brandschutzkonzept.
3. **Probeöffnung und Ortung**: Bewehrung/Spannstahl, Hohlräume, Verbundschichten, Auflagerdetails.
4. **Musterentnahme / Pilotdemontage**: tatsächliche Fugenlösbarkeit, Hebbarkeit, Schäden, Zeitaufwand.
5. **Klassifizierung**: wiederverwendbar als Decke, wiederverwendbar mit Einschränkung, Funktionswechsel, Recycling/Entsorgung.
6. **Empfängerentwurf**: Raster aus vorhandenen Platten, kurze Transportwege, ausreichend Lager- und Montageflächen.
7. **Nachweis**: Tragwerk, Montagezustand, Brand, Schall, Dauerhaftigkeit, Verbindung, Bauphysik.
8. **Dokumentation**: Bauteilpass mit ID, Prüfwerten, Fotos, Lage, Reparaturen, Einbauort.

## Praxisbezug / Beispiele

**ReCreate – Hohlplatten in Tampere**
- Im finnischen ReCreate-Pilot wurden Hohlplatten aus einem Bürogebäude demontiert und in neuen Wohngebäuden wieder eingesetzt. Fugen und Aufbauten wurden getrennt, Elemente markiert und über Qualitätssicherung in den neuen Bauprozess überführt.
- Die Beispiele zeigen, dass Deckenplatten-Reuse nicht nur technisches Demontieren ist, sondern ein abgestimmtes System aus Spendergebäude, Prüfkette, Lagerung, Entwurf, Hersteller-/Prüfkompetenz und behördlicher Akzeptanz.

**Küpfer/Fivet – zugeschnittene Ortbetonplatten**
- Forschungsarbeiten der EPFL zeigen die Möglichkeit, Ortbetondecken aus Abbruchgebäuden in größere Plattenabschnitte zu schneiden und in Neubauten wiederzuverwenden.
- Relevante Lehre: Auch monolithische Bestände können Bauteilquellen sein, aber nur mit präziser Schnittplanung, Hebekonzept, Nachweis der Bewehrung und Entwurf, der mit unregelmäßigen Plattenformaten arbeiten kann.

**RE:SLAB**
- RE:SLAB untersucht tragende Systeme aus wiederverwendeten Stahlbetonplatten mit offener Anschlusslogik. Der Ansatz ist relevant, weil nicht nur einzelne Platten, sondern ein neues System aus wiedergewonnenen Platten und wieder lösbaren Auflagern entwickelt wird.

**Dänische Hohlplatten-Versuche**
- Versuche zu wiederverwendeten Hohlplatten mit neuen Stahl-Diaphragma-Auflagern untersuchen, wie gebrauchte Platten in demontierbare neue Systeme integriert werden können. Praktisch wichtig ist die Verbindung: Sie muss Tragfähigkeit bieten und eine weitere Demontage ermöglichen.

## Herausforderungen / offene Fragen

- **Deckensysteme sind Mehrleistungsbauteile:** Tragfähigkeit allein genügt nicht; Schall, Brand, Schwingung und Fugen sind gleichrangig.
- **Unklare Spannglieder:** Bei Spannbetonplatten sind neue Schnitte oder Bohrungen besonders riskant. Fehlende Spannglieddaten können Wiederverwendung ausschließen.
- **Aufbeton und Verbund:** Viele Decken wurden durch Aufbeton, Estrich oder Fugenverguss monolithisiert. Trennung kann Bauteile beschädigen oder unwirtschaftlich machen.
- **Transport und Gewicht:** Platten sind groß und schwer. Ökologische Vorteile sinken bei langen Transportwegen, mehrfacher Zwischenlagerung oder hohem Reparaturaufwand.
- **Passfähigkeit:** Vorhandene Längen, Breiten und Öffnungen bestimmen das neue Gebäude. Reuse verlangt Entwurfsflexibilität.
- **Regulatorik:** Für gebrauchte tragende Deckenplatten fehlen vielerorts standardisierte Prüfklassen und Anerkennungswege.
- **Versicherung und Gewährleistung:** Die Verantwortungskette vom Spendergebäude bis zum neuen Einbau ist komplex.

## Quellen

- ReCreate Project: Reusing precast concrete for a circular economy. https://recreate-project.eu/
- ReCreate: A third reuse mini-pilot implemented in Finland, 2026. https://recreate-project.eu/2026/04/20/a-third-reuse-mini-pilot-implemented-in-finland/
- ReCreate: Finland pilot. https://recreate-project.eu/project-pilots/finland/
- EN 1168:2005+A3:2011: Precast concrete products – Hollow core slabs. https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- EN 13747: Precast concrete products – Floor plates for floor systems. https://www.concrete.org.uk/fingertips/floor-plates-for-floor-systems-bs-en/
- EN 13369:2023: Common rules for precast concrete products. https://standards.iteh.ai/catalog/standards/cen/7488f236-67c6-4f66-b17e-b61d469f5530/en-13369-2023
- Küpfer, C. et al.: Reuse of cut concrete slabs in new buildings for circular ultra-low-carbon floor designs. Journal of Cleaner Production, 2024. https://www.sciencedirect.com/science/article/pii/S095965262401014X
- Küpfer, C. et al.: Reuse of concrete components in new construction projects: critical review of 77 circular precedents. Journal of Cleaner Production, 2023. https://www.sciencedirect.com/science/article/pii/S0959652622048090
- Estrella, X. et al.: RE:SLAB — a load bearing system for open-ended reuse of concrete slabs, 2024. https://arodes.hes-so.ch/nanna/record/13945/files/Redaelli_2024_RE-SLAB.pdf
- Jørgensen, H. B. et al.: Experimental Investigation of Connections for Reuse of Hollow Core Slabs, 2023. https://portal.findresearcher.sdu.dk/files/232056087/Experimental_Investigation_of_Connections_for_Reuse_of_Hollow_Core_Slabs.pdf
- EPFL Structural Xploration Lab: Atlas of Reused Concrete. https://concrete-reuse.epfl.ch/
- Devènes, J. et al.: Reusability assessment of reinforced concrete components prior to deconstruction from obsolete buildings. Developments in the Built Environment, 2024. https://www.sciencedirect.com/science/article/pii/S2352710224001529
- DIN SPEC 91484:2023-09. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- FCRBE: A guide for identifying the reuse potential of construction products, 2020. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf

Strategischer Leitfaden zur Wiederverwendung von Deckentragwerken: Fertigdecken, Hohlkörper- und Spannbetonelemente

1. Strategische Einordnung: Kreislaufwirtschaft im Sektor der Deckensysteme

Die Bauwirtschaft steht vor einer beispiellosen Transformation. Angesichts der Tatsache, dass der Bausektor für etwa 40 % des globalen Rohstoffverbrauchs und rund 55 % des bundesweiten Abfallaufkommens verantwortlich ist, gewinnt die effiziente Nutzung des „Urbanen Lagers“ – des Bestands an bereits verbauten Materialien – massiv an Bedeutung. Deckentragwerke bilden dabei eine Schlüsselkomponente für die Dekarbonisierung, da sie einen erheblichen Teil der im Gebäude gebundenen „grauen Emissionen“ repräsentieren.

Fachexperten-Urteil: Ein Neubau verursacht im Durchschnitt doppelt so viele CO₂-Emissionen wie eine Sanierung. Während konventionelles Recycling oft ein Downcycling darstellt, ermöglicht die direkte Wiederverwendung (Reuse) den Erhalt der investierten Energie und der Materialgestalt. Die strategische Priorisierung muss daher lauten: Sanierung und Erhalt vor Abbruch und Neubau. Falls ein Rückbau unumgänglich ist, stellt die werterhaltende Demontage von Deckenelementen den wirksamsten Hebel dar.

2. Technische Analyse der Wiederverwendbarkeit von Betondeckensystemen

Die technische Eignung von Betondecken für eine Zweitnutzung hängt maßgeblich von ihrer Konstruktionsart ab. Betonfertigteile bieten aufgrund ihrer modularen Natur systemimmanente Vorteile gegenüber Ortbetonstrukturen.

Potenziale spezifischer Deckentypen

* Spannbeton-Fertigdecken: Diese weisen das höchste Reuse-Potenzial auf. Wegen der Vorspannung sind sie in der Regel rissfrei, was zu einer exzellenten Dauerhaftigkeit führt. Dieser rissfreie Zustand ist das primäre technische Argument für den Nachweis der Restgebrauchseigenschaften.
* Hohlkörperdecken: Durch ihr reduziertes Eigengewicht lassen sie sich effizient als vollständige Elemente wiedergewinnen. Wichtiger Prozessschritt: Vor der Demontage muss oft der „Aufbeton“ (Topping) entfernt werden, um die Modulverbindungen freizulegen.
* Betonplatten/Massivdecken: Auch bewehrte Fertigteilplatten sind geeignet, sofern die statische Integrität beim Ausbau gewahrt bleibt.

Strategische Warnung (Sicherheit): Vor jedem Schnitt oder Trennvorgang muss zwingend die Spannrichtung und der Verlauf der Hauptbewehrung zweifelsfrei festgestellt werden (gemäß Source 410.4.1). Ein Durchtrennen der Hauptbewehrung im falschen Moment kann zum sofortigen Versagen des Bauteils oder angrenzender Felder führen.

Grundvoraussetzungen für die Wiederverwendung (Landesamt Brandenburg)

1. Zugänglichkeit und Demontierbarkeit: Physische Erreichbarkeit ohne Zerstörung der Hauptstruktur.
2. Restgebrauchseigenschaften: Nachweis der Qualität und Prognose der Restnutzungsdauer.
3. Standsicherheit: Statische Belastbarkeit für den neuen Verwendungszweck.
4. Wiedermontierbarkeit: Vorhandensein technischer Schnittstellen für die Neuinstallation.

3. Das Pre-Demolition-Audit (PDA) nach DIN SPEC 91484

Um das Potenzial des Gebäudebestands systematisch zu erschließen, ist ein PDA zwingend erforderlich. Dieses muss deutlich vor dem Rückbau erfolgen, damit die Ergebnisse in die Vergabeunterlagen für den selektiven Rückbau einfließen können.

Das zweistufige Verfahren

* Stufe 1 (Vorprüfung): Identifikation von Bauprodukten mit grundsätzlicher Eignung. Erfassung von Standort, Baujahr, Gebäudeklasse und geschätzten Mengen.
* Stufe 2 (Detailprüfung): Vertiefte Analyse durch Fachgutachter (Statiker, Schadstoffexperten). Hier erfolgt die Differenzierung der Daten:

Bautechnische Eigenschaften	Umweltchemische Eigenschaften
Tragfähigkeit, Spannrichtung, Hauptbewehrung	Schadstoffbelastung (Asbest, KMF, PCB)
Abmessungen (L, B, H) & Form	Chemische Materialzusammensetzung
Verbindungstechnik & Lagerung	Gefährliche Inhaltsstoffe (Parameter/Grenzwerte)
Erhaltungszustand (Rissfreiheit bei Spannbeton)	Oberflächenbelastungen (Farben, PAK)

4. Rechtlicher Rahmen: Vermeidung der Abfalleigenschaft

Die zentrale Hürde für die Wirtschaftlichkeit ist die Abgrenzung zwischen Abfall und Produkt. Sobald ein Bauteil als Abfall eingestuft wird, greift das strenge Regime des Kreislaufwirtschaftsgesetzes (KrWG).

Der 4-Schritte-Prozess zur Produktwahrung

1. Identifizierung: Systematische Erfassung (PDA).
2. Entscheidung über Verwendungszweck: Festlegung einer bautechnisch zulässigen Anschlussnutzung.
3. Selektives Rückbaukonzept: Planung des zerstörungsfreien Ausbaus.
4. Umsetzung: Physische Entnahme.

Fachexperten-Tipp: Die Realisierung des Verwendungszwecks muss zum Zeitpunkt der Entnahme hinreichend sicher sein. Das effektivste Mittel zur Vermeidung der Abfalleigenschaft ist der Abschluss eines Kaufvertrags mit einem Abnehmer noch vor dem Ausbau.

Berliner Besonderheit: Nutzen Sie das Formblatt V 241 F (Besondere Vertragsbedingungen Abfall) und das Formblatt 1 zur systematischen Auflistung der Verwertungs- und Wiederverwendungswege. Für den Immissionsschutz bei Lagerungen ist in Berlin die Senatsverwaltung für Mobilität, Verkehr, Klimaschutz und Umwelt zuständig.

Frühes Ende der Abfalleigenschaft: Falls kein sofortiger Abnehmer gefunden wird, kann ein Bauteil zunächst als Abfall gelagert werden. Es verliert diesen Status jedoch wieder (Beginn der Produkteigenschaft), sobald durch technische Prüfung ein rechtmäßiger Verwendungszweck festgelegt und dessen Realisierung gewiss wird.

5. Bauordnungsrechtliche Verwendbarkeitsnachweise

In der Praxis (insb. BauO Bln) stellt sich die Hierarchie der Nachweise für Sekundärbauteile wie folgt dar:

1. Regelkonformität (VV TB): Entspricht das Bauteil den Technischen Baubestimmungen? (Häufig bei Reuse schwierig).
2. Standard-Zulassungen (abZ/abP): Nur wenn das gebrauchte Teil exakt einer bestehenden Zulassung entspricht.
3. Zustimmung im Einzelfall (ZiE): Dies ist für tragende Sekundärbauteile der praxisrelevanteste Weg. Die ZiE wird durch die Oberste Bauaufsichtsbehörde erteilt.

Warnung zur EU-BauPVO (Verordnung 2024/3110): Ein CE-Kennzeichen wird für gebrauchte Produkte nur dann relevant, wenn die harmonisierten technischen Spezifikationen (htS) diese ausdrücklich einschließen. Aktuell ist dies bei den meisten bestehenden Normen noch nicht der Fall.

6. Operative Umsetzung: Selektiver Rückbau

Der Erfolg entscheidet sich auf der Baustelle. Qualitätssicherung ist hier keine Option, sondern eine Notwendigkeit.

Demontageverfahren

* Ortbetonstrukturen: Erfordern Präzisionsschnitte mittels Diamantsägen. Hier ist der streifenweise Abbruch parallel zur Bewehrungsrichtung oft die einzige Möglichkeit, handhabbare Segmente zu gewinnen.
* Fertigteile (Hohlkörper/Spannbeton): Ziel ist die Gewinnung vollständiger Elemente. Hebezeuge müssen so dimensioniert sein, dass sie das Bauteil bereits während des Trennvorgangs sichern, um unkontrollierte Lastumlagungen zu verhindern.

Vergleich der Verfahren

Merkmal	Zerstörungsfreier Ausbau (Reuse)	Ausbau zur Verwertung (Recycling)
Zielsetzung	Erhalt der Funktionalität und Gestalt	Stoffliche Separierung (Bauschutt)
Aufwand	Hoch (Präzisionsschnitte, Einzelsicherung)	Geringer (maschineller Abbruch)
Kosten	Höhere Personalkosten, Spezialgeräte	Niedrigere operative Kosten
Erhalt der Eigenschaften	Vollständig gegeben (Monitoring nötig)	Geht verloren (Downcycling)

7. Wirtschaftlichkeit, Vermarktung und Steuern

Der Markt wird durch Plattformen wie Concular, Madaster oder restado professionalisiert. Ein Materialpass sichert den Restwert ab, indem er Herkunft, Qualität und Lage dokumentiert.

Umsatzsteuerrechtliche Nuancen (§ 2b UStG)

Ab dem 01.01.2027 entfällt die Privilegierung für juristische Personen des öffentlichen Rechts (jPöR). Der Verkauf von Bauteilen wird umsatzsteuerpflichtig, wenn:

* Eine nachhaltige wirtschaftliche Tätigkeit vorliegt.
* Wettbewerbsrelevanz gegeben ist (Teilnahme am Markt wie ein privater Akteur).

Fachexperten-Tipp: Nutzen Sie die Übergangszeit, um Buchhaltungssysteme auf die Trennung von hoheitlichen und wirtschaftlichen Geschäftsbetrieben vorzubereiten. Nur im wirtschaftlichen Bereich ist ein Vorsteuerabzug für die oft hohen Rückbau- und Prüfkosten möglich.

Ausblick

Die Einführung einer Musterumbauordnung ist essenziell, um Anforderungen an Bestandsmaßnahmen (Brandschutz, Schallschutz) zu flexibilisieren. Nur so kann die ökologische Dividende der Wiederverwendung – die Vermeidung grauer Emissionen – vollumfänglich realisiert werden.

--------------------------------------------------------------------------------

Ressourcen & Links:

* ZiE-Anträge & Formulare: DIBt (www.dibt.de)
* PDA-Standard: Beuth Verlag (DIN SPEC 91484)
* Berliner Leitfaden: Senatsverwaltung MVKU (www.berlin.de/sen/mvku)

------------------------------------------------------------
version 2 of the same notbook:

Strategischer Fachbericht: Wiederverwendung von Deckenelementen und Platten im zirkulären Bauwesen

1. Strategische Einordnung: Bauen im "Urbanen Lager"

Die Bauwirtschaft steht vor einer paradigmatischen Transformation. Angesichts der Tatsache, dass der Sektor in Deutschland für rund 40 % des Rohstoffverbrauchs und über 55 % des gesamten Abfallaufkommens verantwortlich ist, muss der Gebäudebestand konsequent als "Urbanes Lager" (Urban Mining) begriffen werden. Die effiziente Bergung und Wiedernutzung bereits verbauter Ressourcen ist keine bloße ökologische Option, sondern eine ökonomische und rechtliche Notwendigkeit zur Dekarbonisierung der gebauten Umwelt.

Analyse der Kreislaufwirtschaftspotenziale

Die ökologische Überlegenheit der direkten Wiederverwendung (Reuse) gegenüber dem stofflichen Recycling (Downcycling) manifestiert sich in der Erhaltung der gebundenen "grauen Energie". Daten der Deutschen Umwelthilfe (DUH) und des VDI ZRE verdeutlichen dies:

* CO2-Einsparung: Ersatzneubauten verursachen im Durchschnitt die zweifache Menge an CO2-Emissionen im Vergleich zu Sanierungsvorhaben.
* Ressourcenschutz: Rund 90 % des mineralischen Rohstoffverbrauchs in Deutschland entfallen auf den Bausektor. Die Wiederverwendung reduziert diesen Primärbedarf unmittelbar.
* Emissionsminderung durch Substanzerhalt: Durch die gezielte Aufbereitung von Bauteilen (z. B. Fenster) lassen sich gegenüber der Neuherstellung ca. 17 % der Treibhausgasemissionen und 27 % des Primärenergiebedarfs einsparen.

Kernforderungen für den Sektor

Die DUH definiert fünf strategische Säulen, die für großformatige Bauteile wie Deckenplatten operativ umgesetzt werden müssen:

1. Abrissvermeidung: Gesetzlicher Vorrang für Sanierung und Umnutzung (Musterumbauordnung).
2. Verbindliche Zirkularitätskonzepte: Dokumentation der Demontierbarkeit bereits in der Planungsphase.
3. Selektiver Rückbau: Pflicht zur Durchführung von Pre-Demolition Audits (PDA) nach DIN SPEC 91484.
4. Marktstärkung für Sekundärprodukte: Gezielte Nachfrageförderung durch Quoten.
5. Öffentliche Vorbildrolle: Grüne Beschaffung als Markttreiber.

Decken stellen als massivste Bauteile das größte Potenzial zur CO2-Reduktion dar, fungieren jedoch als statisch relevante, aussteifende Horizontalscheiben, was höchste Anforderungen an die technische Demontage stellt.

2. Technische Charakterisierung und Demontageverfahren von Deckensystemen

Deckenplatten sind innerhalb des statischen Systems eines Gebäudes als aussteifende Horizontalscheiben definiert. Jeder Eingriff in diese Substanz erfordert zwingend eine präzise Bestandsanalyse und eine projektbezogene Abbruchstatik, um die Standsicherheit während der selektiven Demontage zu gewährleisten.

Differenzierung der Deckentypen nach LB 410.4.1

Deckentyp	Statische Besonderheit	Rückbauanforderung (zerstörungsfrei)
Massive Stahl-/Spannbeton	Aussteifende Funktion; Spannrichtung/Bewehrung kritisch.	Streifenweiser Abbruch parallel zur Bewehrungsrichtung.
Balkendecken (Stahl, Holz, Beton)	Lastabtragung über Primärbalken.	Manuelle Demontage; Entfernung der Füllkörper; Sicherung der Balken durch Hebezeuge oder Hilfsjoche.
Gewölbedecken	Druckbogenwirkung; oft mit Zugbändern.	Rückbau unter Beachtung des statischen Systems; Trennung der Zugbänder erst nach dem Gewölberückbau.
Fertigbauteile (Slabs)	Modulare Elementbauweise.	Entfernung des Aufbetons (Topping) vor Demontage vollständiger Fertigteile erforderlich.

Operative Rückbaustrategien und BVSF-Potenziale

Gemäß Leistungsbereich 410.4.1 ist bei bewehrten Decken die Feststellung der Hauptbewehrungsrichtung obligatorisch. Ein wesentlicher Fokus liegt auf Spannbeton-Fertigdecken (BVSF). Aufgrund der Vorspannung sind diese Elemente im Regelfall rissfrei, was ihre Dauerhaftigkeit (Service-Life) signifikant erhöht. Ihre modulare Konstruktion begünstigt die "Wiedermontierbarkeit", sofern die Verbindungen zerstörungsfrei gelöst werden können. Dieses hohe technische Potenzial bildet die Basis für die notwendige Zustimmung im Einzelfall (ZiE) durch die Bauaufsicht.

Die physische Integrität beim Ausbau ist die Voraussetzung für die anschließende systematische Erfassung im PDA.

3. Der Prozess der Bauteilerfassung: Pre-Demolition Audit (PDA)

Ein standardisiertes PDA gemäß DIN SPEC 91484 ist essenziell, um eine belastbare Datentiefe für die gesamte Wertschöpfungskette zu generieren. Für Projekte im Land Berlin ist zudem die Integration des Leitfadens zur Erstellung eines Rückbau- und Entsorgungskonzeptes inklusive der zugehörigen Excel-Tabellen zur Bauteilerfassung zwingend.

Das zweistufige Verfahren nach DIN SPEC 91484

1. Stufe 1 (Vorprüfung): Identifikation von Bauprodukten mit grundsätzlichem Reuse-Potenzial auf Basis von Baujahr, Standort und Gebäudeklasse.
2. Stufe 2 (Detailprüfung): Vertiefung technischer Daten, insbesondere der Verbindungsarten, Schadstofffreiheit und geometrischen Genauigkeit.

Erforderliche Bauteilparameter für Deckenplatten

* Statik & Geometrie: Tragfähigkeit, Materialfestigkeiten, Abmessungen, Brandschutzklasse und Gewicht.
* Umweltchemie: Nachweis der Schadstofffreiheit (Asbest, KMF, PCB, PAK) durch Fachgutachten.
* Dokumentation: Verwendung des Berliner Formblatts V 241 F (Besondere Vertragsbedingungen – Abfall) zur rechtssicheren Aufstellung der Wiederverwendungswege.

Akteursrollen

Der Prozess erfordert eine interdisziplinäre Verzahnung: Der Statiker bewertet die Resttragfähigkeit, der Schadstoffgutachter die chemische Unbedenklichkeit und das Abbruchunternehmen führt den selektiven Rückbau gemäß PDA-Vorgaben durch. Diese Dokumentation bildet die Basis für den Übergang vom Abfall- zum Produktstatus.

4. Rechtliche Rahmenbedingungen und Abfallvermeidung

Das strategische Ziel ist die Vermeidung der Abfalleigenschaft nach § 3 KrWG durch die frühzeitige Festlegung eines Verwendungszwecks.

Vermeidung der Abfalleigenschaft und "Frühes Ende"

Um den Abfallstatus zu umgehen, muss eine "hinreichende Gewissheit" der Wiederverwendung bestehen. Der Berliner Leitfaden betont hierbei den Prozess der 4 Schritte: Identifizierung, Entscheidung, Erhalt der Eigenschaften und Umsetzung. Ein kritischer Faktor ist das "Frühe Ende der Abfalleigenschaft" (Modul 1): Bauteile, die zunächst als Abfall eingestuft wurden, können diesen Status bereits auf der Baustelle wieder verlieren, wenn durch technische Prüfungen ein rechtmäßiger Verwendungszweck hinreichend sicher fixiert wird (z. B. durch ein öffentliches Angebot auf Plattformen wie Concular oder restado).

Produktrechtliche Rahmenbedingungen

* EU-BauPVO (neu): Die Verordnung (EU) 3110/2024 bezieht gebrauchte Produkte explizit ein, sofern harmonisierte technische Spezifikationen (htS) vorliegen. Bei "wesentlichen Veränderungen" (z. B. Änderung der statischen Spannweite) greift das Regime für Neuprodukte.
* BauO Bln: Für gebrauchte Deckenplatten sind i. d. R. Verwendbarkeitsnachweise (abZ, ZiE) erforderlich.
* Lagerung: Gemäß § 61 Abs. 1 Nr. 13 BauO Bln ist die baubegleitende Zwischenlagerung verfahrensfrei. Die immissionsschutzrechtliche Genehmigungsfreiheit (§ 4 BImSchG) endet bei Überschreitung von Mengen (30t gefährlich / 100t nicht gefährlich) oder einer Dauer von über einem Jahr.

5. Vertragliche Gestaltung und Haftungsmanagement

Die vertragliche Absicherung bei Primärbauteilen erfordert eine Abkehr von Standardverträgen hin zu spezifischen Risikoverteilungen.

Die "Negative Beschaffenheitsvereinbarung"

Als zentrales Instrument zur Haftungsbeschränkung dient die negative Beschaffenheitsvereinbarung. Hierbei wird der Ist-Zustand (Nutzungsalter, Gebrauchsspuren, Abweichung von aktuellen Normen) als vertragsgemäß definiert. Wichtig: Gegenüber Verbrauchern (§ 13 BGB) sind die Spielräume durch § 476 BGB stark eingeschränkt. Strategisch empfiehlt sich hier der Weg über öffentlich zugängliche Versteigerungen (§ 474 Abs. 2 BGB), um Gewährleistungsausschlüsse rechtssicher zu gestalten.

Szenarien der Abgabe und Umsatzsteuer

* Interne Abgabe: Zwischen Einheiten desselben Rechtsträgers (z. B. Land Berlin/Bezirksämter) liegt kein "Inverkehrbringen" vor; produktrechtliche Hürden sind hier minimiert.
* Wettbewerbliche Grenzen: Gemäß § 63 LHO ist bei Verkauf an Dritte eine Marktwertprüfung erforderlich. Ein öffentliches Angebot (Auktion) dient hierbei gleichzeitig als Nachweis der Nachfrage zur Vermeidung des Abfallstatus.
* Umsatzsteuer: Ab dem 01.01.2027 entfällt die Privilegierung öffentlicher Akteure nach § 2b UStG; Verkäufe werden dann i. d. R. mit 19 % USt belegt.

6. Operative Checkliste für die Wiederverwendung von Decken

Phase 1: Planung & Erkundung

* [ ] PDA (Stufe 1 & 2) nach DIN SPEC 91484 erstellt?
* [ ] Prüfung auf vorliegende htS gemäß neuer EU-BauPVO durchgeführt?
* [ ] Berliner Excel-Tabellen zur Bauteilerfassung (REK) initialisiert?

Phase 2: Selektiver Rückbau

* [ ] Abbruchstatik für aussteifende Horizontalscheiben freigegeben?
* [ ] Selektives Rückbaukonzept inklusive Aufbeton-Entfernung und Hilfsjochen erstellt?
* [ ] Formblatt V 241 F als Vertragsbestandteil integriert?

Phase 3: Vermarktung & Beschaffung

* [ ] Marktwertprüfung nach § 63 LHO (z. B. via Concular/Zoll-Auktion) erfolgt?
* [ ] Rechtssichere negative Beschaffenheitsvereinbarung (Ist-Zustand-Doku) aufgesetzt?
* [ ] Statusprüfung: "Frühes Ende der Abfalleigenschaft" dokumentiert?

Phase 4: Wiedereinbau

* [ ] Erforderlichkeit der Zustimmung im Einzelfall (ZiE) bei der Senatsverwaltung geprüft?
* [ ] Bedenkenanzeige des Bauunternehmers bei beigestellten Bauteilen proaktiv eingefordert?
* [ ] Übereinstimmungserklärung (Ü-Zeichen) durch den Verwender vorbereitet?

Finales Statement

Die Etablierung zirkulärer Prozesse bei statisch relevanten Bauteilen ist der Schlüssel zur Bauwende. Die systematische Nutzung digitaler Materialpässe (z. B. Madaster) sichert den langfristigen Werterhalt und transformiert den Gebäudebestand von einer Entsorgungslast in eine strategische Rohstoffreserve. Wer heute Deckenplatten zerstörungsfrei demontiert, agiert als Treuhänder der Ressourcen von morgen.

--------------------------------------------------------------------------------
Version 3 of the same notebook:

Fachbericht: Wiederverwendung von Deckentragwerken und Fertigteilelementen im Bauwesen

Die Dekarbonisierung des Bausektors ist eine der größten ingenieurtechnischen und regulatorischen Herausforderungen unserer Zeit. Angesichts der Tatsache, dass das Bauwesen in Deutschland für rund 40 % des Rohstoffverbrauchs und 55 % des Abfallaufkommens verantwortlich ist, stellt die Strategie des Urban Mining keine bloße Option, sondern eine Notwendigkeit dar. Deckentragwerke bilden aufgrund ihrer massiven Ausführung das größte „Urbane Lager“ im Hochbau. Ihre werterhaltende Wiederverwendung statt des energieintensiven Recyclings ist der entscheidende Hebel, um graue Emissionen signifikant zu senken und die Transformation zur Kreislaufwirtschaft zu vollziehen.

--------------------------------------------------------------------------------

1. Definition und Abgrenzung

Deckentragwerke sind horizontale Primärbauteile, die neben der Lastabtragung (Eigengewicht, Verkehrslasten) eine entscheidende aussteifende Funktion für das Gesamtbauwerk übernehmen. Sie fungieren als statisches Rückgrat und bilden starre Scheiben zur horizontalen Lastweiterleitung in vertikale Elemente (Wände, Stützen).

Innerhalb der Bestandsanalyse ist strikt zwischen massiven Stahl- und Spannbetondecken, Balkendecken und Gewölbedecken zu unterscheiden. Eine zerstörungsfreie Trennung ist die Grundvoraussetzung für den Erhalt der statischen Integrität. Besonderes Augenmerk gilt hierbei der bauphysikalischen und statischen Entkopplung von der Primärstruktur, ohne die Bewehrungsführung oder den Gefügeverbund zu schädigen.

Quellenbelege: LB 410.4, VDI ZRE.

2. Typologien und Unterarten

Im Bestand differenzieren wir folgende Systeme hinsichtlich ihres Wiederverwendungspotenzials:

* Massive Stahlbeton- und Spannbetondecken: Spannbeton-Fertigdecken eignen sich aufgrund ihrer werkseitigen Vorspannung und der damit einhergehenden Rissfreiheit sowie hohen Dauerhaftigkeit besonders für den Wiedereinsatz.
* Hohlkörper- und Kassetten-Rippendecken: Diese Systeme bieten durch Materialeinsparung logistische Vorteile, erfordern jedoch beim Rückbau aufgrund der filigranen Stege erhöhte Vorsicht.
* Fertigteilplatten und Flachbetondecken: Häufig als Elementdecken mit Ortbetonergänzung (Aufbeton) ausgeführt.
* Balkendecken: Bestehend aus Trägern (Holz, Stahl, Beton) mit Füllkörpern oder Einschüben.
* Gewölbedecken: Statisch anspruchsvolle Bestandsbauteile, deren Rückbau unter strikter Beachtung des Bogenschubs erfolgen muss.
* Hinweis zu CLT-Decken: Cross-Laminated Timber wird im Diskurs als nachhaltige Alternative genannt; in den technischen Regelwerken für den systematischen Rückbau (LB 410.4) fehlen derzeit jedoch noch validierte, detaillierte Verfahrensbeschreibungen für die großskalige Wiederverwendung.

Quellenbelege: LB 410.4, VDI ZRE, BVSF.

3. Typische Materialien

Die stoffliche Zusammensetzung definiert die Trennbarkeit:

* Beton und Bewehrungsstahl: Bei Stahlbetonbauteilen ist der Verbund entscheidend. Kritisch für die Wiederverwendung ist die Trennbarkeit von später aufgebrachtem Aufbeton vom ursprünglichen Fertigteil.
* Spannstahl: Hochfeste Stähle in vorgespannten Systemen, deren Spannungszustand bei der Demontage berücksichtigt werden muss.
* Holz: Primär in historischen Balkendecken, oft belastet durch Holzschutzmittel.
* Füllstoffe: Schlacken, Lehm oder Bauschutt in Balkenfächern, die im Sinne der Sortenreinheit getrennt erfasst werden müssen.

Quellenbelege: LB 410.4, VDI ZRE.

4. Konstruktive Ausbildung und Verbindungen

Die Ausbildung der Knotenpunkte bestimmt den Aufwand der Demontage. Während monolithische Ortbetonverbindungen nur durch spanende Trennverfahren gelöst werden können, bieten moderne Systeme wie die "Deltabeams Green Reuse" von Peikko (in Kombination mit Hohlkörperdecken) bereits im Design-for-Disassembly-Ansatz optimierte, demontierbare Anschlussdetails. Bei Balkendecken müssen zunächst die Füllkörper entfernt werden, um die Tragglieder (Stahl-, Holz- oder Betonbalken) freizulegen. Die Verbindungstechnik (Vergussmörtel, Schweißverbindungen oder Schraubbolzen) ist das Nadelöhr der wirtschaftlichen Bergung.

Quellenbelege: LB 410.4, BVSF.

5. Typische Herkunft im Gebäudebestand

Das „Urbane Lager“ (ca. 15 Mrd. Tonnen Materialbestand in Deutschland) ist ortsgebunden zu identifizieren:

* Wohnungsbau (1960er/70er): Hoher Anteil an seriellen Fertigteilen (Plattenbau), die sich durch Standardisierung für Bauteilbörsen eignen.
* Verwaltungs- und Skelettbau: Große Spannweiten und oft modulare Deckensysteme.
* Infrastruktur: Brückenelemente, die aufgrund ihrer hohen Betonqualität ein erstklassiges Reservoir für den selektiven Rückbau bilden.

Quellenbelege: DUH, DIN SPEC 91484, VDI ZRE.

6. Rückbau- und Demontageverfahren

Der werterhaltende Rückbau erfordert eine präzise technische Abfolge:

1. Voranalyse: Definitive Feststellung der Spannrichtung und des Verlaufs der Hauptbewehrung/Spannglieder.
2. Selektive Demontage: Bei Fertigteilen muss zunächst der Aufbeton vorsichtig entfernt werden, um die Elemente zerstörungsfrei zu lösen.
3. Herausschneiden mittels Diamantwandsägen: Ortbetonstrukturen werden präzise in handhabbare Segmente gesägt.
4. Sicherung: Einsatz von Hilfsjochen, Hebezeugen und Lastaufnahmemitteln.
5. Sonderfall Gewölbe: Hier ist das statische System zwingend zu beachten. Eingelegte oder untergespannte Zugbänder sind jeweils erst nach dem vollständigen Rückbau der Gewölbe zu trennen, um ein unkontrolliertes Versagen der Widerlager zu verhindern.

Quellenbelege: LB 410.2, 410.4, VDI ZRE, Leitfaden Berlin (Modul 1).

7. Schadensbilder, Risiken und Schadstoffe

Kontaminationen sind oft Ausschlusskriterien für den Re-Use. Zu identifizieren sind:

* POPs (Persistent Organic Pollutants): PCB in Altanstrichen/Fugenmassen, HBCD in Dämmstoffplatten (EPS/XPS) und PCP in alten Holzschutzmitteln.
* Formaldehyd: Insbesondere bei Holzwerkstoffen im Innenausbau (Grenzwert gemäß Leitfaden Berlin: 0,062 mg/m³).
* Asbest und KMF: In Spachtelmassen, Fliesenklebern oder Dämmschichten (LB 400).
* Strukturelle Mängel: Karbonatisierungstiefe, Chloridgehalt und Rissbildung mindern die Restnutzungsdauer.

Quellenbelege: LB 410.1, 410.5, Leitfaden Berlin (S. 34).

8. Prüfverfahren und Zustandsbewertung

Das Pre-Demolition-Audit (PDA) nach DIN SPEC 91484 ist zweistufig durchzuführen:

* Stufe 1 (Vorprüfung): Aufnahme von Basisdaten (Baujahr, Gebäudeklasse, grobe Mengen).
* Stufe 2 (Detailprüfung): Tiefgehende Erkundung (Schadstoffanalytik, Feststellung der Verbindungsarten, statische Bestandsaufnahme) zur Bewertung des Anschlussnutzungspotenzials.

Quellenbelege: DIN SPEC 91484, Leitfaden Berlin.

9. Tragfähigkeitsnachweis und sicherheitsrelevante Anforderungen

Die Gewährleistung der Standsicherheit ist die größte technische Hürde. Erforderlich sind:

* Nachweis der Restgebrauchseigenschaften und Prognose der Restnutzungsdauer.
* Erstellung einer Abbruchstatik zur Sicherung des Ausbauzustands (LB 410.2).
* Häufiges Fehlen von Bestandsstatiken erzwingt zerstörungsfreie oder minimalinvasive Prüfverfahren (z.B. Bewehrungsscan, Rückprallhammer).

Quellenbelege: VDI ZRE, LB 410.2/3.

10. Normen, Zulassung und rechtliche Fragen

Die Rechtslage befindet sich im Umbruch:

* EU-BauPVO (neu): Tritt am 8. Januar 2026 vollumfänglich in Kraft. Gebrauchte Produkte fallen nur dann darunter, wenn eine spezifische harmonisierte technische Spezifikation (htS) erarbeitet wurde, die den Re-Use explizit einschließt.
* BauPVO (alt - 305/2011): Gilt für gebrauchte Teile nur, wenn diese „wesentlich verändert“ werden (Änderung der Leistung, des Verwendungszwecks oder der Bauart).
* Bauordnungsrecht (BauO Bln): Da Zulassungen (abZ/abP) beim Ausbau formal erlöschen, ist meist eine Zustimmung im Einzelfall (ZiE) oder eine vorhabenbezogene Bauartgenehmigung (vBG) erforderlich.
* Abfallrecht (KrWG): Die Abfalleigenschaft kann vermieden werden, wenn vor der Entnahme ein rechtmäßiger Verwendungszweck feststeht und die Realisierung hinreichend gewiss ist.

Quellenbelege: Leitfaden Berlin (Module 2 & 3), EU-BauPVO 2024/3110.

11. Aufbereitung, Nachbearbeitung und Anpassung

Die Aufbereitung ist rechtlich als Werkleistung (Tun/Bearbeiten) und nicht als bloße Lieferung einzustufen.

* Reinigung und Entfernung von Anhaftungen.
* Anpassung der Geometrie durch Diamantsägen.
* Prüfung auf Normkonformität. Der ökologische Aufwand der Aufbereitung muss stets gegen die Neuproduktion abgewogen werden, wobei der Re-Use meist deutlich überlegen bleibt.

Quellenbelege: VDI ZRE, Leitfaden Berlin.

12. Wiederverwendungsszenarien im Neubau oder Bestand

* In-situ-Reuse: Wiedereinbau im selben Projekt (logistisch und rechtlich ideal).
* Ex-situ-Reuse: Transfer in andere Projekte des Bauherrn oder Verkauf über Börsen (z.B. Concular, restado). Die Hierarchie der Kreislaufwirtschaft priorisiert die Beibehaltung der Bauteilfunktion vor dem Downcycling.

Quellenbelege: VDI ZRE, DUH.

13. Entwurfs- und Planungsimplikationen

Planung muss dem Bestand folgen (Reverse Design). Die Formgebung orientiert sich an den verfügbaren Rastermaßen der Bestandselemente. Werkzeuge wie Madaster oder Materialpässe sind essenziell, um die Zirkularität bereits in der frühen LP 1-2 abzubilden.

Quellenbelege: DUH, VDI ZRE, DIN SPEC 91484.

14. Logistik, Lagerung und Dokumentation

Logistik entscheidet über die Abfalleigenschaft. Lagerkapazitäten sind kritisch:

* Ab 100 t (nicht gefährlich) bzw. 30 t (gefährlich) ist eine immissionsschutzrechtliche Genehmigung erforderlich, sofern die Lagerung länger als ein Jahr dauert oder nicht auf dem Entstehungsgelände erfolgt.
* Lückenlose Dokumentation (Lage im Altbau, Prüfungsergebnisse) ist für die Haftung des Verwenders unumgänglich.

Quellenbelege: Leitfaden Berlin (Modul 1), VDI ZRE.

15. Wirtschaftlichkeit

Die ökonomische Bilanz verschiebt sich durch den Wegfall der Privilegierung für juristische Personen des öffentlichen Rechts (§ 2b UStG) ab dem 01.01.2027. Der Verlust des BgA-Privilegs (Betrieb gewerblicher Art) führt zur Umsatzsteuerpflicht bei Bauteilverkäufen. Dem gegenüber stehen eingesparte Entsorgungsgebühren und Primärmaterialkosten. Ein hohes Kostensenkungspotenzial ergibt sich langfristig durch Re-Use-Frameworks (Beispiel Berliner Wohnungsbaugesellschaften).

Quellenbelege: Leitfaden Berlin, VDI ZRE.

16. Ökologische Wirkung

Das Pilotprojekt ReCreate belegt Einsparungen von bis zu 92 % der grauen Emissionen. Die DUH fordert daher konsequent eine Abrissgenehmigungspflicht, die nur erteilt wird, wenn eine Ökobilanz die ökologische Überlegenheit eines Ersatzneubaus gegenüber der Sanierung/Wiederverwendung nachweist.

Quellenbelege: VDI ZRE, DUH.

17. Fallstudien und Praxisbeispiele

* ReCreate: Nachweis der technischen Machbarkeit der Betonfertigteil-Wiederverwendung in Europa.
* Superlocal (Kerkrade, NL): Kreislauf-Areal, bei dem Material aus 500 Wohnungen vor Ort für 125 neue Einheiten genutzt wurde.
* Fahrbahnbelag/Brücke: Nutzung von aus Ortbeton gesägten Blöcken. Während für eine prototypische Bogenbrücke 25 identische Blöcke präzise aufbereitet (gebohrt für Vorspannung) wurden, kam beim Parkplatz-Fahrbahnbelag ein Mix aus Blöcken mit unterschiedlichen Abmessungen zum Einsatz.
* Stadtwerke Neustadt: Erfolgreicher Wiedereinsatz von Glastrennwänden und historischen Eichenholzelementen.

Quellenbelege: VDI ZRE.

18. Grenzen, Hemmnisse und offene Fragen

Zentrale Bottlenecks sind das Fehlen einer bundesweiten Musterumbauordnung und der mangelnde politische Wille zur Einführung einer Abrissgenehmigungspflicht. Zudem erschweren anonyme Vergabeverfahren und ungeklärte Haftungsfragen bei gebrauchten Produkten ohne CE-Kennzeichnung den Markthochlauf.

Quellenbelege: VDI ZRE, DUH.

--------------------------------------------------------------------------------
