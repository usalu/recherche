# Graph schema reference — `database: mit-bestand`

This file documents every node label, controlled-vocabulary ID, and key property name that the importer will look for when translating a research dossier into the graph.  
**Always cite sources. Unknown values → write `"unknown"`. Never fabricate.**

---

## Node labels (complete list)

| Node label | What it represents |
|---|---|
| `Akteur` | Person or organisation |
| `Akteurrolle` | Functional role on a project (controlled vocab) |
| `Akteurtyp` | Broad category of actor (controlled vocab) |
| `Akzeptanz` | Acceptance / legitimation signal (controlled vocab) |
| `Aufbereitungsverfahren` | Refurbishment or processing step applied to a component |
| `BauaufgabeIntervention` | Type of construction task (controlled vocab) |
| `Bauobjektklasse` | Building-object category (controlled vocab) |
| `Bauobjektrolle` | Role a building plays in a reuse chain (controlled vocab) |
| `Bauproduktstatus` | Regulatory product-approval status (controlled vocab) |
| `Bausystem` | Construction system (e.g. timber-frame, precast) |
| `Bauteilebene` | Layer / scale of component (structural, envelope, finish …) |
| `Bauteilgruppe` | A batch of reused components (the main reuse-data node) |
| `Bauteiltyp` | Component type (controlled vocab) |
| `Bauweise` | Construction method or style |
| `Bauwerk` | Any building or structure (receiver, donor, depot, storage) |
| `BauwerkEra` | Era / construction period classification |
| `Beschaffungsweg` | Acquisition path for reused material (controlled vocab) |
| `Defekt` | Defect or condition finding on a component batch |
| `Funktionswechsel` | Old vs. new function of a component |
| `Huerde` | Specific barrier encountered |
| `HuerdeKategorie` | Category of barrier (regulatory, technical, logistical …) |
| `Land` | Country node |
| `Layer` | Shearing-layers model layer |
| `LebenszyklusModul` | EN 15978 lifecycle-assessment module |
| `Leistungsanforderung` | Performance requirement a component must meet |
| `Logistik` | Logistics aspect (controlled vocab) |
| `Marktmodell` | Market / economic model (controlled vocab) |
| `MatchingQualitaet` | Quality of donor–receiver match |
| `Material` | Specific material node |
| `Materialgruppe` | Material category (controlled vocab) |
| `Methode` | Design or planning method (controlled vocab) |
| `Norm` | Standard or norm cited (e.g. SIA 269, EN 1993) |
| `Nutzung` | Building use / function (controlled vocab) |
| `Programm` | Funding or research programme |
| `Projekt` | Overarching project record |
| `Prozessphase` | Phase in the reuse process |
| `PruefungNachweis` | Quality test or verification procedure |
| `Quelle` | Bibliographic source |
| `RechtlicheBedingung` | Regulatory or legal condition |
| `Ressourcenquelle` | Source of a material resource |
| `Rueckbauverfahren` | Deconstruction method (controlled vocab) |
| `Schadstoff` | Pollutant (asbestos, PCB, PAH …) |
| `Software` | Digital software used on a project |
| `Stadt` | City node |
| `Status` | Project or building status node |
| `Tool` | Non-software tool or workflow |
| `Tragwerksprinzip` | Structural principle |
| `Verbindungstechnik` | Joining technique (bolting, welding, dry-stacking …) |
| `WiederverwendungsArt` | Type of reuse strategy (controlled vocab) |
| `Wiederverwendungskette` | Full donor→processing→receiver chain |
| `Wirtschaft` | Economic data record |
| `ZertifizierungBewertungssystem` | Certification / rating system (controlled vocab) |
| `ZustandsKlasse` | Condition class of a component batch |

---

## Controlled vocabularies

