# Minimal Package Abstraction Model
## v12 — Connectors Have Ports; Ports Control Compatibility

**Goal**  
Keep the model minimal and calculation-ready.

```text
real component
↓
package abstraction
↓
minimal properties
↓
connectors
↓
ports on connectors
↓
port-to-port compatibility
↓
calculation / evaluation
```

---

# 1. Correct Core Concept

## 1.1 Connector

A **connector** is a typed connection feature on a component package.

It defines:

```text
what relation is possible
which properties the relation needs
which ports it exposes
which checks are required later
```

Example:

```text
bearing_support connector
= a structural connector that allows one element to bear on another.
```

## 1.2 Port

A **port** is the actual connectable socket exposed by a connector.

It defines:

```text
where another element can connect
which direction the connection faces
what port roles it is compatible with
```

Example:

```text
bearing_side port
can connect to
support_side port
```

## 1.3 Compatibility

Compatibility is checked **port-to-port**.

```text
Component A connector → Port A
Component B connector → Port B

Port A compatible with Port B
↓
connector checks can run
```

## 1.4 Minimal schema

```yaml
connector:
  id: structural.bearing_support.edge_left
  package: structural
  kind: bearing_support
  properties:
    support_mode: line
    fixity: pinned
    min_bearing_length_mm: 80
  ports:
    - id: structural.bearing_support.edge_left.bearing_side
      role: bearing_side
      point: [x, y, z]
      direction: [dx, dy, dz]
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
  checks:
    - bearing_overlap
    - direction
    - bearing_length
```

---

# 2. Universal Geometry Abstractions

| Abstraction | Meaning | Example |
|---|---|---|
| **Point** | 0D reference | node, lifting point, sample point |
| **Line** | 1D axis / route | beam axis, joint line, cable route |
| **Surface** | 2D boundary | wall face, slab face, thermal face |
| **Zone** | meaningful sub-area | bearing strip, damage patch |
| **Volume** | 3D body / space | opening, transport envelope |
| **Graph** | nodes + relations | structural graph, service graph |

Important:

```text
Line support = line + narrow bearing strip.
Point support = point + local bearing patch.
```

---

# 3. Package Template

Every package should be written with the same structure:

```text
Representation:
real thing → abstract model

Properties:
only values needed for calculation

Connectors:
minimum connector types

Ports:
listed inside each connector

Examples:
A, B, C
```

---

# 4. Package 0 — Base Geometry

## Representation

```text
real component → simplified geometric body
```

## Properties

```text
dimensions
volume
main faces
main edges
openings
center point
```

## Connectors

```text
None.
```

## Ports

```text
None.
```

Base Geometry only provides the raw geometric basis.

## Example A — DE_1OG_001 slab

```text
real slab
→ volume
→ top surface
→ bottom surface
→ edge lines
→ dimensions: 4500 × 2300 × 180 mm
→ volume: 1.863 m³
```

## Example B — Wand–Decke

```text
wall + slab
→ two simplified volumes
→ wall top surface
→ slab edge surface
→ possible contact area
```

## Example C — SlabBeamColumnFragment

```text
one monolithic fragment
→ one composite volume
→ slab zone
→ beam zone
→ column-stub zone
→ cut faces
→ center point
```

---

# 5. Package 1 — Structural

## Representation

```text
real component → structural abstraction
```

| Real component | Structural abstraction |
|---|---|
| beam | 1D line element |
| column | 1D vertical line element |
| slab | 2D plate surface |
| wall | 2D wall surface |
| local support | point/line + bearing patch |
| composite monolithic component | decomposed graph of slab/beam/column abstractions |

## Properties

```text
role
span direction
section / thickness
material
support geometry
fixity
capacity status: known | unknown
evidence status
```

## Important correction

```text
monolithic_continuity is not a connector.
```

A monolithic component is decomposed into its main structural abstractions.

Example:

```text
SlabBeamColumnFragment
→ slab surface
→ beam line
→ column line
→ shared internal graph relation
```

The internal relation is part of the representation, not a connector and not a port.

## Minimal connectors

Only three structural connector types are needed.

| Connector | Purpose |
|---|---|
| **bearing_support** | one element bears on another |
| **node_joint** | structural node, end, or joint connects to another node/joint |
| **restraint_fixing** | anchor, dowel, screw, rebar, plate, or other restraint/fixing |

Specific systems such as `Schraubanker`, `Edelstahldorn`, `Flachstahlhalter`, or `Verguss` are connector **properties**, not separate connector types.

---

## 5.1 Connector: bearing_support

### Properties

```yaml
properties:
  support_mode: line | point | surface
  load_type: compression
  min_bearing_length_mm: number | unknown
  min_bearing_width_mm: number | unknown
  fixity: free | pinned | roller | spring | fixed
  capacity_status: known | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **bearing_side** | element that sits/bears | support_side |
| **support_side** | element that supports | bearing_side |

### Checks

```text
overlap
direction
bearing length
bearing width
capacity status
damage/evidence status
```

---

## 5.2 Connector: node_joint

### Properties

```yaml
properties:
  joint_mode: pinned | rigid | semi_rigid | spring
  transfer:
    axial: true | false
    shear: true | false
    moment: true | false
  node_type: beam_end | column_end | frame_node | slab_point
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **joint_side** | node or end to join | joint_side |

### Checks

```text
node alignment
direction
rotation condition
required fixity
capacity status
```

---

## 5.3 Connector: restraint_fixing

### Properties

```yaml
properties:
  method_family:
    - anchor
    - dowel
    - post_installed_rebar
    - screw_anchor
    - flat_steel_holder
    - grout
    - steel_support
  restraint_type: translation | rotation | shear | moment | combined
  drilling_required: true | false
  rebar_evidence_required: true | false
  edge_distance_required: true | false
  fire_relevant: true | false
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **fixing_side** | side that applies fixing/restraint | receiving_side |
| **receiving_side** | side that receives fixing/restraint | fixing_side |

### Checks

```text
edge distance
rebar evidence
drilling permission
embedment / engagement
fire relevance
capacity status
```

---

## Example A — DE_1OG_001 slab

### Representation

```text
real slab
→ 2D plate surface
→ edge lines
→ bearing strips at usable edges
```

### Connectors and ports

```yaml
connector:
  id: structural.bearing_support.edge_left
  kind: bearing_support
  properties:
    support_mode: line
    load_type: compression
    min_bearing_length_mm: unknown
    capacity_status: unknown
  ports:
    - role: bearing_side
      point: midpoint_of_left_edge_bearing_strip
      direction: support_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
```

Optional only if restraint is needed:

```yaml
connector:
  id: structural.restraint_fixing.edge_left
  kind: restraint_fixing
  properties:
    method_family: [post_installed_rebar, screw_anchor, flat_steel_holder]
    drilling_required: true
    rebar_evidence_required: true
  ports:
    - role: fixing_side
      point: center_of_fixing_zone
      direction: drilling_axis
      abstraction: surface_zone
      compatible_with:
        - structural.restraint_fixing.receiving_side
```

### Explanation

The slab mainly needs a **bearing_support** connector.  
A **restraint_fixing** connector is only needed if the slab must be tied, anchored, or restrained.

---

## Example B — Wand–Decke

### Representation

```text
wall
→ 2D wall surface
→ top line support strip

slab
→ 2D plate surface
→ edge bearing strip
```

### Wall connector

```yaml
connector:
  id: structural.bearing_support.wall_top
  kind: bearing_support
  properties:
    support_mode: line
    load_type: compression
  ports:
    - role: support_side
      point: midpoint_of_wall_top_strip
      direction: upward
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.bearing_side
```

### Slab connector

```yaml
connector:
  id: structural.bearing_support.slab_edge
  kind: bearing_support
  properties:
    support_mode: line
    load_type: compression
  ports:
    - role: bearing_side
      point: midpoint_of_slab_edge_strip
      direction: support_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
