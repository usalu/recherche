# Entscheidungsliste Akteursnetz

Status: **Entschieden und lokal auf LaTeX angewendet am 20.08.2026.**

## Warum diese Entscheidungen nötig sind

Der bereinigte Bestand hat **618 Knoten und 262 Kanten**. Mit der geprüften
Erweiterung enthält das lokale LaTeX-Netz **809 Knoten und 452 Kanten**.

Kritisch bedeutet hier mindestens eines davon:

- eine reale Beziehung fehlt;
- eine falsche Beziehung würde gedruckt;
- zwei Akteure oder Projekte würden falsch zusammengeführt;
- eine vorhandene Kante verschwindet ohne Entscheidung;
- die Quelle belegt die behauptete Aufgabe nicht.

## 1. Taxonomie freigeben

### Vorschlag

Spaltenname: `Beziehungsprofil`  
`Beziehungsdauer` entfernen.

- `Projektübergreifend / institutionell`: formale Bindung
- `Projektübergreifend / strategisch`: gemeinsames übergeordnetes Ziel
- `Projektübergreifend / operativ`: Zusammenarbeit in mehreren Projekten
- `Vorhabenspezifisch / Vorhaben`: ein konkretes Projekt
- `Vorhabenspezifisch / Leistung`: ein einzelner Auftrag
- `Vorhabenspezifisch / Ereignis`: ein einzelner Vorgang

### Warum kritisch?

Das Profil muss etwas anderes sagen als die Beschreibung. Laufend/beendet ist
nicht relevant. Relevant ist: **mehrere Vorhaben oder nur ein Fall?**

### Entscheidung

**Freigegeben.**

## 2. Neun Sonderfälle

Alle Sonderfälle sind entschieden. Ergebnis: falsche oder nicht
hinreichend belegte Kanten entfernen; belegte Ersatzkanten, Quellenkorrekturen,
Umbenennung und Identitätsentscheidungen anwenden.

### 2.1 Norsk Folkemuseum - Nedre Sem Låve

- **Aktuell:** Norsk Folkemuseum ist mit dem Projekt Nedre Sem verbunden.
- **Belegt:** Holz aus Nedre Sem ging an das andere Projekt TradLab TRE.
- **Kritisch:** Die Kante hat den falschen Zielknoten und behauptet eine
  Projektbeteiligung am Spenderprojekt.
- **Entscheidung:** Falsche Kante entfernen; TradLab TRE als Projekt aufnehmen.
- **Entschieden:** **Entfernen und korrekt durch TradLab TRE ersetzen.**

### 2.2 Brukspecialisten - Borås nya tingsrätt

- **Aktuell:** Im Text als belegt beschrieben, in FINAL-DATA aber entfernt.
- **Belegt:** Die Quelle nennt Projekt und wiederverwendete Ziegel.
- **Nicht belegt:** Die genaue Lieferrolle von Brukspecialisten.
- **Entscheidung:** Ohne relationsspezifischen Beleg keine Kante.
- **Entschieden:** **Nicht aufnehmen.**

### 2.3 CONIX RDBM - MULTI Brussels

- **Aktuell:** Schlüssel heißt `rejected`, Kante wurde später dennoch behalten;
  die gespeicherte Circubuild-URL ist 404.
- **Belegt:** Rotor nennt CONIX RDBM und die Unterstützung während Planung und Bau.
- **Kritisch:** Status und Quelle widersprechen sich.
- **Entscheidung:** Behalten, Rotor-Quelle speichern, Grad `bezug`.
- **Entschieden:** **Behalten und Rotor-Quelle verwenden.**

### 2.4 Ekebäckshöjd

- **Aktuell:** Liljewall, Peab, Stena und Brukspecialisten hängen an einem
  Projektknoten.
- **Belegt:** Peab/Stena/Brukspecialisten beschreiben 397 Wohnungen und 385.000
  Ziegel. Die Liljewall-Quelle scheint eine andere Bauphase zu beschreiben.
- **Kritisch:** Zwei Bauphasen könnten als ein Projekt erscheinen.
- **Entscheidung:** Phasen trennen oder einen gemeinsamen Primärbeleg finden.
- **Entschieden:** **Liljewall-Kante entfernen; Peab-Etappe getrennt halten.**

### 2.5 Caserne de Reuilly

- **Aktuell:** Projektname ist `Jardin de la Caserne de Reuilly`.
- **Belegt:** Ville de Paris und Paris Habitat verantworten das gesamte Quartier;
  der Garten ist nur ein Teil davon.
- **Kritisch:** Die Quelle ist breiter als der Projektknoten.
- **Entscheidung:** In `La Caserne de Reuilly` umbenennen oder einen
  gartenspezifischen Beleg suchen.
- **Entschieden:** **In `La Caserne de Reuilly` umbenennen.**

### 2.6 BTU - Reihenhäuser Hohenmölsen

- **Aktuell:** `Forschungsbegleitung`.
- **Belegt:** Eine BTU-Autorin zeigt das Vorhaben als Fallbeispiel. Eine konkrete
  Forschungsbegleitung des Projekts wird nicht ausdrücklich genannt.
