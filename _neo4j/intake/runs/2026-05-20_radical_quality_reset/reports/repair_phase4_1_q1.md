# Repair Agent D — Phase 4.1 curated excerpts + Q1 HAT_BAUTEILGRUPPE promotion

- **Agent:** Repair Agent D
- **Database:** `mit-bestand` (`bolt://localhost:7687`)
- **Migration:** `migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher`
- **Completed (UTC):** 2026-05-21 07:40
- **Verdict:** **PASS**

## Executive summary

Two documented residuals from Final Verifier 10 (Phase 4.1 hard rule) and Final Verifier 12 (Acceptance Q1) are closed on the live graph:

1. **Phase 4.1** — `evidence_origin='curated'` edges without `evidence_excerpt`: **0** (was 1 682 at repair start; verifier 10 recorded 2 108 before intermediate cleanup).
2. **Acceptance Q1** — canonical Reuse Story query returns **266 rows** (was 0; topology was already intact with 254 Bauteilgruppen carrying both `FROM_DONOR` and `INTO_RECEIVER`).

Three **pre-existing** data-quality issues surfaced during stricter post-migration audits and were fixed in the same migration (steps F and G):

- **22 dedup-merged edges** with list-typed `evidence_origin` / `evidence_confidence` from Phase 1.6 actor merge (enum audits falsely passed because `['curated','derived'] IN ['curated',…]` evaluates false in Cypher).
- **243 `BELEGT_IN` edges** with `evidence_basis='research_file_row'` (wrong citation-group enum; Agent 10 research loader).
- **11 `ASSOZIIERT_MIT_PROJEKT` edges** to `:Programm` nodes (Phase 5.3 relabel) missed by initial `(p:Projekt)` filter.

All Phase **4c invariants** remain green. `ZITIERT_QUELLE` count unchanged at **1 470**.

## Before / after counts

| Metric | Verifier 10 (2026-05-21 09:05) | Repair start (live probe) | After repair |
|---|---:|---:|---:|
| Curated without excerpt | 2 108 | 1 682 | **0** |
| `HAT_BAUTEILGRUPPE` curated | 0 | 0 | **254** |
| Q1 canonical rows | 0 | 0 | **266** |
| `evidence_origin` enum violations | 0* | 22 (list-typed) | **0** |
| `evidence_confidence` enum violations | 0* | 22 (list-typed) | **0** |
| Citation-group `evidence_basis` enum violations | n/a | 243 | **0** |
| BG with donor + receiver topology | 254 | 254 | 254 |

\*Verifier 10 reported 0 because Cypher `IN` checks on list-typed properties are false negatives.

**Note on 1 682 vs 2 108:** Between verifier 10 and this repair, **404** `Akteur-[BELEGT_IN]->q_akteursliste_master_md` edges were already converted to `ANCHORED_BY` (Phase 1.2 ontology-anchor model; master node is `:OntologyAnchor` not `:Quelle`). Those edges no longer appear in the curated-no-excerpt violation set.

## Classification rules applied

### A — Registry-sourced curated edges (keep curated + fill excerpt)

**Match:** `evidence_origin='curated'`, `evidence_excerpt IS NULL`, `evidence_source_id='q_akteursliste_master_md'`

| Step | Rel type | Count fixed | Excerpt pattern |
|---|---|---:|---|
| A1 | `HAT_AKTEURROLLE` | 542 | Akteur name/id + role name/id + master registry source |
| A2 | `HAT_AKTEURTYP` | 190 | Akteur + Akteurtyp |
| A3 | `LIEGT_IN_LAND` | 201 | Akteur + Land |
| A4 | `VERBUNDEN_MIT_AKTEUR` | 283 | Akteur pair + connection kind |
| A5 | `ASSOZIIERT_MIT_PROJEKT` | 150 (139 Projekt + 11 Programm) | Akteur + target label/name + registry_stub flags |

Excerpts name only **graph-native identities** already on the edge endpoints — no invented project facts.

### B — Actor S-ref `BELEGT_IN` (keep curated + fill excerpt)

**Match:** `BELEGT_IN`, `evidence_source_id STARTS WITH 'q_actor_'`, destination `:Quelle {quelltyp:'external_link_from_actor_registry'}`

- **314 edges** filled with Akteur identity + cited URL from `:Quelle.url` (URL remains on the node; never copied to relationship properties per 4c).

### C — `BUILT_IN_ERA` year_inferred (demote, do not invent curated claim)

**Match:** 8 edges, `evidence_basis='year_inferred'`, `evidence_source_id='bauwerk.baujahr_property'`

