# Fachlicher Zwischenbericht  
## Zukunft Bau Forschungsförderung — „Entwerfen mit Bestand“

**Projekt:** Entwerfen mit Bestand  
**Aktenzeichen:** 10.08.18.7-25.06  
**Zuwendungsempfängerin / Koordination:** Leibniz Universität Hannover, Fakultät für Architektur und Landschaft, IEK, Abteilung Nachhaltige Gebäudesysteme (LUH/NGS)  
**Verbundpartner:** Universität der Künste Berlin, Institut für Architektur und Städtebau, Konstruktives Entwerfen und Tragwerksplanung (UdK/KET)  
**Berichtszeitraum:** Januar 2026 bis 10.07.2026  
**Abgabedatum Zwischenbericht:** 10.07.2026  
**Arbeitsfassung:** fachlich und redaktionell geprüft, Stand [EINZUTRAGEN: Datum der internen Freigabe]

---

## Leselogik dieser Fassung

Diese Fassung ist bewusst **arbeitspaketorientiert** aufgebaut. Die vom BBSR geforderte Gliederung des Zwischenberichts — **Ergebnisse, Projektstand, Mittelverwendung und Ergebnisverwertung** — bleibt vollständig erhalten. Innerhalb dieser vier Hauptabschnitte wird der Projektstand jedoch nach den genehmigten Arbeitspaketen dargestellt:

1. **AP-Erfahrung** — Erfahrungswissen, Akteursrollen, Interviews und User-Stories  
2. **AP-Plattform** — Bauteilkatalog, Datenmodell, Plattformarchitektur und Anbindungsfähigkeit  
3. **AP-Tool** — semio-Erweiterung, LCA-, Tragwerks- und KI-Vorbereitung  
4. **AP-Validierung** — Test-Case-Logik, Referenzprojekte und spätere Erprobung

Die ergänzenden Recherchen zu Bauteilbörsen, Wiederverwendungsökosystemen, Referenzprojekten und User-Stories werden **nicht als eigenständige Marktstudie** geführt. Sie werden dort eingesetzt, wo sie eine konkrete Entscheidung im jeweiligen Arbeitspaket stützen. Das verbindende Prüfschema lautet:

> **sichtbar → beschaffbar → entwurfsfähig → bewertbar → anschlussfähig**

Damit wird vermieden, dass die Recherche nur beschreibend bleibt. Sie dient vielmehr der fachlichen Ableitung eines skalierbaren Plattform-, Bauteilkatalog- und semio-Anbindungsmodells.

**Statuslegende für die Arbeitsfassung**

| Marker | Bedeutung |
| --- | --- |
| 🟩 | zum Berichtszeitpunkt fällig und fachlich erreicht bzw. im Wesentlichen abgeschlossen |
| 🟦 | begonnen / in Bearbeitung / fachlich vorbereitet, aber noch nicht meilensteinreif |
| 🟨 | bewusst nur vorbereitend behandelt, weil späterer Meilenstein |
| ⬜ | redaktioneller oder buchhalterischer Platzhalter vor Einreichung zu ergänzen |

---

## Vorbemerkung und Bezugsgrundlagen

Der vorliegende fachliche Zwischenbericht dokumentiert den Bearbeitungsstand des Verbundvorhabens **„Entwerfen mit Bestand“** für den Zeitraum Januar 2026 bis 10.07.2026. Er folgt den Vorgaben des Zuwendungsbescheids und der Anlage „Berichtswesen“. Da das Vorhaben als Verbundprojekt durchgeführt wird, wird in den jeweiligen Abschnitten kenntlich gemacht, welche Arbeiten durch die **Leibniz Universität Hannover, Abteilung Nachhaltige Gebäudesysteme (LUH/NGS)**, und welche Arbeiten durch die **Universität der Künste Berlin, Konstruktives Entwerfen und Tragwerksplanung (UdK/KET)** bearbeitet wurden.

Der Bericht ist bewusst auf den Projektstand zum 10.07.2026 begrenzt. Entsprechend dem bewilligten Meilensteinplan steht für diesen Zwischenbericht insbesondere der Meilenstein **„Erfahrungswissen“** im Vordergrund. Die nachgelagerten Meilensteine **„Softwaredesign“**, **„Life-Cycle-Analysis Feature“**, **„Tragwerk Feature“**, **„Anbindungsfähigkeit“**, **„KI-Assistenz“**, **„Anwendungsbereit“** und **„Dokumentation“** werden nur insoweit dargestellt, wie im Berichtszeitraum Grundlagen, Anforderungen, Strukturentscheidungen oder Vorarbeiten entstanden sind. Es werden keine abgeschlossenen Softwarefunktionen, Berechnungstools, Schnittstellen, KI-Dialogsysteme, Workshops oder Veröffentlichungen behauptet, sofern sie zum Berichtszeitpunkt nicht fällig waren oder nicht durch reale Projektunterlagen belegt sind.

**Wesentliche Bezugsgrundlagen dieser Arbeitsfassung**

- Zuwendungsbescheid zum Forschungsvorhaben „Entwerfen mit Bestand“, Aktenzeichen 10.08.18.7-25.06
- Anlage 1: Zuwendungsantrag mit Arbeits-, Zeit- und Finanzierungsplan
- Anlage 3: ANBest-P
- Anlage 6: Administrativer Zwischennachweis
- Anlage 8: Berichtswesen
- interne User-Story-Sammlungen zu Architektinnen/Architekten, Bauteilbörsen, Tragwerksplanung und Energieberatung
- interne Recherchen zu Bauteilbörsen, Interface-Archetypen, Wiederverwendungsökosystemen und Referenzprojekten

---

# 1. Ergebnisse nach Arbeitspaketen

## 1.1 Zusammenfassende Ergebnislage zum 10.07.2026

Im Berichtszeitraum wurde die erste Projektphase genutzt, um die Anforderungen an eine digitale Plattform für das Entwerfen mit wiederverwendeten Baukomponenten fachlich zu schärfen. Der Schwerpunkt lag auf der Erhebung und Strukturierung von Erfahrungswissen, der Ableitung von User-Stories, der Einordnung bestehender Bauteilbörsen und Wiederverwendungsökosysteme sowie der vorbereitenden Übersetzung dieser Erkenntnisse in Anforderungen an Bauteilkatalog, Datenmodell, semio-Anbindung und spätere Bewertungsfunktionen.

Die wesentliche fachliche Erkenntnis lautet: Das Forschungsvorhaben sollte die Plattform nicht als weitere Bauteilbörse oder als isolierten Webshop verstehen. Der Mehrwert liegt in einer **Übersetzungs- und Integrationsschicht** zwischen vorhandenen Bauteilquellen, heterogenen Angebotsdaten, frühen Entwurfsmodellen, semio, späterer Ökobilanzierung, tragwerksbezogener Vorprüfung und KI-gestützter Assistenz. Die Plattform muss daher nicht nur Bauteile „anzeigen“, sondern den Übergang von sichtbaren Angeboten zu **planungsfähigen, risikobewussten und anschlussfähigen Entwurfsobjekten** unterstützen.

| Arbeitspaket | Stand zum 10.07.2026 | Ergebnislogik |
| --- | --- | --- |
| AP-Erfahrung | 🟩 Schwerpunkt des Zwischenberichts; Erfahrungswissen, Akteursrollen und User-Stories liegen als konsolidierte Arbeitsgrundlage vor | Grundlage für Human-Interface-Design und Softwaredesign |
| AP-Plattform | 🟦 Konzeptionelle und datenlogische Vorarbeiten; kein vollständiger Plattformabschluss | Bauteilkatalog, Datenreife, Bauteilkarte, Anbindungsstrategie |
| AP-Tool | 🟨 Anforderungen und Anschlusslogik vorbereitet; keine abgeschlossenen LCA-, Tragwerks- oder KI-Features | semio-Erweiterung wird aus User-Stories und Datenmodell abgeleitet |
| AP-Validierung | 🟨 Referenzprojekt- und Test-Case-Logik vorbereitet; kein abgeschlossener Workshop/Test-Case | Auswahlkriterien und Validierungsfragen für spätere Phasen |

---

## 1.2 AP-Erfahrung — Erfahrungswissen, Akteursrollen und User-Stories

### 1.2.1 Ziel des Arbeitspakets und Bearbeitungsstand

**AP-Erfahrung** dient dazu, Erfahrungswissen zum Entwurf, zur Performancebeurteilung und zu Nachweisverfahren mit wiederverwendeten Baukomponenten zu sammeln, aufzubereiten und in User-Stories für das Human-Interface-Design zu überführen. Das Arbeitspaket wird gemeinsam durch LUH/NGS und UdK/KET bearbeitet. Die Aufteilung folgt der fachlichen Ausrichtung des Verbundvorhabens: LUH/NGS fokussiert die digitale Plattform, Datenlogik, semio-Anbindung, Energie- und LCA-Perspektive; UdK/KET fokussiert die gestalterische, entwerferische und tragwerksbezogene Perspektive.

Bis zum 10.07.2026 wurde das Erfahrungswissen in eine belastbare Struktur überführt. Es wurden Akteursgruppen, Entscheidungssituationen und fachliche Konfliktfelder identifiziert und in priorisierte User-Stories übersetzt.  
⬜ **[EINZUTRAGEN: Anzahl der geführten Interviews / Gespräche / internen Auswertungssitzungen]**  
⬜ **[EINZUTRAGEN: Zeitraum und Zusammensetzung der Gesprächspartnerinnen und Gesprächspartner, sofern bereits final dokumentiert]**

