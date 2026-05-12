---
name: Neo4j schema catalogue
overview: Metadata-only Neo4j schema. The graph carries identifiers, classifications, measurements, and relationships — NOT German prose. body_md / legacy_paths / build_status / raw labels live only in the source Markdown, never in the graph. **44** Neo4j Labels total (six primary case / component / source types plus thirty-eight folder-backed classification types). **Each node has exactly one Label** — no umbrella or secondary label on nodes. Seven edge types (IST, HAT, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, BENUTZT, GEHÖRT_ZU, BELEGT_IN). All source attribution is via :BELEGT_IN edges to :Quelle nodes.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md (full spec) and _database/_system/NEO4J_SCHEMA_MAP.md (compact map: all Labels + properties, all edge types + properties). Same 4+appendix content order in the main spec; the map is a flattened reference."
    status: pending
  - id: write-1
    content: "Write §1 Node-type catalogue: all **44** Labels (six primary + thirty-eight folder-backed types), one-line purpose each. Confirm against _database/ folder list."
    status: pending
  - id: write-2
    content: "Write §2 Nodes: per-Label property tables. ONLY metadata properties — no body, no legacy_paths, no raw labels, no build_status."
    status: pending
  - id: write-3
    content: "Write §3 Edge-type catalogue: seven edge types (IST, HAT, HAT_STATUS, HAT_WIEDERVERWENDUNGSART, BENUTZT, GEHÖRT_ZU, BELEGT_IN) with source/target Label families and the legacy relations folded into each."
    status: pending
  - id: write-4
    content: "Write §4 Edges: per-edge-type property table. :BELEGT_IN is the only citation edge."
    status: pending
  - id: schema-map
    content: "Write _database/_system/NEO4J_SCHEMA_MAP.md: (A) every Label with full property table, (B) every relationship type with source/target Label patterns, cardinality, and full edge-property table. Mirror §2–§4; update whenever NEO4J_SCHEMA.md changes."
    status: pending
isProject: false
---

# Goal

Author `_database/_system/NEO4J_SCHEMA.md` in the four-part order: §1 Node-type catalogue → §2 Nodes (properties) → §3 Edge-type catalogue → §4 Edges (properties). Plus appendices.

Author a **separate compact map** [`_database/_system/NEO4J_SCHEMA_MAP.md`](_database/_system/NEO4J_SCHEMA_MAP.md) that duplicates nothing narratively but **lists the full machine-oriented catalogue** in one place:

1. **Nodes:** every Neo4j **Label** (all **44** types), each with its **complete property list** (name, type, required, notes) as in §2.
2. **Edges:** every **relationship type** (all **seven**), each with **allowed source Labels → target Labels**, cardinality, and **complete edge property list** (name, type, required, notes) as in §3–§4.

The map must stay **in lockstep** with `NEO4J_SCHEMA.md` when the schema changes. Optional later: generate the map from a single YAML/JSON source of truth — not required for the first authoring pass.

**Key principle: the graph carries metadata only.** German prose, raw labels, legacy file paths, build-batch status — none of this is in the graph. It stays in the Markdown source under `_database/`. The graph carries identifiers (ids), classifications (edges), and quantitative facts (measurement properties).

---

# Hierarchiebaum — alle Knotentypen, Knoten, Eigenschaften; alle Kantentypen, Kanten, Eigenschaften

Lesen: **Knotentyp** = Neo4j-Label. **Knoten** = eine Instanz (ein Unterordner oder ein zusammengeführter Datensatz). **Knoteneigenschaften** = Properties auf diesem Knoten. **Kantentyp** = Relationship-Typ. **Kante** = eine konkrete Relationship zwischen zwei Knoten. **Kanteneigenschaften** = Properties auf der Kante.

Kontrollierte Begriffsknoten (z. B. `:Material`, `:Status`): jedes `id` entspricht in der Regel dem Unterordnernamen unter dem passenden `_database/<label>/<id>/` (Prosa nur in `index.md`, nicht im Graphen). Jeder solche Knoten hat **genau ein** Label — seinen Typnamen.

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
│       └── je ein Knoten pro `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` (siehe §1 ID-Konvention `:Bauteilgruppe`)
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
├── KNOTENTYP :ReuseStrategie
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bestandserhalt_Weiterbauen, In_situ_Wiederverwendung, Direkte_Wiederverwendung, Wiederverwendung_nach_Aufarbeitung, Umnutzung_Repurposing, Kaskade_Downcycling_Bauteilebene
├── KNOTENTYP :Status
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Geplant, In_Bau, Realisiert, Prototyp, Rueckgebaut, Nicht_Realisiert, Unklar
├── KNOTENTYP :WiederverwendungsArt
│   ├── Knoteneigenschaften: id (Pflicht), axis (Pflicht: einordnung | grundtyp)
│   └── Knoten: Bestandserhalt_Nicht_Direct_Reuse, Kein_Direct_Reuse_Nachweis, Moebel_Dekoration_Nicht_Direct_Reuse, Recycling_Nicht_Direct_Reuse, Reuse_Anteil_Unklar, Ungebaut_Nicht_Realisierte_Wiederverwendung, Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung
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
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Akzeptanzproblem, Anschlussproblem, Aufbereitungsaufwand, Ausschreibungsproblem, Bauproduktstatus, Brandschutzkonflikt, Bruch_Beschaedigungsrisiko, Datenluecke, Dauerhaftigkeit_Restlebensdauer, Entwurfsbindung, Fehlende_Datenstandards, Fehlende_Lagerflaeche, Fehlende_Standardisierung, Gewaehrleistung, Haftung, Heterogenitaet_Chargen, Hygieneanforderung, Kompatibilitaetsproblem, Materialqualitaet_Unklar, Mengenunsicherheit, Schadstoffbelastung, Technische_Freigabe, Terminunsicherheit, Toleranzen, Unkonventionelles_Material, Verfuegbarkeitsproblem, Witterung_Feuchte, Zustand_Unklar
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
├── KNOTENTYP :Schadstoff
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Asbest, Bleifarbe, Holzschutzmittel, PAK, PCB
├── KNOTENTYP :Nutzung
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Buero, Gewerbe, Infrastruktur, Kultur, Lager_Depot, Mischnutzung, Schule_Bildung, Sozialbau, Wohnen
├── KNOTENTYP :BauaufgabeIntervention
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Aufstockung, Erweiterung, Fit_out, Neubau, Rueckbau, Sanierung, Translozierung, Umbau, Umnutzung, Wiederaufbau
├── KNOTENTYP :Kontextmerkmal
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bestandserhalt_Policy, Pilotprojekt
├── KNOTENTYP :Entwurfsentscheidung
│   ├── Knoteneigenschaften: id (Pflicht), beschreibung? (string)
│   └── Knoten: Etagenhoehe_durch_Bauteilmass, Fassadenschicht_als_Toleranzpuffer, Doppelfenster_als_Kastenfenster, Achsraster_nach_Bestand, Grundriss_nach_Bauteillaenge, Deckenhoehe_nach_Traegerhoehe, Anschlussdetail_angepasst, Erschliessungskern_verschoben
├── KNOTENTYP :Land
│   ├── Knoteneigenschaften: id (Pflicht), iso_country? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
├── KNOTENTYP :Stadt
│   ├── Knoteneigenschaften: id (Pflicht), koordinaten? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
├── KNOTENTYP :Akteurrolle (nur Wörterbuch; Rolle als Property auf HAT, nicht als IST-Ziel)
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Architektur, Aufbereitung_Refurbishment, Bauausfuehrung, Bauherr_Auftraggeber, Betreiber_Nutzer, Brandschutz_Barrierefreiheit, Fassade, Forschung_Dokumentation, Kunst_Gestaltung, Landschaftsplanung, Materiallieferant, Nachhaltigkeitsberatung, Oeffentliche_Hand, Projektbeteiligte_Unbestimmt, Projektmanagement_Koordination, Pruefung_Qualitaetssicherung, Reuse_Beratung, Rueckbau_Demontage, Stahlbau_Fertigung, TGA_Gebaeudetechnik, Tragwerksplanung
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
    └── Knoten: BBSM, FCRBE, PREUSE, Reallabor_Be_Ware, Zukunftbau, Foerderprogramm, Forschungsprojekt, Kommunales_Programm, Pilotprojekt, Reallabor, Wettbewerb

