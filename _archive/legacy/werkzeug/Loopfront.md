---
type: Werkzeug
dokument: ["[[dokument/Bestandsaufnahme]]"]
methode: ["[[methode/Urban_Mining]]"]
verwandt: ["[[werkzeug/BIM]]", "[[werkzeug/IFC_Viewer]]", "[[werkzeug/Materialdatenbank]]", "[[werkzeug/QR_RFID_Materialtracking]]", "[[werkzeug/Reusefully_LINK]]", "[[werkzeug/Rheaply]]"]
---

# Loopfront

## Verknüpfungen

- **Übergeordnete Themen:** digitale Bestandsaufnahme, Urban Mining, Materialpass, Bauteilkatalog, Reuse-Logistik, zirkuläre Beschaffung, Rückbauplanung, Portfolio- und Projektinventare.
- **Verwandte Dateien:** `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Materialdatenbank.md`, `datenmodell/Materialpass.md`, `datenmodell/Bauteilkatalog.md`, `dokument/Rueckbaukonzept.md`, `dokument/Bestandsaufnahme.md`, `methode/Pre_Demolition_Audit.md`, `methode/Urban_Mining.md`, `logistik/Zwischenlager.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Bauherrschaften, Bestandshalter, Generalunternehmer, Rückbauunternehmen, Architekturbüros, Reuse-Koordinatoren, öffentliche Auftraggeber, Hersteller; Pre-Demolition Audit, Reuse-Audit, Materialpass, QR-/RFID-Kennzeichnung, Bauteilbörse, CO₂- und Abfallmonitoring.

## Kurzdefinition

Loopfront ist eine digitale Plattform für die Erfassung, Verwaltung und Wiederverwendung von Materialien, Produkten und Bauteilen in Bau- und Immobilienprojekten. Der Kernnutzen liegt nicht in allgemeinem BIM-Modellieren, sondern in der **operativen Reuse-Inventarisierung**: Bauteile werden als wiederverwendbare Objekte mit Standort, Zustand, Mengen, Fotos, Abmessungen, technischen Angaben, Verfügbarkeit, potenzieller Wiederverwendung und Wirkungskennzahlen dokumentiert. Loopfront wird vor allem als Werkzeug für Urban-Mining-Prozesse, interne Materialbanken und projektübergreifende Wiederverwendungslogistik genutzt.

## Relevanz für Wiederverwendung im Bauwesen

Loopfront hat eine spezifische Reuse-Nutzung, weil es die Lücke zwischen baulichem Bestand und realer Wiederverwendung adressiert: Viele wiederverwendbare Bauteile scheitern nicht an der Idee, sondern an fehlender Datentiefe, fehlender Sichtbarkeit, unklarem Zeitfenster, ungeklärter Verantwortlichkeit und fehlendem Matching mit Nachfrage. Die Plattform dient dazu, Bauteile früh genug sichtbar zu machen, sie mit Mindestinformationen zu versehen und ihre Bewegung vom Bestandsobjekt bis zum neuen Einsatz oder Lager nachzuverfolgen.

Für Wiederverwendung besonders relevant sind:

- **Bestands- und Rückbauinventare:** Erfassung von Bauteilen vor Sanierung, Umbau, Rückbau oder Abriss.
- **Interne Wiederverwendung:** Unternehmen, Kommunen oder Immobilienportfolios können eigene Materialbestände katalogisieren, bevor externe Marktplätze genutzt werden.
- **Projektübergreifendes Matching:** Bauteile aus einem Projekt können Bedarfen in anderen Projekten zugeordnet werden.
- **Wirkungsnachweis:** Einsparungen bei Abfall, Primärmaterial und CO₂ können projekt- oder portfolioseitig dokumentiert werden, sofern die zugrunde gelegten Faktoren transparent sind.
- **Koordination von Ausbau, Lagerung und Wiedereinbau:** Inventarlisten können als gemeinsame Arbeitsgrundlage für Rückbau, Planung, Einkauf und Logistik dienen.

## Fachinhalt

Loopfront ist als Reuse-orientiertes Bestands- und Materialmanagementsystem einzuordnen. Es arbeitet typischerweise objekt- und listenbasiert, ergänzt durch Bilder, Metadaten, Statusfelder und Standortinformationen. Im Unterschied zu einem klassischen BIM-Modell, das primär Geometrie, Planung und Koordination unterstützt, ist Loopfront stärker auf **Verfügbarkeit, Kreislauffähigkeit und operative Wiederverwendung** ausgerichtet.

### Typische Datentypen

Ein wiederverwendbares Objekt kann unter anderem folgende Daten enthalten:

- Bezeichnung und Kategorie des Bauteils oder Materials.
- Projekt, Gebäude, Geschoss, Raum, Zone oder Lagerort.
- Menge, Einheit, Abmessungen, Gewicht, Materialzusammensetzung, Hersteller oder Produktname, soweit bekannt.
- Fotos, Dokumente, Prüfberichte, Datenblätter, EPDs oder andere Nachweise.
- Zustand, Schadstoffverdacht, Ausbauaufwand, Demontierbarkeit, Reinigungs- oder Reparaturbedarf.
- Verfügbarkeitszeitpunkt, Eigentümer, Ansprechpartner, Reservierungsstatus und Zielverwendung.
- Wiederverwendungsszenario: direkte Wiederverwendung, Reparatur, Refurbishment, Upcycling, Recycling oder Entsorgung.
- Wirkungsindikatoren wie vermiedene Abfallmenge, potenziell vermiedene Emissionen oder wirtschaftlicher Restwert.

### Funktionsweise

Die Plattform unterstützt typischerweise einen Workflow aus:

1. **Inventarisierung:** Vor-Ort-Erfassung durch Tablet/Smartphone, Import vorhandener Listen oder projektbezogene Erhebung.
2. **Klassifikation:** Zuordnung von Kategorien, Materialien und projektinternen Codes; wichtig für spätere Suche.
3. **Qualifizierung:** Bewertung von Zustand, Wiederverwendbarkeit, Risiken und Demontageaufwand.
4. **Publikation / Sichtbarkeit:** Freigabe für interne oder externe Nutzergruppen, je nach Datenschutz und Projektstrategie.
5. **Matching und Reservierung:** Zuordnung von Angeboten zu konkreten Bedarfen, Einkaufslisten oder neuen Projekten.
6. **Logistik und Nachverfolgung:** Statusänderungen von „im Bestand“ über „demontiert“, „gelagert“, „reserviert“ bis „wiederverwendet“.
7. **Reporting:** Aggregierte Kennzahlen für CO₂, Abfall, Materialmengen, Wiederverwendungsquote oder wirtschaftlichen Nutzen.

### Schnittstellen

Loopfront ist dort besonders leistungsfähig, wo es mit anderen Systemen verbunden wird:

- **BIM / IFC:** mögliche Ergänzung zu geometrischen und bauteilbezogenen Daten; nicht jeder Reuse-Workflow benötigt ein vollständiges BIM-Modell.
- **Excel/CSV:** praxisnah für Import und Export von Auditlisten.
- **Materialpässe:** Loopfront kann als operativer Speicher für Materialpassinformationen dienen, ersetzt aber nicht automatisch eine normierte Materialpassmethodik.
- **ERP/Einkauf:** relevant, wenn Reuse-Bauteile in Beschaffungsprozesse eingebunden werden sollen.
- **Lager- und Logistiksysteme:** besonders wichtig bei Zwischenlagerung, Transport und Bestandsführung.
- **QR-/RFID-Kennzeichnung:** physische Identifikation der Bauteile zur Verknüpfung mit digitalen Datensätzen.

### Einordnung gegenüber ähnlichen Werkzeugen

- **BIM** ist primär ein Planungs- und Koordinationsmodell.
- **IFC-Viewer** dienen vor allem der Anzeige und Prüfung offener Modelle.
- **Materialdatenbanken** speichern allgemeine Material- und Produktinformationen.
- **Loopfront** fokussiert auf konkrete, verfügbare Bauteile und deren Wiederverwendungsprozess.
- **Marktplätze** wie RotorDC, SalvoWEB oder CMEx fokussieren stärker auf Angebot/Nachfrage; Loopfront kann davor als Inventarisierungs- und Managementschicht liegen.

## Praxisbezug / Beispiele

Typische Einsatzszenarien sind:

- Eine Kommune erfasst beim Umbau öffentlicher Gebäude Türen, Leuchten, Bodenbeläge, Sanitärkeramik, Stahlbauteile und Möblierung, um sie in anderen kommunalen Projekten einzusetzen.
- Ein Projektentwickler lässt vor Rückbau eines Bürogebäudes ein Reuse-Audit durchführen und nutzt die Plattform, um Materialien intern freizugeben, bevor sie extern angeboten werden.
- Ein Generalunternehmer dokumentiert überschüssige Neumaterialien auf Baustellen und stellt sie anderen Projekten des Unternehmens zur Verfügung.
- Ein Rückbauunternehmen nutzt die Daten zur Planung selektiver Demontage und zur Kommunikation mit potenziellen Abnehmern.

Besonders geeignet sind Bauteile mit klarer Identifizierbarkeit und hoher Wiederverwendungschance: Türen, Verglasungen, Doppelbodenplatten, Leuchten, Sanitärgegenstände, Trennwände, Möbel, technische Einbauten, Stahlprofile, Holzbauteile, Fassadenelemente und Oberflächenmaterialien.

## Herausforderungen / offene Fragen

- **Datenqualität:** Ohne verlässliche Maße, Fotos, Zustandsangaben und Verfügbarkeitsdaten bleibt ein Inventar nur eine Wunschliste.
- **Haftung und Nachweise:** Für tragende, brandschutzrelevante oder sicherheitsrelevante Bauteile müssen Prüfungen und Verantwortlichkeiten geklärt werden.
- **Zeitliche Passung:** Reuse funktioniert nur, wenn Rückbau, Lagerung und Neubau zeitlich koordiniert werden.
- **Marktdichte:** Der Nutzen steigt mit der Zahl aktiver Projekte und Nutzer; kleine Insellösungen können zu wenig Nachfrage erzeugen.
- **Methodische Transparenz:** CO₂- und Abfallkennzahlen müssen nachvollziehbar berechnet werden; sonst sind sie als Entscheidungsgrundlage unsicher.
- **Interoperabilität:** Import/Export über offene Formate ist entscheidend, damit Daten nicht in einer Plattform eingeschlossen bleiben.
- **Status regional unterschiedlich:** Funktionsumfang, Integrationen und Marktverfügbarkeit können je nach Land, Lizenzmodell und Projektpartner variieren und sollten vor Projektbeginn geprüft werden.

## Quellen

- Loopfront, offizielle Website: https://www.loopfront.com/
- Loopfront Help Center / Produktdokumentation: https://help.loopfront.com/
- UKGBC, Circular Economy / reuse resources: https://ukgbc.org/
- Arup / Ellen MacArthur Foundation, Circular Buildings Toolkit: https://ce-toolkit.dhub.arup.com/
- BAMB – Buildings as Material Banks, Material Passports: https://www.bamb2020.eu/topics/materials-passports/
- Byers, B. S. et al. (2024): *From research to practice: A review on technologies for scaling material reuse in the built environment*, Automation in Construction / related circular construction literature.
- Hinweis: Produktfunktionen und Integrationen können sich ändern; vor Anwendung aktuellen Anbieterstand prüfen. Abrufstand: 2026-04-27.
