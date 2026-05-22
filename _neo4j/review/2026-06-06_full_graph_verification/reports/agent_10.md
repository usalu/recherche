# Verifier Agent 10 — Platforms, Depots, Programmes, Software

**Database:** `mit-bestand` (READ-ONLY; no graph mutation performed)
**Date:** 2026-06-06
**Ledger:** [`ledger/agent_10.csv`](../ledger/agent_10.csv) — 175 claim rows
**Method:** Evidence Gate (§3) — live `read-cypher` enumeration + `WebFetch`/`WebSearch`. All proposed actions are for the Aggregator/human only.

## 1. Scope recap (authoritative enumeration)

| Work-set | Cypher | Count |
|---|---|---|
| `Software` nodes | `MATCH (n:Software) RETURN n` | 20 |
| `Tool` nodes | `MATCH (n:Tool) RETURN n` | 1 |
| `Materialdepot` nodes | `MATCH (n:Materialdepot) RETURN n` | 22 |
| `Programm` nodes | `MATCH (n:Programm) RETURN n` | 31 |
| `NUTZT_SOFTWARE` rels | `MATCH ()-[r:NUTZT_SOFTWARE]->() RETURN r` | 54 |
| `TEIL_VON_PROGRAMM` rels | `MATCH ()-[r:TEIL_VON_PROGRAMM]->() RETURN r` | 35 |
| `BETRIEBEN_VON` rels | `MATCH ()-[r:BETRIEBEN_VON]->() RETURN r` | 9 |
| `ERHALT_FOERDERUNG_DURCH` rels | `MATCH ()-[r:ERHALT_FOERDERUNG_DURCH]->() RETURN r` | 3 |
| **Total claims** | | **74 nodes + 101 rels = 175** |

All counts match the plan (§6.2 nodes 74; §6.1 rels 101). Note: several `tool_*`-id nodes (e.g. `tool_qflow`, `tool_bauteilkatalog`, `tool_hts_stockmatcher`) carry the **`Software`** label, not `Tool`; the only `:Tool`-labelled node is `tool_swiss_inv`.

## 2. Counts by verdict

| Verdict | Nodes | Rels | Total |
|---|---:|---:|---:|
| PROVEN | 15 | 7 | 22 |
| PARTIAL | 3 | 12 | 15 |
| UNSUPPORTED | 2 | 0 | 2 |
| UNVERIFIABLE | 3 | 1 | 4 |
| MISSING_EVIDENCE | 46 | 55 | 101 |
| SCHEMA_VIOLATION | 5 | 26 | 31 |
| **Total** | **74** | **101** | **175** |

Proposed-action mix: KEEP 25 · ADD_SOURCE 73 · ESCALATE_HUMAN 56 · MERGE_DUPLICATE 11 · RESOURCE 7 · RELABEL 2 · FIX_PROPERTY 1.

## 3. Systemic findings

