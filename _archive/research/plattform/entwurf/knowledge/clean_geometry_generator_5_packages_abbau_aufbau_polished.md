# Minimal Geometry Generator Package Structure  
## Domain-Owned Geometry, Data Types, and Examples

**Purpose**  
This document defines a minimal and clean structure for geometry generator packages in a reclaimed-component design system.

**Core rule**  
There is no generic connector generator.  
Each domain package owns the geometry, interfaces, ports, and zones that belong to its own domain.

```text
Generator = creates geometry.
System = interprets geometry with rules, evidence, and project data.
Rule Checker = checks active design actions.
```

---

# 1. Minimal System Flow

```text
Minimum Input
+ Base Geometry
+ Component Typology
        ↓
Geometry Generator Packages
        ↓
Generated Geometry Data
        ↓
System Modules
        ↓
Bauteilpass + Rule-Checker Readiness
```

---

# 2. Shared Geometry Data Types

All packages should use the same small vocabulary.

## 2.1 Point

A precise location.

```text
Geometry kind:
0D point
```

Used for:

```text
center of gravity
sample point
anchor point candidate
lifting point candidate
reference point
```

Example:

```yaml
point:
  id: P-001
  kind: point
  xyz: [0, 0, 0]
```

---

## 2.2 Line / Curve

A one-dimensional path, edge, axis, or support line.

```text
Geometry kind:
1D line / curve
```

Used for:

```text
edge
axis
joint line
line support reference
beam axis
crack line
grid line
datum line
```

Important:

```text
A line support is not only a mathematical line.
For checking, it should usually become a narrow surface strip / bearing zone.
```

Example:

```yaml
line:
  id: L-001
  kind: line
  role: support_reference_line
```

---

## 2.3 Surface / Face

A two-dimensional face or contact surface.

```text
Geometry kind:
2D surface / face
```

Used for:

```text
top face
bottom face
wall face
bearing surface
thermal boundary face
insulation face
visible face
storage support surface
```

Example:

```yaml
surface:
  id: S-001
  kind: surface
  role: top_face
```

---

## 2.4 Zone

A meaningful part of a face, edge, or volume.

```text
Geometry kind:
sub-region of point, line, surface, or volume
```

Used for:

```text
bearing zone
anchor zone
no-drill zone
thermal bridge zone
service zone
damage zone
assembly access zone
```

Important:

```text
Most rule-checkable areas are zones, not raw faces.
```

Example:

```yaml
zone:
  id: Z-001
  kind: surface_zone
  role: bearing_zone
  base_geometry: S-001
```

---

## 2.5 Volume / Solid

A three-dimensional body or sub-body.

```text
Geometry kind:
3D volume / solid
```

Used for:

```text
whole component
beam volume
slab volume
column volume
void
monolithic continuity zone
transport envelope
```

Example:

```yaml
volume:
  id: V-001
  kind: solid
  role: component_body
```

---

## 2.6 Port

A named interface location.

```text
Geometry kind:
point, line, surface, or zone with semantic interface meaning
```

Used for:

```text
bearing port
service penetration port
lifting port
room-boundary interface
insulation interface
```

Important:

```text
A port is not always a physical connector.
It is a named place where a relation can happen.
```

Example:

```yaml
port:
  id: PORT-001
  kind: surface_zone_port
  role: structural_bearing_port
  geometry: Z-001
```

---

## 2.7 Interface Region

A region prepared for a possible relationship between components or systems.

```text
Geometry kind:
zone or group of zones
```

Used for:

```text
structural connection
thermal envelope interface
service pass-through
assembly access
visible reuse expression
```

Example:

```yaml
interface_region:
  id: IR-001
  package: structural
  role: load_transfer_interface
  geometry: [Z-001, Z-002]
```

---

# 3. Package Tree

```text
GEOMETRY GENERATOR PACKAGES
│
├── 0. Base Geometry
├── 1. Structural Interface Geometry
├── 2. Energy / Envelope Geometry
├── 3. TGA / Openings Geometry
├── 4. Semantic / Architectural Interface Geometry
├── 5. Logistics / Assembly Geometry
└── 6. Evidence Geometry Overlay
```

---

# 4. Package 0 — Base Geometry

## Purpose

Create the neutral geometry of the component.

## Owns

| Item | Geometry kind |
|---|---|
| Component body | Volume / solid |
| Bounding box | Volume |
| Dimensions | Quantity |
| Faces | Surface |
| Edges | Line |
| Corners | Point |
| Raw openings | Void / volume or boundary line |
| Raw cut-outs | Void / volume |
| Center of gravity | Point |
| Surface area | Quantity |
| Volume | Quantity |

## Does not own

```text
ports
structural meaning
energy meaning
TGA meaning
semantic meaning
logistics meaning
evidence meaning
```

## Minimal output

```yaml
base_geometry:
  body: volume
  faces: surfaces
  edges: lines
  openings: voids
  dimensions: quantities
  volume: quantity
  center_of_gravity: point
```

## Example A — DE_1OG_001 slab

```text
body = slab volume
faces = top, bottom, side faces
edges = long edges, short edges
dimensions = 4500 × 2300 × 180 mm
volume = 1.863 m³
center = center point
```

## Example B — Wand–Decke

```text
wall body = volume
slab body = volume
wall top = surface / edge region
slab edge = surface / edge region
raw overlap candidate = geometric relation only
```

## Example C — SlabBeamColumnFragment

```text
body = one monolithic composite volume
sub-volumes = slab part, beam part, column-stub part
cut faces = surfaces
monolithic junction = volume region
center of gravity = point
```

---

# 5. Package 1 — Structural Interface Geometry

## Purpose

Create geometry for support, bearing, restraint, load transfer, and structural connection.

## General principle

Do not describe everything as a connector.  
For structure, the most important geometry is usually:

```text
bearing surface
support line
support zone
load-transfer zone
anchor candidate zone
dowel candidate zone
grout joint zone
steel support zone
cut-face risk zone
```

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Span direction | Vector / line | Candidate load direction |
| Beam / slab axis | Line | Main structural axis |
| Line support | Line + surface strip | Support along an edge or wall |
| Point support | Point + local surface patch | Support at column or local bearing |
| Bearing zone | Surface zone | Real contact / support area |
| Load-transfer zone | Surface or volume zone | Region where force may pass |
| Anchor candidate zone | Surface zone with point candidates | Possible anchor area |
| Dowel candidate zone | Point or line array inside zone | Possible dowel positions |
| Grout joint zone | Volume / gap zone | Cast or filled joint |
| Steel support zone | Surface or line zone | Possible steel bearing interface |
| Structural no-go zone | Zone | Area where structural connection should not occur |
| Cut-face risk zone | Surface zone | Cut edge or face with structural uncertainty |
| Monolithic continuity zone | Volume zone | Internal continuity inside one piece |

## General port patterns

| Port pattern | Geometry kind |
|---|---|
| bearing-port | surface zone |
| line-support-port | line + surface strip |
| point-support-port | point + surface patch |
| restraint-port | line or surface zone |
| external-structural-interface-port | surface zone |
| cut-face-risk-port | surface zone |

## Does not own

```text
final load capacity
static proof
anchor capacity
punching proof
shear proof
moment proof
fire cover
LCA of connector material
```

## Minimal output

```yaml
structural_geometry:
  span_direction: line_or_vector
  support_zones: zones
  bearing_zones: surface_zones
  point_supports: point_plus_patch
  line_supports: line_plus_strip
  structural_ports: ports
  connection_candidate_zones: zones
```

## Example A — DE_1OG_001 slab

```text
span direction candidate = line / vector
slab-edge bearing = surface zone
line support = edge line + bearing strip
anchor candidate = surface zone near slab edge
structural port = slab-edge-bearing port
```

## Example B — Wand–Decke