```

### Optional restraint/fixing connector

```yaml
connector:
  id: structural.restraint_fixing.wall_slab
  kind: restraint_fixing
  properties:
    method_family: [post_installed_rebar, screw_anchor, flat_steel_holder, grout]
    drilling_required: true
    rebar_evidence_required: true
  ports:
    - role: fixing_side
      point: wall_or_slab_fixing_zone
      direction: drilling_or_joint_axis
      abstraction: surface_zone
      compatible_with:
        - structural.restraint_fixing.receiving_side
```

### Abbau/Aufbau mapping

```text
nachträglicher Bewehrungsanschluss + Verguss
→ restraint_fixing with method_family = post_installed_rebar + grout

Schraubanker mit Flachstahlhalter
→ restraint_fixing with method_family = screw_anchor + flat_steel_holder
```

### Explanation

The connection is structurally minimal:

```text
support_side on wall
↔
bearing_side on slab
```

Additional restraint/fixing is optional and method-specific.

---

## Example C — SlabBeamColumnFragment

### Representation

```text
one monolithic fragment
→ decomposed structural graph

slab zone → 2D plate surface
beam zone → 1D beam line
column stub → 1D column line
shared internal graph relation → representation property
external cut/support faces → possible external connectors
```

### External bearing connector

```yaml
connector:
  id: structural.bearing_support.external_slab_edge
  kind: bearing_support
  properties:
    support_mode: line
    load_type: compression
  ports:
    - role: bearing_side
      point: midpoint_of_external_slab_edge_strip
      direction: support_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
```

### External node connector

```yaml
connector:
  id: structural.node_joint.beam_end
  kind: node_joint
  properties:
    joint_mode: pinned | rigid | semi_rigid
    node_type: beam_end
  ports:
    - role: joint_side
      point: center_of_beam_cut_end
      direction: beam_axis
      abstraction: point_or_surface_patch
      compatible_with:
        - structural.node_joint.joint_side
```

### What does not exist

```text
No monolithic_continuity connector.
No internal slab-beam port.
No internal beam-column port.
```

Internal slab-beam-column continuity is modeled in the representation graph.

---

# 6. Package 2 — Energy / Envelope

## Representation

```text
real component → thermal boundary abstraction
```

## Properties

```text
thermal side: interior | exterior | ground | roof
area
thickness
lambda
assembly status: known | unknown
thermal bridge risk zones
moisture risk zones
```

## Minimal connectors

Only three energy connectors are needed.

| Connector | Purpose |
|---|---|
| **boundary_continuity** | thermal/envelope boundary continues |
| **layer_continuity** | insulation or protection layer continues |
| **penetration_seal** | an opening/crossing through the envelope is sealed |

Thermal bridge is a **property/risk zone**, not a connector unless another element must connect to it.

---

## 6.1 Connector: boundary_continuity

### Properties

```yaml
properties:
  boundary_type: thermal | air | moisture | fire
  side: interior | exterior | ground | roof
  target_performance: known | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **boundary_side** | boundary face | boundary_side |

---

## 6.2 Connector: layer_continuity

### Properties

```yaml
properties:
  layer_type: insulation | waterproofing | vapor_control | fire_protection
  thickness_mm: number | unknown
  performance_status: known | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **layer_side** | layer interface | layer_side |

---

## 6.3 Connector: penetration_seal

### Properties

```yaml
properties:
  seal_type: thermal | air | moisture | fire | acoustic
  penetration_type: service | anchor | joint | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **penetration_side** | opening/crossing | seal_side |
| **seal_side** | sealing material/detail | penetration_side |

---

## Example A — DE_1OG_001 slab

