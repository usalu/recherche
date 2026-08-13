# VERALTET — durch `HANDOFF_STRICT_SEMIO_FINAL.md` ersetzt

Dieser Handoff dokumentiert die Kantenprüfung vor dem harten Knoten-Cleanup.
Seine 859-Knoten-/477-Kanten-Renderzahlen sind nicht mehr aktuell. Für die
Semio-Übergabe gilt ausschließlich `HANDOFF_STRICT_SEMIO_FINAL.md`.

# Handoff: finaler LaTeX-Akteursgraph

Stand: 2026-08-13

## 1. Verbindlicher Umfang

Dieser Arbeitsstand betrifft **nur den LaTeX-Akteursgraphen**. Neo4j wurde nicht verändert
und darf aus diesem Handoff nicht stillschweigend aktualisiert werden. Der Ordnername
`_neo4j/` bezeichnet hier die vorhandene Graph-/LaTeX-Maschinerie, nicht einen autorisierten
Datenbank-Writeback.

Der Kantenplan ist abgeschlossen. Es gibt keine offene Beziehungsklassifikation.

## 2. Abgeschlossenes Ergebnis

- Geprüfte Kantenkandidaten: **570 von 570**.
- Validierte Ergebniszeilen: **570** in **34** Batches.
- Fehlende IDs: **0**.
- Doppelte IDs: **0**.
- Validatorverstöße: **0**.
- Behaltene und belegte Beziehungen: **477**.
- Entfernte Beziehungen: **93**.
  - **68** bloße Verzeichnis-/Katalogverknüpfungen.
  - **25** ohne Beleg für eine konkrete Beziehung.
- Keep und Remove sind disjunkt und ergeben exakt 570.
- Geprüfte Beleg-URLs: **220 von 220 erreichbar**.
- Jede der 570 Kanten hat genau eine Beziehungsart, Richtung und Kurzbeschreibung.
- Jede positive Kante hat URL und Belegzitat.

Wichtig: Die **88 bereits vor dieser Kampagne als `unklar` ausgeschlossenen Kanten** waren
nicht Teil der 570 Kandidaten.

## 3. Sichtbarkeits- und Löschregeln

### Kanten

- Alle **477** behaltenen Beziehungen werden im LaTeX-Fragment gezeichnet.
- Auch Zweierkomponenten bleiben sichtbar (`min_comp=2`).
- Verdeckte behaltene Beziehungen: **0**.
- Die **93** Kanten aus `prune_kanten_final.json` werden nicht gezeichnet.

### Knoten

- LaTeX-Länderpanels enthalten **859 sichtbare Knoten**.
- Darunter bleiben **354 isolierte Knoten sichtbar**. Das ist eine ausdrückliche
  redaktionelle Entscheidung; ein Folgeagent darf sie nicht automatisch ausblenden.
- Die **93 ausdrücklich freigegebenen Knotenentfernungen** aus
  `prune_faktencheck_final.json` sind aus den LaTeX-Panels ausgeschlossen.
- Kein Knoten aus dieser Entfernungsliste ist noch in einem Länderpanel vorhanden.

Die beiden Zahlen 93 sind zufällig gleich: Es handelt sich um zwei verschiedene Listen,
eine für Knoten und eine für Kanten.

## 4. Kassel-Korrektur

Der Quell-Snapshot ordnet sowohl `BauMaB Kassel / Bauteilbörse Kassel` als auch
`Stadt Kassel` fälschlich Belgien zu. Für den LaTeX-Graphen ist dies explizit korrigiert:

- BauMaB-EID: `4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:906` → `DE`
- Stadt-Kassel-EID: `4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:923` → `DE`
- Beziehungs-ID bleibt aus Provenienzgründen `BE:K075`.
- Die Beziehung ist `Trägerschaft` und bleibt belegt.
- Korrekturdatei: `latex_country_overrides.json`.
- Die Korrektur wirkt nur im LaTeX-Ladevorgang; Neo4j bleibt unverändert.

Nach der Korrektur enthält das Deutschland-Panel 84 Organisationen, 18 Projekte und
37 Beziehungen; Belgien enthält 90 Organisationen, 14 Projekte und 57 Beziehungen.
Die Review-Statistiken nach Land behalten dagegen ihre historischen Snapshot-IDs.

## 5. Kanonische Dateien

### Fachliche Ergebnisse

- `PLAN_kanten.md` — Regeln, Taxonomie und Abschlussstatus.
- `KANTEN_ABSCHLUSSBERICHT_FINAL.md` — konkrete Ergebnisse, Deutschland und alle
  93 Kantenentfernungen.
- `KANTEN_LATEX_AUDIT_FINAL.md` — maschinelle Endkontrolle.
- `kanten_klassifikation.json` — alle 570 vollständigen Entscheidungen.
- `keep_kanten_final.json` — 477 Kanten der Positivliste.
- `prune_kanten_final.json` — 93 entfernte Kanten.
- `kanten_konflikte.md` — 20 früher positiv bewertete, nach strengem Standard trotzdem
  entfernte Kanten.
- `kanten_review_inventory.json` — vollständiges Eingabeinventar mit Endpunkten.
- `kanten_source_recheck.json` — Erreichbarkeits- und Zitatabgleich der vorhandenen Quellen.
- `kanten_results/` — 34 validierte Ergebnistabellen.
- `latex_country_overrides.json` — zwei LaTeX-only Kassel-Korrekturen.

