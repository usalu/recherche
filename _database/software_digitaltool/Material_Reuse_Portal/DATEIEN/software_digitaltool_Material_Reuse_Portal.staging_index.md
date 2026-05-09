---
id: "Material_Reuse_Portal"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Material Reuse Portal"
source_count: 2
legacy_paths:
  - "bauteilboerse\\material-reuse-portal.md"
  - "werkzeug\\Material_Reuse_Portal.md"
raw_targets:
  - "software_digitaltool/Material_Reuse_Portal"
migration_actions:
  - "semantic_move"
  - "split_platform_profile"
risk_flags:
  - "duplicate_with_akteur_or_werkzeug"
  - "may_duplicate_bauteilboerse_or_akteur"
---
# Material Reuse Portal

## Migration

- Canonical target: software_digitaltool/Material_Reuse_Portal
- Legacy source count: 2
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: bauteilboerse\material-reuse-portal.md

- Map action: split_platform_profile
- Target role in map: primary
- Raw mapped target: software_digitaltool/material_reuse_portal
- Original primary target: software_digitaltool/material_reuse_portal
- Original secondary targets: akteur/<operator_if_named>; beschaffungsweg/Digitale_Plattform; ressourcenquelle/Bauteilboerse; plattformfunktion/Material_Matching

---
type: Bauteilbörse
---

# Material Reuse Portal

## Kurzbeschreibung
Material Reuse Portal ist ein(e) Aggregator/Portal für wiederverwendbare Bau- und Abbruchmaterialien mit Bezug zu Vereinigtes Königreich; London-/UK-Fokus. Im Reuse-Kontext liegt der Schwerpunkt auf: Bündelt verfügbare Reuse-Angebote aus externen Marktplätzen, um Wiederverwendung leichter auffindbar zu machen.

## Land / Region
Vereinigtes Königreich; London-/UK-Fokus

## Betreiber
CIRCuIT-/ReLondon-Kontext; konkreter laufender Betreiber nicht vollständig angegeben

## Zielgruppe
Planende, Bauunternehmen, Bauherrschaft, Material-Suchende im UK-Kontext

## Plattformtyp
Aggregator/Portal für wiederverwendbare Bau- und Abbruchmaterialien

## Bauteilkategorien
wiederverwendbare Materialien aus verschiedenen Marktplätzen; Kategorien hängen von angeschlossenen Quellen ab

## Art der Wiederverwendung
Bündelt verfügbare Reuse-Angebote aus externen Marktplätzen, um Wiederverwendung leichter auffindbar zu machen

## Funktionen
aggregierte Suche; Verweis auf Quellmarktplätze; Informationsportal zu Reuse-Materialien

## Daten je Bauteil
abhängig von externen Marktplätzen; Portal übernimmt/zeigt aggregierte Listingdaten

## Qualität / Prüfung
keine eigene Prüfung als Verkäufer angegeben; Qualität liegt bei Ursprungsplattform/Anbieter

## Logistik / Lagerung
Portal verkauft nicht selbst; Logistik über Quellmarktplatz/Anbieter

## Geschäftsmodell
Proof-of-concept/Portal; Geschäftsmodell nicht angegeben

## Ökologische Bewertung
senkt Suchkosten für Reuse-Materialien und kann dadurch Abfallvermeidung unterstützen; quantitative Bewertung nicht angegeben

## Stärken
macht verstreute Bestände sichtbar; hilfreich für Sourcing und Marktrecherche

## Schwächen / Hemmnisse
kein Verkäufer; abhängig von Datenqualität und Aktualität externer Plattformen

## Relevanz für zirkuläres Bauen
mittel bis hoch als Suchinfrastruktur für zirkuläre Beschaffung, weniger als direkte Bauteilbörse.

## Quellen und Links
- https://materialreuseportal.com/
- https://www.materialreuseportal.com/About
- https://relondon.gov.uk/built-environment
- https://ukgbc.org/resources/aggregated-material-reuse-marketplace/

---
Hinweis: Verfügbarkeit, Zustand, Maße, Normen- und Brandschutzanforderungen müssen vor Spezifikation oder Kauf direkt mit Anbieter/Betreiber geprüft werden.

### Legacy Source: werkzeug\Material_Reuse_Portal.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Material_Reuse_Portal
- Original primary target: software_digitaltool/Material_Reuse_Portal
- Original secondary targets: 

---
type: Werkzeug
methode: ["[[methode/Urban_Mining]]"]
verwandt: ["[[werkzeug/BIM]]", "[[werkzeug/CMEx]]", "[[werkzeug/Excess_Materials_Exchange]]", "[[werkzeug/Globechain]]", "[[werkzeug/Materialdatenbank]]", "[[werkzeug/Opalis_Plattform]]", "[[werkzeug/Restado]]", "[[werkzeug/Reusefully_LINK]]", "[[werkzeug/SalvoWEB]]"]
---

