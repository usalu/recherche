---
name: Neo4j schema catalogue
overview: Metadata-only Neo4j schema. The graph carries identifiers, classifications, measurements, and relationships — NOT German prose. body_md / legacy_paths / build_status / raw labels live only in the source Markdown, never in the graph. Six instance Labels (:Fallbeispiel, :Bauteilgruppe, :Akteur, :Quelle, :SoftwareDigitaltool, :Wiederverwendungskette) and 37 vocabulary Labels (covering every folder under _database/). Five generic edges (IST, HAT, BENUTZT, GEHÖRT_ZU, BELEGT_IN). All source attribution is via :BELEGT_IN edges to :Quelle nodes.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the 4-section structure: §1 Node-type catalogue, §2 Nodes (per-Label property tables), §3 Edge-type catalogue, §4 Edges (per-edge-type property tables). Plus appendices for principles, constraints, coverage (every folder → Label/drop), renamings."
    status: pending
  - id: write-1
    content: "Write §1 Node-type catalogue: 6 instance Labels and the 37 vocabulary Labels, with one-line purpose each. Confirm against _database/ folder list."
    status: pending
  - id: write-2
    content: "Write §2 Nodes: per-Label property tables. ONLY metadata properties — no body, no legacy_paths, no raw labels, no build_status."
    status: pending
  - id: write-3
    content: "Write §3 Edge-type catalogue: 5 generic edges with source/target Label families and the legacy relations folded into each."
    status: pending
  - id: write-4
    content: "Write §4 Edges: per-edge-type property table. :BELEGT_IN is the only citation edge."
    status: pending
  - id: appendices
    content: "Write the appendices: A modeling principles (metadata-only, hybrid modes), B constraints & indexes, C complete coverage checklist (every folder under _database/ accounted for), D renamings / drops / merges."
    status: pending
---

# Goal

Author `_database/_system/NEO4J_SCHEMA.md` in the four-part order: §1 Node-type catalogue → §2 Nodes (properties) → §3 Edge-type catalogue → §4 Edges (properties). Plus appendices.

**Key principle: the graph carries metadata only.** German prose, raw labels, legacy file paths, build-batch status — none of this is in the graph. It stays in the Markdown source under `_database/`. The graph carries identifiers (ids), classifications (edges), and quantitative facts (measurement properties).

---

# Hierarchiebaum — alle Knotentypen, Knoten, Eigenschaften; alle Kantentypen, Kanten, Eigenschaften

Lesen: **Knotentyp** = Neo4j-Label. **Knoten** = eine Instanz (ein Unterordner oder ein zusammengeführter Datensatz). **Knoteneigenschaften** = Properties auf diesem Knoten. **Kantentyp** = Relationship-Typ. **Kante** = eine konkrete Relationship zwischen zwei Knoten. **Kanteneigenschaften** = Properties auf der Kante.

Vokabular-Knoten: jedes `id` entspricht dem Ordnernamen unter `_database/<vocab>/<id>/` (Prosa nur in `index.md`, nicht im Graphen).