Die User-Stories werden in diesem Bericht nicht als fertige Softwarefunktionen verstanden, sondern als **forschungsmethodisches Zwischenergebnis**. Sie übersetzen Erfahrungswissen in konkrete Anforderungen an Daten, Interaktion, Rollen, Risiken und Entscheidungsunterstützung.

### 1.2.2 Akteursrollen und Entscheidungssituationen

Die Auswertung zeigt, dass die Plattform nicht für eine homogene Nutzergruppe entwickelt werden kann. Wiederverwendung berührt mehrere Rollen mit unterschiedlichen Entscheidungslogiken. Für den nächsten Meilenstein „Softwaredesign“ sind insbesondere die folgenden Rollen relevant:

| Akteursrolle                       | Relevante Entscheidungssituation                                                                                              | Konsequenz für die Plattform                                                                |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Architektinnen und Architekten     | Frühe Entwurfsentscheidungen unter unsicheren Bauteildaten; Abgleich von Raster, Material, Ausdruck, Risiko und Verfügbarkeit | Bauteile müssen als Entwurfsobjekte, Variantenpakete und Risikoinformationen lesbar werden  |
| Bauteilbörsen / Plattformbetreiber | Beschreibung, Bündelung, Aktualisierung und Vermittlung heterogener Bauteile                                                  | Datenmodell muss unvollständige, aber nachvollziehbare Bauteilangaben aufnehmen können      |
| Bestandshalter / Rückbauakteure    | Erfassung, Ausbau, Lagerung, Freigabe und Weitergabe von Bauteilen                                                            | Herkunft, Zeitfenster, Standort, Status und Logistikinformationen sind zentrale Datenfelder |
| Tragwerksplanung                   | Einschätzung von Tragfunktion, Spannweiten, Querschnitten, Anschlüssen und fehlenden Nachweisen                               | Die Plattform darf keine Nachweise ersetzen, muss aber Prüfbedarf früh sichtbar machen      |
| Energieberatung / LCA              | Vergleich von Neu-, Recycling- und ReUse-Varianten im frühen Entwurf                                                          | LCA-relevante Mindestdaten und Unsicherheiten müssen strukturiert geführt werden            |
| Bauherrschaft / Projektsteuerung   | Abwägung von Kosten, Risiko, CO₂-Wirkung, Zeitfenstern und Beschaffbarkeit                                                    | Variantenvergleich und transparente Entscheidungsgrundlagen werden benötigt                 |
| Administration / Plattformbetrieb  | Qualitätssicherung, Datenstatus, Rechte, Schnittstellen und Aktualisierung                                                    | Datenreife, Quellenbezug und Statusänderungen müssen verwaltbar sein                        |

Diese Rollenstruktur ist für das Projekt zentral, weil sie begründet, warum ein einfacher Produktkatalog nicht ausreicht. Entwerfen mit wiederverwendeten Baukomponenten ist ein **mehraktorieller Abstimmungsprozess**, in dem jedes Bauteil zugleich gestalterisches Material, technisches Objekt, logistische Einheit, ökologischer Datenträger und potenzielles Risiko ist.

### 1.2.3 Konsolidierte User-Stories als zentrales Ergebnis

Die im Berichtszeitraum konsolidierten User-Stories lassen sich in fünf fachliche Cluster gliedern. Diese Cluster bilden den Kern des erreichten Meilensteins **„Erfahrungswissen“** und dienen als direkte Grundlage für den nächsten Meilenstein **„Softwaredesign“**.

| Cluster | Kernbedarf | Relevante Rollen | Priorität für Softwaredesign |
| --- | --- | --- | --- |
| Entwurfsfähigkeit von Bauteildaten | Bauteile müssen nach Typ, Maß, Menge, Zustand, Verfügbarkeit und visuellen Eigenschaften auffindbar und als digitale Entwurfsobjekte nutzbar sein | Architektur, Bauteilbörse, Plattformadministration | P1 |
| Verfügbarkeit, Prozessstatus und Reservierung | Zeitfenster, Lagerung, Ausbau, Reservierung, Statusänderungen und Lieferoptionen müssen sichtbar werden | Architektur, Bauteilbörse, Bestandshalter, Rückbau | P1 |
| Datenreife, Prüfbedarf und Risiko | Fehlende Angaben zu Statik, Brandschutz, Schall, Wärme, Schadstoffen, Gewährleistung oder Herkunft müssen kenntlich sein | Architektur, Tragwerksplanung, Energieberatung, Bauteilbörse | P1 |
| Fachliche Vorbewertung und Variantenvergleich | Varianten sollen hinsichtlich Gestaltung, Tragfähigkeit, Kosten, CO₂, Energie und Umsetzbarkeit verglichen werden können | Architektur, Tragwerksplanung, Energieberatung, Bauherrschaft | P2 |
| Dokumentation und Nachvollziehbarkeit | Entscheidungen, Annahmen, Prüfbedarfe und spätere Kennwerte müssen exportierbar werden | Tragwerksplanung, Energieberatung, Administration | P3 |

Die Priorisierung folgt nicht der technischen Attraktivität einzelner Funktionen, sondern der Frage, welche Anforderungen für ein robustes **Human-Interface-Design** und für die nächste Plattformkonzeption zuerst geklärt werden müssen. P1-Anforderungen beschreiben daher die Mindestfähigkeit der Plattform, Bauteile überhaupt planungsfähig zu machen. P2-Anforderungen betreffen spätere Bewertungs- und Variantenlogiken. P3-Anforderungen betreffen Dokumentation, Nachweisführung und Berichtsausgabe, die für spätere Projektphasen relevant werden.

### 1.2.4 Fachliche Schlussfolgerung aus AP-Erfahrung

Die User-Stories bestätigen drei grundlegende Strukturentscheidungen:

1. **Datenreife statt Vollständigkeitsfiktion:** Die Plattform muss unvollständige Bauteildaten aufnehmen können, aber fehlende Angaben eindeutig sichtbar machen. Wiederverwendete Baukomponenten sind selten vollständig dokumentiert. Ein System, das nur vollständig geprüfte Bauteile akzeptiert, wäre für frühe Entwurfsphasen zu restriktiv.
2. **Bauteilpakete statt Einzelstücklogik:** Für Entwurf und Skalierung sind wiederverwendete Komponenten nur dann relevant, wenn sie als Mengen, Chargen, Pakete oder wiederkehrende Bauteilfamilien bearbeitet werden können. Einzelne attraktive Bauteile reichen für systematische Entwurfsprozesse nicht aus.
3. **Frühe Risikointelligenz statt Scheinsicherheit:** Die Plattform darf keine technische Prüfung ersetzen. Sie muss jedoch offenlegen, wo Nachweise, Prüfungen oder fachliche Entscheidungen fehlen, damit Bauteile nicht zu früh als sichere Entwurfsgrundlage behandelt werden.

Damit ist AP-Erfahrung zum Berichtszeitpunkt fachlich so weit fortgeschritten, dass die abgeleiteten Rollen, User-Stories und Prioritäten als Grundlage für AP-Plattform und AP-Tool verwendet werden können.

---

## 1.3 AP-Plattform — Bauteilkatalog, Datenmodell, Interface-Archetypen und Anbindung

### 1.3.1 Rolle des Arbeitspakets im Berichtszeitraum

AP-Plattform umfasst den Aufbau der digitalen Plattform, Oberflächen für Entwerfende, Vertreibende und Administrierende sowie die spätere Möglichkeit, bestehende Bauteilbörsen über Schnittstellen einzubinden. Zum Berichtszeitpunkt ist dieses Arbeitspaket **nicht abgeschlossen**. Im Vordergrund standen konzeptionelle Vorarbeiten, die Auswertung bestehender Bauteilbörsen und die Ableitung eines skalierbaren Bauteilkatalog- und Datenmodells.

Die zentrale redaktionelle Korrektur gegenüber früheren Arbeitsfassungen lautet: Die Bauteilbörsen-Recherche wird nicht als allgemeiner Marktüberblick dargestellt, sondern als **Beginn des Systemdesigns**. Sie beantwortet die Frage, welche Angebotslogiken, Datenfelder und Interface-Muster eine spätere Plattform berücksichtigen muss, damit Bauteile von externen Quellen in den Entwurf überführt werden können.

### 1.3.2 Bauteilbörsen-Recherche als Systemgrundlage

Die interne Bauteilbörsen-Recherche umfasst 51 relevante Plattformen und Angebotskanäle. Der entscheidende Mehrwert der Recherche liegt nicht in der bloßen Anzahl der betrachteten Plattformen, sondern in der Reduktion auf fünf robuste Interface-Archetypen:

| Archetyp | Typische Oberfläche | Relevanz für das Projekt | Konsequenz für die Anbindung |
| --- | --- | --- | --- |
| Depot-Shop | kontrollierter Lagerbestand, Kategorien, Produktkarten, Preise oder Anfrage, Abholung | gute Produktdaten, aber oft begrenzte Herkunfts- und Nachweisinformation | geeignet für standardisierte Produktkarten und manuelle/halbautomatische Übernahme |
| Marketplace | mehrere Anbieter, Suche, Filter, Verkäuferprofil, Standort, Kontakt oder Checkout | hohe Skalierbarkeit, aber heterogene Datenqualität | benötigt Datenreifeprüfung je Listing und Verkäuferquellenbezug |
| Project/Harvest Catalogue | Bauteile aus Rückbauprojekten, Quellgebäuden, Chargen, Zeitfenstern | besonders relevant für große, tragende oder projektbezogene Bauteile | Anbindung muss Projekt, Herkunft, Zeitfenster und Chargenlogik erhalten |
| Brokered Catalogue | Angebotsliste, regionale Vermittlung, Kontaktlogik, individuelle Anfrage | lokal praxisnah, aber wenig automatisiert | eher als kuratierte Quelle; manuelle Prüfung und Kontaktstatus erforderlich |
| External/App Channel | Website nur Einstieg, echte Angebote in App oder externem Kanal | relevant als Hinweis auf Marktlogik, aber schwach als öffentlich belegbares Inventar | nicht als Inventarquelle nutzen, solange kein konkretes Listing belegt ist |

Diese Archetypen sind für das Vorhaben wichtiger als die Frage, ob eine Plattform modern aussieht oder umfangreich ist. Für „Entwerfen mit Bestand“ zählt, ob eine Quelle ein Bauteil so beschreibt, dass es in einem frühen Entwurfsprozess gefunden, bewertet, reserviert und weiterbearbeitet werden kann.

### 1.3.3 Mindestdaten für einen planungsfähigen Bauteilkatalog

Aus der Bauteilbörsen-Recherche und den User-Stories ergibt sich ein kompaktes Mindestdatenmodell. Es bildet die Grundlage für die weitere Plattformkonzeption, ohne zum Berichtszeitpunkt eine fertige Implementierung zu behaupten.

| Datenblock | Pflichtfrage | Mindestinhalt | Bedeutung für Entwurf und Skalierung |
| --- | --- | --- | --- |
| Identität | Welches konkrete Bauteil oder Paket ist gemeint? | Quelle, Plattform, Titel, ID/URL, Erfassungsdatum | verhindert Verwechslung dynamischer Angebote |
| Kategorie | Welche Bauteilfamilie liegt vor? | Bauteiltyp, Kategoriepfad, Klassifikation | ermöglicht Suche, Filterung und Zuordnung im Entwurf |
| Technische Daten | Passt das Bauteil grundsätzlich? | Maße, Menge, Einheit, Material, ggf. Marke/Modell | Voraussetzung für Raster, Geometrie, Tragwerk und LCA |
| Zustand | Wie belastbar ist das Angebot? | Zustandsbeschreibung, Schäden, Reinigung, Prüfung, Fotos | trennt Entwurfsoption von bloßer Inspiration |
| Standort und Logistik | Wo liegt das Bauteil und wie kommt es zum Projekt? | Depot/Projektort, PLZ/Radius, Abholung/Lieferung, Gewicht, Handling | bestimmt reale Beschaffbarkeit und Kosten |
| Zeit und Verfügbarkeit | Wann ist das Bauteil verfügbar? | verfügbar/reserviert/verkauft/in Prüfung, Ausbauzeitpunkt, Lagerdauer, Lieferfenster | kritisch für Entwurfs- und Bauzeitenplanung |
| Transaktion | Was kann der Nutzer tun? | kaufen, reservieren, anfragen, merken, chatten, extern öffnen | unterscheidet Shop, Marktplatz, Vermittlung und Projektkoordination |
| Herkunft und Nachweis | Woher stammt das Bauteil und welche Belege existieren? | Quellgebäude, Verkäufer, Projekt, Prüf-/Gewährleistungshinweis, CO₂-/Abfalldaten falls vorhanden | Voraussetzung für professionelle Wiederverwendung, B2B-Nutzung und spätere Nachweise |

Der wichtigste Designschluss lautet: Ein Bauteil wird für den Entwurf nicht durch ein Foto oder einen Preis relevant, sondern durch die Kombination aus **Kategorie, Menge, Maß, Zustand, Standort, Verfügbarkeit, Handlungsweg und Nachweisstatus**.

### 1.3.4 Datenreife als Plattformprinzip

Die Recherche zeigt, dass externe Bauteilquellen sehr unterschiedliche Datenqualitäten aufweisen. Daraus folgt, dass die Plattform nicht mit einem binären Schema „brauchbar / unbrauchbar“ arbeiten sollte. Stattdessen wird eine Datenreife-Logik vorbereitet:

| Datenreife | Beschreibung | Entwurfsnutzung |
| --- | --- | --- |
| Stufe 1 — sichtbar | Bauteil oder Material wird grundsätzlich sichtbar, aber konkrete Daten fehlen oder liegen nur extern vor | nur Recherchehinweis, keine belastbare Entwurfsgrundlage |
| Stufe 2 — beschaffbar | Kategorie, Ort, Menge oder Kontaktweg sind erkennbar; technische Daten sind teilweise vorhanden | für Vorstudie und Variantenidee nutzbar, aber mit Prüfhinweis |
| Stufe 3 — entwurfsfähig | Maße, Menge, Material, Zustand, Verfügbarkeit und Quelle sind ausreichend dokumentiert | als Bauteilkarte und semio-Objekt vorbereitbar |
| Stufe 4 — bewertbar | zusätzliche Daten zu Masse, Transport, Herkunft, ReUse-Status, LCA oder Tragwerk liegen vor | für Variantenvergleich und fachliche Vorbewertung geeignet |
| Stufe 5 — anschlussfähig / nachweisnah | Prüfungen, Anschlussdetails, Dokumentation und klare Verantwortlichkeiten liegen vor | für spätere Planungs- und Nachweisprozesse relevant |

Zum Berichtszeitpunkt wird diese Logik als konzeptionelles Ergebnis geführt. Sie soll verhindern, dass unvollständige Daten entweder überbewertet oder vorschnell ausgeschlossen werden.

### 1.3.5 Bauteilkarte als zentrales Plattformelement

Aus AP-Erfahrung und AP-Plattform ergibt sich die **Bauteilkarte** als zentrales Interface-Element. Sie soll kein reines Produktdatenblatt sein, sondern eine verdichtete Entscheidungsoberfläche für Entwerfende, Fachplanende und Bauteilbörsen.

Die Bauteilkarte soll perspektivisch folgende Informationsbereiche bündeln:

1. **Identifikation:** Titel, Quelle, URL/ID, Erfassungsdatum, Anbieter
2. **Bauteilbeschreibung:** Typ, Material, Maße, Menge, Einheit, Fotos, 2D-/3D-Datenstatus
3. **Verfügbarkeit:** verfügbar, reserviert, in Prüfung, verkauft, eingelagert, nicht verfügbar
4. **Herkunft:** Quellgebäude, Rückbauprojekt, bisherige Nutzung, Ausbauzeitpunkt
5. **Logistik:** Standort, Transportdistanz, Abholung/Lieferung, Lagerung, Handlingkosten
6. **Datenreife:** sichtbar, beschaffbar, entwurfsfähig, bewertbar, anschlussfähig
7. **Prüfbedarf:** Statik, Brandschutz, Schall, Wärme, Schadstoffe, Gewährleistung
8. **Entwurfsbezug:** Paketzuordnung, mögliche Nutzung, semio-Objektstatus, Variantenbezug

Diese Struktur ist ein direkter Übersetzungsschritt zwischen Bauteilbörsen und semio. Sie erlaubt, heterogene Angebotsdaten zunächst zu ordnen, bevor sie in digitale Entwurfsobjekte, Variantenlogiken oder Bewertungsfunktionen überführt werden.

### 1.3.6 Einordnung der Wiederverwendungsökosysteme

Neben der eigentlichen Bauteilbörsen-Recherche wurden drei Wiederverwendungsökosysteme ausgewertet, um die Skalierungslogik der Plattform besser zu verstehen. Sie werden nicht als Vorbilder kopiert, sondern als Muster genutzt.

**Schweiz: Netzwerk-, Screening- und Datenökosystem**  
Die Schweizer Recherche zeigt Wiederverwendung als Netzwerk aus Akteuren, Tools und Projekten. Relevante Muster sind: nationale Sichtbarkeit durch Netzwerke wie Cirkla, Screening- und Katalogisierungsleistungen durch spezialisierte Akteure wie Zirkular, digitale Produkt- und Materialpässe durch Werkzeuge wie Planular und Madaster sowie gebaute Referenzen wie K.118. Für AP-Plattform ist daraus vor allem abzuleiten, dass skalierbare Wiederverwendung nicht allein durch Marktplätze entsteht, sondern durch die Verbindung von **Akteursnetzwerk, Gebäudescreening, Katalogisierung, Matching, rechtlicher Klärung und Dokumentation**.

**RotorDC / Opalis / FCRBE / PREUSE: Prozess- und Wissensinfrastruktur**  
Die RotorDC-Recherche zeigt, dass ein wiederverwendungsfähiges System nicht nur Angebote listet, sondern auch Demontage, Aufbereitung, Lagerung, Beschreibung, Verkauf, Dokumentation, technische Leitfäden und öffentliche Skalierung verbindet. Besonders relevant für das Projekt ist die Kombination von Shop, physischer Infrastruktur, Materialbehandlung, Opalis-Verzeichnis, technischen Dokumentationen und europäischen Projekten wie FCRBE und PREUSE. Für AP-Plattform bedeutet dies: Die Plattform muss nicht alle Prozessschritte selbst abbilden, aber sie muss die Schnittstellen zwischen **Quelle, Aufbereitung, Verfügbarkeit, technischem Wissen und Entwurf** nachvollziehbar machen.

