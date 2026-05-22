# Missing and Underused `Norm` Nodes in a Circular Construction Reuse Knowledge Graph

Generated: 2026-05-16

## Scope and caveat

This file converts the prior research answer into a standalone Markdown deliverable.

I found one relevant file-library note, but it was a **pollutant/reuse verification note**, not the full norm corpus. Therefore, project examples such as Europa Building, BedZED, Hastings Pier, Superlocal, Plattenpalast, CRCLR, Recyclinghaus, BioPartner 5, Big Dig, and Schildow should be treated as **corpus candidates**, not proof that a given standard was used.

Project–norm edges should only be marked **BELEGT** where project documentation explicitly cites the standard, test report, approval route, or assessment method.

## Recommended new or split norm nodes

| Priority | Recommended node | Why |
|---:|---|---|
| 1 | `norm_cen_ts_1090_201_2024` | Direct reuse-oriented technical specification for reclaimed structural steel; complements EN 1090-2 and is relevant where components are designed under EN 1993-1-1 for quasi-static, non-fatigue situations. |
| 2 | `norm_en_206` / national variants such as `norm_din_en_206`, `norm_nen_en_206` | Fundamental concrete specification/production standard; indirect but important for concrete requalification and comparison to new concrete. |
| 3 | Split `norm_eurocode_generic` into `norm_en_1992`, `norm_en_1993`, `norm_en_1995`, plus `norm_en_1996` | Concrete, steel, timber, and masonry need separate graph semantics; a generic Eurocode node will become noisy. |
| 4 | `norm_cen_ts_17440` | Existing/retained structures assessment framework; useful when reuse means retention, extension, modification, or retrofit rather than extracted component reuse. |
| 5 | `norm_nen_8700`, `norm_nen_8701`, `norm_nen_8702` | Dutch existing-structure assessment; especially relevant to Dutch concrete and structural component reuse. |
| 6 | `norm_nta_8713` | Dutch structural steel reuse guidance; use only if Dutch steel reuse appears in project sources. |
| 7 | `norm_fr_reemploi_acier_cticm` | France-specific professional recommendations for requalification of reused structural steel. |
| 8 | `norm_fcrbe_reclamation_audit` and/or `guide_fcrbe_reuse_toolkit` | Not structural norms, but useful metadata for Belgium, France, UK, Netherlands, and Luxembourg reuse process evidence. |

## Country × material norm table

| Country | Material | Relevant standard | Standard body | Applies to reuse directly or indirectly | Project examples from corpus | Evidence strength | Source citation | Recommended graph action |
|---|---|---|---|---|---|---|---|---|
| UK | Structural steel | SCI P427, SCI P440, BS EN 1090, BS EN 1993, UKCA/UK designated standards; add CEN/TS 1090-201 | SCI, BSI, CEN, UK Gov | SCI P427/P440 and CEN/TS 1090-201 are direct; EN 1090/1993 and UKCA are indirect/legal conformity | BedZED; Hastings Pier if structural steel is documented | Country/material inference only, unless project source names SCI/EN 1090 | https://www.steelconstruction.info/Sustainability ; https://www.nen.nl/cen-ts-1090-201-2024-en-330911 | Add `norm_cen_ts_1090_201_2024`; keep `norm_sci_p427`, `norm_sci_p440`, `norm_en_1090`; add project edge only if documentation says assessment/procurement followed them. |
| UK | Structural timber | BS EN 1995, BS EN 14081, BS 4978, BS 5756 | BSI/CEN | Indirect; grading/design standards, not reuse protocols | Hastings Pier; BedZED if timber reuse confirmed | Country/material inference only | https://ecostandard.org/wp-content/uploads/2025/08/2025-08_ECOS-policy-standards-timber-reuse.pdf | Add as metadata/design basis; no direct reuse edge unless grading report is found. |
| UK | Concrete / reinforced concrete / hollow-core slabs | BS EN 206, BS EN 1992, BS EN 1168, CEN/TS 17440 | BSI/CEN | Indirect; CEN/TS 17440 applies to existing/retained elements | BedZED; any UK precast or concrete reuse project | Country/material inference only | https://www.sis.se/en/produkter/construction-materials-and-building/structures-of-buildings/general/sis-cents-174402022/ ; https://w.sis.se/en/produkter/construction-materials-and-building/elements-of-buildings/ceilings-floors-stairs/ssen11682005/ | Add `norm_en_206`, `norm_en_1992`, `norm_cen_ts_17440`; link only as design/assessment basis. |
| UK | Façade glass / aluminium | BS EN 12150, BS EN 12600, BS EN 1279, BS EN 13830, BS EN 1090 for structural aluminium | BSI/CEN | Indirect; product/performance standards | BedZED; façade/window reuse candidates | Metadata only unless test report exists | EN façade/glass standards and EN 1090 product/execution route | Do not add project norm edge without glass/aluminium test or conformity report. |
| UK | Natural stone / brick / masonry | BS EN 771 series, BS EN 1996, BS 8298 for stone cladding | BSI/CEN | Indirect | Hastings Pier; BedZED if brick/stone reuse confirmed | Metadata only | EN 771 and Eurocode 6 baseline; BS 8298 for stone cladding | Add `norm_en_771`, `norm_en_1996`; edge only if reused masonry was structurally requalified. |
| UK | Insulation / mineral wool | BS EN 13162; hazardous-material screening separately | BSI/CEN | Indirect; product standard for new mineral wool | BedZED; retrofit/interior projects only if reused insulation is confirmed | Mostly unsuitable for graph edge | EN 13162 mineral-wool insulation product standard | Use as material metadata; avoid reuse edge unless insulation was tested and reinstalled. |
| Netherlands | Structural steel | NTA 8713, CEN/TS 1090-201, NEN-EN 1090, NEN-EN 1993, NEN 8700 | NEN/CEN | NTA 8713 and CEN/TS 1090-201 direct; Eurocode/EN 1090 indirect | BioPartner 5; Superlocal if steel involved | Country/material inference only | https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Facilitating-Future-Reuse_June2022.pdf | Add `norm_nta_8713`; link to Dutch steel projects only with source confirmation. |
| Netherlands | Structural timber | NEN-EN 1995, NEN-EN 14081 | NEN/CEN | Indirect | Superlocal; BioPartner 5 if timber/doors/furniture only then non-structural | Metadata only | https://ecostandard.org/wp-content/uploads/2025/08/2025-08_ECOS-policy-standards-timber-reuse.pdf | Add as design-basis metadata, not reuse proof. |
| Netherlands | Concrete / reinforced concrete / hollow-core slabs | CROW-CUR Richtlijn 4:2023, NEN 8700/8701/8702, NEN-EN 1168, NEN-EN 1992, NEN-EN 206 | CROW-CUR, NEN/CEN | CROW-CUR 4 is direct for structural precast reuse; NEN 8700/8702 and EN 1168/1992/206 indirect | Superlocal Expogebouw; BioPartner 5; Dutch hollow-core projects | Strong country/material inference; project BELEGT only if guideline named | https://www.crow.nl/kennisproducten/crow-cur-richtlijn-42023-hergebruik-constructieve-prefab-betonelementen/ ; https://www.nen.nl/en/bouw/constructieve-veiligheid/constructieve-veiligheid-bestaande-bouw | Keep `norm_crow_cur_4_2023`; add `norm_nen_8700`, `norm_nen_8701`, `norm_nen_8702`, `norm_en_206`; connect to HCS/precast reuse projects only when documentation supports it. |
| Netherlands | Façade glass / aluminium | NEN-EN 12150, 12600, 1279, 13830; NEN-EN 1090 for aluminium; Dutch glass design standards such as NEN 2608 need verification | NEN/CEN | Indirect | Superlocal; BioPartner 5 if façade/window reuse documented | Metadata only | EN façade/glass standards are product/performance baselines, not reuse protocols | Add material metadata; do not infer norm edge. |
| Netherlands | Natural stone / brick / masonry | NEN-EN 771, NEN-EN 1996, NEN 8700 where existing masonry retained | NEN/CEN | Indirect | Superlocal; any brick reuse project | Metadata only | EN 771/1996 baseline | Add generic norm nodes; project edge only after masonry assessment evidence. |
| Netherlands | Insulation / mineral wool | NEN-EN 13162; hazardous-substance checks for old mineral wool | NEN/CEN | Indirect | Superlocal; BioPartner 5 only if insulation reused | Mostly unsuitable for edge | EN 13162 baseline | Store as material metadata; no project norm edge without testing. |
| Norway | Structural steel | NS-EN 1090, NS-EN 1993, CEN/TS 1090-201 | Standard Norge/CEN | CEN/TS 1090-201 direct; others indirect | Norwegian corpus project not named in accessible note | Country/material inference only | https://www.nen.nl/cen-ts-1090-201-2024-en-330911 | Add CEN/TS node; link only with project evidence. |
| Norway | Structural timber | NS-EN 1995, NS-EN 14081 | Standard Norge/CEN | Indirect | Norwegian project not named | Metadata only | Timber reuse standardization remains underdeveloped | Metadata only. |
| Norway | Concrete / reinforced concrete / hollow-core slabs | NS 3682:2022, NS-EN 1168, NS-EN 1992, NS-EN 206 | Standard Norge/CEN | NS 3682 direct for hollow-core slab reuse; EN standards indirect | Norwegian hollow-core reuse / KA13-type precedent if in corpus | Strong country/material inference; direct standard | https://standard.no/en/sectors/byggevarer/norwegian-standard-for-hollow-core-slabs-for-reuse--ns-3682/ | Keep `norm_ns_3682`; add edges only to documented HCS projects. |
| Norway | Façade glass / aluminium | NS-EN 12150/12600/1279/13830; NS-EN 1090 | Standard Norge/CEN | Indirect | Norwegian project if façade reuse documented | Metadata only | Product/performance standards only | Metadata only. |
| Norway | Natural stone / brick / masonry | NS-EN 771, NS-EN 1996 | Standard Norge/CEN | Indirect | Norwegian project if masonry reuse documented | Metadata only | EN 771/1996 baseline | Metadata only. |
| Norway | Insulation / mineral wool | NS-EN 13162 | Standard Norge/CEN | Indirect | Norwegian project if insulation reuse documented | Unsuitable for project edge unless tested | EN 13162 baseline | Metadata only. |
| Finland | Structural steel | SFS-EN 1090, SFS-EN 1993, CEN/TS 1090-201 | SFS/CEN | CEN/TS direct; EN standards indirect | Finnish ReCreate / Tampere if steel involved | Country/material inference only | https://www.nen.nl/cen-ts-1090-201-2024-en-330911 | Add CEN/TS node; link only if project evidence. |
| Finland | Structural timber | SFS-EN 1995, SFS-EN 14081 | SFS/CEN | Indirect | Finnish timber reuse cases if present | Metadata only | https://www.sciencedirect.com/science/article/pii/S0921344921001622 | Metadata only; no direct reuse edge. |
| Finland | Concrete / reinforced concrete / hollow-core slabs | SFS-EN 1168, SFS-EN 1992, SFS-EN 206; site-specific verification; ReCreate quality/testing workflow | SFS/CEN; project guidance | Indirect; reuse project practice is emerging | Finnish ReCreate/Tampere hollow-core slabs | Strong project-domain inference, not BELEGT for corpus unless project named | https://recreate-project.eu/tag/hollow-core-slabs/ ; https://w.sis.se/en/produkter/construction-materials-and-building/elements-of-buildings/ceilings-floors-stairs/ssen11682005/ | Add EN 1168/1992/206 nodes; do not invent Finnish reuse norm node unless a national document is confirmed. |
| Finland | Façade glass / aluminium | SFS-EN 12150/12600/1279/13830; SFS-EN 1090 | SFS/CEN | Indirect | Finnish project if façade reuse documented | Metadata only | Product/performance baseline | Metadata only. |
| Finland | Natural stone / brick / masonry | SFS-EN 771, SFS-EN 1996 | SFS/CEN | Indirect | Finnish brick/stone reuse if present | Metadata only | EN masonry baseline | Metadata only. |
| Finland | Insulation / mineral wool | SFS-EN 13162 | SFS/CEN | Indirect | Finnish project if insulation reused | Unsuitable unless test evidence | EN 13162 baseline | Metadata only. |
| Germany | Structural steel | DIN EN 1090, DIN EN 1993, CEN/TS 1090-201; possibly DIN-specific execution rules | DIN/CEN | CEN/TS direct; DIN EN 1090/1993 indirect | Recyclinghaus Hannover; CRCLR; Plattenpalast/Schildow if steel involved | Country/material inference only | https://www.nen.nl/cen-ts-1090-201-2024-en-330911 | Add `norm_cen_ts_1090_201_2024`; retain `norm_en_1090`; add `norm_en_1993`. |
| Germany | Structural timber | DIN EN 1995, DIN EN 14081, DIN 4074 | DIN/CEN | Indirect; grading/design | Recyclinghaus; CRCLR if structural timber documented | Metadata only unless grading evidence | https://ecostandard.org/wp-content/uploads/2025/08/2025-08_ECOS-policy-standards-timber-reuse.pdf | Add/keep timber norm nodes as indirect. |
| Germany | Concrete / reinforced concrete / hollow-core slabs | DIN EN 206, DIN EN 1992, DIN EN 1168, CEN/TS 17440 | DIN/CEN | Indirect; CEN/TS for existing/retained structures | Plattenpalast Berlin; Berlin Schildow; Recyclinghaus | Country/material inference only | https://www.sis.se/en/produkter/construction-materials-and-building/structures-of-buildings/general/sis-cents-174402022/ ; https://w.sis.se/en/produkter/construction-materials-and-building/elements-of-buildings/ceilings-floors-stairs/ssen11682005/ | Add `norm_en_206`, `norm_en_1992`, `norm_cen_ts_17440`; link to Plattenbau reuse only if assessment source confirms. |
| Germany | Façade glass / aluminium | DIN 18008 for glass design; DIN EN 12150/12600/1279/13830; DIN EN 1090 for aluminium structures | DIN/CEN | Indirect | Recyclinghaus; CRCLR; façade-window projects | Metadata only | EN glass/façade standards are performance baselines | Add metadata; no project norm edge without test/design report. |
| Germany | Natural stone / brick / masonry | DIN EN 771, DIN EN 1996, EN 1469 for stone cladding | DIN/CEN | Indirect | Recyclinghaus; CRCLR if brick/stone reused | Metadata only | EN 1469 covers natural-stone slabs for cladding; EN 771/1996 are masonry baselines | Add nodes; edge only with source proof. |
| Germany | Insulation / mineral wool | DIN EN 13162; TRGS/old mineral wool rules as pollutant metadata | DIN/CEN; BAuA/TRGS | Indirect; often more relevant as hazardous-material metadata | CRCLR; Recyclinghaus; Plattenpalast/Schildow if old insulation disturbed/reused | Unsuitable for norm edge unless project tested | EN 13162 product baseline | Use as material metadata; keep pollutant-risk edges separate. |
| Belgium | Structural steel | NBN EN 1090, NBN EN 1993, CEN/TS 1090-201; FCRBE/Buildwise procedures; possible future H-REUSE horizontal standard | NBN/CEN; Buildwise | CEN/TS direct; FCRBE/Buildwise process guidance; EN indirect | Europa Building; Multi Brussels | Country/material inference only | https://buildwise.be/fr/nouvelles/reemploi-des-produits-de-construction/ ; https://www.nen.nl/cen-ts-1090-201-2024-en-330911 | Add CEN/TS steel reuse node; add FCRBE/Buildwise as metadata, not as hard norm. |
| Belgium | Structural timber | NBN EN 1995, NBN EN 14081; FCRBE/Buildwise performance justification | NBN/CEN; Buildwise | Indirect; process guidance | Europa Building reclaimed timber windows are façade/joinery, not necessarily structural | Metadata only | https://buildwise.be/fr/themes/construction-durable/l-economie-circulaire-dans-la-construction/reemploi-recyclage-et-gestion-des-dechets/ | Metadata only unless structural timber assessment exists. |
| Belgium | Concrete / reinforced concrete / hollow-core slabs | NBN EN 206, NBN EN 1992, NBN EN 1168, CEN/TS 17440; FCRBE/Buildwise | NBN/CEN; Buildwise | Indirect; no Belgium-specific direct HCS reuse norm found | Multi Brussels; Europa Building if concrete reuse documented | Country/material inference only | https://www.sis.se/en/produkter/construction-materials-and-building/structures-of-buildings/general/sis-cents-174402022/ | Add EN/TS nodes; use FCRBE as project-process metadata. |
| Belgium | Façade glass / aluminium | NBN EN 12150/12600/1279/13830; NBN EN 1090 for aluminium; Buildwise reuse performance procedure | NBN/CEN; Buildwise | Indirect/process guidance | Europa Building; Multi Brussels | Strong material relevance, but project-standard inference only | https://buildwise.be/fr/themes/construction-durable/l-economie-circulaire-dans-la-construction/reemploi-recyclage-et-gestion-des-dechets/ | Add `guide_buildwise_reuse_performance` metadata; no norm edge without façade testing. |
| Belgium | Natural stone / brick / masonry | NBN EN 771, NBN EN 1996, EN 1469; FCRBE reclamation audit | NBN/CEN; FCRBE | Indirect/process guidance | Multi Brussels; Europa if masonry/stone reused | Metadata only | https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/ | Use FCRBE as metadata; add EN nodes only to materials. |
| Belgium | Insulation / mineral wool | NBN EN 13162; Buildwise reuse-performance and hazardous-material screening | NBN/CEN; Buildwise | Indirect; often unsuitable for direct reuse edge | Multi Brussels; Europa if insulation reused | Unsuitable unless testing exists | https://buildwise.be/fr/nouvelles/reemploi-des-produits-de-construction/ | Metadata only; require project lab evidence. |
| France | Structural steel | CTICM “réemploi d’éléments structuraux en acier”, NF EN 1090, NF EN 1993, CEN/TS 1090-201 | CTICM, AFNOR/CEN | CTICM and CEN/TS direct; EN 1090/1993 indirect | French corpus projects not named in accessible note | Strong country/material inference | https://www.cticm.com/nouvelle-parution-recommandations-professionnelles-reemploi-delements-structuraux-en-acier/ | Add `norm_fr_reemploi_acier_cticm`; add CEN/TS node; project edge only when cited. |
| France | Structural timber | NF EN 1995, NF EN 14081; CSTB reuse guides for wood professionals | AFNOR/CEN; CSTB | Indirect/process guidance | French timber reuse projects if present | Metadata only | https://www.cstb.fr/getmedia/e173e09f-4afe-4e46-9a9e-e0300868f2d5/le-reemploi-en-pratique-pour-les-professionnels-du-bois.pdf | Add CSTB guide as metadata; no structural edge without grading evidence. |
| France | Concrete / reinforced concrete / hollow-core slabs | NF EN 206, NF EN 1992, NF EN 1168, CEN/TS 17440; CSTB risk/reuse guides | AFNOR/CEN; CSTB | Indirect | French concrete reuse projects if present | Country/material inference only | https://www.cstb.fr/en-us/all-the-news/reuse-master-risks-reliability-practices | Add EN/TS nodes; CSTB as metadata. |
| France | Façade glass / aluminium | NF EN 12150/12600/1279/13830; NF EN 1090 for aluminium | AFNOR/CEN | Indirect | French façade reuse projects if present | Metadata only | EN façade/glass standards are baselines; reuse needs performance proof | Metadata only. |
| France | Natural stone / brick / masonry | NF EN 771, NF EN 1996, EN 1469; FCRBE/CSTB reclamation audit | AFNOR/CEN; CSTB/FCRBE | Indirect/process guidance | French masonry/stone projects if present | Metadata only | https://www.cstb.fr/getmedia/365c639a-3f3a-4e19-b2d0-e55f202414a2/Guide-reclamation-audit.pdf | Add FCRBE/CSTB guide metadata; no hard norm edge unless structural assessment exists. |
| France | Insulation / mineral wool | NF EN 13162; CSTB reuse-risk guidance | AFNOR/CEN; CSTB | Indirect; likely unsuitable for direct edge | French retrofit projects if present | Unsuitable unless tested | https://www.cstb.fr/en-us/all-the-news/reuse-master-risks-reliability-practices | Metadata only. |
| Switzerland | Structural steel | SIA 269/3, SIA 263, CEN/TS 1090-201 if European steel reuse route used | SIA/CEN | SIA 269/3 direct for existing steel structures; CEN/TS direct for reclaimed steel components | Swiss corpus projects not named in accessible note | Strong country/material inference | https://trimis.ec.europa.eu/project/maintenance-structures-steel-structures-sia-2693-agb2005202 | Keep/expand `norm_sia_schweiz` into `norm_sia_269`, `norm_sia_269_3`; add CEN/TS if component reuse is transnational. |
| Switzerland | Structural timber | SIA 269/5, SIA 265 | SIA | Direct for existing timber structures; indirect for extracted components | Swiss projects if timber reuse documented | Country/material inference only | https://infoscience.epfl.ch/bitstreams/3b7960f0-cbc2-40c7-91d9-20958022cae2/download | Split SIA node into material-specific child nodes. |
| Switzerland | Concrete / reinforced concrete / hollow-core slabs | SIA 269/2, SIA 262, EN 1168 if HCS product used | SIA/CEN | SIA 269/2 direct for existing concrete assessment; EN 1168 indirect | Swiss concrete reuse projects if present | Strong country/material inference | https://www.academia.edu/5666538/SIA_269_2_the_New_Swisscode_for_Existing_Concrete_Structures | Add `norm_sia_269_2`; link when concrete retained/requalified. |
| Switzerland | Façade glass / aluminium | SIA 260-series design basis; EN glass/façade standards where adopted; EN 1090 for aluminium if applicable | SIA/CEN | Indirect | Swiss façade/window reuse projects if present | Metadata only | SIA 269 is primarily structural; EN façade/glass standards remain product baselines | Metadata only unless façade engineering report exists. |
| Switzerland | Natural stone / brick / masonry | SIA 269/6, SIA 266, EN 771/1469 as product references | SIA/CEN | SIA 269/6 direct for existing masonry structures; product standards indirect | Swiss masonry/stone reuse projects if present | Country/material inference only | https://infoscience.epfl.ch/bitstreams/3b7960f0-cbc2-40c7-91d9-20958022cae2/download | Add `norm_sia_269_6`. |
| Switzerland | Insulation / mineral wool | EN 13162; SIA 2032 for embodied impacts | SIA/CEN | EN indirect; SIA 2032 metadata/LCA, not requalification | Swiss retrofit projects if present | Useful as metadata only | https://www.scandens.ch/know-how-en/erstellungsemissionen-graue-emissionen/ | Keep `norm_sia_schweiz` or add `norm_sia_2032` as LCA metadata, not reuse edge. |
| Denmark | Structural steel | DS/EN 1090, DS/EN 1993, CEN/TS 1090-201 | Danish Standards/CEN | CEN/TS direct; Eurocode indirect | Danish corpus projects if steel reuse present | Country/material inference only | https://www.ds.dk/en/our-services/eurocodes | Add CEN/TS node; use DS/EN as national designation metadata. |
| Denmark | Structural timber | DS/EN 1995, DS/EN 14081 | Danish Standards/CEN | Indirect | Danish corpus projects if timber reused | Metadata only | https://www.ds.dk/en/our-services/eurocodes | Metadata only. |
| Denmark | Concrete / reinforced concrete / hollow-core slabs | DS/EN 1168, DS/EN 1992, DS/EN 206; DS/INF 671:2025 noted but withdrawn; research/project protocols | Danish Standards/CEN; DTI/research | Mostly indirect; no mature mandatory norm reported for reused HCS | Danish hollow-core / Gellerup-type projects | Strong country/material inference, but not graph BELEGT | https://www.dti.dk/projects/reuse-of-hollow-core-slabs/44469 | Do not create hard Danish HCS norm edge; add EN 1168 and perhaps a research/protocol metadata node. |
| Denmark | Façade glass / aluminium | DS/EN 12150/12600/1279/13830; DS/EN 1090 | Danish Standards/CEN | Indirect | Danish façade projects if present | Metadata only | EN product standards baseline | Metadata only. |
| Denmark | Natural stone / brick / masonry | DS/EN 771, DS/EN 1996 | Danish Standards/CEN | Indirect | Danish brick/stone projects if present | Metadata only | https://pub.norden.org/nord2023-031/5-circular-construction-in-the-nordic-countries.html | Metadata only. |
| Denmark | Insulation / mineral wool | DS/EN 13162 | Danish Standards/CEN | Indirect | Danish projects if insulation reused | Unsuitable unless tested | EN 13162 product baseline | Metadata only. |
| USA | Structural steel | AISC 360, AISC 303, ASTM material standards; no direct US reuse norm equivalent found in this pass | AISC/ASTM | Indirect | Big Dig Building | Country/material inference only | AISC/ASTM structural steel design and material identification route | Add only if USA project docs cite AISC/ASTM; otherwise metadata. |
| USA | Structural timber | NDS, grading rules, reclaimed timber grading by qualified agencies | AWC/ALS/WWPA etc. | Indirect | Big Dig only if timber involved | Metadata only | Not enough source evidence in this pass for a safe graph node recommendation | Defer unless project docs cite a grading standard. |
| USA | Concrete / reinforced concrete | ACI 318, ACI 562, ASTM C42/C805/C597 as testing methods | ACI/ASTM | ACI 562 direct for existing concrete repair/assessment; indirect for extracted reuse | Big Dig Building | Country/material inference only | ACI 562 is for assessment, repair, and rehabilitation of existing concrete structures | Add `norm_aci_562` as existing-structure assessment metadata; no reuse edge unless cited. |
| USA | Façade glass / aluminium | ASTM E1300; Aluminum Design Manual; AAMA/FGIA standards | ASTM/Aluminum Association/FGIA | Indirect | Big Dig if façade reuse documented | Metadata only | ASTM E1300 determines load resistance of glass in buildings | Metadata only. |
| USA | Natural stone / brick / masonry | TMS 402/602, ASTM C90/C216/C615/C568 | TMS/ASTM | Indirect | Big Dig if masonry/stone reused | Metadata only | TMS 402 is the US masonry structural code baseline | Metadata only. |
| USA | Insulation / mineral wool | ASTM C612/C665 and related insulation standards | ASTM | Indirect | Big Dig if insulation reused | Unsuitable unless tested | ASTM mineral-fiber standards are product baselines, not reuse protocols | Metadata only. |
| Luxembourg | All six material groups | EN/National Eurocode adoptions; FCRBE reuse toolkit | ILNAS/CEN; FCRBE | EN indirect; FCRBE process guidance | Luxembourg corpus project not named in accessible note | Country-level metadata only | https://www.tudelft.nl/bk/onderzoek/projecten/fcrbe | Use FCRBE as metadata; do not add material-specific norm edges without project docs. |
| Japan | All six material groups | Likely JIS/AIJ/Building Standard Law routes, but not verified in this pass | JIS/AIJ/MLIT | Unknown / indirect | Japan corpus project not named in accessible note | Insufficient evidence | No reliable source captured in this pass | Do not create Japanese norm nodes yet; queue separate Japan-specific standards review. |

