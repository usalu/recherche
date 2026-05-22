# Projects — Research Relevance Overview

**Scope:** Real-world building case studies in the corpus on **Direct Reuse of building
components** (*Bauteilwiederverwendung* / circular construction). Each project models reused
**fixed/structural components** — not loose furniture, generic recycled material, or mere
existing-building retention (*Bestandserhalt*), which are tracked separately.

**How relevance is scored.** Every `Projekt` node carries a `bewertung` (1–5). It expresses how
strong and well-evidenced the project is *as a direct-reuse case*, not how famous the building is:

| `bewertung` | Tier | Meaning |
|:---:|---|---|
| ★★★★★ 5 | Primary cases | Strongest, best-evidenced main cases (*Hauptfälle*) |
| ★★★★ 4 | Strong cases | Solid main / comparison cases with documented reuse |
| ★★★ 3 | Comparison & watchlist | Useful comparators; some still planned/not as-built |
| ★★ 2 | Appendix / concept | Pavilions, demonstrators, unbuilt or thin-evidence cases |

- **Corpus:** 74 projects · user-confirmed through `batch_015`.
- **Distribution:** 7 × ★★★★★ · 24 × ★★★★ · 28 × ★★★ · 15 × ★★.
- **Source records:** [`_neo4j/processed/projects/records/`](../../_neo4j/processed/projects/records/) (one `.kg.jsonl` per project).

---

## Tier 1 — Primary cases (★★★★★)

The seven core anchors of the research. These carry the most defensible structural / fixed-component
reuse evidence.

| Project | Location | Year | Why it matters | Record |
|---|---|:---:|---|---|
| **K.118 / Kopfbau Halle 118** | Winterthur, CH | 2021 | Flagship case: 3-storey extension built from **transferred** components (not just retained Halle 118). ~494 t CO₂ saved, 59% reduction; reuse 14% by weight / 41% by volume. | [file](../../_neo4j/processed/projects/records/p_k118_kopfbau_halle_118_winterthur.kg.jsonl) |
| **BedZED** (Beddington Zero Energy Dev.) | London, UK | 2002 | Early mixed-use eco-quarter; scoring rests on reused **structural steel** and fixed components, not general recycled material. | [file](../../_neo4j/processed/projects/records/p_bedzed_london_hackbridge.kg.jsonl) |
| **BioPartner 5** | Leiden / Oegstgeest, NL | — | ~165 t **reused steel** as the central robust value (sources cite 150–170 t); ~40% CO₂ reduction. Furniture excluded from direct reuse. | [file](../../_neo4j/processed/projects/records/p_biopartner_5_leiden_oegstgeest.kg.jsonl) |
| **KA13 / Kristian Augusts gate 13** | Oslo, NO | 2021 | Large-scale FutureBuilt pilot (4,297 m²): ex-situ hollow-core slabs + steel reuse; ~70% CO₂ reduction. Retention tracked separately. | [file](../../_neo4j/processed/projects/records/p_ka13_kristian_augusts_gate_13_oslo.kg.jsonl) |
| **Recypark Demets / Anderlecht** | Brussels, BE | 2024 | Public recycling park (5,000 m²) built around reused **glulam arches** salvaged from a riding hall. | [file](../../_neo4j/processed/projects/records/p_recypark_demets_anderlecht.kg.jsonl) |
| **Svanen / The Swan Kindergarten** | Gladsaxe, DK | 2022 | Municipal kindergarten using **same-site urban mining** from the former Gladsaxe School; recycling metrics separated from direct reuse. | [file](../../_neo4j/processed/projects/records/p_svanen_kindergarten_gladsaxe.kg.jsonl) |
| **Villa Welpeloo** | Enschede, NL | 2009 | Landmark case: load-bearing reuse of **steel beams** salvaged from a textile/paternoster machine. | [file](../../_neo4j/processed/projects/records/p_villa_welpeloo_enschede.kg.jsonl) |

---

## Tier 2 — Strong cases (★★★★)

Well-documented main and comparison cases. Where reuse is partial, the table notes which stream
carries the evidence.

