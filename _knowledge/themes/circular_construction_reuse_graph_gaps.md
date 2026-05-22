# Country × Material Graph Gaps for Circular Construction Reuse Knowledge Graph

## Context

Corpus country/project counts:

- Germany: 11
- Belgium: 11
- UK: 9
- Netherlands: 9
- Switzerland: 6
- France: 5
- USA: 4
- Finland: 3
- Denmark: 3
- Norway: 1
- Japan: 1
- Luxembourg: 1

Top materials by country:

- Germany: Holz, Beton, Stahl, Ziegel, Lehm
- Belgium: Stahl, Beton, Holz, Naturstein
- UK: Stahl dominant, Holz
- Netherlands: Holz, Stahl, Beton
- Switzerland: Stahl, Beton, Holz, Naturstein, Lehm
- France: Holz, Stahl, Lehm
- USA: Stahl, Beton, Holz
- Finland: Beton / hollow-core slabs
- Denmark: Holz, Beton
- Norway: Beton / hollow-core slabs

## Ranking logic

The top 20 gaps are ranked by expected graph value:

1. Corpus frequency
2. Material prominence in the country cluster
3. Safety and regulatory uncertainty
4. Reusability of the knowledge pattern across countries and materials
5. Availability of norm/test/proof pathways that can be represented in the graph

Baseline assumption: EU rows should inherit EU CPR/Waste Framework concepts, especially product-vs-waste status, CE/DoP/DPP obligations, and future harmonised specifications for used products. The revised EU CPR explicitly opens the door for dedicated harmonised technical specifications for used construction products, while the DPP is intended to carry performance, conformity, technical and traceability data.

Source: <https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng>

## Top 20 graph gaps by expected value

