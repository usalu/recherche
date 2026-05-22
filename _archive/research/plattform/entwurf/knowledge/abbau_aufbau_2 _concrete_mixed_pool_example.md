# Geometry-Generator-Based Bauteilpass System  
## Concrete Abbau/Aufbau Example: Mixed Component Pool

**Purpose**  
This document uses the same architecture as the corrected system document, but applies it to a concrete Abbau/Aufbau-style mixed component pool.

**Corrected architecture**  
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

## 1.1 Example Scenario

The example starts from an already existing **Abbau/Aufbau Bauteilpool**.

The system does **not** model Rückbau or Zuschnitt.  
It assumes that the components already exist as individual elements in the pool.

The mixed example pool contains:

```text
P-001  Deckenplatte / slab
W-001  Wandplatte / wall panel
C-001  Stütze / column
B-001  Träger / support beam or adapter beam
```

## 1.2 Source Logic

The Abbau/Aufbau handbook defines the Bauteilkatalog as the basis for logistics, storage, and reinstallation. It lists the required catalogue fields as:

```text
ID
Skizze
Maße
Öffnungsmaße
Volumen
Masse
optional Beton- und Bewehrungsuntersuchungen
```

The handbook gives the concrete catalogue example:

```text
ID: DE_1OG_001
Maße: L 4500 / B 2300 / H 180 mm
Öffnungen: -
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

This example is used here as **P-001**, the slab component.

## 1.3 Example Component Pool

```yaml
component_pool:
  kit_id: kit-abbau-aufbau-example-pool-001
  kit_name: Abbau Aufbau Beispiel-Bauteilpool

  components:
    - id: P-001
      source_id: DE_1OG_001
      typology: slab
      material_kind: reinforced_concrete
      dimensions_mm:
        length: 4500
        width: 2300
        thickness: 180
      openings: none
      volume_m3: 1.863
      mass_t: 4.1
      source_status: exact handbook catalogue example

    - id: W-001
      source_id: AA-WAND-BSP-001
      typology: wall_panel
      material_kind: reinforced_concrete
      dimensions_mm:
        length: 3000
        height: 3000
        thickness: 100
      volume_m3: 0.9
      mass_t_estimated: 2.16
      source_status: derived from Abbau/Aufbau reused wall example in tender text

    - id: C-001
      source_id: AA-STUETZE-BSP-001
      typology: column
      material_kind: reinforced_concrete
      dimensions_mm:
        width: 350
        depth: 350
        height: 3500
      volume_m3: 0.42875
      mass_t_estimated: 1.03
      source_status: derived from Abbau/Aufbau reused column example in tender text

    - id: B-001
      source_id: AA-TRAEGER-LOGIK-001
      typology: beam
      material_kind: steel_or_reinforced_concrete_adapter
      dimensions_mm:
        length: 4500
        width: 300
        height: 300
      volume_m3_if_concrete: 0.405
      mass_t_if_concrete_estimated: 0.972
      source_status: system example for beam/support typology; Abbau/Aufbau includes steel beam support logic for column-slab connection
```

## 1.4 Main Pipeline

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

## 1.5 What the User Provides

For each component the user or import process provides only:

```yaml
minimum_input:
  component_id: P-001
  component_typology: slab
  material_kind: reinforced_concrete
  base_geometry_reference: geometry/P-001/base.glb

  source_context:
    source_project: Abbau Aufbau
    source_reference: DE_1OG_001
    original_level: 1OG
    original_function: floor_slab

  pool_context:
    current_storage_location: storage-yard-01
    storage_position: A-03-02

  project_defaults:
    density_reinforced_concrete_kg_m3: 2400
    lambda_reinforced_concrete_W_mK: 2.3
    transport_factor_kgco2e_per_tkm: 0.05
    new_precast_concrete_reference_kgco2e_per_t: 171.7
```

## 1.6 What Geometry Generators Produce

For this mixed pool:

```text
P-001 slab:
  slab faces, slab edges, bearing zones, slab-edge ports, envelope candidates, service opening candidates

W-001 wall panel:
  broad faces, top/bottom bearing edges, side joint edges, wall-top ports, wall-bottom ports

C-001 column:
  column axis, base face, head face, column-head port, column-base port

B-001 beam:
  beam axis, beam end zones, beam-top bearing surface, beam-end ports, beam-top ports
```

## 1.7 What System Modules Produce

Using the generated geometry plus Abbau/Aufbau project logic:

```text
Semio binding
identity and traceability
classification
pool availability
material evidence status
structural data status
fire flags
building physics prechecks
services/TGA status
logistics and transport status
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

In this concrete example, each of the four pool components receives a Bauteilpass:

```text
P-001 Bauteilpass = slab passport
W-001 Bauteilpass = wall passport
C-001 Bauteilpass = column passport
B-001 Bauteilpass = beam / support passport
```

Each Bauteilpass combines:

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

For this example:

```text
slab generator runs on P-001
wall-panel generator runs on W-001
column generator runs on C-001
beam generator runs on B-001
```

The generator outputs geometry only:

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

It does not decide:

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

Example:

```text
Geometry Generator:
P-001 has a slab-edge-bearing port.

System Module:
This port can connect to W-001 wall-top-bearing or B-001 beam-top-bearing,
but drilling is blocked unless reinforcement evidence exists.
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

---

## 4.1 Slab Typology — Example P-001

```yaml
typology:
  id: slab
  example_component: P-001
  source_id: DE_1OG_001

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

Concrete output for P-001:

```yaml
P-001_generated_geometry:
  dimensions_mm:
    length: 4500
    width: 2300
    thickness: 180
  top_face_area_m2: 10.35
  volume_m3: 1.863
  mass_t_system: 4.47
  mass_t_catalogue: 4.1
  mass_status: catalogue_value_preferred
  generated_ports:
    - P-001.port.long_edge_left.slab_edge_bearing
    - P-001.port.long_edge_right.slab_edge_bearing
    - P-001.port.top.service_zone
    - P-001.port.top.envelope_candidate
```

Mass explanation:

```text
Calculated mass with default density:
1.863 m³ × 2400 kg/m³ = 4471.2 kg = 4.47 t

Catalogue mass:
ca. 4.1 t

System decision:
Use catalogue mass where available; keep calculated mass as check value.
```

---

## 4.2 Wall Panel Typology — Example W-001

```yaml
typology:
  id: wall_panel
  example_component: W-001

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

Concrete output for W-001:

```yaml
W-001_generated_geometry:
  dimensions_mm:
    length: 3000
    height: 3000
    thickness: 100
  volume_m3: 0.9
  mass_t_estimated: 2.16
  generated_ports:
    - W-001.port.top.wall_top_bearing
    - W-001.port.bottom.wall_bottom_bearing
    - W-001.port.left.wall_side_joint
    - W-001.port.right.wall_side_joint
    - W-001.port.face.wall_face_connector
```

Mass proof:

```text
0.9 m³ × 2400 kg/m³ = 2160 kg = 2.16 t
```

---

## 4.3 Column Typology — Example C-001

```yaml
typology:
  id: column
  example_component: C-001

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

Concrete output for C-001:

```yaml
C-001_generated_geometry:
  dimensions_mm:
    width: 350
    depth: 350
    height: 3500
  volume_m3: 0.42875
  mass_t_estimated: 1.03
  generated_ports:
    - C-001.port.base.column_base_bearing
    - C-001.port.head.column_head_bearing
    - C-001.port.side.column_side_stability_connector
```

Mass proof:

```text
0.35 m × 0.35 m × 3.5 m = 0.42875 m³
0.42875 m³ × 2400 kg/m³ = 1029 kg = 1.03 t
```

---

## 4.4 Beam Typology — Example B-001

```yaml
typology:
  id: beam
  example_component: B-001

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

Concrete output for B-001:

```yaml
B-001_generated_geometry:
  dimensions_mm:
    length: 4500
    width: 300
    height: 300
  volume_m3_if_concrete: 0.405
  mass_t_if_concrete_estimated: 0.972
  generated_ports:
    - B-001.port.left.beam_end_bearing
    - B-001.port.right.beam_end_bearing
    - B-001.port.top.beam_top_bearing
    - B-001.port.side.beam_side_connector
```

Mass proof if reinforced concrete:

```text
4.5 m × 0.3 m × 0.3 m = 0.405 m³
0.405 m³ × 2400 kg/m³ = 972 kg = 0.972 t
```

Important status:

```text
B-001 is included as a beam/support typology example.
If the beam is steel, mass and LCA must use steel profile data, not concrete density.
If the beam is reclaimed reinforced concrete, the above mass precheck applies.
```

---

# 5. Shared Geometry Calculations

## 5.1 Oriented Bounding Box

```text
OBB = oriented_bounding_box(base_geometry)
```

Example:

```text
P-001 OBB = 4500 × 2300 × 180 mm
W-001 OBB = 3000 × 3000 × 100 mm
C-001 OBB = 350 × 350 × 3500 mm
B-001 OBB = 4500 × 300 × 300 mm
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

Example:

```text
P-001 = 4.5 × 2.3 × 0.18 = 1.863 m³
W-001 = 3.0 × 3.0 × 0.1 = 0.9 m³
C-001 = 0.35 × 0.35 × 3.5 = 0.42875 m³
B-001 = 4.5 × 0.3 × 0.3 = 0.405 m³
```

## 5.3 Face Areas

```text
face_area_m2 = area(face_geometry)
total_surface_area_m2 = sum(face_area_m2)
```

Example:

```text
P-001 top face = 4.5 × 2.3 = 10.35 m²
W-001 broad face = 3.0 × 3.0 = 9.0 m²
C-001 side face = 0.35 × 3.5 = 1.225 m²
B-001 top face = 4.5 × 0.3 = 1.35 m²
```

## 5.4 Opening Geometry

```text
openings = detect_voids(base_geometry)
```

Example:

```text
P-001 openings = none in catalogue example
W-001 openings = none in this example unless generated from geometry
C-001 openings = none
B-001 openings = none
```

## 5.5 Geometry-Derived Mass

The Geometry Generator gives volume.  
The System calculates mass.

```text
mass_kg = net_volume_m3 × material_density_kg_m3
```

Example using 2400 kg/m³:

```text
P-001 calculated = 4471 kg, catalogue = ca. 4100 kg
W-001 calculated = 2160 kg
C-001 calculated = 1029 kg
B-001 calculated if concrete = 972 kg
```

## 5.6 Geometry-Derived Self-Weight

The System calculates self-weight from mass.

```text
self_weight_kN = mass_kg × 9.81 / 1000
```

Example:

```text
P-001 catalogue mass 4100 kg → 40.22 kN
W-001 estimated mass 2160 kg → 21.19 kN
C-001 estimated mass 1029 kg → 10.09 kN
B-001 concrete estimate 972 kg → 9.53 kN
```

For P-001 as slab:

```text
self_weight_kN_m2 = 40.22 kN / 10.35 m² = 3.89 kN/m²
```

## 5.7 Rough U-Value Precheck

The Energy Geometry Generator identifies relevant thickness and faces.  
The System calculates the rough precheck.

```text
R_concrete = thickness_m / lambda_concrete_W_mK
U_rough = 1 / (Rsi + R_concrete + Rse)
```

Example for P-001 with lambda = 2.3 W/mK:

```text
R_concrete = 0.18 / 2.3 = 0.078 m²K/W
```

This is **not** a final envelope proof.

## 5.8 Transport GWP Precheck

The Geometry Generator does not calculate LCA.  
The System calculates it using mass and transport context.

```text
transport_gwp_kgco2e =
mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

Example if transport distance = 30 km and factor = 0.05 kgCO₂e/tkm:

```text
P-001 = 4.1 × 30 × 0.05 = 6.15 kgCO₂e
W-001 = 2.16 × 30 × 0.05 = 3.24 kgCO₂e
C-001 = 1.03 × 30 × 0.05 = 1.55 kgCO₂e
B-001 if concrete = 0.972 × 30 × 0.05 = 1.46 kgCO₂e
```

## 5.9 Avoided GWP Potential

```text
avoided_gwp_potential_kgco2e =
mass_t × new_equivalent_reference_kgco2e_per_t
```

Example using 171.7 kgCO₂e/t:

```text
P-001 = 4.1 × 171.7 = 703.97 kgCO₂e
W-001 = 2.16 × 171.7 = 370.87 kgCO₂e
C-001 = 1.03 × 171.7 = 176.85 kgCO₂e
B-001 if concrete = 0.972 × 171.7 = 166.89 kgCO₂e
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
Concrete example
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
or catalogue mass if available
```

### Concrete Example

```yaml
P-001_header:
  component_name: Deckenplatte P-001
  source_id: DE_1OG_001
  dimensions: 4500 × 2300 × 180 mm
  volume: 1.863 m3
  mass: ca. 4.1 t
  availability: available
  tracking_code: QR-P-001

