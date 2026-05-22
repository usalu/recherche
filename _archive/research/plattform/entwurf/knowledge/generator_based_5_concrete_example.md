# Geometry-Generator-Based Bauteilpass System  
## Minimum Input → Geometry Generators → System Modules → Bauteilpass Interface

**Purpose**  
This document defines how a detailed **Piece Detail / Bauteilpass panel** is produced from minimal input.

**Corrected architecture**  
Generators do **only geometry-related work**.

They produce:

```text
geometry representations
geometry abstractions
zones
ports
faces
edges
openings
bounding data
geometry-tied quantities
```

The **system** does everything else:

```text
Semio binding
identity and traceability
availability
classification
evidence mapping
condition interpretation
structural prechecks
fire flags
building physics prechecks
services logic
logistics data
transport data
LCA / Ökobilanz
documentation
completeness
pool warnings
rule-checker readiness
```

---

# 1. System Overview

## 1.1 Main Pipeline

```text
Minimum Input
+ Base Geometry
+ Component Typology
        ↓
Geometry Generators
        ↓
Generated Geometry Representations
        ↓
System Modules
        ↓
Bauteilpass Data
        ↓
Piece Detail Panel
        ↓
Rule-Checker Readiness
```

## 1.2 What the User Provides

```yaml
minimum_input:
  component_id: DE_1OG_001
  component_typology: slab
  material_kind: reinforced_concrete

  base_geometry_reference: representations/DE_1OG_001/base.glb

  source_context:
    source_project: Abbau Aufbau
    source_building: donor-building-001
    original_level: 1OG
    original_function: floor_slab

  pool_context:
    kit_id: kit-abbau-aufbau-pool-001
    current_storage_location: storage-yard-01
    storage_position: A-03-02

  project_defaults:
    density_reinforced_concrete_kg_m3: 2400
    lambda_reinforced_concrete_W_mK: 2.3
    transport_factor_kgco2e_per_tkm: 0.05
    new_precast_concrete_reference_kgco2e_per_t: 171.7

  optional_evidence:
    concrete_test_report: null
    reinforcement_scan: null
    damage_photos: null
    fire_document: null
    lca_dataset: null
```

## 1.3 What Geometry Generators Produce

```text
normalized base geometry
physical geometry abstraction
structural geometry abstraction
energy / envelope geometry abstraction
semantic geometry abstraction
connector-zone geometry
ports
opening geometry
penetration candidates
logistics geometry
face / edge / zone maps
geometry-derived quantities
```

## 1.4 What System Modules Produce

```text
Semio binding
identity and traceability
availability state
classification
allowed / disallowed roles
material evidence status
condition and damage interpretation
reinforcement evidence status
structural data status
fire data status
building physics precheck
services status
logistics status
transport precheck
LCA precheck
documentation status
evidence completeness
pool warnings
rule-checker readiness
```

---

# 2. Core Concepts

## 2.1 Bauteilpass

A **Bauteilpass** is the digital passport of one real reclaimed component.

It combines:

```text
minimum identity data
generated geometry representations
catalogue data
evidence data
system-derived prechecks
documentation state
rule-checker readiness
```

## 2.2 Geometry Generator

A **Geometry Generator** is a preprogrammed typology-based module.

It receives:

```text
component typology
base geometry
project geometry defaults
optional geometry evidence
```

It outputs only geometry-related information:

```text
faces
edges
zones
ports
support regions
connector regions
opening regions
envelope regions
semantic face candidates
logistics geometry
geometry-derived quantities
```

It does **not** decide:

```text
final structural validity
material strength
fire resistance
LCA completeness
approval readiness
connection validity
design preference score
```

## 2.3 System Module

A **System Module** consumes generated geometry plus catalogue/context/evidence data.

It produces non-geometric Bauteilpass information:

```text
classification
evidence state
material state
rule-readiness state
warnings
logistics information
LCA prechecks
documentation completeness
```

---

# 3. Correct Responsibility Split

## 3.1 Geometry Generators

```text
GEO-0 Typology Geometry Selector
GEO-1 Base Geometry Normalizer
GEO-2 Physical Geometry Generator
GEO-3 Structural Geometry Generator
GEO-4 Energy / Envelope Geometry Generator
GEO-5 Semantic / Architectural Geometry Generator
GEO-6 Connector-Zone + Port Geometry Generator
GEO-7 Openings + Penetration Geometry Generator
GEO-8 Logistics Geometry Generator
```

## 3.2 System Modules

```text
SYS-1 Semio Binding Module
SYS-2 Identity + Traceability Module
SYS-3 Pool Availability Module
SYS-4 Classification Module
SYS-5 Material Evidence Module
SYS-6 Condition + Damage Module
SYS-7 Reinforcement Evidence Module
SYS-8 Structural Data Module
SYS-9 Connector / Interface Data Module
SYS-10 Fire Data Module
SYS-11 Building Physics Module
SYS-12 Services / TGA Module
SYS-13 Logistics Module
SYS-14 Transport Module
SYS-15 LCA / Ökobilanz Module
SYS-16 Documentation Module
SYS-17 Completeness Module
SYS-18 Pool Warning Module
SYS-19 Rule-Checker Readiness Module
```

## 3.3 Responsibility Matrix

| Part | Does | Does not do |
|---|---|---|
| **Geometry Generators** | create geometry representations, zones, ports, faces, openings, support regions | decide final validity, evidence, LCA, fire, approval |
| **System Modules** | interpret generated geometry with context, evidence, defaults, and rule libraries | create raw geometry |
| **Rule Checker** | evaluates active placements/connections | store raw pool data |
| **Bauteilpass Panel** | displays pool and generated component data | show active connection results |
| **Connection Passport** | stores A+B connection result | replace Bauteilpass |

---

# 4. Typology Library for Geometry Generators

Each component typology defines how its geometry should be abstracted.

## 4.1 Slab

