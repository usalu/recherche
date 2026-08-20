# Vollreview der Beziehungsprofile und Erweiterungskanten

Datum: 2026-08-20  
Status: **Review abgeschlossen; keine Anwendung freigegeben.**  
Gegenstand: LaTeX-Akteursnetz, nicht Neo4j.

## Kurzurteil

Das vorgeschlagene Beziehungsprofil ist tragfaehig. Die zwei Hauptklassen
`Übergreifend` und `Einzelfall` trennen genau die vom Auftraggeber gewünschte
Frage: mehrere Vorhaben beziehungsweise eine allgemeine Struktur gegen einen
einzelnen abgegrenzten Fall. Die Unterklassen beschreiben die Grundlage der
Verbindung, ohne die konkrete Beziehungsbeschreibung zu wiederholen.

Die Erweiterung ist noch **nicht uebernahmebereit**. Nicht das Profilmodell ist
der Engpass, sondern Datenintegration, Identitaeten, echte Belegzitate und neun
konkrete Sachentscheidungen.

## Gepruefter Umfang

- aktueller sichtbarer Bestand: **618 Knoten, 264 Kanten, 78 Projekte,
  11 Laender und 9 separat gefuehrte Programme**;
- neue Recherche: **71 Projekte** und **193 vorgeschlagene neue Kanten**;
- einheitliches Review-Inventar: **457 Kanten** = 264 Bestand + 193 neu;
- alle **307 unterschiedlichen gespeicherten URLs** wurden erneut aufgerufen;
- **303** waren im automatischen Lauf erreichbar;
- **190 von 457** gespeicherten Zitaten wurden wortgleich gefunden;
- **189 Kanten** wurden wegen abweichender, ungenauer oder technisch nicht
  lesbarer Zitate manuell nachgeprueft;
- alle **108 Akteur-Akteur-Kanten** wurden einzeln einem Beziehungsprofil
  zugeordnet;
- alle **349 Akteur-Projekt-Kanten** (156 Bestand + 193 neu) sind strukturell
  `Einzelfall / Vorhaben`;
- weitere 48 Akteur-Akteur-Kanten gelten ebenfalls nur fuer ein einzelnes
  Vorhaben. Deshalb traegt das Profil insgesamt **397** Kanten.

Das vollstaendige Zeileninventar steht in `relationship_inventory.csv`; die
457 Profilvorschlaege stehen in `profile_proposals.json`.

## Gepruefte Ausgangsannahmen

### 1. Das Schema passt nicht 1:1

Bestaetigt. Die kanonischen Dateien liegen im Faktencheck-Ordner, nicht an den
im Uebergabebericht genannten Netz-Pfaden:

- `klassifikation_actor_project_final.json`: Schluessel sind interne Neo4j-EIDs;
- `kanten_klassifikation.json`: Schluessel sind IDs wie `DE:K031` und die
  Endpunkte sind interne EIDs.

Die Erweiterungsdaten verwenden dagegen `base:*`, `candidate:*`, `proj:*` und
`candidate-edge:*`. Richtung, kanonische Kanten-ID und Provenienz sind nicht
vollstaendig kompatibel. Eine direkte Kopie wuerde die Nachvollziehbarkeit
brechen.

### 2. Mehrfach vorkommende Akteure

Die automatische Kandidatenliste enthielt drei Faelle. Das Ergebnis:

1. **BAM Bouw en Techniek** und **Royal BAM Group / BAM Bouw en Techniek**
   meinen in den beiden Projektquellen dieselbe operative Gesellschaft.
   Zusammenfuehren und den Misch-Namen entfernen. Die Doorlaatpost-Quelle nennt
   ausdruecklich das Entwurfsteam von BAM Bouw en Techniek.
2. **Dura Vermeer** und **Dura Vermeer Bouw Zuid** nicht automatisch
   zusammenfuehren. Die Quellen schreiben Witte Paarden dem Konzernnamen,
   Avignonlaan aber ausdruecklich Bouw Zuid zu. Die Organisationsebene muss pro
   Projekt erhalten bleiben oder mit einer Parent-Child-Regel modelliert werden.
3. **IMd Raadgevende Ingenieurs** und **Van Rossum Raadgevende Ingenieurs** sind
   verschiedene Bueros. Der Aehnlichkeitstreffer ist falsch.

Bereits vorhandene Akteure wie Zirkular und baubuero in situ wurden in der
Erweiterung ueberwiegend korrekt wiederverwendet.

### 3. Die gedruckten Bestandszahlen sind veraltet

