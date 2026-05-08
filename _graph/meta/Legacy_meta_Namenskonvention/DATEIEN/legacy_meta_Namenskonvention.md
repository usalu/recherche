# Namenskonvention

## Verknüpfungen

- [Entity_Schema.md](Entity_Schema.md) – legt fest, welche Ordnernamen überhaupt zulässig sind (jede Entität = ein Top-Level-Ordner); diese Datei regelt nur die Schreibweise.
- [Recherche_Workflow.md](Recherche_Workflow.md) – beim Anlegen jeder neuen Datei greifen die hier definierten Regeln; der Workflow setzt sie als Eingabebedingung voraus.
- [Dataview_Abfragen.md](Dataview_Abfragen.md) – fast jede Query verlässt sich auf konsistente Ordner- und Dateinamen; jede Abweichung von dieser Konvention bricht Filter still.
- [../AGENTS.md](../AGENTS.md) – Repo-Grundregel „ENTITÄT → ID → `index.md` + Dateien" wird hier konkretisiert.
- [../schema.sql](../schema.sql) – `slug` (= Dateiname ohne `.md`) ist Primärschlüssel; die hier festgelegten Slug-Regeln definieren damit zugleich die DB-IDs.

---

## Zweck

Die Namenskonvention sichert maschinelle Lesbarkeit und Plattformportabilität (Windows + macOS + Linux + Git + SQLite + Obsidian) bei gleichzeitig deutschsprachigen Inhalten. Sie verhindert die zwei häufigsten Bruchquellen in Markdown-basierten Wissensrepos: kollidierende Schreibweisen für denselben Begriff (Stütze / Stuetze / Stuetzen / stütze.md) und nicht-portable Sonderzeichen in Pfaden. Außerdem ist sie die Voraussetzung dafür, dass `slug` als stabiler Schlüssel für die spätere SQLite-Migration funktioniert.

---

## Struktur / Regeln / Anwendung

### Grundprinzipien

1. **Sprache:** Inhalt deutsch, Bezeichner ASCII-deutsch (Umlaute transkribiert).
2. **Eindeutigkeit:** Ein Begriff hat genau einen Ordner und genau einen Dateinamen. Synonyme werden im Body als Aliasse genannt, nicht als Zweitdatei angelegt.
3. **Stabilität:** Slugs werden nicht umbenannt, sobald sie verlinkt sind. Korrekturen erfolgen über Aliasse oder Frontmatter-`titel`, nicht über Dateiverschiebung.
4. **Tool-Freundlichkeit vor Eleganz:** Lieber `Brettschichtholzstuetze.md` als `Brettschichtholz‑Stütze.md`.

### Transkription Umlaute / ß

Verbindlich für **alle** Pfadbestandteile (Ordner und Dateinamen), Frontmatter-`slug` und alle internen Markdown-Links:

| Original | Transkription |
|---|---|
| ä / Ä | ae / Ae |
| ö / Ö | oe / Oe |
| ü / Ü | ue / Ue |
| ß | ss |

Anwendungsbeispiele: `Stütze` → `Stuetze`, `Träger` → `Traeger`, `Gebäude` → `gebaeude`, `Hürde` → `huerde`, `Förderprogramm` → `foerderprogramm`. **Im Markdown-Body** (Überschriften, Fließtext, `titel`-Frontmatter) werden Umlaute normal geschrieben.

### Ordnernamen (Entitäten)

- ASCII-Kleinbuchstaben, keine Sonderzeichen, keine Leerzeichen.
- Singular, deutsch (`bauteil`, nicht `bauteile`; `material`, nicht `materialien`).
- Mehrteilige Begriffe als ein Wort, ohne Trenner (`aufbereitungsmethode`, `leistungsanforderung`, `tragwerkssystem`, `reuse_strategie` als einzige Ausnahme mit Underscore wegen Lesbarkeit der Komposita aus zwei Wortstämmen).
- Eine Entität = ein Ordner. Keine Doppelablagen, keine Synonym-Ordner.

### Dateinamen (Instanzen)