- **Kritisch:** Autorenschaft ist nicht automatisch Projektbeteiligung.
- **Entscheidung:** Direkten Beteiligungsbeleg finden; sonst Kante entfernen.
- **Entschieden:** **Entfernen.**

### 2.7 Zwei BAM-Namen

- **Aktuell:** `BAM Bouw en Techniek` und
  `Royal BAM Group / BAM Bouw en Techniek` sind zwei Kandidaten.
- **Belegt:** Beide Projektquellen nennen BAM Bouw en Techniek.
- **Kritisch:** Derselbe Akteur würde doppelt gedruckt.
- **Entscheidung:** Zu `BAM Bouw en Techniek` zusammenführen.
- **Entschieden:** **Zusammenführen.**

### 2.8 Dura Vermeer / Dura Vermeer Bouw Zuid

- **Aktuell:** Zwei ähnlich benannte Akteure.
- **Belegt:** Ein Projekt nennt den Konzernnamen, das andere ausdrücklich die
  regionale Gesellschaft Bouw Zuid.
- **Kritisch:** Zusammenführen könnte Leistungen der falschen Organisationsebene
  zuschreiben.
- **Entscheidung:** Getrennt lassen oder eine eigene Konzernbindung modellieren.
- **Entschieden:** **Getrennt lassen.**

### 2.9 IMd / Van Rossum

- **Aktuell:** Automatischer Ähnlichkeitstreffer.
- **Belegt:** Es sind verschiedene Ingenieurbüros.
- **Kritisch:** Ein Merge wäre sachlich falsch.
- **Entscheidung:** Getrennt lassen.
- **Entschieden:** **Getrennt lassen.**

## 3. Zehn Bestandskanten fehlen im Erweiterungsentwurf

Diese Kanten sind im aktuellen 264-Kanten-Bestand sichtbar, fehlen aber im
447-Kanten-Entwurf. Keine darf still verschwinden. Die Knoten bleiben auch bei
einer Kantenentfernung sichtbar.

| ID | Kontext und Risiko | Entscheidung |
|---|---|---|
| AT:K004 | DRZ ist als operativer Partner am MedUni Campus genannt; genaue Aufgabe fehlt. | **Entfernt:** konkrete Aufgabe nicht belegt. |
| AT:K023 | KÜMMEREI wird mit Träger BFI Wien/Job-TransFair genannt. | **Behalten:** soziale Rückbauarbeit und 25 Beschäftigte belegt. |
| CH:K007 | ELYS war Auslöser für die Gründung von Zirkular; keine konkrete Projektaufgabe belegt. | **Behalten:** `Gründungsimpuls`. |
| CH:K026 | K.118 war Auslöser für die Gründung von Zirkular; keine konkrete Projektaufgabe belegt. | **Behalten:** `Gründungsimpuls`. |
| CH:K036 | NEST ist Plattform, UMAR eine Unit; keine normale Akteur-Projekt-Kante. | **Behalten:** `Plattformzugehörigkeit`. |
| DE:K002 | Claus Asam ist eine Person; seine konkrete Testbauarbeit ist belegt. | **Behalten:** konkrete Errichtung von drei Testbauten. |
| DE:K005 | Claus Asam ist eine Person; Projektleitung ist belegt. | **Behalten:** Projektleitung und Mitinitiierung. |
| NL:K019 | Quelle belegt wiederverwendete Träger, aber keine klare bilaterale Beziehung BioPartner-Leiden. | **Entfernt:** keine bilaterale Beziehung belegt. |
| SE:K023 | Helsingborgshem ist Hauptpartner im schwedischen Pilot; KTH nimmt teil. | **Behalten:** gemeinsamer ReCreate-Pilot belegt. |
| SE:K025 | Quelle nennt Återhus-Partner, nicht eindeutig ReCreate Sweden. | **Behalten:** gemeinsame Återhus-Partnerschaft belegt. |

## 4. Abgeschlossene Pflichtprüfungen

### Quellen

- **190 neue Kanten:** alle besitzen URL und relationsspezifisches Zitat oder
  eine gespeicherte Prüfnotiz.

### Beschreibungen

- **190 neue Beschreibungen:** alle höchstens 60 Zeichen.

### Datenintegration

- Richtung, Kantenart, ID und Provenienz wurden in getrennte lokale
  Erweiterungsartefakte übertragen.
- Der bereinigte 262-Kanten-Bestand bleibt kanonische LaTeX-Basis; FINAL-DATA
  ersetzt ihn nicht.

### Abschlusskontrolle

- Gesamtstand geprüft: **809 Knoten / 452 Kanten / 11 Länder**.
- Alle 31 PDF-Seiten und alle Länderblöcke visuell geprüft.
- Jede sichtbare Kante besitzt Profil, Beschreibung und Quelle.
- Isolierte Knoten bleiben sichtbar.
- Keine Synchronisierung nach `E:\semio`; kein Git und kein Ticket.

## Was jetzt entschieden werden soll

Alle Entscheidungen wurden getroffen. Der lokale LaTeX-Bestand wurde erzeugt
und geprüft. Die Erweiterungskorrekturen stehen verbindlich in
`ERWEITERUNG_KORREKTUREN_FREIGEGEBEN.json`; das angewendete Ergebnis steht in
`erweiterung_final/akteursnetz_erweiterung_final.json`.
