---
name: Neo4j schema visual probe
overview: "Kleiner, separater Visualisierungs-Plan: den Neo4j-Entwurf aus `neo4j_schema_catalogue_3bc01035.plan.md` als **Knoten + Kanten** überprüfen — ohne vollständige Spec. Zwei Modi: (A) **Typgraph** (Labels + erlaubte Kantenmuster, immer überschaubar), (B) **Spielinstanzen** mit **höchstens 10 Knoten** pro stark instanziiertem Primär-Label (`:Fallbeispiel`, `:Bauwerk`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`). Taxonomie-Labels mit ≤20 Kanon-Knoten im Plan **vollständig** als Knoten darstellbar."
todos:

- id: viz-typegraph
  content: "Typgraph erzeugen: ein Knoten pro Neo4j-Label (45); Kanten = erlaubte Muster aus IST/HAT/HAT_STATUS/BENUTZT/GEHÖRT_ZU/BELEGT_IN (Quelle: Hauptplan §3, Appendix F, Appendix G). Ausgabe z. B. Mermaid oder GraphML — ein Bild/Datei pro Familie A–D optional."
  status: pending
- id: viz-sample-data
  content: "Spielgraph (Modus B): Cypher oder JSON mit capped Instanzen — pro Label aus {Fallbeispiel, Bauwerk, ReuseEinsatz, Akteur, Quelle, Software, Tool} max 10 `id`s; alle anderen Labels mindestens 1 Repräsentant wo sinnvoll (Taxonomien vollständig wenn ≤20 Knoten laut Hauptplan)."
  status: pending
- id: viz-validate
  content: "Abgleich: jede Kante des Spielgraphs gegen Appendix F (GEHÖRT_ZU), Appendix G (HAT.art), §3-Kantentabelle; fehlende oder unmögliche Kanten im Hauptplan markieren."
  status: pending

---

# Goal

Ein **separates** Visualisierungs-Artefakt erzeugen, um den Entwurf aus [neo4j_schema_catalogue_3bc01035.plan.md](e:/recherche/.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) **nur als Graphen** (Knoten + Kanten) zu prüfen — **ohne** `NEO4J_SCHEMA.md` zu schreiben und **ohne** reale Datenbankgröße.

Erfolg: Du erkennst auf einen Blick, ob **Label-Menge**, **Kantentypen** und **die wichtigsten Verknüpfungen** stimmig wirken; Abweichungen fließen als Feedback in den Hauptplan zurück.

---

# Modus A — Typgraph (empfohlen zuerst)

**Knoten:** genau **45** Knoten, je einer pro **Neo4j-Label** (§1.A + §1.B im Hauptplan).

**Kanten (keine Neo4j-„Relationship types“ im UI, sondern abstrakte Kantenarten):**

| Abstrakte Kante | Bedeutung im Typgraph |
| ---------------- | --------------------- |
| `IST_typ`        | Subjekt-Label darf per `IST` auf Ziel-Label (Klassifikation) |
| `HAT_typ`      | Subjekt-Label darf per `HAT` auf Ziel-Label (inkl. `art`-Familien grob gruppiert) |
| `HAT_STATUS_typ` | Subjekt-Label → `:Status` |
| `BENUTZT_typ`  | Subjekt-Label → Ziel-Label laut §3 |
| `GEHÖRT_ZU_typ` | Tripel-Pattern aus **Appendix F** des Hauptplans (als Kanten Label→Label mit `rolle` als Label am Kanten-Text) |
| `BELEGT_IN_typ` | Von welchen Label-Gruppen → `:Quelle` (laut §3 `BELEGT_IN`-Zeile) |

**Vorteil:** Kein Sampling nötig; **kein** „>20 Knoten“-Problem. Passt gut zu **Mermaid `flowchart`** in 2–4 **Subgraphen** (Familie A Primär, B Taxonomie in Clustern, C Kantenlegende).

**Quelle im Hauptplan:** §3-Tabelle, **Appendix F**, **Appendix G**, Hierarchiebaum `KANTENTYP`-Abschnitt.

---

# Modus B — Spielinstanzen (gecapped)

