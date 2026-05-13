# Neo4j Building Migration Template

**Purpose:** Convert one old markdown case file into a clean, Neo4j-near migration format.

**Use case:** The user will provide 5 old building/case files at a time. For each old file, produce one completed version of this template.

---

## 0. Non-negotiable migration rules

### 0.1 Central node

Use `Projekt` as the central node.

Do **not** create `Fallbeispiel`.

```text
Old file / case study  ->  Projekt
Project / intervention ->  Projekt
Physical building      ->  Bauwerk
Specific reused item   ->  Bauteilgruppe
```

### 0.2 `Bauteilgruppe` meaning

`Bauteilgruppe` is the specific reuse occurrence, not merely a category.

Examples:

```text
20.35 t reused steel profiles at 55 Great Suffolk Street
self-harvested roof steel reused as stair structure at CRCLR
three apartment concrete units reused as SUPERLOCAL Expogebouw structure
```

### 0.3 Source of truth

Every imported object must be connected to `Quelle` using:

```cypher
-[:BELEGT_IN {datenqualitaet:"Belegt"}]->(:Quelle)
```

`datenqualitaet` is **not** a node. It is always a property on `BELEGT_IN`, and the value is always `"Belegt"`.

### 0.4 Prefer nodes over properties

If a value can connect multiple projects, make it a node.

Use nodes for:

```text
Stadt
Land
Status
Nutzung
Bauobjektklasse
Bauobjektrolle
Bauteiltyp
Bauteilebene
Material
Materialgruppe
Huerde
HuerdeKategorie
Akteurrolle
Akteurtyp
WiederverwendungsArt
Prozessphase
PruefungNachweis
Leistungsanforderung
Norm
Aufbereitungsverfahren
Rueckbauverfahren
Beschaffungsweg
Ressourcenquelle
Logistik
Methode
Verbindungstechnik
RechtlicheBedingung
Schadstoff
Wirtschaft
ZertifizierungBewertungssystem
Tragwerksprinzip
Bauweise
Bausystem
Funktionswechsel
```

Use properties only for:

```text
id
name
raw_name
raw_description
bewertung
flaeche_m2
menge_t
menge_m2
menge_m3
anzahl
gewicht_t
co2_einsparung_t
co2_reduktion_prozent
reuse_anteil_prozent
jahr_beginn
jahr_fertigstellung
baujahr
alte_funktion
neue_funktion
counts_as_direct_reuse
note
```

### 0.5 Removed fields

Do not import these old fields:

```text
entscheidung
warning_bestandserhalt
warning_moebel_dekoration
vertrauensgrad as a node
Datenqualitaet as a node
Kennwert as a node
Fallbeispiel as a node
```

Only keep `bewertung` as a scalar on `Projekt`.

---

## 1. Output contract

For each old file, produce the following sections in this exact order:

```text
1. Migration summary
2. Projekt node
3. Bauwerk nodes
4. Bauteilgruppe nodes
5. Akteur nodes
6. Controlled vocabulary nodes used
7. Relationships
8. Evidence links to Quelle
9. Neo4j-ready JSON
10. Validation checklist
11. Open issues / unclear fields
```

---

# TEMPLATE START

# 1. Migration summary

| Field | Value |
|---|---|
| Source file | `<original_filename.md>` |
| Source node id | `quelle_<slug>` |
| Main project id | `projekt_<slug>` |
| Main project name | `<project name>` |
| Number of Bauwerk nodes | `<n>` |
| Number of Bauteilgruppe nodes | `<n>` |
| Number of Akteur nodes | `<n>` |
| Main reuse type(s) | `<controlled WiederverwendungsArt values>` |
| Main material(s) | `<controlled Material values>` |
| Main hurdle category/categories | `<controlled HuerdeKategorie values>` |

---

# 2. Projekt node

Create exactly one `Projekt` node unless the source is explicitly a reuse chain with multiple independent project units.

## 2.1 Projekt properties

```yaml
label: Projekt
id: projekt_<slug>
name: <project/case name>
bewertung: <integer 1-5 or null>
flaeche_m2: <number or null>
reuse_anteil_prozent: <number or null>
co2_einsparung_t: <number or null>
co2_reduktion_prozent: <number or null>
jahr_beginn: <year or null>
jahr_fertigstellung: <year or null>
raw_summary: <short summary from source>
note: <important non-scalar context or source conflict note>
```

## 2.2 Projekt classification nodes

Use relationships, not properties.

