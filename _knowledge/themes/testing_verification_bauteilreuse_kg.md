# Testing and Verification Methods for Reused Building Elements in a Reuse Knowledge Graph

## Scope

This note curates testing and verification methods relevant to **Bauteilreuse** for `PruefungNachweis` nodes in a reuse knowledge graph.

Existing nodes considered:

- `pr_zustandsbewertung`
- `pr_eignungspruefung_baulehm`
- `pr_abbrandbemessung`

Candidate missing node:

- `pr_zerstoerungsfreie_pruefung` / ZfP / NDT

Evidence marking:

- **BELEGT** = the cited project source directly documents a suitability check, test, or proof for that project or component group.
- **INFER** = the method is standards-required or reuse-relevant, but the cited project source does not explicitly name the method.

## Results table

| Testing method | Existing/proposed node ID | Material | Bauteiltyp | Requirement verified | Standards / legal regime | Project evidence | Source citation | Recommended graph action |
|---|---|---:|---|---|---|---|---|---|
| **Sichtprüfung / Zustandsbewertung** — visual inspection / condition assessment | Existing: `pr_zustandsbewertung` | all | reusable elements before dismantling; façade, doors/windows, steel, concrete, timber | condition, damage, deconstructability, obvious pollutant risk, marketability | reuse due diligence; building-control / structural-safety proof as input | **Juch-Areal**: all reuse elements were checked by specialists for suitability; steel hall, concrete mushroom columns, tunnel concrete slabs are documented. | UBA states elements should be checked in-situ before reuse and that visual inspection gives first pollutant indications; suspected polluted parts require investigation. Source: [Umweltbundesamt, Wiederverwertung von Bauteilen](https://www.umweltbundesamt.de/system/files/medien/378/publikationen/texte_93_2015_wiederverwertung_von_bauteilen_0.pdf). Juch source says all elements were checked by specialists for suitability. Source: [Stadt Zürich, Recyclingzentrum Juch-Areal](https://www.stadt-zuerich.ch/de/planen-und-bauen/projekte-und-ausschreibungen/hochbauvorhaben/planung-ausfuehrung/recyclingzentrum-juch-areal.html). | Keep existing node. Add **project-level `BELEGT`** edge for Juch-Areal to `pr_zustandsbewertung` / generic suitability check. For other projects without explicit inspection text, use Bauteilgruppe-level `INFER`. |
| **Zerstörungsfreie Prüfung / ZfP** — non-destructive testing / NDT | Proposed: `pr_zerstoerungsfreie_pruefung`; synonyms: `ZfP`, `NDT`, `NDE` | steel, concrete, timber, welds, coatings | beams, columns, slabs, welds, plates, façade panels | hidden defects, cracks, weld quality, residual thickness, concrete uniformity, material grade proxies | ISO 9712 for qualified NDT personnel; ISO 17635 for NDT of welds; EN 12504-2 for rebound hammer concrete testing; reuse protocols for structural steel | **No project-specific BELEGT found** in retrieved public sources for Holbein Gardens, CRCLR, People’s Pavilion, or Plattenpalast. Juch only says “Eignung geprüft,” not ZfP. | ISO 9712 covers NDT personnel and methods including ultrasonic, magnetic, penetrant, radiographic, thermographic, acoustic emission and others. Source: [ISO 9712](https://www.iso.org/standard/75614.html). ISO 17635 gives rules for choosing NDT methods for welds. Source: [ISO 17635 sample PDF](https://cdn.standards.iteh.ai/samples/85705/5e96c53f5b0f477ba63f64280a2c9814/ISO-17635-2025.pdf). SCI P427 requires NDT of every reclaimed structural steel member to determine material grade by hardness testing. Source: [SCI P427 Steel Reuse Protocol](https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf). | **Create node.** Link to Bauteilgruppen `Stahltragwerk`, `Stahltraeger`, `Schweissnaht`, `Betonfertigteil`, `Betonplatte`, `Holztragwerk` as **Bauteilgruppe-level `INFER`**. Do not assert project-level `BELEGT` unless a corpus document names ZfP/NDT. |
| **Zerstörende Prüfung** — destructive testing | Proposed: `pr_zerstoerende_pruefung` | steel, concrete, timber, clay/earth | coupons, cores, samples, small specimens | actual strength, chemical composition, density, compressive strength, bending strength | EN 12504-1 / EN 13791 for concrete; EN 408 / EN 14081 family for timber; SCI steel-reuse protocol where NDT is insufficient | **Villa Welpeloo** did not document destructive testing; engineers instead assumed lowest possible steel quality. | Villa Welpeloo source states exact steel specifications were unavailable, so engineers assumed the lowest possible steel quality. Source: [SE2050 Villa Welpeloo case study](https://se2050.org/wp-content/uploads/2024/07/SEI-CE-WG-Circular-Economy-Case-Studies_5-Villa-Welpeloo.pdf). EN 12504-1 specifies taking and testing cores from hardened concrete; EN 13791 is used to assess in-situ concrete strength in structures and precast components. Source: [EN 12504-1 description](https://www.en-standard.eu/csn-en-12504-1-testing-concrete-in-structures-part-1-cored-specimens-taking-examining-and-testing-in-compression/). | Add node as parent/category. Use **Bauteilgruppe-level `INFER`** for structural reuse where actual mechanical properties are unknown. For Villa, create a separate `konservative_bemessungsannahme` / “conservative design assumption” edge, not a testing edge. |
| **Materialprobe / Beprobung** — material sampling | Proposed: `pr_materialbeprobung` | all, especially pollutant-risk materials, concrete, steel, Baulehm | samples, coupons, cores, swabs | composition, contaminants, strength, suitability for reuse | TRGS 519/524 for hazardous substances; EN 12504-1 for concrete cores; DIN 18945–18947 for earth products | **UBA general evidence** strong; **project BELEGT** only if project has actual lab/sample report. | UBA says suspected pollutant-contaminated elements must be investigated and that sampling/testing can be necessary before dismantling. Source: [Umweltbundesamt, Wiederverwertung von Bauteilen](https://www.umweltbundesamt.de/system/files/medien/378/publikationen/texte_93_2015_wiederverwertung_von_bauteilen_0.pdf). TRGS 524 requires investigation and assessment of building materials in contaminated areas. Source: [TRGS 524 English PDF](https://sw6.asup.info/media/g0/b2/aa/1696405701/englisch%20TRGS524_DGUVR101004.pdf). | Create node and connect as superclass to pollutant, concrete-core, Baulehm and steel-coupon tests. Use **Bauteilgruppe-level `INFER`** unless project report names sampling. |
| **Festigkeitssortierung / Holzsortierung** — strength grading / timber grading | Proposed: `pr_festigkeitssortierung_holz`; alternative broader: `pr_holzsortierung` | timber | beams, joists, rafters, boards, CLT/glulam if reclaimed | strength class, stiffness, load-bearing capacity, reusability in structural role | EN 14081-1 for strength-graded structural timber; national visual grading standards; Eurocode 5 design | No named corpus project found with explicit timber grading. People’s Pavilion used wooden frames and Arup design, but the retrieved source does not document timber grading. | EN 14081-1 specifies requirements for visually or machine strength-graded structural timber. Source: [BS EN 14081-1 preview](https://webstore.ansi.org/preview-pages/BSI/preview_30401705.pdf). Platform CB’23 notes that construction timber is strength-graded under European/national standards and that reuse lacks a specific assessment guideline. Source: [Platform CB’23, Quality assessment and assurance when reusing products](https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment-and-assurance-when-reusing-products-from-existing-structures_June2023.pdf). People’s Pavilion source documents wooden frames and Arup involvement, but not grading. Source: [KOersief 106 PDF](https://www.slimbreker.nl/downloads/2018-07%20KOersief%20106.pdf). | Create timber-specific node. Link to `Holztraeger`, `Holzrahmen`, `Dachstuhl`, `Brettschichtholz` as **Bauteilgruppe-level `INFER`**. Project edge only if grading certificate/visual grading report exists. |
| **Brandschutznachweis / Feuerwiderstandsnachweis** — fire-resistance proof | Existing specific: `pr_abbrandbemessung`; proposed generic: `pr_brandschutznachweis` | timber, steel, concrete, façade products, recycled plastic products | structural timber, slabs/walls, façade cladding, fire compartments | R / REI / EI rating, residual load-bearing capacity in fire, combustibility | EN 1995-1-2 for timber fire design/charring; DIN 4102 / EN 13501-2 for fire-resistance classification; local building code fire safety | **CRCLR House** signal remains weak in public search: one hit mentions CRCLR location and “Abbrand berechnetes Material,” but not enough for BELEGT. **People’s Pavilion / Pretty Plastic**: permanent use required stricter fire-resistance compliance; temporary pavilion relied on exit-route safety coordination. | EN 1995-1-2 requires charring to be considered for wood surfaces exposed to fire. Source: [EN 1995-1-2 PDF](https://www.phd.eng.br/wp-content/uploads/2015/12/en.1995.1.2.2004.pdf). DIN 4102 fire-resistance classes use F30 etc. as minutes of function. Source: [CWS overview of fire-resistance classes](https://www.cws.com/en/fire-safety/news/fire-resistance-classes-of-components). People’s Pavilion / Pretty Plastic source says permanent buildings required strict fire-safety standards. Source: [Eindhoven Design District, Pretty Plastic](https://www.eindhovendesigndistrict.nl/en/projects/pretty-plastic). | Keep `pr_abbrandbemessung` for timber charring only. Add generic `pr_brandschutznachweis` for non-timber products. Mark CRCLR as **candidate / `INFER`**, not `BELEGT`, until corpus text explicitly confirms Abbrandbemessung. |
| **Schadstoffprüfung** — pollutant / hazardous-substance testing | Proposed: `pr_schadstoffpruefung` | timber, mineral fibre, sealants, coatings, insulation, concrete, metals | wood elements, façade, floors, sealants, pipe/duct insulation, coatings | absence or management of asbestos, KMF/MMMF, PCB, PAH, PCP/Lindan/DDT, heavy metals | GefStoffV; TRGS 519 for asbestos; TRGS 524 for contaminated areas; waste law / disposal classification | No named project-specific BELEGT found, but this is a high-priority reuse gate for older components. | UBA lists wood preservatives, asbestos, PCB, PAH and heavy metals as pollutant groups relevant before reuse, and says contaminated elements may not be reusable. Source: [Umweltbundesamt, Wiederverwertung von Bauteilen](https://www.umweltbundesamt.de/system/files/medien/378/publikationen/texte_93_2015_wiederverwertung_von_bauteilen_0.pdf). TRGS 519 covers asbestos in demolition, reconstruction, maintenance and waste disposal. Source: [BAuA TRGS 519 PDF](https://www.baua.de/EN/Service/Technical-rules/TRGS/pdf/TRGS-519.pdf?__blob=publicationFile&v=2). | Create node. Link to all pre-1990/high-risk Bauteilgruppen as **Bauteilgruppe-level `INFER`**. Project-level `BELEGT` only with pollutant survey, Schadstoffkataster or lab report. |
| **Feuchteprüfung** — moisture testing | Proposed: `pr_feuchtepruefung` | timber, Baulehm, insulation, masonry | timber beams/boards, earth blocks, rammed earth, reused insulation | moisture content, decay risk, suitability for installation/use class | EN 13183-1 oven-dry reference method; EN 13183-2 resistance method; EN 13183-3 capacitance method; DIN 68800 wood protection | No direct named project BELEGT found. | EN 13183 series covers oven-dry, electrical-resistance and capacitance moisture determination/estimation for sawn timber. Source: [BSI EN 13183 series landing page](https://landingpage.bsigroup.com/LandingPage/Series?UPI=BS+EN+13183). EN 13183-2 defines a non-destructive electrical-resistance method. Source: [EVS EN 13183-2](https://www.evs.ee/en/evs-en-13183-2-2002). DIN 68800 requires timber durability measures; a BFH source notes long-term timber moisture max. 20 mass% for load-bearing components under DIN 68800. Source: [BFH timber moisture PDF](https://www.bfh.ch/dam/jcr%3Ac5724abe-0fe0-4766-81d4-5218a4a5a828/13-ictb2021-koch.pdf). | Create node. Link to `Holzbauteil`, `Baulehm`, `Dämmstoff` as **Bauteilgruppe-level `INFER`**. |
| **Korrosionsprüfung / Restdickenmessung** — corrosion assessment / thickness testing | Proposed: `pr_korrosionspruefung` | steel, reinforced concrete, metal façade | steel beams/columns/plates, connections, coatings, rebar zones | residual section, corrosion loss, coating durability, service life | ISO 12944 for corrosion protection of steel structures; ultrasonic/manual measurements in existing steel assessment; Eurocode structural verification | **Juch-Areal** and **Villa Welpeloo** use reused steel, but sources do not name corrosion testing. | JRC guidance for existing steel structures lists reduction in plate thickness from corrosion as measured manually, ultrasonically or by destructive drilling. Source: [JRC guidance for existing steel structures](https://eurocodes.jrc.ec.europa.eu/sites/default/files/2021-12/EUR23252EN.pdf). ISO 12944 provides corrosion-protection rules for steel structures and coating systems. Source: [ifo overview of DIN EN ISO 12944](https://www.ifo-gmbh.de/en/standards/detail/din-en-iso-12944/). Villa Welpeloo documents reused steel girders but conservative design, not corrosion testing. Source: [SE2050 Villa Welpeloo case study](https://se2050.org/wp-content/uploads/2024/07/SEI-CE-WG-Circular-Economy-Case-Studies_5-Villa-Welpeloo.pdf). | Create node. Link to `Stahltragwerk`, `Stahlstuetze`, `Stahltraeger`, `Metallfassade` as **Bauteilgruppe-level `INFER`**. Project-level `BELEGT` requires inspection/NDT report. |
| **Beton-Bohrkernprüfung** — concrete core testing | Proposed: `pr_bohrkernpruefung_beton`; child of `pr_zerstoerende_pruefung` | concrete | precast slabs, columns, panels, in-situ concrete elements | compressive strength, density, carbonation/chloride if combined with lab tests | EN 12504-1; EN 13791; EN 12390 for compressive test procedures | **Juch-Areal** documents reused concrete mushroom columns and tunnel concrete slabs; suitability was checked, but core testing itself is not named. **Plattenpalast / Plattenvereinigung** relates to reused large precast concrete panels, but public search result only indicates document checking/prototype stage. | Juch source documents concrete mushroom columns and tunnel slabs and says all elements were checked by specialists. Source: [Stadt Zürich, Recyclingzentrum Juch-Areal](https://www.stadt-zuerich.ch/de/planen-und-bauen/projekte-und-ausschreibungen/hochbauvorhaben/planung-ausfuehrung/recyclingzentrum-juch-areal.html). EN 12504-1 covers taking, examining and compression testing cores; EN 13791 covers in-situ concrete strength in structures/precast components. Source: [EN 12504-1 description](https://www.en-standard.eu/csn-en-12504-1-testing-concrete-in-structures-part-1-cored-specimens-taking-examining-and-testing-in-compression/). Plattenvereinigung result mentions checking extensive documents, not core testing. Source: [Plattenvereinigung Abschlussbericht PDF](https://www.plattenvereinigung.de/wp-content/uploads/2023/03/plv_abschlussbericht_web_einzelseiten.pdf). | Create node. For Juch concrete elements, add **project-level `BELEGT` only to generic suitability check**, not to core testing. Add core testing as **Bauteilgruppe-level `INFER`** for reused structural concrete. |
| **Lehm-Eignungsprüfung** — earth/clay suitability testing | Existing: `pr_eignungspruefung_baulehm` | Baulehm, earth blocks, earth mortar, earth plaster | Lehmsteine, Lehmmauermörtel, Lehmputz, rammed earth | grain composition, shrinkage, compressive strength, density, abrasion, moisture sensitivity, application class | DIN 18940 for load-bearing earth-block masonry; DIN 18945 earth blocks; DIN 18946 earth masonry mortar; DIN 18947 earth plaster mortar; MVV TB / DIBt context | Publicly retrieved **Juch-Areal** source documents steel and concrete reuse, not Baulehm. **Villa Welpeloo** documents steel girders, cable-reel timber cladding, insulation, etc., not Baulehm. | Baunetz lists DIN 18940 and its reliance on DIN 18945/18946. Source: [Baunetz Wissen, Normen für den Lehmbau](https://www.baunetzwissen.de/gesund-bauen/fachwissen/regelwerke/normen-fuer-den-lehmbau-3393643). DIBt says DIN 18940 and product standards DIN 18945/18946 were being proposed for MVV TB inclusion. Source: [DIBt, Bauen mit Lehm](https://www.dibt.de/de/aktuelles/meldungen/nachricht-detail/meldung/bauen-mit-lehm). Villa Welpeloo material list does not show Baulehm. Source: [SE2050 Villa Welpeloo case study](https://se2050.org/wp-content/uploads/2024/07/SEI-CE-WG-Circular-Economy-Case-Studies_5-Villa-Welpeloo.pdf). | Keep existing node. Do **not** add Juch/Villa project-level `BELEGT` for Baulehm based on public evidence found. Keep as **Bauteilgruppe-level `INFER`** unless corpus documents clay/earth testing. |
| **Dokumentenprüfung / Herkunfts- und Bestandsnachweis** — document review / provenance verification | Proposed: `pr_dokumentenpruefung_bestand` | all, especially structural elements | steel, precast concrete, façade, windows, mechanical products | previous use, design loads, maintenance history, product data, declared performance, traceability | CPR / CE documentation where product placed on market; structural safety proof; reuse protocols | **Plattenvereinigung / Plattenpalast** search result mentions checking more extensive documents; **Villa Welpeloo** explicitly lacked exact steel specifications and used conservative assumptions. | UBA lists required existing documents such as plans, calculations, maintenance/use records, prior investigations and historical use before reuse. Source: [Umweltbundesamt, Wiederverwertung von Bauteilen](https://www.umweltbundesamt.de/system/files/medien/378/publikationen/texte_93_2015_wiederverwertung_von_bauteilen_0.pdf). Villa Welpeloo lacked exact steel specifications. Source: [SE2050 Villa Welpeloo case study](https://se2050.org/wp-content/uploads/2024/07/SEI-CE-WG-Circular-Economy-Case-Studies_5-Villa-Welpeloo.pdf). Plattenvereinigung result mentions “Prüfung von umfangreicheren Unterlagen.” Source: [Plattenvereinigung Abschlussbericht PDF](https://www.plattenvereinigung.de/wp-content/uploads/2023/03/plv_abschlussbericht_web_einzelseiten.pdf). | Add node. This is often the first verification step before testing. Use **project-level `BELEGT`** for Villa as “documentation gap / conservative assumption,” and for Plattenvereinigung only if the corpus source confirms the PDF context. |

## Strong KG actions

1. **Create `pr_zerstoerungsfreie_pruefung` as a missing node.**  
   It is distinct from `pr_zustandsbewertung`: visual condition assessment can trigger NDT, but ZfP is a formal test family with qualified personnel, equipment and acceptance criteria.

2. **Keep `pr_abbrandbemessung` narrowly scoped to timber fire design/charring.**  
   Add a broader `pr_brandschutznachweis` for fire-resistance classification of non-timber reused or recycled products.

3. **Treat project evidence conservatively.**  
   Based on the public evidence checked here, mark only these as **BELEGT**:
   - Juch-Areal → generic suitability/condition assessment.
   - Villa Welpeloo → documentation gap / conservative structural assumption.
   - People’s Pavilion / Pretty Plastic → fire-safety relevance for permanent application, but not necessarily a documented test for the temporary pavilion.

4. **Do not mark the following as project-level BELEGT without corpus documents that explicitly name them:**
   - ZfP / NDT
   - concrete core testing
   - pollutant testing
   - moisture testing
   - corrosion testing
   - Baulehm suitability testing

## Suggested node additions

```text
pr_zerstoerungsfreie_pruefung
pr_zerstoerende_pruefung
pr_materialbeprobung
pr_festigkeitssortierung_holz
pr_brandschutznachweis
pr_schadstoffpruefung
pr_feuchtepruefung
pr_korrosionspruefung
pr_bohrkernpruefung_beton
pr_dokumentenpruefung_bestand
```

## Suggested hierarchy

```text
pr_zustandsbewertung
  └─ may_trigger → pr_materialbeprobung
  └─ may_trigger → pr_zerstoerungsfreie_pruefung

pr_materialbeprobung
  ├─ pr_schadstoffpruefung
  ├─ pr_bohrkernpruefung_beton
  └─ pr_eignungspruefung_baulehm

pr_zerstoerende_pruefung
  ├─ pr_bohrkernpruefung_beton
  └─ material coupon / lab test variants

pr_zerstoerungsfreie_pruefung
  ├─ ultrasonic testing
  ├─ rebound hammer / sclerometer
  ├─ magnetic particle testing
  ├─ penetrant testing
  ├─ radiographic testing
  └─ thermographic testing

pr_brandschutznachweis
  └─ pr_abbrandbemessung
```

## Edge recommendation summary

| Project | Method edge | Evidence strength |
|---|---|---|
| Juch-Areal Recyclingzentrum Zürich | `pr_zustandsbewertung` / suitability check | **BELEGT** |
| Juch-Areal Recyclingzentrum Zürich | `pr_bohrkernpruefung_beton` | **INFER** |
| Juch-Areal Recyclingzentrum Zürich | `pr_korrosionspruefung` for reused steel | **INFER** |
| Villa Welpeloo Enschede | `pr_dokumentenpruefung_bestand` / missing provenance leading to conservative assumption | **BELEGT** |
| Villa Welpeloo Enschede | destructive testing / NDT of steel | **INFER** only; not documented in retrieved source |
| People’s Pavilion Eindhoven | `pr_brandschutznachweis` / fire-safety relevance | **INFER** for pavilion; stronger for permanent Pretty Plastic application |
| Plattenpalast / Plattenvereinigung Berlin | `pr_dokumentenpruefung_bestand` | **INFER** pending corpus confirmation |
| Plattenpalast / Plattenvereinigung Berlin | concrete core testing | **INFER** |
| CRCLR House / Impact Hub Berlin | `pr_abbrandbemessung` | **INFER** pending explicit corpus citation |
| Holbein Gardens London | ZfP / NDT | **INFER** only; no direct evidence found in retrieved public sources |