**Deutschland: verteilte Infrastruktur, Standards und Datenebene**  
Die Deutschland-Recherche zeigt keine einzelne zentrale Wiederverwendungsinfrastruktur, sondern ein verteiltes Gefüge aus digitalen Plattformen, physischen Bauteilbörsen, Prozessakteuren, zivilgesellschaftlichen Materialhubs, Normen und Dateninstrumenten. Relevante Muster sind insbesondere Pre-Deconstruction Audits, Post-Use-Konzepte, Gebäuderessourcenpässe, Materialkataster und kommunale bzw. portfolioorientierte Urban-Mining-Strategien. Für AP-Plattform folgt daraus, dass Anschlussfähigkeit nicht nur technisch, sondern auch **standardbezogen und dokumentationsfähig** verstanden werden muss.

### 1.3.7 Ergebnis von AP-Plattform zum Berichtszeitpunkt

Zum 10.07.2026 liegt kein abgeschlossenes Plattformprodukt vor. Als fachlich relevantes Zwischenergebnis liegen jedoch vor:

- eine konsolidierte Einordnung von Bauteilbörsen nach Interface-Archetypen,
- ein Mindestdatenmodell für planungsfähige Bauteilinformationen,
- eine Datenreife-Logik für unvollständige und heterogene Quellen,
- eine Bauteilkarte als zentrales Interface-Element,
- eine differenzierte Anbindungsstrategie nach Quellentyp,
- erste Strukturentscheidungen für die spätere semio-Integration.

Diese Ergebnisse sind als Vorbereitung des Meilensteins **„Softwaredesign“** zu verstehen und bilden die Grundlage für die nächsten Entwicklungsentscheidungen.

---

## 1.4 AP-Tool — semio-Erweiterung, LCA-, Tragwerks- und KI-Vorbereitung

### 1.4.1 Rolle des Arbeitspakets im Berichtszeitraum

AP-Tool umfasst die Erweiterung des bestehenden Entwurfstools **semio** für die Wiederverwendung vorhandener Baukomponenten sowie die spätere Integration von Lebenszyklus-, Tragwerks- und KI-Funktionen. Zum Berichtszeitpunkt werden keine abgeschlossenen Features behauptet. Die Arbeiten konzentrierten sich auf die Klärung, welche Informationen semio aus dem Bauteilkatalog benötigt und welche fachlichen Anforderungen aus den User-Stories für spätere Funktionen abzuleiten sind.

Die zentrale Frage lautet: Wie werden Bauteildaten aus heterogenen Quellen so aufbereitet, dass sie nicht nur als Tabellen- oder Angebotsdaten existieren, sondern als **digitale Planungsobjekte** in einem komponentenbasierten Entwurfsprozess verwendet werden können?

### 1.4.2 semio-Anschluss: vom Angebot zum Entwurfsobjekt

Aus den User-Stories der Architektinnen und Architekten ergibt sich, dass ReUse-Bauteile im Entwurf nicht als bloße Katalogeinträge oder PDFs erscheinen dürfen. Sie müssen als digitale Objekte in Entwurfsvarianten überführt werden können. Dafür werden folgende Übersetzungsschritte vorbereitet:

| Ausgangsinformation | Übersetzung in semio-Kontext | Zweck |
| --- | --- | --- |
| Bauteilkategorie, Maße, Menge | komponentenbasierte Entwurfsobjekte oder Bauteilpakete | Raster, Grundriss, Fassade und Materialkonzept prüfen |
| Zustand, Fotos, Oberfläche, Patina | gestalterische und qualitative Entwurfsinformation | Wiederverwendung als bewusste Gestaltung lesbar machen |
| Verfügbarkeit, Zeitfenster, Status | Varianten- und Reservierungslogik | Entwurf nicht auf unsichere Bestände stützen |
| Datenreife und Prüfbedarf | Risikoinformation im Entwurfsmodell | frühe Abstimmung mit Fachplanung ermöglichen |
| Herkunft, Standort, Transport | ökologische und logistische Vorbereitung | spätere LCA- und Kostenbetrachtung ermöglichen |

Zum Berichtszeitpunkt ist diese Logik als konzeptionelle Schnittstelle zwischen AP-Plattform und AP-Tool zu verstehen.

### 1.4.3 LCA-Vorbereitung: Datenbedarf statt Berechnungsversprechen

Die ökologischen User-Stories zeigen, dass Energieberatung und LCA nicht erst am Ende des Entwurfsprozesses relevant werden. Für „Entwerfen mit Bestand“ ist insbesondere die frühe Vergleichbarkeit von neuen, recycelten und wiederverwendeten Varianten relevant. Gleichzeitig muss methodisch vermieden werden, aus unvollständigen Geometrie- oder Punktwolkendaten scheinbar präzise Treibhauspotenzialwerte abzuleiten.

Für die spätere LCA-Funktion werden daher im Berichtszeitraum folgende Datenanforderungen abgeleitet:

| Anforderung                     | Bedeutung                                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------------------------- |
| Masse, Material und Menge       | Grundlage jeder überschlägigen ökologischen Bewertung                                          |
| Herkunft und ReUse-Status       | Unterscheidung zwischen neu, recycelt, wiederverwendet, hybrid ergänzt                         |
| Transportdistanz und Logistik   | Einordnung von regionalen Materialkreisläufen und Transportaufwand                             |
| Substitutionsannahme            | ökobilanzielle Bewertung muss projektspezifisch begründen, welches Primärmaterial ersetzt wird |
| Ergänzende Schichten / Upgrades | hybride Lösungen müssen als eigene Variante geführt werden                                     |
| Unsicherheit / Datenreife       | frühe Werte müssen als Abschätzung, nicht als belastbarer Nachweis gekennzeichnet werden       |

Damit wird die LCA-Funktion zum Berichtszeitpunkt nicht als implementiertes Berechnungstool, sondern als vorbereitete Bewertungslogik beschrieben.

### 1.4.4 Tragwerksvorbereitung: Prüfbedarf als Entwurfsinformation

Die tragwerksbezogenen User-Stories zeigen, dass wiederverwendete tragende Bauteile frühzeitig nach Material, Spannweite, Querschnitt, Tragfunktion, Zustand, früherer Nutzung und vorhandenen Nachweisen sortiert werden müssen. Gleichzeitig darf das System keine statische Prüfung ersetzen. Die im Berichtszeitraum abgeleitete Grundentscheidung lautet daher: Das Tragwerk Feature soll zunächst **tragwerksrelevante Filter, Datenlücken und Prüfbedarfe sichtbar machen**, bevor rechnerische Bewertungen oder Nachweisexporte entwickelt werden.

Relevante tragwerksbezogene Datenfelder sind:

- Material und Bauteiltyp,
- Querschnitt und Abmessungen,
- Spannweite und mögliche Tragfunktion,
- frühere Nutzung und Belastungsgeschichte,
- Zustand und sichtbare Schäden,
- Anschlussart und mögliche Anschlussprinzipien,
- vorhandene Bestandspläne, Prüfungen oder Materialkennwerte,
- offene Nachweise und erforderliche Prüfungen.

Diese Informationen sollen Entwerfende und Tragwerksplanende früher zusammenführen. Ziel ist nicht, unsichere Bauteile freizugeben, sondern zu verhindern, dass tragwerksrelevante Fragen erst nach einem Entwurfsfreeze sichtbar werden.

### 1.4.5 KI-Assistenz: Anforderungen und Interaktionslogik

Die KI-Assistenz ist laut Meilensteinplan erst später fällig. Im Berichtszeitraum wird daher keine funktionsfähige KI-Schnittstelle behauptet. Aus User-Stories, Bauteilkatalog und Datenreife-Logik lassen sich jedoch sinnvolle Einsatzfelder vorbereiten:

| Potenzieller KI-Use-Case | Voraussetzung | Status zum 10.07.2026 |
| --- | --- | --- |
| Vorschlagen geeigneter Bauteile für eine Entwurfssituation | strukturierte Bauteilkategorien, Maße, Mengen, Status und Entwurfsparameter | 🟨 Anforderung abgeleitet |
| Formulieren von Rückfragen bei unvollständigen Daten | Datenreife- und Prüfbedarfslogik | 🟨 Anforderung abgeleitet |
| Unterstützen bei Bauteilpaketen | Paketlogik, Ähnlichkeitskriterien, Verfügbarkeit | 🟨 Anforderung abgeleitet |
| Erklären von Risiken und offenen Nachweisen | Prüfbedarf, Datenlücken, Rollenmodell | 🟨 Anforderung abgeleitet |
| Übersetzen von Bauteilbörsendaten in semio-relevante Vorschläge | Bauteilkarte und Datenmodell | 🟨 Anforderung abgeleitet |

Die Entscheidung, KI erst nach der Strukturierung von Bauteildaten und User-Stories zu behandeln, ist fachlich notwendig. Ohne Datenmodell würde eine KI-Assistenz lediglich generische Antworten liefern und könnte den Entwurfsprozess nicht belastbar unterstützen.

### 1.4.6 Ergebnis von AP-Tool zum Berichtszeitpunkt

