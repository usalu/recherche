# Produktionsprompt: Normalisierte Klassifikation von Akteuren der baulichen Wiederverwendung

## Aufgabe

Klassifiziere jeden angegebenen Akteur nach:

1. **ID**
2. **Name**
3. **Rolle(n)**
4. **Relevanz für Wiederverwendung**

Die Klassifikation bezieht sich auf die Wiederverwendung im gebauten Umfeld, insbesondere auf:

* bestehende Gebäude
* Tragwerke
* Bauteile
* Bauprodukte
* Fassaden
* Innenausbau
* technische Anlagen
* Ausstattung und Mobiliar
* temporäre Bauten und modulare Systeme
* Informationen und Dienstleistungen, die deren Wiederverwendung direkt ermöglichen

Arbeite konservativ. Verwende nur Rollen, die durch die vorliegenden Informationen belegt sind. **Erfinde keine Tätigkeiten und leite keine Reuse-Rolle allein aus allgemeinen Begriffen wie „nachhaltig“, „zirkulär“, „innovativ“ oder „ressourcenschonend“ ab.**

---

## Eingabe

Jeder Akteur kommt als Block in dieser Form:

    ### <ID>
    - Name: <Name>
    - Land: <ISO2>
    - Typ (Altdaten, unbestaetigt): <Typ>
    - Eintragsart: BAUVORHABEN/OBJEKT (keine Organisation)      [nur bei Objekten]
    - Beleg-URL (MUSS geoeffnet werden): <URL>
    - Weitere URL: <URL>                                         [0–3 Stück]
    - Alt-Rollen (Altdaten, NICHT als Beleg verwenden): <a / b>  [optional]
    - Gespeichertes Belegzitat (Nachweis-Schnipsel …): "<Zitat>"

Behandle jeden Akteur unabhängig.

### Die Beleg-URL ist verpflichtend zu öffnen

Das gespeicherte Belegzitat wurde erhoben, um **einen Nachweis zu führen**, nicht um eine Tätigkeit zu beschreiben. Es ist im Median 99 Zeichen lang, im Einzelfall 11 Zeichen (`"Bouw antiek"`, `"Client: NREP"`, `"HSB Göteborg"`).

Eine Rollenzuordnung allein aus diesem Schnipsel wäre in den meisten Fällen entweder geraten oder würde unnötig auf einen Rückfallwert fallen. **Öffne daher für jeden Akteur die Beleg-URL** (bei Bedarf zusätzlich die weiteren URLs) und klassifiziere auf Basis der dort tatsächlich beschriebenen Tätigkeiten. Das Belegzitat dient nur als Einstiegspunkt.

Ist die Seite nicht erreichbar, klassifiziere aus dem Zitat, was belegbar ist, und verwende sonst den passenden Rückfallwert. Rate nicht.

### Alt-Rollen sind kein Beleg

Das Feld `Alt-Rollen` enthält Kategorien aus einem früheren, gröberen Schema (31 Kategorien, bei vielen Einträgen gar nicht vorhanden, nie einzeln verifiziert). Es darf als **Suchhinweis** dienen, niemals als Evidenz. Eine Rolle nur dann vergeben, wenn die geöffnete Seite sie trägt. Das alte Schema wird durch das kontrollierte Vokabular dieses Prompts **ersetzt**, nicht ergänzt.

### Keine Übertragung zwischen Akteuren

Übertrage keine Tätigkeiten:

* von einem Partner auf einen anderen Partner
* von einer Muttergesellschaft auf eine Tochtergesellschaft
* von einem Netzwerk auf einzelne Mitglieder
* von einem Projekt auf alle beteiligten Akteure
* von einer Person auf deren gesamte Organisation
* von einer Organisation auf alle ihre Mitarbeitenden

---

## Ausgabeformat

Gib ausschließlich eine Tabelle mit genau diesen Spalten aus:

| ID | Name | Rolle(n) | Relevanz für Wiederverwendung |
| -- | ---- | -------- | ----------------------------- |

Dabei gelten folgende Formatregeln:

* Genau eine Zeile pro eingegebenem Akteur.
* **ID unverändert aus dem Eingabeblock übernehmen** (Format `LAND:tid`, z. B. `BE:M07`). Die ID ist zwingend: mehrere Akteure tragen denselben Namen, der Name allein ist kein Schlüssel.
* Namen unverändert aus der Eingabe übernehmen, auch bei Sonderzeichen.
* Reihenfolge der Akteure beibehalten.
* Keine Akteure auslassen.
* Keine zusätzlichen Erklärungen vor oder nach der Tabelle.
* Mehrere Rollen mit `/` trennen.
* Den Schrägstrich ausschließlich als Rollentrenner verwenden.
* Keine Aufzählungen, Klammern oder Zusatzkommentare in der Rollen-Spalte.
* Rollen nur aus dem kontrollierten Vokabular dieses Prompts verwenden.
* **Höchstens 3 Rollen** je Akteur, in der Reihenfolge aus Abschnitt 5. Sind mehr belegt, nenne die drei prozessrelevantesten.
* Die Relevanz als einen kurzen vollständigen Satz formulieren, **höchstens 90 Zeichen**.
* Keine Quellen, URLs oder Bewertungen in die vier Ausgabespalten einfügen.

---

# 1. Definition von Wiederverwendung

## Als Wiederverwendung klassifizieren

Eine Tätigkeit ist für diese Klassifikation relevant, wenn sie direkt dazu beiträgt, dass ein vorhandenes Gebäude, Bauteil, Produkt oder eine technische Anlage:

* weitergenutzt wird
* in einem anderen Projekt erneut eingesetzt wird
* demontiert und erhalten wird
* repariert wird
* aufgearbeitet wird
* angepasst oder umgenutzt wird
* geprüft und für einen Wiedereinsatz freigegeben wird
* gelagert oder transportiert wird
* dokumentiert und auffindbar gemacht wird
* vermittelt, verkauft, vermietet oder weitergegeben wird
* durch Beschaffung, Finanzierung, Regulierung oder Planung ermöglicht wird
* durch Standards, Ausbildung, Daten oder spezialisierte Methoden unterstützt wird

Die Identität beziehungsweise Funktion des Gebäudes, Bauteils oder Produkts muss dabei weitgehend erhalten bleiben.

## Ebenfalls einschließen

Folgende Tätigkeiten können zur Wiederverwendung gehören, sofern ein direkter Bezug belegt ist:

* Bestandserhalt
* Gebäudetransformation
* adaptive Umnutzung
* Reparatur
* Instandhaltung
* Refurbishment
* Rekonditionierung
* Remanufacturing
* Wiederaufbereitung
* Wiederverkauf
* Secondhand-Handel
* selektiver Rückbau
* Urban Mining
* Bauteilbörsen
* Materialpässe
* Rücknahmesysteme
* Produkt-Service-Systeme
* Vermietung wiederverwendbarer Systeme
* Wiederverwendung temporärer Konstruktionen
* Nutzung gebrauchter Bauteile in Kunst, Ausstellungsbau oder Produktgestaltung

Ordne diese Begriffe nicht direkt als Rollen zu. Übersetze sie in die konkreten bevorzugten Rollen des kontrollierten Vokabulars.

---

# 2. Abgrenzung zu benachbarten Themen

## Nicht automatisch als Wiederverwendung klassifizieren

Folgende Themen reichen allein nicht für eine Reuse-Klassifikation:

* Kreislaufwirtschaft
* Nachhaltigkeit
* Klimaschutz
* CO₂-Reduktion
* Ressourceneffizienz
* Abfallvermeidung
* Recyclingfähigkeit
* Materialeffizienz
* biobasierte Baustoffe
* emissionsarme Baustoffe
* neue kreislauffähige Produkte
* Lebenszyklusanalysen
* ESG
* Cradle to Cradle
* regenerative Architektur
* nachhaltiges Bauen
* grüne Finanzierung

Ein direkter Beitrag zur Weiter- oder Wiederverwendung muss zusätzlich belegt sein.

## Recycling ist nicht Wiederverwendung

Nicht als direkte Wiederverwendung klassifizieren:

* Zerkleinern von Beton zu Recyclinggranulat
* Einschmelzen von Metall
* Zerfasern von Holz
* chemische Rückgewinnung
* Herstellung neuer Produkte aus Recyclingrohstoffen
* thermische Verwertung
* Kompostierung
* Deponierung
* Downcycling

Ein Recyclingunternehmen darf nur als Reuse-Akteur klassifiziert werden, wenn es zusätzlich Bauteile oder Produkte unzerstört sichert, aufarbeitet, vermittelt oder wieder einsetzt.

## Konventioneller Abbruch ist nicht selektiver Rückbau

Ein Abbruchunternehmen erhält nur die Rolle `Selektiver Rückbau`, `Demontage` oder `Bergung`, wenn ausdrücklich belegt ist, dass Bauteile zerstörungsarm ausgebaut und für eine weitere Nutzung erhalten werden.

