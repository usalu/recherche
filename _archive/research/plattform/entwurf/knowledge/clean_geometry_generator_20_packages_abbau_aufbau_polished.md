# Punktbasierte Connector-Logik für alle Pakete  
## Angepasste Systemversion: Connectoren sind immer Punkte

**Zweck**  
Dieses Dokument passt die bisherige Paketstruktur an die neue Grundregel an:

```text
Connectoren sind immer Punkte.
```

Connectoren sind keine Linien, Flächen, Zonen oder Volumen.  
Sie sind **Punkt-Docking-Handles**, über die verschiedene abstrakte Repräsentationen miteinander andocken, damit das System Regeln, Checks und Berechnungen ausführen kann.

Die abstrakte Geometrie bleibt weiterhin paketabhängig:

```text
Tragwerk: Linie, Platte, Knoten, Auflagerfläche
Energie: Fläche, Schicht, Rand, Durchdringung
TGA: Route, Öffnung, Bohrkörper, Sperrzone
Semantik: Ausrichtungslinie, Sichtfläche, Zugangszone
Logistik: Transporthülle, Hebezone, Lagerauflager
Nachweis: Scanlinie, Schadensfläche, Prüfpunkt
```

Aber:

```text
Der Connector selbst ist immer ein Punkt.
```

---

# 1. Was ändert sich durch punktbasierte Connectoren?

## 1.1 Vorherige Logik

Bisher konnten Connectoren selbst als Zonen, Linien, Flächen oder Patches gedacht werden:

```text
bearing_support = Auflagerstreifen
alignment_handle = Fugenlinie
opening_use = Öffnungsrand
storage_handle = Lagerauflagerzone
```

Das war unscharf, weil Connector und Prüfgeometrie vermischt wurden.

## 1.2 Neue Logik

Jetzt gilt:

```text
Connector = Punkt
Host-Geometrie = Linie / Fläche / Zone / Volumen
Regel = nutzt den Punkt zum Andocken und die Host-Geometrie zum Prüfen
```

Beispiel:

```text
Auflager einer Deckenplatte

Connector:
ein Punkt auf der Auflagerkante

Host-Geometrie:
SupportPatch2D / Auflagerstreifen

Port:
bearing_side

Regel:
prüft nicht nur den Punkt,
sondern die referenzierte SupportPatch2D-Geometrie.
```

## 1.3 Warum ist das besser?

Punkt-Connectoren sind sehr sauber, weil sie drei Dinge trennen:

```text
1. Wo dockt etwas an?
   → ConnectorPoint

2. Was bedeutet das Andocken?
   → Port

3. Welche Geometrie wird geprüft?
   → Host-Geometrie der Repräsentation
```

Dadurch können unterschiedliche Repräsentationen miteinander verbunden werden, ohne dass ihre Geometrieformen gleich sein müssen.

Beispiel:

```text
Structural PlateElement2D
dockt über ConnectorPoint
an
Structural WallPanel2D

Der Punkt dockt.
Die Regel prüft danach die SupportPatch2D-Geometrien.
```

---

# 2. Neue Grundstruktur

## 2.1 Einheitliches Muster

```text
Reales Bauteil
↓
Paket-Repräsentation
↓
abstrakte Geometrie
↓
Eigenschaften
↓
ConnectorPoint
↓
Port
↓
Regel / Check / Berechnung
```

## 2.2 ConnectorPoint-Datentyp

Alle Connectoren verwenden denselben Grunddatentyp:

```text
ConnectorPoint
```

## 2.3 ConnectorPoint-Schema

```yaml
ConnectorPoint:
  id: string
  package: string
  connector_kind: string

  point: Point3D
  local_frame: CoordinateFrame3D optional
  direction: Vector3D optional

  port: string

  host_representation_id: string
  host_geometry_ref: string
  host_geometry_type: string

  check_scope_ref: string optional
  tolerance: number optional

  status:
    - active
    - warning
    - blocked
    - evidence_required
    - engineering_required

  evidence_refs: []
```

## 2.4 Bedeutung der Felder

| Feld | Bedeutung |
|---|---|
| `point` | eigentlicher Docking-Punkt |
| `direction` | Richtung, in die der Connector andockt oder wirkt |
| `port` | Kompatibilitätstyp |
| `host_geometry_ref` | abstrakte Geometrie, auf der der Punkt sitzt |
| `host_geometry_type` | Datentyp der referenzierten Geometrie |
| `check_scope_ref` | Bereich, der für den Check verwendet wird |
| `tolerance` | Andock- oder Prüftoleranz |
| `status` | aktueller Prüf- oder Nachweisstatus |

---

# 3. Entscheidende Trennung

## 3.1 ConnectorPoint

Der ConnectorPoint beantwortet:

```text
Wo dockt eine Repräsentation an eine andere an?
```

## 3.2 Port

Der Port beantwortet:

```text
Welche Art von Kompatibilität ist gemeint?
```

## 3.3 Host-Geometrie

Die Host-Geometrie beantwortet:

```text
Welche Linie, Fläche, Zone oder welches Volumen muss geprüft werden?
```

## 3.4 Regel