Zum 10.07.2026 liegen für AP-Tool keine abgeschlossenen Softwarefeatures vor. Fachlich abgeschlossen bzw. vorbereitet sind jedoch:

- Anforderungen an die Übersetzung von Bauteilkatalogdaten in semio-Entwurfsobjekte,
- Priorisierung der P1-User-Stories für den nächsten Softwaredesign-Schritt,
- Datenanforderungen für spätere LCA-Funktionen,
- Datenanforderungen und Prüfbedarfslogik für spätere Tragwerksfunktionen,
- erste Interaktionslogik für spätere KI-Assistenz.

---

## 1.5 AP-Validierung — Referenzprojekte, Test-Case-Logik und spätere Erprobung

### 1.5.1 Rolle des Arbeitspakets im Berichtszeitraum

AP-Validierung umfasst die spätere Entwicklung eines Test-Cases auf Basis realer Bestände, die testgetriebene Weiterentwicklung der Tools und einen Workshop mit Entwerfenden. Diese Schritte sind zum 10.07.2026 noch nicht als abgeschlossen zu berichten. Im Berichtszeitraum wurde jedoch vorbereitet, nach welchen Kriterien Referenzprojekte, Wiederverwendungsprozesse und spätere Test-Cases ausgewertet werden sollen.

Die Referenzprojekt-Recherche wird daher nicht als Erfolgsnachweis des eigenen Projekts verwendet. Sie dient der Ableitung von **Validierungskriterien**: Welche Arten von Bauteilen, Daten, Risiken und Prozessketten muss die Plattform später abbilden können?

### 1.5.2 Relevante Muster aus Referenzprojekten

Die Projektanalyse wurde auf Fälle konzentriert, die für direkte Wiederverwendung und komponentenbasiertes Entwerfen besonders aussagekräftig sind. Nicht jede bekannte zirkuläre Fallstudie ist für dieses Projekt gleichermaßen relevant. Priorisiert wurden Projekte, bei denen wiederverwendete feste oder tragende Bauteile, donor-to-receiver-Logiken, Bauteilpakete oder dokumentierte Materialflüsse erkennbar sind.

| Projektmuster | Relevante Referenzen | Bedeutung für „Entwerfen mit Bestand“ |
| --- | --- | --- |
| Komponentenbasierter Entwurf aus realen Beständen | K.118 / Kopfbau Halle 118; Villa Welpeloo; BioPartner 5 | Entwurf muss mit vorhandenen Bauteilen umgehen, nicht erst nachträglich Bauteile suchen |
| Wiederverwendung tragender Elemente | KA13, BioPartner 5, Recypark Demets, WBS70-/Plattenbau-Fälle | Tragwerksdaten und Prüfbedarf sind früh zu berücksichtigen |
| Same-site Urban Mining | Svanen / Gladsaxe, Thoravej 29, Rathaus Korbach in eingeschränkter Form | Standort, Ausbau, Logistik und Wiederverwendungskette müssen zusammen gedacht werden |
| Donor-to-receiver-Ketten | House of Fraser → TBC.London, Leipzig Airport, Behnisch München | zeitliche Verfügbarkeit und Reservierung sind für Entwurf und Beschaffung zentral |
| Öffentliche / kommunale Anwendung | Recypark Demets, Svanen, Forum Königsbrunn, Berlin TXL | Skalierbarkeit erfordert dokumentierbare Prozesse, nicht nur Einzelentwürfe |
| Materialpass- und Dateninfrastruktur | Madaster, DGNB Ressourcenpass, DIN SPEC 91484/91525, Heidelberg / Berlin TXL | spätere Anschlussfähigkeit an Standards und Dokumentationssysteme ist relevant |

Die Auswertung bestätigt, dass direkte Wiederverwendung dann planungsfähig wird, wenn Materialfluss, Bauteildaten, technische Prüfung, Logistik und Entwurf frühzeitig miteinander verknüpft werden. Dies stützt die Entscheidung, im Projekt nicht mit einer reinen Marktplatzlogik zu arbeiten, sondern mit einer entwurfsbezogenen Plattformlogik.

### 1.5.3 Skalierbarkeitskriterien für den späteren Test-Case

Aus der Projektauswertung werden folgende Kriterien für die spätere Validierung abgeleitet:

1. **Bauteilgruppen statt Einzelobjekte:** Der Test-Case sollte Bauteilfamilien oder Pakete enthalten, damit Mengen-, Raster- und Variantenfragen geprüft werden können.
2. **Unterschiedliche Datenreife:** Der Test-Case sollte bewusst Bauteile mit vollständigen und unvollständigen Daten enthalten, damit die Datenreife-Logik geprüft werden kann.
3. **Mindestens ein tragwerksrelevantes Szenario:** Es sollte erkennbar sein, welche Informationen für eine tragwerksbezogene Vorbewertung fehlen oder vorhanden sind.
4. **LCA-relevante Mindestdaten:** Masse, Material, Herkunft, Transport und ReUse-Status sollten so weit vorliegen, dass spätere CO₂-Vergleiche vorbereitet werden können.
5. **Zeit- und Verfügbarkeitsbezug:** Der Test-Case sollte Bauteile mit Status, Ausbauzeitpunkt oder Lieferfenster enthalten.
6. **semio-Anschluss:** Bauteile müssen als digitale Entwurfsobjekte oder Bauteilpakete in eine Entwurfssituation übersetzt werden können.
7. **Dokumentierbare Entscheidungen:** Der Test-Case sollte zeigen, welche Entwurfsentscheidungen wegen Daten, Risiken oder Verfügbarkeit getroffen wurden.

### 1.5.4 Ergebnis von AP-Validierung zum Berichtszeitpunkt

Zum 10.07.2026 wurden noch kein abschließender Test-Case und kein Workshop durchgeführt. Als fachlich relevantes Zwischenergebnis liegen jedoch Kriterien für die spätere Test-Case-Auswahl, die Bewertung von Referenzprojekten und die Validierung der Plattformlogik vor.

---

# 2. Projektstand nach Arbeitspaketen

## 2.1 Abgleich mit Meilensteinplan

Der Meilensteinplan sieht folgende Reihenfolge vor. Der vorliegende Zwischenbericht liegt im Berichtszeitraum Januar 2026 bis 10.07.2026 und damit vor den meisten funktionsbezogenen Meilensteinen.

| Meilenstein | Vorgesehener Zeitpunkt | Status zum 10.07.2026 | Bewertung |
| --- | ---: | --- | --- |
| Erfahrungswissen | nach 4 Monaten | 🟩 fachlich erreicht / konsolidiert | Akteursrollen, Entscheidungssituationen und User-Stories liegen als Arbeitsgrundlage vor |
| Softwaredesign | nach 9 Monaten | 🟦 in Vorbereitung | Datenmodell, Bauteilkarte, Archetypen und Prioritäten stützen die nächste Phase |
| Life-Cycle-Analysis Feature | nach 12 Monaten | 🟨 nicht fällig | Datenanforderungen und methodische Grenzen vorbereitet |
| Tragwerk Feature | nach 12 Monaten | 🟨 nicht fällig | Prüfbedarfe und tragwerksrelevante Datenfelder vorbereitet |
| Anbindungsfähigkeit | nach 14 Monaten | 🟨 nicht fällig | Quellentypen und Anbindungslogik vorbereitet |
| KI-Assistenz | nach 15 Monaten | 🟨 nicht fällig | Use-Cases und Voraussetzungen vorbereitet |
| Anwendungsbereit | nach 16 Monaten | 🟨 nicht fällig | keine Anwendungsbereitschaft behauptet |
| Dokumentation | nach 18 Monaten | 🟨 nicht fällig | interne Dokumentationsstruktur vorbereitet |

Der Projektverlauf entspricht damit der Logik des bewilligten Arbeitsplans. Eine Gefährdung des Projektziels wird zum Berichtszeitpunkt nicht festgestellt.  
⬜ **[EINZUTRAGEN: Falls Abweichungen aus Verwaltung/Buchhaltung/Projektsteuerung bestehen, hier konkret ergänzen.]**

## 2.2 Stand AP-Erfahrung

AP-Erfahrung ist der zentrale abgeschlossene bzw. im Wesentlichen abgeschlossene Arbeitsstand dieses Zwischenberichts. Die Ergebnisse wurden nicht als Interviewprotokolle wiedergegeben, sondern in eine für das Softwaredesign nutzbare Form überführt. Die gemeinsame Bearbeitung durch LUH/NGS und UdK/KET ist fachlich sinnvoll, da die Plattform sowohl digitale, energetische und datenbezogene als auch gestalterische und tragwerksbezogene Anforderungen aufnehmen muss.

**Bearbeitung LUH/NGS:**

- Strukturierung der Plattform- und Datenanforderungen,
- Auswertung der Bauteilbörsen- und Datenmuster,
- Ableitung von Anforderungen für LCA, Energie und semio-Anbindung,
- Konsolidierung von User-Stories für Bauteilbörse, Energieberatung und Plattformbetrieb.

**Bearbeitung UdK/KET:**

- Einordnung der entwerferischen und tragwerksbezogenen Entscheidungssituationen,
- Ableitung von User-Stories für Architektur und Tragwerksplanung,
- Bewertung der Referenzprojekte hinsichtlich direkter Bauteilwiederverwendung,
- Vorbereitung von Anforderungen an spätere Test-Case- und Validierungslogik.

