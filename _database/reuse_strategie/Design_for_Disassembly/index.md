---
entity: "reuse_strategie"
id: "Design_for_Disassembly"
title: "Design for Disassembly"
build_status: "promoted_phase42"
legacy_paths:
  - "methode\Design_for_Disassembly.md"
  - "reuse_strategie\Design_for_Disassembly.md"
  - "tragwerkssystem\Design_for_Disassembly.md"
node_kind: "knot"
legacy_type: "Methode; Reuse-Strategie; Tragwerkssystem"
---

# Design for Disassembly

## Verknüpfungen

- `../reuse_strategie/`: Direkte Wiederverwendung, selektiver Rückbau, Urban Mining, Bauteilwiederverwendung vor Recycling, Materialbanken.
- `../prozessphase/`: Konzeptphase, Vorentwurf, Entwurf, Ausführungsplanung, Ausschreibung/Vergabe, Bauausführung, Betrieb/Instandhaltung, Umbau, Rückbau.
- `../dokument/`: Materialpass, Gebäuderessourcenpass, Bauteilpass, Rückbaukonzept, Demontageanleitung, Wartungs- und Instandhaltungsplan, Prüfbericht, Schadstoffkataster, As-built-Dokumentation.
- `../logistik/`: Selektive Demontage, Baustellenlogistik, Zwischenlagerung, Transport, Reinigung/Aufarbeitung, Rücknahmesysteme.
- `../datenmodell/`: BIM/IFC, Bauteil-ID, Material- und Produktdaten, Lebenszyklusmodule, EPD-Daten, Reuse-Potential-Datenfelder, Rückbau-Sequenzen.
- `../werkzeug/`: Materialdatenbank, Gebäuderessourcenpass-Tool, BIM-Modell, QR/RFID-Markierung, digitale Marktplätze, Prüf- und Scanwerkzeuge.

## Kurzdefinition

Design for Disassembly (DfD) bezeichnet die Entwurfs- und Konstruktionslogik, Gebäude, Bauteile und Verbindungen so zu planen, dass sie am Ende einer Nutzungs-, Umbau- oder Rückbauphase zerstörungsarm, sortenrein, sicher und wirtschaftlich demontiert werden können. DfD ist nicht nur ein technisches Detailprinzip, sondern eine Voraussetzung dafür, dass spätere Wiederverwendung realistisch wird: Bauteile müssen erreichbar, lösbar, identifizierbar, prüfbar und in einem Zustand rückgewinnbar sein, der eine erneute Verwendung erlaubt.

## Relevanz für Wiederverwendung im Bauwesen

DfD verschiebt den Entwurf vom einmaligen Errichten zum mehrfachen Nutzen von Bauteilen. Für Wiederverwendung ist entscheidend, dass die im Bauwerk gespeicherten Werte nicht durch verklebte Schichten, zerstörende Befestigungen, fehlende Dokumentation oder nicht zugängliche Installationen verloren gehen. Ein Gebäude kann nur dann als zukünftiges Bauteillager funktionieren, wenn die spätere Demontage bereits im Entwurf mitgedacht wird.

Relevante Wirkungen:

- Erhöht die Wahrscheinlichkeit direkter Wiederverwendung, weil Bauteile ohne große Beschädigung ausgebaut werden können.
- Reduziert Downcycling und Entsorgung, weil Materialien sortenrein getrennt werden.
- Unterstützt Reparatur, Austausch und Anpassbarkeit während der Nutzungsphase.
- Verbessert die Datenbasis für Materialpässe, Gebäuderessourcenpässe und Rückbaukonzepte.
- Macht zirkuläre Ausschreibung überprüfbar, weil Anforderungen an Demontierbarkeit, Verbindungsarten und Dokumentation beschreibbar werden.
- Verringert Risiken im späteren Rückbau, wenn Demontagereihenfolge, Befestigungssysteme, Schadstoffe und Bauteilqualitäten dokumentiert sind.

## Fachinhalt

### Begriffliche Abgrenzung

- **Design for Disassembly**: Fokus auf lösbare, zugängliche, dokumentierte Verbindungen und zerstörungsarme Trennung von Bauteilen.
- **Design for Deconstruction**: häufig breiter verwendet; umfasst die Planung des geordneten Rückbaus eines gesamten Bauwerks einschließlich Baustellenlogistik, Arbeitssicherheit und Materialströmen.
- **Design for Adaptability**: Fokus auf Nutzungsänderung, Erweiterbarkeit, Umbaubarkeit und Austausch einzelner Schichten während des Betriebs.
- **Design for Recycling**: kann auch dann erfüllt sein, wenn Bauteile nicht wiederverwendbar sind, aber als Materialstrom recycelt werden können. Für Wiederverwendung reicht Recyclingfähigkeit nicht aus.
- **Reversible Building Design**: in BAMB und verwandten Forschungsansätzen verwendeter Begriff für Bauweisen, die technische Rückbaubarkeit, Anpassbarkeit und Informationssysteme verbinden.

### Grundprinzipien

1. **Schichtentrennung nach Lebensdauer**  
   Tragwerk, Gebäudehülle, Ausbau, technische Gebäudeausrüstung und Oberflächen altern unterschiedlich. DfD verlangt, dass kurzlebige Schichten gewechselt werden können, ohne langlebige Schichten zu zerstören. Kritisch sind besonders Fassadenanschlüsse, abgehängte Decken, Bodenaufbauten, Installationsschächte und brandschutztechnische Kapselungen.

2. **Reversible Verbindungen**  
   Bevorzugt werden Schraub-, Bolzen-, Klemm-, Steck-, Spann-, Einhänge- und lösbare Systemverbindungen. Problematisch sind vollflächige Verklebungen, Nassverbund, Ortbetonverguss, nicht zugängliche Schweißnähte, Verbundestriche, Verbunddämmungen und Beschichtungen, die nur zerstörend entfernt werden können. Schweißverbindungen sind nicht grundsätzlich ausgeschlossen, erschweren aber Bauteilwiederverwendung häufig, wenn sie nur durch Trennen mit Materialverlust lösbar sind.