Die Regel beantwortet:

```text
Funktioniert diese Verbindung / Berechnung / Warnung wirklich?
```

---

# 4. Docking-Logik

## 4.1 Grundablauf

```text
ConnectorPoint A
+ ConnectorPoint B
↓
Port-Kompatibilität prüfen
↓
Punkte räumlich andocken / snappen / tolerieren
↓
Host-Geometrien laden
↓
fachliche Regel ausführen
↓
Resultat: pass / warning / fail / evidence required
```

## 4.2 Beispiel Tragwerk

```text
ConnectorPoint A:
Punkt auf Platten-Auflagerstreifen
Port: bearing_side
Host-Geometrie: SupportPatch2D der Platte

ConnectorPoint B:
Punkt auf Wandkopf
Port: support_side
Host-Geometrie: SupportPatch2D der Wand

Regel:
bearing_side → support_side

Check:
Punkte docken
SupportPatch2D der Platte und Wand werden verglichen
Überlappung, Richtung und Mindestauflager werden geprüft
```

## 4.3 Punkt ist nicht gleich Prüffläche

Wichtig:

```text
Der ConnectorPoint ist nicht die gesamte Auflagerfläche.
Er ist der Andockpunkt zur Auflagerfläche.
```

Die Fläche bleibt als Host-Geometrie in der Repräsentation.

---

# 5. Wie werden Linien, Flächen und Zonen mit Punkt-Connectoren abgebildet?

## 5.1 Eine Linie

Eine Linie bleibt eine Linie in der Repräsentation, aber der Connector ist ein Punkt auf der Linie.

```text
AlignmentLine
────────────

ConnectorPoint
      ●
```

Nutzung:

```text
Punkt dockt.
Regel prüft danach die ganze AlignmentLine.
```

## 5.2 Eine Fläche

Eine Fläche bleibt eine Fläche in der Repräsentation, aber der Connector sitzt als Referenzpunkt auf ihr.

```text
VisibilitySurface
┌────────────┐
│     ●      │
└────────────┘
```

Nutzung:

```text
Punkt aktiviert Sichtbarkeitsprüfung.
Regel prüft danach die gesamte referenzierte Fläche.
```

## 5.3 Eine Zone

Eine Zone bleibt Zone, aber der ConnectorPoint liegt im Zentrum oder an einem regelrelevanten Punkt.

```text
BlockedZone
▒▒▒▒▒▒▒▒▒▒
▒    ●   ▒
▒▒▒▒▒▒▒▒▒▒
```

Nutzung:

```text
Punkt markiert die Konfliktzone.
Regel prüft Überlappung mit Route, Bohrung oder anderer Host-Geometrie.
```

## 5.4 Eine verteilte Verbindung

Wenn eine Verbindung mehrere reale Punkte braucht, entstehen mehrere ConnectorPoints.

Beispiel Hebepunkte:

```text
●────────●
│        │
●────────●
```

Nicht:

```text
ein Flächenconnector
```

Sondern:

```text
ConnectorPoint[]
```

Also eine Liste einzelner Punkt-Connectoren.

---

# 6. Paketübersicht nach neuer Punktlogik

| Paket | abstrakte Geometrie bleibt | Connector ist immer | Host-Geometrie wird geprüft |
|---|---|---|---|
| Basisgeometrie | Solid, Mesh, Faces, Edges | keine Connectoren | keine |
| Tragwerk | Linie, Platte, Knoten, Auflagerfläche | `ConnectorPoint` | SupportPatch, Node, LineElement, ContinuityZone |
| Energie | Fläche, Schicht, Rand, Durchdringung | `ConnectorPoint` | ThermalSurface, BoundaryEdge, PenetrationLoop, BridgeZone |
| TGA | Route, Öffnung, Bohrkörper, Sperrzone | `ConnectorPoint` | RouteLine, OpeningLoop, DrillingCylinder, BlockedZone |
| Semantik | Ausrichtungslinie, Sichtfläche, Zugangszone | `ConnectorPoint` | AlignmentLine, VisibilitySurface, AccessZone |
| Logistik | Transporthülle, Hebezone, Lagerzone | `ConnectorPoint` | LiftingZone, StorageSupportZone, TransportEnvelope |
| Nachweis | Scanlinie, Schaden, Prüfpunkt | keine Connectoren | modifiziert ConnectorPoints anderer Pakete |

---

# 7. Paket 0 — Basisgeometrie

## 7.1 Abstraktionslogik

```text
Reales Bauteil
→ neutraler geometrischer Körper
→ messbare Geometrie
→ keine Connectoren
→ keine Ports
```

## 7.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| neutraler Körper | `SolidMesh` oder `BRep` | digitale Ausgangsform |
| Bounding Box | `OrientedBoundingBox` | Maße und Transporthülle ableiten |
| Hauptflächen | `FaceSet` | Quelle für Energie, Semantik, Logistik |
| Hauptkanten | `EdgeSet` | Quelle für Tragwerk, Fuge, Ausrichtung |
| rohe Öffnungen | `OpeningLoop[]` | Quelle für TGA und Hülle |
| lokale Achsen | `CoordinateFrame3D` | Orientierung standardisieren |

