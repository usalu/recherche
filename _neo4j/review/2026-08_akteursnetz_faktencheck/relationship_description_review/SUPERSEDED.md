# Dieser Ordner ist historisch

`approval_manifest.json` sagt weiterhin `approved_for_apply: false`, weil
dieser exakte 570-Datensatz-Stand nie durch das Hash-Freigabetor bestätigt
wurde. Der Auftraggeber hat stattdessen direkt entschieden ("ok fix", "cut
the two", spätere Einzelentscheidungen) und die Kürzung wurde per Hand in
`kanten_klassifikation.json` angewendet — mit Korrekturen, die über die
ursprünglichen 570 Vorschläge hinausgehen (98 statt 94 gelöscht, 25 zusätzliche
Nachbesserungen an gebrochenen Sätzen, Franck/Franck-Bricks-Zusammenführung).

`proposals.json`, `README.md`, `FLAGGED_DECISIONS.md` und `batches/` zeigen
den **Stand vor** dieser Nachbesserung. Für den tatsächlich angewendeten
Stand: `kanten_klassifikation.json` selbst, plus
`kanten_klassifikation.json.bak-vor-kuerzung` /
`.bak-vor-nachbesserung` für die Vorstufen.

Maßgeblich: **472** Beziehungen (98 gelöscht), Art-Spalte entfernt,
**264** gezeichnete Kanten, **618** Knoten (Franck/Franck Bricks gemergt).
