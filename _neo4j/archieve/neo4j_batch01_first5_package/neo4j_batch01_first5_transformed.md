# Neo4j Transformation Batch 01 — First 5 Buildings

This file is the human-readable migration result for the first uploaded batch. The companion JSON contains the same result as machine-readable nodes and relationships, and the Cypher file can be used as a first import draft.

## Locked migration rules applied
- Fallbeispiel removed; Projekt is central node.
- Bauteilgruppe represents concrete reused component occurrence / group.
- Quelle is source-of-truth node for every source file.
- datenqualitaet is always a property on BELEGT_IN with value Belegt.
- Bewertung kept as scalar Projekt.bewertung.
- Kennwerte stored as scalar properties on Projekt or Bauteilgruppe.
- Stadt, Land, Bauobjektklasse, Bauobjektrolle, Akteurrolle and Akteurtyp are nodes, not properties.
- No unknown/unbekannt placeholder nodes created.
- Non-direct-reuse items such as recycled glass sub-base or new hemp/lime products are not modeled as Bauteilgruppe.

## Output inventory
- Nodes: **306**
- Relationships: **1173**
- `BELEGT_IN` relationships: **440**, always with `datenqualitaet: "Belegt"`
- Validation: non-Quelle nodes with degree < 2: **0**

## Source-of-truth Quelle nodes
- `quelle_55_great_suffolk_street_london_md` (Quelle): **55_Great_Suffolk_Street_London.md**
- `quelle_association_house_groeditz_md` (Quelle): **Association_house_Groeditz.md**
- `quelle_association_house_plauen_md` (Quelle): **Association_house_Plauen.md**
- `quelle_awm_muenster_circular_office_md` (Quelle): **AWM_Muenster_Circular_Office.md**
- `quelle_bedzed_london_hackbridge_md` (Quelle): **BedZED_London_Hackbridge.md**

## 55 Great Suffolk Street

### Projekt node
- `projekt_55_great_suffolk_street` (Projekt): **55 Great Suffolk Street** — bewertung: 4; flaeche_m2: 1412; co2_einsparung_t: 50

### Direct Bauwerk nodes
- `bauwerk_55_great_suffolk_existing_warehouse` (Bauwerk): **Grade II Listed Victorian warehouse, 55 Great Suffolk Street**
- `bauwerk_55_great_suffolk_external_core` (Bauwerk): **Neuer externer Service- und Erschliessungskern**
- `bauwerk_1_broadgate_donor` (Bauwerk): **1 Broadgate donor site**

### Bauteilgruppe nodes
- `btg_55_steel_from_1_broadgate` (Bauteilgruppe): **Wiederverwendete Stahlprofile aus 1 Broadgate** — menge_t: 8.3; reuse_anteil_prozent: 43
  - NUTZT_MATERIAL → Baustahl; HAT_BAUTEILTYP → Traeger; HAT_BAUTEILTYP → Stuetze; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Urban Mining; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Stahlrahmen; HAT_BAUWEISE → Stahlbau; HAT_METHODE → Design follows availability; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_PRUEFUNG → Testing; HAT_PRUEFUNG → CE Marking; … +19 more
- `btg_55_steel_from_cleveland_stock` (Bauteilgruppe): **Wiederverwendete Stahlprofile aus Cleveland Stock** — menge_t: 11.1; reuse_anteil_prozent: 57
  - NUTZT_MATERIAL → Baustahl; HAT_BAUTEILTYP → Traeger; HAT_BAUTEILTYP → Stuetze; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Reuse-Stockholder-Modell; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Stahlrahmen; HAT_BAUWEISE → Stahlbau; HAT_METHODE → Design follows availability; HAT_PROZESSPHASE → Lagerung; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_PRUEFUNG → Testing; HAT_PRUEFUNG → CE Marking; REFERENZIERT_NORM → EN 1090; … +14 more

### Akteur nodes
- `akteur_fabrix` (Akteur): **Fabrix**
- `akteur_hawkins_brown` (Akteur): **Hawkins\Brown**
- `akteur_symmetrys` (Akteur): **Symmetrys**
- `akteur_akt_ii` (Akteur): **AKT II**
- `akteur_cbre` (Akteur): **CBRE**
- `akteur_opera` (Akteur): **Opera**
- `akteur_gardiner_theobald` (Akteur): **Gardiner & Theobald**
- `akteur_cantillon` (Akteur): **Cantillon**
- `akteur_cleveland_steel_and_tubes` (Akteur): **Cleveland Steel and Tubes**

