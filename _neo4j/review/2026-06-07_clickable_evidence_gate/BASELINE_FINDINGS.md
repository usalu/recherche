# Clickable Evidence — Phase 1 Baseline Findings

**Run:** 2026-06-07 · **DB:** `mit-bestand` · **Validator:** `_scripts/verify_clickable_evidence.py`
**Method:** every claim carrying an http URL was fetched **live**; the stored quote +
the claim's anchor tokens were checked against the actual page text. Live pages only
(no archive.org fallback, per decision).

## Headline (refined, ground-truthed gate)

Of the **824 claims that carry a URL** (498 relationships + 326 nodes):

| evidence_status | count | % | clickable? |
|---|---:|---:|---|
| **CLICKABLE_VERIFIED** | 530 | 64.3 % | yes — quote shown on page |
| **ENTITY_HOMEPAGE** | 118 | 14.3 % | yes — node → its own org homepage |
| LIKELY_REVIEW | 52 | 6.3 % | maybe — deep page, partial match (keep+review) |
| QUOTE_MISMATCH | 81 | 9.8 % | **no** — fact not on page |
| HOMEPAGE_ONLY | 26 | 3.2 % | **no** — rel → bare homepage |
| LINK_DEAD | 17 | 2.1 % | **no** (8 are bot-blocks, likely fine for humans) |

**Acceptable to click today: 648** (verified + entity homepage). **Clear-bad: 124.**

**Against the whole graph** (14,571 rels + 2,263 nodes = 16,834 elements):
**648 clickable = 3.9 %.** Most of the graph simply has no URL at all.

### Gate was first too strict — fixed and ground-truthed
The initial pass flagged 211 failures. Spot-fetching showed ~87 were false alarms:
- `la-ressourcerie.ch/les-matériaux` (score 0.83) genuinely lists `window`, `bois`, `porte` → recovered.
- Actor homepages (`cleveland-steel.com`, `drz-wien.at`, `circularhub.ch`) are valid "see the actor" links → `ENTITY_HOMEPAGE`.
- True failures confirmed by fetch: `lendager.com/projects/upcycle-studios` (no components on page),
  `circularhub.ch/magazin/.../sumami` (empty page). These stay flagged.

The gate now: **VERBATIM** (quote fragment on page) or **STRONG** (≥60 % of distinctive
quote words, ≥3 absolute) ⇒ verified. Partial ⇒ review. Below that ⇒ mismatch.

## Relationships (498 with URL)

| rel type | verified / total | mismatch | homepage | dead |
|---|---:|---:|---:|---:|
| VERBUNDEN_MIT_AKTEUR | 149 / 159 | 10 | 0 | 0 |
| HAT_BAUTEILTYP | 80 / 133 | 29 | 19 | 5 |
| NUTZT_MATERIAL | 56 / 97 | 25 | 13 | 3 |
| BETEILIGT_AN | 54 / 61 | 7 | 0 | 0 |
| ERFUELLT_NACHWEIS | 19 / 24 | 5 | 0 | 0 |
| ERFORDERT_NACHWEIS | 15 / 15 | 0 | 0 | 0 |
| TRIGGERS_REGULIERUNGSFRAGE | 7 / 7 | 0 | 0 | 0 |

- **Strong:** actor edges (`VERBUNDEN_MIT_AKTEUR`, `BETEILIGT_AN`) and regulation edges
  point at real marketplace listings / regulation pages and pass.
- **Weak:** the BG catalogue (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`) — exactly the dossier-quote
  + homepage-URL problem already identified. 77 + 32 + 8 of these fail.

## Nodes (326 with primary_source_url)

232 verified · 36 mismatch · 49 homepage-only · 9 dead. Node names usually appear on
their source page, so node URLs verify better than rel quotes.

## Dead links — nuance (17 total)

| http | count | meaning |
|---|---:|---|
| 404 | 5 | truly gone — must re-source |
| 403 / 401 / 503 | 9 | **bot-blocked** — page likely fine for a human, our fetcher refused |
| conn error | 3 | DNS/timeout — recheck |

Only **5 are genuinely 404**. The 9 blocked ones (CBRE, gladsaxe.dk, utrecht.nl, deerns…)
need a manual/headless recheck before being called dead.

## Homepage-only (81)

URLs like `marketplace.skop.app/`, `cornermat.be/`, `useagain.ch/`, `awm.stadt-muenster.de/`
are root pages — clickable but they don't *show the specific fact*. These need a deep link
to the actual listing/case study.

## What this means for the goal

- **613 facts** already meet your bar (clickable + the page shows the fact). The actor and
  regulation layers are in good shape.
- **211 facts carry a misleading or shallow link** (mismatch + homepage + dead) — these are
  the ones that would embarrass you if clicked. Concentrated in the BG catalogue.
- **~16,000 facts have no link at all** — mostly taxonomy edges (Tier-2/3) plus dossier-only
  empirical claims. These are the bulk of the work in Phases 3–5.

## Phase 2a patch (built, dry-run clean — NOT yet applied)

`patches/ceg_status_and_strip.patch.jsonl` — **892 ops**, dry-run `load_errors: 0`:
- **824 stamps** — writes `evidence_status` + `evidence_checked_at` on every URL-bearing
  claim, so the graph can be filtered to clickable data immediately.
- **68 strips** — removes `evidence_url` from relationships that are `QUOTE_MISMATCH` /
  `HOMEPAGE_ONLY` / truly-dead. The quote is kept; only the misleading link is removed.
- **9 NEEDS_RECHECK** — bot-blocked dead links kept (likely fine for a human).
- **Nodes are never stripped** here — entity/actor homepages are valid click-and-see links.

Apply with: `python _scripts/apply_neo4j_review_patch.py --patch <patch> --confirm <token>`.

## Artifacts
- `CLICKABLE_EVIDENCE_BASELINE.csv` — per-claim status, score, http code, quote, eid.
- `_fetch_cache.json` — cached normalized pages (fast re-scoring without re-fetching).
- `_analyze_baseline.py` — regenerates the breakdown tables.
- `patches/ceg_status_and_strip.patch.jsonl` — the Phase 2a stamp+strip patch.
