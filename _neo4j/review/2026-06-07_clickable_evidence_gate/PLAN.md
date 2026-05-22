# Clickable Evidence Gate (CEG) — Graph-Wide Plan

**Created:** 2026-06-07 · **Database:** `mit-bestand`
**Goal (verbatim from user):** *"I want to make sure the data in my graph is based on an evidence that the user can click on and see directly."*

This plan supersedes the BG-only hunt for the question of *clickability*. The BG rework
proved the *facts* against local dossiers, but attached **non-matching URLs** — so it does
**not** satisfy this goal yet. See `BASELINE_FINDINGS` below.

---

## 1. The Standard — what "clickable evidence" means

A claim (relationship or node fact) is **`CLICKABLE_VERIFIED`** only if **all** hold:

1. **`evidence_url`** is present and starts with `http(s)://`.
2. **The URL resolves** — HTTP 200 on live fetch, or a working `web.archive.org` snapshot.
3. **The quote is on that page** — the normalized `evidence_quote` appears on the fetched
   page, OR the claim's distinctive anchor tokens (project name **+** the specific
   component/material/actor) verifiably co-occur on the page.
4. **The page is the real source** — a deep link to the listing/case study/article, **not**
   a bare homepage or an unrelated multi-project aggregator.

If 1–4 cannot be met, the claim is **not** clickable and must be labelled honestly
(`UNVERIFIABLE_PUBLIC`) rather than carry a misleading link.

---

## 2. Baseline findings (live graph, measured 2026-06-07)

| Scope | Count | Has http `evidence_url` | Has quote | Clickable+quoted |
|---|---:|---:|---:|---:|
| **All relationships** | 14,571 | 498 | 510 | **498 (3.4 %)** |
| **All nodes** | 2,263 | 326 (`primary_source_url`) | — | 668 have `source_urls` |
| **Projekt nodes** | 83 | **2** | — | 63 have `source_urls` |

**Critical caveat:** of the 498 rels that *do* carry a URL, the BG subset audit showed
only ~5 % actually contain the quote on the page (marketplace domains like `rotordb.org`,
`opalis.eu` are genuine; BG dossier edges got bogus homepage/aggregator URLs). So even the
498 must be re-validated, not trusted.

**Conclusion:** today **< 3.4 %** of the graph meets the user's bar. This is a graph-wide
gap, not a BG-only gap.

---

## 3. Edge classification (evidence policy by type)

Not every edge can or should carry its own external link. Three tiers:

### Tier 1 — Empirical claims (MUST have own clickable evidence)
Project/actor/component facts that assert something about the real world.
`VERBUNDEN_MIT_AKTEUR` (159), `NUTZT_MATERIAL` (497), `HAT_BAUTEILTYP` (681),
`BETEILIGT_AN` (499), `AUS_SPENDER` (198), `HAT_BAUWERK` (180), `HAT_KENNWERT` (255),
`HAT_BAUTEILGRUPPE` (364), `HAT_MATERIALGRUPPE` (403), `ERFUELLT_NACHWEIS` (140),
`HAT_DEFEKT` (57) — **plus node facts** on `:Projekt`, `:Akteur`, `:Bauteilgruppe`,
`:Bauwerk`.

### Tier 2 — Derived / taxonomy (inherit evidence transitively)
Classification of an entity into a controlled node. Clickable-verified **iff** the parent
entity (Projekt/Akteur) has a Tier-1-verified source page that names the entity.
`LIEGT_IN_LAND` (633), `LIEGT_IN_STADT` (236), `HAT_NUTZUNG` (228), `HAT_INTERVENTION` (144),
`HAT_PROZESSPHASE` (679), `HAT_AKTEURTYP` (680), `HAT_AKTEURROLLE` (1459),
`HAT_BESCHAFFUNGSWEG` (591), `HAT_LOGISTIK` (434), `HAT_RUECKBAUVERFAHREN` (308), …

### Tier 3 — Ontology / controlled vocabulary (definitional, exempt + labelled)
Domain-knowledge edges, true by definition, not project-specific.
`TYPISCH_BEI_MATERIAL`, `TYPISCH_BEI_BAUTEILTYP`, `IST_UNTERVERFAHREN_VON`,
`ERFORDERT_NACHWEIS` (1542), `TRIGGERS_REGULIERUNGSFRAGE` (1101),
`GESTUETZT_AUF_REGELWERK` (167) where they encode regulation logic.
Stamped `evidence_class = "ontology"` so the user can see they are intentionally exempt.

> The exact tier of each rel type is finalized in **Phase 0** with the user before any write.

---

## 4. Schema convention (added to every claim)

