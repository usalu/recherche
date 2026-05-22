# Bauteilbörse Subgraph — Schema Reference

**Generated:** 2026-06-01 from live `mit-bestand`
**Scope:** the 30 TAKE actors classified as Bauteilbörse / construction-material reuse marketplaces, plus all the node labels and relationship types incident to them.
**Use this as the schema contract** when adding new Bauteilbörsen so they follow the same shape.

---

## 1. Quick visual

```
                       (:Quelle)<--[:BELEGT_IN]--+
                                                 |
        (:Akteurtyp)<--[:HAT_AKTEURTYP]----------|
        (:Akteurrolle)<--[:HAT_AKTEURROLLE]------|
        (:Land)<--[:LIEGT_IN_LAND]---------------|
        (:Marktmodell)<--[:HAT_MARKTMODELL]------|--+
        (:Geschaeftsmodell)<--[:HAT_GESCHAEFTSMODELL]-+
        (:Methode)<--[:HAT_METHODE]--------------|
                                                 |
                                          (:Akteur)                    
                                                ^|       (anchor)
                          [:BETRIEBEN_VON]----->+|
                          [:VERBUNDEN_MIT_AKTEUR]+|        
                                                 |
        (:Material)<--[:NUTZT_MATERIAL]----------|
        (:Bauteiltyp)<--[:HAT_BAUTEILTYP]--------|
        (:Projekt|:Programm)<--[:BETEILIGT_AN]---+

   Exception: software_restado is :Software (single case), not :Akteur.
              Same edge model otherwise.
```

---

## 2. The anchor node

### Required label

| Case | Label |
|---|---|
| Standard | `:Akteur` (29 / 30 anchors) |
| Software/platform-only actor | `:Software` (only `software_restado` currently) |

### Required properties

| Property | Type | Example | Note |
|---|---|---|---|
| `id` | string, snake_case | `bauteilboerse_bremen` | Globally unique; used as join key everywhere |
| `name` | string | `Bauteilbörse Bremen` | Human-readable display name |
| `source_scope` | string | `actor_registry_context` | Where the node was created; `actor_registry_context` for curated Bauteilbörsen |

### Optional properties (commonly present)

| Property | Type | Purpose |
|---|---|---|
| `aliases` | string[] | Other names the actor is known under |
| `review_status` | string | e.g., `needs_source_url_review` |
| `source_quality_summary` | string | Provenance summary |
| `source_trust_score` | number | 0–1 |

---

## 3. Required outgoing edges per anchor

These edges define the **minimum schema contract**. A new Bauteilbörse should have all of them.

| Relation | Target label | Cardinality | Purpose | Current coverage |
|---|---|---:|---|---:|
| `HAT_AKTEURTYP` | `:Akteurtyp` | 1+ | Actor archetype (typically `at_materialhub_bauteilboerse`) | 29/30 (software_restado is `:Software`, no type edge) |
| `LIEGT_IN_LAND` | `:Land` | 1 | Primary country | 30/30 |
| `HAT_AKTEURROLLE` | `:Akteurrolle` | 3–7 | Functional roles | 30/30 |
| `HAT_MARKTMODELL` | `:Marktmodell` | 1 | Transaction type | 30/30 |
| `HAT_GESCHAEFTSMODELL` | `:Geschaeftsmodell` | 1–3 | Business-model archetype | 30/30 |
| `BELEGT_IN` | `:Quelle` | 2–5 | Evidence URL nodes (operator pages) | 30/30 |

---

## 4. Strongly recommended edges (most anchors have)

| Relation | Target label | Cardinality | When to add |
|---|---|---:|---|
| `HAT_METHODE` | `:Methode` | 0–3 | If the operator runs urban mining / catalogue / inventory workflows (gm_dienstleistung_urban_mining and gm_saas_inventar_plattform clusters add these automatically) |
| `NUTZT_MATERIAL` | `:Material` | 0–7 | Per material the actor explicitly handles (closed-set `mat_*` only — see §7) |
| `HAT_BAUTEILTYP` | `:Bauteiltyp` | 0–10 | Per component category the actor explicitly handles (closed-set `bt_*` only) |