KANTEN (alle sieben Typen; jede Kante ist eine Instanz zwischen zwei Knoten)

├── KANTENTYP IST
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung?
│   └── Kante (Beispielmuster)
│       └── (:Fallbeispiel|:Bauteilgruppe|:Akteur|:Quelle|:SoftwareDigitaltool|:Wiederverwendungskette) -[IST]-> (:<KlassifikationsLabel> {id})   (nicht :Status / :ReuseStrategie auf :Fallbeispiel oder :Bauteilgruppe — siehe HAT_STATUS / HAT_WIEDERVERWENDUNGSART)
│
├── KANTENTYP HAT
│   ├── Kanteneigenschaften: art (Pflicht), rolle? (Pflicht wenn art=akteur), anzahl?, intensitaet?, seit?, bis?
│   └── Kante (Beispielmuster)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: huerde|prozessphase|pruefung|norm|…}]-> (:Huerde|:Prozessphase|:Norm|…)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: verbindungstechnik}]-> (:Verbindungstechnik)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: reversibilitaet}]-> (:Reversibilitaet)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: akteur, rolle: "<Akteurrolle.id>"}]-> (:Akteur)
│       └── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: entwurf}]-> (:Entwurfsentscheidung)
│
├── KANTENTYP HAT_STATUS
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung? (optional — gleiche Semantik wie bei IST)
│   └── Kante (Beispielmuster)
│       └── (:Fallbeispiel|:Bauteilgruppe) -[HAT_STATUS]-> (:Status {id})   Hinweis: historisch „Bauobjekt“ = :Fallbeispiel. Beispiel: (:Fallbeispiel)-[:HAT_STATUS]->(:Status {id: "Realisiert"})
│
├── KANTENTYP HAT_WIEDERVERWENDUNGSART
│   ├── Kanteneigenschaften: seit?, bis?, gewichtung? (optional)
│   └── Kante (Beispielmuster)
│       └── (:Fallbeispiel)-[HAT_WIEDERVERWENDUNGSART]-> (:ReuseStrategie {id})   Ziel-Label :ReuseStrategie (sechs Kanon-ids, §1). Kurz „Umnutzung“ -> id Umnutzung_Repurposing. Nicht :WiederverwendungsArt (Einordnung). Beispiel: (:Fallbeispiel)-[:HAT_WIEDERVERWENDUNGSART]->(:ReuseStrategie {id: "Umnutzung_Repurposing"})
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
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: land}]-> (:Land)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: stadt}]-> (:Stadt)
│       ├── (:Fallbeispiel) -[GEHÖRT_ZU {rolle: programm}]-> (:Programm)
│       └── (weitere) je nach Export-Regeln
│
└── KANTENTYP BELEGT_IN
    ├── Kanteneigenschaften: eigenschaft?, seite?, excerpt?, raw_label?
    └── Kante (Beispielmuster)
        └── (:Fallbeispiel|:Bauteilgruppe|…) -[BELEGT_IN]-> (:Quelle)
