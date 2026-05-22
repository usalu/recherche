# IER-P0 Report — Q03 ERFUELLT_NACHWEIS gate violations

**Agent:** IER-P0  
**Date:** 2026-06-06  
**Database:** `mit-bestand` (read-only)  
**Ledger:** [`ledger/ier_p0.csv`](../ledger/ier_p0.csv)  
**Patch (dry-run only):** [`patches/ier_p0.patch.jsonl`](../patches/ier_p0.patch.jsonl)

---

## Scope recap

12 `P6-new-rel-*` rows with `rel_type_or_label=ERFUELLT_NACHWEIS`, prior `verdict=PROVEN`, empty `proof_quote`, and `basis_type=logic` (Q03 graph additions per P6-06 / F8 UNFIXED cluster).

All rows re-adjudicated via live `read-cypher` (PN/NF endpoints, `primary_source_url` where present) plus `WebFetch` on authoritative URLs.

---

## Verdict summary

| Verdict | Count | Share |
|---|---:|---:|
| PROVEN | 9 | 75% |
| PARTIAL | 3 | 25% |
| **Σ** | **12** | 100% |

**Gate D4:** 12/12 rows now have non-empty verbatim `proof_quote`.  
**Gate D7:** 0 `verdict=PROVEN` with empty `proof_quote` in this shard.

| Metric | Before | After |
|---|---:|---:|
| PROVEN (shard) | 12 | 9 |
| Empty `proof_quote` | 12 | 0 |
| `fetched=true` | 0 | 12 |

---

## Fetch strategy

| Cluster | Rows | URL source |
|---|---:|---|
| Q03 high-confidence PN (`primary_source_url` on graph) | 5 | Graph `pn_*.primary_source_url` → WebFetch |
| Q03 medium-confidence method mappings (no PN URL on graph) | 7 | `evidence_basis` standards + rewire_map hints → WebFetch first-party/regulatory pages |

**URL cache hits:** `schwenk.de` served 2 rows (`pn_petrografie`, `pr_eignungspruefung_baulehm` → `nf_rc_gesteinskoernung_eignung`).

**Fetch failures (no row left unfetched):** `dibt.de` (timeout/404), `gesetze-im-internet.de/ersatzbaustoffv/__5.html` (timeout on retry; quote taken from search snippet + `__4.html` cross-check), `bausubstanz.de` (timeout).

---

## Downgrades (PARTIAL — strict two-endpoint gate G3)

| claim_id | from → to | Why PARTIAL |
|---|---|---|
| `P6-new-rel-231164698737` | `pr_dokumentenpruefung_bestand` → `nf_schadstoffkataster_erkundung` | VDI 6202 names Schadstoff-**Erkundung**, not Dokumentenprüfung |
| `P6-new-rel-231164700106` | `pn_approval_process` → `nf_genehmigungs_oder_zustimmungsbedarf` | EU-Bauprodukteverordnung cites Konformitätserklärung, not DIBt Genehmigungsbedarf |
| `P6-new-rel-231164703326` | `pr_zustandsbewertung` → `nf_dauerhaftigkeit_restlebensdauer` | DIN SPEC 91525 PUC cites Machbarkeitsbewertung, not Restlebensdauer |

---

## Strongest proofs (sample quotes)

1. **EPD → Ökobilanz:** *"Zur Erstellung belastbarer Ökobilanzen werden in der Regel Umweltproduktdeklarationen (EPDs) gemäß DIN EN 15804 herangezogen"* — gebaeudeforum.de
2. **Eignungsprüfung → Ersatzbaustoff-Güte:** *"Der Eignungsnachweis besteht aus der Erstprüfung und der Betriebsbeurteilung"* — ErsatzbaustoffV §5
3. **Ankerprüfung → Befestigungsnachweis:** *"To validate the quality of installation of anchors used on the job, i.e. proof tests"* — Würth/ADM site-test guide (EN 1992-4 context)

---

## Patch proposal

12 × `set_rel_properties` on `ERFUELLT_NACHWEIS` edges (`evidence_url`, `evidence_quote`, `evidence_confidence`, `evidence_basis`, `review_run`).  
**No** `add_rel`, `delete_rel`, or node mutations.

Dry-run: see apply report under `apply_reports/ier_p0.patch.apply_report.md`.

---

## Anomalies

- Seven medium-confidence PN/PR nodes have **no** `primary_source_url` on graph; IER-P0 used regulatory first-party pages aligned with Q03 `evidence_basis` prose.
- `pr_eignungspruefung_baulehm` has two distinct `ERFUELLT_NACHWEIS` targets; each row fetched independently (ErsatzbaustoffV vs DAfStb RC).
- Prior ledger `verdict=PROVEN` on all 12 was a P6-06 synthesis artifact (G07 `RESIDUAL_EMPTY_QUOTE`); three rows correctly downgraded.

---

## Single most important finding

The Q03 high-confidence cluster (5 PN nodes with `primary_source_url`) all upgraded cleanly to **PROVEN** with one fetch each; the residual gate debt was entirely on medium-confidence method mappings where graph nodes lack URLs and quotes must name both proof method and Nachweisforderung — three of seven remain **PARTIAL** under strict G3.

---

*IER-P0 — read-only Neo4j + WebFetch. No graph writes applied.*
