# Relationship-coverage probes (live, read-only) — 2026-06-01

Confirms whether node properties flagged as topology/provenance duplicates are
genuinely redundant with existing edges before any removal.

## Topology-duplicate candidates

| Node prop | total | has prop | has edge | prop matches an edge | notes | verdict |
|---|---:|---:|---:|---:|---|---|
| `Bauteilgruppe.primary_bauteiltyp_id` -> `HAT_BAUTEILTYP` | 356 | 356 | 356 | 166 | 192 are `bt_mehrere` (summary); 0 nodes lack the edge | move_to_relationship (full edge coverage) |
| `Bauteilgruppe.primary_material_id` -> `NUTZT_MATERIAL` | 356 | 356 | 321 | 236 | 101 are `mat_mehrere`; **35 have prop but NO edge** | migrate_edge_then_drop |
| `Bauteilgruppe.reuse_status` vs `HAT_STATUS` | 356 | 356 | 356 | n/a | values reuse/retained/planned/dismantled are a DIFFERENT axis than Status nodes (status_realisiert/geplant/verworfen/rueckgebaut) | KEEP as domain (not a duplicate) |
| `Akteur.land` -> `LIEGT_IN_LAND` | 669 | 81 | 220 | 2 | **79 of 81 have prop but no edge** | migrate_edge_then_drop |

## Provenance edge coverage (BELEGT_IN)

| Label | total | has BELEGT_IN | has source-url prop | verdict for source_* props |
|---|---:|---:|---:|---|
| Bauteilgruppe | 356 | 356 | 0 | drop source_* (provenance fully on edges) |
| Bauwerk | 184 | 184 | 0 | drop source_* |
| Projekt | 86 | 83 | 34 | drop source_* (near-full edge coverage) |
| Akteur | 669 | 532 | 134 | drop source_* (mostly on edges; review the 137 w/o BELEGT_IN) |
| Norm | 103 | 3 | 0 | provenance via evidence_* only; migrate before dropping evidence_* |
| Kennwert | 255 | 0 | 52 | **no BELEGT_IN at all**; `source_id` (214) + source_urls hold the only provenance -> migrate to BELEGT_IN before dropping |

## Consequences for the matrix
- `primary_bauteiltyp_id`: drop after confirming `HAT_BAUTEILTYP` (already 100%).
- `primary_material_id`, `Akteur.land`: create the missing edges first, then drop.
- `reuse_status`: keep (genuine reuse-lifecycle field).
- Source/provenance props on Bauteilgruppe/Bauwerk/Projekt/Akteur: safe to drop.
- Kennwert + Norm provenance: must be migrated to `BELEGT_IN`/edges before removal, else provenance is lost.