W-001_header:
  component_name: Wandplatte W-001
  dimensions: 3000 × 3000 × 100 mm
  mass_estimated: 2.16 t

C-001_header:
  component_name: Stütze C-001
  dimensions: 350 × 350 × 3500 mm
  mass_estimated: 1.03 t

B-001_header:
  component_name: Träger B-001
  dimensions: 4500 × 300 × 300 mm
  mass_status: depends_on_material_profile
```

### Must Remain Unknown

```text
measured mass where only estimated
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

### Concrete Example

```yaml
P-001_semio:
  kit_id: kit-abbau-aufbau-example-pool-001
  type_id: type-P-001
  parent_type: type-reclaimed-slab
  type_kind: reclaimed-reinforced_concrete-slab
  stock_total: 1
  stock_available: 1
  generated_representations:
    - P-001.rep.physical
    - P-001.rep.structural
    - P-001.rep.energy
    - P-001.rep.semantic
    - P-001.rep.connector_zones
    - P-001.rep.logistics
  generated_connectors:
    - P-001.port.long_edge_left.slab_edge_bearing
    - P-001.port.long_edge_right.slab_edge_bearing
    - P-001.port.top.service_zone
```

### Must Remain Unknown

```text
manual connector overrides
custom parent taxonomy if project does not define it
true stock if several real components are grouped
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

### Concrete Example

```yaml
P-001_identity:
  source_id: DE_1OG_001
  source_project: Abbau Aufbau
  original_level: 1OG
  element_type: slab
  original_function: floor_slab
  material: reinforced_concrete
  tracking_method: QR generated
  qr_code: QR-P-001
  orientation_candidate:
    top_face: largest horizontal face +Z
    bottom_face: largest horizontal face -Z
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

### Concrete Example

```yaml
pool_availability:
  P-001:
    stock_total: 1
    used_count: 0
    stock_available: 1
    state: available
    storage_position: A-03-02

  W-001:
    stock_total: 1
    used_count: 0
    stock_available: 1
    state: available

  C-001:
    stock_total: 1
    used_count: 0
    stock_available: 1
    state: available

  B-001:
    stock_total: 1
    used_count: 0
    stock_available: 1
    state: available
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

### Concrete Example

```yaml
classification:
  P-001:
    primary_kind: slab
    structural_family: horizontal_spanning
    allowed_roles:
      - floor_slab
      - roof_slab_if_engineered
      - diaphragm_if_engineered
    disallowed_roles:
      - column
      - wall

  W-001:
    primary_kind: wall_panel
    structural_family: vertical_panel
    allowed_roles:
      - wall_panel
      - load_bearing_wall_if_verified
      - partition
    disallowed_roles:
      - slab
      - beam

  C-001:
    primary_kind: column
    structural_family: vertical_point_support
    allowed_roles:
      - vertical_support
      - column_support_if_verified
    disallowed_roles:
      - slab
      - wall_panel

  B-001:
    primary_kind: beam
    structural_family: horizontal_line_support
    allowed_roles:
      - line_support
      - slab_support
      - transfer_beam_if_verified
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

### Concrete Example

```yaml
geometry_overview:
  P-001:
    dimensions_mm: [4500, 2300, 180]
    volume_m3: 1.863
    mass_catalogue_t: 4.1
    mass_calculated_t: 4.47
    mass_display: 4.1
    mass_note: catalogue value preferred

  W-001:
    dimensions_mm: [3000, 3000, 100]
    volume_m3: 0.9
    mass_estimated_t: 2.16

  C-001:
    dimensions_mm: [350, 350, 3500]
    volume_m3: 0.42875
    mass_estimated_t: 1.03

  B-001:
    dimensions_mm: [4500, 300, 300]
    volume_m3_if_concrete: 0.405
    mass_status: depends on steel or concrete definition
```

