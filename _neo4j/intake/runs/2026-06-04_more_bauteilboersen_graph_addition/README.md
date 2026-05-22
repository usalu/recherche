# More Bauteilboersen graph addition

**Date:** 2026-06-04  
**Target database:** `mit-bestand`  
**Run:** `more_bauteilboersen_graph_addition_2026_06_04`

## Imported candidates

Two first-party, active, concrete offer interfaces were added:

| Anchor | Name | Country | Decision |
|---|---|---|---|
| `baumab_kassel` | BauMaB Kassel / Bauteilbörse Kassel | Deutschland | import as Bauteilboerse-style Akteur |
| `zirkulie_bauteilboerse_triesen` | ZirkuLIE Bauteilbörse Triesen | Liechtenstein | import as Bauteilboerse-style Akteur |

## Evidence basis

### BauMaB Kassel

First-party pages show:

- buy/sell platform for used building materials and components;
- physical sales/storage location in Kassel;
- online offer list with filters, prices, availability, dimensions, condition, hazard suspicion, BIM, and pickup/no-shipping signal;
- seller workflow for pre-demolition capture, reservation, deconstruction-window coordination, and direct purchase/reservation;
- project/concept page naming a digital platform plus physical retail place for recording, evaluating, mediating, and temporarily storing materials/components.

### ZirkuLIE

First-party pages show:

- Bauteilboerse for Liechtenstein and Eastern Switzerland;
- webshop with categories, filters, prices, cart actions, material filters, and Triesen location;
- component categories including windows, doors, insulation, roof, facade, building services, sanitary, flooring, stairs and hardware;
- donation workflow for used components and reuse/circular-building centre context.

## Schema note

`land_liechtenstein` did not exist before this run. It was added as:

```cypher
(:Land {id:'land_liechtenstein', name:'Liechtenstein'})
```

This follows the existing `Land` label and `land_*` id pattern. No new `Akteurtyp`, `Akteurrolle`, `Marktmodell`, `Geschaeftsmodell`, `Methode`, `Material`, or `Bauteiltyp` vocabulary nodes were created.

## Run

```powershell
python _neo4j/intake/runs/2026-06-04_more_bauteilboersen_graph_addition/_run_import_more_bauteilboersen.py
```

## Rollback

```cypher
MATCH ()-[r {review_run:'more_bauteilboersen_graph_addition_2026_06_04'}]->()
DELETE r;

MATCH (a:Akteur)
WHERE a.id IN ['baumab_kassel', 'zirkulie_bauteilboerse_triesen']
DETACH DELETE a;

MATCH (l:Land {id:'land_liechtenstein'})
WHERE NOT ()--(l)
DELETE l;
```