## Renovierung ist nicht automatisch Wiederverwendung

Eine Sanierung oder Modernisierung ist nur relevant, wenn sie:

* bestehende Gebäudestrukturen erhält
* vorhandene Bauteile weiterverwendet
* Bauteile aus anderen Projekten integriert
* die Nutzungsdauer bestehender Komponenten verlängert

Ein gewöhnlicher Innenausbau oder Austausch gegen neue Produkte reicht nicht aus.

---

# 3. Evidenzregeln gegen falsche Zuordnungen

## Zulässige Evidenz

Eine Rolle darf vergeben werden, wenn mindestens eine der folgenden Informationen vorliegt:

* ausdrückliche Beschreibung einer Dienstleistung
* dokumentierte Projektaufgabe
* konkrete Produkt- oder Plattformfunktion
* offizielle Tätigkeitsbeschreibung
* nachvollziehbare Beschreibung eines ausgeführten Prozesses
* eindeutige Zuordnung innerhalb eines Projekts
* konkrete Beschreibung eines Reuse-Programms

## Unzureichende Evidenz

Folgende Informationen reichen nicht allein:

* Name des Akteurs
* Firmenname mit Begriffen wie „Circular“, „Green“, „Reuse“ oder „Sustainable“
* allgemeines Leitbild
* Marketing-Slogan
* Mitgliedschaft in einem Netzwerk
* Teilnahme an einer Veranstaltung
* Erwähnung als Projektpartner ohne Aufgabenbeschreibung
* Standort in einem Reuse-Hub
* Zugehörigkeit zu einer Universität
* Zugehörigkeit zu einer Behörde
* Zugehörigkeit zu einem Architektur- oder Ingenieurbüro
* einmalige Erwähnung ohne erkennbare Funktion

## Quellenkonflikte

Bei widersprüchlichen Informationen:

1. aktuelle konkrete Tätigkeitsbeschreibungen bevorzugen
2. offizielle Projekt- oder Dienstleistungsseiten gegenüber allgemeinen Verzeichnissen bevorzugen
3. konkrete Aufgaben gegenüber allgemeinen Selbstbeschreibungen bevorzugen
4. bei nicht auflösbarem Widerspruch nicht raten

## Historische Tätigkeiten

Eine historische Reuse-Rolle nur dann verwenden, wenn:

* sie ausdrücklich dokumentiert ist
* keine aktuellere gegenteilige Information vorliegt
* die Eingabe historische Tätigkeiten einschließt

Eine historische Einzelaktivität nicht automatisch als heutiges dauerhaftes Geschäftsmodell darstellen.

---

# 4. Rückfallwerte

Jeder hier vorgelegte Akteur hat eine geprüfte Beleg-URL. Ein Rückfallwert ist deshalb **nicht** die erwartete Normalantwort, sondern eine begründete Ausnahme — meistens, wenn die Seite nicht mehr erreichbar ist oder nur den Namen bestätigt, ohne eine Tätigkeit zu beschreiben.

Setze ihn trotzdem ohne Zögern, wenn die Evidenz nicht trägt. Ein geratener Rollenwert ist der teurere Fehler.

## Unzureichende Informationen

Verwende:

**Rolle(n):**
`Unzureichende Informationen`

**Relevanz:**
`Die vorliegenden Informationen reichen für eine belastbare Einordnung nicht aus.`

Diesen Wert verwenden, wenn nicht erkennbar ist, was der Akteur konkret macht.

## Reuse-Bezug erkennbar, konkrete Rolle unklar

Verwende:

**Rolle(n):**
`Reuse-Bezug belegt, Rolle unklar`

**Relevanz:**
`Ein direkter Reuse-Bezug ist belegt, die konkrete Funktion bleibt jedoch unklar.`

Diesen Wert nur verwenden, wenn Wiederverwendung ausdrücklich genannt wird, die ausgeführte Tätigkeit aber nicht bestimmbar ist.

## Keine direkte Reuse-Rolle

Verwende:

**Rolle(n):**
`Keine direkte Reuse-Rolle belegt`

**Relevanz:**
`Aus den Informationen ist kein direkter Beitrag zur Wiederverwendung ableitbar.`

Diesen Wert verwenden, wenn die Tätigkeit zwar mit Nachhaltigkeit, Bauwesen oder Recycling verbunden ist, aber keine direkte Wiederverwendungsfunktion belegt ist.

---

# 4b. Regel P — Bauvorhaben und Objekte

Ein Teil der Einträge sind **keine Organisationen**, sondern Gebäude, Pilotprojekte oder Bauvorhaben. Sie sind in der Eingabe mit `Eintragsart: BAUVORHABEN/OBJEKT` markiert. Sie haben keine Rolle im Prozess — sie **sind** der Gegenstand der Wiederverwendung, nicht ein Akteur, der etwas tut.

Das Rollenvokabular der Abschnitte 6 und 7 ist auf solche Einträge nicht anwendbar. Verwende stattdessen genau einen der beiden folgenden Werte:

### `Referenzprojekt`

Verwenden, wenn am konkreten Bauvorhaben belegt Bauteile wiederverwendet, erhalten, umgenutzt oder zerstörungsarm ausgebaut wurden.

**Relevanz:** ein Satz nach den Regeln aus Abschnitt 8, der beschreibt, **was am Objekt wiederverwendet wurde**, nicht wer es getan hat. Beispiele:

    Verbaut 30.000 geborgene Ziegel aus acht Abbruchstellen in der neuen Fassade.
    Erhält die bestehende Tragstruktur und ergänzt sie mit gebrauchten Bauteilen.

### `Referenzprojekt, Reuse-Umfang unklar`

**Relevanz:**
`Das Bauvorhaben ist als Reuse-Referenz belegt, der konkrete Bauteilumfang bleibt offen.`

Verwenden, wenn der Reuse-Bezug des Objekts belegt ist, aber nicht erkennbar wird, welche Bauteile betroffen sind.

Übertrage niemals eine Rolle von einem beteiligten Büro auf das Objekt — oder umgekehrt. Das ist die häufigste Verwechslung in diesem Datensatz.

---

# 5. Regeln für die Rollen-Spalte

## Grundprinzip

Rollen beschreiben, **was ein Akteur im Wiederverwendungsprozess tatsächlich tut**.

Nicht beschreiben:

* Rechtsform
* Größe
* Standort
* Eigentümerstruktur
* allgemeine Branche
* institutionellen Status
* Projektname
* Selbstbezeichnung ohne konkrete Funktion

## Mehrere Rollen

Wenn ein Akteur mehrere klar unterschiedliche Funktionen erfüllt, alle belegten Funktionen nennen — höchstens jedoch drei.

Beispiel:

`Bauteilinventarisierung / Selektiver Rückbau / Lagerung`

Nicht jede einzelne Arbeitshandlung als eigene Rolle aufspalten. Eng zusammengehörige Tätigkeiten mit dem passendsten Oberbegriff normalisieren.

## Redundanz vermeiden

Nicht gleichzeitig Oberbegriff und nahezu identischen Unterbegriff verwenden.

Beispiele:

* Nicht: `Bauteilhandel / Verkauf`

* Verwenden: `Bauteilhandel`

* Nicht: `Vermittlung / Vermittlungsplattform`, wenn ausschließlich eine automatisierte Plattform betrieben wird

* Verwenden: `Vermittlungsplattform`

* Nicht: `Technische Prüfung / Tragfähigkeitsprüfung`, wenn ausschließlich die Tragfähigkeit geprüft wird

* Verwenden: `Tragfähigkeitsprüfung`

* Nicht: `Aufarbeitung / Refurbishment`

* Verwenden: `Aufarbeitung`

## Spezifität

Verwende die spezifischste belegte Rolle.

Beispiele:

* `Tragwerksplanung` statt `Engineering`
* `Bauteilinventarisierung` statt `Beratung`
* `Materialprüfung` statt `Forschung`
* `Vermittlungsplattform` statt `Digitalisierung`
* `Selektiver Rückbau` statt `Bauunternehmen`
* `Richtlinienentwicklung` statt `Netzwerk`
* `Weiterbildung` statt `Bildung`, wenn Fortbildungen angeboten werden

Verwende keinen spezifischeren Begriff, als die Evidenz erlaubt.

## Reihenfolge der Rollen

Rollen in dieser Reihenfolge anordnen:

1. Eigentum, Bauherrschaft, Finanzierung und Regulierung
2. Strategie, Planung und Design
3. Inventarisierung, Suche und Beschaffung
4. Bewertung, Prüfung und Qualitätssicherung
5. Rückbau, Demontage und Bergung
6. Reparatur, Aufarbeitung und Anpassung
7. Lagerung, Logistik und Vermittlung
8. Bauausführung und Wiedereinbau
9. Betrieb und Nutzungsdauerverlängerung
10. Daten, Methoden, Bildung, Standards und Vernetzung
11. soziale Zusatzfunktionen