```
Neo4j_Schema
│
├── KNOTENTYP :Fallbeispiel
│   ├── Knoteneigenschaften (Schema für jeden Knoten dieses Typs)
│   │   ├── id: string (Pflicht, UNIQUE)
│   │   ├── art: string (Pflicht) — Gebaeude | Bruecke | Pavillon | Halle | Lager | Innenausbau | Anlage
│   │   ├── flaeche_m2, projektflaeche_m2, gebaeudemasse_t: float? (optional)
│   │   ├── wohneinheiten, fertigstellung_jahr, entwurfsbeginn_jahr, bauzeit_monate, lebensdauer_jahre: int? (optional)
│   │   ├── restlebensdauer_jahre, kosten_eur, budget_eur, co2_footprint_kg, energieverbrauch_kwh_a, wassereinsparung_m3, bestandslager_m3: float? (optional)
│   │   └── je Messgröße optional: <name>_alt: list<float>?, <name>_vertrauensgrad: string?
│   └── Knoten (Instanzen)
│       └── je ein Knoten pro zusammengeführter Fall-ID (legacy fallstudie + projekt + bauobjekt gleiche id)
│
├── KNOTENTYP :Bauteilgruppe
│   ├── Knoteneigenschaften
│   │   ├── id: string (Pflicht, UNIQUE)
│   │   ├── masse_t, volumen_m3, flaeche_m2, anteil_prozent, co2_einsparung_kg, co2_reduktion_kg: float? (optional)
│   │   ├── anzahl_stueck: int? (optional)
│   │   ├── geerntete_materialien_t, sekundaere_materialien_t, abfall_vermieden_t: float? (optional)
│   │   ├── zielwert_reuse_prozent: float? (optional)
│   │   └── je Messgröße optional: <name>_alt, <name>_vertrauensgrad (wie :Fallbeispiel)
│   └── Knoten (Instanzen)
│       └── je ein Knoten pro legacy reuse_einsatz/<id>/
│
├── KNOTENTYP :Akteur
│   ├── Knoteneigenschaften: id (Pflicht), art? (string), url? (string)
│   └── Knoten: je ./_database/akteur/<id>/
│
├── KNOTENTYP :Quelle
│   ├── Knoteneigenschaften: id (Pflicht), art (Pflicht: Website|Interview|Paper|Buch|Bericht|Datenbank|Vortrag|Norm|Sonstige), url? (string)
│   └── Knoten: je Quelle (Ordner oder fallgebundene abgeleitete id)
│
├── KNOTENTYP :SoftwareDigitaltool
│   ├── Knoteneigenschaften: id (Pflicht), url? (string)
│   └── Knoten: je ./_database/software_digitaltool/<id>/
│
├── KNOTENTYP :Wiederverwendungskette
│   ├── Knoteneigenschaften: id (Pflicht), start_jahr?, end_jahr? (int)
│   └── Knoten: je ./_database/reuse_kette/<id>/ (umbenanntes Konzept)
│
├── KNOTENTYP :Bauteiltyp:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausbau, Boden, Dach, Daemmung, Decke, Fassade, Fenster, Fundament, Gelaender, Stuetze, Technik, Traeger, Treppe, Tuer, Wand
├── KNOTENTYP :Material:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aluminium, Beton, Daemmstoff, Glas, Gusseisen, Holz, Keramik, Kunststoff, Lehm, Naturstein, Recyclingbeton, Stahl, Stahlbeton, Stroh, Ziegel
├── KNOTENTYP :Bauteilebene:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteilgruppe, Einzelbauteil, Gebaeudeteil, Materialcharge, Oberflaechenschicht, System
├── KNOTENTYP :Bauteilzustand:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Beschaedigt, Geprueft, Intakt, Kontaminiert, Korrodiert, Patiniert, Restlebensdauer_Bekannt, Restlebensdauer_Unklar, Ungeprueft
├── KNOTENTYP :Funktionswechsel:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Dekorative_Funktion, Gleiche_Funktion, Konstruktive_Funktion, Neue_Funktion, Technische_Funktion, Unbekannt
├── KNOTENTYP :FuegungVerbindung:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Klemmverbindung, Reversible_Fuegung, Steckverbindung, Verleimung, Vermoertelung, Verschraubung, Verschweissung
├── KNOTENTYP :Bauweise:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fertigteilbauweise, Holzbauweise, Hybridbauweise, Massivbauweise, Ortbetonbauweise, Stahlbauweise
├── KNOTENTYP :Bausystem:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Betonfertigteil_System, Holzrahmenbau, Holz_Skelettbau, Plattenbau, Stahl_Skelettbau
├── KNOTENTYP :Tragwerksprinzip:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fachwerk, Skeletttragwerk, Wandtragwerk, Wand_Kern_Tragwerk
├── KNOTENTYP :ReuseStrategie:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Adaptives_ReUse, Bestandserhalt, Design_for_Disassembly, Direkte_Wiederverwendung, Recycling, Refurbishment, Remanufacturing, Same_Site_ReUse, Upcycling, Urban_Mining, Weiterbauen_im_Bestand
├── KNOTENTYP :ReuseEinsatzstatus:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Geplant, Prototypisch, Realisiert, Temporaer, Unklar, Verworfen, Vorgeschlagen
├── KNOTENTYP :WiederverwendungsArt:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht), axis (Pflicht: einordnung | grundtyp)
│   └── Knoten: Bestandserhalt_Nicht_Direct_Reuse, Kein_Direct_Reuse_Nachweis, Moebel_Dekoration_Nicht_Direct_Reuse, Recycling_Nicht_Direct_Reuse, Reuse_Anteil_Unklar, Ungebaut_Nicht_Realisierte_Wiederverwendung, Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung
├── KNOTENTYP :Ressourcenquelle:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Baustelle, Bauteilboerse, Donorgebaeude, Donor_Infrastruktur, Haendler, Lager, Materialstockpile, Produktionsueberschuss, Unbekannt
├── KNOTENTYP :Beschaffungsweg:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausschreibung, Bauteilboerse, Digitale_Plattform, Direktvermittlung, Eigenbestand, Informelles_Netzwerk, Rueckbauprojekt, Spende
├── KNOTENTYP :Prozessphase:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aufbereitung, Betrieb, Dokumentation, Identifikation, Lagerung, Planung, Pruefung, Rueckbau, Transport, Wiedereinbau
├── KNOTENTYP :Rueckbauverfahren:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausbau_von_Bauteilen, Betonfraesen, Demontage, Selektiver_Rueckbau, Zerstoerungsarme_Bergung
├── KNOTENTYP :Aufbereitungsverfahren:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Drahtglasschneiden, Entmoertelung_von_Fliesen, Holzaufbereitung, Leuchten_Refurbishment, Qualitaetssicherung, Reinigung, Rekonditionierung, Remanufacturing, Reparatur, Verstaerkung, Zuschnitt
├── KNOTENTYP :Logistik:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteiltracking, Just_in_Time, Lagerflaeche, Lagerung, Lokale_Wiederverwendung, Materialmatching, Materialverfuegbarkeit, Transport, Transportdistanz, Zwischenlagerung
├── KNOTENTYP :Methode:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Abrissmonitoring, Bauteilkatalogisierung, Building_Material_Scouting, Design_for_Disassembly, Form_Follows_Availability, Materialinventur, Pre_Deconstruction_Audit, ReUse_Assessment, ReUse_Ausschreibung, Reversibilitaet, Urban_Mining, Wiederverwendungskriterien, Zirkulaere_Ausschreibung
├── KNOTENTYP :Huerde:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit, Schadstoffbelastung, Technische_Freigabe, Terminunsicherheit, Toleranzen, Unkonventionelles_Material, Verfuegbarkeitsproblem, Witterung_Feuchte, Zustand_Unklar
├── KNOTENTYP :PruefungNachweis:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Abbrandbemessung, Brandschutznachweis, Eignungspruefung_Baulehm, Geometrische_Vermessung, Materialpruefung, Schadstoffscreening, Schweissbarkeitspruefung, Sichtpruefung, Statische_Nachweisfuehrung, Zugversuch, Zustandsbewertung
├── KNOTENTYP :Leistungsanforderung:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Brandschutz, Brandschutzanforderung, Dauerhaftigkeit, F90, Feuchteschutz, Feuerwiderstand, R90, REI90, Rueckbaubarkeit, Schadstofffreiheit, Schallschutz, Tragfaehigkeit, Waermeschutz
├── KNOTENTYP :Norm:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: DIN_18940, DIN_EN_15804, DIN_EN_15978, EN_1090, ISO_14040, ISO_14044, ISO_20887
├── KNOTENTYP :RechtlicheBedingung:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauordnungsrecht, EU_Taxonomie, Gewaehrleistung, Produkthaftung, Vergaberecht, Zulassung_im_Einzelfall
├── KNOTENTYP :Schadstoff:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Asbest, Bleifarbe, Holzschutzmittel, PAK, PCB
├── KNOTENTYP :Bauobjektstatus:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Gebaut, Geplant, In_Bau, Prototyp, Rueckgebaut, Temporaer, Unklar, Wettbewerb
├── KNOTENTYP :Nutzung:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Buero, Gewerbe, Infrastruktur, Kultur, Lager_Depot, Mischnutzung, Schule_Bildung, Sozialbau, Wohnen
├── KNOTENTYP :BauaufgabeIntervention:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aufstockung, Erweiterung, Fit_out, Neubau, Rueckbau, Sanierung, Translozierung, Umbau, Umnutzung, Wiederaufbau
├── KNOTENTYP :Kontextmerkmal:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bestandserhalt_Policy, Pilotprojekt
├── KNOTENTYP :Ort:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht), iso_country?, koordinaten? (string)
│   └── Knoten: Aarhus, Arnhem, Asse, Barcelona, Basel, Berlin, Berlin_Neukoelln, Bleijerheide, Boston, Boulder, Brighton, Broethen, Bruessel, Colombelles, Copenhagen, Den_Bosch, Deutschland, Dilbeek, Duiven, Eindhoven, Enschede, Europa, Evere, Gentbrugge, Gladsaxe, Groeditz, Hackbridge, Hannover, Hastings, Helsinki, Kamikatsu, Kindl_Areal_Standort, Kloetinge, Leiden, Lexington, Liege, London, Lo_Reninge, Luxembourg_Limpertsberg, Maassluis, Mehrow, Mouscron, Mueggelsee, Muehlhausen, Muenchen, Muenster, Oslo, Paris, Paso_Robles, Plauen, Rotterdam, Schildow, Schweiz, Southwark, Stains, Tampere, Utrecht, Volkenroda, Walkeweg, Winterthur, Zuerich
├── KNOTENTYP :Akteurrolle:Vokabular (nur Wörterbuch; Rolle als Property auf HAT, nicht als IST-Ziel)
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Architektur, Aufbereitung_Refurbishment, Bauausfuehrung, Bauherr_Auftraggeber, Betreiber_Nutzer, Brandschutz_Barrierefreiheit, Fassade, Forschung_Dokumentation, Kunst_Gestaltung, Landschaftsplanung, Materiallieferant, Nachhaltigkeitsberatung, Oeffentliche_Hand, Projektbeteiligte_Unbestimmt, Projektmanagement_Koordination, Pruefung_Qualitaetssicherung, Reuse_Beratung, Rueckbau_Demontage, Stahlbau_Fertigung, TGA_Gebaeudetechnik, Tragwerksplanung
├── KNOTENTYP :Datenqualitaet:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Belegt, Geschaetzt, Nicht_Belegt, Primaerquelle, Sekundaerquelle, Unbekannt, Widerspruechlich
├── KNOTENTYP :Datenmodell:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteil_ID, IFC, Klassifikation, Materialdatenbank, Materialpass_Schema, Ontologie, Taxonomie
├── KNOTENTYP :Tooltyp:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteilboerse, Materialdatenbank, Materialkataster
├── KNOTENTYP :ZertifizierungBewertungssystem:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: BREEAM, DGNB, LEED, Paris_Proof, WELL
├── KNOTENTYP :Wirtschaft:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Finanzierung, Geschaeftsmodell, Kostenvergleich, Lebenszykluskosten, Preisbildung, Restwert
└── KNOTENTYP :Programm:Vokabular
    ├── Knoteneigenschaften: id (Pflicht), programm_typ (Pflicht: foerderung | forschungskontext)
    └── Knoten: BBSM, FCRBE, PREUSE, Reallabor_Be_Ware, Zukunftbau, Foerderprogramm, Forschungsprojekt, Kommunales_Programm, Pilotprojekt, Reallabor, Wettbewerb

KANTEN (alle fünf Typen; jede Kante ist eine Instanz zwischen zwei Knoten)

├── KANTENTYP IST
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung?
│   └── Kante (Beispielmuster)
│       └── (:Fallbeispiel|:Bauteilgruppe|:Akteur|:Quelle|:SoftwareDigitaltool|:Wiederverwendungskette) -[IST]-> (:<Vokabular-Knotentyp> {id})
│
├── KANTENTYP HAT
│   ├── Kanteneigenschaften: art (Pflicht), rolle? (Pflicht wenn art=akteur), anzahl?, intensitaet?, seit?, bis?
│   └── Kante (Beispielmuster)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: huerde|prozessphase|pruefung|norm|…}]-> (:Huerde|:Prozessphase|:Norm|…)
│       └── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: akteur, rolle: "<Akteurrolle.id>"}]-> (:Akteur)
│
├── KANTENTYP BENUTZT
│   ├── Kanteneigenschaften: anzahl?, einheit?, anteil_prozent?, funktion_alt?, funktion_neu?, aufbereitung?
│   └── Kante (Beispielmuster)
│       └── (:Bauteilgruppe|:Fallbeispiel) -[BENUTZT]-> (:Material|:Methode|:Rueckbauverfahren|:Aufbereitungsverfahren|:SoftwareDigitaltool|:Datenmodell)
│
├── KANTENTYP GEHÖRT_ZU
│   ├── Kanteneigenschaften: rolle (Pflicht), position?, seit?, bis?
│   └── Kante (Beispielmuster)
│       ├── (:Bauteilgruppe) -[GEHÖRT_ZU {rolle: einbauort|herkunft|zwischenlager|verarbeitung|transport}]-> (:Fallbeispiel)
│       ├── (:Bauteilgruppe) -[GEHÖRT_ZU {rolle: kette, position}]-> (:Wiederverwendungskette)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: ort}]-> (:Ort)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: programm}]-> (:Programm)
│       └── (weitere) je nach Export-Regeln
│
└── KANTENTYP BELEGT_IN
    ├── Kanteneigenschaften: eigenschaft?, seite?, excerpt?, raw_label?
    └── Kante (Beispielmuster)
        └── (:Fallbeispiel|:Bauteilgruppe|…) -[BELEGT_IN]-> (:Quelle)
```

