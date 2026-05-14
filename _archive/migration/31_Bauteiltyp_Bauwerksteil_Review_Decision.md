# Phase 31 Bauteiltyp Bauwerksteil Review Decision

## Decision

Keep bauteiltyp/Bauwerksteil out of the clean database.

Reason: Bauwerksteil is usually object scale or system scale, not a reusable component family.

## Database Change

No database nodes or clean edges were added. The held edges need case-level decisions.

## Counts

- Held bauteiltyp/Bauwerksteil edges reviewed: 27

| decision | rows |
|---|---:|
| object_scale_not_component | 12 |
| case_context_required | 6 |
| keep_review_resolve_scale | 4 |
| candidate_structural_system | 4 |
| candidate_precise_component | 1 |

## Sample Rows

| raw label | existing clean edges | decision | suggested target |
|---|---|---|---|
| Garagentor | installed_in_bauobjekt->bauobjekt/ELYS_Kultur_Gewerbehaus_Basel; uses_material->material/Glas | candidate_precise_component | bauteiltyp/Tuer |
| Bestand-Betonstruktur | installed_in_bauobjekt->bauobjekt/Grande_Halle_de_Colombelles; uses_material->material/Beton; uses_material->material/Stahl | candidate_structural_system | tragwerkstyp/Ortbetontragwerk; tragwerksprinzip/Skeletttragwerk |
| bestehender Betonrahmen | installed_in_bauobjekt->bauobjekt/Holbein_Gardens_London; uses_material->material/Beton; uses_material->material/Stahl | candidate_structural_system | tragwerkstyp/Ortbetontragwerk; tragwerksprinzip/Skeletttragwerk |
| Retained 1990s concrete frame TBC | installed_in_bauobjekt->bauobjekt/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain; uses_material->material/Beton | candidate_structural_system | tragwerkstyp/Ortbetontragwerk; tragwerksprinzip/Skeletttragwerk |
| Rohbau | installed_in_bauobjekt->bauobjekt/Recyclinghaus_Hannover; uses_material->material/Holz | candidate_structural_system | tragwerkstyp/* |
| Holz-/Strohbau | installed_in_bauobjekt->bauobjekt/Ferme_du_Rail_Paris; uses_material->material/Holz; uses_material->material/Stroh | case_context_required | bauweise/*; material/Holz; material/Stroh |
| Holzgalerie | installed_in_bauobjekt->bauobjekt/Impact_Hub_Berlin_CRCLR_Fitout; uses_material->material/Holz | case_context_required | bauobjekt/* or precise bauteiltyp/* |
| Holzgalerie / Innenausbau | has_bauteiltyp->bauteiltyp/Innenausbau; installed_in_bauobjekt->bauobjekt/CRCLR_House_Impact_Hub_Berlin; uses_material->material/Holz | case_context_required | bauobjekt/* or precise bauteiltyp/* |
| innere Box | installed_in_bauobjekt->bauobjekt/Maison_DnA_Asse; uses_material->material/Holz | case_context_required | bauobjekt/* or precise bauteiltyp/* |
| Ramp / pier components | installed_in_bauobjekt->bauobjekt/Big_Dig_House_Lexington_Massachusetts; uses_material->material/Beton; uses_material->material/Stahl | case_context_required | bauobjekt/* or precise bauteiltyp/* |
| Wohnungsteile / Betonunits | has_bauteiltyp->bauteiltyp/Betonfertigteil; installed_in_bauobjekt->bauobjekt/Superlocal_Expogebouw_Bleijerheide; uses_material->material/Beton; uses_material->material/Stahl | case_context_required | bauobjekt/* or precise bauteiltyp/* |
| Betriebsgebäude | installed_in_bauobjekt->bauobjekt/Juch_Areal_Recyclingzentrum_Zuerich | keep_review_resolve_scale |  |

## Output

- _migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv
