# Neo4j Batch Transformation Template v1

Use this template to transform old building case-study markdown files into the final Neo4j-ready structure. It is optimized for batches of **5 files at a time** and for token-efficient output.

---

## 0. Core migration rules

1. **Do not create `Fallbeispiel`.**
   - `Projekt` is the central case node.

2. **Keep `Bauwerk`.**
   - `Bauwerk` is the physical object: donor building, receiver building, same-site building, infrastructure, pavilion, depot, reuse centre, etc.

3. **Use `Bauteilgruppe` as the central reuse occurrence node.**
   - A `Bauteilgruppe` is not a generic category.
   - It is the specific reused component group in the project.
   - Example: reused steel beams, reused façade bricks, reused concrete room units, reused windows.

4. **Prefer nodes over properties when the value can connect multiple examples.**
   - Use nodes for city, country, material, material group, component type, actor role, actor type, building role, building class, hurdle, hurdle category, status, use, norm, test, requirement, reuse type.

5. **Use properties only for scalar or case-specific values.**
   - Examples: `bewertung`, `flaeche_m2`, `menge_t`, `menge_m2`, `menge_m3`, `anzahl`, `co2_einsparung_t`, `reuse_anteil_prozent`, `jahr_fertigstellung`, `raw_name`, `alte_funktion`, `neue_funktion`, `note`.

6. **`Datenqualitaet` is not a node.**
   - It appears only as a relationship property on `BELEGT_IN`.
   - Use always: `{datenqualitaet:"Belegt"}`.

7. **`Kennwert` is not a node.**
   - Metrics are properties on the relevant node.
   - Project area goes on `Projekt`.
   - Component weight, quantity, CO₂ saving, volume, etc. go on `Bauteilgruppe`.

8. **`Quelle` is the source-of-truth node.**
   - Every imported file becomes one `Quelle` node.
   - Major nodes must connect to `Quelle` with `BELEGT_IN`.

9. **Remove / do not import these fields as nodes or properties:**
   - `entscheidung`
   - `warning_bestandserhalt`
   - `warning_moebel_dekoration`
   - `vertrauensgrad`
   - `quellenlage` except as `note` if important

10. **Keep only `bewertung` as the reuse score scalar.**

---

## 1. Token-friendly output format

For each batch of 5 old files, produce one answer using this compact format:

```text
BATCH: <batch_name_or_number>
SOURCE_FILES: [<filename_1>, <filename_2>, ...]

CONTROLLED_TERMS_NEW:
  <Label>|<id>|<name>|parent=<optional_parent_id>

PROJECTS:
  P|<project_id>|<project_name>|bewertung=<int>|<scalar_props>

BUILDINGS:
  BW|<bauwerk_id>|<bauwerk_name>|<scalar_props>

COMPONENT_GROUPS:
  BG|<bauteilgruppe_id>|<name>|raw=<raw_name>|old=<alte_funktion>|new=<neue_funktion>|direct=<true/false>|<scalar_props>

ACTORS:
  A|<akteur_id>|<name>|raw=<optional_raw_name>

SOURCES:
  Q|<quelle_id>|<filename>|type=case_markdown

EDGES:
  E|<start_id>|<RELATIONSHIP_TYPE>|<end_id>|<optional_props>

NOTES:
  - <short issue, uncertainty, conflict, or mapping decision>
```

This format is close to Neo4j because every `E|...` line becomes one relationship.

---

## 2. Required node labels and prefixes

Use stable IDs with these prefixes:

| Label | Prefix | Meaning |
|---|---|---|
| Projekt | `p_` | central project / reuse case |
| Bauwerk | `bw_` | physical building/object |
| Bauteilgruppe | `bg_` | specific reused component group / reuse occurrence |
| Akteur | `a_` | person, company, institution, public body |
| Quelle | `q_` | source markdown file |
| Stadt | `ct_` | city |
| Land | `co_` | country |
| Bauteiltyp | `bt_` | controlled component type |
| Bauteilebene | `be_` | controlled component level |
| Material | `mat_` | controlled material |
| Materialgruppe | `mg_` | material family |
| Huerde | `h_` | controlled barrier |
| HuerdeKategorie | `hk_` | barrier category |
| Akteurrolle | `ar_` | actor role |
| Akteurtyp | `at_` | actor type |
| Bauobjektklasse | `bok_` | building object class |
| Bauobjektrolle | `bor_` | donor/receiver/context role |
| Status | `st_` | project/component status |
| Nutzung | `nu_` | use/programme |
| WiederverwendungsArt | `wva_` | reuse type |
| Prozessphase | `ph_` | process phase |
| PruefungNachweis | `pn_` | test/proof |
| Leistungsanforderung | `la_` | requirement |
| Norm | `norm_` | standard/norm |
| Aufbereitungsverfahren | `av_` | processing/refurbishment method |
| Rueckbauverfahren | `rv_` | deconstruction method |
| Beschaffungsweg | `bc_` | procurement route |
| Ressourcenquelle | `rq_` | resource source |
| Logistik | `lg_` | logistics category |
| Methode | `me_` | method |
| Verbindungstechnik | `vt_` | connection technique |
| RechtlicheBedingung | `rb_` | legal condition |
| Schadstoff | `sf_` | contaminant |
| Wirtschaft | `wi_` | economic aspect |
| ZertifizierungBewertungssystem | `zb_` | certification/rating system |
| Tragwerksprinzip | `tp_` | structural principle |
| Bauweise | `bwz_` | construction method |
| Bausystem | `bs_` | building system |
| Funktionswechsel | `fw_` | functional change |

