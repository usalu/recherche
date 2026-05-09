# Dataview Abfragen

## Verknüpfungen

- [Entity_Schema.md](Entity_Schema.md) – legt fest, welche Entitäten und Beziehungen abgefragt werden können; jede Query orientiert sich am dort definierten Schema.
- [Namenskonvention.md](Namenskonvention.md) – Voraussetzung für stabile Queries: Ordner-, Datei- und Frontmatter-Namen müssen eindeutig sein, sonst bricht jeder Filter.
- [Recherche_Workflow.md](Recherche_Workflow.md) – die Queries sind das Audit-Werkzeug für den Workflow (Stubs finden, Quellenpflege prüfen, Lücken sammeln).
- [../AGENTS.md](../AGENTS.md) – Ziel ist ein in SQLite überführbarer Wissensbestand; Dataview ersetzt diese DB nicht, dient aber als Lese-Layer im Editor.
- [../schema.sql](../schema.sql) – die SQL-Sicht auf das Repo; viele Queries hier sind die Markdown-Vorabbildung der späteren SQL-Sichten.
- Alle `*/index.md` der Entitätsordner (`bauteil`, `material`, `gebaeude`, `pruefung`, `aufbereitungsmethode`, `abbruchmethode`, `verbindung`, `tragwerkssystem`, `leistungsanforderung`, `kennwert`, `schadstoff`, `standard`, `recht`, `foerderprogramm`, `akteur`, `projekt`, `fallstudie`, `bericht`, `dokument`, `interview`, `methode`, `prozessphase`, `werkzeug`, `wirtschaft`, `logistik`, `ort`, `huerde`, `reuse_strategie`).

---

## Zweck

