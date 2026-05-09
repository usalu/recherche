# Manual Review Decision Worksheet

Use this as the single human decision sheet. Write your answer under each node.

Decision codes:

- `keep_review`: leave outside `_database`.
- `delete_from_final`: do not import as semantic node.
- `move`: one clean target.
- `split`: multiple clean targets.
- `create`: create a new clean knot, then map.

---

## `bauteiltyp/Auflager_Widerlager`

Issue: support/abutment can be component, foundation, infrastructure, or connection detail.

1. `keep_review` - keep until source context is clear.
2. `delete_from_final` - remove as too infrastructure-specific for this ontology.
3. `move -> bauteiltyp/Fundament` - if it means building support/foundation.
4. `split -> bauteiltyp/Fundament + fuegung_verbindung/*` - if support plus connection detail.
5. `create -> bauteiltyp/Auflager` - if support elements should become a reusable component family.

Your answer:

- Decision: 
- Target(s):
- Notes:

---

## `bauteiltyp/Bauwerksteil`

Issue: usually object-scale or system-scale, not a component type.

1. `keep_review` - safest default.
2. `delete_from_final` - if all content is object/context, not component.
3. `move -> bauobjekt/*` - for building, pavilion, garage, block, retained object.
4. `split -> bauobjekt/* + tragwerkstyp/* + bauteiltyp/*` - for mixed retained structure/component cases.
5. `create -> bauobjekt_beteiligung/*` - if it describes donor/receiver object role in reuse chain.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Bruestung`

Issue: can mean railing, parapet, facade edge, wall part.

1. `keep_review` - if function unclear.
2. `delete_from_final` - if too vague.
3. `move -> bauteiltyp/Gelaender` - for railing/balustrade cases.
4. `split -> bauteiltyp/Gelaender + bauteiltyp/Fassade` - if parapet/facade edge.
5. `create -> bauteiltyp/Bruestung_Parapet` - only if this distinction matters analytically.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Fliese`

Issue: tile can be wall, floor, roof tile, textile tile, or unusual product.

1. `keep_review` - if wall/floor/roof/material unclear.
2. `delete_from_final` - if already covered by raw labels and materials.
3. `move -> bauteiltyp/Boden` - for floor/terrace/paving tiles.
4. `split -> bauteiltyp/Wand or Boden or Dach + material/Keramik or Ziegel or Textil` - most likely clean solution.
5. `create -> bauteiltyp/Oberflaechenbelag` - if you want a general finish/surface component family.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Holzrahmenelement`

Issue: can be building system or wall/panel element.

1. `keep_review` - until source says system vs element.
2. `delete_from_final` - if redundant with existing clean nodes.
3. `move -> bausystem/Holzrahmenbau` - if system.
4. `split -> bausystem/Holzrahmenbau + bauteiltyp/Wand or Platte_Paneel` - if both system and reused element.
5. `create -> bauteiltyp/Holzrahmenwand` - if you need this as a recurring component knot.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Kern`

Issue: usually structural core/object context, not component type.

1. `keep_review` - safest default.
2. `delete_from_final` - if only context, not a reusable thing.
3. `move -> tragwerksprinzip/Wand_Kern_Tragwerk` - if structural core principle.
4. `split -> tragwerksprinzip/Wand_Kern_Tragwerk + bauteiltyp/Traeger or Fassade` - for steel profiles/cladding around core.
5. `create -> tragwerkstyp/Kerntragwerk` - only if core structures are a recurring analytic type.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Kueche`

Issue: kitchen can be fixed fit-out, loose furniture, equipment, or non-direct-reuse boundary.

1. `keep_review` - if fixed/loose unclear.
2. `delete_from_final` - if furniture/non-building scope.
3. `move -> bauteiltyp/Festes_Einbauteil` - for kitchen units, counters, built-in parts.
4. `split -> bauteiltyp/Festes_Einbauteil + Technik_TGA + PV_Anlage` - for mixed kitchen/TGA/solar labels.
5. `move -> bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse` - if loose furniture/decorative only.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Landschaftselement`

Issue: outside/building-adjacent scope; may be park, planter, bike rack, floor/slab.

1. `keep_review` - safest until outdoor scope is defined.
2. `delete_from_final` - if outside current building ontology.
3. `move -> bauteiltyp/Boden` - for paving, deck, parkett, skate surface.
4. `split -> bauobjekt/* + bauteiltyp/Boden + material/*` - for outdoor reused objects/materials.
5. `create -> bauobjektklasse/Aussenraum` or `bauteiltyp/Aussenraumelement` - if landscape reuse should be covered.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Tragstruktur`

Issue: not a true component type; must derive structural entity.

1. `keep_review` - safest default.
2. `delete_from_final` - if too vague.
3. `move -> tragwerkstyp/Holztragwerk or Ortbetontragwerk or Dachtragwerk` - if material/system clear.
4. `split -> tragwerkstyp/* + tragwerksprinzip/* + bauteiltyp/Traeger/Stuetze` - for mixed structural descriptions.
5. `create -> tragwerkstyp/Stahltragwerk` - likely useful gap if many steel-structure cases remain.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `bauteiltyp/Treppenwange`

Issue: stair component or structural member depending on use.

1. `keep_review` - if function unclear.
2. `delete_from_final` - if too specific.
3. `move -> bauteiltyp/Treppe` - if part of stair system.
4. `split -> bauteiltyp/Treppe + bauteiltyp/Traeger` - if reused as structural member.
5. `create -> bauteiltyp/Treppenbauteil` - if stair subcomponents matter.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `datenmodell/Gebaeuderessourcenpass`

Issue: data model is valid, but current content mixes Concular/tool/profile.

1. `keep_review` - until content is cleaned.
2. `delete_from_final` - if content is only source/vendor profile.
3. `move -> datenmodell/Gebaeuderessourcenpass_Schema` - if it describes schema/data structure.
4. `split -> datenmodell/Gebaeuderessourcenpass_Schema + software_digitaltool/Concular + akteur/Concular` - if mixed.
5. `merge -> datenmodell/Materialpass_Schema` - if concept is not distinct enough.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster`

Issue: currently component-like ID, not a clean measured datapoint.

1. `keep_review` - until value/unit/scope is known.
2. `delete_from_final` - if it is actually a reuse item, not a value.
3. `move -> reuse_einsatz/...Fenster` - if it describes the reused window use-case.
4. `split -> datenpunkt/value + reuse_einsatz/Fenster + kennwertdefinition/Bauteilanzahl` - if number of windows exists.
5. `create -> datenpunkt/ELYS...Fenster_Anzahl` - only with numeric value and unit.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger`

Issue: currently component-like ID, not a clean measured datapoint.

1. `keep_review` - until value/unit/scope is known.
2. `delete_from_final` - if it duplicates a reuse item.
3. `move -> reuse_einsatz/...Stahltraeger` - if it describes the reuse use-case.
4. `split -> datenpunkt/value + reuse_einsatz/Stahltraeger + kennwertdefinition/Materialmenge/Wiederverwendungsquote` - if metrics exist.
5. `create -> datenpunkt/Timber...Stahltraeger_Menge` - only with measured amount and unit.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `dokumenttyp/Gebaeuderessourcenpass`

Issue: valid document type, but current content mixes Madaster/DGNB/profile.

1. `keep_review` - until content is cleaned.
2. `delete_from_final` - if not a document type in your system.
3. `move -> dokumenttyp/Gebaeuderessourcenpass` - if cleaned to document/pass type only.
4. `split -> dokumenttyp/Gebaeuderessourcenpass + datenmodell/Gebaeuderessourcenpass_Schema + software_digitaltool/Madaster` - if mixed.
5. `merge -> dokumenttyp/Materialpass` - if you do not want separate resource-pass vs material-pass document types.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `fuegung_verbindung/Beton_Fertigteile_Verbindungen`

Issue: overview/how-to, not one atomic connection type.

1. `keep_review` - until split.
2. `delete_from_final` - if only a note/source dossier.
3. `move -> methode/Verbindungen_im_Betonfertigteilbau` - as method overview.
4. `split -> fuegung_verbindung/Verschraubung + Vermoertelung + Steckverbindung + Methode` - if atomic types are present.
5. `create -> methode/Betonfertigteil_Fuegung` - if method overview should be kept.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `fuegung_verbindung/Composite_Verbindungen`

Issue: composite connection overview, not atomic connection.

1. `keep_review` - until split.
2. `delete_from_final` - if only general source content.
3. `move -> methode/Verbindungen_im_Verbundbau` - as method overview.
4. `split -> fuegung_verbindung/* + material/Composite + methode/*` - if exact connection types exist.
5. `create -> methode/Composite_Fuegung` - if this overview is useful.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `fuegung_verbindung/Holz_Verbindungen`

Issue: timber connection overview, not atomic connection.

1. `keep_review` - until split.
2. `delete_from_final` - if only generic overview.
3. `move -> methode/Verbindungen_im_Holzbau` - as method overview.
4. `split -> fuegung_verbindung/Verschraubung + Steckverbindung + Verleimung + Reversible_Fuegung` - if exact types present.
5. `create -> methode/Holzbau_Fuegung` - if material-specific method overview should exist.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `fuegung_verbindung/Stahl_Verbindungen`

Issue: steel connection overview, not atomic connection.

1. `keep_review` - until split.
2. `delete_from_final` - if only generic overview.
3. `move -> methode/Verbindungen_im_Stahlbau` - as method overview.
4. `split -> fuegung_verbindung/Verschraubung + Verschweissung + Klemmverbindung` - if exact types present.
5. `create -> methode/Stahlbau_Fuegung` - if material-specific method overview should exist.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `fuegung_verbindung/Stahlseil`

Issue: steel cable is component/material, not connection principle.

1. `keep_review` - until use/function is clear.
2. `delete_from_final` - if too specific for ontology.
3. `move -> material/Stahl` - if only material fact.
4. `split -> bauteiltyp/Zugglied_Seil + material/Stahl` - if reused as tension member.
5. `create -> bauteiltyp/Seil_Zugglied` - if cable/tension members recur.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `huerde/Logistikproblem`

Issue: broad fallback, not a precise analytical hurdle.

1. `keep_review` - safest.
2. `delete_from_final` - if only vague label.
3. `move -> huerde/Fehlende_Lagerflaeche or Verfuegbarkeitsproblem or Terminunsicherheit` - if exact logistics issue clear.
4. `split -> huerde/Kompatibilitaetsproblem + Toleranzen + Bruch_Beschaedigungsrisiko` - if multiple issues.
5. `create -> huerde/Transport_Handling` - if transport/handling needs its own recurring barrier.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `huerde/Performance_Nachweis`

Issue: mixes barrier, proof/check, and performance requirement.

1. `keep_review` - safest.
2. `delete_from_final` - if too vague.
3. `move -> huerde/Technische_Freigabe or Datenluecke or Gewaehrleistung` - for barrier cases.
4. `split -> huerde/* + pruefung_nachweis/* + leistungsanforderung/*` - best for mixed labels.
5. `create -> huerde/Nachweisunsicherheit` - if missing proof is a recurring barrier you want separately.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `material/Erde`

Issue: may mean Lehm, excavated soil/resource, or earth product.

1. `keep_review` - if material meaning unclear.
2. `delete_from_final` - if it is only excavation/resource context.
3. `move -> material/Lehm` - for construction earth/pressed earth/earth plaster.
4. `split -> material/Lehm + material/Stroh` - for Stroh/Erde or earth-plaster cases.
5. `create -> material/Bauerde` - only if you need a broader earth-material category.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `material/Guss`

Issue: cast process/form, not exact material unless cast iron/steel known.

1. `keep_review` - safest.
2. `delete_from_final` - if no exact material can be known.
3. `move -> material/Stahl` - only if cast steel/steel is confirmed.
4. `split -> material/Gusseisen + material/Stahl` - if mixed cast iron/steel.
5. `create -> material/Gusseisen` - likely useful if cast iron appears repeatedly.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `material/Metall`

Issue: broad fallback material.

1. `keep_review` - recommended until exact metal is known.
2. `delete_from_final` - if broad fallback should never be a node.
3. `move -> material/Stahl or Aluminium` - only if source proves exact metal.
4. `split -> material/Stahl + Aluminium + other exact materials` - for mixed known metals.
5. `create -> material/Metall_Unbekannt` - if you intentionally want an uncertainty/fallback node.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `material/Recyclingbeton`

Issue: material plus recycling boundary; not direct reuse.

1. `keep_review` - until boundary rule decided.
2. `delete_from_final` - if recycling is outside direct-reuse scope.
3. `move -> material/Beton` - if only material class matters.
4. `split -> material/Beton + bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse` - cleanest if retained.
5. `create -> material/Recyclingbeton` - only if recycled concrete is analytically important as material class.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `reuse_strategie/Temporaerer_Wiedereinbau`

Issue: overlaps strategy and status.

1. `keep_review` - until rule decided.
2. `delete_from_final` - if status covers it.
3. `move -> reuse_einsatzstatus/Temporaer` - if temporary condition only.
4. `split -> reuse_einsatzstatus/Temporaer + reuse_strategie/Direkte_Wiederverwendung` - if both temporary and reuse strategy.
5. `create -> reuse_strategie/Temporaere_Wiederverwendung` - if temporary reuse is a real strategy in your analysis.

Your answer:

- Decision:
- Target(s):
- Notes:

---

## `zertifizierung_bewertungssystem/DGNB`

Issue: valid rating system, but current content mixes resource-pass content.

1. `keep_review` - until content cleaned.
2. `delete_from_final` - if certification systems are not needed.
3. `move -> zertifizierung_bewertungssystem/DGNB` - after stripping mixed content.
4. `split -> zertifizierung_bewertungssystem/DGNB + dokumenttyp/Gebaeuderessourcenpass + datenmodell/*` - if content contains all three.
5. `create -> programm_kontext/DGNB_Ressourcenpass` - if it is more program/context than rating system.

Your answer:

- Decision:
- Target(s):
- Notes:
