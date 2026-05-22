# Verified Abbau/Aufbau Concrete Example  
## Geometry-Generator-Based Bauteilpass for a Mixed Slab–Beam–Column Pool Element

**Status of this document:** corrected and source-audited example.  
**Project basis:** Abbau/Aufbau handbook logic.  
**Important correction:** Geometry Generators produce only geometry-related representations, zones, ports, openings, faces, edges, and geometry-derived quantities. All non-geometric interpretation is produced by System Modules.

---

# 0. Verification Notes

## 0.1 What is directly confirmed by Abbau/Aufbau

The Abbau/Aufbau handbook gives a concrete Bauteilkatalog example:

```yaml
confirmed_catalogue_example:
  id: DE_1OG_001
  type: Deckenplatte / slab element
  dimensions_mm:
    length: 4500
    width: 2300
    height: 180
  openings: "-"
  volume_m3: 1.863
  mass_t: "ca. 4.1"
```

The handbook also defines the Bauteilkatalog fields:

```text
ID
Skizze
Maße in mm
Öffnungsmaße in mm
Volumen in m³
Masse in t
optional concrete and reinforcement investigation results
```

The handbook states that the Bauteilkatalog and element ID form the basis for:

```text
logistics concept
storage
reinstallation
tracking / tracing
```

## 0.2 What is not directly confirmed

The handbook does **not** provide a listed catalogue item that already contains:

```text
one slab slice
+ one beam/downstand slice
+ one column stump/capital zone
inside one single mixed component
```

Therefore, the example element below is a **hypothetical Abbau/Aufbau-style pool component**, not a real handbook catalogue row.

## 0.3 Why the mixed element is still project-consistent

The handbook explicitly works with reused reinforced-concrete elements such as:

```text
Platte
Scheibe
Träger / Unterzug
Stütze
Decke
Wand
Bodenplatte
```

It also discusses early reuse concepts such as:

```text
individual columns
individual slabs
pairs of columns with connecting beams / Unterzüge
```

So a monolithic mixed element is plausible as a **generated pool typology**, but it must be marked as:

```text
hypothetical
geometry-derived
engineering_required
not automatically approved
```

## 0.4 Main corrections made compared to the earlier file

```text
1. The mixed element is now clearly marked as hypothetical.
2. The slab-zone dimensions are anchored to the real Abbau/Aufbau catalogue example DE_1OG_001.
3. The beam and column sub-zones are explicitly generated example geometry, not handbook data.
4. Density is not treated as measured; it is an Abbau/Aufbau-style transport/mass assumption.
5. Mass is marked estimated unless a measured catalogue mass exists.
6. Structural capacity is never calculated from geometry alone.
7. No drilling zone is approved without reinforcement evidence.
8. LCA is only a precheck unless datasets and connector/adapter quantities are available.
9. Connector families are limited to Abbau/Aufbau connection details.
10. Storage rules are adapted to the mixed geometry instead of treating it like a flat slab.
```

---

# 1. System Overview

## 1.1 Example Component

```yaml
example_component:
  component_id: AA_MIX_001
  name: Mixed Slab-Beam-Column Slice
  source_system: Abbau/Aufbau-style Bauteilpool
  status: hypothetical_example_not_handbook_catalogue_item
  material_kind: reinforced_concrete
  component_typology: mixed_slab_beam_column_slice

  description: >
    One monolithic reclaimed reinforced-concrete element containing:
    a slab zone based on the Abbau/Aufbau catalogue example DE_1OG_001,
    an additional downstand beam zone,
    and a column stump / capital-like zone.
```

## 1.2 Source Anchors Used

```yaml
source_anchors:
  catalogue_slab_reference:
    id: DE_1OG_001
    dimensions_mm: 4500 x 2300 x 180
    volume_m3: 1.863
    mass_t: ca_4.1

  lca_transport_factor:
    value: 0.05
    unit: kg_CO2eq_per_tkm
    source_logic: 40t truck transport value used in handbook

  new_concrete_reference:
    value: 171.7
    unit: kg_CO2eq_per_t
    source_logic: new 20cm precast concrete slab reference

  reuse_A1_A3_assumption:
    value: 0
    unit: kg_CO2eq_per_t
    source_logic: used elements have no reused-element dataset, so A1-A3 GWP may be set to zero in the reuse scenario

  mass_density_assumption:
    value: 2.5
    unit: t_per_m3
    source_logic: handbook transport-cost calculation uses approx. 2.5 t/m3 for reinforced concrete
```

## 1.3 Main Pipeline

```text
Minimum Input
+ Base Geometry
+ Mixed Component Typology
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

## 1.4 Minimum Input for This Example

```yaml
minimum_input:
  component_id: AA_MIX_001
  component_typology: mixed_slab_beam_column_slice
  material_kind: reinforced_concrete

  base_geometry_reference: representations/AA_MIX_001/base.glb

  source_context:
    source_project: Abbau/Aufbau
    source_status: hypothetical_pool_element_based_on_handbook_logic
    source_building: unknown
    original_level: unknown
    original_function: slab_beam_column_zone_candidate

  pool_context:
    kit_id: kit-abbau-aufbau-pool-001
    current_storage_location: storage-yard-01
    storage_position: MIX-A-01

  project_defaults:
    density_reinforced_concrete_t_m3: 2.5
    lambda_reinforced_concrete_W_mK: 2.3
    transport_factor_kgCO2eq_per_tkm: 0.05
    new_precast_concrete_reference_kgCO2eq_per_t: 171.7
    default_transport_distance_km: 40

  optional_evidence:
    concrete_test_report: missing
    reinforcement_scan: partial_or_missing
    damage_photos: optional
    fire_document: missing
    lca_dataset: generic_reference_only
