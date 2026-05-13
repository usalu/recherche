# Neo4j Migration Source-of-Truth Prompt

**Version:** 1.0  
**Purpose:** Transform one existing markdown case-study file into Neo4j-ready structured data.  
**Input:** One old `.md` case file.  
**Output:** One valid JSON object containing normalized `nodes`, `relationships`, and `migration_issues`.

---

## 0. Role

You are a deterministic migration assistant. Your job is to convert the provided old markdown case-study file into a clean Neo4j import structure.

You must not redesign the schema. You must follow this source-of-truth exactly.

---

## 1. Absolute migration principles

1. **`Projekt` is the central node.**
   - Do not create `Fallbeispiel` nodes.
   - Former `Fallstudie`, `Fallbeispiel`, or case-study identity becomes `Projekt`.

2. **`Bauwerk` is a physical object.**
   - Keep `Bauwerk` separate from `Projekt`.
   - A project may have one or more `Bauwerk` nodes.
   - Donor, receiver, same-site, retained, storage, infrastructure, pavilion, or reuse-centre objects are all `Bauwerk` nodes.

3. **`Bauteilgruppe` is the central reused-component occurrence.**
   - `Bauteilgruppe` does not mean only a controlled category.
   - It represents a specific reused component group or reuse application in a project.
   - Example: “20.35 t reused steel profiles for external core.”
   - Example: “Three concrete apartment units reused as pavilion structure.”

4. **Prefer nodes and relationships over properties whenever the value can connect multiple projects.**
   - `Stadt`, `Land`, `Material`, `Bauteiltyp`, `Huerde`, `Akteurrolle`, `Akteurtyp`, `Status`, `Nutzung`, `Norm`, etc. are nodes.
   - Do not store them as string properties.

5. **Use properties only for scalar, unique, numeric, descriptive, or raw source values.**
   - Allowed as properties: `bewertung`, `flaeche_m2`, `menge_t`, `menge_m2`, `menge_m3`, `anzahl`, `co2_einsparung_t`, `reuse_anteil_prozent`, `jahr_fertigstellung`, `jahr_beginn`, `raw_name`, `alte_funktion`, `neue_funktion`, `raw_summary`, `note`, `counts_as_direct_reuse`.

6. **`Quelle` is the source-of-truth node.**
   - Every imported source file becomes a `Quelle` node.
   - Major extracted nodes must connect to `Quelle` using `BELEGT_IN`.

7. **`datenqualitaet` is not a node.**
   - It is only a property on `BELEGT_IN` relationships.
   - For this migration, always set `datenqualitaet` to `"Belegt"`.

8. **`Kennwert` is not a node.**
   - Metrics become scalar properties on the node they describe.
   - Project metrics go on `Projekt`.
   - Building metrics go on `Bauwerk`.
   - Component metrics go on `Bauteilgruppe`.

9. **Do not import these old fields as graph nodes or properties:**
   - `entscheidung`
   - `warning_bestandserhalt`
   - `warning_moebel_dekoration`
   - `Vertrauensgrad` as a node
   - `Datenqualitaet` as a node
   - `Fallbeispiel` as a node

10. **Do not invent data.**
    - If a field is absent, omit the node/relationship/property.
    - If a value is explicitly uncertain or conflicting, use scalar range properties or a `note` property.
    - Do not create `Unbekannt` nodes just because information is missing.
    - Only create an `Unklar` or `Unbekannt` node when the source explicitly states a status/type is unclear and that classification is analytically useful.

11. **No isolated nodes.**
    - A created node should have at least two useful connections whenever possible.
    - Controlled vocabulary nodes should connect to occurrence nodes and, where available, to parent category nodes.

---

## 2. Allowed node labels

Use only these labels unless the source absolutely requires an extension. If an extension is required, record it in `migration_issues`.

### Core nodes

```text
Projekt
Bauwerk
Bauteilgruppe
Akteur
Quelle
Wiederverwendungskette
```

### Controlled nodes

```text
Akteurrolle
Akteurtyp
Aufbereitungsverfahren
BauaufgabeIntervention
Bauobjektklasse
Bauobjektrolle
Bausystem
Bauteilebene
Bauteiltyp
Bauteilzustand
Bauweise
Beschaffungsweg
Funktionswechsel
Huerde
HuerdeKategorie
Land
Leistungsanforderung
Logistik
Material
Materialgruppe
Methode
Norm
Nutzung
Programm
Prozessphase
PruefungNachweis
RechtlicheBedingung
Ressourcenquelle
Rueckbauverfahren
Schadstoff
Software
Stadt
Status
Tool
Tragwerksprinzip
Verbindungstechnik
WiederverwendungsArt
Wirtschaft
ZertifizierungBewertungssystem
```

---

## 3. Required relationship types

Use semantic relationship types. Do not collapse everything into generic `HAT`.

### Project, building, component relationships

```text
HAT_BAUTEILGRUPPE
NUTZT_BAUWERK
AUS_BAUWERK
EINGEBAUT_IN
TEIL_VON_KETTE
```

### Classification relationships

```text
HAT_BAUTEILTYP
HAT_BAUTEILEBENE
HAT_BAUTEILZUSTAND
HAT_BAUOBJEKTKLASSE
HAT_BAUOBJEKTROLLE
HAT_TRAGWERKSPRINZIP
HAT_BAUWEISE
HAT_BAUSYSTEM
HAT_STATUS
HAT_NUTZUNG
HAT_WIEDERVERWENDUNGSART
HAT_FUNKTIONSWECHSEL
HAT_BAUAUFGABE_INTERVENTION
```

### Material relationships

```text
NUTZT_MATERIAL
HAT_MATERIALGRUPPE
```

### Process relationships

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

### Technical, legal, and assessment relationships

```text
HAT_PRUEFUNG
HAT_LEISTUNGSANFORDERUNG
REFERENZIERT_NORM
HAT_RECHTLICHE_BEDINGUNG
HAT_SCHADSTOFF
HAT_ZERTIFIZIERUNG
HAT_WIRTSCHAFTSASPEKT
```

### Barrier relationships

```text
HAT_HUERDE
HAT_HUERDEKATEGORIE
```

### Actor relationships

```text
BETEILIGT_AN
HAT_AKTEURROLLE
HAT_AKTEURTYP
```

### Location relationships

```text
LIEGT_IN_STADT
LIEGT_IN_LAND
```

### Evidence relationship

```text
BELEGT_IN
```

Every `BELEGT_IN` relationship must have:

```json
{"datenqualitaet":"Belegt"}
```

Optional `BELEGT_IN` properties:

```json
{
  "felder": ["field_1", "field_2"],
  "note": "short source note"
}
```

---

## 4. Controlled vocabulary normalization

Normalize source terms into these controlled terms whenever possible.

### 4.1 Bauteiltyp

Keep this vocabulary exactly.

```text
Ausbau
Boden
Dach
Daemmung
Decke
Fassade
Fenster
Fundament
Gelaender
Stuetze
Technik
Traeger
Treppe
Tuer
Wand
```

Rules:
- A `Bauteilgruppe` may connect to multiple `Bauteiltyp` nodes.
- Example: reused steel profiles may connect to `Traeger` and `Stuetze`.
- Example: reused apartment units may connect to `Wand` and `Decke`.

### 4.2 Bauteilebene

```text
Bauteilgruppe
Einzelbauteil
Gebaeudeteil
Materialcharge
Oberflaechenschicht
System
```

### 4.3 Bauobjektklasse

```text
Depot_Lager
Gebaeude
Gebaeudeteil
Infrastruktur
Innenausbau
Pavillon
Quartier_Areal
Reuse_Centre
```

### 4.4 Bauobjektrolle

