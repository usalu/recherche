# Produktionsprompt: Normalisierte Klassifikation von Beziehungen im Akteursnetz der baulichen Wiederverwendung

## Aufgabe

Klassifiziere jede angegebene **Verbindung zwischen zwei Knoten** nach:

1. **ID**
2. **Beziehungsart** (kontrolliertes Vokabular)
3. **Richtung**
4. **Beschreibung der Beziehung**

Anders als bei der Akteursklassifikation geht es hier nicht darum, was ein Akteur tut, sondern **was zwei Knoten konkret miteinander verbindet**.

Arbeite radikal evidenzbasiert. Jede Eingabekante ist nur ein Kandidat und gilt zunächst als
nicht vorhanden. Eine positive Beziehung darf nur vergeben werden, wenn eine erreichbare
Quelle **beide Knoten nennt und ihre konkrete Verbindung beschreibt**. Ohne diesen Beleg
wird die Kante gelöscht. **Leite keine Beziehung aus bloßer Nähe, gemeinsamer Branche,
gemeinsamem Ort oder gemeinsamer Nennung in einer Liste ab.**

---

## Eingabe

Jede Verbindung kommt als Block:

    ### <ID>
    - Kantenart: AKTEUR-BAUVORHABEN | AKTEUR-AKTEUR
    - Knoten A: <Name>  [Typ]
    - Knoten B: <Name>  [Typ]
    - Land: <ISO2>
    - Belegstatus: GEPRUEFT | UNGEPRUEFT
    - Beleg-URL (MUSS geoeffnet werden): <URL>          [nur bei GEPRUEFT]
    - Bisherige Beschreibung (Altdaten, nur Hinweis): <Text>   [optional]
    - Gespeichertes Belegzitat (Nachweis-Schnipsel): "<Zitat>" [nur bei GEPRUEFT]

### Belegstatus GEPRUEFT

Eine Quelle wurde bereits gesichert. **Öffne die Beleg-URL** und lies dort, was die beiden Knoten tatsächlich verbindet. Das gespeicherte Zitat wurde erhoben, um *die Existenz* der Verbindung zu belegen, nicht um ihre Art zu beschreiben — es ist als Einstieg zu verwenden, nicht als Beschreibung zu übernehmen.

### Belegstatus UNGEPRUEFT

Für diese Verbindung liegt **keine Quelle** vor. Sie stammt aus einer Datenbankbeziehung oder einem Rechercheüberlauf und wurde nie einzeln geprüft.

Recherchiere aktiv: suche nach beiden Namen gemeinsam, prüfe die Projektseite oder die Website eines der beiden Knoten. Findest du eine Quelle, die beide nennt und ihre Verbindung beschreibt, klassifiziere normal und gib die gefundene URL in der Spalte `Beleg` an. Findest du keine, verwende `Kein Beleg für eine Beziehung`.

**Rate hier auf keinen Fall.** Diese Verbindungen sind ungeprüft in die Zeichnung geraten; genau das soll die Klassifikation aufdecken.

### Bisherige Beschreibung ist kein Beleg

Das Feld `Bisherige Beschreibung` stammt aus einem älteren, gröberen Schema und wurde nie einzeln verifiziert. Als Suchhinweis brauchbar, als Evidenz nicht.

---

## Ausgabeformat

Gib ausschließlich eine Tabelle mit genau diesen Spalten aus:

| ID | Beziehungsart | Richtung | Beschreibung | Beleg | Belegzitat |
| -- | ------------- | -------- | ------------ | ----- | ----------- |

* Genau eine Zeile pro eingegebenem Block, Reihenfolge beibehalten, nichts auslassen.
* **ID unverändert** aus dem Eingabeblock übernehmen.
* **Beziehungsart:** genau **eine** Art aus dem kontrollierten Vokabular (Abschnitt 3 oder 4) oder ein Rückfallwert (Abschnitt 5). Anders als bei Akteursrollen ist **keine Mehrfachnennung** zulässig — eine Kante trägt eine Art. Treffen mehrere zu, nimm die strukturell stärkste (Reihenfolge in Abschnitt 6).
* **Richtung:** `A→B`, `B→A` oder `—` für symmetrische Beziehungen. Siehe Abschnitt 7.
* **Beschreibung:** ein kurzer vollständiger Satz, **höchstens 90 Zeichen**, der die konkrete Verbindung benennt. Regeln in Abschnitt 8.
* **Beleg:** bei `UNGEPRUEFT` die neu gefundene URL, sonst `vorhanden`. Bei fehlendem Fund `—`.
* **Belegzitat:** bei jeder positiven Art ein wörtlicher, beziehungsspezifischer Ausschnitt
  aus der geöffneten Quelle, höchstens 240 Zeichen. Er muss die konkrete Verbindung tragen;
  bloße Namensnennung, Seitentitel oder Such-Snippets genügen nicht. Das Tabellenzeichen `|`
  darf nicht vorkommen. Bei allen Rückfallwerten `—`.