```

---

# 2. Core Concepts

## 2.1 Bauteilpass

For `AA_MIX_001`, the Bauteilpass is a **mixed component passport**:

```text
one real component identity
+ slab sub-zone
+ beam / Unterzug sub-zone
+ column / Stütze sub-zone
+ internal monolithic transition zones
+ external connector zones
+ geometry-derived quantities
+ evidence and system warnings
```

## 2.2 Geometry Generator

The Geometry Generator produces only geometry-related information:

```text
physical geometry
sub-zone map
slab zone
beam zone
column zone
internal transition zones
support / bearing faces
connector-zone geometry
port geometry
opening geometry
logistics geometry
```

It does **not** produce:

```text
final structural approval
material strength
fire resistance rating
LCA completeness
approval readiness
connection validity
target-preference score
```

## 2.3 System Module

The System Modules consume generated geometry plus catalogue/context/evidence data.

For this example, the system produces:

```text
Semio binding
classification
availability
material evidence status
reinforcement evidence status
structural data status
connector options
fire flags
building physics precheck
services status
logistics status
transport precheck
LCA precheck
documentation status
pool warnings
rule-checker readiness
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

## 3.3 Responsibility Matrix for `AA_MIX_001`

| Part | Example output |
|---|---|
| Geometry Generators | slab zone, beam zone, column zone, transition zones, ports, faces, openings |
| System Modules | evidence state, LCA precheck, connector options, logistics status, warnings |
| Rule Checker | validates active connection when the user connects this piece to another piece |
| Bauteilpass Panel | shows pool data and generated component data only |
| Connection Passport | stores result of connecting `AA_MIX_001` to another piece |

---

# 4. Typology Library for This Example

## 4.1 Mixed Typology Definition

```yaml
typology:
  id: mixed_slab_beam_column_slice
  parent_typologies:
    - slab
    - beam
    - column

  handbook_alignment:
    direct_catalogue_match: false
    uses_confirmed_AA_slab_dimensions: true
    uses_AA_element_families:
      - Decke
      - Unterzug
      - Stütze

  geometry_expectation:
    shape: monolithic_composite
    contains:
      - thin_horizontal_slab_zone
      - downstand_beam_zone
      - vertical_column_stump_or_capital_zone

  generated_ports:
    - slab-edge-bearing
    - slab-top-service-zone
    - slab-envelope-face
    - beam-end-bearing
    - beam-side-connector
    - column-base-bearing
    - column-head-or-capital-bearing
    - internal-slab-beam-transition
    - internal-beam-column-transition
```

## 4.2 Concrete Example Geometry

The slab zone is anchored to the confirmed Abbau/Aufbau catalogue row `DE_1OG_001`.

The beam and column zones are generated example geometry.

```yaml
generated_geometry_values:
  slab_zone:
    source: based_on_confirmed_DE_1OG_001_dimensions
    length_mm: 4500
    width_mm: 2300
    thickness_mm: 180
    volume_m3: 1.863

  beam_downstand_zone:
    source: generated_example_geometry
    length_mm: 4500
    width_mm: 300
    extra_depth_below_slab_mm: 420
    volume_m3: 0.567

  column_stump_zone:
    source: generated_example_geometry
    width_mm: 450
    depth_mm: 450
    height_below_beam_mm: 900
    volume_m3: 0.182

  total_net_volume_m3: 2.612
  density_assumption_t_m3: 2.5
  estimated_mass_t: 6.53
```

## 4.3 Calculation Proof

```text
slab volume =
4.50 m × 2.30 m × 0.18 m
= 1.863 m³

beam extra volume =
4.50 m × 0.30 m × 0.42 m
= 0.567 m³

column stump volume =
0.45 m × 0.45 m × 0.90 m
= 0.182 m³

total net volume =
1.863 + 0.567 + 0.182
= 2.612 m³

estimated mass =
2.612 m³ × 2.5 t/m³
= 6.53 t

self weight =
6.53 t × 1000 × 9.81 / 1000
= 64.07 kN
```

---

# 5. Shared Geometry and System Calculations

## 5.1 Dimensions

```yaml
overall_bounding_box:
  length_mm: 4500
  width_mm: 2300
  total_height_mm: 1500
```

The total height includes:

```text
slab thickness: 180 mm
beam downstand below slab: 420 mm
column stump below beam: 900 mm
total: 1500 mm
```

## 5.2 Volume

```yaml
net_volume_m3: 2.612
volume_status: generated_from_example_geometry
```

## 5.3 Mass

```text
mass_t =
2.612 × 2.5
= 6.53 t
```

Status:

```text
estimated
not measured
replace with catalogue mass if measured mass is available
```

## 5.4 Self-Weight

```text
self_weight =
6.53 t × 9.81
= 64.07 kN
```

For slab plan area:

```text
plan_area =
4.50 × 2.30
= 10.35 m²

self_weight_per_plan_area =
64.07 / 10.35
= 6.19 kN/m²
```

## 5.5 Transport GWP Precheck

```text
transport_gwp =
6.53 t × 40 km × 0.05 kg CO₂-eq/tkm
= 13.06 kg CO₂-eq
```

## 5.6 Avoided New-Material GWP Potential

```text
avoided_gwp_potential =
6.53 t × 171.7 kg CO₂-eq/t
= 1121.31 kg CO₂-eq
```

## 5.7 Rough U-Value Precheck

```text
R_concrete =
0.18 / 2.3
= 0.078 m²K/W
```

This is only a rough concrete-layer precheck. It is not a final energy proof.

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

Each section below uses:

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

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
current_storage_location: storage-yard-01
```

### Geometry Generator Output

```yaml
main_dimensions:
  length_mm: 4500
  width_mm: 2300
  total_height_mm: 1500

net_volume_m3: 2.612
preview_source: generated_from_base_geometry
```

### System Output

```yaml
component_name: Mixed Slab-Beam-Column Slice AA_MIX_001
material_label: Stahlbeton
availability: available
mass_t: 6.53
mass_status: estimated_from_generated_volume_and_AA_density_assumption
evidence_completeness: partial_engineering_required
tracking_code: QR-AA_MIX_001
```

### Proof

```text
component_name =
human_label(mixed_slab_beam_column_slice) + " " + component_id

