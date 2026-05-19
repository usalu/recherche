# Import Plan: Inbox Projects — Batch 2026-05-19

**Sources:**
- `_neo4j/intake/inbox/projects/batch 1.md` (3 Swiss projects)
- `_neo4j/intake/inbox/projects/BE_NL_graph_ready_dossiers/Careno_Be_Circular_Brussels.md`
- `_neo4j/intake/inbox/projects/BE_NL_graph_ready_dossiers/Circl_ABN_AMRO_Urban_Mining.md` (duplicate note only)
- `_neo4j/intake/inbox/projects/BE_NL_graph_ready_dossiers/Circl_Pavilion_Amsterdam.md`

**All six Projekt nodes already exist in the graph.** This run adds enrichment, new actors, Bauteilgruppen, and vocabulary links. It does NOT create new Projekt nodes.

**Status:** PLAN — not yet executed

**Audit corrections applied:** 2026-05-19 — see `CORRECTIONS.md` in this folder for full evidence trail.

---

## PHASE 0 — Pre-conditions (must resolve before any import)

These are blocking issues. Do not proceed past Phase 0 until each is resolved.

### P0-A: Resolve Werner Sobek duplicate
Two actor nodes for the same person are linked to `p_umar_unit`:
- `werner_sobek_p` (canonical, keep)
- `Werner_Sobek` (duplicate, remove ASSOZIIERT_MIT_PROJEKT edge, then evaluate whether to delete or merge)

**Action:** Remove the duplicate relationship; verify `werner_sobek_p` carries all needed properties.

### P0-B: Resolve Circl node duplication
Two Projekt nodes refer to the same physical building:
- `p_pavilion_circl_amsterdam` (canonical — full dossier)
- `p_circl_abn_amro` (context note — explicitly flagged as duplicate in inbox dossier)

**Action:** Merge into `p_pavilion_circl_amsterdam`. Migrate all existing relationships from `p_circl_abn_amro` (verified live):
- `michel_baars -[ASSOZIIERT_MIT_PROJEKT]-> p_circl_abn_amro` — RETARGET to `p_pavilion_circl_amsterdam` (incoming rel from michel_baars)
- `p_circl_abn_amro -[BELEGT_IN]-> q_actor_michel_baars_02` — copy to canonical node
- `p_circl_abn_amro -[BELEGT_IN]-> q_actor_michel_baars_03` — copy to canonical node
- `p_circl_abn_amro -[BELEGT_IN]-> q_akteursliste_master_md` — DO NOT copy (already present on canonical)
- `p_circl_abn_amro -[HAT_DOMINANT_MARKTMODELL]-> mm_intra_konzern` — copy to canonical
Then delete `p_circl_abn_amro`.

### P0-C: Resolve Rotor / Rotor DC actor fragmentation
Multiple Rotor-family nodes exist in the graph:
- `Rotor` — main design/research cooperative
- `rotor_asbl_vzw` — same org as asbl/vzw (Belgian legal form)
- `rotor_vzw` — likely same, possibly redundant
- `rotordc` — RotorDC deconstruction platform ← DISTINCT organization
- `rotor_dc` — likely duplicate of `rotordc`

**Action:** Confirm `Rotor` (or `rotor_asbl_vzw`) as canonical for Careno links. Confirm `rotordc` as canonical for UMAR links. Merge `rotor_dc` into `rotordc` if duplicate. Leave `rotor_vzw` for separate review.

### P0-D: Review `mm_intra_konzern` assignment on Circl
The Wirtschaft/Marktmodell node `mm_intra_konzern` ("Intra-Konzern") is currently linked to `p_circl_abn_amro`. The Circl pavilion was ABN AMRO self-funded, but the dossier describes "circular earning models" as the primary economic logic — not intra-group transfer.

**Action:** Retain `mm_intra_konzern` on the merged canonical node (it is sourced/documented). Add `mm_kauf_gebraucht` separately for the fire-hose cabinet procurement. Do not remove `mm_intra_konzern` without explicit user decision.

---

## PHASE 1 — Create new Stadt nodes

Two cities used in this batch are not yet in the graph (verified: `stadt_amsterdam` and `stadt_duebendorf` absent from full Stadt query).

| id | name | Land |
|----|------|------|
| `stadt_duebendorf` | Dübendorf | `land_schweiz` |
| `stadt_amsterdam` | Amsterdam | `land_niederlande` |

**Cypher pattern:**
```cypher
CREATE (n:Stadt {id: 'stadt_duebendorf', name: 'Dübendorf'})
CREATE (n:Stadt {id: 'stadt_amsterdam', name: 'Amsterdam'})
```
Link to existing Land nodes via `LIEGT_IN_LAND`.

---

## PHASE 1.5 — Create receiving Bauwerk nodes (4 new nodes)

`EINGEBAUT_IN` targets only `Bauwerk` nodes (not `Projekt`). Create one Bauwerk node per receiving building, then link:
- `Bauteilgruppe -[EINGEBAUT_IN]-> Bauwerk` (in Phase 7)
- `Projekt -[HAT_BAUTEILGRUPPE]-> Bauteilgruppe` (in Phase 7, from Projekt side)
- `Projekt -[NUTZT_BAUWERK]-> Bauwerk` (link Projekt to its Bauwerk)

