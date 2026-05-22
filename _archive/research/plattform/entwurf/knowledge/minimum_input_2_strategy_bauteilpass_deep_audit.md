# Deep Audit — Minimum Input Strategy for the Bauteilpass Interface

**Purpose**  
This document defines the minimum non-geometric information needed to display a detailed Piece/Bauteilpass panel for a reclaimed component pool.

**Project framing**  
The structure is adapted to the Abbau/Aufbau logic for reusing existing reinforced-concrete components, but it is designed to stay general enough for other reclaimed-component projects.

**Important assumption**  
Manual geometry input is excluded. The system already has access to at least one geometric representation of the component, for example a Semio representation, BIM object, mesh, scan, drawing-derived model, or another geometric source. The user does not manually type dimensions.

---

## Audit Corrections Compared to the Earlier Version

1. **Geometry is not a user input.**  
   Geometry-derived fields are extracted from available representations.

2. **Structural capacity is not calculated from minimal data.**  
   The system may calculate self-weight and precheck support logic, but final load capacity remains `engineering_required` unless structural proof, test data, or an engineer-approved model exists.

3. **Energy data is context-dependent.**  
   A rough U-value precheck can be derived from thickness and assumed thermal conductivity, but final envelope compliance requires project context and assembly layers.

4. **LCA can be precomputed only as a potential.**  
   Reused mass, transport impact, and avoided-new-material potential can be calculated if mass, transport distance, and reference datasets exist. Full LCA needs datasets and scope.

5. **The Piece/Bauteilpass panel shows pool data only.**  
   It must not show active connection validity, current design totals, failed connection rules, or target-preference scores.

---

## Core Input Classification

```text
A. Absolute minimum non-geometric input
   Data the user/project must provide manually or through metadata.

B. Geometry-derived data
   Data extracted from available geometry, not typed by user.

C. Context-derived data
   Data inferred from project defaults, Semio kit structure, naming conventions, or component libraries.

D. Evidence-derived data
   Data extracted from reports, scans, tests, documents, or manual inspection.

E. Non-derivable data
   Data that must remain unknown, partial, warning, or engineering_required.
```

---

## Absolute Minimum Non-Geometric Input Package

```yaml
minimum_non_geometric_input:
  component_id: DE_1OG_001
  element_kind: slab
  material_kind: reinforced_concrete

  source_context:
    source_project: Abbau Aufbau
    source_building_id: donor-building-001
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

  optional_evidence_refs:
    concrete_test_report: null
    reinforcement_scan: null
    damage_photos: null
    lca_dataset: null
    fire_document: null
```

The geometric representation is assumed to be available in the system:

```yaml
system_available_geometry:
  geometry_reference: representations/DE_1OG_001/physical.glb
```

---

## Shared Calculation Proofs

### Bounding dimensions

```text
bounding_box = oriented_bounding_box(geometry_reference)

length = largest horizontal bounding dimension
width = second horizontal bounding dimension
height/thickness = smallest principal dimension for slabs/panels
```

### Volume

```text
net_volume_m3 = solid_volume(geometry_reference)
```

Fallback for rectangular elements:

```text
net_volume_m3 =
(length_m × width_m × thickness_m)
- detected_opening_volume_m3
```

### Mass

```text
mass_kg = net_volume_m3 × density_kg_m3
mass_t = mass_kg / 1000
```

### Surface area

```text
face_area_m2 = area(selected_face_geometry)
total_surface_area_m2 = sum(all_face_areas)
```

### Area for slab-like elements

```text
plan_area_m2 = length_m × width_m
```

### Self-weight

```text
self_weight_kN = mass_kg × 9.81 / 1000
self_weight_kN_m2 = self_weight_kN / plan_area_m2
```

### Transport impact

```text
transport_gwp_kgco2e =
mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

### Avoided new-material GWP potential

```text
avoided_gwp_potential_kgco2e =
mass_t × new_equivalent_reference_kgco2e_per_t
```

### Rough thermal resistance of concrete layer

```text
R_concrete_m2K_W = thickness_m / lambda_concrete_W_mK
```

### Rough U-value precheck

```text
U_rough_W_m2K = 1 / (Rsi + R_concrete + Rse)
```

This is only a precheck. A final energy proof requires full assembly layers, boundary conditions, thermal bridges, and project-specific requirements.

---

# 0. Header / Quick Summary

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
element_kind
material_kind
current_storage_location
```

## Geometry-Derived Data

```text
main dimensions
thumbnail if generated from geometry
volume
mass if density default exists
```

## Context-Derived Data

```text
component name
availability
tracking code
evidence completeness
```

## Calculation / Inference Proof

