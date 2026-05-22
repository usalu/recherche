# Minimal Component Abstraction Model
## Packages, Ports, Connectors, and Examples

**Goal**  
Keep the system as simple as a structural beam model:

```text
real component
↓
abstract package model
↓
minimal properties
↓
ports
↓
connectors / compatibility rules
↓
later calculation or rule check
```

The abstraction should not keep every geometric detail.  
It should keep only the geometry needed for a package to connect, compare, calculate, or warn.

---

# 1. Core Rule

Every package follows the same structure:

```text
Package
│
├── Abstract representation
│   └── point / line / surface / volume / graph
│
├── Minimal properties
│   └── values needed by this package
│
├── Ports
│   └── where this package can relate to another component
│
└── Connectors
    └── which port kinds can connect and what must be checked
```

In Semio terms, a port is the connector handle on a Type:

```text
Port / Semio Connector = ID + Point + Direction
```

For this reuse system, add only two more fields:

```text
kind
compatible_with
```

Minimal port:

```yaml
port:
  id: structural.bearing.edge_left
  kind: bearing
  point: [x, y, z]
  direction: [dx, dy, dz]
  compatible_with:
    - bearing
    - support
```

---

# 2. Universal Abstraction Types

Use only these abstraction types.

| Type | Meaning | Example |
|---|---|---|
| **Point** | 0D reference | node, lifting point, sample point |
| **Line** | 1D axis / edge / path | beam axis, joint line, route |
| **Surface** | 2D contact / boundary | wall face, slab face, bearing face |
| **Volume** | 3D body / envelope | component body, transport box |
| **Zone** | part of point / line / surface / volume | bearing strip, damage patch |
| **Graph** | nodes + edges + relations | structural model, service routes |

Important:

```text
Line support = line + narrow surface strip.
Point support = point + local surface patch.
```

Do not store a structural support as a mathematical line or point only.

---

# 3. Universal Port Structure

```yaml
port:
  id: string
  package: structural | energy | tga | semantic | logistics
  kind: string
  abstract_geometry: point | line | surface | zone | volume
  point: [x, y, z]
  direction: [dx, dy, dz]
  compatible_with: [port_kind]
  required_data: [string]
```

## Port placement rule

```text
A port is placed on the package abstraction,
not randomly on raw geometry.
```

Example:

```text
Beam structural abstraction = 1D line element.
Beam end port = point at line end + direction along beam axis.
```

---

# 4. Universal Connector Rule Structure

A connector is the rule that says which ports can connect and what must be checked.

```yaml
connector:
  id: string
  connects:
    from_port_kind: string
    to_port_kind: string
  required_geometry:
    - overlap
    - alignment
    - distance
  required_data:
    - evidence
    - material
    - capacity
  result:
    - valid
    - warning
    - blocked
```

Example:

```yaml
connector:
  id: bearing_support
  connects:
    from_port_kind: bearing
    to_port_kind: support
  required_geometry:
    - bearing_overlap
    - vertical_alignment
  required_data:
    - load_capacity
    - bearing_length
```

---

# 5. Package 0 — Base Geometry

## General abstraction

```text
Real component → simplified body model
```

## Abstract representation

| Real thing | Abstract model |
|---|---|
| Component body | volume |
| Main faces | surfaces |
| Main edges | lines |
| Openings | void volumes |
| Center | point |
| Dimensions | quantities |

## Minimal properties

```text
length
width
height / thickness
volume
main faces
main edges
center point
```

## Ports

```text
None.
```

Base Geometry creates no ports and no connectors.

## Example A — Abbau/Aufbau slab DE_1OG_001

```text
real slab
→ volume block
→ top surface
→ bottom surface
→ edge lines
→ dimensions: 4500 × 2300 × 180 mm
→ volume: 1.863 m³
```

## Example B — Wand–Decke

```text
real wall + real slab
→ two simplified volumes
→ wall top surface
→ slab edge surface
→ possible contact area
```

