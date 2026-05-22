# Why each decision — Rewire Review explained

This explains *why* each old label gets keep / rewire / delete in `REWIRE_REVIEW.md`, in plain
language. It follows one rule you set:

> **We don't rewire forcefully. We keep information that is correct, makes sense, and is well
> connected. We only replace something when the new version is genuinely more correct, and we
> drop only what is wrong, redundant, or out of scope.**

## The 3-question test applied to every label

For each old label we ask:
1. **Is it correct / evidence-able?** (does it describe something real and true?)
2. **Does it make sense as its own thing?** (or is it just another name for something we already have?)
3. **Is it well connected?** (how many edges actually use it — is it load-bearing in the graph?)

If 1+2+3 are yes → **keep** (maybe add links, but don't force-change existing edges).
If it's correct but a **duplicate** of the new evidenced layer → **replace**.
If it's **wrong, unused, or out of scope** → **drop**.

| Old label | Connections (usage) | Correct? | Own concept? | → Decision |
|---|--:|---|---|---|
| **Schadstoff** | 1 118 | yes (real pollutants) | yes | **KEEP** (+ link to check/law) |
| **Huerde** | 930 | partly | partly | **KEEP the real barriers, DROP the duplicates** |
| **PruefungNachweis** | 465 | yes (real test methods) | yes (finer than our proofs) | **KEEP** (+ link to proof) |
| **Leistungsanforderung** | 452 | yes (real requirements) | yes | **KEEP** (+ optional link) |
| **Norm** | 143 | yes — but duplicated & no evidence | **no** (= Regelwerk) | **REPLACE** with Regelwerk |
| **Bauproduktstatus** | 53 | yes | partly (status vs law) | **KEEP as status**, drop US/JP |
| **RechtlicheBedingung** | 26 | yes — but overlaps & barely used | mostly no | **REPLACE / drop** |

> Note: this **softens** two verdicts from the first review. Because `Leistungsanforderung` (452)
> and `Bauproduktstatus` are real, sensible concepts, we now **keep** them rather than force a
> rewire. Only `Norm` and `RechtlicheBedingung` are genuinely redundant enough to replace.

---

## "Bauproduktstatus (15) → Regelwerk / enum" — what that meant (and the simpler answer)

**What Bauproduktstatus is:** it answers *"what approval / conformity status does this building
product have?"* — e.g. `CE (hEN)`, `CE (ETA)`, `Ü-Zeichen`, `abZ/aBG`, `ZiE/vBG`, `UKCA`,
`NTA 8713`, `PEMD (FR)`, `Tracimat (BE)`, `BauPG (CH)`, plus 3 generic states:
`Bestand vor Ort` (as-found in the existing building), `Projekt-Freigabe` (cleared for this
project), `Status unbekannt`.

**Why I originally wrote "→ Regelwerk / enum":** 12 of the 15 are *named after the conformity
regimes that are also our Regelwerke* (CE = the CPR law, ZiE = the DIBt rule, UKCA = the UKCA rule,
NTA 8713, PEMD, Tracimat…). So one option was to point those at the matching Regelwerk and keep
only the 3 generic states as a small value-list ("enum"). That's what "→ Regelwerk / enum" meant:
*split it — laws to the law layer, plain states stay as states.*

**Why that was too forceful — and the simpler decision:** a *status* ("this beam **has** CE") is
not the same statement as a *law* ("CE marking **is required** by the CPR"). The status is a fact
about the component; the law is the requirement. Your new graph already carries the requirement
(`Bauteilgruppe → UNTERLIEGT_REGELWERK → CPR`). So we don't need to convert the status into a law.

**→ Decision:** **keep `Bauproduktstatus` as a status dimension** (all the conformity states), and
*optionally* add a light cross-link `bps_ce_hen → (CPR Regelwerk)` for navigation — but **leave the
existing `HAT_BAUPRODUKTSTATUS` edges as they are.** Only the 2 non-European ones
(`IBC` USA, `JIS` JP) are dropped as out of scope. Nothing forced.

---

## Why we "split" Huerde

**What Huerde is:** *barriers / obstacles to reuse* — 930 edges, so it's heavily used and worth
respecting. But the 28 Huerde nodes are really **two different kinds of thing mixed together:**

**Group A — regulatory/technical barriers** that are just *another name* for a regulatory topic the
new vocabulary now covers accurately and with evidence:
`Brandschutzkonflikt` (= BrandschutzFrage), `Schadstoffbelastung` (= SchadstoffFrage),
`Bauproduktstatus` (= BauproduktstatusFrage), `Haftung` / `Gewaehrleistung` (= HaftungFrage),
`Technische_Freigabe`, `Hygieneanforderung`, `Dauerhaftigkeit`, `Zustand_unklar`, `Toleranzen`,
`Materialqualitaet_unklar`, `Kompatibilitaetsproblem`, `Fehlende_Datenstandards`,
`Anschlussproblem`, `Bruch_/Beschaedigungsrisiko`, `Fehlende_Standardisierung`.
→ These **duplicate** the new layer. You already told me the old `HAT_HUERDE` links were
*inaccurate*. Keeping both would mean two ways to say the same thing — one vague, one evidenced.
**So we drop these** (the accurate Frage/Nachweis edges replace them).

**Group B — market / logistics / process barriers** that **no regulation describes** — a genuinely
separate, useful axis:
`Akzeptanzproblem` (market acceptance), `Mengenunsicherheit` (quantity uncertainty),
`Terminunsicherheit` (schedule risk), `Verfuegbarkeitsproblem` (availability),
`Fehlende_Lagerflaeche` (no storage space), `Aufbereitungsaufwand` (refurb effort),
`Entwurfsbindung` (design lock-in), `Ausschreibungsproblem` (tendering),
`Heterogenitaet_Chargen` (batch variability), `Witterung_Feuchte` (weather/moisture during storage),
`Unkonventionelles_Material`.
→ These are real, distinct, and **not** covered by any Regelwerk. **So we keep them**, with their
edges untouched.

**"Split" therefore means:** keep the ~11 barriers that add unique information; drop the ~13 that
merely re-label a regulatory topic the evidenced layer now states more accurately. It is **not** a
rewrite of Huerde — it's removing the duplicated half so the graph says each thing once.

> If you'd rather keep *all* Huerde untouched (do nothing here), that's fine too — Huerde then just
> coexists as a looser "barriers" view alongside the precise regulatory layer. Tell me which.

---

## The only true "replace" cases (where the new version is clearly more correct)

- **Norm (143 uses) → Regelwerk.** `Norm` *is* the standards layer, but: (a) **no evidence/URLs**,
  (b) **heavy duplication** — EN 1090 exists 5×, Eurocode 3 exists 3×; 103 nodes ≈ 30 real
  standards. The new `Regelwerk` is the same standards, **deduplicated and each with a source**.
  So we point the `REFERENZIERT_NORM` edges at the matching Regelwerk and retire `Norm`. This is a
  genuine upgrade, not a forced move.
- **RechtlicheBedingung (26 uses) → Regelwerk / question.** Barely used, and every node is either a
  law we already have evidenced (CPR, EU Taxonomy, KrWG, ProdHaftG, Denkmalschutz, Vergaberecht) or
  a legal *question* (Genehmigung/Haftung). Low usage + full overlap → replace.

## What stays exactly as-is (well connected + correct, no forced change)

- **Schadstoff** (1 118) — real pollutants. We only **add** links to the matching check
  (`AsbestCheck`…) and law (`TRGS 519`…). Existing edges untouched.
- **PruefungNachweis** (465) — real test *methods*, finer than our proof categories. We only **add**
  a link from each method to the proof it fulfils, and dedup the `pn_`/`pr_` twins.
- **Leistungsanforderung** (452) — real performance requirements. **Kept as its own axis.** Optional
  links to the proof that demonstrates each; no forced rewire.

## Net effect

Delete only `Norm` and `RechtlicheBedingung` (redundant). Drop a handful of out-of-scope/duplicate
nodes. **Keep everything that is correct, sensible, and well connected** — Schadstoff,
PruefungNachweis, Leistungsanforderung, Bauproduktstatus (as status), and the real-barrier half of
Huerde — adding evidenced links rather than forcing changes. One clean evidenced **law layer**
(`Regelwerk`) replaces the duplicated `Norm`, and the rest of the graph keeps its hard-won
connections.

## Your decisions

- [ ] Huerde: **split** (drop ~13 duplicates) — or keep all untouched?
- [ ] Bauproduktstatus: **keep as status** (drop US/JP) — or convert the 12 routes to Regelwerk links?
- [ ] Leistungsanforderung: **keep as-is** — or fold into Nachweis?
- [ ] Norm → Regelwerk replace: OK?
- [ ] RechtlicheBedingung → replace/drop: OK?
- [ ] Schadstoff / PruefungNachweis: keep + add evidenced links: OK?