## 7.3 Connectoren

```text
keine
```

Die Basisgeometrie bekommt niemals ConnectorPoints.  
Alle ConnectorPoints werden in fachlichen Paketen erzeugt.

## 7.4 Beispiel A — Abbau/Aufbau DE_1OG_001

Die Deckenplatte wird als `SolidMesh` / `BRep` gespeichert.  
Die `OrientedBoundingBox` ergibt 4500 × 2300 × 180 mm.  
`FaceSet` enthält Oberseite, Unterseite und Seitenflächen.  
`EdgeSet` enthält lange und kurze Kanten.

Es gibt keine ConnectorPoints. Eine lange Kante kann später im Tragwerk Host-Geometrie für einen punktbasierten `bearing_support` werden.

## 7.5 Beispiel B — SlabBeamColumnFragment

Das Fragment ist ein monolithischer `SolidMesh`.  
Die Teilregionen werden als `VolumeRegion` oder `FaceSet` markiert:

```text
slab_region
beam_region
column_region
cut_faces
```

Es gibt keine ConnectorPoints. Die Teilregionen sind nur Quellen für spätere Paket-Repräsentationen.

## 7.6 Beispiel C — ReCreate Hollow-Core Slab

Die Hohlkammerdecke wird als `BRep` oder `SolidMesh` mit `VoidVolume[]` gespeichert.  
Die Hohlräume sind noch keine Route und keine Connectoren.

---

# 8. Paket 1 — Tragwerk

## 8.1 Abstraktionslogik

```text
Reales tragendes Bauteil
→ Tragwerksmodell
→ Linie / Platte / Knoten / Auflagerpatch
→ Eigenschaften
→ ConnectorPoint
→ Port
→ strukturelle Regel
```

## 8.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| Trägerachse | `LineElement1D` | Biegung, Querkraft, Knotenanschluss |
| Stützenachse | `LineElement1D` | Normalkraft, Knicken, vertikale Last |
| Platte | `PlateElement2D` | Lastabtragung und Auflagerlogik |
| Wandscheibe | `WallPanel2D` | vertikale Scheiben- und Auflagerlogik |
| Knoten | `Node` | Verbindung von Linien, Platten und Stützen |
| Auflagerpatch | `SupportPatch2D` | Auflagerüberlappung und Mindestauflager |
| Transferknoten | `TransferNode` | Lastübergang zwischen Teilrepräsentationen |
| Kontinuitätszone | `ContinuityZone` | Kraftschluss / Bewehrung / Verguss |

## 8.3 ConnectorPoint-Typen

Alle folgenden Connectoren sind Punkte:

| Connector kind | Port | Punkt sitzt auf Host-Geometrie | Regel prüft |
|---|---|---|---|
| `bearing_support` | `bearing_side` / `support_side` | `SupportPatch2D` oder `Node` | Auflagerung |
| `joint_connection` | `member_side` | `JointLine` oder `LineElement1D` | Fuge / Ausrichtung |
| `anchor_connection` | `anchor_side` | `AnchorZone2D` | Ankerbarkeit |
| `continuity_connection` | `continuity_side` | `ContinuityZone` | Kraftschluss |
| `support_transfer` | `transfer_side` | `TransferNode` | Lastübertragung |

## 8.4 Berechnung / Check

```text
ConnectorPoint A + ConnectorPoint B
+ Ports
+ Host-Geometrien
+ Eigenschaften
↓
struktureller Check
```

Beispiel:

```text
Punkt auf Platten-SupportPatch
dockt an
Punkt auf Wand-SupportPatch
↓
Regel prüft die beiden SupportPatch2D-Flächen
```

## 8.5 Beispiel A — Abbau/Aufbau Wand–Decke mit DE_1OG_001

**Komponenten:**  
DE_1OG_001 als Deckenplatte und eine wiederverwendete Wand.

**Repräsentation:**  
Die Decke ist `PlateElement2D`.  
Die Wand ist `WallPanel2D`.

**Host-Geometrien:**  
Die Plattenkante erzeugt einen `SupportPatch2D`.  
Der Wandkopf erzeugt einen `SupportPatch2D`.  
Eine Anschlusszone erzeugt `AnchorZone2D` oder `ContinuityZone`.

### Punkt-Connectoren der Decke

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `slab_edge_bearing_point` | `bearing_side` | Mittelpunkt des Auflagerstreifens | `SupportPatch2D` | Decke dockt auf Wand |
| `slab_anchor_point` | `anchor_side` | Ankerreferenzpunkt an Kante | `AnchorZone2D` | Schraubanker / Flachstahlhalter |
| `slab_continuity_point` | `continuity_side` | Punkt in Vergusszone | `ContinuityZone` | Bewehrungsanschluss + Verguss |

### Punkt-Connectoren der Wand

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `wall_head_support_point` | `support_side` | Mittelpunkt Wandkopf | `SupportPatch2D` | Wand trägt Decke |
| `wall_anchor_receiver_point` | `support_side` | Ankerempfangspunkt | `AnchorReceiverZone2D` | Ankeraufnahme |
| `wall_continuity_point` | `continuity_side` | Punkt in Anschlusszone | `ContinuityZone` | Kraftschluss |

