# Critical graph audit — evidence vs. generic tagging

A hard, critical pass over the **whole** `mit-bestand` graph (62 labels, ~80 relationship types),
testing your rule: *keep only what is concrete and evidence-able; cut what is generic, unsourced,
broken, or redundant. Quality over quantity.* Recommendations only — nothing deleted.

## The uncomfortable headline

**The analytical graph has almost no edge-level evidence.** Of ~80 relationship types, the core
classification edges are **0% sourced**:

| Relationship | edges | edge-evidence |
|---|--:|--:|
| HAT_HUERDE | 930 | **0%** |
| HAS_RISK_POLLUTANT | 754 | **0%** |
| HAT_PROZESSPHASE | 679 | **0%** |
| HAT_STATUS | 584 | **0%** |
| HAT_PRUEFUNG | 465 | **0%** |
| HAT_LEISTUNGSANFORDERUNG | 452 | **0%** |
| HAT_MATCHINGQUALITAET | 182 | **0%** |
| REFERENZIERT_NORM | 143 | **0%** |

And **0 of 13 Schadstoff, 0 of 103 Norm, 0 of 28 Huerde** nodes have an http source via `BELEGT_IN`.
Evidence exists almost only on the source nodes themselves (`Quelle`, `ExternalLink`) and partly on
`Akteur` (197/689), `Projekt` (33/86), `Kennwert` (52/255), `ReuseRule` (20/20).

**Implication:** this is a richly *tagged* graph, not an *evidenced* one. The new regulation overlay
is currently the **only** layer where every edge carries a source. So "keep only evidenced facts"
would shrink the graph drastically. The realistic clean target is a **3-tier** rule below.

## The classification rule (how to decide per label)

- **Factual** (verifiable from the entity itself — location, material, type, status, era): keep even
  without a per-edge URL. "This is a steel beam in Germany, status Realisiert" needs no citation.
- **Evidenced** (sourced, or in the new overlay): keep.
- **Interpretive & unsourced** (a subjective judgement with no source): this is the cut zone —
  either attach evidence or drop. Quality over quantity bites here.

---

## TIER 1 — Keep (content & sources). The substance of the graph.
`Quelle`, `ExternalLink`, `Akteur`, `Projekt`, `Bauwerk`, `Bauteilgruppe`, `Material`, `Bauteiltyp`,
`Land`, `Stadt`, `Kennwert`, `Dossier`, `ResearchDocument`, `SectionRef`, `Programm`, `Materialdepot`,
`ReuseRule`, `Software`, `Tool`. No action (beyond the encoding fix below).

## TIER 2 — Keep (clean *factual* controlled vocabularies). Concrete, sensible, well-used.
These are good taxonomies with concrete values — keep, even though edges are unsourced, because they
are factual classifications:
`Status` (Geplant/In_Bau/Realisiert…), `Nutzung` (Wohnen/Büro…), `Bauweise` (Holz/Massiv…),
`BauaufgabeIntervention` (Neubau/Rückbau…), `BauwerkEra`, `Defekt`, `ZustandsKlasse`,
`Rueckbauverfahren`, `Aufbereitungsverfahren`, `Methode`, `Bauteilebene`, `Layer` (Brand's 6 shearing
layers — a deliberate model), `Akteurtyp`, `Akteurrolle`, `Materialgruppe`, `Prozessphase`,
`Verbindungstechnik`, `Beschaffungsweg`, `Bauobjektrolle`. Plus the 7-label plan in `REWIRE_REVIEW.md`
(Schadstoff/PruefungNachweis/Leistungsanforderung kept; Norm/RechtlicheBedingung replaced).

## TIER 3 — Consolidate (redundant / overlapping dimensions)
Quality suffers from **several labels describing the same axis**. Recommend merging:

1. **Business/market/economics — 4 overlapping labels → 1–2.**
   `Marktmodell` (370 edges: Kauf/Leasing/Spende/Take-Back…), `Beschaffungsweg` (249:
   Bauteilbörse/Ausschreibung/Spende…), `Geschaeftsmodell` (98: Marktplatz/SaaS…), `Wirtschaft` (52).
   → `Marktmodell` and `Beschaffungsweg` overlap heavily (both "how the part is sourced/transacted").
   **`Wirtschaft` is the worst offender** — it mixes scenario instances ("CapEx höher, Payback über
   OpEx") with bare meta-terms ("Finanzierung", "Kostenvergleich", "Restwert", even a node literally
   named "Geschaeftsmodell"). Inconsistent granularity, unsourced, interpretive → **cut or rebuild**.

2. **Structural typology — 3 labels → consider 1.** `Bauweise` (6), `Bausystem` (9),
   `Tragwerksprinzip` (4) all classify "how it's built/carries load." For a graph this size, three
   parallel structural taxonomies is over-modelling → fold into `Bauweise` (+ keep `Bausystem` only
   for the named prefab systems like Plattenbau IW73, which are concrete and useful).

3. **Reuse-event enums — 4 labels, 6 nodes each → review.** `Wiederverwendungsergebnis`,
   `Wiederverwendungsort`, `Ressourcenquelle`, `Funktionswechsel` each slice the same reuse event.
   Coherent but heavy (≈1 000 edges total, all unsourced). Keep the 2 most informative
   (`Wiederverwendungsergebnis`, `Ressourcenquelle`); question `Funktionswechsel`/`Wiederverwendungsort`.

