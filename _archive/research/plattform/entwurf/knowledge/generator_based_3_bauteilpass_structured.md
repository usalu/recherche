# Generator-Based Bauteilpass System  
## Minimum Input → Typology Generators → Representations → Interface Data

**Purpose**  
This document defines how a detailed **Piece Detail / Bauteilpass panel** can be produced from minimal input using **preprogrammed typology-based Generators**.

**Project context**  
The system is adapted to the Abbau/Aufbau idea of designing with an already existing pool of reclaimed reinforced-concrete components.  
The process starts **after Rückbau / Zuschnitt**: the system assumes a component pool already exists.

**Core principle**  
The user should not manually enter all Bauteilpass fields.  
The user provides minimal identity/context information and a base geometry reference.  
The system generates the rest through typology-specific Generators.

---

# 1. System Overview

## 1.1 Main Pipeline

```text
Minimum Input
+ Base Geometry
+ Component Typology
        ↓
Typology Selector
        ↓
Generators
        ↓
Generated Representations + Geometry-Tied Data
        ↓
Bauteilpass
        ↓
Piece Detail Panel
        ↓
Rule-Checker Readiness
```

## 1.2 What the User Provides

The minimum input is intentionally small:

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

## 1.3 What the System Produces

```text
normalized geometry
physical representation
structural representation
energy / envelope representation
semantic representation
connector-zone representation
ports
openings and penetration candidates
logistics representation
quantity data
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

It contains:

```text
identity
typology
geometry-derived data
generated representations
evidence data
connector / port data
performance data
logistics data
LCA data
documentation status
rule-checker readiness
```

## 2.2 Generator

A **Generator** is a preprogrammed logic module.

It receives:

```text
component typology
base geometry
material type
project defaults
optional evidence
```

It outputs:

```text
representations
geometry-tied data
ports
zones
prechecks
warnings
readiness states
```

A Generator is not a free-form guess.  
It is rule-based logic built for a typology such as:

```text
slab
beam
wall panel
column
mushroom column
stair
landing
foundation / baseplate
facade panel
adapter
```

## 2.3 Evidence vs Generated Data

The system must distinguish:

| Data type | Meaning |
|---|---|
| **Generated data** | Produced from typology + geometry + project defaults. |
| **Evidence data** | Comes from scans, tests, reports, photos, or inspection. |
| **Unknown data** | Cannot be safely produced and must remain unknown. |
| **Engineering-required data** | Cannot be approved without technical proof. |

Example:

```text
Mass can be generated from geometry + density.
Concrete strength cannot be invented.
Rebar position can be inferred weakly, but approved drilling zones need scan evidence.
```

---

# 3. Generator Library

## 3.1 Generator Families

```text
G-0  Typology Selector
G-1  Base Geometry Normalizer
G-2  Physical Geometry Generator
G-3  Structural Representation Generator
G-4  Energy / Envelope Generator
G-5  Semantic / Architectural Generator
G-6  Connector-Zone + Port Generator
G-7  Openings + Penetration Generator
G-8  Condition + Damage Mapper
G-9  Material Evidence Mapper
G-10 Logistics Generator
G-11 LCA / Ökobilanz Generator
G-12 Documentation + Completeness Generator
G-13 Rule-Checker Readiness Generator
```

## 3.2 Generator Responsibility Matrix

| Generator | Input | Output |
|---|---|---|
| **G-0 Typology Selector** | typology, material, base geometry | typology profile, expected roles, default rules |
| **G-1 Base Geometry Normalizer** | base geometry | units, axes, bounding box, clean reference geometry |
| **G-2 Physical Geometry** | normalized geometry | faces, edges, dimensions, volume, physical anomalies |
| **G-3 Structural** | typology, geometry, evidence | span candidates, support zones, bearing zones, structural role |
| **G-4 Energy / Envelope** | geometry, material, exposure context | envelope faces, U-value precheck, thermal bridge zones |
| **G-5 Semantic / Architectural** | typology, source/design context | inside/outside candidates, visible faces, spatial roles |
| **G-6 Connector-Zone + Port** | typology, geometry, connector library | ports, compatible ports, connector zones, no-drill dependencies |
| **G-7 Openings** | geometry, structural zones | openings, penetrations, service candidates, blocked openings |
| **G-8 Condition + Damage** | photos/scans/geometry anomalies | damage records, visual quality, edge/face condition |
| **G-9 Material Evidence** | test reports, scans, material defaults | concrete/rebar evidence status, missing evidence |
| **G-10 Logistics** | geometry, mass, storage context | storage orientation, lifting status, transport readiness |
| **G-11 LCA** | mass, material, transport, datasets | reused mass, transport GWP, avoided GWP potential |
| **G-12 Documentation** | file references | document list, confidence, completeness |
| **G-13 Readiness** | all generated data + evidence states | ready rules, blocked actions, evidence needed |

---

# 4. Typology Library

Each component typology has a profile that tells the Generators what to produce.

## 4.1 Example: Slab

```yaml
typology:
  id: slab
  material_family: reinforced_concrete

  expected_geometry:
    shape: thin_horizontal_plate
    main_faces: top_bottom
    primary_edges: long_edges_short_edges

  default_roles:
    - floor_slab
    - roof_slab
    - horizontal_spanning_element
    - diaphragm_if_engineered

  generated_representations:
    - physical
    - structural
    - energy
    - semantic
    - connector_zones
    - logistics

  default_ports:
    - slab-edge-bearing
    - slab-top-service-zone
    - slab-envelope-face

  default_checks:
    - bearing_overlap
    - span_direction
    - reinforcement_before_drilling
    - fire_if_connector_exposed
    - thermal_if_envelope
    - transport_lca
