# Allgemeiner Rule-Checker-Katalog  
## Anwendbar auf das detaillierte Abbau/Aufbau-Beispiel `AA_MIX_001`

**Ziel dieses Dokuments**  
Die Regeln bleiben **allgemein und projektübertragbar**, werden aber direkt auf das detaillierte Beispiel `AA_MIX_001` angewendet.

**Beispielkontext**  
`AA_MIX_001` ist ein hypothetisches Abbau/Aufbau-artiges Mischbauteil:

```text
ein reales Pool-Bauteil
→ mit Deckenplattenzone
→ Unterzugzone
→ Stützenstumpf / Kapitellzone
→ unregelmäßiger Mischgeometrie
→ generierten Ports und Anschlusszonen
→ unvollständigen Nachweisen
```

**Wichtige Systemtrennung**

```text
Geometrie-Generatoren
→ erzeugen nur Geometrie, Zonen, Ports, Öffnungen, Flächen, Kanten und geometriebezogene Mengen.

Systemmodule
→ erzeugen Semio-Bindung, Klassifikation, Nachweisstatus, LCA, Logistik, Warnungen und Bereitschaft.

Rule Checker
→ prüft aktive Entwurfs-, Platzierungs- und Verbindungssituationen.
```

---

# 1. Kompakter Regelbaum

Der Rule Checker bleibt auf sechs Hauptkategorien beschränkt:

```text
Rule Checker
│
├── 1. Bauteil + Nachweise
├── 2. Geometrie + Ports
├── 3. Tragwerk + Verbindung
├── 4. Nutzung + Raumqualität
├── 5. Hülle + Bauphysik
└── 6. Logistik + Ökobilanz
```

Jede Regel ist allgemein formuliert, aber auf `AA_MIX_001` anwendbar.

---

# 2. Statuslogik

Jede Regel gibt einen klaren Status zurück:

```text
pass
warning
positive
engineering_required
invalid
not_applicable
```

## Bedeutung

```text
pass:
Die Regel ist mit vorhandenen Daten erfüllt.

warning:
Die Situation ist nutzbar, aber riskant, unvollständig oder qualitätsrelevant.

positive:
Die Situation erzeugt eine räumliche, architektonische oder zirkuläre Qualität.

engineering_required:
Die Geometrie ist vorhanden, aber technischer Nachweis fehlt.

invalid:
Harter Konflikt. Die Aktion darf so nicht ausgeführt werden.

not_applicable:
Die Regel ist für diese Situation nicht relevant.
```

---

# 3. Allgemeine Eingaben des Rule Checkers

## 3.1 Geometrie-Generator-Ausgaben

```yaml
geometry_outputs:
  component_geometry: required
  sub_zone_map: optional_required_if_mixed
  face_map: required
  edge_map: required
  port_map: required
  opening_map: required
  bearing_zone_map: required_if_structural
  envelope_candidate_faces: optional
  semantic_face_candidates: optional
  logistics_geometry: required
  transport_envelope: required
```

## 3.2 Systemdaten

```yaml
system_data:
  component_id: required
  component_typology: required
  material_kind: required
  stock_status: required
  evidence_status: required
  source_context: optional
  design_context: required_for_active_checking
  target_preferences: optional
  project_rule_defaults: required
  lca_defaults: optional
  logistics_context: optional
```

## 3.3 Beispiel `AA_MIX_001`

```yaml
AA_MIX_001:
  component_typology: mixed_slab_beam_column_slice
  material_kind: reinforced_concrete
  sub_zones:
    - slab_zone
    - beam_zone
    - column_zone
    - internal_transition_zones
  ports:
    - slab-edge-bearing
    - beam-end-bearing
    - column-base-bearing
    - internal-beam-column-transition
    - service-penetration-candidate
  evidence_status:
    concrete: missing
    reinforcement: partial_or_missing
    damage: partial_or_missing
    fire: missing
    lca: precheck_only
  default_status: engineering_required
```

---

# 4. Kategorie 1 — Bauteil + Nachweise

Diese Regeln prüfen, ob das Bauteil als reales Pool-Objekt eindeutig, verfügbar und ausreichend dokumentiert ist.

---

## 1.1 Eindeutige Bauteilidentität

### Allgemeine Regel

```yaml
rule_id: component_identity_unique
category: Bauteil + Nachweise
type: hard_rule
checks:
  - component_id_exists
  - component_id_unique
  - component_has_type
  - component_has_material
```