4. **`MatchingQualitaet` (9) → properties, not a label.** Its values cram three different axes into
   one flat list — `Geo: lokal`, `Spec: exakt`, `Temporal: geplant`. That's three attributes
   (distance / spec-fit / timing), not one vocabulary. Unsourced + conflated → **rebuild as 3
   properties or cut.**

5. **`Bauobjektklasse` (8) vs `Nutzung` (9)** partly overlap (Depot/Infrastruktur appear in both) →
   keep `Nutzung`, slim `Bauobjektklasse` to the non-use classes (Pavillon, Quartier, Reuse_Centre).

## TIER 4 — Cut (broken / orphan / scaffolding / no evidence & no concrete value)

| Label/Edge | Why cut |
|---|---|
| **`Akzeptanz`** (7) | **Broken**: 0 incoming edges, and values are an incoherent mix of certification systems (BREEAM/DGNB/LEED) and vibes (Patina-Ästhetik, Sichtbarkeit/Lernort). Not a coherent concept. **Delete.** |
| **`OntologyAnchor`** (2, 609 edges) | Import **scaffolding**: 2 mega-hubs everything is `ANCHORED_BY`. Provenance of a bulk seed, not evidence of any real relationship. **Drop the label + ANCHORED_BY** (or demote to a node property). |
| **`STUB_PROJECT_LINK`** (165) | The name says it: **placeholder** Akteur→Projekt links, never verified. Either verify→`BETEILIGT_AN` or **delete**. |
| **`GEHÖRT_ZU`** (55) | Vague "belongs-to" + the type name is **encoding-corrupted** (`GEH�RT_ZU`). Ambiguous semantics → re-type to something specific or delete. |
| **`HuerdeKategorie`** (10) | Only supports `Huerde`, half of which we're dropping; the regulatory questions replace it. Reassess after the Huerde split. |
| **`Wirtschaft`** (12) | See Tier 3.1 — mixed-granularity, unsourced. **Rebuild or cut.** |

## Cross-cutting data-quality problems

1. **Mojibake everywhere.** Names are full of broken encoding: `K�nstliche`, `Pr�fung`,
   `Zerst�rungsfreie`, `Eingeschr�nkt`, `�-Zeichen`. This is a UTF-8/Latin-1 corruption across the
   whole graph → a **one-off normalization pass** is worth doing regardless of everything else.
2. **`PruefungNachweis` needs controlled-vocab cleanup.** 120 nodes with **two prefix families**
   (`pn_*` and `pr_*`) that duplicate (`pn_zugversuch`/`pr_zugversuch`, `pn_sichtpruefung`/
   `pr_sichtpruefung`), and many bare ids with no `name`. Dedup + name before linking under
   Nachweisforderung.
3. **`Norm` duplication** (already in REWIRE_REVIEW): EN 1090 ×5, Eurocode 3 ×3.
4. **No edge evidence anywhere in the analytical core** — see headline. Decide consciously which
   tagging axes are "factual enough" to keep unsourced vs. which must be evidenced or cut.

## Where controlled vocabulary is genuinely missing / weak
- `PruefungNachweis` (free-ish, dual-prefix) → consolidate to the clean `Nachweisforderung` set + methods.
- `Wirtschaft` / `Akzeptanz` → no controlled definition; rebuild or drop.
- `MatchingQualitaet` → split into typed properties.
- Free-text-ish: `Kennwert` (255, values vary) — check it's structured (value+unit+source), not prose.

## Semantic connections worth adding (high value, evidence-able)
- `Schadstoff → Nachweisforderung → Regelwerk` (in the rewire plan) — turns unsourced pollutant tags
  into an evidenced check→law chain.
- `Bauwerk(era) → Schadstoff` already exists (`TYPISCH_BEI_ERA`) — good, evidence-able, keep & exploit.
- `Material/Bauteiltyp → Regelwerk` (the new overlay) — the first evidenced layer over the components.
- `Defekt → Nachweisforderung` (a defect implies a required check) — concrete, addable.
- `Rueckbauverfahren / Aufbereitungsverfahren → Regelwerk` (e.g. selektiver Rückbau ↔ VDI 6210 /
  ÖNORM B3151) — evidence-able, ties process to law.

## Recommended clean-up order (quality-first)
1. **Encoding normalization** (whole graph) — cheap, high quality gain.
2. **Delete Tier 4** (Akzeptanz, OntologyAnchor/ANCHORED_BY, STUB_PROJECT_LINK, GEHÖRT_ZU).
3. **Rewire plan** (Norm/RechtlicheBedingung → Regelwerk; Schadstoff/Pruefung/Leistung links).
4. **Consolidate Tier 3** (business/market; structural typology; reuse enums; MatchingQualitaet).
5. **Apply the evidenced overlay.**
6. **Re-audit** — target: every *interpretive* edge either sourced or gone; factual enums kept; one law layer.

## Honest trade-off for you to weigh
A strict "evidence-only" graph would delete most tagging and keep ~Quelle/Akteur/Projekt/Kennwert +
the new overlay. That's *too* aggressive — the factual taxonomies (material, type, status, era,
location) are valuable and verifiable without a URL. The defensible clean graph = **Tier 1 + Tier 2 +
the evidenced overlay**, with **Tier 3 consolidated** and **Tier 4 deleted**. Tell me how aggressive
you want to be on Tier 3/4 and I'll build the cleanup as a reviewable, reversible run.
