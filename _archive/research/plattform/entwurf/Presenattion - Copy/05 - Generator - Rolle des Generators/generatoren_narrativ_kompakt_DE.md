# Generatoren im Vorplanungssystem  
## Kompakte narrative Erklärung

## 1. Die Grundidee

Ein Generator ist die Übersetzungsschicht zwischen einem realen wiederverwendeten Bauteil und dem digitalen Entwurfssystem.

Ein Bauteil aus dem Katalog ist zunächst nur ein reales Objekt mit Daten: Geometrie, Maße, Masse, Material, Zustand und vielleicht einigen Nachweisen. Damit kann der User das Bauteil zwar sehen, aber das System weiß noch nicht automatisch, **wie** dieses Bauteil entwerferisch benutzt werden kann.

Der Generator macht genau diese Übersetzung.

```text
Bauteilpass / Bauteilkatalog
↓
Generator
↓
entwurfsfähiges Systemobjekt
```

Er erzeugt aus einem Bauteil nicht den finalen Nachweis, sondern eine nutzbare Vorplanungs-Abstraktion.

---

## 2. Warum braucht man Generatoren?

Ohne Generatoren müsste jedes Bauteil manuell interpretiert werden.

Bei einer Deckenplatte müsste jemand jedes Mal entscheiden:

```text
Welche Kanten können Auflager sein?
Welche Kante ist für ein Raster interessant?
Wo kann die Platte an ein anderes Bauteil andocken?
Ist eine Öffnung relevant?
Wo entstehen Warnungen?
Welche Nachweise fehlen später?
```

Bei vielen wiederverwendeten Bauteilen wäre das zu langsam, zu unübersichtlich und nicht skalierbar.

Der Generator automatisiert diese erste Interpretation. Er erkennt aus Typologie und Geometrie, welche vereinfachten Repräsentationen und Andockpunkte sinnvoll sind.

---

## 3. Was macht ein Generator?

Ein Generator nimmt ein reales Bauteil und erzeugt daraus die minimalen Objekte, die das System in der Vorplanung braucht.

Er erzeugt:

```text
vereinfachte Repräsentationen
Host-Geometrien
SharedConnectorPoints
Facets
Ports
Vorplanungswarnungen
fehlende Nachweise
```

Beispiel Deckenplatte:

```text
reale Deckenplatte
↓
Generator
↓
PlateElement2D
SupportPatch2D an relevanten Kanten
SharedConnectorPoints an wenigen strategischen Stellen
StructuralFacet mit bearing_side
SemanticFacet mit Elementname + Sitz des Connectors
LogisticsFacet für Lagerung / Heben
```

Der Generator sagt damit nicht: „Diese Verbindung ist bewiesen.“  
Er sagt: „Diese Stellen sind sinnvoll, um in der Vorplanung damit zu entwerfen und später zu prüfen.“

---

## 4. Was ist der Unterschied zwischen Generator und Checker?

Der Generator erzeugt Möglichkeiten.  
Der Checker bewertet konkrete Verbindungen.

```text
Generator:
Welche Punkte, Ports und Repräsentationen sind für dieses Bauteil sinnvoll?

Checker:
Funktioniert diese konkrete Verbindung zwischen Punkt A und Punkt B?
```

Beispiel:

```text
Generator:
Diese Plattenkante bekommt einen SharedConnectorPoint mit bearing_side.

Checker:
Wenn dieser Punkt an einen Wandkopf andockt, ist das Auflager grob plausibel oder kritisch?
```

Der Generator bereitet also die Prüfung vor.  
Der Checker führt die Prüfung aus.

---

## 5. Was erzeugt der Generator im Detail?

Der Generator erzeugt vier zentrale Dinge.

### 5.1 Repräsentationen

Eine Repräsentation ist eine vereinfachte fachliche Sicht auf das Bauteil.

Beispiele:

```text
Deckenplatte → PlateElement2D
Träger → LineElement1D
Stütze → LineElement1D
Hohlkammerdecke → einachsig spannende Platte
Fragment → Graph aus Platte, Trägerlinie, Stützenlinie und Transferknoten
```

### 5.2 Host-Geometrien

Host-Geometrien sind die Geometrien, die später für Checks verwendet werden.

Beispiele:

```text
SupportPatch2D
AlignmentLine
BridgeZone
OpeningLoop
RouteLine
LiftingZone
StorageSupportZone
```

Der Connector selbst bleibt immer ein Punkt.  
Die Host-Geometrie ist das, was fachlich geprüft wird.

### 5.3 SharedConnectorPoints

SharedConnectorPoints sind wenige strategische Punkte am Bauteil.

Sie sind die sichtbaren Andockpunkte im Interface.

Beispiel:

```text
slab_edge_A_midpoint
hcs_end_A_midpoint
fragment_transfer_node
fragment_cut_face_point
```

Ein SharedConnectorPoint kann mehrere Bedeutungen tragen.

### 5.4 Facets und Ports

Ein Facet beschreibt, warum ein Punkt für ein bestimmtes Paket relevant ist.

Ein Port beschreibt, womit dieser Punkt kompatibel ist.