| Property | Values |
|---|---|
| `evidence_status` | `CLICKABLE_VERIFIED` · `INHERITED_VERIFIED` · `LINK_DEAD` · `QUOTE_MISMATCH` · `HOMEPAGE_ONLY` · `UNVERIFIABLE_PUBLIC` · `ONTOLOGY_EXEMPT` |
| `evidence_url` | deep link only; set **only** when fetched-and-matched |
| `evidence_quote` | verbatim text confirmed present on the page |
| `evidence_checked_at` | ISO timestamp of last successful validation |
| `evidence_class` | `empirical` · `derived` · `ontology` |

---

## 5. The cornerstone — a deterministic validator (the "gate")

`_scripts/verify_clickable_evidence.py` — this is what *guarantees* the goal:

- Input: every claim with an `evidence_url` (and every Tier-1 claim, to flag missing URLs).
- For each: fetch URL (live, then `web.archive.org` fallback), normalize page text,
  test quote-on-page + anchor-token co-occurrence, detect homepage/aggregator.
- Output per claim: one `evidence_status` + reason.
- Emits `CLICKABLE_EVIDENCE_BASELINE.csv` (truth ledger) and rejects any patch that would
  write an `evidence_url` failing the check.
- Runs as a **regression gate** in every later phase — nothing is "verified" unless this
  script says so on a live fetch.

---

## 6. Phases

### Phase 0 — Standard & policy sign-off
Finalize tier assignment per rel type; lock the validator spec; agree the status taxonomy.
*Deliverable:* `CLICKABLE_EVIDENCE_STANDARD.md`.

### Phase 1 — Full inventory (validate what exists)
Run the validator over all 498 URL-bearing rels + 326 URL-bearing nodes. Produce the
honest baseline: how many are truly clickable, dead, mismatched, or homepage-only.
*Deliverable:* `CLICKABLE_EVIDENCE_BASELINE.csv` + summary.

### Phase 2 — Fix the URL-generator bug
Patch `bg_hunt_common.py` / `_bg_hunt_rework_orchestrate.py`: **never** attach a geo/homepage
URL to a dossier-sourced quote. A URL is written only when the validator confirms the quote
is on that exact page. Regenerate the 473-op BG patch under the new rule (most will drop
their URL or move to web-hunt).

### Phase 3 — Resolve dossier-backed claims to public sources
For every dossier-proven claim (the 162 + most of the 311), trace the project's real public
source: `source_urls` list (63 projects have one), dossier `external_sources`, or the case
study's origin. Fetch, run the validator, promote to `CLICKABLE_VERIFIED` only on pass.
Claims whose underlying source is a private case document → `UNVERIFIABLE_PUBLIC`.

### Phase 4 — Web hunt for unsourced Tier-1 claims
Proper search ladder (marketplace listing → case study → named external source → archive.org)
for Tier-1 claims with no clickable source. Validator-gated. No homepage acceptance.

### Phase 5 — Tier-2 transitive verification
For each derived edge, confirm the parent Projekt/Akteur has a Tier-1 `CLICKABLE_VERIFIED`
source page that names the entity; stamp `INHERITED_VERIFIED` + carry the parent URL.

### Phase 6 — Write-back, enforcement, dashboard
Apply only validator-passed patches. Stamp `evidence_status` on **every** edge/node.
Re-run validator as regression. Deliver:
- `CLICKABLE_EVIDENCE_FINAL_REPORT.md` (coverage by tier),
- a Cypher **"clickable-only view"** so the user can query the graph showing *only*
  `CLICKABLE_VERIFIED` / `INHERITED_VERIFIED` data.

---

## 7. Honesty rules (non-negotiable)

1. A URL is written **only** if the validator confirms the quote is on that page, live.
2. Bare homepages and unrelated aggregators are **never** accepted as evidence.
3. Local dossier files are **not** clickable evidence — they must resolve to a public URL
   or the claim is marked `UNVERIFIABLE_PUBLIC`.
4. Claims that cannot be publicly verified are **labelled, not deleted** (user decides
   keep/hide via the clickable-only view).
5. Every "verified" status is reproducible by re-running the validator.

---

## 8. Open decisions for the user

- **D1 — Unverifiable claims:** keep with `UNVERIFIABLE_PUBLIC` label (filterable), or delete?
- **D2 — Tier-2 depth:** stamp all derived edges transitively, or only verify Tier-1 first?
- **D3 — Archive fallback:** is a `web.archive.org` snapshot acceptable as "clickable"?
- **D4 — Scope order:** whole graph at once, or Tier-1 empirical claims first (highest value)?
