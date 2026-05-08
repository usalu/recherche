# Woongroep Boschgaard, Den Bosch — Fallstudie Bauteilwiederverwendung / Direct Reuse

## 1. EINORDNUNG

- **Entscheidung:** VERGLEICHSFALL
- **Bewertung:** ★★★☆☆
- **Begründung:** Reales Wohnprojekt mit hohem Anteil sekundärer / geernteter Bauprodukte und mehreren fest eingebauten Reuse-Bauteilen. Besonders relevant sind wiederverwendete Holz-Dachspanten, eine Aluminiumfassade und wiederverwendete Holz-/Ausbaumaterialien. Nicht als Direct Reuse gewertet werden lose Einrichtungen oder normaler Bestandserhalt des ehemaligen Nachbarschaftszentrums.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** ja
- **Warnung Möbel/Dekoration:** ja
- **Projektstatus:** gebaut / in Nutzung seit 2024

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Woongroep Boschgaard / Collectief Ecosysteem Boschgaard | untersuchter Fall | Superuse; Boschgaard; Zayaz | belegt | Wohnprojekt mit Nachbarschaftsfunktion |
| Ort | Den Bosch / ’s-Hertogenbosch, NL | Standort | Boschgaard; Superuse | belegt | Mgr. van Roosmalenplein 23 |
| Gebäude | ehemaliges Nachbarschaftszentrum De Patio + neue Wohnbauten | Ausgangs- und Zielgebäude | Zayaz; Houtbouw Lente | teilweise belegt | Transformation + Neubauanteile |
| Projekt | 19 soziale Mietwohnungen + Nachbarschaftszentrum | Programm | Superuse; Zayaz | belegt | gemeinschaftliches Wohnen |
| People | Bewohnerinitiative, Zayaz, Superuse Studios, Bouwbedrijf Versteegden, Transfarmers, VanNimwegen | Projektakteure | Boschgaard; Superuse | teilweise belegt | genaue Rollen teils nicht öffentlich detailliert |
| Reuse-Strategie | Oogsten / material harvesting, bauen mit Restmaterialien | zentrale Strategie | Boschgaard; Superuse | belegt | „we don’t go to the construction market“ bei Superuse |
| Bauteil | Holz-Dachspanten / Brettschichtholz-Kniespanten | tragendes / dachbildendes Reuse-Bauteil | Boschgaard; ED.nl; Circulaire Bouweconomie | belegt | aus ehemaliger Bibliothek Sint-Michielsgestel |
| Bauteil | Aluminium-Fassadensystem | Hüllenbauteil | Boschgaard; Duurzame Metaalbouw | belegt | ehem. Stadskantoor Roosendaal; zweite Nutzung als Fassade |
| Bauteil | Holz aus ehemaliger Bibliothek / Tankstelle / Schule / Kunstakademie | HSB, Balken, Ausbaumaterial | Houtbouw Lente; A. Jansen; Circulaire Bouweconomie | teilweise belegt | genaue Position je Bauteil teils unbekannt |
| Material | Sekundärmaterialien / oogstmaterialen | Materialbasis des Projekts | Superuse; Boschgaard | belegt | 84–85 % sekundär/geerntet je nach Quelle |
| Kennwert | 84 % sekundäre Materialien | Circularity-Kennwert | Superuse; The Plan | belegt | Quelle nennt nationalen Vergleich 8 % |
| Kennwert | 85 % bzw. Ziel 90 % wiederverwendete/geerntete Materialien | abweichender Kennwert | Boschgaard; Houtbouw Lente | teilweise belegt | als Quellenkonflikt behandeln |
| Kennwert | 70 % CO₂-Einsparung gegenüber aktuellem Baustandard | Umweltwirkung | Superuse; Boschgaard-Fassadenartikel | teilweise belegt | Methode/Bilanzgrenze öffentlich nicht ausreichend detailliert |
| Kennwert | 700.000 € vermiedene zukünftige Umweltschäden | wirtschaftlich-ökologischer Kennwert | Superuse | teilweise belegt | kein Kostenersatz; Methode unbekannt |
| Logistik | Materiallager / loods | notwendige Zwischenlagerung | Boschgaard Circulariteit | belegt | Lagerplatz als zentrale Hürde |
| Hürde | Materialverfügbarkeit vor Bauplanung | Planungs-/Beschaffungshürde | Boschgaard Circulariteit; Houtbouw Lente | belegt | Entwurf muss Materialfunden folgen |
| Hürde | Bauphysik, Schall, Ausführung | technische Hürde | Houtbouw Lente | belegt | Risiko Schalllecks genannt |
| Hürde | Holzschädlinge / boktor | technische Hürde | Houtbouw Lente | belegt | Risiko bei wiederverwendetem Holz |
| Wirtschaft | Budget sozialer Wohnungsbau | Kostenrahmen | Superuse; Zayaz | teilweise belegt | Bewohnerarbeit als Teil der Umsetzbarkeit |
| Schadstoff | unbekannt | möglicher Prüfbereich | keine spezifische Quelle gefunden | unklar | für geerntete Bauteile nicht öffentlich belegt |
| Prüfung | unbekannt | Qualitäts-/Tragfähigkeitsprüfung | keine spezifische Quelle gefunden | unklar | besonders für Holztragwerk relevant |
| Norm | unbekannt | bauordnungsrechtlicher Nachweis | keine spezifische Quelle gefunden | unklar | keine Normnummern erfinden |
| Software | unbekannt | Erfassung/Matching | keine spezifische Quelle gefunden | unklar | Superuse-Methode, aber Tool nicht belegt |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Oogstmaterial / geerntetes Material | Niederländische Praxis benennt Bauteile als „geerntet“, nicht nur gekauft | Dachspanten, Fassaden, Balken | Bauteil, Logistik, Beschaffungsmodell |
| Bewohner-Selbstbau / Selbstwerkzaamheid | Beteiligung der künftigen Nutzer ist prozessprägend | Bewohner ernten Materialien und bauen mit | People, Wirtschaft, Prozessphase |
| Materiallager / Zwischenlager | Für Reuse-Beschaffung zentral und nicht nur Transport | volle angemietete Lagerhalle | Logistik, Bauteilbörse, Hürde |

