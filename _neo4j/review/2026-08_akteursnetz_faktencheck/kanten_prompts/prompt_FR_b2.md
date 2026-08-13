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

### FR:K021
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Grande Halle de Colombel…  [Bauvorhaben/Objekt]
- Knoten B: Le WIP  [Organisation]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.ekopolis.fr/operations-batiment/grande-halle-de-colombelles
- Bisherige Beschreibung (Altdaten, nur Hinweis): Le WIP war titulaire des Reemploi-Loses und Betreiber des Gebaeudes
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Le WIP, actuel exploitant du bâtiment, a été titulaire de ce lot Réemploi"

### FR:K022
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Maison des Canaux, Paris  [Bauvorhaben/Objekt]
- Knoten B: Les Canaux  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.paris.fr/pages/les-canaux-une-maison-des-economies-solidaires-et-innovantes-4133
- Bisherige Beschreibung (Altdaten, nur Hinweis): Maison des Canaux wird von der Vereinigung Les Canaux betrieben (gérée par)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "la Maison des Canaux, gérée par l'association Les Canaux"

### FR:K023
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Maison des Canaux, Paris  [Bauvorhaben/Objekt]
- Knoten B: Ville de Paris  [Öffentliche Institution]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.paris.fr/pages/l-economie-circulaire-au-coeur-du-chantier-de-la-maison-des-canaux-16966
- Bisherige Beschreibung (Altdaten, nur Hinweis): Ville de Paris als Auftraggeberin/Initiatorin des Sanierungsprojekts Maison des Canaux mit Zirkularitaets-Auflage
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "La Ville de Paris a décidé d'en faire un chantier de travaux exemplaire, sur le plan environnemental, notamment en économie circulaire, et solidaire."

### FR:K024
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Ville de Paris  [Öffentliche Institution]
- Knoten B: Plateforme de réemploi des matériaux de voirie de la Ville de Paris  [Software/Tool-Anbieter]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.paris.fr/pages/le-pave-parisien-a-l-epreuve-du-temps-7511
- Bisherige Beschreibung (Altdaten, nur Hinweis): Direction de la voirie et des déplacements (Dienststelle der Ville de Paris) betreibt den Materialdepot-Standort in Bonneuil-sur-Marne
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Tous les chantiers de voirie parisiens ont leur réserve de granit au cœur d'un immense dépôt de la Direction de la voirie et des déplacements à Bonneuil sur Marne."

### FR:K025
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: Novaedia / Novædia  [Organisation]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Novaedia ist Bauherrin/Nutzerin des Gebaeudes Résilience (Sitz + Werkstaetten)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Le bâtiment accueillera en mars 2020 le siège social et les ateliers de Novaedia, coopérative à but d'insertion sociale"

### FR:K026
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: SOCOTEC  [Unternehmen]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://topophile.net/faire/la-ferme-des-possibles-ou-de-la-serendipite/
- Bisherige Beschreibung (Altdaten, nur Hinweis): SOCOTEC als technischer Kontrolleur des Projekts Résilience
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "contrôleur technique : SOCOTEC"

### FR:K027
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: Depuis 1920  [Unternehmen]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Depuis 1920 als ausfuehrende Tischlerei fuer wiederverwendete Fensterrahmen bei Résilience
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Les châssis ont été déposés, transportés et retravaillés dans les ateliers de l'entreprise de menuiseries Depuis1920"

### FR:K028
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: Association Réavie  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Réavie als Materiallieferant (sanitaere/elektrische Wiederverwendungselemente) fuer Résilience
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "L'association Réavie a préparé et livré des éléments tels que des WC, des luminaires, des poignées de portes, des mitigeurs"

### FR:K029
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: Métabolisme Urbain  [Organisation]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Materialgisement fuer Résilience im Rahmen des Programms Métabolisme Urbain (Plaine Commune) inventarisiert
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Le gisement a été inventoriée par Bellastock dans le cadre du projet « Métabolisme urbain »"

### FR:K030
- Kantenart: AKTEUR-BAUVORHABEN
- Knoten A: Résilience  [Bauvorhaben/Objekt]
- Knoten B: Archipel zéro  [Unternehmen]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Archipel zéro als entwerfende Architekturagentur des Projekts Résilience
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Conçu par l'agence d'architecture Frédéric Denise – Archipel Zéro, le projet illustre l'engagement de la maîtrise d'ouvrage"

### FR:K031
- Kantenart: AKTEUR-AKTEUR
- Knoten A: La Fab Bordeaux  [Öffentliche Institution]
- Knoten B: Collectif CANCAN  [Unternehmen]
- Land: FR
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### FR:K032
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Encore Heureux  [Unternehmen]
- Knoten B: REMIX / matériaux réemploi  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://encoreheureux.org/en/news/creation-d-un-bureau-d-etudes-dedie-au-reemploi
- Bisherige Beschreibung (Altdaten, nur Hinweis): Encore Heureux Architectes (mit Morgan Moinet) hat REMIX gegruendet
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Encore Heureux Architectes et Morgan Moinet décident de fonder REMIX, un bureau d'études"