### Main semantic relationships
- `projekt_55_great_suffolk_street` -[:LIEGT_IN_STADT]-> `stadt_london`
- `projekt_55_great_suffolk_street` -[:HAT_STATUS]-> `status_unklar_live`
- `projekt_55_great_suffolk_street` -[:HAT_NUTZUNG]-> `nutzung_arbeitsplatz`
- `projekt_55_great_suffolk_street` -[:HAT_NUTZUNG]-> `nutzung_buero`
- `projekt_55_great_suffolk_street` -[:HAT_NUTZUNG]-> `nutzung_retail`
- `projekt_55_great_suffolk_street` -[:NUTZT_BAUWERK]-> `bauwerk_55_great_suffolk_existing_warehouse`
- `projekt_55_great_suffolk_street` -[:NUTZT_BAUWERK]-> `bauwerk_55_great_suffolk_external_core`
- `projekt_55_great_suffolk_street` -[:NUTZT_BAUWERK]-> `bauwerk_1_broadgate_donor`
- `projekt_55_great_suffolk_street` -[:HAT_BAUTEILGRUPPE]-> `btg_55_steel_from_1_broadgate`
- `projekt_55_great_suffolk_street` -[:HAT_BAUTEILGRUPPE]-> `btg_55_steel_from_cleveland_stock`
- `btg_55_steel_from_1_broadgate` -[:NUTZT_MATERIAL]-> `material_baustahl`
- `btg_55_steel_from_1_broadgate` -[:HAT_BAUTEILTYP]-> `bauteiltyp_traeger`
- `btg_55_steel_from_1_broadgate` -[:HAT_BAUTEILTYP]-> `bauteiltyp_stuetze`
- `btg_55_steel_from_1_broadgate` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_55_steel_from_1_broadgate` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_urban_mining`
- `btg_55_steel_from_1_broadgate` -[:HAT_HUERDE]-> `huerde_profilverfuegbarkeit`
- `btg_55_steel_from_1_broadgate` -[:HAT_HUERDE]-> `huerde_donor_receiver_timing`
- `btg_55_steel_from_1_broadgate` -[:HAT_HUERDE]-> `huerde_zertifizierung`
- `btg_55_steel_from_1_broadgate` -[:HAT_HUERDE]-> `huerde_services_koordination`
- `btg_55_steel_from_1_broadgate` -[:AUS_BAUWERK]-> `bauwerk_1_broadgate_donor`
- `btg_55_steel_from_1_broadgate` -[:EINGEBAUT_IN]-> `bauwerk_55_great_suffolk_external_core`
- `btg_55_steel_from_cleveland_stock` -[:NUTZT_MATERIAL]-> `material_baustahl`
- `btg_55_steel_from_cleveland_stock` -[:HAT_BAUTEILTYP]-> `bauteiltyp_traeger`
- `btg_55_steel_from_cleveland_stock` -[:HAT_BAUTEILTYP]-> `bauteiltyp_stuetze`
- `btg_55_steel_from_cleveland_stock` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_55_steel_from_cleveland_stock` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_reuse_stockholder_modell`
- `btg_55_steel_from_cleveland_stock` -[:HAT_HUERDE]-> `huerde_marktliquiditaet`
- `btg_55_steel_from_cleveland_stock` -[:HAT_HUERDE]-> `huerde_zertifizierung`
- `btg_55_steel_from_cleveland_stock` -[:HAT_HUERDE]-> `huerde_profilverfuegbarkeit`
- `btg_55_steel_from_cleveland_stock` -[:EINGEBAUT_IN]-> `bauwerk_55_great_suffolk_external_core`

### Open issues carried forward
- Bestandserhalt des denkmalgeschützten Lagerhauses nicht als Direct Reuse gezählt; Fertigstellungsstatus öffentlich unklar.
- Missing: final public completion confirmation, exact profile schedule, connection types, detailed fire/corrosion strategy.

## Association house, Gröditz

### Projekt node
- `projekt_association_house_groeditz` (Projekt): **Association house, Gröditz** — bewertung: 4; jahr_fertigstellung: 2007; transportdistanz_km: 2.5

### Direct Bauwerk nodes
- `bauwerk_groeditz_association_house` (Bauwerk): **Sport-/Vereinshaus Gröditz**
- `bauwerk_groeditz_donor_school_dresden_type` (Bauwerk): **Spendergebäude Schule Typ Dresden**
- `bauwerk_groeditz_donor_wbs70` (Bauwerk): **Spendergebäude WBS70**

### Bauteilgruppe nodes
- `btg_groeditz_dresden_type_precast_parts` (Bauteilgruppe): **Betonfertigteile aus Schule Typ Dresden** — anzahl: 279
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Decke; HAT_BAUTEILTYP → Treppe; HAT_BAUTEILTYP → Fassade; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Huelle; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → Dresden-Typ; HAT_METHODE → Bauteilinventar; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; … +17 more
- `btg_groeditz_wbs70_panels` (Bauteilgruppe): **WBS70-Paneele aus weiterem Spendergebäude** — anzahl: 159
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Decke; HAT_BAUTEILTYP → Fassade; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Huelle; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → WBS70; HAT_METHODE → Bauteilinventar; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; … +15 more

### Akteur nodes
- No actor nodes created because the uploaded source does not provide reliable project actors. Literature names were not converted into Akteur nodes.

