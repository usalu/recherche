# Entscheidungen: Knotenlogos, Dunkelbild und Prüfdokumente

**Stand:** 2026-08-16 · Gilt für den Akteursnetz-Anhang.

**Nachtrag 2026-08-19:** der Anhang steht inzwischen im **Forschungsbericht**,
nicht mehr im Zwischenbericht (`netz/sources.py:report_anhang_root`
entsprechend umgestellt). Nach der Beziehungstext-Kürzung und der
Franck/Franck-Bricks-Zusammenführung: **618 Knoten, 264 gezeichnete Kanten**
(vorher 619/268) — Zahlen unten, die das noch als 619/268 nennen, beschreiben
den damaligen Stand ihrer jeweiligen Messung, nicht mehr den aktuellen.

Dieses Dokument hält fest, **was entschieden ist und warum**. Wer hier etwas
ändert, ändert eine bereits getroffene Entscheidung — dann bitte die Begründung
mit ändern, nicht nur den Wert. Mehrere dieser Punkte waren schon einmal
korrekt und sind später still wieder zurückgefallen; die Begründungen stehen
deshalb auch als Kommentar im Code, wo der jeweilige Wert gesetzt wird.

## Nachtrag 20.08.2026: Dauer der aktuellen Beziehungen

Die Dauer wurde für die **264 tatsächlich gezeichneten Kanten** einzeln gegen
den gespeicherten Beleg geprüft; die alte 268-Zeilen-Tabelle war nur pauschal
aus der Beziehungsart abgeleitet und ist historisch. Aktueller Stand:

- 40 dauerhaft
- 32 befristeter Verbund
- 173 projektgebunden
- 19 einmalig
- 0 unklar

Maßgeblich sind die `dauer_*`-Felder in `kanten_klassifikation.json`. Der
vollständige Bericht mit Begründung und Quelle je Kante steht in
`KANTEN_DAUER_FINAL.md`, `kanten_dauer_final.csv` und
`kanten_dauer_final.json`. Fünf dabei sichtbare Typkonflikte wurden korrigiert;
die früheren Werte bleiben direkt an den betroffenen Kanten als Provenienz
erhalten. Die LaTeX-Tabelle `Akteursbeziehungen` zeigt die Klassifikation in
der Spalte `Beziehungsdauer`.

Die Graph-Topologie bleibt 618/264; kein Neo4j-Schreibzugriff.

---

## 1. Deckkraft: immer 100 %, nie 50 %

Bei 50 % mischt sich jede Marke mit dem Seitenhintergrund. Dadurch sieht
dieselbe Marke im Hell- und im Dunkelbild **verschieden eingefärbt** aus, und
kräftige Markenfarben werden matt.

Der Wert wird in die Assets **eingebrannt** — er lässt sich nachträglich nur
durch komplettes Neurendern korrigieren.

Zwei Stellen hatten `50` als Vorgabewert und haben den Fehler nach jeder
Korrektur erneut eingeschleppt. Beide stehen jetzt auf `100`:

- `accept-suggestions --opacity` (Argparse-Default)
- `command_current_finalize` (`review.get("logo_opacity_percent", 100)`)

Der **Deckkraftregler der Reviewgalerie** ist davon unabhängig. Er ist reine
Ansichtssache und darf nicht in die Assets durchschlagen.

**Prüfung:** ein fertiges Asset muss `max(alpha) == 255` haben. 128 bedeutet
50 % und ist ein Fehler.

## 2. Beschnitt: Hintergrund verlängern, Marke nie abschneiden

Der frühere `circle_cover` skalierte formatfüllend und schnitt den Überschuss
weg — bei breiten Wortmarken hat das die Marke zerschnitten (BOBI Réemploi,
Van der Wal).

Stattdessen `circle_extend`: die Marke wird so weit verkleinert, dass sie
vollständig in den Kreis passt, und der **vorhandene Kachelhintergrund wird
nach außen verlängert**, bis der Kreis wieder randlos gefüllt ist. Der
Kachel-Look bleibt, die Marke bleibt vollständig.

**Maßgeblich ist allein die Marke** — Schrift, Bildzeichen, Icon. Der
Hintergrund zählt nicht mit. Eine quadratische Kachel darf nicht um √2
schrumpfen, nur damit ihre farbigen *Ecken* in den Kreis passen. Genau dafür
gibt es die Vordergrunderkennung (`_dense_foreground`); sie ist kein Beiwerk,
sondern der Kern.

Kein Schrumpflimit: auch sehr breite Wortmarken werden vollständig eingepasst.
Bei 4,55 mm Knotendurchmesser sind sie ohnehin nicht lesbar — die Marke bleibt
aber unversehrt und der Kreis voll.

## 3. Kein durchsichtiger Ring in der Scheibe

Bei den vollflächigen Modi (`circle_cover`, `circle_extend`, `light_backdrop`)
muss die Scheibe bis zum Rand **deckend** sein.

`is_opaque_tile` zählte früher `alpha > 24` und hat damit einen weichen
Schlagschatten als „gefüllt" mitgezählt. Cover-Crop machte daraus eine Scheibe
mit durchsichtigem Ring. Der Test verlangt jetzt zusätzlich echte Deckung
(≥ 0,80 der Fläche mit `alpha >= 250`). Gemessen über alle damals angenommenen
Kacheln: der Fehlerfall lag bei 0,638, der nächstniedrigere echte Fall bei
0,888 — 0,80 liegt in der leeren Lücke dazwischen.

`inner_disc_min_alpha` prüft das dauerhaft in `validate_final_manifest`.

## 4. Kandidat muss überhaupt sichtbar sein

Eine SVG, deren Füllung an CSS oder einer Maske hängt, rastert gelegentlich zu
einem praktisch leeren Bild. `NL:U30` lieferte so ein `logo.svg` mit
Maximalalpha 30, stand als `header_logo` in der Rangfolge über vier
einwandfreien offiziellen Icons desselben Hauses und lief unbemerkt bis in
einen bereits visuell abgenommenen Identitätsaudit durch — im Knoten war
schlicht nichts zu sehen.

`candidate_rejection` verwirft jetzt jede Vorschau mit `max(alpha) < 250`.

**Maximalalpha, nicht Deckungsanteil.** Über alle angenommenen Logos liegt das
Maximum 524-mal bei exakt 255 und einmal bei 30 — sauber trennbar. Der
Deckungsanteil fällt bei dünnen Wortmarken legitim bis 0,009 und taugt nicht
als Grenze.

## 5. Dunkelbild: nur eingreifen, wo Inhalt wirklich verschwindet

Betroffen sind nur `safe_contain` und `neutral_knockout` — die anderen Modi
malen eine deckende Scheibe, die Marke sitzt dort auf ihrem eigenen Grund.

Marken mit **gesättigter, aber dunkler Eigenfarbe** (Navy, Tannengrün) fasst
die Theme-Umfärbung absichtlich nicht an, sonst ginge die Markenfarbe verloren.
Für sie gibt es `dark_backdrop_overrides.json` → `light_backdrop`: eine feste
helle Scheibe hinter der Marke, ein Ergebnis für beide Themes.

**Nicht überanwenden.** Gesättigtes Rot oder Blau liest sich auf Fast-Schwarz
gut. Umgestellt wird nur, wo tatsächlich *Inhalt ausfällt* — etwa wenn eine
Wortmarkenhälfte auf weißem Träger steht und ohne ihn wegfällt, oder eine
dünne Kontur im Grund versinkt.

Die Messung (Anteil der sichtbaren Pixel unter Luma 70 im Dunkelrender) ist
**nur ein Suchfilter, keine Entscheidung**. Sie hat 25 Kandidaten gemeldet,
davon waren rund 9 echte Fälle. Vor jeder Aufnahme in die Overrides das
gerenderte Bild ansehen.

Jeder Eintrag trägt seinen gemessenen Wert **und** einen Satz dazu, was genau
im Dunkelbild ausfällt.

Bekannt und akzeptiert: die Trägerfläche hinter der Knoten-ID dämpft im
Dunkelbild auch eine helle Scheibe zu Grau. Das ist ein alter Zielkonflikt
zwischen ID-Lesbarkeit und Markenfarbe, kein neuer Fehler.

## 5a. `light_backdrop` hat einen zweiten Zweck: Zweiton-Marken retten

Die Neutral-Tokenisierung färbt neutrale Anteile in die Themefarbe um. Trifft
sie **beide** Töne einer Marke, fällt der Kontrast zwischen ihnen weg.

Gefährlich ist genau ein Muster: eine gefüllte dunkle Form mit **ausgespartem
hellem Zeichen darin** — Bellastocks schwarze Scheibe mit weißem BS-Monogramm,
Houtenplatens HP im Kreis, Nomols Wortzeichen, Labrouches Strichzeichnung.
Übrig blieb jeweils eine konturlose Fläche bzw. ein Balken. `light_backdrop`
erhält die Aussparung und liest sich in beiden Themes.

**Unterscheidungsmerkmal: berührt das Weiß den Bildrand?**
Ein weißer *Hintergrund* berührt ihn und wird zu Recht entfernt — die Marke
bleibt als eine Tintenfarbe übrig, eine Helligkeitsspanne nahe null ist dort
das gewünschte Ergebnis (TU Delft, AIX Arkitekter, PLP und viele mehr). Ein
*innenliegendes* Weiß berührt ihn nicht und trägt die Aussage.