If used inside:

```text
no active energy connector needed
```

If used as roof or exterior floor:

```yaml
connector:
  id: energy.boundary_continuity.top
  kind: boundary_continuity
  properties:
    boundary_type: thermal
    side: roof | exterior
  ports:
    - role: boundary_side
      point: center_of_top_surface
      direction: exterior_normal
      abstraction: surface
      compatible_with:
        - energy.boundary_continuity.boundary_side
```

Thermal bridge at edge:

```text
stored as risk zone/property, not connector.
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: energy.layer_continuity.wall_slab_insulation
  kind: layer_continuity
  properties:
    layer_type: insulation
    thickness_mm: unknown
  ports:
    - role: layer_side
      point: insulation_joint_control_point
      direction: exterior_normal
      abstraction: surface_zone
      compatible_with:
        - energy.layer_continuity.layer_side
```

Thermal bridge at joint:

```text
stored as thermal_bridge_risk_zone.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: energy.penetration_seal.cut_face
  kind: penetration_seal
  properties:
    seal_type: moisture
    penetration_type: joint
  ports:
    - role: penetration_side
      point: center_of_cut_face
      direction: cut_face_normal
      abstraction: surface_zone
      compatible_with:
        - energy.penetration_seal.seal_side
```

Beam/column protrusions:

```text
stored as thermal_bridge_risk_zones, not connectors.
```

---

# 7. Package 3 — TGA / Openings

## Representation

```text
real component → opening / service-route abstraction
```

## Properties

```text
opening size
route diameter
axis direction
edge distance
blocked zones
rebar status
```

## Minimal connectors

Only two TGA connector types are needed.

| Connector | Purpose |
|---|---|
| **route_connection** | service route continues |
| **penetration_connection** | service uses opening or drilling |

Blocked zones are not connectors.  
They are properties/zones that block ports.

---

## 7.1 Connector: route_connection

### Properties

```yaml
properties:
  service_type: cable | pipe | air | water | unknown
  route_size_mm: number | unknown
  route_direction: vector
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **route_side** | route endpoint | route_side |

---

## 7.2 Connector: penetration_connection

### Properties

```yaml
properties:
  penetration_type: existing_opening | core_drilling | sleeve
  diameter_mm: number | unknown
  drilling_required: true | false
  rebar_evidence_required: true | false
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **penetration_side** | opening/drilling socket | service_side |
| **service_side** | service using the opening | penetration_side |

---

## Example A — DE_1OG_001 slab

No existing opening is recorded in the given catalogue entry.

Possible candidate only if service routing is needed:

```yaml
connector:
  id: tga.penetration_connection.core_candidate_01
  kind: penetration_connection
  properties:
    penetration_type: core_drilling
    drilling_required: true
    rebar_evidence_required: true
  ports:
    - role: penetration_side
      point: candidate_drilling_center
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - tga.penetration_connection.service_side
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: tga.route_connection.wall_top
  kind: route_connection
  properties:
    service_type: cable
    route_direction: horizontal
  ports:
    - role: route_side
      point: route_control_point
      direction: horizontal_route_direction
      abstraction: line_corridor
      compatible_with:
        - tga.route_connection.route_side
```

Blocked bearing joint:

```text
stored as blocked_zone property, not connector.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: tga.penetration_connection.slab_zone
  kind: penetration_connection
  properties:
    penetration_type: core_drilling
    drilling_required: true
    rebar_evidence_required: true
  ports:
    - role: penetration_side
      point: safe_point_in_slab_zone
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - tga.penetration_connection.service_side
```

Beam and column zones:

```text
stored as blocked_zones, not connectors.
```

---

# 8. Package 4 — Semantic / Architectural

## Representation

```text
real component → spatial / visual abstraction
```

## Properties

```text
visible side
room side
joint line
grid direction
identity zone
condition status
```

## Minimal connectors

Only three semantic connectors are needed.

