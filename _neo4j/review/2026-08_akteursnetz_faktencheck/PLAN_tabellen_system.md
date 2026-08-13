# Plan: Ein Tabellensystem für Knoten und Beziehungen

Ordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\`

## 0. Stand

**Knotentabelle ist gebaut und kompiliert** (`table_grid.py`):

    ID | Name(34) | Rolle-Code | Relevanz(75) | Q      620 Knoten, 10 Seiten
    laufender Kolumnentitel = Land · Quellenliste je Land · 16er-Gruppenlegende

**Beziehungstabelle fehlt.** Die 268 gezeichneten Kanten sind im Diagramm reine
Linien ohne Unterscheidung (`\SemioGraphEdge{x,y}{x,y}`, kein `kind`-Argument),
und es gibt keine Tabelle, die sie erschließt. Wer zwei verbundene Kreise sieht,
kann nicht erkennen, *was* sie verbindet.

    268 gezeichnet   ·   je Land: CH 38 · GB 35 · NL 31 · FI 27 · FR 26 · DE 25
                                   SE 25 · BE 18 · AT 15 · NO 15 · DK 13
    26 Beziehungsarten · Richtung: 151 B→A, 56 A→B, 61 symmetrisch
    268/268 mit Beleg-URL

## 1. Befund vorab: die Beziehungs-Beschreibungen tragen kaum Information

    268 Kanten  ->  nur 65 verschiedene Beschreibungen, davon 40 nur einmal

        33x  "Beide sind als Partner desselben Konsortiums belegt."
        29x  "Der Akteur übernahm den architektonischen Entwurf."
        24x  "Der Akteur übernahm eine benannte Fachplanung."
        18x  "Der Akteur führte benannte Bauleistungen aus."

Diese Sätze wiederholen die Beziehungsart in anderen Worten — genau das, was die
Taxonomie in Abschnitt 8 ausdrücklich untersagt („Keine Wiederholung der
Beziehungsart", „wo möglich den **Namen der gemeinsamen Sache** nennen").

Wichtiger noch: **bei Akteur–Bauvorhaben-Kanten ist die Beschreibung strukturell
überflüssig.** Die gemeinsame Sache *ist* der zweite Endknoten. „M07 → P3,
Entwurf" sagt bereits alles; „Der Akteur übernahm den architektonischen Entwurf"
fügt nichts hinzu.

Die Lücke sitzt bei den Akteur–Akteur-Kanten: dort *wäre* der Name des
Konsortiums die eigentliche Information, und genau dort steht 33× „desselben
Konsortiums", ohne es zu nennen.

**Folgerung:** eine Beschreibungsspalte lohnt nur, wenn die 33 Konsortialkanten
nachgetragen werden. Sonst ist die breiteste Spalte die inhaltsärmste.

## 2. Gemeinsame Spaltengrammatik

Beide Tabellen sollen dieselbe Lesart haben. Die Entsprechung ist exakt:

| Rolle in der Zeile | Knotentabelle | Beziehungstabelle |
|---|---|---|
| Identität | `ID` | `Von → Nach` (zwei IDs) |
| Was es ist | `Name` | — (ergibt sich aus den IDs) |
| Klassifikation | `Rolle-Code` (A–P) | `Art-Code` |
| Prosa | `Relevanz` | `Beschreibung` |
| Beleg | `Q` | `Q` |

Beide: nach Land gruppiert, durchlaufend, laufender Kolumnentitel mit Landesname,
Quellennummern je Land neu beginnend, Codes über eine Legende erschlossen.

---

## Option A — Zwillingstabellen

Zwei getrennte Abschnitte, gleiche Grammatik.

    Knoten :  ID | Name | Rolle | Relevanz | Q
    Kanten :  Von → Nach | Art | Beschreibung | Q

    268 Kanten, einzeilig -> ~4 Seiten          Gesamt ~14 Seiten

**Dafür:** klarste Trennung; jede Tabelle für sich lesbar; kleinster Eingriff in
das Bestehende (die Knotentabelle bleibt unverändert).
**Dagegen:** wer ein Land verstehen will, blättert zwischen zwei Stellen; die
Beschreibungsspalte druckt den Befund aus Abschnitt 1 aus.

---

## Option B — Ein Landesblock, zwei Bänder

Je Land erst die Knoten, dann direkt darunter dessen Beziehungen, im selben
Abschnitt und unter demselben Kolumnentitel.

    Belgien · 62 Organisationen · 8 Projekte
      ID    Name                Rolle   Relevanz                   Q
      ...
      ── Beziehungen ────────────────────────────────────────────────
      Von → Nach   Art                  Beschreibung                Q
      ...

    Gesamt ~14 Seiten, aber alles zu einem Land an einer Stelle

**Dafür:** der Weg vom Diagramm ist ein Sprung, nicht zwei — Panel „Belgien"
führt auf genau einen Block, der Knoten *und* Kanten enthält. Am nächsten an der
Frage „was sehe ich hier eigentlich".
**Dagegen:** zwei verschiedene Spaltenköpfe auf einer Seite; das Band muss
optisch deutlich sein, sonst liest es sich als Fehler.

---

## Option C — Beziehungen in die Knotenzeile gefaltet

Keine eigene Beziehungstabelle. Jede Knotenzeile trägt ihre Verbindungen als
IDs mit Art-Code.

    ID    Name                Rolle   Verbindungen          Q
    U04   BLAF Architecten    C       →P1 Ent · →M12 Btl    12

    620 Zeilen, keine zusätzlichen Seiten  ->  bleibt bei 10 Seiten

**Dafür:** mit Abstand am kompaktesten und am intuitivsten — wer im Diagramm
eine Linie an `U04` sieht, findet sie in derselben Zeile, ohne zweite Suche.
354 der 620 Knoten sind ohnehin isoliert, die Spalte bleibt also meist leer.
**Dagegen:** jede Kante erscheint zweimal (an beiden Endknoten), 268 Kanten →
536 Einträge; die Relevanz muss dafür weichen oder kürzer werden; Richtung und
Beleg der Kante finden keinen Platz.

---

## 3. Empfehlung

**Option B**, mit der Beschreibungsspalte nur dort, wo sie etwas sagt:

* Akteur–Bauvorhaben: **keine** Beschreibung — Art + zweiter Endknoten genügt,
  siehe Abschnitt 1. Spart die breiteste Spalte für 2/3 aller Kanten.
* Akteur–Akteur: Beschreibung **nur mit dem Namen der gemeinsamen Sache**. Die
  33 Konsortialkanten müssten dafür nachgetragen werden (ein kleiner, klar
  begrenzter Rechercheauftrag: „welches Konsortium?").

Damit trägt jede gedruckte Zeile Information, und der Leser springt vom Panel
auf genau einen Landesblock.

## 4. Offen

1. **Option A, B oder C?**
2. **Die 33 Konsortialkanten nachtragen** (Name des Konsortiums) — oder
   Beschreibungsspalte bei Akteur–Akteur-Kanten weglassen?
3. **Die 209 nicht gezeichneten Beziehungen** (Endknoten wurde beim
   Strict-Review entfernt): als eigene Liste ausweisen oder aus dem Bericht
   nehmen?
4. **Kanten im Diagramm unterscheiden?** `semio-graph.sty` definiert bereits
   `muted`/`synth`/`hypo` als Kantenarten, die der Renderer nie benutzt. Die 26
   Arten zerfallen sauber in zwei Klassen — Projektrolle (Entwurf, Fachplanung,
   Bauherrschaft, Bauausführung …) und Organisationsbindung (Konsortialpartner,
   Gründung, Konzernbindung, Trägerschaft) — das wäre ein sichtbarer
   Unterschied ohne neue Mechanik.
