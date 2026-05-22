# Abstraktionslogik für Pakete, Repräsentationen, Connectoren und Ports  
## Version mit Datentypen und Zweck der abstrakten Geometrien

**Zweck**  
Dieses Dokument überführt die Paketstruktur in eine einheitliche Abstraktionslogik nach dem Muster:

```text
Reales Bauteil
→ paket-spezifische Repräsentation
→ abstrakte Geometrie mit Datentyp
→ Eigenschaften
→ Connectoren
→ Ports
→ Regeln / Checks / Berechnungen
```

Der wichtigste Zusatz dieser Version ist:

```text
Jede abstrakte Geometrie bekommt:
1. einen Datentyp
2. einen Zweck im System
```

Das verhindert unklare Begriffe wie „Fläche“, „Zone“ oder „Fragment“, ohne zu sagen, ob sie als Mesh, Linie, Graph, Polygon, Knoten, Bounding Box, Raster, Overlay oder Handle gespeichert wird.

---

# 1. Grundprinzip

## 1.1 Vorbild: Träger im Tragwerksmodell

```text
Realer Träger
→ 1D-Linienelement
→ Querschnitts- und Materialeigenschaften
→ Knoten / Anschlüsse / Auflager
→ Steifigkeitsgleichung
→ Kräfte, Momente, Verformungen, Reaktionen
```

Kurz:

```text
Träger = Liniengeometrie + Querschnittseigenschaften + Knotenanschlüsse + Berechnungsmodell
```

Diese Abstraktionslogik wird auf alle Pakete übertragen.

## 1.2 Allgemeines Muster

```text
Reales Objekt
↓
Paket-Repräsentation
↓
abstrakte Geometrie
↓
Datentyp
↓
Eigenschaften
↓
Connectoren
↓
Ports
↓
Regeln / Checks / Berechnungen
```

## 1.3 Begriffe

| Begriff | Bedeutung |
|---|---|
| **Komponente** | reales wiederverwendetes Bauteil oder Fragment |
| **Paket** | fachliche Sicht auf dieselbe Komponente |
| **Repräsentation** | vereinfachtes Modell der Komponente innerhalb eines Pakets |
| **abstrakte Geometrie** | vereinfachte, paket-spezifische Geometrieform |
| **Datentyp** | technische Form, in der die abstrakte Geometrie gespeichert wird |
| **Eigenschaft** | beschreibender Wert ohne eigene Handlung |
| **Connector** | platzierter, handlungsrelevanter Griffpunkt |
| **Port** | semantischer Kompatibilitätstyp eines Connectors |
| **Regel / Check** | prüft oder berechnet etwas anhand von Eigenschaften, Connectoren und Ports |

## 1.4 Regel für Connectoren

```text
Keine Connectoren auf jede Fläche.
Keine Connectoren auf jede Kante.
Keine Connectoren nur wegen Beschreibung.

Connectoren nur dort,
wo Verbindung, Berechnung, Warnung, Kompatibilität
oder Entwurfsentscheidung stattfinden.
```

---

# 2. Quellenbasis und Beispielkomponenten

## 2.1 Abbau/Aufbau DE_1OG_001

**Quelle:** Abbau/Aufbau-Handbuch, Bauteilkatalog.  
Das Beispiel **DE_1OG_001** ist eine Deckenplatte mit:

```text
Typologie: Deckenplatte
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

Quelle:  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

## 2.2 SlabBeamColumnFragment

**Quelle:** Abbau/Aufbau Masterarbeit 2020.  
Die Masterarbeit beschreibt räumlich wertvolle Stahlbetonfragmente und zugeschnittene Elemente, die auf einem Halbfertigteil-Stahlbetonträger ruhen und über nachträglichen Bewehrungsanschluss kraftschlüssig verbunden werden.

**Systemtypologie:**  
`SlabBeamColumnFragment` ist eine abgeleitete Systemtypologie:

```text
monolithisches Betonfragment
= Plattenbereich + integrierter Trägerbereich + Stützenabschnitt + Schnittflächen
```

Quelle:  
https://abbauaufbau.de/project/masterarbeit-2020

## 2.3 ReCreate Hollow-Core Slab

**Quelle:** ReCreate-Pilotprojekte Niederlande und Finnland.  
Relevante Elemente:

```text
Hohlkammerdecken
Längsfugen
Nassverbindungen
Sägen entlang der Fugen
Heben und Transport
BIM-Inventar
QR-Tracking
Prüfung und Neuberechnung
```

Quellen:  
https://recreate-project.eu/project-pilots/the-netherlands/  
https://recreate-project.eu/project-pilots/finland/

---

# 3. Paketübersicht mit Geometriedatentypen

| Paket | Reales Objekt wird zu | wichtigste abstrakte Geometriedatentypen | Hauptzweck |
|---|---|---|---|
| Basisgeometrie | neutraler Körper | `SolidMesh`, `BRep`, `OrientedBoundingBox`, `FaceSet`, `EdgeSet` | Messen und Ableiten |
| Tragwerk | Analysemodell | `LineElement1D`, `PlateElement2D`, `Node`, `SupportPatch`, `StructuralGraph` | Kraftfluss und Anschlussprüfung |
| Energie / Gebäudehülle | thermisches Modell | `ThermalSurface`, `Layer`, `BoundaryEdge`, `PenetrationLoop`, `BridgeZone` | U-Wert, Kontinuität, Wärmebrücken |
| TGA / Öffnungen | Routenmodell | `RouteLine`, `RouteNode`, `OpeningLoop`, `DrillingCylinder`, `BlockedZone` | Leitungsführung und Konfliktprüfung |
| Semantik / Architektur | Design-Handle-Modell | `AlignmentLine`, `VisibilitySurface`, `AccessZone`, `SideRegion`, `StackPlane` | Entwurfsbeziehungen prüfen |
| Logistik / Montage | Handlingmodell | `TransportEnvelope`, `CenterOfGravityPoint`, `LiftingZone`, `StorageSupportZone`, `AccessVolume` | Heben, Lagern, Transport, Montage |
| Nachweis-Overlay | Konfidenz- / Risiko-Overlay | `EvidenceZone`, `ScanLine`, `DamagePolygon`, `TestPoint`, `ConfidenceField` | Status anderer Connectoren modifizieren |

---

# 4. Paket 0 — Basisgeometrie

## 4.1 Abstraktionslogik

```text
Reales Bauteil
→ neutraler geometrischer Körper
→ messbare Geometrie
→ keine Connectoren
→ keine Ports
→ geometrische Messungen
```

## 4.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| neutraler Körper | `SolidMesh` oder `BRep` | digitale Ausgangsform des Bauteils |
| Bounding Box | `OrientedBoundingBox` | Länge, Breite, Höhe / Dicke und Transporthülle ableiten |
| Hauptflächen | `FaceSet` | Ausgangsdaten für Energie, Semantik, Logistik |
| Hauptkanten | `EdgeSet` | Ausgangsdaten für Tragwerk, Fugen, Ausrichtung |
| rohe Öffnungen | `OpeningLoop[]` | Ausgangsdaten für TGA und Energie-Durchdringungen |
| geometrisches Zentrum | `Point3D` | Grundlage für Schwerpunkt- oder Platzierungslogik |
| lokale Achsen | `CoordinateFrame3D` | Orientierung und Paket-Ableitungen standardisieren |

## 4.3 Eigenschaften

```text
Typologie
Geometriequelle
Einheiten
Länge
Breite
Höhe / Dicke
Volumen
Flächen
Kanten
Öffnungen
Orientierung
Geometrie-Konfidenz
```

## 4.4 Connectoren und Ports

```text
keine Connectoren
keine Ports
```

Basisgeometrie ist neutral. Eine Kante wird erst im Tragwerk zur Auflagerkante, in Semantik zur Ausrichtungslinie oder in Energie zur Wärmebrückenkante.

## 4.5 Berechnung

```text
SolidMesh / BRep + Einheiten
↓
Bounding Box
Volumen
Flächen
Kanten
Öffnungen
geometrisches Zentrum
```

## 4.6 Beispiel A — Abbau/Aufbau DE_1OG_001

Die Deckenplatte wird als `SolidMesh` oder `BRep` gespeichert. Die `OrientedBoundingBox` liefert 4500 × 2300 × 180 mm. `FaceSet` enthält Oberseite, Unterseite und Seitenflächen. `EdgeSet` enthält lange und kurze Kanten. Das Volumen ist 1.863 m³.

Es gibt keine Connectoren. Die lange Kante wird erst im Tragwerk zu `bearing_support` oder in Semantik zu `alignment_handle`.

## 4.7 Beispiel B — SlabBeamColumnFragment

Das Fragment wird als ein zusammenhängender `SolidMesh` gespeichert. Zusätzlich werden rohe Subregionen markiert:

```text
slab_region: FaceSet / VolumeRegion
beam_region: VolumeRegion
column_region: VolumeRegion
cut_faces: FaceSet
```

Diese Subregionen dienen später als Quelle für Tragwerksgraph, Semantik und Logistik.

## 4.8 Beispiel C — ReCreate Hollow-Core Slab

Die Hohlkammerdecke wird als `BRep` oder `SolidMesh` mit `OpeningLoop[]` beziehungsweise `VoidVolume[]` gespeichert. Die Hohlräume bleiben zunächst geometrische Eigenschaften. Erst im TGA-Paket können sie zu `RouteLine` werden.

---

# 5. Paket 1 — Tragwerk

## 5.1 Abstraktionslogik

```text
Reales tragendes Bauteil
→ Tragwerksmodell
→ Linie / Platte / Knoten / Auflagerzone
→ Querschnitts- und Materialeigenschaften
→ strukturelle Connectoren
→ Ports
→ Gleichgewicht, Steifigkeit, Auflager- und Anschlusschecks
```

## 5.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| Trägerachse | `LineElement1D` | Biegung, Querkraft und Knotenanschlüsse berechnen |
| Stützenachse | `LineElement1D` | Normalkraft, Knicken und vertikale Lastübertragung prüfen |
| Plattenfläche | `PlateElement2D` oder `ShellElement2D` | Lastabtragung, Spannrichtung und Auflager prüfen |
| Wandscheibe | `PlateElement2D` oder `WallPanel2D` | vertikale Scheibenwirkung und Auflagerlogik prüfen |
| Knoten | `Node` | Verbindung von Linien, Platten, Stützen und Auflagern |
| Auflagerpatch | `SupportPatch2D` | lokale Auflagerung und Überlappung prüfen |
| Transferknoten | `TransferNode` | Lastübergang zwischen Platte, Träger und Stütze prüfen |
| Kontinuitätszone | `ContinuityZone` | Kraftschluss, Verguss oder Bewehrungskontinuität prüfen |
| struktureller Graph | `StructuralGraph` | Kombination aus Linien, Platten, Knoten und Connectoren |

## 5.3 Eigenschaften

```text
Querschnitt: Breite, Höhe, Fläche A, Trägheitsmoment I
Material: E-Modul, G-Modul
Dicke
Spannrichtung
Kapazitätsstatus
Bewehrungsstatus
Auflagerbedingung
Schadensrelevanz
```

## 5.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `bearing_support` | `bearing_side` / `support_side` | Last wird über Auflagerung übertragen |
| `joint_connection` | `member_side` | Bauteile werden entlang einer Seite / Fuge verbunden |
| `anchor_connection` | `anchor_side` | Verbindung über Anker, Schrauben, Dübel oder Bohrungen |
| `continuity_connection` | `continuity_side` | Kraftschluss oder Bewehrungskontinuität |
| `support_transfer` | `transfer_side` | Lastübertragung über Zwischenzone oder Transferknoten |

## 5.5 Berechnung / Check

```text
LineElement1D / PlateElement2D / Node
+ Querschnitts- und Materialeigenschaften
+ Connectoren
+ Lasten
↓
K u = f oder lokaler Nachweis
↓
Kräfte, Momente, Verformungen, Reaktionen, Warnungen
```

## 5.6 Beispiel A — Abbau/Aufbau Wand–Decke mit DE_1OG_001

**Komponenten:**  
DE_1OG_001 als Deckenplatte und eine wiederverwendete Wand.

**Repräsentation:**  
Die Decke wird als `PlateElement2D` repräsentiert. Die Wand wird als `WallPanel2D` mit Wandkopf-Auflager repräsentiert.

**Abstrakte Geometrien:**  
Die Plattenkante wird als `SupportPatch2D` für Auflagerlogik genutzt. Der Wandkopf wird ebenfalls als `SupportPatch2D` gespeichert. Eine mögliche Verguss- oder Bewehrungszone wird als `ContinuityZone` modelliert.

**Konkrete Connectoren der Decke:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | `SupportPatch2D` | Decke kann auf Wand aufliegen |
| `anchor_connection` | `anchor_side` | `AnchorZone2D` | Schraubanker / Flachstahlhalter möglich |
| `continuity_connection` | `continuity_side` | `ContinuityZone` | nachträglicher Bewehrungsanschluss + Verguss möglich |

**Konkrete Connectoren der Wand:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `support_side` | `SupportPatch2D` | Wand kann Decke tragen |
| `anchor_connection` | `support_side` | `AnchorReceiverZone2D` | Wand nimmt Anker auf |
| `continuity_connection` | `continuity_side` | `ContinuityZone` | Wandanschluss kann kraftschlüssig werden |

**Regeln:**  
`bearing_side → support_side` prüft Überlappung der `SupportPatch2D`, Richtung und Mindestauflager.  
`anchor_side → support_side` prüft Randabstand, Bewehrungskonflikt und Ankerbarkeit.  
`continuity_side → continuity_side` prüft Geometrie der `ContinuityZone`, Vergussraum und Bewehrungsnachweis.

## 5.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Fragment mit Plattenbereich, integriertem Trägerbereich und Stützenabschnitt.

**Repräsentation:**  
Ein `StructuralGraph`, nicht ein unklarer Einzelkörper.

**Abstrakte Geometrien:**

```text
Plattenbereich → PlateElement2D
Trägerbereich → LineElement1D
Stützenbereich → LineElement1D
Schnittpunkt Platte / Träger / Stütze → TransferNode
Schnittfläche → ContinuityZone
```

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | `SupportPatch2D` | Fragment kann dort aufliegen |
| `support_transfer` | `transfer_side` | `TransferNode` + `LineElement1D` | Last läuft über Trägerregion |
| `bearing_support` | `support_side` | `SupportPatch2D` oder `Node` | Stützenregion nimmt Last auf / gibt sie ab |
| `continuity_connection` | `continuity_side` | `ContinuityZone` | Schnittfläche kann kraftschlüssig angeschlossen werden |

**Regeln:**  
`transfer_side → support_side` prüft Lastpfad über `LineElement1D` und `TransferNode`.  
`continuity_side → continuity_side` prüft Schnittflächengeometrie, Bewehrungsnachweis und Kraftschluss.  
`bearing_side → support_side` prüft lokale Auflagerung und Pressung.

## 5.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Wiedergewonnene Hohlkammerdecke.

**Repräsentation:**  
Ein `PlateElement2D` oder ein einachsig spannendes Slab-Element mit Längsrichtung.

**Abstrakte Geometrien:**  
Die Stirnseiten werden als `SupportPatch2D` modelliert. Die Längsfuge wird als `JointLine` oder `LineElement1D` für Fugenprüfung gespeichert. Die Hohlräume bleiben Eigenschaften oder `VoidVolume[]`, nicht automatisch Connectoren.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | `SupportPatch2D` | erstes Endauflager |
| `bearing_support` | `bearing_side` | `SupportPatch2D` | zweites Endauflager |
| `joint_connection` | `member_side` | `JointLine` | Längsfuge zur Nachbarplatte |

**Regeln:**  
Endauflager prüfen Auflagerlänge, Richtung und Toleranz.  
Längsfugen prüfen Ausrichtung, Fugenbreite und Wiederverbindungsdetail.  
Tragfähigkeit bleibt abhängig von Test oder Neuberechnung.

---

# 6. Paket 2 — Energie / Gebäudehülle

## 6.1 Abstraktionslogik

```text
Reales Hüllenbauteil
→ thermisches Modell
→ Fläche / Schicht / Kante / Durchdringung
→ thermische Eigenschaften
→ Hüllen-Connectoren
→ Ports
→ U-Wert-, Kontinuitäts-, Abdichtungs- und Wärmebrückenchecks
```

## 6.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| thermische Grenzfläche | `ThermalSurface` | Innen-/Außenbezug und U-Wert-Fläche definieren |
| Schicht | `Layer` | Dicke, Material und Wärmewiderstand speichern |
| Rand einer thermischen Fläche | `BoundaryEdge` | Anschluss und Kontinuität prüfen |
| Durchdringung | `PenetrationLoop` | Abdichtung und Hüllenunterbrechung prüfen |
| Wärmebrückenzone | `BridgeZone` | Wärmebrückenwarnung erzeugen |
| Dämmschnittstelle | `InsulationInterface` | Dämmschichtkontinuität prüfen |
| Feuchterisikozone | `MoistureRiskZone` | Risiko bei Dach, Boden, Außenkontakt markieren |

## 6.3 Eigenschaften

```text
Dicke d
Wärmeleitfähigkeit λ
thermischer Widerstand R
U-Wert-Status
Fläche
Innen-/Außenstatus
Dämmstatus
Feuchterisiko
Luftdichtheitsstatus
```

## 6.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `thermal_continuity` | `thermal_side` | thermische Grenze muss weiterlaufen |
| `insulation_continuity` | `insulation_side` | Dämmschicht muss weiterlaufen |
| `penetration_sealing` | `penetration_side` | Durchdringung muss abgedichtet werden |
| `thermal_bridge_warning` | `bridge_side` | Wärmebrückenrisiko als Warnzone |

## 6.5 Berechnung / Check

```text
ThermalSurface + Layer(d, λ)
↓
R = d / λ
↓
U = 1 / ΣR
↓
U-Wert-Vorcheck
```

Zusätzlich:

```text
BoundaryEdge / PenetrationLoop / BridgeZone
↓
Kontinuitäts-, Abdichtungs- oder Wärmebrückencheck
```

## 6.6 Beispiel A — Abbau/Aufbau 200-mm-Stahlbetonwand

**Komponente:**  
Wiederverwendete 200-mm-Stahlbetonwand als Außenwand.

**Repräsentation:**  
`ThermalSurface` mit `Layer` für den Beton.

**Abstrakte Geometrien:**  
Die äußere Wandfläche ist `InsulationInterface`. Der Wandrand ist `BoundaryEdge`. Eine Öffnung ist `PenetrationLoop`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | `InsulationInterface` | Dämmung muss anschließen |
| `thermal_continuity` | `thermal_side` | `BoundaryEdge` | thermische Grenze läuft weiter |
| `penetration_sealing` | `penetration_side` | `PenetrationLoop` | Durchdringung muss abgedichtet werden |

**Regeln:**  
Dämmkontinuität prüft Lücken.  
Thermische Kontinuität prüft Grenzflächenanschluss.  
Durchdringungsabdichtung prüft Luftdichtheit und Feuchterisiko.

## 6.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Platten-Träger-Stützen-Fragment.

**Repräsentation:**  
Nur aktiv als Energiepaket, wenn das Fragment Teil der Gebäudehülle wird.

**Abstrakte Geometrien:**  
Eine Schnittfläche an der Hülle wird `ThermalSurface` oder `BoundaryEdge`. Der Platten-Träger-Stützen-Knoten wird `BridgeZone`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `thermal_continuity` | `thermal_side` | `BoundaryEdge` | thermischer Anschluss an Nachbarelement |
| `thermal_bridge_warning` | `bridge_side` | `BridgeZone` | Wärmebrücke am monolithischen Knoten |

**Regeln:**  
Thermische Kontinuität prüft Anschluss an Nachbarhüllenelement.  
Wärmebrücke prüft, ob der monolithische Knoten die thermische Grenze durchstößt.

## 6.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke, wenn als Dach oder außenliegende Decke verwendet.

**Repräsentation:**  
`ThermalSurface` mit Hohlräumen als Eigenschaft oder ergänzendem `VoidVolume[]`.

**Abstrakte Geometrien:**  
Oberseite wird `InsulationInterface`. Plattenkante wird `BridgeZone`. Durchdringung wird `PenetrationLoop`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | `InsulationInterface` | Dämmschicht läuft über Platte |
| `thermal_bridge_warning` | `bridge_side` | `BridgeZone` | Wärmebrückenrisiko an Plattenkante |
| `penetration_sealing` | `penetration_side` | `PenetrationLoop` | Abdichtung erforderlich |

---

# 7. Paket 3 — TGA / Öffnungen

## 7.1 Abstraktionslogik

```text
Reale Öffnung / Leitung / Schacht
→ Routenmodell
→ Linie / Knoten / Öffnung / Bohrzone / Sperrzone
→ Eigenschaften
→ TGA-Connectoren
→ Ports
→ Durchmesser-, Lichtraum-, Konflikt- und Dichtungschecks
```

## 7.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| Leitungsroute | `RouteLine` | Verlauf von Kabel, Rohr oder Kanal prüfen |
| Routenknoten | `RouteNode` | Richtungswechsel, Übergang oder Verbindungspunkt prüfen |
| bestehende Öffnung | `OpeningLoop` | vorhandene Durchdringung nutzen |
| Bohrkandidat | `DrillingCylinder` | neue Kernbohrung räumlich prüfen |
| Sperrzone | `BlockedZone` | Konflikt mit Tragwerk, Bewehrung oder Nutzung markieren |
| Lichtraum | `ClearanceVolume` | Platzbedarf einer Leitung prüfen |
| Schachtanschluss | `ShaftInterface` | Übergang in vertikale Route prüfen |

## 7.3 Eigenschaften

```text
Öffnungsgröße
Öffnungstiefe
Leitungsdurchmesser
Randabstand
Lichtraumstatus
Bohrstatus
Bezug zu Tragwerkszonen
Bezug zur Bewehrung
Brandschutz- / Schallschutzstatus
```

## 7.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `route_continuity` | `route_side` | Leitung kann weitergeführt werden |
| `opening_use` | `opening_side` | bestehende Öffnung wird genutzt |
| `drilling_candidate` | `drilling_side` | neue Bohrung wird vorgeschlagen |
| `blocked_conflict` | `blocked_side` | Zone blockiert Route oder Bohrung |

## 7.5 Berechnung / Check

```text
RouteLine + OpeningLoop / DrillingCylinder + Durchmesser
↓
passt Durchmesser?
ist Lichtraum frei?
Randabstand ok?
Konflikt mit Tragwerk / Bewehrung?
Brandschutz / Schallschutz nötig?
```

## 7.6 Beispiel A — Abbau/Aufbau Öffnung

**Komponente:**  
Wiederverwendete Platte oder Wand mit katalogisierter Öffnung.

**Repräsentation:**  
Öffnungsmodell.

**Abstrakte Geometrien:**  
Öffnung als `OpeningLoop`, geplante Leitung als `RouteLine`, notwendiger Platz als `ClearanceVolume`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `opening_use` | `opening_side` | `OpeningLoop` | bestehende Öffnung wird genutzt |
| `route_continuity` | `route_side` | `RouteLine` | Leitung soll durch Öffnung laufen |

**Regeln:**  
`opening_side → route_side` prüft Durchmesser, Randabstand und Tragwerkskonflikt.  
`route_side → route_side` prüft Leitungsflucht und Lichtraum.

## 7.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Platten-Träger-Stützen-Fragment.

**Repräsentation:**  
Bohr- und Sperrzonenmodell.

**Abstrakte Geometrien:**  
Neue Bohrung als `DrillingCylinder`. Träger- und Stützenregion als `BlockedZone`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `drilling_candidate` | `drilling_side` | `DrillingCylinder` | mögliche neue Bohrung |
| `blocked_conflict` | `blocked_side` | `BlockedZone` | Leitung oder Bohrung kritisch |

**Regeln:**  
Bohrkandidat prüft Bewehrung, Tragwerkszone und Randabstand.  
Blockierte Zone erzeugt Konflikt mit Route oder Bohrung.

## 7.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Routen- oder Hohlraummodell.

**Abstrakte Geometrien:**  
Hohlkammerachse als `RouteLine`, neue Bohrung als `DrillingCylinder`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `route_continuity` | `route_side` | `RouteLine` | Leitung könnte im Hohlraum laufen |
| `drilling_candidate` | `drilling_side` | `DrillingCylinder` | neue Durchdringung möglich |

**Regeln:**  
Hohlraumroute prüft Kontinuität und Durchmesser.  
Bohrkandidat prüft Durchmesser, Bewehrung und Tragwerkskonflikt.

---

# 8. Paket 4 — Semantik / Architektur

## 8.1 Abstraktionslogik

```text
Reales Bauteil als Entwurfselement
→ Design-Handle-Modell
→ Ausrichtungslinie / Sichtfläche / Zugangszone / Seitenbezug
→ architektonische Eigenschaften
→ semantische Connectoren
→ Ports
→ Ausrichtungs-, Sichtbarkeits-, Zugangs- und Raumchecks
```

## 8.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| Ausrichtungslinie | `AlignmentLine` | Raster, Fuge, Datum oder Rhythmus prüfen |
| Sichtfläche | `VisibilitySurface` | Sichtbarkeit, Verdeckung und Oberflächenwirkung prüfen |
| Zugangszone | `AccessZone` | Annäherung, Durchgang oder Nische prüfen |
| Seitenregion | `SideRegion` | Raumseite, Fassadenseite oder Orientierung prüfen |
| Stapel- / Niveaufläche | `StackPlane` | vertikale Beziehung oder Niveau prüfen |
| Öffnungsachse | `OpeningAxis` | Bezug von Öffnungen und Zugang prüfen |
| Raumgrenzenfläche | `SpatialBoundarySurface` | Raumabschluss oder Raumkontinuität prüfen |

## 8.3 Eigenschaften

```text
architektonische Rolle
räumliche Rolle
Sichtbarkeitsstatus
Wiederverwendungsausdruck
Oberflächenzustand
Rasterbezug
Raumbezug
Fassadenbezug
Orientierung
Entwurfspräferenz-Relevanz
```

## 8.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `access_handle` | `access_port` | Zugang / Annäherung / Durchgang |
| `attachment_handle` | `attachment_port` | architektonische Anbindung |
| `stack_handle` | `top_port` / `bottom_port` | Stapelung / vertikale Beziehung |
| `side_handle` | `side_port` | Seite, Raumgrenze, Orientierung |
| `opening_handle` | `opening_port` | architektonische Öffnung |
| `alignment_handle` | `alignment_port` | Raster, Fuge, Datum, Rhythmus |
| `visibility_constraint_handle` | `visibility_port` | Sichtbarkeit / Verdeckung |

## 8.5 Berechnung / Check

```text
Design-Geometrien + Platzierung + Zielpräferenzen
↓
Ausrichtung
Sichtbarkeit
Zugang
Raumgrenze
Fassadenrhythmus
Wiederverwendungsausdruck
```

## 8.6 Beispiel A — Abbau/Aufbau DE_1OG_001

**Komponente:**  
Deckenplatte DE_1OG_001.

**Repräsentation:**  
Architektonisches Plattenmodell.

**Abstrakte Geometrien:**  
Die lange Plattenkante wird als `AlignmentLine` verwendet, falls Fuge oder Raster geprüft werden. Die Unterseite wird als `VisibilitySurface` verwendet, falls sie sichtbar bleiben soll.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | `AlignmentLine` | Fuge oder Raster ausrichten |
| `visibility_constraint_handle` | `visibility_port` | `VisibilitySurface` | Untersicht bleibt sichtbar / wird bewertet |

**Regeln:**  
`alignment_port → alignment_port` prüft Fugen- und Rasterausrichtung.  
`visibility_port` prüft Sichtbarkeit, Verdeckung und Oberflächenwarnung.

## 8.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Fragment mit Platten-, Träger- und Stützenregion.

**Repräsentation:**  
Architektonisches Fragmentmodell.

**Abstrakte Geometrien:**  
Nischenzugang als `AccessZone`. Stützenseite als `SideRegion`. Schnittkante oder Trägerlinie als `AlignmentLine`. Sichtbare Fragmentflächen als `VisibilitySurface`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `access_handle` | `access_port` | `AccessZone` | Annäherung / Zugang prüfen |
| `side_handle` | `side_port` | `SideRegion` | Raumbeziehung prüfen |
| `alignment_handle` | `alignment_port` | `AlignmentLine` | Ausrichtung an Raster / Datum |
| `visibility_constraint_handle` | `visibility_port` | `VisibilitySurface` | Lesbarkeit und Wiederverwendungsausdruck |

**Regeln:**  
Zugang prüft Lichtraum und Annäherung.  
Seitenbezug prüft Raumgrenze.  
Ausrichtung prüft Raster, Fuge und Datum.  
Sichtbarkeit prüft Verdeckung und Oberflächenzustand.

## 8.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Architektonisches Fertigteilmodell.

**Abstrakte Geometrien:**  
Längsfuge als `AlignmentLine`. Oberseite und Unterseite als `StackPlane`, falls Niveau oder Stapelung geprüft wird. Unterseite als `VisibilitySurface`, falls sichtbar.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | `AlignmentLine` | Modul- und Fugenausrichtung |
| `stack_handle` | `top_port` | `StackPlane` | vertikale Relation / Niveau |
| `stack_handle` | `bottom_port` | `StackPlane` | Gegenstück zur vertikalen Relation |
| `visibility_constraint_handle` | `visibility_port` | `VisibilitySurface` | sichtbare Wiederverwendung |

**Regeln:**  
Ausrichtung prüft Modul und Fuge.  
`top_port → bottom_port` prüft Niveau und vertikale Ausrichtung.  
Sichtbarkeit prüft Oberfläche und Verdeckung.

---

# 9. Paket 5 — Logistik / Montage

## 9.1 Abstraktionslogik

```text
Reales Bauteil im Prozess
→ Handlingmodell
→ Transporthülle / Schwerpunkt / Hebezone / Lagerauflager
→ Logistik-Eigenschaften
→ Handling-Connectoren
→ Ports
→ Hebe-, Lager-, Transport- und Montagechecks
```

## 9.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| Transporthülle | `TransportEnvelope` | Transportmaße und Kollisionen prüfen |
| Schwerpunkt | `CenterOfGravityPoint` | Hebbarkeit und Stabilität prüfen |
| Hebezone | `LiftingZone` | mögliche Hebepunkte / Hebeflächen prüfen |
| Lagerauflager | `StorageSupportZone` | Lagerung, Auflagerabstand und Stapelung prüfen |
| Transportauflager | `TransportSupportZone` | Ladungssicherung und Transportsupport prüfen |
| Montagezugangsraum | `AccessVolume` | Zugang für Montage und Verbindung prüfen |
| Schutzzone | `ProtectionZone` | Kanten-, Witterungs- oder Oberflächenschutz prüfen |
| temporäre Abstützzone | `TemporaryBracingZone` | Stabilität vor endgültigem Anschluss prüfen |

## 9.3 Eigenschaften

```text
Masse
Transportmaße
Schwerpunktstatus
Lagerorientierung
Hebestatus
Zugangsstatus
Schutzstatus
temporäre Abstützung
Transportstatus
```

## 9.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `lifting_handle` | `lifting_port` | Heben / Kran |
| `storage_handle` | `storage_port` | Lagerung / Lagerauflager |
| `transport_handle` | `transport_port` | Transporthülle / Ladungssicherung |
| `access_handle` | `access_port` | Montagezugang |
| `protection_handle` | `protection_port` | Schutz sensibler Zonen |
| `temporary_bracing_handle` | `temporary_bracing_port` | temporäre Stabilisierung |

## 9.5 Berechnung / Check

```text
Handling-Geometrie + Masse + Prozessbedingungen
↓
Hebbarkeit
Lagerstabilität
Transporthülle
Montagezugang
Schutzbedarf
temporäre Abstützung
```

## 9.6 Beispiel A — Abbau/Aufbau DE_1OG_001

**Komponente:**  
Deckenplatte DE_1OG_001.

**Repräsentation:**  
Handlingmodell.

**Abstrakte Geometrien:**  
Transporthülle als `TransportEnvelope`, Schwerpunkt als `CenterOfGravityPoint`, Lagerauflager als `StorageSupportZone`, Hebekandidat als `LiftingZone`, Kanten als `ProtectionZone`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `storage_handle` | `storage_port` | `StorageSupportZone` | liegende Lagerung |
| `transport_handle` | `transport_port` | `TransportEnvelope` | Transport und Ladungssicherung |
| `lifting_handle` | `lifting_port` | `LiftingZone` | Hebbarkeit |
| `protection_handle` | `protection_port` | `ProtectionZone` | Schutz gegen Schäden / Witterung |

**Regeln:**  
Lagerung prüft Orientierung, Auflagerabstand und Trennhölzer.  
Transport prüft Maße und Ladungssicherung.  
Heben prüft Schwerpunkt und Hebe-Nachweis.  
Schutz prüft Kanten- und Witterungsschutz.

## 9.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Unregelmäßiges monolithisches Fragment.

**Repräsentation:**  
Komplexes Handlingmodell.

**Abstrakte Geometrien:**  
Schwerpunkt als `CenterOfGravityPoint`, Hebezone als `LiftingZone`, Lagerung als `StorageSupportZone`, Schnittflächen als `ProtectionZone`, mögliche Abstützung als `TemporaryBracingZone`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | `LiftingZone` | Fragment heben |
| `storage_handle` | `storage_port` | `StorageSupportZone` | kippsichere Lagerung |
| `protection_handle` | `protection_port` | `ProtectionZone` | Schnittflächen schützen |
| `temporary_bracing_handle` | `temporary_bracing_port` | `TemporaryBracingZone` | temporäre Stabilisierung |

**Regeln:**  
Heben prüft Schwerpunkt, Hebbarkeit und Kran-Zugang.  
Lagerung prüft Kippstabilität.  
Schutz prüft Schnittflächen und empfindliche Kanten.  
Temporäre Abstützung prüft Montagezugang und Stabilität.

## 9.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Transport- und Hebemodell.

**Abstrakte Geometrien:**  
Hebezonen als `LiftingZone`, Transportkörper als `TransportEnvelope`, Lagerauflager als `StorageSupportZone`.

**Konkrete Connectoren:**

| Connector | Port | Datentyp der Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | `LiftingZone` | Element heben |
| `transport_handle` | `transport_port` | `TransportEnvelope` | Transport prüfen |
| `storage_handle` | `storage_port` | `StorageSupportZone` | Lagerung prüfen |

**Regeln:**  
Heben prüft Hebbarkeit, Schwerpunkt und Beschädigungsrisiko.  
Transport prüft Ladungssicherung und Transporthülle.  
Lagerung prüft Auflagerabstand und Orientierung.

---

# 10. Paket 6 — Nachweis-Overlay

## 10.1 Abstraktionslogik

```text
Realer Nachweis
→ Konfidenz- / Risiko-Overlay
→ Scanfläche / Schadenszone / Prüfpunkt / unbekannte Zone
→ Nachweiseigenschaften
→ keine Connectoren
→ keine Ports
→ Statusmodifikation anderer Connectoren
```

## 10.2 Abstrakte Geometrie: Datentyp und Zweck

| Abstrakte Geometrie | Datentyp | Zweck im System |
|---|---|---|
| Nachweiszone | `EvidenceZone` | räumlicher Bereich eines Nachweises |
| Scanlinie | `ScanLine` | detektierte Bewehrung oder Messlinie |
| Schadensfläche | `DamagePolygon` | Schaden räumlich mit Connectoren überlagern |
| Risslinie | `CrackLine` | Rissverlauf und Konflikt mit Zonen prüfen |
| Prüfpunkt | `TestPoint` | Bohrkern, Karbonatisierung, Chloridprobe lokalisieren |
| unbekannte Zone | `UnknownZone` | fehlende Information als Risiko markieren |
| Konfidenzfeld | `ConfidenceField` | Zuverlässigkeit räumlich abstufen |

## 10.3 Eigenschaften

```text
Nachweistyp
Ort
Konfidenz
Quelle
Datum
betroffenes Paket
betroffener Connector
betroffener Port
Effekt
Begründung
```

## 10.4 Connectoren und Ports

```text
keine Connectoren
keine Ports
```

Nachweise erzeugen keine neuen Connectoren. Sie verändern vorhandene Connectoren.

## 10.5 Berechnung / Check

```text
EvidenceZone / DamagePolygon / UnknownZone
+ Connectorgeometrie
↓
Überlappungsprüfung
↓
bestätigt / Warnung / blockiert / Konfidenz reduziert
```

## 10.6 Beispiel A — Abbau/Aufbau Bewehrungsnachweis

**Komponente:**  
Wand oder Deckenplatte mit möglicher Ankerverbindung.

**Repräsentation:**  
Bewehrungs-Overlay.

**Abstrakte Geometrien:**  
Bewehrungsscan als `ScanLine[]`, unbekannte Bereiche als `UnknownZone`, freigegebene Bereiche als `EvidenceZone`.

**Betroffener Connector:**  
`anchor_connection` im Tragwerk.

**Wirkung:**  
Wenn eine `UnknownZone` den `AnchorZone2D` überlagert, wird `anchor_connection` blockiert oder als Warnung markiert. Wenn `ScanLine[]` eine freie Zone bestätigt, kann die Verbindung zur Ingenieurprüfung weitergehen.

## 10.7 Beispiel B — SlabBeamColumnFragment Schnittfläche

**Komponente:**  
SlabBeamColumnFragment.

**Repräsentation:**  
Schnittflächen-, Rebar- und Schadensoverlay.

**Abstrakte Geometrien:**  
Schnittfläche als `EvidenceZone`, freiliegende Bewehrung als `ScanLine`, Schaden als `DamagePolygon`, unsichere Bereiche als `UnknownZone`.

**Betroffene Connectoren:**  
`continuity_connection`, `support_transfer`, `visibility_constraint_handle`.

**Wirkung:**  
Unbekannte Bewehrung an der Schnittfläche macht `continuity_connection` ingenieurpflichtig. Schaden im Lasttransferbereich warnt `support_transfer`. Schaden auf sichtbaren Flächen warnt `visibility_constraint_handle`.

## 10.8 Beispiel C — ReCreate QR / Test / Neuberechnung

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Tracking-, Test- und Neuberechnungs-Overlay.

**Abstrakte Geometrien:**  
QR-Referenz als `EvidenceRecord`, Testpunkt als `TestPoint`, beschädigte Fuge als `DamagePolygon`, Konfidenz als `ConfidenceField`.

**Betroffene Connectoren:**  
`bearing_support`, `joint_connection`, `lifting_handle`.

**Wirkung:**  
QR-Tracking bestätigt Identität und Rückverfolgbarkeit. Tests oder Neuberechnung erhöhen strukturelle Konfidenz. Unklare Fugenschäden markieren `joint_connection` als manuell zu prüfen.

---

# 11. Kompakte Kompatibilitätsregeln

| Regel | Ports | Checks |
|---|---|---|
| strukturelles Auflager | `bearing_side → support_side` | Überlappung, Richtung, Auflagerlänge |
| strukturelle Verankerung | `anchor_side → support_side` | Randabstand, Bewehrung, Ankerbarkeit |
| strukturelle Kontinuität | `continuity_side → continuity_side` | Bewehrungskontinuität, Verguss, Kraftschluss |
| struktureller Transfer | `transfer_side → support_side / bearing_side` | Lastpfad, lokale Pressung |
| thermische Kontinuität | `thermal_side → thermal_side` | thermische Grenzfortsetzung |
| Dämmkontinuität | `insulation_side → insulation_side` | Schichtfortsetzung, Lücken |
| Hüllendurchdringung | `penetration_side → thermal_side / insulation_side` | Abdichtung, Luftdichtheit, Feuchte |
| TGA-Route | `route_side → route_side` | Leitungsflucht, Lichtraum |
| TGA-Öffnung | `opening_side → route_side` | Durchmesser, Randabstand, Konflikt |
| TGA-Bohrung | `drilling_side → route_side` | Bewehrung, Tragwerkszone, Randabstand |
| architektonischer Zugang | `access_port → access_port` | Lichtraum, Annäherung |
| architektonische Stapelung | `top_port → bottom_port` | Niveau, vertikale Ausrichtung |
| architektonische Ausrichtung | `alignment_port → alignment_port` | Raster, Fuge, Datum |
| Logistik Heben | `lifting_port → Prozessanforderung` | Schwerpunkt, Hebbarkeit |
| Logistik Lagerung | `storage_port → Lagerbedingung` | Orientierung, Auflager, Trennhölzer |

---

# 12. Gesamtabstraktion der drei Beispiele

## 12.1 Abbau/Aufbau DE_1OG_001

| Paket | Repräsentation | wichtigste abstrakte Geometrie | Connectoren |
|---|---|---|---|
| Basisgeometrie | neutraler Plattenkörper | `SolidMesh`, `OrientedBoundingBox`, `FaceSet`, `EdgeSet` | keine |
| Tragwerk | 2D-Platte | `PlateElement2D`, `SupportPatch2D`, `ContinuityZone` | `bearing_support`, `anchor_connection`, `continuity_connection` |
| Energie | thermische Grenzfläche, falls Hülle | `ThermalSurface`, `InsulationInterface`, `BridgeZone` | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Öffnungs- oder Bohrmodell | `OpeningLoop`, `RouteLine`, `DrillingCylinder` | `opening_use`, `drilling_candidate` |
| Semantik | architektonisches Plattenmodell | `AlignmentLine`, `VisibilitySurface` | `alignment_handle`, `visibility_constraint_handle` |
| Logistik | Handlingmodell | `TransportEnvelope`, `LiftingZone`, `StorageSupportZone` | `storage_handle`, `transport_handle`, `lifting_handle`, `protection_handle` |
| Nachweis | Rebar / Material / Schaden | `ScanLine`, `EvidenceZone`, `DamagePolygon` | keine; modifiziert andere |

## 12.2 SlabBeamColumnFragment

| Paket | Repräsentation | wichtigste abstrakte Geometrie | Connectoren |
|---|---|---|---|
| Basisgeometrie | monolithischer Körper mit Teilregionen | `SolidMesh`, `VolumeRegion`, `FaceSet` | keine |
| Tragwerk | Graph aus Platte + Trägerlinie + Stützenlinie + Transferknoten | `PlateElement2D`, `LineElement1D`, `TransferNode`, `ContinuityZone` | `bearing_support`, `support_transfer`, `continuity_connection` |
| Energie | nur bei Hüllennutzung | `ThermalSurface`, `BoundaryEdge`, `BridgeZone` | `thermal_continuity`, `thermal_bridge_warning` |
| TGA | Bohr- und Sperrzonenmodell | `DrillingCylinder`, `BlockedZone` | `drilling_candidate`, `blocked_conflict` |
| Semantik | architektonisches Fragmentmodell | `AccessZone`, `SideRegion`, `AlignmentLine`, `VisibilitySurface` | `access_handle`, `side_handle`, `alignment_handle`, `visibility_constraint_handle` |
| Logistik | komplexes Handlingmodell | `CenterOfGravityPoint`, `LiftingZone`, `TemporaryBracingZone`, `ProtectionZone` | `lifting_handle`, `storage_handle`, `protection_handle`, `temporary_bracing_handle` |
| Nachweis | Schnittflächen / Rebar / Schaden | `EvidenceZone`, `ScanLine`, `DamagePolygon`, `UnknownZone` | keine; modifiziert andere |

## 12.3 ReCreate Hollow-Core Slab

| Paket | Repräsentation | wichtigste abstrakte Geometrie | Connectoren |
|---|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | `BRep`, `VoidVolume[]`, `OpeningLoop[]` | keine |
| Tragwerk | einachsig spannende Fertigteilplatte | `PlateElement2D`, `SupportPatch2D`, `JointLine` | `bearing_support`, `joint_connection` |
| Energie | Hülle, falls Dach / Außenboden | `ThermalSurface`, `InsulationInterface`, `BridgeZone` | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Hohlraum- oder Bohrmodell | `RouteLine`, `DrillingCylinder` | `route_continuity`, `drilling_candidate` |
| Semantik | Modul- und Fugenausrichtungsmodell | `AlignmentLine`, `StackPlane`, `VisibilitySurface` | `alignment_handle`, `stack_handle`, optional `visibility_constraint_handle` |
| Logistik | Hebe-, Transport- und Lagermodell | `LiftingZone`, `TransportEnvelope`, `StorageSupportZone` | `lifting_handle`, `transport_handle`, `storage_handle` |
| Nachweis | BIM / QR / Test / Neuberechnung | `EvidenceRecord`, `TestPoint`, `ConfidenceField`, `DamagePolygon` | keine; modifiziert andere |

---

# 13. Finale Regel

Das Trägerbeispiel bleibt die Vorlage für alle Pakete:

```text
Träger im Tragwerksmodell
= LineElement1D
+ Querschnittseigenschaften
+ Node-Verbindungen
+ Steifigkeitsberechnung
```

Analog dazu:

```text
Deckenplatte im Tragwerk
= PlateElement2D
+ Dicke / Material
+ SupportPatch2D-Connectoren
+ Platten- und Auflagerchecks

Wand in Energie
= ThermalSurface
+ Layer-Eigenschaften
+ BoundaryEdge / PenetrationLoop
+ U-Wert- und Hüllenchecks

Öffnung in TGA
= OpeningLoop
+ Durchmesser / Randabstand
+ RouteLine / DrillingCylinder
+ Konfliktchecks

Fragment in Semantik
= AccessZone / AlignmentLine / VisibilitySurface
+ räumliche Eigenschaften
+ Entwurfschecks

Bauteil in Logistik
= TransportEnvelope
+ CenterOfGravityPoint
+ LiftingZone / StorageSupportZone
+ Prozesschecks

Nachweis
= EvidenceZone / ScanLine / DamagePolygon
+ Konfidenz
+ betroffene Connectoren
+ Statusmodifikation
```

So wird jedes Paket präzise, prüfbar und maschinenlesbar, ohne jede reale Fläche, Kante oder Projektbesonderheit zu übermodellieren.