# Material Reuse Portal

## Verknüpfungen

- **Übergeordnete Themen:** digitale Materialbörse, Marktplatz-Aggregator, zirkuläre Stadt, CIRCuIT, Urban Mining, Materialpass, offene Daten, wiederverwendbare Bauprodukte.
- **Verwandte Dateien:** `werkzeug/Opalis_Plattform.md`, `werkzeug/SalvoWEB.md`, `werkzeug/Materialdatenbank.md`, `werkzeug/BIM.md`, `datenmodell/Materialpass.md`, `methode/Urban_Mining.md`, `methode/Pre_Demolition_Audit.md`, `akteur/ReLondon.md`, `logistik/Zwischenlager.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ReLondon, CIRCuIT-Projekt, London / Greater London, bestehende Marktplätze, Rückbauunternehmen, Planer, Kommunen; Uniclass, Materialpass, Marktplatz-Aggregation, Nachfrageanalyse, Such- und Filterdaten.

## Kurzdefinition

Das Material Reuse Portal ist eine im Rahmen des EU-Horizon-2020-Projekts CIRCuIT entwickelte Plattform, die verfügbare wiederverwendbare Baumaterialien aus mehreren bestehenden Marktplätzen an einem Ort auffindbar machen soll. Es ist weniger ein einzelner Händler oder Lagerbetreiber als ein **Aggregator**: Der Mehrwert liegt in der Bündelung fragmentierter Angebote, in standardisierter Kategorisierung und in der Möglichkeit, Daten über Interesse und Nachfrage nach wiederverwendbaren Bauteilen zu erzeugen.

## Relevanz für Wiederverwendung im Bauwesen

Das Material Reuse Portal hat eine spezifische Reuse-Nutzung, weil es ein zentrales Problem adressiert: Reuse-Angebote sind häufig auf viele kleine Plattformen, Händler, Rückbauprojekte und Anzeigen verteilt. Für Planer und Bauherrschaften ist die Suche nach geeigneten Bauteilen dadurch aufwendig. Das Portal versucht, diese Fragmentierung durch eine übergreifende Such- und Datenebene zu reduzieren.

Für Wiederverwendung relevant sind:

- **Bündelung von Angeboten:** Materialien aus mehreren Quellen werden zusammengeführt.
- **Auffindbarkeit:** Planer und Beschaffer können über eine gemeinsame Oberfläche suchen.
- **Standardisierung:** Kategorien und Klassifikationen sollen Angebote vergleichbarer machen.
- **Materialpassfunktion:** Nutzer können Daten zu interessanten Listings speichern, die später als digitaler Pass oder Datensatz dienen können.
- **Nachfragedaten:** Suchanfragen und gespeicherte Interessen können zeigen, welche Produktgruppen für Wiederverwendung tatsächlich nachgefragt werden.
- **Stadt- und Regionalbezug:** Das Portal ist als Werkzeug für urbane Kreislaufwirtschaft gedacht, nicht nur als Einzelprojektlösung.

## Fachinhalt

### Aggregatorprinzip

Ein klassischer Materialmarktplatz sammelt eigene Angebote. Das Material Reuse Portal verfolgt dagegen das Prinzip, Angebote aus verschiedenen Quellen sichtbar zu machen. Damit vermeidet es, mit bestehenden Marktplätzen direkt zu konkurrieren. Stattdessen entsteht eine übergeordnete Suchschicht, die Nutzer zu den ursprünglichen Anbietern weiterleiten kann.

Dieses Modell ist für Wiederverwendung besonders wichtig, weil der Markt für gebrauchte Bauprodukte stark fragmentiert ist. Viele Plattformen sind regional, materialbezogen oder händlerbezogen. Ein Aggregator kann die Suchkosten reduzieren und Markttransparenz erhöhen.

### Datentypen

Typische Datenfelder sind:

- Produkt- oder Materialkategorie.
- Titel, Beschreibung, Fotos.
- Menge, Maße, Einheit und Zustand, soweit verfügbar.
- Standort oder Liefergebiet.
- Preis oder Angebotsstatus, falls vom Ursprungssystem geliefert.
- Anbieter oder Marktplatzquelle.
- Klassifikation, im Portal insbesondere mit Bezug auf Uniclass.
- gespeicherte Nutzerinteressen und potenzielle Materialpassdaten.

Die Qualität der Daten hängt stark von den angebundenen Marktplätzen ab. Ein Aggregator kann fehlende technische Nachweise nicht automatisch ersetzen.

### Klassifikation und BIM-Bezug

Das Portal nutzt nach eigenen FAQ Informationen die Uniclass-Systematik als Kategorisierungsgrundlage. Das ist relevant, weil Uniclass im Bauwesen als Klassifikationssystem für Produkte, Systeme und Projektinformationen eingesetzt wird und mit BIM-Prozessen kompatibel sein kann. Für Wiederverwendung ist eine gemeinsame Klassifikation entscheidend, damit ein gebrauchtes Bauteil nicht nur als freie Textanzeige, sondern als planungsrelevanter Gegenstand gefunden werden kann.

### Funktionale Einordnung

- **Nicht primär BIM-Tool:** Es erzeugt kein detailliertes Planungsmodell.
- **Nicht primär Prüfwerkzeug:** Es ersetzt keine technische Bewertung der Bauteile.
- **Nicht primär Händler:** Es bündelt Angebote und verweist auf bestehende Anbieter.
- **Primär Marktinfrastruktur:** Es verbessert Auffindbarkeit, Vergleichbarkeit und Datengrundlage für Reuse-Märkte.

### Beziehung zu CIRCuIT

CIRCuIT entwickelte mehrere digitale Werkzeuge zur Unterstützung zirkulären Bauens in Städten. Das Material Reuse Portal ist dabei die Such- und Marktplatzkomponente für verfügbare Materialien. Ergänzende CIRCuIT-Werkzeuge wie Circularity Dashboard, Circularity Atlas und Wissensplattformen liefern eher strategische oder politische Entscheidungsgrundlagen.

## Praxisbezug / Beispiele

Typische Nutzung:

- Ein Architekturbüro sucht gebrauchte Türen, Bodenbeläge, Sanitärobjekte oder Fassadenelemente für ein Londoner Projekt und durchsucht nicht mehrere Einzelportale, sondern einen aggregierten Bestand.
- Eine Kommune möchte wissen, welche Bauteilkategorien regional verfügbar sind, und nutzt Portal- oder Nachfrageinformationen zur Entwicklung von Reuse-Strategien.
- Rückbauunternehmen erhalten indirekt Hinweise, welche Bauteile gefragt sind und deshalb bei kommenden Rückbauprojekten selektiv ausgebaut werden sollten.
- Ein Materialhändler kann über die Einbindung in das Portal zusätzliche Sichtbarkeit erhalten.

Geeignete Materialgruppen sind vor allem standardisierbare oder häufig wiederverwendbare Bauteile: Türen, Fenster, Sanitärobjekte, Bodenbeläge, Fassadenplatten, Ziegel, Holz, Stahlbauteile, Möbel, Leuchten und Innenausbauprodukte.

## Herausforderungen / offene Fragen

- **Status als Proof of Concept:** Das Portal ist stark mit CIRCuIT und London verknüpft; operative Verfügbarkeit und Angebotsdichte müssen projektaktuell geprüft werden.
- **Abhängigkeit von Drittplattformen:** Datenqualität, Verfügbarkeit, Preise und Aktualität liegen oft beim Ursprungssystem.
- **Keine automatische Qualitätssicherung:** Technische Eignung, Schadstofffreiheit, Brandschutz und Gewährleistung müssen separat geprüft werden.
- **Fragmentierte Transaktionen:** Auch wenn die Suche zentralisiert ist, können Kauf, Reservierung, Logistik und Vertragsabschluss weiterhin auf separaten Plattformen erfolgen.
- **Regionale Begrenzung:** Das Modell ist replizierbar, aber Marktdichte, Plattformpartner und Klassifikationssysteme unterscheiden sich je Stadt.
- **Datenstandardisierung:** Freitextanzeigen sind schwer mit Planungs- und Ausschreibungsprozessen zu verbinden; technische Mindestdaten bleiben entscheidend.
- **Logistik:** Auffindbarkeit allein löst nicht Lagerung, Transport, Versicherung und Terminabgleich.

## Quellen

- Material Reuse Portal, offizielle Website: https://materialreuseportal.com/
- Material Reuse Portal, FAQ: https://materialreuseportal.com/Faq
- CIRCuIT Project Report, Supporting circular construction with digital tools: https://report.circuit-project.eu/chapter/supporting-circular-construction-with-digital-tools
- ReLondon, Built environment resources: https://relondon.gov.uk/built-environment
- UKGBC, Aggregated Material Reuse Marketplace: https://ukgbc.org/resources/aggregated-material-reuse-marketplace/
- CIRCuIT / MRP Methodology PDF: https://www.materialreuseportal.com/content/cmep-design-build-internationalisation-methodology-v2.pdf
- ASBP, Digital Platforms, Physical Hubs and Facilitators for Reuse: https://asbp.org.uk/article/reuse-digital-platforms-and-physical-hubs
- Hinweis: Angebotsdichte und Plattformintegrationen vor Nutzung aktuell prüfen. Abrufstand: 2026-04-27.