```yaml
typology:
  id: slab

  geometry_expectation:
    shape: thin_plate
    main_faces:
      - top
      - bottom
    primary_edges:
      - long_edges
      - short_edges

  geometry_outputs:
    - physical_geometry
    - structural_geometry
    - energy_geometry
    - semantic_geometry
    - connector_zone_geometry
    - logistics_geometry

  generated_ports:
    - slab-edge-bearing
    - slab-top-service-zone
    - slab-envelope-face

  generated_zones:
    - top_face
    - bottom_face
    - long_edge_bearing_zones
    - short_edge_candidate_zones
    - opening_zones
    - no_drill_candidates
    - lifting_face_candidates
```

## 4.2 Beam

```yaml
typology:
  id: beam

  geometry_expectation:
    shape: long_horizontal_prism

  geometry_outputs:
    - beam_axis
    - beam_end_zones
    - top_bearing_surface
    - side_faces
    - lifting_candidates

  generated_ports:
    - beam-end-bearing
    - beam-top-bearing
    - beam-side-connector
```

## 4.3 Wall Panel

```yaml
typology:
  id: wall_panel

  geometry_expectation:
    shape: vertical_plate

  geometry_outputs:
    - broad_faces
    - bottom_bearing_edge
    - top_bearing_edge
    - side_joint_edges
    - opening_zones
    - facade_or_room_face_candidates

  generated_ports:
    - wall-bottom-bearing
    - wall-top-bearing
    - wall-side-joint
    - wall-face-connector
```

## 4.4 Column

```yaml
typology:
  id: column

  geometry_expectation:
    shape: vertical_prism

  geometry_outputs:
    - column_axis
    - base_face
    - head_face
    - side_faces
    - lifting_candidates

  generated_ports:
    - column-base-bearing
    - column-head-bearing
    - column-side-stability-connector
```

## 4.5 Mushroom Column

```yaml
typology:
  id: mushroom_column

  geometry_expectation:
    shape: vertical_column_with_capital

  geometry_outputs:
    - shaft_zone
    - capital_zone
    - base_face
    - mushroom_head_bearing_region
    - punching_sensitive_interface_region
    - lifting_candidates
    - special_storage_geometry

  generated_ports:
    - column-base-bearing
    - mushroom-head-bearing
    - capital-slab-interface
    - column-side-stability-connector
```

---

# 5. Shared Geometry Calculations

## 5.1 Oriented Bounding Box

```text
OBB = oriented_bounding_box(base_geometry)
```

Output:

```text
principal axes
length
width
height / thickness
bounding dimensions
```

## 5.2 Volume

```text
net_volume_m3 = solid_volume(base_geometry)
```

Fallback:

```text
net_volume_m3 =
length_m × width_m × thickness_m
- detected_opening_volume_m3
```

## 5.3 Face Areas

```text
face_area_m2 = area(face_geometry)
total_surface_area_m2 = sum(face_area_m2)
```

## 5.4 Opening Geometry

```text
openings = detect_voids(base_geometry)
```

For each opening:

```text
opening_position = centroid(opening)
opening_size = diameter or bounding box
opening_depth = through-depth or recess-depth
edge_distance = distance(opening_boundary, nearest_component_edge)
```

## 5.5 Geometry-Derived Mass

The Geometry Generator gives volume.  
The System calculates mass.

```text
mass_kg = net_volume_m3 × material_density_kg_m3
```

## 5.6 Geometry-Derived Self-Weight

The System calculates self-weight from mass.

```text
self_weight_kN = mass_kg × 9.81 / 1000
```

For slabs:

```text
self_weight_kN_m2 = self_weight_kN / plan_area_m2
```

## 5.7 Rough U-Value Precheck

The Energy Geometry Generator identifies relevant thickness and faces.  
The System calculates the rough precheck.

```text
R_concrete = thickness_m / lambda_concrete_W_mK

U_rough = 1 / (Rsi + R_concrete + Rse)
```

## 5.8 Transport GWP Precheck

The Geometry Generator does not calculate LCA.  
The System calculates it using mass and transport context.

```text
transport_gwp_kgco2e =
mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

## 5.9 Avoided GWP Potential

```text
avoided_gwp_potential_kgco2e =
mass_t × new_equivalent_reference_kgco2e_per_t
```

---

# 6. Piece Detail Panel Structure

The interface is organized into:

```text
0. Header / Quick Summary
1. Semio Binding
2. Identity + Traceability
3. Pool Availability
4. Classification
5. Geometry Overview
6. Geometry Representations
7. Physical Geometry
8. Structural Geometry
9. Energy / Envelope Geometry
10. Semantic / Architectural Geometry
11. Openings + Penetrations
12. Surface + Edge Condition
13. Damage Records
14. Concrete Evidence
15. Reinforcement Evidence
16. Durability + Restnutzungsdauer
17. Structural Data
18. Connector / Interface Data
19. Bohrzonen / No-Drill Zones
20. Fire Data
21. Building Physics Data
22. Acoustic Data
23. TGA / Services Data
24. Logistics Data
25. Transport Data
26. LCA / Ökobilanz Data
27. Documentation
28. Evidence Completeness
29. Pool-Level Warnings
30. Rule-Checker Readiness
31. What Should Not Be Shown
```

Each section is structured as:

```text
Visible details
Minimum input
Geometry generator output
System output
Proof
Must remain unknown
```

---

# 7. Detailed Section Specification

---

## 0. Header / Quick Summary

### Visible Details

```text
Component ID
Component name
Element kind
Material
Current availability
Current storage location
Thumbnail / sketch
Main dimensions
Mass
Evidence completeness
Tracking code
```

### Minimum Input

```text
component_id
component_typology
material_kind
base_geometry_reference
current_storage_location
```

### Geometry Generator Output

```text
main dimensions
net volume
preview geometry / thumbnail source
```

### System Output

```text
component name
material label
availability
mass
evidence completeness
tracking code
```

### Proof

```text
component_name =
human_label(component_typology) + " " + component_id

dimensions =
OBB(base_geometry)

net_volume =
solid_volume(base_geometry)

mass =
net_volume × material_density_default

availability =
stock_total - active_piece_count - reserved_count

tracking_code =
existing QR/RFID/BIM reference
or generated "QR-" + component_id

evidence_completeness =
available_required_fields / required_fields
```

### Must Remain Unknown

```text
measured mass if density is assumed
physical marking status if not recorded
true availability if storage is not synced
```

---

## 1. Semio Binding

### Visible Details

```text
Kit ID
Kit name
Type ID
Type name
Parent type
Type kind
Stock quantity
Available quantity
Current Piece IDs using this Type
Attribute namespace
Quality namespace
Representation list
Connector list
```

### Minimum Input

```text
kit_id
component_id
component_typology
material_kind
base_geometry_reference
```

### Geometry Generator Output

```text
generated representations
generated connector-zone geometry
generated ports
```

### System Output

```text
kit name
type ID
type name
parent type
type kind
stock total
stock available
current piece IDs
namespaces
representation registry
connector registry
```

### Proof

```text
type_id =
"type-" + component_id

parent_type =
"type-reclaimed-" + component_typology

type_kind =
"reclaimed-" + material_kind + "-" + component_typology

stock_total =
1 for individual reclaimed component unless catalogue quantity says otherwise

stock_available =
stock_total - active_piece_count

current_piece_ids =
query design graph by type_id

representations =
base representation + generated geometry representations

connectors =
generated ports registered as Semio connectors
```

### Must Remain Unknown

```text
custom parent taxonomy if project does not define it
true stock if multiple real components are grouped
manual connector overrides
```

---

## 2. Identity + Traceability

### Visible Details

```text
Component ID
Human-readable name
Element type
Material type
Source project
Source building
Original level
Original zone
Original function
Original orientation
Tracking method
QR code
RFID code
BIM GUID
External database reference
Physical marking status
```

### Minimum Input

```text
component_id
component_typology
material_kind
source_project
source_building_id
```

### Geometry Generator Output

```text
orientation candidates
top/bottom candidates
principal axes
```

### System Output

```text
human-readable name
element type label
source level
source zone
original function candidate
tracking method
QR code
internal GUID
external reference
```

### Proof

```text
human_readable_name =
component_id + " (" + component_typology + ")"

source_level =
parse level token from component_id
or use source_context.original_level

original_function =
source_context.original_function
or typology default:
slab → floor_slab
beam → beam
wall → wall_panel
column → column
mushroom_column → column_with_capital

orientation =
geometry principal axes + typology rules

qr_code =
"QR-" + component_id

internal_guid =
system-generated UUID

external_reference =
catalogue_path(component_id)
```

### Must Remain Unknown

```text
real RFID if not scanned
physical marking status
true original orientation if geometry is ambiguous
```

---

## 3. Pool Availability

### Visible Details

```text
Availability state
Storage state
Reservation state
Used count
Stock total
Stock available
Blocked reason
Reserved design
Linked placed pieces
```

### Minimum Input

```text
component_id
stock rule
design graph access
storage location
```

### Geometry Generator Output

```text
none
```

### System Output

```text
used count
stock available
availability state
storage state
linked piece IDs
reservation status
```

### Proof

```text
stock_total =
1 for individual reclaimed element unless quantity is provided

used_count =
count(piece where piece.type_id == type_id)

reserved_count =
count(reservation where reservation.type_id == type_id)

stock_available =
stock_total - used_count - reserved_count

availability_state:
blocked_reason exists → blocked
reserved_count > 0 → reserved
used_count > 0 → placed
stock_available > 0 → available
else unavailable
```

### Must Remain Unknown

```text
manual off-system reservations
actual physical presence if storage is not synchronized
new damage after catalogue creation
```

---

## 4. Classification

### Visible Details

```text
Primary element kind
Secondary classifications
Material family
Structural family
Allowed design roles
Disallowed design roles
Semantic tags
Reuse category
Risk category
```

### Minimum Input

```text
component_typology
material_kind
base_geometry_reference
```

### Geometry Generator Output

```text
shape class
principal dimensions
semantic face candidates
structural zone candidates
```

### System Output

```text
primary kind
secondary classifications
material family
structural family
allowed roles
disallowed roles
semantic tags
reuse category
risk category
```

### Proof

```text
primary_kind =
component_typology

structural_family:
slab → horizontal_spanning
beam → horizontal_line_support
wall → vertical_panel
column → vertical_point_support
mushroom_column → vertical_point_support_with_capital

allowed_roles =
typology role library

disallowed_roles =
roles incompatible with typology unless engineered

risk_category =
missing evidence + damage + unknown structural capacity
```

### Must Remain Unknown

```text
approved alternative role without engineering proof
actual load-bearing category without evidence
```

---

## 5. Geometry Overview

### Visible Details

```text
Unit system
Length
Width
Height / thickness
Bounding box
Gross volume
Net volume
Mass
Density
Center of gravity
Original top face
Original bottom face
Local X axis
Local Y axis
Local Z axis
Geometry tolerance
Placement tolerance
Joint tolerance
```

### Minimum Input

```text
base_geometry_reference
component_typology
material_kind
```

### Geometry Generator Output

```text
unit system
principal axes
bounding box
length
width
height / thickness
gross volume
net volume
center of gravity
top/bottom candidates
local axes
```

### System Output

```text
density
mass
geometry tolerance
placement tolerance
joint tolerance
```

### Proof

```text
dimensions =
OBB(base_geometry)

net_volume =
solid_volume(base_geometry)

density =
measured value if available
else material default

mass =
net_volume × density

center_of_gravity =
volume centroid

top/bottom:
slab → largest parallel faces
wall → vertical broad faces + bottom edge
column → bottom/top faces along vertical axis