Hinweis: Ordner ohne eigenen Knotentyp (z. B. `datenpunkt/`, `kennwertdefinition/`, `fallstudie/`) sind in §1.C des Plans aufgeführt — sie erzeugen **keine** eigenen Knoten im Zielgraphen, sondern fließen in Properties, Kanten oder Merges ein.

---

# §1 Node-type catalogue

**Folder-to-node mapping rule (applies to all entities):**

Each direct subfolder of `_database/` is a **node type** (Neo4j Label). Each subfolder *inside* it is a **node** of that type, with the subfolder name as `id`.

Example for `_database/norm/`:

```
_database/norm/                          → Label :Norm
_database/norm/DIN_18940/index.md        → node (:Norm {id: "DIN_18940"})
_database/norm/EN_1090/index.md          → node (:Norm {id: "EN_1090"})
_database/norm/ISO_20887/index.md        → node (:Norm {id: "ISO_20887"})
```

Same rule for every folder: `_database/material/<x>/` produces `(:Material {id: "<x>"})`, `_database/huerde/<x>/` produces `(:Huerde {id: "<x>"})`, etc.

Exceptions (folders that are NOT 1:1 a node type) are listed in §1.C — they merge into another Label, get renamed, or are dropped.

## §1.A Instance Labels (6)

