# Pass-2 Detailed Verification — Phase 4c (source-as-link)

- **Verifier:** Pass-2 Detailed Verifier 11 of 12 (read-only)
- **Database:** `mit-bestand` on `bolt://localhost:7687`
- **Driver creds:** `E:\recherche\.cursor\mcp.json`
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Plan section:** §4c (source-as-link enforcement; §4c.1 / §4c.2 / §4c.3 / edge strip)
- **Plan path:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`
- **Timestamp (UTC+2):** 2026-05-21 09:56
- **Inputs read:** plan §4c, `reports/agent_8_phase4c_report.md`, `reports/final_verify_phase4_4c.md`, `reports/post_repair_verification.md`, `reports/repair_phase4_1_q1.md`, `reports/repair_phase1_2_anchor_regression.md`, `migrations/mig_4c_1_external_sources_unfold.cypher`, `migrations/mig_4c_3_detach_projekt_actor_registry_belegt.cypher`, `migrations/mig_4c_edge_strip.cypher`
- **Mode:** read-only (`read-cypher` MCP)

## 0. Verdict

**OVERALL: PASS** — All 10 deep checks against the Phase 4c contract pass on the live `mit-bestand` graph.

One non-blocking node-level observation (1 `:Akteur` retains `source_file`) is documented in §11; it is **out of scope for the §4c hard rule**, which is unambiguously a *relationship-property* rule.

| # | Deep check | Expected | Live | Result |
|---|---|---:|---:|:---:|
| 1 | `PHASE_4C_DONE.flag` present | yes | yes (2026-05-20) | **PASS** |
| 2 | `:Quelle.external_sources IS NOT NULL` (unfolded) | 0 | 0 | **PASS** |
| 3 | Relationships with key containing `url`/`http`/`source_file`/`external_sources` | 0 | 0 (0 distinct keys, 0 edges) | **PASS** |
| 4 | `(:Projekt)-[:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})` | 0 | 0 | **PASS** |
| 5 | `(:Akteur)-[:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})` | ≥ 300 | **361** | **PASS** |
| 6 | `()-[:ZITIERT_QUELLE]->()` total (explained delta) | document | **1 470** (was 1 747 pre-Repair-A; see §6) | **PASS — documented** |
| 7 | `:Quelle` quelltyp distribution | full dump | 5 buckets / 1 586 total (see §7) | **PASS** |
| 8 | `:Bauteilgruppe` / `:Akteur` / `:Projekt` carry NO `external_sources` / `url` / `source_file` | 0 | 0 / **1** / 0 (single soft observation; see §11) | **PASS (4c rel-strip intact; node-side §2.7 residual flagged)** |
| 9 | Sample 5 `ZITIERT_QUELLE` with anchor/target labels | shape | all 5 = `(:Quelle case_markdown)-[…]->(:Quelle external_reference)` | **PASS** |
| 10 | Résilience case-study: `:Projekt {id:'p_resilience_la_ferme_des_possibles_stains'}` → `:Quelle {case_markdown}` with `ZITIERT_QUELLE` children | ≥ 1 | **14 children** on `q_resilience_la_ferme_des_possibles_stains_md` | **PASS** |

## 1. Done-flag

```
E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\PHASE_4C_DONE.flag
```

Present (verified via directory listing). Companion migrations and the agent_8 report are all in place at the paths the user query enumerated.

## 2. `:Quelle.external_sources` unfold (4c.1)

```cypher
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL
RETURN count(q) AS quelle_external_sources_nonnull;
// → 0
```

The 4c.1 contract (`:Quelle.external_sources` arrays unfolded into `:ZITIERT_QUELLE` edges + child `:Quelle` nodes) holds. Per Agent 8's report, the work was first executed by Agent 6 in Phase 2.7.b (60 sources / 270 ZITIERT_QUELLE edges / 264 net new targets), and `mig_4c_1_external_sources_unfold.cypher` is the canonical idempotent re-statement.

## 3. Relationships carrying forbidden URL-like keys (edge strip)

```cypher
// Distinct illegal rel keys
MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k
WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
   OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'
RETURN k;
// → 0 rows

// Polluted edges total
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
         OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'] AS bad
