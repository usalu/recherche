# Explorer queries — `mit-bestand` (post Phase B + property cleanup + sidecar 4b/5b)

Tested against the live graph (2026-06-05). Run in **Neo4j Browser** or **Bloom**.

**Tips**

- Prefer `RETURN path` for graph view; pin **`name`** on nodes (not schema labels).
- Tune `LIMIT` per `UNION` block to zoom in/out.
- Law nodes are **multi-label** (`:Tragwerksrecht` + `:Bauproduktrecht`, …) — Bloom counts every label as a color.
- Maps **without** the law layer stay cleaner (6–8 types); maps **with** `GESTUETZT_AUF_REGELWERK` may show extra law-label colors.
- Offloaded QA metadata and internal doc titles: read **`metadata_sidecar_key`** → [`sidecar/entity_metadata.jsonl`](../../review/2026-06-05_post_migration_property_cleanup/sidecar/entity_metadata.jsonl).
- Prefer **`l.country_iso2`** or **`l.id`** over `l.name` when filtering Länder (avoids encoding quirks in copy-paste).

**Good anchors:** `bg_stahl_mehrere_holbein_structural`, `p_holbein_gardens_london`, `p_verbiest_karreveld_brussels`, `p_chiro_d_itterbeek_dilbeek`, `p_k118_kopfbau_halle_118_winterthur`, `bw_chiro_itterbeek_reuse_supply_network`, `bw_cleveland_steel_reclaimed_stock`.

---

## A. Regulation spine & sanity (Variant B)

### A1 — Holbein steel: Bauteil → Frage → Nachweis → Standard (graph)

```cypher
// Regulation spine — Holbein structural steel
MATCH path = (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
  -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung {id:'nf_standsicherheitsnachweis'})
  -[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN path
LIMIT 25
```

Expect paths ending at `SCI P427`, `CEN/TS 1090-201:2024`, etc.

### A2 — Same spine (table / diagram names)

```cypher
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf)
      -[:ERFORDERT_NACHWEIS]->(nf)
      -[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN bg.name AS bauteil, rf.name AS frage, nf.name AS nachweis,
       rw.name AS standard, rw.rechtsbereiche AS domain
ORDER BY nachweis, standard
```

### A3 — Multi-domain law nodes

```cypher
MATCH (rw)
WHERE size([l IN labels(rw) WHERE l ENDS WITH 'recht']) > 1
RETURN rw.name AS standard, rw.rechtsbereiche AS domains
ORDER BY size(rw.rechtsbereiche) DESC, standard
LIMIT 15
```

Examples: `SCI P427` (Tragwerk + Bauprodukt), `EU C&D Waste Protocol` (Schadstoff + Reuse + Rückbau).

### A4 — Jurisdiction: one standard → Länder

```cypher
MATCH path = (rw:Tragwerksrecht {id:'rw_sci_p427'})-[:GILT_IN_LAND]->(l:Land)
RETURN path
```

### A5 — Jurisdiction overview (Tragwerksrecht)

```cypher
MATCH (rw:Tragwerksrecht)-[:GILT_IN_LAND]->(l:Land)
RETURN rw.name AS standard, collect(l.name) AS laender
ORDER BY size(laender) DESC
LIMIT 10
```

### A6 — Project regulation footprint (counts)

```cypher
MATCH (p:Projekt {id:'p_holbein_gardens_london'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
OPTIONAL MATCH (rf)-[:ERFORDERT_NACHWEIS]->(nf)-[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN p.name AS projekt,
       count(DISTINCT rf) AS fragen,
       count(DISTINCT nf) AS nachweise,
       count(DISTINCT rw) AS standards
```

### A7 — Project regulation slice (graph)

```cypher
MATCH path = (p:Projekt {id:'p_holbein_gardens_london'})
  -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf)
  -[:ERFORDERT_NACHWEIS]->(nf)
WHERE nf.id IN [
  'nf_standsicherheitsnachweis',
  'nf_schadstoffpruefung',
  'nf_produktstatus_und_leistungserklaerung'
]
RETURN path
```

---

## B. Reuse chains & procurement

### B1 — Verbiest component: donor / receiver

```cypher
MATCH path = (bg:Bauteilgruppe {id:'bg_stahl_gelaender_verbiest_charleroi'})
  -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(target)
RETURN path
```

### B2 — All reuse edges (sample)

```cypher
MATCH path = (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(target)
WHERE target:Bauwerk OR target:Materialdepot
RETURN path
LIMIT 30
```

Evidence on edges: `source_url`, `source_quote`, `confidence`.

### B3 — Holbein star: regulation + reuse + Huerde + Beschaffung

```cypher
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
OPTIONAL MATCH p1 = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
OPTIONAL MATCH p2 = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
OPTIONAL MATCH p3 = (bg)-[:HAT_HUERDE]->(:Huerde)
OPTIONAL MATCH p4 = (bg)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg)
WITH collect(p1) + collect(p2) + collect(p3) + collect(p4) AS paths
UNWIND paths AS path
RETURN path
LIMIT 50
```

---

## C. Schadstoff routing

### C1 — Pollutant → proof → Schadstoffrecht

```cypher
MATCH path = (s:Schadstoff {id:'s_kmf'})
  -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
  -[:GESTUETZT_AUF_REGELWERK]->(rw:Schadstoffrecht)
RETURN path
```

### C2 — Case-documented Schadstoffprüfung (sourced edges)

```cypher
MATCH path = (bg:Bauteilgruppe)-[r:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung {id:'nf_schadstoffpruefung'})
WHERE r.source_url IS NOT NULL
RETURN path, r.source_url, r.source_quote
LIMIT 10
```

### C3 — Era → Schadstoff → Material (cross-case, see Pattern A in §E)

---

## D. Huerde & barriers

### D1 — Sourced project hurdles

```cypher
MATCH path = (p:Projekt)-[r:HAT_HUERDE]->(h:Huerde)
WHERE r.source_url IS NOT NULL
RETURN path, r.basis, r.confidence
LIMIT 20
```

### D2 — Bauteilgruppe hurdles with basis

```cypher
MATCH path = (bg:Bauteilgruppe)-[r:HAT_HUERDE]->(h:Huerde)
WHERE r.source_url IS NOT NULL
RETURN path, r.basis, r.source_url
LIMIT 15
```

---

## E. Cross-project patterns

Each pattern spans **many projects** and keeps roughly **6–8 node types**.

### Pattern A — Era → pollutant → material → screening (~20 projects, 8 types)

```cypher
MATCH (s:Schadstoff)-[:TYPISCH_BEI_ERA]->(era:BauwerkEra)
MATCH path = (s)-[:TYPISCH_BEI_ERA]->(era)
RETURN path LIMIT 15

UNION
MATCH (s:Schadstoff)-[:TYPISCH_BEI_MATERIAL]->(m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)
MATCH path = (s)-[:TYPISCH_BEI_MATERIAL]->(m)<-[:NUTZT_MATERIAL]-(bg)
RETURN path LIMIT 25

UNION
MATCH (s:Schadstoff)-[:TYPISCH_BEI_MATERIAL]->(m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 25

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
WHERE (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 20
```