⚠ **Strict-evidence rule:** add `NUTZT_MATERIAL` / `HAT_BAUTEILTYP` only when a fetched first-party page literally names the material (e.g. "Material: Keramik") or the component (e.g. "Türen & Zargen"). Search-snippet scope is not enough.

---

## 5. Contextual edges (situational)

| Relation | Direction | Target label | When to add |
|---|---|---|---|
| `BETRIEBEN_VON` | outgoing | `:Akteur` | If the platform/software is operated by a separate operator (e.g. `software_restado -[:BETRIEBEN_VON]-> concular`) |
| `VERBUNDEN_MIT_AKTEUR` | both | `:Akteur` | Partner / network link between two Bauteilbörsen (e.g. `bauteilnetz_deutschland` members) |
| `BETEILIGT_AN` | outgoing | `:Projekt` / `:Programm` | If the actor is part of a research / pilot project |
| `GEHÖRT_ZU` | outgoing | `:Land` (legacy) | Legacy duplicate of `LIEGT_IN_LAND`; prefer the latter |
| `NUTZT_SOFTWARE` | outgoing | `:Software` | If the operator uses a known platform (e.g. an Akteur using `software_restado`) |

---

## 6. Controlled vocabularies (live IDs to reuse)

### 6.1 `:Akteurtyp` (used by 30 anchors)
| ID | Name | Used by |
|---|---|---:|
| `at_materialhub_bauteilboerse` | Materialhub_Bauteilboerse | 28 |
| `at_software_tool_anbieter` | Software_Tool_Anbieter | 3 (additional, for app/SaaS actors) |
| `at_unternehmen` | Unternehmen | 1 (rotordc, additional) |
| `at_ngo_verband_netzwerk` | NGO_Verband_Netzwerk | 1 (bauteilnetz_deutschland) |

### 6.2 `:Akteurrolle` (top roles for Bauteilbörsen)
| ID | Used by (of 30) |
|---|---:|
| `ar_materialbroker` | 29 |
| `ar_materiallieferung_markt` | 29 |
| `ar_software_digitalisierung` | 28 |
| `ar_rueckbau_bauteilernte_logistik` | 25 |
| `ar_reuse_zirkularitaetsberatung` | 16 |
| `ar_aufbereitung_refurbishment` | 14 |
| `ar_bildung_wissenstransfer` | 8 |
| `ar_forschung_dokumentation` | 3 |

### 6.3 `:Marktmodell` — transaction type, exactly one per actor
| ID | Name | Used by |
|---|---|---:|
| `mm_plattform_vermittelt` | Plattform-Kauf | 16 |
| `mm_kauf_gebraucht` | Kauf gebraucht | 12 |
| `mm_spende` | Spende | 2 |

### 6.4 `:Geschaeftsmodell` — business-model archetype, 1–3 per actor
| ID | Name | Used by |
|---|---|---:|
| `gm_marketplace_vermittlung` | Multi-Vendor-Marktplatz | 17 |
| `gm_dienstleistung_urban_mining` | Urban-Mining-Dienstleister mit Verkaufskanal | 13 |
| `gm_shop_eigenstock` | Shop mit Eigenstock | 11 |
| `gm_netzwerk_aggregator` | Netzwerk / Aggregator / Redistribution | 2 |
| `gm_saas_inventar_plattform` | SaaS-Inventarplattform | 1 |

### 6.5 `:Methode` (only urban-mining + saas clusters)
| ID | Used by |
|---|---:|
| `meth_urban_mining` | 13 |
| `meth_pre_deconstruction_audit` | 13 |
| `meth_bauteilkatalogisierung` | 13 |
| `meth_materialinventur` | 1 |
| `meth_abrissmonitoring` | 1 |

### 6.6 `:Material` — closed set of 15 IDs
`mat_aluminium`, `mat_beton`, `mat_daemmstoff`, `mat_glas`, `mat_gusseisen`, `mat_holz`, `mat_keramik`, `mat_kunststoff`, `mat_lehm`, `mat_naturstein`, `mat_recyclingbeton`, `mat_stahl`, `mat_stahlbeton`, `mat_stroh`, `mat_ziegel`