```

## 4.2 Example: Beam

```yaml
typology:
  id: beam
  expected_geometry:
    shape: long_horizontal_prism

  default_roles:
    - line_support
    - horizontal_load_transfer

  default_ports:
    - beam-end-bearing
    - beam-top-bearing
    - beam-side-connector

  generated_data:
    - end support zones
    - top bearing surface
    - span direction
    - lifting candidates
```

## 4.3 Example: Mushroom Column

```yaml
typology:
  id: mushroom_column
  expected_geometry:
    shape: vertical_column_with_capital

  default_roles:
    - vertical_point_support
    - slab_head_support

  default_ports:
    - column-base-bearing
    - mushroom-head-bearing
    - column-side-stability-connector

  generated_data:
    - shaft zone
    - capital zone
    - column base port
    - head bearing port
    - punching-sensitive interface flag
    - special storage / lifting warning
```

---

# 5. Shared Calculation Proofs

## 5.1 Dimensions

```text
oriented_bounding_box = OBB(base_geometry)

length = largest principal dimension
width = second principal dimension
thickness = smallest principal dimension for slab / panel
height = vertical dimension for column / wall
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

## 5.3 Mass

```text
mass_kg = net_volume_m3 × material_density_kg_m3
mass_t = mass_kg / 1000
```

## 5.4 Self-weight

```text
self_weight_kN = mass_kg × 9.81 / 1000
```

For slabs:

```text
self_weight_kN_m2 = self_weight_kN / plan_area_m2
```

## 5.5 Transport Impact

```text
transport_gwp_kgco2e =
mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

## 5.6 Avoided New-Material Potential

```text
avoided_gwp_potential_kgco2e =
mass_t × new_equivalent_reference_kgco2e_per_t
```

## 5.7 Rough U-Value Precheck

```text
R_concrete = thickness_m / lambda_concrete_W_mK

U_rough = 1 / (Rsi + R_concrete + Rse)
```

This is only a precheck.  
A final energy proof requires full assembly layers, thermal bridge calculations, and project-specific boundary conditions.

---

# 6. Piece Detail Panel Structure

The Piece Detail / Bauteilpass panel is organized into 32 sections:

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
Generator used
Generated output
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

### Generator Used

```text
G-0 Typology Selector
G-1 Base Geometry Normalizer
G-2 Physical Geometry Generator
G-11 LCA / Quantity Generator
G-12 Documentation + Completeness Generator
```

### Generated Output

```text
component name
element kind label
main dimensions
mass
thumbnail
availability state
evidence completeness
tracking code
```

### Proof

```text
component_name =
human_label(component_typology) + " " + component_id