```yaml
status:
  - <Status id/name>
nutzung:
  - <Nutzung id/name>
bauaufgabe_intervention:
  - <BauaufgabeIntervention id/name>
wiederverwendungsart:
  - <WiederverwendungsArt id/name>
methode:
  - <Methode id/name>
zertifizierung_bewertungssystem:
  - <ZertifizierungBewertungssystem id/name>
rechtliche_bedingung:
  - <RechtlicheBedingung id/name>
```

---

# 3. Bauwerk nodes

Create one `Bauwerk` node for every physical object that matters to the reuse logic.

Always create separate `Bauwerk` nodes for:

```text
receiver building
external donor building
same-site donor/receiver building
storage depot or intermediate warehouse, when relevant
infrastructure donor, when relevant
```

## 3.1 Bauwerk table

| id | name | adresse | baujahr | note |
|---|---|---|---:|---|
| `bauwerk_<slug>` | `<name>` | `<address or null>` | `<year or null>` | `<note>` |

## 3.2 Bauwerk classifications

| Bauwerk id | Bauobjektklasse | Bauobjektrolle | Stadt | Land | Nutzung | Status |
|---|---|---|---|---|---|---|
| `bauwerk_<slug>` | `Gebaeude` | `Empfaengerobjekt` | `stadt_<slug>` | `land_<slug>` | `<Nutzung>` | `<Status>` |

---

# 4. Bauteilgruppe nodes

Each relevant row in the old `BAUTEIL-INVENTAR` becomes one `Bauteilgruppe`.

A `Bauteilgruppe` is created only when it is a fixed building-related reuse occurrence or a relevant planned reuse occurrence.

Do not create `Bauteilgruppe` for loose furniture, decoration, or normal retention unless it is explicitly part of the direct reuse evaluation.

## 4.1 Bauteilgruppe table

| id | name | raw_name | alte_funktion | neue_funktion | counts_as_direct_reuse | scalar metrics | note |
|---|---|---|---|---|---|---|---|
| `btg_<projectslug>_<component>` | `<clear name>` | `<source wording>` | `<old function>` | `<new function>` | `true/false` | `menge_t:..., anzahl:..., co2_einsparung_t:...` | `<note>` |

## 4.2 Bauteilgruppe classifications

| Bauteilgruppe id | Bauteiltyp | Bauteilebene | Material | Materialgruppe | Tragwerksprinzip | WiederverwendungsArt | Status |
|---|---|---|---|---|---|---|---|
| `btg_<...>` | `Traeger; Stuetze` | `Bauteilgruppe` | `Stahl` | `Metall` | `Skeletttragwerk` | `Direkte_Wiederverwendung` | `Realisiert` |

## 4.3 Bauteilgruppe process / technical data

| Bauteilgruppe id | Prozessphase | Rueckbauverfahren | Aufbereitungsverfahren | Verbindungstechnik | PruefungNachweis | Leistungsanforderung | Norm | RechtlicheBedingung |
|---|---|---|---|---|---|---|---|---|
| `btg_<...>` | `Rueckbau; Pruefung; Wiedereinbau` | `<controlled>` | `<controlled>` | `<controlled>` | `<controlled>` | `<controlled>` | `<controlled>` | `<controlled>` |

## 4.4 Bauteilgruppe hurdles

| Bauteilgruppe id | Huerde | HuerdeKategorie |
|---|---|---|
| `btg_<...>` | `Technische_Freigabe` | `Technisch` |

## 4.5 Bauteilgruppe source/destination

| Bauteilgruppe id | AUS_BAUWERK | EINGEBAUT_IN | Ressourcenquelle | Beschaffungsweg | Logistik |
|---|---|---|---|---|---|
| `btg_<...>` | `bauwerk_<donor>` | `bauwerk_<receiver>` | `Donorgebaeude` | `Rueckbauprojekt` | `Transport; Zwischenlagerung` |

---

# 5. Akteur nodes

All organisations, people, offices, contractors, public bodies, suppliers, researchers, and institutions become `Akteur`.

Roles and types are nodes, not properties.

## 5.1 Akteur table

| id | name | raw_name | note |
|---|---|---|---|
| `akteur_<slug>` | `<normalised name>` | `<source wording>` | `<note>` |

## 5.2 Akteur classifications and participation

| Akteur id | Akteurtyp | Akteurrolle | beteiligt_an |
|---|---|---|---|
| `akteur_<slug>` | `Architekturbüro` | `Architektur` | `projekt_<slug>` |
| `akteur_<slug>` | `Ingenieurbüro` | `Tragwerksplanung` | `btg_<slug>` |