| Label | Purpose | Replaces (legacy folders) |
|---|---|---|
| `:Fallbeispiel` | One physical case-study object | `fallstudie/` + `projekt/` + `bauobjekt/` (merged where ids match) |
| `:Bauteilgruppe` | A group of components in a Fallbeispiel — the reuse-Einsatz | `reuse_einsatz/` |
| `:Akteur` | Office / company / authority / institution / person | `akteur/` |
| `:Quelle` | Source / citation target | `quelle/` |
| `:SoftwareDigitaltool` | Concrete platform | `software_digitaltool/` |
| `:Wiederverwendungskette` | OPTIONAL named multi-Bauteilgruppe reuse program | `reuse_kette/` (renamed; `reuse_kettenstation/` dropped) |

## §1.B Vocabulary Labels (37 — every controlled-knot folder mapped)

Grouped only for reading.

**Bauteil & Material:**
- `:Bauteiltyp` ← `bauteiltyp/`
- `:Material` ← `material/`
- `:Bauteilebene` ← `bauteilebene/`
- `:Bauteilzustand` ← `bauteilzustand/`
- `:Funktionswechsel` ← `funktionswechsel/`
- `:FuegungVerbindung` ← `fuegung_verbindung/`

**Konstruktion:**
- `:Bauweise` ← `bauweise/`
- `:Bausystem` ← `bausystem/`
- `:Tragwerksprinzip` ← `tragwerksprinzip/`

