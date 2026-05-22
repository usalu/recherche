# Bauteilbörse graph — deeper evidence-backed audit run 02

**Date:** 2026-06-02  
**Input graph:** `bauteilboerse_network_2026-06-01.json`  
**Rule for this run:** only propose a correction when the evidence is written directly beside it. If evidence is weak, keep the graph unchanged and mark it as unresolved.

## 1. Current graph state inspected

### Restado

```text
Node `software_restado`: labels=['Software']; name=Restado; url=
  BELEGT_IN -> `q_url_8ed7711262fc72b1eb28d846be8981ff` (['Quelle', 'ExternalLink']; https://restado.de/ueber-restado)
  BELEGT_IN -> `q_url_32f86a870f48e21d1daf42d048a96207` (['Quelle', 'ExternalLink']; https://restado.de/materialreste)
  BELEGT_IN -> `q_url_fc7f92d974b8d75720332cdbc9744048` (['Quelle', 'ExternalLink']; https://restado.de/hilfe/impressum)
  BELEGT_IN -> `q_url_f306d0d30b5b4a88a2eb959bccbf7682` (['Quelle', 'ExternalLink']; https://restado.de/haendler-auf-restado-werden)
  BELEGT_IN -> `q_impact_hub_berlin_crclr_fitout_md` (['Quelle', 'Dossier']; Impact_Hub_Berlin_CRCLR_…)
  BELEGT_IN -> `q_research_restado_md` (['ResearchDocument', 'Quelle']; restado)
  BELEGT_IN -> `q_url_74e67b64770f2741ee9cce15ef3ac2ad` (['Quelle', 'ExternalLink']; https://restado.de/)
  BETRIEBEN_VON -> `concular` (['Akteur']; Concular)
  GEHÖRT_ZU -> `land_deutschland` (['Land']; Deutschland)
  HAT_AKTEURROLLE -> `ar_materialbroker` (['Akteurrolle']; Materialbroker / Reuse-Marketplace-Betreiber)
  … 21 more edges
```

### Opalis actor

```text
Node `opalis`: labels=['Akteur']; name=Opalis; url=
  ANCHORED_BY -> `q_akteursliste_master_md` (['OntologyAnchor']; akteursliste_master.md)
  BELEGT_IN -> `q_akteursliste_master_md` (['OntologyAnchor']; akteursliste_master.md)
  GEHÖRT_ZU -> `land_belgien` (['Land']; Belgien)
  HAT_AKTEURROLLE -> `ar_materialbroker` (['Akteurrolle']; Materialbroker / Reuse-Marketplace-Betreiber)
  HAT_AKTEURROLLE -> `ar_forschung_dokumentation` (['Akteurrolle']; Forschung_Dokumentation)
  HAT_AKTEURROLLE -> `ar_materiallieferung_markt` (['Akteurrolle']; Materiallieferung_Markt)
  HAT_AKTEURROLLE -> `ar_reuse_zirkularitaetsberatung` (['Akteurrolle']; Reuse_Zirkularitaetsberatung)
  HAT_AKTEURTYP -> `at_software_tool_anbieter` (['Akteurtyp']; Software_Tool_Anbieter)
  LIEGT_IN_LAND -> `land_belgien` (['Land']; Belgien)
  VERBUNDEN_MIT_AKTEUR <- `Rotor` (['Akteur']; Rotor)
  … 3 more edges
```

### Opalis software

```text
Node `software_opalis`: labels=['Software']; name=Opalis; url=
  NUTZT_SOFTWARE <- `Rotor` (['Akteur']; Rotor)
```

### Concular