| id | name | Stadt | Status |
|----|------|-------|--------|
| `bw_schaerenmoosstrasse_zuerich` | Schärenmoosstrasse Zürich | `stadt_zuerich` | `status_geplant` |
| `bw_umar_unit_duebendorf` | UMAR Unit, NEST Empa Dübendorf | `stadt_duebendorf` | `status_realisiert` |
| `bw_elementa_walkeweg_basel` | ELEMENTA Walkeweg Basel | `stadt_basel` | `status_geplant` |
| `bw_circl_pavilion_amsterdam` | Circl Pavilion Amsterdam | `stadt_amsterdam` | `status_rueckgebaut` |

Careno (`p_careno_becircular`) has no receiving building. Its Bauteilgruppen link to the Projekt node only via `HAT_BAUTEILGRUPPE`. No `EINGEBAUT_IN` needed.

---

## PHASE 2 — Create new Programm nodes

| id | name | Notes |
|----|------|-------|
| `prog_nest_empa` | NEST — Empa Dübendorf | Living-lab research platform; parent of UMAR unit |
| `prog_be_circular` | Be.Circular / Be Brussels | Brussels-Capital Region circular economy grant; Careno 2016 laureate |
| `prog_stiftung_pwg` | Stiftung PWG Wettbewerb Schärenmoosstrasse | Client-run architecture competition, 2022 |

---

## PHASE 3 — Create new Software and ZBS nodes

| Label | id | name | Notes |
|-------|----|------|-------|
| `Software` | `software_ecotool` | EcoTool | Swiss ecological balance calculation tool; required at ELEMENTA competition stage |
| `ZertifizierungBewertungssystem` | `zbs_ecotool` | EcoTool (ökologische Bilanz) | Same tool as above, appearing in ZBS role for competition requirement |

---

## PHASE 4 — Create new Akteur nodes

Create in this order: organisations first, then persons (persons may link to their organisation).

### 4a. Schärenmoosstrasse actors

| id | name | Rolle |
|----|------|-------|
| `stiftung_pwg` | Stiftung PWG | Bauherrschaft / client |
| `perez_schmidlin_bauing` | Pérez Schmidlin Bauingenieure GmbH | structural engineer |
| `stefan_perez` | Stefan Pérez | structural engineer (person at above firm) |
| `michael_schmidlin` | Michael Schmidlin | structural engineer (person at above firm) |
| `andreas_geser_la_ag` | Andreas Geser Landschaftsarchitekten AG | landscape architect |
| `andreas_geser` | Andreas Geser | landscape architect (person) |

### 4b. UMAR actors

| id | name | Rolle |
|----|------|-------|
| `empa` | Empa | Bauherrschaft / research institute host |
| `kaufmann_zimmerei` | kaufmann zimmerei und tischlerei gmbh | timber contractor |
| `amstein_walthert` | Amstein+Walthert AG | building services engineer |
| `balzer_ingenieure` | Balzer Ingenieure AG | structural engineer |
| `weber_energie_bauphysik` | Weber Energie und Bauphysik | building physics |
| `lindner_se` | Lindner SE | ceiling panel supplier (product-as-service) |
| `nimbus` | Nimbus | lighting designer |
| `magna_glaskeramik` | Magna Glaskeramik | recycled-glass panel manufacturer |
| `ecovative` | Ecovative | mycelium insulation manufacturer |
| `desso_tarkett` | Desso / Tarkett | carpet supplier (take-back service) |

### 4c. ELEMENTA actors

| id | name | Rolle |
|----|------|-------|
| `kanton_basel_stadt` | Kanton Basel-Stadt | public authority / programme owner |
| `monotti_ingegneri` | Monotti Ingegneri Consulenti SA | structural engineer |
| `mario_monotti` | Mario Monotti | structural engineer (person) |
| `usus_la` | USUS Landschaftsarchitektur | landscape architect |
| `roger_keller` | Roger Keller | landscape architect (person) |
| `ana_olalquiaga` | Ana Olalquiaga | architect (person at PARABASE) |
| `caretta_weidmann` | Caretta+Weidmann | façade engineering |
| `gti_engineering` | GTI Engineering | MEP / building services |
| `afc_basel` | AFC | cost management / quantity surveying |
| `senn_technology` | Senn Technology AG | specialist engineering |
| `anima_engineering` | Anima Engineering AG | specialist engineering |
| `bauteilboerse_basel` | Bauteilbörse Basel | component exchange platform (Basel) |
| `digvis_gmbh` | Digvis GmbH | digital visualisation |

### 4d. Careno actors

| id | name | Rolle |
|----|------|-------|
| `bbri` | BBRI — Belgian Building Research Institute | research partner / testing |
| `brussels_capital_region` | Brussels-Capital Region | grant authority |
| `be_circular_be_brussels` | Be.Circular / Be Brussels | grant programme (may be linked to Programm node `prog_be_circular` rather than Akteur — decide at import) |

> Note: `Rotor` and `rotordc` already exist — use existing nodes (see P0-C).

### 4e. Circl actors

| id | name | Rolle |
|----|------|-------|
| `abn_amro` | ABN AMRO | Bauherrschaft / client |
| `tu_delft` | TU Delft | research partner |
| `bam_nl` | BAM | general contractor |
| `donkergroen` | Donkergroen | green / planting contractor |
| `traject` | TRAJECT | project management |
| `lcp_circulair` | lcp-circulair (Lagemaat + cepezedprojects) | circular dismantling contractor (2025) |
| `icon_real_estate` | Icon Real Estate | site owner post-dismantling |
| `victory_group` | Victory Group | site owner post-dismantling |
| `ter_velde_den_besten` | Ter Velde & Den Besten | material passport / digital twin |
| `vermaat` | Vermaat | catering operator |
| `exasun` | Exasun | solar energy supplier |
| `fagerhult` | Fagerhult | lighting supplier |

