# Finales Systemdokument  
# SharedConnectorPoint-System für Entwerfen mit wiederverwendeten Bauteilen

**Version:** Finaler Entwurfsstand  
**Sprache:** Deutsch  
**Prinzip:** wenige strategisch gesetzte Punkt-Connectoren, paketübergreifend genutzt  
**Kernregel:** Ein Punkt. Mehrere Facets. Eine Verbindung. Viele Checks.

---

## 0. Kurzfassung

Das System modelliert wiederverwendete Bauteile nicht mit vielen paket-spezifischen Connectoren.  
Stattdessen bekommt jedes Bauteil wenige strategisch gesetzte **SharedConnectorPoints**.

Ein **SharedConnectorPoint** ist immer ein Punkt im Raum.  
Er ist kein Streifen, keine Fläche, keine Linie und keine Zone.

Die fachlichen Prüfgeometrien bleiben aber erhalten. Sie heißen **Host-Geometrien** und liegen in den jeweiligen Paket-Repräsentationen.

```text
SharedConnectorPoint
= Docking-Punkt

Facet
= paket-spezifische Bedeutung dieses Punktes

Port
= Kompatibilitätstyp innerhalb eines Facets

Host-Geometrie
= Linie / Fläche / Zone / Volumen, die fachlich geprüft wird

Regel
= dockt Punkte und prüft Host-Geometrien
```

Damit kann ein einziger Punkt gleichzeitig tragen, ausrichten, warnen, montierbar sein oder durch Nachweise blockiert werden.

Beispiel:

```text
slab_edge_A_midpoint
│
├── StructuralFacet → bearing_side → SupportPatch2D
├── SemanticFacet   → alignment_port → AlignmentLine
├── EnergyFacet     → bridge_side → BridgeZone
└── LogisticsFacet  → access_port → AccessVolume
```

Die Komponente bleibt einfach.  
Die Verbindung wird reich an Information.

---

# 1. Quellenbasis

## 1.1 Abbau/Aufbau-Handbuch

Das Abbau/Aufbau-Handbuch wird als konkrete Referenz für wiederverwendete Stahlbetonelemente, Bauteilkatalog, Anschlussfamilien, Logistik und Nachweislogik verwendet.

Wichtige verwendete Inhalte:

- Fokus auf wiederverwendete, möglichst großformatige Stahlbetonelemente wie Platte, Scheibe, Träger oder Stütze.
- Bauteilkatalog mit ID, Skizze, Maßen, Öffnungsmaßen, Volumen und Masse.
- Erweiterbarkeit des Bauteilkatalogs mit Beton- und Bewehrungsuntersuchungen.
- Beispiel `DE_1OG_001` mit:
  - Länge: 4500 mm
  - Breite: 2300 mm
  - Höhe / Dicke: 180 mm
  - Volumen: 1.863 m³
  - Masse: ca. 4.1 t
- Anschlussfamilien im Kapitel Ausführungsplanung:
  - Wand–Decke: nachträglicher Bewehrungsanschluss + Verguss
  - Wand–Decke: Schraubanker mit Flachstahlhalter
  - Stütze–Decke: nachträglich montierter Edelstahldorn
  - Stütze–Decke: Winkelverbinder
  - Stütze–Decke: Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
  - Stütze–Decke: Auflager auf Stahlträger
- Lagerlogik:
  - Zwischenlager muss geplant werden.
  - Elemente sollen möglichst nach späterer Einbaureihenfolge gelagert werden.
  - Witterungsschutz wird empfohlen.
  - Lagerhölzer trennen Elemente.
  - Decken liegend, Wände und Stützen eher stehend lagern.

Quelle:  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

---

## 1.2 Abbau/Aufbau Masterarbeit 2020

Die Masterarbeit 2020 dient als Quelle für die Fragmentlogik.

Wichtige verwendete Inhalte:

- Untersuchung der Wiederverwendung zugeschnittener Stahlbetonelemente.
- Räumlich interessante Fragmente wie:
  - Stützen vor Fenstern
  - Nische hinter Stütze
  - Große Stütze in kleinem Raum
- In der entwurflichen Logik werden zugeschnittene Betonteile nicht nur als neutrale Bauteile, sondern als räumlich wirksame Fragmente behandelt.
- Die verwendeten Teile liegen auf einem Halbfertigteil-Stahlbetonträger und werden über nachträglichen Bewehrungsanschluss kraftschlüssig verbunden.

Quelle:  
https://abbauaufbau.de/project/masterarbeit-2020

**Wichtige Systemannahme:**  
`SlabBeamColumnFragment` ist kein benanntes Originalobjekt in der Quelle.  
Es ist eine abgeleitete Systemtypologie für ein monolithisches Fragment mit:

```text
Plattenbereich
integriertem Trägerbereich
Stützenabschnitt
Schnittflächen
räumlicher Fragmentqualität
```

---

## 1.3 ReCreate

ReCreate wird als Beispiel für wiederverwendete Betonfertigteile genutzt, insbesondere für Hohlkammerdecken.

Wichtige verwendete Inhalte:

- Niederländischer Pilot:
  - Prinsenhof-Gebäude in Arnhem.
  - Tragstruktur mit Hohlkammerdecken, die von tragender Fassade zu tragender Fassade spannen.
  - Nassverbindungen.
  - Sägen entlang der Längsfugen.
  - Heben und Transport zur Lager-/Wiederverwendungslogik.
  - Mock-up zur Prüfung von Maßtoleranz und Wiederverbindung.
- Finnischer Pilot:
  - BIM-Inventarisierung.
  - Codiersystem für Rückverfolgbarkeit.
  - QR-Codes vor Transport ins Lager.
  - zerstörungsfreie, teilzerstörende und zerstörende Tests.
  - Neuberechnung nach aktuellen Tragwerksnormen.

Quellen:  
https://recreate-project.eu/project-pilots/the-netherlands/  
https://recreate-project.eu/project-pilots/finland/

---

# 2. Systemziel

Das System soll einen existierenden Pool wiederverwendeter Bauteile entwerfbar machen.

Es muss nicht die ganze Realität speichern.  
Es muss nur speichern, was für diese Aufgaben nötig ist:

```text
Verbindung
Berechnung
Warnung
Kompatibilität
Entwurfsentscheidung
Nachweisstatus
```

Das Ziel ist:

```text
minimale Bauteilstruktur
maximale paketübergreifende Prüfbarkeit
```

---

# 3. Finales Kernprinzip

## 3.1 Nicht mehr: Paket erzeugt Connectoren

Falsch beziehungsweise zu redundant:

```text
Tragwerk erzeugt eigene ConnectorPoints
Energie erzeugt eigene ConnectorPoints
TGA erzeugt eigene ConnectorPoints
Semantik erzeugt eigene ConnectorPoints
Logistik erzeugt eigene ConnectorPoints
```

Das führt zu Punktchaos.

Beispiel Plattenkante:

```text
structural_bearing_point
semantic_alignment_point
energy_bridge_point
logistics_access_point
```

Oft liegen alle auf derselben realen Stelle.

---

## 3.2 Stattdessen: Bauteil erzeugt SharedConnectorPoints

Richtig:

