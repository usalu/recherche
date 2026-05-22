# Finales Systemdokument für die Vorplanung  
# SharedConnectorPoint-System für das Entwerfen mit wiederverwendeten Bauteilen

**Version:** Vorplanung / frühe Entwurfsphase  
**Sprache:** Deutsch  
**Prinzip:** wenige strategisch gesetzte Punkt-Connectoren, paketübergreifend genutzt  
**Kernregel:** Ein Punkt. Mehrere Facets. Eine Verbindung. Frühe Checks.

---

## 0. Kurzfassung

Dieses Dokument reduziert das zuvor entwickelte SharedConnectorPoint-System auf das, was in der **Vorplanung** wirklich notwendig ist.

In der Vorplanung geht es noch nicht um finale Nachweise, Ausführungsdetails oder exakte Bemessung.  
Es geht um:

```text
Bauteile schnell vergleichen
Bauteile sinnvoll platzieren
Verbindungen grob prüfen
Passende Ports finden
Entwurfsoptionen bewerten
Risiken früh erkennen
Nachweisbedarf markieren
```

Das System modelliert deshalb nicht jedes Detail, sondern nur die wichtigsten Entscheidungspunkte.

```text
SharedConnectorPoint
= strategischer Punkt am Bauteil

Facet
= fachliche Bedeutung dieses Punktes

Port
= Kompatibilitätstyp

Host-Geometrie
= vereinfachte Geometrie, die im Vorcheck verwendet wird

Connection Passport
= Vorplanungs-Ergebnis einer Verbindung
```

Die wichtigste Änderung gegenüber der detaillierten Version:

```text
Vorplanung:
wenige Punkte
wenige Facets
grobe Checks
klare Warnungen
keine Ausführungsplanung
keine finale Bemessung
```

Beispiel:

```text
slab_edge_A_midpoint
│
├── StructuralFacet → bearing_side → grober Auflagercheck
├── SemanticFacet   → element_name + connector_sits_on: lange Plattenkante
├── EnergyFacet     → bridge_warning, nur falls Hülle
└── LogisticsFacet  → handling_warning, falls relevant
```

---

# 1. Quellenbasis

## 1.1 Abbau/Aufbau-Handbuch

Das Abbau/Aufbau-Handbuch wird in der Vorplanung vor allem als Quelle für folgende Punkte verwendet:

- Bauteilkatalog-Logik
- Bauteilidentität
- grobe Geometriedaten
- Masse / Volumen
- wiederverwendbare Stahlbetonelemente
- typische Anschlussfamilien
- Lager- und Transportrelevanz
- notwendige Nachweise für spätere Phasen

Für die Vorplanung wichtig ist besonders das Beispielelement:

```text
DE_1OG_001
Typologie: Deckenplatte
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

Quelle:  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

---

## 1.2 Abbau/Aufbau Masterarbeit 2020

Die Masterarbeit 2020 dient als Quelle für das Denken in **räumlichen Fragmenten**.

Für die Vorplanung wichtig sind nicht die Details der späteren Ausführung, sondern die Erkenntnis:

```text
Ein wiederverwendetes Betonfragment kann nicht nur Tragwerk sein.
Es kann auch eine räumliche Situation erzeugen:
Nische, Schwelle, Stütze-im-Raum, sichtbarer Schnitt, Wiederverwendungsausdruck.
```

Daraus wird die Systemtypologie `SlabBeamColumnFragment` abgeleitet:

```text
monolithisches Betonfragment
= Plattenbereich
+ integrierter Trägerbereich
+ Stützenabschnitt
+ Schnittflächen
+ räumliche Fragmentqualität
```

Quelle:  
https://abbauaufbau.de/project/masterarbeit-2020

---

## 1.3 ReCreate

ReCreate wird in der Vorplanung als Referenz für wiederverwendete Betonfertigteile genutzt, insbesondere für Hohlkammerdecken.

Wichtig für die Vorplanung:

- Hohlkammerdecken als wiederverwendbare Fertigteile
- Endauflager
- Längsfugen
- Heben / Transport
- BIM- oder QR-Tracking
- spätere Prüfung / Neuberechnung

Quellen:  
https://recreate-project.eu/project-pilots/the-netherlands/  
https://recreate-project.eu/project-pilots/finland/

---

# 2. Systemziel

Das System unterstützt die Vorplanung mit einem vorhandenen Bauteilpool.

Es soll beantworten:

```text
Welches Bauteil passt ungefähr wohin?
Welche Bauteile können andocken?
Welche Verbindungsideen sind plausibel?
Welche Risiken entstehen früh?
Welche Nachweise fehlen später?
Welche Entwurfspräferenz wird unterstützt?
```

Es soll in der Vorplanung **nicht** leisten:

```text
finale Statik
Ausführungsdetail
Ankerbemessung
Brandschutznachweis
finaler U-Wert-Nachweis
finale LCA
komplette Baustellenlogistik
Genehmigungsfähigkeit
```

Stattdessen erzeugt es:

```text
pass
warning
blocked for design
context_required
evidence_required
engineering_required later
```

---

# 3. Finales Kernprinzip

## 3.1 Nicht mehr: viele Paketpunkte

In der Vorplanung wäre es zu komplex, wenn jedes Paket eigene Punkte erzeugt:

```text
Tragwerkspunkt
Energiepunkt
TGA-Punkt
Semantikpunkt
Logistikpunkt
```

Das überfrachtet das Interface und macht das Matching schwer.

---

## 3.2 Stattdessen: wenige SharedConnectorPoints

Jedes Bauteil bekommt wenige strategische Punkte:

```text
Bauteil
→ wenige SharedConnectorPoints
→ Facets pro Punkt
→ grobe Vorplanungschecks
```

Ein Punkt kann mehrere Pakete bedienen.

Beispiel:

```text
Plattenkante
= Auflageridee
+ Fugen-/Rasteridee
+ mögliche Wärmebrücke
+ Montagezugang
```

---

# 4. Zentrale Begriffe

## 4.1 Component

Ein Bauteil oder Fragment aus dem Pool.

Beispiele:

```text
DE_1OG_001
SlabBeamColumnFragment
ReCreate Hollow-Core Slab
```

---

## 4.2 Package Representation

Eine vereinfachte fachliche Sicht auf das Bauteil.

In der Vorplanung sind diese Repräsentationen bewusst grob.

```text
Basisgeometrie:
Körper, Maße, Orientierung

