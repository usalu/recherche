# Rescue attempt — can the deletion candidates be saved with real data?

Last phase before the final decision. For each candidate I tested **(1) is there real evidence
already in the graph?** and **(2) does real-world data exist that could evidence it?** Verdict per item.

## UPDATE — internet research result (the important part)

I researched each association on the web. **The knowledge behind the generic edges is authoritatively
documented** — so deleting the unsourced edges is *not* information loss; the knowledge is **rescuable
as sourced rules** (which the overlay already expresses). Sources found:

| Association (old generic edge) | Real, authoritative source found | → rescue form |
|---|---|---|
| pollutant ↔ building age/material (`HAS_RISK_POLLUTANT`) | **LfU Bayern "Arbeitshilfe Rückbau schadstoffbelasteter Bausubstanz"** (now added as `rw_lfu_schadstoff_arbeitshilfe`), LABO Schadstoffkataster, BG BAU Gebäudeschadstoffe, schadstoff-kompass — Asbest 1950–95, KMF <2000, PCB ≤1989, PAK ≤1970s | era→Schadstoff→check→law, **sourced** |
| test ↔ material/era (`HAT_PRUEFUNG`) | **SCI P427** (steel: NDT post-1970 / destructive pre-1970), concrete NDT reviews (EN 13791), timber | material/era→Nachweis, **sourced** |
| performance ↔ component (`HAT_LEISTUNGSANFORDERUNG`) | harmonised product standards (EN 14351, EN 13830, EN 1168…) declare the performance characteristics | component→Nachweis, **sourced** |
| barriers (`HAT_HUERDE`, market half) | FCRBE + peer-reviewed reuse-barrier taxonomies | project-level barriers, **sourced** |

**So the corrected conclusion:** the *associations are real and evidenceable*, but only as
**documented rules**, never as the per-component `inferiert` tags. Deleting the generic edges and
re-expressing the same knowledge through the **sourced overlay** (now incl. the LfU Arbeitshilfe for
the Schadstoff/era rules) **preserves the information and adds the evidence it was missing.**

---

## The graph incriminates itself

The connecting edges don't just *lack* sources — their own metadata labels them as not-evidence:

| Edge | What its `evidence_confidence` / basis actually says |
|---|---|
| `HAS_RISK_POLLUTANT` (754) | **`inferiert`** (650) · `unklar` (8) · none (96) — literally "inferred" |
| `HAT_LEISTUNGSANFORDERUNG` (452) | **`unklar`** for **all 452** — literally "unclear" |
| `REQUIRES_VERIFICATION_FOR` (339) | **`material_only`** for 331; only **4 `documented`** |
| `HAT_PRUEFUNG` (465) | id + confidence only, no basis |

And reaching a **real http source from any of the 7 labels = 0** (Huerde, Schadstoff, Norm,
RechtlicheBedingung, PruefungNachweis, Bauproduktstatus, Leistungsanforderung — all zero). The only
"anchors" are a controlled-vocab seed file and the actor-list file — provenance scaffolding, not
evidence of any specific claim.

---

## Verdict per candidate

### 1. Generic concern/assignment edges → DELETION JUSTIFIED
`HAS_RISK_POLLUTANT`, `REQUIRES_VERIFICATION_FOR`, `HAT_PRUEFUNG`, `HAT_LEISTUNGSANFORDERUNG`,
`HAT_HUERDE`, `REFERENZIERT_NORM`, `HAT_BAUPRODUKTSTATUS`, `HAT_RECHTLICHE_BEDINGUNG`.
- **In-graph rescue:** failed — metadata is `inferiert`/`unklar`/`material_only`, 0 sources.
- **Can they be evidenced per-instance?** No — that needs each project's own demolition/audit report,
  which we don't have. The honest best is the **derivation** the overlay already makes (era/material
  → check → law, with the *rule* sourced). 
- **→ Delete the generic edges; replace with the evidenced overlay spine.** Fully justified.
- *Only flicker:* the **4** `documented` pollutant edges — but even these have no source on their
  project. Keep those 4 if you like; they don't change anything.