3. **Zugänglichkeit und Demontagereihenfolge**  
   Eine Verbindung ist nur dann kreislauffähig, wenn sie im eingebauten Zustand gefunden, erreicht und mit vertretbarem Werkzeugaufwand gelöst werden kann. DfD benötigt daher sichtbare oder dokumentierte Befestigungspunkte, Revisionsöffnungen, ausreichende Arbeitsräume, definierte Hebe- und Anschlagpunkte und eine plausible Rückbaufolge.

4. **Sortenreinheit und Materialverträglichkeit**  
   Sortenreine Bauteile sind leichter zu prüfen, aufzubereiten und wieder einzusetzen. Verbundmaterialien müssen so gewählt werden, dass ihre Schichten trennbar oder zumindest klar deklariert sind. Schadstoffe, problematische Flammschutzmittel, alte Beschichtungen, Asbest, PCB, PAK, bleihaltige Anstriche oder kontaminierte Dämmstoffe können Wiederverwendung ausschließen oder auf bestimmte Anwendungen beschränken.

5. **Standardisierung ohne Entwurfsverarmung**  
   Wiederverwendung profitiert von modularen Rastermaßen, wiederholbaren Geometrien, gängigen Querschnitten, toleranzfähigen Details und austauschbaren Systemkomponenten. Standardisierung darf jedoch nicht mit Monotonie verwechselt werden: entscheidend ist die funktionale und geometrische Anschlussfähigkeit zukünftiger Nutzungen.

6. **Robustheit und Mehrfachnutzung**  
   DfD-Bauteile müssen nicht nur demontierbar, sondern auch transportierbar, lagerfähig, prüfbar und erneut montierbar sein. Relevante Merkmale sind Überdimensionierungsreserven, Oberflächenrobustheit, Korrosionsschutz, Kanten- und Eckschutz, lösbare Verschleißteile und verfügbare Ersatzteile.

7. **Dokumentation als Teil des Entwurfs**  
   Ohne Information verliert ein demontierbares Bauteil einen großen Teil seines Wiederverwendungspotenzials. Notwendig sind eindeutige Bauteil-IDs, Materialangaben, Hersteller- und Produktdaten, Maße, Masse, Einbauort, Verbindungsmittel, Prüfwerte, Wartungshistorie, Schadstoffinformationen, Demontagehinweise und As-built-Abweichungen.

8. **Planung für Prüfung und Zulassung**  
   Wiederverwendete Bauteile benötigen im Folgeprojekt Nachweise. DfD sollte daher bereits im Erstprojekt Prüfzugänglichkeit, Kennzeichnung, reversible Brandschutzbekleidungen, dokumentierte Lastannahmen, Materialchargen und Qualitätskontrollen ermöglichen.

### Kriterien nach Bauteilgruppen

**Tragwerk**

- Stahltragwerke: besonders geeignet bei verschraubten/gebölzten Verbindungen, standardisierten Profilen, dokumentierten Stahlgüten, Korrosionsschutz und nachvollziehbarer Belastungsgeschichte. Schweißnähte, Brandschutzbeschichtungen und nicht dokumentierte Ermüdungsbeanspruchung sind kritisch.
- Holztragwerke: gute Chancen bei trocken montierten, verschraubten oder gezapften Elementen, klarer Feuchteführung, zugänglichen Verbindungsmitteln und dokumentierter Holzqualität. Kritisch sind verklebte Verbundsysteme, verdeckte Feuchteschäden, Pilzbefall, Insektenbefall und Brandschutzauflagen.
- Betonfertigteile: Wiederverwendung ist möglich, aber anspruchsvoll. Wichtig sind lösbare Lagerungen, nicht vergossene Anschlüsse, Transport- und Anschlagpunkte, dokumentierte Bewehrung, Betonfestigkeit, Carbonatisierung, Chloridbelastung und Risszustand. Ortbeton und Nassverbund reduzieren Wiederverwendung stark.

**Fassade und Gebäudehülle**

- Demontierbare Fassadenkassetten, vorgehängte hinterlüftete Fassaden, verschraubte Unterkonstruktionen und austauschbare Dichtungssysteme sind vorteilhaft.
- Fenster und Verglasungen benötigen Nachweise zu U-Wert, Dichtheit, Sicherheitsglas, Beschlägen, Restlebensdauer und Maßtoleranz. Energetische Anforderungen können Wiederverwendung einschränken, wenn alte Bauteile aktuelle Anforderungen nicht erfüllen.
- Wärmedämmverbundsysteme sind wegen Verklebung, Putzschichten und Materialverbund häufig schwer wiederzuverwenden; sie sind eher ein Beispiel für recycling- oder entsorgungsorientierte Rückbaustrategien.

**Innenausbau**

- Systemtrennwände, Doppelböden, abgehängte Decken, Leuchten, Türen, Beschläge, Sanitärobjekte, Bodenplatten, Natursteinplatten und Möbel sind häufige DfD-Kandidaten.
- Hohe Wiederverwendungschancen bestehen bei sichtbarer Verschraubung, Standardmaßen, leichter Reinigung, geringen Sicherheitsanforderungen und geringem Schadstoffrisiko.

**Technische Gebäudeausrüstung**

- TGA ist wegen schneller technologischer Alterung, Hygieneanforderungen, Brandschutz, Energieeffizienz und Normkonformität schwieriger. DfD-relevant sind zugängliche Schächte, modulare Leitungsführungen, lösbare Steck-/Klemmverbindungen, Austauschbarkeit von Aggregaten und klare Kennzeichnung.
- Bei Lüftung, Sanitär, Elektro und Brandschutz sind Wiederverwendung und Gewährleistung besonders projekt- und komponentenabhängig zu prüfen.

### Planungs- und Nachweislogik

DfD muss früh beginnen. In der Konzeptphase werden Raster, Gebäudetiefe, Schichten, Tragwerksprinzip und technische Infrastruktur festgelegt. In der Ausführungsplanung werden Details, Verbindungsmittel, Toleranzen, Wartungszugänge und Demontagesequenzen verbindlich. In der Ausschreibung müssen reversible Verbindungen, Dokumentationspflichten, Kennzeichnung und Rückbauinformationen als Leistungen beschrieben werden. Während Bau und Betrieb sind Abweichungen, Reparaturen und Austauschvorgänge in der As-built-Dokumentation zu aktualisieren.

Belastbare DfD-Nachweise können enthalten:

- Demontageplan mit Sequenz, Werkzeugen, Risiken, Hebepunkten und Arbeitsschutz.
- Bauteilliste mit Masse, Material, Verbindungsmittel, Lebensdauer, Einbauort und Wiederverwendungspotenzial.
- Kennzeichnungssystem am Bauteil oder im digitalen Modell.
- Anteil zerstörungsfrei demontierbarer Masse oder Bauteilwerte.
- Anteil sortenrein trennbarer Materialströme.
- Liste kritischer irreversibler Anschlüsse.
- Nachweis, dass Wartung, Reparatur und Austausch ohne Eingriff in Primärbauteile möglich sind.
- Übergabe eines Gebäuderessourcenpasses oder Materialpasses.

### Bewertungsmaßstäbe und KPIs

Für Forschung und Praxis sind folgende Kennwerte belastbarer als pauschale Aussagen zur „Kreislauffähigkeit“:

- Masseanteil zerstörungsfrei demontierbarer Bauteile.
- Wertanteil zerstörungsfrei demontierbarer Bauteile.
- Anzahl und Anteil reversibler Verbindungspunkte.
- Zeitaufwand der Demontage je Bauteil oder Quadratmeter.
- Anteil sortenrein trennbarer Materialien.
- Anteil wiederverwendungsfähiger Bauteile nach technischer Prüfung.
- Dokumentationsvollständigkeit je Bauteilgruppe.
- Austauschbarkeit von Verschleißteilen.
- Verfügbarkeit von Ersatzteilen und Herstellerinformationen.
- Grad der Zugänglichkeit von Befestigungen und Installationen.

### Einordnung in Standards und Frameworks

- ISO 20887 behandelt Prinzipien, Anforderungen und Leitlinien für Demontierbarkeit und Anpassbarkeit von Gebäuden und Ingenieurbauwerken. Sie ist ein wichtiger Referenzrahmen, ersetzt aber keine projektspezifische technische Prüfung.
- Level(s) der Europäischen Kommission adressiert unter anderem Lebenszyklusdenken, Anpassbarkeit und Rückbaubarkeit als Teil ressourceneffizienter Gebäudeplanung.
- DGNB TEC1.6 und der DGNB-Gebäuderessourcenpass bieten im deutschsprachigen Raum anschlussfähige Nachweislogiken für Zirkularität, Rückbau- und Recyclingfreundlichkeit.
- BAMB verbindet Materialpässe und reversible Gebäudeplanung als zwei komplementäre Bausteine: Bauteile müssen technisch rückgewinnbar und zugleich datenmäßig identifizierbar sein.

## Praxisbezug / Beispiele

- **Stahlhallen und Industriegebäude**: Verschraubte Stahltragwerke mit standardisierten Profilen sind klassische Beispiele für hohe DfD-Eignung. Entscheidend bleiben Dokumentation von Stahlgüte, Verbindungsmitteln, Korrosionsschutz und Belastungsgeschichte.
- **Systemtrennwände und Doppelböden im Büroausbau**: Häufig demontierbar, marktgängig und logistisch handhabbar. Sie zeigen, dass DfD dort besonders funktioniert, wo Produkte modular, zugänglich und wiederholt nachgefragt sind.
- **UMAR / NEST, Dübendorf**: Forschungs- und Demonstrationsprojekt, das reversible Konstruktionen, Materialpässe und kreislauffähige Materialwahl experimentell verbindet.
- **Rathaus Brummen, Niederlande**: Oft zitiertes Beispiel für ein Gebäude, das mit Blick auf spätere Demontage und temporäre Nutzung entworfen wurde. Die Übertragbarkeit hängt von Nutzung, Vergabemodell und regionalem Rechtsrahmen ab.
- **Fassadenkassetten und vorgehängte Fassaden**: Bei mechanischer Befestigung, dokumentierten Paneelen und zugänglicher Unterkonstruktion gut rückbaubar. Problematisch sind verklebte Schichten, objektspezifische Sondermaße und fehlende Ersatzteile.

## Herausforderungen / offene Fragen

- **Recht und Gewährleistung**: Wiederverwendbarkeit am Ende der ersten Lebensdauer garantiert noch keine Zulassung im nächsten Projekt. Tragfähigkeit, Brandschutz, Schallschutz, Hygiene und Energieanforderungen müssen neu geprüft werden.
- **Kostenverteilung**: DfD erzeugt Mehrarbeit in Planung und Dokumentation, während der Nutzen oft erst für spätere Eigentümer oder Nutzer entsteht. Geschäftsmodelle und Anreizsysteme sind noch nicht überall etabliert.
- **Dokumentationspflege**: Materialpässe verlieren Wert, wenn Umbauten und Instandhaltung nicht fortgeschrieben werden.
- **Konflikt mit kurzfristiger Optimierung**: Verklebte, vergossene oder hochintegrierte Lösungen können kurzfristig billig, dünn oder schnell sein, sind aber langfristig schlecht demontierbar.
- **Normative Lücken**: Es gibt Referenzstandards und Bewertungssysteme, aber keine flächendeckend verbindliche deutsche Standardmethode, die DfD-Nachweise für alle Bauteilgruppen einheitlich regelt. Anforderungen sind regional, projektspezifisch und vom Gebäudetyp abhängig.
- **Technische Alterung**: TGA, Dichtungen, Beschichtungen, Brandschutzsysteme und energetische Bauteile können trotz Demontierbarkeit technisch veraltet sein.
- **Marktfähigkeit**: Ein demontiertes Bauteil muss nicht nur technisch intakt, sondern auch nachgefragt, lagerbar, transportierbar, versicherbar und wirtschaftlich attraktiv sein.

## Quellen