mass =
2.612 m³ × 2.5 t/m³
= 6.53 t

tracking_code =
"QR-" + component_id
```

### Must Remain Unknown

```text
measured mass
physical marking status
actual storage presence if storage system is not synced
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

```yaml
kit_id: kit-abbau-aufbau-pool-001
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

### Geometry Generator Output

```yaml
representations:
  - physical_geometry
  - structural_geometry
  - energy_geometry
  - semantic_geometry
  - connector_zone_geometry
  - logistics_geometry

generated_ports:
  - slab-edge-bearing
  - beam-end-bearing
  - column-base-bearing
  - column-head-or-capital-bearing
  - service-penetration-candidate
  - thermal-envelope-interface
  - internal-slab-beam-transition
  - internal-beam-column-transition
```

### System Output

```yaml
kit_name: Abbau/Aufbau Bauteilpool
type_id: type-AA_MIX_001
type_name: AA_MIX_001
parent_type: type-reclaimed-mixed-slab-beam-column-slice
type_kind: reclaimed-reinforced_concrete-mixed_slab_beam_column_slice
stock_total: 1
stock_available: 1
attribute_namespace: abbauaufbau
quality_namespace: abbauaufbau
```

### Proof

```text
type_id =
"type-" + component_id

stock_total =
1 because this is one real reclaimed component

connectors =
generated ports registered as Semio connectors
```

### Must Remain Unknown

```text
manual connector overrides
custom parent taxonomy
actual grouped stock if multiple similar elements are later added
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

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
source_project: Abbau/Aufbau
source_building_id: unknown
original_level: unknown
original_function: slab_beam_column_zone_candidate
```

### Geometry Generator Output

```yaml
orientation_candidates:
  slab_top_face: z_positive_large_face
  slab_bottom_face: underside_of_slab
  beam_downstand_direction: z_negative
  column_axis: z_axis
```

### System Output

```yaml
human_readable_name: Mixed Slab-Beam-Column Slice AA_MIX_001
element_type: composite_reclaimed_concrete_element
material_type: reinforced_concrete
tracking_method: generated_qr
qr_code: QR-AA_MIX_001
rfid_code: unknown
internal_guid: generated_uuid
external_reference: catalogue/AA_MIX_001
physical_marking_status: unknown
```

### Proof

```text
original_function is not confirmed from the handbook.
It is marked candidate because the component is a hypothetical pool element.
```

### Must Remain Unknown

```text
true RFID
physical marking status
exact original structural role without archive data
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

```yaml
component_id: AA_MIX_001
stock_rule: individual_component
design_graph_access: true
storage_location: storage-yard-01
```

### Geometry Generator Output

```text
none
```

### System Output

```yaml
stock_total: 1
used_count: 0
reserved_count: 0
stock_available: 1
availability_state: available
storage_state: located
linked_piece_ids: []
reserved_design: null
blocked_reason: null
```

### Proof

```text
stock_available =
1 - 0 - 0
= 1
```

### Must Remain Unknown

```text
actual physical presence without storage scan
new damage after catalogue registration
off-system reservation
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

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

### Geometry Generator Output

```yaml
shape_class: monolithic_composite
sub_zones:
  - slab_zone
  - beam_zone
  - column_zone
structural_zone_candidates:
  - slab_bearing_edges
  - beam_end_faces
  - column_base_face
  - column_head_transition
```

### System Output

```yaml
primary_kind: mixed_component
secondary_kinds:
  - slab_slice
  - downstand_beam_slice
  - column_stump_or_capital_zone
material_family: reinforced_concrete
structural_family: mixed_horizontal_vertical_support
allowed_design_roles:
  - composite_support_element_if_engineered
  - slab_edge_support_zone_if_engineered
  - beam_support_zone_if_engineered
  - column_base_or_head_interface_if_engineered
disallowed_design_roles:
  - simple_generic_slab
  - simple_generic_column
  - approved_primary_structure_without_proof
semantic_tags:
  - reclaimed
  - reinforced_concrete
  - composite
  - abbau_aufbau
reuse_category: reusable_with_verification
risk_category: high_evidence_need
```

### Proof

```text
The risk category is high because the element contains multiple interacting
structural sub-zones. Geometry is available, but structural proof is missing.
```

### Must Remain Unknown

```text
approved final structural role
actual load-bearing capacity
final reuse category without evidence
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

### Geometry Generator Output

```yaml
unit_system: mm
overall_bounding_box:
  length_mm: 4500
  width_mm: 2300
  height_mm: 1500
sub_zone_volumes:
  slab_zone_m3: 1.863
  beam_zone_m3: 0.567
  column_zone_m3: 0.182
net_volume_m3: 2.612
center_of_gravity: generated_from_solid_volume
top_bottom_candidates:
  original_slab_top: z_positive_large_face
  underside_complex_zone: z_negative_composite_face
```

### System Output

```yaml
density_t_m3: 2.5
density_status: AA_assumption_not_measured
mass_t: 6.53
geometry_tolerance_mm: project_default
placement_tolerance_mm: project_default
joint_tolerance_mm: project_default
```

### Proof

```text
mass =
2.612 × 2.5
= 6.53 t
```

### Must Remain Unknown

```text
measured density
actual fabrication tolerance
true original top face if metadata conflicts with generator inference
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

### Geometry Generator Output

```yaml
representations:
  physical:
    file: generated/AA_MIX_001/physical.glb
  structural:
    file: generated/AA_MIX_001/structural-zones.json
  energy:
    file: generated/AA_MIX_001/energy-faces.json
  semantic:
    file: generated/AA_MIX_001/semantic-zones.json
  connector_zones:
    file: generated/AA_MIX_001/ports-and-zones.json
  logistics:
    file: generated/AA_MIX_001/logistics-geometry.json
