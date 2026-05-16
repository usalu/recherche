# 1. Schadstoff / pollutant-screening research

You are researching a reuse knowledge graph about 76 circular construction / Bauteilreuse projects.

### Context
The graph has an underused label `Schadstoff`. Current or candidate pollutant nodes include:
- Existing: `s_asbest`, `s_bleifarbe`, `s_holzschutzmittel`, `s_pak`, `s_pcb`
- Proposed: `s_kmf`, `s_formaldehyd`, `s_schwermetalle`, `s_radon`

Known corpus countries include Germany, Belgium, UK, Netherlands, Switzerland, France, USA, Finland, Denmark, Norway, Japan, Luxembourg.
Important materials in the corpus: Stahl, Holz, Beton, Glas, Stahlbeton, Keramik, Ziegel, Naturstein, Dämmstoff, Aluminium, Kunststoff, Textil, Recyclingbeton, Gusseisen, Bitumen, MDF, Faserzement, Lehm, Stroh.

### Research task
For each pollutant above, identify:
1. Which reused building materials or Bauteiltypen typically carry this pollutant risk.
2. Which countries in the corpus have legal or technical requirements for testing this pollutant before reuse.
3. Which of the following projects likely need verification because of age/material risk:
   - Berlin Schildow Pilot House
   - Europa Building Brussels
   - Multi Brussels Reuse in MULTI
   - Recyclinghaus Hannover
   - Superlocal Expogebouw Bleijerheide
   - Plattenpalast Berlin
   - CRCLR House / Impact Hub Berlin
   - BedZED London Hackbridge
   - Big Dig Building Boston
   - Hastings Pier Visitor Centre
   - BioPartner 5 Leiden
4. Distinguish between:
   - BELEGT: directly documented in a project source
   - INFER: general reuse-domain knowledge only
   - RESEARCH: still needs project-source confirmation

### Output format
Create a table with columns:
Pollutant ID, Pollutant name, Risk materials, Risk period, Relevant countries, Project candidates, Evidence found, Source citation, Recommended graph action.

### Important
Do not recommend adding a graph edge unless the pollutant is explicitly documented for that project or Bauteilgruppe.

# 2. Norms / standards by country and material

You are researching missing and underused `Norm` nodes in a circular construction reuse knowledge graph.

### Context
The corpus contains 76 reuse projects across these main countries:
- Germany: 11 projects
- Belgium: 11
- UK: 9
- Netherlands: 9
- Switzerland: 6
- France: 5
- USA: 4
- Finland and Denmark: 3 each
- Norway, Japan, Luxembourg: 1 each

Important reused materials:
Stahl, Holz, Beton, Glas, Stahlbeton, Keramik, Ziegel, Naturstein, Dämmstoff, Aluminium, Kunststoff, Textil, Recyclingbeton, Gusseisen, Bitumen, MDF, Faserzement, Lehm, Stroh.

### Existing norm nodes include
- `norm_sci_p427`
- `norm_sci_p440`
- `norm_tek_norway`
- `norm_ns_3682`
- `norm_sia_schweiz`
- `norm_crow_cur_4_2023`
- `norm_en_1090`
- `norm_en_1168`
- `norm_historic_sections_book`
- `norm_rt_2012`
- `norm_din_18940`
- `norm_din_en_15804`
- `norm_din_en_15978`
- `norm_iso_14040`
- `norm_iso_14044`
- `norm_iso_20887`

### Candidate missing norm nodes
- `norm_en_206` for concrete
- `norm_eurocode_generic`, preferably split into EN 1992, EN 1993, EN 1995
- `norm_nen_8700` or other Dutch NEN existing-structure standards
- `norm_bs_en_generic`

### Research task
For each country × material pairing, identify the most relevant standards for reuse or requalification of:
1. structural steel
2. structural timber
3. concrete / reinforced concrete / hollow-core slabs
4. façade glass / aluminium
5. natural stone / brick / masonry
6. insulation and mineral wool