Diese Datei sammelt geprüfte Dataview-Abfragen für Obsidian, mit denen das Forschungsrepo gelesen, gepflegt und auditiert wird. Sie ist gleichzeitig Werkzeugkasten und Qualitätssicherung: jede wiederkehrende Frage ans Repo („Welche Dateien sind Stubs?", „Wo fehlen Quellen?", „Welche Bauteile verweisen auf Beton?") soll genau einmal als Query vorliegen, statt jedes Mal manuell durch Ordner zu gehen. Die Queries bilden außerdem die Migrationsgrundlage in das SQLite-Schema (siehe [../schema.sql](../schema.sql)): was sich hier abfragen lässt, lässt sich später auch als SQL-View ausdrücken.

---

## Struktur / Regeln / Anwendung

### Voraussetzungen

- Obsidian mit aktiviertem Plugin **Dataview** (DQL und Dataview-JS).
- Vault-Wurzel ist `reuse/research/`. Alle Pfade in den Queries sind relativ zu dieser Wurzel.
- Empfohlen, aber noch nicht durchgängig vorhanden: YAML-Frontmatter pro Datei mit den Feldern `kategorie`, `status`, `quellen_geprueft`, `materialien`, `bauteile`, `standards`, `akteure`. Solange Frontmatter fehlt, arbeiten die Queries über `file.folder`, `file.name`, `file.outlinks` und Volltextsuche.

### Konventionen für Queries

- Kategorie = unterster Ordnername (`file.folder` rechts vom letzten `/`).
- Index-Dateien immer `index.md`; werden in den meisten Queries explizit ausgeschlossen, weil sie Übersichten und keine Inhalte sind.
- Verknüpfungen werden als Markdown-Links erfasst und über `file.outlinks` / `file.inlinks` ausgewertet.
- Stub-Heuristik: weniger als 25 Zeilen oder fehlender `## Quellen`-Abschnitt oder Auftauchen unter „Offene Lücken" eines Index.

### Standardabfragen

#### 1. Bestandsübersicht je Kategorie

```dataview
TABLE length(rows) AS "Dateien"
FROM "" 
WHERE file.name != "index" AND file.name != "MEMORY" AND contains(file.folder, "reuse/research/")
GROUP BY split(file.folder, "/")[2] AS Kategorie
SORT Kategorie ASC
```

#### 2. Alle Dateien einer Entität mit Kurzdefinition

```dataview
TABLE file.link AS "Datei", L.text AS "Kurzdefinition"
FROM "bauteil"
WHERE file.name != "index"
FLATTEN file.lists AS L
WHERE contains(lower(L.section.subpath), "kurzdefinition") OR contains(lower(L.section.subpath), "kurzueberblick")
SORT file.name ASC
```

> Den `FROM`-Pfad pro Aufruf auf die gewünschte Entität setzen (`"material"`, `"pruefung"`, …).

#### 3. Stub-Detektor (kurze oder unvollständige Dateien)

```dataview
TABLE file.size AS "Bytes", length(file.lists) AS "Listenpunkte"
FROM "" 
WHERE file.name != "index"
  AND contains(file.folder, "reuse/research/")
  AND (file.size < 1500 OR !contains(file.outlinks, [[]]))
SORT file.size ASC
```

#### 4. Dateien ohne `## Quellen`-Abschnitt

```dataviewjs
const pages = dv.pages('"reuse/research"').where(p => p.file.name !== "index");
const ohneQuellen = [];
for (const p of pages) {
  const md = await dv.io.load(p.file.path);
  if (!md || !md.match(/^##\s+Quellen/m)) ohneQuellen.push(p);
}
dv.table(["Datei", "Kategorie"],
  ohneQuellen.map(p => [p.file.link, p.file.folder.split("/").pop()]));
```

#### 5. Verwaiste Dateien (kein eingehender Link)

```dataview
LIST file.inlinks
FROM "" 
WHERE file.name != "index"
  AND contains(file.folder, "reuse/research/")
  AND length(file.inlinks) = 0
SORT file.folder, file.name
```

#### 6. Querverweise zwischen zwei Entitäten

```dataview
TABLE file.outlinks AS "Verweise auf material/"
FROM "bauteil"
WHERE file.name != "index"
  AND any(file.outlinks, (l) => contains(l.path, "material/"))
SORT file.name ASC
```

#### 7. Quellen-Index (alle externen Links)

```dataviewjs
const pages = dv.pages('"reuse/research"').where(p => p.file.name !== "index");
const rows = [];
for (const p of pages) {
  const md = await dv.io.load(p.file.path);
  if (!md) continue;
  const urls = [...md.matchAll(/https?:\/\/[^\s)\]]+/g)].map(m => m[0]);
  for (const u of urls) rows.push([p.file.link, u]);
}
dv.table(["Datei", "URL"], rows);
```

#### 8. Offene Lücken aus allen Index-Dateien

```dataviewjs
const indizes = dv.pages('"reuse/research"').where(p => p.file.name === "index");
const lücken = [];
for (const p of indizes) {
  const md = await dv.io.load(p.file.path);
  if (!md) continue;
  const m = md.match(/##\s+Offene\s+L[üu]cken[\s\S]*?(?=\n##\s|$)/i);
  if (m) lücken.push([p.file.folder.split("/").pop(), p.file.link, m[0].split("\n").length - 1]);
}
dv.table(["Kategorie", "Index", "Zeilen unter ‚Offene Lücken'"], lücken);
```

#### 9. Bauteil → Material-Matrix (für `schema.sql`-Export)

```dataview
TABLE WITHOUT ID
  file.link AS "Bauteil",
  filter(file.outlinks, (l) => contains(l.path, "material/")) AS "Materialien"
FROM "bauteil"
WHERE file.name != "index"
SORT file.name ASC
```

#### 10. Aktivität der letzten zwei Wochen

```dataview
TABLE file.mtime AS "Zuletzt geändert"
FROM "" 
WHERE contains(file.folder, "reuse/research/")
  AND file.mtime >= date(today) - dur(14 days)
SORT file.mtime DESC
LIMIT 50
```

#### 11. Aufgaben aus inline-Tasks (Lückenpflege)

```dataview
TASK
FROM "" 
WHERE contains(file.folder, "reuse/research/") AND !completed
GROUP BY file.folder
```

### Anwendung

- Eine neue wiederkehrende Frage zuerst hier als Query verankern, statt sie ad hoc zu stellen.
- Queries als Codeblöcke direkt in das jeweilige `index.md` einer Entität einbetten ist erlaubt, der kanonische Ort bleibt aber diese Datei.
- Vor jedem Repo-Review (siehe [Recherche_Workflow.md](Recherche_Workflow.md)) mindestens Queries 1, 3, 4, 5 und 8 ausführen.

---

## Empfehlungen für das Repo

- **Frontmatter-Pflicht für Inhaltsdateien einführen.** Mindestfelder: `kategorie` (= Ordnername), `status` (`stub` | `entwurf` | `belegt` | `geprueft`), `quellen_geprueft` (Boolean), Listenfelder für Hauptbeziehungen (`materialien`, `bauteile`, `pruefungen`, `standards`, `akteure`). Damit fallen die Volltext-Workarounds in Queries 4 und 7 weg.
- **`status: stub` als Stub-Marker** statt der heuristischen Größenprüfung in Query 3.
- **Eine Query pro Frage, nicht pro Datei.** Sammlung dieser Queries ist verbindlich; Index-Dateien zitieren sie per Link, dupliziert wird nichts.
- **Konsistente Linkrichtung.** Verknüpfungen werden in der Datei der spezifischeren Entität gepflegt (z. B. `bauteil/Stuetze.md` linkt auf `material/Stahl.md`), so liefert `file.inlinks` an Materialien automatisch alle Bauteile.
- **Synchronität mit `schema.sql`.** Jede Query, die eine Beziehung auswertet (Query 6, 9), entspricht einer geplanten Tabelle oder View in [../schema.sql](../schema.sql). Beim Erweitern der einen Seite die andere mitziehen.
- **Dataview-JS sparsam.** DQL bevorzugen, JS nur dort, wo Volltext (Markdown-Body) gelesen werden muss. Sobald Frontmatter gepflegt ist, JS-Queries zurück auf DQL portieren.

---

## Quellen bzw. Bezugslogik

- Obsidian Dataview Plugin – Dokumentation: https://blacksmithgu.github.io/obsidian-dataview/
- Dataview Query Language Referenz: https://blacksmithgu.github.io/obsidian-dataview/queries/data-commands/
- Dataview JS API: https://blacksmithgu.github.io/obsidian-dataview/api/code-reference/
- Bezugslogik intern: Die Queries in diesem Dokument sind nicht erfunden, sondern leiten sich aus den real existierenden Abschnittsüberschriften der Index-Dateien (`## Verknüpfungen`, `## Zentrale Unterthemen`, `## Wichtige Dateien`, `## Offene Lücken`) und den real existierenden Verknüpfungsblöcken der Inhaltsdateien (`## Verknüpfungen`, `## Quellen`) ab. Jede Änderung an dieser Abschnittsstruktur (siehe [Recherche_Workflow.md](Recherche_Workflow.md)) muss hier nachgezogen werden.
