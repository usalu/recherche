# Universal Minimum-Input Proof for the Piece Detail / Bauteilpass Panel — All Materials

**Purpose:** Define, *material-agnostically*, the smallest amount of information a user or project context must provide so the interface can display the full Piece / Bauteilpass data panel — and prove how every field is derived — for **any** building material (mineral, metal, wood-based, glass, polymer, composite, bio-based), not only reinforced concrete.

**Scope:** Same panel and same section structure as the concrete-specific version, but every default, formula and inference is routed through a single **Material Resolver** instead of hard-coded concrete constants. Nothing in this file assumes a specific material.

**Important constraint (unchanged):** The user does **not** manually enter full geometry. Geometry is assumed available from an existing model, scan, BIM object, mesh, drawing extraction, or Semio representation. The system extracts geometric values automatically.

**Golden rule of this proof:**
> Derive what geometry + the Material Resolver + context can support. Everything that depends on the *specific* material batch, its history, or hidden internals stays `unknown` / `estimated` / `engineering_required` until measured evidence is attached. The system never invents a measured value.

---

## Core Principle — Five Information Classes

Every field on the panel resolves into exactly one class. This is what makes the panel work for all materials with one set of rules.

```text
A. Required minimal input
   Smallest data the user/context must give to create a usable Bauteilpass.

B. Extracted from geometry/model
   Values computed from the available geometric representation. Material-independent.

C. Inferred from material profile + context
   Values from the Material Resolver, type libraries, Semio kit context, project
   defaults, or Abbau/Aufbau assumptions. Carry a confidence flag.

D. Measured-evidence-only
   Values that are only valid from a test, scan, report, or document
   (strength, contaminants, hidden internals, capacity, fire rating, U-value).

E. Never invented
   Values that must remain unknown/warning/engineering_required until evidence
   exists, because guessing them is unsafe.
```

The only thing that changes between concrete, steel, timber, glass, masonry, aluminium, brick, polymer or composite is **what the Material Resolver returns** and **which durability/fire/hidden-element branch applies**. The derivation rules stay identical.

---

## The Material Resolver (heart of the universal proof)

A single function turns a `material_kind` string into a structured profile. Every formula below calls it instead of using concrete numbers.

```text
material_profile(material_kind) -> {
  family,                       # mineral | metal | wood_based | glass | polymer | composite | bio_based | unknown
  density_kg_m3,                # default + plausible range
  thermal_conductivity_W_mK,    # lambda default
  specific_heat_J_kgK,          # default
  structural_behavior,          # isotropic | anisotropic | brittle | ductile | quasi_brittle
  combustibility,               # non_combustible | combustible | limited_combustible
  fire_strength_loss,           # none | high_temp_strength_loss | chars | melts | spalls
  dominant_durability,          # list of degradation mechanisms for this family
  hidden_element_type,          # reinforcement | fasteners | laminations | core | coating | none | unknown
  reuse_reference_category,     # what a NEW equivalent maps to for avoided-impact LCA
  default_confidence            # library_default => low/medium until measured
}
```

### Default Material Table (project-overridable seed values)

Values below are typical reference figures for first-pass derivation only; a measured value always overrides them and raises confidence. Ranges reflect normal variation by product/species/grade.

```text
material_kind            family       density_kg_m3   lambda_W_mK   combustibility      fire_behavior            hidden_element        dominant_durability
---------------------------------------------------------------------------------------------------------------------------------------------------------
reinforced_concrete      mineral      2400 (2300-2500) 1.4 (1.2-2.1) non_combustible    spalls / cover_loss      reinforcement          carbonation, chloride, corrosion-of-rebar, freeze_thaw
plain_concrete           mineral      2300 (2200-2400) 1.4           non_combustible    spalls                   none                   freeze_thaw, sulfate, cracking
structural_steel         metal        7850             50 (15-60)*   non_combustible    high_temp_strength_loss  fasteners/welds        corrosion (general, pitting, galvanic), fatigue
aluminium                metal        2700             205           non_combustible    melts (low melt point)   fasteners              corrosion (galvanic, pitting), softening
solid_timber_softwood    wood_based   470 (370-530)    0.13          combustible        chars                    fasteners              rot (wet/dry/soft), insects, moisture, UV
solid_timber_hardwood    wood_based   750 (590-930)    0.16          combustible        chars                    fasteners              rot, insects, moisture, splitting
glulam / engineered_wood wood_based   500 (450-600)    0.13          combustible        chars                    laminations/adhesive   delamination, rot, insects, moisture
clay_brick / masonry     mineral      1700 (1500-1800) 0.9 (0.6-1.2) non_combustible    stable                   mortar joints          freeze_thaw, efflorescence, salt, mortar_loss
concrete_block           mineral      1400 (1000-2000) 0.5-1.1       non_combustible    stable                   none                   freeze_thaw, cracking
natural_stone            mineral      2600 (2000-2800) 2.0 (1.3-3.5) non_combustible    spalls(some)             none                   weathering, salt, freeze_thaw
glass                    glass        2500 (2500-2580) 1.0           non_combustible    melts/softens, shatters  edge/seal/interlayer   thermal_shock, edge_damage, alkali, delamination(laminated)
gypsum / plasterboard    mineral      900 (700-1200)   0.25          limited_combustible calcines (water loss)    paper_facing           moisture, softening, mold
polymer / plastics       polymer      1200 (900-1500)  0.2 (0.15-0.4) combustible       melts/burns              none                   UV, embrittlement, creep, thermal
mineral_wool_insulation  mineral      80 (30-200)      0.035         non_combustible    stable                   none                   moisture, compression_loss
FRP / composite          composite    1800 (1500-2000) 0.3-1.0       combustible/limited softens / matrix_burn   fibers/matrix          UV, matrix_degradation, delamination, alkali(GFRP)
unknown_material         unknown      requires_input   unknown       unknown            unknown                  unknown                requires_classification
```
\* Steel λ is high but in an *assembly* the governing thermal value is the build-up, not bare steel; for envelope checks steel is treated as a thermal-bridge material, not an insulator.

