# Concrete Example — Geometry-Generator-Based Bauteilpass System  
## Abbau/Aufbau Component DE_1OG_001 + ReCreate Framework Logic

**Purpose**  
This document applies the same system format to one concrete example component.

**Example component**  
The worked example uses the Abbau/Aufbau catalogue component **DE_1OG_001**, interpreted here as a reclaimed reinforced-concrete **slab / Deckenplatte**.

**Source data from Abbau/Aufbau catalogue**

```text
Component ID: DE_1OG_001
Typology: slab / Deckenplatte
Material: reinforced concrete / Stahlbeton
Dimensions: L 4500 mm × B 2300 mm × H 180 mm
Openings: none recorded
Catalogue volume: 1.863 m³
Catalogue mass: ca. 4.1 t
```

**ReCreate role in this document**  
ReCreate is used as the broader reference framework for:

```text
building / component / connector typology thinking
quality management logic
traceability logic
BIM / digital component data logic
reuse-readiness and evidence logic
```

**Important correction maintained**  
Geometry Generators do **only geometry-related work**.

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

The **system modules** do everything else:

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

## 1.1 Main Pipeline for This Example

```text
Minimum Input
+ Base Geometry of DE_1OG_001
+ Typology: slab
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

## 1.2 Minimum Input for This Example

```yaml
minimum_input:
  component_id: DE_1OG_001
  component_typology: slab
  material_kind: reinforced_concrete

  base_geometry_reference: generated_from_catalogue_dimensions/DE_1OG_001.glb

  source_context:
    source_project: Abbau Aufbau
    source_document: Handbuch zur Wiederverwendung von Stahlbetonelementen
    source_catalogue_section: Bauteilkatalog und Bauteilelogistik
    original_level: 1OG
    original_function: floor_slab_candidate

  pool_context:
    kit_id: kit-abbau-aufbau-example-pool
    current_storage_location: example-storage-yard-01
    storage_position: A-03-02
    note: "Storage data is example project context, not directly from the handbook table."

  project_defaults:
    density_reinforced_concrete_kg_m3: 2400
    lambda_reinforced_concrete_W_mK: 2.3
    transport_factor_kgco2e_per_tkm: 0.05
    new_precast_concrete_reference_kgco2e_per_t: 171.7
    example_transport_distance_km: 30
    example_target_u_value_W_m2K: 0.24
    example_min_bearing_length_mm: 80
    example_max_joint_gap_mm: 40

  optional_evidence:
    concrete_test_report: null
    reinforcement_scan: null
    damage_photos: null
    fire_document: null
    lca_dataset: null
```

## 1.3 Geometry Generators Produce

```text
normalized slab geometry
physical slab representation
structural slab geometry representation
energy / envelope geometry representation
semantic slab representation
connector-zone geometry
slab-edge-bearing ports
opening geometry
penetration candidates
logistics geometry
face / edge / zone maps
geometry-derived volume
geometry-derived surface and area data
```

## 1.4 System Modules Produce

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

# 2. Core Concepts in the Example

## 2.1 Bauteilpass

The **Bauteilpass** for DE_1OG_001 is the digital passport of this one real reclaimed slab.

It combines:

```text
Abbau/Aufbau catalogue data
generated slab geometry representations
project defaults
optional evidence data
system-derived prechecks
documentation state
rule-checker readiness
```

## 2.2 Geometry Generator

For this example, the main generator is the **Slab Geometry Generator**.

It receives:

```text
component typology = slab
base geometry = 4500 × 2300 × 180 mm plate
material = reinforced concrete
project geometry defaults
optional evidence
```

It outputs only geometry-related information:

```text
top face
bottom face
long edges
short edges
edge-bearing candidates
slab-edge-bearing ports
service-zone candidates
envelope-face candidates
opening map
transport envelope
plan area
volume
face areas
edge zones
```

It does **not** decide:

```text
final structural validity
material strength
fire resistance
LCA completeness
approval readiness
connection validity
target preference score
```

## 2.3 System Module

System modules consume the generated geometry plus Abbau/Aufbau catalogue data, ReCreate-inspired quality/evidence logic, project defaults, and optional evidence documents.

They produce:

```text
classification
evidence state
material state
warnings
readiness states
LCA prechecks
logistics information
documentation completeness
```

---

# 3. Correct Responsibility Split

## 3.1 Geometry Generators Used in This Example

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

## 3.2 System Modules Used in This Example

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

| Part | Concrete example responsibility | Does not do |
|---|---|---|
| **Geometry Generators** | generate slab faces, edges, bearing zones, ports, openings, envelope candidates, transport envelope | decide final validity, strength, LCA, approval |
| **System Modules** | interpret the generated geometry with Abbau/Aufbau catalogue data, ReCreate quality logic, evidence, defaults, and rule libraries | create raw geometry |
| **Rule Checker** | evaluates active placements and connections, e.g. slab-to-wall | store raw pool data |
| **Bauteilpass Panel** | displays pool and generated component data for DE_1OG_001 | show active connection result |
| **Connection Passport** | stores the result of connecting DE_1OG_001 to another component | replace the Bauteilpass |

---

# 4. Typology Library Entry for the Example

## 4.1 Slab Typology Used for DE_1OG_001

```yaml
typology:
  id: slab
  name: Deckenplatte
  material_family: reinforced_concrete

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
    - long_edge_bearing_candidates
    - short_edge_bearing_candidates
    - opening_zones
    - no_drill_candidates
    - lifting_face_candidates
    - transport_envelope
```

## 4.2 Abbau/Aufbau Connector Logic Relevant to This Slab

When this slab is connected to a wall, the Abbau/Aufbau execution-planning logic gives two relevant wall-slab connection families:

```text
wall + slab
→ post-installed reinforcement connection + grout / injection mortar
→ screw anchor + flat steel holder
```

When the slab is connected to a column, the broader connection family may include:

```text
column + slab
→ post-installed stainless dowel
→ angle connector
→ post-installed reinforcement + grout on new reinforced-concrete beam
→ bearing on steel beam
```

These connector families are not chosen by the Generator.  
The Generator only creates the slab-edge or slab-support ports.  
The System Module maps these ports to possible connector families.

## 4.3 ReCreate Framework Role

ReCreate is used here to justify the hierarchy:

```text
building scale
component scale
connector scale
quality-management scale
traceability / BIM / digital marketplace scale
```

In this document, ReCreate supports the idea that a component should be understood through typology, quality/evidence, documentation, traceability, and reuse-readiness.  
It does not provide the dimensions of DE_1OG_001; those come from Abbau/Aufbau.

---

# 5. Shared Calculations for DE_1OG_001

## 5.1 Dimensions

```text
length = 4500 mm = 4.5 m
width = 2300 mm = 2.3 m
thickness = 180 mm = 0.18 m
```

## 5.2 Plan Area

```text
plan_area_m2 = 4.5 × 2.3 = 10.35 m²
```

## 5.3 Catalogue Volume

```text
volume_m3 = 4.5 × 2.3 × 0.18
volume_m3 = 1.863 m³
```

This matches the Abbau/Aufbau catalogue value.

## 5.4 Catalogue Mass

```text
catalogue_mass_t = ca. 4.1 t
catalogue_mass_kg = 4100 kg
```

## 5.5 Implied Density from Catalogue Mass

Because the catalogue gives both volume and approximate mass:

```text
implied_density_kg_m3 =
catalogue_mass_kg / volume_m3

implied_density_kg_m3 =
4100 / 1.863

implied_density_kg_m3 ≈ 2201 kg/m³
```

## 5.6 Mass from Default Reinforced-Concrete Density

If the system used a default density of 2400 kg/m³:

```text
default_mass_kg =
1.863 × 2400

default_mass_kg =
4471.2 kg

default_mass_t =
4.47 t
```

## 5.7 System Decision

```text
Because Abbau/Aufbau gives a catalogue mass,
the system uses catalogue_mass = ca. 4.1 t.

It also stores:
calculated_default_mass = 4.47 t
implied_density = 2201 kg/m³
mass_source = catalogue
mass_confidence = medium
```

## 5.8 Self-Weight

Using the catalogue mass:

```text
self_weight_kN =
4100 × 9.81 / 1000

self_weight_kN =
40.22 kN
```

Per square metre:

```text
self_weight_kN_m2 =
40.22 / 10.35

self_weight_kN_m2 =
3.89 kN/m²
```

## 5.9 Transport GWP Precheck

Example transport distance:

```text
distance = 30 km
transport_factor = 0.05 kgCO2e/tkm
mass = 4.1 t
```

Calculation:

```text
transport_gwp =
4.1 × 30 × 0.05

transport_gwp =
6.15 kgCO2e
```

## 5.10 Avoided New-Material GWP Potential

Using the Abbau/Aufbau / Ökobaudat example reference:

```text
new_precast_concrete_reference =
171.7 kgCO2e/t
```

Calculation:

```text
avoided_gwp_potential =
4.1 × 171.7

avoided_gwp_potential =
703.97 kgCO2e
```

## 5.11 Rough U-Value Precheck

Assume:

```text
thickness = 0.18 m
lambda_concrete = 2.3 W/mK
Rsi = 0.13
Rse = 0.04
```

Calculation:

```text
R_concrete =
0.18 / 2.3

R_concrete =
0.078 m²K/W
```

```text
U_rough =
1 / (0.13 + 0.078 + 0.04)

U_rough =
4.03 W/m²K
```

System interpretation:

```text
This is not a final energy result.
If DE_1OG_001 becomes part of the thermal envelope,
the system flags: insulation / full assembly proof required.
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
Component ID: DE_1OG_001
Component name: Deckenplatte DE_1OG_001
Element kind: slab / Deckenplatte
Material: reinforced concrete / Stahlbeton
Current availability: available
Current storage location: example-storage-yard-01 / A-03-02
Thumbnail / sketch: generated slab preview
Main dimensions: 4500 × 2300 × 180 mm
Mass: ca. 4.1 t
Evidence completeness: partial
Tracking code: QR-DE_1OG_001
```

### Minimum Input

```text
component_id = DE_1OG_001
component_typology = slab
material_kind = reinforced_concrete
base_geometry_reference = generated_from_catalogue_dimensions/DE_1OG_001.glb
current_storage_location = example-storage-yard-01
```

### Geometry Generator Output

```text
main dimensions = 4500 × 2300 × 180 mm
net volume = 1.863 m³
preview geometry = thin rectangular slab
```

### System Output

```text
component name = Deckenplatte DE_1OG_001
material label = Stahlbeton
availability = available
mass = ca. 4.1 t
evidence completeness = partial
tracking code = QR-DE_1OG_001
```

### Proof

```text
component_name =
"Deckenplatte " + DE_1OG_001

volume =
4.5 × 2.3 × 0.18 =
1.863 m³

mass =
catalogue mass = ca. 4.1 t

