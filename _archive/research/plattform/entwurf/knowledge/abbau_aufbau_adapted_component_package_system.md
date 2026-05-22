# Abbau/Aufbau Component Package System  
## Representations, Properties, Connectors, Ports, Rules, and Examples

**Purpose**  
This document adapts the previous generator/package logic to the new system rule structure:

```text
Component
→ Package
→ Representation
→ Representation properties
→ Connectors
→ Ports
→ Rules / checks
```

The system does **not** store every detail of the real component.  
It stores only the minimum abstraction needed for:

```text
connection
calculation
warning
compatibility
design decision
```

**Project frame**  
The examples are adapted to the Abbau/Aufbau reuse logic for an already existing pool of reclaimed reinforced-concrete elements. The process starts from a **Bauteilpool / Bauteilkatalog**, not from Rückbau or Zuschnitt.

**Main correction**  
There is no generic connector package.  
Each package owns its own representation, properties, connectors, ports, and rules.

---

# 0. Source Basis

## 0.1 New System Rule Source

This document follows the uploaded `system_rules.md`.

Core principles from the new rules:

```text
A representation is a simplified model of a real component for one package.

A connector is a placed actionable handle on a representation.

A port is a semantic compatibility interface.

Properties describe the representation.

Rules check whether two compatible ports can actually work together using connector geometry.
```

## 0.2 Abbau/Aufbau Source Basis

The Abbau/Aufbau examples are based on:

```text
Abbau/Aufbau
Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden
2023
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf
```

Important Abbau/Aufbau content used here:

```text
Bauteilkatalog:
ID, Maße, Öffnungsmaße, Volumen, Masse, Elementtyp,
optional Skizze, Beton- und Bewehrungsuntersuchungen.

Example component:
DE_1OG_001
Deckenplatte
4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t

Connection families:
Fundament - Bodenplatte → Schraubanker
Bodenplatte - Wand → Edelstahldorne, Winkelverbinder
Bodenplatte - Stütze → Edelstahldorn, Winkelverbinder
Wand - Decke → nachträglicher Bewehrungsanschluss + Verguss, Schraubanker mit Flachstahlhalter
Stütze - Decke → Edelstahldorn, Winkelverbinder, Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger, Auflager auf Stahlträger

Energy / Bauphysik:
example with reused 200 mm reinforced-concrete wall,
lambda assumption around 2.3 W/mK in the example context,
U-value / insulation check depending on envelope build-up.

Logistics:
storage order follows later installation logic,
weather protection,
timber separators,
slabs stored lying,
walls and columns generally stored standing if structurally appropriate.
```

---

# 1. Core Logic

## 1.1 The System Model

```text
Component
│
├── Package
│   ├── Representation
│   ├── Representation properties
│   ├── Connectors
│   ├── Ports
│   ├── Rules / checks
│   └── Examples
```

## 1.2 What a Representation Is

A representation is a simplified model of a real component for one package.

It does **not** describe the whole component.  
It describes only what that package needs.

Example:

```text
The same reclaimed slab can have:

Base Geometry representation:
basic body, dimensions, faces, edges, volume

Structural representation:
2D structural plate, bearing strips, support handles

Energy representation:
thermal boundary surface, insulation continuity edges

TGA representation:
openings and possible service penetrations

Semantic representation:
floor surface, ceiling expression, visible reuse edge

Logistics representation:
handling model, transport envelope, storage supports

Evidence representation:
rebar scan overlay, damage overlay, test point overlay
```

## 1.3 What a Property Is

A property describes the representation.

It is not spatially actionable by itself.

Examples:

```text
material
thickness
mass
thermal side
surface condition
visible status
heritage value
blocked status
capacity status
evidence status
```

A property becomes a connector only if it becomes actionable.

Example:

```text
"front side" as description → property

"front entrance where another element connects" → connector
```

## 1.4 What a Connector Is

A connector is a placed actionable handle on a representation.

It exists only where the system needs to:

```text
connect
attach
stack
bear
align
continue
pass through
be lifted
be checked
create a warning
```

A connector defines:

```text
where the handle is
what geometry it uses
which direction it faces, if direction matters
what kind of relation it supports
which port it references
which checks may use it
```

## 1.5 What a Port Is

A port is the semantic compatibility interface referenced by a connector.

Ports do **not** carry geometry.

Many connectors can reference the same port type.

Example:

```text
Many slab bearing strips can reference bearing_side.
Many wall support strips can reference support_side.
Many route endpoints can reference route_side.
Many architectural entrances can reference access_port.
```

## 1.6 Correct Relationship

```text
Properties describe the representation.
Connectors locate usable handles.
Ports define compatibility meaning.
Rules check compatible ports through connector geometry.
```

---

# 2. Package Overview

The system uses seven packages:

```text
0. Base Geometry
1. Structural
2. Energy / Envelope
3. TGA / Openings
4. Semantic / Architectural
5. Logistics / Assembly
6. Evidence Overlay
```

## 2.1 Package Responsibility Table

