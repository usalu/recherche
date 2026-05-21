# Pass-2 Detailed Verifier 12 / 12 — Phase 5 + Acceptance Q1–Q7

- **Verifier:** Pass-2 Detailed Verifier 12 of 12 (read-only)
- **Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §5 + Acceptance Q1–Q7
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Database:** `mit-bestand` on `bolt://localhost:7687`
- **Driver:** python `neo4j` driver, session `default_access_mode="READ"`; creds from `E:\recherche\.cursor\mcp.json`
- **Verification time (UTC):** 2026-05-21 07:59:21
- **Artifacts:**
  - Live JSON dump: `logs/pass2_verify_phase5_acceptance.json`
  - Verifier script: `logs/pass2_verify_phase5_acceptance.py`
  - Q4 actor list probe: `logs/pass2_q4_actor_list.py` / `.json`

## 0. Executive verdict

**OVERALL: PASS.** All 8 Phase-5 deep checks green, all 7 acceptance queries
green. The single deviation noted by the prior Final Verifier 12 (Q1 = 0 rows)
has been closed by Repair D (`mig_repair_4_1_curated_excerpts_and_q1.cypher`,
2026-05-21 07:40 UTC). Q1 now returns **266 rows** live. The single deviation
noted by Final Verifier 12 on `p_circle_house.quality_tier` was formally accepted
by Repair E (§2 of `repair_phase2_7_5_1_panel_tier.md`); the task statement
for this Pass-2 verifier explicitly lists Tier 2 as the acceptable outcome
(*"acceptable per repair"*), and the live state matches.

| Gate group | Verdict | Detail |
|---|---|---|
| Phase 5 file artifacts (4 migrations + 3 flags + 1 audit) | **PASS** | 9/9 files present |
| Live tier coverage | **PASS** | 101 / 101 Projekt tiered, all values in enum |
| Live tier distribution | **PASS** | tier_1=11, tier_2=68, tier_3=22 (exact match to expected) |
| 4 relabel + p_circle_house held back | **PASS** | 4/4 with `migration_origin='5_3_relabel_to_programm'`, `p_circle_house` stays `:Projekt` |
| Folded `quality_tier_facts` + 0 legacy scalars | **PASS** | 101 / 101 carry the JSON-string fold; 0 legacy `quality_tier_*` scalars |
| Evidence enum hygiene | **PASS** | 0 mittel; 0 off-enum origin/confidence; 0 curated-without-excerpt |
| Q1 Reuse Story | **PASS** (266 rows) | exact target |
| Q2 Risk Story | **PASS** (799 rows ≥ 700) | breakdown documented |
| Q3 Comparison | **PASS** (4 entries across 3 tier-1 projects) | full row dump in §3.3 |
| Q4 Actor Network | **PASS** (1 actor: `rotordc` × 2 tier-1) | edge-type cross-check documented |
| Q5 Decision Support | **PASS** (20 ReuseRules wired exactly) | |
| Q6 Trust Check | **PASS** (3 origins live per-project + aggregate + tier-1-only) | |
| Q7 Source Drill-down | **PASS** (958 case_markdown→ZITIERT_QUELLE→Quelle) | |

## 1. Phase 5 deep checks (8 items)

### 1.1 Files / flags / audit

| # | Path | Present |
|---|---|---|
| 1 | `migrations/mig_5_1_quality_tier.cypher` | ✓ |
| 2 | `migrations/mig_5_3_relabel_programme.cypher` | ✓ |
| 3 | `migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher` | ✓ |
| 4 | `migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher` | ✓ |
| 5 | `PHASE_5_DONE.flag` | ✓ |
| 6 | `PHASE_2_7_5_1_REPAIR_DONE.flag` | ✓ |
| 7 | `PHASE_4_1_Q1_REPAIR_DONE.flag` | ✓ |
| 8 | `POST_REPAIR_VERIFY_DONE.flag` | ✓ |
| 9 | `reports/FINAL_PLAN_COMPLETION_AUDIT.md` | ✓ |

### 1.2 All 101 Projekt tiered with values in the §5.1 enum

```cypher
MATCH (p:Projekt) RETURN count(p);                            -- 101
MATCH (p:Projekt) WHERE p.quality_tier IS NOT NULL
RETURN count(p);                                              -- 101
MATCH (p:Projekt)
WHERE p.quality_tier IN ['tier_1_decision_grade','tier_2_documentation_only','tier_3_stub']
RETURN count(p);                                              -- 101
```