| Project | Location | Year | Key reuse focus | Record |
|---|---|:---:|---|---|
| **Holbein Gardens** | London, UK | 2023 | Verified load-bearing steel in the extension (not the 90%+ retention). | [file](../../_neo4j/processed/projects/records/p_holbein_gardens_london.kg.jsonl) |
| **Grubenstrasse 29 / Werkhof 29** | Zürich, CH | 2025 | Conversion + extension with extensive fixed-component reuse (2,600 m²). | [file](../../_neo4j/processed/projects/records/p_grubenstrasse_29_werkhof_29_zuerich.kg.jsonl) |
| **Haus HOS** | Mühlhausen, DE | 2008 | Load-bearing reuse of WBS70 / RC large-panel elements from Leinefelde. | [file](../../_neo4j/processed/projects/records/p_haus_hos_mehrfamilienhaus_muehlhausen.kg.jsonl) |
| **Mehrow Pilot House** | Mehrow, DE | 2005 | WBS70 wall & floor panels from a Marzahn slab block reused load-bearing in a house. | [file](../../_neo4j/processed/projects/records/p_mehrow_pilot_house.kg.jsonl) |
| **Broethen Twin-House** | Hoyerswerda, DE | — | Load-bearing ex-situ reuse of 26 wall + 50 floor P2-system panels. | [file](../../_neo4j/processed/projects/records/p_broethen_twin_house_hoyerswerda.kg.jsonl) |
| **CRCLR House / Impact Hub** | Berlin, DE | 2023 | Roof steel reused as stair stringers; hall retention not counted as reuse. | [file](../../_neo4j/processed/projects/records/p_crclr_house_impact_hub_berlin.kg.jsonl) |
| **Recyclinghaus Hannover** | Hannover, DE | 2019 | Strong envelope + interior reuse case (new glue-free solid-timber primary structure). | [file](../../_neo4j/processed/projects/records/p_recyclinghaus_hannover.kg.jsonl) |
| **Thoravej 29** | Copenhagen, DK | 2025 | Industrial transformation with **self-reuse**: TT/concrete slabs → stairs, brick → flooring/paving. | [file](../../_neo4j/processed/projects/records/p_thoravej_29_copenhagen.kg.jsonl) |
| **Timber Square** | London, UK | (handover TBC) | Large office/mixed-use (52,026 m²) with ex-situ reused steel. | [file](../../_neo4j/processed/projects/records/p_timber_square_london.kg.jsonl) |
| **House of Fraser → TBC.London** | London, UK | 2025 | **Reuse chain**: donor + receiver modelled separately; conflicting quantities preserved. | [file](../../_neo4j/processed/projects/records/p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain.kg.jsonl) |
| **55 Great Suffolk Street** | London, UK | — | Retrofit/extension with reused steel in a new external core; ~50 t CO₂. | [file](../../_neo4j/processed/projects/records/p_55_great_suffolk_street_london.kg.jsonl) |
| **Brent Cross Town Substation** | London, UK | — | Infrastructure/screen structure; CO₂ & reuse share kept as source-conflict ranges. | [file](../../_neo4j/processed/projects/records/p_brent_cross_town_primary_substation_london.kg.jsonl) |
| **Boulder Fire Station 3** | Boulder, US | 2024 | Critical public infrastructure with partial structural reuse of hospital steel sections. | [file](../../_neo4j/processed/projects/records/p_boulder_fire_station_3.kg.jsonl) |
| **Big Dig House** | Lexington, US | — | Built from highway-project (Big Dig) salvage; source conflicts kept as ranges. | [file](../../_neo4j/processed/projects/records/p_big_dig_house_lexington_massachusetts.kg.jsonl) |
| **Saxum Vineyard Equipment Barn** | Paso Robles, US | — | Reused drill-stem pipes as columns and roof structure. | [file](../../_neo4j/processed/projects/records/p_saxum_vineyard_equipment_barn_paso_robles.kg.jsonl) |
| **Europa Building** (Résidence Palace) | Brussels, BE | 2016 | Large-scale public envelope reuse (81,777 m²); heritage retention kept separate. | [file](../../_neo4j/processed/projects/records/p_europa_building_brussels.kg.jsonl) |
| **ELYS Kultur- & Gewerbehaus** | Basel, CH | — | Large-scale envelope-reuse case; concrete structure retention separated. | [file](../../_neo4j/processed/projects/records/p_elys_kultur_gewerbehaus_basel.kg.jsonl) |
| **Lycée Michel Lucius Conversion** | Luxembourg | 2021 | Public campus conversion with several documented direct-reuse streams. | [file](../../_neo4j/processed/projects/records/p_lycee_michel_lucius_conversion_luxembourg.kg.jsonl) |
| **Jeugdkliniek Ithaka / Emergis** | Kloetinge, NL | 2019 | Healthcare direct-reuse case with donor building RWS Terneuzen. | [file](../../_neo4j/processed/projects/records/p_jeugdkliniek_ithaka_emergis_kloetinge.kg.jsonl) |
| **gjG House** | Gentbrugge / Ghent, BE | 2015 | Structurally autonomous curved **brick shell** from reused bricks. | [file](../../_neo4j/processed/projects/records/p_gjg_house_gentbrugge.kg.jsonl) |
| **Maison DnA** | Asse, BE | 2013 | New build with reused **brick walls** as an autonomous structural exterior. | [file](../../_neo4j/processed/projects/records/p_maison_dna_asse.kg.jsonl) |
| **Association house, Gröditz** | Gröditz, DE | 2007 | Built sports/association house using reused precast concrete from two donors. | [file](../../_neo4j/processed/projects/records/p_association_house_groeditz.kg.jsonl) |
| **Association house, Plauen** | Plauen, DE | 2007 | Built association house reusing IW73/6 precast concrete components. | [file](../../_neo4j/processed/projects/records/p_association_house_plauen.kg.jsonl) |
| **Berlin-Schildow Pilot House** | Schildow, DE | 2005 (shell) | Second pilot house; precast large-panel reuse. | [file](../../_neo4j/processed/projects/records/p_berlin_schildow_pilot_house.kg.jsonl) |

