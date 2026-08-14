# Übergabe: vollständige Bildprüfung im Akteursnetz

**Stand:** 2026-08-13  
**Arbeitsbereich:** `_neo4j/review/2026-08_akteursnetz_faktencheck/`  
**Status:** 762 Vorschläge vorläufig übernommen, finalisiert und validiert;
343 Logos in den Zwischenbericht ausgeliefert (Knoten und Tabelle). `render`
und `patch` sind nicht gelaufen, nach Neo4j wurde nichts geschrieben.

## Kurzfassung

Der Bildworkflow für das final beschnittene 859er Akteursnetz ist implementiert. Die
97 Bauvorhaben bleiben bildlos. Für alle 762 Organisationsknoten liegt ein eindeutiger
Vorschlag `logo` oder `none` vor. Alle Vorschläge wurden am 13. August 2026
strukturell geprüft; die ursprünglich 352 Logo-Vorschläge wurden zusätzlich vollständig
auf 22 Prüfbögen in Hell und Dunkel angesehen.

Der Benutzer hat anschließend angewiesen, **alle aktuellen Vorschläge mit 50 %
Logo-Deckkraft vorläufig zu übernehmen**, weil eine spätere erneute Einzelprüfung
möglich bleiben soll. Der Reviewstand lautet:

| Zustand | Anzahl |
|---|---:|
| Organisationen insgesamt | 762 |
| vorläufig übernommene Logos | 343 |
| vorläufig übernommenes `none` | 419 |
| Graph-konsistente Organisationen | 412 |
| Overlay-Organisationen ohne Graph-ID | 350 |
| bildlose Projekte | 97 |
| Logo-Deckkraft | 50 % |
| offene Reviewzeilen | 0 |
| Neo4j-Schreiboperationen | 0 |

`none` ist vollständig: Der bisherige ID-Knoten bleibt unverändert.

## Verbindliche Sicherheitsgrenze

- **Neo4j ist die Quelle der Wahrheit.** Dieser Ordner ist nur Transport und Review.
- `mit-bestand` wurde nicht verändert.
- Es wurden keine `:Quelle`-Knoten, `BELEGT_IN`-Kanten oder Sidecar-Verweise erzeugt.
- Das finale Manifest und die finalen 256×256-Assets sind erzeugt und in den
  Zwischenbericht kopiert. Länder-PDFs (`render`) und der Property-Patch
  (`patch`) wurden bewusst **noch nicht** erzeugt.
- `full_asset_review.json` ist ein vorläufiger Arbeitsstand, keine kanonische
  Graphfreigabe.
- Vor einem Patch muss jeder der 412 graphgestützten Datensätze über `id` exakt
  einen Knoten treffen. Die 350 Overlays bleiben vom Patch ausgeschlossen.

## Was implementiert wurde

### Sammlung und Vorschläge

`full_image_collection.py` unterstützt:

- die eingefrorene 762er Organisationsauswahl aus dem 859er Netz;
- Domainprüfung und Kandidatensammlung von offiziellen Seiten;
- Apple-Touch-Icons, deklarierte Icons, Favicons, geprüfte Header-/Medienmarken,
  strukturierte Logos und eng geprüfte `og:image`-Treffer;
- 128-px-Mindestkante für Rasterbilder und SVG;
- Sperren für Fotos, Social-Media-Zeichen, Partner-/Zertifikatslogos, Platzhalter
  und bekannte Identitätsfehler;
- stabile Vorschläge mit Kandidaten-ID und Kandidaten-SHA-256;
- eine lokale Review-Galerie mit Land-/Statusfilter, Suche, Hell-/Dunkelvorschau,
  Kreisclip, unveränderter ID und Deckkraftregler;
- vorläufige Gesamtübernahme über `accept-suggestions --opacity 50`;
- spätere Einzelkorrektur, ohne die übrigen vorläufigen Zeilen zu verändern;
- Finalisierung und Manifestprüfung (gelaufen) sowie Rendering und trockenen
  Patch (nicht gelaufen) als getrennte Schritte.

### Darstellung und Deckkraft

- Logos werden vollständig innerhalb des Knotens vorbereitet. Flächige rechteckige
  Hintergründe werden kreisfüllend zugeschnitten und kreisförmig maskiert.
- Neutrale weiße/schwarze Flächen werden für Hell/Dunkel tokenisiert; Farbanteile
  bleiben erhalten.
- Reihenfolge: Kreisfüllung, Logo, Zustandskontur, unveränderte ID.
- Der Galerie-Regler steht bei 50 %. Der Wert ist in jeder Reviewzeile gespeichert
  und wird bei späterer Finalisierung auf die Asset-Alphaebene angewendet. Die
  gesammelte Quelldatei wird nicht verändert.
- Ohne Bildmanifest bleibt der historische Renderer bildlos.

### Korrekturen aus dem Vollaudit

14 Organisationen hatten einen falschen oder unbrauchbaren Spitzenkandidaten. Gute
offizielle Alternativen wurden bevorzugt; ohne sichere Alternative wurde `none`
gesetzt. Beispiele:

- BioRegional: fremdes Abstrakt-Logo gesperrt, offizielles App-Icon gewählt.
- Concular: Brandschutztürfoto gesperrt, offizielles Wortzeichen gewählt.
- Fer et Pierre: Telefonsymbol gesperrt, offizielles Wort-/Bildzeichen gewählt.
- Houtenplaten: Platzhalter und Fassadenfoto gesperrt, offizielles HP-Zeichen gewählt.
- Bærebyg: Censio-Logo gesperrt, offizielles Bærebyg-Zeichen gewählt.
- Ohne sichere Alternative `none`: Opera/Opera-Browser, CSTB/BATIPEDIA,
  Bauteilbörse Oldenburg/OOZ, a:gain/GAIN, HSB Göteborg/Business Region Göteborg,
  The Old Slate Yard/Websitebuilder und Matériauthèque/WordPress.

Die vollständige Liste steht in
`bilder_full/final_review/FINAL_SUGGESTION_AUDIT.md`.

## Maßgebliche Dateien

| Datei/Ordner | Bedeutung |
|---|---|
| `bilder_full/selection.json` | eingefrorene 762er Auswahl samt Graph-/Overlay-Zuordnung |
| `bilder_full/domains_review.json` | recherchierte Domain- und Identitätsstände |
| `bilder_full/kandidaten/<LAND>/<TID>/` | Kandidaten und Abrufmetadaten |
| `bilder_full/suggestions.json` | aktueller Vorschlag für alle 762 Knoten |
| `bilder_full/full_asset_review.json` | vorläufiger 762/762-Reviewstand, Deckkraft 100 % (Sicherung des 50-%-Stands als `.bak-opacity50`) |
| `dark_backdrop_overrides.json` | 75 Logos mit hellem Backdrop statt Theme-Umfärbung, je mit gemessenem Grund |
| `bilder_full/final_review/index.json` | Index der 22 visuellen Prüfbögen |
| `bilder_full/final_review/FINAL_SUGGESTION_AUDIT.md` | menschenlesbarer Vollaudit |
| `bilder_full/final_review/FINAL_SUGGESTION_AUDIT.json` | maschinenlesbarer Vollaudit |
| `full_image_collection.py` | Sammlung, Review, Finalisierung, Validierung, Rendering, Patch |
| `full_image_review.html` | lokale Einzelabnahme |
| `pilot_images.py` | Bildaufbereitung, Crop, Themes und Assetprüfungen |
| `test_full_image_collection.py` | Integritäts- und Regressionstests |
| `bilder_full/final_image_manifest.json` | finales 762er Manifest mit Assetpfad und SHA-256 |
| `bilder_full/bilder/<LAND>/<TID>.png` | finale 256×256-RGBA-Assets, `-dark` wo nötig |
| `_neo4j/netz/netz/sources.py` | Manifest-, Asset- und Fragmentziele des Berichts |
| `_neo4j/netz/netz/cli.py` | `--images-manifest`, `--image-paths`, `sync-images`, `sync-fragments` |
| `_neo4j/netz/netz/render/latex/graph_tikz.py` | Bilder nur für akzeptierte Organisationen |
| `_neo4j/netz/netz/render/latex/table_grid.py` | Logospalte der Tabelle (`\SemioLogoFit`) |
| `semio: print/tex/semio-logo.sty` | Pfadauflösung inkl. `-dark`, `\SemioLogoFit` |
| `semio: print/tex/semio-graph.sty` | `\semio@graph@node@image@opacity` |

## Review wieder aufnehmen

Die Galerie läuft lokal unter `http://127.0.0.1:8765/`.

Falls der Server nicht mehr läuft:

```powershell
Set-Location E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck
python full_image_collection.py review-server --host 127.0.0.1 --port 8765 --no-open
```

Die Galerie startet bei 762/762 und Filter `Alle`. Jeder Eintrag trägt zunächst
`vorläufig: logo` oder `vorläufig: none`. Für eine Einzelkorrektur:

1. Organisation suchen oder nach Land filtern.
2. Bei einem Logo einen nicht gesperrten Kandidaten anklicken.
3. `Ausgewähltes Logo bestätigen` oder `none bestätigen` wählen.
4. Nur diese Zeile wird individuell bestätigt (`provisional: false`).

Den Bulk-Schritt nur wiederholen, wenn wirklich alle späteren Einzeländerungen
überschrieben werden sollen:

```powershell
python full_image_collection.py accept-suggestions --opacity 50
```

## Prüfungen

Aktueller Teststand: **24 Tests bestanden**.

```powershell
Set-Location E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck
python -m unittest test_full_image_collection.py
```

Prüfbögen und Audit neu erzeugen:

```powershell
python full_image_collection.py audit-sheets
```

`suggest` erzeugt Vorschläge neu, bestätigt aber nichts. `accept-suggestions`
übernimmt alle aktuellen Vorschläge und überschreibt spätere Einzelkorrekturen.

## Schlussstrecke

**Am 13. August 2026 gelaufen, auf Anweisung des Benutzers, die Bilder in Knoten
und Tabelle des Zwischenberichts zu übernehmen:**

```powershell
python full_image_collection.py finalize   # 343 logo, 419 none
python full_image_collection.py validate   # PASS: 762/762
```

1. `finalize` erzeugte 256×256-RGBA-PNGs unter `bilder_full/bilder/<LAND>/<TID>.png`
   und `final_image_manifest.json`. Die 50 % Deckkraft stecken in der Alphaebene.
2. `validate` prüfte Format, Abmessungen, radialen Sicherheitsbereich,
   Checksummen, Reviewnachweis sowie 412 Graphknoten und 350 Overlays.

**Noch nicht gelaufen:**

```powershell
python full_image_collection.py render
python full_image_collection.py patch
```

3. `render` erzeugt alle elf Länder in Hell/Dunkel sowie bildlose Kontrollen
   und prüft bei 600 dpi. Ruft `netz.cli abb` jetzt mit `--image-paths absolute`
   auf, weil netz standardmäßig berichtsrelative Pfade schreibt (siehe unten).
   Die frühere Zusicherung `Bilder im Fragment == Logos im Manifest` ist
   ersetzt: das gezeichnete Netz ist die strengere Teilmenge und trägt 278 der
   343 Logos. Geprüft wird stattdessen, dass **jedes** Bild im Fragment ein
   Manifestasset ist.
4. `patch` erzeugt nur einen trockenen Property-Patch und Bericht.
   **Kein Neo4j-Write.** `patch --live` prüft read-only die exakten
   `id`-Treffer gegen `mit-bestand`.

## Auslieferung in den Zwischenbericht

Die Assets liegen **im Berichtsrepo**, nicht mehr nur hier. Ein gesetztes
Fragment darf keinen `E:/recherche`-Pfad tragen — es würde nur auf der Maschine
bauen, die es erzeugt hat.

```powershell
Set-Location E:\recherche\_neo4j\netz
python -m netz.cli sync-images       # -> E:\semio\...\zwischenbericht\asset\akteur\<LAND>\<TID>.png
python -m netz.cli abb          --images-manifest <FINAL_MANIFEST>
python -m netz.cli tables-grid   --images-manifest <FINAL_MANIFEST>
python -m netz.cli sync-fragments    # -> ...\zwischenbericht\anhang\akteursnetz-*.tex
```

- `sync-images` kopiert Logo und `-dark`-Nachbar unter dem **Manifest-TID**,
  nicht unter der gedruckten ID: Prüfbögen und SHA-256-Liste sind über TID
  geführt, die gedruckte ID wandert bei jeder Neubelegung des Netzes. Der
  Schritt ist idempotent und räumt Dateien weg, die das Manifest nicht mehr nennt.
- Die Fragmente nennen die Bilder als `asset/akteur/<LAND>/<TID>.png`, also so,
  wie der Bericht seine übrigen Bilder nennt. `semio-logo.sty` löst daraus im
  Dark-Build selbst die `-dark`-Datei auf.
- Die Deckkraft im **Diagramm** setzt der Bericht, nicht die Bildprüfung:
  `\semio@graph@node@image@opacity` in `print/tex/semio-graph.sty`. Bei den 50 %
  aus der Prüfung lagen Logo und ID im selben 4,55-mm-Kreis übereinander und
  beide waren unlesbar. Die Prüfung bleibt die Quelle dafür, **welches** Logo
  erscheint — nicht wie kräftig.

## Deckkraft und Dunkel-auf-Dunkel (2026-08-14)

Zwei Korrekturen an der Druckdarstellung, ausdrücklich vom Benutzer angewiesen,
beide nur an der Zeichnung/Auslieferung — keine Logoentscheidung, keine
Kandidatenwahl, kein Quellen- oder Neo4j-Bezug verändert.

**Deckkraft 50 % → 100 %.** `full_asset_review.json` trug `logo_opacity_percent:
50`; jede Marke mischte sich damit mit dem Seitenhintergrund und erschien in
Light und Dark unterschiedlich eingefärbt. Kopfwert und alle 762 Zeilen auf 100
gesetzt, Kandidaten-ID, SHA-256 und `provisional: true` unverändert. Sicherung
des alten Stands liegt als `full_asset_review.json.bak-opacity50` daneben.

**Dunkel-auf-Dunkel behoben, 75 Logos.** Zwei getrennte Ursachen, ein
gemeinsamer Befund: bei voller Deckkraft verschwanden manche Marken im
Dark-Build, weil ihre eigene Farbe zu dunkel gegen den fast schwarzen
Knoten-Canvas war.

- **Bugfix, 91 Logos:** `crop_mode=safe_contain` erzeugte noch nie eine
  `-dark`-Datei — die vorhandene Theme-Umfärbung (`tokenise_transparent_
  neutral_mark`) hätte bei überwiegend neutralen (schwarz/grau) Marken
  funktioniert, wurde aber nie mit `theme="dark"` aufgerufen. `command_finalize`
  vergleicht jetzt Light- gegen Dark-Rendering vor jeder Deckkraftanwendung und
  schreibt die `-dark`-Datei, sobald sie sich unterscheidet — nicht mehr nur
  bei `neutral_knockout`.
- **Neuer Pfad, 75 Logos, `dark_backdrop_overrides.json`:** Marken, deren
  eigene Farbe gesättigt, aber zu dunkel ist (z. B. Navy, Tannengrün) — die
  Theme-Umfärbung fasst sie absichtlich nicht an, sonst ginge die Markenfarbe
  verloren. `prepare_light_backdrop_canvas` (`pilot_images.py`) backt
  stattdessen eine feste helle Kreisscheibe hinter die Marke und färbt nur
  echte Schwarztöne pixelweise auf das Ink-Token um (`blacken_to_ink`) — jede
  andere Farbe bleibt exakt wie in der Quelle. Ein Ergebnis für beide Themes,
  keine `-dark`-Datei nötig. 62 der 75 kamen aus `safe_contain` (dunkel und
  nicht neutral genug für die alte Umfärbung), 13 aus `neutral_knockout` (der
  neutrale Teil war schon richtig umgefärbt, ein gesättigter dunkler Rest
  aber nicht).

Geprüft am gebauten PDF, nicht nur an der Asset-Datei: 75 Logos auf simuliertem
Light- und Dark-Canvas kontrolliert (alle lesbar, Markenfarbe erhalten),
anschließend Diagrammknoten UND Tabellenspalte im tatsächlich kompilierten PDF
stichprobenartig verglichen (`M13`, `U12`, `M15`, `M43`, `G01`, `S02`, `M05`,
`I03` sowie zwei Bugfix-Fälle) — Farben identisch zwischen Light und Dark, wie
beabsichtigt. `dark_backdrop_overrides.json` dokumentiert jeden Eintrag mit dem
gemessenen Grund (Median-Leuchtdichte, Neutralanteil bzw. Farbanteil im
Dark-Rest). 24 + 9 Tests weiterhin grün.

**Offen, nicht Teil dieser Korrektur:** die Deckkraftfläche hinter der
Knoten-ID im Diagramm (`\semio@graph@node@label@plate@radius/@opacity` in
`semio-graph.sty`) deckt bei radius=1.0 den ganzen Knoten ab und dämpft damit
auch bei kräftigen Marken das Logo insgesamt — ein separater, dem Benutzer
bereits vorgelegter Zielkonflikt zwischen voller ID-Lesbarkeit und voller
Markenfarbe, noch ohne Entscheidung.

Vor dieser Schlussstrecke muss der Benutzer ausdrücklich entscheiden, ob die
vorläufige Gesamtübernahme als Druckfreigabe genügt oder zuerst weitere Einzelfälle
nachgeprüft werden. Die ursprüngliche Planfassung verlangte Einzelbestätigung; der
Benutzer hat später die vorläufige Gesamtübernahme angeordnet. Diese Differenz ist
in `full_asset_review.json` als
`review_mode: bulk_suggestion_acceptance_provisional` und `provisional: true`
sichtbar und darf nicht als endgültige Freigabe umgedeutet werden.

## Arbeitsbaum und Fremdänderungen

Der Arbeitsbaum ist nicht sauber. Neben den Bilddateien bestehen weitere Änderungen
am Akteursnetz, unter anderem Tabellen-/Kantenrendering und
`kanten_klassifikation.json`. Diese können aus paralleler Arbeit stammen und dürfen
nicht pauschal zurückgesetzt oder gemeinsam committed werden. Vor einem Commit den
Scope gezielt auswählen.

## Definition des aktuellen Abschlusses

- 762/762 Entscheidungen vorhanden;
- 343 `logo`, 419 `none`;
- 50 % Logo-Deckkraft überall gespeichert;
- 343 Logoentscheidungen mit Kandidaten-ID und Kandidaten-SHA-256;
- spätere Einzelkorrektur möglich;
- 24 Tests grün;
- kein Neo4j-Write;
- keine finale Asset-, Render- oder Patchfreigabe behauptet.

## Nachtrag 14.08.2026 – aktuelles 619-Knoten-Netz

Die damalige 762er-Auswahl bleibt unverändert als eingefrorener Transportstand.
Der aktuelle Semio-Export wurde separat ausgewertet und enthält 619 Knoten:
541 Organisationen und 78 weiterhin bildlose Projekte.

- 277 Organisationsknoten besitzen bereits ein Logo im aktuellen Bestand.
- Für die 264 bildlosen Organisationen wurden Domains erneut einzeln geprüft,
  offizielle Haupt-, Medien-, Marken- und Trägerseiten tiefer durchsucht und
  browserkomprimierte bzw. webgeschützte Seiten technisch besser erschlossen.
- Der read-only Tiefenlauf ergibt 116 neue identitätsgefilterte Vorschläge und
  148 `none`-Fälle. Maximal erreichbar nach visueller Bestätigung: 393/541.
- Von den 148 `none`-Fällen haben 76 noch keine ausreichend bestätigte bzw.
  freigegebene Organisationsdomain; 72 besitzen eine bestätigte Domain, aber
  keine sichere, drucklesbare und zulässig belegte Marke.
- Klare Fehlzuordnungen (u. a. CSTB-Untermarken, UEA-Fotos, BDP-Farbfläche,
  Google-Play-Grafik, Deutsche-Bahn-Partnerlogo bei Madaster/EPEA) bleiben
  gesperrt. Empa bleibt wegen der dokumentierten Genehmigungspflicht `none`.
- Die klickbare, read-only Galerie liegt unter
  `bilder_full/current_deep_review/index.html`; sie zeigt Hell/Dunkel,
  Kreisclip, unveränderte ID, Land-/Statusfilter und offizielle Quellen.
- Alle 116 neuen Vorschläge sind unbestätigt. Es gab keinen Neo4j-Write und
  keine Übertragung in `mit-bestand`.
- 32 Integritäts- und Regressionstests sind grün.
