# Plan: Rollen und Reuse-Relevanz für alle Knoten

Ordner: `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\`

## Auftrag

859 Knoten des Akteursnetzes bekommen je **Rolle(n)** und **Relevanz für
Wiederverwendung**, nach kontrolliertem Vokabular. Sonst nichts.

## Vorgehen

In `prompts/` liegen **49 fertige Prompts** (`prompt_<LAND>_b<N>.md`), je ≤ 20 Akteure.
Jeder ist vollständig — Taxonomie, Regeln und Akteursdaten in einer Datei. Nichts
zusammensuchen.

Für jeden Prompt:

1. Öffnen, abarbeiten.
2. Für jeden Akteur die **Beleg-URL öffnen** und dort die Tätigkeit lesen.
3. Antwort — nur die Tabelle — als `results/klass_<LAND>_b<N>.md` speichern.

Batches sind unabhängig, Reihenfolge egal, einzeln wiederholbar.

## Ausgabe je Akteur

| ID | Name | Rolle(n) | Relevanz für Wiederverwendung |

ID unverändert (`LAND:tid`), max. 3 Rollen aus dem Vokabular, Relevanz ≤ 90 Zeichen.

## Die vier Fallen

**Die Beleg-URL muss geöffnet werden.** Das mitgelieferte Belegzitat wurde erhoben, um
*einen Nachweis zu führen*, nicht um eine Tätigkeit zu beschreiben — Median 99 Zeichen, am
dünnen Ende `"Bouw antiek"`, `"Client: NREP"`, `"HSB Göteborg"`. Wer nur daraus
klassifiziert, rät. Das Zitat ist der Einstieg, die Seite ist die Evidenz.

**97 Einträge sind Gebäude, keine Organisationen.** In der Eingabe als
`BAUVORHABEN/OBJEKT` markiert. Sie bekommen ausschließlich `Referenzprojekt` bzw.
`Referenzprojekt, Reuse-Umfang unklar` (Regel P). Niemals eine Rolle vom beteiligten Büro
auf das Objekt übertragen oder umgekehrt.

**Alt-Rollen sind kein Beleg.** Altes 31-Kategorien-Schema, bei 372 der 859 Einträge gar
nicht vorhanden, nie verifiziert. Suchhinweis ja, Evidenz nein. Wird vom neuen Vokabular
ersetzt.

**Rückfallwerte setzen, wo die Evidenz nicht trägt.** Sie sind nicht die Normalantwort —
jeder Eintrag hat eine geprüfte Quelle —, aber ein geratener Rollenwert ist der teurere
Fehler.

## Danach (nicht Aufgabe des klassifizierenden Agenten)

    python validate_klassifikation.py   # Vokabular, IDs, Längen, Regel P
    python merge_klassifikation.py      # -> klassifikation.json

`merge_klassifikation.py` vergleicht das Ergebnis mit dem bereits vergebenen Reuse-Grad
(`kern`/`bezug`), der dem Klassifizierer bewusst **nicht** gezeigt wurde. Fällt die
Klassifikation auf einen Rückfallwert, obwohl ein Beleg vergeben ist, landet der Fall in
`klassifikation_konflikte.md` — Entscheidung von Hand, nichts wird automatisch umgestuft.

Das Rendering in die Druckanlage ist ein eigener Auftrag: `HANDOFF_table_build.md`.

## Umfang

    859 Knoten (762 Organisationen + 97 Bauvorhaben)
    AT 31 · BE 106 · CH 81 · DE 100 · DK 65 · FI 41 · FR 108 · GB 129 · NL 117 · NO 35 · SE 46

Ländergruppierung ist Absicht: die zu öffnenden Seiten sind dann überwiegend in einer
Sprache — in der Landessprache beurteilen, nicht über eine Übersetzung.

## Neu erzeugen

    python build_klassifikation_batches.py        # batches/ aus dem gezeichneten Netz
    python assemble_klassifikation_prompt.py --all # prompts/ aus Taxonomie + batches
