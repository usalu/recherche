# Detailed Final Ontology Tree

Purpose: this is the clean final schema with explicit subfiles/knots.

Nothing has been moved. This is the approval version before creating `_database`.

Rule:

- Core entities get data-generated IDs.
- Controlled knots get stable canonical subfiles.
- Very detailed raw labels stay in `reuse_einsatz` text or edge `raw_label`, unless they are important enough to be a canonical knot.

## 1. Core Entities

These folders do not have a fixed small list of subfiles. Their subfiles are generated from real cases, actors, sources, and reuse examples.

```text
_database/
  fallstudie/
    CASE_ID/index.md
    examples:
      Multi_Brussels_Reuse_in_MULTI/index.md
      K118_Kopfbau_Halle_118_Winterthur/index.md

  projekt/
    PROJECT_ID/index.md

  bauobjekt/
    OBJECT_ID/index.md

  akteur/
    ACTOR_ID/index.md
    examples:
      Rotor/index.md
      Zirkular_GmbH/index.md
      Arup/index.md

  reuse_einsatz/
    CASE_ID__NNN__REUSE_ITEM/index.md
    examples:
      Multi_Brussels_Reuse_in_MULTI__001__Blausteinbloecke_Fassadenplatten/index.md
      Multi_Brussels_Reuse_in_MULTI__006__Aufzugsmotoren/index.md

  reuse_kette/
    CHAIN_ID/index.md

  reuse_kettenstation/
    CHAIN_ID__STATION_ID/index.md

  akteur_beteiligung/
    CASE_ID__ACTOR_ID/index.md

  bauobjekt_beteiligung/
    CASE_ID__OBJECT_ROLE__OBJECT_ID/index.md
    starts empty; create when donor/receiver/storage object roles are explicit.

  datenpunkt/
    CASE_ID__DATAPOINT_ID/index.md

  quelle/
    OLD_FILE_ID/index.md
    DATEIEN/original_old_file.md
    final target: all 567 old files archived once.

  software_digitaltool/
    TOOL_ID/index.md
    examples:
      Restado/index.md
      RotorDC/index.md
      Madaster/index.md
      Concular/index.md
```

## 2. Bauobjekt Knots

```text
bauobjektklasse/
  Gebaeude/index.md
  Gebaeudeteil/index.md
  Innenausbau/index.md
  Infrastruktur/index.md
  Pavillon/index.md
  Quartier_Areal/index.md
  Depot_Lager/index.md

bauobjektrolle/
  Donorobjekt/index.md
  Empfaengerobjekt/index.md
  Same_Site_Donor_Receiver/index.md
  Bestandsobjekt/index.md
  Zwischenlager/index.md
  Referenzobjekt/index.md

bauobjektstatus/
  Gebaut/index.md
  In_Bau/index.md
  Geplant/index.md
  Wettbewerb/index.md
  Prototyp/index.md
  Temporaer/index.md
  Rueckgebaut/index.md
  Unklar/index.md

nutzung/
  Wohnen/index.md
  Schule_Bildung/index.md
  Buero/index.md
  Kultur/index.md
  Gewerbe/index.md
  Sozialbau/index.md
  Infrastruktur/index.md
  Mischnutzung/index.md

bauaufgabe_intervention/
  Neubau/index.md
  Umbau/index.md
  Sanierung/index.md
  Erweiterung/index.md
  Aufstockung/index.md
  Fit_out/index.md
  Translozierung/index.md
  Rueckbau/index.md
  Wiederaufbau/index.md

ort/
  ORT_ID/index.md
```

Note for `ort`: this is not a fixed vocabulary like `stadt/index.md`. It should contain concrete places, with fields in frontmatter:

```yaml
ortstyp: "Stadt | Land | Adresse | Region"
stadt:
land:
adresse:
region:
```

## 3. Reuse Knots

```text
reuse_strategie/
  Direct_Reuse/index.md
  Same_Site_Reuse/index.md
  Urban_Mining/index.md
  Design_for_Disassembly/index.md
  Bestandserhalt/index.md
  Recycling/index.md
  Upcycling/index.md
  Remanufacturing/index.md

bewertungslogik_abgrenzung/
  Zaehlt_als_Direct_Reuse/index.md
  Zaehlt_nicht_als_Direct_Reuse/index.md
  Bestandserhalt_separat/index.md
  Recycling_separat/index.md
  Moebel_Dekoration_separat/index.md
  Geplant_Nicht_Realisert/index.md
  Unklar/index.md

reuse_einsatzstatus/
  Realisiert/index.md
  Geplant/index.md
  Verworfen/index.md
  Vorgeschlagen/index.md
  Unklar/index.md
  Temporaer/index.md
  Prototypisch/index.md

ressourcenquelle/
  Donorgebaeude/index.md
  Donor_Infrastruktur/index.md
  Baustelle/index.md
  Lager/index.md
  Bauteilboerse/index.md
  Haendler/index.md
  Produktionsueberschuss/index.md
  Materialstockpile/index.md
  Unbekannt/index.md

beschaffungsweg/
  Direktvermittlung/index.md
  Ausschreibung/index.md
  Bauteilboerse/index.md
  Informelles_Netzwerk/index.md
  Eigenbestand/index.md
  Spende/index.md
  Rueckbauprojekt/index.md
```