confidence:
  physical: high
  structural: medium
  energy: medium
  semantic: medium
  connector_zones: medium
  logistics: medium
```

### System Output

```yaml
representation_registry: registered_in_semio_type
missing_representation_flags:
  - no_original_bim_model
  - no_full_rebar_scan
  - no_fire_document
```

### Proof

```text
All generated representations are derived from base geometry and mixed typology.
Confidence is medium where structural meaning is inferred rather than proven.
```

### Must Remain Unknown

```text
true structural proof
true energy compliance
true semantic use without design context
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
```

### Geometry Generator Output

```yaml
shape_type: monolithic_slab_beam_column_composite
faces:
  slab_top_face: generated
  slab_bottom_faces: generated
  beam_side_faces: generated
  beam_bottom_face: generated
  column_side_faces: generated
  column_base_face: generated
edges:
  slab_perimeter_edges: generated
  beam_end_edges: generated
  column_base_edges: generated
openings: []
cutouts: []
irregularities:
  - local_chipped_edge_candidate_at_slab_corner
physical_tolerance_estimate: generated_from_scan_or_mesh_deviation
```

### System Output

```yaml
damage_candidate_status: requires_visual_confirmation
surface_condition_status: partial
edge_condition_status: partial
```

### Proof

```text
The generator detects a monolithic composite by identifying:
thin slab plate
linear downstand beam zone
vertical column-like projection
```

### Must Remain Unknown

```text
whether chipped edge is damage or modelling artifact
microcracks
surface contamination
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

```yaml
component_typology: mixed_slab_beam_column_slice
base_geometry_reference: representations/AA_MIX_001/base.glb
original_function: slab_beam_column_zone_candidate
```

### Geometry Generator Output

```yaml
structural_zones:
  slab_zone:
    span_direction_candidate: x_axis
    line_bearing_candidates:
      - slab_long_edge_left
      - slab_long_edge_right
    thickness_mm: 180

  beam_zone:
    axis: x_axis
    end_bearing_candidates:
      - beam_end_A
      - beam_end_B
    downstand_depth_mm: 420

  column_zone:
    axis: z_axis
    base_bearing_face: column_base_face
    head_transition_zone: beam_column_transition

  internal_monolithic_transitions:
    - slab_beam_transition
    - beam_column_transition

load_direction: z_negative
structural_openings: []
```

### System Output

```yaml
structural_role: composite_structural_candidate
preferred_support_condition: engineering_required
forbidden_support_condition:
  - use_as_simple_slab_without_accounting_for_beam_column_mass
  - drill_in_transition_zone_without_rebar_scan
minimum_bearing_length_mm: project_rule_required
reinforcement_direction_status: inferred_not_verified
```

### Proof

```text
The component cannot be treated as a simple slab because its mass,
load path, storage, lifting, support, and connector zones are affected by
the beam and column sub-zones.
```

### Must Remain Unknown

```text
actual load capacity
moment capacity
shear capacity
punching resistance
reinforcement layout
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

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
intended_exposure_context: unknown
```

### Geometry Generator Output

```yaml
energy_geometry:
  slab_top_face: possible_floor_or_roof_surface
  slab_edges: thermal_bridge_candidate_if_exterior
  beam_downstand_faces: interior_exposed_mass_candidate
  column_faces: interior_or_exterior_pier_candidate
  thermal_boundary_candidates:
    - slab_top_face_if_roof
    - slab_edge_faces_if_envelope
  moisture_risk_candidates:
    - slab_top_if_exterior_roof
    - column_base_if_ground_contact
```

### System Output

```yaml
envelope_relevance: requires_project_context
rough_U_value_precheck_status: possible_but_not_final
thermal_bridge_warning: conditional
moisture_risk_status: conditional
```

### Proof

```text
If the slab zone becomes part of roof/floor envelope:
R_concrete = 0.18 / 2.3 = 0.078 m²K/W

This is not enough for final energy proof.
The system flags insulation and thermal-bridge checks if the element enters the envelope.
```

### Must Remain Unknown

```text
inside/outside status
final U-value
thermal bridge Psi-value
moisture proof
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

```yaml
component_typology: mixed_slab_beam_column_slice
source_context:
  original_function: slab_beam_column_zone_candidate
target_use_context: unknown
```

### Geometry Generator Output

```yaml
semantic_geometry:
  visible_face_candidates:
    - slab_underside
    - beam_sides
    - beam_bottom
    - column_sides
  hidden_or_bearing_face_candidates:
    - slab_top_if_floor_build_up
    - column_base_if_supported
    - beam_ends_if_connected
  original_use_side_candidates:
    slab_top: floor_side_candidate
    slab_bottom: ceiling_side_candidate
    beam_downstand: exposed_structural_zone_candidate
    column_stump: vertical_support_zone_candidate
```

### System Output

```yaml
potential_new_use:
  - expressive_reuse_structural_fragment
  - hybrid_support_or_spatial_marker_if_engineered
  - local_canopy_or_floor_edge_piece_if_engineered
spatial_role: composite_structural_spatial_piece
visible_reuse_potential: high_if_left_exposed
surface_expression_value: requires_condition_confirmation
```

### Proof

```text
The mixed geometry has strong architectural identity because the beam and column
zones make the original structural system legible.
```

### Must Remain Unknown

```text
actual architectural intention
visual quality without verified photos/scans
whether the piece should be exposed or concealed
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
```

### Geometry Generator Output

```yaml
openings: []
penetration_candidates:
  slab_top_service_zone:
    status: candidate_only
  beam_side_penetration:
    status: not_recommended_without_rebar_scan
  column_penetration:
    status: blocked_by_default