```text
Bauteil erzeugt wenige strategische SharedConnectorPoints.
Pakete hängen Facets an diese Punkte.
Facets tragen Ports und Host-Geometrie-Referenzen.
Verbindungen aktivieren kompatible Facets.
Regeln prüfen die referenzierten Host-Geometrien.
```

Kurz:

```text
Ein Punkt.
Mehrere Facets.
Eine Verbindung.
Viele Checks.
```

---

# 4. Zentrale Begriffe

## 4.1 Component

Ein reales wiederverwendetes Bauteil oder Fragment.

Beispiele:

```text
DE_1OG_001
SlabBeamColumnFragment
ReCreate Hollow-Core Slab
```

---

## 4.2 Package Representation

Eine fachliche Abstraktion derselben Komponente.

Pakete:

```text
Basisgeometrie
Tragwerk
Energie / Gebäudehülle
TGA / Öffnungen
Semantik / Architektur
Logistik / Montage
Nachweis-Overlay
```

---

## 4.3 Host-Geometrie

Die Host-Geometrie ist die fachliche Prüfgeometrie eines Pakets.

Sie kann Linie, Fläche, Zone, Volumen oder Graph sein.

Beispiele:

| Paket | Host-Geometrie | Datentyp |
|---|---|---|
| Tragwerk | Auflagerfläche | `SupportPatch2D` |
| Tragwerk | Lasttransferknoten | `TransferNode` |
| Energie | Wärmebrückenzone | `BridgeZone` |
| Energie | Dämmschnittstelle | `InsulationInterface` |
| TGA | Öffnungsrand | `OpeningLoop` |
| TGA | Bohrkörper | `DrillingCylinder` |
| Semantik | Fugenlinie | `AlignmentLine` |
| Semantik | Sichtfläche | `VisibilitySurface` |
| Logistik | Hebezone | `LiftingZone` |
| Logistik | Lagerauflagerzone | `StorageSupportZone` |
| Nachweis | Schadensfläche | `DamagePolygon` |

---

## 4.4 SharedConnectorPoint

Ein einzelner Punkt im Raum, der auf eine oder mehrere Host-Geometrien verweist.

Er enthält:

```text
Point3D
Richtung
lokaler Frame
Host-Feature
Facets
Evidence Modifiers
Status
```

Er ist der Ort des Andockens.

---

## 4.5 Facet

Ein Facet ist die paket-spezifische Bedeutung eines SharedConnectorPoints.

Beispiel:

```text
slab_edge_A_midpoint
│
├── StructuralFacet
├── SemanticFacet
├── EnergyFacet
└── LogisticsFacet
```

---

## 4.6 Port

Der Port ist der Kompatibilitätstyp innerhalb eines Facets.

Beispiele:

```text
bearing_side
support_side
alignment_port
bridge_side
route_side
opening_side
lifting_port
storage_port
visibility_port
```

Ports haben keine Geometrie.  
Sie definieren nur, welche Facets kompatibel sein können.

---

## 4.7 Evidence Modifier

Nachweise erzeugen keine Connectoren.  
Sie modifizieren Facets oder Connection Passports.

Beispiele:

```text
Rebar scan fehlt → StructuralFacet wird evidence_required.
Schaden überlagert Auflagerzone → StructuralFacet wird warning.
QR-Code vorhanden → Traceability wird confirmed.
Belastungstest vorhanden → StructuralFacet bekommt höhere Konfidenz.
```

---

# 5. Datenmodell

## 5.1 Component

```yaml
Component:
  id: string
  typology: string
  material: string

  base_geometry_ref: string

  package_representations:
    base_geometry: RepresentationRef
    structural: RepresentationRef
    energy: RepresentationRef
    tga: RepresentationRef
    semantic: RepresentationRef
    logistics: RepresentationRef
    evidence: RepresentationRef

  shared_connector_points:
    - SharedConnectorPoint
```

---

## 5.2 SharedConnectorPoint

```yaml
SharedConnectorPoint:
  id: string
  component_id: string

  family: support_edge_point | joint_line_point | opening_center_point |
          transfer_node_point | handling_point | visibility_reference_point |
          custom_point

  point: Point3D
  local_frame: CoordinateFrame3D
  direction: Vector3D
  host_feature_ref: string

  facets:
    structural: StructuralFacet optional
    energy: EnergyFacet optional
    tga: TGAFacet optional
    semantic: SemanticFacet optional
    logistics: LogisticsFacet optional

  evidence_modifiers:
    - EvidenceModifier

  global_status: active | warning | blocked | evidence_required | engineering_required
```

---

## 5.3 Facet

```yaml
Facet:
  package: structural | energy | tga | semantic | logistics
  port: string
  host_geometry_ref: string
  host_geometry_type: string
  active_checks:
    - string
  activation_condition: string optional
  status: active | inactive | warning | blocked | evidence_required | engineering_required
```

---

## 5.4 EvidenceModifier

```yaml
EvidenceModifier:
  evidence_ref: string
  evidence_type: rebar_scan | damage | material_test | qr_tracking |
                 loading_test | calculation | inspection | unknown_zone

  affected_facet: structural | energy | tga | semantic | logistics
  affected_host_geometry_ref: string optional

  effect: confirmed | warning | blocked | confidence_reduced |
          evidence_required | engineering_required

  reason: string
```

---

## 5.5 Connection Passport

```yaml
ConnectionPassport:
  id: string

  point_A: SharedConnectorPoint.id
  point_B: SharedConnectorPoint.id

  active_facets:
    structural: true | false
    energy: true | false
    tga: true | false
    semantic: true | false
    logistics: true | false

  checked_host_geometries:
    structural: []
    energy: []
    tga: []
    semantic: []
    logistics: []

  results:
    structural:
      status: pass | warning | fail | evidence_required | engineering_required
      messages: []

    energy:
      status: pass | warning | fail | context_required | not_applicable
      messages: []

    tga:
      status: pass | warning | fail | not_applicable
      messages: []

    semantic:
      status: pass | warning | fail | preference_dependent
      messages: []

    logistics:
      status: pass | warning | fail | evidence_required
      messages: []

    evidence:
      missing: []
      blocking: []
      warnings: []
```

---

# 6. Paket-Repräsentationen und Host-Geometrien

## 6.1 Basisgeometrie

Die Basisgeometrie erzeugt keine Connectoren.

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| neutraler Körper | `SolidMesh` oder `BRep` | digitale Ausgangsform |
| Bounding Box | `OrientedBoundingBox` | Maße, Orientierung, Transporthülle |
| Hauptflächen | `FaceSet` | Quelle für Energie, Semantik, Logistik |
| Hauptkanten | `EdgeSet` | Quelle für Tragwerk, Fuge, Ausrichtung |
| rohe Öffnungen | `OpeningLoop[]` | Quelle für TGA und Hülle |
| lokale Achsen | `CoordinateFrame3D` | Orientierung |

---

## 6.2 Tragwerk

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| Trägerachse | `LineElement1D` | Biegung, Querkraft, Knotenanschluss |
| Stützenachse | `LineElement1D` | Normalkraft, vertikale Last |
| Platte | `PlateElement2D` | Lastabtragung und Auflagerlogik |
| Wandscheibe | `WallPanel2D` | vertikale Scheiben- und Auflagerlogik |
| Auflagerpatch | `SupportPatch2D` | Auflagerüberlappung |
| Fugenlinie | `JointLine` | Fuge, Toleranz, Wiederverbindung |
| Ankerzone | `AnchorZone2D` | Randabstand, Bohrbarkeit, Rebar-Konflikt |
| Kontinuitätszone | `ContinuityZone` | Bewehrung, Verguss, Kraftschluss |
| Transferknoten | `TransferNode` | Lastübergang |
| Strukturgraph | `StructuralGraph` | Kombination aus Platte, Linie, Knoten |