```text
component_name =
human_label(element_kind) + " " + component_id

main_dimensions =
oriented_bounding_box(geometry_reference)

volume =
solid_volume(geometry_reference)

mass =
volume × density_default(material_kind)

thumbnail =
existing sketch/photo representation
or generated preview from geometry

availability =
stock_total - active_piece_count - reserved_count

tracking_code =
existing QR/RFID/BIM reference
or generated QR code from component_id

evidence_completeness =
available_required_fields / required_fields
```

## Non-Derivable / Must Remain Unknown

```text
true measured mass if density is only assumed
actual physical marking status
physical presence in storage if storage is not synced
real condition if no visual/evidence data exists
```

---

# 1. Semio Binding

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
kit_id
component_id
element_kind
material_kind
```

## Geometry-Derived Data

```text
representation list, if files are attached to the component
connector candidates, if connector-zone geometry exists
```

## Context-Derived Data

```text
kit name
type ID
type name
parent type
type kind
stock
namespaces
current piece IDs
```

## Calculation / Inference Proof

```text
kit_name =
project_context.kit_name or "Bauteilkatalog"

type_id =
"type-" + component_id

type_name =
component_id

parent_type =
"type-reclaimed-" + element_kind

type_kind =
"reclaimed-" + material_kind + "-" + element_kind

stock_total =
1 for individual reclaimed components
unless catalogue quantity states otherwise

stock_available =
stock_total - count(active_pieces_using_type)

current_piece_ids =
query(design_graph where piece.type_id == type_id)

attribute_namespace =
project_slug

quality_namespace =
project_slug

representations =
all files linked to component_id

connector_list =
connector_zone_geometry + element_kind connector library
```

## Non-Derivable / Must Remain Unknown

```text
custom parent taxonomy unless project defines it
true stock if catalogue groups several similar real elements
connector list if no connector zones or rules are available
```

---

# 2. Identity + Traceability

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
element_kind
material_kind
source_project
```

## Geometry-Derived Data

```text
original orientation candidate, only if geometry has orientation metadata
```

## Context-Derived Data

```text
human-readable name
source building
original level
original zone
original function
tracking method
QR code
BIM GUID candidate
external reference
```

## Calculation / Inference Proof

```text
human_readable_name =
component_id + " (" + element_kind + ")"

source_building =
source_context.source_building_id
or parse(component_id)

original_level =
parse level token from component_id
example: DE_1OG_001 → 1OG

original_zone =
parse zone token from component_id
else unknown

original_function =
from source_context.original_function
or from element_kind:
slab → floor_slab
wall → wall_panel
column → column
beam → beam

tracking_method =
existing tracking data if provided
else system_generated_QR

qr_code =
"QR-" + component_id

bim_guid =
imported BIM GUID if present
else generated internal GUID with status system_generated

external_reference =
catalogue_path(component_id)
```

## Non-Derivable / Must Remain Unknown

```text
real RFID code if not scanned/provided
true physical marking status
true original function if not encoded in source context
true original orientation if geometry lacks orientation metadata
```

---

# 3. Pool Availability

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
stock_total or individual_component_assumption
access_to_design_graph
```

## Geometry-Derived Data

```text
none
```

## Context-Derived Data

```text
availability state
storage state
used count
stock available
reserved design
linked pieces
```

## Calculation / Inference Proof

```text
stock_total =
provided stock_total
or 1 for real individual component

used_count =
count(pieces where piece.type_id == type_id)

reserved_count =
count(reservations where reservation.type_id == type_id)

stock_available =
stock_total - used_count - reserved_count

availability_state:
if blocked_reason exists → blocked
else if reserved_count > 0 → reserved
else if used_count > 0 → placed
else if stock_available > 0 → available
else → unavailable

storage_state =
located if storage_location exists
else unknown
```

## Non-Derivable / Must Remain Unknown

```text
whether component is physically still present
manual off-platform reservations
damage after catalogue creation
```

---

# 4. Classification

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
material_kind
```

## Geometry-Derived Data

```text
aspect ratio classification support
shape consistency check
```

## Context-Derived Data

```text
primary kind
secondary classifications
material family
structural family
allowed design roles
disallowed design roles
semantic tags
reuse category
risk category
```

## Calculation / Inference Proof

```text
primary_kind =
element_kind

material_family =
material_kind

structural_family:
slab → horizontal_spanning
wall → vertical_panel
column → vertical_point_support
beam → horizontal_line_support
stair → circulation_component
facade → envelope_component

allowed_design_roles:
slab → floor_slab, roof_slab, diaphragm_if_engineered
wall → wall_panel, shear_wall_if_engineered, partition
column → vertical_support
beam → line_support
stair → circulation

disallowed_design_roles =
all roles incompatible with element_kind unless engineer-approved

semantic_tags =
["reclaimed", material_kind, element_kind, "component-pool"]

reuse_category:
good evidence + no critical damage → reusable_preferred
missing evidence → reusable_with_verification
critical damage → blocked

risk_category =
weighted score from missing evidence + damage + structural role uncertainty
```

