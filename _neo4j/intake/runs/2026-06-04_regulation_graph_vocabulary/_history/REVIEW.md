# REVIEW — Regulation vocabulary overlay for `mit-bestand`

**Run:** `regulation_graph_vocab_2026_06_04`  ·  **Status:** awaiting your approval  ·  **Nothing is written yet.**

This overlay adds a regulation/proof layer on top of the existing graph and connects it to your
Projekte, Materialien, Bauteilgruppen and Bauteiltypen — every connection backed by a real
source URL + quote, derived from facts already in the graph (material, country, load-bearing,
intervention, building era). **No existing nodes or edges are changed or deleted.**

## 1. What gets added

**3 new node types** (the vocabulary):

- **Regulierungsfrage** (11) — the regulatory questions a reuse project raises
- **Nachweisforderung** (33) — the concrete proofs/checks required
- **Regelwerk** (84) — the actual laws/standards (each web-researched, with URL)

**New connections (edges), all carrying `source_url`, `source_quote`, `confidence`, `review_run`):**

| Edge | Meaning | Count |
|---|---|---:|
| anchor → Regulierungsfrage | which questions apply | 1044 |
| anchor → Nachweisforderung | which proofs are required | 1329 |
| anchor → Regelwerk | which laws govern | 1233 |
| + vocabulary backbone (Frage→Nachweis→Regelwerk→Land/Material/Bauteiltyp) | | 552 |

**Total: 128 new nodes + ~4 158 new edges**, across 349 of your existing anchors.

## 2. The 11 Regulierungsfragen (questions)

- ReuseDokumentationFrage
- RueckbauUndBauteilernteFrage
- BauproduktstatusFrage
- TragwerkssicherheitFrage
- BrandschutzFrage
- BauphysikFrage
- SchadstoffFrage
- HygieneElektroFunktionFrage
- GenehmigungsFrage
- HaftungGewaehrleistungFrage
- UmweltvertraeglichkeitOekobilanzFrage

## 3. The 33 Nachweisforderungen (proofs)

Bauteilidentifikation, HerkunftsUndRueckbaudokumentation, ZustandsUndMassaufnahme, Standsicherheitsnachweis, Materialpruefung, Brandschutznachweis, Bauphysiknachweis, Schadstoffpruefung, ProduktstatusUndLeistungserklaerung, GenehmigungsOderZustimmungsbedarf, Befestigungsnachweis, Elektrosicherheitsnachweis, HygieneUndReinigungsnachweis, FormaldehydOderEmissionsnachweis, AsbestCheck, KMFCheck, PCBCheck, PAKCheck, SchwermetallOderBleifarbeCheck, HolzschutzmittelCheck, SicherheitsglasInfo, U_WertOderEnergieInfo, DauerhaftigkeitRestlebensdauer, SchadstoffkatasterErkundung, OekobilanzEPD, MaterialpassRessourcenpass, MineralischeErsatzbaustoffGuete, RcGesteinskoernungEignung, Radonmessung, VOC_Emissionsnachweis, MikrobielleBelastungCheck, BarrierefreiheitNachweis, AbsturzsicherungNachweis


## 4. The 84 Regelwerke (laws/standards), by domain

**Reuse/Rückbau & Abfall** (15): DIN SPEC 91484, DIN SPEC 91525, VDI 6210 Blatt 1, KrWG §6/§7/§8, Gewerbeabfallverordnung (GewAbfV), EU Waste Framework Directive 2008/98/EC, EU C&D Waste Management Protocol (2024), ISO 20887 (Design for Disassembly/Adaptability), OENORM B 3151, France Diagnostic PEMD (loi AGEC), France REP PMCB (filiere batiment), Norway TEK17 (ombrukskartlegging), Belgian regional rules / Tracimat, FCRBE Reuse Toolkit / Reclamation Audit, VOB/C ATV DIN 18459 (Abbruch/Rückbau)

**Tragwerk & Material-Prüfung** (19): CEN/TS 1090-201:2024, SCI P427, NTA 8713 (Reuse of structural steel), EN/DIN EN 1090, EN 1090-2 / EN 14399 (bolt reuse limits), Eurocodes EN/DIN EN 1990-1999, EN ISO 6892-1 (Zugversuch Metalle), DIN 4074 / EN 14081 (Holzsortierung), EN 408 (Holz mechanische Eigenschaften), EN 13791 / EN 12504 (In-situ Beton), SIA 269, SIA 269/2 (Erhaltung Betonbau), DAfStb-Richtlinie R-Beton, fib Bulletins (precast concrete reuse), EN 1168 (Hohlplatten/Hollow-core slabs), EN 1992-4 (Befestigungen in Beton), NEN 8700-serie (bestaande bouw), EN 771 (reclaimed masonry units), Naturstein-Wiederverwendung (guidance)

**Bauproduktstatus & Bauteilnormen** (10): EU CPR 2024/3110, EU CPR 305/2011, DIBt ZiE/vBG/abZ/aBG, MVV TB / VV TB, MBO/LBO, UKCA / CE marking, EN 14351-1/-2 (Fenster & Türen), EN 13830 (Vorhangfassade/Curtain Walling), DIN 18065 (Gebäudetreppen/Geländer), ESPR / Digital Product Passport

