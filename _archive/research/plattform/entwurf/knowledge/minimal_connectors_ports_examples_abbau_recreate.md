# Minimal Package Abstractions for the New Component System  
## Abbau/Aufbau + SlabBeamColumnFragment + ReCreate Examples

**Purpose**  
This document adapts the package logic to the new system model:

```text
Component
→ Package
→ Representation
→ Representation properties
→ Connectors
→ Ports
→ Rules / checks
```

The goal is to keep the abstraction **minimal but complete**.  
A connector is created only when the geometry becomes actionable for:

```text
connection
calculation
warning
compatibility
design decision
```

A port defines compatibility.  
A connector places that compatibility on a representation.

---

# 0. Sources and Example Set

## 0.1 Source References

### Abbau/Aufbau Handbuch

Used for:

```text
Bauteilkatalog structure
DE_1OG_001 slab data
reinforced-concrete connection families
logistics / storage logic
energy / U-value example
evidence needs for concrete and reinforcement
```

Source:  
Abbau/Aufbau, *Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden*, 2023.  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

Important source facts used:

```text
Bauteilkatalog fields:
ID, Maße, Öffnungsmaße, Volumen, Masse, Elementtyp,
optional Skizze, Beton- und Bewehrungsuntersuchungen.

Example element:
DE_1OG_001
L 4500 mm
B 2300 mm
H 180 mm
Volumen 1.863 m³
Masse ca. 4.1 t

Connection families:
Wand - Decke:
- nachträglicher Bewehrungsanschluss + Verguss
- Schraubanker mit Flachstahlhalter

Stütze - Decke:
- nachträglich montierter Edelstahldorn
- Winkelverbinder
- Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
- Auflager auf Stahlträger
```

### Abbau/Aufbau Masterarbeit 2020

Used for the **SlabBeamColumnFragment** example.

Source:  
https://abbauaufbau.de/project/masterarbeit-2020

Important source facts used:

```text
The Masterarbeit studies reuse of cut reinforced-concrete elements from the Rathaus Ahlen case.
The work identifies valuable spatial fragments:
- Stützen vor Fenstern
- Nische hinter Stütze
- Große Stütze in kleinem Raum

The final project uses many cut concrete parts.
The elements rest on a semi-precast reinforced-concrete beam.
A post-installed reinforcement connection makes the used parts and new beam force-locked.
```

**Note:**  
`SlabBeamColumnFragment` is a system example derived from this fragment logic.  
It is not presented as a named object in the source. It is a proposed typology for the new system: a monolithic concrete fragment composed of slab, integrated beam, and column section.

### ReCreate

Used for the third example in each package.

Sources:

```text
ReCreate Netherlands:
https://recreate-project.eu/project-pilots/the-netherlands/

ReCreate Finland:
https://recreate-project.eu/project-pilots/finland/
```

Important source facts used:

```text
ReCreate Netherlands:
- donor building Prinsenhof, Arnhem
- structure mainly hollow-core slabs spanning from load-bearing facade to load-bearing facade
- hollow-core slabs and load-bearing facade elements
- wet connections
- floor sawing at longitudinal joints
- hoisting and transport to Lagemaat site
- mock-up planned to test dimensional tolerance and reconnecting reclaimed elements

ReCreate Finland:
- donor building in Tampere
- elements include columns, beams, hollow-core slabs, sandwich facade elements
- BIM inventory
- coding system for tracing
- disconnection of joints
- QR codes before transport to storage
- testing with non-destructive, semi-destructive, and destructive methods
- recalculation according to current structural design code
```

---

# 1. Core System Rule

## 1.1 Minimal Abstraction Rule

```text
Do not model everything.

Model only what is needed for:
connection
calculation
warning
compatibility
design decision
```

## 1.2 Representation, Property, Connector, Port

```text
Representation
= simplified model of a component for one package.

Property
= information describing the representation.

Connector
= placed actionable handle on a representation.

Port
= semantic compatibility type referenced by a connector.
```

## 1.3 Connector Rule

```text
No connector just because a face exists.
No connector just because an edge exists.
No connector just because a value exists.

Create a connector only if the system will use it for a rule,
connection, warning, calculation, or design operation.
```

## 1.4 Port Rule

```text
Ports do not contain geometry.
Ports define compatibility.

A connector has geometry.
A connector references a port.
A rule checks two compatible ports through connector geometry.
```

---

# 2. Package Overview

The system uses seven packages.

```text
0. Base Geometry
1. Structural
2. Energy / Envelope
3. TGA / Openings
4. Semantic / Architectural
5. Logistics / Assembly
6. Evidence Overlay
```

## 2.1 Minimal Responsibility Table

| Package | Representation | Minimal connectors? | Ports? | Main use |
|---|---|---:|---:|---|
| **0. Base Geometry** | neutral geometric body | no | no | source geometry |
| **1. Structural** | force-transfer model | yes | yes | bearing, support, anchor, continuity |
| **2. Energy / Envelope** | thermal / envelope model | only where actionable | yes | continuity, sealing, bridge warnings |
| **3. TGA / Openings** | service / opening model | yes | yes | routes, penetrations, blocked zones |
| **4. Semantic / Architectural** | design-handle model | only when actionable | yes | alignment, visibility, access, spatial meaning |
| **5. Logistics / Assembly** | handling model | yes | yes | lifting, storage, transport, access |
| **6. Evidence Overlay** | evidence location model | no | no | modifies other connectors |

---

# 3. Global Minimal Connector Vocabulary

The vocabulary below is intentionally small.

## 3.1 Structural

```text
bearing_support
joint_connection
anchor_connection
continuity_connection
support_transfer
```

Ports:

```text
bearing_side
support_side
member_side
anchor_side
continuity_side
transfer_side
```

## 3.2 Energy / Envelope

```text
thermal_continuity
insulation_continuity
penetration_sealing
thermal_bridge_warning
```

Ports:

```text
thermal_side
insulation_side
penetration_side
bridge_side
```

## 3.3 TGA / Openings

```text
route_continuity
opening_use
drilling_candidate
blocked_conflict
```

Ports:

```text
route_side
opening_side
drilling_side
blocked_side
```

## 3.4 Semantic / Architectural

```text
access_handle
attachment_handle
stack_handle
side_handle
opening_handle
alignment_handle
visibility_constraint_handle
```

Ports:

```text
access_port
attachment_port
top_port
bottom_port
side_port
opening_port
alignment_port
visibility_port
```

## 3.5 Logistics / Assembly

```text
lifting_handle
storage_handle
transport_handle
access_handle
protection_handle
temporary_bracing_handle
```

Ports:

```text
lifting_port
storage_port
transport_port
access_port
protection_port
temporary_bracing_port
```

## 3.6 Evidence Overlay

```text
no connectors
no ports
```

Evidence modifies other connectors.

---

# 4. Package 0 — Base Geometry

## 4.1 Package Purpose

```text
The Base Geometry package stores the neutral geometric abstraction of the component.
It does not assign structural, energy, semantic, TGA, logistics, or evidence meaning.
```

## 4.2 Representation

```text
real component → simplified geometric body
```

## 4.3 Minimal Properties

```text
component_typology
geometry_source
unit
local_axes
bounding_box
length
width
height_or_thickness
volume
main_faces
main_edges
raw_openings
center_of_geometry
geometry_confidence
```

## 4.4 Connectors

```text
none
```

## 4.5 Ports

```text
none
```

## 4.6 Rules / Checks

```text
geometry_exists
units_valid
dimensions_extractable
volume_extractable
orientation_extractable_or_unknown
```

## 4.7 What Must Stay Outside This Package

```text
bearing meaning
service meaning
thermal meaning
visible meaning
lifting meaning
damage meaning
```

---

## 4.8 Example 1 — Abbau/Aufbau DE_1OG_001 Slab

```yaml
component:
  id: DE_1OG_001
  typology: slab
  material: reinforced_concrete

package:
  name: base_geometry

representation:
  kind: simplified_geometric_body
  properties:
    length: 4500_mm
    width: 2300_mm
    thickness: 180_mm
    volume: 1.863_m3
    mass_from_catalogue: 4.1_t
    main_faces:
      - top_face
      - bottom_face
      - side_faces
    main_edges:
      - long_edges
      - short_edges
    raw_openings: none_recorded_or_unknown
    geometry_confidence: catalogue_based

connectors: []
ports: []
```

---

## 4.9 Example 2 — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment
  material: reinforced_concrete
  source_logic: Abbau/Aufbau Masterarbeit 2020 fragment logic

package:
  name: base_geometry

representation:
  kind: monolithic_fragment_body
  properties:
    sub_geometries:
      - slab_plate_region
      - integrated_beam_region
      - column_section_region
    bounding_box: extracted_from_model
    volume: extracted_from_model
    raw_faces:
      - slab_top_candidate
      - slab_bottom_candidate
      - beam_side_faces
      - column_side_faces
      - cut_faces
    raw_edges:
      - cut_edges
      - beam_edges
      - slab_edges
      - column_edges
    geometry_confidence: model_or_scan_dependent

connectors: []
ports: []
```

**Important:**  
The fragment is monolithic. The base package stores the continuous geometric body, not three separate components.

---

## 4.10 Example 3 — ReCreate Hollow-Core Slab

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab
  material: precast_reinforced_concrete
  source: ReCreate Netherlands / Finland pilot logic

package:
  name: base_geometry

representation:
  kind: simplified_precast_slab_body
  properties:
    length: from_inventory_or_scan
    width: from_inventory_or_scan
    thickness: from_inventory_or_scan
    hollow_core_voids: raw_voids
    longitudinal_edges: detected
    end_faces: detected
    volume: net_volume_from_geometry
    geometry_confidence: inventory_or_scan_based

connectors: []
ports: []
```

---

# 5. Package 1 — Structural

## 5.1 Package Purpose

```text
The Structural package represents the component only as much as needed for force transfer,
support, anchoring, continuity, and structural warnings.
```

## 5.2 Representation Types

```text
2D_structural_plate
2D_structural_wall
1D_beam_member
1D_column_member
monolithic_structural_fragment
precast_hollow_core_slab_model
structural_support_graph
```

## 5.3 Minimal Properties

```text
structural_role
span_direction_status
support_condition_candidates
bearing_zone_status
capacity_status
reinforcement_evidence_status
minimum_bearing_length_rule
damage_relevance_status
structural_opening_status
```

## 5.4 Minimal Connectors

```text
bearing_support
joint_connection
anchor_connection
continuity_connection
support_transfer
```

## 5.5 Minimal Ports

```text
bearing_side
support_side
member_side
anchor_side
continuity_side
transfer_side
```

## 5.6 Minimal Rules / Checks

```text
bearing_side → support_side:
  overlap
  direction
  minimum_bearing_length

member_side → member_side:
  alignment
  continuity
  joint_geometry

anchor_side → support_side:
  edge_distance
  reinforcement_conflict
  anchor_feasibility
  capacity

continuity_side → continuity_side:
  reinforcement_continuity
  grout_or_cast_joint_geometry
  force_locking_requirement

transfer_side → bearing_side/support_side:
  transfer_path
  local_bearing
  intermediate_support_validity
```