| Package | Representation answers | Connectors only where |
|---|---|---|
| **0. Base Geometry** | What is the neutral geometric body? | No connectors by default |
| **1. Structural** | Where can force transfer, support, anchor, or continuity happen? | forces enter, leave, continue, or are restrained |
| **2. Energy / Envelope** | Where must heat, air, moisture, insulation, or envelope continuity be checked? | continuity, sealing, bridge, or penetration checks occur |
| **3. TGA / Openings** | Where can services pass, route, or conflict? | route starts, ends, passes through, or conflicts |
| **4. Semantic / Architectural** | Where does architectural meaning become actionable? | access, alignment, stacking, visibility, facade, or spatial operation is checked |
| **5. Logistics / Assembly** | Where can the component be lifted, stored, transported, protected, or assembled? | handling, support, clearance, protection, or access is checked |
| **6. Evidence Overlay** | Where is evidence located and what does it affect? | no connectors; evidence modifies other package connectors |

---

# 3. Connector Placement Rule

A connector should not be added only because a face, edge, or surface exists.

Place a connector only if that geometry becomes useful for:

```text
rule
connection
check
warning
calculation
design operation
compatibility
```

## 3.1 Possible Connector Geometry

```text
point
line
edge
strip
surface
opening boundary
route endpoint
local zone
```

## 3.2 Do Not Place Connectors

```text
on every edge
on every face
only because geometry exists
only to repeat a property
only to describe visual detail
where no rule or design operation uses them
```

A connector is not a label.  
A connector is an actionable interface.

---

# 4. Package 0 — Base Geometry

## Representation

```text
real component → simplified geometric body
```

The Base Geometry package is neutral.  
It is the geometric source for all other packages.

## Representation Properties

```text
dimensions
volume
main faces
main edges
raw openings
center point
basic orientation
bounding box
surface areas
geometry confidence
```

## Connectors

```text
none by default
```

## Ports

```text
none by default
```

## Rules

```text
Base Geometry does not define relations by itself.
A face, edge, point, or opening from Base Geometry becomes a connector only when another package gives it functional meaning.
```

Examples:

```text
base edge → structural bearing connector
base opening → TGA opening connector
base surface → energy boundary connector
base point → logistics lifting connector
```

## Example A — Abbau/Aufbau Deckenplatte DE_1OG_001

### Input

```text
component_id: DE_1OG_001
typology: slab / Deckenplatte
material: Stahlbeton
dimensions: 4500 × 2300 × 180 mm
volume: 1.863 m³
mass: ca. 4.1 t
```

### Base Geometry Representation

```yaml
representation:
  id: DE_1OG_001.base_geometry
  package: base_geometry
  kind: simplified_geometric_body

  properties:
    typology: slab
    length: 4500_mm
    width: 2300_mm
    thickness: 180_mm
    volume: 1.863_m3
    main_faces:
      - top_face
      - bottom_face
      - side_faces
    main_edges:
      - long_edges
      - short_edges
    raw_openings: unknown_or_empty
    center_point: geometric_center
    orientation: inferred_from_plate_geometry

  connectors: []
  ports: []
```

### Why No Connectors Here?

The slab has edges and faces, but Base Geometry does not yet know whether an edge is:

```text
bearing edge
thermal edge
visible edge
lifting edge
service edge
```

That meaning belongs to other packages.

---

## Example B — Abbau/Aufbau 200 mm Reused Wall for Envelope Example

### Input

```text
typology: wall / Scheibe
material: Stahlbeton
thickness: 200 mm
use case: reused exterior wall build-up
```

### Base Geometry Representation

```yaml
representation:
  id: wall_200mm.base_geometry
  package: base_geometry
  kind: simplified_geometric_body

  properties:
    typology: wall
    thickness: 200_mm
    main_faces:
      - broad_face_A
      - broad_face_B
    main_edges:
      - top_edge
      - bottom_edge
      - side_edges
    raw_openings: from_catalogue_if_available
    orientation: wall_panel_candidate

  connectors: []
  ports: []
```

---

# 5. Package 1 — Structural

## Representation

```text
real component → structural model
```

Examples:

```text
slab → 2D structural plate
wall → 2D structural wall
beam → 1D line member
column → 1D vertical member
mushroom column → vertical member with head / capital zone
fragment → structural graph or local structural zone
```

## Representation Properties

```text
structural role
span direction
section / thickness
material
support zones
capacity status
damage status
evidence status
minimum bearing length
structural opening status
load-path status
```

## Minimal Connectors

```text
bearing_support
joint_connection
anchor_connection
continuity_connection
edge_restraint
dowel_connection
grout_connection
steel_support_connection
```

## Ports

```text
bearing_side
support_side
member_side
anchor_side
continuity_side
dowel_side
grout_side
steel_support_side
restraint_side
```

## Rules

```text
bearing_side connects to support_side
member_side connects to member_side
anchor_side connects to support_side
continuity_side connects to continuity_side
dowel_side connects to support_side or bearing_side depending detail
grout_side connects to grout_side or continuity_side depending detail
steel_support_side connects to bearing_side or support_side
```

## Checks

```text
overlap
direction
minimum bearing length
capacity
edge distance
anchor feasibility
dowel feasibility
continuity
reinforcement conflict
damage conflict
local bearing
punching if point support is involved
```

## Placement Rule

Place structural connectors where forces:

```text
enter
leave
continue
are restrained
are anchored
are supported
```

Examples:

```text
beam end
column top
column base
slab bearing edge
wall support line
anchor zone
joint line
bearing patch
continuity zone
dowel zone
grout zone
steel support zone
```

---

## Example A — Abbau/Aufbau Wand–Decke

### Abbau/Aufbau Connection Families

```text
Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter
```

### Slab Structural Representation

```yaml
representation:
  id: DE_1OG_001.structural
  package: structural
  kind: 2D_structural_plate

  properties:
    structural_role: slab
    thickness: 180_mm
    material: reinforced_concrete
    span_direction: unknown_or_inferred
    capacity_status: engineering_required
    evidence_status: partial_or_unknown
    minimum_bearing_length: project_rule_required

  connectors:
    - id: DE_1OG_001.edge_long_A.bearing
      kind: bearing_support
      geometry: bearing_strip
      direction: downward
      port:
        role: bearing_side

    - id: DE_1OG_001.edge_long_A.anchor_candidate
      kind: anchor_connection
      geometry: local_anchor_zone
      direction: into_support
      port:
        role: anchor_side

    - id: DE_1OG_001.edge_long_A.grout_joint
      kind: grout_connection
      geometry: joint_strip
      direction: along_edge
      port:
        role: grout_side
```

### Wall Structural Representation

```yaml
representation:
  id: wall_001.structural
  package: structural
  kind: 2D_structural_wall

  properties:
    structural_role: wall_support
    material: reinforced_concrete
    support_status: engineering_required
    reinforcement_status: unknown_or_partial

  connectors:
    - id: wall_001.top.support
      kind: bearing_support
      geometry: support_strip
      direction: upward
      port:
        role: support_side

    - id: wall_001.top.anchor_receiver
      kind: anchor_connection
      geometry: local_anchor_receiver_zone
      direction: downward_or_into_wall
      port:
        role: support_side

    - id: wall_001.top.post_installed_rebar
      kind: continuity_connection
      geometry: rebar_connection_zone
      direction: vertical_or_edge_based
      port:
        role: continuity_side
```

### Compatibility

```yaml
compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  - from: anchor_side
    to: support_side
    checks:
      - edge_distance
      - reinforcement_conflict
      - anchor_feasibility
      - capacity

  - from: grout_side
    to: continuity_side
    checks:
      - joint_geometry
      - reinforcement_continuity
      - grout_zone_clearance
```

### System Interpretation

```text
The representations define possible structural handles.
The rule checker later decides if the active slab-wall connection is valid.

If reinforcement position is unknown:
anchor and drilling checks become warning or blocked.

If capacity is unknown:
structural proof is required.

If exposed steel is used:
fire package may add a fire-cover check.
```

---

## Example B — Abbau/Aufbau Stütze–Decke

### Abbau/Aufbau Connection Families

```text
Stütze - Decke
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder
→ nachträglicher Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
→ Auflager auf Stahlträger
```

### Column Structural Representation

```yaml
representation:
  id: column_001.structural
  package: structural
  kind: 1D_vertical_member

  properties:
    structural_role: vertical_support
    material: reinforced_concrete
    head_support_status: engineering_required
    capacity_status: unknown_or_documented

  connectors:
    - id: column_001.head.support
      kind: bearing_support
      geometry: point_or_patch_support_zone
      direction: upward
      port:
        role: support_side

    - id: column_001.head.dowel_candidate
      kind: dowel_connection
      geometry: local_dowel_zone
      direction: upward
      port:
        role: dowel_side

    - id: column_001.side.angle_connector
      kind: joint_connection
      geometry: side_connector_zone
      direction: lateral
      port:
        role: member_side
```

### Slab Structural Representation

```yaml
representation:
  id: slab_001.structural
  package: structural
  kind: 2D_structural_plate

  properties:
    structural_role: slab
    point_support_status: engineering_required
    punching_status: engineering_required

  connectors:
    - id: slab_001.point_support.column_head
      kind: bearing_support
      geometry: point_bearing_patch
      direction: downward
      port:
        role: bearing_side

    - id: slab_001.steel_beam_support_line
      kind: steel_support_connection
      geometry: line_support_zone
      direction: downward
      port:
        role: steel_support_side
```

### Compatibility

```yaml
compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - local_bearing
      - punching_check
      - direction

  - from: dowel_side
    to: bearing_side
    checks:
      - dowel_position
      - reinforcement_conflict
      - edge_distance
      - capacity

  - from: steel_support_side
    to: support_side
    checks:
      - line_support_overlap
      - steel_beam_capacity
      - fire_cover_requirement
```

---

# 6. Package 2 — Energy / Envelope

## Representation

```text
real component → thermal / envelope model
```

Examples:

```text
external wall → thermal boundary surface
roof slab → thermal boundary surface
window panel → transparent thermal element
service penetration → envelope interruption
insulation layer → insulation continuity model
```

## Representation Properties

```text
thermal side
area
thickness
lambda
U-value
assembly status
air-tightness status
moisture risk status
insulation status
thermal bridge status
```