dimensions =
oriented_bounding_box(base_geometry)

volume =
solid_volume(base_geometry)

mass =
volume × density_default(material_kind)

thumbnail =
existing preview or generated viewport capture

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
measured mass if density is only assumed
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

### Generator Used

```text
G-0 Typology Selector
G-6 Connector-Zone + Port Generator
G-12 Documentation + Completeness Generator
```

### Generated Output

```text
kit name
type ID
type name
parent type
type kind
stock total
stock available
current piece IDs
attribute namespace
quality namespace
representation list
connector list
```

### Proof

```text
kit_name =
project_context.kit_name or "Bauteilkatalog"

type_id =
"type-" + component_id

type_name =
component_id

parent_type =
"type-reclaimed-" + component_typology

type_kind =
"reclaimed-" + material_kind + "-" + component_typology

stock_total =
1 for real individual reclaimed component
unless catalogue quantity says otherwise

stock_available =
stock_total - active_piece_count

current_piece_ids =
query design graph where piece.type_id == type_id

attribute_namespace =
project_slug

quality_namespace =
project_slug

representations =
base geometry + generator outputs

connectors =
generated ports and connector zones from typology generator
```

### Must Remain Unknown

```text
custom parent taxonomy if project does not define it
true stock if several physical pieces are grouped under one type
manually overridden connector hierarchy
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

### Generator Used

```text
G-0 Typology Selector
G-1 Base Geometry Normalizer
G-12 Documentation + Completeness Generator
```

### Generated Output

```text
human-readable name
element type label
source level
source zone
original function candidate
original orientation candidate
tracking method
QR code
internal GUID
external database reference
```

### Proof

```text
human_readable_name =
component_id + " (" + component_typology + ")"

source_level =
parse level token from ID
example: DE_1OG_001 → 1OG
else use source_context.original_level

source_zone =
parse zone token from ID
else unknown

original_function =
source_context.original_function
or typology default:
slab → floor_slab
beam → beam
wall → wall_panel
column → column
mushroom_column → column_with_capital

original_orientation =
from base geometry metadata
or typology generator:
slab → largest faces are top/bottom candidates
column → vertical axis is height candidate

tracking_method =
provided tracking reference
else generated QR

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
physical marking status if not recorded
true original orientation if geometry lacks metadata and typology inference is ambiguous
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

### Generator Used

```text
G-12 Documentation + Completeness Generator
G-13 Rule-Checker Readiness Generator
```

### Generated Output

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
1 for individual reclaimed element
unless quantity is provided

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

storage_state =
located if storage location exists
else unknown
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

### Generator Used

```text
G-0 Typology Selector
G-2 Physical Geometry Generator
G-3 Structural Representation Generator
G-5 Semantic / Architectural Generator
```

### Generated Output

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

material_family =
material_kind

structural_family:
slab → horizontal_spanning
beam → horizontal_line_support
wall → vertical_panel
column → vertical_point_support
mushroom_column → vertical_point_support_with_capital
stair → circulation_component

allowed_design_roles:
slab → floor_slab, roof_slab, diaphragm_if_engineered
beam → line_support
wall → wall_panel, shear_wall_if_engineered, partition_if_nonstructural
column → vertical_support
mushroom_column → vertical_support_with_slab_head
stair → circulation

disallowed_roles =
roles incompatible with typology unless explicitly engineered

semantic_tags =
["reclaimed", material_kind, component_typology, "component-pool"]

reuse_category =
based on condition/evidence completeness

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
material_kind
component_typology
project unit default
```

### Generator Used

```text
G-1 Base Geometry Normalizer
G-2 Physical Geometry Generator
```

### Generated Output

```text
unit system
length
width
height/thickness
bounding box
gross volume
net volume
mass
density
center of gravity
local axes
top/bottom candidates
tolerances
```

### Proof

```text
unit_system =
geometry metadata
or project default

