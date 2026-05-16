# Energy and Climate Dimension for Circular Construction / Bauteilreuse Knowledge Graph

**Purpose:** source-of-truth research table for adding an energy / climate impact layer to a circular construction and building-component-reuse knowledge graph.

**Strict rule used here:** reuse is **not** assumed to be energy-positive. A project-level graph relationship is recommended only where a project source explicitly reports CO₂, energy, GWP, embodied-carbon, embodied-energy, LCA, or energy-performance evidence. Where the source only states circularity or material reuse without an energy or climate result, the recommended graph action is `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE` plus a data-gap node.

**Core LCA modules to model:**

- `A1_A3_PRODUCT`: production of new product / avoided new product production.
- `A4_TRANSPORT`: transport to site, including donor → storage → receiver.
- `A5_CONSTRUCTION_INSTALLATION`: installation, cutting, welding, coating, testing, wastage, construction energy.
- `B4_REPLACEMENT`: future replacement if reused element has shorter residual service life.
- `B6_OPERATIONAL_ENERGY`: heating, cooling, ventilation, lighting, operational energy.
- `C1_C4_END_OF_LIFE`: deconstruction, transport, waste processing, disposal.
- `D_BEYOND_SYSTEM_BOUNDARY`: benefits and loads beyond the system boundary, e.g. avoided production through reuse or recycling credits.

**Accounting statuses to store as an attribute:**

- `ZERO_BURDEN_ASSUMED`: source treats reused element as no upstream burden. Use only if source says so.
- `AVOIDED_PRODUCT_CREDIT`: source reports avoided impact compared with new product.
- `RESIDUAL_PROCESS_IMPACT`: source includes dismantling, transport, storage, testing, cleaning, coating, cutting, or remanufacturing.
- `ALLOCATED_PREVIOUS_LIFE`: some share of original production impact is assigned to the reuse cycle.
- `ACCOUNTING_METHOD_UNCLEAR`: source gives a CO₂ result but does not publish the calculation method.
- `NO_QUANTIFIED_ENERGY_CO2_EVIDENCE`: source gives no usable energy / CO₂ / LCA result.

## Research table