---

## 6.3 Energie / Gebäudehülle

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| thermische Fläche | `ThermalSurface` | U-Wert- und Innen-/Außenbezug |
| Schicht | `Layer` | Dicke, Material, Wärmewiderstand |
| Rand | `BoundaryEdge` | Kontinuität an Anschluss |
| Dämmschnittstelle | `InsulationInterface` | Dämmkontinuität |
| Durchdringung | `PenetrationLoop` | Abdichtung |
| Wärmebrückenzone | `BridgeZone` | Wärmebrückenwarnung |
| Feuchterisikozone | `MoistureRiskZone` | Feuchterisiko |

---

## 6.4 TGA / Öffnungen

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| Route | `RouteLine` | Leitungsverlauf |
| Routenknoten | `RouteNode` | Übergang / Richtungswechsel |
| Öffnung | `OpeningLoop` | vorhandene Öffnung nutzen |
| Bohrung | `DrillingCylinder` | neue Durchdringung prüfen |
| Sperrzone | `BlockedZone` | Konfliktbereich |
| Lichtraum | `ClearanceVolume` | Platzbedarf |
| Schachtanschluss | `ShaftInterface` | vertikale Route |

---

## 6.5 Semantik / Architektur

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| Ausrichtungslinie | `AlignmentLine` | Raster, Fuge, Datum |
| Sichtfläche | `VisibilitySurface` | Sichtbarkeit, Verdeckung, Oberfläche |
| Zugangszone | `AccessZone` | Annäherung, Durchgang, Nische |
| Seitenregion | `SideRegion` | Raumseite, Fassadenseite, Orientierung |
| Stapel- / Niveaufläche | `StackPlane` | vertikale Beziehung |
| Öffnungsachse | `OpeningAxis` | architektonischer Öffnungsbezug |
| Raumgrenzenfläche | `SpatialBoundarySurface` | Raumabschluss |

---

## 6.6 Logistik / Montage

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| Transporthülle | `TransportEnvelope` | Transportmaße, Kollision |
| Schwerpunkt | `CenterOfGravityPoint` | Hebbarkeit, Stabilität |
| Hebezone | `LiftingZone` | Hebeplanung |
| Lagerauflager | `StorageSupportZone` | Lagerung, Stapelung |
| Transportauflager | `TransportSupportZone` | Ladungssicherung |
| Montagezugang | `AccessVolume` | Montage und Fügezugang |
| Schutzzone | `ProtectionZone` | Kanten-, Witterungs-, Oberflächenschutz |
| temporäre Abstützung | `TemporaryBracingZone` | Montagezustand |

---

## 6.7 Nachweis-Overlay

Nachweis-Overlay erzeugt keine SharedConnectorPoints, kann aber existierende Facets modifizieren.

| Abstrakte Geometrie | Datentyp | Zweck |
|---|---|---|
| Nachweiszone | `EvidenceZone` | räumlicher Nachweisbereich |
| Scanlinie | `ScanLine` | Bewehrung / Messlinie |
| Schadensfläche | `DamagePolygon` | Schadensüberlagerung |
| Risslinie | `CrackLine` | Rissverlauf |
| Prüfpunkt | `TestPoint` | Bohrkern, Karbonatisierung, Chloridprobe |
| unbekannte Zone | `UnknownZone` | fehlende Information |
| Konfidenzfeld | `ConfidenceField` | räumliche Zuverlässigkeit |
| Nachweisdatensatz | `EvidenceRecord` | nicht-geometrischer Nachweis, z. B. QR, Prüfbericht |

---

# 7. SharedConnectorPoint-Familien

Die Familien definieren **wo** strategische Punkte platziert werden.  
Sie ersetzen nicht die Paket-Facets.

---

## 7.1 `support_edge_point`

Ein Punkt auf einer tragenden oder potenziell tragenden Kante, Stirnseite oder Randzone.

Typische Host-Geometrien:

```text
SupportPatch2D
AlignmentLine
BridgeZone
AccessVolume
StorageSupportZone
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| StructuralFacet | `bearing_side` oder `support_side` | wenn Last über Auflagerung läuft |
| SemanticFacet | `alignment_port` | wenn Fuge / Raster / Datum relevant |
| EnergyFacet | `bridge_side` | wenn Hüllenkontext aktiv |
| LogisticsFacet | `access_port` oder `storage_port` | wenn Montage / Lagerung relevant |

Perfekt geeignet für:

```text
Plattenkante
Wandkopf
Trägeroberseite
Hohlkammerdecken-Stirnseite
```

---

## 7.2 `joint_line_point`

Ein Punkt auf einer Fuge, Modulachse oder Verbindungslinie.

Typische Host-Geometrien:

```text
JointLine
AlignmentLine
BoundaryEdge
AccessVolume
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| StructuralFacet | `member_side` | wenn Fuge tragend oder verbindend ist |
| SemanticFacet | `alignment_port` | wenn Fuge / Modul / Rhythmus relevant |
| EnergyFacet | `thermal_side` | wenn Hüllenfuge |
| LogisticsFacet | `access_port` | wenn Montagezugang zur Fuge nötig |

Perfekt geeignet für:

```text
Hohlkammerdecken-Längsfuge
Platte-Platte-Fuge
Wand-Wand-Fuge
Fassadenfuge
```

---

## 7.3 `opening_center_point`

Ein Punkt im Zentrum einer Öffnung, eines Hohlraums, einer Durchdringung oder eines Bohrkandidaten.

Typische Host-Geometrien:

```text
OpeningLoop
RouteLine
DrillingCylinder
PenetrationLoop
OpeningAxis
BlockedZone
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| TGAFacet | `opening_side`, `route_side` oder `drilling_side` | wenn Route / Öffnung / Bohrung genutzt wird |
| EnergyFacet | `penetration_side` | wenn Hülle durchdrungen wird |
| SemanticFacet | `opening_port` | wenn Öffnung architektonisch relevant |
| StructuralFacet | warning / evidence only | wenn nahe Auflager / Tragzone |

Perfekt geeignet für:

```text
bestehende Öffnung
Schachtöffnung
geplante Kernbohrung
Hohlkammer als Route
```

---

## 7.4 `transfer_node_point`

Ein Punkt, an dem Lasten, Teilgeometrien oder räumliche Bedeutungen zusammenlaufen.

Typische Host-Geometrien:

```text
TransferNode
StructuralGraph
SideRegion
AlignmentLine
BridgeZone
TemporaryBracingZone
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| StructuralFacet | `transfer_side` | wenn Lastpfad über den Knoten läuft |
| SemanticFacet | `side_port` oder `alignment_port` | wenn Knoten räumlich / architektonisch relevant |
| EnergyFacet | `bridge_side` | wenn Knoten an Hülle liegt |
| LogisticsFacet | `temporary_bracing_port` | wenn temporäre Stabilisierung nötig |
| EvidenceModifier | — | wenn Schaden / Rebar / Unsicherheit vorliegt |