tracking_code =
"QR-" + component_id
```

### Must Remain Unknown

```text
actual physical marking status
real storage verification
measured mass if catalogue mass is approximate
```

---

## 1. Semio Binding

### Visible Details

```text
Kit ID: kit-abbau-aufbau-example-pool
Kit name: Abbau/Aufbau Example Bauteilkatalog
Type ID: type-DE_1OG_001
Type name: DE_1OG_001
Parent type: type-reclaimed-slab
Type kind: reclaimed-reinforced_concrete-slab
Stock quantity: 1
Available quantity: 1
Current Piece IDs using this Type: []
Attribute namespace: abbauaufbau
Quality namespace: abbauaufbau
Representation list: base, physical, structural, energy, semantic, connector-zones, logistics
Connector list: generated slab ports
```

### Minimum Input

```text
kit_id = kit-abbau-aufbau-example-pool
component_id = DE_1OG_001
component_typology = slab
material_kind = reinforced_concrete
base_geometry_reference
```

### Geometry Generator Output

```text
generated physical geometry
generated structural geometry
generated energy geometry
generated semantic geometry
generated connector-zone geometry
generated slab ports
```

### System Output

```text
type_id = type-DE_1OG_001
type_kind = reclaimed-reinforced_concrete-slab
stock_total = 1
stock_available = 1
representations registered in Semio
connectors registered as Semio connectors
```

### Proof

```text
type_id =
"type-" + "DE_1OG_001"

parent_type =
"type-reclaimed-" + "slab"

stock_total =
1 because DE_1OG_001 is one real catalogue element

stock_available =
1 - active_piece_count
```

### Must Remain Unknown

```text
whether multiple physical copies exist
manual connector overrides
real external stock synchronization
```

---

## 2. Identity + Traceability

### Visible Details

```text
Component ID: DE_1OG_001
Human-readable name: DE_1OG_001 (slab)
Element type: slab / Deckenplatte
Material type: reinforced concrete / Stahlbeton
Source project: Abbau Aufbau
Source building: unknown / project-specific
Original level: 1OG
Original zone: unknown
Original function: floor slab candidate
Original orientation: generated from slab typology
Tracking method: generated QR unless real tracking exists
QR code: QR-DE_1OG_001
RFID code: unknown
BIM GUID: system-generated unless imported
External database reference: catalogue/DE_1OG_001
Physical marking status: unknown
```

### Minimum Input

```text
component_id = DE_1OG_001
component_typology = slab
material_kind = reinforced_concrete
source_project = Abbau Aufbau
source_building_id = unknown
```

### Geometry Generator Output

```text
top/bottom face candidates
principal axes
orientation candidate
```

### System Output

```text
human-readable name
source level = 1OG
original function = floor_slab_candidate
QR code
internal GUID
external reference
```

### Proof

```text
source_level =
parse "1OG" from DE_1OG_001

original_function =
typology default for slab = floor_slab_candidate

orientation =
largest two parallel faces = top/bottom candidates

qr_code =
"QR-" + "DE_1OG_001"
```

### Must Remain Unknown

```text
real RFID
physical marking
true donor-building ID
true original orientation if no metadata confirms it
```

---

## 3. Pool Availability

### Visible Details

```text
Availability state: available
Storage state: located
Reservation state: not reserved
Used count: 0
Stock total: 1
Stock available: 1
Blocked reason: none
Reserved design: none
Linked placed pieces: []
```

### Minimum Input

```text
component_id = DE_1OG_001
stock rule = individual reclaimed component
design graph access
storage location = example-storage-yard-01
```

### Geometry Generator Output

```text
none
```

### System Output

```text
used count = 0
stock available = 1
availability state = available
storage state = located
linked piece IDs = []
```

### Proof

```text
stock_total =
1

used_count =
0 active pieces

reserved_count =
0

stock_available =
1 - 0 - 0 =
1

availability =
available
```

### Must Remain Unknown

```text
physical presence if storage system is not verified
manual off-system reservation
damage after catalogue creation
```

---

## 4. Classification

### Visible Details

```text
Primary element kind: slab
Secondary classifications:
- horizontal spanning element
- reclaimed reinforced-concrete component
- large-format reuse element

Material family: reinforced concrete
Structural family: horizontal spanning
Allowed design roles:
- floor slab
- roof slab if engineered
- horizontal diaphragm if engineered

Disallowed design roles:
- wall
- column
- beam

Semantic tags:
- reclaimed
- reinforced concrete
- slab
- Abbau/Aufbau
- ReCreate-compatible component typology

Reuse category: reusable_with_verification
Risk category: medium, because rebar and strength evidence are not linked in this example
```

### Minimum Input

```text
component_typology = slab
material_kind = reinforced_concrete
base_geometry_reference
```

### Geometry Generator Output

```text
shape class = thin plate
principal dimensions
top/bottom faces
edge candidates
```

### System Output

```text
primary kind = slab
structural family = horizontal spanning
allowed roles
disallowed roles
reuse category
risk category
```

### Proof

```text
slab typology + thin-plate geometry =
horizontal spanning family

allowed_roles =
typology role library for slab

risk_category =
missing rebar scan + missing concrete test + structural use intended
```

### Must Remain Unknown

```text
approved use as diaphragm
approved roof use
actual structural capacity
```

---

## 5. Geometry Overview

### Visible Details

```text
Unit system: mm
Length: 4500 mm
Width: 2300 mm
Height / thickness: 180 mm
Bounding box: 4500 × 2300 × 180 mm
Gross volume: 1.863 m³
Net volume: 1.863 m³
Mass: ca. 4.1 t
Density: implied 2201 kg/m³ from catalogue mass
Center of gravity: x 2250 mm, y 1150 mm, z 90 mm
Original top face: candidate
Original bottom face: candidate
Local X axis: long direction
Local Y axis: short direction
Local Z axis: thickness direction
Geometry tolerance: project default
Placement tolerance: project default
Joint tolerance: project default
```

### Minimum Input

```text
base_geometry_reference
component_typology = slab
material_kind = reinforced_concrete
```

### Geometry Generator Output

```text
unit system
principal axes
bounding box
length = 4500 mm
width = 2300 mm
thickness = 180 mm
gross volume = 1.863 m³
net volume = 1.863 m³
center of gravity
top/bottom candidates
local axes
```

### System Output

```text
catalogue mass = ca. 4.1 t
implied density = 2201 kg/m³
tolerances = project defaults
```

### Proof

```text
volume =
4.5 × 2.3 × 0.18 =
1.863 m³

center_of_gravity =
4500/2, 2300/2, 180/2 =
2250, 1150, 90 mm

implied_density =
4100 / 1.863 =
2201 kg/m³
```

### Must Remain Unknown

```text
measured density
internal voids not visible in geometry
true original top/bottom without metadata
actual fabrication tolerance
```

---

## 6. Geometry Representations

### Visible Details

```text
Physical geometry: generated rectangular slab body
Structural geometry: generated slab support and bearing candidates
Energy / envelope geometry: generated face and edge candidates
Semantic geometry: generated top/bottom/visible face candidates
Connector-zone geometry: generated slab-edge-bearing and service ports
Logistics geometry: generated transport envelope and storage orientation geometry
Catalogue sketch: handbook table sketch / generated sketch
Photos: none linked
Scan data: none linked
BIM model: not imported in this example
```

### Minimum Input

```text
base_geometry_reference
component_typology = slab
material_kind = reinforced_concrete
```

### Geometry Generator Output

```text
physical representation
structural geometry representation
energy geometry representation
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
source / confidence display
missing representation flags
```

### Proof

```text
physical representation =
normalized 4500 × 2300 × 180 mm slab

structural representation =
bearing edge candidates + span candidates

energy representation =
top/bottom/edge faces for possible envelope use

semantic representation =
floor-side / ceiling-side candidates

connector-zone representation =
slab-edge-bearing ports

logistics representation =
transport envelope = bounding box
```

### Must Remain Unknown

```text
true semantic context without active design
structural proof
energy compliance
```

---

## 7. Physical Geometry

### Visible Details

```text
Shape type: thin rectangular slab
Exact dimensions: 4500 × 2300 × 180 mm
Surface geometry: 6 main faces
Edge geometry: 4 long/short perimeter edges + vertical edge zones
Opening geometry: none detected / none recorded
Cut-outs: none recorded
Chamfers: none recorded
Irregularities: none from catalogue
Surface damage location: unknown
Edge damage location: unknown
Physical tolerance: project default
```

### Minimum Input

```text
base_geometry_reference
component_typology = slab
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
surface / edge condition status = unknown
damage candidate labels = none because no damage evidence linked
```

### Proof

```text
shape_type =
slab typology + thickness much smaller than length and width

openings =
none recorded in catalogue

faces =
top, bottom, four sides

edges =
perimeter edges and corner lines
```

### Must Remain Unknown

```text
cracks
spalling
surface contamination
edge damage
as-built deviations
```

---

## 8. Structural Geometry

### Visible Details

```text
Structural role: slab / horizontal spanning candidate
Span direction: unknown, generated candidates only
Main reinforcement direction: unknown
Secondary reinforcement direction: unknown
Support edges: long-edge and short-edge candidates
Bearing zones: generated along slab perimeter
Point-support zones: only engineering-required candidate
Line-support zones: generated along slab edges
Load direction: vertical gravity candidate
Preferred support condition: line bearing on wall or beam
Forbidden support condition: point support without engineering proof
Minimum bearing length: project default 80 mm
Structural thickness: 180 mm
Structural openings: none recorded
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
original_function = floor_slab_candidate
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
reinforcement direction status = unknown
```

### Proof

```text
slab typology =
horizontal spanning element

bearing zones =
perimeter edges buffered by project bearing rule

structural thickness =
180 mm

structural openings =
none recorded

minimum bearing length =
project default, not confirmed by source
```

### Must Remain Unknown

```text
actual span direction
actual reinforcement layout
load capacity
moment capacity
shear capacity
punching resistance
```

---

## 9. Energy / Envelope Geometry

### Visible Details

```text
Envelope relevance: requires project context
Exterior faces: candidate only
Interior faces: candidate only
Ground-contact faces: not assumed
Roof faces: possible if used as roof
Thermal boundary faces: candidate if assigned to envelope
Insulation-relevant faces: generated if envelope-relevant
Thermal bridge risk zones: slab edges + connector zones
Moisture risk zones: roof/exterior candidates only
U-value-relevant surfaces: top/bottom/edge faces if envelope-relevant
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
material_kind = reinforced_concrete
intended_exposure_context = unknown
```

### Geometry Generator Output

```text
face candidates
thermal boundary candidate faces
edge zones
connector-crossing candidates
moisture-risk geometry candidates
U-value-relevant thickness = 180 mm
```

### System Output

```text
envelope relevance = requires_project_context
rough U-value = 4.03 W/m²K if treated as concrete-only layer
insulation requirement flag = required if envelope target is 0.24 W/m²K
thermal bridge warnings = possible at slab edges / steel connectors
```

### Proof

```text
R_concrete =
0.18 / 2.3 =
0.078 m²K/W

U_rough =
1 / (0.13 + 0.078 + 0.04) =
4.03 W/m²K
```

### Must Remain Unknown

```text
final U-value
real envelope role
thermal bridge Psi-value
moisture proof
complete assembly performance
```

---

## 10. Semantic / Architectural Geometry

### Visible Details

```text
Inside / outside side: unknown
Room-facing side: candidate
Facade-facing side: candidate only if used in envelope
Visible surface side: top/bottom candidate
Hidden surface side: bearing/contact faces candidate
Original use side: floor-side and ceiling-side candidates
Potential new use: floor slab / roof slab if engineered
Spatial role: horizontal room-defining element
Room boundary role: floor or ceiling plane candidate
Facade rhythm relevance: low unless exposed at edge/facade
Visible reuse potential: unknown because no photos linked
Surface expression value: unknown
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
source_context = Abbau/Aufbau
target_use_context = unknown
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
visible reuse potential
surface expression value
```

### Proof

```text
slab top =
floor-side candidate