1. **Every `Materialdepot` is unsourced (22/22).** Confirms the plan's top red flag. **17 of 22 are explicit placeholders** — names literally say *"Unbekannte Quelle / Spenderquelle / Donorquellen"* ("unknown source") or *"Aggregierte … Donorquellen"* ("aggregated donor sources"). These are modelling artifacts, not real findable depots → `ESCALATE_HUMAN` (deprecate/relabel). The remaining **5 are real named sites** (Bellastock Île-Saint-Denis, Cleveland Steel & Tubes stock, CRCLR/Kindl Hall, ELYS-Areal, Verbiest) → `ADD_SOURCE`.
2. **`Qflow` is mis-sourced.** Both `software_qflow` and `tool_qflow` cite **`qflow.io`**, which is *"Qflow for events … a Wiretouch Business"* — an unrelated **events check-in** company. The real construction Qflow is **Qualis Flow Ltd, `qualisflow.com`** (London, 2018; materials/waste/carbon data platform). Verdict `UNSUPPORTED` → `RESOURCE`. (Bonus: `qualisflow.com` even lists *Grosvenor* as a client, corroborating the Grosvenor donor node.)
3. **Five `Programm` nodes are German category words, not programmes:** `prog_pilotprojekt` ("Pilotprojekt"), `prog_wettbewerb` ("Wettbewerb"), `prog_foerderprogramm` ("Foerderprogramm"), `prog_forschungsprojekt` ("Forschungsprojekt"), `prog_reallabor` ("Reallabor"). 20 `TEIL_VON_PROGRAMM` edges point real projects at these non-entities → `SCHEMA_VIOLATION`/`ESCALATE_HUMAN`. They should become vocabulary/`type` properties, not nodes.
4. **Duplicate / generic-concept Software nodes self-wire via `NUTZT_SOFTWARE`.** `software_qflow ↔ tool_qflow`, `software_bim ↔ tool_bim_bauteilkatalog`/`tool_bauteilkatalog`, `software_concular ↔ software_restado` form bidirectional "software uses software" edges with no factual basis → `MERGE_DUPLICATE`/`SCHEMA_VIOLATION`. `software_concular ↔ software_restado` is wrong semantics: restado *"ist eine Marke der Concular GmbH"* (a brand), not a "uses" relation → `RELABEL`.
5. **No on-edge evidence for usage/membership/funding edges.** All `NUTZT_SOFTWARE`, `TEIL_VON_PROGRAMM`, `ERHALT_FOERDERUNG_DURCH` carry only `id` (no `source_url`/`evidence_url`). Even where the target platform is confirmed real (Concular, Restado, Opalis), the *specific usage claim* is unsourced → `MISSING_EVIDENCE`/`ADD_SOURCE` (recover from the named project dossiers).
6. **`BETRIEBEN_VON` operator facts are mostly solid (7 of 9 PROVEN/strong).** The directly-verifiable imprints/about pages confirm operators (Salvo, materialnomaden, ZirkuLIE, Concular). The one structural caveat: `software_opalis BETRIEBEN_VON opalis` — the real operator per `opalis.eu/about` is **Rotor (+Bellastock)**, so the `opalis` *actor* node is likely redundant with Rotor → `ESCALATE_HUMAN`.

## 4. Ten worst findings (with quotes)

1. **`software_qflow` / `tool_qflow` mis-sourced** (A10-N-009, A10-N-019) — `UNSUPPORTED`. `qflow.io/about/`: *"About Qflow for events … (A Wiretouch Business)"*. Construction Qflow is `qualisflow.com`. → `RESOURCE` + `MERGE_DUPLICATE`.
2. **17 placeholder `Materialdepot` nodes** (A10-N-023/24/27/29–41/43) — `MISSING_EVIDENCE`. e.g. *"Unbekannte Quelle der wiederverwendeten Ziegel"*, *"Aggregierte Pariser Materialquellen"*. → `ESCALATE_HUMAN`.
3. **5 category-word `Programm` nodes** (A10-N-052/53/60/64/74) — `SCHEMA_VIOLATION`. e.g. name = *"Pilotprojekt"*, *"Wettbewerb"*. → `ESCALATE_HUMAN`.
4. **20 `TEIL_VON_PROGRAMM` edges to those non-entities** (A10-R-056…088) — `SCHEMA_VIOLATION`. Real projects linked to a category word, not a programme.
5. **`prog_mas_dfab` name/source mismatch** (A10-N-058) — `PARTIAL`. Cited ETH page is *"'Digital Creativity for Circular Construction' … developed by Professor Catherine De Wolf"*, **not** MAS DFAB / Gramazio Kohler as the node claims. → `FIX_PROPERTY`.
6. **`software_concular ↔ software_restado` mislabelled** (A10-R-049, A10-R-051) — `PARTIAL`. `restado.de` imprint: *"restado ist eine Marke der Concular GmbH"* — a brand, not a "uses" relation. → `RELABEL`.
7. **`software_opalis BETRIEBEN_VON opalis` operator attribution** (A10-R-098) — `PARTIAL`. `opalis.eu/about`: *"The website Opalis was founded by Rotor vzw/asbl … maintained and updated by Rotor and Bellastock"*. Actor `opalis` redundant with Rotor. → `ESCALATE_HUMAN`.
8. **`tool_hts_stockmatcher` dead source** (A10-N-016) — `PARTIAL`. Cited `heynetillettsteel.com/research/` returns **404**; base site confirms *"HTS+ … in-house software developers"* but not the exact "Stockmatcher" tool. → `RESOURCE`.
9. **Unidentifiable software stubs** `software_llmnt`, `tool_rcmi` (A10-N-006, A10-N-020) — `MISSING_EVIDENCE`. No source, not identifiable from the graph. → `ESCALATE_HUMAN`.
10. **Generic-concept "software" nodes** `software_bim`, `software_recrete_finite_element_model`, `tool_bauteilkatalog`, `tool_bim_bauteilkatalog`, `tool_material_passports_maconda` (A10-N-001/10/14/15/17) — `MISSING_EVIDENCE`/`SCHEMA`. Concepts/methods, not named products. → `ESCALATE_HUMAN`/`MERGE_DUPLICATE`.