### Main semantic relationships
- `projekt_association_house_groeditz` -[:LIEGT_IN_STADT]-> `stadt_groeditz`
- `projekt_association_house_groeditz` -[:HAT_STATUS]-> `status_gebaut`
- `projekt_association_house_groeditz` -[:HAT_NUTZUNG]-> `nutzung_sport_verein`
- `projekt_association_house_groeditz` -[:NUTZT_BAUWERK]-> `bauwerk_groeditz_association_house`
- `projekt_association_house_groeditz` -[:NUTZT_BAUWERK]-> `bauwerk_groeditz_donor_school_dresden_type`
- `projekt_association_house_groeditz` -[:NUTZT_BAUWERK]-> `bauwerk_groeditz_donor_wbs70`
- `projekt_association_house_groeditz` -[:HAT_BAUTEILGRUPPE]-> `btg_groeditz_dresden_type_precast_parts`
- `projekt_association_house_groeditz` -[:HAT_BAUTEILGRUPPE]-> `btg_groeditz_wbs70_panels`
- `btg_groeditz_dresden_type_precast_parts` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_BAUTEILTYP]-> `bauteiltyp_decke`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_BAUTEILTYP]-> `bauteiltyp_treppe`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_BAUTEILTYP]-> `bauteiltyp_fassade`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_HUERDE]-> `huerde_systemmix`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_HUERDE]-> `huerde_hoehenausgleich`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_groeditz_dresden_type_precast_parts` -[:HAT_HUERDE]-> `huerde_tragwerksnachweis`
- `btg_groeditz_dresden_type_precast_parts` -[:AUS_BAUWERK]-> `bauwerk_groeditz_donor_school_dresden_type`
- `btg_groeditz_dresden_type_precast_parts` -[:EINGEBAUT_IN]-> `bauwerk_groeditz_association_house`
- `btg_groeditz_wbs70_panels` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_groeditz_wbs70_panels` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_groeditz_wbs70_panels` -[:HAT_BAUTEILTYP]-> `bauteiltyp_decke`
- `btg_groeditz_wbs70_panels` -[:HAT_BAUTEILTYP]-> `bauteiltyp_fassade`
- `btg_groeditz_wbs70_panels` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_groeditz_wbs70_panels` -[:HAT_HUERDE]-> `huerde_systemmix`
- `btg_groeditz_wbs70_panels` -[:HAT_HUERDE]-> `huerde_hoehenausgleich`
- `btg_groeditz_wbs70_panels` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_groeditz_wbs70_panels` -[:HAT_HUERDE]-> `huerde_logistik_schwerer_bauteile`
- `btg_groeditz_wbs70_panels` -[:AUS_BAUWERK]-> `bauwerk_groeditz_donor_wbs70`
- `btg_groeditz_wbs70_panels` -[:EINGEBAUT_IN]-> `bauwerk_groeditz_association_house`

### Open issues carried forward
- Architekt, Tragwerksplaner und Bauherr öffentlich nicht belastbar gefunden.
- Missing: public primary design team data, detailed connection drawings, structural proofs, cost/CO₂ data.

## Association house, Plauen

### Projekt node
- `projekt_association_house_plauen` (Projekt): **Association house, Plauen** — bewertung: 4; jahr_fertigstellung: 2007; transportdistanz_km: 7

### Direct Bauwerk nodes
- `bauwerk_plauen_association_house` (Bauwerk): **Sport-/Vereinshaus Plauen**
- `bauwerk_plauen_donor_iw73_6` (Bauwerk): **Spendergebäude IW73/6-Wohnungsbau**

### Bauteilgruppe nodes
- `btg_plauen_floor_ceiling_slabs` (Bauteilgruppe): **Decken-/Bodenplatten IW73/6** — anzahl: 145
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Decke; HAT_BAUTEILTYP → Boden; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → IW73/6; HAT_METHODE → Bauteilidentifikation; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Tragfaehigkeit; … +11 more
- `btg_plauen_exterior_wall_elements` (Bauteilgruppe): **Außenwandelemente IW73/6** — anzahl: 19
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Fassade; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Huelle; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → IW73/6; HAT_METHODE → Bauteilidentifikation; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; … +14 more
- `btg_plauen_interior_wall_elements` (Bauteilgruppe): **Innenwandelemente IW73/6** — anzahl: 14
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Wand; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → IW73/6; HAT_METHODE → Bauteilidentifikation; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Tragfaehigkeit; HAT_LEISTUNGSANFORDERUNG → Schallschutz; … +10 more
- `btg_plauen_basement_wall_elements` (Bauteilgruppe): **Kellerwandelemente IW73/6** — anzahl: 11
  - NUTZT_MATERIAL → Stahlbetonfertigteil; HAT_BAUTEILTYP → Wand; HAT_BAUTEILEBENE → Tragwerk; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Fertigteil-Wand-Deckensystem; HAT_BAUWEISE → Betonfertigteilbau; HAT_BAUSYSTEM → IW73/6; HAT_METHODE → Bauteilidentifikation; HAT_METHODE → Bauteilgerechte Planung; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Tragfaehigkeit; HAT_LEISTUNGSANFORDERUNG → Feuchteschutz; … +11 more

### Akteur nodes
- No actor nodes created because the uploaded source does not provide reliable project actors. Literature names were not converted into Akteur nodes.

### Main semantic relationships
- `projekt_association_house_plauen` -[:LIEGT_IN_STADT]-> `stadt_plauen`
- `projekt_association_house_plauen` -[:HAT_STATUS]-> `status_gebaut`
- `projekt_association_house_plauen` -[:HAT_NUTZUNG]-> `nutzung_sport_verein`
- `projekt_association_house_plauen` -[:NUTZT_BAUWERK]-> `bauwerk_plauen_association_house`
- `projekt_association_house_plauen` -[:NUTZT_BAUWERK]-> `bauwerk_plauen_donor_iw73_6`
- `projekt_association_house_plauen` -[:HAT_BAUTEILGRUPPE]-> `btg_plauen_floor_ceiling_slabs`
- `projekt_association_house_plauen` -[:HAT_BAUTEILGRUPPE]-> `btg_plauen_exterior_wall_elements`
- `projekt_association_house_plauen` -[:HAT_BAUTEILGRUPPE]-> `btg_plauen_interior_wall_elements`
- `projekt_association_house_plauen` -[:HAT_BAUTEILGRUPPE]-> `btg_plauen_basement_wall_elements`
- `btg_plauen_floor_ceiling_slabs` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_BAUTEILTYP]-> `bauteiltyp_decke`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_BAUTEILTYP]-> `bauteiltyp_boden`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_HUERDE]-> `huerde_bauteilgeometrie_rasterbindung`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_HUERDE]-> `huerde_nachweisfaehigkeit`
- `btg_plauen_floor_ceiling_slabs` -[:HAT_HUERDE]-> `huerde_fehlende_primaerdaten`
- `btg_plauen_floor_ceiling_slabs` -[:AUS_BAUWERK]-> `bauwerk_plauen_donor_iw73_6`
- `btg_plauen_floor_ceiling_slabs` -[:EINGEBAUT_IN]-> `bauwerk_plauen_association_house`
- `btg_plauen_exterior_wall_elements` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_plauen_exterior_wall_elements` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_plauen_exterior_wall_elements` -[:HAT_BAUTEILTYP]-> `bauteiltyp_fassade`
- `btg_plauen_exterior_wall_elements` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_plauen_exterior_wall_elements` -[:HAT_HUERDE]-> `huerde_bauteilgeometrie_rasterbindung`
- `btg_plauen_exterior_wall_elements` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_plauen_exterior_wall_elements` -[:HAT_HUERDE]-> `huerde_nachweisfaehigkeit`
- `btg_plauen_exterior_wall_elements` -[:HAT_HUERDE]-> `huerde_fehlende_primaerdaten`
- `btg_plauen_exterior_wall_elements` -[:HAT_HUERDE]-> `huerde_waermebruecken`
- `btg_plauen_exterior_wall_elements` -[:AUS_BAUWERK]-> `bauwerk_plauen_donor_iw73_6`
- `btg_plauen_exterior_wall_elements` -[:EINGEBAUT_IN]-> `bauwerk_plauen_association_house`
- `btg_plauen_interior_wall_elements` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_plauen_interior_wall_elements` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_plauen_interior_wall_elements` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_plauen_interior_wall_elements` -[:HAT_HUERDE]-> `huerde_bauteilgeometrie_rasterbindung`
- `btg_plauen_interior_wall_elements` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_plauen_interior_wall_elements` -[:HAT_HUERDE]-> `huerde_nachweisfaehigkeit`
- `btg_plauen_interior_wall_elements` -[:HAT_HUERDE]-> `huerde_fehlende_primaerdaten`
- `btg_plauen_interior_wall_elements` -[:AUS_BAUWERK]-> `bauwerk_plauen_donor_iw73_6`
- `btg_plauen_interior_wall_elements` -[:EINGEBAUT_IN]-> `bauwerk_plauen_association_house`
- `btg_plauen_basement_wall_elements` -[:NUTZT_MATERIAL]-> `material_stahlbetonfertigteil`
- `btg_plauen_basement_wall_elements` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_plauen_basement_wall_elements` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_plauen_basement_wall_elements` -[:HAT_HUERDE]-> `huerde_bauteilgeometrie_rasterbindung`
- `btg_plauen_basement_wall_elements` -[:HAT_HUERDE]-> `huerde_anschlussdetails`
- `btg_plauen_basement_wall_elements` -[:HAT_HUERDE]-> `huerde_nachweisfaehigkeit`
- `btg_plauen_basement_wall_elements` -[:HAT_HUERDE]-> `huerde_fehlende_primaerdaten`
- `btg_plauen_basement_wall_elements` -[:HAT_HUERDE]-> `huerde_feuchteschutz`
- `btg_plauen_basement_wall_elements` -[:AUS_BAUWERK]-> `bauwerk_plauen_donor_iw73_6`
- `btg_plauen_basement_wall_elements` -[:EINGEBAUT_IN]-> `bauwerk_plauen_association_house`

### Open issues carried forward
- Architekt, Tragwerksplaner und Bauherr öffentlich nicht belastbar gefunden; Prüfberichte nicht öffentlich gefunden.
- Missing: public primary design team data, detailed connection drawings, structural proofs, cost/CO₂ data.

## AWM Münster, zirkulärer Büroausbau 3. OG

### Projekt node
- `projekt_awm_muenster_circular_office` (Projekt): **AWM Münster, zirkulärer Büroausbau 3. OG** — bewertung: 2; flaeche_m2: 250; jahr_fertigstellung: 2023; co2_einsparung_t: 13.32

### Direct Bauwerk nodes
- `bauwerk_awm_muenster_3og` (Bauwerk): **AWM Verwaltungsgebäude, 3. Obergeschoss Rösnerstraße**

### Bauteilgruppe nodes
- `btg_awm_glass_partitions_doors` (Bauteilgruppe): **Glastrennwände und Türen aus Behrensbau Düsseldorf** — co2_einsparung_t: 4.39
  - NUTZT_MATERIAL → Glas; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Tuer; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → ReUse first; HAT_METHODE → Design follows availability; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_PROZESSPHASE → Monitoring; HAT_LEISTUNGSANFORDERUNG → Brandschutz; HAT_LEISTUNGSANFORDERUNG → Schallschutz; … +8 more
- `btg_awm_wc_partitions` (Bauteilgruppe): **Reuse-WC-Trennwände aus Behrensbau Düsseldorf**
  - NUTZT_MATERIAL → Mischmaterial Innenausbau; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → ReUse first; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Hygiene; HAT_LEISTUNGSANFORDERUNG → Feuchteschutz; HAT_LEISTUNGSANFORDERUNG → Stabilitaet; HAT_HUERDE → Passung Zustand; HAT_HUERDE → Hygiene Feuchte; HAT_BESCHAFFUNGSWEG → Concular Materialplattform; … +2 more
- `btg_awm_cable_trays_shelves` (Bauteilgruppe): **Kabeltrassen als Regale**
  - NUTZT_MATERIAL → Metall; HAT_BAUTEILTYP → Technik; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Technische_Ausstattung; HAT_WIEDERVERWENDUNGSART → Funktionswechsel; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → Upcycling; HAT_METHODE → Design follows availability; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Tragfaehigkeit; HAT_HUERDE → Neue Lastfunktion; HAT_HUERDE → Interior Grenzfall; HAT_AUFBEREITUNG → Umnutzung; HAT_AUFBEREITUNG → 3D-gedruckte Halterungen; … +2 more
- `btg_awm_cable_trays_led_lighting` (Bauteilgruppe): **Kabeltrassen und ReUse-LED-Leuchten als Allgemeinbeleuchtung**
  - NUTZT_MATERIAL → Metall; HAT_BAUTEILTYP → Technik; HAT_BAUTEILEBENE → Technische_Ausstattung; HAT_BAUTEILEBENE → Innenausbau; HAT_WIEDERVERWENDUNGSART → Funktionswechsel; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → Reaktivierung; HAT_METHODE → Aufputzführung; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Elektrosicherheit; HAT_LEISTUNGSANFORDERUNG → Wartbarkeit; HAT_HUERDE → Elektrosicherheit TGA; HAT_HUERDE → Technische Reaktivierung; HAT_AUFBEREITUNG → Reaktivierung; HAT_AUFBEREITUNG → Montage; … +1 more
- `btg_awm_chair_parts_wall_cladding` (Bauteilgruppe): **Wandverkleidung aus alten Schul- und Theaterstühlen**
  - NUTZT_MATERIAL → Holz; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Funktionswechsel; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → Upcycling; HAT_METHODE → Spuren als Gestaltung; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Brandschutz; HAT_LEISTUNGSANFORDERUNG → Oberflaeche; HAT_HUERDE → Interior Grenzfall; HAT_HUERDE → Brandschutz nicht oeffentlich; HAT_HUERDE → Akzeptanz Gebrauchsspuren; … +4 more
- `btg_awm_reused_wood_built_ins` (Bauteilgruppe): **Wiederverwendetes Holz für feste Einbauten**
  - NUTZT_MATERIAL → Holz; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Fester Innenausbau; HAT_STATUS → Eingebaut; HAT_METHODE → ReUse first; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Stabilitaet; HAT_LEISTUNGSANFORDERUNG → Hygiene; HAT_HUERDE → Herkunft Sortierung; HAT_HUERDE → Passung Zustand; HAT_AUFBEREITUNG → Rueckbau; HAT_AUFBEREITUNG → Zuschnitt; HAT_AUFBEREITUNG → Tischlerische Aufbereitung; … +3 more

### Akteur nodes
- `akteur_awm_muenster` (Akteur): **Abfallwirtschaftsbetriebe Münster**
- `akteur_urselmann_interior` (Akteur): **urselmann interior**
- `akteur_concular` (Akteur): **Concular**
- `akteur_petra_jablonicka` (Akteur): **Petra Jablonická**
- `akteur_sven_urselmann` (Akteur): **Sven Urselmann**

### Main semantic relationships
- `projekt_awm_muenster_circular_office` -[:LIEGT_IN_STADT]-> `stadt_muenster`
- `projekt_awm_muenster_circular_office` -[:HAT_STATUS]-> `status_gebaut`
- `projekt_awm_muenster_circular_office` -[:HAT_NUTZUNG]-> `nutzung_verwaltung`
- `projekt_awm_muenster_circular_office` -[:HAT_NUTZUNG]-> `nutzung_buero`
- `projekt_awm_muenster_circular_office` -[:HAT_NUTZUNG]-> `nutzung_workshop`
- `projekt_awm_muenster_circular_office` -[:HAT_NUTZUNG]-> `nutzung_besprechung`
- `projekt_awm_muenster_circular_office` -[:HAT_NUTZUNG]-> `nutzung_kueche`
- `projekt_awm_muenster_circular_office` -[:NUTZT_BAUWERK]-> `bauwerk_awm_muenster_3og`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_glass_partitions_doors`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_wc_partitions`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_cable_trays_shelves`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_cable_trays_led_lighting`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_chair_parts_wall_cladding`
- `projekt_awm_muenster_circular_office` -[:HAT_BAUTEILGRUPPE]-> `btg_awm_reused_wood_built_ins`
- `btg_awm_glass_partitions_doors` -[:NUTZT_MATERIAL]-> `material_glas`
- `btg_awm_glass_partitions_doors` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_awm_glass_partitions_doors` -[:HAT_BAUTEILTYP]-> `bauteiltyp_tuer`
- `btg_awm_glass_partitions_doors` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_awm_glass_partitions_doors` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_awm_glass_partitions_doors` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_glass_partitions_doors` -[:HAT_HUERDE]-> `huerde_passung_zustand`
- `btg_awm_glass_partitions_doors` -[:HAT_HUERDE]-> `huerde_brandschutz_nicht_oeffentlich`
- `btg_awm_glass_partitions_doors` -[:HAT_HUERDE]-> `huerde_interior_grenzfall`
- `btg_awm_glass_partitions_doors` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`
- `btg_awm_wc_partitions` -[:NUTZT_MATERIAL]-> `material_mischmaterial_innenausbau`
- `btg_awm_wc_partitions` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_awm_wc_partitions` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_awm_wc_partitions` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_awm_wc_partitions` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_wc_partitions` -[:HAT_HUERDE]-> `huerde_passung_zustand`
- `btg_awm_wc_partitions` -[:HAT_HUERDE]-> `huerde_hygiene_feuchte`
- `btg_awm_wc_partitions` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`
- `btg_awm_cable_trays_shelves` -[:NUTZT_MATERIAL]-> `material_metall`
- `btg_awm_cable_trays_shelves` -[:HAT_BAUTEILTYP]-> `bauteiltyp_technik`
- `btg_awm_cable_trays_shelves` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_awm_cable_trays_shelves` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_funktionswechsel`
- `btg_awm_cable_trays_shelves` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_cable_trays_shelves` -[:HAT_HUERDE]-> `huerde_neue_lastfunktion`
- `btg_awm_cable_trays_shelves` -[:HAT_HUERDE]-> `huerde_interior_grenzfall`
- `btg_awm_cable_trays_shelves` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`
- `btg_awm_cable_trays_led_lighting` -[:NUTZT_MATERIAL]-> `material_metall`
- `btg_awm_cable_trays_led_lighting` -[:HAT_BAUTEILTYP]-> `bauteiltyp_technik`
- `btg_awm_cable_trays_led_lighting` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_funktionswechsel`
- `btg_awm_cable_trays_led_lighting` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_cable_trays_led_lighting` -[:HAT_HUERDE]-> `huerde_elektrosicherheit_tga`
- `btg_awm_cable_trays_led_lighting` -[:HAT_HUERDE]-> `huerde_technische_reaktivierung`
- `btg_awm_cable_trays_led_lighting` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`
- `btg_awm_chair_parts_wall_cladding` -[:NUTZT_MATERIAL]-> `material_holz`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_funktionswechsel`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_HUERDE]-> `huerde_interior_grenzfall`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_HUERDE]-> `huerde_brandschutz_nicht_oeffentlich`
- `btg_awm_chair_parts_wall_cladding` -[:HAT_HUERDE]-> `huerde_akzeptanz_gebrauchsspuren`
- `btg_awm_chair_parts_wall_cladding` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`
- `btg_awm_reused_wood_built_ins` -[:NUTZT_MATERIAL]-> `material_holz`
- `btg_awm_reused_wood_built_ins` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_awm_reused_wood_built_ins` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_awm_reused_wood_built_ins` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_fester_innenausbau`
- `btg_awm_reused_wood_built_ins` -[:HAT_HUERDE]-> `huerde_herkunft_sortierung`
- `btg_awm_reused_wood_built_ins` -[:HAT_HUERDE]-> `huerde_passung_zustand`
- `btg_awm_reused_wood_built_ins` -[:EINGEBAUT_IN]-> `bauwerk_awm_muenster_3og`

### Open issues carried forward
- Vergleichsfall/Anhang: kleiner Innenausbau; lose Möbel und Bestandserhalt nicht als Direct Reuse gezählt.
- Missing: exact quantities per component, glass/electrical test records, detailed LCA method and fire-safety documentation.

## BedZED / Beddington Zero Energy Development

### Projekt node
- `projekt_bedzed` (Projekt): **BedZED / Beddington Zero Energy Development** — bewertung: 5; jahr_fertigstellung: 2002

### Direct Bauwerk nodes
- `bauwerk_bedzed_quarter` (Bauwerk): **BedZED Wohn- und Arbeitsquartier**

### Bauteilgruppe nodes
- `btg_bedzed_reclaimed_structural_steel` (Bauteilgruppe): **Wiederverwendete Stahlprofile / Stahlrahmen** — menge_t: 98; reuse_anteil_prozent: 95
  - NUTZT_MATERIAL → Baustahl; HAT_BAUTEILTYP → Traeger; HAT_BAUTEILTYP → Stuetze; HAT_BAUTEILEBENE → Tragwerk; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_WIEDERVERWENDUNGSART → Urban Mining; HAT_STATUS → Eingebaut; HAT_TRAGWERKSPRINZIP → Stahlrahmen; HAT_BAUWEISE → Stahlbau; HAT_METHODE → Flexible Querschnittsspezifikation; HAT_METHODE → Design follows availability; HAT_PROZESSPHASE → Bestandsaufnahme; HAT_PROZESSPHASE → Bauteilinventar; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Lagerung; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Planung; … +29 more