## Example C — SlabBeamColumnFragment

```text
real monolithic fragment
→ one composite volume
→ slab volume zone
→ beam volume zone
→ column-stub volume zone
→ cut faces
→ center point
```

---

# 6. Package 1 — Structural

## General abstraction

```text
Real component → structural model
```

## Abstract representation

| Real component | Structural abstraction |
|---|---|
| Beam | 1D line element + nodes |
| Column | 1D vertical line element + nodes |
| Slab | 2D plate surface + edge lines |
| Wall | 2D wall surface + top/bottom lines |
| Local bearing | point + local surface patch |
| Monolithic fragment | graph of lines/surfaces/volume continuity zones |

## Minimal properties

```text
structural role
span direction
support lines / support points
bearing zones
material
section or thickness
capacity status: known | unknown
evidence status
```

## Ports

| Port kind | Abstract geometry | Where |
|---|---|---|
| **bearing** | surface zone | where component bears on another |
| **support** | line+strip or point+patch | where component supports another |
| **joint** | point or line | where structural elements meet |
| **anchor** | point or surface zone | where anchor/drilling may occur |
| **dowel** | point array / line array | where dowels may occur |
| **grout** | gap volume | where filled joint may occur |
| **steel_support** | line or surface zone | where steel support can receive load |
| **continuity** | volume zone | internal monolithic continuity |

## Connector rules

| Connector | Compatible ports | Minimal checks |
|---|---|---|
| **bearing_support** | bearing ↔ support | overlap, direction, bearing length |
| **joint** | joint ↔ joint | node alignment, rotation constraint |
| **anchor_connection** | anchor ↔ anchor/support | edge distance, rebar evidence |
| **dowel_connection** | dowel ↔ dowel/support | alignment, depth, rebar evidence |
| **grout_connection** | grout ↔ bearing/support | gap volume, fillability |
| **steel_support** | bearing ↔ steel_support | contact area, local bearing |
| **monolithic_continuity** | continuity ↔ internal continuity | internal only, not an assembly connector |

## Calculation later

```text
abstract geometry + properties + connectors + loads
↓
structural calculation / rule check
```

## Example A — Abbau/Aufbau slab DE_1OG_001

```text
real slab
→ 2D plate surface
→ edge lines
→ bearing strips at usable edges
```

Ports:

```yaml
- id: structural.bearing.edge_left
  kind: bearing
  abstract_geometry: surface_zone
  point: midpoint_of_left_bearing_strip
  direction: outward_edge_normal
  compatible_with: [support, steel_support]

- id: structural.anchor.edge_left
  kind: anchor
  abstract_geometry: surface_zone
  point: anchor_zone_center
  direction: drilling_axis
  compatible_with: [anchor, support]
```

Possible connectors:

```text
bearing_support
anchor_connection
steel_support
```

Abbau/Aufbau mapping if connected to wall or support:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

---

## Example B — Wand–Decke

```text
wall
→ 2D vertical wall surface
→ wall top support line + strip

slab
→ 2D plate surface
→ slab edge bearing strip
```

Ports:

```yaml
wall:
  - id: structural.support.wall_top
    kind: support
    abstract_geometry: line_plus_surface_strip
    point: midpoint_of_wall_top
    direction: upward
    compatible_with: [bearing]

slab:
  - id: structural.bearing.slab_edge
    kind: bearing
    abstract_geometry: line_plus_surface_strip
    point: midpoint_of_slab_edge
    direction: downward_or_edge_normal
    compatible_with: [support]
```

Connector:

```yaml
connector:
  id: bearing_support
  connects: support ↔ bearing
  checks:
    - bearing_overlap
    - bearing_length
    - alignment
    - capacity_status
```

Abbau/Aufbau connector systems:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

---

## Example C — SlabBeamColumnFragment

```text
real fragment
→ one structural graph
```

Abstraction:

```text
slab zone = 2D plate surface
beam zone = 1D beam line + section
column stub = 1D column line + local node
slab-beam continuity = internal volume zone
beam-column continuity = internal volume zone
cut faces = risk surfaces
```

Ports:

```yaml
- id: structural.bearing.slab_edge_external
  kind: bearing
  abstract_geometry: line_plus_surface_strip
  point: midpoint_of_external_slab_edge
  direction: outward_edge_normal
  compatible_with: [support, steel_support]

- id: structural.bearing.beam_end
  kind: bearing
  abstract_geometry: surface_patch
  point: center_of_beam_cut_end
  direction: beam_axis
  compatible_with: [support, joint, steel_support]

- id: structural.continuity.slab_beam
  kind: continuity
  abstract_geometry: volume_zone
  point: centroid_of_slab_beam_junction
  direction: beam_axis
  compatible_with: []
```

Important:

```text
Internal continuity is not a connector to another component.
External ports connect to other components.
```

---

# 7. Package 2 — Energy / Envelope

## General abstraction

```text
Real component → thermal boundary model
```

## Abstract representation

| Real thing | Energy abstraction |
|---|---|
| Exterior wall/slab face | thermal surface |
| Insulation side | layer interface surface |
| Slab edge | thermal bridge line/zone |
| Penetration | opening through boundary |
| Ground/roof exposure | boundary surface |

## Minimal properties

```text
thermal boundary side
thickness
area
material lambda
exposure: interior | exterior | ground | roof
assembly status: known | unknown
```

## Ports

| Port kind | Abstract geometry | Where |
|---|---|---|
| **thermal_boundary** | surface | face separating thermal zones |
| **insulation** | surface | where insulation attaches |
| **thermal_bridge** | line or zone | edge/joint risk |
| **penetration** | opening zone | through envelope |
| **moisture** | surface/edge zone | exposed risk area |

## Connector rules

| Connector | Compatible ports | Minimal checks |
|---|---|---|
| **thermal_continuity** | thermal_boundary ↔ thermal_boundary | boundary alignment |
| **insulation_connection** | insulation ↔ insulation | layer continuity |
| **thermal_bridge_warning** | thermal_bridge ↔ thermal_bridge/connector | bridge risk |
| **envelope_penetration** | penetration ↔ service/connector | sealing required |
| **moisture_protection** | moisture ↔ exterior/ground/roof | exposure condition |

## Calculation later

```text
surface + thickness + material + layer connector
↓
rough U-value / thermal bridge warning
```

## Example A — DE_1OG_001 slab

If used inside:

```text
no active energy ports needed
```

If used as roof or exterior floor:

```yaml
- id: energy.thermal_boundary.top
  kind: thermal_boundary
  abstract_geometry: surface
  point: center_of_top_surface
  direction: exterior_normal
  compatible_with: [thermal_boundary]

- id: energy.thermal_bridge.edge_left
  kind: thermal_bridge
  abstract_geometry: line_zone
  point: midpoint_of_slab_edge
  direction: exterior_normal
  compatible_with: [thermal_bridge]
```

## Example B — Wand–Decke

```yaml
- id: energy.thermal_bridge.wall_slab_joint
  kind: thermal_bridge
  abstract_geometry: line_zone
  point: midpoint_of_joint
  direction: exterior_normal
  compatible_with: [thermal_bridge]

- id: energy.insulation.wall_face
  kind: insulation
  abstract_geometry: surface
  point: center_of_insulation_side
  direction: exterior_normal
  compatible_with: [insulation]
```

Connector:

```text
insulation_connection
thermal_bridge_warning
```

## Example C — SlabBeamColumnFragment

```yaml
- id: energy.thermal_bridge.beam_projection
  kind: thermal_bridge
  abstract_geometry: volume_or_line_zone
  point: centroid_of_beam_projection
  direction: exterior_normal
  compatible_with: [thermal_bridge]

- id: energy.moisture.cut_face
  kind: moisture
  abstract_geometry: surface_zone
  point: center_of_cut_face
  direction: cut_face_normal
  compatible_with: [moisture]
```

