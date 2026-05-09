---
entity: "quelle"
id: "werkzeug_BIM_md"
title: "werkzeug_BIM_md"
build_status: "promoted_phase42"
source_filename: "BIM.md"
legacy_type: "Werkzeug"
---

# werkzeug_BIM_md

## Verknüpfungen

- **Übergeordnete Themen:** digitale Werkzeuge; Informationsmanagement; Gebäuderessourcenpass; Materialpass; zirkuläre Planung; Rückbauplanung; Bestandsaufnahme.
- **Verwandte Dateien:** `werkzeug/IFC_Viewer.md`; `werkzeug/Madaster_Plattform.md`; `werkzeug/Concular_Plattform.md`; `werkzeug/Materialdatenbank.md`; `werkzeug/Rhino.md`; `dokument/Gebäuderessourcenpass.md`; `dokument/Materialpass.md`; `datenmodell/IFC.md`; `datenmodell/IDS.md`; `datenmodell/BCF.md`; `methode/Pre_Demolition_Audit.md`; `methode/Bauteilkatalogisierung.md`; `logistik/Rueckbauplanung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** buildingSMART; ISO 19650; ISO 16739-1 / IFC; BCF; IDS; bSDD; DIN SPEC 91484; DGNB Gebäuderessourcenpass; Madaster; Concular; ÖKOBAUDAT; EPD-Programme; Planungsbüros, Rückbauunternehmen, Bestandshalter, Prüfstellen.

## Kurzdefinition

BIM, Building Information Modeling bzw. Building Information Management, bezeichnet im Bauwesen zugleich eine modellbasierte Arbeitsmethode, ein digitales Informationsmodell und einen koordinierten Informationsmanagementprozess. Für Wiederverwendung ist nicht die 3D-Geometrie allein entscheidend, sondern die verlässliche, austauschbare und prüfbare Kombination aus Bauteilidentität, Lage, Menge, Material, Zustand, Leistungsdaten, Demontierbarkeit, Herkunft, Eigentum, Nachweisen und künftigen Verwendungsoptionen.

BIM ist deshalb von verwandten Ebenen zu trennen:

- **BIM-Methode:** Rollen, Informationsanforderungen, Austauschzeitpunkte, Prüfprozesse, Common Data Environment, Verantwortlichkeiten.
- **BIM-Modell:** geometrisch-semantisches Gebäudemodell mit Objekten, Mengen, Attributen, Klassifikationen und Beziehungen.
- **IFC:** offenes Austauschformat für BIM-Daten, nicht identisch mit BIM.
- **IFC-Viewer:** Werkzeug zur Anzeige, Prüfung und Kommentierung von IFC-Modellen, nicht primär Autorensystem.
- **Materialpass / Gebäuderessourcenpass:** Auswertung und Dokumentationsformat, das aus BIM, Audits, Datenbanken und Nachweisen gespeist werden kann.
- **Materialplattform / Marktplatz:** Daten- und Marktinfrastruktur für Angebot, Nachfrage, Reservierung, Bewertung und Vermittlung wiederverwendbarer Bauteile.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung scheitert häufig nicht am Fehlen von Material, sondern an fehlender Information: Was ist wo verbaut? In welcher Menge? In welchem Zustand? Mit welchen Nachweisen? Wann wird es verfügbar? Wie lässt es sich demontieren, lagern, transportieren, prüfen und erneut einsetzen? BIM kann diese Informationslücken verringern, wenn das Modell früh und zielgerichtet für zirkuläre Fragen aufgebaut wird.

BIM unterstützt Wiederverwendung in vier Richtungen:

1. **Bestand als Materiallager erfassen:** Bauteile werden räumlich, mengenmäßig und semantisch dokumentiert. Das ist Grundlage für Urban Mining, Pre-Demolition Audits, Rückbauplanung und Ausschreibung.
2. **Wiederverwendbare Bauteile planen:** Re-Use-Elemente können als konkrete Objekte mit variierenden Abmessungen, Zuständen und Restriktionen in die Planung integriert werden.
3. **Kreislauffähigkeit neuer Gebäude sichern:** Lösbare Verbindungen, Schichtenlogik, Zugänglichkeit, Bauteilpässe und Demontageinformationen werden von Anfang an dokumentiert.
4. **Daten an Plattformen und Nachweise übergeben:** BIM- bzw. IFC-Daten können Materialpässe, Gebäuderessourcenpässe, LCA, Kostenmodelle, Logistiklisten, Ausschreibungen und digitale Gebäudelogbücher speisen.

Der Nutzen entsteht erst, wenn Informationsanforderungen explizit festgelegt werden. Ein gewöhnliches Koordinationsmodell enthält oft Geometrie und Mengen, aber keine ausreichenden Angaben zu Zustand, Schadstoffen, Demontierbarkeit, Eigentumsrechten, Wiederverwendungsfreigaben, Prüfzeugnissen, Toleranzen, Lagerbedingungen oder Gewährleistungsfragen.

## Fachinhalt

### Informationsanforderungen für Wiederverwendung

Für ein zirkuläres BIM-Modell sollten Anforderungen projektspezifisch in Auftraggeber-Informationsanforderungen, Modellierungsrichtlinien oder IDS-Prüfregeln gefasst werden. Zentrale Datenfelder sind:

- **Identifikation:** Bauteil-ID, GUID, Inventarnummer, Raum-/Geschossbezug, Gebäudeteil, Foto-Referenzen, QR-/NFC-Verknüpfung.
- **Geometrie und Menge:** Länge, Breite, Höhe, Fläche, Volumen, Masse, Stückzahl, Achsmaß, Einbaulage, Toleranzen.
- **Materialität:** Hauptmaterial, Schichtenaufbau, Verbundmaterialien, Beschichtungen, Verbindungsmittel, Materialklasse, EPD-/ÖKOBAUDAT-Bezug, Schadstoffhinweise.
- **Produkt- und Herstellungsdaten:** Hersteller, Typ, Baujahr, Normbezug, Leistungserklärung, CE-Kennzeichnung soweit verfügbar, Seriennummer, Wartungsdaten.
- **Zustand:** sichtbare Schäden, Korrosion, Verformung, Feuchte, Verschleiß, Restlebensdauer, Prüfergebnis, Bewertungsdatum, Unsicherheitsgrad.
- **Demontierbarkeit:** Verbindungstyp, Zugänglichkeit, zerstörungsarme Demontage möglich, benötigte Werkzeuge, Reihenfolge, Risiken, Zeitaufwand, Verlustquote.
- **Wiederverwendungspotenzial:** direkte Wiederverwendung, Aufbereitung, Reparatur, Remanufacturing, Recycling, Downcycling, Entsorgung.
- **Recht und Nachweis:** Eigentum, Freigabe, Prüfzeugnisse, Zulassungen, Garantien, Haftung, Brandschutz-, Schallschutz-, Tragwerks- und Schadstoffnachweise.
- **Logistik:** Ausbauzeitpunkt, Lagerort, Verpackung, Transportmaß, Gewicht, Stapelbarkeit, Witterungsschutz, Reservierung, Nachfragebezug.
- **Zirkularitätskennwerte:** Re-Use-Anteil, Recyclinganteil, CO₂-Äquivalente, Primärrohstoffersatz, Rückbaupotenzial, Restwert.

### Datenebenen

Für Wiederverwendung sind mehrere Datenebenen zu unterscheiden:

- **Objektebene:** einzelnes Bauteil, z. B. Türblatt, Stahlträger, Fassadenelement, Doppelbodenplatte.
- **Bauteilgruppe:** Fenstercharge, Leuchtenserie, Sanitärkeramik, Ziegelcharge, Natursteinbelag.
- **Gebäudeebene:** Materialinventar, Ressourcenpass, Rückbaukonzept, LCA.
- **Portfolioebene:** mehrere Gebäude, Zeithorizonte für Materialverfügbarkeit, kommunale oder unternehmensweite Urban-Mining-Kataster.
- **Marktebene:** Plattformdaten zu Angebot, Nachfrage, Preisen, Qualitäten, Reservierungen und Vermittlungen.

Diese Ebenen sind nicht identisch. Ein BIM-Modell kann sehr detailliert auf Gebäudeebene sein, aber für Marktnutzung unbrauchbar, wenn Bauteile nicht als handelbare Chargen zusammengefasst, geprüft und mit Verfügbarkeitszeitpunkten versehen werden.

### Schnittstellen

Relevante Schnittstellen sind:

- **IFC:** offenes Format für Geometrie, Bauteile, Beziehungen, Mengen, Klassifikationen und Property Sets. Für Wiederverwendung wichtig, aber oft nur so gut wie Exportdisziplin und Modellierungsregeln.
- **BCF:** Austausch von Modellkommentaren, Prüfhinweisen und Aufgaben zwischen Beteiligten.
- **IDS:** maschinenlesbare Informationsanforderungen, mit denen geprüft werden kann, ob z. B. Material, Masse, Klassifikation oder Demontierbarkeit in einem Modell vorhanden sind.
- **bSDD / Klassifikationssysteme:** strukturierte Begriffe, Klassifikationen und Eigenschaften, um Bauteile über Software- und Ländergrenzen hinweg vergleichbarer zu machen.
- **CSV / Excel:** weiterhin wichtig für Audits, Materiallisten, Plattformimporte und manuelle Qualitätssicherung; oft robuster als komplexe Modellübergaben.
- **APIs:** Übergabe an Materialpassplattformen, LCA-Datenbanken, Marktplätze, CDEs und Portfolio-Tools.

### BIM für Bestand

Bestands-BIM kann aus Vermessung, Laserscans, Photogrammetrie, Bestandsplänen, Bauteilöffnungen, Sondagen, Schadstoffgutachten und manuellen Erfassungen entstehen. Für Wiederverwendung ist ein geometrisch perfektes Scan-to-BIM-Modell weniger wertvoll als ein ausreichend genaues, prüfbares Inventar mit Unsicherheitsangaben. Besonders kritisch sind verdeckte Schichten, nicht sichtbare Verbindungen, Schadstoffe, Herstellungsdaten und reale Zustände.

Sinnvoll ist eine abgestufte Modellierung:

- **Screening:** grobe Mengen, Baualter, Gebäudetyp, potenziell relevante Materialgruppen.
- **Audit-Modell:** Bauteile, Chargen, Mengen, Zustands- und Demontageinformationen.
- **Planungsmodell:** Integration verfügbarer Re-Use-Bauteile in Entwurf, Ausschreibung und Koordination.
- **As-built-Ressourcenmodell:** Dokumentation der eingebauten neuen und wiederverwendeten Bauteile für künftige Zyklen.

### BIM und Materialpass

BIM kann Materialpässe vorbereiten, ersetzt sie aber nicht vollständig. Ein Materialpass benötigt häufig zusätzliche Informationen aus Produktdatenbanken, EPDs, Prüfungen, Wartungsunterlagen, Schadstoffanalysen, Kosten-/Restwertdaten und Rückbauwissen. Plattformen wie Madaster nutzen IFC oder Excel als Eingangsdaten, werten sie aber mit Material-, Umwelt-, Zirkularitäts- und Wertinformationen an. Der DGNB-Gebäuderessourcenpass verfolgt ebenfalls eine strukturierte Dokumentation von Ressourcen, Rückbau- und Kreislaufaspekten.

### BIM und Ausschreibung

BIM kann Wiederverwendung in Ausschreibungen konkretisieren:

- Bauteile als verfügbare Re-Use-Positionen beschreiben.
- Mindestdaten für angebotene gebrauchte Bauteile definieren.
- Rückbauleistungen mit Demontage- und Schutzanforderungen koppeln.
- Bieter zur Datenergänzung, Prüfung und Dokumentation verpflichten.
- Mengen- und Qualitätsunsicherheiten transparent machen.
- Alternativpositionen und Freigabeprozesse für schwankende Verfügbarkeit vorsehen.

### Grenzen und Risiken

- **Datenqualität:** falsche oder unvollständige Materialangaben erzeugen Scheingenauigkeit.
- **Interoperabilität:** IFC-Exporte verlieren je nach Autorensoftware, Version, Mapping und Property-Sets Informationen.
- **Aufwand:** zirkuläre Informationsanforderungen erhöhen den Modellierungs- und Prüfaufwand.
- **Unsicherheit:** Zustand, Schadstoffe und Verbindungen sind oft erst nach Öffnung oder Ausbau sicher bestimmbar.
- **Marktdynamik:** BIM kennt nicht automatisch Nachfrage, Preis, Lagerkapazität oder Verfügbarkeit.
- **Recht:** Modellinformationen ersetzen keine bauaufsichtlichen Nachweise, Prüfungen oder Haftungsregelungen.
- **Datenschutz und Eigentum:** Gebäudedaten können sicherheits-, eigentums- oder wettbewerbsrelevant sein.

## Praxisbezug / Beispiele

- **Pre-Demolition Audit:** BIM kann als digitales Inventar dienen, in dem potenziell wiederverwendbare Bauteile nach DIN-SPEC-Logik erfasst, bewertet und exportiert werden. Bei fehlendem Modell kann ein einfaches Tabelleninventar zunächst zweckmäßiger sein.
- **Gebäuderessourcenpass:** BIM-Mengen und Klassifikationen können die Grundlage für Ressourcenpass, LCA und Materialbilanz bilden. Ergänzungen zu Verbindungen, Rückbau und Schadstoffen müssen gesondert erhoben werden.
- **Madaster-Workflow:** IFC- oder Excel-Daten werden hochgeladen, geprüft, klassifiziert, mit Datenbanken verknüpft und zu Materialpass, Zirkularitäts-, Umwelt- und Wertinformationen verarbeitet.
- **Concular-Workflow:** Bestandserfassung, Audit, Materialkatalogisierung, Matching, Rückbauplanung und Wiedereinbau werden in einen zirkulären Projektprozess eingebettet.
- **Planung mit Re-Use-Fenstern oder Türen:** BIM-Objekte können als konkrete Chargen mit realen Maßen und Zuständen modelliert werden. Entwurf und Raster müssen sich dann an vorhandenen Elementen orientieren, nicht umgekehrt.
- **Stahlträger-Re-Use:** BIM kann Profile, Längen, Massen und Lage erfassen. Tragfähigkeitsnachweise, Materialprüfung, Korrosion, Kerbschäden und Schweißbarkeit bleiben externe technische Prüfaufgaben.

## Herausforderungen / offene Fragen

- Welche Mindestdaten sind erforderlich, damit ein BIM-Objekt tatsächlich als wiederverwendungsfähiges Bauteil gilt?
- Wie lassen sich Zustand, Unsicherheit und Prüfstatus standardisiert in BIM bzw. IFC abbilden?
- Wie können zirkuläre Property-Sets softwareübergreifend zuverlässig exportiert und geprüft werden?
- Wie werden Materialpässe über Jahrzehnte aktuell gehalten, wenn Eigentümer, Software und Plattformen wechseln?
- Wer haftet für falsche oder veraltete Modellinformationen?
- Wie können Daten aus Rückbau, Lager, Marktplatz und Neubauplanung synchronisiert werden?
- Wie werden manuelle Bestandsaufnahmen, Fotos, Prüfberichte und physische Kennzeichnungen dauerhaft mit digitalen IDs verbunden?
- Welche Daten sollen offen sein, welche gehören in geschützte CDEs oder Plattformen?
- Wie kann Modellierungsaufwand proportional zum Wiederverwendungswert gehalten werden?

## Quellen

- buildingSMART International: Industry Foundation Classes / IFC, https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/
- buildingSMART International: openBIM, BCF, IDS und bSDD, https://www.buildingsmart.org/
- ISO 16739-1: Industry Foundation Classes (IFC) for data sharing in the construction and facility management industries.
- ISO 19650-1 / ISO 19650-2: Organization and digitization of information about buildings and civil engineering works, including BIM — Information management using BIM.
- DIN SPEC 91484:2023-09: Procedure to record building materials as a base to evaluate the potential for a high-quality reutilization prior to demolition and renovation work.
- DGNB: Gebäuderessourcenpass, https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- Madaster Documentation: Preparing BIM IFC source files; Material passports; API, https://docs.madaster.com/
- Concular: Zirkuläres Bauen, Urban Mining, Pre-Deconstruction Audit, https://concular.de/
- Platform CB’23: Passports for the Construction Sector, https://platformcb23.nl/
- Eastman, C.; Teicholz, P.; Sacks, R.; Liston, K.: BIM Handbook. Wiley.