### Must Remain Unknown

```text
measured density
internal voids not represented in geometry
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

### Concrete Example

```yaml
P-001_representations:
  physical: geometry/P-001/physical.glb
  structural: geometry/P-001/structural_zones.json
  energy: geometry/P-001/energy_faces.json
  semantic: geometry/P-001/semantic_faces.json
  connector_zones: geometry/P-001/connectors.json
  logistics: geometry/P-001/logistics.json
  confidence: medium_high

C-001_representations:
  structural:
    - column_axis
    - base_face
    - head_face
  connector_zones:
    - column_base_bearing
    - column_head_bearing
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

### Concrete Example

```yaml
physical_geometry:
  P-001:
    shape_type: thin_plate
    faces:
      top: 10.35 m2
      bottom: 10.35 m2
    openings: none
    anomaly_status: not_evaluated_without_scan

  W-001:
    shape_type: vertical_plate
    broad_faces: 2
    side_edges: 4

  C-001:
    shape_type: vertical_prism
    top_face: 0.1225 m2
    bottom_face: 0.1225 m2

  B-001:
    shape_type: long_horizontal_prism
    beam_axis: longitudinal
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

### Concrete Example

```yaml
structural_geometry:
  P-001:
    role: spanning_slab
    span_direction_candidate: long_direction_or_engineering_required
    generated_bearing_zones:
      - long_edge_left
      - long_edge_right
    compatible_supports:
      - W-001.wall_top_bearing
      - B-001.beam_top_bearing
      - C-001.column_head_bearing_if_engineered

  W-001:
    role: wall_panel
    generated_bearing_zones:
      - bottom_edge
      - top_edge
    can_support:
      - slab_edge_bearing_if_verified

  C-001:
    role: vertical_point_support
    generated_zones:
      - base_face
      - head_face
    can_support:
      - slab_point_support_if_engineered
      - beam_end_bearing_if_engineered

  B-001:
    role: horizontal_line_support
    generated_zones:
      - left_end_bearing
      - right_end_bearing
      - top_bearing_surface
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

### Concrete Example

```yaml
energy_geometry:
  P-001:
    if_used_as_interior_floor:
      envelope_relevance: not_relevant
    if_used_as_roof:
      envelope_relevance: relevant
      u_value_thickness_m: 0.18
      R_concrete: 0.078
      final_energy_status: project_context_required

  W-001:
    if_used_as_facade_wall:
      envelope_relevance: relevant
      u_value_thickness_m: 0.10
      thermal_bridge_risk:
        - slab_wall_connector

  C-001:
    envelope_relevance: usually_not_relevant_unless_exposed_structure

  B-001:
    thermal_bridge_risk: high_if_steel_beam_crosses_envelope
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

### Concrete Example

```yaml
semantic_geometry:
  P-001:
    potential_new_use:
      - floor_slab
      - roof_slab_if_engineered
    visible_faces:
      - bottom_face_as_ceiling_candidate
      - edge_faces_if_exposed

  W-001:
    potential_new_use:
      - room_partition
      - load_bearing_wall_if_verified
      - facade_panel_if_envelope_resolved
    visible_faces:
      - broad_face_A
      - broad_face_B

  C-001:
    potential_new_use:
      - exposed_column
      - vertical_support

  B-001:
    potential_new_use:
      - visible_support_beam
      - hidden_transfer_member
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

### Concrete Example

```yaml
openings:
  P-001:
    detected_openings: []
    catalogue_openings: none
    service_reuse: no_existing_opening

  W-001:
    detected_openings: []
    note: if future service penetration requested, rebar scan required

  C-001:
    detected_openings: []
    service_penetration: blocked_by_default

  B-001:
    detected_openings: []
    service_penetration: project_context_required
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

### Concrete Example

```yaml
surface_condition:
  P-001:
    top_face: unknown_without_photo_or_scan
    bottom_face: unknown_without_photo_or_scan
    edge_condition: unknown
    visible_reuse_quality: cannot_rate

  W-001:
    broad_faces: unknown
    visible_reuse_quality: cannot_rate

  C-001:
    side_faces: unknown
    column_corner_damage: unknown

  B-001:
    surface_condition: depends_on_material_and_evidence
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

