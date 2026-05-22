# Old vocab vs. new research — semantic comparison & cleanup decision

**Goal:** a clean, semantic, evidence-accurate graph. For each of the 7 old labels, does the new
researched vocabulary (Regulierungsfrage / Nachweisforderung / Regelwerk) **replace** it, **complement**
it, or is it a **distinct** axis? → decide delete / keep / rewire.

## TL;DR verdict

| Old label | n | Semantic relation to new vocab | Verdict |
|---|--:|---|---|
| **Norm** | 103 | = **Regelwerk**, but no evidence/URLs + heavy duplication | **REPLACE** → rewire to Regelwerk, delete |
| **Bauproduktstatus** | 15 | conformity routes = **Regelwerk**; 3 are status-enums | **REWIRE** (12→Regelwerk) + keep 3 as status |
| **RechtlicheBedingung** | 16 | = **Regelwerk** + Genehmigung/Haftung **Frage** | **REWIRE** → Regelwerk/Frage, delete label |
| **PruefungNachweis** | 120 | concrete test *methods* under **Nachweisforderung** | **KEEP + REWIRE** (subordinate to nf), dedup |
| **Schadstoff** | 13 | real *substances*; new vocab adds the check+law | **KEEP** → rewire to nf + Regelwerk |
| **Leistungsanforderung** | 46 | required *properties*; proven by Nachweisforderung | **KEEP (slim) + REWIRE**, dedup |
| **Huerde** | 28 | mixed: regulatory barriers vs market/logistics | **SPLIT**: delete regulatory ones, keep market ones |

Net: **2 labels deleted** (Norm, RechtlicheBedingung), **1 mostly deleted** (Bauproduktstatus),
**4 kept but rewired/cleaned**. Result is one law layer (Regelwerk, evidenced) instead of four
overlapping ones (Norm + Bauproduktstatus + RechtlicheBedingung + ad-hoc).

---

## 1. Norm (103) → REPLACE with Regelwerk

**What it is:** standards/norms — EN 1090, Eurocodes, EN 206, EN 771, EN 14081, ISO 20887,
EN 15804, NEN 8700, SIA 269, TEK17, CEN/TS 1090-201, DIN 18008/4074/68800…

**Semantics:** this *is* the Regelwerk layer — but **without source URLs/quotes** and with **massive
duplication**: EN 1090 alone appears as `norm_en_1090`, `norm_en_1090_2`, `norm_din_en_1090_2`,
`norm_nen_en_1090_2`, `norm_pd_cen_ts_1090_201`; Eurocode 3 as `norm_en_1993`, `norm_din_en_1993`,
`norm_eurocode_3`. The 103 nodes collapse to ~30 real standards.

**Overlap:** 25 of ~28 standard families already exist as evidenced Regelwerke.
**Genuine gaps** (in Norm, not yet a Regelwerk): clay-masonry DIN 18940/18945-47, natural-stone test
series (EN 12058/12371/12372/1469/1936/13755/1341/14231), EN 13162 (insulation), EN 998/772 (mortar),
EN 338 (timber classes), NS 3682 (NO), CROW-CUR 4 (NL), CEN/TS 17440, SIA 261/262/263/265/416/500,
RT 2012 (→ superseded by RE2020), Swiss BauPG, CB'23, ISO 14040/14044, precast EN 13369/13224/13747.

**Action:**
1. Rewire `REFERENZIERT_NORM` (ReuseRule/Projekt/Bauteilgruppe → Norm) → `UNTERLIEGT_REGELWERK` → matching Regelwerk.
2. For the ~25 gap standards: migrate as new Regelwerke (quick) or research evidence (better).
3. Delete the `Norm` label once rewired. **`GILT_IN_LAND` from Norm is already reproduced** (evidenced) on Regelwerk.

## 2. Bauproduktstatus (15) → REWIRE (12 → Regelwerk) + keep 3 status-enums

**What it is:** conformity routes — CE (hEN), CE (ETA), Ü-Zeichen, abZ/aBG, ZiE/vBG, UKCA, NTA 8713,
PEMD (FR), Tracimat (BE), BauPG (CH), IBC/JIS… + 3 enums (Bestand vor Ort, Projekt-Freigabe, Status unbekannt).

**Semantics:** the named routes are **Regelwerke** I already have (CPR→CE, `rw_dibt_zie_abz`, `rw_ukca_ce`,
`rw_nta_8713`, `rw_fr_pemd`, `rw_be_tracimat_regional`). `bps_nta_8713` already has a `live_graph_link_hint`.