## Non-Derivable / Must Remain Unknown

```text
approved alternative role without engineering proof
true load-bearing classification without structural evidence
```

---

# 5. Geometry Overview

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
project_units_default, if geometry metadata is missing
```

## Geometry-Derived Data

```text
unit system
length
width
height/thickness
bounding box
gross volume
net volume
center of gravity
local axes candidate
top/bottom candidate
```

## Context-Derived Data

```text
density default
mass
tolerances
```

## Calculation / Inference Proof

```text
unit_system =
geometry metadata
or project default

bounding_box =
oriented_bounding_box(geometry)

length/width/height =
principal dimensions from bounding box

gross_volume =
bounding_box volume

net_volume =
solid volume of geometry

density =
measured density if available
else project default for material_kind

mass =
net_volume × density

center_of_gravity =
volume_centroid(geometry)

local_axes =
imported object coordinate system
or principal axes from oriented bounding box

original_top_bottom =
metadata if available
else unknown

tolerances =
project defaults
```

## Non-Derivable / Must Remain Unknown

```text
measured density
internal voids not represented in geometry
true original top/bottom if no metadata exists
actual fabrication tolerance
```

---

# 6. Geometry Representations

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
```

## Geometry-Derived Data

```text
available representations
file types
geometry tags if metadata exists
```

## Context-Derived Data

```text
representation names
missing representations
confidence levels
```

## Calculation / Inference Proof

```text
representation_list =
files linked to component_id

file_type =
file extension

tags =
file metadata, folder, filename, or imported Semio tags

example:
physical.glb → physical, geometry, 3d
structural.json → structural, bearing_zones
energy.json → energy, envelope
connector-zones.json → connector, anchors, no_drill

confidence:
native BIM or scan with metadata → high
manual sketch → medium
filename-only inference → low

missing_representations =
expected_representation_types - available_representation_types
```

## Non-Derivable / Must Remain Unknown

```text
true meaning of untagged files
LOD if metadata is absent
source reliability if provenance is missing
```

---

# 7. Physical Geometry

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
none beyond access to geometry
```

## Geometry-Derived Data

```text
shape type
dimensions
faces
edges
openings
cut-outs
chamfers
irregularities
damage candidates
physical tolerance estimate
```

## Calculation / Inference Proof

```text
shape_type =
classify by aspect ratio and element_kind

faces =
extract planar/mesh faces

edges =
extract boundary curves

openings =
detect holes/voids

cutouts =
detect recesses or non-through voids

chamfers =
detect bevelled edge topology

irregularities =
deviation from ideal fitted solid

damage candidates =
geometric anomalies + optional image/scan evidence

physical_tolerance =
max deviation from fitted ideal planes
```

## Non-Derivable / Must Remain Unknown

```text
small cracks below scan resolution
surface contamination
whether irregularity is intended or damage
```

---

# 8. Structural Geometry

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
original_function
```

## Geometry-Derived Data

```text
support edge candidates
bearing zones
line-support zones
point-support candidates
structural thickness
structural openings
```

## Context-Derived Data

```text
structural role
span direction candidate
load direction
preferred support condition
forbidden support condition
minimum bearing length default
```

## Calculation / Inference Proof

```text
structural_role:
slab → spanning_element
wall → vertical_panel
column → point_support
beam → line_support

span_direction:
if reinforcement data exists → main reinforcement/span logic
else if slab → inferred from aspect ratio and original function
status = inferred/low_confidence

support_edges:
slab → edges perpendicular or parallel to inferred span depending support logic
beam → end zones
wall → bottom/top line zones
column → top/bottom faces

bearing_zones =
support_edges buffered by required bearing width

point_support_zones =
column-head support zones only if engineered or represented

load_direction =
gravity downward by default

minimum_bearing_length =
project default or pair-type rule

structural_openings =
openings intersecting bearing/support/load path zones
```

## Non-Derivable / Must Remain Unknown

```text
actual load capacity
moment/shear capacity
punching safety
true reinforcement layout without scan/drawing
```

---

# 9. Energy / Envelope Geometry

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
intended_exposure_context if known
```

## Geometry-Derived Data

```text
face areas
thickness
edge zones
possible thermal boundary faces
```

## Context-Derived Data

```text
envelope relevance
exterior/interior candidates
thermal bridge candidates
U-value relevance
moisture risk candidates
```

## Calculation / Inference Proof

```text
if intended_exposure_context == interior:
envelope_relevance = not_relevant

if intended_exposure_context in [exterior, roof, ground]:
envelope_relevance = relevant

if exposure unknown:
envelope_relevance = requires_project_context

