# Minimal Package Abstractions for the Component System  
## Polished Version with Abbau/Aufbau, SlabBeamColumnFragment, and ReCreate Examples

**Purpose**  
This document defines a minimal, clean package structure for reclaimed-component design. It follows the system model:

```text
Component → Package → Representation → Properties → Connectors → Ports → Rules / checks
```

The goal is to avoid over-modeling. The system should store only the abstractions needed for **connection, calculation, warning, compatibility, and design decisions**.

---

# 1. Source Basis

## 1.1 Abbau/Aufbau Handbuch

The Abbau/Aufbau handbook is used for the Bauteilkatalog logic, reinforced-concrete connection examples, logistics, energy prechecks, and evidence requirements.

Important points used here:

- The Bauteilkatalog contains ID, dimensions, opening dimensions, volume, mass, element type, and can be extended with concrete and reinforcement investigations.
- Example element **DE_1OG_001** is listed as a Deckenplatte with **4500 × 2300 × 180 mm**, **1.863 m³**, and **ca. 4.1 t**.
- The handbook gives connection examples for pairs such as **Wand–Decke** and **Stütze–Decke**.
- Relevant connection families include **Schraubanker**, **Edelstahldorn**, **Winkelverbinder**, **nachträglicher Bewehrungsanschluss + Verguss**, **Flachstahlhalter**, and **Stahlträger-Auflager**.
- Logistics depends on ID, catalogue, transport, storage order, weather protection, and safe handling.
- Energy / Bauphysik is relevant when reused concrete elements become part of the building envelope.

Source: Abbau/Aufbau, *Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden*, 2023.

## 1.2 Abbau/Aufbau Masterarbeit 2020

The Masterarbeit 2020 is used for the **SlabBeamColumnFragment** example.

Important points used here:

- The thesis studied how a reinforced-concrete building can be cut into elements and reused in a new building.
- It identifies spatially valuable fragments such as **Stützen vor Fenstern**, **Nische hinter Stütze**, and **Große Stütze in kleinem Raum**.
- The final project uses many cut concrete parts.
- The used parts rest on a semi-precast reinforced-concrete beam and are force-locked with a post-installed reinforcement connection.

**Important note:**  
`SlabBeamColumnFragment` is not a named source object. It is a proposed system typology derived from the fragment logic: a monolithic concrete fragment that contains a slab region, an integrated beam region, and a column section.

## 1.3 ReCreate

ReCreate is used for the precast reuse example.

Important points used here:

- The Netherlands pilot uses reclaimed hollow-core slabs and precast facade elements from the Prinsenhof building.
- The Dutch donor building had hollow-core slabs spanning from load-bearing facade to load-bearing facade.
- Wet connections required sawing at longitudinal joints; elements were hoisted and transported.
- A mock-up is intended to test dimensional tolerance and reconnecting reclaimed elements into a robust structure.
- The Finland pilot includes columns, beams, hollow-core slabs, sandwich facade elements, BIM inventory, coding / QR tracing, testing, and recalculation according to current structural design codes.

---

# 2. Core System Rule

## 2.1 Minimal Abstraction

Do not model every real-world detail. Model only what the system needs to make a decision.

A detail belongs in the system only if it supports one of these actions:

- connecting components
- calculating a value
- producing a warning
- checking compatibility
- supporting a design decision

## 2.2 Representation, Property, Connector, Port

| Term | Meaning | Example |
|---|---|---|
| **Representation** | A simplified model of the component for one package. | A slab as a structural plate. |
| **Property** | Information describing a representation. | thickness, mass, capacity status, visibility status |
| **Connector** | A placed actionable handle on a representation. | slab bearing edge |
| **Port** | A semantic compatibility type referenced by a connector. | `bearing_side` |

A connector has geometry.  
A port has compatibility meaning.  
A rule checks compatible ports through connector geometry.

## 2.3 Connector Rule

Do not place connectors on every face or edge.  
Create a connector only if the system uses it for a rule, connection, warning, calculation, or design operation.

Correct:

- slab edge used for support → connector
- wall top used as support → connector
- opening used for a service route → connector
- visible surface checked for obstruction → connector

Incorrect:

- every slab edge → connector
- every visible face → connector
- every descriptive property → connector

---

# 3. Final Package Set

The system has seven packages:

| No. | Package | Core representation | Connector logic |
|---:|---|---|---|
| 0 | **Base Geometry** | neutral geometric body | no connectors |
| 1 | **Structural** | force-transfer abstraction | minimal structural connectors |
| 2 | **Energy / Envelope** | thermal / envelope abstraction | only continuity, sealing, bridge connectors |
| 3 | **TGA / Openings** | service / opening abstraction | route and penetration connectors |
| 4 | **Semantic / Architectural** | design-handle abstraction | only actionable design handles |
| 5 | **Logistics / Assembly** | handling abstraction | lifting, storage, transport, access handles |
| 6 | **Evidence Overlay** | evidence location abstraction | no connectors; modifies other connectors |

---

# 4. Minimal Connector and Port Vocabulary

## 4.1 Structural

| Connector | Port | Meaning |
|---|---|---|
| `bearing_support` | `bearing_side` / `support_side` | A load can be supported or transferred by bearing. |
| `joint_connection` | `member_side` | Two member sides need joint alignment or joining. |
| `anchor_connection` | `anchor_side` | A connector depends on anchors, screws, dowels, or drilled fixings. |
| `continuity_connection` | `continuity_side` | Force-locking or reinforcement continuity is needed. |
| `support_transfer` | `transfer_side` | Load is transferred through an intermediate or local support condition. |

## 4.2 Energy / Envelope

| Connector | Port | Meaning |
|---|---|---|
| `thermal_continuity` | `thermal_side` | Thermal boundary must continue. |
| `insulation_continuity` | `insulation_side` | Insulation layer must continue. |
| `penetration_sealing` | `penetration_side` | Opening or service penetration must be sealed. |
| `thermal_bridge_warning` | `bridge_side` | Single-sided warning zone for thermal bridge risk. |

## 4.3 TGA / Openings

| Connector | Port | Meaning |
|---|---|---|
| `route_continuity` | `route_side` | Service route can continue. |
| `opening_use` | `opening_side` | Existing opening can be reused. |
| `drilling_candidate` | `drilling_side` | New core drilling or penetration may be considered. |
| `blocked_conflict` | `blocked_side` | Zone conflicts with service routing or drilling. |

## 4.4 Semantic / Architectural

| Connector | Port | Meaning |
|---|---|---|
| `access_handle` | `access_port` | Approach, passage, or spatial access is checked. |
| `attachment_handle` | `attachment_port` | Architectural attachment or module relation is checked. |
| `stack_handle` | `top_port` / `bottom_port` | Stacking, vertical relation, or level relation is checked. |
| `side_handle` | `side_port` | Side relation, room boundary, or orientation is checked. |
| `opening_handle` | `opening_port` | Architectural opening or access alignment is checked. |
| `alignment_handle` | `alignment_port` | Grid, datum, rhythm, or joint alignment is checked. |
| `visibility_constraint_handle` | `visibility_port` | Visibility, reuse expression, or obstruction is checked. |

## 4.5 Logistics / Assembly

| Connector | Port | Meaning |
|---|---|---|
| `lifting_handle` | `lifting_port` | Lifting feasibility or crane access is checked. |
| `storage_handle` | `storage_port` | Storage orientation or support is checked. |
| `transport_handle` | `transport_port` | Transport envelope or load securing is checked. |
| `access_handle` | `access_port` | Assembly access is checked. |
| `protection_handle` | `protection_port` | Damage or weather protection is checked. |
| `temporary_bracing_handle` | `temporary_bracing_port` | Temporary stability is checked. |

## 4.6 Evidence Overlay

Evidence has **no connectors and no ports**.  
It modifies connectors from other packages.

Possible effects:

- confirmed
- warning
- blocked
- confidence reduced
- manual check required
- engineering required

---

# 5. Package 0 — Base Geometry

## Purpose

Base Geometry stores the neutral geometric body. It is the source from which other packages derive their own representations.

## Minimal Representation

The base representation contains only:

- typology
- geometry source
- units
- local axes
- bounding box
- length, width, height or thickness
- volume
- main faces
- main edges
- raw openings
- center of geometry
- geometry confidence

## Connectors and Ports

None.

Base Geometry never creates connectors. A base edge, surface, or opening becomes a connector only when another package gives it meaning.

## Checks

- geometry exists
- dimensions are extractable
- volume is extractable
- units are valid
- orientation is known or marked unknown

## Example 1 — Abbau/Aufbau DE_1OG_001

The slab **DE_1OG_001** is represented as one neutral slab body. The base geometry stores its dimensions, volume, main faces, main edges, and raw opening status. It does not yet decide whether a long edge is structural, visible, thermal, or logistical.

## Example 2 — SlabBeamColumnFragment

The fragment is represented as one continuous monolithic body, but the base geometry identifies three raw regions: slab-like region, integrated beam-like region, and column-like region. These are not separate components. They are raw geometric regions inside one component.

## Example 3 — ReCreate Hollow-Core Slab

The ReCreate hollow-core slab is represented as a precast slab body with longitudinal voids, end faces, long edges, and net volume. No connector is created at this level. The longitudinal joint becomes meaningful only in the Structural or Semantic package.

---

# 6. Package 1 — Structural

## Purpose

The Structural package stores the minimal abstraction needed for force transfer, support, anchoring, continuity, and structural warnings.

## Minimal Representation

The representation should be broken down into simple structural abstractions:

| Real geometry | Structural abstraction |
|---|---|
| slab region | plate |
| wall region | wall plate |
| beam region | beam line |
| column region | column line |
| local support patch | support node |
| joint / cast connection | continuity zone |
| complex monolithic fragment | graph of plate + beam line + column line + transfer node |

This avoids vague names like `monolithic_structural_fragment`.  
A complex component should become a small structural graph.

## Minimal Properties

- structural role
- span direction status
- support condition candidates
- bearing zone status
- capacity status
- reinforcement evidence status
- minimum bearing rule
- structural opening status
- damage relevance status

## Minimal Connectors and Ports

Use only:

- `bearing_support` with `bearing_side` or `support_side`
- `joint_connection` with `member_side`
- `anchor_connection` with `anchor_side`
- `continuity_connection` with `continuity_side`
- `support_transfer` with `transfer_side`

## Minimal Checks

| Rule | Checks |
|---|---|
| `bearing_side → support_side` | overlap, direction, minimum bearing length |
| `member_side → member_side` | alignment, continuity, joint geometry |
| `anchor_side → support_side` | edge distance, reinforcement conflict, anchor feasibility, capacity |
| `continuity_side → continuity_side` | reinforcement continuity, force-locking requirement, grout or cast joint geometry |
| `transfer_side → support_side / bearing_side` | transfer path, local bearing, intermediate support validity |

## What Stays Outside

The structural package does not prove final capacity, punching safety, shear resistance, fire cover, or approval. It only creates the rule-facing structural abstraction.

## Example 1 — Abbau/Aufbau Wand–Decke

For a reused slab connected to a reused wall, the structural representation uses only three slab-side handles: a bearing support at the slab edge, an anchor connection zone if a screw anchor or flat-steel holder is used, and a continuity connection zone if post-installed reinforcement with grout is used.

The wall representation has a support-side connector at the wall top. If anchors are used, the wall top also receives the anchor. If a post-installed reinforcement connection is used, the wall top becomes part of a continuity-side relation.

The system checks bearing overlap, direction, minimum bearing length, anchor edge distance, reinforcement conflict, and whether continuity can be force-locked. The Abbau/Aufbau detail names remain system-level connector families, not separate connector types.

## Example 2 — SlabBeamColumnFragment

The fragment is not represented as one vague structural object. It is decomposed into a small structural graph:

- slab region → plate
- integrated beam region → beam line
- column section → column line
- intersection of slab, beam, and column → transfer node
- cut face with possible rebar exposure → continuity zone

Only four structural handles are needed: a bearing support where the slab region can rest, a support transfer at the beam region, a support-side handle at the column base, and a continuity connection at the cut face if it must be force-locked to a new member.

This keeps the monolithic reality but gives the checker clear abstract handles.

## Example 3 — ReCreate Hollow-Core Slab

The hollow-core slab is represented as a spanning plate or one-way slab member. It has bearing-support handles at its two ends and a joint-connection handle along the longitudinal joint line. The longitudinal joint is important because ReCreate Netherlands describes sawing along longitudinal joints and later reconnecting elements in a mock-up.

The structural checks stay minimal: end bearing, alignment, tolerance, and joint reconnection. Capacity remains evidence- or recalculation-dependent.

---

# 7. Package 2 — Energy / Envelope

## Purpose

