# Minimum Input Strategy for the Piece Detail / Bauteilpass Panel

**Purpose:** Define the smallest amount of information a user or project context must provide so the interface can display the full Piece/Bauteilpass data panel.

**Scope:** This document follows the same structure as the previous Piece Detail / Bauteilpass panel.  
**Important constraint:** The user should not manually enter full geometry. Geometry is assumed to be available from an existing model, scan, BIM object, mesh, drawing extraction, or Semio representation. The system extracts geometric values automatically.

---

## Core Principle

The system should separate information into four classes:

```text
A. Required minimal input
   The smallest data needed from user/context to create a usable Bauteilpass.

B. Extracted from geometry/model
   Values calculated from available geometric representations.

C. Inferred from context
   Values derived from project defaults, type libraries, Semio kit context, or Abbau/Aufbau assumptions.

D. Not safely derivable
   Values that must remain unknown, warning, or engineering-required until evidence is provided.
```

---

## Absolute Minimum Input Package

To generate most of the panel automatically, the system needs only:

```text
1. component_id
2. element_kind
3. material_kind
4. one geometry/model reference
5. source/context reference
6. current storage/location reference
7. evidence package references, if available
8. project defaults
```

### Minimal Example

```yaml
minimum_input:
  component_id: DE_1OG_001
  element_kind: slab
  material_kind: reinforced_concrete
  geometry_reference: representations/DE_1OG_001/physical.glb
  source_context:
    project: Abbau Aufbau
    source_building: donor-building-001
    original_level: 1OG
    original_function: floor_slab
  current_location:
    storage_location: storage-yard-01
    storage_position: A-03-02
  evidence_refs:
    concrete_test: optional
    rebar_scan: optional
    damage_photos: optional
  project_defaults:
    density_reinforced_concrete_kg_m3: 2400
    transport_factor_kgco2e_per_tkm: 0.05
    new_precast_concrete_reference_kgco2e_per_t: 171.7
```

With this, the system can calculate or infer most fields. Unknowns are not invented; they become `unknown`, `partial`, or `engineering_required`.

---

## Calculation Proof Basics

### Volume

```text
volume_m3 = extracted_solid_volume_from_geometry
```

If the geometry is a rectangular slab and no exact solid volume is available:

```text
volume_m3 = length_m × width_m × thickness_m - openings_volume_m3
```

### Mass

```text
mass_kg = volume_m3 × density_kg_m3
mass_t = mass_kg / 1000
```

### Self weight

```text
self_weight_kN = mass_kg × 9.81 / 1000
self_weight_kN_m2 = self_weight_kN / area_m2
```

### Area

```text
area_m2 = projected_length_m × projected_width_m
```

### Transport GWP

```text
transport_gwp_kgco2e = mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

### Avoided new-material GWP potential

```text
avoided_gwp_kgco2e = mass_t × new_equivalent_gwp_kgco2e_per_t
```

### Simplified thermal resistance of concrete layer

```text
R_concrete = thickness_m / thermal_conductivity_W_mK
```

### Simplified U-value with only concrete known

```text
U_rough = 1 / (Rsi + R_concrete + Rse)
```

Where `Rsi` and `Rse` are project defaults depending on inside/outside condition.  
This is a rough precheck only, not a final energy proof.

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

## Absolute Minimum Input

```text
component_id
element_kind
material_kind
geometry_reference
current_storage_location
```

## Derived / Calculated

```text
component_name
main_dimensions
mass
thumbnail / sketch preview
availability
evidence_completeness
tracking_code
```

## Proof / Derivation

```text
component_name = humanize(component_id + element_kind)

main_dimensions = bounding_box(geometry_reference)

volume = solid_volume(geometry_reference)
mass = volume × material_density

thumbnail = first available representation tagged sketch/photo/preview
or generated preview from geometry

availability = stock_total - used_count
evidence_completeness = count(available_required_fields) / count(required_fields)
tracking_code = existing QR/RFID/BIM if provided
or generated from component_id
```

## Cannot Be Safely Derived Without Evidence

```text
true physical marking status
true availability if storage system is not synced
actual measured mass if density or geometry is uncertain
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

## Absolute Minimum Input

```text
kit_id
component_id
element_kind
geometry_reference
```

## Derived / Calculated

```text
kit_name
type_id
type_name
parent_type
type_kind
stock_total
stock_available
current_piece_ids
attribute_namespace
quality_namespace
representations
connectors
```

## Proof / Derivation

```text
kit_name = project_context.kit_name or "Bauteilkatalog"

type_id = "type-" + component_id

type_name = component_id

parent_type = "type-reclaimed-" + element_kind

type_kind = "reclaimed-" + material_kind + "-" + element_kind

stock_total = 1 for a real individual reclaimed component
unless catalogue quantity says otherwise

stock_available = stock_total - count(active_piece_instances_using_type)

current_piece_ids = query_design_graph(type_id)

attribute_namespace = project_slug, e.g. "abbauaufbau"

quality_namespace = project_slug, e.g. "abbauaufbau"

representations = all files attached to component_id

connectors = generated from element_kind + connector-zone geometry
or empty until connector zones are extracted
```

