# Deep research feeder — DesignMethodology + ArchitecturalOutput only

Revision note: design-description paragraphs were rewritten as project-specific architectural case notes. They are narrative context only and must not be used directly as node values.

Generated from the kept-project list in `kept_projects_agent_safe_design_nodes_only.md` and enriched with external source leads.

## Agent extraction rule

- **Create / update only these two node types:** `DesignMethodology` and `ArchitecturalOutput`.
- **Do not create new taxonomy/classes.** Map the candidate text onto existing Neo4j node labels/properties/relationships where possible.
- **Reclaimed/reused material must be the active driver.** Extract only when reused/reclaimed components shape form, space, structure, façade, circulation, atmosphere, construction method, module, detail, or aesthetic language.
- **Ignore material lists.** A list of reused items is evidence only unless it changes design logic or architectural output.
- **Ignore generic sustainability claims.** Do not extract from claims about carbon, circularity, or eco-design unless connected to a design effect.
- **Planned, competition, pilot and demonstrator projects remain valid projects.** Non-realised status is not a removal reason.
- **Low/DoNotExtract means:** keep project if it belongs elsewhere in the graph, but do not feed the two new nodes from weak reclaimed-material evidence.

## Suggested controlled values / clustering hints

### DesignMethodology clustering hints

Use these only as matching hints against existing graph vocabulary:

- `MaterialInventoryLedDesign` — material stock identified before design; design adapts to sizes/quantities/condition.
- `FormFollowsAvailability` — final form/layout/structure changes because of available reclaimed components.
- `HarvestMapOrUrbanMining` — scouting, cataloguing, donor-building mapping, material passport/database.
- `DesignForDisassembly` — reversible joints, no glue/wet fix, demountable kit, future reuse as design condition.
- `DonorRecipientReuseChain` — specific donor building/infrastructure supplies recipient project.
- `ReassemblyOrSpoliaComposition` — heterogeneous components recomposed as a legible new whole.
- `ResearchDemonstrator` — pilot/living-lab/project-sheet/research prototype where design method is tested.
- `AdaptiveReuseWithComponentRetention` — existing structural/envelope components retained and made active in new design.

### ArchitecturalOutput clustering hints

Use these only as matching hints against existing graph vocabulary:

- `ReclaimedStructuralExpression` — reused members shape/expose structure.
- `PatchworkFacadeOrComponentSkin` — reclaimed windows/bricks/panels create façade rhythm/collage.
- `ReclaimedInteriorAtmosphere` — reused finishes, partitions, fixtures make spatial character.
- `ModuleDimensionDrivenForm` — module/component dimensions govern form, grid, bay, detail.
- `DemountableKitArchitecture` — output is visibly a reversible kit/system.
- `IndustrialOrInfrastructuralSpolia` — overscale former infrastructure/industry parts become architecture.
- `BiobasedReclaimedHybridAtmosphere` — reclaimed components and bio/geo-sourced materials jointly define atmosphere.
- `PublicDidacticReuseIdentity` — architecture makes reuse visible as civic/educational message.

## Project feed entries

Everything in `SOURCE_EVIDENCE_IGNORE` is evidence/context only. Other agents should not create nodes from that block directly.

---

<a id="1-55-great-suffolk-street-london"></a>
## 1. 55 Great Suffolk Street, London

### MAPPING_ONLY — do not extract
- Project ID: `p_55_great_suffolk_street_london`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The extension treats reclaimed steel as the organiser of the intervention, not as a hidden substitution. By moving the new core outside the warehouse, the design gives second-hand members a clear structural and spatial role: they frame circulation, services, terraces and bridge connections while leaving the existing interiors more flexible. The architecture depends on the contrast between the retained brick warehouse and a visibly assembled steel addition whose proportions follow available stock.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** early-procurement design around available reclaimed steel sections; external-core strategy chosen so reclaimed steel could form a legible new service/circulation spine while existing floorplates stayed largely uninterrupted.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** new external core/amenity tower and bridge links visibly express a reclaimed-steel frame; circulation, servicing, and the old/new contrast become the architectural output of the reuse strategy.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- ASBP 55 Great Suffolk Street: https://asbp.org.uk/case-studies/55-great-suffolk-street
- NLA 55 Great Suffolk Street: https://nla.london/projects/55-great-suffolk-street
- Hawkins Brown 55 Great Suffolk: https://www.hawkinsbrown.com/projects/55-great-suffolk-street/

**Existing topology component hints**
- Reused steel profiles for external core

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="2-association-house-gr-ditz"></a>
## 2. Association house, Gröditz

### MAPPING_ONLY — do not extract
- Project ID: `p_association_house_groeditz`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
This case belongs to the East German precast-reuse lineage, where the building is designed from known concrete panel families rather than from a blank structural grid. The reused Dresden-type and WBS70 components imply a disciplined modular order: spans, wall positions and openings must negotiate what can be recovered, cut and certified. Its architectural interest lies less in surface expression than in turning standardised housing fragments into a small civic building with a new social programme.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Component-catalogue-led design; Specification/dimensional adaptation to reclaimed components; Donor-building / deconstruction-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Modular composition from reclaimed concrete/components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Reused Dresden-type precast concrete components
- Reused WBS70 precast panels

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="3-association-house-plauen"></a>
## 3. Association house, Plauen

### MAPPING_ONLY — do not extract
- Project ID: `p_association_house_plauen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Plauen uses the IW73/6 precast stock as a design framework. The project is best read as a translation exercise: domestic mass-housing components are reassigned to a public association building, so architectural decisions are governed by module size, panel handling, temporary storage and allowable modification. The output is a restrained concrete composition where reuse operates through proportion, assembly logic and the visible memory of industrialised construction rather than through decorative contrast.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Component-catalogue-led design; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching; Storage-supported reuse design; Donor-building / deconstruction-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Modular composition from reclaimed concrete/components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Reused IW73/6 precast concrete components

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="4-awm-m-nster-zirkul-rer-b-roausbau-3-og"></a>
## 4. AWM Münster – zirkulärer Büroausbau 3. OG

### MAPPING_ONLY — do not extract
- Project ID: `p_awm_muenster_circular_office`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The office fit-out is a design of second lives at interior scale. Old chair parts become wall cladding, cable trays shift into shelving and lighting carriers, and reused glass partitions organise workplace transparency. The project’s architectural value is in careful re-designation: components keep traces of former use but are composed into a coherent office atmosphere. It shows reuse as joinery, furnishing, partitioning and surface strategy rather than as structural spectacle.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular office-fit-out methodology combining reused furniture, reclaimed wood, urban-mined building materials, hempcrete/clay finishes, and disassemblable detailing.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** interior architecture reads as a demonstrator of reused assemblies: reclaimed wood structures, exposed natural finishes, reused furniture and reversible details shape the workplace atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- AWM Münster circular fit-out: https://www.jablonicka.com/work/95%2C6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-
- Cradle circular fit-out: https://cradle-mag.de/artikel/zirkulaerer-innenausbau.html

**Existing topology component hints**
- Fixed wall cladding from old chair parts
- Reused WC partitions
- Reused cable trays as shelves and lighting carriers
- Reused glass partitions and doors
- Reused wood for fixed built-ins

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="5-bedzed-beddington-zero-energy-development"></a>
## 5. BedZED / Beddington Zero Energy Development

### MAPPING_ONLY — do not extract
- Project ID: `p_bedzed_london_hackbridge`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
At BedZED, reclaimed steel and timber sit within a broader low-energy urban block, but they still affect the architectural reading of the project. The reused structural steel in workspace areas and reclaimed timber framing belong to a pragmatic palette of local recovery, compact planning and robust detailing. Reuse is not presented as collage; it supports a materially economical architecture where environmental ambition is embedded in construction choices, exposed workspaces and everyday building fabric.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Material-scouting-led design; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching; Regional sourcing-led design; Storage-supported reuse design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Reclaimed timber atmosphere or tectonic detail; Collage interior / reused partition and fit-out language; Structural grid or frame shaped by reclaimed steel

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Reused fixed secondary components
- Reused softwood wall studs
- Reused structural steel frame for workspaces

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="6-berlin-schildow-pilot-house-berlin-schildow-2nd-pilot-house"></a>
## 6. Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house

### MAPPING_ONLY — do not extract
- Project ID: `p_berlin_schildow_pilot_house`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Schildow converts the logic of large-panel housing into a detached-house prototype. The design starts from WBS70 concrete elements cut out of a donor building, so the architectural problem becomes how to reduce, transport and recombine oversized socialist housing components into a smaller residential scale. The result is a house whose proportions, wall rhythm and heaviness are inherited from the source system, making reuse legible through tectonic continuity rather than applied symbolism.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching; Regional sourcing-led design; Just-in-time reclaimed-component integration

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Modular composition from reclaimed concrete/components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Zugeschnittene WBS70-Stahlbetonfertigteile

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="7-bestandverplanzung-pavilion-m-nchen"></a>
## 7. Bestandverplanzung Pavilion, München

### MAPPING_ONLY — do not extract
- Project ID: `p_bestandverplanzung_pavilion_muenchen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The pavilion works like an architectural transplant. Concrete panels from the Olympic Village bungalows are not treated as anonymous raw material; their origin, format and previous assembly logic determine the scale and character of the new object. Design decisions centre on re-siting, recomposition and controlled incompleteness. The architectural quality comes from the tension between familiar prefabricated elements and their new pavilion role, turning urban demolition stock into a compact public fragment.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Urban-mining-led design; Specification/dimensional adaptation to reclaimed components

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Modular composition from reclaimed concrete/components; Reversible tectonic expression / temporary material-bank architecture; Relocated/reassembled building expression

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Betonfertigteil-Paneele aus Olympiadorf-Bungalows

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="8-big-dig-building-boston-cambridge"></a>
## 8. Big Dig Building, Boston/Cambridge

### MAPPING_ONLY — do not extract
- Project ID: `p_big_dig_building_boston`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The proposal reframes highway demolition debris as an architectural stockroom. Instead of designing a conventional building and then searching for recycled content, it imagines ramp, pier and roadway elements as the starting geometry for structure and enclosure. Its design relevance is speculative but strong: infrastructural scale, excessive load capacity and rough component identity would shape span, massing and facade language. The project is therefore a reuse concept for translating civil-engineering remnants into habitable architecture.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** prototype logic: treat infrastructural demolition waste as a ready-made stock of structural members and cladding rather than as scrap.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** proposed structural and envelope language derives from reused highway steel/concrete components, making infrastructure-scaled elements architectural.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Big Dig Building SSD: https://www.ssdarchitecture.com/works/residential/big-dig-building/

**Existing topology component hints**
- Geplante Big-Dig-Infrastrukturbauteile

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="9-big-dig-house-lexington-massachusetts"></a>
## 9. Big Dig House, Lexington, Massachusetts

### MAPPING_ONLY — do not extract
- Project ID: `p_big_dig_house_lexington_massachusetts`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The house domesticates pieces of the Boston highway system. Salvaged steel beams, roadway panels and pier-like components produce a structure with unusual mass, depth and load capacity for a private dwelling. The design accepts the scale and strength of infrastructure, using it to enable roof gardens, deep structural layers and a rugged material character. Its architectural quality comes from that mismatch: domestic rooms are held within an assembly logic borrowed from roads and bridges.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** prefabricated reassembly of salvaged I-93 highway steel and concrete; design accepts the overscale strength/geometry of infrastructure components as a domestic construction system.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** heavy salvaged beams, slabs, bridge-pier logic and roof-garden capacity create a house whose structure and spatial layering are defined by reclaimed highway elements.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Big Dig House Project Architecture: https://projectarchitecture.com/big-dig-house/
- ArchDaily Big Dig House: https://www.archdaily.com/24396/big-dig-house-single-speed-design

**Existing topology component hints**
- Wiederverwendete Inverset-Stahlbetonpaneele
- Wiederverwendete Ramp-, Pier- und Roadway-Komponenten
- Wiederverwendete Stahlträger und Stahlstützen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="10-biopartner-5-leiden-oegstgeest"></a>
## 10. BioPartner 5, Leiden / Oegstgeest

### MAPPING_ONLY — do not extract
- Project ID: `p_biopartner_5_leiden_oegstgeest`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
BioPartner 5 integrates reused elements into a technically demanding laboratory and office building rather than into an informal showcase. Reclaimed steel, partitions, paving, sanitary fixtures and demolition rubble are absorbed into a new institutional architecture where performance, certification and flexibility matter. The design challenge is to make circular components compatible with a clean, precise research environment. Its architectural output is a controlled circular identity: reuse is visible in selected surfaces and structure without undermining laboratory order.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** reuse-led circular shell: donor components and reclaimed materials are integrated into a new laboratory building while maintaining technical performance.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** facade/interior expression uses reused elements as visible parts of the circular identity of the biotech building.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Source should be verified against project documentation for exact reclaimed-element role.

**External source leads**
- BioPartner 5 Popma ter Steege: https://www.popma-tersteege.nl/project/biopartner-5/

**Existing topology component hints**
- Abbruchschutt / Mauerwerkspuin in grüner Fassade
- Wiederverwendete Innenwände und Trennwände
- Wiederverwendete Pflaster-, Naturstein- und Bodenmaterialien
- Wiederverwendete Sanitärobjekte
- Wiederverwendete Stahlträger, Stützen und Rahmen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="11-bluecity-offices-rotterdam"></a>
## 11. BlueCity Offices Rotterdam

### MAPPING_ONLY — do not extract
- Project ID: `p_bluecity_offices_rotterdam`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The office conversion uses reclaimed components to invent an interior language for a former leisure complex turned circular-business hub. Red-cedar window frames become partitions and internal facades, concrete blocks define boundaries, and reused steel enters the fit-out. The design is neither nostalgic nor polished; it works through reorientation, repetition and visible provenance. Spatially, the components organise offices while maintaining a sense of openness, making material flow part of the workplace identity.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** harvest-map / material-flow methodology; reused window frames and steel were not decoration but the main design inputs, requiring adaptive detailing and flexible construction.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** office partitions, transparency, rhythm, and interior atmosphere are shaped by reused window frames; reused steel contributes to the fit-out structure and detail language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- BlueCity Superuse Studios: https://www.superuse-studios.com/projectplus/bluecity-offices/
- Circle Economy BlueCity: https://circle-economy.com/knowledge-hub/article/30011

**Existing topology component hints**
- Betonblöcke als Trennwände
- Mögliche wiederverwendete Balustraden
- Red-Cedar-Fensterrahmen als Trennwände / innere Fassade
- Wiederverwendeter Stahl im Büroausbau

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="12-boulder-fire-station-3-city-of-boulder-fire-rescue-station-3"></a>
## 12. Boulder Fire Station 3 / City of Boulder Fire Rescue Station #3

### MAPPING_ONLY — do not extract
- Project ID: `p_boulder_fire_station_3`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Boulder Fire Station 3 turns salvaged hospital steel into a civic structural order. The design depends on cataloguing wide-flange members, verifying them, and recomposing them with new timber elements into a disciplined public-safety building. Rather than producing a scrap aesthetic, the architecture makes reuse look dependable: exposed beams and columns frame generous operational spaces, while the hybrid structure communicates durability, municipal responsibility and technical confidence.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** structural equivalence design: salvaged steel from deconstruction is catalogued and recomposed into an orderly exposed frame, requiring design adjustments to available member depths.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** visible steel frame and interior beam order become an architectural statement of circular construction without looking ad hoc.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- AISC Boulder Fire Station: https://www.aisc.org/modern-steel/news/inside-davis-partnerships-reuse-of-steel-in-a-new-fire-station/
- Architectural Record Boulder: https://www.architecturalrecord.com/articles/17599-davis-partnership-uses-salvaged-steel-on-a-new-colorado-firehouse

**Existing topology component hints**
- 89 salvaged wide-flange steel members
- Boulder Community Hospital structural steel stockpile
- Neue Glulam Columns im Hybridtragwerk
- PV-Dach / große Dachfläche

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="13-brent-cross-town-primary-substation"></a>
## 13. Brent Cross Town Primary Substation

### MAPPING_ONLY — do not extract
- Project ID: `p_brent_cross_town_primary_substation_london`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The substation separates architectural screen and structural reuse in a precise way. Reclaimed tubular steel is used where its section, length and geometry can work as columns and bracing, while new elements handle conditions that require tighter control. The design quality lies in selective application rather than total reuse. Behind the public artwork and infrastructural wrapper, the project demonstrates how reused industrial steel can quietly determine support, span and connection strategy.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** selective reclaimed-steel structural strategy: reclaimed tubulars used where geometry/load made them appropriate, while new steel was reserved where reused sections would have produced poor connections.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** primary structure of the substation incorporates reused tubular columns; architectural wrapper remains separate, so the reuse output is structural rather than façade-led.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- ASBP Brent Cross Substation: https://asbp.org.uk/case-studies/brent-cross-town-primary-substation
- Arup Brent Cross Substation: https://www.arup.com/projects/brent-cross-town-substation/

**Existing topology component hints**
- Neue façade support members
- Ovaler Substation-Screen
- Reclaimed tubular bracing members
- Reclaimed tubular steel columns

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="14-brighton-waste-house-brighton-wild-house"></a>
## 14. Brighton Waste House / Brighton Wild House

### MAPPING_ONLY — do not extract
- Project ID: `p_brighton_waste_house_brighton`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Waste House is a full-scale teaching experiment where discarded and reclaimed products become architectural lessons. Carpet tiles, denim, vinyl banners, waste timber, concrete blocks and unusual infill materials are built into walls and envelopes so that construction itself becomes a display system. The design does not hide the research character; it makes the building a readable catalogue of assemblies, testing how low-value waste can create enclosure, texture, insulation and public curiosity.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** pedagogical test-house methodology: design and construction test waste-derived components as building elements at full scale.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** walls, insulation, envelope and interior components display waste/reclaimed materials as an experimental architectural language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Brighton Waste House: https://arts.brighton.ac.uk/projects/wastehouse
- ArchDaily Brighton Waste House: https://www.archdaily.com/458245/brighton-waste-house-bb-architects

**Existing topology component hints**
- Denim jeans als Dämm-/Hohlraumfüllung
- Gebrauchte Teppichfliesen als Fassaden-/Außenschicht
- Holz und Sperrholz aus Reststücken
- Vinylbanner als Dampfbremse
- Wiederverwendete Betonblöcke
- Zahnbürsten und Medienabfall als Hohlraumfüllung

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="15-broethen-twin-house-hoyerswerda"></a>
## 15. Broethen Twin-House, Hoyerswerda

### MAPPING_ONLY — do not extract
- Project ID: `p_broethen_twin_house_hoyerswerda`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Broethen twin-house reuses P2 wall and floor slabs as the basis for a new residential composition. Its design logic is constrained by the grammar of the donor system: panel size, lifting sequence, joint lines and allowable cuts shape the layout. The architecture is quiet but conceptually clear, showing how industrialised concrete housing can be re-authored as a smaller domestic type. Reuse is visible through module, mass and structural rhythm.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Material-inventory-led design; Specification/dimensional adaptation to reclaimed components; Local reuse design strategy

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Modular composition from reclaimed concrete/components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- P2-Deckenplatten
- P2-Wandplatten

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="16-careno-be-circular-brussels-ceramic-floor-tile-reuse-research-rotor-rotordc-be-circular-grant-2016"></a>
## 16. Careno - Be.Circular Brussels — Ceramic Floor Tile Reuse Research (Rotor + RotorDC, Be.Circular grant 2016)

### MAPPING_ONLY — do not extract
- Project ID: `p_careno_becircular`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Careno is not a building design but a design-enabling material project. Its architectural relevance lies in making historic ceramic floor tiles usable again: cleaning, sorting, standardising and presenting them as specifiable stock. The design decisions happen at the scale of detail, tolerance, surface and procurement rather than plan or section. It should feed future architectural outputs only when linked to a built installation where reclaimed tiles actively shape floor pattern, room character or finish strategy.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** component-system methodology, not a single building: develop cleaning/treatment/commercialisation methods for reclaimed ceramic floor tiles to make reuse specifiable.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** no direct architectural output node unless linked to a built tile-installation project; output is a reclaimed-tile supply/detail system.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** No/ResearchOnly
- **Important caution:** Do not create ArchitecturalOutput node for a building unless the Neo4j project already contains a built application.

**External source leads**
- Rotor Careno Be.Circular: https://rotordb.org/en/projects/careno-becircular

**Existing topology component hints**
- Careno — Historic ceramic flooring tiles, circa 1900-1960 (raw stock, mortar+grout residues)
- Careno — Re-Tile machine-cleaned reclaimed floor tiles (mortar removed)
- Careno — RotorDC reclaimed ceramic tile stock (online + physical shop)

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="17-cascadeup-london-secondary-timber-glulam-demonstrator"></a>
## 17. CascadeUp / London secondary-timber glulam demonstrator

### MAPPING_ONLY — do not extract
- Project ID: `p_cascadeup_london_secondary_timber_glulam_demonstrator`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
CascadeUp investigates whether demolition timber can become a credible mass-timber architecture. The demonstrator’s design is driven by the limits of reclaimed feedstock: short lengths, variable quality and the need to laminate or panelise timber into new structural formats. The architectural output is small, but its significance is methodological. It shows how reclaimed timber can move beyond rustic reuse into engineered frames and panels with a contemporary tectonic expression.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** research-to-demonstrator methodology converting demolition timber into CLT/glulam-scale secondary timber modules; design constrained by local feedstock within a limited radius.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** small modular timber structure expresses secondary-timber lamellae and demonstrates mass-timber form/assembly from reclaimed feedstock.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- CascadeUp UCL paper: https://discovery.ucl.ac.uk/10210949/1/Rose%20et%20al_WCTE%202025_full%20paper.pdf
- Amazing Architecture CascadeUp: https://www.amazingarchitecture.com/news/from-waste-wood-to-mass-timber-cascadeup-pilot-to-premiere-at-london-design-festival

**Existing topology component hints**
- CLST-Bodenpaneele
- CLST-Wandpaneele
- glulamST-Tragwerksrahmen / Balken und Stuetzen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="18-charles-malis-antenne-administrative-de-molenbeek-saint-jean"></a>
## 18. Charles Malis / Antenne administrative de Molenbeek-Saint-Jean

### MAPPING_ONLY — do not extract
- Project ID: `p_charles_malis_molenbeek`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Charles Malis is primarily an adaptive reuse of an industrial complex into a municipal administrative facility. The retained ornamental facade and concrete structure carry the main design weight, preserving the factory’s urban presence while accommodating new public functions. Reused lights and Bruseleye floor elements appear as component-level interventions, but the architectural narrative should remain cautious: the strongest design claim is transformation of existing fabric, not a fully reclaimed-material-driven composition.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** primary verified design logic is adaptive reuse of an industrial shell/site; reclaimed-component evidence exists in topology but public project pages do not clearly show reclaimed materials driving form or space.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** do not create a strong reclaimed-material ArchitecturalOutput node unless internal Neo4j evidence confirms that reused lights/flooring materially shaped design expression; otherwise treat as retained-building adaptive reuse only.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Low/DoNotExtract
- **Important caution:** Important correction: keep project only if graph category allows retained existing components/adaptive reuse; for reclaimed-material-focused nodes, mark low confidence/no extraction.

**External source leads**
- MAMOUT Charles Malis: https://www.mamout.be/projects/charles-malis
- ArchDaily Charles Malis: https://www.archdaily.com/804017/charles-malis-mamout-plus-willocx-plus-ld2

**Existing topology component hints**
- Erhaltene ornamentale Fassade
- Erhaltenes Betontragwerk
- ROTOR-Leuchten
- Wiederverwendete Bruseleye-Bodenpflaster / Bodenfliesen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="19-chiro-d-itterbeek-sanitary-block-dilbeek"></a>
## 19. Chiro d’Itterbeek / Sanitary block, Dilbeek

### MAPPING_ONLY — do not extract
- Project ID: `p_chiro_d_itterbeek_dilbeek`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The sanitary block is small, but the design work is unusually precise. Reclaimed tiles, sanitary fixtures, mirrors, lighting, doors, windows, bricks and steel profiles are not scattered tokens; they define the wet-room atmosphere, facade texture and everyday usability of the building. The project shows how a modest programme can be designed almost as a fitted assemblage, where each recovered component is selected for dimension, durability, hygiene, finish and visual compatibility.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** RotorDC material-supply method: sanitary-block interior and facade were designed around available reused tiles, sanitary fittings, lighting, mirrors, bricks and joinery.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** facade and wet-room interior are visibly shaped by reclaimed bricks/joinery/tiles and second-hand sanitary equipment; output is a direct reclaimed-component fit-out language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Rotor Chiro Itterbeek: https://rotordb.org/en/projects/sanitary-block-itterbeek-chiro
- Construction21 Chiro: https://www.construction21.org/france/case-studies/h/sanitary-pavilion-of-the-chiro-of-itterbeek-en.html
- FCRBE project sheets: https://vb.nweurope.eu/media/21046/dt4_2_2_project-sheets_041023_lr.pdf

**Existing topology component hints**
- Außentüren
- Bodenfliesen
- Dachziegel (Chiro)
- Fassadenziegel (Chiro)
- Holzfenster
- Leuchten
- Sanitärobjekte (Chiro)
- Stahl-U-Profile als Außenstürze
- Surplus-Betonblöcke
- Surplus-Dämmung Boden/Wand
- … +3 more

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="20-christus-pavillon-christ-pavilion-volkenroda"></a>
## 20. Christus-Pavillon / Christ Pavilion Volkenroda

### MAPPING_ONLY — do not extract
- Project ID: `p_christ_pavilion_volkenroda`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Christus-Pavillon is architectural reuse at the scale of an entire pavilion. Rather than harvesting isolated components, the project relocates and re-anchors a symbolic steel, glass, marble and concrete ensemble in a new religious setting. Design decisions concern dismantling, transport, reassembly and contextual transformation. The architectural quality comes from continuity and displacement: Expo-era elements become a monastery-related spatial sequence, carrying their original formal language into a different spiritual and landscape context.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reversible/disassembly-aware design with reclaimed components; Specification/dimensional adaptation to reclaimed components; Tracked-component design coordination

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Reclaimed-component facade rhythm or patchwork facade; Collage interior / reused partition and fit-out language; Relocated/reassembled building expression; Facade expression shaped by reclaimed components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Dachtragwerk Christusraum
- Gesamtes transloziertes Pavillonensemble
- Kreuzgang / Stahl-Glas-Fassade und Vitrinen
- Marmor-Glas-Wand Christusraum
- Neun kreuzfoermige Stahlstuetzen
- Sichtbetonteile des translozierten Ensembles

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="21-circl-abn-amro-urban-mining-context"></a>
## 21. Circl / ABN AMRO urban mining context

### MAPPING_ONLY — do not extract
- Project ID: `p_circl_abn_amro`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Circl treats the pavilion as a material bank and public demonstration of circular building. Reclaimed timber, reused interior elements and demountable construction are organised into an architecture that must function as restaurant, meeting space and statement object. The design avoids the look of temporary waste reuse by giving recovered components careful detailing and spatial generosity. Its architectural output is a polished but readable kit of materials intended to remain recoverable after use.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular-pavilion methodology: reuse considered from the start, with demountable timber, reused window-frame flooring, reused/recycled floor systems, and component value after first life.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** building operates as a demountable kit and circular interior; floors, ceiling insulation, timber structure and pavilion programme communicate material cycles.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Circl Architecten Cie: https://www.cie.nl/circl?lang=en
- Divisare Circl: https://divisare.com/projects/374731-de-architekten-cie-ossip-van-duivenbode-circl
- ULI Circl: https://europe.uli.org/2020-finalists/circl-a-building-that-became-a-movement/

**Existing topology component hints**
- Circl — 16,000 old jeans incorporated as ceiling insulation (Denimtex)
- Circl — 500 roof solar panels, ~7 years old, lower output than new panels (Exasun)
- Circl — C2C-certified Tarkett iQ One flooring
- Circl — Conference-room window frames, carefully removed from demolished office buildings
- Circl — Floor structure (less suitable for reuse than anticipated per Icon dismantling progress)
- Circl — Fully demountable locally-sourced larch timber support structure (installed 2017; dismantled 2024-2025)
- Circl — Leased Fagerhult DC lighting (product-service system)
- Circl — Leased lifts (product-service system, supplier ownership, 10-year return)
- Circl — Rejected wooden window frames cut into floorboards
- Circl — Remountable façade with C2C-certified plant modules (De Groot & Visser + Donkergroen)
- … +5 more

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="23-circular-centre-netherlands-prinsenhof-a-reuse-pilot"></a>
## 23. Circular Centre Netherlands / Prinsenhof A reuse pilot