The Energy / Envelope package stores only what is needed for thermal continuity, insulation continuity, penetration sealing, and thermal bridge warnings.

## Minimal Representation

Use face-, layer-, and edge-based abstractions. Do not force energy into connector language where surfaces are more accurate.

Representation types:

- thermal boundary surface
- insulation continuity model
- envelope penetration model
- thermal bridge risk model
- moisture boundary model

## Minimal Properties

- thermal role
- inside / outside status
- area
- thickness
- lambda status
- U-value status
- insulation status
- moisture risk status
- envelope context status

## Minimal Connectors and Ports

Use only:

- `thermal_continuity` with `thermal_side`
- `insulation_continuity` with `insulation_side`
- `penetration_sealing` with `penetration_side`
- `thermal_bridge_warning` with `bridge_side`

## Minimal Checks

- thermal boundary continuity
- insulation continuity
- gap check
- sealing requirement
- air tightness
- moisture risk
- thermal bridge warning
- rough U-value precheck

## What Stays Outside

The package does not prove final U-value, moisture safety, energy certification, or full envelope compliance.

## Example 1 — Abbau/Aufbau 200 mm Concrete Wall

A reused 200 mm concrete wall used as exterior wall is represented as a thermal boundary surface. The system stores the concrete thickness, lambda status, and envelope context. The outer surface may receive an insulation-continuity connector, the perimeter may receive a thermal-continuity connector, and openings may receive penetration-sealing connectors.

The system can do a rough precheck using `R = thickness / lambda`, but the final U-value requires the full wall build-up.

## Example 2 — SlabBeamColumnFragment

The fragment only receives energy connectors if it is used at the envelope. If it remains interior, the package can stay inactive or context-required.

If used at the envelope, the cut face can become a thermal-continuity connector and the slab-beam-column intersection can become a thermal-bridge-warning zone. No extra connectors are needed unless a penetration or insulation continuity must be checked.

## Example 3 — ReCreate Hollow-Core Slab

A ReCreate hollow-core slab gets energy representation only if used as roof, exterior floor, or another thermal boundary. The top surface may become an insulation-continuity handle, the slab edge may become a thermal-bridge-warning zone, and service openings may require penetration sealing.

The hollow cores are properties of the thermal model, not separate connectors unless they are used for an actual route or penetration.

---

# 8. Package 3 — TGA / Openings

## Purpose

The TGA / Openings package stores the minimal abstraction needed for openings, service routes, drilling candidates, and blocked zones.

## Minimal Representation

Representation types:

- opening model
- route model
- drilling candidate model
- blocked zone model
- service penetration model

## Minimal Properties

- opening size
- opening axis
- opening depth
- route diameter
- edge distance
- clearance status
- drilling status
- blocked status
- relation to structural zones
- relation to reinforcement status

## Minimal Connectors and Ports

Use only:

- `route_continuity` with `route_side`
- `opening_use` with `opening_side`
- `drilling_candidate` with `drilling_side`
- `blocked_conflict` with `blocked_side`

## Minimal Checks

| Rule | Checks |
|---|---|
| `route_side → route_side` | route alignment, diameter match, clearance |
| `opening_side → route_side` | diameter fits, edge distance, route continuity |
| `drilling_side → route_side` | diameter fits, rebar conflict, structural zone conflict, edge distance |
| `blocked_side` | conflict with route or drilling |

## What Stays Outside

This package does not approve a service design, fire sealing, acoustic sealing, or structural approval of a new penetration.

## Example 1 — Abbau/Aufbau Opening

If the Bauteilkatalog records an opening, the TGA package creates an opening-use connector only if the design can use that opening for a service, access, or routing decision. If no service route uses it, the opening remains only a property.

The system checks size, edge distance, relation to structural zones, and reinforcement status before it allows routing through the opening.

## Example 2 — SlabBeamColumnFragment

The fragment has structural zones that make routing difficult. The slab-like region may receive one drilling-candidate connector if a route is proposed. The beam region and column region can become blocked-conflict zones because they are likely load-transfer regions.

No opening connector is created unless an actual opening exists or a route is being proposed.

## Example 3 — ReCreate Hollow-Core Slab

The hollow-core slab can have a route-continuity connector along a hollow-core void only if the system allows the void to be considered for routing. A new drilling candidate is separate and must be checked against structure, reinforcement, and void geometry.

