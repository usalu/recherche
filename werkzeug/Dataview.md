## Verknüpfungen

- **Übergeordnete Themen:** Wissensmanagement; Markdown-Datenbank; Forschungsrepo; Metadaten; Abfragen; Obsidian-Workflow; Dokumentation.
- **Verwandte Dateien:** `werkzeug/Obsidian.md`; `werkzeug/Materialdatenbank.md`; `werkzeug/BIM.md`; `dokument/Materialpass.md`; `dokument/Quellenarbeit.md`; `datenmodell/Metadaten.md`; `methode/Literaturreview.md`; `methode/Bauteilkatalogisierung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Obsidian Community Plugins; Dataview Plugin; Markdown; YAML Front Matter / Properties; Links und Backlinks; Forschungsdatenmanagement; FAIR-Prinzipien; kontrollierte Schlagwörter; Bauteil- und Quellenregister.

## Kurzdefinition

Dataview ist ein Community-Plugin für Obsidian, das Markdown-Notizen mit strukturierten Metadaten abfragbar macht. Es erzeugt Tabellen, Listen, Aufgabenübersichten und andere Ansichten aus YAML/Properties, Inline-Feldern, Tags, Links, Ordnern und Dateiattributen. Dataview ist damit eine lokale, textbasierte Abfrageebene über ein Markdown-Repo.

Für das Forschungsrepo ist Dataview kein BIM-Werkzeug, keine Materialplattform und keine externe Datenbank. Es ist ein **Recherche- und Ordnungswerkzeug**, mit dem Inhalte aus einzelnen thematischen Dateien sichtbar, kontrollierbar und quer auswertbar werden, solange die Dateien konsistente Metadaten enthalten.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung ist ein querschnittliches Thema: Bauteile, Akteure, Standards, Methoden, Fallstudien, Kennwerte, Risiken, Nachweise und Werkzeuge hängen eng zusammen. In einem dateibasierten Forschungsrepo können diese Beziehungen schnell unübersichtlich werden. Dataview hilft, aus vielen thematischen Markdown-Dateien dynamische Übersichten zu erzeugen.

Typische Nutzen:

- Übersicht über alle Dateien mit fehlenden Quellen, offenen Fragen oder unsicheren Aussagen.
- Tabellen zu Fallstudien, Akteuren, Materialgruppen, Standards oder Werkzeugen.
- Nachverfolgung von Verknüpfungen zwischen Bauteilgruppen, Normen und Prüfanforderungen.
- Kontrolle, ob alle Dateien Pflichtabschnitte, Schlagwörter oder Quellen enthalten.
- Erstellung von Recherche-Dashboards für Re-Use-Plattformen, Materialpässe, BIM, Rückbau und Logistik.
- Trennung zwischen Primärwissen in Dateien und sekundären Ansichten in Dashboards.

Dataview unterstützt damit die wissenschaftliche Arbeitsweise des Repos: Jede Datei bleibt primärer Wissensspeicher; Dataview erzeugt lediglich Ansichten und Auswertungen.

## Fachinhalt

### Funktionsweise

Dataview indexiert Markdown-Dateien im Obsidian-Vault. Es liest Metadaten aus:

- **YAML Front Matter / Properties:** strukturierte Felder am Dateianfang, z. B. `status`, `thema`, `quelle_typ`, `akteur`, `standard`.
- **Inline-Feldern:** Dataview-spezifische Felder innerhalb des Texts, z. B. `Material:: Stahl`.
- **Tags:** z. B. `#standard`, `#plattform`, `#fallstudie`.
- **Links:** interne Wikilinks und ausgehende / eingehende Verknüpfungen.
- **Dateiattributen:** Dateiname, Pfad, Änderungsdatum, Erstellungsdatum, Aufgaben.
- **Tasks:** Markdown-Aufgaben mit Status, Fälligkeitsdatum, Tags oder Inline-Feldern.