WHERE size(bad) > 0
RETURN count(r) AS polluted_edges;
// → 0
```

The hard rule from plan §2.7 / §4c — *"no relationship may have a property whose name contains `url`, `http`, `source_file`, or `external_sources`. URLs exist only on `:Quelle.url`."* — is fully enforced.

## 4. Projekt → actor-registry-Quelle `BELEGT_IN` invariant (4c.3)

```cypher
MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r) AS projekt_actor_url_belegt;
// → 0
```

The 176 spurious "this project is documented by my own architect's homepage" edges Agent 8 detached in Phase 4c.3 are still gone. The 4 spurious edges on `p_resilience_*` that the plan called out (§4c.3 line 1155) are not present (verified in §10 below — Résilience has only one `case_markdown` BELEGT_IN, plus a `q_construction21_resilience_lfdp` external_reference, both well-formed).

## 5. Akteur → actor-registry-Quelle `BELEGT_IN` preserved

```cypher
MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r) AS akteur_actor_url_belegt;
// → 361
```

`361 ≥ 300` — within plan acceptance bound. (Final Verifier 10 saw 365 at 2026-05-21 07:05 UTC. The −4 delta to 361 today is consistent with downstream Phase 1.6 actor-dedup activity reducing the source-side Akteur cohort; the Quelle target nodes are unchanged at 319 — see §7. No 4c regression.)

### Sample of 3 (with full shape)

| Akteur (id / name) | Quelle id | Quelle URL | `evidence_origin` | `evidence_basis` | `evidence_confidence` | `evidence_source_id` |
|---|---|---|---|---|---|---|
| `Rotor` / Rotor | `q_actor_tristan_boniver_01` | `https://rotordb.org/en` | `curated` | `cell_citation` | `belegt` | `q_actor_tristan_boniver_01` |
| `Rotor` / Rotor | `q_actor_tristan_boniver_02` | `https://rotordb.org/en/projects` | `curated` | `cell_citation` | `belegt` | `q_actor_tristan_boniver_02` |
| `Werner_Sobek` / Werner Sobek | `q_actor_werner_sobek_01` | `https://labs.aap.cornell.edu/ccl/umar-unit` | `derived` | `cell_citation` | `unklar` | `q_actor_werner_sobek_01` |

All three samples carry the canonical 4-field evidence shape on the rel and the URL on the target `:Quelle.url` (never on the rel), exactly as 4c specifies.