* Keine zusätzlichen Erklärungen vor oder nach der Tabelle.

---

# 1. Was als Beziehung gilt

Eine Verbindung ist belegt, wenn eine Quelle **beide Knoten nennt** und dabei erkennbar macht, dass zwischen ihnen eine der folgenden Verbindungen besteht:

* gemeinsame Mitwirkung an einem benannten Bauvorhaben
* gemeinsame Mitwirkung in einem benannten Projekt, Konsortium oder Programm
* Gründung, Beteiligung, Übernahme oder Konzernzugehörigkeit
* Betrieb einer Einrichtung, Plattform oder Anlage des jeweils anderen
* Liefer-, Auftrags- oder Dienstleistungsbeziehung
* formalisierte Kooperation oder Mitgliedschaft
* personelle Verflechtung in Leitung oder Gründung

Die Quelle muss die Verbindung **benennen**. Eine Aufzählung beider Namen ohne Aussage über ihr Verhältnis genügt nicht.

Es gibt keinen Vertrauensvorschuss aus der Zeichnung, aus einer Datenbankkante oder aus dem
Status `GEPRUEFT`. Wenn die geöffnete Quelle die konkrete Beziehung nicht trägt, verwende
einen Rückfallwert aus Abschnitt 5; die Kante wird entfernt.

---

# 2. Was ausdrücklich keine Beziehung ist

## Verzeichniseintrag

**Die wichtigste Ausschlussregel dieses Projekts.**

Eine gemeinsame Listung in einem Verzeichnis, Branchenbuch, Mitgliederverzeichnis oder Anbieterkatalog ist **keine** Beziehung zwischen den gelisteten Akteuren — auch dann nicht, wenn das Verzeichnis selbst ein Knoten im Netz ist.

Betroffen sind insbesondere Verbindungen zu:

* Opalis
* bauteilnetz Deutschland
* SalvoWEB
* Bolius genbrugsmaterialer directory
* byggogbevar directory
* Cirkla
* vergleichbare Anbieter- und Bezugsquellenverzeichnisse

Verwende in diesen Fällen die Beziehungsart `Verzeichniseintrag`. Diese Kanten werden anschließend aus der Zeichnung entfernt — sie sind kein Beleg für eine Zusammenarbeit, sondern nur dafür, dass beide im selben Katalog stehen.

**Ausnahme:** Betreibt einer der beiden Knoten das Verzeichnis nachweislich für den anderen,
oder besteht darüber hinaus eine belegte Zusammenarbeit, gilt die tatsächliche
Beziehungsart. Dafür ist ein eigener Beleg erforderlich; die Listung selbst reicht nicht.

Ein formelles Mitgliederverzeichnis kann `Mitgliedschaft` nur dann belegen, wenn es den
Status ausdrücklich als Mitgliedschaft bezeichnet. Ein Anbieter-, Händler-, Partnerlogo-
oder Bezugsquellenverzeichnis belegt keine Mitgliedschaft und keine Zusammenarbeit.

## Ebenfalls keine Beziehung

* gemeinsame Branche, Rechtsform oder Größe
* gemeinsamer Standort, gemeinsame Stadt oder gemeinsames Land
* gemeinsame Teilnahme an einer Veranstaltung ohne benannte Zusammenarbeit
* Nennung beider in derselben Pressemitteilung ohne Aussage über ihr Verhältnis
* gemeinsame Erwähnung in einem Förderprogramm ohne gemeinsames Vorhaben
* Wettbewerbsverhältnis
* gemeinsame Mitgliedschaft in demselben Verband — das verbindet beide mit dem Verband, nicht miteinander
* Zitieren, Verlinken oder Erwähnen der einen Organisation durch die andere