---

# 6. Kontrolliertes Rollenvokabular

Verwende ausschließlich die folgenden Rollen, einen der drei Rückfallwerte oder — bei Objekten — einen der beiden Regel-P-Werte.

## A. Eigentum, Nachfrage und Projektinitiierung

### `Bauherrschaft`

Verwenden, wenn der Akteur ein Bauprojekt beauftragt, zentrale Entscheidungen trifft oder Reuse ausdrücklich als Projektziel vorgibt.

Nicht automatisch für jeden Gebäudeeigentümer verwenden.

### `Gebäudeeigentum`

Verwenden, wenn der Akteur Gebäude oder Portfolios besitzt und über Erhalt, Umbau, Rückbau oder Freigabe von Bauteilen entscheidet.

### `Projektentwicklung`

Verwenden, wenn der Akteur Projekte, Nutzungskonzepte oder Geschäftsmodelle für bestehende Immobilien entwickelt.

### `Portfoliomanagement`

Verwenden, wenn Wiederverwendung über mehrere Gebäude oder ein Immobilienportfolio hinweg koordiniert wird.

### `Projektsteuerung`

Verwenden, wenn Termine, Kosten, Verantwortlichkeiten und Schnittstellen eines Reuse-Projekts gesteuert werden.

### `Programmmanagement`

Verwenden, wenn ein Akteur ein übergeordnetes Reuse-Programm mit mehreren Projekten oder Beteiligten führt.

### `Investor`

Verwenden, wenn Eigenkapital bereitgestellt und finanzielles Projektrisiko übernommen wird.

### `Finanzierung`

Verwenden für Kredite, Finanzierungsprodukte oder andere Kapitalbereitstellung.

### `Fördermittelvergabe`

Verwenden für Zuschüsse, Förderprogramme, Stipendien oder öffentliche Finanzhilfen.

### `Beschaffung`

Verwenden, wenn gebrauchte Bauteile, Reuse-Dienstleistungen oder entsprechende Planungsleistungen eingekauft werden.

### `Öffentliche Beschaffung`

Verwenden, wenn eine öffentliche Stelle Reuse-Kriterien in Ausschreibungen, Wettbewerben oder Vergabeverfahren verankert.

### `Versicherung`

Verwenden, wenn Versicherungs- oder Gewährleistungsmodelle für gebrauchte Bauteile angeboten werden.

---

## B. Regulierung, Recht und institutionelle Rahmenbedingungen

### `Regulierung`

Verwenden, wenn Gesetze, Verordnungen, verbindliche Vorgaben oder politische Regelungen entwickelt oder umgesetzt werden.

### `Genehmigung und Aufsicht`

Verwenden für Baubewilligungen, behördliche Prüfungen und die Überwachung regulatorischer Anforderungen.

### `Rechtsberatung`

Verwenden für rechtliche Beratung zu Haftung, Eigentum, Gewährleistung, Vergabe oder Reuse-Verträgen.

### `Vertragsgestaltung`

Verwenden, wenn spezifische Verträge, Vertragsmuster oder Leistungstexte für Reuse entwickelt werden.

### `Politikberatung`

Verwenden, wenn politische Entscheidungsträger fachlich beraten werden, ohne dass der Akteur selbst verbindliche Regeln erlässt.

### `Reuse-Strategie`

Verwenden, wenn Reuse-Roadmaps, Organisationsstrategien oder übergeordnete Umsetzungskonzepte entwickelt werden.

### `Reuse-Beratung`

Nur verwenden, wenn eine direkte, aber fachlich breit angelegte Reuse-Beratung belegt ist und keine spezifischere Rolle die Tätigkeit ausreichend beschreibt.

`Beratung` allein ist nicht zulässig.

---

## C. Architektur, Planung und Gestaltung

### `Architektur`

Verwenden, wenn Gebäude oder bauliche Projekte entworfen und dabei bestehende oder gebrauchte Elemente integriert werden.

### `Innenarchitektur`

Verwenden für die Planung von Innenräumen mit erhaltenen oder gebrauchten Elementen.

### `Landschaftsarchitektur`

Verwenden für die Wiederverwendung von Freiraumelementen, Belägen, Mauern, Pflanzen oder Außenbauteilen.

### `Stadt- und Arealplanung`

Verwenden für Wiederverwendungsstrategien auf Quartiers-, Stadt- oder Arealebene.

### `Bestandsentwicklung`

Verwenden, wenn bestehende Gebäude weiterentwickelt werden, anstatt sie zu ersetzen.

### `Umnutzungsplanung`

Verwenden für die Planung einer neuen Nutzung bestehender Gebäude oder Strukturen.

### `Reuse-Planung`

Verwenden für die konkrete Integration gebrauchter Bauteile in Planung, Ausschreibung und Umsetzung.

### `Materialberatung`

Verwenden für die Auswahl und Einsatzberatung zu vorhandenen oder wiederverwendeten Materialien.

### `Technische Planung`

Nur als Oberbegriff verwenden, wenn eine technische Planungsleistung belegt, aber keine genauere Disziplin bestimmbar ist.

### `Tragwerksplanung`

Verwenden für statische Planung mit bestehenden oder gebrauchten Tragwerkselementen.

### `Gebäudetechnikplanung`

Verwenden für Wiederverwendung oder Weiterbetrieb von Heizungs-, Lüftungs-, Sanitär-, Elektro- oder anderen technischen Anlagen.

### `Bauphysik`

Verwenden für Wärme-, Feuchte-, Schall- oder bauphysikalische Bewertung im Zusammenhang mit Reuse.

### `Brandschutzplanung`

Verwenden für brandschutztechnische Planung wiederverwendeter Bauteile oder Bestandsgebäude.

### `Schadstoffplanung`

Verwenden für Planung und Management schadstoffbelasteter Bauteile mit Blick auf sicheren Erhalt oder Ausbau.

### `Kostenplanung`

Verwenden für Kostenberechnung, Kostenschätzung oder Kostensteuerung von Reuse-Prozessen.

### `Ausschreibung und Vergabe`

Verwenden für die Formulierung und Vergabe konkreter Reuse-Leistungen.

### `Beschaffungsplanung`

Verwenden für die zeitliche und technische Planung der Beschaffung gebrauchter Bauteile.

### `Rückbauplanung`

Verwenden für die Planung eines selektiven, zerstörungsarmen Rückbaus.

### `Logistikplanung`

Verwenden für die Planung von Transport, Lagerung und zeitlicher Koordination gebrauchter Bauteile.

### `Demontagegerechtes Design`

Verwenden, wenn Gebäude oder Produkte so gestaltet werden, dass ihre Bauteile später zerstörungsfrei getrennt und erneut genutzt werden können.

### `Produktdesign`

Verwenden für Produkte, die aus gebrauchten Bauteilen bestehen oder für mehrfache Nutzung gestaltet werden.

### `Möbeldesign`

Verwenden für Gestaltung und Anpassung wiederverwendeter Möbel oder Bauteile zu Möbeln.

### `Ausstellungs- und Veranstaltungsbau`

Verwenden für wiederverwendbare, modulare oder wiederholt eingesetzte Ausstellungs-, Messe- oder Veranstaltungssysteme.

---

## D. Bestandserfassung, Inventarisierung und Suche

### `Bestandsaufnahme`

Verwenden für die allgemeine Erfassung eines bestehenden Gebäudes oder Bauteilbestands.

### `Bauteilinventarisierung`

Verwenden, wenn einzelne Bauteile systematisch identifiziert, beschrieben, vermessen oder katalogisiert werden.

### `Reuse-Audit`

Verwenden für eine strukturierte Untersuchung eines Gebäudes auf konkret wiederverwendbare Bauteile und Wiederverwendungspotenziale.

### `Potenzialbewertung`

Verwenden, wenn bewertet wird, welche vorhandenen Elemente technisch, wirtschaftlich oder organisatorisch wiederverwendbar sind.

### `Bauteilsuche`

Verwenden für die aktive Suche nach passenden gebrauchten Bauteilen für ein konkretes Projekt.

### `Material- und Bauteilbeschaffung`

Verwenden, wenn gebrauchte Materialien oder Bauteile konkret beschafft werden.

### `Digitale Bestandserfassung`

Verwenden, wenn digitale Verfahren wie Scanning, Bilderkennung oder mobile Erfassung zur Aufnahme vorhandener Bauteile eingesetzt werden.

---

## E. Technische Bewertung, Prüfung und Qualität

### `Zustandsbewertung`

Verwenden, wenn Alter, Beschädigungen, Abnutzung oder Erhaltungszustand beurteilt werden.

### `Technische Prüfung`

Verwenden für eine allgemeine technische Eignungsprüfung, wenn keine spezifischere Prüfart bestimmbar ist.

### `Tragfähigkeitsprüfung`

Verwenden für statische oder mechanische Prüfung von Tragwerkselementen.

### `Funktionsprüfung`

Verwenden für die Prüfung, ob technische Anlagen, Fenster, Türen, Leuchten oder andere Produkte weiterhin funktionieren.

### `Materialprüfung`

Verwenden für physikalische, chemische oder mechanische Prüfung eines Materials oder Bauprodukts.

### `Schadstoffprüfung`

Verwenden für Prüfung auf Asbest, PCB, PAK, Schwermetalle oder andere problematische Stoffe.

### `Brandschutzprüfung`

Verwenden für Prüfung brandschutztechnischer Eigenschaften.

### `Qualitätsprüfung`

Verwenden für die Prüfung definierter Qualitätsmerkmale einzelner Bauteile oder Produkte.

### `Qualitätssicherung`

Verwenden für systematische Prozesse, mit denen Qualität über mehrere Arbeitsschritte hinweg gesichert wird.

### `Zertifizierung`

Verwenden, wenn ein formaler Nachweis oder ein Zertifikat vergeben wird.

### `Zulassung und Normenkonformität`

Verwenden, wenn die regulatorische oder normative Einsatzfähigkeit gebrauchter Bauteile geklärt wird.

### `Herkunftsnachweis`

Verwenden, wenn Herkunft, frühere Nutzung oder Eigentum dokumentiert werden.

### `Rückverfolgbarkeit`

Verwenden, wenn Bauteile über mehrere Nutzungszyklen hinweg eindeutig identifizierbar bleiben.

### `Wertermittlung`

Verwenden für finanzielle oder materielle Bewertung vorhandener Bauteile.

### `Umweltbewertung`

Verwenden, wenn Umweltwirkungen verschiedener Reuse-Optionen verglichen werden.

Nicht verwenden, wenn lediglich eine allgemeine Lebenszyklusanalyse ohne direkten Reuse-Bezug angeboten wird.

### `Wirtschaftlichkeitsbewertung`

Verwenden für Kosten-Nutzen-, Markt- oder Geschäftsmodellbewertungen von Reuse.

### `Risikobewertung`

Verwenden für die Analyse technischer, rechtlicher, terminlicher oder finanzieller Risiken des Wiedereinsatzes.

---

## F. Rückbau, Demontage und Sicherung

### `Selektiver Rückbau`

Verwenden, wenn ein Gebäude kontrolliert und material- oder bauteilbezogen zurückgebaut wird, um Elemente zu erhalten.

### `Demontage`

Verwenden für den zerstörungsarmen Ausbau einzelner Bauteile oder Systeme.

### `Bergung`

Verwenden, wenn Bauteile gezielt vor Zerstörung oder Entsorgung gerettet werden.

### `Rücknahme`

Verwenden, wenn ein Akteur eigene oder fremde Produkte nach der Nutzung zurücknimmt.

### `Rücknahmesystem`

Verwenden, wenn eine dauerhaft organisierte Struktur für Rückgabe, Sammlung und erneuten Einsatz besteht.

### `Sortierung`

Verwenden, wenn ausgebaute Elemente nach Typ, Zustand oder Wiederverwendungspotenzial getrennt werden.

### `Schadstoffsanierung`

Nur verwenden, wenn die Entfernung oder Behandlung von Schadstoffen den Erhalt und Wiedereinsatz anderer Bauteile ermöglicht.

---

## G. Reparatur, Aufarbeitung und Nutzungsdauerverlängerung

### `Instandhaltung`

Verwenden für regelmäßige Maßnahmen, die den funktionsfähigen Zustand erhalten.

### `Reparatur`

Verwenden, wenn beschädigte Produkte oder Bauteile wieder funktionsfähig gemacht werden.

### `Reinigung`

Verwenden, wenn Reinigung ein eigenständiger notwendiger Schritt zur erneuten Nutzung ist.

### `Aufarbeitung`

Verwenden für Refurbishment, Rekonditionierung oder qualitative Erneuerung eines gebrauchten Bauteils.

### `Wiederaufbereitung`

Verwenden für einen systematischen industriellen Prozess, bei dem ein Produkt auf einen definierten Funktions- oder Qualitätszustand zurückgeführt wird.

### `Anpassung`

Verwenden, wenn Maße, Anschlüsse, Oberflächen oder Funktionen für einen neuen Einsatz verändert werden.

### `Umnutzung`

Verwenden, wenn ein vorhandenes Gebäude, Bauteil oder Produkt einer neuen Funktion zugeführt wird.

### `Sanierung`

Verwenden, wenn ein bestehendes Gebäude oder Bauteil technisch erneuert und dabei wesentlich erhalten wird.

### `Modernisierung`

Verwenden, wenn bestehende Elemente technisch verbessert und weitergenutzt werden.

### `Ersatzteilversorgung`

Verwenden, wenn Ersatzteile bereitgestellt werden, um vorhandene Produkte weiterbetreiben zu können.

### `Werkstattfertigung`

Verwenden, wenn gebrauchte Bauteile handwerklich bearbeitet oder zu neuen Einheiten zusammengefügt werden.

### `Fertigung mit Reuse-Material`

Verwenden, wenn neue Produkte überwiegend aus direkt wiederverwendeten Bauteilen oder Produkten gefertigt werden.

Nicht verwenden, wenn lediglich Recyclingrohstoffe eingesetzt werden.

---

## H. Lagerung, Transport und Logistik

### `Lagerung`

Verwenden, wenn gebrauchte Bauteile physisch über einen relevanten Zeitraum aufbewahrt werden.

### `Zwischenlagerung`

Verwenden für zeitlich begrenzte Lagerung zwischen Ausbau und Wiedereinbau.

### `Transport`

Verwenden für den physischen Transport gebrauchter Bauteile.

### `Rückführungslogistik`

Verwenden für organisierte Rücktransporte vom bisherigen Nutzer, Gebäude oder Projekt zum nächsten Prozessschritt.

### `Baustellenlogistik`

Verwenden für Koordination von Anlieferung, Zwischenlagerung und Handhabung auf der Baustelle.

### `Verpackung und Schutz`

Nur verwenden, wenn spezialisierte Verpackungs- oder Schutzleistungen den beschädigungsfreien Transport wiederverwendbarer Bauteile ermöglichen.

---

## I. Handel, Vermittlung und Nutzungsmodelle

### `Bauteilhandel`

Verwenden, wenn ein Akteur gebrauchte Bauteile übernimmt und auf eigene Rechnung verkauft.

`Verkauf` nicht zusätzlich nennen.

### `Vermittlung`

Verwenden, wenn Angebot und Nachfrage aktiv zusammengebracht werden, ohne dass der Akteur die Bauteile zwingend selbst besitzt.

### `Vermittlungsplattform`

Verwenden für einen digitalen Marktplatz oder ein digitales Matching-System für verfügbare und gesuchte Bauteile.

Nicht automatisch `Vermittlung` ergänzen, wenn ausschließlich eine Plattform bereitgestellt wird.

### `Vermietung`

Verwenden, wenn Bauteile, Produkte oder modulare Systeme zeitweise gegen Entgelt bereitgestellt und mehrfach eingesetzt werden.

### `Leasing`

Verwenden für langfristige nutzungsbasierte Bereitstellung mit Rückgabe- oder Weiterverwendungsmodell.

### `Weitergabe`

Verwenden für kostenlose Abgabe, Spende oder nicht-kommerziellen Besitzerwechsel.

### `Auktion`

Verwenden, wenn wiederverwendbare Bauteile über ein Auktionsverfahren vermittelt oder verkauft werden.

### `Produkt-Service-System`

Verwenden, wenn die Funktion eines Produkts angeboten wird und der Anbieter Eigentum, Rücknahme, Wartung oder Wiederaufbereitung organisiert.

---

## J. Bauausführung und Wiedereinbau

### `Bauausführung`

Verwenden, wenn ein Akteur Reuse-Lösungen praktisch auf der Baustelle umsetzt.

### `Wiedereinbau`

Verwenden für den konkreten Einbau gebrauchter Bauteile in ein neues oder bestehendes Gebäude.

### `Montage`

Nur verwenden, wenn eine Montageleistung belegt ist, aber nicht eindeutig festgestellt werden kann, ob es sich um einen Wiedereinbau handelt.

### `Systemintegration`

Verwenden, wenn gebrauchte technische Komponenten in ein neues technisches Gesamtsystem eingebunden werden.

### `Generalunternehmung`

Verwenden, wenn ein Akteur die Gesamtverantwortung für die Ausführung eines Reuse-Projekts übernimmt.

### `Baustellenkoordination`