| Project | Country | Material/Bauteiltyp | Energy or CO₂ topic | Quantitative result if available | LCA method or standard | Boundary condition | Trade-off identified | Evidence source | Recommended graph action |
|---|---|---|---|---|---|---|---|---|---|
| K.118 / Kopfbau Halle 118, Winterthur | Switzerland | Reused steel structure, steel stair, windows, profiled sheet facade, granite facade slabs used as flooring, plus new bio-based materials | Embodied carbon and primary material savings through large-scale component reuse | Sources report about **60% construction-stage GHG reduction**. Source wording differs on **500 t CO₂ saved** vs **500 t primary material saved**; store both as source-specific claims, not as one merged value. | ZHAW / IOP case study; Swiss project reporting; no complete EN 15978 module breakdown in public summary | Construction / Erstellung compared with conventional new construction; operational energy not the main claim | Reused components strongly shaped design; reuse expertise, labour, dismantling, processing and reassembly can dominate costs; local reuse reduces transport burden | `P_CH_K118_INSITU`, `P_CH_K118_IOP`, `P_CH_K118_STEELDOC` | `ADD_PROJECT_GHG_REDUCTION_CLAIM`; `ADD_SOURCE_CONFLICT_FLAG`; `SET_ACCOUNTING_METHOD_UNCLEAR`; add material nodes for steel, window, natural stone, facade sheet |
| Kristian Augusts gate 13 / KA13, Oslo | Norway | Existing load-bearing system, radiators, donor-building components, windows and other building parts | Embodied carbon reduction from high reused-material share | FutureBuilt reports **nearly 80% reused materials** and **70% greenhouse-gas reduction**. | FutureBuilt circular building criteria / greenhouse-gas accounting; exact module split not fully public in summary | Material emissions / project greenhouse-gas comparison; source also mentions emission-free construction and waste target | Reuse required time, skilled personnel, logistics, storage, packaging and labelling; donor availability affected design | `P_NO_KA13_FUTUREBUILT`, `P_NO_KA13_REPORT` | `ADD_PROJECT_GHG_REDUCTION_CLAIM`; `ADD_MATERIAL_REUSE_PERCENTAGE`; `ADD_LOGISTICS_REQUIREMENT`; `SET_ACCOUNTING_METHOD_UNCLEAR` unless the full report is parsed |
| Thoravej 29, Copenhagen | Denmark | In-situ reused TT concrete slabs as stairs, facade / brick material as flooring and paving, retained plastic windows, doors reused as furniture boundary case | CO₂ reduction from transformation and self-reuse; operational-energy tension from retaining old windows | Project sources report **up to 88% CO₂ reduction vs new construction**, **95% material reuse by weight**, and **90% waste reduction**. | DTU analysis referenced by project source; DGNB Gold pre-certification; method not fully public | Renovation / adaptive reuse compared with new construction; unclear split between direct reuse, retention, recycling and avoided demolition | Retained windows have residual life but may underperform thermally; source flags later replacement when needed. Furniture reuse should not inflate building-component-reuse score. | `P_DK_THORAVEJ`, `P_DK_PIHLMANN`, local file `Thoravej_29_Copenhagen.md` | `ADD_PROJECT_CO2_REDUCTION_CLAIM`; `ADD_BOUNDARY_WARNING_RETENTION_VS_DIRECT_REUSE`; `ADD_RESIDUAL_SERVICE_LIFE_CONSTRAINT`; `SET_ACCOUNTING_METHOD_UNCLEAR` |
| Resource Rows, Copenhagen | Denmark | Reused brick wall modules, recycled timber, reused facade materials, recycled/reused construction products | Embodied-carbon reduction claim for upcycled / reused materials | Public secondary sources report around **29% CO₂ reduction during construction phase over 50 years**. The original LCA should be verified before hard ingestion. | LCA / LCC mentioned in project communication; exact EN 15978 modules not fully visible in summary | Whole project / construction phase comparison over service life; reuse and recycling mixed | Brick facade modules still need thermal, moisture and fixing strategy; do not model brick reuse as insulation | `P_DK_RESOURCE_ROWS` plus local file `Resource_Rows_Copenhagen.md` | `STAGING_ADD_PROJECT_LCA_CLAIM_PENDING_VERIFICATION`; `ADD_REUSE_VS_THERMAL_LAYER_NOTE`; `SET_ACCOUNTING_METHOD_UNCLEAR` |
| 55 Great Suffolk Street, London | UK | Reused structural steel profiles for new external access / service core | Embodied-carbon saving from reused steel; upfront embodied carbon of project | About **50 t CO₂ / CO₂e saved** from steel reuse; **386 kgCO₂e/m² A1-A5** upfront embodied carbon; reported reduction vs LETI target in local research file | A1-A5 upfront embodied-carbon assessment; steel comparison against new steel production factor; EN 1090 / CE conformity relevant to reuse certification, not LCA method | Steel claim mainly avoided new production; project A1-A5 includes broader retrofit / retention effects | Lower material price did not guarantee total cost saving because testing, certification, storage, reprocessing and first-of-kind coordination add effort | `P_UK_55GSS_ASBP`, `P_UK_55GSS_NLA`, local file `55_Great_Suffolk_Street_London.md` | `ADD_COMPONENT_CARBON_SAVING_STEEL`; `ADD_PROJECT_A1_A5_GWP`; `ADD_REUSE_CHAIN_DONOR_STOCKHOLDER_RECEIVER`; `SET_ACCOUNTING_STATUS_AVOIDED_PRODUCT_CREDIT_AND_PROCESSING_UNKNOWN` |
| Brent Cross Town Primary Substation, London | UK | Reused steel sections / steel screen for substation | Embodied-carbon saving from reclaimed steel; missed carbon-saving potential due design changes | Sources report **66 t CO₂e** or **99.2 t CO₂e** saving depending on source; **45% reused steelwork** and roughly **40% carbon saving** also reported; local research notes **22 t CO₂e missed** because material reservation no longer matched later design | ASBP / Arup case-study carbon reporting; SCI P427 reuse protocol relevant to steel assessment | Steelwork comparison, exact module boundary differs by source | Early reservation is necessary but design changes can strand reuse stock; testing and certification costs reduce simple material-price advantage | `P_UK_BRENT_ASBP`, `P_UK_BRENT_ARUP`, local file `Brent_Cross_Town_Primary_Substation_London.md` | `ADD_COMPONENT_CARBON_SAVING_STEEL_WITH_CONFLICTING_VALUES`; `ADD_MISSED_REUSE_SAVING`; `ADD_DESIGN_CHANGE_RISK`; `SET_ACCOUNTING_METHOD_UNCLEAR` |
| Tower Bridge Court / TBC London reuse chain from House of Fraser, London | UK | Reused structural steel from House of Fraser / 318 Oxford Street chain | Embodied-carbon saving from reused steel; cleaning, testing and certification burden | Local research records **48 t CO₂ saved** for reused steel. Public tonnage claims conflict: **16 / 20 / 40 / up to 100 t** steel. Overall **6,365 t CO₂ vs new build** and **265 kgCO₂e/m²** are not direct-reuse-only. | Project carbon comparison; steel testing / carbon-equivalent checks for weldability; exact LCA modules not public | Steel reuse chain; donor / receiver quantities differ by publication date and scope | Material traceability and versioned quantities are essential; samples, tests, cleaning and fabrication need their own process nodes | `P_UK_TBC_WILLMOTT`, `P_UK_TBC_NSC`, local file `House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` | `ADD_COMPONENT_CARBON_SAVING_STEEL_48T`; `ADD_SOURCE_CONFLICT_FLAG_FOR_MASS`; `DO_NOT_ATTACH_OVERALL_6365T_TO_DIRECT_REUSE`; `ADD_TESTING_PROCESS` |
| Hastings Pier Visitor Centre | UK | Reused pier deck timber used as cladding / envelope expression | No explicit energy, CO₂ or LCA result found in current case file | None found | None found | Boundary unknown; timber reuse quantity also missing | Reused timber cladding is not automatically insulation; fire, durability, moisture and maintenance may dominate performance | local file `Hastings_Pier_Visitor_Centre.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_DATA_GAP_CO2_LCA`; `ADD_PERFORMANCE_REQUIREMENT_FIRE_MOISTURE_DURABILITY` |
| AWM Münster Circular Office | Germany | Interior fit-out: glass partitions and doors, WC partitions, cable trays, wood, reused interior elements | Circular interior LCA / avoided conventional fit-out impacts | **13.32 t CO₂e saved** and **82% reduction** vs conventional office reconstruction; **4.39 t CO₂ saved** from reused glass partitions and doors; **1.7 t CO₂e** for hemp-lime is not direct reuse | Concular / urselmann circular assessment; local stages `S1-S3`, `S5` reported; method details not fully public | Interior fit-out / office reconstruction compared with conventional alternative | Interior reuse is easier than structural reuse, but fire, acoustic, safety and electrical testing remain relevant; furniture vs fixed-fit-out boundary must be explicit | `P_DE_AWM_CONCULAR`, local file `AWM_Muenster_Circular_Office.md` | `ADD_PROJECT_INTERIOR_CO2_SAVING`; `ADD_COMPONENT_GLASS_PARTITION_SAVING`; `SET_ACCOUNTING_METHOD_UNCLEAR`; `EXCLUDE_NON_REUSE_HEMP_LIME_FROM_DIRECT_REUSE_SAVING` |
| Recyclinghaus Hannover | Germany | Reused facade panels, glass, windows, timber boards, tiles, interior materials | Stored carbon / material carbon; operational-energy trade-off for reused windows | Source records about **100 t CO₂ bound / stored**, but this is **not** a direct-reuse saving. CO₂-saving method not public. | No complete public LCA method found | Whole building material storage, not avoided-production claim | Old window frames were retained / reused but glazing had to be replaced with triple glazing for thermal performance; shows reuse-vs-retrofit trade-off | `P_DE_RECYCLINGHAUS_ZAB`, local file `Recyclinghaus_Hannover.md` | `ADD_STORED_CARBON_METRIC_NOT_AS_REUSE_SAVING`; `ADD_ENERGY_PERFORMANCE_CONSTRAINT_WINDOWS`; `NO_DIRECT_REUSE_CO2_SAVING_EDGE_UNTIL_METHOD_FOUND` |
| Plattenvereinigung, Berlin | Germany | Reused precast concrete / Plattenbau elements from Munich and Frankfurt/Oder | Transport energy / logistics risk for heavy concrete elements | No CO₂ or energy result found | None found | Heavy components transported across long distances; transport emissions not quantified | High-mass concrete reuse may lose climate advantage if long transport, cutting, handling or certification burdens are large | local file `Plattenvereinigung_Berlin.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_TRANSPORT_ENERGY_DATA_GAP`; `ADD_HEAVY_COMPONENT_LOGISTICS_RISK` |
| CRCLR House / Impact Hub Berlin | Germany | Reused / recycled bricks, timber, fit-out and circular material strategies | Climate relevance discussed qualitatively; no project-specific CO₂ or energy result found in current file | None found | None found | Mixed reuse, recycling, renovation and social-economy strategies | Avoid treating circular-branding as LCA evidence; require masses, transport and processing data | local file `CRCLR_House_Impact_Hub_Berlin.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_DATA_GAP_LCA_AND_MASSES`; `KEEP_REUSE_RECYCLING_SEPARATE` |
| Circular Centre Netherlands / Prinsenhof A reuse pilot | Netherlands | Demounted precast concrete floor and facade elements, donor-building concrete, structural elements | Embodied-carbon potential from reuse of precast concrete; donor/receiver status uncertainty | Local research records **550 floor elements**, **350 facade elements**, **17,000 t material**, **12,000 t concrete**, **3,500 t CO₂** and **92% reuse** from project / supplier source; method and final receiver integration need verification | ReCreate / Lagemaat / project reporting; LCA method not fully public in current source | Demolition / demounting and potential reuse; not all elements necessarily installed in final receiver at time of source | Donor and receiver must be temporally coupled; storage, refurbishment, transport, facade insulation and certification matter | `P_NL_CCN_RECREATE`, `P_NL_LAGEMAAT`, local file `Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` | `WATCHLIST_PENDING_BUILT_RECEIVER`; `ADD_DONOR_MATERIAL_CARBON_POTENTIAL`; `DO_NOT_ADD_FINAL_PROJECT_CO2_EDGE_UNTIL_INSTALLED_QUANTITIES_CONFIRMED` |
| SUPERLOCAL Expogebouw, Bleijerheide / Kerkrade | Netherlands | Reused concrete panels and components from donor flats; windows / frames; local demolition material | High material reuse, but no public CO₂ result found for Expogebouw in current file | **95% reused materials** reported, but **CO₂ saving unknown** | No public LCA method found in current file | Demonstrator building; component reuse and recycling mixed | Old windows / frames had asbestos and thermal-performance constraints; later housing market query used to learn performance limits | `P_NL_SUPERLOCAL`, local file `Superlocal_Expogebouw_Bleijerheide.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_MATERIAL_REUSE_PERCENTAGE_ONLY`; `ADD_POLLUTANT_AND_THERMAL_PERFORMANCE_CONSTRAINT` |
| Woongroep Boschgaard, Den Bosch | Netherlands | Reused timber, aluminium facade components, recovered materials, high-performance new energy systems | Whole-project CO₂ reduction claim plus operational-energy systems | Sources report **70% CO₂ saving vs current building standard** and **234 PV modules**; method and boundary are not transparent enough for precise module allocation | Project / Superuse reporting; no public EN 15978 module split in current file | Whole project; direct reuse, new bio-based / low-carbon materials, PV, heat pumps and geothermal effects may be mixed | Energy-efficient operation depends on new insulation, PV, heat pumps and geothermal systems; do not attribute all carbon reduction to reuse | `P_NL_BOSCHGAARD_SUPERUSE`, local file `Woongroep_Boschgaard_Den_Bosch.md` | `ADD_PROJECT_CO2_REDUCTION_CLAIM_WITH_LOW_METHOD_CONFIDENCE`; `ADD_OPERATIONAL_ENERGY_SYSTEMS`; `DO_NOT_ATTRIBUTE_FULL_70PCT_TO_REUSE` |
| Alliander / Liander HQ, Duiven | Netherlands | Circular transformation, existing buildings, material passports, energy concept | Energy-positive / sustainable operation context, but direct-reuse CO₂ data not isolated | No direct-reuse CO₂ result found in current case file; BREEAM / energy-performance claims need separate source parsing | BREEAM / circular design reporting; not direct component-reuse LCA in current evidence | Whole-site transformation; operational energy central but reuse share unclear | Broad circular-building cases mix retention, energy systems, material passports and design-for-disassembly; graph must separate them | local file `Liander_Alliander_HQ_Duiven.md` | `NO_DIRECT_REUSE_CO2_EDGE`; `ADD_OPERATIONAL_ENERGY_CONTEXT_ONLY_IF_QUANTIFIED_SOURCE_FOUND`; `ADD_METHOD_BOUNDARY_WARNING` |
| Verbiest / Karreveld reuse cases, Brussels | Belgium | Existing structure, reused interior elements, new timber reinforcement, hemp insulation | Operational-energy strategy and grey-energy trade-off; no quantified project CO₂ result found | No CO₂ result found; source notes heated area reduced by about half and local hemp insulation | No public LCA method found in current file | Operational energy / heated-zone reduction; not a direct component-reuse LCA | Reducing heated area may save operational energy; adding insulation has embodied-energy cost; reused office elements need safety / electrical checks | local file `Verbiest_Karreveld_Brussels.md` | `NO_PROJECT_LEVEL_CO2_EDGE`; `ADD_OPERATIONAL_ENERGY_STRATEGY_NODE`; `ADD_GRAUE_ENERGIE_VS_HEATING_TRADEOFF_DATA_GAP` |
| Musée de Folklore, Mouscron | Belgium | Reused bricks / masonry elements, mixed with new brickwork | Brick reuse has likely embodied-carbon relevance but no project LCA or CO₂ result found | **30,000 bricks** or **28,500 bricks / 34 m³** depending on source; **25% reuse-brick share** reported; no CO₂ value | No public LCA method found in current file | Material quantity only; no transport, cleaning or testing carbon boundary | Cultural reuse and visible material history do not equal quantified climate benefit; source conflicts on quantities | local file `Musee_de_Folklore_Mouscron.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_MATERIAL_QUANTITY_WITH_SOURCE_CONFLICT`; `ADD_LCA_DATA_GAP` |
| Charles Malis, Molenbeek | Belgium | Existing facade retained, floor / lighting reuse, technical / energy consultant involved | Energy retrofit context without reuse-specific CO₂ evidence | No CO₂ result found | No public LCA method found in current file | Building renovation and small fixed reuse elements; direct-reuse quantities low | Existing facade/technical upgrade may improve energy performance, but reuse quantity and carbon effect are not public | local file `Charles_Malis_Molenbeek.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_ENERGY_RETROFIT_CONTEXT_ONLY`; `ADD_REUSE_QUANTITY_DATA_GAP` |
| Grande Halle de Colombelles | France | Reused mineral wool insulation, sanitary equipment, regional recovered materials, on-site reuse workshop | Waste avoidance, insulation performance and processing/logistics burden | **19 t waste avoided and reused** reported; CO₂ figure appears in unclear unit in source and should **not** be converted to t CO₂ | FCRBE / Construction21 / Ekopolis case sources; no robust kg/t CO₂e LCA result found | Regional reuse logistics and on-site workshop; source quantities differ for insulation, e.g. 430 m² vs 200 m² | Reused insulation requires condition, thermal and fire verification; cleaning, sorting and workshop labour are real burdens | `P_FR_GRANDE_HALLE_FCRBE`, local file `Grande_Halle_de_Colombelles.md` | `NO_PROJECT_LEVEL_CO2_EDGE`; `ADD_WASTE_AVOIDED_METRIC`; `ADD_REUSED_INSULATION_PERFORMANCE_REQUIREMENT`; `ADD_PROCESSING_ENERGY_DATA_GAP` |
| ReCreate Finnish cluster / Tampere precast concrete pilots | Finland | Reused precast concrete: hollow-core slabs, columns, beams, facade / sandwich elements from donor office building | Embodied-carbon potential of structural concrete reuse; EPD and LCA development; service-life / carbonation assessment | Project-specific Finnish CO₂ result not found in the public pilot summaries used here. ReCreate / CORDIS states that reuse of precast components can reduce energy consumption and carbon footprint by **93-98%** compared with virgin production, but this is a programme-level claim, not a Finnish building-specific result. 2026 mini-pilot: **55 reused elements** installed: 35 hollow-core slabs, 13 columns, 7 beams. | ReCreate LCA / EPD development; ISO / EN building-LCA context; EN 16757:2022 carbonation discussion for concrete | Donor building in Tampere; deconstruction, refurbishment by Consolis Parma, structural design by Ramboll; receiver pilot buildings | Remaining service life, carbonation, corrosion risk, quality assurance, logistics and standardisation determine whether reuse is feasible; do not use generic 93-98% as project result | `P_FI_RECREATE_FINLAND`, `P_FI_RECREATE_2026_MINIPILOT`, `P_EU_RECREATE_CORDIS`, `P_FI_RECREATE_CARBONATION` | `ADD_R_AND_D_PILOT_NODE`; `ADD_LCA_METHOD_NODE_FOR_REUSED_PRECAST_CONCRETE`; `NO_PROJECT_LEVEL_CO2_EDGE_FOR_FINNISH_PILOT_UNTIL_BUILDING_LCA_FOUND`; `ADD_SERVICE_LIFE_AND_QA_CONSTRAINTS` |
| Big Dig House, Lexington, Massachusetts | USA | Reused concrete roadway panels, steel and infrastructure components from Boston Big Dig | Potential embodied-energy benefit from heavy component reuse, but no quantitative CO₂ / energy evidence found in current file | None found | None found | Residential building using infrastructure components; transport, cutting, thermal bridge and structural adaptation unknown | Heavy concrete and steel reuse may create thermal bridges or transport burdens; absence of LCA prevents climate claim | local file `Big_Dig_House_Lexington_Massachusetts.md` | `NO_PROJECT_LEVEL_ENERGY_CO2_EDGE`; `ADD_DATA_GAP_TRANSPORT_PROCESSING_THERMAL_BRIDGES`; `ADD_US_CASE_WITH_NO_LCA_EVIDENCE` |