- `btg_bedzed_softwood_wall_studs` (Bauteilgruppe): **Wiederverwendete Holzständer / softwood walling studs**
  - NUTZT_MATERIAL → Holz; HAT_BAUTEILTYP → Wand; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_METHODE → Lokale Beschaffung; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Wandaufbau; HAT_LEISTUNGSANFORDERUNG → Innenausbau; HAT_HUERDE → Aufbereitung Zuschnitt; HAT_HUERDE → Lieferkettenkoordination; HAT_AUFBEREITUNG → Instandsetzung; HAT_AUFBEREITUNG → Behandlung; HAT_AUFBEREITUNG → Zuschnitt im Saegewerk; … +1 more
- `btg_bedzed_scaffold_tube_railings` (Bauteilgruppe): **Gerüstrohre als Geländer/Balustraden**
  - NUTZT_MATERIAL → Baustahl; HAT_BAUTEILTYP → Gelaender; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Aussenraum; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Funktionswechsel; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_METHODE → Lokale Beschaffung; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Aufbereitung; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Absturzsicherung; HAT_LEISTUNGSANFORDERUNG → Dauerhaftigkeit; HAT_HUERDE → Nachweisfaehigkeit; HAT_HUERDE → Passung Zustand; EINGEBAUT_IN → BedZED Wohn- und Arbeitsquartier