---

# 3. Vokabular A — Akteur–Bauvorhaben

Für Kanten mit `Kantenart: AKTEUR-BAUVORHABEN`. Die Beziehungsart benennt, **welchen Beitrag der Akteur an diesem konkreten Bauvorhaben geleistet hat**.

### `Bauherrschaft`

Der Akteur hat das Vorhaben beauftragt, finanziert oder als Eigentümer verantwortet.

### `Entwurf`

Der Akteur hat das Vorhaben entworfen oder architektonisch geplant.

### `Fachplanung`

Der Akteur hat eine Fachdisziplin geplant — Tragwerk, Gebäudetechnik, Bauphysik, Brandschutz oder Schadstoffe.

### `Reuse-Konzept`

Der Akteur hat die Wiederverwendungsstrategie des Vorhabens entwickelt oder beratend begleitet.

### `Bauteilinventarisierung`

Der Akteur hat die vorhandenen Bauteile erfasst, bewertet oder auditiert.

### `Rückbau`

Der Akteur hat für dieses Vorhaben zerstörungsarm zurückgebaut, demontiert oder Bauteile geborgen.

### `Bauteillieferung`

Der Akteur hat gebrauchte Bauteile für dieses Vorhaben geliefert oder vermittelt.

### `Aufarbeitung`

Der Akteur hat Bauteile für dieses Vorhaben repariert, aufgearbeitet oder angepasst.

### `Logistik`

Der Akteur hat für dieses Vorhaben transportiert, zwischengelagert oder die Baustellenlogistik übernommen.

### `Bauausführung`

Der Akteur hat gebaut, montiert oder Bauteile eingebaut.

### `Prüfung und Nachweis`

Der Akteur hat Bauteile für dieses Vorhaben geprüft, zertifiziert oder ihre Zulassung nachgewiesen.

### `Forschungsbegleitung`

Der Akteur hat das Vorhaben wissenschaftlich begleitet, dokumentiert oder als Pilot ausgewertet.

### `Förderung`

Der Akteur hat das Vorhaben mit öffentlichen oder privaten Mitteln gefördert.

### `Betrieb`

Der Akteur betreibt oder bewirtschaftet das fertiggestellte Objekt.

### `Projektbeteiligung, Aufgabe unklar`

Die Mitwirkung am Vorhaben ist belegt, die konkrete Aufgabe geht aus der Quelle nicht hervor.

Nur verwenden, wenn die Beteiligung feststeht. Wenn schon die Beteiligung fraglich ist, gilt Abschnitt 5.

---

# 4. Vokabular B — Akteur–Akteur

Für Kanten mit `Kantenart: AKTEUR-AKTEUR`. Die Beziehungsart benennt das **organisatorische Verhältnis** der beiden Akteure.

### `Konsortialpartner`

Beide wirken in einem benannten gemeinsamen Projekt, Forschungsvorhaben oder Konsortium mit. Die Quelle muss das Vorhaben benennen.

### `Kooperationsvereinbarung`

Eine formalisierte Zusammenarbeit außerhalb eines einzelnen Projekts — Rahmenvertrag, Partnerschaft, gemeinsame Initiative.

### `Gemeinsames Bauvorhaben`

Beide haben an demselben Bauvorhaben mitgewirkt, das Vorhaben selbst ist aber kein eigener Knoten im Netz.

### `Gründung`

Der eine Akteur hat den anderen gegründet, mitgegründet oder als Spin-off hervorgebracht. **Gerichtet.**

### `Übernahme`

Der eine Akteur hat den anderen oder dessen Geschäftsbetrieb übernommen oder gekauft. **Gerichtet.**

### `Konzernbindung`

Der eine Akteur ist Tochter, Abteilung, Geschäftsbereich oder Beteiligung des anderen. **Gerichtet.**

### `Betreiberschaft`

Der eine Akteur betreibt eine Einrichtung, Anlage, Plattform oder ein Depot des anderen. **Gerichtet.**

### `Mitgliedschaft`

Der eine Akteur ist Mitglied im Netzwerk, Verband oder in der Genossenschaft des anderen. **Gerichtet.**

