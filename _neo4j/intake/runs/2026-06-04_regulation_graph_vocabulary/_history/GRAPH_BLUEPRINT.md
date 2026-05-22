# Target graph architecture — clean, evidence-first, no duplication

Zoomed-out synthesis of everything in this chat. Goal: a clean graph organised around three
priorities — **(1) evidence-backed first, (2) things that hang off `Projekt`/`Bauteilgruppe` second,
(3) clear connections, no duplication.** Aggressive where cleaning demands it.

## The core principle that reorganises everything

The graph today mixes **three kinds of node** under one flat list of 62 labels:
1. **Entities** — real things (Projekt, Bauwerk, Bauteilgruppe, Akteur, Quelle, Schadstoff…). *Keep.*
2. **Factual attributes** — verifiable classifications of an entity (Material, Bauteiltyp, Status,
   Era, tragend…). *Keep — verifiable without a URL.*
3. **Interpretive tags** — analytic judgements with no source (Huerde, MatchingQualitaet, Wirtschaft,
   the reuse-event enums…). *This is the cut/consolidate zone.*

And it has **4 overlapping "law" layers** (Norm + RechtlicheBedingung + Bauproduktstatus + ad-hoc)
that the **one evidenced `Regelwerk` layer** now replaces. That single consolidation removes the
biggest duplication in the graph.

## Target model — hub & spoke around Bauteilgruppe + Projekt

```
                       ┌─────────────── EVIDENCE BACKBONE ───────────────┐
                       │  Quelle (incl. ExternalLink)  ← every edge cites │
                       └──────────────────────────────────────────────────┘
        Land/Stadt ── Bauwerk ──(era, Bauobjektrolle=Donor/Receiver, Nutzung)
                          │ HAS_BAUWERK
   Akteur ─BETEILIGT_AN─ PROJEKT ─HAT_BAUTEILGRUPPE─▶ BAUTEILGRUPPE ─HAT_BAUTEILTYP▶ Bauteiltyp
   (Typ/Rolle)            │  (Status, Intervention,        │  (Material, Bauweise,
                          │   Prozessphase, Marktmodell)   │   Verbindungstechnik, Layer,
                          │                                │   ZustandsKlasse+Defekt, Kennwert,
                          │                                │   tragend)
                          ▼                                ▼
     ══════════════ EVIDENCED REGULATION LAYER (new, replaces 4 old) ══════════════
     (Projekt|Bauteilgruppe|Material|Bauteiltyp|Bauwerk)
         ─TRIGGERS_REGULIERUNGSFRAGE▶ Regulierungsfrage
         ─ERFORDERT_NACHWEIS▶ Nachweisforderung ◀─ERFUELLT─ PruefungNachweis(methods)
         ─UNTERLIEGT_REGELWERK▶ Regelwerk ─GILT_IN_LAND▶ Land
     Bauwerk(era) ─TYPISCH_BEI_ERA▶ Schadstoff ─▶ Nachweisforderung ─▶ Regelwerk
```

Reuse-process spokes (kept, slim): `Rueckbauverfahren`, `Aufbereitungsverfahren`, `Methode`,
`Prozessphase`, `Wiederverwendungsergebnis`, `Ressourcenquelle` hang off Projekt/Bauteilgruppe.

---

## Per-label disposition (all 62)

### A. Entities & evidence — KEEP (the spine)
| Label | Action |
|---|---|
| Projekt, Bauteilgruppe, Bauwerk, Akteur, Programm, Materialdepot | **KEEP** (hubs) |
| ReuseRule (20/20 evidenced) | **KEEP** — model citizen (sourced) |
| Quelle | **KEEP** (evidence backbone) |
| ExternalLink | **MERGE → Quelle** (it *is* a source; one source model) |
| Kennwert | **KEEP** — ensure value+unit+source, not prose |
| Software + Tool | **MERGE Tool → Software** (same thing) |
| Land, Stadt | **KEEP** |
| Dossier, ResearchDocument, SectionRef | **RESTRUCTURE** — research-note/provenance layer, not domain. Keep *only* as source provenance or prune; today they add 2 700+ edges of document plumbing. **Decide: prune or isolate.** |

