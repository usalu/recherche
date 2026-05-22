# Final Cleanup F03 — Q01/Q02 merge-redirect re-proof (triples 11–19)

**Agent:** F03 · **Date:** 2026-06-06 · **Database:** `mit-bestand` (read-only)
**Plan:** [`VERIFICATION_PLAN_7_AGENTS_FINAL_CLEANUP.md`](../VERIFICATION_PLAN_7_AGENTS_FINAL_CLEANUP.md) §4 F2 SCOPE_CYPHER triples 11–19
**Ledger:** [`ledger/final_cleanup_f03.csv`](../ledger/final_cleanup_f03.csv)

## 1. Scope

Re-adjudicate **9** merge-redirect relationships that P6-06 synthesized as `P6-new-rel-*` rows with `basis_type=logic`, empty `proof_quote`, and `fetched=false` — an Evidence Gate violation.

| Cluster | Count | Redirect origin |
|---|---:|---|
| `bt_fassade` regulation edges | 2 | Q01 merges (`bt_mauerstein`, `bt_fassadenelement`, …) |
| `bt_fenster` regulation edges | 4 | Q01 merges (`bt_verglasung`, `bt_glasscheibe`) |
| `mat_glas` regulation edges | 2 | Q01 merge (`mat_drahtglas`) |
| `p_timber_square_london` HAT_BAUWERK | 1 | Q02 merge (`bw_externe_stahl_donor_stockholder` → `bw_cleveland_steel_and_tubes_stock`) |
| **Σ** | **9** | |

All 9 edges confirmed live via SCOPE_CYPHER `read-cypher` on 2026-06-06.

## 2. Verdict summary

| Verdict | Count | Share |
|---|---:|---:|
| **PROVEN** | **9** | 100% |
| PARTIAL | 0 | — |
| UNVERIFIABLE | 0 | — |

**Evidence Gate compliance:** 9/9 rows have non-empty `proof_quote`; 9/9 external bases have `fetched=true` and `http_status=200`. No `basis_type=logic` with empty quote remains in this shard.

## 3. Method

1. **Live graph** — `read-cypher` SCOPE_CYPHER triples 11–19; read `source_url` / `source_quote` on regulation edges.
2. **Re-fetch** — 3 unique URLs (reclaimed-brick blog, glassonweb IGU paper, baunormenlexikon DIN 18008-4; stockmatcher case study for geo edge).
3. **Regulation class** — cite live `source_url` + verbatim page excerpt supporting the specific `Nachweisforderung` / `Regulierungsfrage` target (per plan §3 and Agent 07 precedent).
4. **Geo HAT_BAUWERK** — stockmatcher case study names both **Timber Square** project and **Cleveland Steel and Tubes** as reclaimed-steel supplier; depot endpoint independently sourced at `cleveland-steel.com` (R01).

## 4. Per-item outcomes

| claim_id | Edge | Prior synthetic row | Verdict | Basis |
|---|---|---|---|---|
| F03-rel-011 | `bt_fassade` → `nf_materialpruefung` | P6-new-rel-831955132850 | PROVEN | EN 771-1 third-party testing quote |
| F03-rel-012 | `bt_fassade` → `rf_tragwerkssicherheit_frage` | P6-new-rel-731280445874 | PROVEN | structural/non-structural reuse framework quote |
| F03-rel-013 | `bt_fenster` → `nf_materialpruefung` | P6-new-rel-831955132851 | PROVEN | IGU property assessment for reuse |
| F03-rel-014 | `bt_fenster` → `nf_sicherheitsglas_info` | P6-new-rel-631768818099 | PROVEN | DIN 18008-4 §4.1 Sicherheitsglas requirement |
| F03-rel-015 | `bt_fenster` → `nf_absturzsicherung` | P6-new-rel-431582503347 | PROVEN | DIN 18008-4 title/scope (absturzsichernde Verglasungen) |
| F03-rel-016 | `bt_fenster` → `rf_tragwerkssicherheit_frage` | P6-new-rel-931466760627 | PROVEN | DIN 18008-4 §6.1 static/impact proofs |
| F03-rel-017 | `mat_glas` → `nf_absturzsicherung` | P6-new-rel-631768818199 | PROVEN | DIN 18008-4 Anwendungsbereich absturzsichernd |
| F03-rel-018 | `mat_glas` → `rf_tragwerkssicherheit_frage` | P6-new-rel-931466760727 | PROVEN | DIN 18008-4 §6.1 static/impact proofs |
| F03-rel-019 | `p_timber_square_london` → `bw_cleveland_steel_and_tubes_stock` | P6-new-rel-930303702695 | PROVEN | Stockmatcher: Cleveland S&T supplier, 115 t reclaimed steel |

## 5. Notable findings

1. **Q01 regulation redirects inherit valid edge properties** — all 8 regulation survivors carry non-null `source_url` / `source_quote` from pre-merge nodes (Agent 07 evidence); re-fetch confirms quotes.
2. **Q02 HAT_BAUWERK upgrade** — prior ledger `09-hat_bauwerk-1013` was PARTIAL (unsourced aggregate depot). Post-Q02 redirect to R01-sourced `bw_cleveland_steel_and_tubes_stock` plus Stockmatcher case study yields PROVEN with both endpoints named.
3. **No graph mutations** — read-only pass; optional follow-up: add `evidence_url` / `role=donor` on HAT_BAUWERK edge via human-gated patch (not applied).

## 6. Residual / out of scope

- F2 triples 1–10 (remaining 10 redirect rels) — owned by parallel F2 shard → `ledger/final_cleanup_f02.csv`.
- F3 canonical scope (18 actors + 8 Tracimat rels + 1 VMA) — separate work item per plan §4 F3; **not** included in this 9-row shard.

## 7. Outputs

| File | Rows |
|---|---:|
| `ledger/final_cleanup_f03.csv` | **9** |
| `reports/final_cleanup_f03.md` | this report |

**Row count check:** 9 = scope target ✓
