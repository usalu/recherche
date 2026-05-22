# Deep critical audit — the 7 regulation labels (node + edge level)

Focused on the mission labels: **Schadstoff, Huerde, Norm, RechtlicheBedingung, PruefungNachweis,
Bauproduktstatus, Leistungsanforderung.** Tested against: *concrete vs generic, evidenced vs
generically connected, what to keep / clean / delete.* Quality over quantity.

## The decisive finding: confidence ≠ evidence

Every connecting edge carries an **`evidence_confidence` number but NO source** (no URL, no quote):

| Relationship | edges | have `evidence_confidence` | have a real source |
|---|--:|--:|--:|
| HAT_HUERDE | 930 | 930 | **0** |
| HAS_RISK_POLLUTANT | 754 | 658 | **0** (edge) |
| HAT_LEISTUNGSANFORDERUNG | 452 | 452 | **0** |
| HAT_PRUEFUNG | 465 | 357 | **0** |
| REFERENZIERT_NORM | 143 | 143 | **0** |

A confidence score that cites nothing is **generic inference dressed as rigour.** This is the single
biggest quality problem in the mission layer.

## And the connections are provably *generic*, not per-instance facts

`HAS_RISK_POLLUTANT` is risk-typing by material/era, sprayed across the stock:

| Schadstoff | attached to … of 364 Bauteilgruppen |
|---|--:|
| s_schwermetalle | **178** |
| s_bleifarbe | **161** |
| s_formaldehyd / s_pak | 82 / 82 |
| s_holzschutzmittel | 80 |

Avg **2.9 pollutants per component**. Likewise `pr_zustandsbewertung` sits on 131 components,
`pr_sichtpruefung` on 51. These are "all metal → heavy-metal risk", "all components → condition
check" — **generic class tags, not documented findings.**

> This is *exactly* what the new overlay does — but with the derivation rule + legal source on the
> edge. So the overlay is the **evidenced replacement** for these generic-confidence edges.

---

## Per-label verdict (node level + edge level)

### Schadstoff (13 nodes) — KEEP nodes, REPLACE the generic edges
- **Nodes:** concrete real substances (Asbest, KMF, PCB, PAK…). **Keep all 13.**
- **`TYPISCH_BEI_ERA` / `TYPISCH_BEI_MATERIAL` / `TYPISCH_BEI_BAUTEILTYP` (40 edges):** these are the
  *honest, documented* risk rules ("asbestos typical 1900–1945"). **Keep — and make them the basis**
  the overlay derives from.
- **`HAS_RISK_POLLUTANT` (754) + `REQUIRES_VERIFICATION_FOR` (339):** generic, source-less,
  duplicated concern (one component-based, one project-based). **Replace** with the evidenced chain
  `Bauwerk(era)/Material → Schadstoff → Nachweis(AsbestCheck…) → Regelwerk(GefStoffV/TRGS)` the
  overlay already builds. Net: lose 1 093 confidence-only edges, gain sourced ones.
- **Inconsistency:** `s_radon` has no display name (`name = "s_radon"`); pseudo-evidence — Schadstoff
  `BELEGT_IN` points to a **seed Quelle with no http url**, not a real source.

### Huerde (28 nodes) — strongest DELETE candidate
- **0 source on any node, 930 confidence-only edges, you already flagged them inaccurate.** It is the
  least-evidenced, most-interpretive label in the graph.
- Regulatory half (Brandschutzkonflikt, Schadstoffbelastung, Haftung…) is **redundant** with the
  evidenced overlay. Market half (Mengenunsicherheit, Lagerfläche…) is **real but unsourced and has
  no home in an evidence-first graph.**
- **Recommendation (quality over quantity): delete `Huerde` entirely** + `HuerdeKategorie` +
  `HAT_HUERDE`/`HAT_HUERDEKATEGORIE`. If you want to keep a "barriers" lens, keep **only** the ~11
  market barriers as a clearly-labelled *non-evidenced* annotation — but the cleaner graph drops it.

### Norm (103 nodes) — REPLACE & delete
- Duplicated (EN 1090 ×5, Eurocode 3 ×3) and **0 evidence**. `REFERENZIERT_NORM` (143) is generic.
- **Replace** with the evidenced `Regelwerk` (90, each with URL) via `UNTERLIEGT_REGELWERK`; delete
  `Norm`. This is a pure upgrade (more correct, deduplicated, sourced).

### PruefungNachweis (120 nodes) — KEEP methods (clean), REPLACE the generic assignment
- **Nodes:** real test methods — valuable. **But controlled-vocab is broken:** two prefix families
  `pn_*` and `pr_*` **duplicate** (`pn_zugversuch`/`pr_zugversuch`, `pn_sichtpruefung`/
  `pr_sichtpruefung`, `pn_schadstoffanalyse`/`pr_schadstoffscreening`), and ~95 `pn_*` ids have **no
  name**. → **dedup + name** before use.
- **`HAT_PRUEFUNG` (465):** generic per-type assignment, no source. **Replace** with evidenced
  `ERFORDERT_NACHWEIS` (overlay), and hang the cleaned methods under the proof via `ERFUELLT_NACHWEIS`.