```text
Node `concular`: labels=['Akteur']; name=Concular; url=
  ANCHORED_BY -> `q_akteursliste_master_md` (['OntologyAnchor']; akteursliste_master.md)
  BELEGT_IN -> `q_awm_muenster_circular_office_md` (['Quelle', 'Dossier']; AWM_Muenster_Circular_Of…)
  BELEGT_IN -> `q_akteursliste_master_md` (['OntologyAnchor']; akteursliste_master.md)
  BELEGT_IN -> `q_actor_annabelle_von_reutern_02` (['Quelle', 'ExternalLink']; Concular)
  BETEILIGT_AN -> `bg_reuse_glas_mehrere_awm_partitions_doors` (['Bauteilgruppe']; Glass partitions and…)
  BETEILIGT_AN -> `bg_reuse_kunststoff_wand_awm_wc_partitions` (['Bauteilgruppe']; WC partitions)
  BETEILIGT_AN -> `p_crclr_house_impact_hub_berlin` (['Projekt']; CRCLR House)
  BETEILIGT_AN -> `p_awm_muenster_circular_office` (['Projekt']; AWM Münster – zirkulärer…)
  BETEILIGT_AN <- `dominik_campanella` (['Akteur']; Dominik Campanella)
  BETEILIGT_AN <- `julius_schaeufele` (['Akteur']; Julius Schäufele)
  … 24 more edges
```

### Material Index

```text
Node `material_index`: labels=['Akteur']; name=Material Index; url=
  BELEGT_IN -> `q_research_material_index_md` (['ResearchDocument', 'Quelle']; material-index)
  BELEGT_IN -> `q_url_1fdec6782bfebc0692e032972d002955` (['Quelle', 'ExternalLink']; https://material-index.co.uk/)
  BELEGT_IN -> `q_url_c44bdb40f60f1dfb46a1204152587eb0` (['Quelle', 'ExternalLink']; https://material-index.exchange/edits)
  BELEGT_IN -> `q_url_62219abd0009abf5cb3a47469b8dae4a` (['Quelle', 'ExternalLink']; https://www.material-index.co.uk/materials/material-specification)
  BELEGT_IN -> `q_url_df9716f7281bd5c21ee21c219edea46a` (['Quelle', 'ExternalLink']; https://asbp.org.uk/member/material-index)
  BELEGT_IN -> `q_url_cc0ace378d64495001aab9ca672fd329` (['Quelle', 'ExternalLink']; https://material-index.exchange/terms-and-conditions)
  HAT_AKTEURROLLE -> `ar_materialbroker` (['Akteurrolle']; Materialbroker / Reuse-Marketplace-Betreiber)
  HAT_AKTEURROLLE -> `ar_aufbereitung_refurbishment` (['Akteurrolle']; Aufbereitung_Refurbishment)
  HAT_AKTEURROLLE -> `ar_forschung_dokumentation` (['Akteurrolle']; Forschung_Dokumentation)
  HAT_AKTEURROLLE -> `ar_rueckbau_bauteilernte_logistik` (['Akteurrolle']; Rueckbau_Bauteilernte_Logistik)
  … 19 more edges
```

### Marktmodell Plattform-Kauf

```text
Node `mm_plattform_vermittelt`: labels=['Marktmodell']; name=Plattform-Kauf; url=
  HAT_MARKTMODELL <- `baumatpool_ch` (['Akteur']; Baumatpool.ch)
  HAT_MARKTMODELL <- `bg_reuse_stahl_mehrere_awm_cable_trays_shelves_lights` (['Bauteilgruppe']; Cable trays as shelves…)
  HAT_MARKTMODELL <- `bg_reuse_glas_mehrere_awm_partitions_doors` (['Bauteilgruppe']; Glass partitions and…)
  HAT_MARKTMODELL <- `bg_reuse_kunststoff_wand_awm_wc_partitions` (['Bauteilgruppe']; WC partitions)
  HAT_MARKTMODELL <- `bg_reuse_holz_ausbau_awm_fixed_builtins` (['Bauteilgruppe']; Wood for fixed built-ins)
  HAT_MARKTMODELL <- `bg_reuse_holz_wand_awm_cladding_old_chairs` (['Bauteilgruppe']; Fixed wall cladding…)
  HAT_MARKTMODELL <- `bg_reuse_holz_tuer_chiro_external` (['Bauteilgruppe']; Außentüren)
  HAT_MARKTMODELL <- `bg_reuse_ziegel_mehrere_chiro_facade` (['Bauteilgruppe']; Fassadenziegel (Chiro))
  HAT_MARKTMODELL <- `bg_reuse_keramik_boden_chiro_tiles` (['Bauteilgruppe']; Bodenfliesen)
  HAT_MARKTMODELL <- `bg_reuse_unbekannt_technik_chiro_luminaires` (['Bauteilgruppe']; Leuchten)
  … 50 more edges
```

## 2. Corrections / expansions with direct evidence

### 2.1 Restado current node `software_restado` — MUST CORRECT / clarify

**Finding:** Restado is strongly evidenced as an online marketplace / material catalogue for physical building materials. It is **not** evidenced as a standalone SaaS/inventory software product like Madaster or Loopfront. The graph can keep a digital-platform representation, but the property/role should say online marketplace / building-material catalogue, not generic software provider.


**Graph action:** No schema change. Add or prefer an `Akteur` node `restado` if the graph needs actors; keep `software_restado` only as the digital marketplace interface. Keep `BETRIEBEN_VON -> Concular`, but avoid `NUTZT_SOFTWARE` wording that makes Concular appear merely a software user.


**Direct evidence written here:**

- **Restado homepage** — https://restado.de/  
  Evidence: Direct text: `Der Marktplatz für zirkuläre Baustoffe. Für gewerbliche Käufer.` It lists categories such as Türen & Zargen, Fenster, Fliesen & Steine, Dach, Rohbau, Fassade, Innenausbau.

- **Restado homepage** — https://restado.de/  
  Evidence: Direct text: `Deutschlandweit über 1 Millionen Baustoffe - für gewerbliche Käufer.`

- **Restado dealer page** — https://restado.de/haendler-auf-restado-werden/  
  Evidence: Direct text: `Mit restado verkaufst Du auf Europas größten Marktplatz für wiedergewonnene Baustoffe.`

- **Restado dealer page** — https://restado.de/haendler-auf-restado-werden/  
  Evidence: Direct text: sellers can offer materials from Rückbau, Restposten, B-Ware, übriggeblieben auf Baustellen, and new ecological materials.

- **Restado story page** — https://restado.de/restado-die-story/  
  Evidence: Direct text: Restado says it built a website and put rescued building materials online; later it says Concular became the platform for circular construction processes.



### 2.2 Opalis current actor/software/market-model mapping — MUST CORRECT / clarify

**Finding:** Opalis is evidenced as a directory / knowledge and documentation platform around professional reuse dealers, not as a direct purchase marketplace. The graph should not attach Opalis to `Plattform-Kauf` unless there is direct purchase/listing evidence inside Opalis itself.


**Graph action:** No schema change. Keep `opalis` as `Akteur`; keep/rename `software_opalis` only if it means web directory/database. Remove or downgrade links to marketplace-purchase roles/model. Prefer `Forschung_Dokumentation`, `Akteurverzeichnis`, or equivalent existing role if available.


**Direct evidence written here:**

- **Opalis about** — https://opalis.eu/en/about  
  Evidence: Direct text: `This site presents an inventory of the professional dealers in salvaged building materials.`

- **Opalis dealers list** — https://opalis.eu/en/dealers/list  
  Evidence: Direct evidence: the page is a list of dealers with filterable entries, not a checkout or seller listing system.

- **Opalis about** — https://opalis.eu/en/about  
  Evidence: Direct text: Opalis was started in 2012 as an initiative of Rotor and provides information, case studies and documentation around reuse.



### 2.3 Madaster missing as software/material-passport system — MUST ADD / high confidence

**Finding:** Madaster is missing from the graph as a strong digital material-passport / building cadastre system. It should not be modelled as a marketplace unless a separate marketplace source is found.