| Rank | Country | Material | Project cluster | Missing Norms | Missing legal conditions | Missing tests | Missing pollutant checks | Missing processing methods | Priority level | Research sources | Suggested graph action |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | UK | Stahl | Steel-dominant structural reuse | PD CEN/TS 1090-201, EN 1090-2, Eurocode 3, SCI protocol, UKCA/CE interface | Building Regulations Part A; CDM 2015; waste duty-of-care; CE/UKCA status for placed-on-market reclaimed members | Provenance, visual inspection, section geometry, tensile/yield/elongation, Charpy where relevant, weldability/CEV, NDT of welds, corrosion loss, fire-protection evidence | Lead/chromate paint, PAH coatings, asbestos fireproofing, PCB sealants, cadmium/galvanic coatings | Dismantle by unbolting, cut out damaged ends, shotblast, decoat, redrill, recoat, recertify | P1 Critical | CEN/TS defines reuse assessment and declared mechanical/geometrical properties and weldability; SCI protocol covers data, inspection and testing. Source: <https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024> | Create `ReusableStructuralSteelMember` template with edges to `CEN_TS_1090_201`, `SCI_Protocol`, `TestProtocol`, `PollutantScreening`, `BoltedSpliceConnection`, `FireResistanceRequirement`, `CorrosionProtectionRequirement`. |
| 2 | Belgium | Stahl | High-count Belgian steel reuse | CEN/TS 1090-201, EN 1090-2, Eurocode 3, NBN national annexes | Regional waste/product boundary; Tracimat traceability; CPR/CE/DoP/DPP; liability split between salvager, engineer, contractor | Same steel test package as UK, plus batch grouping by provenance and execution class | Coatings with lead/chromate/PAH; asbestos fireproofing; PCB sealants | Selective deconstruction, traceable batch labelling, blasting/decoating, re-fabrication | P1 Critical | Tracimat starts with identification of hazardous/non-hazardous materials and follows selective demolition; Belgian federal CPR pages describe DPP/CPR information needs. Source: <https://www.fir-recycling.com/wp-content/uploads/2023/02/FPRGErkenning_Tracimatversie_Engels.pdf> | Add Belgium-specific `TraceabilityProcedure = Tracimat` and require `ProvenanceEvidence` before assigning steel strength class. |
| 3 | Germany | Stahl | High-count German structural steel | CEN/TS 1090-201, DIN EN 1090-2, DIN EN 1993, MVV TB/DIBt pathway | Whether reused member is CE-marked product, non-harmonised product needing Ü/ZiE/vBG route, or project-specific approval | Mechanical/chemical/weldability tests, geometry, corrosion, existing weld NDT, coating/fire proofing records | Lead/chromate coatings, PAH, asbestos, PCB, old fireproofing | Careful deconstruction, coating removal, trimming, new bolted connections, DIBt/project documentation | P1 Critical | DIBt explains German conformity mark/fitness-for-use routes; CEN/TS 1090-201 defines reuse assessment. Source: <https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques> | Add `GermanyApprovalPath` decision node: `CE_hEN`, `Ü_Zeichen`, `abZ/aBG`, `ZiE/vBG`, `ProjectSpecificEngineerAssessment`. |
| 4 | Netherlands | Stahl | Dutch circular steel / material-passport projects | CEN/TS 1090-201, NEN EN 1090-2, Eurocode 3, Bbl/NEN links | Bbl compliance, CE/DoP if placed on market, CB’23 quality-assurance and passport decision trees | Provenance grouping, mechanical testing, geometry/tolerances, weldability, corrosion, weld NDT | Lead/chromate/PAH coatings, asbestos, PCB, heavy metals | Passport creation, selective dismantling, reconditioning, bolted design-for-disassembly | P1 Critical | Dutch government CE rules, Bbl construction rules and Platform CB’23 quality-assurance guide are directly relevant. Source: <https://www.government.nl/themes/building-and-housing/construction-products/ce-marking-for-construction-products-supervision-and-control> | Create `DutchReuseQualityAssessment` node linked to `MaterialPassport`, `BblPerformanceRequirement`, and `CEN_TS_1090_201_TestProtocol`. |
| 5 | Switzerland | Stahl | Swiss steel-bearing reused components | CEN/TS 1090-201, SIA 263, SIA fire/durability rules, Swiss BauPG | BauPG/market-placement status, canton permit practice, responsibility for declaration of performance | Strength/weldability, geometry, corrosion, coatings, connection history, fire performance | Asbestos, PCB, PAH, heavy metals, chemical coatings | Dismantling, cutting, surface preparation, new bolted/clamped connections, coating renewal | P1 Critical | Swiss construction-product law context and pollutant sources list asbestos, heavy metals, PCB, PAH, wood preservatives and VOCs. Source: <https://openbim-knowledgebase.org/en/docs/chapter-5-swiss-climate-strategy-and-legislation/chapter-5-6-federal-act-on-construction-products-construction-products-act-baupg/> | Add Swiss `BauPGLegalStatus` and `SIA263PerformanceRequirement`; separate `ReusableSteel` from `WasteMetalScrap`. |
| 6 | Belgium | Beton | High-count concrete reuse and precast reuse | Eurocode 2, EN 206, EN 13369, product standards such as EN 1168/EN 13224/EN 13747 where applicable | Product-vs-waste status; regional demolition inventory; CPR/CE gap for reused elements | Drawings/provenance, cover scan, reinforcement scan, cores/rebound/UPV, carbonation, chloride, sulfate, cracks, fire exposure, load test where needed | Asbestos coatings/tiles, PCB joints, PAH/tar membranes, oil contamination, chlorides, heavy metals | Saw-cut, clean, remove screed/topping, repair edges, expose anchors, recast pockets, surface protection | P1 Critical | Belgium requires pre-demolition inventories; FCRBE covers product/waste status; ReCreate discusses legal/technical requirements for precast reuse. Source: <https://ec.europa.eu/environment/pdf/waste/studies/deliverables/CDW_Belgium_Factsheet_Final.pdf> | Create `ReclaimedConcreteElement` template with `ConditionAssessment`, `DurabilityAssessment`, `BearingZoneCheck`, `HazardousSubstanceInventory`. |
| 7 | Netherlands | Beton | Dutch precast/concrete reuse pilots | Eurocode 2, EN 206, EN 13369, EN 1168 for HCS where relevant, Bbl/NEN | Bbl compliance, demolition notification/permit trigger, CE status, CB’23 quality decision tree | Concrete strength, reinforcement/prestress detection, cracks after each handling stage, carbonation/chloride, fire history, load testing | Asbestos, PCB sealants, PAH membranes, chlorides, oil/heavy metals | Deconstruction-as-production-process, storage QA, repair, shortening, cleaning, traceable passporting | P1 Critical | Platform CB’23 quality assurance; Bbl; ReCreate notes testing must align with dismantling, transport, storage, refurbishment and reassembly stages. Source: <https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment-and-assurance-when-reusing-products-from-existing-structures_June2023.pdf> | Add lifecycle stage nodes: `PreDeconstructionAudit → DismantlingInspection → StorageInspection → RefurbishmentQA → ReassemblyAcceptance`. |
| 8 | Germany | Beton | German concrete/precast reuse | Eurocode 2, DIN EN 206, DIN EN 13369, DIN EN 1168 where HCS, DIBt/MVV TB | State building-code route; DIBt approval if no standard route; mineral-waste EBV if element becomes waste | Strength, cover, reinforcement, carbonation/chloride, crack mapping, bearing zones, anchorage, fire damage, load test | Asbestos spacers/coatings, PCB joints, PAH waterproofing, chlorides, heavy metals | Selective dismantling, cutting, cleaning, edge repair, new bearing pads, grouted/mechanical connections | P1 Critical | DIBt approval framework and Germany’s mineral substitute building-material rules are relevant when reused concrete shifts toward waste/recycled-product handling. Source: <https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques> | Add `GermanyConcreteReuseApprovalRoute` and `EBV_NotApplicableUnlessCrushedOrWaste` rule to avoid confusing component reuse with aggregate recycling. |
| 9 | Switzerland | Beton | Swiss concrete structural reuse | SIA 262, SIA 269 existing-structure assessment, EN/SIA product references | VVEA waste status, canton demolition/pollutant rules, BauPG market-placement issue | Cover/rebar scan, cores, carbonation/chloride, crack/damage, fire, remaining service life, load path | Asbestos, PCB, PAH, heavy metals, mineral oil contamination | Selective saw-cut, cleaning, surface repair, new supports, dry/mechanical connections | P1 Critical | Swiss VVEA covers mineral demolition waste; Swiss pollutant practice highlights asbestos, PCB, PAH, heavy metals and other contaminants. Source: <https://www.fedlex.admin.ch/eli/cc/2015/891/en> | Add `RemainingServiceLifeRequirement` and `VVEAWasteStatus` nodes to concrete elements. |
| 10 | Finland | Beton / hollow-core slabs | Finnish ReCreate HCS/precast cluster | EN 1168, Eurocode 2, Finnish national annexes, ReCreate QA procedure | Finnish rules acknowledge reuse in demolition permitting; CE marking not required if a product is reused without substantial modification, but modification can trigger new-product issues | HCS dimensions, strand location, end damage, bending/shear load tests, cracking after handling, carbonation/chloride, fire exposure, bearing length | Asbestos, PCB, PAH, chlorides, insulation contamination, mold/moisture | Careful deconstruction, lifting plan, end repair, shortening with specialist equipment, storage QA, grouted joints | P1 Critical | Finland-specific ReCreate/legal sources and policy brief clarify reuse and CE-marking ambiguity. Source: <https://recreate-project.eu/2025/05/27/which-regulation-pertains-to-deconstruction-and-reuse-of-precast-concrete/> | Build `HollowCoreSlabReuseProtocol` with explicit `StrandIntegrity`, `BearingZone`, `LoadTest`, `HandlingDamage` properties. |
| 11 | Norway | Beton / hollow-core slabs | Norwegian HCS reuse, low count but high transfer value | NS 3682:2022, EN 1168, Eurocode 2, TEK17 | NS 3682 documentation route; waste-plan/demolition obligations; legal status of reused product | Minimum full-scale testing rule, remaining service life, carbonation threshold, strand/bearing condition, shear/bending capacity, fire exposure | Asbestos, PCB, PAH, chlorides, heavy metals | Dismantle, inspect, classify, repair edges, document like new HCS, new grouted/shear-pocket connections | P1 Critical | Standards Norway states NS 3682 covers dismantling through assessment so HCS can be documented similarly to new slabs; ReCreate reports minimum full-scale testing of 2% and at least three slabs. Source: <https://standard.no/en/sectors/byggevarer/norwegian-standard-for-hollow-core-slabs-for-reuse--ns-3682/> | Treat NS 3682 as the reference ontology pattern for all HCS rows; add `FullScaleTestRate` and `CarbonationDepthTrigger`. |
| 12 | Germany | Holz | High-count timber reuse | Eurocode 5, DIN EN 14081/EN 338, DIN 4074 grading, DIN 68800 durability, fire rules | CE/DoP gap for reclaimed graded timber; German waste-wood restrictions if contaminated; proof of fitness for structural use | Species, grade, dimensions, moisture, density/stiffness NDT, biological attack, holes/notches, fastener damage, fire/charring | PCP, lindane, creosote, CCA, lead paint, formaldehyde, mold, asbestos dust | De-nailing, trimming, planing, kiln drying, sorting, regrading, surface treatment, traceable storage | P2 High | Timber reuse sources flag strength-grading uncertainty and NDT reassessment; EU wood-circularity sources highlight POPs/REACH/CLP contamination issues. Source: <https://www.iom3.org/asset/E62529EE-C75E-47E8-BE09F55791407110/> | Create `ReclaimedStructuralTimber` class with mandatory `StrengthGradingEvidence` and `WoodPreservativeScreening`. |
| 13 | Netherlands | Holz | Dutch timber reuse / circular building | Eurocode 5, NEN EN 14081/EN 338, NEN fire/moisture rules, CB’23 passports | Bbl compliance, CE status if re-marketed, CB’23 quality passport | Visual/NDT grading, moisture, stiffness, species, decay/insect attack, connection-hole damage | Wood preservatives, lead paint, mold, formaldehyde, asbestos dust | De-nail, trim, plane, dry, regrade, passport, reversible screw/bolt detailing | P2 High | CB’23 quality-assurance and passport guidance support Dutch reuse workflows. Source: <https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment-and-assurance-when-reusing-products-from-existing-structures_June2023.pdf> | Link `MaterialPassport` to `TimberStrengthGrade`, `MoistureClass`, `ServiceClass`, `BiologicalDurability`. |
| 14 | Belgium | Holz | Belgian reclaimed timber / FCRBE market | Eurocode 5, NBN EN 14081/EN 338, fire/durability rules | Product-vs-waste boundary, Tracimat inventory, CPR/CE ambiguity | Strength grading, moisture, decay, species, previous load/damage, connection defects | PCP/lindane, creosote, lead paint, asbestos contamination, mold | Careful salvage, de-nailing, trimming, planing, drying, batch sorting | P2 High | FCRBE and Tracimat sources support reclamation audit and traceability; timber sources flag grading/pollutant uncertainty. Source: <https://opalis.eu/sites/default/files/2023-10/en_id2023_fcrbe_finition_web.pdf> | Add `BelgianReclamationAudit` edge to timber components before `ReusePotential = structural`. |
| 15 | Switzerland | Holz | Swiss timber reuse | SIA 265, Eurocode-related timber product standards, fire/moisture/durability requirements | BauPG status, cantonal approval, contractual allocation of reuse liability | Species, moisture, strength grading/NDT, decay, insect attack, dimensional stability, connection-hole damage | PCP, lindane, creosote, formaldehyde, mold, asbestos dust, lead paint | De-nailing, trimming, planing, drying, regrading, reversible dry joints | P2 High | Swiss reuse legal framework and pollutant-screening sources support legal and hazardous-material nodes. Source: <https://www.cirkla.ch/en/publications-outils/projet-innosuisse/> | Add `SIA265PerformanceRequirement` and `ContractualWarrantyAllocation` properties. |
| 16 | Belgium | Naturstein | Belgian stone floors, stairs, façade elements | EN 12058 floors/stairs, EN 1469 cladding, EN 1341 paving, EN 12371/12372/14231/1936/13755 tests | CPR/CE if placed on market, product-vs-waste, Tracimat/predemolition inventory | Petrography, flexural strength, slip resistance, frost resistance, water absorption, dimensions, anchor-pullout for cladding | Asbestos backing/mastic, PAH/tar adhesives, salts, oils, heavy metals | Careful dismantling, cleaning, cut-to-size, surface refinish, redrilling anchors, batch grading | P2 High | FCRBE natural-stone sheets and EN 12058 test-method references cover fitness-for-use and required tests. Source: <https://opalis.eu/sites/default/files/2022-01/4.10_en_-_natural_stone_flooring_slab_v01_0.pdf> | Create `ReclaimedNaturalStoneSlab` with application-specific tests: floor = slip/abrasion; exterior = frost; façade = anchor/flexural. |
| 17 | Switzerland | Naturstein | Swiss stone façades/floors | EN/SN 12058, EN/SN 1469, SIA façade/anchorage rules | BauPG, canton permitting, VVEA if waste, pollutant-remediation duties | Petrography, flexural, frost, slip, water absorption, anchor condition, cracks/delamination | Asbestos adhesives, PAH, salts, oils, heavy metals | Dismantle, clean, saw, refinish, redrill, mechanical anchors/clips | P2 High | Natural-stone EN methods plus Swiss VVEA/pollutant sources. Source: <https://cdn.standards.iteh.ai/samples/11505/3673463ce1514a2ebf23dd8d24690556/SIST-EN-12058-2004.pdf> | Add `StoneApplicationContext` node so the graph does not reuse floor-slab data for façade anchorage without extra proof. |
| 18 | UK | Holz | Secondary UK timber reuse cluster | Eurocode 5 / UK NA, BS 4978 visual grading, EN 14081/EN 338, fire/moisture rules | Building Control Part A, CDM/waste duty, UKCA/CE if re-marketed | Visual/NDT grading, moisture, species, stiffness, decay, fastener-hole damage, fire performance | Lead paint, creosote, PCP/lindane, mold, asbestos contamination | De-nail, trim, plane, dry, regrade, new bolted/screwed reversible joints | P2 High | UK legal sources plus timber grading uncertainty sources. Source: <https://www.gov.uk/government/publications/structure-approved-document-a> | Add UK `BuildingControlEvidence` edge from timber element to structural calculations and inspection records. |
| 19 | Germany | Ziegel | German brick/masonry reuse | EN 771-1, EN 772 tests, Eurocode 6/DIN EN 1996, mortar EN 998, frost rules | Product-vs-waste, CE if marketed as masonry unit, heritage vs new-build use, landfill/waste if contaminated | Compressive strength, dimensions, water absorption, frost resistance, soluble salts, bond strength with new mortar | Soot, salts, lead paint/glaze, PAH/tar, asbestos-containing mortars/adhesives | Mortar removal, cleaning, sorting, grading, palletising, lime-mortar reuse detailing | P2 High | FCRBE brick sheet notes mortar removal and compressive-strength/bond issues; Germany legal route via DIBt if non-standard structural use. Source: <https://opalis.eu/sites/default/files/2022-01/2.40_en_-_reclaimed_solid_terracotta_brick_v01_0.pdf> | Add `ReclaimedBrickBatch` with `MortarTypeRemoved`, `SaltRisk`, `FrostExposureClass`, `MasonryDesignStrength`. |
| 20 | Germany | Lehm | German earth/clay reuse | DIN 18940/18945/18946/18947 family, Eurocode-adjacent structural verification, fire/moisture rules | Non-harmonised product status, project-specific approval, indoor-air/moisture responsibility | Clay content, grain size, compressive strength, shrinkage, erosion/water sensitivity, moisture sorption, microbial contamination | Mold, salts, organic contamination, old paints, asbestos dust from mixed demolition | Crush, sieve, rehydrate, reform blocks/plasters, dry, stabilize only where reversible/permitted | P2 High | German DIBt route is relevant for non-standard products; EU/FCRBE product-vs-waste logic applies where reclaimed earth is circulated. Source: <https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques> | Create `EarthenMaterialReuse` branch distinct from brick/concrete; add `MoistureSensitivityRequirement` and `ReversibleStabilisation` properties. |

