# Minimal Geometry Generator Package Structure  
## v5 — Ports, Connectors, Interface Regions, and Example Mapping

**Purpose**  
This document defines a minimal and clean structure for geometry generator packages in a reclaimed-component design system.

**Core rule**  
There is no generic connector generator.  
Each domain package owns the geometry, ports, interface regions, and connector candidates that belong to its own domain.

```text
Generator = creates domain geometry.
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
        ↓
Rule Checker during design
```

---

# 2. Core Interface Terms

## 2.1 Port

A **port** is a named geometric interface location where a relation can happen.

```text
Geometry kind:
point, line, surface, or zone
```

A port is not automatically a physical connector.

Examples:

```text
slab-edge-bearing-port
wall-top-bearing-port
service-penetration-port
lifting-port
room-boundary-port
thermal-envelope-port
```

Minimal schema:

```yaml
port:
  id: string
  package: structural | energy | tga | semantic | logistics
  port_kind: string
  geometry_kind: point | line | surface | zone | volume
  geometry_ref: string
  direction: vector | null
  compatible_port_patterns: []
  confidence: high | medium | low
```

---

## 2.2 Interface Region

An **interface region** is a geometry area prepared for a possible relation between components or systems.

```text
Geometry kind:
usually a zone or group of zones
```

Examples:

```text
bearing interface
thermal bridge interface
service pass-through interface
assembly access interface
visible reuse interface
```

Minimal schema:

```yaml
interface_region:
  id: string
  package: structural | energy | tga | semantic | logistics
  interface_kind: string
  geometry_refs: []
  related_ports: []
  rule_relevance: []
  confidence: high | medium | low
```

---

## 2.3 Connector Candidate

A **connector candidate** is a geometry region where a physical or technical connection system could be placed.

```text
Geometry kind:
point, line array, surface zone, gap volume, or local volume
```

Examples:

```text
anchor candidate zone
dowel candidate zone
grout joint zone
flat steel holder zone
core-drilling candidate
lifting insert candidate
```

Minimal schema:

```yaml
connector_candidate:
  id: string
  package: structural | tga | logistics | energy
  connector_candidate_kind: string
  geometry_kind: point | line | surface_zone | volume_zone
  geometry_ref: string
  allowed_connector_system_patterns: []
  required_evidence: []
  confidence: high | medium | low
```

Important:

```text
The generator creates connector candidates.
The system chooses or filters actual connector systems.
The rule checker evaluates whether the selected connector works in the active design.
```

---

## 2.4 Connector System

A **connector system** is the actual technical connection method.

```text
This is system-level data, not raw geometry.
```

Examples from Abbau/Aufbau:

```text
Schraubanker
Edelstahldorn
Winkelverbinder
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

Minimal schema:

```yaml
connector_system:
  id: string
  system_name: string
  compatible_port_patterns: []
  required_connector_candidates: []
  required_evidence: []
  required_checks: []
```

---

# 3. Shared Geometry Types

## 3.1 Point

```text
0D location
```

Used for:

```text
center of gravity
sample point
anchor point candidate
lifting point candidate
reference point
```

---

## 3.2 Line / Curve

```text
1D path, edge, axis, joint, or datum
```

Used for:

```text
edge
axis
joint line
beam axis
line support reference
datum line
crack line
```

Important:

```text
A line support is not only a mathematical line.
For checking, it should usually become a line plus a narrow surface bearing strip.
```

---

## 3.3 Surface / Face

```text
2D face or contact surface
```

Used for:

```text
top face
bottom face
wall face
bearing surface
thermal boundary face
visible face
storage support surface
```

---

## 3.4 Zone

```text
meaningful sub-region of a point, line, surface, or volume
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

---

## 3.5 Volume / Solid

```text
3D body or sub-body
```

Used for:

```text
whole component
beam volume
slab volume
column volume
void
grout volume
transport envelope
monolithic continuity zone
```

---

# 4. Package Tree

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

# 5. Package 0 — Base Geometry

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
| Raw openings | Void / volume |
| Raw cut-outs | Void / volume |
| Center of gravity | Point |
| Surface area | Quantity |
| Volume | Quantity |

## Ports / connectors

```text
None.
Base Geometry creates no ports and no connector candidates.
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
  ports: []
  connector_candidates: []
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

# 6. Package 1 — Structural Interface Geometry

## Purpose

Create geometry for support, bearing, restraint, load transfer, and structural connection.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Span direction | Vector / line | Candidate load direction |
| Beam / slab axis | Line | Main structural axis |
| Line support | Line + surface strip | Support along edge, wall, or beam |
| Point support | Point + surface patch | Local support at column or point bearing |
| Bearing zone | Surface zone | Real contact / support area |
| Load-transfer zone | Surface or volume zone | Region where force may pass |
| Anchor candidate zone | Surface zone with point candidates | Possible anchor area |
| Dowel candidate zone | Point or line array inside zone | Possible dowel positions |
| Grout joint zone | Volume / gap zone | Cast or filled joint |
| Steel support zone | Surface or line zone | Possible steel bearing interface |
| Structural no-go zone | Zone | Area where structural connection should not occur |
| Cut-face risk zone | Surface zone | Cut edge or face with structural uncertainty |
| Monolithic continuity zone | Volume zone | Internal continuity inside one piece |

## Ports

| Port pattern | Geometry kind | Meaning |
|---|---|---|
| bearing-port | Surface zone | Generic load-bearing interface |
| line-support-port | Line + surface strip | Linear support interface |
| point-support-port | Point + surface patch | Local support interface |
| restraint-port | Line or surface zone | Prevents movement / rotation |
| external-structural-interface-port | Surface zone | External structural connection |
| cut-face-risk-port | Surface zone | Exposed uncertain structural interface |

## Connector candidates

| Connector candidate | Geometry kind |
|---|---|
| anchor-candidate | Point candidates inside surface zone |
| dowel-candidate | Point / line-array candidates |
| post-installed-rebar-candidate | Line or point-array inside surface zone |
| grout-joint-candidate | Gap volume |
| flat-steel-holder-candidate | Surface zone |
| angle-connector-candidate | Surface / edge zone |
| steel-support-candidate | Line or surface zone |

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
  support_zones: zones
  bearing_zones: surface_zones
  point_supports: point_plus_patch
  line_supports: line_plus_strip
  structural_ports: ports
  connector_candidates: connector_candidates
```

## Example A — DE_1OG_001 slab

### Ports

```text
slab-edge-bearing-port
```

Geometry kind:

```text
line + narrow surface bearing strip along slab edge
```

Compatible port patterns:

```text
wall-top-bearing-port
beam-top-bearing-port
column-head-bearing-port, only if engineered
```

### Connector candidates

```text
anchor-candidate zone near slab edge
post-installed-rebar-candidate zone near slab edge
edge-restraint candidate zone
```

### System connector systems

Depending on the paired component, the system may later map this to:

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

### System interpretation

```text
capacity remains engineering_required unless proof exists
drilling / anchoring depends on reinforcement evidence
```

---

## Example B — Wand–Decke

### Ports

```text
wall-top-bearing-port
slab-edge-bearing-port
```

Geometry kinds:

```text
wall-top-bearing-port = line + surface strip
slab-edge-bearing-port = line + surface strip
```

### Interface region

```text
wall-slab-load-transfer-interface
```

Geometry kind:

```text
overlap of two bearing surface strips
```

### Connector candidates

```text
post-installed-rebar-candidate
grout-joint-candidate
flat-steel-holder-candidate
anchor-candidate
```

### Abbau/Aufbau connector systems