slab bottom =
ceiling-side candidate

visible_faces =
top/bottom surfaces unless covered by build-up

spatial_role =
horizontal boundary candidate
```

### Must Remain Unknown

```text
actual architectural intention
inside/outside without placement
visual quality without photos or scan
```

---

## 11. Openings + Penetrations

### Visible Details

```text
Opening ID: none
Opening type: none
Opening position: not applicable
Opening size: not applicable
Opening depth: not applicable
Opening purpose: not applicable
Original service use: unknown / none recorded
Edge distance: not applicable
Relation to reinforcement: unknown
Reusable for services: no existing opening recorded
Blocked opening: none recorded
Unknown opening: none
```

### Minimum Input

```text
base_geometry_reference
component_typology = slab
```

### Geometry Generator Output

```text
detected openings = []
opening geometry = none
penetration candidates = generated service-zone candidates only
```

### System Output

```text
opening ID = none
service reuse candidate = false for existing opening
new core drilling = requires reinforcement scan
```

### Proof

```text
Abbau/Aufbau catalogue opening field =
"-"

therefore:
existing_openings = []
```

### Must Remain Unknown

```text
hidden service sleeves not represented in geometry
new penetration approval
hidden rebar conflicts
```

---

## 12. Surface + Edge Condition

### Visible Details

```text
Top face condition: unknown
Bottom face condition: unknown
Side face condition: unknown
Edge condition: unknown
Spalling: unknown
Cracks: unknown
Exposed reinforcement: unknown
Surface contamination: unknown
Repair marks: unknown
Visual quality: unknown
Visible reuse quality: unknown
```

### Minimum Input

```text
base_geometry_reference
photos_or_scan = none in example
```

### Geometry Generator Output

```text
face map
edge map
surface zones
edge zones
```

### System Output

```text
surface condition = unknown
edge condition = unknown
visual quality = unknown
visible reuse quality = unknown
```

### Proof

```text
No damage photos, scan, or inspection report is linked.
The system cannot classify condition from catalogue dimensions alone.
```

### Must Remain Unknown

```text
subsurface damage
cracks
spalling
chloride contamination
surface contamination
```

---

## 13. Damage Records

### Visible Details

```text
Damage ID: none recorded
Damage type: unknown
Damage location: not applicable
Severity: unknown
Affected face / edge: not applicable
Size: not applicable
Photo reference: none
Repair status: unknown
Rule relevance: none until damage is recorded
Notes: no damage evidence linked
```

### Minimum Input

```text
base_geometry_reference
damage_photo_or_scan = none
```

### Geometry Generator Output

```text
damage-location candidates = none
affected face / edge candidates = generated but no damage mapped
```

### System Output

```text
damage records = []
damage evidence status = missing
```

### Proof

```text
No damage record is present in the catalogue example.
No photo or scan is linked.
```

### Must Remain Unknown

```text
actual damage state
repair status
structural severity
```

---

## 14. Concrete Evidence

### Visible Details

```text
Concrete strength: unknown
Test method: none linked
Test date: unknown
Test document: none
Compressive strength: unknown
Tensile strength: unknown
E-modulus: unknown / default-estimable only if project permits
Density: implied from catalogue mass = 2201 kg/m³; default comparison = 2400 kg/m³
Carbonation depth: unknown
Chloride content: unknown
Pollutant content: unknown
Moisture status: unknown
Evidence confidence: low / partial
```

### Minimum Input

```text
material_kind = reinforced_concrete
optional concrete evidence documents = none
```

### Geometry Generator Output

```text
none
```

### System Output

```text
density default
implied density from catalogue mass
concrete evidence status = missing
missing concrete evidence flags
confidence level = low
```

### Proof

```text
implied_density =
4100 / 1.863 =
2201 kg/m³