```text
wall-top support = line + surface strip
slab-edge bearing = surface zone
grout joint = volume / gap zone
post-installed rebar zone = surface zone with point candidates
flat-steel-holder zone = surface zone
anchor candidate = point candidates inside a surface zone
```

## Example C — SlabBeamColumnFragment

```text
slab zone = surface / volume zone
beam axis = line
column-stub axis = line
slab-beam continuity = volume zone
beam-column continuity = volume zone
external cut face = surface risk zone
external support port = surface zone
internal slab-beam relation = monolithic continuity, not a connector
```

---

# 6. Package 2 — Energy / Envelope Geometry

## Purpose

Create geometry for thermal envelope, moisture, insulation, roof, facade, ground contact, and U-value-related reasoning.

## General principle

Energy geometry is mostly:

```text
face-based
surface-based
edge-based
layer-based
boundary-based
```

Do not force energy into connector language.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Thermal boundary | Surface |
| Exterior face | Surface |
| Interior face | Surface |
| Roof face | Surface |
| Ground-contact face | Surface |
| Facade interface | Surface |
| Insulation interface | Surface |
| U-value thickness | Distance / line normal to surface |
| Thermal bridge edge | Line or narrow zone |
| Envelope penetration | Opening zone |
| Moisture-risk zone | Surface or edge zone |

## General port patterns

| Port pattern | Geometry kind |
|---|---|
| envelope-interface-port | surface |
| insulation-interface-port | surface |
| roof-interface-port | surface |
| ground-contact-port | surface |
| thermal-bridge-edge-port | line or zone |
| envelope-penetration-port | opening zone |

## Does not own

```text
final U-value
thermal bridge Psi-value
moisture proof
GEG compliance
full assembly build-up
```

## Minimal output

```yaml
energy_geometry:
  thermal_boundary_faces: surfaces
  insulation_interfaces: surfaces
  thermal_bridge_zones: line_or_surface_zones
  u_value_thickness: distance
  moisture_risk_zones: zones
```

## Example A — DE_1OG_001 slab

```text
if used inside:
energy relevance = low / not applicable

if used as roof or exterior floor:
roof / exterior face = surface
interior face = surface
U-value thickness = 180 mm distance
slab edge = thermal bridge line / zone
```

## Example B — Wand–Decke

```text
wall-slab joint in envelope = thermal bridge zone
steel crossing insulation = envelope connector crossing zone
insulation interruption = surface / zone
moisture-risk joint = edge / surface zone
```

## Example C — SlabBeamColumnFragment

```text
beam projection = thermal bridge volume / edge zone
column stub = thermal bridge zone if crossing envelope
cut face = envelope risk surface
slab thickness = U-value distance candidate
irregular insulation interface = surface zones
```

---

# 7. Package 3 — TGA / Openings Geometry

## Purpose

Create geometry for openings, penetrations, service routes, shafts, pipes, cables, and core drilling.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Existing opening | Void / opening volume |
| Opening boundary | Line / curve |
| Opening face | Surface |
| Core-drilling candidate | Cylindrical volume or circular surface zone |
| Cable route | Line / corridor zone |
| Pipe route | Line / corridor volume |
| Shaft interface | Surface or volume zone |
| Blocked penetration zone | Surface or volume zone |
| Edge distance | Distance quantity |
| Service port | Opening zone or surface zone |

## General port patterns

| Port pattern | Geometry kind |
|---|---|
| existing-opening-port | opening zone |
| service-penetration-port | opening or surface zone |
| core-drilling-port | cylindrical candidate zone |
| cable-route-port | line / corridor zone |
| pipe-route-port | line / corridor volume |
| shaft-interface-port | surface or volume zone |

## Does not own

```text
approval of drilling
fire sealing
acoustic sealing
reinforcement conflict proof
final TGA design
```

## Minimal output

```yaml
tga_geometry:
  openings: voids
  penetration_candidates: zones
  service_ports: ports
  blocked_zones: zones
  edge_distances: quantities
```

## Example A — DE_1OG_001 slab

```text
existing openings = none recorded in the given catalogue entry
new core-drilling candidates = cylindrical zones
edge distance = distance quantity
service penetration port = generated only if allowed by context
```