### Leistungsanforderung (46 nodes) — CONSOLIDATE then keep slim
- **Real requirements, but heavily duplicated:** fire alone = `la_brandschutz`, `la_brandverhalten`,
  `la_feuerwiderstand`, `la_f90`, `la_r90`, `la_rei90` (6 nodes, one concept). Also `la_haftung`
  (adhesion) collides semantically with Huerde `h_haftung` (liability) — **same string, different
  meaning** → naming inconsistency.
- **Consolidate** the fire/thermal/acoustic clusters (~46 → ~20), then keep as a slim property axis.
  `HAT_LEISTUNGSANFORDERUNG` (452) generic assignment → derive/evidence or keep as factual property.

### RechtlicheBedingung (16) & Bauproduktstatus (15) — low-value, mostly REPLACE
- Tiny usage (26 / 53 edges), 0 evidence, fully overlap the evidenced `Regelwerk`. **Replace** the
  named law-routes with `Regelwerk` links; keep only the 3 `Bauproduktstatus` *status enums*
  (Bestand vor Ort / Projekt-Freigabe / unbekannt). Drop the US/JP nodes.

---

## Systemic inconsistencies found
1. **`evidence_confidence` everywhere, evidence nowhere.** A confidence number with no citation. Either
   attach a source or stop calling it evidence.
2. **Duplicate concern relationships:** `HAS_RISK_POLLUTANT` (Bauteilgruppe-based) vs
   `REQUIRES_VERIFICATION_FOR` (Projekt-based, has `pollutant_basis`) — two ways to say "pollutant
   risk." Collapse to one evidenced path.
3. **`pn_`/`pr_` duplicate test families** in PruefungNachweis.
4. **Name collisions:** `la_haftung` (adhesion) vs `h_haftung` (legal liability) — identical token,
   opposite domains.
5. **Pseudo-evidence:** Schadstoff/Norm `BELEGT_IN` → a *seed* Quelle with no http url; looks sourced,
   isn't.

## What needs a controlled vocabulary
- **PruefungNachweis** → collapse `pn_/pr_` to one named set, mapped under `Nachweisforderung`.
- **Leistungsanforderung** → dedup clusters into a controlled requirement list.
- **Schadstoff** → already a clean 13; just give `s_radon` a name.

## Best semantic re-connection (evidence-first)
Replace the four generic concern-edges with **one evidenced spine**, all already buildable:
```
Bauwerk(era) ──TYPISCH_BEI_ERA(kept)──▶ Schadstoff ──▶ Nachweisforderung ──▶ Regelwerk
Material/Bauteiltyp ───────────────────▶ Regelwerk (overlay, sourced)
Defekt ─────────────────────────────────▶ Nachweisforderung   (a defect implies a check — addable)
```
Every edge here carries a source. The generic `HAS_RISK_POLLUTANT` / `HAT_PRUEFUNG` /
`HAT_LEISTUNGSANFORDERUNG` / `HAT_HUERDE` / `REFERENZIERT_NORM` layers are retired.

## Recommendation summary (quality over quantity)

| Label | Nodes | Generic edges | Verdict |
|---|---|---|---|
| Schadstoff | **keep 13** + TYPISCH_BEI_* | HAS_RISK_POLLUTANT / REQUIRES_VERIFICATION_FOR → **replace** | KEEP nodes, re-evidence edges |
| Huerde | **delete** (or keep 11 market, unsourced) | HAT_HUERDE → **delete** | **DELETE** |
| Norm | delete (dup, no evidence) | REFERENZIERT_NORM → **replace** | **REPLACE→Regelwerk** |
| PruefungNachweis | keep, **dedup pn_/pr_ + name** | HAT_PRUEFUNG → **replace** | KEEP methods, re-evidence |
| Leistungsanforderung | **consolidate ~46→~20** | HAT_LEISTUNGSANFORDERUNG → derive | CONSOLIDATE + keep slim |
| RechtlicheBedingung | delete | HAT_RECHTLICHE_BEDINGUNG → **replace** | **REPLACE→Regelwerk** |
| Bauproduktstatus | keep 3 enums, drop rest | HAT_BAUPRODUKTSTATUS → **replace** | mostly REPLACE |

**Net:** the graph keeps the real *entities* (pollutants, test methods, requirements) and the *honest
documented rules* (TYPISCH_BEI_ERA), **deletes ~2 700 confidence-only generic edges + the Huerde/Norm/
RechtlicheBedingung labels**, and reconnects everything through the **one evidenced spine** (overlay).
Smaller, sourced, consistent.

## Decisions for you
- [ ] **Huerde: delete entirely?** (recommended) or keep 11 market barriers as explicitly non-evidenced?
- [ ] **Retire `HAS_RISK_POLLUTANT` + `REQUIRES_VERIFICATION_FOR`** in favour of the evidenced era/material→Schadstoff→check→law spine?
- [ ] **Retire `HAT_PRUEFUNG` / `HAT_LEISTUNGSANFORDERUNG`** generic edges (keep the nodes)?
- [ ] **PruefungNachweis pn_/pr_ dedup** + naming — do it?
- [ ] **Leistungsanforderung consolidation** (~46→~20) — do it?
- [ ] **Norm / RechtlicheBedingung → Regelwerk replace & delete** — confirm?
