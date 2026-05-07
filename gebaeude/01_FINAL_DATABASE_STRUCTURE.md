# Finale Ordner- und Entitätenstruktur für die Direct-Reuse-Datenbank

Stand: 2026-05-07  
Ziel: saubere Markdown-/Obsidian-Datenbank für Fallstudien zu Bauteilwiederverwendung, Direct Reuse und zirkulärem Bauen.

## 1. Grundprinzip

Die bisher erzeugten `Gebäude/*.md`-Dateien sind inhaltlich meistens **Fallstudien**, nicht nur Gebäudedateien. Deshalb werden sie in `01_Fallstudie/` geführt.

Ein reales physisches Gebäude, z. B. ein Donorgebäude oder ein Empfängergebäude, gehört dagegen in `03_Gebaeude/`.

Die Datenbank trennt künftig streng:

- **Fallstudie** = wissenschaftlich/kuratorisch bewerteter Fall.
- **Projekt** = Planungs-/Bauvorhaben.
- **Gebäude** = physisches Bauwerk, Donor, Empfänger oder Bestand.
- **Bauteiltyp** = generische Bauteilklasse, z. B. Träger, Fenster, Deckenplatte.
- **Bauteilposition** = konkreter wiederverwendeter Bauteilsatz in einer Fallstudie.
- **ReuseKette** = Fluss von Bauteilen von Donor zu Empfänger.
- **Quelle** = überprüfbare Evidenz für eine Aussage.
- **Datenpunkt** = einzelner Kennwert mit Quelle, Methode und Vertrauensgrad.

## 2. Finale Ordnerstruktur

```text
reuse_database/
├── 00_SYSTEM/
│   ├── 00_INDEX.md
│   ├── 01_FINAL_DATABASE_STRUCTURE.md
│   ├── 02_NAMING_CONVENTIONS.md
│   ├── 03_CONTROLLED_VOCABULARY.md
│   ├── 04_MIGRATION_RULES.md
│   └── 00_TEMPLATES/
│       ├── TEMPLATE_Fallstudie.md
│       ├── TEMPLATE_Gebaeude.md
│       ├── TEMPLATE_Projekt.md
│       ├── TEMPLATE_Akteur.md
│       ├── TEMPLATE_Bauteilposition.md
│       ├── TEMPLATE_Quelle.md
│       └── TEMPLATE_Datenpunkt.md
├── 01_Fallstudie/
├── 02_Projekt/
├── 03_Gebaeude/
├── 04_Ort/
├── 05_Akteur/
├── 06_Bauteiltyp/
├── 07_Bauteilposition/
├── 08_Material/
├── 09_ReuseStrategie/
├── 10_ReuseKette/
├── 11_Prozessphase/
├── 12_Methode/
├── 13_Abbruchmethode/
├── 14_Aufbereitungsmethode/
├── 15_Pruefung/
├── 16_Leistungsanforderung/
├── 17_Tragwerkssystem/
├── 18_Verbindung/
├── 19_Norm_Recht/
├── 20_Huerde/
├── 21_Logistik/
├── 22_Wirtschaft/
├── 23_Kennwertdefinition/
├── 24_Datenpunkt/
├── 25_Datenmodell/
├── 26_Dokument/
├── 27_Quelle/
├── 28_Tool_Software/
├── 29_Bauteilboerse/
├── 30_Foerderprogramm/
├── 31_Schadstoff/
├── 32_Status_Bewertung/
├── 33_Quellenkonflikt/
├── 34_Offene_Frage/
├── 90_IMPORT_ROHDATEN/
└── 99_ARCHIV/
```

## 3. Was wohin gehört?

