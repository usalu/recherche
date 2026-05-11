---
name: Neo4j schema catalogue
overview: Explicit catalogue of all Node Labels (with their property schemas) and Edge Types (with their property schemas) for the Neo4j export. Reuse-Einsatz is reified as :Bauteilgruppe; :Fallstudie and :Projekt are removed and replaced by a :Bauwerk super-label with physical-type sub-Labels (:Gebaeude, :Pavillon, …); Datenpunkten are replaced by one Label per Kennwert; :Quelle is kept and cited via :BELEGT. Five generic edge types only — IST, HAT, BENUTZT, GEHÖRT_ZU, BELEGT.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the 4-section structure: §1 Node-type catalogue, §2 Nodes (per-Label property tables), §3 Edge-type catalogue, §4 Edges (per-edge-type property tables). Plus appendices for principles, constraints, coverage, renamings."
    status: pending
  - id: write-1
    content: "Write §1 Node-type catalogue: enumerate every Label across the four families with one-line purpose."
    status: pending
  - id: write-2
    content: "Write §2 Nodes: per-Label property table (name | type | required | source field | notes)."
    status: pending
  - id: write-3
    content: "Write §3 Edge-type catalogue: enumerate the 5 edge types with one-line purpose, source/target Label families, legacy relations folded in."
    status: pending
  - id: write-4
    content: "Write §4 Edges: per-edge-type property table (name | type | required | description)."
    status: pending
  - id: appendices
    content: "Write the appendices: A modeling principles (hybrid A/B/C, naming, multi-label), B constraints & indexes, C coverage checklist (every folder + every legacy relation + every YAML field accounted for), D renamings (fallstudie/projekt merge, reuse_einsatz→:Bauteilgruppe, typo fixes, tragwerkstyp axis split)."
    status: pending
---

# Goal

Author `_database/_system/NEO4J_SCHEMA.md` as the single source of truth for the Neo4j model, organized in the four-part order requested:

1. **§1 Node-type catalogue** — the list of all Labels.
2. **§2 Nodes** — for each Label, its complete property table.
3. **§3 Edge-type catalogue** — the list of all 5 edge types.
4. **§4 Edges** — for each edge type, its complete property table.

Plus appendices (principles, constraints, coverage, renamings) that don't get in the way of the catalogue.

The rest of this plan is the **concrete content draft** for those four sections so you can confirm before I write the file.

---

# §1 Node-type catalogue

## §1.A Physical objects (multi-label hierarchy)

Every physical object carries `:Bauwerk` plus one or more type sub-Labels.

| Label | Purpose |
|---|---|
| `:Bauwerk` | Super-label for every built physical thing |
| `:Gebaeude` | Ordinary building |
| `:Pavillon` | Pavilion / demonstration / temporary structure |
| `:Bruecke` | Bridge |
| `:Halle` | Large hall / shed |
| `:Lager` | Warehouse / depot / material storage |
| `:Innenausbau` | Interior fit-out as the case-study unit |
| `:Anlage` | Infrastructure / external facility |

## §1.B Reified relations & instance nodes

| Label | Purpose |
|---|---|
| `:Bauteilgruppe` | A group of components in a Bauwerk — replaces legacy `:ReuseEinsatz` |
| `:Akteur` | Office / company / authority / institution |
| `:AkteurBeteiligung` | Actor × Bauwerk × role (reified Mode-C) |
| `:ReuseKette` | Full reuse chain |
| `:ReuseKettenstation` | Station in a reuse chain |
| `:BauwerkBeteiligung` | Bauwerk × ReuseKette × role (reified) |
| `:Quelle` | Source / citation / document |
| `:SoftwareDigitaltool` | Concrete platform (Madaster, Concular, …) |

## §1.C Measurement Labels (one per Kennwert)

Replaces legacy `:Datenpunkt`. All share a common property shape (see §2.C).

