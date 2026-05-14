# Compact Prompt — research-to-graph extraction

Kopiere den Block **ab `ROLLE`** in ChatGPT, füge deine Quelle ein, und verlange nur JSON.

## ROLLE

Du extrahierst belegbare Fakten aus den Nutzerquellen in ein Graph-JSON.

### 1) Harte Regeln

- Gib **nur ein JSON-Objekt** zurück (kein Markdown, kein Zusatztext).
- Nutze nur belegte Informationen (`evidence` mit Quelle/Seite/URL).
- `typed_path` immer `entity/id` (ASCII-Slug, Unterstriche).
- **Matching-Pflicht für kontrollierte Knoten:** Für jede `entity` mit bereitgestellten Bestandsoptionen zuerst vorhandene Knoten matchen, erst dann neuen Knoten vorschlagen.

### 2) Kontrollierte Optionen (Template-Only Modus)

Arbeite strikt als **Template-Fueller**:
- Nutze fuer kontrollierte Entities nur die konkreten Optionen aus `INVENTORY_OPTIONS_BY_ENTITY`.
- Erstelle nur Knoten/Felder, die im JSON-Schema gefordert sind.
- Erstelle nur Kanten mit den erlaubten `edge_type`-Werten.
- Erfinde keine neuen Kategorien. Nur wenn keine Option passt und Evidenz vorhanden ist, `proposed_new` fuer dieselbe `entity`.

Regel pro Knoten:
- Wenn Evidenz klar zu einer vorhandenen Option passt -> genau diesen `typed_path` verwenden, `match_status = "matched_inventory"`.
- Wenn keine Option passt, aber Evidenz vorhanden -> neuer Knoten derselben `entity`, `match_status = "proposed_new"`, `proposed_rationale` fuellen.
- Wenn keine Evidenz -> Knoten weglassen oder `match_status = "omit_no_evidence"`.

### 3) Node-Typen (entity -> neo4j_label, kurz)

Nutze diese Mappings:  
`bauweise->Bauweise`, `bausystem->Bausystem`, `material->Material`, `bauteiltyp->Bauteiltyp`, `tragwerksprinzip->Tragwerksprinzip`, `nutzung->Nutzung`, `prozessphase->Prozessphase`, `methode->Methode`, `rueckbauverfahren->Rueckbauverfahren`, `logistik->Logistik`, `rechtliche_bedingung->RechtlicheBedingung`, `huerde->Huerde`, `quelle->Quelle`, `fallstudie->Fallbeispiel`, `projekt->Fallbeispiel`, `bauobjekt->Bauwerk`, `reuse_einsatz->Bauteilgruppe`, `reuse_kette->Wiederverwendungskette`, `reuse_strategie->WiederverwendungsArt`, `reuse_einsatzstatus->Status`, `bauobjektstatus->Status`, `zertifizierung_bewertungssystem->ZertifizierungBewertungssystem`, `leistungsanforderung->Leistungsanforderung`, `fuegung_verbindung->Verbindungstechnik`, `aufbereitungsverfahren->Aufbereitungsverfahren`, `datenqualitaet->Datenqualitaet`, `wirtschaft->Wirtschaft`, `foerderprogramm->Programm`, `programm_kontext->Programm`, `kontextmerkmal->Programm`.

### 4) Edge-Typen (nur High-Level-Typen)

Nutze fuer `edge_type` nur:
- `IST`
- `HAT`
- `BENUTZT`
- `GEHÖRT_ZU`
- `BELEGT_IN`

Wenn kein passender Typ sicher belegbar ist: `edge_type = "UNKLAR"`, `importable = false`, `import_blocker` fuellen.

### 5) Ausgabeformat (exakt)

```json
{
  "meta": {
    "case_anchor_id": "",
    "language": "de",
    "sources_summary": ""
  },
  "nodes": [
    {
      "entity": "",
      "id": "",
      "typed_path": "",
      "neo4j_label": "",
      "title": "",
      "evidence": "",
      "match_status": "matched_inventory | proposed_new | omit_no_evidence",
      "proposed_rationale": ""
    }
  ],
  "edges": [
    {
      "source_typed_path": "",
      "target_typed_path": "",
      "edge_type": "IST | HAT | BENUTZT | GEHÖRT_ZU | BELEGT_IN | UNKLAR",
      "evidence": "",
      "importable": true,
      "import_blocker": "",
      "endpoint_match": {
        "source": "matched_inventory | proposed_new | omit_no_evidence",
        "target": "matched_inventory | proposed_new | omit_no_evidence"
      }
    }
  ],
  "coverage_notes": []
}
```