### Regeln

| Docking | Check |
|---|---|
| `slab_edge_bearing_point` → `wall_head_support_point` | Punkte docken; `SupportPatch2D`-Überlappung, Richtung, Mindestauflager werden geprüft |
| `slab_anchor_point` → `wall_anchor_receiver_point` | Punkte docken; `AnchorZone2D` und Bewehrung werden geprüft |
| `slab_continuity_point` → `wall_continuity_point` | Punkte docken; `ContinuityZone`, Vergussraum und Bewehrung werden geprüft |

**Wichtig:**  
Die Connectoren sind Punkte. Die Auflagerfläche selbst bleibt `SupportPatch2D`.

## 8.6 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Fragment mit Platte, integriertem Träger und Stützenabschnitt.

**Repräsentation:**  
`StructuralGraph` aus:

```text
PlateElement2D
LineElement1D für Träger
LineElement1D für Stütze
TransferNode
ContinuityZone
```

### Punkt-Connectoren

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `fragment_plate_bearing_point` | `bearing_side` | Punkt am Plattenrand | `SupportPatch2D` | Plattenregion kann aufliegen |
| `fragment_transfer_point` | `transfer_side` | Punkt am Transferknoten | `TransferNode` | Lastübergang Platte-Träger-Stütze |
| `fragment_column_support_point` | `support_side` | Punkt an Stützenfuß oder Kopf | `Node` / `SupportPatch2D` | Stützenregion nimmt Last auf |
| `fragment_cut_continuity_point` | `continuity_side` | Punkt auf Schnittfläche | `ContinuityZone` | kraftschlüssiger Anschluss |

### Regeln

Der Transfer-Check dockt Punkte an, prüft aber den `StructuralGraph`.  
Die Kontinuitätsregel dockt Punkte an, prüft aber `ContinuityZone`, Bewehrung und Verguss.

## 8.7 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Wiedergewonnene Hohlkammerdecke.

**Repräsentation:**  
`PlateElement2D` oder einachsig spannendes Fertigteilmodell.

### Punkt-Connectoren

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `hcs_end_A_bearing_point` | `bearing_side` | Mittelpunkt Stirnauflager A | `SupportPatch2D` | erstes Auflager |
| `hcs_end_B_bearing_point` | `bearing_side` | Mittelpunkt Stirnauflager B | `SupportPatch2D` | zweites Auflager |
| `hcs_long_joint_point` | `member_side` | Punkt auf Längsfuge | `JointLine` | Fugen- und Toleranzprüfung |

### Regeln

Der Endauflager-Check nutzt die Punkte zum Andocken und die `SupportPatch2D`-Host-Geometrien zur Prüfung.  
Der Fugencheck nutzt den `hcs_long_joint_point`, prüft aber die gesamte `JointLine`.

---

# 9. Paket 2 — Energie / Gebäudehülle

## 9.1 Abstraktionslogik

```text
Reales Hüllenbauteil
→ thermisches Modell
→ Fläche / Schicht / Rand / Durchdringung
→ ConnectorPoint
→ Port
→ U-Wert-, Kontinuitäts-, Abdichtungs- und Wärmebrückencheck
```

## 9.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| thermische Fläche | `ThermalSurface` | U-Wert- und Innen-/Außenbezug |
| Schicht | `Layer` | Dicke und Material für R-Wert |
| Rand | `BoundaryEdge` | thermische Kontinuität |
| Durchdringung | `PenetrationLoop` | Abdichtung |
| Wärmebrücke | `BridgeZone` | Warnung |
| Dämmschnittstelle | `InsulationInterface` | Dämmkontinuität |

## 9.3 Punkt-Connectoren

| Connector kind | Port | Punkt sitzt auf Host-Geometrie | Regel prüft |
|---|---|---|---|
| `thermal_continuity` | `thermal_side` | `BoundaryEdge` oder `ThermalSurface` | Hüllenkontinuität |
| `insulation_continuity` | `insulation_side` | `InsulationInterface` | Dämmlücken |
| `penetration_sealing` | `penetration_side` | `PenetrationLoop` | Abdichtung |
| `thermal_bridge_warning` | `bridge_side` | `BridgeZone` | Wärmebrückenrisiko |

## 9.4 Beispiel A — Abbau/Aufbau 200-mm-Stahlbetonwand

### Punkt-Connectoren

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `wall_insulation_point` | `insulation_side` | Referenzpunkt auf Außenseite | `InsulationInterface` | Dämmung schließt an |
| `wall_thermal_edge_point` | `thermal_side` | Punkt am Wandrand | `BoundaryEdge` | thermische Grenze läuft weiter |
| `wall_penetration_point` | `penetration_side` | Mittelpunkt einer Öffnung | `PenetrationLoop` | Abdichtung prüfen |

Die U-Wert-Vorprüfung nutzt `ThermalSurface` und `Layer`, nicht den ConnectorPoint allein.

## 9.5 Beispiel B — SlabBeamColumnFragment