### MAPPING_ONLY — do not extract
- Project ID: `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Prinsenhof A pilot should be read as a circular office intervention where existing building components become test material for future practice. The design value lies in how reclaimed parts are documented, selected and reinserted into a working environment rather than merely displayed. It is important to distinguish architectural effects from process evidence: only when reused elements influence partitions, finishes, furniture, facade or spatial organisation should the two new nodes be created.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Material-inventory-led design; Reuse-assessment-led design; Urban-mining-led design; Specification/dimensional adaptation to reclaimed components

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component facade rhythm or patchwork facade; Facade expression shaped by reclaimed components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Betonbruestungen / parapets
- Hohlkoerperdecken / kanaalplaatvloeren
- Prefab-Fassadenelemente

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="24-circular-pavilion-paris"></a>
## 24. Circular Pavilion Paris

### MAPPING_ONLY — do not extract
- Project ID: `p_circular_pavilion_paris`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Circular Pavilion uses recovered doors, timber, lighting and urban materials to construct a public architectural manifesto. Its design is legible because the facade and enclosure are composed from repeated reclaimed elements rather than disguised behind a neutral finish. The pavilion works through accumulation, rhythm and didactic visibility: citizens can read the city’s discarded components as architecture. Its temporary scale allows reuse to become both construction method and public communication.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular-economy demonstration: design process converts multiple waste/reclaimed streams into a public pavilion, making circularity the concept rather than a hidden specification.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** patchwork envelope and temporary pavilion expression communicate the idea that one site’s waste becomes another site’s resource.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- ArchDaily Circular Pavilion: https://www.archdaily.com/778972/the-circular-pavilion-encore-heureux-architects

**Existing topology component hints**
- 180 Holztueren als Fassade
- Ehemalige Ausstellungspaneele
- Holzstruktur aus Baustellenresten
- Mineral-/Steinwolle als Innendaemmung
- Terrassen-Caillebotis aus Paris-Plage
- Vier grosse Leuchten aus oeffentlichem Bestand

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="25-crclr-house-impact-hub-berlin"></a>
## 25. CRCLR House / Impact Hub Berlin

### MAPPING_ONLY — do not extract
- Project ID: `p_crclr_house_impact_hub_berlin`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
CRCLR House transforms an existing industrial site into a circular-workplace and community setting. The design combines retained fabric with reused fit-out components, creating a rough but purposeful environment for collaboration. Reuse is strongest where partitions, interior surfaces, fixtures and retained structures shape the everyday spatial experience. The architecture does not seek a finished corporate image; it uses traces, adaptable rooms and visible resourcefulness to align the building’s atmosphere with its circular-economy programme.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** warehouse transformation and circular fit-out methodology; reused/new sustainable materials are accepted as found or upcycled to fit a coherent workplace identity.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** co-working interiors expose circular material choices while avoiding a low-grade second-hand aesthetic; partitions, finishes and furniture form the output.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- CRCLR circular material systems: https://circularmaterialsystems.com/en/case/impact-hub-berlin-crclr-house/
- LXSY Impact Hub Berlin: https://lxsy.de/en/projects/impact-hub-berlin-at-crclr-house
- Impact Hub UBM: https://www.ubm-development.com/magazin/en/impact-hub-berlin/

**Existing topology component hints**
- Holzgalerie / Innenausbau aus heterogenen Restmaterialien
- Stahlfachwerktraeger fuer Gewaechshausdach / unsicherer Umfang
- Stahlpfetten / I-Traeger aus Hallendach als Treppenwangen
- Vorhangfassadenelemente, Blech und Glas
- Wiederverwendete Holz-Alu-Fenster / Außenfenster
- Wiederverwendete Sanitärobjekte / Duschtassen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="27-elementa-walkeweg-basel-wohnbau-mit-wiederverwendung-von-bestandskomponenten-kanton-basel-stadt-wettbewerb"></a>
## 27. ELEMENTA Walkeweg Basel — Wohnbau mit Wiederverwendung von Bestandskomponenten (Kanton Basel-Stadt Wettbewerb)

### MAPPING_ONLY — do not extract
- Project ID: `p_elementa_walkeweg`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
ELEMENTA is important as a housing proposal organised around the reuse of substantial existing components. The architectural interest lies in how salvaged concrete and other building elements can discipline a new residential scheme: bay spacing, stair logic, facade rhythm and construction sequence all have to negotiate availability. Because delivery status still needs verification, the description should remain design-focused. It is a project about making component reuse compatible with ordinary collective housing, not about a one-off pavilion gesture.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Component-catalogue-led design; Material-inventory-led design; Pre-deconstruction-audit-led design; Donor-building / deconstruction-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Modular composition from reclaimed concrete/components; Reclaimed timber atmosphere or tectonic detail; Collage interior / reused partition and fit-out language

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- ELEMENTA — Brettstapeldecken (new renewable wood)
- ELEMENTA — Lehmbauplatten + Lehmputz (clay boards + plaster)
- ELEMENTA — RC rib-panel load-bearing exterior wall (Baufeld D from Lysbüchel garage)
- ELEMENTA — Reused RC column-beam structure (Baufeld C from Lysbüchel garage)

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="28-elys-kultur-und-gewerbehaus-basel"></a>
## 28. ELYS Kultur- und Gewerbehaus Basel

### MAPPING_ONLY — do not extract
- Project ID: `p_elys_kultur_gewerbehaus_basel`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
ELYS converts former industrial stock into a cultural and commercial environment where reuse is inseparable from atmosphere. Existing structures, reclaimed fit-out pieces and rough material traces produce spaces that feel provisional yet intensely inhabited. The design works by accepting the building’s accumulated layers rather than erasing them. Architectural quality comes from generous industrial rooms, adapted circulation, improvised details and visible material histories that support a mixed cultural programme.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Material-inventory-led design; Material-scouting-led design; Specification/dimensional adaptation to reclaimed components; Adaptive repurposing / function change of reclaimed components

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component facade rhythm or patchwork facade; Reclaimed timber atmosphere or tectonic detail; Facade expression shaped by reclaimed components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- 200 Fenster aus Lagerrestbeständen
- Altholz aus Rückbauten / Dachstühlen
- Aluminium-Trapezblech als Fassadenbekleidung
- Erhaltene Betonhallen / Tragstruktur
- Gitterroste / Brüstungsgitter und Garagentor
- Reuse-Fassade als Holzrahmen-Bauteilsystem
- Steinwolledämmung aus Restposten / Abfallprodukten

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="29-eth-circular-construction-student-reuse-project"></a>
## 29. ETH Circular Construction student reuse project

### MAPPING_ONLY — do not extract
- Project ID: `p_eth_circular_construction_student_reuse_project`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The ETH student project is a compact experiment in designing from an available dismantled stock. Materials from the Huber Pavilions are measured, sorted and reconfigured into a new pavilion, so design authorship shifts from free form-making to selection, negotiation and assembly. Its architectural output is didactic: students and visitors encounter a structure whose proportions, joints and surfaces reveal the limits of the recovered elements and the decisions needed to make them work again.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `DesignMethodology` node proposed from current topology evidence.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `ArchitecturalOutput` node proposed from current topology evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="30-eth-circular-construction-student-reuse-demonstrator-news"></a>
## 30. ETH Circular Construction — student reuse demonstrator/news

### MAPPING_ONLY — do not extract
- Project ID: `p_eth_circular_construction_student_reuse`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
This entry should be treated as the same design story as the ETH Circular Construction pavilion rather than as a second independent case. The relevant architectural content is the reuse of dismantled pavilion materials through student-led design, where available pieces govern form, module and construction sequence. Keep the narrative only as supporting context for the canonical ETH project. The design value is pedagogical: learning reuse by making constraints visible in the built object.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `DesignMethodology` node proposed from current topology evidence.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `ArchitecturalOutput` node proposed from current topology evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="31-europa-building-brussels-r-sidence-palace-europa"></a>
## 31. Europa Building Brussels / Résidence Palace – Europa

### MAPPING_ONLY — do not extract
- Project ID: `p_europa_building_brussels`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Europa Building is not a simple component-reuse project; its architectural power comes from setting a new institutional lantern inside a retained historic block. Reused or repurposed window elements contribute to the layered facade and interior identity, but the larger design decision is urban and symbolic: preserve the Residence Palace fabric while inserting a luminous new council chamber. Reuse here operates through memory, facade layering and the tension between diplomatic monumentality and recovered domestic fragments.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** symbolic reclaimed-component façade strategy: thousands of recovered oak/chestnut window frames from across Europe are recomposed as a brise-soleil/patchwork skin.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** the external façade becomes a political and architectural image of 'unity in diversity' through a patchwork of reused window frames around the glass atrium/lantern.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Europa Opalis: https://opalis.eu/nl/projecten/gevel-europagebouw
- Consilium Europa: https://www.consilium.europa.eu/lv/europa-the-beating-heart-of-europe/
- ArchDigest Europa: https://www.architecturaldigest.com/story/european-union-set-bold-new-brussels-headquarters

**Existing topology component hints**
- 3.750 restaurierte Holzfensterrahmen als Patchwork-Fassade
- Erhaltene Teile des Residence Palace Block A

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="32-fcrbe-facilitating-the-circulation-of-reclaimed-building-elements"></a>
## 32. FCRBE — Facilitating the Circulation of Reclaimed Building Elements

### MAPPING_ONLY — do not extract
- Project ID: `p_fcrbe`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
FCRBE is a programme, not an architectural object, so it should not produce a project-specific architectural output. Its design relevance is methodological: it builds the conditions under which architects can design with reclaimed components by developing inventories, guidance, networks and market confidence. Treat it as infrastructure for design practice. If node extraction occurs, it should describe the methodology of enabling reuse, not a facade, structure or spatial quality of a single building.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** programme/platform, not a building: method is to document, test and circulate reclaimed building elements via case sheets and market guidance.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** no project-specific ArchitecturalOutput node; use only as source/context for other built projects.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** No/ResearchOnly
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- FCRBE project sheets: https://vb.nweurope.eu/media/21046/dt4_2_2_project-sheets_041023_lr.pdf

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="33-ferme-du-rail-paris"></a>
## 33. Ferme du Rail Paris

### MAPPING_ONLY — do not extract
- Project ID: `p_ferme_du_rail_paris`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Ferme du Rail combines social, agricultural and architectural programmes with a material strategy based on reuse and low-impact construction. Reclaimed components contribute to a deliberately modest, workshop-like atmosphere suited to urban farming, housing and public activity. The design decisions emphasise repairability, visible assemblies and a productive landscape rather than formal smoothness. Its architectural quality lies in making social infrastructure feel materially grounded, with reused elements reinforcing the project’s ethic of care and resourcefulness.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** low-tech modular, dry-assembly methodology using reused, recycled and bio-based materials; construction site also operates as a learning/social-integration process.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** timber/straw/reused tile/metal/stone material palette creates an agricultural-urban atmosphere and detail language of modular disassemblable construction.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Circular Materials Ferme du Rail: https://circularmaterialsystems.com/en/case/05_ferme-du-rail/
- Mies Awards Ferme du Rail: https://eumiesawards.com/heritageobject/the-railway-farm/

**Existing topology component hints**
- Bitumen- und Betonblöcke als Außenwege
- Fliesen / Fayence als Badwandbelag
- Granitbordsteine als Stützmauer
- Holzfensterrahmen als Akroterie, Pflanztröge und Geländer
- Holzfensterrahmen als Holzpflaster / Parkett bois de bout
- Stein- und Bürofußbodenplatten als Beläge/Füllplatten
- Textile / rezyklierte Fasern als Sonnenschutzstores
- Wiederverwendetes Holz für feste Schränke

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="34-gjg-house-gentbrugge-ghent"></a>
## 34. gjG House, Gentbrugge / Ghent

### MAPPING_ONLY — do not extract
- Project ID: `p_gjg_house_gentbrugge`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
gjG House is a domestic reuse project where the architectural interest is in calibration rather than abundance. Reused elements are selected and detailed so they become part of a composed residential environment, not simply evidence of thrift. The design negotiates between everyday comfort and the irregularities of recovered components. Its output should be described through the specific building parts documented in the graph: where reclaimed pieces affect facade, interior atmosphere, detail or structure, they become architectural rather than merely material data.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** brick-wall research methodology: reused bricks and shell autonomy are used to question glued brick veneer and create a reusable/structural brick architecture.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** curved brick shell and expressive masonry surface become the output of reclaimed-brick experimentation.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- ArchDaily gjG House: https://www.archdaily.com/951845/gjg-house-blaf-architecten
- Designboom gjG House: https://www.designboom.com/architecture/blaf-architects-reused-bricks-gjg-house-belgium-10-30-2020/

**Existing topology component hints**
- Gekrümmte strukturell autonome Außenmauer / Ziegelschale
- Stahl-/Holz-Infill-Struktur

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="36-grande-halle-de-colombelles-le-wip"></a>
## 36. Grande Halle de Colombelles / Le WIP

### MAPPING_ONLY — do not extract
- Project ID: `p_grande_halle_de_colombelles`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Le WIP transforms an industrial hall into a flexible civic and cultural workplace by preserving the spatial generosity of the existing structure while inserting reused and adaptable elements. The design does not overfinish the hall; it uses robust, legible interventions to support events, workspaces and public gathering. Reuse contributes to an atmosphere of productive incompleteness, where large-span industrial space, lightweight inserts and visible assemblies make the building feel open to change.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** adaptive reuse of industrial hall with selective material reuse; reclaimed components support a public cultural/workspace conversion.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** large industrial volume remains the main spatial output; reuse supports rough, flexible, workshop-like atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Grande Halle WIP Encore Heureux: https://encoreheureux.org/projets/grande-halle-colombelles/

**Existing topology component hints**
- Erhaltene Bestand-Betonstruktur der Halle
- Holzpfetten / Holzstücke als Balkon-, Treppen- oder Geländerbauteile
- Metallträger / poutres métalliques, unklarer Wiedereinbau
- Wiederverwendete Außenschreinerei / Fenster
- Wiederverwendete Fliesen / Fayence
- Wiederverwendete Mineralwolle-Dämmung
- Wiederverwendete Radiatoren
- Wiederverwendete Sanitärobjekte
- Wiederverwendete Türen und Brandschutztüren

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="37-grubenstrasse-29-werkhof-29-z-rich"></a>
## 37. Grubenstrasse 29 / Werkhof 29, Zürich

### MAPPING_ONLY — do not extract
- Project ID: `p_grubenstrasse_29_werkhof_29_zuerich`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Werkhof 29 is a reuse-driven conversion where the design value lies in the relationship between retained industrial character and newly inserted recovered components. The project should be read through its handling of workshops, circulation, facade pieces and interior fit-out rather than through a single spectacular element. Reused materials help produce a pragmatic urban atmosphere: robust, flexible and slightly rough. The architecture works by letting construction history and new programme remain simultaneously visible.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** selective reuse where components lower emissions/economic impact, combined with natural materials; design extends old factory while preserving mixed work uses.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** new upper floors and restored lower levels produce a layered old/new work complex; reclaimed components appear as part of a broader circular tectonic palette.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Grubenstrasse Zirkular: https://zirkular.net/en/project/grubenstrasse-29/
- In Situ Werkhof 29: https://insitu.ch/projekte/351-aufstockung-grubenstrasse

**Existing topology component hints**
- Blaue Stahlblechfassade
- Erhalt und Ertüchtigung des Bestandsgebäudes
- Stahlbauteile für Laubengänge, Treppentürme und Gitterroste
- Wiederverwendete Außentreppe
- Wiederverwendete Dachbleche
- Wiederverwendete Dämmplatten
- Wiederverwendete Fenster und Türen
- Wiederverwendete Geländer
- Wiederverwendete Heizkörper und Sanitärapparate

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="38-hastings-pier-visitor-centre-reclaimed-timber-cladding"></a>
## 38. Hastings Pier Visitor Centre / reclaimed timber cladding

### MAPPING_ONLY — do not extract
- Project ID: `p_hastings_pier_visitor_centre`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The visitor centre gives fire-damaged pier timber a new architectural role. Reclaimed hardwood is cut, sorted and used as cladding, so the building’s surface carries the memory of the destroyed pier while protecting a new public facility. The design is simple but emotionally specific: material provenance becomes facade, atmosphere and civic narrative. Its architectural quality depends on weathered texture, horizontal boarding and the transformation of loss into a calm seaside building.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** on-site timber recovery strategy: damaged pier decking becomes the cladding/skin of the visitor centre.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** weathered reclaimed pier timber defines the visitor centre envelope, atmosphere and memory of the rebuilt pier.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Hastings Pier dRMM: https://drmmstudio.com/project/hastings-pier/

**Existing topology component hints**
- Gespaltene längere Hartholzstücke als Bekleidung von Toiletten / Outbuildings
- Neues CLT-Tragwerk des Visitor Centre
- Restaurierte Pier-Unterstruktur und viktorianischer Pavillon
- Wiederverwendete tropische Hartholz-Deckbohlen als Fassadenbekleidung

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="39-haus-hos-mehrfamilienhaus-m-hlhausen"></a>
## 39. Haus HOS / Mehrfamilienhaus Mühlhausen

### MAPPING_ONLY — do not extract
- Project ID: `p_haus_hos_mehrfamilienhaus_muehlhausen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Haus HOS uses reclaimed concrete elements within a new multi-family housing project, linking East German prefabrication history to contemporary residential needs. The design task is to make salvaged structural parts compatible with new comfort, regulations and domestic layouts. Architectural interest comes from the tension between standardised heavy components and new housing individuality. Reuse is expressed through module, concrete mass and adapted construction logic rather than a deliberately picturesque material collage.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Form follows availability; Component-catalogue-led design; Reuse-assessment-led design; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Modular composition from reclaimed concrete/components; Reclaimed circulation/detail element made architecturally legible

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Wiederverwendete Stahlbeton-Deckenelemente
- Wiederverwendete Stahlbeton-Treppen / Podeste
- Wiederverwendete Stahlbeton-Wandelemente

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="40-holbein-gardens-london"></a>
## 40. Holbein Gardens, London

