# Piece Detail Panel / Bauteilpass Interface

**Source:** Bauteilkatalog / Bauteilpass  
**Scope:** Only collected data from the Bauteilpool.  
**Not included:** Checker results, current connection validity, cluster status, or design scoring.

```text
Click on Piece
→ open Bauteilpass panel
→ show all collected pool data for this real component
```

---

## 0. Header / Quick Summary

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

Example:

```text
ID: DE_1OG_001
Kind: Deckenplatte / slab
Material: Stahlbeton
Status: available / placed / reserved / blocked
Dimensions: 4500 × 2300 × 180 mm
Mass: 4.1 t
Storage: Lagerplatz A-03-02
Tracking: QR-DE_1OG_001
```

---

## 1. Semio Binding

This links the physical component to the Semio data model.

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

Visible fields:

```text
semio.kit.id
semio.kit.name
semio.type.id
semio.type.name
semio.type.kind
semio.type.parent
semio.type.stock.total
semio.type.stock.available
semio.type.stock.unit
semio.type.location
semio.attributes
semio.qualities
semio.representations
semio.connectors
```

---

## 2. Identity + Traceability

This describes the component as a real, unique object.

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

Visible fields:

```text
identity.component_id
identity.name
identity.element_kind
identity.material_kind
identity.source_project
identity.source_building_id
identity.source_level
identity.source_zone
identity.original_function
identity.original_orientation
identity.tracking.method
identity.tracking.qr_code
identity.tracking.rfid
identity.tracking.bim_guid
identity.tracking.external_reference
identity.physical_marking_status
```

---

## 3. Pool Availability

This is still pool data, not checker output.

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

Visible fields:

```text
availability.state
availability.stock_total
availability.stock_available
availability.reserved_for_design
availability.used_as_piece_ids
availability.blocked_reason
availability.current_storage_location
availability.storage_position
```

States:

```text
available
reserved
placed
connected
locked
blocked
unknown
```

---

## 4. Classification

This describes what the component is allowed to be understood as.

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

Visible fields:

```text
classification.primary_kind
classification.secondary_kinds
classification.material_family
classification.structural_family
classification.allowed_design_roles
classification.disallowed_design_roles
classification.semantic_tags
classification.reuse_category
classification.risk_category
```

Example:

```text
Primary kind: slab
Allowed roles:
- floor slab
- roof slab
- horizontal diaphragm if engineered

Disallowed roles:
- wall
- column
- beam
```

---

## 5. Geometry Overview

This is the basic geometry collected in the Bauteilkatalog.

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

Visible fields:

```text
geometry.units
geometry.length
geometry.width
geometry.height
geometry.bounding_box
geometry.volume_gross
geometry.volume_net
geometry.mass
geometry.density
geometry.center_of_gravity
geometry.local_x
geometry.local_y
geometry.local_z
geometry.original_top_face
geometry.original_bottom_face
geometry.geometry_tolerance
geometry.placement_tolerance
geometry.joint_gap_min
geometry.joint_gap_max
```

---

## 6. Geometry Representations

The interface should show each available geometry abstraction separately.

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

Visible fields per representation:

```text
representation.id
representation.name
representation.tags
representation.kind
representation.url
representation.file_type
representation.lod
representation.description
representation.created_at
representation.source
representation.confidence
```

Recommended UI tabs:

```text
Geometry
│
├── Physical
├── Structural
├── Energy / Envelope
├── Semantic
├── Connector Zones
├── Logistics
├── Sketch
└── Photos / Scans
```

---

## 7. Physical Geometry

This is used for visual placement and collision.

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

Visible fields:

```text
physical_geometry.shape_kind
physical_geometry.mesh_or_solid_reference
physical_geometry.length
physical_geometry.width
physical_geometry.height
physical_geometry.edges
physical_geometry.faces
physical_geometry.openings
physical_geometry.cutouts
physical_geometry.irregularities
physical_geometry.damaged_edges
physical_geometry.damaged_faces
physical_geometry.tolerance
```

---

## 8. Structural Geometry

This is geometry interpreted for load-bearing logic.

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

Visible fields:

```text
structural_geometry.structural_role
structural_geometry.preferred_span_direction
structural_geometry.secondary_span_direction
structural_geometry.main_reinforcement_direction
structural_geometry.support_edges
structural_geometry.bearing_zones
structural_geometry.point_support_zones
structural_geometry.line_support_zones
structural_geometry.load_direction
structural_geometry.allowed_support_conditions
structural_geometry.disallowed_support_conditions
structural_geometry.minimum_bearing_length
structural_geometry.structural_thickness
structural_geometry.structural_openings
```

---

## 9. Energy / Envelope Geometry

This is used when the component may become part of the envelope.

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

Visible fields:

```text
energy_geometry.envelope_relevance
energy_geometry.exterior_faces
energy_geometry.interior_faces
energy_geometry.ground_contact_faces
energy_geometry.roof_faces
energy_geometry.thermal_boundary_faces
energy_geometry.insulation_faces
energy_geometry.thermal_bridge_zones
energy_geometry.moisture_risk_zones
energy_geometry.u_value_relevant_surfaces
```