Relevant adaptation:

- `Restado`, `RotorDC`, etc. stay under `software_digitaltool`.
- `Bauteilboerse` is a knot under `ressourcenquelle`, `beschaffungsweg`, and `tooltyp`, not a separate core entity.

## 4. Bauteil / Material Knots

Clean canonical `bauteiltyp` should be less noisy than the current 53 staging labels.

```text
bauteiltyp/
  Stuetze/index.md
  Traeger/index.md
  Decke/index.md
  Wand/index.md
  Fassade/index.md
  Fenster/index.md
  Tuer/index.md
  Treppe/index.md
  Dach/index.md
  Boden/index.md
  Innenausbau/index.md
  Festes_Einbauteil/index.md
  Technik_TGA/index.md
  Sanitaerobjekt/index.md
  Leuchte/index.md
  PV_Anlage/index.md
  Platte_Paneel/index.md
  Betonfertigteil/index.md
  Tragstruktur/index.md
  Bauwerksteil/index.md
```

Merge current staging labels into these canonical nodes:

```text
Bodenbelag, Bodenfliese, Pflaster_Bodenplatte -> Boden
TGA_Element, Heizkoerper, Schacht -> Technik_TGA
Innenausbau_Element, Kueche, Gelaender, Bruestung -> Innenausbau or Festes_Einbauteil
Dachziegel, Dachtragwerk, Vordach_Ueberdachung -> Dach
Brettschichtholzstuetze -> Stuetze
Brettsperrholzdecke -> Decke
Fachwerktraeger, Pfette, Treppenwange -> Traeger or Tragstruktur
Akustikelement, Beschattung_Sonnenschutz, Gitterrost, Blechpaneel -> keep as raw label unless repeatedly needed
```

```text
bauteilebene/
  Einzelbauteil/index.md
  Bauteilgruppe/index.md
  System/index.md
  Gebaeudeteil/index.md
  Materialcharge/index.md

material/
  Beton/index.md
  Stahlbeton/index.md
  Stahl/index.md
  Sekundaerstahl/index.md
  Holz/index.md
  Brettschichtholz/index.md
  Brettsperrholz/index.md
  Glas/index.md
  Aluminium/index.md
  Ziegel/index.md
  Naturstein/index.md
  Keramik/index.md
  Kunststoff/index.md
  Daemmstoff/index.md
  Lehm/index.md
  Stroh/index.md
  Composite/index.md
  Metall/index.md

bauteilzustand/
  Intakt/index.md
  Beschaedigt/index.md
  Kontaminiert/index.md
  Korrodiert/index.md
  Patiniert/index.md
  Geprueft/index.md
  Ungeprueft/index.md
  Restlebensdauer_bekannt/index.md
  Restlebensdauer_unklar/index.md

funktionswechsel/
  Gleiche_Funktion/index.md
  Neue_Funktion/index.md
  Dekorative_Funktion/index.md
  Konstruktive_Funktion/index.md
  Unbekannt/index.md
```

## 5. Tragwerk / Bauweise Knots

```text
bauweise/
  Holzbauweise/index.md
  Massivbauweise/index.md
  Stahlbauweise/index.md
  Hybridbauweise/index.md
  Fertigteilbauweise/index.md
  Ortbetonbauweise/index.md

bausystem/
  Betonfertigteil_System/index.md
  Holzrahmenbau/index.md
  Holz_Skelettbau/index.md
  Stahl_Skelettbau/index.md
  Plattenbau/index.md

tragwerksprinzip/
  Skeletttragwerk/index.md
  Massivtragwerk/index.md
  Fachwerk/index.md
  Rahmentragwerk/index.md
  Plattentragwerk/index.md
  Wandtragwerk/index.md
  Wand_Kern_Tragwerk/index.md

tragwerkstyp/
  Holztragwerk/index.md
  Stahltragwerk/index.md
  Betontragwerk/index.md
  Betonfertigteiltragwerk/index.md
  Wiederverwendetes_Tragwerk/index.md
  Demontierbares_Tragwerk/index.md
  Dachtragwerk/index.md

fuegung_verbindung/
  Geschraubt/index.md
  Gesteckt/index.md
  Geschweisst/index.md
  Geklebt/index.md
  Vergossen/index.md
  Reversibel/index.md
  Irreversibel/index.md
  Klemmverbindung/index.md
  Steckverbindung/index.md
  Vermoertelung/index.md
```