Perfekt geeignet für:

```text
SlabBeamColumnFragment-Knoten
Träger-Stützen-Knoten
Stützenkopf
Pilzkopfstütze
```

---

## 7.5 `handling_point`

Ein Punkt für Heben, Lagern, Transport, Schutz oder temporäre Montage.

Typische Host-Geometrien:

```text
LiftingZone
StorageSupportZone
TransportEnvelope
TransportSupportZone
ProtectionZone
TemporaryBracingZone
CenterOfGravityPoint
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| LogisticsFacet | `lifting_port`, `storage_port`, `transport_port`, `protection_port`, `temporary_bracing_port` | wenn Handling geprüft wird |
| StructuralFacet | `support_side`, optional | wenn Handling-Auflager auch strukturell relevant ist |
| EvidenceModifier | — | wenn Hebe- oder Schadensnachweis fehlt |

Perfekt geeignet für:

```text
Hebekandidat
Lagerauflagerpunkt
Transportauflagerpunkt
Schutzpunkt an Schnittkante
temporäre Abstützung
```

---

## 7.6 `visibility_reference_point`

Ein Punkt, der Sichtbarkeit, Lesbarkeit oder Wiederverwendungsausdruck prüfbar macht.

Typische Host-Geometrien:

```text
VisibilitySurface
DamagePolygon
EvidenceZone
```

Typische Facets:

| Facet | Port | Aktivierung |
|---|---|---|
| SemanticFacet | `visibility_port` | wenn Sichtbarkeit Entwurfsziel ist |
| EvidenceModifier | — | wenn Oberfläche / Schaden / Markierung nachgewiesen wird |

Perfekt geeignet für:

```text
sichtbare Plattenuntersicht
sichtbare Schnittfläche
sichtbare Bauteil-ID
sichtbarer ReUse-Ausdruck
```

Nur erzeugen, wenn Sichtbarkeit wirklich geprüft wird.

---

# 8. Platzierungsregeln

## 8.1 Punkte erzeugen, wenn

Ein SharedConnectorPoint wird erzeugt, wenn mindestens eine Bedingung erfüllt ist:

```text
Er verbindet zwei Bauteile.
Er startet oder empfängt eine Berechnung.
Er trägt eine Warnung.
Er steuert Ausrichtung, Sichtbarkeit, Zugang oder Raumbezug.
Er beeinflusst Heben, Lagerung, Transport oder Montage.
Er wird durch Nachweise modifiziert.
```

---

## 8.2 Punkte nicht erzeugen, wenn

```text
Es nur eine geometrische Beschreibung ist.
Keine Regel den Punkt nutzt.
Keine Verbindung möglich ist.
Keine Warnung oder Berechnung ausgelöst wird.
Er nur eine Fläche oder Kante dupliziert.
```

---

## 8.3 Punkte zusammenführen, wenn

```text
Distanz < Toleranz
gleiche reale Stelle
Host-Geometrien kompatibel
Facets sich sinnvoll ergänzen
keine Sicherheitsregel getrennte Punkte verlangt
```

Beispiel:

```text
Plattenkante:
Structural bearing point
+ Semantic alignment point
+ Energy bridge point
→ ein support_edge_point
```

---

## 8.4 Punkte nicht zusammenführen, wenn

```text
einer oben und einer unten liegt
einer innen und einer außen liegt
einer Heben und einer strukturelles Auflager bewusst trennt
Sicherheitsregeln unterschiedliche Positionen verlangen
unterschiedliche Bauzustände getrennt werden müssen
```

---

## 8.5 Qualitätsregel

```text
1 Facet  = erlaubt, aber prüfen ob nötig
2 Facets = gut
3+ Facets = sehr guter strategischer SharedConnectorPoint
```

---

# 9. Docking- und Prüfablauf

## 9.1 User verbindet zwei Punkte

```text
SharedConnectorPoint A
dockt an
SharedConnectorPoint B
```

## 9.2 System prüft räumliches Docking

```text
Punktnähe
Richtung
Toleranz
lokale Frames
Snap / Transform
```

## 9.3 System findet kompatible Facets

Beispiel:

```text
A.StructuralFacet.port = bearing_side
B.StructuralFacet.port = support_side
→ Structural Check aktiv

A.SemanticFacet.port = alignment_port
B.SemanticFacet.port = alignment_port
→ Semantic Check aktiv

A.EnergyFacet.port = bridge_side
B.EnergyFacet.port = thermal_side
→ Energy Warning aktiv
```

## 9.4 System lädt Host-Geometrien

```text
Structural:
SupportPatch2D A + SupportPatch2D B

Semantic:
AlignmentLine A + AlignmentLine B

Energy:
BridgeZone A + BoundaryEdge B

Logistics:
AccessVolume A + AccessVolume B
```

## 9.5 System führt Checks aus

```text
Tragwerk:
Auflagerüberlappung, Richtung, Mindestauflager, Anker, Kontinuität

Energie:
Wärmebrücke, Dämmkontinuität, Luftdichtheit, Feuchte

TGA:
Route, Öffnung, Bohrung, Konflikt

Semantik:
Ausrichtung, Sichtbarkeit, Zugang, Raumbezug

Logistik:
Heben, Lagerung, Transport, Montagezugang

