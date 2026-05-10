---
type: Werkzeug
datenmodell: ["[[datenmodell/IFC]]"]
verwandt: ["[[werkzeug/BIM]]", "[[werkzeug/Bonsai_BlenderBIM]]", "[[werkzeug/GIS_Urban_Mining]]", "[[werkzeug/IFC_Viewer]]", "[[werkzeug/IfcOpenShell]]", "[[werkzeug/Rhino]]", "[[werkzeug/Urban_Mining_Index]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Open Data, AEC-Datenplattform, BIM-Interoperabilität, Modell-zu-Datenbank-Workflows, Materialpass-Schnittstellen, digitale Planungskoordination.
- **Verwandte Dateien:** `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Rhino.md`, `werkzeug/IfcOpenShell.md`, `werkzeug/Bonsai_BlenderBIM.md`, `werkzeug/Urban_Mining_Index.md`, `datenmodell/IFC.md`, `datenmodell/Materialpass.md`, `methode/Bestandsmodellierung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Speckle Systems, Revit, Rhino, Grasshopper, Archicad, Blender/Bonsai, IFC, AEC Data Pipelines, API, Dashboarding, parametrische Bestandserfassung.

## Kurzdefinition

**Speckle** ist eine offene Datenplattform für Architektur, Ingenieurwesen und Bauwesen. Sie verbindet Modellierungs- und Planungswerkzeuge über Workspaces, Projekte, Konnektoren und Datenströme. Speckle ist nicht auf Wiederverwendung spezialisiert, kann aber als **Datenbrücke** zwischen CAD/BIM-Modellen, Analysewerkzeugen, Dashboards und Materialpass-Workflows dienen.

## Relevanz für Wiederverwendung im Bauwesen

Reuse-Projekte benötigen Daten, die zwischen sehr unterschiedlichen Werkzeugen wandern: Bestandsaufnahme, Rhino/Grasshopper, Revit, IFC, Tabellen, Materialpässe, Marktplätze, LCA, Logistik und Visualisierung. Speckle kann hier relevant sein, weil es AEC-Objekte als zugängliche Daten strukturiert und modellbasierte Informationen nicht nur in proprietären Dateien hält.

Für Wiederverwendung ist das besonders wichtig bei:

- digitalen Inventaren von Bestandsbauteilen,
- Geometrie- und Attributübergabe zwischen Rhino, Grasshopper und BIM,
- Variantenvergleich mit vorhandenen Bauteilen,
- projektübergreifenden Materialdatenflüssen,
- Dashboarding von Mengen, Verfügbarkeit, CO₂ und Wiederverwendungspotenzial.

Speckle ist damit ein **Reuse-Enabler**, kein Reuse-Marktplatz.

## Fachinhalt

### Grundprinzip

Speckle arbeitet mit Datenobjekten, die aus Planungsprogrammen gesendet, gespeichert, versioniert und in anderen Umgebungen empfangen werden können. Die Plattform organisiert Daten in Projekten und Workspaces und stellt Konnektoren zu gängigen AEC-Werkzeugen bereit.

Für Reuse ist entscheidend, dass Modellinformationen nicht als statischer Export enden, sondern weiterverarbeitbar bleiben:

- Objektattribute können ausgelesen und erweitert werden.
- Geometrien können in Analyseumgebungen übertragen werden.
- Modelle können in Webumgebungen sichtbar gemacht werden.
- Varianten und Versionen können dokumentiert werden.
- Daten können über APIs in eigene Workflows eingebunden werden.

### Datentypen

Reuse-relevante Daten in Speckle-Workflows können sein:

- Bauteilgeometrie,
- Objekt-ID und Klassifikation,
- Material- und Produkttyp,
- Maße, Mengen, Flächen, Volumen,
- Lage im Gebäude,
- Rückbau- oder Zustandsattribute,
- Wiederverwendungsstatus,
- CO₂- oder LCA-Kennwerte,
- Verknüpfungen zu Fotos, Prüfzeugnissen, Produktdatenblättern oder Materialpässen.

### Einsatzszenarien

- **Rhino/Grasshopper zu Revit / BIM:** Wiederverwendbare Bauteile können parametrisch sortiert, getestet und in Planungsmodelle übertragen werden.
- **Bestandsmodell zu Dashboard:** Bauteile aus einem Modell werden nach Material, Menge, Zustand oder Rückbaupotenzial ausgewertet.
- **Materialpass-Vorbereitung:** Objektlisten können als Grundlage für Materialpassdaten dienen, sofern Attribute korrekt ergänzt werden.
- **Reuse-Entwurf:** Entwurfsvarianten mit vorhandenen Bauteilen können datenbasiert verglichen werden.
- **Forschung:** Speckle eignet sich für prototypische Workflows, in denen Reuse-Logiken nicht in Standardsoftware vorhanden sind.

### Schnittstellen

Speckle steht zwischen:

- CAD/BIM-Autorensoftware,
- parametrischen Entwurfsumgebungen,
- Web- und Datenbankanwendungen,
- Python/JavaScript-Analysen,
- Materialpass- und Berichtssystemen,
- Visualisierungen und Dashboards.

## Praxisbezug / Beispiele

- **Reuse-Inventar aus Modellobjekten:** Ein Forschungsworkflow kann vorhandene Türen, Fassadenelemente oder Stahlprofile aus Rhino/Grasshopper modellieren, über Speckle bereitstellen und in einem Dashboard nach Abmessung, Zustand und Verfügbarkeit filtern.
- **BIM-Daten zugänglich machen:** Speckle beschreibt AEC-Daten als fragmentiert und positioniert sich als offene Dateninfrastruktur. Für Reuse ist gerade diese Entkopplung wichtig, weil Bauteildaten über Projektgrenzen hinweg nutzbar bleiben müssen.
- **Objekt als Datenzeile:** Speckle kommuniziert die Idee, dass Modellobjekte datenbankartig auswertbar werden können. Genau diese Logik ist für Materialpässe und Reuse-Inventare zentral.

## Herausforderungen / offene Fragen

- **Kein Reuse-Fachmodell:** Speckle liefert Infrastruktur, aber keine standardisierte Reuse-Taxonomie.
- **Attributdisziplin:** Ohne saubere Objektstruktur, Klassifikation und Materialattribute entstehen nur schöne, aber fachlich schwache Datenflüsse.
- **Langzeitarchivierung:** Für Materialpässe braucht es über Jahrzehnte stabile Datenhaltung; Projektplattformen müssen exportierbar und dokumentiert bleiben.
- **Haftung und Prüfungen:** Datenübertragung ersetzt nicht technische Eignungsprüfungen wiederzuverwendender Bauteile.
- **Interoperabilität mit IFC:** Speckle ist nicht dasselbe wie IFC. Für regulatorische und langfristige Austauschprozesse kann IFC weiterhin notwendig sein.

## Quellen

- Speckle Systems: **Welcome to Speckle Docs**, aktualisierte Dokumentation 2026. https://docs.speckle.systems/quickstart/welcome. Zugriff: 2026-04-27.
- Speckle Systems: **Website / open data infrastructure for AEC**. https://speckle.systems/. Zugriff: 2026-04-27.
- Speckle Guide: **Developer Docs / Introduction**. https://speckle.guide/. Zugriff: 2026-04-27.
- Speckle Systems: **Key platform principles**, 06.10.2025. https://speckle.systems/key-platform-principles/. Zugriff: 2026-04-27.
- Speckle Systems: **Putting data to work with Speckle**, 12.11.2025. https://speckle.systems/blog/realizing-aec-s-full-potential-putting-data-to-work-with-speckle/. Zugriff: 2026-04-27.