Die Abfragen werden in Codeblöcken geschrieben und beim Öffnen der Notiz dynamisch gerendert. Grundformen sind `TABLE`, `LIST`, `TASK` und `CALENDAR`; komplexere Auswertungen sind mit DataviewJS möglich.

### Datentypen für das Forschungsrepo

Sinnvolle Metadatenfelder für das Thema Wiederverwendung:

```yaml
---
typ: werkzeug
status: entwurf
themen:
  - wiederverwendung
  - digitale_tools
bezug:
  - BIM
  - materialpass
relevante_standards:
  - ISO 19650
  - IFC
akteure:
  - Planer
  - Bestandshalter
  - Plattformbetreiber
unsicherheit: mittel
letzte_pruefung: 2026-04-27
---
```

Weitere mögliche Felder:

- `materialgruppe`: Stahl, Holz, Glas, Ziegel, Naturstein, TGA, Innenausbau.
- `lebenszyklusphase`: Bestandserfassung, Rückbau, Lagerung, Planung, Wiedereinbau, Betrieb.
- `datenart`: Geometrie, Material, Zustand, Ökobilanz, Recht, Markt, Logistik.
- `quelle_typ`: Norm, Primärquelle, wissenschaftlich, Praxisleitfaden, Plattformseite.
- `region`: EU, Deutschland, Schweiz, Belgien, Niederlande, Frankreich.
- `validitaet`: gesichert, unsicher, regional, veraltet, zu prüfen.
- `pflichtabschnitte_ok`: ja/nein.
- `reviewbedarf`: hoch/mittel/niedrig.

### Abfragebeispiele

Alle Werkzeugdateien mit Status:

```dataview
TABLE status, letzte_pruefung, unsicherheit
FROM "werkzeug"
SORT file.name ASC
```

Alle Dateien, die BIM erwähnen oder verknüpfen:

```dataview
LIST
FROM [[]]
WHERE contains(file.outlinks, [[BIM]]) OR contains(bezug, "BIM")
```

Offene Rechercheaufgaben:

```dataview
TASK
FROM ""
WHERE !completed AND contains(text, "prüfen")
SORT file.path ASC
```

Fallstudien nach Materialgruppe:

```dataview
TABLE materialgruppe, region, reuse_anteil, quelle_typ
FROM "fallstudie"
WHERE materialgruppe
SORT materialgruppe ASC
```

Dateien mit unsicherem Forschungsstand:

```dataview
TABLE typ, unsicherheit, letzte_pruefung
FROM ""
WHERE unsicherheit = "hoch" OR validitaet = "zu prüfen"
```

### Einsatzszenarien

- **Repo-Qualitätssicherung:** Welche Dateien fehlen? Welche Pflichtstruktur ist unvollständig? Welche Quellen sind veraltet?
- **Literaturreview:** Welche Quellen betreffen Standards, Plattformen, Recht, Wirtschaft oder Technik?
- **Akteursmapping:** Welche Akteure werden in welchen Dateien genannt?
- **Materialmatrix:** Welche Materialgruppen haben welche Prüf-, Rückbau- und Wiederverwendungsanforderungen?
- **Methodenvergleich:** Welche Methoden liefern welche Datentypen und in welcher Lebenszyklusphase?
- **Projekt-Dashboard:** Für eine Fallstudie können Materialgruppen, Standards, Risiken, Logistik und Quellen zusammengezogen werden.
- **Unsicherheitsregister:** Unsichere oder regionale Aussagen werden systematisch nachverfolgt.

### Nutzen

- Keine proprietäre Datenbank nötig; Daten bleiben als Markdown lesbar.
- Dynamische Übersichten ohne Duplikation von Inhalten.
- Gute Verbindung mit Obsidian-Links, Backlinks und Graphansicht.
- Niedrige Einstiegshürde für Forschungsnotizen.
- Versionskontrollfreundlich, da Markdown und YAML Git-kompatibel sind.
- Gut geeignet für qualitative Forschung, Quellenarbeit und thematische Wissensnetze.

### Grenzen

- Dataview ist abhängig von Obsidian und Community-Plugin-Wartung.
- Abfragen funktionieren nur so gut wie Metadatenkonventionen.
- Keine robuste Mehrnutzer-Datenbank mit Rechte-, Transaktions- und Validierungslogik.
- Keine garantierte Normkonformität, kein BIM- oder IFC-Parser.
- Für große Datenmengen, komplexe Relationen oder auditfähige Nachweise nur begrenzt geeignet.
- Metadaten können schnell uneinheitlich werden, wenn kein kontrolliertes Vokabular verwendet wird.
- Dataview-Ausgaben sind dynamische Ansichten; beim Export in andere Systeme können sie fehlen oder statisch werden.

### Abgrenzung zu BIM, IFC und Materialdatenbanken

- **Dataview vs. BIM:** Dataview verwaltet textliche Forschungs- und Metadaten; BIM verwaltet digitale Gebäudemodelle.
- **Dataview vs. IFC-Viewer:** Dataview fragt Markdown ab; IFC-Viewer visualisieren und prüfen modellbasierte Bauwerksdaten.
- **Dataview vs. Materialdatenbank:** Dataview kann Materialdaten referenzieren, ersetzt aber keine verifizierte Datenbank mit Kennwerten, EPDs oder Prüfdaten.
- **Dataview vs. Plattform:** Dataview erzeugt kein Marktmatching, keine Verfügbarkeitslogik und keine Transaktionen.

## Praxisbezug / Beispiele

- **Werkzeugregister:** Alle Dateien in `werkzeug/` können nach Zweck, Datentyp, Schnittstelle und Relevanz für Wiederverwendung abgefragt werden.
- **Standardmatrix:** Normen wie ISO 19650, IFC, DIN SPEC 91484, EN 15804 oder DGNB-Gebäuderessourcenpass können mit betroffenen Methoden und Werkzeugen verknüpft werden.
- **Materialgruppen-Dashboard:** Bauteile wie Türen, Fenster, Stahlträger, Ziegel, Naturstein und TGA-Komponenten lassen sich mit Prüfanforderungen, Plattformen und Fallstudien verknüpfen.
- **Quellenkontrolle:** Dateien mit ausschließlich Sekundärquellen oder fehlenden Primärquellen können gezielt gefunden werden.
- **Forschungsprozess:** Unsicherheiten werden nicht versteckt, sondern als Felder wie `unsicherheit: hoch` oder `validitaet: regional` sichtbar gemacht.

## Herausforderungen / offene Fragen

- Welche Metadatenfelder sind im Repo verbindlich, damit Abfragen langfristig stabil bleiben?
- Soll ein kontrolliertes Vokabular für Materialgruppen, Akteure, Standards und Methoden eingeführt werden?
- Wie werden Synonyme behandelt, z. B. Re-Use, Wiederverwendung, Wiederverwertung, Reclaimed Materials?
- Wie kann verhindert werden, dass Dataview-Dashboards Wissen duplizieren statt auf Primärdateien zu verweisen?
- Wie werden dynamische Ansichten bei Export, Archivierung oder Publikation reproduzierbar gemacht?
- Ist Dataview für kollaborative Forschung ausreichend, oder braucht es später eine relationale Datenbank?
- Wie werden Quellenqualität, Unsicherheitsgrad und Aktualität maschinenlesbar abgebildet?

## Quellen

- Dataview Plugin GitHub: blacksmithgu/obsidian-dataview, https://github.com/blacksmithgu/obsidian-dataview
- Dataview Documentation: Query structure, DQL, DataviewJS, https://blacksmithgu.github.io/obsidian-dataview/
- Obsidian Help: Properties, Links, Backlinks, Graph view, Community plugins, https://help.obsidian.md/
- Markdown Guide: Basic Syntax, https://www.markdownguide.org/basic-syntax/
- FAIR Principles: GO FAIR, https://www.go-fair.org/fair-principles/
- W3C: Data on the Web Best Practices, https://www.w3.org/TR/dwbp/