The hollow core itself is not automatically a service connector; it becomes one only when used for routing.

---

# 9. Package 4 — Semantic / Architectural

## Purpose

The Semantic / Architectural package stores actionable architectural design handles. It should not store every visual or semantic description as a connector.

## Minimal Representation

Representation types:

- architectural component model
- room boundary model
- facade relation model
- visibility model
- alignment model
- access model
- stacking model

## Minimal Properties

- architectural role
- spatial role
- visible status
- reuse expression status
- surface condition status
- grid relation status
- room relation status
- facade relation status
- orientation status

## Minimal Connectors and Ports

Use only:

- `access_handle` with `access_port`
- `attachment_handle` with `attachment_port`
- `stack_handle` with `top_port` or `bottom_port`
- `side_handle` with `side_port`
- `opening_handle` with `opening_port`
- `alignment_handle` with `alignment_port`
- `visibility_constraint_handle` with `visibility_port`

## Minimal Checks

- access alignment
- clearance
- architectural attachment compatibility
- stacking direction
- vertical alignment
- side alignment
- room boundary continuity
- opening alignment
- grid alignment
- datum alignment
- joint alignment
- visibility obstruction
- surface condition warning

## What Stays Outside

The package does not judge beauty, final design intention, structure, energy, or fire compliance.

## Example 1 — Abbau/Aufbau DE_1OG_001

For the slab, the top surface can remain a property such as “possible floor surface.” The bottom surface becomes a visibility-constraint connector only if the design wants to expose it as a ceiling. A long edge becomes an alignment connector only if grid or joint alignment is checked.

The slab therefore needs only two likely architectural connectors: one alignment handle on the joint edge and one visibility handle on the bottom face if visible reuse is part of the design.

## Example 2 — SlabBeamColumnFragment

The fragment is architecturally important because its combined slab, beam, and column geometry can create a niche, a column-in-room condition, or a strong spatial threshold.

The semantic representation does not need a separate connector for every face. It needs only the design handles that can be checked: an access handle for the niche entrance, a side handle for the column-room relationship, an alignment handle for the cut edge or beam line, and a visibility handle if the fragment should remain visually legible.

## Example 3 — ReCreate Hollow-Core Slab

For a reclaimed hollow-core slab, the most important semantic handles are usually module and joint alignment. A longitudinal joint can become an alignment handle. The top and bottom planes can become stack handles if the system checks vertical arrangement, level continuity, or module stacking.

Visibility is optional and should be modeled only if the slab underside or reuse identity is part of the architectural intention.

---

# 10. Package 5 — Logistics / Assembly

## Purpose

The Logistics / Assembly package stores only the handling abstraction needed for lifting, storage, transport, protection, access, and temporary assembly.

## Minimal Representation

Representation types:

- handling model
- transport model
- storage model
- lifting model
- assembly access model
- temporary bracing model
- protection model

## Minimal Properties

- mass
- transport dimensions
- center of gravity status
- storage orientation
- lifting status
- access status
- protection status
- temporary bracing status
- transport status

## Minimal Connectors and Ports

Use only:

- `lifting_handle` with `lifting_port`
- `storage_handle` with `storage_port`
- `transport_handle` with `transport_port`
- `access_handle` with `access_port`
- `protection_handle` with `protection_port`
- `temporary_bracing_handle` with `temporary_bracing_port`

## Minimal Checks

- lifting feasibility
- center of gravity
- crane access
- lifting proof required
- storage orientation
- support spacing
- separator required
- transport envelope
- load securing
- route constraints
- assembly access
- connector access
- weather protection
- edge protection
- temporary stability

## What Stays Outside

The package does not produce final lifting proof, crane design, transport permits, complete site logistics, or final assembly sequencing.

## Example 1 — Abbau/Aufbau DE_1OG_001

The slab needs a storage handle for lying storage, a transport handle for load securing and transport envelope, a lifting handle if it will be lifted, and a protection handle if edges or surfaces need protection during storage.

Its catalogue mass of ca. 4.1 t supports logistics prechecks, but lifting proof still needs separate evidence.

## Example 2 — SlabBeamColumnFragment

The fragment has higher handling complexity because the slab, beam, and column regions create an irregular center of gravity and fragile cut faces. It needs a lifting handle, a storage handle, a protection handle for cut faces and damage-sensitive edges, and possibly a temporary-bracing handle if it is unstable during assembly.