## 5.7 What Must Stay Outside This Package

```text
final structural approval
exact load capacity if not proven
fire cover
LCA of connector material
architectural meaning
service routing
```

---

## 5.8 Example 1 — Abbau/Aufbau Wand–Decke / DE_1OG_001

Connection family from Abbau/Aufbau:

```text
Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter
```

```yaml
component:
  id: DE_1OG_001
  typology: slab

package:
  name: structural

representation:
  kind: 2D_structural_plate
  properties:
    structural_role: slab
    thickness: 180_mm
    span_direction_status: inferred_or_unknown
    capacity_status: engineering_required
    reinforcement_evidence_status: required_for_anchor_or_rebar_connection

  connectors:
    - id: DE_1OG_001.edge_A.bearing
      kind: bearing_support
      geometry: edge_bearing_strip
      port: bearing_side

    - id: DE_1OG_001.edge_A.anchor
      kind: anchor_connection
      geometry: edge_anchor_zone
      port: anchor_side

    - id: DE_1OG_001.edge_A.continuity
      kind: continuity_connection
      geometry: edge_grout_or_rebar_zone
      port: continuity_side

rules:
  bearing_support:
    compatible_with: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  anchor_connection:
    compatible_with: support_side
    checks:
      - edge_distance
      - reinforcement_conflict
      - anchor_feasibility

  continuity_connection:
    compatible_with: continuity_side
    checks:
      - reinforcement_continuity
      - grout_zone_geometry
      - force_locking_requirement
```

---

## 5.9 Example 2 — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: structural

representation:
  kind: monolithic_structural_fragment
  properties:
    structural_role:
      - slab_region
      - integrated_beam_region
      - column_section_region
    monolithic_status: true
    internal_force_path_status: engineering_required
    capacity_status: engineering_required
    cut_face_status: relevant

  connectors:
    - id: SBCF_001.slab_edge.bearing
      kind: bearing_support
      geometry: slab_edge_bearing_strip
      port: bearing_side

    - id: SBCF_001.beam_end.support_transfer
      kind: support_transfer
      geometry: beam_end_transfer_patch
      port: transfer_side

    - id: SBCF_001.column_base.support
      kind: bearing_support
      geometry: column_base_patch
      port: support_side

    - id: SBCF_001.cut_face.continuity
      kind: continuity_connection
      geometry: cut_face_rebar_or_grout_zone
      port: continuity_side

rules:
  support_transfer:
    compatible_with:
      - support_side
      - bearing_side
    checks:
      - transfer_path
      - local_bearing
      - alignment

  continuity_connection:
    compatible_with: continuity_side
    checks:
      - cut_face_geometry
      - reinforcement_evidence
      - force_locking_requirement
```

**Why this is minimal:**  
The fragment does not need separate connectors for every slab, beam, and column face. It needs only the handles where force can enter, leave, continue, or transfer.

---

## 5.10 Example 3 — ReCreate Hollow-Core Slab

ReCreate Netherlands describes hollow-core slabs spanning from load-bearing facade to load-bearing facade, wet connections, sawing at longitudinal joints, and later reconnection testing in a mock-up.

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: structural

representation:
  kind: precast_hollow_core_slab_model
  properties:
    structural_role: spanning_slab
    span_direction: along_hollow_core_axis
    longitudinal_joint_status: relevant
    wet_connection_history: likely_or_known
    capacity_status: requires_testing_or_recalculation

  connectors:
    - id: recreate_hcs_001.end_A.bearing
      kind: bearing_support
      geometry: end_bearing_strip
      port: bearing_side

    - id: recreate_hcs_001.end_B.bearing
      kind: bearing_support
      geometry: end_bearing_strip
      port: bearing_side

    - id: recreate_hcs_001.longitudinal_joint.member
      kind: joint_connection
      geometry: longitudinal_joint_edge
      port: member_side

rules:
  bearing_support:
    compatible_with: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  joint_connection:
    compatible_with: member_side
    checks:
      - longitudinal_alignment
      - tolerance
      - joint_reconnection_detail
```

---

# 6. Package 2 — Energy / Envelope

## 6.1 Package Purpose

```text
The Energy / Envelope package represents only the geometry and properties needed for
thermal continuity, insulation continuity, envelope penetration, and thermal bridge warnings.
```

## 6.2 Representation Types

```text
thermal_boundary_surface
insulation_continuity_model
envelope_penetration_model
thermal_bridge_risk_model
moisture_boundary_model
```

## 6.3 Minimal Properties

```text
thermal_role
inside_outside_status
area
thickness
lambda_status
U_value_status
insulation_status
moisture_risk_status
envelope_context_status
```

## 6.4 Minimal Connectors

```text
thermal_continuity
insulation_continuity
penetration_sealing
thermal_bridge_warning
```

## 6.5 Minimal Ports

```text
thermal_side
insulation_side
penetration_side
bridge_side
```

## 6.6 Minimal Rules / Checks

```text
thermal_side → thermal_side:
  thermal_boundary_continuity
  area_match
  layer_context

insulation_side → insulation_side:
  insulation_continuity
  gap_check

penetration_side → thermal_side/insulation_side:
  sealing_required
  air_tightness
  moisture_risk

bridge_side:
  single-sided warning connector
  thermal_bridge_risk
```

## 6.7 What Must Stay Outside This Package

```text
final U-value proof
final moisture proof
full energy certificate
structural fire resistance
architectural expression
```

---

## 6.8 Example 1 — Abbau/Aufbau 200 mm Reused Concrete Wall

Abbau/Aufbau uses a 200 mm reused reinforced-concrete wall in an exterior-wall example and discusses thermal conductivity / U-value logic.