Falls das Fragment Teil der Hülle wird:

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `fragment_thermal_point` | `thermal_side` | Punkt auf Schnittkante | `BoundaryEdge` | thermischer Anschluss |
| `fragment_bridge_point` | `bridge_side` | Punkt am monolithischen Knoten | `BridgeZone` | Wärmebrückenwarnung |

Die Brückenregel dockt nicht an eine Fläche an, sondern markiert eine `BridgeZone` über einen Punkt als prüfrelevant.

## 9.6 Beispiel C — ReCreate Hollow-Core Slab

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `hcs_insulation_point` | `insulation_side` | Punkt auf Oberseite | `InsulationInterface` | Dämmung bei Dachnutzung |
| `hcs_edge_bridge_point` | `bridge_side` | Punkt an Plattenkante | `BridgeZone` | Wärmebrücke |
| `hcs_penetration_point` | `penetration_side` | Punkt an Durchdringung | `PenetrationLoop` | Abdichtung |

---

# 10. Paket 3 — TGA / Öffnungen

## 10.1 Abstraktionslogik

```text
Reale Leitung / Öffnung
→ Routenmodell
→ Linie / Öffnung / Bohrkörper / Sperrzone
→ ConnectorPoint
→ Port
→ Routen- und Konfliktcheck
```

## 10.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| Route | `RouteLine` | Leitungsverlauf |
| Routenknoten | `RouteNode` | Richtungswechsel / Übergang |
| Öffnung | `OpeningLoop` | vorhandene Durchdringung |
| Bohrung | `DrillingCylinder` | neue Durchdringung |
| Sperrzone | `BlockedZone` | Konfliktbereich |
| Lichtraum | `ClearanceVolume` | Platzbedarf |

## 10.3 Punkt-Connectoren

| Connector kind | Port | Punkt sitzt auf Host-Geometrie | Regel prüft |
|---|---|---|---|
| `route_continuity` | `route_side` | `RouteLine` oder `RouteNode` | Leitungsfortsetzung |
| `opening_use` | `opening_side` | `OpeningLoop` | Öffnungsnutzung |
| `drilling_candidate` | `drilling_side` | `DrillingCylinder` | neue Bohrung |
| `blocked_conflict` | `blocked_side` | `BlockedZone` | Konflikt |

## 10.4 Beispiel A — Abbau/Aufbau Öffnung

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `opening_use_point` | `opening_side` | Mittelpunkt Öffnung | `OpeningLoop` | Öffnung nutzen |
| `route_point` | `route_side` | Routenendpunkt | `RouteLine` | Leitung dockt an Öffnung |

Regel: Punkte docken, aber Durchmesser, Randabstand und Konflikt werden an `OpeningLoop`, `RouteLine` und `ClearanceVolume` geprüft.

## 10.5 Beispiel B — SlabBeamColumnFragment

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `fragment_drilling_point` | `drilling_side` | Bohrzentrum | `DrillingCylinder` | neue Bohrung |
| `fragment_blocked_point` | `blocked_side` | Punkt in Sperrzone | `BlockedZone` | Träger-/Stützenbereich blockiert |

Regel: Der Drilling Point dockt an eine Route, aber die Regel prüft den ganzen `DrillingCylinder` gegen `BlockedZone` und Tragwerkszonen.

## 10.6 Beispiel C — ReCreate Hollow-Core Slab

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `hcs_void_route_point` | `route_side` | Punkt auf Hohlkammerachse | `RouteLine` | Hohlraum als Route |
| `hcs_drilling_point` | `drilling_side` | Bohrzentrum | `DrillingCylinder` | neue Durchdringung |

Hohlräume sind nur dann TGA-relevant, wenn ein `route_continuity`-Punkt auf einer `RouteLine` erzeugt wird.

---

# 11. Paket 4 — Semantik / Architektur

## 11.1 Abstraktionslogik

```text
Reales Bauteil als Entwurfselement
→ Design-Handle-Modell
→ Ausrichtungslinie / Sichtfläche / Zugangszone
→ ConnectorPoint
→ Port
→ Entwurfscheck
```

## 11.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| Ausrichtung | `AlignmentLine` | Raster, Fuge, Datum |
| Sichtfläche | `VisibilitySurface` | Sichtbarkeit / Verdeckung |
| Zugang | `AccessZone` | Annäherung / Durchgang |
| Seite | `SideRegion` | Raum- oder Fassadenbezug |
| Stapelfläche | `StackPlane` | Niveau / vertikale Beziehung |
| Öffnungsachse | `OpeningAxis` | Öffnungsbezug |
| Raumgrenze | `SpatialBoundarySurface` | Raumkontinuität |

## 11.3 Punkt-Connectoren

| Connector kind | Port | Punkt sitzt auf Host-Geometrie | Regel prüft |
|---|---|---|---|
| `access_handle` | `access_port` | `AccessZone` | Zugang / Lichtraum |
| `attachment_handle` | `attachment_port` | Anbindungsbereich | architektonische Anbindung |
| `stack_handle` | `top_port` / `bottom_port` | `StackPlane` | vertikale Relation |
| `side_handle` | `side_port` | `SideRegion` | Raum- oder Seitenbezug |
| `opening_handle` | `opening_port` | `OpeningAxis` | Öffnungsbezug |
| `alignment_handle` | `alignment_port` | `AlignmentLine` | Ausrichtung |
| `visibility_constraint_handle` | `visibility_port` | `VisibilitySurface` | Sichtbarkeit |