Tragwerk:
Platte, Linie, Support-Zone, Transfer-Idee

Energie:
Hüllenkante, potenzielle Wärmebrücke, Dämmebene

TGA:
Öffnung, Route, Bohridee, Sperrzone

Semantik / Architektur:
Elementname + wo der Connector sitzt

Logistik:
Masse, Transporthülle, Hebe-/Lageridee

Nachweis:
bekannt / unbekannt / später prüfen
```

---

## 4.3 Host-Geometrie

Host-Geometrien bleiben erhalten, aber in der Vorplanung werden sie als grobe Prüfflächen oder Prüfzonen genutzt.

Beispiele:

| Paket | Host-Geometrie | Vorplanungszweck |
|---|---|---|
| Tragwerk | `SupportPatch2D` | grober Auflagerbereich |
| Tragwerk | `TransferNode` | grober Lastübergang |
| Energie | `BridgeZone` | Wärmebrückenwarnung |
| Energie | `InsulationInterface` | Dämmlogik erkennen |
| TGA | `OpeningLoop` | Öffnung nutzbar? |
| TGA | `BlockedZone` | Route vermeiden |
| Semantik | `ElementConnectorLabel` | Elementname + Sitz des Connectors |
| Logistik | `TransportEnvelope` | passt in Transport / Handling? |
| Logistik | `LiftingZone` | späterer Hebecheck nötig |
| Nachweis | `EvidenceStatus` | Daten bekannt oder fehlen |

---

## 4.4 SharedConnectorPoint

Ein SharedConnectorPoint ist ein strategischer Punkt am Bauteil.

Er speichert:

```text
Position
Familie
Elementname
wo der Punkt sitzt
aktive Facets
Ports
groben Status
fehlende Informationen
```

---

## 4.5 Facet

Ein Facet beschreibt, warum der Punkt für ein Paket relevant ist.

In der Vorplanung soll jedes Facet nur das Minimum enthalten:

```text
port
host_geometry_ref
check_level: vorplanung
status
message
```

---

## 4.6 Port

Ein Port definiert, welche Art von Andocken möglich ist.

Beispiele:

```text
bearing_side
support_side
alignment_port
opening_side
route_side
bridge_side
lifting_port
visibility_port
```

---

## 4.7 Evidence Modifier

In der Vorplanung ist Evidence kein detaillierter Prüfbericht.  
Es ist ein Status:

```text
known
unknown
missing
needs_scan
needs_engineer
needs_test_later
```

---

# 5. Datenmodell

## 5.1 Component

```yaml
Component:
  id: string
  typology: string
  material: string

  planning_phase: vorplanung

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
  direction: Vector3D optional

  element_name: string
  connector_sits_on: string

  facets:
    structural: StructuralFacet optional
    energy: EnergyFacet optional
    tga: TGAFacet optional
    semantic: SemanticFacet optional
    logistics: LogisticsFacet optional

  evidence_status:
    known: string[]
    missing: string[]
    needed_later: string[]

  global_status: ready | warning | blocked_for_design | context_required | evidence_required
```

---

## 5.3 Vereinfachtes Facet für Vorplanung

```yaml
Facet:
  package: structural | energy | tga | semantic | logistics
  port: string

  host_geometry_ref: string
  host_geometry_type: string

  check_level: vorplanung

  check:
    name: string
    result: pass | warning | blocked | context_required | evidence_required

  message: string
```

---

## 5.4 Connection Passport für Vorplanung

```yaml
ConnectionPassport:
  id: string

  point_A: SharedConnectorPoint.id
  point_B: SharedConnectorPoint.id

  planning_phase: vorplanung

  active_checks:
    structural: true | false
    energy: true | false
    tga: true | false
    semantic: true | false
    logistics: true | false

  results:
    structural: pass | warning | blocked | evidence_required | not_active
    energy: pass | warning | context_required | not_active
    tga: pass | warning | blocked | not_active
    semantic: pass | warning | not_active
    logistics: pass | warning | evidence_required | not_active

  missing_information:
    - string

  next_phase_requirements:
    - string