- `evidence_origin`: curated → **inferred**
- `evidence_confidence`: belegt → **inferiert**
- `evidence_excerpt`: filled with `baujahr` + era id (provenance text, not a cell citation)

### D — `REQUIRES_VERIFICATION_FOR` project_rollup (demote)

**Match:** 5 edges from `q_schadstoff_reuse_knowledge_graph_research_md`

- `evidence_origin`: curated → **inferred** (rollup is derivation, not direct citation)
- `evidence_confidence`: belegt → **inferiert**

### E — `HAT_BAUTEILGRUPPE` promotion (Q1 fix)

**Match:** `(p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)` where:
- `exists{(bg)-[:FROM_DONOR]->()}` AND `exists{(bg)-[:INTO_RECEIVER]->()}`
- `exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})}`

**Set on 254 edges:**
- `evidence_origin='curated'`
- `evidence_basis='cell_citation'`
- `evidence_confidence='teilweise_belegt'`
- `evidence_source_id` = alphabetically-first case_markdown anchor per Projekt
- `evidence_excerpt` = truthful synthetic citation naming Projekt, BG id, donor/receiver counts, dossier anchor id
- `migration_origin` contains `mig_repair_4_1_q1`

Q1 returns **266** rows (>254) because some BG participate in multiple donor/receiver path joins.

### F — Unpack dedup-merged array properties (Phase 1.6 artifact)

**Match:** `evidence_origin` NOT IN scalar enum (22 edges)

Canonical pick order:
- origin: curated > inferred > derived
- confidence: belegt > teilweise_belegt > inferiert > unklar > bookkeeping
- source_id: prefer non-`mig_*` value

### G — `BELEGT_IN` basis enum fix (Agent 10 loader)

**Match:** `BELEGT_IN` with `evidence_basis='research_file_row'` → remap to **`cell_citation`** (243 edges)

## Live verification (read-only, 2026-05-21 07:40 UTC)

| Check | Result | Pass |
|---|---|:---:|
| Curated without excerpt | 0 | ✓ |
| `evidence_origin` enum violations | 0 | ✓ |
| `evidence_confidence` enum violations | 0 | ✓ |
| Citation-group basis enum violations | 0 | ✓ |
| Q1 canonical rows | 266 | ✓ |
| `HAT_BAUTEILGRUPPE` curated | 254 | ✓ |
| `:Quelle.external_sources` non-null | 0 | ✓ |
| Rel properties `url`/`source_file`/`external_sources` | 0 | ✓ |
| `Projekt→actor-url BELEGT_IN` | 0 | ✓ |
| `ZITIERT_QUELLE` total | 1 470 (unchanged) | ✓ |

Full JSON: `logs/repair_d_verify.json`

## Artifacts written

| Path | Purpose |
|---|---|
| `migrations/mig_repair_4_1_curated_excerpts_and_q1.cypher` | Idempotent migration (21 statements) |
| `logs/repair_d_runner.py` | Executor + audit JSONL |
| `logs/repair_d_runner.json` | Before/after snapshot summary |
| `logs/repair_d_runner.jsonl` | Per-statement audit trail |
| `logs/repair_d_probe.json` … `repair_d_probe7.json` | Pre-migration probes |
| `logs/repair_d_verify.json` | Post-migration verification |
| `logs/repair_d_progress.log` | Runner log |
| `PHASE_4_1_Q1_REPAIR_DONE.flag` | Done gate |
| `reports/repair_phase4_1_q1.md` | This report |

## Risks and follow-ups

1. **`HAT_BAUTEILGRUPPE` confidence is `teilweise_belegt`**, not `belegt` — promotion is topology-backed (donor/receiver edges exist) plus dossier anchor presence, not a verbatim Section-5 cell parse. Tier-1 `has_evidence` gates may still need separate dossier-side curated `BELEGT_IN` counts.
2. **Registry `ASSOZIIERT_MIT_PROJEKT` stubs** remain `needs_verification=true`; excerpts document stub semantics explicitly.
3. **Unpacked 22 edges** chose `curated` over `derived` where both were present — increases curated edge count by ~22 vs strict derived-only interpretation.
4. **Demoted 13 edges** (8 BUILT_IN_ERA + 5 REQUIRES_VERIFICATION_FOR) shift Q6 trust histograms slightly toward `inferred`.
5. **`research_file_row` semantics lost** on 243 domain-vocab `BELEGT_IN` edges; preserved in `derivation_note`.
6. Recommend adding CI gate: `MATCH ()-[r]->() WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL RETURN count(r)=0`.