**Reuse:**
- `:ReuseStrategie` ← `reuse_strategie/`
- `:ReuseEinsatzstatus` ← `reuse_einsatzstatus/`
- `:WiederverwendungsArt` ← `bewertungslogik_abgrenzung/` (renamed)

**Beschaffung:**
- `:Ressourcenquelle` ← `ressourcenquelle/`
- `:Beschaffungsweg` ← `beschaffungsweg/`

**Prozess & Methode:**
- `:Prozessphase` ← `prozessphase/`
- `:Rueckbauverfahren` ← `rueckbauverfahren/`
- `:Aufbereitungsverfahren` ← `aufbereitungsverfahren/`
- `:Logistik` ← `logistik/`
- `:Methode` ← `methode/`

**Anforderungen & Hürden:**
- `:Huerde` ← `huerde/`
- `:PruefungNachweis` ← `pruefung_nachweis/`
- `:Leistungsanforderung` ← `leistungsanforderung/`
- `:Norm` ← `norm/`
- `:RechtlicheBedingung` ← `rechtliche_bedingung/`
- `:Schadstoff` ← `schadstoff/`

**Fallbeispiel-Kontext:**
- `:Bauobjektstatus` ← `bauobjektstatus/` (bestehend / abgerissen / geplant)
- `:Nutzung` ← `nutzung/`
- `:BauaufgabeIntervention` ← `bauaufgabe_intervention/`
- `:Kontextmerkmal` ← `kontextmerkmal/`

**Geographie:**
- `:Ort` ← `ort/`

**Akteure:**
- `:Akteurrolle` ← `akteurrolle/` (dictionary only — value carried as `rolle` property on HAT edges, no IST edges point here)

**Daten & Bewertung:**
- `:Datenqualitaet` ← `datenqualitaet/`
- `:Datenmodell` ← `datenmodell/`
- `:Tooltyp` ← `tooltyp/`
- `:ZertifizierungBewertungssystem` ← `zertifizierung_bewertungssystem/`

**Wirtschaft & Programme:**
- `:Wirtschaft` ← `wirtschaft/`
- `:Programm` ← `foerderprogramm/` + `programm_kontext/` (merged; `programm_typ` property: `"foerderung"` / `"forschungskontext"`)

## §1.C Folders mapped but NOT a Label

| Folder | Disposition |
|---|---|
| `fallstudie/` | merged into `:Fallbeispiel` |
| `projekt/` | merged into `:Fallbeispiel` |
| `bauobjekt/` | merged into `:Fallbeispiel` |
| `reuse_einsatz/` | renamed to `:Bauteilgruppe` |
| `reuse_kettenstation/` | dropped — stations become GEHÖRT_ZU edges from `:Bauteilgruppe` |
| `akteur_beteiligung/` | dropped — collapsed to `HAT {art:'akteur', rolle:...}` edge |
| `bauobjekt_beteiligung/` | dropped — same pattern |
| `datenpunkt/` | dropped — measurements as node properties |
| `kennwertdefinition/` | dropped — kennwert-names live as property names |
| `bauobjektklasse/` | dropped — values collapse into `:Fallbeispiel.art` |
| `bauobjektrolle/` | dropped — donor/receiver/standalone derivable from incoming GEHÖRT_ZU edges (`rolle:'herkunft'` / `rolle:'einbauort'`) |
| `dokumenttyp/` | dropped — replaced by `:Quelle.art` |
| `tragwerkstyp/` | dropped — axis-mix (review §7.8); material values derivable from `:Material`, reuse values folded into `:WiederverwendungsArt` |
| `foerderprogramm/` | merged into `:Programm` |
| `programm_kontext/` | merged into `:Programm` |
| `bewertungslogik_abgrenzung/` | renamed to `:WiederverwendungsArt` |
| `reuse_kette/` | renamed to `:Wiederverwendungskette` |

Total: 54 folders → 6 instance Labels + 37 vocabulary Labels + 11 dropped + 4 merged-or-renamed.

---

# §2 Nodes — properties per Label

Property table columns: **name** | **type** | **req** | **notes**.

**No `body_md`, no `title`, no `legacy_paths`, no `build_status`, no raw-text labels on any node.** All German prose stays in the source Markdown under `_database/<entity>/<id>/index.md`, outside the graph.

## §2.A `:Fallbeispiel`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE; folder slug |
| `art` | string | ✓ | one of `"Gebaeude"`, `"Bruecke"`, `"Pavillon"`, `"Halle"`, `"Lager"`, `"Innenausbau"`, `"Anlage"` |

**Building-level measurement properties** (all optional; missing = unknown):