thermal_boundary_faces =
faces separating conditioned from unconditioned/exterior context

insulation_faces =
exterior side of thermal boundary

thermal_bridge_zones =
connector zones crossing thermal boundary + slab/wall edges at exterior

moisture_risk_zones =
ground-contact + roof + exposed horizontal surfaces

U_value_relevant_surfaces =
thermal_boundary_faces
```

## Energy Calculation Proof

```text
lambda_concrete =
measured value
or project default for reinforced concrete

R_concrete =
thickness_m / lambda_concrete

U_rough =
1 / (Rsi + R_concrete + Rse)
```

## Non-Derivable / Must Remain Unknown

```text
final U-value without full assembly
required insulation thickness without target and full layer build-up
thermal bridge Psi-value
moisture safety
inside/outside without design context
```

---

# 10. Semantic / Architectural Geometry

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
source_context
target_use_context optional
```

## Geometry-Derived Data

```text
face candidates
visible area candidates
surface side candidates
```

## Context-Derived Data

```text
inside/outside side
room-facing side
facade-facing side
original use side
potential new use
spatial role
surface expression value
```

## Calculation / Inference Proof

```text
inside/outside:
from original BIM tags or design placement context
else unknown

room_facing_faces:
faces adjacent to room volumes in semantic model

facade_facing_faces:
faces adjacent to exterior/envelope context

visible_faces:
faces not covered by other pieces, finishes, or hidden layers

original_use_side:
slab top → floor side
slab bottom → ceiling side
if orientation metadata exists

potential_new_use:
element_kind role library

surface_expression_value =
visible_area × visual_quality × visible_reuse_preference
```

## Non-Derivable / Must Remain Unknown

```text
desired architectural expression
true inside/outside without source/design semantics
visual quality if no photos/scans exist
```

---

# 11. Openings + Penetrations

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
none beyond geometry
```

## Geometry-Derived Data

```text
opening ID
opening type
opening position
opening size
opening depth
edge distance
```

## Context-Derived Data

```text
service reuse candidate
blocked opening candidate
unknown relation to reinforcement
```

## Calculation / Inference Proof

```text
openings =
detect through-voids and recesses in geometry

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
through depth or recess depth

edge_distance =
minimum distance from opening boundary to component edge

relation_to_reinforcement =
intersect(opening zone, rebar map)
if no rebar map → unknown

service_reuse_allowed =
existing opening + not in bearing zone + no known rebar conflict

blocked =
opening intersects bearing zone, damaged zone, or forbidden zone
```

## Non-Derivable / Must Remain Unknown

```text
original purpose without documentation
whether opening is approved for new services
hidden rebar conflict without scan
```

---

# 12. Surface + Edge Condition

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
photos_or_scan_reference
```

If absent:

```text
condition = unknown
```

## Geometry-Derived Data

```text
face and edge classification
geometric damage candidates
```

## Evidence-Derived Data

```text
spalling
cracks
exposed reinforcement
surface contamination candidates
repair marks
visual quality
```

## Calculation / Inference Proof

```text
top/bottom/side faces =
from geometry orientation

spalling =
missing material at edges/faces in scan + visual evidence

cracks =
line features in image/scan above threshold

exposed_reinforcement =
detected steel/rust features + geometry recess

surface_contamination =
texture/color anomalies
confidence low unless lab/inspection confirms

visual_quality =
score from damage severity, discoloration, cracks, repair marks

visible_reuse_quality =
visual_quality × semantic_visibility_potential
```

## Non-Derivable / Must Remain Unknown

```text
subsurface damage
chloride contamination
microcracks
actual repair quality
```

---

# 13. Damage Records

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
damage_photo_or_scan_reference
```

## Geometry-Derived Data

```text
location
affected face/edge
size
```

## Evidence-Derived Data

```text
damage type
severity candidate
photo reference
rule relevance
```

## Calculation / Inference Proof

```text
damage_id =
component_id + "-damage-" + index

damage_kind:
line feature → crack
missing material → spalling/edge_damage
rust color → corrosion_mark
visible steel → exposed_rebar

location =
mapped from photo/scan to geometry coordinates

severity =
damage size × structural relevance × location factor

rule_relevance:
overlaps bearing zone → structural/interface relevance
overlaps visible face → architectural relevance
exposes rebar → durability/reinforcement relevance
```

## Non-Derivable / Must Remain Unknown

```text
cause of damage
repair quality
final structural severity without expert review
```

---

# 14. Concrete Evidence

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
```

## Context-Derived Data

```text
density default
evidence status
missing evidence list
confidence level
```

## Evidence-Derived Data

```text
compressive strength
tensile strength
E-modulus
carbonation depth
chloride content
pollutant content
moisture status
```

## Calculation / Inference Proof

