# Final Final Tree - Compact Human Approval View

Nothing has been moved. This is the target structure to approve before creating `_database`.

Legend:

- `[old knowledge]` = existing knowledge file becomes a clean semantic node.
- `[split building example]` = old `Gebäude/*.md` case was split into graph nodes.
- `[generated knot]` = repeated labels became controlled vocabulary.
- `[source archive]` = old file preserved once as evidence/source.

Full exhaustive node list: `_migration/final_final_node_approval_matrix.csv`  
Every old source file tree: `_migration/final_final_legacy_source_tree.md`

## Target Tree

```text
_database/

  _system/
    schema.md
      Human-readable entity + edge schema.
    import_manifest.md
      What was imported, when, from where.
    migration_notes.md
      Decisions, caveats, unresolved review logic.

  _edges/
    edges_reviewed.csv
      Only approved graph facts.
    edges_review_queue.csv
      Unresolved or uncertain labels. Not imported as facts.

  quelle/ (567 old files) [source archive]
    OLD_FILE_ID/
      index.md
        Source metadata, original old path, target decision.
      DATEIEN/
        original_old_file.md
    examples:
      Gebaeude_Multi_Brussels_Reuse_in_MULTI/
      bauteilboerse_restado/
      tragwerkssystem_Betonfertigteil_System/
      material_Beton/
      prozessphase_Wiedereinbau/

  fallstudie/ (99) [split building example]
    FALLSTUDIE_ID/
      index.md
        Clean case summary. No full duplicated old file text.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI/
      K118_Kopfbau_Halle_118_Winterthur/
      55_Great_Suffolk_Street_London/

  projekt/ (89) [split building example]
    PROJEKT_ID/
      index.md
        Project frame: process, intervention, participants, timeline.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI/
      Recypark_Demets_Anderlecht/
      Plattenpalast_Berlin/

  bauobjekt/ (88) [split building example]
    BAUOBJEKT_ID/
      index.md
        Physical building/object/site. City, country, type, status.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI/
      Europa_Building_Brussels/
      CRCLR_House_Impact_Hub_Berlin/

  reuse_einsatz/ (637) [split building example]
    REUSE_EINSATZ_ID/
      index.md
        One concrete reused element/material use.
        Links to fallstudie, projekt, bauobjekt, material, bauteiltyp, huerde.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/
      Multi_Brussels_Reuse_in_MULTI__006__Aufzugsmotoren/
      K118_Kopfbau_Halle_118_Winterthur__001__Stahltraeger/

  reuse_kette/ (43) [split building example]
    REUSE_KETTE_ID/
      index.md
        Donor-source-to-new-use chain.
      DATEIEN/

  reuse_kettenstation/ (86) [split building example]
    REUSE_KETTENSTATION_ID/
      index.md
        Individual station in a reuse chain: donor, storage, processing, receiver.
      DATEIEN/

  datenpunkt/ (619) [split building example]
    DATENPUNKT_ID/
      index.md
        One quantitative or factual value from a case.
        Links to kennwertdefinition.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI__Flaeche/
      Multi_Brussels_Reuse_in_MULTI__Urban_Mining_Anteil/

  akteur/ (65) [old knowledge + generated from repeated case labels]
    AKTEUR_ID/
      index.md
        Real actor: office, institution, platform operator, company, person.
      DATEIEN/
    examples:
      Rotor/
      Rotor_DC/
      Madaster/
      Zirkular_GmbH/
      Arup/
      Bauteilboerse_Bremen/

  akteur_beteiligung/ (238) [split building example]
    AKTEUR_BETEILIGUNG_ID/
      index.md
        Actor in a specific project/case with a role.
      DATEIEN/
    examples:
      Multi_Brussels_Reuse_in_MULTI__Rotor/
      Multi_Brussels_Reuse_in_MULTI__Cordeel/
      55_Great_Suffolk_Street_London__Fabrix/

  bauobjekt_beteiligung/ (0 now, schema folder)
    BAUOBJEKT_BETEILIGUNG_ID/
      index.md
        Object role in a reuse chain or project.
        Use later for donor object, receiver object, same-site object, storage/depot object.
      DATEIEN/
    examples to create later:
      CASE_ID__Donorobjekt__Building_A/
      CASE_ID__Empfaengerobjekt__Building_B/

  software_digitaltool/ (76) [old knowledge]
    TOOL_ID/
      index.md
        Digital platform/tool/software. Includes material marketplaces.
      DATEIEN/
    examples:
      Restado/
      RotorDC/
      Madaster/
      Concular/
```

