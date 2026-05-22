# Semantic proof of the plan — obligations, evidence, and the holes it found

Before executing, the plan is tested against semantic obligations a clean migration must satisfy.
Each is checked against the live graph. **Two genuine holes were found in Phase 3** — the proof works;
they're fixed below.

## Obligations & results

### P1 — Rewire completeness (no orphaned meaning). **PASS**
Every old node slated for replacement maps to a real target.
- Measured: **333 / 341** old nodes map to a real target; **8** are gaps/out-of-scope (3 US/JP →
  delete; 5 EU gaps = Swiss BauPG, CROW-CUR, SIA 500 → logged, not silently dropped).
- ⇒ No meaning is orphaned; the 8 are explicitly tracked.

### P2 — Meaning preservation (rewire = identity/generalization, not distortion). **PASS**
Spot checks confirm old→new is the same standard:
`norm_en_1090 ("EN 1090") → rw_en_1090` · `norm_eurocode_3 ("Eurocode 3") → rw_eurocodes_en_1990_1999`
· `rb_eu_taxonomie ("EU_Taxonomie") → rw_eu_taxonomy` · `bps_nta_8713 ("NTA 8713") → rw_nta_8713`.
Norm/RechtlicheBedingung/Bauproduktstatus values are all standards/laws we hold as evidenced Regelwerke.

### P3 — No information loss on deletion. **CONDITIONAL — 2 holes found in Phase 3 (Schadstoff)**
The plan retires `HAS_RISK_POLLUTANT` (754) and re-derives pollutant risk via sourced era/material
rules. The proof shows that derivation **does not cover everything**:

**Hole 3.1 — 5 pollutants have NO era/material/Bauteiltyp rule** (so they can't be re-derived):
`s_radon`, `s_schimmel`, `s_chlorid`, `s_salze`, `s_mineraloel` (all era=mat=bt=0). These are
**exposure/condition-based, not era-typical**: radon = geology/location (StrlSchG), schimmel = moisture
damage (UBA/Defekt), chloride/salts = exposure, mineral-oil = contamination. Blindly deleting their
`HAS_RISK_POLLUTANT` would **orphan them**.

**Hole 3.2 — era-derivation is too sparse to replace the layer:** only **38 of 228** Bauteilgruppen
with `HAS_RISK_POLLUTANT` have a project with a `Bauwerk`+era. Era-derivation alone covers ~17%.
Material-derivation reaches more (283 BTG have a material) **but only for material-typical pollutants**
(schwermetalle/formaldehyd/…). So a pure "delete + era-derive" loses the pollutant signal for most
components.

→ **Plan fix (Phase 3 refined below).** The rest of P3 is sound:
- Norm/RechtlicheBedingung/Bauproduktstatus → fully covered by Regelwerk (P1/P2). ✓
- `HAT_PRUEFUNG`/`HAT_LEISTUNGSANFORDERUNG`: `inferiert`/`unklar`, replaced by overlay; nodes kept. ✓
- Akzeptanz/OntologyAnchor/STUB/GEHÖRT_ZU: 0 unique information. ✓
- Huerde: **kept** (B-clean), so no loss. ✓

### P3c — PruefungNachweis nodes don't get orphaned. **PASS (with the ERFUELLT_NACHWEIS step)**
65 of 120 methods are reachable *only* via `HAT_PRUEFUNG` today. Retiring it is safe **only because**
Phase 4 adds `(method)-[:ERFUELLT_NACHWEIS]->(Nachweisforderung)` — the method catalog then hangs under
the requirement layer. ⇒ The `ERFUELLT_NACHWEIS` step is **load-bearing**, not optional. (Granularity
note: "this component tested by method X" becomes "component requires Nachweis category Y ← method X".)

### P4 — Consolidations are true equivalences. **PASS**
Measured overlaps justify each merge: Marktmodell∩Beschaffungsweg = 86 BTG; 245 BTG carry ≥3 of the 4
reuse-event labels; Tragwerksprinzip = 4 nodes, 25 Bauwerk overlap with Bauweise. No distinct meaning
is conflated (Geschaeftsmodell kept separate = actor-side; Bausystem kept = named systems).

### P5 — Target model orthogonality (no duplicate axis remains). **PASS (by construction)**
After the plan each kept label occupies a distinct slot: one **law** layer (Regelwerk), one **proof**
(Nachweisforderung) + **method** detail (PruefungNachweis), one **question** (Regulierungsfrage), one
**pollutant** (Schadstoff), one **requirement** (Leistungsanforderung), distinct **physical/condition/
process/market/actor/geo** attributes. The 6→1 law collapse + the merges remove all known duplicates.

### P6 — Priorities satisfied. **PASS**
(1) Evidence: every regulation edge sourced (overlay audited 0 problems). (2) Connectivity: every kept
label connects to Projekt/Bauteilgruppe or a kept entity (per `GRAPH_BLUEPRINT_DATA.md`); orphans
deleted. (3) De-duplication: P4/P5.

### P7 — Referential integrity. **PASS**
`apply_to_graph.py` dry-run: all 135 nodes + 4 330 edges resolve to existing nodes; deletions are
snapshot-guarded and tagged for clean reverse.

---

## Required plan fix — Phase 3 (Schadstoff), refined

The original "retire all `HAS_RISK_POLLUTANT` and era-derive" is **too aggressive** (Holes 3.1/3.2).
Corrected Phase 3:

1. **Derive via BOTH era AND material** (not era only): `Bauwerk(era)→Schadstoff` *and*
   `Material→Schadstoff` (use existing `TYPISCH_BEI_ERA` + `TYPISCH_BEI_MATERIAL`, both now cited to
   LfU/TRGS/REACH). This covers the 8 era/material-typical pollutants across era-known (38) **and**
   material-known (283) components.
2. **Exposure/condition pollutants (the 5):** do **not** delete blindly. Re-route with the right basis:
   - `s_radon` → `Land/Standort` + `StrlSchG` (location/geology, `basis='location'`).
   - `s_schimmel` → `Defekt`(moisture) + UBA guide (`basis='condition'`).
   - `s_chlorid`, `s_salze`, `s_mineraloel` → `Defekt`/exposure (`basis='condition/exposure'`), cited to
     VDI 6202 / LfU.
3. **Retire `HAS_RISK_POLLUTANT` only where a sourced replacement exists.** For any component-pollutant
   link with **no** derivation and **no** condition basis, **flag** it `screening_unverified` and put
   it to you for an explicit drop/keep call — never silently delete a signal we couldn't reproduce.
4. Acceptance (updated): every of the 13 Schadstoff reachable by a *sourced* path (era, material,
   location, or condition); count of `screening_unverified` reported; 0 silent losses.

This keeps the migration **evidence-first without information loss**.

## Verdict
The plan is **semantically sound** for Phases 0,1,2,4,5,6,7 as written, and for Phase 3 **after the
refinement above**. The two holes were real and are now closed; `ERFUELLT_NACHWEIS` (Phase 4) is
confirmed load-bearing. No duplicate axis survives; every kept edge is factual or sourced.
