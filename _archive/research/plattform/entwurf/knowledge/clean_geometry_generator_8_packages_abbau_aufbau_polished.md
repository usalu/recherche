# Component Geometry Packages  
## v7 — Semio-Aligned Ports and Connectors

**Purpose**  
This document corrects the package structure around the actual Semio idea of **Ports / Connectors**.

The document keeps the package logic, but removes the confusing extra layer of “connector profiles.”  
In Semio, the useful concept is simpler:

```text
A Type owns connector definitions.
A Piece inherits those connectors.
A Connection links one connector on one Piece to one connector on another Piece.
```

In this document, **Port** means the conceptual connection point and **Connector** means its concrete Semio representation. They should be treated as one object:

```text
Semio Connector / Port
= ID + Point + Direction
```

---

# 1. Corrected Core Model

## 1.1 Semio hierarchy

```text
Kit
└── Type
    ├── Representation(s)
    ├── Meaning / role
    └── Connector(s) / Port(s)
        ├── ID
        ├── Point
        └── Direction

Design
└── Piece
    └── inherits Type geometry, meaning, and connectors
```

## 1.2 Correct component-package hierarchy

Each reclaimed component has several domain packages.  
Each package can produce representations.  
A representation can expose interfaces.  
Only interfaces that need connection behavior expose Semio connectors / ports.

```text
Component
│
├── Package
│   ├── Representation
│   │   ├── Interface
│   │   │   └── Semio Connector / Port
│   │   │       ├── connector_id
│   │   │       ├── point
│   │   │       └── direction
│   │   └── Geometry / quantities
│   └── Evidence / confidence
```

## 1.3 What changed from the previous version

Removed:

```text
Connector Profile
free-floating Port
generic connector generator
connector candidate as separate parallel object
```

Kept:

```text
domain packages
representations
interfaces
Semio connector / port objects
evidence effects
```

New rule:

```text
An interface may have zero, one, or more Semio connectors.

But every Semio connector belongs to a concrete interface.
```

---

# 2. Semio Connector / Port

## 2.1 Definition

A Semio Connector / Port is the minimal snap object that allows a Piece to connect to another Piece.

```yaml
semio_connector:
  id: string
  point: [x, y, z]
  direction: [dx, dy, dz]
```

## 2.2 Extended project metadata

For the reclaimed-component system, we can add metadata around the Semio connector without changing the core idea.

```yaml
semio_connector:
  id: structural.edge_bearing.long_left
  point: [x, y, z]
  direction: [dx, dy, dz]

  package: structural
  representation: structural_interface_representation
  interface_id: slab_edge_bearing_interface_left
  geometry_kind: point_on_surface_zone
  geometry_ref: Z_slab_edge_left
  kind: bearing
  confidence: medium
```

## 2.3 What the point means

The connector point is the snap reference.

| Interface geometry | Connector point should be |
|---|---|
| Surface interface | center or meaningful control point of the surface |
| Surface zone | center of the zone or repeated points along the zone |
| Line support | point on line, usually midpoint or repeated points |
| Point support | the support point |
| Opening | center of opening or axis point |
| Lifting zone | lifting point or center of lifting surface |
| Datum / grid relation | point on datum line, usually with line direction metadata |

## 2.4 What the direction means

The connector direction tells Semio how the piece should face and align when connected.

| Interface type | Direction should usually be |
|---|---|
| Bearing surface | outward normal or support direction |
| Wall top support | upward / support normal |
| Slab edge support | outward edge normal or bearing direction |
| Service opening | through-axis of opening |
| Envelope face | outward thermal / exterior normal |
| Lifting point | lifting direction |
| Datum relation | datum alignment direction |
| Grid relation | grid continuation direction |

## 2.5 Minimal connector rule

```text
Do not create connectors everywhere.

Create connectors only where a real design relation should be possible.
```

This follows the Semio logic that connectors are intentional snap points, not automatic geometry decorations.

---

# 3. Geometry Kinds

## 3.1 Point

```text
0D location
```

Used for:

```text
connector point
center of gravity
sample point
anchor reference point
lifting point
```

## 3.2 Line

```text
1D path
```

Used for:

```text
edge
axis
joint line
datum line
grid line
line support reference
```

Important:

```text
A line support is not only a mathematical line.
For checking and representation it should become:
line reference + narrow bearing surface strip.
```

## 3.3 Surface

```text
2D face
```

Used for:

```text
slab top
slab bottom
wall face
bearing surface
thermal face
visible face
storage face
```

## 3.4 Surface Zone

```text
meaningful part of a surface
```

Used for:

```text
bearing strip
anchor zone
dowel zone
visible patch
damage area
storage support area
```

## 3.5 Volume

```text
3D body
```

Used for:

```text
component body
void
opening volume
transport envelope
monolithic continuity region
grout gap
```

## 3.6 Volume Zone

```text
meaningful part of a volume
```

Used for:

```text
beam zone
slab zone
column-stub zone
monolithic junction
service corridor
clearance volume
```

---

# 4. Package Tree

```text
GEOMETRY PACKAGES
│
├── 0. Base Geometry Package
├── 1. Structural Interface Package
├── 2. Energy / Envelope Package
├── 3. TGA / Openings Package
├── 4. Semantic / Architectural Package
├── 5. Logistics / Assembly Package
└── 6. Evidence Overlay Package
```

Each package owns:

```text
its domain representation
its domain interfaces
the Semio connectors needed by those interfaces
the geometry and quantities behind them
```

---

# 5. Package 0 — Base Geometry Package

## General role

Creates neutral component geometry.  
It does not create Semio connectors.

## Representations

```text
base_solid_representation
base_face_edge_representation
base_opening_representation
base_quantity_representation
```

## Owns

| Item | Geometry kind |
|---|---|
| Component body | Volume |
| Bounding box | Volume |
| Faces | Surface |
| Edges | Line |
| Corners | Point |
| Raw openings | Void / volume |
| Raw cut-outs | Void / volume |
| Center of gravity | Point |
| Dimensions | Quantity |
| Volume | Quantity |
| Surface area | Quantity |

## Connectors

```text
None.
```

## Example A — DE_1OG_001 slab

```text
body = slab volume
faces = top, bottom, side faces
edges = long edges, short edges
dimensions = 4500 × 2300 × 180 mm
volume = 1.863 m³
center of gravity = point
```

## Example B — Wand–Decke

```text
wall body = volume
slab body = volume
wall top geometry = surface / edge region
slab edge geometry = surface / edge region
raw overlap candidate = geometric relation only
```

## Example C — SlabBeamColumnFragment

```text
body = one monolithic composite volume
sub-volume candidates = slab part, beam part, column-stub part
cut faces = surfaces
monolithic junction = volume region
center of gravity = point
```

---

# 6. Package 1 — Structural Interface Package

## General role

Creates geometry for support, bearing, load transfer, restraint, and structural connection.

## Representations

```text
structural_support_representation
structural_bearing_representation
structural_connection_representation
structural_risk_representation
```

## General interfaces

| Interface | Geometry kind |
|---|---|
| Bearing interface | Surface zone |
| Line support interface | Line + surface strip |
| Point support interface | Point + surface patch |
| Load-transfer interface | Surface or volume zone |
| Restraint interface | Line or surface zone |
| Cut-face risk interface | Surface zone |
| Monolithic continuity interface | Volume zone |

## Semio connectors / ports

Structural connectors are placed on structural interfaces.

```yaml
structural_connector:
  id: structural.<interface_kind>.<local_name>
  point: interface_control_point
  direction: interface_normal_or_load_transfer_direction
  package: structural
  kind: bearing | support | restraint | anchor | dowel | grout | steel_support | continuity
```