### LaTeX-Ausgabe

- `E:/recherche/_neo4j/netz/figs/frag_abb_netz.tex` — kanonisches Fragment,
  **477** `\SemioGraphEdge`-Aufrufe.
- `E:/recherche/_neo4j/netz/figs/akteursnetz_faktencheck_final.pdf` — kanonische,
  visuell geprüfte Vier-Seiten-PDF.

Nicht als kanonisch verwenden: `_akteursnetz_final.pdf`,
`KANTEN_ABSCHLUSSBERICHT.md` und `KANTEN_LATEX_AUDIT.md`. Diese Namen stammen aus einem
früheren Zwischenstand vor der Kassel-Korrektur. Die Dateien mit `_FINAL` beziehungsweise
`akteursnetz_faktencheck_final.pdf` ersetzen sie.

## 6. Aktive Codepfade

- `netz/sources.py` registriert Kanten-Prune und Länderkorrektur.
- `netz/cli.py::load_network()` vereinigt die bisherigen Ausschlüsse mit
  `prune_kanten_final.json` und lädt die Länderkorrektur.
- `netz/data/corrections.py` validiert die LaTeX-only Korrekturdatei.
- `netz/model/concepts.py::build_network()` wendet Länderkorrekturen vor der
  Länderpartition an.
- `netz/render/latex/graph_tikz.py` nutzt `min_comp=2`, damit Zweierbeziehungen sichtbar
  bleiben.
- `netz/render/latex/framing.py` sagt korrekt: `alle belegten Verbindungen`.
- `netz/tests/test_kanten_final.py` prüft die 477/93-Partition, vollständige
  Kantensichtbarkeit und Kassel im Deutschland-Panel.

## 7. Reproduzierbare Prüfung

Aus `E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck`:

```text
python validate_kanten.py
python merge_kanten.py
python finalize_kanten_report.py
```

Erwartet:

```text
570 eindeutige IDs
0 fehlend
0 doppelt
0 Regelverstöße
477 keep + 93 remove = 570
LaTeX model 477; fragment 477; hidden keep 0
```

Aus `E:/recherche/_neo4j/netz`:

```text
python -m unittest discover -s netz/tests -p "test_*.py"
python -m netz.cli abb
python build.py akteursnetz_faktencheck_final.tex frag_abb_netz.tex
E:/semio/.repo/cache/tectonic/0.16.9/tectonic.exe --keep-logs -Z search-path=E:/semio/print/tex --outdir E:/recherche/_neo4j/netz/figs E:/recherche/_neo4j/netz/figs/akteursnetz_faktencheck_final.tex
```

Letzter Testlauf: **14 Tests, alle bestanden**. Die PDF wurde danach auf allen vier Seiten
gerendert und visuell geprüft. Es gibt keine abgeschnittenen oder leeren Graphseiten.

Bekannte, nicht blockierende Build-Warnungen:

- Fontconfig findet keine Default-Konfiguration.
- eine `Underfull \hbox` um Zeile 192 des zusammengesetzten Dokuments;
- BibTeX meldet in diesem graph-only Dokument Warnungen ohne Auswirkung auf die PDF.

## 8. Prüfsummen des Abschlussstands

```text
4f84570be5a6e5c350ce187c6dff172dc4d71373946002a10b74c726cf26d6a0  keep_kanten_final.json
9f157e0216a3870d794e6d1aaa96558fd6e062495f310a1cefc42472bb0fdcd2  prune_kanten_final.json
fdf14a01615bccb7f75a97151c87e7b251c7b1e58dcef20118d0b1a5fdcaf7e6  kanten_klassifikation.json
e508d911e63811ed16008e874361a1104526e52558a15b8cd40113ed997ded92  latex_country_overrides.json
28fbbdd22af8bc5895c9ae1d5e9efc5257347f3e21d7bb352dbb6f77bbd19bc9  frag_abb_netz.tex
fd20af47c61501e574b5f18349c0328016a0776660a2d2751388c588db9369a4  akteursnetz_faktencheck_final.pdf
```

Wenn einer dieser Inputs bewusst geändert wird, müssen Fragment, PDF, Abschlussberichte
und Prüfsummen gemeinsam neu erzeugt werden.

## 9. Was noch offen ist

Für den Kantenplan: **nichts**. Es gibt keine wartende Entscheidung und keine versteckte
behaltene Beziehung.

Mögliche Folgearbeit liegt außerhalb dieses abgeschlossenen Auftrags:

1. das kanonische Fragment in die vollständige Hauptpublikation integrieren und den
   Gesamtbericht bauen;
2. die falsche Kassel-Länderangabe später in ihrer eigentlichen Datenquelle korrigieren,
   aber nur mit neuer ausdrücklicher Autorisierung;
3. den fertigen Stand gezielt versionieren/committen.

## 10. Arbeitsbaum-Sicherheit

Der Git-Arbeitsbaum enthält weitere, teilweise schon vorher vorhandene Änderungen,
insbesondere aus der Bild-/Pilotarbeit. Ein Folgeagent darf **keinen pauschalen Reset oder
Checkout** ausführen. Nur die konkret zum Kanten-/LaTeX-Abschluss gehörenden Dateien sollen
gezielt ausgewählt werden. Es wurde in diesem Lauf weder gestaged noch committed.