```text
Bestandsobjekt
Donorobjekt
Empfaengerobjekt
Referenzobjekt
Same_Site_Donor_Receiver
Zwischenlager
```

### 4.5 Material and Materialgruppe

Allowed `Material` examples:

```text
Aluminium
Beton
Daemmstoff
Glas
Gusseisen
Holz
Keramik
Kunststoff
Lehm
Naturstein
Recyclingbeton
Stahl
Stahlbeton
Stroh
Ziegel
```

Use these `Materialgruppe` mappings:

```text
Stahl -> Metall
Aluminium -> Metall
Gusseisen -> Metall
Beton -> Mineralisch
Stahlbeton -> Mineralisch
Recyclingbeton -> Mineralisch
Ziegel -> Mineralisch
Keramik -> Mineralisch
Naturstein -> Mineralisch
Lehm -> Mineralisch
Glas -> Mineralisch
Holz -> Biobasiert
Stroh -> Biobasiert
Daemmstoff -> Verbund_oder_Daemmstoff
Kunststoff -> Kunststoff
```

If the material is not in the list, create the closest material only if clearly supported. Otherwise keep the raw material in `Bauteilgruppe.note` and record a `migration_issue`.

### 4.6 HuerdeKategorie

Every `Huerde` should connect to one `HuerdeKategorie`.

```text
Technisch
Rechtlich
Wirtschaftlich
Logistisch
Planerisch
Daten_Evidenz
Sozial_Organisatorisch
Umwelt_Gesundheit
```

Recommended mapping:

```text
Akzeptanzproblem -> Sozial_Organisatorisch
Anschlussproblem -> Technisch
Aufbereitungsaufwand -> Technisch
Ausschreibungsproblem -> Rechtlich
Bauproduktstatus -> Rechtlich
Brandschutzkonflikt -> Technisch
Bruch_Beschaedigungsrisiko -> Technisch
Datenluecke -> Daten_Evidenz
Dauerhaftigkeit_Restlebensdauer -> Technisch
Entwurfsbindung -> Planerisch
Fehlende_Datenstandards -> Daten_Evidenz
Fehlende_Lagerflaeche -> Logistisch
Fehlende_Standardisierung -> Daten_Evidenz
Gewaehrleistung -> Rechtlich
Haftung -> Rechtlich
Heterogenitaet_Chargen -> Daten_Evidenz
Hygieneanforderung -> Technisch
Kompatibilitaetsproblem -> Technisch
Materialqualitaet_Unklar -> Daten_Evidenz
Mengenunsicherheit -> Daten_Evidenz
Schadstoffbelastung -> Umwelt_Gesundheit
Technische_Freigabe -> Technisch
Terminunsicherheit -> Logistisch
Toleranzen -> Technisch
Unkonventionelles_Material -> Planerisch
Verfuegbarkeitsproblem -> Logistisch
Witterung_Feuchte -> Technisch
Zustand_Unklar -> Daten_Evidenz
```

### 4.7 Akteurrolle

Use controlled actor roles, not properties.

```text
Architektur
Aufbereitung_Refurbishment
Bauausfuehrung
Bauherr_Auftraggeber
Betreiber_Nutzer
Brandschutz_Barrierefreiheit
Fassade
Forschung_Dokumentation
Kunst_Gestaltung
Landschaftsplanung
Materiallieferant
Nachhaltigkeitsberatung
Oeffentliche_Hand
Projektbeteiligte_Unbestimmt
Projektmanagement_Koordination
Pruefung_Qualitaetssicherung
Reuse_Beratung
Rueckbau_Demontage
Stahlbau_Fertigung
TGA_Gebaeudetechnik
Tragwerksplanung
```

### 4.8 Akteurtyp

Use `Akteurtyp` to group actors. Examples:

```text
Architekturbuero
Ingenieurbuero
Bauherr
Developer
Wohnungsbaugesellschaft
Oeffentliche_Institution
Rueckbauunternehmen
Bauunternehmen
Materialhaendler
Reuse_Beratung
Forschungseinrichtung
Universitaet
Kuenstler
Nutzer_Betreiber
Genossenschaft
NGO_Netzwerk
Softwareanbieter
Foerderinstitution
Unbestimmt
```

### 4.9 WiederverwendungsArt

```text
Adaptives_ReUse
Bestandserhalt
Design_for_Disassembly
Direkte_Wiederverwendung
Recycling
Refurbishment
Remanufacturing
Same_Site_ReUse
Upcycling
Urban_Mining
Weiterbauen_im_Bestand
```

Rules:
- Use `Direkte_Wiederverwendung` for counted direct reuse.
- Use `Bestandserhalt` only as contextual classification, not as direct reuse.
- If the component stays in place and same function, it usually is not a `Bauteilgruppe` unless the source treats it as transformed or reused in a new way.

### 4.10 Status

Use controlled status nodes.

```text
Gebaut
Geplant
In_Bau
Prototyp
Rueckgebaut
Temporaer
Unklar
Wettbewerb
Realisiert
Verworfen
Vorgeschlagen
```

Prefer `Realisiert` for component-level reuse status if the reused component is built/installed.
Prefer `Gebaut` for project-level built status.

---

## 5. Markdown-to-graph migration rules

### 5.1 Section 1: Einordnung

Map as follows:

```text
Entscheidung                  -> do not import
Bewertung                     -> Projekt.bewertung
Begründung                    -> Projekt.note or Projekt.raw_summary
Vertrauensgrad                -> do not create node; BELEGT_IN handles source link
Warnung Bestandserhalt        -> do not import
Warnung Möbel/Dekoration      -> do not import
Projektstatus                 -> Projekt -[:HAT_STATUS]-> Status
```

### 5.2 Section 2: Entitäten-Mapping

Map as follows:

```text
Fallstudie                    -> Projekt
Projekt                       -> Projekt
Gebäude / Bauwerk             -> Bauwerk
Ort                           -> Stadt + Land
People / Akteur               -> Akteur
Architekt / Bauherr etc.      -> Akteur + Akteurrolle
Bauteil                       -> Bauteilgruppe + Bauteiltyp
Material                      -> Material + Materialgruppe
Reuse-Strategie               -> WiederverwendungsArt / Methode
Abbruchmethode                -> Rueckbauverfahren
Aufbereitungsmethode          -> Aufbereitungsverfahren
Tragwerkssystem               -> Tragwerksprinzip / Bausystem / Bauweise
Verbindung                    -> Verbindungstechnik
Prüfung                       -> PruefungNachweis
Leistungsanforderung          -> Leistungsanforderung
Norm                          -> Norm
Recht                         -> RechtlicheBedingung
Schadstoff                    -> Schadstoff
Wirtschaft                    -> Wirtschaft
Logistik                      -> Logistik
Bauteilbörse                  -> Beschaffungsweg / Ressourcenquelle
Methode                       -> Methode
Software                      -> Software
Tool                          -> Tool
Quelle                        -> Quelle
```

### 5.3 Section 3: Fallstudie

Map as follows:

```text
Name                          -> Projekt.name
Ort                           -> Stadt + Land
Gebäude                       -> Bauwerk
Projekt                       -> Projekt.name / Projekt.raw_summary
Beteiligte Akteure            -> Akteur nodes
Architekt                     -> Akteur + Akteurrolle Architektur
Tragwerksplaner               -> Akteur + Akteurrolle Tragwerksplanung
Bauherr                       -> Akteur + Akteurrolle Bauherr_Auftraggeber
Zeitraum                      -> Projekt.jahr_beginn / Projekt.jahr_fertigstellung
Ursprüngliche Nutzung          -> Bauwerk or Projekt -[:HAT_NUTZUNG]-> Nutzung, or Bauteilgruppe.alte_funktion when component-specific
Neue Nutzung                  -> Projekt/Bauwerk -[:HAT_NUTZUNG]-> Nutzung
Fläche / Maßstab              -> Projekt.flaeche_m2 or Bauwerk.flaeche_m2
Schutzstatus                  -> RechtlicheBedingung or Projekt.note
Quellenlage                   -> do not create node; use Quelle links
```