### FR:K033
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Mobius Réemploi  [Unternehmen]
- Knoten B: CSTB  [Forschung/Lehre]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cstb.fr/nos-offres/toutes-nos-offres/accompagner-developpement-reemploi
- Bisherige Beschreibung (Altdaten, nur Hinweis): SPIROU-Forschungskonsortium, Mobius Réemploi als CSTB-Partner
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "le projet de recherche SPIROU (Sécuriser les Pratiques Innovantes de Réemploi via une Offre Unifiée) co-financé par l'ADEME, le CSTB et ses partenaires Mobius réemploi, le Booster du Réemploi / A4MT et Qualiconsult"

### FR:K034
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CANCAN Architecture  [Unternehmen]
- Knoten B: REFAIR Bordeaux  [Materialhub/Bauteilbörse]
- Land: FR
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### FR:K035
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CSTB  [Forschung/Lehre]
- Knoten B: Bellastock  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://lecho-circulaire.com/le-projet-fcrbe-facilite-le-reemploi-dans-la-construction/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Beide als Konsortialpartner im FCRBE-Interreg-Projekt genannt (Drittquelle, gespeicherte REPAR-Zuordnung nicht eigenstaendig verifiziert)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Bellastock et le CSTB en France, Bruxelles-Environnement, Belgian Building Research Institute (BBRI) et la Confédération de la Construction en Belgique, la School of Architecture and Design de l'Université de Brighton et l'opérateur britannique Salvo."

### FR:K036
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CSTB  [Forschung/Lehre]
- Knoten B: FCRBE (Facilitating the Circulation of Reclaimed Building Elements)  [Forschung/Lehre]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://lecho-circulaire.com/le-projet-fcrbe-facilite-le-reemploi-dans-la-construction/
- Bisherige Beschreibung (Altdaten, nur Hinweis): CSTB als Konsortialpartner im FCRBE-Projekt
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Bellastock et le CSTB en France, Bruxelles-Environnement, Belgian Building Research Institute (BBRI) et la Confédération de la Construction en Belgique, la School of Architecture and Design de l'Université de Brighton et l'opérateur britannique Salvo."

### FR:K037
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CSTB  [Forschung/Lehre]
- Knoten B: Fédération Française du Bâtiment et des Travaux publics de Haute-Garonne (FFB 31)  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cstb.fr/toutes-les-actualites/projet-life-waste2build
- Bisherige Beschreibung (Altdaten, nur Hinweis): Gemeinsame Mitgliedschaft im LIFE-Waste2Build-Konsortium (Toulouse Métropole)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "le consortium piloté par Toulouse Métropole réunissant le CSTB et cinq autres partenaires (Synéthic, Envirobat Occitanie, Toulouse Business School, la Fédération Française du Bâtiment et des Travaux Publics du 31, l'Institut National de l'Économie Circulaire)"

### FR:K038
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CSTB  [Forschung/Lehre]
- Knoten B: Institut National de l'Économie Circulaire (INEC)  [NGO/Verband/Netzwerk]
- Land: FR
- Belegstatus: UNGEPRUEFT
- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'

### FR:K039
- Kantenart: AKTEUR-AKTEUR
- Knoten A: CSTB  [Forschung/Lehre]
- Knoten B: Booster du Réemploi (A4MT)  [Organisation]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://www.cstb.fr/nos-offres/toutes-nos-offres/accompagner-developpement-reemploi
- Bisherige Beschreibung (Altdaten, nur Hinweis): SPIROU-Forschungskonsortium, Booster du Réemploi/A4MT als CSTB-Partner
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "le projet de recherche SPIROU (Sécuriser les Pratiques Innovantes de Réemploi via une Offre Unifiée) co-financé par l'ADEME, le CSTB et ses partenaires Mobius réemploi, le Booster du Réemploi / A4MT et Qualiconsult"

### FR:K040
- Kantenart: AKTEUR-AKTEUR
- Knoten A: Bellastock  [NGO/Verband/Netzwerk]
- Knoten B: FCRBE (Facilitating the Circulation of Reclaimed Building Elements)  [Forschung/Lehre]
- Land: FR
- Belegstatus: GEPRUEFT
- Beleg-URL (MUSS geoeffnet werden): https://lecho-circulaire.com/le-projet-fcrbe-facilite-le-reemploi-dans-la-construction/
- Bisherige Beschreibung (Altdaten, nur Hinweis): Bellastock als Konsortialpartner im FCRBE-Projekt (franz. Partner)
- Gespeichertes Belegzitat (Nachweis-Schnipsel): "Bellastock et le CSTB en France, Bruxelles-Environnement, Belgian Building Research Institute (BBRI) et la Confédération de la Construction en Belgique, la School of Architecture and Design de l'Université de Brighton et l'opérateur britannique Salvo."

