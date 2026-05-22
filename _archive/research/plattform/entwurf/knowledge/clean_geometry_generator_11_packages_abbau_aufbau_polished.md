# Minimal Package Abstraction Model
## v10 — Connectors Own Ports

**Goal**  
Keep each package as simple as the structural beam example:

```text
real component
↓
abstract representation
↓
minimal properties
↓
connectors
↓
ports inside those connectors
↓
calculation / evaluation
```

**Correction**  
Ports are not independent objects.  
A port exists only as part of a connector.

```text
Wrong:
Package → Ports + Connector Rules

Correct:
Package → Connectors → Ports
```

A connector defines the relation.  
Its ports are the geometric handles used by that relation.

---

# 1. Universal Rule

Every package has only four things:

```text
1. Representation
   The simplified model used by the package.

2. Properties
   The minimum values needed for calculation.

3. Connectors
   The minimum connector types needed by the package.

4. Ports
   The connector-owned endpoints.
```

A port is always tied to one connector.

```yaml
connector:
  id: structural.bearing_support.edge_left
  kind: bearing_support
  ports:
    - role: bearing_side
      point: [x, y, z]
      direction: [dx, dy, dz]
      abstraction: surface_zone
```

---

# 2. Universal Geometry Abstractions

| Abstraction | Meaning | Example |
|---|---|---|
| **Point** | 0D reference | node, lifting point, sample point |
| **Line** | 1D axis / route | beam axis, joint line, cable route |
| **Surface** | 2D boundary | slab face, wall face, thermal face |
| **Zone** | meaningful sub-area | bearing strip, damage patch |
| **Volume** | 3D body / space | component body, opening, transport envelope |
| **Graph** | nodes + relations | structural graph, service graph |

Important:

```text
Line support = line + narrow bearing strip.
Point support = point + local bearing patch.
```

---

# 3. Minimal Connector Schema

```yaml
connector:
  id: string
  package: structural | energy | tga | semantic | logistics
  kind: string
  abstraction: point | line | surface | zone | volume | graph
  ports:
    - role: string
      point: [x, y, z]
      direction: [dx, dy, dz]
      abstraction: point | line | surface | zone | volume
      compatible_with:
        - connector_kind.port_role
  checks:
    - minimal_check
  output: pass | warning | fail | value
```

## Meaning

```text
connector.kind
= what relation is possible

connector.ports
= the exact handles where that relation can attach

checks
= the minimum tests needed before the relation can be trusted
```

---

# 4. Package Overview

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

## Connectors

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

## Representation

```text
real component → structural model
```

## Minimal abstraction

| Real component | Structural representation |
|---|---|
| beam | 1D line element |
| column | 1D vertical line element |
| slab | 2D plate surface |
| wall | 2D wall surface |
| support | point/line + bearing patch |
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

## Minimal connectors

Only four structural connector types are needed at this abstraction level.

| Connector | What it represents | Port roles |
|---|---|---|
| **bearing_support** | one element bears on another | bearing_side, support_side |
| **joint_connection** | structural node / rigid or pinned relation | joint_side_a, joint_side_b |
| **anchor_connection** | fixed / restrained relation using drilled or inserted connection | anchor_side, receiving_side |
| **monolithic_continuity** | internal continuity inside one real component | continuity_side_a, continuity_side_b |

Special systems such as screws, dowels, grout, and steel supports are later mapped as variants of these connector types.

## Connector checks

| Connector | Minimal checks |
|---|---|
| **bearing_support** | overlap, direction, bearing length, capacity status |
| **joint_connection** | node alignment, rotation condition |
| **anchor_connection** | edge distance, rebar evidence, drilling permission |
| **monolithic_continuity** | internal only, evidence confidence |

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

```yaml
connector:
  id: structural.bearing_support.edge_left
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - role: bearing_side
      point: midpoint_of_left_edge_bearing_strip
      direction: downward_or_support_normal
      abstraction: surface_zone
      compatible_with:
        - bearing_support.support_side
  checks:
    - bearing_overlap
    - bearing_length
    - alignment
```