```yaml
component:
  id: AA_wall_200
  typology: wall
  material: reinforced_concrete

package:
  name: energy_envelope

representation:
  kind: thermal_boundary_surface
  properties:
    thickness: 200_mm
    lambda_status: project_default_or_measured
    U_value_status: precheck_only
    envelope_context_status: exterior_wall
    insulation_status: required_by_assembly

  connectors:
    - id: AA_wall_200.outer.insulation
      kind: insulation_continuity
      geometry: outer_surface
      port: insulation_side

    - id: AA_wall_200.perimeter.thermal
      kind: thermal_continuity
      geometry: perimeter_edge_zone
      port: thermal_side

    - id: AA_wall_200.opening.seal
      kind: penetration_sealing
      geometry: opening_perimeter_if_present
      port: penetration_side

rules:
  insulation_continuity:
    checks:
      - gap_check
      - layer_continuity

  thermal_continuity:
    checks:
      - thermal_boundary_continuity

  penetration_sealing:
    checks:
      - air_tightness
      - moisture_risk
```

Calculation precheck:

```text
R_concrete = thickness / lambda
U_rough = 1 / (Rsi + R_concrete + Rse)
```

---

## 6.9 Example 2 — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: energy_envelope

representation:
  kind: thermal_bridge_risk_model
  properties:
    envelope_context_status: only_if_used_at_envelope
    monolithic_intersections: slab_beam_column_junctions
    U_value_status: not_applicable_until_envelope_role
    thermal_bridge_status: potential

  connectors:
    - id: SBCF_001.cut_face.thermal
      kind: thermal_continuity
      geometry: cut_face_boundary_if_envelope
      port: thermal_side

    - id: SBCF_001.junction.bridge
      kind: thermal_bridge_warning
      geometry: slab_beam_column_junction
      port: bridge_side

rules:
  thermal_bridge_warning:
    checks:
      - envelope_context
      - connector_or_junction_crosses_boundary
```

**Minimal logic:**  
The fragment gets no energy connectors unless it is used at an envelope boundary or has an envelope penetration.

---

## 6.10 Example 3 — ReCreate Hollow-Core Slab as Roof / Floor Boundary

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: energy_envelope

representation:
  kind: thermal_boundary_surface
  properties:
    envelope_context_status: context_required
    hollow_core_voids: relevant_for_thermal_model_if_used
    insulation_status: required_if_roof_or_exterior_floor

  connectors:
    - id: recreate_hcs_001.top.insulation
      kind: insulation_continuity
      geometry: top_surface_if_roof
      port: insulation_side

    - id: recreate_hcs_001.edge.bridge
      kind: thermal_bridge_warning
      geometry: slab_edge
      port: bridge_side

    - id: recreate_hcs_001.opening.seal
      kind: penetration_sealing
      geometry: penetration_perimeter_if_present
      port: penetration_side
```

---

# 7. Package 3 — TGA / Openings

## 7.1 Package Purpose

```text
The TGA / Openings package represents openings, voids, drilling candidates,
routes, blocked zones, and service continuity.
```

## 7.2 Representation Types

```text
opening_model
route_model
drilling_candidate_model
blocked_zone_model
service_penetration_model
```

## 7.3 Minimal Properties

```text
opening_size
opening_axis
opening_depth
route_diameter
edge_distance
clearance_status
drilling_status
blocked_status
relation_to_structural_zones
relation_to_rebar_status
```

## 7.4 Minimal Connectors

```text
route_continuity
opening_use
drilling_candidate
blocked_conflict
```

## 7.5 Minimal Ports

```text
route_side
opening_side
drilling_side
blocked_side
```

## 7.6 Minimal Rules / Checks

```text
route_side → route_side:
  route_alignment
  diameter_match
  clearance

opening_side → route_side:
  diameter_fits
  edge_distance
  route_continuity

drilling_side → route_side:
  diameter_fits
  rebar_conflict
  structural_zone_conflict
  edge_distance

blocked_side:
  conflicts_with_route_side
```

## 7.7 What Must Stay Outside This Package

```text
final service design
fire sealing proof
acoustic sealing proof
structural approval of new penetration
```

---

## 7.8 Example 1 — Abbau/Aufbau Existing Opening in Bauteilkatalog

```yaml
component:
  id: AA_wall_or_slab_001
  typology: slab_or_wall

package:
  name: tga_openings

representation:
  kind: opening_model
  properties:
    opening_size: from_catalogue_if_available
    edge_distance: calculated_from_geometry
    drilling_status: existing_opening
    relation_to_rebar_status: unknown_until_evidence

  connectors:
    - id: AA_001.opening.use
      kind: opening_use
      geometry: opening_boundary
      port: opening_side

rules:
  opening_use:
    compatible_with: route_side
    checks:
      - diameter_fits
      - edge_distance
      - structural_zone_conflict
```

---

## 7.9 Example 2 — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: tga_openings

representation:
  kind: blocked_zone_model
  properties:
    routing_status: difficult_due_to_monolithic_geometry
    blocked_zones:
      - column_section_region
      - beam_region
      - structural_transfer_region
    drilling_status: requires_rebar_scan

  connectors:
    - id: SBCF_001.slab_region.drilling
      kind: drilling_candidate
      geometry: slab_region_drilling_zone
      port: drilling_side

    - id: SBCF_001.beam_region.blocked
      kind: blocked_conflict
      geometry: beam_transfer_zone
      port: blocked_side

rules:
  drilling_candidate:
    compatible_with: route_side
    checks:
      - rebar_conflict
      - structural_zone_conflict
      - edge_distance

  blocked_conflict:
    checks:
      - route_conflict