tolerances =
project defaults
```

### Must Remain Unknown

```text
measured density
internal voids not represented in geometry
true original top/bottom if inference conflicts with metadata
actual fabrication tolerance
```

---

## 6. Geometry Representations

### Visible Details

```text
Physical geometry
Structural geometry
Energy / envelope geometry
Semantic geometry
Connector-zone geometry
Logistics geometry
Catalogue sketch
Photos
Scan data
BIM model
```

### Minimum Input

```text
base_geometry_reference
component_typology
material_kind
```

### Geometry Generator Output

```text
physical representation
structural geometry representation
energy / envelope geometry representation
semantic geometry representation
connector-zone geometry
logistics geometry
generated tags
confidence levels
```

### System Output

```text
representation registry
representation labels
missing representation flags
source / confidence display
```

### Proof

```text
physical representation =
normalized base geometry

structural representation =
typology-specific support zones, span candidates, load direction zones

energy representation =
faces and edges relevant to envelope / thermal precheck

semantic representation =
inside/outside candidates, room/facade candidates, visible faces

connector-zone representation =
ports, bearing regions, anchor candidates, service zones

logistics representation =
lifting candidates, storage orientation geometry, transport envelope
```

### Must Remain Unknown

```text
true semantic meaning without context
true structural proof
true energy compliance
```

---

## 7. Physical Geometry

### Visible Details

```text
Shape type
Exact dimensions
Surface geometry
Edge geometry
Opening geometry
Cut-outs
Chamfers
Irregularities
Surface damage location
Edge damage location
Physical tolerance
```

### Minimum Input

```text
base_geometry_reference
component_typology
```

### Geometry Generator Output

```text
shape type
faces
edges
openings
cut-outs
chamfers
irregularities
physical tolerance estimate
geometry anomaly candidates
```

### System Output

```text
damage candidate labels only if supported by evidence
surface / edge condition status if evidence exists
```

### Proof

```text
shape_type =
typology + aspect ratio classification

faces =
extract from solid or mesh

edges =
extract boundary curves

openings =
detect through-voids

cutouts =
detect non-through recesses

chamfers =
detect bevelled edge topology

irregularities =
deviation from ideal typology primitive

physical_tolerance =
deviation from fitted planes / surfaces
```

### Must Remain Unknown

```text
whether irregularity is damage or intentional
small cracks below scan resolution
surface contamination without visual/lab evidence
```

---

## 8. Structural Geometry

### Visible Details

```text
Structural role
Span direction
Main reinforcement direction
Secondary reinforcement direction
Support edges
Bearing zones
Point-support zones
Line-support zones
Load direction
Preferred support condition
Forbidden support condition
Minimum bearing length
Structural thickness
Structural openings
```

### Minimum Input

```text
component_typology
base_geometry_reference
original_function optional
```

### Geometry Generator Output

```text
support edge candidates
bearing zones
line-support zones
point-support candidates
load direction zones
structural thickness
structural openings
span direction candidate
```

### System Output

```text
structural role
preferred support condition
forbidden support condition
minimum bearing length
reinforcement direction status
```

### Proof

```text
slab:
bearing zones generated on support-relevant edges

beam:
bearing zones generated at beam ends and top face

wall:
bearing/support zones generated at bottom/top edges and side joints

column:
point-support zones generated at base and head

mushroom_column:
shaft zone + capital/head bearing region generated

structural_openings =
openings intersecting generated support/load zones

minimum_bearing_length =
project / typology rule, not geometry generator
```

### Must Remain Unknown

```text
actual load capacity
moment capacity
shear capacity
punching resistance
true reinforcement layout without scan
```

---

## 9. Energy / Envelope Geometry

### Visible Details

```text
Envelope relevance
Exterior faces
Interior faces
Ground-contact faces
Roof faces
Thermal boundary faces
Insulation-relevant faces
Thermal bridge risk zones
Moisture risk zones
U-value-relevant surfaces
```

### Minimum Input

```text
component_typology
base_geometry_reference
material_kind
intended_exposure_context optional
```

### Geometry Generator Output

```text
face candidates
thermal boundary candidate faces
edge zones
connector-crossing candidates
moisture-risk geometry candidates
U-value-relevant thickness
```

### System Output

```text
envelope relevance
exterior / interior status
thermal bridge warnings
moisture risk status
rough U-value precheck
insulation requirement flag
```

### Proof

```text
thermal_boundary_faces =
generated candidate faces based on context and face orientation

thermal_bridge_zones =
connector zones crossing generated thermal boundary
+ exposed slab/wall edges

moisture_risk_zones =
ground-contact candidates + roof candidates + exposed horizontal faces

R_concrete =
thickness / lambda_concrete

U_rough =
1 / (Rsi + R_concrete + Rse)
```

### Must Remain Unknown

```text
final U-value
thermal bridge Psi-value
moisture proof
inside/outside without design context
```

---

## 10. Semantic / Architectural Geometry

### Visible Details

```text
Inside / outside side
Room-facing side
Facade-facing side
Visible surface side
Hidden surface side
Original use side
Potential new use
Spatial role
Room boundary role
Facade rhythm relevance
Visible reuse potential
Surface expression value
```

### Minimum Input

```text
component_typology
base_geometry_reference
source_context
target_use_context optional
```

### Geometry Generator Output

```text
room-facing face candidates
facade-facing face candidates
visible face candidates
hidden face candidates
original-use-side candidates
semantic zone geometry
```

### System Output

```text
potential new use
spatial role
room boundary role
facade rhythm relevance
visible reuse potential
surface expression value
```

### Proof

```text
original_use_side:
slab top → floor side candidate
slab bottom → ceiling side candidate
wall broad faces → room/facade candidates
column sides → visible structural face candidates

visible_faces =
faces not covered by generated support zones or hidden layer flags

