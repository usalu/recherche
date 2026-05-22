# Geometry Generator Packages for Reclaimed Component Design  
## v3 — Generalized Package Structure + Data Types + Examples A/B/C

**Purpose**  
This document defines a clean, generalized package structure for geometry generators in a reclaimed-component design system.

**Context**  
The system is inspired by the Abbau/Aufbau logic of reusing large-format reinforced-concrete elements from an existing component pool. It assumes the components already exist in a **Bauteilpool / Bauteilkatalog**. The system does not treat Rückbauplanung or Zuschnittplanung as active design phases.

**Main correction in this version**  
Each package starts with a **general, reusable definition**. Specific names such as `mushroom-head-bearing`, `capital-slab-interface`, or `slab-beam-monolithic-interface` are moved into the examples. The general package definitions now describe **data types**, **expected outputs**, and **naming patterns**, not single-case element names.

---

# 0. Verified Reference Basis

## 0.1 Abbau/Aufbau factual anchors

The following project-specific statements are used as factual anchors from the Abbau/Aufbau handbook.

### Reuse focus

Abbau/Aufbau focuses on the reuse of large-format reinforced-concrete elements, described as:

```text
Platte
Scheibe
Träger
Stütze
```

### Bauteilkatalog fields

The Bauteilkatalog should contain:

```text
ID
Elementtyp
Maße: Länge, Breite, Höhe
Öffnungsmaße
Volumen
Masse
optional: räumliche Skizze
optional: Betonuntersuchungen
optional: Bewehrungsuntersuchungen
```

The catalogue and the ID form the basis for:

```text
Logistikkonzept
Lagerung
Wiedereinbau
Tracking / Tracing
```

### Abbau/Aufbau example component

```text
ID: DE_1OG_001
Länge: 4500 mm
Breite: 2300 mm
Höhe / Dicke: 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

### Verified Abbau/Aufbau connection families

```text
Fundament - Bodenplatte
→ Schraubanker

Bodenplatte - Wand
→ nachträglich montierte Edelstahldorne
→ Winkelverbinder

Bodenplatte - Stütze
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder

Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter

Stütze - Decke
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder
→ nachträglicher Bewehrungsanschluss + Verguss auf neu herzustellenden Stahlbetonträger
→ Auflager auf Stahlträger
```

### Verified energy / envelope logic

Abbau/Aufbau treats Bauphysik and energy as relevant when reused concrete elements are used in connection with:

```text
Außenwand
Dach
Gebäudehülle
Außenklima
Baugrund / Erdreich
```

The handbook includes an exterior-wall example with:

```text
200 mm reused reinforced-concrete wall
GEG example target U-value: 0.28 W/(m²K)
assumed reinforced-concrete thermal conductivity: 2.3 W/(mK)
wood-fibre insulation thermal conductivity: 0.042 W/(mK)
example result: target met from 14 cm insulation in that specific build-up
```

### Verified logistics / storage logic

Abbau/Aufbau states:

```text
intermediate storage should not be too far from the Abbau and Aufbau locations
each additional transport kilometre worsens the LCA
storage position should follow the later installation sequence
weather protection is recommended where possible
elements should be separated by protective timber
elements should generally be stored in their original orientation
slabs should be stored lying
walls and columns should be stored standing
```

### Verified LCA logic

Abbau/Aufbau describes LCA according to DIN EN 15978 and focuses especially on GWP.

The handbook states that:

```text
LCA requires quantity takeoff and datasets such as Ökobaudat or EPD
for reused concrete elements without available reused-element datasets,
A1-A3 GWP may be set to 0 kg CO₂-eq/t
a comparison with new elements can be used to calculate saving potential
transport distance affects the ecological balance
```

**Reference**  
Abbau/Aufbau, *Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden*, 2023.  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

---

# 1. Example Set Used Throughout This Document

Each package is described generally first.  
Then the same three examples are mapped to the package in the order **A → B → C**.

## Example A — Abbau/Aufbau slab DE_1OG_001

```text
Component:
DE_1OG_001

Typology:
slab / Deckenplatte

Source:
Abbau/Aufbau Bauteilkatalog example

Known data:
4500 × 2300 × 180 mm
1.863 m³
ca. 4.1 t
```

## Example B — Abbau/Aufbau Wand–Decke connection

```text
Component pair:
reused wall + reused slab

Pair type:
Wand - Decke

Abbau/Aufbau connector families:
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

## Example C — SlabBeamColumnFragment