```

---

## 7.10 Example 3 — ReCreate Hollow-Core Slab

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: tga_openings

representation:
  kind: route_model
  properties:
    hollow_core_voids: potential_service_or_void_geometry
    drilling_status: requires_structural_and_rebar_check
    longitudinal_void_axis: along_span

  connectors:
    - id: recreate_hcs_001.core.route
      kind: route_continuity
      geometry: hollow_core_axis_or_void
      port: route_side

    - id: recreate_hcs_001.new_drill.candidate
      kind: drilling_candidate
      geometry: proposed_drilling_zone
      port: drilling_side

rules:
  route_continuity:
    compatible_with: route_side
    checks:
      - route_alignment
      - continuity

  drilling_candidate:
    compatible_with: route_side
    checks:
      - structural_zone_conflict
      - rebar_conflict
      - diameter_fits
```

---

# 8. Package 4 — Semantic / Architectural

## 8.1 Package Purpose

```text
The Semantic / Architectural package represents only architectural design handles
that are actionable in the system.
```

## 8.2 Representation Types

```text
architectural_component_model
room_boundary_model
facade_relation_model
visibility_model
alignment_model
access_model
stacking_model
```

## 8.3 Minimal Properties

```text
architectural_role
spatial_role
visible_status
reuse_expression_status
surface_condition_status
grid_relation_status
room_relation_status
facade_relation_status
orientation_status
```

## 8.4 Minimal Connectors

```text
access_handle
attachment_handle
stack_handle
side_handle
opening_handle
alignment_handle
visibility_constraint_handle
```

## 8.5 Minimal Ports

```text
access_port
attachment_port
top_port
bottom_port
side_port
opening_port
alignment_port
visibility_port
```

## 8.6 Minimal Rules / Checks

```text
access_port → access_port:
  approach_alignment
  clearance

attachment_port → attachment_port:
  architectural_attachment_compatibility

top_port → bottom_port:
  stacking_direction
  vertical_alignment

side_port → side_port:
  side_alignment
  room_boundary_continuity

opening_port → opening_port/access_port:
  opening_alignment
  spatial_access

alignment_port → alignment_port:
  grid_alignment
  datum_alignment
  joint_alignment

visibility_port:
  single-sided visibility check
  obstruction
  surface_condition_warning
```

## 8.7 What Must Stay Outside This Package

```text
beauty judgment
final design intention
structural safety
energy compliance
fire compliance
```

---

## 8.8 Example 1 — Abbau/Aufbau DE_1OG_001 Slab

```yaml
component:
  id: DE_1OG_001
  typology: slab

package:
  name: semantic_architectural

representation:
  kind: architectural_component_model
  properties:
    architectural_role: reused_slab
    possible_roles:
      - floor_surface
      - ceiling_surface
      - roof_surface_if_context
    visible_status: context_required
    reuse_expression_status: surface_evidence_required
    grid_relation_status: module_candidate

  connectors:
    - id: DE_1OG_001.edge.joint_alignment
      kind: alignment_handle
      geometry: long_edge_line
      port: alignment_port

    - id: DE_1OG_001.bottom.visibility
      kind: visibility_constraint_handle
      geometry: bottom_surface
      port: visibility_port

rules:
  alignment_handle:
    compatible_with: alignment_port
    checks:
      - joint_alignment
      - grid_alignment

  visibility_constraint_handle:
    checks:
      - visibility_obstruction
      - surface_condition_warning
```

---

## 8.9 Example 2 — SlabBeamColumnFragment

The Masterarbeit 2020 fragment logic is architectural: valuable situations include columns before windows, niche behind column, and oversized column in a small room.

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: semantic_architectural

representation:
  kind: architectural_fragment_model
  properties:
    architectural_role: spatial_fragment
    spatial_qualities:
      - niche_behind_column_candidate
      - column_in_room_candidate
      - slab_beam_spatial_threshold
    reuse_expression_status: high_if_visible
    irregularity_status: design_relevant

  connectors:
    - id: SBCF_001.column_side.room_relation
      kind: side_handle
      geometry: column_side_surface
      port: side_port

    - id: SBCF_001.niche.access
      kind: access_handle
      geometry: niche_entry_zone
      port: access_port

    - id: SBCF_001.fragment_edge.alignment
      kind: alignment_handle
      geometry: cut_edge_or_beam_line
      port: alignment_port

    - id: SBCF_001.fragment.visibility
      kind: visibility_constraint_handle
      geometry: combined_visible_surfaces
      port: visibility_port

rules:
  side_handle:
    compatible_with: side_port
    checks:
      - room_boundary_continuity
      - side_alignment

  access_handle:
    compatible_with: access_port
    checks:
      - approach_alignment
      - clearance

  visibility_constraint_handle:
    checks:
      - visibility_obstruction
      - reuse_expression
```

---

## 8.10 Example 3 — ReCreate Hollow-Core Slab / Precast Elements

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: semantic_architectural

representation:
  kind: architectural_component_model
  properties:
    architectural_role: reused_precast_slab
    spatial_role: floor_or_roof_plate
    visible_status: context_required
    grid_relation_status: strong_due_to_precast_module
    reuse_expression_status: optional

  connectors:
    - id: recreate_hcs_001.longitudinal_joint.alignment
      kind: alignment_handle
      geometry: longitudinal_joint_line
      port: alignment_port

    - id: recreate_hcs_001.top.stack
      kind: stack_handle
      geometry: top_plane
      port: top_port

    - id: recreate_hcs_001.bottom.stack
      kind: stack_handle
      geometry: bottom_plane
      port: bottom_port

rules:
  alignment_handle:
    compatible_with: alignment_port
    checks:
      - module_alignment
      - joint_alignment

  stack_handle:
    compatible_with:
      - top_port
      - bottom_port
    checks:
      - vertical_alignment
      - level_offset
```