- ASCII, transkribierte Umlaute (s. o.).
- **PascalCase mit Unterstrich als Wortgrenze** für mehrteilige Begriffe: `Selektiver_Rueckbau.md`, `Brettschichtholzstuetze.md`, `Lysbuechel_Parkhaus.md`, `DIN_EN_206.md`.
- Endung immer `.md`.
- Keine Leerzeichen, keine Bindestriche, keine Punkte außer vor `.md`.
- Keine Datums- oder Versionssuffixe im Dateinamen (Versionierung übernimmt Git, Status übernimmt Frontmatter).
- Index einer Kategorie heißt immer `index.md` (Kleinbuchstaben).
- Akronyme/Normenkennungen bleiben in Großbuchstaben und werden mit Unterstrich abgesetzt: `DIN_EN_206.md`, `VDI_6210.md`, `ISO_19650.md`.

### Frontmatter-`slug`

- Identisch zum Dateinamen ohne `.md`.
- Wird in [../schema.sql](../schema.sql) als Primärschlüssel verwendet.
- Bei Konflikt zwischen Dateiname und Frontmatter-`slug` gilt: Datei umbenennen, nicht Slug ändern.

### Frontmatter-`titel`

- Lesetitel mit Umlauten und Leerzeichen (`titel: "Stütze"`, `titel: "DIN EN 206 – Beton"`).
- In Anführungszeichen, wenn Sonderzeichen oder Leerzeichen enthalten.
- Wird in Index-Auflistungen statt des Dateinamens angezeigt.

### Überschriften im Markdown

- `#` einmalig pro Datei für den Dateititel (mit Umlauten); für Inhaltsdateien optional, weil der Titel über Frontmatter geliefert wird.
- `##` für die Pflichtabschnitte gemäß [Entity_Schema.md](Entity_Schema.md) (`## Verknüpfungen`, `## Kurzdefinition`, …). Wortlaut der Pflichtabschnitte ist exakt einzuhalten – Dataview-Queries matchen darauf.
- `###` für Unterkapitel im Fachinhalt.
- Kein `####` und tiefer; bei Bedarf in eine neue Datei aufteilen.
- Wenn Emoji-Marker für Sektionen verwendet werden (vgl. CLAUDE.md), dann an den Anfang der Überschrift, ein Emoji, eindeutig pro Sektion (`## 🔖 Verknüpfungen`). Anwendung optional, aber dann konsistent über alle Dateien einer Kategorie.

### Verlinkung

- **Intern, im selben Vault:** relative Markdown-Links, nicht Wiki-Links. Beispiele:
  - Datei → Datei in derselben Kategorie: `[Stuetze.md](Stuetze.md)`
  - Datei → Datei in anderer Kategorie: `[material/Beton.md](../material/Beton.md)`
  - Datei → Index einer Kategorie: `[bauteil/](../bauteil/)`
- **Externe Quellen:** vollständige `https://`-URLs mit beschreibendem Linktext oder als bibliographischer Eintrag im `## Quellen`-Block.
- Linkziele immer mit ASCII-Pfad (s. o.).

### Identifikatoren außerhalb des Vaults

- **Ticket-IDs** (vgl. CLAUDE.md): `YYYY/MM/DD/TICKETSLUG`, Slug in Kebab-Case (`2026/04/28/meta-files-fill`). Tickets liegen unter `.repo/🎫/`, nicht im Vault.
- **Goal-IDs:** `goalslug/subgoalslug/...`, Kebab-Case.
- **Titel** (Tickets, Goals, Berichte): Title Case, niemals Slug, niemals ALL CAPS, niemals reine Kleinschreibung. Beispiel: „Meta-Dateien Vervollständigen", nicht „meta-dateien vervollständigen" und nicht „META-DATEIEN VERVOLLSTÄNDIGEN".

### Verbotenes / Anti-Beispiele