## 2.3 Stand AP-Plattform

AP-Plattform befindet sich in der konzeptionellen und strukturellen Bearbeitung. Die wichtigsten Grundlagen für das spätere Softwaredesign sind vorhanden: Interface-Archetypen, Datenreife, Mindestdatenmodell, Bauteilkarte und Anbindungsstrategie. Nicht abgeschlossen sind Implementierung, produktive Schnittstellen, vollständige Nutzeroberflächen und beispielhafte reale Anbindung externer Bauteilbörsen. Diese sind späteren Projektphasen zugeordnet.

## 2.4 Stand AP-Tool

AP-Tool ist inhaltlich vorbereitet, aber nicht funktionsseitig abgeschlossen. Die semio-Erweiterung wird aus den P1-User-Stories und dem Bauteilkatalog abgeleitet. Die LCA-, Tragwerks- und KI-Anforderungen wurden bewusst als Vorarbeiten formuliert, um spätere Entwicklungsschritte methodisch belastbar zu machen und keine nicht fälligen Features zu behaupten.

## 2.5 Stand AP-Validierung

AP-Validierung ist zum Berichtszeitpunkt vorbereitend bearbeitet. Die Referenzprojekte wurden ausgewertet, um Kriterien für Test-Case, Workshop und spätere Validierung abzuleiten. Ein realer Test-Case, eine abgeschlossene Demonstration oder ein Workshop werden nicht behauptet.

## 2.6 Risiken und Steuerungsmaßnahmen

| Risiko | Relevanz | Steuerungsmaßnahme |
| --- | --- | --- |
| Heterogene Datenqualität externer Bauteilquellen | hoch | Einführung von Datenreife statt Ausschluss unvollständiger Daten |
| Verwechslung von Marktplatz und Entwurfsplattform | hoch | Plattform als Übersetzungs- und Integrationsschicht definieren |
| Überpräzise LCA-Aussagen in frühen Phasen | mittel bis hoch | Kennzeichnung von Abschätzungen, Substitutionsannahmen und Unsicherheiten |
| Tragwerksrelevante Scheinsicherheit | hoch | Prüfbedarf sichtbar machen, keine automatisierte Nachweisbehauptung |
| Veraltete oder dynamische Angebotsdaten | hoch | Erfassungsdatum, Quelle, Status und Screenshot-/Belegprotokoll führen |
| Überfrachtung der Nutzeroberfläche | mittel | Priorisierung P1/P2/P3 und phasenbezogene Darstellung |
| Abhängigkeit von externen Plattformen | mittel | quellentypabhängige Anbindungsstrategie statt einheitlicher API-Annahme |

---

# 3. Mittelverwendung nach Arbeitspaketen

## 3.1 Übersicht

Die Mittelverwendung im Berichtszeitraum steht im Zusammenhang mit der Erarbeitung der fachlichen und technischen Grundlagen des Vorhabens. Im Mittelpunkt standen Personalaufwendungen für Recherche, Analyse, Abstimmung, Strukturierung der User-Stories, AP-bezogene Konzeption und Projektkoordination.

⬜ **[EINZUTRAGEN: tatsächliche Ausgaben laut Buchhaltung LUH/NGS im Berichtszeitraum]**  
⬜ **[EINZUTRAGEN: tatsächliche Ausgaben bzw. Mittelweiterleitung / Mittelabruf UdK/KET im Berichtszeitraum]**  
⬜ **[EINZUTRAGEN: Stand Mittelanforderungen, Kassenbestand, noch nicht verausgabte Mittel]**

| Kostenposition | Stand / Beschreibung | Zuordnung |
| --- | --- | --- |
| Personal | wissenschaftliche Bearbeitung, Recherche, Auswertung, Konzeption, Abstimmung | alle AP, Schwerpunkt AP-Erfahrung und AP-Plattform |
| Reisekosten | ⬜ [EINZUTRAGEN: ggf. angefallene oder geplante Reisen] | AP-Erfahrung / AP-Validierung |
| Sach- und Materialkosten | ⬜ [EINZUTRAGEN: ggf. Software-, Cloud-, Material- oder Workshopvorbereitungen] | AP-Plattform / AP-Tool |
| Leistungen Dritter | ⬜ [EINZUTRAGEN: ggf. externe Entwicklungs-, Beratungs- oder Unterstützungsleistungen] | AP-Plattform / AP-Tool |

## 3.2 Notwendigkeit und Angemessenheit

Die geleisteten Arbeiten waren für den Projektfortschritt notwendig und angemessen, da die spätere Softwareentwicklung eine belastbare Anforderungsgrundlage benötigt. Insbesondere bei wiederverwendeten Baukomponenten besteht das Risiko, technische Entwicklung zu früh an Einzelbeispielen oder unvollständigen Angebotsdaten auszurichten. Die im Berichtszeitraum geleisteten Arbeiten reduzieren dieses Risiko, indem sie Rollen, User-Stories, Datenfelder, Datenreife, Anbindungsarten und Validierungskriterien systematisch vorbereiten.

Die Arbeit im Berichtszeitraum ist damit als methodisch erforderliche Vorphase der späteren Implementierung zu bewerten. Sie ist nicht als Verzögerung gegenüber der Softwareentwicklung zu verstehen, sondern als Voraussetzung dafür, dass Softwaredesign, semio-Anbindung, LCA-, Tragwerks- und KI-Funktionen fachlich zielgerichtet entwickelt werden können.

## 3.3 Hinweise zu Nachweisen und Verwaltung

Die Bestimmungen des Zuwendungsbescheids und der ANBest-P sind weiterhin zu beachten. Für den administrativen Zwischennachweis sind die tatsächlichen Einnahmen, Ausgaben, Bundesmittel, Eigenmittel, Drittmittel und ggf. Kassenbestände entsprechend den Verwaltungsvorgaben einzutragen. Der vorliegende fachliche Zwischenbericht ersetzt nicht die zahlenmäßige Darstellung des administrativen Zwischennachweises.

---

# 4. Ergebnisverwertung nach Arbeitspaketen

## 4.1 Verwertung der Ergebnisse aus AP-Erfahrung

Die Ergebnisse aus AP-Erfahrung werden unmittelbar für den nächsten Meilenstein **„Softwaredesign“** verwertet. Die User-Stories dienen als Priorisierungsinstrument und verhindern, dass die Plattform aus einer rein technischen Perspektive entwickelt wird. Sie machen sichtbar, welche Informationen Entwerfende, Bauteilbörsen, Tragwerksplanende und Energieberatung in welcher Planungsphase benötigen.

## 4.2 Verwertung der Ergebnisse aus AP-Plattform

Die Bauteilbörsen- und Ökosystemrecherchen werden in AP-Plattform verwertet, indem sie konkrete Strukturentscheidungen stützen:

- keine Gleichbehandlung aller externen Quellen,
- Unterscheidung von Depot-Shop, Marketplace, Project/Harvest Catalogue, Brokered Catalogue und External/App Channel,
- Einführung einer Datenreife-Logik,
- Entwicklung der Bauteilkarte als zentraler Informationsträger,
- Vorbereitung eines Screenshot- und Belegprotokolls für dynamische Quellen,
- Orientierung der Anbindung an reale Interface- und Datenmuster statt an abstrakte API-Annahmen.

## 4.3 Verwertung der Ergebnisse aus AP-Tool

Die Ergebnisse aus AP-Tool werden in die semio-Erweiterung überführt. Besonders relevant sind die Anforderungen an Bauteilpakete, digitale Entwurfsobjekte, Verfügbarkeitsstatus, Prüfbedarf, Variantenvergleich und spätere Bewertungsfunktionen. Die LCA-, Tragwerks- und KI-Vorarbeiten werden als Anforderungen für spätere Entwicklungsphasen gesichert.

## 4.4 Verwertung der Ergebnisse aus AP-Validierung

Die Referenzprojektanalyse wird für die spätere Auswahl und Ausgestaltung des Test-Cases verwertet. Die relevanten Referenzprojekte zeigen, dass Validierung nicht nur prüfen darf, ob eine Oberfläche bedienbar ist. Sie muss prüfen, ob das System den Übergang von realen Beständen zu Entwurfsobjekten, Bauteilpaketen, Datenreife, Prüfbedarf und Variantenentscheidung unterstützt.

## 4.5 Transferperspektive

Der Ergebnistransfer ist zum Berichtszeitpunkt vorbereitend angelegt. Konkrete Veröffentlichungen oder öffentliche Software-Releases werden nicht behauptet. Für die weitere Projektlaufzeit sind insbesondere folgende Transferpfade relevant:

- projektinterne Weiterentwicklung der User-Stories zu HID- und Softwaredesign-Entscheidungen,
- spätere Dokumentation von Datenmodell, Bauteilkarte und Anbindungslogik,
- spätere Nutzung der Referenzprojekt- und Bauteilbörsenanalyse im Forschungsbericht,
- spätere Open-Source- und Dokumentationsstrategie entsprechend Projektantrag,
- spätere Darstellung der Ergebnisse im Rahmen von Zukunft Bau Berichtswesen und Projektetagen.

---

# 5. Anlagen / Arbeitsgrundlagen für die weitere Projektbearbeitung

## Anlage A — Konsolidierte User-Stories nach Rolle und Priorität

