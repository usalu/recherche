# Minimal Package Abstraction Model
## Representations, Ports, Connectors, and Examples

**Goal**  
Reduce each package to the minimum needed for calculation, evaluation, or rule checking.

The model follows the same logic as a structural beam abstraction:

```text
real component
↓
abstract representation
↓
minimal properties
↓
ports
↓
connector rules
↓
calculation / evaluation
```

A package should not keep all geometry.  
It keeps only the geometry required for its own calculation.

---

# 1. Universal Rule

Each package has only four things:

```text
1. Representation
   The simplified model used by that package.

2. Properties
   The minimum values required for calculation.

3. Ports
   The minimal places where this package can connect or relate.

4. Connector rules
   The minimal rules that connect compatible ports.
```

A **port** is a Semio-style connector handle:

```text
Port = ID + point + direction + kind
```

A **connector rule** defines which port kinds can connect and what must be checked.

---

# 2. Universal Geometry Abstractions

| Abstraction | Meaning | Example |
|---|---|---|
| **Point** | 0D reference | node, lifting point, sample point |
| **Line** | 1D axis / edge / route | beam axis, joint line, cable route |
| **Surface** | 2D face / boundary | slab face, wall face, thermal boundary |
| **Zone** | part of a point, line, surface, or volume | bearing strip, damage patch |
| **Volume** | 3D body / space | component body, opening, transport envelope |
| **Graph** | nodes + edges + relations | structural network, service network |

Important:

```text
Line support = line + narrow bearing strip.
Point support = point + local bearing patch.
```

---

# 3. Minimal Port Schema

```yaml
port:
  id: string
  package: structural | energy | tga | semantic | logistics
  kind: string
  point: [x, y, z]
  direction: [dx, dy, dz]
  abstraction: point | line | surface | zone | volume
  compatible_with: [port_kind]
```

---

# 4. Minimal Connector Rule Schema

```yaml
connector_rule:
  id: string
  connects: [port_kind, port_kind]
  checks: [minimal_check]
  output: pass | warning | fail | value
```

---

# 5. Package Overview

```text
PACKAGES
│
├── 0. Base Geometry
├── 1. Structural
├── 2. Energy / Envelope
├── 3. TGA / Openings
├── 4. Semantic / Architectural
├── 5. Logistics / Assembly
└── 6. Evidence Overlay
```

---

# 6. Package 0 — Base Geometry

## 6.1 Representation

```text
real component → simplified geometric body
```

## 6.2 Minimal abstraction

| Real geometry | Abstract representation |
|---|---|
| component | volume |
| face | surface |
| edge | line |
| opening | void volume |
| center | point |

## 6.3 Minimal properties

```text
dimensions
volume
main faces
main edges
openings
center point
```

## 6.4 Ports

```text
None.
```

Base Geometry does not create ports or connector rules.

## 6.5 Connector rules

```text
None.
```

## 6.6 Explanation

Base Geometry is the neutral source.  
Other packages read it and create their own abstractions.

Example:

```text
real slab
→ volume
→ top surface
→ bottom surface
→ edge lines
```

---

# 7. Package 1 — Structural

## 7.1 Representation

```text
real component → structural model
```

## 7.2 Minimal abstraction

| Real component | Structural representation |
|---|---|
| beam | 1D line element |
| column | 1D vertical line element |
| slab | 2D plate surface |
| wall | 2D wall surface |
| support | point/line + bearing patch |
| monolithic fragment | graph of line/surface elements + continuity zones |

## 7.3 Minimal properties

```text
role
span direction
section / thickness
material
support zones
capacity status: known | unknown
evidence status
```

## 7.4 Minimal ports

| Port kind | Abstraction | Meaning | Compatible with |
|---|---|---|---|
| **bearing** | surface zone | this element bears on something | support, steel_support |
| **support** | line+strip or point+patch | this element supports something | bearing |
| **joint** | point or line | structural node / meeting point | joint |
| **anchor** | point / surface zone | possible fixed connection | anchor, support |
| **continuity** | volume zone | internal monolithic continuity | continuity only internal |

## 7.5 Minimal connector rules