**Graph action:** No schema change. Add `Software` node `software_madaster` and/or `Akteur` node `madaster`; connect to `Software_Digitalisierung`, `Materialpass`, `Gebaeuderessourcenpass`, `Materialinventur`, `Digitale_Dokumentation` using existing labels/edge types. Do **not** connect to `Plattform-Kauf` without separate evidence.


**Direct evidence written here:**

- **Madaster material passport** — https://madaster.com/material-passport/  
  Evidence: Direct text: `A material passport is a comprehensive digital record detailing the composition and reuse potential of materials within a building.`

- **Madaster material passport** — https://madaster.com/material-passport/  
  Evidence: Direct text: Madaster records materials/products in a building, including quality, origin and disassemblability.

- **Madaster platform menu** — https://madaster.com/material-passport/  
  Evidence: Direct evidence: platform features include Material passport, Circularity Insights, Product registration, Life cycle assessments, Portfolio performance, Asset valuation.



### 2.4 Loopfront missing as reuse platform/software — MUST ADD / high confidence

**Finding:** Loopfront is a strong missing software/platform case because it directly combines resource inventory, reuse surveys, marketplace and tracking.


**Graph action:** No schema change. Add `Software` node `software_loopfront` and `Akteur` node `loopfront` if actor/software separation is used. Connect to `Software_Digitalisierung`, `Materialinventur`, `Bauteilkatalogisierung`, `Marktplatz/Plattform-Kauf` only with evidence note that Loopfront has internal/external marketplace functions.


**Direct evidence written here:**

- **Loopfront product page** — https://www.loopfront.com/product  
  Evidence: Direct text: `Full overview of all available resources ranging from building materials to furniture.`

- **Loopfront product page** — https://www.loopfront.com/product  
  Evidence: Direct text: `Manage inventory and materials in storage or at locations.`

- **Loopfront product page** — https://www.loopfront.com/product  
  Evidence: Direct text: marketplace function allows acquiring materials on internal and external marketplace; excess materials can be placed there for reuse.

- **Loopfront product page** — https://www.loopfront.com/product  
  Evidence: Direct text: Loopfront supports QR/floor-plan material tracking and reuse surveying.



### 2.5 Material Reuse Portal missing as aggregator platform — MUST ADD / high confidence

**Finding:** The Material Reuse Portal is a distinct missing platform type: an aggregator across multiple marketplaces, not a depot and not a single-inventory shop.


**Graph action:** No schema change. Add `Software` or `Akteur` node `material_reuse_portal` with actor ReLondon if desired. Connect to `Software_Digitalisierung`, `Akteurverzeichnis`/service-provider directory if available, `Marktplatz_Aggregator` only if already present; otherwise use existing `HAT_MARKTMODELL` with comment `aggregator, not direct seller`.


**Direct evidence written here:**

- **UKGBC solution page** — https://ukgbc.org/resources/aggregated-material-reuse-marketplace/  
  Evidence: Direct text: `Aggregating data from multiple marketplaces to create a single platform where reusable construction materials can be found.`

- **UKGBC solution page** — https://ukgbc.org/resources/aggregated-material-reuse-marketplace/  
  Evidence: Direct text: the Portal uses an aggregator approach to simplify finding materials; it can include new material data sources over time.

- **UKGBC solution page** — https://ukgbc.org/resources/aggregated-material-reuse-marketplace/  
  Evidence: Direct text: `The Material Reuse Portal is free to use.` Company name: ReLondon; UK availability: Yes; launch date: December 2022.



### 2.6 RAEDIFICARE missing as marketplace + service platform — MUST ADD / high confidence

**Finding:** RAEDIFICARE is a strong missing French professional BTP reuse marketplace and service ecosystem, with both catalogue/listing and diagnostic/AMO service dimensions.


**Graph action:** No schema change. Add `Akteur` node `raedificare` and, if separating software, `Software` node `software_raedificare_marketplace`. Connect to `Materialbroker / Reuse-Marketplace-Betreiber`, `Reuse_Zirkularitaetsberatung`, `Software_Digitalisierung`, `Materialinventur`, `Pre_Deconstruction_Audit`/`Diagnostic PEMD` if existing nodes allow.


**Direct evidence written here:**

- **RAEDIFICARE marketplace** — https://raedificare.com/marketplace/  
  Evidence: Direct text: `La market place de don et de vente en ligne de matériaux de réemploi du BTP.`

- **RAEDIFICARE marketplace** — https://raedificare.com/marketplace/  
  Evidence: Direct text: connects materials available on construction sites, demolition-bound buildings and surplus orders to buyers/projects across the territory.

- **RAEDIFICARE marketplace** — https://raedificare.com/marketplace/  
  Evidence: Direct evidence: browsing catalogue, advanced search, online messaging, catalogues/need alerts, catalog creation, listing materials, publishing online.

- **RAEDIFICARE marketplace** — https://raedificare.com/marketplace/  
  Evidence: Direct text: no buyer commission; no sales commission; catalogues can be imported/exported in CSV/XLS/PDF; environmental balance can be generated.



### 2.7 ReUse and Trade missing as online shop/catalogue pattern — ADD / medium-high confidence

**Finding:** ReUse and Trade is a missing German online catalogue/shop, but its visible current stock is mainly furniture/equipment/sanitary/household/garden categories rather than a broad structural building-component exchange.


**Graph action:** No schema change. Add `Akteur` node `reuse_and_trade` with a cautious component scope: furniture/equipment/interior/sanitary/garden/DIY. Avoid marking as structural-material exchange unless structural listings are directly found.


**Direct evidence written here:**

- **ReUse and Trade article overview** — https://www.reuseandtrade.de/artikeluebersicht/Schnaeppchen-fuer-Privatkunden.aspx  
  Evidence: Direct evidence: the page has login/account, catalogue overview, article overview, shopping cart, comparison list and wishlist.

- **ReUse and Trade article overview** — https://www.reuseandtrade.de/artikeluebersicht/Schnaeppchen-fuer-Privatkunden.aspx  
  Evidence: Direct evidence: visible categories include Elektrogeräte, Garten & Terrasse, Handwerk/Heimwerken, Heizung/Sanitär, Haushaltsgeräte, Möbel und Accessoires.

- **ReUse and Trade article overview** — https://www.reuseandtrade.de/artikeluebersicht/Schnaeppchen-fuer-Privatkunden.aspx  
  Evidence: Direct evidence: visible product listings show price, VAT, quantity, dimensions and pickup/availability information.



### 2.8 Material Index existing node — KEEP, but evidence supports narrowing wording

**Finding:** Material Index is already present and the graph’s broad service/software/market roles are mostly evidence-supported. The only caution is to phrase it as audit + platform + broker/exchange, not only as a generic multi-vendor marketplace.


**Graph action:** No schema change. Keep Material Index, but set evidence notes: `audit/passport/exchange/tracking + marketplace/broker`. The `SaaS-Inventarplattform` edge can remain with `wahrscheinlich` or be upgraded only if the graph accepts official site text as enough evidence.


**Direct evidence written here:**

- **Material Index audits page** — https://material-index.co.uk/audits  
  Evidence: Direct text: Material Index offers circular-economy services with auditing, reuse consultancy and material exchange teams.

- **Material Index audits page** — https://material-index.co.uk/audits  
  Evidence: Direct text: audits are delivered through a digital AI-enabled platform capturing component-level data with environmental analytics.

- **Material Index audits page** — https://material-index.co.uk/audits  
  Evidence: Direct text: every audit includes access to the Material Index Marketplace where materials can be sold or donated.

- **Material Index audits page** — https://material-index.co.uk/audits  
  Evidence: Direct text: Material Index can act as material broker, connecting clients with Exchange Partners.



### 2.9 Concular core actor — KEEP / no new correction without more evidence

**Finding:** Concular as a circular-building service/platform actor is evidenced, and its link to Restado is plausible. The unsafe part is only the wording that treats Restado as generic software that Concular `uses` rather than a marketplace operated/connected to Concular.


**Graph action:** No schema change. Keep Concular. Prefer `BETRIEBEN_VON` Restado -> Concular or a neutral `VERBUNDEN_MIT_AKTEUR` connection. Avoid extra software-use edges unless Concular page explicitly says it uses that tool.


**Direct evidence written here:**

- **Restado story page** — https://restado.de/restado-die-story/  
  Evidence: Direct text: Concular was started in 2020 and became a platform enabling circular construction processes.

- **Concular navigation** — https://concular.de/warum-zirkulaeres-bauen-ein-gemeinschaftsprojekt-ist-und-was-concular-dafuer-tut/  
  Evidence: Direct evidence: Concular has sections for Rückbau, Bestand, Neubau, Material-Shop, CircularLCA, digital building resource pass, urban mining cadastre and advisory services.

- **Restado homepage** — https://restado.de/  
  Evidence: Direct evidence: Restado links users to Concular for circular construction, material passports, dismantling firms and material brokerage.



## 3. Graph patch list, without schema change

These are patch instructions, not a new schema. They use existing node labels and relationship types already visible in the graph.


### A. Edits to existing graph

1. `software_restado`: change description/kind to `online marketplace / material catalogue for reclaimed and surplus building materials`. Keep only if the graph models websites/platforms as software. Add evidence URLs from Restado homepage, dealer page and story page.

2. `software_restado -> concular` with `BETRIEBEN_VON`: keep as evidenced, but avoid adding/repeating `NUTZT_SOFTWARE` Restado/Concular edges unless the graph explicitly distinguishes `operated software` from `software used by actor`.

3. `opalis` and `software_opalis`: change/downgrade market model to `directory / dealer inventory / documentation`. Remove `Plattform-Kauf` unless direct buy/sell evidence is found on Opalis itself.

4. `material_index`: keep existing broad roles, but annotate as `audit + platform + material broker + marketplace access` rather than only `multi-vendor marketplace`.


### B. Additions, same schema

1. Add `software_madaster` / `madaster`: digital material passport, circularity insights, product registration, LCA, portfolio performance, asset valuation. Do not mark as direct marketplace.

2. Add `software_loopfront` / `loopfront`: resource inventory, reuse survey, internal/external marketplace, QR/floor-plan tracking, reports.

3. Add `material_reuse_portal`: aggregator platform across multiple marketplaces; operator/source ReLondon/UKGBC evidence.

4. Add `raedificare`: French BTP reuse marketplace + PEMD/diagnostic/AMO/service platform.

5. Add `reuse_and_trade`: online catalogue/shop, but with cautious scope: office/furniture/equipment/sanitary/DIY visible stock.

6. ReSource Marktplaats and Globechain still need a fresh source pass before graph patching; do not add them from memory.


## 4. Explicit non-corrections / things not to invent

- Do **not** call Restado a physical depot unless an evidence source shows Restado operates its own depot/warehouse. Current evidence supports an online marketplace/catalogue for physical materials.

- Do **not** call Opalis a purchase marketplace unless direct checkout/listing evidence is found. Current evidence supports dealer directory and documentation.

- Do **not** connect Madaster to `Plattform-Kauf`; its direct evidence is material passport/cadastre/data platform.

- Do **not** upgrade ReUse and Trade to structural-material marketplace based only on visible current listings; visible evidence points mainly to equipment/furniture/sanitary/DIY categories.

- Do **not** remove uncertain nodes solely because earlier checks were inconsistent. Keep them with lower confidence until contradicted by evidence.


## 5. What needs one more direct-source pass

1. `ReSource Marktplaats`: verify from official app/website whether it is still live, what geography it covers, and whether it is an exchange app, marketplace or inventory tool.

2. `Globechain`: verify construction-specific function and current inventory categories from official pages that are readable without login.

3. `ReUse and Trade`: inspect deeper categories/pages for any structural components beyond the visible furniture/equipment listings.

4. `Restado`: if you want to model it as `Software`, add a note that this means `web marketplace interface`, not SaaS or internal inventory software.