It should not get generic lifting connectors on every region. One or two candidate lifting handles are enough until a lifting concept is engineered.

## Example 3 — ReCreate Hollow-Core Slab

The ReCreate slab needs lifting, transport, and storage handles. These reflect the pilot reality: elements were hoisted, transported, coded or traced, and stored. QR tracing belongs to evidence / identity, not to the logistics connector itself.

The logistics package checks transport dimensions, load securing, storage support, and whether lifting data is complete.

---

# 11. Package 6 — Evidence Overlay

## Purpose

The Evidence Overlay package records where evidence is located and how it affects connectors from other packages.

Evidence never creates connectors.  
Evidence modifies connector confidence or status.

## Minimal Representation

Representation types:

- scan overlay
- damage overlay
- test point overlay
- photo annotation overlay
- confidence overlay
- unknown zone overlay

## Minimal Properties

- evidence type
- location
- confidence
- source
- date
- affected package
- affected connector
- affected port
- effect
- reason
- evidence status

## Connectors and Ports

None.

## Minimal Effects

- confirmed
- warning
- blocked
- confidence reduced
- manual check required
- engineering required

## Minimal Checks

- if evidence overlaps a connector, modify connector status
- if unknown zone overlaps a connector, mark warning or blocked
- if damage overlaps a connector, mark warning or manual check
- if rebar scan clears an anchor zone, allow engineering check
- if test data confirms a material property, increase confidence

## Example 1 — Abbau/Aufbau Rebar Evidence

If reinforcement position is unknown, the evidence overlay marks affected anchor connections as warning or blocked. If a scan confirms a clear anchor zone, the anchor connection can proceed to engineering check.

The evidence overlay does not create an anchor connector. It only modifies the structural anchor connector.

## Example 2 — SlabBeamColumnFragment Cut Face Evidence

The fragment’s cut face may expose or interrupt reinforcement. The evidence overlay can mark the continuity connection as engineering required, reduce confidence in support transfer, or warn if damage overlaps a visible architectural handle.

Evidence connects the structural, semantic, and logistics consequences without inventing new connectors.

## Example 3 — ReCreate Testing and QR Evidence

ReCreate’s BIM inventory, coding system, QR tracing, testing, and recalculation evidence can increase confidence in base geometry, logistics traceability, and structural capacity status.

QR evidence confirms identity and traceability. Loading tests or recalculation evidence can increase structural confidence. Unknown joint damage can still mark joint connections as manual-check required.

---

# 12. Compact Global Compatibility Rules

Keep the global rule list short.

| Rule | Compatible ports | Minimal checks |
|---|---|---|
| structural bearing | `bearing_side → support_side` | overlap, direction, bearing length |
| structural anchor | `anchor_side → support_side` | edge distance, rebar conflict, feasibility |
| structural continuity | `continuity_side → continuity_side` | alignment, reinforcement continuity, force-locking |
| structural transfer | `transfer_side → support_side / bearing_side` | transfer path, local bearing |
| energy continuity | `thermal_side → thermal_side` | boundary continuity |
| insulation continuity | `insulation_side → insulation_side` | layer continuity, gap |
| envelope penetration | `penetration_side → thermal_side / insulation_side` | sealing, air tightness, moisture |
| TGA route | `route_side → route_side` | route alignment, clearance |
| TGA opening | `opening_side → route_side` | diameter, edge distance, structural conflict |
| TGA drilling | `drilling_side → route_side` | diameter, rebar conflict, structural conflict |
| semantic access | `access_port → access_port` | clearance, approach |
| semantic stacking | `top_port → bottom_port` | vertical alignment, level offset |
| semantic alignment | `alignment_port → alignment_port` | grid, joint, datum |
| logistics lifting | `lifting_port → process requirement` | lifting feasibility, center of gravity |
| logistics storage | `storage_port → storage condition` | orientation, support, separators |

---

# 13. Complete Example A — Abbau/Aufbau DE_1OG_001

The slab **DE_1OG_001** is the clean individual-component example.

## Minimal Component Data

- Typology: slab / Deckenplatte
- Material: reinforced concrete
- Dimensions: 4500 × 2300 × 180 mm
- Volume: 1.863 m³
- Mass: ca. 4.1 t

## Package Abstractions

Base Geometry stores the slab as a neutral body with dimensions, volume, faces, edges, and raw opening state.

