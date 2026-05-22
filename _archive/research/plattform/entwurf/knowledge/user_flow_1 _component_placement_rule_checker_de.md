# Vollständiger User- und System-Flow  
## Bauteile nacheinander platzieren, verbinden und prüfen

**Ziel**  
Dieses Dokument beschreibt, was passiert, wenn ein User im Playground ein Bauteil nach dem anderen aus dem Bauteilkatalog platziert und verbindet.

**Wichtige Korrektur**  
Die **Generatoren laufen nicht erst beim Platzieren**.  
Sie laufen bereits vorher, beim Import / Aufbau des Bauteilpools.

Beim Platzieren ist der **Bauteilpass bereits vorhanden**:

```text
Bauteilpass
├── Identität
├── Semio-Bindung
├── Klassifikation
├── Geometrie-Repräsentationen
├── Subzonen
├── Ports
├── Öffnungen
├── Auflagerzonen
├── Hüllflächen-Kandidaten
├── Logistikgeometrie
├── Material- und Nachweisstatus
├── LCA-Vorprüfung
├── Pool-Warnungen
└── Rule-Checker-Readiness
```

Der Playground erzeugt daraus **Piece-Instanzen** im aktiven Entwurf.

---

# 1. Grundarchitektur

## 1.1 Vor dem Entwerfen: Bauteilpool ist vorbereitet

```text
Bauteil wird in den Pool importiert
        ↓
Geometrie-Generatoren laufen einmalig oder bei Datenänderung
        ↓
Systemmodule ergänzen nicht-geometrische Daten
        ↓
Bauteilpass wird gespeichert
        ↓
Bauteil erscheint im Bauteilkatalog
```

## 1.2 Während des Entwerfens: User platziert Bauteile

```text
User wählt Bauteil aus Bauteilkatalog
        ↓
System lädt vorhandenen Bauteilpass
        ↓
User platziert Piece im Playground
        ↓
System erstellt Piece-Instanz
        ↓
Rule Checker prüft aktive Situation
        ↓
Design Graph wird aktualisiert
        ↓
UI zeigt Status, Warnungen, Chancen, fehlende Nachweise
```

## 1.3 Generatoren vs. Runtime-Checks

| Ebene | Zeitpunkt | Aufgabe |
|---|---|---|
| **Geometrie-Generatoren** | vor Platzierung | erzeugen Geometrien, Subzonen, Ports, Öffnungen, Flächen, Kanten, Mengen |
| **Systemmodule** | vor Platzierung und bei Kontextänderung | erzeugen Bauteilpassdaten, Nachweisstatus, LCA-Vorprüfung, Pool-Warnungen |
| **Rule Checker** | während Entwurf | prüft Platzierung, Verbindung, Nutzung, Hülle, Logistik, LCA-Kontext |
| **Design Graph** | während Entwurf | speichert platzierte Pieces, Verbindungen, Räume, Abhängigkeiten |
| **Connection Passport** | nach Verbindung | speichert Ergebnis einer konkreten Verbindung |

---

# 2. Zentrale Datenobjekte

## 2.1 Component / Bauteil

Das ist das reale Pool-Objekt.

```yaml
component:
  component_id: AA_MIX_001
  type: mixed_fragment
  material: reinforced_concrete
  stock_total: 1
  bauteilpass: existing
```

## 2.2 Bauteilpass

Der Bauteilpass ist vor dem Platzieren vorhanden.

```yaml
bauteilpass:
  identity:
    component_id: AA_MIX_001
    material: reinforced_concrete
    typology: mixed_fragment

  geometry_representations:
    physical: available
    structural: available
    energy: available
    semantic: available
    connector_zones: available
    logistics: available

  generated_geometry:
    sub_zones:
      - slab_zone
      - beam_zone
      - column_stub_zone
      - internal_transition_zones
    ports:
      - slab-edge-bearing
      - beam-end-bearing
      - column-base-bearing
      - service-penetration-candidate
    openings: []
    bearing_zones: available
    transport_envelope: available

  system_status:
    evidence:
      concrete: missing
      reinforcement: partial_or_missing
      fire: missing
      lifting: missing
      lca: precheck_only
    warnings:
      - mixed_component_requires_subzone_logic
      - no_drilling_without_rebar_scan
      - structural_capacity_unknown
```

## 2.3 Piece

Ein Piece ist eine platzierte Instanz eines Pool-Bauteils.

```yaml
piece:
  piece_id: P001
  source_component_id: AA_MIX_001
  transform:
    position: [0, 0, 0]
    rotation: [0, 0, 90]
    mirrored: false
  active_role: mixed_fragment
  connection_ids: []
```

## 2.4 Connection Passport

Eine Verbindung ist ein eigenes Objekt.

```yaml
connection_passport:
  connection_id: C001
  pieces:
    - P001
    - P002
  ports:
    P001: slab-edge-bearing
    P002: wall-top-bearing
  status: engineering_required
  missing_data:
    - reinforcement_scan
    - connector_capacity
    - structural_proof
```

## 2.5 Design Graph

Der Entwurf ist ein Graph.

```yaml
design_graph:
  nodes:
    pieces:
      - P001
      - P002
    spaces: []
    adapters: []
  edges:
    placements:
      - P001
      - P002
    connections:
      - C001
    supports: []
    adjacency: []
    dependencies: []
```

---

# 3. Statusmodell

```yaml
statuses:
  pass: Regel erfüllt
  warning: möglich, aber Risiko / Qualität / unvollständig
  positive: räumlicher, ökologischer oder zirkulärer Mehrwert
  engineering_required: Fachnachweis erforderlich
  invalid: harte Regelverletzung
  not_applicable: nicht relevant
  blocked_by_missing_data: Prüfung nicht ausführbar
```

---

# 4. Beispiel-Pool für den Flow