### Akteurrolle — role of a person/org on a project
```
ar_bauherr_auftraggeber       client / Bauherr / owner
ar_entwurf_planung            architecture / lead design
ar_tragwerksplanung           structural engineering
ar_tga_gebaeudetechnik        building services (HVAC, electrical)
ar_fassade                    façade specialist
ar_brandschutz_barrierefreiheit  fire protection / accessibility
ar_nachhaltigkeitsberatung    sustainability / LCA consultant
ar_reuse_beratung             reuse consultant (general)
ar_reuse_zirkularitaetsberatung  circularity / reuse planning specialist
ar_rueckbau_bauteilernte_logistik  deconstruction / harvesting / logistics
ar_bauausfuehrung_fertigung   main contractor / builder
ar_materialbroker             material broker / reuse-marketplace operator
ar_materiallieferung_markt    material supplier / market side
ar_oeffentliche_hand_foerderung   public authority / funder / regulator
ar_forschung_dokumentation    research / documentation
ar_bildung_wissenstransfer    teaching / knowledge transfer
ar_fachplanung_nachweis       specialist planner / certifier
ar_projektmanagement_koordination  project management / coordination
ar_stahlbau_fertigung         steel fabrication
ar_kunst_gestaltung           art / artistic direction
ar_landschaftsplanung         landscape
ar_software_digitalisierung   software / digitisation
ar_betrieb_nutzung            building operator / end user
ar_aufbereitung_refurbishment  refurbishment contractor
```

### Akteurtyp — broad category of actor
```
at_person
at_unternehmen
at_forschung_lehre
at_oeffentliche_institution
at_foerdergeber_programmtraeger
at_materialhub_bauteilboerse
at_software_tool_anbieter
at_ngo_verband_netzwerk
at_organisation
```

### Bauobjektrolle — role a building plays
```
bor_donorobjekt               donor building (material source)
bor_empfaengerobjekt          receiver building (built outcome)
bor_bestandsobjekt            existing building retained in situ
bor_same_site_donor_receiver  donor and receiver on same site
bor_referenzobjekt            reference / comparator building
bor_zwischenlager             intermediate storage site
```

### Bauobjektklasse — building-object type
```
bok_gebaeude
bok_gebaeudeteil
bok_pavillon
bok_infrastruktur
bok_innenausbau
bok_depot_lager
bok_quartier_areal
bok_reuse_centre
```

### BauaufgabeIntervention — construction task type
```
bai_neubau
bai_sanierung
bai_umbau
bai_umnutzung
bai_fit_out
bai_aufstockung
bai_erweiterung
bai_rueckbau
bai_translozierung
bai_wiederaufbau
```

### Nutzung — building use
```
nut_wohnen
nut_buero
nut_schule_bildung
nut_gewerbe
nut_kultur
nut_mischnutzung
nut_sozialbau
nut_infrastruktur
nut_lager_depot
```

### Materialgruppe — material category
```
mg_metall
mg_mineralisch
mg_holz_biobasiert
mg_glas_keramik
mg_daemmstoff
mg_kunststoff
mg_lehm_erde
mg_verbundstoff
mg_recyclingmaterial
mg_unbekannt
```

### Bauteiltyp — component type
```
bt_traeger       beam
bt_stuetze       column
bt_decke         floor/ceiling slab
bt_wand          wall
bt_fassade       façade element
bt_fenster       window
bt_boden         floor finish
bt_dach          roof element
bt_tuer          door
bt_treppe        stair
bt_fundament     foundation
bt_daemmung      insulation
bt_technik       technical/MEP component
bt_ausbau        fit-out element
bt_gelaender     railing / balustrade
```

### WiederverwendungsArt — reuse strategy type
```
wva_direkte_wiederverwendung    direct reuse (same form, same function)
wva_adaptives_reuse             adaptive reuse (same element, changed context)
wva_refurbishment               refurbishment before reuse
wva_remanufacturing             significant reworking
wva_recycling                   material recycling
wva_upcycling                   value-adding transformation
wva_design_for_disassembly      designed for future disassembly
wva_same_site_reuse             same-site reuse
wva_urban_mining                urban mining strategy
wva_bestandserhalt              retention of existing structure
wva_weiterbauen_im_bestand      continuing to build within existing stock
```

### Beschaffungsweg — acquisition path
```
bweg_rueckbauprojekt        sourced from a specific demolition project
bweg_direktvermittlung      direct brokered handover
bweg_bauteilboerse          component exchange (physical or online)
bweg_digitale_plattform     via digital platform (Concular, Madaster, Opalis …)
bweg_lager                  from existing stockpile / depot
bweg_eigenbestand           from own portfolio / same organisation
bweg_spende                 donation
bweg_ausschreibung          tendered procurement
bweg_informelles_netzwerk   informal network / word-of-mouth
bweg_leihmodell             loan / lease model
```