| name | type | notes |
|---|---|---|
| `flaeche_m2` | float? | |
| `projektflaeche_m2` | float? | |
| `gebaeudemasse_t` | float? | |
| `wohneinheiten` | int? | |
| `fertigstellung_jahr` | int? | |
| `entwurfsbeginn_jahr` | int? | |
| `bauzeit_monate` | int? | |
| `lebensdauer_jahre` | int? | |
| `restlebensdauer_jahre` | float? | |
| `kosten_eur` | float? | |
| `budget_eur` | float? | |
| `co2_footprint_kg` | float? | |
| `energieverbrauch_kwh_a` | float? | |
| `wassereinsparung_m3` | float? | |
| `bestandslager_m3` | float? | |

For each measurement property, optional parallel:
- `<name>_alt: list<float>?` — alternate values from conflicting sources
- `<name>_vertrauensgrad: string?` — `belegt` / `teilweise_belegt` / `unklar` / `umstritten`

Source attribution: `:BELEGT_IN` edges with `eigenschaft:'<name>'`.

## §2.B `:Bauteilgruppe`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE |

**Component-group measurement properties:**

| name | type | notes |
|---|---|---|
| `masse_t` | float? | |
| `anzahl_stueck` | int? | |
| `volumen_m3` | float? | |
| `flaeche_m2` | float? | component area |
| `anteil_prozent` | float? | share of receiver's total |
| `co2_einsparung_kg` | float? | |
| `co2_reduktion_kg` | float? | |
| `geerntete_materialien_t` | float? | |
| `sekundaere_materialien_t` | float? | |
| `abfall_vermieden_t` | float? | |
| `zielwert_reuse_prozent` | float? | |

Same `_alt` and `_vertrauensgrad` shadow properties as on `:Fallbeispiel`.

**No properties for:** bauteil_label, material_label, alte_funktion, neue_funktion, herkunft_label, pruefung_label_raw, norm_recht_label_raw, huerde_label_raw, menge_umfang_raw, quelle_label_raw, body, title.

Where each of those previously lived in the graph (and now lives as an edge or is lost):
- `bauteil_label` (`"Stahlträger / Stützen"`) → canonical `IST→:Bauteiltyp` edge only; fine variant lost at graph level (still in source Markdown).
- `material_label` (`"Brettschichtholz"`) → canonical `BENUTZT→:Material` edge; fine variant lost at graph level.
- `menge_umfang_raw` (`"98 t; 95 %"`) → parsed onto `BENUTZT` edge: `anzahl: 98, einheit: "t", anteil_prozent: 95`.
- `alte_funktion` / `neue_funktion` → on the `BENUTZT` edge: `funktion_alt`, `funktion_neu`.
- `herkunft_label` → resolved to `GEHÖRT_ZU {rolle:'herkunft'}→:Fallbeispiel`; if unresolvable, lost at graph level.
- `pruefung_label`, `norm_recht_label`, `huerde_label` → broken into atomic `HAT` edges to `:PruefungNachweis` / `:Norm` / `:Huerde`.
- `quelle_label` → broken into `:BELEGT_IN` edges to `:Quelle` nodes.

## §2.C `:Akteur`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE |
| `art` | string? | – | optional: `"Firma"`, `"Buero"`, `"Behoerde"`, `"Institution"`, `"Person"`, `"Verband"`, `"Bauherrschaft"`, `"Sonstige"` |
| `url` | string? | – | website / firm page |

## §2.D `:Quelle`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE; folder slug or case-scoped derived (`K118_Kopfbau__S4`) |
| `art` | string | ✓ | one of `"Website"`, `"Interview"`, `"Paper"`, `"Buch"`, `"Bericht"`, `"Datenbank"`, `"Vortrag"`, `"Norm"`, `"Sonstige"` |
| `url` | string? | – | source URL or DOI |

No outgoing edges from `:Quelle`. All metadata about a citation (page, excerpt, raw shorthand, scoped property) lives on the incoming `:BELEGT_IN` edge.

## §2.E `:SoftwareDigitaltool`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE |
| `url` | string? | – | |

## §2.F `:Wiederverwendungskette`

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE |
| `start_jahr` | int? | – | |
| `end_jahr` | int? | – | |

## §2.G Vocabulary Labels (shared shape — every label in §1.B)

Each Label in §1.B has **as many nodes as there are subfolders** under its corresponding `_database/<vocab>/` directory. For instance: `_database/material/` has subfolders for `Stahl`, `Holz`, `Beton`, `Stahlbeton`, … — each becomes a `(:Material {id: "..."})` node. Same for every other vocab Label.

Each vocab node has only:

| name | type | req | notes |
|---|---|---|---|
| `id` | string | ✓ | UNIQUE within the Label; the subfolder name under `_database/<vocab>/<id>/` |

The id is the queryable identifier. The German prose body explaining the term remains in the source Markdown `_database/<vocab>/<id>/index.md`, outside the graph.

Special additions per vocab Label:

| Label | extra property | notes |
|---|---|---|
| `:Ort` | `iso_country: string?`, `koordinaten: string?` | optional geographic metadata |
| `:Programm` | `programm_typ: string` (req) | `"foerderung"` or `"forschungskontext"` |
| `:WiederverwendungsArt` | `axis: string` (req) | `"einordnung"` (legacy bewertungslogik values) or `"grundtyp"` (wiederverwendet/original/hybrid — absorbed from dropped :Bauteilgruppentyp) |