compressive strength =
unknown because no test report is linked
```

### Must Remain Unknown

```text
real concrete strength
chloride content
pollutants
carbonation depth
moisture condition
```

---

## 15. Reinforcement Evidence

### Visible Details

```text
Reinforcement position status: unknown
Main reinforcement direction: unknown / inferred candidate only
Secondary reinforcement direction: unknown
Cover top: unknown
Cover bottom: unknown
Cover sides: unknown
Rebar scan reference: none
Rebar condition: unknown
Corrosion risk: unknown
No-drill zones: generated candidates only
Drill-approved zones: none approved
Anchor-approved zones: none approved
Unknown reinforcement zones: all structural drilling zones
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
rebar scan = none
reinforcement drawing = none
```

### Geometry Generator Output

```text
candidate support zones
candidate connector zones
candidate no-drill zones near edges/supports
```

### System Output

```text
reinforcement position status = unknown
all drilling zones = unknown / blocked
approved anchor zones = none
corrosion risk = unknown
```

### Proof

```text
No rebar map exists.
Therefore:
drill_approved_zones = []
anchor_approved_zones = []
unknown_reinforcement_zones = all connector zones requiring drilling
```

### Must Remain Unknown

```text
true rebar location
safe anchor zones
cover depth
internal corrosion
```

---

## 16. Durability + Restnutzungsdauer

### Visible Details

```text
Durability status: engineering_required
Carbonation risk: unknown
Chloride risk: unknown
Corrosion risk: unknown
Freeze-thaw risk: context-dependent
Moisture exposure risk: depends on storage / future use
Estimated remaining service life: unknown
Repair requirement: unknown
Protection requirement: yes if stored outdoors
```

### Minimum Input

```text
material_kind = reinforced_concrete
storage / exposure context = example outdoor storage
condition status = unknown
```

### Geometry Generator Output

```text
exposed face candidates
moisture-risk geometry candidates
damage-zone geometry = none mapped
```

### System Output

```text
durability status = engineering_required
moisture risk = possible if outdoor storage
protection required = true if outdoor storage
remaining service life = unknown
```

### Proof

```text
carbonation risk needs carbonation depth + cover.
chloride risk needs chloride test.
remaining service life needs durability assessment.
```

### Must Remain Unknown

```text
reliable remaining service life
internal corrosion
chloride-induced corrosion risk
repair requirement
```

---

## 17. Structural Data

### Visible Details

```text
Structural role: slab / horizontal spanning candidate
Load-bearing status: likely structural, proof required
Self weight: 40.22 kN total; 3.89 kN/m²
Allowed support types: wall top, beam top, column head if engineered
Allowed bearing zones: generated slab edge zones
Allowed span direction: unknown
Maximum reuse span: 4500 mm or 2300 mm candidate, not verified
Known load capacity: unknown
Capacity evidence status: missing
Required proof status: structural proof required
Original structural function: floor slab candidate
```

### Minimum Input

```text
component_typology = slab
material_kind = reinforced_concrete
base_geometry_reference
original_function = floor_slab_candidate
```

### Geometry Generator Output

```text
structural geometry
bearing zones
support zones
span candidates
plan area = 10.35 m²
volume = 1.863 m³
```

### System Output

```text
structural role
load-bearing status candidate
self weight
allowed support types
allowed bearing zones
capacity evidence status
proof requirement status
```

### Proof

```text
self_weight =
4100 × 9.81 / 1000 =
40.22 kN

self_weight_per_m2 =
40.22 / 10.35 =
3.89 kN/m²
```

### Must Remain Unknown

```text
allowable live load
bending capacity
shear capacity
punching resistance
fire-reduced capacity
```

---

## 18. Connector / Interface Data

### Visible Details

```text
Connector ID:
- conn-DE_1OG_001-long-edge-A
- conn-DE_1OG_001-long-edge-B
- conn-DE_1OG_001-short-edge-A
- conn-DE_1OG_001-short-edge-B
- conn-DE_1OG_001-top-service-zone
- conn-DE_1OG_001-envelope-face

Connector type:
- slab-edge-bearing
- slab-top-service-zone
- thermal-envelope-interface

Compatible ports:
- wall-top-bearing
- beam-top-bearing
- column-head-bearing if engineered
- service-penetration
- insulation-layer / facade-zone if envelope

Mandatory or optional:
- bearing ports: mandatory if slab is used structurally
- service / envelope ports: optional until context requires them

Allowed connection role:
- vertical load transfer
- service routing
- thermal envelope interface

Allowed connector systems for wall+slab:
- post-installed reinforcement + grout / injection mortar
- screw anchor + flat steel holder

Minimum bearing length: project default 80 mm
Maximum gap: project default 40 mm
Drilling permission: blocked until reinforcement scan exists
Fire check required: yes if steel connector exposed or fire-relevant
Structural check required: yes
Thermal check required: yes if envelope
Service check required: yes if penetration
Reversibility preference: dry / bolted preferred if target requires reversibility
```

### Minimum Input

```text
component_typology = slab
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
connector IDs
connector names
compatible ports
mandatory / optional status
allowed connector systems
minimum bearing length
maximum gap
drilling permission
required checks
reversibility preference
```

### Proof

```text
slab edges generate slab-edge-bearing ports.

wall+slab connector options are read from the Abbau/Aufbau connector family:
- post-installed reinforcement + grout
- screw anchor + flat steel holder

drilling permission =
blocked because reinforcement evidence is unknown.
```

### Must Remain Unknown

```text
connector capacity
safe anchor positions
actual reversibility of a selected custom connector
```

---

## 19. Bohrzonen / No-Drill Zones

### Visible Details

```text
Approved drilling zones: none approved
Forbidden drilling zones: generated edge/bearing/no-drill candidates
Unknown drilling zones: all connector zones requiring drilling
Approved anchor zones: none
Forbidden anchor zones: bearing edges until rebar scan exists
Minimum edge distance: project / connector default
Minimum spacing: project / connector default
Concrete cover requirement: unknown
Rebar conflict status: unknown
Scan confidence: none
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
project drilling defaults
rebar scan = none
```

### Geometry Generator Output

```text
connector zones
edge buffers
opening buffers
bearing zones
```

### System Output

```text
forbidden zones
unknown zones
approved drilling zones = []
approved anchor zones = []
edge distance rules
spacing rules
rebar conflict status = unknown
scan confidence = none
```

### Proof

```text
Because no reinforcement scan exists:
approved_drilling_zones = []
unknown_zones = all connector zones requiring drilling
```

### Must Remain Unknown

```text
approved drilling zones
anchor pull-out capacity
hidden conflicts
```

---

## 20. Fire Data

### Visible Details

```text
Material fire class: non-combustible material assumption for reinforced concrete
Known fire resistance: unknown
Evidence status: project-context-required
Fire-relevant surfaces: generated candidate faces only
Connector fire warning conditions: exposed steel connector in fire-relevant context
Exposed steel warning: applies if steel anchor / plate / beam is used
Fire cover requirement if connected: required if connector detail is fire-relevant
```

### Minimum Input

```text
material_kind = reinforced_concrete
component_typology = slab
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
The slab material can be treated as non-combustible at material level.
The final fire resistance of the assembly depends on connection, support, exposure, and building context.
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
Thermal conductivity: project default 2.3 W/mK unless tested
Density: implied 2201 kg/m³ or default 2400 kg/m³
Specific heat capacity: project default / unknown
U-value data: rough concrete-only U = 4.03 W/m²K
Envelope relevance: requires project context
Insulation requirement if envelope: yes if target is 0.24 W/m²K
Thermal bridge zones: slab edges + connector zones
Moisture risk: possible if roof / exterior / ground / outdoor storage
Ground-contact suitability: requires verification
Roof suitability: requires waterproofing + thermal + structural proof
Acoustic relevance: mass-relevant
```

### Minimum Input

```text
material_kind = reinforced_concrete
component_typology = slab
base_geometry_reference
exposure_context = unknown
project thermal defaults
```

### Geometry Generator Output

```text
thickness = 0.18 m
thermal boundary candidate faces
thermal bridge geometry candidates
moisture-risk geometry candidates
surface areas
```

### System Output

```text
thermal conductivity estimate
density
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
0.18 / 2.3 =
0.078 m²K/W

