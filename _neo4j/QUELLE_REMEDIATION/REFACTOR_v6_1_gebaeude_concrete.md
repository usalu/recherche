# Q-EXT v6.1 — gebäude-only refactor, with concrete extraction numbers

**Date:** 2026-05-22 · **Author:** orchestrator
**Trigger:** user instruction (verbatim): *"unfold retrace test on cocrete and refractor the plan accordingly. BE CONCRETE AND SEARCH THE REPO FOR ANY EVIDENCE: IGONRE ANYTHIGN ELSE IN ARCHIEVE BESIDE gebäude"*

> **TL;DR.** v6 covered four input-file families. The user has narrowed scope to **only `_archive/research/gebaeude/*.md`** — bauteilbörse, registry, and research files are out of scope for this wave. I built and ran a concrete unfolder against all 76 gebäude dossiers. It produces **6,150 (node, dossier, locator, URL) triples** with 388 distinct URLs and 2,587 distinct (entity_type, value) targets. 71/76 dossiers parse cleanly; 5 fail because of dossier-internal abbreviations (e.g. `CMS → Circular Material Systems`) that need a per-dossier alias table.

This document **supersedes §1.1, §1.2, §1.3, §1.4 of [REFACTOR_v6_decision.md](REFACTOR_v6_decision.md)** with proof. v6.C (kill `:ZITIERT_QUELLE`) is unchanged.

---

## §1 What the test actually does (and runs)

Files:
- Test driver: [test_gebaeude_unfolder.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/test_gebaeude_unfolder.py)
- Full-scale runner: [unfold_all_gebaeude.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude.py)
- Full triple log (one JSON per line): [unfold_all_gebaeude_triples.jsonl](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude_triples.jsonl)
- Per-dossier summary: [unfold_all_gebaeude_summary.json](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude_summary.json)

Pipeline:
1. Read each `.md` in `_archive/research/gebaeude/` (76 files).
2. Split into H2 sections.
3. Parse the `## Quellen [und Links] / [/ Links]` master section into a name→URL map. Two styles are now supported (see §3).
4. Walk every table row in the **7 table-bearing sections** (§2 ENTITÄTEN-MAPPING, §5 BAUTEIL-INVENTAR, §6 PROZESS UND LOGISTIK, §7 TECHNIK, §8 KENNWERTE, §9 HÜRDEN-MATRIX, §10 WIRTSCHAFT — but §10 has no real Quelle column in any dossier so it contributes 0).
5. For each row, find the entity column + the Quelle column. Extract refs (S-refs OR named tokens). Resolve each ref to a URL via the master map. Emit one triple per (row, ref, URL).

Read-only. Does not touch the graph.

---

## §2 The numbers — concrete

```
GLOBAL SUMMARY — 76 gebäude dossiers
  Total triples extracted:        6,150
  Distinct URLs:                    388
  Distinct (entity_type, value):  2,587
  Dossiers with ZERO triples:         5   (6.6 %)
  Dossiers with ZERO Quellen:         4   (5.3 %)
  Rows skipped (no Quelle col):   1,587
  Rows skipped (unresolved ref):     15
```

Per-section breakdown of the 6,150 triples:

| Section | Triples | %  |
|---|---:|---:|
| 2. ENTITÄTEN-MAPPING       | 2,454 | 39.9 % |
| 6. PROZESS UND LOGISTIK    |   933 | 15.2 % |
| 5. BAUTEIL-INVENTAR        |   820 | 13.3 % |
| 8. KENNWERTE               |   815 | 13.3 % |
| 7. TECHNIK, LEISTUNG, NORMEN |  677 | 11.0 % |
| 9. HÜRDEN-MATRIX           |   451 |  7.3 % |
| 10. WIRTSCHAFT             |     0 |    0 % |

Top entity-type buckets from §2 (column 0 = entity type, column 1 = value):

