# FINAL PLAN — clean, evidence-first regulation graph

**Supersedes** the exploratory `PLAN.md`. Synthesises everything in this chat into locked decisions +
a phased, reversible migration. Decisions are final; **execution is still gated per phase** (no DB
write until each phase is approved — DB writes are the only irreversible step).

Principles (in priority order): **(1) evidence-backed wins · (2) hangs off Projekt/Bauteilgruppe ·
(3) clear, de-duplicated connections.** Aggressive where cleaning requires it.

---

## Final decisions (locked)

### A. Apply the evidenced overlay — the new law layer
- Add `Regulierungsfrage` (11) / `Nachweisforderung` (33) / `Regelwerk` (91) — every node+edge sourced.
- Add the 3 729 evidenced anchor edges (`TRIGGERS_REGULIERUNGSFRAGE`, `ERFORDERT_NACHWEIS`,
  `UNTERLIEGT_REGELWERK`) — material/jurisdiction/era/tragend-gated, audited clean (0 mismatches).

### B. Collapse 6 overlapping law/cert labels → `Regelwerk` (biggest de-duplication)
| Old | Action |
|---|---|
| `Norm` (103) | rewire `REFERENZIERT_NORM` → `UNTERLIEGT_REGELWERK`; **delete label** |
| `RechtlicheBedingung` (16) | rewire → Regelwerk/Frage; **delete label** |
| `Bauproduktstatus` (15) | rewire 12 routes → Regelwerk; keep 3 status as a **BTG property**; drop US/JP |
| `Geltungsbereich` (6) | **delete** (= `Regelwerk-[:GILT_IN_LAND]`) |
| `Zertifizierungssystem` (8) | **merge → Regelwerk** (DGNB/BREEAM/QNG) |
| `LCAModule` (5) | **merge → Regelwerk** (EN 15804) |

### C. Keep the real entities — re-evidenced, not deleted
- **Schadstoff** (13): keep; **keep + cite** `TYPISCH_BEI_ERA` (LfU Arbeitshilfe/TRGS — see
  `POLLUTANT_ERA_EVIDENCE.md`); name `s_radon`. **Retire** the 754 `HAS_RISK_POLLUTANT` +
  339 `REQUIRES_VERIFICATION_FOR` (`inferiert`/`material_only`) → replaced by the sourced spine
  `Bauwerk(era)/Material → Schadstoff → Nachweisforderung → Regelwerk`.
- **PruefungNachweis** (120): keep methods; **dedup `pn_`/`pr_` twins, name bare ids**; retire generic
  `HAT_PRUEFUNG` → `ERFORDERT_NACHWEIS` (overlay) + `ERFUELLT_NACHWEIS` (method→Nachweis).
- **Leistungsanforderung** (46): **consolidate ~46→~20** (fire/thermal/acoustic clusters); retire
  generic `HAT_LEISTUNGSANFORDERUNG`; keep as factual property where concrete, else derive.

### D. Huerde — **B-clean: rescue as an evidenced barrier vocabulary** (decision: B)
- **Keep ~11 market/logistics/perception barriers** as a controlled "Reuse-Hemmnis" vocabulary,
  tagged with the Rakhshan (2020) 6-category taxonomy; add the Rakhshan review + FCRBE as backing sources.
- **Delete** the ~13 regulatory Huerde (redundant with the overlay) + `HuerdeKategorie` + all 930
  `inferiert` `HAT_HUERDE` edges.
- **Reconnect with evidence:** technical barriers → Bauteilgruppe (material-derived, cited);
  market/organisational/perception → Projekt (case-documented where the project has a source, else
  taxonomy-derived). Every kept edge carries a source + `basis`. See `HUERDE_RESEARCH.md` and Phase 5.

### E. Consolidate duplicate axes (each backed by measured overlap)
| Merge / restructure | Evidence |
|---|---|
| `Marktmodell` → `Beschaffungsweg` | 86 BTG carry both |
| `Wiederverwendungsort` + `Funktionswechsel` → **BTG properties** | 245 BTG carry ≥3 of the 4 reuse-event labels |
| `Tragwerksprinzip` → `Bauweise` | 4 nodes, 25 Bauwerk overlap |
| `Bauobjektklasse` → `Nutzung` (non-use values kept) | overlap on Depot/Infrastruktur |
| `Layer` → **Bauteiltyp property** (15 edges) · `Bauteilebene` → **BTG property** (289 edges) | marginal/attribute |
| `ExternalLink` → unify under `Quelle` (source model) · `Tool` → `Software` | same concept |

