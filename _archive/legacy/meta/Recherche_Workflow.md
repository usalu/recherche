# Recherche Workflow

## Verknüpfungen

- [Entity_Schema.md](Entity_Schema.md) – jede neue Datei wird einer im Schema definierten Entität zugeordnet; ohne Schema-Eintrag keine Recherche.
- [Namenskonvention.md](Namenskonvention.md) – legt fest, wie Ordner, Dateien und Slugs heißen müssen, bevor der Workflow überhaupt beginnt.
- [Dataview_Abfragen.md](Dataview_Abfragen.md) – liefert die Audit-Queries, mit denen jede Workflow-Stufe überprüft wird (Stubs, fehlende Quellen, verwaiste Dateien, offene Lücken).
- [../AGENTS.md](../AGENTS.md) – Repo-Grundstruktur; jede Datei hier muss in dieses Schema einsortierbar sein.
- [../prompts.md](../prompts.md) – Vorlage für Deep-Research-Prompts (Software-Ökosystem, Norm, Akteurslandschaft); wird im Workflow als Eingabevorlage verwendet.
- [../schema.sql](../schema.sql) – Endziel: jede Inhaltsdatei muss in das relationale Schema überführbar sein.

---

## Zweck

Dieses Dokument beschreibt den tatsächlichen Arbeitsablauf, mit dem neue Themen ins Repo aufgenommen, Quellen gesichert, Inhalte zerlegt (Chunking) und Dateien dauerhaft gepflegt werden. Es ist explizit **kein** Best-Practice-Aufsatz, sondern eine Schritt-für-Schritt-Anleitung, die

- für Tiefenrecherche mit LLMs (Deep Research) reproduzierbare Eingabe und Ausgabe definiert,
- für Quellensicherung Belegpflicht und Speicherort regelt,
- für Chunking eine feste Abschnittsstruktur vorgibt,
- für Dateipflege wiederkehrende Aufräumläufe verankert.

Das Dokument richtet sich an Forschende, die direkt im Vault arbeiten, sowie an Agenten, die im Auftrag von Forschenden Dateien erzeugen oder ändern.

---

## Struktur / Regeln / Anwendung

### Stufe 1 – Thema einordnen (vor jeder Recherche)

1. Begriff bestimmen, ASCII-Slug bilden (siehe [Namenskonvention.md](Namenskonvention.md)).
2. Entitätsordner aus [Entity_Schema.md](Entity_Schema.md) wählen.
3. Prüfen, ob die Datei schon existiert: Volltextsuche im Vault + Dataview Query 1/2 aus [Dataview_Abfragen.md](Dataview_Abfragen.md).
4. Falls vorhanden: bestehende Datei erweitern, **keine** Zweitdatei. Falls nicht: weiter mit Stufe 2.
5. Wenn der Begriff in keine Entität passt, **nicht** spontan einen neuen Ordner anlegen, sondern zuerst [Entity_Schema.md](Entity_Schema.md) ergänzen.

### Stufe 2 – Datei anlegen

1. Datei am korrekten Ort mit korrektem Namen anlegen (`<entitaet>/<Slug>.md`).
2. Frontmatter aus [Entity_Schema.md](Entity_Schema.md) einsetzen, mindestens mit `kategorie`, `titel`, `slug`, `status: stub`, `quellen_geprueft: false`, `zuletzt_geprueft: <heute>`.
3. Pflichtabschnitte als leere Überschriften setzen:
   ```
   ## Verknüpfungen
   ## Kurzdefinition
   ## Relevanz für Wiederverwendung im Bauwesen
   ## Fachinhalt
   ## Praxisbezug / Beispiele
   ## Herausforderungen / offene Fragen
   ## Quellen
   ```
4. In den `## Verknüpfungen`-Block sofort die offensichtlichen Beziehungen zu anderen Entitäten eintragen (Material, Bauteil, Prüfung, Standard, Akteur, Fallstudie). Lieber drei Links zu viel als ein Link zu wenig.
5. Eintrag im `index.md` der Kategorie ergänzen: in „Wichtige Dateien dieser Kategorie" mit einer Zeile Kurzbeschreibung. Stubs gehören zusätzlich in „Offene Lücken / Ausbaufelder".