```text
resolve_density(material_kind):
  if measured_density exists -> use measured, confidence = high
  else -> material_profile(material_kind).density_kg_m3, confidence = low (library_default)
  if material_kind == unknown -> density = unknown, block mass derivation until provided
```

Everywhere the concrete-specific document said "2400 kg/m³" or "lambda_concrete", this universal version says `resolve_density(material_kind)` and `material_profile(material_kind).thermal_conductivity_W_mK`.

---

## Absolute Minimum Input Package

To generate most of the panel automatically, the system needs only (identical shape to the concrete version, but `material_kind` now drives the resolver):

```text
1. component_id
2. element_kind
3. material_kind            # drives the Material Resolver
4. one geometry/model reference
5. source/context reference
6. current storage/location reference
7. evidence package references, if available
8. project defaults         # incl. material library + factors
```

### Minimal Example (any material — timber shown; swap material_kind for steel/glass/masonry/etc.)

```yaml
minimum_input:
  component_id: DE_1OG_001
  element_kind: beam
  material_kind: glulam            # resolver fills density, lambda, fire, durability branch
  geometry_reference: representations/DE_1OG_001/physical.glb
  source_context:
    project: Abbau Aufbau
    source_building: donor-building-001
    original_level: 1OG
    original_function: floor_beam
  current_location:
    storage_location: storage-yard-01
    storage_position: A-03-02
  evidence_refs:
    material_test: optional        # generic: strength/grade test, coupon, core, scan
    hidden_element_scan: optional  # generic: rebar scan OR fastener/lamination/coating scan
    damage_photos: optional
  project_defaults:
    transport_factor_kgco2e_per_tkm: 0.05
    new_equivalent_reference_by_material:    # maps material -> avoided-impact dataset
      glulam: new_glulam_beam_reference
    gravity_m_s2: 9.81
```

With this, the system derives most fields. Unknowns become `unknown`, `partial`, `estimated`, or `engineering_required` — never invented.

---

## Universal Calculation Proofs (material-independent math, material-dependent inputs)

### Volume
```text
volume_m3 = extracted_solid_volume_from_geometry
# fallback for a prismatic element when no exact solid is available:
volume_m3 = length_m × width_m × thickness_m − openings_volume_m3
```

### Mass
```text
density_kg_m3 = resolve_density(material_kind)        # measured > library default
mass_kg = volume_m3 × density_kg_m3
mass_t  = mass_kg / 1000
# confidence(mass) = confidence(geometry) ∧ confidence(density)
```

### Self weight
```text
self_weight_kN     = mass_kg × g / 1000              # g from project defaults (9.81)
self_weight_kN_m2  = self_weight_kN / area_m2        # for planar elements
self_weight_kN_m   = self_weight_kN / length_m       # for linear elements (beam/column)
```

### Area
```text
area_m2 = projected_length_m × projected_width_m     # planar
# linear/point elements: report surface_area and section_area instead
```

### Transport GWP
```text
transport_gwp_kgco2e = mass_t × transport_distance_km × transport_factor_kgco2e_per_tkm
```

### Avoided new-material GWP potential (works for any material via resolver)
```text
ref = material_profile(material_kind).reuse_reference_category
avoided_gwp_kgco2e = mass_t × new_equivalent_gwp_kgco2e_per_t[ref]
# if no reference dataset for this material -> avoided_gwp = unknown (generic_required)
```

### Thermal resistance of a single homogeneous layer (any material)
```text
lambda = material_profile(material_kind).thermal_conductivity_W_mK
R_layer = thickness_m / lambda
```

### Rough U-value with only one layer known (precheck, any material)
```text
U_rough = 1 / (Rsi + R_layer + Rse)
# Rsi, Rse = project defaults by inside/outside condition.
# For high-conductivity materials (steel, aluminium) U_rough is meaningless alone:
#   flag thermal_bridge = true, status = assembly_required.
# This is a rough precheck only, never a final energy proof.
```

---

# 0. Header / Quick Summary

**Min input:** `component_id, element_kind, material_kind, geometry_reference, current_storage_location`

**Proof / Derivation**
```text
component_name        = humanize(component_id + element_kind + material_kind)
main_dimensions       = bounding_box(geometry_reference)
volume                = solid_volume(geometry_reference)
mass                  = volume × resolve_density(material_kind)
thumbnail             = first representation tagged sketch/photo/preview, else generated preview
availability          = stock_total − used_count
evidence_completeness = count(available_required_fields) / count(required_fields)
tracking_code         = existing QR/RFID/BIM if provided, else generated from component_id
```
**E — never invented:** true physical marking, true availability if storage not synced, measured mass if density/geometry uncertain.

---

# 1. Semio Binding

**Min input:** `kit_id, component_id, element_kind, geometry_reference`

**Proof / Derivation**
```text
kit_name           = project_context.kit_name or "Bauteilkatalog"
type_id            = "type-" + component_id
type_name          = component_id
parent_type        = "type-reclaimed-" + element_kind
type_kind          = "reclaimed-" + material_kind + "-" + element_kind   # material-agnostic
stock_total        = 1 for a single real reclaimed component, unless catalogue says otherwise
stock_available    = stock_total − count(active_piece_instances_using_type)
current_piece_ids  = query_design_graph(type_id)
attribute_namespace= project_slug
quality_namespace  = project_slug
representations     = all files attached to component_id
connectors          = generated from element_kind + connector-zone geometry, else empty
```
**E:** custom taxonomy parent, grouped stock, connector list without zone abstraction.

---

# 2. Identity + Traceability

**Min input:** `component_id, element_kind, material_kind, source_project/project_context`