### 6.7 `:Bauteiltyp` — closed set of 13 commonly used IDs
`bt_ausbau`, `bt_boden`, `bt_dach`, `bt_daemmung`, `bt_decke`, `bt_fassade`, `bt_fenster`, `bt_gelaender`, `bt_stuetze`, `bt_technik`, `bt_traeger`, `bt_treppe`, `bt_tuer`, `bt_wand` (plus `bt_mehrere` for explicit batches only — do not use as a placeholder).

### 6.8 `:Land` — used countries
`land_belgien`, `land_daenemark`, `land_deutschland`, `land_frankreich`, `land_niederlande`, `land_norwegen`, `land_oesterreich`, `land_schweiz`, `land_vereinigtes_koenigreich`.

### 6.9 `:Quelle` — evidence URLs
Properties: `id` (`q_url_<md5>`), `url`, `quelltyp` (`external_link` for operator pages), `title` (optional).
Use a deterministic ID: `q_url_` + md5(canonical URL). Each `BELEGT_IN` edge points at one Quelle node.

---

## 7. Cluster fingerprints — what auto-derives from `HAT_GESCHAEFTSMODELL`

When an anchor has a particular Geschäftsmodell, the following Akteurrolle / Methode edges should be present (gap-filled if missing):

| Geschäftsmodell | Auto-fingerprint Akteurrollen | Auto-fingerprint Methoden |
|---|---|---|
| `gm_shop_eigenstock` | `ar_materialbroker` | — |
| `gm_marketplace_vermittlung` | `ar_materialbroker`, `ar_software_digitalisierung` | — |
| `gm_dienstleistung_urban_mining` | `ar_rueckbau_bauteilernte_logistik`, `ar_aufbereitung_refurbishment`, `ar_materiallieferung_markt`, `ar_reuse_zirkularitaetsberatung` | `meth_urban_mining`, `meth_pre_deconstruction_audit`, `meth_bauteilkatalogisierung` |
| `gm_saas_inventar_plattform` | `ar_software_digitalisierung`, `ar_forschung_dokumentation` | `meth_materialinventur`, `meth_bauteilkatalogisierung`, `meth_abrissmonitoring` |
| `gm_netzwerk_aggregator` | `ar_bildung_wissenstransfer`, `ar_forschung_dokumentation`, `ar_materialbroker` | — |

---

## 8. Worked example — `bauteilboerse_bremen`

```cypher
(:Akteur {id:'bauteilboerse_bremen', name:'Bauteilbörse Bremen', source_scope:'actor_registry_context'})

-- Required
  -[:HAT_AKTEURTYP]-> (:Akteurtyp {id:'at_materialhub_bauteilboerse'})
  -[:LIEGT_IN_LAND]->  (:Land     {id:'land_deutschland'})
  -[:HAT_MARKTMODELL]-> (:Marktmodell {id:'mm_kauf_gebraucht'})
  -[:HAT_GESCHAEFTSMODELL]-> (:Geschaeftsmodell {id:'gm_shop_eigenstock'})
  -[:HAT_GESCHAEFTSMODELL]-> (:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})

-- Roles (subset shown)
  -[:HAT_AKTEURROLLE]-> (:Akteurrolle {id:'ar_materialbroker'})
  -[:HAT_AKTEURROLLE]-> (:Akteurrolle {id:'ar_materiallieferung_markt'})
  -[:HAT_AKTEURROLLE]-> (:Akteurrolle {id:'ar_rueckbau_bauteilernte_logistik'})
  -[:HAT_AKTEURROLLE]-> (:Akteurrolle {id:'ar_software_digitalisierung'})
  ...

-- Methoden (urban-mining fingerprint)
  -[:HAT_METHODE]-> (:Methode {id:'meth_urban_mining'})
  -[:HAT_METHODE]-> (:Methode {id:'meth_pre_deconstruction_audit'})
  -[:HAT_METHODE]-> (:Methode {id:'meth_bauteilkatalogisierung'})

-- Evidence URLs
  -[:BELEGT_IN]-> (:Quelle {id:'q_url_<md5>', url:'https://www.bauteilboerse-bremen.de/start', quelltyp:'external_link'})
  -[:BELEGT_IN]-> (:Quelle {url:'https://www.bauteilboerse-bremen.de/katalog'})
  ...

-- Strict imports (when product-level evidence exists)
  -[:NUTZT_MATERIAL]-> (:Material {id:'mat_holz'})
  -[:NUTZT_MATERIAL]-> (:Material {id:'mat_glas'})
  -[:HAT_BAUTEILTYP]-> (:Bauteiltyp {id:'bt_fenster'})
  -[:HAT_BAUTEILTYP]-> (:Bauteiltyp {id:'bt_tuer'})
  -[:HAT_BAUTEILTYP]-> (:Bauteiltyp {id:'bt_boden'})
  -[:HAT_BAUTEILTYP]-> (:Bauteiltyp {id:'bt_ausbau'})
```