## Cannot Be Safely Derived Without Evidence

```text
true parent hierarchy if project has custom component taxonomy
actual stock if multiple identical components are grouped
connector list if no connector-zone abstraction exists
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

## Absolute Minimum Input

```text
component_id
element_kind
material_kind
source_project or project_context
```

## Derived / Calculated

```text
human_readable_name
source_building
original_level
original_zone
original_function
original_orientation
tracking_method
QR code
BIM GUID
external_reference
```

## Proof / Derivation

```text
human_readable_name = element_kind_label + " " + component_id

source_building = project_context.source_building
or parse from component_id naming convention

original_level = parse(component_id) if ID contains floor marker such as EG, 1OG, UG
else unknown

original_zone = parse(component_id) if zone marker exists
else unknown

original_function = infer from element_kind:
slab → floor_slab or roof_slab depending source level/context
wall → wall_panel
column → column
beam → beam
stair → stair_element

original_orientation = from geometry local axes and representation metadata
or unknown if not tagged

tracking_method = existing tracking reference if present
else generated QR as default

qr_code = "QR-" + component_id

bim_guid = imported from BIM if available
else generated internal GUID with status "system-generated"

external_reference = catalogue_path(component_id)
```

## Cannot Be Safely Derived Without Evidence

```text
actual physical marking on the component
real RFID tag
true original function if ID/context does not encode it
true original orientation if geometry has no orientation metadata
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

## Absolute Minimum Input

```text
component_id
stock_total
design_graph_access
```

If stock is not provided:

```text
stock_total = 1
```

## Derived / Calculated

```text
availability.state
used_count
stock_available
reserved_for_design
used_as_piece_ids
blocked_reason
storage_state
```

## Proof / Derivation

```text
used_count = count(pieces where piece.type_id == type_id)

stock_available = stock_total - used_count - reserved_count

availability.state:
if blocked_reason exists → blocked
else if reserved_for_design exists → reserved
else if used_count > 0 → placed
else if stock_available > 0 → available
else → unavailable

used_as_piece_ids = list(pieces where piece.type_id == type_id)

storage_state = current_storage_location + storage_position exists ? "located" : "unknown"
```

## Cannot Be Safely Derived Without Evidence

```text
physical presence in storage
lost/damaged after catalogue creation
manual reservation outside the system
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

## Absolute Minimum Input

```text
element_kind
material_kind
```

## Derived / Calculated

```text
primary_kind
secondary_kinds
material_family
structural_family
allowed_design_roles
disallowed_design_roles
semantic_tags
reuse_category
risk_category
```

## Proof / Derivation

```text
primary_kind = element_kind

material_family = material_kind

structural_family:
slab → horizontal_spanning
wall → vertical_panel
column → vertical_point_support
beam → horizontal_line_support
stair → circulation_component
facade → envelope_component

allowed_design_roles from element_kind library:
slab → floor_slab, roof_slab, diaphragm_if_engineered
wall → load_bearing_wall_if_verified, partition, shear_wall_if_engineered
column → vertical_support
beam → line_support
stair → circulation

disallowed_design_roles = roles structurally incompatible with primary_kind

semantic_tags = [reclaimed, material_kind, element_kind, component_pool]

reuse_category:
if condition unknown → reusable_with_verification
if condition good → reusable_preferred
if critical damage → blocked

risk_category:
calculated from missing evidence + damage + unknown structural role
```

## Cannot Be Safely Derived Without Evidence

```text
confirmed load-bearing category
approved alternative use
risk category if condition and evidence are entirely missing
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

## Absolute Minimum Input

```text
geometry_reference
material_kind
```

## Derived / Calculated

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

## Proof / Derivation

```text
unit_system = geometry metadata
or project default, e.g. mm

bounding_box = compute_AABB_or_OBB(geometry_reference)

length = longest horizontal bounding dimension
width = second horizontal bounding dimension
height/thickness = smallest dimension for slab/panel
or vertical dimension for column/wall depending orientation

gross_volume = bounding_box_volume

net_volume = solid_mesh_volume - opening_volumes
or exact BIM solid volume if available

density = material_default(material_kind)
reinforced_concrete default ≈ 2400 kg/m3 unless measured

mass = net_volume × density

center_of_gravity = volume_centroid(geometry)

local axes = imported local coordinate system
or inferred from longest/shortest dimensions

original top/bottom = metadata if available
or inferred from original orientation/context
else unknown

geometry_tolerance = project default
placement_tolerance = project default
joint_tolerance = project default
```

## Cannot Be Safely Derived Without Evidence

```text
measured density
true original top/bottom without metadata
true construction tolerances if not measured
internal voids if geometry does not include them
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

## Absolute Minimum Input

```text
at least one geometry_reference
```

## Derived / Calculated

```text
representation list
representation tags
file type
LOD
description
source
confidence
missing representations
```

## Proof / Derivation

```text
representations = files linked to component_id