## 3. FALLSTUDIE

- **Name:** Woongroep Boschgaard / Collectief Ecosysteem Boschgaard
- **Ort:** ’s-Hertogenbosch / Den Bosch, Niederlande
- **Gebäude:** ehemaliges Nachbarschaftszentrum De Patio; neue Wohn- und Gemeinschaftsbauten
- **Projekt:** 19 soziale Mietwohnungen mit Nachbarschaftszentrum und kollektivem Wohnen
- **Beteiligte People / Akteure:** Bewohnerinitiative Boschgaard, Wohnungsbaugesellschaft Zayaz, Superuse Studios, Bouwbedrijf Versteegden, Transfarmers, VanNimwegen; weitere Materiallieferanten / Rückbauakteure
- **Architekt:** Superuse Studios
- **Tragwerksplaner:** unbekannt
- **Bauherr:** Zayaz / Projektstruktur mit Bewohnerinitiative; genaue Eigentums-/Bauherrschaftsrolle je Projektphase unbekannt
- **Zeitraum:** Entwicklung vor 2024; Fertigstellung / Inbetriebnahme Anfang 2024; Eröffnung 1. Juni 2024 laut Boschgaard-Fassadenartikel
- **Ursprüngliche Nutzung:** Nachbarschaftszentrum / ehemaliges buurthuis De Patio
- **Neue Nutzung:** 19 soziale Mietwohnungen, kollektive Wohnfunktionen, Nachbarschaftszentrum
- **Fläche / Maßstab:** unbekannt; 19 Wohneinheiten belegt
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** gut für Grunddaten und Reuse-Anspruch; mittel für genaue Bauteilprüfungen, Mengen je Bauteil und Normen

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ Bauteilwiederverwendung; in-situ Bestandstransformation; Materialwiederverwendung
- **Hauptniveau:** räumlicher Innenausbau / Gebäudehülle / Dachtragwerk / Material
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Das Weiterverwenden des ehemaligen Nachbarschaftszentrums zählt nur als Kontext. Reuse zählt hier dort, wo Bauteile aus anderen Rückbauquellen neu eingebaut wurden oder vorhandene Bauteile in neuer Funktion eingesetzt wurden, z. B. Holz-Dachspanten, Aluminiumfassade und geerntete Holzbauteile.
- **Warum ist der Fall relevant?** Boschgaard zeigt, wie ein soziales Wohnprojekt mit Bewohnerbeteiligung, Materialernte und starkem Reuse-Anteil realisiert werden kann. Die Relevanz liegt weniger in einem einzelnen spektakulären Tragwerk als in der systematischen Beschaffung und Integration vieler gebrauchter Bauteile.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Dachspanten / Kniespanten | Brettschichtholz / Holz | ehemalige Bibliothek De Brenthof, Sint-Michielsgestel | Dach-/Überdachungstragwerk | Dachaufbau / Dachform Boschgaard | 24 Spanten laut ED.nl; Boschgaard nennt große hölzerne Dachspanten | ja | ja | nein | nein | Ausbau, Transport, Lagerung, Anpassung | unbekannt | unbekannt | Tragfähigkeit, Dauerhaftigkeit, Holzschutz | unbekannt | Geometrie passte erst nach Planungsabgleich; Lagerung | Boschgaard, ED.nl, Circulaire Bouweconomie | Prüfung, Verbindung |
| Aluminium-Fassadensystem | Aluminium, Glas | Stadskantoor Roosendaal | Fassadensystem | Fassade im Wohnprojekt | Umfang unbekannt; 50 Jahre alte Fassade belegt | nein | nein | ja | nein | Demontage, Anpassung an neuen Entwurf | unbekannt | unbekannt | Witterung, Dichtigkeit, Wärme, Befestigung | unbekannt | Maßanpassung, Gestaltung, Gewährleistung | Boschgaard, Duurzame Metaalbouw | Menge, U-Wert |
| HSB-Holz / Balken | Holz | u. a. ehemalige Bibliothek Sint-Michielsgestel, geslooptes Tankstation Haarlem, alte Kunstakademie, Schule Boschveld | Trag-/Ausbauholz | HSB-Wände/-Decken, Balken, Ausbau | unbekannt | teilweise | ja | teilweise | nein | Sortieren, Zuschnitt, ggf. Behandlung | unbekannt | unbekannt | Tragfähigkeit, Schallschutz, Holzschutz | unbekannt | Boktor-Risiko, Schalllecks | Houtbouw Lente, A. Jansen, Circulaire Bouweconomie | genaue Bauteilpositionen |
| Betonplatten / Bestand | Beton | ehemaliges De-Patio-Gebäude / Grundstück | Boden-/Bestandsbauteil | weitergenutzt im Projekt | unbekannt | teilweise | nein | nein | nein | Erhalt / Strippen | bestehend | unbekannt | Tragfähigkeit, Gebrauchstauglichkeit | unbekannt | zählt nur als Bestandserhalt, wenn gleiche Funktion | Bouw en Uitvoering | Direct-Reuse-Anteil |
| Türen / Schiebetüren | Holz/Metall/Glas | Abbruch- und Renovierungsprojekte | Türen | Türen / Raumabschluss | unbekannt | nein | ja | nein | nein | Aufarbeitung, Anpassung | Beschläge unbekannt | unbekannt | Feuer-/Schall-/Nutzungssicherheit | unbekannt | Maße, Brandschutz | Circulaire Bouweconomie; Boschgaard | Herkunft je Tür |
| Küchenblöcke | gemischt | gesuchte / geerntete Bauteile | Küche | feste Einbauten | unbekannt | nein | ja | nein | technisch teils | Reinigung, Anpassung | unbekannt | unbekannt | Hygiene, Wasser/Elektro | unbekannt | technische Anschlüsse | Circulaire Bouweconomie | eingebauter Umfang |
| WC / Sanitär | Keramik/Metall | gesuchte / geerntete Bauteile | Sanitär | Sanitäranlagen | unbekannt | nein | nein | nein | ja | Reinigung, Anschlussanpassung | unbekannt | unbekannt | Hygiene, Dichtheit | unbekannt | Gewährleistung | Circulaire Bouweconomie | Umfang |
| Kabelgoten / Notbeleuchtung | Metall/Kunststoff/Elektro | gesuchte / geerntete Bauteile | technische Gebäudeelemente | Elektro-/Sicherheitsinstallation | unbekannt | nein | nein | nein | ja | unbekannt | unbekannt | unbekannt | Elektrosicherheit | unbekannt | Zulassung, Alter | Circulaire Bouweconomie | Einbau belegt? |
| Feste Ausstattung / Garderobe | Holz/Metall | geerntete Materialien | unbekannt | fester Innenausbau | unbekannt | nein | ja | nein | nein | unbekannt | unbekannt | unbekannt | Gebrauchstauglichkeit | unbekannt | Möbelgrenze beachten | Boschgaard | ob fest eingebaut |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | vorhandenes De-Patio-Gebäude und nutzbare Materialien prüfen | Superuse, Bewohner, Zayaz | Bestand/Materialpotenzial analysieren | unbekannt | kein Bulldozer; Strippen erwähnt | unbekannt | unbekannt | lokal | Bestandserhalt vs. Reuse trennen | Erhalt sinnvoller Teile | Bouw en Uitvoering |
| Bauteilinventar | „Boodschappenlijst“ und Materialsuche | Boschgaard, Superuse, Rückbaupartner | Harvesting / Oogsten | unbekannt | selektiver Rückbau bei Spendergebäuden | Sortieren, Lagern | unbekannt | Netzwerk von Abriss-/Renovierungsprojekten | Verfügbarkeit folgt fremden Zeitplänen | flexible Planung | Boschgaard; Circulaire Bouweconomie |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | öffentliche Angaben fehlen | unbekannt | unbekannt |
| Rückbau | Bauteile aus Bibliothek, Roosendaal-Fassade, weiteren Objekten sichern | Rückbauunternehmen, Projektteam | selektive Demontage | unbekannt | de-/rückbaubegleitend | unbekannt | unbekannt | Transporte nach Den Bosch / Lager | Timing mit Rückbauprojekten | frühe Sicherung und Lager | ED.nl; Boschgaard |
| Ausbau | Dachspanten, Fassadenelemente, Balken bergen | Rückbaupartner | Demontage statt Zerstörung | unbekannt | selektiv | unbekannt | unbekannt | Kran/Transport unbekannt | Größen/Maße | Entwurf folgt Bauteilen | Boschgaard |
| Transport | Bauteile aus Sint-Michielsgestel, Roosendaal, Haarlem etc. transportieren | unbekannt | LKW anzunehmen, aber nicht belegt | unbekannt | - | - | - | regional | Transportdistanz nicht bilanziert | unbekannt | Quellen nennen Herkunftsorte |
| Lagerung | Materialien in angemieteter Halle sammeln | Boschgaard | Zwischenlager / loods | unbekannt | - | Sortierung | unbekannt | Lagerhalle | zu wenig bezahlbarer Lagerraum | eigene Halle, Priorisierung | Boschgaard Circulariteit |
| Aufbereitung | gebrauchte Bauteile einbaufähig machen | Bauunternehmen, Superuse, Fachfirmen | Reinigen, Zuschneiden, ggf. Reparieren | unbekannt | - | unbekannt | unbekannt | Werkstatt unbekannt | Qualität/Gewährleistung | Fallweise Anpassung | Houtbouw Lente; Boschgaard |
| Planung | Gebäudegeometrie an Bauteile anpassen | Superuse | materialgetriebener Entwurf | unbekannt | - | - | unbekannt | Materialfunde beeinflussen Zeitplan | Welstand / genehmigte Dachform | Planungsanpassung | Boschgaard Dachspanten |
| Genehmigung | Bauantrag / Abgleich mit Anforderungen | Zayaz, Gemeinde, Planer | reguläre Genehmigung | unbekannt | - | - | unbekannt | - | Reuse-Bauteile in Nachweisführung | unbekannt | Boschgaard Dachspanten indirekt |
| Wiedereinbau | Spanten, Fassade, Hölzer, Ausbau einbauen | Versteegden, Bewohner, Fachfirmen | Wieder-/Neumontage | unbekannt | - | Montageanpassung | unbekannt | Baustelle Den Bosch | Schall, Bauphysik, Holzschutz | fachliche Begleitung | Houtbouw Lente |
| Monitoring | CO₂-/Materialanteile ausweisen | Superuse / Projektteam | Ökobilanz / Kennwertkommunikation | unbekannt | - | - | unbekannt | - | Methode nicht transparent | Kennwerte veröffentlichen | Superuse |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | neue Baukörper als HSB; wiederverwendete Holzspanten für Dachaufbau belegt | Tragfähigkeit, Gebrauchstauglichkeit | unbekannt | unbekannt | Geometrie, Holzalter, Holzschutz | Entwurf folgte den geernteten Spanten | Boschgaard; Houtbouw Lente |
| Lastabtragung | genaue Lastpfade unbekannt | statischer Nachweis | unbekannt | unbekannt | keine öffentlichen Details | unbekannt | unbekannt |
| Verbindung | Anschlüsse Spanten/Fassade unbekannt | Tragfähigkeit, Demontierbarkeit, Dichtheit | unbekannt | unbekannt | Altmaße vs. Neubau | unbekannt | unbekannt |
| Brandschutz | keine Details; bei Türen/Sanitärräumen relevant | Feuerwiderstand / Rettungswege | unbekannt | unbekannt | Nachweis gebrauchter Bauteile | unbekannt | unbekannt |
| Schallschutz | als Herausforderung genannt | Vermeidung von Schalllecks | unbekannt | unbekannt | Ausführung muss Entwurf exakt erfüllen | Qualitätssicherung nötig | Houtbouw Lente |
| Feuchte | Holz-/Fassaden-Reuse verlangt Feuchteschutz | Dauerhaftigkeit | unbekannt | unbekannt | alte Bauteile, neue Einbausituation | unbekannt | unbekannt |
| Wärmeschutz | hochwertige Dämmung / passive Maßnahmen genannt | Energieeffizienz | unbekannt | unbekannt | gebrauchte Fassadenteile und Dichtigkeit | Kombination mit neuer Dämmung | Superuse; Boschgaard |
| Wärmebrücken | besonders bei Aluminiumfassade relevant | vermeiden / minimieren | unbekannt | unbekannt | altes Fassadensystem | unbekannt | unbekannt |
| Luftdichtheit | keine Daten | Luftdichtheit Gebäudehülle | unbekannt | unbekannt | gebrauchte Fenster/Fassade | unbekannt | unbekannt |
| TGA-Integration | PV, Wärmepumpen, Erdwärmesonden, Regenwasser belegt | Energie/Haustechnik | unbekannt | unbekannt | Integration mit Reuse-Bau | unbekannt | Boschgaard |
| Barrierefreiheit | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |
| Dauerhaftigkeit | Holzschädlinge als Risiko | Holzschutz / Wartbarkeit | unbekannt | unbekannt | Boktor-Risiko | Prüfung/Behandlung nötig, aber nicht öffentlich belegt | Houtbouw Lente |
| Wartung | grüne Dächer/Fassaden und geerntete Bauteile | Instandhaltung | unbekannt | unbekannt | gemischte Bauteilalter | unbekannt | Boschgaard |
| Zulassung | keine Details | bauaufsichtliche Akzeptanz | unbekannt | unbekannt | Reuse-Bauteile ohne Standardproduktdaten | unbekannt | unbekannt |
| Haftung | keine Details | Gewährleistung | unbekannt | unbekannt | gebrauchte Bauteile | unbekannt | unbekannt |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Wohneinheiten | 19 | Einheiten | Projektangabe | Projekt | Superuse; Zayaz | belegt |
| Fertigstellung / Nutzung | Anfang 2024 | Jahr | Projektangabe | Projekt | Houtbouw Lente | belegt |
| Sekundäre Materialien | 84 | % | unbekannt | alle Materialien / Gebäude, laut Superuse | Superuse | teilweise belegt |
| Geerntete Materialien | ca. 85 | % | unbekannt | Gebäude, laut Houtbouw Lente/Boschgaard | Houtbouw Lente; Boschgaard | teilweise belegt |
| Zielwert Reuse | 90 | % | Ziel/Planung | Baumaterialien | Boschgaard | teilweise belegt |
| CO₂-Einsparung | 70 | % | unbekannt | Vergleich mit aktuellem Baustandard | Superuse; Boschgaard-Fassadenartikel | teilweise belegt |
| vermiedene Umweltschäden | 700.000 | € | unbekannt | „future environmental damage“ | Superuse | teilweise belegt |
| Anteil an Baukosten | 1/5 | Anteil | unbekannt | Vergleich zu Baukosten | Superuse | teilweise belegt |
| PV-Anlage | 234 | Module | Projektangabe | Betrieb / Energie | Boschgaard | belegt |
| Erdwärmesonden | 80 | m Länge | Projektangabe | TGA | Boschgaard | belegt |
| Regenwasserspeicher | bis 80 | m³ | Projektangabe | Betrieb Wasser | Boschgaard | belegt |
| wiederverwendete Dachspanten | 24 | Stück | Presseangabe | Bauteile aus Bibliothek | ED.nl | teilweise belegt |
| Fläche | unbekannt | m² | - | - | - | unklar |
| U-Wert | unbekannt | W/m²K | - | Bauteil | - | unklar |
| Transportdistanz | unbekannt | km | - | Bauteiltransport | - | unklar |
| Baukosten | unbekannt | € | - | Projekt | - | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Materialverfügbarkeit nicht synchron zur Bauplanung | logistisch | Bauteile werden frei, wenn Spendergebäude rückgebaut werden | Entwurf und Terminplan müssen flexibel sein | Bauteil, Logistik, Reuse-Strategie | frühe Suche, Lagerung, flexible Planung | Reuse braucht Beschaffung vor Detailplanung | Boschgaard Circulariteit |
| Lagerkapazität | logistisch/wirtschaftlich | viele Bauteile müssen zwischengelagert werden | Annahme guter Angebote wird begrenzt | Logistik, Wirtschaft | angemietete Halle; Priorisierung | Materiallager ist zentrale Infrastruktur | Boschgaard Circulariteit |
| Bauphysik / Schall | technisch | HSB und gebrauchte Bauteile verlangen präzise Ausführung | Risiko von Schalllecks | Leistungsanforderung, Prüfung | sorgfältige Planung/Ausführung | Reuse ist auch Qualitätssicherungsproblem | Houtbouw Lente |
| Holzschädlinge | technisch | wiederverwendetes Holz kann Vorschäden haben | Risiko für Dauerhaftigkeit | Schadstoff/Schädling, Bauteil | Prüfung/Behandlung nötig; Details unbekannt | Holzreuse benötigt Prüfpfad | Houtbouw Lente |
| Genehmigte Form vs. gefundene Bauteile | gestalterisch/rechtlich | Dachform war bereits mit Gremien abgestimmt | gefundene Spanten mussten geometrisch passen | Bauteil, Recht, Planung | Entwurfsabgleich mit Spanten | Reuse-Funde können Entwurf nicht beliebig ändern | Boschgaard Dachspanten |
| Gewährleistung und Produktdaten | rechtlich/technisch | gebrauchte Bauteile haben unvollständige Dokumentation | Unsicherheit für Planer/Ausführung | Recht, Prüfung, Wirtschaft | unbekannt | Dokumentation muss früh aufgebaut werden | abgeleitet aus Datenlücken |
| Budget sozialer Wohnungsbau | wirtschaftlich | begrenzte Kosten | Bedarf an Eigenleistung und günstiger Beschaffung | Wirtschaft, People | Bewohnerarbeit, Materialernte | Sozialer Reuse-Bau braucht kollaborative Modelle | Superuse; Zayaz |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** projektbezogene Materialernte aus Rückbau- und Renovierungsprojekten; Netzwerkbeschaffung; Bewohnerbeteiligung; teilweise Materiallager.
- **Bauteilbörse / Quelle:** keine klassische Bauteilbörse belegt; Quellen u. a. Bibliothek Sint-Michielsgestel, Stadskantoor Roosendaal, alte Schule Boschveld, altes verzorgingshuis Zuiderschans, Tankstelle Haarlem, Kunstakademie.
- **Kostenwirkung:** Superuse nennt 700.000 € vermiedene zukünftige Umweltschäden bzw. 1/5 der Baukosten; keine vollständigen Projektkosten öffentlich belegt.
- **Zeitwirkung:** Materialsuche und Lagerung erhöhen Koordinationsaufwand; genaue Bauzeit unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch; Bewohner ernten Materialien, bauen mit und begleiten Entwicklung.
- **Lagerung:** stark relevant; Boschgaard beschreibt angemietete Halle als fast voll und Lagerraum als Engpass.
- **Marktbarrieren:** Materialdaten fehlen, Timing der Rückbauprojekte, begrenzte Lagerflächen, technische Nachweise, Akzeptanz bei regulären Bauprozessen.

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** hoch; Materialgeschichten wie Dachspanten und Fassade werden kommunikativ hervorgehoben.
- **räumliche Transformation:** ehemaliges Nachbarschaftszentrum wird Teil eines neuen kollektiven Wohnmodells.
- **Atmosphäre / Ausdruck:** gemeinschaftlich, materialbasiert, ökologisch; genaue Innenraumwirkung quellenabhängig.
- **Umgang mit Spuren:** Wiederverwendung wird als Identität des Projekts gezeigt; genaue konservatorische Strategie unbekannt.
- **sozialer Wert:** sehr hoch; soziale Miete, Bewohner-Selbstorganisation, Nachbarschaftszentrum und Stadtacker.
- **Denkmal- oder Bestandswert:** kein Denkmalstatus belegt; Bestandswert als soziale und materielle Ressource.
- **Kritik / Grenzen:** viele Kennwerte nicht methodisch offen; Anteil direkter Bauteilwiederverwendung ist nicht für jedes Element isolierbar; Bestandserhalt darf nicht als Direct Reuse überbewertet werden.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Norm, Recht, Prüfung, Schadstoff, Software, detailliertes Tragwerkssystem, Verbindung, genaue Abbruchmethode.
- **Welche neuen Entitäten wären sinnvoll?** Oogstmaterial, Bewohner-Selbstbau, Materiallager, Materialgeschichte.
- **Welche Daten fehlen?** genaue BGF, Bauteilmengen je Kategorie, Prüfberichte der Holzspanten, Details der Aluminiumfassade, Transportdistanzen, vollständige LCA-Methode, Baukosten.
- **Welche Quellen müssten geprüft werden?** Bauantrag, Statik, Materialpass, Rückbau-/Prüfprotokolle, Kostendokumentation, LCA-Bericht, Detailpläne der Fassade und Dachspanten.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** Anhang / Vergleichsfall in der Hauptliste mittlerer Priorität
- **5 wichtigste Fakten:**
  1. 19 soziale Wohneinheiten plus Nachbarschaftszentrum in Den Bosch.
  2. 84–85 % sekundäre/geerntete Materialien werden von Projektquellen genannt.
  3. Wiederverwendete Holz-Dachspanten aus Sint-Michielsgestel prägen Dachform und Trag-/Raumlogik.
  4. Eine ca. 50 Jahre alte Aluminiumfassade aus dem Stadskantoor Roosendaal wurde im Projekt weiterverwendet.
  5. Lagerung und Timing von Rückbauquellen waren zentrale Prozesshürden.
