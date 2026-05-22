# Playground Rule Checker  
## Connecting the Monolithic Mixed Component `AA_MIX_001` with Another Component

**Document type:** Rule-checker specification for the Playground.  
**Project frame:** Abbau/Aufbau-inspired reclaimed reinforced-concrete design workflow.  
**Component A:** `AA_MIX_001` — hypothetical monolithic mixed slab–beam–column pool element.  
**Component B:** any other placed reclaimed component from the Bauteilkatalog.

---

# 0. Core Idea

The Playground rule checker runs when the user places `AA_MIX_001` and starts connecting it to another component.

```text
User places AA_MIX_001
+ User places Component B
+ User selects or snaps Port A to Port B
        ↓
Rule Checker reads:
- generated geometry of both components
- ports and connector zones
- Bauteilpass data
- evidence status
- project rule library
- Abbau/Aufbau connector families
        ↓
Rule Checker returns:
valid / warning / invalid / engineering_required
```

The checker does **not** treat `AA_MIX_001` as a simple slab.  
It treats it as a **mixed monolithic component** with multiple sub-zones:

```text
AA_MIX_001
│
├── slab zone
├── downstand beam zone
├── column stump / capital zone
├── slab-beam transition zone
└── beam-column transition zone
```

---

# 1. Rule-Checker Boundary

## 1.1 What the Rule Checker Uses

The rule checker uses data from:

```text
Component A Bauteilpass
Component B Bauteilpass
generated geometry representations
connector-zone geometry
ports
evidence status
material status
project defaults
Abbau/Aufbau connector library
target design preferences
current Playground placement graph
```

## 1.2 What the Rule Checker Produces

```text
connection status
rule result tree
connection passport
warnings
blocked actions
required evidence
allowed connector families
disallowed connector families
suggested next actions
local cluster update
```

## 1.3 What the Rule Checker Does Not Produce

```text
new geometry
raw component data
manual approval
final structural proof
fire approval
full LCA proof
building permit approval
```

---

# 2. Actors in the Playground

## 2.1 Component A: Monolithic Mixed Element

```yaml
component_A:
  id: AA_MIX_001
  typology: mixed_slab_beam_column_slice
  material: reinforced_concrete
  status: hypothetical_abbau_aufbau_style_component
  geometry_status: generated
  evidence_status: partial_engineering_required
  mass_t: 6.53
  main_sub_zones:
    - slab_zone
    - beam_downstand_zone
    - column_stump_zone
    - slab_beam_transition
    - beam_column_transition
```

## 2.2 Component B: Generic Reclaimed Component

Component B can be any other placed component from the pool:

```text
wall panel
slab
beam
column
mushroom column
baseplate
foundation piece
adapter / new mediator piece
facade panel
stair / landing
```

Example placeholders:

```yaml
component_B:
  id: B_SELECTED_BY_USER
  typology: wall_panel | slab | beam | column | baseplate | adapter
  material: reinforced_concrete | steel | hybrid
  geometry_status: generated
  evidence_status: varies_by_component
```

## 2.3 Connection Candidate

A connection candidate is created when the user tries to join one port to another:

```yaml
connection_candidate:
  id: CANDIDATE_001
  component_A: AA_MIX_001
  port_A: selected_or_snapped_port
  component_B: B_SELECTED_BY_USER
  port_B: selected_or_snapped_port
  placement_context:
    relative_position: generated_from_playground
    rotation: generated_from_playground
    contact_area: generated_from_geometry
    gap: generated_from_geometry
    overlap: generated_from_geometry
```

---

# 3. Generated Ports of `AA_MIX_001`

The geometry generator creates candidate ports.  
The rule checker then decides whether a connection through each port is allowed, risky, or blocked.

## 3.1 Port Tree

```text
AA_MIX_001 Ports
│
├── P-A1 slab-edge-bearing-left
├── P-A2 slab-edge-bearing-right
├── P-A3 slab-top-service-zone
├── P-A4 slab-envelope-face
│
├── P-A5 beam-end-bearing-A
├── P-A6 beam-end-bearing-B
├── P-A7 beam-side-connector
│
├── P-A8 column-base-bearing
├── P-A9 column-head / capital-bearing
│
├── P-A10 internal-slab-beam-transition
└── P-A11 internal-beam-column-transition
```