```text
Typology:
SlabBeamColumnFragment

Status:
proposed composite system typology

Description:
one monolithic reinforced-concrete fragment composed of:
- slab portion
- integrated beam portion
- partial column section

Origin:
cut from an existing structural bay

Important:
This is not a named standard element in the Abbau/Aufbau handbook.
It is a proposed extension of the component-pool logic.
```

---

# 2. System Principle

## 2.1 Main pipeline

```text
Minimum Input
+ Base Geometry
+ Component Typology
        ↓
Domain Geometry Generator Packages
        ↓
Generated Domain Geometry
        ↓
System Modules
        ↓
Bauteilpass + Rule-Checker Readiness
        ↓
Rule Checker during active design
```

## 2.2 What geometry generators produce

Geometry generators produce only geometry-related data:

```text
faces
edges
zones
ports
interface regions
voids
openings
support candidates
bearing candidates
connector candidates
transport envelopes
storage geometry
semantic interface candidates
evidence overlays
geometry-derived quantities
```

## 2.3 What geometry generators do not produce

Geometry generators do not decide:

```text
final structural safety
actual load capacity
fire compliance
approval readiness
true concrete strength
true reinforcement position
full LCA
final U-value
target preference score
connection validity
```

Those are produced later by:

```text
system modules
rule libraries
engineering evidence
project defaults
connection checker
```

---

# 3. Why There Is No Generic Connector Generator

A generic connector generator creates overlap because “connector” has different meanings in different domains.

```text
structural connector
≠ envelope interface
≠ service penetration
≠ lifting point
≠ architectural alignment relation
```

Correct approach:

```text
Each domain package owns its own interface vocabulary.
```

Examples:

```text
Structural package:
bearing zones, anchor zones, dowel zones, grout zones, steel-support zones

Energy / Envelope package:
thermal boundary faces, insulation interfaces, thermal bridge zones

TGA / Openings package:
openings, penetrations, service ports, core-drilling candidates

Semantic / Architectural package:
room-boundary interfaces, facade-rhythm interfaces, visible-reuse interfaces

Logistics / Assembly package:
lifting zones, storage support zones, stacking interfaces, assembly access

Evidence package:
rebar scan zones, damage zones, sample points, confidence zones
```

---

# 4. Shared Data-Type Vocabulary

This section defines the data types used by all packages.  
The packages below should reuse these types instead of inventing new structures.

## 4.1 GeometryPrimitive

Neutral geometric objects extracted from the base model.

```yaml
GeometryPrimitive:
  id: string
  kind: face | edge | vertex | solid | void | opening | surface | axis | plane | point | volume
  geometry_ref: string
  local_coordinates: object
  dimensions: object | null
  area_m2: number | null
  volume_m3: number | null
  normal_vector: [number, number, number] | null
  confidence: high | medium | low
```

## 4.2 DomainZone

A geometry region with domain meaning.

```yaml
DomainZone:
  id: string
  package: base | structural | energy | tga | semantic | logistics | evidence
  zone_kind: string
  geometry_refs: [string]
  derived_from: [GeometryPrimitive.id]
  role: string
  status: generated | evidence_based | inferred | unknown
  confidence: high | medium | low
```

## 4.3 Port

A port is a possible interface point, edge, face, or region that can participate in a relation.

```yaml
Port:
  id: string
  package: structural | energy | tga | semantic | logistics
  port_kind: string
  geometry_ref: string
  direction: [number, number, number] | null
  interface_role: string
  compatible_port_patterns: [string]
  mandatory: boolean
  confidence: high | medium | low
```

Important: A port is not always a physical connector.  
A semantic port can be a `room-boundary-interface`; a logistics port can be a `lifting-candidate`; an energy port can be an `insulation-layer-interface`.

## 4.4 InterfaceRegion

A relation-ready region that may be read by the rule checker.

```yaml
InterfaceRegion:
  id: string
  package: structural | energy | tga | semantic | logistics
  interface_kind: string
  geometry_refs: [string]
  related_ports: [Port.id]
  pair_type_patterns: [string]
  rule_relevance: [string]
  status: generated | evidence_based | context_required
  confidence: high | medium | low
```

## 4.5 GeometryQuantity

Quantities derived from geometry.

```yaml
GeometryQuantity:
  id: string
  quantity_kind: length | width | height | thickness | area | volume | centroid | distance | overlap | clearance
  value: number | object
  unit: string
  source: geometry | generated | calculated
  confidence: high | medium | low
```

## 4.6 EvidenceOverlay

Geometry from scans, tests, photos, or surveys.

```yaml
EvidenceOverlay:
  id: string
  evidence_kind: rebar_scan | damage | crack | spalling | sample_point | photo_mapping | confidence_zone
  geometry_ref: string
  source_document: string | null
  measured_value: object | null
  confidence: high | medium | low
```