```text
density:
if measured → measured
else material default

compressive_strength:
only from test/report
else unknown

tensile_strength:
from test
or estimated from compressive strength if project permits
status = estimated

E_modulus:
from test
or estimated from compressive strength
status = estimated

carbonation_depth:
only from carbonation test

chloride_content:
only from lab test

pollutant_content:
only from lab/screening

confidence:
tested → high
documented but old → medium
estimated/default → low
unknown → none
```

## Non-Derivable / Must Remain Unknown

```text
real compressive strength without test
chloride content
pollutants
carbonation depth
moisture condition
```

---

# 15. Reinforcement Evidence

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
```

## Geometry-Derived Data

```text
candidate structural zones
candidate support zones
```

## Context-Derived Data

```text
main reinforcement direction candidate
unknown reinforcement zones
rebar evidence status
```

## Evidence-Derived Data

```text
actual reinforcement position
cover
condition
approved drill zones
anchor zones
corrosion risk
```

## Calculation / Inference Proof

```text
main_reinforcement_direction:
from scan/drawing
else infer from structural geometry and span direction
status = inferred_low_confidence

cover:
from scan/drawing
else unknown

no_drill_zones:
known rebar zones + edge buffers + bearing zones

if no rebar map:
all structural drilling zones = unknown/blocked

drill_approved_zones:
connector zones - rebar buffers - edge buffers - damaged zones

anchor_approved_zones:
drill_approved_zones that satisfy anchor depth and spacing

corrosion_risk:
visual rust + carbonation/chloride + exposed rebar
```

## Non-Derivable / Must Remain Unknown

```text
true rebar location
safe anchor zones
corrosion inside concrete
cover depth without scan/drawing
```

---

# 16. Durability + Restnutzungsdauer

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
storage/exposure context
condition status if available
```

## Context-Derived Data

```text
freeze-thaw risk candidate
moisture risk candidate
protection requirement
```

## Evidence-Derived Data

```text
carbonation risk
chloride risk
corrosion risk
remaining service life estimate
repair requirement
```

## Calculation / Inference Proof

```text
carbonation_risk:
if carbonation_depth and cover known:
risk high if carbonation_depth >= cover
else unknown

chloride_risk:
from chloride test
else unknown

corrosion_risk:
combine carbonation_risk + chloride_risk + exposed_rebar + rust marks

freeze_thaw_risk:
exterior or wet storage context → possible risk

moisture_risk:
outdoor storage, ground contact, roof, exposed horizontal faces

repair_required:
damage severity medium/critical or exposed rebar

protection_required:
outdoor storage or moisture risk

remaining_service_life:
requires durability model and tests
else engineering_required
```

## Non-Derivable / Must Remain Unknown

```text
reliable remaining service life
internal corrosion
chloride-induced corrosion risk without test
```

---

# 17. Structural Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
material_kind
original_function
```

## Geometry-Derived Data

```text
self weight
area
span candidate
bearing zones
maximum reuse span candidate
```

## Context-Derived Data

```text
structural role
load-bearing status candidate
allowed support types
allowed bearing zones
capacity evidence status
required proof status
```

## Calculation / Inference Proof

```text
self_weight_kN =
mass_kg × 9.81 / 1000

self_weight_kN_m2 =
self_weight_kN / plan_area_m2

allowed_support_types:
slab → wall_top, beam_top, column_head_if_engineered
beam → column_top, wall_top
wall → base_line
column → base_point

allowed_span_direction:
from reinforcement if known
else inferred from geometry/original function

maximum_reuse_span:
dimension in inferred span direction
not equal to verified capacity

known_load_capacity:
only from structural proof/test
else unknown

required_proof_status:
if intended structural use and capacity unknown → proof_required
```

## Non-Derivable / Must Remain Unknown

```text
final capacity
punching resistance
moment/shear capacity
allowable live load
```

---

# 18. Connector / Interface Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
project connector library
```

## Geometry-Derived Data

```text
connector zone candidates
directions
geometry references
bearing zones
service zones
envelope faces
```

## Context-Derived Data

```text
ports
compatible ports
mandatory status
allowed connector systems
required checks
reversibility preference
```

## Calculation / Inference Proof

```text
connector_id =
component_id + connector_zone_id

port:
slab edge → slab-edge-bearing
wall top → wall-top-bearing
column top → column-head-bearing
service opening → service-penetration

compatible_ports =
lookup(connector_library, port)

mandatory:
structural support connector required for structural role → true
service/envelope connector → optional unless context requires

direction =
outward normal of connector zone

allowed_connection_role:
bearing zone → vertical-load-transfer
service zone → service-routing
envelope face → thermal-interface

allowed_connector_systems:
from pair-type connector library
example wall+slab:
post_installed_rebar_grout
screw_anchor_flat_steel_holder

min_bearing_length =
pair-type project rule

max_gap =
project tolerance

drilling_permission:
depends on reinforcement status and approved drill zones

requires_fire/thermal/service_check:
true if connector role intersects those contexts
```

