---
id: "Platform_CB23"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Platform CB23"
source_count: 1
legacy_paths:
  - "werkzeug\\Platform_CB23.md"
raw_targets:
  - "software_digitaltool/Platform_CB23"
migration_actions:
  - "semantic_move"
risk_flags:
  - "may_duplicate_bauteilboerse_or_akteur"
---
# Platform CB23

## Migration

- Canonical target: software_digitaltool/Platform_CB23
- Legacy source count: 1
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: werkzeug\Platform_CB23.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Platform_CB23
- Original primary target: software_digitaltool/Platform_CB23
- Original secondary targets: 

---
type: Werkzeug
verwandt: ["[[werkzeug/DGNB_Gebaeuderessourcenpass]]", "[[werkzeug/Madaster_Plattform]]", "[[werkzeug/One_Click_LCA_Building_Circularity]]", "[[werkzeug/Pre_Demolition_Audit_Tools]]", "[[werkzeug/Urban_Mining_Index]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Circular Construction, Messmethodik, Materialpässe, Beschaffung, Wiederverwendung, Standards, Niederlande, zirkuläre Bauwirtschaft.
- **Verwandte Dateien:** `werkzeug/DGNB_Gebaeuderessourcenpass.md`, `werkzeug/Urban_Mining_Index.md`, `werkzeug/One_Click_LCA_Building_Circularity.md`, `werkzeug/Madaster_Plattform.md`, `werkzeug/Pre_Demolition_Audit_Tools.md`, `datenmodell/Materialpass.md`, `methode/Zirkularitaetsbewertung.md`, `methode/Zirkulaere_Beschaffung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Platform CB’23, Rijkswaterstaat, niederländische Bauwirtschaft, Guide Measuring Circularity, Guide Passports for the Construction Sector, Lexicon, Circular Procurement, Reuse, Design.

## Kurzdefinition

**Platform CB’23** ist eine niederländische Plattform zur Entwicklung gemeinsamer Vereinbarungen für zirkuläres Bauen. Sie stellt Leitfäden zu Begriffen, Messung von Zirkularität, Pässen, Design, Beschaffung und Wiederverwendung bereit. Platform CB’23 ist kein einzelnes Softwaretool, aber eine wichtige **methodische Infrastruktur** für digitale Werkzeuge.

## Relevanz für Wiederverwendung im Bauwesen

Digitale Reuse-Tools brauchen gemeinsame Begriffe und Messlogiken. Ohne Standards bleibt unklar, was als reuse, recycling, circularity, passport, demountable oder value retention gilt. Platform CB’23 ist relevant, weil sie genau diese methodische Verständigung unterstützt.

Für Wiederverwendung ist die Plattform wichtig durch:

- Begriffsdefinitionen für zirkuläres Bauen,
- Messindikatoren für Circularity,
- Passlogik für Produkte, Bauteile und Bauwerke,
- Orientierung für zirkuläre Beschaffung,
- Verknüpfung von Materialerhalt, Umweltwirkung und Werterhalt,
- Übertragbarkeit auf digitale Tools und Datenmodelle.

## Fachinhalt

### Messlogik

Der Guide „Measuring Circularity“ benennt drei zentrale Ziele zirkulären Bauens:

1. **Schutz von Materialbeständen**,
2. **Schutz der Umwelt**,
3. **Werterhalt**.

Diese Dreiteilung ist für Reuse besonders nützlich, weil Wiederverwendung nicht nur als Abfallvermeidung, sondern als Werterhalt und Ressourcenschutz verstanden wird.

### Passports for the Construction Sector

Der Pass-Leitfaden beschreibt, wie Informationen über Produkte, Elemente, Gebäude oder Infrastrukturen strukturiert werden können. Für digitale Reuse-Tools ist dies relevant, weil Passdaten typischerweise Grundlage für spätere Wiederverwendung sind:

- Was ist das Objekt?
- Wo ist es eingebaut?
- Woraus besteht es?
- Welche Leistung und Qualität hat es?
- Wie kann es demontiert werden?
- Welche Nutzung ist nach Lebensende möglich?

### Einsatz in digitalen Werkzeugen

Platform-CB’23-Methoden können genutzt werden, um:

- Datenfelder für Materialpässe zu strukturieren,
- Circularity Scores transparenter zu machen,
- Beschaffungskriterien für wiederverwendete Bauteile zu formulieren,
- Reuse- und Recycling-Szenarien zu unterscheiden,
- Datenmodelle an gemeinsame Definitionen zu koppeln.

### Abgrenzung

Platform CB’23 ist kein Marktplatz, keine BIM-Software und kein Materialpassanbieter. Die Relevanz liegt in der **Standardisierung von Sprache, Kriterien und Bewertungslogik**.

## Praxisbezug / Beispiele

- **Niederländischer Kontext:** Die Niederlande sind im Bereich zirkuläres Bauen methodisch weit entwickelt. CB’23 bietet eine gute Referenz für Forschungsarbeiten, die Reuse nicht nur projektbezogen, sondern systemisch betrachten.
- **Materialpass-Workflows:** Ein eigenes Materialpass-Datenmodell kann sich an CB’23 orientieren, um kompatible Begriffe und Informationskategorien zu verwenden.
- **Ausschreibungen:** Zirkuläre Beschaffung kann auf CB’23-Begriffe zurückgreifen, z. B. für Anforderungen an Demontierbarkeit, Wiederverwendungsanteile oder Wertbeibehaltung.
- **Bewertungstools:** Urban Mining Index, One Click LCA oder eigene Scoring-Modelle können mit CB’23-Zielen verglichen werden.

## Herausforderungen / offene Fragen

- **Nationale Einbettung:** CB’23 stammt aus dem niederländischen Kontext; Übertragbarkeit auf Deutschland, Österreich oder Schweiz muss geprüft werden.
- **Leitfaden statt Norm:** Die Dokumente sind wichtige Vereinbarungsgrundlagen, aber nicht automatisch verbindliche Normen.
- **Operationalisierung:** Digitale Tools müssen Leitfadenbegriffe in konkrete Datenfelder, Pflichtangaben und Prüfroutinen übersetzen.
- **Bewertungsgewichtung:** Schutz von Materialbestand, Umwelt und Wert können im Einzelfall zu unterschiedlichen Entscheidungen führen.
- **Praxisdaten:** Einheitliche Definitionen lösen nicht automatisch das Problem unvollständiger Gebäudedaten.

## Quellen

- Platform CB’23: **English overview**. https://platformcb23.nl/english/. Zugriff: 2026-04-27.
- Platform CB’23: **Guide Measuring Circularity**. https://platformcb23.nl/wp-content/uploads/PlatformCB23_Guide_Measuring-Circularity.pdf. Zugriff: 2026-04-27.
- Platform CB’23: **Guide Passports for the Construction Sector**. https://platformcb23.nl/wp-content/uploads/PlatformCB23_Guide_Passports-for-the-construction-sector.pdf. Zugriff: 2026-04-27.
- FEHRL: **Rijkswaterstaat is member of the Dutch Platform CB’23**, 05.03.2021. https://www.fehrl.org/news/rws-is-member-of-the-dutch-platform-cb23-circular-construction-in-2023. Zugriff: 2026-04-27.
- One Planet Network: **Passports for the Construction Sector**. https://www.oneplanetnetwork.org/sites/default/files/from-crm/231-bdc862c090000e0a40350180c0b12b4e_Platform_CB23_Guide_Passports_for_the_construction_sector_2.0.pdf. Zugriff: 2026-04-27.
