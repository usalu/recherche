# Swiss reuse bubble — evidence sidecar

Off-graph evidence dossier for intake `2026-06-05_swiss_reuse_bubble`.  
Graph relationships carry **Tier 1** pointers; full provenance lives here.

## Three-tier model

| Tier | Location | Contents |
|------|----------|----------|
| **1 — Graph** | Neo4j rel properties | `evidence_quote` (≤240), `evidence_confidence`, `evidence_url`, `evidence_claim_ids`, `metadata_sidecar_key` |
| **2 — Claims** | `claims.jsonl` | Atomic facts with dossier section, corroborating URLs, verbatim excerpt |
| **3 — Captures** | `url_captures.jsonl` | Per-URL fetch record (`capture_method`, `captured_at`, verbatim quote) |

Interpretive conclusions (`fact_label: Interpretive_conclusion`) are stored in the sidecar **only** — they may inform `teilweise_belegt` edges but are not stated as sourced facts.

## Files

| File | Rows | Purpose |
|------|------|---------|
| `claims.jsonl` | 30 claims | Atomic evidence units (Fact vs Interpretive) |
| `url_captures.jsonl` | 37 URLs | Verbatim excerpts + capture metadata |
| `edge_evidence.jsonl` | 1 per `add_rel` | Full claim chain per patch relationship |
| `manifest.json` | — | Run metadata and counts |

Human index: [`../CLAIM_INDEX.csv`](../CLAIM_INDEX.csv) (rel ↔ claim matrix).

## Lookup workflow

1. Read `metadata_sidecar_key` on a relationship in Neo4j (after apply).
2. Find the row in `edge_evidence.jsonl`:

```powershell
Select-String -Path edge_evidence.jsonl -Pattern "r_cirkla__verbunden_mit_akteur__useagain_bauteilclick"
```

3. Follow `evidence_claim_ids` into `claims.jsonl` for corroborating sources and dossier section.
4. Follow `primary_source_id` into `url_captures.jsonl` for verbatim page text.

## Example claim chain (Gruner → Basel → useagain)

```
claim_gruner_basal_useagain_chain
  primary: q_url_18e12ef… (gruner.ch news)
  corroborates: q_url_9fce1894… (library-of-reuse)
  dossier: §6
  rels: r_gruner_reuse__verbunden…, r_bauteilboerse_basel…, r_useagain…
```

## Regenerate

```powershell
cd _neo4j/intake/runs/2026-06-05_swiss_reuse_bubble
python _build_evidence_layer.py
```

Edits to claims: `_evidence_claims.py` → rebuild patches + sidecar.