| Ordner | Entität | Inhalt | Beispiel |
|---|---|---|---|
| `01_Fallstudie/` | Fallstudie | Bewerteter Direct-Reuse-Fall mit allen 13 Analyseabschnitten | `BioPartner_5_Leiden_Oegstgeest.md` |
| `02_Projekt/` | Projekt | Bau- oder Forschungsprojekt als organisatorische Einheit | `BioPartner_5.md`, `ReCreate.md` |
| `03_Gebaeude/` | Gebäude | Physisches Gebäude: Donor, Empfänger, Bestand, Pavillon | `Gorlaeus_High_Rise_Leiden.md` |
| `04_Ort/` | Ort | Stadt, Quartier, Adresse, Areal | `Leiden_Bio_Science_Park.md` |
| `05_Akteur/` | Akteur | Organisationen, Büros, Behörden, Institute, Personen, Netzwerke | `Rotor.md`, `BBSR_Zukunft_Bau.md` |
| `06_Bauteiltyp/` | Bauteiltyp | Generische Bauteilklasse | `Traeger.md`, `Fenster.md`, `Deckenplatte.md` |
| `07_Bauteilposition/` | Bauteilposition | Konkretes wiederverwendetes Bauteilpaket in einem Fall | `BioPartner_5_Gorlaeus_Stahltragwerk.md` |
| `08_Material/` | Material | Materialklassen und spezifische Materialgruppen | `Baustahl.md`, `Brettschichtholz.md` |
| `09_ReuseStrategie/` | Reuse-Strategie | Direct Reuse, ex-situ, in-situ transformiert, Gebäudeversetzung usw. | `Ex_situ_Bauteilwiederverwendung.md` |
| `10_ReuseKette/` | Reuse-Kette | Donor-Empfänger-Fluss, ggf. mehrere Stationen | `House_of_Fraser_to_TBC_London_Stahl.md` |
| `11_Prozessphase/` | Prozessphase | Bestandsaufnahme, Rückbau, Lagerung, Wiedereinbau usw. | `Bauteilinventar.md` |
| `12_Methode/` | Methode | Materialaudit, Urban Mining, selektiver Rückbau usw. | `Pre_Demolition_Audit.md` |
| `13_Abbruchmethode/` | Abbruchmethode | Selektiver Rückbau, Schneiden, Demontage usw. | `Selektiver_Rueckbau.md` |
| `14_Aufbereitungsmethode/` | Aufbereitungsmethode | Reinigung, Entmörtelung, Rekonditionierung, Refurbishment | `Holzaufbereitung.md` |
| `15_Pruefung/` | Prüfung | Tests, Sichtprüfung, Materialprüfung, Tragwerksnachweis | `Materialpruefung_Stahl.md` |
| `16_Leistungsanforderung/` | Leistungsanforderung | Brandschutz, Tragfähigkeit, U-Wert, Dauerhaftigkeit usw. | `Tragfaehigkeit.md` |
| `17_Tragwerkssystem/` | Tragwerkssystem | Stahl-Skelettbau, Holztragwerk, Betonfertigteilsystem usw. | `Stahl_Skelettbau.md` |
| `18_Verbindung/` | Verbindung | Schrauben, Schweißen, reversible Fügung, Anschlussdetails | `Geschraubte_Verbindung.md` |
| `19_Norm_Recht/` | Norm/Recht | Normen, Zulassung, Haftung, Bauordnungsrecht | `Haftung.md`, `Bauproduktrecht.md` |
| `20_Huerde/` | Hürde | Technische, rechtliche, logistische, wirtschaftliche Hürden | `Verfuegbarkeitsproblem.md` |
| `21_Logistik/` | Logistik | Transport, Lager, Zwischenlager, Just-in-time-Beschaffung | `Zwischenlagerung.md` |
| `22_Wirtschaft/` | Wirtschaft | Kostenwirkung, Beschaffung, Versicherung, Marktbarrieren | `Gewaehrleistung.md` |
| `23_Kennwertdefinition/` | Kennwertdefinition | Definition eines Kennwerts | `CO2_Einsparung.md` |
| `24_Datenpunkt/` | Datenpunkt | Konkreter Zahlenwert mit Quelle und Bilanzgrenze | `Holbein_Gardens_Reused_Steel_24t.md` |
| `25_Datenmodell/` | Datenmodell | IFC, Materialpass, Ontologie, Klassifikation | `Materialpass_Schema.md` |
| `26_Dokument/` | Dokument | Auditbericht, Materialpass, LCA, Ausschreibung, Publikation | `Pre_Demolition_Audit.md` |
| `27_Quelle/` | Quelle | Konkrete externe Quelle, Webseite, PDF, Fachartikel | `Rotor_MULTI_De_Brouckere_Tower.md` |
| `28_Tool_Software/` | Tool/Software | Software und digitale Tools | `Madaster.md`, `One_Click_LCA.md` |
| `29_Bauteilboerse/` | Bauteilbörse | Marktplätze, Handelsplattformen, Reuse-Portale | `Rotor_DC.md` |
| `30_Foerderprogramm/` | Förderprogramm | Programme, Förderlinien, Forschungsrahmen | `FCRBE.md` |
| `31_Schadstoff/` | Schadstoff | Asbest, PCB, Blei, Schadstoffprüfung | `Asbest.md` |
| `32_Status_Bewertung/` | Status/Bewertung | Kontrollvokabular für Projektstatus, Entscheidung, Sterne | `Projektstatus.md` |
| `33_Quellenkonflikt/` | Quellenkonflikt | Dokumentierte Widersprüche zwischen Quellen | `TBC_London_Stahlmenge_20t_vs_40t.md` |
| `34_Offene_Frage/` | Offene Frage | Fehlende Daten, zu prüfende Quellen, Forschungsfragen | `BioPartner_5_Stahlpruefung_unbekannt.md` |
| `90_IMPORT_ROHDATEN/` | Rohdaten | Unsortierte Imports, alte Listen, Web-Clippings | `gebaeude4_wiederverwendung_direct_reuse_examples.md` |
| `99_ARCHIV/` | Archiv | Ersetzte, doppelte, veraltete oder verworfene Dateien | `duplicate_old.md` |