tags = parse file metadata, filename, folder, or user labels
example:
physical.glb → [physical, geometry, 3d]
structural.json → [structural, analysis]
energy.json → [energy, envelope]
connector-zones.json → [connector, zones]

file_type = extension

LOD = from file metadata or inferred:
mesh/solid → physical geometry
2D SVG/PDF → sketch
JSON zones → abstracted rule geometry

confidence:
native BIM/scan with metadata → high
manual sketch → medium
filename-only inference → low
```

## Cannot Be Safely Derived Without Evidence

```text
semantic meaning of a representation if not tagged or inferable
true LOD without metadata
source reliability without provenance
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

## Absolute Minimum Input

```text
physical_geometry_reference
```

## Derived / Calculated

```text
shape type
dimensions
faces
edges
openings
cut-outs
chamfers
irregularities
damaged geometry candidates
physical tolerance
```

## Proof / Derivation

```text
shape_type = classify geometry:
thin rectangular solid → slab/panel
tall rectangular prism → column/wall depending aspect and type
long horizontal prism → beam

faces = extract mesh/solid faces

edges = extract boundary edges

openings = detect holes/voids in geometry

cutouts = non-rectangular voids or recesses

chamfers = bevelled edges detected from edge topology

irregularities = deviations from ideal bounding prism

damage candidates = geometry anomalies + linked damage photos
physical_tolerance = deviation from fitted ideal planes
```

## Cannot Be Safely Derived Without Evidence

```text
whether an irregularity is damage or intended geometry
surface contamination not visible in geometry
small cracks below scan resolution
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

## Absolute Minimum Input

```text
element_kind
geometry_reference
original_function or context
```

Optional but important:

```text
reinforcement_scan_reference
```

## Derived / Calculated

```text
structural_role
span direction candidate
support edges
bearing zones
point-support zones
line-support zones
load direction
preferred support condition
forbidden support condition
minimum bearing length default
structural thickness
structural openings
```

## Proof / Derivation

```text
structural_role from element_kind:
slab → spanning_element
wall → vertical_panel
column → vertical_support
beam → line_support

span_direction:
if reinforcement main direction known → reinforcement direction
else for rectangular slab → longer direction or project rule
else unknown/engineering_required

support_edges:
slab → two long or short edges depending span direction
beam → two end zones
wall → bottom edge and possibly top line
column → top and bottom faces

bearing_zones = support_edges buffered by required bearing width

point_support_zones:
slab + column support only if connector zone exists or engineering_required

line_support_zones:
slab edges, beam top, wall top

load_direction:
gravity → vertical downward by default

minimum_bearing_length = project default by pair type
or from structural rule library

structural_thickness = physical thickness minus non-structural layers if known
else physical thickness

structural_openings = openings intersecting load path or bearing zone
```

## Cannot Be Safely Derived Without Evidence

```text
actual capacity
punching safety
true reinforcement layout if no scan/drawing exists
moment capacity
fire-reduced structural capacity
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

## Absolute Minimum Input

```text
geometry_reference
material_kind
intended_context_if_available:
  interior / exterior / roof / ground / unknown
```

## Derived / Calculated

```text
envelope relevance
exterior/interior face candidates
ground-contact candidates
roof candidates
thermal boundary candidates
insulation faces
thermal bridge risk zones
moisture risk zones
U-value relevant surfaces
```

## Proof / Derivation

```text
if intended_context is interior:
envelope_relevance = not_relevant

if intended_context is exterior/roof/ground:
envelope_relevance = relevant

if context unknown:
envelope_relevance = requires_project_context

exterior_faces = faces connected to envelope layer in design context
or semantically tagged exterior

ground_contact_faces = downward faces at ground/foundation context

roof_faces = upper faces in roof context

thermal_boundary_faces = faces separating conditioned from unconditioned/exterior space

insulation_faces = exterior side of thermal boundary

thermal_bridge_zones = connector zones crossing thermal boundary + slab edges at exterior

moisture_risk_zones = ground-contact faces + exterior horizontal top faces + exposed joints

U-value relevant surfaces = thermal_boundary_faces
```

## Minimal Energy Calculation

```text
R_concrete = thickness_m / lambda_concrete

U_rough = 1 / (Rsi + R_concrete + Rse)
```

If `lambda_concrete` is missing:

```text
lambda_concrete = project_default_for_reinforced_concrete
status = estimated
```

## Cannot Be Safely Derived Without Evidence

```text
final U-value without full assembly build-up
moisture proof
thermal bridge Psi-value
actual insulation layer
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

## Absolute Minimum Input

```text
element_kind
geometry_reference
source_context
optional target_use_context
```

## Derived / Calculated

```text
inside/outside side
room-facing side candidates
facade-facing side candidates
visible surfaces
hidden surfaces
original use side
potential new use
spatial role
room boundary role
facade rhythm relevance
visible reuse potential
surface expression value
```

## Proof / Derivation

```text
inside/outside side:
from source BIM tags or design placement context
else unknown

