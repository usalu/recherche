# Orchestrator decisions — Quelle remediation

> Append-only. Each row is a decision the orchestrator made during integration that an agent's brief did not explicitly resolve.

---

## OD-Q1 — Use of secondary labels over standalone labels (2026-05-21)

### Context

`:Quelle` had 5+ sub-types via a `.quelltyp` property. Discriminator-as-property is unergonomic in Neo4j Browser (every query needs a `WHERE`). Standalone labels would break existing `BELEGT_IN → :Quelle` queries.

### Decision

Use **secondary labels** on the same node: `:Quelle :Dossier`, `:Quelle :ExternalLink`, etc. Keeps back-compat AND enables `MATCH (d:Dossier)` for new queries.

### Rationale

Cheap; reversible; zero query-breaking.

---

## OD-Q2 — Body cache shared between S2 and S3 (2026-05-21)

### Context

S2 fetches every URL once; S3 needs to parse the body. Doing fresh HTTP in S3 would double network load and risk inconsistency between probe-time and verify-time.

### Decision

S2 owns `shared/url_bodies/<md5>.{html,pdf}.{gz}` cache. S3 reads from it. Each cache file has a companion `.meta.json` so the cache is self-describing.

### Rationale

One HTTP request per URL. Deterministic verification (same body that was probed). Forensic auditability.

### Reversibility

Delete the cache directory; both S2 and S3 will re-create their parts on re-run.

---

## OD-Q3 — Wayback Machine as a first-class fallback (2026-05-21)

### Context

Many cited URLs are 5–10 years old. Some are dead by now. Without a fallback, those citations become irrecoverable.

### Decision

- **Proactive archiving** for every reachable URL: fire-and-forget `web.archive.org/save/<url>` (QD-1).
- **Snapshot lookup** for every dead URL: `archive.org/wayback/available?url=<url>` (S2 step).
- **Verification on snapshot** for dead URLs that have a snapshot (QD-5): treat as valid evidence, but tag `verification_method='wayback'` so the user knows.

### Rationale

Cheap insurance. Maintains research integrity even when source pages disappear.

### Reversibility

Tag, don't bake — `url_wayback_*` properties are pure metadata.

---

## OD-Q4 — Three-tier match algorithm with explicit thresholds (2026-05-21)

### Context

A binary "exact match or no match" is too brittle for real prose. A pure semantic match (embeddings) is too expensive and opaque.

### Decision

Three explicit tiers:
- **A:** exact substring (after normalisation) → `verbatim_match`, score=1.0
- **B:** RapidFuzz `partial_ratio ≥ 85` → `paraphrase_match`, score=ratio/100
- **C:** token-set overlap ≥ 0.80 of significant tokens → `token_match`, score=overlap
- **Fallback:** `no_text_match`, score=best of B/C seen, method='none'

Each citation edge records its tier + score. The user can re-tune thresholds and re-run S3 with `--threshold-*` overrides.

### Rationale

Transparent, explainable, replayable. No black-box semantic match.

---

## OD-Q5 — `source_trust_score` formula (2026-05-21)

### Context

The user needs a single number to sort `:Projekt` nodes by source quality in Browser. Multiple components → must combine somehow.

### Decision

`source_trust_score(p) = mean over all paths of (url_reachability × verification_grade)`.

`url_reachability` and `verification_grade` are explicit constants per status (see [AGENT_S5_visibility.md §3](AGENT_S5_visibility.md)). NULL when the node has no citation paths.

### Rationale

- Multiplicative penalises dead URLs (they multiply by 0.0–0.5).
- Mean across paths means projects with many sources average out single failures.
- NULL distinguishes "untested" from "tested and failing".

### Open question

Could a weighted formula (give recent verifications more weight) be better? Defer to a future round; current formula is a Schelling point.

---

## OD-Q6 — Treatment of `topology_synthesized` edges (2026-05-21)

### Context

R1's reclassification labelled 19,071 edges as `topology_synthesized` (the Repair D auto-generated excerpts). These aren't supposed to be verbatim from a source; verifying them is meaningless.

### Decision

S3 **explicitly skips** edges with `evidence_origin IN ['topology_synthesized','inferred','registry_derived']`. The `verification_status` for these stays as default (set by S3 to `'skipped_non_curated'` on first pass).

Only `evidence_origin='source_curated'` edges undergo the three-tier match.

### Rationale

Verification is a meaningful question only for source-curated claims. Synthesizing a verification on synthesized text is theater.

### Side effect

The `source_quality_summary` reported by S5 honestly reflects only the source-curated portion of a node's evidence. Topology-synthesized edges contribute to `source_urls` (via S5's traversal) but don't count in `n_verbatim` / `n_no_match`. A separate property `n_topology_skipped` may be added if useful.

---

## OD-Q7 — Cross-language citations (2026-05-21)

### Context

Some dossier excerpts are in German; some cited pages are in English (or vice versa). Cross-lingual semantic matching needs translation infrastructure we don't have.

### Decision (QD-6 default)

Detect language on both excerpt and page text. If they differ, tag `verification_status='language_mismatch'`. Emit `:DataIssue {kind:'citation_language_mismatch'}` for future manual review.

### Future work

A v2 could translate the excerpt via the Claude API and retry the three-tier match. Estimated cost: $0.001 per citation × ~3,000 source_curated = $3. Cheap, but defer to a follow-up round.

---

## OD-Q8 — Re-curation pathway (not in scope for this run) (2026-05-21)

### Context

S6 emits `:DataIssue` for every `no_text_match`. The user then has to decide: is the citation wrong, or is the page wrong?

### Decision

Not addressed in this round. Manual re-curation is a separate workflow:

1. Pull all `MATCH (i:DataIssue {kind:'citation_no_text_match', status:'open'})`.
2. For each, open the URL, read the page, find the actual cell.
3. Either:
   - Update the dossier `.md` file (preferred — preserves source-of-truth).
   - Or, if the URL is fundamentally wrong, mark the `:DataIssue` as `status='wont_fix'` with a note.

A future agent could automate (2) via the Claude API ("here's the excerpt, here's the page, does any other excerpt match?").

---

**End of ORCHESTRATOR_DECISIONS.md.**