### Input

```text
component_id
component_typology
material_kind
Semio type registry
Bauteilkatalog
```

### Output

```yaml
pass: component is uniquely identifiable
invalid: component_id missing or duplicated
warning: component exists but source metadata incomplete
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
reason:
  - AA_MIX_001 has unique ID
  - typology is defined
  - material is defined as reinforced_concrete
warning:
  - source building and original level are unknown
```

---

## 1.2 Verfügbarkeit im Pool

### Allgemeine Regel

```yaml
rule_id: component_stock_available
category: Bauteil + Nachweise
type: hard_rule
checks:
  - stock_total
  - used_count
  - reserved_count
  - blocked_reason
```

### Output

```yaml
pass: stock_available > 0
warning: reserved but maybe reusable
invalid: stock_available == 0 or blocked
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
reason:
  stock_total: 1
  used_count: 0
  reserved_count: 0
  stock_available: 1
```

---

## 1.3 Nachweisvollständigkeit

### Allgemeine Regel

```yaml
rule_id: evidence_completeness
category: Bauteil + Nachweise
type: evidence_gate
checks:
  - concrete_evidence
  - reinforcement_evidence
  - damage_evidence
  - fire_evidence
  - lca_dataset
  - lifting_evidence
```

### Output

```yaml
pass: required evidence complete
warning: non-critical evidence missing
engineering_required: evidence missing for structural/fire/drilling/lifting
invalid: critical missing evidence for requested action
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  concrete: missing
  reinforcement: partial_or_missing
  fire: missing
  lifting: missing
  lca: precheck_only
```

### Bedeutung

```text
Das Bauteil darf im Entwurf platziert und geometrisch untersucht werden.
Es darf aber nicht statisch freigegeben, gebohrt oder final verbunden werden.
```

---

## 1.4 Schadstoff- und Quellrisiko

### Allgemeine Regel

```yaml
rule_id: source_risk_flag
category: Bauteil + Nachweise
type: evidence_warning
checks:
  - source_building_risk
  - facade_damage_history
  - asbestos_or_pollutant_context
  - contamination_clearance
```

### Output

```yaml
pass: no source risk known and clearance exists
warning: source risk unknown
engineering_required: source has known risk but clearance missing
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning
reason:
  source_building: unknown
  pollutant_clearance: missing
```

### Allgemeine Formulierung

```text
Ein intaktes Tragwerk bedeutet nicht automatisch,
dass das einzelne wiedergewonnene Bauteil schadstofffrei oder wiederverwendungsfähig ist.
```

---

# 5. Kategorie 2 — Geometrie + Ports

Diese Regeln prüfen Form, Subzonen, Ports, Öffnungen und geometrische Kompatibilität.

---

## 2.1 Fragmenttyp erkannt

### Allgemeine Regel

```yaml
rule_id: fragment_typology_classified
category: Geometrie + Ports
type: geometry_precheck
checks:
  - shape_family
  - polygon_footprint
  - sub_zone_map_if_mixed
  - irregular_edges
```

### Output

```yaml
pass: fragment family classified
warning: unusual but classified
invalid: shape unclassified
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
fragment_family: mixed_slab_beam_column_slice
sub_zones:
  - slab_zone
  - beam_zone
  - column_zone
  - internal_transition_zones
```

---

## 2.2 Mischbauteil darf nicht als Einfachbauteil behandelt werden

### Allgemeine Regel

```yaml
rule_id: mixed_fragment_requires_subzone_logic
category: Geometrie + Ports
type: hard_rule
checks:
  - component_has_multiple_structural_subzones
  - design_treats_as_single_simple_type
```

### Output

```yaml
pass: subzone logic active
invalid: mixed element treated as simple slab / beam / column
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
reason:
  subzone logic active
  component not treated as simple slab
```

### Harte Invalid-Bedingung

```text
Wenn AA_MIX_001 als normale flache Deckenplatte verbunden wird,
ohne Unterzug- und Stützenzone zu berücksichtigen:
→ invalid
```

---

## 2.3 Ports vorhanden und typisiert

### Allgemeine Regel

```yaml
rule_id: port_generation_complete
category: Geometrie + Ports
type: geometry_precheck
checks:
  - port_exists
  - port_has_geometry
  - port_has_direction
  - port_has_role
```

### Output