```

### System Output

```yaml
existing_service_openings: []
core_drilling_status: blocked_until_rebar_scan
service_reuse_status: no_existing_openings
```

### Proof

```text
The generator finds no existing through-openings.
The system blocks new service penetrations until reinforcement evidence exists.
```

### Must Remain Unknown

```text
hidden sleeves or undocumented openings
safe core drilling zones without rebar scan
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
damage_photos: optional_or_partial
```

### Geometry Generator Output

```yaml
face_map:
  slab_top: generated
  slab_underside: generated
  beam_sides: generated
  beam_bottom: generated
  column_sides: generated
  column_base: generated
edge_map: generated
geometric_anomaly_candidates:
  - slab_corner_A_chip
```

### System Output

```yaml
surface_condition_status: partial
edge_condition_status: warning_if_photo_confirms_damage
spalling: minor_candidate
cracks: unknown
exposed_reinforcement: unknown_or_not_detected
visual_quality: requires_photo_review
visible_reuse_quality: requires_condition_confirmation
```

### Proof

```text
The system can interpret a chipped corner only because the geometry generator
mapped the anomaly to a slab perimeter edge.
```

### Must Remain Unknown

```text
microcracks
chloride contamination
subsurface damage
true repair quality
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
damage_photos: optional_or_partial
```

### Geometry Generator Output

```yaml
damage_location_candidates:
  - id: geom-damage-candidate-001
    location: slab_corner_A
    affected_geometry: slab_perimeter_edge
    approximate_size_mm:
      length: 120
      depth: 25
```

### System Output

```yaml
damage_records:
  - id: damage-AA_MIX_001-001
    kind: edge_spalling_candidate
    severity: minor_to_medium_if_confirmed
    affected_face_or_edge: slab_corner_A
    photo_reference: photos/AA_MIX_001/corner_A.jpg
    repair_status: unknown
    rule_relevance:
      - do_not_use_as_primary_bearing_zone_without_review
      - visible_reuse_surface_warning
```

### Proof

```text
Severity increases if damage intersects a generated bearing zone.
```

### Must Remain Unknown

```text
cause of damage
whether damage affects reinforcement
final severity without expert review
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

```yaml
material_kind: reinforced_concrete
concrete_test_report: missing
```

### Geometry Generator Output

```text
none
```

### System Output

```yaml
density_t_m3: 2.5
density_status: AA_assumption_for_estimation_not_tested
compressive_strength: unknown
tensile_strength: unknown
e_modulus: unknown
carbonation_depth: unknown
chloride_content: unknown
pollutant_content: unknown
moisture_status: unknown
evidence_confidence: low
missing_evidence:
  - concrete_strength_test
  - carbonation_test
  - chloride_test
  - pollutant_screening_if_required
```

### Proof

```text
Density can support mass estimation.
Strength, carbonation, chloride, pollutant and moisture values cannot be invented.
```

### Must Remain Unknown

```text
actual concrete strength
chloride content
carbonation depth
pollutant content
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

```yaml
component_typology: mixed_slab_beam_column_slice
reinforcement_scan: partial_or_missing
```

### Geometry Generator Output

```yaml
candidate_rebar_relevant_zones:
  - slab_zone
  - beam_downstand_zone
  - slab_beam_transition
  - beam_column_transition
  - column_zone
generated_no_drill_candidate_zones:
  - slab_beam_transition
  - beam_column_transition
  - column_head_region
```

### System Output

```yaml
reinforcement_position_status: partial_or_unknown
main_reinforcement_direction: inferred_x_axis_for_slab_and_beam
secondary_reinforcement_direction: inferred_y_axis_for_slab
cover_status: unknown
rebar_condition: unknown
corrosion_risk: unknown
no_drill_zones:
  - beam_column_transition
  - slab_beam_transition
  - column_head_region
  - unknown_rebar_zones
drill_approved_zones: []
anchor_approved_zones: []
```

### Proof

```text
Because reinforcement evidence is partial or missing, the system cannot approve drilling.
Generated connector zones become candidates, not approvals.
```

### Must Remain Unknown

```text
true reinforcement layout
approved anchor zones
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

```yaml
material_kind: reinforced_concrete
storage_context: outdoor_storage_or_unknown
condition_status: partial
```

### Geometry Generator Output

```yaml
exposed_face_candidates:
  - slab_top
  - beam_sides
  - column_sides
moisture_risk_geometry_candidates:
  - slab_top_if_exposed
  - column_base_if_in_contact_with_ground
damage_zone_geometry:
  - slab_corner_A
```

### System Output

```yaml
durability_status: requires_verification
carbonation_risk: unknown
chloride_risk: unknown
corrosion_risk: unknown
freeze_thaw_risk: possible_if_unprotected_outdoor_storage
moisture_exposure_risk: medium_if_uncovered
estimated_remaining_service_life: engineering_required
repair_requirement: local_edge_repair_review
protection_requirement: weather_protection_required
```

### Proof

```text
Outdoor storage and exposed damaged edges increase durability risk.
Remaining service life cannot be calculated without material tests.
```

### Must Remain Unknown

```text
remaining service life
internal corrosion
chloride-induced risk
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

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
original_function: slab_beam_column_zone_candidate
```

### Geometry Generator Output

```yaml
structural_geometry:
  slab_bearing_edges:
    - slab_long_edge_left
    - slab_long_edge_right
  beam_end_zones:
    - beam_end_A
    - beam_end_B
  column_base_face: generated
  column_head_transition: generated
  span_candidate: x_axis
  plan_area_m2: 10.35
  net_volume_m3: 2.612
```

### System Output

```yaml
structural_role: composite_structural_candidate
load_bearing_status: engineering_required
self_weight_kN: 64.07
self_weight_kN_m2: 6.19
allowed_support_types:
  - engineered_wall_top_support_at_slab_edges
  - engineered_beam_end_support
  - engineered_column_base_support
  - steel_support_or_adapter_if_engineered
allowed_span_direction: inferred_x_axis
maximum_reuse_span_candidate_mm: 4500
known_load_capacity: unknown
capacity_evidence_status: missing
required_proof_status: structural_proof_required
```

