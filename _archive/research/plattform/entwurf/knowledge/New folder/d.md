Compact System Rules
Component Packages, Representations, Connectors, and Ports
1. Core Logic

Each reclaimed component is abstracted through package-specific representations.

Component
→ Package
→ Representation
→ Representation properties
→ Connectors
→ Semantic ports
→ Rules / checks

The system does not store every detail of the real component.
It stores only what is needed for:

connection
calculation
warning
compatibility
design decision
2. Main Concepts
Representation

A representation is a simplified model of the real component for one specific package.

Examples:

Structural package:
slab → 2D plate surface

Energy package:
wall → thermal boundary surface

TGA package:
wall opening → route / opening model

Semantic package:
wall → spatial boundary model

Logistics package:
slab → handling model

Evidence package:
scan / photo / inspection → overlay model

Each representation owns only the properties it needs.

Connector

A connector is a placed relation object.

It defines:

where a relation happens
what geometry is involved
which direction it faces
what kind of relation it supports
which semantic port it exposes
what checks are required

Connectors carry geometry and relation logic.

Port

A port is a semantic interface.

It defines:

the role of a connector
what it can connect to
which compatibility rules apply

Ports do not carry geometry.

Correct relation
Geometry belongs to connectors.
Meaning belongs to ports.
Properties belong to representations.
Rules connect compatible ports through connector geometry.

Example:

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
      port:
        role: bearing_side

compatibility:
  - from: bearing_side
    to: support_side
    checks:
      - overlap
      - direction
      - minimum_bearing_length
3. Package Structure

Each package follows the same structure:

Package
├── Representation
├── Representation properties
├── Connectors
├── Semantic ports
├── Rules
└── Examples

Packages:

0. Base Geometry
1. Structural
2. Energy / Envelope
3. TGA / Openings
4. Semantic / Architectural
5. Logistics / Assembly
6. Evidence Overlay
4. Package Rules
0. Base Geometry Package
Representation
real component → simplified geometric body
Representation properties
dimensions
volume
main faces
main edges
openings
center point
Connectors
none
Ports
none
Rule

Base Geometry is the neutral geometric source for all other packages.
It does not define relations by itself.

1. Structural Package
Representation
real component → structural model

Examples:

beam → 1D line element
column → 1D vertical line element
slab → 2D plate surface
wall → 2D wall surface
monolithic fragment → structural graph
Representation properties
role
span direction
section / thickness
material
support zones
capacity status
evidence status
Minimal connectors
bearing_support
joint_connection
anchor_connection
monolithic_continuity
Semantic ports
bearing_side
support_side
member_side
anchor_side
continuity_side
Example
representation:
  id: slab_structural_plate
  kind: 2D_plate_surface

  connectors:
    - id: slab.edge_left.bearing
      kind: bearing_support
      geometry: bearing_strip
      port:
        role: bearing_side
representation:
  id: wall_structural_support
  kind: 2D_wall_surface

  connectors:
    - id: wall.top.support
      kind: bearing_support
      geometry: support_strip
      port:
        role: support_side
Rules
bearing_side connects to support_side
member_side connects to member_side
anchor_side connects to support_side
continuity_side connects to continuity_side

Checks:

overlap
direction
minimum bearing length
capacity
edge distance
2. Energy / Envelope Package
Representation
real component → thermal boundary model

Examples:

external wall → thermal surface
roof slab → thermal boundary surface
window panel → transparent thermal boundary
service penetration → thermal opening / interruption
Representation properties
thermal side
area
thickness
lambda
U-value
assembly status
air-tightness status
moisture risk status
Minimal connectors
thermal_continuity
insulation_continuity
thermal_bridge_warning
penetration_sealing
Semantic ports
thermal_side
insulation_side
bridge_side
penetration_side
envelope_side
Example
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
representation:
  id: pipe_energy_penetration
  kind: penetration_object

  connectors:
    - id: pipe.penetration
      kind: penetration_sealing
      geometry: pipe_outer_boundary
      port:
        role: penetration_side
Rules
thermal_side connects to thermal_side
insulation_side connects to insulation_side
penetration_side connects to envelope_side
bridge_side may be a single-sided warning port

Checks:

thermal continuity
insulation continuity
air tightness
sealing requirement
thermal bridge risk
3. TGA / Openings Package
Representation
real component → service route / opening model

Examples:

wall with opening → opening model
slab with core hole → vertical route model
duct → service route model
blocked area → conflict zone
Representation properties
opening size
route diameter
axis direction
edge distance
clearance
fire rating status
blocked status
Minimal connectors
route_continuity
opening_use
core_drilling_use
blocked_conflict
Semantic ports
route_side
opening_side
drilling_side
blocked_side
Example
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
representation:
  id: duct_route_model
  kind: route_model

  connectors:
    - id: duct.route_start
      kind: route_continuity
      geometry: route_endpoint
      port:
        role: route_side
Rules
route_side connects to route_side
opening_side connects to route_side
drilling_side connects to route_side
blocked_side conflicts with route_side

Checks:

diameter fits
edge distance
clearance
fire rating
blocked zone conflict
4. Semantic / Architectural Package
Representation
real component → spatial / visual relation model

Examples:

wall panel → room boundary surface
floor panel → visible grid surface
facade element → visual identity surface
reuse fragment → heritage / identity zone
Representation properties
visible side
room side
joint line
grid direction
identity zone
surface condition status
heritage value
finish status
Minimal connectors
boundary_alignment
joint_alignment
grid_continuity
visibility_relation
Semantic ports
boundary_side
joint_side
grid_side
visible_side
observer_side
Example
representation:
  id: wall_semantic_boundary
  kind: spatial_boundary_model

  connectors:
    - id: wall.room_side
      kind: boundary_alignment
      geometry: boundary_surface
      port:
        role: boundary_side

    - id: wall.visible_face
      kind: visibility_relation
      geometry: visible_surface
      port:
        role: visible_side
representation:
  id: room_observer_model
  kind: viewpoint_model

  connectors:
    - id: room.main_viewpoint
      kind: visibility_relation
      geometry: observation_zone
      port:
        role: observer_side
Rules
boundary_side connects to boundary_side
joint_side connects to joint_side
grid_side connects to grid_side
visible_side connects to observer_side

Checks:

boundary alignment
joint alignment
grid continuity
visibility
identity / heritage expression
5. Logistics / Assembly Package
Representation
real component → handling model

Examples:

slab → lifting and transport body
beam → crane handling model
wall panel → storage and protection model
fragile fragment → protected handling model
Representation properties
mass
transport dimensions
center of gravity
storage orientation
lifting status
access clearance
protection zones
fragile zones
maximum tilt angle
Minimal connectors
lifting_check
storage_check
transport_check
access_check
protection_check
Semantic ports
lifting_side
storage_side
transport_side
access_side
protection_side
Example
representation:
  id: slab_logistics_model
  kind: handling_model

  connectors:
    - id: slab.lifting_points
      kind: lifting_check
      geometry: lifting_points
      port:
        role: lifting_side

    - id: slab.transport_supports
      kind: transport_check
      geometry: support_zones
      port:
        role: transport_side

    - id: slab.fragile_edge
      kind: protection_check
      geometry: protected_edge_zone
      port:
        role: protection_side
Rules

Logistics connectors may be single-sided.

They often check against:

equipment
process constraints
site zones
access paths
storage conditions
transport limits

Checks:

lifting feasibility
transport stability
storage safety
access clearance
protection requirement
6. Evidence Overlay Package
Representation
evidence → overlay model

Examples:

scan result → evidence location model
photo annotation → evidence marker model
inspection note → confidence overlay
rebar uncertainty → blocked or warning zone
Representation properties
evidence type
location
confidence
affected connector
affected port role
effect
reason
source
date
Connectors
none
Ports
none

Evidence does not create connectors.
It modifies connectors from other packages.

Example
evidence_effect:
  affected_connector: structural.anchor_connection.edge_left
  affected_port_role: anchor_side
  effect: blocked
  reason: unknown_rebar
  confidence: medium
Rules

Evidence can modify a connector by marking it as:

confirmed
warning
blocked
confidence_reduced
requires_manual_check

Evidence should not create new relation logic.
It should only confirm, weaken, block, or warn about existing connector logic.

5. Compatibility Rules

Compatibility belongs to semantic ports.

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
6. Final Template

Use this structure for every package:

Package name

Representation:
real thing → abstract model

Representation properties:
only values needed by this representation

Connectors:
minimum relation objects needed by this representation

Ports:
semantic interfaces referenced by connectors

Rules:
minimum checks

Examples:
how the component maps into the representation
7. Final Principle
Keep the abstraction small.

Representations own their properties.
Connectors contain geometry, location, direction, and relation logic.
Ports define semantic roles and compatibility interfaces.

Only model what is needed for:
- connection
- calculation
- warning
- compatibility
- design decision

The system should always reduce a real component to the simplest useful package-specific representation.