---

## 3. Required relationship types

Use only these relationship types unless a new one is absolutely necessary:

### Project / building / component

```text
HAT_BAUTEILGRUPPE
NUTZT_BAUWERK
AUS_BAUWERK
EINGEBAUT_IN
TEIL_VON_KETTE
```

### Classification

```text
HAT_BAUTEILTYP
HAT_BAUTEILEBENE
HAT_BAUOBJEKTKLASSE
HAT_BAUOBJEKTROLLE
HAT_TRAGWERKSPRINZIP
HAT_BAUWEISE
HAT_BAUSYSTEM
HAT_STATUS
HAT_NUTZUNG
HAT_WIEDERVERWENDUNGSART
HAT_FUNKTIONSWECHSEL
```

### Material

```text
NUTZT_MATERIAL
HAT_MATERIALGRUPPE
```

### Process

```text
HAT_PROZESSPHASE
HAT_METHODE
HAT_RUECKBAUVERFAHREN
HAT_AUFBEREITUNG
HAT_BESCHAFFUNGSWEG
HAT_RESSOURCENQUELLE
HAT_LOGISTIK
HAT_VERBINDUNGSTECHNIK
```

### Technical / legal / economic

```text
HAT_PRUEFUNG
HAT_LEISTUNGSANFORDERUNG
REFERENZIERT_NORM
HAT_RECHTLICHE_BEDINGUNG
HAT_SCHADSTOFF
HAT_ZERTIFIZIERUNG
HAT_WIRTSCHAFTSASPEKT
```

### Barriers

```text
HAT_HUERDE
HAT_HUERDEKATEGORIE
```

### Actors

```text
BETEILIGT_AN
HAT_AKTEURROLLE
HAT_AKTEURTYP
```

### Location

```text
LIEGT_IN_STADT
LIEGT_IN_LAND
```

### Evidence

```text
BELEGT_IN
```

`BELEGT_IN` must always have:

```text
{datenqualitaet:"Belegt"}
```

---

## 4. Compact node line syntax

### Projekt

```text
P|p_<slug>|<name>|bewertung=<1-5>|flaeche_m2=<number>|jahr_fertigstellung=<year>|co2_einsparung_t=<number>|reuse_anteil_prozent=<number>|note=<short_note>
```

Only include properties that exist.

### Bauwerk

```text
BW|bw_<slug>|<name>|adresse=<text>|baujahr=<year>|note=<short_note>
```

Do not include city, country, building class, role, status, or use as properties. Use edges to nodes.

### Bauteilgruppe

```text
BG|bg_<project_slug>_<component_slug>|<name>|raw=<source_term>|old=<old_function>|new=<new_function>|direct=<true/false>|menge_t=<number>|menge_m2=<number>|menge_m3=<number>|anzahl=<number>|co2_einsparung_t=<number>|note=<short_note>
```

Only include scalar properties that exist.

### Akteur

```text
A|a_<slug>|<name>|raw=<optional_raw_name>
```

### Quelle

```text
Q|q_<file_slug>|<filename>|type=case_markdown
```

### Controlled term

```text
T|<Label>|<id>|<name>
```

Example:

```text
T|Material|mat_stahl|Stahl
T|Materialgruppe|mg_metall|Metall
T|Bauteiltyp|bt_traeger|Traeger
T|Huerde|h_technische_freigabe|Technische_Freigabe
T|HuerdeKategorie|hk_technisch|Technisch
```

### Edge

```text
E|<start_id>|<RELATIONSHIP_TYPE>|<end_id>|<props_optional>
```

Example:

```text
E|bg_55gss_steel_core|NUTZT_MATERIAL|mat_stahl
E|mat_stahl|HAT_MATERIALGRUPPE|mg_metall
E|bg_55gss_steel_core|BELEGT_IN|q_55_great_suffolk_street|datenqualitaet=Belegt
```

---

## 5. Mandatory edges per node type

### Every `Projekt`

Must have at least:

```text
E|p_*|HAT_BAUTEILGRUPPE|bg_*
E|p_*|BELEGT_IN|q_*|datenqualitaet=Belegt
```

Usually also:

```text
E|p_*|NUTZT_BAUWERK|bw_*
E|p_*|HAT_STATUS|st_*
E|p_*|HAT_NUTZUNG|nu_*
```

### Every `Bauwerk`

Must have at least:

```text
E|bw_*|HAT_BAUOBJEKTKLASSE|bok_*
E|bw_*|HAT_BAUOBJEKTROLLE|bor_*
E|bw_*|BELEGT_IN|q_*|datenqualitaet=Belegt
```

Usually also:

```text
E|bw_*|LIEGT_IN_STADT|ct_*
E|ct_*|LIEGT_IN_LAND|co_*
```

### Every `Bauteilgruppe`

Must have at least:

```text
E|bg_*|HAT_BAUTEILTYP|bt_*
E|bg_*|NUTZT_MATERIAL|mat_*
E|bg_*|BELEGT_IN|q_*|datenqualitaet=Belegt
```

Usually also:

```text
E|bg_*|AUS_BAUWERK|bw_*
E|bg_*|EINGEBAUT_IN|bw_*
E|bg_*|HAT_WIEDERVERWENDUNGSART|wva_*
E|bg_*|HAT_STATUS|st_*
```

### Every `Akteur`

Must have at least:

```text
E|a_*|BETEILIGT_AN|p_* or bg_*
E|a_*|HAT_AKTEURROLLE|ar_*
```

Usually also:

```text
E|a_*|HAT_AKTEURTYP|at_*
E|a_*|BELEGT_IN|q_*|datenqualitaet=Belegt
```

---

## 6. Markdown-to-template mapping

### §1 Einordnung

| Old field | New target |
|---|---|
| Entscheidung | do not import |
| Bewertung | `Projekt.bewertung` |
| Begründung | `Projekt.note` if short and important |
| Vertrauensgrad | do not import |
| Warnung Bestandserhalt | do not import |
| Warnung Möbel/Dekoration | do not import |
| Projektstatus | `Projekt -[:HAT_STATUS]-> Status` |

### §2 Entitäten-Mapping

| Old entity | New target |
|---|---|
| Fallstudie | `Projekt` |
| Projekt | `Projekt` |
| Gebäude / Bauobjekt | `Bauwerk` |
| Ort | `Stadt` + `Land` |
| People / Akteur | `Akteur` + `Akteurrolle` + `Akteurtyp` |
| Bauteil | `Bauteilgruppe` + `Bauteiltyp` |
| Material | `Material` + `Materialgruppe` |
| Reuse-Strategie | `WiederverwendungsArt` / `Methode` |
| Abbruchmethode | `Rueckbauverfahren` |
| Aufbereitungsmethode | `Aufbereitungsverfahren` |
| Prüfung | `PruefungNachweis` |
| Leistungsanforderung | `Leistungsanforderung` |
| Norm | `Norm` |
| Recht | `RechtlicheBedingung` |
| Schadstoff | `Schadstoff` |
| Wirtschaft | `Wirtschaft` |
| Logistik | `Logistik` |
| Quelle | `Quelle` via `BELEGT_IN` |

### §3 Fallstudie

| Old field | New target |
|---|---|
| Name | `Projekt.name` |
| Ort | `Stadt` + `Land` |
| Gebäude | `Bauwerk` |
| Beteiligte | `Akteur` |
| Architekt | `Akteur` + role `Architektur` |
| Tragwerksplaner | `Akteur` + role `Tragwerksplanung` |
| Bauherr | `Akteur` + role `Bauherr_Auftraggeber` |
| Zeitraum | `Projekt.jahr_beginn` / `Projekt.jahr_fertigstellung` |
| Ursprüngliche Nutzung | `Nutzung` or `Bauteilgruppe.old` |
| Neue Nutzung | `Nutzung` or `Bauteilgruppe.new` |
| Fläche | `Projekt.flaeche_m2` or `Bauwerk.flaeche_m2` |

### §5 Bauteil-Inventar

Each row becomes one `Bauteilgruppe`.

