# SharedConnectorPoint-System  
## Minimale punktbasierte Connectoren mit paketübergreifenden Facets

**Ziel**  
Dieses Dokument beschreibt die nächste, reduzierte Systemlogik:

```text
Ein Bauteil bekommt nicht pro Paket eigene Connectoren.
Ein Bauteil bekommt wenige strategische SharedConnectorPoints.
Jeder SharedConnectorPoint kann mehrere Paket-Facets tragen.
Eine Verbindung dockt zwei Punkte.
Die Pakete teilen sich diese Verbindung und führen ihre jeweiligen Checks aus.
```

Dadurch bleibt die Komponente einfach, während die Verbindung reich an Information wird.

---

# 1. Grundidee

## 1.1 Bisherige Logik

Bisher konnte jedes Paket eigene Punkt-Connectoren erzeugen:

```text
Tragwerkspunkt
Energiepunkt
TGA-Punkt
Semantikpunkt
Logistikpunkt
```

Das führt schnell zu Dopplungen, weil dieselbe reale Stelle oft in mehreren Paketen relevant ist.

Beispiel einer Plattenkante:

```text
Tragwerk:
Auflagerpunkt

Semantik:
Fugen- oder Rasterpunkt

Energie:
Wärmebrückenpunkt

Logistik:
Montagezugangspunkt
```

Alle liegen geometrisch oft an derselben Stelle.

## 1.2 Neue Logik

Die neue Lösung ist:

```text
ein strategischer SharedConnectorPoint
+ mehrere Paket-Facets
```

Beispiel:

```text
slab_edge_A_midpoint
│
├── StructuralFacet
│   └── bearing_side
│
├── SemanticFacet
│   └── alignment_port
│
├── EnergyFacet
│   └── bridge_side, nur wenn Hüllenkontext aktiv
│
└── LogisticsFacet
    └── access_port, nur wenn Montagezugang geprüft wird
```

Ein Punkt kann also mehrere Bedeutungen tragen.

---

# 2. Zentrale Regel

```text
Connectoren sind immer Punkte.
```

Aber:

```text
Der Punkt ersetzt nicht die fachliche Prüfgeometrie.
```

Die saubere Trennung lautet:

```text
SharedConnectorPoint
= Docking-Punkt

Facet
= paket-spezifische Bedeutung dieses Punktes

Port
= Kompatibilitätstyp innerhalb eines Facets

Host-Geometrie
= Linie, Fläche, Zone oder Volumen, die für den Check geprüft wird

Regel
= dockt zwei Punkte und prüft die Host-Geometrien der aktiven Facets
```

---

# 3. Neues Datenmodell

## 3.1 Component-Level

```text
Component
│
├── BaseGeometry
│
├── PackageRepresentations
│   ├── StructuralRepresentation
│   ├── EnergyRepresentation
│   ├── TGARepresentation
│   ├── SemanticRepresentation
│   ├── LogisticsRepresentation
│   └── EvidenceOverlay
│
└── SharedConnectorPoints
```

## 3.2 SharedConnectorPoint-Level

```text
SharedConnectorPoint
│
├── Punktgeometrie
├── lokale Richtung
├── lokaler Frame
├── Host-Feature
│
├── StructuralFacet
├── EnergyFacet
├── TGAFacet
├── SemanticFacet
├── LogisticsFacet
└── EvidenceModifiers
```

## 3.3 Connection-Level

```text
Connection
│
├── SharedConnectorPoint A
├── SharedConnectorPoint B
│
├── StructuralResult
├── EnergyResult
├── TGAResult
├── SemanticResult
├── LogisticsResult
└── EvidenceResult
```

---

# 4. SharedConnectorPoint-Schema

```yaml
SharedConnectorPoint:
  id: string
  component_id: string

  point: Point3D
  local_frame: CoordinateFrame3D
  direction: Vector3D
  host_feature_ref: string

  facets:
    structural:
      port: string
      host_geometry_ref: string
      host_geometry_type: string
      active_checks: string[]

    energy:
      port: string
      host_geometry_ref: string
      host_geometry_type: string
      active_checks: string[]

    tga:
      port: string
      host_geometry_ref: string
      host_geometry_type: string
      active_checks: string[]

    semantic:
      port: string
      host_geometry_ref: string
      host_geometry_type: string
      active_checks: string[]

    logistics:
      port: string
      host_geometry_ref: string
      host_geometry_type: string
      active_checks: string[]

  evidence_modifiers:
    - evidence_ref: string
      affected_facet: string
      effect: confirmed | warning | blocked | evidence_required | engineering_required
      reason: string

  status: active | warning | blocked | evidence_required | engineering_required
```

---

# 5. Begriffsklärung

## 5.1 SharedConnectorPoint

Ein Punkt im Raum, an dem ein Bauteil andocken kann.

Er beantwortet:

```text
Wo wird verbunden, geprüft oder angedockt?
```

## 5.2 Facet

Ein paket-spezifischer Bedeutungsanteil eines SharedConnectorPoints.

Es beantwortet:

```text
Warum ist dieser Punkt für ein bestimmtes Paket relevant?
```

Beispiele:

```text
StructuralFacet:
dieser Punkt ist ein Auflagerpunkt

EnergyFacet:
dieser Punkt liegt an einer Wärmebrückenzone

SemanticFacet:
dieser Punkt liegt auf einer Fugen- oder Rasterlinie

LogisticsFacet:
dieser Punkt ist montage- oder lagerrelevant
```

## 5.3 Port

Der Port beschreibt die Kompatibilität innerhalb eines Facets.

Beispiele:

```text
bearing_side
support_side
alignment_port
bridge_side
route_side
lifting_port
```

## 5.4 Host-Geometrie

Die Host-Geometrie ist die eigentliche fachliche Prüfgeometrie.

Beispiele:

```text
SupportPatch2D
AlignmentLine
BridgeZone
OpeningLoop
LiftingZone
VisibilitySurface
```

Der Punkt dockt.  
Die Host-Geometrie wird geprüft.

---

# 6. Warum SharedConnectorPoints sinnvoll sind

## 6.1 Weniger Connectoren

Statt pro Paket eigene Punkte zu erzeugen:

```text
slab_edge_structural_point
slab_edge_semantic_point
slab_edge_energy_point
slab_edge_logistics_point
```

wird ein Punkt erzeugt:

```text
slab_edge_A_midpoint
```

mit mehreren Facets.

## 6.2 Bessere Verbindungspässe

Wenn zwei SharedConnectorPoints verbunden werden, entsteht ein gemeinsamer Connection Passport:

```text
Connection Passport
│
├── structural check
├── energy check
├── TGA check
├── semantic check
├── logistics check
└── evidence effects
```

Eine Verbindung wird dadurch nicht nur als statisches Detail verstanden, sondern als **paketübergreifender Entwurfszustand**.

## 6.3 Weniger Interface-Chaos

Die Benutzeroberfläche muss nicht fünf überlagerte Punkte zeigen.  
Sie zeigt einen Punkt, der mehrere Facets besitzt.

---

# 7. Minimale SharedConnectorPoint-Familien

Diese Familien sind keine Paket-Connectoren.  
Sie beschreiben strategische Punktpositionen auf Bauteilen.

## 7.1 `support_edge_point`

Ein Punkt auf einer Kante, Linie oder Randzone, die tragen, ausrichten, anschließen oder warnen kann.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| StructuralFacet | `bearing_side` oder `support_side` | `SupportPatch2D` |
| SemanticFacet | `alignment_port` | `AlignmentLine` |
| EnergyFacet | `bridge_side`, falls Hülle | `BridgeZone` |
| LogisticsFacet | `access_port`, falls Montage relevant | `AccessVolume` |

Typische Beispiele:

```text
Plattenkante
Wandkopf
Trägeroberseite
Hohlkammerdecken-Stirnseite
```

---

## 7.2 `joint_line_point`

Ein Punkt auf einer Fuge, Modulachse oder Verbindungslinie.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| StructuralFacet | `member_side` | `JointLine` |
| SemanticFacet | `alignment_port` | `AlignmentLine` |
| EnergyFacet | `thermal_side`, falls Hüllenfuge | `BoundaryEdge` |
| LogisticsFacet | `access_port`, falls Fuge montiert werden muss | `AccessVolume` |

Typische Beispiele:

```text
Hohlkammerdecken-Längsfuge
Wand-Wand-Fuge
Platte-Platte-Fuge
Fassadenfuge
```

---

## 7.3 `opening_center_point`

Ein Punkt im Zentrum einer Öffnung, eines Hohlraums oder einer Durchdringung.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| TGAFacet | `opening_side` oder `route_side` | `OpeningLoop` oder `RouteLine` |
| EnergyFacet | `penetration_side`, falls Hülle | `PenetrationLoop` |
| SemanticFacet | `opening_port`, falls architektonische Öffnung | `OpeningAxis` |
| StructuralFacet | meist nur Warnbezug | `BlockedZone` oder `SupportPatch2D` |

Typische Beispiele:

```text
bestehende Öffnung
Schachtöffnung
Hohlkammer als Route
geplante Kernbohrung
```

---

## 7.4 `transfer_node_point`

Ein Punkt, an dem Lasten, Geometrien oder Bedeutungen zusammenlaufen.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| StructuralFacet | `transfer_side` | `TransferNode` oder `StructuralGraph` |
| SemanticFacet | `side_port` oder `alignment_port` | `SideRegion` oder `AlignmentLine` |
| EnergyFacet | `bridge_side`, falls Hülle | `BridgeZone` |
| LogisticsFacet | `temporary_bracing_port`, falls instabil | `TemporaryBracingZone` |

Typische Beispiele:

```text
SlabBeamColumnFragment-Knoten
Träger-Stützen-Knoten
Stützenkopf
Pilzkopfstütze
```

---

## 7.5 `handling_point`

Ein Punkt für Heben, Lagern, Transportieren, Schützen oder temporäres Abstützen.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| LogisticsFacet | `lifting_port`, `storage_port`, `transport_port`, `protection_port` | `LiftingZone`, `StorageSupportZone`, `TransportEnvelope`, `ProtectionZone` |
| StructuralFacet | `support_side`, falls Handling-Auflager strukturell relevant | `SupportPatch2D` |
| EvidenceModifier | Hebe- oder Schadensnachweis | `EvidenceZone` |

Typische Beispiele:

```text
Hebepunkt
Lagerauflagerpunkt
Transportauflagerpunkt
Schutzpunkt an Schnittkante
temporäre Abstützung
```

---

## 7.6 `visibility_reference_point`

Ein Punkt, der Sichtbarkeit, Lesbarkeit oder Wiederverwendungsausdruck prüfbar macht.

Typische Facets:

| Facet | Port | Host-Geometrie |
|---|---|---|
| SemanticFacet | `visibility_port` | `VisibilitySurface` |
| EvidenceModifier | Oberflächenzustand / Schaden | `DamagePolygon` |

Typische Beispiele:

```text
sichtbare Plattenuntersicht
sichtbare Schnittfläche
sichtbare Bauteilmarkierung
sichtbarer ReUse-Ausdruck
```

Dieser Punkt wird nicht für jede sichtbare Fläche erzeugt, sondern nur wenn Sichtbarkeit tatsächlich Teil der Entwurfsprüfung ist.

---

# 8. Erzeugungslogik für SharedConnectorPoints

## 8.1 Schritt 1 — Kandidaten aus Geometrie erzeugen

Mögliche Kandidaten:

```text
Kantenmittelpunkte
Fugenmittelpunkte
Öffnungszentren
strukturelle Knoten
Transferknoten
Hebekandidaten
Schwerpunktbezug
Schnittflächenmittelpunkte
Stirnflächenmittelpunkte
```

## 8.2 Schritt 2 — Facets zuweisen

Für jeden Kandidaten wird geprüft:

```text
Liegt der Punkt auf einer tragenden Host-Geometrie?
→ StructuralFacet

Liegt der Punkt an einer Hüllengrenze oder Wärmebrückenzone?
→ EnergyFacet

Liegt der Punkt auf einer Route, Öffnung oder Bohrung?
→ TGAFacet

Ist der Punkt relevant für Raster, Fuge, Sichtbarkeit, Zugang oder Raumbezug?
→ SemanticFacet

Ist der Punkt relevant für Heben, Lagern, Transport, Schutz oder Montage?
→ LogisticsFacet
```

