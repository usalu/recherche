# Q-EXT.C v4 — refactor decision (page-content cross-check)

**Date:** 2026-05-22 r2 · **Author:** orchestrator
**Trigger:** user instruction: "compare it to the html and figure out how to refactor the plan and make it work for each node. pick 2-5 elements of each node type for testing"

> **TL;DR.** I ran a comparator on 16 sample nodes across 5 types. The cached HTML bodies (S2's `shared/url_bodies/`) provide ground truth. The previous v3 rule (C3 = dossier-side mention) produces **false claims of source backing** — the dossier may cite a URL but the page doesn't actually confirm anything. The right criterion is **C4 = BOTH (dossier-side AND page-side mention)**. This document presents the test results and proposes v4.

---

## §1 What I tested

[test_node_link.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/test_node_link.py) — a Python harness that:

1. Builds an index of 726 URL → cached body path entries from `shared/url_bodies/*.meta.json`.
2. For each test node, reads the dossier `.md` file from disk.
3. For each URL cited in the dossier, looks up the cached HTML body.
4. Tests **three** evidence types:
   - **D** (dossier-mention): node term appears in `.md` near the URL
   - **P** (page-mention): node term appears in the cached HTML body
   - **BOTH** (D + P): the gold standard

### 16 test nodes across 5 types

| Type | Sample nodes | Dossiers |
|---|---|---|
| Material | Holz, Beton, Stahl (×2) | Stuttgart 210, Holbein, K118 |
| Norm | CEN/TS 1090-201, EN 1090 | Holbein |
| Bauteilgruppe | Schalungselement, formwork | Stuttgart 210 |
| Akteur | HTWG Konstanz, Klingelhöfer Krötsch, AKT II, Baubüro in situ | Stuttgart 210, Holbein, K118 |
| Schadstoff | Asbest | Holbein |
| Projekt | Stuttgart 210, Holbein Gardens, K118 | (same) |

---

## §2 Results table

For each (node, dossier), the URLs were checked against both dossier-text and cached-page-text. Counts shown out of the URLs the dossier cites for that node's context.

| Node | Dossier | URLs total | URLs cached | **BOTH** | D only | P only | neither |
|---|---|---:|---:|---:|---:|---:|---:|
| **Material** |  |  |  |  |  |  |  |
| Holz | Stuttgart 210 | 179 | 115 | **20** | 14 | 88 | 57 |
| Beton | Stuttgart 210 | 179 | 115 | **5** | 10 | 62 | 102 |
| Stahl | Holbein | 13 | 10 | **10** | 3 | 0 | 0 |
| Stahl | K118 | 9 | 7 | 0 | 0 | 4 | 5 |
| **Norm** |  |  |  |  |  |  |  |
| CEN/TS 1090-201 | Holbein | 13 | 10 | **0** | 0 | 0 | 13 |
| EN 1090 | Holbein | 13 | 10 | **0** | 0 | 0 | 13 |
| **Bauteilgruppe** |  |  |  |  |  |  |  |
| Schalungselement | Stuttgart 210 | 179 | 115 | **0** | 2 | 0 | 177 |
| formwork | Stuttgart 210 | 179 | 115 | **0** | 30 | 0 | 149 |
| **Akteur** |  |  |  |  |  |  |  |
| HTWG Konstanz | Stuttgart 210 | 179 | 115 | **30** | 1 | 78 | 70 |
| Klingelhöfer Krötsch | Stuttgart 210 | 179 | 115 | **19** | 19 | 15 | 126 |
| AKT II | Holbein | 13 | 10 | **0** | 0 | 0 | 13 |
| Baubüro in situ | K118 | 9 | 7 | **4** | 0 | 3 | 2 |
| **Schadstoff** |  |  |  |  |  |  |  |
| Asbest | Holbein | 13 | 10 | **0** | 0 | 0 | 13 |
| **Projekt** |  |  |  |  |  |  |  |
| Stuttgart 210 | Stuttgart 210 | 179 | 115 | **76** | 17 | 39 | 47 |
| Holbein Gardens | Holbein | 13 | 10 | **9** | 4 | 0 | 0 |
| K118 | K118 | 9 | 7 | **4** | 5 | 0 | 0 |

---

## §3 What the data tells us — five findings

### F1 — "BOTH" is the gold standard

When both the dossier text near the URL AND the cached page body mention the node, the link is essentially proven. Holbein → Stahl scored 10 BOTH / 0 P-only / 0 neither — every cited URL holds up under cross-check.

### F2 — "D only" cases are real false claims

Stuttgart 210 dossier cites the baunetzwissen.de project page via [S7] across many of its rows. But the baunetzwissen.de page is specifically about the **Ingersheim youth pavilion** — it doesn't say "Klingelhöfer Krötsch" or "Stuttgart 210" as labels. The dossier author lumped that URL into many cells; only some are warranted.

19 D-only matches for `Klingelhöfer Krötsch` is the signature pattern — the dossier author put their name in multiple cells but only ~half the URLs they cited actually mention them.

**Implication: C3 (dossier-mention only) treats "D only" as confirmation. v4 must require BOTH.**

### F3 — "P only" is coincidental noise

"Holz" appears in 88 page-bodies of URLs cited by Stuttgart 210, but the dossier text near most of those URLs is about a different topic (e.g., a row about asbestos that happens to cite a building-info page that incidentally mentions wood). Counting P-only as confirmation would inflate every Material with hundreds of spurious URLs.

### F4 — Norms with version numbers are unfindable

"CEN/TS 1090-201" — exact literal — appears in zero pages. Pages say "EN 1090", "CEN/TS 1090", or no version at all. Need partial-token matching for norms — match on the most-discriminating numeric token (e.g., "1090-201" → "1090"), with a clear ranking.

### F5 — Projekt nodes are special (high BOTH rate)

Stuttgart 210: 76 BOTH out of 115 cached URLs (66 %). Holbein Gardens: 9 of 10 (90 %). K118: 4 of 7 (57 %). These are the strongest signals because the dossier and the URLs ARE about the project. Projekt nodes should always be C4-confirmable; if they're not, the dossier ↔ URL relationship is suspect.

---

## §4 The refactor — v4 design

### §4.1 New criterion C4 (replaces C3)

```
C4 — Cross-confirmed mention.
    For a (node, URL) pair, C4 holds iff:
      • The dossier .md text near the URL citation mentions a term for the node, AND
      • The URL's cached page body mentions a term for the node.
    Term = expanded set per node:
      - node.name (lowercased, ≥ 4 chars)
      - all entries in node.aliases
      - curated DE↔EN synonyms from synonyms.json
      - id-stem (mat_stahl → 'stahl')
      - For Norm: strongest digit-token (CEN/TS 1090-201 → '1090-201' or '1090')
```

C1 (dossier-grounded direct edge) and C2 (S3 content-verified) remain unchanged. C3 (D-only) is **deprecated** — it produces false positives.

### §4.2 New evidence prefix

```
evidence_grammar:
  'c1_dossier_grounded:<dossier_id>:<sref>'
  'c2_content_verified:<method>:<score>'
  'c4_cross_confirmed:<dossier_id>:<d_terms>:<p_terms>'  ← REPLACES 'excerpt_mention:'
```

`confirmed_source_urls` is the set of URLs that pass at least one of C1/C2/C4.

### §4.3 Architecture change

C3 was a pure-Cypher rule (`zq.evidence_excerpt =~ regex`). C4 needs the cached HTML body, which lives on disk in `shared/url_bodies/`. So C4 is **runner-side**, not pure Cypher:

```
Q-EXT.C v4 runner (run_confirm4):
  1. Build URL → cache-path index (already implemented in test_node_link.py).
  2. For every (node, URL) candidate from the broad source_urls set:
     a. Locate the citing :ZITIERT_QUELLE edge's evidence_excerpt (D-text).
     b. Locate the cached page body for the URL (P-text).
     c. Expand node terms (name + aliases + synonyms + id-stem + norm-token).
     d. Test: D_hit = any term in D-text; P_hit = any term in P-text.
     e. If D_hit AND P_hit → record as confirmed URL with reason c4.
  3. Aggregate per node; write confirmed_source_urls + confirmation_evidence.
  4. Set primary_source_url = confirmed_source_urls[0].
```

### §4.4 Migration shape

[mig_qext_c_v4_confirmed_urls.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_qext/migrations/mig_qext_c_v4_confirmed_urls.cypher) is a simple parameterised write:

```cypher
// Per node — runner pre-computes the confirmed list with reasons
UNWIND $node_results AS row
MATCH (n {id: row.node_id})
SET n.confirmed_source_urls   = row.confirmed_urls,
    n.confirmed_source_count  = size(row.confirmed_urls),
    n.confirmation_evidence   = row.evidence,
    n.primary_source_url      = CASE WHEN size(row.confirmed_urls) > 0
                                     THEN row.confirmed_urls[0] ELSE NULL END,
    n.confirmed_urls_updated_at = date(),
    n.migration_origin = coalesce(n.migration_origin, '') + ' | mig_qext_c_v4_cross_confirmed';
```

The heavy lifting (text extraction, matching) is in Python.

---

## §5 Expected outcomes after v4 runs

Based on the 16-node sample, projected across the graph:

| Node type | Expected confirmed URL ratio |
|---|---|
| `:Projekt` | high — most projects have BOTH-confirmed URLs |
| `:Akteur` (well-known) | medium-high — registry actors have their own URLs |
| `:Material` | medium — depends on synonym coverage |
| `:Norm` | low — needs partial-token matching (still residual) |
| `:Bauteilgruppe` | low — German technical terms rarely on English pages |
| `:Schadstoff` | varies — Asbest works via "asbestos", others may not |

This is the honest signal. Materials and Norms scoring low isn't a bug; it's the corpus's bilingual reality and the fact that most material-level claims come from German technical text that doesn't appear in cited (often English) pages.

---

## §6 What to delete from v2/v3

- The `excerpt_mention:` reasons in `confirmation_evidence` are misleading — they imply confirmation but only checked one side. v4 deprecates them.
- `primary_source_url` from v1 (loose reachability heuristic) is removed.

The `source_urls` array from Q-EXT.B is **kept** — it's the broad candidate set, useful for context. `confirmed_source_urls` is the strict subset.

---

## §7 Edge cases noticed during testing

1. **Holbein → Asbest = 0/13.** Holbein Gardens dossier mentions asbestos for context but the project isn't fundamentally about asbestos. The 0 BOTH count is honest — those URLs don't confirm Asbest.

2. **Stuttgart 210 → Schalungselement = 0/179.** The German technical term appears only in 2 dossier cells; cached pages (mostly English) don't say "Schalungselement". The dossier itself uses "formwork" in some cells (30 D-only matches). v4 should test ALL terms; "formwork" SHOULD have matched some pages but didn't because the bilingual matching wasn't applied. **Fix**: ensure synonym map covers German↔English for Bauteilgruppe too.

3. **Klingelhöfer Krötsch — 19 BOTH AND 19 D-only.** Half the dossier's claims are confirmed by page content; the other half aren't. The user can see this in the evidence map — partial confirmation is itself a valuable signal.

4. **K118 → Stahl = 0 BOTH / 4 P-only / 5 neither.** Surprising. The K118 dossier doesn't have "Stahl" near any URL in the dossier text — but several pages mention it. Means: either the K118 dossier should be edited to include "Stahl" in the relevant rows, OR the URLs are page-grounded but not dossier-claimed for steel. v4 honestly tags these as not confirmed.

---

## §8 What you decide

| ID | Question | Default |
|---|---|---|
| V4-1 | Replace C3 entirely or keep both (with C3 demoted to a lower-trust tier)? | **Replace** — keep code simple |
| V4-2 | For Norms, fall back to the strongest numeric token when full literal fails? | YES |
| V4-3 | Skip nodes with name length < 4 (current behavior)? | YES |
| V4-4 | Cap page-text scan at 80k chars per URL for performance? | YES (already done in test) |
| V4-5 | Run v4 against ALL ~2,420 source-bearing nodes, or just a sample first? | Run all; idempotent. Single pass takes ~10–20 minutes. |
| V4-6 | Re-include German↔English synonyms for Bauteilgruppe / process labels? | YES — extend synonyms.json |

---

## §9 Run instructions (once v4 runner is wired in)

```bash
# (Q-EXT.A v2 — re-extract wider dossier context — was already prepared as 'rewiden'.
#  Optional; v4 doesn't strictly need it since the runner reads dossiers from disk.)

# Q-EXT.C v4 — cross-confirmed source URLs (replaces v1/v2/v3 primary/confirm logic):
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_runner.py confirm4
```

Writes `PHASE_QEXT_C_V4_DONE.flag`. Idempotent.

---

## §10 Long-term-plan adjustment

[LONG_TERM_PLAN.md §4.1](../LONG_TERM_PLAN.md) (Ingestion contract) gets one new validator: `validate_url_cache_present.py` — every new `:ZITIERT_QUELLE` edge requires a corresponding S2 body cache entry; otherwise C4 can never confirm and the citation is downgraded automatically.

This pushes future ingestion into a virtuous loop: probe → cache → confirm at write time.

---

**End of REFACTOR_v4_decision.md.**