U_rough =
1 / (0.13 + 0.078 + 0.04) =
4.03 W/m²K
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
Mass relevance: yes
Airborne sound data: unknown
Impact sound data: unknown
Acoustic evidence status: missing
Recommended acoustic use: potential floor/ceiling mass layer
Acoustic warning: required if target use has high acoustic demand
```

### Minimum Input

```text
component_typology = slab
material_kind = reinforced_concrete
base_geometry_reference
```

### Geometry Generator Output

```text
surface area
plan area = 10.35 m²
volume = 1.863 m³
thickness = 180 mm
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
4100 kg / 10.35 m² =
396 kg/m²

High mass means acoustic relevance is likely,
but actual acoustic performance is not known.
```

### Must Remain Unknown

```text
airborne sound rating
impact sound performance
flanking transmission
```

---

## 23. TGA / Services Data

### Visible Details

```text
Existing service openings: none recorded
Approved service zones: none approved
Blocked service zones: bearing zones and unknown-rebar drilling zones
Possible cable penetrations: only after scan / approval
Possible pipe penetrations: only after scan / approval
Core drilling allowed: no
Core drilling blocked: yes, until reinforcement scan exists
Rebar scan required for services: yes
```

### Minimum Input

```text
base_geometry_reference
component_typology = slab
service context = none
```

### Geometry Generator Output

```text
opening geometry = none
penetration candidates
service-zone candidates
connector/service port geometry
edge distances
```

### System Output

```text
existing service openings = []
approved service zone candidates = none without scan
blocked service zones
core drilling status
rebar scan requirement
```

### Proof

```text
Catalogue opening field = none.
No rebar scan exists.
Therefore new core drilling is blocked until reinforcement evidence is added.
```

### Must Remain Unknown

```text
actual TGA route fit
safe drilling
fire/acoustic sealing details
```

---

## 24. Logistics Data

### Visible Details

```text
Current storage location: example-storage-yard-01
Storage position: A-03-02
Recommended storage orientation: lying flat
Forbidden storage orientation: standing on edge without engineering support
Weather protection required: yes if outdoor
Separator required: yes if stacked
Mass: ca. 4.1 t
Lifting point status: unknown / engineering-required
Lifting points: none documented
Transport mode: 40t truck assumed
Transport readiness: partial
Load securing required: yes
Damage protection required: yes
Temporary bracing requirement: not for flat storage; check during installation
Assembly access zones: slab edges and top face
Installation notes: support components must be installed before slab
```

### Minimum Input

```text
component_typology = slab
base_geometry_reference
material_kind = reinforced_concrete
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
installation notes
```

### Proof

```text
Slab typology =
lying-flat storage recommended.

Mass =
catalogue 4.1 t.

Transport envelope =
4500 × 2300 × 180 mm.
```

### Must Remain Unknown

```text
safe lifting design
actual crane radius
site access
lifting anchors
```

---

## 25. Transport Data

### Visible Details

```text
Transport mode: 40t truck assumed
Transport distance: example 30 km
Transport factor: 0.05 kgCO2e/tkm
Transport emissions status: calculated precheck
Maximum transport size: normal check required
Special transport required: probably no based on dimensions, but route-specific
Protection requirement: yes
Load securing note: required
```

### Minimum Input

```text
storage location
target site location
project transport defaults
```

### Geometry Generator Output

```text
transport dimensions = 4500 × 2300 × 180 mm
transport envelope
```

### System Output

```text
transport mass = 4.1 t
transport distance = 30 km example
transport mode = 40t truck assumed
transport GWP = 6.15 kgCO2e
special transport flag = context-dependent
protection requirement
load securing note
```

### Proof

```text
transport_gwp =
4.1 × 30 × 0.05 =
6.15 kgCO2e
```

### Must Remain Unknown

```text
actual route restrictions
transport permit requirements
exact emissions without final route and vehicle
```

---

## 26. LCA / Ökobilanz Data

### Visible Details

```text
Material: reinforced concrete
Mass: ca. 4.1 t
Reused mass: ca. 4.1 t
A1-A3 reuse assumption: 0 kgCO2e/t if project applies Abbau/Aufbau reuse assumption
Transport factor: 0.05 kgCO2e/tkm
Transport distance: 30 km example
New equivalent reference: precast concrete slab reference
New equivalent GWP: 171.7 kgCO2e/t
Avoided GWP potential: 703.97 kgCO2e
EPD dataset: missing
Ökobaudat dataset: reference value only
Generic dataset status: required for full LCA
LCA completeness: partial
Environmental indicators: GWP precheck only
```

### Minimum Input

```text
material_kind = reinforced_concrete
component_typology = slab
base_geometry_reference
project_lca_defaults
storage and target location if transport included
```

### Geometry Generator Output

```text
volume = 1.863 m³
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
4.1 t