## Controlled Knot Tree

```text
_database/

  bauteiltyp/ (53)
    BAUTEILTYP_ID/index.md
      Component family. Used by reuse_einsatz.
    important examples:
      Fassade/
      Platte_Paneel/
      Betonfertigteil/
      Tuer/
      Wand/
      TGA_Element/
      Deckenplatte/
      Tragstruktur/

  bauteilebene/ (0 now, schema folder)
    ID/index.md
      Scale of the reused thing.
    target knots:
      Einzelbauteil/
      Bauteilgruppe/
      System/
      Gebaeudeteil/
      Materialcharge/

  bauteilzustand/ (0 now, schema folder)
    ID/index.md
      Condition/status of a reused component.
    target knots:
      intakt/
      beschaedigt/
      kontaminiert/
      korrodiert/
      patiniert/
      geprueft/
      ungeprueft/
      restlebensdauer_unklar/

  funktionswechsel/ (0 now, schema folder)
    ID/index.md
      Whether old and new function are same or changed.
    target knots:
      gleiche_Funktion/
      neue_Funktion/
      dekorative_Funktion/
      konstruktive_Funktion/
      unbekannt/

  material/ (27)
    MATERIAL_ID/index.md
      Material class, not component.
    important examples:
      Beton/
      Stahl/
      Holz/
      Naturstein/
      Aluminium/
      Keramik/
      Sekundaerstahl/

  tragwerkstyp/ (9)
    TRAGWERKSTYP_ID/index.md
      Derived structural type, not every structural-looking word.
    important examples:
      Betonfertigteil_Tragwerk/
      Holz_Skeletttragwerk/
      Stahl_Skeletttragwerk/
      Wiederverwendetes_Betontragwerk/

  tragwerksprinzip/ (4)
    TRAGWERKSPRINZIP_ID/index.md
      Abstract structural principle.
    examples:
      Skelettbauweise/
      Massivbauweise/

  bausystem/ (3)
    BAUSYSTEM_ID/index.md
      Construction system.
    examples:
      Betonfertigteil_System/
      WBS_70/

  bauobjektklasse/ (1)
    ID/index.md
      What kind of object the Bauobjekt is.
    target knots:
      Gebaeude/
      Gebaeudeteil/
      Innenausbau/
      Infrastruktur/
      Pavillon/
      Quartier_Areal/
      Depot_Lager/

  bauobjektrolle/ (0 now, schema folder)
    ID/index.md
      Role of a Bauobjekt in a reuse chain.
    target knots:
      Donorobjekt/
      Empfaengerobjekt/
      Same_Site_Donor_Receiver/
      Bestandsobjekt/
      Zwischenlager/
      Referenzobjekt/

  bauobjektstatus/ (0 now, schema folder)
    ID/index.md
      Built/planned/status state of the object.
    target knots:
      gebaut/
      in_Bau/
      geplant/
      Wettbewerb/
      Prototyp/
      temporaer/
      rueckgebaut/
      unklar/

  nutzung/ (0 now, schema folder)
    ID/index.md
      Use/program of a building or object.
    target knots:
      Wohnen/
      Schule/
      Buero/
      Kultur/
      Gewerbe/
      Sozialbau/
      Infrastruktur/
      Mischnutzung/

  bauweise/ (2)
    BAUWEISE_ID/index.md
      Material/construction way.
    examples:
      Holzbauweise/

  bauaufgabe_intervention/ (3)
    ID/index.md
      Intervention type.
    examples:
      Aufstockung/
      Umbau/

  fuegung_verbindung/ (12)
    ID/index.md
      Connection/jointing principle.
    examples:
      Reversible_Fuegung/
      Verschraubung/
      Klemmverbindung/
      Verschweissung/

  reuse_strategie/ (8)
    ID/index.md
      Strategy of reuse/circularity.
    examples:
      Direct_Reuse/
      Urban_Mining/
      Design_for_Disassembly/

  prozessphase/ (9)
    ID/index.md
      Process phase.
    examples:
      Rueckbau/
      Transport/
      Lagerung/
      Aufbereitung/
      Wiedereinbau/

  aufbereitungsverfahren/ (7)
    ID/index.md
      Cleaning, repair, remanufacturing, testing preparation.

  rueckbauverfahren/ (5)
    ID/index.md
      Deconstruction/dismantling method.

  logistik/ (6)
    ID/index.md
      Transport, storage, timing, sourcing logistics.

  huerde/ (30)
    ID/index.md
      Real project barrier.
    important examples:
      Anschlussproblem/
      Verfuegbarkeitsproblem/
      Technische_Freigabe/
      Bruch_Beschaedigungsrisiko/
      Aufbereitungsaufwand/

  bewertungslogik_abgrenzung/ (7)
    ID/index.md
      Boundary/scoring logic, not real project hurdle.
    examples:
      Kein_Direct_Reuse_Nachweis/
      Bestandserhalt_Nicht_Direct_Reuse/
      Recycling_Nicht_Direct_Reuse/

  pruefung_nachweis/ (11)
    ID/index.md
      Test/evidence type.
    examples:
      Sichtpruefung/
      Materialpruefung/
      Statische_Nachweisfuehrung/
      Schadstoffscreening/

  leistungsanforderung/ (13)
    ID/index.md
      Requirement/performance demand.
    examples:
      Brandschutz/
      Schallschutz/
      Tragfaehigkeit/

  norm/ (9)
    ID/index.md
      Actual named standard.
    examples:
      EN_1090/

  rechtliche_bedingung/ (6)
    ID/index.md
      Law/regulatory topic.
    examples:
      Bauproduktrecht/
      Produkthaftung/

  kennwertdefinition/ (31)
    ID/index.md
      Type of metric.
    important examples:
      Flaeche/
      Materialmenge/
      CO2_Emissionen/
      Baukosten/
      Transportdistanz/
      Bauteilanzahl/

  datenqualitaet/ (0 now, schema folder)
    ID/index.md
      Reliability/source quality of a value or claim.
    target knots:
      belegt/
      geschaetzt/
      widerspruechlich/
      unbekannt/
      Sekundaerquelle/
      Primaerquelle/

  wirtschaft/ (6)
    ID/index.md
      Economic topic.

  schadstoff/ (5)
    ID/index.md
      Hazardous substance.
    examples:
      Asbest/
      PCB/

  foerderprogramm/ (5)
    ID/index.md
      Funding/research program.
    examples:
      BBSM/
      PREUSE/

  ort/ (12)
    ID/index.md
      Place/city/country/location knot.

  datenmodell/ (9)
    ID/index.md
      Data model/passport/model logic.
    examples:
      Materialpass/
      Madaster_Materialpass/

  dokumenttyp/ (16)
    ID/index.md
      Source/document type.

  programm_kontext/ (0 now, schema folder)
    ID/index.md
      Context/program type around a case.
    target knots:
      Foerderprogramm/
      Wettbewerb/
      Forschungsprojekt/
      kommunales_Programm/

  tooltyp/ (2)
    ID/index.md
      Type of digital tool/platform.
    examples:
      Bauteilboerse/

  beschaffungsweg/ (2)
    ID/index.md
      How components/materials are sourced.
    examples:
      Digitale_Plattform/

  ressourcenquelle/ (1)
    ID/index.md
      Resource/source category.

  akteurrolle/ (21)
    ID/index.md
      Role of an actor in a project.
    examples:
      Bauherr_Auftraggeber/
      Architektur/
      Tragwerksplanung/
      Rueckbau_Demontage/
      Materiallieferant/

  bauobjektklasse/ (1) [approve separately]
    ID/index.md
      Auxiliary object class.

  kontextmerkmal/ (2) [approve separately]
    ID/index.md
      Context marker.

  reuse_einsatzstatus/ (1) [approve separately]
    ID/index.md
      Status of reuse use.

  zertifizierung_bewertungssystem/ (1)
    ID/index.md
      Certification/rating system.
```