## 8.3 Schritt 3 — Punkte zusammenführen

Punkte werden zusammengeführt, wenn:

```text
Distanz < Toleranz
gleiche reale Stelle
Host-Geometrien kompatibel
keine Sicherheitsregel getrennte Punkte verlangt
```

Nicht zusammenführen, wenn:

```text
einer oben und einer unten liegt
einer innen und einer außen liegt
einer sicherheitskritisch getrennt bleiben muss
Hebe- und Auflagerpunkt bewusst unterschiedlich sind
```

## 8.4 Schritt 4 — Inaktive Punkte löschen

Ein Punkt wird gelöscht, wenn:

```text
kein Facet aktiv ist
keine Regel ihn nutzt
keine Warnung ihn nutzt
keine Verbindung ihn nutzt
keine Entwurfsentscheidung ihn nutzt
```

---

# 9. Docking- und Check-Ablauf

## 9.1 User verbindet zwei Punkte

```text
SharedConnectorPoint A
dockt an
SharedConnectorPoint B
```

## 9.2 System findet kompatible Facets

Beispiel:

```text
A.StructuralFacet.port = bearing_side
B.StructuralFacet.port = support_side
→ struktureller Auflagercheck aktiv

A.SemanticFacet.port = alignment_port
B.SemanticFacet.port = alignment_port
→ semantischer Ausrichtungscheck aktiv

A.EnergyFacet.port = bridge_side
B.EnergyFacet.port = thermal_side
→ Wärmebrückenwarnung aktiv
```

## 9.3 System lädt Host-Geometrien

```text
Structural:
SupportPatch2D von A
SupportPatch2D von B

Semantic:
AlignmentLine von A
AlignmentLine von B

Energy:
BridgeZone von A
BoundaryEdge oder ThermalSurface von B
```

## 9.4 System führt Paketchecks aus

```text
Tragwerk:
Auflagerüberlappung, Richtung, Mindestauflager

Energie:
Wärmebrücke, Dämmkontinuität, Abdichtung

TGA:
Leitungsführung, Durchdringung, Konflikt

Semantik:
Raster, Fuge, Sichtbarkeit, Zugang

Logistik:
Montagezugang, Hebbarkeit, Lagerung

Nachweis:
Bewehrung, Schaden, fehlende Evidenz
```

## 9.5 Ergebnis: Connection Passport

```text
Connection Passport
│
├── Point A
├── Point B
│
├── StructuralResult
├── EnergyResult
├── TGAResult
├── SemanticResult
├── LogisticsResult
└── EvidenceResult
```

---

# 10. Beispiel A — Abbau/Aufbau DE_1OG_001

## 10.1 Komponente