| Connector | Purpose |
|---|---|
| **boundary_relation** | room/spatial boundary relates to another boundary |
| **alignment_relation** | joint, datum, or grid aligns |
| **visibility_relation** | visible reuse or identity is expressed |

---

## 8.1 Connector: boundary_relation

### Properties

```yaml
properties:
  boundary_type: room | facade | circulation | threshold
  side: interior | exterior | public | private | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **boundary_side** | spatial boundary surface | boundary_side |

---

## 8.2 Connector: alignment_relation

### Properties

```yaml
properties:
  alignment_type: joint | datum | grid
  direction: vector
  spacing_mm: number | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **alignment_side** | line/grid/datum handle | alignment_side |

---

## 8.3 Connector: visibility_relation

### Properties

```yaml
properties:
  visibility_type: exposed_surface | cut_face | reuse_identity | trace
  condition_status: known | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **visible_side** | visible reuse surface/zone | visible_side, identity_side |
| **identity_side** | ID/trace/story zone | visible_side, identity_side |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: semantic.visibility_relation.bottom
  kind: visibility_relation
  properties:
    visibility_type: exposed_surface
  ports:
    - role: visible_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface
      compatible_with:
        - semantic.visibility_relation.visible_side
        - semantic.visibility_relation.identity_side
```

```yaml
connector:
  id: semantic.alignment_relation.width_grid
  kind: alignment_relation
  properties:
    alignment_type: grid
    spacing_mm: 2300
  ports:
    - role: alignment_side
      point: midpoint_of_reference_edge
      direction: grid_direction
      abstraction: line
      compatible_with:
        - semantic.alignment_relation.alignment_side
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: semantic.boundary_relation.wall_face
  kind: boundary_relation
  properties:
    boundary_type: room
  ports:
    - role: boundary_side
      point: center_of_wall_face
      direction: room_side_normal
      abstraction: surface
      compatible_with:
        - semantic.boundary_relation.boundary_side
```

```yaml
connector:
  id: semantic.alignment_relation.wall_slab_joint
  kind: alignment_relation
  properties:
    alignment_type: joint
  ports:
    - role: alignment_side
      point: midpoint_of_joint_line
      direction: joint_direction
      abstraction: line
      compatible_with:
        - semantic.alignment_relation.alignment_side
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: semantic.visibility_relation.monolithic_fragment
  kind: visibility_relation
  properties:
    visibility_type: trace
  ports:
    - role: visible_side
      point: centroid_of_visible_fragment_zone
      direction: viewing_normal
      abstraction: surface_or_zone
      compatible_with:
        - semantic.visibility_relation.visible_side
        - semantic.visibility_relation.identity_side
```

Original bay rhythm:

```yaml
connector:
  id: semantic.alignment_relation.original_bay_grid
  kind: alignment_relation
  properties:
    alignment_type: grid
  ports:
    - role: alignment_side
      point: original_bay_reference_point
      direction: original_grid_direction
      abstraction: line
      compatible_with:
        - semantic.alignment_relation.alignment_side
```

---

# 9. Package 5 — Logistics / Assembly

## Representation

```text
real component → handling abstraction
```

## Properties

```text
mass
transport dimensions
center of gravity
storage orientation
lifting status
access clearance
protection zones
```

## Minimal connectors

Only four logistics connectors are needed.

| Connector | Purpose |
|---|---|
| **lifting_interface** | component can be lifted |
| **support_interface** | component can be stored or temporarily supported |
| **fixation_interface** | component can be fixed for transport/assembly |
| **access_interface** | component requires or offers assembly access |

Protection is normally a property/zone, not a connector, unless a protection system itself needs to attach.

---

## 9.1 Connector: lifting_interface

### Properties