## 11.4 Beispiel A — Abbau/Aufbau DE_1OG_001

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `slab_alignment_point` | `alignment_port` | Punkt auf langer Kante | `AlignmentLine` | Fuge / Raster ausrichten |
| `slab_visibility_point` | `visibility_port` | Punkt auf Unterseite | `VisibilitySurface` | Untersicht sichtbar halten |

Regel: Der Punkt dockt an andere Alignment- oder Visibility-Logiken, aber der Check nutzt die ganze Linie oder Fläche.

## 11.5 Beispiel B — SlabBeamColumnFragment

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `fragment_access_point` | `access_port` | Punkt im Nischenzugang | `AccessZone` | Zugang prüfen |
| `fragment_side_point` | `side_port` | Punkt auf Stützenseite | `SideRegion` | Raumbeziehung |
| `fragment_alignment_point` | `alignment_port` | Punkt auf Schnittkante / Trägerlinie | `AlignmentLine` | Ausrichtung |
| `fragment_visibility_point` | `visibility_port` | Punkt auf sichtbarer Fragmentfläche | `VisibilitySurface` | Lesbarkeit |

## 11.6 Beispiel C — ReCreate Hollow-Core Slab

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `hcs_alignment_point` | `alignment_port` | Punkt auf Längsfuge | `AlignmentLine` | Modul- / Fugenausrichtung |
| `hcs_top_stack_point` | `top_port` | Punkt auf Oberseite | `StackPlane` | Niveau / Stapelung |
| `hcs_bottom_stack_point` | `bottom_port` | Punkt auf Unterseite | `StackPlane` | Gegenstück zur Stapelung |
| `hcs_visibility_point` | `visibility_port` | Punkt auf Unterseite | `VisibilitySurface` | sichtbare Wiederverwendung |

---

# 12. Paket 5 — Logistik / Montage

## 12.1 Abstraktionslogik

```text
Reales Bauteil im Prozess
→ Handlingmodell
→ Transporthülle / Schwerpunkt / Hebezone / Lagerauflager
→ ConnectorPoint
→ Port
→ Prozesscheck
```

## 12.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| Transporthülle | `TransportEnvelope` | Transportmaße |
| Schwerpunkt | `CenterOfGravityPoint` | Heben / Stabilität |
| Hebezone | `LiftingZone` | Hebeplanung |
| Lagerauflager | `StorageSupportZone` | Lagerung |
| Transportauflager | `TransportSupportZone` | Ladungssicherung |
| Montagezugang | `AccessVolume` | Montagezugang |
| Schutzzone | `ProtectionZone` | Schutzbedarf |
| temporäre Abstützung | `TemporaryBracingZone` | Montagezustand |

## 12.3 Punkt-Connectoren

| Connector kind | Port | Punkt sitzt auf Host-Geometrie | Regel prüft |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | `LiftingZone` | Hebbarkeit |
| `storage_handle` | `storage_port` | `StorageSupportZone` | Lagerung |
| `transport_handle` | `transport_port` | `TransportEnvelope` oder `TransportSupportZone` | Transport |
| `access_handle` | `access_port` | `AccessVolume` | Montagezugang |
| `protection_handle` | `protection_port` | `ProtectionZone` | Schutz |
| `temporary_bracing_handle` | `temporary_bracing_port` | `TemporaryBracingZone` | temporäre Stabilität |

## 12.4 Beispiel A — Abbau/Aufbau DE_1OG_001

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `slab_storage_point` | `storage_port` | Punkt auf Lagerauflager | `StorageSupportZone` | liegende Lagerung |
| `slab_transport_point` | `transport_port` | Referenzpunkt der Transporthülle | `TransportEnvelope` | Transport prüfen |
| `slab_lifting_point` | `lifting_port` | Hebekandidat | `LiftingZone` | Hebbarkeit prüfen |
| `slab_protection_point` | `protection_port` | Punkt an sensibler Kante | `ProtectionZone` | Schutz prüfen |

## 12.5 Beispiel B — SlabBeamColumnFragment

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `fragment_lifting_point` | `lifting_port` | Hebekandidat | `LiftingZone` | Fragment heben |
| `fragment_storage_point` | `storage_port` | Lagerauflagerpunkt | `StorageSupportZone` | kippsichere Lagerung |
| `fragment_protection_point` | `protection_port` | Punkt auf Schnittfläche | `ProtectionZone` | Schnittfläche schützen |
| `fragment_bracing_point` | `temporary_bracing_port` | Punkt an Abstützzone | `TemporaryBracingZone` | temporäre Stabilisierung |

## 12.6 Beispiel C — ReCreate Hollow-Core Slab