| Connector rule | Connects | Minimal checks |
|---|---|---|
| **bearing_support** | bearing ↔ support | overlap, direction, bearing length |
| **joint_connection** | joint ↔ joint | node alignment, rotation condition |
| **anchor_connection** | anchor ↔ anchor/support | edge distance, rebar evidence |
| **monolithic_continuity** | continuity ↔ continuity | internal continuity only |

These four are enough for the minimal structural abstraction.  
Special systems such as screws, dowels, grout, or steel supports can be mapped later as variants of these connector rules.

## 7.6 Calculation logic

```text
structural representation
+ properties
+ ports
+ connector rules
+ loads
↓
structural check / calculation
```

Example for a beam:

```text
beam → 1D line element
ports → end joints
connectors → joint_connection / support
calculation → stiffness model
```

---

## 7.7 Example A — Abbau/Aufbau slab DE_1OG_001

### Representation

```text
real slab
→ 2D plate surface
→ edge lines
→ bearing strips at usable edges
```

### Minimal properties

```text
dimensions: 4500 × 2300 × 180 mm
volume: 1.863 m³
mass: ca. 4.1 t
thickness: 180 mm
capacity status: unknown unless proof exists
```

### Ports

```yaml
- id: structural.bearing.edge_left
  kind: bearing
  abstraction: surface_zone
  point: midpoint_of_left_edge_bearing_strip
  direction: downward_or_support_normal
  compatible_with: [support, steel_support]

- id: structural.anchor.edge_left
  kind: anchor
  abstraction: surface_zone
  point: center_of_anchor_candidate_zone
  direction: drilling_axis
  compatible_with: [anchor, support]
```

### Connector rules

```text
bearing_support:
slab bearing port ↔ wall/beam/steel support port

anchor_connection:
slab anchor port ↔ support or anchor port
```

### Explanation

The slab is not stored as a full detailed mesh for structural checking.  
It becomes a plate with edge bearing ports.  
Only if a design needs fixing or restraint does the anchor port become relevant.

---

## 7.8 Example B — Wand–Decke

### Representation

```text
wall → 2D wall surface + top support strip
slab → 2D plate surface + edge bearing strip
```

### Ports

```yaml
wall:
  - id: structural.support.wall_top
    kind: support
    abstraction: line_plus_surface_strip
    point: midpoint_of_wall_top
    direction: upward
    compatible_with: [bearing]

slab:
  - id: structural.bearing.slab_edge
    kind: bearing
    abstraction: line_plus_surface_strip
    point: midpoint_of_slab_edge
    direction: downward_or_edge_normal
    compatible_with: [support]
```

### Connector rules

```text
bearing_support:
wall support ↔ slab bearing

anchor_connection:
optional restraint / fixing

joint_connection:
only if the wall-slab interface is modeled as a rigid node
```

### Abbau/Aufbau mapping

The following Abbau/Aufbau connector systems can be treated as system-level variants of the connector rules:

```text
nachträglicher Bewehrungsanschluss + Verguss
→ anchor_connection + bearing_support

Schraubanker mit Flachstahlhalter
→ anchor_connection + bearing_support
```

### Explanation

The minimal structural calculation does not need to know every screw or plate at first.  
It needs to know:

```text
where the slab bears
where the wall supports
whether the interface is only bearing, fixed, or restrained
what evidence is missing
```

---

## 7.9 Example C — SlabBeamColumnFragment

### Representation

```text
one real monolithic fragment
→ structural graph

slab zone → 2D plate surface
beam zone → 1D beam line + section
column stub → 1D column line
internal junctions → continuity zones
cut faces → risk surfaces
```

### Ports

```yaml
- id: structural.bearing.slab_edge_external
  kind: bearing
  abstraction: line_plus_surface_strip
  point: midpoint_of_external_slab_edge
  direction: outward_or_support_normal
  compatible_with: [support, steel_support]

- id: structural.joint.beam_end
  kind: joint
  abstraction: surface_patch
  point: center_of_beam_cut_end
  direction: beam_axis
  compatible_with: [joint, support]

- id: structural.continuity.slab_beam
  kind: continuity
  abstraction: volume_zone
  point: centroid_of_slab_beam_junction
  direction: beam_axis
  compatible_with: [continuity]
```

### Connector rules