## Graph schema additions recommended from this track

### New node labels

- `EnergyClimateClaim`
- `EmbodiedCarbonClaim`
- `EmbodiedEnergyClaim`
- `OperationalEnergyClaim`
- `LCAMethod`
- `LCAModule`
- `AccountingStatus`
- `TransportEnergyBurden`
- `ProcessingEnergyBurden`
- `ResidualServiceLife`
- `PerformanceTradeoff`
- `SourceConflict`
- `DataGap`

### New relationship types

- `(Project)-[:HAS_CARBON_CLAIM]->(EmbodiedCarbonClaim)`
- `(Project)-[:HAS_OPERATIONAL_ENERGY_CLAIM]->(OperationalEnergyClaim)`
- `(Claim)-[:USES_METHOD]->(LCAMethod)`
- `(Claim)-[:COVERS_MODULE]->(LCAModule)`
- `(Component)-[:AVOIDS_PRODUCTION_OF]->(NewProductScenario)`
- `(Component)-[:REQUIRES_PROCESS]->(ProcessingEnergyBurden)`
- `(Component)-[:REQUIRES_TRANSPORT]->(TransportEnergyBurden)`
- `(Component)-[:HAS_RESIDUAL_SERVICE_LIFE]->(ResidualServiceLife)`
- `(Component)-[:HAS_PERFORMANCE_TRADEOFF]->(PerformanceTradeoff)`
- `(Claim)-[:HAS_ACCOUNTING_STATUS]->(AccountingStatus)`
- `(Claim)-[:HAS_SOURCE_CONFLICT]->(SourceConflict)`
- `(Project)-[:HAS_DATA_GAP]->(DataGap)`