## 4. Zentrale Modellierungsentscheidung

### 4.1 Fallstudie ist nicht Gebäude

Alle bisher erzeugten `Gebäude/*.md`-Fallstudien sollten nach `01_Fallstudie/` migriert werden.

Beispiel:

```text
alt:
Gebäude/BioPartner_5_Leiden_Oegstgeest.md

neu:
01_Fallstudie/BioPartner_5_Leiden_Oegstgeest.md
02_Projekt/BioPartner_5.md
03_Gebaeude/BioPartner_5_Oegstgeest.md
03_Gebaeude/Gorlaeus_High_Rise_Leiden.md
07_Bauteilposition/BioPartner_5_Gorlaeus_Stahltragwerk.md
10_ReuseKette/Gorlaeus_to_BioPartner_5_Stahltragwerk.md
```

### 4.2 Akteur statt People / Lehrstuhl / Gastprofessur / NGO / Büro

Alles, was handeln, planen, fördern, prüfen, lehren, forschen, bauen oder handeln kann, wird `Akteur`.

Nicht mehr getrennt führen als eigene Top-Level-Entitäten:

- People
- Lehrstuhl
- Gastprofessur
- Architekt
- Tragwerksplaner
- Bauherr
- NGO
- Netzwerk
- öffentliche Institution

Diese Rollen werden als Felder in `05_Akteur/*.md` geführt:

```yaml
akteur_typ: "planung_architektur_ingenieurwesen"
rollen:
  - Architekt
  - Reuse-Beratung
  - Forschung
```

### 4.3 Bauteiltyp vs. Bauteilposition

`06_Bauteiltyp/Traeger.md` beschreibt allgemein, was ein Träger ist.

`07_Bauteilposition/Holbein_Gardens_reused_steel_beams.md` beschreibt den konkreten wiederverwendeten Trägersatz in Holbein Gardens.

Dadurch kann dieselbe Bauteilklasse in vielen Fällen sauber verglichen werden.

### 4.4 Quelle vs. Dokument

`26_Dokument/` enthält Dokumenttypen oder interne Dokumente: Materialpass, LCA, Auditbericht, Ausschreibung.

`27_Quelle/` enthält konkrete Nachweise: eine bestimmte Projektseite, ein PDF, ein Fachartikel, ein Interview.

Jeder Wert, jede Menge und jede CO₂-Zahl muss auf eine Datei in `27_Quelle/` oder auf „unbekannt“ verweisen.

## 5. Pflichtfelder pro Datei

Jede Datei bekommt YAML-Frontmatter.

### 5.1 Pflichtfelder für alle Entitäten

```yaml
---
id: ""
entity_type: ""
title: ""
aliases: []
status: "aktiv"      # aktiv | pruefen | archiviert | entfernen
created: "YYYY-MM-DD"
last_reviewed: "YYYY-MM-DD"
source_quality: "unbekannt"  # belegt | teilweise_belegt | unklar | unbekannt
tags: []
---
```

### 5.2 Fallstudie

