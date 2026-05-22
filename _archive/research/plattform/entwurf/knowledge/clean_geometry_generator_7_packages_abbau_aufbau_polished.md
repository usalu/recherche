# Component Geometry Packages  
## v6 — Packages, Representations, Interfaces, Connector-Bound Ports

**Purpose**  
This document defines the clean data structure for geometry generator packages in a reclaimed-component design system.

**Core correction**  
Each reclaimed component has several **domain packages**.  
Each package produces one or more **representations**.  
Each representation contains **interfaces**.  
Each interface can expose **ports**.  
Ports are not free-floating: **a port is always tied to a connector profile**.

The system should therefore be structured as:

```text
Component
│
├── Package
│   ├── Representation
│   │   ├── Interface
│   │   │   ├── Connector Profile
│   │   │   │   └── Port(s)
│   │   │   └── Geometry
│   │   └── Quantities
│   └── Evidence / confidence
```

---

# 1. Minimal Source Context

This document uses Abbau/Aufbau only as a reference context for concrete examples.

Verified Abbau/Aufbau anchors:

```text
The project focuses on large-format reinforced-concrete elements:
Platte, Scheibe, Träger, Stütze.

The Bauteilkatalog contains:
ID, Elementtyp, Maße, Öffnungsmaße, Volumen, Masse,
and may include sketch, concrete investigation, and reinforcement investigation.

Example element:
DE_1OG_001
4500 × 2300 × 180 mm
1.863 m³
ca. 4.1 t

Verified Wand–Decke connector families:
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

Example C in this document is a **proposed system typology**, not a named Abbau/Aufbau handbook element.

---

# 2. Main Rule

```text
Do not create one generic connector generator.

Create domain packages.

Each package owns:
1. its representations
2. its interfaces
3. its connector profiles
4. its connector-bound ports
5. its geometry and quantities
```

A connector profile can be:

```text
physical connector profile
technical interface profile
boundary profile
semantic relation profile
logistics handling profile
```

So “connector” does not always mean a steel part or anchor.  
It means a typed relation mechanism belonging to a domain.

---

# 3. Core Terms

## 3.1 Component

A real reclaimed object in the pool.

```yaml
component:
  id: DE_1OG_001
  typology: slab
  material: reinforced_concrete
  packages: []
```

---

## 3.2 Package

A package is a domain-specific group of generated representations.

```yaml
package:
  id: structural
  name: Structural Interface Package
  representations: []
```

---

## 3.3 Representation

A representation is a domain view of the component geometry.

Examples:

```text
base solid representation
structural interface representation
thermal envelope representation
service opening representation
semantic interface representation
logistics handling representation
evidence overlay representation
```

```yaml
representation:
  id: structural_support_representation
  package: structural
  geometry_refs: []
  interfaces: []
  quantities: []
  confidence: high | medium | low
```

---

## 3.4 Interface

An interface is a domain-specific place where the component can relate to something else.

```yaml
interface:
  id: slab_edge_bearing_interface_01
  package: structural
  interface_kind: bearing_interface
  geometry_kind: surface_zone
  geometry_ref: Z-001
  connector_profiles: []
```

---

## 3.5 Connector Profile

A connector profile defines what kind of relation the interface supports.

```yaml
connector_profile:
  id: bearing_support_profile
  domain: structural
  connector_kind: bearing_support
  is_physical_connector: false
  compatible_profile_patterns: []
  ports: []
  required_evidence: []
```

Examples:

```text
bearing support profile
anchor profile
grout joint profile
thermal boundary profile
service penetration profile
lifting profile
datum alignment profile
visible reuse profile
```

---

## 3.6 Port

A port is the geometric handle of a connector profile.  
A port must always belong to a connector profile.

```yaml
port:
  id: slab_edge_bearing_port_01
  connector_profile_id: bearing_support_profile
  port_kind: bearing_surface_port
  geometry_kind: surface_zone
  geometry_ref: Z-001
  direction: normal_or_vector
  side: top | bottom | edge | face | internal | external