surface_expression_value =
visible area × visual quality × visible reuse preference
```

### Must Remain Unknown

```text
actual architectural intention
inside/outside without context
visual quality if no scan/photo/inspection exists
```

---

## 11. Openings + Penetrations

### Visible Details

```text
Opening ID
Opening type
Opening position
Opening size
Opening depth
Opening purpose
Original service use
Edge distance
Relation to reinforcement
Reusable for services
Blocked opening
Unknown opening
```

### Minimum Input

```text
base_geometry_reference
component_typology
```

### Geometry Generator Output

```text
detected openings
opening geometry
opening position
opening size
opening depth
edge distance
penetration candidates
```

### System Output

```text
opening ID
opening type label
relation to reinforcement
service reuse candidate
blocked opening status
unknown opening status
```

### Proof

```text
openings =
detect through-voids and recesses

opening_position =
centroid(opening geometry)

opening_size =
diameter or bounding dimensions

edge_distance =
distance from opening boundary to nearest edge

blocked =
opening overlaps bearing zone, damaged zone, or no-drill zone
```

### Must Remain Unknown

```text
original purpose without documentation
approval for new service use
hidden rebar conflict without scan
```

---

## 12. Surface + Edge Condition

### Visible Details

```text
Top face condition
Bottom face condition
Side face condition
Edge condition
Spalling
Cracks
Exposed reinforcement
Surface contamination
Repair marks
Visual quality
Visible reuse quality
```

### Minimum Input

```text
base_geometry_reference
photos_or_scan optional
```

### Geometry Generator Output

```text
face map
edge map
geometric anomaly candidates
surface zones
edge zones
```

### System Output

```text
surface condition
edge condition
spalling candidate status
crack status
exposed reinforcement status
visual quality
visible reuse quality
```

### Proof

```text
face classification =
generated from typology and geometry normals

geometric anomalies =
deviation from ideal typology primitive

condition labels =
from visual evidence, scan evidence, or manual inspection

visible_reuse_quality =
visual_quality × generated visible_face_area × semantic visibility
```

### Must Remain Unknown

```text
subsurface damage
chloride contamination
microcracks
surface contamination without evidence
```

---

## 13. Damage Records

### Visible Details

```text
Damage ID
Damage type
Damage location
Severity
Affected face / edge
Size
Photo reference
Repair status
Rule relevance
Notes
```

### Minimum Input

```text
base_geometry_reference
damage_photo_or_scan optional
```

### Geometry Generator Output

```text
damage-location geometry candidates
affected face / edge candidates
damage size if geometric anomaly exists
```

### System Output

```text
damage ID
damage type
severity candidate
rule relevance
repair status
notes
```

### Proof

```text
damage location =
mapped to generated face/edge geometry

severity =
damage size × overlap with bearing/connector/visible zones

rule relevance:
overlap with bearing zone → structural/interface relevance
overlap with visible face → architectural relevance
exposed rebar → durability relevance
```

### Must Remain Unknown

```text
cause of damage
repair status if undocumented
final structural severity without expert review
```

---

## 14. Concrete Evidence

### Visible Details

```text
Concrete strength
Test method
Test date
Test document
Compressive strength
Tensile strength
E-modulus
Density
Carbonation depth
Chloride content
Pollutant content
Moisture status
Evidence confidence
```

### Minimum Input

```text
material_kind
optional concrete evidence documents
```

### Geometry Generator Output

```text
none
```

### System Output

```text
density default
concrete evidence status
missing concrete evidence flags
confidence level
estimated material values if allowed
```

### Proof

```text
density =
tested value
or project material default

compressive_strength =
test/report only

E_modulus =
test/report
or estimated from compressive strength if project permits

carbonation_depth =
test only

chloride_content =
lab test only

confidence:
tested → high
documented → medium
estimated/default → low
unknown → none
```

### Must Remain Unknown

```text
real concrete strength without test
chloride content
pollutants
carbonation depth
moisture condition
```

---

## 15. Reinforcement Evidence

### Visible Details

```text
Reinforcement position status
Main reinforcement direction
Secondary reinforcement direction
Cover top
Cover bottom
Cover sides
Rebar scan reference
Rebar condition
Corrosion risk
No-drill zones
Drill-approved zones
Anchor-approved zones
Unknown reinforcement zones
```

### Minimum Input

```text
component_typology
base_geometry_reference
optional rebar scan / reinforcement drawing
```

### Geometry Generator Output

```text
candidate reinforcement zones
support zones
connector zones
no-drill geometry candidates
```

### System Output

```text
reinforcement direction candidate
position status
cover status
no-drill zones
drill-approved zones if evidence exists
anchor-approved zones if evidence exists
corrosion risk candidate
```

### Proof

```text
main_reinforcement_direction =
scan/drawing if available
else inferred from typology and span direction

cover =
scan/drawing/test only

no_drill_zones =
known rebar zones + edge buffers + bearing zones

if rebar map missing:
all drilling zones = unknown or blocked

drill_approved_zones =
connector zones - rebar buffers - edge buffers - damaged zones
```

### Must Remain Unknown

```text
true rebar location
safe anchor zones without scan
cover depth
internal corrosion
```

---

## 16. Durability + Restnutzungsdauer

### Visible Details

```text
Durability status
Carbonation risk
Chloride risk
Corrosion risk
Freeze-thaw risk
Moisture exposure risk
Estimated remaining service life
Repair requirement
Protection requirement
```

### Minimum Input

```text
material_kind
storage/exposure context
condition status optional
```

### Geometry Generator Output

```text
exposed face candidates
moisture-risk geometry candidates
damage-zone geometry if available
```

### System Output

```text
durability status
carbonation risk
chloride risk
corrosion risk
freeze-thaw risk
moisture exposure risk
repair requirement
protection requirement
remaining service life status
```

### Proof

```text
carbonation_risk =
carbonation_depth compared to concrete cover

chloride_risk =
lab chloride value

corrosion_risk =
carbonation risk + chloride risk + exposed rebar + rust marks

moisture_risk =
ground / roof / outdoor storage / exposed horizontal faces

repair_required =
medium/critical damage or exposed rebar
```

### Must Remain Unknown

```text
reliable remaining service life
internal corrosion
chloride risk without lab test
```

---

## 17. Structural Data

### Visible Details

```text
Structural role
Load-bearing status
Self weight
Allowed support types
Allowed bearing zones
Allowed span direction
Maximum reuse span
Known load capacity
Capacity evidence status
Required proof status
Original structural function
```

### Minimum Input

```text
component_typology
material_kind
base_geometry_reference
source_context original_function optional
```

### Geometry Generator Output

```text
structural geometry
bearing zones
support zones
span candidate
plan area
volume
```

### System Output

```text
structural role
load-bearing status candidate
self weight
allowed support types
allowed bearing zones
allowed span direction candidate
maximum reuse span candidate
capacity evidence status
proof requirement status
```

### Proof

```text
self_weight_kN =
mass_kg × 9.81 / 1000

allowed_support_types =
typology structural library

maximum_reuse_span =
dimension in generated span direction
not verified capacity

capacity_evidence_status =
known only if test/static proof exists

required_proof_status =
structural use + unknown capacity → proof_required
```

### Must Remain Unknown

```text
final load capacity
punching resistance
moment capacity
shear capacity
allowable live load
```

---

## 18. Connector / Interface Data

### Visible Details

```text
Connector ID
Connector name
Connector type
Port
Compatible ports
Mandatory or optional
Direction
Geometry reference
Allowed connection role
Allowed connector systems
Minimum bearing length
Maximum gap
Edge distance requirement
Drilling permission
Fire check required
Structural check required
Thermal check required
Service check required
Reversibility preference
```

### Minimum Input

```text
component_typology
base_geometry_reference
project connector library
```

### Geometry Generator Output

```text
connector-zone geometry
port geometry
port directions
bearing regions
service regions
envelope interface regions
edge distance geometry
```

### System Output

```text
connector ID
connector name
connector type
compatible ports
mandatory / optional status
allowed connection role
allowed connector systems
minimum bearing length
maximum gap
edge distance requirement
drilling permission
required checks
reversibility preference
```

### Proof

```text
port examples:
slab edge → slab-edge-bearing
wall top → wall-top-bearing
beam top → beam-top-bearing
column head → column-head-bearing
mushroom capital → mushroom-head-bearing
service opening → service-penetration
envelope face → thermal-envelope-interface

compatible_ports =
lookup connector library

allowed_connector_systems =
pair-type connector library

drilling_permission =
rebar evidence + no-drill zones

required checks =
structural / fire / thermal / service depending context and connector role
```

### Must Remain Unknown

```text
connector capacity without connector detail
safe drilled connector without rebar evidence
actual reversibility of custom connector
```

---

## 19. Bohrzonen / No-Drill Zones

### Visible Details

```text
Approved drilling zones
Forbidden drilling zones
Unknown drilling zones
Approved anchor zones
Forbidden anchor zones
Minimum edge distance
Minimum spacing
Concrete cover requirement
Rebar conflict status
Scan confidence
```

### Minimum Input

```text
component_typology
base_geometry_reference
project drilling defaults
optional rebar scan
```

### Geometry Generator Output

```text
connector zones
edge buffers
opening buffers
bearing zones
damage-zone geometry if available
```

### System Output

```text
forbidden zones
unknown zones
approved drilling zones if evidence exists
approved anchor zones if evidence exists
edge distance rules
spacing rules
rebar conflict status
scan confidence
```

### Proof

```text
forbidden_zones =
bearing zones + damaged zones + edge buffers + opening buffers + known rebar buffers

unknown_zones =
zones without rebar evidence

approved_drilling_zones =
connector zones - forbidden zones - unknown zones

approved_anchor_zones =
approved drilling zones satisfying anchor depth and spacing
```

### Must Remain Unknown

```text
approved drilling without rebar evidence
anchor pull-out capacity
hidden conflicts
```

---

## 20. Fire Data

### Visible Details

```text
Material fire class
Known fire resistance
Evidence status
Fire-relevant surfaces
Connector fire warning conditions
Exposed steel warning
Fire cover requirement if connected
```

### Minimum Input

```text
material_kind
component_typology
project fire defaults
```

### Geometry Generator Output

```text
fire-relevant face candidates
connector exposure geometry candidates
```

### System Output

```text
material fire class candidate
known fire resistance status
connector fire warning conditions
exposed steel warning condition
fire cover requirement condition
```

### Proof

```text
reinforced concrete =
non-combustible material assumption

known_fire_resistance =
only from test/calculation/document

exposed_steel_warning =
true for connector systems with exposed steel

fire_cover_required_if =
exposed steel connector in fire-relevant context
```

### Must Remain Unknown

```text
actual fire resistance rating
fire compartment compliance
connector fire resistance without detail
```

---

## 21. Building Physics Data

### Visible Details

```text
Thermal conductivity
Density
Specific heat capacity
U-value data
Envelope relevance
Insulation requirement if envelope
Thermal bridge zones
Moisture risk
Ground-contact suitability
Roof suitability
Acoustic relevance
```

### Minimum Input

```text
material_kind
component_typology
base_geometry_reference
exposure_context optional
project thermal defaults
```

### Geometry Generator Output

```text
thickness
thermal boundary candidate faces
thermal bridge geometry candidates
moisture-risk geometry candidates
surface areas
```

### System Output

```text
thermal conductivity estimate
density
specific heat estimate
rough U-value
envelope relevance
insulation requirement flag
thermal bridge zones
moisture risk
ground/roof suitability warning
acoustic relevance
```

### Proof

```text
R_concrete =
thickness / lambda

U_rough =
1 / (Rsi + R_concrete + Rse)

