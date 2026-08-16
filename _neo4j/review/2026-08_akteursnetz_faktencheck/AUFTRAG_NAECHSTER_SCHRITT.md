# Auftrag: Akteursnetz-Bildbestand — Sammel- und Auswahlagent

**Adressat:** der Agent, der Logokandidaten sammelt, filtert und auswählt.
Nur Sammlung, Identitätsprüfung und Bildaufbereitung.

**Nicht in diesem Auftrag:** Satz, Typografie und Tabellenlayout. Das liegt
beim Layoutagenten und wird hier auch dann nicht angefasst, wenn es beim
Prüfen auffällt — dort gemeldet, nicht selbst geändert. (Offen und dort
gemeldet: die Spaltenüberschrift steht am Kopf der AN.2-Seiten doppelt.)

Arbeitsordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck`
Bericht: `E:\semio\mit-bestand\bericht\zwischenbericht`

**Vor dem ersten Eingriff `ENTSCHEIDUNGEN.md` lesen.** Dort stehen die
getroffenen Entscheidungen mit Begründung — Deckkraft, Beschnitt, Dunkelbild,
Sperrlisten, Fragmenterzeugung, Prüfdisziplin. Wer dort einen Wert ändert,
ändert eine Entscheidung und muss die Begründung mitändern.

Stand 16.08.2026, alles gebaut und grün: 476 der 541 Organisationen tragen ein
Logo (88 %), Abbildungen und Tabellen übereinstimmend, `validate` 762/762 PASS,
Deckkraft 100 %, 90 `light_backdrop`-Overrides, beide PDFs neu. 39 Tests,
davon 2 rot (Aufgabe 2).

---

# Teil A — Aufgaben

## A1. Sperrregel `{"*"}` wirkt nicht (echter Fehler)

`MANUAL_CANDIDATE_REJECTIONS` kennt die Schreibweise `{"*": "Begründung"}` für
„diesen Knoten ganz sperren". `candidate_rejection` prüft aber nur

```python
if candidate.get("id") in manual:
```

— ein Eintrag `"*"` trifft damit **nie** eine echte Kandidaten-ID. Die Regel
ist im Auswahlcode wirkungslos; nur der Test wertet `'*'` aus.

10 Knoten tragen so eine Regel. 9 davon sind aus anderen Gründen `none`,
deshalb fiel es nie auf. `FR:M19` hat inzwischen einen Kandidaten, der alle
übrigen Filter besteht, und wurde dadurch trotz Sperre `logo`.

**Zu tun:** entweder `'*'` in `candidate_rejection` tatsächlich auswerten,
oder die 10 Einträge in präzise `MANUAL_CANDIDATE_URL_REJECTIONS` überführen
(bevorzugt, siehe `ENTSCHEIDUNGEN.md` Abschnitt 6: die Datei sperren, nicht den
Akteur). Danach prüfen, ob Knoten von `logo` auf `none` fallen, die es nicht
sollen.

## A2. Zwei rote Tests: veraltete Sperren, nicht kaputte Daten

```
FAIL test_final_visual_audit_rejections_stay_withheld
FAIL test_last_hunt_exact_marks_and_wrong_assets
```

Drei Knoten, alle drei in der Zweitprüfung vom 16.08.2026 ausdrücklich als
**richtig** bestätigt (`bilder_full/CURRENT_LOGO_REVERIFICATION_2026-08-16.md`):

| Knoten | Test erwartet | tatsächlich | Befund der Zweitprüfung |
|---|---|---|---|
| `FR:M19` Gauthey Cheminées | gesperrt | `logo` c01 | offizielles Gauthey-Wortzeichen |
| `GB:M09` Enviromate | `none` | `logo` | offizielles Wortzeichen, CDN gehört zur Website-Auslieferung |
| `BE:S03` SundaHus | `none` | `logo` | offizielles Zeichen in der iBinder-Gruppenfassung |

Bei `BE:S03` wurde `sundahus-horisontell-2` bereits bewusst aus der
URL-Sperrliste entfernt — die Daten sind also absichtlich aktualisiert, der
Test hinkt nach.

**Zu tun:** die drei Quellbilder ansehen, dann Sperren und Testerwartungen auf
den bestätigten Stand bringen. Nicht den Test anpassen, ohne vorher zu prüfen,
ob die Sperre oder die Daten veraltet sind.

---

# Teil B — Nicht anfassen

Diese Punkte sind offen, aber **keine Aufgabe**. Sie hängen an einer
Entscheidung des Auftraggebers. Hier steht nur, warum nichts zu tun ist —
damit sie nicht aus Hilfsbereitschaft doch angefasst werden.

## B1. Bildrechte — der eigentliche Blocker

474 der 476 Logos stehen auf `blocked_pending_permission`, 1 auf
`blocked_pending_legal_review`, 1 ist `conditional` lizenziert. Es wurde keine
Anfrage gestellt. Identität geprüft ≠ Veröffentlichung erlaubt.

**Keine Anfragen versenden, keine Rechte bewerten, keinen Knoten deswegen auf
`none` setzen.** Das ist eine geschäftliche und rechtliche Entscheidung.
Warteschlange zur Ansicht: `bilder_full/CURRENT_IMAGE_RIGHTS_AUDIT.csv`.

## B2. 65 Organisationen ohne Logo

FR 21 · CH 12 · GB 8 · DE 7 · BE 6 · DK 4 · NL 3 · NO 2 · SE 1 · FI 1

Der letzte Sammellauf holte für 53 dieser Knoten neue Kandidaten und ergab
**keinen einzigen brauchbaren** — alle scheitern weiterhin an den Identitäts-,
Foto- und Social-Media-Filtern.

**Keinen weiteren breiten Sammellauf starten.** Ob einzeln nachrecherchiert
oder der Stand als Endstand akzeptiert wird, entscheidet der Auftraggeber.

## B3. Textprüfung

`TEXTPRUEFUNG_RELEVANZ.csv` und `TEXTPRUEFUNG_BEZIEHUNGEN.csv` sind übergeben;
Korrekturen kamen noch nicht zurück.

**Nicht selbst umformulieren.** Erst wenn Korrekturen vorliegen, werden sie in
`klassifikation_actor_project_final.json` bzw. `kanten_klassifikation.json`
eingepflegt.

Nebenbefund zur Kenntnis: die gedruckte Tabelle kürzt beide Spalten bei
60 Zeichen auf Wortgrenze; 550 von 619 Relevanzsätzen sind betroffen, im Median
21 Zeichen, maximal 45. Der volle Text steht in den Daten.

## B4. Neo4j

**Kein Schreibzugriff, auch nicht probeweise.** Der vorbereitete Patch bleibt
unangetastet liegen (`full_image_property_patch.json`, `dry_run_only: true`,
412 Zeilen, nie angewandt).

---

# Ablauf nach jeder inhaltlichen Änderung

```bash
cd E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck
python full_image_collection.py finalize
python full_image_collection.py validate            # muss PASS sein
python full_image_collection.py current-finalize
python build_report_manifest.py

cd E:/recherche/_neo4j/netz
M=E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/bilder_full/report_image_manifest.json
python -m netz.cli sync-images  --images-manifest "$M"
python -m netz.cli abb          --images-manifest "$M"
python -m netz.cli tables-grid  --images-manifest "$M"
python -m netz.cli sync-fragments

cd E:/semio && bun run build:mit-bestand:zwischenbericht --skip-nx-cache
```

Danach prüfen:

1. `validate` PASS, Tests grün
2. alle Assets `max(alpha) == 255` (100 % Deckkraft)
3. `grep -c 'image='` in `akteursnetz-figuren.tex` gleich `grep -c 'SemioLogoFit'`
   in `akteursnetz-tabellen.tex`, beide plausibel
   — **0 heißt: `--images-manifest` vergessen**, dann druckt der Bericht
   klaglos leere Knoten
4. beide PDFs neuer als der Asset-Sync
5. Stichprobe im gebauten PDF **angesehen**, hell und dunkel — nicht nur Zahlen
   vergleichen
6. kein Neo4j-Write

Wer einen Knoten im PDF sucht: das aktuelle Netz nummeriert die `tid` neu.
Über die **`eid`** abbilden, sonst prüft man den falschen Knoten.