### F. Delete (scaffolding / orphan / broken / unsourced-mess)
`Akzeptanz` (orphan, incoherent) · `OntologyAnchor` + `ANCHORED_BY` (import scaffolding) ·
`STUB_PROJECT_LINK` (placeholder) · `GEHÖRT_ZU` (corrupt/vague) · `Wirtschaft` (mixed-granularity) ·
`MatchingQualitaet` → 3 BTG properties (Geo/Spec/Temporal). Drop the 4 `documented` pollutant edges
(no source even on those).

### G. Keep, untouched — the evidence backbone & factual layer
- **Evidence:** `Quelle`, `ExternalLink`(merged), `SectionRef` (575 http), `Dossier` (source hub),
  `ResearchDocument`, `Kennwert`, `ReuseRule`. *(Correction from data: these are evidence, not plumbing.)*
- **Entities:** Projekt, Bauteilgruppe, Bauwerk, Akteur, Programm, Materialdepot, Software, Land, Stadt.
- **Factual attributes:** Material, Materialgruppe, Bauteiltyp, Nutzung, BauwerkEra, Status,
  BauaufgabeIntervention, Defekt, ZustandsKlasse, Verbindungstechnik, Bauobjektrolle, Bauweise,
  Bausystem, Prozessphase, Rueckbauverfahren, Aufbereitungsverfahren, Methode, Ressourcenquelle,
  Wiederverwendungsergebnis, Logistik, Beschaffungsweg, Geschaeftsmodell, Akteurtyp, Akteurrolle.

---

## Target state
- **62 labels → ~34.** One evidenced `Regelwerk` law layer (was 6 overlapping). ~2 700
  `inferiert`/`unklar` generic edges retired → re-derived from sourced rules. Evidence backbone kept.
  Every regulation edge sourced; every kept tag either factual or sourced. No duplicate axes.

## Phased migration (each = one idempotent, `review_run`-tagged run, individually reversible)
| Phase | Does | Rollback |
|---|---|---|
| 0 | **Backup** + encoding normalization (mojibake, whole graph) | restore backup |
| 1 | Apply evidenced overlay (nodes + 601 backbone + 3 729 anchor edges) | `review_run` delete |
| 2 | Regulation collapse (B): rewire→Regelwerk, merge Zert/LCAModule/Geltungsbereich, delete Norm/RechtlBed | per-phase tag |
| 3 | Schadstoff re-evidence (C) + retire `HAS_RISK_POLLUTANT`/`REQUIRES_VERIFICATION_FOR` | snapshot pre-delete |
| 4 | PruefungNachweis dedup + Leistungsanforderung consolidate + retire their generic edges | snapshot |
| 5 | Delete Huerde (D) + Tier-F deletions | snapshot |
| 6 | Consolidations (E): merges + property migrations | snapshot |
| 7 | **Re-audit** (`audit_edges.py` + gap survey): target 0 generic regulation edges, ~34 labels | — |

Each phase snapshots the nodes/edges it will remove before removing them (à la existing
`_snapshot_predelete.py`), and is tagged so it deletes cleanly in reverse.

## What I need to start
- Confirm the locked decisions (or override any — esp. **Huerde A** and the **document-layer keep**).
- Approve **Phase 0 + 1** to begin (backup + encoding + apply the already-built, validated overlay).
  I'll run phases one at a time, re-auditing after each, nothing further without your go-ahead.

## Document map (for reference)
`STATE_REVIEW.md` (overview) · `GRAPH_BLUEPRINT_DATA.md` (per-label data + verdicts) ·
`AUDIT_7_LABELS_DEEP.md` · `RESCUE_VERDICT.md` · `POLLUTANT_ERA_EVIDENCE.md` · `HUERDE_RESEARCH.md` ·
`REWIRE_REVIEW.md` + `DECISIONS_EXPLAINED.md` · `EVIDENCE_REGELWERK.md` · `GRAPH_CRITICAL_AUDIT.md`.