### Rueckbauverfahren — deconstruction method
```
rv_selektiver_rueckbau          selective deconstruction
rv_demontage                    careful disassembly
rv_ausbau_von_bauteilen         removal of individual components
rv_zerstoerungsarme_bergung     non-destructive recovery
rv_betonfraesen                 concrete milling
```

### Methode — design or planning method
```
meth_form_follows_availability     design driven by what is available
meth_pre_deconstruction_audit      pre-demolition audit
meth_bauteilkatalogisierung        component cataloguing
meth_materialinventur              material inventory
meth_design_for_disassembly        design for disassembly
meth_urban_mining                  urban mining methodology
meth_reuse_ausschreibung           reuse-specific tendering
meth_zirkulaere_ausschreibung      circular procurement
meth_reversibilitaet               reversibility design principle
meth_reuse_assessment              reuse assessment procedure
meth_abrissmonitoring              demolition monitoring
meth_building_material_scouting    material scouting
meth_wiederverwendungskriterien    reuse criteria framework
```

### Bauproduktstatus — regulatory product status (country-specific)
```
bps_tracimat_be          Tracimat selective-deconstruction certificate (Belgium)
bps_pemd_fr              PEMD déclaration de réemploi (France)
bps_zie_vbg              ZiE / vBG project-specific approval (Germany)
bps_abz_abg              abZ / aBG general approval (Germany)
bps_project_specific     project-specific approval (generic)
bps_ce_hen               CE marking via harmonised standard
bps_ce_eta               CE marking via European Technical Assessment
bps_ukca                 UKCA marking (UK post-Brexit)
bps_nta_8713             NTA 8713 (Netherlands)
bps_baupg_ch             BauPG (Switzerland)
bps_ue_zeichen           Ü-Zeichen (Germany, older)
bps_bestand_no_status    in-situ existing — no separate status required
bps_unbekannt            status unknown
```

### ZertifizierungBewertungssystem — certification / rating system
```
zbs_breeam
zbs_dgnb
zbs_leed
zbs_well
zbs_nabers
zbs_nordic_swan_ecolabel
zbs_paris_proof
```

### Marktmodell — economic / market model
```
mm_kauf_gebraucht              purchase of second-hand material
mm_plattform_vermittelt        platform-mediated purchase
mm_spende                      donation / free supply
mm_same_site                   same-site reuse (no market transaction)
mm_intra_konzern               intra-corporate transfer
mm_forschungsprojekt_zuteilung  research-programme allocation
mm_take_back_service           take-back / reverse-logistics service
mm_leasing                     leasing model
mm_rueckkauf                   buy-back arrangement
mm_kauf_neu                    purchase of new-equivalent replacement
```

### Akzeptanz — acceptance / legitimation signal
```
ak_aesthetik_patinakultur       patina / aged-aesthetic acceptance by client/users
ak_breeam_zertifizierung        BREEAM credits for reuse
ak_dgnb_zertifizierung          DGNB credits for reuse
ak_leed_zertifizierung          LEED credits for reuse
ak_oeffentlicher_bauherr_pilot  public-sector client running a pilot
```

### Logistik — logistics aspects
```
log_transport
log_transportdistanz
log_lagerung
log_zwischenlagerung
log_bauteiltracking
log_materialmatching
log_materialverfuegbarkeit
log_just_in_time
log_lagerflaeche
log_lokale_wiederverwendung
```

### Programm — existing programme nodes in graph
```
prog_fcrbe                     FCRBE (Interreg NWE)
prog_interreg_nwe              Interreg North-West Europe (general)
prog_horizon_2020              Horizon 2020
prog_reallabor                 Reallabor (generic)
prog_reallabor_be_ware         Reallabor B(e) Ware (TU Berlin)
prog_zukunftbau                Zukunft Bau (BBSR, Germany)
prog_recreate                  ReCreate (Finland/EU)
prog_recreate_local            ReCreate local Finnish cluster
prog_pilotprojekt              Pilot project (generic)
prog_bbsm                      BBSM
prog_expo_2000                 EXPO 2000 Hannover
prog_urban_innovative_actions  Urban Innovative Actions (UIA, EU)
prog_preuse                    PREUSE
prog_foerderprogramm           Foerderprogramm (generic)
prog_forschungsprojekt         Forschungsprojekt (generic)
prog_wettbewerb                Wettbewerb / competition
prog_kommunales_programm       Kommunales Programm (generic)
```

### Software — existing software nodes in graph
```
software_bim        BIM (generic)
software_concular   Concular
software_restado    Restado
software_qflow      Qflow
software_inies      INIES (FR LCA database)
```