## 3.2 Port Status Logic

| Port | Geometry role | External connection allowed? | Default checker status |
|---|---|---:|---|
| `slab-edge-bearing` | slab edge support | yes | `engineering_required` |
| `slab-top-service-zone` | service candidate | maybe | `blocked_until_rebar_scan` |
| `slab-envelope-face` | thermal / envelope face | yes, non-structural | `context_required` |
| `beam-end-bearing` | beam end support | yes | `engineering_required` |
| `beam-side-connector` | lateral restraint / adapter | maybe | `engineering_required` |
| `column-base-bearing` | vertical support base | yes | `engineering_required` |
| `column-head / capital-bearing` | support / slab-head zone | yes | `engineering_required` |
| `internal-slab-beam-transition` | internal monolithic zone | no external connector | `blocked` |
| `internal-beam-column-transition` | internal monolithic zone | no external connector | `blocked` |

## 3.3 Hard Rule

```text
Internal monolithic transition zones are not normal connector ports.

If the user tries to connect through:
- internal-slab-beam-transition
- internal-beam-column-transition

→ FAIL / blocked
```

Reason:

```text
These zones are structurally sensitive and may contain complex reinforcement.
They cannot be used as external connector areas without a dedicated engineering detail.
```

---

# 4. Component B Port Types

The rule checker reads Component B’s generated ports.

## 4.1 Common Component B Ports

```text
wall-top-bearing
wall-bottom-bearing
wall-side-joint
wall-face-connector

slab-edge-bearing
slab-top-service-zone
slab-envelope-face

beam-end-bearing
beam-top-bearing
beam-side-connector

column-base-bearing
column-head-bearing
column-side-stability-connector

baseplate-wall-port
baseplate-column-port
foundation-port

adapter-port
steel-support-port
thermal-envelope-interface
service-penetration
```

## 4.2 Port Compatibility Table

| `AA_MIX_001` Port A | Compatible Component B Ports | Typical pair type |
|---|---|---|
| `slab-edge-bearing` | `wall-top-bearing`, `beam-top-bearing`, `steel-support-port` | slab-wall / slab-beam / slab-steel |
| `beam-end-bearing` | `wall-top-bearing`, `column-head-bearing`, `steel-support-port` | beam-wall / beam-column / beam-steel |
| `column-base-bearing` | `baseplate-column-port`, `foundation-port`, `adapter-port` | column-base / column-foundation |
| `column-head / capital-bearing` | `slab-edge-bearing`, `slab-bottom-bearing`, `adapter-port` | column-slab / column-adapter |
| `slab-envelope-face` | `thermal-envelope-interface`, `insulation-layer`, `facade-zone` | envelope / non-structural |
| `slab-top-service-zone` | `service-penetration`, `service-route` | TGA / service |
| `beam-side-connector` | `adapter-port`, `steel-support-port`, `lateral-restraint-port` | lateral restraint / adapter |

---

# 5. Rule Checker Sequence

When the user connects `AA_MIX_001` to Component B, the checker runs this sequence:

```text
RC-0 Connection Intent
RC-1 Catalogue + Availability
RC-2 Geometry + Port Compatibility
RC-3 Evidence Gate
RC-4 Structural Role + Load Path
RC-5 Connector Family Selection
RC-6 Drilling / Rebar / No-Drill Check
RC-7 Fire Check
RC-8 Building Physics / Envelope Check
RC-9 TGA / Services Check
RC-10 Logistics / Buildability Check
RC-11 LCA / Ökobilanz Check
RC-12 Target Preference Weighting
RC-13 Local Cluster Update
RC-14 Connection Passport Output
```

---

# 6. RC-0 — Connection Intent

## Goal

Understand what the user is trying to do.

## Input

```yaml
user_action:
  component_A: AA_MIX_001
  selected_port_A: port_A
  component_B: B_SELECTED_BY_USER
  selected_port_B: port_B
  connector_preference: optional
  target_role: optional
```

## Rules