Nachweis:
Bewehrung, Schaden, Test, QR, fehlende Evidenz
```

## 9.6 Ergebnis

Ein gemeinsamer Connection Passport speichert alle Resultate.

---

# 10. Paket-Facets und minimale Ports

## 10.1 StructuralFacet

| Port | Bedeutung | Host-Geometrie |
|---|---|---|
| `bearing_side` | Bauteil gibt Last über Auflager ab | `SupportPatch2D` |
| `support_side` | Bauteil nimmt Last auf | `SupportPatch2D` / `Node` |
| `member_side` | Fuge / Bauteilseite wird verbunden | `JointLine` |
| `anchor_side` | Anker / Schraube / Dorn / Bohrung | `AnchorZone2D` |
| `continuity_side` | Kraftschluss / Bewehrung / Verguss | `ContinuityZone` |
| `transfer_side` | Lasttransfer über Knoten / Zwischenstruktur | `TransferNode` / `StructuralGraph` |

---

## 10.2 EnergyFacet

| Port | Bedeutung | Host-Geometrie |
|---|---|---|
| `thermal_side` | thermische Grenze | `ThermalSurface` / `BoundaryEdge` |
| `insulation_side` | Dämmschicht | `InsulationInterface` |
| `penetration_side` | Hüllendurchdringung | `PenetrationLoop` |
| `bridge_side` | Wärmebrückenwarnung | `BridgeZone` |

---

## 10.3 TGAFacet

| Port | Bedeutung | Host-Geometrie |
|---|---|---|
| `route_side` | Leitungsverlauf | `RouteLine` |
| `opening_side` | bestehende Öffnung | `OpeningLoop` |
| `drilling_side` | neue Bohrung / Kernbohrung | `DrillingCylinder` |
| `blocked_side` | Konfliktzone | `BlockedZone` |

---

## 10.4 SemanticFacet

| Port | Bedeutung | Host-Geometrie |
|---|---|---|
| `access_port` | Zugang / Annäherung | `AccessZone` |
| `attachment_port` | architektonische Anbindung | `SideRegion` / custom |
| `top_port` | obere Stapel- / Niveaufläche | `StackPlane` |
| `bottom_port` | untere Stapel- / Niveaufläche | `StackPlane` |
| `side_port` | Raumseite / Orientierung | `SideRegion` |
| `opening_port` | architektonische Öffnung | `OpeningAxis` |
| `alignment_port` | Raster / Fuge / Datum | `AlignmentLine` |
| `visibility_port` | Sichtbarkeit / Verdeckung | `VisibilitySurface` |

---

## 10.5 LogisticsFacet

| Port | Bedeutung | Host-Geometrie |
|---|---|---|
| `lifting_port` | Heben | `LiftingZone` |
| `storage_port` | Lagerung | `StorageSupportZone` |
| `transport_port` | Transport | `TransportEnvelope` / `TransportSupportZone` |
| `access_port` | Montagezugang | `AccessVolume` |
| `protection_port` | Schutz | `ProtectionZone` |
| `temporary_bracing_port` | temporäre Stabilisierung | `TemporaryBracingZone` |

---

# 11. Kompatibilitätsregeln

| Regel | Punkt-Port-Docking | Host-Geometrie-Check |
|---|---|---|
| strukturelles Auflager | `bearing_side → support_side` | `SupportPatch2D`-Überlappung, Richtung, Auflagerlänge |
| strukturelle Verankerung | `anchor_side → support_side` | `AnchorZone2D`, Randabstand, Bewehrung |
| strukturelle Kontinuität | `continuity_side → continuity_side` | `ContinuityZone`, Verguss, Bewehrung |
| strukturelle Fuge | `member_side → member_side` | `JointLine`, Ausrichtung, Toleranz |
| struktureller Transfer | `transfer_side → support_side / bearing_side` | `StructuralGraph`, `TransferNode`, Lastpfad |
| thermische Kontinuität | `thermal_side → thermal_side` | `BoundaryEdge`, `ThermalSurface` |
| Dämmkontinuität | `insulation_side → insulation_side` | `InsulationInterface`, Lücken |
| Hüllendurchdringung | `penetration_side → thermal_side / insulation_side` | `PenetrationLoop`, Luftdichtheit, Feuchte |
| Wärmebrücke | `bridge_side` | `BridgeZone`, Kontextwarnung |
| TGA-Route | `route_side → route_side` | `RouteLine`, `ClearanceVolume` |
| TGA-Öffnung | `opening_side → route_side` | `OpeningLoop`, Durchmesser, Randabstand |
| TGA-Bohrung | `drilling_side → route_side` | `DrillingCylinder`, Bewehrung, Tragwerkszone |
| TGA-Konflikt | `blocked_side` | `BlockedZone` gegen Route / Bohrung |
| architektonischer Zugang | `access_port → access_port` | `AccessZone`, Lichtraum |
| architektonische Stapelung | `top_port → bottom_port` | `StackPlane`, Niveau |
| architektonische Ausrichtung | `alignment_port → alignment_port` | `AlignmentLine`, Raster, Fuge |
| Sichtbarkeit | `visibility_port` | `VisibilitySurface`, Verdeckung, Oberflächenzustand |
| Logistik Heben | `lifting_port → Prozessanforderung` | `LiftingZone`, Schwerpunkt |
| Logistik Lagerung | `storage_port → Lagerbedingung` | `StorageSupportZone`, Orientierung |
| Logistik Transport | `transport_port → Transportanforderung` | `TransportEnvelope`, Ladungssicherung |
| Montagezugang | `access_port → Prozessanforderung` | `AccessVolume`, Zugänglichkeit |
| Schutz | `protection_port → Schutzanforderung` | `ProtectionZone`, Schaden / Witterung |
| temporäre Stabilisierung | `temporary_bracing_port → Montageanforderung` | `TemporaryBracingZone`, Stabilität |

---

# 12. Beispiel A — Abbau/Aufbau DE_1OG_001

## 12.1 Komponente

```text
ID: DE_1OG_001
Typologie: Deckenplatte
Material: Stahlbeton
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

---

## 12.2 Paket-Repräsentationen

| Paket | Repräsentation | Host-Geometrien |
|---|---|---|
| Basisgeometrie | neutraler Plattenkörper | `SolidMesh`, `OrientedBoundingBox`, `FaceSet`, `EdgeSet` |
| Tragwerk | `PlateElement2D` | `SupportPatch2D`, `AnchorZone2D`, `ContinuityZone` |
| Energie | aktiv bei Hüllennutzung | `ThermalSurface`, `BridgeZone`, `InsulationInterface`, `PenetrationLoop` |
| TGA | aktiv bei Öffnung / Route / Bohrung | `OpeningLoop`, `RouteLine`, `DrillingCylinder` |
| Semantik | architektonisches Plattenmodell | `AlignmentLine`, `VisibilitySurface`, `StackPlane` |
| Logistik | Handlingmodell | `TransportEnvelope`, `StorageSupportZone`, `LiftingZone`, `ProtectionZone` |
| Nachweis | Overlay | `ScanLine`, `DamagePolygon`, `UnknownZone`, `EvidenceRecord` |

---

## 12.3 Perfekt platzierte minimale SharedConnectorPoints

Für `DE_1OG_001` reichen typischerweise diese Punkte:

```text
1. slab_edge_A_midpoint
2. slab_edge_B_midpoint
3. slab_visibility_reference
4. slab_lifting_reference
5. slab_storage_reference
6. slab_opening_center, nur falls Öffnung / Route relevant
```

Nicht erzeugen:

```text
Connectoren auf jeder Fläche
Connectoren auf jeder Kante
separate Energie-/Semantik-/Tragwerks-Punkte auf derselben Kante
```

---

## 12.4 Punkt 1 — `slab_edge_A_midpoint`

**Familie:** `support_edge_point`  
**Position:** Mittelpunkt der langen Plattenkante A  
**Warum perfekt platziert?**  
Diese eine reale Stelle deckt Auflagerung, Fuge / Raster, mögliche Wärmebrücke und Montagezugang ab.

| Facet | Port | Host-Geometrie | Aktivierung | Check |
|---|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | wenn Kante auf Wand / Träger aufliegt | Auflagerüberlappung, Richtung, Mindestauflager |
| StructuralFacet optional | `anchor_side` | `AnchorZone2D` | wenn Schraubanker / Flachstahlhalter verwendet wird | Randabstand, Bewehrung, Ankerbarkeit |
| StructuralFacet optional | `continuity_side` | `ContinuityZone` | wenn Bewehrungsanschluss + Verguss verwendet wird | Kraftschluss, Vergussraum, Bewehrung |
| SemanticFacet | `alignment_port` | `AlignmentLine` | wenn Fuge / Raster relevant | Fugen- und Rasterausrichtung |
| EnergyFacet | `bridge_side` | `BridgeZone` | nur bei Hüllenkontext | Wärmebrückenwarnung |
| LogisticsFacet | `access_port` | `AccessVolume` | bei Montageprüfung | Montagezugang |

---

## 12.5 Punkt 2 — `slab_edge_B_midpoint`

Gleich wie `slab_edge_A_midpoint`, aber auf der gegenüberliegenden Kante.  
Er ist nötig, wenn die Platte auf zwei Linien gelagert wird oder wenn beide Längskanten im Raster / Fugenbild relevant sind.

---