```

---

# 6. Paket-Repräsentationen und Host-Geometrien

## 6.1 Basisgeometrie

In der Vorplanung muss die Basisgeometrie nur genug liefern, um Bauteile zu platzieren und Punkte abzuleiten.

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| neutraler Körper | `SolidMesh` oder `BRep` | Bauteil sichtbar und platzierbar machen |
| Bounding Box | `OrientedBoundingBox` | Maße, Drehung, Transportabschätzung |
| Hauptflächen | `FaceSet` | Oberseite / Unterseite / Seiten ableiten |
| Hauptkanten | `EdgeSet` | Kantenpunkte ableiten |
| rohe Öffnungen | `OpeningLoop[]` | mögliche Öffnungen erkennen |
| lokale Achsen | `CoordinateFrame3D` | Orientierung im Entwurf |

---

## 6.2 Tragwerk

In der Vorplanung wird das Tragwerk als **Plausibilitätsmodell** genutzt, nicht als Nachweis.

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| Platte | `PlateElement2D` | erkennt: kann als Platte / Decke gedacht werden |
| Linie | `LineElement1D` | erkennt: Träger- oder Stützenrichtung |
| Auflagerbereich | `SupportPatch2D` | grober Auflager-Check |
| Fugenlinie | `JointLine` | Fuge / Nachbarbauteil plausibel? |
| Kontinuitätszone | `ContinuityZone` | Kraftschluss später möglich? |
| Transferknoten | `TransferNode` | grober Lastübergang |
| Strukturgraph | `StructuralGraph` | Fragment grob lesbar machen |

Keine finale Bemessung.  
Nur:

```text
plausibel
unplausibel
Nachweis später nötig
```

---

## 6.3 Energie / Gebäudehülle

In der Vorplanung wird Energie nur als Kontext- und Warnsystem genutzt.

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| thermische Fläche | `ThermalSurface` | liegt das Bauteil in der Hülle? |
| Dämmschnittstelle | `InsulationInterface` | Dämmung prinzipiell anschließbar? |
| Hüllenkante | `BoundaryEdge` | Hüllenanschluss erkennen |
| Durchdringung | `PenetrationLoop` | Abdichtung später nötig? |
| Wärmebrückenzone | `BridgeZone` | frühe Wärmebrückenwarnung |
| Feuchtezone | `MoistureRiskZone` | Kontextwarnung bei Dach / Boden / außen |

Keine finale Energieprüfung.  
Nur:

```text
Hülle relevant?
Dämmung anschließbar?
Wärmebrücke wahrscheinlich?
Abdichtung später nötig?
```

---

## 6.4 TGA / Öffnungen

In der Vorplanung wird TGA nur als **Routing- und Konfliktvorprüfung** genutzt.

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| Route | `RouteLine` | grobe Leitungsführung |
| Öffnung | `OpeningLoop` | Öffnung nutzbar? |
| Bohrkandidat | `DrillingCylinder` | Bohrung später prüfen |
| Sperrzone | `BlockedZone` | Tragwerk / sensible Zone vermeiden |
| Lichtraum | `ClearanceVolume` | grober Platzbedarf |

Keine finale TGA-Planung.  
Nur:

```text
Route denkbar?
Öffnung nutzbar?
Bohrung kritisch?
Kollision wahrscheinlich?
```

---

## 6.5 Semantik / Architektur

In der Vorplanung wird Semantik bewusst stark vereinfacht.

Sie beschreibt nicht komplexe architektonische Bedeutungen, sondern hilft beim Entwerfen und Matching vieler unterschiedlicher Elemente.

Deshalb speichert sie nur:

```text
Elementname
wo der Connector sitzt
einfache Entwurfsrolle
einfache Matching-Hilfe
```

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| Element-Label | `ElementConnectorLabel` | lesbarer Name des Elements / Bereichs |
| Sitzbeschreibung | `ConnectorPlacementLabel` | erklärt, wo der Punkt sitzt |
| Ausrichtungslinie | `AlignmentLine`, optional | Fuge / Raster grob ausrichten |
| Sichtreferenz | `VisibilityReference`, optional | sichtbar / nicht sichtbar markieren |
| Zugangsreferenz | `AccessReference`, optional | Zugang / Nische grob markieren |

Beispiele für Semantik:

```text
Element: Deckenplatte
Connector sitzt auf: lange Plattenkante A

Element: SlabBeamColumnFragment
Connector sitzt auf: Schnittfläche am Trägerbereich

Element: Hohlkammerdecke
Connector sitzt auf: Stirnauflager A
```

Das reicht für die Vorplanung, um Ports und Elemente zu matchen, ohne zu viele architektonische Spezialfälle zu erzeugen.

---

## 6.6 Logistik / Montage

In der Vorplanung ist Logistik ein Warn- und Machbarkeitscheck.

| Abstrakte Geometrie | Datentyp | Vorplanungszweck |
|---|---|---|
| Transporthülle | `TransportEnvelope` | grob: zu groß / handhabbar |
| Schwerpunkt | `CenterOfGravityPoint` | Hebecheck später nötig |
| Hebezone | `LiftingZone` | Hebbarkeit markieren |
| Lagerauflager | `StorageSupportZone` | Lagerung plausibel? |
| Montagezugang | `AccessVolume` | Anschluss erreichbar? |
| Schutzzone | `ProtectionZone` | sensible Kanten / Flächen |

Keine finale Montageplanung.  
Nur:

```text
massiv / schwer?
Transport grob möglich?
Heben später prüfen?
Lagerung plausibel?
Montagezugang blockiert?
```

---

## 6.7 Nachweis-Overlay

In der Vorplanung ist Nachweis ein Statussystem.

| Status | Bedeutung |
|---|---|
| `known` | Information liegt vor |
| `unknown` | Information unbekannt |
| `missing` | Information fehlt für sinnvollen Check |
| `needed_later` | in LP3 / Ausführung erforderlich |
| `blocks_design` | verhindert aktuelle Entwurfsentscheidung |

Beispiele:

```text
Bewehrung unbekannt → anchor_side nur warning
Materialtest fehlt → structural capacity evidence_required
QR bekannt → identity confirmed
Schaden unbekannt → visibility / support warning
```

---

# 7. SharedConnectorPoint-Familien

Für die Vorplanung reichen sechs Familien.

---

## 7.1 `support_edge_point`

Punkt an einer Kante oder Stirnseite, die als Auflager, Fuge, Rasterkante oder Hüllenkante dienen kann.

Typisch für:

```text
Deckenplattenkante
Wandkopf
Trägeroberseite
Hohlkammerdecken-Stirnseite
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| StructuralFacet | `bearing_side` / `support_side` | grob: liegt etwas richtig auf? |
| SemanticFacet | `alignment_port` | sitzt an welcher Kante / Fuge? |
| EnergyFacet | `bridge_side` | Hüllenkante? Wärmebrücke möglich? |
| LogisticsFacet | `access_port` | Anschluss erreichbar? |

---

## 7.2 `joint_line_point`

Punkt an einer Fuge oder Modulachse.

Typisch für:

```text
Platte-Platte-Fuge
Hohlkammerdecken-Längsfuge
Wand-Wand-Fuge
Fassadenfuge
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| StructuralFacet | `member_side` | Fuge / Verbindung plausibel? |
| SemanticFacet | `alignment_port` | Modul / Raster passt? |
| EnergyFacet | `thermal_side` | Hüllenfuge? |
| LogisticsFacet | `access_port` | Fuge montierbar? |

---

## 7.3 `opening_center_point`

Punkt im Zentrum einer Öffnung, eines Hohlraums oder einer möglichen Bohrung.

Typisch für:

```text
bestehende Öffnung
Schachtöffnung
Hohlkammer als Route
Bohrkandidat
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| TGAFacet | `opening_side` / `route_side` / `drilling_side` | Route denkbar? |
| EnergyFacet | `penetration_side` | Abdichtung später nötig? |
| StructuralFacet | warning | Nähe zu Tragzone kritisch? |
| SemanticFacet | `opening_port` | Öffnung entwerferisch relevant? |

---

## 7.4 `transfer_node_point`