```text
bearing_support:
external slab/beam bearing ↔ support

joint_connection:
beam end ↔ new beam/column joint

monolithic_continuity:
internal slab-beam-column continuity
```

### Explanation

The fragment is not three pieces connected together.  
It is one piece with internal continuity.  
Only the external ports connect to other components.

---

# 8. Package 2 — Energy / Envelope

## 8.1 Representation

```text
real component → thermal boundary model
```

## 8.2 Minimal abstraction

| Real condition | Energy representation |
|---|---|
| exterior surface | thermal boundary surface |
| insulation side | insulation surface |
| edge / joint | thermal bridge line or zone |
| opening through envelope | penetration zone |
| roof/ground exposure | exposure surface |

## 8.3 Minimal properties

```text
thermal side: interior | exterior | ground | roof
area
thickness
lambda
assembly status: known | unknown
```

## 8.4 Minimal ports

| Port kind | Abstraction | Meaning | Compatible with |
|---|---|---|---|
| **thermal_boundary** | surface | thermal surface | thermal_boundary |
| **insulation** | surface | insulation layer contact | insulation |
| **thermal_bridge** | line / zone | heat-loss risk | thermal_bridge |
| **penetration** | opening zone | envelope break | penetration, service |

## 8.5 Minimal connector rules

| Connector rule | Connects | Minimal checks |
|---|---|---|
| **thermal_continuity** | thermal_boundary ↔ thermal_boundary | same boundary side, aligned surfaces |
| **insulation_continuity** | insulation ↔ insulation | layer continuity |
| **thermal_bridge_warning** | thermal_bridge ↔ thermal_bridge/connector | risk condition |
| **penetration_sealing** | penetration ↔ service/connector | sealing required |

## 8.6 Calculation logic

```text
surfaces + thickness + lambda + connector rules
↓
rough U-value / continuity check / thermal bridge warning
```

---

## 8.7 Example A — DE_1OG_001 slab

### Representation

```text
if used inside:
no active energy model needed

if used as roof or exterior floor:
2D thermal boundary surface
edge thermal bridge line
thickness = 180 mm
```

### Ports

```yaml
- id: energy.thermal_boundary.top
  kind: thermal_boundary
  abstraction: surface
  point: center_of_top_surface
  direction: exterior_normal
  compatible_with: [thermal_boundary]

- id: energy.thermal_bridge.edge_left
  kind: thermal_bridge
  abstraction: line_zone
  point: midpoint_of_slab_edge
  direction: exterior_normal
  compatible_with: [thermal_bridge]
```

### Connector rules

```text
thermal_continuity
thermal_bridge_warning
```

### Explanation

The slab only needs energy ports when it is part of the building envelope.  
Interior slabs do not need an active thermal connector model.

---

## 8.8 Example B — Wand–Decke

### Representation

```text
wall-slab joint
→ thermal bridge line/zone if in envelope
```

### Ports

```yaml
- id: energy.thermal_bridge.wall_slab_joint
  kind: thermal_bridge
  abstraction: line_zone
  point: midpoint_of_joint
  direction: exterior_normal
  compatible_with: [thermal_bridge]

- id: energy.insulation.wall_side
  kind: insulation
  abstraction: surface
  point: center_of_insulation_side
  direction: exterior_normal
  compatible_with: [insulation]
```

### Connector rules

```text
insulation_continuity
thermal_bridge_warning
```

### Explanation

The energy model does not need the full connector detail.  
It needs to know whether insulation continues and whether the joint creates a bridge.

---

## 8.9 Example C — SlabBeamColumnFragment

### Representation

```text
irregular thermal boundary model
beam projection = thermal bridge zone
column stub = thermal bridge zone
cut face = moisture / envelope risk surface
```

### Ports

```yaml
- id: energy.thermal_bridge.beam_projection
  kind: thermal_bridge
  abstraction: zone
  point: centroid_of_beam_projection
  direction: exterior_normal
  compatible_with: [thermal_bridge]

- id: energy.penetration.cut_face_risk
  kind: penetration
  abstraction: surface_zone
  point: center_of_cut_face
  direction: cut_face_normal
  compatible_with: [penetration]
```

### Connector rules

