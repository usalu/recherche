# Bauteile IBS graph addition

**Date:** 2026-06-04  
**Target database:** `mit-bestand`  
**Anchor:** `bauteilkatalog_immobilien_basel_stadt`  
**Display name:** Bauteilkatalog Immobilien Basel-Stadt

## Decision

Add `https://bauteile-ibs.ch/` as a schema-compatible Bauteilboerse-style `:Akteur`.

The site is not a public third-party marketplace. It is a restricted project/harvest catalogue:

- the catalogue is titled "Immobilien Basel-Stadt Bauteilkatalog zur Wiederverwendung";
- it exposes categories, component listings, component detail pages, downloads, CO2 values, and a cart action;
- the project page says the offer is only available to cantonal projects / competition participants, not to third parties;
- Zirkular states that it catalogued Re-Use components for Immobilien Basel-Stadt and that the components come from current Basel-Stadt deconstruction objects.

Because the live graph has no dedicated "Project/Harvest Catalogue" vocabulary node, the closest existing graph model is:

- `Akteurtyp`: `at_materialhub_bauteilboerse`
- `Land`: `land_schweiz`
- `Marktmodell`: `mm_kauf_gebraucht`
- `Geschaeftsmodell`: `gm_dienstleistung_urban_mining`

## Evidence sources

First-party / operator evidence:

- `https://bauteile-ibs.ch/`
- `https://bauteile-ibs.ch/info`
- `https://bauteile-ibs.ch/components`
- `https://bauteile-ibs.ch/componentsmine`
- `https://bauteile-ibs.ch/contact`

Project/operator provenance:

- `https://zirkular.net/de/projekt/bauteilkatalog-immobilien-basel-stadt`

Representative component evidence:

- `https://bauteile-ibs.ch/components/163-msh0012-passerelle-fenster`
- `https://bauteile-ibs.ch/components/114-msh002-stahltragwerk`
- `https://bauteile-ibs.ch/components/193-msh005-holzbalkendecke-halle`
- `https://bauteile-ibs.ch/components/144-msh030-waermedaemmung`
- `https://bauteile-ibs.ch/components/203-ran-gr10-sandwichpaneele`
- `https://bauteile-ibs.ch/components/180-kly-gr08-alu-fassadenplatten`

## Reused graph nodes

- `immobilien_basel_stadt`
- `zirkular`
- `digvis_gmbh`
- `bauteilboerse_basel_overall`
- `tool_bauteilkatalog`
- `p_elementa_walkeweg`

## Strict material and component edges

Only closed-set IDs already present in the live graph are used.

Materials:

- `mat_stahl`
- `mat_holz`
- `mat_daemmstoff`
- `mat_aluminium`
- `mat_glas`

Bauteiltypen:

- `bt_fenster`
- `bt_traeger`
- `bt_decke`
- `bt_daemmung`
- `bt_fassade`
- `bt_treppe`
- `bt_gelaender`
- `bt_technik`
- `bt_stuetze`

## Baseline note

`python _scripts/_gap_survey.py` was run before this import. The current graph did **not** return all-zero mandatory checks; existing failures included `r.id NULL`, case-specific `BELEGT_IN`, and Bauteilgruppe coverage gaps. These are baseline conditions, not introduced by this addition.

## Run

```powershell
python _neo4j/intake/runs/2026-06-04_bauteile_ibs_graph_addition/_run_import_bauteile_ibs.py
```

Connection defaults:

- URI: `neo4j://127.0.0.1:7687`
- database: `mit-bestand`
- password: `NEO4J_PASSWORD` or `.neo4j_password`

## Rollback

```cypher
MATCH ()-[r {review_run:'bauteile_ibs_graph_addition_2026_06_04'}]->()
DELETE r;

MATCH (a:Akteur {id:'bauteilkatalog_immobilien_basel_stadt'})
DETACH DELETE a;

MATCH (q:Quelle)
WHERE q.id IN [
  'q_url_670d60d96b673e1ec02d090291b7e2f7',
  'q_url_e3efdbf29c121c4a4b16d0dc7c8f6545',
  'q_url_474582b3b551d45e9bf5b728ae2fcfee',
  'q_url_4221cdd696149a2560934c80f30e534e',
  'q_url_c5d71f9b73b8f79a37f775a52d33cfab',
  'q_url_8446c5c4c7444039df21ff57c63d4ae4',
  'q_url_e379d26c92c90f88082991724eebcd1e',
  'q_url_720d94c7a5ac93ee5e12fb8f58db6961',
  'q_url_90474e5f5fe205b131a9a2dc729180ca',
  'q_url_5cd0914342420dc6cb456bfd79ce6bb2',
  'q_url_69688fccf32bbc9dc389e8bee5eeb1f4'
]
AND NOT ()--(q)
DELETE q;
```