Structural represents it as a plate with bearing support at relevant edges. Anchor and continuity connectors are added only if the design uses an Abbau/Aufbau connection family such as screw anchor, flat-steel holder, or post-installed reinforcement with grout.

Energy / Envelope stays inactive unless the slab becomes roof, exterior floor, or envelope component. Then it adds insulation continuity, thermal bridge warning, or penetration sealing connectors.

TGA / Openings adds opening-use or drilling-candidate connectors only when an opening exists or a route is proposed.

Semantic / Architectural adds alignment or visibility connectors only when the slab edge, underside, or grid becomes part of the design logic.

Logistics / Assembly adds storage, transport, lifting, and protection handles because mass, storage, and handling are always relevant for real reused concrete elements.

Evidence Overlay modifies the structural and logistics connectors if reinforcement, damage, or lifting evidence is missing.

---

# 14. Complete Example B — SlabBeamColumnFragment

The **SlabBeamColumnFragment** is a proposed system typology derived from the Abbau/Aufbau Masterarbeit fragment logic.

## Minimal Component Idea

It is one monolithic reclaimed concrete fragment with:

- a slab-like plate region
- an integrated beam-like line region
- a column-like line region
- cut faces and irregular spatial qualities

## Correct Abstract Representation

Do not model it as one vague `monolithic_structural_fragment`.

Use a small graph:

- slab region → plate
- beam region → beam line
- column region → column line
- slab-beam-column intersection → transfer node
- cut face → continuity zone, if force-locking is required

## Package Abstractions

Base Geometry stores the fragment as one continuous body with sub-regions, not separate components.

Structural decomposes it into plate, beam line, column line, transfer node, and continuity zone. The minimal connectors are bearing support, support transfer, and continuity connection.

Energy / Envelope only activates if the fragment is used at the envelope. The slab-beam-column junction may become a thermal bridge warning.

TGA / Openings treats the beam and column regions as likely blocked zones. A drilling candidate is created only if a service route is proposed.

Semantic / Architectural is especially important: the fragment may create a niche, a column-in-room situation, a spatial threshold, or visible reuse identity. Only access, side, alignment, and visibility handles are needed.

Logistics / Assembly uses lifting, storage, protection, and temporary bracing handles because the fragment is irregular and likely difficult to handle.

Evidence Overlay modifies continuity and support transfer confidence if cut-face rebar, damage, or material condition is unknown.

---

# 15. Complete Example C — ReCreate Hollow-Core Slab

The ReCreate example uses a reclaimed precast hollow-core slab.

## Minimal Component Idea

It is a one-way precast slab with:

- end bearing zones
- longitudinal joints
- hollow-core voids
- transport and tracing history
- testing or recalculation evidence

## Package Abstractions

Base Geometry stores the slab body, longitudinal voids, end faces, edges, and net volume.

Structural represents it as a one-way slab or spanning plate. It needs bearing support at the two ends and joint connection along the longitudinal edge. Capacity depends on testing or recalculation.

Energy / Envelope activates only if the slab is used as roof or exterior floor. It may add insulation continuity, thermal bridge warning, or penetration sealing.

TGA / Openings can treat a hollow core as route continuity only if the design explicitly uses it as a route. Otherwise, hollow cores remain properties.

Semantic / Architectural mainly uses alignment handles for module and joint alignment. Stack handles are added only if level or vertical stacking logic is checked.

Logistics / Assembly uses lifting, transport, and storage handles because ReCreate pilots involve hoisting, transport, storage, and tracing.

Evidence Overlay records BIM inventory, QR or coding data, testing, loading tests, and recalculation status. It modifies structural confidence and traceability, but it does not create connectors.

---

# 16. Final Clean Rule

Use properties for descriptions.  
Use connectors only for actionable handles.  
Use ports only for compatibility.  
Use evidence only to modify confidence, warnings, or blocked status.

The minimum system should therefore avoid long connector vocabularies and keep each package small:

- Base Geometry: no connectors
- Structural: 5 connector types
- Energy / Envelope: 4 connector types
- TGA / Openings: 4 connector types
- Semantic / Architectural: 7 connector types
- Logistics / Assembly: 6 connector types
- Evidence Overlay: no connectors

This is enough to support reclaimed component design without over-modeling every face, edge, or project-specific detail.