### Pay special attention to
- UK reused structural steel: SCI P427 / SCI P440 / UKCA / EN 1090
- Netherlands and Finland/Norway hollow-core slab reuse: CROW-CUR, NS 3682, EN 1168, NEN standards
- Switzerland: SIA standards relevant to reuse
- Germany: DIN / DIN EN standards for reused concrete, steel, and timber
- Belgium and France: any reuse-specific protocols or standards

### Output format
Return a table:
Country, Material, Relevant standard, Standard body, Applies to reuse directly or indirectly, Project examples from corpus, Evidence strength, Source citation, Recommended graph action.

### Important
Mark whether each norm is:
- project-specific BELEGT
- country/material inference only
- unsuitable for graph edge but useful as metadata.

# 3. Rechtliche Bedingungen / legal regimes

You are researching legal and regulatory conditions affecting Bauteilreuse projects in a reuse knowledge graph.

### Context
The graph has the label `RechtlicheBedingung`. Existing nodes include:
- `rb_bauordnungsrecht`
- `rb_ce_ukca_marking_reused_steel`
- `rb_zulassung_im_einzelfall`
- `rb_boulder_deconstruction_ordinance_8366`
- `rb_grade_ii_listing`
- `rb_vergaberecht`
- `rb_eu_taxonomie`
- `rb_gewaehrleistung`
- `rb_produkthaftung`

### Candidate missing nodes
- `rb_denkmalschutz`
- `rb_materialpass`
- `rb_bauproduktenverordnung_cpr`
- `rb_kreislaufwirtschaftsgesetz_krwg`
- `rb_dibt_zustimmung`

### Corpus countries
Germany, Belgium, UK, Netherlands, Switzerland, France, USA, Finland, Denmark, Norway, Japan, Luxembourg.

### Research task
For each country, identify the main legal regimes affecting reuse of structural building elements, grouped by:
1. Building approval / Bauordnungsrecht
2. One-off approval / Zustimmung im Einzelfall / equivalent national route
3. Construction Products Regulation / CE / UKCA / product status
4. Warranty and liability
5. Public procurement
6. Heritage protection / Denkmalschutz
7. Waste law vs product status
8. Material passport / circularity reporting obligations

### Focus especially on
- Germany: MBO, ZiE/vBG, DIBt, KrWG, CPR
- UK: UKCA, CE legacy, Grade II / heritage, reused steel
- Belgium: Brussels-Capital, Wallonia, Flanders reuse programmes
- Netherlands: Madaster/material passport, NEN, circular procurement
- Switzerland: SIA, cantonal building approval, BAFU if relevant
- France: RE2020 / procurement / reuse law
- USA: Boulder Deconstruction Ordinance 8366

### Output format
Table columns:
Country, Legal regime, Applies to which material/Bauteiltyp, Relevant project candidates, Evidence source, Is this graph node existing or proposed, Recommended graph action.

### Important
Only recommend project-level graph relationships when a source connects the legal condition to a specific project.
Otherwise mark as country-level metadata.


# 4. Leistungsanforderungen / performance requirements

You are researching performance requirements for reused construction elements in a circular construction knowledge graph.

### Context
The graph has label `Leistungsanforderung`. Existing nodes include:
- `la_dauerhaftigkeit`
- `la_tragfaehigkeit`
- `la_brandschutz`
- `la_feuchteschutz`
- `la_waermeschutz`
- `la_schallschutz`
- `la_rueckbaubarkeit`
- `la_schadstofffreiheit`
- `la_feuerwiderstand`
- `la_f90`
- `la_r90`
- `la_rei90`

The current graph heavily uses Dauerhaftigkeit, Tragfähigkeit, Brandschutz, Feuchteschutz, Wärmeschutz, and Schallschutz. It likely under-tags Rückbaubarkeit and Schadstofffreiheit. Fire-resistance class nodes F90, R90, REI90 are currently unused.

### Research task
For each common reused Bauteiltyp, identify mandatory or typical Leistungsanforderungen by country:
- reused steel beams
- reused timber beams / timber panels
- reused concrete slabs / hollow-core slabs
- reused façade elements / windows / glass
- reused brick / stone / masonry
- reused insulation
- reused interior fit-out elements