### Concrete Example

```yaml
damage_records:
  P-001:
    records: []
    status: no_damage_data_provided

  W-001:
    records: []
    status: no_damage_data_provided

  C-001:
    records: []
    status: no_damage_data_provided

  B-001:
    records: []
    status: no_damage_data_provided
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

### Concrete Example

```yaml
concrete_evidence:
  P-001:
    density_used: catalogue_mass_preferred
    compressive_strength: unknown
    carbonation_depth: unknown
    chloride_content: unknown
    evidence_status: incomplete

  W-001:
    compressive_strength: project_text_mentions_C25_30_if_protocol_exists
    evidence_status: requires_protocol

  C-001:
    compressive_strength: project_text_mentions_C25_30_if_protocol_exists
    evidence_status: requires_protocol

  B-001:
    if_steel: concrete_evidence_not_applicable
    if_concrete: concrete_evidence_required
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

### Concrete Example

```yaml
reinforcement_evidence:
  P-001:
    main_reinforcement_direction: inferred_from_slab_typology
    status: unknown_without_scan
    drilling_permission: blocked_until_rebar_scan

  W-001:
    status: unknown_without_scan
    wall_anchor_drilling: blocked_until_rebar_scan

  C-001:
    status: unknown_without_scan
    dowel_connection: engineering_required

  B-001:
    if_steel: reinforcement_not_applicable
    if_concrete: unknown_without_scan
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

### Concrete Example

```yaml
durability:
  P-001:
    status: engineering_required
    carbonation_risk: unknown
    chloride_risk: unknown
    moisture_risk: depends_on_storage_and_future_use

  W-001:
    status: engineering_required
    if_facade_use: moisture_and_freeze_thaw_check_required

  C-001:
    status: engineering_required
    corner_damage_risk: unknown

  B-001:
    if_steel: corrosion_protection_required
    if_concrete: concrete_durability_required
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

### Concrete Example

```yaml
structural_data:
  P-001:
    role: slab
    self_weight_kN: 40.22
    self_weight_kN_m2: 3.89
    allowed_supports:
      - wall_top
      - beam_top
      - column_head_if_engineered
    load_capacity: unknown
    proof_required: true

  W-001:
    role: wall_panel
    self_weight_kN: 21.19
    can_support_slab: only_if_verified
    proof_required: true

  C-001:
    role: column
    self_weight_kN: 10.09
    can_support_beam_or_slab: only_if_verified
    proof_required: true

  B-001:
    role: beam
    self_weight_kN_if_concrete: 9.53
    can_support_slab: only_if_verified
    proof_required: true
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

### Concrete Example

```yaml
connector_interface_data:
  P-001:
    ports:
      - slab-edge-bearing
      - slab-top-service-zone
      - slab-envelope-face
    compatible_ports:
      slab-edge-bearing:
        - W-001.wall-top-bearing
        - B-001.beam-top-bearing
        - C-001.column-head-bearing-if-engineered

  W-001:
    ports:
      - wall-top-bearing
      - wall-bottom-bearing
      - wall-side-joint
    compatible_ports:
      wall-top-bearing:
        - P-001.slab-edge-bearing

  C-001:
    ports:
      - column-base-bearing
      - column-head-bearing
    compatible_ports:
      column-head-bearing:
        - P-001.slab-point-support-if-engineered
        - B-001.beam-end-bearing-if_engineered

  B-001:
    ports:
      - beam-end-bearing
      - beam-top-bearing
    compatible_ports:
      beam-top-bearing:
        - P-001.slab-edge-bearing
```

Abbau/Aufbau connector families available for this example:

```yaml
allowed_connection_families:
  wall_slab:
    - post_installed_rebar_grout
    - screw_anchor_flat_steel_holder

  column_slab:
    - stainless_dowel
    - angle_connector
    - post_installed_rebar_grout_on_new_rc_beam
    - steel_beam_support

  base_column:
    - stainless_dowel
    - angle_connector
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

### Concrete Example

```yaml
drilling_zones:
  P-001:
    connector_zones_generated: true
    rebar_scan: missing
    approved_drilling_zones: []
    unknown_zones:
      - all_anchor_related_zones
    blocked_action:
      - drill_for_anchor_without_scan

  W-001:
    rebar_scan: missing
    wall_top_anchor_zone: unknown

  C-001:
    rebar_scan: missing
    dowel_zone: unknown

  B-001:
    if_steel: drilling_logic_uses_steel_connection_rules
    if_concrete: rebar_scan_required
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

### Concrete Example

```yaml
fire_data:
  P-001:
    material: reinforced_concrete
    material_fire_class_candidate: non_combustible
    fire_resistance_rating: unknown
    connector_fire_warning: if_exposed_steel_connector

  W-001:
    fire_resistance_rating: unknown
    fire_context_required: true

  C-001:
    fire_resistance_rating: unknown
    column_fire_proof_required_if_loadbearing: true

  B-001:
    if_steel:
      exposed_steel_warning: true
      fire_cover_required_if_fire_relevant: true
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

### Concrete Example

```yaml
building_physics:
  P-001:
    thickness_m: 0.18
    lambda_default: 2.3
    R_concrete: 0.078
    envelope_status: requires_context

  W-001:
    thickness_m: 0.10
    R_concrete: 0.043
    if_external_wall: insulation_required_likely

  C-001:
    building_physics_relevance: mostly_contextual

  B-001:
    if_steel: thermal_bridge_risk_high_if_envelope_crossing
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

### Concrete Example

```yaml
acoustic_data:
  P-001:
    mass_per_area: 4100 kg / 10.35 m2 = 396 kg/m2
    acoustic_relevance: high_mass_element
    actual_rating: unknown

  W-001:
    mass_per_area: 2160 kg / 9.0 m2 = 240 kg/m2
    acoustic_relevance: potentially_useful_wall_mass
    actual_rating: unknown

  C-001:
    acoustic_relevance: low_for_room_separation

  B-001:
    acoustic_relevance: context_dependent
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

### Concrete Example

```yaml
services_data:
  P-001:
    existing_openings: none
    new_core_drilling: blocked_until_rebar_scan

  W-001:
    existing_openings: none
    vertical_service_route: possible_only_with_context_and_scan

  C-001:
    service_penetration: not_preferred

  B-001:
    service_conflict: depends_on_beam_location
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

### Concrete Example

```yaml
logistics_data:
  P-001:
    mass: 4.1 t
    recommended_storage_orientation: lying_flat
    separator_required: true
    weather_protection_required: true
    lifting_points: engineering_required

  W-001:
    mass: 2.16 t
    recommended_storage_orientation: standing_with_support_or_engineered_storage
    temporary_bracing: likely_required

  C-001:
    mass: 1.03 t
    storage_orientation: standing_or_supported_horizontal
    temporary_bracing: context_required

  B-001:
    mass: depends_on_material
    storage_orientation: supported_at_beam_support_points
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

### Concrete Example

```yaml
transport_data:
  assumed_distance_km: 30
  factor_kgco2e_per_tkm: 0.05

  P-001:
    transport_gwp: 6.15 kgCO2e

  W-001:
    transport_gwp: 3.24 kgCO2e

  C-001:
    transport_gwp: 1.55 kgCO2e

  B-001_if_concrete:
    transport_gwp: 1.46 kgCO2e
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

### Concrete Example

```yaml
lca_data:
  project_assumptions:
    A1_A3_reuse_component: 0 kgCO2e/t
    new_concrete_reference: 171.7 kgCO2e/t
    transport_factor: 0.05 kgCO2e/tkm
    distance: 30 km

  P-001:
    reused_mass_t: 4.1
    transport_gwp: 6.15
    avoided_gwp_potential: 703.97
    lca_status: precheck_only

  W-001:
    reused_mass_t: 2.16
    transport_gwp: 3.24
    avoided_gwp_potential: 370.87
    lca_status: precheck_only

  C-001:
    reused_mass_t: 1.03
    transport_gwp: 1.55
    avoided_gwp_potential: 176.85
    lca_status: precheck_only

  B-001_if_concrete:
    reused_mass_t: 0.972
    transport_gwp: 1.46
    avoided_gwp_potential: 166.89
    lca_status: material_definition_required
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