Verwenden, wenn mehrere Reuse-Gewerke, Lieferungen oder Einbauprozesse auf der Baustelle koordiniert werden.

---

## K. Betrieb, Nutzung und Gebäudeverlängerung

### `Gebäudebetrieb`

Verwenden, wenn bestehende Gebäude oder Anlagen durch Betriebskonzepte länger genutzt werden.

### `Facility Management`

Verwenden, wenn Wartung, Reparatur, Ersatzteilmanagement und Weiterbetrieb professionell organisiert werden.

### `Temporärnutzung`

Verwenden, wenn bestehende Gebäude oder Flächen vorübergehend weitergenutzt werden, anstatt leer zu stehen oder frühzeitig abgebrochen zu werden.

### `Nutzungsmanagement`

Verwenden, wenn Belegung, gemeinsame Nutzung oder Nutzungswechsel organisiert werden, um den Bestand besser auszulasten.

### `Modulare Systeme`

Verwenden, wenn Konstruktionen wiederholt auf-, ab- und umgebaut werden können.

---

## L. Daten und digitale Infrastruktur

### `Materialdokumentation`

Verwenden, wenn Informationen zu Materialien oder Bauteilen strukturiert dokumentiert werden.

### `Materialpass`

Verwenden, wenn digitale oder physische Material- beziehungsweise Produktpässe erstellt oder betrieben werden.

### `Bauteilkataster`

Verwenden, wenn vorhandene oder verfügbare Bauteile in einem systematischen Register erfasst werden.

### `Bestandsdatenmanagement`

Verwenden für Pflege und Verwaltung von Daten über bestehende Gebäude und ihre Komponenten.

### `Datenplattform`

Verwenden für digitale Infrastruktur zur Speicherung und Nutzung von Reuse-relevanten Daten.

Nicht verwenden, wenn die Hauptfunktion die Vermittlung von Angebot und Nachfrage ist; dann `Vermittlungsplattform` verwenden.

### `Softwareentwicklung`

Verwenden, wenn Software speziell für Inventarisierung, Planung, Prüfung, Logistik oder Vermittlung von Reuse entwickelt wird.

### `Datenanalyse`

Verwenden, wenn Daten ausgewertet werden, um Reuse-Potenziale, Materialflüsse oder passende Bauteile zu bestimmen.

### `BIM und digitaler Zwilling`

Verwenden, wenn Gebäudemodelle oder digitale Zwillinge direkt zur Dokumentation oder Planung wiederverwendbarer Elemente eingesetzt werden.

### `Bilderkennung`

Verwenden, wenn Bildverarbeitung oder künstliche Intelligenz Bauteile erkennt, klassifiziert oder inventarisiert.

### `Datenstandardisierung`

Verwenden, wenn gemeinsame Datenfelder, Austauschformate, Klassifikationen oder Schnittstellen entwickelt werden.

---

## M. Methoden, Technologie und Erprobung

### `Methodenentwicklung`

Verwenden, wenn konkrete Verfahren für Inventarisierung, Bewertung, Planung, Rückbau, Matching oder Wiedereinbau entwickelt werden.

### `Technologieentwicklung`

Verwenden, wenn neue technische Werkzeuge, Maschinen, Prüfverfahren oder digitale Technologien für Reuse entwickelt werden.

### `Pilotierung`

Verwenden, wenn Methoden oder Prozesse in Pilotprojekten praktisch getestet werden.

### `Angewandte Forschung`

Nur verwenden, wenn eine direkte Reuse-Forschung belegt ist und keine präzisere Rolle den Beitrag vollständig beschreibt.

`Angewandte Forschung` darf möglichst nicht allein stehen.

Bevorzugte Kombinationen sind beispielsweise:

* `Methodenentwicklung / Angewandte Forschung`
* `Materialprüfung / Angewandte Forschung`
* `Datenanalyse / Angewandte Forschung`
* `Technologieentwicklung / Angewandte Forschung`

`Forschung` allein ist nicht zulässig.

### `Monitoring und Evaluation`

Verwenden, wenn Reuse-Projekte oder Programme systematisch beobachtet und hinsichtlich ihrer Wirkung bewertet werden.

---

## N. Bildung, Wissen und Vernetzung

### `Lehre`

Verwenden für formale Hochschul- oder Berufsschullehre mit direktem Reuse-Inhalt.

### `Ausbildung`

Verwenden für strukturierte berufliche Erstausbildung.

### `Weiterbildung`

Verwenden für Kurse, Seminare oder Fortbildungen für bereits Berufstätige.

### `Berufliche Qualifizierung`

Verwenden, wenn Personen gezielt für praktische Reuse-Tätigkeiten qualifiziert werden.

### `Wissensvermittlung`

Verwenden für Leitfäden, Publikationen, Ausstellungen oder Informationsangebote mit konkretem Reuse-Wissen.

### `Wissenstransfer`

Verwenden, wenn Wissen zwischen Forschung, Planung, Wirtschaft, Verwaltung und Praxis übertragen wird.

### `Netzwerkkoordination`

Verwenden, wenn ein Akteur ein Reuse-Netzwerk aktiv organisiert oder führt.

Nicht allein aufgrund einer Netzwerkmitgliedschaft verwenden.

### `Branchenverband`

Verwenden, wenn ein Verband die Interessen einer Reuse-bezogenen Branche organisiert und vertritt.

### `Standardisierung`

Verwenden, wenn einheitliche freiwillige Prozesse, Begriffe, Datenmodelle oder Vorgehensweisen entwickelt werden.

### `Normung`

Verwenden, wenn formale technische Normen entwickelt oder bearbeitet werden.

### `Richtlinienentwicklung`

Verwenden für Leitlinien, Handbücher, technische Regeln oder Beschaffungshilfen.

### `Interessenvertretung`

Verwenden, wenn politische oder gesellschaftliche Interessen von Reuse-Akteuren vertreten werden.

### `Öffentlichkeitsarbeit`

Verwenden, wenn gezielt öffentliche Aufmerksamkeit und Akzeptanz für Wiederverwendung aufgebaut werden.

### `Community-Aufbau`

Verwenden, wenn lokale Nutzer-, Reparatur-, Material- oder Fachgemeinschaften aufgebaut und betreut werden.

### `Veranstaltungsorganisation`

Verwenden für Konferenzen, Fachveranstaltungen oder Austauschformate, wenn Reuse deren klarer Schwerpunkt ist.

---

## O. Soziale Zusatzfunktionen

Diese Rollen nur zusätzlich zu einer konkreten Reuse-Funktion verwenden.

### `Arbeitsintegration`

Verwenden, wenn Rückbau, Aufarbeitung, Lagerung oder Verkauf mit der Integration von Menschen in den Arbeitsmarkt verbunden wird.

### `Beschäftigungsprogramm`

Verwenden, wenn Reuse-Tätigkeiten im Rahmen eines strukturierten Beschäftigungsangebots durchgeführt werden.

### `Soziale Qualifizierung`

Verwenden, wenn praktische Reuse-Arbeit mit sozialpädagogischer Begleitung und Kompetenzaufbau verbunden ist.

Nicht allein `Sozialunternehmen`, `Stiftung` oder `gemeinnützig` als Rolle verwenden.

---

# 7. Normalisierung häufiger unpräziser Begriffe

## „Forschung“

Nicht direkt übernehmen.

Stattdessen prüfen, ob die konkrete Tätigkeit eine der folgenden ist:

* `Methodenentwicklung`
* `Technologieentwicklung`
* `Materialprüfung`
* `Datenanalyse`
* `Pilotierung`
* `Monitoring und Evaluation`
* `Lehre`
* `Angewandte Forschung`

## „Beratung“

Nicht direkt übernehmen.

Stattdessen die tatsächliche Beratungsleistung bestimmen:

* `Reuse-Strategie`
* `Reuse-Planung`
* `Bauteilinventarisierung`
* `Potenzialbewertung`
* `Bauteilsuche`
* `Materialberatung`
* `Rückbauplanung`
* `Technische Prüfung`
* `Rechtsberatung`
* `Beschaffungsplanung`
* `Wirtschaftlichkeitsbewertung`
* `Reuse-Beratung` nur als letzter fachlich begründeter Oberbegriff

## „Engineering“

Nicht direkt übernehmen.

Mögliche Normalisierung:

* `Tragwerksplanung`
* `Gebäudetechnikplanung`
* `Technische Prüfung`
* `Tragfähigkeitsprüfung`
* `Materialprüfung`
* `Brandschutzplanung`
* `Bauphysik`
* `Technische Planung`

## „Plattform“

Nicht direkt übernehmen.

Mögliche Normalisierung:

* `Vermittlungsplattform`
* `Datenplattform`
* `Materialpass`
* `Bauteilkataster`
* `Bestandsdatenmanagement`
* `Softwareentwicklung`

## „Urban Mining“

Nicht als normalisierte Rolle verwenden.