### MAPPING_ONLY — do not extract
- Project ID: `p_holbein_gardens_london`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Holbein Gardens combines deep retrofit with selective structural reuse, making the existing building fabric an active design resource. Rather than replacing the frame wholesale, the project works with what can remain and what can be inserted, producing a layered office architecture. Reclaimed or retained elements shape the structural strategy, facade response and interior character. The design quality lies in showing commercial redevelopment as careful editing: conservation, new performance and reuse are coordinated into a polished urban workplace.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** direct structural-steel reuse in office redevelopment; reclaimed members are integrated with retained fabric and engineered timber extensions.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** steel/timber hybrid frame, visible structural order and retained building fabric create a low-carbon extension language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Holbein Gardens TERC: https://terc.org.uk/54-2/
- IStructE Holbein Gardens: https://www.istructe.org/structural-awards/projects/2023/holbein-gardens/
- GlobalABC Holbein: https://globalabc.org/sustainable-materials-hub/resources/steel-reuse-incorporating-reclaimed-steel-holbein-gardens

**Existing topology component hints**
- Erhaltener Betonrahmen und Bestandshülle
- Neue CLT-Decken der Erweiterung
- Reclaimed stone / brickwork, Menge und Rolle unklar
- Wiederverwendete Stahlträger und Stahlstützen für die Aufstockung

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="41-house-of-fraser-318-oxford-street-tbc-london-steel-reuse-chain"></a>
## 41. House of Fraser / 318 Oxford Street → TBC.London steel reuse chain

### MAPPING_ONLY — do not extract
- Project ID: `p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
This entry is best understood as a design and logistics chain linking a donor department-store structure to a new commercial project. The architectural decision is made before the recipient building is complete: steel members are identified, tested and assigned so they can influence the next structural design. Its design significance lies in timing, dimensional matching and procurement. The output is not only a building part, but a model for making urban demolition stock shape future office construction.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** donor-to-recipient steel reuse chain: structural steel from demolition is processed and redirected into TBC.London, making reuse a procurement/design dependency.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architectural output belongs to recipient project where reused steel is installed; donor building itself should not receive output node unless graph represents chain explicitly.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- House of Fraser ASBP: https://asbp.org.uk/case-studies/house-of-fraser-to-tbc-london-steel-reuse

**Existing topology component hints**
- 1930er Stahlträger vom House of Fraser in TBC.London
- Erhaltener 1990er Betonrahmen TBC
- Handrails, fixtures, bricks und demolition materials mit unklarer fester Reuse-Funktion
- Refabrizierte Stahlstützen aus unteren Geschossen für neue obere Ebenen 318 Oxford Street
- Repurposed Cleveland steel für obere Etage TBC

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="42-h-rm-l-nranta-a-kruunu-recreate-mini-pilot-tampere"></a>
## 42. Härmälänranta / A-Kruunu ReCreate mini-pilot Tampere

### MAPPING_ONLY — do not extract
- Project ID: `p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Tampere mini-pilot tests how precast concrete components from existing buildings can become a credible basis for new construction. Design decisions are governed by the size, condition and connection possibilities of recovered elements. The architectural output should be described modestly: a demonstrator of module transfer, not a fully mature housing language unless the graph proves it. Its value is in showing how concrete panel reuse can move from research question to buildable prototype.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Component-catalogue-led design; Pre-deconstruction-audit-led design; Reuse-assessment-led design; Specification/dimensional adaptation to reclaimed components; Material-matching-led design coordination

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component architectural expression unclear from topology evidence

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Luftschutzraum-Deckenbereich als Einbauort
- Wiederverwendete Hohlkörperdecken / hollow-core slabs

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="43-impact-hub-berlin-crclr-fit-out"></a>
## 43. Impact Hub Berlin / CRCLR Fit-out

### MAPPING_ONLY — do not extract
- Project ID: `p_impact_hub_berlin_crclr_fitout`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Impact Hub fit-out translates CRCLR’s circular agenda into everyday workspace design. Reclaimed partitions, surfaces, fixtures and furniture help produce an interior that is flexible, informal and materially explicit. The design choices favour adaptability and visible assembly over a seamless office finish. Reuse becomes spatial communication: tenants encounter the building’s values through desks, meeting rooms, partitions and rough surfaces, not through abstract sustainability signage.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular interior method inside CRCLR-House: use-as-found plus selective upcycling, with damaged/uneven reclaimed materials adapted to the design concept.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** interior atmosphere is deliberately shaped by reclaimed and renewable materials, proving second-hand materials can support a high-quality contemporary workplace.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- LXSY Impact Hub Berlin: https://lxsy.de/en/projects/impact-hub-berlin-at-crclr-house
- Impact Hub UBM: https://www.ubm-development.com/magazin/en/impact-hub-berlin/
- CRCLR circular material systems: https://circularmaterialsystems.com/en/case/impact-hub-berlin-crclr-house/

**Existing topology component hints**
- Holzgalerie / zweite Ebene, Wiederverwendung nicht belegt
- Holzlatten aus Tischlereiresten für Telefonboxen
- Recycelte Filzpaneele für Akustik in Telefonboxen
- Red MDF boards als feste Empfangs-/Treffpunktzone
- Schwarze MDF-Platten als Schranktüren und Wandpaneele
- Türen, Fenster und Sanitär im CRCLR-Gesamtprojekt mit unscharfer Fit-out-Zuordnung
- Wiederverwendete Ziegel im Empfang / Treffpunkt

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="44-institut-de-botanique-de-l-ulg-li-ge"></a>
## 44. Institut de Botanique de l’ULg, Liège

### MAPPING_ONLY — do not extract
- Project ID: `p_institut_de_botanique_ulg_liege`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Botanical Institute conversion is an adaptive reuse project where design begins with the retained institutional building and its existing spatial order. Reuse is strongest when existing fabric, structure and finishes are preserved or supplemented by recovered components to support new functions. The architectural quality comes from careful transformation rather than replacement: old academic rooms, circulation and material traces are reinterpreted for contemporary use, giving the project a layered civic and educational character.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Specification/dimensional adaptation to reclaimed components; Local sourcing-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component facade rhythm or patchwork facade; Reclaimed timber atmosphere or tectonic detail; Facade expression shaped by reclaimed components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Erhaltene Hauptstruktur des Bestandsgebäudes
- Wiederverwendete / rückgewonnene Holzfassade

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="45-interreg-nwe-fcrbe"></a>
## 45. Interreg NWE FCRBE

### MAPPING_ONLY — do not extract
- Project ID: `p_interreg_nwe_fcrbe`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
This is the programme framing of FCRBE, not a building to describe architecturally. Its relevance for design is that it formalises the ecosystem around reclaimed building elements: inventories, reclamation networks, specification guidance and market knowledge. It should help agents understand methodology at the scale of practice, policy and procurement. Do not extract a facade or spatial output from it; connect it only to design methods if existing graph structures already support programme-level methodology.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** programme/platform, not a building: method is to document, test and circulate reclaimed building elements via case sheets and market guidance.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** no project-specific ArchitecturalOutput node; use only as source/context for other built projects.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** No/ResearchOnly
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- FCRBE project sheets: https://vb.nweurope.eu/media/21046/dt4_2_2_project-sheets_041023_lr.pdf

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="46-jeugdkliniek-ithaka-emergis-kloetinge"></a>
## 46. Jeugdkliniek Ithaka / Emergis Kloetinge

### MAPPING_ONLY — do not extract
- Project ID: `p_jeugdkliniek_ithaka_emergis_kloetinge`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Ithaka’s design relevance lies in applying reuse to a sensitive care environment, where atmosphere, durability and comfort are as important as circular ambition. Reused components must be domesticated: they need to contribute to calm interiors, safe details and spatial clarity rather than appear as rough salvage. Architectural output should be tied only to documented components, but the broader design question is clear: how can recovered building elements support a therapeutic setting without compromising dignity or performance?
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** donor-building inventory as design brief: reusable materials from a former Rijkswaterstaat office were coded/database-managed and used as starting point for clinic design.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** exterior frames, internal doors, façade cladding, timber floors and paving shape the clinic’s architectural fabric and circular identity.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Ithaka Rothuizen: https://rothuizen-architecten.nl/project/circulair-gebouw-voor-kind-en-jeugdkliniek/
- Impuls Zeeland Ithaka: https://www.impulszeeland.nl/projecten/showcase-circulair-verbouwen-kinder-en-jeugdkliniek-emergis

**Existing topology component hints**
- Azobé-Hartholz-Shingles im dritten Leben
- Erhaltener Emergis-Bestand
- Teilweise wiederverwendete technische Bauteile
- Wiederverwendete Außenkozijnen / Fensterrahmen mit Sonnenschutz
- Wiederverwendete Holzfußböden und Straßenklinker
- Wiederverwendete Holzträger / houten balken
- Wiederverwendete Innentüren mit Hang- und Schließwerk

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="47-juch-areal-recyclingzentrum-z-rich"></a>
## 47. Juch-Areal Recyclingzentrum Zürich

### MAPPING_ONLY — do not extract
- Project ID: `p_juch_areal_recyclingzentrum_zuerich`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The recycling centre uses reclaimed components within an infrastructure building that already deals with material flows. This gives the architecture a direct conceptual fit: the place for sorting urban resources is itself designed from recovered parts. The design should be read through robust construction, accessible circulation, weathering surfaces and didactic visibility. Reuse strengthens the building’s public message, turning an operational facility into an architectural demonstration of the city’s circular material metabolism.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** re-assembling methodology: reused components from different urban mines are composed into modular, compact, demountable/adaptable recycling-centre architecture.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** recognisable reused wall elements and a vertical planted filter give the recycling centre a new identity; architecture makes component reuse visible and didactic.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Juch Studio Loko: https://www.studioloko.ch/en/projects/recyclingzentrum-juch-areal
- Juch Graber Pulver: https://www.graberpulver.ch/projekt/recyclingzentrum-juch-areal

**Existing topology component hints**
- Beton-Pilzstützen und Deckenelemente aus Schellinghalle Rümlang
- Gebrauchte Betonplatten aus dem Kerenzerbergtunnel
- Geplante 1:1 versetzte Stahlstruktur der Recyclinghalle Hagenholz

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="48-jugendtreff-ingersheim-clt-reuse-pilot-stuttgart-210-first-reallab-2024"></a>
## 48. Jugendtreff Ingersheim — CLT-Reuse Pilot (Stuttgart 210 first reallab, 2024)

### MAPPING_ONLY — do not extract
- Project ID: `p_jugendtreff_ingersheim`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Jugendtreff Ingersheim turns former Stuttgart 21 formwork into a youth-centre construction system. The design has to accept the geometry, marks and structural behaviour of CLT-like timber formwork elements, translating infrastructure-site waste into walls or roof components. Its architectural quality comes from that visible conversion: a young public building gains a tactile, experimental timber identity while demonstrating that temporary construction aids can become long-life spatial elements.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** student/reallab methodology using Stuttgart 21 timber formwork elements as structural/spatial triggers, then wrapping/protecting them with a simpler autonomous timber envelope.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** elliptical timber youth pavilion and protected interior/formwork pieces turn construction-site remnants into a social meeting place and spatial exhibit.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Stuttgart 210 ArchDaily: https://www.archdaily.com/1024776/stuttgart-210-think-ahead-build-on-hft-stuttgart
- Stuttgart 210 Divisare: https://divisare.com/projects/521618-achim-birnbaum-stuttgart-210-living-lab-ingersheim-pilot-project
- Ingersheim project page: https://www.ingersheim.de/website/de/freizeit-wein-kultur/pavillon

**Existing topology component hints**
- Jugendtreff Ingersheim — 12 curved CLT formwork elements as primary structure (FW: formwork→structure)
- Jugendtreff Ingersheim — CLT offcuts used for secondary fit-out elements

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="49-k118-kopfbau-halle-118-winterthur"></a>
## 49. K118 Kopfbau Halle 118 Winterthur

### MAPPING_ONLY — do not extract
- Project ID: `p_k118_kopfbau_halle_118_winterthur`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
K118 is one of the clearest examples of component-led architecture. Reclaimed steel, windows, facade elements, stairs and interior pieces are composed into an addition whose design was shaped by what could be found, tested and joined. The building does not hide heterogeneity; it turns it into architectural order through careful proportion, exposed assembly and precise detailing. The result is neither nostalgic nor improvised, but a rigorous architecture of visible second-use elements.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** material-inventory-led design: reused components were found, tested, dimensionally adapted and coordinated before/during design so that the new extension follows what was available.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** facade, structure, windows, stairs and interior surfaces express a collage of reclaimed components while remaining coherent as a new workplace addition.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- K118 In Situ: https://insitu.ch/projekte/196-kopfbau-halle-118
- K118 Zirkular: https://zirkular.net/en/project/k118/

**Existing topology component hints**
- Erhaltene Industriehalle Halle 118 als Sockel
- Wiederverwendete Fenster, Fassadenbleche und EPS-Dämmung
- Wiederverwendete Naturstein-/Granitplatten, Klinker und Holzplatten
- Wiederverwendete Stahlträger und Stützen der Aufstockung
- Wiederverwendete externe Stahltreppe

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="50-ka13-kristian-augusts-gate-13-oslo"></a>
## 50. KA13 / Kristian Augusts gate 13, Oslo

### MAPPING_ONLY — do not extract
- Project ID: `p_ka13_kristian_augusts_gate_13_oslo`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
KA13 shows how an ordinary office transformation can become a reuse-driven design exercise. The project keeps and upgrades existing structures while integrating reused components into facade, interior and technical strategies. Design quality comes from making circular construction appear professional and urban, not experimental in a fragile sense. The architectural output is a restrained commercial building whose material decisions reveal a shift from replacement culture toward careful reconfiguration and selective recovered-component use.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** major circular renovation methodology using donor buildings: façade panels, concrete decks, windows, grilles and stone decks sourced from other projects dictate specification and detailing.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** colourful reused façade panels, reused decks/railings/windows and preserved office building mass create the architectural identity of Norway’s circular building exemplar.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- KA13 FutureBuilt: https://www.futurebuilt.no/forbildeprosjekter/kristian-augusts-gate-13-oslo
- Circle Economy KA13: https://circle-economy.com/knowledge-hub/article/8422
- KA13 Entra report: https://www.entra.no/vare-eiendommer/alle-eiendommer/kristian-augusts-gate-13/_/attachment/inline/31ec37c5-5944-4338-a4db-826336969f42%3A8fd12a6e4418e59f3ffe7be9916e27b7e0239d8f/20230113_KA13_erfaringsrapport_engelsk.pdf