```yaml
pass: required ports exist
warning: optional ports missing
invalid: required connection port missing
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
generated_ports:
  - slab-edge-bearing
  - beam-end-bearing
  - column-base-bearing
  - service-penetration-candidate
```

---

## 2.4 Port-Kompatibilität

### Allgemeine Regel

```yaml
rule_id: port_compatibility
category: Geometrie + Ports
type: connection_precheck
checks:
  - port_A_type
  - port_B_type
  - compatible_port_pairs
  - alignment
  - overlap
```

### Output

```yaml
pass: ports compatible and aligned
warning: compatible but tolerance / proof missing
invalid: incompatible ports
```

### Anwendung auf `AA_MIX_001`

```yaml
example_connection:
  AA_MIX_001.port: slab-edge-bearing
  target_piece.port: wall-top-bearing

status: warning
reason:
  ports are conceptually compatible
  but structural proof and reinforcement evidence missing
```

---

## 2.5 Unregelmäßige Kanten und Winkel

### Allgemeine Regel

```yaml
rule_id: irregular_edge_usability
category: Geometrie + Ports
type: architectural_geometry_warning
checks:
  - acute_angles
  - small_residual_triangles
  - non_orthogonal_edges
  - edge_accessibility
```

### Output

```yaml
pass: irregular geometry usable
warning: awkward corner or inefficient residual area
positive: expressive reuse geometry if desired
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning_or_positive
reason:
  mixed geometry may create strong spatial character
  but irregular edges and projections must be checked in room context
```

---

## 2.6 Öffnungen und Durchdringungen

### Allgemeine Regel

```yaml
rule_id: opening_and_penetration_check
category: Geometrie + Ports
type: geometry_and_evidence_gate
checks:
  - existing_openings
  - penetration_candidates
  - edge_distance
  - bearing_zone_overlap
  - reinforcement_status
```

### Output

```yaml
pass: existing opening usable
warning: opening exists but use unclear
engineering_required: new penetration needs rebar scan
invalid: opening or penetration conflicts with bearing zone
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  no existing openings
  new penetrations require reinforcement scan
  column and transition zones blocked by default
```

---

# 6. Kategorie 3 — Tragwerk + Verbindung

Diese Regeln prüfen Auflager, Lastpfade, Verbindungsprinzipien und technische Nachweise.

---

## 3.1 Auflagerüberdeckung

### Allgemeine Regel

```yaml
rule_id: bearing_overlap
category: Tragwerk + Verbindung
type: structural_precheck
checks:
  - bearing_zone_A
  - bearing_zone_B
  - overlap_area
  - minimum_bearing_length
  - eccentricity
```

### Output

```yaml
pass: geometric bearing sufficient
warning: bearing exists but proof missing
invalid: no bearing overlap or unstable eccentricity
engineering_required: geometry ok but structural proof missing
```

### Anwendung auf `AA_MIX_001`

```yaml
example:
  port: slab-edge-bearing
  target: wall-top-bearing

status: engineering_required
reason:
  bearing geometry can be generated
  but capacity, reinforcement and minimum bearing proof are missing
```

---

## 3.2 Lastpfad-Kontinuität

### Allgemeine Regel

```yaml
rule_id: load_path_continuity
category: Tragwerk + Verbindung
type: structural_precheck
checks:
  - vertical_load_path
  - support_sequence
  - unsupported_edges
  - cantilever_zones
  - mixed_subzone_load_effects
```

### Output

```yaml
pass: load path geometrically continuous
warning: local engineering needed
invalid: unsupported structural zone
engineering_required: load path plausible but not proven
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  slab, beam and column zones produce complex load path
  self weight is high
  structural capacity is unknown
```

---

## 3.3 Neuer Träger / Adapter als legitime Systemkomponente

### Allgemeine Regel

```yaml
rule_id: new_adapter_or_support_component
category: Tragwerk + Verbindung
type: system_component_rule
checks:
  - adapter_has_type
  - adapter_has_geometry
  - adapter_has_ports
  - adapter_material_known
  - adapter_connection_detail_defined
```

### Output

```yaml
pass: adapter fully defined
warning: adapter geometry exists but proof missing
engineering_required: adapter needed for support or tolerance
invalid: adapter missing but required
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  beam-end-bearing or slab-edge-bearing may need new support beam / steel support / concrete adapter
```

### Allgemein wichtig

```text
Der Checker darf neue Hilfsbauteile nicht als Fehler behandeln.
Adapter, neue Träger und Auflager sind Teil des Wiederverwendungssystems.
```