```

Important:

```text
No free ports.
Every port belongs to one connector profile.
```

---

# 4. Shared Geometry Kinds

| Geometry kind | Meaning | Example |
|---|---|---|
| Point | 0D location | center of gravity, sample point, local anchor point |
| Line | 1D path | edge, axis, joint line, datum |
| Surface | 2D face | wall face, slab top, bearing surface |
| Surface zone | part of a surface | bearing strip, anchor zone, visible patch |
| Volume | 3D body | component body, void, transport envelope |
| Volume zone | part of a volume | monolithic continuity zone, grout pocket |
| Distance | scalar quantity | edge distance, thickness |
| Direction / vector | orientation | span direction, port direction |

Important structural clarification:

```text
Line support = line reference + narrow surface bearing strip.
Point support = point reference + local surface patch.
Neither should be stored as a mathematical line/point only.
```

---

# 5. Package Tree

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

---

# 6. Package 0 — Base Geometry Package

## General role

Creates the neutral geometric representation of the component.

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

## Interfaces / connectors / ports

```text
None.
The Base Geometry Package creates no domain interfaces, no connector profiles, and no ports.
```

## Minimal data structure

```yaml
base_geometry_package:
  representations:
    - base_solid_representation
    - base_face_edge_representation
  interfaces: []
  connector_profiles: []
  ports: []
```

## Example A — DE_1OG_001 slab

```text
component body = slab volume
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
component body = one monolithic composite volume
sub-volume candidates = slab part, beam part, column-stub part
cut faces = surfaces
monolithic junction = volume region
center of gravity = point
```

---

# 7. Package 1 — Structural Interface Package

## General role

Creates representations for support, bearing, restraint, load transfer, and structural connection geometry.

## Representations

```text
structural_support_representation
structural_bearing_representation
structural_connector_representation
structural_risk_representation
```

## General interface types

| Interface type | Geometry kind | Meaning |
|---|---|---|
| Bearing interface | Surface zone | Direct support/contact area |
| Line support interface | Line + surface strip | Support along wall, beam, or edge |
| Point support interface | Point + surface patch | Local support at column or point bearing |
| Restraint interface | Line or surface zone | Prevents movement or rotation |
| Load-transfer interface | Surface or volume zone | Force transfer region |
| Connector placement interface | Surface zone / volume zone | Where connector profile can be placed |
| Cut-face risk interface | Surface zone | Cut or exposed structural uncertainty |
| Monolithic continuity interface | Volume zone | Internal continuity within one piece |

## Connector profiles

| Connector profile | Physical? | Typical ports |
|---|---|---|
| Bearing support profile | No | bearing surface port |
| Anchor profile | Yes | anchor point port / anchor zone port |
| Dowel profile | Yes | dowel point port / dowel line-array port |
| Post-installed rebar profile | Yes | rebar insertion port |
| Grout joint profile | Yes | grout volume port |
| Steel support profile | Yes | steel bearing port |
| Restraint profile | Maybe | restraint line / surface port |
| Monolithic continuity profile | No | internal continuity port, internal only |

## Minimal data structure

```yaml
structural_package:
  representations:
    - structural_support_representation
    - structural_connector_representation
  interfaces:
    - bearing_interface
    - line_support_interface
    - point_support_interface
  connector_profiles:
    - bearing_support_profile
    - anchor_profile
    - grout_joint_profile
  ports:
    - connector-bound ports only
```

## Example A — DE_1OG_001 slab

### Interface

```text
slab-edge bearing interface
```

Geometry:

```text
line reference + narrow surface bearing strip
```

### Connector profile → ports

```text
bearing support profile
→ slab-edge-bearing-surface-port

anchor profile, only as candidate
→ slab-edge-anchor-zone-port

post-installed rebar profile, only as candidate
→ slab-edge-rebar-insertion-port
```

### Possible system-level connector systems

Depending on the paired component:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

## Example B — Wand–Decke

### Interfaces

```text
wall top bearing interface
slab edge bearing interface
wall-slab load-transfer interface
```

Geometry:

```text
wall top = line + surface strip
slab edge = line + surface strip
load transfer = overlap of bearing strips
```

### Connector profile → ports

```text
bearing support profile
→ wall-top-bearing-port
→ slab-edge-bearing-port

post-installed rebar profile
→ wall-rebar-insertion-port
→ slab-rebar-receiving-port

grout joint profile
→ wall-slab-grout-volume-port

flat steel holder / anchor profile
→ wall-anchor-port
→ slab-holder-port
```

### Abbau/Aufbau connector systems

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

## Example C — SlabBeamColumnFragment

### Interfaces

```text
external slab-edge bearing interface
external beam-end bearing interface, if beam is cut at end
external column bearing interface, depending orientation
cut-face risk interface
internal slab-beam continuity interface
internal beam-column continuity interface
```

### Connector profile → ports

```text
bearing support profile
→ external slab-edge-bearing-port
→ beam-end-bearing-port
→ column-local-bearing-port

cut-face risk profile
→ cut-face-risk-port

monolithic continuity profile
→ internal slab-beam-continuity-port
→ internal beam-column-continuity-port
```

Important:

```text
Internal monolithic continuity ports are internal reference ports.
They are not connector ports for assembling separate pieces.
External interfaces are the places that can receive connector profiles.
```

---

# 8. Package 2 — Energy / Envelope Package

## General role

Creates representations for thermal envelope, insulation, moisture, roof, facade, ground contact, and U-value-relevant geometry.

## Representations

```text
thermal_boundary_representation
insulation_interface_representation
thermal_bridge_representation
moisture_risk_representation
```

## General interface types

| Interface type | Geometry kind | Meaning |
|---|---|---|
| Thermal boundary interface | Surface | Boundary between thermal zones |
| Insulation interface | Surface | Insulation attachment / layer side |
| Roof interface | Surface | Roof build-up relation |
| Ground-contact interface | Surface | Ground / soil relation |
| Facade interface | Surface | Exterior wall / facade relation |
| Thermal bridge interface | Line or narrow zone | Heat-loss risk |
| Envelope penetration interface | Opening / zone | Penetration through envelope |
| Moisture risk interface | Surface or edge zone | Water / condensation risk |

## Connector profiles

Energy connector profiles are usually **boundary profiles**, not hardware.

| Connector profile | Physical? | Typical ports |
|---|---|---|
| Thermal boundary profile | No | thermal face port |
| Insulation layer profile | No | insulation face port |
| Thermal bridge profile | No | thermal bridge edge port |
| Envelope penetration profile | Maybe | penetration boundary port |
| Moisture protection profile | Maybe | moisture risk port |

## Minimal data structure

```yaml
energy_package:
  representations:
    - thermal_boundary_representation
    - thermal_bridge_representation
  interfaces:
    - thermal_boundary_interface
    - insulation_interface
  connector_profiles:
    - thermal_boundary_profile
    - insulation_layer_profile
  ports:
    - connector-bound boundary ports
```

## Example A — DE_1OG_001 slab

### Interface

```text
roof interface, if used as roof
exterior-floor interface, if exposed below
interior ceiling/floor interface, if used inside
thermal bridge interface at slab edge
```

### Connector profile → ports

```text
thermal boundary profile
→ slab-thermal-face-port

insulation layer profile
→ slab-insulation-face-port

thermal bridge profile
→ slab-edge-thermal-bridge-port
```

## Example B — Wand–Decke

### Interfaces

```text
wall-slab thermal bridge interface
envelope penetration interface if connector crosses insulation
insulation interruption interface
moisture risk joint interface if exposed
```

### Connector profile → ports

```text
thermal bridge profile
→ wall-slab-thermal-bridge-port

insulation layer profile
→ wall-insulation-port
→ slab-edge-insulation-port

envelope penetration profile
→ connector-crossing-envelope-port
```

## Example C — SlabBeamColumnFragment

### Interfaces

```text
irregular envelope interface
beam projection thermal bridge interface
column-stub thermal bridge interface
cut-face envelope risk interface
irregular insulation interface
```

### Connector profile → ports

```text
thermal bridge profile
→ beam-projection-thermal-bridge-port
→ column-stub-thermal-bridge-port