```text
Is the action a structural connection?
Is it a service penetration?
Is it an envelope contact?
Is it a temporary placement?
Is it an adapter request?
```

## Output

```yaml
connection_intent:
  kind: structural | service | envelope | logistics | unknown
  confidence: high | medium | low
```

## Example

```yaml
example:
  port_A: slab-edge-bearing
  port_B: wall-top-bearing
  intent: structural
```

---

# 7. RC-1 — Catalogue + Availability

## Goal

Check whether both components are real, available, and usable.

## Input

```yaml
component_A:
  id: AA_MIX_001
  stock_available: 1
  evidence_status: partial_engineering_required

component_B:
  id: B_SELECTED_BY_USER
  stock_available: value_from_catalogue
  evidence_status: value_from_catalogue
```

## Rules

```text
A and B must have valid IDs.
A and B must be available or already placed in this design.
A and B must not be duplicated beyond available stock.
A and B must have generated geometry.
A and B must have a Bauteilpass.
```

## Output

```yaml
RC-1:
  status: pass | warning | fail
  messages:
    - component_found
    - stock_available
    - geometry_available
    - evidence_partial
```

## Fail Conditions

```text
Component missing from catalogue
Component already used beyond stock
Component has no generated geometry
Component blocked in pool
```

---

# 8. RC-2 — Geometry + Port Compatibility

## Goal

Check whether the selected ports can geometrically and semantically meet.

## Input

```yaml
geometry:
  port_A_geometry
  port_B_geometry
  contact_area
  overlap
  gap
  orientation
  collision_status
  tolerance
```

## Rules

```text
Ports must be compatible.
Directions must be plausible.
Contact or bearing area must exist.
Gap must be inside tolerance or require adapter.
Components must not collide outside intended connection zones.
Connection must not occur through internal transition zones.
```

## Port Compatibility Rule

```yaml
if:
  port_A: slab-edge-bearing
  port_B: wall-top-bearing
then:
  pair_type: slab_wall
  geometry_check: allowed_candidate
```

```yaml
if:
  port_A: internal-beam-column-transition
then:
  status: fail
  reason: internal_transition_zone_not_external_connector
```

## Output

```yaml
RC-2:
  status: pass | warning | fail
  pair_type: slab_wall | beam_column | column_base | envelope | service | unknown
  geometry_result:
    contact_area: calculated
    overlap: calculated
    gap: calculated
    adapter_required: true | false
```

## Warning Conditions

```text
Compatible ports but insufficient bearing overlap
Compatible ports but gap exceeds direct connection tolerance
Compatible ports but adapter is needed
Orientation plausible but not ideal
```

---

# 9. RC-3 — Evidence Gate

## Goal

Prevent false approval when material or reinforcement evidence is missing.

## Input

```yaml
evidence:
  concrete_strength_A
  concrete_strength_B
  rebar_scan_A
  rebar_scan_B
  damage_records_A
  damage_records_B
  fire_document_A
  fire_document_B
```

## Rules

```text
If the connection transfers load → concrete strength evidence required.
If the connection drills, anchors, dowels, or cuts → rebar evidence required.
If the connection touches damaged zone → damage review required.
If the connector uses steel in fire-relevant context → fire detail required.
If connection is non-standard → engineering_required.
```

## Output

```yaml
RC-3:
  status: pass | warning | engineering_required | fail
  missing_evidence:
    - concrete_strength_test
    - full_rebar_scan
    - damage_review
    - fire_detail
```

## Hard Gate

```text
No drilling approval without reinforcement evidence.
```

For `AA_MIX_001`:

```yaml
default:
  drilling_status: blocked_until_rebar_scan
  structural_status: engineering_required
```

---

# 10. RC-4 — Structural Role + Load Path

## Goal

Check whether the connection creates a plausible local load path.

## Input

```yaml
structural:
  pair_type
  port_A_role
  port_B_role
  load_direction
  bearing_zone_A
  bearing_zone_B
  self_weight_A
  self_weight_B
  estimated_local_reaction
  structural_capacity_evidence
```

## Rules

```text
Load must have a plausible path.
Support component must be allowed to support.
Supported component must be allowed to bear on selected zone.
Mixed component must not be simplified as a flat slab.
Column / beam / slab zones must be treated separately.
Transition zones cannot be loaded or drilled without proof.
Accumulated loads from local cluster must be checked.
```

## Pair-Specific Checks

### A. `AA_MIX_001` slab edge → wall top

```text
Check slab edge bearing.
Check wall top bearing zone.
Check minimum bearing length.
Check damage on slab edge.
Check rebar if anchoring is proposed.
```

### B. `AA_MIX_001` beam end → column head

```text
Check beam end contact.
Check column head support.
Check eccentricity.
Check local crushing / bearing proof.
Check stability during assembly.
```

### C. `AA_MIX_001` column base → baseplate/foundation

```text
Check base contact.
Check vertical load path.
Check dowel / angle connector requirement.
Check column stump stability.
Check no drilling without rebar scan.
```

### D. `AA_MIX_001` column head / capital → slab

```text
Check local support geometry.
Check punching-sensitive region.
Check column-slab connector family.
Mark as engineering_required.
```

## Output

```yaml
RC-4:
  status: pass | warning | engineering_required | fail
  structural_role:
    pair_type: detected_pair
    load_path: plausible | not_plausible | engineering_required
    structural_proof_required: true
```

## Fail Conditions

```text
No bearing/contact where structural support is claimed
Load path ends in unsupported component
Connection through internal transition zone
Component B cannot support Component A
Component A used in incompatible role without adapter/proof
```

---

# 11. RC-5 — Connector Family Selection

## Goal

Map the detected pair type to possible Abbau/Aufbau connector families.

## Abbau/Aufbau Connector Families

```text
Foundation - Baseplate
→ Schraubanker

Baseplate - Wall
→ nachträglich montierte Edelstahldorne
→ Winkelverbinder

Baseplate - Column
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder

Wall - Slab
→ nachträglicher Bewehrungsanschluss + Verguss / Injektionsmörtel
→ Schraubanker mit Flachstahlhalter

Column - Slab
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder
→ Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
→ Auflager auf Stahlträger
```

## Mapping for `AA_MIX_001`

```yaml
connector_mapping:
  slab_edge_to_wall_top:
    pair_type: wall_slab
    candidate_connectors:
      - post_installed_rebar_grout
      - screw_anchor_flat_steel_holder
    default_status: engineering_required

  column_base_to_baseplate:
    pair_type: baseplate_column
    candidate_connectors:
      - stainless_dowel
      - angle_connector
    default_status: engineering_required

  column_head_to_slab:
    pair_type: column_slab
    candidate_connectors:
      - stainless_dowel
      - angle_connector
      - rebar_grout_on_new_concrete_beam
      - steel_beam_support
    default_status: engineering_required

  beam_end_to_support:
    pair_type: beam_support
    candidate_connectors:
      - steel_beam_support
      - project_specific_adapter
    default_status: engineering_required
```

## Output

```yaml
RC-5:
  status: warning | engineering_required | fail
  allowed_connector_families:
    - connector_family
  blocked_connector_families:
    - connector_family
  connector_evidence_required:
    - rebar_scan
    - structural_connector_proof
    - fire_detail_if_exposed_steel
```

## Hard Rules

```text
Connector family can be suggested, not approved.
Approval requires evidence and structural proof.

If connector requires drilling:
→ rebar scan required.

If connector exposes steel:
→ fire check required.

If connector adds material:
→ LCA connector material required.
```

---

# 12. RC-6 — Drilling / Rebar / No-Drill Check

## Goal

Check whether a proposed connector requires drilling, anchoring, doweling, or rebar connection.

## Input

```yaml
connector:
  type
  requires_drilling
  requires_anchor
  requires_rebar_connection
  requires_grout

geometry:
  drilling_zone_A
  drilling_zone_B
  no_drill_zones_A
  no_drill_zones_B
  edge_distances
  transition_zones

evidence:
  rebar_scan_A
  rebar_scan_B
```

## Rules

```text
No approved drilling without rebar scan.
No drilling in internal transition zones.
No drilling in damaged edge zones.
No drilling if edge distance is insufficient.
No anchor approval without connector product/detail proof.
```

