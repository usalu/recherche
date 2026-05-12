---
name: Neo4j schema catalogue
overview: Metadata-only Neo4j schema. The graph carries identifiers, classifications, measurements, and relationships — NOT German prose. body_md / legacy_paths / build_status / raw labels live only in the source Markdown, never in the graph. Six instance Labels (:Fallbeispiel, :Bauteilgruppe, :Akteur, :Quelle, :SoftwareDigitaltool, :Wiederverwendungskette) and 39 vocabulary Labels (covering every folder under _database/). Five generic edges (IST, HAT, BENUTZT, GEHÖRT_ZU, BELEGT_IN). All source attribution is via :BELEGT_IN edges to :Quelle nodes.
todos:
  - id: spec-skeleton
    content: "Create _database/_system/NEO4J_SCHEMA.md with the 4-section structure: §1 Node-type catalogue, §2 Nodes (per-Label property tables), §3 Edge-type catalogue, §4 Edges (per-edge-type property tables). Plus appendices for principles, constraints, coverage (every folder → Label/drop), renamings."
    status: pending
  - id: write-1
    content: "Write §1 Node-type catalogue: 6 instance Labels and the 39 vocabulary Labels, with one-line purpose each. Confirm against _database/ folder list."
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
isProject: false
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
├── KNOTENTYP :Verbindungstechnik:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Geschraubt, Geschweisst, Gesteckt, Geklebt, Vergossen, Klemmverbindung
├── KNOTENTYP :Bauweise:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fertigteilbauweise, Holzbauweise, Hybridbauweise, Massivbauweise, Ortbetonbauweise, Stahlbauweise
├── KNOTENTYP :Bausystem:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Betonfertigteil_System, Holzrahmenbau, Holz_Skelettbau, Plattenbau, Stahl_Skelettbau
├── KNOTENTYP :Tragwerksprinzip:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Fachwerk, Skeletttragwerk, Wandtragwerk, Wand_Kern_Tragwerk
├── KNOTENTYP :Reversibilitaet:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Reversibel, Teilweise_reversibel, Irreversibel, Unbekannt
├── KNOTENTYP :ReuseStrategie:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Bestandserhalt_Weiterbauen, In_situ_Wiederverwendung, Direkte_Wiederverwendung, Wiederverwendung_nach_Aufarbeitung, Umnutzung_Repurposing, Kaskade_Downcycling_Bauteilebene
├── KNOTENTYP :Status:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht)
│   └── Knoten: Gebaut, Geplant, Realisiert, Nicht_Realisiert
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
├── KNOTENTYP :Entwurfsentscheidung:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht), beschreibung? (string)
│   └── Knoten: Etagenhoehe_durch_Bauteilmass, Fassadenschicht_als_Toleranzpuffer, Doppelfenster_als_Kastenfenster, Achsraster_nach_Bestand, Grundriss_nach_Bauteillaenge, Deckenhoehe_nach_Traegerhoehe, Anschlussdetail_angepasst, Erschliessungskern_verschoben
├── KNOTENTYP :Land:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht), iso_country? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
├── KNOTENTYP :Stadt:Vokabular
│   ├── Knoteneigenschaften: id (Pflicht), koordinaten? (string)
│   └── Knoten: (keine Aufzählung im Plan — aus `ort/` klassifiziert)
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
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: verbindungstechnik}]-> (:Verbindungstechnik)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: reversibilitaet}]-> (:Reversibilitaet)
│       ├── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: akteur, rolle: "<Akteurrolle.id>"}]-> (:Akteur)
│       └── (:Fallbeispiel|:Bauteilgruppe) -[HAT {art: entwurf}]-> (:Entwurfsentscheidung)
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
  (:Bauteiltyp:Vokabular {id: "Ausbau"})
  (:Bauteiltyp:Vokabular {id: "Boden"})
  (:Bauteiltyp:Vokabular {id: "Dach"})
  (:Bauteiltyp:Vokabular {id: "Daemmung"})
  (:Bauteiltyp:Vokabular {id: "Decke"})
  (:Bauteiltyp:Vokabular {id: "Fassade"})
  (:Bauteiltyp:Vokabular {id: "Fenster"})
  (:Bauteiltyp:Vokabular {id: "Fundament"})
  (:Bauteiltyp:Vokabular {id: "Gelaender"})
  (:Bauteiltyp:Vokabular {id: "Stuetze"})
  (:Bauteiltyp:Vokabular {id: "Technik"})
  (:Bauteiltyp:Vokabular {id: "Traeger"})
  (:Bauteiltyp:Vokabular {id: "Treppe"})
  (:Bauteiltyp:Vokabular {id: "Tuer"})
  (:Bauteiltyp:Vokabular {id: "Wand"})

:Material
  (:Material:Vokabular {id: "Aluminium"})
  (:Material:Vokabular {id: "Beton"})
  (:Material:Vokabular {id: "Daemmstoff"})
  (:Material:Vokabular {id: "Glas"})
  (:Material:Vokabular {id: "Gusseisen"})
  (:Material:Vokabular {id: "Holz"})
  (:Material:Vokabular {id: "Keramik"})
  (:Material:Vokabular {id: "Kunststoff"})
  (:Material:Vokabular {id: "Lehm"})
  (:Material:Vokabular {id: "Naturstein"})
  (:Material:Vokabular {id: "Recyclingbeton"})
  (:Material:Vokabular {id: "Stahl"})
  (:Material:Vokabular {id: "Stahlbeton"})
  (:Material:Vokabular {id: "Stroh"})
  (:Material:Vokabular {id: "Ziegel"})

:Bauteilebene
  (:Bauteilebene:Vokabular {id: "Bauteilgruppe"})
  (:Bauteilebene:Vokabular {id: "Einzelbauteil"})
  (:Bauteilebene:Vokabular {id: "Gebaeudeteil"})
  (:Bauteilebene:Vokabular {id: "Materialcharge"})
  (:Bauteilebene:Vokabular {id: "Oberflaechenschicht"})
  (:Bauteilebene:Vokabular {id: "System"})