- ISO 20887:2020, *Sustainability in buildings and civil engineering works — Design for disassembly and adaptability — Principles, requirements and guidance*. https://www.iso.org/standard/69370.html
- Europäische Kommission, Level(s) – European framework for sustainable buildings. https://environment.ec.europa.eu/topics/circular-economy/levels_en
- Europäische Kommission / BUILD UP, *Circular economy principles and how to design buildings*. https://build-up.ec.europa.eu/en/resources-and-tools/publications/circular-economy-principles-and-how-design-buildings
- BAMB – Buildings as Material Banks, Material Passports und Reversible Building Design. https://www.bamb2020.eu/ und https://www.bamb2020.eu/topics/materials-passports/
- CORDIS, BAMB project summary. https://cordis.europa.eu/project/id/642384
- DGNB, Gebäuderessourcenpass. https://www.dgnb.de/de/nachhaltiges-bauen/zirkulaeres-bauen/gebaeuderessourcenpass
- DGNB, Kriterium TEC1.6 Zirkuläres Bauen / Rückbau- und Recyclingfreundlichkeit. https://www.dgnb.de/de/zertifizierung/gebaeude/neubau/kriterien
- FCRBE / Interreg NWE, Reuse Toolkit und Leitfäden zur Wiederverwendung rückgewonnener Bauteile. https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- Guy, B.; Ciarimboli, N. (2005): *Design for Disassembly in the Built Environment: A Guide to Closed-Loop Design and Building*. Hamer Center / Pennsylvania State University.
- Crowther, P. (2005): *Design for Disassembly – Themes and Principles*. RAIA/BDP Environment Design Guide.
- Brand, S. (1994): *How Buildings Learn: What Happens After They’re Built*. Viking.

# Design for Disassembly

## Verknüpfungen

- `../methode/Design_for_Disassembly.md` – operative Methoden, Checklisten, Detailprinzipien und Bewertungsansätze.
- `../methode/Materialpass.md` – Dokumentation von Bauteilen, Verbindungen, Demontagefolge und Materialdaten.
- `../methode/Urban_Mining.md` – zukünftiger Bestand als geplanter Rohstoff- und Bauteilspeicher.
- `../methode/Selektiver_Rueckbau.md` – spätere Rückbauphase, die durch DfD vorbereitet wird.
- `../methode/Lebenszyklusanalyse.md` – Bewertung von Wiederverwendungs-, Reparatur- und Recyclingpotenzialen.
- `../projekt/UMAR_NEST.md`, `../projekt/Zirkulaeres_Bauen.md`, `../projekt/Bauteilpass.md`.
- `../fallstudie/UMAR.md`, `../fallstudie/K118_Kopfbau_Halle_118.md`, `../fallstudie/Demontierbarer_Holzbau.md`.
- `../tragwerkssystem/Holztragwerk.md`, `../tragwerkssystem/Stahltragwerk.md`, `../tragwerkssystem/Modulbau.md`, `../tragwerkssystem/Fassade.md`, `../tragwerkssystem/Ausbau.md`.
- `../verbindung/Schraubverbindung.md`, `../verbindung/Bolzenverbindung.md`, `../verbindung/Klemmverbindung.md`, `../verbindung/Steckverbindung.md`, `../verbindung/Trockene_Fuge.md`, `../verbindung/Schweissverbindung.md`, `../verbindung/Klebverbindung.md`.
- `../huerde/Irreversible_Verbindungen.md`, `../huerde/Materialverbund.md`, `../huerde/Dokumentationsverlust.md`, `../huerde/Normung.md`, `../huerde/Brandschutz.md`, `../huerde/Wirtschaftlichkeit.md`.

## Kurzdefinition

Design for Disassembly (DfD) ist eine Entwurfsstrategie, die Gebäude, Bauteile und Verbindungen so plant, dass sie am Ende einer Nutzungsphase zerstörungsarm, sortenrein, sicher und wirtschaftlich demontiert, repariert, ersetzt, wiederverwendet, remanufactured oder hochwertig recycelt werden können. Im Bauwesen wird DfD häufig zusammen mit **Design for Adaptability** gedacht: Gebäude sollen nicht nur rückbaubar, sondern auch während ihrer Lebensdauer an neue Nutzungen anpassbar sein.

In dieser Datei wird DfD als **strategische Voraussetzung zukünftiger Wiederverwendung** beschrieben. Die konkrete Methoden-Datei kann Checklisten, Bewertungsraster und Detailkataloge enthalten; hier steht die Rolle von DfD innerhalb der Reuse-Strategien im Vordergrund.

Abgrenzung:

- **DfD**: plant zukünftige Demontage und Wiederverwendung bereits im Neubau oder Umbau ein.
- **Selektiver Rückbau**: führt Demontage an bestehenden Gebäuden aus; DfD erleichtert ihn, ersetzt ihn aber nicht.
- **Direkte Wiederverwendung**: nutzt Bauteile erneut; DfD erhöht die Wahrscheinlichkeit, dass diese Bauteile später wiederverwendbar sind.
- **Recyclinggerechtes Bauen**: zielt auf sortenreine Stoffströme; DfD priorisiert Produkt- und Bauteilerhalt vor stofflicher Verwertung.
- **Modulares Bauen**: kann DfD unterstützen, ist aber nicht automatisch demontierbar, wenn Module verklebt, vergossen oder schlecht dokumentiert sind.
- **Flexibles Bauen**: erleichtert Nutzungswechsel; DfD ergänzt Flexibilität um Rückbau- und Wiederverwendungsfähigkeit.

## Relevanz für Wiederverwendung im Bauwesen

Viele heutige Wiederverwendungsprobleme entstehen nicht erst beim Rückbau, sondern bereits beim ursprünglichen Entwurf: verklebte Schichten, unzugängliche Befestigungen, fehlende Bauteildaten, untrennbare Verbundmaterialien, individuelle Sonderformate und mangelhafte Dokumentation. DfD adressiert diese Ursachen.

Für das Entwerfen mit Bestand hat DfD zwei Rollen:

1. **Bei neuen Ergänzungen im Bestand**  
   Alles, was heute in einen Bestand eingebaut wird, soll später wieder lösbar sein. Dadurch wird Weiterbauen im Bestand nicht zur nächsten Rückbauhürde.

2. **Bei Neubauten als künftiger Bestand**  
   Gebäude werden als zukünftige Bauteillager geplant. Materialpässe, reversible Verbindungen und robuste Module schaffen eine Grundlage für spätere direkte Wiederverwendung.

DfD ist damit keine Wiederverwendung im engeren Sinn, sondern eine **präventive Reuse-Strategie**. Es verschiebt die Verantwortung von der Abbruchphase in die Planungsphase.

## Fachinhalt

### Grundprinzipien

- **Zugänglichkeit**: Verbindungen, Befestigungen und Installationen müssen erreichbar sein.
- **Reversibilität**: Bauteile sollen gelöst werden können, ohne sie oder angrenzende Bauteile zu zerstören.
- **Sortenreinheit**: Materialschichten und Produkte sollen trennbar bleiben.
- **Mechanische statt chemische Verbindung**: Schrauben, Bolzen, Klemmen, Stecken und trockene Fugen bevorzugen; Kleben, Vergießen und Ausschäumen minimieren.
- **Schichtenprinzip**: Tragwerk, Hülle, Ausbau und TGA haben unterschiedliche Lebensdauern und sollten unabhängig austauschbar sein.
- **Standardisierung und Modularität**: Wiederholbare Maße und Bauteile erhöhen künftige Marktgängigkeit.
- **Robuste Toleranzen**: Bauteile sollen auch in anderen Kontexten einbaubar sein.
- **Kennzeichnung und Dokumentation**: Bauteile, Materialien, Hersteller, Prüfwerte, Einbauorte und Demontagefolge dokumentieren.
- **Wartbarkeit**: Regelmäßige Instandhaltung muss ohne zerstörende Eingriffe möglich sein.
- **Sicherer Rückbau**: Demontagefolge, Hebepunkte, Lasten, Gefahrenstoffe und Reststabilität mitdenken.

### Anforderungen nach Gebäudeschicht

- **Tragwerk**: Schraub- und Bolzenverbindungen, lösbare Knoten, klare Lastpfade, zugängliche Verbindungsmittel, Materialkennzeichnung. Schwierigkeit: Brandschutzbekleidungen, Schweißverbindungen, Ortbetonmonolithe.
- **Fassade**: Elementierung, austauschbare Dichtungen, lösbare Unterkonstruktion, Trennung von Bekleidung, Dämmung und Tragstruktur. Schwierigkeit: Wärmedämmverbundsysteme, Verklebungen, schwer trennbare Paneele.
- **Dach**: lösbare Abdichtungs- und Begrünungsschichten sind schwierig; mechanisch befestigte Systeme und klare Schichten helfen.
- **Ausbau**: reversible Trennwände, demontierbare Decken, Hohlraum- und Doppelböden, sichtbare Befestigungen, sortenreine Bodenbeläge.
- **TGA**: zugängliche Schächte, austauschbare Komponenten, flexible Trassen, keine Einbetonierung, digitale Dokumentation.
- **Verbindungen**: Konstruktive Details sind der Kern von DfD. Eine wiederverwendbare Materialwahl verliert ihren Wert, wenn die Verbindung zerstörend ist.

### Kriterien für DfD-taugliche Planung

- Verbindung ist sichtbar, erreichbar oder in Plänen eindeutig lokalisierbar.
- Verbindung kann mit Standardwerkzeugen gelöst werden.
- Demontagefolge ist logisch und ohne vollständige Zerstörung angrenzender Schichten möglich.
- Bauteil kann transportiert und wieder eingebaut werden.
- Bauteil hat eigenständige Trag-, Schutz- oder Nutzfunktion und ist nicht nur Teil eines irreversiblen Verbunds.
- Material- und Produktdaten bleiben über Lebensdauer verfügbar.
- Bauteil besitzt Maße und Leistungsdaten, die künftige Wiederverwendung realistisch machen.
- Wartung und Teilaustausch sind vorgesehen.
- Schadstoffe und problematische Beschichtungen werden vermieden.
- Rückbau ist sicher, auch wenn Gebäude teilweise demontiert wird.
- Neue Bauteile im Bestand beeinträchtigen die Demontage bestehender wertvoller Bauteile nicht.

### Strategische Entscheidungen

- **Produkt- vor Stoffkreislauf**: zuerst Wiederverwendung des Bauteils ermöglichen, dann Remanufacturing, dann Recycling.
- **Lebensdauer entkoppeln**: kurzlebige Schichten dürfen langlebige Schichten nicht zerstören.
- **Dokumentation als Bauteilwert**: Ohne Daten sinkt künftiger Wiederverwendungswert.
- **Weniger Verbund, mehr Fuge**: Trennbarkeit ist oft wichtiger als maximale Anfangsoptimierung.
- **Reparierbarkeit planen**: DfD beginnt nicht erst beim Rückbau, sondern bei Wartung und Austausch.
- **Bestandsumbau nicht verschlechtern**: Ergänzungen müssen die spätere Wiederverwendung des Bestands unterstützen.
- **Brandschutz integriert denken**: Brandschutz darf Demontage nicht vollständig unmöglich machen; demontierbare Bekleidungen und lösbare Kapselungen prüfen.
- **Materialgesundheit**: Schadstoffarme Materialien erhöhen zukünftige Wiederverwendungschancen.

### Vorteile

- Erhöht zukünftige direkte Wiederverwendung und hochwertige Verwertung.
- Reduziert Rückbaukosten und Abfallmengen in späteren Lebenszyklen.
- Erleichtert Reparatur, Wartung und Austausch.
- Unterstützt Anpassungsfähigkeit bei Nutzungswechseln.
- Erhöht Transparenz durch Materialpässe und Dokumentation.
- Kann Bauteilrestwerte sichtbar machen.
- Verbessert Sicherheit beim Rückbau.
- Stärkt zirkuläre Geschäftsmodelle wie Rücknahme, Leasing, Produkt-Service-Systeme und Reuse-Marktplätze.
- Macht Gebäude zu planbaren Materialdepots.