## Example B — Wand–Decke

```text
service conflict near joint = blocked zone
vertical pass-through = opening / volume candidate
horizontal route along wall top = line / corridor zone
core drilling near bearing = blocked or warning zone
```

## Example C — SlabBeamColumnFragment

```text
slab area = possible service penetration zone
beam web = blocked or sensitive zone
column stub = blocked or sensitive zone
core drilling outside monolithic junction = cylindrical candidate zone
service conflict with beam depth = volume conflict zone
```

---

# 8. Package 4 — Semantic / Architectural Interface Geometry

## Purpose

Create geometry for spatial, visual, facade, rhythm, alignment, identity, and reuse-expression relations.

## General principle

This package should lean toward interfaces, not only faces.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Room-boundary interface | Surface |
| Facade-rhythm interface | Surface, line, or module interval |
| Visible-reuse interface | Surface or edge zone |
| Ceiling expression | Surface |
| Floor surface | Surface |
| Exposed edge | Line or narrow surface zone |
| Joint line | Line |
| Datum alignment | Line / plane |
| Grid continuation | Line / module spacing |
| Threshold interface | Line / surface zone |
| Reuse identity display zone | Surface zone |

## General port patterns

| Port pattern | Geometry kind |
|---|---|
| room-boundary-port | surface |
| facade-rhythm-port | surface or line |
| visible-reuse-port | surface or edge zone |
| ceiling-expression-port | surface |
| floor-surface-port | surface |
| exposed-edge-port | line or strip |
| datum-alignment-port | line or plane |
| grid-continuation-port | line / spacing pattern |
| threshold-port | line or surface zone |

## Does not own

```text
beauty judgment
final design intent
structural validity
energy validity
fire compliance
```

## Minimal output

```yaml
semantic_geometry:
  architectural_interfaces: interface_regions
  visible_zones: surface_or_edge_zones
  datum_lines: lines
  grid_lines: lines
  identity_zones: surface_zones
```

## Example A — DE_1OG_001 slab

```text
top = floor-surface interface
bottom = ceiling-expression interface
long edge = exposed-edge interface
joint = joint-line interface
width repetition = grid-continuation pattern
component ID mark = reuse-identity zone
```

## Example B — Wand–Decke

```text
wall side = room-boundary interface
slab underside = ceiling-expression interface
wall-slab joint = joint-line
top datum = datum-alignment line
visible connector area = visible-reuse zone if exposed
```

## Example C — SlabBeamColumnFragment

```text
monolithic junction = visible-reuse interface
cut face = exposed-cut-face interface
beam underside = beam-expression interface
column stub = reuse-story interface
slab edge = datum-alignment line
original bay rhythm = grid-continuation pattern
```

---

# 9. Package 5 — Logistics / Assembly Geometry

## Purpose

Create geometry for storage, lifting, transport, access, assembly, protection, and temporary bracing.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Transport envelope | Volume |
| Storage orientation | Orientation vector / state |
| Center of gravity | Point |
| Lifting candidate | Point or surface zone |
| Storage support | Surface zone or line support |
| Stacking interface | Surface zone |
| Assembly access | Volume / clearance zone |
| Installation clearance | Volume |
| Crane pick zone | Point or volume zone |
| Temporary bracing | Surface or line zone |
| Protection zone | Surface or edge zone |
| Damage-sensitive zone | Surface or edge zone |

## General port patterns

| Port pattern | Geometry kind |
|---|---|
| lifting-port | point or surface zone |
| crane-pick-port | point or volume zone |
| storage-support-port | surface or line zone |
| transport-support-port | surface or line zone |
| stacking-port | surface zone |
| assembly-access-port | clearance volume |
| temporary-bracing-port | surface or line zone |
| protection-port | surface or edge zone |

## Does not own

```text
lifting proof
crane capacity
transport permit
site logistics plan
assembly approval
```

## Minimal output

