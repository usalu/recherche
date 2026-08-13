# Plan: Kompakte Darstellung der Akteurstabelle

Ordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\`
Renderer: `E:\recherche\_neo4j\netz\netz\render\latex\table_grid.py`

## 0. Ausgangslage, gemessen

    620 Knoten (440 kern · 180 bezug, darunter 78 Referenzprojekte)
    heutige Tabelle: 631 Zeilen/Überschriften auf 10 Seiten
    heutige Spalten: ID | Name | Typ | Rollen (ausgeschrieben)
    Nutzbreite:      181 mm      Kalibrierung: 0,2294 mm/Zeichen/pt

Was die Tabelle breit macht, sind zwei Textspalten:

| Feld | Median | p90 | Max |
|---|---|---|---|
| Name | 17 | 37 | 77 |
| Rolle(n) ausgeschrieben | 15 | 42 | 71 |
| Relevanz | 75 | 83 | 90 |

## 1. Der Hebel: die Taxonomie gruppiert sich bereits selbst

93 verschiedene Rollen kommen vor — ein Kürzel je Rolle wäre eine Legende mit 93
Einträgen, und die Verteilung hat einen langen Schwanz (die 30 häufigsten Rollen decken
nur 80 % der Nennungen). Rollenkürzel scheiden damit aus.

**Aber die Taxonomie ordnet ihre Rollen bereits in 15 Abschnitte A–O** (`Eigentum`,
`Regulierung`, `Planung`, `Inventarisierung`, `Prüfung`, `Rückbau`, `Aufarbeitung`,
`Logistik`, `Handel`, `Bauausführung`, `Betrieb`, `Daten`, `Methoden`, `Bildung`,
`Soziales`). Geprüft: **alle 93 vorkommenden Rollen mappen sauber**, einzige Ausnahme ist
`Referenzprojekt` (78×), das als **P** eine eigene 16. Klasse bildet.

    Rollenspalte:  "Bauteilinventarisierung / Selektiver Rückbau / Lagerung"   54 Zeichen
    Gruppencode:   "D·F·H"                                                      5 Zeichen

456 der 620 Knoten tragen ohnehin nur **eine** Rolle — für sie ist der Code **ein
Zeichen**. Die Legende hat 16 Zeilen statt 93 und ist inhaltlich schon geschrieben.

## 2. Was rechnerisch passt

Breitenbudget, mit derselben Kalibrierung wie die Bildplanung (0,2294 mm/Zeichen/pt):

| Layout | Breite | |
|---|---|---|
| heute: ID·Name52·Typ·Rollen ausgeschrieben | 177 mm | passt, aber voll |
| + Relevanz 90 Z. @6,2 pt, Name 40 | 216 mm | zu breit |
| + Relevanz 90 Z. @5,8 pt, Name 34 | 198 mm | zu breit |
| + Relevanz 90 Z. @5,4 pt, Name 34 | 184 mm | **knapp zu breit** |
| **ID·Name·Grad·Code, ohne Relevanz** | **104 mm** | **77 mm frei** |

Zwei Befunde:

1. **Die Relevanz passt in keiner Schriftgröße in dieselbe Zeile.** Auch bei 5,4 pt und
   auf 34 Zeichen gekürztem Namen fehlen 3 mm. Sie erzwingt entweder eine zweite Zeile
   (Seitenzahl verdoppelt sich) oder sie verlässt die Zeile.
2. **Ohne Relevanz bleiben 77 mm frei** — genug für eine zweite Spalte.

## 3. Empfehlung: zweispaltig, Rollen als Gruppencode

    Spalte: ID | Name (30 Z.) | Grad | Code        = 70,3 mm
    zwei Spalten nebeneinander + Bundsteg          = 146,6 mm   (von 181 mm)
    drei Spalten                                   = 223 mm     zu breit

**Ergebnis: 631 Zeilen auf ~5 statt 10 Seiten**, bei 34 mm Reserve für Bundsteg und
Trennlinie.

Grad als Glyphe statt Wort (`kern` → ●, `bezug` → ○) kostet 1 mm statt 8 mm und ist
isomorph zum bereits gedruckten Nachweisschlüssel D/P/— aus Anlage `nachweismatrix`.

Der Name auf 30 Zeichen trifft 110 von 620 Einträgen (18 %). Bei 34 Zeichen sind es 82
(13 %) — kostet 6 mm je Spalte, passt zweispaltig immer noch. **Empfehlung: 34.**

## 4. Wohin mit der Relevanz

Sie ist das Ergebnis der Klassifikationsarbeit und sollte nicht ersatzlos entfallen. Drei
Möglichkeiten, in dieser Reihenfolge sinnvoll:

1. **Eigener schmaler Anhangsblock, nur `kern`** (440 Einträge): zweispaltig
   `ID · Relevanz`, ca. 4 Seiten. Trennt die dichte Übersichtstabelle von der Begründung.
2. **Vollständig in die Reviewdatei**, im Bericht gar nicht gedruckt. Billigste Lösung,
   verschenkt aber den Kern der Recherche.
3. **Zweizeilige Zeile in der Haupttabelle** — verdoppelt die Seitenzahl auf ~20 und
   macht die Tabelle wieder unübersichtlich. Nicht empfohlen.

## 5. Zusätzlich: Überblicksmatrix vor der Tabelle

Eine 11 × 16-Matrix (Länder × Rollengruppen) fasst alle 620 Knoten auf **einer
Viertelseite** zusammen und beantwortet Fragen, die die Liste nicht beantwortet. Bereits
gerechnet:

```
      A   B   C   D   E   F   G   H   I   J   K   L   M   N   O   P