---

# 6. Controlled vocabulary nodes used

List only controlled nodes that are used in this transformed file.

## 6.1 Location

```yaml
Stadt:
  - id: stadt_<slug>
    name: <name>
Land:
  - id: land_<slug>
    name: <name>
```

## 6.2 Building classification

```yaml
Bauobjektklasse:
  - id: bok_<slug>
    name: <controlled value>
Bauobjektrolle:
  - id: bor_<slug>
    name: <controlled value>
```

## 6.3 Component / material classification

```yaml
Bauteiltyp:
  - id: bt_<slug>
    name: <controlled value>
Bauteilebene:
  - id: eb_<slug>
    name: <controlled value>
Material:
  - id: mat_<slug>
    name: <controlled value>
Materialgruppe:
  - id: matgrp_<slug>
    name: <controlled value>
Tragwerksprinzip:
  - id: tragwerk_<slug>
    name: <controlled value>
```

## 6.4 Reuse / process classification

```yaml
WiederverwendungsArt:
  - id: wva_<slug>
    name: <controlled value>
Status:
  - id: status_<slug>
    name: <controlled value>
Prozessphase:
  - id: phase_<slug>
    name: <controlled value>
Rueckbauverfahren:
  - id: rueckbau_<slug>
    name: <controlled value>
Aufbereitungsverfahren:
  - id: aufbereitung_<slug>
    name: <controlled value>
Beschaffungsweg:
  - id: beschaffung_<slug>
    name: <controlled value>
Ressourcenquelle:
  - id: ressource_<slug>
    name: <controlled value>
Logistik:
  - id: logistik_<slug>
    name: <controlled value>
Methode:
  - id: methode_<slug>
    name: <controlled value>
```

## 6.5 Technical / legal / hurdle classification

```yaml
PruefungNachweis:
  - id: pruefung_<slug>
    name: <controlled value>
Leistungsanforderung:
  - id: anf_<slug>
    name: <controlled value>
Norm:
  - id: norm_<slug>
    name: <controlled value>
RechtlicheBedingung:
  - id: recht_<slug>
    name: <controlled value>
Schadstoff:
  - id: schadstoff_<slug>
    name: <controlled value>
Huerde:
  - id: h_<slug>
    name: <controlled value>
HuerdeKategorie:
  - id: hk_<slug>
    name: <controlled value>
```

## 6.6 Actor classification

```yaml
Akteurrolle:
  - id: rolle_<slug>
    name: <controlled value>
Akteurtyp:
  - id: akttyp_<slug>
    name: <controlled value>
```

---

# 7. Relationships

Use only the final semantic relationships below.

## 7.1 Project / building / component relationships

```cypher
(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)
(:Projekt)-[:NUTZT_BAUWERK]->(:Bauwerk)
(:Bauteilgruppe)-[:AUS_BAUWERK]->(:Bauwerk)
(:Bauteilgruppe)-[:EINGEBAUT_IN]->(:Bauwerk)
(:Bauteilgruppe)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette)
```

## 7.2 Classification relationships

```cypher
(:Projekt)-[:HAT_STATUS]->(:Status)
(:Projekt)-[:HAT_NUTZUNG]->(:Nutzung)
(:Bauwerk)-[:HAT_STATUS]->(:Status)
(:Bauwerk)-[:HAT_NUTZUNG]->(:Nutzung)
(:Bauwerk)-[:HAT_BAUOBJEKTKLASSE]->(:Bauobjektklasse)
(:Bauwerk)-[:HAT_BAUOBJEKTROLLE]->(:Bauobjektrolle)
(:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(:Bauteiltyp)
(:Bauteilgruppe)-[:HAT_BAUTEILEBENE]->(:Bauteilebene)
(:Bauteilgruppe)-[:HAT_TRAGWERKSPRINZIP]->(:Tragwerksprinzip)
(:Bauteilgruppe)-[:HAT_BAUWEISE]->(:Bauweise)
(:Bauteilgruppe)-[:HAT_BAUSYSTEM]->(:Bausystem)
(:Bauteilgruppe)-[:HAT_STATUS]->(:Status)
(:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSART]->(:WiederverwendungsArt)
(:Bauteilgruppe)-[:HAT_FUNKTIONSWECHSEL]->(:Funktionswechsel)
```

## 7.3 Material relationships

```cypher
(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material)
(:Material)-[:HAT_MATERIALGRUPPE]->(:Materialgruppe)
```

## 7.4 Process relationships

```cypher
(:Bauteilgruppe)-[:HAT_PROZESSPHASE]->(:Prozessphase)
(:Bauteilgruppe)-[:HAT_METHODE]->(:Methode)
(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren)
(:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)
(:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg)
(:Bauteilgruppe)-[:HAT_RESSOURCENQUELLE]->(:Ressourcenquelle)
(:Bauteilgruppe)-[:HAT_LOGISTIK]->(:Logistik)
(:Bauteilgruppe)-[:HAT_VERBINDUNGSTECHNIK]->(:Verbindungstechnik)
```

## 7.5 Technical / legal relationships

```cypher
(:Bauteilgruppe)-[:HAT_PRUEFUNG]->(:PruefungNachweis)
(:Bauteilgruppe)-[:HAT_LEISTUNGSANFORDERUNG]->(:Leistungsanforderung)
(:Bauteilgruppe)-[:REFERENZIERT_NORM]->(:Norm)
(:Bauteilgruppe)-[:HAT_RECHTLICHE_BEDINGUNG]->(:RechtlicheBedingung)
(:Bauteilgruppe)-[:HAT_SCHADSTOFF]->(:Schadstoff)
(:Bauteilgruppe)-[:HAT_ZERTIFIZIERUNG]->(:ZertifizierungBewertungssystem)
(:Bauteilgruppe)-[:HAT_WIRTSCHAFTSASPEKT]->(:Wirtschaft)
```

## 7.6 Hurdle relationships

```cypher
(:Projekt)-[:HAT_HUERDE]->(:Huerde)
(:Bauteilgruppe)-[:HAT_HUERDE]->(:Huerde)
(:Huerde)-[:HAT_HUERDEKATEGORIE]->(:HuerdeKategorie)
```

## 7.7 Actor relationships

```cypher
(:Akteur)-[:BETEILIGT_AN]->(:Projekt)
(:Akteur)-[:BETEILIGT_AN]->(:Bauteilgruppe)
(:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
(:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp)
```

## 7.8 Location relationships

```cypher
(:Projekt)-[:LIEGT_IN_STADT]->(:Stadt)
(:Bauwerk)-[:LIEGT_IN_STADT]->(:Stadt)
(:Stadt)-[:LIEGT_IN_LAND]->(:Land)
```

## 7.9 Evidence relationships

```cypher
(:Projekt)-[:BELEGT_IN {datenqualitaet:"Belegt"}]->(:Quelle)
(:Bauwerk)-[:BELEGT_IN {datenqualitaet:"Belegt"}]->(:Quelle)
(:Bauteilgruppe)-[:BELEGT_IN {datenqualitaet:"Belegt"}]->(:Quelle)
(:Akteur)-[:BELEGT_IN {datenqualitaet:"Belegt"}]->(:Quelle)
```

---

# 8. Evidence links to Quelle

Create one `Quelle` node for the old source file.

```yaml
Quelle:
  id: quelle_<sourcefile_slug>
  name: <source filename>
  quelltyp: case_markdown
```

Every major imported node must have a `BELEGT_IN` relationship to this `Quelle`.

| from_label | from_id | relationship | to_label | to_id | relationship_properties |
|---|---|---|---|---|---|
| Projekt | `projekt_<slug>` | BELEGT_IN | Quelle | `quelle_<slug>` | `{datenqualitaet:"Belegt"}` |
| Bauwerk | `bauwerk_<slug>` | BELEGT_IN | Quelle | `quelle_<slug>` | `{datenqualitaet:"Belegt"}` |
| Bauteilgruppe | `btg_<slug>` | BELEGT_IN | Quelle | `quelle_<slug>` | `{datenqualitaet:"Belegt"}` |
| Akteur | `akteur_<slug>` | BELEGT_IN | Quelle | `quelle_<slug>` | `{datenqualitaet:"Belegt"}` |

---

# 9. Neo4j-ready JSON

After the human-readable sections, produce this exact JSON shape.

```json
{
  "source_file": "<original_filename.md>",
  "nodes": [
    {
      "label": "Projekt",
      "id": "projekt_<slug>",
      "properties": {
        "name": "<name>",
        "bewertung": 4,
        "flaeche_m2": null,
        "note": "<note>"
      }
    },
    {
      "label": "Bauwerk",
      "id": "bauwerk_<slug>",
      "properties": {
        "name": "<name>",
        "adresse": null,
        "baujahr": null,
        "note": null
      }
    },
    {
      "label": "Bauteilgruppe",
      "id": "btg_<slug>",
      "properties": {
        "name": "<name>",
        "raw_name": "<raw source wording>",
        "alte_funktion": "<old function>",
        "neue_funktion": "<new function>",
        "counts_as_direct_reuse": true,
        "menge_t": null,
        "menge_m2": null,
        "menge_m3": null,
        "anzahl": null,
        "co2_einsparung_t": null,
        "note": null
      }
    }
  ],
  "relationships": [
    {
      "from": "projekt_<slug>",
      "type": "HAT_BAUTEILGRUPPE",
      "to": "btg_<slug>",
      "properties": {}
    },
    {
      "from": "btg_<slug>",
      "type": "HAT_BAUTEILTYP",
      "to": "bt_<slug>",
      "properties": {}
    },
    {
      "from": "btg_<slug>",
      "type": "BELEGT_IN",
      "to": "quelle_<slug>",
      "properties": {
        "datenqualitaet": "Belegt"
      }
    }
  ],
  "validation": {
    "fallbeispiel_removed": true,
    "datenqualitaet_only_on_belegt_in": true,
    "kennwert_nodes_absent": true,
    "stadt_land_are_nodes": true,
    "bauobjektklasse_rolle_are_nodes": true,
    "akteurrollen_are_nodes": true,
    "bauteilgruppe_is_occurrence": true,
    "major_nodes_have_source_link": true
  }
}
```

---

# 10. Validation checklist

Before finalising each transformed file, check:

```text
[ ] No Fallbeispiel node exists.
[ ] Projekt is the central node.
[ ] Bewertung exists only as Projekt.bewertung.
[ ] Entscheidung was not imported.
[ ] warning_bestandserhalt was not imported.
[ ] warning_moebel_dekoration was not imported.
[ ] Datenqualitaet is not a node.
[ ] Every BELEGT_IN relationship has {datenqualitaet:"Belegt"}.
[ ] Kennwert is not a node.
[ ] Numeric values are stored as properties on the most relevant node.
[ ] Stadt and Land are nodes, not properties.
[ ] Bauobjektklasse and Bauobjektrolle are nodes, not properties.
[ ] Akteurrolle and Akteurtyp are nodes, not properties.
[ ] Bauteiltyp is unchanged and used as a controlled node.
[ ] Bauteilgruppe is a reuse occurrence, not a generic type.
[ ] Each Bauteilgruppe connects to at least Bauteiltyp, Material, and Quelle.
[ ] Each Material connects to Materialgruppe.
[ ] Each Huerde connects to HuerdeKategorie.
[ ] Major nodes connect to Quelle.
[ ] No loose furniture/decorative reuse is imported as Bauteilgruppe unless explicitly counted as fixed building reuse.
[ ] Normal Bestandserhalt is not counted as direct reuse.
```

---

# 11. Open issues / unclear fields

Use this section for missing or conflicting information. Do not invent values.

| Issue | Affected node | Field / relationship | Treatment |
|---|---|---|---|
| `<issue>` | `<node id>` | `<field>` | `<left null / note added / range used>` |

---

# TEMPLATE END

---

## Batch workflow for 5 files

When processing 5 files at a time, produce:

```text
1. One completed template per source file.
2. One batch summary table.
3. One shared controlled-node merge list.
4. One issue list for unresolved conflicts.
```

### Batch summary table

| Source file | Projekt id | Bauwerk count | Bauteilgruppe count | Akteur count | Main Material nodes | Main Huerde nodes | Ready for import? |
|---|---|---:|---:|---:|---|---|---|
| `<file.md>` | `projekt_<slug>` | `<n>` | `<n>` | `<n>` | `<materials>` | `<hurdles>` | `yes/no` |

### Shared controlled-node merge list

Use this to avoid duplicate controlled vocabulary nodes across the 5 files.

```yaml
Material:
  - mat_stahl: Stahl
  - mat_stahlbeton: Stahlbeton
Materialgruppe:
  - matgrp_metall: Metall
  - matgrp_mineralisch: Mineralisch
Bauteiltyp:
  - bt_traeger: Traeger
  - bt_stuetze: Stuetze
Huerde:
  - h_technische_freigabe: Technische_Freigabe
HuerdeKategorie:
  - hk_technisch: Technisch
```