| Label | Kennwert covered |
|---|---|
| `:Flaeche` | Fläche, Projektfläche, Gebäudefläche |
| `:CO2_Einsparung` | CO₂-Einsparung (relativ / absolut) |
| `:CO2_Footprint` | CO₂-Footprint, GWP |
| `:CO2_Reduktion` | CO₂-Reduktion Materialien |
| `:Reuse_Anteil` | Anteil reused/upcycled/secondary in % |
| `:Sekundaere_Materialien` | Menge sekundärer Materialien |
| `:Geerntete_Materialien` | Menge geernteter Materialien |
| `:Masse` | Masse in t, kg |
| `:Volumen` | Volumen in m³ |
| `:Kosten` | Kosten gesamt |
| `:Budget` | Budget gesamt |
| `:Anteil_an_Baukosten` | Anteil an Baukosten in % |
| `:Wohneinheiten` | Anzahl Wohneinheiten |
| `:Lebensdauer` | Lebensdauer in Jahren |
| `:Bauzeit` | Bauzeit in Monaten |
| `:Fertigstellung` | Fertigstellungsjahr |
| `:Entwurfsbeginn` | Entwurfsbeginnjahr |
| `:Energieverbrauch` | Energieverbrauch |
| `:Wassereinsparung` | Wassereinsparung |
| `:Restlebensdauer` | Restlebensdauer |
| `:Abfall_vermieden` | vermiedener Abfall |
| `:Vermiedene_Umweltschaeden` | vermiedene Umweltschäden |
| `:Zielwert_Reuse` | Reuse-Zielwert |
| `:Stueckzahl` | Stückzahlen (Fenster, Stahlträger, …) |
| `:Gebaeudemasse` | erhaltene Gebäudemasse |
| `:Bestandslager` | Bestandslager-Volumen |

Final list comes from enumerating `_database/kennwertdefinition/`.

## §1.D Vocabulary Labels (all multi-labelled `:<Label>:Vokabular`)