Nicht verwenden für zwei Akteure, die lediglich beide Mitglied desselben Dritten sind.

### `Trägerschaft`

Der eine Akteur trägt, finanziert oder verantwortet den anderen institutionell — etwa eine Kommune gegenüber einer von ihr getragenen Einrichtung. **Gerichtet.**

### `Lieferbeziehung`

Der eine Akteur liefert dem anderen regelmäßig Bauteile oder Material. **Gerichtet.**

### `Dienstleistungsbeziehung`

Der eine Akteur erbringt für den anderen eine benannte Dienstleistung — Beratung, Planung, Rückbau, Prüfung. **Gerichtet.**

### `Personelle Verflechtung`

Dieselbe Person führt, gründet oder leitet beide Akteure.

### `Verzeichniseintrag`

Beide sind lediglich gemeinsam in einem Verzeichnis gelistet. Siehe Abschnitt 2 — diese Kante wird entfernt.

### `Zusammenarbeit, Art unklar`

Eine Zusammenarbeit ist ausdrücklich belegt, ihre Form geht aus der Quelle nicht hervor.

---

# 5. Rückfallwerte

## Kein Beleg für eine Beziehung

**Beziehungsart:** `Kein Beleg für eine Beziehung`
**Richtung:** `—`
**Beschreibung:** `Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung.`

Verwenden, wenn die Recherche durchgeführt wurde und keine Quelle die Verbindung trägt. Bei `UNGEPRUEFT`-Kanten ist das ein zu erwartendes Ergebnis, kein Fehler.

## Beziehung nicht prüfbar

**Beziehungsart:** `Beziehung nicht prüfbar`
**Richtung:** `—`
**Beschreibung:** `Die Quelle ist nicht erreichbar, eine Prüfung war nicht möglich.`

Verwenden, wenn die Beleg-URL nicht erreichbar ist und keine Ersatzquelle gefunden wurde.
Nicht verwenden, wenn die Seite erreichbar war und nur nichts hergab — dann gilt `Kein
Beleg für eine Beziehung`. **Dieser Wert führt ebenfalls zur Löschung:** Nichtprüfbarkeit
ist kein Beleg für eine Beziehung.

---

# 6. Vorrang bei mehreren zutreffenden Arten

Trifft mehr als eine Art zu, nimm die strukturell stärkste. Vorrang von oben nach unten:

1. `Übernahme`
2. `Konzernbindung`
3. `Gründung`
4. `Trägerschaft`
5. `Betreiberschaft`
6. `Personelle Verflechtung`
7. `Konsortialpartner`
8. `Gemeinsames Bauvorhaben`
9. `Kooperationsvereinbarung`
10. `Lieferbeziehung`
11. `Dienstleistungsbeziehung`
12. `Mitgliedschaft`
13. `Zusammenarbeit, Art unklar`
14. `Verzeichniseintrag`

Beispiel: Sind zwei Akteure Konsortialpartner **und** steht der eine im Anbieterverzeichnis des anderen, gilt `Konsortialpartner`. Eine dauerhafte Struktur schlägt eine punktuelle.

Bei `AKTEUR-BAUVORHABEN` gilt: die Aufgabe, die den größten Teil des Reuse-Beitrags ausmacht. Hat ein Büro entworfen *und* das Reuse-Konzept erstellt, gilt `Reuse-Konzept`, weil das die spezifischere Aussage ist.

---

# 7. Richtung

Die Zeichnung ist ungerichtet, die Beziehung ist es oft nicht. Gib die Richtung deshalb ausdrücklich an:

* `A→B` — Knoten A ist der handelnde oder übergeordnete Teil
* `B→A` — Knoten B ist der handelnde oder übergeordnete Teil
* `—` — die Beziehung ist symmetrisch

Lesart je Art:

| Art | `A→B` bedeutet |
|---|---|
| `Gründung` | A hat B gegründet |
| `Übernahme` | A hat B übernommen |
| `Konzernbindung` | B gehört zu A |
| `Trägerschaft` | A trägt B |
| `Betreiberschaft` | A betreibt eine Einrichtung von B |
| `Mitgliedschaft` | A ist Mitglied bei B |
| `Lieferbeziehung` | A liefert an B |
| `Dienstleistungsbeziehung` | A erbringt die Leistung für B |

Symmetrisch (immer `—`): `Konsortialpartner`, `Kooperationsvereinbarung`, `Gemeinsames Bauvorhaben`, `Personelle Verflechtung`, `Verzeichniseintrag`, `Zusammenarbeit, Art unklar`, alle Rückfallwerte.

Bei `AKTEUR-BAUVORHABEN` immer die Richtung Akteur → Bauvorhaben angeben, also `A→B` oder `B→A` je nachdem, welcher Knoten der Akteur ist.

---

# 8. Regeln für die Beschreibung

## Inhalt

Die Beschreibung muss benennen, **was die beiden Knoten konkret verbindet**:

* Welche gemeinsame Sache? (Projektname, Vorhaben, Einrichtung)
* Welcher Beitrag oder welches Verhältnis?
* Bei gerichteten Arten: wer gegenüber wem?

## Form

* Ein kurzer vollständiger Satz, **höchstens 90 Zeichen**.
* Wo möglich den **Namen der gemeinsamen Sache** nennen — das ist der wertvollste Teil.
* Aktiv formulieren.
* Keine Wiederholung der Beziehungsart in anderen Worten.
* Keine Wertungen, keine Marketing-Sprache.
* Keine Namen der beiden Knoten wiederholen — sie stehen bereits in der Tabelle.

## Gute Beispiele

    Konsortialpartner im EU-H2020-Projekt BAMB.
    Aufbereitung und Logistik des wiederverwendeten Stahls.
    Gründungsmitglied der BauKarussell-Genossenschaft.
    Übernahm die Plattform Oogstkaart.nl vom Entwickler.
    Betreibt das Materialdepot der Sirkulær Ressurssentral.
    Entwurfsarchitekt des Reuse-Vorhabens.
    Abteilung innerhalb des Gruner-Konzerns.

## Schlechte Beispiele

    Arbeiten zusammen.                          (nichtssagend)
    Sind Partner.                                (wiederholt nur die Art)
    Beide engagieren sich für Kreislaufwirtschaft. (keine Verbindung)
    Wichtige Kooperation im Bereich Reuse.       (Wertung ohne Inhalt)
    A und B sind Konsortialpartner.              (Namen wiederholt)

---

# 9. Interne Entscheidungsschritte

Für jede Kante:

1. Welche Kantenart? `AKTEUR-BAUVORHABEN` → Vokabular A, `AKTEUR-AKTEUR` → Vokabular B.
2. Bei `GEPRUEFT`: Beleg-URL öffnen. Bei `UNGEPRUEFT`: aktiv nach einer Quelle suchen.
3. Nennt die Quelle **beide** Knoten?
4. Beschreibt sie ihr Verhältnis — oder listet sie sie nur nebeneinander?
5. Ist es ein reiner Verzeichniseintrag? Dann `Verzeichniseintrag`, unabhängig davon, wie plausibel eine Zusammenarbeit wirkt.
6. Treffen mehrere Arten zu? Vorrang nach Abschnitt 6.
7. Ist die Art gerichtet? Dann Richtung bestimmen.
8. Beschreibung: benennt sie die gemeinsame Sache, ist sie ≤ 90 Zeichen?
9. Trägt die Evidenz nicht? Rückfallwert nach Abschnitt 5, ohne zu raten.

---

# 10. Abschließende Qualitätskontrolle

* Jede Eingabe hat genau eine Ausgabezeile, ID unverändert.
* Genau **eine** Beziehungsart je Kante, exakt aus dem Vokabular.
* Vokabular A nur bei `AKTEUR-BAUVORHABEN`, Vokabular B nur bei `AKTEUR-AKTEUR`.
* Richtung gesetzt und zur Art passend; symmetrische Arten tragen `—`.
* Beschreibung ≤ 90 Zeichen, nennt die gemeinsame Sache, wiederholt nicht die Art.
* Verzeichnis-Listungen sind als `Verzeichniseintrag` erkannt, nicht als Zusammenarbeit.
* Keine Beziehung allein aus gemeinsamer Branche, Ort oder Verbandsmitgliedschaft abgeleitet.
* Bei `UNGEPRUEFT` wurde tatsächlich gesucht, und die gefundene URL steht in der Beleg-Spalte.
* Jede positive Art hat eine erreichbare URL, die Art und Richtung tatsächlich trägt.
* Jede positive Art hat ein Belegzitat, das die konkrete Beziehung tatsächlich ausdrückt.
* Ist die Quelle nicht erreichbar und gibt es keinen Ersatz, wird nicht behalten, sondern `Beziehung nicht prüfbar` gesetzt.
* Bei Unsicherheit wurde nicht geraten.

---

## Zu klassifizierende Verbindungen

### NL:K061
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: The Green House Utrecht  [Bauvorhaben/Objekt]
- Knoten B: Pieters Bouwtechniek  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/projects/the-green-house/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Konstruktive Fachplanung (stability)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "stability: pieters bouwtechniek"

### NL:K062
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: The Green House Utrecht  [Bauvorhaben/Objekt]
- Knoten B: Strukton Worksphere  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/projects/the-green-house/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Gebaeudetechnik-Planung und -Ausfuehrung
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "building services: strukton worksphere"

### NL:K063
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: The Green House Utrecht  [Bauvorhaben/Objekt]
- Knoten B: Ballast Nedam  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/projects/the-green-house/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Hauptausfuehrender (main contractor)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "main contractor: ballast nedam"

### NL:K064
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: The Green House Utrecht  [Bauvorhaben/Objekt]
- Knoten B: Kampstaal  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/projects/the-green-house/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Ausfuehrender Stahlbauer
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "contractor steel construction: kampstaal"

### NL:K065
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: The Green House Utrecht  [Bauvorhaben/Objekt]
- Knoten B: De Groot & Visser  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/projects/the-green-house/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Ausfuehrender Fassadenbauer
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "facades: de groot & visser"

### NL:K066
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: ABN AMRO  [Unternehmen]
- Knoten B: Circl  [Bauvorhaben/Objekt]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.duurzaamnieuws.nl/abn-amro-geeft-circulair-bouwen-gezicht-met-paviljoen-circl/
- Bisherige Beschreibung (Altdaten, nur Hinweis): ABN AMRO ist Bauherrin/Entwicklerin und Betreiberin des Circl-Paviljoens, dessen Bauteile ueberwiegend wiederverwendet sind.
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "ABN AMRO heeft dit pand circulair ontwikkeld en gebouwd om de opgedane kennis te delen en klanten goed over circulariteit te kunnen adviseren."

### NL:K067
- Kantenart: AKTEUR-AKTEUR
- Knoten A: ABN AMRO  [Unternehmen]
- Knoten B: Victory Group  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://victorygroup.com/news/victory-group-acquires-abn-amros-zuidas-head-office
- Bisherige Beschreibung (Altdaten, nur Hinweis): Sale-and-leaseback: ABN AMRO verkaufte den Zuidas-Hauptsitz (inkl. spaeterer Rueckbau/Wiederverwendung des Circl-Pavillons) an Victory Group als Kaeufer.
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "ABN AMRO and Victory Group have announced that they have reached an agreement regarding the sale and leaseback of the bank's head office"

### NL:K068
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Villa Welpeloo Enschede  [Bauvorhaben/Objekt]
- Knoten B: Superuse Studios / 2012Architecten  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.ellenmacarthurfoundation.org/circular-examples/finding-and-utilising-waste-materials-for-construction-purposes
- Bisherige Beschreibung (Altdaten, nur Hinweis): Superuse Studios entwarf und realisierte Villa Welpeloo als ausfuehrendes Architekturbuero.
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Villa Welpeloo is a house and art studio designed and constructed in 2005 by Superuse Studios."

### NL:K069
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Superuse Studios / 2012Architecten  [Unternehmen]
- Knoten B: New Horizon UM  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://architectenweb.nl/nieuws/artikel.aspx?ID=47638
- Bisherige Beschreibung (Altdaten, nur Hinweis): New Horizon Urban Mining nam het platform Oogstkaart.nl over, dat Superuse Studios tien jaar eerder ontwikkelde; samenwerking wordt voortgezet.
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Om die vraag te beantwoorden ontwikkelde Superuse Studios tien jaar geleden het platform Oogstkaart.nl. Met de overname door New Horizon Urban Mining moet het platform doorgroeien tot het belangrijkste platform op dit gebied in Nederland."

### NL:K070
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Woongroep Boschgaard…  [Bauvorhaben/Objekt]
- Knoten B: Bewohnerinitiative Boschgaard  [Organisation]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.crowdbuilding.com/d/initiatieven/boschgaard
- Bisherige Beschreibung (Altdaten, nur Hinweis): Bewohnerinitiative gruendete und verwaltet das Wohnprojekt Boschgaard
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "het initiatief volledig bij de toekomstige bewoners vandaan komt"

### NL:K071
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Woongroep Boschgaard…  [Bauvorhaben/Objekt]
- Knoten B: Zayaz  [Organisation]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.zayaz.nl/boschgaard
- Bisherige Beschreibung (Altdaten, nur Hinweis): Zayaz ist Bauherrin/Eigentuemerin von Boschgaard
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Zayaz ondersteunt en faciliteert hen hierin. En blijft eigenaar van het gebouw"

### NL:K072
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Woongroep Boschgaard…  [Bauvorhaben/Objekt]
- Knoten B: Bouwbedrijf Versteegden  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.versteegden.nl/koninklijk-bezoek/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Versteegden ist ausfuehrendes Bauunternehmen im Auftrag von Zayaz fuer Boschgaard
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Bouwbedrijf Versteegden bouwt in opdracht van woningcorporatie Zayaz in Den Bosch aan een voor Nederland uniek circulair woonproject."

### NL:K073
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Woongroep Boschgaard…  [Bauvorhaben/Objekt]
- Knoten B: Transfarmers  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://boschgaard.nl/transfarmers/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Transfarmers ist zentraler Partner von Boschgaard, Nutzer der Gemeinschaftsraeume
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Transfarmers is meer dan gewoon een partner. We kunnen zeker zeggen dat Boschgaard er niet geweest was als Transfarmers niet bestaan had."

### NL:K074
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Woongroep Boschgaard…  [Bauvorhaben/Objekt]
- Knoten B: VanNimwegen  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://boschgaard.nl/van-nimwegen/
- Bisherige Beschreibung (Altdaten, nur Hinweis): VanNimwegen ist Berater fuer die Wooncooperatie Boschgaard
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Warren van Hoof, van adviesbureau VanNimwegen, is onder andere op het gebied van wooncoöperaties onze adviseur."

### NL:K075
- Kantenart: AKTEUR-AKTEUR
- Knoten A: lcp-circulair  [Unternehmen]
- Knoten B: Icon Real Estate  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://iconrealestate.com/news/circular-innovation-the-dismantling-of-the-circl-pavilion/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Icon Real Estate beauftragt lcp-circulair als Demontage-/Reuse-Partner fuer das Circl-Paviljoen-Projekt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "We're teaming up with lcp-circulair, a joint venture between cepezedprojects and Lagemaat."

### NL:K076
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Icon Real Estate  [Unternehmen]
- Knoten B: Victory Group  [Unternehmen]
- Land: NL
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### NL:K077
- Kantenart: AKTEUR-AKTEUR
- Knoten A: New Horizon  [Unternehmen]
- Knoten B: Urban Mining Collective  [NGO/Verband/Netzwerk]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.baars-bloemhoff.nl/baars-&-bloemhoff-wordt-partner-van-urban-mining-collective-cms-bb-intro-partner-urbanminingcollective
- Bisherige Beschreibung (Altdaten, nur Hinweis): New Horizon und Urban Mining Collective werden gemeinsam als Traeger derselben Kooperation genannt (New Horizon als operativer Partner/Betreiber des Kollektivs)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Sinds dit jaar werken we samen met New Horizon en maken we deel uit van het Urban Mining Collective, samen met Stiho en andere partners uit de bouwwereld."

### NL:K078
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Baars & Bloemhoff  [Materialhub/Bauteilbörse]
- Knoten B: Urban Mining Collective  [NGO/Verband/Netzwerk]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.baars-bloemhoff.nl/baars-&-bloemhoff-wordt-partner-van-urban-mining-collective-cms-bb-intro-partner-urbanminingcollective
- Bisherige Beschreibung (Altdaten, nur Hinweis): Baars & Bloemhoff ist Partner des Urban Mining Collective
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Sinds dit jaar werken we samen met New Horizon en maken we deel uit van het Urban Mining Collective, samen met Stiho en andere partners uit de bouwwereld."