```

Hinweis: Ordner ohne eigenen Knotentyp (z. B. `datenpunkt/`, `kennwertdefinition/`, `fallstudie/`) sind in §1.C des Plans aufgeführt — sie erzeugen **keine** eigenen Knoten im Zielgraphen, sondern fließen in Properties, Kanten oder Merges ein.

## Autoritativer vertikaler Gesamtbaum — Knoten (Node Types + Nodes + Properties)

Diese Liste ist die gewünschte Zielform für die finale Schema-Datei: **ein Knotentyp, darunter jeder Knoten einzeln vertikal, mit seinen Properties direkt daneben**. Keine horizontalen Kommalisten in der finalen Fassung.

Format-Regel (wichtig für die Lesbarkeit): Jede Zeile, die mit `(:<Label>` beginnt, definiert **genau einen** Knoten. Diese Zeile enthält alle Knoten-Properties **im selben Zeilen-Block** (keine zweizeiligen Node-Definitionen). Die Properties stehen als genau ein `{...}`-Block (z. B. `{id: "Stahl", axis: "grundtyp"}`). **Alle `id`-Werte** folgen zusätzlich der Tabelle **„ID- und Namenskonvention (Lesbarkeit)“** in §1 (ASCII, keine Listenzeichen, keine `__`-Monster-Slugs).

Die folgenden Blöcke zeigen **Muster** (nicht die vollständige Knotenzahl). Die endgültige Exportliste folgt §1 **ID- und Namenskonvention (Lesbarkeit)**.

```text
:Fallbeispiel
  (:Fallbeispiel {id: "Berlin_Schildow_Pilot_Haus", art: "Gebaeude"})
  (:Fallbeispiel {id: "55_Great_Suffolk_Street_London", art: "Lager"})
  (:Fallbeispiel {id: "K118_Halle_118_Winterthur", art: "Halle"})
  (:Fallbeispiel {id: "AWM_Muenster_Circular_Office", art: "Innenausbau"})
  ... (alle weiteren Fallbeispiele: ASCII, logische Wortfolge, keine Sonderzeichen-Mojibake)

:Bauteilgruppe
  (:Bauteilgruppe {id: "K118_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "K118_C02_Treppe"})
  (:Bauteilgruppe {id: "ELYS_C01_Fenster"})
  (:Bauteilgruppe {id: "Plattenpalast_C01_Wandplatten"})
  (:Bauteilgruppe {id: "55GSS_C01_Traeger_Stuetzen"})
  (:Bauteilgruppe {id: "CRCLR_C02_Wandpaneele"})
  (:Bauteilgruppe {id: "Werkhof29_C01_Fassadenbleche"})
  ... (Muster `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` — Graph-`id` = Ordner-Slug)

:Akteur
  (:Akteur {id: "Circular_Berlin"})
  (:Akteur {id: "Circular_Structural_Design"})
  (:Akteur {id: "Bellastock"})
  (:Akteur {id: "Arup"})
  (:Akteur {id: "Dirk_Hebel"})
  ... (eine Organisation oder Person pro Knoten — keine `A;B,C`-Listen in `id`)

:Quelle
  (:Quelle {id: "BBSR_Zukunft_Bau_foerderprogramm", art: "Website"})
  (:Quelle {id: "Circular_Berlin_marktstudie_wiederverwendung", art: "Bericht"})
  (:Quelle {id: "Bellastock_research_note", art: "Paper"})
  ... (kurze Zitations-Slugs — nicht `akteur_04_..._md` oder Roh-Dateinamen)

:SoftwareDigitaltool
  (:SoftwareDigitaltool {id: "Concular_Plattform"})
  (:SoftwareDigitaltool {id: "IfcOpenShell"})
  (:SoftwareDigitaltool {id: "BIM"})
  (:SoftwareDigitaltool {id: "Globechain"})
  ... (Produkt- oder Markenname lesbar; einheitliche Schreibweise pro Eintrag)

:Wiederverwendungskette
  (:Wiederverwendungskette {id: "55_Great_Suffolk_Street_London"})
  (:Wiederverwendungskette {id: "K118_Halle_118_Winterthur"})
  (:Wiederverwendungskette {id: "House_of_Fraser_Oxford_Street_London_reuse_chain"})
  ... (typisch an Fallbeispiel gebunden; gleiches Kurz-Muster wie zugehöriges `(:Fallbeispiel {id:…})` wenn 1:1)

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

:ReuseStrategie
  (:ReuseStrategie {id: "Bestandserhalt_Weiterbauen"})
  (:ReuseStrategie {id: "In_situ_Wiederverwendung"})
  (:ReuseStrategie {id: "Direkte_Wiederverwendung"})
  (:ReuseStrategie {id: "Wiederverwendung_nach_Aufarbeitung"})
  (:ReuseStrategie {id: "Umnutzung_Repurposing"})
  (:ReuseStrategie {id: "Kaskade_Downcycling_Bauteilebene"})

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

:Schadstoff
  (:Schadstoff {id: "Asbest"})
  (:Schadstoff {id: "Bleifarbe"})
  (:Schadstoff {id: "Holzschutzmittel"})
  (:Schadstoff {id: "PAK"})
  (:Schadstoff {id: "PCB"})

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

:Kontextmerkmal
  (:Kontextmerkmal {id: "Bestandserhalt_Policy"})
  (:Kontextmerkmal {id: "Pilotprojekt"})

:Land
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Pla
:Stadt
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Plan

:Akteurrolle
  (:Akteurrolle {id: "Architektur"})
  (:Akteurrolle {id: "Aufbereitung_Refurbishment"})
  (:Akteurrolle {id: "Bauausfuehrung"})
  (:Akteurrolle {id: "Bauherr_Auftraggeber"})
  (:Akteurrolle {id: "Betreiber_Nutzer"})
  (:Akteurrolle {id: "Brandschutz_Barrierefreiheit"})
  (:Akteurrolle {id: "Fassade"})
  (:Akteurrolle {id: "Forschung_Dokumentation"})
  (:Akteurrolle {id: "Kunst_Gestaltung"})
  (:Akteurrolle {id: "Landschaftsplanung"})
  (:Akteurrolle {id: "Materiallieferant"})
  (:Akteurrolle {id: "Nachhaltigkeitsberatung"})
  (:Akteurrolle {id: "Oeffentliche_Hand"})
  (:Akteurrolle {id: "Projektbeteiligte_Unbestimmt"})
  (:Akteurrolle {id: "Projektmanagement_Koordination"})
  (:Akteurrolle {id: "Pruefung_Qualitaetssicherung"})
  (:Akteurrolle {id: "Reuse_Beratung"})
  (:Akteurrolle {id: "Rueckbau_Demontage"})
  (:Akteurrolle {id: "Stahlbau_Fertigung"})
  (:Akteurrolle {id: "TGA_Gebaeudetechnik"})
  (:Akteurrolle {id: "Tragwerksplanung"})

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

Same rule for every folder: `_database/material/<x>/` produces `(:Material {id: "<x>"})`, `_database/huerde/<x>/` produces `(:Huerde {id: "<x>"})`, etc.

**`id` vs. Ordnername:** Für die **38** folder-gestützten Labels in §1.B ist `id` in der Regel **gleich** dem Unterordnernamen (ggf. ASCII nach derselben Tabelle). Für **`:Bauteilgruppe`** im kanonischen Ordner **`bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`** ist Graph-`id` **gleich** dem Unterordner-Slug (verbindliches Muster — siehe Tabelle unten). Für die übrigen **fünf** Primär-Labels in §1.A (`:Fallbeispiel`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette`) ist `id` der **vom Export normalisierte** Slug nach der folgenden Tabelle — der Quellordnername ist nur Eingabe, nicht zwingend 1:1 der Graph-`id`.

**ID- und Namenskonvention (Lesbarkeit)**

| Regel | Vorgabe |
|-------|---------|
| Zeichensatz | **ASCII** in `id`. Umlaute als `ae`, `oe`, `ue`, `ss` (keine kaputten Fragmente wie `Tr_ger`, `T_ren`). |
| Trenner | Nur **einfaches** `_` zwischen Wortteilen. **Keine** doppelten `__` als Padding, **keine** `;` oder `,` innerhalb einer `id`. |
| Ein Knoten | **Eine** reale Entität pro Knoten — **keine** Listen (`A;B,C`) in einer `id`. Mehrere Akteure → mehrere `:Akteur`-Knoten + mehrere Kanten. |
| Länge | Kurz halten: bevorzugt **≤ 48** Zeichen pro `id` (harte Grenze im Export z. B. 96). |
| `:Fallbeispiel` | `id` = erkennbarer **Projekt- oder Orts-Slug**, z. B. `Berlin_Schildow_Pilot_Haus`, `55_Great_Suffolk_Street_London` — Wortfolge logisch lesbar. |
| `:Bauteilgruppe` | **Verbindliches Muster** (Ordner + Graph-`id`): `_database/bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` → `(:Bauteilgruppe {id: "<CASE>_C<NN>_<ELEMENT>"})`. **`CASE`**: kurzer, stabiler Projektcode (ASCII, oft Kürzel des `:Fallbeispiel`, z. B. `K118`, `ELYS`, `55GSS`, `CRCLR`, `Werkhof29`, `Plattenpalast`). **`<NN>`**: zweistellige laufende Nummer pro Fall (`01`…`99`). **`<ELEMENT>`**: snake_case-Bauteilgruppenname (ASCII, lesbar). Beispiele: `K118_C01_Traeger_Stuetzen`, `K118_C02_Treppe`, `ELYS_C01_Fenster`, `Plattenpalast_C01_Wandplatten`, `55GSS_C01_Traeger_Stuetzen`, `CRCLR_C02_Wandpaneele`, `Werkhof29_C01_Fassadenbleche`. Anbindung an `:Fallbeispiel` über `GEHÖRT_ZU {rolle:'einbauort'}` (o. ä.); `CASE` muss nicht 1:1 dem langen `Fallbeispiel.id` entsprechen. Legacy `reuse_einsatz/` wird beim Export auf dieses Muster **gemappt oder umbenannt**. |
| `:Akteur` | `id` = **Organisationskurzname** in konsistentem Wortbild (`Circular_Berlin`, `Circular_Structural_Design`, `Bellastock`) oder **Person** `Vorname_Nachname`. Keine technischen Pfad-Präfixe. |
| `:Quelle` | `id` = **kurzer Zitations-Slug**, z. B. `Circular_Berlin_marktstudie_2023` — **nicht** gespiegelte Dateipfade wie `akteur_04_planung_..._md`. |
| `:SoftwareDigitaltool` | Produkt- oder Plattformname lesbar (`Concular_Plattform`, `IfcOpenShell`); einheitliche Groß-/Kleinschreibung pro Eintrag. |
| `:Wiederverwendungskette` | `id` an Fallbeispiel anbindbar (`K118_Halle_118_Winterthur`) oder eigener kurzer Kettenname — ohne URL-artige Monsterstrings. |
| Weitere `_database`-Labels (§1.B) | `id` = stabiler Term-Slug; gleiche ASCII-/Trennerregeln; Ordner unter `_database/<label>/` möglichst schon so benannt, damit Import trivial bleibt. |

Exceptions (folders that are NOT 1:1 a node type) are listed in §1.C — they merge into another Label, get renamed, or are dropped.

**Geography exception:** `_database/ort/<id>/` is not mapped to a single `:Ort` Label. On export, each slug becomes either `(:Land {id})` or `(:Stadt {id})` according to a classification rule (country/region vs city/district/site). The plan does not enumerate those node ids.

**`:Status` — vereinheitlicht (Gebäude- + Einsatz-Lebenszyklus):** Label **`:ReuseEinsatzstatus`** und **`:Bauobjektstatus`** entfallen. Es gibt **genau sieben** `:Status`-Knoten. Anbindung nur über **`HAT_STATUS`** (nicht `IST`) von **`(:Fallbeispiel)`** und **`(:Bauteilgruppe)`** an `:Status`.

| Kanon-`id` (`:Status`) | Kurzbedeutung |
|--------|---------------|
| `Geplant` | noch nicht in Ausführung / Konkurrenzphase |
| `In_Bau` | in Ausführung |
| `Realisiert` | fertiggestellt und (ggf.) in Nutzung |
| `Prototyp` | Versuchs-/Pilotstand |
| `Rueckgebaut` | Rückbau / Abbruch abgeschlossen |
| `Nicht_Realisiert` | nicht umgesetzt / verworfen |
| `Unklar` | nicht eindeutig zuordenbar |

**Legacy `reuse_einsatzstatus/<id>/` → `(:Status {id})`:**

| Legacy `reuse_einsatzstatus/<id>/` | → Kanon-`id` |
|---|---|
| `Geplant` | `Geplant` |
| `Vorgeschlagen` | `Geplant` |
| `Prototypisch` | `Prototyp` |
| `Realisiert` | `Realisiert` |
| `Temporaer` | `Realisiert` (oder `Prototyp` — Heuristik nach Fallakte) |
| `Verworfen` | `Nicht_Realisiert` |
| `Unklar` | `Unklar` |

**Legacy `bauobjektstatus/<id>/` → `(:Status {id})`:** (Ordner `bauobjektstatus/` mappt auf dieselben sieben Knoten; Label `:Bauobjektstatus` entfällt.)

| Legacy `bauobjektstatus/<id>/` | → Kanon-`id` |
|---|---|
| `Gebaut` | `Realisiert` |
| `Geplant` | `Geplant` |
| `In_Bau` | `In_Bau` |
| `Prototyp` | `Prototyp` |
| `Rueckgebaut` | `Rueckgebaut` |
| `Temporaer` | `Prototyp` (oder `Realisiert` — Heuristik) |
| `Unklar` | `Unklar` |
| `Wettbewerb` | `Geplant` |

**Reuse-Strategie-Konsolidierung (verbindlich — 6 Kanon-Knoten):** Legacy `reuse_strategie/` hat **elf** Unterordner; im Graphen gibt es **genau sechs** `:ReuseStrategie`-Knoten nach **Art der Wiederverwendung** (Gebäude-/Bauteilnutzung, nicht Marketing-Jargon). **`(:Fallbeispiel)`** (synonym historisch **Bauobjekt**) und optional **`(:Bauteilgruppe)`** verbinden die Strategie über **`HAT_WIEDERVERWENDUNGSART`** → `:ReuseStrategie` — **nicht** über `IST`. Ausführliche Beispiele bleiben in den Markdown-Quellen; im Graphen nur Kanon-`id`.

| Nr. | Kanon-`id` (`:ReuseStrategie`) | Leitidee (Kurz) |
|-----|----------------|----------------|
| **1** | `Bestandserhalt_Weiterbauen` | Gebäude oder große Gebäudeteile bleiben erhalten und werden angepasst. |
| **2** | `In_situ_Wiederverwendung` | Bauteile bleiben am ursprünglichen Ort und werden weitergenutzt. |
| **3** | `Direkte_Wiederverwendung` | Bauteil wird ausgebaut und an anderer Stelle mit **gleicher Funktion** wieder eingebaut. |
| **4** | `Wiederverwendung_nach_Aufarbeitung` | Bauteil wird gereinigt, repariert, geprüft oder angepasst (inkl. konstruktive **Vorbereitung** auf spätere Demontage / DfD-Logik). |
| **5** | `Umnutzung_Repurposing` | Bauteil erhält eine **neue Funktion**. |
| **6** | `Kaskade_Downcycling_Bauteilebene` | Bauteil wird in einer **weniger anspruchsvollen** Funktion weitergenutzt (inkl. stofflicher Rückführung / Bestandserschließung aus Altbestand). |

| Legacy `reuse_strategie/<id>/` | → Kanon-`id` |
|---|---|
| `Bestandserhalt`, `Weiterbauen_im_Bestand`, `Refurbishment`, `Adaptives_ReUse` | `Bestandserhalt_Weiterbauen` |
| `Same_Site_ReUse` | `In_situ_Wiederverwendung` |
| `Direkte_Wiederverwendung` | `Direkte_Wiederverwendung` |
| `Remanufacturing`, `Design_for_Disassembly` | `Wiederverwendung_nach_Aufarbeitung` |
| `Upcycling` | `Umnutzung_Repurposing` |
| `Recycling`, `Urban_Mining` | `Kaskade_Downcycling_Bauteilebene` |

**Fügung/Verbindung → nur Verbindungstechnik:** Legacy folder `fuegung_verbindung/` enthielt gemischte Begriffe; im Graphen wird **ausschließlich die Verbindungs-/Fügetechnik** über **`:Verbindungstechnik`** abgebildet (`HAT {art:'verbindungstechnik'}`). **`:Reversibilitaet` gehört nicht zu „Verbindungen“** in diesem Sinne: kein Import aus `fuegung_verbindung/` für dieses Label, keine Zeile in der folgenden Tabelle.

| Legacy `fuegung_verbindung/<id>/` | Target Label | Canonical node `id` |
|---|---|---|
| `Verschraubung` | `:Verbindungstechnik` | `Geschraubt` |
| `Verschweissung` | `:Verbindungstechnik` | `Geschweisst` |
| `Steckverbindung` | `:Verbindungstechnik` | `Gesteckt` |
| `Verleimung` | `:Verbindungstechnik` | `Geklebt` |
| `Vermoertelung` | `:Verbindungstechnik` | `Vergossen` |
| `Klemmverbindung` | `:Verbindungstechnik` | `Klemmverbindung` |

| Legacy `fuegung_verbindung/Reversible_Fuegung/` | Graph (dieser Plan) |
|---|---|
| (gesamter Ordner) | **Kein** automatischer Export zu `:Verbindungstechnik` oder `:Reversibilitaet`; Inhalt bleibt in Markdown / spätere eigenständige Kuratierung außerhalb der Verbindungs-Pipeline. |

**`:Reversibilitaet` — nur eigener Knotentyp:** Label **`:Reversibilitaet`** mit genau vier Knoten (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`), eigene **UNIQUE-Constraint** auf `(n:Reversibilitaet).id`, ausschließlich **`HAT {art:'reversibilitaet'}`** von `:Fallbeispiel` / `:Bauteilgruppe`. Datenquelle: **explizite** Metadaten (z. B. künftiges Feld / Kuratierung) — **nicht** `fuegung_verbindung/`, **nicht** `IST`, keine Einbettung unter `:Verbindungstechnik`.

## §1.A Primär-Labels (6)


| Label                     | Purpose                                                     | Replaces (legacy folders)                                          |
| ------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| `:Fallbeispiel`           | One physical case-study object                              | `fallstudie/` + `projekt/` + `bauobjekt/` (merged where ids match) |
| `:Bauteilgruppe`          | A group of components in a Fallbeispiel — the reuse-Einsatz | `bauteilgruppe/` (Zielordner; `id`-Muster `<CASE>_C<NN>_<ELEMENT>` — siehe §1); Legacy: `reuse_einsatz/` → Migration auf dieses Muster |
| `:Akteur`                 | Office / company / authority / institution / person         | `akteur/`                                                          |
| `:Quelle`                 | Source / citation target                                    | `quelle/`                                                          |
| `:SoftwareDigitaltool`    | Concrete platform                                           | `software_digitaltool/`                                            |
| `:Wiederverwendungskette` | OPTIONAL named multi-Bauteilgruppe reuse program            | `reuse_kette/` (renamed; `reuse_kettenstation/` dropped)           |


## §1.B Weitere Labels (38 — jeder `_database/<label>/`-Ordner; `ort/` splits into two Labels; `fuegung_verbindung/` → **`:Verbindungstechnik`** only; **`:Reversibilitaet`** is a separate node type without `fuegung_verbindung/` provenance; `reuse_strategie/` → **six** `:ReuseStrategie` nodes — see exception table; **`bauobjektstatus/`** merged into **`:Status`** — see §1 Status tables)

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

- `:Reversibilitaet` ← **kein** `fuegung_verbindung/`-Bezug; **vier feste** Knoten; nur `HAT {art:'reversibilitaet'}`; Daten nur aus **expliziten** Quellen (nicht aus der Verbindungs-Migration). **Nicht** dasselbe wie `methode/Reversibilitaet/` → weiterhin `(:Methode {id: "Reversibilitaet"})` per **`BENUTZT`**.

**Konstruktion:**

- `:Bauweise` ← `bauweise/`
- `:Bausystem` ← `bausystem/`
- `:Tragwerksprinzip` ← `tragwerksprinzip/`

**Reuse:**

- `:ReuseStrategie` ← `reuse_strategie/` (**eleven** legacy folders → **six** canonical `id`s — **Art der Wiederverwendung**; **`HAT_WIEDERVERWENDUNGSART`** from `:Fallbeispiel` / `:Bauteilgruppe` — see **Reuse-Strategie-Konsolidierung** in §1)
- `:Status` ← `reuse_einsatzstatus/` + **`bauobjektstatus/`** (**merged** — **seven** canonical nodes; **Label `:Bauobjektstatus` dropped**; see §1 Status tables; edges **`HAT_STATUS`** from `:Fallbeispiel` / `:Bauteilgruppe`)
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

- `:Nutzung` ← `nutzung/`
- `:BauaufgabeIntervention` ← `bauaufgabe_intervention/`
- `:Kontextmerkmal` ← `kontextmerkmal/`
- `:Entwurfsentscheidung` ← **new** — no legacy folder; created fresh. Label capturing design adaptations forced by reuse constraints. Connected via `HAT {art:'entwurf'}` from `:Bauteilgruppe` (component-specific) or `:Fallbeispiel` (project-wide). Initial values defined from K.118 example and generalised across all case data.

**Geographie:**

- `:Land` ← each qualifying entry from `ort/` (export classification: country / macro-region)
- `:Stadt` ← each qualifying entry from `ort/` (export classification: city, borough, or project-scale site id)

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


| Folder                        | Disposition                                                                                                                    |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `fallstudie/`                 | merged into `:Fallbeispiel`                                                                                                    |
| `projekt/`                    | merged into `:Fallbeispiel`                                                                                                    |
| `bauobjekt/`                  | merged into `:Fallbeispiel`                                                                                                    |
| `reuse_einsatz/`              | renamed to `:Bauteilgruppe`; Zielablage **`bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`** mit Graph-`id` = Ordner-Slug (§1 ID-Konvention)                                                              |
| `reuse_kettenstation/`        | dropped — stations become GEHÖRT_ZU edges from `:Bauteilgruppe`                                                                |
| `akteur_beteiligung/`         | dropped — collapsed to `HAT {art:'akteur', rolle:...}` edge                                                                    |
| `bauobjekt_beteiligung/`      | dropped — same pattern                                                                                                         |
| `datenpunkt/`                 | dropped — measurements as node properties                                                                                      |
| `kennwertdefinition/`         | dropped — kennwert-names live as property names                                                                                |
| `bauobjektklasse/`            | dropped — values collapse into `:Fallbeispiel.art`                                                                             |
| `bauobjektrolle/`             | dropped — donor/receiver/standalone derivable from incoming GEHÖRT_ZU edges (`rolle:'herkunft'` / `rolle:'einbauort'`)         |
| `dokumenttyp/`                | dropped — replaced by `:Quelle.art`                                                                                            |
| `tragwerkstyp/`               | dropped — axis-mix (review §7.8); material values derivable from `:Material`, reuse values folded into `:WiederverwendungsArt` |
| `foerderprogramm/`            | merged into `:Programm`                                                                                                        |
| `programm_kontext/`           | merged into `:Programm`                                                                                                        |
| `bewertungslogik_abgrenzung/` | renamed to `:WiederverwendungsArt`                                                                                             |
| `bauobjektstatus/`            | merged into `:Status` — **seven** canonical `id`s (§1); dedicated **`HAT_STATUS`** edges; Label `:Bauobjektstatus` removed |
| `reuse_kette/`                | renamed to `:Wiederverwendungskette`                                                                                           |


Total: 54 folders → **44** Neo4j Labels (§1.A + §1.B) + 11 dropped + 4 merged-or-renamed (`ort/` yields two Labels; `fuegung_verbindung/` → `:Verbindungstechnik` only — `:Reversibilitaet` has no folder provenance; `reuse_strategie/` → **six** `:ReuseStrategie` nodes; `bauobjektstatus/` + `reuse_einsatzstatus/` → **one** `:Status` Label with **seven** canonical nodes).

---

# §2 Nodes — properties per Label

Property table columns: **name** | **type** | **req** | **notes**.

**No `body_md`, no `title`, no `legacy_paths`, no `build_status`, no raw-text labels on any node.** All German prose stays in the source Markdown under `_database/<entity>/<id>/index.md`, outside the graph.

## §2.A `:Fallbeispiel`


| name  | type   | req | notes                                                                                             |
| ----- | ------ | --- | ------------------------------------------------------------------------------------------------- |
| `id`  | string | ✓   | UNIQUE; nach §1 **ID-Konvention** normalisierter Slug (Export), lesbar; nicht zwingend 1:1 alter Ordnername |
| `art` | string | ✓   | one of `"Gebaeude"`, `"Bruecke"`, `"Pavillon"`, `"Halle"`, `"Lager"`, `"Innenausbau"`, `"Anlage"` |


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

## §2.B `:Bauteilgruppe`


| name | type   | req | notes  |
| ---- | ------ | --- | ------ |
| `id` | string | ✓   | UNIQUE; verbindlich `<CASE>_C<NN>_<ELEMENT>` wie in §1 (Ordner `bauteilgruppe/<id>/`) |


**Component-group measurement properties:**


| name                       | type   | notes                     |
| -------------------------- | ------ | ------------------------- |
| `masse_t`                  | float? |                           |
| `anzahl_stueck`            | int?   |                           |
| `volumen_m3`               | float? |                           |
| `flaeche_m2`               | float? | component area            |
| `anteil_prozent`           | float? | share of receiver's total |
| `co2_einsparung_kg`        | float? |                           |
| `co2_reduktion_kg`         | float? |                           |
| `geerntete_materialien_t`  | float? |                           |
| `sekundaere_materialien_t` | float? |                           |
| `abfall_vermieden_t`       | float? |                           |
| `zielwert_reuse_prozent`   | float? |                           |


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


| name  | type    | req | notes                                                                                                                   |
| ----- | ------- | --- | ----------------------------------------------------------------------------------------------------------------------- |
| `id`  | string  | ✓   | UNIQUE; lesbarer Organisations- oder Personen-Slug (§1 ID-Konvention); **keine** Listen in einem `id` |
| `art` | string? | –   | optional: `"Firma"`, `"Buero"`, `"Behoerde"`, `"Institution"`, `"Person"`, `"Verband"`, `"Bauherrschaft"`, `"Sonstige"` |
| `url` | string? | –   | website / firm page                                                                                                     |


## §2.D `:Quelle`


| name  | type    | req | notes                                                                                                                   |
| ----- | ------- | --- | ----------------------------------------------------------------------------------------------------------------------- |
| `id`  | string  | ✓   | UNIQUE; kurzer Zitations-Slug (§1 ID-Konvention), z. B. `Circular_Berlin_marktstudie_2023` — nicht Roh-Dateipfad |
| `art` | string  | ✓   | one of `"Website"`, `"Interview"`, `"Paper"`, `"Buch"`, `"Bericht"`, `"Datenbank"`, `"Vortrag"`, `"Norm"`, `"Sonstige"` |
| `url` | string? | –   | source URL or DOI                                                                                                       |


No outgoing edges from `:Quelle`. All metadata about a citation (page, excerpt, raw shorthand, scoped property) lives on the incoming `:BELEGT_IN` edge.

## §2.E `:SoftwareDigitaltool`


| name  | type    | req | notes  |
| ----- | ------- | --- | ------ |
| `id`  | string  | ✓   | UNIQUE; Produkt-/Plattform-Slug (§1 ID-Konvention), z. B. `Concular_Plattform`, `IfcOpenShell` |
| `url` | string? | –   |        |


## §2.F `:Wiederverwendungskette`


| name         | type   | req | notes  |
| ------------ | ------ | --- | ------ |
| `id`         | string | ✓   | UNIQUE; typisch gleiches Kurz-Muster wie zugehöriges `:Fallbeispiel` oder eigener Kettenname (§1 ID-Konvention) |
| `start_jahr` | int?   | –   |        |
| `end_jahr`   | int?   | –   |        |


## §2.G Weitere Labels — gemeinsame Minimal-Properties (§1.B)

Die meisten Labels in §1.B haben **so viele Knoten wie Unterordner** unter dem jeweiligen `_database/<label>/`-Pfad. Beispiel: `_database/material/` mit `Stahl`, `Holz`, `Beton`, … → je ein `(:Material {id: "…"})`. **Ausnahmen:** `:Land` / `:Stadt` (Geographie-Exception); `:Status` (**sieben** feste Kanon-`id`s aus **zusammengeführtem** `reuse_einsatzstatus/` + `bauobjektstatus/` — §1; nur **`HAT_STATUS`**); `:ReuseStrategie` (**elf** Legacy-Ordner → **sechs** Kanon-`id`s — §1); `:Verbindungstechnik` (Technik-Ordner unter `fuegung_verbindung/` — §1; `Reversible_Fuegung/` ausgeschlossen); `:Reversibilitaet` (**vier** feste Knoten, **kein** `fuegung_verbindung/` — §1).

Jeder dieser Knoten hat standardmäßig nur:


| name | type   | req | notes                                                                       |
| ---- | ------ | --- | --------------------------------------------------------------------------- |
| `id` | string | ✓   | UNIQUE within the Label; in der Regel der Unterordnername unter `_database/<label>/<id>/`, normalisiert nach §1 (ASCII, ein `_` zwischen Wortteilen) |


The id is the queryable identifier. The German prose body explaining the term remains in the source Markdown `_database/<label>/<id>/index.md`, outside the graph.

Zusätzliche Properties nur bei ausgewählten Labels:


| Label                   | extra property               | notes                                                                                                                                       |
| ----------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `:Land`                 | `iso_country: string?`       | optional ISO country code                                                                                                                   |
| `:Stadt`                | `koordinaten: string?`       | optional coordinates string                                                                                                                 |
| `:Programm`             | `programm_typ: string` (req) | `"foerderung"` or `"forschungskontext"`                                                                                                     |
| `:WiederverwendungsArt` | `axis: string` (req)         | `"einordnung"` (legacy bewertungslogik values) or `"grundtyp"` (wiederverwendet/original/hybrid — absorbed from dropped :Bauteilgruppentyp) |
| `:Status`               | —                            | exactly **seven** nodes (`Geplant`, `In_Bau`, `Realisiert`, `Prototyp`, `Rueckgebaut`, `Nicht_Realisiert`, `Unklar`); legacy `reuse_einsatzstatus/` + `bauobjektstatus/` map per §1; edges **`HAT_STATUS`** only |
| `:ReuseStrategie`       | —                            | exactly **six** canonical `id`s (see §1 **Reuse-Strategie-Konsolidierung**); **eleven** legacy `reuse_strategie/` folders map to those ids |
| `:Verbindungstechnik`  | —                            | six canonical technique ids (see §1); legacy `fuegung_verbindung/` technique folders remap to these `id` values |
| `:Reversibilitaet`      | —                            | exactly **four** nodes (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`); **not** sourced from `fuegung_verbindung/` (see §1) |


---

# §3 Edge-type catalogue


| Edge                     | Subject Labels                                                                                             | Object Labels                                                                                                    | Cardinality  | Purpose                                                       |
| ------------------------ | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------- |
| `IST`                    | `:Fallbeispiel`, `:Bauteilgruppe`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette` | andere **Klassifikations-Labels** als Ziel — **ausgenommen** `:Status` und `:ReuseStrategie`, wenn Subjekt **`:Fallbeispiel` oder `:Bauteilgruppe`** (dann `HAT_STATUS` / `HAT_WIEDERVERWENDUNGSART`) | N:1 typical | classification (not lifecycle / not reuse-strategy on case or component) |
| `HAT`                    | `:Fallbeispiel`, `:Bauteilgruppe`                                                                          | weitere **Klassifikations-Labels** **oder** `:Akteur` (mit `art:'akteur', rolle:...`)                                                   | N:M          | qualitative attribute / actor participation                   |
| `HAT_STATUS`             | `:Fallbeispiel`, `:Bauteilgruppe`                                                                          | `:Status`                                                                                              | N:1 typical  | lifecycle / realisation state (seven canonical `id`s — §1)   |
| `HAT_WIEDERVERWENDUNGSART` | `:Fallbeispiel`, `:Bauteilgruppe` (optional)                                                             | `:ReuseStrategie`                                                                                      | N:1 typical  | *Art der Wiederverwendung* — six canonical `id`s (§1)        |
| `BENUTZT`                | `:Bauteilgruppe`, `:Fallbeispiel`                                                                          | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:SoftwareDigitaltool`, `:Datenmodell` | N:M          | instrumental usage; quantitative carrier                      |
| `GEHÖRT_ZU`              | any                                                                                                        | `:Fallbeispiel`, `:Wiederverwendungskette`, `:Land`, `:Stadt`, `:Programm`                                       | N:1 / N:M    | membership / containment / location / chain station / origin  |
| `BELEGT_IN`              | any node carrying a citable claim                                                                          | `:Quelle`                                                                                                        | N:M          | citation / evidence — the only place source attribution lives |


## Legacy relations folded in

- **IST:** `has_bauteiltyp`, `has_bewertungslogik_abgrenzung` (→ `:WiederverwendungsArt`), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`. ( **`has_reuse_einsatzstatus` / `has_bauobjektstatus` → `HAT_STATUS` → `:Status`**. **`has_reuse_strategie` → `HAT_WIEDERVERWENDUNGSART` → `:ReuseStrategie`**.)
- **HAT_STATUS:** `has_reuse_einsatzstatus`, `has_bauobjektstatus` (legacy) — **seven** canonical `:Status` `id`s (§1).
- **HAT_WIEDERVERWENDUNGSART:** `has_reuse_strategie` — **six** canonical `:ReuseStrategie` `id`s (§1).
- **HAT:** `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff`, `has_kontextmerkmal`, `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung` → **only** `HAT {art:'verbindungstechnik'}` → `:Verbindungstechnik` per §1 Verbindungstabelle (technique subfolders); **`HAT {art:'reversibilitaet'}`** → `:Reversibilitaet` is **independent** (explicit metadata — not from `fuegung_verbindung/`), `has_logistik`, `has_wirtschaft`, plus actor participation `has_akteurrolle` → `HAT {art:'akteur', rolle:...}`, plus `has_entwurfsentscheidung` → `HAT {art:'entwurf'}` from `:Bauteilgruppe` or `:Fallbeispiel` to `:Entwurfsentscheidung`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool`, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt` → `rolle:'einbauort'`; new `sourced_from_bauobjekt` → `rolle:'herkunft'`; `part_of_reuse_kette` → `rolle:'kette'` (to `:Wiederverwendungskette`); `located_in_ort` → split: `rolle:'land'` (to `:Land`) and/or `rolle:'stadt'` (to `:Stadt`) depending on classified target; `relates_to_bauobjekt` → `rolle:'fallbeispiel'`; `involves_foerderprogramm` / `has_programm_kontext` → `rolle:'programm'` (to `:Programm`).
- **BELEGT_IN:** replaces unresolved `quelle_label` shorthand on every node and every `quelle_id` previously planned as edge property. Replaces the gap relation `documented_in_quelle`. Direction: claim → `:Quelle`.

Dropped legacy relations (no destination): `belongs_to_fallstudie`, `belongs_to_projekt`, `has_projekt`, `has_bauobjekt`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_tragwerkstyp`, `has_dokumenttyp`, `has_akteurrolle` (target dropped), `measured_on_bauobjekt`, `measures_kennwertdefinition`, `involves_akteur` (collapsed into HAT).

---

# §4 Edges — properties per edge type

**Note:** None of IST / HAT / HAT_STATUS / HAT_WIEDERVERWENDUNGSART / BENUTZT / GEHÖRT_ZU carry a `quelle_id` or `quelle_label`. Source attribution lives exclusively on `:BELEGT_IN` edges from the edge's source node, optionally scoped via the `eigenschaft` property.

## §4.A `:IST`


| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.B `:HAT_STATUS`

Same optional properties as **`IST`** (temporal validity / confidence).

| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.C `:HAT_WIEDERVERWENDUNGSART`

Same optional properties as **`IST`**.

| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.D `:HAT`


| name          | type    | req | notes                                                                                                                                                                                                                                    |
| ------------- | ------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `art`         | string  | ✓   | one of `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"schadstoff"`, `"kontext"`, `"recht"`, `"nutzung"`, `"intervention"`, `"verbindungstechnik"`, `"reversibilitaet"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"`, `"akteur"`, `"entwurf"` |
| `rolle`       | string? | –   | required when `art='akteur'`; e.g. `"Architektur"`, `"Tragwerksplanung"`, `"Bauherr_Auftraggeber"`; validates against `:Akteurrolle.id`                                                                                                  |
| `anzahl`      | int?    | –   | multiplicity                                                                                                                                                                                                                             |
| `intensitaet` | string? | –   | qualitative strength                                                                                                                                                                                                                     |
| `seit`        | date?   | –   |                                                                                                                                                                                                                                          |
| `bis`         | date?   | –   |                                                                                                                                                                                                                                          |


## §4.E `:BENUTZT`


| name             | type    | req | notes                               |
| ---------------- | ------- | --- | ----------------------------------- |
| `anzahl`         | float?  | –   | quantity used                       |
| `einheit`        | string? | –   | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float?  | –   | share-of-total                      |
| `funktion_alt`   | string? | –   | original role                       |
| `funktion_neu`   | string? | –   | new role                            |
| `aufbereitung`   | string? | –   | processing applied (free text)      |


## §4.F `:GEHÖRT_ZU`


| name       | type   | req | notes                                                                                                                                                  |
| ---------- | ------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rolle`    | string | ✓   | one of `"fallbeispiel"`, `"einbauort"`, `"herkunft"`, `"zwischenlager"`, `"verarbeitung"`, `"transport"`, `"kette"`, `"land"`, `"stadt"`, `"programm"` |
| `position` | int?   | –   | order in sequence (e.g., chain station number)                                                                                                         |
| `seit`     | date?  | –   |                                                                                                                                                        |
| `bis`      | date?  | –   |                                                                                                                                                        |


## §4.G `:BELEGT_IN`

Direction: **(claim) → (:Quelle)**.


| name          | type    | req | notes                                                                                                                                |
| ------------- | ------- | --- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `eigenschaft` | string? | –   | scopes citation to a specific property of the source node (e.g. `"flaeche_m2"`, `"co2_einsparung_kg"`); omit for node-level citation |
| `seite`       | string? | –   | page number                                                                                                                          |
| `excerpt`     | string? | –   | quoted excerpt                                                                                                                       |
| `raw_label`   | string? | –   | original shorthand (`"S4"`, `"[S1]"`)                                                                                                |


---

# Appendix A — Modeling principles

- **Metadata-only graph.** German prose, raw labels, legacy paths, batch tags do not enter the graph. They stay in the source Markdown.
- **Modes A/B/C coexist** but Mode A (property) is reserved for: identifiers, type discriminators (`art`, `programm_typ`, `axis`), and quantitative measurements (with `_alt`/`_vertrauensgrad` shadows).
- **Measurement placement.** Building-level → `:Fallbeispiel`. Component-group-level → `:Bauteilgruppe`. Inherently relational quantities → on the `BENUTZT` edge.
- **Role placement.** A role IS an edge property, never a node target. `:HAT {art:'akteur', rolle:'Architektur'}->(:Akteur)`. `:Akteurrolle` is a dictionary of allowed `rolle` strings, not an IST target.
- **Citation placement.** Source attribution NEVER lives as a property. Always `:BELEGT_IN → :Quelle` with optional `eigenschaft` to scope.
- **Naming.** German PascalCase Labels, SCREAMING_SNAKE edges, snake_case properties.
- **`:Status` (einheitlich).** Genau **sieben** Kanon-Knoten (§1). **`HAT_STATUS`** von `:Fallbeispiel` (historisch „Bauobjekt“) und `:Bauteilgruppe` → `:Status`. Label **`:Bauobjektstatus`** entfällt; Ordner `bauobjektstatus/` mappt auf dieselben Knoten.
- **`:ReuseStrategie` vs. `:WiederverwendungsArt`.** *Art der Wiederverwendung* (Direkt, Umnutzung, …) liegt auf **`:ReuseStrategie`** und wird mit **`HAT_WIEDERVERWENDUNGSART`** an **`(:Fallbeispiel)`** (optional `:Bauteilgruppe`) angebunden — Kanon-`id` z. B. `Umnutzung_Repurposing` (Kurzwort „Umnutzung“ ist keine eigene Graph-`id`). **`:WiederverwendungsArt`** bleibt die **Einordnungs-/Grundtyp**-Taxonomie (`axis`) und wird weiter über **`IST`** erreicht.
- **Verbindungstechnik vs Reversibilität.** Joining method (`:Verbindungstechnik`) comes only from **`fuegung_verbindung/`** technique folders. **`:Reversibilitaet`** is a separate `HAT` axis (`art:'reversibilitaet'`) with **no** `fuegung_verbindung/` provenance — not a “Verbindung” import. A value like “geschraubt” is not a reversibility class.
- **:Reversibilitaet vs :Methode `id:"Reversibilitaet"`.** The Label **`:Reversibilitaet`** holds the **detachability scale** (`Reversibel`, …) and is reached only via `HAT {art:'reversibilitaet'}`. The folder `_database/methode/Reversibilitaet/` is a **different concept** (a methodological approach) and remains a **`:Methode`** node, typically linked with **`BENUTZT`**. Never merge these into one Label.
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
- canonical-axis fields (`bauteiltyp:`, `material:`, …) → IST / BENUTZT edges to classification nodes
- raw labels (`bauteil_label:`, `material_label:`, `pruefung_label:`, `huerde_label:`, …) → NOT in the graph; remain only in the source Markdown
- prose `body` → NOT in the graph
- `quelle_label:` → resolved to `:Quelle` nodes + `:BELEGT_IN` edges
- `legacy_paths:`, `build_status:` → NOT in the graph

# Appendix D — Renamings, drops, merges


| Change                                                                                   | Action                                                                                                                                     |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `fallstudie/` + `projekt/` + `bauobjekt/` (shared id)                                    | merged into `:Fallbeispiel` with `art` property                                                                                            |
| `reuse_einsatz/`                                                                         | renamed to `:Bauteilgruppe`; kanonische Pfade **`bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`** (siehe §1)                                                                                                                |
| `reuse_kette/`                                                                           | renamed to `:Wiederverwendungskette` (kept; optional grouping)                                                                             |
| `reuse_kettenstation/`                                                                   | dropped — stations become GEHÖRT_ZU edges from `:Bauteilgruppe`                                                                            |
| `bewertungslogik_abgrenzung/`                                                            | renamed to `:WiederverwendungsArt`, absorbed values of dropped Bauteilgruppentyp via `axis` property                                       |
| `foerderprogramm/` + `programm_kontext/`                                                 | merged into `:Programm` with `programm_typ` property                                                                                       |
| `akteur_beteiligung/` + `bauobjekt_beteiligung/`                                         | dropped — role lives as edge property on `HAT`                                                                                             |
| `bauobjektklasse/`                                                                       | dropped — values collapse into `:Fallbeispiel.art`                                                                                         |
| `bauobjektrolle/`                                                                        | dropped — derivable from incoming GEHÖRT_ZU edges                                                                                          |
| `dokumenttyp/`                                                                           | dropped — replaced by `:Quelle.art` (general values: Website / Interview / Paper / Buch / Bericht / Datenbank / Vortrag / Norm / Sonstige) |
| `tragwerkstyp/`                                                                          | dropped — axis-mix; values folded into `:Material` or `:WiederverwendungsArt`                                                              |
| `kennwertdefinition/`                                                                    | dropped — kennwert-names become property names                                                                                             |
| `datenpunkt/`                                                                            | dropped — measurements become node properties                                                                                              |
| All `body_md`, `legacy_paths`, `build_status`, `title`, raw-label properties on any node | dropped — graph is metadata-only                                                                                                           |
| Graph-`id` auf Instanz-Labels (`:Fallbeispiel`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette`) | nicht zwingend 1:1 alter Ordner-/Dateiname — **Normalisierung** nach §1 **ID- und Namenskonvention (Lesbarkeit)** (ASCII, ein `_`, keine Listen/`__`-Padding-Slugs) |
| `:Bauteilgruppe` unter `bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/` | Graph-`id` **=** Ordner-Slug (verbindliches Muster §1); Migration von Legacy `reuse_einsatz/` mappt auf dieses Muster |
| `:BELEGT` (Quelle → claim)                                                               | reversed and renamed to `:BELEGT_IN` (claim → Quelle)                                                                                      |
| All `*_quelle`, `*_quellen`, `quelle_id`, `quelle_label_raw` properties anywhere         | dropped — replaced exclusively by `:BELEGT_IN` edges                                                                                       |
| `Moebelsepearat` value in WiederverwendungsArt                                           | renamed to `Moebel_separat`                                                                                                                |
| `ort/Scwheiz`                                                                            | renamed to `ort/Schweiz`; export classifies the node as `:Land` or `:Stadt` (no `:Ort`)                                                    |
| `reuse_einsatzstatus/`                                                                   | merged into **`:Status`** — **seven** canonical `id`s + legacy mapping (§1); edges **`HAT_STATUS`** (not `IST`) |
| `bauobjektstatus/`                                                                       | merged into **`:Status`** (same seven nodes); **`:Bauobjektstatus` Label removed**; **`HAT_STATUS`** from `:Fallbeispiel` |
| `has_reuse_strategie` / `IST→:ReuseStrategie` on `:Fallbeispiel`                          | use **`HAT_WIEDERVERWENDUNGSART` → `:ReuseStrategie`** (six canonical `id`s — §1 + Appendix E) |
| `reuse_strategie/`                                                                       | **Eleven** legacy folders → **six** `:ReuseStrategie` canonical `id`s — *Art der Wiederverwendung* (§1 + Appendix E)                         |
| `fuegung_verbindung/`                                                                     | Label `:FuegungVerbindung` dropped → **`:Verbindungstechnik`** only (six technique folders; `Reversible_Fuegung/` not mapped to graph in this pipeline — see §1) |
| `:Reversibilitaet` (detachability scale)                                                  | **Not** sourced from `fuegung_verbindung/`; own four nodes; `HAT { art: 'reversibilitaet' }` from explicit metadata only |
| Bauteiltyp drop-and-remap (SCHEMA.md §5)                                                 | already applied — noted in spec                                                                                                            |
| Material drop-and-merge (SCHEMA.md §6)                                                   | already applied — noted in spec                                                                                                            |


---

# Appendix E — `ReuseStrategie`: sechs Kanon-Knoten — *Art der Wiederverwendung* (verbindlich)

**Stand:** Es gelten **genau sechs** `:ReuseStrategie`-Knoten (Kanon-`id`s in §1). Legacy `reuse_strategie/` (**elf** Ordner) mappt beim Export auf diese `id`s. Frühere 7er-Varianten sind **ersetzt**.

**Normative Tabelle (fachlich; Beispiele nur in Markdown-Quellen, nicht im Graphen):**

| Nr. | Art der Wiederverwendung (`id`) | Erklärung | Beispiel |
|-----|-----------------------------------|-----------|----------|
| **1** | `Bestandserhalt_Weiterbauen` | Gebäude oder große Gebäudeteile bleiben erhalten und werden angepasst. | Fabrik wird zu Wohnhaus, Tragwerk bleibt bestehen |
| **2** | `In_situ_Wiederverwendung` | Bauteile bleiben am ursprünglichen Ort und werden weitergenutzt. | Treppe, Decke, Fassade oder Wand bleibt im Gebäude |
| **3** | `Direkte_Wiederverwendung` | Bauteil wird ausgebaut und an anderer Stelle mit gleicher Funktion wieder eingebaut. | Tür bleibt Tür, Fenster bleibt Fenster |
| **4** | `Wiederverwendung_nach_Aufarbeitung` | Bauteil wird gereinigt, repariert, geprüft oder angepasst (inkl. DfD / Remanufacturing als Aufbereitung). | Ziegel reinigen, Parkett schleifen, Stahlträger prüfen |
| **5** | `Umnutzung_Repurposing` | Bauteil erhält eine neue Funktion. | Fenster wird Innenwand, Tür wird Tischplatte |
| **6** | `Kaskade_Downcycling_Bauteilebene` | Bauteil wird in einer weniger anspruchsvollen Funktion weitergenutzt. | tragendes Holz wird Innenausbau, Fassadenplatten werden Gartenbelag |

**Technische Umsetzung:** Legacy→Kanon-Mapping in **§1** unter **Reuse-Strategie-Konsolidierung**. *Hinweis Export:* `Upcycling` → `Umnutzung_Repurposing` ist eine **Heuristik** (häufig funktionale Neuausrichtung); bei reinem Qualitäts-/Aufarbeitungspfad kann der Export alternativ `Wiederverwendung_nach_Aufarbeitung` setzen, wenn die Fallakte das trägt.

---

## Final counts

- **44** Labels total (**6** primär in §1.A + **38** in §1.B)
- **7** edge types (`IST`, `HAT`, `HAT_STATUS`, `HAT_WIEDERVERWENDUNGSART`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN`)
- **0** body / legacy / prose properties (metadata-only)

## Deliverable: schema map file

| File | Purpose |
|------|---------|
| [`_database/_system/NEO4J_SCHEMA.md`](_database/_system/NEO4J_SCHEMA.md) | Vollständige Spezifikation inkl. Erklärungen, Hierarchie, Legacy-Mappings, Anhänge |
| [`_database/_system/NEO4J_SCHEMA_MAP.md`](_database/_system/NEO4J_SCHEMA_MAP.md) | **Kompakte Gesamtlandkarte:** alle **Knotentypen (Labels)** mit **allen Knoten-Properties**; alle **Kantentypen** mit **allen Kanten-Properties** und erlaubten Quell-/Ziel-Labels (kein erzählender Doppeltext — tabellarisch / flach) |

Die Map dient Lesern und Tools als **einzige Checkliste** „was gibt es im Graphen als Typ + Property“. Änderungen am Schema **immer** in beiden Dateien nachziehen (oder später aus einer gemeinsamen Quelle generieren — siehe Goal).

## Out of scope (this plan)

- Writing the **data** export script (Markdown → Neo4j bulk-load).
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.