## Output

```yaml
RC-6:
  status: pass | warning | fail | engineering_required
  drilling_status:
    A: blocked_until_rebar_scan
    B: depends_on_component_B
  no_drill_zones:
    - slab_beam_transition
    - beam_column_transition
    - damaged_slab_corner
```

## Fail Conditions

```text
User selects internal transition zone as anchor area
User drills into unknown reinforcement zone
User drills too close to damaged edge
User drills without required evidence
```

---

# 13. RC-7 — Fire Check

## Goal

Flag fire issues caused by reused concrete and connector systems.

## Input

```yaml
fire:
  material_A
  material_B
  fire_rating_A
  fire_rating_B
  connector_material
  exposed_steel
  fire_context
```

## Rules

```text
Concrete material is not enough to prove assembly fire rating.
Exposed steel connectors may require fire protection.
Weakest fire-relevant part governs the connection.
Fire check is required if connection is part of compartment, escape route, or fire-rated structure.
```

## Output

```yaml
RC-7:
  status: pass | warning | engineering_required
  fire_warnings:
    - exposed_steel_connector_requires_fire_detail
    - fire_rating_missing
```

## Typical Warning for `AA_MIX_001`

```text
If angle connector, steel support, screw anchor with flat steel holder, or exposed steel beam support is used:
→ fire detail required.
```

---

# 14. RC-8 — Building Physics / Envelope Check

## Goal

Check whether the connection affects energy, moisture, acoustic, or envelope performance.

## Input

```yaml
building_physics:
  envelope_context
  thermal_boundary_faces
  connector_crosses_envelope
  slab_edge_exposed
  moisture_exposure
  acoustic_target
```

## Rules

```text
If connection is interior and non-envelope → energy check may be not applicable.
If connection crosses envelope → thermal bridge warning.
If slab edge is exterior → insulation / U-value / moisture check.
If massive element is used in acoustic context → acoustic evidence required.
```

## Output

```yaml
RC-8:
  status: pass | warning | not_applicable | engineering_required
  warnings:
    - thermal_bridge_candidate
    - envelope_context_required
    - acoustic_performance_requires_assembly
```

## Important

```text
The Bauteilpass may contain a rough concrete-layer U-value precheck.
The rule checker must not treat this as final energy compliance.
```

---

# 15. RC-9 — TGA / Services Check

## Goal

Check whether the connection blocks or enables service routing.

## Input

```yaml
services:
  existing_openings_A
  existing_openings_B
  service_zone_A
  service_zone_B
  proposed_core_drilling
  rebar_status
```

## Rules

```text
Existing openings can be reused if not structurally conflicting.
New core drilling requires rebar scan.
No service drilling through column zone or transition zone by default.
No service drilling through bearing zone without engineering review.
```

## Output

```yaml
RC-9:
  status: pass | warning | fail | engineering_required
  service_result:
    existing_opening_reuse: true | false
    new_penetration_allowed: false_until_rebar_scan
```

## For `AA_MIX_001`

```text
No existing openings are assumed.
Service zones are only candidates.
Core drilling is blocked until reinforcement evidence exists.
```

---

# 16. RC-10 — Logistics / Buildability Check

## Goal

Check whether the connection can actually be assembled.

## Input

```yaml
logistics:
  component_A_mass
  component_B_mass
  lifting_status_A
  lifting_status_B
  access_to_connector
  storage_orientation
  assembly_sequence
  crane_context
```

## Rules

```text
Connector must remain accessible during assembly.
AA_MIX_001 cannot be handled like a flat slab.
Mixed geometry may need custom lifting frame.
Support component must be installed before the mixed component if it carries it.
Dry or reversible connectors may be preferred if target preference demands reversibility.
```

## Output

```yaml
RC-10:
  status: pass | warning | engineering_required
  buildability_warnings:
    - lifting_design_required
    - connector_access_must_remain_open
    - custom_support_frame_required
    - assembly_sequence_required
```

## Common Warning

```text
AA_MIX_001 has eccentric mixed geometry.
Check lifting, temporary support, and assembly sequence before approving placement.
```

---

# 17. RC-11 — LCA / Ökobilanz Check