---

# 9. Package 5 — Logistics / Assembly

## 9.1 Package Purpose

```text
The Logistics / Assembly package represents only the handling model needed for
lifting, storage, transport, protection, access, and temporary assembly conditions.
```

## 9.2 Representation Types

```text
handling_model
transport_model
storage_model
lifting_model
assembly_access_model
temporary_bracing_model
protection_model
```

## 9.3 Minimal Properties

```text
mass
transport_dimensions
center_of_gravity_status
storage_orientation
lifting_status
access_status
protection_status
temporary_bracing_status
transport_status
```

## 9.4 Minimal Connectors

```text
lifting_handle
storage_handle
transport_handle
access_handle
protection_handle
temporary_bracing_handle
```

## 9.5 Minimal Ports

```text
lifting_port
storage_port
transport_port
access_port
protection_port
temporary_bracing_port
```

## 9.6 Minimal Rules / Checks

```text
lifting_handle:
  lifting_feasibility
  center_of_gravity
  crane_access
  lifting_proof_required

storage_handle:
  storage_orientation
  support_spacing
  separator_required
  stability

transport_handle:
  transport_envelope
  load_securing
  route_constraints

access_handle:
  installation_access
  connector_access

protection_handle:
  weather_protection
  edge_protection
  damage_sensitive_zone

temporary_bracing_handle:
  bracing_required
  access_clearance
  stability
```

## 9.7 What Must Stay Outside This Package

```text
final lifting proof
crane design
transport permit
complete site logistics plan
final assembly sequencing
```

---

## 9.8 Example 1 — Abbau/Aufbau DE_1OG_001 Slab

Abbau/Aufbau logistics guidance supports lying storage for slabs, protection, and timber separation.

```yaml
component:
  id: DE_1OG_001
  typology: slab

package:
  name: logistics_assembly

representation:
  kind: handling_model
  properties:
    mass: 4.1_t
    transport_dimensions: 4500_x_2300_x_180_mm
    storage_orientation: lying_recommended
    center_of_gravity_status: geometric_center_available
    lifting_status: evidence_required
    protection_status: required_if_outdoor_storage

  connectors:
    - id: DE_1OG_001.storage
      kind: storage_handle
      geometry: underside_support_zones
      port: storage_port

    - id: DE_1OG_001.transport
      kind: transport_handle
      geometry: transport_support_zones
      port: transport_port

    - id: DE_1OG_001.lifting
      kind: lifting_handle
      geometry: lifting_candidate_zones
      port: lifting_port

    - id: DE_1OG_001.protection
      kind: protection_handle
      geometry: edge_and_surface_protection_zones
      port: protection_port

rules:
  storage_handle:
    checks:
      - storage_orientation
      - separator_required

  lifting_handle:
    checks:
      - lifting_proof_required
      - center_of_gravity

  protection_handle:
    checks:
      - edge_protection
      - weather_protection
```

---

## 9.9 Example 2 — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: logistics_assembly

representation:
  kind: handling_model
  properties:
    mass: extracted_or_catalogued
    geometry_complexity: high
    center_of_gravity_status: must_be_calculated
    storage_orientation: custom_required
    lifting_status: engineering_required
    protection_status: required_for_cut_faces_and_column_edges
    temporary_bracing_status: possible

  connectors:
    - id: SBCF_001.lifting
      kind: lifting_handle
      geometry: balanced_lifting_candidate_zone
      port: lifting_port

    - id: SBCF_001.storage
      kind: storage_handle
      geometry: stable_storage_support_zones
      port: storage_port

    - id: SBCF_001.bracing
      kind: temporary_bracing_handle
      geometry: column_or_beam_bracing_zone
      port: temporary_bracing_port

    - id: SBCF_001.protection
      kind: protection_handle
      geometry: cut_face_and_edge_protection_zones
      port: protection_port

rules:
  lifting_handle:
    checks:
      - center_of_gravity
      - lifting_feasibility
      - crane_access

  temporary_bracing_handle:
    checks:
      - stability
      - assembly_access

  protection_handle:
    checks:
      - cut_face_protection
      - damage_sensitive_zone
```

---

## 9.10 Example 3 — ReCreate Hollow-Core Slab / Precast Elements

ReCreate Netherlands notes that hollow-core slabs were hoisted and transported after sawing; ReCreate Finland notes QR coding before transport to storage.

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: logistics_assembly

representation:
  kind: transport_and_lifting_model
  properties:
    mass: from_inventory_or_calculation
    transport_dimensions: from_inventory
    lifting_status: deconstruction_or_reuse_lift_required
    storage_status: storage_yard_or_factory
    tracing_status: qr_or_code_system_available

  connectors:
    - id: recreate_hcs_001.lifting
      kind: lifting_handle
      geometry: hoisting_candidate_zones
      port: lifting_port

    - id: recreate_hcs_001.transport
      kind: transport_handle
      geometry: transport_support_zones
      port: transport_port

    - id: recreate_hcs_001.storage
      kind: storage_handle
      geometry: storage_support_zones
      port: storage_port

rules:
  lifting_handle:
    checks:
      - lifting_feasibility
      - center_of_gravity
      - deconstruction_damage_risk

  transport_handle:
    checks:
      - load_securing
      - transport_envelope

  storage_handle:
    checks:
      - storage_orientation
      - support_spacing
```

---

# 10. Package 6 — Evidence Overlay

## 10.1 Package Purpose