### Tool — existing tool nodes in graph
```
tool_bauteilkatalog              component catalogue / material passport
tool_bim_bauteilkatalog          BIM-linked component catalogue
tool_oogstkaart_harvest_map      Oogstkaart / Harvest Map
tool_hts_stockmatcher            HTS Reused Steel Stockmatcher
tool_material_passports_maconda  Material passports (Maconda workflow)
```

---

## Key quantitative properties — `Bauwerk` node (receiver building)

| Property name | Meaning | Unit |
|---|---|---|
| `bgf_m2` | Gross floor area | m² |
| `nutzflaeche_m2` | Net usable area | m² |
| `geschosse_anzahl` | Number of storeys | integer |
| `fertigstellung_jahr` | Completion year | year |
| `entwurf_jahr` / `entwurfsstart_jahr` | Design start year | year |
| `bau_jahr_von` / `bau_jahr_bis` | Construction period | year |
| `baujahr` | Year of construction (single) | year |
| `reuse_anteil_prozent` | Reuse rate by mass (%) | % |
| `wiederverwendungsrate_gewicht_prozent` | Reuse rate by weight | % |
| `wiederverwendungsrate_volumen_prozent` | Reuse rate by volume | % |
| `reuse_masse_t` | Total mass of reused material | tonnes |
| `co2_einsparung_t` | CO₂ savings total | t CO₂e |
| `co2_einsparung_prozent` | CO₂ savings as % of reference | % |
| `baukosten_eur` | Total construction cost | € |
| `baukosten_eur_m2` | Construction cost per m² | €/m² |
| `lca_module_scope` | LCA scope reported (e.g. "A1-A5", "A1-C4") | text |
| `transportdistanz_donor_receiver_km` | Transport distance donor→site | km |
| `design_for_disassembly` | Designed for disassembly | true/false |
| `material_passport` | Material passport registered | true/false/platform-name |
| `foerderprogramm` | Funding programme name | text |
| `zertifizierung` | Certification achieved | text |
| `lebensdauer_geplant_jahre` | Planned service life | years |
| `adresse` | Street address | text |
| `ort` | City / district | text |
| `land` | Country (ISO-2 code preferred) | text |
| `bauwerkstatus` | Current status (built / in construction / planned / cancelled) | text |
| `nutzung_alt` | Original use | text |
| `nutzung_neu` | New / current use | text |

## Key quantitative properties — `Bauteilgruppe` node (component batch)

| Property name | Meaning | Unit |
|---|---|---|
| `menge_t` / `menge_t_min` / `menge_t_max` | Quantity in tonnes | t |
| `menge_m2` / `menge_m2_min` / `menge_m2_max` | Quantity in m² | m² |
| `menge_m3` | Quantity in m³ | m³ |
| `menge_stueck` | Quantity in pieces | integer |
| `menge_m` | Linear quantity | m |
| `bauteilalter_jahre` | Age of component at time of reuse | years |
| `lagerdauer_jahre` | Storage duration between harvest and reinstall | years |
| `transportdistanz_km` | Transport distance (donor to receiver) | km |
| `asbeststatus` | Asbestos screening result | text |
| `alte_funktion` | Original function / use | text |
| `neue_funktion` | New function / use | text |
| `herkunft` | Provenance description | text |
| `counts_as_direct_reuse` | Counts as direct reuse | true/false |
| `counts_as_bestandserhalt` | Counts as in-situ retention | true/false |
| `counts_as_recycling` | Counts as recycling | true/false |
| `counts_as_remanufacturing` | Counts as remanufacturing | true/false |
| `reuse_status` | Status at time of reuse | text |
| `donor_unknown` | Donor building not identified | true/false |

## Key properties — `Akteur` node

| Property | Meaning |
|---|---|
| `id` | Stable ID used in graph (e.g. `Werner_Sobek`) |
| `name` | Short display name |
| `name_full` | Full legal / formal name |
| `land` | Country of primary base |

## Key properties — `Programm` node

| Property | Meaning |
|---|---|
| `name` | Programme name |
| `jahr_start` / `start_jahr` | Start year |
| `end_jahr` / `jahr_bauzeit_ende` | End year |
| `funding_amount_eur` | Total programme budget (€) |
| `foerderprogramm` | Funding source name |
| `beschreibung` | Short description |

