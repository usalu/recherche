# Ontology Overlap And Conflict Report

Status: double-check before final move.  
Scope checked: `_migration/15_Detailed_Final_Ontology_Tree.md`, `_migration/final_schema_folder_decisions.csv`, `_migration/12_Final_Final_Approval_Preview.md`, `_migration/final_final_tree_all_nodes.md`, and current staged `_graph` folder names.

## Short Verdict

The final ontology is usable, but it should not be imported exactly as the current `_graph` staging stands.

There are three kinds of overlap:

1. **Safe typed overlap**: same label in different folders is okay if the relation is explicit, e.g. `akteur/Madaster` versus `software_digitaltool/Madaster`.
2. **Semantic conflict**: current staging puts one concept in the wrong entity level, e.g. `material/Beton_Fertigteile`.
3. **Migration artifact**: accidental generated nodes such as `fallstudie/index` and `reuse_kette/index`.

The high-risk items below should be fixed before creating `_database`.

## High-Risk Fix Before Final Move

| Issue | Current Conflict | Decision |
|---|---|---|
| Material vs component | `material/Beton_Fertigteile` overlaps with `bauteiltyp/Betonfertigteil` | Keep `Betonfertigteil` only as `bauteiltyp`; material should be `Beton` or `Stahlbeton`. |
| Ziegel ambiguity | `bauteiltyp/Ziegel` and `material/Ziegel` conceptually overlap | Keep `material/Ziegel`; if component is needed use `bauteiltyp/Mauerstein_Block` or create `bauteiltyp/Ziegelstein_Mauerstein`, not plain `Ziegel`. |
| Dachtragwerk level | `bauteiltyp/Dachtragwerk` and `tragwerkstyp/Dachtragwerk` | Keep `Dachtragwerk` as `tragwerkstyp`; map bauteil details to `Dach`, `Traeger`, `Pfette`, etc. |
| Tragstruktur fallback | `bauteiltyp/Tragstruktur` can duplicate `tragwerkstyp/*` | Use only when the source says reused "structure/frame" and no finer component is known. Otherwise link to `tragwerkstyp` plus concrete `bauteiltyp`. |
| Bauwerksteil too vague | `bauteiltyp/Bauwerksteil` overlaps with `bauobjektklasse/Gebaeudeteil` | Use `bauobjekt` + `bauobjektklasse/Gebaeudeteil` for physical object parts. Keep `bauteiltyp/Bauwerksteil` only as temporary review fallback. |
| Umnutzung as strategy | `reuse_strategie/Umnutzung` duplicates `bauaufgabe_intervention/Umnutzung` | Prefer `bauaufgabe_intervention/Umnutzung`. Use reuse strategy only for circular strategy, not general building-use change. |
| Bestandserhalt/Recycling scoring | `reuse_strategie/Bestandserhalt`, `reuse_strategie/Recycling`, and `bewertungslogik_abgrenzung/*` can double-count Direct Reuse | Strategy says what the project does. `bewertungslogik_abgrenzung` says how it is counted. Do not count `Bestandserhalt` or `Recycling` as Direct Reuse unless a separate `Reuse_Einsatz` proves component reuse. |
| Process vs procurement | `prozessphase/Ausschreibung`, `beschaffungsweg/*`, `dokumenttyp/Ausschreibung`, `rechtliche_bedingung/Vergaberecht` | Remove `Ausschreibung` from canonical `prozessphase`. Use `beschaffungsweg/Ausschreibung` for sourcing route, `dokumenttyp/Ausschreibung` for document, `rechtliche_bedingung/Vergabe` for legal topic. |
| Process phase names | Current `Bestandserfassung`, `Entwurf`, `Betrieb_und_Rueckbauplanung` are not canonical | Map to `Identifikation + Dokumentation`, `Planung`, and `Betrieb + Planung`. Add missing canonical `Pruefung`. |
| Generic norm nodes | Draft mentioned `Eurocode`, `DIN`, `SIA`, `Nationale_Norm`, `Technische_Richtlinie` | Do not import these as normal `norm` nodes unless marked as `node_kind: category`. Prefer actual named standards like `EN_1090`, `ISO_20887`, `DIN_EN_15804`. |
| Duplicate norm | `DIN_EN_15804` and `EN_15804` | Merge to one canonical node, probably `DIN_EN_15804` if German context matters. |
| Not-a-norm | `norm/Wiederverwendungskriterien` | Move to `leistungsanforderung`, `methode`, or `bewertungslogik_abgrenzung`; not a norm. |
| Material passport collision | `datenmodell/Materialpass`, `datenmodell/Materialpass_Schema`, `dokumenttyp/Materialpass`, `zertifizierung_bewertungssystem/Material_Passport` | Use `datenmodell/Materialpass_Schema` for model, `dokumenttyp/Materialpass` for document. Remove `Material_Passport` from certification unless it is a real rating/certification in a source. |
| Madaster collision | Draft puts `Madaster` in `datenmodell` and `software_digitaltool` | Keep `software_digitaltool/Madaster`. Model is `datenmodell/Materialpass_Schema` or `Gebaeuderessourcenpass`, implemented by Madaster. |
| Materialdatenbank collision | `datenmodell/Materialdatenbank` and `software_digitaltool/Materialdatenbank` | If it is a software/platform type, use `tooltyp/Materialdatenbank`; if it is a data structure, use `datenmodell`. Do not keep a generic software node named only `Materialdatenbank`. |
| Accidental index nodes | `_graph/fallstudie/index`, `_graph/reuse_kette/index`, `_graph/reuse_kettenstation/index__Donor`, `_graph/reuse_kettenstation/index__Receiver` | Exclude/delete from final import. These are migration artifacts. |
| Datapoint/reuse same ID | Examples: `Timber_Square_London__001__Wiederverwendete_Stahltr_ger` appears as `datenpunkt` and `reuse_einsatz`; same for one ELYS Fenster row | Rename or review datapoints. A datapoint should be a value, not the same ID as a reused component. |