## Goal

Check the environmental effect of using this connection.

## Input

```yaml
lca:
  reused_mass_A
  reused_mass_B
  transport_distance_A
  transport_distance_B
  connector_material
  adapter_material
  new_equivalent_reference
  dataset_status
```

## Rules

```text
Reused mass can be counted.
Transport impact can be calculated if distance and factor exist.
Avoided new-material potential can be estimated.
Connector and adapter material must be added.
Full LCA requires datasets.
```

## Base Formula

```text
connection_lca_precheck =
avoided_new_material_potential
- transport_impact
- connector_material_impact
- adapter_material_impact
```

## For `AA_MIX_001`

From the verified Bauteilpass example:

```yaml
AA_MIX_001:
  mass_t: 6.53
  transport_factor: 0.05 kg_CO2eq_per_tkm
  default_transport_distance_km: 40
  transport_gwp_kgCO2eq: 13.06
  avoided_gwp_potential_kgCO2eq: 1121.20
  simple_net_precheck_before_connector_adapter_kgCO2eq: 1108.14
```

## Output

```yaml
RC-11:
  status: pass | warning | engineering_required
  lca_result:
    reused_mass_added: calculated
    transport_gwp: calculated_if_distance_known
    connector_impact: missing_until_connector_quantity_known
    adapter_impact: missing_if_adapter_used
    full_lca_status: incomplete_until_dataset_linked
```

## Warning Conditions

```text
Connector material missing
Adapter material missing
Transport distance unknown
Dataset missing
Only GWP calculated, other indicators missing
```

---

# 18. RC-12 — Target Preference Weighting

## Goal

Weight technically possible options according to project intent.

## Input

```yaml
target_preferences:
  reuse_mass_priority: high | medium | low
  reversibility: high | medium | low
  visible_reuse: high | medium | low
  low_new_material: high | medium | low
  structural_system_preference: wall_bearing | frame | hybrid | unknown
  assembly_simplicity: high | medium | low
```

## Rules

```text
Preferences do not override hard failures.
Preferences rank valid or warning-level options.
A reversible target penalizes grouted irreversible details.
A low-carbon target penalizes heavy adapters and excessive steel.
A visible-reuse target rewards exposed readable mixed geometry.
A simple assembly target penalizes custom complex connectors.
```

## Output

```yaml
RC-12:
  preference_score: high | medium | low
  preference_reason:
    - visible_reuse_positive
    - connector_complexity_negative
    - high_reuse_mass_positive
    - engineering_evidence_gap_negative
```

## Example

```yaml
if:
  target_visible_reuse: high
  target_low_new_material: high
  target_reversibility: high

then:
  AA_MIX_001_score:
    visible_reuse: high
    reuse_mass: high
    reversibility: low_if_grouted_connector
    buildability: medium_to_low
```

---

# 19. RC-13 — Local Cluster Update

## Goal

Update the local assembly after each new connection.

## Input

```yaml
cluster:
  existing_connections
  new_connection_candidate
  used_components
  shared_supports
  shared_connector_zones
  local_lca_total
  local_warning_list
```

## Rules

```text
A real component cannot be used twice beyond stock.
Support zones cannot be overloaded without proof.
Connector zones cannot overlap.
Transition zones must remain blocked.
Assembly sequence must remain possible.
Connector access must remain possible.
Local LCA and reused mass must update.
```

## Output

```yaml
RC-13:
  cluster_status: pass | warning | fail | engineering_required
  updates:
    - used_component_registered
    - local_reused_mass_updated
    - local_lca_precheck_updated
    - support_zone_load_warning
    - connector_access_warning
```

## Cluster Warning for `AA_MIX_001`

```text
Because AA_MIX_001 has multiple sub-zones, one connection may consume or block
nearby future connector zones. The cluster graph must mark affected zones as occupied.
```

---

# 20. RC-14 — Connection Passport Output

Every attempted connection creates or updates a Connection Passport.

## Template