### Connector: anchor_connection

```yaml
connector:
  id: structural.anchor_connection.edge_left
  kind: anchor_connection
  abstraction: surface_zone
  ports:
    - role: anchor_side
      point: center_of_anchor_zone
      direction: drilling_axis
      abstraction: surface_zone
      compatible_with:
        - anchor_connection.receiving_side
  checks:
    - edge_distance
    - rebar_evidence
    - drilling_permission
```

### Explanation

The slab does not need many structural connectors.  
At minimum it needs:

```text
bearing_support
anchor_connection, only if restraint / fixing is needed
```

For Abbau/Aufbau this can later map to systems such as:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

---

## Example B — Wand–Decke

### Representation

```text
wall → 2D wall surface + top support strip
slab → 2D plate surface + edge bearing strip
```

### Connector: bearing_support

On wall:

```yaml
connector:
  id: structural.bearing_support.wall_top
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - role: support_side
      point: midpoint_of_wall_top_strip
      direction: upward
      abstraction: line_plus_surface_strip
      compatible_with:
        - bearing_support.bearing_side
```

On slab:

```yaml
connector:
  id: structural.bearing_support.slab_edge
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - role: bearing_side
      point: midpoint_of_slab_edge_strip
      direction: downward_or_edge_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - bearing_support.support_side
```

### Connector: anchor_connection

```yaml
connector:
  id: structural.anchor_connection.wall_slab
  kind: anchor_connection
  abstraction: surface_zone
  ports:
    - role: anchor_side
      point: wall_anchor_zone
      direction: drilling_axis
      abstraction: surface_zone
      compatible_with:
        - anchor_connection.receiving_side
```

### Explanation

Minimal structural reading:

```text
wall supports
slab bears
optional anchor/rebar connection restrains or fixes
```

Abbau/Aufbau mapping:

```text
nachträglicher Bewehrungsanschluss + Verguss
→ bearing_support + anchor_connection

Schraubanker mit Flachstahlhalter
→ bearing_support + anchor_connection
```

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

### Connector: bearing_support

```yaml
connector:
  id: structural.bearing_support.external_slab_edge
  kind: bearing_support
  abstraction: line_plus_surface_strip
  ports:
    - role: bearing_side
      point: midpoint_of_external_slab_edge
      direction: support_normal
      abstraction: line_plus_surface_strip
      compatible_with:
        - bearing_support.support_side
```

### Connector: joint_connection

```yaml
connector:
  id: structural.joint_connection.beam_end
  kind: joint_connection
  abstraction: point_or_surface_patch
  ports:
    - role: joint_side_a
      point: center_of_beam_cut_end
      direction: beam_axis
      abstraction: surface_patch
      compatible_with:
        - joint_connection.joint_side_b
```

### Connector: monolithic_continuity

```yaml
connector:
  id: structural.monolithic_continuity.slab_beam
  kind: monolithic_continuity
  abstraction: volume_zone
  ports:
    - role: continuity_side_a
      point: centroid_of_slab_beam_junction
      direction: beam_axis
      abstraction: volume_zone
      compatible_with:
        - monolithic_continuity.continuity_side_b
```

### Explanation

The fragment is one real component, not three connected pieces.  
Internal continuity connectors describe what is already monolithic.  
Only external connectors are used to connect to other components.

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

## Minimal connectors

| Connector | What it represents | Port roles |
|---|---|---|
| **thermal_continuity** | two thermal boundary surfaces continue | boundary_side_a, boundary_side_b |
| **insulation_continuity** | insulation layer continues | insulation_side_a, insulation_side_b |
| **thermal_bridge_warning** | edge/joint/protrusion creates bridge risk | bridge_source |
| **penetration_sealing** | opening or crossing through envelope | penetration_side, sealing_side |

## Connector checks

| Connector | Minimal checks |
|---|---|
| **thermal_continuity** | boundary side, alignment |
| **insulation_continuity** | layer continuity |
| **thermal_bridge_warning** | bridge risk condition |
| **penetration_sealing** | sealing required |

