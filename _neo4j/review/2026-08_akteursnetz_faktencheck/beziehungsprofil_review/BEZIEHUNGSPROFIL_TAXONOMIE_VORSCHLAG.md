# Freigegebene Taxonomie: Beziehungsprofil

Status: **Am 20.08.2026 freigegeben und auf den aktuellen LaTeX-Bestand angewendet.**

## Empfohlene Tabellenspalten

| Spalte | Aufgabe |
|---|---|
| Beziehungsart | Was verbindet die beiden Knoten konkret? |
| Beschreibung | Was geschah konkret in diesem Fall? |
| Beziehungsprofil | Ist die Verbindung uebergreifend oder ein Einzelfall? |

`Beziehungsdauer` soll entfallen. Ob etwas noch laeuft, beendet ist oder ein
Enddatum hat, beantwortet nicht die entscheidende Frage. Entscheidend ist, ob
die Verbindung mehrere Vorhaben traegt oder nur einen abgegrenzten Fall.

## Kontrolliertes Vokabular

| Beziehungsprofil | Klare Bedeutung | Typische Faelle |
|---|---|---|
| `Projektübergreifend / institutionell` | Eine formale organisatorische Bindung besteht unabhängig von einem einzelnen Projekt. | Mitgliedschaft, Gründung, Tochtergesellschaft, Joint Venture, institutionelles Netzwerk |
| `Projektübergreifend / strategisch` | Die Akteure verfolgen über mehrere Projekte hinweg ein gemeinsames Ziel oder Programm. | Rahmenkooperation, gemeinsame Initiative, Absichtserklärung, gemeinsamer Marktaufbau |
| `Projektübergreifend / operativ` | Die Akteure arbeiten in mehreren Projekten praktisch oder geschäftlich zusammen. | wiederkehrende Lieferungen, Plattformanbindung, wiederholte Demontage- oder Aufarbeitungsleistung |
| `Vorhabenspezifisch / Vorhaben` | Die Verbindung gilt nur fuer ein benanntes Bau- oder Forschungsprojekt. | Planung, Lieferung, Rueckbau, Bauausfuehrung oder Forschung an einem Projektknoten |
| `Vorhabenspezifisch / Leistung` | Eine einzelne beauftragte Leistung ist belegt, aber kein eigener Projektknoten. | einmaliges Gutachten, einzelne Beratung, einzelne Lieferung |
| `Vorhabenspezifisch / Ereignis` | Ein einzelner Vorgang ist die ganze Verbindung. | einmalige Uebernahme, Materialuebergabe oder Gruendungsakt ohne fortbestehende Bindung |

## Entscheidungsregel

1. Gilt die Verbindung nur fuer ein benanntes Projekt, einen Auftrag oder ein
   Ereignis? Dann `Vorhabenspezifisch`.
2. Besteht sie nachweislich unabhängig von einem einzelnen Projekt oder über
   mehrere Projekte hinweg? Dann `Projektübergreifend`.
3. Bei `Projektübergreifend` entscheidet die Grundlage:
   formal-organisatorisch = `institutionell`, gemeinsames Ziel = `strategisch`,
   wiederholte praktische Leistung = `operativ`.
4. Bei `Vorhabenspezifisch` entscheidet der Rahmen:
   Projekt = `Vorhaben`, Auftrag = `Leistung`, isolierter Vorgang = `Ereignis`.

## Harte Grenzen

- Ein Projekt kann Jahre dauern und bleibt trotzdem `Vorhabenspezifisch / Vorhaben`.
- Eine einmalige Lieferung ist nicht `uebergreifend`, nur weil der Lieferant
  generell viele Projekte bearbeitet.
- Zwei Mitglieder desselben Netzwerks haben nicht automatisch eine bilaterale
  Beziehung. Eine direkte Koordination oder Vereinbarung muss belegt sein.
- Eine Gründung ist `Übergreifend / institutionell`, wenn daraus
  Mitgliedschaft, Eigentum oder eine dauerhafte Organisationsbindung entsteht.
- Die Klassifikation liest weder die bestehende Beschreibung noch fruehere
  `dauer*`-Felder. Sie wird aus Endpunkten, Beziehungsart und Quelle abgeleitet.

## Ergebnis der Vollklassifikation

| Profil | Alle 457 geprueften Kanten | Erweiterungsentwurf mit 447 Kanten |
|---|---:|---:|
| Projektübergreifend / institutionell | 38 | 38 |
| Projektübergreifend / strategisch | 7 | 7 |
| Projektübergreifend / operativ | 5 | 5 |
| Vorhabenspezifisch / Vorhaben | 397 | 387 |
| Vorhabenspezifisch / Leistung | 8 | 8 |
| Vorhabenspezifisch / Ereignis | 2 | 2 |

Alle 193 neuen Kanten fuehren von einem Akteur zu einem konkreten Projekt.
Deshalb sind sie im Beziehungsprofil strukturell `Vorhabenspezifisch / Vorhaben`.
Die konkrete `Beziehungsart` und die Beschreibung bleiben davon getrennt.