## 5. Confirmed real (PROVEN) — KEEP

- **Software/Tool (6):** Cirkla-Scan, Concular, Opalis, Planular, Restado, Swiss Inv — all confirmed on the vendor's own page (e.g. Concular *"Zirkuläres Bauen & Urban Mining vom Marktführer"*; restado imprint; `cirkla.ch/swiss-inv`).
- **Programme (9, incl. cross-refs):** FCRBE, Holzbau-Offensive BW, Innosuisse legal-framework, Interreg NWE, PREC, PREUSE, Stuttgart 210, SWIRCULAR, Architecture of Reuse Brussels. Notable cross-reference: `opalis.eu/about` simultaneously confirms **FCRBE**, **Interreg NWE**, **PREC**, **PREUSE**, **Rotor**, and **Bellastock**.
- **`BETRIEBEN_VON` (PROVEN):** SalvoWEB→Salvo, re:store→materialnomaden, ZirkuLIE→Stiftung Lebenswertes Liechtenstein, Concular platform→Concular, FCRBE→Interreg NWE; Rotor→Opalis.

## 6. Escalated to human (56 items — see ledger `proposed_action=ESCALATE_HUMAN`)

- **5 category-word `Programm` nodes** + the **20 edges** pointing to them.
- **17 placeholder `Materialdepot` nodes** ("unknown/aggregated donor sources").
- **Generic/unidentifiable Software stubs:** `software_bim`, `software_llmnt`, `software_recrete_finite_element_model`, `tool_bauteilkatalog`, `tool_material_passports_maconda`, `tool_rcmi`.
- **`prog_recreate_local`** (sub-pilot label; merge into `prog_recreate`).
- **`prog_re_use_hoefe`** — graph already flags *"dossier explicitly says Vienna location is unverified"*.
- **`software_opalis BETRIEBEN_VON opalis`** — verify redundancy of actor `opalis` vs `Rotor`.

## 7. Anomalies / notes for the Aggregator

- **Could not fetch this pass (UNVERIFIABLE, source present):** `software_ecotool` (`concular.de/ecotool`), `prog_reallabor_be_ware` (`zrs.berlin`, 2× timeout), `prog_rebridge` (`ec.europa.eu` RFCS). Re-fetch recommended; all three are plausibly real.
- **`bauteilkatalog_immobilien_basel_stadt BETRIEBEN_VON immobilien_basel_stadt`** (A10-R-094) — name-internal consistency only (edge `confidence` 0.9); add `immobilien.bs.ch` source.
- **No graph writes were made.** All findings are proposals; mutations must go through `apply_neo4j_review_patch.py` (dry-run → human `--confirm`).

## Summary

Of 175 claims (74 nodes, 101 rels): **22 PROVEN, 15 PARTIAL, 2 UNSUPPORTED, 4 UNVERIFIABLE, 101 MISSING_EVIDENCE, 31 SCHEMA_VIOLATION.** The single most important finding is twofold: (a) **all 22 `Materialdepot` nodes are unsourced and 17 are explicit "unknown/aggregated donor" placeholders** requiring deprecation, and (b) **the `Qflow` software/tool nodes are mis-sourced to an unrelated events company (`qflow.io`)** when the real entity is Qualis Flow (`qualisflow.com`). Secondary structural rot: five `Programm` nodes are German category words (Pilotprojekt/Wettbewerb/…) with 20 edges into them, and several "Software" nodes are duplicates or generic concepts that self-wire via `NUTZT_SOFTWARE`. Operator (`BETRIEBEN_VON`) facts are largely solid (7/9 confirmed), with the one caveat that Opalis's true operator is Rotor+Bellastock, not the redundant `opalis` actor node.
