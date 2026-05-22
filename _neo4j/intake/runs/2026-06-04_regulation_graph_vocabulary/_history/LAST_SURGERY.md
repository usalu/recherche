# LAST SURGERY — final cleaning & connection plan (current live graph)

State: `mit-bestand` post-migration = **2 273 nodes · 15 118 rels · 51 labels · 48 reltypes.** The big
migration is done and clean (sources→properties, no `Quelle`; one node per standard; spine intact; 0
duplicate/parallel edges; confidence numeric). This plan closes the **only remaining gaps** found by a
full re-analysis. Each item: what · why · risk · how. Safe order at the end. Reversible (Phase-0 backup
exists: `_neo4j/review/backups/20260605T152248Z-mit-bestand`).

## What's already clean (no action)
Regulation edges 100 % sourced — `ERFORDERT_NACHWEIS` (1483), `TRIGGERS_REGULIERUNGSFRAGE` (1100),
`GILT_IN_LAND` (281), `GESTUETZT_AUF_REGELWERK` (167), `ERFUELLT_NACHWEIS` (118), `HAT_HUERDE` (237),
`TYPISCH_BEI_ERA`/`TYPISCH_BEI_BAUTEILTYP`. Factual edges (NUTZT_MATERIAL, HAT_BAUTEILTYP, HAT_PROZESSPHASE…)
are 0 % sourced **by design** (observed facts, not inference — leave them).

---

## S1 — Finish the Schadstoff evidence (the one real regulation gap)  · risk: MED
**Problem:** the pollutant sub-layer is the *only* unsourced regulation evidence:
- `HAT_SCHADSTOFFRISIKO` 100 edges — 0 % sourced (has `evidence_status`, no `source_url`).
- `ERFORDERT_SCHADSTOFFPRUEFUNG` 37 edges — 0 % sourced. (These two = the 137 "status-without-source".)
- `TYPISCH_BEI_MATERIAL` only 24 % sourced.
- `s_radon` is **unreachable** (no risk/typical/prüfung edge).
**Fix:** source these from the pollutant×era/material matrix (`POLLUTANT_ERA_EVIDENCE.md` — LfU
Arbeitshilfe/TRGS/REACH): `SET r.source_url/source_quote/confidence` on the existing edges (don't
duplicate); route `s_radon` → location/`StrlSchG`; tag any edge with no backing as
`screening_unverified` and list it for an explicit drop/keep.
**Accept:** 0 edges with `evidence_status` but no `source_url` (except the reported `screening_unverified`
set); all 13 `Schadstoff` reachable by a sourced path.

## S2 — Connect the 30 connectable component groups  · risk: LOW
**Problem:** 110 `Bauteilgruppe` don't reach the regulation layer; **30 of them have a material** (so the
overlay should have linked them — a real coverage gap). 80 have no material → expected, leave.
**Fix:** re-run the material-derivation (`connect_anchors_to_vocab.py` logic) for those 30 → add the
sourced `ERFORDERT_NACHWEIS`/`TRIGGERS_REGULIERUNGSFRAGE` they're missing.
**Accept:** every `Bauteilgruppe` *with a material* reaches the regulation layer; coverage 254→284.

## S3 — Orphans & duplicates  · risk: LOW–MED
- **Duplicate actors:** `Werner Sobek` ×2, `Gruner ReUse` ×2 → **merge** (keep one, redirect edges).
- **5 orphan `Projekt` (0 edges):** `p_lysp8` is a *real building project* — **investigate/restore its
  links** (likely lost connections); the other 4 (`p_fcrbe`, `p_eth_circular…`, `p_rcmi_concular`,
  `p_refair_bordeaux`) are **networks/platforms mis-typed as Projekt** → reclassify to `Programm`/`Akteur`
  or delete. + 1 orphan `Programm` → merge/delete.
- **11 unused controlled-vocab values** (Verbindungstechnik ×4, Land ×2 [Ukraine/Italien], Akteurrolle ×2,
  Ressourcenquelle ×1, Bauteiltyp ×1, Bausystem ×1) → **delete** (unused enum entries; keep the catalog tight).
**Accept:** 0 orphan nodes (except deliberately-kept reference Länder, if you choose); 0 duplicate actor names.

## S4 — Optional structural tidy (your call)  · risk: LOW
- **Fold `ERFORDERT_SCHADSTOFFPRUEFUNG`(37) → `ERFORDERT_NACHWEIS`** (target `nf_schadstoffpruefung`):
  removes a near-duplicate reltype (48→47), unifies "requires a proof".
- **Unify the 11 `…recht` labels → one `Regelwerk` + `domain` property** (closer to your "one card per law"
  wording; 51→~41 labels). *Or* keep the domain split (queryable by domain — also valid). **Decision needed.**

## S5 — Final audit & sign-off  · risk: none
Re-run the gates; write `FINAL_AUDIT_REPORT.md`; refresh `AGENTS.md` (its 2 580-node figure is stale →
2 273). Targets: **0** status-without-source (bar reported screening), **all 13 Schadstoff** sourced-reachable,
**0** orphan nodes, **0** duplicate actors, BTG reg-coverage = all material-bearing groups, labels ~41
(if S4 unify) / 51 (if kept), reltypes ≤48; `audit_edges.py` 0; `_gap_survey.py` 0.

---

## Safe order (each: dry-run → review → commit → snapshot, reversible)
1. **S1** Schadstoff evidence (source the 137 + radon).
2. **S2** connect the 30 material-bearing groups.
3. **S3** merge duplicate actors → reclassify/restore orphan projects → delete unused vocab values.
4. **S4** (if approved) fold the schadstoff-prüfung reltype / unify `…recht` labels.
5. **S5** final audit.

## Decisions before I cut
1. **S3 orphan projects:** restore `p_lysp8` from intent/data, and delete-or-reclassify the 4 network ones? (default: reclassify networks → `Programm`, keep/repair LysP8)
2. **S3 unused vocab + orphan Länder:** delete all unused values (incl. Ukraine/Italien)? (default: yes)
3. **S4 `…recht`:** unify to one `Regelwerk`+`domain` (→~41 labels) or keep the 11 domain labels? (default: keep)
4. **S4 reltype fold:** fold `ERFORDERT_SCHADSTOFFPRUEFUNG`→`ERFORDERT_NACHWEIS`? (default: yes)
