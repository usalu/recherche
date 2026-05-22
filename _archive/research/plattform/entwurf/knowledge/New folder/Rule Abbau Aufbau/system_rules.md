# System Rules

## Component Packages, Representations, Connectors, and Ports

## 1. Core Logic

Each reclaimed component is described through package-specific representations.

```text
Component
→ Package
→ Representation
→ Representation properties
→ Connectors
→ Ports
→ Rules / checks
```

The system does not store every detail of the real component.

It stores only the minimum abstraction needed for:

```text
connection
calculation
warning
compatibility
design decision
```

A representation describes the component for one purpose.

A connector marks a usable handle on that representation.

A port defines what kind of handle it is and what it can connect to.

A rule checks whether two compatible handles can actually work together.

---

## 2. Main Concepts

## Representation

A representation is a simplified model of a real component for one package.

It does not describe the whole object.
It describes only what that package needs.

Examples:

```text
Structural package:
slab → structural plate

Energy / Envelope package:
wall → thermal boundary

TGA / Openings package:
opening → route or penetration model

Semantic / Architectural package:
component → architectural role and design handles

Logistics / Assembly package:
component → handling model

Evidence Overlay package:
scan / photo / inspection → evidence overlay
```

Each representation owns its own properties.

Example:

```text
The same slab can have:

Structural properties:
thickness, material, span direction, support zones

Energy properties:
area, lambda, U-value, thermal side

Logistics properties:
mass, transport size, lifting points, center of gravity
```

---

## Connector

A connector is a placed handle on a representation.

It exists where the system needs to connect, place, align, support, pass through, lift, check, or warn.

A connector defines:

```text
where the handle is
what geometry it uses
which direction it faces, if direction matters
what kind of relation it supports
which port it references
which checks may use it
```

Connectors carry geometry, placement, direction, and relation logic.

A connector should not be added only because a face, edge, or surface exists.

A connector should be added only when that geometry becomes useful for a rule, connection, check, warning, or design operation.

---

## Port

A port is a semantic compatibility interface.

It defines:

```text
what kind of handle a connector exposes
what it can connect to
which compatibility rules apply
```

Ports do not carry geometry.

Ports are reusable.
Many connectors can reference the same kind of port.

Example:

```text
Several door connectors can reference the same access port.
Several bearing connectors can reference the same bearing-side port.
Several route endpoints can reference the same route-side port.
```

---

## Properties

Properties describe the representation.

They store information that is needed for decisions, calculation, filtering, or checking, but does not itself create a connection.

Examples:

```text
front
back
east
west
material
thickness
heritage value
visible status
surface condition
mass
thermal side
blocked status
```

A property should not become a connector unless it becomes spatially actionable.

Example:

```text
"front side" as description → property

"front entrance where another element connects" → connector
```

---

## Correct Relationship

```text
Properties describe the representation.
Connectors locate usable handles.
Ports define compatibility meaning.
Rules check compatible ports through connector geometry.
```

Example:

```yaml
representation:
  id: slab_structural_plate
  kind: 2D_plate_surface
  properties:
    thickness: 180_mm
    material: reinforced_concrete
    span_direction: unknown

  connectors:
    - id: slab.edge_left.bearing
      kind: bearing_support
      geometry: bearing_strip
      direction: outward
      port:
        role: bearing_side

compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length
```

---

## 3. Connector Placement Rule

Place connectors only at functional interface locations.

```text
A connector belongs where something can:

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

Use the smallest useful geometry for the connector.

Possible connector geometry:

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

Do not place connectors:

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

# 4. Package Structure

Each package follows the same structure:

```text
Package
├── Representation
├── Representation properties
├── Connectors
├── Ports
├── Rules
└── Examples
```

Packages:

```text
0. Base Geometry
1. Structural
2. Energy / Envelope
3. TGA / Openings
4. Semantic / Architectural
5. Logistics / Assembly
6. Evidence Overlay
```

---

# 5. Package Rules

## 0. Base Geometry Package

### Representation

```text
real component → simplified geometric body
```

### Representation properties

```text
dimensions
volume
main faces
main edges
openings
center point
basic orientation
```

### Connectors

```text
none by default
```

### Ports

```text
none by default
```

### Rule

Base Geometry is the neutral geometric source for all other packages.

It does not define relations by itself.

A face, edge, point, or opening from Base Geometry can become a connector only when another package gives it a functional meaning.

Examples:

```text
base edge → structural bearing connector
base opening → TGA opening connector
base surface → energy boundary connector
base point → logistics lifting connector
```

---

## 1. Structural Package

### Representation

```text
real component → structural model
```

Examples:

```text
beam → 1D structural member
column → 1D vertical member
slab → 2D structural plate
wall → 2D structural wall
fragment → structural graph or local structural zone
```

### Representation properties

```text
structural role
span direction
section / thickness
material
support zones
capacity status
damage status
evidence status
```

### Minimal connectors

```text
bearing_support
joint_connection
anchor_connection
continuity_connection
```

### Ports

```text
bearing_side
support_side
member_side
anchor_side
continuity_side
```

### Examples

```yaml
representation:
  id: slab_structural_plate
  kind: 2D_plate_surface

  connectors:
    - id: slab.edge_left.bearing
      kind: bearing_support
      geometry: bearing_strip
      direction: downward
      port:
        role: bearing_side
