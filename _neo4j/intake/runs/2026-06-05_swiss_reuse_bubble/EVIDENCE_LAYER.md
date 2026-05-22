# Evidence layer specification

> **DEPRECATED (2026-06-06):** Evidence lives on graph node/rel properties only. See [`sidecar/DEPRECATED.md`](sidecar/DEPRECATED.md).

**Run:** `2026-06-05_swiss_reuse_bubble`  
**Dossier:** `swiss_reuse_bubble_v2.md` (Fact vs Interpretive labels preserved)

## Design (historical)

The intake originally used a **three-tier evidence stack** — superseded by graph-only properties.

```text
Tier 3  url_captures.jsonl     verbatim page text + fetch metadata
           ↑
Tier 2  claims.jsonl            atomic Fact / Interpretive units + corroboration
           ↑
Tier 1  Neo4j relationships     short quote, confidence, sidecar pointer
```

## Tier 1 — Graph relationship properties

Required on every `add_rel`:

| Property | Rule |
|----------|------|
| `evidence_url` | Primary first-party URL |
| `evidence_quote` | ≤240 chars; from `quote_short` of primary claim |
| `evidence_excerpt` | ≤500 chars; verbatim from `quote_verbatim` (sidecar-redundant but speeds Browser audit) |
| `evidence_confidence` | `belegt` \| `teilweise_belegt` |
| `evidence_source_id` | Primary `:Quelle` id |
| `evidence_basis` | Machine basis code |
| `evidence_origin` | `live_url_capture` \| `dossier_anchored` |
| `evidence_claim_ids` | List of claim ids (JSON array on graph) |
| `secondary_evidence_source_ids` | Corroborating `:Quelle` ids when present |
| `dossier_section` | e.g. `§2.3` from research doc |
| `fact_label` | `Fact` or `Interpretive_conclusion` |
| `metadata_sidecar_key` | `rel:{TYPE}:{from}->{to}` |

`Interpretive_conclusion` edges use `teilweise_belegt` and must not paraphrase conclusions as direct quotes.

## Tier 2 — Atomic claims (`sidecar/claims.jsonl`)

30 claims covering:

- Cirkla network / directory / committee (§2)
- K.118 / ELYS participation (§4)
- Marketplace supply chain (§5–6)
- Tools & programs (§8–9)
- Coordination actors (§10) — **Interpretive** where no direct partnership URL

Each claim record:

```json
{
  "claim_id": "claim_gruner_basal_useagain_chain",
  "label": "Fact",
  "dossier_section": "§6",
  "statement": "...",
  "primary_url": "...",
  "primary_source_id": "q_url_...",
  "corroborating_source_ids": ["q_url_..."],
  "quote_verbatim": "...",
  "quote_short": "...",
  "confidence": "belegt",
  "capture_method": "live_fetch_2026_06_05"
}
```

## Tier 3 — URL captures (`sidecar/url_captures.jsonl`)

One row per registered URL with:

- `capture_method`: `live_fetch_2026_06_05` | `dossier_register`
- `captured_at`: ISO timestamp
- `quote_verbatim` / `quote_short`

Live-fetched pages (2026-06-05): Cirkla homepage/association/publications, Zirkular K.118/legal framework, Gruner news, library-of-reuse, ETH reuse page (Sumami→useagain **upgraded to belegt**), C33 homepage.

## Corroboration policy

| Actor type | Minimum `BELEGT_IN` URLs |
|------------|--------------------------|
| Bauteilbörse / marketplace | 2+ first-party (directory + operator site) |
| Program / Software | 1 primary + dossier cross-ref |
| Coordination actor | 1 homepage; ecosystem edges `teilweise_belegt` |

Phase 1 adds corroborating `BELEGT_IN` for: useagain (×2), salza, materiuum, bauteilladen, wick, sumami.

## Confidence upgrades in this layer

| Edge | Was | Now | Reason |
|------|-----|-----|--------|
| sumami ↔ useagain | teilweise_belegt | **belegt** | ETH page: "they are developing useagain- the Swiss brokerage and sales platform" |
| Cirkla ↔ Zirkular | teilweise_belegt | teilweise_belegt | Claim marked `Interpretive_conclusion`; no direct partnership URL |

## Files to regenerate together

```text
_evidence_claims.py          # edit claims / edge map
_build_evidence_layer.py     # rebuild sidecar + patches
CLAIM_INDEX.csv              # human rel↔claim matrix
patches/*.patch.jsonl        # enriched Tier-1 properties
```

## QA queries (post-apply)

```cypher
// Every bubble edge must have claim ids and sidecar key
MATCH ()-[r]->()
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN count(r) AS total,
       sum(CASE WHEN r.evidence_claim_ids IS NULL THEN 1 ELSE 0 END) AS missing_claims,
       sum(CASE WHEN r.metadata_sidecar_key IS NULL THEN 1 ELSE 0 END) AS missing_sidecar;

// Interpretive edges explicitly tagged
MATCH ()-[r]->()
WHERE r.fact_label = 'Interpretive_conclusion'
RETURN r.id, r.evidence_confidence, r.dossier_section;
```