- `btg_bedzed_reclaimed_doors` (Bauteilgruppe): **Wiederverwendete Türen**
  - NUTZT_MATERIAL → Holz; HAT_BAUTEILTYP → Tuer; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Innenausbau; HAT_BAUTEILEBENE → Raumstruktur; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_METHODE → Lokale Beschaffung; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Nutzbarkeit; HAT_LEISTUNGSANFORDERUNG → Brandschutz; HAT_HUERDE → Komplexe Lieferketten Türen; HAT_HUERDE → Brandschutz nicht oeffentlich; EINGEBAUT_IN → BedZED Wohn- und Arbeitsquartier
- `btg_bedzed_reclaimed_kerbs_paving` (Bauteilgruppe): **Wiederverwendete Bordsteine und Natursteinplatten**
  - NUTZT_MATERIAL → Naturstein_Betonstein; HAT_BAUTEILTYP → Boden; HAT_BAUTEILTYP → Ausbau; HAT_BAUTEILEBENE → Aussenraum; HAT_WIEDERVERWENDUNGSART → Ex-situ Bauteilwiederverwendung; HAT_STATUS → Eingebaut; HAT_METHODE → Lokale Beschaffung; HAT_PROZESSPHASE → Rueckbau; HAT_PROZESSPHASE → Transport; HAT_PROZESSPHASE → Wiedereinbau; HAT_LEISTUNGSANFORDERUNG → Rutschfestigkeit; HAT_LEISTUNGSANFORDERUNG → Frostbestaendigkeit; HAT_LEISTUNGSANFORDERUNG → Aussenraumtauglichkeit; HAT_HUERDE → Komplexe Lieferketten Pflaster; HAT_HUERDE → Reuse Recycling Abgrenzung; EINGEBAUT_IN → BedZED Wohn- und Arbeitsquartier

