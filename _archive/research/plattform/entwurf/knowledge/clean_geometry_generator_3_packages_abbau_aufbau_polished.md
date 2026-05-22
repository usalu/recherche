# Geometry Generator Packages for Reclaimed Component Design  
## Domain-Owned Interface Geometry + Abbau/Aufbau Examples A, B, C

**Purpose**  
This document defines a clean package structure for geometry generators in a reclaimed-component design system.

**Context**  
The system is inspired by the Abbau/Aufbau logic of reusing large-format reinforced-concrete elements from an existing component pool. It assumes the components already exist in a **Bauteilpool / Bauteilkatalog**. It does not describe Rückbauplanung or Zuschnittplanung as active system phases.

**Core correction**  
There is no generic **Connector-Zone + Port Generator**.  
Each domain package owns the interface geometry, ports, zones, and connector-like relations that belong to its own domain.

---

# 0. Verified Reference Basis

## 0.1 Abbau/Aufbau source basis

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

## 0.2 Example set used throughout this document

Each package below stays general first.  
Then it maps three examples to that package.

```text
Example A:
Abbau/Aufbau slab DE_1OG_001

Example B:
Abbau/Aufbau Wand–Decke connection

Example C:
Proposed composite typology SlabBeamColumnFragment
```

### Example A — DE_1OG_001

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

### Example B — Wand–Decke connection

```text
Component pair:
reused wall + reused slab

Pair type:
Wand - Decke

Abbau/Aufbau connector families:
nachträglicher Bewehrungsanschluss + Verguss
Schraubanker mit Flachstahlhalter
```

### Example C — SlabBeamColumnFragment

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

# 1. System Principle

## 1.1 Main pipeline

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

## 1.2 What geometry generators produce

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

## 1.3 What geometry generators do not produce

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

# 2. Why There Is No Generic Connector Generator

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

# 3. Package Tree

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

# 4. Package Ownership Rule

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

# 5. Package 0 — Base Geometry

## 5.1 General definition

### Domain question

```text
What is the neutral shape of the component before domain meaning is assigned?
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

### Output type

```text
neutral geometry primitives
```

### Typical schema

```yaml
base_geometry:
  units: mm
  local_axes:
    x: principal_axis_x
    y: principal_axis_y
    z: principal_axis_z
  dimensions:
    length: null
    width: null
    height_or_thickness: null
  volume_m3: null
  surface_area_m2: null
  faces: []
  edges: []
  raw_openings: []
  center_of_gravity: null
  confidence: high | medium | low
```

## 5.2 Example A — DE_1OG_001 slab

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

## 5.3 Example B — Wand–Decke connection

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

## 5.4 Example C — SlabBeamColumnFragment

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

# 6. Package 1 — Structural Interface Geometry

## 6.1 General definition

### Domain question

```text
Where can force transfer, support, bearing, restraint, or structural connection happen?
```

### Accuracy note

This package should not be reduced to “connectors.”  
For structural logic, the following terms are often more accurate:

```text
bearing zone
support zone
load-transfer zone
restraint zone
interface region
anchor candidate zone
dowel candidate zone
grout joint zone
steel support zone
```

Ports are used only where they describe a structural relationship.

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
flat-steel-holder zones
angle-connector zones
steel-support zones
edge restraint zones
shear-transfer zones
moment-transfer-required zones
pair-type structural interface geometry
```

### Structural ports

```text
slab-edge-bearing
wall-top-bearing
wall-bottom-bearing
beam-top-bearing
beam-end-bearing
column-base-bearing
column-head-bearing
mushroom-head-bearing
capital-slab-interface
slab-beam-monolithic-interface
beam-column-monolithic-interface
```

### Structural interface / connector zones

