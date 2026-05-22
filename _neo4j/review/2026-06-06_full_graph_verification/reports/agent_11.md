# Verifier Agent 11 — Regulation / legal layer (nodes + structural edges)

**Database:** `mit-bestand` (READ-ONLY; only `get-schema` + `read-cypher` used; no graph mutation)
**Date:** 2026-06-06
**Ledger:** [`ledger/agent_11.csv`](../ledger/agent_11.csv) — 559 rows
**Generator (provenance):** [`_agent11_build_ledger.py`](../_agent11_build_ledger.py)

## 1. Scope recap

| Surface | Owned by Agent 11 | Count |
|---|---|---:|
| Nodes — typed `*recht` law labels | 11 labels, 91 unique nodes | 91 |
| Nodes — `ReuseRule` | synthetic country×material rules | 20 |
| Rels — `GESTUETZT_AUF_REGELWERK` | `Nachweisforderung` → law node | 167 |
| Rels — `GILT_IN_LAND` | law node → `Land` | 281 |
| **Total claims** | | **559** |

Agent 11 verifies **node identity** (each instrument is a real law/standard/regulation),
**label/`rechtsbereiche` taxonomy coherence**, and **structural + country-attribution logic**
of the two edge types. **Live URL proof of the `source_url` carried on these rels is owned by
Agent 07**; this shard defers that and only references the expected merge.

### Enumeration Cypher (work-set)
```cypher
// nodes
MATCH (n) WHERE any(l IN labels(n) WHERE l ENDS WITH 'recht') OR 'ReuseRule' IN labels(n) RETURN n;
// structural edges
MATCH (nf:Nachweisforderung)-[r:GESTUETZT_AUF_REGELWERK]->(rw) RETURN nf,rw;
MATCH (rw)-[r:GILT_IN_LAND]->(l:Land) WHERE any(x IN labels(rw) WHERE x ENDS WITH 'recht') RETURN rw,l;
```

## 2. Counts by verdict

| Verdict | Nodes | Rels | Total |
|---|---:|---:|---:|
| PROVEN | 111 | 448 | **559** |
| PARTIAL / UNSUPPORTED / DEAD_LINK / CONTRADICTION / SCHEMA_VIOLATION | 0 | 0 | **0** |

Proposed action for **every** item: `KEEP`. **No deletions, relabels, or escalations required** in
this layer. The legal layer is the cleanest surface in the campaign.

## 3. Cross-check against authoritative docs (all PASS)

Verified live `mit-bestand` against `FINAL_AUDIT_REPORT.md` and `VARIANT_B_TAXONOMY.md`:

| Check | Expected (docs) | Live | OK |
|---|---|---|:--:|
| Typed law nodes | 91 | 91 | ✅ |
| Multi-label law nodes | 48 | 48 | ✅ |
| `GESTUETZT_AUF_REGELWERK` | 167 | 167 | ✅ |
| `GILT_IN_LAND` | 281 | 281 | ✅ |
| `labels(rw)` == `rechtsbereiche[]` | (by design) | 0 mismatches | ✅ |
| Per-label counts | Tragwerk 26 / Bauprodukt 23 / ReuseDoku 18 / Schadstoff 17 / Rueckbau 16 / Umwelt 13 / Bauphysik 10 / Brandschutz 8 / Genehmigung 7 / HygieneElektro 4 / Haftung 3 | identical | ✅ |
| `:Regelwerk` legacy label | 0 | 0 | ✅ |