### Countries to cover
Germany, Switzerland, Netherlands, Belgium, UK, France, Norway, Finland, Denmark.

### Questions to answer
1. Which performance requirements are legally mandatory?
2. Which are commonly required by standards or engineering practice?
3. Which requirements are reuse-specific?
4. How are fire resistance classes such as F90, R90, REI90 documented or proven?
5. Should F90/R90/REI90 be modeled as child nodes of Brandschutz or as separate graph nodes?

### Output format
Table:
Bauteiltyp, Country, Required performance, Related graph node, Relevant standard/legal basis, Evidence source, Project examples, Recommended graph action.

### Important
Separate general code requirements from project-specific documented requirements.
Do not recommend a graph edge unless the requirement is documented for a project or Bauteilgruppe.

# 5. Verbindungstechnik / connection techniques and reversibility

You are researching connection techniques in a Bauteilreuse knowledge graph.

### Context
Existing `Verbindungstechnik` nodes include:
- `vt_verschraubung`
- `vt_reversible_fuegung`
- `vt_verschweissung`
- `vt_vermoertelung`
- `vt_klemmverbindung`
- `vt_mauerwerk_ausgleich`
- `vt_steckverbindung`
- `vt_verleimung`

### Candidate missing nodes
- `vt_holzduebel`
- `vt_nagelung`

### Known issue
`vt_verschraubung` and `vt_reversible_fuegung` overlap. The graph may need a parent-child relationship where Verschraubung, Klemmverbindung, Steckverbindung, and Holzdübel are subtypes of reversible joining.

### Projects of interest
- CascadeUp London secondary timber / glulam demonstrator
- Plattenpalast Berlin
- Recyclinghaus Hannover
- timber-reuse projects across Germany, Switzerland, Netherlands, Belgium, UK, Denmark

### Research task
Catalogue the connection technique used in timber, steel, masonry, and façade reuse cases.

For each project/Bauteilgruppe found:
1. Identify the joining method.
2. Determine whether it is reversible, partially reversible, or irreversible.
3. Identify whether the method supports future reuse.
4. Identify if special processing is needed to separate or clean the component.
5. Recommend whether the graph should add a relationship to an existing node or create a new Verbindungstechnik node.

### Output format
Project, Bauteilgruppe/Bauteiltyp, Material, Connection technique, Reversibility level, Evidence quote, Source citation, Existing/proposed graph node, Recommended graph action.

### Important
Do not infer connection technique from material alone. Require source evidence.

# 6. Aufbereitungsverfahren / processing and reconditioning

You are researching `Aufbereitungsverfahren` for reused building elements in a circular construction graph.

### Context
The graph already has several processing/reconditioning nodes, but the knowledge map identifies gaps:
- Existing gap: `av_drahtglasschneiden` has no relationships
- Proposed missing node: `av_sandstrahlen` / sandblasting, especially for reused steel corrosion protection
- Related processes likely include cleaning, de-nailing, planing, cutting, testing, coating removal, corrosion treatment, pressure testing, dimensional adaptation, and material sorting.

### Known project signal
- BedZED London Hackbridge may document sandblasting / corrosion treatment for reused steel.
- “Korrosionsschutz” appears in multiple project files and may point to steel reconditioning.
- Drahtglasschneiden should be checked for projects reusing wired glass.

### Research task
For each major material group, identify typical and documented Aufbereitungsverfahren:
1. Stahl
2. Holz
3. Beton / Stahlbeton / hollow-core slabs
4. Glas / Drahtglas
5. Ziegel / Naturstein / Mauerwerk
6. Dämmstoff / Mineralwolle
7. Aluminium
8. Lehm / Stroh / bio-based materials

For each process:
- Define the process
- Identify which material/Bauteiltyp it applies to
- Identify whether it is documented in corpus projects
- Identify whether it should become a new graph node
- Identify likely Leistungsanforderung or PrüfungNachweis links

### Output format
Process name, Proposed ID, Material, Bauteiltyp, Project evidence, General reuse relevance, Source citation, Recommended graph action.

### Important
Separate documented project evidence from general best practice.

# 7. PrüfungNachweis / testing and verification