Je nach konkreter Tätigkeit aufteilen in:

* `Bauteilinventarisierung`
* `Reuse-Audit`
* `Potenzialbewertung`
* `Selektiver Rückbau`
* `Bergung`
* `Bauteilhandel`
* `Materialdokumentation`

## „Reuse-Hub“ oder „Reuse-Zentrum“

Nicht als Rolle übernehmen.

Stattdessen die tatsächlichen Funktionen erfassen, beispielsweise:

* `Lagerung`
* `Aufarbeitung`
* `Bauteilhandel`
* `Vermittlung`
* `Weiterbildung`
* `Community-Aufbau`

## „Marktplatz“

Normalisieren als:

* `Vermittlungsplattform`, wenn digital vermittelt wird
* `Vermittlung`, wenn persönliche Vermittlungsarbeit erfolgt
* `Bauteilhandel`, wenn der Akteur Waren übernimmt und selbst verkauft

## „Salvage“

Je nach Tätigkeit normalisieren als:

* `Bergung`
* `Demontage`
* `Selektiver Rückbau`
* `Bauteilhandel`

## „Deconstruction“

Normalisieren als:

* `Selektiver Rückbau`, wenn das Gebäude systematisch rückgebaut wird
* `Demontage`, wenn einzelne Bauteile ausgebaut werden

## „Refurbishment“ oder „Reconditioning“

Normalisieren als:

* `Aufarbeitung`

## „Remanufacturing“

Normalisieren als:

* `Wiederaufbereitung`

## „Adaptive Reuse“

Je nach Funktion normalisieren als:

* `Bestandsentwicklung`
* `Umnutzungsplanung`
* `Architektur`
* `Umnutzung`

## „Material Passport“

Normalisieren als:

* `Materialpass`
* gegebenenfalls zusätzlich `Materialdokumentation`
* gegebenenfalls zusätzlich `Datenplattform`

## „Reverse Logistics“

Normalisieren als:

* `Rückführungslogistik`

## „Take-back“

Normalisieren als:

* `Rücknahme`, wenn einzelne Rücknahmen erfolgen
* `Rücknahmesystem`, wenn ein dauerhaftes System besteht

## „Product as a Service“

Normalisieren als:

* `Produkt-Service-System`

## „Training“

Je nach Zielgruppe normalisieren als:

* `Ausbildung`
* `Weiterbildung`
* `Berufliche Qualifizierung`
* `Soziale Qualifizierung`

## „Advocacy“

Normalisieren als:

* `Interessenvertretung`
* gegebenenfalls `Politikberatung`
* gegebenenfalls `Öffentlichkeitsarbeit`

## „Material Library“

Je nach Funktion normalisieren als:

* `Materialdokumentation`
* `Wissensvermittlung`
* `Bauteilkataster`
* `Bauteilhandel`, falls Materialien tatsächlich verkauft werden

---

# 8. Regeln für „Relevanz für Wiederverwendung“

## Inhalt

Die Relevanz muss den konkreten kausalen Beitrag des Akteurs beschreiben:

* Was wird getan?
* An welchem Objekt?
* An welcher Stelle des Wiederverwendungsprozesses?
* Welcher Wiedereinsatz oder welche Nutzungsdauerverlängerung wird dadurch ermöglicht?

## Form

* Ein kurzer vollständiger Satz.
* **Höchstens 90 Zeichen** (die Ausgabe wird in eine gedruckte Tabelle mit begrenzter Breite gesetzt).
* Möglichst 6 bis 12 Wörter.
* Aktiv formulieren.
* Mit einem konkreten Verb beginnen.
* Keine allgemeinen Wertungen.
* Keine Marketing-Sprache.
* Keine unbelegten Umweltwirkungen.
* Die Rollen-Spalte nicht nur wortgleich wiederholen.
* Höchstens zwei bis drei eng zusammenhängende Wirkungen nennen.
* Wiederverwendung, Wiedereinbau, weitere Nutzung oder Bestandserhalt klar erkennbar machen.

## Bevorzugte Verben

* beauftragt
* besitzt
* finanziert
* fördert
* beschafft
* verankert
* reguliert
* genehmigt
* plant
* erhält
* transformiert
* erfasst
* inventarisiert
* bewertet
* sucht
* prüft
* zertifiziert
* dokumentiert
* sichert
* demontiert
* birgt
* sortiert
* reinigt
* repariert
* arbeitet auf
* bereitet auf
* passt an
* lagert
* transportiert
* vermittelt
* verkauft
* vermietet
* führt weiter
* baut ein
* integriert
* betreibt
* wartet
* verlängert
* standardisiert
* qualifiziert
* vernetzt
* entwickelt
* erprobt
* schafft Rechtssicherheit
* macht auffindbar
* erhält Informationen

## Zu vermeidende Formulierungen

Nicht verwenden:

* `Fördert Nachhaltigkeit.`
* `Unterstützt die Kreislaufwirtschaft.`
* `Ist wichtig für Reuse.`
* `Trägt zu einer grüneren Zukunft bei.`
* `Ist ein innovativer Akteur.`
* `Reduziert Abfall und CO₂.`
  Nur zulässig, wenn dies konkret gemessen und für die Aufgabe ausdrücklich relevant ist.
* `Bietet Lösungen für Wiederverwendung.`
* `Beschäftigt sich mit zirkulärem Bauen.`
* `Forscht zu Reuse.`
* `Berät zu Nachhaltigkeit.`

---

# 9. Normalisierte Relevanzmuster

## Bauherrschaft und Eigentum

`Beauftragt Projekte mit bestehenden und wiederverwendeten Bauteilen.`

`Entscheidet über Erhalt, Umbau und Freigabe vorhandener Bauteile.`

## Finanzierung und Förderung

`Stellt Kapital für Projekte mit hohem Wiederverwendungsanteil bereit.`

`Finanziert die Entwicklung und Umsetzung von Reuse-Prozessen.`

## Öffentliche Beschaffung

`Verankert Wiederverwendung in Ausschreibungen und Beschaffungsentscheidungen.`

## Regulierung

`Schafft verbindliche Rahmenbedingungen für den Wiedereinsatz gebrauchter Bauteile.`

## Architektur und Planung

`Integriert bestehende Strukturen und gebrauchte Bauteile in neue Planungen.`

`Plant den Erhalt und die Umnutzung bestehender Gebäude.`

## Inventarisierung

`Erfasst wiederverwendbare Bauteile vor Umbau oder Rückbau.`

## Potenzialbewertung

`Bewertet vorhandene Bauteile auf ihre Eignung für eine weitere Nutzung.`

## Bauteilsuche

`Sucht passende gebrauchte Bauteile für konkrete Bauprojekte.`

## Technische Prüfung

`Prüft gebrauchte Bauteile für einen sicheren und regelkonformen Wiedereinbau.`

## Selektiver Rückbau

`Demontiert und sichert Bauteile ohne Verlust ihrer Wiederverwendbarkeit.`

## Reparatur und Aufarbeitung

`Repariert und bereitet gebrauchte Bauteile für eine weitere Nutzung auf.`

## Lagerung und Logistik

`Lagert und transportiert Bauteile zwischen Ausbau und neuer Nutzung.`

## Handel und Vermittlung

`Führt verfügbare Bauteile neuen Nutzern und Projekten zu.`

`Macht verfügbare Bauteile auffindbar und vermittelt sie an neue Projekte.`

## Wiedereinbau

`Integriert gebrauchte Bauteile fachgerecht in neue oder bestehende Gebäude.`

## Gebäudebetrieb

`Verlängert die Nutzungsdauer bestehender Gebäude und technischer Anlagen.`

## Materialdokumentation

`Dokumentiert Materialien für ihre spätere Identifikation und Wiederverwendung.`

## Materialpass und Rückverfolgbarkeit

`Erhält Bauteilinformationen über mehrere Nutzungszyklen hinweg.`

## Methoden- und Technologieentwicklung

`Entwickelt und erprobt konkrete Verfahren für Planung und Wiedereinsatz.`

## Bildung

`Qualifiziert Fachleute für Planung, Prüfung und Umsetzung von Reuse.`

## Standards und Richtlinien

`Entwickelt einheitliche Verfahren für verlässliche Reuse-Prozesse.`

## Recht

`Schafft vertragliche und rechtliche Sicherheit für den Wiedereinsatz.`

## Versicherung

`Reduziert Risiken durch Gewährleistungsmodelle für gebrauchte Bauteile.`

## Arbeitsintegration

`Verbindet die Aufarbeitung gebrauchter Bauteile mit beruflicher Integration.`

---

# 10. Positive Klassifikationsbeispiele