---

## 10. Semantic / Architectural Geometry

This describes architectural meaning, not only shape.

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

Visible fields:

```text
semantic_geometry.inside_side
semantic_geometry.outside_side
semantic_geometry.room_facing_faces
semantic_geometry.facade_facing_faces
semantic_geometry.visible_faces
semantic_geometry.hidden_faces
semantic_geometry.original_use_context
semantic_geometry.potential_new_uses
semantic_geometry.spatial_role
semantic_geometry.room_boundary_role
semantic_geometry.facade_rhythm_role
semantic_geometry.visible_reuse_potential
semantic_geometry.surface_expression_value
```

---

## 11. Openings + Penetrations

Collected openings from the pool.

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

Visible fields:

```text
openings.id
openings.kind
openings.position
openings.width
openings.height
openings.diameter
openings.depth
openings.original_purpose
openings.edge_distance
openings.rebar_relation
openings.service_reuse_allowed
openings.status
openings.notes
```

Opening status:

```text
existing
usable
blocked
requires_verification
unknown
```

---

## 12. Surface + Edge Condition

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

Visible fields:

```text
condition.top_face
condition.bottom_face
condition.side_faces
condition.edges
condition.spalling
condition.cracks
condition.exposed_rebar
condition.surface_contamination
condition.repair_marks
condition.visual_quality
condition.visible_reuse_quality
```

---

## 13. Damage Records

Each damage should be clickable.

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

Visible fields:

```text
damage.id
damage.kind
damage.location
damage.affected_face
damage.affected_edge
damage.severity
damage.length
damage.width
damage.depth
damage.photo_reference
damage.repair_status
damage.rule_relevance
damage.notes
```

Damage types:

```text
crack
spalling
edge damage
surface damage
corrosion mark
exposed reinforcement
deformation
unknown
```

---

## 14. Concrete Evidence

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

Visible fields:

```text
concrete.compressive_strength
concrete.compressive_strength_unit
concrete.tensile_strength
concrete.e_modulus
concrete.density
concrete.carbonation_depth
concrete.chloride_content
concrete.pollutant_content
concrete.moisture_status
concrete.test_method
concrete.test_date
concrete.test_document
concrete.evidence_status
concrete.confidence_level
```

Evidence status:

```text
tested
estimated
derived
unknown
not_required
requires_verification
```

---

## 15. Reinforcement Evidence

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

Visible fields:

```text
reinforcement.position_status
reinforcement.main_direction
reinforcement.secondary_direction
reinforcement.cover_top
reinforcement.cover_bottom
reinforcement.cover_sides
reinforcement.scan_reference
reinforcement.condition_status
reinforcement.corrosion_risk
reinforcement.no_drill_zones
reinforcement.drill_approved_zones
reinforcement.anchor_approved_zones
reinforcement.unknown_zones
reinforcement.evidence_status
```

---

## 16. Durability + Restnutzungsdauer

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

Visible fields:

```text
durability.status
durability.carbonation_risk
durability.chloride_risk
durability.corrosion_risk
durability.freeze_thaw_risk
durability.moisture_exposure_risk
durability.remaining_service_life_years
durability.repair_required
durability.protection_required
durability.notes
```

---

## 17. Structural Data

This is collected or estimated data from the pool, not the current design result.

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

Visible fields:

```text
structural.primary_role
structural.load_bearing_status
structural.self_weight
structural.allowed_support_types
structural.allowed_bearing_zones
structural.allowed_span_direction
structural.maximum_reuse_span
structural.known_load_capacity
structural.capacity_evidence_status
structural.required_proof_status
structural.original_structural_function
```

---

## 18. Connector / Interface Data

This is one of the most important interface sections.

For each connector:

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

Visible fields:

```text
connectors.id
connectors.name
connectors.kind
connectors.port
connectors.compatible_ports
connectors.mandatory
connectors.direction
connectors.geometry_reference
connectors.allowed_connection_roles
connectors.allowed_connector_systems
connectors.min_bearing_length
connectors.max_gap
connectors.edge_distance_requirement
connectors.drilling_permission
connectors.requires_fire_check
connectors.requires_structural_check
connectors.requires_thermal_check
connectors.requires_service_check
connectors.reversibility_preference
```

Example connector systems visible:

```text
post_installed_rebar_grout
screw_anchor_flat_steel_holder
stainless_dowel
angle_connector
steel_beam_support
dry_bearing_with_restraint
approved_core_drilling
existing_opening
```

---

## 19. Bohrzonen / No-Drill Zones

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

Visible fields:

```text
drilling.approved_zones
drilling.forbidden_zones
drilling.unknown_zones
drilling.approved_anchor_zones
drilling.forbidden_anchor_zones
drilling.minimum_edge_distance
drilling.minimum_anchor_spacing
drilling.cover_requirement
drilling.rebar_conflict_status
drilling.scan_confidence
```

---

## 20. Fire Data

Only collected component-level fire data.