```yaml
---
id: "fs_biopartner_5_leiden_oegstgeest"
entity_type: "Fallstudie"
title: "BioPartner 5, Leiden / Oegstgeest"
aliases: ["BioPartner 5", "Biopartner 5 Leiden"]
entscheidung: "HAUPTFALL"
rating: "★★★★★"
vertrauensgrad: "belegt"
projektstatus: "gebaut"
warnung_bestandserhalt: false
warnung_moebel_dekoration: false
direct_reuse_valid: true
reuse_hauptniveau: ["Tragwerk"]
reuse_art: ["ex-situ", "Bauteilwiederverwendung"]
ort: ["[[04_Ort/Leiden_Oegstgeest]]"]
projekt: ["[[02_Projekt/BioPartner_5]]"]
gebaeude_empfaenger: ["[[03_Gebaeude/BioPartner_5_Oegstgeest]]"]
gebaeude_donor: ["[[03_Gebaeude/Gorlaeus_High_Rise_Leiden]]"]
reuse_ketten: ["[[10_ReuseKette/Gorlaeus_to_BioPartner_5_Stahltragwerk]]"]
akteure:
  - akteur: "[[05_Akteur/Popma_ter_Steege]]"
    rolle: "Architekt"
  - akteur: "[[05_Akteur/IMd_Raadgevende_Ingenieurs]]"
    rolle: "Tragwerksplaner"
quellen: []
last_reviewed: "2026-05-07"
---
```

### 5.3 Bauteilposition

```yaml
---
id: "bp_biopartner_5_gorlaeus_stahltragwerk"
entity_type: "Bauteilposition"
title: "BioPartner 5 – wiederverwendetes Gorlaeus-Stahltragwerk"
fallstudie: "[[01_Fallstudie/BioPartner_5_Leiden_Oegstgeest]]"
bauteiltypen:
  - "[[06_Bauteiltyp/Traeger]]"
  - "[[06_Bauteiltyp/Stuetze]]"
material: "[[08_Material/Baustahl]]"
herkunft: "[[03_Gebaeude/Gorlaeus_High_Rise_Leiden]]"
empfaenger: "[[03_Gebaeude/BioPartner_5_Oegstgeest]]"
alte_funktion: "tragendes Stahltragwerk"
neue_funktion: "tragendes Stahltragwerk"
menge_wert: "unbekannt"
menge_einheit: "unbekannt"
tragend: true
raeumlich: false
huelle: false
technisch: false
pruefung: []
leistungsanforderung: ["[[16_Leistungsanforderung/Tragfaehigkeit]]"]
quellen: []
vertrauensgrad: "belegt"
---
```

## 6. Namenskonvention

### 6.1 Ordner

- Format: `NN_EntityName`
- ASCII bevorzugt: `Gebaeude`, `Pruefung`, `Huerde`
- Singular verwenden: `Fallstudie`, nicht `Fallstudien`
- Keine Leerzeichen in Ordnernamen

### 6.2 Dateien

- Format: `Readable_Title_Case.md`
- Keine Sonderzeichen, keine Schrägstriche, keine Doppelpunkte
- Umlaute ersetzen: `ä → ae`, `ö → oe`, `ü → ue`, `ß → ss`
- Keine Nummernpräfixe bei Entitätsdateien, weil die `id` im Frontmatter stabil ist

## 7. Relationstypen

| Relation | Von | Nach | Beispiel |
|---|---|---|---|
| `ist_fallstudie_von` | Fallstudie | Projekt | BioPartner-Fallstudie → BioPartner 5 |
| `hat_empfaengergebaeude` | Fallstudie | Gebäude | BioPartner-Fallstudie → BioPartner 5 |
| `hat_donorgebaeude` | Fallstudie | Gebäude | BioPartner-Fallstudie → Gorlaeus |
| `verwendet_bauteilposition` | Fallstudie | Bauteilposition | Holbein Gardens → reused steel beams |
| `ist_typ_von` | Bauteilposition | Bauteiltyp | reused steel beams → Träger |
| `besteht_aus_material` | Bauteilposition | Material | steel beams → Baustahl |
| `folgt_strategie` | Fallstudie | ReuseStrategie | K.118 → ex-situ |
| `hat_prozessphase` | Fallstudie | Prozessphase | K.118 → Rückbau |
| `hat_huerde` | Fallstudie | Hürde | Timber Square → Terminunsicherheit |
| `hat_datenpunkt` | Fallstudie | Datenpunkt | Holbein Gardens → 24 t reused steel |
| `belegt_durch` | Aussage/Datenpunkt | Quelle | 24 t steel → IStructE article |
| `hat_quellenkonflikt` | Fallstudie/Datenpunkt | Quellenkonflikt | TBC.London → 20 t vs. 40 t |