```text
DE_1OG_001
Typologie: Deckenplatte
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

## 10.2 Minimale SharedConnectorPoints

Für die Platte reichen wenige strategische Punkte:

```text
1. slab_edge_A_midpoint
2. slab_edge_B_midpoint
3. slab_opening_center, nur wenn Öffnung vorhanden oder Route vorgeschlagen
4. slab_visibility_reference, nur wenn Untersicht sichtbar bleiben soll
5. slab_lifting_reference, falls Heben geprüft wird
6. slab_storage_reference, falls Lagerung geprüft wird
```

## 10.3 Beispielpunkt: `slab_edge_A_midpoint`

| Ebene | Inhalt |
|---|---|
| Punkt | Mittelpunkt der langen Plattenkante A |
| Host-Feature | Plattenkante / Auflagerbereich |
| Strategische Familie | `support_edge_point` |

### Facets

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | Auflagerüberlappung, Richtung, Mindestauflager |
| SemanticFacet | `alignment_port` | `AlignmentLine` | Fugen- und Rasterausrichtung |
| EnergyFacet | `bridge_side`, nur bei Hülle | `BridgeZone` | Wärmebrückenwarnung |
| LogisticsFacet | `access_port`, falls Montage relevant | `AccessVolume` | Montagezugang |

## 10.4 Verbindung zu einer Wand

```text
slab_edge_A_midpoint
dockt an
wall_top_midpoint
```

Aktive Checks:

| Paket | Check |
|---|---|
| Tragwerk | `SupportPatch2D`-Überlappung, Mindestauflager |
| Semantik | Fugen- und Rasterausrichtung |
| Energie | Wärmebrücke, falls Hüllenkontext |
| Logistik | Montagezugang |
| Nachweis | Bewehrung und Schaden beeinflussen StructuralFacet |

---

# 11. Beispiel B — SlabBeamColumnFragment

## 11.1 Komponente

```text
SlabBeamColumnFragment
= monolithisches Betonfragment mit Plattenbereich,
integriertem Trägerbereich und Stützenabschnitt
```

## 11.2 Minimale SharedConnectorPoints

```text
1. fragment_transfer_node
2. fragment_cut_face_point
3. fragment_plate_edge_point
4. fragment_column_base_or_head_point
5. fragment_niche_access_point
6. fragment_lifting_reference
```

## 11.3 Beispielpunkt: `fragment_transfer_node`

| Ebene | Inhalt |
|---|---|
| Punkt | Schnittpunkt von Platten-, Träger- und Stützenregion |
| Host-Feature | struktureller und räumlicher Knoten |
| Strategische Familie | `transfer_node_point` |

### Facets

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `transfer_side` | `StructuralGraph` + `TransferNode` | Lastpfad über Platte, Trägerlinie und Stützenlinie |
| SemanticFacet | `side_port` oder `alignment_port` | `SideRegion` / `AlignmentLine` | räumlicher Schwellen- oder Orientierungscheck |
| EnergyFacet | `bridge_side`, falls Hülle | `BridgeZone` | Wärmebrückenwarnung |
| LogisticsFacet | `temporary_bracing_port`, falls Montage instabil | `TemporaryBracingZone` | temporäre Stabilisierung |
| EvidenceModifier | — | `DamagePolygon`, `ScanLine`, `UnknownZone` | Bewehrung / Schaden / Konfidenz |

## 11.4 Beispielpunkt: `fragment_cut_face_point`

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `continuity_side` | `ContinuityZone` | Kraftschluss, Bewehrung, Verguss |
| SemanticFacet | `visibility_port`, falls sichtbar | `VisibilitySurface` | sichtbare Schnittfläche, Wiederverwendungsausdruck |
| LogisticsFacet | `protection_port` | `ProtectionZone` | Schnittflächenschutz |
| EvidenceModifier | — | `ScanLine`, `DamagePolygon` | Rebar- und Schadensstatus |

Ein Punkt deckt hier Tragwerk, Semantik, Logistik und Nachweis ab.

---

# 12. Beispiel C — ReCreate Hollow-Core Slab

## 12.1 Komponente

```text
wiedergewonnene Hohlkammerdecke
= einachsig spannende Fertigteilplatte mit Längshohlräumen,
Stirnauflagerzonen und Längsfugen
```

## 12.2 Minimale SharedConnectorPoints

```text
1. hcs_end_A_midpoint
2. hcs_end_B_midpoint
3. hcs_long_joint_midpoint
4. hcs_void_route_point, nur wenn Hohlraum als Route genutzt wird
5. hcs_lifting_reference
6. hcs_qr_reference, falls räumliches Tracking relevant ist
```

## 12.3 Beispielpunkt: `hcs_end_A_midpoint`

| Ebene | Inhalt |
|---|---|
| Punkt | Mittelpunkt der Stirnauflagerzone A |
| Host-Feature | Stirnseite / Auflagerbereich |
| Strategische Familie | `support_edge_point` |

### Facets

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `bearing_side` | `SupportPatch2D` | Endauflager |
| LogisticsFacet | `transport_port` oder `storage_port` | `TransportSupportZone` / `StorageSupportZone` | Transport / Lagerung |
| SemanticFacet | `alignment_port`, falls Modul relevant | `AlignmentLine` | Modulausrichtung |
| EnergyFacet | `bridge_side`, falls Dach / Außenboden | `BridgeZone` | Wärmebrückenwarnung |

## 12.4 Beispielpunkt: `hcs_long_joint_midpoint`

| Facet | Port | Host-Geometrie | Check |
|---|---|---|---|
| StructuralFacet | `member_side` | `JointLine` | Längsfugenverbindung, Toleranz |
| SemanticFacet | `alignment_port` | `AlignmentLine` | Fugen- und Modulraster |
| EnergyFacet | `thermal_side`, falls Hüllenfuge | `BoundaryEdge` | thermische Kontinuität |
| LogisticsFacet | `access_port`, falls Fuge montiert wird | `AccessVolume` | Montagezugang |

---

# 13. Connection Passport

## 13.1 Was ist ein Connection Passport?

Ein Connection Passport ist das Ergebnis einer Verbindung zwischen zwei SharedConnectorPoints.

Er speichert nicht nur:

```text
A ist mit B verbunden
```

sondern:

```text
Welche Facets wurden verbunden?
Welche Paketchecks sind aktiv?
Welche Host-Geometrien wurden geprüft?
Welche Warnungen oder Nachweise fehlen?
```

## 13.2 Struktur

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

  results:
    structural:
      status: pass | warning | fail | engineering_required
      checked_host_geometries: []
      messages: []

    energy:
      status: pass | warning | fail | context_required
      checked_host_geometries: []
      messages: []

    tga:
      status: pass | warning | fail | not_applicable
      checked_host_geometries: []
      messages: []

    semantic:
      status: pass | warning | fail | preference_dependent
      checked_host_geometries: []
      messages: []

    logistics:
      status: pass | warning | fail | evidence_required
      checked_host_geometries: []
      messages: []

    evidence:
      missing: []
      blocking: []
      warnings: []
```