### Akteur nodes
- `akteur_peabody_trust` (Akteur): **Peabody Trust**
- `akteur_bill_dunster_zedfactory` (Akteur): **Bill Dunster / ZEDfactory**
- `akteur_bioregional` (Akteur): **BioRegional**
- `akteur_arup` (Akteur): **Arup**
- `akteur_ellis_moore` (Akteur): **Ellis & Moore Consulting Engineers**
- `akteur_gardiner_theobald_bedzed` (Akteur): **Gardiner & Theobald**

### Main semantic relationships
- `projekt_bedzed` -[:LIEGT_IN_STADT]-> `stadt_london`
- `projekt_bedzed` -[:HAT_STATUS]-> `status_gebaut`
- `projekt_bedzed` -[:HAT_NUTZUNG]-> `nutzung_wohnen`
- `projekt_bedzed` -[:HAT_NUTZUNG]-> `nutzung_arbeiten`
- `projekt_bedzed` -[:HAT_NUTZUNG]-> `nutzung_gemeinschaftsnutzung`
- `projekt_bedzed` -[:NUTZT_BAUWERK]-> `bauwerk_bedzed_quarter`
- `projekt_bedzed` -[:HAT_BAUTEILGRUPPE]-> `btg_bedzed_reclaimed_structural_steel`
- `projekt_bedzed` -[:HAT_BAUTEILGRUPPE]-> `btg_bedzed_softwood_wall_studs`
- `projekt_bedzed` -[:HAT_BAUTEILGRUPPE]-> `btg_bedzed_scaffold_tube_railings`
- `projekt_bedzed` -[:HAT_BAUTEILGRUPPE]-> `btg_bedzed_reclaimed_doors`
- `projekt_bedzed` -[:HAT_BAUTEILGRUPPE]-> `btg_bedzed_reclaimed_kerbs_paving`
- `btg_bedzed_reclaimed_structural_steel` -[:NUTZT_MATERIAL]-> `material_baustahl`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_BAUTEILTYP]-> `bauteiltyp_traeger`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_BAUTEILTYP]-> `bauteiltyp_stuetze`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_urban_mining`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_HUERDE]-> `huerde_passende_stahlprofile_schwer_verfuegbar`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_HUERDE]-> `huerde_qualitaetsnachweis_historischer_profile`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_HUERDE]-> `huerde_zusatzaufbereitung`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_HUERDE]-> `huerde_gebogene_profile_nicht_reused`
- `btg_bedzed_reclaimed_structural_steel` -[:HAT_HUERDE]-> `huerde_lagerbedarf`
- `btg_bedzed_reclaimed_structural_steel` -[:EINGEBAUT_IN]-> `bauwerk_bedzed_quarter`
- `btg_bedzed_softwood_wall_studs` -[:NUTZT_MATERIAL]-> `material_holz`
- `btg_bedzed_softwood_wall_studs` -[:HAT_BAUTEILTYP]-> `bauteiltyp_wand`
- `btg_bedzed_softwood_wall_studs` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_bedzed_softwood_wall_studs` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_bedzed_softwood_wall_studs` -[:HAT_HUERDE]-> `huerde_aufbereitung_zuschnitt`
- `btg_bedzed_softwood_wall_studs` -[:HAT_HUERDE]-> `huerde_lieferkettenkoordination`
- `btg_bedzed_softwood_wall_studs` -[:EINGEBAUT_IN]-> `bauwerk_bedzed_quarter`
- `btg_bedzed_scaffold_tube_railings` -[:NUTZT_MATERIAL]-> `material_baustahl`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_BAUTEILTYP]-> `bauteiltyp_gelaender`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_funktionswechsel`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_HUERDE]-> `huerde_nachweisfaehigkeit`
- `btg_bedzed_scaffold_tube_railings` -[:HAT_HUERDE]-> `huerde_passung_zustand`
- `btg_bedzed_scaffold_tube_railings` -[:EINGEBAUT_IN]-> `bauwerk_bedzed_quarter`
- `btg_bedzed_reclaimed_doors` -[:NUTZT_MATERIAL]-> `material_holz`
- `btg_bedzed_reclaimed_doors` -[:HAT_BAUTEILTYP]-> `bauteiltyp_tuer`
- `btg_bedzed_reclaimed_doors` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_bedzed_reclaimed_doors` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_bedzed_reclaimed_doors` -[:HAT_HUERDE]-> `huerde_komplexe_lieferketten_turen`
- `btg_bedzed_reclaimed_doors` -[:HAT_HUERDE]-> `huerde_brandschutz_nicht_oeffentlich`
- `btg_bedzed_reclaimed_doors` -[:EINGEBAUT_IN]-> `bauwerk_bedzed_quarter`
- `btg_bedzed_reclaimed_kerbs_paving` -[:NUTZT_MATERIAL]-> `material_naturstein_betonstein`
- `btg_bedzed_reclaimed_kerbs_paving` -[:HAT_BAUTEILTYP]-> `bauteiltyp_boden`
- `btg_bedzed_reclaimed_kerbs_paving` -[:HAT_BAUTEILTYP]-> `bauteiltyp_ausbau`
- `btg_bedzed_reclaimed_kerbs_paving` -[:HAT_WIEDERVERWENDUNGSART]-> `wiederverwendungsart_ex_situ_bauteilwiederverwendung`
- `btg_bedzed_reclaimed_kerbs_paving` -[:HAT_HUERDE]-> `huerde_komplexe_lieferketten_pflaster`
- `btg_bedzed_reclaimed_kerbs_paving` -[:HAT_HUERDE]-> `huerde_reuse_recycling_abgrenzung`
- `btg_bedzed_reclaimed_kerbs_paving` -[:EINGEBAUT_IN]-> `bauwerk_bedzed_quarter`