---

## 9. Template — adding a new Bauteilbörse

Replace `<...>` placeholders. All vocab IDs MUST already exist (see §6); the only NEW node here is the anchor itself.

```cypher
// === Replace these ===========================================
WITH
  '<anchor_id>'                    AS aid,
  '<Display Name>'                 AS aname,
  'land_<country>'                 AS land_id,
  'mm_<transaction_type>'          AS mm_id,        // see §6.3
  ['gm_<cluster_id>']              AS gm_ids,       // 1-3 from §6.4
  ['at_materialhub_bauteilboerse'] AS type_ids,     // optional extras
  // operator-controlled URLs (2-5):
  ['https://<operator>/about',
   'https://<operator>/catalog']   AS evidence_urls,
  // optional strict imports (only with first-party evidence):
  ['mat_holz', 'mat_keramik']      AS strict_materials,   // from §6.6
  ['bt_tuer', 'bt_fenster']        AS strict_bauteiltypen // from §6.7

// === Create anchor ===========================================
MERGE (a:Akteur {id: aid})
ON CREATE SET a.name = aname,
              a.source_scope = 'actor_registry_context',
              a.review_run   = 'add_new_bauteilboerse_2026_06_01';

// === Required edges ==========================================
WITH a, land_id, mm_id, gm_ids, type_ids, evidence_urls, strict_materials, strict_bauteiltypen
MATCH (l:Land {id: land_id})           MERGE (a)-[:LIEGT_IN_LAND]->(l);
MATCH (a {id: $aid}), (m:Marktmodell {id: $mm_id}) MERGE (a)-[:HAT_MARKTMODELL]->(m);
UNWIND $type_ids AS tid
  MATCH (a {id: $aid}), (t:Akteurtyp {id: tid}) MERGE (a)-[:HAT_AKTEURTYP]->(t);
UNWIND $gm_ids AS gid
  MATCH (a {id: $aid}), (g:Geschaeftsmodell {id: gid}) MERGE (a)-[:HAT_GESCHAEFTSMODELL]->(g);

// === Akteurrolle fingerprint based on Geschäftsmodell ========
// Run §7 logic — easiest: re-execute STEP 3 of FINAL_IMPORT_PLAN.md
// (the per-cluster `MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {...}) ... MERGE (a)-[:HAT_AKTEURROLLE]->...` patterns)

// === Methode fingerprint =====================================
// Same: re-execute STEP 4 of FINAL_IMPORT_PLAN.md.

// === Evidence URLs (BELEGT_IN) ===============================
UNWIND $evidence_urls AS url
WITH $aid AS aid, url, 'q_url_' + apoc.util.md5([url]) AS qid
MERGE (q:Quelle {id: qid})
  ON CREATE SET q.url = url, q.quelltyp = 'external_link'
WITH aid, q
MATCH (a {id: aid}) MERGE (a)-[:BELEGT_IN]->(q);

// === Strict imports (only with first-party evidence) =========
UNWIND $strict_materials AS mid
  MATCH (a {id: $aid}), (m:Material {id: mid})
  MERGE (a)-[r:NUTZT_MATERIAL]->(m)
  ON CREATE SET r.evidence_confidence='belegt',
                r.review_run='add_new_bauteilboerse_2026_06_01';

UNWIND $strict_bauteiltypen AS bid
  MATCH (a {id: $aid}), (b:Bauteiltyp {id: bid})
  MERGE (a)-[r:HAT_BAUTEILTYP]->(b)
  ON CREATE SET r.evidence_confidence='belegt',
                r.review_run='add_new_bauteilboerse_2026_06_01';
```

