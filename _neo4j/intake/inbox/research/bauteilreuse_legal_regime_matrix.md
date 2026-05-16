# Legal and regulatory conditions affecting Bauteilreuse projects

Prepared: 2026-05-16

**Purpose.** This Markdown file supports modelling of `RechtlicheBedingung` nodes in a reuse knowledge graph for structural building-element reuse.

**Scope.** Structural building elements include load-bearing steel, timber, concrete, masonry, slabs, beams, columns, load-bearing façades, structural kits and safety-critical connectors.

**Project-edge rule.** A project-level graph relationship is recommended only where a cited source connects a legal condition to a specific project or case. Otherwise, the row is explicitly treated as **country-level metadata**.

**Important limitation.** This is legal-regulatory research support, not legal advice. Competent authorities, local counsel, engineers and insurers should verify any project-specific conclusion.

## High-level node action summary

| Node | Status in prompt | Recommended graph action |
|---|---:|---|
| `rb_bauordnungsrecht` | Existing | Keep as general parent for country building approval/building-code requirements. |
| `rb_zulassung_im_einzelfall` | Existing | Keep as generic one-off/project-specific approval concept, but distinguish national equivalents from German ZiE. |
| `rb_dibt_zustimmung` | Proposed | Add as Germany-specific child/specialization of ZiE/vBG practice. |
| `rb_bauproduktenverordnung_cpr` | Proposed | Add for EU/EEA CPR/CE product-status issues; do not attach to USA/Japan/UK domestic status without country-specific qualifier. |
| `rb_ce_ukca_marking_reused_steel` | Existing | Keep UK-specific and steel-specific. |
| `rb_gewaehrleistung` | Existing | Keep as warranty/defects parent; add country notes for decennial liability, standard contracts or statutory warranties. |
| `rb_produkthaftung` | Existing | Keep as product-liability/product-safety parent where reused elements are supplied/placed on market. |
| `rb_vergaberecht` | Existing | Keep as public procurement parent; project-level edges require tender/project evidence. |
| `rb_eu_taxonomie` | Existing | Keep for EU taxonomy/circularity reporting where taxonomy criteria are invoked. |
| `rb_denkmalschutz` | Proposed | Add as general heritage-protection parent; relate `rb_grade_ii_listing` as UK-specific child/instance. |
| `rb_grade_ii_listing` | Existing | Keep for UK listed-building cases; project edge only with evidence of Grade II/listed status. |
| `rb_kreislaufwirtschaftsgesetz_krwg` | Proposed | Add as Germany-specific waste/reuse-law node; do not use for other countries. |
| `rb_materialpass` | Proposed | Add as cross-country parent for material passports, deconstruction inventories, material mapping, PEMD and circularity reporting. |
| `rb_boulder_deconstruction_ordinance_8366` | Existing | Keep as Boulder-specific node; project-level edge is supported for Boulder Community Hospital/city-owned site case. |

## Detailed matrix

