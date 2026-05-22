# Semantic Reuse Network Catalog

> Live graph snapshot: **2263 nodes / 14571 relationships** in `mit-bestand` — generated 2026-06-16.

Each section has a **graph query** (`RETURN` nodes/relationships/paths for Neo4j Browser Graph view), executed stats, and a short reading. Paste the Cypher block, run it, switch to **Graph** (not Table). Extends [`PRESENTATION_REUSE_NETWORKS.md`](../2026-06-06_cross_bubble_extension/PRESENTATION_REUSE_NETWORKS.md).

## 1. Actor reuse constellation (all countries)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.review_run IS NOT NULL
RETURN a, r, b;
```
**What it shows:** Evidence-tagged reuse coordination links between actors.

**Headline:** 159 directed tagged connections across 11 research runs.

**Stats — actors in network by country:**

| Country | Actors in network |
| --- | --- |
| Schweiz | 51 |
| Deutschland | 36 |
| (no country edge) | 27 |
| Belgien | 16 |
| Frankreich | 15 |
| Niederlande | 7 |
| Vereinigtes Königreich | 6 |
| Österreich | 6 |
| Dänemark | 4 |
| USA | 2 |
| Finnland | 1 |
**Reading:** Dense national clumps joined by long cross-border edges. Switzerland and Germany dominate; 27 actors lack `LIEGT_IN_LAND`.

## 2. Swiss reuse bubble (star network around Cirkla)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN a, r, b;
```
**What it shows:** Swiss coordination as a centralised star — Cirkla as national directory.

**Headline:** 14 connections in `swiss_reuse_bubble_2026_06_05`.

**Stats — all bubbles:**

| review_run | Connections |
| --- | --- |
| post_ier_w3_2026_06_07 | 93 |
| swiss_reuse_bubble_2026_06_05 | 14 |
| germany_reuse_bubble_2026_06_05 | 13 |
| cross_bubble_extension_2026_06_06 | 9 |
| agent_06b_non_bubble_actor_networks_2026_06_06 | 9 |
| post_quality_p06_02_2026_06_06 | 9 |
| france_reuse_bubble_2026_06_05 | 6 |
| rotor_dc_reuse_bubble_2026_06_05 | 3 |
| netherlands_reuse_bubble_2026_06_05 | 1 |
| quality_pass_q05_2026_06_06 | 1 |
| remediation_wave2_r04_2026_06_06 | 1 |
**Reading:** Star topology — Cirkla lists depots, consultancies, software. Zirkular, baubüro in situ, Matériuum orbit the hub.

## 3. Actors by country (full registry)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[r:LIEGT_IN_LAND]->(l:Land)
RETURN a, r, l;
```
**What it shows:** Every geolocated actor linked to its country (`LIEGT_IN_LAND`).

**Stats — actor counts:**

| Country | Actors |
| --- | --- |
| (no country edge) | 355 |
| Schweiz | 111 |
| Deutschland | 69 |
| Belgien | 33 |
| Niederlande | 32 |
| Frankreich | 31 |
| Vereinigtes Königreich | 22 |
| Österreich | 13 |
| Dänemark | 10 |
| Liechtenstein | 2 |
| USA | 2 |
| Finnland | 1 |
| Norwegen | 1 |
**Reading:** 355 actors have no country edge (project-only dossier actors). CH (111), DE (69), BE (33), NL (32), FR (31) lead among geolocated actors.

## 4. Projects × country × actors

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[r1:BETEILIGT_AN]->(p:Projekt)-[r2:LIEGT_IN_LAND]->(l:Land)
RETURN a, r1, p, r2, l;
```
**What it shows:** Full tripartite network — who participates in which project in which country.

**Tip:** Large hairball; filter e.g. `WHERE l.name = 'Deutschland'` in Browser.

**Stats — projects by country:**

