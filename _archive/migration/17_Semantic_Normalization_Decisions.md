# Semantic Normalization Decisions

Status: approval map before final database import.  
No files have been moved or deleted.

Rule used here: final IDs must be typed path IDs like `entity/id`. Never import bare slugs.

## Core Decision Table

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/fallstudie/index` | `delete` | Generated from an `index.md` source by mistake; not a real case. | CONFIDENT |
| `_graph/reuse_kette/index` | `delete` | Generated from an `index.md` source by mistake; not a real reuse chain. | CONFIDENT |
| `_graph/reuse_kettenstation/index__Donor` | `delete` | Derived from fake `index` chain; not a real station. | CONFIDENT |
| `_graph/reuse_kettenstation/index__Receiver` | `delete` | Derived from fake `index` chain; not a real station. | CONFIDENT |
| `_graph/datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger` | `review -> rename or delete` | Same ID as a reuse item; a datenpunkt must be a value, not a component. | REVIEW_REQUIRED |
| `_graph/datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster` | `review -> rename or delete` | Same ID as a reuse item; a datenpunkt must be a value, not a component. | REVIEW_REQUIRED |

## Material / Component / Structure

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/material/Beton_Fertigteile` | `move -> _database/bauteiltyp/Betonfertigteil` | Betonfertigteile are component/product types, not material; material stays `Beton` or `Stahlbeton`. | CONFIDENT |
| `_graph/bauteiltyp/Ziegel` | `move -> _database/material/Ziegel` | Ziegel is primarily what something is made of; component cases use `bauteiltyp/Mauerstein_Block` plus raw label. | CONFIDENT |
| `_graph/bauteiltyp/Mauerstein_Block` | `keep -> _database/bauteiltyp/Mauerstein_Block` | Correct component family for brick/block units; material is linked separately. | CONFIDENT |
| `_graph/bauteiltyp/Betonblock` | `move -> _database/bauteiltyp/Mauerstein_Block` | A concrete block is a block component; keep `material/Beton` as separate fact. | CONFIDENT |
| `_graph/bauteiltyp/Dachtragwerk` | `move -> _database/tragwerkstyp/Dachtragwerk` | A roof structure is a structural type/system, not a simple component type. | CONFIDENT |
| `_graph/tragwerkstyp/Dachtragwerk` | `keep -> _database/tragwerkstyp/Dachtragwerk` | Correct strongest type. Merge bauteiltyp content here. | CONFIDENT |
| `_graph/bauteiltyp/Tragstruktur` | `keep as review fallback -> _database/bauteiltyp/Tragstruktur` | Use only when the source names a structural assembly without precise component or system. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Bauwerksteil` | `move/split -> _database/bauobjektklasse/Gebaeudeteil` | Whole building parts are object scale, not component type; create bauobjekt/beteiligung if concrete. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Brettschichtholzstuetze` | `move -> _database/bauteiltyp/Stuetze` | Component type is column; `Brettschichtholz` is material. | CONFIDENT |
| `_graph/bauteiltyp/Brettsperrholzdecke` | `move -> _database/bauteiltyp/Decke` | Component type is slab/floor/ceiling; `Brettsperrholz` is material. | CONFIDENT |
| `_graph/bauteiltyp/Fachwerktraeger` | `move -> _database/bauteiltyp/Traeger` | Component type is beam/girder; `Fachwerk` belongs to structural principle/raw label. | CONFIDENT |
| `_graph/bauteiltyp/Pfette` | `move -> _database/bauteiltyp/Traeger` | A purlin is a beam/member subtype; keep `Pfette` as raw label. | CONFIDENT |
| `_graph/bauteiltyp/Treppenwange` | `review -> _database/bauteiltyp/Traeger or _database/bauteiltyp/Treppe` | Could be structural member or stair component depending on old/new function. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Deckenplatte` | `move -> _database/bauteiltyp/Decke` | Deckenplatte is a specific slab/floor element; broad component type is Decke. | CONFIDENT |
| `_graph/bauteiltyp/Tragende_Wand` | `move -> _database/bauteiltyp/Wand` | Component type is wall; add `tragwerksprinzip/Wandtragwerk` when structural role matters. | CONFIDENT |
| `_graph/bauteiltyp/Innenwand` | `move -> _database/bauteiltyp/Wand` | Interior wall is a wall subtype; keep interior use as raw label. | CONFIDENT |
| `_graph/bauteiltyp/Bodenbelag` | `move -> _database/bauteiltyp/Boden` | Floor finish is part of the Boden component family. | CONFIDENT |
| `_graph/bauteiltyp/Bodenfliese` | `move -> _database/bauteiltyp/Boden` | Floor tile is Boden plus material/raw label. | CONFIDENT |
| `_graph/bauteiltyp/Pflaster_Bodenplatte` | `move -> _database/bauteiltyp/Boden` | Paving/floor plates belong to Boden for this ontology; keep exact raw label. | CONFIDENT |
| `_graph/bauteiltyp/Dachziegel` | `move/split -> _database/bauteiltyp/Dach + _database/material/Ziegel` | Roof tile is roof component plus brick/clay material. | CONFIDENT |
| `_graph/bauteiltyp/Vordach_Ueberdachung` | `move -> _database/bauteiltyp/Dach` | Canopy/covering is roof-family component. | CONFIDENT |
| `_graph/bauteiltyp/TGA_Element` | `move -> _database/bauteiltyp/Technik_TGA` | TGA_Element is a generic technical-building-services component. | CONFIDENT |
| `_graph/bauteiltyp/Heizkoerper` | `move -> _database/bauteiltyp/Technik_TGA` | Radiator is TGA component; keep exact raw label. | CONFIDENT |
| `_graph/bauteiltyp/Schacht` | `move -> _database/bauteiltyp/Technik_TGA` | Shaft is service/technical infrastructure component in this schema. | CONFIDENT |
| `_graph/bauteiltyp/Feuerschutztuer` | `move/split -> _database/bauteiltyp/Tuer + _database/leistungsanforderung/Brandschutz` | It is a door with fire-safety requirement, not a separate top-level component family. | CONFIDENT |
| `_graph/bauteiltyp/Innenausbau_Element` | `move -> _database/bauteiltyp/Innenausbau` | Generic fit-out element belongs to the interior-fit-out family. | CONFIDENT |
| `_graph/bauteiltyp/Kueche` | `move -> _database/bauteiltyp/Festes_Einbauteil` | Built-in kitchen is fixed fit-out, not a separate core component family. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Bruestung` | `review -> _database/bauteiltyp/Gelaender or _database/bauteiltyp/Fassade` | Bruestung can be guardrail/parapet/facade edge; needs case context. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Gelaender` | `keep -> _database/bauteiltyp/Gelaender` | Common reusable building component; specific but still useful. | CONFIDENT |
| `_graph/bauteiltyp/Blechpaneel` | `move -> _database/bauteiltyp/Platte_Paneel` | Panel is component type; broad `Metall` should stay out unless the exact metal is known. | CONFIDENT |
| `_graph/bauteiltyp/Fundament_Bodenplatte` | `move -> _database/bauteiltyp/Fundament` | Foundation is a real component family missing from the current canonical list. | CONFIDENT |
| `_graph/bauteiltyp/Holzrahmenelement` | `review -> _database/bausystem/Holzrahmenbau or _database/bauteiltyp/Wand` | Could describe a building system or a wall/panel element. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Kern` | `review -> _database/tragwerksprinzip/Wand_Kern_Tragwerk` | Structural core is usually a structural principle/system, not a reusable component type. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Moebel` | `move -> _database/bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse` | Furniture should not be counted as construction-component direct reuse unless explicitly scoped. | CONFIDENT |
| `_graph/bauteiltyp/Daemmung` | `keep -> _database/bauteiltyp/Daemmung` | Insulation is a reusable product/layer category; link material separately to `Daemmstoff`, `Mineralwolle`, etc. | CONFIDENT |
| `_graph/bauteiltyp/Fliese` | `review -> _database/bauteiltyp/Boden or _database/bauteiltyp/Wand` | Tile can be floor or wall; needs case context. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Akustikelement` | `keep -> _database/bauteiltyp/Akustikelement` | Repeated reusable fit-out/product category; not too broad and not only raw text. | CONFIDENT |
| `_graph/bauteiltyp/Beschattung_Sonnenschutz` | `keep -> _database/bauteiltyp/Beschattung_Sonnenschutz` | Distinct facade/building component category. | CONFIDENT |
| `_graph/bauteiltyp/Gitterrost` | `keep -> _database/bauteiltyp/Gitterrost` | Distinct industrial/floor/walkway component category. | CONFIDENT |
| `_graph/bauteiltyp/Auflager_Widerlager` | `keep as review fallback -> _database/bauteiltyp/Auflager_Widerlager` | Real structural support element, but may overlap with infrastructure/foundation context. | REVIEW_REQUIRED |
| `_graph/bauteiltyp/Landschaftselement` | `keep as review fallback -> _database/bauteiltyp/Landschaftselement` | Useful for outdoor reuse cases, but outside main building-component scope. | REVIEW_REQUIRED |

## Materials

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/material/Beton` | `keep -> _database/material/Beton` | Correct material class. | CONFIDENT |
| `_graph/material/Stahlbeton` | `keep -> _database/material/Stahlbeton` | Correct material class. | CONFIDENT |
| `_graph/material/Stahl` | `keep -> _database/material/Stahl` | Correct material class. | CONFIDENT |
| `_graph/material/Sekundaerstahl` | `keep -> _database/material/Sekundaerstahl` | Useful material/source subtype; do not merge with generic Stahl. | CONFIDENT |
| `_graph/material/Holz` | `keep -> _database/material/Holz` | Correct material class. | CONFIDENT |
| `_graph/material/Brettschichtholz` | `keep -> _database/material/Brettschichtholz` | Important engineered-wood material subtype. | CONFIDENT |
| `_graph/material/Brettsperrholz` | `keep -> _database/material/Brettsperrholz` | Important engineered-wood material subtype. | CONFIDENT |
| `_graph/material/Naturstein` | `keep -> _database/material/Naturstein` | Correct broad material. | CONFIDENT |
| `_graph/material/Granit` | `keep -> _database/material/Granit` | Specific stone type is useful for reuse and sourcing. | CONFIDENT |
| `_graph/material/Marmor` | `keep -> _database/material/Marmor` | Specific stone type is useful for reuse and sourcing. | CONFIDENT |
| `_graph/material/Keramik` | `keep -> _database/material/Keramik` | Correct material class. | CONFIDENT |
| `_graph/material/Sanitarkeramik` | `move -> _database/material/Keramik` | Sanitary ceramic is material subtype; component should be `bauteiltyp/Sanitaerobjekt`. | CONFIDENT |
| `_graph/material/Mineralwolle` | `keep -> _database/material/Mineralwolle` | Useful insulation material subtype; also link to `material/Daemmstoff`. | CONFIDENT |
| `_graph/material/Polystyrol` | `keep -> _database/material/Polystyrol` | Useful insulation/plastic material subtype; also link to `material/Daemmstoff`. | CONFIDENT |
| `_graph/material/Daemmstoff` | `keep -> _database/material/Daemmstoff` | Correct broad material family. | CONFIDENT |
| `_graph/material/Recyclingbeton` | `keep as review material -> _database/material/Recyclingbeton` | It is material, but do not count as direct reuse; link to recycling strategy. | REVIEW_REQUIRED |
| `_graph/material/Metall` | `keep as review fallback -> _database/material/Metall` | Broad fallback when exact metal is unknown; prefer Stahl/Aluminium when known. | REVIEW_REQUIRED |
| `_graph/material/Guss` | `review -> _database/material/Gusseisen or _database/material/Metall` | `Guss` is too ambiguous without knowing cast iron, cast steel, etc. | REVIEW_REQUIRED |
| `_graph/material/Erde` | `review -> _database/material/Lehm or _database/material/Erde` | Construction-earth context may mean Lehm; keep exact only if source needs it. | REVIEW_REQUIRED |

## Tragwerk / Bauweise / Fuegung

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/tragwerksprinzip/Skelettbauweise` | `move -> _database/tragwerksprinzip/Skeletttragwerk` | It is a structural principle; final label should be the derived structure type wording. | CONFIDENT |
| `_graph/tragwerkstyp/Skeletttragwerk` | `move -> _database/tragwerksprinzip/Skeletttragwerk` | Material-neutral skeleton is a principle, not a material/system-specific type. | CONFIDENT |
| `_graph/bausystem/Holz_Skelettbau` | `keep -> _database/bausystem/Holz_Skelettbau` | Correct as construction system; link to `tragwerkstyp/Holz_Skeletttragwerk`. | CONFIDENT |
| `_graph/bausystem/Stahl_Skelettbau` | `keep -> _database/bausystem/Stahl_Skelettbau` | Correct as construction system; link to `tragwerkstyp/Stahl_Skeletttragwerk`. | CONFIDENT |
| `_graph/bausystem/Betonfertigteil_System` | `keep -> _database/bausystem/Betonfertigteil_System` | Correct as construction system; link to concrete material and precast component/structure. | CONFIDENT |
| `_graph/tragwerkstyp/Betonfertigteiltragwerk` | `keep -> _database/tragwerkstyp/Betonfertigteiltragwerk` | Correct derived structural type. | CONFIDENT |
| `_graph/tragwerkstyp/Ortbetontragwerk` | `keep -> _database/tragwerkstyp/Ortbetontragwerk` | Correct structural type; separate from `bauweise/Ortbetonbauweise`. | CONFIDENT |
| `_graph/bauweise/Ortbetonbauweise` | `keep -> _database/bauweise/Ortbetonbauweise` | Correct construction way, not the structural type itself. | CONFIDENT |
| `_graph/fuegung_verbindung/Reversible_Fuegung` | `keep -> _database/fuegung_verbindung/Reversible_Fuegung` | Correct connection principle; derive demountable/reversible structural implications via edges. | CONFIDENT |
| `_graph/fuegung_verbindung/Beton_Fertigteile_Verbindungen` | `move -> _database/methode/Betonfertigteil_Fuegung` | This is a material/system-specific how-to topic, not one connection type. | REVIEW_REQUIRED |
| `_graph/fuegung_verbindung/Holz_Verbindungen` | `move -> _database/methode/Holzverbindungen_ReUse` | Material-specific connection overview belongs to method/how, not controlled connection knot. | REVIEW_REQUIRED |
| `_graph/fuegung_verbindung/Stahl_Verbindungen` | `move -> _database/methode/Stahlverbindungen_ReUse` | Material-specific connection overview belongs to method/how, not controlled connection knot. | REVIEW_REQUIRED |
| `_graph/fuegung_verbindung/Composite_Verbindungen` | `move -> _database/methode/Composite_Fuegung` | Material-specific connection overview belongs to method/how, not controlled connection knot. | REVIEW_REQUIRED |
| `_graph/fuegung_verbindung/Stahlseil` | `review -> _database/bauteiltyp/Stahlseil or keep as raw connection detail` | A steel cable is usually a component/tension element, not a connection principle. | REVIEW_REQUIRED |
| `_graph/fuegung_verbindung/Verleimung` | `keep -> _database/fuegung_verbindung/Verleimung` | Correct joining principle; also a known ReUse barrier. | CONFIDENT |
| `_graph/fuegung_verbindung/Verschraubung` | `keep -> _database/fuegung_verbindung/Verschraubung` | Correct joining principle. | CONFIDENT |
| `_graph/fuegung_verbindung/Vermoertelung` | `keep -> _database/fuegung_verbindung/Vermoertelung` | Correct joining principle. | CONFIDENT |
| `_graph/fuegung_verbindung/Verschweissung` | `keep -> _database/fuegung_verbindung/Verschweissung` | Correct joining principle. | CONFIDENT |
| `_graph/fuegung_verbindung/Klemmverbindung` | `keep -> _database/fuegung_verbindung/Klemmverbindung` | Correct joining principle. | CONFIDENT |
| `_graph/fuegung_verbindung/Steckverbindung` | `keep -> _database/fuegung_verbindung/Steckverbindung` | Correct joining principle. | CONFIDENT |