Semantic rule:

```text
Betonfertigteil-System -> bausystem/Betonfertigteil_System
derived structure -> tragwerkstyp/Betonfertigteiltragwerk
component family -> bauteiltyp/Betonfertigteil
material -> material/Beton
```

## 6. Process / Methods Knots

This is the style you asked for.

```text
prozessphase/
  Identifikation/index.md
  Dokumentation/index.md
  Pruefung/index.md
  Rueckbau/index.md
  Transport/index.md
  Lagerung/index.md
  Aufbereitung/index.md
  Planung/index.md
  Wiedereinbau/index.md
  Betrieb/index.md
```

Map current staging phase names:

```text
Bestandserfassung -> Identifikation + Dokumentation
Entwurf -> Planung
Betrieb_und_Rueckbauplanung -> Betrieb + Planung
Ausschreibung -> keep as Prozessphase only if needed; otherwise link to rechtliche_bedingung/Vergaberecht
```

```text
rueckbauverfahren/
  Selektiver_Rueckbau/index.md
  Zerstoerungsarmer_Rueckbau/index.md
  Demontage/index.md
  Teilrueckbau/index.md
  Ausbau_von_Bauteilen/index.md

aufbereitungsverfahren/
  Reinigung/index.md
  Zuschnitt/index.md
  Reparatur/index.md
  Pruefung/index.md
  Verstaerkung/index.md
  Remanufacturing/index.md
  Rekonditionierung/index.md
  Entmoertelung/index.md

logistik/
  Just_in_time/index.md
  Zwischenlagerung/index.md
  Lokale_Wiederverwendung/index.md
  Transportdistanz/index.md
  Bauteiltracking/index.md
  Materialmatching/index.md
  Materialverfuegbarkeit/index.md
```

## 7. Requirements / Barriers Knots

```text
pruefung_nachweis/
  Sichtpruefung/index.md
  Materialpruefung/index.md
  Tragfaehigkeitsnachweis/index.md
  Brandschutznachweis/index.md
  Schadstoffpruefung/index.md
  Geometrische_Vermessung/index.md
  Zustandsbewertung/index.md
  Zugversuch/index.md
  Schweissbarkeitspruefung/index.md

leistungsanforderung/
  Tragfaehigkeit/index.md
  Brandschutz/index.md
  Schallschutz/index.md
  Waermeschutz/index.md
  Feuchteschutz/index.md
  Dauerhaftigkeit/index.md
  Gebrauchstauglichkeit/index.md
  Rueckbaubarkeit/index.md
  Schadstofffreiheit/index.md

norm/
  Eurocode/index.md
  DIN/index.md
  SIA/index.md
  Nationale_Norm/index.md
  Technische_Richtlinie/index.md
  EN_1090/index.md
  DIN_EN_15804/index.md
  DIN_EN_15978/index.md
  ISO_14040/index.md
  ISO_14044/index.md
  ISO_20887/index.md

rechtliche_bedingung/
  Zulassung/index.md
  Haftung/index.md
  Gewaehrleistung/index.md
  Bauordnung/index.md
  Vergabe/index.md
  Eigentum/index.md
  Bauproduktrecht/index.md
  Produkthaftung/index.md

schadstoff/
  Asbest/index.md
  PCB/index.md
  PAK/index.md
  Blei/index.md
  Holzschutzmittel/index.md
  Unbekannte_Kontamination/index.md

huerde/
  Zeitdruck/index.md
  Fehlende_Dokumentation/index.md
  Normunsicherheit/index.md
  Kosten/index.md
  Lagerung/index.md
  Versicherung_Haftung/index.md
  Akzeptanz/index.md
  Verfuegbarkeit/index.md
  Logistikproblem/index.md
  Anschlussproblem/index.md
  Aufbereitungsaufwand/index.md
  Technische_Freigabe/index.md
  Bruch_Beschaedigungsrisiko/index.md
  Materialqualitaet_Unklar/index.md
  Zustand_Unklar/index.md
  Kompatibilitaetsproblem/index.md
```

Keep detailed current hurdle nodes only if they add meaning. Otherwise merge:

```text
Fehlende_Lagerflaeche -> Lagerung
Gewaehrleistung + Haftung -> Versicherung_Haftung or rechtliche_bedingung/Gewaehrleistung
Brandschutzkonflikt -> leistungsanforderung/Brandschutz + huerde/Normunsicherheit
```