```yaml
connection_passport:
  id: CONN_AA_MIX_001_B_001

  components:
    A: AA_MIX_001
    B: B_SELECTED_BY_USER

  selected_ports:
    A: port_A
    B: port_B

  pair_type:
    detected: slab_wall | beam_column | column_base | envelope | service | unknown

  status:
    overall: pass | warning | engineering_required | fail
    geometry: pass | warning | fail
    evidence: pass | warning | engineering_required | fail
    structure: pass | warning | engineering_required | fail
    connector: pass | warning | engineering_required | fail
    fire: pass | warning | engineering_required | not_applicable
    building_physics: pass | warning | engineering_required | not_applicable
    services: pass | warning | engineering_required | not_applicable
    logistics: pass | warning | engineering_required
    lca: pass | warning | engineering_required
    cluster: pass | warning | engineering_required | fail

  allowed_connector_families:
    - connector_family

  blocked_actions:
    - drilling_without_rebar_scan
    - use_internal_transition_zone_as_connector
    - approve_structural_capacity_without_proof

  required_evidence:
    - concrete_strength_test
    - full_rebar_scan
    - structural_connection_proof
    - connector_detail
    - fire_detail_if_exposed_steel
    - lifting_design
    - LCA_connector_dataset

  suggested_next_actions:
    - choose_external_generated_port
    - add_adapter_if_gap_or_orientation_mismatch
    - upload_rebar_scan
    - select_AbbauAufbau_connector_family
    - request_structural_proof
```

---

# 21. Concrete Example A — `AA_MIX_001` Slab Edge to Wall Panel

## User Action

```yaml
user_action:
  component_A: AA_MIX_001
  port_A: slab-edge-bearing-left
  component_B: AA_WALL_001
  port_B: wall-top-bearing
```

## Checker Result

```yaml
connection_result:
  pair_type: wall_slab
  geometry: warning
  evidence: engineering_required
  structure: engineering_required
  connector: engineering_required
  fire: warning
  building_physics: context_required
  logistics: engineering_required
  lca: warning
  overall: engineering_required
```

## Why

```text
Geometry ports are compatible.
But structural capacity, rebar position, connector proof, and fire detail are missing.
```

## Candidate Connector Families

```text
nachträglicher Bewehrungsanschluss + Verguss / Injektionsmörtel
Schraubanker mit Flachstahlhalter
```

## Required Evidence

```text
full rebar scan at slab edge
full rebar scan at wall top
bearing length proof
connector proof
fire detail if steel is exposed
LCA dataset for connector material
```

---

# 22. Concrete Example B — `AA_MIX_001` Column Base to Baseplate

## User Action

```yaml
user_action:
  component_A: AA_MIX_001
  port_A: column-base-bearing
  component_B: AA_BASE_001
  port_B: baseplate-column-port
```

## Checker Result

```yaml
connection_result:
  pair_type: baseplate_column
  geometry: pass_if_contact_area_sufficient
  evidence: engineering_required
  structure: engineering_required
  connector: engineering_required
  fire: context_required
  logistics: engineering_required
  lca: warning
  overall: engineering_required
```

## Candidate Connector Families

```text
nachträglich montierter Edelstahldorn
Winkelverbinder
```

## Required Evidence

```text
column stump reinforcement evidence
baseplate reinforcement evidence
vertical load proof
temporary stability proof
anchor/dowel detail
lifting and assembly sequence
```

---

# 23. Concrete Example C — Blocked Transition-Zone Connection

## User Action

```yaml
user_action:
  component_A: AA_MIX_001
  port_A: internal-beam-column-transition
  component_B: AA_BEAM_002
  port_B: beam-end-bearing
```

## Checker Result

```yaml
connection_result:
  pair_type: invalid_transition_connection
  geometry: fail
  evidence: fail
  structure: fail
  connector: fail
  overall: fail
```

## Why

```text
The selected port is an internal monolithic transition zone.
It is not an external connector zone.
It may contain complex reinforcement and stress concentration.
```

## System Message

```text
Connection blocked.
Choose an external generated port:
- slab-edge-bearing
- beam-end-bearing
- column-base-bearing
- column-head/capital-bearing
```

---

# 24. UI Feedback in the Playground

## 24.1 Visual Status Colors

```text
Green:
geometry compatible and no hard rule failed

Yellow:
possible but warning exists

Orange:
engineering_required

Red:
blocked / fail

Grey:
not applicable or not enough context
```