insulation_required =
if envelope relevant and U_rough above target

thermal_bridge_zones =
connector zones crossing envelope + exposed edges
```

### Must Remain Unknown

```text
final U-value
thermal bridge Psi-value
moisture proof
actual acoustic value
```

---

## 22. Acoustic Data

### Visible Details

```text
Mass relevance
Airborne sound data
Impact sound data
Acoustic evidence status
Recommended acoustic use
Acoustic warning
```

### Minimum Input

```text
component_typology
material_kind
base_geometry_reference
```

### Geometry Generator Output

```text
surface area
plan area
volume
thickness
```

### System Output

```text
mass per area
mass relevance
recommended acoustic use candidate
acoustic warning
evidence status
```

### Proof

```text
mass_per_area =
mass_kg / area_m2

mass_relevance =
true if mass_per_area exceeds project threshold

airborne_sound_data =
test/database/calculation only

impact_sound_data =
requires assembly build-up
```

### Must Remain Unknown

```text
actual airborne sound rating
impact sound performance
flanking transmission
```

---

## 23. TGA / Services Data

### Visible Details

```text
Existing service openings
Approved service zones
Blocked service zones
Possible cable penetrations
Possible pipe penetrations
Core drilling allowed
Core drilling blocked
Rebar scan required for services
```

### Minimum Input

```text
base_geometry_reference
component_typology
optional service context
```

### Geometry Generator Output

```text
opening geometry
penetration candidates
service-zone candidates
connector/service port geometry
edge distances
```

### System Output

```text
existing service openings
approved service zone candidates
blocked service zones
possible cable penetrations
possible pipe penetrations
core drilling status
rebar scan requirement
```

### Proof

```text
existing_openings =
detected openings

approved_service_zones =
existing openings + zones outside bearing/no-drill/rebar zones

blocked_service_zones =
bearing zones + no-drill zones + damaged structural zones

core_drilling_allowed =
approved zone + rebar data + edge distance ok
```

### Must Remain Unknown

```text
actual TGA route fit
fire/acoustic sealing
safe drilling without rebar evidence
```

---

## 24. Logistics Data

### Visible Details

```text
Current storage location
Storage position
Recommended storage orientation
Forbidden storage orientation
Weather protection required
Separator required
Mass
Lifting point status
Lifting points
Transport mode
Transport readiness
Load securing required
Damage protection required
Temporary bracing requirement
Assembly access zones
Installation notes
```

### Minimum Input

```text
component_typology
base_geometry_reference
material_kind
storage location
```

### Geometry Generator Output

```text
transport envelope
center of gravity
candidate lifting regions
storage orientation geometry
assembly access zones
connector access faces
```

### System Output

```text
recommended storage orientation
forbidden storage orientation
weather protection requirement
separator requirement
mass
lifting point status
transport mode
transport readiness
load securing
damage protection
temporary bracing candidate
installation notes
```

### Proof

```text
mass =
volume × density

storage orientation:
slab → lying flat
beam → supported at generated support zones
wall → standing only with support or engineering_required
column → stable storage depending slenderness
mushroom column → special support due to capital/head geometry

assembly_access_zones =
connector zones + required installation faces
```

### Must Remain Unknown

```text
safe lifting design
actual crane radius
site access
```

---

## 25. Transport Data

### Visible Details

```text
Transport mode
Transport distance
Transport factor
Transport emissions status
Maximum transport size
Special transport required
Protection requirement
Load securing note
```

### Minimum Input

```text
storage location
target site location
project transport defaults
```

### Geometry Generator Output

```text
transport dimensions
transport envelope
```

### System Output

```text
transport mass
transport distance
transport mode
transport GWP
special transport flag
protection requirement
load securing note
```

### Proof

```text
transport_distance =
route_distance(storage, target_site)

transport_mode =
project default unless dimensions/mass exceed threshold

transport_gwp =
mass_t × distance_km × transport_factor

special_transport_required =
component dimensions or mass exceed transport limits
```

### Must Remain Unknown

```text
actual route restrictions
transport permit requirements
exact emissions without route/mode
```

---

## 26. LCA / Ökobilanz Data

### Visible Details

```text
Material
Mass
Reused mass
A1-A3 reuse assumption
Transport factor
Transport distance
New equivalent reference
New equivalent GWP
Avoided GWP potential
EPD dataset
Ökobaudat dataset
Generic dataset status
LCA completeness
Environmental indicators
```

### Minimum Input

```text
material_kind
component_typology
base_geometry_reference
project_lca_defaults
storage and target location if transport included
```

### Geometry Generator Output

```text
volume
surface area
dimensions
```

### System Output

```text
material
mass
reused mass
A1-A3 reuse assumption
transport impact
new equivalent reference
avoided GWP potential
dataset status
LCA completeness
indicator placeholders
```

### Proof

```text
reused_mass =
mass

A1-A3 reuse assumption =
0 kgCO2e/t if project uses reuse assumption

transport_gwp =
mass_t × distance_km × transport_factor

new_equivalent_reference =
map typology + material to reference dataset

avoided_gwp_potential =
mass_t × new_equivalent_gwp_per_t
```

### Must Remain Unknown

```text
full LCA without datasets
connector-specific impact
adapter impact
module B/C/D values
non-GWP indicators without dataset
```

---

## 27. Documentation

### Visible Details

```text
Catalogue sheet
Sketch
Photos
Laser scan
BIM model
Concrete test report
Rebar scan
Damage report
Transport document
Storage document
LCA document
EPD / Ökobaudat reference
Approval document
Notes
```

### Minimum Input

```text
component_id
file references optional
```

### Geometry Generator Output

```text
generated geometry representations can be registered as documents/files
```

### System Output

```text
document IDs
document kind
title
status
date if metadata exists
author if metadata exists
confidence
missing document list
```

### Proof

```text
document_id =
component_id + document_kind

document_kind =
file path/tag classifier