Die folgende Tabelle dokumentiert die im Berichtszeitraum konsolidierten User-Stories. Sie ist als Arbeitsgrundlage für das Softwaredesign zu verstehen, nicht als Liste bereits umgesetzter Funktionen.

| Rolle | User-Story / Bedarf | Priorität | Zuordnung |
| --- | --- | --- | --- |
| Architektur | verfügbare ReUse-Bauteile bereits in Wettbewerb, Vorstudie oder Konzeptphase sehen | P1 | AP-Erfahrung / AP-Tool |
| Architektur | Bauteile nach Typ, Maß, Menge, Zustand und Verfügbarkeit filtern | P1 | AP-Plattform / AP-Tool |
| Architektur | Bauteile als digitale Planungsobjekte übernehmen | P1 | AP-Tool |
| Architektur | Entwurfsrisiken zu Statik, Brandschutz, Schall, Wärme, Schadstoffen oder Gewährleistung sehen | P1 | AP-Plattform / AP-Tool |
| Architektur | relevante Bauteile temporär reservieren | P2 | AP-Plattform |
| Architektur | mehrere Entwurfsvarianten mit unterschiedlichen Bauteilpaketen vergleichen | P2 | AP-Tool |
| Architektur | nach Oberfläche, Patina, Gebrauchsspuren und visueller Varianz sortieren | P2 | AP-Tool |
| Architektur | Änderungswarnungen bei beschädigten, verzögerten, neu bewerteten oder nicht verfügbaren Bauteilen erhalten | P2 | AP-Plattform |
| Architektur | phasenbezogene Checkliste für ReUse-Entscheidungen erhalten | P3 | AP-Tool / Dokumentation |
| Bauteilbörse | Bauteile mit Maßen, Mengen, Zustand, Fotos, Anschlussart, Standort und Verfügbarkeit beschreiben | P1 | AP-Plattform |
| Bauteilbörse | ähnliche Bauteile zu verwendbaren Paketen bündeln | P1 | AP-Plattform |
| Bauteilbörse | Ausbauzeitpunkt, Lagerdauer und Lieferfenster anzeigen | P1 | AP-Plattform |
| Bauteilbörse | Status verfügbar, reserviert, in Prüfung, verkauft, eingelagert oder nicht verfügbar verwalten | P1 | AP-Plattform |
| Bauteilbörse | Gebäudebestandsdaten in einem einheitlichen Format erhalten | P2 | AP-Plattform / Anbindung |
| Bauteilbörse | statischen, brandschutztechnischen, schadstoffbezogenen oder energetischen Prüfbedarf markieren | P1 | AP-Plattform / AP-Tool |
| Bauteilbörse | Ausbau-, Lager-, Aufbereitungs-, Transport- und Handlingkosten getrennt darstellen | P2 | AP-Plattform / LCA/Kosten |
| Tragwerksplanung | ReUse-Bauteile nach Material, Spannweite, Querschnitt, Tragfunktion, Zustand und früherer Nutzung filtern | P1 | AP-Tool |
| Tragwerksplanung | fehlende Angaben zu Belastungsgeschichte, Anschlüssen, Bewehrung, Materialqualität oder Bestandsplänen sehen | P1 | AP-Tool |
| Tragwerksplanung | vorgeschlagene Bauteilanordnungen früh kommentieren | P2 | AP-Tool / AP-Validierung |
| Tragwerksplanung | machbare Anschlussprinzipien dokumentieren | P2 | AP-Tool |
| Tragwerksplanung | Varianten mit wiederverwendeten und neuen Elementen vergleichen | P2 | AP-Tool |
| Tragwerksplanung | Berechnungen, Annahmen, Prüfresultate und Entscheidungen standardisiert exportieren | P3 | AP-Tool / Dokumentation |
| Energieberatung | wiederverwendete Bauteile mit LCA-relevanten Kennwerten verknüpfen | P2 | AP-Tool |
| Energieberatung | Masse, Material, Herkunft, Transport und ReUse-Status für frühe CO₂-Abschätzung erhalten | P1/P2 | AP-Plattform / AP-Tool |
| Energieberatung | CO₂-Effekt verschiedener Entwurfsvarianten vergleichen | P2 | AP-Tool |
| Energieberatung | vereinfachte Geometrien und thermische Zonen übernehmen | P3 | AP-Tool |
| Energieberatung | Projekt mit CO₂- und Ressourcen-Grenzwerten vergleichen | P3 | AP-Tool |
| Energieberatung | hybride Lösungen aus ReUse-Bauteil, neuen Schichten oder Upgrades erkennen | P2 | AP-Tool |
| Energieberatung | Diagramme und Kennwerte exportieren | P3 | Dokumentation / Ergebnisverwertung |

## Anlage B — Bauteilbörsen-Korpus als Arbeitsgrundlage für AP-Plattform

Die 51 betrachteten Plattformen werden nicht vollständig als Marktstudie ausgewertet, sondern als Korpus zur Ableitung von Interface- und Datenmustern. Die folgende Tabelle dokumentiert den relevanten Ausschnitt für das Systemdesign.

| # | Plattform | Land/Region | Archetyp | Datenreife laut Recherche | Relevanz für das Projekt |
| ---: | --- | --- | --- | ---: | --- |
| 1 | BatiTerre | Belgien | Depot-Shop | 3 | Produktkarten, Standort, Maße, Preis |
| 2 | Cornermat / Retrival | Belgien | Depot-Shop | 3 | Materialnavigation, Depotlogik |
| 3 | Materialenbank Leuven / Atelier Circuler | Belgien | Brokered Catalogue | 2 | regionale Materialbank, Kontaktlogik |
| 4 | RotorDC | Belgien | Project/Harvest Catalogue | 3 | Per-Building-Quelle, Shop + Herkunft |
| 5 | Bauteilbörse Bremen | Deutschland | Depot-Shop | 3 | lokaler Katalog, Lagerort, Artikeldaten |
| 6 | bauteilnetz Deutschland | Deutschland | Brokered Catalogue | 2 | Verbundkatalog, Anbieterbezug |
| 7 | Concular Shop | Deutschland | Project/Harvest Catalogue | 3 | Rückbauprojekt, B2B-Daten, Verfügbarkeit |
| 8 | Materialrest24 | Deutschland | Marketplace | 2 | Restmengen, sellerabhängige Daten |
| 9 | Restado | Deutschland | Marketplace | 3 | Stadt-/Kategoriesuche, Verkäufer-/Abhollogik |
| 10 | Genbyg | Dänemark | Depot-Shop | 3 | Lager-Webshop, Produkt- und Quellenlogik |
| 11 | Articonnex | Frankreich | Depot-Shop | 2 | ReUse-/Surplus-Shop |
| 12 | Backacia | Frankreich | Marketplace | 2 | professioneller Marktplatz mit Zeitdaten |
| 13 | BatRecup | Frankreich | External/App Channel | 1 | App-/externer Kanal, kein Inventar über Landingpage |
| 14 | Bâticycle | Frankreich | Marketplace | 2 | Anbieterprofil innerhalb Marktplatz |
| 15 | Cycle Up | Frankreich | Marketplace | 3 | Marktplatz mit professioneller Herkunfts-/Nachweislogik |
| 16 | Cycle Zéro | Frankreich | External/App Channel | 1 | App-first, externe Angebotsprüfung nötig |
| 17 | R-Place | Frankreich | Marketplace | 2 | B2B-Angebotslogik |
| 18 | RAEDIFICARE | Frankreich | Project/Harvest Catalogue | 2 | technische Lose, Beschaffungsworkflow |
| 19 | REFAIR Bordeaux | Frankreich | Project/Harvest Catalogue | 2 | Ressourcendossier, Interessenliste |
| 20 | Réempro | Frankreich | Marketplace | 2 | professionelle Listings |
| 21 | Skop Marketplace | Frankreich | Marketplace | 3 | Ort, Verkäufer, Suchradius |
| 22 | Gebruiktebouwmaterialen | Niederlande | Depot-Shop | 2 | Sortimentskatalog |
| 23 | Insert Marketplace | Niederlande | Marketplace | 2 | strukturierter ReUse-Marktplatz |
| 24 | ReSource Marktplaats | Niederlande | External/App Channel | 1 | App-Store / In-App-Angebot nötig |
| 25 | Archipel Sion Ressourcerie | Schweiz | Project/Harvest Catalogue | 2 | Ressourcerie-Inventar, Ort/Projekt |
| 26 | Baumatpool.ch | Schweiz | Marketplace | 2 | sellerbasierte Angebotslogik |
| 27 | Bauteilbörse Basel | Schweiz | Depot-Shop | 2 | regionaler Bauteilkatalog |
| 28 | Bauteilladen Winterthur | Schweiz | Depot-Shop | 2 | lokaler Shop/Katalog |
| 29 | Bauteilvermittlung Zürichsee-Oberland | Schweiz | Brokered Catalogue | 2 | Vermittlungslogik |
| 30 | Bauteilverwertung Köppel & Klein | Schweiz | Brokered Catalogue | 2 | Verkaufsseite, Kontakt/Abholung |
| 31 | GGZ@WORK Laden 2 Bauteile Zug | Schweiz | Depot-Shop | 2 | physischer Laden, Sortimentsbeleg |
| 32 | Gruner ReUse | Schweiz | Marketplace | 2 | technische Felder, Produktplattform |
| 33 | La Ressourcerie Fribourg | Schweiz | Brokered Catalogue | 2 | selektiver Materialkatalog |
| 34 | Matériuum | Schweiz | Depot-Shop | 3 | Ressourcerie-Shop, strukturierte Klassifikation |
| 35 | Matériuum Genève Ressourcerie | Schweiz | Project/Harvest Catalogue | 1 | projektspezifischer Kanal, sauber trennen |
| 36 | Ressourcerie Lausanne / Matériuum / R-UUL | Schweiz | Project/Harvest Catalogue | 1 | Kanal-/Projektbezug notwendig |
| 37 | ReUse Recycling Center Riedtwil | Schweiz | Depot-Shop | 2 | gebrauchte Bauteile im Shopkontext |
| 38 | REUZI | Schweiz | Marketplace | 2 | Agora-/Anbieterlogik |
| 39 | Salza | Schweiz | Marketplace | 3 | Radius, Freigabeprozess, Chat/Übergabe |
| 40 | Stiftung Chance BauTeile Zürich / Glattbrugg | Schweiz | Brokered Catalogue | 1 | physische soziale Infrastruktur, konkretes Listing nötig |
| 41 | useagain / Bauteilclick | Schweiz | Marketplace | 3 | PLZ-/Umkreis- und Lieferlogik |
| 42 | Wick ReUse / ROTO Baumarkt | Schweiz | External/App Channel | 1 | externes Ricardo-Angebot als Beleg nötig |
| 43 | Building Spares Market | Vereinigtes Königreich | Marketplace | 2 | Kleinanzeigenlogik |
| 44 | Enviromate | Vereinigtes Königreich | Marketplace | 3 | Radiuslogik |
| 45 | Globechain | Vereinigtes Königreich | Marketplace | 2 | Business-Marktplatz |
| 46 | Material Index | Vereinigtes Königreich | Marketplace | 3 | Audit-/Brokerage-Overlay |
| 47 | SalvoWEB | Vereinigtes Königreich | Marketplace | 3 | Marketplace-/Dealerprofil-Hybrid |
| 48 | Surplus Building & Plumbing Materials | Vereinigtes Königreich | Marketplace | 3 | collect-from-postcode, E-Commerce-Daten |
| 49 | Sustainability Yard | Vereinigtes Königreich | Marketplace | 3 | moderner Multi-Seller-Marktplatz |
| 50 | BauKarussell | Österreich | Project/Harvest Catalogue | 3 | Social-Urban-Mining-Katalog, Projektquelle |
| 51 | re:Laden / HarvestMAP Vienna | Österreich | Project/Harvest Catalogue | 3 | Karten-/Listenlogik, Quelle/Projekt |