### Proof

```text
self_weight_kN =
6.53 t × 9.81
= 64.07 kN

self_weight_kN_m2 =
64.07 / 10.35
= 6.19 kN/m²
```

### Must Remain Unknown

```text
final load capacity
live load
punching resistance around column zone
moment and shear capacity
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

```yaml
component_typology: mixed_slab_beam_column_slice
project_connector_library: abbau_aufbau_connection_families
```

### Geometry Generator Output

```yaml
ports:
  - id: port-slab-edge-left
    port: slab-edge-bearing
    geometry_ref: slab_long_edge_left
  - id: port-slab-edge-right
    port: slab-edge-bearing
    geometry_ref: slab_long_edge_right
  - id: port-beam-end-A
    port: beam-end-bearing
    geometry_ref: beam_end_A
  - id: port-beam-end-B
    port: beam-end-bearing
    geometry_ref: beam_end_B
  - id: port-column-base
    port: column-base-bearing
    geometry_ref: column_base_face
  - id: port-column-head-transition
    port: internal-beam-column-transition
    geometry_ref: beam_column_transition
  - id: port-service-top
    port: service-penetration-candidate
    geometry_ref: slab_top_service_zone
```

### System Output

```yaml
AA_connector_families_available:
  foundation_baseplate:
    - Schraubanker
  baseplate_wall:
    - nachtraeglich_montierte_Edelstahldorne
    - Winkelverbinder
  baseplate_column:
    - nachtraeglich_montierter_Edelstahldorn
    - Winkelverbinder
  wall_slab:
    - nachtraeglicher_Bewehrungsanschluss_und_Verguss
    - Schraubanker_mit_Flachstahlhalter
  column_slab:
    - nachtraeglich_montierter_Edelstahldorn
    - Winkelverbinder
    - Bewehrungsanschluss_und_Verguss_auf_neuem_Stahlbetontraeger
    - Auflager_auf_Stahltraeger

connector_options_by_port:
  slab-edge-bearing:
    compatible_ports:
      - wall-top-bearing
      - beam-top-bearing
    status: engineering_required_due_to_rebar_uncertainty

  column-base-bearing:
    compatible_ports:
      - baseplate-column-port
      - foundation-column-port
    status: engineering_required

  beam-end-bearing:
    compatible_ports:
      - wall-top-bearing
      - column-head-bearing
      - steel-support
    status: engineering_required_project_specific

  internal-beam-column-transition:
    status: internal_monolithic_zone_not_external_connector
```

### Proof

```text
Geometry generator creates ports.
System maps each port to Abbau/Aufbau connector families.
Because reinforcement and capacity are missing, all structural connectors remain engineering_required.
```

### Must Remain Unknown

```text
connector capacity
approved drilling zones
final reversibility
final fire treatment
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

```yaml
component_typology: mixed_slab_beam_column_slice
rebar_scan: partial_or_missing
project_drilling_defaults: available
```

### Geometry Generator Output

```yaml
candidate_drilling_zones:
  - slab_edge_zones
  - beam_side_zones
  - column_base_zone
forbidden_geometry_candidates:
  - slab_beam_transition
  - beam_column_transition
  - damaged_slab_corner_A
```

### System Output

```yaml
approved_drilling_zones: []
forbidden_drilling_zones:
  - beam_column_transition
  - slab_beam_transition
  - damaged_slab_corner_A
unknown_drilling_zones:
  - slab_edge_zones
  - beam_side_zones
  - column_base_zone
approved_anchor_zones: []
rebar_conflict_status: unknown
scan_confidence: partial_or_missing
```

### Proof

```text
No approved drilling zone can be produced because reinforcement evidence is incomplete.
Generated connector zones are candidates, not approvals.
```

### Must Remain Unknown

```text
actual safe drilling zones
anchor pull-out capacity
hidden rebar conflicts
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

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
fire_document: missing
```

### Geometry Generator Output

```yaml
fire_relevant_surface_candidates:
  - slab_underside_if_ceiling
  - beam_sides_and_bottom_if_exposed
  - column_sides_if_exposed
connector_exposure_candidates:
  - slab_edge_connectors
  - column_base_connectors
  - beam_end_supports
```

### System Output

```yaml
material_fire_class: non_combustible_material_assumption
known_fire_resistance: unknown
evidence_status: project_context_required
exposed_steel_warning: conditional
fire_cover_required_if:
  - angle_connector_used_in_fire_relevant_assembly
  - steel_support_used_without_fire_protection
  - exposed_anchor_or_flat_steel_holder_in_fire_context
```

### Proof

```text
Concrete material class does not prove the fire resistance of the new assembly.
Abbau/Aufbau connector details show fire-cover relevance especially for angle connectors and steel supports.
```

### Must Remain Unknown

```text
actual fire resistance rating
compartment compliance
connector fire resistance
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

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
exposure_context: unknown
project_thermal_defaults:
  lambda_reinforced_concrete_W_mK: 2.3
```

### Geometry Generator Output

```yaml
thicknesses:
  slab_thickness_m: 0.18
thermal_bridge_geometry_candidates:
  - slab_edges
  - beam_downstand_if_crossing_envelope
  - column_zone_if_crossing_envelope
surface_areas: generated
```

### System Output

```yaml
thermal_conductivity_W_mK: 2.3
density_t_m3: 2.5
rough_U_value_status: precheck_only
envelope_relevance: requires_project_context
thermal_bridge_zones: conditional
moisture_risk: conditional
acoustic_relevance: high_mass_component
```

### Proof

```text
R_concrete =
0.18 / 2.3
= 0.078 m²K/W

The rough U-value is not a final proof because insulation and full assembly are missing.
```

