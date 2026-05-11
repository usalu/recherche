# Research Database Extraction — Wiederverwendung im Bauwesen

Generated: 2026-05-11

---

## 1. Database Overview

**Name:** Reuse Knowledge Base + Graph (working title in files: *reuse_ontology*)
**Location:** `e:\recherche\_database\`
**Canonical schema:** `_database/_system/SCHEMA.md`
**SQLite artifact:** `_database/_system/reuse_ontology.sqlite`
**Edge CSV:** `_database/_edges/clean_confirmed_edges.csv`
**Tool used by user:** Tolaria (Markdown/wikilinks editor, similar to Obsidian)

**Purpose:** PhD-level research on Wiederverwendung (reuse) of building components, materials, and systems in architecture and construction. Combines general domain knowledge with structured built case studies, all navigable as a knowledge graph.

**Main topic areas:**
- Built case studies: 96 buildings/projects with per-component reuse records
- Reuse strategies, status, process phases
- Materials, component types, structural systems
- Actors, roles, institutions
- Hurdles (barriers), norms, legal conditions, contaminants
- Data points (quantities, CO₂, cost, area) with source references
- Evaluation frameworks, data quality
- Digital tools, platforms, software
- Economics, funding programs

**Organization logic:** Folder-per-instance. Every entity is a folder under `_database/<entity_type>/<instance_id>/index.md`. The folder name is the node ID. YAML frontmatter = structured metadata. Body = German prose knowledge. Typed edges are stored separately in `_edges/clean_confirmed_edges.csv` and materialized to SQLite.

**Key naming conventions:**
- Node IDs are ASCII-slugified German/English titles, e.g. `K118_Kopfbau_Halle_118_Winterthur__001__Stahltr_ger_St_tzen`
- German umlauts are stripped (ü → `_`), spaces → `_`, double-underscores as field separators in compound IDs
- Controlled knots use CamelCase or underscore IDs (e.g. `Direkte_Wiederverwendung`, `Toleranzen`)
- All prose is German; some English terms used for international cases (e.g. "reclaimed steel", "hollow core slabs")
- Source labels are shorthand `[S1]`, `S2`, etc. — not resolved to full quelle records in the frontmatter

---

## 2. Entities / Tables / Collections

### Core entities (heavy nodes — instances are the data)

| Entity/Table | Field | Field type | Example values | Purpose | Notes/problems |
|---|---|---|---|---|---|
| `fallstudie` | `id` | text (slugified) | `K118_Kopfbau_Halle_118_Winterthur` | Unique node ID | Required |
| `fallstudie` | `title` | free text | `"K.118 – Kopfbau Halle 118, Winterthur"` | Display name | Required |
| `fallstudie` | `entity` | controlled vocab | `"fallstudie"` | Type tag | Required |
| `fallstudie` | `build_status` | status | `promoted_phase42` | Migration tracking | Internal; not query-facing |
| `fallstudie` | `bauobjekt` | relation (list) | `["K118_Kopfbau_Halle_118_Winterthur"]` | Links to bauobjekt | Often same ID as fallstudie |
| `fallstudie` | `projekt` | relation (list) | `["K118_Kopfbau_Halle_118_Winterthur"]` | Links to projekt | Often same ID as fallstudie |
| `fallstudie` | `legacy_paths` | provenance (list) | `["Gebäude\\K118_...md"]` | Source file | Migration artifact; can be removed later |
| `fallstudie` | body prose | free text (German) | Kurzdefinition, Relevanz, Fachinhalt… | Rich knowledge text | Required; quality varies |
| `projekt` | `id` | text | `K118_Kopfbau_Halle_118_Winterthur` | Unique ID | Required |
| `projekt` | `entity` | controlled | `"projekt"` | Type tag | — |
| `bauobjekt` | `id` | text | `K118_Kopfbau_Halle_118_Winterthur` | Unique ID | Note: fallstudie/projekt/bauobjekt often share the same ID — three separate nodes |
| `bauobjekt` | body | free text | building description | — | Often stub |
| `akteur` | `id` | text | `baubüro_in_situ_zirkular`, `Rotor_DC` | Unique ID | — |
| `akteur` | body | free text | Description of firm/institution | — | — |
| `reuse_einsatz` | `id` | compound slug | `K118_Kopfbau__001__Stahltr_ger_St_tzen` | `<case>__<NNN>__<bauteil_slug>` | Required; ~634 nodes |
| `reuse_einsatz` | `entity` | controlled | `"reuse_einsatz"` | — | Required |
| `reuse_einsatz` | `bauteil_label` | free text | `"Stahlträger / Stützen"` | Exact component name | Fine-grained; not a relation |
| `reuse_einsatz` | `material_label` | free text | `"Stahl"`, `"Brettschichtholz"` | Exact material name | Fine-grained; not a relation |
| `reuse_einsatz` | `herkunft_label` | free text | `"Teilrückbau Halle ELYS Basel"` | Donor source description | Free text; not linked to a bauobjekt edge yet |
| `reuse_einsatz` | `alte_funktion` | free text | `"Tragwerk Halle"` | Component's old role | Not yet linked via `has_funktionswechsel` |
| `reuse_einsatz` | `neue_funktion` | free text | `"Tragwerk Aufstockung"` | Component's new role | Not yet linked |
| `reuse_einsatz` | `menge_umfang` | free text / number | `"98 t; 95 % des tragenden Stahls"`, `"unbekannt"` | Quantity | Mixed format; not split into value+unit |
| `reuse_einsatz` | `pruefung_label` | free text | `"Sichtprüfung; Herstellungsdatum; Rost/Scaling"` | Testing description | Free text; partially linked via `has_pruefung_nachweis` |
| `reuse_einsatz` | `norm_recht_label` | free text | `"Historic Sections Book; sonst unbekannt"` | Norm/regulation | Free text; partially linked via `references_norm` |
| `reuse_einsatz` | `huerde_label` | free text | `"statischer Nachweis, Geometrie"` | Hurdle description | Free text; partially linked via `has_huerde` |
| `reuse_einsatz` | `quelle_label` | free text | `"[S1], [S6]"` | Source shorthand | ⚠ Not resolved to quelle nodes — unlinked |
| `reuse_einsatz` | `fallstudie` | relation | `"fallstudie/K118_..."` | Parent case | Required |
| `reuse_einsatz` | `bauobjekt` | relation (list) | `["K118_..."]` | Receiver object | Required |
| `reuse_einsatz` | `projekt` | relation (list) | `["K118_..."]` | Parent project | Required |
| `reuse_einsatz` | body bullets | free text | `- **Verbindung:** vermutlich geschraubt` | Structured prose | Partially parseable |
| `datenpunkt` | `id` | compound slug | `K118_Kopfbau__001__Fl_che` | `<case>__<NNN>__<metric>` | ~600+ nodes |
| `datenpunkt` | `wert` | number (as string) | `"1.100"`, `"98"` | Measured/reported value | ⚠ Stored as string; German decimal convention (period = thousands separator) |
| `datenpunkt` | `einheit` | free text | `"m²"`, `"t"`, `"kgCO₂e"` | Unit | Free text; not controlled vocabulary |
| `datenpunkt` | `quelle_label` | free text | `"[S2], [S4]"` | Source shorthand | ⚠ Not resolved to quelle nodes |
| `datenpunkt` | `fallstudie` | relation | `"fallstudie/K118_..."` | Parent case | Required |
| `datenpunkt` | `bauobjekt` | relation (list) | — | Object measured | Required |
| `datenpunkt` | body | free text | Vertrauensgrad, Bilanzgrenze, Methode | Context | Partially structured |
| `quelle` | id, body | text | `abbruchmethode_md`, `Geb_ude_K118_...md` | Source record | ⚠ quelle folder mostly contains legacy MD stubs, not structured citation records |
| `akteur_beteiligung` | `id` | compound | `55_Great_Suffolk__001__Fabrix` | `<case>__<NNN>__<akteur>` | Edge-as-node |
| `akteur_beteiligung` | `fallstudie`, `projekt`, `bauobjekt` | relations | — | Parent context | Required |
| `software_digitaltool` | id, body | text | Madaster, Concular, Restado, Loopfront | Digital platforms | — |

### Controlled knots (taxonomy nodes)

| Entity/Table | Field | Field type | Example values | Purpose | Notes/problems |
|---|---|---|---|---|---|
| `bauteiltyp` | id | controlled | `Stuetze`, `Traeger`, `Decke`, `Wand`, `Fassade`, `Fenster`, `Tuer`, `Treppe`, `Dach`, `Boden`, `Ausbau`, `Technik`, `Fundament`, `Gelaender`, `Daemmung` | 15 canonical component families | Canonical; finalized |
| `material` | id | controlled | `Beton`, `Stahlbeton`, `Recyclingbeton`, `Stahl`, `Aluminium`, `Gusseisen`, `Holz`, `Glas`, `Ziegel`, `Naturstein`, `Keramik`, `Kunststoff`, `Daemmstoff`, `Lehm`, `Stroh` | 15 material substances | Canonical; some legacy variants remain in quelle folder |
| `reuse_strategie` | id | controlled | `Direkte_Wiederverwendung`, `Same_Site_ReUse`, `Urban_Mining`, `Design_for_Disassembly`, `Bestandserhalt`, `Recycling`, `Upcycling`, `Remanufacturing`, `Adaptives_ReUse`, `Refurbishment`, `Weiterbauen_im_Bestand` | 11 reuse strategies | 11 defined; schema says 8 canonical — slight mismatch |
| `reuse_einsatzstatus` | id | controlled | `realisiert`, `geplant`, `verworfen`, `vorgeschlagen`, `unklar`, `temporaer`, `prototypisch` | 7 status values | Canonical |
| `bewertungslogik_abgrenzung` | id | controlled | `zaehlt_als_Direct_Reuse`, `zaehlt_nicht`, `Bestandserhalt_separat`, `Recycling_separat`, `Moebelsepearat`, `geplant_aber_nicht_realisiert`, `unklar` | Evaluation boundary classifier | 7 values; typo: `Moebelsepearat` |
| `huerde` | id | controlled | Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit, Schadstoffbelastung, Technische_Freigabe, Terminunsicherheit, Toleranzen, Unkonventionelles_Material, Verfuegbarkeitsproblem, Witterung_Feuchte, Zustand_Unklar | `has_huerde` on `reuse_einsatz` | 27 values; most-developed vocabulary; Gewaehrleistung/Haftung overlap |
| `prozessphase` | id | controlled | Rueckbau, Aufbereitung, Wiedereinbau, Transport, Lagerung, Pruefung, Identifikation, Entwurf, Ausschreibung, Bestandserfassung, Betrieb_und_Rueckbauplanung | `has_prozessphase` | 11 values; solid |
| `rueckbauverfahren` | id | controlled | Demontage, Selektiver_Rueckbau, Ausbau, Zerstoerungsarme_Bergung, schonender_Rueckbau | `has_rueckbauverfahren` | ~5–6 values; generic labels excluded from linking |
| `aufbereitungsverfahren` | id | controlled | Sandstrahlen, Entmoertelung_von_Fliesen, Holzaufbereitung, Rekonditionierung, Reparatur, Qualitaetssicherung, Leuchten_Refurbishment, Drahtglasschneiden | `has_aufbereitungsverfahren` | ~8 values |
| `fuegung_verbindung` | id | controlled | geschraubt, gesteckt, geschweisst, geklebt, vergossen, reversibel, irreversibel | `has_fuegung_verbindung` | `reversibel`/`irreversibel` are meta-categories, not techniques — may cause analytical confusion |
| `tragwerkstyp` | id | controlled | Holztragwerk, Stahltragwerk, Betontragwerk, wiederverwendetes_Tragwerk, demontierbares_Tragwerk | `has_tragwerkstyp` | ⚠ Mixes material-typed (first 3) with reuse-strategy-typed (last 2) — heterogeneous axis |
| `bauweise` | id | controlled | Holzbauweise, Massivbauweise, Stahlbauweise, Hybridbauweise, Fertigteilbauweise | `has_bauweise` (gap) | 5 values |
| `pruefung_nachweis` | id | controlled | Sichtpruefung, Statische_Nachweisfuehrung, Materialpruefung, Schadstoffscreening, Geometrische_Vermessung, Zugversuch, Brandnachweis, Abbrandbemessung, Schweissbarkeitspruefung, Eignungspruefung_Baulehm, Zustandsbewertung | `has_pruefung_nachweis` | 11 values; solid |
| `leistungsanforderung` | id | controlled | Tragfaehigkeit, Brandschutz, Schallschutz, Waermeschutz, Dauerhaftigkeit, Schadstofffreiheit, Rueckbaubarkeit, Feuchteschutz | `has_leistungsanforderung` | 8 values; only 3 edges linked — severely underused |
| `norm` | id | controlled | DIN_EN_15804, DIN_EN_15978, ISO_14040, ISO_14044, ISO_20887, F90, R90, REI90, Brandschutzanforderung, DIN_18940, Wiederverwendungskriterien, EU_Taxonomie, Feuerwiderstand | `references_norm` | 12+ values; only 9 edges linked — severely underused |
| `schadstoff` | id | controlled | Asbest, PCB, PAK, Bleifarbe, Holzschutzmittel | `has_schadstoff` (gap) | 5 values |
| `akteurrolle` | id | controlled | Architektur, Tragwerksplanung, Bauherr_Auftraggeber, Nachhaltigkeitsberatung, Reuse_Beratung, Materiallieferant, Projektmanagement_Koordination | `has_akteurrolle` | ~10+ values |
| `methode` | id | controlled | Materialpass, Design_for_Disassembly, Urban_Mining, Form_Follows_Availability, Materialinventur, Building_Material_Scouting, Bauteilkatalogisierung, ReUse_Assessment, Reversibilitaet, Zirkulaere_Ausschreibung, Bestandserhalt | `has_methode` (gap) | Bestandserhalt and DfD overlap with `reuse_strategie` |
| `datenqualitaet` | id | controlled | belegt, teilweise_belegt, unbekannt, umstritten (implied) | `has_datenqualitaet` (gap) | Currently only as `Vertrauensgrad` prose field in datenpunkt body; not linked as edges |
| `ort` | id | controlled/core | Berlin, Basel, Bruessel, Oslo, London, … (53+ city nodes) | `located_in_ort` | Hierarchical structure not enforced; `ort/Scwheiz_md` has a typo |
| `wirtschaft` | id | controlled | Kostenvergleich, Lebenszykluskosten, Geschaeftsmodell, Finanzierung, Preisbildung, Restwert | `has_wirtschaft` (gap) | ~6 values |
| `foerderprogramm` | id | controlled | FCRBE, PREUSE, BBSM, Reallabor_Be_Ware, Zukunftbau | `involves_foerderprogramm` (gap) | ~5 values |
| `logistik` | id | controlled | Transport, Lagerung, Zwischenlagerung, Materialmatching, Materialverfuegbarkeit, Lagerflaeche, ReUse_Centre | `has_logistik` (gap) | ~7 values |
| `ressourcenquelle` | id | controlled | (not inspected in detail) | Procurement source type | ⚠ gap relation — 0 edges |
| `beschaffungsweg` | id | controlled | (not inspected) | Procurement route | ⚠ gap relation — 0 edges |
| `funktionswechsel` | id | controlled | (not inspected) | Function change type | ⚠ gap relation — 0 edges |
| `bauteilzustand` | id | controlled | (not inspected) | Component condition | ⚠ gap relation — 0 edges |
| `bauteilebene` | id | controlled | (not inspected) | Component scale (element/system/material) | ⚠ gap relation — 0 edges |

---

## 3. Relationships

### Populated relations (confirmed edges)

| From entity | Relationship | To entity | Cardinality | Count | Example |
|---|---|---|---|---|---|
| `*` (any) | `belongs_to_fallstudie` | `fallstudie` | N:1 | 1,618 | `reuse_einsatz/K118__001` → `fallstudie/K118_...` |
| `*` (any) | `belongs_to_projekt` | `projekt` | N:1 | 1,492 | → `projekt/K118_...` |
| `reuse_einsatz` | `has_bauteiltyp` | `bauteiltyp` | N:1 | 637 | → `bauteiltyp/Traeger` |
| `reuse_einsatz` | `installed_in_bauobjekt` | `bauobjekt` | N:1 | 637 | → `bauobjekt/K118_...` |
| `datenpunkt` | `measured_on_bauobjekt` | `bauobjekt` | N:1 | 617 | — |
| `datenpunkt` | `measures_kennwertdefinition` | `kennwertdefinition` | N:1 | 609 | → `kennwertdefinition/CO2_Einsparung` |
| `reuse_einsatz` | `uses_material` | `material` | N:1 | 553 | → `material/Stahl` |
| `reuse_einsatz` | `has_huerde` | `huerde` | N:M | 442 | → `huerde/Toleranzen` |
| `reuse_einsatz` | `has_reuse_einsatzstatus` | `reuse_einsatzstatus` | N:1 | 407 | → `reuse_einsatzstatus/realisiert` |
| `reuse_einsatz` | `has_prozessphase` | `prozessphase` | N:M | 394 | → `prozessphase/Rueckbau` |
| `akteur_beteiligung` | `has_akteurrolle` | `akteurrolle` | N:M | 298 | → `akteurrolle/Architektur` |
| `reuse_einsatz` | `has_reuse_strategie` | `reuse_strategie` | N:1 | 248 | → `reuse_strategie/Direkte_Wiederverwendung` |
| `akteur_beteiligung` | `relates_to_bauobjekt` | `bauobjekt` | N:1 | 238 | — |
| `reuse_einsatz` | `has_bewertungslogik_abgrenzung` | `bewertungslogik_abgrenzung` | N:1 | 164 | → `bewertungslogik_abgrenzung/zaehlt_als_Direct_Reuse` |
| `fallstudie` | `has_projekt` | `projekt` | 1:1 | 89 | — |
| `fallstudie` | `has_bauobjekt` | `bauobjekt` | 1:N | 88 | — |
| `reuse_einsatz` | `has_rueckbauverfahren` | `rueckbauverfahren` | N:M | 84 | → `rueckbauverfahren/Demontage` |
| `reuse_kettenstation` | `part_of_reuse_kette` | `reuse_kette` | N:1 | 84 | — |
| `reuse_einsatz` | `has_pruefung_nachweis` | `pruefung_nachweis` | N:M | 48 | → `pruefung_nachweis/Sichtpruefung` |
| `akteur_beteiligung` | `involves_akteur` | `akteur` | N:1 | 44 | → `akteur/baubüro_in_situ` |
| `reuse_einsatz` | `has_tragwerkstyp` | `tragwerkstyp` | N:1 | 26 | → `tragwerkstyp/Stahltragwerk` |
| `reuse_einsatz` | `has_fuegung_verbindung` | `fuegung_verbindung` | N:M | 21 | → `fuegung_verbindung/geschraubt` |
| `reuse_einsatz` | `references_norm` | `norm` | N:M | 9 | → `norm/ISO_20887` |
| `reuse_einsatz` | `has_leistungsanforderung` | `leistungsanforderung` | N:M | 3 | → `leistungsanforderung/Tragfaehigkeit` |

### Gap relations (defined in schema, 0 edges)

| From entity | Relationship | To entity | Notes |
|---|---|---|---|
| `reuse_einsatz` | `has_ressourcenquelle` | `ressourcenquelle` | Procurement origin type |
| `reuse_einsatz` | `has_beschaffungsweg` | `beschaffungsweg` | Procurement route |
| `reuse_einsatz` | `has_aufbereitungsverfahren` | `aufbereitungsverfahren` | Processing method |
| `reuse_einsatz` | `has_logistik` | `logistik` | Logistics type |
| `reuse_einsatz` | `has_funktionswechsel` | `funktionswechsel` | Function change |
| `reuse_einsatz` | `has_bauteilzustand` | `bauteilzustand` | Condition |
| `reuse_einsatz` | `has_bauteilebene` | `bauteilebene` | Scale layer |
| `reuse_einsatz` | `has_bauweise` | `bauweise` | Construction approach |
| `reuse_einsatz` | `has_bausystem` | `bausystem` | Named construction system |
| `reuse_einsatz` | `has_tragwerksprinzip` | `tragwerksprinzip` | Structural principle |
| `bauobjekt` | `has_bauobjektklasse` | `bauobjektklasse` | Building class |
| `bauobjekt` | `has_bauobjektrolle` | `bauobjektrolle` | Donor/receiver role |
| `bauobjekt` | `has_bauobjektstatus` | `bauobjektstatus` | Status |
| `bauobjekt` | `has_nutzung` | `nutzung` | Use type |
| `bauobjekt` | `has_bauaufgabe_intervention` | `bauaufgabe_intervention` | Intervention type |
| `bauobjekt` | `located_in_ort` | `ort` | Location (74 edges added in batch 50f) |
| `reuse_einsatz` | `has_rechtliche_bedingung` | `rechtliche_bedingung` | Legal condition |
| `reuse_einsatz` | `has_schadstoff` | `schadstoff` | Contaminant |
| `reuse_einsatz` | `has_kontextmerkmal` | `kontextmerkmal` | Context feature |
| `reuse_einsatz` | `has_zertifizierung_bewertungssystem` | `zertifizierung_bewertungssystem` | Certification |
| `reuse_einsatz` | `has_datenmodell` | `datenmodell` | Data model used |
| `reuse_einsatz` | `has_dokumenttyp` | `dokumenttyp` | Document type |
| `reuse_einsatz` | `has_tooltyp` | `tooltyp` | Tool category |
| `reuse_einsatz` | `uses_software_digitaltool` | `software_digitaltool` | Specific tool |
| `reuse_einsatz` | `documented_in_quelle` | `quelle` | ⚠ Source links missing across the board |
| `datenpunkt` | `has_datenqualitaet` | `datenqualitaet` | Quality level |
| `*` | `involves_foerderprogramm` | `foerderprogramm` | Funding program |
| `*` | `has_programm_kontext` | `programm_kontext` | Research context |
| `reuse_einsatz` | `has_methode` | `methode` | Method used |
| `reuse_einsatz` | `has_wirtschaft` | `wirtschaft` | Economic dimension |
| `bauobjekt` | `donor_for` | `bauobjekt` | ⚠ Missing: donor→receiver relationship not represented as edge |
| `reuse_einsatz` | `sourced_from_bauobjekt` | `bauobjekt` | ⚠ `herkunft_label` is free text; not linked to donor bauobjekt node |

---

## 4. Controlled Vocabularies / Categories

| Vocabulary name | Current values | Where used | Problems / overlaps / unclear terms |
|---|---|---|---|
| `bauteiltyp` | Stuetze, Traeger, Decke, Wand, Fassade, Fenster, Tuer, Treppe, Dach, Boden, Ausbau, Technik, Fundament, Gelaender, Daemmung | `has_bauteiltyp` on `reuse_einsatz` | Finalized; legacy variants (Leuchte, Sanitaerobjekt, Platte_Paneel, etc.) were remapped |
| `material` | Beton, Stahlbeton, Recyclingbeton, Stahl, Aluminium, Gusseisen, Holz, Glas, Ziegel, Naturstein, Keramik, Kunststoff, Daemmstoff, Lehm, Stroh | `uses_material` on `reuse_einsatz` | Finalized; Sekundärstahl, Brettschichtholz, etc. stored only as `material_label` free text |
| `reuse_strategie` | Direkte_Wiederverwendung, Same_Site_ReUse, Urban_Mining, Design_for_Disassembly, Bestandserhalt, Recycling, Upcycling, Remanufacturing, Adaptives_ReUse, Refurbishment, Weiterbauen_im_Bestand | `has_reuse_strategie` on `reuse_einsatz` | 11 nodes but schema §8 declares 8 canonical — Adaptives_ReUse, Refurbishment, Weiterbauen_im_Bestand are additions not in schema; overlap between Bestandserhalt and Weiterbauen_im_Bestand unclear |
| `reuse_einsatzstatus` | realisiert, geplant, verworfen, vorgeschlagen, unklar, temporaer, prototypisch | `has_reuse_einsatzstatus` | Solid; 7 values |
| `bewertungslogik_abgrenzung` | zaehlt_als_Direct_Reuse, zaehlt_nicht, Bestandserhalt_separat, Recycling_separat, Moebelsepearat, geplant_aber_nicht_realisiert, unklar | `has_bewertungslogik_abgrenzung` | Typo `Moebelsepearat` (should be `Moebel_separat`); 7 values |
| `huerde` | Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit, Schadstoffbelastung, Technische_Freigabe, Terminunsicherheit, Toleranzen, Unkonventionelles_Material, Verfuegbarkeitsproblem, Witterung_Feuchte, Zustand_Unklar | `has_huerde` on `reuse_einsatz` | 27 values; Gewaehrleistung/Haftung overlap |
| `prozessphase` | Rueckbau, Aufbereitung, Wiedereinbau, Transport, Lagerung, Pruefung, Identifikation, Entwurf, Ausschreibung, Bestandserfassung, Betrieb_und_Rueckbauplanung | `has_prozessphase` | 11 values; solid |
| `rueckbauverfahren` | Demontage, Selektiver_Rueckbau, Ausbau, Zerstoerungsarme_Bergung, schonender_Rueckbau | `has_rueckbauverfahren` | ~5–6 values; generic labels excluded from linking |
| `aufbereitungsverfahren` | Sandstrahlen, Entmoertelung_von_Fliesen, Holzaufbereitung, Rekonditionierung, Reparatur, Qualitaetssicherung, Leuchten_Refurbishment, Drahtglasschneiden | `has_aufbereitungsverfahren` | ~8 values |
| `fuegung_verbindung` | geschraubt, gesteckt, geschweisst, geklebt, vergossen, reversibel, irreversibel | `has_fuegung_verbindung` | `reversibel`/`irreversibel` are meta-categories, not specific techniques |
| `tragwerkstyp` | Holztragwerk, Stahltragwerk, Betontragwerk, wiederverwendetes_Tragwerk, demontierbares_Tragwerk | `has_tragwerkstyp` | ⚠ Mixes material-typed (first 3) with reuse-strategy-typed (last 2) — heterogeneous axis |
| `bauweise` | Holzbauweise, Massivbauweise, Stahlbauweise, Hybridbauweise, Fertigteilbauweise | `has_bauweise` (gap) | 5 values |
| `pruefung_nachweis` | Sichtpruefung, Statische_Nachweisfuehrung, Materialpruefung, Schadstoffscreening, Geometrische_Vermessung, Zugversuch, Brandnachweis, Abbrandbemessung, Schweissbarkeitspruefung, Eignungspruefung_Baulehm, Zustandsbewertung | `has_pruefung_nachweis` | 11 values; solid |
| `leistungsanforderung` | Tragfaehigkeit, Brandschutz, Schallschutz, Waermeschutz, Dauerhaftigkeit, Schadstofffreiheit, Rueckbaubarkeit, Feuchteschutz | `has_leistungsanforderung` | 8 values; only 3 edges linked — severely underused |
| `norm` | DIN_EN_15804, DIN_EN_15978, ISO_14040, ISO_14044, ISO_20887, F90, R90, REI90, Brandschutzanforderung, DIN_18940, Wiederverwendungskriterien, EU_Taxonomie, Feuerwiderstand | `references_norm` | 12+ values; only 9 edges linked — severely underused |
| `schadstoff` | Asbest, PCB, PAK, Bleifarbe, Holzschutzmittel | `has_schadstoff` (gap) | 5 values |
| `akteurrolle` | Architektur, Tragwerksplanung, Bauherr_Auftraggeber, Nachhaltigkeitsberatung, Reuse_Beratung, Materiallieferant, Projektmanagement_Koordination | `has_akteurrolle` | ~10+ values; some actors hold multiple roles |
| `methode` | Materialpass, Design_for_Disassembly, Urban_Mining, Form_Follows_Availability, Materialinventur, Building_Material_Scouting, Bauteilkatalogisierung, ReUse_Assessment, Reversibilitaet, Zirkulaere_Ausschreibung, Bestandserhalt | `has_methode` (gap) | Bestandserhalt and DfD overlap with `reuse_strategie` |
| `datenqualitaet` | belegt, teilweise_belegt, unbekannt, umstritten (implied) | `has_datenqualitaet` (gap) | Only as prose `Vertrauensgrad` in datenpunkt body; not graph edges |
| `ort` | Berlin, Basel, Bruessel, Oslo, London, … (53+ city nodes) | `located_in_ort` | Hierarchical structure not enforced; `Scwheiz` typo |

---

## 5. Example Records

### Record 1 — Case Study (fallstudie)

**Entity:** `fallstudie`
**ID:** `K118_Kopfbau_Halle_118_Winterthur`
**Title:** K.118 – Kopfbau Halle 118, Winterthur

| Field | Value |
|---|---|
| entity | `fallstudie` |
| bauobjekt | `K118_Kopfbau_Halle_118_Winterthur` |
| projekt | `K118_Kopfbau_Halle_118_Winterthur` |
| build_status | `promoted_phase42` |
| body | Rich German prose: Kurzdefinition, Relevanz, Fachinhalt, Praxisbezug |

**Related records:** 12 `reuse_einsatz` nodes, 9 `datenpunkt` nodes, edges to `huerde`, `bauteiltyp`, `material`, `prozessphase`, `reuse_strategie`, `reuse_einsatzstatus`

**Missing:** `quelle` links (only shorthand `[S1]–[S6]`), `ort` edge, `bauaufgabe_intervention`, `akteur_beteiligung` nodes (actors named in prose but not extracted as edges)

---

### Record 2 — Reuse Use-Case (reuse_einsatz)

**Entity:** `reuse_einsatz`
**ID:** `BedZED_London_Hackbridge__001__Stahlrahmen_Stahlprofile`

| Field | Value |
|---|---|
| bauteil_label | `"Stahlrahmen / Stahlprofile"` |
| material_label | `"Stahl"` |
| herkunft_label | `"Lokale Abbruchstandorte im 35-mile-Radius; teilweise Brighton Railway Station"` |
| alte_funktion | `"Tragende Stahlbauteile in früheren Gebäuden"` |
| neue_funktion | `"Tragende Stahlrahmen, v. a. Workspaces"` |
| menge_umfang | `"98 t; 95 % des tragenden Stahls"` |
| pruefung_label | `"Sichtprüfung; Herstellungsdatum; Rost/Scaling; vorhandene Verbindungen; Fabrikationseignung"` |
| norm_recht_label | `"Historic Sections Book; sonst unbekannt"` |
| huerde_label | `"Profilverfügbarkeit; gebogene Profile nicht verfügbar/akzeptiert"` |
| quelle_label | `"S4, S2"` |
| fallstudie | `fallstudie/BedZED_London_Hackbridge` |

**Graph edges present:** `has_bauteiltyp`, `installed_in_bauobjekt`, `uses_material`, `has_huerde`, `has_reuse_einsatzstatus`, `has_prozessphase`, `has_reuse_strategie`, `has_bewertungslogik_abgrenzung`, `has_rueckbauverfahren`, `has_pruefung_nachweis`

**Missing edges:** `has_aufbereitungsverfahren` (Sandstrahlen is in prose), `has_logistik`, `has_ressourcenquelle`, donor `bauobjekt` link, `documented_in_quelle`

---

### Record 3 — Data Point (datenpunkt)

**Entity:** `datenpunkt`
**ID:** `K118_Kopfbau_Halle_118_Winterthur__001__Fl_che`

| Field | Value |
|---|---|
| wert | `"1.100"` (= 1,100 m²; German thousands separator) |
| einheit | `"m²"` |
| quelle_label | `"[S2], [S4]"` |
| Vertrauensgrad | `belegt` |
| Bilanzgrenze | `Aufstockung` |
| Methode | `Projektangabe` |
| fallstudie | `fallstudie/K118_...` |
| bauobjekt | `K118_...` |

**Graph edges:** `measured_on_bauobjekt`, `measures_kennwertdefinition`

**Missing:** `documented_in_quelle`, `has_datenqualitaet` edge; conflicting values not modeled with explicit `contradicts` edge

---

### Record 4 — General Knowledge Knot (huerde)

**Entity:** `huerde`
**ID:** `Toleranzen`

| Field | Value |
|---|---|
| body | German prose explaining the dimensional tolerance hurdle in reuse |
| Linked by | 442 `reuse_einsatz` nodes (most frequent hurdle in database) |

---

### Record 5 — Actor Involvement (akteur_beteiligung)

**Entity:** `akteur_beteiligung`
**ID:** `55_Great_Suffolk_Street_London__001__Fabrix`

| Field | Value |
|---|---|
| involves_akteur | `akteur/Fabrix` |
| has_akteurrolle | `akteurrolle/Bauherr_Auftraggeber` |
| relates_to_bauobjekt | `bauobjekt/55_Great_Suffolk_Street_London` |
| belongs_to_fallstudie | `fallstudie/55_Great_Suffolk_Street_London` |
| belongs_to_projekt | `projekt/55_Great_Suffolk_Street_London` |

---

## 6. Source and Evidence Structure

**Current state:** Partially implemented — structurally weak.

| Aspect | Status |
|---|---|
| `quelle` folder exists | Yes — but contains mostly legacy Markdown stubs, not structured citation records |
| Citation fields | `quelle_label` on `reuse_einsatz` and `datenpunkt` uses shorthand codes like `[S1]`, `S4` |
| Resolution of shorthand to full source | ⚠ Not done — shorthand is case-local; no global quelle ID cross-reference |
| `documented_in_quelle` edges | 0 currently (gap relation, not yet populated) |
| Claims linked to sources | ⚠ Only via `quelle_label` free-text field; no graph edges |
| Data points linked to sources | ⚠ Same — `quelle_label` in frontmatter, not an edge |
| Source types (in legacy stubs) | Publikation, Pre_Demolition_Audit, Bauteilkatalog, LCA, Materialpass, Materialinventar, Materialsheet, Auditbericht, Ausschreibungstext, Bauwerksdiagnose, ReUse_Toolkit, Reversibilitaetskonzept, Rueckbaukataster, Specification_Method, Opalis_Datenbank, Bestandsaufnahme |
| Page numbers / excerpts | Not stored |
| Primary vs secondary source | Not distinguished in graph |
| Interview records | `interview_md` exists as stub; no structured interview records |
| Conflicting values | Multiple `datenpunkt` nodes created for same KPI with different values — but no explicit `contradicts` or `alternative_value` edge |

---

## 7. Current Problems

### Structural / Graph

1. **`quelle_label` is unresolved shorthand.** `[S1]`, `S4` etc. on every `reuse_einsatz` and `datenpunkt` are not linked to `quelle` nodes. The graph cannot answer "which sources support this claim?" — the evidence layer is essentially missing from the graph.

2. **Donor bauobjekt not linked.** `herkunft_label` (e.g. `"Teilrückbau Halle ELYS Basel"`) is free text on `reuse_einsatz`. The donor building is often a named `bauobjekt` in the same database, but no `sourced_from_bauobjekt` edge connects them.

3. **~30 gap relations not yet populated.** The graph has 24 populated relation types but the schema defines ~54. Many important contextual attributes (`has_bauweise`, `has_bausystem`, `has_nutzung`, `has_methode`, `has_wirtschaft`, `has_schadstoff`, `has_rechtliche_bedingung`, `has_logistik`, `has_aufbereitungsverfahren`) are only in prose or `_label` fields.

4. **`fallstudie`, `projekt`, and `bauobjekt` share the same ID** in ~96 cases. Intentional by design but can confuse graph traversal — three separate node types with identical IDs collapse in naive queries.

5. **`reuse_kette` and `reuse_kettenstation` underused.** Only 84 `part_of_reuse_kette` edges exist; chains are not fully modeled for most cases.

### Terminology / Vocabulary

6. **Mixed German/English throughout.** Case titles, bauteil_labels, and prose mix German and English (especially UK/NL/BE cases). Cross-language queries require normalization.

7. **`methode` and `reuse_strategie` overlap.** `Design_for_Disassembly` and `Bestandserhalt` appear in both entity types with different granularity. No rule resolves which to use.

8. **`tragwerkstyp` mixes axes.** `wiederverwendetes_Tragwerk` and `demontierbares_Tragwerk` are reuse strategies, while `Holztragwerk`, `Stahltragwerk`, `Betontragwerk` are material classifications. These should be separate dimensions.

9. **`reuse_strategie` has 11 nodes, schema says 8.** Three additions (`Adaptives_ReUse`, `Refurbishment`, `Weiterbauen_im_Bestand`) are present but not in canonical schema §8.

10. **`bewertungslogik_abgrenzung` has a typo.** `Moebelsepearat` should be `Moebel_separat`.

11. **`ort/Scwheiz_md`** — typo; should be `Schweiz`.

12. **`datenqualitaet` not linked as edges.** Only used as `Vertrauensgrad` prose field in datenpunkt body. Cannot graph-query "how many data points are only partially verified?"

### Data Quality

13. **`menge_umfang` is a mixed-format string.** Contains quantities, percentages, and "unbekannt" in a single free-text field. Cannot be used for numeric aggregation without parsing.

14. **`wert` in datenpunkt stored as string.** Uses German number formatting (`"1.100"` = 1,100; `"3.404"` = 3,404). Needs type conversion for any quantitative analysis.

15. **`einheit` is uncontrolled.** `"m²"`, `"t"`, `"kgCO₂e"`, `"tCO₂e"`, `"kg CO₂"` etc. — units are not normalized.

16. **5 unmapped gebaeude/ files** not yet extracted into the graph (see HANDOFF.md §5 Step 2).

17. **`build_status: promoted_phase42`** on essentially every node — not informative for ongoing work; could be removed or repurposed.

18. **Legacy folder duplication risk.** Top-level legacy folders (`akteur/`, `material/`, `projekt/`, etc.) still exist alongside canonical `_database/` equivalents — user could edit wrong copy.

---

## 8. Reuse-Specific Extraction Readiness

| Capability | Ready? | Notes |
|---|---|---|
| A project with many separate reuse cases | ✅ Yes | `fallstudie` → `reuse_einsatz` (N) via `belongs_to_fallstudie`; e.g. Brighton Waste House has 12 `reuse_einsatz` nodes |
| A reused component with donor object, receiver object, material, quantity, condition, function change | ⚠ Partial | Material ✅, receiver bauobjekt ✅, bauteil_label ✅, menge_umfang ✅ (but free text), condition (`bauteilzustand`) ❌ not linked, function change (`alte_funktion`/`neue_funktion`) ❌ only free text, donor bauobjekt ❌ only `herkunft_label` free text |
| A reuse chain with stations (donor, dismantling, storage, transport, processing, receiver) | ⚠ Partial | `reuse_kette` and `reuse_kettenstation` exist; only 84 chain edges populated; most cases don't have fully modeled chains |
| Actors and their roles | ✅ Yes | `akteur_beteiligung` + `akteurrolle` fully populated; 298 role edges |
| Hurdles and how they were solved | ⚠ Partial | Hurdles linked (442 edges) ✅; "how solved" has no relation type — no `huerde_loesung` edge or entity |
| Regulations, norms, and performance requirements | ⚠ Weak | `references_norm`: 9 edges; `has_leistungsanforderung`: 3 edges; `has_rechtliche_bedingung`: 0 edges — severely sparse |
| CO₂, mass, cost, area, quantity, and other data points | ✅ Yes (structurally) | `datenpunkt` nodes exist for all these KPIs; 609 `measures_kennwertdefinition` edges |
| Conflicting values from different sources | ⚠ Partial | Multiple `datenpunkt` nodes for same KPI exist (e.g. BioPartner Stahlmasse 001+002); no explicit `contradicts` or `alternative_source_value` edge |
| Uncertainty and data quality | ⚠ Weak | `Vertrauensgrad` exists as prose field; `has_datenqualitaet` relation not yet populated; cannot graph-query data quality |
| Difference between Direct Reuse, Bestandserhalt, Recycling, Upcycling, DfD | ✅ Yes | `reuse_strategie` vocabulary covers all; `bewertungslogik_abgrenzung` prevents overcounting; well-designed |

---

## 9. Summary Statistics (as of 2026-05-09)

| Metric | Value |
|---|---|
| Total nodes | 3,043 |
| Total edges | 9,256 |
| Populated relation types | 24 (+6 partially from batch 50a–50j) |
| Defined but empty relation types | ~30 |
| `fallstudie` nodes | ~96 |
| `reuse_einsatz` nodes | ~637 |
| `datenpunkt` nodes | ~600+ |
| `akteur_beteiligung` nodes | estimated ~300+ |
| Controlled knot entity types | ~35 |
| Dangling endpoints | 0 |
| Type mismatches | 0 |
| `rule_low` edges | 0 |
| Mojibake titles | 0 |

---

## Notes for Critiquing Agent

- The **query center is `reuse_einsatz`** — all analytical queries should start here.
- The **source evidence layer is the biggest structural gap**: `quelle_label` shorthand codes are case-local and unresolved, `documented_in_quelle` edges are missing, no citations link claims to sources in the graph.
- The **donor building relationship is missing as an edge**: `herkunft_label` is prose only.
- **~30 contextual relation types** are defined in the schema but have 0 populated edges — the graph is ~45% complete by relation coverage.
- The prose content (`index.md` bodies) is rich and high-quality; the structured graph layer is still being built from it.
- The `Gebäude/` folder (source files) is the gold standard for what edges should eventually exist — every ENTITÄTEN-MAPPING and BAUTEIL-INVENTAR table row is a potential edge.
- Mixed-language case titles and labels are intentional (international case studies); normalizing them would require a translation/mapping layer.
