# Übergabe: Logos im Akteursnetz

**Stand:** 2026-08-16

**Status:** Identitätsprüfung vollständig; Veröffentlichung rechtlich noch nicht freigegeben.

**Sicherheitsgrenze:** `mit-bestand` blieb unverändert. Es gab keinen Neo4j-Write.

## Zweite Vollprüfung 2026-08-16

Alle 33 Prüfbögen und damit alle 476 aktuell verwendeten Logos wurden ein zweites
Mal visuell kontrolliert. Die 20 in den letzten drei Arbeitssitzungen ergänzten
Logos wurden zusätzlich einzeln gegen die aktuellen offiziellen Organisations-
oder eindeutig belegten Trägerseiten geprüft. Ergebnis: **20/20 richtig**, keine
Ersetzung erforderlich, keine offene Identitätsprüfung. Die 13 Gruppen identischer
Quelldateien sind vollständig erklärte Organisations-, Untereinheits- oder
Trägermarken und keine zufälligen Dubletten.

Der technische Gegenlauf prüfte 757 Basis- und Dunkelassets auf Vorhandensein,
SHA-256, PNG/RGBA, 256×256 und Kreisbegrenzung. Es gab null Fehler; 41/41 Tests
bestanden. Der ausführliche Nachweis liegt in
`bilder_full/CURRENT_LOGO_REVERIFICATION_2026-08-16.md`.

## Ergebnis

Der eingefrorene 859er Transport enthält 762 Organisationen und 97 bildlose Projekte.
Alle 762 Organisationen sind vorläufig mit genau einem Ergebnis abgeschlossen:

| Ergebnis | Anzahl |
|---|---:|
| `logo` | 525 |
| `none` | 237 |
| offene Reviews | 0 |
| Deckkraft | 50 % |

Das aktuelle Netz ist kleiner und umfasst 619 Knoten:

| Aktueller Stand | Anzahl |
|---|---:|
| Organisationen | 541 |
| Projekte, absichtlich bildlos | 78 |
| korrekte offizielle Logo-Ergebnisse | 476 |
| begründete `none`-Ergebnisse | 65 |
| offene Identitätsprüfungen | 0 |

Die aktuelle Fassung ergänzt 16 recherchierte Logos als eigenen Render-Overlay
unter `bilder_full/current_only_final/`. Darunter sind Toulouse Métropole und
AD VITAM MATERIAL als zwei Organisationen außerhalb des alten 762er-Freeze;
14 weitere waren im Freeze noch `none`. Der eingefrorene Transport wurde dafür
nicht umgedeutet oder erweitert.

## Letzte Restjagd und Korrekturen

Der letzte Lauf prüfte alle 81 noch bildlosen aktuellen Organisationen erneut in
offiziellen Headern, Medienbereichen, CSS-/SVG-Quellen und WordPress-Medien. 16
eindeutige Marken wurden übernommen: Archipel zéro, Bellastock, Toulouse Métropole,
Gauthey Cheminées, Enviromate, Surplus Building & Plumbing Materials, Antique
Wooden Floors, Romsey Reclamation, E&A Reclamation, Lagemaat Heerde, Ter Velde &
Den Besten, Eeuwenhout Antoine Verhofstede, Heyns Recycling, AD VITAM MATERIAL,
Sundahus sowie Joensuun Rakennuspurku ja Timanttiurakointi Oy.

Zusätzlich wurden die letzten Fehlzuordnungen entfernt:

- Enviromate: StartUs-Logo verworfen → exaktes offizielles Enviromate-Wortzeichen
- RAEDIFICARE: Baustellenfoto verworfen → offizielles Wortzeichen
- Grayo: Fototextur verworfen → offizielles Wortzeichen
- Sundahus: Sundahus/iBinder-Kombinationslogo verworfen → exaktes offizielles Sundahus-Logo
- PREUSE: Interreg-/EU-Förderlockup verworfen → `none`
- Empa: generisches App-Symbol verworfen → offizielles Empa-Wortzeichen
- FORE Partnership und Elliott Wood: gegen die offizielle Seite gegengeprüft

Fotos, Social-Media-Symbole, Partner-/Zertifikatslogos, Förderlockups und zu kleine
Rasterdateien bleiben ausgeschlossen. `none` ist ein vollständiges Ergebnis und
lässt den bisherigen ID-Knoten unverändert.

## Darstellung