```text
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

### Required evidence

```text
reinforcement position
edge distance
anchor spacing
structural proof
fire context if exposed steel is used
```

---

## Example C — SlabBeamColumnFragment

### Ports

```text
external slab-edge-bearing-port
beam-end-bearing-port, if beam is cut at end
column-base-bearing-port or column-head-bearing-port, depending orientation
cut-face-risk-port
```

Geometry kinds:

```text
slab-edge-bearing-port = line + surface strip
beam-end-bearing-port = surface patch
column-bearing-port = point + local surface patch
cut-face-risk-port = cut surface zone
```

### Internal zones

```text
slab-beam monolithic-continuity zone
beam-column monolithic-continuity zone
```

Geometry kind:

```text
volume zones
```

Important:

```text
Internal monolithic continuity zones are not connectors.
Only external interfaces become ports or connector candidates.
```

### Connector candidates

```text
anchor-candidate zones only outside critical monolithic junctions
dowel-candidate zones only where reinforcement evidence permits
steel-support candidates at external cut/support faces
```

### Required evidence

```text
reinforcement continuity
capacity of remaining fragment
cut-face condition
lifting strategy
```

---

# 7. Package 2 — Energy / Envelope Geometry

## Purpose

Create geometry for thermal envelope, moisture, insulation, roof, facade, ground contact, and U-value reasoning.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Thermal boundary | Surface | Boundary between thermal zones |
| Exterior face | Surface | Face exposed to exterior |
| Interior face | Surface | Face facing interior |
| Roof face | Surface | Roof-relevant exposed surface |
| Ground-contact face | Surface | Face near soil / ground |
| Facade interface | Surface | External wall / facade relation |
| Insulation interface | Surface | Face where insulation can attach |
| U-value thickness | Distance / line normal to surface | Thickness for rough U-value |
| Thermal bridge edge | Line or narrow zone | Heat-loss risk zone |
| Envelope penetration | Opening zone | Service/connector crossing envelope |
| Moisture-risk zone | Surface or edge zone | Water / moisture risk |

## Ports

| Port pattern | Geometry kind |
|---|---|
| envelope-interface-port | Surface |
| insulation-interface-port | Surface |
| roof-interface-port | Surface |
| ground-contact-port | Surface |
| thermal-bridge-edge-port | Line or narrow zone |
| envelope-penetration-port | Opening zone |

## Connector candidates

Energy does not usually create physical connector systems.  
It creates **crossing / interruption candidates**:

| Candidate | Geometry kind |
|---|---|
| thermal-bridge-candidate | Line / narrow zone |
| envelope-crossing-candidate | Zone |
| insulation-interruption-candidate | Surface / zone |
| moisture-risk-candidate | Surface / edge zone |

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
  ports: envelope_ports_if_needed
  connector_candidates: crossing_or_interruption_candidates
```

## Example A — DE_1OG_001 slab

### Ports

```text
roof-interface-port, if used as roof
envelope-interface-port, if used as exterior floor
insulation-interface-port, if insulation is attached
thermal-bridge-edge-port at slab edge
```

### Connector / interruption candidates

```text
slab-edge thermal-bridge-candidate
envelope-penetration-candidate if openings exist
insulation-interruption-candidate at connector locations
```

### System interpretation

```text
if used only inside:
energy relevance may be not applicable

if used as roof or exterior floor:
full assembly build-up is required
thermal bridge assessment is required at edges and connectors
```

---

## Example B — Wand–Decke

### Ports

```text
wall-envelope-interface-port, if wall is part of envelope
slab-edge thermal-bridge-edge-port
insulation-interface-port
```

### Connector / interruption candidates

```text
wall-slab thermal-bridge-candidate
steel-connector envelope-crossing-candidate
insulation-interruption-candidate
moisture-risk joint candidate
```

### System interpretation

```text
rough thermal warning possible
final Psi-value requires thermal bridge calculation
final U-value requires full layer build-up
exposed steel connector may need thermal separation or detailing
```

---

## Example C — SlabBeamColumnFragment

### Ports

```text
irregular-envelope-interface-port
insulation-interface-port around irregular geometry
thermal-bridge-edge-port at beam / column projections
```

### Connector / interruption candidates

```text
beam projection thermal-bridge-candidate
column-stub thermal-bridge-candidate
cut-face envelope-risk candidate
irregular insulation-interruption candidate
```

### System interpretation

```text
if used in envelope:
irregular geometry likely creates thermal bridge risk
full build-up and thermal bridge calculation are required
cut faces may need protection and insulation detailing
```

---

# 8. Package 3 — TGA / Openings Geometry

## Purpose

Create geometry for openings, penetrations, service routes, shafts, pipes, cables, and core drilling.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Existing opening | Void / opening volume | Existing pass-through |
| Opening boundary | Line / curve | Edge of opening |
| Opening face | Surface | Interior surface of opening |
| Core-drilling candidate | Cylindrical volume or circular surface zone | Possible new drilling |
| Cable route | Line / corridor zone | Cable path |
| Pipe route | Line / corridor volume | Pipe path |
| Shaft interface | Surface or volume zone | Shaft / vertical service interface |
| Blocked penetration zone | Surface or volume zone | Area to avoid |
| Edge distance | Quantity | Distance to edge |
| Service port | Opening or surface zone | Service interface |