| Country | Legal regime | Applies to which material/Bauteiltyp | Relevant project candidates | Evidence source | Is this graph node existing or proposed | Recommended graph action |
| --- | --- | --- | --- | --- | --- | --- |
| Germany | 1. Building approval / Bauordnungsrecht | All reused load-bearing members and safety-critical assemblies; steel, timber, concrete, masonry, façades. | Country-level metadata only unless a project source is available. | [DE-MBO] | Existing: `rb_bauordnungsrecht` | Attach Germany country metadata and MBO evidence. |
| Germany | 2. ZiE / vBG / DIBt one-off route | Non-standard, undocumented or rule-deviating reused Bauprodukte and Bauarten. | Country-level metadata only unless a project source is available. | [DE-DIBT], [DE-MBO] | Existing + proposed: `rb_zulassung_im_einzelfall`, `rb_dibt_zustimmung` | Add `rb_dibt_zustimmung` as Germany-specific child/specialization. |
| Germany | 3. CPR / CE / construction product status | Reused products placed on market: steel, timber, precast concrete, fasteners, kits. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [EU-CPR-COM] | Proposed: `rb_bauproduktenverordnung_cpr` | Create EU CPR node; link to Germany as country metadata. |
| Germany | 4. Warranty and liability | All reused structural elements; especially load-bearing members and connectors. | Project edge only where contract/insurance/project source identifies the condition. | [DE-DIBT], [FCRBE-INSURANCE] | Existing: `rb_gewaehrleistung`, `rb_produkthaftung` | Keep generic nodes; add note that reuse needs test records and risk allocation. |
| Germany | 5. Public procurement | Public buildings, deconstruction and reused-element supply packages. | Project edge only where a tender/project source cites the requirement. | [EU-GPP-BUILDINGS], [EU-TAXONOMY-RENOVATION] | Existing: `rb_vergaberecht`, `rb_eu_taxonomie` | Add country metadata; project edge only from tender/call text. |
| Germany | 6. Heritage protection / Denkmalschutz | Historic timber, masonry, iron/steel, façades and protected fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [DE-MBO] | Proposed: `rb_denkmalschutz` | Create general heritage node; add state-law note. |
| Germany | 7. Waste law vs product status / KrWG | All dismantled elements; distinction between reuse of non-waste and preparation for reuse of waste. | Country-level metadata only unless a project source is available. | [DE-KRWG], [DE-UBA-WASTE] | Proposed: `rb_kreislaufwirtschaftsgesetz_krwg` | Add Germany-specific KrWG node; relate to generic waste/product-status concept. |
| Germany | 8. Material passport / circularity reporting | Whole-building inventories and reusable structural components. | Project edge only where a source identifies a passport, inventory or report for that project. | [DE-DGNB-PASS], [EU-TAXONOMY-RENOVATION] | Proposed: `rb_materialpass` | Add country metadata; mark mostly voluntary/procurement/taxonomy-driven. |
| UK | 1. Building approval / building regulations | Reused steel, timber, concrete, masonry and structural connections. | Country-level metadata only unless a project source is available. | [UK-APPROVED-DOCS] | Existing: `rb_bauordnungsrecht` | Attach UK building-control metadata. |
| UK | 2. Project-specific technical acceptance | Non-standard reused members; especially reclaimed structural steel. | Country-level metadata only unless a project source is available. | [UK-SCI-STEEL], [UK-APPROVED-DOCS] | Existing generic: `rb_zulassung_im_einzelfall` by analogy | Model as local building-control acceptance, not German ZiE. |
| UK | 3. CE / UKCA / reused steel product status | Structural steel most directly; other construction products covered by designated standards. | Country-level metadata only; project edge only if source cites product-status/marking route. | [UK-GOV-CPR], [UK-CE-UKCA], [UK-SCI-STEEL] | Existing: `rb_ce_ukca_marking_reused_steel` | Keep material-specific; do not apply to non-steel without new evidence. |
| UK | 4. Warranty and liability | All reused structural elements and supplier/contractor chains. | Project edge only where contract/insurance/project source identifies the condition. | [FCRBE-INSURANCE] | Existing: `rb_gewaehrleistung`, `rb_produkthaftung` | Add UK country note on contract and latent-defect risk. |
| UK | 5. Public procurement | Public buildings, deconstruction contracts, steel packages. | Project edge only where a tender/project source cites the requirement. | [UK-CONSTRUCTION-PLAYBOOK], [EU-GPP-BUILDINGS] | Existing: `rb_vergaberecht` | Add UK procurement metadata. |
| UK | 6. Listed buildings / Grade II heritage | Protected historic fabric: timber, masonry, façades, structures. | Project edge only with evidence that the specific building/component is protected or listed. | [UK-HISTORIC-ENGLAND] | Existing + proposed: `rb_grade_ii_listing`, `rb_denkmalschutz` | Keep `rb_grade_ii_listing` as UK-specific child of heritage. |
| UK | 7. Waste law vs product status | Dismantled elements moved, stored or sold as reclaimed materials. | Country-level metadata only unless a project source is available. | [UK-WASTE-DOC], [FCRBE-PRODUCT-WASTE] | No dedicated node in prompt | Consider generic waste/product-status node; do not use KrWG. |
| UK | 8. Material passport / circularity reporting | Whole-building and component inventories; mostly voluntary/client-led. | Project edge only where a source identifies a passport, inventory or report for that project. | [UKGBC-CE] | Proposed: `rb_materialpass` | Add UK metadata; project edge only with passport source. |
| Belgium | 1. Regional building permits | Reused structural elements in Brussels-Capital, Wallonia and Flanders. | Country-level metadata only unless a project source is available. | [BE-BRUSSELS-PERMIT], [BE-FLANDERS-PERMIT], [BE-WALLONIA-PERMIT] | Existing: `rb_bauordnungsrecht` | Add Belgium regional-permit metadata. |
| Belgium | 2. Case-by-case technical acceptance | Non-standard reused structural products; technical control/engineer/insurer acceptance. | Country-level metadata only unless a project source is available. | [FCRBE-INSURANCE], [OPALIS-ABOUT] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as case-by-case proof; no ZiE-equivalence asserted. |
| Belgium | 3. EU CPR / CE / product status | Reused elements placed on market: steel, timber, concrete, kits. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [FCRBE-PRODUCT-WASTE] | Proposed: `rb_bauproduktenverordnung_cpr` | Create CPR node; link Belgium country metadata. |
| Belgium | 4. Decennial liability and insurance | Structural stability/solidity/watertightness; load-bearing elements. | Project edge only where contract/insurance/project source identifies the condition. | [BE-FPS-DECENNIAL], [FCRBE-INSURANCE] | Existing: `rb_gewaehrleistung` | Add Belgium decennial-liability country note. |
| Belgium | 5. Public procurement / circular reuse programmes | Public buildings, public-space works, deconstruction and reuse supply. | Project edge only where a tender/project source cites the requirement. | [EU-GPP-BUILDINGS], [FCRBE-FINAL] | Existing: `rb_vergaberecht` | Country metadata; project edge only from tender/source. |
| Belgium | 6. Heritage protection | Protected regional heritage fabric and listed buildings. | Project edge only with evidence that the specific building/component is protected or listed. | [BE-BRUSSELS-HERITAGE], [BE-FLANDERS-HERITAGE], [BE-WALLONIA-HERITAGE] | Proposed: `rb_denkmalschutz` | Add regional heritage metadata. |
| Belgium | 7. Waste law vs product status | All dismantled elements; end-of-waste and product/non-waste distinction. | Country-level metadata only unless a project source is available. | [FCRBE-PRODUCT-WASTE], [BE-OVAM] | No dedicated node in prompt | Add generic waste/product-status metadata; do not use KrWG. |
| Belgium | 8. Material passport / circularity reporting | Reuse inventories and circular construction tools; structural elements where documented. | Project edge only where a source identifies a passport, inventory or report for that project. | [OPALIS-ABOUT], [FCRBE-FINAL], [BE-FLANDERS-OPALIS] | Proposed: `rb_materialpass` | Add Belgium programme metadata; project edge only with inventory. |
| Netherlands | 1. Bbl / Omgevingswet building approval | Reused structural steel, timber, concrete, masonry and façades. | Country-level metadata only unless a project source is available. | [NL-BBL-IPLO], [NL-GOV-CE] | Existing: `rb_bauordnungsrecht` | Add Netherlands Bbl metadata. |
| Netherlands | 2. Equivalence / performance proof | Non-standard reused members with engineering proof and standards route. | Country-level metadata only unless a project source is available. | [NL-BBL-IPLO], [NL-NEN] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as equivalence/performance proof, not ZiE. |
| Netherlands | 3. EU CPR / CE / NEN product status | Construction products placed on market; structural products and kits. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [NL-NEN] | Proposed: `rb_bauproduktenverordnung_cpr` | Link CPR and NEN documentation as country metadata. |
| Netherlands | 4. Warranty and product liability | All reused structural elements and contractor/supplier chains. | Project edge only where contract/insurance/project source identifies the condition. | [NL-CMS-PL] | Existing: `rb_gewaehrleistung`, `rb_produkthaftung` | Add Dutch liability metadata. |
| Netherlands | 5. Circular public procurement | Public buildings, infrastructure and deconstruction/reuse packages. | Project edge only where a tender/project source cites the requirement. | [NL-GOV-CE], [NL-PIANOO] | Existing: `rb_vergaberecht` | Add circular procurement country metadata. |
| Netherlands | 6. Heritage protection | Monuments and protected urban/village views. | Project edge only with evidence that the specific building/component is protected or listed. | [NL-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Netherlands heritage metadata. |
| Netherlands | 7. Waste law vs product status | Dismantled components, secondary materials and product/resource status. | Country-level metadata only unless a project source is available. | [NL-GOV-CE], [FCRBE-PRODUCT-WASTE] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Netherlands | 8. Material passport / Madaster / MPG context | Whole-building material records, residual value, reusable components. | Project edge only where a source identifies a passport, inventory or report for that project. | [NL-MADASTER], [NL-GOV-CE] | Proposed: `rb_materialpass` | Add country metadata; edge to projects only with Madaster/passport evidence. |
| Switzerland | 1. Cantonal building approval and SIA standards | Reused structural steel, timber, concrete, masonry and façades. | Country-level metadata only unless a project source is available. | [CH-PERMIT], [CH-SIA] | Existing: `rb_bauordnungsrecht` | Add Switzerland cantonal/SIA metadata. |
| Switzerland | 2. Project-specific technical acceptance | Non-standard reused members requiring engineer proof and cantonal acceptance. | Country-level metadata only unless a project source is available. | [CH-PERMIT], [CH-SIA] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as local technical acceptance, not ZiE. |
| Switzerland | 3. Construction-products regime / market status | Structural products placed on market; Swiss regime distinct from EU but CE relevant for trade. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-COM] | Proposed variant: `rb_bauproduktenverordnung_cpr` only with note | Link as related, not identical; consider `rb_schweizer_bauproduktegesetz` if granularity needed. |
| Switzerland | 4. Warranty and liability / SIA 118 | All reused structural elements; defects rights and contract allocation. | Project edge only where contract/insurance/project source identifies the condition. | [CH-SIA118-EXTRACT] | Existing: `rb_gewaehrleistung` | Add Swiss SIA/CO defects metadata. |
| Switzerland | 5. Public procurement | Public buildings and reused material packages. | Project edge only where a tender/project source cites the requirement. | [CH-BKB] | Existing: `rb_vergaberecht` | Add Swiss procurement metadata. |
| Switzerland | 6. Heritage protection | Protected historic fabric and monuments. | Project edge only with evidence that the specific building/component is protected or listed. | [CH-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Swiss heritage metadata. |
| Switzerland | 7. Waste law vs product status | Construction waste, mineral waste, timber, metals, reusable elements. | Country-level metadata only unless a project source is available. | [CH-BAFU-CE], [CH-BAFU-WASTE] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Switzerland | 8. Material passport / circularity reporting | Building inventories and reusable structural elements; mostly voluntary/client-led. | Project edge only where a source identifies a passport, inventory or report for that project. | [CH-BAFU-CE] | Proposed: `rb_materialpass` | Add voluntary/passport metadata. |
| France | 1. Building approval / RE2020 context | Reused structural elements in new buildings; carbon/LCA context for materials. | Country-level metadata only unless a project source is available. | [FR-RE2020] | Existing: `rb_bauordnungsrecht` | Add France RE2020/building-regulation metadata. |
| France | 2. ATEx / technical assessment route | Innovative or non-traditional reused structural systems and components. | Country-level metadata only unless a project source is available. | [FR-CSTB-ATEX], [FCRBE-INSURANCE] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Relate ATEx as national one-off/experimental proof route. |
| France | 3. EU CPR / CE / product status | Reused products placed on market: steel, timber, concrete, connectors. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [FCRBE-PRODUCT-WASTE] | Proposed: `rb_bauproduktenverordnung_cpr` | Link France to CPR node. |
| France | 4. Decennial liability and insurance | Structural elements and inseparable works affecting stability or fitness. | Project edge only where contract/insurance/project source identifies the condition. | [FR-DECENNIAL], [FCRBE-INSURANCE] | Existing: `rb_gewaehrleistung` | Add France decennial liability metadata. |
| France | 5. Public procurement / AGEC circularity | Public construction, deconstruction, reuse and recycled-content criteria. | Project edge only where a tender/project source cites the requirement. | [FR-AGEC], [EU-GPP-BUILDINGS] | Existing: `rb_vergaberecht` | Add France AGEC/procurement metadata. |
| France | 6. Heritage protection | Monuments historiques and protected heritage fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [FR-CULTURE-HERITAGE] | Proposed: `rb_denkmalschutz` | Add France heritage metadata. |
| France | 7. Waste law vs product status / AGEC / PMCB | Dismantled components and construction products/materials moving through reuse channels. | Country-level metadata only unless a project source is available. | [FR-AGEC], [FCRBE-PRODUCT-WASTE] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| France | 8. PEMD diagnostic and RE2020 LCA | Products, equipment, materials and waste in major demolition/renovation; whole-building LCA for new buildings. | Project edge only where a source identifies a passport, inventory or report for that project. | [FR-PEMD], [FR-RE2020] | Proposed: `rb_materialpass` | Add `PEMD` as France-specific material-inventory child/note. |
| USA | 1. State/local building code / IBC-based approval | Reused structural steel, timber, concrete, masonry and connectors. | Country-level metadata only unless a project source is available. | [US-ICC-AMMR], [US-SE2050-SALVAGED] | Existing: `rb_bauordnungsrecht` | Add USA local-code metadata. |
| USA | 2. IBC 104.11 alternative materials and methods | Salvaged/reused structural products not prescriptively covered by code. | Country-level metadata only unless a project source is available. | [US-ICC-AMMR], [US-SE2050-SALVAGED] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as IBC alternative means/materials route. |
| USA | 3. US product-status route, no CPR | US listing/testing/ASTM/ICC-ES/engineer proof; CE/CPR not domestic law. | Country-level metadata only; project edge only if source cites product-status/marking route. | [US-ICC-AMMR] | CPR node not applicable | Do not attach CPR to USA; add country-specific product-status note. |
| USA | 4. Warranty and liability | All reused structural components; product/supplier/contractor allocation varies by state. | Project edge only where contract/insurance/project source identifies the condition. | [US-VENABLE-WARRANTY] | Existing: `rb_gewaehrleistung`, `rb_produkthaftung` | Add USA contract/product-liability metadata. |
| USA | 5. Public procurement / domestic preferences | Public works; steel and iron sourcing; sustainability and waste diversion criteria. | Project edge only where a tender/project source cites the requirement. | [US-FAR-BUYAMERICAN], [US-FHWA-BUYAMERICA] | Existing: `rb_vergaberecht` | Add USA procurement metadata. |
| USA | 6. Historic preservation | Historic properties, Section 106, state/local landmarks. | Project edge only with evidence that the specific building/component is protected or listed. | [US-NPS-NHPA], [US-ACHP-106] | Proposed: `rb_denkmalschutz` | Add USA heritage metadata. |
| USA | 7. Waste law / Boulder Ordinance 8366 | C&D waste and recovered elements; Boulder requires high diversion and deconstruction documentation. | Project-level edge supported for Boulder Community Hospital/city-owned site. | [US-BOULDER-REQ], [US-SE2050-BOULDER] | Existing: `rb_boulder_deconstruction_ordinance_8366` | Add country/city metadata and project edge to Boulder case. |
| USA | 8. Material passport / circularity reporting | Reuse inventories and local waste-diversion documentation; no general federal material-passport law. | Boulder case has stockpile/diversion documentation, not a universal passport duty. | [US-BOULDER-GUIDE], [US-SE2050-BOULDER] | Proposed: `rb_materialpass` | Use as project practice only if KG distinguishes voluntary inventory from legal obligation. |
| Finland | 1. Building Act / municipal approval | Reused structural steel, timber, concrete, masonry and assemblies. | Country-level metadata only unless a project source is available. | [FI-BUILDING-ACT] | Existing: `rb_bauordnungsrecht` | Add Finland building-approval metadata. |
| Finland | 2. Case-by-case technical proof | Non-standard reused structural elements requiring engineering and standards proof. | Country-level metadata only unless a project source is available. | [FI-BUILDING-ACT], [FI-SFS] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as municipal technical acceptance, not ZiE. |
| Finland | 3. EU CPR / CE / product status | Construction products placed on market; harmonised structural products. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [EU-CPR-COM] | Proposed: `rb_bauproduktenverordnung_cpr` | Link Finland to CPR node. |
| Finland | 4. Warranty and liability / YSE practice | All reused structural elements; quality assurance and hidden-defect risk. | Project edge only where contract/insurance/project source identifies the condition. | [FI-CHAMBERS] | Existing: `rb_gewaehrleistung` | Add Finland YSE/defects metadata. |
| Finland | 5. Public procurement | Public construction and deconstruction; circular/green criteria. | Project edge only where a tender/project source cites the requirement. | [FI-KEINO], [EU-GPP-BUILDINGS] | Existing: `rb_vergaberecht` | Add Finland procurement metadata. |
| Finland | 6. Built-heritage protection | Protected historic buildings and structural fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [FI-HERITAGE-ACT] | Proposed: `rb_denkmalschutz` | Add Finland heritage metadata. |
| Finland | 7. Waste law vs product status | C&D materials and dismantled components; waste/product distinction. | Country-level metadata only unless a project source is available. | [FI-WASTE-ACT], [FCRBE-PRODUCT-WASTE] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Finland | 8. Climate declaration / material report trajectory | Whole-building material data and structural components under low-carbon construction reforms. | Project edge only where a source identifies a passport, inventory or report for that project. | [FI-LOW-CARBON], [FI-BUILDING-ACT] | Proposed: `rb_materialpass` | Add Finland material-report metadata; verify transitional dates per project. |
| Denmark | 1. BR18 building approval | Reused structural steel, timber, concrete, masonry and assemblies. | Country-level metadata only unless a project source is available. | [DK-BR18], [DK-LCA] | Existing: `rb_bauordnungsrecht` | Add Denmark BR18 metadata. |
| Denmark | 2. Case-by-case municipal/technical acceptance | Non-standard reused structural elements requiring engineer proof and standards. | Country-level metadata only unless a project source is available. | [DK-BR18], [DK-STANDARDS] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as building-permit technical acceptance. |
| Denmark | 3. EU CPR / CE / product status | Construction products placed on market; structural products and kits. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [DK-NORDIC-REUSE] | Proposed: `rb_bauproduktenverordnung_cpr` | Link Denmark to CPR node. |
| Denmark | 4. Warranty and liability / AB18 | All reused structural components and contractor/supplier chains. | Project edge only where contract/insurance/project source identifies the condition. | [DK-AB18] | Existing: `rb_gewaehrleistung` | Add Denmark AB18/defects metadata. |
| Denmark | 5. Public procurement | Public buildings and circular construction material procurement. | Project edge only where a tender/project source cites the requirement. | [DK-NORDIC-CIRCULAR], [EU-GPP-BUILDINGS] | Existing: `rb_vergaberecht` | Add Denmark circular procurement metadata. |
| Denmark | 6. Heritage protection | Listed/protected buildings and structural fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [DK-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Denmark heritage metadata. |
| Denmark | 7. Waste law vs product status | C&D waste and reusable/recyclable construction products. | Country-level metadata only unless a project source is available. | [DK-NORDIC-REUSE] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Denmark | 8. BR18 LCA / material reporting | Whole-building LCA and material data; passports mostly voluntary/client-led. | Project edge only where a source identifies a passport, inventory or report for that project. | [DK-LCA], [DK-NORDIC-CIRCULAR] | Proposed: `rb_materialpass` | Add Denmark LCA/material-data metadata. |
| Norway | 1. TEK17 building approval | Reused structural steel, timber, concrete, masonry and products suitable for reuse/recovery. | Country-level metadata only unless a project source is available. | [NO-TEK17] | Existing: `rb_bauordnungsrecht` | Add Norway TEK17 metadata. |
| Norway | 2. Product documentation and local acceptance | Non-standard or non-CE-marked reused products requiring documented performance. | Country-level metadata only unless a project source is available. | [NO-DIBK-PRODUCTS], [NO-TEK17] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as documentation/acceptance route, not ZiE. |
| Norway | 3. EEA CPR / CE / AVCP product status | Construction products including non-CE-marked products sold in Norway. | Country-level metadata only; project edge only if source cites product-status/marking route. | [NO-DIBK-PRODUCTS], [EU-CPR-COM] | Proposed: `rb_bauproduktenverordnung_cpr` | Link Norway as EEA/CPR-related country metadata. |
| Norway | 4. Warranty and liability / NS contracts | All reused structural components under NS 8405/8407-type contracts. | Project edge only where contract/insurance/project source identifies the condition. | [NO-NS-OVERVIEW], [NO-CHAMBERS] | Existing: `rb_gewaehrleistung` | Add Norway NS contracts/defects metadata. |
| Norway | 5. Public procurement | Municipal/public circular construction material procurement. | Project edge only where a tender/project source cites the requirement. | [NO-PROCUREMENT], [DK-NORDIC-CIRCULAR] | Existing: `rb_vergaberecht` | Add Norway circular procurement metadata. |
| Norway | 6. Heritage protection | Protected cultural heritage buildings and fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [NO-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Norway heritage metadata. |
| Norway | 7. Waste law vs product status / reuse mapping | C&D waste; TEK17 waste plans and reuse/material recovery planning. | Country-level metadata only unless a project source is available. | [NO-TEK17] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Norway | 8. Material mapping / reuse reporting | Material mapping, waste plans and reusable components under TEK17 practice. | Project edge only where a source identifies a passport, inventory or report for that project. | [NO-TEK17], [NO-PROCUREMENT] | Proposed: `rb_materialpass` | Add Norway material-mapping metadata. |
| Japan | 1. Building Standards Act approval | Designated structural materials: steel, timber, concrete and major structural components. | Country-level metadata only unless a project source is available. | [JP-BSA], [JP-JTCCM] | Existing: `rb_bauordnungsrecht` | Add Japan building-law metadata. |
| Japan | 2. MLIT approval / JIS-JAS alternative | Designated materials not conforming to JIS/JAS or requiring approval. | Country-level metadata only unless a project source is available. | [JP-JTCCM], [JP-BSA] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as product/material approval route, not ZiE. |
| Japan | 3. Product status, no CPR | Japan uses JIS/JAS/MLIT approval and Building Standards Act; CPR not domestic. | Country-level metadata only; project edge only if source cites product-status/marking route. | [JP-JTCCM], [JP-BSA] | CPR node not applicable | Do not attach CPR to Japan. |
| Japan | 4. Housing warranty and liability | Major structural elements of new housing; foundations, columns, beams, load-bearing walls, roof trusses. | Project edge only where contract/insurance/project source identifies the condition. | [JP-HOUSING-WARRANTY] | Existing: `rb_gewaehrleistung` | Add Japan 10-year structural warranty metadata. |
| Japan | 5. Green public procurement | Public procurement of environmentally preferable goods/materials. | Project edge only where a tender/project source cites the requirement. | [JP-GREEN-PURCH], [JP-GREEN-BASIC] | Existing: `rb_vergaberecht` | Add Japan green procurement metadata. |
| Japan | 6. Cultural-property protection | Protected temples, shrines, historic timber/masonry/metal structures. | Project edge only with evidence that the specific building/component is protected or listed. | [JP-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Japan heritage metadata. |
| Japan | 7. Construction Material Recycling Law | Concrete, asphalt-concrete and wood materials; more recycling-focused than direct reuse. | Country-level metadata only unless a project source is available. | [JP-RECYCLING] | No dedicated node in prompt | Add waste/recycling metadata; no KrWG. |
| Japan | 8. Material passport / circularity reporting | No general material-passport duty identified; recycling and green procurement are reporting proxies. | Project edge only where a source identifies a passport, inventory or report for that project. | [JP-RECYCLING], [JP-GREEN-PURCH] | Proposed: `rb_materialpass` with caution | Add note: no general passport obligation found. |
| Luxembourg | 1. Municipal building permits | Reused structural steel, timber, concrete, masonry and façades. | Country-level metadata only unless a project source is available. | [LU-GUICHET-HOUSING], [LU-CE-STRATEGY] | Existing: `rb_bauordnungsrecht` | Add Luxembourg permit metadata. |
| Luxembourg | 2. Project-specific acceptance | Non-standard reused structural elements requiring engineer/permit/insurer acceptance. | Country-level metadata only unless a project source is available. | [LU-LIST-INVENTORY], [LU-CE-STRATEGY] | Existing generic by analogy: `rb_zulassung_im_einzelfall` | Model as project-specific technical acceptance. |
| Luxembourg | 3. EU CPR / CE / product status | Construction products placed on market; structural products and kits. | Country-level metadata only; project edge only if source cites product-status/marking route. | [EU-CPR-305], [EU-CPR-COM] | Proposed: `rb_bauproduktenverordnung_cpr` | Link Luxembourg to CPR node. |
| Luxembourg | 4. Decennial liability | Structural/shell elements and serious defects under civil-law liability. | Project edge only where contract/insurance/project source identifies the condition. | [LU-DECENNIAL] | Existing: `rb_gewaehrleistung` | Add Luxembourg decennial-liability metadata. |
| Luxembourg | 5. Public procurement / circular economy strategy | Public buildings, circular deconstruction and reusable-material procurement. | Project edge only where a tender/project source cites the requirement. | [LU-CE-METHODOLOGY], [LU-CE-STRATEGY] | Existing: `rb_vergaberecht` | Add Luxembourg circular procurement metadata. |
| Luxembourg | 6. Cultural heritage protection | Classified/protected buildings and historic fabric. | Project edge only with evidence that the specific building/component is protected or listed. | [LU-HERITAGE] | Proposed: `rb_denkmalschutz` | Add Luxembourg heritage metadata. |
| Luxembourg | 7. Waste law vs product status | Deconstruction materials; distinction between products/components that became waste and those that did not. | Country-level metadata only unless a project source is available. | [LU-CE-STRATEGY], [LU-LIST-INVENTORY] | No dedicated node in prompt | Add generic waste/product-status metadata. |
| Luxembourg | 8. Deconstruction inventories / material-passport logic | Whole-building inventories and reusable products/components. | Project edge only where a source identifies a passport, inventory or report for that project. | [LU-INVENTORY], [LU-LIST-INVENTORY] | Proposed: `rb_materialpass` | Add Luxembourg inventory/material-passport metadata. |


## Project-level relationship recommendations

| Project candidate | Legal condition node | Evidence basis | Recommended relationship |
|---|---|---|---|
| Boulder Community Hospital / Boulder city-owned site circular deconstruction case | `rb_boulder_deconstruction_ordinance_8366` | The SE2050 case study connects Boulder Ordinance 8366, the 75 percent diversion requirement, the hospital/city-owned site and stockpiled structural steel. Sources: [US-SE2050-BOULDER], [US-BOULDER-REQ]. | Add project-level edge such as `(:Projekt)-[:AFFECTED_BY]->(:RechtlicheBedingung {id:"rb_boulder_deconstruction_ordinance_8366"})`. |
| Boulder Community Hospital / city-owned site | `rb_materialpass` or inventory metadata | The case has diversion and stockpile documentation, but the sources do not show a legal material-passport obligation. | Prefer the Boulder ordinance edge. Add `rb_materialpass` only as voluntary/project-practice metadata if the KG distinguishes legal obligations from documentation practices. |
| UK Grade II/listed building projects | `rb_grade_ii_listing` | Only if the corpus source proves that the specific project/building is Grade II/listed. | Do not infer from country; project edge only with project evidence. |
| UK reused structural steel projects | `rb_ce_ukca_marking_reused_steel` | Only if the project/source discusses CE/UKCA/product-status or a steel reuse protocol for that project. | Otherwise country-level metadata only. |
| German projects using reused structural components | `rb_zulassung_im_einzelfall` and/or `rb_dibt_zustimmung` | Only if the project/source names ZiE, vBG, DIBt or the competent Land authority. | Otherwise country-level metadata only. |
| French demolition/renovation projects with PEMD | `rb_materialpass` | Only if the project/source states PEMD diagnostic or material inventory. | Use `rb_materialpass` with France attribute `PEMD`. |
| Dutch projects using Madaster/material passports | `rb_materialpass` | Only if the project/source names Madaster or a material passport. | Do not infer from national circular economy policy alone. |
| Norwegian projects with TEK17 material mapping | `rb_materialpass` | Only if the project/source includes waste plan, material mapping or reuse/recovery mapping for the project. | Otherwise country-level metadata only. |

## Modelling cautions

1. **Do not collapse national one-off routes into ZiE.** German ZiE/vBG, US IBC 104.11, French ATEx, Dutch equivalence, Swiss cantonal acceptance and Japanese MLIT material approval are related concepts but not identical.
2. **Separate legal obligation from enabling practice.** Madaster, Opalis, Rotor, SCI protocols and deconstruction inventories may support compliance, but they are not always legal obligations.
3. **Distinguish product from waste.** For EU countries, a reused element may remain a product if it never becomes waste; if it enters waste channels, preparation-for-reuse/end-of-waste reasoning may be needed.
4. **Keep material-specific nodes material-specific.** `rb_ce_ukca_marking_reused_steel` should not be reused for timber, concrete or masonry unless a separate source supports that extension.
5. **Use heritage project edges only with protected-building evidence.** Country heritage law alone is country metadata, not a project relationship.

## Evidence source bibliography

[BE-BRUSSELS-HERITAGE]: https://patrimoine.brussels/
[BE-BRUSSELS-PERMIT]: https://urbanisme.irisnet.be/lepermisdurbanisme
[BE-FLANDERS-HERITAGE]: https://www.onroerenderfgoed.be/
[BE-FLANDERS-OPALIS]: https://www.vlaanderen-circulair.be/en/node/58/opalis
[BE-FLANDERS-PERMIT]: https://www.vlaanderen.be/omgevingsvergunning
[BE-FPS-DECENNIAL]: https://economie.fgov.be/en/themes/financial-services/insurance/construction/decennial-civil-liability
[BE-OVAM]: https://ovam-english.vlaanderen.be/waste-and-materials
[BE-WALLONIA-HERITAGE]: https://agencewallonnedupatrimoine.be/
[BE-WALLONIA-PERMIT]: https://www.wallonie.be/fr/demarches/demander-un-permis-durbanisme
[CH-BAFU-CE]: https://www.bafu.admin.ch/bafu/en/home/topics/economy-consumption/info-specialists/circular-economy.html
[CH-BAFU-WASTE]: https://www.bafu.admin.ch/bafu/en/home/topics/waste.html
[CH-BKB]: https://www.bkb.admin.ch/bkb/en/home/themen/oeffentliches-beschaffungswesen.html
[CH-HERITAGE]: https://www.bak.admin.ch/bak/en/home/cultural-heritage.html
[CH-PERMIT]: https://www.ch.ch/en/housing/homeownership/building-and-renovating/building-permit/
[CH-SIA]: https://www.sia.ch/en/services/sia-norm/
[CH-SIA118-EXTRACT]: https://shop.sia.ch/f7c2ccee-9554-43f6-b952-ab9b8e93f251/F/DownloadAnhang
[DE-DGNB-PASS]: https://www.dgnb.de/de/themen/gebaeuderessourcenpass
[DE-DIBT]: https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg
[DE-KRWG]: https://www.gesetze-im-internet.de/krwg/BJNR021210012.html
[DE-MBO]: https://www.bauministerkonferenz.de/Dokumente/42323066.pdf
[DE-UBA-WASTE]: https://www.umweltbundesamt.de/themen/abfall-ressourcen/abfallwirtschaft/abfallrecht
[DK-AB18]: https://www.byggerietsregler.dk/wp-content/uploads/2020/04/UK-AB18.pdf
[DK-BR18]: https://bygningsreglementet.dk/
[DK-HERITAGE]: https://slks.dk/english/work-areas/architecture/listed-buildings/
[DK-LCA]: https://help.oneclicklca.com/en/articles/275707-denmark-bygningsreglementet-br18-and-lca
[DK-NORDIC-CIRCULAR]: https://pub.norden.org/nord2024-029/
[DK-NORDIC-REUSE]: https://pub.norden.org/us2023-441/us2023-441.pdf
[DK-STANDARDS]: https://www.ds.dk/en
[EU-CE-ACTION]: https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52020DC0098
[EU-CPR-305]: https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32011R0305
[EU-CPR-COM]: https://single-market-economy.ec.europa.eu/sectors/construction/construction-products-regulation-cpr_en
[EU-GPP-BUILDINGS]: https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2022-03/GPP_Buildings_TR_v1.01.pdf
[EU-TAXONOMY-RENOVATION]: https://ec.europa.eu/sustainable-finance-taxonomy/activities/activity/351/view
[FCRBE-FINAL]: https://vb.nweurope.eu/media/21554/fcrbe_final-report_ve.pdf
[FCRBE-INSURANCE]: https://opalis.eu/sites/default/files/2024-04/Prospective%20report%20on%20reuse%20and%20insurance%20-%20EN.pdf
[FCRBE-PRODUCT-WASTE]: https://opalis.eu/sites/default/files/2022-02/FCRBE-booklet-04-Product_waste-EN_0.pdf
[FI-BUILDING-ACT]: https://ym.fi/en/the-reform-of-the-land-use-and-building-act
[FI-CHAMBERS]: https://practiceguides.chambers.com/practice-guides/construction-law-2025/finland/trends-and-developments
[FI-HERITAGE-ACT]: https://www.finlex.fi/en/laki/kaannokset/2010/en20100498
[FI-KEINO]: https://www.hankintakeino.fi/en
[FI-LOW-CARBON]: https://ym.fi/en/low-carbon-construction
[FI-SFS]: https://sfs.fi/en/standards/
[FI-WASTE-ACT]: https://www.finlex.fi/en/laki/kaannokset/2011/en20110646
[FR-AGEC]: https://circulareconomy.europa.eu/platform/en/strategies/french-act-law-against-waste-and-circular-economy
[FR-CSTB-ATEX]: https://www.cstb.fr/en/evaluation/atex/
[FR-CULTURE-HERITAGE]: https://www.culture.gouv.fr/Thematiques/monuments-sites
[FR-DECENNIAL]: https://www.franceassureurs.fr/wp-content/uploads/how-decennial-liability-insurance-work.pdf
[FR-PEMD]: https://www.ecologie.gouv.fr/politiques-publiques/diagnostic-produits-equipements-materiaux-dechets-pemd
[FR-RE2020]: https://www.ecologie.gouv.fr/politiques-publiques/reglementation-environnementale-re2020
[JP-BSA]: https://www.japaneselawtranslation.go.jp/en/laws/view/4024/en
[JP-GREEN-BASIC]: https://www.env.go.jp/en/laws/policy/green/h31bp_en.pdf
[JP-GREEN-PURCH]: https://www.env.go.jp/content/000064788.pdf
[JP-HERITAGE]: https://www.bunka.go.jp/english/policy/cultural_properties/
[JP-HOUSING-WARRANTY]: https://www.how.or.jp/information/docs/Housing%20Warranty%20Scheme%20in%20Japan%20_EN_2024.pdf
[JP-JTCCM]: https://www.jtccm.or.jp/english/overview
[JP-RECYCLING]: https://www.env.go.jp/content/900452889.pdf
[LU-CE-METHODOLOGY]: https://economie-circulaire.public.lu/en/strategy/methodology.html
[LU-CE-STRATEGY]: https://economie-circulaire.public.lu/dam-assets/publications/2021/Strategy-circular-economy-Luxembourg-EN.pdf
[LU-DECENNIAL]: https://www.lalux.lu/fileadmin/mediatheque/documents/compliance/ipid/ipid_aprobat_rc-decennale_en.pdf
[LU-GUICHET-HOUSING]: https://guichet.public.lu/en/citoyens/logement.html
[LU-HERITAGE]: https://guichet.public.lu/en/citoyens/loisirs/culture/patrimoine-culturel/classement-batiment-patrimoine-culturel-national.html
[LU-INVENTORY]: https://luxinnovation.lu/news/reusing-construction-materials-the-ball-is-in-the-middle-of-the-field
[LU-LIST-INVENTORY]: https://www.list.lu/media-event/news/news-detail/towards-a-circular-construction
[NL-BBL-IPLO]: https://iplo.nl/regelgeving/omgevingswet/inhoud/besluit-bouwwerken-leefomgeving/
[NL-CMS-PL]: https://cms.law/en/int/expert-guides/expert-guide-to-product-liability-and-warranty-litigation/netherlands
[NL-GOV-CE]: https://www.government.nl/themes/economy/sustainable-economy/circular-economy-by-2050
[NL-HERITAGE]: https://english.cultureelerfgoed.nl/
[NL-MADASTER]: https://madaster.com/material-passport/
[NL-NEN]: https://www.nen.nl/en/building-and-construction
[NL-PIANOO]: https://www.pianoo.nl/en/sustainable-public-procurement
[NO-CHAMBERS]: https://practiceguides.chambers.com/practice-guides/comparison/960/16313/25544-25545-25546-25547-25548-25549-25550-25551-25552-25553
[NO-DIBK-PRODUCTS]: https://www.dibk.no/byggevarer/pcp-construction-norway
[NO-HERITAGE]: https://www.riksantikvaren.no/en/
[NO-NS-OVERVIEW]: https://www.dalan.no/en/property/construction-law/legal-aspects-of-construction-contracts/
[NO-PROCUREMENT]: https://www.anskaffelser.no/en/english/npcp/nordic-network-circular-construction-materials
[NO-TEK17]: https://www.dibk.no/globalassets/byggeregler/regulation-on-technical-requirements-for-construction-works--technical-regulations.pdf
[OPALIS-ABOUT]: https://opalis.eu/en/about
[UK-APPROVED-DOCS]: https://www.gov.uk/government/collections/approved-documents
[UK-CE-UKCA]: https://www.gov.uk/guidance/placing-ukca-or-ce-marked-products-on-the-market-in-great-britain
[UK-CONSTRUCTION-PLAYBOOK]: https://www.gov.uk/government/publications/the-construction-playbook
[UK-GOV-CPR]: https://www.gov.uk/guidance/construction-products-regulation-in-great-britain
[UK-HISTORIC-ENGLAND]: https://historicengland.org.uk/listing/what-is-designation/listed-buildings/
[UK-SCI-STEEL]: https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf
[UK-WASTE-DOC]: https://www.gov.uk/government/publications/waste-duty-of-care-code-of-practice
[UKGBC-CE]: https://ukgbc.org/our-work/topics/circular-economy/
[US-ACHP-106]: https://www.achp.gov/protecting-historic-properties/section-106-process/introduction-section-106
[US-BOULDER-GUIDE]: https://bouldercolorado.gov/deconstruction-requirements-guide
[US-BOULDER-REQ]: https://bouldercolorado.gov/services/sustainable-deconstruction-requirements
[US-FAR-BUYAMERICAN]: https://www.acquisition.gov/far/52.225-21
[US-FHWA-BUYAMERICA]: https://www.fhwa.dot.gov/construction/contracts/buyam_qageneral.cfm
[US-ICC-AMMR]: https://media.iccsafe.org/Annual/2016/Alternate-Means-and-Materials-for-Code-Compliance.pdf
[US-NPS-NHPA]: https://www.nps.gov/subjects/historicpreservation/national-historic-preservation-act.htm
[US-SE2050-BOULDER]: https://se2050.org/wp-content/uploads/2024/07/SEI-CE-WG-Circular-Economy-Case-Studies_2-Boulder-Community-Hospital.pdf
[US-SE2050-SALVAGED]: https://se2050.org/wp-content/uploads/2021/09/Webster-The-Use-of-Salvaged-Structural-Materials-in-New-Construction.pdf
[US-VENABLE-WARRANTY]: https://www.venable.com/-/media/files/services/design-build/construction-law-other-issues/47--contractors_constructionv1.pdf
