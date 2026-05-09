# Target Ontology Comparison

Compared against your proposed entity/knot list.

## Short Result

Your structure is better as the final schema.

The current preview already has most entities, but I was too conservative by excluding several empty-but-important schema folders. For the final database, these should exist even if they start with zero nodes, because they are important graph categories.

## Core Entities

| Your entity | Current preview | Decision |
|---|---:|---|
| `Fallstudie` | yes, 99 | keep |
| `Projekt` | yes, 89 | keep |
| `Bauobjekt` | yes, 88 | keep |
| `Akteur` | yes, 65 | keep |
| `Reuse_Einsatz` | yes, 637 | keep as central entity |
| `Reuse_Kette` | yes, 43 | keep |
| `Reuse_Kettenstation` | yes, 86 | keep |
| `Akteur_Beteiligung` | yes, 238 | keep |
| `Bauobjekt_Beteiligung` | exists but excluded/empty | promote into final schema |
| `Datenpunkt` | yes, 619 | keep |
| `Quelle` | yes, but final should archive all 567 old files | keep and expand |

Extra but needed:

| Entity | Current preview | Decision |
|---|---:|---|
| `Software_Digitaltool` | yes, 76 | keep as concrete entity, not only knot |

Reason: Restado, RotorDC, Madaster, Concular are actual tools/platforms. They need node pages.

## Controlled Knots

### Bauobjekt

| Your knot | Current preview | Decision |
|---|---:|---|
| `Bauobjektklasse` | yes, 1 | keep |
| `Bauobjektrolle` | excluded/empty | add to final schema |
| `Bauobjektstatus` | excluded/empty | add to final schema |
| `Nutzung` | excluded/empty | add to final schema |
| `Bauaufgabe_Intervention` | yes, 3 | keep |
| `Ort` | yes, 12 | keep |

### Reuse

| Your knot | Current preview | Decision |
|---|---:|---|
| `Reuse_Strategie` | yes, 8 | keep |
| `Bewertungslogik_Abgrenzung` | yes, 7 | keep |
| `Reuse_Einsatzstatus` | yes, 1 | keep and expand |
| `Ressourcenquelle` | yes, 1 | keep and expand |
| `Beschaffungsweg` | yes, 2 | keep and expand |

### Bauteil / Material

| Your knot | Current preview | Decision |
|---|---:|---|
| `Bauteiltyp` | yes, 53 | keep |
| `Bauteilebene` | excluded/empty | add to final schema |
| `Material` | yes, 27 | keep |
| `Bauteilzustand` | excluded/empty | add to final schema |
| `Funktionswechsel` | excluded/empty | add to final schema |

### Tragwerk / Bauweise

| Your knot | Current preview | Decision |
|---|---:|---|
| `Bauweise` | yes, 2 | keep and expand |
| `Bausystem` | yes, 3 | keep and expand |
| `Tragwerksprinzip` | yes, 4 | keep |
| `Tragwerkstyp` | yes, 9 | keep |
| `Fuegung_Verbindung` | yes, 12 | keep |

### Process / Methods

| Your knot | Current preview | Decision |
|---|---:|---|
| `Prozessphase` | yes, 9 | keep and expand |
| `Rueckbauverfahren` | yes, 5 | keep |
| `Aufbereitungsverfahren` | yes, 7 | keep |
| `Logistik` | yes, 6 | keep |

### Requirements / Barriers

| Your knot | Current preview | Decision |
|---|---:|---|
| `Pruefung_Nachweis` | yes, 11 | keep |
| `Leistungsanforderung` | yes, 13 | keep |
| `Norm` | yes, 9 | keep |
| `Rechtliche_Bedingung` | yes, 6 | keep |
| `Schadstoff` | yes, 5 | keep |
| `Huerde` | yes, 30 | keep |

### Data / Evaluation

| Your knot | Current preview | Decision |
|---|---:|---|
| `Kennwertdefinition` | yes, 31 | keep |
| `Datenqualitaet` | excluded/empty | add to final schema |
| `Zertifizierung_Bewertungssystem` | yes, 1 | keep and expand |
| `Datenmodell` | yes, 9 | keep |
| `Software_Digitaltool` | yes, 76 | keep as entity |
| `Dokumenttyp` | yes, 16 | keep |

### Context

| Your knot | Current preview | Decision |
|---|---:|---|
| `Programm_Kontext` | excluded/empty | add to final schema |
| `Kontextmerkmal` | yes, 2 | keep |
| `Wirtschaft` | yes, 6 | keep |

## Current Extras Not In Your List

| Current folder | Decision |
|---|---|
| `Akteurrolle` | keep; needed for `Akteur_Beteiligung` role normalization |
| `Tooltyp` | keep; useful for Restado/RotorDC/Madaster classification |
| `Foerderprogramm` | keep; concrete programs like BBSM/PREUSE, while `Programm_Kontext` is the type/context |
| `Methode` | keep if you want method knowledge like Form Follows Availability; otherwise move to `Quelle` only |
| `Meta` | keep out of final database |

## Corrected Final Schema

The final database should include these folders:

```text
_database/
  _system/
  _edges/

  fallstudie/
  projekt/
  bauobjekt/
  akteur/
  reuse_einsatz/
  reuse_kette/
  reuse_kettenstation/
  akteur_beteiligung/
  bauobjekt_beteiligung/
  datenpunkt/
  quelle/
  software_digitaltool/

  bauobjektklasse/
  bauobjektrolle/
  bauobjektstatus/
  nutzung/
  bauaufgabe_intervention/
  ort/

  reuse_strategie/
  bewertungslogik_abgrenzung/
  reuse_einsatzstatus/
  ressourcenquelle/
  beschaffungsweg/

  bauteiltyp/
  bauteilebene/
  material/
  bauteilzustand/
  funktionswechsel/

  bauweise/
  bausystem/
  tragwerksprinzip/
  tragwerkstyp/
  fuegung_verbindung/

  prozessphase/
  rueckbauverfahren/
  aufbereitungsverfahren/
  logistik/

  pruefung_nachweis/
  leistungsanforderung/
  norm/
  rechtliche_bedingung/
  schadstoff/
  huerde/

  kennwertdefinition/
  datenqualitaet/
  zertifizierung_bewertungssystem/
  datenmodell/
  dokumenttyp/

  programm_kontext/
  kontextmerkmal/
  wirtschaft/

  akteurrolle/
  tooltyp/
  foerderprogramm/
  methode/
```

## What Changes From My Previous Preview

Add/promote these into final schema:

```text
bauobjekt_beteiligung/
bauobjektrolle/
bauobjektstatus/
nutzung/
bauteilebene/
bauteilzustand/
funktionswechsel/
datenqualitaet/
programm_kontext/
```

Keep as extra useful schema:

```text
akteurrolle/
tooltyp/
foerderprogramm/
methode/
software_digitaltool/
```

Keep out:

```text
meta/
akteurleistung/
akteurtyp/
beleg/
plattformfunktion/
plattformzugang/
```

## Recommendation

Use your ontology as the final schema. Then migrate the current staged nodes into it, adding empty `index.md` schema placeholders for the missing controlled knots before any final move.