### 5.4 Section 4: Reuse-Strategie

Map as follows:

```text
Art der Wiederverwendung      -> WiederverwendungsArt
Hauptniveau                   -> Bauteilebene / Bauteiltyp / Tragwerksprinzip
Unterschied zu Sanierung etc. -> use only if it affects counts_as_direct_reuse or WiederverwendungsArt
Warum relevant                -> Projekt.note
```

### 5.5 Section 5: Bauteil-Inventar

Each inventory table row becomes one `Bauteilgruppe` node.

Map columns as follows:

```text
Bauteil                       -> Bauteilgruppe.raw_name + Bauteiltyp
Material                      -> Material + Materialgruppe
Herkunft                      -> AUS_BAUWERK / Ressourcenquelle
alte Funktion                 -> Bauteilgruppe.alte_funktion
neue Funktion                 -> Bauteilgruppe.neue_funktion
Menge/Umfang                  -> scalar properties on Bauteilgruppe
tragend?                      -> Tragwerksprinzip or note
räumlich?                     -> Bauteilebene or note
Hülle?                        -> Bauteiltyp Fassade/Fenster/Dach etc.
technisch?                    -> Bauteiltyp Technik
Eingriff/Aufbereitung         -> Aufbereitungsverfahren
Verbindung                    -> Verbindungstechnik
Prüfung                       -> PruefungNachweis
Leistungsanforderung          -> Leistungsanforderung
Norm/Recht                    -> Norm / RechtlicheBedingung
Hürde                         -> Huerde + HuerdeKategorie
Quelle                        -> BELEGT_IN -> Quelle
unbekannt                     -> note
```

---

## 6. ID-generation rules

Use stable lowercase ASCII IDs.

Rules:
- Lowercase.
- Replace spaces, slashes, dashes, punctuation with underscores.
- Remove accents.
- Use project prefix for occurrence nodes.
- Use controlled-vocab prefix for controlled terms.

Examples:

```text
Projekt: projekt_55_great_suffolk_street
Bauwerk: bauwerk_55_gss_receiver
Bauteilgruppe: btg_55gss_reused_steel_profiles_external_core
Akteur: akt_hawkins_brown
Quelle: quelle_55_great_suffolk_street_london_md
Bauteiltyp: bt_traeger
Material: mat_stahl
Materialgruppe: matgrp_metall
Huerde: h_technische_freigabe
HuerdeKategorie: hk_technisch
Stadt: stadt_london
Land: land_united_kingdom
```

Do not create duplicate nodes with different IDs for the same controlled term.

---

## 7. Output format

Return exactly one valid JSON object.

Do not wrap the JSON in markdown.
Do not add explanations outside the JSON.

Use this structure:

```json
{
  "nodes": [
    {
      "id": "projekt_example",
      "label": "Projekt",
      "properties": {
        "name": "Example Project",
        "bewertung": 4
      }
    }
  ],
  "relationships": [
    {
      "start_id": "projekt_example",
      "type": "BELEGT_IN",
      "end_id": "quelle_example_md",
      "properties": {
        "datenqualitaet": "Belegt"
      }
    }
  ],
  "migration_issues": [
    {
      "severity": "info",
      "message": "No issue."
    }
  ]
}
```

### 7.1 Node object rules

Each node must contain:

```json
{
  "id": "stable_unique_id",
  "label": "AllowedLabel",
  "properties": {}
}
```

Properties must not duplicate controlled relationships.