insulation layer profile
→ irregular-insulation-face-port

moisture protection profile
→ cut-face-moisture-risk-port
```

---

# 9. Package 3 — TGA / Openings Package

## General role

Creates representations for openings, penetrations, service routing, shafts, pipes, cables, sleeves, and core drilling.

## Representations

```text
opening_representation
penetration_representation
service_route_representation
service_conflict_representation
```

## General interface types

| Interface type | Geometry kind | Meaning |
|---|---|---|
| Existing opening interface | Void / opening zone | Existing usable opening |
| Service penetration interface | Opening or surface zone | Service pass-through |
| Core-drilling interface | Cylindrical volume / circular zone | Candidate drilling |
| Cable route interface | Line / corridor zone | Cable path |
| Pipe route interface | Line / corridor volume | Pipe path |
| Shaft interface | Surface or volume zone | Vertical service relation |
| Blocked penetration interface | Surface or volume zone | Avoid / blocked service area |

## Connector profiles

| Connector profile | Physical? | Typical ports |
|---|---|---|
| Existing opening profile | No | opening boundary port |
| Sleeve profile | Yes | sleeve receiving port |
| Core-drilling profile | Yes/process | circular drilling port |
| Cable route profile | Maybe | cable route port |
| Pipe route profile | Maybe | pipe route port |
| Shaft connection profile | Maybe | shaft interface port |

## Minimal data structure

```yaml
tga_package:
  representations:
    - opening_representation
    - service_route_representation
  interfaces:
    - existing_opening_interface
    - core_drilling_interface
  connector_profiles:
    - sleeve_profile
    - core_drilling_profile
  ports:
    - connector-bound service ports
```

## Example A — DE_1OG_001 slab

### Interface

```text
no existing opening interface recorded in the catalogue entry
possible core-drilling interface only as generated candidate
possible service penetration interface if project context requires it
```

### Connector profile → ports

```text
core-drilling profile
→ slab-core-drilling-port

sleeve profile
→ slab-sleeve-receiving-port, only if drilling is allowed
```

## Example B — Wand–Decke

### Interfaces

```text
vertical service pass-through interface, if opening exists
horizontal service route interface along wall / slab zone
blocked penetration interface near bearing joint
```

### Connector profile → ports

```text
core-drilling profile
→ non-structural-core-drilling-port

sleeve profile
→ service-sleeve-port

cable route profile
→ horizontal-cable-route-port
```

## Example C — SlabBeamColumnFragment

### Interfaces

```text
service penetration interface in slab zone
blocked penetration interface near beam web
blocked penetration interface near column stub
core-drilling interface outside monolithic junctions
```

### Connector profile → ports

```text
core-drilling profile
→ safe-zone-core-drilling-port

sleeve profile
→ slab-zone-sleeve-port

pipe route profile
→ route-around-beam-port
```

---

# 10. Package 4 — Semantic / Architectural Package

## General role

Creates representations for spatial, visual, facade, rhythm, alignment, identity, and reuse-expression relations.

## Representations

```text
spatial_interface_representation
visibility_representation
facade_rhythm_representation
datum_grid_representation
reuse_expression_representation
```

## General interface types

| Interface type | Geometry kind | Meaning |
|---|---|---|
| Room-boundary interface | Surface | Defines space |
| Facade-rhythm interface | Surface / line / interval | Facade order |
| Visible-reuse interface | Surface or edge zone | Shows reused component |
| Ceiling expression interface | Surface | Visible underside |
| Floor surface interface | Surface | Floor / finish relation |
| Joint-line interface | Line | Visible joint |
| Datum alignment interface | Line / plane | Alignment reference |
| Grid continuation interface | Line / spacing pattern | Repetition / order |
| Reuse identity interface | Surface zone | ID / trace display |

## Connector profiles

Semantic connector profiles are **relation profiles**, not hardware.

| Connector profile | Physical? | Typical ports |
|---|---|---|
| Room boundary profile | No | room boundary port |
| Visible reuse profile | No | visible surface / edge port |
| Datum alignment profile | No | datum line port |
| Grid continuation profile | No | grid line / interval port |
| Joint expression profile | No | joint line port |
| Reuse identity profile | No | identity display port |

## Minimal data structure

```yaml
semantic_package:
  representations:
    - spatial_interface_representation
    - reuse_expression_representation
  interfaces:
    - room_boundary_interface
    - visible_reuse_interface
  connector_profiles:
    - visible_reuse_profile
    - datum_alignment_profile
  ports:
    - connector-bound architectural relation ports
