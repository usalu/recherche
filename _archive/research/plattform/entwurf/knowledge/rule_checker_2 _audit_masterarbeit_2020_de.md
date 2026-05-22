# Regelprüfer-Audit  
## Abbau/Aufbau Masterarbeit 2020 — Szenarien aus Text und Bildern

**Ziel:** Prüfen, ob der bisherige Rule Checker die Szenarien der Masterarbeit 2020 abdeckt.  
**Korrekte Systemlogik:** Geometrie-Generatoren erzeugen nur Geometrie, Zonen, Ports, Öffnungen, Flächen, Kanten und geometriegebundene Mengen. Alle Bewertungen, Warnungen, Nachweise und Regelentscheidungen kommen von Systemmodulen und dem Rule Checker.

---

# 0. Quelle und Status

## Geprüfte Quelle

```text
Abbau/Aufbau
Masterarbeit 2020
Christoph Henschel
MA Thesis 2020, UdK Berlin
Fallstudie: Rathaus Ahlen
```

## Relevante Projektdaten aus der Seite

```text
Ziel:
Ein abzureißendes Stahlbetongebäude wird in Elemente zerlegt,
und diese Elemente werden zum Bau eines neuen Gebäudes an anderem Standort verwendet.

Fallstudie:
Rathaus Ahlen, Baujahr 1970, Stahlbetonkonstruktion laut Gutachten vollständig intakt.

Geometrische Grundlage:
neunstöckiger Verwaltungstrakt mit dreieckigem Raster.

Elementformen:
Parallelogramme, Trapezformen und Sonderformen.

Finales Projekt:
Wohnhaus aus 440 Zuschnittteilen.
23 ein- und zweistöckige Wohnungen.
Wohnungsgrößen zwischen 90 m² und 140 m².
Schmale Innenhöfe liefern Licht und Luft.
Innere Struktur ist an der zickzackartigen Fassade ablesbar.

Konstruktionsprinzip:
wiederverwendete Betonteile ruhen auf einem neuen Halbfertigteilträger aus Stahlbeton.
Die Verbindung erfolgt über nachträglichen Bewehrungsanschluss.
```

## Wichtige Einschränkung für unser System

Unser Konzept ignoriert den aktiven Zuschnittprozess.  
Aber der Rule Checker muss die **Ergebnisse des Zuschnitts** abdecken:

```text
unregelmäßige Platten
Trapeze
Parallelogramme
Sonderformen
Bauteile mit Stützenresten
Bauteile mit Unterzügen
Bauteile mit Mischgeometrien
viele einzigartige Einzelteile
```

---

# 1. Bildanalyse: Was die Bilder als Szenarien zeigen

## 1.1 Elementekatalog / Teilekatalog

Die Katalogbilder zeigen viele Einzelteile mit unterschiedlichen Grundrissen, Winkeln und teilweise vertikalen Stützen-/Unterzuganteilen.

```text
Szenario:
Nicht alle Bauteile sind einfache rechteckige Platten.

Rule-Checker-Folge:
Der Checker braucht eine Fragment-Typologie, nicht nur slab / beam / column.
```

Erforderliche Geometrietypen:

```text
irregular_slab
trapezoid_slab
parallelogram_slab
slab_with_downstand_beam
slab_with_column_stub
slab_beam_column_fragment
special_fragment
```

## 1.2 Zusammengesetzte Betonteile / Hofhausstruktur

Das Bild der zusammengesetzten Betonteile zeigt eine teppichartige Struktur mit Höfen, Lücken, Zeilen und unregelmäßigen Gebäudevorsprüngen.

```text
Szenario:
Lücken sind nicht automatisch Fehler.
Sie können Innenhöfe, Lichthöfe oder Erschließungsräume sein.

Rule-Checker-Folge:
Der Checker muss zwischen Fehlerlücke und intentionalem Patio unterscheiden.
```

Benötigte Regeln:

```text
void_is_classified
patio_has_light_air_access
patio_has_minimum_width
patio_has_drainage_strategy
patio_edges_are_supported
units_have_outdoor_or_light_access
```

## 1.3 Stützen vor Fenstern

Die Bildserie „Stützen vor Fenstern“ zeigt eine Stütze nahe an einer Fensterzone.