Wrong:

```json
{
  "label": "Bauwerk",
  "properties": {
    "stadt": "London",
    "land": "United Kingdom",
    "bauobjektrolle": "Donorobjekt"
  }
}
```

Correct:

```json
{
  "label": "Bauwerk",
  "properties": {
    "name": "1 Broadgate"
  }
}
```

Then add relationships to `Stadt`, `Land`, and `Bauobjektrolle`.

### 7.2 Relationship object rules

Each relationship must contain:

```json
{
  "start_id": "node_a",
  "type": "RELATIONSHIP_TYPE",
  "end_id": "node_b",
  "properties": {}
}
```

Only `BELEGT_IN` requires `datenqualitaet`.

---

## 8. Minimum graph requirements

Every transformed file must create at least:

```text
1 Projekt
1 Quelle
1 BELEGT_IN relationship from Projekt to Quelle
```

If the file contains reusable components, each component group must create:

```text
1 Bauteilgruppe
1 HAT_BAUTEILGRUPPE relationship from Projekt to Bauteilgruppe
1 HAT_BAUTEILTYP relationship, if type can be classified
1 NUTZT_MATERIAL relationship, if material is known
1 BELEGT_IN relationship from Bauteilgruppe to Quelle
```

If donor or receiver objects are known, create `Bauwerk` nodes and connect them:

```text
Bauteilgruppe -[:AUS_BAUWERK]-> Bauwerk donor
Bauteilgruppe -[:EINGEBAUT_IN]-> Bauwerk receiver
```

---

## 9. Handling uncertainty and conflict

Do not create `Datenqualitaet` nodes.
Do not create `Claim` nodes.
Do not create `Kennwert` nodes.

Use properties and notes:

```json
{
  "flaeche_m2_min": 4871,
  "flaeche_m2_max": 7603,
  "note": "Conflicting area values in source file."
}
```

If a component quantity conflicts:

```json
{
  "menge_t_min": 16,
  "menge_t_max": 100,
  "note": "Public sources report conflicting reused steel quantities."
}
```

If the source says something is unknown, do not create a node for the unknown term. Add a note only if analytically important.

---

## 10. Direct reuse boundary

Create `Bauteilgruppe` nodes only for actual reused building components, technical components, fixed elements, structural elements, envelope elements, spatial elements, or material/component groups.

Do not create counted `Bauteilgruppe` nodes for:

```text
ordinary Bestandserhalt where the component stayed in place and same function
loose furniture
decoration only
general adaptive reuse without component movement or transformation
recycling into raw material unless the source frames it as direct component/material reuse
future design-for-disassembly without current reuse
```

If Bestandserhalt is important context, represent it as:

```text
Projekt -[:HAT_WIEDERVERWENDUNGSART]-> Bestandserhalt
```

But do not count it as a `Bauteilgruppe` unless it involves transformed or newly reused components.

---

## 11. Final checklist before output

Before returning JSON, verify:

1. There is no `Fallbeispiel` node.
2. `Projekt` is central.
3. `Bauwerk` is separate from `Projekt`.
4. `Bauteilgruppe` is a reuse occurrence, not just a category.
5. `stadt`, `land`, `bauobjektklasse`, `bauobjektrolle`, `akteurrolle`, `material`, `bauteiltyp`, `huerde`, `status`, `nutzung`, and `norm` are not properties when they should be nodes.
6. `datenqualitaet` appears only on `BELEGT_IN` relationships and is always `"Belegt"`.
7. Metrics are properties, not nodes.
8. Source file is represented as `Quelle`.
9. Major nodes link to `Quelle` through `BELEGT_IN`.
10. No invented facts are present.
11. Output is valid JSON only.

---

## 12. Paste the old markdown file below

Transform the following old markdown case file according to this source-of-truth prompt.

```markdown
<<PASTE_OLD_MARKDOWN_FILE_HERE>>
```