status:
file exists → available
expected but absent → missing
partial evidence → partial

confidence:
signed report → high
BIM/scan model → medium/high
manual note → lower
```

### Must Remain Unknown

```text
document validity
approval status
author/date if metadata missing
```

---

## 28. Evidence Completeness

### Visible Details

```text
Identity complete
Geometry complete
Mass complete
Openings complete
Concrete evidence complete
Rebar evidence complete
Damage evidence complete
Connector zones complete
Logistics complete
LCA complete
Fire data complete
Building physics complete
Services data complete
```

### Minimum Input

```text
component_id
component_typology
material_kind
base_geometry_reference
```

### Geometry Generator Output

```text
geometry completeness
openings completeness
connector-zone completeness
logistics geometry completeness
```

### System Output

```text
completeness status per category
overall completeness score
missing fields
project-context-required flags
```

### Proof

```text
identity_complete =
component_id + typology + material + source exists

geometry_complete =
base geometry processed successfully

mass_complete =
volume + density available

openings_complete =
opening generator executed

connector_zones_complete =
connector geometry generated with confidence

concrete_complete =
required evidence present

reinforcement_complete =
scan/drawing mapped

lca_complete =
mass + transport + dataset/reference

fire_complete =
fire proof/rating or project context exists

building_physics_complete =
thermal data + exposure context + assembly
```

### Must Remain Unknown

```text
true completeness for concrete/rebar/fire/energy without evidence
```

---

## 29. Pool-Level Warnings

### Visible Details

```text
Missing rebar scan
Missing chloride test
Minor edge damage
Unknown lifting points
Unknown transport distance
Missing LCA dataset
Missing fire rating
Unknown thermal conductivity
Do not drill without verification
Do not use damaged edge as bearing zone
```

### Minimum Input

```text
generated geometry
system completeness statuses
damage evidence if available
project required evidence list
```

### Geometry Generator Output

```text
bearing zones
connector zones
damage-zone candidates
opening zones
logistics geometry
```

### System Output

```text
warning list
severity
related field
recommended next evidence
```

### Proof

```text
if rebar evidence missing:
warn Missing rebar scan

if chloride unknown and durability relevant:
warn Missing chloride test

if lifting points unknown:
warn Unknown lifting points

if transport distance unknown:
warn Unknown transport distance

if LCA dataset missing:
warn Missing LCA dataset

if fire rating unknown:
warn Missing fire rating

if drilling zones unknown:
warn Do not drill without verification

if damage overlaps generated bearing zone:
warn Do not use damaged edge as bearing zone
```

### Must Remain Unknown

```text
severity of hidden risks
actual safety of warned actions
```

---

## 30. Rule-Checker Readiness

### Visible Details

```text
Ready rules
Rules needing more evidence
Blocked actions
Default status if used
Missing evidence list
```

### Minimum Input

```text
generated representations
system evidence completeness statuses
project rule library
```

### Geometry Generator Output

```text
geometry/interface readiness
bearing zone readiness
port readiness
opening readiness
energy geometry readiness
logistics geometry readiness
```

### System Output

```text
ready rules
rules requiring more evidence
blocked actions
default connection status
missing evidence list
```

### Proof

```text
if identity complete:
identity check ready

if geometry generated:
geometry/interface check ready

if structural geometry generated:
bearing and pair-type precheck ready

if connector ports generated:
port compatibility check ready

if mass generated:
logistics and LCA precheck ready

if rebar evidence missing:
anchor/drilling check needs evidence

if structural capacity unknown:
structural load proof required

if fire rating unknown:
fire proof required in fire context

if energy context unknown:
envelope check requires context

blocked actions:
drilling without rebar evidence
using damaged generated bearing edge
placing component when stock unavailable
using typology in incompatible role
```

### Must Remain Unknown

```text
final engineering pass/fail
approval readiness
custom connector safety
```

---

## 31. What Should Not Be Shown

### Boundary

The Piece/Bauteilpass panel shows **pool data and generated component representations only**.

It should not show:

```text
current connection validity
failed connection rules
cluster status
accumulated loads from current design
selected connector result
current design LCA total
current building score
target preference score
suggested fixes for a specific active connection
```

### Correct Separation

```text
Piece Panel =
data and generated representations of one real component

Connection Passport =
result of connecting Piece A to Piece B

Rule Checker Panel =
active validation state of the current design

Design Dashboard =
whole-design scores and preference ranking
```

---

# 8. Final Summary

## 8.1 User Provides

```text
component_id
component_typology
material_kind
base geometry reference
source context
storage context
project defaults
optional evidence references
```

## 8.2 Geometry Generators Produce

```text
normalized geometry
physical geometry
structural geometry
energy / envelope geometry
semantic geometry
connector-zone geometry
ports
openings
penetration candidates
logistics geometry
geometry-derived quantities
```

## 8.3 System Modules Produce

```text
Semio binding
identity and traceability
classification
availability
material evidence status
structural data status
fire status
building physics precheck
services status
logistics status
transport precheck
LCA precheck
documentation status
evidence completeness
pool warnings
rule-checker readiness
```

## 8.4 Evidence Still Required For

```text
real concrete strength
true reinforcement position
approved drilling zones
structural capacity
fire resistance
final U-value
actual acoustic performance
remaining service life
full LCA indicators
approval readiness
```

---

# 9. Minimal UI Tab Structure

```text
Piece Detail / Bauteilpass
│
├── Overview
├── Identity
├── Semio Binding
├── Geometry
│   ├── Physical
│   ├── Structural
│   ├── Energy
│   ├── Semantic
│   ├── Connector Zones
│   └── Logistics
├── Openings
├── Condition + Damage
├── Concrete Evidence
├── Reinforcement
├── Structural Data
├── Connectors
├── Fire
├── Building Physics
├── Services
├── Logistics
├── LCA
├── Documents
├── Completeness
└── Pool Warnings
```