## Ports

| Port pattern | Geometry kind |
|---|---|
| existing-opening-port | Opening zone |
| service-penetration-port | Opening or surface zone |
| core-drilling-port | Cylindrical candidate zone |
| cable-route-port | Line / corridor zone |
| pipe-route-port | Line / corridor volume |
| shaft-interface-port | Surface or volume zone |

## Connector candidates

| Candidate | Geometry kind |
|---|---|
| core-drilling-candidate | Cylindrical volume |
| sleeve-candidate | Cylindrical volume / opening zone |
| service-box-candidate | Volume zone |
| route-corridor-candidate | Line / corridor zone |

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
  connector_candidates: drilling_or_sleeve_candidates
  blocked_zones: zones
  edge_distances: quantities
```

## Example A — DE_1OG_001 slab

### Ports

```text
no existing-opening-port recorded in the given catalogue entry
possible core-drilling-port if system allows candidate generation
possible service-penetration-port if project context needs TGA route
```

### Connector candidates

```text
core-drilling-candidate = cylindrical volume
sleeve-candidate = cylindrical volume, only if drilling is allowed
```

### System interpretation

```text
rebar evidence required before drilling
structural zones must be avoided
fire / acoustic sealing may be required depending use
```

---

## Example B — Wand–Decke

### Ports

```text
vertical-service-pass-through-port if opening exists
horizontal-service-route-port along wall / slab zone
core-drilling-port only outside structural interface
```

### Connector candidates

```text
core-drilling-candidate away from bearing zone
sleeve-candidate if penetration is approved
service-route-corridor candidate
```

### System interpretation

```text
service penetrations near the structural connection require coordination
new drilling depends on reinforcement evidence
fire and acoustic sealing may be required depending use
```

---

## Example C — SlabBeamColumnFragment

### Ports

```text
service-penetration-port in slab zone
blocked service port near beam web
blocked service port near column stub
core-drilling-port only outside monolithic junctions
```

### Connector candidates

```text
core-drilling-candidate outside monolithic junction
sleeve-candidate in non-critical slab zone
route-corridor-candidate avoiding beam depth
```

### System interpretation

```text
beam and column zones are structurally sensitive
service penetrations should prefer non-critical slab zones
reinforcement evidence is required before drilling
```

---

# 9. Package 4 — Semantic / Architectural Interface Geometry

## Purpose

Create geometry for spatial, visual, facade, rhythm, alignment, identity, and reuse-expression relations.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Room-boundary interface | Surface | Defines space |
| Facade-rhythm interface | Surface, line, or module interval | Facade order |
| Visible-reuse interface | Surface or edge zone | Shows reused component |
| Ceiling expression | Surface | Visible underside |
| Floor surface | Surface | Walkable / floor finish relation |
| Exposed edge | Line or narrow surface zone | Visible edge expression |
| Joint line | Line | Visible joint |
| Datum alignment | Line / plane | Alignment reference |
| Grid continuation | Line / module spacing | Repetition / system order |
| Threshold interface | Line / surface zone | Spatial transition |
| Reuse identity display zone | Surface zone | ID / trace display |

## Ports

Semantic ports are architectural relation ports, not mechanical connectors.

| Port pattern | Geometry kind |
|---|---|
| room-boundary-port | Surface |
| facade-rhythm-port | Surface or line |
| visible-reuse-port | Surface or edge zone |
| ceiling-expression-port | Surface |
| floor-surface-port | Surface |
| exposed-edge-port | Line or strip |
| datum-alignment-port | Line or plane |
| grid-continuation-port | Line / spacing pattern |
| threshold-port | Line or surface zone |

## Connector candidates

Semantic geometry does not create physical connector systems.  
It creates **architectural relation candidates**:

| Candidate | Geometry kind |
|---|---|
| alignment-candidate | Line / plane |
| joint-expression-candidate | Line |
| visibility-candidate | Surface / edge zone |
| grid-continuation-candidate | Line / spacing pattern |
| reuse-identity-candidate | Surface zone |

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
  ports: semantic_ports
  relation_candidates: architectural_relation_candidates
```

## Example A — DE_1OG_001 slab

### Ports

```text
floor-surface-port at top face
ceiling-expression-port at bottom face
exposed-edge-port along long edges
grid-continuation-port based on slab width
reuse-identity-port if ID is visible
```