All vocab Labels carry the second Label `:Vokabular`.

---

# §3 Edge-type catalogue

| Edge | Subject Labels | Object Labels | Cardinality | Purpose |
|---|---|---|---|---|
| `IST` | `:Fallbeispiel`, `:Bauteilgruppe`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette` | vocab | N:1 per axis | classification / status |
| `HAT` | `:Fallbeispiel`, `:Bauteilgruppe` | vocab (rich) **or** `:Akteur` (with `art:'akteur', rolle:...`) | N:M | qualitative attribute / actor participation |
| `BENUTZT` | `:Bauteilgruppe`, `:Fallbeispiel` | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:SoftwareDigitaltool`, `:Datenmodell` | N:M | instrumental usage; quantitative carrier |
| `GEHÖRT_ZU` | any | `:Fallbeispiel`, `:Wiederverwendungskette`, `:Ort`, `:Programm` | N:1 / N:M | membership / containment / location / chain station / origin |
| `BELEGT_IN` | any node carrying a citable claim | `:Quelle` | N:M | citation / evidence — the only place source attribution lives |

## Legacy relations folded in

- **IST:** `has_bauteiltyp`, `has_reuse_einsatzstatus`, `has_reuse_strategie`, `has_bewertungslogik_abgrenzung` (→ `:WiederverwendungsArt`), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_bauobjektstatus`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`.
- **HAT:** `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff`, `has_kontextmerkmal`, `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung`, `has_logistik`, `has_wirtschaft`, plus actor participation `has_akteurrolle` → `HAT {art:'akteur', rolle:...}`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool`, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt` → `rolle:'einbauort'`; new `sourced_from_bauobjekt` → `rolle:'herkunft'`; `part_of_reuse_kette` → `rolle:'kette'` (to `:Wiederverwendungskette`); `located_in_ort` → `rolle:'ort'`; `relates_to_bauobjekt` → `rolle:'fallbeispiel'`; `involves_foerderprogramm` / `has_programm_kontext` → `rolle:'programm'` (to `:Programm`).
- **BELEGT_IN:** replaces unresolved `quelle_label` shorthand on every node and every `quelle_id` previously planned as edge property. Replaces the gap relation `documented_in_quelle`. Direction: claim → `:Quelle`.

Dropped legacy relations (no destination): `belongs_to_fallstudie`, `belongs_to_projekt`, `has_projekt`, `has_bauobjekt`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_tragwerkstyp`, `has_dokumenttyp`, `has_akteurrolle` (target dropped), `measured_on_bauobjekt`, `measures_kennwertdefinition`, `involves_akteur` (collapsed into HAT).

---

# §4 Edges — properties per edge type

**Note:** None of IST / HAT / BENUTZT / GEHÖRT_ZU carry a `quelle_id` or `quelle_label`. Source attribution lives exclusively on `:BELEGT_IN` edges from the edge's source node, optionally scoped via the `eigenschaft` property.

## §4.A `:IST`

| name | type | req | notes |
|---|---|---|---|
| `seit` | date? | – | start of validity |
| `bis` | date? | – | end of validity |
| `gewichtung` | float? | – | 0..1 confidence |

## §4.B `:HAT`

| name | type | req | notes |
|---|---|---|---|
| `art` | string | ✓ | one of `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"schadstoff"`, `"kontext"`, `"recht"`, `"nutzung"`, `"intervention"`, `"fuegung"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"`, `"akteur"` |
| `rolle` | string? | – | required when `art='akteur'`; e.g. `"Architektur"`, `"Tragwerksplanung"`, `"Bauherr_Auftraggeber"`; validates against `:Akteurrolle.id` |
| `anzahl` | int? | – | multiplicity |
| `intensitaet` | string? | – | qualitative strength |
| `seit` | date? | – | |
| `bis` | date? | – | |

## §4.C `:BENUTZT`

| name | type | req | notes |
|---|---|---|---|
| `anzahl` | float? | – | quantity used |
| `einheit` | string? | – | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float? | – | share-of-total |
| `funktion_alt` | string? | – | original role |
| `funktion_neu` | string? | – | new role |
| `aufbereitung` | string? | – | processing applied (free text) |

## §4.D `:GEHÖRT_ZU`

| name | type | req | notes |
|---|---|---|---|
| `rolle` | string | ✓ | one of `"fallbeispiel"`, `"einbauort"`, `"herkunft"`, `"zwischenlager"`, `"verarbeitung"`, `"transport"`, `"kette"`, `"ort"`, `"programm"` |
| `position` | int? | – | order in sequence (e.g., chain station number) |
| `seit` | date? | – | |
| `bis` | date? | – | |

## §4.E `:BELEGT_IN`

Direction: **(claim) → (:Quelle)**.

| name | type | req | notes |
|---|---|---|---|
| `eigenschaft` | string? | – | scopes citation to a specific property of the source node (e.g. `"flaeche_m2"`, `"co2_einsparung_kg"`); omit for node-level citation |
| `seite` | string? | – | page number |
| `excerpt` | string? | – | quoted excerpt |
| `raw_label` | string? | – | original shorthand (`"S4"`, `"[S1]"`) |