**Proof / Derivation**
```text
human_readable_name = element_kind_label + " " + component_id
source_building     = project_context.source_building or parse(component_id)
original_level      = parse(component_id) if floor marker (EG/1OG/UG) else unknown
original_zone       = parse(component_id) if zone marker else unknown
original_function   = infer from element_kind (material-independent):
                      slab->floor/roof, wall->panel, column->column, beam->beam, stair->stair
original_orientation= geometry local axes + representation metadata, else unknown
tracking_method     = existing reference, else generated QR
qr_code             = "QR-" + component_id
bim_guid            = imported, else system-generated GUID (status: system-generated)
external_reference  = catalogue_path(component_id)
```
**E:** physical marking, real RFID, true original function/orientation if not encoded.

---

# 3. Pool Availability

**Min input:** `component_id, stock_total (default 1), design_graph_access`

**Proof / Derivation**
```text
used_count       = count(pieces where piece.type_id == type_id)
stock_available  = stock_total − used_count − reserved_count
availability.state:
  blocked_reason exists      -> blocked
  reserved_for_design exists -> reserved
  used_count > 0             -> placed
  stock_available > 0        -> available
  else                       -> unavailable
used_as_piece_ids = list(pieces where piece.type_id == type_id)
storage_state     = (storage_location + storage_position exists) ? "located" : "unknown"
```
**E:** physical presence, loss/damage after cataloguing, manual reservation outside system.

---

# 4. Classification

**Min input:** `element_kind, material_kind`

**Proof / Derivation**
```text
primary_kind     = element_kind
material_family  = material_profile(material_kind).family
structural_family:
  slab->horizontal_spanning, wall->vertical_panel, column->vertical_point_support,
  beam->horizontal_line_support, stair->circulation, facade->envelope_component
allowed_design_roles    = element_kind library ∩ material capability
  (e.g. brittle glass -> never primary load-bearing without engineering;
   ductile steel -> broad structural roles; timber -> bending/axial per grade)
disallowed_design_roles = roles incompatible with primary_kind OR with material_family
  (e.g. combustible material in a required non_combustible position -> disallowed/warning)
semantic_tags    = [reclaimed, material_kind, material_family, element_kind, component_pool]
reuse_category:
  condition unknown   -> reusable_with_verification
  condition good      -> reusable_preferred
  critical damage     -> blocked
risk_category    = f(missing evidence, damage, unknown structural role, material brittleness)
```
**E:** confirmed load-bearing category, approved alternative use, risk with no condition data.

---

# 5. Geometry Overview

**Min input:** `geometry_reference, material_kind`

**Proof / Derivation**
```text
unit_system   = geometry metadata or project default (e.g. mm)
bounding_box  = compute_AABB_or_OBB(geometry_reference)
length        = longest horizontal bounding dimension
width         = second horizontal bounding dimension
height/thick  = smallest dimension (planar) or vertical dimension (column/wall) by orientation
gross_volume  = bounding_box_volume
net_volume    = solid_mesh_volume − opening_volumes, or exact BIM solid volume
density       = resolve_density(material_kind)        # library default flagged low confidence
mass          = net_volume × density
center_of_gravity = volume_centroid(geometry)         # for anisotropic materials still geometric
local_axes    = imported CS, else inferred from longest/shortest dimension
                NOTE: for anisotropic materials (timber, FRP, laminated) also record GRAIN/FIBER
                axis if metadata exists, else grain_axis = unknown (engineering_required for capacity)
top/bottom    = metadata if available, else inferred from orientation/context, else unknown
tolerances    = project defaults (geometry/placement/joint)
```
**E:** measured density, true top/bottom without metadata, true tolerances, internal voids not in geometry, grain/fiber orientation without evidence.

---

# 6. Geometry Representations

**Min input:** `at least one geometry_reference`

**Proof / Derivation**
```text
representations = files linked to component_id
tags    = parse metadata/filename/folder/labels
          physical.glb -> [physical,geometry,3d]; structural.json -> [structural,analysis];
          energy.json -> [energy,envelope]; connector-zones.json -> [connector,zones]
file_type = extension
LOD     = metadata or inferred (mesh/solid->physical; 2D->sketch; JSON zones->rule geometry)
confidence = native BIM/scan->high; manual sketch->medium; filename-only->low
```
**E:** semantic meaning without tag, true LOD without metadata, source reliability without provenance.

---

# 7. Physical Geometry

**Min input:** `physical_geometry_reference`

**Proof / Derivation** (purely geometric — fully material-independent)
```text
shape_type = classify(geometry):
  thin rectangular solid -> slab/panel/sheet
  tall prism             -> column/wall (by aspect + type)
  long horizontal prism  -> beam/linear member
  rod/tube section       -> linear metal/timber member
faces        = extract mesh/solid faces
edges        = extract boundary edges
openings     = detect holes/voids
cutouts      = non-rectangular voids/recesses
chamfers     = bevelled edges from edge topology
irregularities = deviation from ideal bounding prism
damage_candidates = geometry anomalies + linked damage photos
physical_tolerance = deviation from fitted ideal planes
```
**E:** whether an irregularity is damage or intended, surface contamination not in geometry, sub-resolution cracks.

---

# 8. Structural Geometry

**Min input:** `element_kind, geometry_reference, original_function/context`
**Optional (raises confidence):** `hidden_element_scan` (rebar / fastener / lamination map)

**Proof / Derivation**
```text
structural_role from element_kind:
  slab->spanning_element, wall->vertical_panel, column->vertical_support, beam->line_support
span_direction:
  if directional internal structure known (rebar dir / grain dir / fiber dir / corrugation) -> use it
  else rectangular planar -> longer direction or project rule
  else unknown / engineering_required
support_edges:
  slab->two opposite edges per span; beam->two end zones; wall->base (+top line); column->top/bottom faces
bearing_zones      = support_edges buffered by required bearing width
line/point_support = per element_kind; point support only if connector zone exists, else engineering_required
load_direction     = gravity vertical downward by default
minimum_bearing_length = project default by pair type / structural rule library
structural_thickness   = physical thickness minus non-structural layers if known, else physical thickness
structural_openings    = openings intersecting load path / bearing zone
```
**E:** actual capacity, buckling/punching/shear safety, true internal layout without scan, fire-reduced capacity.
Material note: brittle materials (glass, some stone) escalate to engineering_required earlier; ductile materials (steel) allow more inferred roles.

---

# 9. Energy / Envelope Geometry

**Min input:** `geometry_reference, material_kind, intended_context (interior/exterior/roof/ground/unknown)`

**Proof / Derivation**
```text
envelope_relevance:
  intended_context interior          -> not_relevant
  intended_context exterior/roof/ground -> relevant
  unknown                            -> requires_project_context
exterior_faces       = faces on envelope layer / tagged exterior
ground_contact_faces = downward faces at ground/foundation context
roof_faces           = upper faces in roof context
thermal_boundary     = faces separating conditioned from unconditioned/exterior
insulation_faces     = exterior side of thermal boundary
thermal_bridge_zones = connector zones crossing boundary + slab/edge at exterior
                       + ANY high-conductivity material element (steel/aluminium) crossing boundary
moisture_risk_zones  = ground-contact + exterior horizontal tops + exposed joints
U_relevant_surfaces  = thermal_boundary faces
```
**Minimal energy calc (any material):**
```text
lambda = material_profile(material_kind).thermal_conductivity_W_mK
R_layer = thickness_m / lambda
U_rough = 1 / (Rsi + R_layer + Rse)
if lambda missing -> lambda = library default, status = estimated
if material is metal -> status = thermal_bridge, assembly_required (U_rough not meaningful alone)
```
**E:** final U-value, moisture proof, Psi-value, actual insulation, inside/outside without context.

---

# 10. Semantic / Architectural Geometry

**Min input:** `element_kind, geometry_reference, source_context, optional target_use_context`

**Proof / Derivation**
```text
inside/outside side = source BIM tags / placement context, else unknown
room_facing_faces   = faces adjacent to semantic room volumes
facade_facing_faces = faces adjacent to exterior/envelope context
visible_faces       = faces not covered by other layers/finishes/hidden flags
hidden_faces        = faces assigned to bearing/envelope/ground/covered assemblies
original_use_side   = original_function + orientation (slab top=walking, bottom=ceiling)
potential_new_use   = element_kind library ∩ material capability
spatial_role        = element_kind + placement context
facade_rhythm_relevance = true if visible exterior face / facade-facing tag
visible_reuse_potential = condition.visual_quality + visible area − damage severity
surface_expression_value= weighted(visible_reuse_potential, surface_condition, repair_marks,
                          material character e.g. exposed timber/steel/brick aesthetic)
```
**E:** desired expression, inside/outside without metadata, visual quality without photos.

---

# 11. Openings + Penetrations

**Min input:** `geometry_reference`  •  **Optional:** `service_context, hidden_element_scan`

**Proof / Derivation**
```text
openings   = detect voids in geometry
opening_id = component_id + opening_index
opening_type: circular->core_drilling/bore; rectangular->opening; irregular->unknown_cutout
position   = opening centroid (local coords)
size       = circle->diameter; rectangle->w×h; through-depth = thickness
edge_distance = distance(opening boundary, nearest edge)
relation_to_hidden_elements:
  if hidden_element_scan exists -> intersect(opening zone, hidden-element map)
     (rebar map / fastener map / lamination map / stud map)
  else unknown
service_reuse_allowed:
  opening clear of structural + hidden-element zones -> candidate, else requires_verification
blocked_opening: opening intersects bearing zone, damaged zone, or no-modify zone
```
**E:** original purpose, code-compliance for new services, hidden-internal conflict without scan.

---

# 12. Surface + Edge Condition

**Min input:** `photos_or_scan_reference`  (if none: all condition fields = unknown)

**Proof / Derivation** (defect *vocabulary* selected by material family)
```text
faces      = geometry face classification (top/bottom/side)
condition  = visual inspection / computer-vision classification
defect_set = material_profile(material_kind).dominant_durability mapped to visible signs:
  mineral  -> spalling, cracks, exposed reinforcement, efflorescence, surface loss
  metal    -> corrosion (rust, pitting), coating loss, deformation, weld defects
  wood     -> rot/decay, insect holes, checks/splits, fungal staining, fastener corrosion bleed
  glass    -> chips, edge damage, scratches, seal/interlayer failure, surface devitrification
  polymer  -> embrittlement, chalking, cracking, discoloration, UV degradation
repair_marks         = patch-like regions
visual_quality       = score(damage, discoloration, cracks, repair marks)
visible_reuse_quality= visual_quality × semantic_visibility_potential
```
**E:** subsurface damage, internal contamination, microcracks, true repair quality.

---

# 13. Damage Records

**Min input:** `damage_photo_or_scan_reference`  •  **Optional:** `manual_damage_annotation`

**Proof / Derivation**
```text
damage_id   = component_id + damage_index
damage_kind = classification from evidence, vocabulary by family (see §12)
location    = map photo/scan coords to geometry face/edge
severity    = f(size, location, structural relevance)  # bearing zone -> higher
size        = bounding box of damage region
photo_reference = source image
rule_relevance:
  overlaps bearing zone   -> structural/interface rules
  overlaps visible face   -> architectural/visible reuse rules
  exposes hidden element  -> durability/internal rules (rebar exposed, fastener exposed, fiber exposed)
```
**E:** repair status unless documented, cause of damage, structural severity without engineering.

---

# 14. Material Composition & Strength Evidence  *(generalizes "Concrete Evidence")*

**Min input:** `material_kind`
**Optional evidence (any of):** `material_test_report, coupon/core_sample, mill_certificate, grade_stamp, lab_report`

**Derived / Calculated**
```text
density estimate, modulus estimate, grade/class candidate, evidence status, confidence, missing-evidence flags
```

**Proof / Derivation** — branches by family, same skeleton for all:
```text
density:
  measured -> measured(high); else material_profile default(low)

strength / grade  (the material's primary structural property):
  ONLY from test/cert/stamp, else unknown. Family-specific field name:
    mineral(concrete) -> compressive_strength (fck)        from core/test report
    masonry/stone     -> compressive_strength              from test
    metal(steel/alu)  -> yield + tensile strength, grade   from mill cert / coupon
    wood_based        -> strength class / species+grade     from grade stamp / visual+machine grading
    glass             -> type (annealed/toughened/laminated) from mark / spec sheet
    polymer/composite -> grade / fiber-matrix spec          from datasheet / coupon

secondary_modulus (E-modulus):
  from test/cert; else estimated from primary strength via family formula, status = estimated

contaminants / harmful_content:
  ONLY from lab/screening. Family-relevant set:
    mineral -> chloride, carbonation depth, sulfate, alkali
    metal   -> coating type (lead paint?), galvanic risk pairing
    wood    -> preservative/biocide treatment, fire-retardant, fungicide, old coatings
    glass   -> coating/interlayer type
    polymer -> additives, flame retardants, plasticizers
  else unknown

moisture_status: from test or environmental context, else unknown
                 (critical for wood_based and porous mineral; record always)

confidence_level: tested->high; documented-but-old->medium; default/estimated->low; unknown->none
```
**E:** real strength/grade, contaminant content, internal moisture, hidden composition — all measured-only.

---

# 15. Embedded / Hidden Element Evidence  *(generalizes "Reinforcement Evidence")*

The concrete document assumed rebar. Universally, almost every reused element hides *something* you must not damage and that governs capacity. The Resolver names it:

```text
hidden_element_type = material_profile(material_kind).hidden_element_type
  reinforced_concrete -> reinforcement (rebar, tendons)
  steel/aluminium     -> fasteners, welds, connections, internal stiffeners
  timber/glulam       -> fasteners, connectors, glue lines / laminations
  masonry             -> mortar joints, wall ties, embedded lintels
  glass(laminated/IGU)-> interlayer, edge seal, spacer
  composite/FRP       -> fiber layout, core, ply orientation
  homogeneous (plain) -> none
```

**Min input:** `element_kind, structural_geometry`
**Optional (required for high confidence):** `hidden_element_scan, shop_drawing, x-ray/ultrasonic/cover-meter scan`

**Proof / Derivation** (one rule set, hidden_element_type selects the map)
```text
internal_direction (e.g. main rebar dir / grain dir / fiber dir / joint pattern):
  scan/drawing exists -> from evidence(high)
  else infer from span/original function -> inferred_low_confidence
cover / embedment_depth:
  from scan/drawing/test, else unknown
no_modify_zones (generalized no-drill):
  from internal-element map + cover/edge/bearing buffers
  if no map -> all structurally relevant zones become unknown/blocked for drilling/cutting
modify_approved_zones:
  zones with sufficient clearance from internal elements + edges, ONLY if internal data exists
anchor/fix_approved_zones:
  connector zones ∩ modify_approved_zones ∩ edge-distance rules
unknown_zones: all zones not scanned/documented
internal_degradation_risk:
  metal internals -> corrosion risk; glue lines -> delamination risk;
  ties/connectors -> corrosion/loosening; from condition + contaminants + visual signs, else unknown
```
**E:** true internal location, true cover/embedment, safe anchor zones, internal corrosion/delamination — measured-only.

---

# 16. Durability + Restnutzungsdauer (Remaining Service Life)

**Min input:** `material_kind, condition_status, exposure_context (if known)`
**Optional evidence:** family-specific tests (carbonation/chloride for mineral; moisture/probe for wood; coating/thickness for metal; etc.)

**Proof / Derivation** — the degradation branch is chosen by the Resolver:
```text
mechanisms = material_profile(material_kind).dominant_durability
evaluate each relevant mechanism:

mineral (concrete/masonry/stone):
  carbonation_risk = (carbonation_depth >= cover) ? high : lower   # needs both, else unknown
  chloride_risk    = from chloride test, else unknown
  freeze_thaw_risk = exterior/ground/moisture exposure -> possible
  salt/efflorescence (masonry) = exposure + visible salts

metal (steel/aluminium):
  corrosion_risk = f(coating condition, exposure class, visible rust/pitting, galvanic pairing)
  fatigue_risk   = if cyclically loaded original use -> engineering_required, else low
  (steel non-combustible but loses strength in fire -> see §20)

wood_based (timber/glulam):
  decay_risk     = f(moisture content, ground/weather contact, fungal/insect signs)
  delamination_risk (glulam/engineered) = from glue-line condition / exposure
  insect_risk    = visible bore holes / species susceptibility / context

glass:
  thermal_shock + edge_damage + (laminated) interlayer/delamination + (GFRP near alkali) corrosion

polymer/composite:
  UV/embrittlement/creep/matrix degradation from age + exposure

repair_required     = damage severity medium/critical OR exposed internal element -> true
protection_required = outdoor storage OR moisture/UV/corrosion risk -> true
remaining_service_life = requires durability model + tests, else unknown / engineering_required
```
**E:** reliable remaining service life, internal corrosion/decay, true degradation rate — measured/modelled only.

---

# 17. Structural Data

**Min input:** `element_kind, geometry_reference, material_kind, original_function/context`

**Proof / Derivation**
```text
structural_role     = classification from element_kind
load_bearing_status:
  slab/beam/column/load-bearing wall -> likely structural
  partition/facade/glazing           -> non-structural until evidence
  brittle materials (glass/stone)    -> structural only with engineering proof
self_weight_kN      = mass_kg × g / 1000
self_weight_kN_m2   = self_weight_kN / area_m2       (planar)
self_weight_kN_m    = self_weight_kN / length_m      (linear)
allowed_support_types: slab->wall/beam top, column head if engineered; beam->column/wall top;
                       wall->base/foundation; column->foundation/base point
allowed_bearing_zones = structural_geometry.bearing_zones
allowed_span_direction = internal evidence (rebar/grain/fiber) if available, else aspect+kind
maximum_reuse_span    = from dimensions + original function (NOT final capacity)
known_load_capacity   = ONLY from evidence/test/static proof, else unknown
capacity_evidence_status = tested / documented / unknown
required_proof_status = used structurally + capacity unknown -> structural_proof_required
```
**E:** final capacity, punching/shear/buckling resistance, actual design load — measured-only.

---

# 18. Connector / Interface Data

**Min input:** `element_kind, structural_geometry, connector_zone_geometry (if available)`

**Proof / Derivation**
```text
connector_id   = component_id + connector_zone_id
connector_name = humanize(connector_id)
connector_type: bearing edge->bearing; service zone->service; envelope face->envelope; lifting pt->logistics
port:          slab edge->slab-edge-bearing; wall top->wall-top-bearing; column top->column-head-bearing;
               beam top->beam-top-bearing; service opening->service-penetration
compatible_ports = connector library by port
mandatory:     structural support for role -> true; service/envelope -> false
direction      = outward normal of connector zone
geometry_reference = connector-zone object
allowed_connection_role: bearing->vertical-load-transfer; service->routing; envelope->thermal-interface
allowed_connector_systems = Abbau/Aufbau library by (material_pair × element_pair)
  # generalized: concrete->grout/post-installed rebar; steel->bolt/weld/clamp;
  #              timber->screw/dowel/bracket; masonry->tie/anchor; glass->clamp/structural-seal
minimum_bearing_length / maximum_gap / edge_distance = library + tolerance + anchor rules
fixing_permission:
  if hidden-element map missing -> unknown/blocked
  if approved modify zone exists -> allowed in approved zone
fire/structural/thermal/service checks = set by connector role + context
reversibility_preference = project preference / connector library
                           (mechanical fixings -> reversible; adhesive/weld/grout -> low reversibility)
```
**E:** safe drilled/fixed zone without internal scan, connector capacity, actual reversibility of custom connectors.

---

# 19. Penetration / Fixing Zones  *(generalizes "Bohrzonen / No-Drill Zones")*

**Min input:** `connector_zone_geometry, hidden_element_evidence_status`
**For real approved zones:** `hidden_element_scan` (rebar / fastener / lamination / tie map)

**Proof / Derivation**
```text
forbidden_zones = bearing zones + damaged zones + edge buffers + known internal-element zones
unknown_zones   = zones without internal-element evidence
approved_penetration_zones = connector zones − forbidden_zones − internal buffers − edge buffers
approved_fixing_zones      = approved_penetration_zones where anchor/fix depth & spacing possible
minimum_edge_distance / minimum_spacing = connector/anchor/fixing library (material-specific)
cover/embedment_requirement = internal evidence or project default
internal_conflict_status    = intersect(fixing_zone, internal-element map)
scan_confidence             = scan metadata / evidence status
```
Material note: timber and steel allow many reversible fixings in approved zones; glass and prestressed/post-tensioned concrete escalate to engineering_required almost everywhere.
**E:** approved zones if internals unknown, real conflict without scan, pull-out/connection capacity.

---

# 20. Fire Data

**Min input:** `material_kind, element_kind`
**Optional:** `fire_test_or_classification, project_fire_context`

**Proof / Derivation** — class comes from the Resolver:
```text
reaction_to_fire (material-level only):
  material_profile(material_kind).combustibility
    non_combustible  -> concrete, masonry, stone, glass(base), steel, aluminium, mineral wool
    combustible      -> timber, most polymers, many composites
    limited          -> gypsum, some treated/composite products
  status = material-level only (NOT a system fire-resistance rating)
fire_behavior_warning = material_profile(material_kind).fire_strength_loss
    steel/aluminium -> high_temp_strength_loss / melts  (non-combustible BUT needs protection)
    timber          -> chars at known rate (residual section concept) -> still combustible
    glass           -> shatters/softens, not a fire barrier unless specified fire-glass
    concrete        -> spalling risk, cover loss
known_fire_resistance = ONLY tested/documented/engineer-calculated, else unknown/project_context_required
fire_relevant_surfaces = surfaces in compartment/escape/envelope in design context
connector_fire_warning = exposed steel/metal connector in fire-relevant assembly -> cover required
fire_protection_required_if:
  combustible material in required-non-combustible position, OR
  unprotected metal (incl. steel) in fire-rated assembly, OR exposed steel connector
```
**E:** actual fire-resistance rating, compartment compliance, connector fire performance — tested/engineered only.

---

# 21. Building Physics Data

**Min input:** `material_kind, geometry_reference, exposure_context (if known)`

**Proof / Derivation**
```text
thermal_conductivity = material_profile(material_kind).thermal_conductivity_W_mK, else unknown
density              = measured or resolver default
specific_heat        = material_profile(material_kind).specific_heat_J_kgK
rough_U_value        = 1 / (Rsi + thickness/lambda + Rse)   # metals -> thermal_bridge flag
envelope_relevance   = exposure_context or semantic placement
insulation_required_if_envelope = rough_U > project target -> insulation_required
thermal_bridge_zones = connectors crossing envelope + slab edges + any metal member crossing boundary
moisture_risk        = ground/exterior/roof exposure -> candidate
                       (wood_based & porous mineral: always record; metals: condensation/galvanic)
ground_contact_suitability = requires moisture/durability context, default requires_verification
roof_suitability     = requires waterproofing + structural + thermal context, default requires_verification
acoustic_relevance   = mass-law: high mass/area (concrete, masonry, stone) -> relevant;
                       lightweight (timber, steel sheet, glass) -> needs assembly/test
```
**E:** final assembly U-value, Psi-value, moisture safety, actual acoustic performance.

---

# 22. Acoustic Data

**Min input:** `mass, element_kind, material_kind`

**Proof / Derivation**
```text
mass_per_area = mass_kg / area_m2
mass_relevance: high mass/area (mineral/stone/masonry) -> airborne sound relevant;
                lightweight (timber/steel/glass) -> assembly-dependent, single panel insufficient
airborne_sound_data = ONLY test/database/calculation, else unknown
impact_sound_data   = ONLY assembly context with floor build-up, else unknown
recommended_acoustic_use = high mass -> separation layers; lightweight -> needs layered build-up
acoustic_warning = high acoustic demand + no acoustic evidence -> warning
```
**E:** actual airborne/impact ratings, performance after new assembly.

---

# 23. TGA / Services Data

**Min input:** `openings_from_geometry, hidden_element_evidence_status`  •  **Optional:** `service_route_context`

**Proof / Derivation**
```text
existing_service_openings = openings detected in geometry
approved_service_zones    = existing openings + zones outside bearing & known internal elements
                            (if internal data missing -> requires_verification)
blocked_service_zones     = bearing zones + no-modify zones + damaged structural zones
cable_penetration_possible= small openings / approved zones (depends on internal-element evidence)
pipe_penetration_possible = larger openings / approved zones (stronger evidence required)
core_drilling_allowed     = approved zone + internal-conflict absent (mineral/masonry)
cutting_allowed (metal/timber/glass) = approved zone + no internal-element conflict + edge distance
modify_blocked            = no-modify zone, bearing zone, unknown internals, insufficient edge distance
scan_required             = new penetration requested + internals unknown -> true
```
**E:** actual route compatibility, approved core drilling/cutting without scan, service fire/acoustic sealing.

---

# 24. Logistics Data

**Min input:** `current_storage_location, geometry_reference, mass_or_material_density, element_kind`

**Proof / Derivation**
```text
mass = volume × resolve_density(material_kind) if not measured
recommended_storage_orientation:
  slab/sheet/glass -> lying flat / vertical-in-rack per material (glass: vertical A-frame)
  wall/column      -> standing only if safely supported, else project rule
  beam/linear      -> supported at defined points to avoid sag (timber/steel: support spacing rule)
forbidden_storage_orientations = orientations causing unsupported bending/instability
weather_protection_required:
  outdoor storage OR moisture-sensitive (wood, gypsum, steel-corrosion) -> true
  glass -> protect edges + avoid thermal/impact; timber -> ventilated, off-ground
separator_required = stacked rigid elements -> avoid surface/edge damage (esp. glass, finished surfaces)
mass_handling_class = f(mass) -> manual / mechanical / crane
lifting_point_status = documented -> known, else engineering_required
                       (material note: timber & glass need spreader/soft slings; steel may have lugs)
transport_mode = project default (truck) unless size/mass exceeds limits
transport_readiness = mass known + dims known + storage accessible + protection defined
load_securing_required = always true for transport
damage_protection_required = true for reused components (edge/surface protection by material)
temporary_bracing_required = unstable vertical / slender elements -> likely true
assembly_access_zones = from connector zones + geometry
```
**E:** safe lifting-point design, actual crane requirement, actual site access.

---

# 25. Transport Data

**Min input:** `storage_location, target_site_location, component_dimensions, component_mass, project_transport_factor`
(If target unknown: `transport_distance = unknown`.)

**Proof / Derivation**
```text
transport_distance_km = route_distance(storage_location, target_site_location)
transport_mode        = project default (e.g. truck_40t)
transport_factor      = project default (kgCO2e/tkm)
transport_gwp         = mass_t × distance_km × factor
max_transport_size_check = compare bounding_box to normal transport limits
special_transport_required = dimension or mass exceeds limit (long steel/glulam, large glass panels)
protection_required   = true for reclaimed elements (fragile materials: higher protection class)
load_securing_note    = required by transport mode
```
**E:** route restrictions, permit requirements, exact emissions without route/mode.

---

# 26. LCA / Ökobilanz Data

**Min input:** `material_kind, mass, transport_distance or locations, project_lca_defaults`

**Proof / Derivation** (material-agnostic via reference mapping)
```text
reused_mass_t = mass_t
A1-A3_reuse_assumption:
  reused component -> project may set manufacturing impact to 0 for reuse scenario
  status = project_assumption
transport_factor = project default
transport_gwp    = mass_t × transport_distance_km × transport_factor
new_equivalent_reference:
  ref = material_profile(material_kind).reuse_reference_category
  map (element_kind + material) -> reference dataset:
    concrete slab -> new precast slab; steel beam -> new structural steel;
    timber beam -> new glulam/sawn; brick -> new fired brick; glass -> new float/IGU
new_equivalent_gwp     = dataset value[ref]
avoided_gwp_potential  = mass_t × new_equivalent_gwp_kgco2e_per_t[ref]
generic_dataset_status = EPD/Ökobaudat link missing -> generic_required
lca_completeness       = complete only if mass + transport + dataset + reference exist
environmental_indicators = from EPD/Ökobaudat if linked, else unknown
```
**E:** full LCA without datasets, connector-specific impact, modules B/C/D, indicators beyond GWP.

---

# 27. Documentation

**Min input:** `component_id, file_links (if available)`

**Proof / Derivation**
```text
document_id   = component_id + document_kind
document_kind = classify by folder/name/tag (generalized):
  photos/ -> photo; scan/ -> scan/laser_scan;
  evidence/material -> material_test_report (concrete test / mill cert / grade stamp / datasheet);
  evidence/internal -> hidden_element_scan (rebar scan / fastener map / lamination report);
  lca/ -> lca_document
title  = humanize(filename)
url    = file path
status = exists->available; expected-but-missing->missing; partial->partial
date/author = file metadata, else unknown
confidence = signed/tested report->high; scan/model->medium/high; manual note->low/medium
```
**E:** author without metadata, document validity, approval status.

---

# 28. Evidence Completeness

**Min input:** `component_id, element_kind, geometry_reference, material_kind`