### Relation candidates

```text
joint-expression candidate
datum-alignment candidate
visible-reuse candidate
```

### System interpretation

```text
supports visible reuse preference
supports regular grid preference
surface expression depends on condition evidence
```

---

## Example B — Wand–Decke

### Ports

```text
room-boundary-port at wall face
ceiling-expression-port at slab underside
joint-line-port at wall-slab joint
datum-alignment-port at top of wall / slab edge
visible-reuse-port if connector remains exposed
```

### Relation candidates

```text
visible joint expression
room subdivision relation
ceiling datum relation
reuse identity display
```

### System interpretation

```text
can support room layout logic
can express joint and reuse identity
does not decide whether exposed connector is aesthetically desired
```

---

## Example C — SlabBeamColumnFragment

### Ports

```text
visible-reuse-port at monolithic junction
exposed-cut-face-port
beam-expression-port
column-stub-expression-port
grid-continuation-port from original structural bay
datum-alignment-port along slab edge
```

### Relation candidates

```text
reuse-story candidate
former-structural-bay expression candidate
cut-face expression candidate
ceiling-depth expression candidate
```

### System interpretation

```text
this typology can show the former structural bay
visible beam and column remnants can become an architectural feature
the system should not reduce it to generic slab semantics
```

---

# 10. Package 5 — Logistics / Assembly Geometry

## Purpose

Create geometry for storage, lifting, transport, access, assembly, protection, and temporary bracing.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Transport envelope | Volume | Transport size |
| Storage orientation | Orientation vector / state | How to store |
| Center of gravity | Point | Handling reference |
| Lifting candidate | Point or surface zone | Possible lifting place |
| Storage support | Surface zone or line support | Where to support in storage |
| Stacking interface | Surface zone | Where elements can stack |
| Assembly access | Volume / clearance zone | Required access |
| Installation clearance | Volume | Space needed for placement |
| Crane pick zone | Point or volume zone | Crane interaction |
| Temporary bracing | Surface or line zone | Temporary stability |
| Protection zone | Surface or edge zone | Needs protection |
| Damage-sensitive zone | Surface or edge zone | Avoid impact |

## Ports

| Port pattern | Geometry kind |
|---|---|
| lifting-port | Point or surface zone |
| crane-pick-port | Point or volume zone |
| storage-support-port | Surface or line zone |
| transport-support-port | Surface or line zone |
| stacking-port | Surface zone |
| assembly-access-port | Clearance volume |
| temporary-bracing-port | Surface or line zone |
| protection-port | Surface or edge zone |

## Connector candidates

| Candidate | Geometry kind |
|---|---|
| lifting-insert-candidate | Point / local surface zone |
| temporary-bracing-candidate | Surface or line zone |
| storage-support-candidate | Surface or line zone |
| transport-fixation-candidate | Surface or edge zone |

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
  lifting_ports: ports
  lifting_candidates: connector_candidates
  storage_supports: zones
  assembly_access: clearance_volumes
  protection_zones: zones