### Stufe 3 – Tiefenrecherche (Deep Research)

1. **Eingabe für das LLM**: Begriff, Entität, Beziehungsraum (welche anderen Dateien sind relevant), gewünschte Tiefe und Sprache. Vorlagen siehe [../prompts.md](../prompts.md). Prompt explizit auf Quellen mit URL und Erscheinungsjahr verpflichten.
2. **Drei Suchpfade parallel** (jeden mindestens einmal):
   - LLM-gestützte Synthese (Deep Research, ChatGPT/Claude/Gemini-Tools mit Suchfunktion). Ergebnis ist immer Entwurf, nie Beleg.
   - Forschungsdatenbanken: Google Scholar, ScienceDirect, CORDIS (EU-Forschung), TIB Hannover, Fraunhofer-Publikationen, BBSR-Publikationen.
   - Primärquellen: Norm-/Richtlinienverlage (DIN, VDI, ISO, Beuth), Behörden (UBA, BMBF, BMWSB), Branchenakteure (Concular, Madaster, ReCreate, FCRBE, Opalis, Rotor).
3. **Mindestumfang pro Datei**:
   - Bauteil/Material/Prüfung/Methode: ≥ 5 belegte Quellen, davon ≥ 1 Norm/Richtlinie und ≥ 1 Forschungsprojekt oder peer-reviewed Paper.
   - Standard/Recht: ≥ 1 Primärquelle (Originalnorm/-gesetz) ist Pflicht; ohne diese Quelle keine Statusänderung über `entwurf` hinaus.
   - Akteur/Projekt/Fallstudie: ≥ 1 offizielle Eigenpublikation (Website, Bericht) plus ≥ 1 unabhängige Quelle.
4. **Anti-Halluzinations-Regel**: Bevor eine Aussage in den Body übernommen wird, muss die zugehörige URL geöffnet und gelesen worden sein. Behauptungen ohne überprüfbaren Beleg werden im Body als „offene Frage" markiert und unter `## Herausforderungen / offene Fragen` aufgenommen, nicht als Faktum formuliert.

### Stufe 4 – Quellen sichern

1. Jede zitierte Quelle als Eintrag in `## Quellen` mit:
   - **Autor:in / Herausgeber:in**, **Jahr**, **Titel**, **Träger/Verlag** (falls vorhanden), **vollständige URL**, optional **Zugriffsdatum** in eckigen Klammern: `[abgerufen 2026-04-28]`.
   - DOI, wenn vorhanden, zusätzlich zur URL.
2. **Lokale Sicherung** großer oder zitierkritischer Dokumente (Berichte, Whitepapers, behördliche Veröffentlichungen): PDF in den zugehörigen Entitätsordner ablegen, gleicher Slug-Stamm wie die Markdown-Datei plus aussagekräftiges Suffix (`Stuetze_BBSR_2024_Reuse-Studie.pdf`). Pfad als relativer Link in `## Quellen` zusätzlich zur URL.
3. **Keine Hotlinks ohne URL.** Wenn nur ein PDF lokal liegt und kein Online-Pendant existiert, das in `## Quellen` ausdrücklich vermerken.
4. **Versionierung von Normen**: Erscheinungsjahr/Ausgabe der Norm (`DIN EN 206:2021-06`) zwingend nennen, weil Inhalte sich zwischen Ausgaben ändern.
5. **Interview/Workshop-Material**: kommt nicht direkt in `## Quellen`, sondern bekommt eine eigene Datei in `interview/` und wird von dort verlinkt.

### Stufe 5 – Chunking (Inhalt strukturieren)

Recherchierter Stoff wird **nicht** als Fließtext abgekippt, sondern entlang der Pflichtabschnitte zerlegt. Faustregeln:

- **`## Kurzdefinition`** – 3–8 Sätze. Beantwortet: was ist das, wofür im Reuse-Kontext relevant, welche Abgrenzungen.
- **`## Relevanz für Wiederverwendung im Bauwesen`** – ein bis zwei Absätze. Warum gehört das ins Repo, welcher Hebel für die Wiederverwendung.
- **`## Fachinhalt`** – mit `###`-Unterabschnitten gegliedert. Empfohlene Unterabschnitte je nach Entität: *Typische Vorkommen im Bestand*, *Relevante Eigenschaften*, *Demontagefähigkeit*, *Alterung und Schadensmechanismen*, *Prüfbedarf*, *Aufbereitung*, *Grenzen*, *Regulatorische Einordnung* (siehe als Vorlage [../material/Beton.md](../material/Beton.md)).
- **`## Praxisbezug / Beispiele`** – konkrete Projekte, Fallstudien, Akteure, Werkzeuge; jeweils mit Querverweis zu der entsprechenden Datei im Vault.
- **`## Herausforderungen / offene Fragen`** – Unsicherheiten, regulatorische Lücken, fehlende Daten. Nicht weglassen, weil hier die nächsten Recherche-Schritte abgelegt werden.
- **`## Quellen`** – siehe Stufe 4.

Längenrichtwerte: Inhaltsdatei zwischen 80 und 250 Zeilen Markdown. Größer → in Teildateien splitten und den ursprünglichen Slug zur Übersichtsseite machen.

### Stufe 6 – Vernetzung und Index pflegen

1. `## Verknüpfungen` der neuen Datei abschließend prüfen: alle in der Datei genannten Entitäten müssen verlinkt sein.
2. In den verlinkten Zielentitäten **nicht** rückwärts manuell verlinken – Backlinks erzeugt Obsidian, doppelte Pflege ist verboten.
3. `index.md` der eigenen Kategorie aktualisieren: Eintrag in „Wichtige Dateien", ggf. in „Zentrale Unterthemen", aus „Offene Lücken" entfernen, sobald Status > `stub`.
4. Querverbindungen zu anderen Kategorien: in `index.md` nur dann, wenn die Verbindung kategorial ist (nicht datei-spezifisch).

### Stufe 7 – Statuswechsel

`status:` im Frontmatter wandert nur in einer Richtung weiter, jeweils mit klarer Mindestbedingung:

| Status | Bedingung |
|---|---|
| `stub` | Datei existiert, Pflichtstruktur leer, ggf. Stichworte. |
| `entwurf` | Alle Pflichtabschnitte gefüllt, mindestens eine Quelle, `## Verknüpfungen` initial gesetzt. |
| `belegt` | Quellen-Mindestumfang aus Stufe 3 erreicht, jede zentrale Aussage mit Beleg. |
| `geprueft` | Zweitlesung durch eine zweite Person (oder explizit dokumentierter Selbst-Review nach ≥ 2 Wochen Abstand), `quellen_geprueft: true`, `zuletzt_geprueft` aktualisiert. |

### Stufe 8 – Wiederkehrende Pflege

