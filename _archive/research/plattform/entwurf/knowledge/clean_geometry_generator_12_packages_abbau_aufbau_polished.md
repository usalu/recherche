# Minimal Package Abstraction Model
## v11 — Ports as the Actual Connectable Sockets

**Goal**  
Keep the system minimal and clear:

```text
real component
↓
package abstraction
↓
minimal properties
↓
connector
↓
port(s)
↓
port-to-port compatibility
↓
calculation / evaluation
```

---

# 1. Correct Core Concept

## 1.1 Connector vs Port

```text
Connector = the connection feature or behavior on a component.

Port = the actual exposed socket / handle where another element can connect.
```

A connector can expose one or more ports.

```text
Connector
└── Port(s)
```

Two components do not connect because their connector names are similar.  
They connect because one connector exposes a port that is compatible with a port exposed by another connector.

```text
Component A connector → Port A
Component B connector → Port B

Port A compatible with Port B
↓
connection can be checked
```

---

# 2. Minimal Data Model

## 2.1 Component hierarchy

```text
Component
│
├── Package
│   ├── Representation
│   ├── Properties
│   └── Connectors
│       └── Ports
```

## 2.2 Connector

A connector describes **what kind of relation this component can offer**.

```yaml
connector:
  id: structural.bearing_support.edge_left
  package: structural
  kind: bearing_support
  abstraction: line_plus_surface_strip
  checks:
    - bearing_overlap
    - bearing_length
    - direction
  ports: []
```

## 2.3 Port

A port is the **actual connectable socket**.

```yaml
port:
  id: structural.bearing_support.edge_left.bearing_side
  role: bearing_side
  point: [x, y, z]
  direction: [dx, dy, dz]
  abstraction: surface_zone
  compatible_with:
    - structural.bearing_support.support_side
```

## 2.4 Connection

A connection is created when two compatible ports meet.

```yaml
connection:
  from: component_A.structural.bearing_support.edge_left.bearing_side
  to: component_B.structural.bearing_support.wall_top.support_side
```

Then the connector checks are applied.

---

# 3. Universal Rule

For every package, ask only:

```text
1. What is the abstract representation?
2. What minimal properties are needed?
3. Which connectors exist?
4. Which ports do these connectors expose?
5. Which ports are compatible?
```

---

# 4. Geometry Abstractions

| Abstraction | Meaning | Example |
|---|---|---|
| **Point** | 0D reference | node, lifting point |
| **Line** | 1D axis / route | beam axis, joint line |
| **Surface** | 2D boundary | wall face, slab face |
| **Zone** | meaningful sub-area | bearing strip, damage patch |
| **Volume** | 3D body / space | opening, transport envelope |
| **Graph** | nodes + relations | structural graph, route graph |

Important:

```text
Line support = line + narrow bearing strip.
Point support = point + local bearing patch.
```

---

# 5. Package 0 — Base Geometry

## Representation

```text
real component → simplified geometric body
```

## Minimal properties

```text
dimensions
volume
main faces
main edges
openings
center point
```

## Connectors and ports

```text
None.
```

Base Geometry creates no connectors and no ports.

## Example A — Abbau/Aufbau slab DE_1OG_001

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
→ composite volume
→ slab zone
→ beam zone
→ column-stub zone
→ cut faces
→ center point
```

---

# 6. Package 1 — Structural

## Representation

```text
real component → structural model
```

## Minimal abstraction

| Real component | Structural abstraction |
|---|---|
| beam | 1D line element |
| column | 1D vertical line element |
| slab | 2D plate surface |
| wall | 2D wall surface |
| local support | point/line + bearing patch |
| monolithic fragment | graph of line/surface elements + continuity zones |

## Minimal properties

```text
role
span direction
section / thickness
material
support zones
capacity status: known | unknown
evidence status
```

## Minimal connectors and ports

| Connector | What it means | Ports it exposes |
|---|---|---|
| **bearing_support** | one element bears on / supports another | bearing_side, support_side |
| **joint_connection** | two structural nodes or ends meet | joint_side_a, joint_side_b |
| **anchor_connection** | restrained/fixed drilled or inserted connection | anchor_side, receiving_side |
| **monolithic_continuity** | internal continuity inside one real component | continuity_side_a, continuity_side_b |

## Port compatibility

| Port | Compatible with |
|---|---|
| bearing_side | support_side |
| support_side | bearing_side |
| joint_side_a | joint_side_b |
| anchor_side | receiving_side |
| receiving_side | anchor_side |
| continuity_side_a | continuity_side_b, internal only |

## Connector checks

| Connector | Minimal checks |
|---|---|
| bearing_support | overlap, direction, bearing length, capacity status |
| joint_connection | node alignment, rotation condition |
| anchor_connection | edge distance, rebar evidence, drilling permission |
| monolithic_continuity | internal only, evidence confidence |

---

## Example A — DE_1OG_001 slab

### Representation

```text
real slab
→ 2D plate surface
→ edge lines
→ bearing strips at usable edges
```

### Connector: bearing_support

The slab edge can expose a **bearing_side** port.

```yaml
connector:
  id: structural.bearing_support.edge_left
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - id: structural.bearing_support.edge_left.bearing_side
      role: bearing_side
      point: midpoint_of_left_edge_bearing_strip
      direction: downward_or_support_normal
      abstraction: surface_zone
      compatible_with:
        - structural.bearing_support.support_side
```

### Connector: anchor_connection

Only needed if the slab must be fixed, restrained, or tied.

```yaml
connector:
  id: structural.anchor_connection.edge_left
  kind: anchor_connection
  abstraction: surface_zone
  ports:
    - id: structural.anchor_connection.edge_left.anchor_side
      role: anchor_side
      point: center_of_anchor_zone
      direction: drilling_axis
      abstraction: surface_zone
      compatible_with:
        - structural.anchor_connection.receiving_side
```

### Explanation

The port is the connectable part:

```text
bearing_support.edge_left.bearing_side
```

Another element must expose:

```text
bearing_support.support_side
```

Only then can the structural bearing connector be checked.

---

## Example B — Wand–Decke

### Representation

```text
wall → 2D wall surface + top support strip
slab → 2D plate surface + edge bearing strip
```

### Wall connector

```yaml
connector:
  id: structural.bearing_support.wall_top
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - id: structural.bearing_support.wall_top.support_side
      role: support_side
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
  abstraction: line_plus_surface_strip
  ports:
    - id: structural.bearing_support.slab_edge.bearing_side
      role: bearing_side
      point: midpoint_of_slab_edge_strip
      direction: downward_or_edge_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
```

### Port-to-port connection

```text
slab_edge.bearing_side
↔
wall_top.support_side
```

### Abbau/Aufbau system mapping

The same port connection can later be realized by connector systems such as:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

The system is selected later.  
The ports only define that the slab edge can connect to the wall top.

---

## Example C — SlabBeamColumnFragment

### Representation

```text
one real monolithic fragment
→ structural graph

slab zone → 2D plate surface
beam zone → 1D beam line + section
column stub → 1D column line
internal junctions → continuity zones
external cut faces → risk/support surfaces
```

### External bearing connector

```yaml
connector:
  id: structural.bearing_support.external_slab_edge
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - id: structural.bearing_support.external_slab_edge.bearing_side
      role: bearing_side
      point: midpoint_of_external_slab_edge
      direction: support_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - structural.bearing_support.support_side
```

### Internal continuity connector

```yaml
connector:
  id: structural.monolithic_continuity.slab_beam
  kind: monolithic_continuity
  abstraction: volume_zone
  ports:
    - id: structural.monolithic_continuity.slab_beam.continuity_side_a
      role: continuity_side_a
      point: centroid_of_slab_beam_junction
      direction: beam_axis
      abstraction: volume_zone
      compatible_with:
        - structural.monolithic_continuity.continuity_side_b
```

### Explanation

External connector ports are for other elements.  
Internal continuity ports are only internal references that describe the monolithic relation.

---

# 7. Package 2 — Energy / Envelope

## Representation

```text
real component → thermal boundary model
```

## Minimal properties

```text
thermal side: interior | exterior | ground | roof
area
thickness
lambda
assembly status: known | unknown
```

## Minimal connectors and ports

| Connector | What it means | Ports it exposes |
|---|---|---|
| **thermal_continuity** | two thermal surfaces continue | boundary_side_a, boundary_side_b |
| **insulation_continuity** | insulation layer continues | insulation_side_a, insulation_side_b |
| **thermal_bridge_warning** | edge/joint/protrusion creates risk | bridge_source |
| **penetration_sealing** | opening/crossing through envelope | penetration_side, sealing_side |

## Port compatibility

| Port | Compatible with |
|---|---|
| boundary_side_a | boundary_side_b |
| insulation_side_a | insulation_side_b |
| bridge_source | none; warning source |
| penetration_side | sealing_side |
| sealing_side | penetration_side |

---

## Example A — DE_1OG_001 slab

If the slab is part of the envelope:

```yaml
connector:
  id: energy.thermal_continuity.top
  kind: thermal_continuity
  abstraction: surface
  ports:
    - id: energy.thermal_continuity.top.boundary_side_a
      role: boundary_side_a
      point: center_of_top_surface
      direction: exterior_normal
      abstraction: surface
      compatible_with:
        - energy.thermal_continuity.boundary_side_b
```

Thermal bridge warning:

```yaml
connector:
  id: energy.thermal_bridge_warning.edge_left
  kind: thermal_bridge_warning
  abstraction: line_zone
  ports:
    - id: energy.thermal_bridge_warning.edge_left.bridge_source
      role: bridge_source
      point: midpoint_of_slab_edge
      direction: exterior_normal
      abstraction: line_zone
      compatible_with: []
```

### Explanation

The top surface port can connect to another thermal boundary.  
The edge bridge port does not connect to another port; it marks a risk source.

---

## Example B — Wand–Decke

```yaml
connector:
  id: energy.insulation_continuity.wall_side
  kind: insulation_continuity
  abstraction: surface
  ports:
    - id: energy.insulation_continuity.wall_side.insulation_side_a
      role: insulation_side_a
      point: center_of_insulation_side
      direction: exterior_normal
      abstraction: surface
      compatible_with:
        - energy.insulation_continuity.insulation_side_b
```

```yaml
connector:
  id: energy.thermal_bridge_warning.wall_slab_joint
  kind: thermal_bridge_warning
  abstraction: line_zone
  ports:
    - id: energy.thermal_bridge_warning.wall_slab_joint.bridge_source
      role: bridge_source
      point: midpoint_of_joint
      direction: exterior_normal
      abstraction: line_zone
      compatible_with: []
```

### Explanation

The insulation port connects to another insulation port.  
The bridge port is a risk marker.

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: energy.thermal_bridge_warning.beam_projection
  kind: thermal_bridge_warning
  abstraction: zone
  ports:
    - id: energy.thermal_bridge_warning.beam_projection.bridge_source
      role: bridge_source
      point: centroid_of_beam_projection
      direction: exterior_normal
      abstraction: zone
      compatible_with: []
```

### Explanation

The fragment exposes thermal risk ports at protrusions and cut faces.  
Only ports that represent layer continuity should be connectable.

---

# 8. Package 3 — TGA / Openings

## Representation

```text
real component → service route / opening model
```

## Minimal properties

```text
opening size
route diameter
axis direction
edge distance
blocked status
```

## Minimal connectors and ports

| Connector | What it means | Ports it exposes |
|---|---|---|
| **route_continuity** | service route continues | route_side_a, route_side_b |
| **opening_use** | existing opening used by service | opening_side, service_side |
| **core_drilling_use** | new drilling used by service | drilling_side, service_side |
| **blocked_conflict** | service conflicts with blocked zone | blocked_side |

## Port compatibility

| Port | Compatible with |
|---|---|
| route_side_a | route_side_b |
| opening_side | service_side |
| drilling_side | service_side |
| service_side | opening_side, drilling_side |
| blocked_side | none; conflict marker |

---

## Example A — DE_1OG_001 slab

No existing opening is recorded. Candidate only if needed:

```yaml
connector:
  id: tga.core_drilling_use.candidate_01
  kind: core_drilling_use
  abstraction: cylinder
  ports:
    - id: tga.core_drilling_use.candidate_01.drilling_side
      role: drilling_side
      point: candidate_center
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - tga.core_drilling_use.service_side
```

### Explanation