## 12.6 Punkt 3 — `slab_visibility_reference`

**Familie:** `visibility_reference_point`  
**Position:** Referenzpunkt auf der Plattenunterseite  
**Nur erzeugen, wenn die Untersicht sichtbar bleiben oder bewertet werden soll.**

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| SemanticFacet | `visibility_port` | `VisibilitySurface` | Sichtbarkeit, Verdeckung, Oberflächenzustand |
| EvidenceModifier | — | `DamagePolygon` / `EvidenceZone` | Schaden oder Oberflächenqualität beeinflusst Sichtbarkeit |

---

## 12.7 Punkt 4 — `slab_lifting_reference`

**Familie:** `handling_point`  
**Position:** Hebekandidat oder Schwerpunktnähe  
**Nur erzeugen, wenn Heben geprüft wird.**

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Hebbarkeit, Schwerpunkt, Hebe-Nachweis |
| EvidenceModifier | — | `EvidenceRecord` | Hebe-/Transportnachweis fehlt oder bestätigt |

---

## 12.8 Punkt 5 — `slab_storage_reference`

**Familie:** `handling_point`  
**Position:** Lagerauflagerpunkt / Unterseite  
**Warum separat vom Hebepunkt?**  
Lagerung und Heben können unterschiedliche reale Positionen erfordern.

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| LogisticsFacet | `storage_port` | `StorageSupportZone` | liegende Lagerung, Lagerhölzer, Auflagerabstand |
| LogisticsFacet optional | `protection_port` | `ProtectionZone` | Kanten- / Witterungsschutz |

---

## 12.9 Punkt 6 — `slab_opening_center`

**Familie:** `opening_center_point`  
**Nur erzeugen, wenn Öffnung existiert oder Route / Bohrung vorgeschlagen wird.**

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| TGAFacet | `opening_side` | `OpeningLoop` | Öffnung nutzbar? Durchmesser? Randabstand? |
| TGAFacet optional | `drilling_side` | `DrillingCylinder` | neue Bohrung möglich? |
| EnergyFacet optional | `penetration_side` | `PenetrationLoop` | Abdichtung bei Hüllennutzung |
| StructuralFacet warning | — | `BlockedZone` / `SupportPatch2D` | Konflikt mit Tragwerkszone |

---

## 12.10 Verbindung: Decke–Wand

```text
slab_edge_A_midpoint
dockt an
wall_top_midpoint
```

Aktive Checks:

| Paket | Ergebnislogik |
|---|---|
| Tragwerk | `SupportPatch2D`-Überlappung, Mindestauflager, ggf. Anker oder Kontinuität |
| Energie | Wärmebrücke, falls Hüllenkontext |
| Semantik | Fuge / Raster / Datum |
| Logistik | Montagezugang |
| Nachweis | Bewehrung, Schaden, fehlende Ankerfreigabe |

Abbau/Aufbau-Anschlussfamilien werden so abgebildet:

| Abbau/Aufbau-Detail | System-Facet |
|---|---|
| Schraubanker mit Flachstahlhalter | StructuralFacet `anchor_side` |
| nachträglicher Bewehrungsanschluss + Verguss | StructuralFacet `continuity_side` |
| Brandschutzbekleidung bei Stahlteilen | Energy / Fire Warning über Kontext, nicht eigener Punkt |

---

# 13. Beispiel B — SlabBeamColumnFragment

## 13.1 Komponente

```text
SlabBeamColumnFragment
= monolithisches Betonfragment mit:
  - Plattenbereich
  - integriertem Trägerbereich
  - Stützenabschnitt
  - Schnittflächen
  - räumlicher Fragmentqualität
```

---

## 13.2 Paket-Repräsentationen

| Paket | Repräsentation | Host-Geometrien |
|---|---|---|
| Basisgeometrie | monolithischer Körper mit Teilregionen | `SolidMesh`, `VolumeRegion`, `FaceSet` |
| Tragwerk | `StructuralGraph` | `PlateElement2D`, `LineElement1D`, `TransferNode`, `ContinuityZone` |
| Energie | nur bei Hüllennutzung | `ThermalSurface`, `BoundaryEdge`, `BridgeZone` |
| TGA | Bohr- und Sperrzonenmodell | `DrillingCylinder`, `BlockedZone` |
| Semantik | architektonisches Fragmentmodell | `AccessZone`, `SideRegion`, `AlignmentLine`, `VisibilitySurface` |
| Logistik | komplexes Handlingmodell | `CenterOfGravityPoint`, `LiftingZone`, `StorageSupportZone`, `ProtectionZone`, `TemporaryBracingZone` |
| Nachweis | Schnittflächen-, Rebar-, Schadensoverlay | `EvidenceZone`, `ScanLine`, `DamagePolygon`, `UnknownZone` |

---

## 13.3 Perfekt platzierte minimale SharedConnectorPoints

Für das Fragment reichen typischerweise diese Punkte:

```text
1. fragment_transfer_node
2. fragment_cut_face_point
3. fragment_plate_edge_point
4. fragment_column_base_or_head_point
5. fragment_niche_access_point
6. fragment_lifting_reference
```

Diese Punkte sind strategisch, weil sie jeweils mehrere Paketrollen bündeln.

---

## 13.4 Punkt 1 — `fragment_transfer_node`

**Familie:** `transfer_node_point`  
**Position:** Schnittpunkt von Plattenbereich, Trägerbereich und Stützenabschnitt  
**Warum perfekt platziert?**  
Hier bündeln sich Lastpfad, räumliche Bedeutung, mögliche Wärmebrücke und Montageinstabilität.

| Facet | Port | Host-Geometrie | Aktivierung | Check |
|---|---|---|---|---|
| StructuralFacet | `transfer_side` | `StructuralGraph` + `TransferNode` | immer bei struktureller Nutzung | Lastpfad Platte → Trägerlinie → Stützenlinie |
| SemanticFacet | `side_port` oder `alignment_port` | `SideRegion` / `AlignmentLine` | wenn räumliche Schwelle / Orientierung relevant | Raumbezug, Ausrichtung |
| EnergyFacet | `bridge_side` | `BridgeZone` | nur bei Hüllennutzung | Wärmebrückenwarnung |
| LogisticsFacet | `temporary_bracing_port` | `TemporaryBracingZone` | wenn Montagezustand instabil | temporäre Stabilisierung |
| EvidenceModifier | — | `DamagePolygon`, `ScanLine`, `UnknownZone` | wenn Bewehrung / Schaden unklar | Konfidenz, Warnung, Engineering Required |

---

## 13.5 Punkt 2 — `fragment_cut_face_point`

**Familie:** `visibility_reference_point` + `handling_point` + strukturelle Kontinuität  
**Position:** relevante Schnittfläche  
**Warum perfekt platziert?**  
Die Schnittfläche ist gleichzeitig struktureller Anschluss, sichtbarer ReUse-Ausdruck, Schutzbereich und Nachweisrisiko.

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `continuity_side` | `ContinuityZone` | Kraftschluss, Verguss, Bewehrung |
| SemanticFacet | `visibility_port` | `VisibilitySurface` | sichtbare Schnittfläche, ReUse-Ausdruck |
| LogisticsFacet | `protection_port` | `ProtectionZone` | Schutz der Schnittkante |
| EvidenceModifier | — | `ScanLine`, `DamagePolygon`, `UnknownZone` | Rebar-Status, Schaden, Unsicherheit |