bounding_box =
oriented_bounding_box(base_geometry)

dimensions =
principal dimensions of bounding box

gross_volume =
bounding box volume

net_volume =
solid volume of base geometry

density =
measured density if available
else project default for material

mass =
net_volume × density

center_of_gravity =
volume centroid

local_axes =
geometry metadata or principal axes

top/bottom:
slab → two largest parallel faces
wall → vertical broad faces + bottom edge
column → bottom/top faces along vertical axis

tolerances =
project defaults
```

### Must Remain Unknown

```text
measured density
internal voids not represented in geometry
true original top/bottom if typology inference conflicts with metadata
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

### Generator Used

```text
G-1 Base Geometry Normalizer
G-2 Physical Geometry Generator
G-3 Structural Representation Generator
G-4 Energy / Envelope Generator
G-5 Semantic / Architectural Generator
G-6 Connector-Zone + Port Generator
G-10 Logistics Generator
```

### Generated Output

```text
physical representation
structural representation
energy representation
semantic representation
connector-zone representation
logistics representation
generated representation tags
confidence levels
missing representation flags
```

### Proof

```text
physical representation =
normalized base geometry

structural representation =
typology-specific support zones, span candidates, load directions

energy representation =
faces and zones relevant to envelope/thermal precheck

semantic representation =
inside/outside candidates, visible faces, room/facade candidates

connector-zone representation =
ports, bearing zones, anchor zones, service zones

logistics representation =
lifting candidates, storage orientation, transport envelope

confidence =
high if evidence/model metadata supports generation
medium if generated from clear typology
low if inferred from ambiguous shape
```

### Must Remain Unknown

```text
true semantic meaning without context
true structural proof without evidence
true energy compliance without assembly context
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

### Generator Used

```text
G-2 Physical Geometry Generator
G-7 Openings + Penetration Generator
G-8 Condition + Damage Mapper
```

### Generated Output

```text
shape type
faces
edges
openings
cut-outs
chamfers
irregularities
damage candidates
physical tolerance estimate
```

### Proof

```text
shape_type =
typology + aspect ratio classification

faces =
extract from solid/mesh

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

damage candidates =
geometry anomalies + optional photo/scan evidence

physical_tolerance =
deviation from fitted planes/surfaces
```

### Must Remain Unknown

```text
small cracks below scan resolution
surface contamination without visual/lab evidence
whether an irregularity is intentional or damage
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
original_function if available
```

### Generator Used

```text
G-3 Structural Representation Generator
G-7 Openings + Penetration Generator
G-9 Material Evidence Mapper
```

### Generated Output

```text
structural role
span direction candidate
support edges
bearing zones
line-support zones
point-support candidates
load direction
preferred support condition
forbidden support condition
minimum bearing length
structural thickness
structural openings
```

### Proof

```text
structural_role:
slab → spanning_element
beam → line_support
wall → vertical_panel
column → point_support
mushroom_column → point_support_with_capital

span_direction:
from reinforcement evidence if available
else generated from typology and aspect ratio
status = inferred

support_edges:
slab → generated bearing edges
beam → end supports
wall → bottom/top line
column → base/head faces
mushroom_column → base + capital/head region

bearing_zones =
support edges buffered by typology rule

point_support_zones =
column or mushroom column head zones

load_direction =
gravity downward by default

minimum_bearing_length =
typology + pair rule default

structural_openings =
openings intersecting generated load/support zones
```

### Must Remain Unknown

```text
actual load capacity
moment capacity
shear capacity
punching resistance
true reinforcement layout without scan/drawing
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
intended_exposure_context if known
```

### Generator Used

```text
G-4 Energy / Envelope Generator
G-5 Semantic / Architectural Generator
G-6 Connector-Zone + Port Generator
```

### Generated Output

```text
envelope relevance
exterior/interior candidates
ground-contact candidates
roof candidates
thermal boundary candidates
insulation faces
thermal bridge zones
moisture risk zones
U-value relevant surfaces
```

### Proof

```text
if intended_exposure_context = interior:
envelope_relevance = not_relevant