| ConnectorPoint | Port | Punkt | Host-Geometrie | Bedeutung |
|---|---|---|---|---|
| `hcs_lifting_point` | `lifting_port` | Hebepunkt | `LiftingZone` | Heben |
| `hcs_transport_point` | `transport_port` | Transportreferenzpunkt | `TransportEnvelope` | Transport |
| `hcs_storage_point` | `storage_port` | Lagerauflagerpunkt | `StorageSupportZone` | Lagerung |

---

# 13. Paket 6 — Nachweis-Overlay

## 13.1 Abstraktionslogik

```text
Realer Nachweis
→ Overlay
→ Scanlinie / Schaden / Prüfpunkt / unbekannte Zone
→ keine Connectoren
→ keine Ports
→ Statusmodifikation vorhandener ConnectorPoints
```

## 13.2 Abstrakte Geometrie: Datentyp und Zweck

| Geometrie | Datentyp | Zweck |
|---|---|---|
| Nachweiszone | `EvidenceZone` | Bereich eines Nachweises |
| Scanlinie | `ScanLine` | Bewehrung / Messlinie |
| Schadensfläche | `DamagePolygon` | Schaden mit Connector-Host vergleichen |
| Risslinie | `CrackLine` | Rissverlauf prüfen |
| Prüfpunkt | `TestPoint` | Karbonatisierung / Chlorid / Bohrkern |
| unbekannte Zone | `UnknownZone` | Risiko fehlender Information |
| Konfidenzfeld | `ConfidenceField` | Zuverlässigkeit räumlich darstellen |

## 13.3 Connectoren und Ports

```text
keine Connectoren
keine Ports
```

Nachweis-Overlays docken nicht.  
Sie überlagern Host-Geometrien oder ConnectorPoints und modifizieren deren Status.

## 13.4 Check

```text
Evidence geometry
+ ConnectorPoint
+ Host-Geometrie
↓
Überlappung / Nähe / Zugehörigkeit
↓
confirmed / warning / blocked / evidence_required
```

## 13.5 Beispiel A — Abbau/Aufbau Bewehrungsnachweis

Eine `UnknownZone` oder fehlende `ScanLine` überlagert die `AnchorZone2D` eines `anchor_connection`-Punkts. Der ConnectorPoint bleibt Punkt, aber sein Status wird `blocked` oder `evidence_required`.

## 13.6 Beispiel B — SlabBeamColumnFragment Schnittfläche

Ein `DamagePolygon` überlagert die `ContinuityZone` eines `fragment_cut_continuity_point`. Der Punkt bleibt der Connector, aber der Check markiert ihn als `engineering_required`.

## 13.7 Beispiel C — ReCreate QR / Test / Neuberechnung

Ein `EvidenceRecord` bestätigt die Identität. Ein `TestPoint` oder eine Neuberechnung erhöht die Konfidenz der `bearing_support`-ConnectorPoints. Ein `DamagePolygon` an der Fuge kann den `joint_connection`-ConnectorPoint auf `manual_check_required` setzen.

---

# 14. Kompakte Kompatibilitätsregeln

| Regel | Punkt-Port-Docking | Host-Geometrie-Check |
|---|---|---|
| strukturelles Auflager | `bearing_side → support_side` | `SupportPatch2D`-Überlappung, Richtung, Auflagerlänge |
| strukturelle Verankerung | `anchor_side → support_side` | `AnchorZone2D`, Randabstand, Bewehrung |
| strukturelle Kontinuität | `continuity_side → continuity_side` | `ContinuityZone`, Verguss, Bewehrung |
| struktureller Transfer | `transfer_side → support_side / bearing_side` | `StructuralGraph`, `TransferNode`, Lastpfad |
| thermische Kontinuität | `thermal_side → thermal_side` | `BoundaryEdge`, `ThermalSurface` |
| Dämmkontinuität | `insulation_side → insulation_side` | `InsulationInterface`, Lücken |
| Hüllendurchdringung | `penetration_side → thermal_side / insulation_side` | `PenetrationLoop`, Luftdichtheit, Feuchte |
| TGA-Route | `route_side → route_side` | `RouteLine`, `ClearanceVolume` |
| TGA-Öffnung | `opening_side → route_side` | `OpeningLoop`, Durchmesser, Randabstand |
| TGA-Bohrung | `drilling_side → route_side` | `DrillingCylinder`, Rebar, Tragwerkszone |
| architektonischer Zugang | `access_port → access_port` | `AccessZone`, Lichtraum |
| architektonische Stapelung | `top_port → bottom_port` | `StackPlane`, Niveau |
| architektonische Ausrichtung | `alignment_port → alignment_port` | `AlignmentLine`, Raster, Fuge |
| Logistik Heben | `lifting_port → Prozessanforderung` | `LiftingZone`, Schwerpunkt |
| Logistik Lagerung | `storage_port → Lagerbedingung` | `StorageSupportZone`, Orientierung |

---

# 15. Gesamtabstraktion der drei Beispiele

## 15.1 Abbau/Aufbau DE_1OG_001