```yaml
properties:
  lifting_method: crane | sling | insert | unknown
  lifting_capacity_status: known | unknown
  center_of_gravity_required: true
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **lifting_side** | component lifting point/zone | tool_side |
| **tool_side** | lifting tool side | lifting_side |

---

## 9.2 Connector: support_interface

### Properties

```yaml
properties:
  support_context: storage | temporary_support | assembly_support
  orientation: lying | standing | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **component_support_side** | component side to support | base_support_side |
| **base_support_side** | support base side | component_support_side |

---

## 9.3 Connector: fixation_interface

### Properties

```yaml
properties:
  fixation_context: transport | assembly
  method: strap | clamp | brace | unknown
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **component_fixing_side** | component fixation point/zone | fixation_tool_side |
| **fixation_tool_side** | tool/vehicle/bracing side | component_fixing_side |

---

## 9.4 Connector: access_interface

### Properties

```yaml
properties:
  access_type: assembly | inspection | connection_work
  clearance_volume_required: true
```

### Ports

| Port | Meaning | Compatible with |
|---|---|---|
| **component_access_side** | component access zone | site_access_side |
| **site_access_side** | site/workspace access | component_access_side |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: logistics.support_interface.bottom_storage
  kind: support_interface
  properties:
    support_context: storage
    orientation: lying
  ports:
    - role: component_support_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface_zone
      compatible_with:
        - logistics.support_interface.base_support_side
```

```yaml
connector:
  id: logistics.lifting_interface.top
  kind: lifting_interface
  properties:
    lifting_method: unknown
    center_of_gravity_required: true
  ports:
    - role: lifting_side
      point: lifting_candidate_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - logistics.lifting_interface.tool_side
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: logistics.access_interface.wall_top
  kind: access_interface
  properties:
    access_type: connection_work
    clearance_volume_required: true
  ports:
    - role: component_access_side
      point: center_of_wall_top_access_zone
      direction: access_direction
      abstraction: volume
      compatible_with:
        - logistics.access_interface.site_access_side
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: logistics.lifting_interface.stable_zone
  kind: lifting_interface
  properties:
    lifting_method: unknown
    center_of_gravity_required: true
  ports:
    - role: lifting_side
      point: stable_lifting_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - logistics.lifting_interface.tool_side
```

Cut face protection:

```text
stored as protection_zone property unless a protection system must attach.
```

---

# 10. Package 6 — Evidence Overlay

## Representation

```text
evidence → overlay abstraction
```

## Properties

```text
evidence type
location
confidence
affected connector
affected port
effect: ok | warning | blocked | confidence_reduced
```

## Connectors

```text
None.
```

## Ports

```text
None.
```

Evidence modifies existing connector ports.

## Evidence effect schema

```yaml
evidence_effect:
  affected_connector: string
  affected_port: string
  effect: warning | blocked | confidence_reduced
  reason: string
```

## Example A — DE_1OG_001 slab

```yaml
evidence_effect:
  affected_connector: structural.restraint_fixing.edge_left
  affected_port: structural.restraint_fixing.edge_left.fixing_side
  effect: blocked
  reason: unknown_rebar
```

## Example B — Wand–Decke

```yaml
evidence_effect:
  affected_connector: structural.bearing_support.wall_top
  affected_port: structural.bearing_support.wall_top.support_side
  effect: warning
  reason: damage_at_wall_top
```

## Example C — SlabBeamColumnFragment

```yaml
evidence_effect:
  affected_connector: structural.node_joint.beam_end
  affected_port: structural.node_joint.beam_end.joint_side
  effect: confidence_reduced
  reason: crack_near_beam_column_zone
```

---

# 11. Final Rule

```text
Connector = typed relation feature with properties.

Port = actual socket exposed by that connector.

Compatibility = port-to-port.

Risk zones, blocked zones, thermal bridges, damage, and protection zones
are not connectors unless they expose a real connectable port.
```

This keeps the model minimal:

```text
Representation
Properties
Connectors
Ports inside connectors
Port compatibility