```

## Example A — DE_1OG_001 slab

### Interfaces

```text
floor surface interface
ceiling expression interface
exposed edge interface
joint line interface
grid continuation interface
reuse identity interface
```

### Connector profile → ports

```text
floor surface profile
→ slab-floor-surface-port

ceiling expression profile
→ slab-ceiling-expression-port

visible reuse profile
→ slab-edge-visible-reuse-port

grid continuation profile
→ slab-width-grid-port
```

## Example B — Wand–Decke

### Interfaces

```text
room boundary interface at wall
ceiling expression interface at slab underside
joint line interface at wall-slab joint
datum alignment interface at top of wall / slab edge
visible reuse interface if connector remains visible
```

### Connector profile → ports

```text
room boundary profile
→ wall-room-boundary-port

joint expression profile
→ wall-slab-joint-line-port

datum alignment profile
→ wall-top-datum-port
→ slab-edge-datum-port

visible reuse profile
→ exposed-connector-visible-port
```

## Example C — SlabBeamColumnFragment

### Interfaces

```text
visible monolithic junction interface
exposed cut-face interface
beam expression interface
column-stub expression interface
grid continuation interface from original bay rhythm
datum alignment interface along slab edge
```

### Connector profile → ports

```text
visible reuse profile
→ monolithic-junction-visible-port

joint / cut expression profile
→ cut-face-expression-port

grid continuation profile
→ original-bay-grid-port

reuse identity profile
→ fragment-story-port
```

---

# 11. Package 5 — Logistics / Assembly Package

## General role

Creates representations for storage, lifting, transport, assembly access, protection, and temporary bracing.

## Representations

```text
transport_representation
storage_representation
lifting_representation
assembly_access_representation
protection_representation
temporary_stability_representation
```

## General interface types

| Interface type | Geometry kind | Meaning |
|---|---|---|
| Transport envelope interface | Volume | Transport size |
| Storage support interface | Surface zone / line strip | Storage bearing |
| Lifting interface | Point or surface zone | Lifting location |
| Stacking interface | Surface zone | Stackable contact |
| Assembly access interface | Clearance volume | Required access |
| Installation clearance interface | Volume | Placement space |
| Temporary bracing interface | Surface or line zone | Temporary stability |
| Protection interface | Surface or edge zone | Damage protection |

## Connector profiles

| Connector profile | Physical? | Typical ports |
|---|---|---|
| Lifting profile | Maybe | lifting point / lifting zone port |
| Storage support profile | No | storage support port |
| Stacking profile | No | stacking surface port |
| Transport fixation profile | Maybe | fixation port |
| Temporary bracing profile | Maybe | bracing port |
| Protection profile | No | protection zone port |

## Minimal data structure

```yaml
logistics_package:
  representations:
    - transport_representation
    - lifting_representation
  interfaces:
    - lifting_interface
    - storage_support_interface
  connector_profiles:
    - lifting_profile
    - temporary_bracing_profile
  ports:
    - connector-bound handling ports
```

## Example A — DE_1OG_001 slab

### Interfaces

```text
lying storage interface
stacking interface
transport envelope interface
assembly access interface along bearing edges
lifting interface candidates
```

### Connector profile → ports

```text
storage support profile
→ slab-lying-storage-port

stacking profile
→ slab-stacking-surface-port

lifting profile
→ slab-lifting-zone-port