```text
Material fire class
Known fire resistance
Evidence status
Fire-relevant surfaces
Connector fire warning conditions
Exposed steel warning
Fire cover requirement if connected
```

Visible fields:

```text
fire.material_class
fire.fire_resistance_rating
fire.evidence_status
fire.fire_relevant_surfaces
fire.connector_fire_conditions
fire.exposed_steel_warning
fire.fire_cover_required_if
fire.notes
```

---

## 21. Building Physics Data

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

Visible fields:

```text
building_physics.thermal_conductivity
building_physics.density
building_physics.specific_heat_capacity
building_physics.u_value
building_physics.envelope_relevance
building_physics.insulation_requirement_if_envelope
building_physics.thermal_bridge_zones
building_physics.moisture_risk
building_physics.ground_contact_suitability
building_physics.roof_suitability
building_physics.acoustic_relevance
```

---

## 22. Acoustic Data

```text
Mass relevance
Airborne sound data
Impact sound data
Acoustic evidence status
Recommended acoustic use
Acoustic warning
```

Visible fields:

```text
acoustics.mass_relevance
acoustics.airborne_sound_value
acoustics.impact_sound_value
acoustics.evidence_status
acoustics.recommended_use
acoustics.warning
```

---

## 23. TGA / Services Data

Only available pool-level service information.

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

Visible fields:

```text
services.existing_openings
services.approved_service_zones
services.blocked_service_zones
services.cable_penetration_possible
services.pipe_penetration_possible
services.core_drilling_allowed
services.core_drilling_blocked
services.rebar_scan_required
```

---

## 24. Logistics Data

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

Visible fields:

```text
logistics.current_storage_location
logistics.storage_position
logistics.recommended_storage_orientation
logistics.forbidden_storage_orientations
logistics.weather_protection_required
logistics.separator_required
logistics.mass
logistics.lifting_point_status
logistics.lifting_points
logistics.transport_mode
logistics.transport_ready
logistics.load_securing_required
logistics.damage_protection_required
logistics.temporary_bracing_required
logistics.assembly_access_zones
logistics.installation_notes
```

---

## 25. Transport Data

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

Visible fields:

```text
transport.mode
transport.distance_km
transport.factor_kgco2e_per_tkm
transport.emissions_status
transport.maximum_transport_size
transport.special_transport_required
transport.protection_required
transport.load_securing_note
```

---

## 26. LCA / Ökobilanz Data

Only component-level collected pool data, not current connection result.

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

Visible fields:

```text
lca.material
lca.mass_t
lca.reused_mass_t
lca.a1_a3_reuse_assumption
lca.transport_factor
lca.transport_distance
lca.new_equivalent_reference
lca.new_equivalent_gwp
lca.avoided_gwp_potential
lca.epd_dataset
lca.oekobaudat_dataset
lca.generic_dataset_status
lca.completeness_status
lca.indicators.gwp
lca.indicators.odp
lca.indicators.pocp
lca.indicators.ap
lca.indicators.ep
lca.indicators.primary_energy
lca.indicators.fresh_water
lca.indicators.resource_use
```

---

## 27. Documentation

All linked evidence documents.

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

Visible fields:

```text
documents.catalogue_sheet
documents.sketch
documents.photos
documents.laser_scan
documents.bim_model
documents.concrete_test_report
documents.rebar_scan
documents.damage_report
documents.transport_document
documents.storage_document
documents.lca_document
documents.epd_reference
documents.oekobaudat_reference
documents.approval_document
documents.notes
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

---

## 28. Evidence Completeness

This is still based only on collected pool data.

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

Visible fields:

```text
completeness.identity
completeness.geometry
completeness.mass
completeness.openings
completeness.concrete
completeness.reinforcement
completeness.damage
completeness.connector_zones
completeness.logistics
completeness.lca
completeness.fire
completeness.building_physics
completeness.services
```

Statuses:

```text
complete
partial
missing
not_required
requires_project_context
```

---

## 29. Pool-Level Warnings

These are not checker results from a connection.  
They are warnings already attached to the component passport.

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

---

## 30. Rule-Checker Readiness

This tells which future rules can run from the collected pool data.

```text
Ready rules
Rules needing more evidence
Blocked actions
Default status if used
Missing evidence list
```

Visible fields:

```text
rule_readiness.ready_rules
rule_readiness.rules_requiring_more_evidence
rule_readiness.blocked_actions
rule_readiness.default_connection_status_when_used
rule_readiness.missing_evidence
```

Example:

```text
Ready:
- identity check
- geometry check
- mass check
- bearing-zone precheck

Needs evidence:
- full anchor check
- fire resistance check
- thermal envelope check

Blocked:
- drill outside approved zone
- use damaged edge as bearing
```

---

## 31. What Should Not Be Shown in This Panel

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

Those belong to the **Connection Passport** or **Rule Checker Panel**, not the clicked Piece’s Bauteilpass.

---

## Minimal UI Tab Structure

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

This is the full set of details visible when the user clicks a Piece, limited strictly to data collected from the Bauteilpool / Bauteilkatalog.