### Concrete Example

```yaml
documentation:
  P-001:
    catalogue_source: Abbau Aufbau handbook table
    base_geometry: geometry/P-001/base.glb
    concrete_test_report: missing
    rebar_scan: missing
    damage_photos: missing
    lca_dataset: project_default_precheck

  W-001:
    catalogue_source: system example based on Abbau/Aufbau tender wall dimensions
    concrete_test_report: missing
    rebar_scan: missing

  C-001:
    catalogue_source: system example based on Abbau/Aufbau tender column dimensions
    concrete_test_report: missing
    rebar_scan: missing

  B-001:
    catalogue_source: system beam/support typology example
    material_profile_document: required
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

### Concrete Example

```yaml
evidence_completeness:
  P-001:
    identity: complete
    geometry: complete
    mass: complete_catalogue
    connector_zones: generated
    concrete_evidence: missing
    reinforcement_evidence: missing
    fire: requires_context
    building_physics: requires_context
    lca: precheck_available

  W-001:
    identity: partial
    geometry: generated_from_example_dimensions
    mass: estimated
    concrete_evidence: missing
    reinforcement_evidence: missing

  C-001:
    identity: partial
    geometry: generated_from_example_dimensions
    mass: estimated
    concrete_evidence: missing
    reinforcement_evidence: missing

  B-001:
    identity: system_example
    material_definition: incomplete
    lca: incomplete_until_material_confirmed
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

### Concrete Example

```yaml
pool_warnings:
  P-001:
    - missing_rebar_scan
    - missing_concrete_strength_test
    - missing_fire_rating
    - do_not_drill_without_verification
    - connector_lca_dataset_missing

  W-001:
    - example_component_requires_real_catalogue_record
    - missing_rebar_scan
    - missing_concrete_strength_test
    - do_not_use_as_loadbearing_until_verified

  C-001:
    - missing_rebar_scan
    - missing_column_capacity_proof
    - base_and_head_dowel_zones_unverified

  B-001:
    - material_profile_required
    - connector_capacity_required
    - fire_protection_required_if_steel_and_exposed
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

### Concrete Example

```yaml
rule_checker_readiness:
  ready_now:
    - identity_check
    - stock_availability_check
    - geometry_fit_check
    - pair_classification
    - port_compatibility_precheck
    - mass_logistics_precheck
    - LCA_mass_transport_precheck

  needs_evidence:
    - structural_capacity
    - reinforcement_scan
    - anchor_drilling_zones
    - fire_rating
    - thermal_envelope_context
    - connector_capacity
    - connector_lca_dataset

  blocked_actions:
    - drill_without_rebar_scan
    - approve_loadbearing_connection_without_structural_proof
    - approve_exposed_steel_connector_without_fire_detail
    - calculate_full_LCA_without_dataset

  default_status_if_user_connects:
    P-001_to_W-001: warning_engineering_required
    P-001_to_C-001: warning_engineering_required_punching_or_point_support
    P-001_to_B-001: warning_engineering_required
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

### Concrete Example

```text
When clicking P-001:
show its generated slab ports, geometry, mass, catalogue data, warnings.

Do not show:
"connection P-001 to W-001 is valid/invalid."

That appears only after the user actually connects P-001 to W-001.
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

---

# 10. Source References

## Abbau/Aufbau handbook references used for this example

```text
Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden
Abbau/Aufbau, AP3, 2023

Relevant project logic used:
- Bauteilkatalog fields: ID, Skizze, Maße, Öffnungsmaße, Volumen, Masse
- DE_1OG_001 catalogue example
- Tracking and tracing through BIM, QR code, RFID
- Transport and storage logic
- LCA assumptions for reused concrete and transport
- Execution-planning connector families:
  Wand-Decke:
    nachträglicher Bewehrungsanschluss + Verguss
    Schraubanker mit Flachstahlhalter
  Stütze-Decke:
    Edelstahldorn
    Winkelverbinder
    Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
    Auflager auf Stahlträger
  Bodenplatte-Stütze:
    Edelstahldorn
    Winkelverbinder
- Tender examples:
  reused wall plates, thickness 10 cm, length/height 3 m
  reused column, rectangular 35 × 35 cm, height 3.5 m
```