**Existing topology component hints**
- Erhaltenes KA13-Bestandstragwerk und Außenwände
- Wiederverwendete Bürofronten, Türen und Fassadenbekleidung
- Wiederverwendete Hohlkörperdecken aus Regjeringsbygg R4
- Wiederverwendete Radiatoren, Sanitär und Lüftungskanäle
- Wiederverwendeter Stahl in Bestand und Erweiterung

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="51-kamikatsu-zero-waste-center-hotel-why"></a>
## 51. Kamikatsu Zero Waste Center / Hotel WHY

### MAPPING_ONLY — do not extract
- Project ID: `p_kamikatsu_zero_waste_center_hotel_why`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Kamikatsu’s building is a civic emblem for a town organised around zero waste. Reused windows, fittings and materials help create an architecture that feels handmade, local and publicly legible. The design uses irregularity as a virtue: recovered pieces contribute to facade rhythm, interior warmth and narrative identity. Rather than hiding behind a generic eco-aesthetic, the building lets visitors read reuse through thresholds, surfaces and everyday details connected to the town’s waste-sorting culture.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** community-salvage methodology: materials are collected from local buildings and assembled into a zero-waste civic centre/hotel that embodies the town’s waste policy.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** mosaic façade of reclaimed windows and doors creates the building’s iconic elevation; interiors continue the recycled/reclaimed material atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Kamikatsu ArchDaily: https://www.archdaily.com/943994/kamikatsu-zero-waste-center-hiroshi-nakamura-and-nap
- Kamikatsu Dezeen: https://www.dezeen.com/2021/02/02/kamikatsu-zero-waste-centre-hiroshi-nakamura-nap/

**Existing topology component hints**
- Alte Fliesen als Mosaik-, Boden- und Traufendetail
- Alte Rathauswandteile als Exterior Receiving Wall
- Alte Shoji-Schirme und Glastüren im Hotel
- Ca. 700 gespendete Fassadenfenster
- Glas- und Keramikscherben als fester Bodenbelag

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="52-kindergarten-m-slistrasse-manegg-z-rich"></a>
## 52. Kindergarten Mööslistrasse / Manegg Zürich

### MAPPING_ONLY — do not extract
- Project ID: `p_kindergarten_moeoeslistrasse_manegg_zuerich`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The kindergarten applies reuse to a precise educational building type, where robustness, daylight, scale and atmosphere matter. Reclaimed components must be integrated into a child-friendly environment rather than showcased as raw salvage. The design interest is in how reused elements affect facade rhythm, interior tactility, structural decisions or play-space character while still meeting safety and comfort demands. Its strongest extraction should follow documented components, not a generic claim of circular construction.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** city-stock reuse methodology: reusable elements from former housing/city stock are identified and inserted into a kindergarten conversion, targeting emissions savings.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** exterior stair, canopy, railings, planters, shading structure, refurbished sinks/toilets and second-hand furniture create a pragmatic school architecture of visible reuse.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Kindergarten Mööslistrasse Zirkular: https://zirkular.net/en/project/kindergarten-moeoeslistrasse/
- Stadt Zürich Kindergarten: https://www.stadt-zuerich.ch/de/planen-und-bauen/portfolio/bauten-anlagen/schulbauten/kindergarten-moeoeslistrasse.html
- Swiss Architects Kindergarten: https://swiss-architects.com/de/architecture-news/bau-der-woche/re-use-macht-schule

**Existing topology component hints**
- Brandschutztüren aus Schulhaus Lavater
- Erhaltene Werkhofstruktur und Umnutzung ehemaliger Wohnungen
- Stahlpergola / Beschattung aus Einkaufswagendepot
- Wiederverwendete Akustikelemente
- Wiederverwendete Außentreppe
- Wiederverwendete Sanitärapparate und gebrauchte Küche
- Wiederverwendete Stahlträger / Unterzüge / Stützen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="53-liander-alliander-hq-duiven"></a>
## 53. Liander / Alliander HQ, Duiven

### MAPPING_ONLY — do not extract
- Project ID: `p_liander_alliander_hq_duiven`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Liander’s campus renovation uses reuse to reshape a corporate complex into a connected workplace. Existing buildings and recovered materials contribute to a large interior landscape under a new unifying roof, making reuse part of spatial organisation rather than just supply. The design quality lies in stitching fragments together: old structures, reused components and new circulation create a collective working environment with a warm, workshop-like atmosphere. Circularity is expressed through connection, openness and material layering.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** urban-mining and circular-campus methodology: existing materials and donor components are reorganised into a large workplace/campus, with reuse influencing the atrium/roof and interior identity.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** large covered interior streets/atrium and patchwork reused components create a circular workplace atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Alliander HQ RAU: https://rau.eu/portfolio/liander-2/

**Existing topology component hints**
- Erhaltene Bestandsgebäude des Campus
- Gemeinsame Überdachung / Atriumhülle als Transformationsbauteil
- Materialpass / dokumentiertes Materialinventar
- Teilweise wiederverwendete Innenausbau-Elemente

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="54-lo-reninge-town-hall-fa-ade-stadhuis-lo"></a>
## 54. Lo-Reninge Town Hall façade / Stadhuis Lo

### MAPPING_ONLY — do not extract
- Project ID: `p_lo_reninge_town_hall_facade`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Lo-Reninge town hall facade is a focused case where reclaimed material operates at the scale of civic image. Reused bricks or facade elements do not simply reduce impact; they shape how the public building meets the street and relates to local continuity. The design interest is in rhythm, texture, colour and weathering. Architectural output should therefore be described through the facade’s material presence and how recovered components support institutional dignity without appearing ornamental or nostalgic.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** contextual reclaimed-brick method: local/yellow reclaimed bricks are selected and detailed to relate to adjacent convent masonry using lime/slurry finish.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** soft pale reclaimed brickwork creates a historically embedded civic façade that is new but visually continuous with the town fabric.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Lo-Reninge Archello: https://archello.com/project/stadhuis-lo-reninge
- Lo-Reninge Building Design PDF: https://www.hughstrange.com/pdf/writing/noa-lo-reninge-bdtech-march-2013.pdf

**Existing topology component hints**
- Erhaltenes ehemaliges Kloster
- Wiederverwendete Fassadenziegel

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="55-lokomotion-technology-centre-mini-pilot-tampere"></a>
## 55. Lokomotion Technology Centre mini-pilot Tampere

### MAPPING_ONLY — do not extract
- Project ID: `p_lokomotion_technology_centre_mini_pilot_tampere`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Lokomotion mini-pilot tests reclaimed concrete and component reuse in an industrial or technological context. Its architectural importance is experimental: design decisions are constrained by what can be dismantled, certified and recomposed into a new demonstrator. Rather than offering a finished architectural language, the project helps define future rules for module selection, connection and structural confidence. Extract only where the recovered elements visibly determine form, span, envelope or spatial organisation.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Material-inventory-led design; Pre-deconstruction-audit-led design; Reuse-assessment-led design; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component architectural expression unclear from topology evidence

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- 27 wiederverwendete Hohlkörperdecken

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="56-lyc-e-michel-lucius-conversion-luxembourg"></a>
## 56. Lycée Michel Lucius Conversion, Luxembourg

### MAPPING_ONLY — do not extract
- Project ID: `p_lycee_michel_lucius_conversion_luxembourg`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The lycée conversion uses existing building stock as the starting condition for an educational architecture. Reuse becomes relevant where retained fabric and recovered components affect classrooms, circulation, facade or interior atmosphere. The design challenge is to make a transformed structure feel coherent for school life while preserving material value. Its architectural quality should be read through adaptive continuity: new learning spaces emerge by editing and reinterpreting what is already there rather than by total replacement.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** selective deconstruction/reuse pilot: school wings are transformed by salvaging and reinserting building materials instead of replacement/demolition.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** new library/classroom atmosphere derives from reused components and retained structures; exact output nodes should be limited to documented elements in graph/source.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Opalis Lycée Michel Lucius: https://opalis.eu/en/projects/conversion-two-wings-lycee-michel-lucius
- Daedalus Lycée Michel Lucius: https://www.daedalus.lu/projekte/neugestaltung-des-gelandes-des-lycee-michel-lucius/

**Existing topology component hints**
- 11,8 t Stahlprofile als Überdachung
- 12 Metall-Deckenpaneele / 4,3 m²
- 135 m² wiederverwendete Straßenpflasterplatten
- 38 Fertigbetonelemente als Rinnen
- 419 m² Gips-Akustikpaneele aus abgehängten Decken
- 61 m² Bodenblech als Fassadenbekleidung
- Stahlfassadenpaneele als Geländer

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="57-lysp8"></a>
## 57. LYSP8

### MAPPING_ONLY — do not extract
- Project ID: `p_lysp8`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
LYSP8 should be treated as a duplicate or stub of the fuller LysP8 entry. Its design description is therefore limited: the architectural relevance lies in a Basel reuse pilot where kitchens, doors, facade elements, tiles and metal grating are reintroduced into housing or mixed-use space. Keep this paragraph as mapping context only. The canonical project should carry the real design narrative, because that entry contains the component evidence needed to support extraction.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** reuse pilot in Basel housing: stock components are incorporated during design, likely requiring dimensional coordination and donor-source matching.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architectural output should be extracted only where reused façade, structural, or interior components visibly shape housing expression.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- LysP8 Zirkular: https://zirkular.net/en/project/lysp8/

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="58-lysp8-lysb-chelstrasse-8-reuse-pilot-basel-loeliger-strub-zirkular-stiftung-habitat"></a>
## 58. LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel (Loeliger Strub / Zirkular / Stiftung Habitat)

### MAPPING_ONLY — do not extract
- Project ID: `p_lysp8_basel`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
LysP8 is a practical architecture of many small recovered decisions rather than one heroic reused structure. Kitchens, doors, tiles, facade parts and steel grating steps are worked into a new or transformed building so that reuse influences thresholds, surfaces, circulation and domestic atmosphere. The design quality comes from careful matching: everyday components are given enough order to feel intentional, while their different origins remain readable as part of the building’s circular character.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** reuse pilot in Basel housing: stock components are incorporated during design, likely requiring dimensional coordination and donor-source matching.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architectural output should be extracted only where reused façade, structural, or interior components visibly shape housing expression.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- LysP8 Zirkular: https://zirkular.net/en/project/lysp8/

**Existing topology component hints**
- LysP8 — All kitchens reclaimed from a Zürich housing estate and stored for project
- LysP8 — DfD timber structure with screwed visible elements
- LysP8 — Oxacrete Nossim poured-earth floor (Oxara + Repoxit + KIBAG)
- LysP8 — Reuse façade components: roof tiles, window shutters, fibre-cement panels, railings
- LysP8 — Reused doors and tiles
- LysP8 — Reused steel grid grating steps for seat stair

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="59-maison-des-canaux-paris"></a>
## 59. Maison des Canaux, Paris

### MAPPING_ONLY — do not extract
- Project ID: `p_maison_des_canaux_paris`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Maison des Canaux turns a historic canal-side building into a circular-economy showcase through interior and building-component reuse. The design is less about formal novelty than about demonstrating how offices, event rooms and public spaces can be remade with recovered elements. Reused finishes, furniture, fixtures and construction details create a warm, visibly assembled atmosphere. The project’s architectural quality lies in making circular procurement feel hospitable, civic and compatible with heritage fabric.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular renovation platform/project; use only documented reclaimed material interventions rather than generic sustainability claims.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architectural output requires project-specific component evidence; otherwise mark as circular renovation context.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Low
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Maison des Canaux: https://www.maisondescanaux.paris/

**Existing topology component hints**
- Wiederverwendete Boden- und Wandbeläge
- Wiederverwendete Sanitärteile
- Wiederverwendete Türen / Raumabschlüsse
- Wiederverwendete feste Einbauten / technische Elemente

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="60-maison-dna-dna-house-asse"></a>
## 60. Maison DnA / dnA House, Asse

### MAPPING_ONLY — do not extract
- Project ID: `p_maison_dna_asse`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Maison DnA uses reclaimed components to give a small domestic project a distinctive material intelligence. The design should be read through how recovered elements influence openings, surfaces, structure or interior detailing, rather than through sustainability claims. Its architectural value lies in selective composition: second-hand parts are absorbed into a coherent house while retaining enough difference to reveal their origin. The result is domestic architecture shaped by availability, adaptation and careful detailing.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** BLAF experimental brick/wall research; only use for reclaimed-component nodes if graph/source proves reused bricks/components, otherwise it is not enough.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** possible brick tectonic output; do not assert reclaimed-material expression without evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Low/DoNotExtract
- **Important caution:** Source placeholder not adequate for Maison DnA; requires external verification.

**External source leads**
- ArchDaily Charles Malis: https://www.archdaily.com/804017/charles-malis-mamout-plus-willocx-plus-ld2

**Existing topology component hints**
- Neue innere Holzrahmenbox als Energie- und Nutzungsschicht
- Wiederverwendete Ziegelwände als äußere autonome Struktur

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="61-maison-vignette-auderghem"></a>
## 61. Maison Vignette, Auderghem

### MAPPING_ONLY — do not extract
- Project ID: `p_maison_vignette_auderghem`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Maison Vignette is a compact urban reuse case where architectural quality depends on precision at domestic scale. Reclaimed components shape the building through surface, opening, fixture or detail decisions rather than through a large structural gesture. The design challenge is to balance the irregularity of recovered materials with the intimacy and clarity expected in a house. Extraction should therefore focus on documented design effects: facade texture, interior atmosphere, custom details or spatial adaptation driven by recovered parts.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** bio/reclaimed material design: straw, clay plaster, reused facing bricks, unglued wood and load-bearing floors shape the house’s construction logic.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** wooden/bio-based house with reused brick and natural finishes produces a healthy, low-tech material atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Caviar Vignette: https://caviar.archi/vignette-brussels-belgium/
- Archiweek Vignette: https://archiweek.urban.brussels/en/event/vignette-3
- FCRBE project sheets: https://vb.nweurope.eu/media/21046/dt4_2_2_project-sheets_041023_lr.pdf

**Existing topology component hints**
- 13,5 m² wiederverwendete Terrakotta-Bodenfliesen
- 21 m² wiederverwendete Wandfliesen aus Solvay-Gebäude
- 3.000 wiederverwendete Ziegel für 36 m² Fassaden-Claustra
- 40 m² wiederverwendete Blausteinplatten
- Wiederverwendete Sanitärobjekte von Rotor DC

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="62-meduni-campus-mariannengasse-wien-baukarussell-pre-demolition-reuse"></a>
## 62. MedUni Campus Mariannengasse Wien — BauKarussell pre-demolition reuse