| Label | Domain |
|---|---|
| `:Bauteiltyp` | Stütze, Träger, Decke, Wand, Fassade, Fenster, Tür, Treppe, Dach, Boden, Ausbau, Technik, Fundament, Geländer, Dämmung (15) |
| `:Bauteilgruppentyp` | wiederverwendet, original, hybrid (new — 3) |
| `:Material` | Beton, Stahlbeton, Recyclingbeton, Stahl, Aluminium, Gusseisen, Holz, Glas, Ziegel, Naturstein, Keramik, Kunststoff, Dämmstoff, Lehm, Stroh (15) |
| `:Bauteilebene` | Bauteil-Skalenebene |
| `:Bauteilzustand` | Zustandsbewertung |
| `:Funktionswechsel` | Art der Funktionsänderung |
| `:Tragwerkstyp` | Holztragwerk, Stahltragwerk, Betontragwerk (material-typed only — 3) |
| `:Tragwerksprinzip` | Skelett, Massiv, Fachwerk, Rahmen, Plattentragwerk |
| `:Bauweise` | Holzbauweise, Massivbauweise, Stahlbauweise, Hybridbauweise, Fertigteilbauweise |
| `:Bausystem` | Named systems (Betonfertigteil-System, Holzrahmenbau, …) |
| `:FuegungVerbindung` | geschraubt, gesteckt, geschweißt, geklebt, vergossen, reversibel, irreversibel |
| `:ReuseStrategie` | Direct Reuse, Same-Site Reuse, Urban Mining, DfD, Bestandserhalt, Recycling, Upcycling, Remanufacturing (canonical 8) |
| `:ReuseEinsatzstatus` | realisiert, geplant, verworfen, vorgeschlagen, unklar, temporär, prototypisch (7) |
| `:BewertungslogikAbgrenzung` | zählt als Direct Reuse, zählt nicht, Bestandserhalt separat, Recycling separat, Möbel separat, geplant aber nicht realisiert, unklar (7) |
| `:Ressourcenquelle` | Herkunftstyp (Recycling-Hof, Direktabbruch, …) |
| `:Beschaffungsweg` | Beschaffungs-Route |
| `:Prozessphase` | Rückbau, Aufbereitung, Wiedereinbau, Transport, Lagerung, Prüfung, Identifikation, Entwurf, Ausschreibung, Bestandserfassung, Betrieb_und_Rückbauplanung (11) |
| `:Rueckbauverfahren` | Demontage, Selektiver_Rückbau, Ausbau, Zerstoerungsarme_Bergung, schonender_Rückbau |
| `:Aufbereitungsverfahren` | Sandstrahlen, Entmörtelung, Holzaufbereitung, Rekonditionierung, Reparatur, Qualitätssicherung, Leuchten_Refurbishment, Drahtglasschneiden |
| `:Logistik` | Transport, Lagerung, Materialmatching, Materialverfügbarkeit, Lagerfläche, ReUse_Centre |
| `:Methode` | Materialpass, DfD, Urban_Mining, Form_Follows_Availability, Materialinventur, Building_Material_Scouting, Bauteilkatalogisierung, ReUse_Assessment, Reversibilitaet, Zirkulaere_Ausschreibung, Bestandserhalt |
| `:Huerde` | 27 hurdle types (Toleranzen, Datenlücke, Brandschutzkonflikt, …) |
| `:PruefungNachweis` | Sichtprüfung, Statische_Nachweisführung, Materialprüfung, Schadstoffscreening, Geometrische_Vermessung, Zugversuch, Brandnachweis, Abbrandbemessung, Schweissbarkeitsprüfung, Eignungsprüfung_Baulehm, Zustandsbewertung |
| `:Leistungsanforderung` | Tragfähigkeit, Brandschutz, Schallschutz, Wärmeschutz, Dauerhaftigkeit, Schadstofffreiheit, Rückbaubarkeit, Feuchteschutz |
| `:Norm` | DIN_EN_15804, DIN_EN_15978, ISO_14040, ISO_14044, ISO_20887, F90, R90, REI90, … |
| `:RechtlicheBedingung` | Rechtliche Rahmenbedingungen |
| `:Schadstoff` | Asbest, PCB, PAK, Bleifarbe, Holzschutzmittel |
| `:Bauobjektklasse` | Wohngebäude, Bürogebäude, Industriegebäude, Pavillon, … |
| `:Bauobjektrolle` | Donor / Receiver / Stand-Alone |
| `:Bauobjektstatus` | bestehend, abgerissen, geplant, … |
| `:Nutzung` | Wohnen, Büro, Produktion, Kultur, … |
| `:BauaufgabeIntervention` | Neubau, Umbau, Sanierung, Aufstockung, Rückbau, … |
| `:Kontextmerkmal` | freie Kontextmerkmale |
| `:Ort` | 53+ Städte mit Self-Loop GEHÖRT_ZU für Stadt → Land |
| `:Akteurrolle` | Architektur, Tragwerksplanung, Bauherr_Auftraggeber, Nachhaltigkeitsberatung, Reuse_Beratung, Materiallieferant, Projektmanagement_Koordination |
| `:Datenqualitaet` | belegt, teilweise_belegt, unbekannt, umstritten |
| `:Datenmodell` | benutztes Datenmodell |
| `:Dokumenttyp` | Publikation, Pre_Demolition_Audit, Materialpass, Materialinventar, Bauteilkatalog, … |
| `:Tooltyp` | Tool-Kategorie |
| `:ZertifizierungBewertungssystem` | DGNB, BREEAM, LEED, … |
| `:Wirtschaft` | Kostenvergleich, Lebenszykluskosten, Geschäftsmodell, Finanzierung, Preisbildung, Restwert |
| `:Foerderprogramm` | FCRBE, PREUSE, BBSM, Reallabor_Be_Ware, Zukunftbau |
| `:ProgrammKontext` | Forschungsprogramm-Kontext |
| `:Einheit` (new) | m², t, kg, kgCO₂e, tCO₂e, m³, Stück, EUR, Jahre, Monate, % |
| `:Kennwertdefinition` | Kennwert-Taxonomie (Fläche, CO₂-Einsparung, …) — bleibt parallel zu den Measurement-Labels als Grouping-Vokabular |

## §1.E Auxiliary

| Label | Purpose |
|---|---|
| `:BuildBatch` | One node per migration batch (e.g. `phase42`, `phase50a`) for provenance |

---

# §2 Nodes — properties per Label

Property table columns: **name** | **type** | **req** | **source / mode** | **notes**.

`A` = Mode A (property only); `B` = Mode B (also has an outgoing edge to a vocab node); `C` = part of Mode C (reified node).

## §2.A Physical-object Labels

All physical-object Labels share the same property schema; the differentiator is the multi-Label tag.