Beispiel:

```text
slab_edge_A_midpoint

StructuralFacet:
port = bearing_side

SemanticFacet:
element_name = Deckenplatte
connector_sits_on = lange Plattenkante A

EnergyFacet:
port = bridge_side, nur wenn Hülle relevant

LogisticsFacet:
port = access_port, wenn Montagezugang geprüft wird
```

---

## 6. Wie arbeitet ein Generator?

Der Ablauf ist immer ähnlich.

```text
1. Bauteildaten lesen
2. Typologie erkennen
3. Basisgeometrie analysieren
4. vereinfachte Repräsentationen erzeugen
5. Host-Geometrien ableiten
6. Kandidatenpunkte setzen
7. Facets und Ports zuweisen
8. doppelte Punkte zusammenführen
9. unnötige Punkte löschen
10. Vorplanungsstatus ausgeben
```

Das Ziel ist nicht, möglichst viele Informationen zu erzeugen.  
Das Ziel ist, die **richtigen wenigen Punkte** zu erzeugen.

---

## 7. Beispiel: Deckenplatte

Input:

```text
Deckenplatte
Maße
Masse
Geometrie
Material
```

Generatoroutput:

```text
PlateElement2D
lange Kanten als mögliche Auflagerbereiche
SupportPatch2D an Kanten
AlignmentLine an Kanten
TransportEnvelope
StorageSupportZone
SharedConnectorPoints:
- slab_edge_A_midpoint
- slab_edge_B_midpoint
- slab_lifting_reference
- slab_storage_reference
```

Semantisch wird in der Vorplanung nur einfach beschrieben:

```text
Elementname: Deckenplatte
Connector sitzt auf: lange Plattenkante A
```

Das reicht, um Bauteile zu matchen und Ports sinnvoll zu verbinden.

---

## 8. Beispiel: Hohlkammerdecke

Input:

```text
Hohlkammerdecke
Stirnseiten
Längsfugen
Hohlräume
Transport- oder Trackingstatus
```

Generatoroutput:

```text
einachsig spannende Platte
SupportPatch2D an beiden Stirnseiten
JointLine an Längsfuge
optional RouteLine im Hohlraum
SharedConnectorPoints:
- hcs_end_A_midpoint
- hcs_end_B_midpoint
- hcs_long_joint_midpoint
- hcs_void_route_point, nur wenn Route relevant
- hcs_lifting_reference
```

Semantisch:

```text
Elementname: Hohlkammerdecke
Connector sitzt auf: Stirnauflager A
```

---

## 9. Beispiel: SlabBeamColumnFragment

Input:

```text
monolithisches Fragment
Plattenbereich
Trägerbereich
Stützenabschnitt
Schnittflächen
```

Generatoroutput:

```text
StructuralGraph
PlateElement2D
LineElement1D für Träger
LineElement1D für Stütze
TransferNode
ContinuityZone an Schnittfläche
SharedConnectorPoints:
- fragment_transfer_node
- fragment_cut_face_point
- fragment_plate_edge_point
- fragment_column_base_or_head_point
- fragment_lifting_reference
```

Semantisch:

```text
Elementname: SlabBeamColumnFragment
Connector sitzt auf: Transferknoten
```

oder:

```text
Elementname: SlabBeamColumnFragment
Connector sitzt auf: Schnittfläche
```

---

## 10. Wofür ist der Generator in der Vorplanung da?

Der Generator macht Bauteile schnell entwerfbar.

Er hilft bei:

```text
Bauteile auswählen
Bauteile platzieren
Andockpunkte finden
Ports matchen
grobe Verbindungsideen prüfen
Risiken früh erkennen
fehlende Nachweise markieren
```

Er hält das Interface einfach, weil nicht jede Fläche und jede Kante als Connector erscheint. Stattdessen zeigt das System wenige strategische Punkte mit klaren Bedeutungen.

---

## 11. Was erzeugt der Generator nicht?

Der Generator erzeugt keine finalen Nachweise.

Er erzeugt nicht:

```text
finale Statik
Ankerbemessung
Ausführungsdetails
finalen U-Wert
Brandschutznachweis
finale TGA-Planung
Hebeplan
Genehmigungsfähigkeit
```

Diese Dinge kommen später.

In der Vorplanung erzeugt der Generator nur:

```text
Plausibilität
Warnungen
Kontextbedarf
Nachweisbedarf
Matching-Logik
```

---

## 12. Die wichtigste Systemformel

```text
Bauteilpass
+ Typologie
+ Geometrie
+ Kontext
↓
Generator
↓
Repräsentationen
+ Host-Geometrien
+ SharedConnectorPoints
+ Facets
+ Ports
+ Vorplanungsstatus
↓
Checker
↓
Connection Passport
```

---

## 13. Ein-Satz-Erklärung

Ein Generator ist die typologiebasierte Übersetzungslogik, die ein reales wiederverwendetes Bauteil in wenige, klare und prüfbare Vorplanungsobjekte verwandelt.

---

## 14. Noch kürzer

```text
Generatoren machen aus Bauteilen entwurfsfähige Systemobjekte.
```
