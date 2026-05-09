---
type: Bauteil
material: ["[[material/Beton]]", "[[material/Brettsperrholz]]", "[[material/Stahl]]"]
pruefung: ["[[pruefung/Zustandsbewertung]]"]
reuse_strategie: ["[[reuse_strategie/Direkte_Wiederverwendung]]"]
verwandt: ["[[bauteil/Betonfertigteil]]", "[[bauteil/Brettsperrholzdecke]]", "[[bauteil/Holzrahmenelement]]", "[[bauteil/Wand]]"]
---

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