room-facing faces:
faces adjacent to semantic room volumes in design context

facade-facing faces:
faces adjacent to exterior/envelope context

visible faces:
faces not covered by other layers, finishes, or hidden flags

hidden faces:
faces assigned to bearing, envelope build-up, ground, or covered assemblies

original use side:
from original_function + orientation metadata
slab top = floor walking side
slab bottom = ceiling side

potential_new_use:
from element_kind library:
slab → floor/roof
wall → wall/partition/shear wall
column → support
beam → support line

spatial_role:
from element kind + placement context

facade rhythm relevance:
true if visible exterior face or facade-facing semantic tag

visible reuse potential:
condition.visual_quality + visible surface area + damage severity

surface_expression_value:
weighted score from visible_reuse_potential, surface_condition, repair_marks
```

## Cannot Be Safely Derived Without Evidence

```text
actual desired architectural expression
inside/outside side without placement or source metadata
visual quality if photos/scans are missing
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

## Absolute Minimum Input

```text
geometry_reference
```

Optional:

```text
service_context
rebar_scan_reference
```

## Derived / Calculated

```text
opening IDs
opening type
position
size
depth
edge distance
relation to reinforcement
service reuse candidate
blocked/unknown status
```

## Proof / Derivation

```text
openings = detect voids in geometry

opening_id = component_id + opening_index

opening_type:
circular void → core_drilling
rectangular void → opening
irregular void → unknown_cutout

position = opening centroid in local coordinates

size:
circle → diameter
rectangle → width × height
through-opening depth = component thickness

edge_distance = distance(opening boundary, nearest component edge)

relation_to_reinforcement:
if rebar scan exists → intersect(opening zone, rebar map)
else unknown

service_reuse_allowed:
if opening exists and does not conflict with structural/rebar zones → candidate
else requires_verification

blocked opening:
if opening intersects bearing zone, damaged zone, or no-drill/no-service zone
```

## Cannot Be Safely Derived Without Evidence

```text
original purpose
whether existing opening is code-compliant for new TGA
hidden reinforcement conflict without scan
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

## Absolute Minimum Input

```text
photos_or_scan_reference
```

If no visual evidence exists:

```text
all condition fields = unknown
```

## Derived / Calculated

```text
face condition
edge condition
spalling candidates
crack candidates
exposed reinforcement candidates
surface contamination candidates
repair marks
visual quality
visible reuse quality
```

## Proof / Derivation

```text
top/bottom/side faces = geometry face classification

condition = visual inspection data or computer vision classification

spalling = detected missing concrete at edges/faces + visual evidence

cracks = line features in photos/scans above detection threshold

exposed reinforcement = metallic linear features + damage context

surface contamination = color/texture anomaly, only low confidence

repair marks = patch-like surface regions

visual_quality = score(surface damage, discoloration, cracks, repair marks)

visible_reuse_quality = visual_quality × semantic_visibility_potential
```

## Cannot Be Safely Derived Without Evidence

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

## Absolute Minimum Input

```text
damage_photo_or_scan_reference
```

Optional:

```text
manual_damage_annotation
```

## Derived / Calculated

```text
damage ID
damage type candidate
location
affected face/edge
severity candidate
size
photo reference
rule relevance
```

## Proof / Derivation

```text
damage_id = component_id + damage_index

damage_kind = classification from visual evidence:
line → crack
missing edge material → edge damage/spalling
rust color near rebar → corrosion mark
visible steel → exposed reinforcement

location = map photo/scan coordinates to geometry face/edge

severity:
minor/medium/critical from size + location + structural relevance
example:
damage at bearing zone → higher severity
damage at non-structural visible face → lower severity

size = measured bounding box of damage region

photo_reference = source image used

rule_relevance:
if damage overlaps bearing zone → affects structural/interface rules
if damage overlaps visible face → affects architectural/visible reuse
if damage exposes rebar → affects durability/rebar rules
```

## Cannot Be Safely Derived Without Evidence

```text
repair status unless documented
cause of damage
structural severity without engineering judgement
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

## Absolute Minimum Input

```text
material_kind
```

Optional evidence:

```text
concrete_test_report
core_sample_report
lab_report
```

## Derived / Calculated

```text
density estimate
E-modulus estimate
evidence status
confidence level
missing evidence flags
```

## Proof / Derivation

```text
density:
if measured density exists → measured
else material default, e.g. reinforced_concrete ≈ 2400 kg/m3

compressive_strength:
only from test report or existing documentation
else unknown

tensile_strength:
from test report or estimated from compressive strength with engineering formula
status = estimated/engineering_required

E-modulus:
from test report
or estimated from compressive strength using selected project formula
status = estimated

carbonation_depth:
only from carbonation test
else unknown

chloride_content:
only from lab test
else unknown

pollutant_content:
only from lab/screening report
else unknown

moisture_status:
from test or environmental context
else unknown

confidence_level:
tested → high
documented but old → medium
default/estimated → low
unknown → none
```

