# Remediation R06 — Dead Regulation URLs (Agent 07)

**Agent:** R06 · **Date:** 2026-06-06 · **Scope:** Agent 07 `DEAD_LINK` + `UNVERIFIABLE` / `RESOURCE`
**Input:** [`ledger/agent_07.csv`](../ledger/agent_07.csv) · **Output ledger:** [`ledger/remediation_r06.csv`](../ledger/remediation_r06.csv)
**Patch:** [`patches/remediation_r06_regulation_urls.patch.jsonl`](../patches/remediation_r06_regulation_urls.patch.jsonl)

## Summary

| Metric | Count |
|---|---:|
| Scope relationships | 63 |
| Distinct dead/unverifiable URLs | 5 |
| Fixed (confirmed alternate) | 63 |
| Deferred (no confirmed fix) | 0 |
| Patch ops (`set_rel_properties`) | 63 |

### URL-level fixes

| rels | agent07 verdict | old URL | new URL | R06 verdict | note |
|---:|---|---|---|---|---|
| 37 | DEAD_LINK | `https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefa…` | `https://bauportal.bgbau.de/bauportal-12025/rund-um-die-bg-bau/novellie…` | PROVEN | Moved/dead link; confirmed alternate at https://bauportal.bgbau.de/bauportal-12025/rund-um-die-bg-bau/novellierung-gefahrstoffverordnung-umgang-mit-asbest |
| 11 | UNVERIFIABLE | `https://vito.be/en/news/demolition-guide-recognizes-building-materials…` | `https://ovam.vlaanderen.be/bouw-sloopopvolging` | PROVEN | Moved/dead link; confirmed alternate at https://ovam.vlaanderen.be/bouw-sloopopvolging |
| 9 | DEAD_LINK | `https://www.fib-international.org/publications/fib-bulletins/special-d…` | `https://shop.fib-international.org/publications/fib-bulletins/228-spec…` | PROVEN | Moved/dead link; confirmed alternate at https://shop.fib-international.org/publications/fib-bulletins/228-special-design-considerations-for-precast-prestress-hollow-core-floors-pdf |
| 3 | DEAD_LINK | `https://www.endk.ch/de/energiepolitik/muken…` | `https://endk.ch/energiepolitik/` | PROVEN | Moved/dead link; confirmed alternate at https://endk.ch/energiepolitik/ |
| 3 | DEAD_LINK | `https://www.vdi.de/richtlinien/details/vdi-3492-messen-von-innenraumlu…` | `https://www.vdi.de/mitgliedschaft/vdi-richtlinien/details/vdi-3492-inn…` | PROVEN | Moved/dead link; confirmed alternate at https://www.vdi.de/mitgliedschaft/vdi-richtlinien/details/vdi-3492-innenraumluft-aussenluft-messen-anorganischer-faserfoermiger-partikel-rasterelektronenmikroskopisches-verfahren |

## Method

- Re-fetched each stored `source_url` and candidate alternates from Agent 07 notes.
- Confirmed fix only when HTTP 200 and page body contains claim-specific needles.
- Paywalled/login-gated pages marked **UNVERIFIABLE**, never **PROVEN**.
- Patch uses `set_rel_properties` with `source_url` only (non-destructive).

## Apply

✅ **Applied** 2026-06-06: **63 `set_rel_properties` / 0 errors**
([`apply_reports/remediation_r06_regulation_urls.patch.apply_report.md`](../apply_reports/remediation_r06_regulation_urls.patch.apply_report.md)).
Graph unchanged at **2 295 nodes / 15 327 rels** (property-only updates).

Generated 2026-06-06 16:55 UTC · applied 16:56 UTC.