## Non-Derivable / Must Remain Unknown

```text
connector capacity without product/detail
safe drilled connector without rebar evidence
actual reversibility of custom connector
```

---

# 19. Bohrzonen / No-Drill Zones

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
element_kind
project anchor/drilling defaults
```

## Geometry-Derived Data

```text
edge buffers
bearing zones
connector zones
opening buffers
```

## Evidence-Derived Data

```text
known rebar zones
cover
scan confidence
approved drill zones
```

## Calculation / Inference Proof

```text
forbidden_zones =
bearing_zones + damaged_zones + edge_buffers + opening_buffers + known_rebar_buffers

unknown_zones =
zones not covered by rebar evidence

approved_drilling_zones =
connector_zones - forbidden_zones - unknown_zones

approved_anchor_zones =
approved_drilling_zones satisfying anchor depth and spacing

minimum_edge_distance =
anchor/connector library

minimum_spacing =
anchor/connector library

rebar_conflict_status =
intersection(anchor_zone, rebar_map)

scan_confidence =
metadata from rebar scan
```

## Non-Derivable / Must Remain Unknown

```text
approved drilling zones without rebar evidence
anchor pull-out capacity
actual hidden conflict
```

---

# 20. Fire Data

## Visible Details

```text
Material fire class
Known fire resistance
Evidence status
Fire-relevant surfaces
Connector fire warning conditions
Exposed steel warning
Fire cover requirement if connected
```

## Absolute Minimum Non-Geometric Input

```text
material_kind
element_kind
```

## Context-Derived Data

```text
material fire class candidate
connector fire warning conditions
exposed steel condition
fire cover requirement condition
```

## Evidence-Derived Data

```text
known fire resistance
fire test/calculation status
```

## Calculation / Inference Proof

```text
material_fire_class:
reinforced concrete → non-combustible material assumption

known_fire_resistance:
only from proof/test/calculation
else project_context_required

fire_relevant_surfaces:
from future assembly/fire compartment context
not piece-only

connector_fire_warning:
if connector material includes exposed steel and fire context applies

fire_cover_required_if:
exposed steel connector, angle connector, steel support, unprotected steel bracket
```

## Non-Derivable / Must Remain Unknown

```text
actual fire resistance rating
compartment compliance
connector fire performance without detail
```

---

# 21. Building Physics Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
exposure_context if known
project thermal defaults
```

## Geometry-Derived Data

```text
thickness
surface area
edge zones
```

## Context-Derived Data

```text
thermal conductivity estimate
density
specific heat estimate
rough U-value
envelope relevance
insulation flag
thermal bridge zones
moisture risk
ground/roof suitability warnings
acoustic relevance
```

## Calculation / Inference Proof

```text
lambda =
measured value or material default

density =
measured or material default

R_concrete =
thickness / lambda

U_rough =
1 / (Rsi + R_concrete + Rse)

insulation_required_if_envelope:
if U_rough > project_target_U then true

thermal_bridge_zones =
connector zones crossing envelope + exposed edges

moisture_risk:
ground/exterior/roof exposure → risk candidate

acoustic_relevance:
massive component → mass relevant
```

## Non-Derivable / Must Remain Unknown

```text
final U-value of full assembly
thermal bridge Psi-value
moisture safety
actual acoustic performance
```

---

# 22. Acoustic Data

## Visible Details

```text
Mass relevance
Airborne sound data
Impact sound data
Acoustic evidence status
Recommended acoustic use
Acoustic warning
```

## Absolute Minimum Non-Geometric Input

```text
element_kind
material_kind
```

## Geometry-Derived Data

```text
area
mass per area
```

## Context-Derived Data

```text
mass relevance
recommended acoustic use candidate
acoustic warning
```

## Calculation / Inference Proof

```text
mass_per_area_kg_m2 =
mass_kg / area_m2

mass_relevance =
true if mass_per_area exceeds project threshold

airborne_sound_data =
test/database/calculation only
else unknown

impact_sound_data =
requires assembly/floor build-up
else unknown

recommended_acoustic_use =
high mass → useful for separating elements
but final use requires context

acoustic_warning =
high acoustic target + no evidence
```

## Non-Derivable / Must Remain Unknown

```text
actual airborne sound rating
impact sound performance
flanking transmission
```

---

# 23. TGA / Services Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
none beyond geometry
```

## Geometry-Derived Data

```text
existing openings
possible service opening candidates
edge distances
```

## Context-Derived Data

```text
approved service zone candidates
blocked service zones
core drilling requirement
rebar scan requirement
```

## Calculation / Inference Proof

```text
existing_service_openings =
detected openings