```yaml
pool:
  AA_MIX_001:
    type: mixed_fragment
    description: Deckenplatte + Unterzug + Stützenstumpf
    bauteilpass_status: ready
    stock_available: 1

  WALL_001:
    type: wall_panel
    description: wiederverwendete Wandscheibe
    bauteilpass_status: ready
    stock_available: 1

  BEAM_NEW_001:
    type: new_adapter_beam
    description: neuer Hilfs- oder Adapterträger
    bauteilpass_status: ready
    stock_available: 1

  SLAB_TRAP_001:
    type: trapezoid_slab_fragment
    description: unregelmäßiges Deckenfragment
    bauteilpass_status: ready
    stock_available: 1

  COLUMN_001:
    type: reclaimed_column
    description: wiederverwendete Stütze
    bauteilpass_status: ready
    stock_available: 1

  FACADE_001:
    type: facade_or_envelope_fragment
    description: Fassaden- oder Hüllfragment
    bauteilpass_status: ready
    stock_available: 1
```

---

# 5. Phase A — Vor dem User: Pool-Vorbereitung

Diese Phase passiert **vor** dem eigentlichen Playground-Entwurf.

## 5.1 Import eines Bauteils

```yaml
event: import_component
component_id: AA_MIX_001
```

## 5.2 Geometrie-Generatoren laufen

```text
GEO-1 Basisgeometrie normalisieren
GEO-2 physische Geometrie erzeugen
GEO-3 Tragwerksgeometrie erzeugen
GEO-4 Energie- / Hüllgeometrie erzeugen
GEO-5 semantische Geometrie erzeugen
GEO-6 Anschlusszonen + Ports erzeugen
GEO-7 Öffnungen + Durchdringungen erkennen
GEO-8 Logistikgeometrie erzeugen
```

## 5.3 Generator-Ausgaben

```yaml
geometry_outputs:
  physical_geometry: generated
  sub_zone_map:
    - slab_zone
    - beam_zone
    - column_stub_zone
    - internal_transition_zones
  face_map: generated
  edge_map: generated
  opening_map: generated
  port_map: generated
  support_zone_map: generated
  envelope_candidate_faces: generated
  semantic_face_candidates: generated
  transport_envelope: generated
  center_of_gravity: generated
  volume: generated
```

## 5.4 Systemmodule laufen

```text
SYS-1 Semio-Bindung
SYS-2 Identität + Rückverfolgbarkeit
SYS-3 Pool-Verfügbarkeit
SYS-4 Klassifikation
SYS-5 Materialnachweise
SYS-6 Zustand + Schäden
SYS-7 Bewehrungsnachweise
SYS-8 Tragwerksdatenstatus
SYS-9 Anschlussdatenstatus
SYS-10 Brandschutzstatus
SYS-11 Bauphysikstatus
SYS-12 TGA-Status
SYS-13 Logistikstatus
SYS-14 Transportstatus
SYS-15 LCA-Vorprüfung
SYS-16 Dokumentation
SYS-17 Vollständigkeit
SYS-18 Pool-Warnungen
SYS-19 Rule-Checker-Readiness
```

## 5.5 Bauteilpass wird gespeichert

```yaml
bauteilpass_status: ready
rule_checker_readiness:
  geometry_ready: true
  port_ready: true
  stock_check_ready: true
  structural_precheck_ready: true
  drilling_check_ready: false
  reason: reinforcement_missing
```

## 5.6 Wichtig

```text
Ab jetzt werden Generatoren nicht bei jeder Platzierung neu ausgeführt.
Sie werden nur erneut ausgeführt, wenn sich die Basisdaten des Bauteils ändern.
```

---

# 6. Phase B — User öffnet den Playground

## 6.1 User-Aktion

```yaml
action: open_playground
```

## 6.2 System intern

```text
lädt Bauteilkatalog
lädt Bauteilpässe
lädt Rule Library
lädt Projektdefaults
lädt Zielpräferenzen
initialisiert leeren Design Graph
```

## 6.3 Design Graph

```yaml
design_graph:
  nodes:
    pieces: []
    spaces: []
  edges:
    connections: []
```

## 6.4 UI

```text
Links:
Bauteilkatalog

Mitte:
leerer Playground

Rechts:
kein aktives Bauteil

Unten:
Projektstatus leer
```

---

# 7. Schritt 1 — User wählt erstes Bauteil `AA_MIX_001`

## 7.1 User-Aktion

```yaml
action: select_component
component_id: AA_MIX_001
```

## 7.2 System intern

Das System lädt den vorhandenen Bauteilpass.

```yaml
loaded:
  bauteilpass: AA_MIX_001
  geometry_representations: existing
  ports: existing
  evidence_status: existing
  pool_warnings: existing
```

## 7.3 Kein Generator läuft

```yaml
generator_runtime:
  status: not_running
  reason: bauteilpass_already_exists
```

## 7.4 Checker läuft als Auswahlprüfung

```yaml
rules_run:
  - identity_unique
  - component_stock_available
  - evidence_completeness
  - geometry_readable
  - typology_classified
  - mixed_component_subzones
```

## 7.5 Ergebnis

```yaml
selection_result:
  identity_unique: pass
  component_stock_available: pass
  evidence_completeness: engineering_required
  geometry_readable: pass
  typology_classified: pass
  mixed_component_subzones: pass
  overall: selectable_with_warnings
```

## 7.6 UI

```text
Bauteil kann ausgewählt werden.

Badge:
"Bauteilpass bereit"

Warnungen:
- Tragwerksnachweis fehlt
- Bewehrung unvollständig
- Bohrungen nicht freigegeben
- Mischbauteil: Subzonenlogik aktiv
```

---

# 8. Schritt 2 — User zieht `AA_MIX_001` in den Playground

## 8.1 User-Aktion

```yaml
action: drag_component_to_scene
component_id: AA_MIX_001
preview_position: [0, 0, 0]
```

## 8.2 System intern

Das System erstellt eine temporäre Preview-Instanz.

```yaml
preview_piece:
  temp_id: PREVIEW_001
  source_component_id: AA_MIX_001
  transform: temporary
  committed: false
```

## 8.3 Was mit vorhandener Geometrie passiert

Die vorhandenen Geometrien werden nur transformiert:

```text
physical_geometry × preview_transform
sub_zone_map × preview_transform
port_map × preview_transform
support_zone_map × preview_transform
transport_envelope × preview_transform
```

## 8.4 Checker läuft live

```yaml
rules_run_live:
  - collision_check
  - orientation_side_logic
  - placement_boundary_check
  - temporary_state_stability
```

## 8.5 Ergebnis

```yaml
preview_result:
  collision_check: pass
  orientation_side_logic: warning
  placement_boundary_check: pass
  temporary_state_stability: engineering_required
  overall: placeable_with_warnings
```

## 8.6 UI

```text
Bauteil erscheint halbtransparent.

Outline:
gelb / orange

Meldung:
"Platzierbar. Temporäre Stabilität und spätere Lagerung / Hebung benötigen Nachweis."
```

---

# 9. Schritt 3 — User rotiert das Bauteil

## 9.1 User-Aktion

```yaml
action: rotate_preview
piece: PREVIEW_001
rotation_z: 90deg
```

## 9.2 System intern

Wieder keine Generatoren.  
Nur Transformation der vorhandenen Repräsentationen.

```yaml
transformed_geometry:
  ports: transformed
  sub_zones: transformed
  support_zones: transformed
  semantic_faces: transformed
```

## 9.3 Checker läuft

```yaml
rules_run:
  - orientation_side_logic
  - port_direction_validity
  - support_zone_orientation
  - semantic_side_warning
```

## 9.4 Ergebnis

```yaml
result:
  orientation_side_logic: warning
  port_direction_validity: pass
  support_zone_orientation: warning
  semantic_side_warning: warning
  overall: rotation_allowed_with_warnings
```

## 9.5 UI

```text
Rotation erlaubt.

Hinweis:
"Rotation verändert Port-Ausrichtung, mögliche Spannrichtung und semantische Seiten.
Statischer Nachweis bleibt erforderlich."
```

---

# 10. Schritt 4 — User platziert `AA_MIX_001`

## 10.1 User-Aktion

```yaml
action: commit_placement
component_id: AA_MIX_001
position: [0, 0, 0]
rotation: [0, 0, 90]
```

## 10.2 System intern

Die Preview wird eine echte Piece-Instanz.

```yaml
piece:
  piece_id: P001
  source_component_id: AA_MIX_001
  transform:
    position: [0, 0, 0]
    rotation: [0, 0, 90]
  active_role: mixed_fragment
```

## 10.3 Design Graph Update

```yaml
design_graph.nodes.pieces:
  - P001

design_graph.edges.placements:
  - piece: P001
    component: AA_MIX_001
```

## 10.4 Pool Update

```yaml
AA_MIX_001.stock:
  stock_total: 1
  used_count: 1
  stock_available: 0
```

## 10.5 Checker läuft

```yaml
rules_run:
  - inventory_unique_use
  - placement_collision_check
  - mixed_component_subzones
  - temporary_state_stability
  - lifting_assembly
  - storage_strategy
  - lca_precheck
```

## 10.6 Ergebnis

```yaml
placement_result:
  inventory_unique_use: pass
  placement_collision_check: pass
  mixed_component_subzones: pass
  temporary_state_stability: engineering_required
  lifting_assembly: engineering_required
  storage_strategy: engineering_required
  lca_precheck: positive_and_warning
  overall: placed_with_engineering_warnings
```

## 10.7 UI

```text
Bauteil ist platziert.

Status:
"Platziert, nicht technisch freigegeben"

Warnungen:
- Hebepunkte fehlen
- temporäre Stabilität nicht nachgewiesen
- Mischbauteil benötigt Subzonenlogik
- LCA nur Vorprüfung

Positive Info:
- Wiederverwendete Masse erzeugt potenzielles CO₂-Einsparpotenzial
```

---

# 11. Schritt 5 — User versucht, `AA_MIX_001` als einfache Platte zu nutzen

## 11.1 User-Aktion

```yaml
action: assign_role
piece_id: P001
requested_role: simple_slab
```

## 11.2 System intern

```yaml
requested_role: simple_slab
actual_typology: mixed_fragment
existing_sub_zones:
  - slab_zone
  - beam_zone
  - column_stub_zone
```

## 11.3 Checker läuft

```yaml
rules_run:
  - typology_role_compatibility
  - mixed_component_subzones
  - load_path_continuity
```

## 11.4 Ergebnis

```yaml
role_assignment_result:
  typology_role_compatibility: invalid
  mixed_component_subzones: invalid
  load_path_continuity: engineering_required
  overall: invalid
```

## 11.5 UI

```text
Rote Meldung:
"Dieses Bauteil darf nicht als einfache Platte behandelt werden."

Grund:
"Es enthält Unterzug- und Stützenzonen. Bitte als Mischfragment oder nachgewiesenes Kompositbauteil nutzen."
```

## 11.6 Systemaktion

```yaml
requested_role_rejected: true
piece_role_remains: mixed_fragment
```

---

# 12. Schritt 6 — User platziert `WALL_001`

## 12.1 User-Aktion

```yaml
action: place_component
component_id: WALL_001
near_piece: P001
```

## 12.2 System intern

Bauteilpass von `WALL_001` existiert bereits.

```yaml
loaded_bauteilpass:
  component_id: WALL_001
  type: wall_panel
  ports:
    - wall-bottom-bearing
    - wall-top-bearing
    - wall-side-joint
```

## 12.3 Neue Piece-Instanz

```yaml
piece:
  piece_id: P002
  source_component_id: WALL_001
  active_role: wall_panel
```

