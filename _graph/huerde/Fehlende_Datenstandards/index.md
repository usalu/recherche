---
id: "Fehlende_Datenstandards"
entity: "huerde"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Fehlende Datenstandards"
legacy_type: "HÃ¼rde"
legacy_paths:
  - "huerde\Fehlende_Datenstandards.md"
target_primary: "huerde/Fehlende_Datenstandards"
target_secondary: ""
risk_flags: ""
---
# Fehlende Datenstandards

## Migration

- Target: huerde/Fehlende_Datenstandards
- Legacy source count: 1
- Legacy types: HÃ¼rde
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: huerde\Fehlende_Datenstandards.md

---
type: Hürde
verwandt: ["[[huerde/Ausschreibungsproblem]]", "[[huerde/Datenluecke]]"]
---

## Verknüpfungen

**Übergeordnete Themen**
- Hürden / Technisch und organisatorisch
- Datenmodell / Interoperabilität / Materialpass / BIM / Produktpass
- Standard / DIN SPEC 91484, ISO 19650, IFC, EN 15804, EU-Digital Product Passport
- Recht / Nachweisführung, Bauprodukte, öffentliche Beschaffung
- Logistik / Bauteiltracking, Plattformen, Lagerverwaltung
- Wirtschaft / Markttransparenz, Bewertung, Skalierung