```text
Szenario:
Ein tragendes Element blockiert möglicherweise Fenster, Blick, Tageslicht oder Möblierung.

Rule-Checker-Folge:
Das ist nicht automatisch ungültig.
Es ist eine architektonische Warnung oder Qualität, abhängig von Zielpräferenzen.
```

Benötigte Regeln:

```text
column_window_clearance
daylight_obstruction_warning
view_obstruction_warning
furniture_clearance_near_column
architectural_quality_if_intentional
```

## 1.4 Nische hinter Stütze

Das Bild „Nische hinter Stütze“ zeigt eine nutzbare oder problematische Restzone hinter einer Stütze.

```text
Szenario:
Irreguläre Geometrie erzeugt Nischen.

Rule-Checker-Folge:
Der Checker darf Nischen nicht pauschal als Fehler bewerten.
Er muss zwischen nutzbarer Nische, Totraum und Konfliktzone unterscheiden.
```

Benötigte Regeln:

```text
niche_depth
niche_width
niche_accessibility
niche_program_fit
dead_corner_warning
positive_spatial_quality_tag
```

## 1.5 Große Stütze in kleinem Raum

Das Bild „Große Stütze in kleinem Raum“ zeigt eine dominante Stütze in einem engen Raum, etwa Bad oder Nebenraum.

```text
Szenario:
Das Bauteil ist konstruktiv möglich, kann aber Raumfunktion, Bewegungsfläche und Möblierung stören.

Rule-Checker-Folge:
Der Checker braucht Nutzungskontext.
Eine große Stütze in einem Bad ist anders zu bewerten als in einem Atelier oder Hof.
```

Benötigte Regeln:

```text
room_usable_area_after_obstacles
minimum_clearance_for_program
bathroom_fixture_clearance
accessibility_clearance
oversized_column_warning
spatial_character_positive_if_preferred
```

## 1.6 Verbindung auf neuem Halbfertigteilträger

Die Seite beschreibt, dass die wiederverwendeten Teile auf einem neuen Halbfertigteilträger aus Stahlbeton ruhen und durch nachträglichen Bewehrungsanschluss kraftschlüssig verbunden werden.

```text
Szenario:
Wiederverwendetes Fragment + neuer Träger + nachträglicher Bewehrungsanschluss.

Rule-Checker-Folge:
Der Checker muss neue Adapter-/Trägerelemente als Systemkomponenten akzeptieren.
```

Benötigte Regeln:

```text
new_support_beam_port
reclaimed_piece_to_new_beam_bearing
post_installed_rebar_connection_required
grout_or_mortar_connection_required
bearing_length_check
rebar_scan_required_before_drilling
connector_capacity_engineering_required
fire_cover_for_connection
```

---

# 2. Fehlende oder zu schwache Regelgruppen im bisherigen Checker

Der bisherige Checker deckt Bauteilpass, Geometrie, Ports, LCA, Logistik, Bohrzonen und Nachweise bereits ab.  
Aus der Masterarbeit 2020 müssen jedoch folgende Regelgruppen explizit ergänzt werden.

---

## A. Fragment- und Sonderform-Regeln

### Warum nötig

Die Masterarbeit erzeugt viele unregelmäßige Bauteile:

```text
Parallelogramme
Trapeze
Sonderformen
Platten mit Stützenanteilen
Platten mit Unterzügen
Mischfragmente
```

### Generator-Ausgabe

```text
polygon_footprint
edge_angle_list
edge_length_list
non_orthogonal_edges
sub_zone_map
support_projection_map
overhang_map
fragment_family
```

### System- / Checker-Regeln

```yaml
rules:
  - id: fragment_shape_classification
    type: geometry_precheck
    result:
      pass: shape_classified
      warning: shape_unusual_but_usable
      invalid: shape_unclassified

  - id: acute_angle_usability
    type: architectural_warning
    result:
      warning: acute_angle_creates_low_usability_corner

  - id: fragment_orientation_locked
    type: reuse_constraint
    result:
      warning: flipping_or_rotating_changes_top_bottom_or_rebar_assumption

  - id: mixed_fragment_requires_subzone_logic
    type: hard_gate
    result:
      invalid: treated_as_simple_slab
      pass: subzones_detected
```

---

## B. Patio- und Hofhaus-Regeln

### Warum nötig

Das finale Projekt nutzt schmale Innenhöfe für Licht und Luft.  
Lücken sind also ein Entwurfsprinzip, nicht nur Restflächen.