- Assetformat: 256×256 PNG, RGBA
- sichtbare Pixel kreisförmig begrenzt
- farbige Rechteckmarken kreisfüllend beschnitten, nicht künstlich aufgefüllt
- freistehende Marken vollständig innerhalb des Kreises
- neutrale Schwarz-/Weißanteile themefähig; Markenfarben bleiben erhalten
- Reihenfolge: Knotenfüllung, Logo, Kontur/Zustand, unveränderte zentrierte ID
- vorläufige Logo-Deckkraft: 50 %

Die 33 Prüfbögen enthalten alle 525 Vorschläge in Hell und Dunkel. Die Vorschläge
sind weiterhin später einzeln revidierbar.

## Bildrechte

Für alle 476 aktuell verwendbaren Logos sind Quelle, Kontaktweg, Rechteentscheidung
und Druckfreigabestatus dokumentiert. Herkunft ist jedoch keine Nutzungserlaubnis:

| Rechtegate | Anzahl |
|---|---:|
| schriftliche Erlaubnis erforderlich | 474 |
| juristische/Markenprüfung erforderlich | 1 |
| bedingt lizenziert | 1 |
| externe Erlaubnisanfragen versendet | 0 |

Vor Veröffentlichung muss für jede blockierte Marke eine schriftliche Freigabe
abgelegt oder ausschließlich dieser Knoten auf `none` gesetzt werden. Details:
`bilder_full/CURRENT_IMAGE_RIGHTS_AUDIT.md` und `.csv`.

## Maßgebliche Dateien

| Datei | Zweck |
|---|---|
| `bilder_full/CURRENT_LOGO_IDENTITY_AUDIT.json` | vollständiger 541er Identitätsnachweis |
| `bilder_full/CURRENT_LOGO_IDENTITY_AUDIT.csv` | prüfbare Tabellenfassung |
| `bilder_full/CURRENT_LOGO_IDENTITY_AUDIT.html` | klickbare Galerie aller 541 Organisationen |
| `bilder_full/CURRENT_IMAGE_RIGHTS_AUDIT.json` | Rechtegate für 476 Logos |
| `bilder_full/CURRENT_IMAGE_RIGHTS_AUDIT.csv` | Kontakt-/Freigabewarteschlange |
| `bilder_full/final_image_manifest.json` | validierter eingefrorener 762er Transport |
| `bilder_full/current_image_manifest.json` | Rendertransport für 541 aktuelle Organisationen |
| `bilder_full/final_review/index.json` | Index der 33 Prüfbögen |
| `bilder_full/final_review/FINAL_SUGGESTION_AUDIT.json` | maschineller Vollaudit |
| `bilder_full/full_image_property_patch.json` | trockener Property-Patch, 412 Graphzeilen |
| `bilder_full/full_image_property_patch_report.md` | Match-/Overlaybericht, 350 Overlays |
| `bilder_full/render/render_report.json` | bestandener Druckrender-Nachweis |
| `bilder_full/render/akteursnetz_images_light.pdf` | Netz mit Logos, hell |
| `bilder_full/render/akteursnetz_images_dark.pdf` | Netz mit Logos, dunkel |
| `bilder_full/render/akteursnetz_control_light.pdf` | bildlose Kontrolle, hell |
| `bilder_full/render/akteursnetz_control_dark.pdf` | bildlose Kontrolle, dunkel |
| `bilder_full/bilder/<LAND>/<TID>.png` | finale Freeze-Assets |
| `bilder_full/current_only_final/` | 16 aktuelle Overlay-Assets |
| `full_image_collection.py` | Sammlung, Review, Finalisierung, Validierung |
| `pilot_images.py` | Crop, Kreisbegrenzung, Themebehandlung |

## Reproduzierbare Abschlussbefehle

```powershell
Set-Location E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck
python full_image_collection.py suggest
python full_image_collection.py accept-suggestions --opacity 50
python full_image_collection.py finalize
python full_image_collection.py validate
python full_image_collection.py current-scope
python full_image_collection.py current-deep-review
python full_image_collection.py rights-audit
python full_image_collection.py current-finalize
python full_image_collection.py render
python full_image_collection.py patch
python -m unittest -v test_full_image_collection.py test_current_image_render.py
```

Aktueller Prüfstand: **41/41 Tests bestanden** und
`PASS: 762/762 explicitly confirmed; assets and provenance valid`.

Der vollständige `render`-Lauf ist bestanden: alle 476 Logos des aktuellen Netzes
werden gezeichnet; Hell, Dunkel sowie beide bildlosen
Kontrollfassungen umfassen je vier Seiten. Alle 16 Seiten wurden bei 600 dpi
gerastert und mit SHA-256 im Renderbericht dokumentiert. Der trockene `patch`-Lauf
ist ebenfalls bestanden: 412 Graphzeilen und 350 dokumentierte Overlays, null
Schreiboperationen. Eine Datenbankänderung benötigt weiterhin eine separate Freigabe.