## Anlage C — Forschungsintegration nach Arbeitspaket

| Recherche / Arbeitsgrundlage | Wichtiger Inhalt | Einordnung im Bericht |
| --- | --- | --- |
| Bauteilbörsen-Interface-Recherche | fünf Archetypen, 51 Plattformen, Datenreife, Mindestdaten, Screenshot-Protokoll | AP-Plattform, Bauteilkatalog, Anbindung |
| Swiss Reuse Bubble | Cirkla, Zirkular, K.118, Planular, Madaster, Cirkla-Scan, Netzwerk- und Dateninfrastruktur | AP-Plattform und AP-Validierung; Skalierbarkeit durch Ökosystemlogik |
| RotorDC Reuse Bubble | Shop, Demontage, Aufbereitung, Lager, Opalis, FCRBE, PREUSE | AP-Plattform; Prozesskette und Wissensinfrastruktur |
| Germany Reuse Bubble | Concular/restado, Bauteilbörsen, HdM, DIN SPEC, DGNB, Madaster, Urban Mining Index | AP-Plattform; Standards, Daten und verteilte Infrastruktur |
| Projects Research | Tier-1- und Tier-2-Direktreuse-Projekte | AP-Validierung; Kriterien für spätere Test-Cases |
| User-Stories | Architektur, Bauteilbörse, Tragwerk, Energieberatung | AP-Erfahrung; Grundlage für Softwaredesign |

## Anlage D — Screenshot- und Belegprotokoll für AP-Plattform

Für spätere Dokumentation und Vergleichbarkeit sollen Screenshots nicht beliebig gesammelt werden, sondern je Archetyp denselben Zweck erfüllen:

| Archetyp | Screenshot 1 | Screenshot 2 | Screenshot 3 | Screenshot 4 |
| --- | --- | --- | --- | --- |
| Depot-Shop | Shop-/Kategorieeinstieg | Produktkarte | Detailseite mit Daten | Standort/Abholung/Warenkorb |
| Marketplace | Suche/Filter mit Ort | Listingkarte | Verkäufer/Standort | Kontakt/Checkout/Radius |
| Project/Harvest Catalogue | Projekt-/Quellübersicht | Ressource/Charge | Verfügbarkeitsfenster | Anfrage/Interesse/Nachweis |
| Brokered Catalogue | Angebots-/Materialliste | konkrete Karte | Kontakt/Vermittlung | Standort/Abholung |
| External/App Channel | offizielle Einstiegsseite | externer/App-Kanal | echtes Listing | Aktion/Ort/Verkäufer |

Dateinamen sollten nach folgendem Muster geführt werden:

`YYYY-MM-DD_land_plattform_archetyp_ebene_kurzbeschreibung.png`

## Anlage E — Projektmuster für spätere Validierung

| Relevanzstufe | Projekte / Fälle | Verwendung im Vorhaben |
| --- | --- | --- |
| Primäre Direktreuse-Fälle | K.118, BedZED, BioPartner 5, KA13, Recypark Demets, Svanen, Villa Welpeloo | hohe Relevanz für komponentenbasiertes Entwerfen und direkte Wiederverwendung |
| Starke Vergleichsfälle | Holbein Gardens, Werkhof 29, Haus HOS, Mehrow Pilot House, Broethen Twin-House, CRCLR House, Recyclinghaus Hannover, Thoravej 29, Timber Square, TBC.London | Ableitung von Bauteilpaketen, Tragwerksfragen, Donor-to-Receiver-Prozessen und Bestands-/Neubauhybriden |
| Infrastruktur- und Prozessfälle | RotorDC, Opalis, FCRBE, PREUSE, Concular, Berlin TXL, Heidelberg Circular City, Haus der Materialisierung | Ableitung von Skalierungs-, Dokumentations- und Prozessmustern |
| Vorsichtig zu verwenden | rein konzeptionelle, nicht gebaute oder schwach belegte Fälle | nur als Kontext, nicht als Nachweis direkter Wiederverwendung |

---

# 6. Redaktionelle Prüfliste vor Einreichung

Vor der Einreichung sind folgende Punkte zu prüfen und zu ergänzen:

- ⬜ tatsächliche Anzahl, Art und Zeitraum der Interviews / Gespräche ergänzen;
- ⬜ tatsächliche Ausgaben laut Buchhaltung ergänzen;
- ⬜ ggf. Abweichungen vom Arbeits-, Zeit- oder Finanzierungsplan konkret benennen;
- ⬜ prüfen, ob interne Recherchen als Anlagen mit eingereicht oder nur im Forschungsbericht weiterverwendet werden;
- ⬜ sicherstellen, dass keine unfälligen Meilensteine als abgeschlossen dargestellt werden;
- ⬜ Schreibweise von Projektpartnern, Institutsbezeichnungen und Ansprechpartnern final prüfen;
- ⬜ Förderhinweis, Aktenzeichen und formale Einreichungsvorgaben prüfen;
- ⬜ ggf. vertrauliche interne Arbeitsstände, Namen oder nicht abgestimmte Quellen vor externer Weitergabe entfernen.

---

# Quellen- und Arbeitsgrundlagen

## Förder- und Projektunterlagen

- Zuwendungsbescheid 10.08.18.7-25.06_ZwB_mU_22.10.2025
- Anlage 1 Zuwendungsantrag
- Anlage 3 ANBest-P
- Anlage 6 Administrativer Zwischennachweis
- Anlage 8 Berichtswesen
- Weiterleitungsvertrag LUH — UdK, soweit für Arbeitspaket- und Mittelzuordnung relevant

## Interne Arbeitsgrundlagen und Recherchen

- User-Stories Architektur, Bauteilbörse, Tragwerksplanung und Energieberatung
- BAUTEILBÖRSEN_RESEARCH_INTERFACE_DATA_FINAL_CLEAN_2026-06-04
- swiss_reuse_bubble_v2
- rotor_dc_reuse_bubble_v2
- germany_reuse_bubble_v1
- PROJECTS_RESEARCH
- bisherige interne Arbeitsfassungen des Zwischenberichts

## Hinweis zur Verwendung der Recherche

Die ergänzenden Recherchen werden in diesem Zwischenbericht als interne Arbeits- und Entscheidungsgrundlage genutzt. Sie ersetzen weder eine vollständige wissenschaftliche Literaturauswertung noch die später im Forschungsbericht erforderliche quellenkritische Darstellung. Für den Zwischenbericht ist maßgeblich, dass die Recherchen die bis zum 10.07.2026 erreichten Arbeitspaket-Ergebnisse fachlich begründen und die nächsten Schritte in Richtung Softwaredesign, Bauteilkatalog, semio-Anbindung und Validierung nachvollziehbar vorbereiten.
