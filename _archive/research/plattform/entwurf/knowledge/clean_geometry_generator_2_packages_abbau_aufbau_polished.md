# Geometry Generator Packages for Reclaimed Component Design
## Clean Domain Structure + Abbau/Aufbau Examples

**Scope**  
This document defines the clean package structure for geometry generators in a reclaimed-component design system.

**Project framing**  
The system is inspired by **Abbau/Aufbau** and starts from an already existing **Bauteilpool / Bauteilkatalog**. The generators do not decide the Rückbau or Zuschnitt. They process elements that already exist in the pool.

**Core correction**  
There is no generic “Connector-Zone + Port Generator.”  
Each domain package owns its own interface and connector geometry.

---

## 0. Verified Abbau/Aufbau Reference Basis

The following Abbau/Aufbau details are used as factual anchors:

### Reused component types

Abbau/Aufbau frames reuse around large-format reinforced-concrete elements such as:

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

### Example component from Abbau/Aufbau

```text
ID: DE_1OG_001
Länge: 4500 mm
Breite: 2300 mm
Höhe / Dicke: 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

### Verified connector families from Abbau/Aufbau execution planning

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

Abbau/Aufbau states that thermal performance becomes especially relevant when reused reinforced-concrete elements are used in contact with the exterior climate, the ground, as part of an exterior wall, or in the roof.

For an example exterior wall, Abbau/Aufbau uses:

```text
200 mm reused reinforced-concrete wall
thermal conductivity to be measured or assumed
GEG target U-value in example: 0.28 W/(m²K)
assumed reinforced-concrete λ: 2.3 W/(mK)
wood-fibre insulation example: λ = 0.042 W/(mK)
```

The example shows that the required U-value is met from 14 cm insulation in that specific wall build-up.

### Verified storage / logistics logic

Abbau/Aufbau states that:

```text
intermediate storage should not be too far away
each transport kilometre worsens the LCA
storage should follow later installation order
elements should be protected from weather where possible
elements should be separated by protective timber
elements should generally be stored in their original orientation
slabs should be stored lying
walls and columns should be stored standing
```

### Verified LCA logic

Abbau/Aufbau describes LCA according to DIN EN 15978 and emphasizes GWP. It states that:

```text
LCA requires quantity takeoff and datasets such as Ökobaudat or EPD
for used concrete elements without available datasets, A1-A3 GWP can be set to 0 kg CO₂-eq/t
a comparison with new elements can be used to calculate the saving potential
transport distance affects the ecological balance
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

Generators produce only geometry-related data:

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
transport envelope
storage orientation geometry
semantic interface candidates
evidence overlays
geometry-derived quantities
```

## 1.3 What geometry generators do not produce

Generators do not decide:

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

Those are produced by system modules and the rule checker.

---

# 2. Why There Is No Generic Connector Generator

A generic connector generator creates overlap because “connector” means different things in different domains.

```text
structural connector
≠ envelope interface
≠ service penetration
≠ logistics lifting point
≠ architectural alignment relation
```

Correct approach:

```text
Each domain owns its own interface vocabulary.
```

For example:

```text
Structural package owns:
bearing zones, anchor zones, dowel zones, grout zones, steel-support zones.

Energy package owns:
thermal boundary faces, insulation interfaces, thermal bridge zones.

TGA package owns:
openings, penetrations, core-drilling candidates, service ports.

Semantic package owns:
room-boundary interfaces, facade-rhythm interfaces, visible-reuse interfaces.

Logistics package owns:
lifting zones, storage support zones, stacking interfaces, assembly access.

Evidence package owns:
rebar scan zones, damage zones, sample points, confidence zones.
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

# 4. Rule for Package Ownership

Use this question:

```text
What gives this geometry its meaning?
```

| Meaning question | Package |
|---|---|
| Is it neutral shape? | Base Geometry |
| Can force transfer, support, bearing, restraint, or structural connection happen here? | Structural Interface Geometry |
| Does it affect heat, moisture, U-value, roof, facade, ground contact, or thermal envelope? | Energy / Envelope Geometry |
| Can services pass through, connect, or conflict here? | TGA / Openings Interface Geometry |
| Does it create spatial, visual, facade, rhythm, alignment, or reuse-expression meaning? | Semantic / Architectural Interface Geometry |
| Can it be lifted, stored, transported, protected, accessed, assembled, or temporarily braced? | Logistics / Assembly Interface Geometry |
| Is it measured, damaged, scanned, tested, sampled, or uncertain? | Evidence Geometry Overlay |

---

# 5. Package 0 — Base Geometry

## Domain question

```text
What is the neutral shape of the component before domain meaning is assigned?
```

## Owns

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

## Does not own

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

## Output type

```text
neutral geometry primitives
```

## Typical schema

```yaml
base_geometry:
  units: mm
  local_axes:
    x: long_direction
    y: short_direction
    z: thickness_or_height
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

## Example A — Abbau/Aufbau slab DE_1OG_001

```text
Input:
DE_1OG_001
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

## Example B — 200 mm reused concrete wall

```text
Input:
reused reinforced-concrete wall
thickness = 200 mm

Base Geometry output:
wall panel geometry
two broad faces
top edge
bottom edge
side edges
200 mm thickness
surface areas
volume geometry
```

---

# 6. Package 1 — Structural Interface Geometry

## Domain question

```text
Where can force transfer, support, bearing, restraint, or structural connection happen?
```

## Accuracy note

This package should not be reduced to “connectors.”  
For Tragwerk, these terms are more accurate:

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

## Owns

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

## Structural ports

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

## Structural interface / connector zones

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

## Does not own

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

## System uses this package for

```text
pair classification
bearing overlap check
load-path precheck
connector family filtering
reinforcement / drilling dependency
structural rule-checker readiness
```

## Example A — Wand–Decke connection

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

## Example B — Stütze–Decke connection

Verified Abbau/Aufbau connector families:

```text
Stütze - Decke
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder
→ nachträglicher Bewehrungsanschluss + Verguss auf neu herzustellenden Stahlbetonträger
→ Auflager auf Stahlträger
```

Structural Interface Geometry output:

```text
column-head-bearing port
slab point-support candidate region
dowel-candidate zone
angle-connector zone
steel-beam-support zone
new-beam support interface zone
punching-sensitive interface region
```

System interpretation:

```text
punching check required
local bearing check required
connector capacity required
fire cover may be required for exposed steel connector
```

---

# 7. Package 2 — Energy / Envelope Geometry

## Domain question

```text
Where does the component participate in the thermal envelope, moisture boundary, roof, facade, ground contact, or U-value-relevant assembly?
```

## Accuracy note

Energy / Envelope should remain mainly:

```text
face-based
surface-based
edge-based
layer-based
boundary-based
```

Do not force connector language here. Use ports only for real interface conditions.

## Owns

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

## Energy interface ports

```text
thermal-envelope-interface
insulation-layer-interface
roof-build-up-interface
ground-contact-interface
facade-interface
thermal-bridge-edge
envelope-penetration-zone
```

## Does not own

```text
final U-value proof
full layer build-up
GEG compliance
moisture proof
thermal bridge Psi-value
energy certificate
```

## System uses this package for

```text
rough U-value precheck
insulation requirement flag
thermal bridge warning
moisture exposure warning
envelope rule readiness
```

## Example A — 200 mm reused concrete wall in exterior wall

Verified Abbau/Aufbau example:

```text
20 cm reused reinforced-concrete wall
λ for reinforced concrete may be assumed or measured
example assumption: λ = 2.3 W/(mK)
GEG example target: U = 0.28 W/(m²K)
wood-fibre insulation λ = 0.042 W/(mK)
example result: target met from 14 cm insulation in that build-up
```

Energy / Envelope Geometry output:

```text
outer broad face candidate
inner broad face candidate
200 mm U-value-relevant thickness
facade interface face
insulation-layer interface face
edge thermal bridge candidates
```

System precheck:

```text
R_concrete = thickness / λ_concrete
U_rough = 1 / (Rsi + R_concrete + Rse)
```

## Example B — reused slab as roof or exterior floor

Energy / Envelope Geometry output:

```text
roof candidate face
interior candidate face
slab-edge thermal bridge zone
roof-build-up interface
insulation interface
moisture-risk horizontal face
```

System requirements:

```text
project envelope context
full roof / floor build-up
insulation layer data
U-value target
thermal bridge assessment
moisture proof
```

---

# 8. Package 3 — TGA / Openings Interface Geometry

## Domain question

```text
Where can services pass through, connect, or conflict with existing component geometry?
```

## Owns

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

## TGA ports

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

## Does not own

```text
approval of drilling
fire sealing proof
acoustic sealing proof
service route design
reinforcement conflict proof
```

## System uses this package for

```text
service opening reuse
core drilling warning
TGA route coordination
penetration blocked / allowed precheck
conflict with structural zones
```

## Example A — openings in Bauteilkatalog

Abbau/Aufbau lists opening dimensions as part of the Bauteilkatalog when openings exist.

TGA / Openings Geometry output:

```text
existing-opening-port
opening position
opening size
edge distance
possible service reuse candidate
```

System interpretation:

```text
structural conflict check required
reinforcement relation required
service reuse possible only with project context
fire / acoustic sealing may be required
```

## Example B — core drilling / sample geometry

Abbau/Aufbau discusses core extraction and testing as part of material investigation. In the design system, a core-drilling candidate is geometry that must be checked before any new penetration.

TGA / Openings Geometry output:

```text
core-drilling-candidate zone
diameter candidate
depth candidate
edge distance
relation to structural interface zones
```

System warning:

```text
block or warn if reinforcement position is unknown
block if the zone overlaps structural interface
warn if fire/acoustic/service proof is missing
```

---

# 9. Package 4 — Semantic / Architectural Interface Geometry

## Domain question

```text
What spatial, visual, facade, rhythm, alignment, or reuse-expression relation can this component create?
```

## Accuracy note

This package should lean toward **interfaces**, not just faces.  
The goal is to describe architectural relations.

## Owns

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

## Semantic / architectural interface ports

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

## Does not own

```text
beauty judgment
final design intent
structural validity
energy validity
fire compliance
```

## System uses this package for

```text
visible reuse preference
room layout logic
facade rhythm logic
alignment / grid logic
architectural warnings
design preference scoring
```

## Example A — slab as floor / ceiling expression

For Abbau/Aufbau slab DE_1OG_001:

```text
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

## Example B — reused wall as room / facade interface

For a reused wall panel:

```text
inner broad side → room-boundary-interface
outer broad side → facade-rhythm-interface
vertical edge → joint-line-interface
top edge → datum-alignment-interface
surface marks → visible-reuse-interface
```

System use:

```text
cellular room logic
facade rhythm
visible reuse expression
joint alignment
```

---

# 10. Package 5 — Logistics / Assembly Interface Geometry

## Domain question

```text
How can the component be stored, lifted, transported, protected, accessed, and assembled?
```

## Owns

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

## Logistics ports

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

## Does not own

```text
lifting proof
crane capacity decision
transport permit
site logistics plan
assembly sequence approval
```

## System uses this package for

```text
mass and lifting precheck
storage orientation warning
transport envelope check
assembly access warning
temporary bracing requirement
installation sequence compatibility
```

## Example A — slab storage

Verified Abbau/Aufbau guidance:

```text
slabs should be stored lying
elements should be separated by protective timber
weather protection is recommended where possible
storage order should follow later installation sequence
```

Logistics / Assembly Interface Geometry output:

```text
lying-flat storage interface
stacking support zones
timber-separator contact zones
transport envelope
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

## Example B — wall / column storage

Verified Abbau/Aufbau guidance:

```text
walls and columns should generally be stored standing
storage should respect original orientation where possible
```

Logistics / Assembly Interface Geometry output:

```text
standing storage interface
base support zone
temporary bracing interface
transport support zone
damage-sensitive edge zones
crane pick candidate zone
```

System interpretation:

```text
standing support available?
temporary bracing required?
orientation compatible?
damage-sensitive edges protected?
```

---

# 11. Package 6 — Evidence Geometry Overlay

## Domain question

```text
Where is measured, scanned, damaged, tested, sampled, uncertain, or evidence-relevant geometry located?
```

## Owns

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

## Evidence geometry points / zones

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

## Does not own

```text
final material acceptance
structural safety
durability decision
repair design
approval decision
```

## System uses this package for

```text
missing evidence warnings
drilling / anchor blocking
damage overlap with bearing zones
damage overlap with visible reuse interfaces
durability warnings
confidence scoring
engineering-required flags
```

## Example A — reinforcement evidence

Abbau/Aufbau emphasizes archive drawings, static calculations, formwork and reinforcement plans, and reinforcement detection if needed.

Evidence Geometry Overlay output:

```text
rebar-detected-zone
unknown-rebar-zone
cover-depth zones
anchor-blocking zones
scan confidence zones
```

System interpretation:

```text
does anchor candidate zone intersect rebar?
is drilling allowed?
is reinforcement position missing?
is structural proof required?
```

## Example B — carbonation / core sample

Abbau/Aufbau discusses material investigation such as core sampling and carbonation-related assessment.

Evidence Geometry Overlay output:

```text
core-sample-point
carbonation-test-point
sample depth geometry
tested surface zone
confidence zone
```

System interpretation:

```text
carbonation depth known?
cover depth known?
corrosion risk warning?
durability evidence complete?
```

---

# 12. Complete Example A — Abbau/Aufbau Slab DE_1OG_001

## Input

```text
component_id: DE_1OG_001
typology: slab / Deckenplatte
material: reinforced concrete
dimensions: 4500 × 2300 × 180 mm
volume: 1.863 m³
mass: ca. 4.1 t
```

## Package outputs

```text
Base Geometry:
dimensions, faces, edges, volume, center geometry

Structural Interface Geometry:
slab-edge-bearing zones
span candidate
anchor candidate zones
slab-edge-bearing ports

Energy / Envelope Geometry:
roof / exterior-floor candidates
U-value-relevant thickness = 180 mm
slab-edge thermal bridge candidates

TGA / Openings Geometry:
opening candidates
service penetration candidates
core-drilling candidate zones

Semantic / Architectural Interface Geometry:
floor-surface interface
ceiling-visible interface
exposed-edge interface
grid-continuation interface
reuse-identity interface

Logistics / Assembly Interface Geometry:
lying-flat storage geometry
transport envelope
stacking support zones
assembly access along bearing edges

Evidence Geometry Overlay:
rebar scan zones if available
damage zones if mapped
sample points if tested
unknown evidence zones
```

## System interpretation

```text
mass is known from catalogue or calculable from volume and density
transport GWP can be calculated if transport distance is known
structural capacity remains engineering_required unless proof exists
drilling remains blocked or warning if reinforcement position is unknown
```

---

# 13. Complete Example B — Abbau/Aufbau Wand–Decke Connection

## Input

```text
component A: reused wall / Wand
component B: reused slab / Decke
pair type: Wand - Decke
connection families from Abbau/Aufbau:
- nachträglicher Bewehrungsanschluss + Verguss
- Schraubanker mit Flachstahlhalter
```

## Package outputs

```text
Base Geometry:
wall and slab primitives

Structural Interface Geometry:
wall-top-bearing port
slab-edge-bearing port
line-bearing zone
post-installed-rebar zone
grout-joint zone
flat-steel-holder zone
anchor candidate zone

Energy / Envelope Geometry:
if connection is in envelope:
thermal bridge edge
envelope connector crossing zone
insulation interface interruption

TGA / Openings Geometry:
service penetration conflict zones near connection
blocked core-drilling zones near structural interface

Semantic / Architectural Interface Geometry:
joint-line interface
visible-reuse edge
datum-alignment interface
room-boundary interface

Logistics / Assembly Interface Geometry:
assembly access to wall top
slab lifting / placement envelope
temporary support / access zone if needed

Evidence Geometry Overlay:
rebar scan zones
unknown reinforcement zones
damage overlap with bearing zone
anchor blocking zones
```

## System interpretation

```text
connection can only be checked after:
bearing overlap is known
reinforcement evidence is known
connector family is selected
fire context is known
assembly access is possible

if reinforcement is unknown:
anchor / drilling is warning or blocked

if exposed steel connector is fire-relevant:
fire cover or fire detail is required
```

---

# 14. Complete Example C — SlabBeamColumnFragment

## Status of this example

This is a **proposed composite typology** for the design system.

It is not presented in the Abbau/Aufbau handbook as a named standard element.  
It is consistent with the Abbau/Aufbau logic because the handbook focuses on reuse of large-format reinforced-concrete components and discusses elements such as slab, beam, column, and structural connections. Here, the component is assumed to already exist in the pool after being cut from an existing structural bay.

## Definition

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

## Minimum input

```yaml
component_id: SBCF_001
component_typology: SlabBeamColumnFragment
material: reinforced_concrete
base_geometry_reference: geometry/SBCF_001.glb
source_context:
  original_system: in-situ reinforced-concrete structural bay
  original_role: slab + beam + column zone
  cut_status: already_cut_and_in_pool
```

## Package 0 — Base Geometry output