(`apoc.util.md5` requires APOC. If you don't have APOC, generate the `q_url_<md5>` IDs in your application code and pass them in.)

---

## 10. Validation queries — does my new actor follow the schema?

```cypher
// 10.1 — Every Bauteilbörse anchor has the 5 required edges
MATCH (a {id: $new_anchor_id})
OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)         WITH a, count(t)  AS n_typ
OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)              WITH a, n_typ, count(l) AS n_land
OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m:Marktmodell)     WITH a, n_typ, n_land, count(m) AS n_mm
OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)            WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)     WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)                WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_evidence
RETURN a.id, n_typ, n_land, n_mm, n_gm, n_roles, n_evidence,
       CASE WHEN n_typ>=1 AND n_land=1 AND n_mm=1 AND n_gm>=1 AND n_roles>=3 AND n_evidence>=2
            THEN 'OK' ELSE 'MISSING_REQUIRED' END AS schema_check;

// 10.2 — Materials/Bauteiltypen use only closed-set IDs
MATCH (a {id: $new_anchor_id})-[:NUTZT_MATERIAL]->(m)
WHERE NOT m.id STARTS WITH 'mat_' OR NOT m:Material
RETURN 'INVALID_MATERIAL' AS issue, m.id;

MATCH (a {id: $new_anchor_id})-[:HAT_BAUTEILTYP]->(b)
WHERE NOT b.id STARTS WITH 'bt_' OR NOT b:Bauteiltyp
RETURN 'INVALID_BAUTEILTYP' AS issue, b.id;

// 10.3 — Fingerprint completeness: every actor with gm_dienstleistung_urban_mining
//        should also have ar_rueckbau_bauteilernte_logistik and meth_urban_mining
MATCH (a {id: $new_anchor_id})-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(:Akteurrolle {id:'ar_rueckbau_bauteilernte_logistik'})
OPTIONAL MATCH (a)-[:HAT_METHODE]->(:Methode {id:'meth_urban_mining'})
WITH a, count(*) AS dummy
// adjust as needed for your check
RETURN a.id, 'fingerprint check' AS test;

// 10.4 — Reuse: which other Bauteilbörsen share my Geschäftsmodell + Land?
MATCH (mine {id: $new_anchor_id})-[:HAT_GESCHAEFTSMODELL]->(g),
      (mine)-[:LIEGT_IN_LAND]->(l)
MATCH (peer)-[:HAT_GESCHAEFTSMODELL]->(g),
      (peer)-[:LIEGT_IN_LAND]->(l)
WHERE peer.id <> mine.id
RETURN peer.id, g.id, l.id ORDER BY peer.id;
```

---

## 11. Per-anchor reference table (current 30)

| Anchor | Land | Akteurtyp(en) | Geschäftsmodell(e) | Marktmodell |
|---|---|---|---|---|
| `articonnex` | land_frankreich | at_materialhub_bauteilboerse | gm_shop_eigenstock | mm_kauf_gebraucht |
| `backacia` | land_frankreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_dienstleistung_urban_mining | mm_plattform_vermittelt |
| `baticycle` | land_frankreich | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `batiterre` | land_belgien | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `batrecup` | land_frankreich | at_materialhub_bauteilboerse + at_software_tool_anbieter | gm_marketplace_vermittlung | mm_spende |
| `baukarussell` | land_oesterreich | at_materialhub_bauteilboerse | gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `bauteilboerse_bremen` | land_deutschland | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `bauteilladen_winterthur` | land_schweiz | at_materialhub_bauteilboerse | gm_shop_eigenstock | mm_kauf_gebraucht |
| `bauteilnetz_deutschland` | land_deutschland | at_ngo_verband_netzwerk | gm_netzwerk_aggregator | mm_plattform_vermittelt |
| `building_spares_market` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `cornermat_retrival` | land_belgien | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `cycle_up` | land_frankreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_dienstleistung_urban_mining | mm_plattform_vermittelt |
| `cycle_zero` | land_frankreich | at_materialhub_bauteilboerse + at_software_tool_anbieter | gm_marketplace_vermittlung | mm_spende |
| `enviromate` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `gebruiktebouwmaterialen` | land_niederlande | at_materialhub_bauteilboerse | gm_shop_eigenstock | mm_kauf_gebraucht |
| `genbyg` | land_daenemark | at_materialhub_bauteilboerse | gm_shop_eigenstock | mm_kauf_gebraucht |
| `insert_marketplace` | land_niederlande | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `material_index` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_dienstleistung_urban_mining + gm_saas_inventar_plattform | mm_plattform_vermittelt |
| `materialenbank_leuven_atelier_circuler` | land_belgien | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `materialrest24` | land_deutschland | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `r_place` | land_frankreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `re_store_harvestmap_vienna` | land_oesterreich | at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `reempro` | land_frankreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_dienstleistung_urban_mining | mm_plattform_vermittelt |
| `rotordc` | land_belgien | at_unternehmen + at_materialhub_bauteilboerse | gm_shop_eigenstock + gm_dienstleistung_urban_mining | mm_kauf_gebraucht |
| `salvoweb` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_netzwerk_aggregator | mm_plattform_vermittelt |
| `skop_marketplace` | land_frankreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung + gm_dienstleistung_urban_mining | mm_plattform_vermittelt |
| `software_restado` | land_deutschland | *(none — `:Software` label is the classification)* | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `surplus_building_and_plumbing_materials` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `sustainability_yard` | land_vereinigtes_koenigreich | at_materialhub_bauteilboerse + at_software_tool_anbieter | gm_marketplace_vermittlung | mm_plattform_vermittelt |
| `useagain_bauteilclick` | land_schweiz | at_materialhub_bauteilboerse | gm_marketplace_vermittlung | mm_plattform_vermittelt |

---

## 12. Anti-patterns / common mistakes

| Mistake | Why it's wrong |
|---|---|
| Using `:Software` instead of `:Akteur` for a non-software-only operator | `:Software` is reserved for actual software products. Operators are `:Akteur`. |
| `bt_mehrere` as a placeholder when categories aren't extracted | Reserved for explicit *batches* of mixed components, not "I don't know yet". |
| Inventing new `mat_*` / `bt_*` / `mm_*` / `at_*` IDs | All four are closed sets. If nothing fits, log a vocab proposal — don't create an off-vocab node. |
| Importing materials from third-party scope descriptions | `belegt` requires first-party fetched HTML with the material literally named. Categories or English/French scope words don't count without the material noun (e.g. `carrelage` ≠ `mat_keramik` unless source says "céramique"). |
| Multiple `HAT_MARKTMODELL` per actor | Each anchor gets exactly one — that's the per-transaction mechanism. Use multiple `HAT_GESCHAEFTSMODELL` for hybrid actors instead. |
| Skipping `BELEGT_IN` evidence | Every claim must be evidence-backed. The 30 TAKE actors all have 2–5 first-party URLs. |

---

## 13. Quick Cypher recipes

```cypher
// All current Bauteilbörse anchors (Akteur OR Software with HAT_GESCHAEFTSMODELL)
MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell)
WHERE a:Akteur OR a:Software
RETURN a.id, labels(a) ORDER BY a.id;

// All Bauteilbörsen in one country
MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell),
      (a)-[:LIEGT_IN_LAND]->(:Land {id:'land_deutschland'})
RETURN a.id;

// Find peers: same Geschäftsmodell archetype
MATCH (peer)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_shop_eigenstock'})
RETURN peer.id;

// What Material/Bauteiltyp coverage exists per anchor?
MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell)
OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(m)
OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(b)
WITH a.id AS actor, collect(DISTINCT m.id) AS mats, collect(DISTINCT b.id) AS bts
RETURN actor, size(mats) AS n_mat, size(bts) AS n_bt, mats, bts
ORDER BY size(mats)+size(bts) DESC;
```