## Highest-value graph implementation pattern

Steel and hollow-core slab rows should become reusable graph templates first.

Steel has the clearest cross-country norm anchor via `CEN/TS 1090-201`.

Hollow-core slabs have the strongest reuse-specific national precedent via Norway’s `NS 3682` and the ReCreate QA work.

Concrete, timber, stone, brick and earth can then inherit the same structure:

```text
LegalStatus
  → ApplicableNorm
  → TestEvidence
  → PollutantScreening
  → ProcessingMethod
  → ConnectionTechnique
  → PerformanceRequirement
  → ReuseDecision
```

## Suggested core graph classes

```text
ReusableConstructionProduct
ReusableStructuralSteelMember
ReclaimedConcreteElement
ReclaimedHollowCoreSlab
ReclaimedStructuralTimber
ReclaimedNaturalStoneSlab
ReclaimedBrickBatch
EarthenMaterialReuse
MaterialPassport
ProductWasteStatus
ApplicableNorm
LegalCondition
TestProtocol
PollutantScreening
ProcessingMethod
ConnectionTechnique
PerformanceRequirement
ReuseDecision
```

## Suggested high-value relationships

```text
hasApplicableNorm
hasLegalCondition
requiresTest
requiresPollutantCheck
requiresProcessingMethod
usesConnectionTechnique
mustSatisfyPerformanceRequirement
hasTraceabilityEvidence
hasMaterialPassport
hasApprovalRoute
hasReuseDecision
hasCountrySpecificConstraint
```

## First implementation priorities

1. Encode steel reuse first using `CEN_TS_1090_201` as the core norm node.
2. Encode hollow-core slab reuse using `NS_3682` and ReCreate QA stages as the reference model.
3. Add country-specific legal-status decision trees for Germany, Belgium, Netherlands, Switzerland, UK, Finland and Norway.
4. Add pollutant-screening branches by material rather than by country, then specialize with national legal references.
5. Separate true component reuse from recycling, downcycling and waste-derived substitute materials.
