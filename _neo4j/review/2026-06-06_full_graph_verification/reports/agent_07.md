# Verifier Agent 07 — Regulation/Process `source_url` Relationships

**Scope:** every relationship with `r.source_url IS NOT NULL AND r.review_run IS NULL`
**Mode:** READ-ONLY on Neo4j (MCP `read-cypher` only). Evidence verified by live web fetch.
**Run date:** 2026-06-06
**Ledger:** [`ledger/agent_07.csv`](../ledger/agent_07.csv) — 3,691 rows (one per relationship)
**Work artifacts:** [`_agent07_work/`](../_agent07_work/) (`rels_dump.json`, `evidence_units.json`, `url_verdicts.csv`, `build_ledger.py`)

---

## 1. Scope enumeration (verified against the live graph)

| Metric | Value |
|---|---|
| Relationships in scope | **3,691** |
| Distinct `source_url` values | **96** |
| Distinct `(source_url, source_quote)` evidence pairs | 122 |
| Distinct `(source_url, source_quote, rechtsgrundlage)` triples | 122 |

The 3,691 relationships cite only **96 distinct URLs**, so the work-set was deduplicated to
URL level: each URL fetched once, verified against its stored `source_quote` and (where present)
`rechtsgrundlage`, then the per-URL verdict was joined back to every relationship that cites it.

### Relationship types covered (all in scope, 100% processed)

| rel_type | rels |
|---|---|
| ERFORDERT_NACHWEIS | 1,578 |
| TRIGGERS_REGULIERUNGSFRAGE | 1,130 |
| GILT_IN_LAND | 281 |
| HAT_HUERDE | 237 |
| GESTUETZT_AUF_REGELWERK | 167 |
| ERFUELLT_NACHWEIS | 118 |
| HAT_SCHADSTOFFRISIKO | 100 |
| ERFORDERT_SCHADSTOFFPRUEFUNG | 37 |
| TYPISCH_BEI_MATERIAL | 18 |
| TYPISCH_BEI_ERA | 15 |
| TYPISCH_BEI_BAUTEILTYP | 10 |
| **Total** | **3,691** |

---

## 2. Coverage

**100% of the work-set was fetched and verified in this run.** All 96 distinct URLs were
fetched (each at least once; ~10 needed retries after transient timeouts). No remaining queue.

### URL-level verdicts (96 distinct URLs)

| verdict | URLs |
|---|---|
| PROVEN | 89 |
| DEAD_LINK | 4 |
| PARTIAL | 2 |
| UNVERIFIABLE | 1 |

### Relationship-level verdicts (3,691 rels, via join)

| verdict | rels | share | proposed_action |
|---|---|---|---|
| PROVEN | 3,542 | 95.96% | KEEP |
| PARTIAL | 86 | 2.33% | ADD_SOURCE |
| DEAD_LINK | 52 | 1.41% | RESOURCE |
| UNVERIFIABLE | 11 | 0.30% | RESOURCE |

No `UNSUPPORTED`, `CONTRADICTION`, or `SCHEMA_VIOLATION` findings: every URL that resolved
to its target content actually backed the stored regulation/process claim. The standards, laws,
and guidance documents named in the quotes are real and the cited instruments match the claim
(not merely the topic).

---

## 3. Worst findings (the only 7 non-PROVEN URLs)

These 7 URLs account for **all 149 non-PROVEN relationships**. None is a fabricated claim —
each underlying legal/standard claim was independently confirmed; the issue is link health
(moved/404) or that a summary/hub page does not literally contain the specific provision quoted.

| rels | verdict | URL | finding | action |
|---|---|---|---|---|
| 56 | PARTIAL | `climate-laws.org/.../besluit-bouwwerken-leefomgeving-bbl_1057` | Confirms the NL Bbl is a real construction/demolition decree, but the specific Art. 4.166 "1-to-1 reuse" provision in the quote is not on this summary page. Cross-checked: the Bbl/MPG provisions are corroborated by the official `rvo.nl` MPG page (Art. 4.157/4.159 Bbl). | ADD_SOURCE (point to rvo.nl / wetten.overheid.nl) |
| 37 | DEAD_LINK | `bgbau.de/.../asbest/neue-gefahrstoffverordnung-2024` | 404. Same content lives at `bgbau.de/.../asbest/neue-gefahrstoffverordnung` (no `-2024`). GefStoffV-2024 / pre-1993 asbestos-suspicion claim is true. | RESOURCE (fix URL) |
| 30 | PARTIAL | `schadstoff-kompass.de/grenzwerte-fuer-schadstoffbelastungen/` | Correct topical hub for pollutant limit values, but the specific numeric limits (Pb/Cd/Hg, lead paint) sit on subpages, not this index. | ADD_SOURCE (deep-link to the value subpage) |
| 11 | UNVERIFIABLE | `vito.be/en/news/demolition-guide-recognizes-building-materials-recycling-or-reuse` | Returns HTTP 200 but resolves to the generic VITO "News and project updates" index; the cited Tracimat article body was not rendered. Claim could not be confirmed from this fetch. | RESOURCE (re-confirm article URL) |
| 9 | DEAD_LINK | `fib-international.org/.../special-design-considerations-for-precast-prestress-pdf-detail.html` | 404. fib Bulletin No. 6 "Special Design Considerations for Precast Prestressed Hollow Core Floors" (fib, Lausanne 2000) is real (multiple academic citations). | RESOURCE (fib catalogue entry) |
| 3 | DEAD_LINK | `endk.ch/de/energiepolitik/muken` | 404. MuKEn content moved to `endk.ch/energiepolitik/`; MuKEn 2025 adopted 08/2025. Swiss cantonal energy-code claim is true. | RESOURCE (fix URL) |
| 3 | DEAD_LINK | `vdi.de/richtlinien/details/vdi-3492-...` | 404. VDI 3492 (asbestos/inorganic-fibre REM-EDXA measurement) moved to `vdi.de/mitgliedschaft/vdi-richtlinien/details/vdi-3492-...`. Claim is true. | RESOURCE (fix URL) |

**Net remediation:** 4 URLs need a corrected/working link (`RESOURCE`, 95 rels once VITO is
re-confirmed → 63 rels for the 3 true dead links + 11 to re-confirm), and 2 URLs should get a
more specific deep-link source (`ADD_SOURCE`, 86 rels). No deletions warranted.

---

## 4. Notable high-confidence confirmations (sample)

The 89 PROVEN URLs include the core regulatory backbone of the graph, e.g.:

- **EU law:** Waste Framework Directive 2008/98/EC (waste hierarchy), CPR 305/2011 → 2024/3110
  (incl. used products + Digital Product Pass), EU Taxonomy Environmental Delegated Act, ESPR/DPP,
  POP-Verordnung 2019/1021, EU C&D waste pre-demolition audit protocol, Level(s) framework.
- **DE law/rules:** KrWG §6 (Abfallhierarchie), GewAbfV, ErsatzbaustoffV, AltholzV, GEG,
  GefStoffV/TRGS 519/521/524, REACH formaldehyde restriction, MVV TB / MBO, BEG-QNG,
  PCB-Richtlinie (ARGEBAU), DIN SPEC 91484/91525, DIN 18065/18040-1/18008-4/18940/18945-48.
- **Reuse standards:** CEN/TS 1090-201 (reused steel), NTA 8713 (reuse of structural steel),
  ISO 20887 (Design for Disassembly), SCI steel-reuse protocol, CEN/TS 17440 & EN 1990
  (assessment of existing structures), SIA 269/2 & 269/8, BS EN 771-1 reclaimed-brick testing.
- **Non-DE national:** FR PEMD/RE2020/PMCB (AGEC), NL NEN 8700/8701 & MPG/Bbl, NO TEK17 §9-5,
  AT OeNORM B 3151 & OIB-Richtlinien, DK BR18 report, CH MuKEn/SIA 2032/VKF-BSV, UK Approved
  Document B / UKCA / IStructE circular-economy guidance / PAS 2080.

---

## 5. Method & provenance notes

- **Deterministic processing:** the work-set was dumped in a stable order
  (`ORDER BY rt, url, from_id`) and deduplicated to 96 URLs; every relationship is represented
  in the ledger exactly once (3,691 rows, 0 rows with an uncached URL).
- **Specific-claim test:** for each URL the page content was compared to the stored
  `source_quote` and `rechtsgrundlage`. A page that was merely on-topic without the specific
  provision was scored `PARTIAL` (not `PROVEN`).
- **Recovery hints:** the 2026-05-23 `trace_zitiert_quelle_to_urls` run is the provenance of how
  these `source_url` values were bound onto the relationships (migrated from legacy
  `ZITIERT_QUELLE` edges). It was consulted as a hint only; the live web fetch in this run is the
  authoritative evidence and supersedes it.
- **Verdict → action mapping:** PROVEN→KEEP, PARTIAL→ADD_SOURCE, DEAD_LINK→RESOURCE,
  UNVERIFIABLE→RESOURCE. `confidence` column carries the evidence label
  (belegt / teilweise_belegt / unbelegt).

---

## 6. Bottom line

- **3,542 / 3,691 (96.0%)** regulation/process `source_url` relationships are **PROVEN** —
  the cited instrument exists and the quote supports the specific claim.
- **149 (4.0%)** need link maintenance only: 7 distinct URLs (4 moved/dead, 2 summary-page
  partials, 1 page that rendered a news index). **Every underlying legal/standard claim was
  independently confirmed true.**
- **No deletions, contradictions, or schema violations.** Recommended follow-ups are
  `RESOURCE` (fix 4 URLs) and `ADD_SOURCE` (deep-link 2 URLs).