---

## 3.4 Nachträglicher Bewehrungsanschluss

### Allgemeine Regel

```yaml
rule_id: post_installed_rebar_connection
category: Tragwerk + Verbindung
type: engineering_gate
checks:
  - drilling_zone
  - rebar_scan
  - anchor_design
  - grout_or_mortar_detail
  - edge_distance
  - fire_cover_if_required
```

### Output

```yaml
pass: only with verified engineering detail
engineering_required: normal status before proof
invalid: drilling without rebar evidence
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  reinforcement scan missing or partial
  drilling zones not approved
  connection capacity unknown
```

---

## 3.5 No-Drill-Zonen

### Allgemeine Regel

```yaml
rule_id: no_drill_zone_enforcement
category: Tragwerk + Verbindung
type: hard_rule
checks:
  - generated_no_drill_zones
  - known_rebar_zones
  - unknown_rebar_zones
  - bearing_zones
  - transition_zones
```

### Output

```yaml
pass: drilling only in approved zones
engineering_required: zone unknown
invalid: drilling in forbidden zone
```

### Anwendung auf `AA_MIX_001`

```yaml
invalid_if:
  - drilling in slab_beam_transition
  - drilling in beam_column_transition
  - drilling in column_head_region
  - drilling without rebar evidence

status_default: engineering_required
```

---

## 3.6 Anschlussfamilie passend

### Allgemeine Regel

```yaml
rule_id: connector_family_match
category: Tragwerk + Verbindung
type: connection_precheck
checks:
  - port_pair
  - connector_family
  - material_pair
  - reversibility
  - fire_condition
  - structural_role
```

### Output

```yaml
pass: connector family suitable in principle
warning: suitable but detail missing
engineering_required: structural connector not verified
invalid: connector family incompatible
```

### Anwendung auf `AA_MIX_001`

```yaml
possible_connector_families:
  slab_to_wall_or_beam:
    - post_installed_rebar_grout
    - screw_anchor_flat_steel_holder
  column_to_base:
    - stainless_dowel
    - angle_connector
  column_or_beam_to_slab:
    - steel_support
    - engineered_grout_detail

status: engineering_required
```

---

# 7. Kategorie 4 — Nutzung + Raumqualität

Diese Regeln prüfen, ob aus den Bauteilen brauchbare Räume entstehen.  
Sie sind allgemein formuliert und nicht nur auf Wohnungsbau beschränkt.

---

## 4.1 Nutzungsprogramm passt zur Geometrie

### Allgemeine Regel

```yaml
rule_id: program_fit
category: Nutzung + Raumqualität
type: architectural_performance
checks:
  - target_use
  - room_area
  - usable_area
  - obstacle_map
  - ceiling_height
  - daylight_access
```

### Output

```yaml
pass: program fits
warning: program possible with reduced quality
positive: geometry strengthens spatial character
invalid: required function impossible
```

### Anwendung auf `AA_MIX_001`

```yaml
status: depends_on_room_context
warning_if:
  - column zone blocks required use area
  - beam downstand reduces usable height
positive_if:
  - exposed beam/column fragment is desired as spatial character
```

---

## 4.2 Nutzbare Fläche nach Hindernissen

### Allgemeine Regel

```yaml
rule_id: usable_area_after_obstacles
category: Nutzung + Raumqualität
type: spatial_quality
checks:
  - room_polygon
  - obstacle_geometry
  - clear_area
  - minimum_clearance
  - furniture_or_program_zones
```

### Output

```yaml
pass: usable area sufficient
warning: usable area reduced
invalid: required clearance fails
positive: obstacle creates useful zoning
```

### Anwendung auf `AA_MIX_001`

```yaml
obstacles:
  - column_zone
  - beam_downstand
  - irregular slab edge

status: warning_or_positive
```

---

## 4.3 Stütze vor Fenster

### Allgemeine Regel

```yaml
rule_id: column_near_window
category: Nutzung + Raumqualität
type: architectural_quality
checks:
  - column_position
  - window_or_facade_opening
  - daylight_path
  - view_axis
  - clearance
```

### Output

```yaml
warning: daylight or view reduced
positive: expressive structural reuse if target preference allows
invalid: required egress or minimum opening blocked
```

### Anwendung auf `AA_MIX_001`

```yaml
if column_zone placed in front of window:
  status: warning_or_positive
  warning_reason:
    - view may be reduced
    - daylight may be reduced
  positive_reason:
    - visible reused structure expresses original system
```

