# Data-grounded blueprint — every label, with the numbers

Companion to `GRAPH_BLUEPRINT.md`, now backed by concrete measurements for all 62 labels:
**n** = nodes · **→P** = distinct nodes reached from a Projekt · **→BTG** = from a Bauteilgruppe ·
**httpEv** = nodes with a real http source. Priorities: **evidence first**, **Projekt/Bauteilgruppe
connectivity second**, **no duplication third**.

## Finding 0 — evidence is concentrated in ~9 labels; everything analytical is 0
| Has real http evidence | n / httpEv |
|---|---|
| Quelle | 2981 / **2737** |
| ExternalLink | 2610 / **2610** |
| SectionRef | 582 / **575** |
| Akteur | 689 / 197 |
| ResearchDocument | 396 / 187 |
| Dossier | 97 / **69** |
| Kennwert | 255 / 52 |
| Projekt | 86 / 33 |
| ReuseRule | 20 / **20** |
| **All 53 other labels** | **0 http evidence** |

→ The regulation/classification/process layers have **zero** real sources. The new `Regelwerk`/
`Nachweisforderung`/`Regulierungsfrage` overlay is the **only** evidenced regulation layer. (Correction
to the earlier draft: **Dossier + SectionRef are evidence carriers, NOT plumbing — keep them.**)

## Finding 1 — the evidence backbone (keep, it's the spine of trust)
`Quelle` (+`ExternalLink` merged), `SectionRef`, `Dossier`, `ResearchDocument`, `Kennwert`, `ReuseRule`.
Dossier connects Akteur(429)/BTG(287)/Bauwerk(188)/Kennwert(162)/Stadt(102) via `HAS_SOURCE_LINK` — it's
the per-entity source hub. **These are the most valuable nodes for an evidence-first graph.**

## Finding 2 — core entities (keep; the hubs)
| Label | n | →P | →BTG | verdict |
|---|--:|--:|--:|---|
| Projekt | 86 | — | — | KEEP hub |
| Bauteilgruppe | 364 | 360 | — | KEEP hub |
| Bauwerk | 184 | 174 | 149 | KEEP |
| Akteur | 689 | 0 | 0 | KEEP (actor side) |
| Programm | 29 | 17 | 0 | KEEP |
| Materialdepot | 22 | 16 | 19 | KEEP |
| Software (+Tool→merge) | 18/7 | 14/6 | 7/3 | KEEP, merge Tool→Software |
| Land, Stadt | 17/74 | 13/60 | — | KEEP |