## Medium-Risk Overlap: Keep, But Define Clearly

| Overlap | Safe Rule |
|---|---|
| `fallstudie`, `projekt`, `bauobjekt`, `reuse_kette` often share the same case slug | Safe if IDs are imported as `entity/id`, not just `id`. Relations should say: `fallstudie documents projekt`, `projekt uses bauobjekt`, `reuse_kette belongs_to fallstudie/project`. |
| `akteur` and `akteur_beteiligung` | `akteur` is the real organization/person. `akteur_beteiligung` is a role in one project/case. |
| `akteurrolle` and `akteur_beteiligung` | `akteurrolle` is vocabulary; `akteur_beteiligung` is event/participation. |
| `bauobjektrolle` and `bauobjekt_beteiligung` | `bauobjektrolle` is vocabulary; `bauobjekt_beteiligung` is object-in-chain participation. |
| `Restado`, `Madaster`, `Bauteilboerse_Bremen` as actor and digital tool | Safe if actor means operator/institution and software means platform/tool. Use edge `akteur operates software_digitaltool`. |
| `DGNB` as actor and certification system | Safe if `akteur/DGNB` is the institution and `zertifizierung_bewertungssystem/DGNB` is the rating system. |
| `Transport` and `Lagerung` in `prozessphase` and `logistik` | Safe if process phase means "when it happens"; logistics means "how it is organized/measured". |
| `Pruefung` in `prozessphase` and `pruefung_nachweis` | Safe if phase is process step; proof node is evidence/test type. |
| `Aufbereitung` and `aufbereitungsverfahren` | Safe if phase is process step; method is the concrete action such as Reinigung, Zuschnitt, Reparatur. |
| `Rueckbau` and `rueckbauverfahren` | Safe if phase is process step; method is selektiver Rueckbau, Demontage, etc. |
| `Brandschutz` in performance/proof/hurdle | Safe if separated as: requirement = `leistungsanforderung/Brandschutz`, proof = `pruefung_nachweis/Brandschutznachweis`, barrier = `huerde/Brandschutzkonflikt` or `huerde/Normunsicherheit`. |
| `Haftung`/`Gewaehrleistung` in law and hurdle | Legal topic goes to `rechtliche_bedingung`; project obstacle goes to `huerde/Versicherung_Haftung` or specific hurdle. |
| `Kosten` in `kennwertdefinition`, `wirtschaft`, and `huerde` | `kennwertdefinition` is measured value type; `wirtschaft` is economic topic; `huerde` is a project obstacle. Prefer specific nodes like `Baukosten`, `Mehrkosten`, `Kostenrisiko`. |
| `Design_for_Disassembly` in `methode` and `reuse_strategie` | Safe if `methode` is knowledge/method page and `reuse_strategie` is case classification. |
| `Materialpass` as data model and document | Safe only if names make the distinction visible: `datenmodell/Materialpass_Schema` and `dokumenttyp/Materialpass`. |

## Current Staging Gaps That Are Not Conflicts

These are incomplete but not dangerous if treated as schema folders:

| Folder | Current State | Action |
|---|---|---|
| `bauobjektrolle` | 0 nodes | Create schema folder; populate later from donor/receiver roles. |
| `bauobjektstatus` | 0 nodes | Create schema folder; no fake facts. |
| `nutzung` | 0 nodes | Create schema folder; map uses later. |
| `bauteilebene` | 0 nodes | Create schema folder; useful for Einzelbauteil/System/Materialcharge. |
| `bauteilzustand` | 0 nodes | Create schema folder; populate from review. |
| `funktionswechsel` | 0 nodes | Create schema folder; populate when old/new function is known. |
| `datenqualitaet` | 0 nodes | Create schema folder; useful for values and claims. |
| `programm_kontext` | 0 nodes | Create schema folder; link concrete `foerderprogramm` nodes to it. |

## Specific Folder Decisions

### Bauteilboerse / Digital Platforms

Do not create a final `bauteilboerse` core entity.

Correct split:

```text
software_digitaltool/Restado
tooltyp/Bauteilboerse
beschaffungsweg/Bauteilboerse or beschaffungsweg/Digitale_Plattform
ressourcenquelle/Bauteilboerse
akteur/Restado if the operator/company is discussed
```

This is not a conflict if the graph relation says what each node means.

### Reuse Centre

Current staging has `bauobjektklasse/Reuse_Centre`. This is too specific for the final canonical object class list.

Better final mapping:

```text
bauobjektklasse/Depot_Lager
bauobjektrolle/Zwischenlager
reuse_kettenstation/[station node with role storage/processing/marketplace]
```

Keep the exact term "Reuse Centre" as a title, alias, or raw label if the source uses it.

### Actor / Platform Hybrids

Examples: `Madaster`, `Restado`, `Bauteilboerse_Bremen`, `Bauteilnetz_Deutschland`.

Correct pattern:

```text
akteur/[operator or organization]
software_digitaltool/[platform or tool]
tooltyp/[tool category]
```

Do not merge the actor and tool just because they share a public name.

### Case / Project / Building

Repeated slugs across `fallstudie`, `projekt`, and `bauobjekt` are expected. The conflict is only dangerous if Tolaria imports node IDs without the entity prefix.

Use global node ID:

```text
fallstudie/Multi_Brussels_Reuse_in_MULTI
projekt/Multi_Brussels_Reuse_in_MULTI
bauobjekt/Multi_Brussels_Reuse_in_MULTI
```

Do not use only:

```text
Multi_Brussels_Reuse_in_MULTI
```

## Consequences If Not Fixed

- Direct Reuse statistics can become wrong because `Bestandserhalt`, `Recycling`, planned reuse, and actual reused components may be counted together.
- Material queries become polluted if component types stay in `material`, especially `Beton_Fertigteile`.
- Component queries become noisy if system/structure terms stay in `bauteiltyp`, especially `Dachtragwerk` and `Tragstruktur`.
- Digital platform queries split across actor/tool/data-model folders without clear edges.
- Standards analysis becomes unreliable if generic families and non-norm criteria are stored as `norm`.
- SQLite/Tolaria joins can collapse different nodes with the same slug unless every node ID includes the entity folder.
- Review queues become harder because broad fallback nodes like `Bauwerksteil`, `Tragstruktur`, and `Materialdatenbank` hide what is actually unknown.

## Required Cleanup Checklist

Before final `_database` creation:

1. Exclude migration artifacts: `fallstudie/index`, `reuse_kette/index`, `reuse_kettenstation/index__Donor`, `reuse_kettenstation/index__Receiver`.
2. Normalize `bauteiltyp` to the approved broad families; keep details as raw labels or aliases.
3. Move `material/Beton_Fertigteile` to `bauteiltyp/Betonfertigteil`.
4. Resolve `Ziegel`, `Dachtragwerk`, `Tragstruktur`, and `Bauwerksteil` according to semantic level.
5. Replace current process phases with canonical `Identifikation`, `Dokumentation`, `Pruefung`, `Rueckbau`, `Transport`, `Lagerung`, `Aufbereitung`, `Planung`, `Wiedereinbau`, `Betrieb`.
6. Remove `Ausschreibung` from canonical `prozessphase`; keep it as procurement/document/legal topic where needed.
7. Clean `norm`: merge `EN_15804`/`DIN_EN_15804`; remove `Wiederverwendungskriterien`; avoid generic norm-family nodes as facts.
8. Split passport/tool concepts: `Materialpass_Schema`, `dokumenttyp/Materialpass`, `software_digitaltool/Madaster`.
9. Keep actor/tool duplicates only with explicit `operates`, `provides`, or `is_operator_of` edges.
10. Make Tolaria/SQLite node IDs path-based: `entity/id`.

## Final Assessment

No need to redesign the whole ontology again. The entity list is strong.

The problem is mainly **normalization before import**:

- keep the final entity folders,
- keep typed overlaps where they represent different real things,
- remove migration artifacts,
- tighten ambiguous knots before creating `_database`.