The drilling-side port does not mean drilling is allowed.  
It only means another service-side port can try to use it, then checks are applied.

---

## Example B — Wand–Decke

```yaml
connector:
  id: tga.route_continuity.wall_top
  kind: route_continuity
  abstraction: line_corridor
  ports:
    - id: tga.route_continuity.wall_top.route_side_a
      role: route_side_a
      point: route_control_point
      direction: horizontal_route_direction
      abstraction: line_corridor
      compatible_with:
        - tga.route_continuity.route_side_b
```

Blocked zone:

```yaml
connector:
  id: tga.blocked_conflict.bearing_joint
  kind: blocked_conflict
  abstraction: zone
  ports:
    - id: tga.blocked_conflict.bearing_joint.blocked_side
      role: blocked_side
      point: center_of_bearing_joint
      direction: joint_normal
      abstraction: zone
      compatible_with: []
```

### Explanation

One port allows route continuation.  
The blocked port is not compatible with anything; it only prevents routes.

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: tga.core_drilling_use.slab_zone
  kind: core_drilling_use
  abstraction: cylinder
  ports:
    - id: tga.core_drilling_use.slab_zone.drilling_side
      role: drilling_side
      point: safe_slab_zone_point
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - tga.core_drilling_use.service_side
```

### Explanation

The service connector belongs to the slab zone only.  
Beam and column zones should expose blocked ports if they are not usable for services.

---

# 9. Package 4 — Semantic / Architectural

## Representation

```text
real component → spatial / visual relation model
```

## Minimal properties

```text
visible side
room side
joint line
grid direction
identity zone
condition status
```

## Minimal connectors and ports

| Connector | What it means | Ports it exposes |
|---|---|---|
| **boundary_alignment** | room boundaries align / continue | boundary_side_a, boundary_side_b |
| **joint_alignment** | visible joints align | joint_side_a, joint_side_b |
| **grid_continuity** | grid/module continues | grid_side_a, grid_side_b |
| **visibility_relation** | reuse expression / identity relation | visible_side, identity_side |

## Port compatibility

| Port | Compatible with |
|---|---|
| boundary_side_a | boundary_side_b |
| joint_side_a | joint_side_b |
| grid_side_a | grid_side_b |
| visible_side | identity_side, visible_side |
| identity_side | visible_side, identity_side |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: semantic.visibility_relation.bottom
  kind: visibility_relation
  abstraction: surface
  ports:
    - id: semantic.visibility_relation.bottom.visible_side
      role: visible_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface
      compatible_with:
        - semantic.visibility_relation.identity_side
        - semantic.visibility_relation.visible_side
```

```yaml
connector:
  id: semantic.grid_continuity.width
  kind: grid_continuity
  abstraction: line
  ports:
    - id: semantic.grid_continuity.width.grid_side_a
      role: grid_side_a
      point: midpoint_of_reference_edge
      direction: grid_direction
      abstraction: line
      compatible_with:
        - semantic.grid_continuity.grid_side_b
```

### Explanation

The visible underside can relate to reuse identity or another visible reuse zone.  
The grid port connects only to another grid port.

---

## Example B — Wand–Decke

```yaml
connector:
  id: semantic.boundary_alignment.wall_face
  kind: boundary_alignment
  abstraction: surface
  ports:
    - id: semantic.boundary_alignment.wall_face.boundary_side_a
      role: boundary_side_a
      point: center_of_wall_face
      direction: room_side_normal
      abstraction: surface
      compatible_with:
        - semantic.boundary_alignment.boundary_side_b
```

```yaml
connector:
  id: semantic.joint_alignment.wall_slab
  kind: joint_alignment
  abstraction: line
  ports:
    - id: semantic.joint_alignment.wall_slab.joint_side_a
      role: joint_side_a
      point: midpoint_of_joint
      direction: joint_direction
      abstraction: line
      compatible_with:
        - semantic.joint_alignment.joint_side_b
```

### Explanation

The wall face exposes a boundary port.  
The wall-slab joint exposes a joint alignment port.

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: semantic.visibility_relation.monolithic_junction
  kind: visibility_relation
  abstraction: zone
  ports:
    - id: semantic.visibility_relation.monolithic_junction.visible_side
      role: visible_side
      point: centroid_of_visible_junction
      direction: viewing_normal
      abstraction: zone
      compatible_with:
        - semantic.visibility_relation.identity_side
        - semantic.visibility_relation.visible_side