transport fixation profile
→ slab-edge-fixation-port
```

## Example B — Wand–Decke

### Interfaces

```text
wall-top assembly access interface
slab placement envelope interface
joint access interface
temporary support interface if required
```

### Connector profile → ports

```text
assembly access profile
→ wall-top-access-port
→ slab-edge-access-port

temporary bracing / support profile
→ temporary-support-port

lifting profile
→ slab-placement-lifting-port
```

## Example C — SlabBeamColumnFragment

### Interfaces

```text
irregular transport envelope interface
shifted center-of-gravity handling interface
lifting interface at stable regions
temporary bracing interface if column stub creates instability
protection interface at cut faces
assembly access interface around beam / column projection
```

### Connector profile → ports

```text
lifting profile
→ stable-zone-lifting-port

temporary bracing profile
→ column-stub-bracing-port

protection profile
→ cut-face-protection-port

transport fixation profile
→ stable-face-fixation-port
```

---

# 12. Package 6 — Evidence Overlay Package

## General role

Maps evidence from scans, tests, photos, documents, and inspections onto package geometry.

## Representations

```text
reinforcement_overlay_representation
damage_overlay_representation
sample_point_representation
confidence_overlay_representation
```

## General interface types

Evidence does not normally create connector profiles.  
It qualifies, blocks, or reduces confidence in ports and connector profiles from other packages.

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
| Confidence zone | Zone | changes confidence of generated ports |

## Port effects

```yaml
port_effect:
  affected_port_id: string
  effect: ok | warning | blocked | confidence_reduced
  reason: string
  evidence_ref: string
```

## Minimal data structure

```yaml
evidence_package:
  representations:
    - reinforcement_overlay_representation
    - damage_overlay_representation
  overlays:
    - rebar_lines
    - damage_zones
    - sample_points
  port_effects:
    - warning_or_blocking_relations
```

## Example A — DE_1OG_001 slab

### Evidence overlays

```text
rebar scan zones if available
unknown rebar zones if no scan exists
damage zones if mapped
core sample points if tested
carbonation sample points if tested
```

### Effect on connector-bound ports

```text
unknown rebar zone
→ warns / blocks slab-edge-anchor-zone-port

damage at slab edge
→ warns slab-edge-bearing-surface-port

spalling at lifting region
→ warns slab-lifting-zone-port
```

## Example B — Wand–Decke

### Evidence overlays

```text
wall rebar overlay
slab rebar overlay
unknown reinforcement zone at joint
damage overlap with wall-top bearing zone
damage overlap with slab-edge bearing zone
```

### Effect on connector-bound ports

```text
rebar conflict
→ blocks wall-anchor-port or slab-anchor-port

unknown reinforcement
→ warns post-installed-rebar ports

damage at wall top
→ warns wall-top-bearing-port

damage at slab edge
→ warns slab-edge-bearing-port
```

## Example C — SlabBeamColumnFragment

### Evidence overlays

```text
slab rebar zones
beam rebar zones
column rebar zones
unknown rebar at monolithic junction
cut-face exposed reinforcement
cracks near beam-column junction
damage at cut faces
```

### Effect on connector-bound ports

```text
unknown rebar at junction
→ blocks drilling / anchor ports near monolithic junction

cut-face damage
→ warns cut-face-risk-port

exposed rebar
→ warns durability and structural connector profiles

cracks near beam-column junction
→ reduces confidence of monolithic continuity ports
```

---

# 13. Clean Component Structure

Each component should store package outputs like this:

```yaml
component:
  id: string
  typology: string
  material: string

  packages:
    base:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    structural:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    energy:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    tga:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    semantic:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    logistics:
      representations: []
      interfaces: []
      connector_profiles: []
      ports: []

    evidence:
      representations: []
      overlays: []
      port_effects: []
```

---

# 14. Final Rule

```text
A port is never just a loose tag on a face.

A port belongs to a connector profile.
A connector profile belongs to an interface.
An interface belongs to a representation.
A representation belongs to a package.
A package belongs to a component.
```