---

# 14. Interface-Logik

## 14.1 Anzeige im Bauteilmodus

Im Bauteilpass werden SharedConnectorPoints als wenige strategische Punkte angezeigt.

Jeder Punkt zeigt:

```text
Name
Position
aktive Facets
Ports pro Facet
Host-Geometrien
Status
fehlende Nachweise
mögliche Verbindungen
```

Beispiel:

```text
slab_edge_A_midpoint

Facets:
- Structural: bearing_side
- Semantic: alignment_port
- Energy: bridge_side, context required
- Logistics: access_port

Status:
- Structural: evidence required
- Semantic: ready
- Energy: inactive until envelope
- Logistics: ready
```

## 14.2 Anzeige im Verbindungsmodus

Wenn der User zwei Punkte verbindet, zeigt das Interface nicht nur „verbunden“, sondern:

```text
Structural Check
Energy Check
TGA Check
Semantic Check
Logistics Check
Evidence Status
```

So wird eine Verbindung als mehrschichtiger Entwurfszustand verständlich.

---

# 15. Entscheidungsregeln für minimale Punkte

## 15.1 Punkt erzeugen, wenn

```text
er zwei Bauteile verbinden kann
er eine Berechnung startet
er eine Warnung tragen kann
er eine Ausrichtung / Sichtbarkeit / Zugang prüft
er Handling oder Montage beeinflusst
er durch Nachweise modifiziert wird
```

## 15.2 Punkt nicht erzeugen, wenn

```text
er nur eine geometrische Beschreibung ist
er keine aktive Regel hat
er keine Verbindung herstellen kann
er keine Warnung oder Berechnung auslöst
er nur eine Fläche oder Kante dupliziert
```

## 15.3 Gute Punkte sind multifunktional

Ein SharedConnectorPoint mit mehreren Facets ist besonders wertvoll:

```text
1 Facet  = erlaubt, aber prüfen ob nötig
2 Facets = gut
3+ Facets = sehr guter strategischer Punkt
```

---

# 16. Finale Systemregel

Die neue Systemregel lautet:

```text
Nicht jedes Paket erzeugt eigene Connectoren.
Das Bauteil erzeugt wenige SharedConnectorPoints.
Pakete hängen Facets an diese Punkte.
Verbindungen aktivieren kompatible Facets.
Regeln prüfen die referenzierten Host-Geometrien.
Nachweise modifizieren Facets oder Connection Passports.
```

Dadurch entsteht:

```text
weniger Punktchaos
weniger Dopplung
klarere Benutzeroberfläche
gemeinsame Verbindungslogik
paketübergreifende Checks
skalierbare Bauteilkataloge
```

Die wichtigste Kurzform:

```text
Ein Punkt.
Mehrere Facets.
Eine Verbindung.
Viele Checks.
```
