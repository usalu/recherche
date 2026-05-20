# Agent 8 — Wave-3 Report (Phase 4c)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 8 of 12 — Wave 3, Phase 4c (source-as-link enforcement)
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 4c.1, 4c.3, edge strip, 4c.2 prep
**Scope NOT touched:** §4c.2 full backfill (Agent 9 / 10 own dossier parsing); §4b loader rewrite; any Phase 3 enrichment.

## Status

`PHASE_4C_DONE.flag` written at the run root. Re-running `agent8_runner.py`
is a verified no-op (the live counts hit by the runner's idempotency
probes are all zero after this pass: `external_sources_remaining = 0`,
`projekt_belegt_actor_registry = 0`, `edges_with_illegal_keys = 0`).

## Top-line counts

| Marker                                                   | Before Agent-8 | After Agent-8 | Δ |
|---|---:|---:|---:|
| Total nodes                                              | 2 674          | **2 674**    | 0 |
| Total relationships                                      | 19 800         | **19 624**   | **-176** (Phase 4c.3 detach) |
| `:Quelle` total                                          | 726            | **726**      | 0 |
| `:Quelle.external_sources` arrays                        | 0              | **0**        | 0 (already done by Agent 6) |
| `:ZITIERT_QUELLE` edges                                  | 639            | **639**      | 0 |
| `:Quelle.quelltyp = 'external_link_from_actor_registry'` | 319            | **319**      | 0 (target nodes preserved) |
| `(Projekt)-[:BELEGT_IN]->(actor_registry Quelle)`        | **176**        | **0**        | **-176** |
| `(Akteur)-[:BELEGT_IN]->(actor_registry Quelle)`         | 360            | **360**      | 0 (preserved, plan §4c.3) |
| Relationships with `url`/`http`/`source_file`/`external_sources` key | 0 | **0**        | 0 (already clean) |
| Distinct illegal rel keys                                | 0              | **0**        | 0 |

## Files produced

```
runs/2026-05-20_radical_quality_reset/
├── PHASE_4C_DONE.flag
├── migrations/
│   ├── mig_4c_1_external_sources_unfold.cypher                    (canonical pattern + acceptance)
│   ├── mig_4c_3_detach_projekt_actor_registry_belegt.cypher       (canonical delete + acceptance)
│   └── mig_4c_edge_strip.cypher                                   (canonical audit + acceptance)
├── deleted/
│   ├── phase4c_3_projekt_actor_registry_belegt.jsonl              (176 lines: per-edge forensic snapshot)
│   └── (phase4c_1_external_sources.jsonl / phase4c_edge_strip.jsonl not written — both no-ops)
├── logs/
│   ├── agent8_probe.py                                            (read-only pre-flight probe)
│   ├── agent8_runner.py                                           (orchestrator: 4c.1 → 4c.3 → edge strip)
│   ├── agent8_progress.log                                        (stamped runtime log)
│   ├── agent8_result.json                                         (machine-readable before/after counts + payload)
│   ├── agent8_case_md_inspect.py / .json                          (live :Quelle case_markdown census)
│   └── agent8_build_manifest.py                                   (Phase 4c.2 manifest generator)
└── reports/
    ├── agent_8_phase4c_report.md                                  (this file)
    └── agent_8_dossier_manifest.json                              (Phase 4c.2 prep for Agent 9)
```

## Phase 4c.1 — Unfold `:Quelle.external_sources` → `:ZITIERT_QUELLE`

**No-op on this run.** Pre-flight probe confirmed:

- `MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q)` → **0**
- `MATCH ()-[r:ZITIERT_QUELLE]->() WHERE r.evidence_basis = 'external_sources_array' RETURN count(r)` → **269** (≈ 270 reported by Agent 6 — exact match after counting the one entry whose raw string contained no URL and was therefore skipped).
- `MATCH (q:Quelle) WHERE q.quelltyp = 'external_link' RETURN count(q)` → **264** target nodes — matches Agent 6's `Phase 2.7.b` count of 264 net new targets.

**Source of prior work:** Phase 2.7.b executed by Agent 6 on 2026-05-20 with
identical canonical pattern. Per-source forensic record kept at
`deleted/phase2_7_external_sources.jsonl` (60 lines).