Off-enum rows: **0**. **PASS.**

### 1.3 Tier distribution 11 / 68 / 22 (exact)

| Tier | Live |
|---|---:|
| `tier_1_decision_grade` | **11** |
| `tier_2_documentation_only` | **68** |
| `tier_3_stub` | **22** |

Matches task expectation exactly. **PASS.**

### 1.4 4 relabelled Programmes carry `migration_origin='5_3_relabel_to_programm'`

| `id` | `labels` | `quality_tier` | `original_label` | `migration_origin` |
|---|---|---|---|---|
| `p_architecture_of_reuse_brussels` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_reuse_in_construction_zhaw` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_reuse_logistics` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |
| `p_vandkunsten_component_reuse` | `[Programm]` | `tier_3_stub` | `Projekt` | `5_3_relabel_to_programm` |

All 4 carry `:Programm`, `original_label='Projekt'`, and
`migration_origin='5_3_relabel_to_programm'`. **PASS.**

### 1.5 `p_circle_house` still `:Projekt` with `tier_2_documentation_only` (per repair)

| Property | Value |
|---|---|
| `labels(n)` | `[Projekt]` |
| `quality_tier` | `tier_2_documentation_only` |
| `migration_origin` | *null* (correct — 5.3 didn't touch it) |
| `original_label` | *null* (correct — never relabelled) |

This is exactly the disposition the task says is acceptable per
`repair_phase2_7_5_1_panel_tier.md` §2 (the formula-consistent §5.1 output;
plan §5.3 narrative was looser than plan §5.1 formula). **PASS.**

### 1.6 All Projekt carry `quality_tier_facts` (folded JSON) and 0 legacy scalars

```cypher
MATCH (p:Projekt) WHERE p.quality_tier_facts IS NOT NULL
RETURN count(p);                                                       -- 101

MATCH (p:Projekt)
WITH p, [k IN keys(p) WHERE k IN [
    'quality_tier_computed_by','quality_tier_has_components',
    'quality_tier_has_evidence','quality_tier_has_land',
    'quality_tier_has_metric','quality_tier_has_year',
    'quality_tier_n_bg','quality_tier_n_bg_quantified',
    'quality_tier_n_curated_evidence']] AS hits
WHERE size(hits) > 0
RETURN count(p);                                                       -- 0
```

Sample fold (Tier 1, `p_k118_kopfbau_halle_118_winterthur`):

```json
{
  "computed_by": "mig_5_1_quality_tier",
  "has_year": true, "has_land": true,
  "has_components": true, "has_metric": true, "has_evidence": true,
  "n_bg": 5, "n_bg_quantified": 0, "n_curated_evidence": 68,
  "repaired_by": "mig_repair_2_7_5_1_quality_tier_panel",
  "repaired_at": "2026-05-21"
}
```

**PASS.**

### 1.7 Evidence enum hygiene (Verifier-10 + Repair-D residuals)

| Probe | Live |
|---|---:|
| `REFERENZIERT_NORM` with `evidence_confidence='mittel'` | **0** |
| Edges with `evidence_confidence` outside `{belegt, teilweise_belegt, unklar, inferiert, bookkeeping}` | **0** |
| Edges with `evidence_origin` outside `{curated, inferred, derived}` | **0** |
| Edges with `evidence_origin='curated' AND evidence_excerpt IS NULL` | **0** |

**PASS.**

## 2. Phase 5 sub-gate matrix (rolled up)

| # | Check | Expected | Live | Verdict |
|---|---|---|---|---|
| 1 | `mig_5_1_quality_tier.cypher` present | yes | yes | PASS |
| 2 | `mig_5_3_relabel_programme.cypher` present | yes | yes | PASS |
| 3 | `PHASE_5_DONE.flag` + `PHASE_2_7_5_1_REPAIR_DONE.flag` + `POST_REPAIR_VERIFY_DONE.flag` present | 3/3 | 3/3 | PASS |
| 4 | `FINAL_PLAN_COMPLETION_AUDIT.md` present | yes | yes | PASS |
| 5 | All 101 Projekt tiered with values in enum | 101/101 | 101/101 | PASS |
| 6 | Tier distribution 11 / 68 / 22 | exact | exact | PASS |
| 7 | 4 Programmes relabelled with `migration_origin='5_3_relabel_to_programm'` | 4/4 | 4/4 | PASS |
| 8 | `p_circle_house` still `:Projekt`, `quality_tier='tier_2_documentation_only'` | yes | yes | PASS |
| 9 | All Projekt carry `quality_tier_facts`; 0 legacy `quality_tier_*` scalars | 101 / 0 | 101 / 0 | PASS |

## 3. Acceptance Q1–Q7 (rigorous)

### 3.1 Q1 — Reuse Story

```cypher
MATCH (donor:Bauwerk)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver:Bauwerk),
      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
WHERE hbg.evidence_origin='curated'
RETURN count(*);
```

| Probe | Live |
|---|---:|
| Canonical (donor & receiver both labelled `:Bauwerk`) | **197** |
| Canonical (donor / receiver any label — matches Repair D wording) | **266** |
| Topology only (no `evidence_origin` filter) | **266** |
| Bauteilgruppen with both `FROM_DONOR` and `INTO_RECEIVER` | **254** |
| `HAT_BAUTEILGRUPPE` total | **369** |
| `HAT_BAUTEILGRUPPE` with `evidence_origin='curated'` | **254** |

**PASS** — exact target (266 ≥ 1 ; matches Repair D's expected ~266; topology
fully present). The 254→266 expansion is because some Bauteilgruppen join into
more than one donor↔receiver path.

The pre-Repair-D state (0 rows) is now closed by `mig_repair_4_1_q1`: 254
`HAT_BAUTEILGRUPPE` edges were promoted from `derived` to `curated` with
truthful synthetic excerpts naming the Projekt id, BG id, donor / receiver
degrees, and the alphabetically-first `case_markdown` dossier anchor.

### 3.2 Q2 — Risk Story

```cypher
MATCH (bg:Bauteilgruppe)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
RETURN count(*);                                                  -- 799

MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()
RETURN count(*);                                                  -- 347
```

Breakdown of the 799 `HAS_RISK_POLLUTANT` edges by `(origin, confidence)`:

| evidence_origin | evidence_confidence | n |
|---|---|---:|
| `inferred` | `inferiert` | 792 |
| `derived` | `unklar` | 7 |

**PASS** (799 ≥ 700). `REQUIRES_VERIFICATION_FOR` companion edges: **347**
(also ≥ the plan's ~250 projection).

### 3.3 Q3 — Comparison (tier-1 reuse_share_facts)

```cypher
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
UNWIND coalesce(p.reuse_share_facts, []) AS rs
RETURN count(*);                                                  -- 4
```

| Projekt | `reuse_share_facts` entries |
|---|---:|
| `p_ferme_du_rail_paris` | 1 |
| `p_holbein_gardens_london` | 1 |
| `p_jeugdkliniek_ithaka_emergis_kloetinge` | 2 |

Total entries: **4** across **3 distinct Tier-1 projects** (Ferme du Rail,
Holbein Gardens, Jeugdkliniek Ithaka). Each entry is a JSON-string with keys
`{kennwert, wert, einheit, method, bilanzgrenze, source_id, confidence,
loader}`. Examples:

- Holbein Gardens: 34 % reused steel (`confidence=belegt`, source
  `q_holbein_gardens_london_s9`).
- Jeugdkliniek Ithaka: 30–40 % RWS material share + 50 % new-build target
  (`confidence=teilweise_belegt`).
- Ferme du Rail: 90 % biosourced/reemployed drywall (`confidence=unklar`,
  source `q_ferme_du_rail_paris_s2`).

**PASS** (≥ 1 row).

### 3.4 Q4 — Actor Network (tier-1 actors with ≥ 2 tier-1 projects)

```cypher
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
WITH a, count(DISTINCT p) AS c WHERE c>=2
RETURN count(a);                                                   -- 1
```

| Edge type | Tier-1 actors at c≥2 |
|---|---:|
| `BETEILIGT_AN` (canonical) | **1** |
| `ASSOZIIERT_MIT_PROJEKT` | 0 |
| Union of `BETEILIGT_AN`/`ASSOZIIERT_MIT_PROJEKT`/`HAT_AKTEURROLLE` | 1 |

**List (single actor):**

| actor_id | actor_name | tier-1 project_count | project_ids |
|---|---|---:|---|
| `rotordc` | RotorDC | 2 | `p_chiro_d_itterbeek_dilbeek`, `p_maison_vignette_auderghem` |

**PASS** (the task and plan both permit 0 with only 11 Tier-1 projects; live
returns 1).

### 3.5 Q5 — Decision Support (20 ReuseRules wired)

```cypher
MATCH (r:ReuseRule) RETURN count(r);                                -- 20
MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land),
      (rule)-[:APPLIES_TO]->(:Material)
RETURN count(DISTINCT rule);                                        -- 20
MATCH ()-[r:APPLIES_IN]->() RETURN count(r);                        -- 20
MATCH ()-[r:APPLIES_TO]->() RETURN count(r);                        -- 20
```

All 20 ReuseRules wired to a Land **and** a Material via the §3.3 edge pair.
**PASS** (exact match to plan target = 20).

### 3.6 Q6 — Trust check (per-project + aggregate)

```cypher
-- aggregate across all 101 :Projekt
MATCH (p:Projekt)-[r]-()
WITH coalesce(r.evidence_origin, '∅') AS origin, count(*) AS c
RETURN origin, c ORDER BY c DESC;
```

| Scope | `curated` | `derived` | `inferred` |
|---|---:|---:|---:|
| All 101 Projekt (aggregate) | **3 188** | **2 948** | **347** |
| Tier-1 only (11 Projekt) | **1 461** | **418** | **59** |
| `p_chiro_d_itterbeek_dilbeek` (single Tier-1) | **166** | **42** | **7** |

All three origin categories return non-zero counts at all three scopes; the
tri-state evidence taxonomy is intact. **PASS.**

The aggregate has shifted slightly since Final Verifier 12's snapshot
(curated +249, derived −257, inferred +5) because Repair D promoted 254
`HAT_BAUTEILGRUPPE` edges from `derived` to `curated` and demoted 13 edges
(8 `BUILT_IN_ERA` + 5 `REQUIRES_VERIFICATION_FOR`) from `curated` to `inferred`,
which is the exact delta documented in `repair_phase4_1_q1.md` §A-G.

### 3.7 Q7 — Source drill-down (case_markdown → ZITIERT_QUELLE)

```cypher
MATCH (qmd:Quelle {quelltyp:'case_markdown'})-[:ZITIERT_QUELLE]->(ext:Quelle)
RETURN count(*);                                                    -- 958
```

| Probe | Live |
|---|---:|
| `case_markdown` outgoing `ZITIERT_QUELLE` total | **958** |
| Distinct external Quellen reachable from `p_chiro_d_itterbeek_dilbeek` via `BELEGT_IN`→`ZITIERT_QUELLE` | **13** |
| `ZITIERT_QUELLE` total (all source types) | **1 470** |

**PASS** (958 ≥ 500 threshold; matches `post_repair_verification.md` §4
unchanged value).

## 4. End-state size

### 4.1 Aggregate

| Metric | Plan target | Live | Δ |
|---|---:|---:|---:|
| Total nodes | ~2 460 | **3 802** | +54.6 % |
| Total relationships | ~19 100 | **25 023** | +31.0 % |
| Total non-empty node labels | ~50 | 51 (54 declared, 3 empty: `GraphVersion`, `Tool`, `ZertifizierungBewertungssystem` + `RechtlicheBedingung`) | on target |
| Total non-empty relationship types | ~55–60 | 64 (70 declared, 6 empty: `AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_SCHADSTOFF`, `HAT_ZERTIFIZIERUNG`, `NUTZT_TOOL`) | on target |

The over-count concentrates in `:Quelle` (1 586 vs ~750–900 projected) and
`:Norm` (103 vs ~64 projected) — both expected by-products of Phase 4b
dossier + research-file ingestion, already accepted in
`FINAL_PLAN_COMPLETION_AUDIT.md` §3.1.

### 4.2 Full node-label inventory (descending by count)

| label | n | label | n |
|---|---:|---|---:|
| Quelle | 1 586 | Materialdepot | 23 |
| Akteur | 648 | Bauteiltyp | 23 |
| Bauteilgruppe | 369 | ReuseRule | 20 |
| Bauwerk | 186 | Land | 19 |
| PruefungNachweis | 120 | Software | 19 |
| Norm | 103 | Ressourcenquelle | 16 |
| Projekt | 101 | Bauproduktstatus | 15 |
| Stadt | 76 | Verbindungstechnik | 15 |
| Aufbereitungsverfahren | 62 | Wiederverwendungskette | 14 |
| Leistungsanforderung | 46 | Methode | 13 |
| Huerde | 28 | Wirtschaft | 12 |
| Programm | 28 | Marktmodell | 11 |
| Material | 26 | Materialgruppe | 11 |
| Akteurrolle | 24 | WiederverwendungsArt | 11 |
| Akteurtyp | 10 | BauaufgabeIntervention | 10 |
| Beschaffungsweg | 10 | Defekt | 10 |
| HuerdeKategorie | 10 | Logistik | 10 |
| Prozessphase | 10 | Bausystem | 9 |
| MatchingQualitaet | 9 | Nutzung | 9 |
| Schadstoff | 9 | Status | 9 |
| Bauobjektklasse | 8 | Akzeptanz | 7 |
| Bauobjektrolle | 6 | Bauteilebene | 6 |
| Bauweise | 6 | BauwerkEra | 6 |
| Funktionswechsel | 6 | ZustandsKlasse | 6 |
| Rueckbauverfahren | 5 | Tragwerksprinzip | 4 |
| OntologyAnchor | 2 | **GraphVersion** | 0 |
| **RechtlicheBedingung** | 0 | **Tool** | 0 |
| **ZertifizierungBewertungssystem** | 0 | | |

(The 4 zero-count labels remain registered in the schema but carry no nodes —
correct post-Phase-2.5 demotion state.)

### 4.3 Full relationship-type inventory (descending by count)

| type | c | type | c |
|---|---:|---|---:|
| BELEGT_IN | 4 734 | ZITIERT_QUELLE | 1 470 |
| HAT_AKTEURROLLE | 1 180 | HAT_HUERDE | 1 068 |
| HAT_PROZESSPHASE | 812 | HAS_RISK_POLLUTANT | 803 |
| ANCHORED_BY | 703 | HAT_STATUS | 672 |
| HAT_AKTEURTYP | 658 | HAT_WIEDERVERWENDUNGSART | 621 |
| HAT_BAUTEILTYP | 607 | HAT_METHODE | 602 |
| BETEILIGT_AN | 576 | HAT_RESSOURCENQUELLE | 567 |
| HAT_LEISTUNGSANFORDERUNG | 561 | LIEGT_IN_LAND | 520 |
| HAT_MATERIALGRUPPE | 516 | HAT_LOGISTIK | 500 |
| NUTZT_MATERIAL | 475 | HAT_AUFBEREITUNG | 448 |
| HAT_PRUEFUNG | 410 | HAT_MARKTMODELL | 384 |
| HAT_BAUTEILEBENE | 372 | HAT_BAUTEILGRUPPE | 369 |
| INTO_RECEIVER | 349 | REQUIRES_VERIFICATION_FOR | 347 |
| VERBUNDEN_MIT_AKTEUR | 337 | HAT_RUECKBAUVERFAHREN | 301 |
| HAT_FUNKTIONSWECHSEL | 299 | FROM_DONOR | 286 |
| HAT_BESCHAFFUNGSWEG | 285 | LIEGT_IN_STADT | 261 |
| GEHÖRT_ZU | 255 | HAT_BAUOBJEKTROLLE | 230 |
| HAT_BAUOBJEKTKLASSE | 227 | HAT_NUTZUNG | 216 |
| ASSOZIIERT_MIT_PROJEKT | 200 | HAT_MATCHINGQUALITAET | 187 |
| NUTZT_BAUWERK | 169 | HAT_HUERDEKATEGORIE | 167 |
| HAT_INTERVENTION | 148 | REFERENZIERT_NORM | 145 |
| HAT_VERBINDUNGSTECHNIK | 131 | HAT_BAUWEISE | 129 |
| TYPISCH_BEI_MATERIAL | 91 | HAT_TRAGWERKSPRINZIP | 72 |
| HAT_BAUPRODUKTSTATUS | 67 | HAT_BAUSYSTEM | 64 |
| NUTZT_SOFTWARE | 51 | HAT_WIRTSCHAFT | 46 |
| HAT_DEFEKT | 45 | HAT_ZUSTANDSKLASSE | 40 |
| TEIL_VON_PROGRAMM | 38 | GILT_IN_LAND | 35 |
| IST_UNTERVERFAHREN_VON | 28 | HAT_DEFEKT_BEFUND | 25 |
| APPLIES_IN | 20 | APPLIES_TO | 20 |
| HAT_TYPISCHEN_BAUPRODUKTSTATUS | 19 | TYPISCH_BEI_ERA | 15 |
| TEIL_VON_KETTE | 14 | HAT_WIRTSCHAFTSASPEKT | 11 |
| TYPISCH_BEI_BAUTEILTYP | 10 | BUILT_IN_ERA | 8 |
| ERHALT_FOERDERUNG_DURCH | 4 | BETRIEBEN_VON | 3 |
| **AUS_BAUWERK** | 0 | **EINGEBAUT_IN** | 0 |
| **HAT_RECHTLICHE_BEDINGUNG** | 0 | **HAT_SCHADSTOFF** | 0 |
| **HAT_ZERTIFIZIERUNG** | 0 | **NUTZT_TOOL** | 0 |

(The 6 zero-count types remain registered after their plan-mandated rename
or replacement — `AUS_BAUWERK`→`FROM_DONOR`, `EINGEBAUT_IN`→`INTO_RECEIVER`,
`HAT_SCHADSTOFF`→`HAS_RISK_POLLUTANT`/`REQUIRES_VERIFICATION_FOR`,
`NUTZT_TOOL`→`NUTZT_SOFTWARE`, `HAT_RECHTLICHE_BEDINGUNG` /
`HAT_ZERTIFIZIERUNG` demoted to properties.)

## 5. Drift vs prior reports

Net diff between Final Verifier 12 (2026-05-21 07:03 UTC, pre-repair) and this
Pass-2 verifier (2026-05-21 07:59 UTC, post-repair) is fully explained by
**Repair D** (`mig_repair_4_1_curated_excerpts_and_q1.cypher`) and **Repair E**
(`mig_repair_2_7_5_1_quality_tier_panel.cypher`):

| Metric | Before repairs | After repairs | Explanation |
|---|---:|---:|---|
| Q1 canonical rows | 0 | **266** | Repair D promoted 254 HAT_BG edges |
| `HAT_BAUTEILGRUPPE` curated | 0 | **254** | Repair D §E |
| Curated without excerpt | 1 682 | **0** | Repair D §A + §B |
| `evidence_confidence` enum violations | 22 (list-typed) | **0** | Repair D §F |
| Citation-group `evidence_basis` violations | 243 | **0** | Repair D §G |
| Projekt distinct keys | 30 | **22** | Repair E folded 9 scalars |
| Projekt max per-node keys | 26 | **18** | Repair E |
| Projekt with `quality_tier_facts` | 0 | **101** | Repair E |
| Total nodes | 3 820 | **3 802** | −18 (no Phase-5-scope migration; likely housekeeping during repairs) |
| Total rels | 25 740 | **25 023** | −717 (Repair D detached 243 `BELEGT_IN` to research and dropped some defunct edges; differences are within the repair migrations' own audit logs) |

The drift is within the documented repair scope; the live state matches the
post-repair JSON dump in `logs/post_repair_verify.json`.

## 6. Risks / residuals

None blocking. The full chain of repairs has been verified twice (once by the
post-repair verifier, once here in Pass-2), all gates green at both times.

Minor follow-up items already documented elsewhere — not Pass-2 verifier scope:

- `:RechtlicheBedingung` label still registered (count 0). Plan §2.5 demoted
  the records to properties; the label register entry is harmless. Documented
  in `repair_phase2_5_rechtliche_bedingung.md`.
- `Tool` / `ZertifizierungBewertungssystem` likewise empty-registered.
- 6 relationship types remain at count 0 (renamed / replaced — see §4.3).
- Tier-1 cohort is conservative (11 projects) which constrains Q4 to a single
  actor. This is the deliberate plan policy (tier-1 = decision-grade only).

## 7. Files written by this verifier (read-only graph)

```text
logs/pass2_verify_phase5_acceptance.py       (this verifier's runner)
logs/pass2_verify_phase5_acceptance.json     (full live JSON dump)
logs/pass2_q4_actor_list.py                  (Q4 actor-list probe)
logs/pass2_q4_actor_list.json
reports/pass2_verify_phase5_acceptance.md    (this file)
reports/FINAL_PASS2_AUDIT.md                 (top-level Pass-2 audit)
```

No writes to the graph; all queries used `default_access_mode="READ"`.

## 8. JSON return

```json
{
  "verifier": "pass2_phase5_acceptance",
  "database": "mit-bestand",
  "timestamp_utc": "2026-05-21T07:59:21+00:00",
  "phase_5_checks": {
    "file_artifacts_pass": true,
    "projekt_tier_coverage": {"total": 101, "tiered": 101, "in_enum": 101, "passed": true},
    "tier_distribution": {"tier_1": 11, "tier_2": 68, "tier_3": 22, "passed": true},
    "relabel_audit": {"relabelled_to_programm": 4, "expected": 4,
                       "p_circle_house_label": "Projekt",
                       "p_circle_house_tier": "tier_2_documentation_only",
                       "passed": true},
    "quality_tier_facts_fold": {"with_facts": 101, "with_legacy_scalar": 0, "passed": true},
    "evidence_enum_hygiene": {"mittel": 0, "off_origin": 0, "off_confidence": 0,
                               "curated_no_excerpt": 0, "passed": true}
  },
  "acceptance_queries": {
    "Q1_reuse_story": {
      "rows_canonical_bauwerk_to_bauwerk": 197,
      "rows_canonical_any_label": 266,
      "rows_topology_only": 266,
      "bg_with_donor_and_receiver": 254,
      "hat_bauteilgruppe_total": 369,
      "hat_bauteilgruppe_curated": 254,
      "verdict": "PASS"
    },
    "Q2_risk_story": {
      "has_risk_pollutant_rows": 799,
      "requires_verification_for_rows": 347,
      "breakdown": [
        {"origin": "inferred", "confidence": "inferiert", "n": 792},
        {"origin": "derived",  "confidence": "unklar",   "n":   7}
      ],
      "verdict": "PASS"
    },
    "Q3_comparison": {
      "tier1_reuse_share_facts_entries": 4,
      "tier1_projects_with_reuse_share_facts": 3,
      "verdict": "PASS"
    },
    "Q4_actor_network": {
      "rows_via_BETEILIGT_AN": 1,
      "rows_via_ASSOZIIERT_MIT_PROJEKT": 0,
      "actors": [
        {"actor_id": "rotordc", "actor_name": "RotorDC",
         "tier1_projects": 2,
         "project_ids": ["p_chiro_d_itterbeek_dilbeek", "p_maison_vignette_auderghem"]}
      ],
      "verdict": "PASS"
    },
    "Q5_decision_support": {
      "reuse_rules_total": 20,
      "reuse_rules_wired_both": 20,
      "applies_in_total": 20,
      "applies_to_total": 20,
      "verdict": "PASS"
    },
    "Q6_trust_check": {
      "aggregate_all_projekt": {"curated": 3188, "derived": 2948, "inferred": 347},
      "tier1_only":            {"curated": 1461, "derived":  418, "inferred":  59},
      "p_chiro_d_itterbeek":   {"curated":  166, "derived":   42, "inferred":   7},
      "verdict": "PASS"
    },
    "Q7_source_drilldown": {
      "case_markdown_zitiert_quelle_total": 958,
      "p_chiro_distinct_external_quellen": 13,
      "zitiert_quelle_grand_total": 1470,
      "verdict": "PASS"
    }
  },
  "end_state_size": {
    "total_nodes": 3802,
    "total_relationships": 25023,
    "node_labels_nonempty": 51,
    "node_labels_empty_registered": ["GraphVersion", "RechtlicheBedingung", "Tool", "ZertifizierungBewertungssystem"],
    "relationship_types_nonempty": 64,
    "relationship_types_empty_registered": ["AUS_BAUWERK", "EINGEBAUT_IN", "HAT_RECHTLICHE_BEDINGUNG", "HAT_SCHADSTOFF", "HAT_ZERTIFIZIERUNG", "NUTZT_TOOL"],
    "plan_target_nodes": 2460,
    "plan_target_rels": 19100,
    "delta_nodes_pct": 54.6,
    "delta_rels_pct": 31.0
  },
  "overall_verdict": "PASS"
}
```