Ohne diese Unterscheidung meldet eine reine Spannenmessung 71 Fälle, von denen
die allermeisten korrekt sind; mit ihr bleiben 15, von denen sich beim Ansehen
4 als echt herausstellten. Auch hier gilt Abschnitt 9: die Messung sucht, das
Auge entscheidet.

## 6. Sperrlisten sperren die Datei, nicht den Akteur

`MANUAL_CANDIDATE_REJECTIONS` mit `{"*": ...}` sperrt einen Knoten komplett.
Das war jeweils richtig, solange nur ein untauglicher Kandidat vorlag — und
wurde falsch, sobald eine spätere Recherche die echte Marke fand: die pauschale
Regel hätte dann nur noch die *richtige* Datei blockiert.

Regel: die konkrete untaugliche Datei sperren, bevorzugt über
`MANUAL_CANDIDATE_URL_REJECTIONS` (URL-Fragment, überlebt einen ID-Wechsel bei
der nächsten Ernte). `{"*"}` nur, solange wirklich nichts Brauchbares existiert.

`MANUAL_DOMAIN_REJECTIONS` benennt eine **Fremddomain**. Bekommt der Knoten
später die richtige Domain zugeordnet, ist der Eintrag gegenstandslos und muss
weg — sonst sperrt er eine inzwischen korrekte Quelle. So geschehen bei
`GB:U44` (opera.com, der Browser → operapm.co.uk) und `DK:U02` (gain.de, das
deutsche GAIN → again.dk).

Wenn ein Test auf eine solche Sperre anschlägt: erst prüfen, ob die Sperre
oder die Daten veraltet sind. Nicht reflexhaft den Test anpassen.

## 7. Fragmente immer mit `--images-manifest` erzeugen

Das Flag hat **bewusst keinen Vorgabewert** — der bildlose Kontrolllauf lebt
davon, dass es fehlt. Ein Lauf ohne das Flag erzeugt daher klaglos Fragmente
**ganz ohne Logos** und der Bericht druckt leere Knoten, ohne dass etwas
fehlschlägt.

```
python -m netz.cli abb          --images-manifest <manifest>
python -m netz.cli tables-grid  --images-manifest <manifest>
python -m netz.cli sync-fragments
```

**Gegenprobe nach jedem Lauf:** `grep -c 'image=' akteursnetz-figuren.tex` und
`grep -c 'SemioLogoFit' akteursnetz-tabellen.tex` müssen dieselbe, plausible
Zahl liefern. 0 bedeutet: Flag vergessen.

## 8. Das Rendermanifest kommt aus dem aktuellen Audit

Der Bericht zeichnet das **aktuelle 619-Knoten-Netz**;
`final_image_manifest.json` beschreibt die eingefrorene **762er
Transportauswahl**. Das deckt sich fast, aber nicht ganz: Knoten, die es im
aktuellen Netz gibt und in der Auswahl nicht, fehlten im Bericht, obwohl ihr
Logo geprüft war.

Deshalb `build_report_manifest.py` → `bilder_full/report_image_manifest.json`,
abgeleitet aus `CURRENT_LOGO_IDENTITY_AUDIT.json`. Nach jedem
`current-finalize` neu erzeugen und die drei `netz.cli`-Aufrufe darauf zeigen
lassen.

`cc/tid` wird zum Dateinamen im Bericht — das Skript bricht bei einer Kollision
ab, weil zwei Knoten auf denselben Namen ein stiller Überschreibfehler wäre.

## 9. Prüfen heißt ansehen

- **Rendern und hinsehen.** Kein Befund ohne Bild. Mehrere „Fehler" in diesem
  Verlauf waren nach Ansicht des Quellbilds echtes Markendesign.
- **Bytevergleich gegen PDF-eingebettete Bilder ist ungültig.** Tectonic/XeTeX
  kodiert Rasterbilder beim Einbetten neu; Hashes stimmen auch bei identischem
  Inhalt nicht. Direkt rendern (PyMuPDF) und ansehen.
- **`tid` im Netz ≠ `tid` im Manifest.** Das aktuelle Netz nummeriert neu.
  Wer einen Knoten im PDF sucht, muss über die **`eid`** abbilden — sonst
  prüft man den falschen Knoten. Ist genau so passiert.
- **Nach `finalize` gegenprüfen**, welche Assets sich geändert haben
  (`{key: sha256}` vorher/nachher). Jede Änderung muss erklärbar sein.
