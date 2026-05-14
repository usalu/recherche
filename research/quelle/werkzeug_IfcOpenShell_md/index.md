---
entity: "quelle"
id: "werkzeug_IfcOpenShell_md"
title: "werkzeug_IfcOpenShell_md"
build_status: "promoted_phase42"
source_filename: "IfcOpenShell.md"
legacy_type: "Werkzeug"
---

# werkzeug_IfcOpenShell_md

## Verknüpfungen

- **Übergeordnete Themen:** IFC-Verarbeitung, OpenBIM, Automatisierung, Datenextraktion, Geometrieauswertung, Materialpass-Datenpipelines.
- **Verwandte Dateien:** `werkzeug/BIM.md`, `werkzeug/IFC_Viewer.md`, `werkzeug/Bonsai_BlenderBIM.md`, `werkzeug/Speckle.md`, `datenmodell/IFC.md`, `datenmodell/Property_Sets.md`, `datenmodell/Materialpass.md`, `methode/Mengenermittlung.md`, `methode/Bauteilkartierung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** IfcOpenShell, buildingSMART, IFC2x3, IFC4, IFC4x3, OpenCASCADE, IfcConvert, IfcPatch, Python, BIM-Poweruser, Forschungsworkflows.

## Kurzdefinition

**IfcOpenShell** ist ein quelloffenes Toolkit und eine Geometrie-Engine für IFC. Es ermöglicht, Building Information Models im IFC-Format zu lesen, zu schreiben, zu verändern und geometrisch auszuwerten. Es richtet sich sowohl an Softwareentwickler als auch an BIM-Poweruser.

Für Wiederverwendung ist IfcOpenShell kein Endnutzer-Marktplatz, sondern ein **technischer Baustein**, mit dem IFC-Daten für Materialinventare, Materialpässe, Mengenermittlung und Reuse-Analysen nutzbar gemacht werden können.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung braucht maschinenlesbare Informationen über Bauteile: Was ist vorhanden? Wo ist es? Woraus besteht es? Welche Mengen, Maße und Eigenschaften hat es? IFC kann diese Informationen enthalten, aber sie müssen extrahiert, geprüft und ergänzt werden. Genau hier ist IfcOpenShell relevant.

IfcOpenShell unterstützt Wiederverwendung durch:

- automatisierte Auswertung von IFC-Modellen,
- Ermittlung von Mengen, Flächen, Volumen und Bauteillisten,
- Zugriff auf Property Sets und Klassifikationen,
- Ergänzung eigener Reuse-Attribute,
- Modellbereinigung und Datenvalidierung,
- Verknüpfung von Geometrie und Materialpassdaten.

Damit kann IfcOpenShell die technische Grundlage für eigene Reuse-Tools bilden.

## Fachinhalt

### Kernfunktionen

IfcOpenShell bietet u. a.:

- Parsing von IFC-Dateien,
- Lesen und Schreiben von IFC-Schemas,
- Geometrieerzeugung aus IFC-Objekten,
- Python- und C++-Schnittstellen,
- Konvertierung von IFC-Geometrie,
- Modellmanipulation und Patch-Workflows,
- Zugriff auf Beziehungen, Mengen, Property Sets und Klassifikationen.

Die Projektseite beschreibt IfcOpenShell als Toolkit, um digitale Plattformen für die gebaute Umwelt zu entwickeln.

### Reuse-relevante Operationen

Für ein Forschungsrepo zur Wiederverwendung sind besonders folgende Operationen relevant:

- **Objektfilterung:** z. B. alle Türen, Fenster, Träger, Fassadenelemente oder Deckenplatten extrahieren.
- **Mengenermittlung:** Längen, Flächen, Volumen, Stückzahlen und Massen auswerten.
- **Materialanalyse:** Materialzuweisungen und Schichtaufbauten lesen.
- **Property-Set-Auswertung:** Zustand, Demontierbarkeit, Wiederverwendungsstatus oder Prüfbedarf abfragen.
- **Datenanreicherung:** eigene Attribute in IFC schreiben oder externe Tabellen mit IFC-GUIDs verknüpfen.
- **Qualitätskontrolle:** fehlende Klassifikationen, doppelte Objekte, unplausible Mengen oder nicht zugewiesene Materialien erkennen.

### Typische Datenpipeline

1. IFC-Modell laden.
2. Relevante Bauteilklassen auswählen.
3. Mengen und Eigenschaften extrahieren.
4. Daten mit Fotos, Audits, Schadstoffprüfungen oder Materialpässen verbinden.
5. Ergebnis als CSV, JSON, Datenbank oder Passdatensatz exportieren.
6. Optional: Reuse-Attribute zurück ins IFC-Modell schreiben.

### Abgrenzung

IfcOpenShell ist keine grafische BIM-Komplettlösung. Bonsai / BlenderBIM nutzt IfcOpenShell als Grundlage für eine Benutzeroberfläche. IfcOpenShell selbst ist eher Bibliothek, Toolkit und Automatisierungsumgebung.

## Praxisbezug / Beispiele

- **Automatische Bauteilliste:** Aus einem Bestands-IFC werden alle `IfcDoor`-Objekte mit Abmessungen, Material, Geschoss und GUID exportiert. Diese Liste dient als Grundlage für einen Reuse-Katalog.
- **Materialpass-Befüllung:** IFC-Mengen werden mit Ökobilanzdaten und Rückbauinformationen verknüpft, um Materialpassfelder vorzubefüllen.
- **Modellprüfung:** Ein Skript prüft, ob alle wiederverwendungsrelevanten Objekte über Materialangaben, Lage und eindeutige IDs verfügen.
- **Forschung zu Circular Design:** Eigene Indikatoren wie Demontierbarkeit, Sortenreinheit oder Wiederverwendungspotenzial können auf IFC-Objekte bezogen berechnet werden.

## Herausforderungen / offene Fragen

- **IFC-Datenqualität:** Viele IFC-Modelle enthalten unvollständige oder uneinheitliche Materialinformationen.
- **Geometrie vs. Semantik:** Geometrisch vorhandene Objekte sind nicht automatisch korrekt klassifiziert.
- **Bestand:** Für ältere Gebäude gibt es oft kein IFC-Modell; die Erstellung kann aufwendig sein.
- **Property-Set-Standardisierung:** Reuse-Attribute sind nicht einheitlich normiert.
- **Softwarekompetenz:** IfcOpenShell erfordert technisches Wissen, vor allem bei Python-/C++-Workflows.
- **Haftung:** Automatisierte Mengen und Eigenschaften müssen für Ausschreibung, Rückbau und Wiedereinbau geprüft werden.

## Quellen

- IfcOpenShell: **The open source IFC toolkit and geometry engine**. https://ifcopenshell.org/. Zugriff: 2026-04-27.
- IfcOpenShell Docs: **Introduction**. https://docs.ifcopenshell.org/introduction.html. Zugriff: 2026-04-27.
- IfcOpenShell: **Downloads – C++, Python and utilities**. https://ifcopenshell.org/downloads.html. Zugriff: 2026-04-27.
- GitHub: **IfcOpenShell repository**. https://github.com/IfcOpenShell/IfcOpenShell. Zugriff: 2026-04-27.
- OpenCascade: **IfcOpenShell project profile**. https://dev.opencascade.org/project/ifcopenshell. Zugriff: 2026-04-27.