You are researching testing and verification methods for reused building elements in a reuse knowledge graph.

### Context
Existing `PruefungNachweis` nodes include:
- `pr_zustandsbewertung`
- `pr_eignungspruefung_baulehm`
- `pr_abbrandbemessung`

Candidate missing node:
- `pr_zerstoerungsfreie_pruefung` / ZfP / NDT

### Known project signals
- Holbein Gardens London
- CRCLR House / Impact Hub Berlin
- People’s Pavilion Eindhoven
- Plattenpalast Berlin
may mention non-destructive testing or reuse-relevant verification.
- Juch-Areal Recyclingzentrum Zürich and Villa Welpeloo Enschede may mention Baulehm suitability testing.
- CRCLR House may mention Abbrandbemessung.

### Research task
For each testing/verification method relevant to Bauteilreuse, identify:
1. Name of method in German and English
2. Applicable material/Bauteiltyp
3. What performance requirement it verifies
4. Which standards or legal regimes require it
5. Which corpus projects document it
6. Whether it supports a graph relationship at project or Bauteilgruppe level

### Include methods such as
- visual inspection / Zustandsbewertung
- destructive testing
- non-destructive testing / NDT / ZfP
- material sampling
- strength grading
- fire-resistance proof
- pollutant testing
- moisture testing
- corrosion testing
- concrete core testing
- timber grading
- Lehm suitability testing

### Output format
Testing method, Existing/proposed node ID, Material, Bauteiltyp, Requirement verified, Project evidence, Source citation, Recommended graph action.

### Important
Mark whether evidence is strong enough for `BELEGT` or only general `INFER`.


# 8. Country × material research matrix
You are researching a country × material gap matrix for a circular construction reuse knowledge graph.

### Context
The corpus contains these country/project counts:
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

### Top materials by country
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

### Research task
For every country × top-material pairing, identify the most important missing graph knowledge:
1. Applicable Norms
2. Legal conditions
3. Required Prüfungen/Nachweise
4. Common Schadstoff risks
5. Common Aufbereitungsverfahren
6. Reuse-specific connection techniques
7. Performance requirements

### Output format
Country, Material, Project cluster, Missing Norms, Missing legal conditions, Missing tests, Missing pollutant checks, Missing processing methods, Priority level, Research sources, Suggested graph action.

### Important
Prioritize high-frequency combinations first:
- UK × Stahl
- Belgium × Stahl/Beton/Holz/Naturstein
- Germany × Holz/Beton/Stahl
- Netherlands × Holz/Stahl/Beton
- Switzerland × Stahl/Beton/Holz/Naturstein
- Finland/Norway × Beton hollow-core slabs

### Final output
Rank the top 20 graph gaps by expected value.

# 9. Deterministic graph patch validation

You are validating a proposed graph patch for a circular construction / Bauteilreuse knowledge graph.

### Context
The current proposal contains deterministic additions from archive evidence.

### Proposed add_rel operations
1. Add `HAT_SCHADSTOFF`: Berlin Schildow Pilot House → `s_asbest`
2. Add `HAT_SCHADSTOFF`: Europa Building Brussels → `s_asbest`
3. Add `HAT_SCHADSTOFF`: Multi Brussels Reuse in MULTI → `s_asbest`
4. Add `HAT_SCHADSTOFF`: Superlocal Expogebouw Bleijerheide → `s_asbest`
5. Add `HAT_RECHTLICHE_BEDINGUNG`: Recypark Demets Anderlecht → `rb_vergaberecht`
6. Add `HAT_RECHTLICHE_BEDINGUNG`: Zinneke Feder Masui4ever Brussels → `rb_vergaberecht`
7. Add `HAT_RECHTLICHE_BEDINGUNG`: 55 Great Suffolk Street London → `rb_ce_ukca_marking_reused_steel`
8. Add `HAT_RECHTLICHE_BEDINGUNG`: Hastings Pier Visitor Centre → `rb_grade_ii_listing`
9. Add `HAT_VERBINDUNGSTECHNIK`: CascadeUp London secondary timber/glulam demonstrator → `vt_verleimung`