---

# Appendix A — Modeling principles

- **Metadata-only graph.** German prose, raw labels, legacy paths, batch tags do not enter the graph. They stay in the source Markdown.
- **Modes A/B/C coexist** but Mode A (property) is reserved for: identifiers, type discriminators (`art`, `programm_typ`, `axis`), and quantitative measurements (with `_alt`/`_vertrauensgrad` shadows).
- **Measurement placement.** Building-level → `:Fallbeispiel`. Component-group-level → `:Bauteilgruppe`. Inherently relational quantities → on the `BENUTZT` edge.
- **Role placement.** A role IS an edge property, never a node target. `:HAT {art:'akteur', rolle:'Architektur'}->(:Akteur)`. Vocab `:Akteurrolle` is a dictionary.
- **Citation placement.** Source attribution NEVER lives as a property. Always `:BELEGT_IN → :Quelle` with optional `eigenschaft` to scope.
- **Naming.** German PascalCase Labels, SCREAMING_SNAKE edges, snake_case properties.
- **Constraint.** Every Label has `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE`.

# Appendix B — Constraints & indexes

- UNIQUE id per Label.
- Range indexes on `:Fallbeispiel(art)`, `:Fallbeispiel(flaeche_m2)`, `:Fallbeispiel(fertigstellung_jahr)`, `:Bauteilgruppe(masse_t)`, `:Bauteilgruppe(co2_einsparung_kg)`, `:Akteur(art)`, `:Quelle(art)`.
- No full-text index (no body_md to index).

# Appendix C — Coverage checklist

The Labels in §1.A + §1.B + the drop/merge table in §1.C account for every folder under `_database/` (54 folders + `_edges` + `_system`).

YAML frontmatter fields on legacy `fallstudie` / `projekt` / `bauobjekt` / `reuse_einsatz` / `datenpunkt` / `akteur_beteiligung`:
- structural relations (`fallstudie:`, `projekt:`, `bauobjekt:`) → resolved or collapsed
- measurement fields (`wert:`, `einheit:`) → properties on `:Fallbeispiel` / `:Bauteilgruppe`
- canonical-axis fields (`bauteiltyp:`, `material:`, …) → IST / BENUTZT edges to vocab
- raw labels (`bauteil_label:`, `material_label:`, `pruefung_label:`, `huerde_label:`, …) → NOT in the graph; remain only in the source Markdown
- prose `body` → NOT in the graph
- `quelle_label:` → resolved to `:Quelle` nodes + `:BELEGT_IN` edges
- `legacy_paths:`, `build_status:` → NOT in the graph

# Appendix D — Renamings, drops, merges

| Change | Action |
|---|---|
| `fallstudie/` + `projekt/` + `bauobjekt/` (shared id) | merged into `:Fallbeispiel` with `art` property |
| `reuse_einsatz/` | renamed to `:Bauteilgruppe` |
| `reuse_kette/` | renamed to `:Wiederverwendungskette` (kept; optional grouping) |
| `reuse_kettenstation/` | dropped — stations become GEHÖRT_ZU edges from `:Bauteilgruppe` |
| `bewertungslogik_abgrenzung/` | renamed to `:WiederverwendungsArt`, absorbed values of dropped Bauteilgruppentyp via `axis` property |
| `foerderprogramm/` + `programm_kontext/` | merged into `:Programm` with `programm_typ` property |
| `akteur_beteiligung/` + `bauobjekt_beteiligung/` | dropped — role lives as edge property on `HAT` |
| `bauobjektklasse/` | dropped — values collapse into `:Fallbeispiel.art` |
| `bauobjektrolle/` | dropped — derivable from incoming GEHÖRT_ZU edges |
| `dokumenttyp/` | dropped — replaced by `:Quelle.art` (general values: Website / Interview / Paper / Buch / Bericht / Datenbank / Vortrag / Norm / Sonstige) |
| `tragwerkstyp/` | dropped — axis-mix; values folded into `:Material` or `:WiederverwendungsArt` |
| `kennwertdefinition/` | dropped — kennwert-names become property names |
| `datenpunkt/` | dropped — measurements become node properties |
| All `body_md`, `legacy_paths`, `build_status`, `title`, raw-label properties on any node | dropped — graph is metadata-only |
| `:BELEGT` (Quelle → claim) | reversed and renamed to `:BELEGT_IN` (claim → Quelle) |
| All `*_quelle`, `*_quellen`, `quelle_id`, `quelle_label_raw` properties anywhere | dropped — replaced exclusively by `:BELEGT_IN` edges |
| `Moebelsepearat` value in WiederverwendungsArt | renamed to `Moebel_separat` |
| `ort/Scwheiz` | renamed to `ort/Schweiz` |
| Bauteiltyp drop-and-remap (SCHEMA.md §5) | already applied — noted in spec |
| Material drop-and-merge (SCHEMA.md §6) | already applied — noted in spec |

---

## Final counts

- **6** instance Labels
- **37** vocabulary Labels
- **5** edge types
- **0** body / legacy / prose properties (metadata-only)

## Out of scope (this plan)

- Writing the export script.
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.