---

## 4.4 Nische hinter Stütze

### Allgemeine Regel

```yaml
rule_id: niche_behind_obstacle
category: Nutzung + Raumqualität
type: spatial_quality
checks:
  - niche_depth
  - niche_width
  - accessibility
  - program_fit
  - visibility
```

### Output

```yaml
positive: usable niche
warning: dead corner
invalid: inaccessible trap zone if code-relevant
```

### Anwendung auf `AA_MIX_001`

```yaml
if column_zone creates niche:
  status: positive_or_warning
  positive_if:
    - niche usable for shelf, seating, storage, threshold, planting
  warning_if:
    - niche too narrow or inaccessible
```

---

## 4.5 Große Stütze in kleinem Raum

### Allgemeine Regel

```yaml
rule_id: oversized_obstacle_in_small_room
category: Nutzung + Raumqualität
type: program_check
checks:
  - obstacle_size
  - room_size
  - required_clearances
  - fixture_clearances
  - accessibility
```

### Output

```yaml
pass: obstacle acceptable
warning: room quality reduced
invalid: required clearance fails
positive: strong spatial character if accepted by design preference
```

### Anwendung auf `AA_MIX_001`

```yaml
if column_zone lies in small bathroom / kitchen / corridor:
  status: warning_or_invalid
  invalid_if:
    - required fixture clearance fails
    - accessibility clearance fails
```

---

## 4.6 Unregelmäßige Ecke

### Allgemeine Regel

```yaml
rule_id: awkward_corner_detection
category: Nutzung + Raumqualität
type: architectural_warning
checks:
  - acute_angle
  - residual_area
  - accessibility
  - furniture_fit
```

### Output

```yaml
warning: awkward or low-usability corner
positive: spatial character if intentionally used
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning_or_positive
reason:
  mixed fragment edges may create expressive but difficult corners
```

---

## 4.7 Patio / Hof / Lücke

### Allgemeine Regel

```yaml
rule_id: void_or_patio_classification
category: Nutzung + Raumqualität
type: spatial_topology
checks:
  - void_geometry
  - open_to_sky
  - adjacent_rooms
  - access
  - light_air_role
```

### Output

```yaml
pass: void classified as patio / courtyard / service void
warning: unclassified residual void
invalid: inaccessible or harmful void
positive: patio improves light, air, spatial quality
```

### Anwendung auf `AA_MIX_001`

```yaml
if AA_MIX_001 participates in courtyard edge:
  status: pass_or_positive_if_void_classified
  warning_if:
    - patio too narrow
    - drainage missing
    - edge support undefined
```

---

# 8. Kategorie 5 — Hülle + Bauphysik

Diese Regeln prüfen thermische, feuchte-, brandschutz- und fassadenbezogene Szenarien.

---

## 5.1 Hüllrelevanz

### Allgemeine Regel

```yaml
rule_id: envelope_relevance
category: Hülle + Bauphysik
type: building_physics_precheck
checks:
  - exterior_face
  - interior_face
  - thermal_boundary
  - conditioned_space_relation
```

### Output

```yaml
pass: not envelope or envelope data complete
warning: envelope relevance unclear
engineering_required: envelope use needs assembly proof
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required_if_used_as_envelope
reason:
  slab, beam or column zones may cross thermal boundary
  final assembly unknown
```

---

## 5.2 Wärmebrücken an komplexen Kanten

### Allgemeine Regel

```yaml
rule_id: thermal_bridge_complex_edges
category: Hülle + Bauphysik
type: energy_warning
checks:
  - edge_count
  - projections
  - connector_crossings
  - material_continuity
```

### Output

```yaml
pass: no thermal boundary affected
warning: thermal bridge risk
engineering_required: detailed thermal bridge calculation needed
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning_or_engineering_required
risk_zones:
  - slab_edges
  - beam_downstand_if_exterior
  - column_zone_if_crossing_envelope
```

---

## 5.3 Feuchte- und Witterungsdetails

### Allgemeine Regel

```yaml
rule_id: moisture_weathering_edges
category: Hülle + Bauphysik
type: building_physics_warning
checks:
  - exposed_horizontal_faces
  - exterior_corners
  - joints
  - patio_edges
  - drainage_strategy
```

### Output