| Falsch | Richtig | Begründung |
|---|---|---|
| `Stütze.md` | `Stuetze.md` | Umlaut im Pfad |
| `stuetze.md` | `Stuetze.md` | Falsche Groß-/Kleinschreibung; Konflikt auf Case-insensitive-FS |
| `Brettschichtholz Stütze.md` | `Brettschichtholzstuetze.md` | Leerzeichen im Pfad, Umlaut |
| `bauteile/` | `bauteil/` | Plural |
| `case_studies/` | `fallstudie/` | Englisch |
| `Lysbüchel-Parkhaus_v2.md` | `Lysbuechel_Parkhaus.md` | Bindestrich + Umlaut + Versionssuffix |
| `DIN-EN-206.md` | `DIN_EN_206.md` | Bindestriche statt Unterstrich |
| `material/Beton/index.md` (zweite Ebene) | `material/Beton.md` | Doppelte Ordnerschachtelung |

### Anwendung auf bestehende Dateien

- Beim Bearbeiten einer bestehenden Datei wird die Konvention soft durchgesetzt: Frontmatter ergänzen, interne Verlinkungen normalisieren, Überschriften-Wortlaut prüfen. Datei wird nur dann umbenannt, wenn die alte Schreibweise objektiv falsch (Umlaut im Pfad, Plural, Sprachwechsel) und Bestandsverlinkung gering ist.
- Bei größeren Umbenennungen: Pflicht zur Aktualisierung aller eingehenden Links (`file.inlinks`-Audit per Dataview, Query 5 in [Dataview_Abfragen.md](Dataview_Abfragen.md)).

---

## Empfehlungen für das Repo

- **Konvention prüfen, bevor eine Datei angelegt wird, nicht danach.** Faustregel: kann der Pfad in einer Bash-Pipeline ohne Quotes stehen, ist er korrekt.
- **Slug = Dateiname**, ausnahmslos. Frontmatter-`slug` ist Sicherungskopie für die SQL-Migration, nicht Alternative.
- **Aliasse statt Zweitdateien.** Wenn „Brettschichtholzstütze" auch unter „BSH-Stütze" gesucht wird, gehört das in `aliases:` im Frontmatter, nicht in eine zweite Datei.
- **Eine Datei pro Begriff, eine Überschriftshierarchie pro Datei.** Bei Wachstum aufteilen, nicht durch tiefere Heading-Levels lösen.
- **Linter einführen.** Sobald Frontmatter durchgängig ist, lohnt ein kleines Skript (Python/PowerShell), das Datei- und Slug-Regeln mechanisch prüft. Bis dahin: Query 1, 2 und 5 aus [Dataview_Abfragen.md](Dataview_Abfragen.md) als Sichtprüfung.
- **Umbenennungen sind Refactorings.** Sie gehören in einen eigenen Ticket-Schritt mit Link-Update, nicht nebenher in einen inhaltlichen Edit.
- **Sprachgrenze respektieren.** Inhalt deutsch, Bezeichner ASCII-deutsch, externe Standards in deren Originalbezeichnung (`DIN_EN_206`, nicht `DIN_EN_Beton`).

---

## Quellen bzw. Bezugslogik

- Bezugslogik intern: Die Regeln sind aus dem realen Stand der Top-Level-Ordner und der Inhaltsdateien abgeleitet. Auswertung u. a. von [../bauteil/](../bauteil/), [../material/](../material/), [../abbruchmethode/](../abbruchmethode/), [../gebaeude/](../gebaeude/) (durchgängig PascalCase mit Unterstrich, Umlaute transkribiert, Singular-Ordner).
- Vorgabe Repo-Grundstruktur: [../AGENTS.md](../AGENTS.md).
- Ticket- und Goal-Konvention: CLAUDE.md im Repo-Root.
- Externe Referenzen für die portablen Pfadregeln:
  - POSIX Portable Filename Character Set (IEEE Std 1003.1, 3.282) – `[A-Za-z0-9._-]`.
  - Microsoft, „Naming Files, Paths, and Namespaces" – Verbot bestimmter Zeichen unter Windows: https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file
  - Git, Hinweise zur Case-(In)Sensitivity der Arbeitsbäume: https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreignoreCase
  - Obsidian Help, Linkformate und interne Pfade: https://help.obsidian.md/Linking+notes+and+files/Internal+links