## 8. Data / Evaluation Knots

```text
kennwertdefinition/
  CO2/index.md
  Masse/index.md
  Wiederverwendungsanteil/index.md
  Kosten/index.md
  Flaeche/index.md
  Bauteilanzahl/index.md
  Materialmenge/index.md
  Transportdistanz/index.md
  Bauzeit/index.md
  Baukosten/index.md
  Energiebedarf/index.md
  Energieerzeugung/index.md
  U_Wert/index.md
  Recyclingquote/index.md
  Abfallvermeidung/index.md

datenqualitaet/
  Belegt/index.md
  Geschaetzt/index.md
  Widerspruechlich/index.md
  Unbekannt/index.md
  Sekundaerquelle/index.md
  Primaerquelle/index.md

zertifizierung_bewertungssystem/
  BREEAM/index.md
  DGNB/index.md
  LEED/index.md
  WELL/index.md
  Paris_Proof/index.md
  Material_Passport/index.md

datenmodell/
  Materialpass/index.md
  Gebaeudepass/index.md
  Bauteilkatalog/index.md
  BIM_Modell/index.md
  Madaster/index.md
  IFC/index.md
  Ontologie/index.md
  Taxonomie/index.md

software_digitaltool/
  TOOL_ID/index.md
  examples:
    Restado/index.md
    RotorDC/index.md
    Madaster/index.md
    Concular/index.md
    BIM/index.md
    One_Click_LCA/index.md

dokumenttyp/
  Plan/index.md
  Bericht/index.md
  Inventar/index.md
  Pruefbericht/index.md
  Ausschreibung/index.md
  Materialpass/index.md
  Fotodokumentation/index.md
  Bauteilkatalog/index.md
  Pre_Demolition_Audit/index.md
```

## 9. Context Knots

```text
programm_kontext/
  Foerderprogramm/index.md
  Wettbewerb/index.md
  Forschungsprojekt/index.md
  Kommunales_Programm/index.md

foerderprogramm/
  PROGRAMM_ID/index.md
  examples:
    BBSM/index.md
    PREUSE/index.md

kontextmerkmal/
  Denkmalschutz/index.md
  Oeffentliche_Beschaffung/index.md
  Sozialer_Wohnbau/index.md
  Genossenschaft/index.md
  Bildungsprojekt/index.md
  Partizipativer_Bauprozess/index.md

wirtschaft/
  Kostenersparnis/index.md
  Mehrkosten/index.md
  Marktverfuegbarkeit/index.md
  Geschaeftsmodell/index.md
  Restwert/index.md
  Rueckbaukosten/index.md
```

## 10. Actor / Tool Supporting Knots

```text
akteurrolle/
  Bauherr_Auftraggeber/index.md
  Architektur/index.md
  Tragwerksplanung/index.md
  Bauausfuehrung/index.md
  Rueckbau_Demontage/index.md
  Materiallieferant/index.md
  Reuse_Beratung/index.md
  Pruefung_Qualitaetssicherung/index.md
  Aufbereitung_Refurbishment/index.md
  Forschung_Dokumentation/index.md
  Nachhaltigkeitsberatung/index.md
  Projektmanagement_Koordination/index.md
  Landschaftsplanung/index.md
  TGA_Gebaeudetechnik/index.md
  Brandschutz_Barrierefreiheit/index.md
  Stahlbau_Fertigung/index.md
  Fassade/index.md
  Kunst_Gestaltung/index.md
  Betreiber_Nutzer/index.md
  Oeffentliche_Hand/index.md
  Projektbeteiligte_Unbestimmt/index.md

tooltyp/
  Bauteilboerse/index.md
  Materialdatenbank/index.md
  Materialpass_Plattform/index.md
  BIM_Tool/index.md
  LCA_Tool/index.md
  GIS_Urban_Mining_Tool/index.md
  Tracking_Tool/index.md
```

## 11. Keep Out Of First Final Version

```text
meta/
akteurleistung/
akteurtyp/
beleg/
gebaeudetypologie/
plattformfunktion/
plattformzugang/
```

Reason: redundant, meta-only, or covered by better final folders.

## 12. Most Important Adaptation From Current Staging

The final schema should not copy every staging knot one-to-one.

Important cleanups:

```text
prozessphase:
  current 9 -> canonical 10

bauteiltyp:
  current 53 -> canonical broad families, raw details kept on reuse_einsatz

huerde:
  current 30 -> keep only semantic barriers, merge duplicates like Haftung/Gewaehrleistung

quelle:
  current 96 -> final 567 source archive nodes, one for every old file

empty ontology folders:
  create as schema folders, but do not create fake data nodes
```