:Bauteilzustand
  (:Bauteilzustand:Vokabular {id: "Beschaedigt"})
  (:Bauteilzustand:Vokabular {id: "Geprueft"})
  (:Bauteilzustand:Vokabular {id: "Intakt"})
  (:Bauteilzustand:Vokabular {id: "Kontaminiert"})
  (:Bauteilzustand:Vokabular {id: "Korrodiert"})
  (:Bauteilzustand:Vokabular {id: "Patiniert"})
  (:Bauteilzustand:Vokabular {id: "Restlebensdauer_Bekannt"})
  (:Bauteilzustand:Vokabular {id: "Restlebensdauer_Unklar"})
  (:Bauteilzustand:Vokabular {id: "Ungeprueft"})

:Funktionswechsel
  (:Funktionswechsel:Vokabular {id: "Dekorative_Funktion"})
  (:Funktionswechsel:Vokabular {id: "Gleiche_Funktion"})
  (:Funktionswechsel:Vokabular {id: "Konstruktive_Funktion"})
  (:Funktionswechsel:Vokabular {id: "Neue_Funktion"})
  (:Funktionswechsel:Vokabular {id: "Technische_Funktion"})
  (:Funktionswechsel:Vokabular {id: "Unbekannt"})

:Verbindungstechnik
  (:Verbindungstechnik:Vokabular {id: "Geschraubt"})
  (:Verbindungstechnik:Vokabular {id: "Geschweisst"})
  (:Verbindungstechnik:Vokabular {id: "Gesteckt"})
  (:Verbindungstechnik:Vokabular {id: "Geklebt"})
  (:Verbindungstechnik:Vokabular {id: "Vergossen"})
  (:Verbindungstechnik:Vokabular {id: "Klemmverbindung"})

:Bauweise
  (:Bauweise:Vokabular {id: "Fertigteilbauweise"})
  (:Bauweise:Vokabular {id: "Holzbauweise"})
  (:Bauweise:Vokabular {id: "Hybridbauweise"})
  (:Bauweise:Vokabular {id: "Massivbauweise"})
  (:Bauweise:Vokabular {id: "Ortbetonbauweise"})
  (:Bauweise:Vokabular {id: "Stahlbauweise"})

:Bausystem
  (:Bausystem:Vokabular {id: "Betonfertigteil_System"})
  (:Bausystem:Vokabular {id: "Holzrahmenbau"})
  (:Bausystem:Vokabular {id: "Holz_Skelettbau"})
  (:Bausystem:Vokabular {id: "Plattenbau"})
  (:Bausystem:Vokabular {id: "Stahl_Skelettbau"})

:Tragwerksprinzip
  (:Tragwerksprinzip:Vokabular {id: "Fachwerk"})
  (:Tragwerksprinzip:Vokabular {id: "Skeletttragwerk"})
  (:Tragwerksprinzip:Vokabular {id: "Wandtragwerk"})
  (:Tragwerksprinzip:Vokabular {id: "Wand_Kern_Tragwerk"})

:Reversibilitaet
  (:Reversibilitaet:Vokabular {id: "Reversibel"})
  (:Reversibilitaet:Vokabular {id: "Teilweise_reversibel"})
  (:Reversibilitaet:Vokabular {id: "Irreversibel"})
  (:Reversibilitaet:Vokabular {id: "Unbekannt"})

:ReuseStrategie
  (:ReuseStrategie:Vokabular {id: "Bestandserhalt_Weiterbauen"})
  (:ReuseStrategie:Vokabular {id: "In_situ_Wiederverwendung"})
  (:ReuseStrategie:Vokabular {id: "Direkte_Wiederverwendung"})
  (:ReuseStrategie:Vokabular {id: "Wiederverwendung_nach_Aufarbeitung"})
  (:ReuseStrategie:Vokabular {id: "Umnutzung_Repurposing"})
  (:ReuseStrategie:Vokabular {id: "Kaskade_Downcycling_Bauteilebene"})

:Status
  (:Status:Vokabular {id: "Gebaut"})
  (:Status:Vokabular {id: "Geplant"})
  (:Status:Vokabular {id: "Realisiert"})
  (:Status:Vokabular {id: "Nicht_Realisiert"})