```text
The Evidence Overlay package stores where evidence is located and how it affects connectors
from other packages.
```

Evidence does not create connectors.  
Evidence modifies connectors.

## 10.2 Representation Types

```text
scan_overlay
damage_overlay
test_point_overlay
photo_annotation_overlay
confidence_overlay
unknown_zone_overlay
```

## 10.3 Minimal Properties

```text
evidence_type
location
confidence
source
date
affected_package
affected_connector
affected_port
effect
reason
evidence_status
```

## 10.4 Connectors

```text
none
```

## 10.5 Ports

```text
none
```

## 10.6 Minimal Effects

```text
confirmed
warning
blocked
confidence_reduced
requires_manual_check
engineering_required
```

## 10.7 Minimal Rules / Checks

```text
if evidence overlaps connector:
  modify connector status

if unknown zone overlaps connector:
  mark connector as warning or blocked

if damage overlaps connector:
  mark connector as warning or requires manual check

if rebar scan clears anchor zone:
  allow anchor to proceed to engineering check

if test data confirms material property:
  update property confidence
```

---

## 10.8 Example 1 — Abbau/Aufbau Bewehrung / Material Evidence

```yaml
component:
  id: wall_001
  typology: wall

package:
  name: evidence_overlay

representation:
  kind: scan_overlay
  properties:
    evidence_type: reinforcement_scan
    confidence: partial
    affected_package: structural
    affected_connector: wall_001.top.anchor_receiver
    affected_port: support_side
    effect: warning_or_blocked
    reason: reinforcement_position_unknown_or_partial

connectors: []
ports: []

effect:
  if_unknown_rebar_zone_overlaps_anchor_connection:
    connector_status: blocked_or_warning
```

---

## 10.9 Example 2 — SlabBeamColumnFragment Damage / Cut Face Evidence

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment

package:
  name: evidence_overlay

representation:
  kind: damage_and_cut_face_overlay
  properties:
    evidence_type:
      - cut_face_record
      - damage_photo
      - rebar_scan_if_available
    confidence: evidence_dependent
    affected_connectors:
      - SBCF_001.cut_face.continuity
      - SBCF_001.beam_end.support_transfer
      - SBCF_001.column_base.support
    effect: requires_manual_check
    reason: monolithic_fragment_cut_faces_and_internal_rebar_unknown

connectors: []
ports: []

effect:
  if_cut_face_rebar_unknown:
    continuity_connection: engineering_required

  if_damage_overlaps_support_transfer:
    support_transfer: warning

  if_damage_overlaps_visibility_connector:
    visibility_constraint_handle: surface_condition_warning
```

---

## 10.10 Example 3 — ReCreate Testing / QR / Recalculation Evidence

ReCreate Finland used BIM inventory, a coding system for tracing, QR codes before storage, pre-deconstruction audit, structural survey, and testing.

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab

package:
  name: evidence_overlay

representation:
  kind: testing_and_tracking_overlay
  properties:
    evidence_type:
      - qr_tracking
      - bim_inventory
      - structural_survey
      - loading_test_if_available
    confidence: evidence_dependent
    affected_package:
      - structural
      - logistics_assembly
      - base_geometry
    affected_connectors:
      - recreate_hcs_001.end_A.bearing
      - recreate_hcs_001.end_B.bearing
      - recreate_hcs_001.lifting
    effect: confirmed_or_engineering_required
    reason: test_and_recalculation_status

connectors: []
ports: []

effect:
  if_loading_test_or_recalculation_available:
    structural_capacity_status: confidence_increased

  if_QR_code_available:
    traceability_status: confirmed

  if_joint_damage_unknown:
    joint_connection: requires_manual_check
```

---

# 11. Minimal Global Compatibility Rules

This global list should stay small.

```yaml
compatibility_rules:

  structural_bearing:
    from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  structural_anchor:
    from: anchor_side
    to: support_side
    checks:
      - edge_distance
      - reinforcement_conflict
      - anchor_feasibility
      - capacity

  structural_continuity:
    from: continuity_side
    to: continuity_side
    checks:
      - alignment
      - reinforcement_continuity
      - force_locking_requirement

  structural_transfer:
    from: transfer_side
    to:
      - support_side
      - bearing_side
    checks:
      - transfer_path
      - local_bearing
      - intermediate_support_validity

  energy_thermal:
    from: thermal_side
    to: thermal_side
    checks:
      - thermal_boundary_continuity

  energy_insulation:
    from: insulation_side
    to: insulation_side
    checks:
      - insulation_continuity
      - gap_check

  energy_penetration:
    from: penetration_side
    to:
      - thermal_side
      - insulation_side
    checks:
      - sealing_required
      - air_tightness
      - moisture_risk

  tga_route:
    from: route_side
    to: route_side
    checks:
      - route_alignment
      - clearance

  tga_opening:
    from: opening_side
    to: route_side
    checks:
      - diameter_fits
      - edge_distance
      - structural_zone_conflict

  tga_drilling:
    from: drilling_side
    to: route_side
    checks:
      - diameter_fits
      - rebar_conflict
      - structural_zone_conflict

  semantic_access:
    from: access_port
    to: access_port
    checks:
      - clearance
      - approach_alignment

  semantic_stack:
    from: top_port
    to: bottom_port
    checks:
      - vertical_alignment
      - level_offset

  semantic_alignment:
    from: alignment_port
    to: alignment_port
    checks:
      - grid_alignment
      - joint_alignment
      - datum_alignment

  logistics_lifting:
    from: lifting_port
    to: equipment_or_process_requirement
    checks:
      - lifting_feasibility
      - center_of_gravity
      - crane_access

  logistics_storage:
    from: storage_port
    to: storage_condition
    checks:
      - orientation
      - support_spacing
      - separator_required
```