### `:Bauwerk` (and its sub-Labels `:Gebaeude` / `:Pavillon` / `:Bruecke` / `:Halle` / `:Lager` / `:Innenausbau` / `:Anlage`)

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug under `_database/bauobjekt/<id>/` | UNIQUE per Label |
| `title` | string | ✓ | YAML `title` | |
| `body_md` | string | ✓ | merged from legacy bauobjekt + fallstudie + projekt body | concatenated under `## Fallstudie` / `## Projekt` / `## Bauobjekt` subheaders |
| `fertigstellung_jahr` | int? | – | parsed from prose or YAML | A |
| `legacy_paths` | list&lt;string&gt; | – | provenance | A |
| `build_status` | string? | – | YAML `build_status` | A |

## §2.B Reified-relation Labels

### `:Bauteilgruppe`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | legacy `reuse_einsatz` id, e.g. `K118_Kopfbau__001__Stahltr_ger_St_tzen` | UNIQUE |
| `title` | string | ✓ | YAML `title` | |
| `bauteil_label` | string | ✓ | YAML `bauteil_label` (`"Stahlträger / Stützen"`) | A — fine label kept verbatim |
| `material_label` | string | ✓ | YAML `material_label` (`"Brettschichtholz"`) | A — fine label kept verbatim |
| `menge_umfang_raw` | string | – | YAML `menge_umfang` verbatim | A |
| `alte_funktion` | string? | – | YAML | A |
| `neue_funktion` | string? | – | YAML | A |
| `herkunft_label` | string? | – | YAML `herkunft_label` verbatim | A |
| `pruefung_label_raw` | string? | – | YAML `pruefung_label` verbatim | A |
| `norm_recht_label_raw` | string? | – | YAML `norm_recht_label` verbatim | A |
| `huerde_label_raw` | string? | – | YAML `huerde_label` verbatim | A |
| `quelle_label_raw` | string? | – | YAML `quelle_label` verbatim (e.g. `"S4, S2"`) | A |
| `body_md` | string | ✓ | German prose | A |
| `legacy_paths` | list&lt;string&gt; | – | provenance | A |
| `build_status` | string? | – | YAML | A |

### `:Akteur`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug under `_database/akteur/<id>/` | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | German prose | A |
| `legacy_paths` | list&lt;string&gt; | – | | A |

### `:AkteurBeteiligung`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | slug `<case>__<NNN>__<akteur>` | UNIQUE |
| `legacy_paths` | list&lt;string&gt; | – | | A |

(All other content lives on outgoing edges — see §4.)

### `:ReuseKette`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | A |

### `:ReuseKettenstation`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | – | | A |
| `position` | int | ✓ | parsed | A |

### `:BauwerkBeteiligung` (renamed from :BauobjektBeteiligung)

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | slug | UNIQUE |

### `:Quelle`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug under `_database/quelle/<id>/` OR derived per-case for resolved shorthand | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | A |
| `case_id` | string? | – | case the shorthand was scoped to | A |
| `citation_short` | string? | – | `"S4"` | A |
| `citation_full` | string? | – | full reference text | A |
| `quelle_typ` | string? | – | Publikation, Pre_Demolition_Audit, Materialpass, … | A (parallel `IST→:Dokumenttyp` edge) |
| `url` | string? | – | | A |
| `seite` | string? | – | optional default page | A |

### `:SoftwareDigitaltool`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | | A |
| `url` | string? | – | | A |

## §2.C Measurement Labels (shared property shape)

All measurement Labels (`:Flaeche`, `:CO2_Einsparung`, `:Reuse_Anteil`, `:Masse`, `:Kosten`, `:Wohneinheiten`, `:Volumen`, `:Lebensdauer`, `:Bauzeit`, `:Fertigstellung`, `:Energieverbrauch`, `:Wassereinsparung`, `:Restlebensdauer`, `:Abfall_vermieden`, `:Vermiedene_Umweltschaeden`, `:Zielwert_Reuse`, `:Stueckzahl`, `:Gebaeudemasse`, `:Bestandslager`, `:Budget`, `:Anteil_an_Baukosten`, `:CO2_Footprint`, `:CO2_Reduktion`, `:Sekundaere_Materialien`, `:Geerntete_Materialien`, `:Entwurfsbeginn`) carry the same properties:

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | legacy datenpunkt id | UNIQUE |
| `title` | string | ✓ | YAML | |
| `wert_raw` | string | ✓ | YAML `wert` verbatim (`"1.100"`, `"250 / 312 / 400"`) | A — preserves original notation |
| `wert_values` | list&lt;float&gt; | – | parsed German-number-aware | A |
| `einheit_raw` | string | ✓ | YAML `einheit` | A |
| `einheit_norm` | string | – | canonical | A (parallel `IST→:Einheit` edge) |
| `bilanzgrenze` | string? | – | body | A |
| `methode_text` | string? | – | body | A |
| `vertrauensgrad` | string? | – | body | A (parallel `IST→:Datenqualitaet` edge) |
| `widerspricht_id` | string? | – | id of contradicting measurement | A |
| `body_md` | string | ✓ | | A |
| `quelle_label_raw` | string? | – | YAML `quelle_label` verbatim | A |
| `legacy_paths` | list&lt;string&gt; | – | | A |

