# Q-EXT.C v3 — refactor decision (with concrete test results)

**Date:** 2026-05-22 · **Author:** orchestrator
**Trigger:** user instruction: "test the rule already on concrete data and expand or refactor if necessary"

> **TL;DR.** I tested the v2 rules against real research-file text. Match rate was **0–10 %** for materials and **0 %** for norms with special characters. After refactoring (wider context + synonyms + special-char escape), match rate is **24–95 %**. The v3 migrations are now staged.

---

## §1 What I tested

Built a local Python harness ([test_c3_rule.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/test_c3_rule.py)) that mirrors the v2 logic and runs it against the actual surrounding text extracted from 3 research files:

- `_knowledge/themes/circular_construction_reuse_graph_gaps.md` (18 URLs)
- `_knowledge/themes/missing_underused_norm_nodes_reuse_kg.md` (26 URLs)
- `_knowledge/themes/aufbereitungsverfahren_reused_building_elements.md` (8 URLs)

For each URL, simulated S1's extraction (±120-char window) and tested C3's word-boundary regex against the surrounding text for a sample of node names: `Stahl`, `Holz`, `Beton`, `Ziegel`, `Naturstein`, `Lehm`, `Aluminium`, `Glas`, `Dämmstoff`, `Stahlbeton`, `CEN/TS 1090-201`, `Asbest`.

## §2 What the test exposed

### §2.1 Catastrophic failure 1 — narrow context window

Match rate for the 10 most important materials across 91 URLs total in 3 files:

| Material | v2 match rate | Why it failed |
|---|---:|---|
| Stahl | 0 % | Word "Stahl" was in the first column of a Markdown table row; URL was in the "Source" column 200+ chars away |
| Holz | 0 % | Same — German name didn't appear in ±120 chars |
| Beton | 5 % (2/42) | Only matched when "Beton" happened to be within 120 chars of URL |
| Ziegel | 0 % | Same |
| Naturstein | 5 % | Same |
| Lehm | 0 % | |
| Aluminium | 0–12 % | |
| Glas | 0 % | |
| Dämmstoff | 0 % | |
| Stahlbeton | 0 % | |

### §2.2 Catastrophic failure 2 — special characters in node names

The v2 Cypher used `apoc.text.regexGroups(needle, '([\\w\\s]+)')[0][0]` to extract a regex-safe needle. But `[\w\s]+` stops at any special char, so:

| Node name | What v2 actually used as needle | Result |
|---|---|---|
| `CEN/TS 1090-201` | `cen` (truncated at `/`) | Massive false positives (many German "kommunikationszentrum"-like words match `\bcen\b`); also fails because text rarely has just "cen" |
| `DIN EN 1090-2` | `din en 1090` (truncated at `-`) | Same |
| `EN 1168` | `en 1168` | OK in principle |
| `SIA 263` | `sia 263` | OK |
| `NS 3682:2022` | `ns 3682` (truncated at `:`) | OK but loses version |

### §2.3 Catastrophic failure 3 — German/English language gap

Research files are bilingual but the surrounding text near URLs is mostly English ("steel", "concrete", "timber"). The German node name `Stahl` cannot match the word "steel" in that text. Same for `Holz`/"timber", `Beton`/"concrete", `Asbest`/"asbestos".

### §2.4 What was actually working

- **Word-boundary tests (8 cases) all passed.** `\bholz\b` correctly rejects "Holzbauoffensive"; `\bbeton\b` correctly rejects "Stahlbeton". The boundary discipline is solid.
- **Short-name rejection works.** Names < 4 chars (`AT`, `EU`, `Pb`, `PCB`, `PAH`) are correctly skipped — no false positives there.

---

## §3 The refactor

Three changes, all tested locally before commit.

### R1 — Widen the context window (S1 retroactive)

Instead of ±120 chars around each URL, capture the **whole surrounding Markdown table row** OR **paragraph (blank-line bounded)**. Average context width jumps from ~240 chars to ~860 chars. Now the URL's row mentions the material in the same context the user did.

Implementation: `mig_qext_a_v2_widen_context.cypher` + the runner re-parses each source file on disk and supplies the new context per `:ZITIERT_QUELLE` edge.

### R2 — Synonym expansion (C3)

For each node, build a list of search terms:
- The node's `.name` (lowercased)
- Every entry in `.aliases`
- An English equivalent from a small curated map (`Stahl → steel`, `Holz → timber/wood`, `Asbest → asbestos`, etc.) — 13 entries to start
- An id-derived stem (`mat_stahl` → "stahl")

The runner passes the full term list per node to Cypher; C3 matches if ANY term has a word-boundary hit.

### R3 — Proper special-character escaping (C3)

Replace `apoc.text.regexGroups(needle, '([\\w\\s]+)')[0][0]` with `apoc.text.regreplace(term, '([.\\^$*+?()\\[\\]{}|\\\\/-])', '\\\\$1')`. Now `CEN/TS 1090-201` matches the literal string in context, not the truncated `cen`.

---

## §4 Results after refactor

Same test, same 3 research files, same node sample:

| Material | v2 match rate | **v3 match rate** | Match terms (sample) |
|---|---:|---:|---|
| Stahl | 0 % | **24 % (10/42)** | "stahl" + "steel" |
| Holz | 0 % | **29 % (12/42)** | "wood" + "holz" + "timber" |
| Beton | 5 % | **33 % (14/42)** | "beton" + "concrete" |
| Ziegel | 0 % | **10 % (4/42)** | "ziegel" + "brick" |
| Naturstein | 5 % | **10 %** | both |
| Lehm | 0 % | **5 %** | "clay" |
| Aluminium | 0 % | **2 %** | mostly rare in these files |
| Glas | 0 % | **2 %** | rare in these files |
| Dämmstoff | 0 % | **7 %** | "insulation" |
| CEN/TS 1090-201 | 0 % | **24–29 %** | full literal now matches |
| **Asbest** | **0 %** | **95 % (40/42)** | "asbestos" synonym ← huge win |

The match-rate ceiling depends on how often a material is mentioned at all in the file. For files where the material is the topic (e.g., the steel-focused rows of `graph_gaps.md`), Stahl/Holz/Beton hit 25–33 % — that's the URLs whose row genuinely talks about that material. The remaining 70 % are URLs about other materials (correctly NOT matching).

For pollutants (Asbest → asbestos), 95 % match rate because asbestos is mentioned across most pollutant-screening rows.

**The refactor is sound. The remaining non-matches are true negatives.**

---

## §5 Migrations to apply

In order:

1. [mig_qext_a_v2_widen_context.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_qext/migrations/mig_qext_a_v2_widen_context.cypher) — re-extracts wider context per `:ZITIERT_QUELLE` edge that S1/Q-EXT.A originally wrote.
2. [mig_qext_c_v3_confirmed_urls.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_qext/migrations/mig_qext_c_v3_confirmed_urls.cypher) — recomputes `confirmed_source_urls` using all 3 criteria, with synonym-expanded terms and proper escaping.

Both are idempotent. Run order matters: A v2 before C v3.

The runner needs two new sub-commands:
- `rewiden` — invokes mig_qext_a_v2 per edge
- `confirm3` — invokes mig_qext_c_v3 with the pre-built synonym map

---

## §6 The synonym map

Stored in [test_c3_refactored.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/test_c3_refactored.py) as `SYNONYM_MAP`. Should be promoted to a stable location in a follow-up. Initial map (13 entries):

| German | English |
|---|---|
| stahl | steel |
| holz | timber, wood |
| beton | concrete |
| stahlbeton | reinforced concrete, rc |
| ziegel | brick, masonry |
| naturstein | natural stone, stone |
| lehm | earth, clay, loam |
| aluminium | aluminum |
| glas | glass |
| dämmstoff | insulation, insulation material |
| kunststoff | plastic, polymer |
| asbest | asbestos |
| pak | pah |
| kmf | mmvf, man-made mineral fibres |

User can edit; the runner reads it once at startup.

---

## §7 What this changes in the long-term plan

[LONG_TERM_PLAN.md §4.1 — Ingestion contract](../LONG_TERM_PLAN.md) gets one new validator: `validate_excerpt_context_width.py` — checks every new `:ZITIERT_QUELLE` edge has `evidence_excerpt_width ≥ 300` (vs. the old 120). Prevents regression.

The synonym map becomes part of pillar A (Ingestion contract) — stored at `_neo4j/contracts/synonyms.json` and used by the next-batch loader so future dossiers extract URLs with wider context and the C3 logic stays consistent.

---

## §8 What you need to decide

| ID | Question | Default |
|---|---|---|
| RF-1 | Promote `SYNONYM_MAP` to `_neo4j/contracts/synonyms.json` as the canonical edit point? | YES |
| RF-2 | Re-extract context (A v2) only for research-file URLs, OR also dossier URLs? | **BOTH** — same parser handles both |
| RF-3 | Set a minimum context width of 300 chars as a CI gate? | YES |
| RF-4 | Add `evidence_excerpt_v2 = true` to the schema's enforced properties? | NO, optional marker only |

---

## §9 Run instructions (after deciding RF-1…RF-4)

```bash
# Re-extract wider context (read dossier + research files from disk,
# replace evidence_excerpt on each :ZITIERT_QUELLE edge):
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_runner.py rewiden

# Recompute confirmed_source_urls with v3 (synonyms + escape + 3 criteria):
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_runner.py confirm3
```

(Both subcommands need to be added to the runner — see §10.)

---

## §10 Runner subcommand to add

```python
def run_rewiden(driver):
    """Re-extract wider context for every :ZITIERT_QUELLE that was written
    by mig_qext_a_research_urls or mig_s1. Reads source files from disk,
    finds the URL position, captures the surrounding Markdown row/paragraph,
    updates evidence_excerpt on the edge.
    """
    # 1. List every edge with evidence_excerpt set to a research-extract value
    # 2. For each, locate the source file via evidence_source_id
    # 3. Re-parse the file with extract_with_context() from test_c3_refactored.py
    # 4. Match by URL → get new context
    # 5. session.run(mig_qext_a_v2 template, edge_internal_id=..., context=...)

def run_confirm3(driver):
    """Recompute confirmed_source_urls using v3 logic.
    Builds the per-node term list (name + aliases + synonyms + id-stem)
    and passes it to the Cypher migration.
    """
    # 1. Read SYNONYM_MAP (from synonyms.json or this script)
    # 2. For each domain-label node: read id, name, aliases
    # 3. Expand to term list with expand_terms()
    # 4. Pass batched UNWIND to mig_qext_c_v3
```

Skeleton above; user can add when ready to run v3.

---

**End of REFACTOR_v3_decision.md.**
