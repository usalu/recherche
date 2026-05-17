# Research dossier workflow — 23 missing case studies

Twenty-three building-reuse case studies are referenced in our archive but have no dedicated research dossier yet. This folder contains seven batched prompts (≤ 5 projects each, grouped by category) that you can hand to an external research assistant (ChatGPT, Perplexity, a research intern) to fill the gap.

Every batch document follows the same workflow and asks for the same kinds of information — only the per-project focus differs.

## What every research dossier must contain

For each project, produce **one structured markdown file** that covers as many of the categories below as the public record allows. Categories that genuinely cannot be sourced are marked **"unknown"** rather than fabricated.

**Every factual statement must cite at least one source** — see "Source discipline" below.

### Identification
- Canonical project name + any alternate names / abbreviations
- Country, city / district, street address if known
- Latitude/longitude or a Plus Code if available
- Building owner / client (Bauherr / Auftraggeber)
- Project status: built, under construction, in planning, study only, paused, cancelled
- Time line: design start, construction start, completion, opening, decommissioning if applicable

### Buildings involved
- Each *receiver* building (the one being constructed / converted)
- Each *donor* building (where reused parts came from), if applicable
- For each building: type / use class (housing, education, office, industry, infrastructure, public, etc.), construction era, original use, current use, gross floor area, number of stories
- Whether the receiver is new construction, refurbishment, extension, adaptive reuse, or temporary

### People and organizations involved
For each, give name, role on this project, organization they belong to, and country base. Roles to specifically probe for:
- Architecture / design
- Structural engineering
- Building services (HVAC / electrical)
- Façade specialists
- Fire protection / accessibility
- Sustainability / LCA consultants
- Reuse / refurbishment specialists
- Demolition / deconstruction contractor
- Construction contractor
- Public-sector approvers / regulators involved
- Research or academic partners
- Material brokers / platforms used (Madaster, Concular, Restado, Opalis, Rotor DC, Salvo, etc.)
- Funders / grant-program operators
- Tenants / end users where relevant

### Reused / repurposed components
For each distinct group of reused components (e.g. "steel I-beams from teardown X", "WBS70 concrete panels", "bricks from Carlsberg site"):
- What is the component (concrete name, e.g. "Stahlträger HEB-200", "Fenster Holz/Alu", "Granit-Trittstufen")
- What material (steel, timber, concrete, brick, glass, stone, aluminium, plastic, composite, …)
- Component type / function (beam, column, slab, wall, façade panel, window, door, roof element, stair, foundation, finishes …)
- Where they came from — donor building, demolition site, salvage yard, broker, in-situ teardown
- Original use vs. new use (same role? downgraded role? changed function entirely?)
- Quantity / scope: number of pieces, mass in tons, volume in m³, area in m², linear meters
- Age at time of reuse
- Transport distance donor → site if known
- Whether they count as direct reuse or refurbished reuse
- Whether they are structural, envelope, spatial, technical, or finish

### Processing of reused components
For each component group, list the processing it underwent between teardown and reinstallation:
- Demolition method (selective deconstruction, mechanical demolition, careful dismantling)
- On-site or off-site refurbishment (cleaning, cutting, planing, sandblasting, recoating, welding, ...)
- Quality testing / non-destructive testing performed (visual inspection, ultrasonic, magnetic-particle, load testing, material sampling, ...)
- Storage between teardown and reinstall (where, for how long, conditions)
- Logistics (truck, rail, ship, container; packaging method)
- Joining technique used in reinstallation (welding, bolting, gluing, mortaring, dry-stacking, mechanical fastening)
- Whether the reinstall preserves design-for-disassembly

### Quality, defects, performance
- Condition assessment of the reused components: like-new, traces of use, requires rework, downgraded use class, not reusable
- Specific defects observed: corrosion, cracking, deformation, carbonation (concrete), biological attack (wood/straw/clay), delamination, surface defects, fire damage, chemical contamination (salt, acid, oil), or **explicit statement of "no relevant defects"**
- Pollutants screened for (asbestos, PCB, PAH, lead paint, formaldehyde, heavy metals, biocides, …) and the results
- Performance requirements the reused components had to meet (load-bearing, fire rating, acoustic, thermal, airtightness, durability, slip-resistance, …)
- Performance verification path (project-specific approval, type approval, declaration of performance, third-party expert opinion, …)
- Did anything fail and require swap-out?

