---
type: Werkzeug
---

## Verknüpfungen

- **Übergeordnete Themen:** OpenBIM, IFC-native Modellierung, offene Planungswerkzeuge, Datenhoheit, digitale Bestandsmodelle, Materialpass-Authoring.
- **Verwandte Dateien:** `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/IfcOpenShell.md`, `werkzeug/Speckle.md`, `werkzeug/Rhino.md`, `datenmodell/IFC.md`, `datenmodell/Materialpass.md`, `methode/Bestandsmodellierung.md`, `methode/Design_for_Disassembly.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Bonsai, BlenderBIM, Blender, IfcOpenShell, buildingSMART, IFC2x3, IFC4, IFC4x3, Open Source AEC, OpenBIM, native IFC authoring.

## Kurzdefinition

**Bonsai** – früher stark mit **BlenderBIM** verbunden – ist ein freies, quelloffenes OpenBIM-Add-on für Blender. Es wird als native IFC-Autorensoftware beschrieben: IFC ist nicht nur Exportformat, sondern Arbeits- und Datenmodell. Bonsai basiert eng auf IfcOpenShell und ermöglicht Modellierung, Prüfung, Mengenermittlung und weitere BIM-nahe Workflows in einer offenen Umgebung.

Für Wiederverwendung ist Bonsai vor allem relevant, weil es **offene, langfristig zugängliche Bestands- und Bauteildaten** unterstützt.

## Relevanz für Wiederverwendung im Bauwesen

Reuse-Projekte brauchen robuste digitale Daten, die nicht nur kurzfristig in proprietären Projektdateien existieren. Wenn wiederverwendbare Bauteile in einem offenen IFC-Modell beschrieben werden, können sie später besser ausgewertet, geprüft, ergänzt und übertragen werden.

Bonsai ist reuse-relevant, weil es:

- IFC nativ bearbeiten kann,
- Open-Source-Workflows für Forschung und Praxis ermöglicht,
- Bauteile mit Geometrie und Eigenschaften zusammenführt,
- Materialpass-Attribute modellnah ergänzbar macht,
- Bestandsmodelle ohne proprietäre Lizenzbarrieren zugänglich macht,
- mit IfcOpenShell und Python-Workflows kombinierbar ist.

Es ist jedoch **kein fertiges Reuse-Tool**: Reuse-Logik, Datenfelder und Bewertungsmethoden müssen projektspezifisch ergänzt werden.

## Fachinhalt

### Funktionsweise

Bonsai läuft als Add-on in Blender. Die Software nutzt IFC als Datenstruktur und erlaubt u. a.:

- IFC-Modelle zu erstellen und zu bearbeiten,
- Bauteile zu klassifizieren,
- Eigenschaften und Property Sets zu verwalten,
- Geometrie und semantische Daten gemeinsam zu bearbeiten,
- Zeichnungen, Mengen, Termin- oder Kosteninformationen in OpenBIM-Kontexten zu nutzen,
- Modelle zu prüfen und zu koordinieren.

Die eigentliche Stärke für Reuse liegt darin, dass **Bauteile als semantische Objekte** und nicht nur als Meshes oder CAD-Linien modelliert werden können.

### Reuse-relevante Datentypen

- IFC-Objektklasse, z. B. `IfcDoor`, `IfcWindow`, `IfcBeam`, `IfcSlab`, `IfcCovering`.
- Material- und Schichtaufbauten.
- Mengen: Länge, Fläche, Volumen, Masse.
- Lage: Gebäude, Geschoss, Raum, Bauteilgruppe.
- Property Sets: Zustand, Rückbaubarkeit, Wiederverwendungsstatus, Schadstoffverdacht, Prüfbedarf.
- Referenzen: Fotos, Scans, Datenblätter, EPDs, Materialpass-IDs.

### Einsatzszenarien

- **Bestandsmodellierung:** Aufnahme vorhandener Gebäude oder Bauteile als IFC-Modell.
- **Bauteilkataloge:** Modellierung wiederverwendbarer Komponenten mit Geometrie und Eigenschaften.
- **Materialpass-Erstellung:** Ergänzen von Eigenschaften, die später in Tabellen, Pässe oder Auswertungen exportiert werden.
- **Entwurf mit vorhandenen Komponenten:** Reuse-Bauteile als echte BIM-Objekte in Varianten testen.
- **Forschung / Lehre:** Entwicklung eigener OpenBIM-Reuse-Workflows ohne proprietäre Software.

### Schnittstellen

- **IfcOpenShell:** technische Grundlage für IFC-Verarbeitung, Skripting und Automatisierung.
- **IFC:** Austauschformat für OpenBIM-Prozesse.
- **Blender:** Geometrische Bearbeitung, Visualisierung, Modellierung.
- **Speckle / Python / Tabellen:** mögliche Auswertung und Weitergabe von Daten.
- **Materialpasssysteme:** Bonsai kann Daten vorbereiten, ersetzt aber keine Passplattform.

## Praxisbezug / Beispiele

- **IFC-natives Bestandsmodell:** Ein Rückbauobjekt kann als IFC-Modell aufgebaut werden, in dem Türen, Trennwände, Leuchten, Stahlprofile oder Fassadenelemente als eigene Objekte mit Mengen und Zustand erfasst werden.
- **Open-Source-Forschung:** Universitäten und Reallabore können eigene Reuse-Attribute definieren und über IfcOpenShell auswerten, ohne von geschlossenen Datenmodellen abhängig zu sein.
- **Bauteilbibliothek:** Wiederverwendbare Komponenten können mit standardisierten Eigenschaften modelliert und in neuen Entwürfen eingesetzt werden.

## Herausforderungen / offene Fragen

- **Lernkurve:** Blender und IFC-native Modellierung sind für viele Planungsbüros ungewohnt.
- **Modellieraufwand:** Für Reuse müssen Objekte präziser getrennt und beschrieben werden als in vielen üblichen BIM-Modellen.
- **Eigenschaftsstandard:** Es fehlt häufig ein allgemein akzeptiertes Property-Set für Wiederverwendung.
- **Prüf- und Haftungsdaten:** Technische Eignung, Brandschutz, Statik und Schadstofffreiheit müssen außerhalb der Modellierung abgesichert werden.
- **Kompatibilität:** Obwohl IFC offen ist, unterscheiden sich Softwareinterpretationen; Tests mit Zielsystemen bleiben notwendig.

## Quellen

- Bonsai: **Official website**. https://bonsaibim.org/. Zugriff: 2026-04-27.
- Blender Extensions: **Bonsai add-on**. https://extensions.blender.org/add-ons/bonsai/. Zugriff: 2026-04-27.
- Open Source Construction: **Bonsai project profile**. https://opensource.construction/projects/bonsai/. Zugriff: 2026-04-27.
- IfcOpenShell: **Open source IFC toolkit and geometry engine**. https://ifcopenshell.org/. Zugriff: 2026-04-27.
- Tim McGinley: **Bonsai / BlenderBIM course documentation**. https://timmcginley.github.io/41934/Concepts/Bonsai/index.html. Zugriff: 2026-04-27.