---

# 8. Package 3 — TGA / Openings

## General abstraction

```text
Real component → service route / opening model
```

## Abstract representation

| Real thing | TGA abstraction |
|---|---|
| Hole/opening | opening volume + centerline |
| Core drilling | cylindrical volume |
| Cable path | line/corridor |
| Pipe path | line/corridor volume |
| Shaft | volume interface |
| Blocked area | blocked zone |

## Minimal properties

```text
opening size
opening axis
edge distance
route diameter / width
blocked status
rebar status
```

## Ports

| Port kind | Abstract geometry | Where |
|---|---|---|
| **opening** | opening volume | existing opening |
| **core_drilling** | cylinder | possible new drilling |
| **cable_route** | line/corridor | cable path |
| **pipe_route** | line/corridor volume | pipe path |
| **shaft** | volume/surface | shaft connection |
| **blocked** | zone | do-not-use zone |

## Connector rules

| Connector | Compatible ports | Minimal checks |
|---|---|---|
| **opening_reuse** | opening ↔ pipe_route/cable_route | size, alignment |
| **core_drilling** | core_drilling ↔ route | rebar evidence, edge distance |
| **pipe_connection** | pipe_route ↔ pipe_route/opening | diameter, route continuity |
| **cable_connection** | cable_route ↔ cable_route/opening | corridor continuity |
| **blocked_conflict** | any TGA port ↔ blocked | warning/block |

## Example A — DE_1OG_001 slab

The given catalogue entry records no opening.

Possible generated candidate:

```yaml
- id: tga.core_drilling.candidate_01
  kind: core_drilling
  abstract_geometry: cylinder
  point: candidate_center
  direction: drilling_axis
  compatible_with: [pipe_route, cable_route]
```

Required:

```text
rebar evidence
edge distance
structural conflict check
```

## Example B — Wand–Decke

```yaml
- id: tga.cable_route.wall_top
  kind: cable_route
  abstract_geometry: line_corridor
  point: route_control_point
  direction: horizontal_route_direction
  compatible_with: [cable_route, opening]

- id: tga.blocked.bearing_joint
  kind: blocked
  abstract_geometry: zone
  point: center_of_bearing_joint
  direction: joint_normal
  compatible_with: []
```

## Example C — SlabBeamColumnFragment

```yaml
- id: tga.core_drilling.slab_zone
  kind: core_drilling
  abstract_geometry: cylinder
  point: safe_slab_zone_point
  direction: drilling_axis
  compatible_with: [pipe_route, cable_route]

- id: tga.blocked.beam_zone
  kind: blocked
  abstract_geometry: volume_zone
  point: center_of_beam_zone
  direction: beam_axis
  compatible_with: []
```

---

# 9. Package 4 — Semantic / Architectural

## General abstraction

```text
Real component → spatial / visual relation model
```

## Abstract representation

| Real thing | Semantic abstraction |
|---|---|
| Room face | boundary surface |
| Visible edge | expression line |
| Joint | joint line |
| Repetition | grid line / module |
| Cut face | reuse identity surface |
| Former structure | story / trace interface |

## Minimal properties

```text
visible side
room side
facade side
joint line
grid direction
identity surface
surface condition status
```

## Ports

| Port kind | Abstract geometry | Where |
|---|---|---|
| **room_boundary** | surface | creates/joins room boundary |
| **facade_rhythm** | line/surface interval | facade order |
| **visible_reuse** | surface/edge zone | visible reuse expression |
| **joint_line** | line | visible joint |
| **datum** | line/plane | alignment |
| **grid** | line/module | repetition |
| **identity** | surface zone | ID/reuse trace |

## Connector rules