## §2.D Vocabulary Labels (shared property shape)

All vocab Labels (every Label in §1.D) carry `:<Label>:Vokabular` and share:

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | folder slug under `_database/<vocab>/<id>/` | UNIQUE |
| `title` | string | ✓ | YAML | |
| `body_md` | string | ✓ | German prose of the knot | A |
| `legacy_paths` | list&lt;string&gt; | – | | A |

`:Ort` has additionally:

| name | type | req | notes |
|---|---|---|---|
| `iso_country` | string? | – | when target node is a country |
| `koordinaten` | string? | – | optional lat/lon |

## §2.E Auxiliary

### `:BuildBatch`

| name | type | req | source | notes |
|---|---|---|---|---|
| `id` | string | ✓ | e.g. `phase42`, `phase50a` | UNIQUE |
| `description` | string? | – | | A |
| `datum` | date? | – | | A |

---

# §3 Edge-type catalogue

Five generic predicates. No edge-as-edge from reuse_einsatz.

| Edge | Subject Labels | Object Labels | Cardinality | Purpose |
|---|---|---|---|---|
| `IST` | any | vocab | N:1 per axis | classification / identity / status / role |
| `HAT` | `:Bauteilgruppe`, `:Bauwerk`, measurement, `:AkteurBeteiligung` | vocab (rich body) | N:M | qualitative attribute / feature |
| `BENUTZT` | `:Bauteilgruppe`, `:Bauwerk` | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:SoftwareDigitaltool`, `:Datenmodell` | N:M | instrumental usage / quantitative consumption |
| `GEHÖRT_ZU` | any | container Labels | N:1 / N:M | membership / containment / location / scope / origin |
| `BELEGT` | `:Quelle` | any cited node | N:M | citation / evidence |

**Legacy relations folded into each edge type:**

- **IST:** `has_bauteiltyp`, `has_reuse_einsatzstatus`, `has_reuse_strategie`, `has_bewertungslogik_abgrenzung`, `has_tragwerkstyp`, `has_akteurrolle`, `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_bauobjektstatus`, `has_dokumenttyp`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`, plus new `has_bauteilgruppentyp` and new `has_einheit`.
- **HAT:** `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff`, `has_kontextmerkmal`, `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung`, `has_logistik`, `has_wirtschaft`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool`, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt`, new `sourced_from_bauobjekt`, `part_of_reuse_kette`, `located_in_ort`, `relates_to_bauobjekt`, `involves_akteur`, `involves_foerderprogramm`, `has_programm_kontext`, `measured_on_bauobjekt`, `measures_kennwertdefinition`. (Legacy `belongs_to_fallstudie`, `belongs_to_projekt`, `has_projekt`, `has_bauobjekt` are **dropped** because `:Fallstudie` and `:Projekt` no longer exist as Labels.)
- **BELEGT:** new — replaces unresolved `quelle_label` shorthand and the planned `documented_in_quelle` gap relation.

---

# §4 Edges — properties per edge type

## §4.A `:IST`

| name | type | req | notes |
|---|---|---|---|
| `seit` | date? | – | optional start of validity |
| `bis` | date? | – | optional end of validity |
| `gewichtung` | float? | – | 0..1 confidence |
| `quelle_id` | string? | – | source ref shorthand (parallel to `:BELEGT` edge) |

## §4.B `:HAT`