---

# 12. Full Example Flow A — Abbau/Aufbau DE_1OG_001

```yaml
component:
  id: DE_1OG_001
  typology: slab
  material: reinforced_concrete
  source: Abbau/Aufbau Bauteilkatalog

catalogue:
  length: 4500_mm
  width: 2300_mm
  thickness: 180_mm
  volume: 1.863_m3
  mass: 4.1_t

packages:

  base_geometry:
    representation: simplified_geometric_body
    connectors: []
    ports: []

  structural:
    representation: 2D_structural_plate
    connectors:
      - bearing_support
      - anchor_connection
      - continuity_connection
    ports:
      - bearing_side
      - anchor_side
      - continuity_side

  energy_envelope:
    representation: thermal_boundary_surface_if_envelope
    connectors:
      - insulation_continuity
      - thermal_bridge_warning
      - penetration_sealing
    ports:
      - insulation_side
      - bridge_side
      - penetration_side

  tga_openings:
    representation: opening_model_if_opening_or_route_exists
    connectors:
      - opening_use
      - drilling_candidate
    ports:
      - opening_side
      - drilling_side

  semantic_architectural:
    representation: architectural_component_model
    connectors:
      - alignment_handle
      - visibility_constraint_handle
    ports:
      - alignment_port
      - visibility_port

  logistics_assembly:
    representation: handling_model
    connectors:
      - storage_handle
      - transport_handle
      - lifting_handle
      - protection_handle
    ports:
      - storage_port
      - transport_port
      - lifting_port
      - protection_port

  evidence_overlay:
    representation: evidence_overlay_if_available
    connectors: []
    ports: []
```

---

# 13. Full Example Flow B — SlabBeamColumnFragment

```yaml
component:
  id: SBCF_001
  typology: slab_beam_column_fragment
  material: reinforced_concrete
  source_logic: Abbau/Aufbau Masterarbeit 2020 spatial fragment logic

description:
  monolithic_fragment_composed_of:
    - slab_region
    - integrated_beam_region
    - column_section_region

packages:

  base_geometry:
    representation: monolithic_fragment_body
    connectors: []
    ports: []

  structural:
    representation: monolithic_structural_fragment
    connectors:
      - bearing_support
      - support_transfer
      - continuity_connection
    ports:
      - bearing_side
      - support_side
      - transfer_side
      - continuity_side

  energy_envelope:
    representation: thermal_bridge_risk_model_if_envelope
    connectors:
      - thermal_continuity
      - thermal_bridge_warning
    ports:
      - thermal_side
      - bridge_side

  tga_openings:
    representation: blocked_zone_and_drilling_model
    connectors:
      - drilling_candidate
      - blocked_conflict
    ports:
      - drilling_side
      - blocked_side

  semantic_architectural:
    representation: architectural_fragment_model
    connectors:
      - access_handle
      - side_handle
      - alignment_handle
      - visibility_constraint_handle
    ports:
      - access_port
      - side_port
      - alignment_port
      - visibility_port

  logistics_assembly:
    representation: handling_model
    connectors:
      - lifting_handle
      - storage_handle
      - protection_handle
      - temporary_bracing_handle
    ports:
      - lifting_port
      - storage_port
      - protection_port
      - temporary_bracing_port

  evidence_overlay:
    representation: cut_face_damage_rebar_overlay
    connectors: []
    ports: []
```

---

# 14. Full Example Flow C — ReCreate Hollow-Core Slab

```yaml
component:
  id: recreate_hcs_001
  typology: hollow_core_slab
  material: precast_reinforced_concrete
  source_logic: ReCreate Netherlands / Finland pilot

description:
  reused_precast_hollow_core_slab:
    source_facts:
      - hollow_core_slabs
      - wet_connections_or_joint_disconnection
      - hoisting_and_transport
      - BIM_inventory_or_QR_tracing
      - structural_testing_or_recalculation

packages:

  base_geometry:
    representation: simplified_precast_slab_body
    connectors: []
    ports: []

  structural:
    representation: precast_hollow_core_slab_model
    connectors:
      - bearing_support
      - joint_connection
    ports:
      - bearing_side
      - member_side

  energy_envelope:
    representation: thermal_boundary_surface_if_roof_or_exterior_floor
    connectors:
      - insulation_continuity
      - thermal_bridge_warning
      - penetration_sealing
    ports:
      - insulation_side
      - bridge_side
      - penetration_side

  tga_openings:
    representation: hollow_core_route_or_drilling_model
    connectors:
      - route_continuity
      - drilling_candidate
    ports:
      - route_side
      - drilling_side

  semantic_architectural:
    representation: architectural_component_model
    connectors:
      - alignment_handle
      - stack_handle
    ports:
      - alignment_port
      - top_port
      - bottom_port

  logistics_assembly:
    representation: transport_and_lifting_model
    connectors:
      - lifting_handle
      - transport_handle
      - storage_handle
    ports:
      - lifting_port
      - transport_port
      - storage_port

  evidence_overlay:
    representation: tracking_testing_overlay
    connectors: []
    ports: []
```

---

# 15. Final Rule

```text
Keep connectors minimal.

Use a connector only when a representation needs an actionable handle.

Use a port only when compatibility needs to be defined.

Use properties for everything else.

Evidence does not create connectors.
Evidence modifies connector confidence, warning, or blocked status.
```

This gives the system enough abstraction to support:

```text
reuse design
connection checking
warning generation
compatibility reasoning
LCA and logistics prechecks
architectural design guidance
```

without over-modeling every face, edge, or detail.