```

### Explanation

The fragment exposes visible reuse ports at the monolithic junction and cut faces.  
These ports connect only to semantic visibility or identity relations.

---

# 10. Package 5 — Logistics / Assembly

## Representation

```text
real component → handling model
```

## Minimal properties

```text
mass
transport dimensions
center of gravity
storage orientation
lifting status
access clearance
protection zones
```

## Minimal connectors and ports

| Connector | What it means | Ports it exposes |
|---|---|---|
| **lifting_check** | component can be lifted | lifting_side, tool_side |
| **storage_check** | component can be stored | component_support_side, storage_base_side |
| **transport_check** | component can be transported/fixed | component_fixing_side, vehicle_side |
| **access_check** | assembly access exists | component_access_side, site_access_side |
| **protection_check** | fragile area needs protection | fragile_side, protection_side |

## Port compatibility

| Port | Compatible with |
|---|---|
| lifting_side | tool_side |
| component_support_side | storage_base_side |
| component_fixing_side | vehicle_side |
| component_access_side | site_access_side |
| fragile_side | protection_side |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: logistics.storage_check.bottom
  kind: storage_check
  abstraction: surface_zone
  ports:
    - id: logistics.storage_check.bottom.component_support_side
      role: component_support_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface_zone
      compatible_with:
        - logistics.storage_check.storage_base_side
```

```yaml
connector:
  id: logistics.lifting_check.top
  kind: lifting_check
  abstraction: point_or_zone
  ports:
    - id: logistics.lifting_check.top.lifting_side
      role: lifting_side
      point: lifting_candidate_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - logistics.lifting_check.tool_side
```

### Explanation

The slab exposes a storage support port and a lifting port.  
Only matching logistics tool/base ports can connect.

---

## Example B — Wand–Decke

```yaml
connector:
  id: logistics.access_check.wall_top
  kind: access_check
  abstraction: clearance_volume
  ports:
    - id: logistics.access_check.wall_top.component_access_side
      role: component_access_side
      point: center_of_wall_top_access_zone
      direction: access_direction
      abstraction: volume
      compatible_with:
        - logistics.access_check.site_access_side
```

### Explanation

The access port says the wall top must remain reachable during assembly.

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: logistics.lifting_check.stable_zone
  kind: lifting_check
  abstraction: point_or_zone
  ports:
    - id: logistics.lifting_check.stable_zone.lifting_side
      role: lifting_side
      point: stable_lifting_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - logistics.lifting_check.tool_side
```

```yaml
connector:
  id: logistics.protection_check.cut_face
  kind: protection_check
  abstraction: surface_zone
  ports:
    - id: logistics.protection_check.cut_face.fragile_side
      role: fragile_side
      point: center_of_cut_face
      direction: cut_face_normal
      abstraction: surface_zone
      compatible_with:
        - logistics.protection_check.protection_side
```

### Explanation

The fragment exposes handling ports only where handling or protection is needed.

---

# 11. Package 6 — Evidence Overlay

## Representation

```text
evidence → overlay model
```

## Minimal properties

```text
evidence type
location
confidence
affected connector
affected port
effect: ok | warning | blocked | confidence_reduced
```

## Connectors and ports

```text
Evidence creates no design connectors and no ports.
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
  affected_connector: structural.anchor_connection.edge_left
  affected_port: structural.anchor_connection.edge_left.anchor_side
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
  affected_connector: structural.monolithic_continuity.slab_beam
  affected_port: structural.monolithic_continuity.slab_beam.continuity_side_a
  effect: confidence_reduced
  reason: crack_near_junction
```

---

# 12. Final Minimal Template

Use this template for every package:

```text
Package name

Representation:
real thing → abstract model

Properties:
only values needed for calculation

Connectors:
minimal connector types

Ports:
listed inside each connector
the actual sockets another element can connect to

Compatibility:
defined port-to-port

Example:
representation + connector + ports + explanation
```

Final rule:

```text
Ports are the actual things another element connects to.

Connectors group and define these ports.

Compatibility happens port-to-port.