## Minimal Connectors

```text
thermal_continuity
insulation_continuity
penetration_sealing
thermal_bridge_warning
air_tightness_joint
moisture_boundary_joint
```

## Ports

```text
thermal_side
insulation_side
penetration_side
envelope_side
bridge_side
air_tightness_side
moisture_side
```

## Rules

```text
thermal_side connects to thermal_side
insulation_side connects to insulation_side
penetration_side connects to envelope_side
bridge_side may be single-sided
air_tightness_side connects to air_tightness_side
moisture_side connects to moisture_side
```

## Checks

```text
thermal continuity
insulation continuity
air tightness
sealing requirement
thermal bridge risk
moisture risk
U-value precheck
assembly completeness
```

## Placement Rule

Place energy connectors where heat, air, moisture, or envelope continuity must be checked.

Examples:

```text
thermal boundary edge
insulation edge
window perimeter
door perimeter
service penetration
air-tightness joint
thermal bridge risk zone
roof build-up edge
ground-contact interface
```

---

## Example A — Abbau/Aufbau 200 mm Reused Concrete Wall as Exterior Wall

### Energy Representation

```yaml
representation:
  id: wall_200mm.energy
  package: energy_envelope
  kind: thermal_boundary_surface

  properties:
    material: reinforced_concrete
    thickness: 200_mm
    lambda: 2.3_W_per_mK_or_project_default
    thermal_side: interior_exterior_required
    assembly_status: incomplete_until_layers_defined
    U_value_status: precheck_only
    moisture_risk_status: context_required

  connectors:
    - id: wall_200mm.edge_left.thermal
      kind: thermal_continuity
      geometry: thermal_edge
      port:
        role: thermal_side

    - id: wall_200mm.outer_face.insulation
      kind: insulation_continuity
      geometry: insulation_interface_surface
      port:
        role: insulation_side

    - id: wall_200mm.opening_01.envelope
      kind: penetration_sealing
      geometry: opening_perimeter
      port:
        role: envelope_side
```

### System Calculation

```text
R_concrete = thickness / lambda
R_concrete = 0.20 / 2.3
R_concrete ≈ 0.087 m²K/W

U_rough = 1 / (Rsi + R_concrete + Rse)
```

### Meaning

```text
The energy representation does not prove GEG compliance.
It only creates the energy model needed for U-value precheck,
insulation continuity, air-tightness, and thermal bridge warnings.
```

---

## Example B — Abbau/Aufbau Reused Slab as Roof / Exterior Floor

### Energy Representation

```yaml
representation:
  id: DE_1OG_001.energy
  package: energy_envelope
  kind: thermal_boundary_surface

  properties:
    material: reinforced_concrete
    thickness: 180_mm
    lambda: project_default_or_measured
    thermal_use_case: roof_or_exterior_floor_if_selected
    U_value_status: context_required
    insulation_status: required_if_envelope

  connectors:
    - id: DE_1OG_001.top.roof_build_up
      kind: insulation_continuity
      geometry: top_surface
      port:
        role: insulation_side

    - id: DE_1OG_001.edge.thermal_bridge
      kind: thermal_bridge_warning
      geometry: slab_edge_zone
      port:
        role: bridge_side

    - id: DE_1OG_001.service_penetration.envelope
      kind: penetration_sealing
      geometry: opening_or_penetration_perimeter
      port:
        role: envelope_side
```

### Rules

```yaml
rules:
  - connector: DE_1OG_001.edge.thermal_bridge
    checks:
      - thermal_bridge_risk
      - insulation_continuity
      - air_tightness_if_envelope

  - connector: DE_1OG_001.service_penetration.envelope
    checks:
      - sealing_required
      - moisture_risk
      - air_tightness
```

---

# 7. Package 3 — TGA / Openings

## Representation

```text
real component → service route / opening model
```

Examples:

```text
wall opening → opening model
slab hole → vertical route opening
duct → route segment
pipe → route segment
blocked area → conflict zone
```

## Representation Properties

```text
opening size
opening type
route diameter
axis direction
edge distance
clearance
fire rating status
blocked status
drilling status
relation to structural zones
relation to reinforcement
```

## Minimal Connectors

```text
route_continuity
opening_use
core_drilling_use
blocked_conflict
service_penetration
```

## Ports

```text
route_side
opening_side
drilling_side
blocked_side
service_side
```

## Rules

```text
route_side connects to route_side
opening_side connects to route_side
drilling_side connects to route_side
blocked_side conflicts with route_side
service_side connects to service_side
```

## Checks

```text
diameter fits
edge distance
clearance
fire rating
blocked zone conflict
route continuity
reinforcement conflict
structural zone conflict
```

## Placement Rule

Place TGA connectors where a service route starts, ends, passes through, or conflicts.

Examples:

```text
duct endpoint
pipe endpoint
cable tray endpoint
wall opening
slab opening
drilling centerline
route crossing
blocked area
minimum clearance zone
```

---

## Example A — Abbau/Aufbau Existing Opening from Bauteilkatalog

### Opening Representation

