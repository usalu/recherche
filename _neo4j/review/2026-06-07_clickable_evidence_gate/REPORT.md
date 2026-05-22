# Clickable Evidence Gate — Phase 1 + 2 Report

**Date:** 2026-06-07 · **DB:** `mit-bestand`
**Goal:** every fact in the graph should rest on evidence the user can **click and see directly.**
**Status:** investigation + proposals complete. **Nothing applied. No edges or data deleted.**

---

## 1. What was built

`_scripts/verify_clickable_evidence.py` — a deterministic **gate** that, for any claim with a
URL, fetches the page **live** and checks the stored quote is actually on it. This is the
mechanism that makes the guarantee reproducible: a fact is "verified" only if this script
confirms it on a live fetch. A disk cache (`_fetch_cache.json`) makes re-runs fast.

The gate was tuned against **ground truth** (pages were read by hand) so it neither
over-passes homepages nor over-fails strong deep links. Verdict scale:
- **VERBATIM / STRONG** → `CLICKABLE_VERIFIED` (quote shown on page)
- **WEAK** → `LIKELY_REVIEW` (deep page, partial — keep + review)
- below → `QUOTE_MISMATCH` / `HOMEPAGE_ONLY` / `LINK_DEAD`

---

## 2. Baseline — the honest state of the graph

824 of the graph's claims carry a URL (498 relationships + 326 nodes). Live-checked:

| status | count | clickable? |
|---|---:|---|
| CLICKABLE_VERIFIED | 530 | ✅ |
| ENTITY_HOMEPAGE | 118 | ✅ (node → its own org homepage) |
| LIKELY_REVIEW | 52 | ⚠️ partial |
| QUOTE_MISMATCH | 81 | ❌ |
| HOMEPAGE_ONLY | 26 | ❌ |
| LINK_DEAD | 17 | ❌ (8 bot-blocked, likely fine for humans) |

- **Click-safe today: 648.** **Clear-bad: 124.**
- **Whole graph:** 16,834 elements; only **648 (3.9 %)** are clickable. ~16,000 elements
  (mostly taxonomy edges) carry **no link at all** — Phase 3–5 territory.

By layer:
- **Actors & regulation** (`VERBUNDEN_MIT_AKTEUR` 149/159, `BETEILIGT_AN` 54/61,
  `ERFORDERT_NACHWEIS` 15/15): strong — real marketplace / regulation pages.
- **Component catalogue** (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`): the weak spot — facts proven
  against **local dossiers** but stapled to homepage/aggregator URLs.

---

## 3. Phase 2a — stamp + strip (PROPOSAL, not applied)

`patches/ceg_status_and_strip.patch.jsonl` — 892 ops, dry-run clean:
- **824 stamps** of `evidence_status` so you can filter the graph to click-safe data.
- **68 strips** of `evidence_url` from relationships whose link does **not** show the fact
  (the quote is kept — only the misleading link is removed).
- **Never strips nodes** (actor/entity homepages are valid) and **deletes nothing**.

> Held per your instruction. This changes only properties; it removes **no edges**.

---

## 4. Phase 2b — gate-validated re-hunt (PROPOSAL, not applied)

For the 115 clear-bad claims (excluding 9 bot-blocked) the re-hunt searched endpoint
`source_urls`, connected-project sources, and DuckDuckGo, then **re-validated each candidate
with the gate** — a URL is proposed only when the quote is truly on that page.

`patches/ceg_rehunt_recovered_links.patch.jsonl` — **7 recovered** (dry-run clean):

| claim | recovered clickable URL |
|---|---|
| Carla Ferrando / Pablo Garrido (VERBUNDEN_MIT_AKTEUR) | beta-architecture.com/elementa-parabase… |
| Bauteilbörse Hannover | restado.de/profil/bauteilboerse-hannover |
| Michel Massmünster | park-books.com/produkt/bauteile-wiederverwenden |
| Eike Roswag-Klinge | nbl.berlin/persons/prof-eike-roswag-klinge |
| Anders Lendager | circularmaterialsystems.com/…/resource-rows |
| Andrea Klinge | zrs.berlin/…/be-ware |

**108 still unverified:**
- **30** have **no discoverable public source** (no endpoint URLs; web search returned nothing).
- **78** had candidate pages, but the **specific quote is not verifiably on them**.

**All 7 recoveries are actors/people.** Web search works for named people/orgs; it does **not**
recover the granular component-catalogue facts.

---

## 5. The core finding

There are two evidence regimes in this graph:

1. **Publicly verifiable** — actors, organisations, regulation, marketplace listings. These
   can be made click-and-see. Mostly already are; the rest are recoverable (see the 7).
2. **Dossier-derived** — the `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` component facts. These were
   curated from project case documents (`.kg.jsonl`), many of which have **no public deep
   page** that lists components per project. For these, a clickable public link often does
   **not exist** — the honest label is `UNVERIFIABLE_PUBLIC`, not a faked URL.

**Nuance worth acting on:** some `QUOTE_MISMATCH` are *adequate* pages where our *synthesized*
quote simply isn't literal (e.g. La Ressourcerie's `/les-matériaux` really does list windows/
wood/doors). These are salvageable by **replacing the stored quote with an actual on-page
sentence**, then re-running the gate — a worthwhile Phase 3 step.

---

## 6. Recommendation (your call — nothing applied)

1. **Apply 2a stamps** so you can immediately query click-safe data (no deletes).
2. **Apply the 7 re-hunt recoveries** (gate-proven).
3. **Phase 3 (quote-repair):** for the ~78 candidate-but-mismatch cases, swap synthesized
   quotes for real on-page sentences and re-validate — likely recovers a meaningful share of
   the marketplace/ressourcerie component claims.
4. **Decide the dossier-derived component facts** (the `decide_later` set): keep with an
   `UNVERIFIABLE_PUBLIC` label (filtered out of the click-safe view), or hide them.

### A "click-safe only" view (once 2a is applied)
```cypher
MATCH (a)-[r]->(b)
WHERE r.evidence_status IN ['CLICKABLE_VERIFIED']
RETURN a, r, b
```

---

## 7. Artifacts
- `_scripts/verify_clickable_evidence.py` — the gate.
- `CLICKABLE_EVIDENCE_BASELINE.csv` — per-claim status/score/http/quote.
- `BASELINE_FINDINGS.md` — baseline detail.
- `REHUNT_LEDGER.csv` — re-hunt outcome per claim.
- `patches/ceg_status_and_strip.patch.jsonl` — 2a stamp+strip (proposal).
- `patches/ceg_rehunt_recovered_links.patch.jsonl` — 7 recoveries (proposal).
- `PLAN.md` — full 6-phase plan.