---

## Tier 3 — Comparison & watchlist cases (★★★)

Useful comparators. Several are **watchlist** items — disassembly/design documented but reuse not
yet built / as-built confirmed.

| Project | Location | Note | Record |
|---|---|---|---|
| **Circular Centre NL / Prinsenhof A** | Arnhem, NL | Watchlist: strong disassembly + planned reuse (~3,500 t CO₂); reinstallation not yet as-built. | [file](../../_neo4j/processed/projects/records/p_circular_centre_netherlands_prinsenhof_a_reuse_pilot.kg.jsonl) |
| **Juch-Areal Recyclingzentrum** | Zürich, CH | Watchlist: planned public reuse pilot (~600 t CO₂), execution 2026–2027. | [file](../../_neo4j/processed/projects/records/p_juch_areal_recyclingzentrum_zuerich.kg.jsonl) |
| **Melkinlaituri School & Day-care** | Helsinki, FI | Commercial replication of ReCreate: 64 reused hollow-core slabs from Suutarila. | [file](../../_neo4j/processed/projects/records/p_melkinlaituri_primary_school_daycare_centre_helsinki.kg.jsonl) |
| **Härmälänranta / A-Kruunu ReCreate** | Tampere, FI | ReCreate mini-pilot: load-bearing hollow-core slabs from a 1980s office. | [file](../../_neo4j/processed/projects/records/p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere.kg.jsonl) |
| **Lokomotion Technology Centre** | Tampere, FI | Load-bearing hollow-core slab reuse in two zones of a large industrial project. | [file](../../_neo4j/processed/projects/records/p_lokomotion_technology_centre_mini_pilot_tampere.kg.jsonl) |
| **Grande Halle de Colombelles / Le WIP** | Colombelles, FR | Dedicated *Lot 01 Réemploi*; concrete-hall retention modelled separately. | [file](../../_neo4j/processed/projects/records/p_grande_halle_de_colombelles.kg.jsonl) |
| **La Ferme du Rail** | Paris, FR | New build with documented fixed direct-reuse parts; 90% figure mixes biosourced + reused. | [file](../../_neo4j/processed/projects/records/p_ferme_du_rail_paris.kg.jsonl) |
| **Résilience / La Ferme des Possibles** | Stains, FR | Direct reuse in envelope, interior, MEP, outdoor; new primary structure. | [file](../../_neo4j/processed/projects/records/p_resilience_la_ferme_des_possibles_stains.kg.jsonl) |
| **Maison des Canaux** | Paris, FR | Known social-circular refurbishment; some documented fixed reuse fit-out. | [file](../../_neo4j/processed/projects/records/p_maison_des_canaux_paris.kg.jsonl) |
| **Maison Vignette** | Auderghem, BE | Private new build with fixed reuse in façade/finishes/sanitary; new timber-straw-hempcrete structure. | [file](../../_neo4j/processed/projects/records/p_maison_vignette_auderghem.kg.jsonl) |
| **MULTI Brussels** | Brussels, BE | Large-scale refit with material passport; reuse only for transformed/re-placed parts. | [file](../../_neo4j/processed/projects/records/p_multi_brussels_reuse_in_multi.kg.jsonl) |
| **Musée de Folklore / MUSEF** | Mouscron, BE | Façade reuse with bricks from eight demolition sources. | [file](../../_neo4j/processed/projects/records/p_musee_de_folklore_mouscron.kg.jsonl) |
| **Lo-Reninge Town Hall façade** | Lo-Reninge, BE | New façade from reused bricks; cloister retention separate. | [file](../../_neo4j/processed/projects/records/p_lo_reninge_town_hall_facade.kg.jsonl) |
| **Institut de Botanique ULg** | Liège, BE | Reuse relevance in a partly documented reused timber façade. | [file](../../_neo4j/processed/projects/records/p_institut_de_botanique_ulg_liege.kg.jsonl) |
| **Chiro d'Itterbeek (sanitary block)** | Dilbeek, BE | Very small new build (15 m²) with many reused + surplus components. | [file](../../_neo4j/processed/projects/records/p_chiro_d_itterbeek_dilbeek.kg.jsonl) |
| **Verbiest + Karreveld** | Brussels, BE | Combined comparator of two AgwA projects. | [file](../../_neo4j/processed/projects/records/p_verbiest_karreveld_brussels.kg.jsonl) |
| **Zinneke / FEDER Masui4ever** | Brussels, BE | 94% retention is context, not a direct-reuse value. | [file](../../_neo4j/processed/projects/records/p_zinneke_feder_masui4ever_brussels.kg.jsonl) |
| **BlueCity Offices** | Rotterdam, NL | Reuse focus: fixed window-frame partitions; ~60 t CO₂, 68% reduction. | [file](../../_neo4j/processed/projects/records/p_bluecity_offices_rotterdam.kg.jsonl) |
| **Liander / Alliander HQ** | Duiven, NL | Strong circular transformation; concrete direct-reuse parts only partly documented. | [file](../../_neo4j/processed/projects/records/p_liander_alliander_hq_duiven.kg.jsonl) |
| **The Green House** | Utrecht, NL | Temporary circular pavilion with real reuse parts; DfD tracked separately. | [file](../../_neo4j/processed/projects/records/p_the_green_house_utrecht.kg.jsonl) |
| **Resource Rows** | Copenhagen, DK | Visible direct reuse of brick-wall modules as façade/envelope parts. | [file](../../_neo4j/processed/projects/records/p_resource_rows_copenhagen.kg.jsonl) |
| **Upcycle Studios** | Copenhagen, DK | Source conflicts (area, year, concrete qty) kept as min/max. | [file](../../_neo4j/processed/projects/records/p_upcycle_studios_copenhagen.kg.jsonl) |
| **TRÆ High-Rise** | Aarhus, DK | High-rise with reuse/upcycling components; new/hybrid primary structure. | [file](../../_neo4j/processed/projects/records/p_trae_high_rise_aarhus.kg.jsonl) |
| **Woongroep Boschgaard** | s-Hertogenbosch, NL | Sources cite 84–90% harvested/secondary materials; method open. | [file](../../_neo4j/processed/projects/records/p_woongroep_boschgaard_den_bosch.kg.jsonl) |
| **Kindergarten Mööslistrasse / Manegg** | Zürich, CH | Municipal reuse pilot (~12.5 t CO₂); depot retention + loose furniture separated. | [file](../../_neo4j/processed/projects/records/p_kindergarten_moeoeslistrasse_manegg_zuerich.kg.jsonl) |
| **Brighton Waste House** | Brighton, UK | Strong material/living-lab demonstrator; not primarily a load-bearing reuse case. | [file](../../_neo4j/processed/projects/records/p_brighton_waste_house_brighton.kg.jsonl) |
| **Hastings Pier Visitor Centre** | Hastings, UK | Only fixed reused timber cladding counted; pier restoration excluded. | [file](../../_neo4j/processed/projects/records/p_hastings_pier_visitor_centre.kg.jsonl) |
| **Kamikatsu Zero Waste Center / Hotel WHY** | Kamikatsu, JP | New build with strongly visible local component/material reuse. | [file](../../_neo4j/processed/projects/records/p_kamikatsu_zero_waste_center_hotel_why.kg.jsonl) |

---

## Tier 4 — Appendix, concept & negative cases (★★)

Pavilions, temporary demonstrators, prototypes, unbuilt proposals, and thin-evidence cases. Kept for
methodological contrast and learning value rather than as primary evidence.

| Project | Location | Why appendix/concept | Record |
|---|---|---|---|
| **People's Pavilion** | Eindhoven, NL | Temporary 100%-borrowed demonstrator; dismantled after 9 days. | [file](../../_neo4j/processed/projects/records/p_peoples_pavilion_eindhoven.kg.jsonl) |
| **Circular Pavilion (Pavillon Circulaire)** | Paris, FR | Small temporary demonstrator (70 m²); loose chairs excluded. | [file](../../_neo4j/processed/projects/records/p_circular_pavilion_paris.kg.jsonl) |
| **Christ Pavilion** | Volkenroda, DE | Whole EXPO-2000 pavilion dismantled and rebuilt (translocation). | [file](../../_neo4j/processed/projects/records/p_christ_pavilion_volkenroda.kg.jsonl) |
| **Plattenvereinigung** | Berlin, DE | Temporary, demountable recycled building from East/West precast panels. | [file](../../_neo4j/processed/projects/records/p_plattenvereinigung_berlin.kg.jsonl) |
| **Plattenpalast** | Berlin, DE | Micro-house/gallery from WBS70 panels; windows from Palast der Republik. | [file](../../_neo4j/processed/projects/records/p_plattenpalast_berlin.kg.jsonl) |
| **SUPERLOCAL Expogebouw** | Kerkrade, NL | Demonstrator with three cut-out apartment sections from a tower block. | [file](../../_neo4j/processed/projects/records/p_superlocal_expogebouw_bleijerheide.kg.jsonl) |
| **Impact Hub Berlin Interior (CRCLR fit-out)** | Berlin, DE | Supplementary interior fit-out; only fixed room elements counted. | [file](../../_neo4j/processed/projects/records/p_impact_hub_berlin_crclr_fitout.kg.jsonl) |
| **PLP Architecture HQ fit-out** | London, UK | Headline figures include furniture/donations; only fixed parts counted. | [file](../../_neo4j/processed/projects/records/p_plp_london_hq_circular_studio_fitout.kg.jsonl) |
| **AWM Münster circular office** | Münster, DE | Small circular interior fit-out (~13.3 t CO₂, 82% reduction). | [file](../../_neo4j/processed/projects/records/p_awm_muenster_circular_office.kg.jsonl) |
| **CascadeUp glulam demonstrator** | London, UK | Remanufacturing case: salvage timber → glulamST/CLST; quantities unknown. | [file](../../_neo4j/processed/projects/records/p_cascadeup_london_secondary_timber_glulam_demonstrator.kg.jsonl) |
| **Re:Crete footbridge** | EPFL, CH | Research prototype from sawn cast-in-place concrete blocks; not a building. | [file](../../_neo4j/processed/projects/records/p_recrete_footbridge_reused_concrete_blocks.kg.jsonl) |
| **Bestandverplanzung Pavilion** | München, DE | Small built demonstrator; little public technical documentation. | [file](../../_neo4j/processed/projects/records/p_bestandverplanzung_pavilion_muenchen.kg.jsonl) |
| **Montessori Maassluis** | Maassluis, NL | Watchlist: reused hollow-core slabs in design but not yet as-built (≈2026/27). | [file](../../_neo4j/processed/projects/records/p_montessori_maassluis.kg.jsonl) |
| **Big Dig Building** | Boston, US | Award-winning but **unbuilt** proposal; concept/appendix case. | [file](../../_neo4j/processed/projects/records/p_big_dig_building_boston.kg.jsonl) |
| **Roots in the Sky / Blackfriars** | London, UK | **Negative/learning case**: planned structural steel reuse, not built as evidence. | [file](../../_neo4j/processed/projects/records/p_roots_in_the_sky_blackfriars_crown_court.kg.jsonl) |

---

## At a glance

- **Start here (the canonical anchors):** K.118 Winterthur, Villa Welpeloo, KA13 Oslo, BioPartner 5,
  BedZED, Svanen Kindergarten, Recypark Demets.
- **Reuse-chain modelling exemplar:** House of Fraser → TBC.London (separate donor/receiver).
- **ReCreate hollow-core-slab thread (FI/NO):** KA13 · Härmälänranta · Lokomotion · Melkinlaituri.
- **Large-panel (WBS70/P2) reuse thread (DE):** Haus HOS · Mehrow · Broethen · Plattenpalast · Plattenvereinigung.
- **Watchlist (planned, not yet as-built):** Circular Centre NL · Juch-Areal · Montessori Maassluis.
- **Negative/unbuilt for contrast:** Big Dig Building · Roots in the Sky.

*Generated 2026-06-30 from the user-confirmed projects dataset (`_neo4j/processed/projects/`, 74 records, ratings via the `bewertung` property).*