:WiederverwendungsArt
  (:WiederverwendungsArt:Vokabular {id: "Bestandserhalt_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Kein_Direct_Reuse_Nachweis", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Moebel_Dekoration_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Recycling_Nicht_Direct_Reuse", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Reuse_Anteil_Unklar", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Ungebaut_Nicht_Realisierte_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung", axis: "einordnung"})
  (:WiederverwendungsArt:Vokabular {id: "wiederverwendet", axis: "grundtyp"})
  (:WiederverwendungsArt:Vokabular {id: "original", axis: "grundtyp"})
  (:WiederverwendungsArt:Vokabular {id: "hybrid", axis: "grundtyp"})

:Ressourcenquelle
  (:Ressourcenquelle:Vokabular {id: "Baustelle"})
  (:Ressourcenquelle:Vokabular {id: "Bauteilboerse"})
  (:Ressourcenquelle:Vokabular {id: "Donorgebaeude"})
  (:Ressourcenquelle:Vokabular {id: "Donor_Infrastruktur"})
  (:Ressourcenquelle:Vokabular {id: "Haendler"})
  (:Ressourcenquelle:Vokabular {id: "Lager"})
  (:Ressourcenquelle:Vokabular {id: "Materialstockpile"})
  (:Ressourcenquelle:Vokabular {id: "Produktionsueberschuss"})
  (:Ressourcenquelle:Vokabular {id: "Unbekannt"})

:Beschaffungsweg
  (:Beschaffungsweg:Vokabular {id: "Ausschreibung"})
  (:Beschaffungsweg:Vokabular {id: "Bauteilboerse"})
  (:Beschaffungsweg:Vokabular {id: "Digitale_Plattform"})
  (:Beschaffungsweg:Vokabular {id: "Direktvermittlung"})
  (:Beschaffungsweg:Vokabular {id: "Eigenbestand"})
  (:Beschaffungsweg:Vokabular {id: "Informelles_Netzwerk"})
  (:Beschaffungsweg:Vokabular {id: "Rueckbauprojekt"})
  (:Beschaffungsweg:Vokabular {id: "Spende"})

:Prozessphase
  (:Prozessphase:Vokabular {id: "Aufbereitung"})
  (:Prozessphase:Vokabular {id: "Betrieb"})
  (:Prozessphase:Vokabular {id: "Dokumentation"})
  (:Prozessphase:Vokabular {id: "Identifikation"})
  (:Prozessphase:Vokabular {id: "Lagerung"})
  (:Prozessphase:Vokabular {id: "Planung"})
  (:Prozessphase:Vokabular {id: "Pruefung"})
  (:Prozessphase:Vokabular {id: "Rueckbau"})
  (:Prozessphase:Vokabular {id: "Transport"})
  (:Prozessphase:Vokabular {id: "Wiedereinbau"})

:Rueckbauverfahren
  (:Rueckbauverfahren:Vokabular {id: "Ausbau_von_Bauteilen"})
  (:Rueckbauverfahren:Vokabular {id: "Betonfraesen"})
  (:Rueckbauverfahren:Vokabular {id: "Demontage"})
  (:Rueckbauverfahren:Vokabular {id: "Selektiver_Rueckbau"})
  (:Rueckbauverfahren:Vokabular {id: "Zerstoerungsarme_Bergung"})

:Aufbereitungsverfahren
  (:Aufbereitungsverfahren:Vokabular {id: "Drahtglasschneiden"})
  (:Aufbereitungsverfahren:Vokabular {id: "Entmoertelung_von_Fliesen"})
  (:Aufbereitungsverfahren:Vokabular {id: "Holzaufbereitung"})
  (:Aufbereitungsverfahren:Vokabular {id: "Leuchten_Refurbishment"})
  (:Aufbereitungsverfahren:Vokabular {id: "Qualitaetssicherung"})
  (:Aufbereitungsverfahren:Vokabular {id: "Reinigung"})
  (:Aufbereitungsverfahren:Vokabular {id: "Rekonditionierung"})
  (:Aufbereitungsverfahren:Vokabular {id: "Remanufacturing"})
  (:Aufbereitungsverfahren:Vokabular {id: "Reparatur"})
  (:Aufbereitungsverfahren:Vokabular {id: "Verstaerkung"})
  (:Aufbereitungsverfahren:Vokabular {id: "Zuschnitt"})

:Logistik
  (:Logistik:Vokabular {id: "Bauteiltracking"})
  (:Logistik:Vokabular {id: "Just_in_Time"})
  (:Logistik:Vokabular {id: "Lagerflaeche"})
  (:Logistik:Vokabular {id: "Lagerung"})
  (:Logistik:Vokabular {id: "Lokale_Wiederverwendung"})
  (:Logistik:Vokabular {id: "Materialmatching"})
  (:Logistik:Vokabular {id: "Materialverfuegbarkeit"})
  (:Logistik:Vokabular {id: "Transport"})
  (:Logistik:Vokabular {id: "Transportdistanz"})
  (:Logistik:Vokabular {id: "Zwischenlagerung"})

:Methode
  (:Methode:Vokabular {id: "Abrissmonitoring"})
  (:Methode:Vokabular {id: "Bauteilkatalogisierung"})
  (:Methode:Vokabular {id: "Building_Material_Scouting"})
  (:Methode:Vokabular {id: "Design_for_Disassembly"})
  (:Methode:Vokabular {id: "Form_Follows_Availability"})
  (:Methode:Vokabular {id: "Materialinventur"})
  (:Methode:Vokabular {id: "Pre_Deconstruction_Audit"})
  (:Methode:Vokabular {id: "ReUse_Assessment"})
  (:Methode:Vokabular {id: "ReUse_Ausschreibung"})
  (:Methode:Vokabular {id: "Reversibilitaet"})
  (:Methode:Vokabular {id: "Urban_Mining"})
  (:Methode:Vokabular {id: "Wiederverwendungskriterien"})
  (:Methode:Vokabular {id: "Zirkulaere_Ausschreibung"})

:Huerde
  (:Huerde:Vokabular {id: "Akzeptanzproblem"})
  (:Huerde:Vokabular {id: "Anschlussproblem"})
  (:Huerde:Vokabular {id: "Aufbereitungsaufwand"})
  (:Huerde:Vokabular {id: "Ausschreibungsproblem"})
  (:Huerde:Vokabular {id: "Bauproduktstatus"})
  (:Huerde:Vokabular {id: "Brandschutzkonflikt"})
  (:Huerde:Vokabular {id: "Bruch_Beschaedigungsrisiko"})
  (:Huerde:Vokabular {id: "Datenluecke"})
  (:Huerde:Vokabular {id: "Dauerhaftigkeit_Restlebensdauer"})
  (:Huerde:Vokabular {id: "Entwurfsbindung"})
  (:Huerde:Vokabular {id: "Fehlende_Datenstandards"})
  (:Huerde:Vokabular {id: "Fehlende_Lagerflaeche"})
  (:Huerde:Vokabular {id: "Fehlende_Standardisierung"})
  (:Huerde:Vokabular {id: "Gewaehrleistung"})
  (:Huerde:Vokabular {id: "Haftung"})
  (:Huerde:Vokabular {id: "Heterogenitaet_Chargen"})
  (:Huerde:Vokabular {id: "Hygieneanforderung"})
  (:Huerde:Vokabular {id: "Kompatibilitaetsproblem"})
  (:Huerde:Vokabular {id: "Materialqualitaet_Unklar"})
  (:Huerde:Vokabular {id: "Mengenunsicherheit"})
  (:Huerde:Vokabular {id: "Schadstoffbelastung"})
  (:Huerde:Vokabular {id: "Technische_Freigabe"})
  (:Huerde:Vokabular {id: "Terminunsicherheit"})
  (:Huerde:Vokabular {id: "Toleranzen"})
  (:Huerde:Vokabular {id: "Unkonventionelles_Material"})
  (:Huerde:Vokabular {id: "Verfuegbarkeitsproblem"})
  (:Huerde:Vokabular {id: "Witterung_Feuchte"})
  (:Huerde:Vokabular {id: "Zustand_Unklar"})

:PruefungNachweis
  (:PruefungNachweis:Vokabular {id: "Abbrandbemessung"})
  (:PruefungNachweis:Vokabular {id: "Brandschutznachweis"})
  (:PruefungNachweis:Vokabular {id: "Eignungspruefung_Baulehm"})
  (:PruefungNachweis:Vokabular {id: "Geometrische_Vermessung"})
  (:PruefungNachweis:Vokabular {id: "Materialpruefung"})
  (:PruefungNachweis:Vokabular {id: "Schadstoffscreening"})
  (:PruefungNachweis:Vokabular {id: "Schweissbarkeitspruefung"})
  (:PruefungNachweis:Vokabular {id: "Sichtpruefung"})
  (:PruefungNachweis:Vokabular {id: "Statische_Nachweisfuehrung"})
  (:PruefungNachweis:Vokabular {id: "Zugversuch"})
  (:PruefungNachweis:Vokabular {id: "Zustandsbewertung"})

:Leistungsanforderung
  (:Leistungsanforderung:Vokabular {id: "Brandschutz"})
  (:Leistungsanforderung:Vokabular {id: "Brandschutzanforderung"})
  (:Leistungsanforderung:Vokabular {id: "Dauerhaftigkeit"})
  (:Leistungsanforderung:Vokabular {id: "F90"})
  (:Leistungsanforderung:Vokabular {id: "Feuchteschutz"})
  (:Leistungsanforderung:Vokabular {id: "Feuerwiderstand"})
  (:Leistungsanforderung:Vokabular {id: "R90"})
  (:Leistungsanforderung:Vokabular {id: "REI90"})
  (:Leistungsanforderung:Vokabular {id: "Rueckbaubarkeit"})
  (:Leistungsanforderung:Vokabular {id: "Schadstofffreiheit"})
  (:Leistungsanforderung:Vokabular {id: "Schallschutz"})
  (:Leistungsanforderung:Vokabular {id: "Tragfaehigkeit"})
  (:Leistungsanforderung:Vokabular {id: "Waermeschutz"})

:Norm
  (:Norm:Vokabular {id: "DIN_18940"})
  (:Norm:Vokabular {id: "DIN_EN_15804"})
  (:Norm:Vokabular {id: "DIN_EN_15978"})
  (:Norm:Vokabular {id: "EN_1090"})
  (:Norm:Vokabular {id: "ISO_14040"})
  (:Norm:Vokabular {id: "ISO_14044"})
  (:Norm:Vokabular {id: "ISO_20887"})

:RechtlicheBedingung
  (:RechtlicheBedingung:Vokabular {id: "Bauordnungsrecht"})
  (:RechtlicheBedingung:Vokabular {id: "EU_Taxonomie"})
  (:RechtlicheBedingung:Vokabular {id: "Gewaehrleistung"})
  (:RechtlicheBedingung:Vokabular {id: "Produkthaftung"})
  (:RechtlicheBedingung:Vokabular {id: "Vergaberecht"})
  (:RechtlicheBedingung:Vokabular {id: "Zulassung_im_Einzelfall"})

:Schadstoff
  (:Schadstoff:Vokabular {id: "Asbest"})
  (:Schadstoff:Vokabular {id: "Bleifarbe"})
  (:Schadstoff:Vokabular {id: "Holzschutzmittel"})
  (:Schadstoff:Vokabular {id: "PAK"})
  (:Schadstoff:Vokabular {id: "PCB"})

:Bauobjektstatus
  (:Bauobjektstatus:Vokabular {id: "Gebaut"})
  (:Bauobjektstatus:Vokabular {id: "Geplant"})
  (:Bauobjektstatus:Vokabular {id: "In_Bau"})
  (:Bauobjektstatus:Vokabular {id: "Prototyp"})
  (:Bauobjektstatus:Vokabular {id: "Rueckgebaut"})
  (:Bauobjektstatus:Vokabular {id: "Temporaer"})
  (:Bauobjektstatus:Vokabular {id: "Unklar"})
  (:Bauobjektstatus:Vokabular {id: "Wettbewerb"})

:Nutzung
  (:Nutzung:Vokabular {id: "Buero"})
  (:Nutzung:Vokabular {id: "Gewerbe"})
  (:Nutzung:Vokabular {id: "Infrastruktur"})
  (:Nutzung:Vokabular {id: "Kultur"})
  (:Nutzung:Vokabular {id: "Lager_Depot"})
  (:Nutzung:Vokabular {id: "Mischnutzung"})
  (:Nutzung:Vokabular {id: "Schule_Bildung"})
  (:Nutzung:Vokabular {id: "Sozialbau"})
  (:Nutzung:Vokabular {id: "Wohnen"})

:BauaufgabeIntervention
  (:BauaufgabeIntervention:Vokabular {id: "Aufstockung"})
  (:BauaufgabeIntervention:Vokabular {id: "Erweiterung"})
  (:BauaufgabeIntervention:Vokabular {id: "Fit_out"})
  (:BauaufgabeIntervention:Vokabular {id: "Neubau"})
  (:BauaufgabeIntervention:Vokabular {id: "Rueckbau"})
  (:BauaufgabeIntervention:Vokabular {id: "Sanierung"})
  (:BauaufgabeIntervention:Vokabular {id: "Translozierung"})
  (:BauaufgabeIntervention:Vokabular {id: "Umbau"})
  (:BauaufgabeIntervention:Vokabular {id: "Umnutzung"})
  (:BauaufgabeIntervention:Vokabular {id: "Wiederaufbau"})

:Kontextmerkmal
  (:Kontextmerkmal:Vokabular {id: "Bestandserhalt_Policy"})
  (:Kontextmerkmal:Vokabular {id: "Pilotprojekt"})

:Land
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Pla
:Stadt
  — Knoten aus `ort/` nach Klassifikation; keine Aufzählung im Plan

:Akteurrolle
  (:Akteurrolle:Vokabular {id: "Architektur"})
  (:Akteurrolle:Vokabular {id: "Aufbereitung_Refurbishment"})
  (:Akteurrolle:Vokabular {id: "Bauausfuehrung"})
  (:Akteurrolle:Vokabular {id: "Bauherr_Auftraggeber"})
  (:Akteurrolle:Vokabular {id: "Betreiber_Nutzer"})
  (:Akteurrolle:Vokabular {id: "Brandschutz_Barrierefreiheit"})
  (:Akteurrolle:Vokabular {id: "Fassade"})
  (:Akteurrolle:Vokabular {id: "Forschung_Dokumentation"})
  (:Akteurrolle:Vokabular {id: "Kunst_Gestaltung"})
  (:Akteurrolle:Vokabular {id: "Landschaftsplanung"})
  (:Akteurrolle:Vokabular {id: "Materiallieferant"})
  (:Akteurrolle:Vokabular {id: "Nachhaltigkeitsberatung"})
  (:Akteurrolle:Vokabular {id: "Oeffentliche_Hand"})
  (:Akteurrolle:Vokabular {id: "Projektbeteiligte_Unbestimmt"})
  (:Akteurrolle:Vokabular {id: "Projektmanagement_Koordination"})
  (:Akteurrolle:Vokabular {id: "Pruefung_Qualitaetssicherung"})
  (:Akteurrolle:Vokabular {id: "Reuse_Beratung"})
  (:Akteurrolle:Vokabular {id: "Rueckbau_Demontage"})
  (:Akteurrolle:Vokabular {id: "Stahlbau_Fertigung"})
  (:Akteurrolle:Vokabular {id: "TGA_Gebaeudetechnik"})
  (:Akteurrolle:Vokabular {id: "Tragwerksplanung"})

:Datenqualitaet
  (:Datenqualitaet:Vokabular {id: "Belegt"})
  (:Datenqualitaet:Vokabular {id: "Geschaetzt"})
  (:Datenqualitaet:Vokabular {id: "Nicht_Belegt"})
  (:Datenqualitaet:Vokabular {id: "Primaerquelle"})
  (:Datenqualitaet:Vokabular {id: "Sekundaerquelle"})
  (:Datenqualitaet:Vokabular {id: "Unbekannt"})
  (:Datenqualitaet:Vokabular {id: "Widerspruechlich"})

:Datenmodell
  (:Datenmodell:Vokabular {id: "Bauteil_ID"})
  (:Datenmodell:Vokabular {id: "IFC"})
  (:Datenmodell:Vokabular {id: "Klassifikation"})
  (:Datenmodell:Vokabular {id: "Materialdatenbank"})
  (:Datenmodell:Vokabular {id: "Materialpass_Schema"})
  (:Datenmodell:Vokabular {id: "Ontologie"})
  (:Datenmodell:Vokabular {id: "Taxonomie"})

:Tooltyp
  (:Tooltyp:Vokabular {id: "Bauteilboerse"})
  (:Tooltyp:Vokabular {id: "Materialdatenbank"})
  (:Tooltyp:Vokabular {id: "Materialkataster"})

:ZertifizierungBewertungssystem
  (:ZertifizierungBewertungssystem:Vokabular {id: "BREEAM"})
  (:ZertifizierungBewertungssystem:Vokabular {id: "DGNB"})
  (:ZertifizierungBewertungssystem:Vokabular {id: "LEED"})
  (:ZertifizierungBewertungssystem:Vokabular {id: "Paris_Proof"})
  (:ZertifizierungBewertungssystem:Vokabular {id: "WELL"})

:Wirtschaft
  (:Wirtschaft:Vokabular {id: "Finanzierung"})
  (:Wirtschaft:Vokabular {id: "Geschaeftsmodell"})
  (:Wirtschaft:Vokabular {id: "Kostenvergleich"})
  (:Wirtschaft:Vokabular {id: "Lebenszykluskosten"})
  (:Wirtschaft:Vokabular {id: "Preisbildung"})
  (:Wirtschaft:Vokabular {id: "Restwert"})

:Programm
  (:Programm:Vokabular {id: "BBSM", programm_typ: "foerderung"})
  (:Programm:Vokabular {id: "FCRBE", programm_typ: "foerderung"})
  (:Programm:Vokabular {id: "PREUSE", programm_typ: "foerderung"})
  (:Programm:Vokabular {id: "Reallabor_Be_Ware", programm_typ: "foerderung"})
  (:Programm:Vokabular {id: "Zukunftbau", programm_typ: "foerderung"})
  (:Programm:Vokabular {id: "Foerderprogramm", programm_typ: "forschungskontext"})
  (:Programm:Vokabular {id: "Forschungsprojekt", programm_typ: "forschungskontext"})
  (:Programm:Vokabular {id: "Kommunales_Programm", programm_typ: "forschungskontext"})
  (:Programm:Vokabular {id: "Pilotprojekt", programm_typ: "forschungskontext"})
  (:Programm:Vokabular {id: "Reallabor", programm_typ: "forschungskontext"})
  (:Programm:Vokabular {id: "Wettbewerb", programm_typ: "forschungskontext"})
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

**Instanz-`id` vs. Ordnername:** Für **Vokabular-Labels** (§1.B) ist `id` in der Regel **gleich** dem Unterordnernamen (ggf. ASCII nach derselben Tabelle). Für **`:Bauteilgruppe`** im kanonischen Ordner **`bauteilgruppe/<CASE>_C<NN>_<ELEMENT>/`** ist Graph-`id` **gleich** dem Unterordner-Slug (verbindliches Muster — siehe Tabelle unten). Für die übrigen Instanz-Labels (`:Fallbeispiel`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette`) ist `id` der **vom Export normalisierte** Slug nach der folgenden Tabelle — der Quellordnername ist nur Eingabe, nicht zwingend 1:1 der Graph-`id`.

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
| Vokabular (§1.B) | `id` = stabiler Term-Slug; gleiche ASCII-/Trennerregeln; Ordner unter `_database/<vocab>/` möglichst schon so benannt, damit Import trivial bleibt. |

Exceptions (folders that are NOT 1:1 a node type) are listed in §1.C — they merge into another Label, get renamed, or are dropped.

**Geography exception:** `_database/ort/<id>/` is not mapped to a single `:Ort` Label. On export, each slug becomes either `(:Land:Vokabular {id})` or `(:Stadt:Vokabular {id})` according to a classification rule (country/region vs city/district/site). The plan does not enumerate those node ids.

**Reuse-Einsatz-Status exception:** Legacy folder `reuse_einsatzstatus/` has **seven** subfolders, but the graph exposes **four** vocabulary nodes under the Label **`:Status`** (not `:ReuseEinsatzstatus`). `(:Bauteilgruppe)-[:IST]->(:Status:Vokabular)` carries the lifecycle; fine-grained legacy values are merged on import:

| Legacy `reuse_einsatzstatus/<id>/` | `(:Status:Vokabular {id})` |
|---|---|
| `Vorgeschlagen`, `Prototypisch` | `Gebaut` |
| `Geplant` | `Geplant` |
| `Realisiert`, `Temporaer` | `Realisiert` |
| `Verworfen`, `Unklar` | `Nicht_Realisiert` |

**Reuse-Strategie-Konsolidierung (verbindlich — 6 Kanon-Knoten):** Legacy `reuse_strategie/` hat **elf** Unterordner; im Graphen gibt es **genau sechs** `:ReuseStrategie:Vokabular`-Knoten nach **Art der Wiederverwendung** (Gebäude-/Bauteilnutzung, nicht Marketing-Vokabular). `(:Bauteilgruppe|:Fallbeispiel)-[:IST]->(:ReuseStrategie)` zielt immer auf einen dieser Kanon-`id`-Werte. Ausführliche Beispiele bleiben in den Markdown-Quellen; im Graphen nur `id`.

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

**`:Reversibilitaet` — nur eigener Knotentyp:** Eigenes Vokabular-Label **`:Reversibilitaet:Vokabular`** mit genau vier Knoten (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`), eigene **UNIQUE-Constraint** auf `(n:Reversibilitaet).id`, ausschließlich **`HAT {art:'reversibilitaet'}`** von `:Fallbeispiel` / `:Bauteilgruppe`. Datenquelle: **explizite** Metadaten (z. B. künftiges Feld / Kuratierung) — **nicht** `fuegung_verbindung/`, **nicht** `IST`, keine Einbettung unter `:Verbindungstechnik`.

## §1.A Instance Labels (6)


| Label                     | Purpose                                                     | Replaces (legacy folders)                                          |
| ------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------ |
| `:Fallbeispiel`           | One physical case-study object                              | `fallstudie/` + `projekt/` + `bauobjekt/` (merged where ids match) |
| `:Bauteilgruppe`          | A group of components in a Fallbeispiel — the reuse-Einsatz | `bauteilgruppe/` (Zielordner; `id`-Muster `<CASE>_C<NN>_<ELEMENT>` — siehe §1); Legacy: `reuse_einsatz/` → Migration auf dieses Muster |
| `:Akteur`                 | Office / company / authority / institution / person         | `akteur/`                                                          |
| `:Quelle`                 | Source / citation target                                    | `quelle/`                                                          |
| `:SoftwareDigitaltool`    | Concrete platform                                           | `software_digitaltool/`                                            |
| `:Wiederverwendungskette` | OPTIONAL named multi-Bauteilgruppe reuse program            | `reuse_kette/` (renamed; `reuse_kettenstation/` dropped)           |


## §1.B Vocabulary Labels (39 — every controlled-knot folder mapped; `ort/` splits into two Labels; `fuegung_verbindung/` → **`:Verbindungstechnik`** only; **`:Reversibilitaet`** is a separate node type without `fuegung_verbindung/` provenance; `reuse_strategie/` → **six** `:ReuseStrategie` nodes — see exception table)

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

- `:Reversibilitaet` ← **kein** `fuegung_verbindung/`-Bezug; **vier feste** Vokabular-Knoten; nur `HAT {art:'reversibilitaet'}`; Daten nur aus **expliziten** Quellen (nicht aus der Verbindungs-Migration). **Nicht** dasselbe wie `methode/Reversibilitaet/` → weiterhin `(:Methode:Vokabular {id: "Reversibilitaet"})` per **`BENUTZT`**.

**Konstruktion:**

- `:Bauweise` ← `bauweise/`
- `:Bausystem` ← `bausystem/`
- `:Tragwerksprinzip` ← `tragwerksprinzip/`

**Reuse:**

- `:ReuseStrategie` ← `reuse_strategie/` (**eleven** legacy folders → **six** canonical `id`s — **Art der Wiederverwendung**; `IST` from `:Bauteilgruppe` / `:Fallbeispiel` — see **Reuse-Strategie-Konsolidierung** in §1)
- `:Status` ← `reuse_einsatzstatus/` (seven legacy folders → **four** nodes; Label renamed from `:ReuseEinsatzstatus`; see exception table above)
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
- `:Entwurfsentscheidung` ← **new** — no legacy folder; created fresh. Vocabulary Label capturing design adaptations forced by reuse constraints. Connected via `HAT {art:'entwurf'}` from `:Bauteilgruppe` (component-specific) or `:Fallbeispiel` (project-wide). Initial values defined from K.118 example and generalised across all case data.

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
| `reuse_kette/`                | renamed to `:Wiederverwendungskette`                                                                                           |


Total: 54 folders → 6 instance Labels + 39 vocabulary Labels + 11 dropped + 4 merged-or-renamed (`ort/` yields two Labels; `fuegung_verbindung/` → `:Verbindungstechnik` only — `:Reversibilitaet` has no folder provenance; `reuse_strategie/` → **six** `:ReuseStrategie` nodes).

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


## §2.G Vocabulary Labels (shared shape — every label in §1.B)

Most Labels in §1.B have **as many nodes as there are subfolders** under the corresponding `_database/<vocab>/` directory. For instance: `_database/material/` has subfolders for `Stahl`, `Holz`, `Beton`, `Stahlbeton`, … — each becomes a `(:Material {id: "..."})` node. **Exceptions:** `:Land` / `:Stadt` (see geography exception); `:Status` (seven legacy `reuse_einsatzstatus/` folders consolidate to **four** canonical ids — see §1 exception table); `:ReuseStrategie` (**eleven** legacy `reuse_strategie/` folders consolidate to **six** canonical ids — see §1); `:Verbindungstechnik` (six technique folders under `fuegung_verbindung/` remap to canonical ids — see §1 table; `Reversible_Fuegung/` excluded); `:Reversibilitaet` (**four** fixed nodes, **no** `fuegung_verbindung/` mapping — see §1).

Each vocab node has only:


| name | type   | req | notes                                                                       |
| ---- | ------ | --- | --------------------------------------------------------------------------- |
| `id` | string | ✓   | UNIQUE within the Label; in der Regel der Unterordnername unter `_database/<vocab>/<id>/`, normalisiert nach §1 (ASCII, ein `_` zwischen Wortteilen) |


The id is the queryable identifier. The German prose body explaining the term remains in the source Markdown `_database/<vocab>/<id>/index.md`, outside the graph.

Special additions per vocab Label:


| Label                   | extra property               | notes                                                                                                                                       |
| ----------------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `:Land`                 | `iso_country: string?`       | optional ISO country code                                                                                                                   |
| `:Stadt`                | `koordinaten: string?`       | optional coordinates string                                                                                                                 |
| `:Programm`             | `programm_typ: string` (req) | `"foerderung"` or `"forschungskontext"`                                                                                                     |
| `:WiederverwendungsArt` | `axis: string` (req)         | `"einordnung"` (legacy bewertungslogik values) or `"grundtyp"` (wiederverwendet/original/hybrid — absorbed from dropped :Bauteilgruppentyp) |
| `:Status`               | —                            | exactly **four** nodes (`Gebaut`, `Geplant`, `Realisiert`, `Nicht_Realisiert`); legacy subfolder slug maps to canonical `id` per §1 exception table |
| `:ReuseStrategie`       | —                            | exactly **six** canonical `id`s (see §1 **Reuse-Strategie-Konsolidierung**); **eleven** legacy `reuse_strategie/` folders map to those ids |
| `:Verbindungstechnik`  | —                            | six canonical technique ids (see §1); legacy `fuegung_verbindung/` technique folders remap to these `id` values |
| `:Reversibilitaet`      | —                            | exactly **four** nodes (`Reversibel`, `Teilweise_reversibel`, `Irreversibel`, `Unbekannt`); **not** sourced from `fuegung_verbindung/` (see §1) |


All vocab Labels carry the second Label `:Vokabular`.

---

# §3 Edge-type catalogue


| Edge        | Subject Labels                                                                                             | Object Labels                                                                                                    | Cardinality  | Purpose                                                       |
| ----------- | ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------- |
| `IST`       | `:Fallbeispiel`, `:Bauteilgruppe`, `:Akteur`, `:Quelle`, `:SoftwareDigitaltool`, `:Wiederverwendungskette` | vocab                                                                                                            | N:1 per axis | classification / status                                       |
| `HAT`       | `:Fallbeispiel`, `:Bauteilgruppe`                                                                          | vocab (rich) **or** `:Akteur` (with `art:'akteur', rolle:...`)                                                   | N:M          | qualitative attribute / actor participation                   |
| `BENUTZT`   | `:Bauteilgruppe`, `:Fallbeispiel`                                                                          | `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:SoftwareDigitaltool`, `:Datenmodell` | N:M          | instrumental usage; quantitative carrier                      |
| `GEHÖRT_ZU` | any                                                                                                        | `:Fallbeispiel`, `:Wiederverwendungskette`, `:Land`, `:Stadt`, `:Programm`                                       | N:1 / N:M    | membership / containment / location / chain station / origin  |
| `BELEGT_IN` | any node carrying a citable claim                                                                          | `:Quelle`                                                                                                        | N:M          | citation / evidence — the only place source attribution lives |


## Legacy relations folded in

- **IST:** `has_bauteiltyp`, `has_reuse_einsatzstatus` (→ `:Status`, values consolidated to max four), `has_reuse_strategie` (→ `:ReuseStrategie`, **eleven** legacy folders → **six** canonical `id`s — see §1), `has_bewertungslogik_abgrenzung` (→ `:WiederverwendungsArt`), `has_datenqualitaet`, `has_bauteilebene`, `has_bauteilzustand`, `has_funktionswechsel`, `has_bauweise`, `has_bausystem`, `has_tragwerksprinzip`, `has_bauobjektstatus`, `has_tooltyp`, `has_datenmodell`, `has_zertifizierung_bewertungssystem`.
- **HAT:** `has_huerde`, `has_prozessphase`, `has_pruefung_nachweis`, `references_norm`, `has_leistungsanforderung`, `has_schadstoff`, `has_kontextmerkmal`, `has_rechtliche_bedingung`, `has_nutzung`, `has_bauaufgabe_intervention`, `has_fuegung_verbindung` → **only** `HAT {art:'verbindungstechnik'}` → `:Verbindungstechnik` per §1 Verbindungstabelle (technique subfolders); **`HAT {art:'reversibilitaet'}`** → `:Reversibilitaet` is **independent** (explicit metadata — not from `fuegung_verbindung/`), `has_logistik`, `has_wirtschaft`, plus actor participation `has_akteurrolle` → `HAT {art:'akteur', rolle:...}`, plus `has_entwurfsentscheidung` → `HAT {art:'entwurf'}` from `:Bauteilgruppe` or `:Fallbeispiel` to `:Entwurfsentscheidung:Vokabular`.
- **BENUTZT:** `uses_material`, `uses_software_digitaltool`, `has_methode`, `has_rueckbauverfahren`, `has_aufbereitungsverfahren`.
- **GEHÖRT_ZU:** `installed_in_bauobjekt` → `rolle:'einbauort'`; new `sourced_from_bauobjekt` → `rolle:'herkunft'`; `part_of_reuse_kette` → `rolle:'kette'` (to `:Wiederverwendungskette`); `located_in_ort` → split: `rolle:'land'` (to `:Land`) and/or `rolle:'stadt'` (to `:Stadt`) depending on classified target; `relates_to_bauobjekt` → `rolle:'fallbeispiel'`; `involves_foerderprogramm` / `has_programm_kontext` → `rolle:'programm'` (to `:Programm`).
- **BELEGT_IN:** replaces unresolved `quelle_label` shorthand on every node and every `quelle_id` previously planned as edge property. Replaces the gap relation `documented_in_quelle`. Direction: claim → `:Quelle`.

Dropped legacy relations (no destination): `belongs_to_fallstudie`, `belongs_to_projekt`, `has_projekt`, `has_bauobjekt`, `has_bauobjektklasse`, `has_bauobjektrolle`, `has_tragwerkstyp`, `has_dokumenttyp`, `has_akteurrolle` (target dropped), `measured_on_bauobjekt`, `measures_kennwertdefinition`, `involves_akteur` (collapsed into HAT).

---

# §4 Edges — properties per edge type

**Note:** None of IST / HAT / BENUTZT / GEHÖRT_ZU carry a `quelle_id` or `quelle_label`. Source attribution lives exclusively on `:BELEGT_IN` edges from the edge's source node, optionally scoped via the `eigenschaft` property.

## §4.A `:IST`


| name         | type   | req | notes             |
| ------------ | ------ | --- | ----------------- |
| `seit`       | date?  | –   | start of validity |
| `bis`        | date?  | –   | end of validity   |
| `gewichtung` | float? | –   | 0..1 confidence   |


## §4.B `:HAT`


| name          | type    | req | notes                                                                                                                                                                                                                                    |
| ------------- | ------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `art`         | string  | ✓   | one of `"huerde"`, `"prozessphase"`, `"pruefung"`, `"norm"`, `"leistung"`, `"schadstoff"`, `"kontext"`, `"recht"`, `"nutzung"`, `"intervention"`, `"verbindungstechnik"`, `"reversibilitaet"`, `"logistik"`, `"wirtschaft"`, `"zertifizierung"`, `"akteur"`, `"entwurf"` |
| `rolle`       | string? | –   | required when `art='akteur'`; e.g. `"Architektur"`, `"Tragwerksplanung"`, `"Bauherr_Auftraggeber"`; validates against `:Akteurrolle.id`                                                                                                  |
| `anzahl`      | int?    | –   | multiplicity                                                                                                                                                                                                                             |
| `intensitaet` | string? | –   | qualitative strength                                                                                                                                                                                                                     |
| `seit`        | date?   | –   |                                                                                                                                                                                                                                          |
| `bis`         | date?   | –   |                                                                                                                                                                                                                                          |


## §4.C `:BENUTZT`


| name             | type    | req | notes                               |
| ---------------- | ------- | --- | ----------------------------------- |
| `anzahl`         | float?  | –   | quantity used                       |
| `einheit`        | string? | –   | unit (`"t"`, `"m2"`, `"Stueck"`, …) |
| `anteil_prozent` | float?  | –   | share-of-total                      |
| `funktion_alt`   | string? | –   | original role                       |
| `funktion_neu`   | string? | –   | new role                            |
| `aufbereitung`   | string? | –   | processing applied (free text)      |


## §4.D `:GEHÖRT_ZU`


| name       | type   | req | notes                                                                                                                                                  |
| ---------- | ------ | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `rolle`    | string | ✓   | one of `"fallbeispiel"`, `"einbauort"`, `"herkunft"`, `"zwischenlager"`, `"verarbeitung"`, `"transport"`, `"kette"`, `"land"`, `"stadt"`, `"programm"` |
| `position` | int?   | –   | order in sequence (e.g., chain station number)                                                                                                         |
| `seit`     | date?  | –   |                                                                                                                                                        |
| `bis`      | date?  | –   |                                                                                                                                                        |


## §4.E `:BELEGT_IN`

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
- **Role placement.** A role IS an edge property, never a node target. `:HAT {art:'akteur', rolle:'Architektur'}->(:Akteur)`. Vocab `:Akteurrolle` is a dictionary.
- **Citation placement.** Source attribution NEVER lives as a property. Always `:BELEGT_IN → :Quelle` with optional `eigenschaft` to scope.
- **Naming.** German PascalCase Labels, SCREAMING_SNAKE edges, snake_case properties.
- **:Status vs :Bauobjektstatus.** `:Status` is the reuse-**Einsatz** lifecycle only (`IST` from `:Bauteilgruppe`). Building-level construction state stays `:Bauobjektstatus` on `:Fallbeispiel` — different semantics; do not merge.
- **Homonym `Gebaut`.** The canonical `:Status` node `id:"Gebaut"` (legacy `Vorgeschlagen` + `Prototypisch`) is **not** the same concept as `:Bauobjektstatus {id:"Gebaut"}` on a `:Fallbeispiel`. Queries must always constrain the Label (`:Status` vs `:Bauobjektstatus`).
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
- canonical-axis fields (`bauteiltyp:`, `material:`, …) → IST / BENUTZT edges to vocab
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
| `reuse_einsatzstatus/`                                                                   | Label `:ReuseEinsatzstatus` → **`:Status`**; **seven** legacy folders → **four** graph nodes (mapping table in §1)                           |
| `reuse_strategie/`                                                                       | **Eleven** legacy folders → **six** `:ReuseStrategie` canonical `id`s — *Art der Wiederverwendung* (§1 + Appendix E)                         |
| `fuegung_verbindung/`                                                                     | Label `:FuegungVerbindung` dropped → **`:Verbindungstechnik`** only (six technique folders; `Reversible_Fuegung/` not mapped to graph in this pipeline — see §1) |
| `:Reversibilitaet` (detachability scale)                                                  | **Not** sourced from `fuegung_verbindung/`; own four nodes; `HAT { art: 'reversibilitaet' }` from explicit metadata only |
| Bauteiltyp drop-and-remap (SCHEMA.md §5)                                                 | already applied — noted in spec                                                                                                            |
| Material drop-and-merge (SCHEMA.md §6)                                                   | already applied — noted in spec                                                                                                            |


---

# Appendix E — `ReuseStrategie`: sechs Kanon-Knoten — *Art der Wiederverwendung* (verbindlich)

**Status:** Es gelten **genau sechs** `:ReuseStrategie`-Knoten (Kanon-`id`s in §1). Legacy `reuse_strategie/` (**elf** Ordner) mappt beim Export auf diese `id`s. Frühere 7er-Varianten sind **ersetzt**.

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

- **6** instance Labels
- **39** vocabulary Labels
- **5** edge types
- **0** body / legacy / prose properties (metadata-only)

## Out of scope (this plan)

- Writing the export script.
- Running a Neo4j instance.
- Filling the ~30 gap relations from prose.
- Translating German labels to English.