### Must Remain Unknown

```text
final U-value
thermal bridge Psi-value
moisture safety
actual acoustic rating
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

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

### Geometry Generator Output

```yaml
plan_area_m2: 10.35
volume_m3: 2.612
```

### System Output

```yaml
mass_per_area_kg_m2: 630.98
mass_relevance: high
airborne_sound_data: unknown
impact_sound_data: unknown
acoustic_evidence_status: missing
recommended_acoustic_use: potential_massive_separating_or_exposed_structural_element
acoustic_warning: acoustic_performance_requires_assembly_context
```

### Proof

```text
mass per area =
6531 kg / 10.35 m²
= 630.98 kg/m²
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

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
service_context: unknown
```

### Geometry Generator Output

```yaml
existing_openings: []
service_zone_candidates:
  - slab_top_service_zone
  - slab_edge_service_zone
blocked_service_zone_candidates:
  - beam_column_transition
  - column_zone
  - slab_beam_transition
```

### System Output

```yaml
existing_service_openings: []
approved_service_zones: []
blocked_service_zones:
  - beam_column_transition
  - column_zone
  - unknown_rebar_zones
possible_cable_penetrations: requires_rebar_scan
possible_pipe_penetrations: requires_rebar_scan_and_structural_review
core_drilling_allowed: false
core_drilling_blocked: true
rebar_scan_required_for_services: true
```

### Proof

```text
No existing service openings are generated.
New penetrations require reinforcement evidence and structural review.
```

### Must Remain Unknown

```text
actual TGA route fit
safe core drilling
fire/acoustic sealing detail
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

```yaml
component_typology: mixed_slab_beam_column_slice
base_geometry_reference: representations/AA_MIX_001/base.glb
material_kind: reinforced_concrete
storage_location: storage-yard-01
```

### Geometry Generator Output

```yaml
transport_envelope:
  length_mm: 4500
  width_mm: 2300
  height_mm: 1500
center_of_gravity: generated
lifting_candidate_regions:
  - slab_top_lifting_region_candidate
  - beam_zone_lifting_region_candidate
storage_orientation_geometry:
  recommended_candidate: custom_support_frame_or_engineered_laying_position
assembly_access_zones:
  - slab_edges
  - beam_ends
  - column_base
```

### System Output

```yaml
current_storage_location: storage-yard-01
storage_position: MIX-A-01
recommended_storage_orientation: engineering_required_due_to_mixed_geometry
forbidden_storage_orientation:
  - unsupported_on_column_stump
  - standing_without_frame
weather_protection_required: true
separator_required: true
mass_t: 6.53
lifting_point_status: engineering_required
transport_mode: truck_40t_candidate
transport_readiness: partial
load_securing_required: true
damage_protection_required: true
temporary_bracing_requirement: likely_required_during_handling
installation_notes:
  - support_mixed_geometry_during_storage
  - do_not_stack_like_flat_slab_without_engineering
```

### Proof

```text
Abbau/Aufbau recommends storing elements in the orientation for which they were originally designed.
For a mixed element, neither pure slab nor pure column storage logic is sufficient.
```

### Must Remain Unknown

```text
safe lifting design
actual crane radius
final transport support frame
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

```yaml
storage_location: storage-yard-01
target_site_location: rebuild-site-01
transport_distance_km: 40
project_transport_factor_kgCO2eq_per_tkm: 0.05
```

### Geometry Generator Output

```yaml
transport_dimensions:
  length_mm: 4500
  width_mm: 2300
  height_mm: 1500
transport_envelope_status: generated
```

### System Output

```yaml
transport_mode: truck_40t_candidate
transport_distance_km: 40
transport_factor_kgCO2eq_per_tkm: 0.05
transport_gwp_kgCO2eq: 13.06
special_transport_required: check_required_due_to_height_and_support_frame
protection_requirement: required
load_securing_note: required_for_reclaimed_concrete_composite
```

### Proof

```text
transport_gwp =
6.53 t × 40 km × 0.05 kg CO₂-eq/tkm
= 13.06 kg CO₂-eq
```

### Must Remain Unknown

```text
actual route restrictions
actual permit requirement
actual emissions without route/mode confirmation
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

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
project_lca_defaults:
  transport_factor_kgCO2eq_per_tkm: 0.05
  new_precast_concrete_reference_kgCO2eq_per_t: 171.7
transport_distance_km: 40
```

### Geometry Generator Output

```yaml
volume_m3: 2.612
surface_area: generated
dimensions: generated
```

### System Output

```yaml
material: reinforced_concrete
mass_t: 6.53
reused_mass_t: 6.53
a1_a3_reuse_assumption_kgCO2eq_per_t: 0
transport_gwp_kgCO2eq: 13.06
new_equivalent_reference: new_20cm_precast_concrete_slab_reference_for_GWP_precheck
new_equivalent_gwp_kgCO2eq_per_t: 171.7
avoided_gwp_potential_kgCO2eq: 1121.31
simple_net_precheck_before_connector_adapter_kgCO2eq: 1108.25
lca_status: precheck_only
generic_dataset_status: required_for_full_LCA
environmental_indicators:
  gwp: partial
  odp: unknown
  pocp: unknown
  ap: unknown
  ep: unknown
  primary_energy: unknown
  fresh_water: unknown
```

### Proof

```text
avoided_gwp_potential =
6.53 × 171.7
= 1121.31 kg CO₂-eq

simple net precheck =
1121.31 - 13.06
= 1108.25 kg CO₂-eq before connector/adapter impacts
```

### Must Remain Unknown

```text
full LCA
connector-specific impact
adapter material impact
module B/C/D impacts
non-GWP indicators without datasets
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

```yaml
component_id: AA_MIX_001
file_references:
  base_geometry: available
  damage_photos: optional
  rebar_scan: partial_or_missing
```

### Geometry Generator Output