| Connector | Compatible ports | Minimal checks |
|---|---|---|
| **room_boundary_alignment** | room_boundary ↔ room_boundary | coplanarity/alignment |
| **joint_expression** | joint_line ↔ joint_line | line continuity |
| **datum_alignment** | datum ↔ datum | alignment |
| **grid_continuity** | grid ↔ grid | spacing/direction |
| **visible_reuse_relation** | visible_reuse ↔ visible_reuse/identity | visibility preference |

## Example A — DE_1OG_001 slab

```yaml
- id: semantic.ceiling.bottom
  kind: visible_reuse
  abstract_geometry: surface
  point: center_of_bottom_face
  direction: downward_normal
  compatible_with: [visible_reuse]

- id: semantic.grid.width
  kind: grid
  abstract_geometry: line
  point: midpoint_of_reference_edge
  direction: grid_direction
  compatible_with: [grid]
```

## Example B — Wand–Decke

```yaml
- id: semantic.room_boundary.wall_face
  kind: room_boundary
  abstract_geometry: surface
  point: center_of_wall_face
  direction: room_side_normal
  compatible_with: [room_boundary]

- id: semantic.joint.wall_slab
  kind: joint_line
  abstract_geometry: line
  point: midpoint_of_joint
  direction: joint_direction
  compatible_with: [joint_line, datum]
```

## Example C — SlabBeamColumnFragment

```yaml
- id: semantic.visible_reuse.monolithic_junction
  kind: visible_reuse
  abstract_geometry: volume_zone_or_surface_zone
  point: centroid_of_visible_junction
  direction: viewing_normal
  compatible_with: [visible_reuse, identity]

- id: semantic.grid.original_bay
  kind: grid
  abstract_geometry: line
  point: original_bay_reference_point
  direction: original_grid_direction
  compatible_with: [grid]
```

---

# 10. Package 5 — Logistics / Assembly

## General abstraction

```text
Real component → handling model
```

## Abstract representation

| Real thing | Logistics abstraction |
|---|---|
| Whole object | transport envelope |
| Weight location | center point |
| Lifting place | point/zone |
| Storage face | support surface |
| Access need | clearance volume |
| Bracing place | line/surface zone |
| Fragile edge | protection zone |

## Minimal properties

```text
transport dimensions
mass
center of gravity
storage orientation
lifting status
access clearance
protection zones
```

## Ports

| Port kind | Abstract geometry | Where |
|---|---|---|
| **lifting** | point/surface zone | lifting location |
| **storage_support** | surface/line strip | storage support |
| **stacking** | surface zone | stacking contact |
| **transport_fixation** | point/edge zone | tie-down/fixation |
| **assembly_access** | clearance volume | required access |
| **temporary_bracing** | surface/line zone | temporary stability |
| **protection** | surface/edge zone | fragile area |

## Connector rules

| Connector | Compatible ports | Minimal checks |
|---|---|---|
| **lifting_connection** | lifting ↔ crane/lifting tool | lifting evidence, CG |
| **storage_support** | storage_support ↔ storage base | orientation, support spacing |
| **transport_fixation** | transport_fixation ↔ vehicle/fixation | envelope, tie-down |
| **temporary_bracing** | temporary_bracing ↔ bracing system | stability need |
| **assembly_access** | assembly_access ↔ site clearance | clearance volume |
| **protection** | protection ↔ protection material | exposed/damaged surface |

## Example A — DE_1OG_001 slab

```yaml
- id: logistics.storage.bottom
  kind: storage_support
  abstract_geometry: surface_zone
  point: center_of_bottom_face
  direction: downward_normal
  compatible_with: [storage_support]

- id: logistics.lifting.top
  kind: lifting
  abstract_geometry: point_or_surface_zone
  point: lifting_candidate_point
  direction: upward
  compatible_with: [lifting]
```

## Example B — Wand–Decke

```yaml
- id: logistics.access.wall_top
  kind: assembly_access
  abstract_geometry: clearance_volume
  point: center_of_wall_top_access_zone
  direction: access_direction
  compatible_with: [assembly_access]

- id: logistics.lifting.slab_placement
  kind: lifting
  abstract_geometry: point
  point: slab_lifting_reference
  direction: upward
  compatible_with: [lifting]
```