## Connector meaning

| Connector kind | Geometry basis | Meaning |
|---|---|---|
| bearing | surface zone | direct support/contact |
| support | line+strip or point+patch | support condition |
| anchor | surface zone + point | possible anchor point |
| dowel | point or line array | possible dowel position |
| grout | gap volume | filled/cast joint |
| steel_support | line or surface zone | steel support interface |
| continuity | volume zone | internal monolithic continuity |

## Example A — DE_1OG_001 slab

### Interfaces

```text
slab edge bearing interface
possible line support interface
anchor zone interface near edge
```

### Semio connectors

```yaml
- id: structural.bearing.edge_long_left
  point: midpoint_of_left_long_edge_bearing_strip
  direction: outward_edge_normal
  kind: bearing

- id: structural.bearing.edge_long_right
  point: midpoint_of_right_long_edge_bearing_strip
  direction: outward_edge_normal
  kind: bearing
```

Optional, only if the system wants anchorable slab edges:

```yaml
- id: structural.anchor.edge_long_left
  point: anchor_zone_control_point
  direction: drilling_axis_or_surface_normal
  kind: anchor
```

### Abbau/Aufbau connector system mapping

These Semio connectors can later be associated with system-level connection methods depending on the paired component:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

The connector system is not the Semio connector itself.  
The Semio connector is the snap / interface handle.

---

## Example B — Wand–Decke

### Interfaces

```text
wall top bearing interface
slab edge bearing interface
wall-slab load-transfer interface
grout joint interface
anchor / flat-steel-holder interface
```

### Semio connectors

```yaml
# On wall Type
- id: structural.bearing.wall_top
  point: midpoint_of_wall_top_bearing_strip
  direction: upward_normal
  kind: bearing

# On slab Type
- id: structural.bearing.slab_edge
  point: midpoint_of_slab_edge_bearing_strip
  direction: outward_edge_normal
  kind: bearing

# Optional connector-method handles
- id: structural.grout.wall_top
  point: grout_joint_control_point
  direction: joint_normal
  kind: grout

- id: structural.anchor.wall_top
  point: anchor_zone_control_point
  direction: drilling_axis
  kind: anchor
```

### Abbau/Aufbau connector system mapping

```text
Wand - Decke:
- nachträglicher Bewehrungsanschluss + Verguss
- Schraubanker mit Flachstahlhalter
```

Mapping:

```text
post-installed rebar + grout
uses:
structural.bearing.wall_top
structural.bearing.slab_edge
structural.grout.wall_top

screw anchor + flat steel holder
uses:
structural.bearing.wall_top
structural.bearing.slab_edge
structural.anchor.wall_top
```

---

## Example C — SlabBeamColumnFragment

### Interfaces

```text
external slab-edge bearing interface
external beam-end bearing interface, if beam is cut at end
external column bearing interface, depending orientation
cut-face risk interface
internal slab-beam monolithic continuity interface
internal beam-column monolithic continuity interface
```

### Semio connectors

External connectors:

```yaml
- id: structural.bearing.slab_edge_external
  point: midpoint_of_external_slab_edge_bearing_strip
  direction: outward_edge_normal
  kind: bearing

- id: structural.bearing.beam_end_external
  point: center_of_beam_end_patch
  direction: beam_axis
  kind: bearing

- id: structural.risk.cut_face
  point: center_of_cut_face
  direction: cut_face_normal
  kind: risk
```

Internal reference connectors, only if useful for documentation / internal logic:

```yaml
- id: structural.continuity.slab_beam
  point: centroid_of_slab_beam_junction
  direction: beam_axis
  kind: continuity

- id: structural.continuity.beam_column
  point: centroid_of_beam_column_junction
  direction: column_axis
  kind: continuity
```

Important:

```text
Internal continuity connectors are not assembly connectors.
They document monolithic continuity inside one component.
External interfaces are the places that can connect to other Pieces.
```