Punkt an einem Last- oder Geometrieknoten.

Typisch für:

```text
SlabBeamColumnFragment-Knoten
Träger-Stützen-Knoten
Pilzkopfstütze
Stützenkopf
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| StructuralFacet | `transfer_side` | grober Lastpfad plausibel? |
| SemanticFacet | label only / `side_port` optional | welches Element / welcher Knoten? |
| EnergyFacet | `bridge_side` | bei Hülle: Wärmebrücke möglich? |
| LogisticsFacet | `temporary_bracing_port` | temporäre Stabilität später prüfen? |

---

## 7.5 `handling_point`

Punkt für Heben, Lagern, Transport oder Schutz.

Typisch für:

```text
Hebekandidat
Lagerauflagerpunkt
Transportreferenz
Schutzpunkt an Schnittkante
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| LogisticsFacet | `lifting_port` / `storage_port` / `transport_port` / `protection_port` | Handling plausibel? |
| EvidenceModifier | — | Hebe- oder Transportnachweis fehlt? |

---

## 7.6 `visibility_reference_point`

Punkt für sichtbare Wiederverwendung oder sichtbare Schnittflächen.

Typisch für:

```text
sichtbare Plattenunterseite
sichtbare Schnittfläche
sichtbare Bauteilmarkierung
```

Mögliche Facets:

| Facet | Port | Vorplanungscheck |
|---|---|---|
| SemanticFacet | `visibility_port` | sichtbar / verdeckt? |
| EvidenceModifier | — | Oberfläche / Schaden bekannt? |

Nur erzeugen, wenn Sichtbarkeit Teil der Entwurfsentscheidung ist.

---

# 8. Platzierungsregeln

## 8.1 Punkte erzeugen, wenn

```text
der Punkt eine Verbindungsidee ermöglicht
der Punkt für frühes Matching wichtig ist
der Punkt einen groben Check startet
der Punkt eine Warnung trägt
der Punkt für Entwurfspräferenz relevant ist
der Punkt späteren Nachweisbedarf sichtbar macht
```

---

## 8.2 Punkte nicht erzeugen, wenn

```text
er nur eine beliebige Fläche beschreibt
er keine Verbindungsidee hat
er keinen Vorplanungscheck startet
er keine Warnung erzeugt
er nur eine bestehende Kante dupliziert
```

---

## 8.3 Punkte zusammenführen, wenn

```text
sie an derselben realen Stelle sitzen
sie dieselbe Entwurfsentscheidung betreffen
ihre Facets sich sinnvoll ergänzen
kein Vorplanungscheck getrennte Punkte braucht
```

---

## 8.4 Punkte getrennt halten, wenn

```text
oben / unten unterschieden werden muss
innen / außen unterschieden werden muss
Heben und Auflagern bewusst unterschiedliche Orte sind
ein Sichtpunkt nicht gleich ein Auflagerpunkt ist
ein Bohrpunkt nicht gleich ein Tragwerkspunkt ist
```

---

## 8.5 Vorplanungs-Qualitätsregel

```text
1 Facet  = erlaubt, wenn für Entwurf wichtig
2 Facets = guter Punkt
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

---

## 9.2 System prüft grobes Docking

In der Vorplanung genügt:

```text
Punkte liegen nahe genug
Richtungen sind grob kompatibel
Bauteile überlappen nicht falsch
Platzierung ist plausibel
```

---

## 9.3 System findet kompatible Facets

Beispiel:

```text
A.StructuralFacet.port = bearing_side
B.StructuralFacet.port = support_side
→ struktureller Vorcheck aktiv

A.SemanticFacet.port = alignment_port
B.SemanticFacet.port = alignment_port
→ Matching / Ausrichtung aktiv

A.EnergyFacet.port = bridge_side
→ Wärmebrückenwarnung aktiv
```

---

## 9.4 System lädt Host-Geometrien

Beispiele:

```text
SupportPatch2D
AlignmentLine
BridgeZone
OpeningLoop
AccessVolume
StorageSupportZone
```

---

## 9.5 System führt Vorplanungschecks aus

```text
Tragwerk:
grob plausibel / kritisch / Nachweis später

Energie:
Hülle relevant / Wärmebrücke möglich / Kontext nötig

TGA:
Route denkbar / Bohrung kritisch / Öffnung nutzbar

Semantik:
Elementname + Connector sitzt wo?
Ausrichtung / Sichtbarkeit nur einfach

Logistik:
zu schwer? Hebecheck später? Montagezugang?