### 2. Norm / RechtlicheBedingung / Bauproduktstatus (named law-routes) → DELETION JUSTIFIED (already re-evidenced)
- **In-graph rescue:** failed — 0 sources.
- **Real-world rescue:** *succeeds, but already done* — every named regime (CE/CPR, ZiE, UKCA, NTA 8713,
  PEMD, Tracimat, EU Taxonomy, KrWG, ProdHaftG…) now exists as an **evidenced `Regelwerk`** with a URL.
- **→ Replace with `Regelwerk` and delete the old labels.** The evidence lives in the replacement.

### 3. Entity nodes (NOT deletion candidates) → KEEP, re-evidenced by the overlay
`Schadstoff` (13 substances), `PruefungNachweis` (test methods), `Leistungsanforderung` (requirements)
are real things. They were never the problem — the *generic edges to them* were. Keep the nodes
(dedup PruefungNachweis `pn_/pr_`, consolidate Leistung fire-cluster, name `s_radon`), and let the
overlay supply the evidenced connections. `TYPISCH_BEI_ERA` (the documented pollutant-by-era rule) is
the one honest, reusable piece — keep it and derive from it.

### 4. Huerde → THE ONE GENUINE RESCUE — but only the market half, via new research
- **In-graph rescue:** failed hardest — nodes have only `id` + `name`, edges are `inferiert`, **0**
  sources of any kind.
- **Real-world rescue:** **possible.** "Barriers to component reuse" is a documented research field —
  peer-reviewed taxonomies + FCRBE cover exactly the market/logistics/cultural barriers
  (knowledge gaps, market infrastructure, **stakeholder perception/risk**, storage, availability,
  institutional lock-in, weak policy). The ~11 market barriers (Mengenunsicherheit, Lagerfläche,
  Akzeptanz, Verfügbarkeit, Aufbereitungsaufwand…) **could be re-evidenced from literature.**
- **But:** (a) that's a *different* axis than this regulation mission; (b) the ~13 **regulatory**
  Huerde (Brandschutzkonflikt, Schadstoffbelastung, Haftung…) are **redundant** with the evidenced
  overlay and not worth rescuing; (c) the current `HAT_HUERDE` edges (per-component, `inferiert`)
  are wrong regardless and go.
- **→ Two clean options:**
  - **(A) Delete Huerde entirely** — simplest, fully justified for an evidence-first regulation graph.
  - **(B) Keep ~11 market barriers as a small, separately-researched "Reuse-Hemmnis" vocabulary** —
    re-evidenced from the literature above, connected at project/programme level (not per-component
    inference). A ~1-round research task, only if you value the barriers lens.

---

## Bottom line

| Candidate | Real data to save it? | Final verdict |
|---|---|---|
| `HAS_RISK_POLLUTANT` / `REQUIRES_VERIFICATION_FOR` | no (own metadata: inferiert/material_only) | **delete → overlay spine** |
| `HAT_PRUEFUNG` / `HAT_LEISTUNGSANFORDERUNG` (edges) | no (unklar) | **delete → overlay** |
| `HAT_HUERDE` (edges) | no | **delete** |
| `Norm` / `RechtlicheBedingung` / `Bauproduktstatus`-routes | yes — *as evidenced Regelwerke* | **replace & delete** |
| Entity nodes (Schadstoff/Pruefung/Leistung) | yes — via overlay | **keep + clean** |
| `Huerde` nodes (market half) | **yes — via literature** | **your call: delete (A) or research-rescue (B)** |
| `Huerde` nodes (regulatory half) | no (redundant) | **delete** |

Internet research confirms the *associations* are real and documented — but only at the **rule**
level, never as the per-component `inferiert` tags. So: **delete the unsourced generic edges and the
redundant labels; keep the real entity nodes; re-express the knowledge through the sourced overlay**
(now including the LfU Arbeitshilfe for Schadstoff/era). This *preserves and sources* the information
rather than losing it. The only genuinely optional rescue is the **~11 market-barrier Huerde** nodes
(documented in reuse literature) — keep only if you want a barriers axis.

Tell me **A (delete Huerde) or B (research-rescue the 11 market barriers)**, and whether to keep the
4 `documented` pollutant edges, and I'll build the final reversible cleanup+rewire run.