---

# 7. Package 2 — Energy / Envelope Package

## General role

Creates geometry for thermal envelope, moisture, insulation, roof, facade, ground contact, and U-value-relevant reasoning.

## Representations

```text
thermal_boundary_representation
insulation_interface_representation
thermal_bridge_representation
moisture_risk_representation
```

## General interfaces

| Interface | Geometry kind |
|---|---|
| Thermal boundary interface | Surface |
| Insulation interface | Surface |
| Roof interface | Surface |
| Ground-contact interface | Surface |
| Facade interface | Surface |
| Thermal bridge interface | Line or narrow zone |
| Envelope penetration interface | Opening / zone |
| Moisture risk interface | Surface or edge zone |

## Semio connectors / ports

Energy connectors are boundary handles, not usually physical parts.

```yaml
energy_connector:
  id: energy.<interface_kind>.<local_name>
  point: interface_control_point
  direction: exterior_or_boundary_normal
  package: energy
  kind: thermal_boundary | insulation | thermal_bridge | moisture | penetration
```

## Example A — DE_1OG_001 slab

```yaml
- id: energy.thermal_boundary.top
  point: center_of_top_face
  direction: upward_normal
  kind: thermal_boundary

- id: energy.thermal_bridge.edge_long_left
  point: midpoint_of_left_long_edge
  direction: outward_edge_normal
  kind: thermal_bridge
```

Use only if the slab participates in the envelope.

## Example B — Wand–Decke

```yaml
- id: energy.thermal_bridge.wall_slab_joint
  point: midpoint_of_wall_slab_joint_line
  direction: exterior_boundary_normal
  kind: thermal_bridge

- id: energy.insulation.wall_slab_joint
  point: insulation_interruption_control_point
  direction: exterior_normal
  kind: insulation
```

## Example C — SlabBeamColumnFragment

```yaml
- id: energy.thermal_bridge.beam_projection
  point: centroid_of_beam_projection_zone
  direction: exterior_boundary_normal
  kind: thermal_bridge

- id: energy.moisture.cut_face
  point: center_of_exposed_cut_face
  direction: cut_face_normal
  kind: moisture
```

---

# 8. Package 3 — TGA / Openings Package

## General role

Creates geometry for openings, penetrations, service routing, shafts, pipes, cables, sleeves, and core drilling.

## Representations

```text
opening_representation
penetration_representation
service_route_representation
service_conflict_representation
```

## General interfaces

| Interface | Geometry kind |
|---|---|
| Existing opening interface | Void / opening zone |
| Service penetration interface | Opening or surface zone |
| Core-drilling interface | Cylindrical volume / circular zone |
| Cable route interface | Line / corridor zone |
| Pipe route interface | Line / corridor volume |
| Shaft interface | Surface or volume zone |
| Blocked penetration interface | Surface or volume zone |

## Semio connectors / ports

```yaml
tga_connector:
  id: tga.<interface_kind>.<local_name>
  point: opening_center_or_route_control_point
  direction: opening_axis_or_route_direction
  package: tga
  kind: opening | core_drilling | cable | pipe | shaft | blocked
```

## Example A — DE_1OG_001 slab

No opening is recorded in the given catalogue entry.

Optional candidate if project context needs it:

```yaml
- id: tga.core_drilling.candidate_01
  point: candidate_drilling_center
  direction: drilling_axis
  kind: core_drilling
```

## Example B — Wand–Decke

```yaml
- id: tga.route.wall_top_horizontal
  point: route_control_point_along_wall_top
  direction: horizontal_route_direction
  kind: cable

- id: tga.blocked.bearing_joint
  point: center_of_blocked_joint_zone
  direction: joint_normal
  kind: blocked
```

## Example C — SlabBeamColumnFragment