```
prozessphase    933   (every §6 row)
bauteil         820   (every §5 row)
kennwert        815   (every §8 row)
thema           677   (every §7 row)
huerde          451   (every §9 row)
Bauteil         416   (§2 declared-Bauteil rows)
People          401   (§2 declared-People rows)
Kennwert        237
Fallstudie      180   (1 per dossier × 2-3 refs each)
Gebäude         151
Projekt         138
Ort             131
Material        105
Reuse-Strategie  98
Hürde            71
Methode          43
Logistik         42
Prüfung          41
Tragwerkssystem  39
Bauherr          38
```

This is the raw `:CITED_FROM_DOSSIER` edge volume that v6 Wave 2 must write for the gebäude subset. **6,150 edges**, **per-row locator** down to section + row index.

---

## §3 The two citation styles (and the parser change)

When I sampled 5 dossiers earlier, I found one citation style. Scaling to 76 surfaced a second one.

### §3.1 Style 1 — S-ref labelled (~46 dossiers)

```
## Quellen und Links
- [S1] Title. https://...                ← Holbein, Ferme du Rail
[S1] Title: https://...                  ← K118 (no leading dash)
- **S1 — Title:** https://...            ← Resource Rows, Villa Welpeloo
- **S1 – Title.** `https://...`          ← rare backticked variant
```

Tables reference: `S1, S2` (with or without brackets, comma- or slash-separated).

### §3.2 Style 2 — named-token list (~30 dossiers)

```
## Quellen / Links                ← (also 'Quellen', 'Quellen und Links')
1. ASBP — 55 Great Suffolk Street case study: https://asbp.org.uk/...
- CITYFÖRSTER – Recyclinghaus Hanover: https://www.cityfoerster.net/...
- Circular Material Systems – CRCLR / Impact Hub Berlin: https://...
```

Tables reference: `ASBP, NLA, Hawkins\Brown` — i.e. the org name appears in the cell, often abbreviated.

Parser keys: I index each Style-2 entry by (a) the literal head token, (b) the normalised head token (lowercase, punctuation-stripped), (c) the first whitespace-separated word, (d) its normalised form. Then in the table row I split the cell on `, ; / und |` and lookup each token against all four keys; if no exact match, I try a substring match (≥3-char prefix overlap on both sides).

### §3.3 The remaining 5 still-zero dossiers

| Dossier | Why zero |
|---|---|
| CRCLR_House_Impact_Hub_Berlin | Table uses `CMS` → Quellen has `Circular Material Systems`. No textual overlap. |
| ELYS_Kultur_Gewerbehaus_Basel | Quellen list missing? (4 entries detected, but tokens don't appear in tables.) |
| Europa_Building_Brussels | Same — dossier-internal abbreviation system |
| Institut_de_Botanique_ULg_Liege | Same |
| Thoravej_29_Copenhagen | Same |

**Decision:** v6.1.A.5 = an optional per-dossier `quellen_alias.yaml` overlay (~5 files). Anything not in the alias map stays unresolved (honest signal). The user reviews these 5 dossiers manually; the unfolder reads the YAML if present.

---

## §4 What v6.1 actually ships (gebäude-only scope)

Drops from original v6:
- ~~v6.A.2 `unfolder_bauteilboerse_file.py`~~ — out of scope
- ~~v6.A.3 `unfolder_registry.py`~~ — out of scope
- ~~v6.A.4 `unfolder_research.py`~~ — out of scope

Keeps (and concretises) from v6:
- **v6.A.1 — `unfolder_building_dossier.py`**: the parser tested above, promoted to runner. Reads all 76 `.md`, writes `:CITED_FROM_DOSSIER` edges (one per triple).
- **v6.C — `mig_qext_v6_c_kill_zitiert_quelle.cypher`**: unchanged. Drops `:ZITIERT_QUELLE`, renames `:Quelle:ExternalLink` → `:UrlMetadata`.
- **v6.B — `mig_qext_v6_b_unfolding_taxonomy.cypher`**: still sets `unfolding_kind` + `unfolding_origin` on every node + edge, but for **gebäude-touched nodes only** (filter on `n.dossier_id STARTS WITH 'q_'` and label in the gebäude entity set). Other nodes keep their legacy `evidence_origin` for now.
- **v6.D — `audit_full_tracing.py`**: per-label `fully_traced %` report restricted to the gebäude scope.

Adds:
- **v6.1.A.5 — `quellen_alias.yaml` overlay** (per-dossier, ≤5 files). Optional. Lets the user resolve abbreviations like `CMS → Circular Material Systems`.

---

## §5 The locator string — concrete format

Every emitted triple becomes a `:CITED_FROM_DOSSIER` edge with a `locator` property that pinpoints **the exact row in the exact section**:

```
locator: 'sec:5.BAUTEIL-INVENTAR/row:3/col:Bauteil:Stahlträger I-Profil'
```

Format (final): `sec:<sec_no>.<sec_slug>/row:<row_idx>/col:<entity_col_name>:<entity_value_trunc>`

For §2 ENTITÄTEN-MAPPING (where column-0 is the entity TYPE and column-1 is the value), use:

```
locator: 'sec:2.ENTITAETEN-MAPPING/row:7/typ:Material/val:Stahl'
```

This is enough to round-trip back to the dossier and visually confirm the citation. (Eyeballed on the sample triples in the JSONL log — works.)

---

## §6 What stays from v6 unchanged

§3.1, §3.2, §3.3, §3.4 (UrlMetadata side-lookup), §4 (unfolding taxonomy), §6 (mapping legacy evidence_origin), §7 (kill `:ZITIERT_QUELLE` migration), §8 (full tracing definition), §10 (open decisions), §12 (post-v6 user-facing view), §13 (long-term-plan adjustment), §14 (why v6 ends here), §15 (run order — minus the bauteilbörse/registry/research subcommands).

---

## §7 Updated run order (gebäude-only)

```bash
# Wave 1 — kill :ZITIERT_QUELLE  (unchanged from v6)
python qext_runner.py kill_zitiert_quelle