### Generator-Ausgabe

```text
void_geometry
patio_candidate
open_to_sky_candidate
adjacent_room_edges
facade_edge_map
```

### System- / Checker-Regeln

```yaml
rules:
  - id: void_classification
    type: spatial_topology
    result:
      pass: void_is_patio_or_courtyard
      warning: unclassified_void
      invalid: inaccessible_or_unventilated_void_if_required

  - id: patio_light_air_access
    type: architectural_performance
    result:
      pass: patio_supplies_adjacent_rooms
      warning: patio_too_narrow_or_too_deep
      invalid: no_light_air_access_for_required_room

  - id: patio_edge_support
    type: structural_precheck
    result:
      pass: all_patio_edges_supported_or_engineered
      warning: support_needs_engineering
      invalid: unsupported_edge

  - id: patio_drainage_strategy
    type: building_physics_warning
    result:
      warning: drainage_not_defined
```

---

## C. Wohnungs- und Raumqualitätsregeln

### Warum nötig

Die Masterarbeit beschreibt, dass erste Assemblagen zu große Wohnungen und unpraktische Ecken/Winkel erzeugten.  
Spätere Entwürfe wurden genauer auf Wohnungen und Räume abgestimmt.

### Generator-Ausgabe

```text
room_polygon
obstacle_geometry
usable_area_polygon
edge_angle_map
column_positions
beam_downstand_positions
```

### System- / Checker-Regeln

```yaml
rules:
  - id: dwelling_area_range
    type: target_preference_or_project_rule
    result:
      pass: unit_area_within_target
      warning: unit_too_large_or_too_small

  - id: usable_area_after_obstacles
    type: architectural_performance
    result:
      pass: usable_area_sufficient
      warning: usable_area_reduced_by_columns_or_angles
      invalid: room_function_not_possible

  - id: impractical_corner_detection
    type: architectural_warning
    result:
      warning: acute_or_tiny_corner_detected

  - id: furniture_fit
    type: program_check
    result:
      pass: basic_furniture_fits
      warning: furniture_fit_limited
      invalid: required_fixture_clearance_failed

  - id: circulation_clearance
    type: accessibility_or_function
    result:
      pass: route_clear
      warning: narrow_route
      invalid: route_blocked
```

---

## D. Stütze-Fenster-Nische-Regeln

### Warum nötig

Die Seite hebt drei räumlich wertvolle Situationen hervor:

```text
Stützen vor Fenstern
Nische hinter Stütze
große Stütze in kleinem Raum
```

Diese Szenarien müssen als eigene architektonische Regeln auftauchen.

### Generator-Ausgabe

```text
column_geometry
window_edge_or_facade_opening_candidate
niche_geometry
room_boundary_geometry
obstacle_clearance_map
```

### System- / Checker-Regeln

```yaml
rules:
  - id: column_in_front_of_window
    type: architectural_warning_or_quality
    result:
      warning: view_or_daylight_reduced
      positive: expressive_reuse_condition_if_preferred

  - id: niche_behind_column
    type: spatial_quality
    result:
      positive: usable_niche
      warning: dead_space
      invalid: inaccessible_trap_zone_if_code_relevant

  - id: oversized_column_in_small_room
    type: program_check
    result:
      warning: room_quality_reduced
      invalid: bathroom_or_access_clearance_failed
      positive: strong_spatial_character_if_preferred
```

---

## E. Fassaden- und Zickzack-Regeln

### Warum nötig

Die Seite beschreibt, dass die innere Struktur an der Fassade mit zickzackartigen Vorsprüngen ablesbar wird.

### Generator-Ausgabe

```text
facade_edge_polyline
zigzag_depth
projection_map
corner_count
exterior_face_candidates
```

### System- / Checker-Regeln

```yaml
rules:
  - id: zigzag_facade_expression
    type: architectural_quality
    result:
      positive: internal_reuse_structure_legible
      warning: too_many_unresolved_external_corners

  - id: facade_weathering
    type: envelope_warning
    result:
      warning: exposed_corner_needs_waterproofing_or_detail

  - id: thermal_bridge_at_zigzag_edges
    type: energy_precheck
    result:
      warning: thermal_bridge_risk_at_many_edges

  - id: facade_fire_separation
    type: code_context
    result:
      engineering_required: if_fire_distance_or_compartment_unknown
```

---

## F. Neue-Träger- und Adapter-Regeln

### Warum nötig

Das finale Projekt nutzt neue Halbfertigteilträger als Auflager und nachträgliche Bewehrungsanschlüsse.

### Generator-Ausgabe

```text
reclaimed_piece_bearing_edge
new_beam_axis
new_beam_top_bearing_surface
connector_port_pair
drilling_zone_candidate
```

### System- / Checker-Regeln

```yaml
rules:
  - id: reclaimed_piece_on_new_beam
    type: structural_precheck
    result:
      pass: bearing_geometry_aligned
      warning: bearing_needs_static_proof
      invalid: no_bearing_overlap

  - id: post_installed_rebar_connection
    type: engineering_required
    result:
      engineering_required: rebar_scan_anchor_design_grout_detail_needed

  - id: force_fit_connection_status
    type: structural_connection
    result:
      pass: only_if_engineer_verified
      warning: detail_missing
      invalid: connector_not_defined

  - id: grout_gap_and_tolerance
    type: construction_precheck
    result:
      warning: joint_gap_or_tolerance_missing
```

---

## G. Logistik- und Mengenregeln für 440 Teile

### Warum nötig

Das finale Projekt verwendet 440 Zuschnittteile.  
Der Checker muss also Massen, Reihenfolge, Verfügbarkeit und eindeutige IDs über viele Einzelstücke stabil verwalten.

### Generator-Ausgabe

```text
transport_envelope_per_piece
mass_per_piece
support_points_per_piece
assembly_sequence_geometry
```

### System- / Checker-Regeln

```yaml
rules:
  - id: unique_piece_use
    type: inventory_hard_rule
    result:
      invalid: same_piece_used_twice

  - id: sequence_storage_installation
    type: logistics_warning
    result:
      warning: storage_order_not_matching_assembly_sequence

  - id: crane_and_transport_limits
    type: logistics_hard_or_warning
    result:
      pass: within_limits
      warning: near_limit
      invalid: exceeds_transport_or_crane_limit

  - id: assembly_batch_consistency
    type: process_check
    result:
      warning: many_unique_shapes_without_sequence_or_label_plan
```

---

## H. Schadstoff- und Bestandsrisiko-Regeln

### Warum nötig

Beim Rathaus Ahlen werden Asbestvorkommen und Fassadenschäden erwähnt, obwohl die Stahlbetonkonstruktion als intakt beschrieben wird.

### Generator-Ausgabe

```text
source_zone_relation
surface_origin_candidate
facade_adjacency_candidate
```

### System- / Checker-Regeln

```yaml
rules:
  - id: hazardous_material_source_flag
    type: evidence_gate
    result:
      warning: source_building_has_asbestos_history
      engineering_required: contamination_clearance_missing

  - id: facade_damage_origin_flag
    type: condition_warning
    result:
      warning: element_from_facade_related_zone_needs_surface_check

  - id: intact_structure_not_equal_to_approved_reuse
    type: evidence_gate
    result:
      warning: intact_existing_structure_still_requires_component_proof
```

---

# 3. Updated Rule-Checker Status

## Already covered by previous checker

```text
identity
stock availability
geometry / interface check
component passport completeness
basic structural readiness
connector readiness
bohrzonen / no-drill zones
fire data status
building physics precheck
services / TGA status
logistics
transport
LCA precheck
documentation
pool warnings
rule-checker readiness
```

## Must be added or made explicit

```text
fragment typology rules
irregular shape usability
patio / courtyard rules
room usability rules
column-window-niche scenarios
zigzag facade rules
new beam / adapter support rules
large quantity / 440-piece inventory logic
asbestos / hazardous source flag
spatial-quality-as-opportunity rules
```

---

# 4. Concrete Rule Tree Addition

The high-level checker tree should stay compact:

```text
Rule Checker
│
├── 1. Component + Evidence
├── 2. Geometry + Ports
├── 3. Structural + Connection
├── 4. Architecture + Use Quality
├── 5. Envelope + Building Physics
└── 6. Logistics + LCA
```

The Masterarbeit 2020 scenarios land mainly in:

```text
2. Geometry + Ports
  ├── irregular fragment classification
  ├── mixed fragment sub-zones
  ├── port generation for special fragments
  └── void / patio geometry

3. Structural + Connection
  ├── support on new semi-precast beam
  ├── post-installed reinforcement connection
  ├── bearing overlap
  ├── no-drill until rebar evidence
  └── engineering proof for force-fit connection

4. Architecture + Use Quality
  ├── room area and usability
  ├── impractical corners
  ├── column in front of window
  ├── niche behind column
  ├── oversized column in small room
  ├── patio light and air
  └── zigzag facade expression

5. Envelope + Building Physics
  ├── facade edge complexity
  ├── thermal bridges at zigzag edges
  ├── moisture/weathering at corners
  └── courtyard drainage

6. Logistics + LCA
  ├── 440-piece ID tracking
  ├── storage and assembly sequence
  ├── transport/crane limits
  ├── 4.5 km local transport scenario
  └── reuse vs new material precheck
```

---

# 5. Exact Scenario-to-Rule Mapping

| Scenario from Masterarbeit 2020 | Geometry Generator output | System / Rule Checker output |
|---|---|---|
| Parallelogram / trapezoid pieces | polygon footprint, edge angles | irregular fragment classified, acute-corner warning |
| Special mixed pieces | sub-zone map | mixed fragment cannot be treated as simple slab |
| Carpet-like assembly with voids | void geometry | patio or unclassified void check |
| Patio houses | courtyard geometry, adjacent rooms | light/air, drainage, edge support rules |
| Too-large or awkward apartments | room polygons | unit area and usability warnings |
| Stützen vor Fenstern | column + window relation | daylight/view obstruction or positive spatial character |
| Nische hinter Stütze | niche geometry | usable niche / dead-space classification |
| Große Stütze in kleinem Raum | obstacle in room | clearance, fixture, usability check |
| Zigzag facade | facade polyline | thermal bridge, weathering, expression rules |
| 440 parts | piece IDs + inventory graph | unique use, stock, sequence checks |
| New semi-precast support beam | new beam port + piece bearing port | bearing overlap + force-fit connection proof |
| Post-installed reinforcement | drilling/anchor candidates | rebar scan and engineering proof required |
| Rathaus with asbestos / facade damage | source-risk metadata | hazardous-material evidence gate |

---

# 6. Minimal Implementation Logic

## 6.1 Geometry Generators must output

```yaml
geometry_outputs:
  fragment_family: irregular_slab | trapezoid_slab | slab_with_stub | slab_with_beam | mixed_fragment
  polygon_footprint: required
  edge_angle_list: required
  sub_zone_map: required_if_mixed
  column_zones: optional
  beam_zones: optional
  support_edges: required
  bearing_faces: required
  ports: required
  void_candidates: required_in_assembly
  room_obstacle_map: required_in_design_context
  facade_polyline: required_if_exterior
  transport_envelope: required
```

## 6.2 System modules must add

```yaml
system_outputs:
  evidence_status
  contamination_status
  structural_proof_status
  connector_proof_status
  room_program_context
  target_design_preferences
  patio_classification
  facade_context
  unit_area
  logistics_sequence
  lca_precheck
```

## 6.3 Rule checker statuses

```yaml
statuses:
  pass: rule satisfied from available data
  warning: usable but risk or quality issue
  positive: spatial or circular-design opportunity
  engineering_required: cannot approve without proof
  invalid: hard conflict or impossible condition
```

---

# 7. Final Required Checker Additions

```text
ADD:
- Fragment family classifier
- Irregular edge and acute-angle usability checker
- Patio / void classifier
- Room usability checker
- Column-window-niche checker
- Zigzag facade checker
- New support beam adapter checker
- Post-installed reinforcement connection checker
- Large-inventory sequencing checker
- Hazardous source flag checker

KEEP:
- structural proof as engineering_required
- no drilling without rebar evidence
- LCA as precheck unless datasets are complete
- connection results outside Bauteilpass
```

---

# 8. Bottom Line

The current rule-checker structure is mostly correct, but the Masterarbeit 2020 adds an important missing layer:

```text
The checker must evaluate not only whether components connect,
but also whether irregular reused fragments create usable, safe,
and architecturally valuable spaces.
```

Therefore, the system needs explicit rules for:

```text
irregular fragments
patio voids
spatial obstacles
columns near windows
niches
large columns in small rooms
zigzag facades
new support beam connections
large-scale inventory control
hazardous source evidence
```

These are not optional extras.  
They are central scenarios of the Abbau/Aufbau Masterarbeit 2020.
