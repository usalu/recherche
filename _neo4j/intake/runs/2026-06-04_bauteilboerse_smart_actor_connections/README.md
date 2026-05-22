# Bauteilboerse smart actor connections

**Date:** 2026-06-04  
**Target database:** `mit-bestand`  
**Run:** `bauteilboerse_smart_actor_connections_2026_06_04`

## Purpose

Add high-confidence actor-to-Bauteilboerse connections that are directly supported by first-party evidence. This run avoids name-similarity merges and uses only existing relationship types:

- `VERBUNDEN_MIT_AKTEUR`
- `BETRIEBEN_VON`
- `BELEGT_IN`
- standard actor classification edges for newly created actors

## Imported connections

| Bauteilboerse | Connection | Actor | Evidence |
|---|---|---|---|
| `baumab_kassel` | `VERBUNDEN_MIT_AKTEUR` | `stadt_kassel` | BauMaB concept/imprint: initiated in Stadt Kassel climate strategy and funded by Stadt Kassel |
| `baumab_kassel` | `VERBUNDEN_MIT_AKTEUR` | `surap_gmbh` | BauMaB homepage: environmental footprint/resource analysis with partner SURAP |
| `zirkulie_bauteilboerse_triesen` | `BETRIEBEN_VON` | `stiftung_lebenswertes_liechtenstein` | ZirkuLIE imprint names Stiftung Lebenswertes Liechtenstein |
| `zirkulie_bauteilboerse_triesen` | `VERBUNDEN_MIT_AKTEUR` | `re_win` | ZirkuLIE donation page names cooperation with Verein Re-Win |

## New actors

Created and minimally classified:

- `stadt_kassel`
- `surap_gmbh`
- `stiftung_lebenswertes_liechtenstein`

Reused existing:

- `re_win`

## Run

```powershell
python _neo4j/intake/runs/2026-06-04_bauteilboerse_smart_actor_connections/_run_import_smart_actor_connections.py
```

## Rollback

```cypher
MATCH ()-[r {review_run:'bauteilboerse_smart_actor_connections_2026_06_04'}]->()
DELETE r;

MATCH (a:Akteur)
WHERE a.id IN ['stadt_kassel', 'surap_gmbh', 'stiftung_lebenswertes_liechtenstein']
AND NOT ()--(a)
DELETE a;
```