### MAPPING_ONLY — do not extract
- Project ID: `p_meduni_campus_mariannengasse`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
MedUni Mariannengasse is primarily a donor-side design resource rather than a recipient building. Its architectural relevance lies in pre-demolition selection: components are identified, removed and prepared so they can influence other projects’ design decisions. The project changes the design process by making future material availability visible before demolition. Do not describe a final architectural output unless a recipient building is linked; treat this as the supply-side moment where architecture becomes possible elsewhere.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Component-catalogue-led design; Material-inventory-led design; Pre-deconstruction-audit-led design; Donor-building / deconstruction-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component facade rhythm or patchwork facade; Collage interior / reused partition and fit-out language

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- MedUni Mariannengasse — Bike workshop equipment (donor batch)
- MedUni Mariannengasse — Doors repurposed as wall cladding (donor batch)
- MedUni Mariannengasse — Fluorescent tubes (hazardous removal, not reuse)
- MedUni Mariannengasse — Heavy-duty shelves (donor batch)
- MedUni Mariannengasse — Jugendstil glass ceiling retained in situ
- MedUni Mariannengasse — Paternoster cabins (donor batch → Wiener Aufzugmuseum)

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="63-mehrow-pilot-house"></a>
## 63. Mehrow Pilot House

### MAPPING_ONLY — do not extract
- Project ID: `p_mehrow_pilot_house`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Mehrow pilot house belongs to the experimental precast-concrete reuse lineage. Design begins with available large panels and the technical problem of turning them into a new domestic structure. The architectural output is expected to be modular, heavy and direct, with proportions inherited from the donor building system. Its value is in showing how housing components once designed for standardised urban blocks can be cut, transported and recomposed as a small prototype house.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching; Regional sourcing-led design; Storage-supported reuse design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Modular composition from reclaimed concrete/components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- 22 wiederverwendete WBS70-Wandplatten
- 27 wiederverwendete WBS70-Deckenplatten

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="64-melkinlaituri-primary-school-and-day-care-centre-helsinki"></a>
## 64. Melkinlaituri Primary School and Day-care Centre Helsinki

### MAPPING_ONLY — do not extract
- Project ID: `p_melkinlaituri_primary_school_daycare_centre_helsinki`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Melkinlaituri applies component reuse to a demanding public education programme. The design relevance lies in integrating recovered elements into a school and day-care environment that must be safe, durable, bright and legible for children. Reuse should be extracted only where it shapes facade, structure, interior surfaces or furniture at architectural scale. The broader design question is how reclaimed components can support institutional calm and everyday robustness rather than appear as temporary experimentation.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Specification/dimensional adaptation to reclaimed components

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component architectural expression unclear from topology evidence

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- 64 reused hollow-core slabs from Suutarila community centre

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="65-montessori-maassluis"></a>
## 65. Montessori Maassluis

### MAPPING_ONLY — do not extract
- Project ID: `p_montessori_maassluis`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Montessori Maassluis is relevant where reused components support a learning environment organised around flexibility, tactility and child-scaled spaces. The design should not be reduced to a material checklist. Architectural output depends on whether recovered elements shape classrooms, partitions, finishes, facade or furniture in ways that influence pedagogy and atmosphere. Keep extraction cautious: the strongest nodes should come from documented connections between reclaimed materials and the spatial qualities of the school.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching; Storage-supported reuse design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Geplante wiederverwendete Hohlkörperdecken

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="66-multi-brussels-reuse-in-multi"></a>
## 66. Multi Brussels / Reuse in MULTI

### MAPPING_ONLY — do not extract
- Project ID: `p_multi_brussels_reuse_in_multi`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
MULTI is a large-scale office transformation where reuse has to work within a commercial urban building rather than a small demonstrator. The design value lies in coordinating retained structure, reused interior elements and new performance requirements into a coherent workplace. Architectural quality comes from editing: keeping enough of the existing fabric to preserve embodied value while introducing reused components that shape fit-out, circulation and atmosphere. It demonstrates reuse as a mainstream redevelopment strategy.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** large-scale reuse consultancy methodology: reclaimed elements are identified and matched to contemporary construction requirements in a complex office transformation.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** extract output only for specific graph-documented components; likely reused interior/façade elements in a multi-layered office reuse narrative.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Rotor Multi: https://rotordb.org/en/projects/reuse-multi-project
- Rotor Architecture of Reuse Brussels: https://rotordb.org/en/projects/architecture-reuse-brussels
- BMA reuse Brussels PDF: https://bma.brussels/app/uploads/2024/10/The-architecture-of-reuse-in-Brussels.pdf

**Existing topology component hints**
- Wieder eingebaute Aufzugsmotoren
- Wiederverwendete Aluminiumprofile
- Wiederverwendete Blaustein-Fassadenblöcke und -platten
- Wiederverwendete Granit- und Natursteinplatten

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="67-mus-e-de-folklore-vie-frontali-re-musef-mouscron"></a>
## 67. Musée de Folklore Vie Frontalière / MUSEF Mouscron

### MAPPING_ONLY — do not extract
- Project ID: `p_musee_de_folklore_mouscron`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
MUSEF uses reuse in a museum context, where material traces can resonate with collection, memory and local culture. The design should be read through how recovered building elements shape display environments, circulation, surfaces or the relationship between old and new fabric. Reuse is architecturally meaningful if it supports the museum’s narrative atmosphere rather than simply supplying cheaper materials. Extract nodes only where component origin influences the visitor experience or spatial character.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Urban-mining-led design; Specification/dimensional adaptation to reclaimed components; Donor-building / deconstruction-led design

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Reclaimed-component facade rhythm or patchwork facade; Facade expression shaped by reclaimed components

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Wiederverwendete Fassadenziegel aus acht Mouscron-Abbruchquellen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="69-pavilion-circl-amsterdam"></a>
## 69. Pavilion Circl Amsterdam

### MAPPING_ONLY — do not extract
- Project ID: `p_pavilion_circl_amsterdam`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
This entry should be merged into the broader Circl case. Its design narrative is the same: a demountable pavilion whose architectural quality comes from material-bank thinking, reused components and carefully reversible construction. The building’s value is in presenting circularity as refined public architecture rather than as makeshift reuse. Use this paragraph only as duplicate context, and place extraction on the canonical Circl project where component evidence and relationships are more complete.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular-pavilion methodology: reuse considered from the start, with demountable timber, reused window-frame flooring, reused/recycled floor systems, and component value after first life.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** building operates as a demountable kit and circular interior; floors, ceiling insulation, timber structure and pavilion programme communicate material cycles.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Circl Architecten Cie: https://www.cie.nl/circl?lang=en
- Divisare Circl: https://divisare.com/projects/374731-de-architekten-cie-ossip-van-duivenbode-circl
- ULI Circl: https://europe.uli.org/2020-finalists/circl-a-building-that-became-a-movement/

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="70-people-s-pavilion-eindhoven"></a>
## 70. People’s Pavilion Eindhoven

### MAPPING_ONLY — do not extract
- Project ID: `p_peoples_pavilion_eindhoven`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The People’s Pavilion is architecture made from borrowed responsibility. Components were temporarily loaned, assembled without irreversible fixing, and returned after use, so the entire design is shaped by disassembly and accountability. The pavilion’s form and details make that ethic public: coloured cladding, modular scaffolding-like order and visible joints communicate that nothing is consumed permanently. Its architectural quality is festive but precise, turning a temporary event building into a manifesto for reversible civic construction.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** borrowed-materials methodology: all components are loaned, kept unharmed, and strapped together; no sawing, drilling, screws or glue so everything can return to owners.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** temporary pavilion expression comes from stacked/strapped borrowed beams, concrete, façade elements, roof glass and recycled plastic cladding; construction method is the architecture.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- People Overtreders W: https://www.overtreders-w.nl/en/peoplespavilion
- ArchDaily People Pavilion: https://www.archdaily.com/915977/peoples-pavilion-bureau-sla-plus-overtreders-w

**Existing topology component hints**
- Geliehene Betonpfähle / Betonelemente
- Geliehene Fassadenelemente
- Geliehene Holzträger
- Geliehenes Glasdach
- Pretty Plastic Schindeln aus Haushaltskunststoff

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="71-plattenpalast-berlin"></a>
## 71. Plattenpalast Berlin

### MAPPING_ONLY — do not extract
- Project ID: `p_plattenpalast_berlin`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Plattenpalast turns East German concrete panels into a small urban pavilion or house-like object, making large-panel construction visible outside its original housing-block context. The design works through displacement: familiar prefabricated slabs are recomposed into a compact, almost archetypal form. Architectural quality comes from the contrast between heavy industrial panels and the new scale of occupation. Reuse is not merely material saving; it produces a recognisable spolia of post-war housing culture.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** reuse of prefabricated concrete slab/panel stock as architectural system; design turns GDR housing panels into pavilion/house components.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** panel dimensions and joints create the architectural form and tectonic language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Plattenpalast Karlsruhe: https://www.karlsruhe.de/b1/stadtgeschichte/kunst_und_kultur/kunst_im_oeffentlichen_raum/plattenpalast

**Existing topology component hints**
- 13 WBS70-Wand- und Deckenelemente
- Fenster und Rahmen aus dem Palast der Republik

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="72-plattenvereinigung-berlin"></a>
## 72. Plattenvereinigung Berlin

### MAPPING_ONLY — do not extract
- Project ID: `p_plattenvereinigung_berlin`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Plattenvereinigung uses salvaged prefabricated panels as a public and cultural architectural statement. The design recomposes mass-housing components into a new pavilion-like structure, making the source system legible through joints, panel proportions and concrete surfaces. Its architectural value is both spatial and symbolic: components associated with standardised housing become a flexible civic object. The output depends on recognising the panels’ previous life while allowing them to support new gatherings and programmes.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** reassembly of reclaimed concrete panels into a new collective/pavilion form; prefabricated panel logic governs geometry and construction.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** visible concrete panel modules make the architectural expression.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Küpfer et al concrete reuse: https://www.sciencedirect.com/science/article/pii/S0959652622048090

**Existing topology component hints**
- Deckenelemente / Zwischendecke
- Ost- und westdeutsche Betonfertigteile
- Treppenelemente
- Wand- und Fassadenelemente aus Betonfertigteilen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="73-plp-london-hq-circular-studio-fit-out"></a>
## 73. PLP London HQ circular studio fit-out

### MAPPING_ONLY — do not extract
- Project ID: `p_plp_london_hq_circular_studio_fitout`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
PLP’s studio fit-out treats circularity as a workplace design method. Reclaimed and reused elements enter furniture, partitions, finishes and possibly lighting, shaping the atmosphere of an architectural office that wants its own space to demonstrate design values. The quality lies in editorial control: components with different origins are curated into a professional interior rather than left as a salvage collage. Extraction should focus on how recovered pieces define work zones, surfaces and social areas.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular fit-out methodology consolidating materials from former and new office spaces; reuse became the default procurement and design framework.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** workplace interior uses reused materials in a refined neutral atmosphere, proving circularity can produce high-quality office aesthetics and layouts.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- PLP Wallpaper: https://www.wallpaper.com/architecture/plp-architecture-circular-office-design-london-uk

**Existing topology component hints**
- Materialbibliothek-Oberflächen aus Projektmustern
- Reclaimed marble / feste Oberflächen
- Terrazzo-/Spolia-Arbeits- und Küchenflächen
- wiederverwendete feste Fit-out-Komponenten aus altem/neuem Studio

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="74-rcmi-concular-blueprint-project"></a>
## 74. RCMI / Concular blueprint project

### MAPPING_ONLY — do not extract
- Project ID: `p_rcmi_concular`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
RCMI is not a building design but a method-oriented project concerned with making component reuse insurable, certifiable or repeatable. Its design relevance is indirect yet important: it affects how architects can specify reclaimed components with confidence. Do not extract architectural output from this record. If existing graph structures allow, connect it to design methodology only as a process framework that reduces risk and enables future material-driven design decisions.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** blueprint/insurance/procurement project; create methodology node only at programme level if graph supports it, not architectural output.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** no building ArchitecturalOutput node; relates to enabling reuse markets and risk management.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** No/ResearchOnly
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Rotor Architecture of Reuse Brussels: https://rotordb.org/en/projects/architecture-reuse-brussels

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="75-re-use-h-fe"></a>
## 75. RE-USE Höfe

### MAPPING_ONLY — do not extract
- Project ID: `p_re_use_hoefe`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
RE-USE Höfe should be treated cautiously as a pilot or process context unless a specific built project is linked. Its architectural relevance appears to be the investigation of courtyard or housing situations through reused components and circular planning. The design description should stay methodological: possible effects on shared spaces, thresholds, surfaces and construction strategy need evidence before extraction. Keep it as a reuse-design context, not as a confirmed architectural output record.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `DesignMethodology` node proposed from current topology evidence.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `ArchitecturalOutput` node proposed from current topology evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="76-re-crete-footbridge-reused-concrete-blocks"></a>
## 76. Re:Crete footbridge — reused concrete blocks

### MAPPING_ONLY — do not extract
- Project ID: `p_recrete_footbridge_reused_concrete_blocks`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Re:Crete makes the structural consequences of reclaimed concrete explicit. Instead of crushing concrete into aggregate, the project stacks or recomposes large blocks into a bridge, so design decisions revolve around compression, geometry, contact surfaces and safe assembly. The architectural output is intentionally direct: a small piece of infrastructure that reveals the mass and previous life of the material. It demonstrates how reclaimed concrete can become form, structure and public object simultaneously.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** structural design around reclaimed concrete blocks; reused concrete pieces are assessed and recomposed into a pedestrian bridge.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** bridge form and structural logic are defined by discrete reclaimed concrete blocks/components.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- ReCrete SXL: https://sxl.epfl.ch/projects/recrete/
- Küpfer et al concrete reuse: https://www.sciencedirect.com/science/article/pii/S0959652622048090

**Existing topology component hints**
- 25 Betonblöcke / Bogensegmente aus Ortbeton-Kellerwänden

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="77-reallabor-b-e-ware"></a>
## 77. Reallabor B(e) Ware

### MAPPING_ONLY — do not extract
- Project ID: `p_reallabor_b_e_ware`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Reallabor B(e) Ware is best understood as a live testing environment for designing and building with reused materials. It should not be forced into a single architectural-output narrative unless a specific demonstrator is attached. Its design value is procedural: it examines how planning, procurement, regulation and construction details change when reused components become the starting point. Treat it as a methodological incubator that can feed project design decisions elsewhere in the graph.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** living-lab methodology to turn Berlin waste/secondary materials into ambitious local building structures, bridging research, testing and practice.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** output should be tied to specific demonstrator structures; otherwise use as methodology/research context only.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/Research
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Reallabor B(e)Ware NBL: https://www.nbl.berlin/projects/reallabor-be-ware/
- Reallabor B(e)Ware ZRS: https://www.zrs.berlin/project/reallabor-be-ware-gebaeudetragwerke-aus-sekundaermaterialien-made-in-berlin/

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="78-reallabor-b-e-ware"></a>
## 78. Reallabor B(e) Ware