```yaml
logistics_geometry:
  transport_envelope: volume
  center_of_gravity: point
  lifting_candidates: points_or_zones
  storage_supports: zones
  assembly_access: clearance_volumes
  protection_zones: zones
```

## Example A — DE_1OG_001 slab

```text
transport envelope = 4500 × 2300 × 180 mm volume
center of gravity = point
lying storage = orientation state
stacking support = surface zones
timber separator contact = surface strips
assembly access = clearance zone along bearing edges
```

## Example B — Wand–Decke

```text
wall-top access = clearance zone
slab placement envelope = volume
connector access = clearance zone at joint
temporary support = surface / line zone if needed
sequence relation = wall first, slab after
```

## Example C — SlabBeamColumnFragment

```text
transport envelope = irregular volume
center of gravity = shifted point
lifting candidates = points / surface zones
cut-face protection = surface zone
storage support = custom surface zones
temporary bracing = surface / line zone if column stub is unstable
rotation risk = swept volume
```

---

# 10. Package 6 — Evidence Geometry Overlay

## Purpose

Map evidence from scans, tests, photos, documents, and inspections onto geometry.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Rebar line | Line / curve |
| Rebar zone | Line buffer / volume zone |
| Cover depth | Distance quantity |
| Unknown rebar zone | Surface or volume zone |
| Damage zone | Surface or volume zone |
| Crack line | Line |
| Spalling zone | Surface / edge zone |
| Exposed rebar | Line or surface zone |
| Core sample point | Point / cylindrical volume |
| Carbonation sample point | Point / depth line |
| Chloride sample point | Point |
| Photo-mapped surface | Surface |
| Confidence zone | Zone |

## Does not own

```text
final material acceptance
structural safety
durability decision
repair design
approval decision
```

## Minimal output

```yaml
evidence_geometry:
  rebar_lines: lines
  unknown_rebar_zones: zones
  damage_zones: zones
  sample_points: points
  confidence_zones: zones
```

## Example A — DE_1OG_001 slab

```text
rebar scan = lines / zones if available
unknown rebar = zones if scan missing
damage = surface or edge zones if mapped
core sample = point / cylinder if tested
carbonation sample = point / depth line if tested
```

## Example B — Wand–Decke

```text
wall rebar = line / zone overlay
slab rebar = line / zone overlay
anchor-blocking zone = rebar buffer zone
bearing damage = overlap between damage zone and bearing zone
unknown rebar at joint = warning zone
```

## Example C — SlabBeamColumnFragment

```text
slab rebar = line / zone
beam rebar = line / zone
column rebar = line / zone
junction unknown rebar = volume zone
cut-face exposed rebar = line / surface zone
cracks near junction = crack lines
damage at cut faces = surface zones
```

---

# 11. Complete Example C — SlabBeamColumnFragment

## Status

```text
This is a proposed composite typology for the system.
It is not a named standard element in the Abbau/Aufbau handbook.
```

## Definition

```text
A monolithic reinforced-concrete fragment composed of:
- slab portion
- integrated beam portion
- partial column section

It is cut from an existing structural bay and stored as one real component.
```

## System treatment

```text
one component ID
one Bauteilpass
one Semio Type
one placed Piece
multiple internal geometry zones
external interface ports only
internal monolithic continuity zones, not internal connectors
```

## Required evidence

```text
reinforcement continuity
capacity of remaining fragment
condition of cut faces
crack / damage severity
safe lifting strategy
fire behavior of irregular exposed geometry
thermal bridge proof if used in envelope
```

---

# 12. Final Boundary

```text
Generator:
creates domain geometry.

System:
interprets geometry with catalogue data, evidence, rules, and project defaults.

Rule Checker:
evaluates active design actions.
```

Example:

```text
Generator:
creates slab-edge bearing zone.

System:
knows it can be checked against wall-top support.

Rule Checker:
checks the actual placed slab-wall connection.
```

---

# 13. Final Rule

```text
Do not create one generic connector package.

Create domain geometry packages.

Each package owns the interface geometry that belongs to its own domain.
```