```yaml
representation:
  id: slab_001.openings
  package: tga_openings
  kind: opening_model

  properties:
    opening_status: from_catalogue_if_available
    opening_size: from_opening_geometry_or_catalogue
    edge_distance: calculated_from_geometry
    drilling_status: unknown_until_rebar_checked
    relation_to_structural_zones: system_check_required

  connectors:
    - id: slab_001.opening_01
      kind: opening_use
      geometry: opening_boundary
      port:
        role: opening_side

    - id: slab_001.opening_01.service_candidate
      kind: service_penetration
      geometry: opening_axis_or_boundary
      direction: through_component
      port:
        role: service_side
```

### Compatibility

```yaml
compatibility:
  - from: opening_side
    to: route_side
    checks:
      - diameter_fits
      - clearance
      - fire_rating
      - structural_zone_conflict
```

---

## Example B — Core Drilling Candidate

### Core Drilling Representation

```yaml
representation:
  id: wall_001.core_drilling_model
  package: tga_openings
  kind: drilling_candidate_model

  properties:
    drilling_status: requires_rebar_evidence
    edge_distance: calculated
    blocked_status: depends_on_structural_and_rebar_zones

  connectors:
    - id: wall_001.core_candidate_01
      kind: core_drilling_use
      geometry: drilling_centerline_and_diameter
      direction: through_wall
      port:
        role: drilling_side

    - id: wall_001.blocked_zone_01
      kind: blocked_conflict
      geometry: blocked_area
      port:
        role: blocked_side
```

### Rules

```yaml
rules:
  - from: drilling_side
    to: route_side
    checks:
      - diameter_fits
      - edge_distance
      - reinforcement_conflict
      - structural_zone_conflict

  - from: blocked_side
    to: route_side
    checks:
      - conflict
```

---

# 8. Package 4 — Semantic / Architectural

## Representation

```text
real component → architectural role / design-handle model
```

This package describes what the component means in the design.

Most architectural meaning should stay as properties.  
Use connectors only when that meaning becomes a usable design handle.

## Representation Properties

```text
architectural role
spatial role
front / back
left / right
east / west / north / south
entrance side
view side
orientation
visible status
heritage value
surface condition
finish status
design intent
reuse expression value
grid relation
room relation
facade relation
```

## Minimal Connectors

```text
access_handle
attachment_handle
stack_handle
side_handle
core_position_handle
opening_handle
alignment_handle
visibility_constraint_handle
reuse_identity_handle
```

## Ports

```text
access_port
attachment_port
top_port
bottom_port
side_port
core_port
opening_port
alignment_port
visibility_port
reuse_identity_port
```

## Rules

```text
access_port connects to access_port
attachment_port connects to attachment_port
top_port connects to bottom_port
side_port connects to compatible side_port
core_port connects to compatible core or shaft handle
opening_port connects to compatible access or route handle
alignment_port connects to alignment_port
visibility_port may be single-sided
reuse_identity_port may be single-sided
```

## Checks

```text
access alignment
clearance
approach direction
attachment compatibility
stacking compatibility
orientation
side compatibility
opening alignment
grid alignment
joint alignment
visibility obstruction
reuse identity visibility
```

## Placement Rule

Place semantic / architectural connectors only where architectural meaning becomes actionable.

Examples:

```text
entrance zone
door zone
platform side
module attachment side
top stacking point
bottom stacking point
core center
opening center
alignment edge
joint line
visible reuse zone if visibility is checked
```

Do not create a connector only because something is visible, historic, named, categorized, or meaningful.

Example:

```text
heritage value → property

heritage surface that must not be covered → connector only if the system checks visibility or obstruction
```

---

## Example A — Abbau/Aufbau Deckenplatte as Floor / Ceiling Expression

### Semantic Representation

```yaml
representation:
  id: DE_1OG_001.semantic
  package: semantic_architectural
  kind: architectural_component

  properties:
    architectural_role: reused_slab
    possible_new_roles:
      - floor_surface
      - ceiling_surface
      - roof_surface_if_context
    visible_status: context_required
    reuse_expression_value: depends_on_surface_condition
    grid_relation: slab_module_candidate

  connectors:
    - id: DE_1OG_001.top.floor_surface
      kind: alignment_handle
      geometry: top_surface_reference
      port:
        role: alignment_port

    - id: DE_1OG_001.bottom.ceiling_visible
      kind: visibility_constraint_handle
      geometry: bottom_surface_reference
      port:
        role: visibility_port

    - id: DE_1OG_001.long_edge.joint_line
      kind: alignment_handle
      geometry: long_edge_line
      port:
        role: alignment_port

    - id: DE_1OG_001.id_mark.reuse_identity
      kind: reuse_identity_handle
      geometry: marking_location_if_available
      port:
        role: reuse_identity_port
```

### Rules

```yaml
rules:
  - connector: DE_1OG_001.long_edge.joint_line
    checks:
      - grid_alignment
      - joint_alignment

  - connector: DE_1OG_001.bottom.ceiling_visible
    checks:
      - visibility_obstruction
      - surface_condition_warning

  - connector: DE_1OG_001.id_mark.reuse_identity
    checks:
      - identity_visibility
      - marking_not_covered_if_required
```