| name | type | req | notes |
|---|---|---|---|
| `art` | string | ✓ | discriminator: `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"schadstoff"`, `"kontext"`, `"recht"`, `"nutzung"`, `"intervention"`, `"fuegung"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"` |
| `anzahl` | int? | – | multiplicity |
| `intensitaet` | string? | – | qualitative strength (`"gering"`, `"mittel"`, `"hoch"`) |
| `quelle_id` | string? | – | source ref |

## §4.C `:BENUTZT`

| name | type | req | notes |
|---|---|---|---|
| `anzahl` | float? | – | quantity used |
| `einheit` | string? | – | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float? | – | share-of-total in % |
| `funktion_alt` | string? | – | original role of the consumed thing |
| `funktion_neu` | string? | – | new role |
| `aufbereitung` | string? | – | processing applied (free text, e.g. `"Sandstrahlen"`) |
| `quelle_id` | string? | – | source ref |

## §4.D `:GEHÖRT_ZU`

| name | type | req | notes |
|---|---|---|---|
| `rolle` | string | ✓ | one of `"einbauort"`, `"herkunft"`, `"bauwerk"`, `"kette"`, `"ort"`, `"kontext"`, `"foerderprogramm"`, `"akteur"`, `"misst"`, `"messung_objekt"`, `"batch"` |
| `position` | int? | – | ordering in a sequence (chain station number) |
| `seit` | date? | – | start of validity |
| `bis` | date? | – | end of validity |
| `quelle_id` | string? | – | source ref |

## §4.E `:BELEGT`

| name | type | req | notes |
|---|---|---|---|
| `seite` | string? | – | page number |
| `excerpt` | string? | – | quoted excerpt |
| `raw_label` | string? | – | original shorthand, e.g. `"S4"`, `"[S1]"` |

---

# Appendix A — Modeling principles

- **Hybrid Modes A/B/C** coexist. Many fields use A + B (raw label as property AND canonical taxonomy as edge).
- **German PascalCase Labels**, **SCREAMING_SNAKE edges**, **snake_case properties**.
- **Multi-label** physical-object hierarchy (`:Bauwerk:Gebaeude`).
- **Reuse-Einsatz is reified** as `:Bauteilgruppe`; no dedicated WIEDERVERWENDET edge.
- **Vocab nodes carry `:Vokabular`** super-label for taxonomy enumeration.
- Every Label has UNIQUE constraint on `id`.

# Appendix B — Constraints & indexes

- `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE` per Label.
- Range indexes on `:Bauteilgruppe(bauteil_label)`, `:Bauteilgruppe(material_label)`, `:Bauwerk(title)`, every measurement Label `(wert_values, einheit_norm)`.
- Full-text index `body_de` over `body_md` on all instance + vocab + measurement Labels.

# Appendix C — Coverage checklist

Verification table (in the final spec) showing every:

- folder under `_database/<entity>/` → destination Label
- legacy relation in `clean_confirmed_edges.csv` → one of the 5 edge types (via the legacy-mapping table in §3)
- YAML frontmatter field on legacy `fallstudie` / `projekt` / `bauobjekt` / `reuse_einsatz` / `datenpunkt` / `akteur_beteiligung` → destination property in §2

Items explicitly not preserved: `build_status` free-text values keep as A property but are not modeled as edges/relations; legacy `belongs_to_fallstudie` / `belongs_to_projekt` edges are dropped (no target Label).

# Appendix D — Renamings & taxonomy fixes

- Legacy `fallstudie/<id>/` + `projekt/<id>/` + `bauobjekt/<id>/` records sharing an id → merged into one `:Bauwerk` node.
- Legacy `reuse_einsatz/<id>/` → `:Bauteilgruppe` node.
- New vocab `:Bauteilgruppentyp` (`wiederverwendet`, `original`, `hybrid`).
- New vocab `:Einheit`.
- `:Tragwerkstyp` axis split — material-typed values kept; reuse-typed values (`wiederverwendetes_Tragwerk`, `demontierbares_Tragwerk`) lifted to `:Bauteilgruppentyp`.
- `Moebelsepearat` → `Moebel_separat`.
- `ort/Scwheiz` → `ort/Schweiz`.
- Bauteiltyp drop-and-remap from [SCHEMA.md §5](_database/_system/SCHEMA.md) (already applied).
- Material drop-and-merge from [SCHEMA.md §6](_database/_system/SCHEMA.md) (already applied).

---

## Out of scope (this plan)

- Writing the export script.
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.
