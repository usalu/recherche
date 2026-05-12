---
name: Neo4j schema visual probe
overview: "Visualisierungs-Plan mit **vollständiger Inventur**: alle **45** Labels und alle **6** Kantentypen inkl. `GEHÖRT_ZU`-Tripel (Appendix F), `HAT.art`→Ziel, `IST`-Ziele, `BENUTZT`, `HAT_STATUS`, `BELEGT_IN` (Abschnitt „Vollständige Inventur“). Modus A = Typgraph; Modus B = Spielinstanzen mit max. 10 Knoten pro Primär-Label unter {Fallbeispiel, Bauwerk, ReuseEinsatz, Akteur, Quelle, Software, Tool}."
todos:

- id: viz-typegraph
  content: "Typgraph erzeugen: **45** UI-Knoten (Liste Abschnitt A); Kanten **exakt** nach Abschnitt B.1–B.7 — keine weiteren Kantentypen. Ausgabe z. B. Mermaid/GraphML; optional 4 Dateien nach Cluster."
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

# Vollständige Inventur — alle Knoten (Labels) und Kanten

> Spiegelung von [neo4j_schema_catalogue_3bc01035.plan.md](e:/recherche/.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) §1.A/B, §3, Appendix F/G. **Typgraph:** je **ein** UI-Knoten pro Eintrag unten. **Spielgraph:** pro Label-**Typ** Instanzen nach Capping-Regeln (Modus B).

## A) Alle Neo4j-Labels — **45** Label-Typen (Referenz)

### §1.A Primär-Labels (**9**)

1. `:Fallbeispiel`  
2. `:Bauwerk`  
3. `:Bauteilgruppe`  
4. `:ReuseEinsatz`  
5. `:Akteur`  
6. `:Quelle`  
7. `:Software`  
8. `:Tool`  
9. `:Wiederverwendungskette`  

### §1.B Weitere Labels (**36**)

10. `:Bauteiltyp`  
11. `:Material`  
12. `:Bauteilebene`  
13. `:Bauteilzustand`  
14. `:Funktionswechsel`  
15. `:Verbindungstechnik`  
16. `:Reversibilitaet`  
17. `:Bauweise`  
18. `:Bausystem`  
19. `:Tragwerksprinzip`  
20. `:Status`  
21. `:WiederverwendungsArt`  
22. `:Ressourcenquelle`  
23. `:Beschaffungsweg`  
24. `:Prozessphase`  
25. `:Rueckbauverfahren`  
26. `:Aufbereitungsverfahren`  
27. `:Logistik`  
28. `:Methode`  
29. `:Huerde`  
30. `:PruefungNachweis`  
31. `:Leistungsanforderung`  
32. `:Norm`  
33. `:RechtlicheBedingung`  
34. `:Nutzung`  
35. `:BauaufgabeIntervention`  
36. `:Entwurfsentscheidung`  
37. `:Messpunkt`  
38. `:Land`  
39. `:Stadt`  
40. `:Akteurrolle`  
41. `:Datenqualitaet`  
42. `:Tooltyp`  
43. `:ZertifizierungBewertungssystem`  
44. `:Wirtschaft`  
45. `:Programm`  

---

## B) Alle Neo4j-Kantentypen — **6** + Kanten-Properties (für Visualisierung)

| Kantentyp | Pflicht-Properties (laut Hauptplan §4) | Kurznotiz Visualisierung |
| --------- | ---------------------------------------- | ------------------------ |
| `IST` | optional `seit`, `bis`, `gewichtung` | nur Klassifikation |
| `HAT` | `art` (Pflicht), optional `rolle`, `anzahl`, `intensitaet`, `seit`, `bis` | `rolle` nur wenn `art = akteur` |
| `HAT_STATUS` | wie `IST` (optional Zeit/Gewichtung) | Ziel immer `:Status` |
| `BENUTZT` | optional `anzahl`, `einheit`, `anteil_prozent`, `funktion_alt`, `funktion_neu`, `aufbereitung` | quantitative Träger |
| `GEHÖRT_ZU` | `rolle` (Pflicht), optional `position`, `seit`, `bis` | nur Tripel aus Tabelle **B.5** |
| `BELEGT_IN` | optional `eigenschaft`, `seite`, `excerpt`, `raw_label` | immer → `:Quelle` |

---

## B.1) `IST` — erlaubte Subjekte und Ziele (Typgraph)

**Subjekt-Labels (alle dürfen ausgehend `IST` haben):**  
`:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`

**Ziel-Labels („Klassifikation“; im Typgraph je eine gerichtete Kante Subjekt → Ziel, sofern fachlich möglich):**  
alle **§1.B**-Labels **außer** `:Status` und **außer** `:Akteurrolle` (**kein** `IST` aufs Wörterbuch `Akteurrolle`, Hauptplan §1.B).

