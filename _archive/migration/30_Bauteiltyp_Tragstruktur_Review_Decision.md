# Phase 30 Bauteiltyp Tragstruktur Review Decision

## Decision

Keep bauteiltyp/Tragstruktur out of the clean database.

Reason: Tragstruktur is not a true component type. Each case should become a structural type, structural principle, material-specific structure, or concrete component.

## Database Change

No database nodes or clean edges were added. Some rows reveal possible future ontology knots, especially tragwerkstyp/Stahltragwerk.

## Counts

- Held bauteiltyp/Tragstruktur edges reviewed: 28

| decision | rows |
|---|---:|
| keep_review_derive_structure | 12 |
| candidate_new_or_existing_tragwerk | 8 |
| candidate_existing_tragwerkstyp | 4 |
| covered_by_existing_tragwerkstyp | 3 |
| covered_or_candidate_components | 1 |

## Sample Rows

| raw label | existing clean edges | decision | suggested target |
|---|---|---|---|
| Betonhallen / Tragstruktur | uses_material->material/Beton | candidate_existing_tragwerkstyp | tragwerkstyp/Ortbetontragwerk |
| Concrete slab on metal deck / composite framing | has_bauteiltyp->bauteiltyp/Platte_Paneel; uses_material->material/Beton; uses_material->material/Stahl | candidate_existing_tragwerkstyp | tragwerkstyp/Ortbetontragwerk |
| Holzstruktur | uses_material->material/Holz | candidate_existing_tragwerkstyp | tragwerkstyp/Holztragwerk |
| Holzstruktur | uses_material->material/Holz | candidate_existing_tragwerkstyp | tragwerkstyp/Holztragwerk |
| Aussteifung |  | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Aussteifung / bracing members | uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Neue/recycled-content Stahlbauteile | has_bauteiltyp->bauteiltyp/Leuchte; uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Primärtragwerk / Aussteifung |  | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Stahlbauteile Laubengänge | uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Stahlkonstruktion Beschattung | has_bauteiltyp->bauteiltyp/Beschattung_Sonnenschutz; uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Stahlstruktur der Traghalle Hagenholz | uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |
| Stahltragwerk | uses_material->material/Stahl | candidate_new_or_existing_tragwerk | tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk |

## Output

- _migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv
