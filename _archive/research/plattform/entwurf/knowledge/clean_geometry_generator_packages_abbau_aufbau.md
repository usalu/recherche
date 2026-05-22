# Clean Package Structure for Geometry Generators  
## Domain-Owned Geometry Packages for Reclaimed Component Design

**Context:** Abbau/Aufbau-inspired design system for an already existing pool of reclaimed reinforced-concrete components.  
**Correction:** There is no generic “Connector-Zone + Port Generator.” Each domain package owns the geometry vocabulary that gives its interfaces meaning.  
**Important rule:** Prefer interface / connector logic where it helps the domain. Do **not** force connector language where faces, surfaces, edges, or zones are technically more accurate. This is especially important for **Tragwerk** and **Energy / Envelope**.

---

## 0. Source Basis

This document is grounded in the Abbau/Aufbau handbook logic:

- Abbau/Aufbau focuses on the reuse of large-format reinforced-concrete elements such as **Platte, Scheibe, Träger, Stütze**.
- The Bauteilkatalog contains **ID, Maße, Öffnungsmaße, Volumen, Masse**, and may be extended with **Beton- und Bewehrungsuntersuchungen**.
- The ID and catalogue form the basis for **Logistik, Lagerung und Wiedereinbau**.
- Execution planning includes concrete connection families such as **Schraubanker**, **Edelstahldorn**, **Winkelverbinder**, **nachträglicher Bewehrungsanschluss + Verguss**, **Flachstahlhalter**, and **Stahlträger-Auflager**.
- Bauphysik / Energie is relevant when reused concrete elements become part of the envelope, for example exterior wall, roof, or ground-contact component.
- Logistics includes storage order, weather protection, separation with timber, and correct storage orientation.
- LCA includes transport impact and avoided new-material comparison.

Reference:  
Abbau/Aufbau, *Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden*, 2023.  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

---

# 1. System Principle

## 1.1 Correct Architecture

```text
Minimum Input
+ Base Geometry
+ Component Typology
        ↓
Domain Geometry Generator Packages
        ↓
Generated domain geometry
        ↓
System Modules
        ↓
Bauteilpass + Rule-Checker Readiness
```

## 1.2 What Generators Do

Generators only produce geometry-related data:

```text
faces
edges
zones
ports
interface regions
voids
openings
support candidates
connector candidates
transport envelopes
semantic interface candidates
evidence overlays
geometry-derived quantities
```

## 1.3 What Generators Do Not Do

Generators do not decide:

```text
final structural safety
actual load capacity
fire compliance
approval readiness
true material strength
true reinforcement position
full LCA
final U-value
target preference score
connection validity
```

Those are handled by **system modules** and later by the **rule checker**.

---

# 2. Why the Generic Connector Generator Is Removed

The previous structure had:

```text
Structural Geometry Generator
Connector-Zone + Port Generator
Energy Geometry Generator
Semantic Geometry Generator
Logistics Geometry Generator
```

This creates overlap because “connector” has different meanings in different domains.

```text
structural connector
≠ envelope interface
≠ service penetration
≠ logistics lifting point
≠ architectural alignment relation
```

## Correct Rule

```text
Each domain package owns its own:
- geometry
- zones
- ports, only where technically useful
- interface vocabulary
- rule-facing geometric data
```

## Test for Where Something Belongs

```text
What question gives this geometry meaning?
```

| Question | Package |
|---|---|
| Can force transfer? | Structural Interface Geometry |
| Does it affect heat, moisture, U-value, or envelope? | Energy / Envelope Geometry |
| Can services pass through or connect? | TGA / Openings Interface Geometry |
| Does it create room, facade, visibility, rhythm, alignment, or reuse expression? | Semantic / Architectural Interface Geometry |
| Can it be lifted, stored, transported, assembled, or accessed? | Logistics / Assembly Interface Geometry |
| Is it measured, damaged, scanned, sampled, or uncertain? | Evidence Geometry Overlay |
| Is it neutral raw shape? | Base Geometry |

---

# 3. Final Package Tree

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

# 4. Package 0 — Base Geometry

## Domain Question

```text
What is the neutral shape of the component before any domain meaning is assigned?
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
raw voids
raw openings
volume
surface areas
center of gravity geometry
geometry confidence
```

## Does Not Own

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

## Output Type

```text
neutral geometry primitives
```

## Typical Fields

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
  faces: []
  edges: []
  raw_openings: []
  center_of_gravity: null
  confidence: high | medium | low
```

## Abbau/Aufbau Example 1 — Deckenplatte DE_1OG_001

From the Abbau/Aufbau Bauteilkatalog example:

```text
ID: DE_1OG_001
L = 4500 mm
B = 2300 mm
H = 180 mm
Volumen = 1.863 m³
Masse = ca. 4.1 t
```

Base Geometry produces:

```text
one slab-like solid
top face
bottom face
four side faces
two long edges
two short edges
volume geometry
center-of-volume candidate
```

## Abbau/Aufbau Example 2 — 20 cm Stahlbetonwand in Energy Example

The Bauphysik example assumes a reused **200 mm Stahlbetonwand** as the structural part of an exterior wall build-up.

Base Geometry produces:

```text
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

# 5. Package 1 — Structural Interface Geometry

## Domain Question

```text
Where can force transfer, support, bearing, restraint, or structural connection happen?
```

## Important Accuracy Rule

This package should not be reduced to “connectors.”  
For Tragwerk, **bearing zones, support surfaces, load-transfer regions, and structural interfaces** are more accurate than generic connector language.

Use ports only where they describe a structural relation.

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

## Structural Ports

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
```

## Structural Interface / Connector Zones

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
```

## Does Not Own

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

## System Uses This Package For

```text
pair classification
bearing overlap check
load-path precheck
connector family filtering
drilling / reinforcement dependency
structural rule-checker readiness
```

## Abbau/Aufbau Example 1 — Wand–Decke

Abbau/Aufbau lists two execution-planning variants for **Wand–Decke**:

```text
Wand - Decke
→ nachträglicher Bewehrungsanschluss + Verguss
→ Schraubanker mit Flachstahlhalter
```

Structural Interface Geometry generates:

```text
wall-top-bearing port
slab-edge-bearing port
line-bearing-zone at wall top
slab-edge support zone
post-installed-rebar-zone
grout-joint-zone
flat-steel-holder-zone
anchor-candidate-zone
edge-distance geometry
```

The generator does not approve the anchor.  
The system later needs:

```text
reinforcement position
anchor spacing
edge distance
structural proof
fire context if exposed steel is used
```

## Abbau/Aufbau Example 2 — Stütze–Decke

Abbau/Aufbau lists several **Stütze–Decke** variants:

```text
Stütze - Decke
→ nachträglich montierter Edelstahldorn
→ Winkelverbinder
→ nachträglicher Bewehrungsanschluss + Verguss auf neuem Stahlbetonträger
→ Auflager auf Stahlträger
```

Structural Interface Geometry generates:

```text
column-head-bearing port
slab point-support candidate region
dowel-candidate-zone
angle-connector-zone
steel-beam-support-zone
new-beam support interface zone
punching-sensitive interface region
```

The system later marks:

```text
punching check required
local bearing check required
connector capacity required
fire cover possibly required for steel connector
```

---

# 6. Package 2 — Energy / Envelope Geometry

## Domain Question

```text
Where does the component participate in the thermal envelope, moisture boundary, roof, facade, ground contact, or U-value-relevant assembly?
```

## Important Accuracy Rule

Energy / Envelope must remain **face-, surface-, edge-, and layer-based**.  
Do not force it into connector language. Use ports only for actual interface conditions.

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

## Energy Interface Ports

Only where useful:

```text
thermal-envelope-interface
insulation-layer-interface
roof-build-up-interface
ground-contact-interface
facade-interface
thermal-bridge-edge
envelope-penetration-zone
```

## Does Not Own

```text
final U-value proof
full layer build-up
GEG compliance
moisture proof
thermal bridge Psi-value
energy certificate
```

## System Uses This Package For

```text
rough U-value precheck
insulation requirement flag
thermal bridge warning
moisture exposure warning
envelope rule readiness
```

## Abbau/Aufbau Example 1 — Reused 200 mm Concrete Wall in Exterior Wall

Abbau/Aufbau gives an exterior-wall example with a reused **200 mm Stahlbetonwand**, where the concrete thermal conductivity must be assumed or measured and insulation thickness is determined to meet the GEG U-value requirement.

Energy / Envelope Geometry generates:

```text
outer broad face candidate
inner broad face candidate
200 mm U-value-relevant thickness
facade interface face
insulation-layer interface face
edge thermal bridge candidates
```

The system later calculates:

```text
R_concrete = thickness / lambda_concrete
U_rough = 1 / (Rsi + R_concrete + Rse)
```

Abbau/Aufbau notes a reinforced concrete thermal conductivity assumption of **2.3 W/mK** for density 2.3 t/m³ and 1% reinforcement in its example.

## Abbau/Aufbau Example 2 — Reused Slab Used as Roof or Exterior Floor

If a reused slab is used as roof or as a floor exposed to outside / ground climate, Energy / Envelope Geometry generates:

```text
top roof candidate face
bottom interior candidate face
slab-edge thermal bridge zone
roof-build-up interface
insulation interface
moisture-risk top face
```

The system later requires:

```text
project envelope context
full roof / floor build-up
insulation layer data
U-value target
thermal bridge assessment
```

---

# 7. Package 3 — TGA / Openings Interface Geometry

## Domain Question

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

## TGA Ports

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

## Does Not Own

```text
approval of drilling
fire sealing proof
acoustic sealing proof
service route design
reinforcement conflict proof
```

## System Uses This Package For

```text
service opening reuse
core drilling warning
TGA route coordination
penetration blocked / allowed precheck
conflict with structural zones
```

## Abbau/Aufbau Example 1 — Existing Openings in Bauteilkatalog

The Abbau/Aufbau Bauteilkatalog includes **Öffnungsmaße** where present.

TGA / Openings Geometry generates:

```text
existing-opening-port
opening position
opening size
edge distance
possible service reuse candidate
```

The system later checks:

```text
is the opening structurally acceptable?
does it conflict with reinforcement?
can it be used for services?
does it require fire/acoustic sealing?
```

## Abbau/Aufbau Example 2 — Core Drilling as Evidence / Penetration Issue

Abbau/Aufbau discusses core drilling in the context of material testing, for example carbonation testing. In a design system, a similar geometric operation can also be represented as a **core-drilling candidate**.

TGA / Openings Geometry generates:

```text
core-drilling-candidate zone
diameter candidate
depth candidate
edge distance
relation to structural bearing zones
```

The system later blocks or warns if:

```text
reinforcement position is unknown
zone overlaps structural interface
edge distance is insufficient
fire/acoustic/service proof is missing
```

---

# 8. Package 4 — Semantic / Architectural Interface Geometry

## Domain Question

```text
What spatial, visual, facade, rhythm, alignment, or reuse-expression relation can this component create?
```

## Important Accuracy Rule

This is the package where it is most useful to lean toward **interfaces**, not just faces.  
The geometry should be described as architectural relations.

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

## Semantic / Architectural Interface Ports

These are not mechanical connectors.  
They are architectural relation ports.

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

## Does Not Own

```text
beauty judgment
final design intent
structural validity
energy validity
fire compliance
```

## System Uses This Package For

```text
visible reuse preference
room layout logic
facade rhythm logic
alignment / grid logic
architectural warning
design preference scoring
```

## Abbau/Aufbau Example 1 — Deckenplatte as Ceiling / Floor Expression

For slab **DE_1OG_001**, Semantic / Architectural Interface Geometry generates:

```text
top face → floor-surface-interface
bottom face → ceiling-visible-interface
long edge → exposed-edge-interface
slab joint → joint-line-interface
repeated slab width → grid-continuation-interface
component ID location → reuse-identity-interface
```

The system later can support design preferences such as:

```text
visible reuse = high
regular grid = high
tolerance visibility = medium
```

## Abbau/Aufbau Example 2 — Reused Wall as Room / Facade Interface

For a reused wall panel, Semantic / Architectural Interface Geometry generates:

```text
inner broad side → room-boundary-interface
outer broad side → facade-rhythm-interface
vertical edge → joint-line-interface
top edge → datum-alignment-interface
surface marks → visible-reuse-interface
```

The system later evaluates:

```text
does this wall support cellular rooms?
does it form a facade rhythm?
should reuse traces remain visible?
does the joint line align with neighboring elements?
```

---

# 9. Package 5 — Logistics / Assembly Interface Geometry

## Domain Question

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

## Logistics Ports

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

## Does Not Own

```text
lifting proof
crane capacity decision
transport permit
site logistics plan
assembly sequence approval
```

## System Uses This Package For

```text
mass and lifting precheck
storage orientation warning
transport envelope check
assembly access warning
temporary bracing requirement
installation sequence compatibility
```

## Abbau/Aufbau Example 1 — Slab Storage

Abbau/Aufbau recommends that slabs should be stored lying down, with elements separated by protective timber, and protected from weather where possible.

Logistics / Assembly Interface Geometry for a slab generates:

```text
lying-flat storage interface
stacking support zones
timber-separator contact zones
transport envelope
center-of-gravity reference
assembly access along bearing edges
```

The system later produces:

```text
recommended storage orientation = lying
separator required = true
weather protection recommended = true
lifting proof required if lifting points unknown
```

## Abbau/Aufbau Example 2 — Wall / Column Storage

Abbau/Aufbau notes that walls and columns should generally be stored standing, because reinforcement was designed for those load cases.

Logistics / Assembly Interface Geometry generates:

```text
standing storage interface
base support zone
temporary bracing interface
transport support zone
damage-sensitive edge zones
crane pick candidate zone
```

The system later checks:

```text
standing support available?
temporary bracing required?
is transport / storage orientation compatible?
are damage-sensitive edges protected?
```

---

# 10. Package 6 — Evidence Geometry Overlay

## Domain Question

```text
Where is measured, scanned, damaged, tested, uncertain, or evidence-relevant geometry located?
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

## Evidence Geometry Points / Zones

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

## Does Not Own

```text
final material acceptance
structural safety
durability decision
repair design
approval decision
```

## System Uses This Package For

```text
missing evidence warnings
drilling / anchor blocking
damage overlap with bearing zones
damage overlap with visible reuse interfaces
durability warnings
confidence scoring
engineering-required flags
```

## Abbau/Aufbau Example 1 — Rebar Scan / Bewehrungslage

Abbau/Aufbau emphasizes archive drawings, static calculations, formwork and reinforcement plans; if reinforcement plans are unavailable, reinforcement must be detected.

Evidence Geometry Overlay generates:

```text
rebar-detected-zone
unknown-rebar-zone
cover-depth zones
anchor-blocking zones
scan confidence zones
```

The system later checks:

```text
does anchor candidate zone intersect rebar?
is drilling allowed?
is Bewehrungslage missing?
is structural proof required?
```

## Abbau/Aufbau Example 2 — Carbonation / Core Sample Location

Abbau/Aufbau discusses carbonation testing with a core sample.

Evidence Geometry Overlay generates:

```text
core-sample-point
carbonation-test-point
sample depth geometry
tested surface zone
confidence zone
```

The system later checks:

```text
carbonation depth known?
cover depth known?
corrosion risk warning?
durability evidence complete?
```

---

# 11. Final Package Summary

## Clean Package Tree

```text
GEOMETRY GENERATOR PACKAGES
│
├── 0. Base Geometry
│   Neutral primitives: dimensions, faces, edges, volume, openings.
│
├── 1. Structural Interface Geometry
│   Structural bearing, support, load-transfer, anchor, dowel, grout,
│   steel-support and pair-type interface geometry.
│
├── 2. Energy / Envelope Geometry
│   Thermal faces, envelope boundaries, U-value thickness,
│   insulation interfaces, moisture and thermal-bridge zones.
│
├── 3. TGA / Openings Interface Geometry
│   Openings, penetrations, service routes, cable/pipe ports,
│   core-drilling candidates.
│
├── 4. Semantic / Architectural Interface Geometry
│   Room, facade, visibility, rhythm, datum, grid,
│   joint-line and reuse-expression interfaces.
│
├── 5. Logistics / Assembly Interface Geometry
│   Lifting, transport, storage, stacking, assembly access,
│   temporary bracing and protection interfaces.
│
└── 6. Evidence Geometry Overlay
    Rebar, damage, cracks, samples, tests, unknown zones,
    and confidence geometry.
```

## Core Boundary

```text
Generator:
creates domain geometry.

System:
interprets domain geometry with catalogue data, evidence, rules, and project defaults.

Rule Checker:
evaluates active design actions such as connecting Component A to Component B.
```

## Example Boundary

```text
Generator:
creates slab-edge-bearing zone.

System:
knows this can be compatible with wall-top-bearing.

Rule Checker:
checks whether the actual placed slab and wall have enough overlap,
known reinforcement, allowed connector, fire treatment, and LCA data.
```

---

# 12. Two Complete Abbau/Aufbau Example Flows

## Example A — Deckenplatte DE_1OG_001

### Input

```text
component_id: DE_1OG_001
typology: slab / Deckenplatte
material: reinforced concrete
dimensions: 4500 × 2300 × 180 mm
volume: 1.863 m³
mass: ca. 4.1 t
```

### Package Outputs

```text
Base Geometry:
dimensions, faces, edges, volume, center geometry

Structural Interface Geometry:
slab-edge-bearing zones,
span candidate,
anchor candidate zones,
slab-edge-bearing ports

Energy / Envelope Geometry:
roof/exterior-floor candidates,
U-value-relevant thickness 180 mm,
slab-edge thermal bridge candidates

TGA / Openings Geometry:
opening candidates,
service penetration candidates,
core-drilling candidate zones

Semantic / Architectural Interface Geometry:
floor-surface interface,
ceiling-visible interface,
exposed-edge interface,
grid-continuation interface,
reuse-identity interface

Logistics / Assembly Interface Geometry:
lying-flat storage geometry,
transport envelope,
stacking support zones,
assembly access along bearing edges

Evidence Geometry Overlay:
rebar scan zones if available,
damage zones if mapped,
sample points if tested,
unknown evidence zones
```

### System Interpretation

```text
mass = known from catalogue / calculable from volume and density
transport GWP can be calculated if transport distance is known
structural capacity remains engineering_required unless proof exists
drilling remains blocked or warning if reinforcement position is unknown
```

---

## Example B — Wand–Decke Connection in Abbau/Aufbau

### Input

```text
component A: reused wall / Wand
component B: reused slab / Decke
pair type: Wand - Decke
connection families from Abbau/Aufbau:
- nachträglicher Bewehrungsanschluss + Verguss
- Schraubanker mit Flachstahlhalter
```

### Package Outputs

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

### System Interpretation

```text
connection can be checked only after:
bearing overlap is known,
reinforcement evidence is known,
connector family is selected,
fire context is known,
assembly access is possible.

If reinforcement is unknown:
anchor / drilling is warning or blocked.

If exposed steel connector is fire-relevant:
fire cover or fire detail is required.
```

---

# 13. Final Rule

```text
Do not create one generic connector package.

Create domain packages.

Each package owns the connector/interface geometry that belongs to its domain.
```

This creates a system that is both minimal and accurate:

```text
Structural connector logic stays structural.
Energy remains boundary / surface / layer based.
TGA owns penetrations and service ports.
Semantic owns architectural interfaces.
Logistics owns lifting / assembly / storage interfaces.
Evidence overlays all of them.
```