> Note: `hans_hammink`, `michel_baars`, `de_architekten_cie`, `new_horizon`, `de_groot_en_visser` already exist — use existing nodes.

---

## PHASE 5 — Create source Bauwerk nodes

These are the origin buildings for salvaged components. They are distinct from the Projekt nodes (which are the receiving projects).

| id | name | Location | Notes |
|----|------|----------|-------|
| `bw_ubs_altstetten` | UBS Datenzentrum Altstetten | Zürich-Altstetten | Source of two-storey hall for Schärenmoosstrasse |
| `bw_generale_de_banque_brussels` | Générale de Banque / BNP Paribas Fortis HQ | Brussels | Source of Jules Wabbes door handles for UMAR |
| `bw_lysbueechel_garage_basel` | Lysbüchel Parkgarage | Basel, Lysbüchel area | Source of RC columns, slabs, rib panels for ELEMENTA |

---

## PHASE 6 — Enrich existing Projekt nodes (properties)

Add or update these properties on existing nodes. Do not overwrite existing verified values — use `SET n.property = value` only where property is null or explicitly superseded.

### p_schaerenmoosstrasse_zuerich
```
address = "Schärenmoosstrasse 115/117, Zürich"
year_competition = 2022
current_status = "1st-rank competition result 2022; development recommended; unbuilt"
bauobjektklasse = "Wohnbau / Gewerbebau (Umnutzung Büro zu Wohnen)"
short_description = "Wettbewerbsprojekt ménage à trois: Umnutzung zweier Bürobauten zu
                     Wohn- und Gewerbenutzung mit wiederverwendetem Hallengebäude"
```
Link: `LIEGT_IN_STADT → stadt_zuerich` (EXISTS), `LIEGT_IN_LAND → land_schweiz` (EXISTS)

### p_umar_unit
```
address = "Überlandstrasse 129, 8600 Dübendorf"
year_construction_start = 2017
year_completed = 2018
gross_floor_area_conflict = "S1: 155 m², S3: 126 m² — unresolved; flag for source review"
current_status = "active research demonstrator in NEST; decommissioning not confirmed"
bauobjektrolle = "Demonstrator / Reallabor / materialdepot"
bauobjektklasse = "Forschungsgebäude-Einheit / Wohnmodul"
```
Link: `LIEGT_IN_STADT → stadt_duebendorf` (CREATE Phase 1), `LIEGT_IN_LAND → land_schweiz` (EXISTS)

### p_elementa_walkeweg
```
address = "Emilie Louise Frey-Strasse, 4053 Basel"
year_competition = 2023
year_construction_planned_start = 2027
year_construction_planned_end = 2029
gross_floor_area = 20000
dwelling_units = 150
current_status = "Projektplanung 2023–2025; Realisierung geplant 2027–2029; unbuilt"
bauobjektklasse = "Wohnbau (Mietvertrag Plus / Wohnbauprogramm 1000+)"
```
Link: `LIEGT_IN_STADT → stadt_basel` (EXISTS), `LIEGT_IN_LAND → land_schweiz` (EXISTS)

### p_careno_becircular
```
project_type_note = "Forschungs- und Kommerzialisierungsprojekt — kein Gebäude"
year_programme = 2016
programme_name = "Be.Circular / Be Brussels laureate 2016"
current_status = "Abgeschlossen; Produktlinie Re-Tile aktiv bei RotorDC"
```
Link: `LIEGT_IN_STADT → stadt_bruessel` (EXISTS), `LIEGT_IN_LAND → land_belgien` (EXISTS)

### p_pavilion_circl_amsterdam (canonical after P0-B merge)
```
address = "Gustav Mahlerplein, Amsterdam Zuidas"
year_construction_start = 2016
year_completed = 2017
date_opened = "2017-09-05"
date_dismantled = "2025-03"
gross_floor_area_min = 2000
current_status = "vollständig rückgebaut; Bauteile in Lagerung ab März 2025"
bauobjektrolle = "Demonstrations- und Referenzprojekt zirkuläres Bauen"
bauobjektklasse = "Büro / Gastronomie / Veranstaltung"
michel_baars_role_note = "Rolle bei Circl nicht öffentlich verifiziert (Quellenkonflikt)"
```
Link: `LIEGT_IN_STADT → stadt_amsterdam` (CREATE Phase 1), `LIEGT_IN_LAND → land_niederlande` (EXISTS)

---

## PHASE 7 — Create Bauteilgruppe nodes and link vocabulary

Create each Bauteilgruppe node, then add relationships. All vocabulary node IDs below are verified existing nodes unless marked CREATE.

**Relationship type reference for Bauteilgruppe nodes** (confirmed from existing graph):
| Plan label | Correct rel type |
|-----------|------------------|
| Bauteiltyp | `HAT_BAUTEILTYP` |
| Materialgruppe | `HAT_MATERIALGRUPPE` |
| WiederverwendungsArt | `HAT_WIEDERVERWENDUNGSART` |
| Beschaffungsweg | `HAT_BESCHAFFUNGSWEG` |
| Verbindungstechnik | `HAT_VERBINDUNGSTECHNIK` |
| Rueckbauverfahren | `HAT_RUECKBAUVERFAHREN` |
| Aufbereitungsverfahren | `HAT_AUFBEREITUNG` |
| ZustandsKlasse | `HAT_ZUSTANDSKLASSE` ← NEW rel type (first use) |
| Defekt | `HAT_DEFEKT` |
| PruefungNachweis | `HAT_PRUEFUNG` |
| Bauproduktstatus | `HAT_BAUPRODUKTSTATUS` |
| Leistungsanforderung | `HAT_LEISTUNGSANFORDERUNG` |
| Schadstoff | `HAT_SCHADSTOFF` |
| Logistik | `HAT_LOGISTIK` |
| Marktmodell | `HAT_MARKTMODELL` |
| AUS_BAUWERK | `AUS_BAUWERK` |
| EINGEBAUT_IN | `EINGEBAUT_IN` → targets Bauwerk node (Phase 1.5) |
| Methode | `HAT_METHODE` |