approved_service_zones =
existing openings + non-structural zones + zones outside known rebar/bearing

blocked_service_zones =
bearing zones + no-drill zones + damaged structural zones

cable_penetration_possible =
small opening or approved drilling zone

pipe_penetration_possible =
larger opening or approved drilling zone

core_drilling_allowed =
approved zone + rebar data + edge distance ok

core_drilling_blocked =
unknown rebar, no-drill zone, bearing zone, insufficient edge distance

rebar_scan_required =
true if new penetration requested and rebar unknown
```

## Non-Derivable / Must Remain Unknown

```text
actual TGA route fit
approved fire/acoustic sealing
safe core drilling without rebar scan
```

---

# 24. Logistics Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
current_storage_location
storage_position optional
element_kind
material_kind
```

## Geometry-Derived Data

```text
mass
dimensions
center of gravity
access faces
```

## Context-Derived Data

```text
recommended storage orientation
forbidden orientations
weather protection
separator requirement
transport mode
load securing
damage protection
temporary bracing candidate
assembly access zones
```

## Calculation / Inference Proof

```text
mass =
volume × density

recommended_storage_orientation:
slab → lying flat
wall → standing if supported, otherwise engineering_required
column → standing or supported depending length/slenderness
beam → supported at defined support points

forbidden_storage_orientations:
orientation causing unintended bending or instability

weather_protection_required:
true for outdoor storage or durability risk

separator_required:
true for stacked concrete to avoid contact damage

lifting_point_status:
known only if evidence exists
else engineering_required

transport_mode:
project default unless size/mass exceeds limits

temporary_bracing_required:
true for vertical/slender unstable elements

assembly_access_zones:
faces/edges containing connectors
```

## Non-Derivable / Must Remain Unknown

```text
safe lifting design
actual crane requirement
site access constraints
```

---

# 25. Transport Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
storage_location
target_site_location
project_transport_factor
```

## Geometry-Derived Data

```text
transport dimensions
transport mass
```

## Context-Derived Data

```text
distance
transport mode
emissions status
special transport candidate
protection requirement
load securing note
```

## Calculation / Inference Proof

```text
transport_distance_km =
route_distance(storage_location, target_site_location)

transport_mode =
project default, e.g. 40t truck

transport_gwp =
mass_t × distance_km × factor

maximum_transport_size_check =
compare dimensions to normal transport limits

special_transport_required =
dimension or mass exceeds threshold

protection_required =
true for reclaimed concrete elements

load_securing_required =
true for transport
```

## Non-Derivable / Must Remain Unknown

```text
actual route restrictions
permit requirements
exact emissions without route/mode
```

---

# 26. LCA / Ökobilanz Data

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
material_kind
project_lca_defaults
storage_location and target_site_location, if transport is included
```

## Geometry-Derived Data

```text
mass
volume
```

## Context-Derived Data

```text
reused mass
A1-A3 reuse assumption
transport impact
new equivalent reference
avoided GWP potential
dataset status
LCA completeness
```

## Calculation / Inference Proof

```text
reused_mass_t =
mass_t

A1_A3_reuse_assumption =
0 kgCO2e/t if project uses Abbau/Aufbau reuse assumption

transport_gwp =
mass_t × transport_distance_km × transport_factor

new_equivalent_reference =
map element_kind + material to project reference dataset

avoided_gwp_potential =
mass_t × new_equivalent_gwp_per_t

lca_completeness:
mass known + transport known + reference dataset known + required indicators known

GWP:
calculated if reference and transport exist

ODP/POCP/AP/EP/PE/FW/resource indicators:
only from EPD/Ökobaudat/generic datasets
```

## Non-Derivable / Must Remain Unknown

```text
full LCA without datasets
connector-specific impact
adapter impact
module B/C/D values
environmental indicators beyond GWP
```

---

# 27. Documentation

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
file references if available
```

## Context-Derived Data

```text
document IDs
document kind
title
status
confidence
missing document list
```

## Calculation / Inference Proof

```text
document_id =
component_id + "-" + document_kind

document_kind =
classify by folder/name/tag

title =
humanize(filename)

status:
file exists → available
expected but absent → missing
partial report → partial

date/author =
file metadata or unknown

confidence:
signed lab/test report → high
BIM/scan model → medium/high
manual note → low/medium
```

## Non-Derivable / Must Remain Unknown

```text
document validity
author if metadata missing
approval status without document
```

---

# 28. Evidence Completeness

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
component_id
element_kind
material_kind
```

## Geometry-Derived Data

```text
geometry completeness
mass calculability
openings completeness
connector zone candidates
```

## Context-Derived Data

```text
completeness statuses
overall completeness score
missing fields list
project-context-required flags
```

## Calculation / Inference Proof