## 4.7 Expected package output

Every package should output:

```yaml
PackageOutput:
  package_id: string
  package_name: string
  inputs_used:
    - base_geometry
    - typology
    - project_defaults
    - evidence_if_available
  generated_primitives: [GeometryPrimitive]
  zones: [DomainZone]
  ports: [Port]
  interface_regions: [InterfaceRegion]
  quantities: [GeometryQuantity]
  overlays: [EvidenceOverlay]
  confidence_summary:
    overall: high | medium | low
    reasons: [string]
```

Not every package uses every field.  
For example, Energy may output many zones and quantities but few ports. Evidence may output overlays but no ports.

---

# 5. Package Tree

```text
GEOMETRY GENERATOR PACKAGES
│
├── 0. Base Geometry
│
├── 1. Structural Interface Geometry
│
├── 2. Energy / Envelope Geometry
│
├── 3. TGA / Openings Interface Geometry
│
├── 4. Semantic / Architectural Interface Geometry
│
├── 5. Logistics / Assembly Interface Geometry
│
└── 6. Evidence Geometry Overlay
```

---

# 6. Package Ownership Rule

Use this question:

```text
What gives this geometry its meaning?
```

| Meaning question | Package |
|---|---|
| Is it neutral shape? | Base Geometry |
| Can force transfer, support, bearing, restraint, or structural connection happen here? | Structural Interface Geometry |
| Does it affect heat, moisture, U-value, roof, facade, ground contact, or envelope? | Energy / Envelope Geometry |
| Can services pass through, connect, or conflict here? | TGA / Openings Interface Geometry |
| Does it create spatial, visual, facade, rhythm, alignment, or reuse-expression meaning? | Semantic / Architectural Interface Geometry |
| Can it be lifted, stored, transported, protected, accessed, assembled, or temporarily braced? | Logistics / Assembly Interface Geometry |
| Is it measured, damaged, scanned, tested, sampled, or uncertain? | Evidence Geometry Overlay |

---

# 7. Package 0 — Base Geometry

## 7.1 General definition

### Domain question

```text
What is the neutral shape of the component before domain meaning is assigned?
```

### General expected data

```text
The Base Geometry package should output neutral primitives and quantities.
It should not create domain-specific ports.
It is the geometric source of truth for all later packages.
```

### Expected data types

```text
GeometryPrimitive
GeometryQuantity
PackageOutput
```

### Owns

```text
normalized geometry
coordinate system
local axes
bounding box
dimensions
faces
edges
corners
raw openings / voids
raw cut-outs
volume
surface areas
center of gravity geometry
geometry confidence
```

### Does not own

```text
structural support meaning
thermal meaning
service meaning
architectural meaning
logistics meaning
evidence meaning
ports
connection rules
```

### Expected output pattern

```yaml
base_geometry_output:
  primitives:
    - kind: solid
    - kind: face
    - kind: edge
    - kind: void
  quantities:
    - length
    - width
    - height_or_thickness
    - volume
    - surface_area
    - centroid
  ports: []
  interface_regions: []
```

## 7.2 Example A — DE_1OG_001 slab

```text
Input:
4500 × 2300 × 180 mm
1.863 m³
ca. 4.1 t

Base Geometry output:
slab-like solid
top face
bottom face
four side faces
two long edges
two short edges
raw volume geometry
center-of-volume candidate
```

## 7.3 Example B — Wand–Decke connection

```text
Input:
one wall geometry
one slab geometry

Base Geometry output:
wall neutral geometry
slab neutral geometry
wall top edge / top face as raw geometry
slab edge as raw geometry
contact-relevant bounding geometry
raw distance / overlap candidates
```

The base package does not decide that this is a structural connection. It only provides the geometric primitives.

## 7.4 Example C — SlabBeamColumnFragment

```text
Input:
one monolithic composite fragment geometry

Base Geometry output:
overall bounding box
slab-like sub-volume candidate
beam-like sub-volume candidate
column-stub sub-volume candidate
monolithic junction geometry
cut faces
raw openings / voids if present
overall center of gravity
surface and edge map
```

The base package does not yet decide which zones are structural, semantic, or logistics-relevant.

---

# 8. Package 1 — Structural Interface Geometry

## 8.1 General definition

### Domain question

```text
Where can force transfer, support, bearing, restraint, or structural connection happen?
```

### General expected data

```text
The Structural Interface Geometry package should output load-related zones and structural interfaces.

It may create ports, but only as generic structural interface patterns.
The general package definition should not list one-off ports for special typologies.
Specific typology ports belong in examples or typology profiles.
```

### Expected data types

```text
DomainZone
Port
InterfaceRegion
GeometryQuantity
PackageOutput
```

### General port patterns

```text
[element]-bearing-port
[element]-support-port
[element]-restraint-port
[element]-stability-port
[edge]-line-support-port
[face]-point-support-port
[cut-face]-structural-risk-port
```

### General zone patterns

```text
bearing-zone
support-zone
line-support-zone
point-support-zone
load-transfer-zone
restraint-zone
anchor-candidate-zone
dowel-candidate-zone
post-installed-rebar-zone
grout-joint-zone
steel-support-zone
cut-face-structural-risk-zone
monolithic-continuity-zone
structural-opening-conflict-zone
```

### Owns

```text
structural role geometry
span direction candidates
support zones
bearing zones
line support zones
point support zones
load-transfer zones
structural opening conflict zones
structural no-go zones
structural ports
structural interface zones
anchor candidate zones
dowel candidate zones
post-installed rebar zones
grout / cast joint zones
steel-support zones
edge restraint zones
shear-transfer zones
moment-transfer-required zones
pair-type structural interface geometry
```

### Does not own

```text
final load capacity
structural proof
anchor capacity
punching safety
shear resistance
moment resistance
fire cover requirement
LCA of connector material
```

### System uses this package for

```text
pair classification
bearing overlap check
load-path precheck
connector family filtering
reinforcement / drilling dependency
structural rule-checker readiness
```

### Expected output pattern

```yaml
structural_interface_output:
  zones:
    - zone_kind: bearing-zone
    - zone_kind: support-zone
    - zone_kind: anchor-candidate-zone
  ports:
    - port_kind: generic-bearing-port
    - port_kind: generic-support-port
  interface_regions:
    - interface_kind: structural-load-transfer-interface
  quantities:
    - overlap_length
    - bearing_width
    - edge_distance
```

## 8.2 Example A — DE_1OG_001 slab

```text
Structural Interface Geometry output:
slab-edge-bearing zones
possible line-bearing zones
span direction candidate
structural opening conflict zones
anchor candidate zones near support edges
slab-edge-bearing ports
minimum-bearing reference zones
```

System interpretation:

```text
actual capacity remains engineering_required unless proof exists
span direction remains low-confidence if reinforcement is unknown
drilling / anchoring depends on reinforcement evidence
```

## 8.3 Example B — Wand–Decke connection

Verified Abbau/Aufbau connector families:

```text
Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter
```

Structural Interface Geometry output:

```text
wall-top-bearing port
slab-edge-bearing port
line-bearing zone at wall top
slab-edge support zone
post-installed-rebar zone
grout-joint zone
flat-steel-holder zone
anchor-candidate zone
edge-distance geometry
```

System interpretation:

```text
requires reinforcement position
requires anchor spacing / edge distance checks
requires structural proof
may require fire detail if exposed steel connector is fire-relevant
```

## 8.4 Example C — SlabBeamColumnFragment

```text
Structural Interface Geometry output:
slab-zone structural surface
beam-axis candidate
beam-bottom / beam-side structural zones
column-stub axis candidate
column-cut-face structural-risk zone
slab-beam monolithic-continuity zone
beam-column monolithic-continuity zone
external slab-edge-bearing ports
beam-end-bearing ports if beam is cut at ends
column-base or column-head bearing port depending orientation
cut-face structural-risk zones
anchor candidate zones only outside critical monolithic junctions
dowel candidate zones only where reinforcement evidence permits
load-transfer path candidates:
- slab zone → beam zone
- beam zone → column stub
- external support → fragment
```

Accuracy note:

```text
The slab, beam, and column part are not three connected pieces.
They are one monolithic reclaimed component.

Internal relations are monolithic continuity zones, not connectors.
Only external interfaces become ports or connector zones.
```

---

# 9. Package 2 — Energy / Envelope Geometry

## 9.1 General definition

### Domain question

```text
Where does the component participate in the thermal envelope, moisture boundary, roof, facade, ground contact, or U-value-relevant assembly?
```

### General expected data

```text
The Energy / Envelope package is primarily face-, surface-, edge-, layer-, and boundary-based.

It should not be forced into connector language.
Ports are only used where the geometry represents an actual envelope interface.
```

### Expected data types

```text
DomainZone
InterfaceRegion
GeometryQuantity
Port, only if useful
PackageOutput
```

### General interface patterns

```text
thermal-boundary-face
exterior-face-candidate
interior-face-candidate
roof-interface
ground-contact-interface
facade-interface
insulation-layer-interface
thermal-bridge-zone
moisture-risk-zone
envelope-penetration-zone
```

### Owns

```text
thermal boundary faces
exterior face candidates
interior face candidates
roof face candidates
ground-contact face candidates
facade interface faces
insulation layer interface faces
U-value-relevant thickness
thermal bridge zones
envelope penetration zones
envelope connector crossing zones
moisture-risk zones
```

### Does not own

```text
final U-value proof
full layer build-up
GEG compliance
moisture proof
thermal bridge Psi-value
energy certificate
```

### System uses this package for

```text
rough U-value precheck
insulation requirement flag
thermal bridge warning
moisture exposure warning
envelope rule readiness
```

### Expected output pattern

```yaml
energy_envelope_output:
  zones:
    - zone_kind: thermal-boundary-face
    - zone_kind: thermal-bridge-zone
    - zone_kind: moisture-risk-zone
  interface_regions:
    - interface_kind: envelope-interface
    - interface_kind: insulation-interface
  quantities:
    - u_value_relevant_thickness
    - surface_area
  ports:
    - optional envelope-interface-port
```

## 9.2 Example A — DE_1OG_001 slab

```text
Energy / Envelope Geometry output:
roof candidate face if used as roof
exterior-floor candidate if exposed below
interior floor/ceiling candidate if used inside
U-value-relevant thickness = 180 mm
slab-edge thermal bridge candidates
envelope penetration candidates if openings exist
```

System interpretation:

```text
if used only inside:
envelope relevance may be not_applicable

if used as roof or exterior floor:
full assembly build-up is required
thermal bridge assessment is required at edges and connectors
```

## 9.3 Example B — Wand–Decke connection

```text
Energy / Envelope Geometry output:
thermal boundary interruption if the joint is in the envelope
slab-edge thermal bridge zone
wall-slab interface thermal bridge candidate
envelope connector crossing zone if steel connector crosses insulation layer
insulation-layer interruption candidate
moisture-risk joint if exposed
```

System interpretation:

```text
rough thermal warning possible
final Psi-value requires thermal bridge calculation
final U-value requires full layer build-up
exposed steel connector may need thermal separation or detailing
```

## 9.4 Example C — SlabBeamColumnFragment

```text
Energy / Envelope Geometry output:
exposed slab surfaces
exposed beam surfaces
exposed column-stub surfaces
beam projection thermal bridge candidate
column-stub thermal bridge candidate
cut-face envelope risk zones
U-value-relevant thickness candidates for slab zone
moisture-risk horizontal surfaces
insulation interface candidates around irregular geometry
```

System interpretation:

```text
if used in envelope:
irregular geometry likely creates thermal bridge risk
full build-up and thermal bridge calculation are required
cut faces may need protection and insulation detailing
```

---

# 10. Package 3 — TGA / Openings Interface Geometry

## 10.1 General definition

### Domain question

```text
Where can services pass through, connect, or conflict with existing component geometry?
```

### General expected data

```text
The TGA / Openings package owns all opening, penetration, void, service-access, and routing interface geometry.

It may produce ports, because services often need explicit pass-through or connection locations.
```

### Expected data types

```text
GeometryPrimitive
DomainZone
Port
InterfaceRegion
GeometryQuantity
PackageOutput
```

### General port patterns

```text
existing-opening-port
service-penetration-port
core-drilling-candidate-port
cable-route-port
pipe-route-port
shaft-interface-port
vertical-pass-through-port
horizontal-pass-through-port
```

### General zone patterns

```text
opening-zone
void-zone
recess-zone
service-route-zone
blocked-penetration-zone
core-drilling-candidate-zone
edge-distance-zone
service-conflict-zone
```

### Owns

```text
existing openings
raw voids
recesses
core-drilling candidates
cable penetration zones
pipe penetration zones
shaft interface zones
service route interface zones
TGA ports
blocked penetration geometry
edge distances around openings
opening relation to structural zones
```

### Does not own

```text
approval of drilling
fire sealing proof
acoustic sealing proof
service route design
reinforcement conflict proof
```

### System uses this package for

```text
service opening reuse
core drilling warning
TGA route coordination
penetration blocked / allowed precheck
conflict with structural zones
```

### Expected output pattern

```yaml
tga_openings_output:
  primitives:
    - kind: opening
    - kind: void
  zones:
    - zone_kind: service-route-zone
    - zone_kind: core-drilling-candidate-zone
    - zone_kind: blocked-penetration-zone
  ports:
    - port_kind: service-penetration-port
    - port_kind: existing-opening-port
  quantities:
    - diameter
    - opening_width
    - opening_height
    - edge_distance
```

## 10.2 Example A — DE_1OG_001 slab

```text
TGA / Openings Geometry output:
raw openings if present
service penetration candidates
core-drilling candidate zones
edge distances
relation to slab-edge structural zones
```

For the listed Abbau/Aufbau catalogue entry DE_1OG_001, no opening is indicated in the table. Therefore:

```text
existing openings = none recorded
new penetration candidates = possible only as generated candidate zones
rebar evidence required before drilling
```

## 10.3 Example B — Wand–Decke connection

```text
TGA / Openings Geometry output:
service penetration conflict zones near the wall-slab joint
blocked core-drilling zones near structural bearing
vertical service pass-through candidates if openings exist
horizontal route conflict zones along the wall top / slab edge
```

System interpretation:

```text
service penetrations near the structural connection require coordination
new drilling depends on reinforcement evidence
fire and acoustic sealing may be required depending use
```

## 10.4 Example C — SlabBeamColumnFragment

```text
TGA / Openings Geometry output:
existing openings if any
service penetration candidates in slab zone
blocked penetration zones near beam web
blocked penetration zones near column stub
core-drilling candidates outside monolithic junctions
edge distances to cut faces
service route conflicts with beam depth
service route conflicts with column-stub zone
```

System interpretation:

```text
beam and column zones are structurally sensitive
service penetrations should prefer non-critical slab zones
reinforcement evidence is required before drilling
```

---

# 11. Package 4 — Semantic / Architectural Interface Geometry

## 11.1 General definition

### Domain question

```text
What spatial, visual, facade, rhythm, alignment, or reuse-expression relation can this component create?
```

### General expected data

```text
The Semantic / Architectural package should lean toward interfaces, not only faces.

It describes architectural relations:
room, facade, rhythm, grid, datum, visibility, threshold, identity, and reuse expression.
```

### Expected data types

```text
DomainZone
Port
InterfaceRegion
GeometryQuantity
PackageOutput
```

### General interface patterns

```text
room-boundary-interface
facade-rhythm-interface
visible-reuse-interface
ceiling-expression-interface
floor-surface-interface
circulation-facing-interface
threshold-interface
joint-line-interface
datum-alignment-interface
grid-continuation-interface
reuse-identity-interface
```

### Owns

```text
room-boundary interfaces
facade-rhythm interfaces
visible-reuse interfaces
ceiling-expression interfaces
floor-surface interfaces
circulation-facing interfaces
public/private threshold interfaces
joint-line expression zones
exposed-edge expression zones
alignment / datum interfaces
grid / module interfaces
spatial subdivision interfaces
architectural tolerance-expression zones
reuse identity display zones
```

### Does not own

```text
beauty judgment
final design intent
structural validity
energy validity
fire compliance
```

### System uses this package for

```text
visible reuse preference
room layout logic
facade rhythm logic
alignment / grid logic
architectural warnings
design preference scoring
```

### Expected output pattern

```yaml
semantic_architectural_output:
  zones:
    - zone_kind: visible-reuse-zone
    - zone_kind: room-boundary-zone
    - zone_kind: facade-rhythm-zone
  ports:
    - port_kind: architectural-interface-port
  interface_regions:
    - interface_kind: datum-alignment-interface
    - interface_kind: grid-continuation-interface
  quantities:
    - visible_area
    - edge_length
    - rhythm_spacing
```

## 11.2 Example A — DE_1OG_001 slab

```text
Semantic / Architectural output:
top face → floor-surface-interface
bottom face → ceiling-visible-interface
long edge → exposed-edge-interface
slab joint → joint-line-interface
repeated slab width → grid-continuation-interface
component ID location → reuse-identity-interface
```

System use:

```text
visible reuse preference
regular grid preference
tolerance visibility
surface expression
```

## 11.3 Example B — Wand–Decke connection

```text
Semantic / Architectural output:
wall broad side → room-boundary-interface
slab underside → ceiling-visible-interface
wall-slab joint → joint-line-interface
top of wall / slab edge → datum-alignment-interface
visible connector zone → visible-reuse-interface if exposed
```

System use:

```text
room subdivision logic
ceiling datum logic
visible joint expression
component identity display
```

## 11.4 Example C — SlabBeamColumnFragment

```text
Semantic / Architectural output:
composite-fragment identity interface
visible monolithic junction interface
exposed cut-face interface
beam-expression interface
column-stub expression interface
ceiling-depth interface
reuse-story interface
datum-alignment interface along slab edge
grid-continuation interface based on original bay rhythm
```

System interpretation:

```text
this typology can show the former structural bay
visible beam and column remnants can become an architectural feature
the system should not reduce this component to generic slab semantics
```

---

# 12. Package 5 — Logistics / Assembly Interface Geometry

## 12.1 General definition

### Domain question

```text
How can the component be stored, lifted, transported, protected, accessed, and assembled?
```

### General expected data

```text
The Logistics / Assembly package owns all handling-related geometry.

It may produce ports, but these are not structural connectors.
They are handling, access, support, lifting, storage, stacking, and assembly interface points or zones.
```

### Expected data types

```text
DomainZone
Port
InterfaceRegion
GeometryQuantity
PackageOutput
```

### General port patterns

```text
lifting-candidate-port
crane-pick-port
storage-support-port
transport-support-port
stacking-interface-port
assembly-access-port
temporary-bracing-port
protection-required-port
installation-clearance-port
```

### General zone patterns

```text
transport-envelope-zone
storage-orientation-zone
center-of-gravity-reference
lifting-candidate-zone
storage-support-zone
stacking-interface-zone
assembly-access-zone
installation-clearance-zone
temporary-bracing-zone
damage-sensitive-zone
```

### Owns

```text
transport envelope
storage orientation geometry
center of gravity reference
lifting interface zones
lifting ports
storage support zones
stacking interface zones
assembly access interfaces
installation clearance zones
crane pick zones
temporary bracing interfaces
protection / damage-sensitive zones
transport support zones
```

### Does not own

```text
lifting proof
crane capacity decision
transport permit
site logistics plan
assembly sequence approval
```

### System uses this package for

```text
mass and lifting precheck
storage orientation warning
transport envelope check
assembly access warning
temporary bracing requirement
installation sequence compatibility
```

### Expected output pattern

```yaml
logistics_assembly_output:
  zones:
    - zone_kind: transport-envelope-zone
    - zone_kind: storage-support-zone
    - zone_kind: assembly-access-zone
  ports:
    - port_kind: lifting-candidate-port
    - port_kind: temporary-bracing-port
  interface_regions:
    - interface_kind: stacking-interface
    - interface_kind: installation-clearance-interface
  quantities:
    - transport_length
    - transport_width
    - transport_height
    - center_of_gravity
```

## 12.2 Example A — DE_1OG_001 slab

Verified Abbau/Aufbau guidance:

```text
slabs should be stored lying
elements should be separated by protective timber
weather protection is recommended where possible
storage order should follow later installation sequence
```

Logistics / Assembly output:

```text
lying-flat storage interface
stacking support zones
timber-separator contact zones
transport envelope = 4500 × 2300 × 180 mm
center-of-gravity reference
assembly access along bearing edges
```

System interpretation:

```text
recommended storage orientation = lying
separator required = true
weather protection recommended = true
lifting proof required if lifting points unknown
```

## 12.3 Example B — Wand–Decke connection

```text
Logistics / Assembly output:
wall-top assembly access interface
slab lifting / placement envelope
connector access zone at wall-slab joint
temporary support / access zone if needed
installation clearance above wall
sequence dependency:
wall/support first, slab placement after
```

System interpretation:

```text
connection must remain accessible until completed
slab placement requires lifting/handling proof
assembly sequence must avoid blocking connector access
```

## 12.4 Example C — SlabBeamColumnFragment

```text
Logistics / Assembly output:
irregular transport envelope
shifted center of gravity
lifting candidate zones
do-not-lift-at-sensitive-cut-face zones
support zones for storage
temporary bracing interface if column stub creates instability
protection-required zones at cut faces
assembly access zones around beam and column projection
rotation / handling risk zones
```

System interpretation:

```text
center of gravity may not be geometric center
special lifting planning likely required
cut faces and monolithic junctions may need protection
storage may require custom support
```

---

# 13. Package 6 — Evidence Geometry Overlay

## 13.1 General definition

### Domain question

```text
Where is measured, scanned, damaged, tested, sampled, uncertain, or evidence-relevant geometry located?
```

### General expected data

```text
The Evidence Geometry Overlay package maps external evidence onto geometry.

It does not judge final safety.
It creates spatial evidence layers that other packages and the system can use.
```

### Expected data types

```text
EvidenceOverlay
DomainZone
GeometryPrimitive
GeometryQuantity
PackageOutput
```

### General overlay patterns

```text
rebar-detected-zone
unknown-rebar-zone
cover-depth-zone
core-sample-point
carbonation-test-point
chloride-test-point
damage-zone
crack-line
spalling-zone
exposed-rebar-zone
photo-evidence-zone
confidence-zone
```

### Owns

```text
rebar scan geometry
detected reinforcement lines
cover-depth zones
unknown reinforcement zones
damage zones
crack lines
spalling zones
exposed rebar zones
carbonation sample points
chloride sample points
core sample locations
photo-mapped surfaces
test locations
confidence zones
```

### Does not own

```text
final material acceptance
structural safety
durability decision
repair design
approval decision
```

### System uses this package for

```text
missing evidence warnings
drilling / anchor blocking
damage overlap with bearing zones
damage overlap with visible reuse interfaces
durability warnings
confidence scoring
engineering-required flags
```

### Expected output pattern

```yaml
evidence_geometry_output:
  overlays:
    - evidence_kind: rebar_scan
    - evidence_kind: damage
    - evidence_kind: sample_point
  zones:
    - zone_kind: unknown-rebar-zone
    - zone_kind: damage-zone
    - zone_kind: confidence-zone
  quantities:
    - cover_depth
    - crack_length
    - carbonation_depth
```

## 13.2 Example A — DE_1OG_001 slab

```text
Evidence Geometry Overlay output:
rebar scan zones if available
unknown reinforcement zones if no scan exists
damage zones if mapped
core sample points if tested
carbonation sample points if tested
confidence zones for catalogue data
```

System interpretation:

```text
if reinforcement is unknown:
drilling / anchor checks are blocked or warning

if damage overlaps slab-edge-bearing zone:
bearing use receives warning

if carbonation / chloride evidence is missing:
durability remains incomplete
```

## 13.3 Example B — Wand–Decke connection

```text
Evidence Geometry Overlay output:
wall reinforcement scan zones
slab reinforcement scan zones
unknown reinforcement zones at anchor candidates
damage overlap with wall-top bearing zone
damage overlap with slab-edge bearing zone
anchor-blocking zones
```

System interpretation:

```text
does anchor candidate zone intersect reinforcement?
is drilling allowed?
is bearing zone damaged?
is structural proof required?
```

## 13.4 Example C — SlabBeamColumnFragment

```text
Evidence Geometry Overlay output:
rebar scan zones across slab, beam, and column parts
unknown reinforcement zones at monolithic junctions
cut-face exposed reinforcement zones
core sample points if tested
carbonation sample points
damage zones at cut faces
crack lines near beam-column junction
confidence zones:
- slab region
- beam region
- column-stub region
- monolithic junction region
```

System interpretation:

```text
actual reinforcement continuity remains evidence-required
cut-face durability must be assessed
beam-column junction cracks are structurally relevant
drilling near monolithic junctions should be blocked until evidence exists
```

---

# 14. Complete Example C — SlabBeamColumnFragment

## 14.1 Status

```text
This is a proposed composite typology for the design system.

It is not presented in the Abbau/Aufbau handbook as a named standard element.

It is compatible with the system logic because Abbau/Aufbau works with large-format reinforced-concrete elements and discusses slab, beam, column, and connection logic.
```

## 14.2 Definition

```text
Typology name:
SlabBeamColumnFragment

Description:
A monolithic reinforced-concrete fragment composed of:
- slab portion
- integrated beam portion
- partial column section

Origin:
cut from an existing structural bay

Key property:
The slab, beam, and column part are not separate pieces.
They remain monolithically connected inside one reclaimed fragment.
```

## 14.3 How the system should treat it

```text
one component ID
one Bauteilpass
one Semio Type
one placed Piece
multiple internal geometry zones
external interface ports only
internal monolithic continuity zones, not internal connectors
```

## 14.4 Required evidence

```text
reinforcement continuity
capacity of remaining beam-column-slab fragment
condition of cut faces
crack / damage severity
safe lifting strategy
fire behavior of irregular exposed geometry
thermal bridge proof if used in envelope
```

---

# 15. System Boundary

## 15.1 Generator

```text
creates domain geometry
```

Examples:

```text
creates slab-edge-bearing zone
creates wall-top-bearing zone
creates monolithic-continuity zone
creates thermal bridge candidate zone
creates lifting candidate zone
```

## 15.2 System

```text
interprets geometry with catalogue data, evidence, rules, and project defaults
```

Examples:

```text
labels connector family
calculates mass
flags missing reinforcement scan
calculates transport precheck
marks proof required
```

## 15.3 Rule Checker

```text
evaluates active design actions
```

Example:

```text
user connects slab edge to wall top

checker tests:
bearing overlap
reinforcement evidence
selected connector family
fire context
LCA data
logistics access
local cluster effects
```

---

# 16. Final Rule

```text
Do not create one generic connector package.

Create domain geometry packages.

Each package owns the interface geometry that belongs to its own domain.
```

This keeps the system:

```text
minimal
accurate
extendable
Abbau/Aufbau-compatible
able to handle both simple components and composite monolithic fragments
```