```yaml
generated_files:
  - generated/AA_MIX_001/physical.glb
  - generated/AA_MIX_001/structural-zones.json
  - generated/AA_MIX_001/energy-faces.json
  - generated/AA_MIX_001/semantic-zones.json
  - generated/AA_MIX_001/ports-and-zones.json
  - generated/AA_MIX_001/logistics-geometry.json
```

### System Output

```yaml
documents:
  catalogue_sheet: generated
  sketch: generated_preview
  photos: optional_or_partial
  laser_scan: unknown
  bim_model: unavailable
  concrete_test_report: missing
  rebar_scan: partial_or_missing
  damage_report: partial_or_missing
  transport_document: missing
  storage_document: partial
  lca_document: precheck_generated
  approval_document: missing
```

### Proof

```text
Generated geometry files can be registered as documents,
but they do not replace concrete tests, rebar scans, or approval documents.
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

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
```

### Geometry Generator Output

```yaml
geometry_complete: true
openings_complete: true
connector_zones_complete: true
logistics_geometry_complete: true
energy_geometry_complete: true
semantic_geometry_complete: true
```

### System Output

```yaml
completeness:
  identity: complete_for_hypothetical_example
  geometry: complete
  mass: estimated
  openings: complete_no_openings_detected
  concrete: missing
  reinforcement: partial_or_missing
  damage: partial_or_missing
  connector_zones: generated_medium_confidence
  logistics: partial
  lca: precheck_only
  fire: requires_project_context
  building_physics: requires_project_context
  services: partial
overall_status: partial_engineering_required
```

### Proof

```text
Geometry can be complete while evidence is incomplete.
This is the key separation between generated geometry and proven material performance.
```

### Must Remain Unknown

```text
full structural evidence
fire rating
energy compliance
approved drilling zones
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

```yaml
generated_geometry: complete
evidence_status:
  concrete: missing
  rebar: partial_or_missing
  damage: partial_or_missing
  fire: missing
  lca: precheck_only
```

### Geometry Generator Output

```yaml
bearing_zones:
  - slab_long_edge_left
  - slab_long_edge_right
  - beam_end_A
  - beam_end_B
  - column_base_face
damage_zone_candidates:
  - slab_corner_A
connector_zones: generated
```

### System Output

```yaml
pool_warnings:
  - missing_concrete_strength_test
  - incomplete_or_missing_rebar_scan
  - no_approved_drilling_zones
  - missing_chloride_test
  - possible_edge_damage_at_slab_corner_A
  - unknown_lifting_points
  - missing_fire_rating
  - LCA_full_dataset_missing
  - do_not_drill_without_verification
  - do_not_use_damaged_slab_corner_as_primary_bearing
  - mixed_element_requires_custom_storage_and_lifting_review
```

### Proof

```text
Warnings are created by the system from:
generated zones + evidence completeness + Abbau/Aufbau project rules.
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

```yaml
generated_representations: complete
system_evidence_status: partial
project_rule_library: abbau_aufbau
```

### Geometry Generator Output

```yaml
readiness_geometry:
  geometry_interface_ready: true
  structural_zone_ready: true
  port_ready: true
  opening_ready: true
  energy_geometry_ready: true
  logistics_geometry_ready: true
```

### System Output

```yaml
ready_rules:
  - identity_check
  - stock_availability_check
  - basic_geometry_check
  - mixed_typology_detection
  - pair_type_precheck
  - port_compatibility_precheck
  - opening_detection_check
  - mass_and_transport_precheck
  - LCA_precheck

rules_needing_more_evidence:
  - full_structural_capacity_check
  - anchor_drilling_check
  - approved_connector_capacity_check
  - fire_rating_check
  - thermal_envelope_check
  - lifting_design_check
  - full_LCA_dataset_check

blocked_actions:
  - drilling_into_transition_zones
  - drilling_without_rebar_scan
  - using_component_as_simple_slab_without_mixed_typology
  - using_damaged_corner_as_primary_bearing
  - approving_structural_load_capacity_without_proof

default_status_if_used:
  connection_status: warning_or_engineering_required
  reason: geometry_ready_but_evidence_incomplete
```

### Proof

```text
The geometry generator makes the component usable for spatial design and prechecks.
The system prevents false approval by requiring evidence for structural, drilling,
fire, lifting, and full LCA decisions.
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
data and generated representations of AA_MIX_001

Connection Passport =
result of connecting AA_MIX_001 to another piece

Rule Checker Panel =
active validation state of the current design

Design Dashboard =
whole-design scores and preference ranking
```

---

# 8. Final Verified Summary

## 8.1 Concrete Parts from Abbau/Aufbau

```text
Confirmed catalogue example:
DE_1OG_001
4500 × 2300 × 180 mm
1.863 m³
ca. 4.1 t

Confirmed catalogue fields:
ID, sketch, dimensions, opening dimensions, volume, mass,
optional concrete and reinforcement investigation results.

Confirmed tracking logic:
ID marking, QR, BIM, RFID possible.

Confirmed LCA values:
0.05 kg CO₂-eq/tkm transport factor
171.7 kg CO₂-eq/t new 20 cm precast concrete slab reference
A1-A3 reused element GWP can be set to 0 kg CO₂-eq/t when no reused dataset exists.

Confirmed connector families:
Schraubanker
Edelstahldorn
Winkelverbinder
nachträglicher Bewehrungsanschluss + Verguss / Injektionsmörtel
Schraubanker mit Flachstahlhalter
Auflager auf Stahlträger
```

## 8.2 Hypothetical Parts

```text
AA_MIX_001 itself is hypothetical.
The beam zone and column stump dimensions are generated example geometry.
The structural role is not approved.
The connector zones are candidates.
The drilling zones are not approved.
The LCA result is precheck only.
```

## 8.3 Evidence Still Required

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
lifting design
connector capacity
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