```text
thermal_bridge_warning
penetration_sealing
```

### Explanation

The fragment can create complex thermal bridges.  
Minimal modeling only needs to mark the protrusions and cut faces as risk ports.

---

# 9. Package 3 — TGA / Openings

## 9.1 Representation

```text
real component → service route / opening model
```

## 9.2 Minimal abstraction

| Real condition | TGA representation |
|---|---|
| existing opening | opening volume + axis |
| possible drilling | cylinder |
| cable route | line corridor |
| pipe route | line / volume corridor |
| blocked area | blocked zone |

## 9.3 Minimal properties

```text
opening size
route diameter
axis direction
edge distance
blocked status
```

## 9.4 Minimal ports

| Port kind | Abstraction | Meaning | Compatible with |
|---|---|---|---|
| **opening** | opening volume | existing opening | pipe_route, cable_route |
| **core_drilling** | cylinder | possible new hole | pipe_route, cable_route |
| **pipe_route** | corridor volume | pipe path | opening, core_drilling, pipe_route |
| **cable_route** | line corridor | cable path | opening, core_drilling, cable_route |
| **blocked** | zone | cannot pass | none |

## 9.5 Minimal connector rules

| Connector rule | Connects | Minimal checks |
|---|---|---|
| **route_continuity** | pipe_route/cable_route ↔ pipe_route/cable_route | alignment, diameter/corridor |
| **opening_use** | opening ↔ pipe_route/cable_route | size, axis |
| **core_drilling_use** | core_drilling ↔ pipe_route/cable_route | edge distance, rebar evidence |
| **blocked_conflict** | any route ↔ blocked | block |

---

## 9.6 Example A — DE_1OG_001 slab

### Representation

```text
no existing opening recorded
optional core-drilling cylinder if services are required
```

### Ports

```yaml
- id: tga.core_drilling.candidate_01
  kind: core_drilling
  abstraction: cylinder
  point: candidate_center
  direction: drilling_axis
  compatible_with: [pipe_route, cable_route]
```

### Connector rules

```text
core_drilling_use
blocked_conflict
```

### Explanation

The slab should not automatically allow drilling.  
The port only says where drilling could be checked.

---

## 9.7 Example B — Wand–Decke

### Representation

```text
service route line near wall/slab
blocked zone near bearing joint
```

### Ports

```yaml
- id: tga.cable_route.wall_top
  kind: cable_route
  abstraction: line_corridor
  point: route_control_point
  direction: horizontal_route_direction
  compatible_with: [cable_route, opening]

- id: tga.blocked.bearing_joint
  kind: blocked
  abstraction: zone
  point: center_of_bearing_joint
  direction: joint_normal
  compatible_with: []
```

### Connector rules

```text
route_continuity
blocked_conflict
```

### Explanation

The service model stays minimal: possible route plus blocked structural joint.

---

## 9.8 Example C — SlabBeamColumnFragment

### Representation

```text
possible route through slab zone
blocked beam and column zones
```

### Ports

```yaml
- id: tga.core_drilling.slab_zone
  kind: core_drilling
  abstraction: cylinder
  point: safe_slab_zone_point
  direction: drilling_axis
  compatible_with: [pipe_route, cable_route]

- id: tga.blocked.beam_zone
  kind: blocked
  abstraction: volume_zone
  point: center_of_beam_zone
  direction: beam_axis
  compatible_with: []
```

### Connector rules

```text
core_drilling_use
blocked_conflict
```

### Explanation

The service abstraction only needs to mark safe possible holes and blocked structural zones.

---

# 10. Package 4 — Semantic / Architectural

## 10.1 Representation

```text
real component → spatial / visual relation model
```

## 10.2 Minimal abstraction

| Real condition | Semantic representation |
|---|---|
| room side | boundary surface |
| visible surface | visible zone |
| joint | line |
| grid/rhythm | line or module |
| identity trace | surface zone |

## 10.3 Minimal properties

```text
visible side
room side
joint line
grid direction
identity zone
condition status
```

## 10.4 Minimal ports