### Pattern B — Reuse object + Herkunftsdokumentation (~12 projects, 7 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
MATCH (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
MATCH (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_herkunfts_und_rueckbaudokumentation'})
RETURN path LIMIT 25

UNION
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
MATCH (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 30
```

### Pattern C — Holz vs Stahl, same Tragwerk spine (~18 projects, 6 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
WHERE m.id IN ['mat_holz', 'mat_stahl']
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m)
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
WHERE m.id IN ['mat_holz', 'mat_stahl']
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
WHERE m.id IN ['mat_holz', 'mat_stahl']
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
RETURN path LIMIT 25
```

### Pattern D — Steel “proof bundle” (~14 projects, 5 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
WHERE nf.id IN [
  'nf_materialpruefung',
  'nf_dauerhaftigkeit_restlebensdauer',
  'nf_standsicherheitsnachweis'
]
RETURN path LIMIT 45

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 25
```

### Pattern E — Materialpruefung universal hub, sampled (~15 projects, 6 types)

```cypher
MATCH (nf:Nachweisforderung {id:'nf_materialpruefung'})
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(nf)
WITH p, collect(bg)[0..1] AS bgs
ORDER BY p.name
LIMIT 15
UNWIND bgs AS bg
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(nf)
RETURN path

UNION
MATCH (nf:Nachweisforderung {id:'nf_materialpruefung'})
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(nf)
WITH p, collect(bg)[0..1] AS bgs
ORDER BY p.name
LIMIT 15
UNWIND bgs AS bg
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 15

UNION
MATCH (nf:Nachweisforderung {id:'nf_materialpruefung'})
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
      -[:ERFORDERT_NACHWEIS]->(nf)
WITH p, collect(bg)[0..1] AS bgs
ORDER BY p.name
LIMIT 15
UNWIND bgs AS bg
MATCH path = (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 15
```

Swap `nf_materialpruefung` → `nf_produktstatus_und_leistungserklaerung` for the Bauproduktstatus hub.

### Pattern F — Standsicherheit across jurisdictions (~10 projects, 5 types)

```cypher
MATCH (l:Land)<-[:LIEGT_IN_LAND]-(p:Projekt)
WHERE l.name IN ['Deutschland','Belgien','Niederlande','Vereinigtes Koenigreich','Schweiz','Finnland']
WITH l, p ORDER BY p.name
WITH l, collect(p)[0..2] AS ps
UNWIND ps AS p
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (p)-[:LIEGT_IN_LAND]->(l)
RETURN path

UNION
MATCH (l:Land)<-[:LIEGT_IN_LAND]-(p:Projekt)
WHERE l.name IN ['Deutschland','Belgien','Niederlande','Vereinigtes Koenigreich','Schweiz','Finnland']
WITH l, p ORDER BY p.name
WITH l, collect(p)[0..2] AS ps
UNWIND ps AS p
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
RETURN path
```

### Pattern G — Brandschutz material fan-out (~19 projects, 6 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_brandschutz_frage'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_brandschutz_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_brandschutznachweis'})
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_brandschutz_frage'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_brandschutz_frage'})
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
WHERE m.id IN ['mat_holz','mat_glas','mat_daemmstoff']
RETURN path LIMIT 25
```

### Pattern H1 — Cleveland steel shared stock (2 London projects)

```cypher
MATCH (bw:Bauwerk {id:'bw_cleveland_steel_reclaimed_stock'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path

UNION
MATCH (bw:Bauwerk {id:'bw_cleveland_steel_reclaimed_stock'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path

UNION
MATCH (bw:Bauwerk {id:'bw_cleveland_steel_reclaimed_stock'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
RETURN path

UNION
MATCH (bw:Bauwerk {id:'bw_cleveland_steel_reclaimed_stock'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
RETURN path
```

### Pattern H2 — Tampere office donor (2 Finnish projects)

```cypher
MATCH (bw:Bauwerk {id:'bw_tampere_1980s_office_donor'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path

UNION
MATCH (bw:Bauwerk {id:'bw_tampere_1980s_office_donor'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path

UNION
MATCH (bw:Bauwerk {id:'bw_tampere_1980s_office_donor'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_herkunfts_und_rueckbaudokumentation'})
RETURN path
```

---

## F. Single-project “big maps” (6–8 node types, many edges)

Use themed slices — a full single-project query easily hits 15+ label types.

### Map 1 — Chiro d'Itterbeek (~104 paths, 8 types) — densest

```cypher
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 20

UNION
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN path LIMIT 15

UNION
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 50

UNION
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
RETURN path LIMIT 20

UNION
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:LIEGT_IN_LAND|LIEGT_IN_STADT]->(geo)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN path LIMIT 12
```

### Map 2 — K.118 Winterthur (~74 paths, 7 types)

```cypher
MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})
MATCH path = (p)-[:HAT_METHODE]->(meth:Methode)
RETURN path LIMIT 6

UNION
MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 20

UNION
MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN path LIMIT 16

UNION
MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 40

UNION
MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[:LIEGT_IN_LAND]->(l:Land)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN path LIMIT 16
```

### Map 3 — MedUni Wien (~48 paths, 6 types)

```cypher
MATCH (p:Projekt {id:'p_meduni_campus_mariannengasse'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 25

UNION
MATCH (p:Projekt {id:'p_meduni_campus_mariannengasse'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
RETURN path LIMIT 20

UNION
MATCH (p:Projekt {id:'p_meduni_campus_mariannengasse'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 60

UNION
MATCH (p:Projekt {id:'p_meduni_campus_mariannengasse'})-[:LIEGT_IN_LAND|LIEGT_IN_STADT]->(geo)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN path LIMIT 20
```

### Map 4 — Verbiest Brussels (~56 paths, 6 types)

```cypher
MATCH (p:Projekt {id:'p_verbiest_karreveld_brussels'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
RETURN path LIMIT 25

UNION
MATCH (p:Projekt {id:'p_verbiest_karreveld_brussels'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 35

UNION
MATCH (p:Projekt {id:'p_verbiest_karreveld_brussels'})-[:LIEGT_IN_LAND|LIEGT_IN_STADT]->(geo)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN path LIMIT 15
```

### Map 5 — Schadstoff cross-case (~69 paths, 7 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage {id:'rf_schadstoff_frage'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
MATCH path = (s)-[:TYPISCH_BEI_MATERIAL]->(m)<-[:NUTZT_MATERIAL]-(bg)
RETURN path LIMIT 25

UNION
MATCH (bg:Bauteilgruppe)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 20
```

### Map 6 — Steel cross-case (~45 paths, 7 types)

```cypher
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
  -[:GESTUETZT_AUF_REGELWERK]->(rw:Tragwerksrecht)
RETURN path LIMIT 25

UNION
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path LIMIT 20
```

### Map 7 — Multi Brussels (~54 paths, 6 types)

```cypher
MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
RETURN path LIMIT 30

UNION
MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 20

UNION
MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path LIMIT 40

UNION
MATCH (p:Projekt {id:'p_multi_brussels_reuse_in_multi'})-[:LIEGT_IN_LAND|LIEGT_IN_STADT]->(geo)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN path LIMIT 10
```

### Map 8 — Recyclinghaus + typed laws (~56 paths, 8 types)

```cypher
MATCH (p:Projekt {id:'p_recyclinghaus_hannover'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
  -[:GESTUETZT_AUF_REGELWERK]->(rw:Tragwerksrecht)
RETURN path LIMIT 15

UNION
MATCH (p:Projekt {id:'p_recyclinghaus_hannover'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_standsicherheitsnachweis'})
  -[:GESTUETZT_AUF_REGELWERK]->(rw:Tragwerksrecht)-[:GILT_IN_LAND]->(l:Land)
RETURN path LIMIT 30

UNION
MATCH (p:Projekt {id:'p_recyclinghaus_hannover'})-[:LIEGT_IN_LAND]->(l:Land)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path LIMIT 20
```

---

## G. Integrity & graph health (table view)

### G1 — Regulation overlay counts

```cypher
RETURN
  size([(n) WHERE any(l IN labels(n) WHERE l ENDS WITH 'recht') | n]) AS typed_law_nodes,
  size([()-[r:GESTUETZT_AUF_REGELWERK]->() | r]) AS gestuetzt,
  size([()-[r:GILT_IN_LAND]->() | r]) AS gilt_in_land,
  size([()-[r:TRIGGERS_REGULIERUNGSFRAGE]->() | r]) AS triggers,
  size([()-[r:ERFORDERT_NACHWEIS]->() | r]) AS erfordert
```

Expected: `91 / 167 / 281 / 1130 / 1578` (TRIGGERS/ERFORDERT drift +30/+95 vs Phase B baseline — see [`regulation_drift_report.json`](../../review/2026-06-05_post_migration_property_cleanup/regulation_drift_report.json)).

### G2 — No duplicate GESTUETZT edges

```cypher
MATCH (nf:Nachweisforderung)-[r:GESTUETZT_AUF_REGELWERK]->(rw)
WITH nf, rw, count(r) AS c WHERE c > 1
RETURN nf.id, rw.id, c
```

### G3 — No parallel duplicate edges (any type)

```cypher
MATCH (a)-[r]->(b)
WITH a, b, type(r) AS t, count(*) AS c
WHERE c > 1
RETURN t, count(*) AS duplicate_pairs
ORDER BY duplicate_pairs DESC
```

Should return empty.

### G4 — Regelwerk label still absent

```cypher
MATCH (n:Regelwerk) RETURN count(n) AS regelwerk_nodes
```

Expected: `0`.

### G5 — Every Nachweisforderung with GESTUETZT has matching law node

```cypher
MATCH (nf:Nachweisforderung)-[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN count(DISTINCT nf) AS nf_with_laws, count(DISTINCT rw) AS distinct_laws
```

### G6 — Graph size snapshot

```cypher
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels
```

Expected: `2287 / 15393` (structure stable; property sidecar applied 2026-06-05).

### G7 — Sidecar pointer sanity

```cypher
RETURN
  size([()-[r]->() WHERE r.metadata_sidecar_key IS NOT NULL | r]) AS rel_sidecar_keys,
  size([(n) WHERE n.metadata_sidecar_key IS NOT NULL | n]) AS node_sidecar_keys,
  size([()-[r]->() WHERE r.review_status IS NOT NULL | r]) AS review_status_left,
  size([(n) WHERE n.source_titles IS NOT NULL AND any(t IN n.source_titles WHERE t CONTAINS '.md') | n]) AS md_titles_left
```

Expected: `615 / 607 / 0 / 0`.

---

## I. Reuse narratives (story queries)

These are **single-story** maps — good for presentations and “why does this case matter?”

### I1 — Chiro: one supply network, twelve components

The densest reuse project: every reused Bauteilgruppe points at the same **Materialdepot** hub.

```cypher
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(md:Materialdepot {id:'bw_chiro_itterbeek_reuse_supply_network'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(md)
RETURN path
LIMIT 40
```

Table view — what came through the network:

```cypher
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(md:Materialdepot {id:'bw_chiro_itterbeek_reuse_supply_network'})
OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
OPTIONAL MATCH (bg)-[:HAT_BESCHAFFUNGSWEG]->(b:Beschaffungsweg)
RETURN bg.name AS component, m.name AS material, b.name AS beschaffung
ORDER BY component
```

Expect **12 rows**, mostly `Digitale_Plattform` procurement.

### I2 — Chiro: sanitary block donor (multi-material demolition source)

Twelve components also link to the **sanitary block** Bauwerk donor — a second narrative layer.

```cypher
MATCH (bw:Bauwerk {id:'bw_chiro_itterbeek_sanitary_block'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path
LIMIT 25

UNION
MATCH (bw:Bauwerk {id:'bw_chiro_itterbeek_sanitary_block'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)
RETURN path
LIMIT 20
```

### I3 — Funktionswechsel: “Neue Funktion” in the reuse chain

**238** reused components carry `funktionswechsel: Neue_Funktion` — adaptive reuse, not like-for-like.

```cypher
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
  AND 'Neue_Funktion' IN coalesce(bg.funktionswechsel, [])
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
RETURN path
LIMIT 35

UNION
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
  AND 'Neue_Funktion' IN coalesce(bg.funktionswechsel, [])
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
RETURN path
LIMIT 25
```

Compare with **Gleiche_Funktion** (74 components) by swapping the `WHERE` clause.

### I4 — Holbein steel: dual donor story (depot + Cleveland stock)

Holbein structural steel links to **both** a Materialdepot aggregator and the shared **Cleveland Steel** Bauwerk.

```cypher
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
RETURN path

UNION
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
WHERE nf.id IN ['nf_standsicherheitsnachweis','nf_materialpruefung','nf_dauerhaftigkeit_restlebensdauer']
RETURN path

UNION
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
MATCH path = (bg)<-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(l:Land {country_iso2:'GB'})
RETURN path
```

### I5 — Verbiest: Charleroi steel + Brussels depot

Belgian reuse corridor: steel from Charleroi donor, storage via Verbiest Lagerhaus depot.

```cypher
MATCH (p:Projekt {id:'p_verbiest_karreveld_brussels'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t.id IN ['bw_palais_des_expositions_charleroi','bw_verbiest_lagerhaus_zu_haus_und_atelier']
   OR bg.id = 'bg_stahl_gelaender_verbiest_charleroi'
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
RETURN path
LIMIT 20

UNION
MATCH (p:Projekt {id:'p_verbiest_karreveld_brussels'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
      -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_herkunfts_und_rueckbaudokumentation'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf)
RETURN path
LIMIT 15
```

### I6 — Recyclinghaus Hannover: donor = receiver building

Nine components reuse material **from the same building** being transformed.

```cypher
MATCH (p:Projekt {id:'p_recyclinghaus_hannover'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw:Bauwerk {id:'bw_recyclinghaus_hannover'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path
LIMIT 30

UNION
MATCH (p:Projekt {id:'p_recyclinghaus_hannover'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw:Bauwerk {id:'bw_recyclinghaus_hannover'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path
LIMIT 40
```

### I7 — ReuseRule jurisdiction templates (screening knowledge, not case evidence)

Twenty **ReuseRule** nodes encode country×material screening templates (Schadstoff + Aufbereitung edges).

```cypher
MATCH (rr:ReuseRule {id:'rr_be_stahl'})
MATCH path = (rr)-[:HAT_SCHADSTOFFRISIKO|HAT_AUFBEREITUNG]->(target)
RETURN path
LIMIT 25

UNION
MATCH (rr:ReuseRule)
WHERE rr.name CONTAINS 'Stahl'
MATCH path = (rr)-[:HAT_SCHADSTOFFRISIKO]->(s:Schadstoff)
RETURN path
LIMIT 20
```

Swap `rr_be_stahl` → `rr_de_holz`, `rr_fi_beton_hollow_core` (check `MATCH (rr:ReuseRule) RETURN rr.id, rr.name` for ids).

---

## J. Cross-project comparative findings

Table-first queries for “what repeats across cases?” — then pick a row and plug IDs into graph maps.

### J1 — Reuse intensity leaderboard (projects)

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WITH p, count(DISTINCT bg) AS reuse_bgs
ORDER BY reuse_bgs DESC
LIMIT 15
MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN p.name AS projekt, l.country_iso2 AS land, reuse_bgs
ORDER BY reuse_bgs DESC
```

Top hits: Chiro (12), Recyclinghaus (9), Grubenstrasse/Werkhof (8), Verbiest/Lycée/Résilience/Impact Hub/Kindergarten Möösli (7 each).

### J2 — Shared donor buildings (multi-project stories)

```cypher
MATCH (bw:Bauwerk)<-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
WITH bw, count(DISTINCT bg) AS components, count(DISTINCT p) AS projects,
     collect(DISTINCT p.name)[0..4] AS sample_projects
WHERE components >= 6
RETURN bw.name AS donor, components, projects, sample_projects
ORDER BY components DESC
LIMIT 12
```

**Pattern H1/H2** in §E drill into Cleveland steel and Tampere office; this query finds **all** shared-donor hubs.

### J3 — Steel reuse by jurisdiction

```cypher
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(l:Land)
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
WHERE (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
RETURN l.country_iso2 AS land, count(DISTINCT p) AS projects, count(DISTINCT bg) AS steel_reuse_bgs
ORDER BY steel_reuse_bgs DESC
```

All **42** steel projects have reuse edges — steel in this corpus is inherently a reuse narrative.

### J4 — Procurement channel mix (cross-case)

```cypher
MATCH (bg:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(b:Beschaffungsweg)
WHERE (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
RETURN b.name AS kanal, count(bg) AS reused_components
ORDER BY reused_components DESC
```

Dominant channels: **Spende** (108), **Eigenbestand** (79), **Digitale_Plattform** + **Rueckbauprojekt** (64 each).

### J5 — Urban Mining method × reuse overlap

```cypher
MATCH (p:Projekt)-[:HAT_METHODE]->(:Methode {id:'meth_urban_mining_und_scouting'})
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WITH p, count(DISTINCT bg) AS reuse_bgs
ORDER BY reuse_bgs DESC
LIMIT 12
MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN p.name AS projekt, l.country_iso2 AS land, reuse_bgs
```

17 projects declare Urban Mining; **59** reuse components sit in those projects.

### J6 — Double burden: reuse + Schadstoff regulation

```cypher
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WHERE (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path
LIMIT 25

UNION
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WHERE (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_schadstoff_frage'})
MATCH path = (bg)-[:NUTZT_MATERIAL]->(m:Material)<-[:TYPISCH_BEI_MATERIAL]-(s:Schadstoff)
RETURN path
LIMIT 20
```

~14 components carry **both** a reuse chain and an explicit Schadstoff regulation trigger.

### J7 — Same hurdle, many projects (barrier convergence)

```cypher
MATCH (p:Projekt)-[r:HAT_HUERDE]->(h:Huerde {id:'h_verfuegbarkeitsproblem'})
OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN p.name AS projekt, l.country_iso2 AS land, r.basis, r.confidence
ORDER BY p.name
LIMIT 20
```

Swap hurdle id: `h_entwurfsbindung` (12 projects), `h_terminunsicherheit` (11), `h_witterung_feuchte` (11).

Graph fan-out for the top barrier:

```cypher
MATCH (p:Projekt)-[:HAT_HUERDE]->(h:Huerde {id:'h_verfuegbarkeitsproblem'})
MATCH path = (p)-[:HAT_HUERDE]->(h)
RETURN path
LIMIT 25

UNION
MATCH (p:Projekt)-[:HAT_HUERDE]->(h:Huerde {id:'h_verfuegbarkeitsproblem'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WHERE (p)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN path
LIMIT 20
```

### J8 — Reuse documentation law stack (cross-jurisdiction)

```cypher
MATCH (nf:Nachweisforderung {id:'nf_herkunfts_und_rueckbaudokumentation'})
      -[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN rw.name AS standard, rw.rechtsbereiche AS domains
ORDER BY size(rw.rechtsbereiche) DESC, standard
```

18 standards anchor Herkunftsdokumentation — EU Waste Framework, DIN SPEC 91484, FCRBE Toolkit, Tracimat, ISO 20887, …

---

## K. Procurement, logistics & preparation chains

### K1 — Spende → Aufbereitung → reuse (preparation pipeline)

```cypher
MATCH (bg:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Spende'})
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
MATCH path = (bg)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Spende'})
RETURN path
LIMIT 20

UNION
MATCH (bg:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Spende'})
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
MATCH path = (bg)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)
RETURN path
LIMIT 30

UNION
MATCH (bg:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Spende'})
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
MATCH path = (bg)-[:HAT_LOGISTIK]->(log)
WHERE log.name IN ['Lagerung','Transport','Materialmatching']
RETURN path
LIMIT 25
```

### K2 — Digital platform corridor (top platform projects)

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Digitale_Plattform'})
WITH p, count(bg) AS platform_bgs
WHERE platform_bgs >= 4
ORDER BY platform_bgs DESC
LIMIT 6
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Digitale_Plattform'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg)
RETURN path
LIMIT 40
```

Chiro, Impact Hub, Verbiest, Lycée Michel Lucius lead this cluster.

### K3 — Aufbereitung hub ranking

```cypher
MATCH (bg:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(av:Aufbereitungsverfahren)
RETURN av.name AS verfahren, count(bg) AS components
ORDER BY components DESC
```

**Pruefung_Sortierung_QS** (88) dominates; **Remanufacturing_und_Upcycling** (37) marks upscale reuse.

### K4 — Materialdepot hubs (aggregated donors)

```cypher
MATCH (md:Materialdepot)<-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
WITH md, count(DISTINCT bg) AS components, count(DISTINCT p) AS projects
WHERE components >= 4
RETURN md.name AS depot, components, projects
ORDER BY components DESC
```

Graph the Chiro network (12 components):

```cypher
MATCH (md:Materialdepot {id:'bw_chiro_itterbeek_reuse_supply_network'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(md)
RETURN path
LIMIT 35
```

---

## L. Methods, actors & process patterns

### L1 — Method stack per high-reuse project

```cypher
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})
MATCH path = (p)-[:HAT_METHODE]->(m:Methode)
RETURN path

UNION
MATCH (p:Projekt {id:'p_chiro_d_itterbeek_dilbeek'})
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
RETURN path
LIMIT 25
```

Compare with `p_impact_hub_berlin_crclr_fitout`, `p_grande_halle_de_colombelles`.

### L2 — Actor roles on reuse-heavy projects

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WITH p, count(DISTINCT bg) AS reuse_bgs
WHERE reuse_bgs >= 6
MATCH (p)-[:BETEILIGT_AN|VERBUNDEN_MIT_AKTEUR]->(a:Akteur)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
RETURN p.name AS projekt, ar.name AS rolle, count(a) AS akteure
ORDER BY projekt, akteure DESC
```

Expect **Reuse_Zirkularitaetsberatung**, **Entwurf_Planung**, **Rueckbau_Bauteilernte_Logistik** prominently.

### L3 — Design methods cross-case (table)

```cypher
MATCH (p:Projekt)-[:HAT_METHODE]->(m:Methode)
WITH m.name AS methode, count(DISTINCT p) AS projects
ORDER BY projects DESC
RETURN methode, projects
LIMIT 10
```

---

## M. Evidence & proof narratives

### M1 — Case-documented Schadstoffprüfung (sourced edges)

```cypher
MATCH (bg:Bauteilgruppe)-[r:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung {id:'nf_schadstoffpruefung'})
WHERE r.source_url IS NOT NULL
MATCH path = (bg)-[r]->(nf)
RETURN path, r.source_url, r.confidence
ORDER BY r.confidence DESC
LIMIT 12
```

### M2 — Proof fulfillment via PruefungNachweis nodes

`ERFUELLT_NACHWEIS` links **PruefungNachweis** → **Nachweisforderung** (case-level “we did this test”).

```cypher
MATCH (pn:PruefungNachweis)-[:ERFUELLT_NACHWEIS]->(nf:Nachweisforderung)
WITH nf, count(pn) AS documented_tests
ORDER BY documented_tests DESC
LIMIT 8
MATCH path = (pn:PruefungNachweis)-[:ERFUELLT_NACHWEIS]->(nf)
RETURN path
LIMIT 30
```

Materialprüfung leads (54 documented tests in corpus).

### M3 — Sourced reuse-chain evidence (donor edges with URLs)

```cypher
MATCH (bg:Bauteilgruppe)-[r:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE r.source_url IS NOT NULL
  AND (t:Bauwerk OR t:Materialdepot)
MATCH path = (bg)-[r]->(t)
RETURN path, r.source_url, r.confidence
LIMIT 15
```

### M4 — Sidecar metadata lookup (post 4b/5b)

```cypher
// Find archived review metadata for an edge
MATCH (a {id:'bg_stahl_mehrere_holbein_structural'})-[r:TRIGGERS_REGULIERUNGSFRAGE]->(b)
WHERE r.metadata_sidecar_key IS NOT NULL
RETURN type(r) AS rel, r.metadata_sidecar_key, r.confidence, r.source_url
LIMIT 5
```

Then grep `entity_metadata.jsonl` for the key — see [`sidecar/README.md`](../../review/2026-06-05_post_migration_property_cleanup/sidecar/README.md).

---

## N. Regional corridors (multi-project maps)

### N1 — Brussels / Belgium belt

```cypher
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(:Land {country_iso2:'BE'})
WHERE p.id IN [
  'p_verbiest_karreveld_brussels',
  'p_multi_brussels_reuse_in_multi',
  'p_chiro_d_itterbeek_dilbeek'
]
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
RETURN path
LIMIT 35

UNION
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(:Land {country_iso2:'BE'})
WHERE p.id IN ['p_verbiest_karreveld_brussels','p_multi_brussels_reuse_in_multi','p_chiro_d_itterbeek_dilbeek']
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_reusedokumentationfrage'})
      -[:ERFORDERT_NACHWEIS]->(nf {id:'nf_herkunfts_und_rueckbaudokumentation'})
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf)
RETURN path
LIMIT 25
```

### N2 — Berlin CRCLR cluster

```cypher
MATCH (p:Projekt)
WHERE p.id IN ['p_impact_hub_berlin_crclr_fitout','p_crclr_house_impact_hub_berlin']
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(md:Materialdepot {id:'bw_berlin_fitout_donor_sources'})
RETURN path
LIMIT 30

UNION
MATCH (p:Projekt)
WHERE p.id IN ['p_impact_hub_berlin_crclr_fitout','p_crclr_house_impact_hub_berlin']
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:HAT_BESCHAFFUNGSWEG]->(:Beschaffungsweg {name:'Digitale_Plattform'})
RETURN path
LIMIT 25
```

### N3 — London steel corridor

```cypher
MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(:Land {country_iso2:'GB'})
MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
WHERE (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
WITH p, collect(bg)[0..2] AS sample_bgs
UNWIND sample_bgs AS bg
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:NUTZT_MATERIAL]->(:Material {id:'mat_stahl'})
RETURN path
LIMIT 20

UNION
MATCH (bw:Bauwerk {id:'bw_cleveland_steel_reclaimed_stock'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)-[:LIEGT_IN_LAND]->(:Land {country_iso2:'GB'})
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path
LIMIT 15
```

### N4 — Paris circular build cluster

```cypher
MATCH (p:Projekt)
WHERE p.id IN ['p_circular_pavilion_paris','p_maison_des_canaux_paris','p_resilience_la_ferme_des_possibles_stains']
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(t)
WHERE t:Bauwerk OR t:Materialdepot
RETURN path
LIMIT 40

UNION
MATCH (p:Projekt {id:'p_circular_pavilion_paris'})-[:HAT_BAUTEILGRUPPE]->(bg)
      -[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(:Materialdepot {id:'bw_paris_material_sources_circular_pavilion'})
MATCH path = (bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(:Materialdepot)
RETURN path
LIMIT 20
```

### N5 — Zurich Werkhof pair (shared receiver building)

```cypher
MATCH (bw:Bauwerk {id:'bw_werkhof_29_receiver'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
      <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
MATCH path = (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->(bw)
RETURN path
LIMIT 30

UNION
MATCH (bw:Bauwerk {id:'bw_werkhof_29_receiver'})
      <-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]-(bg:Bauteilgruppe)
MATCH path = (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
  -[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
RETURN path
LIMIT 25
```

---

## O. Analytical snapshots (table-only)

Quick scans without graph rendering.

### O1 — Reuse status on Bauteilgruppen

```cypher
MATCH (bg:Bauteilgruppe)
RETURN bg.reuse_status AS status, count(*) AS components
ORDER BY components DESC
```

### O2 — Funktionswechsel distribution (reuse components only)

```cypher
MATCH (bg:Bauteilgruppe)-[:AUS_SPENDER|IN_EMPFANGSOBJEKT]->()
RETURN bg.funktionswechsel AS funktionswechsel, count(*) AS components
ORDER BY components DESC
```

### O3 — Logistik pattern ranking

```cypher
MATCH (bg:Bauteilgruppe)-[:HAT_LOGISTIK]->(l)
RETURN l.name AS logistik, count(*) AS components
ORDER BY components DESC
```

### O4 — Projects × regulation footprint matrix

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
WITH p, count(DISTINCT rf) AS fragen, count(DISTINCT bg) AS bgs
ORDER BY fragen DESC
LIMIT 15
MATCH (p)-[:LIEGT_IN_LAND]->(l:Land)
RETURN p.name AS projekt, l.country_iso2 AS land, bgs, fragen
ORDER BY fragen DESC
```

---

## H. Quick picker

| Goal | Query |
|------|--------|
| “Does Variant B look right?” | **A1** |
| Reuse geography | **B1**, **Map 4** |
| Cross-case substance routing | **Pattern A**, **Map 5** |
| Cross-case steel / Tragwerk | **Pattern C/D**, **Map 6**, **J3** |
| Maximum single-project density | **Map 1** (Chiro), **I1** |
| Shared donor story | **Pattern H1/H2**, **J2** |
| Compliance hub star | **Pattern E** |
| Reuse supply-network narrative | **I1**, **K4** |
| Funktionswechsel / adaptive reuse | **I3**, **O2** |
| Procurement channels | **J4**, **K1**, **K2** |
| Barrier convergence | **J7**, **D1** |
| Regional corridors | **N1–N5** |
| Proof / evidence stories | **M1–M3**, **C2** |
| Sidecar archived metadata | **M4**, **G7** |
| Health check | **G1–G4**, **G7** |

---

## Related artifacts

- Run plan: [`FINAL_PLAN_V2.md`](FINAL_PLAN_V2.md)
- Phase B taxonomy: [`VARIANT_B_TAXONOMY.md`](VARIANT_B_TAXONOMY.md)
- Audit: [`FINAL_AUDIT_REPORT.md`](FINAL_AUDIT_REPORT.md)
- Property cleanup: [`../../review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md`](../../review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md)
- Sidecar archive: [`../../review/2026-06-05_post_migration_property_cleanup/sidecar/README.md`](../../review/2026-06-05_post_migration_property_cleanup/sidecar/README.md)