---

## Example A — DE_1OG_001 slab

If used as roof or exterior floor:

```yaml
connector:
  id: energy.thermal_continuity.top
  kind: thermal_continuity
  abstraction: surface
  ports:
    - role: boundary_side_a
      point: center_of_top_surface
      direction: exterior_normal
      abstraction: surface
      compatible_with:
        - thermal_continuity.boundary_side_b
```

```yaml
connector:
  id: energy.thermal_bridge_warning.edge_left
  kind: thermal_bridge_warning
  abstraction: line_zone
  ports:
    - role: bridge_source
      point: midpoint_of_slab_edge
      direction: exterior_normal
      abstraction: line_zone
      compatible_with: []
```

Explanation:

```text
Interior slab: no active energy connectors needed.
Envelope slab: thermal surface and edge bridge connectors are enough.
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: energy.thermal_bridge_warning.wall_slab_joint
  kind: thermal_bridge_warning
  abstraction: line_zone
  ports:
    - role: bridge_source
      point: midpoint_of_joint
      direction: exterior_normal
      abstraction: line_zone
      compatible_with: []
```

```yaml
connector:
  id: energy.insulation_continuity.wall_side
  kind: insulation_continuity
  abstraction: surface
  ports:
    - role: insulation_side_a
      point: center_of_insulation_side
      direction: exterior_normal
      abstraction: surface
      compatible_with:
        - insulation_continuity.insulation_side_b
```

Explanation:

```text
The energy model only needs to know whether insulation continues
and whether the wall-slab joint creates a thermal bridge.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: energy.thermal_bridge_warning.beam_projection
  kind: thermal_bridge_warning
  abstraction: zone
  ports:
    - role: bridge_source
      point: centroid_of_beam_projection
      direction: exterior_normal
      abstraction: zone
      compatible_with: []
```

```yaml
connector:
  id: energy.penetration_sealing.cut_face
  kind: penetration_sealing
  abstraction: surface_zone
  ports:
    - role: penetration_side
      point: center_of_cut_face
      direction: cut_face_normal
      abstraction: surface_zone
      compatible_with:
        - penetration_sealing.sealing_side
```

Explanation:

```text
The fragment only needs risk connectors for protrusions and cut faces.
Full thermal calculation comes later.
```

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

## Minimal connectors

| Connector | What it represents | Port roles |
|---|---|---|
| **route_continuity** | service route continues | route_side_a, route_side_b |
| **opening_use** | existing opening used by service | opening_side, service_side |
| **core_drilling_use** | new drilling used by service | drilling_side, service_side |
| **blocked_conflict** | service conflicts with blocked zone | blocked_side |

## Connector checks

| Connector | Minimal checks |
|---|---|
| **route_continuity** | alignment, diameter/corridor |
| **opening_use** | size, axis |
| **core_drilling_use** | edge distance, rebar evidence |
| **blocked_conflict** | overlap with blocked zone |

---

## Example A — DE_1OG_001 slab

No existing opening is recorded. Candidate only if needed:

```yaml
connector:
  id: tga.core_drilling_use.candidate_01
  kind: core_drilling_use
  abstraction: cylinder
  ports:
    - role: drilling_side
      point: candidate_center
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - core_drilling_use.service_side
  checks:
    - edge_distance
    - rebar_evidence
```

Explanation:

```text
The slab does not automatically allow drilling.
The connector only marks where drilling could be checked.
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: tga.route_continuity.wall_top
  kind: route_continuity
  abstraction: line_corridor
  ports:
    - role: route_side_a
      point: route_control_point
      direction: horizontal_route_direction
      abstraction: line_corridor
      compatible_with:
        - route_continuity.route_side_b
```

```yaml
connector:
  id: tga.blocked_conflict.bearing_joint
  kind: blocked_conflict
  abstraction: zone
  ports:
    - role: blocked_side
      point: center_of_bearing_joint
      direction: joint_normal
      abstraction: zone
      compatible_with: []
```

Explanation:

```text
The service model needs only a route connector and a blocked joint connector.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: tga.core_drilling_use.slab_zone
  kind: core_drilling_use
  abstraction: cylinder
  ports:
    - role: drilling_side
      point: safe_slab_zone_point
      direction: drilling_axis
      abstraction: cylinder
      compatible_with:
        - core_drilling_use.service_side
```

```yaml
connector:
  id: tga.blocked_conflict.beam_zone
  kind: blocked_conflict
  abstraction: volume_zone
  ports:
    - role: blocked_side
      point: center_of_beam_zone
      direction: beam_axis
      abstraction: volume_zone
      compatible_with: []
```

Explanation:

```text
The service model keeps only possible route/drilling zones and blocked structural zones.
```

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

## Minimal connectors

| Connector | What it represents | Port roles |
|---|---|---|
| **boundary_alignment** | room boundaries align / continue | boundary_side_a, boundary_side_b |
| **joint_alignment** | visible joints align | joint_side_a, joint_side_b |
| **grid_continuity** | grid/module continues | grid_side_a, grid_side_b |
| **visibility_relation** | reuse expression / identity relation | visible_side, identity_side |

## Connector checks

| Connector | Minimal checks |
|---|---|
| **boundary_alignment** | coplanarity, adjacency |
| **joint_alignment** | line alignment |
| **grid_continuity** | spacing, direction |
| **visibility_relation** | visibility preference, surface condition |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: semantic.visibility_relation.bottom
  kind: visibility_relation
  abstraction: surface
  ports:
    - role: visible_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface
      compatible_with:
        - visibility_relation.identity_side
```

```yaml
connector:
  id: semantic.grid_continuity.width
  kind: grid_continuity
  abstraction: line
  ports:
    - role: grid_side_a
      point: midpoint_of_reference_edge
      direction: grid_direction
      abstraction: line
      compatible_with:
        - grid_continuity.grid_side_b
```

Explanation:

```text
The semantic model keeps the visible underside and the grid direction.
It does not need all geometry.
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: semantic.boundary_alignment.wall_face
  kind: boundary_alignment
  abstraction: surface
  ports:
    - role: boundary_side_a
      point: center_of_wall_face
      direction: room_side_normal
      abstraction: surface
      compatible_with:
        - boundary_alignment.boundary_side_b
```

```yaml
connector:
  id: semantic.joint_alignment.wall_slab
  kind: joint_alignment
  abstraction: line
  ports:
    - role: joint_side_a
      point: midpoint_of_joint
      direction: joint_direction
      abstraction: line
      compatible_with:
        - joint_alignment.joint_side_b
```

Explanation:

```text
Only two architectural relations are needed:
room boundary and joint alignment.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: semantic.visibility_relation.monolithic_junction
  kind: visibility_relation
  abstraction: zone
  ports:
    - role: visible_side
      point: centroid_of_visible_junction
      direction: viewing_normal
      abstraction: zone
      compatible_with:
        - visibility_relation.identity_side
```

```yaml
connector:
  id: semantic.grid_continuity.original_bay
  kind: grid_continuity
  abstraction: line
  ports:
    - role: grid_side_a
      point: original_bay_reference_point
      direction: original_grid_direction
      abstraction: line
      compatible_with:
        - grid_continuity.grid_side_b
```

Explanation:

```text
The fragment’s architectural value is the visible former structural bay.
The model only keeps visibility and grid connectors.
```

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

## Minimal connectors

| Connector | What it represents | Port roles |
|---|---|---|
| **lifting_check** | component can be lifted | lifting_side, tool_side |
| **storage_check** | component can be stored | component_support_side, storage_base_side |
| **transport_check** | component can be transported/fixed | component_fixing_side, vehicle_side |
| **access_check** | assembly access exists | component_access_side, site_access_side |
| **protection_check** | fragile area needs protection | fragile_side, protection_side |

## Connector checks

| Connector | Minimal checks |
|---|---|
| **lifting_check** | mass, center of gravity, evidence |
| **storage_check** | orientation, support spacing |
| **transport_check** | envelope, fixation |
| **access_check** | clearance |
| **protection_check** | exposed/damaged surface |

---

## Example A — DE_1OG_001 slab

```yaml
connector:
  id: logistics.storage_check.bottom
  kind: storage_check
  abstraction: surface_zone
  ports:
    - role: component_support_side
      point: center_of_bottom_face
      direction: downward_normal
      abstraction: surface_zone
      compatible_with:
        - storage_check.storage_base_side
