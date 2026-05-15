# Validation report — batch_012

## Counts

- `p_recypark_demets_anderlecht.kg.jsonl`: 15 nodes, 97 relationships
- `p_resilience_la_ferme_des_possibles_stains.kg.jsonl`: 34 nodes, 220 relationships
- `p_resource_rows_copenhagen.kg.jsonl`: 9 nodes, 63 relationships
- `p_roots_in_the_sky_blackfriars_crown_court.kg.jsonl`: 21 nodes, 132 relationships
- `p_saxum_vineyard_equipment_barn_paso_robles.kg.jsonl`: 19 nodes, 118 relationships

## Contract checks

- Projekt-only center: PASS — no Fallbeispiel nodes emitted.
- Kennwerte as scalar properties: PASS — no Kennwert nodes emitted.
- Source-of-truth Quellen: PASS — each file has one Quelle node and BELEGT_IN relations with `datenqualitaet=Belegt`.
- Controlled-node approach: PASS — Stadt, Land, Bauwerk roles/classes, Akteurrollen/-typen, Bauteiltypen, Materialgruppen, Hürden and process concepts are relationship targets.
- Roots status: PASS — modeled as planned/failed appendix case with `status_geplant` + `status_verworfen`, not as built proof.
- Node degree target: PASS — every emitted non-seed node has at least two incident relationships inside its project file.

## Notes

- `controlled_terms.delta.jsonl` is intentionally empty in this batch; RT 2012, INIES and RISA-3D are emitted as source-specific nodes in the relevant project files, not as global controlled vocabulary terms.
- No loose furniture/decor-only elements were promoted to core Direct Reuse nodes.