| Inventory column | New target |
|---|---|
| Bauteil | `BG.raw` + `HAT_BAUTEILTYP` |
| Material | `NUTZT_MATERIAL` |
| Herkunft | `AUS_BAUWERK` or `HAT_RESSOURCENQUELLE` |
| alte Funktion | `BG.old` |
| neue Funktion | `BG.new` |
| Menge/Umfang | scalar properties on `BG` |
| tragend? | `HAT_TRAGWERKSPRINZIP` or note |
| räumlich? | `HAT_BAUTEILEBENE` or note |
| Hülle? | `HAT_BAUTEILTYP` e.g. Fassade/Fenster/Dach |
| technisch? | `HAT_BAUTEILTYP` = Technik |
| Aufbereitung | `HAT_AUFBEREITUNG` |
| Verbindung | `HAT_VERBINDUNGSTECHNIK` |
| Prüfung | `HAT_PRUEFUNG` |
| Leistungsanforderung | `HAT_LEISTUNGSANFORDERUNG` |
| Norm/Recht | `REFERENZIERT_NORM` / `HAT_RECHTLICHE_BEDINGUNG` |
| Hürde | `HAT_HUERDE` |
| Quelle | `BELEGT_IN` |
| unbekannt | `note` only if important |

---

## 7. Controlled parent mappings

### Materialgruppe

```text
Metall: Stahl, Aluminium, Gusseisen
Mineralisch: Beton, Stahlbeton, Ziegel, Keramik, Naturstein, Glas, Lehm, Recyclingbeton
Biobasiert: Holz, Stroh
Kunststoff: Kunststoff
Daemmstoff: Daemmstoff
```

### HuerdeKategorie

```text
Technisch: Technische_Freigabe, Anschlussproblem, Kompatibilitaetsproblem, Toleranzen, Bruch_Beschaedigungsrisiko, Materialqualitaet_Unklar, Dauerhaftigkeit_Restlebensdauer, Witterung_Feuchte
Rechtlich: Bauproduktstatus, Gewaehrleistung, Haftung, Ausschreibungsproblem
Wirtschaftlich: Aufbereitungsaufwand, Preisbildung, Kostenvergleich, Restwert
Logistisch: Fehlende_Lagerflaeche, Terminunsicherheit, Verfuegbarkeitsproblem, Mengenunsicherheit
Planerisch: Entwurfsbindung, Fehlende_Standardisierung, Form_Follows_Availability
Daten_Evidenz: Datenluecke, Fehlende_Datenstandards, Zustand_Unklar
Sozial_Organisatorisch: Akzeptanzproblem, Nutzerbetrieb, Koordinationsaufwand
Umwelt_Gesundheit: Schadstoffbelastung, Hygieneanforderung
```

### Bauobjektrolle

```text
Donorobjekt
Empfaengerobjekt
Bestandsobjekt
Same_Site_Donor_Receiver
Zwischenlager
Referenzobjekt
```

### Bauobjektklasse

```text
Gebaeude
Gebaeudeteil
Infrastruktur
Innenausbau
Pavillon
Quartier_Areal
Reuse_Centre
Depot_Lager
```

---

## 8. Output validation checklist

Before returning a converted batch, check:

```text
[ ] No Fallbeispiel nodes.
[ ] Projekt is the central node.
[ ] Every project has at least one Bauteilgruppe.
[ ] Every Bauteilgruppe has Bauteiltyp, Material, and Quelle.
[ ] Every Bauwerk has Bauobjektklasse, Bauobjektrolle, and Quelle.
[ ] Stadt and Land are nodes, not properties.
[ ] Bauobjektklasse and Bauobjektrolle are nodes, not properties.
[ ] Akteurrolle and Akteurtyp are nodes, not properties.
[ ] Datenqualitaet appears only on BELEGT_IN and is always Belegt.
[ ] Kennwerte are properties, not nodes.
[ ] Entscheidung and warnings are not imported.
[ ] Bewertung is kept on Projekt.
[ ] Huerde connects to HuerdeKategorie.
[ ] Material connects to Materialgruppe.
[ ] Controlled values are reused when possible.
[ ] New controlled terms are listed under CONTROLLED_TERMS_NEW.
```

---

## 9. Empty-value rule

Do not output unknown empty fields.

Bad:

```text
flaeche_m2=unknown|co2_einsparung_t=unknown
```

Good:

```text
note=Fläche und CO2 nicht belegt
```

If an unknown value does not matter for graph structure, omit it entirely.

---

## 10. Batch response skeleton

Use this exact skeleton when transforming files:

```text
BATCH: <number_or_name>
SOURCE_FILES: [file1.md, file2.md, file3.md, file4.md, file5.md]

CONTROLLED_TERMS_NEW:
  T|<Label>|<id>|<name>

PROJECTS:
  P|<id>|<name>|bewertung=<n>|<scalars>

BUILDINGS:
  BW|<id>|<name>|<scalars>

COMPONENT_GROUPS:
  BG|<id>|<name>|raw=<raw>|old=<old>|new=<new>|direct=<true/false>|<scalars>

ACTORS:
  A|<id>|<name>

SOURCES:
  Q|<id>|<filename>|type=case_markdown

EDGES:
  E|<start_id>|<RELATIONSHIP_TYPE>|<end_id>|<props_if_any>

NOTES:
  - <short notes only>
```