| Port kind | Abstraction | Meaning | Compatible with |
|---|---|---|---|
| **room_boundary** | surface | space boundary | room_boundary |
| **visible_reuse** | surface/edge zone | visible reuse expression | visible_reuse, identity |
| **joint_line** | line | visible joint | joint_line, datum |
| **datum** | line/plane | alignment | datum, joint_line |
| **grid** | line/module | repetition | grid |
| **identity** | surface zone | trace / ID | visible_reuse, identity |

## 10.5 Minimal connector rules

| Connector rule | Connects | Minimal checks |
|---|---|---|
| **boundary_alignment** | room_boundary ↔ room_boundary | coplanarity / adjacency |
| **joint_alignment** | joint_line ↔ joint_line/datum | line alignment |
| **grid_continuity** | grid ↔ grid | spacing / direction |
| **visibility_relation** | visible_reuse ↔ visible_reuse/identity | visibility preference |

---

## 10.6 Example A — DE_1OG_001 slab

### Representation

```text
bottom surface as visible ceiling
edge line as joint / grid
```

### Ports

```yaml
- id: semantic.visible_reuse.bottom
  kind: visible_reuse
  abstraction: surface
  point: center_of_bottom_face
  direction: downward_normal
  compatible_with: [visible_reuse, identity]

- id: semantic.grid.width
  kind: grid
  abstraction: line
  point: midpoint_of_reference_edge
  direction: grid_direction
  compatible_with: [grid]
```

### Connector rules

```text
visibility_relation
grid_continuity
```

### Explanation

The semantic model does not need all surfaces.  
It needs only visible surfaces, grid lines, and identity zones.

---

## 10.7 Example B — Wand–Decke

### Representation

```text
wall face as room boundary
wall-slab joint as joint line
```

### Ports

```yaml
- id: semantic.room_boundary.wall_face
  kind: room_boundary
  abstraction: surface
  point: center_of_wall_face
  direction: room_side_normal
  compatible_with: [room_boundary]

- id: semantic.joint.wall_slab
  kind: joint_line
  abstraction: line
  point: midpoint_of_joint
  direction: joint_direction
  compatible_with: [joint_line, datum]
```

### Connector rules

```text
boundary_alignment
joint_alignment
```

### Explanation

Only two architectural relations are needed here: spatial boundary and joint expression.

---

## 10.8 Example C — SlabBeamColumnFragment

### Representation

```text
monolithic junction as visible reuse zone
original bay rhythm as grid line
cut face as identity surface
```

### Ports

```yaml
- id: semantic.visible_reuse.monolithic_junction
  kind: visible_reuse
  abstraction: zone
  point: centroid_of_visible_junction
  direction: viewing_normal
  compatible_with: [visible_reuse, identity]

- id: semantic.grid.original_bay
  kind: grid
  abstraction: line
  point: original_bay_reference_point
  direction: original_grid_direction
  compatible_with: [grid]
```

### Connector rules

```text
visibility_relation
grid_continuity
```

### Explanation

The fragment’s architectural value is its visible former structure.  
The minimal model captures only this visibility and grid relation.

---

# 11. Package 5 — Logistics / Assembly

## 11.1 Representation

```text
real component → handling model
```

## 11.2 Minimal abstraction

| Real condition | Logistics representation |
|---|---|
| whole object | transport volume |
| mass center | point |
| lifting place | point/zone |
| storage face | surface zone |
| access need | clearance volume |
| fragile area | protection zone |

## 11.3 Minimal properties

```text
mass
transport dimensions
center of gravity
storage orientation
lifting status
access clearance
protection zones
```

## 11.4 Minimal ports

| Port kind | Abstraction | Meaning | Compatible with |
|---|---|---|---|
| **lifting** | point/zone | lift component | lifting |
| **storage_support** | surface/line strip | store component | storage_support |
| **transport_fixation** | point/edge zone | secure during transport | transport_fixation |
| **assembly_access** | clearance volume | access during assembly | assembly_access |
| **protection** | surface/edge zone | protect fragile area | protection |

## 11.5 Minimal connector rules

| Connector rule | Connects | Minimal checks |
|---|---|---|
| **lifting_check** | lifting ↔ lifting tool | mass, center of gravity, evidence |
| **storage_check** | storage_support ↔ storage base | orientation, support spacing |
| **transport_check** | transport_fixation ↔ vehicle/fixation | envelope, fixation |
| **access_check** | assembly_access ↔ site/access volume | clearance |
| **protection_check** | protection ↔ protection material | exposed/damaged surface |