---

## Example B — Abbau/Aufbau Reused Wall as Room / Facade Interface

### Semantic Representation

```yaml
representation:
  id: wall_001.semantic
  package: semantic_architectural
  kind: architectural_component

  properties:
    architectural_role: reused_wall_panel
    spatial_role:
      - room_boundary
      - facade_candidate_if_exterior
    visible_status: context_required
    surface_condition: evidence_required
    facade_rhythm_value: depends_on_repetition_and_alignment

  connectors:
    - id: wall_001.room_boundary
      kind: side_handle
      geometry: broad_face_reference
      direction: inward_or_contextual
      port:
        role: side_port

    - id: wall_001.facade_rhythm_edge
      kind: alignment_handle
      geometry: vertical_edge_line
      port:
        role: alignment_port

    - id: wall_001.visible_reuse_surface
      kind: visibility_constraint_handle
      geometry: selected_visible_surface
      port:
        role: visibility_port
```

### Rules

```yaml
rules:
  - connector: wall_001.facade_rhythm_edge
    checks:
      - vertical_alignment
      - facade_grid_alignment

  - connector: wall_001.room_boundary
    checks:
      - spatial_continuity
      - room_boundary_alignment

  - connector: wall_001.visible_reuse_surface
    checks:
      - visibility_obstruction
      - surface_condition_warning
```

---

# 9. Package 5 — Logistics / Assembly

## Representation

```text
real component → handling model
```

Examples:

```text
slab → lifting and transport body
beam → crane handling model
wall panel → storage model
fragile fragment → protected handling model
large element → access and clearance model
```

## Representation Properties

```text
mass
transport dimensions
center of gravity
storage orientation
lifting status
access clearance
protection zones
fragile zones
maximum tilt angle
transport status
storage status
assembly access status
```

## Minimal Connectors

```text
lifting_handle
storage_handle
transport_handle
access_handle
protection_handle
temporary_bracing_handle
stacking_handle
```

## Ports

```text
lifting_port
storage_port
transport_port
access_port
protection_port
temporary_bracing_port
stacking_port
```

## Rules

Logistics connectors may be single-sided.

They often check against:

```text
equipment
process constraints
site zones
access paths
storage conditions
transport limits
assembly sequence
```

## Checks

```text
lifting feasibility
transport stability
storage safety
access clearance
protection requirement
center of gravity
maximum tilt
temporary bracing
assembly access
```

## Placement Rule

Place logistics connectors where handling, transport, storage, or assembly constraints must be checked.

Examples:

```text
lifting point
lifting zone
crane hook zone
forklift support zone
transport support
storage bearing zone
assembly access zone
fragile edge
protected surface
center of gravity reference
temporary bracing point
```

---

## Example A — Abbau/Aufbau Slab Storage

Abbau/Aufbau recommends slabs be stored lying, protected, and separated with timber where needed.

### Logistics Representation

```yaml
representation:
  id: DE_1OG_001.logistics
  package: logistics_assembly
  kind: handling_model

  properties:
    mass: 4.1_t
    transport_dimensions: 4500_x_2300_x_180_mm
    storage_orientation: lying_recommended
    center_of_gravity: geometric_center
    lifting_status: evidence_required
    protection_status: required_if_outdoor_storage
    separator_status: required_for_stacking

  connectors:
    - id: DE_1OG_001.storage_supports
      kind: storage_handle
      geometry: underside_support_zones
      port:
        role: storage_port

    - id: DE_1OG_001.transport_supports
      kind: transport_handle
      geometry: transport_support_zones
      port:
        role: transport_port

    - id: DE_1OG_001.lifting_candidate
      kind: lifting_handle
      geometry: lifting_candidate_zones
      port:
        role: lifting_port

    - id: DE_1OG_001.protected_edges
      kind: protection_handle
      geometry: edge_protection_zones
      port:
        role: protection_port
```

### Rules

```yaml
rules:
  - connector: DE_1OG_001.storage_supports
    checks:
      - storage_orientation
      - support_spacing
      - separator_required

  - connector: DE_1OG_001.lifting_candidate
    checks:
      - lifting_proof_required
      - center_of_gravity
      - crane_access

  - connector: DE_1OG_001.protected_edges
    checks:
      - damage_protection
      - weather_protection
```

---

## Example B — Abbau/Aufbau Wall / Column Storage

Abbau/Aufbau notes that walls and columns generally need storage consistent with their structural behavior and should be protected and ordered for later installation.

### Logistics Representation

```yaml
representation:
  id: column_001.logistics
  package: logistics_assembly
  kind: handling_model

  properties:
    component_kind: column
    storage_orientation: standing_candidate
    mass: from_catalogue_or_calculation
    center_of_gravity: generated_or_measured
    lifting_status: evidence_required
    temporary_bracing_status: likely_required_if_standing

  connectors:
    - id: column_001.base.storage_support
      kind: storage_handle
      geometry: base_support_zone
      port:
        role: storage_port

    - id: column_001.bracing_interface
      kind: temporary_bracing_handle
      geometry: side_bracing_zone
      port:
        role: temporary_bracing_port

    - id: column_001.crane_pick
      kind: lifting_handle
      geometry: crane_pick_candidate_zone
      port:
        role: lifting_port

    - id: column_001.protection_zone
      kind: protection_handle
      geometry: damage_sensitive_edge_or_head_zone
      port:
        role: protection_port
```