## 12.4 Design Graph Update

```yaml
design_graph.nodes.pieces:
  - P001
  - P002
```

## 12.5 Live-Snap-Erkennung

Das System erkennt potenziell kompatible Ports.

```yaml
snap_candidates:
  - piece_A: P001
    port_A: slab-edge-bearing
    piece_B: P002
    port_B: wall-top-bearing
    relation: possible_bearing_connection
```

## 12.6 Checker läuft live

```yaml
rules_run_live:
  - port_compatibility
  - bearing_overlap
  - collision_check
  - tolerance_fit
```

## 12.7 Ergebnis

```yaml
snap_result:
  port_compatibility: pass
  bearing_overlap: warning
  collision_check: pass
  tolerance_fit: warning
  overall: snap_possible_with_warning
```

## 12.8 UI

```text
Snap-Vorschlag erscheint.

Gelbe Verbindungslinie:
"Geometrisch kompatibel, aber Nachweise fehlen."
```

---

# 13. Schritt 7 — User bestätigt Verbindung P001 ↔ P002

## 13.1 User-Aktion

```yaml
action: connect_components
piece_A: P001
port_A: slab-edge-bearing
piece_B: P002
port_B: wall-top-bearing
```

## 13.2 System intern

Connection Passport wird erzeugt.

```yaml
connection:
  connection_id: C001
  pieces:
    - P001
    - P002
  ports:
    P001: slab-edge-bearing
    P002: wall-top-bearing
  connector_family: candidate_wall_slab_connection
```

## 13.3 Design Graph Update

```yaml
design_graph.edges.connections:
  - C001

design_graph.edges.supports:
  - supporter: P002
    supported: P001
    status: engineering_required
```

## 13.4 Checker läuft

```yaml
rules_run:
  - port_compatibility
  - bearing_overlap
  - load_path_continuity
  - connector_family_match
  - post_installed_rebar_connection
  - intrusive_action_gate
  - no_drill_zone_enforcement
  - connector_fire_exposure
  - lca_precheck
```

## 13.5 Ergebnis

```yaml
connection_result_C001:
  port_compatibility: pass
  bearing_overlap: engineering_required
  load_path_continuity: engineering_required
  connector_family_match: engineering_required
  post_installed_rebar_connection: engineering_required
  intrusive_action_gate: invalid_without_rebar_scan
  no_drill_zone_enforcement: engineering_required
  connector_fire_exposure: engineering_required_if_fire_relevant
  lca_precheck: warning
  overall: engineering_required
```

## 13.6 UI

```text
Verbindung wird gespeichert, aber nicht freigegeben.

Status:
engineering_required

Rote Teilmeldung:
"Bohrung / Anker nicht erlaubt ohne Bewehrungsscan."

Orange Meldung:
"Anschlussdetail und Tragwerksnachweis erforderlich."
```

## 13.7 Connection Passport

```yaml
connection_passport_C001:
  status: engineering_required
  ready:
    - geometry
    - ports
    - basic_bearing_precheck
  missing:
    - reinforcement_scan
    - connector_capacity
    - bearing_length_proof
    - structural_calculation
    - fire_detail_if_relevant
```

---

# 14. Schritt 8 — User fügt neuen Adapterträger `BEAM_NEW_001` hinzu

## 14.1 User-Aktion

```yaml
action: place_component
component_id: BEAM_NEW_001
role: support_adapter
under_piece: P001
```

## 14.2 System intern

Der Adapterträger hat ebenfalls einen Bauteilpass.

```yaml
BEAM_NEW_001:
  type: new_adapter_beam
  engineered: true
  ports:
    - beam-top-bearing
    - beam-end-bearing
```

## 14.3 Neue Piece-Instanz

```yaml
piece:
  piece_id: P003
  source_component_id: BEAM_NEW_001
  active_role: support_adapter
```

## 14.4 Design Graph Update

```yaml
design_graph.nodes.pieces:
  - P001
  - P002
  - P003
```

## 14.5 System erkennt Adapterlogik

```yaml
adapter_detection:
  adapter_piece: P003
  supported_piece_candidate: P001
  adapter_role: new_support_component
```

## 14.6 Checker läuft

```yaml
rules_run:
  - new_adapter_or_support_component
  - port_compatibility
  - bearing_overlap
  - load_path_continuity
  - connector_family_match
  - tolerance_fit
  - future_reuse_reversibility
  - lca_precheck
```

## 14.7 Ergebnis

```yaml
adapter_result:
  new_adapter_or_support_component: pass
  port_compatibility: pass
  bearing_overlap: warning
  load_path_continuity: engineering_required
  connector_family_match: engineering_required
  tolerance_fit: warning
  future_reuse_reversibility: warning
  lca_precheck: warning
  overall: improves_geometry_but_requires_engineering
```

## 14.8 UI

```text
Positive Info:
"Adapterträger verbessert geometrische Auflagerlogik."

Warnungen:
- Anschluss P001 ↔ P003 benötigt Tragwerksnachweis
- Adaptermaterial muss in LCA ergänzt werden
- Reversibilität hängt vom Anschlussdetail ab
```

---

# 15. Schritt 9 — User verbindet `AA_MIX_001` mit Adapterträger

## 15.1 User-Aktion

```yaml
action: connect_components
piece_A: P001
port_A: beam-end-bearing_or_slab-bearing-zone
piece_B: P003
port_B: beam-top-bearing
```

## 15.2 System intern

Neue Verbindung:

```yaml
connection:
  connection_id: C002
  pieces:
    - P001
    - P003
  role: reclaimed_piece_on_new_support
```

## 15.3 Checker läuft

```yaml
rules_run:
  - port_compatibility
  - bearing_overlap
  - new_adapter_or_support_component
  - load_path_continuity
  - connector_family_match
  - grout_gap_and_tolerance
  - connector_fire_exposure
  - lca_precheck
```