| Country | Projects |
| --- | --- |
| Deutschland | 15 |
| Belgien | 12 |
| Niederlande | 12 |
| Vereinigtes Königreich | 11 |
| Schweiz | 10 |
| Dänemark | 5 |
| Frankreich | 5 |
| USA | 4 |
| Finnland | 3 |
| Japan | 1 |
| Luxemburg | 1 |
| Norwegen | 1 |
| Österreich | 1 |
**Cross-border actors:**

| Actor | Countries | Projects |
| --- | --- | --- |
| Arup | Vereinigtes Königreich, Niederlande | 3 |
**Reading:** DE/BE/NL lead project counts. Only **Arup** spans UK + Netherlands.

## 5. Top actors per country (example: Switzerland)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (l:Land {name: 'Schweiz'})<-[r2:LIEGT_IN_LAND]-(p:Projekt)<-[r1:BETEILIGT_AN]-(a:Akteur)
RETURN a, r1, p, r2, l;
```
**What it shows:** Actor–project–country subgraph for one country (Schweiz). Change `Land {name: …}` for other countries.

**Stats — top 3 actors per country (sample):**

| Country | Actor | Projects |
| --- | --- | --- |
| Belgien | Rotor | 4 |
| Belgien | RotorDC | 3 |
| Belgien | BLAF Architecten | 2 |
| Deutschland | Claus Asam | 2 |
| Deutschland | IEMB / TU Berlin | 2 |
| Deutschland | LXSY Architektur | 2 |
| Dänemark | Lendager | 3 |
| Dänemark | Artelia | 2 |
| Dänemark | a:gain | 2 |
| Finnland | Consolis Parma | 3 |
| Finnland | Ramboll Finland | 3 |
| Finnland | Umacon | 3 |
| Frankreich | Albert & Co | 1 |
| Frankreich | Archipel zéro | 1 |
| Frankreich | Association Réavie | 1 |
**Reading:** National champions — Zirkular (4 projects) in CH, Rotor/RotorDC in BE, Cleveland Steel & Tubes in UK.

## 6. Actor–role map

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)
WHERE COUNT { (a)-[:HAT_AKTEURROLLE]->() } >= 3
MATCH (a)-[r:HAT_AKTEURROLLE]->(ar:Akteurrolle)
RETURN a, r, ar;
```
**What it shows:** Actors with ≥3 roles and their `HAT_AKTEURROLLE` edges.

**Stats — top roles:**

| Role | Assignments |
| --- | --- |
| Reuse_Zirkularitaetsberatung | 217 |
| Entwurf_Planung | 184 |
| Materiallieferung_Markt | 147 |
| Forschung_Dokumentation | 133 |
| Fachplanung_Nachweis | 117 |
| Bauherr_Auftraggeber | 84 |
| Projektmanagement_Koordination | 79 |
| Rueckbau_Bauteilernte_Logistik | 78 |
| Bauausfuehrung_Fertigung | 69 |
| Software_Digitalisierung | 67 |
**Stats — most multi-role actors:**

| Actor | Role count |
| --- | --- |
| BauKarussell | 8 |
| Cleveland Steel & Tubes | 8 |
| Cycle Up | 8 |
| Mobius Réemploi | 8 |
| re:store / HarvestMAP Vienna | 8 |
| REFAIR Bordeaux | 8 |
| RotorDC | 8 |
| Rotor | 7 |
**Reading:** Material hubs (Concular, Matériuum, Bauteilkatalog Basel) carry 6–7 roles — full-stack reuse operators.

## 7. Actor type × role matrix (Materialhub slice)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[rt:HAT_AKTEURTYP]->(at:Akteurtyp),
      (a)-[rr:HAT_AKTEURROLLE]->(ar:Akteurrolle)