### Proposed new nodes
- `s_kmf`
- `rb_denkmalschutz`
- `rb_materialpass`
- `norm_en_206`
- `vt_holzduebel`
- `av_sandstrahlen`
- `pr_zerstoerungsfreie_pruefung`

### Research task
Validate every proposed operation against primary or reliable secondary sources.

For each proposed operation:
1. Confirm whether the evidence exists.
2. Identify whether evidence is project-level or Bauteilgruppe-level.
3. Check whether the relationship type is semantically correct.
4. Check whether a broader or more specific node would be better.
5. Mark status:
   - APPROVE
   - APPROVE WITH CAVEAT
   - NEEDS BG-LEVEL SOURCE
   - REJECT
6. Provide a short explanation and citation.

### Output format
Operation, Evidence found, Evidence level, Semantic fit, Risk/caveat, Status, Source citation.

### Important
Do not assume that project-level pollutant evidence applies to every Bauteilgruppe.
Do not approve KMF unless the insulation age or risk category is clear enough.

# 10. Stub projects, material passports, and final coverage audit

You are completing a final research coverage audit for a circular construction reuse knowledge graph.

### Context
The knowledge map identifies open work on:
1. Materialpass / digital material passport / Madaster / Concular / digital twin evidence
2. Stub project nodes that need promote-or-drop decisions
3. Actor nodes with ambiguous or missing project evidence

### Materialpass candidate projects include
- 55 Great Suffolk Street
- Jeugdkliniek Ithaka
- Liander HQ Duiven
- Multi Brussels
- PLP London HQ
- additional projects where Madaster, Concular, digital twin, or material passport is mentioned

### Stub project promote candidates
- LYSP8 Basel
- Stuttgart 210
- UMAR Unit
- Circle House
- Reallabor B(e) Ware
- Schärenmoosstrasse Zürich
- ELEMENTA Walkeweg
- MedUni Mariannengasse
- OBK 27
- Pavilion Circl Amsterdam
- RE-USE Höfe
- Circl / ABN AMRO
- Granby Workshop
- Vandkunsten component reuse

### Stub project drop candidates
- ZHAW research
- Architecture of Reuse Brussels
- Careno Be.Circular
- ETH student reuse
- FCRBE
- REFAIR Bordeaux platform
- Interreg NWE FCRBE
- RCMI Concular
- REBRIDGE
- Reuse Logistics

### Ambiguous actor nodes
- `zirkular_cirkla`
- `zrs_architekten`

### Registry-only actor nodes needing evidence or acceptance
bizh, citydev_brussels, dare_gmbh, denkstatt, edith_maryon_stift, eitel_partner, gibbins_architekten, glasfischer_glastec, heinrich_boell_stiftung, koimo_development, kunst_stoffe_ev, mehr_als_wohnen, rotor_vzw, stiftung_habitat, zusammenkunft_berlin.

### Research task
For each item:
1. Determine whether a primary source or reliable case study exists.
2. Summarize the reuse strategy.
3. Identify donor sources, reused materials, Bauteiltypen, and any Schadstoff findings.
4. Identify norms, legal conditions, testing methods, and material passport evidence.
5. Recommend whether the item should be:
   - promoted to full Projekt node
   - kept as stub
   - dropped
   - modeled as Akteur, Tool, Programm, or Forschung instead of Projekt

### Output format
Item name, Type, Evidence found, Reuse strategy, Materials/Bauteiltypen, Actors, Legal/norm/testing evidence, Materialpass evidence, Recommendation, Source citation.

### Final deliverable
Produce a prioritized list of graph updates that would close the biggest remaining gaps.

# 11. Wirtschaft / cost, market, procurement, business case

You are researching the economic dimension of a circular construction / Bauteilreuse knowledge graph.

### Context
The graph covers reuse of building components across multiple construction projects, countries, materials, and Bauteiltypen. Existing research tracks cover pollutants, norms, legal conditions, testing, performance requirements, connection techniques, and processing methods. Missing track: Wirtschaft / economic feasibility.

### Research task
Investigate the economic factors that determine whether reused building components are actually viable.