## 15.4 Ergebnis

```yaml
connection_result_C002:
  port_compatibility: pass
  bearing_overlap: warning
  new_adapter_or_support_component: pass
  load_path_continuity: engineering_required
  connector_family_match: engineering_required
  grout_gap_and_tolerance: warning
  connector_fire_exposure: engineering_required_if_fire_relevant
  lca_precheck: warning
  overall: engineering_required_but_preferred_over_unsupported_condition
```

## 15.5 UI

```text
Verbindung C002 wird orange dargestellt.

Meldung:
"Neuer Träger als Adapter ist zulässig und sinnvoll, aber Anschlussnachweis erforderlich."

Design Dashboard:
"Lastpfad verbessert, Nachweisstatus weiterhin offen."
```

---

# 16. Schritt 10 — User platziert `SLAB_TRAP_001`

## 16.1 User-Aktion

```yaml
action: place_component
component_id: SLAB_TRAP_001
near_piece: P001
```

## 16.2 System intern

Bauteilpass existiert bereits.

```yaml
SLAB_TRAP_001:
  type: trapezoid_slab_fragment
  geometry:
    polygon_footprint: trapezoid
    non_orthogonal_edges: true
    ports:
      - slab-edge-bearing
      - slab-side-joint
```

## 16.3 Neue Piece-Instanz

```yaml
piece:
  piece_id: P004
  source_component_id: SLAB_TRAP_001
```

## 16.4 Checker läuft

```yaml
rules_run:
  - inventory_unique_use
  - geometry_readable
  - typology_classified
  - irregular_edge_usability
  - collision_check
  - tolerance_fit
```

## 16.5 Ergebnis

```yaml
placement_result_P004:
  inventory_unique_use: pass
  geometry_readable: pass
  typology_classified: pass
  irregular_edge_usability: warning_or_positive
  collision_check: pass
  tolerance_fit: warning
  overall: placed_with_spatial_quality_warning
```

## 16.6 UI

```text
Bauteil wird platziert.

Hinweis:
"Trapezform kann unpraktische Restflächen erzeugen, aber auch räumliche Qualität."
```

---

# 17. Schritt 11 — User schiebt `SLAB_TRAP_001` an `AA_MIX_001`

## 17.1 User-Aktion

```yaml
action: move_piece_near_piece
piece: P004
target_piece: P001
```

## 17.2 System intern

System erkennt mögliche Kantenverbindung.

```yaml
candidate_connection:
  P004.port: slab-side-joint
  P001.port: slab-edge-bearing_or_slab-side-edge
```

## 17.3 Checker läuft live

```yaml
rules_run_live:
  - port_compatibility
  - edge_alignment
  - tolerance_fit
  - awkward_corner_detection
  - void_or_gap_detection
```

## 17.4 Ergebnis

```yaml
live_result:
  port_compatibility: warning
  edge_alignment: warning
  tolerance_fit: warning
  awkward_corner_detection: warning_or_positive
  void_or_gap_detection: warning
  overall: connectable_but_gap_or_angle_needs_decision
```

## 17.5 UI

```text
System zeigt:
- mögliche Fuge
- mögliche Restlücke
- Winkelwarnung
- Option: "als Patio / Fuge / Restvoid klassifizieren"
```

---

# 18. Schritt 12 — User lässt eine Lücke als Patio / Hof

## 18.1 User-Aktion

```yaml
action: classify_void
void_id: V001
classification: patio
```

## 18.2 System intern

Der Design Graph erhält einen Space Node.

```yaml
space:
  space_id: V001
  type: patio
  adjacent_pieces:
    - P001
    - P004
```

## 18.3 Checker läuft

```yaml
rules_run:
  - void_patio_courtyard
  - patio_light_air_access
  - patio_edge_support
  - moisture_weathering
  - drainage_strategy
```

## 18.4 Ergebnis

```yaml
patio_result:
  void_patio_courtyard: positive
  patio_light_air_access: warning
  patio_edge_support: engineering_required
  moisture_weathering: warning
  drainage_strategy: warning
  overall: positive_with_required_detailing
```

## 18.5 UI

```text
Patio wird blau markiert:
positive räumliche Qualität

Warnungen:
- Mindestbreite / Licht / Luft prüfen
- Entwässerung fehlt
- Patio-Kanten brauchen Auflager- und Abdichtungsdetail
```

---

# 19. Schritt 13 — User platziert `COLUMN_001`

## 19.1 User-Aktion

```yaml
action: place_component
component_id: COLUMN_001
inside_space: ROOM_001
```

## 19.2 System intern

```yaml
piece:
  piece_id: P005
  source_component_id: COLUMN_001
  type: reclaimed_column
```

## 19.3 Checker läuft

```yaml
rules_run:
  - inventory_unique_use
  - placement_collision_check
  - load_path_continuity
  - temporary_state_stability
  - usable_area
  - obstacle_quality
```

## 19.4 Ergebnis

```yaml
placement_result_P005:
  inventory_unique_use: pass
  placement_collision_check: pass
  load_path_continuity: engineering_required
  temporary_state_stability: engineering_required
  usable_area: warning
  obstacle_quality: context_dependent
  overall: placed_with_structural_and_spatial_checks
```

## 19.5 UI

```text
Stütze platziert.

Warnung:
"Tragende Rolle nicht nachgewiesen."

Raumhinweis:
"Stütze reduziert nutzbare Fläche. Kann als räumliche Qualität markiert werden."
```

---

# 20. Schritt 14 — Stütze steht vor Fenster

## 20.1 User-Aktion

```yaml
action: move_column
piece: P005
near_window: W001
```

## 20.2 System intern

Das System erkennt eine Beziehung zwischen Stütze und Fenster.

```yaml
spatial_relation:
  type: column_near_window
  piece: P005
  window: W001
```

## 20.3 Checker läuft