### MAPPING_ONLY — do not extract
- Project ID: `p_reallabor_be_ware`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Reallabor B(e) Ware is best understood as a live testing environment for designing and building with reused materials. It should not be forced into a single architectural-output narrative unless a specific demonstrator is attached. Its design value is procedural: it examines how planning, procurement, regulation and construction details change when reused components become the starting point. Treat it as a methodological incubator that can feed project design decisions elsewhere in the graph.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** living-lab methodology to turn Berlin waste/secondary materials into ambitious local building structures, bridging research, testing and practice.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** output should be tied to specific demonstrator structures; otherwise use as methodology/research context only.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/Research
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Reallabor B(e)Ware NBL: https://www.nbl.berlin/projects/reallabor-be-ware/
- Reallabor B(e)Ware ZRS: https://www.zrs.berlin/project/reallabor-be-ware-gebaeudetragwerke-aus-sekundaermaterialien-made-in-berlin/

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="79-rebridge-structural-reuse-project"></a>
## 79. REBRIDGE structural reuse project

### MAPPING_ONLY — do not extract
- Project ID: `p_rebridge_structural_reuse_project`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
REBRIDGE is a research-oriented structural reuse project, so its architectural description should focus on potential design methodology rather than a finished building. It asks how reclaimed steel or structural elements can be verified, catalogued and redeployed safely. The design significance is in moving reuse from small finishes to primary structure, where spans, loads, connections and tolerances govern architectural possibilities. Extract architectural output only when a built demonstrator is explicitly linked.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** structural-reuse research/platform focusing on whole steel bridge spans/components as catalogued reusable assets.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** architectural output only when linked to an actual bridge/building installation; otherwise research node only.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** No/ResearchOnly
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Küpfer et al concrete reuse: https://www.sciencedirect.com/science/article/pii/S0959652622048090

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="80-recyclinghaus-hannover"></a>
## 80. Recyclinghaus Hannover

### MAPPING_ONLY — do not extract
- Project ID: `p_recyclinghaus_hannover`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Recyclinghaus Hannover is a dense architectural collage, but one controlled by building logic rather than random assemblage. Reused bricks, facade panels, profile glass, aluminium windows, sauna timber and exhibition boards shape envelope, interiors and details. The design accepts material heterogeneity while giving it a coherent house form. Its quality lies in the productive friction between domestic order and visible reclaimed origins: the building becomes a catalogue of recovered parts made habitable through careful composition.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** availability-first design: reclaimed components, especially windows/materials, are measured, certified and designed into the building; reversible/demountable detailing supports future reuse.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** façade and interior are visibly composed from heterogeneous reclaimed components; the house aesthetic is a deliberate collage of reuse.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Recyclinghaus Hannover Cityförster: https://www.cityfoerster.net/projects/recyclinghaus-136.html
- FCRBE project sheets: https://vb.nweurope.eu/media/21046/dt4_2_2_project-sheets_041023_lr.pdf

**Existing topology component hints**
- Abbruchziegel in nichttragenden Innenwänden
- Faserzement-/Eternitplatten als Fassadenbekleidung
- Holzleisten aus alten Saunabänken
- Messebauplatten als Wandverkleidung, Türen und Einbauten
- Profilbauglas aus alter Lackiererei
- Recyclingbeton in Fundament/Bodenplatte
- wiederverwendete Aluminiumfenster mit neuer Verglasung
- wiederverwendete Waschbecken / Sanitäreinbauten
- wiederverwendetes Wellblech als Fassadenkomponente

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="81-recypark-demets-recypark-anderlecht"></a>
## 81. Recypark Demets / Recypark Anderlecht

### MAPPING_ONLY — do not extract
- Project ID: `p_recypark_demets_anderlecht`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Recypark Anderlecht makes circularity tangible in a public waste facility. Second-hand steel beams and other recovered components determine major parts of the structure, while the building’s programme already concerns urban material flows. The design uses this overlap to produce an architecture that is both operational and didactic. Its spatial and structural order shows that a recycling centre can itself be built as a demonstrator of reuse, not only as a place where reuse begins.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** form-follows-availability structural method: final form depended on second-hand beams still to be found; Rotor helped select materials and set reuse methodology.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** recognisable salvaged structural timbers/frames shape the combined waste-collection centre and skatepark identity, making circular economy visible in a civic infrastructure.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Recypark Rotor: https://rotordb.org/en/projects/recypark-anderlecht
- RotorDC Recypark blog: https://rotordc.com/blog/inspiration-4/recypark-in-anderlecht-brussels-101
- RIBA J Recypark: https://www.ribaj.com/intelligence/recypark-in-anderlecht-belgium/

**Existing topology component hints**
- Brettschichtholzbögen Recypark Demets

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="82-refair-bordeaux-reuse-platform"></a>
## 82. REFAIR Bordeaux reuse platform

### MAPPING_ONLY — do not extract
- Project ID: `p_refair_bordeaux_reemploi_platform`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
REFAIR Bordeaux is a platform rather than a building, so its design paragraph should not invent architectural qualities. Its relevance is that it changes the conditions under which architects design: it makes reclaimed products visible, searchable and potentially specifiable. The design methodology is logistical and curatorial, linking supply, demand and project timing. Use it as context for future reclaimed-component design, not as evidence of facade, spatial or structural output.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `DesignMethodology` node proposed from current topology evidence.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** No `ArchitecturalOutput` node proposed from current topology evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="83-resource-rows-copenhagen"></a>
## 83. Resource Rows Copenhagen

### MAPPING_ONLY — do not extract
- Project ID: `p_resource_rows_copenhagen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Resource Rows gives old brickwork a new facade logic by cutting wall fragments into modules rather than cleaning individual bricks. This decision preserves mortar, colour variation and irregular edges, making the origin of the material visible in a controlled residential envelope. The design turns a technical problem into an aesthetic one: patchwork masonry panels create rhythm, depth and memory. Reuse shapes not only material content but the entire architectural image of the housing block.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** resource-efficiency and material-innovation methodology; old cement-mortar brick façades are cut into modules and reassembled rather than cleaned into individual bricks.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** irregular chessboard/patchwork brick façade modules, roof houses and reused wood/aluminium define the residential architecture.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Resource Rows Lendager: https://lendager.com/project/resource-rows/
- Resource Rows Detail: https://www.detail.de/de_en/brick-patchwork-for-the-climates-sake-resource-rows-in-copenhagen
- Circular Materials Resource Rows: https://circularmaterialsystems.com/en/case/02_en_resource-rows/

**Existing topology component hints**
- Ziegelfassadenmodule / Mauerwerksausschnitte Resource Rows

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="84-roots-in-the-sky-blackfriars-crown-court"></a>
## 84. Roots in the Sky / Blackfriars Crown Court

### MAPPING_ONLY — do not extract
- Project ID: `p_roots_in_the_sky_blackfriars_crown_court`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Roots in the Sky remains relevant as a planned or superseded reuse concept because unrealised status is not itself a reason to discard it. The design idea combines retained lower structures with a new timber-and-planting identity and possible reclaimed steel strategy. Its architectural significance lies in imagining how an existing court building could support a dramatically different public and ecological programme. Treat outputs as proposed design intentions, not built evidence, and keep extraction tied to documented reuse claims.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Pre-deconstruction-audit-led design; Reuse-assessment-led design; Urban-mining-led design; Specification/dimensional adaptation to reclaimed components; Storage-supported temporal matching

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** Expressed reused structure / reuse-driven structural logic; Structural grid or frame shaped by reclaimed steel

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium/TopologyOnly
- **Important caution:** No additional external source was captured in this deeper pass. Treat old graph/topology evidence as context only and verify online before writing the two new nodes.

**External source leads**
- No external source captured in this pass; verify before extraction.

**Existing topology component hints**
- Bestandsfundamente und erste Geschosse Blackfriars
- Geplante Stahlträger / Stahlprofile Roots

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="85-r-silience-la-ferme-des-possibles-stains"></a>
## 85. Résilience / La Ferme des Possibles Stains

### MAPPING_ONLY — do not extract
- Project ID: `p_resilience_la_ferme_des_possibles_stains`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Résilience combines reuse with bioclimatic construction to make a social and agricultural building feel materially rooted. Reused windows, radiators, granite paving, sanitary objects and lighting interact with earth, straw and timber, producing a facade and interior palette that is both pragmatic and atmospheric. The design quality lies in continuity between environmental performance and material character: reclaimed components help define daylight, thermal behaviour, texture and the everyday dignity of a community-oriented farm building.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** bioclimatic local-material methodology combining earth, straw, wood and reused construction materials; reclaimed windows form key façade element.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** long glazed façade made from reused windows, raw earth/straw/wood palette and Trombe-wall/bioclimatic logic shape the building’s atmosphere and environmental performance.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Resilience Construction21: https://www.construction21.org/france/case-studies/h/resilience-the-farm-of-possibilities-en.html
- Resilience PDF: https://www.leoffdd.fr/fichiersprojets/5ffc75b7a924a.pdf
- Resilience Plaine Commune PDF: https://plainecommune.fr/fileadmin/user_upload/Portail_Plaine_Commune/4_Vie_du_territoire/Presse/Sujets_MAG/Fabrique_de_la_ville/Fiche_MAG_19_EN.pdf

**Existing topology component hints**
- BTC-Ziegel Mur Trombe Résilience
- Doppeltverglaste Holzfenster Résilience
- Einfachverglaste Holzfenster Résilience
- Granitpflaster Résilience
- Gussradiatoren Résilience
- Leuchten Résilience
- Sanitärobjekte Résilience

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="86-saxum-vineyard-equipment-barn"></a>
## 86. Saxum Vineyard Equipment Barn

### MAPPING_ONLY — do not extract
- Project ID: `p_saxum_vineyard_equipment_barn_paso_robles`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Saxum barn converts oil-field drill-stem pipe and steel offcuts into an agricultural structure with a direct industrial presence. The design does not refine the components beyond recognition; it lets their strength, circular sections and weathering character define columns, roof support and large gates. Architectural quality comes from a precise fit between source and programme: rugged industrial salvage becomes appropriate vineyard infrastructure, giving the barn a tough, place-specific tectonic language.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** agricultural/industrial salvage methodology: oil-field pipe and recycled materials are transformed into winery equipment barn structure and enclosure.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** rugged exposed reclaimed pipe/steel tectonic gives the barn its industrial-agricultural aesthetic.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Saxum Vineyard Equipment Barn: https://www.claytonkorte.com/work/saxum-vineyard-equipment-barn/

**Existing topology component hints**
- Drill-Stem-Pipe Dachtragwerk Saxum
- Drill-Stem-Pipe Stützen Saxum
- Wetternde Stahl-Offcut-Tore Saxum

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="87-sch-renmoosstrasse-115-117-z-rich-m-nage-trois-stiftung-pwg-wettbewerb-2022"></a>
## 87. Schärenmoosstrasse 115/117 Zürich — ménage à trois (Stiftung PWG Wettbewerb 2022)

### MAPPING_ONLY — do not extract
- Project ID: `p_schaerenmoosstrasse_zuerich`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Schärenmoosstrasse proposes a careful conversion of existing office stock into housing, using retention and selective component reuse as design tools. The existing stair cores, buildings and possible reused structural hall elements shape collective spaces and access. Its architectural quality is not in a reclaimed-material collage but in spatial reprogramming: workplaces become dwellings through added communal rooms, galleries and shared thresholds. Treat specific reuse outputs as provisional until the graph confirms built component evidence.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** adaptive conversion competition focused on gentle appropriation of existing office stock into housing; only extract reclaimed-component nodes if graph has specific reused elements.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** DO NOT EXTRACT without stronger evidence
- **Candidate text:** spatial output is generous communal halls/encounters in adapted stock; reclaimed material output unproven.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Low/DoNotExtract
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Schärenmoos competition: https://competitions.espazium.ch/de/wettbewerbe/decisi/umnutzung-buro-zu-wohnen-scharenmoosstrasse-115-117-zurich

**Existing topology component hints**
- SMS Zürich — Existing stair cores retained
- SMS Zürich — Photovoltaic system, 250 m² PV roof array
- SMS Zürich — Self-supporting steel arcade / Laubengang
- SMS Zürich — Two-storey communal hall from UBS Datenzentrum Altstetten
- SMS Zürich — existing Micro+Dixa buildings retained in place

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="88-stuttgart-210"></a>
## 88. Stuttgart 210

### MAPPING_ONLY — do not extract
- Project ID: `p_stuttgart_210`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Stuttgart 210 is an umbrella research context for transforming construction-site and infrastructure remnants into architectural prototypes. Its design relevance is strongest where it leads to built pilots such as Jugendtreff Ingersheim. The methodology is to treat temporary formwork and site waste as a future material stock with geometry, marks and constraints. Do not extract a standalone architectural output unless a demonstrator is attached; use this record to connect research, sourcing and design experimentation.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** research programme translating Stuttgart 21 timber formwork waste into architectural prototypes; design accepts lost/available formwork pieces as constraints.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** outputs are pilot pavilions/youth spaces where formwork geometry produces unusual spatial/tectonic identity.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Stuttgart 210 ArchDaily: https://www.archdaily.com/1024776/stuttgart-210-think-ahead-build-on-hft-stuttgart
- Stuttgart 210 Divisare: https://divisare.com/projects/521618-achim-birnbaum-stuttgart-210-living-lab-ingersheim-pilot-project
- Ingersheim project page: https://www.ingersheim.de/website/de/freizeit-wein-kultur/pavillon

**Existing topology component hints**
- None in topology evidence.

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="89-superlocal-expogebouw-superlocal-pavilion"></a>
## 89. SUPERLOCAL Expogebouw / Superlocal Pavilion

### MAPPING_ONLY — do not extract
- Project ID: `p_superlocal_expogebouw_bleijerheide`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
SUPERLOCAL tests circular neighbourhood renewal by reusing components from high-rise demolition. Concrete apartment modules, window frames, kitchens, doors, railings and installation parts become design material for pavilions or new housing experiments. The architectural interest lies in maintaining component identity at different scales: whole room-sized pieces can become spatial modules, while smaller fittings carry everyday domestic memory. It is a district-scale reuse laboratory where demolition is treated as a source of architecture.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** circular estate methodology aiming to reuse materials from existing high-rise demolition into new homes/pavilions; tests component and concrete reuse at district scale.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** demonstrator building/pavilion output should be tied to reused concrete/brick/product components where documented.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Superlocal estate: https://www.superlocal.eu/sce-en/
- Küpfer et al concrete reuse: https://www.sciencedirect.com/science/article/pii/S0959652622048090

**Existing topology component hints**
- Drei Beton-Wohnungsteile / Großmodule
- Fensterrahmen / Kozijnen
- Feste Küche und Installationen
- Haustüren, Geländer und Brüstungen
- Heizkörper und Aluminiumrohre

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="90-svanen-the-swan-kindergarten-gladsaxe"></a>
## 90. Svanen / The Swan Kindergarten Gladsaxe

### MAPPING_ONLY — do not extract
- Project ID: `p_svanen_kindergarten_gladsaxe`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Svanen uses the demolition of an older school as a material basis for a new kindergarten. Roof tiles, bricks, timber trusses, rafters and facade elements are recovered and reintegrated, so the design links new child-centred spaces to the material memory of the site. Architectural quality comes from making reuse feel calm, safe and ordered. The building turns local demolition stock into a tactile educational environment rather than a spectacular salvage display.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** on-site circular building-site methodology: former school materials are mapped, recovered, stored and reused directly in the replacement kindergarten.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** kindergarten form and material character follow available on-site components; it is presented as a building where form follows availability.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Svanen Lendager: https://lendager.com/project/the-swan/
- Svanen Metropolis: https://metropolismag.com/projects/lendager-completes-the-worlds-first-ecolabeled-kindergarten/

**Existing topology component hints**
- Holz-Dachbinder / timber trusses
- Holzrafters / træspær
- Stahlfassadenelemente
- Wiederverwendete Dachziegel / roof tiles
- Wiederverwendete Ziegel / bricks
- Zerkleinerter Beton als Recycling-Zuschlag

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="91-the-green-house-utrecht"></a>
## 91. The Green House Utrecht

### MAPPING_ONLY — do not extract
- Project ID: `p_the_green_house_utrecht`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
The Green House is designed as a temporary, demountable restaurant and meeting pavilion that can move after its first use. Reused glass panels, timber floor elements, pavers and wall cladding influence the building’s greenhouse-like image and dry-assembly details. Its architecture is intentionally light, systematic and recoverable. The design quality comes from making reversibility visible but polished: a civic pavilion that behaves like a material bank without looking provisional.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** temporary demountable kit methodology; dimensions derive from reused smoked-glass façade panels and the whole pavilion is designed for relocation after 15 years.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** generic steel kit, reusable foundation blocks, reused glass second skin/greenhouse, and demountable detailing define the pavilion’s architectural expression.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- The Green House ArchDaily: https://www.archdaily.com/915728/the-green-house-architectenbureau-cepezed
- Dutch Architects Green House: https://dutcharchitects.org/projects/the-green-house-utrecht

**Existing topology component hints**
- Dämmung in Holzbodenelementen
- Neues demontierbares Stahltragwerk
- Pflasterklinker Erdgeschoss
- Pre-used wood Geschossdecke
- Rauchglas-Fassadenpaneele
- Wiederverwendete feste Wandverkleidung / wainscot

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="92-thoravej-29-copenhagen"></a>
## 92. Thoravej 29 Copenhagen

### MAPPING_ONLY — do not extract
- Project ID: `p_thoravej_29_copenhagen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Thoravej 29 transforms an industrial building into a community and workspace through radical retention and internal reuse. Existing structures, concrete deck elements, bricks, doors and other components are recut or reassigned, so the design reads as an edited continuation of the factory rather than a replacement. Architectural quality lies in the thickness of traces: old surfaces, reused stairs, improvised furniture boundaries and new communal spaces form a coherent, rough but carefully composed environment.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** radical adaptive reuse methodology: careful dismantling and reintegration of structural elements, surfaces and interior components achieves very high reuse/recycling rate.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architecture preserves and reconfigures the old factory into a community workspace; existing/reused surfaces and components create continuity and atmosphere.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Thoravej ArchDaily: https://www.archdaily.com/1034502/thoravej-29-pihlmann-architects
- Thoravej DAC: https://dac.dk/en/magazine/places/thoravej-29-what-can-be-reused-must-be-reused-376