if intended_exposure_context = exterior / roof / ground:
envelope_relevance = relevant

if context unknown:
envelope_relevance = requires_project_context

thermal_boundary_faces =
faces separating conditioned and exterior/unconditioned context

insulation_faces =
exterior side of thermal boundary

thermal_bridge_zones =
connector zones crossing thermal boundary
+ exposed slab/wall edges

moisture_risk_zones =
ground-contact faces
+ roof faces
+ exterior horizontal faces

U_value_relevant_surfaces =
thermal boundary faces
```

### Energy Proof

```text
R_concrete = thickness / lambda_concrete

U_rough = 1 / (Rsi + R_concrete + Rse)
```

### Must Remain Unknown

```text
final U-value without full assembly
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

### Generator Used

```text
G-5 Semantic / Architectural Generator
G-8 Condition + Damage Mapper
```

### Generated Output

```text
inside/outside candidates
room-facing candidates
facade-facing candidates
visible face candidates
hidden face candidates
original use side
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
slab top → floor side
slab bottom → ceiling side
wall broad faces → room/facade candidates
column sides → visible structural faces
beam sides/bottom → visible support element

potential_new_use =
typology role library

visible_faces =
faces not covered by generated support zones, envelope layers, or hidden flags

surface_expression_value =
visible_area × visual_quality × visible_reuse_preference
```

### Must Remain Unknown

```text
actual intended architectural expression
inside/outside if no source or placement context exists
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

### Generator Used

```text
G-7 Openings + Penetration Generator
G-3 Structural Representation Generator
G-9 Material Evidence Mapper
```

### Generated Output

```text
detected openings
opening IDs
opening type
position
size
depth
edge distance
service reuse candidate
blocked opening candidate
relation to reinforcement status
```

### Proof

```text
openings =
detect through-voids and recesses

opening_id =
component_id + "-opening-" + index

opening_type:
circular → core_drilling_candidate
rectangular → rectangular_opening
irregular → unknown_cutout

position =
opening centroid in local coordinates

size =
diameter or bounding dimensions

depth =
component thickness for through opening

edge_distance =
minimum distance to nearest edge

relation_to_reinforcement =
intersect opening zone with rebar map
or unknown if no map exists

blocked =
opening overlaps bearing zone, damaged zone, no-drill zone
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

### Generator Used

```text
G-8 Condition + Damage Mapper
G-5 Semantic / Architectural Generator
```

### Generated Output

```text
face condition candidates
edge condition candidates
geometric damage candidates
visual quality
visible reuse quality
```

### Proof

```text
face classification =
from typology and geometry normals

spalling candidates =
missing material or irregular edge/faces

crack candidates =
photo/scan line detection if evidence exists

exposed_rebar candidates =
visual detection + damage region

visual_quality =
damage severity + discoloration + cracks + repair marks

visible_reuse_quality =
visual_quality × visible_face_area × semantic visibility
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

### Generator Used

```text
G-8 Condition + Damage Mapper
G-3 Structural Representation Generator
G-5 Semantic / Architectural Generator
```

### Generated Output

```text
damage candidates
damage IDs
location
affected face/edge
severity candidate
rule relevance
```

### Proof

```text
damage_id =
component_id + "-damage-" + index

damage_kind:
line feature → crack
missing concrete → spalling/edge damage
rust color → corrosion mark
visible steel → exposed reinforcement

location =
mapped to geometry coordinates

severity =
damage size × overlap with bearing/connector/visible zones

rule_relevance:
bearing overlap → structural/interface
visible face → architectural
exposed rebar → durability/reinforcement
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

### Generator Used

```text
G-9 Material Evidence Mapper
G-12 Documentation + Completeness Generator
```

### Generated Output

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
else unknown

E_modulus =
test/report
or estimated from compressive strength if project permits

carbonation_depth =
test only

chloride_content =
lab test only

pollutant_content =
lab/screening only

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

### Generator Used

```text
G-3 Structural Representation Generator
G-6 Connector-Zone + Port Generator
G-9 Material Evidence Mapper
```

### Generated Output

```text
reinforcement direction candidate
unknown reinforcement zones
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
status = low confidence

cover =
scan/drawing/test only
else unknown

no_drill_zones =
known rebar zones + edge buffers + bearing zones

if rebar map missing:
all drilling zones = unknown or blocked

drill_approved_zones =
connector zones - rebar buffers - edge buffers - damaged zones

anchor_approved_zones =
drill approved zones satisfying anchor spacing/depth
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

### Generator Used

```text
G-8 Condition + Damage Mapper
G-9 Material Evidence Mapper
G-4 Energy / Envelope Generator
```

### Generated Output

```text
durability status
carbonation risk if evidence exists
chloride risk if evidence exists
corrosion risk candidate
freeze-thaw risk candidate
moisture exposure risk
repair requirement
protection requirement
```

### Proof

```text
carbonation_risk =
carbonation_depth compared to concrete cover

chloride_risk =
lab chloride value

corrosion_risk =
carbonation risk + chloride risk + exposed rebar + rust marks

freeze_thaw_risk =
exterior/wet exposure context

moisture_risk =
ground / roof / outdoor storage / exposed horizontal faces

repair_required =
medium/critical damage or exposed rebar

protection_required =
outdoor storage or moisture risk
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

### Generator Used

```text
G-3 Structural Representation Generator
G-9 Material Evidence Mapper
```

### Generated Output

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

self_weight_kN_m2 =
self_weight_kN / plan_area_m2

allowed_support_types:
slab → wall top, beam top, column head if engineered
beam → column top, wall top
wall → base line
column → base point
mushroom_column → base point + slab/head interface

allowed_span_direction =
reinforcement evidence or typology inference

maximum_reuse_span =
dimension in generated span direction
not verified capacity

capacity_evidence_status =
known only if test/static proof exists
else unknown

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

### Generator Used

```text
G-6 Connector-Zone + Port Generator
G-3 Structural Representation Generator
G-4 Energy / Envelope Generator
G-7 Openings + Penetration Generator
```

### Generated Output

```text
connector zones
ports
compatible ports
mandatory connectors
directions
allowed connector systems
minimum bearing lengths
maximum gaps
edge distances
drilling permission status
required checks
reversibility preference
```

### Proof

```text
connector_zone =
typology-specific face/edge/region

connector_id =
component_id + connector_zone_id

port examples:
slab edge → slab-edge-bearing
wall top → wall-top-bearing
beam top → beam-top-bearing
column head → column-head-bearing
mushroom capital → mushroom-column-head-bearing
service opening → service-penetration
envelope face → thermal-envelope-interface

compatible_ports =
lookup connector library

mandatory =
true for required structural support ports
false for optional service/envelope ports

direction =
outward normal of connector zone

allowed_connector_systems =
pair-type connector library:
wall+slab → post_installed_rebar_grout, screw_anchor_flat_steel_holder
base+wall → stainless_dowel, angle_connector
base+column → stainless_dowel, angle_connector
column+slab → stainless_dowel, angle_connector, steel_beam_support, engineered grout detail

drilling_permission =
based on rebar evidence and no-drill zones

required checks =
structural if load-bearing
fire if exposed steel/fire context
thermal if envelope context
service if penetration context
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
connector-zone representation
project drilling defaults
optional rebar scan
```

### Generator Used

```text
G-6 Connector-Zone + Port Generator
G-9 Material Evidence Mapper
```

### Generated Output

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

rebar_conflict_status =
intersect(anchor zones, rebar map)

scan_confidence =
scan metadata
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

### Generator Used

```text
G-4 Energy / Envelope Generator
G-6 Connector-Zone + Port Generator
G-9 Material Evidence Mapper
```

### Generated Output

