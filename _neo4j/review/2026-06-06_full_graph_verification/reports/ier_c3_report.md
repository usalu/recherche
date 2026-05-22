# IER-C3 Report — VMA missing evidence

**Agent:** IER-C3 · **Date:** 2026-06-06 · **Database:** `mit-bestand`

## Scope

- Live `VERBUNDEN_MIT_AKTEUR` with `evidence_url IS NULL`: **182**
- Excluded tier-A/D overlap (PARTIAL, tier-A ME, F09-synth logic): **18**
- **Shard processed:** **164**

## Verdict summary

| Verdict | Count |
|---|---:|
| PROVEN | 104 |
| UNSUPPORTED | 47 |
| MISSING_EVIDENCE | 13 |

## Proposed actions

| Action | Count |
|---|---:|
| ADD_SOURCE | 104 |
| DELETE | 60 |

**PROVEN upgrades:** 104 · **DELETE proposals:** 60

## Method

WebSearch (DuckDuckGo HTML) → WebFetch candidate URLs from endpoint `source_urls`, curated hints, and search results. **Strict two-endpoint gate:** quote must name both actors. Unsupported after fetch → `DELETE`.

## Top PROVEN recoveries (sample)

- `anders_lendager` → `Lendager`: Resource Rows - Lendager /********* Compiled CSS - Do not edit *********/ :root{--button_padding:11px 23px;}.has-awb-col… ([https://lendager.com/project/resource-rows](https://lendager.com/project/resource-rows))
- `anja_rosen` → `urban_mining_index`: Impressum | Urban Mining Index Home Das ist der Urban Mining Index Systematik Qualitätsstufen Bewertungsebenen Aktuelles… ([https://urban-mining-index.de/impressum](https://urban-mining-index.de/impressum))
- `anna_buser` → `re_win`: Genau an dieser Stelle im Sommer 2022 ist eine Idee entstanden, die das Klima schont und gleichzeitig Nothilfe leistet: … ([https://re-win.ch/verein/ueber](https://re-win.ch/verein/ueber))
- `barbara_buser` → `baubuero_in_situ`: Genau an dieser Stelle im Sommer 2022 ist eine Idee entstanden, die das Klima schont und gleichzeitig Nothilfe leistet: … ([https://re-win.ch/verein/ueber](https://re-win.ch/verein/ueber))
- `barbara_buser` → `zirkular`: Über uns | RE-WIN Home Events Fenster für die Ukraine Übersicht Projektstatus Unterstützer:innen Fenster spenden News Ve… ([https://re-win.ch/verein/ueber](https://re-win.ch/verein/ueber))
- `baubuero_in_situ` → `zirkular`: Zirkular Projects Building K.118 Completed simultaneously by baubüro in situ in 2021, the projects K.118 in Winterthur a… ([https://zirkular.net/en/project/building-k-118/](https://zirkular.net/en/project/building-k-118/))
- `baukarussell` → `markus_meissner`: Impressum - BauKarussell Zum Inhalt springen Angebot Zirkulärer Rückbau BauK-Akademie Forschung & Entwicklung Re-Use Bau… ([https://www.baukarussell.at/impressum](https://www.baukarussell.at/impressum))
- `baukarussell` → `matthias_neitsch`: Impressum - BauKarussell Zum Inhalt springen Angebot Zirkulärer Rückbau BauK-Akademie Forschung & Entwicklung Re-Use Bau… ([https://www.baukarussell.at/impressum](https://www.baukarussell.at/impressum))
- `baukarussell` → `re_use_austria`: Projekte - BauKarussell Zum Inhalt springen Angebot Zirkulärer Rückbau BauK-Akademie Forschung & Entwicklung Re-Use Baut… ([https://www.baukarussell.at/projekte](https://www.baukarussell.at/projekte))
- `baukarussell` → `romm_zt`: Impressum - BauKarussell Zum Inhalt springen Angebot Zirkulärer Rückbau BauK-Akademie Forschung & Entwicklung Re-Use Bau… ([https://www.baukarussell.at/impressum](https://www.baukarussell.at/impressum))

## Worst unsupported (DELETE sample)

- `2hs` → `dirk_e_hebel` (UNSUPPORTED): prior=A06B-rel-0001; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `3xn` → `gxn` (UNSUPPORTED): prior=A06B-rel-0003; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `3xn` → `vandkunsten` (UNSUPPORTED): prior=A06B-rel-0004; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `Werner_Sobek` → `vanessa_propach` (UNSUPPORTED): prior=A06B-rel-0006; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `akt_ii` → `symmetrys` (UNSUPPORTED): prior=A06B-rel-0007; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `andreas_sonderegger` → `zhaw` (UNSUPPORTED): prior=A06B-rel-0011; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `annabelle_von_reutern` → `tomas` (UNSUPPORTED): prior=A06B-rel-0016; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `baukarussell` → `oekologie_institut` (UNSUPPORTED): prior=A06B-rel-0020; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `baumab_kassel` → `surap_gmbh` (UNSUPPORTED): prior=A06B-rel-0025; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed
- `bellastock` → `hugo_topalov` (UNSUPPORTED): prior=A06B-rel-0027; prior_verdict=MISSING_EVIDENCE; connection_kind=null; fetched but strict two-endpoint gate failed

## Headline

Of **164** unsourced VMA edges, **104** upgraded to PROVEN via internet evidence; **60** proposed for deletion as unsupported after strict two-endpoint gate.