```

## Example A — DE_1OG_001 slab

### Ports

```text
storage-support-port at lower face
stacking-port at top / support strips
assembly-access-port along bearing edges
lifting-port candidates on top face or edge zones
```

### Connector candidates

```text
lifting-insert-candidate, if evidence or design allows
transport-fixation-candidate at edge zones
timber-separator support candidate as surface strips
```

### System interpretation

```text
recommended storage orientation = lying
separator required = true
weather protection recommended = true
lifting proof required if lifting points unknown
```

---

## Example B — Wand–Decke

### Ports

```text
wall-top assembly-access-port
slab lifting / placement port
joint access port
temporary-support-port if required
```

### Connector candidates

```text
temporary-bracing-candidate
temporary-support-candidate
transport-fixation-candidate
```

### System interpretation

```text
connection must remain accessible until completed
slab placement requires lifting / handling proof
assembly sequence must avoid blocking connector access
```

---

## Example C — SlabBeamColumnFragment

### Ports

```text
lifting-port candidates around stable regions
storage-support-port at custom support zones
temporary-bracing-port if column stub creates instability
protection-port at cut faces
assembly-access-port around beam and column projection
```

### Connector candidates

```text
lifting-insert-candidate only outside damaged / sensitive cut zones
temporary-bracing-candidate at column-stub or beam zone
transport-fixation-candidate at stable external faces
```

### System interpretation

```text
center of gravity may not be geometric center
special lifting planning likely required
cut faces and monolithic junctions may need protection
storage may require custom support
```

---

# 11. Package 6 — Evidence Geometry Overlay

## Purpose

Map evidence from scans, tests, photos, documents, and inspections onto geometry.

## Owns

| Item | Geometry kind | Meaning |
|---|---|---|
| Rebar line | Line / curve | Detected reinforcement |
| Rebar zone | Line buffer / volume zone | Reinforcement influence |
| Cover depth | Distance quantity | Concrete cover |
| Unknown rebar zone | Surface or volume zone | Missing scan confidence |
| Damage zone | Surface or volume zone | Local damage |
| Crack line | Line | Crack evidence |
| Spalling zone | Surface / edge zone | Missing concrete |
| Exposed rebar | Line or surface zone | Visible reinforcement |
| Core sample point | Point / cylindrical volume | Test extraction |
| Carbonation sample point | Point / depth line | Test location |
| Chloride sample point | Point | Test location |
| Photo-mapped surface | Surface | Photo evidence location |
| Confidence zone | Zone | Evidence confidence |

## Ports

```text
None by default.
Evidence overlays modify or block ports generated by other packages.
```

## Connector effects

Evidence does not create connector systems.  
It affects whether connector candidates are usable.

| Evidence overlay | Effect on ports / connectors |
|---|---|
| rebar-detected-zone | may block anchor or drilling candidate |
| unknown-rebar-zone | marks drilling as warning / blocked |
| damage-zone | may block bearing, lifting, or visible reuse |
| exposed-rebar-zone | durability warning, connection warning |
| core-sample-point | evidence marker, not connector |
| confidence-zone | changes confidence of generated ports |

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
  port_effects: blocking_or_warning_relations
```

## Example A — DE_1OG_001 slab

### Evidence overlays

```text
rebar scan = lines / zones if available
unknown rebar = zones if scan missing
damage = surface or edge zones if mapped
core sample = point / cylinder if tested
carbonation sample = point / depth line if tested
```

### Effect on ports / connectors

```text
unknown rebar zone blocks or warns anchor candidates
damage at slab edge warns slab-edge-bearing port
spalling at lifting region warns lifting-port candidate
```

---

## Example B — Wand–Decke

### Evidence overlays

```text
wall rebar = line / zone overlay
slab rebar = line / zone overlay
anchor-blocking zone = rebar buffer zone
bearing damage = overlap between damage zone and bearing zone
unknown rebar at joint = warning zone
```

### Effect on ports / connectors

```text
rebar conflict blocks anchor-candidate
unknown rebar warns post-installed-rebar-candidate
damage at wall top warns wall-top-bearing-port
damage at slab edge warns slab-edge-bearing-port
```

---

## Example C — SlabBeamColumnFragment

### Evidence overlays

```text
slab rebar = line / zone
beam rebar = line / zone
column rebar = line / zone
junction unknown rebar = volume zone
cut-face exposed rebar = line / surface zone
cracks near junction = crack lines
damage at cut faces = surface zones
```

### Effect on ports / connectors

```text
unknown rebar at monolithic junction blocks drilling
cut-face damage warns cut-face-risk-port
exposed rebar warns durability and connection use
cracks near beam-column junction warn structural interface use
```

---

# 12. Final Boundary

```text
Generator:
creates domain geometry, ports, interface regions, and connector candidates.

System:
maps generated geometry to connector systems, evidence status, project rules, and Bauteilpass fields.

Rule Checker:
evaluates active design actions and selected connections.
```

Example:

```text
Generator:
creates slab-edge-bearing-port and anchor-candidate zone.

System:
maps it to possible connector systems such as
nachträglicher Bewehrungsanschluss + Verguss
or Schraubanker mit Flachstahlhalter.

Rule Checker:
checks the actual slab-wall connection:
bearing overlap,
rebar evidence,
anchor distance,
fire context,
assembly access,
and LCA data.
```

---

# 13. Final Rule

```text
Do not create one generic connector package.

Create domain geometry packages.

Each package owns:
1. its geometry
2. its ports
3. its interface regions
4. its connector candidates
5. its rule-facing geometry
```