```yaml
- id: tga.core_drilling.slab_zone
  point: safe_candidate_point_in_slab_zone
  direction: drilling_axis
  kind: core_drilling

- id: tga.blocked.beam_web
  point: center_of_beam_web_blocked_zone
  direction: beam_web_normal
  kind: blocked
```

---

# 9. Package 4 — Semantic / Architectural Package

## General role

Creates geometry for spatial, visual, facade, rhythm, alignment, identity, and reuse-expression relations.

## Representations

```text
spatial_interface_representation
visibility_representation
facade_rhythm_representation
datum_grid_representation
reuse_expression_representation
```

## General interfaces

| Interface | Geometry kind |
|---|---|
| Room-boundary interface | Surface |
| Facade-rhythm interface | Surface / line / interval |
| Visible-reuse interface | Surface or edge zone |
| Ceiling expression interface | Surface |
| Floor surface interface | Surface |
| Joint-line interface | Line |
| Datum alignment interface | Line / plane |
| Grid continuation interface | Line / spacing pattern |
| Reuse identity interface | Surface zone |

## Semio connectors / ports

Semantic connectors are relation handles.  
They are not hardware.

```yaml
semantic_connector:
  id: semantic.<interface_kind>.<local_name>
  point: interface_control_point
  direction: alignment_or_visibility_direction
  package: semantic
  kind: room_boundary | visible_reuse | datum | grid | joint | identity
```

## Example A — DE_1OG_001 slab

```yaml
- id: semantic.floor.top
  point: center_of_top_face
  direction: upward_normal
  kind: floor

- id: semantic.ceiling.bottom
  point: center_of_bottom_face
  direction: downward_normal
  kind: ceiling

- id: semantic.grid.width
  point: midpoint_of_reference_edge
  direction: grid_direction
  kind: grid
```

## Example B — Wand–Decke

```yaml
- id: semantic.room_boundary.wall_face
  point: center_of_wall_room_face
  direction: room_side_normal
  kind: room_boundary

- id: semantic.joint.wall_slab
  point: midpoint_of_wall_slab_joint
  direction: joint_line_direction
  kind: joint

- id: semantic.datum.wall_top
  point: midpoint_of_wall_top_line
  direction: datum_direction
  kind: datum
```

## Example C — SlabBeamColumnFragment

```yaml
- id: semantic.visible_reuse.monolithic_junction
  point: centroid_of_visible_junction
  direction: viewing_or_surface_normal
  kind: visible_reuse

- id: semantic.identity.cut_face
  point: center_of_cut_face
  direction: cut_face_normal
  kind: identity

- id: semantic.grid.original_bay
  point: original_bay_reference_point
  direction: original_bay_grid_direction
  kind: grid
```

---

# 10. Package 5 — Logistics / Assembly Package

## General role

Creates geometry for storage, lifting, transport, assembly access, protection, and temporary bracing.

## Representations

```text
transport_representation
storage_representation
lifting_representation
assembly_access_representation
protection_representation
temporary_stability_representation
```

## General interfaces

| Interface | Geometry kind |
|---|---|
| Transport envelope interface | Volume |
| Storage support interface | Surface zone / line strip |
| Lifting interface | Point or surface zone |
| Stacking interface | Surface zone |
| Assembly access interface | Clearance volume |
| Installation clearance interface | Volume |
| Temporary bracing interface | Surface or line zone |
| Protection interface | Surface or edge zone |

## Semio connectors / ports

```yaml
logistics_connector:
  id: logistics.<interface_kind>.<local_name>
  point: handling_or_access_control_point
  direction: lifting_access_or_support_direction
  package: logistics
  kind: lifting | storage | stacking | access | bracing | protection
```

## Example A — DE_1OG_001 slab

```yaml
- id: logistics.storage.lying_bottom
  point: center_of_bottom_face
  direction: downward_normal
  kind: storage

- id: logistics.lifting.top_candidate
  point: lifting_candidate_point_on_top
  direction: upward_lifting_direction
  kind: lifting

- id: logistics.access.edge_bearing
  point: midpoint_of_bearing_edge
  direction: access_direction
  kind: access
```