## Cannot Be Safely Derived Without Evidence

```text
real concrete strength
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

## Absolute Minimum Input

```text
element_kind
structural_geometry
```

Optional but required for high confidence:

```text
rebar_scan_reference
reinforcement_drawing
```

## Derived / Calculated

```text
main reinforcement direction candidate
secondary reinforcement direction candidate
no-drill zones candidate
unknown reinforcement zones
rebar evidence status
```

## Proof / Derivation

```text
main_reinforcement_direction:
if scan/drawing exists → from evidence
else infer from slab span direction or original function
status = inferred_low_confidence

cover:
from scan/drawing/test
else unknown

no_drill_zones:
from rebar map + cover zones + bearing zones
if no rebar map → all structurally relevant zones become unknown/blocked for drilling

drill_approved_zones:
zones with sufficient distance from rebar and edges
only if rebar data exists

anchor_approved_zones:
intersection of connector zones + drill-approved zones + edge distance rules

unknown_zones:
all zones not scanned or not documented

corrosion_risk:
from condition + carbonation/chloride + visual rust
else unknown
```

## Cannot Be Safely Derived Without Evidence

```text
true rebar location
true cover depth
safe anchor zones
corrosion inside concrete
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

## Absolute Minimum Input

```text
material_kind
condition_status
exposure_context_if_known
```

Optional evidence:

```text
carbonation_test
chloride_test
moisture_data
```

## Derived / Calculated

```text
durability status
carbonation risk
chloride risk
corrosion risk
freeze-thaw risk
moisture exposure risk
repair requirement
protection requirement
```

## Proof / Derivation

```text
carbonation_risk:
if carbonation_depth known + cover known:
risk = carbonation_depth >= cover ? high : lower
else unknown

chloride_risk:
from chloride test
else unknown

corrosion_risk:
combine carbonation_risk + chloride_risk + exposed_rebar + rust marks

freeze_thaw_risk:
if exterior/roof/ground/exposed moisture context → possible
else low/not_relevant

moisture_exposure_risk:
from energy/envelope context + storage/weather exposure

repair_required:
if damage severity medium/critical or exposed rebar → true

protection_required:
if outdoor storage or moisture risk → true

remaining_service_life:
requires durability model and tests
else unknown/engineering_required
```

## Cannot Be Safely Derived Without Evidence

```text
reliable remaining service life
chloride-induced corrosion risk
internal corrosion
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

## Absolute Minimum Input

```text
element_kind
geometry_reference
material_kind
original_function_or_context
```

## Derived / Calculated

```text
structural role
load-bearing status candidate
self weight
allowed support types
allowed bearing zones
allowed span direction candidate
maximum reuse span candidate
capacity evidence status
required proof status
original structural function
```

## Proof / Derivation

```text
structural_role = classification from element_kind

load_bearing_status:
slab/beam/column/load-bearing wall → likely structural
partition/facade → unknown or non-structural until evidence

self_weight_kN = mass_kg × 9.81 / 1000

self_weight_kN_m2 = self_weight_kN / area_m2

allowed_support_types:
slab → wall_top, beam_top, column_head_if_engineered
beam → column_top, wall_top
wall → base/foundation line
column → foundation/base point

allowed_bearing_zones = structural_geometry.bearing_zones

allowed_span_direction:
from reinforcement evidence if available
else inferred from aspect ratio + element kind

maximum_reuse_span:
from dimensions + original function
not final capacity

known_load_capacity:
only if evidence/test/static proof exists
else unknown

capacity_evidence_status:
tested/documented/unknown

required_proof_status:
if used structurally and capacity unknown → structural_proof_required
```

## Cannot Be Safely Derived Without Evidence

```text
final load capacity
punching resistance
moment/shear capacity
actual design load
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

## Absolute Minimum Input

```text
element_kind
structural_geometry
connector_zone_geometry if available
```

## Derived / Calculated

```text
connector ID
connector name
connector type
port
compatible ports
mandatory status
direction
geometry reference
allowed connection role
allowed connector systems
minimum bearing length
maximum gap
edge distance requirement
drilling permission
check requirements
reversibility preference
```

## Proof / Derivation

```text
connector_id = component_id + connector_zone_id

connector_name = humanize(connector_id)

connector_type:
bearing edge → bearing connector
service zone → service connector
envelope face → envelope connector
lifting point → logistics connector

port:
slab bearing edge → slab-edge-bearing
wall top → wall-top-bearing
column top → column-head-bearing
beam top → beam-top-bearing
service opening → service-penetration

compatible_ports = connector library by port

mandatory:
structural supports required for element role → true
optional service/envelope connectors → false

direction = outward normal of connector zone

geometry_reference = connector-zone geometry object

allowed_connection_role:
bearing zone → vertical-load-transfer
service zone → service-routing
envelope face → thermal-envelope-interface

allowed_connector_systems:
from Abbau/Aufbau connector library by pair type
example:
wall+slab → post_installed_rebar_grout, screw_anchor_flat_steel_holder

minimum_bearing_length = project rule by pair type

maximum_gap = project tolerance

edge_distance_requirement = connector library + anchor rules

drilling_permission:
if rebar map missing → unknown/blocked
if approved zone exists → allowed in approved zone

fire/structural/thermal/service checks:
set true depending connector role and context

reversibility_preference:
from project preference or connector library
```

