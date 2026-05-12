---
name: Neo4j schema catalogue
overview: |
  Metadata-only Neo4j schema for the recherche knowledge base: 52 node labels, five relationship types.
  This plan is the authoring source for _database/_system/NEO4J_SCHEMA.md (narrative spec) and
  NEO4J_SCHEMA_MAP.md (flat machine-oriented tables). German prose stays in Markdown under _database/;
  the graph holds ids, classifications, measurements, and edges. Exceptions—title and optional vendor
  fields—apply only to Software and Tool nodes (section 6).
todos:
  - id: neo4j-schema-md
    content: "Write _database/_system/NEO4J_SCHEMA.md: sections 1–8 of this plan as §1–§4, plus appendices A–G (A = plan section 4; B/C as plan; D = plan sections 5.4 + 7.1; E reuse_strategie; F GEHÖRT_ZU matrix; G HAT.art literals). 52 labels, five rel types; tables follow authoring rules (no bold inside cells for rel names)."
    status: pending
  - id: neo4j-schema-map-md
    content: "Write _database/_system/NEO4J_SCHEMA_MAP.md in lockstep: flat tables for every label (properties) and every rel type (allowed patterns + edge props); mirror NEO4J_SCHEMA.md §2–§4 and appendices F–G."
    status: pending
isProject: false
---

# Neo4j schema catalogue (plan)

## 1. Goal and deliverables

Author `[_database/_system/NEO4J_SCHEMA.md](_database/_system/NEO4J_SCHEMA.md)` in order: node-type catalogue, node properties, edge-type catalogue, edge properties, then appendices **A–G** as listed below.

Author `[_database/_system/NEO4J_SCHEMA_MAP.md](_database/_system/NEO4J_SCHEMA_MAP.md)` as a compact mirror: every label with full property list; every relationship type with allowed source and target labels, cardinality, and edge properties. No narrative duplication—tables only.

Optional later: generate both files from a single YAML or JSON source; not required for the first pass.

Visual sample vertices (Browser/demo only): [neo4j_schema_visual_nodes_attachment.md](neo4j_schema_visual_nodes_attachment.md).

## 2. Counts

| Item | Value |
| --- | --- |
| Neo4j labels | **52** — each label is a **primary** node type (first-class `:Label` with `UNIQUE` on `id`; no secondary or “taxonomy-only” tier) |
| Relationship types | **5**: `IST`, `HAT`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN` |

## 3. Authoring rules (normative for Markdown tables)

- In table cells, write relationship names as plain text: `IST`, `HAT`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN` (no bold wrappers around rel names in cells).
- Allowed `GEHÖRT_ZU` triples `(sourceLabel, rolle, targetLabel)`: **Appendix F** only.
- Allowed `HAT.art` literals: **Appendix G** only.
- `BELEGT_IN`: only when the shorthand resolves to an existing `(:Quelle)`; when the subject is a classification node (any label in section 5.2), only if the source defines that taxonomy entry (not mere prose mention).
- `HAT`: keep `:Huerde` and `:PruefungNachweis` disjoint in meaning; no `IST` or `GEHÖRT_ZU` between `:Huerde` nodes and no parent “cluster” hurdle nodes.
- Measurements: if `:Bauwerk` exists, building-scale measurements live on `:Bauwerk`; otherwise on `:Fallbeispiel` until a `:Bauwerk` is materialised; component-group and reuse KPIs on `:Bauteilgruppe` (including `reuse_einsatz/`); relational quantities via `BENUTZT` (see section 4).

## 4. Modeling principles (Appendix A — single source in this plan)

- **Every label is primary.** All **52** labels are first-class node types: each uses its own Neo4j `:Label`, the same `UNIQUE` constraint on `id`, and the same metadata-only rules; differences are only which optional properties apply (for example `title` on `:Software` / `:Tool`).
- **Metadata-only graph.** No `body_md`, `legacy_paths`, `build_status`, or raw-label properties on nodes. German prose stays in `_database/<entity>/<id>/index.md`. The `title` property (and optional fields per section 6) exists **only** on `(:Software)` and `(:Tool)`.
- **Modes A/B/C** coexist; Mode A (property) for identifiers, discriminators (`art`, `programm_typ`, `axis`), and quantitative measurements (with optional `_alt` / `_vertrauensgrad` shadows where specified in the schema doc).
- **Measurement placement.** Physical component-group quantities **and** reuse-action KPIs (e.g. CO₂) → `:Bauteilgruppe` (including rows exported from `reuse_einsatz/`). Relational quantities → `BENUTZT`.
- **Roles on edges.** Actor role is an edge property, never a separate “role node” target: `HAT { art: 'akteur', rolle: '<Akteurrolle.id>' }` → the **organisation-actor** node (one of the primary labels in section 6.1, including `:Akteur` fallback when no slug resolves); `HAT { art: 'person', rolle: '<Akteurrolle.id>' }` → `(:Person)` for natural persons. The eight canonical `(:Akteurrolle)` nodes are dictionary only (section 5.5). Organisation **kind** is encoded by the **Neo4j primary label** chosen from the first canonical `akteurtyp/<slug>` in `index.md` (section 6.1)—not a string property and not `IST` to separate type nodes. **`:Person`** carries natural-person identity only (same Markdown heuristics as before).
- **Citations.** No `quelle_id` / `quelle_label` on nodes or on non-evidence edges. Use `BELEGT_IN` (claim → `(:Quelle)`) only when resolvable; optional `eigenschaft` scopes the cited field.
- **Naming.** German PascalCase labels, SCREAMING_SNAKE relationship types, snake_case properties.
- **`:Status`.** Exactly seven canonical nodes (section 5.9); link with **`HAT { art: "status" }`** from `:Bauwerk` (building lifecycle), optionally `:Fallbeispiel` / `:Bauteilgruppe` (including reuse-episode lifecycle from `reuse_einsatz/`). Label `:Bauobjektstatus` removed.
- **`:WiederverwendungsArt`.** Three axes via `axis` property; *Art der Wiederverwendung* (`axis: "reuse_strategie"`, six canonical ids) attaches with `HAT { art: "wiederverwendungsart" }` only—details **Appendix E**.
- **Verbindungstechnik vs Reversibilität.** Joining methods from `fuegung_verbindung/` technique folders → `:Verbindungstechnik` via `HAT { art: 'verbindungstechnik' }`. `:Reversibilitaet` is separate (`HAT { art: 'reversibilitaet' }`), not imported from `fuegung_verbindung/`, not nested under `:Verbindungstechnik`.
- **`:Reversibilitaet` vs `:Methode { id: "Reversibilitaet" }`.** The label holds the detachability scale; `_database/methode/Reversibilitaet/` is methodological and stays `:Methode`, typically `BENUTZT`. Do not merge into one label.
- **Constraints.** `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE` for every label.

## 5. Node-type catalogue

### 5.1 Folder-to-node rule

Each `_database/<label>/<id>/` folder (where that label maps to a Neo4j label) yields one node with `id` from the subfolder name, unless a section below states a merge, rename, or export normalisation.

Example:

```text
_database/norm/                  → Label :Norm
_database/norm/DIN_18940/      → (:Norm { id: "DIN_18940" })
```

Exceptions: section 5.4 (no label), section 5.2 (merge and export conventions for specific labels), section 5.8 (id readability).

### 5.2 All node labels (52)

Every label is a **primary** node type: one Neo4j `:Label`, `UNIQUE` on `id`, same authoring rules. There is **no** `:Tooltyp` label (`tooltyp/` → properties on `:Tool` / `:Software`, §5.4).

The **Examples** column lists up to **20** instance `id` values from `_database/_system/node_inventory.csv` (sorted, unique per label) where applicable; `akteur/` rows split into **`:Person`** vs **organisation-actor labels** using `index.md` heuristics and the slug→label map (§6.1). Regenerate: `python _scripts/generate_plan_section_5_2.py` (generator emits one §5.2 row per organisation-actor label and per-label examples).

| Label | Folder(s) / provenance | Notes | Examples (≤20 `id`s) |
| --- | --- | --- | --- |
| `:PlanungArchitekturIngenieurwesen` | `akteur/` | Organisations whose `index.md` resolves to slug `planung_architektur_ingenieurwesen` (§6.1); not natural persons | Bellastock, CITYFOERSTER, Circular_Structural_Design, Huetten_und_Palaeste, LXSY_Architektur, Lendager, PARABASE, Rotor, Superuse_Studios, Werner_Sobek, ZRS_Architekten_Ingenieure, baubuero_in_situ_zirkular |
| `:ForschungLehreWissenstransfer` | `akteur/` | Slug `forschung_lehre_wissenstransfer` | Bauhaus_Erde, Natural_Building_Lab, VDI_ZRE, Wuppertal_Institut |
| `:OeffentlicheInstitutionenFoerderung` | `akteur/` | Slug `oeffentliche_institutionen_foerderung` | BBSR_Zukunft_Bau, BIM_Berlin, Bundesstiftung_Bauakademie, Bundesstiftung_Baukultur, ReUse_Berlin, Umweltbundesamt |
| `:KammernVerbaendeNgosNetzwerke` | `akteur/` | Slug `kammern_verbaende_ngos_netzwerke` | Architects_for_Future_Deutschland, Architektenkammer_Berlin_A_Wie_Zirkulaer, BDA_Bund_Deutscher_Architektinnen_Architekten, C2C_NGO, Circular_Berlin, DGNB, Phase_Nachhaltigkeit, re_source_Stiftung |
| `:UnternehmerverbandHistorischeBaustoffeUHBMd` | `akteur/` | Slug `Unternehmerverband_Historische_Baustoffe_UHB_md` (§6.1) | Unternehmerverband_Historische_Baustoffe_UHB |
| `:MaterialinitiativenHubs` | `akteur/` | Slug `materialinitiativen_hubs` | BIZH, CRCLR_House, Haus_der_Materialisierung, IfM_Initiativen_fuer_Materialkreislaeufe, Kunst_Stoffe_Berlin, Material_Mafia |
| `:ReuseBeratungProzessdienstleister` | `akteur/` | Slug `reuse_beratung_prozessdienstleister` | Drees_und_Sommer, EPEA, Zirkular_GmbH |
| `:Professur` | `akteur/` | Slug `professur` (after optional alias pass) | Nachhaltiges_Bauen |
| `:Akteur` | `akteur/` | **Fallback only:** organisation in `akteur/` when **no** §6.1 slug resolves—not used for persons | Arup, BLAF_Architecten, Bauteilboerse_Bremen, Bauteilboerse_Hannover, Bauteilnetz_Deutschland, Cleveland_Steel_and_Tubes, Concular, Consolis_Parma, IMd_Raadgevende_Ingenieurs, Lindner_Group_ReUsed_Products, Madaster, Ramboll_Finland, Restado, Rotor_DC, Skanska_Finland, Umacon, cepezed |
| `:Akteurrolle` | `akteurrolle/` | Twenty-one legacy folders → eight canonical `id`s (§5.5); cells show folder names. | Architektur, Aufbereitung_Refurbishment, Bauausfuehrung, Bauherr_Auftraggeber, Betreiber_Nutzer, Brandschutz_Barrierefreiheit, Fassade, Forschung_Dokumentation, Kunst_Gestaltung, Landschaftsplanung, Materiallieferant, Nachhaltigkeitsberatung, Oeffentliche_Hand, Projektbeteiligte_Unbestimmt, Projektmanagement_Koordination, Pruefung_Qualitaetssicherung, Reuse_Beratung, Rueckbau_Demontage, Stahlbau_Fertigung, TGA_Gebaeudetechnik |
| `:Aufbereitungsverfahren` | `aufbereitungsverfahren/` |  | Drahtglasschneiden, Entmoertelung_von_Fliesen, Holzaufbereitung, Leuchten_Refurbishment, Qualitaetssicherung, Reinigung, Rekonditionierung, Remanufacturing, Reparatur, Verstaerkung, Zuschnitt |
| `:BauaufgabeIntervention` | `bauaufgabe_intervention/` |  | Aufstockung, Erweiterung, Fit_out, Neubau, Rueckbau, Sanierung, Translozierung, Umbau, Umnutzung, Wiederaufbau |
| `:Bauteilebene` | `bauteilebene/` |  | Bauteilgruppe, Einzelbauteil, Gebaeudeteil, Materialcharge, Oberflaechenschicht, System |
| `:Bauteilgruppe` | `bauteilgruppe/` (optional), `reuse_einsatz/`, inventory | Physical component group **and** reuse-episode anchor: `reuse_einsatz/` (canonical), optional `bauteilgruppe/`; mass + reuse KPIs (e.g. CO₂) on the same node (§5.8). **Individual `id` (folder slug) is *bauteil-centric*: the readable tail names the Bauteil / Baugruppe / homogenes Los; a leading `{fall}__{nnn}__` segment is only for uniqueness and traceability—full case or supplier narrative stays in Markdown / edges, not in the tail.** Examples = current inventory (may still carry legacy narrative tails). | 55_Great_Suffolk_Street_London__001__Stahlprofile_f_r_neuen_externen_Kern, 55_Great_Suffolk_Street_London__002__Stahl_aus_1_Broadgate, 55_Great_Suffolk_Street_London__003__Reclaimed_stock_von_Cleveland, 55_Great_Suffolk_Street_London__004__Bestandslagerhaus, 55_Great_Suffolk_Street_London__005__Br_ckenlinks_zum_Kern, 55_Great_Suffolk_Street_London__006__Fassadenbekleidung_externer_Kern, AWM_Muenster_Circular_Office__001__Glastrennw_nde_und_T_ren, AWM_Muenster_Circular_Office__002__WC_Trennw_nde, AWM_Muenster_Circular_Office__003__Kabeltrassen_als_Regale, AWM_Muenster_Circular_Office__004__Kabeltrassen_und_LED_Leuchten, AWM_Muenster_Circular_Office__005__Wandverkleidung_aus_Stuhllehnen_sitzen, AWM_Muenster_Circular_Office__006__Sideboard_Holzeinbauten, AWM_Muenster_Circular_Office__007__Hanfkalksteine, AWM_Muenster_Circular_Office__008__Lehmbauw_nde, AWM_Muenster_Circular_Office__009__Akustik_Baffeln, AWM_Muenster_Circular_Office__010__M_bel, Association_house_Groeditz__001__Au_enwand_Fertigteile, Association_house_Groeditz__002__Innenwand_Fertigteile, Association_house_Groeditz__003__Innenwandrahmen, Association_house_Groeditz__004__Deckenelemente |
| `:Bauteiltyp` | `bauteiltyp/` |  | Ausbau, Boden, Dach, Daemmung, Decke, Fassade, Fenster, Fundament, Gelaender, Stuetze, Technik, Traeger, Treppe, Tuer, Wand |
| `:Bauteilzustand` | `bauteilzustand/` |  | Beschaedigt, Geprueft, Intakt, Kontaminiert, Korrodiert, Patiniert, Restlebensdauer_Bekannt, Restlebensdauer_Unklar, Ungeprueft |
| `:Bauwerk` | `bauobjekt/` | Physical built work + building-level measurements; `GEHÖRT_ZU { rolle: 'fallbeispiel' }` → `:Fallbeispiel` | 55_Great_Suffolk_Street_London, AWM_Muenster_Circular_Office, Altes_Hobelwerk_Winterthur, Areal_Walkeweg_Nord, Association_house_Groeditz, Association_house_Plauen, BOELL_LAB_Berlin, BedZED_London_Hackbridge, Berlin_Schildow_Pilot_House, Berlin_Schildow_Pilot_House_2, Bestandshalle_CRCLR_House, Bestandverplanzung_Pavilion_Muenchen, Big_Dig_Building_Boston, Big_Dig_House_Lexington_Massachusetts, BioPartner_5_Leiden_Oegstgeest, BlueCity_Offices_Rotterdam, Boulder_Fire_Station_3, Brent_Cross_Town_Primary_Substation_London, Brighton_Waste_House_Brighton, Broethen_Twin_House_Hoyerswerda |
| `:Bauweise` | `bauweise/` |  | Fertigteilbauweise, Holzbauweise, Hybridbauweise, Massivbauweise, Ortbetonbauweise, Stahlbauweise |
| `:Bausystem` | `bausystem/` |  | Betonfertigteil_System, Holz_Skelettbau, Holzrahmenbau, Plattenbau, Stahl_Skelettbau |
| `:Beschaffungsweg` | `beschaffungsweg/` |  | Ausschreibung, Bauteilboerse, Digitale_Plattform, Direktvermittlung, Eigenbestand, Informelles_Netzwerk, Rueckbauprojekt, Spende |
| `:Datenqualitaet` | `datenqualitaet/` |  | Belegt, Geschaetzt, Nicht_Belegt, Primaerquelle, Sekundaerquelle, Unbekannt, Widerspruechlich |
| `:Entwurfsentscheidung` | _(curated)_ | Curated (no folder); `HAT { art: 'entwurf' }` from `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe` | Etagenhoehe_durch_Bauteilmass, Fassadenschicht_als_Toleranzpuffer, Doppelfenster_als_Kastenfenster, Achsraster_nach_Bestand, Grundriss_nach_Bauteillaenge, Deckenhoehe_nach_Traegerhoehe, Anschlussdetail_angepasst, Erschliessungskern_verschoben |
| `:Fallbeispiel` | `fallstudie/`, `projekt/` | Case / project **record** (not the physical asset); merged on matching ids | 55_Great_Suffolk_Street_London, AWM_Muenster_Circular_Office, Altes_Hobelwerk_Winterthur, Areal_Walkeweg_Nord, Association_house_Groeditz, Association_house_Plauen, BIZH_Reallabor, BOELL_LAB_Berlin, Be_Ware, BedZED_London_Hackbridge, Berlin_Schildow_Pilot_House, Berlin_Schildow_Pilot_House_2, Bestandshalle_CRCLR_House, Bestandverplanzung_Pavilion_Muenchen, Big_Dig_Building_Boston, Big_Dig_House_Lexington_Massachusetts, BioPartner_5_Leiden_Oegstgeest, BlueCity_Offices_Rotterdam, Boulder_Fire_Station_3, Brent_Cross_Town_Primary_Substation_London |
| `:Funktionswechsel` | `funktionswechsel/` |  | Dekorative_Funktion, Gleiche_Funktion, Konstruktive_Funktion, Neue_Funktion, Technische_Funktion, Unbekannt |
| `:Huerde` | `huerde/` | General hurdles; not chemical substance nodes | Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit |
| `:Land` | `ort/` | `ort/` rows classified as country / macro-region → `:Land` (`ort_geo_label.py`, §5.1a) | Deutschland, Europa, Schweiz |
| `:Leistungsanforderung` | `leistungsanforderung/` |  | Brandschutz, Brandschutzanforderung, Dauerhaftigkeit, F90, Feuchteschutz, Feuerwiderstand, R90, REI90, Rueckbaubarkeit, Schadstofffreiheit, Schallschutz, Tragfaehigkeit, Waermeschutz |
| `:Logistik` | `logistik/` |  | Bauteiltracking, Just_in_Time, Lagerflaeche, Lagerung, Lokale_Wiederverwendung, Materialmatching, Materialverfuegbarkeit, Transport, Transportdistanz, Zwischenlagerung |
| `:Material` | `material/` |  | Aluminium, Beton, Daemmstoff, Glas, Gusseisen, Holz, Keramik, Kunststoff, Lehm, Naturstein, Recyclingbeton, Stahl, Stahlbeton, Stroh, Ziegel |
| `:Methode` | `methode/` | Includes `methode/Reversibilitaet/` — distinct from `:Reversibilitaet` label | Abrissmonitoring, Bauteilkatalogisierung, Building_Material_Scouting, Design_for_Disassembly, Form_Follows_Availability, Materialinventur, Pre_Deconstruction_Audit, ReUse_Assessment, ReUse_Ausschreibung, Reversibilitaet, Urban_Mining, Wiederverwendungskriterien, Zirkulaere_Ausschreibung |
| `:Norm` | `norm/` |  | DIN_18940, DIN_EN_15804, DIN_EN_15978, EN_1090, ISO_14040, ISO_14044, ISO_20887 |
| `:Nutzung` | `nutzung/` |  | Buero, Gewerbe, Infrastruktur, Kultur, Lager_Depot, Mischnutzung, Schule_Bildung, Sozialbau, Wohnen |
| `:Person` | `person/` (optional); `akteur/` (subset — see Notes) | `person/` when present; plus classified `akteur/<id>/`; label from `legacy_type: Person` or `akteurtyp/Person` in `index.md` (no separate `akteurtyp` property—`:Person` is the discriminator) | Dirk_Hebel, Kerstin_Mueller, Kerstin_Muller, desiree_mann, ellen_macarthur, fred_mudge, gj_bart_van_den_brink, patrick_teuffel |
| `:Programm` | `foerderprogramm/`, `programm_kontext/`, `kontextmerkmal/` | `programm_typ`: `foerderung` \| `forschungskontext`; `Pilotprojekt` merges with `kontextmerkmal/` | BBSM, Bestandserhalt_Policy, FCRBE, Foerderprogramm, Forschungsprojekt, Kommunales_Programm, PREUSE, Pilotprojekt, Reallabor, Reallabor_Be_Ware, Wettbewerb, Zukunftbau |
| `:Prozessphase` | `prozessphase/` |  | Aufbereitung, Betrieb, Dokumentation, Identifikation, Lagerung, Planung, Pruefung, Rueckbau, Transport, Wiedereinbau |
| `:PruefungNachweis` | `pruefung_nachweis/` |  | Abbrandbemessung, Brandschutznachweis, Eignungspruefung_Baulehm, Geometrische_Vermessung, Materialpruefung, Schadstoffscreening, Schweissbarkeitspruefung, Sichtpruefung, Statische_Nachweisfuehrung, Zugversuch, Zustandsbewertung |
| `:Quelle` | `quelle/` | Citation target | AGENTS_md, Geb_ude_55_Great_Suffolk_Street_London_md, Geb_ude_AWM_Muenster_Circular_Office_md, Geb_ude_Association_house_Groeditz_md, Geb_ude_Association_house_Plauen_md, Geb_ude_BedZED_London_Hackbridge_md, Geb_ude_Berlin_Schildow_Pilot_House_2_md, Geb_ude_Berlin_Schildow_Pilot_House_md, Geb_ude_Bestandverplanzung_Pavilion_Muenchen_md, Geb_ude_Big_Dig_Building_Boston_md, Geb_ude_Big_Dig_House_Lexington_Massachusetts_md, Geb_ude_BioPartner_5_Leiden_Oegstgeest_md, Geb_ude_BlueCity_Offices_Rotterdam_md, Geb_ude_Boulder_Fire_Station_3_md, Geb_ude_Brent_Cross_Town_Primary_Substation_London_md, Geb_ude_Brighton_Waste_House_Brighton_md, Geb_ude_Broethen_Twin_House_Hoyerswerda_md, Geb_ude_CRCLR_House_Impact_Hub_Berlin_md, Geb_ude_CascadeUp_London_secondary_timber_glulam_demonstrator_md, Geb_ude_Charles_Malis_Molenbeek_md |
| `:RechtlicheBedingung` | `rechtliche_bedingung/` | Single node for `Gewaehrleistung`; no duplicate under `:Huerde` | Bauordnungsrecht, EU_Taxonomie, Gewaehrleistung, Produkthaftung, Vergaberecht, Zulassung_im_Einzelfall |
| `:Ressourcenquelle` | `ressourcenquelle/` |  | Baustelle, Bauteilboerse, Donor_Infrastruktur, Donorgebaeude, Haendler, Lager, Materialstockpile, Produktionsueberschuss, Unbekannt |
| `:Reversibilitaet` | — | Four fixed nodes; `HAT { art: 'reversibilitaet' }` only; no `fuegung_verbindung/` provenance | Reversibel, Teilweise_reversibel, Irreversibel, Unbekannt |
| `:Rueckbauverfahren` | `rueckbauverfahren/` |  | Ausbau_von_Bauteilen, Betonfraesen, Demontage, Selektiver_Rueckbau, Zerstoerungsarme_Bergung |
| `:Schadstoff` | `schadstoff/` | Stammdaten per substance folder; `HAT { art: "schadstoff" }` | Asbest, Bleifarbe, Holzschutzmittel, PAK, PCB |
| `:Software` | `software_digitaltool/` | First 20 slugs from `software_digitaltool/` (α) — **illustration**; export assigns `:Software` vs `:Tool` (§5.6) | Abriss_Atlas, BIM, Bauteilboerse_Bremen, Bauteilboerse_Hannover, Bauteilnetz_Deutschland, Bonsai_BlenderBIM, CMEx, Concular_Plattform, Cycle_Up, Dataview, Excess_Materials_Exchange, GIS_Urban_Mining, Globechain, IFC_Viewer, IfcOpenShell, Klimaschutz_Konfigurator, Library_of_Reuse, Lindner_Group_ReUsed_Products, Loopfront, Maconda_Materialpass |
| `:Stadt` | `ort/` | `ort/` rows not classified as `:Land` → `:Stadt` (`ort_geo_label.py`) | Aarhus, Arnhem, Asse, Barcelona, Basel, Berlin, Berlin_Neukoelln, Bleijerheide, Boston, Boulder, Brighton, Broethen, Bruessel, Colombelles, Copenhagen, Den_Bosch, Dilbeek, Duiven, Eindhoven, Enschede |
| `:Status` | `reuse_einsatzstatus/`, `bauobjektstatus/` | Seven canonical `id`s after export; examples are legacy folder names | Gebaut, Geplant, In_Bau, Prototyp, Prototypisch, Realisiert, Rueckgebaut, Temporaer, Unklar, Verworfen, Vorgeschlagen, Wettbewerb |
| `:Tool` | `software_digitaltool/` | Slugs 21–40 from `software_digitaltool/` (α) — **illustration** only (§5.6) | Maconda_ROMULUS, Madaster, Material_Index, Material_Reuse_Portal, One_Click_LCA, One_Click_LCA_Building_Circularity, Opalis, Platform_CB23, Pre_Demolition_Audit_Tools, QR_RFID_Materialtracking, Qflow, Restado, Reusefully_LINK, Rheaply, Rhino, RotorDB, RotorDC, SalvoWEB, Speckle, Superyard |
| `:Tragwerksprinzip` | `tragwerksprinzip/` |  | Fachwerk, Skeletttragwerk, Wand_Kern_Tragwerk, Wandtragwerk |
| `:Verbindungstechnik` | `fuegung_verbindung/` | Six technique folders only (§5.10); `Reversible_Fuegung/` excluded from examples | Klemmverbindung, Steckverbindung, Verleimung, Vermoertelung, Verschraubung, Verschweissung |
| `:WiederverwendungsArt` | `bewertungslogik_abgrenzung/`, `reuse_strategie/` | `axis`: `einordnung` \| `grundtyp` \| `reuse_strategie`; strategy: Appendix E | Adaptives_ReUse, Bestandserhalt, Bestandserhalt_Nicht_Direct_Reuse, Design_for_Disassembly, Direkte_Wiederverwendung, Kein_Direct_Reuse_Nachweis, Moebel_Dekoration_Nicht_Direct_Reuse, Recycling, Recycling_Nicht_Direct_Reuse, Refurbishment, Remanufacturing, Reuse_Anteil_Unklar, Same_Site_ReUse, Ungebaut_Nicht_Realisierte_Wiederverwendung, Upcycling, Urban_Mining, Weiterbauen_im_Bestand, Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung |
| `:Wiederverwendungskette` | `reuse_kette/` | Optional named chain; `reuse_kettenstation/` → `GEHÖRT_ZU` edges, not nodes | 55_Great_Suffolk_Street_London, AWM_Muenster_Circular_Office, BedZED_London_Hackbridge, Bestandverplanzung_Pavilion_Muenchen, Big_Dig_Building_Boston, Big_Dig_House_Lexington_Massachusetts, BioPartner_5_Leiden_Oegstgeest, BlueCity_Offices_Rotterdam, Boulder_Fire_Station_3, Brent_Cross_Town_Primary_Substation_London, Broethen_Twin_House_Hoyerswerda, CascadeUp_London_secondary_timber_glulam_demonstrator, Christ_Pavilion_Volkenroda, Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot, Circular_Pavilion_Paris, Europa_Building_Brussels, Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere, Holbein_Gardens_London, House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain, Jeugdkliniek_Ithaka_Emergis_Kloetinge |
| `:Wirtschaft` | `wirtschaft/` |  | Finanzierung, Geschaeftsmodell, Kostenvergleich, Lebenszykluskosten, Preisbildung, Restwert |
| `:ZertifizierungBewertungssystem` | `zertifizierung_bewertungssystem/` |  | BREEAM, DGNB, LEED, Paris_Proof, WELL |
### 5.4 Folders without their own label

Disposition for `_database/` folders that do not become a standalone Neo4j label (or merge into an existing one).

| Folder | Disposition |
| --- | --- |
| `fallstudie/`, `projekt/` | Merged into `:Fallbeispiel` |
| `reuse_kettenstation/` | Dropped—sequence via `GEHÖRT_ZU` from `:Bauteilgruppe` |
| `akteur_beteiligung/`, `bauobjekt_beteiligung/` | Dropped—roles on `HAT { art: 'akteur', rolle: … }` → organisation-actor label from §6.1 (including `:Akteur` fallback) or `HAT { art: 'person', rolle: … }` → `(:Person)` |
| `person/` | Optional dedicated folder for `:Person` (when used); until populated, persons also come from classified `akteur/<id>/` (see §5.2) |
| `datenpunkt/` | Dropped—measurements as node properties |
| `kennwertdefinition/` | Dropped—names become property keys |
| `tooltyp/` | Dropped—no `:Tooltyp` nodes; legacy `has_tooltyp` → optional `tooltyp` on `:Tool` and/or `softwaretyp` on `:Software` (values such as `Bauteilboerse`, `Materialdatenbank`, `Materialkataster`—see section 6) |
| `datenmodell/` | Dropped—no `:Datenmodell` nodes; optional string/list fields on relevant nodes (see schema doc) |
| `bauobjektklasse/` | Dropped—values on `:Bauwerk` or `:Fallbeispiel` per export rule |
| `bauobjektrolle/` | Dropped—infer from `GEHÖRT_ZU` (`herkunft`, `einbauort`, …) on `:Bauteilgruppe` → `:Bauwerk` |
| `dokumenttyp/` | Dropped—use `:Quelle.art` |
| `tragwerkstyp/` | Dropped—axis mix; fold to `:Material` / `:WiederverwendungsArt` as appropriate |
| `foerderprogramm/`, `programm_kontext/` | Merged into `:Programm` |
| `bewertungslogik_abgrenzung/` | Renamed conceptually to `:WiederverwendungsArt` nodes |
| `reuse_strategie/` | Six canonical nodes under `axis: "reuse_strategie"`—Appendix E; not a separate label |
| `bauobjektstatus/` | Merged into `:Status` (seven nodes, `HAT { art: "status" }`) |
| `reuse_kette/` | Renamed to `:Wiederverwendungskette` |
| `kontextmerkmal/` | No `:Kontextmerkmal` label—`Pilotprojekt` → `(:Programm { id: "Pilotprojekt" })`; `Bestandserhalt_Policy` → no taxonomy node (strategy vocabulary or Markdown only) |

**Additional legacy resolutions (not separate folders):** Legacy relation `:BELEGT` reversed to `BELEGT_IN` (claim → `:Quelle`). Drop all `*_quelle`, `quelle_id`, `quelle_label_raw` on nodes and non-evidence edges. Typo fixes on export: `Moebelsepearat` → `Moebel_separat`; `ort/Scwheiz` → `ort/Schweiz` with correct `:Land` / `:Stadt` classification.

**Count check:** Live entity folders map to **52** labels as in section 2; `bauobjekt/` → `:Bauwerk` (listed in section 5.2); `reuse_einsatz/` → `:Bauteilgruppe` (not a separate `:ReuseEinsatz` label); `software_digitaltool/` splits into `:Software` / `:Tool`; `tooltyp/` → properties only (section 5.4); `akteur/` splits into **eight organisation-actor labels + `:Akteur` fallback + `:Person`** on export (sections 5.2 and 6.1); merged or dropped folders are listed in this section only.

### 5.5 `:Akteurrolle` — eight canonical nodes

Twenty-one legacy subfolders under `akteurrolle/<id>/` map to these eight `id` values. Edge property `rolle` on `HAT` (when `art` is `akteur` → an organisation-actor node per §6.1, or `person` → `(:Person)`) must always be one of these—not the raw folder name.

Canonical ids: `Bauherrschaft_Nutzung`, `Planung_Gestaltung`, `Tragwerk_Fassade`, `TGA_Sicherheit`, `Ausfuehrung_Logistik`, `Beratung_Forschung`, `Qualitaetssicherung`, `Koordination`.

| Legacy folder | Canonical `:Akteurrolle.id` |
| --- | --- |
| `Bauherr_Auftraggeber`, `Betreiber_Nutzer`, `Oeffentliche_Hand` | `Bauherrschaft_Nutzung` |
| `Architektur`, `Landschaftsplanung`, `Kunst_Gestaltung` | `Planung_Gestaltung` |
| `Tragwerksplanung`, `Fassade`, `Stahlbau_Fertigung` | `Tragwerk_Fassade` |
| `TGA_Gebaeudetechnik`, `Brandschutz_Barrierefreiheit` | `TGA_Sicherheit` |
| `Bauausfuehrung`, `Rueckbau_Demontage`, `Materiallieferant`, `Aufbereitung_Refurbishment` | `Ausfuehrung_Logistik` |
| `Reuse_Beratung`, `Nachhaltigkeitsberatung`, `Forschung_Dokumentation` | `Beratung_Forschung` |
| `Pruefung_Qualitaetssicherung` | `Qualitaetssicherung` |
| `Projektmanagement_Koordination`, `Projektbeteiligte_Unbestimmt` | `Koordination` |

### 5.6 `:Software` and `:Tool`

**Semantics**

- `:Software` — named full digital ecosystem, platform, or application.
- `:Tool` — smaller artefact (plug-in, script, calculator, API, module, workflow helper). Not an umbrella for Software.

**Node properties**

| Label | Required | Optional |
| --- | --- | --- |
| `:Software` | `id`, `title` | `softwaretyp`, `anbieter`, `url` |
| `:Tool` | `id`, `title` | `tooltyp`, `funktion`, `version` |

Optional enums (detail in `NEO4J_SCHEMA.md`): `softwaretyp` on `:Software` and `tooltyp` on `:Tool` (string or small controlled set; former `tooltyp/` folder ids map here—no separate taxonomy nodes).

**Edges**

- `(:Tool)-[:GEHÖRT_ZU { rolle: "software" }]->(:Software)` optional host link.
- `BENUTZT` may target `:Software` or `:Tool`.
- `IST` from `:Software` / `:Tool` to other classification labels per export rules (former `tooltyp/` categories → properties only).

**Migration from `software_digitaltool/`**

1. Classify each subfolder explicitly as `:Software` or `:Tool` (not everything as Tool).
2. Retire monolithic `:SoftwareDigitaltool`; legacy `uses_software_digitaltool` → `BENUTZT` to the correct target.
3. Clear host modules: create `:Tool` and optionally `GEHÖRT_ZU { rolle: "software" }` to the host `:Software`.

| Example | Label |
| --- | --- |
| Madaster, Concular, Restado, Loopfront | `:Software` |
| Revit, Rhino, OneClickLCA, Excel, QGIS | `:Software` |
| Grasshopper material-matching script, Revit material-pass plug-in, CO₂ spreadsheet, CSV import script, API connector, matching algorithm | `:Tool` |

### 5.7 `:Huerde` vs `:PruefungNachweis` (flat model)

- `:Huerde` (`huerde/`, `HAT { art: "huerde" }`) — risk, conflict, or barrier to reuse (e.g. missing technical approval, fire-safety conflict). Not a named inspection method.
- `:PruefungNachweis` (`pruefung_nachweis/`, `HAT { art: "pruefung" }`) — concrete proof or inspection type (instrument).
- Both may attach to the same `:Bauteilgruppe` when the sources support it. No hurdle hierarchy in the graph (no `IST` / `GEHÖRT_ZU` between `:Huerde` nodes; no synthetic parent hurdles).

### 5.8 Id and naming convention (readability)

| Topic | Rule |
| --- | --- |
| Charset | ASCII in `id`; umlauts as `ae`, `oe`, `ue`, `ss` |
| Separators | Single `_` between word parts; no `__` padding; no `;` or `,` inside one `id` |
| One entity | One node per real entity—no list ids (`A;B`) |
| Length | Prefer ≤ 48 characters (hard cap e.g. 96 in export) |
| `:Fallbeispiel` | Project / case slug; not building `art` (that belongs on `:Bauwerk`) |
| `:Bauwerk` | Stable slug per built work; link to case via `GEHÖRT_ZU { rolle: 'fallbeispiel' }` |
| `:Bauteilgruppe` | Pattern `<CASE>_C<NN>_<ELEMENT>` when used; rows from `reuse_einsatz/<id>/` use the folder slug as graph `id` (often the same pattern) |
| Organisation actors (§6.1) | Stable slug for **organisations** (company, authority, NGO, office) — not personal names; primary `:Label` is chosen from `akteurtyp/<slug>` or `:Akteur` fallback |
| `:Person` | Natural persons: `Vorname_Nachname` style slug; same ASCII rules as organisation actors |
| `:Quelle` | Short citation slug—not mirrored file paths |
| `:Software` / `:Tool` | Stable product slug + human `title` |
| Bauteilbörse | Canonical id `Bauteilboerse` on `:Ressourcenquelle` and `:Beschaffungsweg`; regional exchanges as separate **organisation-actor** nodes (correct primary label from §6.1, e.g. `Bauteilboerse_Hannover`) |
| Other labels (section 5.2) | Ordnername = default `id` when already ASCII-clean |

### 5.9 `:Status` — seven canonical nodes

| `id` | Meaning (short) |
| --- | --- |
| `Geplant` | Not yet built / early phase |
| `In_Bau` | Under construction |
| `Realisiert` | Completed and in use (typical) |
| `Prototyp` | Pilot / experimental stand |
| `Rueckgebaut` | Demolished / dismantled |
| `Nicht_Realisiert` | Not realised / discarded |
| `Unklar` | Ambiguous |

Legacy `reuse_einsatzstatus/<id>/` → canonical `id`:

| Legacy | → Canonical |
| --- | --- |
| `Geplant` | `Geplant` |
| `Vorgeschlagen` | `Geplant` |
| `Prototypisch` | `Prototyp` |
| `Realisiert` | `Realisiert` |
| `Temporaer` | `Realisiert` or `Prototyp` (heuristic) |
| `Verworfen` | `Nicht_Realisiert` |
| `Unklar` | `Unklar` |

Legacy `bauobjektstatus/<id>/` → canonical `id`:

| Legacy | → Canonical |
| --- | --- |
| `Gebaut` | `Realisiert` |
| `Geplant` | `Geplant` |
| `In_Bau` | `In_Bau` |
| `Prototyp` | `Prototyp` |
| `Rueckgebaut` | `Rueckgebaut` |
| `Temporaer` | `Prototyp` or `Realisiert` (heuristic) |
| `Unklar` | `Unklar` |
| `Wettbewerb` | `Geplant` |

### 5.10 `fuegung_verbindung/` → `:Verbindungstechnik`

| Legacy folder | Canonical `:Verbindungstechnik.id` |
| --- | --- |
| `Verschraubung` | `Geschraubt` |
| `Verschweissung` | `Geschweisst` |
| `Steckverbindung` | `Gesteckt` |
| `Verleimung` | `Geklebt` |
| `Vermoertelung` | `Vergossen` |
| `Klemmverbindung` | `Klemmverbindung` |

`Reversible_Fuegung/`: no automatic export to `:Verbindungstechnik` or `:Reversibilitaet` in this pipeline—content stays in Markdown unless curated later.

## 6. Node properties (full detail)

Full per-label property tables belong in `NEO4J_SCHEMA.md` §2 and in `NEO4J_SCHEMA_MAP.md`. This plan defines labels, dispositions, allowed edges, and appendices A–G (normative tables: E–G; A/D point to sections 4 and 5.4 + 7.1).

### 6.1 Organisation-actor labels: one primary `:Label` per distinct `akteurtyp/<slug>` (granular; no type vertices, no `akteurtyp` property)

Natural persons are always **`(:Person)`** (Markdown: `legacy_type: Person` or `akteurtyp/Person` in `index.md`—unchanged from §5.2). **Organisations** from `_database/akteur/<id>/` get **exactly one** primary Neo4j label: the label is chosen from the **first** recognised **`akteurtyp/<slug>`** token in the entity’s `index.md` (provenance body), after **optional alias resolution** only (table below). The slug is **not** stored as a separate `akteurtyp` string property—the **label name** is the classifier. **Not** modelled as `(:X)-[:IST]->(:Akteurtyp)`.

**Granularity rule:** each **distinct** canonical slug that appears in curated `index.md` for organisations maps to **its own** primary `:Label` in the table—**no** silent bucketing of one slug into another’s label unless an explicit **alias** row maps the prose token to a canonical slug. When the corpus gains a **new** organisation slug, add a **new** table row + §5.2 row + `IST` / `BELEGT_IN` subject lists in the same authoring change (or use **`:Akteur`** as interim fallback until the vocabulary row exists).

- **Resolved slug:** use the **Neo4j label** in the mapping table (PascalCase, German spelling rules as for other labels).
- **No / unknown slug:** use **`:Akteur`** as the **fallback** primary label for that organisation row until `index.md` is curated.
- **`:Person`:** never receives organisation labels; raw `akteurtyp/Person` participates only in **label** routing to `:Person`.

**Optional slug aliases (organisations):** apply **before** the mapping table; only the rows listed here may collapse tokens—everything else stays character-for-character as the slug segment after `akteurtyp/`.

| Raw token / variant in `index.md` | Canonical slug for table lookup |
| --- | --- |
| Folder or token spelling `Professur` vs slug `professur` | `professur` |

**Slug → primary `:Label` (closed vocabulary for classified organisations):**

| Canonical slug (`akteurtyp/<slug>` after alias pass) | Neo4j primary label |
| --- | --- |
| `planung_architektur_ingenieurwesen` | `:PlanungArchitekturIngenieurwesen` |
| `forschung_lehre_wissenstransfer` | `:ForschungLehreWissenstransfer` |
| `oeffentliche_institutionen_foerderung` | `:OeffentlicheInstitutionenFoerderung` |
| `kammern_verbaende_ngos_netzwerke` | `:KammernVerbaendeNgosNetzwerke` |
| `Unternehmerverband_Historische_Baustoffe_UHB_md` | `:UnternehmerverbandHistorischeBaustoffeUHBMd` |
| `materialinitiativen_hubs` | `:MaterialinitiativenHubs` |
| `reuse_beratung_prozessdienstleister` | `:ReuseBeratungProzessdienstleister` |
| `professur` | `:Professur` |

**Optional properties** on these nodes follow the same metadata-only rules as other primary labels (`id` required, `UNIQUE`; other fields only where the schema doc lists them—**not** an `akteurtyp` duplicate).

| Label group | Required | Optional |
| --- | --- | --- |
| Eight organisation-actor labels above, plus `:Akteur` fallback, plus `:Person` | `id` | Per `NEO4J_SCHEMA.md` / inventory (e.g. `art` where used elsewhere)—**no** `akteurtyp` property |

## 7. Edge-type catalogue

| Edge | Subject labels | Object labels | Cardinality (typical) | Purpose |
| --- | --- | --- | --- | --- |
| `IST` | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:PlanungArchitekturIngenieurwesen`, `:ForschungLehreWissenstransfer`, `:OeffentlicheInstitutionenFoerderung`, `:KammernVerbaendeNgosNetzwerke`, `:UnternehmerverbandHistorischeBaustoffeUHBMd`, `:MaterialinitiativenHubs`, `:ReuseBeratungProzessdienstleister`, `:Professur`, `:Akteur`, `:Person`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette` | Classification labels except `:Status` (use `HAT { art: "status" }`) and not `axis: "reuse_strategie"` on case/building/action (use `HAT { art: "wiederverwendungsart" }`) | N:1 | Taxonomic classification |
| `HAT` | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe` | Classification labels; **`HAT { art: "status" }` → `:Status`** (lifecycle); `HAT { art: 'akteur', rolle: … }` → organisation-actor node (§6.1, including `:Akteur` fallback); `HAT { art: 'person', rolle: … }` → `(:Person)`; includes `wiederverwendungsart` → `:WiederverwendungsArt`, `schadstoff` → `:Schadstoff` | N:M | Qualitative facets, actors, strategy axis, substances, lifecycle |
| `BENUTZT` | `:Bauteilgruppe`, `:Bauwerk`, `:Fallbeispiel` | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Software`, `:Tool` | N:M | Instrumental / material use |
| `GEHÖRT_ZU` | `:Bauwerk`, `:Bauteilgruppe`, `:Fallbeispiel`, `:Software`, `:Tool` | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:Wiederverwendungskette`, `:Land`, `:Stadt`, `:Programm`, `:Software` | varies | Membership, geography, chain, program, tool host—**Appendix F** |
| `BELEGT_IN` | Claim-holding nodes: `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:PlanungArchitekturIngenieurwesen`, `:ForschungLehreWissenstransfer`, `:OeffentlicheInstitutionenFoerderung`, `:KammernVerbaendeNgosNetzwerke`, `:UnternehmerverbandHistorischeBaustoffeUHBMd`, `:MaterialinitiativenHubs`, `:ReuseBeratungProzessdienstleister`, `:Professur`, `:Akteur`, `:Person`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`, plus `:Entwurfsentscheidung`. Any **other** label from section 5.2 as subject **only** if the cited source defines that taxonomy entry (not a passing prose mention) | `:Quelle` | N:M | Evidence only—edge properties in section 8 |

### 7.1 Legacy relation folding (reference)

- `IST`: `has_bauteiltyp`, `has_bewertungslogik_abgrenzung` (→ `:WiederverwendungsArt` with appropriate `axis`), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_zertifizierung_bewertungssystem`; reuse strategy misuse → `HAT { art: "wiederverwendungsart" }` with `axis: "reuse_strategie"` (not `IST`). **`has_tooltyp`** → no graph edge—set optional `tooltyp` / `softwaretyp` on `:Tool` / `:Software` instead. Legacy **`has_akteurtyp`** / `akteurtyp/<slug>` as a *target node* → choose the organisation’s **primary `:Label`** from section 6.1 (not `IST` to a type vertex; **no** `akteurtyp` string property on the actor node).
- `HAT`: **`has_reuse_einsatzstatus`**, **`has_bauobjektstatus`** → **`HAT { art: "status" }`** → `:Status`; strategy, hurdles, substances, inspections, norms, legal, usage, intervention, connection technique, reversibility, logistics, economy, actors (`has_akteurrolle` → `art: 'akteur'` / `art: 'person'` to organisation-actor node / `:Person` per source classification), design decisions (`has_entwurfsentscheidung`)—`art` values per Appendix G; `has_fuegung_verbindung` → only `:Verbindungstechnik` per section 5.10.
- `BENUTZT`: `uses_material`, `uses_software_digitaltool` (→ `:Software` or `:Tool`), `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`; `has_datenmodell` → properties on nodes, not a `:Datenmodell` label.
- `GEHÖRT_ZU`: fall membership, spatial roles (`einbauort`, `herkunft`, …), chain, program, tool→software, land/stadt, Pilotprojekt program link—**Appendix F** for triples.
- `BELEGT_IN`: resolved shorthands; direction claim → `:Quelle`; see section 8 resolution rule.

**Dropped relations (no direct edge after fold):** `has_projekt`, `has_bauobjekt`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_tragwerkstyp`, `has_dokumenttyp`, `has_akteurrolle` as node-target pattern, `measured_on_bauobjekt`, `measures_kennwertdefinition`, `involves_akteur` (no edge until participation is remodelled on graph nodes). `belongs_to_fallstudie` / `belongs_to_projekt` for the **action’s** case anchor → `GEHÖRT_ZU { rolle: 'fallbeispiel' }`, not dropped in that sense.

## 8. Edge properties

No `quelle_id` or `quelle_label` on `IST`, `HAT`, `BENUTZT`, or `GEHÖRT_ZU`. Evidence lives only on `BELEGT_IN` from the node that asserts the fact.

### `IST` (optional temporal / confidence)

| name | type | req | notes |
| --- | --- | --- | --- |
| `seit` | date? | no | start validity |
| `bis` | date? | no | end validity |
| `gewichtung` | float? | no | 0..1 confidence |

### `HAT`

| name | type | req | notes |
| --- | --- | --- | --- |
| `art` | string | yes | Appendix G; `wiederverwendungsart` → `axis: "reuse_strategie"`; `schadstoff` → `:Schadstoff`; **`status` → `:Status`** (lifecycle) |
| `rolle` | string? | if `art` is `akteur` or `person` | One of the eight ids in section 5.5 |
| `anzahl` | int? | no | multiplicity |
| `intensitaet` | string? | no | qualitative strength |
| `seit` | date? | no | also used for `art: "status"` edges |
| `bis` | date? | no | also used for `art: "status"` edges |
| `gewichtung` | float? | no | 0..1 confidence; typical on `art: "status"` |

### `BENUTZT`

| name | type | req | notes |
| --- | --- | --- | --- |
| `anzahl` | float? | no | quantity |
| `einheit` | string? | no | e.g. `t`, `m2`, `Stueck` |
| `anteil_prozent` | float? | no | share |
| `funktion_alt` | string? | no | original role |
| `funktion_neu` | string? | no | new role |
| `aufbereitung` | string? | no | processing description |

### `GEHÖRT_ZU`

| name | type | req | notes |
| --- | --- | --- | --- |
| `rolle` | string | yes | Must form a valid triple with source and target labels—Appendix F |
| `position` | int? | no | sequence index (e.g. chain station) |
| `seit` | date? | no | |
| `bis` | date? | no | |

### `BELEGT_IN`

Direction: **(claim) → (:Quelle)**.

| name | type | req | notes |
| --- | --- | --- | --- |
| `eigenschaft` | string? | no | scopes citation to a property name on the source node |
| `seite` | string? | no | page |
| `excerpt` | string? | no | short quote |
| `raw_label` | string? | no | original shorthand (`S4`, `[S1]`) |

**Resolution:** create `BELEGT_IN` only when the shorthand resolves to a stable `(:Quelle)`; then optionally set `raw_label` for audit. If unresolved, keep shorthand in Markdown only—no fake `:Quelle`, no orphan edge.

---

# Appendix A — Modeling principles

Single normative list: **section 4** of this plan. `NEO4J_SCHEMA.md` should copy or reference that section as its Appendix A without duplicating a second full prose block elsewhere.

# Appendix B — Constraints and indexes

- `UNIQUE` constraint on `id` for every label.
- Range indexes (as needed for queries): e.g. `:Fallbeispiel(art)`, `:Bauwerk(art)`, `:Bauwerk(flaeche_m2)`, `:Bauwerk(fertigstellung_jahr)`, `:Bauteilgruppe(masse_t)`, `:Bauteilgruppe(co2_einsparung_kg)`, each organisation-actor label (§6.1, including `:UnternehmerverbandHistorischeBaustoffeUHBMd`) and `:Akteur` with `:Label(art)` where the schema attaches `art`, `:Person(art)`, `:Quelle(art)`.
- No full-text index on graph prose (there is no `body_md` on nodes).

# Appendix C — Coverage checklist

- Section 5.2 (all labels) plus section 5.4 (folders without a label) account for every live entity folder under `_database/` (system folders `_edges`, `_system` excluded). Label count **52** by design (not equal to raw folder count).
- YAML frontmatter on legacy entities: structural keys resolve to `GEHÖRT_ZU` / properties / `IST` / `HAT` / `BENUTZT` as per the schema doc; `quelle_label` resolves to `BELEGT_IN` or stays in Markdown; `body`, `legacy_paths`, `build_status` never enter the graph.
- `akteurrolle/` many subfolders → eight `:Akteurrolle` nodes; `kontextmerkmal/` → no `:Kontextmerkmal` label (section 5.4).

# Appendix D — Renamings, drops, merges

Single normative source: **section 5.4** (folder disposition and one-off legacy resolutions) and **section 7.1** (relation folding). `NEO4J_SCHEMA.md` Appendix D should mirror those subsections only—no second large matrix duplicating section 5.4.

# Appendix E — `:WiederverwendungsArt` (`axis: "reuse_strategie"`): sechs Kanon-Knoten — *Art der Wiederverwendung* (verbindlich)

Genau **sechs** Knoten `(:WiederverwendungsArt { axis: "reuse_strategie" })`. **Elf** Legacy-Ordner unter `reuse_strategie/` kollabieren darauf. Anbindung nur `HAT { art: "wiederverwendungsart" }` von `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`. **Kein** separates Label `:ReuseStrategie`.

| Nr. | `id` | Erklärung | Beispiel |
| --- | --- | --- | --- |
| **1** | `Bestandserhalt_Weiterbauen` | Gebäude oder große Gebäudeteile bleiben erhalten und werden angepasst. | Fabrik wird zu Wohnhaus, Tragwerk bleibt bestehen |
| **2** | `In_situ_Wiederverwendung` | Bauteile bleiben am ursprünglichen Ort und werden weitergenutzt. | Treppe, Decke, Fassade oder Wand bleibt im Gebäude |
| **3** | `Direkte_Wiederverwendung` | Bauteil wird ausgebaut und an anderer Stelle mit gleicher Funktion wieder eingebaut. | Tür bleibt Tür, Fenster bleibt Fenster |
| **4** | `Wiederverwendung_nach_Aufarbeitung` | Bauteil wird gereinigt, repariert, geprüft oder angepasst (inkl. DfD / Remanufacturing als Aufbereitung). | Ziegel reinigen, Parkett schleifen, Stahlträger prüfen |
| **5** | `Umnutzung_Repurposing` | Bauteil erhält eine neue Funktion. | Fenster wird Innenwand, Tür wird Tischplatte |
| **6** | `Kaskade_Downcycling_Bauteilebene` | Bauteil wird in einer weniger anspruchsvollen Funktion weitergenutzt. | tragendes Holz wird Innenausbau, Fassadenplatten werden Gartenbelag |

**Legacy `reuse_strategie/<id>/` → Kanon-`id` (Export):**

| Legacy `reuse_strategie/<id>/` | → Kanon-`id` |
| --- | --- |
| `Bestandserhalt`, `Weiterbauen_im_Bestand`, `Refurbishment`, `Adaptives_ReUse` | `Bestandserhalt_Weiterbauen` |
| `Same_Site_ReUse` | `In_situ_Wiederverwendung` |
| `Direkte_Wiederverwendung` | `Direkte_Wiederverwendung` |
| `Remanufacturing`, `Design_for_Disassembly` | `Wiederverwendung_nach_Aufarbeitung` |
| `Upcycling` | `Umnutzung_Repurposing` |
| `Recycling`, `Urban_Mining` | `Kaskade_Downcycling_Bauteilebene` |

**Heuristik:** `Upcycling` → `Umnutzung_Repurposing` ist die Default-Zuordnung; bei reinem Qualitäts-/Aufarbeitungspfad darf der Export alternativ `Wiederverwendung_nach_Aufarbeitung` setzen, wenn die Fallakte das trägt.

# Appendix F — `GEHÖRT_ZU` allowlist (authoritative)

Allowed triples `(sourceLabel, rolle, targetLabel)`:

| sourceLabel | rolle | targetLabel |
| --- | --- | --- |
| `:Bauwerk` | `fallbeispiel` | `:Fallbeispiel` |
| `:Bauteilgruppe` | `fallbeispiel` | `:Fallbeispiel` |
| `:Bauteilgruppe` | `einbauort` | `:Bauwerk` |
| `:Bauteilgruppe` | `herkunft` | `:Bauwerk` |
| `:Bauteilgruppe` | `zwischenlager` | `:Bauwerk` |
| `:Bauteilgruppe` | `verarbeitung` | `:Bauwerk` |
| `:Bauteilgruppe` | `transport` | `:Bauwerk` |
| `:Bauteilgruppe` | `kette` | `:Wiederverwendungskette` |
| `:Fallbeispiel` | `land` | `:Land` |
| `:Fallbeispiel` | `stadt` | `:Stadt` |
| `:Bauwerk` | `land` | `:Land` |
| `:Bauwerk` | `stadt` | `:Stadt` |
| `:Fallbeispiel` | `programm` | `:Programm` |
| `:Software` | `programm` | `:Programm` |
| `:Tool` | `programm` | `:Programm` |
| `:Tool` | `software` | `:Software` |

# Appendix G — Canonical `HAT.art` literals

Allowed values for `HAT.art` (sorted):

`akteur`, `entwurf`, `huerde`, `intervention`, `logistik`, `norm`, `nutzung`, `person`, `pruefung`, `prozessphase`, `recht`, `reversibilitaet`, `schadstoff`, `status`, `verbindungstechnik`, `wirtschaft`, `wiederverwendungsart`, `zertifizierung`

- Chemical substance Stammdaten from `schadstoff/`: target `(:Schadstoff)`, edge `HAT { art: "schadstoff" }` (not `art: "huerde"`). Generic hurdle “Schadstoffbelastung” under `huerde/`: target `(:Huerde)` with `HAT { art: "huerde" }`.
- Participant edges: `HAT { art: "akteur", rolle: … }` → organisation-actor node (§6.1, including `:Akteur` fallback); `HAT { art: "person", rolle: … }` → `(:Person)` (natural persons). `rolle` uses the eight canonical `(:Akteurrolle).id` values in both cases (§5.5). Organisation kind is the **primary Neo4j label**, not a property and not a separate type vertex.

---

## Out of scope (this plan document)

- Implementing the Markdown → Neo4j bulk export script.
- Operating or hosting Neo4j.
- Closing all ~30 “gap” relations from prose-only mentions.
- Translating German labels to English.