### Standards, norms, regulatory regime
- Country-specific norms cited (e.g. SIA 269, DIN 4074, EN 1992, EN 1993, NEN 8700, CEN/TS 1090-201, EN 12504, BS 8500, …)
- Construction-product regulatory status of the reused components: CE marking, UKCA, project-specific approval (German ZiE / vBG, Swiss BAB, Belgian Tracimat traceability certificate, Dutch PEMD declaration, French Réemploi/REP declaration, US ICC-ES, …)
- Building permits / planning hurdles encountered
- Country-specific pollutant bans relevant to the donor era (e.g. asbestos was banned in Germany 1993, Netherlands 1994, France 1997, UK 2000 — components from before the ban need screening)

### Quantitative outcomes
- Reuse rate by mass (%) and by volume (%) — both are often reported and differ markedly
- Embodied-carbon savings vs. a hypothetical new-build reference (tons CO₂e, %)
- Material savings (tons of virgin material avoided)
- Cost: total construction cost (€ or local currency, ex/inc VAT), cost per m², cost premium or discount vs. new-build reference
- Funding sources: grants, subsidies, research-program funding, naming sponsors
- Hidden costs explicitly mentioned: storage, testing, refurbishment labor hours, reuse-coordination role

### Strategy and economics
- Where this project sits in the reuse spectrum: same-site reuse, in-situ reuse, off-site direct reuse, brokered second-hand purchase, donation, platform-mediated purchase, take-back agreement, intra-corporate transfer, research-program allocation
- Economic model: cost-neutral vs. premium; how the premium is justified (LCA, marketing, subsidy); presence of a separately budgeted reuse-coordination role
- Acceptance signals: sustainability certification (DGNB, BREEAM, LEED, Minergie, HQE), public-client pilot framework, insurer acceptance, end-user / aesthetic acceptance of visible patina

### Process and design approach
- Whether the design follows availability ("form follows availability") vs. specifies parts first
- Methods cited (component-catalog approach, urban mining, pre-deconstruction audit, material passport, reuse tendering, design-for-disassembly, ...)
- Software / tools used (Madaster, Concular, Restado, BIM tools, material-passport platforms, custom databases, ...)
- Lifecycle-assessment scope reported (EN 15978 modules A1–A5 only? A–C? cradle-to-grave?)

### Donor-receiver matching characteristics
- Time-axis matching: did donor and receiver align in time, or was material stockpiled (interim storage), or forward-reserved years ahead?
- Geographic matching: same site, local (< 50 km), regional (50–500 km), international, intercontinental
- Specification matching: exact 1:1 reuse, adjusted (cut/drilled/refurbished), or repurposed (changed function entirely)

### Hurdles and lessons learned
- Technical hurdles (structural certification, tolerances, condition uncertainty, …)
- Economic hurdles (extra labor, testing cost, schedule risk, …)
- Legal / regulatory hurdles (no clear approval path, liability, warranty, …)
- Logistical hurdles (transport distance, storage need, just-in-time challenges, …)
- Organizational hurdles (new coordination roles, knowledge gaps, …)
- Specific lessons named by the project team for future projects

## Source discipline (Quelle)

**Every claim must have at least one cited source.** Use a numbered bracket system inside the dossier:

```
- The project was completed in 2021 [S1], [S3].
- 41 % reuse rate by volume [S6].
- Bauherr was Stiftung Abendrot [S1], [S5].
- Norm cited but exact number not publicly disclosed [unklar].
```

At the end of the dossier, list every source with full citation:

```
## Sources
- [S1] baubüro in situ: K.118 Kopfbau Halle 118 — project page. https://www.insitu.ch/... (accessed 2026-05-17)
- [S2] Hochparterre, 06/2021: "K.118 — die zweite Halle in der Halle"
- [S3] Eva Stricker et al., ZHAW Reuse Compendium, 2022, pp. 88–105
- [S4] Arch2O.com, 2021-08-12: "K.118 Halle 118 by baubüro in situ"
- [S5] ETH/ZHAW Joint Reuse-Research Initiative, 2022 annual report
- [S6] EGGA case study, 2021, sustainability summary
- [S7] ArchDaily, 2021: "Halle 118"
- [S8] Detail, 11/2021, p. 1042–1051
```

Source kinds to prefer (in order):
1. Official project / firm pages
2. Peer-reviewed publications and research reports
3. Reputable trade press (Hochparterre, Detail, ArchDaily, espazium, dezeen, Architectural Record)
4. Government / regulator publications
5. Conference papers and theses
6. General press as supporting evidence only

Do not invent sources or paraphrase Wikipedia without finding the underlying citation. Mark "no source found" rather than guess.

## Categories most likely to be under-documented (probe explicitly)

Public reuse case studies generally do well on identification, actors, materials, and headline carbon numbers. They tend to be weak on:

- **Defect-screening evidence** — most cases say "tested" without naming the method
- **Country-specific regulatory product-status path** (Tracimat / PEMD / ZiE / project-specific approval) — usually only mentioned in technical reports
- **Hidden costs** — the reuse-coordination role, storage, and testing costs are real but often glossed
- **Donor-receiver matching** — temporal storage and geographic distance are often qualitative, ask for specifics
- **End-user / aesthetic acceptance** — usually only in critic / press articles
- **Concrete norm numbers** — projects often say "to current standards" without naming the norm

Push for specifics in these categories during research, and explicitly mark "unknown" if nothing is found.

## What we already know per project

Each batch document below lists the project's currently-known name and a list of people / organizations that we've already linked to it via the actor registry. **Do not re-discover these** — use them as anchors to find related sources, and add new names with their roles.

## Reference example

The single best concrete example of the depth and structure we want is the **K.118 / Kopfbau Halle 118, Winterthur** dossier:
- Path: [`_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`](../../../../_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md)
- Sections in K.118 worth copying as a structure: 1 EINORDNUNG, 2 ENTITÄTEN-MAPPING, 3 FALLSTUDIE, 4 REUSE-STRATEGIE, 5 BAUTEIL-INVENTAR, 6 PROZESS UND LOGISTIK, 7 TECHNIK / LEISTUNG / NORMEN, 8 KENNWERTE, 9 HÜRDEN, 10 WIRTSCHAFT, 11 LESSONS LEARNED, plus the Sources list at the end.

## Output

For each project, deliver one file:

```
_archive/research/gebaeude/<ProjectName>.md
```

Filename matches our convention for the existing 76 case studies (German base name, underscores, no spaces). One file per project — even if two stub names refer to the same building (the merge happens at the integration step, not in research).

## Batch index

| # | Batch | Projects | Note |
|---|---|---:|---|
| 1 | [Swiss pilots](batch_01_swiss_pilots.md) | 3 | Built case studies in Switzerland |
| 2 | [DE/AT/CH large urban](batch_02_de_at_large.md) | 5 | Larger / urban-scale projects |
| 3 | [BE/NL case-study buildings](batch_03_be_nl_buildings.md) | 3 | Belgian + Dutch, one possible duplicate to flag |
| 4 | [UK + unclear](batch_04_uk_unclear.md) | 2 | One UK project + one identification puzzle |
| 5 | [Teaching / research programs](batch_05_teaching_programs.md) | 4 | Not buildings — pedagogical or research initiatives |
| 6 | [EU-funded consortia](batch_06_eu_consortia.md) | 4 | Multi-partner R&D programmes |
| 7 | [Reuse platforms / tools](batch_07_reuse_platforms.md) | 2 | Digital marketplaces / matching tools |

Total: 23 dossiers.

Categories 5–7 are not buildings, so they only need the *Identification + People + Sources + Outcomes + Hurdles* sections, plus a list of case-study buildings the programme produced (if any).