### B. Factual component/building attributes — KEEP, consolidate overlaps
| Keep | Consolidate / restructure |
|---|---|
| Material, Bauteiltyp, Nutzung, BauwerkEra, Status, BauaufgabeIntervention, Verbindungstechnik, Layer (Brand's 6), Defekt, ZustandsKlasse, Bauobjektrolle (Donor/Receiver — vital) | **Bauweise** absorbs **Bausystem** + **Tragwerksprinzip** (3 structural typologies → 1, keep named prefab systems as values) · **Bauobjektklasse** → fold non-use values into Nutzung · **Bauteilebene** → make a *property* of Bauteilgruppe (granularity), not a label · **Materialgruppe** keep (coarse roll-up) |

### C. Regulation — COLLAPSE 4 old → 1 evidenced layer (the big win)
| Label | Action |
|---|---|
| **Regulierungsfrage / Nachweisforderung / Regelwerk** (new) | **KEEP** — the evidenced layer |
| **Norm** (103, dup, 0 evidence) | **DELETE → Regelwerk** |
| **RechtlicheBedingung** (16) | **DELETE → Regelwerk/Frage** |
| **Bauproduktstatus** (15) | **REPLACE → Regelwerk**; keep 3 status values as a property |
| **Geltungsbereich** (6) | **DELETE** → expressed by `Regelwerk-[:GILT_IN_LAND]` |
| **Zertifizierungssystem** (8: DGNB/BREEAM/QNG) | **MERGE → Regelwerk** (they're conformity schemes) |
| **LCAModule** (5) | **MERGE → Regelwerk (EN 15804)** or Kennwert |
| **Schadstoff** (13) | **KEEP** — re-evidenced via `TYPISCH_BEI_ERA` (sourced: LfU/TRGS) |
| **PruefungNachweis** (120) | **KEEP methods**, dedup `pn_/pr_`, name them, subordinate to Nachweisforderung |
| **Leistungsanforderung** (46) | **KEEP slim** (consolidate fire/thermal dups ~46→~20), link to Nachweis |

### D. Reuse-process & market — CONSOLIDATE hard (heavy duplication, 0 evidence)
| Family | Action |
|---|---|
| **Market/business:** Marktmodell (370) · Beschaffungsweg (249) · Geschaeftsmodell (98) · Wirtschaft (52) | **MERGE Marktmodell+Beschaffungsweg → one "Beschaffung/Marktmodell"**; keep **Geschaeftsmodell** only for actor business-models; **DELETE Wirtschaft** (mixed-granularity mess) |
| **Reuse-event:** Wiederverwendungsergebnis · Ressourcenquelle · Wiederverwendungsort · Funktionswechsel | **KEEP Wiederverwendungsergebnis + Ressourcenquelle**; **fold Wiederverwendungsort + Funktionswechsel** (→ properties) |
| **Process stages:** Methode · Rueckbauverfahren · Aufbereitungsverfahren · Prozessphase | **KEEP** (genuinely distinct stages) — but accept as factual-unsourced |
| **Logistik** (10) | **KEEP slim** or fold into project properties |
| **MatchingQualitaet** (9) | **DELETE → 3 properties** (Geo / Spec-fit / Temporal) — it conflates 3 axes |

### E. Barriers — RESTRUCTURE or DELETE
| Label | Action |
|---|---|
| **Huerde** (28) | **B-clean** (evidenced barrier vocab, Rakhshan taxonomy, technical→Bauteilgruppe / market→Projekt) **or A-simple delete**. Either way **delete the 930 `inferiert` edges**. |
| **HuerdeKategorie** (10) | **DELETE** (supports Huerde) |

### F. Scaffolding / broken — DELETE (aggressive, justified)
| Label/Edge | Why |
|---|---|
| **Akzeptanz** (7, 0 in-edges, incoherent values) | **DELETE** |
| **OntologyAnchor** (2, 609 ANCHORED_BY) | **DELETE** — import scaffolding, not evidence |
| **STUB_PROJECT_LINK** (165) | **DELETE/verify** — placeholder by name |
| **GEHÖRT_ZU** (55, corrupt name) | **DELETE/re-type** — vague |
| **Wiederverwendungskette** (14) | **QUESTION** — keep only if it adds real chains |

---

## What this achieves

- **62 labels → ~35.** Deletes ~10, merges ~12, restructures ~5.
- **One evidenced law layer** instead of four overlapping ones (Norm/RechtlicheBedingung/Bauproduktstatus/Zertifizierung/Geltungsbereich/LCAModule → Regelwerk).
- **Every regulation edge sourced**; the ~2 700 `inferiert`/`unklar` generic edges retired and re-derived from sourced rules.
- **No duplicate axes**: 3 structural typologies→1, 4 market labels→2, 4 reuse-event→2, building-class folded into use.
- **Everything hangs off Projekt/Bauteilgruppe** or a kept attribute of them; orphans (Akzeptanz) and scaffolding (OntologyAnchor/STUB) gone.

## Priority order to execute (each a reversible, tagged run)
1. **Encoding normalization** (whole graph) — fixes mojibake; cheap, high quality.
2. **Apply the evidenced regulation overlay** (already built & validated).
3. **Regulation collapse**: Norm/RechtlicheBedingung/Bauproduktstatus/Geltungsbereich/Zertifizierung/
   LCAModule → Regelwerk; retire `REFERENZIERT_NORM` etc.; wire Schadstoff/Pruefung/Leistung.
4. **Retire generic edges** (`HAS_RISK_POLLUTANT`, `HAT_PRUEFUNG`, `HAT_LEISTUNGSANFORDERUNG`,
   `HAT_HUERDE`) → replaced by sourced spine.
5. **Tier-F deletions** (Akzeptanz, OntologyAnchor, STUB, GEHÖRT_ZU).
6. **Consolidations** (market, reuse-event, structural typology, MatchingQualitaet, Bauobjektklasse).
7. **Huerde** decision (B-clean or A-delete).
8. **Re-audit** — target: every interpretive edge sourced or gone; one law layer; ~35 clean labels.

## Decisions I need (aggressive defaults in **bold**)
1. Regulation collapse incl. Zertifizierungssystem + Geltungsbereich + LCAModule → Regelwerk? **Yes.**
2. Retire all generic `inferiert` edges in favour of the sourced spine? **Yes.**
3. Tier-F deletions (Akzeptanz, OntologyAnchor/ANCHORED_BY, STUB_PROJECT_LINK, GEHÖRT_ZU)? **Yes.**
4. Market 4→2, reuse-event 4→2, structural 3→1, drop Wirtschaft, MatchingQualitaet→properties? **Yes.**
5. Huerde: **B-clean** (evidenced) or A-delete?
6. Dossier/ResearchDocument/SectionRef: keep as provenance or **prune**?