| Paket | Repräsentation | Host-Geometrie | Punkt-Connectoren |
|---|---|---|---|
| Basisgeometrie | neutraler Plattenkörper | `SolidMesh`, `FaceSet`, `EdgeSet` | keine |
| Tragwerk | `PlateElement2D` | `SupportPatch2D`, `AnchorZone2D`, `ContinuityZone` | `slab_edge_bearing_point`, `slab_anchor_point`, `slab_continuity_point` |
| Energie | Hülle, falls relevant | `ThermalSurface`, `InsulationInterface`, `BridgeZone` | `wall_insulation_point`, `thermal_edge_point`, `penetration_point` |
| TGA | Öffnungs-/Bohrmodell | `OpeningLoop`, `RouteLine`, `DrillingCylinder` | `opening_use_point`, `route_point`, `drilling_point` |
| Semantik | architektonisches Plattenmodell | `AlignmentLine`, `VisibilitySurface` | `slab_alignment_point`, `slab_visibility_point` |
| Logistik | Handlingmodell | `TransportEnvelope`, `LiftingZone`, `StorageSupportZone` | `slab_storage_point`, `slab_transport_point`, `slab_lifting_point` |
| Nachweis | Overlay | `ScanLine`, `DamagePolygon`, `UnknownZone` | keine; modifiziert ConnectorPoints |

## 15.2 SlabBeamColumnFragment

| Paket | Repräsentation | Host-Geometrie | Punkt-Connectoren |
|---|---|---|---|
| Basisgeometrie | monolithischer Körper | `SolidMesh`, `VolumeRegion`, `FaceSet` | keine |
| Tragwerk | `StructuralGraph` | `PlateElement2D`, `LineElement1D`, `TransferNode`, `ContinuityZone` | `fragment_plate_bearing_point`, `fragment_transfer_point`, `fragment_cut_continuity_point` |
| Energie | Hülle, falls relevant | `BoundaryEdge`, `BridgeZone` | `fragment_thermal_point`, `fragment_bridge_point` |
| TGA | Bohr- und Sperrzonenmodell | `DrillingCylinder`, `BlockedZone` | `fragment_drilling_point`, `fragment_blocked_point` |
| Semantik | Fragmentmodell | `AccessZone`, `SideRegion`, `AlignmentLine`, `VisibilitySurface` | `fragment_access_point`, `fragment_side_point`, `fragment_alignment_point`, `fragment_visibility_point` |
| Logistik | komplexes Handlingmodell | `LiftingZone`, `StorageSupportZone`, `ProtectionZone`, `TemporaryBracingZone` | `fragment_lifting_point`, `fragment_storage_point`, `fragment_protection_point`, `fragment_bracing_point` |
| Nachweis | Schnittflächen-Overlay | `EvidenceZone`, `ScanLine`, `DamagePolygon`, `UnknownZone` | keine; modifiziert ConnectorPoints |

## 15.3 ReCreate Hollow-Core Slab

| Paket | Repräsentation | Host-Geometrie | Punkt-Connectoren |
|---|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | `BRep`, `VoidVolume[]`, `OpeningLoop[]` | keine |
| Tragwerk | einachsig spannende Platte | `PlateElement2D`, `SupportPatch2D`, `JointLine` | `hcs_end_A_bearing_point`, `hcs_end_B_bearing_point`, `hcs_long_joint_point` |
| Energie | Hülle, falls relevant | `ThermalSurface`, `InsulationInterface`, `BridgeZone` | `hcs_insulation_point`, `hcs_edge_bridge_point`, `hcs_penetration_point` |
| TGA | Hohlraum-/Bohrmodell | `RouteLine`, `DrillingCylinder` | `hcs_void_route_point`, `hcs_drilling_point` |
| Semantik | Modulmodell | `AlignmentLine`, `StackPlane`, `VisibilitySurface` | `hcs_alignment_point`, `hcs_top_stack_point`, `hcs_bottom_stack_point` |
| Logistik | Transport-/Hebemodell | `LiftingZone`, `TransportEnvelope`, `StorageSupportZone` | `hcs_lifting_point`, `hcs_transport_point`, `hcs_storage_point` |
| Nachweis | BIM / QR / Test | `EvidenceRecord`, `TestPoint`, `ConfidenceField`, `DamagePolygon` | keine; modifiziert ConnectorPoints |

---

# 16. Finale Regel

Die entscheidende Systemregel lautet:

```text
Connectoren sind immer Punkte.
```

Aber:

```text
Punkte ersetzen nicht die fachliche Prüfgeometrie.
```

Die richtige Struktur ist:

```text
ConnectorPoint
= Docking-Punkt + Port + Richtung + Referenz auf Host-Geometrie

Host-Geometrie
= Linie / Fläche / Zone / Volumen der Paket-Repräsentation

Regel
= dockt ConnectorPoints und prüft die Host-Geometrien
```

Dadurch kann jede Repräsentation sauber andocken:

```text
PlateElement2D dockt an WallPanel2D
ThermalSurface dockt an ThermalSurface
RouteLine dockt an OpeningLoop
AlignmentLine dockt an AlignmentLine
LiftingZone dockt an Prozessanforderung
EvidenceZone modifiziert ConnectorPoint-Status
```

So bleibt das System minimal, maschinenlesbar und gleichzeitig konkret genug, um echte ReUse-Bauteile mit unterschiedlichen abstrakten Repräsentationen zu prüfen.