**Domain/range integrity (deterministic Cypher):**
- `GESTUETZT_AUF_REGELWERK`: 167/167 with source ∈ `Nachweisforderung` and target a typed law node (0 bad).
- `GILT_IN_LAND`: 281/281 with source a typed law node and target `:Land` (0 bad).
- **Orphans:** 0 law nodes lack `GILT_IN_LAND`; 0 law nodes lack an incoming `GESTUETZT_AUF_REGELWERK`. Every law node is wired on both axes.
- **Evidence fields present** (for Agent 07's live fetch): 281/281 `GILT_IN_LAND` and 167/167 `GESTUETZT` carry both `source_url` and `source_quote`.

## 4. Node identity — each instrument is a real law/standard/regulation

All 91 `rw_*` nodes resolve to genuine, identifiable instruments across the right standards bodies
and jurisdictions, e.g.:
- **Binding statutes/ordinances:** KrWG, GewAbfV, GefStoffV, EBV, StrlSchG, ProdHaftG/BGB, GEG,
  AltholzV, EU WFD 2008/98, EU CPR 305/2011 & 2024/3110, POP 2019/1021, REACH Annex XVII,
  ESPR, loi AGEC (PEMD / REP PMCB), RE2020, BR18, TEK17, Bbl/MPG, MuKEn, MBO/LBO, Denkmalschutz.
- **Standards (CEN/EN/ISO/DIN/national):** Eurocodes EN 1990–1999, EN 1090(-2)/14399, EN 1168,
  EN 13501, EN 13791/12504, EN 408, EN 771, EN ISO 6892, EN 13162/13830/14351, EN 15804/15978,
  CEN/TS 1090-201, CEN/TS 17440, DIN 18008/18040/18065/4074/4102/18945, DIN SPEC 91484/91525,
  NEN 8700, NTA 8713, ÖNORM B 3151, SIA 269/269-2/380-1/2032, VKF, OIB, SCI P427, UK ADB,
  UKCA/CE, PAS 2080, TRGS 519/521/524, VDI 3492/6202/6210/6023-6022, PCB-Richtlinie, ISO 20887.
- **Voluntary frameworks / guidance (real but soft-law — flagged in ledger `notes`, kept as
  reference nodes):** `rw_naturstein_reuse` (0.65), `rw_fib_precast_reuse` (0.70),
  `rw_glas_reuse_igu` (0.70), `rw_qng_dgnb` (0.75), `rw_zirkulaere_vergabe` (0.75),
  `rw_istructe_reuse` (0.80), `rw_fcrbe_reuse_toolkit` (0.80), `rw_madaster_grp` (0.80),
  `rw_eu_levels` (0.80). These are legitimate normative references; they are **not** binding
  statutes/standards but the `*recht` labels are domain buckets (per the taxonomy's own note —
  "reference standards, not spray nodes"), so they remain valid. No action needed.

## 5. Country attribution (`GILT_IN_LAND`) — coherent

Nine `Land` targets are used: DE, BE, NL, FR, NO, DK, AT, CH, UK. Attribution patterns:
- **National instruments map to their own country** and are all correct (SIA/MuKEn/VKF→CH;
  NEN/NTA/Bbl/MPG→NL; ÖNORM/OIB→AT; TEK17→NO; BR18→DK; PEMD/RE2020/REP PMCB→FR;
  SCI P427/IStructE/ADB/PAS 2080/UKCA→UK; DIN/TRGS/VDI/DIBt/KrWG/EBV/GefStoffV/… →DE).
- **Pan-EU / EN / ISO instruments** map to the 7-country EU/EEA subset present in the graph
  (DE, BE, NL, FR, NO, DK, AT). 31 instruments use this set → 217 edges.
- **`rw_fcrbe_reuse_toolkit` → UK+BE+NL+FR** correctly matches the Interreg North-West Europe
  partner geography of the FCRBE project.
- **`rw_madaster_grp` → DE+NL** matches Madaster's NL origin and DE Gebäuderessourcenpass uptake.

Edge total reconciles exactly: 217 (EU7×31) + 4 (FCRBE) + 2 (Madaster) + 58 (single-country) = **281**.

## 6. Anomalies / observations (non-blocking — no action proposed)

1. **EN/EU standards exclude CH and UK from `GILT_IN_LAND`.** Eurocodes, EN product norms and EU
   regulations are scoped only to the 7 continental EU/EEA graph countries; Switzerland and the UK
   are intentionally covered by national equivalents (SIA, BS/UKCA) rather than the EN/EU node.
   This is a **deliberate, internally-coherent jurisdiction-scoping decision**, not an error — but
   a reviewer wanting EN-applies-everywhere semantics should be aware the graph models it as
   national-equivalent substitution. (Flagged in every EU7 edge's `notes`.)
2. **`ReuseRule` is not a legal instrument.** The 20 `rr_*` nodes are synthetic country×material
   aggregators (each wired via `HAT_AUFBEREITUNG` + `HAT_SCHADSTOFFRISIKO`, degree ≥4, no `source_url`).
   They are valid internal nodes but the "instrument-reality" test does not apply; verified by logic
   only. Worth a scope note for the Aggregator: they sit in Agent 11's node scope but belong
   conceptually closer to the process/Schadstoff layer than the typed-law layer.
3. **`rr_fi_beton_hollow_core_slabs` references Finland**, which has **no `land_finnland`** node in
   the legal layer. Because `ReuseRule` has no `GILT_IN_LAND`/`LIEGT_IN_LAND` edge, this produces no
   contradiction, but Finland coverage is asymmetric vs the 9 legal-layer countries.
4. **`rw_din_4074_en_14081` and `rw_din_en_13501`** carry German `DIN` prefixes yet map to the
   EU7 set. Justified because each wraps a harmonised EN standard (EN 14081 / EN 13501); the EN core
   is genuinely pan-European. Loose but defensible; kept.

## 7. Ten "worst" findings

There are **no UNSUPPORTED / contradiction / schema findings** in this layer. The ten lowest-confidence
or most-loosely-scoped items (all still PROVEN/KEEP, listed for transparency) are:

| # | element | issue | verdict |
|---|---|---|---|
| 1 | `rw_naturstein_reuse` | confidence 0.65; generic web guidance, not a law/standard | PROVEN (soft-law note) |
| 2 | `rw_fib_precast_reuse` | confidence 0.70; fib bulletins are guidance | PROVEN (soft-law note) |
| 3 | `rw_glas_reuse_igu` | confidence 0.70; Glass-for-Europe guidance | PROVEN (soft-law note) |
| 4 | `rr_fi_beton_hollow_core_slabs` | Finland has no legal-layer `Land` node | PROVEN (logic, note) |
| 5 | `rw_qng_dgnb` / `rw_zirkulaere_vergabe` | confidence 0.75; voluntary scheme / procurement guidance | PROVEN (soft-law note) |
| 6 | EU7 scoping of `rw_eurocodes_en_1990_1999` | CH/UK excluded despite de-facto adoption | PROVEN (scoping note) |
| 7 | `rw_din_4074_en_14081` | DIN-prefixed id mapped pan-EU | PROVEN (note) |
| 8 | `rw_din_en_13501` | DIN-prefixed id mapped pan-EU | PROVEN (note) |
| 9 | 20 `ReuseRule` nodes | not legal instruments; layer-placement question | PROVEN (logic, scope note) |
| 10 | `rw_madaster_grp` | private passport scheme labelled as ReuseDoku/Umwelt *recht* | PROVEN (soft-law note) |

## 8. Escalated to human

**None.** No item in the regulation/legal layer requires human adjudication. The two scope-level
observations (ReuseRule placement; EN/EU CH-UK exclusion) are noted for the Aggregator but do not
warrant a graph change.

## 9. Handoff to Agent 07 / Aggregator

- All 448 structural edges carry `source_url` + `source_quote` — ready for Agent 07's live-fetch
  pass. Agent 11 marks them structurally PROVEN; the final verdict should be **merged** with
  Agent 07's HTTP-level result per edge `element_id` (`gestuetzt__<nf>__<law>`, `gilt__<law>__<land>`).
- Coverage for the Aggregator: Agent 11 owns and has emitted **all 91 typed-law nodes, all 20
  ReuseRule nodes, all 167 `GESTUETZT_AUF_REGELWERK`, all 281 `GILT_IN_LAND`** — zero gaps in scope.

---

**Summary:** 559/559 regulation-layer claims verified PROVEN, 0 problems, all `KEEP`. Counts, the
48 multi-label nodes, per-label distribution, domain/range, orphan-freedom, and country attribution
all reconcile exactly with `FINAL_AUDIT_REPORT.md` and `VARIANT_B_TAXONOMY.md`. The single most
important finding is a non-defect: pan-EU/EN instruments are deliberately scoped to the 7 EU/EEA
graph countries and exclude CH/UK (covered by SIA / BS-UKCA national equivalents) — coherent, but
the Aggregator should record it as the layer's one modelling assumption. Live URL proof of the
448 `source_url`s is deferred to Agent 07.
