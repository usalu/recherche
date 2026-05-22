# IER-B1 Report — Geo placeholder BETEILIGT_AN

**Agent:** IER-B1  
**Generated:** 2026-06-06 21:19 UTC  
**Mode:** READ-ONLY (no graph mutations)

## Scope

- Element-ledger shard: **197** rows (`PARTIAL` `BETEILIGT_AN` → `:Projekt`, `basis_ref=akteur_typ_projekt_geo.json`)
- Plan document cites **223**; live element ledger enumerates **197** (remaining **26** are tier-D inferred `BETEILIGT_AN` → `Bauteilgruppe`, excluded per disjointness rules).
- Unique URLs fetched (cache): **107**

## Verdict summary

| Verdict | Count |
|---|---:|
| UNSUPPORTED | 97 |
| PARTIAL | 86 |
| PROVEN | 14 |

- URLs resolved on ledger rows: **197/197**
- Rows with `fetched=true`: **197**

## Proposed actions

| Action | Count |
|---|---:|
| DELETE | 97 |
| RESOURCE | 86 |
| KEEP | 14 |

## Method

1. Loaded scope from `VERIFICATION_LEDGER_ELEMENT.csv` (placeholder geo tokens).
2. Resolved HTTP URLs from `projekte_addresses.json` / `evidence_deep_dive.json`, inbox dossiers (`intake/inbox`, `processed`, `_archive`), and live `:Projekt` `source_urls`.
3. Rejected pipeline tokens (`processed`, `archive`, `Council of the EU`, …) as final `basis_ref`.
4. `WebFetch` each candidate URL; extracted verbatim `proof_quote` (≤300 chars).
5. `PROVEN` only when quote names **both** actor and project on fetched page.

## PROVEN samples

- `abn_amro` → `p_circl_abn_amro`: [https://www.degebouwengids.nl/en/circl-circular-and-sustainable/](https://www.degebouwengids.nl/en/circl-circular-and-sustainable/)
  > The furniture in Circl was previously used, and restored, by ABN AMRO.
- `drz_demontage_recycling` → `p_meduni_campus_mariannengasse`: [https://www.baukarussell.at/2020/09/03/vom-luster-bis-zum-kupferkabel/](https://www.baukarussell.at/2020/09/03/vom-luster-bis-zum-kupferkabel/)
  > Markus Meissner, Ressourcenmanager und Leiter von BauKarussell: „Der sozialen Kernaufgabe von BauKarussell konnten wir am MedUni Campus Mariannengasse intensiv nachkommen: Innerhalb der zehn Monate fa
- `ucl_circular_economy_lab` → `p_cascadeup_london_secondary_timber_glulam_demonstrator`: [https://www.ucl.ac.uk/circular-economy-lab/research/reusing-wood-demolition-mass-timber-products](https://www.ucl.ac.uk/circular-economy-lab/research/reusing-wood-demolition-mass-timber-products)
  > The pilot, known as CascadeUp, brings our bio-based, circular economy research to life.
- `biopartner_center_leiden` → `p_biopartner_5_leiden_oegstgeest`: [https://leidenbioscienceparkprojects.nl/en/sustainability/circulariteit](https://leidenbioscienceparkprojects.nl/en/sustainability/circulariteit)
  > Project page Gorlaeus high-rise Re-use of steel Around 150 tons of steel from the former Gorlaeus high-rise building have been re-used in the main supporting structure of BioPartner 5.
- `deerns` → `p_biopartner_5_leiden_oegstgeest`: [https://www.biopartnerleiden.nl/media_blog/opening_biopartner5/](https://www.biopartnerleiden.nl/media_blog/opening_biopartner5/)
  > Articles about BioPartner 5: Vakblad Deerns over BioPartner 5 (Dutch) Magazine Leven!

## Ten worst findings

1. **PARTIAL** `cbre` → `p_55_great_suffolk_street_london` — basis: `https://nla.london/projects/55-great-suffolk-street` — project on page, actor 'CBRE' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `gardiner_and_theobald` → `p_55_great_suffolk_street_london` — basis: `https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/` — project on page, actor 'Gardiner & Theobald' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `cantillon` → `p_55_great_suffolk_street_london` — basis: `https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/` — project on page, actor 'Cantillon' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `akt_ii` → `p_55_great_suffolk_street_london` — basis: `https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/` — project on page, actor 'AKT II' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `opera` → `p_55_great_suffolk_street_london` — basis: `https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/` — project on page, actor 'Opera' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `hawkins_brown` → `p_55_great_suffolk_street_london` — basis: `https://asbp.org.uk/case-studies/55-great-suffolk-street` — project on page, actor 'Hawkins\Brown' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `symmetrys` → `p_55_great_suffolk_street_london` — basis: `https://www.ribaj.com/intelligence/reusing-steel-fabrix-hawkins-brown-sheppard-robson-riba-exhibition/` — project on page, actor 'Symmetrys' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `popma_ter_steege_architecten` → `p_biopartner_5_leiden_oegstgeest` — basis: `https://leidenbioscienceparkprojects.nl/en/sustainability/circulariteit` — project on page, actor 'Popma ter Steege Architecten / PTSA' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `de_vries_en_verburg` → `p_biopartner_5_leiden_oegstgeest` — basis: `https://leidenbioscienceparkprojects.nl/en/sustainability/circulariteit` — project on page, actor 'De Vries en Verburg' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv
1. **PARTIAL** `vic_obdam_staalbouw` → `p_biopartner_5_leiden_oegstgeest` — basis: `https://leidenbioscienceparkprojects.nl/en/sustainability/circulariteit` — project on page, actor 'Vic Obdam Staalbouw' not named; source=dossier:_neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv

## Key finding

The dominant outcome is **UNSUPPORTED** (97/197). Placeholder `evidence_url` tokens on geo-imported `BETEILIGT_AN` edges stored pipeline metadata instead of HTTP URLs; project-level dossier URLs often confirm the **project** but not the specific **actor** participation link — those rows remain `PARTIAL` + `RESOURCE` until actor-named consortium pages are found.