```text
material fire class candidate
fire-relevant surfaces candidate
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

fire_relevant_surfaces =
generated if context marks component as compartment/envelope/escape-route relevant

exposed_steel_warning =
true for connector systems with exposed steel

fire_cover_required_if =
angle connector, steel beam support, steel plate, exposed anchor in fire-relevant condition
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

### Generator Used

```text
G-4 Energy / Envelope Generator
G-11 LCA / Ökobilanz Generator
```

### Generated Output

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
lambda =
measured value or material default

density =
measured value or material default

R_concrete =
thickness / lambda

U_rough =
1 / (Rsi + R_concrete + Rse)

insulation_required =
if envelope relevant and U_rough above target

thermal_bridge_zones =
connector zones crossing envelope + exposed edges

moisture_risk =
roof, ground, exterior, wet storage

acoustic_relevance =
high mass per area
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

### Generator Used

```text
G-4 Energy / Envelope Generator
G-5 Semantic / Architectural Generator
```

### Generated Output

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

recommended_acoustic_use =
high mass → potential separating element

acoustic_warning =
high acoustic target + no evidence
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

### Generator Used

```text
G-7 Openings + Penetration Generator
G-6 Connector-Zone + Port Generator
G-9 Material Evidence Mapper
```

### Generated Output

```text
existing openings
approved service zone candidates
blocked service zones
possible cable penetrations
possible pipe penetrations
core drilling allowed/blocked
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

core_drilling_blocked =
unknown rebar or no-drill zone or bearing zone

rebar_scan_required =
true if new penetration requested and reinforcement unknown
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

### Generator Used

```text
G-10 Logistics Generator
G-2 Physical Geometry Generator
G-6 Connector-Zone + Port Generator
```

### Generated Output

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
assembly access zones
```

### Proof

```text
mass =
volume × density

storage orientation:
slab → lying flat
beam → supported at calculated support zones
wall → standing only with support or engineering_required
column → stable storage depending slenderness
mushroom column → special support due to capital/head geometry

weather_protection_required =
outdoor storage or durability risk

separator_required =
true when stacked/stored concrete surfaces may be damaged

lifting_point_status =
known if documented
else engineering_required

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

### Generator Used

```text
G-10 Logistics Generator
G-11 LCA / Ökobilanz Generator
```

### Generated Output

```text
transport dimensions
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

protection_required =
true for reclaimed component transport

load_securing_required =
true
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

### Generator Used

```text
G-11 LCA / Ökobilanz Generator
```

### Generated Output

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

LCA completeness =
mass + transport + reference dataset + indicator datasets

GWP =
calculated if transport and reference exist

other indicators =
only from EPD / Ökobaudat / generic dataset
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

### Generator Used

```text
G-12 Documentation + Completeness Generator
```

### Generated Output

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

title =
humanize(filename)

status:
file exists → available
expected but absent → missing
partial evidence → partial

confidence:
signed test report → high
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

### Generator Used

```text
G-12 Documentation + Completeness Generator
```

### Generated Output

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

concrete_complete =
required concrete evidence present

reinforcement_complete =
scan/drawing mapped

damage_complete =
visual evidence/inspection mapped

connector_zones_complete =
connector generator executed with confidence

logistics_complete =
storage + mass + transport/lifting status known

lca_complete =
mass + transport + dataset/reference

fire_complete =
fire proof/rating or project context exists

building_physics_complete =
thermal data + exposure context + assembly

services_complete =
openings + service zones + rebar status
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
generated completeness statuses
damage evidence if available
project required evidence list
```

### Generator Used

```text
G-13 Rule-Checker Readiness Generator
```

### Generated Output

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

if thermal conductivity unknown:
warn Unknown thermal conductivity

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
all generated representations
evidence completeness statuses
project rule library
```

### Generator Used

```text
G-13 Rule-Checker Readiness Generator
```

### Generated Output

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

if structural representation generated:
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

if LCA dataset missing:
full LCA requires dataset

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

The Piece/Bauteilpass panel shows **pool and generated component data only**.

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

## 8.2 Generators Produce

```text
normalized geometry
physical representation
structural representation
energy / envelope representation
semantic representation
connector-zone representation
ports
openings
derived quantities
logistics representation
LCA precheck
evidence completeness
pool warnings
rule-checker readiness
```

## 8.3 Evidence Still Required For

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
