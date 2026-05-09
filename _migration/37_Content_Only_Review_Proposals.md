# Phase 37 Content-Only Review Proposals

## Scope

Proposal-only pass for the 11 manual-review nodes with no held clean-edge rows. No manual decisions were written.

## Output

- _migration/37_content_only_review_proposals.csv

## By Proposal Class

| class | nodes |
|---|---:|
| component_subtype | 1 |
| connection_overview | 4 |
| document_model_tool_mixed | 1 |
| model_document_tool_mixed | 1 |
| strategy_status_overlap | 1 |
| system_vs_component | 1 |
| valid_system_mixed_content | 1 |
| wrong_entity_component_material | 1 |

## Node Proposals

| node | recommended handling | possible final targets |
|---|---|---|
| bauteiltyp/Holzrahmenelement | defer_until_source_context | bausystem/Holzrahmenbau or bauteiltyp/Wand or bauteiltyp/Platte_Paneel |
| bauteiltyp/Treppenwange | merge_or_exact_component_after_context | bauteiltyp/Treppe or bauteiltyp/Traeger |
| datenmodell/Gebaeuderessourcenpass | clean_and_split_later | datenmodell/Gebaeuderessourcenpass_Schema; software_digitaltool/Concular; akteur/Concular |
| dokumenttyp/Gebaeuderessourcenpass | clean_and_split_later | dokumenttyp/Gebaeuderessourcenpass; datenmodell/Gebaeuderessourcenpass_Schema; software_digitaltool/Madaster |
| fuegung_verbindung/Beton_Fertigteile_Verbindungen | do_not_import_as_atomic_connection | methode/Verbindungen_im_Betonfertigteilbau or atomic fuegung_verbindung/* |
| fuegung_verbindung/Composite_Verbindungen | do_not_import_as_atomic_connection | methode/Verbindungen_im_Verbundbau or atomic fuegung_verbindung/* |
| fuegung_verbindung/Holz_Verbindungen | do_not_import_as_atomic_connection | methode/Verbindungen_im_Holzbau or atomic fuegung_verbindung/* |
| fuegung_verbindung/Stahl_Verbindungen | do_not_import_as_atomic_connection | methode/Verbindungen_im_Stahlbau or atomic fuegung_verbindung/* |
| fuegung_verbindung/Stahlseil | defer_until_component_knot_decision | bauteiltyp/Zugglied_Seil or material/Stahl |
| reuse_strategie/Temporaerer_Wiedereinbau | defer_until_strategy_status_rule | reuse_einsatzstatus/Temporaer plus reuse_strategie/Direkte_Wiederverwendung if applicable |
| zertifizierung_bewertungssystem/DGNB | clean_content_then_possible_import | zertifizierung_bewertungssystem/DGNB |

## Rule

These rows should stay out of _database until the final manual decision pass.
