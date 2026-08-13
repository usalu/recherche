# LaTeX-Kantenaudit — Abschluss

Stand: 2026-08-13

## Ergebnis

- Entscheidungsmenge: **570 von 570** Kanten, keine fehlende und keine doppelte ID.
- Positive Liste: **477** belegte Beziehungen.
- Entfernungsliste: **93** Kandidaten.
- Mengenprüfung: Keep und Remove sind disjunkt und ergeben genau 570.
- LaTeX-Netzmodell: **477** Kanten; es ist mengenidentisch mit der positiven Liste.
- LaTeX-Fragment: **455** sichtbare Kanten in **11** Länderabbildungen.
- **22** belegte Kanten bleiben im Netzmodell, werden aber von der bestehenden
  Darstellungsregel „nur zusammenhängende Cluster ab drei Knoten“ nicht gezeichnet.
- Entfernte Kante noch im LaTeX-Netzmodell: **0**.
- Geprüfte Belegseiten: **220 von 220 erreichbar**.
- Kompilierte PDF-Endkontrolle: vorhanden, lesbar und visuell auf allen vier Seiten geprüft.

## Artefakte

- `keep_kanten_final.json`: vollständige Positivliste.
- `prune_kanten_final.json`: vollständige Entfernungsliste.
- `figs/frag_abb_netz.tex`: neu erzeugtes LaTeX-Fragment.
- `figs/_akteursnetz_final.pdf`: kompilierte Endkontrolle.
