# Druckpilot für Bilder im Akteursnetz

Ordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\`

## 0. Die bestimmende Größe — bitte zuerst lesen

Alles an diesem Plan hängt an einer Zahl, die aus dem Stylesheet kommt, nicht aus einer
Schätzung (`print/tex/semio-graph.sty`, Zeile 17):

    Knotenradius            2,275 mm      -> Durchmesser 4,55 mm
    focal-Knoten            2,575 mm      -> Durchmesser 5,15 mm
    größtes Quadrat im Kreis 3,22 mm      -> 38 px bei 300 dpi, 76 px bei 600 dpi

**Ein Knoten ist so groß wie ein kleines „o“ im Fließtext.** Das nutzbare Bildfeld ist
3,22 mm im Quadrat. Das ist Favicon-Format, kein Bildformat.

Daraus folgt hart:

* **Fotos scheiden aus.** Ein Gebäudefoto bei 3,2 mm ist ein grauer Fleck. Das gilt auch
  für gute Fotos — es ist eine Frage der Fläche, nicht der Qualität.
* **Wortmarken scheiden aus.** „Gardiner & Theobald“ als Schriftzug bei 3,2 mm ist eine
  Schmutzlinie. Auch zweizeilige Logos mit Claim fallen weg.
* **Es funktionieren nur einfache Bildmarken:** Signet, Wappen, Piktogramm —
  hoher Kontrast, wenige Formen, keine Feinlinien, kein Farbverlauf.

Das ist keine Einschränkung, die sich wegarbeiten lässt: Das Web hat für genau diese Größe
bereits eine Lösung, nämlich das Favicon. **Die Suche ist deshalb eine Favicon-Suche,
keine Bildersuche** — und das macht sie zum großen Teil automatisierbar.

### Größer geht kaum

Vergrößern hilft weniger, als es scheint, weil die dichten Panels es nicht hergeben
(181 × 50 mm, GB hat 129 Knoten):

| Radius | Bildfeld | @300 dpi | Flächenfüllung GB | Layout |
|---|---|---|---|---|
| 2,275 mm (heute) | 3,22 mm | 38 px | 23 % | tragfähig |
| 3,0 mm | 4,24 mm | 50 px | 40 % | beginnt zu überlappen |
| 3,5 mm | 4,95 mm | 58 px | 55 % | unbrauchbar |
| 5,0 mm | 7,07 mm | 84 px | 112 % | unmöglich |

Selbst am oberen Ende des Machbaren (r = 3,0 mm) bleibt es Favicon-Format. **Die Bildjagd
sollte deshalb nicht auf eine spätere Vergrößerung spekulieren.**

---

## 1. Zwei Entscheidungen vorab

### 1.1 Das Label bleibt unverändert über dem Bild

Der Knoten trägt heute die ID („M07“, `\SemioMono` 5,2 pt ≈ 1,83 mm) mittig im Kreis.
Für den Pilot bleibt dieses Label **byte- und stilgleich** an derselben Stelle; ein
optionales Bild wird darunter gezeichnet. Es gibt keine adaptive Schriftfarbe, Kontur,
Platte oder Außenbeschriftung. Besteht ein Logo diesen Härtetest nicht, bleibt der Knoten
im heutigen ID-only-Zustand.

### 1.2 Bauvorhaben bekommen keine Bilder

97 der 859 Knoten sind Gebäude und Pilotprojekte, keine Organisationen. Sie haben kein
Logo, und ein Gebäudefoto scheitert an Abschnitt 0. Sie behalten ihre geometrische
Auszeichnung (`state`) und bleiben bildlos.

**Damit ist die reale Aufgabe: 762 Organisationen, nicht 859 Knoten.**

---

## 2. Welches Bild — nach Knotenklasse

Die Klasse steht als `typ` in `worklist.json`. Sie bestimmt, wonach überhaupt zu suchen
ist. Innerhalb der Klasse wird einzeln entschieden.

| Klasse | n | Erste Wahl | Zweite Wahl | Typisches Problem |
|---|---|---|---|---|
| Unternehmen | 344 | Bildmarke/Signet ohne Schriftzug | ID-only | reine Wortmarke → ID-only |
| Materialhub / Bauteilbörse | 199 | Signet | ID-only | oft sehr kleine Anbieter ohne echtes Logo |
| Forschung / Lehre | 58 | Siegel oder Institutssignet | ID-only | detailliertes Siegel → ID-only |
| Öffentliche Institution | 41 | **Wappen** | ID-only | Quelle und Nutzungsregeln einzeln prüfen |
| NGO / Verband / Netzwerk | 50 | Signet | ID-only | Claim mit im Logo → ID-only |
| Software / Tool-Anbieter | 30 | App-Icon | Signet | App-Icon ist meist die beste Quelle überhaupt |
| Förderträger | 8 | Wappen oder Amtszeichen | ID-only | Wortmarke → ID-only |
| Sonstige / unklar | 32 | einzeln prüfen | ID-only | Klasse nicht aus Altbestand ableiten |
| Bauvorhaben / Objekt | 97 | **kein Bild** | — | siehe 1.2 |

### Die Prüffrage bei jedem Einzelfall

> Ist die Marke bei 3,2 mm noch als *diese* Marke erkennbar — oder nur noch als Fleck?

Im Zweifel bleibt ausschließlich die bestehende Knoten-ID sichtbar. Monogramme entfallen,
weil sie mit der darüberliegenden Tabellen-ID ein zweites konkurrierendes Kürzel erzeugen.

---

## 3. Woher — Bezugsreihenfolge

Der finale `worklist`-Snapshot enthält bei **291 der 859 Knoten** mindestens eine URL und
insgesamt 386 Hosts. Faktencheck-Belege liefern zwar für alle 859 Knoten eine URL, sind aber
häufig Drittseiten. Keine dieser Zahlen ist eine Zahl „eigener Domains“.

Vor der Ernte wird deshalb je Pilotknoten eine Betreiber-/Organisationsdomain einzeln
bestätigt. Beleg-URLs sind nur Rechercheeinstieg und werden nie automatisch zur Logoquelle.

Wasserfall, in dieser Reihenfolge:

1. **`apple-touch-icon`** (`/apple-touch-icon.png`, meist 180 × 180) — die mit Abstand
   beste Quelle: eine Marke, die der Betreiber selbst für kleine quadratische Darstellung
   gezeichnet hat. Genau unser Problem, vom Eigentümer gelöst.
2. **`<link rel="icon">` im HTML**, bevorzugt SVG oder das größte PNG.
3. **`/favicon.ico`** — enthält oft mehrere Auflösungen; die größte nehmen.
4. **`og:image`** nur, wenn es tatsächlich ein Logo zeigt (oft ein Foto → dann verwerfen).
5. **Logo aus dem Seitenkopf**, per Hand identifiziert (`<img>` im `<header>`).
6. **Presse-/Downloadbereich** der Organisation („Logo“, „Presse“, „Media Kit“) — liefert
   meist eine saubere SVG/EPS-Fassung.
7. **Lizenzierte Wikimedia-Datei** bei öffentlichen Stellen, sofern Quelle und Lizenz
   einzeln geprüft wurden.
8. **ID-only** (Abschnitt 2).

Schritte 1–4 laufen nur auf den einzeln bestätigten Domains. Jeder Kandidat bleibt bis zur
visuellen Einzelentscheidung im Status `candidate`.

**Nicht verwenden:** Logo-Aggregatoren (Clearbit, logo.dev u. Ä.) — unklare Rechtelage und
oft veraltete Marken. Immer von der Domain des Eigentümers.

---

## 4. Zielformat und Zuschnitt

### Was gesucht wird

* **Mindestens 128 px Kantenlänge**, besser 180 px (apple-touch-icon) oder SVG.
* Quadratisch oder auf quadratisch beschneidbar.
* Möglichst mit transparentem oder einfarbigem Hintergrund.

Alles unter 128 px kürzester Kante verwerfen und bei der unveränderten ID-only-Darstellung
bleiben — Hochskalieren erzeugt nur Matsch.

### Aufbereitung (verbindlich, für alle gleich)

Master mit **256 × 256 px** ablegen. Das ist bei 3,22 mm rechnerisch weit über Druckbedarf
und lässt Reserve, falls der Knoten später wächst.

1. **Rand abschneiden.** Transparenten bzw. einfarbigen Rand trimmen. Logos kommen fast
   immer mit eingebautem Weißraum — der halbiert sonst die effektive Größe.
2. **Quadratisch auffüllen.** Auf das Bounding-Quadrat der langen Kante zentrieren, nicht
   verzerren.
3. **Sicherheitsabstand.** Sichtbare Pixel radial so skalieren, dass sie höchstens **93 %
   des Kreisradius** erreichen. Ein pauschales 86-%-Quadrat passt nicht sicher in den Kreis.
4. **Kreismaske.** Der Knoten ist ein Kreis; alles außerhalb wird abgeschnitten. Deshalb
   muss die Marke in den **Innenkreis** passen, nicht ins Quadrat — das ist die eigentliche
   Beschneidung und der Grund für Schritt 3.
5. **Transparenz behalten.** Der Theme-Hintergrund wird nicht ins PNG eingebrannt.
6. **Kontrastprüfung.** Marken müssen unverändert in Hell- und Dunkelfassung funktionieren.
   Bei zu geringem Kontrast bleibt der Knoten ID-only; Logos werden nicht umgefärbt.

Im Knoten wird das 256-px-Asset mit **100 % des Kreisdurchmessers** dargestellt (Faktor
1,43 gegenüber der ersten korrigierten 70-%-Probe). Die sichtbaren Farbpixel sind im Asset
radial auf höchstens 93 % begrenzt und bleiben deshalb vollständig innerhalb der Kontur;
die Kreismaske bleibt zusätzlich aktiv. Die unveränderte ID liegt weiterhin mittig darüber.

Werkzeug: **Pillow 12.1** und **CairoSVG 2.9**. ImageMagick wird nicht verwendet.

Ablage des Piloten: `bilder_pilot/bilder/<LAND>/<tid>.png`. Das Transportmanifest ist
nicht kanonisch; es dient ausschließlich zur Prüfung und zur Erzeugung eines separaten,
nicht angewendeten Neo4j-Property-Patches (`logo` / `none`).

---

## 5. Rechte

Der Bericht wird veröffentlicht. Das ist kein Nebenaspekt:

* **Logos sind Marken.** Ihre Wiedergabe zur Bezeichnung genau der Organisation, über die
  berichtet wird, ist der klassische Fall zulässiger Benutzung — aber sie darf keine
  Zusammenarbeit, Billigung oder Mitgliedschaft suggerieren. Die Abbildung zeigt ein
  Rechercheergebnis; das muss aus Bildunterschrift und Legende hervorgehen.
* **Nicht verändern über den Zuschnitt hinaus.** Nur trimmen, skalieren und beim Rendering
  kreisförmig beschneiden. Nicht umfärben, kombinieren oder nachzeichnen.
* **Wappen** öffentlicher Stellen unterliegen teils eigenen Regeln — bei Kommunen und
  Behörden Quelle und Lizenz notieren.
* **Fotos gar nicht erst aufnehmen** — sie scheitern ohnehin an Abschnitt 0, und ihre
  Rechtelage ist ungleich schwieriger als die von Marken.
* Jede Quelle wird ausschließlich im nicht-kanonischen Transportmanifest mit Abrufdatum,
  Quellenart, Lizenzhinweis und SHA-256 geführt. Ohne belastbare Quelle: ID-only.

---

## 6. Ablauf

    1. Kandidaten ernten     Skript über 47 bestätigte Pilotdomains:
                             apple-touch-icon, <link rel=icon>, favicon.ico, og:image
                             -> bilder_kandidaten/<tid>/*.png + Metadaten

    2. Automatisch sichten   verwerfen: < 128 px kürzester Kante, nicht quadratisierbar,
                             Kontrast zu gering, offensichtliches Foto
                             -> Rest geht in die Einzelentscheidung

    3. Einzelentscheidung    je Knoten: welche Kandidatin, oder Stufe 5-7 von Hand,
                             oder ID-only. Prüffrage aus Abschnitt 2.
                             Batches nach Land, wie bei den anderen Durchgängen

    4. Aufbereiten           Schritte 1-6 aus Abschnitt 4, einheitlich per Skript

    5. Prüfen                Vollständigkeit, Mindestgröße, Kontrast, Quellenangabe

    6. Setzen                semio-graph.sty um optionale Bildfüllung erweitern,
                             Renderer übergibt den Pfad; bestehende ID bleibt darüber

Schritt 1, 2, 4 und 5 sind mechanisch. Nur Schritt 3 braucht Urteil — und nur für die
Knoten, die Schritt 2 nicht schon entschieden hat.

## 7. Umfang

    Pilot: 48 Organisationen
      GB 16 · NL 16 · AT 16
      GB/NL je 12 graphgestützt + 4 Overlay
      AT 11 graphgestützt + 5 Overlay
      47 bestätigte Domains · 1 ohne belastbare aktuelle Domain
      Ergebnis nach 600-dpi-Druckprüfung: 11 Logo · 37 unveränderte ID-only-Knoten
      Patchstatus: 35 graphgestützt · 13 Overlay-only · nicht angewendet

Die Auswahl stammt aus dem final beschnittenen 859er-Netz; Projekte sind ausgeschlossen.
Innerhalb jedes Landes und Stratum rotiert die Auswahl nach Knotentyp, alterniert
URL-vorhanden/URL-fehlt soweit verfügbar und verwendet SHA-256 über `LAND:tid` als
stabile Sortierung. Das Auswahlmanifest hält diese Policy und den Hash des Graph-Exports
fest.

## 8. Was zuerst zu klären ist

1. **Label:** bestehende ID unverändert über dem Bild.
2. **Knotenradius:** 2,275 mm bleibt unverändert.
3. **Fallback:** keine Monogramme; unbrauchbare oder unbelegte Bilder ergeben ID-only.
4. **Rollout:** zuerst 48er-Druckpilot; kein automatischer Vollrollout auf 762 Organisationen.

## 9. Vollsammlung nach Pilotfreigabe (2026-08-13)

Auf ausdrückliche Erweiterung des Arbeitsumfangs wurde die reine Kandidatensammlung auf
alle **762 Organisationen** des finalen 859er-Netzes ausgedehnt; die **97 Projekte** bleiben
bildlos. Diese Stufe ist weiterhin Transport und Review, kein Rendering-Rollout und kein
Neo4j-Import.

* 447 Organisationsdomains einzeln bestätigt (47 Pilotentscheidungen, 400 dokumentierte
  Identitätsprüfungen); 291 Domainfälle bleiben offen, 24 haben keinen Domainkandidaten.
* 950 technisch zulässige Bildkandidaten für 366 Organisationen gesammelt; 81 bestätigte
  Domains lieferten in der festgelegten Kandidatenkette keinen zulässigen Treffer.
* SVG-Dateien sind unabhängig von einer gerenderten Mindestkante zulässig; Rasterbilder
  benötigen mindestens 128 px an der kürzesten Kante.
* Alle Kandidaten führen Quelle, Quellenart, Abrufdatum, Lizenznotiz, Reviewstatus sowie
  SHA-256 von Quelldatei und PNG-Vorschau.
* `pending_domain` und `no_usable_candidate` sind Sammlungszustände, keine endgültigen
  `none`-Entscheidungen. Jedes Bild bleibt bis zur visuellen und rechtlichen Einzelprüfung
  `review_status: pending`.

Artefakte: `bilder_full/selection.json`, `bilder_full/domains_review.json`,
`bilder_full/collection_manifest.json`, `bilder_full/contact_sheets/` und
`bilder_full/COLLECTION_REPORT.md`.