**Action:** rewire `HAT_BAUPRODUKTSTATUS` to `UNTERLIEGT_REGELWERK`/`ProduktstatusUndLeistungserklaerung`;
**keep** the 3 enums (Bestand vor Ort / Projekt-Freigabe / unbekannt) as a small status value-set (or a
property), since they encode an actual per-component status, not a law.

## 3. RechtlicheBedingung (16) → REWIRE → Regelwerk + Frage, delete label

**What it is:** legal conditions — CPR, EU_Taxonomie, KrWG, DIBt-Zustimmung, Produkthaftung, BauPG,
UKCA/CE for reused steel, Materialpass-Pflicht, + Denkmalschutz, Grade II Listing, Vergaberecht,
Bauordnungsrecht, Boulder ordinance.

**Semantics:** split in two —
- **= Regelwerk** (already have): CPR, EU Taxonomy, KrWG, DIBt ZiE, ProdHaftG, UKCA/CE, Materialpass(Madaster).
- **= Regulierungsfrage**: Denkmalschutz/Grade II Listing/Bauordnungsrecht/Boulder → `GenehmigungsFrage`;
  Vergaberecht/Gewaehrleistung/Produkthaftung → `HaftungGewaehrleistungFrage`/`GenehmigungsFrage`.
- **Genuine gaps** worth new Regelwerke: Denkmalschutz, Grade II Listing, Vergaberecht (procurement).

**Action:** rewire `HAT_RECHTLICHE_BEDINGUNG` to the right Regelwerk/Frage; add 2-3 new Regelwerke
(Denkmalschutz, Vergaberecht); delete the label.

## 4. PruefungNachweis (120) → KEEP as test-method layer, REWIRE under Nachweisforderung

**What it is:** concrete **test methods** — Bohrkern-Druckfestigkeit, Rückprallhammer, Ultraschall,
Zugversuch, Schweissbarkeit, Festigkeitssortierung, Schadstoffanalyse, Sichtprüfung, Karbonatisierung…

**Semantics:** finer-grained than my 33 `Nachweisforderung`. Nachweisforderung = *what must be proven*
(Materialpruefung, Standsicherheitsnachweis, AsbestCheck); PruefungNachweis = *how* (the method). They
are complementary layers, not duplicates. The new EN 13791 / EN ISO 6892 / EN 408 Regelwerke document
exactly these methods.

**Caveats:** (a) duplication — `pn_zugversuch`/`pr_zugversuch`, `pn_sichtpruefung`/`pr_sichtpruefung`
(two prefix families pn_/pr_); (b) many are bare ids without names.

**Action:** **keep**, but (1) dedup pn_/pr_ pairs, (2) add `ERFUELLT_NACHWEIS` (method → Nachweisforderung),
e.g. `pn_bohrkern_druckfestigkeit`→`Materialpruefung`, `pn_schadstoffanalyse`→`Schadstoffpruefung`,
`pn_zugversuch`→`Materialpruefung`. The method layer then hangs cleanly under the requirement layer.

## 5. Schadstoff (13) → KEEP, rewire to Nachweisforderung + Regelwerk

**What it is:** real pollutant substances — Asbest, KMF, PCB, PAK, Schwermetalle, Schimmel, Radon,
Formaldehyd, Holzschutzmittel, Chlorid, Salze, Mineraloel, Bleifarbe.

**Semantics:** **not replaced** — these are entities, not rules. The new vocab adds the *check*
(Nachweisforderung) and the *law* (Regelwerk). Clean 1:1 rewire:

| Schadstoff | → Nachweisforderung | → Regelwerk |
|---|---|---|
| s_asbest | AsbestCheck | TRGS 519, GefStoffV, VDI 3492 |
| s_kmf | KMFCheck | TRGS 521, VDI 3492 |
| s_pcb | PCBCheck | PCB-Richtlinie, POP |
| s_pak | PAKCheck | POP |
| s_schwermetalle / s_bleifarbe | SchwermetallOderBleifarbeCheck | REACH |
| s_formaldehyd | FormaldehydOderEmissionsnachweis / VOC | REACH, AgBB |
| s_holzschutzmittel | HolzschutzmittelCheck | DIN 68800 / AltholzV |
| s_schimmel | MikrobielleBelastungCheck | UBA-Schimmelleitfaden |
| s_radon | Radonmessung | StrlSchG |