## Process / Method / Procurement

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/prozessphase/Ausschreibung` | `move/split -> _database/methode/ReUse_Ausschreibung + _database/beschaffungsweg/Ausschreibung + _database/dokumenttyp/Ausschreibung` | Ausschreibung is procurement/method/document logic, not a canonical process phase. | CONFIDENT |
| `_graph/prozessphase/Bestandserfassung` | `split -> _database/prozessphase/Identifikation + _database/prozessphase/Dokumentation` | Bestandserfassung contains identification and documentation work. | CONFIDENT |
| `_graph/prozessphase/Entwurf` | `move -> _database/prozessphase/Planung` | Entwurf is planning/design phase in the canonical process vocabulary. | CONFIDENT |
| `_graph/prozessphase/Betrieb_und_Rueckbauplanung` | `split -> _database/prozessphase/Betrieb + _database/prozessphase/Planung` | Combines operation and future deconstruction planning; should not stay one phase. | CONFIDENT |
| `_graph/prozessphase/Rueckbau` | `keep -> _database/prozessphase/Rueckbau` | Correct process phase. | CONFIDENT |
| `_graph/prozessphase/Transport` | `keep -> _database/prozessphase/Transport` | Correct process phase; separate from logistics strategy. | CONFIDENT |
| `_graph/logistik/Transport` | `keep -> _database/logistik/Transport` | Correct logistics topic; same label is safe because folder meaning differs. | CONFIDENT |
| `_graph/prozessphase/Lagerung` | `keep -> _database/prozessphase/Lagerung` | Correct process phase. | CONFIDENT |
| `_graph/logistik/Lagerung` | `keep -> _database/logistik/Lagerung` | Correct logistics topic; same label is safe because folder meaning differs. | CONFIDENT |
| `_graph/prozessphase/Aufbereitung` | `keep -> _database/prozessphase/Aufbereitung` | Correct process phase; concrete actions stay in `aufbereitungsverfahren`. | CONFIDENT |
| `_graph/prozessphase/Wiedereinbau` | `keep -> _database/prozessphase/Wiedereinbau` | Correct process phase. | CONFIDENT |
| `missing _graph/prozessphase/Pruefung` | `create -> _database/prozessphase/Pruefung` | Canonical process needs a testing/proof phase separate from proof types. | CONFIDENT |

## Reuse Strategy / Boundary Logic

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/reuse_strategie/Umnutzung` | `move -> _database/bauaufgabe_intervention/Umnutzung` | Umnutzung is a building intervention/use change, not component-level reuse strategy. | CONFIDENT |
| `_graph/bauaufgabe_intervention/Umnutzung` | `keep -> _database/bauaufgabe_intervention/Umnutzung` | Correct strongest type. Merge strategy content here. | CONFIDENT |
| `_graph/reuse_strategie/Bestandserhalt` | `keep -> _database/reuse_strategie/Bestandserhalt` | Valid circular strategy, but not automatically Direct Reuse. | CONFIDENT |
| `_graph/bewertungslogik_abgrenzung/Bestandserhalt_Nicht_Direct_Reuse` | `keep -> _database/bewertungslogik_abgrenzung/Bestandserhalt_Nicht_Direct_Reuse` | Correct scoring/boundary logic; prevents double-counting. | CONFIDENT |
| `_graph/bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse` | `keep -> _database/bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse` | Correct scoring/boundary logic; recycling is not direct reuse. | CONFIDENT |
| `_graph/reuse_strategie/Refurbishment` | `keep -> _database/reuse_strategie/Refurbishment` | Valid reuse strategy; concrete actions link to `aufbereitungsverfahren`. | CONFIDENT |
| `_graph/reuse_strategie/Temporaerer_Wiedereinbau` | `keep -> _database/reuse_strategie/Temporaerer_Wiedereinbau` | Valid strategy/status-like reuse pattern; link also to `reuse_einsatzstatus/Temporaer`. | REVIEW_REQUIRED |