**Every Bauteilgruppe also requires (see CORRECTIONS O1–O3):**
- `HAT_BAUTEILEBENE → be_bauteilgruppe` (or `be_materialcharge` for Careno tile stocks)
- `HAT_STATUS → status_xxx` (see status table in CORRECTIONS O2)
- `HAT_RESSOURCENQUELLE → rq_donorgebaeude` (for BGs with source Bauwerk)

**Projekt ↔ Bauteilgruppe direction:** `Projekt -[HAT_BAUTEILGRUPPE]-> Bauteilgruppe`
Bauteilgruppe then links to receiving Bauwerk via `EINGEBAUT_IN → bw_xxx`.

### 7.1 Schärenmoosstrasse Bauteilgruppen

**bg_mage_bestand** — Existing buildings Micro + Dixa (preserved in place)
```
Bauteiltyp:        bt_wand, bt_decke
Materialgruppe:    mg_mineralisch
WiederverwendungsArt: wva_bestandserhalt
Beschaffungsweg:   bweg_eigenbestand
Verbindungstechnik: vt_verschraubung
ZustandsKlasse:    zk_unbekannt_pruefung_offen
Defekt:            def_keine_befunde
PruefungNachweis:  pr_statische_nachweisfuehrung, pr_zustandsbewertung
Bauproduktstatus:  bps_bestand_no_status
Leistungsanforderung: la_tragfaehigkeit, la_waermeschutz
Logistik:          log_transport
EINGEBAUT_IN:      bw_schaerenmoosstrasse_zuerich  [Bauwerk, Phase 1.5]
```

**bg_mage_hall** — Hall from UBS Altstetten (reused)
```
Bauteiltyp:        bt_decke, bt_wand
Materialgruppe:    mg_mineralisch
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_rueckbauprojekt
Rueckbauverfahren: rv_selektiver_rueckbau
Aufbereitungsverfahren: av_beton_anhaftungen_entfernen
ZustandsKlasse:    zk_unbekannt_pruefung_offen
Defekt:            def_oberflaechenmangel
PruefungNachweis:  pr_statische_nachweisfuehrung
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_tragfaehigkeit, la_waermeschutz
Logistik:          log_transport
AUS_BAUWERK:       bw_ubs_altstetten
EINGEBAUT_IN:      bw_schaerenmoosstrasse_zuerich  [Bauwerk, Phase 1.5]
```

**bg_mage_arcade** — Self-supporting steel arcade / Laubengang
```
Bauteiltyp:        bt_traeger
Materialgruppe:    mg_metall
WiederverwendungsArt: wva_direkte_wiederverwendung  [status unverified — note on node]
ZustandsKlasse:    zk_unbekannt_pruefung_offen
PruefungNachweis:  pr_korrosionspruefung
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_tragfaehigkeit
EINGEBAUT_IN:      bw_schaerenmoosstrasse_zuerich  [Bauwerk, Phase 1.5]
```

### 7.2 UMAR Bauteilgruppen

**bg_umar_timber** — Untreated timber structure + facade
```
Bauteiltyp:        bt_wand, bt_fassade
Materialgruppe:    mg_holz_biobasiert
WiederverwendungsArt: wva_design_for_disassembly
Beschaffungsweg:   bweg_ausschreibung
Verbindungstechnik: vt_verschraubung, vt_steckverbindung
Rueckbauverfahren: rv_selektiver_rueckbau
Aufbereitungsverfahren: av_holzaufbereitung
ZustandsKlasse:    zk_neuwertig
Defekt:            def_keine_befunde
PruefungNachweis:  pr_festigkeitssortierung_holz
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_rueckbaubarkeit, la_waermeschutz
Schadstoff:        s_holzschutzmittel  [check: untreated = none expected]
Logistik:          log_transport
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_alu_copper** — Aluminium + copper facade elements
```
Bauteiltyp:        bt_fassade
Materialgruppe:    mg_metall
WiederverwendungsArt: wva_recycling
Verbindungstechnik: vt_verschraubung
Rueckbauverfahren: rv_demontage
Aufbereitungsverfahren: av_entrosten_korrosionsbehandlung
ZustandsKlasse:    zk_neuwertig
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_rueckbaubarkeit
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_wabbes_handles** — Jules Wabbes door handles (loan from Rotor)
```
Bauteiltyp:        bt_tuer
Materialgruppe:    mg_metall
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_direktvermittlung
Rueckbauverfahren: rv_ausbau_von_bauteilen, rv_zerstoerungsarme_bergung
Aufbereitungsverfahren: av_reinigung, av_rekonditionierung
ZustandsKlasse:    zk_gebrauchsspuren_funktional
Defekt:            def_keine_befunde
PruefungNachweis:  pr_sichtpruefung, pr_dokumentenpruefung_bestand
Bauproduktstatus:  bps_project_specific
Leistungsanforderung: la_rueckbaubarkeit
Logistik:          log_lagerung, log_transport
AUS_BAUWERK:       bw_generale_de_banque_brussels
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
Marktmodell:       mm_leasing  [loan / return model]
```

**bg_umar_magna_glass** — Sintered recycled-glass panels (Magna Glaskeramik)
```
Bauteiltyp:        bt_fassade
Materialgruppe:    mg_glas_keramik
WiederverwendungsArt: wva_upcycling, wva_recycling
Beschaffungsweg:   bweg_direktvermittlung
Aufbereitungsverfahren: av_remanufacturing
ZustandsKlasse:    zk_neuwertig
Defekt:            def_keine_befunde
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_rueckbaubarkeit
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_mycelium** — Ecovative mycelium insulation boards
```
Bauteiltyp:        bt_daemmung
Materialgruppe:    mg_daemmstoff  [CORRECTION: not wood; mycelium = bio-based insulation;
                                   mg_holz_biobasiert would be wrong label]
material_note:     "mycelium / pilzbasiert — Ecovative Grow"
WiederverwendungsArt: wva_recycling  [composting at EoL]
Verbindungstechnik: vt_reversible_fuegung
Rueckbauverfahren: rv_demontage
ZustandsKlasse:    zk_neuwertig
Bauproduktstatus:  bps_project_specific
Leistungsanforderung: la_rueckbaubarkeit, la_waermeschutz
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_carpets** — Desso/Tarkett carpets (take-back service)
```
Bauteiltyp:        bt_boden
Materialgruppe:    mg_kunststoff
WiederverwendungsArt: wva_recycling
Beschaffungsweg:   bweg_leihmodell
Rueckbauverfahren: rv_ausbau_von_bauteilen
Aufbereitungsverfahren: av_remanufacturing
ZustandsKlasse:    zk_neuwertig
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_rueckbaubarkeit
Logistik:          log_transport
Marktmodell:       mm_take_back_service
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_lindner_ceiling** — Lindner Plafotherm heated/chilled ceiling panels
```
Bauteiltyp:        bt_decke
Materialgruppe:    mg_verbundstoff
WiederverwendungsArt: wva_design_for_disassembly
Beschaffungsweg:   bweg_leihmodell
Verbindungstechnik: vt_verschraubung, vt_klemmverbindung
Rueckbauverfahren: rv_demontage
ZustandsKlasse:    zk_neuwertig
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_rueckbaubarkeit
Logistik:          log_transport
Marktmodell:       mm_take_back_service
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

**bg_umar_recycled_bricks** — Recycled bricks + recycled insulation
```
Bauteiltyp:        bt_wand
Materialgruppe:    mg_mineralisch
WiederverwendungsArt: wva_direkte_wiederverwendung, wva_recycling
Beschaffungsweg:   bweg_lager
Rueckbauverfahren: rv_ausbau_von_bauteilen
Aufbereitungsverfahren: av_moertelentfernung_ziegel
ZustandsKlasse:    zk_gebrauchsspuren_funktional
Schadstoff:        s_pak  [old bituminous coatings — check]
Bauproduktstatus:  bps_project_specific
EINGEBAUT_IN:      bw_umar_unit_duebendorf  [Bauwerk, Phase 1.5]
```

### 7.3 ELEMENTA Bauteilgruppen

**bg_elementa_baufeld_c** — Reused RC column-beam structure (Baufeld C)
```
Bauteiltyp:        bt_stuetze, bt_decke
Materialgruppe:    mg_mineralisch
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_bauteilboerse, bweg_digitale_plattform, bweg_rueckbauprojekt
Verbindungstechnik: vt_bolzenverbindung, vt_verschraubung
Rueckbauverfahren: rv_selektiver_rueckbau
Aufbereitungsverfahren: av_beton_anhaftungen_entfernen,
                        av_betonfertigteil_tagging_sortierung,
                        av_betonfertigteil_saegen
ZustandsKlasse:    zk_unbekannt_pruefung_offen
Defekt:            def_oberflaechenmangel, def_karbonatisierung
PruefungNachweis:  pr_bohrkernpruefung_beton, pr_dokumentenpruefung_bestand,
                   pr_statische_nachweisfuehrung, pr_schadstoffpruefung
Bauproduktstatus:  bps_project_specific, bps_baupg_ch
Leistungsanforderung: la_tragfaehigkeit, la_dauerhaftigkeit
Schadstoff:        s_pak, s_asbest  [parking garage ~1970s; check joint sealing]
Logistik:          log_just_in_time, log_materialmatching,
                   log_lokale_wiederverwendung, log_zwischenlagerung, log_bauteiltracking
AUS_BAUWERK:       bw_lysbueechel_garage_basel
EINGEBAUT_IN:      bw_elementa_walkeweg_basel  [Bauwerk, Phase 1.5]
```

**bg_elementa_baufeld_d** — RC rib-panel load-bearing exterior wall (Baufeld D)
```
Bauteiltyp:        bt_wand, bt_fassade
Materialgruppe:    mg_mineralisch
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_bauteilboerse, bweg_rueckbauprojekt
Verbindungstechnik: vt_verschraubung
Rueckbauverfahren: rv_selektiver_rueckbau
Aufbereitungsverfahren: av_beton_anhaftungen_entfernen,
                        av_betonfertigteil_tagging_sortierung
ZustandsKlasse:    zk_unbekannt_pruefung_offen
PruefungNachweis:  pr_bohrkernpruefung_beton, pr_statische_nachweisfuehrung
Bauproduktstatus:  bps_project_specific, bps_baupg_ch
Leistungsanforderung: la_tragfaehigkeit, la_dauerhaftigkeit
Schadstoff:        s_pak, s_asbest
Logistik:          log_just_in_time, log_materialmatching, log_zwischenlagerung
AUS_BAUWERK:       bw_lysbueechel_garage_basel
EINGEBAUT_IN:      bw_elementa_walkeweg_basel  [Bauwerk, Phase 1.5]
```

**bg_elementa_brettstapel** — Brettstapeldecken (new renewable wood)
```
Bauteiltyp:        bt_decke
Materialgruppe:    mg_holz_biobasiert
WiederverwendungsArt: wva_weiterbauen_im_bestand
Verbindungstechnik: vt_steckverbindung
ZustandsKlasse:    zk_neuwertig
Bauproduktstatus:  bps_baupg_ch
Leistungsanforderung: la_waermeschutz, la_schallschutz
EINGEBAUT_IN:      bw_elementa_walkeweg_basel  [Bauwerk, Phase 1.5]
```

**bg_elementa_clay** — Lehmbauplatten + Lehmputz
```
Bauteiltyp:        bt_wand
Materialgruppe:    mg_lehm_erde
WiederverwendungsArt: wva_direkte_wiederverwendung
Aufbereitungsverfahren: av_lehm_sieben_mischen
ZustandsKlasse:    zk_neuwertig
Leistungsanforderung: la_waermeschutz, la_feuchteschutz
EINGEBAUT_IN:      bw_elementa_walkeweg_basel  [Bauwerk, Phase 1.5]
```

### 7.4 Careno Bauteilgruppen

> Note: These Bauteilgruppen have no `EINGEBAUT_IN` relationship — there is no receiving building. Link via `TEIL_VON_PROGRAMM → prog_be_circular` to anchor them in the graph.

**bg_careno_raw_tiles** — Salvaged ceramic flooring tiles 1900–1960 (unprocessed stock)
```
Bauteiltyp:        bt_boden
Materialgruppe:    mg_glas_keramik
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_rueckbauprojekt
Rueckbauverfahren: rv_ausbau_von_bauteilen, rv_zerstoerungsarme_bergung
Aufbereitungsverfahren: av_entmoertelung_von_fliesen, av_reinigung,
                        av_materialsortierung_chargenbildung
ZustandsKlasse:    zk_unbekannt_pruefung_offen
Defekt:            def_riss, def_oberflaechenmangel
PruefungNachweis:  pr_sichtpruefung, pr_geometrische_vermessung
Bauproduktstatus:  bps_project_specific
Schadstoff:        s_bleifarbe  [tiles 1900–1960 may carry lead glaze — verify]
Logistik:          log_lagerung, log_materialverfuegbarkeit
```

**bg_careno_cleaned_tiles** — Re-Tile cleaned + quality-sorted tiles (product)
```
Bauteiltyp:        bt_boden
Materialgruppe:    mg_glas_keramik
WiederverwendungsArt: wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_digitale_plattform, bweg_lager
Aufbereitungsverfahren: av_entmoertelung_von_fliesen, av_qualitaetssicherung
ZustandsKlasse:    zk_gebrauchsspuren_funktional
Defekt:            def_keine_befunde
Bauproduktstatus:  bps_project_specific  [Re-Tile certificate by Rotor/RotorDC]
Logistik:          log_bauteiltracking
```

### 7.5 Circl Bauteilgruppen

**bg_circl_larch** — Locally-sourced larch timber structure
```
Bauteiltyp:        bt_traeger, bt_wand, bt_decke
Materialgruppe:    mg_holz_biobasiert
WiederverwendungsArt: wva_design_for_disassembly
Beschaffungsweg:   bweg_direktvermittlung
Verbindungstechnik: vt_reversible_fuegung
Rueckbauverfahren: rv_selektiver_rueckbau  [completed by lcp-circulair, 2025]
Aufbereitungsverfahren: av_holz_festigkeitssortierung
ZustandsKlasse:    zk_gebrauchsspuren_funktional  [dismantled 2025; in storage]
PruefungNachweis:  pr_dokumentenpruefung_bestand, pr_festigkeitssortierung_holz
Bauproduktstatus:  bps_nta_8713  [NL reuse standard — EXACT HIT]
Leistungsanforderung: la_rueckbaubarkeit, la_tragfaehigkeit
Logistik:          log_bauteiltracking, log_lokale_wiederverwendung
EINGEBAUT_IN:      bw_circl_pavilion_amsterdam  [Bauwerk, Phase 1.5]
```

**bg_circl_firehose_cabinets** — Second-hand fire-hose-reel cabinets (New Horizon)
```
Bauteiltyp:        bt_technik
Materialgruppe:    mg_metall
WiederverwendungsArt: wva_urban_mining, wva_direkte_wiederverwendung
Beschaffungsweg:   bweg_direktvermittlung
Rueckbauverfahren: rv_ausbau_von_bauteilen
Aufbereitungsverfahren: av_reinigung
ZustandsKlasse:    zk_gebrauchsspuren_funktional
Defekt:            def_korrosion
PruefungNachweis:  pr_sichtpruefung, pr_korrosionspruefung
Bauproduktstatus:  bps_nta_8713
Marktmodell:       mm_kauf_gebraucht
EINGEBAUT_IN:      bw_circl_pavilion_amsterdam  [Bauwerk, Phase 1.5]
```

**bg_circl_plants** — Roof garden / plant modules (Donkergroen)
```
Bauteiltyp:        bt_dach
Materialgruppe:    mg_holz_biobasiert
WiederverwendungsArt: wva_design_for_disassembly
Beschaffungsweg:   bweg_direktvermittlung
Rueckbauverfahren: rv_demontage
EINGEBAUT_IN:      bw_circl_pavilion_amsterdam  [Bauwerk, Phase 1.5]
```