Also **32** Ziel-Labels für `IST` (alle §1.B **außer** `:Status`, `:Akteurrolle`, `:Entwurfsentscheidung`, `:Messpunkt` — `Entwurfsentscheidung` nur per `HAT { art: "entwurf" }`, `Messpunkt` nur per `GEHÖRT_ZU { rolle: "messung" }`):

`:Bauteiltyp`, `:Material`, `:Bauteilebene`, `:Bauteilzustand`, `:Funktionswechsel`, `:Verbindungstechnik`, `:Reversibilitaet`, `:Bauweise`, `:Bausystem`, `:Tragwerksprinzip`, `:WiederverwendungsArt`, `:Ressourcenquelle`, `:Beschaffungsweg`, `:Prozessphase`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Logistik`, `:Methode`, `:Huerde`, `:PruefungNachweis`, `:Leistungsanforderung`, `:Norm`, `:RechtlicheBedingung`, `:Nutzung`, `:BauaufgabeIntervention`, `:Land`, `:Stadt`, `:Datenqualitaet`, `:Tooltyp`, `:ZertifizierungBewertungssystem`, `:Wirtschaft`, `:Programm`

**Hinweis:** `:Entwurfsentscheidung` **nur** über `HAT` mit `art: "entwurf"` (Hauptplan Legacy-Folding), **nicht** über `IST`. **`:Messpunkt`** **nur** über **`GEHÖRT_ZU { rolle: "messung" }`**, **nicht** über `IST`.

**Verboten (explizit Hauptplan §3):**  
Von **`:Fallbeispiel`**, **`:Bauwerk`** oder **`:ReuseEinsatz`** **kein** `IST` zu **`(:WiederverwendungsArt { axis: "reuse_strategie" })`** — diese Achse nur **`HAT { art: "wiederverwendungsart" }`**.

---

## B.2) `HAT` — Subjekte, `HAT.art` → Ziel-Label, Sonderfall Akteur

**Subjekt-Labels:** `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:ReuseEinsatz`

**Ziel bei `art = akteur`:** `:Akteur` (Kante **muss** `rolle` ∈ der **8** Kanon-`Akteurrolle.id` aus Hauptplan §1.D tragen — im Typgraph reicht Kanten-Text „`art=akteur, rolle=*`“).

**Ziel bei `art = wiederverwendungsart`:** `:WiederverwendungsArt` mit **`axis: "reuse_strategie"`** (nur so).

**`HAT.art` → Ziel-Label** (jede Zeile = Typgraph-Kante(n) vom Subjekt-Quartett zum Ziel-Label; Literal vollständig in **B.6**):

| `HAT.art` | Ziel-Label |
| --------- | ---------- |
| `huerde` | `:Huerde` |
| `prozessphase` | `:Prozessphase` |
| `pruefung` | `:PruefungNachweis` |
| `norm` | `:Norm` |
| `leistung` | `:Leistungsanforderung` |
| `recht` | `:RechtlicheBedingung` |
| `nutzung` | `:Nutzung` |
| `intervention` | `:BauaufgabeIntervention` |
| `verbindungstechnik` | `:Verbindungstechnik` |
| `reversibilitaet` | `:Reversibilitaet` |
| `logistik` | `:Logistik` |
| `wirtschaft` | `:Wirtschaft` |
| `zertifizierung` | `:ZertifizierungBewertungssystem` |
| `akteur` | `:Akteur` |
| `entwurf` | `:Entwurfsentscheidung` |
| `wiederverwendungsart` | `:WiederverwendungsArt` (nur `axis: "reuse_strategie"`) |

---

## B.3) `HAT_STATUS`

**Subjekt-Labels:** `:Bauwerk`, `:ReuseEinsatz`, optional `:Fallbeispiel`, optional `:Bauteilgruppe`  
**Ziel-Label:** immer `:Status`

---

## B.4) `BENUTZT`

**Subjekt-Labels:** `:Bauteilgruppe`, `:ReuseEinsatz`, `:Bauwerk`, `:Fallbeispiel`  
**Ziel-Labels:** `:Material`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Software`, `:Tool`

---

## B.5) `GEHÖRT_ZU` — **vollständige** erlaubte Tripel `(sourceLabel, rolle, targetLabel)`