---

## Relationship types and what they link

| Relationship | From → To | Meaning |
|---|---|---|
| `BETEILIGT_AN` | Akteur → Bauwerk/Projekt | Actor participated in project (with `rolle_text`) |
| `HAT_AKTEURROLLE` | Akteur → Akteurrolle | Actor's functional role |
| `HAT_AKTEURTYP` | Akteur → Akteurtyp | Actor's category |
| `GEHÖRT_ZU` | Akteur → Akteur | Person belongs to organisation |
| `VERBUNDEN_MIT_AKTEUR` | Akteur → Akteur | Peer connection between actors |
| `AUS_BAUWERK` | Bauteilgruppe → Bauwerk | Component batch came from this donor |
| `EINGEBAUT_IN` | Bauteilgruppe → Bauwerk | Component batch installed in this receiver |
| `HAT_BAUTEILTYP` | Bauteilgruppe → Bauteiltyp | Component type |
| `HAT_MATERIALGRUPPE` | Bauteilgruppe → Materialgruppe | Material category |
| `HAT_WIEDERVERWENDUNGSART` | Bauwerk/Bauteilgruppe → WiederverwendungsArt | Reuse strategy |
| `HAT_BESCHAFFUNGSWEG` | Bauteilgruppe → Beschaffungsweg | How material was acquired |
| `HAT_RUECKBAUVERFAHREN` | Bauteilgruppe → Rueckbauverfahren | Deconstruction method |
| `HAT_AUFBEREITUNG` | Bauteilgruppe → Aufbereitungsverfahren | Processing step |
| `HAT_PRUEFUNG` | Bauteilgruppe → PruefungNachweis | Quality test / verification |
| `HAT_DEFEKT` | Bauteilgruppe → Defekt | Defect or condition finding |
| `HAT_LEISTUNGSANFORDERUNG` | Bauteilgruppe → Leistungsanforderung | Performance requirement |
| `HAT_VERBINDUNGSTECHNIK` | Bauteilgruppe → Verbindungstechnik | Joining technique |
| `HAT_BAUOBJEKTROLLE` | Bauwerk → Bauobjektrolle | Donor / receiver / depot role |
| `HAT_BAUOBJEKTKLASSE` | Bauwerk → Bauobjektklasse | Building type class |
| `HAT_NUTZUNG` | Bauwerk → Nutzung | Use category |
| `HAT_INTERVENTION` | Bauwerk → BauaufgabeIntervention | Construction task type |
| `HAT_ZERTIFIZIERUNG` | Bauwerk → ZertifizierungBewertungssystem | Certification |
| `HAT_BAUPRODUKTSTATUS` | Bauteilgruppe → Bauproduktstatus | Regulatory status of reused product |
| `HAT_METHODE` | Bauwerk/Bauteilgruppe → Methode | Design / planning method used |
| `REFERENZIERT_NORM` | Bauwerk/Bauteilgruppe → Norm | Standard cited |
| `HAT_LOGISTIK` | Bauteilgruppe → Logistik | Logistics aspect |
| `NUTZT_SOFTWARE` | Bauwerk/Projekt → Software | Software tool used |
| `NUTZT_TOOL` | Bauwerk/Projekt → Tool | Non-software tool used |
| `LIEGT_IN_LAND` | Bauwerk → Land | Country location |
| `LIEGT_IN_STADT` | Bauwerk → Stadt | City location |
| `ERHALT_FOERDERUNG_DURCH` | Bauwerk/Projekt → Programm | Funded by programme |
| `TEIL_VON_PROGRAMM` | Bauwerk/Projekt → Programm | Part of research/funding programme |
| `BERECHNET_NACH_MODUL` | Bauwerk → LebenszyklusModul | LCA modules used |
| `HAT_MARKTMODELL` | Bauteilgruppe/Bauwerk → Marktmodell | Market model |
| `HAT_DOMINANT_MARKTMODELL` | Bauwerk → Marktmodell | Dominant market model |
| `HAT_WIRTSCHAFT` | Bauwerk → Wirtschaft | Economic data record |
| `HAT_DOMINANT_AKZEPTANZ` | Bauwerk → Akzeptanz | Dominant acceptance signal |
| `HAT_HUERDE` | Bauwerk/Bauteilgruppe → Huerde | Barrier encountered |
| `ZITIERT_QUELLE` | any → Quelle | Source citation |
