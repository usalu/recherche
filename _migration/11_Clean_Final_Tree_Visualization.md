# Clean Final Tree Visualization

## Important

This is only the target picture. Nothing has been moved yet.

Proposed final root:

```text
_database/
```

## Final Root Tree

```text
_database/
  _system/
    schema.md
    import_manifest.md
    migration_notes.md

  _edges/
    edges_reviewed.csv
    edges_review_queue.csv
    edge_schema.md

  quelle/
    SOURCE_ID/
      index.md
      DATEIEN/
        original_legacy_file.md

  fallstudie/
    FALLSTUDIE_ID/
      index.md
      DATEIEN/

  projekt/
    PROJEKT_ID/
      index.md
      DATEIEN/

  bauobjekt/
    BAUOBJEKT_ID/
      index.md
      DATEIEN/

  reuse_einsatz/
    REUSE_EINSATZ_ID/
      index.md
      DATEIEN/

  reuse_kette/
    REUSE_KETTE_ID/
      index.md
      DATEIEN/

  reuse_kettenstation/
    REUSE_KETTENSTATION_ID/
      index.md
      DATEIEN/

  datenpunkt/
    DATENPUNKT_ID/
      index.md
      DATEIEN/

  akteur/
    AKTEUR_ID/
      index.md
      DATEIEN/

  akteur_beteiligung/
    AKTEUR_BETEILIGUNG_ID/
      index.md
      DATEIEN/

  software_digitaltool/
    TOOL_ID/
      index.md
      DATEIEN/
```

## Final Knot Tree

These are classification folders. They use the same `ID/index.md` pattern.

```text
_database/
  bauteiltyp/
    BAUTEILTYP_ID/
      index.md
      DATEIEN/

  material/
    MATERIAL_ID/
      index.md
      DATEIEN/

  tragwerkstyp/
    TRAGWERKSTYP_ID/
      index.md
      DATEIEN/

  tragwerksprinzip/
    TRAGWERKSPRINZIP_ID/
      index.md
      DATEIEN/

  bausystem/
    BAUSYSTEM_ID/
      index.md
      DATEIEN/

  bauweise/
    BAUWEISE_ID/
      index.md
      DATEIEN/

  bauaufgabe_intervention/
    BAUAUFGABE_ID/
      index.md
      DATEIEN/

  fuegung_verbindung/
    FUEGUNG_ID/
      index.md
      DATEIEN/

  reuse_strategie/
    REUSE_STRATEGIE_ID/
      index.md
      DATEIEN/

  prozessphase/
    PROZESSPHASE_ID/
      index.md
      DATEIEN/

  aufbereitungsverfahren/
    AUFBEREITUNGSVERFAHREN_ID/
      index.md
      DATEIEN/

  rueckbauverfahren/
    RUECKBAUVERFAHREN_ID/
      index.md
      DATEIEN/

  logistik/
    LOGISTIK_ID/
      index.md
      DATEIEN/

  huerde/
    HUERDE_ID/
      index.md
      DATEIEN/

  bewertungslogik_abgrenzung/
    ABGRENZUNG_ID/
      index.md
      DATEIEN/

  pruefung_nachweis/
    PRUEFUNG_ID/
      index.md
      DATEIEN/

  leistungsanforderung/
    LEISTUNGSANFORDERUNG_ID/
      index.md
      DATEIEN/

  norm/
    NORM_ID/
      index.md
      DATEIEN/

  rechtliche_bedingung/
    RECHT_ID/
      index.md
      DATEIEN/

  kennwertdefinition/
    KENNWERT_ID/
      index.md
      DATEIEN/

  wirtschaft/
    WIRTSCHAFT_ID/
      index.md
      DATEIEN/

  schadstoff/
    SCHADSTOFF_ID/
      index.md
      DATEIEN/

  foerderprogramm/
    FOERDERPROGRAMM_ID/
      index.md
      DATEIEN/

  ort/
    ORT_ID/
      index.md
      DATEIEN/

  datenmodell/
    DATENMODELL_ID/
      index.md
      DATEIEN/

  dokumenttyp/
    DOKUMENTTYP_ID/
      index.md
      DATEIEN/

  tooltyp/
    TOOL_TYP_ID/
      index.md
      DATEIEN/

  beschaffungsweg/
    BESCHAFFUNGSWEG_ID/
      index.md
      DATEIEN/

  ressourcenquelle/
    RESSOURCENQUELLE_ID/
      index.md
      DATEIEN/

  zertifizierung_bewertungssystem/
    ZERTIFIZIERUNG_ID/
      index.md
      DATEIEN/
```

## Concrete Example: MULTI Brussels

Old source file:

```text
Gebäude/
  Multi_Brussels_Reuse_in_MULTI.md
```

Clean final result:

```text
_database/
  quelle/
    Gebaeude_Multi_Brussels_Reuse_in_MULTI/
      index.md
      DATEIEN/
        Multi_Brussels_Reuse_in_MULTI.md

  fallstudie/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
      DATEIEN/

  projekt/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
      DATEIEN/

  bauobjekt/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
      DATEIEN/

  reuse_einsatz/
    Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__002__Blaustein_Flagstones/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__003__Granitboden/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__004__Granitplatten_Terrasse/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__005__Aluminiumprofile/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__006__Aufzugsmotoren/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__007__Tueren_Waende_Einbauten/
      index.md
      DATEIEN/

  datenpunkt/
    Multi_Brussels_Reuse_in_MULTI__001__Flaeche/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__002__Urban_Mining_Anteil/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__003__Betonbestand_Erhalten/
      index.md
      DATEIEN/

  akteur_beteiligung/
    Multi_Brussels_Reuse_in_MULTI__001__Whitewood/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__002__Immobel/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__003__CONIX_RDBM/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__004__Cordeel/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__005__Rotor/
      index.md
      DATEIEN/

    Multi_Brussels_Reuse_in_MULTI__006__RotorDC/
      index.md
      DATEIEN/

  akteur/
    Rotor/
      index.md
      DATEIEN/

    RotorDC/
      index.md
      DATEIEN/

  software_digitaltool/
    Madaster/
      index.md
      DATEIEN/

  material/
    Naturstein/
      index.md
      DATEIEN/

    Aluminium/
      index.md
      DATEIEN/

  bauteiltyp/
    Fassade/
      index.md
      DATEIEN/

    Platte_Paneel/
      index.md
      DATEIEN/

    Bodenbelag/
      index.md
      DATEIEN/

    TGA_Element/
      index.md
      DATEIEN/

    Tuer/
      index.md
      DATEIEN/

    Wand/
      index.md
      DATEIEN/

    Festes_Einbauteil/
      index.md
      DATEIEN/

  huerde/
    Bruch_Beschaedigungsrisiko/
      index.md
      DATEIEN/

    Aufbereitungsaufwand/
      index.md
      DATEIEN/

  kennwertdefinition/
    Flaeche/
      index.md
      DATEIEN/

    Materialmenge/
      index.md
      DATEIEN/

    Recyclingquote/
      index.md
      DATEIEN/

  datenmodell/
    Materialpass/
      index.md
      DATEIEN/

  zertifizierung_bewertungssystem/
    BREEAM/
      index.md
      DATEIEN/
```

## Concrete Example: Restado

Old source file:

```text
bauteilboerse/
  restado.md
```

Clean final result:

```text
_database/
  quelle/
    Bauteilboerse_restado/
      index.md
      DATEIEN/
        restado.md

  software_digitaltool/
    Restado/
      index.md
      DATEIEN/

  tooltyp/
    Bauteilboerse/
      index.md
      DATEIEN/

  beschaffungsweg/
    Digitale_Plattform/
      index.md
      DATEIEN/

  ressourcenquelle/
    Bauteilboerse/
      index.md
      DATEIEN/
```

Restado should not become a separate `bauteilboerse` entity in the final structure. It is a `software_digitaltool` with platform/marketplace classifications.

## Concrete Example: Betonfertigteil-System

Old source file:

```text
tragwerkssystem/
  Betonfertigteil_System.md
```

Clean final result:

```text
_database/
  quelle/
    Tragwerkssystem_Betonfertigteil_System/
      index.md
      DATEIEN/
        Betonfertigteil_System.md

  bausystem/
    Betonfertigteil_System/
      index.md
      DATEIEN/

  tragwerkstyp/
    Betonfertigteil_Tragwerk/
      index.md
      DATEIEN/

  bauteiltyp/
    Betonfertigteil/
      index.md
      DATEIEN/

  material/
    Beton/
      index.md
      DATEIEN/
```

Semantic rule:

```text
Betonfertigteil-System = Bausystem
derived structural type = Betonfertigteil-Tragwerk
component family = Betonfertigteil
material = Beton
```

## What Should Not Appear In Final Tree

These should not be copied into the final tree unless later approved:

```text
_database/
  akteurleistung/
  akteurtyp/
  bauobjekt_beteiligung/
  bauobjektrolle/
  bauobjektstatus/
  bauteilebene/
  bauteilzustand/
  beleg/
  datenqualitaet/
  funktionswechsel/
  gebaeudetypologie/
  nutzung/
  plattformfunktion/
  plattformzugang/
  programm_kontext/
```

Reason:

They are empty, immature, or not needed for the clean first database version.

## What A Clean Node Folder Contains

Minimal:

```text
ID/
  index.md
  DATEIEN/
```

With copied source:

```text
ID/
  index.md
  DATEIEN/
    original_or_supporting_source.md
```

With no copied source:

```text
ID/
  index.md
  DATEIEN/
```

## What The Final Move Should Produce

At the end, the clean database should look like this:

```text
_database/
  _system/
  _edges/
  quelle/
  fallstudie/
  projekt/
  bauobjekt/
  reuse_einsatz/
  reuse_kette/
  reuse_kettenstation/
  datenpunkt/
  akteur/
  akteur_beteiligung/
  software_digitaltool/
  bauteiltyp/
  material/
  tragwerkstyp/
  tragwerksprinzip/
  bausystem/
  bauweise/
  bauaufgabe_intervention/
  fuegung_verbindung/
  reuse_strategie/
  prozessphase/
  aufbereitungsverfahren/
  rueckbauverfahren/
  logistik/
  huerde/
  bewertungslogik_abgrenzung/
  pruefung_nachweis/
  leistungsanforderung/
  norm/
  rechtliche_bedingung/
  kennwertdefinition/
  wirtschaft/
  schadstoff/
  foerderprogramm/
  ort/
  datenmodell/
  dokumenttyp/
  tooltyp/
  beschaffungsweg/
  ressourcenquelle/
  zertifizierung_bewertungssystem/
```