| Beschreibung des Akteurs | Rolle(n) | Relevanz für Wiederverwendung |
| --- | --- | --- |
| Architekturbüro transformiert Bestandsgebäude und plant mit gebrauchten Bauteilen | Architektur / Bestandsentwicklung / Reuse-Planung | Integriert bestehende Strukturen und gebrauchte Bauteile in neue Planungen. |
| Eigentümer beauftragt einen Umbau mit hohem Anteil gebrauchter Bauteile | Gebäudeeigentum / Bauherrschaft | Beauftragt Projekte mit bestehenden und wiederverwendeten Bauteilen. |
| Immobilienentwickler entwickelt neue Nutzungen für leer stehende Bestandsgebäude | Projektentwicklung / Bestandsentwicklung / Umnutzungsplanung | Entwickelt neue Nutzungen und erhält bestehende Gebäudestrukturen. |
| Stiftung stellt Zuschüsse für Reuse-Pilotprojekte bereit | Fördermittelvergabe | Finanziert die Erprobung und Umsetzung von Reuse-Projekten. |
| Bank bietet spezielle Kredite für Bestands- und Reuse-Projekte an | Finanzierung | Stellt Kapital für Bestandserhalt und Wiederverwendungsprojekte bereit. |
| Versicherung entwickelt Gewährleistungsmodelle für gebrauchte Bauteile | Versicherung / Risikobewertung | Reduziert Risiken beim Wiedereinsatz gebrauchter Bauteile. |
| Stadt schreibt wiederverwendete Bauteile in öffentlichen Wettbewerben vor | Öffentliche Beschaffung / Regulierung | Verankert Wiederverwendung in öffentlichen Ausschreibungen. |
| Beratungsbüro erstellt Reuse-Roadmaps für Immobilienportfolios | Reuse-Strategie / Portfoliomanagement | Entwickelt portfolioweite Strategien für Bauteilwiederverwendung. |
| Fachbüro inventarisiert Gebäude vor dem Rückbau | Bauteilinventarisierung / Reuse-Audit | Erfasst wiederverwendbare Bauteile vor dem Rückbau. |
| Dienstleister sucht gebrauchte Fassadenelemente für ein konkretes Projekt | Bauteilsuche / Material- und Bauteilbeschaffung | Beschafft passende gebrauchte Bauteile für den geplanten Wiedereinbau. |
| Tragwerksbüro prüft gebrauchte Stahlträger und plant deren Einbau | Tragfähigkeitsprüfung / Tragwerksplanung | Prüft und plant Stahlbauteile für einen sicheren Wiedereinbau. |
| Prüflabor untersucht gebrauchte Holzträger auf Festigkeit und Schadstoffe | Materialprüfung / Schadstoffprüfung | Prüft gebrauchte Bauteile auf Sicherheit und technische Eignung. |
| Rückbauunternehmen baut Fenster, Türen und Träger zerstörungsarm aus | Selektiver Rückbau / Demontage / Bergung | Demontiert und sichert Bauteile ohne Verlust ihrer Wiederverwendbarkeit. |
| Werkstatt reinigt, repariert und passt gebrauchte Fenster an | Reparatur / Aufarbeitung / Anpassung | Bereitet gebrauchte Fenster für den Einsatz in neuen Projekten auf. |
| Unternehmen lagert ausgebaute Bauteile und liefert sie an Baustellen | Lagerung / Transport / Baustellenlogistik | Lagert und transportiert Bauteile zwischen Ausbau und Wiedereinbau. |
| Händler übernimmt gebrauchte Türen und verkauft sie aus einem Lager | Lagerung / Bauteilhandel | Lagert gebrauchte Bauteile und führt sie einer neuen Nutzung zu. |
| Onlineplattform verbindet Abbruchprojekte mit suchenden Planungsbüros | Vermittlungsplattform | Macht verfügbare Bauteile auffindbar und verbindet Angebot mit Nachfrage. |
| Makler vermittelt gebrauchte Bauteile persönlich zwischen Projekten | Vermittlung | Vermittelt verfügbare Bauteile an passende neue Projekte. |
| Bauunternehmen baut gebrauchte Fassadenplatten in einem Neubau ein | Bauausführung / Wiedereinbau | Integriert gebrauchte Fassadenelemente fachgerecht in ein neues Gebäude. |
| Leuchtenhersteller nimmt Produkte zurück, prüft und überarbeitet sie | Rücknahmesystem / Funktionsprüfung / Wiederaufbereitung | Führt gebrauchte Leuchten nach Prüfung und Aufarbeitung erneut ein. |
| Facility-Management-Unternehmen repariert und wartet technische Anlagen | Facility Management / Instandhaltung / Reparatur | Verlängert die Nutzungsdauer bestehender technischer Anlagen. |
| Plattform erstellt Materialpässe und verfolgt Bauteile über Nutzungszyklen | Materialpass / Datenplattform / Rückverfolgbarkeit | Erhält Bauteilinformationen für spätere Wiederverwendung. |
| Hochschule entwickelt Matching-Algorithmen und unterrichtet Reuse-Planung | Methodenentwicklung / Datenanalyse / Lehre | Entwickelt Matching-Methoden und qualifiziert Planende für Reuse. |
| Forschungsgruppe entwickelt Prüfverfahren für gebrauchte Betonbauteile | Methodenentwicklung / Materialprüfung / Angewandte Forschung | Entwickelt Prüfverfahren für den Wiedereinsatz von Betonbauteilen. |
| Verband veröffentlicht Vertragsmuster und technische Reuse-Leitlinien | Branchenverband / Vertragsgestaltung / Richtlinienentwicklung | Schafft rechtliche und technische Grundlagen für Reuse-Projekte. |
| Netzwerk organisiert Fachtreffen und verbindet Rückbau, Planung und Handel | Netzwerkkoordination / Veranstaltungsorganisation / Wissenstransfer | Vernetzt Akteure und überträgt Reuse-Wissen zwischen Fachbereichen. |
| Rechtskanzlei entwickelt Verträge für den Verkauf gebrauchter Bauteile | Rechtsberatung / Vertragsgestaltung | Schafft vertragliche Sicherheit für Handel und Wiedereinbau. |
| Zertifizierungsstelle vergibt Nachweise für aufgearbeitete Bauteile | Zertifizierung / Qualitätssicherung | Bestätigt die Qualität aufgearbeiteter Bauteile für eine erneute Nutzung. |
| Sozialbetrieb bereitet Bauteile auf und qualifiziert arbeitssuchende Personen | Aufarbeitung / Berufliche Qualifizierung / Arbeitsintegration | Verbindet Bauteilaufarbeitung mit Qualifizierung und Arbeitsintegration. |
| Betreiber vermietet modulare Messestände über viele Veranstaltungen hinweg | Vermietung / Modulare Systeme / Ausstellungs- und Veranstaltungsbau | Ermöglicht den wiederholten Einsatz modularer Veranstaltungssysteme. |
| Organisation vermittelt leer stehende Gebäude für temporäre Nutzungen | Temporärnutzung / Vermittlung | Verlängert die Nutzung bestehender Gebäude vor Umbau oder Rückbau. |
| Möbeldesigner fertigt Tische aus ausgebauten Tragwerkselementen | Möbeldesign / Anpassung / Fertigung mit Reuse-Material | Führt ausgebaute Bauteile durch Anpassung einer neuen Nutzung zu. |
| Hersteller konstruiert Trennwandsysteme für mehrfache Demontage und Montage | Demontagegerechtes Design / Modulare Systeme / Produkt-Service-System | Ermöglicht die wiederholte Nutzung von Trennwandsystemen. |
| Bauvorhaben mit 30.000 geborgenen Ziegeln in der neuen Museumsfassade | Referenzprojekt | Verbaut 30.000 geborgene Ziegel aus acht Abbruchstellen in der Fassade. |

---

# 11. Negative und mehrdeutige Beispiele

| Beschreibung des Akteurs | Rolle(n) | Relevanz für Wiederverwendung |
| --- | --- | --- |
| Unternehmen zerkleinert Abbruchbeton zu Recyclinggranulat | Keine direkte Reuse-Rolle belegt | Die Tätigkeit betrifft Recycling, nicht die direkte Wiederverwendung von Bauteilen. |
| Hersteller produziert neue Platten aus recyceltem Kunststoff | Keine direkte Reuse-Rolle belegt | Die Herstellung aus Recyclingmaterial ist keine direkte Bauteilwiederverwendung. |
| Architekturbüro bezeichnet sich allgemein als nachhaltig | Keine direkte Reuse-Rolle belegt | Eine konkrete Tätigkeit zur Wiederverwendung ist nicht belegt. |
| Beratungsfirma bietet allgemeine ESG- und Nachhaltigkeitsberatung | Keine direkte Reuse-Rolle belegt | Aus den Angaben ist kein direkter Beitrag zur Wiederverwendung ableitbar. |
| Abbruchunternehmen führt ausschließlich maschinellen Totalabbruch durch | Keine direkte Reuse-Rolle belegt | Ein zerstörungsarmer Ausbau wiederverwendbarer Bauteile ist nicht belegt. |
| Universität besitzt ein Institut für Kreislaufwirtschaft, konkrete Tätigkeit unbekannt | Unzureichende Informationen | Die vorliegenden Informationen reichen für eine belastbare Einordnung nicht aus. |
| Unternehmen wird als Partner eines Reuse-Projekts genannt, Aufgabe unbekannt | Reuse-Bezug belegt, Rolle unklar | Ein direkter Reuse-Bezug ist belegt, die konkrete Funktion bleibt jedoch unklar. |
| Mitglied eines Reuse-Netzwerks ohne eigene beschriebene Tätigkeit | Unzureichende Informationen | Aus der Mitgliedschaft lässt sich keine konkrete Reuse-Funktion ableiten. |
| Datenbank enthält nur Umweltproduktdeklarationen neuer Baustoffe | Keine direkte Reuse-Rolle belegt | Die Datenbank dokumentiert neue Produkte, aber keine direkte Wiederverwendung. |
| Baustoffhersteller wirbt mit vollständig recyclingfähigen Produkten | Keine direkte Reuse-Rolle belegt | Recyclingfähigkeit allein belegt keine Wiederverwendungsfunktion. |
| Unternehmen trägt „Reuse“ im Namen, weitere Informationen fehlen | Unzureichende Informationen | Der Name allein reicht für eine belastbare Einordnung nicht aus. |
| Stadt besitzt Gebäude, konkrete Reuse-Maßnahmen sind nicht beschrieben | Unzureichende Informationen | Gebäudeeigentum allein belegt noch keine aktive Wiederverwendungsfunktion. |
| Hochschule unterrichtet allgemeine Architektur, Reuse wird nicht erwähnt | Keine direkte Reuse-Rolle belegt | Eine spezifische Lehre zur Wiederverwendung ist nicht belegt. |
| Plattform verkauft ausschließlich neue Baustoffe | Keine direkte Reuse-Rolle belegt | Der Verkauf neuer Baustoffe stellt keine direkte Wiederverwendung dar. |
| Unternehmen führt CO₂-Bilanzen durch, ohne Reuse-Optionen zu bewerten | Keine direkte Reuse-Rolle belegt | Eine allgemeine Umweltbewertung ist keine direkte Wiederverwendungsfunktion. |
| Bauvorhaben als Reuse-Referenz belegt, Bauteilumfang nicht erkennbar | Referenzprojekt, Reuse-Umfang unklar | Das Bauvorhaben ist als Reuse-Referenz belegt, der konkrete Bauteilumfang bleibt offen. |

---

# 12. Interne Entscheidungsschritte

Führe für jeden Akteur intern diese Prüfung durch:

1. Ist der Eintrag als `BAUVORHABEN/OBJEKT` markiert? Dann gilt Regel P (Abschnitt 4b).
2. Wurde die Beleg-URL geöffnet?
3. Ist eine konkrete Tätigkeit beschrieben?
4. Betrifft die Tätigkeit ein bestehendes Gebäude, gebrauchtes Bauteil, Produkt oder eine technische Anlage?
5. Bleibt dessen Identität oder Funktion weitgehend erhalten?
6. Trägt die Tätigkeit direkt zu Erhalt, Ausbau, Prüfung, Aufarbeitung, Vermittlung, Wiedereinbau oder Nutzungsdauerverlängerung bei?
7. Oder schafft sie eine konkrete Voraussetzung durch Planung, Finanzierung, Beschaffung, Regulierung, Daten, Standards oder Qualifizierung?
8. Ist jede ausgewählte Rolle durch einen konkreten Beleg gedeckt?
9. Gibt es eine spezifischere Rolle als einen allgemeinen Begriff?
10. Wurden ähnliche Tätigkeiten mit denselben bevorzugten Begriffen normalisiert?
11. Wurden Recycling, Nachhaltigkeit und Kreislaufwirtschaft korrekt von Wiederverwendung abgegrenzt?
12. Wurden keine Rollen von Partnern, Muttergesellschaften oder Projektverbünden übertragen?
13. Ist die Relevanz konkret, aktiv, ≤ 90 Zeichen und ohne Marketing-Sprache formuliert?
14. Muss wegen unzureichender Evidenz ein Rückfallwert verwendet werden?

Gib anschließend nur die fertige Tabelle aus.

---

# 13. Abschließende Qualitätskontrolle

Vor der Ausgabe sicherstellen:

* Jede Eingabe hat genau eine Ausgabezeile.
* Die ID ist unverändert übernommen.
* Der Name ist unverändert.
* Alle Rollen stammen exakt aus dem kontrollierten Vokabular.
* Höchstens 3 Rollen je Akteur.
* Jede Relevanz ist höchstens 90 Zeichen lang.
* Objekte (`BAUVORHABEN/OBJEKT`) tragen ausschließlich Regel-P-Werte.
* Organisationen tragen keine Regel-P-Werte.
* Keine Rolle basiert allein auf dem Namen des Akteurs.
* Keine Rolle basiert allein auf allgemeinen Nachhaltigkeitsbegriffen.
* Keine unbelegte Tätigkeit wurde ergänzt.
* Keine Recyclingaktivität wurde als Wiederverwendung dargestellt.
* Keine Netzwerkmitgliedschaft wurde als Netzwerkkoordination interpretiert.
* Keine Universitätszugehörigkeit wurde automatisch als Forschung oder Lehre interpretiert.
* Keine Plattform wurde automatisch als Handel oder Lagerung interpretiert.
* Kein Gebäudeeigentümer wurde automatisch als Bauherrschaft interpretiert.
* Kein konventioneller Abbruch wurde als selektiver Rückbau interpretiert.
* Keine Rolle ist unnötig redundant.
* Die Relevanz beschreibt einen konkreten Beitrag.
* Bei Unsicherheit wurde nicht geraten.
* Rückfallwerte wurden exakt und einheitlich verwendet.

---

## Zu klassifizierende Akteure

### DK:P6
- Name: TRÆ High-Rise
- Land: DK
- Eintragsart: BAUVORHABEN/OBJEKT (keine Organisation) -- siehe Regel P
- Beleg-URL (MUSS geoeffnet werden): https://lendager.com/project/trae
- Weitere URL: https://eumiesawards.com/heritageobject/tr
- Weitere URL: https://dac.dk/en/magazine/places/trae-materials-before-form-458
- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): "TRAE ... is a 78-meter beacon of circular construction, showing that large-scale architecture can combine reused materials, biogenic resources"

### DK:U33
- Name: Tscherning
- Land: DK
- Typ (Altdaten, unbestaetigt): Unternehmen
- Beleg-URL (MUSS geoeffnet werden): https://vaerdibyg.dk/case/svanen-i-gladsaxe-cirkulaer-nedrivning/
- Alt-Rollen (Altdaten, NICHT als Beleg verwenden): Rueckbau_Bauteilernte_Logistik
- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): "For entreprenoeren Tscherning har udfordringen vaeret, at man normalt kan nedrive meget med maskine"

### DK:P7
- Name: Upcycle Studios Copenhagen
- Land: DK
- Eintragsart: BAUVORHABEN/OBJEKT (keine Organisation) -- siehe Regel P
- Beleg-URL (MUSS geoeffnet werden): https://estatemedia.dk/dk/2017/08/30/nrep-arkitektgruppen-bygger-20-raekkehuse-upcyclede-materialer-oerestad-syd/
- Weitere URL: https://nrep.com/project/upcycle-studios
- Weitere URL: https://lendager.com/project/upcycle-studios
- Weitere URL: https://www.again.dk/project-references/upcycle-studios
- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): "NREP og Arkitektgruppen har netop taget første spadestik på endnu et byggeri i Ørestad Syd, nemlig byggeriet af 20 rækkehuse under navnet Upcycle Studios."

### DK:S03
- Name: UpcyclingForum
- Land: DK
- Typ (Altdaten, unbestaetigt): Software_Tool_Anbieter
- Beleg-URL (MUSS geoeffnet werden): https://www.upcyclingforum.dk/
- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): "Kortlæg materialer, dokumentér CO₂-reduktioner og del på tværs af kommunegrænser og virksomheder."

### DK:U34
- Name: Vandkunsten
- Land: DK
- Typ (Altdaten, unbestaetigt): Unternehmen
- Beleg-URL (MUSS geoeffnet werden): https://vandkunsten.com/en/projects/circuit-eu-circular
- Weitere URL: https://vandkunsten.com/en
- Alt-Rollen (Altdaten, NICHT als Beleg verwenden): Entwurf_Planung / Forschung_Dokumentation / Reuse_Zirkularitaetsberatung
- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): "help the partner cities to look at their city as material mine for raw materials and components which can be reused instead of crushed and downgraded"