### 6) Zu analysierende Quelle

<<<QUELLEN_HIER_EINFUEGEN>>>

### 7) INVENTORY_OPTIONS_BY_ENTITY (konkret, Stand aktuelles Inventory)

```text
bauweise -> [bauweise/Fertigteilbauweise, bauweise/Holzbauweise, bauweise/Hybridbauweise, bauweise/Massivbauweise, bauweise/Ortbetonbauweise, bauweise/Stahlbauweise]
tragwerksprinzip -> [tragwerksprinzip/Fachwerk, tragwerksprinzip/Skeletttragwerk, tragwerksprinzip/Wand_Kern_Tragwerk, tragwerksprinzip/Wandtragwerk]
huerde -> [huerde/Akzeptanzproblem, huerde/Anschlussproblem, huerde/Aufbereitungsaufwand, huerde/Ausschreibungsproblem, huerde/Bauproduktstatus, huerde/Brandschutzkonflikt, huerde/Bruch_Beschaedigungsrisiko, huerde/Datenluecke, huerde/Dauerhaftigkeit_Restlebensdauer, huerde/Entwurfsbindung, huerde/Fehlende_Datenstandards, huerde/Fehlende_Lagerflaeche, huerde/Fehlende_Standardisierung, huerde/Gewaehrleistung, huerde/Haftung, huerde/Heterogenitaet_Chargen, huerde/Hygieneanforderung, huerde/Kompatibilitaetsproblem, huerde/Materialqualitaet_Unklar, huerde/Mengenunsicherheit, huerde/Schadstoffbelastung, huerde/Technische_Freigabe, huerde/Terminunsicherheit, huerde/Toleranzen, huerde/Unkonventionelles_Material, huerde/Verfuegbarkeitsproblem, huerde/Witterung_Feuchte, huerde/Zustand_Unklar]
logistik -> [logistik/Bauteiltracking, logistik/Just_in_Time, logistik/Lagerflaeche, logistik/Lagerung, logistik/Lokale_Wiederverwendung, logistik/Materialmatching, logistik/Materialverfuegbarkeit, logistik/Transport, logistik/Transportdistanz, logistik/Zwischenlagerung]
bausystem -> [bausystem/Betonfertigteil_System, bausystem/Holz_Skelettbau, bausystem/Holzrahmenbau, bausystem/Plattenbau, bausystem/Stahl_Skelettbau]
bauteiltyp -> [bauteiltyp/Ausbau, bauteiltyp/Boden, bauteiltyp/Dach, bauteiltyp/Daemmung, bauteiltyp/Decke, bauteiltyp/Fassade, bauteiltyp/Fenster, bauteiltyp/Fundament, bauteiltyp/Gelaender, bauteiltyp/Stuetze, bauteiltyp/Technik, bauteiltyp/Traeger, bauteiltyp/Treppe, bauteiltyp/Tuer, bauteiltyp/Wand]
bauteilebene -> [bauteilebene/Bauteilgruppe, bauteilebene/Einzelbauteil, bauteilebene/Gebaeudeteil, bauteilebene/Materialcharge, bauteilebene/Oberflaechenschicht, bauteilebene/System]
bauteilzustand -> [bauteilzustand/Beschaedigt, bauteilzustand/Geprueft, bauteilzustand/Intakt, bauteilzustand/Kontaminiert, bauteilzustand/Korrodiert, bauteilzustand/Patiniert, bauteilzustand/Restlebensdauer_Bekannt, bauteilzustand/Restlebensdauer_Unklar, bauteilzustand/Ungeprueft]
material -> [material/Aluminium, material/Beton, material/Daemmstoff, material/Glas, material/Gusseisen, material/Holz, material/Keramik, material/Kunststoff, material/Lehm, material/Naturstein, material/Recyclingbeton, material/Stahl, material/Stahlbeton, material/Stroh, material/Ziegel]
nutzung -> [nutzung/Buero, nutzung/Gewerbe, nutzung/Infrastruktur, nutzung/Kultur, nutzung/Lager_Depot, nutzung/Mischnutzung, nutzung/Schule_Bildung, nutzung/Sozialbau, nutzung/Wohnen]
prozessphase -> [prozessphase/Aufbereitung, prozessphase/Betrieb, prozessphase/Dokumentation, prozessphase/Identifikation, prozessphase/Lagerung, prozessphase/Planung, prozessphase/Pruefung, prozessphase/Rueckbau, prozessphase/Transport, prozessphase/Wiedereinbau]
methode -> [methode/Abrissmonitoring, methode/Bauteilkatalogisierung, methode/Building_Material_Scouting, methode/Design_for_Disassembly, methode/Form_Follows_Availability, methode/Materialinventur, methode/Pre_Deconstruction_Audit, methode/ReUse_Assessment, methode/ReUse_Ausschreibung, methode/Reversibilitaet, methode/Urban_Mining, methode/Wiederverwendungskriterien, methode/Zirkulaere_Ausschreibung]
rueckbauverfahren -> [rueckbauverfahren/Ausbau_von_Bauteilen, rueckbauverfahren/Betonfraesen, rueckbauverfahren/Demontage, rueckbauverfahren/Selektiver_Rueckbau, rueckbauverfahren/Zerstoerungsarme_Bergung]
aufbereitungsverfahren -> [aufbereitungsverfahren/Drahtglasschneiden, aufbereitungsverfahren/Entmoertelung_von_Fliesen, aufbereitungsverfahren/Holzaufbereitung, aufbereitungsverfahren/Leuchten_Refurbishment, aufbereitungsverfahren/Qualitaetssicherung, aufbereitungsverfahren/Reinigung, aufbereitungsverfahren/Rekonditionierung, aufbereitungsverfahren/Remanufacturing, aufbereitungsverfahren/Reparatur, aufbereitungsverfahren/Verstaerkung, aufbereitungsverfahren/Zuschnitt]
rechtliche_bedingung -> [rechtliche_bedingung/Bauordnungsrecht, rechtliche_bedingung/EU_Taxonomie, rechtliche_bedingung/Gewaehrleistung, rechtliche_bedingung/Produkthaftung, rechtliche_bedingung/Vergaberecht, rechtliche_bedingung/Zulassung_im_Einzelfall]
ressourcenquelle -> [ressourcenquelle/Baustelle, ressourcenquelle/Bauteilboerse, ressourcenquelle/Donor_Infrastruktur, ressourcenquelle/Donorgebaeude, ressourcenquelle/Haendler, ressourcenquelle/Lager, ressourcenquelle/Materialstockpile, ressourcenquelle/Produktionsueberschuss, ressourcenquelle/Unbekannt]
beschaffungsweg -> [beschaffungsweg/Ausschreibung, beschaffungsweg/Bauteilboerse, beschaffungsweg/Digitale_Plattform, beschaffungsweg/Direktvermittlung, beschaffungsweg/Eigenbestand, beschaffungsweg/Informelles_Netzwerk, beschaffungsweg/Rueckbauprojekt, beschaffungsweg/Spende]
reuse_strategie -> [reuse_strategie/Adaptives_ReUse, reuse_strategie/Bestandserhalt, reuse_strategie/Design_for_Disassembly, reuse_strategie/Direkte_Wiederverwendung, reuse_strategie/Recycling, reuse_strategie/Refurbishment, reuse_strategie/Remanufacturing, reuse_strategie/Same_Site_ReUse, reuse_strategie/Upcycling, reuse_strategie/Urban_Mining, reuse_strategie/Weiterbauen_im_Bestand]
reuse_einsatzstatus -> [reuse_einsatzstatus/Geplant, reuse_einsatzstatus/Prototypisch, reuse_einsatzstatus/Realisiert, reuse_einsatzstatus/Temporaer, reuse_einsatzstatus/Unklar, reuse_einsatzstatus/Verworfen, reuse_einsatzstatus/Vorgeschlagen]
bauobjektstatus -> [bauobjektstatus/Gebaut, bauobjektstatus/Geplant, bauobjektstatus/In_Bau, bauobjektstatus/Prototyp, bauobjektstatus/Rueckgebaut, bauobjektstatus/Temporaer, bauobjektstatus/Unklar, bauobjektstatus/Wettbewerb]
datenqualitaet -> [datenqualitaet/Belegt, datenqualitaet/Geschaetzt, datenqualitaet/Nicht_Belegt, datenqualitaet/Primaerquelle, datenqualitaet/Sekundaerquelle, datenqualitaet/Unbekannt, datenqualitaet/Widerspruechlich]
zertifizierung_bewertungssystem -> [zertifizierung_bewertungssystem/BREEAM, zertifizierung_bewertungssystem/DGNB, zertifizierung_bewertungssystem/LEED, zertifizierung_bewertungssystem/Paris_Proof, zertifizierung_bewertungssystem/WELL]
leistungsanforderung -> [leistungsanforderung/Brandschutz, leistungsanforderung/Brandschutzanforderung, leistungsanforderung/Dauerhaftigkeit, leistungsanforderung/F90, leistungsanforderung/Feuchteschutz, leistungsanforderung/Feuerwiderstand, leistungsanforderung/R90, leistungsanforderung/REI90, leistungsanforderung/Rueckbaubarkeit, leistungsanforderung/Schadstofffreiheit, leistungsanforderung/Schallschutz, leistungsanforderung/Tragfaehigkeit, leistungsanforderung/Waermeschutz]
fuegung_verbindung -> [fuegung_verbindung/Klemmverbindung, fuegung_verbindung/Reversible_Fuegung, fuegung_verbindung/Steckverbindung, fuegung_verbindung/Verleimung, fuegung_verbindung/Vermoertelung, fuegung_verbindung/Verschraubung, fuegung_verbindung/Verschweissung]
wirtschaft -> [wirtschaft/Finanzierung, wirtschaft/Geschaeftsmodell, wirtschaft/Kostenvergleich, wirtschaft/Lebenszykluskosten, wirtschaft/Preisbildung, wirtschaft/Restwert]
foerderprogramm -> [foerderprogramm/BBSM, foerderprogramm/FCRBE, foerderprogramm/PREUSE, foerderprogramm/Reallabor_Be_Ware, foerderprogramm/Zukunftbau]
programm_kontext -> [programm_kontext/Foerderprogramm, programm_kontext/Forschungsprojekt, programm_kontext/Kommunales_Programm, programm_kontext/Pilotprojekt, programm_kontext/Reallabor, programm_kontext/Wettbewerb]
kontextmerkmal -> [kontextmerkmal/Bestandserhalt_Policy, kontextmerkmal/Pilotprojekt]
schadstoff -> [schadstoff/Asbest, schadstoff/Bleifarbe, schadstoff/Holzschutzmittel, schadstoff/PAK, schadstoff/PCB]
norm -> [norm/DIN_18940, norm/DIN_EN_15804, norm/DIN_EN_15978, norm/EN_1090, norm/ISO_14040, norm/ISO_14044, norm/ISO_20887]
bauaufgabe_intervention -> [bauaufgabe_intervention/Aufstockung, bauaufgabe_intervention/Erweiterung, bauaufgabe_intervention/Fit_out, bauaufgabe_intervention/Neubau, bauaufgabe_intervention/Rueckbau, bauaufgabe_intervention/Sanierung, bauaufgabe_intervention/Translozierung, bauaufgabe_intervention/Umbau, bauaufgabe_intervention/Umnutzung, bauaufgabe_intervention/Wiederaufbau]
funktionswechsel -> [funktionswechsel/Dekorative_Funktion, funktionswechsel/Gleiche_Funktion, funktionswechsel/Konstruktive_Funktion, funktionswechsel/Neue_Funktion, funktionswechsel/Technische_Funktion, funktionswechsel/Unbekannt]
akteurrolle -> [akteurrolle/Architektur, akteurrolle/Aufbereitung_Refurbishment, akteurrolle/Bauausfuehrung, akteurrolle/Bauherr_Auftraggeber, akteurrolle/Betreiber_Nutzer, akteurrolle/Brandschutz_Barrierefreiheit, akteurrolle/Fassade, akteurrolle/Forschung_Dokumentation, akteurrolle/Kunst_Gestaltung, akteurrolle/Landschaftsplanung, akteurrolle/Materiallieferant, akteurrolle/Nachhaltigkeitsberatung, akteurrolle/Oeffentliche_Hand, akteurrolle/Projektbeteiligte_Unbestimmt, akteurrolle/Projektmanagement_Koordination, akteurrolle/Pruefung_Qualitaetssicherung, akteurrolle/Reuse_Beratung, akteurrolle/Rueckbau_Demontage, akteurrolle/Stahlbau_Fertigung, akteurrolle/TGA_Gebaeudetechnik, akteurrolle/Tragwerksplanung]
```