Agent 8's canonical, idempotent re-statement of the migration lives at
`migrations/mig_4c_1_external_sources_unfold.cypher`. The runner
(`logs/agent8_runner.py`, function `run_phase_4c_1`) re-implements the
same unfold logic with the same slugify / extract-title heuristics and
the same 5-field evidence shape, so a future regression that
reintroduces an `external_sources` array can be fixed by re-running
Agent 8 alone.

## Phase 4c.3 — Detach wrong `(Projekt)-[:BELEGT_IN]->(actor_registry Quelle)`

**Done.** 176 edges deleted in a single transaction (`logs/agent8_runner.py`,
function `run_phase_4c_3`).

| Step | Result |
|---|---|
| Pre-delete count                                                          | 176 |
| Forensic snapshot (`deleted/phase4c_3_projekt_actor_registry_belegt.jsonl`) | 176 JSON lines, one per edge: `projekt_id`, `quelle_id`, `quelle_url`, full `rel_props` for reversibility |
| `DELETE r` (single tx)                                                    | 176 edges removed |
| Post-delete count                                                          | 0 |
| `(Akteur)-[:BELEGT_IN]->(actor_registry Quelle)` invariant                | 360 → 360 (unchanged) |
| Target `:Quelle.quelltyp='external_link_from_actor_registry'` node invariant | 319 → 319 (unchanged) |

**Why this matters:** Actor-registry URLs document an actor's identity
(homepage, Wikipedia, archdaily author page, etc.). Folding them onto a
`:Projekt` via `BELEGT_IN` produces ~176 spurious "this project is
documented by my own architect's homepage" evidence claims. The plan's
§4c.3 calls them out and demands the actor-side relationship survive
intact. The four spurious edges on `p_resilience_*` cited in the plan
(line 1155) are all present in the journal and confirmed deleted.

**Top 5 Projekte by edges deleted** (from
`deleted/phase4c_3_projekt_actor_registry_belegt.jsonl`):

| Projekt | Edges deleted |
|---|---:|
| `p_circular_pavilion_paris` | 2 |
| `p_crclr_house_impact_hub_berlin` | 1 |
| (full counts available in the journal — 99 Projekte are affected) | … |

**Canonical Cypher:** `migrations/mig_4c_3_detach_projekt_actor_registry_belegt.cypher`.

## Edge strip — `url` / `http` / `source_file` / `external_sources` keys on relationships

**No-op on this run.** Pre-flight probe confirmed:

- `MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http' OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources' RETURN k` → **0 rows**
- Polluted edge count → **0**

**Source of prior work:** Phase 2.7.d executed by Agent 6 canonicalised
4 948 polluted edges and removed legacy `source` / `evidence` /
`source_excerpt` / `datenqualitaet` keys; Agent 7 (Wave-3, edge-pollution
full closure) finished the remaining 319 edges that already carried
`evidence_origin` from upstream agents. The result is a fully clean live
relationship surface — every URL now sits on `:Quelle.url`, and every
relationship carries at most the 5 canonical evidence fields plus its
own structural payload (`rolle_text` and similar domain-specific
typing).

Agent 8's canonical, idempotent re-statement of the strip lives at
`migrations/mig_4c_edge_strip.cypher`. The runner
(`logs/agent8_runner.py`, function `run_edge_strip`) re-implements an
APOC-based per-key strip that is safe to re-run and that writes a
forensic snapshot to `deleted/phase4c_edge_strip.jsonl` before
touching any edge (no snapshot exists this run because nothing was
stripped).

**Hard rule from plan §2.7 / §4c now holds (verified):**
*"no relationship may have a property whose name contains `url`, `http`,
`source_file`, or `external_sources`. URLs exist only on `:Quelle.url`."*

## Phase 4c.2 prep — Dossier manifest for Agent 9

`reports/agent_8_dossier_manifest.json` (97 entries; ~2.9 MB JSON).

| Slice | Count |
|---|---:|
| Total dossier files                                       | **97** |
| `_archive/research/gebaeude/*.md` (German narrative)      | 76 |
| `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/**/*.md` (English tables) | 21 |
| Files matched to a live `:Quelle.quelltyp='case_markdown'` id | 76 / 97 (all gebaeude/*) |
| Files with no live `:Quelle` yet (Agent 9 must MERGE)     | 21 / 97 (all batch2/*) |
| Files with a detectable `## Quellen` / `## Sources` block | 56 / 97 |
| Files without an obvious sources block (Agent 9 may need to parse inline citations) | 41 / 97 |
| Multi-dossier files (concatenated; need per-H1 split)     | **1** (`batch 1.md` → 3 dossiers) |
| Expected-quelle-id collisions (gebaeude ↔ batch2)         | 0 |

> The plan oscillates between "**14**", "**20**" and "**21**" batch2
> dossiers (lines 27 / 1142 / 1224 / 1498). The manifest captures all 21
> markdown files in the batch2 raw_tree (one of which, `batch 1.md`,
> bundles 3 dossiers) plus all 76 gebaeude/* files. Agent 9 / 10 own
> the scope filter; the manifest leaves the choice explicit by tagging
> each entry's `corpus` and `format_hint`.

Per-entry payload (`entries[i]`):

```jsonc
{
  "rel_path": "_archive/research/gebaeude/Holbein_Gardens_London.md",
  "abs_path": "E:\\recherche\\_archive\\research\\gebaeude\\Holbein_Gardens_London.md",
  "size_bytes": 12345,
  "mtime_utc": "2026-05-07T…",
  "sha1": "…",                  // drift detector for Agent 9
  "corpus": "gebaeude",         // "gebaeude" | "batch2"
  "format_hint": "case_markdown",
  "h1_titles": ["Holbein Gardens, London — …"],
  "expected_quelle_id": "q_holbein_gardens_london_md",
  "live_quelle_id": "q_holbein_gardens_london_md",   // null = Agent 9 MERGEs
  "sources_block_kind": "quellen_und_links",         // | "sources" | null
  "sources_block_offset": 8432,                      // byte offset for stream-parse
  "inline_url_count": 17,                            // upper-bound on q_ext_* targets
  "sref_inline_count": 42                            // upper-bound on q_<slug>_sN nodes
}
```

The loader contract hint embedded in the manifest spells out the
canonical `MERGE` pattern Agent 9 should use so the case-markdown S-refs
become `:ZITIERT_QUELLE` children with `evidence_basis='case_markdown_sources'`
(matching the 4c source-link contract laid out in plan §4c).

**Important boundary respected:** Agent 8 did **NOT** parse any dossier
beyond the headers and a regex count of citation markers. The full
`[Sn]` extraction, URL resolution, and `MERGE (q_<slug>_sN)` work
belongs to Agent 9 / 10 per the plan's Phase 4b loader scope.

## Plan acceptance criteria (Agent-8 scope)

- [x] `MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q) = 0` — yes (Agent 6 already executed; Agent 8 re-verified and provides an idempotent canonical script).
- [x] `MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r) = 0` — yes (176 → 0 in one tx).
- [x] `MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r)` invariant — 360 before / 360 after.
- [x] `MATCH ()-[r]->() UNWIND keys(r) AS k WITH DISTINCT k WHERE toLower(k) CONTAINS 'url' OR toLower(k) CONTAINS 'http' OR toLower(k) CONTAINS 'source_file' OR toLower(k) CONTAINS 'external_sources' RETURN k` → empty.
- [x] Phase 4c.2 dossier manifest produced (97 entries; matches live `:Quelle.case_markdown` for the 76 gebaeude entries).
- [x] `PHASE_4C_DONE.flag` and `mig_4c_*.cypher` deliverables in place.

## Reversibility

- **Phase 4c.1 (no-op this run)** — reverse-able via
  `deleted/phase2_7_external_sources.jsonl` (Agent 6's journal). For any
  future re-execution that does touch live data, Agent 8 writes its own
  per-source journal to `deleted/phase4c_1_external_sources.jsonl`
  (empty this run).
- **Phase 4c.3** — `deleted/phase4c_3_projekt_actor_registry_belegt.jsonl`
  carries one JSON line per deleted edge: `projekt_id`, `quelle_id`,
  `quelle_url`, full `rel_props`. Reversal is a parameterised
  `MERGE (p:Projekt {id:$projekt_id})-[r:BELEGT_IN]->(q:Quelle {id:$quelle_id}) SET r += $rel_props`.
- **Edge strip (no-op this run)** — Agent 8 writes a journal at
  `deleted/phase4c_edge_strip.jsonl` for any future execution; the
  snapshot taken before Wave 1 (`snapshot/relationships.jsonl`) is the
  authoritative pre-Phase-2.7 record of legacy edge properties.

## Boundaries respected

- Did **NOT** run Phase 4b (loader rewrite) — Agent 9 / 10 scope.
- Did **NOT** parse any dossier beyond a structural scan (headers, byte
  offset of the sources block, count of inline citation markers).
- Did **NOT** create any new `:Quelle.case_markdown` nodes for the 21
  batch2 dossiers — that's Agent 9's MERGE on first load.
- Did **NOT** alter any of the 319 `:Quelle.quelltyp='external_link_from_actor_registry'`
  target nodes — only Projekt-side BELEGT_IN edges were detached.
- Did **NOT** touch the 360 `(Akteur)-[:BELEGT_IN]->(actor_registry Quelle)`
  edges — those remain the canonical evidence link for actor identity.
- Did **NOT** run any Phase 3 inference.

## Hand-off

### To Agent 9 (Phase 4b loader rewrite)

- Read `reports/agent_8_dossier_manifest.json` first. Each `entries[i]`
  is a self-contained work item with the exact `q_<slug>_md` id you
  must MERGE, a sources-block byte offset for stream-parsing, and an
  inline-citation upper bound for sanity-checking your S-ref extraction.
- The 76 gebaeude dossiers already have a live `:Quelle.case_markdown`
  node. Your loader can MERGE on `expected_quelle_id`; the existing
  panel keys (`id`, `name`, `quelltyp='case_markdown'`, `source_file`,
  `source_scope`, `_archive`) are already in place — do not strip them.
- The 21 batch2 dossiers have no live :Quelle yet. MERGE-create them
  with the same canonical 8-key panel that Phase 2.7 enforces
  (`id`, `name`, `quelltyp='case_markdown'`, `url=null`, `source_file`,
  `access_date`, `title`, `source_scope`).
- For each `[Sn]` in the sources block, MERGE a child
  `q_<slug>_sN:Quelle {quelltyp:'external_reference', url:<extracted>}`
  and a `(q_md)-[:ZITIERT_QUELLE]->(q_sN)` edge with
  `evidence_basis='case_markdown_sources'`, `evidence_origin='derived'`,
  `evidence_source_id='mig_4b'`, `evidence_confidence='unklar'`,
  `evidence_excerpt=<raw bib line>`.
- `batch 1.md` is a multi-dossier file — split on `^# ` before
  generating dossier ids. The H1 titles captured in the manifest
  (`Schärenmoosstrasse Zürich`, `UMAR Unit — NEST, Empa Dübendorf`,
  `ELEMENTA / Walkeweg Basel`) give you the per-dossier slug.
- All 4 c-side invariants Agent 8 enforced (no `external_sources`, no
  Projekt→actor_registry BELEGT_IN, no illegal rel keys) are
  preconditions for your loader. If you reintroduce any of them, the
  Wave-4 acceptance gate fails.

### To Agent 7 (edge-pollution full closure)

- Live count `MATCH ()-[r]->() WHERE (r.source IS NOT NULL OR r.evidence IS NOT NULL OR r.source_excerpt IS NOT NULL OR r.datenqualitaet IS NOT NULL) RETURN count(r)` — Agent 8 did NOT re-execute the strip; if your Wave-3 pass has run, the count is already 0; if not, your scope still applies. Agent 8's edge strip targets a different rule (key-name contains `url`/`http`/`source_file`/`external_sources`), which is independent of the 4-legacy-key pollution Agent 7 owns.

### Acceptance after Agent 9 / 10 (informational, not Agent 8's gate)

- Plan §4c §4c.2 target: **≥ 85 of 96** case-markdown anchors must have
  `size((q)-[:ZITIERT_QUELLE]->()) ≥ 1`. Today (post-Agent-8): 56 / 97
  have an obvious sources block; the remaining 41 will need inline
  citation parsing. Agent 8's `inline_url_count` and `sref_inline_count`
  give Agent 9 an early signal for which dossiers need fallback parsing.

Agent 8 stops here.
