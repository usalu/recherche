---
type: Werkzeug
---

## Verknüpfungen

- **Übergeordnete Themen:** parametrische Planung; Geometrie; digitale Entwurfswerkzeuge; Bestandserfassung; Bauteilvarianten; Design for Disassembly; Schnittstellen.
- **Verwandte Dateien:** `werkzeug/BIM.md`; `werkzeug/IFC_Viewer.md`; `werkzeug/Materialdatenbank.md`; `datenmodell/IFC.md`; `methode/Entwerfen_mit_verfuegbaren_Bauteilen.md`; `methode/Parametrische_Planung.md`; `methode/Bauteilkatalogisierung.md`; `logistik/Zuschnitt_Anpassung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Robert McNeel & Associates; Rhino 3D; Grasshopper; Rhino.Inside.Revit; VisualARQ; Speckle; COMPAS; Karamba3D; Scan-to-Model; parametrische Bauteilpassung; Wiederverwendung von Stahl, Holz, Fassadenelementen, Fenstern, Platten und Innenausbau.

## Kurzdefinition

Rhino, vollständig Rhinoceros 3D, ist eine 3D-Modellierungssoftware von Robert McNeel & Associates. Sie ist besonders stark in freier Geometrie, NURBS-Modellierung, Flächen, Kurven, SubD-Modellierung und Schnittstellen. In der Architektur wird Rhino häufig zusammen mit Grasshopper genutzt, einer visuellen Programmierumgebung für parametrische und algorithmische Entwurfsprozesse.

Für Wiederverwendung ist Rhino kein Materialpass- oder Marktplatzsystem. Es ist ein **geometrisches und parametrisches Entwurfswerkzeug**, das besonders nützlich ist, wenn Entwürfe an vorhandene, unregelmäßige oder chargenabhängige Bauteile angepasst werden müssen.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung kehrt die übliche Logik der Planung teilweise um: Nicht jedes Bauteil wird neu nach Wunschmaß bestellt; oft müssen vorhandene Bauteile mit realen Maßen, Toleranzen, Zuständen und Stückzahlen in ein neues Entwurfssystem integriert werden. Rhino und Grasshopper können diese Anpassungs- und Variantenprozesse unterstützen.

Relevanz:

- Modellierung und Analyse vorhandener Bauteile und Geometrien.
- Parametrische Anpassung von Entwürfen an verfügbare Bauteile.
- Optimierung von Zuschnitt, Rasterung, Sortierung und Wiederverwendungsmustern.
- Integration von Scan-, Punktwolken- oder Vermessungsdaten.
- Geometrische Vorprüfung von Re-Use-Elementen, z. B. Fassadenpaneele, Träger, Platten, Fenster.
- Verbindung mit BIM-Workflows über Rhino.Inside.Revit, IFC-Plugins, VisualARQ oder Speckle.
- Entwicklung von Entwurfsstrategien für variable Materialverfügbarkeit.

## Fachinhalt

### Funktionsweise

Rhino arbeitet objekt- und geometriebasiert mit:

- Kurven, Flächen, Volumenkörpern, Meshes, SubD-Geometrien.
- präzisen Modellierungs- und Analysewerkzeugen.
- Layern, Blöcken, Gruppen und Attributen.
- Import/Export zahlreicher CAD-, Mesh-, Bild- und Datenformate.
- Grasshopper für parametrische Definitionen, Datenbäume, Listenoperationen und algorithmische Geometrie.
- Erweiterungen für BIM, Tragwerk, Optimierung, Simulation, Fertigung und Datenübergabe.

### Rhino im Re-Use-Workflow

#### 1. Bauteile erfassen

Vorhandene Bauteile können als Geometrieobjekte modelliert oder aus Vermessung, Scan, Fotos, CAD-Plänen oder Tabellen erzeugt werden. Beispiele:

- Stahlträger mit Profil, Länge, Bohrungen.
- Holzlamellen mit Querschnitt, Länge, Krümmung.
- Fassadenpaneele mit Maßen und Befestigungspunkten.
- Natursteinplatten mit Dicke, Kantenqualität und Schadstellen.
- Fenster mit Rahmenmaß, Öffnungsrichtung und Glaspaket.
- Ziegel oder Fliesen als Chargen mit Stückzahl und Maßtoleranz.

#### 2. Entwurf anpassen

Grasshopper kann Entwurfssysteme an vorhandene Bauteile anpassen:

- Raster aus verfügbaren Elementmaßen ableiten.
- Bauteile nach Länge, Zustand oder Material sortieren.
- Schnittverlust minimieren.
- Paneele auf Fassadenflächen verteilen.
- Öffnungen an vorhandene Fenstergrößen anpassen.
- Bauteile nach Tragfähigkeit oder Restlänge clustern.
- Varianten nach Materialausnutzung, Verschnitt, Transport oder CO₂ vergleichen.

#### 3. Daten anreichern

Rhino-Objekte können Attribute oder User Text erhalten. In Grasshopper können Tabellen mit Bauteildaten eingelesen werden. Diese Daten sind aber nicht automatisch normiert oder BIM-konform. Für robuste Nutzung müssen Felder und IDs sorgfältig definiert werden.

Mögliche Attribute:

- Bauteil-ID.
- Herkunftsgebäude.
- Material.
- Maße.
- Zustand.
- Gewicht.
- Verfügbarkeit.
- Prüfstatus.
- Einbauposition.
- Schnitt- oder Bearbeitungsbedarf.

#### 4. Übergabe

Rhino kann Daten an andere Systeme übergeben:

- Geometrieexport: DWG, DXF, OBJ, STL, STEP, 3DM.
- BIM-Übergabe: über VisualARQ, Rhino.Inside.Revit, IFC-Workflows oder Speckle.
- Tabellenexport: CSV/Excel über Grasshopper-Skripte.
- Fertigung: CNC-, Laser-, Zuschnitt- oder Roboterpfade über entsprechende Plugins.
- Visualisierung: Renderings, Diagramme, Explosionszeichnungen.

### Relevante Erweiterungen

- **Grasshopper:** visuelle Programmierung; zentral für parametrische Re-Use-Logik.
- **Rhino.Inside.Revit:** Rhino/Grasshopper innerhalb von Revit; verbindet parametrische Geometrie mit BIM-Modellen.
- **VisualARQ:** BIM-orientierte Architekturmodellierung in Rhino, einschließlich IFC-Import/Export.
- **Speckle:** offene Datenplattform für AEC-Datenübertragung zwischen Rhino, Revit, Grasshopper und weiteren Tools.
- **Karamba3D:** Tragwerksanalyse in Grasshopper; nützlich für frühe Varianten, ersetzt aber keine prüffähige Statik.
- **COMPAS:** computational framework für Architektur, Struktur und digitale Fertigung.
- **Ladybug Tools:** Umweltanalysen; indirekt relevant für Bauteilstrategien und Entwurfsvarianten.

### Nutzen

- Sehr flexibel bei unregelmäßigen, vorhandenen oder variierenden Bauteilen.
- Gut geeignet für iterative Entwurfsvarianten.
- Grasshopper ermöglicht regelbasierte Wiederverwendungsstrategien.
- Stark in Geometrie, Visualisierung und digitaler Fertigung.
- Kann zwischen Scan, Entwurf, Fertigung und BIM vermitteln.
- Unterstützt Design for Disassembly, wenn Verbindungs- und Schichtenlogik geometrisch entwickelt wird.

### Grenzen

- Rhino ist von sich aus kein normiertes BIM-Informationsmodell.
- Objektattribute sind weniger streng als IFC- oder Revit-Parameter.
- Datenqualität hängt stark von individueller Modellierungsdisziplin ab.
- Material-, Zustands-, LCA- und Nachweisdaten müssen extern gepflegt werden.
- IFC-Übergaben können komplex und verlustbehaftet sein.
- Parametrische Skripte sind oft personengebunden und schwer wartbar.
- Für Ausschreibung, Genehmigung und Gebäudebetrieb sind zusätzliche BIM-/Dokumentationsprozesse nötig.

## Praxisbezug / Beispiele

- **Fassade aus wiederverwendeten Paneelen:** Vorhandene Paneele mit unterschiedlichen Maßen werden in Grasshopper katalogisiert und auf eine neue Fassadenfläche verteilt. Algorithmus minimiert Zuschnitt und ordnet beschädigte Paneele weniger sichtbaren Bereichen zu.
- **Holztragwerk aus Rückbauholz:** Längen, Querschnitte und Qualitäten werden tabellarisch eingelesen. Grasshopper entwickelt Raster und Zuschnittvarianten; statische Prüfung erfolgt separat.
- **Natursteinboden:** Platten werden nach Maß und Zustand sortiert; Verlegeplan minimiert Zuschnitt und berücksichtigt Randzonen.
- **Fenster-Re-Use:** Entwurf von Öffnungen orientiert sich an verfügbaren Fenstermaßen. Rhino unterstützt Varianten der Fassadengliederung.
- **Bauteilpassung in Bestand:** Punktwolken oder Messdaten werden genutzt, um neue wiederverwendete Bauteile an unregelmäßige Bestandsgeometrien anzupassen.
- **Design for Disassembly:** Verbindungspunkte, Schraubrichtungen und Montagefolgen werden geometrisch simuliert und als Explosionszeichnungen dokumentiert.

## Herausforderungen / offene Fragen

- Wie werden Rhino-/Grasshopper-Objekte stabil mit Bauteil-IDs, Materialpässen und Plattformdaten verknüpft?
- Wie lassen sich parametrische Re-Use-Entwürfe nachvollziehbar dokumentieren, wenn Skripte projektindividuell sind?
- Wie kann IFC-Export mit Re-Use-spezifischen Properties robust gelöst werden?
- Wie werden Unsicherheiten aus Bestandsaufnahme, Toleranzen und Zustand in Varianten berücksichtigt?
- Welche Schnittstellen eignen sich für Rückkopplung zwischen Marktplattformen und Entwurfsmodellen?
- Wie können Planende vermeiden, dass geometrische Optimierung rechtliche, technische oder logistische Risiken überdeckt?
- Wie werden Rhino-basierte Re-Use-Prozesse in Ausschreibung und Ausführung übersetzt?

## Quellen

- Rhino 3D: Official website and product information, https://www.rhino3d.com/
- McNeel: Grasshopper, https://www.rhino3d.com/features/grasshopper/
- Rhino Developer / Rhino.Inside.Revit Guides, https://developer.rhino3d.com/guides/rhinocommon/rhino-inside/
- VisualARQ: BIM for Rhino, IFC workflows, https://www.visualarq.com/
- Speckle: open-source AEC data platform, https://speckle.systems/
- Karamba3D: parametric structural engineering for Grasshopper, https://www.karamba3d.com/
- COMPAS Framework, https://compas.dev/
- buildingSMART: IFC/openBIM standards, https://www.buildingsmart.org/
- McNeel Forum and documentation: Rhino / Grasshopper workflows, https://discourse.mcneel.com/