Die visuelle Endkontrolle der Hell-/Dunkelfassungen und der bildlosen Kontrollen
zeigt keine abgeschnittenen Rahmen, Logos außerhalb des Kreisclips oder fehlenden
Glyphen. Die unveränderten IDs liegen weiterhin lesbar über den Bildmarken.

## Review öffnen

Die bestehende lokale Galerie läuft unter `http://127.0.0.1:8765/`. Falls sie
neu gestartet werden muss:

```powershell
python full_image_collection.py review-server --host 127.0.0.1 --port 8765 --no-open
```

Eine spätere Einzelentscheidung ersetzt nur den betreffenden Knoten. Den Bulk-Befehl
`accept-suggestions` nur erneut ausführen, wenn alle Einzelkorrekturen bewusst wieder
überschrieben werden sollen.

## Nachtrag 16.08.2026 – Entscheidungen dokumentiert, Neo4j ausgesetzt

Die getroffenen Entscheidungen zu Deckkraft, Beschnitt, Dunkelbild,
Sperrlisten, Fragmenterzeugung und Prüfdokumenten stehen jetzt gesammelt in
**`ENTSCHEIDUNGEN.md`** — mit Begründung, weil mehrere davon schon einmal
korrekt waren und später still zurückgefallen sind. Wer dort einen Wert
ändert, ändert eine Entscheidung und muss die Begründung mitändern.

Kurzfassung der wichtigsten Punkte:

- **Deckkraft 100 %**, nie 50 %. Zwei Vorgabewerte (`accept-suggestions
  --opacity`, `command_current_finalize`) standen auf 50 und haben den Fehler
  nach jeder Korrektur erneut eingeschleppt; beide stehen jetzt auf 100.
  Fertiges Asset muss `max(alpha) == 255` haben.
- **`circle_extend` statt Beschnitt**: Hintergrund nach außen verlängern, die
  Marke nie abschneiden. Nur die Marke bestimmt die Skalierung, nicht der
  Hintergrund.
- **`is_opaque_tile`** verlangt zusätzlich echte Deckung (≥ 0,80 mit
  `alpha >= 250`), sonst entstand aus einem weichen Schlagschatten ein
  durchsichtiger Ring in der Scheibe.
- **`candidate_rejection`** verwirft Vorschauen mit `max(alpha) < 250`. Eine
  zu einem praktisch leeren Bild gerasterte SVG (`NL:U30`) stand sonst in der
  Rangfolge über vier einwandfreien offiziellen Icons und lief bis in einen
  bereits abgenommenen Identitätsaudit durch.
- **Dunkelbild**: `light_backdrop` nur, wo tatsächlich Inhalt ausfällt. Die
  Luma-Messung ist ein Suchfilter, keine Entscheidung — vor jeder Aufnahme das
  gerenderte Bild ansehen. Aktuell 86 Overrides.
- **Sperrlisten** sperren die konkrete Datei, nicht den Akteur; eine Sperre auf
  eine Fremddomain ist gegenstandslos, sobald dem Knoten die richtige Domain
  zugeordnet ist.
- **Fragmente immer mit `--images-manifest`.** Das Flag hat bewusst keinen
  Vorgabewert; ohne es entstehen klaglos Fragmente ganz ohne Logos.
- **Rendermanifest** aus `build_report_manifest.py`, abgeleitet aus dem
  aktuellen Identitätsaudit — die 762er Auswahl deckt das aktuelle Netz nicht
  vollständig ab.

**Neo4j ist vorerst nicht Teil der Aufgabe.** Der Property-Patch wird nicht
ausgeführt, auch nicht probeweise. Der vorbereitete Stand bleibt unangetastet
liegen (`full_image_property_patch.json`, `dry_run_only: true`, 412 Zeilen,
350 Overlay-Knoten ausgenommen, 0 Zuordnungsfehler, nie angewandt); gelöscht
ist nichts, damit später ohne Neuaufbau daran angeknüpft werden kann.

Aktueller Stand des Berichts: 476 der 541 Organisationen des aktuellen
619-Knoten-Netzes tragen ein Logo (88 %), Abbildungen und Tabellen
übereinstimmend; `validate` 762/762 grün; beide PDFs neu gebaut. Offen bleiben
die Bildrechte (474 der 476 warten auf schriftliche Genehmigung, 1 auf
markenrechtliche Prüfung, 1 bedingt lizenziert) — das ist derzeit die
eigentliche Grenze, nicht die Bildqualität.