AT    6   1   4   2   .   2   1   .   8   .   .   3   .   1   3   3
BE    6   6   6   2   2   4   1   .  30   .   .   4   5   1   .   9
CH    7   4  23   4   1   9   4   4  21   1   .   6  13   8   .  10
DE   11   4  24   8   5   3   8   4  11   1   .   2  16  12   .  12
DK    1   .   5   3   1   7   3   1  15   .   .   .   2   1   .   5
FI    5   3   9   .   5   1   2   .   4   3   .   .  16   1   .   5
FR    7  12   6   4   4   4   3   .  51   1   .   .   .   1   .   5
GB    7   6  13   4   3   8   3   2  31   3   1   4   2   3   .  12
NL    8   4  18   5   1   4   4   2  24   1   1   5   4   4   .  12
NO    6   4   8   .   .   2   .   4  11   2   .   1   7   7   .   2
SE    8   1   3   4   3   2   1   5   9   1   .   4   2   6   .   3
```

Das ist bereits ein Ergebnis, kein Layout: Frankreich ist stark handelsgeprägt (I = 51),
Deutschland und die Schweiz planungs- und methodenlastig (C, M), **Spalte K (Betrieb) ist
europaweit fast leer (3 Nennungen)** — eine Lücke, die im Fließtext eine Aussage wert ist.

Als Punktraster oder Graustufenfeld gesetzt braucht die Matrix keine Zahlen und wird noch
kleiner.

## 6. Umsetzung

Alles in `table_grid.py`, kein neuer LaTeX-Mechanismus:

1. **Gruppenmapping** aus `KLASSIFIKATION_TAXONOMIE.md` ableiten (die `## A.`–`## O.`
   Abschnittsüberschriften + `### \`Rolle\``), als Konstante in `vocab.py` neben
   `ROLE_SHORT` ablegen. `Referenzprojekt` → `P`.
2. **Spalten umstellen** auf `ID | Name(34) | Grad | Code`, `X_*`-Offsets neu setzen.
3. **Zweispaltig paginieren**: `ROWS_PER_PAGE` bleibt 66, aber je Seite zwei Spalten —
   die Zeilenliste wird in Blöcke zu 132 geteilt und mit einem zweiten x-Offset gesetzt.
   Ländertrenner dürfen dabei nicht mitten in einer Spalte hängenbleiben.
4. **Legende** mit 16 Einträgen über `SemioGraphLegend`-Muster (existiert bereits).
5. **Matrix** als eigenes kleines Fragment, analog `programme_table.py`
   (`netz.cli matrix` → `figs/frag_matrix.tex`).
6. **Relevanzblock** nach Entscheidung aus Abschnitt 4.

Fragment danach wie gehabt nach
`E:\semio\mit-bestand\bericht\zwischenbericht\anhang\akteursnetz-tabellen.tex` kopieren,
Bericht einmal bauen, keine parallelen Builds.

## 7. Zu entscheiden

1. **Relevanz** — eigener `kern`-Block (empfohlen), nur Reviewdatei, oder zweizeilig?
2. **Namenslänge** 34 (13 % gekürzt, empfohlen) oder 38 (9 %, kostet 6 mm je Spalte)?
3. **Matrix** aufnehmen? Sie ersetzt keine Tabelle, sie erschließt sie.