Nachweis:
bekannt / fehlt / später nötig
```

---

## 9.6 Ergebnis

Ein Connection Passport für Vorplanung.

Er ist kein Ausführungsnachweis.  
Er ist eine Entscheidungshilfe.

---

# 10. Paket-Facets und minimale Ports

## 10.1 StructuralFacet

In der Vorplanung reduziert auf Plausibilität.

| Port | Bedeutung | Vorplanungscheck |
|---|---|---|
| `bearing_side` | Bauteil gibt Last ab | kann aufliegen? |
| `support_side` | Bauteil nimmt Last auf | kann tragen / stützen? |
| `member_side` | Fuge / Bauteilseite | kann anschließen? |
| `anchor_side` | Ankeridee | Nachweis später nötig |
| `continuity_side` | Kraftschlussidee | Nachweis später nötig |
| `transfer_side` | Lastübergang | Lastpfad grob plausibel? |

---

## 10.2 EnergyFacet

| Port | Bedeutung | Vorplanungscheck |
|---|---|---|
| `thermal_side` | thermische Grenze | Hüllenkontext? |
| `insulation_side` | Dämmebene | Dämmung anschließbar? |
| `penetration_side` | Durchdringung | Abdichtung später nötig? |
| `bridge_side` | Wärmebrücke | Warnung |

---

## 10.3 TGAFacet

| Port | Bedeutung | Vorplanungscheck |
|---|---|---|
| `route_side` | Leitung / Route | Route denkbar? |
| `opening_side` | Öffnung | nutzbar? |
| `drilling_side` | Bohrung | kritisch? |
| `blocked_side` | Sperrzone | Route vermeiden |

---

## 10.4 SemanticFacet

In der Vorplanung stark vereinfacht.

| Port | Bedeutung | Vorplanungscheck |
|---|---|---|
| `alignment_port` | Fuge / Raster / Modul | passt ungefähr? |
| `visibility_port` | sichtbar / verdeckt | Entwurfsabsicht? |
| `access_port` | Zugang / Nische | grob zugänglich? |
| `side_port` | Seite / Orientierung | welche Seite? |
| `opening_port` | Öffnungsbezug | welche Öffnung? |
| `top_port` / `bottom_port` | oben / unten | vertikale Zuordnung |

Semantik speichert immer:

```text
element_name
connector_sits_on
```

Beispiel:

```text
element_name: Deckenplatte
connector_sits_on: lange Kante A
```

---

## 10.5 LogisticsFacet

| Port | Bedeutung | Vorplanungscheck |
|---|---|---|
| `lifting_port` | Heben | Hebecheck später |
| `storage_port` | Lagerung | Lagerung plausibel? |
| `transport_port` | Transport | Transporthülle kritisch? |
| `access_port` | Montagezugang | Zugang blockiert? |
| `protection_port` | Schutz | sensible Fläche / Kante? |
| `temporary_bracing_port` | temporäre Stabilität | später prüfen |

---

# 11. Kompatibilitätsregeln

In der Vorplanung sind Kompatibilitätsregeln bewusst grob.

| Regel | Punkt-Port-Docking | Vorplanungscheck |
|---|---|---|
| Auflager | `bearing_side → support_side` | liegt plausibel auf? Mindestauflager später prüfen |
| Ankeridee | `anchor_side → support_side` | prinzipiell denkbar? Rebar-Nachweis später |
| Kraftschlussidee | `continuity_side → continuity_side` | Anschlussfamilie denkbar? Engineering später |
| Fuge | `member_side → member_side` | Fuge / Ausrichtung plausibel? |
| Lasttransfer | `transfer_side → support_side / bearing_side` | Lastpfad grob plausibel? |
| Hülle | `thermal_side → thermal_side` | Hüllenkontinuität möglich? |
| Dämmung | `insulation_side → insulation_side` | Dämmung anschließbar? |
| Durchdringung | `penetration_side → thermal_side / insulation_side` | Abdichtung später nötig |
| Wärmebrücke | `bridge_side` | Warnung |
| Route | `route_side → route_side` | Leitungsführung denkbar? |
| Öffnung | `opening_side → route_side` | Öffnung nutzbar? |
| Bohrung | `drilling_side → route_side` | kritisch, Nachweis später |
| Sperrzone | `blocked_side` | vermeiden |
| Ausrichtung | `alignment_port → alignment_port` | Raster / Fuge grob passend |
| Sichtbarkeit | `visibility_port` | sichtbar / verdeckt |
| Heben | `lifting_port` | Hebecheck später |
| Lagerung | `storage_port` | Lagerung plausibel |
| Transport | `transport_port` | Transport grob möglich |
| Montagezugang | `access_port` | zugänglich? |
| Schutz | `protection_port` | Schutzbedarf markieren |

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

## 12.2 Paket-Repräsentationen für Vorplanung

| Paket | Repräsentation | Vorplanungszweck |
|---|---|---|
| Basisgeometrie | neutraler Plattenkörper | Größe, Orientierung, Platzierung |
| Tragwerk | Platte mit möglichen Auflagerkanten | grob tragende Platzierung |
| Energie | nur falls Hülle | Wärmebrücken- / Dämmwarnung |
| TGA | nur falls Öffnung / Bohrung | Route oder Konflikt |
| Semantik | Elementname + Sitz des Connectors | einfaches Matching vieler Elemente |
| Logistik | Masse / Transport / Lagerung | Handlingwarnung |
| Nachweis | Status | was fehlt später? |

---

## 12.3 Perfekt platzierte minimale SharedConnectorPoints

Für Vorplanung reichen:

```text
1. slab_edge_A_midpoint
2. slab_edge_B_midpoint
3. slab_visibility_reference, nur falls sichtbar geplant
4. slab_lifting_reference
5. slab_storage_reference
6. slab_opening_center, nur falls Öffnung / Route relevant
```

---

## 12.4 Punkt 1 — `slab_edge_A_midpoint`

**Familie:** `support_edge_point`  
**Elementname:** Deckenplatte  
**Connector sitzt auf:** langer Plattenkante A  
**Warum hier?**  
Diese Kante ist wahrscheinlich Auflager, Fuge, Rasterkante, mögliche Wärmebrücke und Montagekante.

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | kann auf Wand / Träger aufliegen? |
| StructuralFacet optional | `anchor_side` | `AnchorZone2D` | Ankeridee möglich, Nachweis später |
| StructuralFacet optional | `continuity_side` | `ContinuityZone` | Kraftschlussidee möglich, Nachweis später |
| SemanticFacet | `alignment_port` | `ElementConnectorLabel` + optional `AlignmentLine` | Element: Deckenplatte; sitzt auf langer Kante A |
| EnergyFacet | `bridge_side` | `BridgeZone` | nur Warnung, falls Hülle |
| LogisticsFacet | `access_port` | `AccessVolume` | Anschluss erreichbar? |

---

## 12.5 Punkt 2 — `slab_edge_B_midpoint`

**Elementname:** Deckenplatte  
**Connector sitzt auf:** langer Plattenkante B

Gleiche Logik wie Kante A.  
Wichtig, wenn die Platte zweiseitig gelagert, im Raster ausgerichtet oder als Modul wiederholt wird.

---

## 12.6 Punkt 3 — `slab_visibility_reference`

**Familie:** `visibility_reference_point`  
**Elementname:** Deckenplatte  
**Connector sitzt auf:** Plattenunterseite  
**Nur erzeugen, wenn Sichtbarkeit Teil des Entwurfs ist.**

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| SemanticFacet | `visibility_port` | `VisibilityReference` | Unterseite sichtbar / verdeckt? |
| EvidenceModifier | — | `EvidenceStatus` | Oberfläche / Schaden unbekannt? |

---

## 12.7 Punkt 4 — `slab_lifting_reference`

**Familie:** `handling_point`  
**Elementname:** Deckenplatte  
**Connector sitzt auf:** Hebereferenz / Schwerpunktnähe

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Hebecheck später nötig |
| EvidenceModifier | — | `EvidenceStatus` | Hebedaten fehlen? |

---

## 12.8 Punkt 5 — `slab_storage_reference`

**Familie:** `handling_point`  
**Elementname:** Deckenplatte  
**Connector sitzt auf:** Unterseite / Lagerauflager

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| LogisticsFacet | `storage_port` | `StorageSupportZone` | liegende Lagerung plausibel? |
| LogisticsFacet optional | `protection_port` | `ProtectionZone` | Schutzbedarf? |

---

## 12.9 Punkt 6 — `slab_opening_center`

**Familie:** `opening_center_point`  
**Elementname:** Deckenplatte  
**Connector sitzt auf:** Zentrum einer bestehenden oder geplanten Öffnung  
**Nur erzeugen, wenn Öffnung oder Route relevant ist.**

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| TGAFacet | `opening_side` | `OpeningLoop` | Öffnung nutzbar? |
| TGAFacet optional | `drilling_side` | `DrillingCylinder` | Bohridee kritisch? |
| EnergyFacet optional | `penetration_side` | `PenetrationLoop` | Abdichtung später nötig |
| StructuralFacet warning | — | `BlockedZone` | Tragwerkskonflikt möglich |

---

## 12.10 Verbindung: Decke–Wand

```text
slab_edge_A_midpoint
dockt an
wall_top_midpoint
```

Vorplanungs-Ergebnis:

| Paket | Ergebnis |
|---|---|
| Tragwerk | Auflageridee plausibel / Nachweis später |
| Semantik | Deckenplatte lange Kante A dockt an Wandkopf |
| Energie | Wärmebrücke nur relevant, wenn Hülle |
| Logistik | Montagezugang grob prüfen |
| Nachweis | Bewehrung / Anker / Material später prüfen |

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

## 13.2 Paket-Repräsentationen für Vorplanung

| Paket | Repräsentation | Vorplanungszweck |
|---|---|---|
| Basisgeometrie | monolithischer Körper mit Teilregionen | Fragment sichtbar und platzierbar machen |
| Tragwerk | Platte + Trägerlinie + Stützenlinie + Transferknoten | grober Lastpfad |
| Energie | nur falls Hülle | Wärmebrückenwarnung |
| TGA | Bohr- und Sperrzonenmodell | kritische Zonen vermeiden |
| Semantik | Elementname + Sitz des Connectors | Fragmentrollen einfach matchen |
| Logistik | komplexes Handlingmodell | Hebe- / Schutz- / Stabilitätswarnung |
| Nachweis | Schnittfläche / Schaden / Bewehrung | später prüfen |

---

## 13.3 Perfekt platzierte minimale SharedConnectorPoints

Für Vorplanung reichen:

```text
1. fragment_transfer_node
2. fragment_cut_face_point
3. fragment_plate_edge_point
4. fragment_column_base_or_head_point
5. fragment_niche_access_point
6. fragment_lifting_reference
```

---

## 13.4 Punkt 1 — `fragment_transfer_node`

**Familie:** `transfer_node_point`  
**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Knoten zwischen Plattenbereich, Trägerbereich und Stützenabschnitt  
**Warum hier?**  
Hier bündeln sich Lastpfad, räumliche Identität und mögliche Stabilitätsrisiken.

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `transfer_side` | `StructuralGraph` + `TransferNode` | Lastpfad grob plausibel? |
| SemanticFacet | `side_port` oder nur Label | `ElementConnectorLabel` | Element: Fragment; sitzt auf Transferknoten |
| EnergyFacet optional | `bridge_side` | `BridgeZone` | Wärmebrücke, falls Hülle |
| LogisticsFacet optional | `temporary_bracing_port` | `TemporaryBracingZone` | temporäre Stabilität später prüfen |
| EvidenceModifier | — | `EvidenceStatus` | Rebar / Schaden unbekannt? |

---

## 13.5 Punkt 2 — `fragment_cut_face_point`

**Familie:** kombinierter Schnittflächenpunkt  
**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Schnittfläche des Fragments  
**Warum hier?**  
Die Schnittfläche ist Anschlussidee, sichtbarer ReUse-Ausdruck und Schutzrisiko.

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `continuity_side` | `ContinuityZone` | Kraftschlussidee möglich? |
| SemanticFacet | `visibility_port` | `VisibilityReference` | Schnittfläche sichtbar? |
| LogisticsFacet | `protection_port` | `ProtectionZone` | Schnittfläche schützen? |
| EvidenceModifier | — | `EvidenceStatus` | Bewehrung / Schaden später prüfen |

---

## 13.6 Punkt 3 — `fragment_plate_edge_point`

**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Rand des Plattenbereichs

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | kann der Plattenbereich aufliegen? |
| SemanticFacet | `alignment_port` | `ElementConnectorLabel` + optional `AlignmentLine` | Plattenkante / Raster / Kante |
| EnergyFacet optional | `bridge_side` | `BridgeZone` | Hüllenkante? |
| LogisticsFacet optional | `access_port` | `AccessVolume` | Montagezugang? |

---

## 13.7 Punkt 4 — `fragment_column_base_or_head_point`

**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Stützenfuß oder Stützenkopf

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `support_side` | `Node` / `SupportPatch2D` | kann Last aufnehmen / abgeben? |
| SemanticFacet | `side_port` | `ElementConnectorLabel` | Stützenabschnitt identifizieren |
| LogisticsFacet optional | `temporary_bracing_port` | `TemporaryBracingZone` | Stabilisierung später? |
| EvidenceModifier | — | `EvidenceStatus` | Schaden / Unsicherheit? |

---

## 13.8 Punkt 5 — `fragment_niche_access_point`

**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Nischenzugang / räumlicher Schwelle

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| SemanticFacet | `access_port` | `AccessReference` | Nische / Zugang grob nutzbar? |
| SemanticFacet optional | `side_port` | `ElementConnectorLabel` | welche Seite / welcher Raumbezug? |
| EvidenceModifier optional | — | `EvidenceStatus` | sichtbarer Schaden? |

---

## 13.9 Punkt 6 — `fragment_lifting_reference`

**Elementname:** SlabBeamColumnFragment  
**Connector sitzt auf:** Hebereferenz des unregelmäßigen Fragments

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Hebecheck später nötig |
| LogisticsFacet optional | `storage_port` | `StorageSupportZone` | Lagerung kritisch? |
| EvidenceModifier | — | `EvidenceStatus` | Hebe- / Materialdaten fehlen? |

---

## 13.10 Verbindung: Fragment auf neuem Träger

```text
fragment_cut_face_point
oder
fragment_plate_edge_point
dockt an
new_beam_support_point
```

Vorplanungs-Ergebnis:

| Paket | Ergebnis |
|---|---|
| Tragwerk | Lastpfad / Kraftschlussidee plausibel oder kritisch |
| Semantik | Fragmentkante / Schnittfläche dockt an neuen Träger |
| Logistik | Montage / Schutz / temporäre Stabilität prüfen |
| Nachweis | Schnittflächenbewehrung später zwingend prüfen |
| Energie | nur falls Hülle |

---

# 14. Beispiel C — ReCreate Hollow-Core Slab

## 14.1 Komponente

```text
ReCreate Hollow-Core Slab
= wiedergewonnene Hohlkammerdecke mit:
  - einachsiger Spannrichtung
  - Stirnauflagerzonen
  - Längsfugen
  - Hohlkammern
  - Hebe-, Transport- und Trackinghistorie