**Verwandte Dateien**
- `datenmodell/Bauteilpass.md`
- `datenmodell/Materialpass.md`
- `datenmodell/IFC_BIM.md`
- `datenmodell/Produktidentifikation.md`
- `standard/DIN_SPEC_91484.md`
- `standard/ISO_19650.md`
- `standard/IFC.md`
- `standard/Digitaler_Produktpass.md`
- `standard/EPD_EN_15804.md`
- `huerde/Datenluecke.md`
- `huerde/Ausschreibungsproblem.md`
- `logistik/Bauteiltracking.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure: Normungsorganisationen, buildingSMART, DIN, ISO, Europäische Kommission, Plattformbetreiber, Softwareanbieter, Bauherrschaften, Planende, Hersteller, Rückbauunternehmen, Bauteilbörsen, Prüfstellen, Behörden.
- Fallstudien / Ansätze: BAMB Materials Passports; EU Digital Product Passport für Bauprodukte; DIN SPEC 91484; digitale Gebäudelogbücher; Materialkataster; openBIM/IFC; Re-Use-Plattformen.
- Standards / Datenrahmen: DIN SPEC 91484, ISO 19650, ISO 20887, IFC, bSDD, EN 15804, EN 15978, EU Level(s), CPR (EU) 2024/3110, ESPR-DPP-Logik.
- Methoden: gemeinsame Datenfelder, eindeutige Bauteil-ID, Klassifikation, Zustandsklassen, Prüfstatus, API-Schnittstellen, Mapping zwischen BIM, AVA, Lager, Marktplatz und Nachweisdokumenten.

## Kurzdefinition

Fehlende Datenstandards bezeichnen die Barriere, dass Informationen über wiederverwendbare Bauteile nicht einheitlich strukturiert, benannt, klassifiziert, ausgetauscht und über den Lebenszyklus fortgeschrieben werden. Anders als bei der Datenlücke geht es hier nicht primär darum, dass Informationen fehlen, sondern darum, dass vorhandene Informationen in inkompatiblen Formaten, Begriffen, Detailtiefen und Systemen vorliegen.

Ein Bauteil kann fotografiert, vermessen, geprüft und beschrieben sein; wenn aber jede Plattform andere Felder verwendet, Zustände anders klassifiziert, Bauteilgruppen unterschiedlich benennt und Nachweise nicht maschinenlesbar verknüpft, bleibt der Datensatz schwer nutzbar. Wiederverwendung skaliert erst, wenn Bauteildaten zwischen Rückbau, Planung, Ausschreibung, Prüfung, Lager, Marktplatz, BIM-Modell und Betrieb verlässlich fließen können.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung ist informationsintensiv. Für neue Bauprodukte existieren etablierte Datenketten: Herstellerdatenblätter, Produktnormen, Leistungserklärungen, CE-Kennzeichnung, EPDs, Ausschreibungstexte, BIM-Objekte und Händlerkataloge. Für gebrauchte Bauteile fehlen oft vergleichbare, standardisierte Datenflüsse.

Fehlende Datenstandards erzeugen Reibung an allen Schnittstellen:
- Rückbauinventare lassen sich nicht direkt in Re-Use-Marktplätze übertragen.
- Materialpässe sind nicht mit BIM- oder AVA-Systemen kompatibel.
- Bauteilbezeichnungen, Qualitätsklassen und Prüfstatus sind nicht vergleichbar.
- Plattformen können Bestände nicht zuverlässig aggregieren.
- Bauherrschaften können Re-Use-Ziele nicht einheitlich bilanzieren.
- Planende müssen Daten manuell übertragen und interpretieren.
- Prüfstellen erhalten uneinheitliche Unterlagen.
- Logistik und Lagerverwaltung verlieren Rückverfolgbarkeit.

Damit wird Wiederverwendung projektabhängig, manuell und schwer skalierbar. Der Markt bleibt fragmentiert, obwohl einzelne Projekte gute Daten erzeugen.

## Fachinhalt

### 1. Abgrenzung zur Datenlücke

**Datenlücke:** Ein Brandschutztürblatt hat kein Typenschild, keine Prüfunterlagen und unbekannte Dichtungen. Es fehlen Informationen.

**Fehlender Datenstandard:** Für dieselbe Tür liegen Fotos, Maße, Herstellerangaben und Prüfstatus vor, aber Plattform A nennt sie „Tür“, Plattform B „Feuerschutzabschluss“, BIM nutzt eine IFC-Klasse ohne Re-Use-Felder, das Lager führt eine Excel-Liste und die Ausschreibung benötigt andere Attribute. Die Informationen existieren, sind aber nicht interoperabel.

In der Praxis müssen beide Probleme getrennt adressiert werden: Erstens Daten erheben, zweitens Daten nach gemeinsamen Regeln strukturieren.

### 2. Zentrale Standardisierungslücken

**Uneinheitliche Bauteilklassifikation:** Es gibt keine allgemein durchgesetzte, reuse-spezifische Klassifikation, die Bauteiltyp, Funktion, Einbaulage, Material, Systemzugehörigkeit und Anschlussnutzung eindeutig verbindet. Bestehende Klassifikationen aus Kostenplanung, BIM oder Produktkatalogen sind nicht immer auf Rückbau und Wiederverwendung ausgelegt.

**Fehlende Zustands- und Qualitätsklassen:** Begriffe wie „gut erhalten“, „gebrauchsfähig“, „sanierungsbedürftig“, „geprüft“, „as-is“, „refurbished“ oder „re-use ready“ werden uneinheitlich verwendet. Für Käufer:innen ist unklar, ob damit Sichtprüfung, technische Prüfung oder nur Händlerangabe gemeint ist.

**Unklare Prüfstatus-Logik:** Wiederverwendung braucht eine klare Trennung zwischen ungeprüft, vorbewertet, schadstoffgeprüft, technisch geprüft, bauaufsichtlich bewertet, freigegeben und eingebaut. Ohne Standard werden Risiken verdeckt.

**Keine durchgängige eindeutige Identifikation:** Bauteile brauchen über Ausbau, Transport, Lagerung, Verkauf, Einbau und Betrieb hinweg eine eindeutige ID. Ohne stabile Kennung gehen Herkunft, Prüfungen und Dokumente verloren.

**Mangelnde Semantik:** Ein Datenfeld „Material“ kann Hauptmaterial, Oberflächenmaterial, Verbundaufbau oder Recyclingfraktion bedeuten. Semantische Standards müssen definieren, was ein Feld genau meint.

**Dokumentenverknüpfung:** Fotos, Gutachten, Prüfberichte, Leistungserklärungen, EPDs, Wartungsprotokolle und Schadstoffanalysen liegen oft als PDFs oder Bilddateien vor, aber ohne strukturierte Zuordnung zu Bauteil, Version, Prüfdatum und Gültigkeitsbereich.

**Interoperabilität zwischen Softwareinseln:** BIM-Modelle, CAFM-Systeme, AVA-Programme, Marktplätze, Lagerverwaltungssoftware, LCA-Tools und Behördenportale nutzen unterschiedliche Datenmodelle. Manuelle Übertragung erzeugt Fehler und Kosten.

**Fehlende Definition von Re-Use-Kennzahlen:** Re-Use-Anteil kann nach Masse, Volumen, Stückzahl, Kosten, CO₂-Einsparung oder Bauteilwert berechnet werden. Ohne gemeinsame Methode sind Projektziele und Benchmarks nicht vergleichbar.

### 3. Bestehende Standardisierungsansätze

**DIN SPEC 91484:** Die DIN SPEC 91484 beschreibt ein Verfahren zur Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten als Grundlage für die Bewertung des Anschlussnutzungspotenzials. Sie ist ein wichtiger Schritt, weil sie die Bestandserfassung strukturiert. Sie löst aber nicht automatisch alle Fragen der digitalen Interoperabilität, Plattformintegration und internationalen Klassifikation.

**BAMB Materials Passports:** Das EU-Projekt BAMB hat Materialpässe und reversible Gebäudekonzepte als Werkzeuge für zirkuläre Wertschöpfung entwickelt. Materialpässe zeigen, welche Daten für Rückgewinnung, Wert und Anschlussnutzung relevant sind. Die Herausforderung bleibt, diese Ansätze in Alltagssoftware, Normung und Beschaffung zu verankern.

**EU Digital Product Passport und CPR 2024/3110:** Die neue EU-Bauproduktenverordnung führt einen digitalen Produktpass für Bauprodukte ein. Dieser kann langfristig Produktinformationen, Nachhaltigkeitsdaten, Konformität und Rückverfolgbarkeit stärken. Für heute bereits verbaute Bestandsbauteile bleibt aber offen, wie historische Produkte ohne ursprünglichen digitalen Pass integriert werden.

**ISO 19650 und BIM-Informationsmanagement:** ISO 19650 gibt Prinzipien für Informationsmanagement mit BIM vor. Sie hilft bei Rollen, Prozessen und Informationsanforderungen, ist aber kein spezifischer Re-Use-Bauteildatenstandard.

**IFC / openBIM:** IFC ermöglicht den Austausch von Gebäudemodelldaten. Für Wiederverwendung müssen jedoch zusätzliche Attribute zu Zustand, Herkunft, Demontage, Prüfung, Lagerung und Anschlussnutzung definiert oder verlässlich gemappt werden.

**EN 15804 / EPDs und EN 15978:** Diese Standards strukturieren Umweltproduktdeklarationen und Gebäudebilanzierung. Für Re-Use sind sie wichtig, weil ökologische Vorteile nachweisbar werden müssen. Sie ersetzen aber keinen Bauteilpass und keine technischen Eignungsdaten.

**EU Level(s):** Level(s) bietet einen Rahmen zur Bewertung von Ressourceneffizienz, Lebenszyklus und Kreislauffähigkeit von Gebäuden. Es kann Re-Use-Ziele einbetten, aber es ist kein operativer Lager- oder Bauteildatenstandard.

### 4. Anforderungen an einen Re-Use-Datenstandard

Ein belastbarer Datenstandard für Wiederverwendung sollte mindestens abdecken:

- eindeutige Bauteil-ID und Versionierung
- Herkunftsgebäude, Standort, Ausbauzeitpunkt
- Eigentum und Freigabestatus
- Bauteilgruppe, Funktion, Material, Systemzugehörigkeit
- Maße, Gewicht, Geometrie, Toleranzen
- Zustand, Schäden, Reparaturen, Oberflächen
- Verbindung, Demontageaufwand, Bruchrisiko
- technische Eigenschaften und Leistungsnachweise
- Schadstoffinformationen und Prüfberichte
- Brandschutz-, Schallschutz-, Tragwerks- und Hygieneanforderungen
- Lagerort, Verpackung, Handling, Transportbedingungen
- Verfügbarkeit, Reservierung, Preis, Menge
- zulässige Anschlussnutzungen und Einschränkungen
- ökologische Daten: vermiedene Herstellung, Re-Use-Anteil, Bilanzannahmen
- Prüfstatus, Prüfstelle, Datum, Gültigkeitsbereich
- Schnittstellen zu BIM, AVA, LCA, Marktplatz, Lager und Betrieb

Wichtig ist eine abgestufte Datentiefe: Nicht jedes Bauteil benötigt den gleichen Aufwand. Ein Standard muss zwischen einfacher Wiederverwendung im Innenausbau und hochkritischen tragenden oder brandschutzrelevanten Bauteilen unterscheiden.

### 5. Daten-Governance

Datenstandards sind nicht nur technische Tabellen. Sie müssen Verantwortlichkeiten klären:
- Wer erstellt den ersten Datensatz?
- Wer darf Informationen ändern?
- Wer bestätigt Prüfstatus und Freigabe?
- Wie werden Versionen dokumentiert?
- Wie werden Fehler korrigiert?
- Wer haftet für falsche Angaben?
- Welche Daten sind öffentlich, vertraulich oder sicherheitsrelevant?
- Wie lange müssen Daten nach Einbau erhalten bleiben?

Ohne Governance entstehen Scheingenauigkeit und Haftungsrisiken. Ein Re-Use-Bauteilpass muss daher Datenqualität, Quelle und Verantwortlichkeit sichtbar machen.

## Praxisbezug / Beispiele

**Excel-Inventar versus BIM-Modell:** Viele Rückbauinventare entstehen in Tabellen mit Fotos und Kommentaren. Planende arbeiten jedoch in BIM oder CAD. Ohne standardisierte Feldnamen und IDs müssen Informationen manuell übertragen werden; dabei gehen Prüfstatus, Unsicherheiten und Dokumentlinks verloren.

**Marktplatzdaten:** Ein Bauteilmarkt kann „100 Türen, guter Zustand“ anzeigen. Für eine Ausschreibung braucht die Planung jedoch Maße, Anschlagrichtung, Brand- und Schallschutz, Zargen, Beschläge, Prüfstatus, Liefertermin und Reservierbarkeit. Ohne standardisierte Pflichtfelder bleibt das Angebot unverbindlich.

**Materialpass im Neubau:** Ein Gebäude kann heute mit Materialpass geplant werden. Wenn der Pass aber keine maschinenlesbaren Daten, eindeutigen IDs, Austauschformate und Updateprozesse hat, ist er in 30 Jahren möglicherweise nur ein statisches PDF und für Wiederverwendung begrenzt nützlich.

**EPD-Daten:** Umweltproduktdeklarationen sind hilfreich für ökologische Bewertung neuer Produkte. Bei gebrauchten Bauteilen müssen jedoch Herkunft, Restlebensdauer, Aufbereitung und vermiedene Neuproduktion ergänzt werden. Ein EPD-Standard allein bildet diese Re-Use-Logik nicht vollständig ab.

**Öffentliche Beschaffung:** Vergabestellen brauchen vergleichbare Nachweise. Wenn Anbieter Re-Use-Anteile unterschiedlich berechnen, können Angebote nicht fair bewertet werden. Standardisierte Re-Use-Kennzahlen und Nachweislisten sind daher vergaberelevant.

## Herausforderungen / offene Fragen

- Welche Datenfelder sollten europaweit verpflichtend, welche projektspezifisch optional sein?
- Wie können Bestandsbauteile ohne historische Produktdaten in zukünftige digitale Produktpass-Systeme integriert werden?
- Wie werden IFC, Materialpässe, EPDs, Lagerdaten und Ausschreibungsdaten semantisch verbunden?
- Wer betreibt vertrauenswürdige Register für Bauteil-IDs, Prüfstatus und Nachweise?
- Wie wird verhindert, dass komplexe Datenanforderungen kleine Re-Use-Akteure ausschließen?
- Wie können offene Standards mit kommerziellen Plattformen vereinbart werden?
- Welche Datenqualität genügt für nicht sicherheitskritische Bauteile, welche ist für tragende oder brandschutzrelevante Bauteile erforderlich?
- Wie werden Änderungen nach Ausbau, Reinigung, Reparatur und Wiedereinbau versioniert?
- Unsicher / im Wandel: EU-Digital-Product-Passport-Anforderungen für Bauprodukte werden schrittweise konkretisiert. Für bestehende, bereits verbaute Produkte ist die praktische Einbindung noch nicht abschließend geklärt.

## Quellen

- DIN Media: *DIN SPEC 91484:2023-09 – Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des hochwertigen Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten*. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- Europäische Union: *Regulation (EU) 2024/3110 laying down harmonised rules for the marketing of construction products*, insbesondere Kapitel zum Digital Product Passport. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
- Belgian Federal Public Service Economy: *The Digital Product Passport for construction products*, 2025. https://economie.fgov.be/en/themes/enterprises/specific-sectors/construction/construction-products/regulation-eu-20243110/digital-product-passport
- BAMB / Buildings as Material Banks: *Materials Passports – Best Practice*, 2019. https://globalabc.org/sustainable-materials-hub/resources/bamb-materials-passports-best-practice
- BAMB: Übersicht Berichte und Publikationen zu Material Passports und Reversible Building Design. https://www.bamb2020.eu/library/overview-reports-and-publications/
- CORDIS / European Commission: *BAMB – Buildings as Material Banks: project results*. https://cordis.europa.eu/project/id/642384/results
- buildingSMART International: *Industry Foundation Classes (IFC)*. https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/
- ISO: *ISO 19650 – Organization and digitization of information about buildings and civil engineering works, including BIM*. https://www.iso.org/standard/68078.html
- ISO: *ISO 20887:2020 – Sustainability in buildings and civil engineering works — Design for disassembly and adaptability*. https://www.iso.org/standard/69370.html
- Europäische Kommission: *Level(s) – European framework for sustainable buildings*. https://environment.ec.europa.eu/topics/circular-economy/levels_en
- FCRBE / Brussels Environment: *Digital tools for Reuse*, 2024. https://guidebatimentdurable.brussels/sites/default/files/documents/2024-05/fcrbe_digital-tools-for-reuse_final-version_compressed.pdf