### Required properties for every carbon / energy claim

```yaml
claim_value: number | string
claim_unit: kgCO2e | tCO2e | kgCO2e_per_m2 | percent | kWh | MJ | unknown
claim_topic: embodied_carbon | embodied_energy | operational_energy | transport_energy | processing_energy | stored_carbon | waste_avoided
baseline: new_product | conventional_building | new_build | current_standard | unknown
lca_modules: [A1_A3, A4, A5, B4, B6, C1_C4, D]
accounting_status: ZERO_BURDEN_ASSUMED | AVOIDED_PRODUCT_CREDIT | RESIDUAL_PROCESS_IMPACT | ALLOCATED_PREVIOUS_LIFE | ACCOUNTING_METHOD_UNCLEAR | NO_QUANTIFIED_ENERGY_CO2_EVIDENCE
is_direct_reuse_only: true | false | mixed | unknown
includes_transport: true | false | unknown
includes_processing: true | false | unknown
includes_testing: true | false | unknown
includes_storage: true | false | unknown
includes_operational_energy: true | false | unknown
source_confidence: high | medium | low
source_url_or_file: string
notes: string
```

## Source registry

### Standards and method references

- `S_ISO_14040` — ISO 14040, Environmental management — Life cycle assessment — Principles and framework. https://www.iso.org/standard/37456.html
- `S_ISO_14044` — ISO 14044, Environmental management — Life cycle assessment — Requirements and guidelines. https://www.iso.org/standard/38498.html
- `S_EN_15804` — EN 15804 / DIN EN 15804, sustainability of construction works, environmental product declarations, core rules for construction products. https://standards.iteh.ai/catalog/standards/cen/456c728f-7d3f-44d9-8dc4-d80e1ccf1a45/en-15804-2012a2-2019
- `S_EN_15978` — EN 15978, sustainability of construction works, assessment of environmental performance of buildings. https://standards.iteh.ai/catalog/standards/cen/62c22cef-5666-4719-91f9-3e2deac8a2094/en-15978-2011
- `S_SFOE_REUSE_LCA_2025` — Swiss Federal Office of Energy, Reuse-LCA final report, 2025; includes A1-A3, A4, B4, C1-C4 and logistics / reconditioning focus. https://zirkular.net/wp-content/uploads/2025/07/8169-20250331-reuse-lca-heig-vd-final-report-e-ec-vf2.pdf
- `S_NORDIC_LCA_REUSE` — Nordic Sustainable Construction, reuse of construction materials rewarded in Nordic building LCA. https://www.nordicsustainableconstruction.com/news/2023/may/reuse-of-construction-materials

