---
entity: "datenmodell"
id: "Materialdatenbank"
title: "Materialdatenbank"
build_status: "promoted_phase42"
legacy_paths:
  - "dokument\Materialdatenbank.md"
node_kind: "knot"
legacy_type: "Dokument"
---

# Materialdatenbank

﻿## Verknüpfungen

**Übergeordnete Themen**
- [[../werkzeug/Materialpass]]
- [[../werkzeug/BIM]]
- [[../werkzeug/Urban_Mining_Plattform]]
- [[../standard/DIN_SPEC_91484]]
- [[../standard/EN_15804]]
- [[../standard/IFC]]
- [[../kennwert/GWP]]
- [[../kennwert/ReUse_Potenzial]]

**Verwandte Dateien**
- [[Bauteilkatalog]]
- [[Materialsheet]]
- [[LCA]]
- [[Opalis_Datenbank]]
- [[ReUse_Toolkit]]
- [[Ausschreibungstext]]
- [[Reversibilitaetskonzept]]

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Bauherrschaft, Asset Management, Planende, Auditor:innen, Plattformbetreiber, EPD-Datenbanken, Hersteller, Rückbauunternehmen.
- Fallstudien/Systeme: BAMB Materials Passports, Madaster, Concular, Opalis, ÖKOBAUDAT, KBOB, baubook, EU Level(s).
- Materialien: alle Bauproduktgruppen; besonders hohe Mengen, hohe Umweltwirkung oder hohes Wiederverwendungspotenzial.
- Methoden: Materialpass, Bauteil-ID, Datenqualitätsstufen, IFC/BIM-Verknüpfung, Klassifikation, API/Export, LCA-Datenverknüpfung.

## Kurzdefinition

Eine **Materialdatenbank** ist eine strukturierte digitale Sammlung von Material-, Produkt-, Bauteil-, Umwelt- und Bestandsdaten. Sie kann Bauteilkataloge, Materialpässe, EPDs, Prüfberichte, Rückbauhinweise, LCA-Daten und Marktdaten verknüpfen.

Abgrenzung: Der `Bauteilkatalog` ist projekt- oder gebäudespezifisch und listet konkrete Bauteile. Das `Materialsheet` ist generisches Fachwissen zu einer Produktgruppe. Die `Materialdatenbank` ist die übergreifende Dateninfrastruktur.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung ist datenabhängig. Materialien bleiben nur dann als zukünftige Ressourcen nutzbar, wenn Informationen über Menge, Ort, Qualität, Verbindung, Schadstoffe, Eigentum, Rückbaubarkeit und Umweltwirkung erhalten bleiben. Eine Materialdatenbank unterstützt Urban Mining, Entwurf, Ausschreibung, LCA, Materialpässe, Rückbauplanung, Sekundärmärkte und Monitoring von Re-Use-Quoten.

## Fachinhalt

### Datentypen
- **Materialdaten:** Materialart, Zusammensetzung, Dichte, Masse, Schichten, Schadstoffe, Recycling- und Re-Use-Eignung.
- **Produktdaten:** Hersteller, Typ, Seriennummer, EPD, Leistungserklärung, Wartung, Maße, technische Werte.
- **Bauteildaten:** Einbauort, Bauteil-ID, Zustand, Verbindung, Fotos, Prüfberichte, Rückbaubarkeit.
- **Gebäudedaten:** Pläne, BIM-Modelle, Baujahr, Umbauhistorie, Eigentum, Rückbauzeitpunkt.
- **Umweltdaten:** GWP, Primärenergie, Ressourcenverbrauch, Wiederverwendungspotenzial, Modul-D-Szenarien.

### Granularität
Die Datenbank muss Ebenen sauber trennen: Material, Produkt, Bauteil, Charge, System, Gebäude, Portfolio. Für direkte Wiederverwendung reichen grobe Materialmassen nicht aus; notwendig sind Objekt- oder Chargendaten mit Zustand, Maße, Verbindung und Freigabestatus. Für frühe Urban-Mining-Strategien können Massen- und Materialdaten genügen.

### Mindestdaten für Re-Use
- eindeutige ID;
- Material-/Produktgruppe;
- Menge und Einheit;
- Ort / Einbauort;
- Maße und Gewicht;
- Zustand;
- Verbindung und Demontierbarkeit;
- Schadstoffstatus;
- technische Funktion;
- Eigentum und Verfügbarkeit;
- Aufbereitungsbedarf;
- mögliche Anschlussnutzung;
- LCA-Datensatz oder Umweltkennwert;
- Datenvertrauensniveau.