---

## 13.6 Punkt 3 — `fragment_plate_edge_point`

**Familie:** `support_edge_point`  
**Position:** Rand des Plattenbereichs

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | Auflagerung des Plattenbereichs |
| SemanticFacet | `alignment_port` | `AlignmentLine` | Kante als Fuge / Raster / Datum |
| EnergyFacet optional | `bridge_side` | `BridgeZone` | wenn Hüllenkante |
| LogisticsFacet optional | `access_port` | `AccessVolume` | Montagezugang |

---

## 13.7 Punkt 4 — `fragment_column_base_or_head_point`

**Familie:** `support_edge_point` oder `transfer_node_point`  
**Position:** Stützenfuß oder Stützenkopf

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `support_side` | `Node` / `SupportPatch2D` | Lastaufnahme oder Lastabgabe |
| LogisticsFacet | `temporary_bracing_port` | `TemporaryBracingZone` | Stabilität während Montage |
| EvidenceModifier | — | `DamagePolygon` / `UnknownZone` | Schaden / Unsicherheit |

---

## 13.8 Punkt 5 — `fragment_niche_access_point`

**Familie:** `visibility_reference_point` / `access`  
**Position:** Zugang zur Nische oder räumlichen Schwelle

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| SemanticFacet | `access_port` | `AccessZone` | Lichtraum, Annäherung, Raumzugang |
| SemanticFacet optional | `side_port` | `SideRegion` | Stütze-Raum-Beziehung |
| EvidenceModifier optional | — | `DamagePolygon` | sichtbarer Schaden |

---

## 13.9 Punkt 6 — `fragment_lifting_reference`

**Familie:** `handling_point`  
**Position:** Hebekandidat, abhängig vom Schwerpunkt

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Hebbarkeit, Schwerpunkt, Kran |
| LogisticsFacet optional | `storage_port` | `StorageSupportZone` | Lagerung |
| EvidenceModifier | — | `EvidenceRecord` | Hebe-/Materialnachweis |

---

## 13.10 Verbindung: Fragment auf neuem Träger

```text
fragment_cut_face_point
oder
fragment_plate_edge_point
dockt an
new_precast_beam_support_point
```

Aktive Checks:

| Paket | Check |
|---|---|
| Tragwerk | Kontinuität, Auflagerung, Lasttransfer |
| Semantik | Ausrichtung des Fragments / räumliche Wirkung |
| Logistik | Montagezugang, temporäre Stabilisierung |
| Nachweis | Schnittflächenbewehrung, Schaden, Engineering Required |
| Energie | nur bei Hüllennutzung |

---

# 14. Beispiel C — ReCreate Hollow-Core Slab

## 14.1 Komponente

```text
ReCreate Hollow-Core Slab
= wiedergewonnene Hohlkammerdecke
mit:
  - einachsiger Spannrichtung
  - Stirnauflagerzonen
  - Längsfugen
  - Hohlkammern
  - Hebe-, Transport- und Trackinghistorie
```

---

## 14.2 Paket-Repräsentationen

| Paket | Repräsentation | Host-Geometrien |
|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | `BRep`, `SolidMesh`, `VoidVolume[]`, `OpeningLoop[]` |
| Tragwerk | einachsig spannende Platte | `PlateElement2D`, `SupportPatch2D`, `JointLine` |
| Energie | aktiv bei Dach / Außenboden | `ThermalSurface`, `InsulationInterface`, `BridgeZone`, `PenetrationLoop` |
| TGA | Hohlraum- oder Bohrmodell | `RouteLine`, `DrillingCylinder`, `BlockedZone` |
| Semantik | Modul- und Fugenausrichtungsmodell | `AlignmentLine`, `StackPlane`, `VisibilitySurface` |
| Logistik | Hebe-, Transport- und Lagermodell | `LiftingZone`, `TransportEnvelope`, `StorageSupportZone` |
| Nachweis | BIM / QR / Test / Neuberechnung | `EvidenceRecord`, `TestPoint`, `ConfidenceField`, `DamagePolygon` |

---

## 14.3 Perfekt platzierte minimale SharedConnectorPoints

Für eine Hohlkammerdecke reichen typischerweise:

```text
1. hcs_end_A_midpoint
2. hcs_end_B_midpoint
3. hcs_long_joint_midpoint
4. hcs_void_route_point, nur wenn Hohlraum als Route genutzt wird
5. hcs_lifting_reference
6. hcs_qr_reference, nur wenn räumliches Tracking sichtbar / prüfbar sein soll
```

---

## 14.4 Punkt 1 — `hcs_end_A_midpoint`

**Familie:** `support_edge_point`  
**Position:** Mittelpunkt der Stirnauflagerzone A  
**Warum perfekt platziert?**  
Der Punkt bündelt Endauflager, Transport / Lagerung, Modulbezug und mögliche Wärmebrücke.

| Facet | Port | Host-Geometrie | Aktivierung | Check |
|---|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | immer bei Wiederverwendung als Decke | Endauflager |
| LogisticsFacet | `transport_port` oder `storage_port` | `TransportSupportZone` / `StorageSupportZone` | bei Transport / Lagerung | Ladungssicherung, Lagerauflager |
| SemanticFacet | `alignment_port` | `AlignmentLine` | wenn Modul / Fuge relevant | Modulausrichtung |
| EnergyFacet | `bridge_side` | `BridgeZone` | wenn Dach / Außenboden | Wärmebrückenwarnung |

---

## 14.5 Punkt 2 — `hcs_end_B_midpoint`

Gleich wie `hcs_end_A_midpoint`, aber an der zweiten Stirnseite.

Er ist notwendig, weil eine einachsig spannende Hohlkammerdecke zwei Endauflager benötigt.

---

## 14.6 Punkt 3 — `hcs_long_joint_midpoint`

**Familie:** `joint_line_point`  
**Position:** Mittelpunkt der Längsfuge

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `member_side` | `JointLine` | Längsfugenverbindung, Toleranz |
| SemanticFacet | `alignment_port` | `AlignmentLine` | Fugen- und Modulraster |
| EnergyFacet optional | `thermal_side` | `BoundaryEdge` | thermische Kontinuität bei Hüllenfuge |
| LogisticsFacet optional | `access_port` | `AccessVolume` | Montagezugang zur Fuge |

---

## 14.7 Punkt 4 — `hcs_void_route_point`

**Familie:** `opening_center_point`  
**Nur erzeugen, wenn ein Hohlraum tatsächlich als Route genutzt wird.**

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| TGAFacet | `route_side` | `RouteLine` | Leitungsführung im Hohlraum |
| TGAFacet optional | `drilling_side` | `DrillingCylinder` | Durchdringung zum Hohlraum |
| EnergyFacet optional | `penetration_side` | `PenetrationLoop` | Abdichtung bei Hüllennutzung |
| StructuralFacet warning | — | `BlockedZone` | Konflikt mit Tragwerk / Rebar |

---

## 14.8 Punkt 5 — `hcs_lifting_reference`

**Familie:** `handling_point`  
**Position:** Hebekandidat / Hebezone

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Hebbarkeit, Schwerpunkt, Beschädigungsrisiko |
| EvidenceModifier | — | `EvidenceRecord` | Hebe- / Transportnachweis |