```

```yaml
representation:
  id: wall_structural_support
  kind: 2D_wall_surface

  connectors:
    - id: wall.top.support
      kind: bearing_support
      geometry: support_strip
      direction: upward
      port:
        role: support_side
```

```yaml
representation:
  id: beam_structural_member
  kind: 1D_line_member

  connectors:
    - id: beam.end_a
      kind: joint_connection
      geometry: endpoint
      port:
        role: member_side

    - id: beam.end_b
      kind: joint_connection
      geometry: endpoint
      port:
        role: member_side
```

### Rules

```text
bearing_side connects to support_side
member_side connects to member_side
anchor_side connects to support_side
continuity_side connects to continuity_side
```

Checks:

```text
overlap
direction
minimum bearing length
capacity
edge distance
anchor feasibility
continuity
```

### Placement rule

Place structural connectors where forces enter, leave, continue, or are restrained.

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
```

---

## 2. Energy / Envelope Package

### Representation

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

### Representation properties

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
```

### Minimal connectors

```text
thermal_continuity
insulation_continuity
penetration_sealing
thermal_bridge_warning
```

### Ports

```text
thermal_side
insulation_side
penetration_side
envelope_side
bridge_side
```

### Examples

```yaml
representation:
  id: wall_energy_boundary
  kind: thermal_boundary_surface

  connectors:
    - id: wall.edge_left.thermal
      kind: thermal_continuity
      geometry: thermal_edge
      port:
        role: thermal_side

    - id: wall.opening_01.envelope
      kind: penetration_sealing
      geometry: opening_perimeter
      port:
        role: envelope_side
```

```yaml
representation:
  id: pipe_energy_penetration
  kind: penetration_object

  connectors:
    - id: pipe.penetration
      kind: penetration_sealing
      geometry: pipe_outer_boundary
      port:
        role: penetration_side
```

### Rules

```text
thermal_side connects to thermal_side
insulation_side connects to insulation_side
penetration_side connects to envelope_side
bridge_side may be single-sided
```

Checks:

```text
thermal continuity
insulation continuity
air tightness
sealing requirement
thermal bridge risk
moisture risk
```

### Placement rule

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
```

---

## 3. TGA / Openings Package

### Representation

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

### Representation properties

```text
opening size
route diameter
axis direction
edge distance
clearance
fire rating status
blocked status
drilling status
```

### Minimal connectors

```text
route_continuity
opening_use
core_drilling_use
blocked_conflict
```

### Ports

```text
route_side
opening_side
drilling_side
blocked_side
```

### Examples

```yaml
representation:
  id: wall_opening_model
  kind: opening_model

  connectors:
    - id: wall.opening_01
      kind: opening_use
      geometry: opening_boundary
      port:
        role: opening_side

    - id: wall.blocked_zone_01
      kind: blocked_conflict
      geometry: blocked_area
      port:
        role: blocked_side
```

```yaml
representation:
  id: duct_route_model
  kind: route_model

  connectors:
    - id: duct.route_start
      kind: route_continuity
      geometry: route_endpoint
      direction: along_route
      port:
        role: route_side

    - id: duct.route_end
      kind: route_continuity
      geometry: route_endpoint
      direction: along_route
      port:
        role: route_side
```

### Rules

```text
route_side connects to route_side
opening_side connects to route_side
drilling_side connects to route_side
blocked_side conflicts with route_side
```

Checks:

```text
diameter fits
edge distance
clearance
fire rating
blocked zone conflict
route continuity
```

### Placement rule

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

## 4. Semantic / Architectural Package

### Representation

```text
real component → architectural role / design-handle model
```

This package describes what the component means in the design.

Most architectural meaning should remain as properties.

Use connectors only when that meaning becomes a usable design handle.

Examples:

```text
capsule → spatial module with entrance handle
core → circulation element with access handles
base → support element with core-position handles
bridge → platform element with side handles
facade element → element with attachment or alignment handles
reuse fragment → element with visibility or preservation constraints
```