### Datenqualität
Daten sollten nach Vertrauensniveau gekennzeichnet werden:
- **A:** geprüft, gemessen, dokumentiert;
- **B:** fachlich erfasst, aber noch nicht vollständig geprüft;
- **C:** aus Plänen oder Sichtprüfung abgeleitet;
- **D:** geschätzt oder unsicher.

Ohne solche Kennzeichnung erzeugen Datenbanken scheinbare Genauigkeit, die Ausschreibung, LCA und Haftung gefährden kann.

### Interoperabilität
Notwendig sind offene Exportformate (CSV, XLSX, JSON, IFC), stabile IDs, Klassifikationssysteme, Versionierung, Rollenkonzepte, Verlinkung zu Fotos/Plänen/Prüfberichten und langfristige Archivierung. Proprietäre Systeme sind riskant, wenn Daten beim Eigentümerwechsel oder nach Projektende nicht übertragbar sind.

## Praxisbezug / Beispiele

- **BAMB Materials Passports:** elektronische Datensätze sollen Informationen zu Materialien, Produkten und Komponenten zugänglich machen, damit Wiederverwendung, Rücknahme und reversible Planung erleichtert werden.
- **Portfolio-Urban-Mining:** Eine Wohnungsbaugesellschaft koppelt Sanierungen mit Neubauprojekten, indem Türen, Heizkörper oder Pflaster vorab als verfügbare Ressource geführt werden.
- **Ausschreibung:** geprüfte Datenbankeinträge können Vertragsanlage werden; dabei muss klar sein, welche Felder verbindlich und welche informativ sind.
- **LCA:** Mengen und Bauteil-IDs werden mit EPD- oder Datenbankwerten verknüpft; Unsicherheiten bleiben sichtbar.

## Herausforderungen / offene Fragen

- keine einheitliche internationale Datenstruktur für Re-Use-Materialpässe;
- hoher Pflegeaufwand über lange Gebäudenutzungsdauer;
- Haftungsfrage bei falschen oder veralteten Daten;
- unterschiedliche Klassifikationen in BIM, EPD, Kostenplanung und Marktplätzen;
- Datenschutz, Eigentum und Sicherheitsinteressen;
- Daten allein erzeugen keinen Markt: Rückbau, Logistik, Lagerung und Nachfrage bleiben erforderlich.

## Quellen

- FCRBE / Interreg NWE: Facilitating the circulation of reclaimed building elements in Northwestern Europe, Projektoutputs und Final Report. https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- Opalis: Documentation, Material Sheets, Procurement Strategies, Reclamation Audit, FutuREuse Booklets. https://opalis.eu/en/documentation
- European Commission: EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works, Updated edition 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- DIN SPEC 91484:2023-09: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des hochwertigen Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- ISO 20887:2020: Sustainability in buildings and civil engineering works — Design for disassembly and adaptability. https://www.iso.org/standard/69370.html
- BAMB: Materials Passports. https://www.bamb2020.eu/topics/materials-passports/
- BAMB: Reversible Building Design. https://www.bamb2020.eu/topics/reversible-building-design/
- Heinrich, M.; Lang, W.: Materials Passports — Best Practice. BAMB, 2019.
- European Commission: Level(s). https://environment.ec.europa.eu/topics/circular-economy/levels_en
- ÖKOBAUDAT. https://www.oekobaudat.de/
- KBOB / ecobau: Ökobilanzdaten im Baubereich. https://www.kbob.admin.ch/

id:
name: Materialdatenbank
type:
status: seed
aliases: []
tags: []
source_notes: []
links:
  related_akteure: []
  related_fallstudien: []
  related_gebaeude: []
  related_bauteile: []
  related_tragwerkssysteme: []
  related_materialien: []
  related_methoden: []
  related_abbruchmethoden: []
  related_aufbereitungsmethoden: []
  related_pruefungen: []
  related_logistiken: []
  related_dokumente: []
  related_standards: []
  related_huerden: []
  related_foerderprogramme: []
  related_orte: []
  related_werkzeuge: []
  related_interviews: []
  related_berichte: []
---

# Materialdatenbank

## Kurzdefinition

## Warum relevant fuer Reuse

## Wichtige Verbindungen

## Evidenz / Beispiele

## Offene Fragen