| sourceLabel | rolle | targetLabel |
| ----------- | ----- | ------------- |
| `:Bauwerk` | `fallbeispiel` | `:Fallbeispiel` |
| `:ReuseEinsatz` | `fallbeispiel` | `:Fallbeispiel` |
| `:ReuseEinsatz` | `bauteilgruppe` | `:Bauteilgruppe` |
| `:ReuseEinsatz` | `einbauort` | `:Bauwerk` |
| `:ReuseEinsatz` | `herkunft` | `:Bauwerk` |
| `:ReuseEinsatz` | `zwischenlager` | `:Bauwerk` |
| `:ReuseEinsatz` | `verarbeitung` | `:Bauwerk` |
| `:ReuseEinsatz` | `transport` | `:Bauwerk` |
| `:Bauteilgruppe` | `einbauort` | `:Bauwerk` |
| `:Bauteilgruppe` | `herkunft` | `:Bauwerk` |
| `:Bauteilgruppe` | `zwischenlager` | `:Bauwerk` |
| `:Bauteilgruppe` | `verarbeitung` | `:Bauwerk` |
| `:Bauteilgruppe` | `transport` | `:Bauwerk` |
| `:ReuseEinsatz` | `kette` | `:Wiederverwendungskette` |
| `:Bauteilgruppe` | `kette` | `:Wiederverwendungskette` |
| `:Fallbeispiel` | `land` | `:Land` |
| `:Fallbeispiel` | `stadt` | `:Stadt` |
| `:Bauwerk` | `land` | `:Land` |
| `:Bauwerk` | `stadt` | `:Stadt` |
| `:Fallbeispiel` | `programm` | `:Programm` |
| `:Software` | `programm` | `:Programm` |
| `:Tool` | `programm` | `:Programm` |
| `:Tool` | `software` | `:Software` |
| `:Messpunkt` | `messung` | `:Bauwerk` |
| `:Messpunkt` | `messung` | `:Fallbeispiel` |
| `:Messpunkt` | `messung` | `:Bauteilgruppe` |
| `:Messpunkt` | `messung` | `:ReuseEinsatz` |

---

## B.6) `HAT.art` — vollständige Literal-Liste (Appendix G)

`akteur`, `entwurf`, `huerde`, `intervention`, `logistik`, `norm`, `nutzung`, `pruefung`, `prozessphase`, `recht`, `reversibilitaet`, `verbindungstechnik`, `wirtschaft`, `wiederverwendungsart`, `zertifizierung`

**Zusatzregel:** Schadstoff-Import → Ziel `:Huerde` mit `kategorie: "Schadstoff"`, Kante immer `art: "huerde"` (kein Literal `schadstoff`).

---

## B.7) `BELEGT_IN` — erlaubte Subjekt-Labels → Ziel `:Quelle`

**Richtung:** Subjekt → `:Quelle` (Kantentyp `BELEGT_IN`).

**Subjekt-Labels (laut Hauptplan §3, zuzüglich Kuratierung):**

- Immer: `:Fallbeispiel`, `:Bauwerk`, `:Bauteilgruppe`, `:ReuseEinsatz`, `:Akteur`, `:Quelle`, `:Software`, `:Tool`, `:Wiederverwendungskette`, `:Entwurfsentscheidung`, `:Messpunkt`
- Zusätzlich **§1.B**-Klassifikationsknoten **nur**, wenn die Quelle den **Taxonomieeintrag** belegt (nicht nur Fließtext) — im Typgraph optional als gestrichelte Kante „nur wenn Export-Flag“ kennzeichnen.

**Ziel:** ausschließlich `:Quelle`. **Keine** Kante ohne auflösbares `(:Quelle)` (Hauptplan §4.F).

---

# Modus A — Typgraph (empfohlen zuerst)

**Implementierung:** 1:1 aus Abschnitt **„Vollständige Inventur“** oben — keine weiteren Labels oder Kantenmuster hinzufügen.

**Knoten:** genau **45** Knoten, je einer pro **Neo4j-Label** (Abschnitt **A**).

**Kanten:** die **sechs** Neo4j-Relationship-Typen mit den **exakten** Endpunkt-Regeln aus **B.1–B.7** (keine abstrakten `*_typ`-Namen nötig — im Diagramm z. B. Farbe pro Kantentyp).

**Quelle bei Abweichung:** [Hauptplan](e:/recherche/.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md) §3, Appendix F/G, Hierarchiebaum `KANTENTYP` — bei Konflikt Hauptplan führend, dann diesen Visualisierungs-Plan anpassen.

**Vorteil:** Kein Sampling nötig; **kein** „>20 Knoten“-Problem. Passt gut zu **Mermaid `flowchart`** in 2–4 **Subgraphen** (Primär vs. Taxonomie vs. `GEHÖRT_ZU`-Stern um `Fallbeispiel`/`Bauwerk`/`ReuseEinsatz`).

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
- **`GEHÖRT_ZU`:** ausschließlich Tripel aus **B.5** (= Hauptplan Appendix F).
- **`HAT`:** `art` nur Literale aus **B.6**; für `wiederverwendungsart` mindestens eine Kette zu `(:WiederverwendungsArt { axis: "reuse_strategie" })`.
- **`IST`:** Regeln **B.1** (kein `IST` zu `WiederverwendungsArt` mit `reuse_strategie` von Fall/Bauwerk/Einsatz).
- **`IST`:** nach **B.1**; im Demo mindestens je ein Beispiel `axis: "einordnung"` und `axis: "grundtyp"` auf `(:WiederverwendungsArt)`.
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