**Proof / Derivation** (categories generalized; concrete/rebar replaced by material/internal)
```text
identity_complete        = component_id + kind + material + source exist
geometry_complete        = geometry_reference exists; dimensions/volume extractable
mass_complete            = mass measured OR mass = volume × density derivable
openings_complete        = geometry processed for openings, else partial/unknown
material_evidence_complete = strength/grade test/cert present for the material, else partial/missing
internal_evidence_complete = hidden-element scan/drawing exists and zones mapped, else partial/missing
                             (none -> complete if hidden_element_type == none)
damage_complete          = visual inspection/photos exist, else missing
connector_zones_complete = connector-zone representation exists or generated w/ confidence, else partial
logistics_complete       = storage + mass + transport + lifting status known
lca_complete             = mass + transport + dataset/reference exist
fire_complete            = component fire rating or project fire calc exists, else requires_project_context
building_physics_complete= thermal data + context + assembly known, else requires_project_context
services_complete        = openings + service zones + internal status known, else partial
overall_score            = weighted mean of category statuses
```
**E:** full completeness for material/internal/fire/energy without project evidence.

---

# 29. Pool-Level Warnings

**Min input:** `completeness statuses, damage records, material evidence statuses, logistics statuses`

**Proof / Derivation** (warnings keyed by Resolver branch)
```text
internal.position_status == missing            -> "Missing internal scan (rebar/fastener/lamination)"
material.strength/grade == unknown             -> "Missing strength/grade evidence"
contaminant relevant & == unknown              -> "Missing contaminant/treatment test"
                                                  (chloride for concrete; lead paint for steel;
                                                   preservative for timber; additives for polymer)
damage.severity == minor                       -> "Minor edge/surface damage"
lifting_points == unknown                      -> "Unknown lifting points"
transport_distance == unknown                  -> "Unknown transport distance"
lca.dataset == missing                         -> "Missing LCA dataset"
fire.rating == unknown                         -> "Missing fire rating"
combustible material in non-combustible role   -> "Fire: combustible material in protected position"
metal member crossing thermal boundary         -> "Thermal bridge risk"
thermal_conductivity == unknown                -> "Unknown thermal conductivity"
penetration zones unknown                      -> "Do not drill/cut without verification"
damaged edge overlaps bearing zone             -> "Do not use damaged edge as bearing zone"
moisture-sensitive material stored unprotected -> "Protect from moisture (rot/corrosion/softening)"
fields: pool_warnings.{id,kind,message,severity,related_data_field,recommended_next_data}
```
**E:** severity of hidden risks, actual safety of warned actions.

---

# 30. Rule-Checker Readiness

**Min input:** `all completeness statuses, element_kind, connector zones, material evidence status`

**Proof / Derivation**
```text
ready_rules:
  identity complete    -> identity check ready
  geometry complete    -> geometry/interface check ready
  mass complete        -> logistics/LCA mass precheck ready
  bearing zones exist  -> bearing precheck ready
rules_requiring_more_evidence:
  internals missing    -> anchor/drilling/cutting check needs evidence
  capacity unknown     -> structural load check needs evidence
  fire rating unknown  -> fire check needs project proof
  thermal context unknown -> envelope check needs context
  lca dataset missing  -> LCA check needs dataset
blocked_actions:
  internals unknown        -> drilling/cutting blocked
  damaged bearing edge     -> use as bearing blocked
  stock used               -> placement blocked
  element/material incompatible with role -> role blocked
                              (e.g. combustible in non-combustible role; brittle as primary support)
default_status_when_used:
  any engineering-required evidence missing -> warning/engineering_required
  critical hard evidence missing            -> invalid/block
  else                                      -> pass
```
**E:** final pass/fail for engineering rules, actual approval readiness.

---

# 31. What Should Not Be Shown in This Panel

This panel shows only collected **pool** data of the real component. It must NOT show connection- or design-specific results:

```text
current connection validity        | failed connection rules
cluster status                     | accumulated loads from current design
selected connector result          | current design LCA total
current building score              | target preference score
suggested fixes for a specific connection
```

**Absolute boundary rule**
```text
If a value depends on a specific active connection or design configuration,
it belongs to the Connection Passport or Rule Checker Panel — not the Piece/Bauteilpass panel.

Piece panel        = data of the real component from the pool (any material)
Connection Passport= result of connecting Piece A to Piece B
Rule Checker Panel = active validation state of the current design
Design Dashboard   = whole-design scores and totals
```

---

# Minimal UI Tab Structure (material-agnostic)

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
├── Material Evidence            # (was Concrete Evidence)
├── Embedded / Hidden Elements   # (was Reinforcement)
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

```text
User gives:
  component_id
  element_kind
  material_kind            # the only thing that re-routes all defaults
  geometry/model reference
  source/storage context
  optional evidence references

System derives (any material, via Material Resolver + geometry):
  dimensions, volume, mass, self-weight
  surface/edge/opening data, geometry abstractions
  classification (family-aware), connector candidates
  logistics, transport & LCA prechecks
  thermal/fire/durability *branch* for the material family
  completeness statuses, pool warnings, rule-checker readiness

System never invents (measured-evidence-only, class D/E):
  structural capacity
  true internal layout (rebar / fasteners / fibers / laminations)
  fire-resistance rating
  final U-value
  contaminant / treatment content
  remaining service life
  exact LCA indicators without datasets
```

**One sentence:** *Keep the user input minimal and identical for every material; let a single Material Resolver supply family-specific defaults and confidence; derive everything geometry + context can support; and hold every batch-, history-, or internals-dependent value at `unknown` / `estimated` / `engineering_required` until measured evidence is attached.*

---

## Reference sources for the default tables

- Density of construction materials (concrete, steel, aluminium, timber, glass, brick, stone): [theConstructor](https://theconstructor.org/building/density-construction-materials/13531/), [StructX](https://www.structx.com/Material_Properties_013.html)
- Thermal conductivity of building materials: [C-Therm](https://ctherm.com/applications/building-materials/), [Engineering Toolbox](https://www.engineeringtoolbox.com/thermal-conductivity-d_429.html)
- Material passport data fields & circular-construction scope: [Material passport — Wikipedia](https://en.wikipedia.org/wiki/Material_passport), [Madaster](https://madaster.com/material-passport/)
- Degradation mechanisms (steel corrosion, timber decay, glass/masonry): [Designing Buildings — Degradation of construction materials](https://www.designingbuildings.co.uk/wiki/Degradation_of_construction_materials)