---

## 14.9 Punkt 6 — `hcs_qr_reference`

**Familie:** `visibility_reference_point` oder `custom_point`  
**Nur erzeugen, wenn räumliche Rückverfolgbarkeit im Interface oder auf dem Bauteil relevant ist.**

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| SemanticFacet optional | `visibility_port` | `VisibilitySurface` | QR / ID sichtbar oder nicht verdeckt |
| EvidenceModifier | — | `EvidenceRecord` | QR bestätigt Identität / Tracking |

---

## 14.10 Verbindung: Hohlkammerdecke auf Auflager

```text
hcs_end_A_midpoint
dockt an
support_wall_or_beam_point
```

Aktive Checks:

| Paket | Check |
|---|---|
| Tragwerk | Endauflager, Auflagerlänge, Toleranz |
| Logistik | Montage- und Transportstatus |
| Semantik | Modulausrichtung, falls aktiv |
| Energie | Wärmebrücke, falls Hüllenkontext |
| Nachweis | Test, Neuberechnung, QR / Tracking |

---

# 15. Interface-Logik

## 15.1 Bauteilmodus

Im Bauteilpass zeigt das Interface pro Komponente nur wenige strategische Punkte.

Für jeden Punkt sichtbar:

```text
Name
Familie
Position
aktive Facets
Ports je Facet
Host-Geometrien
Status
fehlende Nachweise
mögliche Verbindungspartner
```

Beispiel:

```text
slab_edge_A_midpoint

Facets:
- Structural: bearing_side, anchor_side optional, continuity_side optional
- Semantic: alignment_port
- Energy: bridge_side, context required
- Logistics: access_port

Status:
- Structural: evidence required
- Semantic: ready
- Energy: inactive until envelope
- Logistics: ready
```

---

## 15.2 Verbindungsmodus

Beim Verbinden zweier Punkte zeigt das Interface:

```text
Docking OK / nicht OK
Structural Check
Energy Check
TGA Check
Semantic Check
Logistics Check
Evidence Status
```

Das Ergebnis ist kein einzelnes „valid / invalid“, sondern ein mehrschichtiger Verbindungszustand.

---

## 15.3 Warnlogik

Warnungen werden nicht global und unklar ausgegeben, sondern facet-bezogen:

```text
StructuralFacet:
Bewehrung fehlt für anchor_side

EnergyFacet:
Wärmebrücke prüfen

SemanticFacet:
Fuge nicht im Raster

LogisticsFacet:
Montagezugang blockiert

Evidence:
Schaden überlagert SupportPatch2D
```

---

# 16. Warum die Punkte jetzt korrekt platziert sind

## 16.1 Sie sitzen an realen Entscheidungspunkten

Die Punkte liegen nicht zufällig auf Flächen, sondern an Stellen, an denen Entscheidungen entstehen:

```text
Auflagerkante
Fuge
Öffnung
Transferknoten
Schnittfläche
Hebepunkt
Sichtreferenz
```

---

## 16.2 Sie bündeln mehrere Paketrollen

Ein guter SharedConnectorPoint trägt nicht nur eine Funktion.

Beispiel Plattenkante:

```text
Tragwerk: Auflager
Semantik: Fuge / Raster
Energie: Wärmebrücke
Logistik: Montagezugang
```

---

## 16.3 Sie vermeiden doppelte Punkte

Statt vier Punkte auf derselben Kante:

```text
structural point
semantic point
energy point
logistics point
```

gibt es einen Punkt mit vier Facets.

---

## 16.4 Sie behalten die fachliche Genauigkeit

Die Punktlogik reduziert nicht die Prüfqualität, weil die Host-Geometrien erhalten bleiben:

```text
Punkt dockt.
SupportPatch2D wird geprüft.
AlignmentLine wird geprüft.
BridgeZone wird geprüft.
AccessVolume wird geprüft.
```

---

## 16.5 Sie sind skalierbar

Neue Pakete können später als neue Facets ergänzt werden, ohne neue Geometriepunkte zu erzeugen.

Beispiel:

```text
FireFacet
CostFacet
LCAFacet
RegulationFacet
```

Diese könnten an bestehende SharedConnectorPoints andocken, wenn sie dort sinnvoll sind.

---

# 17. Finale Systemregel

```text
Connectoren sind immer Punkte.
```

Aber:

```text
Punkte sind nur Docking-Handles.
Die fachliche Bedeutung liegt in Facets.
Die fachliche Prüfung liegt in Host-Geometrien.
Das Ergebnis liegt im Connection Passport.
```

Die finale Struktur lautet:

```text
Component
→ Package Representations
→ Host-Geometrien
→ wenige SharedConnectorPoints
→ Facets mit Ports
→ Docking zwischen Punkten
→ Checks über Host-Geometrien
→ Connection Passport
```

Die wichtigste Kurzform:

```text
Ein Punkt.
Mehrere Facets.
Eine Verbindung.
Viele Checks.
```

---

# 18. Praktische Implementierungsreihenfolge

## Schritt 1 — Basisgeometrie importieren

```text
SolidMesh / BRep
FaceSet
EdgeSet
OpeningLoop
OrientedBoundingBox
CoordinateFrame
```

---

## Schritt 2 — Paket-Repräsentationen erzeugen

```text
StructuralGraph
ThermalSurface
RouteLine
AlignmentLine
TransportEnvelope
EvidenceOverlay
```

---

## Schritt 3 — Kandidatenpunkte erzeugen

```text
Kantenmittelpunkte
Fugenmittelpunkte
Öffnungszentren
Transferknoten
Schnittflächenpunkte
Hebekandidaten
Lagerauflagerpunkte
Sichtreferenzen
```

---

## Schritt 4 — Facets anhängen

```text
liegt auf SupportPatch2D → StructuralFacet
liegt auf AlignmentLine → SemanticFacet
liegt auf BridgeZone → EnergyFacet
liegt auf OpeningLoop → TGAFacet
liegt auf LiftingZone → LogisticsFacet
wird von EvidenceZone überlagert → EvidenceModifier
```

---

## Schritt 5 — Punkte zusammenführen

```text
räumlich nahe
gleiche reale Stelle
kompatible Host-Geometrien
kein Sicherheitsgrund zur Trennung
```

---

## Schritt 6 — inaktive Punkte löschen

```text
keine Facets
keine Checks
keine Warnungen
keine Verbindungen
→ löschen
```

---

## Schritt 7 — Verbindungspässe erzeugen

Jede User-Verbindung zwischen zwei Punkten erzeugt einen Connection Passport mit allen aktiven Facet-Checks.

---

# 19. Endergebnis

Das finale System ist minimal und konkret zugleich:

```text
Bauteil:
wenige Punkte

Punkt:
mehrere Facets

Facet:
Port + Host-Geometrie + Check

Verbindung:
gemeinsamer Connection Passport

Nachweis:
modifiziert Facets und Checks
```

Damit ist das System geeignet für:

```text
Abbau/Aufbau-Bauteilkataloge
monolithische Fragmente
ReCreate-Fertigteilbauteile
neue ReUse-Projekte mit anderen Typologien
```

Es bleibt generalisierbar, weil die Punktfamilien abstrakt sind.  
Es bleibt konkret, weil jedes Facet seine Host-Geometrie und seinen Check kennt.