```

---

## 14.2 Paket-Repräsentationen für Vorplanung

| Paket | Repräsentation | Vorplanungszweck |
|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | Größe, Stirnseiten, Hohlräume erkennen |
| Tragwerk | einachsig spannende Platte | Endauflager und Fuge grob prüfen |
| Energie | nur falls Dach / Außenboden | Wärmebrücken- / Dämmwarnung |
| TGA | Hohlraum- oder Bohrmodell | Route nur falls genutzt |
| Semantik | Elementname + Sitz des Connectors | Modul / Fuge einfach matchen |
| Logistik | Hebe-, Transport-, Lagermodell | Handlingwarnung |
| Nachweis | BIM / QR / Teststatus | später prüfen / bestätigen |

---

## 14.3 Perfekt platzierte minimale SharedConnectorPoints

Für Vorplanung reichen:

```text
1. hcs_end_A_midpoint
2. hcs_end_B_midpoint
3. hcs_long_joint_midpoint
4. hcs_void_route_point, nur wenn Hohlraum als Route genutzt wird
5. hcs_lifting_reference
6. hcs_qr_reference, nur wenn Tracking räumlich relevant ist
```

---

## 14.4 Punkt 1 — `hcs_end_A_midpoint`

**Familie:** `support_edge_point`  
**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** Stirnauflager A  
**Warum hier?**  
Der Punkt deckt Endauflager, Transport / Lagerung, Modulbezug und mögliche Hüllenkante ab.

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | Endauflager plausibel? |
| LogisticsFacet | `transport_port` oder `storage_port` | `TransportSupportZone` / `StorageSupportZone` | Transport / Lagerung grob plausibel? |
| SemanticFacet | `alignment_port` | `ElementConnectorLabel` + optional `AlignmentLine` | Element: Hohlkammerdecke; sitzt auf Stirnauflager A |
| EnergyFacet optional | `bridge_side` | `BridgeZone` | Wärmebrücke, falls Dach / Außenboden |

---

## 14.5 Punkt 2 — `hcs_end_B_midpoint`

**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** Stirnauflager B

Gleiche Logik wie `hcs_end_A_midpoint`.  
Notwendig, weil eine Hohlkammerdecke zwei Endauflager braucht.

---

## 14.6 Punkt 3 — `hcs_long_joint_midpoint`

**Familie:** `joint_line_point`  
**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** Längsfuge

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| StructuralFacet | `member_side` | `JointLine` | Fuge / Wiederverbindung plausibel? |
| SemanticFacet | `alignment_port` | `ElementConnectorLabel` + optional `AlignmentLine` | Element: Hohlkammerdecke; sitzt auf Längsfuge |
| EnergyFacet optional | `thermal_side` | `BoundaryEdge` | Hüllenfuge? |
| LogisticsFacet optional | `access_port` | `AccessVolume` | Fuge montierbar? |

---

## 14.7 Punkt 4 — `hcs_void_route_point`

**Familie:** `opening_center_point`  
**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** Hohlkammerachse  
**Nur erzeugen, wenn Hohlraum als Route genutzt wird.**

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| TGAFacet | `route_side` | `RouteLine` | Route durch Hohlraum denkbar? |
| TGAFacet optional | `drilling_side` | `DrillingCylinder` | Bohrung zum Hohlraum kritisch? |
| EnergyFacet optional | `penetration_side` | `PenetrationLoop` | Abdichtung später nötig |
| StructuralFacet warning | — | `BlockedZone` | Tragwerkskonflikt möglich |

---

## 14.8 Punkt 5 — `hcs_lifting_reference`

**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** Hebereferenz / Hebezone

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| LogisticsFacet | `lifting_port` | `LiftingZone` | Heben später prüfen |
| EvidenceModifier | — | `EvidenceStatus` | Hebe- / Transportdaten fehlen? |

---

## 14.9 Punkt 6 — `hcs_qr_reference`

**Elementname:** Hohlkammerdecke  
**Connector sitzt auf:** QR- / ID-Position, falls räumlich relevant

| Facet | Port | Host-Geometrie | Vorplanungscheck |
|---|---|---|---|
| SemanticFacet optional | `visibility_port` | `VisibilityReference` | QR / ID sichtbar? |
| EvidenceModifier | — | `EvidenceStatus` | Identität / Tracking bestätigt? |

---

## 14.10 Verbindung: Hohlkammerdecke auf Auflager

```text
hcs_end_A_midpoint
dockt an
support_wall_or_beam_point
```

Vorplanungs-Ergebnis:

| Paket | Ergebnis |
|---|---|
| Tragwerk | Endauflager plausibel, Nachweis später |
| Semantik | Hohlkammerdecke Stirnauflager A dockt an Auflager |
| Logistik | Transport / Lager / Montage grob relevant |
| Energie | Wärmebrücke nur bei Hüllenkontext |
| Nachweis | QR, Test, Neuberechnung später wichtig |

---

# 15. Interface-Logik

## 15.1 Bauteilmodus

Das Interface zeigt pro Bauteil nur wenige Punkte.

Pro Punkt sichtbar:

```text
Punktname
Familie
Elementname
Connector sitzt auf
aktive Facets
Ports
Vorplanungsstatus
fehlende Informationen
mögliche Matching-Partner
```

Beispiel:

```text
slab_edge_A_midpoint