```yaml
rules_run:
  - daylight_view
  - column_near_window
  - circulation_accessibility
  - target_preference_alignment
```

## 20.4 Ergebnis ohne Präferenz

```yaml
result_without_preference:
  daylight_view: warning
  column_near_window: warning
  circulation_accessibility: pass
  target_preference_alignment: neutral
  overall: warning
```

## 20.5 Ergebnis mit Präferenz „sichtbare Wiederverwendung“

```yaml
result_with_visible_reuse_preference:
  daylight_view: warning
  column_near_window: positive
  target_preference_alignment: positive
  overall: positive_with_daylight_warning
```

## 20.6 UI

```text
System zeigt nicht nur Fehler.

Meldung:
"Stütze reduziert Sicht / Tageslicht, kann aber als sichtbare Wiederverwendungsqualität akzeptiert werden."

Option:
- als Problem markieren
- als räumliches Motiv akzeptieren
```

---

# 21. Schritt 15 — User erzeugt Nische hinter Stütze

## 21.1 User-Aktion

```yaml
action: adjust_room_wall
effect: niche_behind_column
piece: P005
```

## 21.2 System intern

```yaml
spatial_condition:
  type: niche_behind_obstacle
  obstacle: P005
  niche_geometry: generated_from_room_update
```

## 21.3 Checker läuft

```yaml
rules_run:
  - niche_behind_obstacle
  - usable_area
  - program_fit
```

## 21.4 Ergebnis

```yaml
niche_result:
  niche_behind_obstacle: positive_or_warning
  usable_area: warning_if_too_small
  program_fit: depends_on_target_use
```

## 21.5 UI

```text
Wenn Nische nutzbar:
blau / positive

"Kann als Regal, Sitznische, Stauraum oder räumliche Schwelle genutzt werden."

Wenn nicht nutzbar:
gelb / warning

"Restfläche zu klein oder schlecht zugänglich."
```

---

# 22. Schritt 16 — User weist Raumfunktion zu

## 22.1 User-Aktion

```yaml
action: assign_program
space_id: ROOM_001
program: bathroom
```

## 22.2 System intern

System prüft Hindernisse, Bewegungsflächen und Fixtures.

```yaml
room_context:
  program: bathroom
  obstacles:
    - P005
    - beam_downstand_from_P001
  required_clearances:
    - fixture_clearance
    - door_swing
    - accessibility_optional
```

## 22.3 Checker läuft

```yaml
rules_run:
  - program_fit
  - usable_area
  - oversized_obstacle_in_small_room
  - circulation_accessibility
```

## 22.4 Ergebnis

```yaml
bathroom_result:
  program_fit: warning_or_invalid
  usable_area: warning
  oversized_obstacle_in_small_room: warning_or_invalid
  circulation_accessibility: pass_or_invalid
  overall: depends_on_clearance
```

## 22.5 UI

```text
Bei ausreichender Bewegungsfläche:
"Bad möglich, aber Stütze reduziert Nutzbarkeit."

Bei zu geringer Bewegungsfläche:
"Ungültig: erforderliche Sanitärobjekt- oder Bewegungsflächen nicht erfüllt."
```

---

# 23. Schritt 17 — User platziert Fassadenelement `FACADE_001`

## 23.1 User-Aktion

```yaml
action: place_component
component_id: FACADE_001
context: exterior_facade
```

## 23.2 System intern

```yaml
piece:
  piece_id: P006
  source_component_id: FACADE_001
  active_context: envelope
```

## 23.3 Checker läuft

```yaml
rules_run:
  - envelope_relevance
  - thermal_bridge_risk
  - moisture_weathering
  - fire_safety
  - acoustic_performance
  - provenance_traceability
```

## 23.4 Ergebnis

```yaml
facade_result:
  envelope_relevance: engineering_required
  thermal_bridge_risk: warning
  moisture_weathering: warning
  fire_safety: engineering_required
  acoustic_performance: warning
  provenance_traceability: warning
  overall: envelope_context_requires_proofs
```

## 23.5 UI

```text
Fassadenelement wird platziert.

Orange:
"Hüllkontext erfordert energetische, feuchte- und brandschutztechnische Nachweise."

Gelb:
"Wärmebrücken- und Witterungsdetails fehlen."
```

---

# 24. Schritt 18 — User verbindet Fassade mit Tragstruktur

## 24.1 User-Aktion

```yaml
action: connect_components
piece_A: P006
port_A: facade-back-connector
piece_B: P001
port_B: slab-edge-or-beam-side
```

## 24.2 System intern

Neue Verbindung:

```yaml
connection:
  connection_id: C003
  role: facade_to_structure
```

## 24.3 Checker läuft

```yaml
rules_run:
  - port_compatibility
  - connector_family_match
  - thermal_bridge_risk
  - moisture_weathering
  - connector_fire_exposure
  - tolerance_fit
  - future_reuse_reversibility
```

## 24.4 Ergebnis

```yaml
facade_connection_result:
  port_compatibility: warning
  connector_family_match: engineering_required
  thermal_bridge_risk: warning
  moisture_weathering: warning
  connector_fire_exposure: engineering_required
  tolerance_fit: warning
  future_reuse_reversibility: warning
  overall: engineering_required
```

## 24.5 UI

```text
Verbindung gespeichert, nicht freigegeben.

Meldungen:
- Anschlussdetail fehlt
- Wärmebrückenrisiko
- Feuchtedetail fehlt
- Brandschutzkontext fehlt
- Reversibilität abhängig vom Anschluss
```

---

# 25. Schritt 19 — User startet Gesamtcheck

## 25.1 User-Aktion

```yaml
action: run_global_check
```

## 25.2 System intern

Der Rule Checker prüft den gesamten Design Graph.

```yaml
global_rules:
  - inventory_unique_use
  - connection_graph_completeness
  - load_path_continuity
  - unresolved_engineering_required
  - invalid_actions
  - envelope_open_issues
  - room_quality_summary
  - logistics_summary
  - lca_precheck_summary
```

## 25.3 Ergebnis

```yaml
global_check:
  placed_pieces: 6
  connections: 3
  invalid_issues:
    - no_drilling_allowed_without_rebar_scan
    - P001_cannot_be_simple_slab
  engineering_required:
    - C001_wall_slab_connection
    - C002_adapter_support_connection
    - C003_facade_connection
    - lifting_for_P001
    - fire_for_facade_and_connectors
    - structural_capacity_for_reclaimed_components
  warnings:
    - patio_drainage_missing
    - thermal_bridge_risk
    - room_usability_reduced_by_column
    - LCA_connector_impacts_missing
  positives:
    - reused_mass_potential
    - visible_reuse_expression
    - patio_spatial_quality
    - niche_spatial_quality_if_accepted
```

## 25.4 UI

```text
Dashboard zeigt:

Rot:
2 invalid issues

Orange:
mehrere engineering_required Themen

Gelb:
Raum-, Hülle-, Logistik- und LCA-Warnungen

Blau:
räumliche und zirkuläre Qualitäten
```

---

# 26. Schritt 20 — User klickt auf ein Problem

## 26.1 User-Aktion

```yaml
action: click_rule_issue
issue: no_drilling_allowed_without_rebar_scan
```

## 26.2 System intern

System öffnet betroffene Zone.

```yaml
affected:
  piece: P001
  component: AA_MIX_001
  zone: beam_column_transition
  rule: intrusive_action_gate
```

## 26.3 UI

```text
3D-Ansicht zoomt auf die Übergangszone.

Panel zeigt:
- Regel
- Grund
- fehlende Daten
- mögliche nächste Schritte
```

## 26.4 Rule Result

```yaml
rule_result:
  rule_id: intrusive_action_gate
  category: Verbindung + Tragwerk
  status: invalid
  affected_piece_ids:
    - P001
  affected_zones:
    - beam_column_transition
  message: Nicht in diese Übergangszone bohren.
  reason: Bewehrungslage unbekannt und Zone tragwerksrelevant.
  required_next_data:
    - vollständiger Bewehrungsscan
    - Anschlussnachweis
  suggested_actions:
    - alternative Anschlusszone wählen
    - Adapterträger nutzen
    - trockene reversible Verbindung prüfen
  severity: critical
```

---

# 27. Schritt 21 — User akzeptiert eine positive räumliche Qualität

## 27.1 User-Aktion

```yaml
action: accept_spatial_quality
condition: column_near_window
preference: visible_reuse
```

## 27.2 System intern

Zielpräferenz wird im Design Context gespeichert.

```yaml
target_preferences:
  visible_reuse: high
  spatial_complexity: accepted
```

## 27.3 Checker re-evaluiert

```yaml
rules_recomputed:
  - target_preference_alignment
  - daylight_view
  - obstacle_quality
```

## 27.4 Ergebnis

```yaml
updated_result:
  column_near_window:
    status: positive_with_warning
    positive: visible_reuse_expression
    warning: daylight_reduction
```

## 27.5 UI

```text
Die Stütze-vor-Fenster-Situation wird nicht mehr nur als Problem angezeigt.

Neuer Status:
"Akzeptierte räumliche Qualität mit Tageslichtwarnung."
```

---

# 28. Schritt 22 — User startet LCA-Vorprüfung

## 28.1 User-Aktion

```yaml
action: run_lca_precheck
```

## 28.2 System intern

System summiert:

```text
wiederverwendete Masse
neue Adaptermasse
Transportdistanzen
Transportfaktoren
Referenz-Neubauteile
fehlende Connector- und Reparaturwirkungen
```

## 28.3 Checker läuft

```yaml
rules_run:
  - lca_precheck
  - connector_adapter_impact_missing
  - transport_feasibility
  - future_reuse_reversibility
```

## 28.4 Ergebnis

```yaml
lca_result:
  status: positive_and_warning
  positive:
    - reused_mass_has_avoided_material_potential
  warnings:
    - adapter_impacts_missing
    - connector_impacts_missing
    - repair_impacts_missing
    - full_dataset_missing
```

## 28.5 UI

```text
LCA-Panel:

Blau:
"Wiederverwendungspotenzial vorhanden."

Gelb:
"Nur Vorprüfung. Neue Adapter, Verbinder, Reparaturen und Datensätze fehlen."
```

---

# 29. Schritt 23 — User exportiert Entwurf

## 29.1 User-Aktion

```yaml
action: export_design
```

## 29.2 System intern

Exportpaket wird erzeugt:

```yaml
export:
  design_graph: included
  piece_instances: included
  connection_passports: included
  rule_results: included
  unresolved_issues: included
  bauteilpass_references: included
  lca_precheck: included
  evidence_requirements: included
```

## 29.3 Checker finalisiert Exportstatus

```yaml
export_status:
  allowed: true
  approval_ready: false
  reason:
    - engineering_required_items_open
    - invalid_drilling_action_blocked
    - full_lca_missing
```

## 29.4 UI

```text
Export erlaubt als:
"Entwurfsstand / Vorprüfung"

Nicht erlaubt als:
"Ausführungsfreigabe / Genehmigungsnachweis"
```

---

# 30. Gesamtlogik als Sequenzdiagramm

```text
User
 │
 │ wählt Bauteil
 ▼
Bauteilkatalog
 │
 │ lädt vorhandenen Bauteilpass
 ▼
Playground
 │
 │ erzeugt Preview Piece
 ▼
Rule Checker
 │
 │ live checks: Kollision, Orientierung, Platzierbarkeit
 ▼
User
 │
 │ platziert Bauteil
 ▼
Design Graph
 │
 │ erstellt Piece Instance
 │ aktualisiert Stock
 ▼
Rule Checker
 │
 │ placement checks
 ▼
User
 │
 │ verbindet Bauteil A + B
 ▼
Connection Passport
 │
 │ speichert Ports, Zonen, Connector-Kandidat
 ▼
Rule Checker
 │
 │ connection checks
 ▼
Dashboard
 │
 │ zeigt pass / warning / positive / engineering_required / invalid
```