- **Das Prüfwerkzeug selbst prüfen.** Die Kontaktbögen der Tiefenprüfung
  malten jede Marke auf Schwarz, weil `.convert("RGB")` den Alphakanal
  wegwirft — bei `safe_contain` und `neutral_knockout` ist das die gesamte
  Umgebung. Dunkle Marken waren dort unsichtbar, obwohl im Knoten alles
  stimmte. Wer nach so einem Bogen urteilt, verwirft gute Logos und übersieht
  schlechte. Transparenz immer auf die Zielfläche komponieren
  (`alpha_composite`), nie `convert`.

## 10. Prüfdokumente: kompakt, Klarnamen, voller Wortlaut

`TEXTPRUEFUNG_*` dienen allein der Beurteilung der **Formulierung**:

- Akteure: `Akteur; Rolle; Relevanz`
- Kanten: `Von; Nach; Beschreibung`

Klarnamen statt Codes. Keine IDs, Belege, Zeichenzahlen oder Kürzungsmarker.
Immer der **volle** Wortlaut, nicht der im Druck gekürzte Auszug — beurteilt
wird der Satz, nicht das Layout. Wiederholte Beschreibungen bleiben eigene
Zeilen, weil jede zu einem anderen Aktuerspaar gehört.

Erzeugt aus denselben Quellen wie der Tabellenrenderer, damit eine Zeile
wirklich der gedruckten Zeile entspricht.

Zum Layout: die gedruckte Tabelle kürzt Relevanz und Beschreibung bei
60 Zeichen auf Wortgrenze. 550 von 619 Relevanzsätzen sind betroffen, im Median
gehen 21 Zeichen verloren. Der volle Text steht in den Daten; nur die
Druckspalte ist kurz.

## 11. Der Reviewstand ist vorläufig

`provisional: true` bzw. `accepted_provisional` heißt: als Satzstand
übernommen, **nicht** endgültig freigegeben und **keine Rechtefreigabe**.

Identität geprüft ≠ Veröffentlichung erlaubt. Von den 476 verwendeten Logos
warten 474 auf schriftliche Genehmigung, 1 auf markenrechtliche Prüfung, 1 ist
nur bedingt lizenziert. Vor einer externen Veröffentlichung muss diese
Warteschlange abgearbeitet oder der jeweilige Knoten auf `none` gesetzt werden.
Das ist derzeit die eigentliche Grenze, nicht die Bildqualität.

## 12. Neo4j: vorerst außerhalb des Auftrags

**Kein Schreibzugriff auf Neo4j.** Der Property-Patch ist bis auf Weiteres
nicht Teil der Aufgabe und wird nicht ausgeführt — auch nicht „nur zur Probe".

Der vorbereitete Stand bleibt unangetastet liegen
(`full_image_property_patch.json`, `dry_run_only: true`, 412 Zeilen, 350
Overlay-Knoten ausgenommen, 0 Zuordnungsfehler). Er wurde nie angewandt und
wird jetzt auch nicht angewandt; gelöscht ist nichts, damit später ohne
Neuaufbau daran angeknüpft werden kann.

Neo4j bleibt die Quelle der Wahrheit; dieser Ordner ist Transport und Review.
`mit-bestand` wird nur über die erzeugten Assets und Fragmente berührt.

---

## Kurzcheck vor dem Abgeben

1. `python full_image_collection.py validate` → PASS
2. Deckkraft: alle Assets `max(alpha) == 255`
3. `build_report_manifest.py` neu erzeugt
4. Fragmente **mit** `--images-manifest`; `grep -c 'image='` plausibel und
   gleich der `SemioLogoFit`-Zahl
5. Bericht mit `--skip-nx-cache` gebaut, beide PDFs neuer als der Asset-Sync
6. Stichprobe im gebauten PDF angesehen, **hell und dunkel**
7. Kein Neo4j-Write

## 13. Beziehungsprofil statt Beziehungsdauer (20.08.2026)

Verbindliche Hauptklassen:

- `Projektübergreifend`: Beziehung gilt über mehrere Projekte oder eine
  formale gemeinsame Struktur hinweg.
- `Vorhabenspezifisch`: Beziehung gilt nur für ein konkretes Projekt, einen
  Auftrag oder ein Ereignis.

Unterklassen: `institutionell`, `strategisch`, `operativ`, `Vorhaben`,
`Leistung`, `Ereignis`. Laufend/beendet und eine zeitliche Dauer werden nicht
klassifiziert.

Aktueller LaTeX-Stand nach Anwendung: **618 Knoten / 262 Kanten**. AT:K004 und
NL:K019 wurden als unbelegt entfernt; alle Endknoten bleiben sichtbar. Jede
verbleibende Kante besitzt mindestens eine Quellen-URL und ein Belegzitat.

Die neun Sonderentscheidungen und die verbindlichen Korrekturen der
71-Projekte-Erweiterung stehen unter
`beziehungsprofil_review/ERWEITERUNG_KORREKTUREN_FREIGEGEBEN.json`.