## Norm / Requirement / Proof

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/norm/DIN_EN_15804` | `keep -> _database/norm/DIN_EN_15804` | Actual named standard. | CONFIDENT |
| `_graph/norm/EN_15804` | `move -> _database/norm/DIN_EN_15804` | Duplicate standard family in this German-context dataset; keep as alias. | CONFIDENT |
| `_graph/norm/DIN_EN_15978` | `keep -> _database/norm/DIN_EN_15978` | Actual named standard. | CONFIDENT |
| `_graph/norm/EN_1090` | `keep -> _database/norm/EN_1090` | Actual named standard. | CONFIDENT |
| `_graph/norm/ISO_14040` | `keep -> _database/norm/ISO_14040` | Actual named standard. | CONFIDENT |
| `_graph/norm/ISO_14044` | `keep -> _database/norm/ISO_14044` | Actual named standard. | CONFIDENT |
| `_graph/norm/ISO_20887` | `keep -> _database/norm/ISO_20887` | Actual named standard. | CONFIDENT |
| `_graph/norm/Wiederverwendungskriterien` | `move -> _database/methode/Wiederverwendungskriterien` | It is an assessment/decision framework, not a norm. | CONFIDENT |
| `_graph/pruefung_nachweis/Brandnachweis` | `move -> _database/pruefung_nachweis/Brandschutznachweis` | Normalize label to proof type; requirement remains `leistungsanforderung/Brandschutz`. | CONFIDENT |
| `_graph/huerde/Brandschutzkonflikt` | `keep -> _database/huerde/Brandschutzkonflikt` | Correct as project barrier; link to requirement and proof nodes. | CONFIDENT |

## Legal Conditions / Barriers

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/rechtliche_bedingung/Gewaehrleistung` | `keep -> _database/rechtliche_bedingung/Gewaehrleistung` | Legal/contractual topic; distinct from a project barrier. | CONFIDENT |
| `_graph/huerde/Gewaehrleistung` | `keep -> _database/huerde/Gewaehrleistung` | Real project barrier caused by warranty uncertainty; typed path prevents false merge. | CONFIDENT |
| `_graph/huerde/Haftung` | `keep -> _database/huerde/Haftung` | Real project barrier caused by liability uncertainty. | CONFIDENT |
| `_graph/rechtliche_bedingung/Produkthaftung` | `keep -> _database/rechtliche_bedingung/Produkthaftung` | Legal topic; not the same as hurdle. | CONFIDENT |
| `_graph/huerde/Fehlende_Lagerflaeche` | `keep -> _database/huerde/Fehlende_Lagerflaeche` | More precise and safer than broad `huerde/Lagerung`, which conflicts with phase/logistics. | CONFIDENT |
| `_graph/huerde/Logistikproblem` | `keep -> _database/huerde/Logistikproblem` | Correct broad barrier when exact logistics issue is unknown. | REVIEW_REQUIRED |
| `_graph/huerde/Performance_Nachweis` | `move -> _database/huerde/Fehlender_Performance_Nachweis` | Barrier is missing/uncertain proof, not the proof type itself. | REVIEW_REQUIRED |
| `_graph/huerde/Schadstoffbelastung` | `keep -> _database/huerde/Schadstoffbelastung` | Correct barrier; pollutant types stay in `schadstoff`, testing in `pruefung_nachweis`. | CONFIDENT |

