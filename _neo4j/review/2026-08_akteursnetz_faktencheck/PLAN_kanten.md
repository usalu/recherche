# Plan: Beziehungsart und Beschreibung für alle Kanten

Ordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\`

## Abschlussstatus

**Vollständig ausgeführt am 2026-08-13 für den LaTeX-Graphen.** Alle 570 Kanten wurden
entschieden: 477 behalten, 93 entfernt. Keep und Remove bilden eine vollständige,
disjunkte Partition. Die Entfernungsliste ist im LaTeX-Loader aktiviert, das Fragment wurde
neu erzeugt und als PDF kompiliert. Es erfolgte kein Neo4j-Writeback. Siehe
`KANTEN_ABSCHLUSSBERICHT.md` und `KANTEN_LATEX_AUDIT.md`.

## Auftrag

570 gezeichnete Verbindungen bekommen je **Beziehungsart**, **Richtung** und eine kurze
**Beschreibung**, nach kontrolliertem Vokabular. Sonst nichts.

## Radikaler Grundsatz: Der Endgraph ist eine Positivliste

Eine gezeichnete Kante ist zunächst **nur ein Prüf-Kandidat**, keine Beziehung. Sie darf im
Endgraph nur bleiben, wenn eine zugängliche Quelle die **konkrete Beziehung zwischen genau
diesen beiden Knoten** belegt. Der Endgraph wird deshalb aus einer expliziten Keep-Liste
aufgebaut; er entsteht nicht dadurch, dass man nur einige offensichtlich schlechte Kanten
aus dem alten Netz entfernt.

Für jede Kante gilt binär:

* **KEEP:** Quelle nennt beide Knoten und beschreibt ihre konkrete Zusammenarbeit,
  Organisationsbeziehung oder Projektrolle.
* **DELETE:** alles andere — Verzeichnis-/Katalogeintrag, bloße Nennung, gemeinsame Branche,
  gemeinsamer Ort, gemeinsame Veranstaltung, gemeinsame Mitgliedschaft bei einem Dritten,
  Vermutung, nicht erreichbare Quelle oder erfolglose Recherche.

Es gibt **keinen Bestandsschutz** für gezeichnete oder früher als `belegt` bezeichnete
Kanten. Ein früherer Grad ist nur ein Konflikthinweis. Ohne heute prüfbaren Beleg wird die
Kante gelöscht. Eine Löschung kann nur durch erneute Klassifikation mit einer konkreten
Beleg-URL rückgängig gemacht werden.

Gegenstück zur Akteursklassifikation (`PLAN_klassifikation.md`): dort *was ein Akteur tut*,
hier *was zwei Knoten verbindet*.

## Freigabestatus

**Preflight abgeschlossen und freigegeben (2026-08-13).** Die Kanten stammen aus dem
Neo4j-Export vom 2026-08-10 plus den dokumentierten Overlays, Audit- und Prune-Dateien.
`kanten_batches/_index.json` enthält für jede Eingabe SHA-256, Größe und Laufkennung.

Vor Beginn und nach jeder Änderung an einer Quelle zwingend ausführen:

    python preflight_kanten.py

Nur `PREFLIGHT OK` gibt die Klassifikationsbatches frei. Bei geändertem Hash müssen Batches
und Prompts neu erzeugt werden. Das verhindert, dass ein veralteter Zeichnungs-Snapshot
stillschweigend als aktueller Neo4j-Stand behandelt wird.

## Vorgehen

In `kanten_prompts/` liegen **34 fertige Prompts** (`prompt_<LAND>_b<N>.md`), je ≤ 20
Kanten. Jeder ist vollständig — Taxonomie, Regeln und Kantendaten in einer Datei.

Für jeden Prompt:

1. Öffnen, abarbeiten.
2. Bei `GEPRUEFT` die Beleg-URL öffnen; bei `UNGEPRUEFT` aktiv nach einer Quelle suchen.
   Die Quelle muss **beide Knoten nennen und ihr konkretes Verhältnis beschreiben**.
3. Antwort — nur die Tabelle — als `kanten_results/kanten_<LAND>_b<N>.md` speichern.

Batches sind unabhängig, Reihenfolge egal, einzeln wiederholbar.

## Ausgabe je Kante

| ID | Beziehungsart | Richtung | Beschreibung | Beleg | Belegzitat |

Genau **eine** Art (keine Mehrfachnennung wie bei Akteursrollen), Richtung `A→B` / `B→A` /
`—`, Beschreibung ≤ 90 Zeichen. Jede positive Kante braucht zusätzlich ein wörtliches,
beziehungsspezifisches Belegzitat (≤ 240 Zeichen); eine URL ohne tragenden Textausschnitt
reicht nicht für KEEP.

## Zwei Vokabulare, nach Kantenart getrennt

Die Kantenart steht in jedem Block. Sie entscheidet, welches Vokabular gilt:

**`AKTEUR-BAUVORHABEN`** (318 Kanten) — was hat der Akteur *an diesem Vorhaben* getan:
`Bauherrschaft`, `Entwurf`, `Fachplanung`, `Reuse-Konzept`, `Bauteilinventarisierung`,
`Rückbau`, `Bauteillieferung`, `Aufarbeitung`, `Logistik`, `Bauausführung`,
`Prüfung und Nachweis`, `Forschungsbegleitung`, `Förderung`, `Betrieb`.
Falls die Beteiligung sicher, aber die konkrete Aufgabe nicht bestimmbar ist:
`Projektbeteiligung, Aufgabe unklar`.

**`AKTEUR-AKTEUR`** (252 Kanten) — welches organisatorische Verhältnis:
`Konsortialpartner`, `Kooperationsvereinbarung`, `Gemeinsames Bauvorhaben`, `Gründung`,
`Übernahme`, `Konzernbindung`, `Betreiberschaft`, `Mitgliedschaft`, `Trägerschaft`,
`Lieferbeziehung`, `Dienstleistungsbeziehung`, `Personelle Verflechtung`,
`Verzeichniseintrag`.
Falls die Zusammenarbeit sicher, aber ihre Form nicht bestimmbar ist:
`Zusammenarbeit, Art unklar`.

Die Vokabulare sind nicht austauschbar; der Validator weist eine Art aus dem falschen Block
zurück.

## Die vier Fallen

**Verzeichniseinträge sind keine Beziehung.** Die wichtigste Regel dieses Projekts. Eine
gemeinsame Listung bei Opalis, bauteilnetz, SalvoWEB, Bolius oder byggogbevar verbindet die
Gelisteten nicht miteinander — sie sagt nur, dass beide im selben Katalog stehen. Solche
Kanten bekommen `Verzeichniseintrag` und werden anschließend entfernt. Das ist derselbe
Maßstab, mit dem die Fan-Boxen entfernt wurden.

Auch eine Profilseite, ein Logo in einer Partnerübersicht oder eine gemeinsame Aufzählung
reicht nicht. `Mitgliedschaft` ist nur zulässig, wenn die Quelle ausdrücklich sagt, dass A
Mitglied von B ist. `Konsortialpartner` ist nur zulässig, wenn beide als Partner desselben
benannten Konsortiums oder Projekts ausgewiesen sind. Die Beweislast liegt immer bei KEEP.

**125 Kanten haben keine bereits geprüfte Quelle.** Sie sind als `UNGEPRUEFT` markiert. Sie kamen
über eine Datenbankbeziehung oder einen Rechercheüberlauf in die Zeichnung und wurden nie
einzeln geprüft. Hier muss aktiv gesucht werden; findet sich nichts, gilt `Kein Beleg für
eine Beziehung`. Das ist ein erwartetes Ergebnis, kein Fehler — **63 dieser 125 hängen an
den Verzeichnis-Hubs**.

**Richtung angeben.** Die Zeichnung ist ungerichtet, `Übernahme`, `Gründung`,
`Konzernbindung`, `Betreiberschaft`, `Mitgliedschaft`, `Trägerschaft`, `Lieferbeziehung`
und `Dienstleistungsbeziehung` sind es nicht. Die Lesart steht in Abschnitt 7 der
Taxonomie.

**Eine Art, nicht mehrere.** Treffen mehrere zu, gilt die Vorrangliste in Abschnitt 6: eine
dauerhafte Struktur schlägt eine punktuelle. Konsortialpartner, die zusätzlich im
Verzeichnis des anderen stehen, sind Konsortialpartner.

## Danach (nicht Aufgabe des klassifizierenden Agenten)

    python validate_kanten.py   # Vokabular, Richtung, Beleg, Längen, IDs und Dateien
    python merge_kanten.py      # validiert erneut; schreibt nur bei vollständigem Erfolg

`merge_kanten.py` berechnet Keep- und Entfernungsliste nach festen Regeln — nie durch ein
Modell beurteilt:

* **R-V** `Verzeichniseintrag` → entfernen
* **R-K** `Kein Beleg für eine Beziehung` → entfernen
* **R-N** `Beziehung nicht prüfbar` → entfernen
* **R-P** jede positiv klassifizierte und belegte Kante → behalten

`Beziehung nicht prüfbar` ist jetzt ausdrücklich ein Entfernungsgrund. Eine Zugriffssperre
ist ein ehrlicher Befund über die Recherche, aber kein Beleg für eine Graphbeziehung.

Außerdem vergleicht es das Ergebnis mit dem Kantengrad (`belegt`/`teilweise_belegt`), der
dem Klassifizierer bewusst **nicht** gezeigt wurde. Verwirft die Klassifikation eine früher
positiv bewertete Kante, erscheint sie zur Nachvollziehbarkeit in `kanten_konflikte.md`,
steht aber trotzdem in `prune_kanten_final.json`. Der Konfliktbericht ist kein Wartesaal.
Nur ein neuer, konkreter Beleg darf die Kante durch erneute Klassifikation in die Keep-Liste
zurückbringen.

## Belegstandard für KEEP

Eine positive Beziehungsart ist nur zulässig, wenn alle Punkte erfüllt sind:

1. Die Quelle ist erreichbar und ihre URL wird gespeichert.
2. Beide Endknoten sind eindeutig identifizierbar; reine Namensähnlichkeit genügt nicht.
3. Die Quelle beschreibt die Beziehung selbst, nicht nur zwei getrennte Tatsachen.
4. Die gewählte Art und — falls gerichtet — die Richtung gehen aus der Quelle hervor.
5. Die Beschreibung sagt konkret, was A und B verbindet.
6. Ein kurzes wörtliches Belegzitat dokumentiert genau die Textstelle, die die Beziehung trägt.

Bevorzugt werden offizielle Projekt-, Organisations-, Vergabe-, Unternehmens- oder
Institutionsseiten. Sekundärquellen sind zulässig, wenn sie die Beziehung eindeutig
beschreiben. Suchtreffer, Snippets, automatisch erzeugte Profile und aggregierte
Verzeichnisse sind kein ausreichender Beleg.

## Umfang

    570 gezeichnete Kanten
      Akteur–Bauvorhaben  318   (293 geprüft · 25 ungeprüft)
      Akteur–Akteur       252   (152 geprüft · 100 ungeprüft)

    AT 30 · BE 86 · CH 46 · DE 49 · DK 42 · FI 40 · FR 44 · GB 95 · NL 78 · NO 27 · SE 33

Die 88 bereits als `unklar` bewerteten Kanten sind hier nicht enthalten — sie wurden schon
aus der Zeichnung entfernt.

Ländergruppierung ist Absicht: die zu öffnenden Seiten sind dann überwiegend in einer
Sprache.

## Warum sich die Aufteilung der 570 Kanten geändert hat

Die Zeichnung selbst bleibt unverändert bei 570 Kanten. Der Ferry-Dusika-Stadion-Rückbau
war im Legacy-Overlay als Unternehmen markiert, ist für diese Prüfung aber eindeutig ein
Bauvorhaben. Ein expliziter, review-lokaler Override in
`kanten_node_kind_overrides.json` ordnet deshalb seine 12 gezeichneten Kanten dem
Akteur–Bauvorhaben-Vokabular zu. Er verändert weder Neo4j noch die Legacy-Zeichnungsquelle.

Ein zweiter Override korrigiert `Kv Återbruket, Litteraturgatan/Selma stad, Göteborg`
ebenfalls als Bauvorhaben. Seine beiden Kanten bezeichnen Entwurf und Bauausführung.

Damit verschiebt sich nur die Aufteilung: 318 statt 304 Akteur–Bauvorhaben und 252 statt
266 Akteur–Akteur. Die Gesamtzahl und die Faktenprüfungsabdeckung bleiben unverändert:
445 geprüft, 125 ungeprüft.

Dass die größten ungeprüften Bündel an Opalis (25), Bolius (15),
bauteilnetz (11), SalvoWEB (9) und byggogbevar (3) hängen, ist der Grund, diese Lücke jetzt
zu schließen: Verzeichniskanten sind nach den Projektregeln ausgeschlossen, sind aber
mangels Prüfung bisher in der Zeichnung geblieben.

## Neu erzeugen

    python build_kanten_batches.py         # kanten_batches/ aus dem gezeichneten Netz
    python assemble_kanten_prompt.py --all # kanten_prompts/ aus Taxonomie + batches
    python preflight_kanten.py              # Hashes, Vokabular, IDs, Typen, Prompts

## LaTeX-Anwendung und Provenienz

Die Markdown-Ergebnisse und erzeugten JSON-Dateien dokumentieren den geprüften
LaTeX-Zeichnungsstand. `merge_kanten.py` trägt Lauf, Snapshot, Quelldatei, Merge-Art,
Review-Status und Evidenzfelder in die Klassifikation ein.

`keep_kanten_final.json` ist die vollständige, belegte Positivliste des geprüften
570-Kanten-Snapshots. `prune_kanten_final.json` ist ihr vollständiges Komplement und wird
vom LaTeX-Loader als Ausschlussliste verwendet. Keep und Remove sind disjunkt und ergeben
zusammen exakt alle 570 geprüften Kanten. Neo4j ist für diesen Auftrag außerhalb des
Umfangs; es wurde nicht verändert.

## Dateien

| Datei | Zweck |
|---|---|
| `KANTEN_TAXONOMIE.md` | Prompt inkl. beider Vokabulare |
| `kanten_batches/` + `_index.json` | 34 Eingabeblöcke, ID-Register und Quell-Snapshot |
| `kanten_node_kind_overrides.json` | explizite review-lokale Typkorrektur |
| `kanten_prompts/` | 34 fertige, eigenständige Prompts |
| `kanten_results/` | hier die Antworten ablegen |
| `preflight_kanten.py` | Fail-closed Freigabe vor dem Start |
| `validate_kanten.py` | Regelprüfung |
| `merge_kanten.py` | Zusammenführung + vollständige Keep-/Entfernungslisten |
| `keep_kanten_final.json` | vollständige Positivliste: nur belegte Beziehungen |
| `prune_kanten_final.json` | vollständiges Komplement: alle unbelegten Kandidaten |
| `kanten_konflikte.md` | frühere positive Grade, die trotzdem entfernt werden |
| `KANTEN_ABSCHLUSSBERICHT.md` | alle Ergebnisse, Deutschland vollständig, alle 93 Entfernungen |
| `KANTEN_LATEX_AUDIT.md` | maschinelle Mengen- und LaTeX-Endkontrolle |