```text
overall composite bounding box
slab plate volume
integrated beam volume
column-stub volume
monolithic junction geometry
cut faces
raw openings / voids if present
overall center of gravity
sub-volume candidates:
- slab zone
- beam zone
- column section zone
```

## Package 1 — Structural Interface Geometry output

This package is the most important for this typology.

```text
slab-zone structural surface
beam-axis candidate
beam-bottom / beam-side structural zones
column-stub axis candidate
column-cut-face structural risk zone
slab-beam monolithic-continuity zone
beam-column monolithic-continuity zone
external slab-edge-bearing ports
beam-end-bearing ports if beam is cut at ends
column-base or column-head bearing port depending fragment orientation
cut-face structural-risk zones
anchor candidate zones only outside critical monolithic junctions
dowel candidate zones only where reinforcement evidence permits
load-transfer path candidates:
- slab → beam
- beam → column stub
- external support → fragment
```

## Structural accuracy notes

```text
Do not treat the slab, beam, and column as independent connected pieces.
They are one monolithic fragment.

Do not create internal connectors between slab, beam, and column.
The internal relation is monolithic continuity, not a new connector.

Do create external structural interface ports at cut faces and support edges.
These are where the fragment can connect to the new building.
```

## Package 2 — Energy / Envelope Geometry output

```text
if used in envelope:
exposed slab surfaces
exposed beam surfaces
exposed column-stub surfaces
thermal bridge risk at beam projection
thermal bridge risk at column stub
cut-face envelope risk zones
U-value-relevant thickness candidates for slab zone
moisture-risk horizontal surfaces
insulation interface candidates around irregular geometry
```

## Energy accuracy notes

```text
Energy geometry remains surface-, edge-, and layer-based.
The beam and column protrusions may create thermal bridge risk if they cross the envelope.
Final U-value and thermal bridge proof require full assembly context.
```

## Package 3 — TGA / Openings Interface Geometry output

```text
existing openings if any
service penetration candidates in slab zone
blocked penetration zones near beam web
blocked penetration zones near column stub
core-drilling candidates outside monolithic junctions
edge distances to cut faces
service route conflicts with beam depth
service route conflicts with column-stub zone
```

## TGA accuracy notes

```text
The beam and column zones should be treated as structurally sensitive.
Service penetrations should prefer non-critical slab zones and require reinforcement evidence.
```

## Package 4 — Semantic / Architectural Interface Geometry output

```text
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

## Semantic accuracy notes

```text
This typology can express reuse more strongly than a simple slab.
The visible beam and column remnant can show the previous structural bay.
The system should not hide this under generic slab semantics.
```

## Package 5 — Logistics / Assembly Interface Geometry output

```text
irregular transport envelope
shifted center of gravity
lifting candidate zones
do-not-lift-at-sensitive-cut-face zones
support zones for storage
temporary bracing interface if vertical column stub creates instability
protection-required zones at cut faces
assembly access zones around beam and column projection
rotation / handling risk zones
```

## Logistics accuracy notes

```text
The center of gravity may not be at the geometric center.
The fragment may require special lifting planning.
Cut faces and monolithic junctions may need protection during storage and transport.
```

## Package 6 — Evidence Geometry Overlay output

```text
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

## System interpretation for Example C

```text
This is a composite real component, not an assembly of three placed pieces.

The Bauteilpass should store:
one component ID
one Semio Type
one Piece when placed
multiple internal geometry zones

The rule checker should expose:
external structural connection options
cut-face risk warnings
lifting / storage warnings
evidence requirements for reinforcement
special thermal bridge warnings if used in envelope
architectural reuse-expression potential
```

## What remains evidence-required

```text
actual reinforcement continuity
capacity of the remaining beam-column-slab fragment
safe external support conditions
cut-face durability
lifting strategy
crack / damage severity
fire behavior of irregular exposed geometry
thermal bridge proof if used in envelope
```

---

# 15. Final Boundary

## Generator

```text
creates domain geometry
```

Example:

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

Example:

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
checker tests overlap, evidence, connector, fire, LCA, logistics, and cluster effects
```

---

# 16. Final Rule

```text
Do not create one generic connector package.

Create domain packages.

Each package owns the interface geometry that belongs to its own domain.
```

This keeps the system:

```text
minimal
accurate
extendable
Abbau/Aufbau-compatible
ready for complex composite fragments