```text
line-bearing-zone
point-bearing-zone
anchor-candidate-zone
dowel-candidate-zone
post-installed-rebar-zone
grout-joint-zone
flat-steel-holder-zone
angle-connector-zone
steel-beam-support-zone
edge-restraint-zone
shear-transfer-zone
moment-transfer-required-zone
monolithic-continuity-zone
cut-face-structural-risk-zone
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

## 6.2 Example A — DE_1OG_001 slab

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

## 6.3 Example B — Wand–Decke connection

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

## 6.4 Example C — SlabBeamColumnFragment

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

# 7. Package 2 — Energy / Envelope Geometry

## 7.1 General definition

### Domain question

```text
Where does the component participate in the thermal envelope, moisture boundary, roof, facade, ground contact, or U-value-relevant assembly?
```

### Accuracy note

Energy / Envelope should remain mainly:

```text
face-based
surface-based
edge-based
layer-based
boundary-based
```

Do not force it into connector language. Use ports only for real interface conditions.

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

### Energy interface ports

```text
thermal-envelope-interface
insulation-layer-interface
roof-build-up-interface
ground-contact-interface
facade-interface
thermal-bridge-edge
envelope-penetration-zone
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

## 7.2 Example A — DE_1OG_001 slab

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

## 7.3 Example B — Wand–Decke connection

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

## 7.4 Example C — SlabBeamColumnFragment

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

# 8. Package 3 — TGA / Openings Interface Geometry

## 8.1 General definition

### Domain question

```text
Where can services pass through, connect, or conflict with existing component geometry?
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

### TGA ports

```text
existing-opening-port
service-penetration
core-drilling-candidate
cable-route-port
pipe-route-port
shaft-interface
wet-room-service-interface
vertical-service-pass-through
horizontal-service-pass-through
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

## 8.2 Example A — DE_1OG_001 slab

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

## 8.3 Example B — Wand–Decke connection

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

## 8.4 Example C — SlabBeamColumnFragment

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

# 9. Package 4 — Semantic / Architectural Interface Geometry

## 9.1 General definition

### Domain question

```text
What spatial, visual, facade, rhythm, alignment, or reuse-expression relation can this component create?
```

### Accuracy note

This package should lean toward **interfaces**, not just faces.  
The goal is to describe architectural relations.

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

### Semantic / architectural interface ports

These are not mechanical connectors.

```text
room-boundary-interface
facade-rhythm-interface
visible-reuse-interface
ceiling-visible-interface
floor-finish-interface
exposed-edge-interface
joint-line-interface
datum-alignment-interface
grid-continuation-interface
circulation-facing-interface
threshold-interface
reuse-identity-interface
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

## 9.2 Example A — DE_1OG_001 slab

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

## 9.3 Example B — Wand–Decke connection

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

## 9.4 Example C — SlabBeamColumnFragment

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

# 10. Package 5 — Logistics / Assembly Interface Geometry

## 10.1 General definition

### Domain question

```text
How can the component be stored, lifted, transported, protected, accessed, and assembled?
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

### Logistics ports

```text
lifting-point-candidate
crane-pick-zone
storage-support-zone
transport-support-zone
stacking-interface
assembly-access-interface
temporary-bracing-interface
protection-required-zone
installation-clearance-zone
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

## 10.2 Example A — DE_1OG_001 slab

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

## 10.3 Example B — Wand–Decke connection

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

## 10.4 Example C — SlabBeamColumnFragment

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

# 11. Package 6 — Evidence Geometry Overlay

## 11.1 General definition

### Domain question

```text
Where is measured, scanned, damaged, tested, sampled, uncertain, or evidence-relevant geometry located?
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

### Evidence geometry points / zones

```text
rebar-detected-zone
unknown-rebar-zone
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

## 11.2 Example A — DE_1OG_001 slab

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

## 11.3 Example B — Wand–Decke connection

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

## 11.4 Example C — SlabBeamColumnFragment

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

# 12. Complete Example C — SlabBeamColumnFragment

## 12.1 Status

```text
This is a proposed composite typology for the design system.

It is not presented in the Abbau/Aufbau handbook as a named standard element.

It is compatible with the system logic because Abbau/Aufbau works with large-format reinforced-concrete elements and discusses slab, beam, column, and connection logic.
```

## 12.2 Definition

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

## 12.3 How the system should treat it

```text
one component ID
one Bauteilpass
one Semio Type
one placed Piece
multiple internal geometry zones
external interface ports only
internal monolithic continuity zones, not internal connectors
```

## 12.4 Required evidence

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

# 13. System Boundary

## Generator

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

## System

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

## Rule Checker

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

# 14. Final Rule

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