## 8. Migration der bestehenden Listen

### 8.1 Akteur-Ordner

Die bisherigen Akteur-Unterordner werden nicht als Top-Level-Struktur behalten. Sie werden zu `akteur_typ`.

```text
alt:
01_oeffentliche_institutionen_foerderung/BBSR_Zukunft_Bau.md
04_planung_architektur_ingenieurwesen/Rotor.md
05_reuse_beratung_prozessdienstleister/Concular.md

neu:
05_Akteur/BBSR_Zukunft_Bau.md
05_Akteur/Rotor.md
05_Akteur/Concular.md
```

### 8.2 Berichte und Dokumente

```text
alt:
bericht/01_BIM_Berlin_detailed.md
dokument/Materialpass.md

neu:
26_Dokument/BIM_Berlin_detailed.md
26_Dokument/Materialpass.md
```

### 8.3 Software und Tools

```text
alt:
software/Madaster.md
Tool/...

neu:
28_Tool_Software/Madaster.md
```

### 8.4 Gebäude-Dateien

```text
alt:
Gebäude/BedZED_London_Hackbridge.md

neu:
01_Fallstudie/BedZED_London_Hackbridge.md
03_Gebaeude/BedZED_Hackbridge.md
```

## 9. Bewertungs- und Abgrenzungslogik

```yaml
entscheidung:
  - HAUPTFALL
  - VERGLEICHSFALL
  - ANHANG
  - ENTFERNEN

projektstatus:
  - gebaut
  - im_bau
  - prototyp
  - geplant
  - ungebaut
  - abgebrochen
  - unklar

vertrauensgrad:
  - belegt
  - teilweise_belegt
  - unklar
  - unbekannt

direct_reuse_valid:
  - true
  - false
  - teilweise
  - unbekannt
```

## 10. Neue Entitäten, die wirklich nötig sind

| Neue Entität | Warum nötig? | Beispiel |
|---|---|---|
| `Bauteilposition` | Trennt generischen Bauteiltyp von konkretem Reuse-Bauteilpaket | Holbein Gardens – reused steel beams |
| `ReuseKette` | Erfasst Donor → Zwischenlager → Empfänger | House of Fraser → TBC.London |
| `Quelle` | Saubere Evidenzdateien statt Links nur am Ende | Rotor-Projektseite, IStructE-Artikel |
| `Datenpunkt` | Einzelne Werte mit Quelle, Methode, Bilanzgrenze | 24 t reused steel |
| `Quellenkonflikt` | Widersprüche bleiben sichtbar | TBC.London 20 t vs. 40 t |
| `Offene_Frage` | Datenlücken werden abfragbar | Prüfung Stahl unbekannt |
| `Status_Bewertung` | Einheitliches Vokabular für Sterne, Status, Direct-Reuse-Validität | Projektstatus gebaut/geplant |

## 11. Empfohlene Reihenfolge der Bereinigung

1. Alle erzeugten `Gebäude/*.md` in `01_Fallstudie/` verschieben.
2. Für jeden Fall mindestens ein `03_Gebaeude/`-Dokument anlegen.
3. Bei ex-situ-Fällen Donorgebäude als eigene `03_Gebaeude/`-Datei ergänzen.
4. Alle Akteure in `05_Akteur/` zusammenführen.
5. Pro Fall die wichtigsten wiederverwendeten Bauteile als `07_Bauteilposition/` anlegen.
6. Quellen aus den Quellenblöcken in `27_Quelle/` normalisieren.
7. Mengen/CO₂/Kosten/Bauzeit-Werte als `24_Datenpunkt/` auslagern.
8. Widersprüche als `33_Quellenkonflikt/` dokumentieren.
9. Entfernen-/DfD-/Watchlist-Fälle nicht löschen, sondern in `01_Fallstudie/` belassen mit `entscheidung: ENTFERNEN` oder `ANHANG`.
10. Alte oder doppelte Dateien nach `99_ARCHIV/` verschieben.

## 12. Minimaler Fallstudienaufbau

Jede Datei in `01_Fallstudie/` sollte diese Überschriften behalten:

```markdown
# Titel

## 1. Einordnung
## 2. Entitäten-Mapping
## 3. Fallstudie
## 4. Reuse-Strategie
## 5. Bauteil-Inventar
## 6. Prozess und Logistik
## 7. Technik, Leistung, Normen
## 8. Kennwerte
## 9. Hürden-Matrix
## 10. Wirtschaft und Beschaffung
## 11. Gestaltung und kultureller Wert
## 12. Offene Entitäten und Datenlücken
## 13. Abschluss
## Quellen
```

## 13. Beispiel: BioPartner 5 als sauber modellierter Fall

```text
01_Fallstudie/BioPartner_5_Leiden_Oegstgeest.md
02_Projekt/BioPartner_5.md
03_Gebaeude/BioPartner_5_Oegstgeest.md
03_Gebaeude/Gorlaeus_High_Rise_Leiden.md
04_Ort/Leiden_Oegstgeest.md
05_Akteur/Leiden_University.md
05_Akteur/Popma_ter_Steege.md
05_Akteur/IMd_Raadgevende_Ingenieurs.md
06_Bauteiltyp/Traeger.md
06_Bauteiltyp/Stuetze.md
07_Bauteilposition/BioPartner_5_Gorlaeus_Stahltragwerk.md
08_Material/Baustahl.md
09_ReuseStrategie/Ex_situ_Bauteilwiederverwendung.md
10_ReuseKette/Gorlaeus_to_BioPartner_5_Stahltragwerk.md
15_Pruefung/Materialpruefung_Stahl.md
16_Leistungsanforderung/Tragfaehigkeit.md
17_Tragwerkssystem/Stahl_Skelettbau.md
20_Huerde/Verfuegbarkeitsproblem.md
27_Quelle/Nationale_Staalprijs_BioPartner_5.md
34_Offene_Frage/BioPartner_5_Pruefdossier_Stahl_unbekannt.md
```

## 14. Beispiel: TBC.London als Reuse-Kette statt normales Gebäude

```text
01_Fallstudie/Tower_Bridge_Court_TBC_London_steel_reuse.md
02_Projekt/TBC_London.md
03_Gebaeude/Tower_Bridge_Court_London.md
03_Gebaeude/House_of_Fraser_318_Oxford_Street.md
07_Bauteilposition/TBC_London_reused_House_of_Fraser_steel.md
10_ReuseKette/House_of_Fraser_to_TBC_London_Stahl.md
24_Datenpunkt/TBC_London_reused_steel_20t.md
24_Datenpunkt/TBC_London_reused_steel_40t.md
33_Quellenkonflikt/TBC_London_Stahlmenge_20t_vs_40t.md
```

## 15. Was nicht mehr als eigene Top-Level-Entität geführt werden sollte

| Alt | Neu |
|---|---|
| `People` | `05_Akteur/` mit `akteur_typ: person` |
| `Lehrstuhl` | `05_Akteur/` mit `akteur_typ: forschung_lehre` |
| `Gastprofessur` | `05_Akteur/` mit `akteur_typ: forschung_lehre` |
| `Bericht` | `26_Dokument/` mit `dokument_typ: bericht` |
| `Software` und `Tool` getrennt | `28_Tool_Software/` |
| `Gebäude` als Fallstudienordner | `01_Fallstudie/` |
| reine Akteur-Unterkategorien als Ordner | `05_Akteur/` + Frontmatter-Felder |
| Kennwertdefinition und konkreter Wert in derselben Datei | `23_Kennwertdefinition/` + `24_Datenpunkt/` |

## 16. Finale Empfehlung

Diese Struktur ist groß genug für die komplette Fallstudiensammlung, aber nicht unnötig kleinteilig. Die wichtigsten Verbesserungen gegenüber der bisherigen Struktur sind:

1. Fallstudien werden nicht mehr mit Gebäuden verwechselt.
2. Donorgebäude, Empfängergebäude und Reuse-Ketten werden sauber modelliert.
3. Bauteiltypen und konkrete wiederverwendete Bauteile werden getrennt.
4. Akteure werden vereinheitlicht und über Rollen beschrieben.
5. Quellen, Datenpunkte und Quellenkonflikte werden abfragbar.
6. Entfernen-/DfD-/Watchlist-Fälle bleiben nachvollziehbar, aber stören nicht die Hauptliste.