## Finding 3 — factual attributes of BTG/Bauwerk (keep; verifiable without URL)
| Label | n | →P | →BTG | verdict |
|---|--:|--:|--:|---|
| Material | 26 | 10 | 20 | KEEP |
| Materialgruppe | 11 | 0 | 11 | KEEP (coarse roll-up) |
| Bauteiltyp | 23 | 14 | 16 | KEEP |
| Nutzung | 9 | 9 | 0 | KEEP (absorbs Bauobjektklasse) |
| Bauobjektklasse | 8 | 5 | 0 | FOLD → Nutzung (non-use values stay) |
| Bauobjektrolle | 6 | 0(→Bauwerk 6) | 0 | KEEP (Donor/Receiver — vital for reuse) |
| BauwerkEra | 6 | 0(→Bauwerk 4) | 0 | KEEP (drives Schadstoff, sourced) |
| Status | 9 | 9 | 3 | KEEP |
| BauaufgabeIntervention | 10 | 10 | 0 | KEEP (drives project reg-context) |
| Defekt | 10 | 7 | 5 | KEEP (condition) |
| ZustandsKlasse | 6 | 0 | 3 | KEEP (condition class) |
| Verbindungstechnik | 15 | 1 | 11 | KEEP (disassembly relevance) |
| Bauteilebene | 6 | 0 | 6 (289 edges) | KEEP → make a **property** of BTG |
| Bauweise | 6 | 6 | 5 | KEEP (absorb Tragwerksprinzip) |
| Bausystem | 9 | 2 | 7 | KEEP (named prefab systems) |
| Tragwerksprinzip | 4 | 2 | 4 | **MERGE → Bauweise** (only 25 Bauwerk overlap, 4 nodes) |
| Layer | 6 | 0 | 0 (15 edges via Bauteiltyp) | **DEMOTE → Bauteiltyp property** (Brand's layers, marginal) |

## Finding 4 — regulation: collapse 6 old labels → 1 evidenced layer
| Label | n | →P | →BTG | verdict |
|---|--:|--:|--:|---|
| **Regulierungsfrage / Nachweisforderung / Regelwerk** (new) | 11/33/91 | — | — | **KEEP** (the evidenced layer) |
| Norm | 103 | 12 | 9 | **DELETE → Regelwerk** (EN1090 ×5 dup, 0 evidence) |
| RechtlicheBedingung | 16 | 5 | 3 | **DELETE → Regelwerk/Frage** |
| Bauproduktstatus | 15 | 0 | 7 | **REPLACE → Regelwerk** (+3 status as property) |
| Geltungsbereich | 6 | **0** | **0** | **DELETE** (orphan; = `Regelwerk-[:GILT_IN_LAND]`) |
| Zertifizierungssystem | 8 | 7 | 0 | **MERGE → Regelwerk** (DGNB/BREEAM/QNG) |
| LCAModule | 5 | 4 | 0 | **MERGE → Regelwerk (EN 15804)** / Kennwert |
| Schadstoff | 13 | 8 | 8 | **KEEP** (re-evidenced via `TYPISCH_BEI_ERA`, sourced) |
| PruefungNachweis | 120 | 43 | 14 | **KEEP methods** (dedup `pn_/pr_`, name) → under Nachweisforderung |
| Leistungsanforderung | 46 | 0 | 9 | **KEEP slim** (consolidate fire/thermal dups) |

→ Six overlapping law/cert labels become **one sourced `Regelwerk`**. Biggest single de-duplication.

## Finding 5 — reuse-process & market: consolidate (redundancy measured)
| Label | n | →P | →BTG | verdict |
|---|--:|--:|--:|---|
| Ressourcenquelle | 6 | 5 | 5 | **KEEP** (where component came from) |
| Wiederverwendungsergebnis | 6 | 2 | 6 | **KEEP** (reuse result) |
| Wiederverwendungsort | 6 | 4 | 5 | **FOLD → property** (245 BTG carry ≥3 of these 4 = redundant) |
| Funktionswechsel | 6 | 0 | 5 | **FOLD → property** |
| Rueckbauverfahren | 6 | 3 | 6 | KEEP (deconstruction) |
| Aufbereitungsverfahren | 6 | 5 | 6 | KEEP (refurbishment) |
| Methode | 6 | 6 | 0 | KEEP (reuse strategy) |
| Prozessphase | 10 | 10 | 10 | KEEP (lifecycle) |
| Wiederverwendungskette | 14 | 0 | 14 | QUESTION (keep only if real chains) |
| Marktmodell | 11 | 0 | 9 | **MERGE → Beschaffung** (86 BTG overlap with Beschaffungsweg) |
| Beschaffungsweg | 10 | 8 | 10 | **KEEP** (merged target) |
| Geschaeftsmodell | 5 | 0(→Akteur 5) | 0 | KEEP (actor business model) |
| Wirtschaft | 12 | 12 | 2 | **DELETE/REBUILD** (mixed-granularity, unsourced) |
| Logistik | 10 | 9 | 10 | KEEP slim |
| MatchingQualitaet | 9 | 9 | 1 | **DELETE → 3 properties** (Geo/Spec/Temporal conflated) |

## Finding 6 — actor classifications (keep; actor-side, not BTG)
`Akteurtyp` (10, →Akteur 10), `Akteurrolle` (24, →Akteur 22): **KEEP** — valid actor taxonomy, but
note they connect to Akteur, not the reuse objects (secondary under priority-2).

## Finding 7 — barriers
`Huerde` (28, →P 28 / →BTG 27, **0 evidence**): **B-clean** (evidenced Rakhshan taxonomy, technical→BTG /
market→Projekt) or **A-delete**. `HuerdeKategorie` (10): **DELETE**.

## Finding 8 — scaffolding / broken (DELETE, confirmed by data)
| Label/Edge | Data | verdict |
|---|---|---|
| Akzeptanz | 7 nodes, →P 0, →BTG 0, →Akteur 0 — **fully orphan** | **DELETE** |
| OntologyAnchor | 2 nodes, 609 `ANCHORED_BY` (scaffolding) | **DELETE** + edge |
| Geltungsbereich | →P 0 / →BTG 0 (orphan) | **DELETE** (see Finding 4) |
| STUB_PROJECT_LINK (165) | placeholder by name | **DELETE/verify** |
| GEHÖRT_ZU (55) | corrupt name, vague | **DELETE/re-type** |

---

## Net result (data-grounded)
- **62 labels → ~34.** Delete ~9 (Akzeptanz, OntologyAnchor, Geltungsbereich, HuerdeKategorie, Wirtschaft,
  MatchingQualitaet, + Norm/RechtlicheBedingung/Bauproduktstatus-as-labels). Merge ~11 (ExternalLink,
  Tool, Tragwerksprinzip, Bauobjektklasse, Zertifizierungssystem, LCAModule, Marktmodell,
  Wiederverwendungsort, Funktionswechsel, Layer→prop, Bauteilebene→prop). Keep the rest.
- **One evidenced `Regelwerk`** replaces 6 overlapping law/cert/scope labels.
- **~2 700 `inferiert`/`unklar` generic edges retired** → re-derived from sourced rules.
- **Evidence backbone kept and elevated** (Quelle/SectionRef/Dossier/ResearchDocument) — corrected from
  the earlier "prune" idea; the data shows these are the graph's actual evidence.
- **Reuse-event 4→2, market 4→2 (drop Wirtschaft), structural 3→2 (fold Tragwerksprinzip)** — each
  backed by measured overlap (245 / 86 / 25).

## Corrections this data pass made to the earlier blueprint
1. **Dossier/SectionRef/ResearchDocument: KEEP (evidence), not prune** — they hold 575+187+69 http sources.
2. **Structural typology: fold only Tragwerksprinzip** (overlap is 25, not large) — keep Bauweise+Bausystem.
3. **Layer → property** (15 edges only); **Bauteilebene → keep/property** (289 edges, real BTG attribute).

## Open decisions (unchanged, aggressive defaults bold)
1. Regulation collapse (Norm/RechtlBed/Bauproduktstatus/Geltungsbereich/Zertifizierung/LCAModule → Regelwerk)? **Yes**
2. Retire generic `inferiert` edges → sourced spine? **Yes**
3. Tier-8 deletions (Akzeptanz/OntologyAnchor/STUB/GEHÖRT_ZU)? **Yes**
4. Consolidations (reuse-event/market/structural/MatchingQualitaet/Wirtschaft)? **Yes**
5. **Huerde: B-clean or A-delete?**
6. Document layer: **KEEP** (data says evidence) — agreed?
