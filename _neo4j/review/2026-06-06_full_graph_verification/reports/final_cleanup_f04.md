# Final Cleanup F04 — P6-04 Scope B Actor Re-proof

**Agent:** F04 (read-only Neo4j + WebFetch)  
**Date:** 2026-06-06  
**Scope:** 18 `Akteur` nodes flagged `UNVERIFIABLE` in P6-04 Scope B (`post_quality_p06_04.csv`)  
**Cross-walk:** `ledger/post_quality_p06_04.csv` (`P604-A06B-node-*`, scope `B`)  
**Ledger:** `ledger/final_cleanup_f04.csv` (**18 rows**)

---

## Scope recap

Re-adjudicated the F3 actor-node list from `VERIFICATION_PLAN_7_AGENTS_FINAL_CLEANUP.md` §Agent F3 (SCOPE_CYPHER nodes block). Each row re-fetched graph `source_urls` (and alternates only when graph URLs failed or omitted the actor name). Evidence Gate: `PROVEN` / `PARTIAL` require non-empty verbatim `proof_quote`; external claims require `fetched=true`.

Live Neo4j (`mit-bestand`): all 18 nodes present as `:Akteur` with expected `elementId` values.

---

## Verdict histogram

| Verdict | Count | Δ vs P6-04 (all 18 were UNVERIFIABLE) |
|---|---:|---|
| **PROVEN** | 12 | +12 |
| **PARTIAL** | 2 | +2 |
| **UNVERIFIABLE** | 4 | −14 |
| **Σ** | **18** | |

**Upgrade rate:** 14/18 (77.8%) upgraded from P6-04 `UNVERIFIABLE`.

---

## Upgrades (PROVEN)

| Actor | basis_ref | proof anchor |
|---|---|---|
| andreas_sonderegger | zirkular.net (zhaw graph URL 404) | ZHAW IKE team listing |
| eva_stricker | zirkular.net | project management credit |
| guido_brandi | zirkular.net | IKE team listing |
| barrault_pressacco | barraultpressacco.com/about | practice founded 2009 |
| catherine_de_wolf | ethz.ch news | Professor Catherine De Wolf |
| christian_schoeningh | nbau.org CRCLR article | byline + project team |
| fabian_sauser | swiss-architects.com | Projektleiter: Fabian Sauser |
| fabio_gramazio | gramaziokohler.arch.ethz.ch | Vortragende: Fabio Gramazio |
| frederic_denise | bellastock.com/projets/resilience | Frédéric Denise — Archipel Zéro |
| georg_hubmann | circularmaterialsystems.com/en/about | research lead credit |
| hugo_topalov | Interreg NWE FCRBE page | Hugo Topalov from Bellastock |
| julia_turpin | grandhuit.eu/notre-equipe | coopératrice associée |

---

## PARTIAL (quote present, first-party gap)

| Actor | Issue | proposed_action |
|---|---|---|
| annette_hillebrandt | Graph `architektur.uni-wuppertal.de/.../annette-hillebrandt` returned **503**; Wikipedia bio used | KEEP; re-fetch Wuppertal people page |
| hans_hammink | Graph `architectencie.nl` timed out; CMS case pages omit name; dutchararchitects.org names project architect | KEEP; ADD_SOURCE architectencie.nl when live |

---

## Residual UNVERIFIABLE (strict gate)

| Actor | Blocker |
|---|---|
| **anja_rosen** | `urban-mining-index.de` (sole graph URL) describes the UMI tool but does not name Anja Rosen |
| **annabelle_von_reutern** | `concular.de` fetched; `tomas-architecture.com` timeout — neither graph URL names actor |
| **gxn** | Sole graph source is CircleHouse PDF — fetch timeout; no readable verbatim quote |
| **jan_haerens** | `rotordb.org` Zinneke page credits Renaud Haerlingen; graph `vai.be` / `ouest.be` omit Jan Haerens |

All four: **KEEP** (sources present or plausible; human spot-fetch / ADD_SOURCE recommended).

---

## Worst findings (attestation gaps)

1. **ZHAW cluster (3 upgraded via Zirkular):** Graph still points at dead zhaw.ch research URL (404). Recommend `ADD_SOURCE` → `zirkular.net` IKE publication page for andreas_sonderegger, eva_stricker, guido_brandi.
2. **anja_rosen:** Urban Mining Index site is first-party for the *tool*, not the *person* — off-graph bibliographic sources (VDI/IRB, Manual of Recycling) name Rosen but are not on `source_urls`; do not infer PROVEN without graph URL update.
3. **jan_haerens:** Strong off-graph attestation exists (Brussels Architecture Prize, ouest.be lectures) but none are on graph `source_urls`; rotordb credit mismatch (Haerlingen vs Haerens) blocks strict upgrade.
4. **gxn:** PDF evidence on graph unreadable in this run; 3XN/GXN ecosystem pages attest entity but are not listed on node `source_urls`.

---

## P6-04 cross-walk

Every row carries `prior_claim_id=P604-A06B-node-*` matching `post_quality_p06_04.csv` Scope B actor entries. No graph mutations performed.

---

## Summary

F04 re-proof upgraded **12 actors to PROVEN** and **2 to PARTIAL** under the strict Evidence Gate, leaving **4 UNVERIFIABLE** with justified KEEP. Primary blockers: dead or non-attesting graph URLs (zhaw 404, UMI homepage without author string, unreadable GXN PDF, rotordb name mismatch for Jan Haerens). Outputs ready for F4 ledger merge override priority #1 (when full F3 ledger is complete).