---

## 11.6 Example A — DE_1OG_001 slab

### Representation

```text
transport volume
center point
bottom storage surface
edge assembly access
```

### Ports

```yaml
- id: logistics.storage.bottom
  kind: storage_support
  abstraction: surface_zone
  point: center_of_bottom_face
  direction: downward_normal
  compatible_with: [storage_support]

- id: logistics.lifting.top
  kind: lifting
  abstraction: point_or_zone
  point: lifting_candidate_point
  direction: upward
  compatible_with: [lifting]
```

### Connector rules

```text
storage_check
lifting_check
transport_check
```

### Explanation

The logistics model does not need all geometry.  
It needs mass, center, envelope, support face, and lifting/access ports.

---

## 11.7 Example B — Wand–Decke

### Representation

```text
wall-top access volume
slab placement / lifting reference
```

### Ports

```yaml
- id: logistics.access.wall_top
  kind: assembly_access
  abstraction: clearance_volume
  point: center_of_wall_top_access_zone
  direction: access_direction
  compatible_with: [assembly_access]

- id: logistics.lifting.slab_placement
  kind: lifting
  abstraction: point
  point: slab_lifting_reference
  direction: upward
  compatible_with: [lifting]
```

### Connector rules

```text
access_check
lifting_check
```

### Explanation

Only access and lifting are needed for this interface.

---

## 11.8 Example C — SlabBeamColumnFragment

### Representation

```text
irregular transport volume
shifted center point
stable lifting zone
cut-face protection zone
temporary access/bracing zone
```

### Ports

```yaml
- id: logistics.lifting.stable_zone
  kind: lifting
  abstraction: point_or_zone
  point: stable_lifting_point
  direction: upward
  compatible_with: [lifting]

- id: logistics.protection.cut_face
  kind: protection
  abstraction: surface_zone
  point: center_of_cut_face
  direction: cut_face_normal
  compatible_with: [protection]
```

### Connector rules

```text
lifting_check
protection_check
transport_check
```

### Explanation

The fragment needs a handling abstraction because its center of gravity and fragile cut faces may not be simple.

---

# 12. Package 6 — Evidence Overlay

## 12.1 Representation

```text
evidence → overlay model
```

## 12.2 Minimal abstraction

| Evidence | Abstraction |
|---|---|
| rebar scan | line / zone |
| unknown rebar | uncertainty zone |
| damage | surface/volume zone |
| crack | line |
| core sample | point/cylinder |
| confidence | zone |

## 12.3 Minimal properties

```text
evidence type
location
confidence
affected port
effect: ok | warning | blocked | confidence_reduced
```

## 12.4 Ports

```text
None.
```

Evidence does not create design ports.  
It modifies other package ports.

## 12.5 Connector rules

Evidence has only one rule type:

| Connector rule | Applies to | Minimal checks |
|---|---|---|
| **evidence_effect** | any port | overlap, evidence type, severity |

## 12.6 Example A — DE_1OG_001 slab

```text
unknown rebar
→ warning/block on structural.anchor.edge_left

damage at slab edge
→ warning on structural.bearing.edge_left

spalling at lifting region
→ warning on logistics.lifting.top
```

## 12.7 Example B — Wand–Decke

```text
rebar conflict
→ block structural.anchor.wall_top

unknown reinforcement
→ warning on structural.anchor.wall_top

damage at wall top
→ warning on structural.support.wall_top
```

## 12.8 Example C — SlabBeamColumnFragment

```text
unknown rebar at monolithic junction
→ block nearby anchor/core-drilling ports

cut-face damage
→ warning on structural cut-face risk port

cracks near beam-column junction
→ reduce confidence of structural continuity
```

---

# 13. Final Minimal Template

Use this template for every package:

```text
Package name

Representation:
real thing → abstract model

Properties:
only values needed for calculation

Ports:
minimal port kinds + where they sit

Connector rules:
minimal rules that connect compatible ports

Example:
representation + ports + connector rules + short explanation
```

This is the target level of abstraction.