**bg_circl_solar_boiler** — Fasolar solar boiler / facade
```
Bauteiltyp:        bt_technik, bt_fassade
Materialgruppe:    mg_metall
WiederverwendungsArt: wva_design_for_disassembly
Beschaffungsweg:   bweg_direktvermittlung
Rueckbauverfahren: rv_demontage
Leistungsanforderung: la_rueckbaubarkeit
EINGEBAUT_IN:      bw_circl_pavilion_amsterdam  [Bauwerk, Phase 1.5]
```

---

## PHASE 8 — Add project-level category relationships

Link the Projekt nodes to all relevant vocabulary nodes at the building/project level. These are the relationships that go on the Projekt node itself (not on Bauteilgruppen).

### p_schaerenmoosstrasse_zuerich
```
HAT_INTERVENTION:         bai_umnutzung, bai_umbau
HAT_NUTZUNG:              nut_wohnen, nut_gewerbe
HAT_METHODE:              meth_form_follows_availability, meth_reuse_assessment
REFERENZIERT_NORM:        norm_sia_schweiz  (SIA 500 barrier-free, SIA 261 seismic)
HAT_HUERDE:               h_technische_freigabe  [×3 aspects: thermal, seismic, roof load — single node, single rel]
                          h_entwurfsbindung
HAT_WIRTSCHAFT:           wi_capex_hoeher_subvention
TEIL_VON_PROGRAMM:        prog_wettbewerb, prog_stiftung_pwg
HAT_DOMINANT_AKZEPTANZ:   ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK:            bw_schaerenmoosstrasse_zuerich  [new, Phase 1.5]
```

### p_umar_unit
```
HAT_INTERVENTION:         bai_neubau
HAT_NUTZUNG:              nut_wohnen
HAT_METHODE:              meth_design_for_disassembly, meth_reversibilitaet,
                          meth_urban_mining, meth_bauteilkatalogisierung
REFERENZIERT_NORM:        norm_sia_schweiz
HAT_HUERDE:               h_fehlende_standardisierung, h_fehlende_datenstandards, h_datenluecke
HAT_WIRTSCHAFT:           wi_capex_hoeher_opex_payback, wi_hidden_costs_lagerung_pruefung,
                          wi_geschaeftsmodell
HAT_DOMINANT_MARKTMODELL: mm_take_back_service  [carpets + ceiling service contracts]
NUTZT_TOOL:               tool_bim_bauteilkatalog
TEIL_VON_PROGRAMM:        prog_forschungsprojekt, prog_reallabor, prog_nest_empa
HAT_DOMINANT_AKZEPTANZ:   ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK:            bw_umar_unit_duebendorf  [new, Phase 1.5]
```

### p_elementa_walkeweg
```
HAT_INTERVENTION:         bai_neubau
HAT_NUTZUNG:              nut_wohnen
HAT_METHODE:              meth_pre_deconstruction_audit, meth_bauteilkatalogisierung,
                          meth_materialinventur, meth_form_follows_availability
REFERENZIERT_NORM:        norm_sia_schweiz
HAT_HUERDE:               h_entwurfsbindung, h_verfuegbarkeitsproblem,
                          h_heterogenitaet_chargen, h_terminunsicherheit, h_toleranzen
HAT_WIRTSCHAFT:           wi_capex_niedriger_direkter_ersparnis, wi_capex_hoeher_subvention,
                          wi_hidden_costs_lagerung_pruefung, wi_lebenszykluskosten
HAT_DOMINANT_MARKTMODELL: mm_plattform_vermittelt
NUTZT_SOFTWARE:           software_ecotool
NUTZT_TOOL:               tool_bauteilkatalog
HAT_ZERTIFIZIERUNG:       zbs_ecotool  [Pflichtnachweis Wettbewerb — see C-note F3]
TEIL_VON_PROGRAMM:        prog_wettbewerb, prog_kommunales_programm
HAT_DOMINANT_AKZEPTANZ:   ak_oeffentlicher_bauherr_pilot
NUTZT_BAUWERK:            bw_elementa_walkeweg_basel  [new, Phase 1.5]
```

### p_careno_becircular
```
HAT_METHODE:       meth_wiederverwendungskriterien, meth_building_material_scouting
HAT_HUERDE:        h_aufbereitungsaufwand, h_materialqualitaet_unklar,
                   h_fehlende_standardisierung, h_bruch_beschaedigungsrisiko,
                   h_gewaehrleistung
HAT_WIRTSCHAFT:    wi_capex_hoeher_subvention, wi_preisbildung, wi_geschaeftsmodell
HAT_DOMINANT_MARKTMODELL: mm_take_back_service
TEIL_VON_PROGRAMM: prog_forschungsprojekt, prog_be_circular
```

### p_pavilion_circl_amsterdam
```
HAT_INTERVENTION:         bai_neubau
HAT_NUTZUNG:              nut_buero, nut_mischnutzung
HAT_METHODE:              meth_design_for_disassembly, meth_zirkulaere_ausschreibung,
                          meth_urban_mining, meth_abrissmonitoring
HAT_DOMINANT_MARKTMODELL: mm_intra_konzern  [MIGRATE from p_circl_abn_amro in P0-B]
HAT_WIRTSCHAFT:           wi_capex_hoeher_marketing_payback, wi_restwert
NUTZT_TOOL:               tool_material_passports_maconda
NUTZT_BAUWERK:            bw_circl_pavilion_amsterdam  [new, Phase 1.5]
```