- **5 wichtigste Bauteile:** Dachspanten, Aluminiumfassade, HSB-Holz/Balken, Türen/Innenausbau, Sanitär-/Küchenelemente.
- **5 wichtigste Hürden:** Lagerraum, Materialtiming, Bauphysik/Schall, Holzschädlinge, Nachweis/Gewährleistung.
- **5 wichtigste übertragbare Erkenntnisse:** Reuse braucht frühes Harvesting; Lager sind Infrastruktur; Entwurf muss Materialien folgen; Bewohnerbeteiligung kann Kostenrahmen stützen; Kennwerte müssen Direct Reuse von Bestandserhalt trennen.
- **5 offene Fragen:** Welche Bauteile sind wirklich tragend? Welche Prüfungen wurden durchgeführt? Welche Transportemissionen entstanden? Wie wurde die Fassade bauphysikalisch ertüchtigt? Wie setzen sich 84/85/90 % Materialanteile methodisch zusammen?

## Quellen / Links

- Superuse Studios — Housing Cooperative Boschgaard: https://www.superuse-studios.com/projectplus/woongroep-boschgaard/
- Boschgaard — Duurzaam bouwen: https://boschgaard.nl/duurzaam-bouwen/
- Boschgaard — Circulariteit / Lagerung: https://boschgaard.nl/circulariteit/
- Boschgaard — Dachspanten: https://boschgaard.nl/het-verhaal-van-onze-dakspanten/
- Boschgaard — Aluminiumgevel: https://boschgaard.nl/slim-ontwerp-is-sleutel-voor-succesvol-hergebruik-aluminium-gevel/
- Houtbouw Lente — Woongroep Boschgaard: https://houtbouwlente.nl/project/boschgaard/
- Zayaz — Boschgaard: https://www.zayaz.nl/boschgaard
- Circulaire Bouweconomie — Materialsuche Boschgaard: https://circulairebouweconomie.nl/nieuws/duurzaam-woonproject-boschgaard-zoekt-bouwmaterialen/
- ED.nl — Spanten Brenthof Gestel bekommen zweites Leben: https://www.ed.nl/boxtel/spanten-brenthof-gestel-krijgen-tweede-leven-in-den-bosch~ad6e7896/
- Duurzame Metaalbouw — Aluminium-Fassade: https://duurzamemetaalbouw.nl/nieuws/van-stadskantoor-naar-sociale-woningbouw-tweede-leven-voor-jaren-70-gevel/