```text
identity_complete =
component_id + element_kind + material_kind exists

geometry_complete =
geometry exists and dimensions/volume extractable

mass_complete =
measured mass or volume × density available

openings_complete =
geometry processed for openings

concrete_complete =
test report includes required concrete fields

reinforcement_complete =
scan/drawing exists and zones mapped

damage_complete =
photos/inspection exists

connector_zones_complete =
connector-zone geometry exists or generated with confidence

logistics_complete =
storage + mass + transport/lifting status known

lca_complete =
mass + transport + dataset/reference exist

fire_complete =
rating/proof exists
else requires_project_context

building_physics_complete =
thermal data + exposure context + assembly known

services_complete =
openings + service zones + rebar status known
```

## Non-Derivable / Must Remain Unknown

```text
full concrete/rebar/fire/energy completeness without evidence
```

---

# 29. Pool-Level Warnings

## Visible Details

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

## Absolute Minimum Non-Geometric Input

```text
completeness statuses
condition status if available
project required evidence list
```

## Context-Derived Data

```text
warning list
warning severity
recommended next data
```

## Calculation / Inference Proof

```text
if reinforcement.position_status == missing:
warn("Missing rebar scan")

if chloride_content == unknown and durability relevant:
warn("Missing chloride test")

if damage.severity == minor:
warn("Minor edge damage")

if lifting_points == unknown:
warn("Unknown lifting points")

if transport_distance == unknown:
warn("Unknown transport distance")

if lca.dataset == missing:
warn("Missing LCA dataset")

if fire.rating == unknown:
warn("Missing fire rating")

if thermal_conductivity == unknown:
warn("Unknown thermal conductivity")

if drilling zones unknown:
warn("Do not drill without verification")

if damaged edge overlaps bearing zone:
warn("Do not use damaged edge as bearing zone")
```

## Non-Derivable / Must Remain Unknown

```text
severity of hidden risks
actual safety of warned actions
```

---

# 30. Rule-Checker Readiness

## Visible Details

```text
Ready rules
Rules needing more evidence
Blocked actions
Default status if used
Missing evidence list
```

## Absolute Minimum Non-Geometric Input

```text
element_kind
material_kind
completeness statuses
```

## Geometry-Derived Data

```text
geometry/interface readiness
bearing zone readiness
mass/logistics readiness
```

## Context-Derived Data

```text
ready rules
rules requiring more evidence
blocked actions
default status if used
missing evidence list
```

## Calculation / Inference Proof

```text
ready_rules:
if identity complete → identity check
if geometry complete → geometry/interface check
if mass complete → logistics and LCA precheck
if bearing zones exist → bearing precheck

rules_requiring_more_evidence:
if rebar missing → anchor/drilling check
if capacity unknown → structural load check
if fire rating unknown → fire proof
if thermal context unknown → energy/envelope check
if LCA dataset missing → LCA result check

blocked_actions:
if rebar unknown → drilling blocked
if damaged bearing edge → bearing use blocked
if stock unavailable → placement blocked
if element kind incompatible → role blocked

default_connection_status:
critical missing data → invalid/block
engineering evidence missing → warning/engineering_required
all required data exists → pass possible
```

## Non-Derivable / Must Remain Unknown

```text
final pass/fail for engineering-heavy rules
approval readiness
actual safety of custom connectors
```

---

# 31. What Should Not Be Shown in This Panel

## Visible Boundary

Because this panel shows only collected pool data, it should not show:

```text
current connection validity
failed connection rules
cluster status
accumulated loads from current design
selected connector result
current design LCA total
current building score
target preference score
suggested fixes for a specific connection
```

## Absolute Minimum Rule

```text
If the information depends on an active connection or current design configuration,
it belongs outside the Piece/Bauteilpass panel.
```

## Boundary Proof

```text
Piece Panel =
data of the real component from the pool

Connection Passport =
result of connecting Piece A to Piece B

Rule Checker Panel =
active validation state of the current design

Design Dashboard =
whole-design scores, totals, and preferences
```

---

# Final Minimum Input Summary

## User or project context must provide

```text
component_id
element_kind
material_kind
source context
storage context
project defaults
optional evidence references
```

## System extracts from geometry

```text
dimensions
volume
mass if density is known/defaulted
surface and edge geometry
openings
face areas
connector-zone candidates
support-zone candidates
logistics geometry candidates
```

## System derives from context

```text
Semio binding
classification
allowed roles
connector candidates
transport precheck
LCA precheck
evidence completeness
pool-level warnings
rule-checker readiness
```

## System must not invent

```text
structural capacity
true reinforcement position
approved drilling zones
actual fire rating
final U-value
actual acoustic rating
remaining service life
approval readiness
complete LCA indicators without datasets
```

---

# Minimal UI Tab Structure

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