## Graph action model

Do **not** add blanket project–norm edges from country/material alone.

Recommended modeling pattern:

```text
Project --usesMaterial--> Material
Material --hasApplicableNormCandidate--> Norm
Project --hasApplicableNormCandidate--> Norm
```

Use the last edge only when labelled:

```text
country/material inference only
```

Use a stronger compliance edge only when project documentation is explicit:

```text
Project --compliesWithNorm--> Norm
```

Recommended edge-status values:

- `project-specific BELEGT`
- `country/material inference only`
- `unsuitable for graph edge but useful as metadata`

## Practical graph update recommendations

1. Add `norm_cen_ts_1090_201_2024`.
2. Add `norm_en_206`.
3. Split `norm_eurocode_generic` into:
   - `norm_en_1992`
   - `norm_en_1993`
   - `norm_en_1995`
   - `norm_en_1996`
4. Add `norm_cen_ts_17440`.
5. Add Dutch existing-building standards:
   - `norm_nen_8700`
   - `norm_nen_8701`
   - `norm_nen_8702`
6. Add `norm_nta_8713` for Dutch reused structural steel, but only connect it to projects with documentation.
7. Split `norm_sia_schweiz` into material-relevant SIA nodes:
   - `norm_sia_269`
   - `norm_sia_269_2`
   - `norm_sia_269_3`
   - `norm_sia_269_5`
   - `norm_sia_269_6`
8. Add `norm_fr_reemploi_acier_cticm`.
9. Add FCRBE/Buildwise/CSTB guides as **guidance/metadata nodes**, not as hard structural compliance norms.
10. Treat insulation/mineral wool standards mostly as product or hazardous-material metadata, not direct reuse requalification edges.