# Wave 2 — gebäude unfolding only
python qext_runner.py unfold_gebaeude_dossiers     # v6.1.A.1
python qext_runner.py taxonomy_gebaeude            # v6.B (gebäude-filtered)
python qext_runner.py audit_tracing_gebaeude       # v6.D (gebäude-filtered)
```

Other archives (bauteilbörse, registry, research) keep their current `evidence_origin` for this wave. A future v7 can extend the pattern if/when the user opens that scope.

---

## §8 Validation budget

After v6.1 runs end-to-end against `mit-bestand`, expect:

| Metric | Expected value | Source |
|---|---:|---|
| `:CITED_FROM_DOSSIER` edges with non-null `source_url` | **≥ 6,150** | §2 |
| Distinct URLs on such edges | **≥ 388** | §2 |
| `:ZITIERT_QUELLE` edges remaining | **0** | v6.C audit |
| `:UrlMetadata` nodes (renamed from `:ExternalLink`) | preserved count from S2 | v6.C |
| `unfolding_kind` set on every gebäude-touched node | **100 %** | v6.B audit |
| Audit query `fully_traced %` for `:Projekt`, `:Material`, `:Bauteil`, `:Akteur` | **≥ 80 %** for gebäude-anchored | v6.D |

The 5 abbreviation-mismatch dossiers are the explicit miss until the alias YAML is filled in.

---

## §9 The provenance taxonomy — same 10 kinds, gebäude-relevant subset

Of the 10 kinds in v6 §4:

| Kind | Used by v6.1 gebäude wave |
|---|---|
| `dossier_row` | YES — primary kind for every emitted triple |
| `dossier_section` | YES — used when a row has a section-level note instead of a row Quelle |
| `bauteilboerse_file` | no — out of scope |
| `registry_row` | no — out of scope |
| `research_section` | no — out of scope |
| `research_table_row` | no — out of scope |
| `inference_rule` | preserved on existing inference-derived nodes |
| `controlled_vocabulary` | preserved on existing vocab nodes |
| `topology_synthesized` | preserved |
| `user_curated` | preserved |

So the gebäude wave touches `unfolding_kind ∈ {dossier_row, dossier_section}` for the new edges, and **does not overwrite** the 4 inferential/synthetic kinds on existing nodes.

---

## §10 What changes in this doc vs v6

| In v6 | In v6.1 |
|---|---|
| 4 unfolders to author | **1 unfolder** (gebäude only) |
| "Estimated ~thousands of triples" | **6,150 triples (measured)** |
| Two citation styles unmentioned | **Two styles named + parser tested** |
| No abbreviation-mismatch handling | **`quellen_alias.yaml` overlay** for 5 dossiers |
| Locator format = handwaved | **Locator format pinned (see §5)** |
| v6.B touches all nodes | **v6.B touches gebäude-anchored nodes only** |

---

## §11 Why we trust the count

The 6,150 number is the output of the parser run against the actual disk content, not an estimate. Per-dossier counts are in [unfold_all_gebaeude_summary.json](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude_summary.json). The full triple log is in [unfold_all_gebaeude_triples.jsonl](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude_triples.jsonl) — 6,150 lines, one JSON object per line, ready to chunk and `MERGE` into Neo4j.

Spot-check the JSONL with `head -1` to see the shape:

```json
{
  "dossier_id": "holbein_gardens_london",
  "section": "2. ENTITÄTEN-MAPPING",
  "row_idx": 0,
  "kind": "entity_value",
  "entity_type": "Fallstudie",
  "entity_value": "Holbein Gardens",
  "sref": "S1",
  "url": "https://www.grosvenor.com/news-insights/some-of-uk's-first-salvaged-steel-...",
  "url_title": "Grosvenor"
}
```

Each line maps one-to-one to one `:CITED_FROM_DOSSIER` edge that v6.1.A.1 writes.

---

## §12 Execution result (2026-05-22)

Executed against live `mit-bestand` with:

```bash
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py
```

Pre-write backup:
- `_neo4j/review/backups/2026-05-22_pre_qext_v6_1_gebaeude`

Result in Neo4j:

| Metric | Actual |
|---|---:|
| `:CITED_FROM_DOSSIER` edges written by `qext_v6_1_gebaeude_unfolder` | 6,150 |
| Distinct `source_url` values | 388 |
| Dossiers touched | 71 |
| Raw `(entity_type, entity_value)` targets | 2,591 |
| `DossierEntityTarget` nodes | 2,591 |
| `EXACT_MATCH_CANDIDATE` review edges | 306 |

Review status of raw targets:

| Status | Count |
|---|---:|
| `unresolved_no_exact_match` | 2,282 |
| `exact_unique_candidate` | 306 |
| `exact_ambiguous_candidates` | 3 |

Implementation artefacts:
- Runner: [qext_v6_1_gebaeude_runner.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py)
- Report JSON: [qext_v6_1_gebaeude_import_report.json](../intake/runs/2026-05-21_quelle_remediation/agent_qext/reports/qext_v6_1_gebaeude_import_report.json)
- Report MD: [qext_v6_1_gebaeude_import_report.md](../intake/runs/2026-05-21_quelle_remediation/agent_qext/reports/qext_v6_1_gebaeude_import_report.md)
- Done flag: `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/PHASE_QEXT_V6_1_GEBAEUDE_DONE.flag`
- Next-step plan: [NEXT_STEPS_v6_1_gebaeude.md](NEXT_STEPS_v6_1_gebaeude.md)

Important boundary: this execution imported the 6,150 gebäude JSONL triples. It did **not** run the broader destructive v6.C `kill_zitiert_quelle` migration; current graph audit still reports 8,229 `:ZITIERT_QUELLE` relationships. That broader migration remains a separate wave because it touches non-gebäude source chains too.

---

**End of REFACTOR_v6_1_gebaeude_concrete.md.**