- **Wöchentlich:** Dataview Query 3 (Stubs), 4 (fehlende Quellen), 10 (Aktivität) → in einem kurzen Eintrag im jeweiligen `index.md` unter „Offene Lücken" zusammenfassen.
- **Monatlich:** Dataview Query 5 (verwaiste Dateien), 8 (alle „Offene Lücken"-Abschnitte) → daraus eine priorisierte Aufgabenliste ableiten.
- **Bei Norm-/Rechtsänderungen:** alle Dateien mit Frontmatter-Feld `standards` oder `recht`, die den geänderten Eintrag enthalten, zurück auf `entwurf` setzen, bis nachgeprüft.
- **Halbjährlich:** Bestand der Top-Level-Ordner mit [Entity_Schema.md](Entity_Schema.md) abgleichen; jede Drift dokumentieren oder korrigieren.

### Stufe 9 – Temporäre Artefakte

- Ad-hoc-Skripte, Logs, Zwischenexporte und Prompt-Mitschnitte gehören **nicht** in den Vault. Wenn sie für einen konkreten Arbeitsschritt nötig sind, leben sie unter dem zugehörigen Ticket-Ordner (`.repo/🎫/YY/MM/DD/<slug>/`, vgl. CLAUDE.md), nicht unter `reuse/research/`.
- Debug-Notizen in Inhaltsdateien sind verboten. Wenn vorübergehend nötig, mit Marker `<!-- DEBUG: ... -->` und vor Statuswechsel zu `belegt` zwingend entfernen.

---

## Empfehlungen für das Repo

- **Recherche immer als Schleife denken, nicht linear.** Eine Datei wird mehrfach durchlaufen (Stub → Entwurf → Belegt → Geprüft); Workflow-Stufen 3–6 wiederholen sich, statt einmal komplett abgearbeitet zu werden.
- **Kein Inhalt ohne Quelle, keine Quelle ohne Inhalt.** Eine `## Quellen`-Liste, die nicht durch Aussagen im Body gedeckt ist, ist wertlos und wird beim Audit auffällig.
- **Stub bewusst zulassen.** Lieber 30 Stubs mit klaren Slugs und Verknüpfungen als 5 perfekte Dateien und 25 weiße Flecken im Beziehungsraum.
- **LLM-Output als Material, nicht als Wahrheit.** Jede Aussage aus Deep-Research-Tools wird gegen eine externe Primärquelle geprüft, bevor sie in den Body wandert. Halluzinierte Quellen sind erfahrungsgemäß die häufigste Fehlerklasse.
- **Eine Person, eine Aufgabe, ein Ticket.** Größere Recherchen werden in Tickets gebündelt (vgl. CLAUDE.md), damit Statuswechsel und Quellensicherung nachvollziehbar bleiben.
- **Dataview-Audits als festen Termin einplanen.** Ohne wiederkehrendes Audit verfällt jedes Wissensrepo zu einer Halde.
- **`schema.sql` regelmäßig regenerieren.** Spätestens, wenn sich Entitäten oder Beziehungen geändert haben. Damit bleibt das Repo migrierbar.

---

## Quellen bzw. Bezugslogik

- Bezugslogik intern: Der Workflow leitet sich aus der real existierenden Abschnittsstruktur der Inhaltsdateien ([../material/Beton.md](../material/Beton.md), [../bauteil/index.md](../bauteil/index.md), [../abbruchmethode/index.md](../abbruchmethode/index.md)) und den Repo-Vorgaben in [../AGENTS.md](../AGENTS.md) und CLAUDE.md ab. Quellenpflicht und Statusmodell folgen dem Anspruch von [../AGENTS.md](../AGENTS.md), aus dem Vault eine SQLite-Datenbank zu generieren.
- Methodische Bezüge zu Deep Research, Quellensicherung und Wissensrepo-Pflege:
  - DFG, „Leitlinien zur Sicherung guter wissenschaftlicher Praxis", insbesondere Leitlinien 7 (Quellen), 13 (Belegbarkeit), 17 (Archivierung): https://www.dfg.de/foerderung/grundlagen_rahmenbedingungen/gwp/
  - FAIR-Prinzipien für Forschungsdaten (Wilkinson et al. 2016, „The FAIR Guiding Principles for scientific data management and stewardship"): https://www.go-fair.org/fair-principles/
  - ALA / ACRL Framework for Information Literacy (Quellenkritik, Authority Is Constructed and Contextual): https://www.ala.org/acrl/standards/ilframework
  - „Deep Research" als Methode in LLM-Tools: Anthropic Claude Research, OpenAI Deep Research, Google Gemini Deep Research – jeweils Produktdokumentation der Anbieter, Stand 2025/2026.
- Spezifische Quellenarten der Bau-/Reuse-Domäne: CORDIS (EU-Forschung), BBSR/UBA-Publikationen, FCRBE-/Opalis-Dokumente, ReCreate-Projektmaterial, Concular-/Madaster-Whitepapers, DIN-/VDI-Normen – jeweils zitiert in den entsprechenden Inhaltsdateien (siehe `## Quellen` z. B. in [../material/Beton.md](../material/Beton.md)).