```yaml
pass: detail defined
warning: drainage or waterproofing missing
engineering_required: roof / ground / exterior exposure needs proof
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning
warning_if:
  - slab top exposed
  - column base near ground
  - beam downstand exposed to weather
```

---

## 5.4 Brandschutz bei Anschlüssen

### Allgemeine Regel

```yaml
rule_id: connector_fire_exposure
category: Hülle + Bauphysik
type: fire_precheck
checks:
  - connector_material
  - exposed_steel
  - fire_relevant_surface
  - compartment_context
```

### Output

```yaml
pass: fire detail proven
warning: exposed steel needs treatment
engineering_required: fire context unknown or proof missing
invalid: known fire requirement not met
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  connector family may include steel plates, angle connectors, anchors or steel supports
  fire document missing
```

---

## 5.5 Fassaden- und Zickzackkanten

### Allgemeine Regel

```yaml
rule_id: facade_edge_expression_and_risk
category: Hülle + Bauphysik
type: architectural_and_physics
checks:
  - facade_polyline
  - projections
  - recesses
  - exterior_corner_count
  - weathering
  - thermal_bridge_risk
```

### Output

```yaml
positive: reuse structure readable in facade
warning: many exterior corners need detailing
engineering_required: envelope and fire checks missing
```

### Anwendung auf `AA_MIX_001`

```yaml
if AA_MIX_001 creates facade projection:
  status: positive_and_warning
  positive:
    - reused structural logic becomes visible
  warning:
    - weathering and thermal bridges need detail
```

---

# 9. Kategorie 6 — Logistik + Ökobilanz

Diese Regeln prüfen Bestand, Transport, Montagefolge, Hebung, Lagerung und Umweltwirkung.

---

## 6.1 Eindeutige Nutzung eines Bauteils

### Allgemeine Regel

```yaml
rule_id: unique_piece_use
category: Logistik + Ökobilanz
type: inventory_hard_rule
checks:
  - component_id
  - active_piece_instances
  - stock_available
```

### Output

```yaml
pass: piece used once or stock available
invalid: same unique piece used twice
```

### Anwendung auf `AA_MIX_001`

```yaml
status: pass
reason:
  unique piece not yet placed
```

---

## 6.2 Lagerung passend zur Geometrie

### Allgemeine Regel

```yaml
rule_id: storage_orientation_safe
category: Logistik + Ökobilanz
type: logistics_precheck
checks:
  - component_geometry
  - center_of_gravity
  - support_points
  - original_orientation
  - stacking_condition
```

### Output

```yaml
pass: storage orientation proven
warning: storage needs support strategy
engineering_required: lifting or storage design missing
invalid: unstable storage
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  mixed slab-beam-column geometry cannot be stored like flat slab by default
  column stump creates eccentric support condition
```

---

## 6.3 Hebe- und Montagefähigkeit

### Allgemeine Regel

```yaml
rule_id: lifting_and_assembly_readiness
category: Logistik + Ökobilanz
type: logistics_engineering_gate
checks:
  - mass
  - center_of_gravity
  - lifting_points
  - crane_capacity
  - temporary_support
```

### Output

```yaml
pass: lifting plan proven
warning: heavy or eccentric piece
engineering_required: lifting points unknown
invalid: exceeds known crane / lifting limit
```

### Anwendung auf `AA_MIX_001`

```yaml
status: engineering_required
reason:
  estimated mass is high
  center of gravity is eccentric
  lifting points unknown
```

---

## 6.4 Transportgrenzen

### Allgemeine Regel

```yaml
rule_id: transport_limit_check
category: Logistik + Ökobilanz
type: logistics_precheck
checks:
  - transport_envelope
  - mass
  - route
  - vehicle_type
  - permits
```

### Output

```yaml
pass: within transport limits
warning: near limit or route unknown
engineering_required: special support / permit unclear
invalid: exceeds hard limit
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning
reason:
  transport envelope is known
  but support frame and route constraints are not defined
```

---

## 6.5 Ökobilanz-Vorprüfung

### Allgemeine Regel

```yaml
rule_id: lca_precheck
category: Logistik + Ökobilanz
type: environmental_precheck
checks:
  - reused_mass
  - transport_distance
  - transport_factor
  - new_equivalent_reference
  - connector_adapter_impacts
  - dataset_completeness
```

### Output

```yaml
pass: full LCA complete
warning: precheck only
positive: reuse has avoided-GWP potential
engineering_required: environmental declaration / dataset missing
```

### Anwendung auf `AA_MIX_001`