## How One Building File Breaks Down

Old file:

```text
Gebäude/Multi_Brussels_Reuse_in_MULTI.md
```

Clean final tree:

```text
_database/

  quelle/
    Gebaeude_Multi_Brussels_Reuse_in_MULTI/
      index.md
        Says: this is the archived old source file.
      DATEIEN/Multi_Brussels_Reuse_in_MULTI.md

  fallstudie/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
        Says: MULTI is a documented reuse/urban-mining case.

  projekt/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
        Says: project process, conversion/reconstruction, involved parties.

  bauobjekt/
    Multi_Brussels_Reuse_in_MULTI/
      index.md
        Says: physical building in Brussels, former Philips/Brouckere Tower.

  reuse_einsatz/
    Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/
      index.md
        One reused element group.
        Links:
          primary_bauteiltyp -> bauteiltyp/Fassade
          secondary_bauteiltyp -> bauteiltyp/Platte_Paneel
          material -> material/Naturstein
          huerde -> huerde/Bruch_Beschaedigungsrisiko

    Multi_Brussels_Reuse_in_MULTI__002__Blaustein_Flagstones/
      index.md
        One reused natural-stone floor/paving use.

    Multi_Brussels_Reuse_in_MULTI__003__Granitboden/
      index.md
        One reused floor material use.

    Multi_Brussels_Reuse_in_MULTI__004__Granitplatten_Terrasse/
      index.md
        One reused terrace plate use.

    Multi_Brussels_Reuse_in_MULTI__005__Aluminiumprofile/
      index.md
        One reused profile/component use.

    Multi_Brussels_Reuse_in_MULTI__006__Aufzugsmotoren/
      index.md
        One reused technical component use.

    Multi_Brussels_Reuse_in_MULTI__007__Tueren_Waende_Einbauten/
      index.md
        Mixed fixed building elements. Needs review if too broad.

  datenpunkt/
    Multi_Brussels_Reuse_in_MULTI__Flaeche/
      index.md
        One measured value, linked to kennwertdefinition/Flaeche.

    Multi_Brussels_Reuse_in_MULTI__Urban_Mining_Anteil/
      index.md
        One metric, linked to relevant kennwertdefinition.

  akteur_beteiligung/
    Multi_Brussels_Reuse_in_MULTI__Rotor/
      index.md
        Rotor's role in this case.

    Multi_Brussels_Reuse_in_MULTI__Cordeel/
      index.md
        Cordeel's role in this case.

  software_digitaltool/
    Madaster/
      index.md
        Tool/platform used for material passport logic.
```

Human explanation:

The old building file is not one final node. It becomes a source archive plus a small case graph. The building story is `fallstudie`; the actual building is `bauobjekt`; every reused component line becomes `reuse_einsatz`; numbers become `datenpunkt`; people/companies become `akteur_beteiligung`; reusable categories such as material, component type, hurdle and metric are linked as knots.

## How One Actor File Breaks Down

Old file:

```text
akteur/.../Rotor.md
```

Clean final tree:

```text
_database/
  quelle/
    akteur_Rotor/
      index.md
      DATEIEN/Rotor.md

  akteur/
    Rotor/
      index.md
        Canonical actor profile.

  akteur_beteiligung/
    CASE_ID__Rotor/
      index.md
        Rotor's role in one specific project.

  akteurrolle/
    Reuse_Beratung/
      index.md
        Controlled role knot.
```

Human explanation:

`akteur/Rotor` is the actor itself. `akteur_beteiligung/...Rotor` is Rotor in one concrete case. `akteurrolle/Reuse_Beratung` is the role type.

## How One Bauteilboerse File Breaks Down

Old file:

```text
bauteilboerse/restado.md
```

Clean final tree:

```text
_database/
  quelle/
    bauteilboerse_restado/
      index.md
      DATEIEN/restado.md

  software_digitaltool/
    Restado/
      index.md
        Digital marketplace/tool.

  tooltyp/
    Bauteilboerse/
      index.md
        Platform type.

  beschaffungsweg/
    Digitale_Plattform/
      index.md
        Procurement path.

  ressourcenquelle/
    Bauteilboerse/
      index.md
        Resource source type.
```

Human explanation:

There is no final `bauteilboerse` entity. Restado is a `software_digitaltool`; "Bauteilboerse" is a tool type/source/procurement classification.

## How One Tragwerkssystem File Breaks Down

Old file:

```text
tragwerkssystem/Betonfertigteil_System.md
```

Clean final tree:

```text
_database/
  quelle/
    tragwerkssystem_Betonfertigteil_System/
      index.md
      DATEIEN/Betonfertigteil_System.md

  bausystem/
    Betonfertigteil_System/
      index.md
        Correct semantic entity: construction/system logic.

  tragwerkstyp/
    Betonfertigteil_Tragwerk/
      index.md
        Derived structural type.

  bauteiltyp/
    Betonfertigteil/
      index.md
        Component family.

  material/
    Beton/
      index.md
        Material family.
```

Human explanation:

`Betonfertigteil-System` is not itself just a "tragwerk". It is first a `bausystem`. From that, the graph can derive `tragwerkstyp/Betonfertigteil_Tragwerk`, and link relevant `bauteiltyp` and `material`.

## Folders Not In First Final Version

```text
_database/
  meta/                         hold outside final database
  akteurleistung/               exclude for now
  akteurtyp/                    exclude for now
  beleg/                        exclude for now
  gebaeudetypologie/            exclude for now
  plattformfunktion/            exclude for now
  plattformzugang/              exclude for now
```

Reason:

These are empty, immature, or not necessary for the first clean database version.
