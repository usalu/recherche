# State review — everything so far, one place

A review of the whole effort and its current, internally-consistent state. Nothing is written to
`mit-bestand` yet. All numbers below are from the latest re-run (pipeline validates 100% clean).

## Mission
Replace the weak, generically-connected regulation vocabulary with a clean, **evidence-backed**
layer, connect it to the real graph anchors, then critically decide what of the old graph to keep,
rewire, or delete — *quality over quantity, evidence not generic.*

## What exists now (built + validated)

**New evidenced vocabulary** (`vocab_nodes.jsonl`, `vocab_edges.csv`):
- 11 `Regulierungsfrage`, 33 `Nachweisforderung`, **91 `Regelwerk`** (each web-researched, with URL+quote)
- **601 backbone edges**: GILT_IN_LAND 281, GESTUETZT_AUF_REGELWERK 169, ERFORDERT_NACHWEIS 94, BETRIFFT_MATERIAL 39, BETRIFFT_BAUTEILTYP 18
- 8 link directly to live nodes (`bps_nta_8713`, `rb_eu_taxonomie`, `s_radon`, `s_schimmel`, `norm_nen_8700`…)

**Anchor connections** (`anchor_edges.csv`) — derived from *factual* attributes, evidenced, never Huerde/Norm:
- **3 729 edges across ~363 anchors**: TRIGGERS_REGULIERUNGSFRAGE, ERFORDERT_NACHWEIS, UNTERLIEGT_REGELWERK
- Gated by: material (`NUTZT_MATERIAL`) + load-bearing (`tragend`) + component type (`HAT_BAUTEILTYP`) +
  composite handling; project by **context** (`HAT_INTERVENTION`/phase/use/era), not just country;
  national rules filtered to the component's country.
- Audit: **0 jurisdiction mismatches, 0 structural-on-non-loadbearing, 0 bad targets, confidence ∈(0,1].**

**Rewire of the 7 old labels** (`rewire_map.csv`, all 341 nodes mapped):
- REWIRE→Regelwerk 123 · KEEP+wire methods 120 · REWIRE→Nachweis/Frage 46 · DELETE regulatory-Huerde 17
  · KEEP+wire Schadstoff 13 · KEEP market-Huerde 11 · KEEP status-enums 3 · gaps/out-of-scope 8.

## The evidence verdict (the heart of it)
- **The old mission layer is generic, not evidenced** — by its own metadata: `HAS_RISK_POLLUTANT`
  confidence=`inferiert`, `HAT_LEISTUNGSANFORDERUNG`=`unklar` (all 452), `REQUIRES_VERIFICATION_FOR`
  331/339 `material_only`; **0** of the 7 labels reach a real http source.
- **Internet research proves the knowledge is real and citable** — but only as *rules*: pollutant×era
  (LfU Bayern Arbeitshilfe, LABO, polludoc, allum), test×material/era (SCI P427, EN 13791), barriers
  (FCRBE/academic). See `POLLUTANT_ERA_EVIDENCE.md`.
- **Therefore deletion of the generic edges is not loss** — the same knowledge is re-expressed,
  sourced, through the overlay (now incl. `rw_lfu_schadstoff_arbeitshilfe`).

## Final cleanup decision (rescue-informed)
| Old label | Decision | Why |
|---|---|---|
| **Schadstoff** | KEEP nodes + `TYPISCH_BEI_ERA` (now cited); replace generic edges | real substances; era-rules sourced |
| **PruefungNachweis** | KEEP methods (dedup `pn_/pr_`, name); replace generic `HAT_PRUEFUNG` | real test methods |
| **Leistungsanforderung** | KEEP slim (consolidate fire/thermal dups); derive assignment | real requirements |
| **Norm** | **DELETE** → Regelwerk | duplicated (EN1090 ×5), 0 evidence; replaced by sourced Regelwerk |
| **RechtlicheBedingung** | **DELETE** → Regelwerk/Frage | tiny use, full overlap |
| **Bauproduktstatus** | keep 3 status enums; replace rest → Regelwerk; drop US/JP | conformity routes = Regelwerke |
| **Huerde** | regulatory half **DELETE**; market half = your call (A delete / B research-rescue) | only market barriers have a real-data lifeline |

## Documents (reading order)
1. `STATE_REVIEW.md` (this) — overview.
2. `REVIEW.md` — simple sign-off of the new overlay.
3. `AUDIT_7_LABELS_DEEP.md` — critical node+edge audit of the 7 labels.
4. `RESCUE_VERDICT.md` — can deletions be saved? (incl. internet research).
5. `POLLUTANT_ERA_EVIDENCE.md` — sourced pollutant×era matrix.
6. `REWIRE_REVIEW.md` + `DECISIONS_EXPLAINED.md` — old→new mapping + rationale.
7. `GRAPH_CRITICAL_AUDIT.md` — whole-graph audit (deferred, for later).
8. `EVIDENCE_REGELWERK.md` — all 91 Regelwerke with sources.

## Open decisions before the migration is built
1. **Huerde:** A (delete all) or B (keep ~11 market barriers, research-rescued)?
2. Keep the 4 `documented` pollutant edges (harmless) or drop?
3. **Leistungsanforderung:** consolidate ~46→~20 — confirm?
4. **PruefungNachweis:** dedup `pn_/pr_` + add names — confirm?
5. Aggressiveness: the migration will (a) add overlay + evidenced links, (b) replace Norm/
   RechtlicheBedingung, (c) delete the `inferiert` generic edges + dropped labels. Confirm scope.

## What the migration run will do (on approval)
One idempotent, `review_run`-tagged script: create overlay nodes/edges (sourced) → add rewire links
→ retire generic edges + replaced labels → re-run `audit_edges.py`. Full one-line rollback. Nothing
runs until you approve it.