Bestaetigt. Der Renderer liest aktuell **618/264/78/11**; die separate
Programmliste enthaelt **9** Eintraege. Die Angabe `620/268/8` in
`akteursnetz.tex` ist vor der Erweiterung bereits falsch.

### 4. Wirkung der CLI-Befehle

Bestaetigt durch Quellcode und `--help`, ohne die schreibenden Befehle
auszufuehren:

- `abb`, `tables`, `tables-grid` und `programme` erzeugen Fragmente;
- `sync-images` kopiert freigegebene Bilder und entfernt dort nicht mehr
  manifestierte Dateien;
- `sync-fragments` kopiert erzeugte Fragmente in den Semio-Anhang.

Diese Befehle sind daher keine reinen Pruefkommandos und wurden in diesem
Review nicht ausgefuehrt.

## Kritische Integrationsfehler

### Zehn Bestandskanten verschwinden still

Der Erweiterungsentwurf uebernimmt nur 254 der sichtbaren 264 Bestandskanten.
Folgende zehn Kanten duerfen nicht ohne Einzelentscheidung verschwinden:

| ID | Verbindung | vorhandene Beziehungsart |
|---|---|---|
| AT:K004 | DRZ - MedUni Campus Wien | Projektbeteiligung, Aufgabe unklar |
| AT:K023 | Ferry-Dusika-Stadion Rueckbau - Job-TransFair | Projektbeteiligung, Aufgabe unklar |
| CH:K007 | ELYS - Zirkular | Projektbeteiligung, Aufgabe unklar |
| CH:K026 | K.118 Winterthur - Zirkular | Projektbeteiligung, Aufgabe unklar |
| CH:K036 | NEST/Empa-Eawag - UMAR Unit | Forschungsbegleitung |
| DE:K002 | Berlin-Schildow Pilot - Claus Asam | Pruefung und Nachweis |
| DE:K005 | Claus Asam - Mehrow Pilot House | Projektbeteiligung, Aufgabe unklar |
| NL:K019 | BioPartner 5 - Leiden University | Bauteillieferung |
| SE:K023 | Helsingborgshem - ReCreate Sweden/KTH | Konsortialpartner |
| SE:K025 | ReCreate Sweden/KTH - NCC | Konsortialpartner |

Mehrere gespeicherte Zitate stuetzen eine reale Beziehung. Der Entwurf muss
fuer jede Zeile entweder eine explizite Entfernung mit Grund oder eine saubere
Migration enthalten. Die Knoten bleiben bei einer Kantenentfernung sichtbar.

### Der Bestand wurde im Erweiterungsdatensatz semantisch verflacht

Die 254 uebernommenen Bestandskanten tragen dort nur generische Werte wie
`Organisationsbindung`, `Projektbeitrag` und den Satz
`Im abgeschlossenen Faktencheck belegte Verbindung.`. Deshalb darf der
FINAL-DATA-Block des Kandidatendokuments **nicht** als neue Wahrheit fuer den
Bestand verwendet werden. Die 264 kanonischen Bestandskanten muessen aus der
Faktencheck-Datei kommen; nur gepruefte neue Zeilen werden ergaenzt.

## Konkrete Sachentscheidungen vor einer Uebernahme

### A. Kante entfernen und korrekt neu modellieren

`candidate-edge:proposal:proj:108:B:3` verbindet **Norsk Folkemuseum** mit
**Nedre Sem Laave** als Projektbeitrag. Das ist sachlich falsch modelliert.
Belegt ist eine Materialweitergabe von Nedre Sem an das andere Projekt
**TradLab TRE** beim Museum. Loesung:

- diese Akteur-Projekt-Kante entfernen;
- TradLab TRE als eigenes Projekt aufnehmen;
- Norsk Folkemuseum mit TradLab TRE verbinden;
- die Materialherkunft Nedre Sem -> TradLab TRE nur modellieren, wenn
  Projekt-Projekt-Materialfluesse im Schema zugelassen werden.

Beleg: [Norsk Folkemuseum](https://norskfolkemuseum.no/handverkstunet) und
[FutureBuilt](https://www.futurebuilt.no/nyheter/med-fortiden-inn-i-futurebuilt).

### B. Eine verworfene Kante wieder aufnehmen

`proposal:proj:106:B:4` **Brukspecialisten AB -> Boras nya tingsraett** ist im
Entscheidungsblock `prune`, obwohl der spaetere Projekttext sie als belegt
beschreibt. Die offizielle Projektseite nennt 2.700 m2 wiederverwendete
Ziegelfassade. Loesung: denselben Brukspecialisten-Akteur wie bei proj:104
verwenden und die Kante als `Bauteillieferung` aufnehmen.

Beleg: [Brukspecialisten](https://brukspecialisten.se/projekt-post-type/boras-nya-tingsratt/).

### C. Quelle austauschen, Kante behalten

`proposal:rejected:P41-B03` **CONIX RDBM -> MULTI Brussels** kann als
`Einzelfall / Vorhaben` erhalten bleiben. Die gespeicherte Circubuild-Seite ist
404, aber Rotors Projektseite nennt CONIX RDBM und Whitewood und beschreibt
Rotors Unterstuetzung waehrend Entwurf und Bau. Grad bleibt `bezug`, nicht
`kern`; das Belegzitat und die URL muessen ersetzt werden.

Beleg: [Rotor MULTI](https://rotordb.org/en/projects/multi-de-brouckere-tower).

### D. Projektidentitaet Ekebackshoejd klaeren

Unter `proj:104` werden Quellen aus wahrscheinlich unterschiedlichen
Bauetappen zusammengefuehrt. Die Brukspecialisten-/Peab-/Stena-Quellen
beschreiben 397 Wohnungen und 385.000 wiederverwendete Ziegel. Die
nyaprojekt-Seite zu Liljewall nennt einen anderen Entwickler- und
Projektkontext. Loesung: Projektphase eindeutig benennen und entweder die
Liljewall-Kante einer zweiten Phase zuordnen oder einen gemeinsamen Primaerbeleg
finden. Keine Phase nur aus dem Ortsnamen ableiten.

### E. Projektname Caserne de Reuilly erweitern

`proj:95` heisst derzeit `Jardin de la Caserne de Reuilly`. Die zweitseitige
ADEME-Fiche belegt Ville de Paris und Paris Habitat als Projekttraeger des
gesamten Quartiers **La Caserne de Reuilly**, in dem der Garten nur ein Teil
ist. Loesung: Projektknoten in `La Caserne de Reuilly` umbenennen oder einen
garten-spezifischen Beleg beschaffen. Mit dem breiteren Projektnamen sind beide
Bauherrschaftskanten belegt.

### F. BTU-Kante bleibt offen

`candidate-edge:proposal:proj:115:A:1` **BTU Bauliches Recycling ->
Reihenhaeuser Hohenmoelsen** ist als `Forschungsbegleitung` noch nicht direkt
belegt. Der Artikel stammt von der BTU-Autorin und zeigt das Projekt als
Fallbeispiel, sagt aber nicht ausdruecklich, dass die BTU dieses konkrete
Vorhaben wissenschaftlich begleitet hat. Loesung: direkte Projektquelle finden;
sonst die Kante entfernen. `Projektbeteiligung, Aufgabe unklar` waere ebenfalls
zu stark, solange nur die Dokumentation belegt ist.

### G. Nicht mehr offene Belegprobleme

Folgende zuvor schwache Faelle konnten mit konkreten Passagen geklaert werden:

- Bellastock am Kaysersberg-Projekt sowie ADEME-Foerderung und kommunale
  Bauherrschaft: FCRBE-Fiche Seite 50;
- Bellastock bei Pulse: offizielle Bellastock-Projektseite;
- Bellastock bei Caserne Mellinet: Bellastock und Nantes Metropole
  Amenagement;
- ERNE am NEST Sprint: HUSNER nennt die Sicherung und Aufbereitung der
  Holzteile gemeinsam mit ERNE;
- HUSNER am Basel Pavillon und Sprint: eigene Projektuebersicht;
- die Rollen an uptownBasel Building 8: Projektseite von Schnetzer Puskas;
- BauKarussell - Job-TransFair und BauKarussell - pulswerk: beide sind
  Gruendungsmitglieder der Genossenschaft;
- Tscherning - GreenDozer: staendige Materiallieferungen sind im
  Geschaeftsbericht ausdruecklich genannt;
- Akademiska Hus, Vasakronan und Wiklunds: gemeinsame Absichtserklaerung und
  gemeinsamer Aufbau der KRETS-Materialdrehscheibe.

## Korrekturen an bestehenden Beziehungsarten

Das Profil ist klar, aber folgende vorhandene Detailtypen sind zu grob oder
falsch benannt:

| ID | Belegt | Profil | empfohlene Detailkorrektur |
|---|---|---|---|
| AT:K013 | Job-TransFair ist Gründungsmitglied von BauKarussell | Übergreifend / institutionell | `Konsortialpartner` -> `Gründung` oder gerichtete `Mitgliedschaft` |
| AT:K014 | pulswerk ist Gründungsmitglied von BauKarussell | Übergreifend / institutionell | `Konsortialpartner` -> `Gründung` oder gerichtete `Mitgliedschaft` |
| CH:K011 | RE-WIN nennt Zusammenarbeit mit baubüro in situ | Übergreifend / strategisch | `Zusammenarbeit, Art unklar` -> `Kooperationsvereinbarung`, falls keine formellere Grundlage auffindbar |
| DK:K010 | Tscherning liefert GreenDozer laufend Materialpartien | Übergreifend / operativ | `Zusammenarbeit, Art unklar` -> `Lieferbeziehung` |
| DK:K024 | GreenDozer-Angebote werden technisch in Circue eingebunden; Marktplatz zahlt Transaktionskosten | Übergreifend / operativ | `Kooperationsvereinbarung` -> `Dienstleistungsbeziehung` oder neuer Typ `Plattformanbindung` |
| SE:K003 | Akademiska Hus ist an Handslaget angeschlossen | Übergreifend / institutionell | `Konsortialpartner` -> gerichtete `Mitgliedschaft` |
| SE:K005 | Akademiska Hus und Wiklunds tragen eine gemeinsame KRETS-Absichtserklärung | Übergreifend / strategisch | `Konsortialpartner` -> `Kooperationsvereinbarung` |
| SE:K022 | Vasakronan ist an Handslaget angeschlossen | Übergreifend / institutionell | `Konsortialpartner` -> gerichtete `Mitgliedschaft` |
| SE:K029 | Vasakronan und Wiklunds tragen dieselbe KRETS-Absichtserklärung | Übergreifend / strategisch | `Konsortialpartner` -> `Kooperationsvereinbarung` |

CH:K004, CH:K006 und GB:K046 sind als `Übergreifend / operativ` tragfähig:
BTVZ beschreibt wiederkehrende Demontage/Aufbereitung durch Stiftung Chance;
useagain bindet den Bauteilladen Winterthur als Anbieter ein und leitet Anfragen
an ihn; HTS und Cleveland sind an mindestens Holbein Gardens und Timber Square
gemeinsam belegt.

## Beschreibungs- und Zitatqualitaet der Erweiterung

- alle 193 neuen Kanten haben eine URL und ein nichtleeres Zitatfeld;
- **177 von 193** Beschreibungen sind laenger als das geplante 60-Zeichen-Limit;
- viele Zitatfelder enthalten Pruefkommentare wie `URL erreichbar` oder
  `beide URLs bestaetigt` statt eines woertlichen Quellenzitats;
- die Zitate muessen vor einer Uebernahme durch kurze, relationstragende
  Originalpassagen ersetzt werden;
- erst danach koennen die 193 Beschreibungen als aktive Saetze mit maximal
  60 Zeichen vorgeschlagen und freigegeben werden.

Das Beziehungsprofil darf dabei nicht aus der Beschreibung erzeugt werden.
Beschreibung und Profil sind zwei unabhaengige Felder.

## Empfohlene naechste Freigabereihenfolge

1. Die sechs Sachentscheidungen A-F und die drei Identitätsentscheidungen
   bestätigen.
2. Fuer die zehn ausgelassenen Bestandskanten je `behalten` oder `entfernen`
   protokollieren; keine stille Entfernung.
3. Den Bestand aus den kanonischen 264 Kanten neu aufbauen und nur gepruefte
   Erweiterungskanten hinzufuegen.
4. Echte Belegzitate fuer die Erweiterung speichern und alle Beschreibungen auf
   maximal 60 Zeichen normalisieren.
5. Erst dann die Spalte `Beziehungsprofil` mit den 457 geprueften Vorschlaegen
   in die LaTeX-Tabelle integrieren.
6. Vor dem Anwenden einen neuen Zaehllauf machen. Erwartbare Aenderungen aus
   den Entscheidungen: Brukspecialisten +1, falsche Norsk-Folkemuseum-Kante -1;
   die BTU-Kante bleibt bis zur Quellenentscheidung offen.

## Artefakte

- `relationship_inventory.json` und `.csv`: alle 457 Kanten;
- `source_access_audit.json`: URL- und Zitatpruefung;
- `manual_batches/batch_01.md` bis `batch_10.md`: 189 manuell gepruefte
  Quellenfaelle;
- `profile_proposals.json`: Profilvorschlag fuer jede Kante;
- `BEZIEHUNGSPROFIL_TAXONOMIE_VORSCHLAG.md`: druckreife Taxonomiedefinition.

Keines dieser Artefakte ist `approved_for_apply`. Kanonische JSON-Dateien,
Renderer, Semio-Fragmente und LaTeX-Ausgaben wurden durch dieses Review nicht
veraendert.