**Zweck:** Typische **Instanz**-Pfade sichtbar machen (ein `id` pro Knoten).

## Capping-Regel (verbindlich)

Für diese **Primär-Labels** höchstens **10** Knoten im Spielgraph (willkürliche aber konsistente Demo-`id`s, z. B. `DEMO_FB_01` …):

- `:Fallbeispiel`, `:Bauwerk`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`

Alle **übrigen Labels:**

- Taxonomien mit **≤20** Kanon-Knoten im Hauptplan: **alle** Kanon-`id`s als Knoten (klein genug).
- Taxonomien mit **>20** Ordner-/Knoten im realen `_database/` (z. B. `:Huerde` mit vielen `huerde/`-Einträgen): im Spielgraph nur **Stichprobe (5–8 Knoten)** plus eine Kante „…“-Kommentar in der Legende — Ziel ist **Schema-Fit**, nicht Daten-Vollständigkeit.

## Kanten im Spielgraph

- Nur **die sechs** Neo4j-Kantentypen: `IST`, `HAT`, `HAT_STATUS`, `BENUTZT`, `GEHÖRT_ZU`, `BELEGT_IN`.
- **`GEHÖRT_ZU`:** ausschließlich Tripel aus **Appendix F**.
- **`HAT`:** `art` nur Literale aus **Appendix G**; für `wiederverwendungsart` mindestens **eine** Kette `(:ReuseEinsatz)-[:HAT]->(:WiederverwendungsArt {axis:\"reuse_strategie\"})`.
- **`IST`:** mindestens je **ein** Beispiel für `axis: \"einordnung\"` und `axis: \"grundtyp\"` an einem Subjekt, **kein** `IST` mit `axis: \"reuse_strategie\"` (verboten im Hauptplan).
- **`BELEGT_IN`:** nur wo eine Demo-`:Quelle` existiert; **keine** unaufgelösten Shorthands.

---

# Deliverables (Vorschlag, Repo-relativ)

| Artefakt | Inhalt |
| -------- | ------ |
| `_database/_system/viz/schema_typegraph.mmd` | Mermaid: Modus A (optional 4 Dateien nach Familie) |
| `_database/_system/viz/schema_sample.cypher` | `MERGE`-Skript für Modus B (capped) |
| `_database/_system/viz/README_viz.md` | 1 Seite: Legende, Capping, Link zum Hauptplan |

Kein Zwang zu Neo4j-Installation: Mermaid reicht für Modus A; Modus B optional in Neo4j Browser laden.

---

# Abgleich mit Hauptplan (Checkliste)

- [ ] Alle **45** Labels im Typgraph vorhanden
- [ ] Alle **6** Kantentypen durch mindestens eine **Instanz**-Kante in Modus B abgedeckt
- [ ] **Appendix F** vollständig als erlaubte `GEHÖRT_ZU`-Kanten modellierbar (kein „Phantom-Tripel“)
- [ ] **`reuse_strategie`** nur über `HAT`+`wiederverwendungsart`, nie über `IST`
- [ ] `BELEGT_IN` nur zu existierender `:Quelle`

---

# Out of scope

- Echte Daten aus `_database/` importieren
- Performance, Indizes, Constraints testen
- Volltext oder `body_md`

---

## Mini-Legende (Modus A, verbal)

**Primär-Cluster:** `Fallbeispiel` —`GEHÖRT_ZU`→ `Bauwerk`; `ReuseEinsatz` —`GEHÖRT_ZU`→ `Fallbeispiel` / `Bauteilgruppe` / `Bauwerk` (rollen aus F); `Tool` —`GEHÖRT_ZU`→ `Software`; `Software|Tool` —`GEHÖRT_ZU`→ `Programm`; Akten/Ort analog F.

**Klassifikations-Cluster:** viele kleine Labels hängen an `Fallbeispiel|Bauwerk|ReuseEinsatz|…` per `IST`/`HAT`/`HAT_STATUS`/`BENUTZT` gemäß Hauptplan §3.

Damit hast du **eine** visuelle Gesamtsicht ohne die instanzreichen Typen zu überladen.