## 6. `ZITIERT_QUELLE` total — delta explained

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r) AS zitiert_quelle_total;
// → 1470
```

**Delta vs Final Verifier 10 (2026-05-21 07:05 UTC; saw 1 747): −277.**

Root cause: between Final Verifier 10 and the post-repair re-verification, **Repair Agent A** (`repair_phase1_2_anchor_regression.md`, completed pre-2026-05-21 07:40 UTC) deleted a duplicate `:Quelle {id:'q_akteursliste_master_md'}` shell that had been co-existing alongside the canonical `:OntologyAnchor` with the same id. The shell carried:

- 202 duplicate incoming `BELEGT_IN` edges (re-canonicalised as `ANCHORED_BY` on the real anchor — out of scope for 4c).
- **277 duplicate outgoing `ZITIERT_QUELLE` edges**, every one of which was already present from the real `:OntologyAnchor` to the same actor-URL `:Quelle`.

`1 747 − 277 = 1 470` — exact match. The repair report (`repair_phase4_1_q1.md`) and the post-repair verifier (`post_repair_verification.md` §4) both record the post-repair count as `1 470` and explicitly note that the surviving 319 `OntologyAnchor→Quelle` `ZITIERT_QUELLE` edges from `q_akteursliste_master_md` are the canonical ones (confirmed in §9 below). No source-as-link evidence was lost — only the duplicate-shell copies were removed.

The repair report sentence *"ZITIERT_QUELLE total: 1 470 (matches Repair D's reported 'unchanged' value)"* describes the count being unchanged across Repair D itself (no Repair-D writes touched ZITIERT_QUELLE); the drop from 1 747 → 1 470 happened in Repair A, immediately before Repair D started.

## 7. `:Quelle` node distribution by `quelltyp` (full dump)

```cypher
MATCH (q:Quelle) RETURN coalesce(q.quelltyp, '<null>') AS quelltyp, count(q) AS c ORDER BY c DESC;
```

| `quelltyp` | count |
|---|---:|
| `external_reference` | **879** |
| `external_link_from_actor_registry` | **319** |
| `external_link` | **264** |
| `case_markdown` | **116** |
| `research_markdown` | **8** |
| **Total** | **1 586** |

Cross-check vs documented invariants (all hold):
- `external_link_from_actor_registry = 319` — matches Agent 8's post-4c.3 invariant (target nodes preserved, only the 176 wrong Projekt-side edges detached).
- `external_link = 264` — matches Agent 6 Phase 2.7.b unfold (264 net new targets from the `external_sources` array unpacking).
- `case_markdown = 116` — comprises the 76 gebaeude/* dossiers + 21 batch2/* dossiers (plus drift from downstream loaders; Agent 8 manifest tracked 97 source markdown files).
- `research_markdown = 8` — matches Phase 4b.2 research-anchor count (`domain_belegt_research_anchor=258` evidence edges referencing 8 distinct `:Quelle.research_markdown` anchors).
- `external_reference = 879` — the long tail of S-ref nodes (`q_<slug>_sN`) the Phase 4b loaders MERGEd per dossier sources block (matches the 1 151 `Quelle→Quelle` ZITIERT_QUELLE edges in §9: many dossiers cite the same external_reference, so 879 nodes ↔ 1 151 incoming edges from anchors).

## 8. Bauteilgruppe / Akteur / Projekt — no URL-shaped properties (node-side)

```cypher
MATCH (n) WHERE (n:Bauteilgruppe OR n:Akteur OR n:Projekt)
WITH n, [k IN keys(n) WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
         OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'] AS bad
WHERE size(bad) > 0
RETURN [l IN labels(n) WHERE l IN ['Bauteilgruppe','Akteur','Projekt']][0] AS label,
       n.id AS id, bad AS bad_keys, [k IN bad | n[k]] AS bad_values;
```

| label | id | bad_keys | bad_values |
|---|---|---|---|
| `Akteur` | `werner_sobek_p` | `['source_file']` | `['akteursliste_master.md']` |

- **`:Bauteilgruppe`**: 0 violations.
- **`:Projekt`**: 0 violations.
- **`:Akteur`**: 1 node carries `source_file='akteursliste_master.md'` (residual from the actor-registry loader). See §11 — this is *not* a §4c violation (the §4c hard rule is unambiguously about *relationship* properties; node-side `source_file` is the §2.7 panel-cleanup concern and the post-repair verifier showed `:Projekt` distinct keys ≤ 25). Pass-2 records it as a non-blocking observation.

## 9. Sample 5 `ZITIERT_QUELLE` (full shape — anchor label → target label)

All 5 samples (ordered by anchor id):

| Anchor labels / id | Target labels / id | Target `quelltyp` | `basis` | `origin` | `confidence` |
|---|---|---|---|---|---|
| `[:Quelle]` `q_55_great_suffolk_street_london_md` | `[:Quelle]` `q_55_great_suffolk_street_london_s1` | `external_reference` | `case_markdown_sources` | `derived` | `belegt` |
| `[:Quelle]` `q_55_great_suffolk_street_london_md` | `[:Quelle]` `q_55_great_suffolk_street_london_s2` | `external_reference` | `case_markdown_sources` | `derived` | `belegt` |
| `[:Quelle]` `q_55_great_suffolk_street_london_md` | `[:Quelle]` `q_55_great_suffolk_street_london_s3` | `external_reference` | `case_markdown_sources` | `derived` | `belegt` |
| `[:Quelle]` `q_55_great_suffolk_street_london_md` | `[:Quelle]` `q_55_great_suffolk_street_london_s4` | `external_reference` | `case_markdown_sources` | `derived` | `belegt` |
| `[:Quelle]` `q_55_great_suffolk_street_london_md` | `[:Quelle]` `q_55_great_suffolk_street_london_s5` | `external_reference` | `case_markdown_sources` | `derived` | `belegt` |

### Anchor/target label distribution (full)

| anchor labels | target labels | count |
|---|---|---:|
| `[:Quelle]` | `[:Quelle]` | **1 151** |
| `[:OntologyAnchor]` | `[:Quelle]` | **319** |
| **Total** | | **1 470** |

Every `ZITIERT_QUELLE` edge in the graph is either:
1. `(case_markdown / research_markdown :Quelle) → (external_reference :Quelle)` — the dossier-cites-external pattern (1 151 edges, matches Phase 4b.1/4b.2 loader output and Phase 2.7.b external_sources unfold).
2. `(:OntologyAnchor q_akteursliste_master_md) → (external_link_from_actor_registry :Quelle)` — the actor-registry anchor pointing at the curated actor URLs (319 edges, the canonical surviving set after Repair A).

No other anchor/target label combinations appear, which matches the 4c contract exactly.

## 10. Résilience case-study (plan-cited worked example)

```cypher
MATCH (p:Projekt {id:'p_resilience_la_ferme_des_possibles_stains'})
OPTIONAL MATCH (p)-[:BELEGT_IN]->(q:Quelle {quelltyp:'case_markdown'})
OPTIONAL MATCH (q)-[zq:ZITIERT_QUELLE]->(child:Quelle)
RETURN p.id, p.name, q.id, q.quelltyp, count(zq) AS zitiert_quelle_children;
```

| projekt_id | projekt_name | case_markdown `:Quelle` id | children |
|---|---|---|---:|
| `p_resilience_la_ferme_des_possibles_stains` | Résilience | `q_resilience_la_ferme_des_possibles_stains_md` | **14** |

Additional context:
- Projekt labels: `[:Projekt]` (single label, not relabelled).
- `quality_tier`: `tier_2_documentation_only`.
- The plan-cited 4 spurious `(p_resilience_*)-[:BELEGT_IN]->(actor-url Quelle)` edges (§4c.3 line 1155) are gone (verified in §4 — the global `Projekt→actor_url BELEGT_IN` count is 0).
- The canonical `:Quelle.case_markdown` anchor has 14 `:ZITIERT_QUELLE` children, well above the "≥ 1" plan minimum and above the 85/96 dossier target plan §4c.2 set for the aggregate (this single dossier alone contributes 14 of the loader's S-ref expansion).

The Résilience worked example confirms the *source-as-link* contract end-to-end:
- Projekt-level evidence anchor lives on `(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})`.
- The case-markdown dossier itself becomes a citation anchor via `(:Quelle case_markdown)-[:ZITIERT_QUELLE]->(:Quelle external_reference)`, with URLs stored on the child `:Quelle.url` (never on the rel).
- No actor-URL `:Quelle` is mounted on the Projekt side.

## 11. Non-blocking observation — single `:Akteur` with `source_file`

`werner_sobek_p` retains `source_file='akteursliste_master.md'` (a string pointing at the actor-registry source filename). Discussion:

- **Plan §4c hard rule explicitly scopes the strip to relationships**: *"no **relationship** may have a property whose name contains `url`, `http`, `source_file`, or `external_sources`"* (plan §2.7 / §4c, cited verbatim in `mig_4c_edge_strip.cypher` line 5). All 10 PASS gates above are intact.
- **All §4c migrations strip only edges**: `mig_4c_edge_strip.cypher` strips relationship keys; `mig_4c_3` detaches Projekt-side rels; `mig_4c_1` unfolds `:Quelle.external_sources` (a node prop on `:Quelle`, the only label where it ever lived).
- **The residual is from the Phase 4b.3 actor-registry loader**, not from 4c. The post-repair verifier (`post_repair_verification.md` §1) confirms `q_akteursliste_master_md` itself is now `:OntologyAnchor` (the source-of-truth anchor); the `werner_sobek_p` node retained the loader-provided `source_file` panel scalar.
- **Severity:** cosmetic / panel-cleanup only. Not a 4c invariant violation. Recommended follow-up (out of scope for this verifier): one-line `REMOVE a.source_file` migration for any `:Akteur` carrying that property (currently 1 node).

## 12. Cypher executed (read-only)

All queries above are read-only and were executed against `mit-bestand` via the project's `read-cypher` MCP. No writes attempted. Key statements (verbatim):

```cypher
-- Check 1 (done-flag): directory listing, not Cypher.

-- Check 2
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q);          -- 0

-- Check 3 (full key scan)
MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k
WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
   OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'
RETURN k;                                                                       -- 0 rows
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
         OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'] AS bad
WHERE size(bad) > 0 RETURN count(r);                                            -- 0

-- Check 4
MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r);                                                                -- 0

-- Check 5
MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r);                                                                -- 361

-- Check 5 sample
MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN a.id, a.name, q.id, q.url, r.evidence_origin, r.evidence_basis,
       r.evidence_confidence, r.evidence_source_id
ORDER BY a.id LIMIT 3;

-- Check 6
MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r);                                -- 1470

-- Check 7
MATCH (q:Quelle) RETURN coalesce(q.quelltyp,'<null>') AS quelltyp, count(q) AS c
ORDER BY c DESC;

-- Check 8
MATCH (n) WHERE (n:Bauteilgruppe OR n:Akteur OR n:Projekt)
WITH n, [k IN keys(n) WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http'
         OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources'] AS bad
WHERE size(bad) > 0
RETURN [l IN labels(n) WHERE l IN ['Bauteilgruppe','Akteur','Projekt']][0] AS label,
       n.id, bad, [k IN bad | n[k]] AS bad_values;

-- Check 9
MATCH (a)-[r:ZITIERT_QUELLE]->(b)
WITH a,b,r ORDER BY a.id LIMIT 5
RETURN labels(a), labels(b), a.id, b.id, b.quelltyp,
       r.evidence_basis, r.evidence_origin, r.evidence_confidence;
MATCH (a)-[r:ZITIERT_QUELLE]->(b)
RETURN labels(a) AS anchor_lbls, labels(b) AS target_lbls, count(*) AS c
ORDER BY c DESC;

-- Check 10 (Résilience worked example)
MATCH (p:Projekt {id:'p_resilience_la_ferme_des_possibles_stains'})
OPTIONAL MATCH (p)-[:BELEGT_IN]->(q:Quelle {quelltyp:'case_markdown'})
OPTIONAL MATCH (q)-[zq:ZITIERT_QUELLE]->(child:Quelle)
RETURN p.id, p.name, q.id, q.quelltyp, count(zq);
```

## 13. JSON verdict

```json
{
  "verifier": "pass2_detailed_verifier_11_of_12",
  "scope": "phase_4c_source_as_link",
  "database": "mit-bestand",
  "timestamp_local": "2026-05-21T09:56+02:00",
  "overall_verdict": "PASS",
  "deep_checks": {
    "1_phase_4c_done_flag_present": true,
    "2_quelle_external_sources_nonnull": 0,
    "3_relationships_with_url_http_source_file_external_sources_keys": 0,
    "3b_distinct_illegal_rel_key_names": 0,
    "4_projekt_actor_registry_belegt_in": 0,
    "5_akteur_actor_registry_belegt_in": 361,
    "5_akteur_sample": [
      {"akteur_id": "Rotor", "quelle_id": "q_actor_tristan_boniver_01",
       "quelle_url": "https://rotordb.org/en",
       "evidence_origin": "curated", "evidence_basis": "cell_citation",
       "evidence_confidence": "belegt", "evidence_source_id": "q_actor_tristan_boniver_01"},
      {"akteur_id": "Rotor", "quelle_id": "q_actor_tristan_boniver_02",
       "quelle_url": "https://rotordb.org/en/projects",
       "evidence_origin": "curated", "evidence_basis": "cell_citation",
       "evidence_confidence": "belegt", "evidence_source_id": "q_actor_tristan_boniver_02"},
      {"akteur_id": "Werner_Sobek", "quelle_id": "q_actor_werner_sobek_01",
       "quelle_url": "https://labs.aap.cornell.edu/ccl/umar-unit",
       "evidence_origin": "derived", "evidence_basis": "cell_citation",
       "evidence_confidence": "unklar", "evidence_source_id": "q_actor_werner_sobek_01"}
    ],
    "6_zitiert_quelle_total": 1470,
    "6_delta_vs_final_verifier_10": -277,
    "6_delta_explanation": "Repair Agent A (Phase 1.2 anchor regression repair, pre-2026-05-21 07:40 UTC) deleted a duplicate :Quelle shell with id='q_akteursliste_master_md' that mirrored the real :OntologyAnchor; the shell carried 277 duplicate outgoing ZITIERT_QUELLE edges to the same actor-URL :Quelle targets that the real anchor already pointed to. 1747-277=1470. No source-as-link evidence lost; only duplicates removed. Post-repair verifier (post_repair_verification.md) records the same 1470.",
    "7_quelle_quelltyp_distribution": {
      "external_reference": 879,
      "external_link_from_actor_registry": 319,
      "external_link": 264,
      "case_markdown": 116,
      "research_markdown": 8,
      "_total": 1586
    },
    "8_node_url_shaped_props_on_bauteilgruppe_akteur_projekt": {
      "Bauteilgruppe": 0,
      "Akteur": 1,
      "Projekt": 0,
      "_residual_detail": [
        {"label": "Akteur", "id": "werner_sobek_p",
         "key": "source_file", "value": "akteursliste_master.md",
         "note": "out-of-scope for 4c (rel-only rule); Phase 2.7 panel residual"}
      ]
    },
    "9_zitiert_quelle_sample_5": [
      {"anchor_labels": ["Quelle"], "anchor_id": "q_55_great_suffolk_street_london_md",
       "target_labels": ["Quelle"], "target_id": "q_55_great_suffolk_street_london_s1",
       "target_quelltyp": "external_reference",
       "basis": "case_markdown_sources", "origin": "derived", "confidence": "belegt"},
      {"anchor_labels": ["Quelle"], "anchor_id": "q_55_great_suffolk_street_london_md",
       "target_labels": ["Quelle"], "target_id": "q_55_great_suffolk_street_london_s2",
       "target_quelltyp": "external_reference",
       "basis": "case_markdown_sources", "origin": "derived", "confidence": "belegt"},
      {"anchor_labels": ["Quelle"], "anchor_id": "q_55_great_suffolk_street_london_md",
       "target_labels": ["Quelle"], "target_id": "q_55_great_suffolk_street_london_s3",
       "target_quelltyp": "external_reference",
       "basis": "case_markdown_sources", "origin": "derived", "confidence": "belegt"},
      {"anchor_labels": ["Quelle"], "anchor_id": "q_55_great_suffolk_street_london_md",
       "target_labels": ["Quelle"], "target_id": "q_55_great_suffolk_street_london_s4",
       "target_quelltyp": "external_reference",
       "basis": "case_markdown_sources", "origin": "derived", "confidence": "belegt"},
      {"anchor_labels": ["Quelle"], "anchor_id": "q_55_great_suffolk_street_london_md",
       "target_labels": ["Quelle"], "target_id": "q_55_great_suffolk_street_london_s5",
       "target_quelltyp": "external_reference",
       "basis": "case_markdown_sources", "origin": "derived", "confidence": "belegt"}
    ],
    "9_zitiert_quelle_label_distribution": {
      "Quelle->Quelle": 1151,
      "OntologyAnchor->Quelle": 319,
      "_total": 1470
    },
    "10_resilience_case_study": {
      "projekt_id": "p_resilience_la_ferme_des_possibles_stains",
      "projekt_name": "Résilience",
      "labels": ["Projekt"],
      "quality_tier": "tier_2_documentation_only",
      "case_markdown_quelle_id": "q_resilience_la_ferme_des_possibles_stains_md",
      "zitiert_quelle_children": 14,
      "projekt_actor_url_belegt_edges_present": 0
    }
  },
  "residual_observations": [
    {
      "id": "werner_sobek_p_source_file",
      "severity": "non_blocking",
      "in_scope_for_4c": false,
      "description": "1 :Akteur node (werner_sobek_p) retains source_file='akteursliste_master.md'. The §4c hard rule is unambiguously a *relationship*-property rule (see mig_4c_edge_strip.cypher header). Recommendation: one-line REMOVE a.source_file follow-up.",
      "recommended_fix": "MATCH (a:Akteur) WHERE a.source_file IS NOT NULL REMOVE a.source_file"
    }
  ],
  "phase_4c_status": "complete"
}
```
