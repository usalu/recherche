---
name: Neo4j schema catalogue
overview: Metadata-only Neo4j schema. The graph carries identifiers, classifications, measurements, and relationships — NOT German prose. **Each node has exactly one Label.** **`title`** is allowed **only** on **`(:Software)`** and **`(:Tool)`** (short display name, §1.E); otherwise `body_md` / `legacy_paths` / `build_status` / raw labels stay only in source Markdown. **44** Neo4j Labels total (**nine** primary types: **case/project record** `:Fallbeispiel`, **built work** `:Bauwerk`, component group, reuse action, actors, sources, **`:Software`** (platforms/apps), **`:Tool`** (modules/scripts), chains, plus **thirty-five** folder-backed classification types). **:Software** = vollständiges digitales Ökosystem/Plattform/Anwendung; **:Tool** = kleineres Modul/Plug-in/Skript/etc., **kein** Synonym für Software (§1.E). **Six** edge types (`IST`, `HAT`, `HAT_STATUS`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN`). **Deliverables:** `_database/_system/NEO4J_SCHEMA.md` + `_database/_system/NEO4J_SCHEMA_MAP.md`.
todos:

- id: spec-skeleton
content: "Create _database/_system/NEO4J_SCHEMA.md (full spec) and _database/_system/NEO4J_SCHEMA_MAP.md (compact map: all Labels + properties, all edge types + properties). Same 4+appendix content order in the main spec; the map is a flattened reference."
status: pending
- id: write-1
content: "Write §1 Node-type catalogue: all **44** Labels (nine primary + thirty-five folder-backed types), one-line purpose each. Confirm against _database/ folder list."
status: pending
- id: write-2
content: "Write §2 Nodes: per-Label property tables. ONLY metadata properties — no body, no legacy_paths, no raw labels, no build_status."
status: pending
- id: write-3
content: "Write §3 Edge-type catalogue: six edge types (IST, HAT, HAT_STATUS, BENUTZT, GEHÖRT_ZU, BELEGT_IN) with source/target Label families and the legacy relations folded into each."
status: pending
- id: write-4
content: "Write §4 Edges: per-edge-type property table. :BELEGT_IN is the only citation edge."
status: pending
- id: schema-map
content: "Write _database/_system/NEO4J_SCHEMA_MAP.md: (A) every Label with full property table, (B) every relationship type (six) with source/target Label patterns, cardinality, and full edge-property table. Mirror §2–§4; update whenever NEO4J_SCHEMA.md changes."
status: pending
- id: appendices
content: "Write the appendices: A modeling principles (metadata-only, hybrid modes), B constraints & indexes, C complete coverage checklist (every folder under _database/ accounted for), D renamings / drops / merges."
status: pending

---

# Goal

Author `_database/_system/NEO4J_SCHEMA.md` in the four-part order: §1 Node-type catalogue → §2 Nodes (properties) → §3 Edge-type catalogue → §4 Edges (properties). Plus appendices.

Author a **separate compact map** `[_database/_system/NEO4J_SCHEMA_MAP.md](_database/_system/NEO4J_SCHEMA_MAP.md)` that duplicates nothing narratively but **lists the full machine-oriented catalogue** in one place:

1. **Nodes:** every Neo4j **Label** (all **44** types), each with its **complete property list** (name, type, required, notes) as in §2.
2. **Edges:** every **relationship type** (all **six**), each with **allowed source Labels → target Labels**, cardinality, and **complete edge property list** (name, type, required, notes) as in §3–§4.

The map must stay **in lockstep** with `NEO4J_SCHEMA.md` when the schema changes. Optional later: generate the map from a single YAML/JSON source of truth — not required for the first authoring pass.

**Key principle: the graph carries metadata only.** German prose, raw labels, legacy file paths, build-batch status — none of this is in the graph. It stays in the Markdown source under `_database/`. The graph carries identifiers (ids), classifications (edges), and quantitative facts (measurement properties). **Exception:** **`title`** (and optional `url` / vendor fields) on **`(:Software)`** and **`(:Tool)`** only — see §1.E / §2.

---

# Hierarchiebaum — alle Knotentypen, Knoten, Eigenschaften; alle Kantentypen, Kanten, Eigenschaften

Lesen: **Knotentyp** = Neo4j-Label. **Knoten** = eine Instanz (ein Unterordner oder ein zusammengeführter Datensatz). **Knoteneigenschaften** = Properties auf diesem Knoten. **Kantentyp** = Relationship-Typ. **Kante** = eine konkrete Relationship zwischen zwei Knoten. **Kanteneigenschaften** = Properties auf der Kante.

Kontrollierte Begriffsknoten (z. B. `:Material`, `:Status`): jedes `id` entspricht in der Regel dem Unterordnernamen unter dem passenden `_database/<label>/<id>/` (Prosa nur in `index.md`, nicht im Graphen). Jeder solche Knoten hat **genau ein** Label — seinen Typnamen.

```
Neo4j_Schema
│
├── KNOTENTYP :Fallbeispiel
│   ├── Knoteneigenschaften (Fallstudien-/Projekt-Datensatz — **nicht** das physische Bauwerk)
│   │   ├── id: string (Pflicht, UNIQUE)
│   │   ├── art: string (Pflicht) — Fallstudie | Projekt | Fallstudie_Projekt (oder verbindliches Enum nach Export)
│   │   └── optional: studienjahr?, projektstart_jahr?, projektende_jahr?: int? (nur wenn aus Frontmatter belegt)
│   └── Knoten (Instanzen)
│       └── je ein Knoten pro zusammengeführter Fall-/Projekt-ID (`fallstudie/` + `projekt/` gleiche id)
│
├── KNOTENTYP :Bauwerk
│   ├── Knoteneigenschaften (physisches **Bauwerk** — bisherige Gebäude-/Anlagen-Semantik)
│   │   ├── id: string (Pflicht, UNIQUE)
│   │   ├── art: string (Pflicht) — Gebaeude | Bruecke | Pavillon | Halle | Lager | Innenausbau | Anlage
│   │   ├── flaeche_m2, projektflaeche_m2, gebaeudemasse_t: float? (optional)
│   │   ├── wohneinheiten, fertigstellung_jahr, entwurfsbeginn_jahr, bauzeit_monate, lebensdauer_jahre: int? (optional)
│   │   ├── restlebensdauer_jahre, kosten_eur, budget_eur, co2_footprint_kg, energieverbrauch_kwh_a, wassereinsparung_m3, bestandslager_m3: float? (optional)
│   │   └── je Messgröße optional: <name>_alt: list<float>?, <name>_vertrauensgrad: string?
│   └── Knoten (Instanzen)
│       └── je ein Knoten pro Legacy-`bauobjekt/<id>/` (oder abgeleitet aus Fallakte); **Verknüpfung** zum Datensatz: `GEHÖRT_ZU {rolle: 'fallbeispiel'}` → `:Fallbeispiel`
│
├── KNOTENTYP :Bauteilgruppe
│   ├── Knoteneigenschaften
│   │   ├── id: string (Pflicht, UNIQUE)
│   │   ├── masse_t, volumen_m3, flaeche_m2: float? (optional) — physische Größen der Elementgruppe
│   │   ├── anzahl_stueck: int? (optional)
│   │   ├── geerntete_materialien_t, sekundaere_materialien_t, abfall_vermieden_t: float? (optional)
│   │   └── je Messgröße optional: <name>_alt, <name>_vertrauensgrad (wie :Bauwerk)
│   └── Knoten (Instanzen)
│       └── je ein Knoten pro `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` (siehe §1 ID-Konvention `:Bauteilgruppe`) — **nur** die physische Elementgruppe
│
├── KNOTENTYP :ReuseEinsatz
│   ├── Knoteneigenschaften
│   │   ├── id: string (Pflicht, UNIQUE) — Slug wie Legacy-`reuse_einsatz/<id>/` oder gleiches `<CASE>_C<NN>_<ELEMENT>`-Muster nach Export-Konvention §1
│   │   ├── anteil_prozent, co2_einsparung_kg, co2_reduktion_kg, zielwert_reuse_prozent: float? (optional) — am **Einsatz** gemessene / berichtete Wirkung
│   │   └── je Messgröße optional: <name>_alt, <name>_vertrauensgrad (wie :Bauwerk)
│
├── KNOTENTYP :Akteur
│   ├── Knoteneigenschaften: id (Pflicht), art? (string), url? (string)
│   └── Knoten: je ./_database/akteur/<id>/
│
├── KNOTENTYP :Quelle
│   ├── Knoteneigenschaften: id (Pflicht), art (Pflicht: Website|Interview|Paper|Buch|Bericht|Datenbank|Vortrag|Norm|Sonstige), url? (string)
│   └── Knoten: je Quelle (Ordner oder fallgebundene abgeleitete id)
│
├── KNOTENTYP :Software
│   ├── Knoteneigenschaften: id (Pflicht), title (Pflicht), softwaretyp? (enum §1.E), anbieter? (string), url? (string)
│   └── Knoten: aus `software_digitaltool/` **nur** als **Plattform/Anwendung** klassifizierte Einträge + neu angelegte Software-Knoten (§1.E)
├── KNOTENTYP :Tool
│   ├── Knoteneigenschaften: id (Pflicht), title (Pflicht), tooltyp? (enum §1.E), funktion? (string), version? (string)
│   └── Knoten: Add-ins/Skripte/Rechner/… aus `software_digitaltool/` oder eigener Import; optional `GEHÖRT_ZU {rolle: software}` → `:Software` (§1.E)
│
├── KNOTENTYP :Wiederverwendungskette
│   ├── Knoteneigenschaften: id (Pflicht), start_jahr?, end_jahr? (int)
│   └── Knoten: je ./_database/reuse_kette/<id>/ (umbenanntes Konzept)
│
├── KNOTENTYP :Bauteiltyp
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausbau, Boden, Dach, Daemmung, Decke, Fassade, Fenster, Fundament, Gelaender, Stuetze, Technik, Traeger, Treppe, Tuer, Wand
├── KNOTENTYP :Material
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aluminium, Beton, Daemmstoff, Glas, Gusseisen, Holz, Keramik, Kunststoff, Lehm, Naturstein, Recyclingbeton, Stahl, Stahlbeton, Stroh, Ziegel
├── KNOTENTYP :Bauteilebene
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteilgruppe, Einzelbauteil, Gebaeudeteil, Materialcharge, Oberflaechenschicht, System
├── KNOTENTYP :Bauteilzustand
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Beschaedigt, Geprueft, Intakt, Kontaminiert, Korrodiert, Patiniert, Restlebensdauer_Bekannt, Restlebensdauer_Unklar, Ungeprueft
├── KNOTENTYP :Funktionswechsel
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Dekorative_Funktion, Gleiche_Funktion, Konstruktive_Funktion, Neue_Funktion, Technische_Funktion, Unbekannt
├── KNOTENTYP :Verbindungstechnik
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Geschraubt, Geschweisst, Gesteckt, Geklebt, Vergossen, Klemmverbindung
├── KNOTENTYP :Bauweise
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fertigteilbauweise, Holzbauweise, Hybridbauweise, Massivbauweise, Ortbetonbauweise, Stahlbauweise
├── KNOTENTYP :Bausystem
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Betonfertigteil_System, Holzrahmenbau, Holz_Skelettbau, Plattenbau, Stahl_Skelettbau
├── KNOTENTYP :Tragwerksprinzip
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fachwerk, Skeletttragwerk, Wandtragwerk, Wand_Kern_Tragwerk
├── KNOTENTYP :Reversibilitaet
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Reversibel, Teilweise_reversibel, Irreversibel, Unbekannt
├── KNOTENTYP :Status
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Geplant, In_Bau, Realisiert, Prototyp, Rueckgebaut, Nicht_Realisiert, Unklar
├── KNOTENTYP :WiederverwendungsArt
│   ├── Knoteneigenschaften: id (Pflicht), axis (Pflicht: einordnung | grundtyp | reuse_strategie)
│   └── Knoten: sieben `einordnung` + drei `grundtyp` + sechs `reuse_strategie` (Kanon-`id`s §1 / Appendix E); Anbindung **Art der Wiederverwendung** an Fall/**Einsatz** nur per **`HAT { art: 'wiederverwendungsart' }`**, nicht als eigener Kantentyp
├── KNOTENTYP :Ressourcenquelle
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Baustelle, Bauteilboerse, Donorgebaeude, Donor_Infrastruktur, Haendler, Lager, Materialstockpile, Produktionsueberschuss, Unbekannt
├── KNOTENTYP :Beschaffungsweg
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausschreibung, Bauteilboerse, Digitale_Plattform, Direktvermittlung, Eigenbestand, Informelles_Netzwerk, Rueckbauprojekt, Spende
├── KNOTENTYP :Prozessphase
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aufbereitung, Betrieb, Dokumentation, Identifikation, Lagerung, Planung, Pruefung, Rueckbau, Transport, Wiedereinbau
├── KNOTENTYP :Rueckbauverfahren
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Ausbau_von_Bauteilen, Betonfraesen, Demontage, Selektiver_Rueckbau, Zerstoerungsarme_Bergung
├── KNOTENTYP :Aufbereitungsverfahren
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Drahtglasschneiden, Entmoertelung_von_Fliesen, Holzaufbereitung, Leuchten_Refurbishment, Qualitaetssicherung, Reinigung, Rekonditionierung, Remanufacturing, Reparatur, Verstaerkung, Zuschnitt
├── KNOTENTYP :Logistik
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteiltracking, Just_in_Time, Lagerflaeche, Lagerung, Lokale_Wiederverwendung, Materialmatching, Materialverfuegbarkeit, Transport, Transportdistanz, Zwischenlagerung
├── KNOTENTYP :Methode
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Abrissmonitoring, Bauteilkatalogisierung, Building_Material_Scouting, Design_for_Disassembly, Form_Follows_Availability, Materialinventur, Pre_Deconstruction_Audit, ReUse_Assessment, ReUse_Ausschreibung, Reversibilitaet, Urban_Mining, Wiederverwendungskriterien, Zirkulaere_Ausschreibung
├── KNOTENTYP :Huerde
│   ├── Knoteneigenschaften: id (Pflicht), kategorie? (string) — für Stoff-Stammdaten aus **`schadstoff/`**: `kategorie: "Schadstoff"` (Pflicht bei diesem Import); für `huerde/`-Allgemeinhürden weglassen oder anderes Enum nach Export
│   └── Knoten: Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit, Schadstoffbelastung, Technische_Freigabe, Terminunsicherheit, Toleranzen, Unkonventionelles_Material, Verfuegbarkeitsproblem, Witterung_Feuchte, Zustand_Unklar (Ordner `huerde/`) **sowie** Asbest, Bleifarbe, Holzschutzmittel, PAK, PCB (Ordner `schadstoff/` — jeweils **`kategorie: "Schadstoff"`**)
├── KNOTENTYP :PruefungNachweis
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Abbrandbemessung, Brandschutznachweis, Eignungspruefung_Baulehm, Geometrische_Vermessung, Materialpruefung, Schadstoffscreening, Schweissbarkeitspruefung, Sichtpruefung, Statische_Nachweisfuehrung, Zugversuch, Zustandsbewertung
├── KNOTENTYP :Leistungsanforderung
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Brandschutz, Brandschutzanforderung, Dauerhaftigkeit, F90, Feuchteschutz, Feuerwiderstand, R90, REI90, Rueckbaubarkeit, Schadstofffreiheit, Schallschutz, Tragfaehigkeit, Waermeschutz
├── KNOTENTYP :Norm
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: DIN_18940, DIN_EN_15804, DIN_EN_15978, EN_1090, ISO_14040, ISO_14044, ISO_20887
├── KNOTENTYP :RechtlicheBedingung
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauordnungsrecht, EU_Taxonomie, Gewaehrleistung, Produkthaftung, Vergaberecht, Zulassung_im_Einzelfall
├── KNOTENTYP :Nutzung
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Buero, Gewerbe, Infrastruktur, Kultur, Lager_Depot, Mischnutzung, Schule_Bildung, Sozialbau, Wohnen
├── KNOTENTYP :BauaufgabeIntervention
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aufstockung, Erweiterung, Fit_out, Neubau, Rueckbau, Sanierung, Translozierung, Umbau, Umnutzung, Wiederaufbau
├── KNOTENTYP :Entwurfsentscheidung
│   ├── Knoteneigenschaften: id (Pflicht), beschreibung? (string)
│   └── Knoten: Etagenhoehe_durch_Bauteilmass, Fassadenschicht_als_Toleranzpuffer, Doppelfenster_als_Kastenfenster, Achsraster_nach_Bestand, Grundriss_nach_Bauteillaenge, Deckenhoehe_nach_Traegerhoehe, Anschlussdetail_angepasst, Erschliessungskern_verschoben
├── KNOTENTYP :Land
│   ├── Knoteneigenschaften: id (Pflicht), iso_country? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
├── KNOTENTYP :Stadt
│   ├── Knoteneigenschaften: id (Pflicht), koordinaten? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
├── KNOTENTYP :Akteurrolle (nur Wörterbuch; Rolle als Property auf HAT, nicht als IST-Ziel — **acht** kanonische Knoten; Legacy-`akteurrolle/*`-Ordner **nicht** 1:1, siehe §1.D)
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauherrschaft_Nutzung, Planung_Gestaltung, Tragwerk_Fassade, TGA_Sicherheit, Ausfuehrung_Logistik, Beratung_Forschung, Qualitaetssicherung, Koordination
├── KNOTENTYP :Datenqualitaet
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Belegt, Geschaetzt, Nicht_Belegt, Primaerquelle, Sekundaerquelle, Unbekannt, Widerspruechlich
├── KNOTENTYP :Datenmodell
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteil_ID, IFC, Klassifikation, Materialdatenbank, Materialpass_Schema, Ontologie, Taxonomie
├── KNOTENTYP :Tooltyp
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bauteilboerse, Materialdatenbank, Materialkataster
├── KNOTENTYP :ZertifizierungBewertungssystem
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: BREEAM, DGNB, LEED, Paris_Proof, WELL
├── KNOTENTYP :Wirtschaft
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Finanzierung, Geschaeftsmodell, Kostenvergleich, Lebenszykluskosten, Preisbildung, Restwert
└── KNOTENTYP :Programm
    ├── Knoteneigenschaften: id (Pflicht), programm_typ (Pflicht: foerderung | forschungskontext)
    └── Knoten: BBSM, FCRBE, PREUSE, Reallabor_Be_Ware, Zukunftbau, Foerderprogramm, Forschungsprojekt, Kommunales_Programm, Pilotprojekt (auch Provenienz **`kontextmerkmal/Pilotprojekt`** — **ein** Kanon-Knoten), Reallabor, Wettbewerb

KANTEN (alle sechs Typen; jede Kante ist eine Instanz zwischen zwei Knoten)

├── KANTENTYP IST
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung?
│   └── Kante (Beispielmuster)
│       └── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz|:Akteur|:Quelle|:Software|:Tool|:Wiederverwendungskette) -[IST]-> (:<KlassifikationsLabel> {id})   (nicht :Status — siehe HAT_STATUS; nicht :WiederverwendungsArt mit axis reuse_strategie auf :Fallbeispiel|:ReuseEinsatz|:Bauwerk — siehe HAT mit art=wiederverwendungsart)
│
├── KANTENTYP HAT
│   ├── Kanteneigenschaften: art (Pflicht), rolle? (Pflicht wenn art=akteur), anzahl?, intensitaet?, seit?, bis?
│   └── Kante (Beispielmuster)
│       ├── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz) -[HAT {art: huerde|prozessphase|pruefung|norm|…}]-> (:Huerde|:Prozessphase|:Norm|…)
│       ├── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz) -[HAT {art: verbindungstechnik}]-> (:Verbindungstechnik)
│       ├── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz) -[HAT {art: reversibilitaet}]-> (:Reversibilitaet)
│       ├── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz) -[HAT {art: akteur, rolle: "<Kanon_Akteurrolle.id>"}]-> (:Akteur)   `rolle` = **eine** der **acht** IDs aus §1.D (nicht Roh-Ordnername)
│       ├── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz) -[HAT {art: entwurf}]-> (:Entwurfsentscheidung)
│       └── (:Fallbeispiel|:Bauwerk|:ReuseEinsatz) -[HAT {art: wiederverwendungsart}]-> (:WiederverwendungsArt {id, axis: "reuse_strategie"})   *Art der Wiederverwendung* — Fallakte / **Bauwerk** / **Einsatz** (sechs Kanon-`id`s §1). Beispiel: (:ReuseEinsatz)-[:HAT {art: "wiederverwendungsart"}]->(:WiederverwendungsArt {id: "Umnutzung_Repurposing", axis: "reuse_strategie"})
│
├── KANTENTYP HAT_STATUS
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung? (optional — gleiche Semantik wie bei IST)
│   └── Kante (Beispielmuster)
│       └── (:Bauwerk|:ReuseEinsatz|:Fallbeispiel|:Bauteilgruppe) -[HAT_STATUS]-> (:Status {id})   **Gebäude-/Anlagen-Lebenszyklus** → :Bauwerk (kanonisch für `bauobjektstatus/`); **Einsatz** → :ReuseEinsatz; **Fall-/Projekt-Ebene** → :Fallbeispiel (optional); :Bauteilgruppe nur Legacy. Beispiel: (:Bauwerk)-[:HAT_STATUS]->(:Status {id: "Realisiert"})
│
├── KANTENTYP BENUTZT
│   ├── Kanteneigenschaften: anzahl?, einheit?, anteil_prozent?, funktion_alt?, funktion_neu?, aufbereitung?
│   └── Kante (Beispielmuster)
│       └── (:Bauteilgruppe|:ReuseEinsatz|:Bauwerk|:Fallbeispiel) -[BENUTZT]-> (:Material|:Methode|:Rueckbauverfahren|:Aufbereitungsverfahren|:Software|:Tool|:Datenmodell)
│
├── KANTENTYP GEHÖRT_ZU
│   ├── Kanteneigenschaften: rolle (Pflicht), position?, seit?, bis?
│   └── Kante (Beispielmuster)
│       ├── (:Bauwerk) -[GEHÖRT_ZU {rolle: fallbeispiel}]-> (:Fallbeispiel)   welches **Bauwerk** zu welchem Fall-/Projekt-Datensatz gehört
│       ├── (:ReuseEinsatz) -[GEHÖRT_ZU {rolle: bauteilgruppe}]-> (:Bauteilgruppe)   welche physische Gruppe dieser Einsatz betrifft
│       ├── (:ReuseEinsatz) -[GEHÖRT_ZU {rolle: einbauort|herkunft|zwischenlager|verarbeitung|transport}]-> (:Bauwerk)   logischer Ort / Strom der Aktion am **Bauwerk**
│       ├── (:Bauteilgruppe) -[GEHÖRT_ZU {rolle: einbauort|herkunft|zwischenlager|verarbeitung|transport}]-> (:Bauwerk)   räumliche/logische Zuordnung der **physischen** Gruppe zum **Bauwerk**
│       ├── (:Bauteilgruppe|:ReuseEinsatz) -[GEHÖRT_ZU {rolle: kette, position}]-> (:Wiederverwendungskette)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: land}]-> (:Land)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: stadt}]-> (:Stadt)
│       ├── (:Bauwerk) -[GEHÖRT_ZU {rolle: land}]-> (:Land)   optional — Standort des Bauwerks
│       ├── (:Bauwerk) -[GEHÖRT_ZU {rolle: stadt}]-> (:Stadt)   optional
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: programm}]-> (:Programm)
│       ├── (:Software|:Tool) -[GEHÖRT_ZU {rolle: programm}]-> (:Programm)   optional — z. B. **Pilotprojekt** (Legacy `kontextmerkmal/`)
│       ├── (:Tool) -[GEHÖRT_ZU {rolle: software}]-> (:Software)   Modul/Plug-in/Skript gehört zu Host-**Plattform** / Ökosystem (optional)
│       └── (weitere) je nach Export-Regeln
│
└── KANTENTYP BELEGT_IN
    ├── Kanteneigenschaften: eigenschaft?, seite?, excerpt?, raw_label?
    └── Kante (Beispielmuster)
        └── (:Fallbeispiel|:Bauwerk|:Bauteilgruppe|:ReuseEinsatz|…) -[BELEGT_IN]-> (:Quelle)
```

Hinweis: Ordner ohne eigenen Knotentyp (z. B. `datenpunkt/`, `kennwertdefinition/`) sind in §1.C des Plans aufgeführt — sie erzeugen **keine** eigenen Knoten im Zielgraphen, sondern fließen in Properties, Kanten oder Merges ein. **`fallstudie/`** und **`projekt/`** → **`:Fallbeispiel`**; **`bauobjekt/`** → **`:Bauwerk`** (mit `GEHÖRT_ZU` zum zugehörigen `:Fallbeispiel`).

## Autoritativer vertikaler Gesamtbaum — Knoten (Node Types + Nodes + Properties)

Diese Liste ist die gewünschte Zielform für die finale Schema-Datei: **ein Knotentyp, darunter jeder Knoten einzeln vertikal, mit seinen Properties direkt daneben**. Keine horizontalen Kommalisten in der finalen Fassung.

Format-Regel (wichtig für die Lesbarkeit): Jede Zeile, die mit `(:<Label>` beginnt, definiert **genau einen** Knoten. Diese Zeile enthält alle Knoten-Properties **im selben Zeilen-Block** (keine zweizeiligen Node-Definitionen). Die Properties stehen als genau ein `{...}`-Block (z. B. `{id: "Stahl", axis: "grundtyp"}`). **Alle `id`-Werte** folgen zusätzlich der Tabelle **„ID- und Namenskonvention (Lesbarkeit)“** in §1 (ASCII, keine Listenzeichen, keine `__`-Monster-Slugs).

Die folgenden Blöcke zeigen **Muster** (nicht die vollständige Knotenzahl). Die endgültige Exportliste folgt §1 **ID- und Namenskonvention (Lesbarkeit)**.

```text
:Fallbeispiel
  (:Fallbeispiel {id: "Berlin_Schildow_Pilot_Haus", art: "Fallstudie_Projekt"})
  (:Fallbeispiel {id: "55_Great_Suffolk_Street_London", art: "Projekt"})
  (:Fallbeispiel {id: "K118_Halle_118_Winterthur", art: "Fallstudie"})
  (:Fallbeispiel {id: "AWM_Muenster_Circular_Office", art: "Fallstudie_Projekt"})
  ... (Fall-/Projekt-Datensatz: ASCII-Slug; **kein** `art: Gebaeude` mehr — das liegt auf `:Bauwerk`)

:Bauwerk
  (:Bauwerk {id: "Berlin_Schildow_Pilot_Haus_Gebaeude", art: "Gebaeude"})
  (:Bauwerk {id: "55_Great_Suffolk_Street_London_Lager", art: "Lager"})
  (:Bauwerk {id: "K118_Halle_118_Winterthur", art: "Halle"})
  (:Bauwerk {id: "AWM_Muenster_Circular_Office", art: "Innenausbau"})
  ... (physisches Bauwerk; `id` oft aus Legacy `bauobjekt/` oder abgeleitet; `GEHÖRT_ZU {rolle: 'fallbeispiel'}` → zugehöriges `(:Fallbeispiel)`)

:Bauteilgruppe
  (:Bauteilgruppe {id: "K118_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "K118_C02_Treppe"})
  (:Bauteilgruppe {id: "ELYS_C01_Fenster"})
  (:Bauteilgruppe {id: "Plattenpalast_C01_Wandplatten"})
  (:Bauteilgruppe {id: "55GSS_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "CRCLR_C02_Wandpaneele"})
  (:Bauteilgruppe {id: "Werkhof29_C01_Fassadenbleche"})
  ... (Muster `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` — Graph-`id` = Ordner-Slug)

:ReuseEinsatz
  (:ReuseEinsatz {id: "K118_C01_Traeger_Stuetzen"})
  (:ReuseEinsatz {id: "K118_C02_Treppe"})
  ... (je `_database/reuse_einsatz/<id>/` **oder** gleicher Slug wie zugehörige `:Bauteilgruppe`, wenn 1:1 materialisiert — Graph-`id` = Export-Slug §1)

:Akteur
  (:Akteur {id: "Circular_Berlin"})
  (:Akteur {id: "Circular_Structural_Design"})
  (:Akteur {id: "Bellastock"})
  (:Akteur {id: "Arup"})
  (:Akteur {id: "Dirk_Hebel"})
  (:Akteur {id: "Bauteilboerse_Hannover"})
  (:Akteur {id: "Bauteilboerse_Bremen"})
  ... (eine Organisation oder Person pro Knoten — keine `A;B,C`-Listen in `id`; **Bauteilbörse** als Konzept-Knoten → **`id: "Bauteilboerse"`** auf `:Ressourcenquelle` / `:Beschaffungsweg` / `:Tooltyp`, siehe §1 ID-Tabelle)

:Quelle
  (:Quelle {id: "BBSR_Zukunft_Bau_foerderprogramm", art: "Website"})
  (:Quelle {id: "Circular_Berlin_marktstudie_wiederverwendung", art: "Bericht"})
  (:Quelle {id: "Bellastock_research_note", art: "Paper"})
  ... (kurze Zitations-Slugs — nicht `akteur_04_..._md` oder Roh-Dateinamen)

:Software
  (:Software {id: "Madaster", title: "Madaster", softwaretyp: "Materialdatenbank"})
  (:Software {id: "Concular", title: "Concular", softwaretyp: "Bauteilplattform"})
  (:Software {id: "Restado", title: "Restado"})
  (:Software {id: "Loopfront", title: "Loopfront"})
  (:Software {id: "Revit", title: "Autodesk Revit", softwaretyp: "CAD"})
  (:Software {id: "Rhino", title: "Rhino", softwaretyp: "CAD"})
  (:Software {id: "OneClickLCA", title: "One Click LCA", softwaretyp: "LCA_Software"})
  (:Software {id: "Excel", title: "Microsoft Excel", softwaretyp: "Tabellenkalkulation"})
  (:Software {id: "QGIS", title: "QGIS", softwaretyp: "GIS"})
  ... (vollständige **Plattform/Anwendung**; `title` = Kurzname; `softwaretyp` optional enum §1.E)

:Tool
  (:Tool {id: "Grasshopper_Material_Matching_Skript", title: "Grasshopper-Skript Material-Matching", tooltyp: "Skript", funktion: "Matching"})
  (:Tool {id: "Revit_Materialpass_Plugin", title: "Revit-Materialpass-Plug-in", tooltyp: "Plugin"})
  (:Tool {id: "CO2_Rechner_Spreadsheet", title: "CO2-Rechner (Tabellenblatt)", tooltyp: "Rechner"})
  (:Tool {id: "CSV_Import_Skript", title: "CSV-Import-Skript", tooltyp: "Skript"})
  (:Tool {id: "API_Connector", title: "API-Connector", tooltyp: "API"})
  (:Tool {id: "Material_Matching_Algorithmus", title: "Material-Matching-Algorithmus", tooltyp: "Modul"})
  ... (kleineres **Modul/Feature/Skript** — **kein** Synonym für `:Software`; optional `GEHÖRT_ZU {rolle: software}` → Host-`:Software`)

:Wiederverwendungskette
  (:Wiederverwendungskette {id: "55_Great_Suffolk_Street_London"})
  (:Wiederverwendungskette {id: "K118_Halle_118_Winterthur"})
  (:Wiederverwendungskette {id: "House_of_Fraser_Oxford_Street_London_reuse_chain"})
  ... (typisch an **Fallakte** `(:Fallbeispiel)` oder zugehöriges **Bauwerk** gebunden; gleiches Kurz-Muster wie `(:Fallbeispiel {id:…})` wenn 1:1)

:Bauteiltyp
  (:Bauteiltyp {id: "Ausbau"})
  (:Bauteiltyp {id: "Boden"})
  (:Bauteiltyp {id: "Dach"})
  (:Bauteiltyp {id: "Daemmung"})
  (:Bauteiltyp {id: "Decke"})
  (:Bauteiltyp {id: "Fassade"})
  (:Bauteiltyp {id: "Fenster"})
  (:Bauteiltyp {id: "Fundament"})
  (:Bauteiltyp {id: "Gelaender"})
  (:Bauteiltyp {id: "Stuetze"})
  (:Bauteiltyp {id: "Technik"})
  (:Bauteiltyp {id: "Traeger"})
  (:Bauteiltyp {id: "Treppe"})
  (:Bauteiltyp {id: "Tuer"})
  (:Bauteiltyp {id: "Wand"})

:Material
  (:Material {id: "Aluminium"})
  (:Material {id: "Beton"})
  (:Material {id: "Daemmstoff"})
  (:Material {id: "Glas"})
  (:Material {id: "Gusseisen"})
  (:Material {id: "Holz"})
  (:Material {id: "Keramik"})
  (:Material {id: "Kunststoff"})
  (:Material {id: "Lehm"})
  (:Material {id: "Naturstein"})
  (:Material {id: "Recyclingbeton"})
  (:Material {id: "Stahl"})
  (:Material {id: "Stahlbeton"})
  (:Material {id: "Stroh"})
  (:Material {id: "Ziegel"})

:Bauteilebene
  (:Bauteilebene {id: "Bauteilgruppe"})
  (:Bauteilebene {id: "Einzelbauteil"})
  (:Bauteilebene {id: "Gebaeudeteil"})
  (:Bauteilebene {id: "Materialcharge"})
  (:Bauteilebene {id: "Oberflaechenschicht"})
  (:Bauteilebene {id: "System"})

:Bauteilzustand
  (:Bauteilzustand {id: "Beschaedigt"})
  (:Bauteilzustand {id: "Geprueft"})
  (:Bauteilzustand {id: "Intakt"})
  (:Bauteilzustand {id: "Kontaminiert"})
  (:Bauteilzustand {id: "Korrodiert"})
  (:Bauteilzustand {id: "Patiniert"})
  (:Bauteilzustand {id: "Restlebensdauer_Bekannt"})
  (:Bauteilzustand {id: "Restlebensdauer_Unklar"})
  (:Bauteilzustand {id: "Ungeprueft"})

:Funktionswechsel
  (:Funktionswechsel {id: "Dekorative_Funktion"})
  (:Funktionswechsel {id: "Gleiche_Funktion"})
  (:Funktionswechsel {id: "Konstruktive_Funktion"})
  (:Funktionswechsel {id: "Neue_Funktion"})
  (:Funktionswechsel {id: "Technische_Funktion"})
  (:Funktionswechsel {id: "Unbekannt"})

:Verbindungstechnik
  (:Verbindungstechnik {id: "Geschraubt"})
  (:Verbindungstechnik {id: "Geschweisst"})
  (:Verbindungstechnik {id: "Gesteckt"})
  (:Verbindungstechnik {id: "Geklebt"})
  (:Verbindungstechnik {id: "Vergossen"})
  (:Verbindungstechnik {id: "Klemmverbindung"})

:Bauweise
  (:Bauweise {id: "Fertigteilbauweise"})
  (:Bauweise {id: "Holzbauweise"})
  (:Bauweise {id: "Hybridbauweise"})
  (:Bauweise {id: "Massivbauweise"})
  (:Bauweise {id: "Ortbetonbauweise"})
  (:Bauweise {id: "Stahlbauweise"})

:Bausystem
  (:Bausystem {id: "Betonfertigteil_System"})
  (:Bausystem {id: "Holzrahmenbau"})
  (:Bausystem {id: "Holz_Skelettbau"})
  (:Bausystem {id: "Plattenbau"})
  (:Bausystem {id: "Stahl_Skelettbau"})

:Tragwerksprinzip
  (:Tragwerksprinzip {id: "Fachwerk"})
  (:Tragwerksprinzip {id: "Skeletttragwerk"})
  (:Tragwerksprinzip {id: "Wandtragwerk"})
  (:Tragwerksprinzip {id: "Wand_Kern_Tragwerk"})

:Reversibilitaet
  (:Reversibilitaet {id: "Reversibel"})
  (:Reversibilitaet {id: "Teilweise_reversibel"})
  (:Reversibilitaet {id: "Irreversibel"})
  (:Reversibilitaet {id: "Unbekannt"})

:Status
  (:Status {id: "Geplant"})
  (:Status {id: "In_Bau"})
  (:Status {id: "Realisiert"})
  (:Status {id: "Prototyp"})
  (:Status {id: "Rueckgebaut"})
  (:Status {id: "Nicht_Realisiert"})
  (:Status {id: "Unklar"})

:WiederverwendungsArt
  (:WiederverwendungsArt {id: "Bestandserhalt_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Kein_Direct_Reuse_Nachweis", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Moebel_Dekoration_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Recycling_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Reuse_Anteil_Unklar", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Ungebaut_Nicht_Realisierte_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt {id: "Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt {id: "wiederverwendet", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "original", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "hybrid", axis: "grundtyp"})
  (:WiederverwendungsArt {id: "Bestandserhalt_Weiterbauen", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "In_situ_Wiederverwendung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Direkte_Wiederverwendung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Wiederverwendung_nach_Aufarbeitung", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Umnutzung_Repurposing", axis: "reuse_strategie"})
  (:WiederverwendungsArt {id: "Kaskade_Downcycling_Bauteilebene", axis: "reuse_strategie"})

:Ressourcenquelle
  (:Ressourcenquelle {id: "Baustelle"})
  (:Ressourcenquelle {id: "Bauteilboerse"})
  (:Ressourcenquelle {id: "Donorgebaeude"})
  (:Ressourcenquelle {id: "Donor_Infrastruktur"})
  (:Ressourcenquelle {id: "Haendler"})
  (:Ressourcenquelle {id: "Lager"})
  (:Ressourcenquelle {id: "Materialstockpile"})
  (:Ressourcenquelle {id: "Produktionsueberschuss"})
  (:Ressourcenquelle {id: "Unbekannt"})

:Beschaffungsweg
  (:Beschaffungsweg {id: "Ausschreibung"})
  (:Beschaffungsweg {id: "Bauteilboerse"})
  (:Beschaffungsweg {id: "Digitale_Plattform"})
  (:Beschaffungsweg {id: "Direktvermittlung"})
  (:Beschaffungsweg {id: "Eigenbestand"})
  (:Beschaffungsweg {id: "Informelles_Netzwerk"})
  (:Beschaffungsweg {id: "Rueckbauprojekt"})
  (:Beschaffungsweg {id: "Spende"})

:Prozessphase
  (:Prozessphase {id: "Aufbereitung"})
  (:Prozessphase {id: "Betrieb"})
  (:Prozessphase {id: "Dokumentation"})
  (:Prozessphase {id: "Identifikation"})
  (:Prozessphase {id: "Lagerung"})
  (:Prozessphase {id: "Planung"})
  (:Prozessphase {id: "Pruefung"})
  (:Prozessphase {id: "Rueckbau"})
  (:Prozessphase {id: "Transport"})
  (:Prozessphase {id: "Wiedereinbau"})

:Rueckbauverfahren
  (:Rueckbauverfahren {id: "Ausbau_von_Bauteilen"})
  (:Rueckbauverfahren {id: "Betonfraesen"})
  (:Rueckbauverfahren {id: "Demontage"})
  (:Rueckbauverfahren {id: "Selektiver_Rueckbau"})
  (:Rueckbauverfahren {id: "Zerstoerungsarme_Bergung"})

:Aufbereitungsverfahren
  (:Aufbereitungsverfahren {id: "Drahtglasschneiden"})
  (:Aufbereitungsverfahren {id: "Entmoertelung_von_Fliesen"})
  (:Aufbereitungsverfahren {id: "Holzaufbereitung"})
  (:Aufbereitungsverfahren {id: "Leuchten_Refurbishment"})
  (:Aufbereitungsverfahren {id: "Qualitaetssicherung"})
  (:Aufbereitungsverfahren {id: "Reinigung"})
  (:Aufbereitungsverfahren {id: "Rekonditionierung"})
  (:Aufbereitungsverfahren {id: "Remanufacturing"})
  (:Aufbereitungsverfahren {id: "Reparatur"})
  (:Aufbereitungsverfahren {id: "Verstaerkung"})
  (:Aufbereitungsverfahren {id: "Zuschnitt"})

:Logistik
  (:Logistik {id: "Bauteiltracking"})
  (:Logistik {id: "Just_in_Time"})
  (:Logistik {id: "Lagerflaeche"})
  (:Logistik {id: "Lagerung"})
  (:Logistik {id: "Lokale_Wiederverwendung"})
  (:Logistik {id: "Materialmatching"})
  (:Logistik {id: "Materialverfuegbarkeit"})
  (:Logistik {id: "Transport"})
  (:Logistik {id: "Transportdistanz"})
  (:Logistik {id: "Zwischenlagerung"})

:Methode
  (:Methode {id: "Abrissmonitoring"})
  (:Methode {id: "Bauteilkatalogisierung"})
  (:Methode {id: "Building_Material_Scouting"})
  (:Methode {id: "Design_for_Disassembly"})
  (:Methode {id: "Form_Follows_Availability"})
  (:Methode {id: "Materialinventur"})
  (:Methode {id: "Pre_Deconstruction_Audit"})
  (:Methode {id: "ReUse_Assessment"})
  (:Methode {id: "ReUse_Ausschreibung"})
  (:Methode {id: "Reversibilitaet"})
  (:Methode {id: "Urban_Mining"})
  (:Methode {id: "Wiederverwendungskriterien"})
  (:Methode {id: "Zirkulaere_Ausschreibung"})

:Huerde
  (:Huerde {id: "Akzeptanzproblem"})
  (:Huerde {id: "Anschlussproblem"})
  (:Huerde {id: "Aufbereitungsaufwand"})
  (:Huerde {id: "Ausschreibungsproblem"})
  (:Huerde {id: "Bauproduktstatus"})
  (:Huerde {id: "Brandschutzkonflikt"})
  (:Huerde {id: "Bruch_Beschaedigungsrisiko"})
  (:Huerde {id: "Datenluecke"})
  (:Huerde {id: "Dauerhaftigkeit_Restlebensdauer"})
  (:Huerde {id: "Entwurfsbindung"})
  (:Huerde {id: "Fehlende_Datenstandards"})
  (:Huerde {id: "Fehlende_Lagerflaeche"})
  (:Huerde {id: "Fehlende_Standardisierung"})
  (:Huerde {id: "Gewaehrleistung"})
  (:Huerde {id: "Haftung"})
  (:Huerde {id: "Heterogenitaet_Chargen"})
  (:Huerde {id: "Hygieneanforderung"})
  (:Huerde {id: "Kompatibilitaetsproblem"})
  (:Huerde {id: "Materialqualitaet_Unklar"})
  (:Huerde {id: "Mengenunsicherheit"})
  (:Huerde {id: "Schadstoffbelastung"})
  (:Huerde {id: "Technische_Freigabe"})
  (:Huerde {id: "Terminunsicherheit"})
  (:Huerde {id: "Toleranzen"})
  (:Huerde {id: "Unkonventionelles_Material"})
  (:Huerde {id: "Verfuegbarkeitsproblem"})
  (:Huerde {id: "Witterung_Feuchte"})
  (:Huerde {id: "Zustand_Unklar"})
  (:Huerde {id: "Asbest", kategorie: "Schadstoff"})
  (:Huerde {id: "Bleifarbe", kategorie: "Schadstoff"})
  (:Huerde {id: "Holzschutzmittel", kategorie: "Schadstoff"})
  (:Huerde {id: "PAK", kategorie: "Schadstoff"})
  (:Huerde {id: "PCB", kategorie: "Schadstoff"})

:PruefungNachweis
  (:PruefungNachweis {id: "Abbrandbemessung"})
  (:PruefungNachweis {id: "Brandschutznachweis"})
  (:PruefungNachweis {id: "Eignungspruefung_Baulehm"})
  (:PruefungNachweis {id: "Geometrische_Vermessung"})
  (:PruefungNachweis {id: "Materialpruefung"})
  (:PruefungNachweis {id: "Schadstoffscreening"})
  (:PruefungNachweis {id: "Schweissbarkeitspruefung"})
  (:PruefungNachweis {id: "Sichtpruefung"})
  (:PruefungNachweis {id: "Statische_Nachweisfuehrung"})
  (:PruefungNachweis {id: "Zugversuch"})
  (:PruefungNachweis {id: "Zustandsbewertung"})

:Leistungsanforderung
  (:Leistungsanforderung {id: "Brandschutz"})
  (:Leistungsanforderung {id: "Brandschutzanforderung"})
  (:Leistungsanforderung {id: "Dauerhaftigkeit"})
  (:Leistungsanforderung {id: "F90"})
  (:Leistungsanforderung {id: "Feuchteschutz"})
  (:Leistungsanforderung {id: "Feuerwiderstand"})
  (:Leistungsanforderung {id: "R90"})
  (:Leistungsanforderung {id: "REI90"})
  (:Leistungsanforderung {id: "Rueckbaubarkeit"})
  (:Leistungsanforderung {id: "Schadstofffreiheit"})
  (:Leistungsanforderung {id: "Schallschutz"})
  (:Leistungsanforderung {id: "Tragfaehigkeit"})
  (:Leistungsanforderung {id: "Waermeschutz"})

:Norm
  (:Norm {id: "DIN_18940"})
  (:Norm {id: "DIN_EN_15804"})
  (:Norm {id: "DIN_EN_15978"})
  (:Norm {id: "EN_1090"})
  (:Norm {id: "ISO_14040"})
  (:Norm {id: "ISO_14044"})
  (:Norm {id: "ISO_20887"})

:RechtlicheBedingung
  (:RechtlicheBedingung {id: "Bauordnungsrecht"})
  (:RechtlicheBedingung {id: "EU_Taxonomie"})
  (:RechtlicheBedingung {id: "Gewaehrleistung"})
  (:RechtlicheBedingung {id: "Produkthaftung"})
  (:RechtlicheBedingung {id: "Vergaberecht"})
  (:RechtlicheBedingung {id: "Zulassung_im_Einzelfall"})

:Nutzung
  (:Nutzung {id: "Buero"})
  (:Nutzung {id: "Gewerbe"})
  (:Nutzung {id: "Infrastruktur"})
  (:Nutzung {id: "Kultur"})
  (:Nutzung {id: "Lager_Depot"})
  (:Nutzung {id: "Mischnutzung"})
  (:Nutzung {id: "Schule_Bildung"})
  (:Nutzung {id: "Sozialbau"})
  (:Nutzung {id: "Wohnen"})

:BauaufgabeIntervention
  (:BauaufgabeIntervention {id: "Aufstockung"})
  (:BauaufgabeIntervention {id: "Erweiterung"})
  (:BauaufgabeIntervention {id: "Fit_out"})
  (:BauaufgabeIntervention {id: "Neubau"})
  (:BauaufgabeIntervention {id: "Rueckbau"})
  (:BauaufgabeIntervention {id: "Sanierung"})
  (:BauaufgabeIntervention {id: "Translozierung"})
  (:BauaufgabeIntervention {id: "Umbau"})
  (:BauaufgabeIntervention {id: "Umnutzung"})
  (:BauaufgabeIntervention {id: "Wiederaufbau"})

:Land
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Pla
:Stadt
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Plan

:Akteurrolle
  (:Akteurrolle {id: "Bauherrschaft_Nutzung"})
  (:Akteurrolle {id: "Planung_Gestaltung"})
  (:Akteurrolle {id: "Tragwerk_Fassade"})
  (:Akteurrolle {id: "TGA_Sicherheit"})
  (:Akteurrolle {id: "Ausfuehrung_Logistik"})
  (:Akteurrolle {id: "Beratung_Forschung"})
  (:Akteurrolle {id: "Qualitaetssicherung"})
  (:Akteurrolle {id: "Koordination"})
  ... (acht Kanon-Knoten; Legacy-Unterordner `akteurrolle/<alt>/` → kanonische `id` per §1.D)

:Datenqualitaet
  (:Datenqualitaet {id: "Belegt"})
  (:Datenqualitaet {id: "Geschaetzt"})
  (:Datenqualitaet {id: "Nicht_Belegt"})
  (:Datenqualitaet {id: "Primaerquelle"})
  (:Datenqualitaet {id: "Sekundaerquelle"})
  (:Datenqualitaet {id: "Unbekannt"})
  (:Datenqualitaet {id: "Widerspruechlich"})

:Datenmodell
  (:Datenmodell {id: "Bauteil_ID"})
  (:Datenmodell {id: "IFC"})
  (:Datenmodell {id: "Klassifikation"})
  (:Datenmodell {id: "Materialdatenbank"})
  (:Datenmodell {id: "Materialpass_Schema"})
  (:Datenmodell {id: "Ontologie"})
  (:Datenmodell {id: "Taxonomie"})

:Tooltyp
  (:Tooltyp {id: "Bauteilboerse"})
  (:Tooltyp {id: "Materialdatenbank"})
  (:Tooltyp {id: "Materialkataster"})

:ZertifizierungBewertungssystem
  (:ZertifizierungBewertungssystem {id: "BREEAM"})
  (:ZertifizierungBewertungssystem {id: "DGNB"})
  (:ZertifizierungBewertungssystem {id: "LEED"})
  (:ZertifizierungBewertungssystem {id: "Paris_Proof"})
  (:ZertifizierungBewertungssystem {id: "WELL"})

:Wirtschaft
  (:Wirtschaft {id: "Finanzierung"})
  (:Wirtschaft {id: "Geschaeftsmodell"})
  (:Wirtschaft {id: "Kostenvergleich"})
  (:Wirtschaft {id: "Lebenszykluskosten"})
  (:Wirtschaft {id: "Preisbildung"})
  (:Wirtschaft {id: "Restwert"})

:Programm
  (:Programm {id: "BBSM", programm_typ: "foerderung"})
  (:Programm {id: "FCRBE", programm_typ: "foerderung"})
  (:Programm {id: "PREUSE", programm_typ: "foerderung"})
  (:Programm {id: "Reallabor_Be_Ware", programm_typ: "foerderung"})
  (:Programm {id: "Zukunftbau", programm_typ: "foerderung"})
  (:Programm {id: "Foerderprogramm", programm_typ: "forschungskontext"})
  (:Programm {id: "Forschungsprojekt", programm_typ: "forschungskontext"})
  (:Programm {id: "Kommunales_Programm", programm_typ: "forschungskontext"})
  (:Programm {id: "Pilotprojekt", programm_typ: "forschungskontext"})
  (:Programm {id: "Reallabor", programm_typ: "forschungskontext"})
  (:Programm {id: "Wettbewerb", programm_typ: "forschungskontext"})
```

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

Same rule for every folder: `_database/material/<x>/` produces `(:Material {id: "<x>"})`, `_database/huerde/<x>/` produces `(:Huerde {id: "<x>"})`, `_database/schadstoff/<x>/` produces `(:Huerde {id: "<x>", kategorie: "Schadstoff"})`, etc.

`**id` vs. Ordnername:** Für die **35** folder-gestützten Labels in §1.B ist `id` in der Regel **gleich** dem Unterordnernamen (ggf. ASCII nach derselben Tabelle). Für `**:Bauteilgruppe`** im Ordner `**bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`** und für `**:ReuseEinsatz`** in `**reuse_einsatz/<id>/`** ist Graph-`id` **gleich** dem jeweiligen Unterordner-Slug (bzw. verbindliches `<CASE>_C<NN>_<ELEMENT>`-Muster für `:Bauteilgruppe` — siehe Tabelle unten). Für die übrigen **sieben** Primär-Labels in §1.A (`:Fallbeispiel`, `:Bauwerk`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`) ist `id` der **vom Export normalisierte** Slug nach der folgenden Tabelle — der Quellordnername ist nur Eingabe, nicht zwingend 1:1 der Graph-`id` (**`:Bauwerk`** typisch aus Legacy `bauobjekt/<id>/` oder abgeleitet und mit `(:Fallbeispiel)` verknüpft; **`:Software`** / **`:Tool`** typisch aus `software_digitaltool/<id>/` nach §1.E-Klassifikation).

**ID- und Namenskonvention (Lesbarkeit)**


| Regel                             | Vorgabe                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Zeichensatz                       | **ASCII** in `id`. Umlaute als `ae`, `oe`, `ue`, `ss` (keine kaputten Fragmente wie `Tr_ger`, `T_ren`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Trenner                           | Nur **einfaches** `_` zwischen Wortteilen. **Keine** doppelten `__` als Padding, **keine** `;` oder `,` innerhalb einer `id`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Ein Knoten                        | **Eine** reale Entität pro Knoten — **keine** Listen (`A;B,C`) in einer `id`. Mehrere Akteure → mehrere `:Akteur`-Knoten + mehrere Kanten.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Länge                             | Kurz halten: bevorzugt **≤ 48** Zeichen pro `id` (harte Grenze im Export z. B. 96).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `:Fallbeispiel`                   | `id` = erkennbarer **Projekt- oder Orts-Slug** der Fall-/Projektakte, z. B. `Berlin_Schildow_Pilot_Haus`, `55_Great_Suffolk_Street_London` — Wortfolge logisch lesbar (**kein** Gebäude-`art`-Feld; physisches Bauwerk → **`:Bauwerk`**).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `:Bauwerk`                        | `id` = stabiler Slug pro **physischem Bauwerk** (oft gleich oder erweitert gegenüber dem zugehörigen `Fallbeispiel.id`, z. B. Suffix `_Gebaeude`); Quelle typisch `bauobjekt/<id>/`. Verknüpfung zur Akte: `(:Bauwerk)-[:GEHÖRT_ZU {rolle: 'fallbeispiel'}]->(:Fallbeispiel)`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `:Bauteilgruppe`                  | **Physische Elementgruppe** — verbindliches Muster (Ordner + Graph-`id`): `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` → `(:Bauteilgruppe {id: "<CASE>_C<NN>_<ELEMENT>"})`. `**CASE`**: kurzer, stabiler Projektcode (ASCII, oft Kürzel des `:Fallbeispiel`, z. B. `K118`, `ELYS`, `55GSS`, `CRCLR`, `Werkhof29`, `Plattenpalast`). `**<NN>`**: zweistellige laufende Nummer pro Fall (`01`…`99`). `**<ELEMENT>**`: snake_case-Bauteilgruppenname (ASCII, lesbar). Beispiele: `K118_C01_Traeger_Stuetzen`, `K118_C02_Treppe`, `ELYS_C01_Fenster`, `Plattenpalast_C01_Wandplatten`, `55GSS_C01_Traeger_Stuetzen`, `CRCLR_C02_Wandpaneele`, `Werkhof29_C01_Fassadenbleche`. Räumliche/logische Anbindung an **`:Bauwerk`** / `:Fallbeispiel` typischerweise über `GEHÖRT_ZU` (und/oder über verknüpften `:ReuseEinsatz`); `CASE` muss nicht 1:1 dem langen `Fallbeispiel.id` entsprechen. |
| `:ReuseEinsatz`                   | **Wiederverwendungs-Aktion** (Ereignis/Einsatz), nicht die physische Masse selbst: `_database/reuse_einsatz/<id>/` → `(:ReuseEinsatz {id: "<id>"})` (ASCII-Slug wie §1). Verknüpfung zur physischen Gruppe: `(:ReuseEinsatz)-[:GEHÖRT_ZU {rolle: 'bauteilgruppe'}]->(:Bauteilgruppe)` wenn beide Knoten existieren; sonst nur Einsatz-Knoten aus Legacy-Daten. |
| `:Akteur`                         | `id` = **Organisationskurzname** in konsistentem Wortbild (`Circular_Berlin`, `Circular_Structural_Design`, `Bellastock`) oder **Person** `Vorname_Nachname`. Keine technischen Pfad-Präfixe.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `:Quelle`                         | `id` = **kurzer Zitations-Slug**, z. B. `Circular_Berlin_marktstudie_2023` — **nicht** gespiegelte Dateipfade wie `akteur_04_planung_..._md`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `:Software`                       | `id` = stabiler Produkt-/Plattform-Slug (ASCII); **`title`** = lesbarer Kurzname (z. B. `Madaster`, `Autodesk Revit`). Optional `softwaretyp` / `anbieter` / `url` (§1.E).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `:Tool`                           | `id` = stabiler Slug für Modul/Skript/API/…; **`title`** = lesbarer Kurzname. Optional `tooltyp` / `funktion` / `version` (§1.E). **Kein** Ersatz für `:Software` — bei vollständiger Plattform immer **`:Software`**.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `:Wiederverwendungskette`         | `id` an Fallbeispiel anbindbar (`K118_Halle_118_Winterthur`) oder eigener kurzer Kettenname — ohne URL-artige Monsterstrings.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Bauteilbörse** (deutscher Begriff) | Im Graphen **kein** separates Label; Kanon-**`id`** = **`Bauteilboerse`** (Umlaut → `oe`) auf **`(:Ressourcenquelle)`**, **`(:Beschaffungsweg)`**, **`(:Tooltyp)`** — Ordner `_database/ressourcenquelle/Bauteilboerse/`, `beschaffungsweg/Bauteilboerse/`, `tooltyp/Bauteilboerse/`. **Regionale Börsen / Marktplätze** als eigene **`(:Akteur)`**-Knoten, z. B. **`Bauteilboerse_Hannover`**, **`Bauteilboerse_Bremen`** (`_database/akteur/`). **`_database/software_digitaltool/Bauteilboerse_*`** → **`(:Software)`** oder **`(:Tool)`** nach §1.E. (Prosa mit „ö“, z. B. `_database/quelle/…/bauteilbörse.md`, bleibt nur in Markdown.) |
| Weitere `_database`-Labels (§1.B) | `id` = stabiler Term-Slug; gleiche ASCII-/Trennerregeln; Ordner unter `_database/<label>/` möglichst schon so benannt, damit Import trivial bleibt.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |


Exceptions (folders that are NOT 1:1 a node type) are listed in §1.C — they merge into another Label, get renamed, or are dropped.

**Geography exception:** `_database/ort/<id>/` is not mapped to a single `:Ort` Label. On export, each slug becomes either `(:Land {id})` or `(:Stadt {id})` according to a classification rule (country/region vs city/district/site). The plan does not enumerate those node ids.

`**:Status` — vereinheitlicht (Gebäude- + Einsatz-Lebenszyklus):** Label `**:ReuseEinsatzstatus`** und `**:Bauobjektstatus**` entfallen. Es gibt **genau sieben** `:Status`-Knoten. Anbindung nur über `**HAT_STATUS`** (nicht `IST`) von `**(:Bauwerk)**` (**Gebäude-/Anlagen-Lebenszyklus** — kanonisch für `bauobjektstatus/`), **`(:ReuseEinsatz)`** (Einsatz — **kanonisch** für Einsatz-Lebenszyklus), optional **`(:Fallbeispiel)`** (Fall-/Projekt-Ebene, wenn kein separates `:Bauwerk` materialisiert ist) und optional **`(:Bauteilgruppe)`** (nur wenn explizit gruppenbezogener Status erhalten bleibt) an `:Status`.


| Kanon-`id` (`:Status`) | Kurzbedeutung                              |
| ---------------------- | ------------------------------------------ |
| `Geplant`              | noch nicht in Ausführung / Konkurrenzphase |
| `In_Bau`               | in Ausführung                              |
| `Realisiert`           | fertiggestellt und (ggf.) in Nutzung       |
| `Prototyp`             | Versuchs-/Pilotstand                       |
| `Rueckgebaut`          | Rückbau / Abbruch abgeschlossen            |
| `Nicht_Realisiert`     | nicht umgesetzt / verworfen                |
| `Unklar`               | nicht eindeutig zuordenbar                 |


**Legacy `reuse_einsatzstatus/<id>/` → `(:Status {id})`:**


| Legacy `reuse_einsatzstatus/<id>/` | → Kanon-`id`                                             |
| ---------------------------------- | -------------------------------------------------------- |
| `Geplant`                          | `Geplant`                                                |
| `Vorgeschlagen`                    | `Geplant`                                                |
| `Prototypisch`                     | `Prototyp`                                               |
| `Realisiert`                       | `Realisiert`                                             |
| `Temporaer`                        | `Realisiert` (oder `Prototyp` — Heuristik nach Fallakte) |
| `Verworfen`                        | `Nicht_Realisiert`                                       |
| `Unklar`                           | `Unklar`                                                 |


**Legacy `bauobjektstatus/<id>/` → `(:Status {id})`:** (Ordner `bauobjektstatus/` mappt auf dieselben sieben Knoten; Label `:Bauobjektstatus` entfällt.)


| Legacy `bauobjektstatus/<id>/` | → Kanon-`id`                               |
| ------------------------------ | ------------------------------------------ |
| `Gebaut`                       | `Realisiert`                               |
| `Geplant`                      | `Geplant`                                  |
| `In_Bau`                       | `In_Bau`                                   |
| `Prototyp`                     | `Prototyp`                                 |
| `Rueckgebaut`                  | `Rueckgebaut`                              |
| `Temporaer`                    | `Prototyp` (oder `Realisiert` — Heuristik) |
| `Unklar`                       | `Unklar`                                   |
| `Wettbewerb`                   | `Geplant`                                  |


**Reuse-Strategie-Konsolidierung (verbindlich — 6 Kanon-Knoten):** Legacy `reuse_strategie/` hat **elf** Unterordner; im Graphen sind das **genau sechs** Knoten `**(:WiederverwendungsArt { axis: "reuse_strategie" })`** (*Art der Wiederverwendung*). `**(:Fallbeispiel)`** (Fall-/Projektakte), **`(:Bauwerk)`** (physisches Bauwerk — früher oft mit „Bauobjekt“ verwechselt) und **`(:ReuseEinsatz)`** verbinden sie ausschließlich per `**HAT { art: 'wiederverwendungsart' }**` — **kein** eigener Kantentyp, **kein** separates Label `:ReuseStrategie`. Ausführliche Beispiele bleiben in den Markdown-Quellen; im Graphen nur Kanon-`id` + `axis`.


| Nr.   | Kanon-`id` (`:WiederverwendungsArt`, `axis: "reuse_strategie"`) | Leitidee (Kurz)                                                                                                                                 |
| ----- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | `Bestandserhalt_Weiterbauen`                                    | Gebäude oder große Gebäudeteile bleiben erhalten und werden angepasst.                                                                          |
| **2** | `In_situ_Wiederverwendung`                                      | Bauteile bleiben am ursprünglichen Ort und werden weitergenutzt.                                                                                |
| **3** | `Direkte_Wiederverwendung`                                      | Bauteil wird ausgebaut und an anderer Stelle mit **gleicher Funktion** wieder eingebaut.                                                        |
| **4** | `Wiederverwendung_nach_Aufarbeitung`                            | Bauteil wird gereinigt, repariert, geprüft oder angepasst (inkl. konstruktive **Vorbereitung** auf spätere Demontage / DfD-Logik).              |
| **5** | `Umnutzung_Repurposing`                                         | Bauteil erhält eine **neue Funktion**.                                                                                                          |
| **6** | `Kaskade_Downcycling_Bauteilebene`                              | Bauteil wird in einer **weniger anspruchsvollen** Funktion weitergenutzt (inkl. stofflicher Rückführung / Bestandserschließung aus Altbestand). |



| Legacy `reuse_strategie/<id>/`                                                 | → Kanon-`id`                         |
| ------------------------------------------------------------------------------ | ------------------------------------ |
| `Bestandserhalt`, `Weiterbauen_im_Bestand`, `Refurbishment`, `Adaptives_ReUse` | `Bestandserhalt_Weiterbauen`         |
| `Same_Site_ReUse`                                                              | `In_situ_Wiederverwendung`           |
| `Direkte_Wiederverwendung`                                                     | `Direkte_Wiederverwendung`           |
| `Remanufacturing`, `Design_for_Disassembly`                                    | `Wiederverwendung_nach_Aufarbeitung` |
| `Upcycling`                                                                    | `Umnutzung_Repurposing`              |
| `Recycling`, `Urban_Mining`                                                    | `Kaskade_Downcycling_Bauteilebene`   |


**Fügung/Verbindung → nur Verbindungstechnik:** Legacy folder `fuegung_verbindung/` enthielt gemischte Begriffe; im Graphen wird **ausschließlich die Verbindungs-/Fügetechnik** über `**:Verbindungstechnik`** abgebildet (`HAT {art:'verbindungstechnik'}`). `**:Reversibilitaet` gehört nicht zu „Verbindungen“** in diesem Sinne: kein Import aus `fuegung_verbindung/` für dieses Label, keine Zeile in der folgenden Tabelle.


| Legacy `fuegung_verbindung/<id>/` | Target Label          | Canonical node `id` |
| --------------------------------- | --------------------- | ------------------- |
| `Verschraubung`                   | `:Verbindungstechnik` | `Geschraubt`        |
| `Verschweissung`                  | `:Verbindungstechnik` | `Geschweisst`       |
| `Steckverbindung`                 | `:Verbindungstechnik` | `Gesteckt`          |
| `Verleimung`                      | `:Verbindungstechnik` | `Geklebt`           |
| `Vermoertelung`                   | `:Verbindungstechnik` | `Vergossen`         |
| `Klemmverbindung`                 | `:Verbindungstechnik` | `Klemmverbindung`   |



| Legacy `fuegung_verbindung/Reversible_Fuegung/` | Graph (dieser Plan)                                                                                                                                                               |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (gesamter Ordner)                               | **Kein** automatischer Export zu `:Verbindungstechnik` oder `:Reversibilitaet`; Inhalt bleibt in Markdown / spätere eigenständige Kuratierung außerhalb der Verbindungs-Pipeline. |


`**:Reversibilitaet` — nur eigener Knotentyp:** Label `**:Reversibilitaet`** mit genau vier Knoten (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`), eigene **UNIQUE-Constraint** auf `(n:Reversibilitaet).id`, ausschließlich `**HAT {art:'reversibilitaet'}`** von `:Fallbeispiel` / `:Bauwerk` / `:Bauteilgruppe` / `:ReuseEinsatz`. Datenquelle: **explizite** Metadaten (z. B. künftiges Feld / Kuratierung) — **nicht** `fuegung_verbindung/`, **nicht** `IST`, keine Einbettung unter `:Verbindungstechnik`.

## §1.A Primär-Labels (9)


| Label                     | Purpose                                                     | Replaces (legacy folders)                                                                                                              |
| ------------------------- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| `:Fallbeispiel`           | **Case-study / project record** (metadata layer, not the built asset) | `fallstudie/` + `projekt/` (merged where ids match)                                                                                    |
| `:Bauwerk`                | **Physical built work** (building, bridge, hall, …) + building-level measurements | `bauobjekt/` → **`:Bauwerk`**; link to `:Fallbeispiel` via `GEHÖRT_ZU {rolle: 'fallbeispiel'}`                                         |
| `:Bauteilgruppe`          | **Physical** component group (mass, geometry, stock)      | `bauteilgruppe/` (canonical `id` pattern `<CASE>_C<NN>_<ELEMENT>` — see §1)                                                           |
| `:ReuseEinsatz`           | **Reuse action** / deployment event linked to group + **Bauwerk**  | `reuse_einsatz/` (one node per folder; link to `:Bauteilgruppe` via `GEHÖRT_ZU {rolle: 'bauteilgruppe'}` when both exist)               |
| `:Akteur`                 | Office / company / authority / institution / person         | `akteur/`                                                                                                                              |
| `:Quelle`                 | Source / citation target                                    | `quelle/`                                                                                                                              |
| `:Software`               | **Complete** named digital ecosystem, platform, or application (host system) | `software_digitaltool/` **only** entries classified as full platforms/apps — see §1.E                                                  |
| `:Tool`                   | Smaller module, plug-in, script, workflow aid, API, calculator, sub-tool (**not** a synonym for `:Software`) | `software_digitaltool/` entries classified as modules/scripts/… + optional `GEHÖRT_ZU {rolle: 'software'}` → `:Software` (§1.E)          |
| `:Wiederverwendungskette` | OPTIONAL named multi-Bauteilgruppe reuse program            | `reuse_kette/` (renamed; `reuse_kettenstation/` dropped)                                                                               |


## §1.B Weitere Labels (35 — jeder `_database/<label>/`-Ordner **mit eigenem Neo4j-Label** **außer** `**:Akteurrolle**` (siehe §1.D: viele Legacy-Unterordner → **acht** Kanon-Knoten); `ort/` splits into two Labels; `fuegung_verbindung/` → `**:Verbindungstechnik`** only; `**:Reversibilitaet**` is a separate node type without `fuegung_verbindung/` provenance; `**reuse_strategie/**` + `**bewertungslogik_abgrenzung/**` → `**:WiederverwendungsArt**` mit `axis` (`einordnung` | `grundtyp` | `reuse_strategie`); `**bauobjektstatus/**` merged into `**:Status**` — see §1 Status tables; **`kontextmerkmal/`** → **kein** `:Kontextmerkmal`-Label — siehe §1.C; **`schadstoff/`** → **kein** `:Schadstoff`-Label — Stoff-Knoten sind **`:Huerde`** mit **`kategorie: "Schadstoff"`** — siehe §1.C)

Grouped only for reading.

**Bauteil & Material:**

- `:Bauteiltyp` ← `bauteiltyp/`
- `:Material` ← `material/`
- `:Bauteilebene` ← `bauteilebene/`
- `:Bauteilzustand` ← `bauteilzustand/`
- `:Funktionswechsel` ← `funktionswechsel/`

**Verbindung (Technik):**

- `:Verbindungstechnik` ← `fuegung_verbindung/` **nur** die sechs Technik-Ordner (siehe Tabelle); Ordner `Reversible_Fuegung/` **kein** Ziel dieses Labels.

**Lösbarkeit (eigenständiger Knotentyp — nicht unter Verbindungen):**

- `:Reversibilitaet` ← **kein** `fuegung_verbindung/`-Bezug; **vier feste** Knoten; nur `HAT {art:'reversibilitaet'}`; Daten nur aus **expliziten** Quellen (nicht aus der Verbindungs-Migration). **Nicht** dasselbe wie `methode/Reversibilitaet/` → weiterhin `(:Methode {id: "Reversibilitaet"})` per `**BENUTZT`**.

**Konstruktion:**

- `:Bauweise` ← `bauweise/`
- `:Bausystem` ← `bausystem/`
- `:Tragwerksprinzip` ← `tragwerksprinzip/`

**Reuse:**

- `:Status` ← `reuse_einsatzstatus/` + `**bauobjektstatus/`** (**merged** — **seven** canonical nodes; **Label `:Bauobjektstatus` dropped**; see §1 Status tables; edges `**HAT_STATUS`** from `:Bauwerk` / `:ReuseEinsatz` / optional `:Fallbeispiel` / optional `:Bauteilgruppe`)
- `:WiederverwendungsArt` ← `bewertungslogik_abgrenzung/` (renamed) **+** `reuse_strategie/` (**eleven** legacy folders → **six** canonical `id`s with `**axis: "reuse_strategie"`** — *Art der Wiederverwendung*; from `:Fallbeispiel` / `:Bauwerk` / `:ReuseEinsatz` only via `**HAT { art: "wiederverwendungsart" }**` — see **Reuse-Strategie-Konsolidierung** in §1)

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

- `:Huerde` ← `huerde/` **und** `schadstoff/` (chem./Stoff-Stammdaten: je Unterordner → **`(:Huerde { id, kategorie: "Schadstoff" })`** — **kein** separates Label `:Schadstoff`)
- `:PruefungNachweis` ← `pruefung_nachweis/`
- `:Leistungsanforderung` ← `leistungsanforderung/`
- `:Norm` ← `norm/`
- `:RechtlicheBedingung` ← `rechtliche_bedingung/`

**Fallbeispiel-Kontext:**

- `:Nutzung` ← `nutzung/`
- `:BauaufgabeIntervention` ← `bauaufgabe_intervention/`
- `:Entwurfsentscheidung` ← **new** — no legacy folder; created fresh. Label capturing design adaptations forced by reuse constraints. Connected via `HAT {art:'entwurf'}` from `:ReuseEinsatz` (action-specific), `:Bauteilgruppe` (physical-group-specific), `:Bauwerk` (building-level), or `:Fallbeispiel` (project-wide). Initial values defined from K.118 example and generalised across all case data.

**Geographie:**

- `:Land` ← each qualifying entry from `ort/` (export classification: country / macro-region)
- `:Stadt` ← each qualifying entry from `ort/` (export classification: city, borough, or project-scale site id)

**Akteure:**

- `:Akteurrolle` ← `akteurrolle/` (**kein** 1:1 Ordner→Knoten): im Graphen **genau acht** `(:Akteurrolle {id})` nach §1.D; **`HAT { art: 'akteur' }.rolle`** trägt **immer** die **kanonische** `id` (Bund), nicht den Roh-Unterordnernamen. Keine `IST`-Kanten auf `:Akteurrolle`.

**Daten & Bewertung:**

- `:Datenqualitaet` ← `datenqualitaet/`
- `:Datenmodell` ← `datenmodell/`
- `:Tooltyp` ← `tooltyp/` (**Taxonomie-Label**; **nicht** dasselbe wie die **Property** `tooltyp` auf **`(:Tool)`** — §1.E)
- `:ZertifizierungBewertungssystem` ← `zertifizierung_bewertungssystem/`

**Wirtschaft & Programme:**

- `:Wirtschaft` ← `wirtschaft/`
- `:Programm` ← `foerderprogramm/` + `programm_kontext/` + **Provenienz** `kontextmerkmal/Pilotprojekt` (merged; **ein** Kanon-Knoten `(:Programm { id: "Pilotprojekt" })`; `programm_typ` property: `"foerderung"` / `"forschungskontext"`)

## §1.C Folders mapped but NOT a Label


| Folder                        | Disposition                                                                                                                                                                                                              |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fallstudie/`                 | merged into `:Fallbeispiel` (case/project **record**)                                                                                                                                                                   |
| `projekt/`                    | merged into `:Fallbeispiel` (same **record** layer)                                                                                                                                                                      |
| `reuse_kettenstation/`        | dropped — stations become GEHÖRT_ZU edges from `:ReuseEinsatz` (preferred) or `:Bauteilgruppe`                                                                                                                           |
| `akteur_beteiligung/`         | dropped — collapsed to `HAT {art:'akteur', rolle:...}` edge                                                                                                                                                              |
| `bauobjekt_beteiligung/`      | dropped — same pattern                                                                                                                                                                                                   |
| `datenpunkt/`                 | dropped — measurements as node properties                                                                                                                                                                                |
| `kennwertdefinition/`         | dropped — kennwert-names live as property names                                                                                                                                                                          |
| `bauobjektklasse/`            | dropped — values attach to **`:Bauwerk`** or **`:Fallbeispiel`** per export (building typology vs. case record); no separate Label                                                                                       |
| `bauobjektrolle/`             | dropped — donor/receiver/standalone derivable from incoming GEHÖRT_ZU edges (`rolle:'herkunft'` / `rolle:'einbauort'`) **on `:ReuseEinsatz` / `:Bauteilgruppe` → `:Bauwerk`**                                              |
| `dokumenttyp/`                | dropped — replaced by `:Quelle.art`                                                                                                                                                                                      |
| `tragwerkstyp/`               | dropped — axis-mix (review §7.8); material values derivable from `:Material`, reuse values folded into `:WiederverwendungsArt`                                                                                           |
| `foerderprogramm/`            | merged into `:Programm`                                                                                                                                                                                                  |
| `programm_kontext/`           | merged into `:Programm`                                                                                                                                                                                                  |
| `bewertungslogik_abgrenzung/` | renamed to `:WiederverwendungsArt`                                                                                                                                                                                       |
| `reuse_strategie/`            | folded into `:WiederverwendungsArt` with `**axis: "reuse_strategie"**` (**six** canonical `id`s); **not** a separate Label; edges `**HAT { art: "wiederverwendungsart" }`** from `:Fallbeispiel` / `:Bauwerk` / `:ReuseEinsatz` (§1) |
| `bauobjektstatus/`            | merged into `:Status` — **seven** canonical `id`s (§1); dedicated `**HAT_STATUS`** edges; Label `:Bauobjektstatus` removed                                                                                               |
| `reuse_kette/`                | renamed to `:Wiederverwendungskette`                                                                                                                                                                                     |
| `kontextmerkmal/`             | **Kein Label `:Kontextmerkmal`:** `Pilotprojekt` → derselbe Knoten wie **`(:Programm { id: "Pilotprojekt" })`** aus `programm_kontext/` (Legacy **`has_kontextmerkmal`** → **`GEHÖRT_ZU { rolle: 'programm' }` → `:Programm`** je Exportregel); **`Bestandserhalt_Policy`** → **kein** eigener Taxonomie-Knoten (fachliche Einordnung über **`reuse_strategie/Bestandserhalt`** → **`WiederverwendungsArt`** / **`HAT { art: "wiederverwendungsart" }`** wo sinnvoll; sonst nur Markdown / **`BELEGT_IN`**) |
| `schadstoff/`                 | **Kein Label `:Schadstoff`:** Unterordner → **`(:Huerde { id, kategorie: "Schadstoff" })`**; Kanten weiterhin **`HAT { art: "huerde" }`** (nicht mehr `art: "schadstoff"`). Legacy **`has_schadstoff`** → **`HAT { art: "huerde" }` → `:Huerde`** |
Total: 54 folders → **44** Neo4j Labels (**9** in §1.A + **35** in §1.B) + 10 dropped + **6** merged-or-renamed (`ort/` yields two Labels; `fuegung_verbindung/` → `:Verbindungstechnik` only — `:Reversibilitaet` has no folder provenance; **`bauobjekt/`** → **`:Bauwerk`** (Primär-Label — **not** listed in §1.C); **`software_digitaltool/`** → **`:Software`** **or** **`:Tool`** per §1.E (split of former single primary **`:SoftwareDigitaltool`**); **`schadstoff/`** → **`:Huerde`** with `kategorie: "Schadstoff"` — **not** a separate Label; **`kontextmerkmal/`** → **`:Programm`** + Strategie-Vokabular — **not** a separate Label; `reuse_einsatz/` → **`:ReuseEinsatz`**; `reuse_strategie/` folds into `**:WiederverwendungsArt`** as `**axis: "reuse_strategie"**` (**six** canonical `id`s — not a separate Label; `bauobjektstatus/` + `reuse_einsatzstatus/` → **one** `:Status` Label with **seven** canonical nodes).

## §1.D `:Akteurrolle` — Kanon-Bündel (8 Knoten)

**Ziel:** weniger Begriffsknoten, stabilere Abfragen. Die **21** Legacy-Unterordner unter `_database/akteurrolle/<id>/` werden beim Export auf **acht** Kanon-`id`s abgebildet. Feingliederung bleibt in den jeweiligen `index.md`-Quellen, nicht im Graphen.

**Kanon-`id` (`:Akteurrolle`) — genau diese acht Knoten:** `Bauherrschaft_Nutzung`, `Planung_Gestaltung`, `Tragwerk_Fassade`, `TGA_Sicherheit`, `Ausfuehrung_Logistik`, `Beratung_Forschung`, `Qualitaetssicherung`, `Koordination`.


| Legacy-Ordner `akteurrolle/<id>/` | Kanon-`:Akteurrolle.id`     |
| --------------------------------- | ---------------------------- |
| `Bauherr_Auftraggeber`            | `Bauherrschaft_Nutzung`      |
| `Betreiber_Nutzer`              | `Bauherrschaft_Nutzung`      |
| `Oeffentliche_Hand`               | `Bauherrschaft_Nutzung`      |
| `Architektur`                     | `Planung_Gestaltung`         |
| `Landschaftsplanung`              | `Planung_Gestaltung`         |
| `Kunst_Gestaltung`                | `Planung_Gestaltung`         |
| `Tragwerksplanung`                | `Tragwerk_Fassade`           |
| `Fassade`                         | `Tragwerk_Fassade`           |
| `Stahlbau_Fertigung`              | `Tragwerk_Fassade`           |
| `TGA_Gebaeudetechnik`             | `TGA_Sicherheit`             |
| `Brandschutz_Barrierefreiheit`    | `TGA_Sicherheit`             |
| `Bauausfuehrung`                  | `Ausfuehrung_Logistik`       |
| `Rueckbau_Demontage`              | `Ausfuehrung_Logistik`       |
| `Materiallieferant`               | `Ausfuehrung_Logistik`       |
| `Aufbereitung_Refurbishment`      | `Ausfuehrung_Logistik`       |
| `Reuse_Beratung`                  | `Beratung_Forschung`         |
| `Nachhaltigkeitsberatung`         | `Beratung_Forschung`         |
| `Forschung_Dokumentation`         | `Beratung_Forschung`         |
| `Pruefung_Qualitaetssicherung`    | `Qualitaetssicherung`        |
| `Projektmanagement_Koordination`  | `Koordination`               |
| `Projektbeteiligte_Unbestimmt`    | `Koordination`               |


## §1.E `:Software` und `:Tool` — Semantik, Properties, Kanten, Migration

**Normative Unterscheidung**

- **`:Software`** — vollständiges benanntes digitales **Ökosystem**, **Plattform** oder **Anwendung** (ein eigenständiges System / Produkt im Software-Sinne).
- **`:Tool`** — kleineres **funktionales** Artefakt: Modul, Plug-in, Feature, Skript, Workflow-Hilfe, API, Rechner, Matching-Algorithmus oder Sub-Tool, das **innerhalb** oder **zusammen mit** einer Software-Umgebung arbeitet. **`:Tool` ist kein Oberbegriff für `:Software` und kein generischer Ersatz für „Software“.**

**Knoten-Properties**

| Label       | Pflicht        | Optional |
| ----------- | -------------- | -------- |
| `:Software` | `id`, `title`  | `softwaretyp`, `anbieter`, `url` |
| `:Tool`     | `id`, `title`  | `tooltyp`, `funktion`, `version` |

- **`softwaretyp`** (optional, Property auf `:Software`): `BIM_Plattform` \| `Materialdatenbank` \| `Bauteilplattform` \| `LCA_Software` \| `CAD` \| `GIS` \| `Tabellenkalkulation` \| `Projektplattform` \| `Sonstiges`
- **`tooltyp`** (optional, Property auf `:Tool`): `Plugin` \| `Skript` \| `Rechner` \| `API` \| `Feature` \| `Modul` \| `Workflow` \| `Template` \| `Sonstiges`

**Abgrenzung: Label `:Tooltyp` vs. Property `tooltyp`**

- **`:Tooltyp`** (§1.B, Ordner `tooltyp/`) = **Taxonomie-Knoten** wie andere Klassifikations-Labels; typische Anbindung per **`IST`** je Exportregel.
- **`tooltyp`** auf **`(:Tool)`** = **Instanz-Property** am konkreten Tool (kann fachlich zu einem `:Tooltyp`-Knoten passen, **muss** aber nicht identisch sein).

**Kanten**

- **`(:Tool)-[:GEHÖRT_ZU { rolle: "software" }]->(:Software)`** — optionale Zugehörigkeit eines Sub-Tools zur Host-**Software**.
- **`BENUTZT`** — Ziel kann **`(:Software)`** oder **`(:Tool)`** sein.
- **`IST`** — **`(:Software)`** und **`(:Tool)`** wie andere Primär-Instanzen gegenüber Klassifikations-Labels (z. B. `:Tooltyp`).

**Migration aus `software_digitaltool/`**

1. Jeder Unterordner wird beim Export **explizit** als **`(:Software)`** **oder** **`(:Tool)`** klassifiziert — **nicht** pauschal alles als „Tool“.
2. Der frühere Primär-Typ **`:SoftwareDigitaltool`** entfällt; Legacy **`uses_software_digitaltool`** → **`BENUTZT`** mit Ziel **`(:Software)`** oder **`(:Tool)`** je nach Einordnung.
3. Klar erkennbare **Module** einer **Host-Plattform**: **`(:Tool)`** anlegen und optional **`GEHÖRT_ZU { rolle: "software" }`** zur **Host-`:Software`** setzen.

**Beispiele (Einordnung)**

| Beispiel | Label |
| -------- | ----- |
| Madaster, Concular, Restado, Loopfront | `:Software` |
| Revit, Rhino, OneClickLCA, Excel, QGIS | `:Software` |
| Grasshopper-Skript Material-Matching | `:Tool` |
| Revit-Materialpass-Plug-in | `:Tool` |
| CO2-Rechner-Tabellenblatt | `:Tool` |
| CSV-Import-Skript | `:Tool` |
| API-Connector | `:Tool` |
| Material-Matching-Algorithmus | `:Tool` |


---

# §2 Nodes — properties per Label

Property table columns: **name** | **type** | **req** | **notes**.

**No `body_md`, no `legacy_paths`, no `build_status`, no raw-text labels on any node.** All German prose stays in the source Markdown under `_database/<entity>/<id>/index.md`, outside the graph. **`title`** (und die übrigen Felder aus §1.E) sind **nur** auf **`(:Software)`** und **`(:Tool)`** erlaubt — sonst **kein** `title` auf Knoten.

## §2.A `:Fallbeispiel`


| name               | type   | req | notes                                                                                                                                      |
| ------------------ | ------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `id`               | string | ✓   | UNIQUE; nach §1 **ID-Konvention** normalisierter Slug der **Fall-/Projektakte** (Export), lesbar; nicht zwingend 1:1 alter Ordnername        |
| `art`              | string | ✓   | one of `"Fallstudie"`, `"Projekt"`, `"Fallstudie_Projekt"` (oder verbindliches Enum nach Export) — **kein** Gebäudetyp; der liegt auf `:Bauwerk` |
| `studienjahr`      | int?   | –   | optional, nur wenn aus Frontmatter belegt                                                                                                  |
| `projektstart_jahr`| int?   | –   | optional                                                                                                                                   |
| `projektende_jahr` | int?   | –   | optional                                                                                                                                   |


**No building-level measurement properties** on `:Fallbeispiel` — those belong on **`:Bauwerk`** (§2.B). Programme / Ort auf Akten-Ebene weiter über `GEHÖRT_ZU` (Land, Stadt, Programm) wie in §3.

## §2.B `:Bauwerk`


| name  | type   | req | notes                                                                                                       |
| ----- | ------ | --- | ----------------------------------------------------------------------------------------------------------- |
| `id`  | string | ✓   | UNIQUE; nach §1 **ID-Konvention**; typisch aus Legacy `bauobjekt/<id>/` oder abgeleitet                      |
| `art` | string | ✓   | one of `"Gebaeude"`, `"Bruecke"`, `"Pavillon"`, `"Halle"`, `"Lager"`, `"Innenausbau"`, `"Anlage"`           |


**Building-level measurement properties** (all optional; missing = unknown):


| name                     | type   | notes |
| ------------------------ | ------ | ----- |
| `flaeche_m2`             | float? |       |
| `projektflaeche_m2`      | float? |       |
| `gebaeudemasse_t`        | float? |       |
| `wohneinheiten`          | int?   |       |
| `fertigstellung_jahr`    | int?   |       |
| `entwurfsbeginn_jahr`    | int?   |       |
| `bauzeit_monate`         | int?   |       |
| `lebensdauer_jahre`      | int?   |       |
| `restlebensdauer_jahre`  | float? |       |
| `kosten_eur`             | float? |       |
| `budget_eur`             | float? |       |
| `co2_footprint_kg`       | float? |       |
| `energieverbrauch_kwh_a` | float? |       |
| `wassereinsparung_m3`    | float? |       |
| `bestandslager_m3`       | float? |       |


For each measurement property, optional parallel:

- `<name>_alt: list<float>?` — alternate values from conflicting sources
- `<name>_vertrauensgrad: string?` — `belegt` / `teilweise_belegt` / `unklar` / `umstritten`

Source attribution: `:BELEGT_IN` edges with `eigenschaft:'<name>'`.

**Structural edge (not a property):** `(:Bauwerk)-[:GEHÖRT_ZU {rolle: 'fallbeispiel'}]->(:Fallbeispiel)` — welches physische Bauwerk zu welcher Fallakte gehört.

## §2.C `:Bauteilgruppe`


| name | type   | req | notes                                                                                 |
| ---- | ------ | --- | ------------------------------------------------------------------------------------- |
| `id` | string | ✓   | UNIQUE; verbindlich `<CASE>_C<NN>_<ELEMENT>` wie in §1 (Ordner `bauteilgruppe/<id>/`) |


**Physical component-group measurements** (Masse, Geometrie, Bestand der **Elementgruppe** — nicht projektbezogene Einsatz-KPIs):


| name                       | type   | notes            |
| -------------------------- | ------ | ---------------- |
| `masse_t`                  | float? |                  |
| `anzahl_stueck`            | int?   |                  |
| `volumen_m3`               | float? |                  |
| `flaeche_m2`               | float? | physical area    |
| `geerntete_materialien_t`  | float? |                  |
| `sekundaere_materialien_t` | float? |                  |
| `abfall_vermieden_t`       | float? |                  |


Same `_alt` and `_vertrauensgrad` shadow properties as on `:Bauwerk` (and other measurement nodes).

**No properties for:** bauteil_label, material_label, alte_funktion, neue_funktion, herkunft_label, pruefung_label_raw, norm_recht_label_raw, huerde_label_raw, menge_umfang_raw, quelle_label_raw, body, title.

Where each of those previously lived in the graph (and now lives as an edge or is lost):

- `bauteil_label` (`"Stahlträger / Stützen"`) → canonical `IST→:Bauteiltyp` edge only; fine variant lost at graph level (still in source Markdown).
- `material_label` (`"Brettschichtholz"`) → canonical `BENUTZT→:Material` edge from `:Bauteilgruppe` or `:ReuseEinsatz` depending on claim scope; fine variant lost at graph level.
- `menge_umfang_raw` (`"98 t; 95 %"`) → parsed onto `BENUTZT` edge from the node carrying the quantity (often `:ReuseEinsatz` for share-of-project metrics): `anzahl: 98, einheit: "t", anteil_prozent: 95`.
- `alte_funktion` / `neue_funktion` → on the `BENUTZT` edge: `funktion_alt`, `funktion_neu`.
- `herkunft_label` → resolved to `GEHÖRT_ZU {rolle:'herkunft'}→:Bauwerk` (subject `:ReuseEinsatz` or `:Bauteilgruppe` per §3); if unresolvable, lost at graph level.
- `pruefung_label`, `norm_recht_label`, `huerde_label` → broken into atomic `HAT` edges to `:PruefungNachweis` / `:Norm` / `:Huerde` (subject typically `:ReuseEinsatz`, `:Bauwerk`, or `:Fallbeispiel`).
- `quelle_label` → broken into `:BELEGT_IN` edges to `:Quelle` nodes.

## §2.D `:ReuseEinsatz`


| name | type   | req | notes                                                                                      |
| ---- | ------ | --- | ------------------------------------------------------------------------------------------ |
| `id` | string | ✓   | UNIQUE; Slug aus `reuse_einsatz/<id>/` (§1); kann mit zugehöriger `:Bauteilgruppe.id` übereinstimmen |


**Reuse-action / project-impact measurements** (typisch aus Legacy-`reuse_einsatz/`-Frontmatter):


| name                     | type   | notes                                  |
| ------------------------ | ------ | -------------------------------------- |
| `anteil_prozent`         | float? | share of receiver / project total      |
| `co2_einsparung_kg`      | float? |                                        |
| `co2_reduktion_kg`       | float? |                                        |
| `zielwert_reuse_prozent` | float? |                                        |


Same `_alt` and `_vertrauensgrad` shadow properties as on `:Bauwerk` / `:Fallbeispiel` where numeric claims exist.

**Structural edges (not properties):** link to physical group `GEHÖRT_ZU {rolle: 'bauteilgruppe'}→(:Bauteilgruppe)` when both exist; link to **`:Bauwerk`** (and optionally `:Fallbeispiel`) via `GEHÖRT_ZU` with `rolle` in `einbauort`, `herkunft`, etc. (see §3).

## §2.E `:Akteur`


| name  | type    | req | notes                                                                                                                   |
| ----- | ------- | --- | ----------------------------------------------------------------------------------------------------------------------- |
| `id`  | string  | ✓   | UNIQUE; lesbarer Organisations- oder Personen-Slug (§1 ID-Konvention); **keine** Listen in einem `id`                   |
| `art` | string? | –   | optional: `"Firma"`, `"Buero"`, `"Behoerde"`, `"Institution"`, `"Person"`, `"Verband"`, `"Bauherrschaft"`, `"Sonstige"` |
| `url` | string? | –   | website / firm page                                                                                                     |


## §2.F `:Quelle`


| name  | type    | req | notes                                                                                                                   |
| ----- | ------- | --- | ----------------------------------------------------------------------------------------------------------------------- |
| `id`  | string  | ✓   | UNIQUE; kurzer Zitations-Slug (§1 ID-Konvention), z. B. `Circular_Berlin_marktstudie_2023` — nicht Roh-Dateipfad        |
| `art` | string  | ✓   | one of `"Website"`, `"Interview"`, `"Paper"`, `"Buch"`, `"Bericht"`, `"Datenbank"`, `"Vortrag"`, `"Norm"`, `"Sonstige"` |
| `url` | string? | –   | source URL or DOI                                                                                                       |


No outgoing edges from `:Quelle`. All metadata about a citation (page, excerpt, raw shorthand, scoped property) lives on the incoming `:BELEGT_IN` edge.

## §2.G `:Software`


| name           | type    | req | notes                                                                                          |
| -------------- | ------- | --- | ---------------------------------------------------------------------------------------------- |
| `id`           | string  | ✓   | UNIQUE; Produkt-/Plattform-Slug (§1 ID-Konvention), z. B. `Madaster`, `Revit`                  |
| `title`        | string  | ✓   | Lesbarer Kurzname (Anzeige), z. B. `Madaster`, `Autodesk Revit`                                |
| `softwaretyp`  | string? | –   | optional enum §1.E (`BIM_Plattform`, `Materialdatenbank`, …)                                   |
| `anbieter`     | string? | –   | optional vendor / publisher                                                                    |
| `url`          | string? | –   | optional product URL                                                                           |


## §2.H `:Tool`


| name        | type    | req | notes                                                                                          |
| ----------- | ------- | --- | ---------------------------------------------------------------------------------------------- |
| `id`        | string  | ✓   | UNIQUE; Slug für Modul/Skript/… (§1 ID-Konvention)                                             |
| `title`     | string  | ✓   | Lesbarer Kurzname                                                                              |
| `tooltyp`   | string? | –   | optional enum §1.E — **nicht** verwechseln mit Taxonomie-Label **`:Tooltyp`**                  |
| `funktion`  | string? | –   | optional short functional description                                                         |
| `version`   | string? | –   | optional version string                                                                        |


## §2.I `:Wiederverwendungskette`


| name         | type   | req | notes                                                                                                           |
| ------------ | ------ | --- | --------------------------------------------------------------------------------------------------------------- |
| `id`         | string | ✓   | UNIQUE; typisch gleiches Kurz-Muster wie zugehöriges `:Fallbeispiel` oder eigener Kettenname (§1 ID-Konvention) |
| `start_jahr` | int?   | –   |                                                                                                                 |
| `end_jahr`   | int?   | –   |                                                                                                                 |


## §2.J Weitere Labels — gemeinsame Minimal-Properties (§1.B)

Die meisten Labels in §1.B haben **so viele Knoten wie Unterordner** unter dem jeweiligen `_database/<label>/`-Pfad. Beispiel: `_database/material/` mit `Stahl`, `Holz`, `Beton`, … → je ein `(:Material {id: "…"})`. **Ausnahmen:** `:Land` / `:Stadt` (Geographie-Exception); `:Status` (**sieben** feste Kanon-`id`s aus **zusammengeführtem** `reuse_einsatzstatus/` + `bauobjektstatus/` — §1; nur `**HAT_STATUS`**); `:WiederverwendungsArt` (**mehr** Knoten als nur `bewertungslogik_abgrenzung/`, weil `**reuse_strategie/`** (**elf** Legacy-Ordner) auf **sechs** Kanon-`id`s mit `**axis: "reuse_strategie"`** kollabiert — §1; *Art der Wiederverwendung* von Fallakte / **Bauwerk** / **Einsatz** (`:ReuseEinsatz`) nur `**HAT { art: "wiederverwendungsart" }**`, Einordnung/Grundtyp weiter `**IST**`); `:Verbindungstechnik` (Technik-Ordner unter `fuegung_verbindung/` — §1; `Reversible_Fuegung/` ausgeschlossen); `:Reversibilitaet` (**vier** feste Knoten, **kein** `fuegung_verbindung/` — §1). **Hinweis:** Ordner-Label **`:Tooltyp`** ist eine **Klassifikations-Taxonomie**; die Property **`tooltyp`** existiert **nur** auf **`(:Tool)`** (§1.E / §2.H).

Jeder dieser Knoten hat standardmäßig nur:


| name | type   | req | notes                                                                                                                                                |
| ---- | ------ | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id` | string | ✓   | UNIQUE within the Label; in der Regel der Unterordnername unter `_database/<label>/<id>/`, normalisiert nach §1 (ASCII, ein `_` zwischen Wortteilen) |


The id is the queryable identifier. The German prose body explaining the term remains in the source Markdown `_database/<label>/<id>/index.md`, outside the graph.

Zusätzliche Properties nur bei ausgewählten Labels:


| Label                   | extra property               | notes                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------------------- | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `:Land`                 | `iso_country: string?`       | optional ISO country code                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `:Stadt`                | `koordinaten: string?`       | optional coordinates string                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `:Programm`             | `programm_typ: string` (req) | `"foerderung"` or `"forschungskontext"`                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `:WiederverwendungsArt` | `axis: string` (req)         | `"einordnung"` (legacy `bewertungslogik_abgrenzung/`), `"grundtyp"` (`wiederverwendet` / `original` / `hybrid` — absorbed from dropped `:Bauteilgruppentyp`), or `**"reuse_strategie"`** (*Art der Wiederverwendung* — **six** canonical `id`s; **eleven** legacy `reuse_strategie/` folders map to those `id`s — §1); `**axis: "reuse_strategie"`** from `:Fallbeispiel` / `:Bauwerk` / `:ReuseEinsatz` only via `**HAT { art: "wiederverwendungsart" }**`, not `IST` |
| `:Status`               | —                            | exactly **seven** nodes (`Geplant`, `In_Bau`, `Realisiert`, `Prototyp`, `Rueckgebaut`, `Nicht_Realisiert`, `Unklar`); legacy `reuse_einsatzstatus/` + `bauobjektstatus/` map per §1; edges `**HAT_STATUS`** — **Gebäude-Lebenszyklus** kanonisch von `:Bauwerk` |
| `:Verbindungstechnik`   | —                            | six canonical technique ids (see §1); legacy `fuegung_verbindung/` technique folders remap to these `id` values                                                                                                                                                                                                                                                                                                                                            |
| `:Huerde`               | `kategorie: string?`         | bei Import aus **`schadstoff/`**: **`"Schadstoff"`** (verbindlich); bei `huerde/`-Knoten optional weglassen                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `:Reversibilitaet`      | —                            | exactly **four** nodes (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`); **not** sourced from `fuegung_verbindung/` (see §1)                                                                                                                                                                                                                                                                                                            |

# §3 Edge-type catalogue


| Edge         | Subject Labels                                                                                                                        | Object Labels                                                                                                                                                                                                                                                                                                                                 | Cardinality | Purpose                                                                                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `IST`        | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`            | andere **Klassifikations-Labels** — **ausgenommen** `:Status` (**`HAT_STATUS`**) und **nicht** `:WiederverwendungsArt` mit **`axis: "reuse_strategie"`** auf `:Fallbeispiel`, `:Bauwerk` oder `:ReuseEinsatz` (**`HAT { art: "wiederverwendungsart" }`**)                                                             | N:1 typical | classification (not lifecycle; not *Art der Wiederverwendung* on case/building/action — that axis uses **`HAT`**)                                                      |
| `HAT`        | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:ReuseEinsatz`                                                                                     | weitere **Klassifikations-Labels** **oder** `:Akteur` (`art:'akteur', rolle:...`); inkl. **`HAT { art: "wiederverwendungsart" }` → `:WiederverwendungsArt`** (`axis: "reuse_strategie"`)                                                                                                                      | N:M         | qualitative attribute / actor participation / *Art der Wiederverwendung* (reuse-strategy axis)                                                                 |
| `HAT_STATUS` | `:Bauwerk`, `:ReuseEinsatz`, `:Fallbeispiel` (optional), `:Bauteilgruppe` (optional)                                                                         | `:Status`                                                                                                                                                                                                                                                                                                                                      | N:1 typical | lifecycle — **Gebäude/Anlage** kanonisch **`(:Bauwerk)`** (`bauobjektstatus/`); **Einsatz** (`:ReuseEinsatz`); optional Fallakte (`:Fallbeispiel`) / Gruppe (`:Bauteilgruppe`)                                                       |
| `BENUTZT`    | `:Bauteilgruppe`, `:ReuseEinsatz`, `:Bauwerk`, `:Fallbeispiel`                                                                                    | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Software`, `:Tool`, `:Datenmodell`                                                                                                                                                                                                                                | N:M         | instrumental usage; quantitative carrier                                                                                                                      |
| `GEHÖRT_ZU`  | any                                                                                                                                   | `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:Wiederverwendungskette`, `:Land`, `:Stadt`, `:Programm`, `:Software`                                                                                                                                                                                                                                                    | N:1 / N:M   | membership / **Bauwerk → Fallakte** (`rolle: 'fallbeispiel'`) / **ReuseEinsatz → Bauteilgruppe** (`rolle: 'bauteilgruppe'`) / **Tool → Software** (`rolle: 'software'`) / chain / location / origin                                                           |
| `BELEGT_IN`  | any node carrying a citable claim                                                                                                   | `:Quelle`                                                                                                                                                                                                                                                                                                                                      | N:M         | citation / evidence — the only place source attribution lives                                                                                                    |


## Legacy relations folded in

- **IST:** `has_bauteiltyp`, `has_bewertungslogik_abgrenzung` (→ `:WiederverwendungsArt` with `**axis: "einordnung"**` or `**"grundtyp"**` as applicable), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`. ( **`has_reuse_einsatzstatus` / `has_bauobjektstatus` → `HAT_STATUS` → `:Status`**. **`has_reuse_strategie` → `HAT { art: "wiederverwendungsart" }` → `:WiederverwendungsArt`** with `**axis: "reuse_strategie"**` — **six** canonical `id`s, §1; Subjekt typisch **`:ReuseEinsatz`**.)
- **HAT_STATUS:** `has_reuse_einsatzstatus`, `has_bauobjektstatus` (legacy) — **seven** canonical `:Status` `id`s (§1).
- **HAT:** `has_reuse_strategie` → **`HAT { art: "wiederverwendungsart" }`** → `:WiederverwendungsArt` (`axis: "reuse_strategie"`); `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff` → **`HAT { art: "huerde" }` → `:Huerde`** (Zielknoten aus `schadstoff/` mit `kategorie: "Schadstoff"`), `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung` → **only** `HAT {art:'verbindungstechnik'}` → `:Verbindungstechnik` per §1 Verbindungstabelle (technique subfolders); `**HAT {art:'reversibilitaet'}`** → `:Reversibilitaet` is **independent** (explicit metadata — not from `fuegung_verbindung/`), `has_logistik`, `has_wirtschaft`, plus actor participation `has_akteurrolle` → `HAT {art:'akteur', rolle:...}`, plus `has_entwurfsentscheidung` → `HAT {art:'entwurf'}` from `:ReuseEinsatz`, `:Bauteilgruppe`, `:Bauwerk`, or `:Fallbeispiel` to `:Entwurfsentscheidung`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool` → **`BENUTZT`** → **`(:Software)`** oder **`(:Tool)`** je §1.E, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt` → `rolle:'einbauort'` → Ziel **`(:Bauwerk)`** (subject often **`:ReuseEinsatz`** oder `:Bauteilgruppe`); `sourced_from_bauobjekt` → `rolle:'herkunft'` → **`(:Bauwerk)`**; **`:ReuseEinsatz` → `:Bauteilgruppe`** → `rolle:'bauteilgruppe'`; **`:Bauwerk` → `:Fallbeispiel`** → `rolle:'fallbeispiel'` (Fallakte); `part_of_reuse_kette` → `rolle:'kette'` (to `:Wiederverwendungskette`); **`:Tool` → `:Software`** → `rolle:'software'` (Host-Plattform, optional); `located_in_ort` → split: `rolle:'land'` (to `:Land`) and/or `rolle:'stadt'` (to `:Stadt`) depending on classified target; Legacy-Name `relates_to_bauobjekt` → dieselbe **`Bauwerk`→`Fallbeispiel`**-Kante mit `rolle:'fallbeispiel'`; `involves_foerderprogramm` / `has_programm_kontext` → `rolle:'programm'` (to `:Programm`). Ehemaliges **`has_kontextmerkmal` (Pilotprojekt)** → **`GEHÖRT_ZU { rolle: 'programm' }` → `(:Programm { id: "Pilotprojekt" })`** auch von Subjekten wie **`:Software`** / **`:Tool`** (§1.C).
- **BELEGT_IN:** replaces unresolved `quelle_label` shorthand on every node and every `quelle_id` previously planned as edge property. Replaces the gap relation `documented_in_quelle`. Direction: claim → `:Quelle`.

Dropped legacy relations (no destination): `belongs_to_fallstudie`, `belongs_to_projekt`, `has_projekt`, `has_bauobjekt`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_tragwerkstyp`, `has_dokumenttyp`, `has_akteurrolle` (target dropped), `measured_on_bauobjekt`, `measures_kennwertdefinition`, `involves_akteur` (collapsed into HAT).

---

# §4 Edges — properties per edge type

**Note:** None of IST / HAT / HAT_STATUS / BENUTZT / GEHÖRT_ZU carry a `quelle_id` or `quelle_label`. Source attribution lives exclusively on `:BELEGT_IN` edges from the edge's source node, optionally scoped via the `eigenschaft` property.

## §4.A `:IST`


| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.B `:HAT_STATUS`

Same optional properties as `**IST`** (temporal validity / confidence).


| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.C `:HAT`


| name          | type    | req | notes                                                                                                                                                                                                                                                                                                                                                             |
| ------------- | ------- | --- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `art`         | string  | ✓   | one of `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"recht"`, `"nutzung"`, `"intervention"`, `"verbindungstechnik"`, `"reversibilitaet"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"`, `"akteur"`, `"entwurf"`, `**"wiederverwendungsart"**` (→ `:WiederverwendungsArt` with `axis: "reuse_strategie"`) — **not** `"schadstoff"` (Stoff-Hürden: target **`(:Huerde)`** with `kategorie: "Schadstoff"` via **`art: "huerde"`**) |
| `rolle`       | string? | –   | required when `art='akteur'`; **must** be one of the **eight** canonical `:Akteurrolle.id` values in §1.D (e.g. `Planung_Gestaltung`, `Ausfuehrung_Logistik`) — **not** the raw legacy folder name under `akteurrolle/` |
| `anzahl`      | int?    | –   | multiplicity                                                                                                                                                                                                                                                                                                                                                      |
| `intensitaet` | string? | –   | qualitative strength                                                                                                                                                                                                                                                                                                                                              |
| `seit`        | date?   | –   |                                                                                                                                                                                                                                                                                                                                                                   |
| `bis`         | date?   | –   |                                                                                                                                                                                                                                                                                                                                                                   |


## §4.D `:BENUTZT`


| name             | type    | req | notes                               |
| ---------------- | ------- | --- | ----------------------------------- |
| `anzahl`         | float?  | –   | quantity used                       |
| `einheit`        | string? | –   | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float?  | –   | share-of-total                      |
| `funktion_alt`   | string? | –   | original role                       |
| `funktion_neu`   | string? | –   | new role                            |
| `aufbereitung`   | string? | –   | processing applied (free text)      |


## §4.E `:GEHÖRT_ZU`


| name       | type   | req | notes                                                                                                                                                  |
| ---------- | ------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rolle`    | string | ✓   | one of `"fallbeispiel"`, `"bauteilgruppe"`, `"einbauort"`, `"herkunft"`, `"zwischenlager"`, `"verarbeitung"`, `"transport"`, `"kette"`, `"land"`, `"stadt"`, `"programm"`, `"software"` |
| `position` | int?   | –   | order in sequence (e.g., chain station number)                                                                                                         |
| `seit`     | date?  | –   |                                                                                                                                                        |
| `bis`      | date?  | –   |                                                                                                                                                        |


## §4.F `:BELEGT_IN`

Direction: **(claim) → (:Quelle)**.


| name          | type    | req | notes                                                                                                                                |
| ------------- | ------- | --- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `eigenschaft` | string? | –   | scopes citation to a specific property of the source node (e.g. `"flaeche_m2"`, `"co2_einsparung_kg"`); omit for node-level citation |
| `seite`       | string? | –   | page number                                                                                                                          |
| `excerpt`     | string? | –   | quoted excerpt                                                                                                                       |
| `raw_label`   | string? | –   | original shorthand (`"S4"`, `"[S1]"`)                                                                                                |


---

# Appendix A — Modeling principles

- **Metadata-only graph.** German prose, raw labels, legacy paths, batch tags do not enter the graph. They stay in the source Markdown. **`title`** (plus optional `softwaretyp` / `tooltyp` / `anbieter` / `url` / `funktion` / `version` per §2) is stored **only** on **`(:Software)`** and **`(:Tool)`** — nowhere else on nodes.
- **Modes A/B/C coexist** but Mode A (property) is reserved for: identifiers, type discriminators (`art`, `programm_typ`, `axis`), and quantitative measurements (with `_alt`/`_vertrauensgrad` shadows).
- **Measurement placement.** Building-level → **`:Bauwerk`**. Fall-/Projektakte ohne separates Bauwerk → Messwerte nur auf `:Fallbeispiel`, wenn der Export kein `:Bauwerk` materialisiert (Ausnahme; Zielzustand: **`:Bauwerk`**). **Physical** component-group quantities → `:Bauteilgruppe`. **Reuse-action** KPIs (share, CO₂ impact, reuse targets) → `:ReuseEinsatz`. Inherently relational quantities → on the `BENUTZT` edge.
- **Role placement.** A role IS an edge property, never a node target. `:HAT {art:'akteur', rolle:'Planung_Gestaltung'}->(:Akteur)`. `:Akteurrolle` supplies **exactly eight** dictionary nodes (§1.D); `rolle` on the edge is **always** one of those canonical ids, mapped from legacy `akteurrolle/` folder names at export.
- **Citation placement.** Source attribution NEVER lives as a property. Always `:BELEGT_IN → :Quelle` with optional `eigenschaft` to scope.
- **Naming.** German PascalCase Labels, SCREAMING_SNAKE edges, snake_case properties.
- **`**:Status` (einheitlich).** Genau **sieben** Kanon-Knoten (§1). **`HAT_STATUS`** von **`:Bauwerk`** (Gebäude-/Anlagen-Lebenszyklus — kanonisch für `bauobjektstatus/`), **`(:ReuseEinsatz)`** (Einsatz-Lebenszyklus — kanonisch), optional **`(:Fallbeispiel)`** / **`(:Bauteilgruppe)`** → `:Status`. Label **`:Bauobjektstatus`** entfällt; Ordner `bauobjektstatus/` mappt auf dieselben Knoten.
- **`**:WiederverwendungsArt` — drei Achsen (`axis`).** *Art der Wiederverwendung* (Direkt, Umnutzung, …) ist **`axis: "reuse_strategie"`** auf **`(:WiederverwendungsArt)`** — **sechs** Kanon-`id`s (§1). **`(:Fallbeispiel)`**, **`(:Bauwerk)`** und **`(:ReuseEinsatz)`** verbinden diese Knoten nur per **`HAT { art: "wiederverwendungsart" }`** (kein eigener Kantentyp). **Einordnung** und **Grundtyp** bleiben **`axis: "einordnung"`** / **`"grundtyp"`** und werden von Fall/**Bauwerk**/**Einsatz**/Gruppe weiter über **`IST`** erreicht (Subjekt je nach Achse).
- **Verbindungstechnik vs Reversibilität.** Joining method (`:Verbindungstechnik`) comes only from `**fuegung_verbindung/`** technique folders. `**:Reversibilitaet**` is a separate `HAT` axis (`art:'reversibilitaet'`) with **no** `fuegung_verbindung/` provenance — not a “Verbindung” import. A value like “geschraubt” is not a reversibility class.
- **:Reversibilitaet vs :Methode `id:"Reversibilitaet"`.** The Label `**:Reversibilitaet`** holds the **detachability scale** (`Reversibel`, …) and is reached only via `HAT {art:'reversibilitaet'}` from `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, or `:ReuseEinsatz`. The folder `_database/methode/Reversibilitaet/` is a **different concept** (a methodological approach) and remains a `**:Methode`** node, typically linked with `**BENUTZT**`. Never merge these into one Label.
- **Constraint.** Every Label has `CREATE CONSTRAINT FOR (n:<Label>) REQUIRE n.id IS UNIQUE`.

# Appendix B — Constraints & indexes

- UNIQUE id per Label.
- Range indexes on `:Fallbeispiel(art)`, `:Bauwerk(art)`, `:Bauwerk(flaeche_m2)`, `:Bauwerk(fertigstellung_jahr)`, `:Bauteilgruppe(masse_t)`, `:ReuseEinsatz(co2_einsparung_kg)`, `:Akteur(art)`, `:Quelle(art)`.
- No full-text index (no body_md to index).

# Appendix C — Coverage checklist

The Labels in §1.A + §1.B + the drop/merge table in §1.C account for every folder under `_database/` (54 folders + `_edges` + `_system`). **Gesamt: 44 Neo4j-Labels** (§1.A + §1.B). Ordner **`kontextmerkmal/`** bleibt im Dateibaum, hat aber **kein** eigenes Neo4j-Label (§1.C). Ordner **`akteurrolle/`** bleibt mit vielen Unterordnern; im Graphen gibt es dafür nur **acht** `:Akteurrolle`-Knoten (§1.D).

YAML frontmatter fields on legacy `fallstudie` / `projekt` / `bauobjekt` / `reuse_einsatz` / `datenpunkt` / `akteur_beteiligung`:

- structural relations (`fallstudie:`, `projekt:`, `bauobjekt:`) → resolved or collapsed
- measurement fields (`wert:`, `einheit:`) → properties on **`:Bauwerk`** (Gebäudeebene), `:Bauteilgruppe` / `:ReuseEinsatz` (siehe §2 Messplatzierung), optional `:Fallbeispiel` nur wenn kein `:Bauwerk`-Knoten exportiert wird
- canonical-axis fields (`bauteiltyp:`, `material:`, …) → IST / BENUTZT edges to classification nodes
- raw labels (`bauteil_label:`, `material_label:`, `pruefung_label:`, `huerde_label:`, …) → NOT in the graph; remain only in the source Markdown
- prose `body` → NOT in the graph
- `quelle_label:` → resolved to `:Quelle` nodes + `:BELEGT_IN` edges
- `legacy_paths:`, `build_status:` → NOT in the graph
- **`akteurrolle/`** (viele Legacy-Unterordner) → **acht** kanonische **`(:Akteurrolle)`**-Knoten; `HAT.rolle` = Bund-`id` (§1.D)
- **`kontextmerkmal/`** (zwei Stubs) → **kein** `:Kontextmerkmal`-Knoten: **`Pilotprojekt`** → **`(:Programm { id: "Pilotprojekt" })`**; **`Bestandserhalt_Policy`** → kein Taxonomie-Knoten (§1.C)

# Appendix D — Renamings, drops, merges


| ------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fallstudie/` + `projekt/` (shared id)                                                                                 | merged into **`:Fallbeispiel`** — **Fall-/Projektakte**                                                                                                                      |
| `bauobjekt/` (pro physisches Bauwerk)                                                                                  | **`(:Bauwerk)`**; `GEHÖRT_ZU {rolle: 'fallbeispiel'}` → **`(:Fallbeispiel)`** bei gleicher Fall-ID                                                                           |
| `reuse_einsatz/`                                                                                                         | **`(:ReuseEinsatz)`** — eine Instanz pro Ordner; `GEHÖRT_ZU {rolle: 'bauteilgruppe'}` → **`(:Bauteilgruppe)`** wenn physische Gruppe materialisiert; kanonische physische Pfade weiterhin `**bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/**` |
| `reuse_kette/`                                                                                                           | renamed to `:Wiederverwendungskette` (kept; optional grouping)                                                                                                               |
| `reuse_kettenstation/`                                                                                                   | dropped — stations become GEHÖRT_ZU edges from `:ReuseEinsatz` (preferred) or `:Bauteilgruppe`                                                                               |
| `bewertungslogik_abgrenzung/`                                                                                            | renamed to `:WiederverwendungsArt`, absorbed values of dropped Bauteilgruppentyp via `axis` property                                                                         |
| `foerderprogramm/` + `programm_kontext/`                                                                                 | merged into `:Programm` with `programm_typ` property; **`kontextmerkmal/Pilotprojekt`** teilt denselben **`(:Programm { id: "Pilotprojekt" })`**-Knoten (§1.C)                                                                              |
| `kontextmerkmal/`                                                                                                        | **Label `:Kontextmerkmal` removed** — `Pilotprojekt` → `:Programm`; `Bestandserhalt_Policy` → keine Knoteninstanz (§1.C)                                                                 |
| `akteurrolle/`                                                                                                           | **21** Legacy-Unterordner → **acht** kanonische **`(:Akteurrolle)`**-Knoten; `HAT.rolle` nur Bund-`id` (§1.D)                                                                               |
| `akteur_beteiligung/` + `bauobjekt_beteiligung/`                                                                         | dropped — role lives as edge property on `HAT`                                                                                                                               |
| `bauobjektklasse/`                                                                                                       | dropped — values attach to **`:Bauwerk`** or **`:Fallbeispiel`** per export rule                                                                                                                           |
| `bauobjektrolle/`                                                                                                        | dropped — derivable from incoming `GEHÖRT_ZU` edges **to `:Bauwerk`**                                                                                                                                       |
| `dokumenttyp/`                                                                                                           | dropped — replaced by `:Quelle.art` (general values: Website / Interview / Paper / Buch / Bericht / Datenbank / Vortrag / Norm / Sonstige)                                   |
| `tragwerkstyp/`                                                                                                          | dropped — axis-mix; values folded into `:Material` or `:WiederverwendungsArt`                                                                                                |
| `kennwertdefinition/`                                                                                                    | dropped — kennwert-names become property names                                                                                                                               |
| `datenpunkt/`                                                                                                            | dropped — measurements become node properties                                                                                                                                |
| `software_digitaltool/` (früher monolithisch `:SoftwareDigitaltool`) | Split in **`(:Software)`** und **`(:Tool)`** nach §1.E; Legacy **`uses_software_digitaltool`** → **`BENUTZT`** → `:Software` \| `:Tool` |
| `schadstoff/`                                                                                                            | **Label `:Schadstoff` removed** — Unterordner → **`(:Huerde { id, kategorie: "Schadstoff" })`**; **`HAT { art: "huerde" }`** (§1.C) |
| All `body_md`, `legacy_paths`, `build_status`, `title`, raw-label properties on any node                                 | dropped — graph is metadata-only **except** `title` (and optional fields §1.E) on **`(:Software)`** / **`(:Tool)`** only                                                                                                                                             |
| Graph-`id` auf Instanz-Labels (`:Fallbeispiel`, `:Bauwerk`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`) | nicht zwingend 1:1 alter Ordner-/Dateiname — **Normalisierung** nach §1 **ID- und Namenskonvention (Lesbarkeit)** (ASCII, ein `_`, keine Listen/`_`_-Padding-Slugs)          |
| `:Bauteilgruppe` unter `bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`                                                           | Graph-`id` **=** Ordner-Slug (verbindliches Muster §1) — **physische** Gruppe                                                                                                                        |
| `:ReuseEinsatz` aus `reuse_einsatz/<id>/`                                                                              | Graph-`id` **=** Ordner-Slug; Verknüpfung zur Gruppe per `GEHÖRT_ZU {rolle: 'bauteilgruppe'}` — **Aktion** getrennt von **`:Bauteilgruppe`**                                                                 |
| `:BELEGT` (Quelle → claim)                                                                                               | reversed and renamed to `:BELEGT_IN` (claim → Quelle)                                                                                                                        |
| All `*_quelle`, `*_quellen`, `quelle_id`, `quelle_label_raw` properties anywhere                                         | dropped — replaced exclusively by `:BELEGT_IN` edges                                                                                                                         |
| `Moebelsepearat` value in WiederverwendungsArt                                                                           | renamed to `Moebel_separat`                                                                                                                                                  |
| `ort/Scwheiz`                                                                                                            | renamed to `ort/Schweiz`; export classifies the node as `:Land` or `:Stadt` (no `:Ort`)                                                                                      |
| `reuse_einsatzstatus/`                                                                                                   | merged into `**:Status`** — **seven** canonical `id`s + legacy mapping (§1); edges `**HAT_STATUS`** (not `IST`)                                                              |
| `bauobjektstatus/`                                                                                                       | merged into `**:Status`** (same seven nodes); `**:Bauobjektstatus` Label removed**; **`HAT_STATUS`** from `:Bauwerk` / `:ReuseEinsatz` (optional `:Fallbeispiel`, `:Bauteilgruppe`)                                                    |
| `has_reuse_strategie` / falsche `IST`-Anbindung der *Art der Wiederverwendung* ohne `:ReuseEinsatz`                    | use **`HAT { art: "wiederverwendungsart" }` → `:WiederverwendungsArt`** with **`axis: "reuse_strategie"`** — Subjekt typisch **`(:ReuseEinsatz)`**, auch **`(:Bauwerk)`** / **`(:Fallbeispiel)`** (§1 + Appendix E)                           |
| `reuse_strategie/`                                                                                                       | **Eleven** legacy folders → **six** `:WiederverwendungsArt` nodes (`axis: "reuse_strategie"`) — *Art der Wiederverwendung*; **`HAT`** von `:Fallbeispiel` / `:Bauwerk` / `:ReuseEinsatz`; **no** `:ReuseStrategie` Label |
| `fuegung_verbindung/`                                                                                                    | Label `:FuegungVerbindung` dropped → `**:Verbindungstechnik`** only (six technique folders; `Reversible_Fuegung/` not mapped to graph in this pipeline — see §1)             |
| `:Reversibilitaet` (detachability scale)                                                                                 | **Not** sourced from `fuegung_verbindung/`; own four nodes; `HAT { art: 'reversibilitaet' }` from explicit metadata only                                                     |
| Bauteiltyp drop-and-remap (SCHEMA.md §5)                                                                                 | already applied — noted in spec                                                                                                                                              |
| Material drop-and-merge (SCHEMA.md §6)                                                                                   | already applied — noted in spec                                                                                                                                              |


---

# Appendix E — `:WiederverwendungsArt` (`axis: "reuse_strategie"`): sechs Kanon-Knoten — *Art der Wiederverwendung* (verbindlich)

**Stand:** Es gelten **genau sechs** Knoten **`(:WiederverwendungsArt { axis: "reuse_strategie" })`** (Kanon-`id`s in §1). Legacy `reuse_strategie/` (**elf** Ordner) mappt beim Export auf diese `id`s + `axis`. Frühere 7er-Varianten sind **ersetzt**. **Kein** separates Label `:ReuseStrategie`; Anbindung von **`(:Fallbeispiel)`**, **`(:Bauwerk)`** und **`(:ReuseEinsatz)`** nur **`HAT { art: "wiederverwendungsart" }`**.

**Normative Tabelle (fachlich; Beispiele nur in Markdown-Quellen, nicht im Graphen):**


| Nr.   | Art der Wiederverwendung (`id`)      | Erklärung                                                                                                 | Beispiel                                                            |
| ----- | ------------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **1** | `Bestandserhalt_Weiterbauen`         | Gebäude oder große Gebäudeteile bleiben erhalten und werden angepasst.                                    | Fabrik wird zu Wohnhaus, Tragwerk bleibt bestehen                   |
| **2** | `In_situ_Wiederverwendung`           | Bauteile bleiben am ursprünglichen Ort und werden weitergenutzt.                                          | Treppe, Decke, Fassade oder Wand bleibt im Gebäude                  |
| **3** | `Direkte_Wiederverwendung`           | Bauteil wird ausgebaut und an anderer Stelle mit gleicher Funktion wieder eingebaut.                      | Tür bleibt Tür, Fenster bleibt Fenster                              |
| **4** | `Wiederverwendung_nach_Aufarbeitung` | Bauteil wird gereinigt, repariert, geprüft oder angepasst (inkl. DfD / Remanufacturing als Aufbereitung). | Ziegel reinigen, Parkett schleifen, Stahlträger prüfen              |
| **5** | `Umnutzung_Repurposing`              | Bauteil erhält eine neue Funktion.                                                                        | Fenster wird Innenwand, Tür wird Tischplatte                        |
| **6** | `Kaskade_Downcycling_Bauteilebene`   | Bauteil wird in einer weniger anspruchsvollen Funktion weitergenutzt.                                     | tragendes Holz wird Innenausbau, Fassadenplatten werden Gartenbelag |


**Technische Umsetzung:** Legacy→Kanon-Mapping in **§1** unter **Reuse-Strategie-Konsolidierung**. *Hinweis Export:* `Upcycling` → `Umnutzung_Repurposing` ist eine **Heuristik** (häufig funktionale Neuausrichtung); bei reinem Qualitäts-/Aufarbeitungspfad kann der Export alternativ `Wiederverwendung_nach_Aufarbeitung` setzen, wenn die Fallakte das trägt.

---

## Final counts

- **44** Labels total (**9** primär in §1.A + **35** in §1.B)
- **6** edge types (`IST`, `HAT`, `HAT_STATUS`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN`)
- **0** body / legacy / prose on nodes **except** `title` (+ optional §1.E fields) on **`(:Software)`** / **`(:Tool)`** only

## Deliverable: schema map file


| File                                                                             | Purpose                                                                                                                                                                                                                                 |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[_database/_system/NEO4J_SCHEMA.md](_database/_system/NEO4J_SCHEMA.md)`         | Vollständige Spezifikation inkl. Erklärungen, Hierarchie, Legacy-Mappings, Anhänge                                                                                                                                                      |
| `[_database/_system/NEO4J_SCHEMA_MAP.md](_database/_system/NEO4J_SCHEMA_MAP.md)` | **Kompakte Gesamtlandkarte:** alle **Knotentypen (Labels)** mit **allen Knoten-Properties**; alle **Kantentypen** mit **allen Kanten-Properties** und erlaubten Quell-/Ziel-Labels (kein erzählender Doppeltext — tabellarisch / flach) |


Die Map dient Lesern und Tools als **einzige Checkliste** „was gibt es im Graphen als Typ + Property“. Änderungen am Schema **immer** in beiden Dateien nachziehen (oder später aus einer gemeinsamen Quelle generieren — siehe Goal).

## Out of scope (this plan)

- Writing the **data** export script (Markdown → Neo4j bulk-load).
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.