**Existing topology component hints**
- Fassaden-/Ziegelüberschuss zu Boden/Pflaster
- Kunststofffenster im Bestand
- TT-/Betondecken zu Treppen
- Türen zu Tischplatten / Möbelgrenze

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="93-timber-square-london"></a>
## 93. Timber Square London

### MAPPING_ONLY — do not extract
- Project ID: `p_timber_square_london`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Timber Square combines retained printworks structure, new timber construction and selective reused steel into a layered office redevelopment. Reuse is not the only design driver, but it changes the structural and interior narrative: existing frames remain, reclaimed beams appear around cores, and CLT introduces a warmer contemporary layer. The architectural quality is in the legible coexistence of old industrial fabric, new timber order and targeted second-use steel within a commercial city block.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** hybrid retained-structure/CLT/reused-steel methodology; reused steel beams are selectively used around cores to support efficient CLT spans.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** retained printworks, CLT and reused-steel core zones create a layered structural/aesthetic output in a commercial redevelopment.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Timber Square Steel Construction PDF: https://steelconstruction.info/images/b/be/Timber_Square_London_1.pdf
- Timber Development Timber Square: https://timberdevelopment.uk/print-and-ink-buildings-timber-square/

**Existing topology component hints**
- CLT-Hybriddecken als Kontextbauteil
- Demontierbare TGA-/Plant-Komponenten
- Retained Print Building Structure
- Wiederverwendete Stahlträger
- Wiederverwendeter Stahlträger als Empfangstresen

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="94-tr-high-rise"></a>
## 94. TRÆ High-Rise

### MAPPING_ONLY — do not extract
- Project ID: `p_trae_high_rise_aarhus`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
TRÆ brings reclaimed and upcycled components into a high-rise timber context. Aluminium facade panels, reused or upcycled window elements, old timber floors and even wind-turbine blades for shading help shape an architecture that presents circularity at urban scale. The design challenge is refinement: reused materials must contribute to a coherent tower rather than appear experimental. Its output is a polished high-rise expression where circular components enter facade, interior surfaces and environmental devices.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** upcycle-timber high-rise methodology combining reused materials, timber systems and reclaimed aluminium façade at tower scale.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** timber high-rise expression and reclaimed façade materials present circular construction as refined high-rise architecture.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- TRAE Lendager: https://lendager.com/project/trae/
- TRAE ArchDaily: https://www.archdaily.com/1036295/trae-high-rise-building-lendager-arkitekter

**Existing topology component hints**
- Aluminium-Fassadenplatten
- Holzböden aus alten Fensterrahmen und Gellerup-Bauteilen
- Troldtekt-Akustikplatten
- Upcycled window elements
- Windturbinenflügel als Sonnenschutz

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="95-umar-unit-urban-mining-and-recycling-nest-empa-d-bendorf"></a>
## 95. UMAR Unit — Urban Mining and Recycling, NEST Empa Dübendorf

### MAPPING_ONLY — do not extract
- Project ID: `p_umar_unit`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
UMAR is a research apartment designed as a catalogue of reversible material cycles. Most components are selected for separability, take-back, reuse, recycling or compostability; reclaimed Jules Wabbes door handles add a small but explicit reused-component layer. The architectural output is a clean demonstrator rather than a salvage collage: dry joints, modular layers, visible systems and controlled material contrasts show how a dwelling can be designed for future disassembly and resource recovery.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** design-for-cycles methodology: every resource must be reusable, recyclable or compostable; components are separable and returnable to biological/technical cycles.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** experimental residential unit expresses reversible dry joints, separable layers, modular walls and circular material palettes as architectural language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- UMAR Empa: https://nest.empa.ch/urban-mining
- UMAR Werner Sobek: https://www.wernersobek.com/projects/nest-unit-umar/

**Existing topology component hints**
- UMAR — Aluminium + copper facade elements
- UMAR — Desso/Tarkett carpets (take-back product-service system)
- UMAR — DfD untreated timber structure + facade
- UMAR — Ecovative mycelium insulation boards
- UMAR — Jules Wabbes door handles (loan from Rotor; from Brussels Générale de Banque HQ)
- UMAR — Lindner Plafotherm heated/chilled ceiling panels (take-back service)
- UMAR — Magna Glaskeramik sintered recycled-glass panels (kitchen tabletop + bath cladding)
- UMAR — Recycled bricks + recycled insulation

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="97-upcycle-studios-copenhagen"></a>
## 97. Upcycle Studios Copenhagen

### MAPPING_ONLY — do not extract
- Project ID: `p_upcycle_studios_copenhagen`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Upcycle Studios turns waste streams into a marketable housing architecture. Reused windows, recycled concrete from metro works and timber offcuts are not merely technical substitutions; they shape facade modules, interior warmth and the project’s urban identity. The design is deliberately normal enough to prove circular construction can enter the housing market, yet specific enough for material origin to matter. Its architectural quality comes from making upcycling feel domestic, repeatable and visually composed.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** upcycling methodology using concrete waste, reused windows and reclaimed wood to make new housing while demonstrating commercial viability of circular construction.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** housing expression, large window modules, concrete elements and timber finishes are shaped by reused/upcycled sources, turning waste into a domestic aesthetic.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Upcycle Studios Lendager: https://lendager.com/project/upcycle-studios/
- UrbanNext Upcycle Studios: https://urbannext.net/upcycled-studios/

**Existing topology component hints**
- Dinesen-Offcuts als Böden/Wände/Fassaden
- Doppelverglaste Fenster
- Recyclingbeton aus Copenhagen Metro

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="98-verbiest-karreveld"></a>
## 98. Verbiest + Karreveld

### MAPPING_ONLY — do not extract
- Project ID: `p_verbiest_karreveld_brussels`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Verbiest + Karreveld transforms existing warehouse-like conditions with a deliberately frugal palette of recovered materials. Tiles, railings, ceiling systems, lights and stones from other sites are used to create homes, studios or collective spaces that retain a raw working character. The design quality lies in controlled roughness: reused elements are not polished away but arranged so they support domestic use, artistic production and a sense of accumulated urban material history.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** frugal warehouse transformation; consistent material reuse and existing-language embrace drive conversion into dwelling/studio/garden.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architecture keeps the warehouse character while creating domestic/artistic spaces; reused materials support a deliberate rough, adaptive material language.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Verbiest AgwA: https://www.agwa.be/en/projects/1718_verbiest/201/
- Verbiest Brussels Architecture Prize: https://brusselsarchitectureprize.be/en/project/esp-karreveld/

**Existing topology component hints**
- Karreveld abgehängte Decken und Leuchten
- Karreveld modulares Innenwandsystem
- Verbiest Dach- und Terrassenfliesen
- Verbiest dekorative Fliesen aus Hanzinelle
- Verbiest-Fliesen (Keramik/Stein) aus Palais des Expositions Charleroi
- Verbiest-Geländer aus Palais des Expositions Charleroi
- Verbiest-Steine (Natur-/Mauersteine) aus Palais des Expositions Charleroi

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="99-villa-welpeloo-enschede"></a>
## 99. Villa Welpeloo Enschede

### MAPPING_ONLY — do not extract
- Project ID: `p_villa_welpeloo_enschede`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Villa Welpeloo is a landmark harvest-map house. The architects searched the region for available waste and reclaimed materials, then allowed those discoveries to steer structure, cladding, insulation and interior elements. Steel from a textile machine, wood from cable reels and other recovered parts give the house an idiosyncratic but coherent language. Its architectural quality comes from making supply-chain improvisation rigorous: the building feels designed, yet its form and materiality remain visibly dependent on found resources.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** harvest-map / dynamic-final-design methodology: local waste/reclaimed materials are scouted first and then the design flexes around what becomes available.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** steel structure from textile machinery, reclaimed cladding/fixtures and locally sourced waste materials generate new forms and a materially explicit house.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Villa Welpeloo Superuse: https://www.superuse-studios.com/projectplus/villa-welpeloo/
- Circle Economy Villa Welpeloo: https://circle-economy.com/knowledge-hub/article/30046
- Ellen MacArthur Villa Welpeloo: https://www.ellenmacarthurfoundation.org/circular-examples/finding-and-utilising-waste-materials-for-construction-purposes

**Existing topology component hints**
- Bau-/Montagelift als Innenlift
- Holzfassade aus Kabeltrommeln
- Polystyrol-Dämmplatten aus Restplatten
- Stahlträger aus Paternoster-Textilmaschine

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="100-woongroep-boschgaard-den-bosch"></a>
## 100. Woongroep Boschgaard Den Bosch

### MAPPING_ONLY — do not extract
- Project ID: `p_woongroep_boschgaard_den_bosch`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Boschgaard combines collective housing, self-build culture and circular material use. Reclaimed facade systems, timber elements, doors and interior components can shape both the shared identity of the group and the tactile quality of everyday spaces. The design is likely strongest where participation and material reuse meet: residents encounter the building as something assembled, adapted and collectively cared for. Extraction should follow documented components, especially facade, timber structure, doors and fit-out.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** collective self-build/circular housing methodology using second-hand and bio-based components; extract only graph-documented reclaimed materials.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** architectural output likely combines participatory housing with visible reused/bio-based material details; requires project-specific evidence.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** Medium
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Woongroep Boschgaard: https://www.boschgaard.nl/

**Existing topology component hints**
- Aluminium-Fassadensystem
- HSB-Holz Balken und Ausbauholz
- Holz-Dachspanten / Brettschichtholz-Kniespanten
- Türen und Innenausbau

</details>
<!-- AGENT_IGNORE_END -->


---

<a id="101-zinneke-feder-masui4ever-brussels"></a>
## 101. Zinneke / FEDER Masui4ever Brussels

### MAPPING_ONLY — do not extract
- Project ID: `p_zinneke_feder_masui4ever_brussels`
- Use this only to match the existing Neo4j `Project` node.

### DESIGN_DESCRIPTION_CONTEXT — ignore for node extraction
<!-- AGENT_IGNORE_START: DESIGN_DESCRIPTION_CONTEXT. Narrative design summary only. Do not create nodes directly from this paragraph. -->
Zinneke’s building supports a cultural organisation whose identity already depends on collaboration, making, procession and public expression. Reused parquet, terrace boards, window frames, steel stairs, lintels, insulation and ventilation components can therefore become part of a workshop-like architectural atmosphere. The design value lies in coordination: procurement, co-design and technical reuse are brought into a lively cultural workspace. Architectural output should focus on how recovered elements shape circulation, surfaces and productive interiors.
<!-- AGENT_IGNORE_END -->

### EXTRACT: DesignMethodology node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** co-design/procurement methodology: reuse objectives are translated into legal procurement, material matching and collaborative implementation across parties.

### EXTRACT: ArchitecturalOutput node candidate
- **Extraction status:** CREATE/UPDATE if graph relation fits
- **Candidate text:** cultural workspace output derives from preserved/reused fabric and material interventions; exact nodes should follow documented components in graph/source.

<!-- AGENT_IGNORE_START: SOURCE_EVIDENCE_IGNORE. Evidence/context only. Do not collect node data from this block. -->
<details data-agent-ignore="true">
<summary>SOURCE_EVIDENCE_IGNORE — deeper research notes and source leads</summary>

- **Evidence confidence for the two new nodes:** High
- **Important caution:** Extract only if reused/reclaimed components actively shape design logic or architectural output; otherwise keep this as evidence only.

**External source leads**
- Zinneke Rotor: https://rotordb.org/en/projects/zinneke-feder-masui4ever
- Zinneke research paper: https://www.taylorfrancis.com/chapters/oa-edit/10.1201/9781003507670-11/beyond-innovative-procurement-katrien-steukers-micha%C3%ABl-ghyoot-lionel-devlieger-stephanie-van-de-voorde
- BMA reuse Brussels PDF: https://bma.brussels/app/uploads/2024/10/The-architecture-of-reuse-in-Brussels.pdf

**Existing topology component hints**
- Eichenparkett und Azobé-Terrassendielen
- Fensterrahmen (Zinneke)
- Kompletter Lüftungsverbund
- Stahl-Treppen
- Stahlträger als Stürze
- Steinwolle-Dämmplatten

</details>
<!-- AGENT_IGNORE_END -->