### Representation properties

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
```

### Minimal connectors

```text
access_handle
attachment_handle
stack_handle
side_handle
core_position_handle
opening_handle
alignment_handle
```

### Ports

```text
access_port
attachment_port
top_port
bottom_port
side_port
core_port
opening_port
alignment_port
```

### Examples

```yaml
representation:
  id: capsule_architectural_model
  kind: architectural_component

  properties:
    architectural_role: residential_module
    entrance_side: back
    view_side: front

  connectors:
    - id: capsule.entrance
      kind: access_handle
      geometry: entrance_zone
      direction: outward
      port:
        role: access_port
```

```yaml
representation:
  id: core_architectural_model
  kind: architectural_component

  properties:
    architectural_role: circulation_core

  connectors:
    - id: core.platform_door
      kind: access_handle
      geometry: platform_door_zone
      direction: outward
      port:
        role: access_port
```

```yaml
representation:
  id: base_architectural_model
  kind: architectural_component

  properties:
    architectural_role: podium_base

  connectors:
    - id: base.core_position_east
      kind: core_position_handle
      geometry: core_center_point
      direction: upward
      port:
        role: core_port
```

```yaml
representation:
  id: bridge_architectural_model
  kind: architectural_component

  properties:
    architectural_role: platform_bridge

  connectors:
    - id: bridge.east_side
      kind: side_handle
      geometry: side_midpoint
      direction: east
      port:
        role: side_port

    - id: bridge.west_side
      kind: side_handle
      geometry: side_midpoint
      direction: west
      port:
        role: side_port
```

### Rules

```text
access_port connects to access_port
attachment_port connects to attachment_port
top_port connects to bottom_port
side_port connects to compatible side_port
core_port connects to compatible core or shaft handle
opening_port connects to compatible access or route handle
alignment_port connects to alignment_port
```

Checks:

```text
access alignment
clearance
approach direction
attachment compatibility
stacking compatibility
orientation
side compatibility
opening alignment
grid or joint alignment
```

### Placement rule

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
```

Do not create a connector only because something is visible, historic, named, categorized, or meaningful.

Those are properties unless they become part of a check or design operation.

Example:

```text
heritage value → property

heritage surface that must not be covered → connector only if the system checks visibility or obstruction
```

---

## 5. Logistics / Assembly Package

### Representation

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

### Representation properties

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
```

### Minimal connectors

```text
lifting_handle
storage_handle
transport_handle
access_handle
protection_handle
```

### Ports

```text
lifting_port
storage_port
transport_port
access_port
protection_port
```

### Examples

```yaml
representation:
  id: slab_logistics_model
  kind: handling_model

  connectors:
    - id: slab.lifting_points
      kind: lifting_handle
      geometry: lifting_points
      port:
        role: lifting_port

    - id: slab.transport_supports
      kind: transport_handle
      geometry: support_zones
      port:
        role: transport_port

    - id: slab.fragile_edge
      kind: protection_handle
      geometry: protected_edge_zone
      port:
        role: protection_port
```

### Rules

Logistics connectors may be single-sided.

They often check against:

```text
equipment
process constraints
site zones
access paths
storage conditions
transport limits
```

Checks:

```text
lifting feasibility
transport stability
storage safety
access clearance
protection requirement
center of gravity
maximum tilt
```

### Placement rule

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
```

---

## 6. Evidence Overlay Package

### Representation

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

### Representation properties

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
```

### Connectors

```text
none
```

### Ports

```text
none
```

Evidence does not create connectors.

Evidence modifies connectors from other packages.

### Example

```yaml
evidence_effect:
  affected_connector: structural.anchor_connection.edge_left
  affected_port: anchor_port
  effect: blocked
  reason: unknown_rebar
  confidence: medium
```

### Rules

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

# 6. Compatibility Rules

Compatibility belongs to ports.

Connector geometry is used to check whether the compatible ports can actually connect.

```yaml
compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length

  - from: route_side
    to: opening_side
    checks:
      - diameter_fits
      - edge_distance
      - fire_rating

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
```

---

# 7. Final Template

Use this structure for every package:

```text
Package name

Representation:
real thing → abstract model

Representation properties:
only values needed by this representation

Connectors:
minimum handles needed by this representation

Ports:
semantic compatibility interfaces referenced by connectors

Rules:
minimum checks

Examples:
how the component maps into the representation
```

---

# 8. Final Principle

```text
Keep the abstraction small.

Representations own descriptive and calculable properties.
Connectors define placed handles.
Ports define compatibility meaning.
Rules use connector geometry to check compatible ports.

Only model what is needed for:
- connection
- calculation
- warning
- compatibility
- design decision
```

The system should always reduce a real component to the simplest useful package-specific representation.