## 24.2 Port Overlay

```text
solid outline:
available port

dashed outline:
candidate port, evidence required

red cross:
blocked port

lock icon:
blocked until evidence is uploaded

fire icon:
fire detail required

anchor icon:
rebar scan required

leaf/CO2 icon:
LCA dataset missing or precheck only
```

## 24.3 Rule Checker Panel

```text
Connection: AA_MIX_001 → Component B

Status:
ENGINEERING REQUIRED

Main reason:
Geometry is usable, but structural and reinforcement evidence are incomplete.

Required:
- rebar scan
- structural proof
- connector detail
- fire detail if steel is exposed
- LCA connector dataset
```

---

# 25. Minimal Rule Tree

```text
Playground Rule Checker
│
├── RC-0 Connection Intent
├── RC-1 Catalogue + Availability
├── RC-2 Geometry + Port Compatibility
├── RC-3 Evidence Gate
├── RC-4 Structural Role + Load Path
├── RC-5 Connector Family Selection
├── RC-6 Drilling / Rebar / No-Drill
├── RC-7 Fire
├── RC-8 Building Physics / Envelope
├── RC-9 TGA / Services
├── RC-10 Logistics / Buildability
├── RC-11 LCA / Ökobilanz
├── RC-12 Target Preference Weighting
├── RC-13 Local Cluster Update
└── RC-14 Connection Passport
```

---

# 26. Minimal Data Contract

## 26.1 Rule Checker Input

```yaml
rule_checker_input:
  design_id: playground_design_001

  component_A:
    id: AA_MIX_001
    type_id: type-AA_MIX_001
    selected_port: port_A
    bauteilpass_ref: catalogue/AA_MIX_001
    geometry_refs:
      structural: generated/AA_MIX_001/structural-zones.json
      connectors: generated/AA_MIX_001/ports-and-zones.json
      energy: generated/AA_MIX_001/energy-faces.json
      logistics: generated/AA_MIX_001/logistics-geometry.json

  component_B:
    id: B_SELECTED_BY_USER
    type_id: type-B
    selected_port: port_B
    bauteilpass_ref: catalogue/B_SELECTED_BY_USER
    geometry_refs:
      structural: generated/B/structural-zones.json
      connectors: generated/B/ports-and-zones.json

  placement:
    transform_A: matrix
    transform_B: matrix
    relative_transform: matrix
    contact_geometry: calculated

  project:
    connector_library: abbau_aufbau
    density_assumptions: project_defaults
    lca_defaults: project_defaults
    target_preferences: project_preferences
```

## 26.2 Rule Checker Output

```yaml
rule_checker_output:
  connection_id: CONN_AA_MIX_001_B_001
  overall_status: pass | warning | engineering_required | fail

  rule_results:
    RC-0: result
    RC-1: result
    RC-2: result
    RC-3: result
    RC-4: result
    RC-5: result
    RC-6: result
    RC-7: result
    RC-8: result
    RC-9: result
    RC-10: result
    RC-11: result
    RC-12: result
    RC-13: result

  connection_passport_ref: generated/connections/CONN_AA_MIX_001_B_001.json

  ui_feedback:
    color: green | yellow | orange | red | grey
    message: string
    required_actions:
      - action
```

---

# 27. Final Summary

The Playground rule checker for `AA_MIX_001` must follow one core principle:

```text
Geometry can make a connection candidate visible.
Only evidence and rules can make it valid.
```

For the monolithic mixed component:

```text
Generated geometry enables:
- port detection
- contact checks
- sub-zone detection
- connector candidates
- LCA and logistics prechecks

System rules prevent:
- treating it as a simple slab
- drilling without rebar scan
- using internal transition zones as connector zones
- approving structural capacity from geometry alone
- ignoring fire, logistics, and LCA consequences
```

Default result for most real structural connections involving `AA_MIX_001`:

```text
ENGINEERING_REQUIRED
```

Reason:

```text
The geometry is usable for design exploration,
but structural capacity, reinforcement, connector detail, fire treatment,
lifting, and approval evidence are not complete.
```