---

## PHASE 9 — Actor relationships

For each new actor created in Phase 4, add `BETEILIGT_AN` or `ASSOZIIERT_MIT_PROJEKT` relationships to the relevant Projekt node with a `rolle` property.

**Already-linked actors that must NOT be re-linked (already have `ASSOZIIERT_MIT_PROJEKT`):**

| id | Project | Verified role |
|---|---|---|
| `studio_trachsler_hoffmann` | `p_schaerenmoosstrasse_zuerich` | design architect |
| `daniel_hoffmann` | `p_schaerenmoosstrasse_zuerich` | architect (person) |
| `gian_trachsler` | `p_schaerenmoosstrasse_zuerich` | architect (person) |
| `dirk_e_hebel` | `p_umar_unit` | architect / researcher |
| `felix_heisel` | `p_umar_unit` | researcher |
| `vanessa_propach` | `p_umar_unit` | researcher |
| `carla_ferrando_costansa` | `p_elementa_walkeweg` | architect (role null — set to "Architekt") |
| `pablo_garrido_arnaiz` | `p_elementa_walkeweg` | architect (role null — set to "Architekt") |
| `lionel_billiet` | `p_careno_becircular` | Rotor researcher |
| `sebastien_paulet` | `p_careno_becircular` | Rotor researcher |
| `hans_hammink` | `p_pavilion_circl_amsterdam` | Bauherrschaft / ABN AMRO side |

Action for `carla_ferrando_costansa` and `pablo_garrido_arnaiz`: update `rolle` property to `"Architekt"` (currently null).

Existing actor nodes that need new relationship to their project (not yet linked):

| Existing actor | Project | Rolle |
|---|---|---|
| `parabase` | `p_elementa_walkeweg` | Architekt (lead) |
| `immobilien_basel_stadt` | `p_elementa_walkeweg` | Bauherrschaft |
| `hochbauamt_basel_stadt` | `p_elementa_walkeweg` | Bauherrschaft (confirm overlap with IBS) |
| `zirkular_gmbh` | `p_elementa_walkeweg` | Wiederverwendungsberatung / Bauteilkatalog |
| `Rotor` | `p_careno_becircular` | Forschungsleitung |
| `rotordc` | `p_careno_becircular` | Re-Tile service delivery |
| `rotordc` | `p_umar_unit` | Bauteillieferant (Wabbes handles) |
| `de_architekten_cie` | `p_pavilion_circl_amsterdam` | Architect |
| `new_horizon` | `p_pavilion_circl_amsterdam` | Urban mining supplier |
| `de_groot_en_visser` | `p_pavilion_circl_amsterdam` | Solartechnik |

---

## PHASE 10 — Source provenance

For every new node created in this run, add a `BELEGT_IN` relationship to a `Quelle` node. Either reuse existing Quelle nodes already linked to the Projekt nodes, or create a minimal new Quelle node referencing the inbox dossier file as the current source.

Minimum properties for a run-created Quelle:
```
source_file: "_neo4j/intake/inbox/projects/[filename].md"
run: "2026-05-19_inbox_projects_import"
review_status: "inbox_unverified"
```

---

## PHASE 11 — Post-import checks

Run these verification queries after import.

```cypher
-- 1. Confirm all 5 Projekt nodes have LIEGT_IN_STADT
MATCH (p:Projekt) WHERE p.id IN [
  'p_schaerenmoosstrasse_zuerich','p_umar_unit','p_elementa_walkeweg',
  'p_careno_becircular','p_pavilion_circl_amsterdam'
]
OPTIONAL MATCH (p)-[:LIEGT_IN_STADT]->(s:Stadt)
RETURN p.id, s.id

-- 2. Confirm no remaining p_circl_abn_amro node
MATCH (n {id: 'p_circl_abn_amro'}) RETURN n.id

-- 3. Confirm Werner Sobek duplicate removed from UMAR
MATCH (p:Projekt {id:'p_umar_unit'})-[:ASSOZIIERT_MIT_PROJEKT]->(a:Akteur)
WHERE a.name = 'Werner Sobek'
RETURN a.id, a.name

-- 4. Confirm Lysbüchel source building is linked to all three ELEMENTA Bauteilgruppen
MATCH (bg:Bauteilgruppe)-[:AUS_BAUWERK]->(bw:Bauwerk {id:'bw_lysbueechel_garage_basel'})
RETURN bg.id, bw.id

-- 5. Confirm Careno Bauteilgruppen have no dangling EINGEBAUT_IN
MATCH (bg:Bauteilgruppe) WHERE bg.id STARTS WITH 'bg_careno'
OPTIONAL MATCH (bg)-[:EINGEBAUT_IN]->(p)
RETURN bg.id, p.id
```

---

## Summary of nodes to create

| Label | Count |
|-------|-------|
| `Stadt` | 2 |
| `Bauwerk` (source buildings) | 3 |
| `Bauwerk` (receiving buildings, Phase 1.5) | 4 |
| `Programm` | 3 |
| `Software` | 1 |
| `ZertifizierungBewertungssystem` | 1 |
| `Akteur` | 44 |
| `Bauteilgruppe` | 20 |
| **Total new nodes** | **78** |

**New relationship type introduced in this run:**
- `HAT_ZUSTANDSKLASSE` (first use; `ZustandsKlasse` nodes exist, no incoming rels exist yet)

All other node types use **existing nodes only** — 0 new vocabulary nodes required.