## Example B — Wand–Decke

```yaml
- id: logistics.access.wall_top
  point: midpoint_of_wall_top_access_zone
  direction: access_direction
  kind: access

- id: logistics.lifting.slab_placement
  point: slab_lifting_reference_point
  direction: lifting_direction
  kind: lifting
```

## Example C — SlabBeamColumnFragment

```yaml
- id: logistics.lifting.stable_zone
  point: stable_lifting_candidate
  direction: lifting_direction
  kind: lifting

- id: logistics.bracing.column_stub
  point: bracing_candidate_on_column_stub
  direction: bracing_direction
  kind: bracing

- id: logistics.protection.cut_face
  point: center_of_cut_face_protection_zone
  direction: cut_face_normal
  kind: protection
```

---

# 11. Package 6 — Evidence Overlay Package

## General role

Maps scans, tests, photos, documents, and inspections onto package geometry.

Evidence does not normally create Semio connectors.  
It qualifies or blocks connectors from the other packages.

## Representations

```text
reinforcement_overlay_representation
damage_overlay_representation
sample_point_representation
confidence_overlay_representation
```

## Evidence overlays

| Evidence item | Geometry kind | Effect |
|---|---|---|
| Rebar line | Line / curve | may block anchor / drilling |
| Rebar zone | Line buffer / volume zone | may block connector placement |
| Unknown rebar zone | Surface or volume zone | warning / blocked |
| Damage zone | Surface or volume zone | may block bearing, lifting, visible use |
| Crack line | Line | structural / durability warning |
| Spalling zone | Surface / edge zone | bearing / lifting / visual warning |
| Exposed rebar | Line or surface zone | durability / connection warning |
| Core sample point | Point / cylinder | evidence marker |
| Confidence zone | Zone | changes confidence of generated connectors |

## Port effects

```yaml
port_effect:
  affected_connector_id: string
  effect: ok | warning | blocked | confidence_reduced
  reason: string
  evidence_ref: string
```

## Example A — DE_1OG_001 slab

```text
unknown rebar zone
→ warns / blocks structural.anchor.edge_long_left

damage at slab edge
→ warns structural.bearing.edge_long_left

spalling at lifting region
→ warns logistics.lifting.top_candidate
```

## Example B — Wand–Decke

```text
rebar conflict
→ blocks structural.anchor.wall_top

unknown reinforcement
→ warns structural.grout.wall_top or structural.anchor.wall_top

damage at wall top
→ warns structural.bearing.wall_top

damage at slab edge
→ warns structural.bearing.slab_edge
```

## Example C — SlabBeamColumnFragment

```text
unknown rebar at monolithic junction
→ blocks nearby structural anchor connectors

cut-face damage
→ warns structural.risk.cut_face

exposed rebar
→ warns durability and structural use

cracks near beam-column junction
→ reduces confidence of structural.continuity.beam_column
```

---

# 12. Correct Component Data Shape

```yaml
component:
  id: string
  typology: string
  material: string

  packages:
    base:
      representations: []
      interfaces: []
      connectors: []

    structural:
      representations: []
      interfaces: []
      connectors: []

    energy:
      representations: []
      interfaces: []
      connectors: []

    tga:
      representations: []
      interfaces: []
      connectors: []

    semantic:
      representations: []
      interfaces: []
      connectors: []

    logistics:
      representations: []
      interfaces: []
      connectors: []

    evidence:
      representations: []
      overlays: []
      port_effects: []
```

---

# 13. Final Rule

```text
Do not separate Port and Connector into two competing concepts.

Use one Semio-aligned object:
Semio Connector / Port = ID + Point + Direction.

Every connector belongs to:
Component → Package → Representation → Interface.

Pieces inherit connectors from their Type.
Connections reference connector IDs on placed Pieces.