Cover these dimensions:
1. Cost comparison between reused and new components
2. Labour cost for dismantling, sorting, cleaning, testing, transport, storage, and reinstallation
3. Savings from avoided disposal, avoided landfill, avoided new material purchase, or avoided CO₂ costs
4. Market availability and supply-chain reliability of reused Bauteile
5. Storage and logistics costs
6. Risk premiums, insurance, warranty, liability, and contingency costs
7. Public procurement effects: whether reuse was enabled or blocked by tendering rules
8. Business models: component marketplace, reuse consultant, material broker, donor-building inventory, take-back system, leasing, urban mining platform
9. Funding, subsidies, grants, or pilot-programme support
10. Whether the project reports a measurable economic outcome

### Countries to cover
Germany, Switzerland, Netherlands, Belgium, UK, France, Denmark, Finland, Norway, USA.

### Materials/Bauteiltypen to prioritise
Structural steel, structural timber, concrete slabs, façade elements, windows, brick, natural stone, insulation, interior fit-out, MEP components.

### Output format
Create a table with:
Country, Project or project type, Material/Bauteiltyp, Economic factor, Cost driver or saving, Quantitative value if available, Evidence source, Graph node recommendation, Recommended relationship.

### Suggested graph concepts to look for
- Wirtschaftlichkeit
- Kosteneinsparung
- Mehrkosten
- Rückbaukosten
- Lagerkosten
- Transportkosten
- Prüfkosten
- Aufbereitungskosten
- Entsorgungskosten
- CO₂-Kosten
- Wiederverkaufswert
- Restwert
- Materialbörse
- Geschäftsmodell
- Förderprogramm
- Vergabemodell

### Important
Separate documented project evidence from general economic assumptions.
Only recommend a project-level graph edge if a source explicitly discusses economic effects for that project.

# 12. Energie / embodied energy, operational energy, CO₂, LCA

You are researching the energy and climate dimension of a circular construction / Bauteilreuse knowledge graph.

### Context
The graph covers circular construction and reuse of building components. Existing research covers pollutants, norms, legal issues, testing, performance requirements, connection techniques, and processing. Missing track: Energie / energy and climate impact.

### Research task
Investigate how reused construction components affect energy demand, embodied carbon, operational energy, and life-cycle assessment.

Cover these dimensions:
1. Embodied energy saved by reusing components instead of producing new ones
2. Embodied carbon / Global Warming Potential saved through reuse
3. Operational energy effects, especially when old reused components perform worse or better thermally
4. Trade-offs between reuse and energy-efficiency upgrades
5. Transport energy and logistics emissions
6. Energy used in processing, cleaning, cutting, testing, coating, or remanufacturing reused elements
7. LCA methods used: DIN EN 15804, EN 15978, ISO 14040, ISO 14044, building LCA tools, EPDs
8. Whether reused elements were counted as zero-impact, avoided impact, residual impact, or allocated impact
9. Whether the project reports quantitative CO₂, energy, or LCA results
10. Whether energy performance requirements influenced the ability to reuse components

### Materials/Bauteiltypen to prioritise
Steel, concrete, timber, aluminium, glass, brick, natural stone, insulation, façade elements, windows, structural elements, interior fit-out.

### Countries to cover
Germany, Switzerland, Netherlands, Belgium, UK, France, Denmark, Finland, Norway, USA.

### Output format
Create a table with:
Project, Country, Material/Bauteiltyp, Energy or CO₂ topic, Quantitative result if available, LCA method or standard, Boundary condition, Trade-off identified, Evidence source, Recommended graph action.

### Suggested graph concepts to look for
- Graue Energie
- Primärenergie
- Embodied Energy
- Embodied Carbon
- CO₂-Einsparung
- GWP
- LCA
- EPD
- Rückbauenergie
- Transportenergie
- Aufbereitungsenergie
- Betriebsenergie
- Wärmeschutz
- Energieeffizienz
- Reuse-vs-retrofit trade-off

### Important
Do not treat reuse as automatically energy-positive. Check whether the source accounts for transport, processing, testing, storage, and replacement performance.
Only recommend a project-level graph relationship if a project source gives explicit energy, CO₂, or LCA evidence.