### Project / case sources

- `P_CH_K118_INSITU` — baubüro in situ, K.118 Kopfbau Halle 118. https://www.insitu.ch/projekte/196-k118-kopfbau-halle-118
- `P_CH_K118_IOP` — Stricker et al., “Case Study K.118 – The Reuse of Building Components in Winterthur, Switzerland,” Journal of Physics: Conference Series 2600, 2023. https://doi.org/10.1088/1742-6596/2600/19/192008
- `P_CH_K118_STEELDOC` — steeldoc, Kopfbau Halle 118. https://szs.ch/wp-content/uploads/2021-02_03_5_d_Kopfbau_Halle_118.pdf
- `P_NO_KA13_FUTUREBUILT` — FutureBuilt, Kristian Augusts gate 13, Oslo. https://www.futurebuilt.no/forbildeprosjekter/kristian-augusts-gate-13-oslo
- `P_NO_KA13_REPORT` — Reuse and transformation, KA13 findings report, linked from FutureBuilt / Entra. https://www.entra.no/vare-eiendommer/alle-eiendommer/kristian-augusts-gate-13/_/attachment/inline/31ec37c5-5944-4338-a4db-826336969f42%3A8fd12a6e4418e59f3ffe7be9916e27b7e0239d8f/20230113_KA13_erfaringsrapport_engelsk.pdf
- `P_DK_THORAVEJ` — Thoravej 29 sustainability / reuse project pages. https://www.thoravej29.dk/en/sustainability
- `P_DK_PIHLMANN` — Pihlmann Architects, Thoravej 29. https://pihlmann.dk/project/thoravej-29
- `P_DK_RESOURCE_ROWS` — Resource Rows / Lendager / upcycling project communication; verify original LCA before ingestion. https://lendager.com/architecture/resource-rows/
- `P_UK_55GSS_ASBP` — ASBP, 55 Great Suffolk Street case study. https://asbp.org.uk/case-studies/55-great-suffolk-street
- `P_UK_55GSS_NLA` — New London Architecture, 55 Great Suffolk Street. https://www.nla.london/projects/55-great-suffolk-street
- `P_UK_BRENT_ASBP` — ASBP, Brent Cross Town Primary Substation case study. https://asbp.org.uk/case-studies/brent-cross-town-primary-substation
- `P_UK_BRENT_ARUP` — Arup, Brent Cross Town Primary Substation. https://www.arup.com/projects/brent-cross-town-primary-substation/
- `P_UK_TBC_WILLMOTT` — Willmott Dixon, Tower Bridge Court / TBC London project communication. https://www.willmottdixon.co.uk/projects/tbc-london
- `P_UK_TBC_NSC` — New Steel Construction, reused steel / Tower Bridge Court reporting. https://www.newsteelconstruction.com/wp/reuse-helps-tbc-london-cut-carbon/
- `P_DE_AWM_CONCULAR` — Concular / AWM Münster Circular Office material and CO₂ reporting. https://concular.de/projekt/awm-muenster/
- `P_DE_RECYCLINGHAUS_ZAB` — Zentrum für Architektur und Baukultur / Recyclinghaus Hannover references. https://www.zab-hannover.de/
- `P_NL_CCN_RECREATE` — ReCreate project / Circular Centre Netherlands references. https://recreate-project.eu/
- `P_NL_LAGEMAAT` — Lagemaat, Prinsenhof A deconstruction / reuse reporting. https://www.lagemaat-sloopwerken.nl/
- `P_NL_SUPERLOCAL` — SUPERLOCAL / Expogebouw project sources. https://www.superlocal.eu/
- `P_NL_BOSCHGAARD_SUPERUSE` — Superuse, Woongroep Boschgaard. https://www.superuse-studios.com/projectplus/woongroep-boschgaard/
- `P_FR_GRANDE_HALLE_FCRBE` — FCRBE / Construction21 / Ekopolis sources for Grande Halle de Colombelles. https://www.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/
- `P_FI_RECREATE_FINLAND` — ReCreate, Finland pilot. https://recreate-project.eu/project-pilots/finland/
- `P_FI_RECREATE_2026_MINIPILOT` — ReCreate, third Finnish mini-pilot. https://recreate-project.eu/2026/04/20/a-third-reuse-mini-pilot-implemented-in-finland/
- `P_EU_RECREATE_CORDIS` — CORDIS, ReCreate project objective and programme-level 93–98% energy/carbon reduction claim. https://cordis.europa.eu/project/id/958200
- `P_FI_RECREATE_CARBONATION` — ReCreate, service life, carbonation and carbon footprint discussion. https://recreate-project.eu/2025/01/15/reusing-precast-concrete-for-a-sustainable-future-evaluating-service-life-carbonation-and-carbon-footprint/

## Ingestion priority

1. **High confidence / add now with source-specific values:** 55 Great Suffolk Street, KA13, AWM Münster, Thoravej 29, K.118.
2. **Add with source-conflict or method-warning flags:** Brent Cross Town Primary Substation, TBC London / House of Fraser chain, Woongroep Boschgaard, Circular Centre Netherlands / Prinsenhof A.
3. **Energy-performance / trade-off nodes, not CO₂-saving edges:** Recyclinghaus Hannover, Verbiest / Karreveld, Grande Halle de Colombelles, SUPERLOCAL Expogebouw.
4. **No project-level energy / CO₂ relationship until new evidence is found:** Hastings Pier Visitor Centre, Plattenvereinigung Berlin, CRCLR House, Musée de Folklore Mouscron, Charles Malis, Liander / Alliander HQ, Big Dig House.

