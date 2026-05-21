# Repair Report: Phase 1.5 / 1.6 Residuals

Timestamp: 2026-05-21T07:18:05.005145+00:00
Database: `mit-bestand`
Status: PASS

## Before

- Akteur count: 650
- Node count: 3804
- Relationship count: 25047
- Case-insensitive actor duplicate ordered pairs: 2
- Residual target ids: [{'id': 'Bellastock', 'labels': ['Akteur'], 'degree': 18}, {'id': 'bauburo_in_situ', 'labels': ['Akteur'], 'degree': 8}, {'id': 'norm_din_18940', 'labels': ['Norm'], 'degree': 1}]

## Actions

- merged bauburo_in_situ into baubuero_in_situ: {'id': 'baubuero_in_situ', 'aliases': ['bauburo_in_situ', 'baubüro in situ'], 'degree': 24}
- merged Bellastock into bellastock: {'id': 'bellastock', 'aliases': ['Bellastock'], 'degree': 27}
- remapped norm_din_18940 into norm_din_18940_family: {'id': 'norm_din_18940_family', 'aliases': ['norm_din_18940', 'DIN 18940'], 'degree': 1}

## After

- Akteur count: 648
- Node count: 3802
- Relationship count: 25023
- Phase 1.5 norm targets remaining: []
- Phase 1.6 merge-in ids remaining: []
- Case-insensitive actor duplicate ordered pairs: 0
- Canonical actor degrees: [{'id': 'baubuero_in_situ', 'labels': ['Akteur'], 'degree': 24}, {'id': 'bellastock', 'labels': ['Akteur'], 'degree': 27}]
- Norm remap target: [{'id': 'norm_din_18940_family', 'labels': ['Norm'], 'degree': 1}]

## Relationship Loss

Semantic relationship coverage passed: all 27 relationships journalled from the three residual nodes have an equivalent relationship from/to the canonical replacement after repair. The physical relationship count dropped by 24 because `apoc.refactor.mergeNodes(..., mergeRels: true)` collapsed duplicate parallel relationships while moving them to canonical nodes. No residual-node relationship endpoint was left uncovered; `norm_din_18940` was remapped into `norm_din_18940_family`, preserving the incoming `REFERENZIERT_NORM` edge from `rr_de_lehm`.

## Audit

- JSONL audit: `deleted\repair_phase1_5_1_6_residuals.jsonl`
- Migration: `migrations/mig_repair_1_5_1_6_residuals.cypher`