transport_gwp =
4.1 × 30 × 0.05 =
6.15 kgCO2e

avoided_gwp_potential =
4.1 × 171.7 =
703.97 kgCO2e
```

### Must Remain Unknown

```text
full LCA indicators without datasets
connector-specific impact
adapter impact
module B/C/D values
non-GWP indicators
```

---

## 27. Documentation

### Visible Details

```text
Catalogue sheet: Abbau/Aufbau catalogue table
Sketch: handbook sketch / generated preview
Photos: none linked
Laser scan: none linked
BIM model: none linked
Concrete test report: none linked
Rebar scan: none linked
Damage report: none linked
Transport document: none linked
Storage document: example context only
LCA document: handbook reference values only
EPD / Ökobaudat reference: reference value included
Approval document: none linked
Notes: ReCreate quality logic recommends documentation before reuse approval
```

### Minimum Input

```text
component_id = DE_1OG_001
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
DE_1OG_001 + document_kind

available:
catalogue table
generated geometry

missing:
concrete test
rebar scan
damage report
fire document
full LCA dataset
```

### Must Remain Unknown

```text
document validity beyond cited source
approval status
author/date for generated project files
```

---

## 28. Evidence Completeness

### Visible Details

```text
Identity complete: partial / enough for example
Geometry complete: complete for rectangular geometry
Mass complete: catalogue mass available
Openings complete: complete for catalogue-level none
Concrete evidence complete: missing
Rebar evidence complete: missing
Damage evidence complete: missing
Connector zones complete: generated, not evidence-confirmed
Logistics complete: partial
LCA complete: partial
Fire data complete: requires project context
Building physics complete: requires project context
Services data complete: incomplete because no rebar scan
```

### Minimum Input

```text
component_id = DE_1OG_001
component_typology = slab
material_kind = reinforced_concrete
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
geometry_complete =
dimensions + generated geometry exist

mass_complete =
catalogue mass exists

concrete_complete =
false because no test report linked

reinforcement_complete =
false because no scan/drawing linked

connector_zones_complete =
generated only, evidence status partial

lca_complete =
partial because GWP precheck exists, full datasets missing
```

### Must Remain Unknown

```text
full structural completeness
full fire completeness
full energy completeness
approval readiness
```

---

## 29. Pool-Level Warnings

### Visible Details

```text
Missing rebar scan
Missing concrete strength test
Missing chloride / carbonation evidence
Unknown lifting points
Unknown actual transport route
Missing full LCA dataset
Missing fire rating
Thermal conductivity is project default, not tested
Do not drill without reinforcement verification
Do not approve structural capacity without proof
```

### Minimum Input

```text
generated geometry
system completeness statuses
project required evidence list
```

### Geometry Generator Output

```text
bearing zones
connector zones
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
if reinforcement evidence missing:
warn Missing rebar scan

if concrete strength unknown:
warn Missing concrete strength test

if drilling zones unknown:
warn Do not drill without verification

if capacity unknown:
warn Structural proof required

if LCA dataset missing:
warn Full LCA dataset missing
```

### Must Remain Unknown

```text
hidden risk severity
actual safety of warned actions
regulatory acceptability
```

---

## 30. Rule-Checker Readiness

### Visible Details

```text
Ready rules:
- identity check
- geometry/interface check
- pair classification
- bearing-zone precheck
- mass/logistics precheck
- LCA precheck

Rules needing more evidence:
- anchor/drilling check
- full structural capacity check
- fire resistance check
- full thermal-envelope check
- full LCA indicators
- approval-readiness check

Blocked actions:
- drilling without rebar scan
- approving anchor zones
- approving final structural capacity
- claiming final fire rating
- claiming final U-value

Default status if used:
warning / engineering_required
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
geometry generated =
geometry/interface check ready

ports generated =
port compatibility check ready

mass available =
logistics and LCA precheck ready

rebar missing =
anchor/drilling check blocked

capacity missing =
structural proof required
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
data and generated representations of DE_1OG_001

Connection Passport =
result of connecting DE_1OG_001 to another component, e.g. wall W-003

Rule Checker Panel =
active validation state of the current design

Design Dashboard =
whole-design scores and preference ranking
```

---

# 8. Final Summary

## 8.1 User Provides for the Example

```text
component_id = DE_1OG_001
component_typology = slab
material_kind = reinforced_concrete
base geometry reference or catalogue dimensions
source context = Abbau/Aufbau
storage context = example
project defaults
optional evidence references
```

## 8.2 Geometry Generators Produce for DE_1OG_001

```text
normalized slab geometry
physical geometry
structural slab geometry
energy / envelope geometry
semantic geometry
connector-zone geometry
slab-edge-bearing ports
service-zone candidates
opening map
penetration candidates
logistics geometry
volume and geometric quantities
```

## 8.3 System Modules Produce for DE_1OG_001

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

## 8.4 Evidence Still Required

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

---

# 10. References Used for This Example

## Abbau/Aufbau

```text
Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden.
Used for:
- Bauteilkatalog fields
- example component DE_1OG_001
- dimensions, volume, mass
- tracking / tracing logic
- transport factor
- new concrete reference value
- connector families
- logistics and storage logic
```

## ReCreate

```text
ReCreate — Reusing precast concrete for a circular economy.
Used as broader framework for:
- component and connector typology thinking
- BIM / traceability logic
- quality management logic
- evidence and documentation logic
- reuse-readiness logic
```