**Schadstoffe** (14): TRGS 519, TRGS 521, TRGS 524, GefStoffV (2024), REACH Anhang XVII Eintrag 77, POP-Verordnung (EU) 2019/1021, VDI/GVSS 6202 Blatt 1, PCB-Richtlinie (ARGEBAU), DIN 68800 / AltholzV, AgBB-Schema / DIN EN 16516 (VOC), VDI 3492 (Faser-/Asbestmessung), UBA-Schimmelleitfaden, StrlSchG (Radon), Ersatzbaustoffverordnung (EBV)

**Brandschutz** (6): DIN EN 13501, DIN 4102/4108/4109, VKF Brandschutzvorschriften (CH), UK Building Regs Approved Document B, OIB-Richtlinien, DIN 18008

**Bauphysik/Energie & Ökobilanz** (13): GEG, SIA 380/1, SIA 2032 (Graue Energie), Switzerland MuKEn, France RE2020, Netherlands MPG (MilieuPrestatie Gebouwen), UK PAS 2080:2023 (whole-life carbon), EN 15804 / EN 15978 (EPD/LCA), EU Taxonomy (Circular Economy TSC), EU Level(s) framework, Madaster / Gebaeuderessourcenpass, QNG / DGNB Zertifizierung, Flat-glass / IGU reuse guidance (Glass for Europe)

**Genehmigung/Recht & Funktion** (6): Dutch Bbl, Denmark BR18 (Bygningsreglementet), ProdHaftG / BGB §823, DGUV V3 / DIN VDE 0100-600 / 0105-100, VDI 6023 / VDI 6022 (Hygiene), DIN 18040 (Barrierefreies Bauen)


## 5. Worked examples (how to read a connection)


### MATERIAL: `mat_stahl` — Stahl
- **Questions:** BauproduktstatusFrage, TragwerkssicherheitFrage
- **Required proofs:** Befestigungsnachweis, Materialpruefung, ProduktstatusUndLeistungserklaerung, Standsicherheitsnachweis
- **Governing laws:** CEN/TS 1090-201:2024, EN 1090-2 / EN 14399 (bolt reuse limits), EN ISO 6892-1 (Zugversuch Metalle), EN/DIN EN 1090, NTA 8713 (Reuse of structural steel), SCI P427
- *example evidence:* Material 'mat_stahl' wird durch rw_cen_ts_1090_201 (CEN/TS 1090-201:2024) geregelt
  → https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024

### BAUTEILGRUPPE: `bg_mehrere_dach_grubenstrasse_sheets` — Dachbleche
- **Questions:** BauproduktstatusFrage, TragwerkssicherheitFrage
- **Required proofs:** Befestigungsnachweis, Materialpruefung, ProduktstatusUndLeistungserklaerung, Standsicherheitsnachweis
- **Governing laws:** CEN/TS 1090-201:2024, EN 1090-2 / EN 14399 (bolt reuse limits), EN ISO 6892-1 (Zugversuch Metalle), EN/DIN EN 1090
- *example evidence:* Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [tragend unbekannt -> strukturelle Relevanz zu pruefen]
  → https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024

### PROJEKT: `p_55_great_suffolk_street_london` — 55 Great Suffolk Street
- **Questions:** UmweltvertraeglichkeitOekobilanzFrage
- **Required proofs:** OekobilanzEPD
- **Governing laws:** UK PAS 2080:2023 (whole-life carbon)
- *example evidence:* Projekt in ['land_vereinigtes_koenigreich']; Reuse-Projekt; rw_uk_pas2080 gilt
  → https://www.bsigroup.com/en-US/insights-and-media/insights/brochures/pas-2080-carbon-management-in-infrastructure-and-built-environment/

## 6. Deliberately NOT connected (honest gaps)

- Materials with no researched rule: Kunststoff, Dämmstoff, Bitumen, Lehm, Stroh, Textil, Kupfer/Messing, PCM.
- `mat_faserzement` (Eternit): left unmapped — old fibre-cement is often asbestos, modern is not; needs your call.
- Non-load-bearing steel railings in non-DE projects (no EU-wide non-structural steel reuse rule).
- The old `HAT_HUERDE` / `REFERENZIERT_NORM` edges were **not** used (you flagged them as inaccurate).

## 7. Quality checks already run

- `audit_edges.py`: **0** jurisdiction mismatches, **0** structural rules on non-load-bearing parts, **0** bad targets, confidence all in (0,1].
- `apply_to_graph.py` dry-run: **all 128 nodes + edges resolve** against the live graph (validated, no writes).

## 8. To import (only after you approve)

```powershell
python apply_to_graph.py            # dry-run, no writes (re-check)
python apply_to_graph.py --commit   # writes the overlay
```
**Full rollback (one step, removes everything this run added):**
```cypher
MATCH ()-[r {review_run:'regulation_graph_vocab_2026_06_04'}]->() DELETE r;
MATCH (n {source_scope:'regulation_graph_vocab_2026_06_04'}) DETACH DELETE n;
```

## 9. Sign-off checklist

- [ ] Vocabulary (questions / proofs / laws) makes sense
- [ ] Domain coverage is right for your scope
- [ ] Worked examples look correct
- [ ] Gaps in §6 are acceptable (or tell me to research them)
- [ ] OK that national rules apply only in their country
- [ ] Approve commit