---

# 31. Was das System bei jedem neuen Bauteil macht

Für jedes neu platzierte Bauteil läuft immer:

```yaml
on_new_piece_placed:
  read_existing_bauteilpass: true
  run_generators: false
  create_piece_instance: true
  transform_existing_geometry: true
  update_design_graph: true
  update_inventory: true
  run_checker:
    - inventory_unique_use
    - collision_check
    - orientation_side_logic
    - typology_role_compatibility
    - temporary_state_stability
    - logistics_warning
    - lca_precheck_update
```

---

# 32. Was das System bei jeder neuen Verbindung macht

```yaml
on_new_connection:
  read_existing_ports: true
  run_generators: false
  create_connection_passport: true
  update_design_graph_edges: true
  run_checker:
    - port_compatibility
    - bearing_overlap
    - load_path_continuity
    - connector_family_match
    - intrusive_action_gate
    - no_drill_zone_enforcement
    - fire_safety
    - thermal_bridge_risk
    - tolerance_fit
    - lca_connector_impact
```

---

# 33. Was das System bei jedem neuen Raumkontext macht

```yaml
on_space_or_program_update:
  run_generators: false
  update_space_graph: true
  run_checker:
    - program_fit
    - usable_area
    - obstacle_quality
    - daylight_view
    - circulation_accessibility
    - void_patio_courtyard
    - target_preference_alignment
```

---

# 34. Was das System bei jedem neuen Hüllkontext macht

```yaml
on_envelope_context_update:
  run_generators: false
  use_existing_envelope_candidate_faces: true
  run_checker:
    - envelope_relevance
    - thermal_bridge_risk
    - moisture_weathering
    - fire_safety
    - acoustic_performance
    - durability_service_life
```

---

# 35. Was das System bei jedem neuen Logistik- oder LCA-Check macht

```yaml
on_logistics_or_lca_update:
  run_generators: false
  use_existing_transport_envelope: true
  use_existing_mass_and_volume: true
  run_checker:
    - storage_strategy
    - lifting_assembly
    - transport_feasibility
    - assembly_sequence
    - lca_precheck
    - future_reuse_reversibility
    - effort_cost_sensitivity
```

---

# 36. Wichtigste UI-Panels

## 36.1 Bauteilkatalog

```text
zeigt:
- verfügbare Bauteile
- Typologie
- Material
- Thumbnail
- Quick Status
- Warnungen
- Bauteilpass-Link
```

## 36.2 Bauteilpass-Panel

```text
zeigt:
- Daten eines Pool-Bauteils
- keine aktive Verbindung
- keine aktuellen Raum- oder Gebäude-Scores
```

## 36.3 Piece-Panel

```text
zeigt:
- platzierte Instanz
- Position
- Rotation
- aktive Rolle
- transformierte Ports
- aktive Warnungen
```

## 36.4 Connection-Panel

```text
zeigt:
- Verbindung zwischen Pieces
- Ports
- Anschlussfamilie
- Status
- fehlende Nachweise
```

## 36.5 Rule-Checker-Panel

```text
zeigt:
- aktive Regelresultate
- pass / warning / positive / engineering_required / invalid
- betroffene Zonen
- nächste erforderliche Daten
```

## 36.6 Design-Dashboard

```text
zeigt:
- globale Risiken
- offene Engineering-Themen
- LCA-Vorprüfung
- Logistikstatus
- Raumqualitäten
- Zielpräferenz-Abgleich
```

---

# 37. Beispielhafter Endzustand

Nach allen Schritten:

```yaml
design_graph:
  pieces:
    P001: AA_MIX_001
    P002: WALL_001
    P003: BEAM_NEW_001
    P004: SLAB_TRAP_001
    P005: COLUMN_001
    P006: FACADE_001

  connections:
    C001:
      from: P001
      to: P002
      status: engineering_required
    C002:
      from: P001
      to: P003
      status: engineering_required
    C003:
      from: P006
      to: P001
      status: engineering_required

  spaces:
    V001:
      type: patio
      status: positive_with_warnings
    ROOM_001:
      type: bathroom_or_room
      status: context_dependent
```

## Globaler Status

```yaml
global_status:
  usable_as_design_study: true
  approval_ready: false
  construction_ready: false

  invalid:
    - drilling_without_rebar_scan
    - treating_mixed_fragment_as_simple_slab

  engineering_required:
    - structural_capacity
    - connector_details
    - fire_proof
    - lifting_plan
    - envelope_detail
    - full_lca

  warnings:
    - thermal_bridge_risk
    - patio_drainage_missing
    - room_usability_reduced
    - lca_adapter_impacts_missing

  positives:
    - reused_material_potential
    - visible_reuse_quality
    - patio_quality
    - niche_quality
```

---

# 38. Kernaussage

```text
Beim Platzieren wird nichts neu generiert.
Der Bauteilpass existiert bereits.

Der Playground macht:
- Instanzen erzeugen
- vorhandene Geometrien transformieren
- Graph aktualisieren
- Verbindungen speichern
- aktive Regelprüfungen ausführen
```

Der Rule Checker ist dadurch schnell und nachvollziehbar:

```text
Bauteilpass sagt:
Was ist dieses Bauteil?

Piece sagt:
Wo und wie wird es benutzt?

Connection Passport sagt:
Wie ist es verbunden?

Rule Checker sagt:
Was passt, was ist riskant, was braucht Nachweise, was ist ungültig?

Dashboard sagt:
Was bedeutet das für den gesamten Entwurf?
```