Element:
Deckenplatte

Connector sitzt auf:
lange Plattenkante A

Facets:
- Structural: bearing_side
- Semantic: alignment_port
- Energy: bridge_side, context required
- Logistics: access_port

Status:
warning: Bewehrung / Anschlussnachweis später nötig
```

---

## 15.2 Verbindungsmodus

Beim Verbinden zweier Punkte zeigt das Interface:

```text
Docking plausibel?
Tragwerk plausibel?
Hülle relevant?
TGA-Konflikt?
Elemente / Ports passen?
Logistik kritisch?
Welche Nachweise fehlen später?
```

---

## 15.3 Semantik-Anzeige

Semantik wird bewusst einfach gezeigt:

```text
Elementname:
Deckenplatte

Connector sitzt auf:
lange Plattenkante A

Matching-Hinweis:
passt zu support_edge_point eines Wandkopfs oder Trägers
```

Keine komplexe semantische Ontologie in der Vorplanung.

---

# 16. Warum die Punkte jetzt korrekt platziert sind

## 16.1 Sie sitzen an Vorplanungsentscheidungen

Nicht jede Kante bekommt einen Punkt.  
Nur Orte, an denen eine frühe Entscheidung entsteht:

```text
Auflageridee
Fuge / Raster
Öffnung / Route
Transferknoten
Schnittfläche
Hebung / Lagerung
Sichtbarkeit
```

---

## 16.2 Sie bündeln mehrere Facets

Ein guter Punkt deckt mehrere Fragen ab:

```text
Kann es tragen?
Kann es andocken?
Wie heißt das Element?
Wo sitzt der Connector?
Ist Hülle betroffen?
Ist Montage möglich?
Welche Daten fehlen?
```

---

## 16.3 Sie vermeiden Overmodeling

Die Vorplanung braucht keine vollständige Ausführungslogik.

Deshalb werden reduziert:

```text
keine exakten Ankerdetails
keine vollständige U-Wert-Berechnung
keine finale Statik
keine vollständige TGA-Planung
keine komplexe Semantik
keine komplette Montageplanung
```

---

## 16.4 Sie bleiben erweiterbar

Was in der Vorplanung nur Warning ist, kann in späteren Phasen detailliert werden:

```text
anchor_side
→ Ausführungsdetail / Bemessung