### Rules

```yaml
rules:
  - connector: column_001.base.storage_support
    checks:
      - storage_stability
      - support_surface
      - maximum_tilt

  - connector: column_001.bracing_interface
    checks:
      - temporary_bracing_required
      - access_clearance

  - connector: column_001.crane_pick
    checks:
      - lifting_feasibility
      - center_of_gravity
      - crane_access
```

---

# 10. Package 6 — Evidence Overlay

## Representation

```text
evidence → overlay model
```

Examples:

```text
scan result → evidence location model
photo annotation → evidence marker model
inspection note → confidence overlay
rebar uncertainty → blocked or warning zone
damage observation → risk overlay
```

## Representation Properties

```text
evidence type
location
confidence
affected connector
affected port
effect
reason
source
date
evidence status
```

## Connectors

```text
none
```

## Ports

```text
none
```

Evidence does not create connectors.  
Evidence modifies connectors from other packages.

## Rules

Evidence can modify a connector by marking it as:

```text
confirmed
warning
blocked
confidence_reduced
requires_manual_check
```

Evidence should not create new relation logic.  
It should only confirm, weaken, block, or warn about existing connector logic.

---

## Example A — Bewehrungsscan / Unknown Rebar

Abbau/Aufbau emphasizes archive drawings, static calculations, formwork plans, reinforcement plans, and reinforcement detection if documentation is insufficient.

### Evidence Overlay

```yaml
representation:
  id: wall_001.evidence.rebar_scan
  package: evidence_overlay
  kind: scan_overlay

  properties:
    evidence_type: reinforcement_scan
    source: scan_or_archive_plan
    confidence: medium
    affected_connector: wall_001.top.anchor_receiver
    affected_port: support_side
    effect: warning_or_blocked
    reason: reinforcement_position_unknown_or_partial

  connectors: []
  ports: []
```

### Effect

```yaml
evidence_effect:
  affected_connector: wall_001.top.anchor_receiver
  affected_port: support_side
  effect: blocked
  reason: unknown_rebar
  confidence: medium
```

### System Use

```text
If anchor zone intersects unknown rebar zone:
anchor connection is blocked or warning.

If rebar scan confirms clear zone:
anchor connection can proceed to engineering check.
```

---

## Example B — Carbonation / Core Sample Point

Abbau/Aufbau discusses material investigation such as carbonation testing and concrete assessment.

### Evidence Overlay

```yaml
representation:
  id: wall_001.evidence.carbonation_test
  package: evidence_overlay
  kind: test_point_overlay

  properties:
    evidence_type: carbonation_test
    source: core_sample_or_surface_test
    location: mapped_test_point
    confidence: high_if_lab_report_exists
    affected_connectors:
      - wall_001.outer_face.insulation
      - wall_001.top.support
    effect: warning_or_confirmed
    reason: durability_relevance

  connectors: []
  ports: []
```

### Effect

```yaml
evidence_effect:
  affected_connector: wall_001.top.support
  effect: confidence_reduced
  reason: carbonation_depth_close_to_cover
  confidence: high
```

### System Use

```text
If carbonation depth reaches cover:
durability warning.

If chloride content is unknown:
chloride test warning if exposure context requires it.

If damage overlaps a bearing connector:
structural connector gets warning or manual-check status.
```

---

# 11. Global Compatibility Rules

Compatibility belongs to **ports**.

Connector geometry is used to check whether the compatible ports can actually connect.

```yaml
compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  - from: member_side
    to: member_side
    checks:
      - alignment
      - continuity
      - connection_detail

  - from: anchor_side
    to: support_side
    checks:
      - edge_distance
      - reinforcement_conflict
      - anchor_feasibility
      - capacity

  - from: route_side
    to: opening_side
    checks:
      - diameter_fits
      - edge_distance
      - fire_rating
      - route_continuity

  - from: drilling_side
    to: route_side
    checks:
      - diameter_fits
      - edge_distance
      - reinforcement_conflict
      - structural_zone_conflict

  - from: penetration_side
    to: envelope_side
    checks:
      - sealing_required
      - thermal_bridge_warning
      - air_tightness

  - from: access_port
    to: access_port
    checks:
      - alignment
      - clearance
      - approach_direction

  - from: top_port
    to: bottom_port
    checks:
      - vertical_alignment
      - stacking_direction
      - level_offset

  - from: alignment_port
    to: alignment_port
    checks:
      - grid_alignment
      - joint_alignment
      - datum_alignment

  - from: lifting_port
    to: equipment_or_process_requirement
    checks:
      - lifting_feasibility
      - center_of_gravity
      - crane_access

  - from: storage_port
    to: storage_condition
    checks:
      - orientation
      - support_spacing
      - separator_required
```

---

# 12. Complete Abbau/Aufbau Example Flow A — Deckenplatte DE_1OG_001

## 12.1 Minimal Input

