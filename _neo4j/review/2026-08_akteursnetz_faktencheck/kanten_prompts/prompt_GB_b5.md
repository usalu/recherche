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

### GB:K081
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Roots in the Sky  [Bauvorhaben/Objekt]
- Knoten B: Erith  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.theconstructionindex.co.uk/news/view/second-hand-steel-to-hold-up-forest-in-the-sky
- Bisherige Beschreibung (Altdaten, nur Hinweis): Rueckbau/Bauteilernte (Abbruch- und Baugrubenarbeiten)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Erith will deliver the basement box and demolition works as part of the two-stage construction process."

### GB:K082
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Roots in the Sky  [Bauvorhaben/Objekt]
- Knoten B: Fabrix  [Unternehmen]
- Land: GB
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### GB:K083
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: AKT II  [Unternehmen]
- Knoten B: 55 Great Suffolk Street  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### GB:K084
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Symmetrys  [Unternehmen]
- Knoten B: 55 Great Suffolk Street  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### GB:K085
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Mace  [Unternehmen]
- Knoten B: Timber Square London  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### GB:K086
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Landsec  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://ukgbc.org/resources/timber-square/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Bauherr/Client
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Client: Landsec"

### GB:K087
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Bennetts Associates  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://ukgbc.org/resources/timber-square/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Architect
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Architect: Bennetts Associates"

### GB:K088
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Hoare Lea  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://ukgbc.org/resources/timber-square/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Sustainability Consultant
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Sustainability: Hoare Lea"

### GB:K089
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Alinea / T+T Alinea  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.ttalinea.com/news/timber-square-reaches-practical-completion/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Quantity Surveyor / Cost Management
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Since 2018, we have provided full cost management services through to completion"

### GB:K090
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Opera  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.operapm.co.uk/place/our-projects/timber-square-southwark
- Bisherige Beschreibung (Altdaten, nur Hinweis): Project Manager / Employer's Agent
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Opera have led the procurement and management of the professional team, programming and contractor procurement strategy for the site"

### GB:K091
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Timber Square London  [Bauvorhaben/Objekt]
- Knoten B: Hybrid Structures  [Unternehmen]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.bdonline.co.uk/intelligence-for-architects/timber-square-a-step-up-for-clt/5143269.article
- Bisherige Beschreibung (Altdaten, nur Hinweis): Bauausfuehrung CLT/Stahl-Superstruktur
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "a job done by the Hybrid Structures division of specialist Hare, which also did the steelwork"

### GB:K092
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Opera  [Unternehmen]
- Knoten B: 55 Great Suffolk Street  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://asbp.org.uk/case-studies/55-great-suffolk-street
- Bisherige Beschreibung (Altdaten, nur Hinweis): Project Manager
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Opera (Project Manager – 55 Great Suffolk Street)"

### GB:K093
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Hawkins\Brown  [Unternehmen]
- Knoten B: 55 Great Suffolk Street  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.hawkinsbrown.com/projects/55-great-suffolk-street/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Architect
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Scope: Architecture"

### GB:K094
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Fabrix  [Unternehmen]
- Knoten B: 55 Great Suffolk Street  [Bauvorhaben/Objekt]
- Land: GB
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.ukgbc.org/solutions/case-study-55-great-suffolk-street/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Bauherr/Client
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Fabrix (client)"

### GB:K095
- Kantenart: AKTEUR-AKTEUR
- Knoten A: The Engineers Reuse Collective (TERC)  [Unternehmen]
- Knoten B: Elliott Wood  [Unternehmen]
- Land: GB
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