```yaml
status: positive_and_warning
positive:
  - reused mass has avoided new-material potential
warning:
  - connector and adapter impacts missing
  - full dataset incomplete
  - result is only precheck
```

---

## 6.6 Montage- und Sequenzlogik

### Allgemeine Regel

```yaml
rule_id: assembly_sequence_consistency
category: Logistik + Ökobilanz
type: process_check
checks:
  - piece_sequence
  - storage_order
  - transport_batch
  - crane_reach
  - dependency_graph
```

### Output

```yaml
pass: sequence defined
warning: sequence incomplete
invalid: impossible sequence or inaccessible piece
```

### Anwendung auf `AA_MIX_001`

```yaml
status: warning
reason:
  mixed element likely needs defined assembly order, temporary supports, and access strategy
```

---

# 10. Allgemeine Regel-zu-Beispiel-Matrix

| Allgemeine Regel | Zweck | Anwendung auf `AA_MIX_001` |
|---|---|---|
| component_identity_unique | eindeutige ID | pass |
| component_stock_available | Bestand prüfen | pass |
| evidence_completeness | Nachweise prüfen | engineering_required |
| source_risk_flag | Schadstoff-/Quellrisiko | warning |
| fragment_typology_classified | Formfamilie erkennen | pass |
| mixed_fragment_requires_subzone_logic | Mischbauteil korrekt behandeln | pass / invalid wenn als einfache Platte genutzt |
| port_generation_complete | Ports vorhanden | pass |
| port_compatibility | Ports zueinander prüfen | warning / engineering_required |
| irregular_edge_usability | Sonderform nutzbar machen | warning / positive |
| opening_and_penetration_check | Öffnungen / Durchdringungen | engineering_required |
| bearing_overlap | Auflagerüberdeckung | engineering_required |
| load_path_continuity | Lastpfad | engineering_required |
| new_adapter_or_support_component | neue Träger / Adapter | engineering_required |
| post_installed_rebar_connection | nachträglicher Bewehrungsanschluss | engineering_required |
| no_drill_zone_enforcement | Bohren verhindern | invalid bei verbotenen Zonen |
| connector_family_match | passende Anschlussfamilie | engineering_required |
| program_fit | Nutzung passt | kontextabhängig |
| usable_area_after_obstacles | nutzbare Fläche | warning / positive |
| column_near_window | Stütze vor Fenster | warning / positive |
| niche_behind_obstacle | Nische hinter Stütze | positive / warning |
| oversized_obstacle_in_small_room | große Stütze kleiner Raum | warning / invalid |
| awkward_corner_detection | unpraktische Ecke | warning / positive |
| void_or_patio_classification | Patio / Hof | positive / warning |
| envelope_relevance | Hüllrelevanz | engineering_required wenn Hülle |
| thermal_bridge_complex_edges | Wärmebrücken | warning |
| moisture_weathering_edges | Feuchte / Witterung | warning |
| connector_fire_exposure | Brandschutz Anschluss | engineering_required |
| facade_edge_expression_and_risk | Fassadenkante / Ausdruck | positive + warning |
| unique_piece_use | eindeutige Nutzung | pass |
| storage_orientation_safe | sichere Lagerung | engineering_required |
| lifting_and_assembly_readiness | Heben / Montage | engineering_required |
| transport_limit_check | Transport | warning |
| lca_precheck | Ökobilanz | positive + warning |
| assembly_sequence_consistency | Montagefolge | warning |

---

# 11. Checker-Verhalten beim Platzieren von `AA_MIX_001`

## 11.1 Wenn der User das Bauteil nur platziert

```yaml
trigger: place_piece
piece: AA_MIX_001
```

### Checker läuft

```text
component_identity_unique
component_stock_available
fragment_typology_classified
mixed_fragment_requires_subzone_logic
storage_orientation_safe
lifting_and_assembly_readiness
lca_precheck
```

### Ergebnis

```yaml
placement_status: allowed_with_warnings
warnings:
  - mixed geometry requires subzone logic
  - lifting and storage require engineering review
  - LCA is precheck only
```

---

## 11.2 Wenn der User `AA_MIX_001` als einfache Platte verwenden will

```yaml
trigger: assign_role
piece: AA_MIX_001
requested_role: simple_slab
```

### Checker läuft

```text
mixed_fragment_requires_subzone_logic
load_path_continuity
usable_area_after_obstacles
```

### Ergebnis