```yaml
component:
  id: DE_1OG_001
  typology: slab
  material: reinforced_concrete

catalogue_data:
  length: 4500_mm
  width: 2300_mm
  thickness: 180_mm
  volume: 1.863_m3
  mass: 4.1_t
```

## 12.2 Package Representations

```text
Base Geometry:
real slab → simplified geometric body

Structural:
slab → 2D structural plate

Energy / Envelope:
slab → thermal boundary surface if used as roof / exterior floor

TGA / Openings:
slab → opening / vertical route model if openings exist or drilling is requested

Semantic / Architectural:
slab → floor / ceiling / visible reuse design-handle model

Logistics / Assembly:
slab → handling model

Evidence Overlay:
scan / photo / inspection → evidence overlay
```

## 12.3 Minimal Connectors

```text
Structural:
slab-edge-bearing
anchor candidate at support edge
grout joint candidate if wall/slab connection

Energy:
roof-build-up interface if used as roof
thermal bridge warning edge
penetration sealing if opening crosses envelope

TGA:
opening-use connector if opening exists
core-drilling candidate if service route is proposed

Semantic:
joint-line alignment handle
ceiling-visible handle if visibility is checked
reuse identity handle if ID/marking should remain visible

Logistics:
storage support handle
transport support handle
lifting candidate handle
protection handle

Evidence:
no connectors; modifies others
```

## 12.4 Readiness

```text
Ready:
base geometry
mass / volume
logistics precheck
basic structural geometry
semantic grid / joint potential

Requires evidence:
capacity
reinforcement
anchor feasibility
fire rating if exposed connector
final energy proof if envelope
full LCA if datasets incomplete
```

---

# 13. Complete Abbau/Aufbau Example Flow B — Wand–Decke Connection

## 13.1 Pair Type

```text
Component A: reused wall
Component B: reused slab
Pair: Wand - Decke
```

## 13.2 Abbau/Aufbau Connection Families

```text
Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter
```

## 13.3 Package-Level Connection Logic

### Structural Package

```yaml
wall_structural:
  connectors:
    - id: wall.top.support
      kind: bearing_support
      port:
        role: support_side

    - id: wall.top.anchor_receiver
      kind: anchor_connection
      port:
        role: support_side

slab_structural:
  connectors:
    - id: slab.edge.bearing
      kind: bearing_support
      port:
        role: bearing_side

    - id: slab.edge.anchor
      kind: anchor_connection
      port:
        role: anchor_side

compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  - from: anchor_side
    to: support_side
    checks:
      - edge_distance
      - reinforcement_conflict
      - anchor_feasibility
```

### Energy Package

If the connection is in the envelope:

```yaml
energy:
  connectors:
    - id: wall_slab_joint.thermal_bridge
      kind: thermal_bridge_warning
      port:
        role: bridge_side

    - id: wall_slab_joint.air_tightness
      kind: air_tightness_joint
      port:
        role: air_tightness_side

checks:
  - thermal_bridge_risk
  - air_tightness
  - insulation_continuity
```

### TGA / Openings Package

If services pass near the joint:

```yaml
tga:
  connectors:
    - id: slab.near_joint.service_penetration
      kind: service_penetration
      port:
        role: service_side

checks:
  - structural_zone_conflict
  - reinforcement_conflict
  - fire_rating
```

### Semantic / Architectural Package

```yaml
semantic:
  connectors:
    - id: wall_slab_joint.visible_line
      kind: alignment_handle
      port:
        role: alignment_port

    - id: wall_slab_joint.visible_reuse
      kind: visibility_constraint_handle
      port:
        role: visibility_port

checks:
  - joint_alignment
  - visibility_obstruction
  - reuse_expression
```

### Logistics / Assembly Package

```yaml
logistics:
  connectors:
    - id: slab.assembly_access_edge
      kind: access_handle
      port:
        role: access_port

    - id: wall.top.installation_access
      kind: access_handle
      port:
        role: access_port

checks:
  - assembly_access
  - installation_sequence
  - lifting_feasibility
```

### Evidence Overlay Package

```yaml
evidence_effect:
  affected_connector: wall.top.anchor_receiver
  affected_port: support_side
  effect: warning_or_blocked
  reason: reinforcement_position_unknown
```

## 13.4 Rule Checker Result Logic

```text
If bearing overlap is insufficient:
structural connection fails.

If reinforcement is unknown:
anchor / drilling is blocked or warning.

If connector uses exposed steel in fire-relevant area:
energy / fire-related warning.

If joint line is visible and misaligned:
semantic / architectural warning.

If assembly access is blocked:
logistics warning.

If evidence is incomplete:
connection passport records required evidence.
```

---

# 14. Final Principle

```text
Keep the abstraction small.

Representations own descriptive and calculable properties.
Connectors define placed actionable handles.
Ports define compatibility meaning.
Rules use connector geometry to check compatible ports.
Evidence modifies existing connector logic but does not create new ports.

Only model what is needed for:
- connection
- calculation
- warning
- compatibility
- design decision
```

This makes the Abbau/Aufbau system compatible with the new package model while keeping the concrete reuse-specific details.
