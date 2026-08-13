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

### NL:K001
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: Lagemaat Heerde  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.gelderland.nl/themas/duurzaamheid/circulaire-economie/prinsenhof
- Bisherige Beschreibung (Altdaten, nur Hinweis): Lagemaat realisiert das Circulair Centrum Heerde aus den freikommenden Prinsenhof-Materialien
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Die uitdaging is opgepakt door de firma Lagemaat; die met vrijwel alle vrijkomende materialen er een circulair centrum van gaan realiseren in Heerde."

### NL:K002
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: cepezed  [Unternehmen]
- Land: NL
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### NL:K003
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: Provincie Gelderland  [Öffentliche Institution]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.gelderland.nl/themas/duurzaamheid/circulaire-economie/prinsenhof
- Bisherige Beschreibung (Altdaten, nur Hinweis): Provincie Gelderland ist Auftraggeberin des Prinsenhof-Projekts, dessen Materialien in das Circulair Centrum Heerde fliessen
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "We hebben als provincie en opdrachtgever betrokken en welwillende partijen de ruimte gegeven om te pionieren."

### NL:K004
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: ReCreate Dutch cluster  [Forschung/Lehre]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://recreate-project.eu/project-pilots/the-netherlands/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Der ReCreate Dutch Pilot Cluster errichtet das Wissenszentrum/Circular Centre in Heerde als Teil des Pilotprojekts
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "The building will be a knowledge centre for circular use of building components."

### NL:K005
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: IMd Raadgevende Ingenieurs  [Unternehmen]
- Land: NL
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### NL:K006
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Circular Centre Netherla…  [Bauvorhaben/Objekt]
- Knoten B: Dycore  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.gelderland.nl/themas/duurzaamheid/circulaire-economie/prinsenhof
- Bisherige Beschreibung (Altdaten, nur Hinweis): Dycore erstellt mit den Partnern das Garantieprotokoll fuer wiederverwendete Elemente, die u.a. in das Circulair Centrum Heerde gehen
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Met provincie, gemeente Arnhem, Lagemaat en Dycore: uitvoeringsprotocol opgesteld voor de garantiestelling voor tweedehands kanaalplaatvloeren en dragende wanden"

### NL:K007
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Lagemaat Heerde  [Unternehmen]
- Knoten B: lcp-circulair  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://lcp-circulair.nl/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Lagemaat ist Mitgruender/Partner der Joint Venture lcp-circulair (samenwerking tussen cepezed projects en Lagemaat)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "LCP circulair is een samenwerking tussen cepezed projects en Lagemaat"

### NL:K008
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Lagemaat Heerde  [Unternehmen]
- Knoten B: Ter Velde & Den Besten  [Software/Tool-Anbieter]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.aannemervak.nl/bouwpraktijk/bouwtrends/circulaire-aanpak-bewijst-kracht-80-materialen-krijgt-tweede-leven/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Beide im selben Circl-Paviljoen-Reuseprojekt taetig (Scan bzw. Demontage), keine explizite direkte Beauftragungs-/Partnerbeziehung zwischen den beiden auf der geoeffneten Seite genannt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Voorafgaand aan de demontage maakt ingenieursbureau Ter Velde & Den Besten uit Hattemerbroek een 3D-scan; demontagebedrijf Lagemaat uit Heerde vormt met Cepezedprojects lCP Circulair"

### NL:K009
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: cepezed  [Unternehmen]
- Knoten B: The Green House Utrecht  [Bauvorhaben/Objekt]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cepezed.com/recent/circulair-paviljoen-the-green-house-geopend/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Entwerfer/Architekt des Projekts
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "The circular and highly sustainable design was made by cepezed in commission of consortium R Creators."

### NL:K010
- Kantenart: AKTEUR-AKTEUR
- Knoten A: cepezed  [Unternehmen]
- Knoten B: lcp-circulair  [Unternehmen]
- Land: NL
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### NL:K011
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: IMd Raadgevende Ingenieurs  [Unternehmen]
- Knoten B: BioPartner 5  [Bauvorhaben/Objekt]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Constructief ontwerp (structural engineer) auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Constructief ontwerp: IMd Raadgevende Ingenieurs"

### NL:K012
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: IMd Raadgevende Ingenieurs  [Unternehmen]
- Knoten B: Montessori Maassluis  [Bauvorhaben/Objekt]
- Land: NL
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### NL:K013
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: BioPartner Center Leiden  [Organisation]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Opdrachtgever (client) auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Opdracht: Biopartner Center Leiden"

### NL:K014
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: Popma ter Steege Architecten / PTSA  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Architect auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Architectuur: Popma ter Steege Architecten"

### NL:K015
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: De Vries en Verburg  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Hoofdaannemer (main contractor) auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Hoofduitvoering: De Vries en Verburg"

### NL:K016
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: Vic Obdam Staalbouw  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Staalbouwer (steel contractor) auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Staalbouw: Vic Obdam Staalbouw"

### NL:K017
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: Deerns  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Installatie-/bouwfysica-adviseur auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Advies installatietechniek, bouwfysica en duurzaamheid: Deerns"

### NL:K018
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: STONE22  [Unternehmen]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.staalmakers.nl/projecten/biopartner-5/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Projectmanagement auf dem BioPartner-5-Projektblatt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Projectmanagement: Stone 22"

### NL:K019
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BioPartner 5  [Bauvorhaben/Objekt]
- Knoten B: Leiden University / Gorlaeus donor source  [Forschung/Lehre]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.universiteitleiden.nl/en/news/2020/11/gorlaeus-highrise-lives-on-in-two-new-buildings-in-leiden
- Bisherige Beschreibung (Altdaten, nur Hinweis): Donor-Stahlquelle (Gorlaeus-Gebaeude der Universiteit Leiden) fuer das Donorskelet von BioPartner 5
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "The metal was processed on our campus and then used as a 'donor skeleton' for BioPartner's fifth building."

### NL:K020
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: BlueCity Offices…  [Bauvorhaben/Objekt]
- Knoten B: BlueCity / Blue City 010 BV  [Organisation]
- Land: NL
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://rotterdamarchitectuurprijs.nl/index.php?item=blue-city-010-offices&lang=nl&tag=utiliteit
- Bisherige Beschreibung (Altdaten, nur Hinweis): Opdrachtgever (Bauherr) des Projekts Blue City 010 Offices
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Opdrachtgever: Blue City"