```yaml
status: invalid
reason:
  - piece contains beam and column sub-zones
  - cannot be treated as simple slab
```

---

## 11.3 Wenn der User eine Deckenrand-Verbindung erstellt

```yaml
trigger: connect
piece_A: AA_MIX_001
port_A: slab-edge-bearing
piece_B: wall_or_beam
port_B: wall-top-bearing_or_beam-top-bearing
```

### Checker läuft

```text
port_compatibility
bearing_overlap
connector_family_match
post_installed_rebar_connection
no_drill_zone_enforcement
connector_fire_exposure
```

### Ergebnis

```yaml
status: engineering_required
reason:
  - geometry and ports are compatible in principle
  - structural capacity missing
  - reinforcement scan missing
  - connector detail missing
```

---

## 11.4 Wenn der User in eine Übergangszone bohren will

```yaml
trigger: drill
piece: AA_MIX_001
zone: beam_column_transition
```

### Checker läuft

```text
no_drill_zone_enforcement
post_installed_rebar_connection
evidence_completeness
```

### Ergebnis

```yaml
status: invalid
reason:
  - transition zone is no-drill by default
  - reinforcement position unknown
  - high structural risk
```

---

## 11.5 Wenn das Bauteil eine Nische im Raum erzeugt

```yaml
trigger: room_update
piece: AA_MIX_001
effect: niche_behind_column
```

### Checker läuft

```text
niche_behind_obstacle
usable_area_after_obstacles
program_fit
```

### Ergebnis

```yaml
status: positive_or_warning
positive_if:
  - niche is accessible
  - niche fits program
  - target preference values spatial complexity
warning_if:
  - niche is too narrow
  - creates dead space
```

---

## 11.6 Wenn das Bauteil Teil einer Fassade wird

```yaml
trigger: assign_envelope_context
piece: AA_MIX_001
context: exterior_facade
```

### Checker läuft

```text
envelope_relevance
thermal_bridge_complex_edges
moisture_weathering_edges
connector_fire_exposure
facade_edge_expression_and_risk
```

### Ergebnis

```yaml
status: engineering_required_with_positive_architectural_value
positive:
  - expressive reused structure visible at facade
warnings:
  - thermal bridge risk
  - weathering detail missing
  - fire context missing
```

---

# 12. Minimaler Implementierungs-Output

Für jede Regel sollte der Checker diese Struktur zurückgeben:

```yaml
rule_result:
  rule_id: string
  category: string
  status: pass | warning | positive | engineering_required | invalid | not_applicable
  affected_piece_ids: []
  affected_ports: []
  affected_zones: []
  message: string
  reason: string
  required_next_data: []
  suggested_actions: []
  severity: low | medium | high | critical
```

## Beispiel für `AA_MIX_001`

```yaml
rule_result:
  rule_id: no_drill_zone_enforcement
  category: Tragwerk + Verbindung
  status: invalid
  affected_piece_ids:
    - AA_MIX_001
  affected_zones:
    - beam_column_transition
  message: Nicht in die Unterzug-Stützen-Übergangszone bohren.
  reason: Diese Zone ist tragwerksrelevant und die Bewehrungslage ist unbekannt.
  required_next_data:
    - vollständiger Bewehrungsscan
    - statischer Anschlussnachweis
  suggested_actions:
    - alternative Anschlusszone wählen
    - Adapter oder neuen Träger verwenden
  severity: critical
```

---

# 13. Schlussfolgerung

Die Regeln bleiben allgemein, weil sie nicht speziell auf Abbau/Aufbau oder `AA_MIX_001` festgelegt sind.

Sie sind aber auf `AA_MIX_001` anwendbar, weil sie mit generischen Inputs arbeiten:

```text
Typologie
Subzonen
Ports
Auflagerzonen
Öffnungen
Nachweisstatus
Nutzungskontext
Hüllkontext
Logistikkontext
LCA-Kontext
```

Dadurch kann derselbe Rule Checker später auch andere Projekte prüfen:

```text
einfache Deckenplatten
Träger
Wände
Stützen
Treppen
Sonderformen
Mischfragmente
Adapter
neue Hilfsträger
```

Der entscheidende Punkt:

```text
Die Regeln prüfen nicht nur, ob Bauteile verbunden werden können.
Sie prüfen auch, ob aus wiederverwendeten Fragmenten sichere,
brauchbare und architektonisch sinnvolle Räume entstehen.
```