## Example C — SlabBeamColumnFragment

```yaml
- id: logistics.lifting.stable_zone
  kind: lifting
  abstract_geometry: point_or_surface_zone
  point: stable_lifting_point
  direction: upward
  compatible_with: [lifting]

- id: logistics.bracing.column_stub
  kind: temporary_bracing
  abstract_geometry: surface_zone
  point: bracing_point_on_column_stub
  direction: bracing_direction
  compatible_with: [temporary_bracing]

- id: logistics.protection.cut_face
  kind: protection
  abstract_geometry: surface_zone
  point: center_of_cut_face
  direction: cut_face_normal
  compatible_with: [protection]
```

---

# 11. Package 6 — Evidence Overlay

## General abstraction

```text
Evidence → overlay model
```

## Abstract representation

| Evidence | Abstraction |
|---|---|
| Rebar scan | line / zone |
| Unknown rebar | uncertainty zone |
| Damage | surface/volume zone |
| Crack | line |
| Spalling | surface/edge zone |
| Core sample | point/cylinder |
| Carbonation test | point/depth line |
| Confidence | zone |

## Minimal properties

```text
evidence type
location
confidence
affected ports
effect: ok | warning | blocked | confidence_reduced
```

## Ports

```text
None by default.
```

Evidence does not create design ports.  
It modifies the usability of ports from other packages.

## Evidence effects

| Evidence overlay | Affected ports |
|---|---|
| rebar line / zone | anchor, dowel, core_drilling |
| unknown rebar | anchor, dowel, core_drilling |
| damage zone | bearing, lifting, visible_reuse |
| crack line | structural bearing/continuity |
| exposed rebar | structural, durability-related ports |
| spalling zone | bearing, lifting, visible_reuse |
| confidence zone | any generated port |

## Example A — DE_1OG_001 slab

```text
unknown rebar
→ blocks / warns structural.anchor.edge_left

damage at slab edge
→ warns structural.bearing.edge_left

spalling at lifting region
→ warns logistics.lifting.top
```

## Example B — Wand–Decke

```text
rebar conflict
→ blocks structural.anchor.wall_top

unknown reinforcement
→ warns structural.grout.wall_top

damage at wall top
→ warns structural.support.wall_top

damage at slab edge
→ warns structural.bearing.slab_edge
```

## Example C — SlabBeamColumnFragment

```text
unknown rebar at monolithic junction
→ blocks nearby anchor/core-drilling ports

cut-face damage
→ warns structural.cut_face_risk

exposed rebar
→ warns structural and durability use

cracks near beam-column junction
→ reduces confidence of structural.continuity.beam_column
```

---

# 12. Minimal Component Data Shape

```yaml
component:
  id: string
  typology: string
  material: string

  packages:
    structural:
      abstraction: line | surface | graph | volume
      properties: {}
      ports: []
      connectors: []

    energy:
      abstraction: surface_boundary_model
      properties: {}
      ports: []
      connectors: []

    tga:
      abstraction: opening_route_model
      properties: {}
      ports: []
      connectors: []

    semantic:
      abstraction: spatial_visual_model
      properties: {}
      ports: []
      connectors: []

    logistics:
      abstraction: handling_model
      properties: {}
      ports: []
      connectors: []

    evidence:
      abstraction: overlay_model
      overlays: []
      port_effects: []
```

---

# 13. Final Minimal Rule

```text
For every package ask only four questions:

1. What is the abstract representation?
2. What minimal properties does it need?
3. Where are the ports?
4. Which connector rules can use those ports?
```

That is the target level of abstraction.

Example:

```text
Beam in structural package:
real beam → 1D line element
properties → section + material
ports → end joints / supports
connectors → joint, support, bearing
calculation later → line + properties + connectors + loads
```