**Action:** **keep all 13.** Keep their strong existing edges (`HAS_RISK_POLLUTANT`,
`REQUIRES_VERIFICATION_FOR`, `Land REGULIERT`, `TYPISCH_BEI_ERA/MATERIAL/BAUTEILTYP` — these are good
evidence). Add `Schadstoff → Nachweisforderung` (above). My 5 new `*Check` nf nodes are the bridge.

## 6. Leistungsanforderung (46) → KEEP slim, REWIRE to Frage/Nachweis, dedup

**What it is:** required performance properties — Feuerwiderstand/R90/REI90/F90, Korrosionsschutz,
Schweissbarkeit, Tragfaehigkeit, Waermeschutz, Schallschutz, Dichtheit, Dauerhaftigkeit, Schadstofffreiheit…

**Semantics:** a distinct axis (the *requirement/property*), proven by a Nachweisforderung and governed
by a Regelwerk. Heavily redundant internally (fire = la_brandschutz/la_brandverhalten/la_feuerwiderstand/
la_f90/la_r90/la_rei90).

**Action:** **keep a slimmed set**; dedup the fire/thermal/acoustic clusters; rewire to the matching
Frage/Nachweis (Feuerwiderstand→BrandschutzFrage/Brandschutznachweis; Korrosionsschutz→Materialpruefung;
Schadstofffreiheit→SchadstoffFrage; Waermeschutz→BauphysikFrage). Or fold entirely into Nachweis if you
prefer fewer axes — your call.

## 7. Huerde (28) → SPLIT: delete regulatory, keep market/logistics

**What it is:** reuse barriers. Two semantic groups:
- **Regulatory/technical barriers** (now covered accurately by the new vocab) →
  Brandschutzkonflikt, Bauproduktstatus, Schadstoffbelastung, Gewaehrleistung, Haftung,
  Technische_Freigabe, Hygieneanforderung, Dauerhaftigkeit_Restlebensdauer, Toleranzen,
  Materialqualitaet_unklar, Zustand_unklar, Fehlende_Datenstandards, Kompatibilitaetsproblem.
  → **delete / replace** by the (accurate) Frage/Nachweis edges.
- **Market / logistics / process barriers** (NOT covered by any regulation — a genuinely distinct,
  valuable axis) → Akzeptanzproblem, Mengenunsicherheit, Terminunsicherheit, Verfuegbarkeitsproblem,
  Fehlende_Lagerflaeche, Aufbereitungsaufwand, Entwurfsbindung, Ausschreibungsproblem,
  Heterogenitaet_Chargen, Witterung_Feuchte. → **keep** as a "Hemmnis/Barriere" dimension.

**Action:** keep ~10 market/logistics Huerde; drop the ~13 regulatory ones (their `HAT_HUERDE` edges
were the inaccurate ones you flagged — the new evidence-based edges replace them). Re-derive the kept
ones from real project evidence if needed.

---

## Proposed clean end-state

- **One law layer:** `Regelwerk` (84, evidenced) — absorbs Norm + Bauproduktstatus-routes + RechtlicheBedingung.
- **One requirement layer:** `Regulierungsfrage` (questions) + `Nachweisforderung` (proofs).
- **Method detail:** `PruefungNachweis` (deduped) hung under `Nachweisforderung` via `ERFUELLT_NACHWEIS`.
- **Real entities kept:** `Schadstoff` (wired to checks/laws), slim `Leistungsanforderung`, slim `Huerde` (market barriers only).
- **Deleted labels:** `Norm`, `RechtlicheBedingung`; **mostly deleted:** `Bauproduktstatus` (keep 3 enums).

## What I need from you (per label)

Tick the verdict (or override):
- [ ] **Norm** → REPLACE (rewire to Regelwerk + migrate ~25 gap standards) & delete
- [ ] **Bauproduktstatus** → REWIRE 12→Regelwerk, keep 3 status-enums
- [ ] **RechtlicheBedingung** → REWIRE → Regelwerk/Frage (+3 new Regelwerke) & delete
- [ ] **PruefungNachweis** → KEEP, dedup, link under Nachweisforderung
- [ ] **Schadstoff** → KEEP, wire to checks + laws
- [ ] **Leistungsanforderung** → KEEP slim + rewire (or fold into Nachweis?)
- [ ] **Huerde** → SPLIT (keep ~10 market barriers, drop ~13 regulatory)

Once you decide, I'll build the rewire+delete migration (idempotent, tagged, with rollback) as a
separate reviewable run — and re-run the audit so the end-state is provably clean.