bridge_side
→ Wärmebrückenberechnung

lifting_port
→ Hebeplan

visibility_port
→ Material- / Oberflächenbewertung

EvidenceStatus
→ Prüfbericht / Scan / Nachweis
```

---

# 17. Finale Systemregel

Für die Vorplanung lautet die finale Struktur:

```text
Component
→ vereinfachte Package Representations
→ wenige SharedConnectorPoints
→ einfache Facets
→ Ports für Matching
→ grobe Vorplanungschecks
→ Connection Passport
→ Liste fehlender Nachweise für spätere Phasen
```

Die wichtigste Kurzform:

```text
Ein Punkt.
Mehrere Facets.
Einfaches Matching.
Frühe Warnungen.
Keine Ausführungsplanung.
```

---

# 18. Praktische Implementierungsreihenfolge

## Schritt 1 — Basisgeometrie importieren

```text
SolidMesh / BRep
Bounding Box
FaceSet
EdgeSet
OpeningLoop
CoordinateFrame
```

---

## Schritt 2 — einfache Paket-Repräsentationen erzeugen

```text
PlateElement2D
SupportPatch2D
BridgeZone
OpeningLoop
ElementConnectorLabel
TransportEnvelope
EvidenceStatus
```

---

## Schritt 3 — Kandidatenpunkte erzeugen

```text
Kantenmittelpunkte
Stirnflächenmittelpunkte
Fugenmittelpunkte
Öffnungszentren
Transferknoten
Schnittflächenpunkte
Hebereferenzen
Lagerreferenzen
Sichtreferenzen
```

---

## Schritt 4 — Facets anhängen

```text
liegt auf Auflagerbereich → StructuralFacet
liegt auf Fuge / Kante → SemanticFacet mit element_name + connector_sits_on
liegt an Hüllenkante → EnergyFacet warning
liegt auf Öffnung / Route → TGAFacet
liegt auf Hebe- / Lagerzone → LogisticsFacet
hat fehlende Daten → EvidenceStatus
```

---

## Schritt 5 — Punkte zusammenführen

```text
gleiche reale Stelle
gleiche Entwurfsentscheidung
kompatible Facets
kein Grund zur Trennung
```

---

## Schritt 6 — unnötige Punkte löschen

```text
kein aktives Facet
kein Matching
kein Vorplanungscheck
keine Warnung
→ löschen
```

---

## Schritt 7 — Connection Passport erzeugen

Jede Verbindung erzeugt einen Vorplanungs-Connection-Passport mit:

```text
pass / warning / blocked / context_required / evidence_required
```

---

# 19. Endergebnis

Das reduzierte Vorplanungssystem ist:

```text
klein genug für ein klares Interface
konkret genug für echte Bauteile
abstrakt genug für viele Typologien
präzise genug für frühe Warnungen
offen genug für spätere Nachweise
```

Für jedes Bauteil gilt:

```text
wenige SharedConnectorPoints
jeder Punkt hat einfache Facets
Semantik nennt Element + Sitz des Connectors
Tragwerk prüft grobe Plausibilität
Energie warnt bei Hüllenkontext
TGA warnt bei Route / Öffnung / Bohrung
Logistik warnt bei Handling
Nachweisstatus markiert spätere Arbeit
```

Damit unterstützt das System genau die Vorplanung:

```text
Bauteile auswählen
Bauteile platzieren
Bauteile andocken
Ports matchen
Risiken früh sehen
Nachweise für später markieren
```