### Grenzen

- DfD verursacht oft höheren Planungsaufwand und manchmal höhere Anfangskosten.
- Spätere Wiederverwendung bleibt unsicher, weil Märkte, Normen und Anforderungen sich ändern.
- Reversible Verbindungen können Anforderungen an Feuer, Schall, Luftdichtheit oder Feuchte erschweren.
- Nicht jedes Material oder System ist sinnvoll demontierbar.
- Dokumentation muss über Jahrzehnte gepflegt werden.
- Eigentümerwechsel und fehlende Datenpflege gefährden Materialpässe.
- Optimierung auf Demontage kann mit anderen Zielen kollidieren, z. B. Robustheit, Kosten, Brandschutz oder Schallschutz.
- Standardisierung kann gestalterische und lokale Anpassung einschränken.
- Ohne Rückbauinfrastruktur bleibt DfD theoretisch.

### Relevante Akteure

- Bauherrschaft: Kreislaufziele, Budget, langfristige Wertstrategie.
- Architekt:innen: Schichtentrennung, Detailprinzipien, Materialwahl.
- Tragwerksplanung: lösbare Knoten, Lastpfade, Demontagestabilität.
- TGA-Planung: zugängliche, austauschbare Systeme.
- Brandschutz- und Bauphysikplanung: reversible Lösungen trotz Anforderungen.
- Hersteller: Produktdesign, Rücknahme, Ersatzteile, Dokumentation.
- Bauunternehmen und Handwerk: ausführbare, dokumentierte Verbindungen.
- Facility Management: Pflege von Daten, Wartung, Austausch.
- Rückbauunternehmen: Rückbauwissen bereits in Planung einbringen.
- Behörden und Zertifizierungssysteme: Anreize und Nachweismethoden.
- Digitale Plattformen / Materialpassanbieter: langfristige Datenhaltung.

## Praxisbezug / Beispiele

- **UMAR, NEST Dübendorf**: Demonstrator für Urban Mining, reversible Konstruktionen, trennbare Materialien und Materialdokumentation. Das Projekt zeigt DfD als architektonisches und technisches Prinzip, nicht nur als Rückbauoption.
- **K.118 Kopfbau Halle 118**: Das Projekt nutzt wiederverwendete Bauteile und verdeutlicht zugleich, warum neue Ergänzungen so gefügt werden sollten, dass zukünftige Wiederverwendung möglich bleibt.
- **Stahlbau mit Schraub-/Bolzenverbindungen**: Sehr gute DfD-Eignung, wenn Profile nicht verschweißt oder unzugänglich verkleidet werden und Materialkennwerte dokumentiert sind.
- **Holzbau mit mechanischen Verbindungsmitteln**: Gute Voraussetzungen für Demontage; problematisch werden vollflächige Verklebungen, hybride Verbünde und nicht zugängliche Knoten.
- **Systemtrennwände, Doppelböden, abgehängte Decken**: Im Ausbau häufig DfD-tauglich, sofern Raster, Befestigungen und Herstellerdaten erhalten bleiben.
- **Fassaden mit lösbarer Unterkonstruktion**: Bekleidungen, Dämmung und Tragstruktur sollten getrennt demontierbar sein. Wärmedämmverbundsysteme gelten häufig als negative Gegenbeispiele.
- **Serielle Sanierungsmodule**: Potenzial, wenn Module nicht nur schnell montiert, sondern auch später lösbar, reparierbar und dokumentiert sind.

Praxisprinzipien:

- DfD-Ziele in Leistungsphasen und Ausschreibung festlegen.
- Demontagekonzept parallel zum Montagekonzept erstellen.
- Verbindungskatalog projektbezogen führen.
- Bauteile mit QR-/RFID-/digitalem Pass verknüpfen, sofern Datenpflege gesichert ist.
- Klebstoffe, Schäume, Nassverbund und verdeckte irreversible Befestigungen kritisch prüfen.
- Trennung der Gebäudeschichten im Detail kontrollieren.
- Rückbauunternehmen und Facility Management früh einbinden.
- Nach Fertigstellung As-built-Daten und Demontagehinweise übergeben.

## Herausforderungen / offene Fragen

- **Zeitversatz**: Nutzen entsteht oft erst Jahrzehnte später, Kosten entstehen heute.
- **Marktunsicherheit**: Niemand weiß sicher, welche Bauteile künftig nachgefragt werden.
- **Regulatorische Unsicherheit**: Zukünftige Normen können heutige wiederverwendbare Bauteile entwerten.
- **Datenhaltung**: Materialpässe müssen langlebig, aktualisierbar und eigentümerübergreifend verfügbar sein.
- **Bewertungssysteme**: Es fehlen einheitliche, allgemein verpflichtende DfD-Indikatoren.
- **Haftung und Eigentum**: Wer besitzt den zukünftigen Bauteilwert, und wer haftet bei Rückbau?
- **Brandschutz und Bauphysik**: Viele leistungsfähige Systeme beruhen auf Schichtverbund; DfD verlangt alternative Details.
- **Baukultur**: Sichtbare Fugen, Schrauben und modulare Logiken verändern Ästhetik.
- **Kostenrechnung**: Restwert und vermiedene Rückbaukosten werden in Investitionsrechnungen selten berücksichtigt.
- **Umgang mit Bestand**: Bei Umbauten muss DfD sowohl für neue Ergänzungen als auch für die Schonung vorhandener Bauteile gelten.
- **Zertifizierung**: DGNB, Level(s) und andere Systeme adressieren Zirkularität zunehmend, doch Projektpraxis und Nachweistiefe variieren.

## Quellen

- ISO 20887:2020: Sustainability in buildings and civil engineering works — Design for disassembly and adaptability — Principles, requirements and guidance. https://www.iso.org/standard/69370.html
- European Commission: Circular Economy Principles for Buildings Design, 2020. https://single-market-economy.ec.europa.eu/
- European Commission: Level(s) – European framework for sustainable buildings. https://green-forum.ec.europa.eu/green-business/levels_en
- European Commission: Construction Products Regulation (CPR). https://single-market-economy.ec.europa.eu/sectors/construction/construction-products-regulation-cpr_en
- Regulation (EU) 2024/3110: Construction Products Regulation. Official Journal of the European Union, 18.12.2024.
- Regulation (EU) 2024/1781: Ecodesign for Sustainable Products Regulation. Official Journal of the European Union, 2024.
- Crowther, P. (2005): Design for Disassembly – Themes and Principles. RAIA/Queensland University of Technology.
- Guy, B.; Ciarimboli, N. (2005): Design for Disassembly in the Built Environment: A Guide to Closed-Loop Design and Building. Hamer Center / Pennsylvania State University.
- Durmisevic, E. (2006): Transformable Building Structures. Design for disassembly as a way to introduce sustainable engineering to building design & construction. Dissertation, TU Delft.
- Akinade, O. et al. (2017): Design for Deconstruction using a circular economy approach. Fachliteratur zu DfD-Bewertung im Bauwesen.
- Empa / NEST: Urban Mining and Recycling Unit. https://nest-umar.net/
- Werner Sobek: NEST Unit UMAR. https://www.wernersobek.com/projects/nest-unit-umar/
- DGNB: Zirkuläres Bauen, Rückbau- und Recyclingfreundlichkeit, Gebäuderessourcenpass. https://www.dgnb.de/
- Madaster: Material passports and circularity documentation. https://madaster.com/
- Umweltbundesamt / BBSR: Veröffentlichungen zu Kreislaufwirtschaft, Urban Mining und Umbaukultur. https://www.umweltbundesamt.de/ ; https://www.bbsr.bund.de/

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; zirkuläres Bauen; Entwerfen mit Bestand; Kreislaufwirtschaft; Materialpass; Open Building; Lebenszyklusplanung.
- **Verwandte Dateien:** `tragwerkssystem/Reversible_Fuegung.md`; `tragwerkssystem/Skelettbauweise.md`; `tragwerkssystem/Stahl_Skelettbau.md`; `tragwerkssystem/Holz_Skelettbau.md`; `tragwerkssystem/Betonfertigteil_System.md`; `bauteil/Alle_Bauteile.md`; `verbindung/Verbindungsmittel.md`; `pruefung/Bauteilpass.md`; `reuse_strategie/Design_for_Reuse.md`; `reuse_strategie/Bauteilernte.md`; `projekt/BAMB.md`; `projekt/FCRBE.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ISO 20887:2020; BAMB; FCRBE; EU Level(s); DGNB-Zirkularitätsindex; Gebäuderessourcenpass; Materialpass; BIM; Bauteilkataster; Rückbaukonzept; reversible Verbindungstechnik; Schichtenmodell nach Lebensdauer; Circular Economy Action Plan; Construction Products Regulation (EU) 2024/3110.

## Kurzdefinition

Design for Disassembly (DfD) bezeichnet die Planung von Gebäuden, Tragwerken, Bauteilen und Verbindungen so, dass sie am Ende einer Nutzungsphase zerstörungsarm demontiert, geprüft, repariert, angepasst und wiederverwendet werden können. Design for Disassembly ist kein einzelnes Detail, sondern eine Systemlogik aus reversiblen Fügungen, zugänglichen Verbindungspunkten, getrennten Materialschichten, standardisierten Bauteilen, dokumentierten Eigenschaften und vorausschauender Rückbauplanung.

## Relevanz für Wiederverwendung im Bauwesen

- **Voraussetzung für zukünftige Bauteilwiederverwendung:** Ohne DfD werden viele Bauteile beim Rückbau beschädigt, vermischt oder rechtlich/technisch nicht mehr nachweisbar.
- **Wertsteigerung der Materialbank Gebäude:** Gebäude werden nicht nur als Nutzobjekte, sondern als temporäre Lager hochwertiger Bauteile verstanden.
- **Adaptionsfähigkeit während der Nutzung:** DfD erleichtert Umbau, Reparatur, Austausch und Umnutzung. Wiederverwendung beginnt damit oft schon im Gebäude selbst, nicht erst nach Abriss.
- **Reduktion von Downcycling:** Sortenreine Trennung und zerstörungsarme Demontage erhöhen die Chance auf gleichwertige Wiederverwendung statt Recycling oder Entsorgung.
- **Planungsdisziplin über Gewerke hinweg:** Tragwerk, Ausbau, Fassade, Haustechnik, Brandschutz und Bauphysik müssen gemeinsam rückbaubar gedacht werden.

## Fachinhalt

### Grundprinzipien

- **Reversibilität:** Verbindungen können gelöst werden, ohne die Hauptbauteile wesentlich zu zerstören.
- **Zugänglichkeit:** Verbindungsmittel, Knoten und Installationen bleiben auffindbar und erreichbar; Wartungs- und Rückbauöffnungen sind eingeplant.
- **Trennbarkeit:** Tragwerk, Fassade, Ausbau, Haustechnik, Dämmung und Abdichtung werden nach Material, Funktion und Lebensdauer getrennt.
- **Standardisierung und Modularität:** Wiederkehrende Raster, Querschnitte, Verbindungsmittel und Bauteilgrößen erhöhen die Wahrscheinlichkeit einer zweiten Nutzung.
- **Einfachheit:** Wenige, robuste Verbindungstypen und klare Lastpfade sind rückbau- und prüffreundlicher als hochgradig optimierte Sonderlösungen.
- **Dokumentation:** Materialpass, Bauteilnummern, Prüfzeugnisse, Einbauorte, Verbindungsmittel, Wartungshistorie und Rückbauanleitungen bleiben digital und analog verfügbar.
- **Sicherer Rückbau:** Die Montagefolge ist grundsätzlich umkehrbar; temporäre Aussteifungen, Hebepunkte, Lastfälle und Demontagezustände sind mitgeplant.

### Entwurfsregeln für Tragwerkssysteme

- Primärtragwerk langlebig, nutzungsneutral und gut zugänglich planen.
- Sekundärstruktur, Fassade und Ausbau austauschbar und mit kürzerer Lebensdauer entkoppeln.
- Verbundwirkungen nur dort einsetzen, wo sie rückbaubar oder als bewusster Zielkonflikt dokumentiert sind.
- Raster und Spannweiten so wählen, dass Bauteile in unterschiedlichen Gebäuden wieder nutzbar bleiben.
- Übermäßige Spezialisierung vermeiden: Sonderformen, extreme Zuschnitte und objektspezifische Knoten reduzieren ReUse-Marktchancen.
- Verbindungsmittel möglichst sichtbar, lösbar, korrosionsgeschützt und normnah wählen.
- Schichten mit ähnlicher Lebensdauer koppeln; Schichten mit unterschiedlicher Lebensdauer entkoppeln.
- Bauteile mit ausreichenden Hebe-, Transport- und Lageroptionen planen.

### DfD auf Systemebene

- **Gebäudeebene:** flexible Grundrisse, ausreichend Geschosshöhe, Tragwerk/Fassade/Innenausbau getrennt, Nutzungsänderungen eingeplant.
- **Systemebene:** austauschbare Deckenfelder, Fassadenelemente, Module, Stützen-/Trägerachsen, Technikzonen.
- **Bauteilebene:** identifizierbare Elemente mit bekannten Material- und Leistungsdaten.
- **Verbindungsebene:** lösbare Knoten mit klarer Lastabtragung und geringem Beschädigungsrisiko.
- **Informationsebene:** Bauteilpass, Wartungsplan, Rückbauanleitung, digitale Produktdaten, Fotodokumentation, As-built-Modell.

### Bewertungskriterien

- Lösbarkeit der Verbindung ohne Zerstörung des Hauptbauteils.
- Anzahl und Zugänglichkeit der Verbindungsmittel.
- Sortenreinheit und Schadstofffreiheit.
- Standardisierungsgrad und Wiederverwendungsmarkt.
- Robustheit gegenüber Umbauten, Reparaturen und Nutzungsänderungen.
- Verfügbarkeit von Leistungsnachweisen und Prüfverfahren.
- Ökobilanz: Zusatzmaterial für Reversibilität darf den zukünftigen Nutzen nicht unverhältnismäßig übersteigen.

## Praxisbezug / Beispiele

- **BAMB:** Das Projekt hat Materialpässe und reversible Gebäudedesign-Ansätze als Instrumente für Gebäude als Materialbanken entwickelt.
- **FCRBE:** Das ReUse Toolkit zeigt, dass Wiederverwendung nicht nur aus Entwurfsdetails besteht, sondern aus Beschaffung, Spezifikation, Prüfung, Lagerung, Rückbau und rechtlicher Zuordnung.
- **Stahlhallen:** Geschraubte Stahlrahmen mit standardisierten Profilen und klarer Dokumentation können als ganze Struktur, als Teilrahmen oder als Einzelprofile wiederverwendet werden.
- **Holzmodulbau:** Module mit lösbaren Transport- und Anschlussknoten, getrennten Installationen und dokumentierten Bauteilen können an anderer Stelle erneut eingesetzt werden.
- **Fassaden- und Ausbaukomponenten:** Obwohl diese Datei Tragwerkssysteme fokussiert, zeigt der Ausbau oft die DfD-Probleme besonders deutlich: verklebte Schichten, Mischmaterialien und verdeckte Befestigungen verhindern hochwertige Wiederverwendung.

## Herausforderungen / offene Fragen

- **Zielkonflikte mit Bauphysik:** Luftdichtheit, Schallschutz, Feuchteschutz und Brandschutz werden häufig über Schichten, Verklebungen, Verguss und Bekleidungen hergestellt, die Demontierbarkeit erschweren.
- **Kosten und Verantwortlichkeiten:** DfD-Nutzen entsteht oft in der Zukunft, Kosten aber heute. Ohne Geschäftsmodelle, Restwertlogik oder Rücknahmeverträge bleibt DfD schwer durchsetzbar.
- **Normen und Zulassung:** Für neue Bauprodukte sind Nachweiswege etabliert; für wiederverwendete Bauteile sind Re-Qualifizierung, Leistungserklärung und Haftung häufig projektspezifisch.
- **Dokumentationsverlust:** Materialpässe nützen nur, wenn sie über Jahrzehnte gepflegt, zugänglich und rechtlich verwendbar bleiben.
- **Überdimensionierung:** Nutzungsneutrale und wiederverwendbare Bauteile können mehr Material benötigen. Dieser Mehraufwand muss über längere Nutzung, Anpassbarkeit und ReUse plausibel kompensiert werden.
- **Marktunsicherheit:** Wiederverwendung setzt Nachfrage, Lager, Standardmaße, Prüfstellen, Gewährleistung und Beschaffungsprozesse voraus. DfD allein schafft diesen Markt nicht, reduziert aber zukünftige Barrieren.

## Quellen

- ISO 20887:2020: *Sustainability in buildings and civil engineering works — Design for disassembly and adaptability — Principles, requirements and guidance*. https://www.iso.org/standard/69370.html
- ISO: *Tearing down the carbon footprint of buildings with new International Standard*, 2020. https://www.iso.org/news/ref2480.html
- BAMB: *Buildings as Material Banks*. https://www.bamb2020.eu/
- BAMB: *Materials Passports*. https://www.bamb2020.eu/topics/materials-passports/
- European Commission: *Level(s) — European framework for sustainable buildings*. https://green-forum.ec.europa.eu/green-business/levels_en
- FCRBE / Rotor: *Reuse Toolkit: material sheets*. https://rotordb.org/en/projects/reuse-toolkit-material-sheets
- European Commission: *EU Construction & Demolition Waste Management Protocol including guidelines for pre-demolition and pre-renovation audits of construction works*, 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- DGNB: *Circular building in the DGNB System*. https://www.dgnb.de/en/sustainable-building/circular-building/toolbox/circular-building-in-the-dgnb-system
- Regulation (EU) 2024/3110: *Construction Products Regulation*. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