### Open issues carried forward
- Bewertung fokussiert Direct Reuse, nicht allgemeine Energie-/Recyclingstrategie.
- Missing: exact donor building per profile, detailed fire/acoustic proofs, warranty contract details and long-term monitoring data.

## Relationship type counts
- `AUS_BAUWERK`: 7
- `BELEGT_IN`: 440
- `BETEILIGT_AN`: 20
- `EINGEBAUT_IN`: 19
- `HAT_AKTEURROLLE`: 36
- `HAT_AKTEURTYP`: 25
- `HAT_AUFBEREITUNG`: 28
- `HAT_BAUOBJEKTKLASSE`: 10
- `HAT_BAUOBJEKTROLLE`: 12
- `HAT_BAUSYSTEM`: 6
- `HAT_BAUTEILEBENE`: 38
- `HAT_BAUTEILGRUPPE`: 19
- `HAT_BAUTEILTYP`: 38
- `HAT_BAUWEISE`: 9
- `HAT_BESCHAFFUNGSWEG`: 6
- `HAT_HUERDE`: 60
- `HAT_HUERDEKATEGORIE`: 34
- `HAT_LEISTUNGSANFORDERUNG`: 53
- `HAT_LOGISTIK`: 12
- `HAT_MATERIALGRUPPE`: 7
- `HAT_METHODE`: 30
- `HAT_NUTZUNG`: 28
- `HAT_PROZESSPHASE`: 81
- `HAT_PRUEFUNG`: 8
- `HAT_RESSOURCENQUELLE`: 8
- `HAT_RUECKBAUVERFAHREN`: 14
- `HAT_STATUS`: 34
- `HAT_TRAGWERKSPRINZIP`: 9
- `HAT_VERBINDUNGSTECHNIK`: 2
- `HAT_WIEDERVERWENDUNGSART`: 29
- `LIEGT_IN_LAND`: 4
- `LIEGT_IN_STADT`: 15
- `NUTZT_BAUWERK`: 10
- `NUTZT_MATERIAL`: 19
- `REFERENZIERT_NORM`: 3

## Validation checklist
- [x] No `Fallbeispiel` node.
- [x] No placeholder node named `unbekannt`.
- [x] `Bewertung` stored only as scalar property on `Projekt`.
- [x] `datenqualitaet` appears only on `BELEGT_IN` relationships and is always `Belegt`.
- [x] `Stadt`, `Land`, `Bauobjektklasse`, `Bauobjektrolle`, `Akteurrolle`, `Akteurtyp`, `Bauteiltyp`, `Materialgruppe`, and `HuerdeKategorie` are nodes.
- [x] Kennwerte are properties on `Projekt` or `Bauteilgruppe`, not separate `Kennwert` nodes.
- [x] Non-direct-reuse/recycling-only elements are excluded from `Bauteilgruppe`, but can be added later as separate circular-material layer if needed.
- [x] No non-Quelle node has degree below 2 in the generated graph.