## Cannot Be Safely Derived Without Evidence

```text
safe drilled connector zone without rebar evidence
connector capacity
actual reversibility if custom connector is used
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

## Absolute Minimum Input

```text
connector_zone_geometry
reinforcement_evidence_status
```

For real approved drilling zones:

```text
rebar_scan_reference
```

## Derived / Calculated

```text
approved drilling zones
forbidden drilling zones
unknown zones
approved anchor zones
forbidden anchor zones
minimum edge distance
minimum spacing
cover requirement
rebar conflict status
scan confidence
```

## Proof / Derivation

```text
forbidden_zones:
bearing zones + damaged zones + edge buffers + known rebar zones

unknown_zones:
zones without rebar evidence

approved_drilling_zones:
connector zones
minus forbidden_zones
minus rebar buffers
minus edge buffers

approved_anchor_zones:
approved_drilling_zones
where anchor depth and spacing are possible

minimum_edge_distance:
from connector/anchor library

minimum_spacing:
from connector/anchor library

cover_requirement:
from reinforcement evidence or project default

rebar_conflict_status:
intersection(anchor_zone, rebar_map)

scan_confidence:
from scan metadata or evidence status
```

## Cannot Be Safely Derived Without Evidence

```text
approved drilling zones if reinforcement is unknown
actual rebar conflict without scan
anchor pull-out capacity
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

## Absolute Minimum Input

```text
material_kind
element_kind
```

Optional:

```text
fire_test_or_classification
project_fire_context
```

## Derived / Calculated

```text
material fire class candidate
evidence status
fire-relevant surfaces candidate
connector fire warning conditions
exposed steel warning condition
fire cover requirement if connected
```

## Proof / Derivation

```text
material_fire_class:
reinforced concrete → non-combustible material assumption
status = material-level only

known_fire_resistance:
only if tested/documented or calculated by engineer
else unknown/project_context_required

fire_relevant_surfaces:
surfaces that become part of compartment/escape/envelope in design context

connector_fire_warning_conditions:
if connector material = steel and fire relevant → fire cover required warning

exposed_steel_warning:
true if connector system includes exposed steel

fire_cover_required_if:
angle connector, steel beam support, exposed steel plate, unprotected anchor
in fire-relevant assembly
```

## Cannot Be Safely Derived Without Evidence

```text
actual fire resistance rating
fire compartment compliance
connector fire performance
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

## Absolute Minimum Input

```text
material_kind
geometry_reference
exposure_context if known
```

## Derived / Calculated

```text
thermal conductivity estimate
density
specific heat estimate
rough U-value
envelope relevance
insulation requirement flag
thermal bridge zones
moisture risk
ground-contact suitability
roof suitability
acoustic relevance
```

## Proof / Derivation

```text
thermal_conductivity:
from material dataset default
else unknown

density:
from measured density or material default

specific_heat:
from material dataset default

rough U-value:
R = thickness / lambda
U = 1 / (Rsi + R + Rse)

envelope_relevance:
from exposure_context or semantic placement

insulation_requirement_if_envelope:
if rough U-value > project target → insulation_required

thermal_bridge_zones:
connectors crossing envelope + slab edges at exterior

moisture_risk:
ground/exterior/roof exposure → risk candidate

ground_contact_suitability:
requires moisture/durability context
default = requires_verification

roof_suitability:
requires waterproofing + structural + thermal context
default = requires_verification

acoustic_relevance:
massive concrete → mass relevant
actual acoustic values unknown unless tested
```

## Cannot Be Safely Derived Without Evidence

```text
final U-value of complete assembly
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

## Absolute Minimum Input

```text
mass
element_kind
material_kind
```

## Derived / Calculated

```text
mass relevance
acoustic evidence status
recommended acoustic use candidate
acoustic warning
```

## Proof / Derivation

```text
mass_relevance:
massive concrete + high mass per area → relevant for airborne sound

mass_per_area = mass_kg / area_m2

airborne_sound_data:
only from test/database/calculation
else unknown

impact_sound_data:
only from assembly context with floor build-up
else unknown

recommended_acoustic_use:
if high mass → useful for separation layers/walls/floors
but context required

acoustic_warning:
if intended use has high acoustic demand and no acoustic evidence → warning
```

## Cannot Be Safely Derived Without Evidence

```text
actual airborne sound rating
actual impact sound rating
performance after new assembly
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

## Absolute Minimum Input

```text
openings_from_geometry
reinforcement_evidence_status
```

Optional:

```text
service_route_context
```

## Derived / Calculated

```text
existing service openings
approved service zones
blocked service zones
possible cable penetrations
possible pipe penetrations
core drilling allowed/blocked
rebar scan requirement
```

## Proof / Derivation

```text
existing_service_openings = openings detected in geometry

approved_service_zones:
existing openings + zones outside structural bearing and known rebar
if rebar data missing → requires verification

blocked_service_zones:
bearing zones + no-drill zones + damaged structural zones

cable_penetration_possible:
small openings or approved drilling zones
status depends on rebar evidence

pipe_penetration_possible:
larger openings or approved drilling zones
requires stronger evidence

core_drilling_allowed:
only if zone is approved + rebar conflict absent

core_drilling_blocked:
if no-drill zone, bearing zone, unknown rebar, or insufficient edge distance

rebar_scan_required:
true if new penetration is requested and rebar unknown
```

## Cannot Be Safely Derived Without Evidence

```text
actual TGA route compatibility
approved core drilling without rebar scan
service fire/acoustic sealing
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

## Absolute Minimum Input

```text
current_storage_location
geometry_reference
mass_or_material_density
element_kind
```

## Derived / Calculated

```text
storage position
recommended storage orientation
forbidden storage orientations
weather protection required
separator required
mass
lifting point status
transport mode
transport readiness
load securing
damage protection
temporary bracing requirement
assembly access zones
installation notes
```

## Proof / Derivation

```text
mass = volume × density if not measured

recommended_storage_orientation:
slab → lying flat
wall/column → usually standing only if safely supported; otherwise project rule
beam → supported at defined points

forbidden_storage_orientations:
orientations causing unsupported bending or instability

weather_protection_required:
true if outdoor storage or durability risk

separator_required:
true for concrete elements stacked/stored to avoid damage

lifting_point_status:
if lifting points documented → known
else engineering_required

transport_mode:
project default truck unless size/mass exceeds limits

transport_readiness:
mass known + dimensions known + storage accessible + protection required

load_securing_required:
always true for transport

damage_protection_required:
true for reused components

temporary_bracing_required:
vertical unstable elements → likely true
horizontal slabs → during lifting/installation check

assembly_access_zones:
from connector zones and geometry
```

## Cannot Be Safely Derived Without Evidence

```text
safe lifting point design
actual crane requirement
actual site access
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

## Absolute Minimum Input

```text
storage_location
target_site_location
component_dimensions
component_mass
project_transport_factor
```

If target site is unknown:

```text
transport_distance = unknown
```

## Derived / Calculated

```text
transport mode
transport distance
transport emissions status
maximum transport size check
special transport required
protection requirement
load securing note
```

## Proof / Derivation

```text
transport_distance_km = route_distance(storage_location, target_site_location)

transport_mode = project default, e.g. truck_40t

transport_factor = project default, e.g. kgCO2e/tkm

transport_gwp = mass_t × distance_km × factor

maximum_transport_size_check:
compare bounding_box to normal transport limits

special_transport_required:
if dimension or mass exceeds limit

protection_required = true for reclaimed elements

load_securing_note = required by transport mode
```

## Cannot Be Safely Derived Without Evidence

```text
actual route restrictions
actual transport permit requirement
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

## Absolute Minimum Input

```text
material_kind
mass
transport_distance or locations
project_lca_defaults
```

## Derived / Calculated

```text
reused mass
A1-A3 reuse assumption
transport factor
transport impact
new equivalent reference
new equivalent GWP
avoided GWP potential
generic dataset status
LCA completeness
indicator placeholders
```

## Proof / Derivation

```text
reused_mass_t = mass_t

A1-A3 reuse assumption:
for reused component, project may set manufacturing impact to 0 for reuse scenario
status = project_assumption

transport_factor = project default

transport_gwp = mass_t × transport_distance_km × transport_factor

new_equivalent_reference:
map element_kind + material to reference dataset
slab reinforced concrete → precast concrete slab reference

new_equivalent_gwp = dataset value

avoided_gwp_potential = mass_t × new_equivalent_gwp_kgco2e_per_t

connector/adapters are not included here unless already part of pool data

generic_dataset_status:
if EPD/Ökobaudat link missing → generic_required

lca_completeness:
complete only if mass + transport + dataset + reference exist

environmental indicators:
from EPD/Ökobaudat if linked
else unknown
```

## Cannot Be Safely Derived Without Evidence

```text
full LCA without datasets
connector-specific impact
module B/C/D impacts
exact environmental indicators beyond GWP
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

Each document should show:

```text
document.id
document.kind
document.title
document.url
document.status
document.date
document.author
document.confidence
```

## Absolute Minimum Input

```text
component_id
file_links if available
```

## Derived / Calculated

```text
document IDs
document kind
title
status
confidence
missing document list
```

## Proof / Derivation

```text
document_id = component_id + document_kind

document_kind = classify file by folder/name/tag:
photos/ → photo
scan/ → laser_scan
evidence/concrete → concrete_test_report
evidence/rebar → rebar_scan
lca/ → lca_document

title = humanize(filename)

url = file path

status:
file exists → available
file missing but expected → missing
partial scan/report → partial

date/author:
from file metadata if available
else unknown

confidence:
signed/tested report → high
scan/model → medium/high depending source
manual note → low/medium
```

## Cannot Be Safely Derived Without Evidence

```text
document author if metadata missing
document validity
approval status
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

## Absolute Minimum Input

```text
component_id
element_kind
geometry_reference
material_kind
```

## Derived / Calculated

```text
completeness status for each evidence category
overall completeness score
missing fields list
project-context-required flags
```

## Proof / Derivation

```text
identity complete:
component_id + kind + material + source exists

geometry complete:
geometry_reference exists and dimensions/volume extractable

mass complete:
mass measured or mass calculable from volume × density

openings complete:
geometry processed for openings
else partial/unknown

concrete complete:
test report includes required concrete fields
else partial/missing

reinforcement complete:
rebar scan/drawing exists and zones are mapped
else partial/missing

damage complete:
visual inspection/photos exist
else missing

connector zones complete:
connector-zone representation exists or generated with confidence
else partial

logistics complete:
storage location + mass + transport status + lifting status known

LCA complete:
mass + transport + dataset/reference exist

fire complete:
component fire rating or project fire calculation exists
else requires_project_context

building physics complete:
thermal data + context + assembly known
else requires_project_context

services complete:
openings + service zones + rebar status known
else partial
```

## Cannot Be Safely Derived Without Evidence

```text
full completeness for concrete/rebar/fire/energy without project evidence
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

Visible fields:

```text
pool_warnings.id
pool_warnings.kind
pool_warnings.message
pool_warnings.severity
pool_warnings.related_data_field
pool_warnings.recommended_next_data
```

## Absolute Minimum Input

```text
completeness statuses
damage records
material evidence statuses
logistics statuses
```

## Derived / Calculated

```text
warning list
warning severity
related data field
recommended next data
```

## Proof / Derivation

```text
if reinforcement.position_status == missing:
warning = Missing rebar scan

if chloride_content == unknown and durability context relevant:
warning = Missing chloride test

if damage.severity == minor:
warning = Minor edge damage

if lifting_points == unknown:
warning = Unknown lifting points

if transport_distance == unknown:
warning = Unknown transport distance

if lca.dataset == missing:
warning = Missing LCA dataset

if fire.rating == unknown:
warning = Missing fire rating

if thermal_conductivity == unknown:
warning = Unknown thermal conductivity

if drilling zones are unknown:
warning = Do not drill without verification

if damaged edge overlaps bearing zone:
warning = Do not use damaged edge as bearing zone
```

## Cannot Be Safely Derived Without Evidence

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

## Absolute Minimum Input

```text
all completeness statuses
element_kind
connector zones
material evidence status
```

## Derived / Calculated

```text
ready rules
rules needing more evidence
blocked actions
default status if used
missing evidence list
```

## Proof / Derivation

```text
ready_rules:
if identity complete → identity check ready
if geometry complete → geometry/interface check ready
if mass complete → logistics/LCA mass precheck ready
if bearing zones exist → bearing precheck ready

rules_requiring_more_evidence:
if rebar missing → anchor/drilling check needs evidence
if capacity unknown → structural load check needs evidence
if fire rating unknown → fire check needs project proof
if thermal context unknown → envelope check needs context
if LCA dataset missing → LCA check needs dataset

blocked_actions:
if rebar unknown → drilling blocked
if damaged bearing edge → use as bearing blocked
if stock used → placement blocked
if element kind incompatible → role blocked

default_connection_status_when_used:
if any engineering-required evidence missing → warning/engineering_required
if critical missing hard evidence → invalid/block
else pass
```

## Cannot Be Safely Derived Without Evidence

```text
final pass/fail for engineering rules
actual approval readiness
```

---

# 31. What Should Not Be Shown in This Panel

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
If the data depends on a specific active connection or design configuration,
it belongs to the Connection Passport or Rule Checker Panel,
not the Piece/Bauteilpass panel.
```

## Proof / Boundary Logic

```text
Piece panel = data of the real component from the pool

Connection Passport = result of connecting Piece A to Piece B

Rule Checker Panel = active validation state of current design

Design Dashboard = whole-design scores and totals
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

---

# Final Summary

The minimum data strategy is:

```text
User gives:
component_id
element_kind
material_kind
geometry/model reference
source/storage context
optional evidence references

System derives:
dimensions
volume
mass
surface/edge/opening data
geometry abstractions
classification
connector candidates
logistics prechecks
LCA prechecks
completeness statuses
pool warnings
rule-checker readiness

System does not invent:
structural capacity
true reinforcement position
fire resistance rating
final U-value
approval readiness
actual service life
exact LCA indicators without datasets
```

This keeps the interface minimal for the user but detailed enough for Abbau/Aufbau-style reclaimed component design.