```

```yaml
connector:
  id: logistics.lifting_check.top
  kind: lifting_check
  abstraction: point_or_zone
  ports:
    - role: lifting_side
      point: lifting_candidate_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - lifting_check.tool_side
```

Explanation:

```text
The slab logistics model needs storage and lifting connectors.
Transport can use the same body envelope and fixing connector if needed.
```

---

## Example B — Wand–Decke

```yaml
connector:
  id: logistics.access_check.wall_top
  kind: access_check
  abstraction: clearance_volume
  ports:
    - role: component_access_side
      point: center_of_wall_top_access_zone
      direction: access_direction
      abstraction: volume
      compatible_with:
        - access_check.site_access_side
```

```yaml
connector:
  id: logistics.lifting_check.slab_placement
  kind: lifting_check
  abstraction: point
  ports:
    - role: lifting_side
      point: slab_lifting_reference
      direction: upward
      abstraction: point
      compatible_with:
        - lifting_check.tool_side
```

Explanation:

```text
Only access and lifting connectors are needed for this interface.
```

---

## Example C — SlabBeamColumnFragment

```yaml
connector:
  id: logistics.lifting_check.stable_zone
  kind: lifting_check
  abstraction: point_or_zone
  ports:
    - role: lifting_side
      point: stable_lifting_point
      direction: upward
      abstraction: point_or_zone
      compatible_with:
        - lifting_check.tool_side
```

```yaml
connector:
  id: logistics.protection_check.cut_face
  kind: protection_check
  abstraction: surface_zone
  ports:
    - role: fragile_side
      point: center_of_cut_face
      direction: cut_face_normal
      abstraction: surface_zone
      compatible_with:
        - protection_check.protection_side
```

Explanation:

```text
The fragment needs lifting and protection connectors because it has irregular mass and cut faces.
```

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
affected port role
effect: ok | warning | blocked | confidence_reduced
```

## Connectors

Evidence has no design connectors of its own.  
It modifies connectors from other packages.

## Minimal rule

```text
evidence_effect
```

## Evidence effect schema

```yaml
evidence_effect:
  id: string
  affected_connector: string
  affected_port_role: string
  effect: warning | blocked | confidence_reduced
  reason: string
```

## Example A — DE_1OG_001 slab

```yaml
evidence_effect:
  affected_connector: structural.anchor_connection.edge_left
  affected_port_role: anchor_side
  effect: blocked
  reason: unknown_rebar
```

```yaml
evidence_effect:
  affected_connector: logistics.lifting_check.top
  affected_port_role: lifting_side
  effect: warning
  reason: spalling_near_lifting_zone
```

## Example B — Wand–Decke

```yaml
evidence_effect:
  affected_connector: structural.anchor_connection.wall_slab
  affected_port_role: anchor_side
  effect: blocked
  reason: rebar_conflict
```

```yaml
evidence_effect:
  affected_connector: structural.bearing_support.wall_top
  affected_port_role: support_side
  effect: warning
  reason: damage_at_wall_top
```

## Example C — SlabBeamColumnFragment

```yaml
evidence_effect:
  affected_connector: structural.monolithic_continuity.slab_beam
  affected_port_role: continuity_side_a
  effect: confidence_reduced
  reason: crack_near_junction
```

```yaml
evidence_effect:
  affected_connector: structural.anchor_connection.cut_face
  affected_port_role: anchor_side
  effect: blocked
  reason: unknown_rebar_at_cut_face
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
listed only inside each connector

Example:
representation + connector + connector-owned ports + explanation
```

Final rule:

```text
No standalone ports.
Every port belongs to a connector.