## Data Model / Document / Software / Actor

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/datenmodell/Materialpass` | `move/merge -> _database/datenmodell/Materialpass_Schema` | `Materialpass` alone should be document; data-model node should be the schema. | CONFIDENT |
| `_graph/datenmodell/Materialpass_Schema` | `keep -> _database/datenmodell/Materialpass_Schema` | Correct data model/schema node. | CONFIDENT |
| `_graph/dokumenttyp/Materialpass` | `keep -> _database/dokumenttyp/Materialpass` | Correct document/pass type. | CONFIDENT |
| `draft zertifizierung_bewertungssystem/Material_Passport` | `delete / do not create` | Material passport is not a certification system in this ontology. | CONFIDENT |
| `draft datenmodell/Madaster` | `delete / do not create` | Madaster is a tool/platform and possibly actor, not a data model. | CONFIDENT |
| `_graph/software_digitaltool/Madaster` | `keep -> _database/software_digitaltool/Madaster` | Correct as platform/tool. | CONFIDENT |
| `_graph/akteur/Madaster` | `keep -> _database/akteur/Madaster` | Correct if used for operator/institution profile; link to tool via `operates`. | CONFIDENT |
| `_graph/datenmodell/Gebaeuderessourcenpass` | `review -> _database/datenmodell/Gebaeuderessourcenpass_Schema` | Final type is valid, but current content is a Concular profile and must be cleaned. | REVIEW_REQUIRED |
| `_graph/dokumenttyp/Gebaeuderessourcenpass` | `keep with cleanup -> _database/dokumenttyp/Gebaeuderessourcenpass` | Correct document type, but current content mixes Madaster/DGNB source profiles. | REVIEW_REQUIRED |
| `_graph/zertifizierung_bewertungssystem/DGNB` | `keep with cleanup -> _database/zertifizierung_bewertungssystem/DGNB` | DGNB rating system is valid; resource-pass content should move to document/model nodes. | REVIEW_REQUIRED |
| `_graph/akteur/DGNB` | `keep -> _database/akteur/DGNB` | Correct actor/institution node; distinct from DGNB rating system. | CONFIDENT |
| `_graph/software_digitaltool/ReUse_Toolkit` | `move/merge -> _database/dokumenttyp/ReUse_Toolkit` | Content says it is not software; it is a toolkit/guide bundle. | CONFIDENT |
| `_graph/dokumenttyp/ReUse_Toolkit` | `keep -> _database/dokumenttyp/ReUse_Toolkit` | Correct document/toolkit type. | CONFIDENT |
| `_graph/software_digitaltool/Materialdatenbank` | `move -> _database/tooltyp/Materialdatenbank` | Generic "Materialdatenbank" is a tool category, not a specific software tool. | CONFIDENT |
| `_graph/datenmodell/Materialdatenbank` | `keep -> _database/datenmodell/Materialdatenbank` | Correct as database/data-structure concept. | CONFIDENT |
| `_graph/software_digitaltool/Restado` | `keep -> _database/software_digitaltool/Restado` | Correct actual digital marketplace/tool. | CONFIDENT |
| `_graph/akteur/Restado` | `keep -> _database/akteur/Restado` | Correct if representing operator/company; link to platform via `operates`. | CONFIDENT |
| `_graph/tooltyp/Bauteilboerse` | `keep -> _database/tooltyp/Bauteilboerse` | Correct platform category. | CONFIDENT |
| `_graph/beschaffungsweg/Bauteilboerse` | `keep -> _database/beschaffungsweg/Bauteilboerse` | Correct procurement route. | CONFIDENT |
| `_graph/ressourcenquelle/Bauteilboerse` | `keep -> _database/ressourcenquelle/Bauteilboerse` | Correct source category. | CONFIDENT |
| `_graph/beschaffungsweg/Digitale_Plattform` | `keep -> _database/beschaffungsweg/Digitale_Plattform` | Broader procurement route than Bauteilboerse; useful when platform type is unknown. | CONFIDENT |

## Case / Project / Object Typed ID Rule

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/fallstudie/* same slug as projekt/bauobjekt` | `keep -> _database/fallstudie/id` | Same slug is safe because entity path gives meaning. | CONFIDENT |
| `_graph/projekt/* same slug as fallstudie/bauobjekt` | `keep -> _database/projekt/id` | Project frame is distinct from case article and physical object. | CONFIDENT |
| `_graph/bauobjekt/* same slug as fallstudie/projekt` | `keep -> _database/bauobjekt/id` | Physical object is distinct from project and case. | CONFIDENT |
| `_graph/reuse_kette/* same slug as fallstudie/projekt` | `keep -> _database/reuse_kette/id` | Reuse chain is distinct from project/case; typed ID prevents merge. | CONFIDENT |

## Final Import Rules

| old_path | decision | reason | status |
|---|---|---|---|
| `_graph/_edges/*` | `keep as import support -> _database/_edges/*` | Edges must carry relation type; they prevent false semantic merges. | CONFIDENT |
| `_graph/quelle/*` | `keep -> _database/quelle/*` | Old knowledge should be archived once as source evidence. | CONFIDENT |
| `bare slug IDs` | `delete / forbid` | Bare slugs collapse different entities; always use `entity/id`. | CONFIDENT |