WHERE at.id = 'at_materialhub_bauteilboerse'
RETURN a, rt, at, rr, ar;
```
**What it shows:** How `Materialhub_Bauteilboerse` actors combine type and role edges.

**Stats — top type×role pairs (all types):**

| Actor type | Role | Actors |
| --- | --- | --- |
| Unternehmen | Entwurf_Planung | 97 |
| Person | Reuse_Zirkularitaetsberatung | 96 |
| Person | Entwurf_Planung | 87 |
| Unternehmen | Fachplanung_Nachweis | 79 |
| Unternehmen | Reuse_Zirkularitaetsberatung | 66 |
| Person | Forschung_Dokumentation | 65 |
| Unternehmen | Bauausfuehrung_Fertigung | 53 |
| Unternehmen | Materiallieferung_Markt | 53 |
| Materialhub_Bauteilboerse | Materialbroker / Reuse-Marketplace-Betreiber | 49 |
| Materialhub_Bauteilboerse | Materiallieferung_Markt | 49 |
| Materialhub_Bauteilboerse | Software_Digitalisierung | 49 |
| Unternehmen | Projektmanagement_Koordination | 38 |
**Reading:** Material hubs almost always combine marketplace operator, market supply, and software/digitalisation.

## 8. Norms by country (typed law nodes)

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (rw)-[r:GILT_IN_LAND]->(l:Land)
WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
RETURN rw, r, l;
```
**What it shows:** All 91 typed law nodes and their `GILT_IN_LAND` jurisdiction edges.

**Stats — laws per country:**

| Country | Law nodes |
| --- | --- |
| Deutschland | 67 |
| Niederlande | 37 |
| Frankreich | 35 |
| Belgien | 33 |
| Österreich | 33 |
| Dänemark | 32 |
| Norwegen | 32 |
| Schweiz | 6 |
| Vereinigtes Königreich | 6 |
**Multi-country standards (top 5):**

| Standard | Countries |
| --- | --- |
| CEN/TS 1090-201:2024 | 7 |
| CEN/TS 17440 (Bewertung bestehender Tragwerke) | 7 |
| DIN 4074 / EN 14081 (Holzsortierung) | 7 |
| DIN EN 13501 | 7 |
| EN/DIN EN 1090 | 7 |
**Reading:** Germany/EU scopes dominate. 48/91 standards are multi-label across legal domains.

## 9. Component → norm regulation chain

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH path = (bg:Bauteilgruppe {id: 'bg_stahl_mehrere_holbein_structural'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)
      -[:GESTUETZT_AUF_REGELWERK]->(rw)
      -[:GILT_IN_LAND]->(:Land)
WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
RETURN path;
```
**What it shows:** Holbein structural steel — path from Bauteilgruppe through Regulierungsfrage → Nachweisforderung → Tragwerksrecht → Land.

**Coverage:** 284 Bauteilgruppen trigger questions; 284 reach law nodes.

**Full chain (all domains, more paths):**

```cypher
MATCH path = (bg:Bauteilgruppe {id: 'bg_stahl_mehrere_holbein_structural'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(:Nachweisforderung)
      -[:GESTUETZT_AUF_REGELWERK]->(rw)
      -[:GILT_IN_LAND]->(:Land)
WHERE any(lbl IN labels(rw) WHERE lbl ENDS WITH 'recht')
RETURN path;
```
**Stats — question/proof summary:**

| Question | Proof | Standards |
| --- | --- | --- |
| BauproduktstatusFrage | Bauteilidentifikation | 7 |
| BauproduktstatusFrage | Befestigungsnachweis | 4 |
| BauproduktstatusFrage | Brandschutznachweis | 6 |
| BauproduktstatusFrage | DauerhaftigkeitRestlebensdauer | 4 |
| BauproduktstatusFrage | GenehmigungsOderZustimmungsbedarf | 6 |
| BauproduktstatusFrage | HerkunftsUndRueckbaudokumentation | 17 |
| BauproduktstatusFrage | MaterialpassRessourcenpass | 4 |
| BauproduktstatusFrage | Materialpruefung | 17 |
**Reading:** One steel component triggers Tragwerk, Schadstoff, Bauprodukt, Genehmigung simultaneously — deepest semantic chain for reuse legitimacy.

## 10. Bauteilgruppen from which projects

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (p:Projekt {id: 'p_k118_kopfbau_halle_118_winterthur'})-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN p, r, bg, t, bt;
```
**What it shows:** K.118 project and its Bauteilgruppen + Bauteiltypen.

**Alternate — top project by component count:**

```cypher
MATCH (p:Projekt {id: 'p_meduni_campus_mariannengasse'})-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
OPTIONAL MATCH (bg)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN p, r, bg, t, bt;
```
**Stats — top projects:**

| Project | Bauteilgruppen |
| --- | --- |
| MedUni Campus Wien | 20 |
| K.118 Winterthur | 16 |
| Chiro d’Itterbeek | 12 |
| Maison des Canaux, Paris | 10 |
| Grubenstrasse 29 | 9 |
| Multi Brussels | 9 |
| Recyclinghaus Hannover | 9 |
| Ferme du Rail Paris | 8 |
**Reading:** Facades and walls dominate; MedUni Wien (20) and K.118 (16) are best entry points.

## 11. Donor → receiver material flows

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (bg:Bauteilgruppe)-[rs:AUS_SPENDER]->(donor:Bauwerk),
      (bg)-[re:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)
OPTIONAL MATCH (p:Projekt)-[hp:HAT_BAUTEILGRUPPE]->(bg)
RETURN bg, rs, donor, re, recv, p, hp;
```
**What it shows:** Bauteilgruppe donor/receiver buildings (`AUS_SPENDER` / `IN_EMPFANGSOBJEKT`).

**Cross-country subgraph:**

```cypher
MATCH (bg:Bauteilgruppe)-[rs:AUS_SPENDER]->(donor:Bauwerk)-[:LIEGT_IN_LAND]->(dl:Land),
      (bg)-[re:IN_EMPFANGSOBJEKT]->(recv:Bauwerk)-[:LIEGT_IN_LAND]->(rl:Land)
WHERE dl <> rl
OPTIONAL MATCH (p:Projekt)-[hp:HAT_BAUTEILGRUPPE]->(bg)
RETURN bg, rs, donor, dl, re, recv, rl, p, hp;
```
**Stats — sample flows:**

| Component | Project |
| --- | --- |
| Steel profiles for… | 55 Great Suffolk Street |
| Cable trays as shelves… | AWM Münster – zirkulärer… |
| Fixed wall cladding… | AWM Münster – zirkulärer… |
| Glass partitions and… | AWM Münster – zirkulärer… |
| WC partitions | AWM Münster – zirkulärer… |
| Wood for fixed built-ins | AWM Münster – zirkulärer… |
**Reading:** Mostly intra-country. Standout: UMAR door handles BE → CH.

## 12. Material & Bauteiltyp reuse patterns

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[t:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
WHERE bt.name IN ['Fassade', 'Wand', 'Traeger', 'Fenster', 'Stuetze']
RETURN p, r, bg, t, bt;
```
**What it shows:** Projects linked to envelope/structure Bauteilgruppen and Bauteiltypen.

**Materials subgraph:**

```cypher
MATCH (p:Projekt)-[r:NUTZT_MATERIAL]->(m:Material)
RETURN p, r, m;
```
**Stats:**

| Bauteiltyp | Projects |
| --- | --- |
| Wand | 47 |
| Fassade | 44 |
| Traeger | 34 |
| Boden | 31 |
| Decke | 30 |
| Ausbau | 25 |
| Technik | 24 |
| Fenster | 23 |
**Reading:** Wand/Fassade in 44+ projects; material tagging sparser than Bauteiltyp.

## 13. Reuse barriers (Hürden) network

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (p:Projekt)-[r:HAT_HUERDE]->(h:Huerde)
RETURN p, r, h;
```
**What it shows:** Projects and their documented reuse obstacles.

**Stats — top barriers:**

| Barrier | Projects |
| --- | --- |
| Verfuegbarkeitsproblem | 16 |
| Entwurfsbindung | 12 |
| Terminunsicherheit | 11 |
| Witterung_Feuchte | 11 |
| Aufbereitungsaufwand | 9 |
| Fehlende_Lagerflaeche | 8 |
| Heterogenitaet_Chargen | 8 |
| Mengenunsicherheit | 6 |
| Unkonventionelles_Material | 5 |
| Ausschreibungsproblem | 4 |
| Akzeptanzproblem | 3 |
**Reading:** **Verfügbarkeitsproblem** #1 (16 projects) — reuse is a coordination problem.

## 14. Hubs, bridges & synthesis

**Graph query (Neo4j Browser → Graph view):**

```cypher
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]-(b:Akteur)
WHERE r.review_run IS NOT NULL
  AND (
    a.id IN ['cirkla', 'opalis', 'zirkular', 'concular', 'rotordc', 'useagain_bauteilclick']
    OR b.id IN ['cirkla', 'opalis', 'zirkular', 'concular', 'rotordc', 'useagain_bauteilclick']
  )
RETURN a, r, b;
```
**What it shows:** Core hub actors and their tagged reuse connections.

**Full tagged constellation:**

```cypher
MATCH (a:Akteur)-[r:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
WHERE r.review_run IS NOT NULL
RETURN a, r, b;
```
**Bridge nodes (span ≥2 bubbles):**

| Actor | Bubbles spanned |
| --- | --- |
| Cirkla | 4 |
| Opalis | 4 |
| RotorDC | 3 |
| Concular | 3 |
| Bellastock | 3 |
| Zirkular | 2 |
**Path useagain → CSTB:** `(no path within 12 hops)`

**Reading:** Cirkla & Opalis span 4 bubbles each. Continental bridging remains fragile.

## 14b. Software network

**Graph query:**

```cypher
MATCH (p:Projekt)-[r:NUTZT_SOFTWARE]->(sw)
RETURN p, r, sw;
```
**Stats:**

| Software | Projects |
| --- | --- |
| BIM / digitaler Bauteilkatalog | 2 |
| Concular | 1 |
| EcoTool | 1 |
| HTS Reused Steel Stockmatcher | 1 |
| INIES | 1 |
| LLMNT | 1 |


## 14c. Business-model network (actors)

**Graph query:**

```cypher
MATCH (a:Akteur)-[r:HAT_GESCHAEFTSMODELL]->(gm:Geschaeftsmodell)
RETURN a, r, gm;
```
**Stats:**

| Model | Actors |
| --- | --- |
| Urban-Mining-Dienstleister mit Verkaufskanal | 28 |
| Shop mit Eigenstock | 27 |
| Multi-Vendor-Marktplatz | 26 |
| Netzwerk / Aggregator / Redistribution | 6 |
| SaaS-Inventarplattform | 3 |


## Appendix — Quick reference

| § | Graph pattern | Key rels |
|---|---|---|
| 1–2 | Actor hubs | `VERBUNDEN_MIT_AKTEUR` |
| 3 | Actor → Land | `LIEGT_IN_LAND` |
| 4–5 | Actor → Projekt → Land | `BETEILIGT_AN` |
| 6–7 | Actor → Rolle/Typ | `HAT_AKTEURROLLE`, `HAT_AKTEURTYP` |
| 8 | Law → Land | `GILT_IN_LAND` |
| 9 | BG → RF → NF → law → Land | regulation chain |
| 10 | Projekt → Bauteilgruppe → Bauteiltyp | `HAT_BAUTEILGRUPPE` |
| 11 | BG → donor/recv Bauwerk | `AUS_SPENDER`, `IN_EMPFANGSOBJEKT` |
| 12–13 | Projekt → Material/Hürde | `NUTZT_MATERIAL`, `HAT_HUERDE` |
| 14 | Hub subgraph | `VERBUNDEN_MIT_AKTEUR` |

Regenerate stats: `python _run_catalog_queries.py` then `python _build_catalog_md.py`.
Export graph JSON (one file per network): `python _export_graph_networks.py` → [`graph_networks/`](graph_networks/) (see [`manifest.json`](graph_networks/manifest.json)).
