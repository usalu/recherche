# Abschlussbericht: Faktencheck der LaTeX-Graphkanten

Stand: 2026-08-13

## Konkretes Ergebnis

Alle **570 von 570** Kandidaten wurden einzeln entschieden. Es gibt keine offene Entscheidung.
Der LaTeX-Graph verwendet jetzt eine strikte Positivliste: **477 belegt und behalten**,
**93 entfernt**. Von den 93 Entfernungen sind **68 bloße Verzeichniseinträge** und
**25 Fälle ohne Beleg für eine Beziehung**.

Im LaTeX-Netzmodell sind exakt 477 Kanten. Das erzeugte Fragment zeichnet 455;
die übrigen 22 belegten Kanten liegen in Zweierkomponenten und werden durch die
bestehende Regel ‚nur zusammenhängende Cluster ab drei Knoten‘ nicht sichtbar ausgegeben.
Sie sind nicht gelöscht.

Es wurden keine Daten nach Neo4j geschrieben.

## Ergebnis nach Land

| Land | geprüft | behalten | entfernt |
|---|---:|---:|---:|
| AT | 30 | 27 | 3 |
| BE | 86 | 58 | 28 |
| CH | 46 | 44 | 2 |
| DE | 49 | 36 | 13 |
| DK | 42 | 26 | 16 |
| FI | 40 | 38 | 2 |
| FR | 44 | 36 | 8 |
| GB | 95 | 84 | 11 |
| NL | 78 | 77 | 1 |
| NO | 27 | 19 | 8 |
| SE | 33 | 32 | 1 |

## Behaltene Beziehungsarten

| Beziehungsart | Anzahl |
|---|---:|
| Aufarbeitung | 7 |
| Bauausführung | 47 |
| Bauherrschaft | 49 |
| Bauteilinventarisierung | 3 |
| Bauteillieferung | 24 |
| Betreiberschaft | 8 |
| Betrieb | 13 |
| Dienstleistungsbeziehung | 13 |
| Entwurf | 53 |
| Fachplanung | 63 |
| Forschungsbegleitung | 8 |
| Förderung | 4 |
| Gemeinsames Bauvorhaben | 9 |
| Gründung | 19 |
| Konsortialpartner | 74 |
| Konzernbindung | 7 |
| Kooperationsvereinbarung | 11 |
| Lieferbeziehung | 4 |
| Logistik | 1 |
| Mitgliedschaft | 5 |
| Projektbeteiligung, Aufgabe unklar | 11 |
| Prüfung und Nachweis | 8 |
| Reuse-Konzept | 8 |
| Rückbau | 13 |
| Trägerschaft | 8 |
| Zusammenarbeit, Art unklar | 7 |

## Deutschland: alle 49 Entscheidungen

| ID | Knoten A | Knoten B | Entscheidung | Beziehungsart/Grund | Konkreter Befund | Beleg |
|---|---|---|---|---|---|---|
| DE:K001 | Abfallwirtschaftsbetriebe Münster | AWM Münster – zirkulärer… | BEHALTEN | Bauherrschaft | Der Akteur verantwortete das Vorhaben als Bauherr. | [Quelle](https://awm.stadt-muenster.de/aktuelles/newsdetail/moderne-arbeitswelt-aus-gebrauchten-materialien) |
| DE:K002 | Berlin-Schildow Pilot | Claus Asam | BEHALTEN | Prüfung und Nachweis | Der Akteur prüfte oder zertifizierte Bauteile. | [Quelle](https://taz.de/Die-Wiedergeburt-der-Platte/!493469/) |
| DE:K003 | Berlin-Schildow Pilot | IEMB / TU Berlin | BEHALTEN | Prüfung und Nachweis | Der Akteur prüfte oder zertifizierte Bauteile. | [Quelle](https://taz.de/Die-Wiedergeburt-der-Platte/!493469/) |
| DE:K004 | Berlin-Schildow Pilot | Architekturbüro Conclus | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://taz.de/Die-Wiedergeburt-der-Platte/!493469/) |
| DE:K005 | Claus Asam | Mehrow Pilot House | BEHALTEN | Projektbeteiligung, Aufgabe unklar | Die Quelle belegt die Beteiligung, aber keine genaue Aufgabe. | [Quelle](https://www.baulinks.de/webplugin/2005/1177.php4) |
| DE:K006 | IEMB / TU Berlin | Plattenpalast Berlin | BEHALTEN | Forschungsbegleitung | Der Akteur begleitete das Vorhaben wissenschaftlich. | [Quelle](https://wwstudio.de/projects/plattenpalst) |
| DE:K007 | CRCLR House | Solares Bauen | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://www.dbz.de/artikel/crclr-house-berlin-3945221.html) |
| DE:K008 | CRCLR House | eZeit | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://www.dbz.de/artikel/crclr-house-berlin-3945221.html) |
| DE:K009 | CRCLR House | LXSY Architektur | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://lxsy.de/projekte/impact-hub-berlin-at-crclr-house) |
| DE:K010 | ZRS Ingenieure | Impact Hub Berlin | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://www.zrs.berlin/en/project/crclr-house-2/) |
| DE:K011 | Haus HOS | Seidl + Seidl Architekten | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.seidlarchitekten.de/haus-hos-muehlhausen/) |
| DE:K012 | Impact Hub Berlin | Impact Hub Berlin | BEHALTEN | Betrieb | Der Akteur betrieb das Vorhaben oder die Einrichtung. | [Quelle](https://www.buildingsocialecology.org/projects/crclr-house-berlin/) |
| DE:K013 | Impact Hub Berlin | TRNSFRM eG | BEHALTEN | Betrieb | Der Akteur betrieb das Vorhaben oder die Einrichtung. | [Quelle](https://www.dbz.de/artikel/crclr-house-berlin-3945221.html) |
| DE:K014 | Impact Hub Berlin | Die Zusammenarbeiter | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://www.dbz.de/artikel/crclr-house-berlin-3945221.html) |
| DE:K015 | Impact Hub Berlin | LXSY Architektur | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://lxsy.de/projekte/impact-hub-berlin-at-crclr-house) |
| DE:K016 | Plattenpalast Berlin | Wiewiorra Hopp Architekten | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://wwstudio.de/projects/plattenpalst) |
| DE:K017 | Plattenvereinigung Berlin | zukunftsgeraeusche GbR | BEHALTEN | Betrieb | Der Akteur betrieb das Vorhaben oder die Einrichtung. | [Quelle](https://www.plattenvereinigung.de/imprint/) |
| DE:K018 | Plattenvereinigung Berlin | TU Berlin Fachgebiet Bauphysik und Baukonstruktionen | BEHALTEN | Forschungsbegleitung | Der Akteur begleitete das Vorhaben wissenschaftlich. | [Quelle](https://www.tu.berlin/en/bauphysik/research/past-projects/projekt-plattenvereinigung) |
| DE:K019 | Plattenvereinigung Berlin | Deutsche Bundesstiftung Umwelt (DBU) | BEHALTEN | Förderung | Der Akteur finanzierte oder förderte das Vorhaben. | [Quelle](https://www.plattenvereinigung.de/project/) |
| DE:K020 | Plattenvereinigung Berlin | Bundeszentrale für politische Bildung (bpb) | BEHALTEN | Förderung | Der Akteur finanzierte oder förderte das Vorhaben. | [Quelle](https://www.plattenvereinigung.de/project/) |
| DE:K021 | Recyclinghaus Hannover | Gundlach GmbH & Co. KG Wohnungsunternehmen | BEHALTEN | Bauherrschaft | Der Akteur verantwortete das Vorhaben als Bauherr. | [Quelle](https://www.aknds.de/architektur-baukultur/staatspreis-2020/engere-wahl-2020/recyclinghaus-hannover-kronsberg-hannover) |
| DE:K022 | Recyclinghaus Hannover | DREWES + SPETH Beratende Ingenieure | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://www.aknds.de/architektur-baukultur/staatspreis-2020/engere-wahl-2020/recyclinghaus-hannover-kronsberg-hannover) |
| DE:K023 | Recyclinghaus Hannover | H2A | BEHALTEN | Fachplanung | Der Akteur übernahm eine benannte Fachplanung. | [Quelle](https://www.aknds.de/architektur-baukultur/staatspreis-2020/engere-wahl-2020/recyclinghaus-hannover-kronsberg-hannover) |
| DE:K024 | Recyclinghaus Hannover | CITYFÖRSTER | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://www.aknds.de/architektur-baukultur/staatspreis-2020/engere-wahl-2020/recyclinghaus-hannover-kronsberg-hannover) |
| DE:K025 | Jugendtreff Ingersheim | Gemeinde Ingersheim | BEHALTEN | Bauherrschaft | Die Gemeinde Ingersheim war Bauherrin des Jugendtreffs. | [Quelle](https://klingelhoefer-kroetsch.de/projekte/jugendtreff-ingersheim/) |
| DE:K026 | AWM Münster – zirkulärer… | Urselmann Interior | BEHALTEN | Bauausführung | Der Akteur führte benannte Bauleistungen aus. | [Quelle](https://awm.stadt-muenster.de/aktuelles/newsdetail/moderne-arbeitswelt-aus-gebrauchten-materialien) |
| DE:K027 | AWM Münster – zirkulärer… | Petra Jablonická | BEHALTEN | Entwurf | Der Akteur übernahm den architektonischen Entwurf. | [Quelle](https://www.jablonicka.com/work/95,6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-) |
| DE:K028 | AWM Münster – zirkulärer… | Sven Urselmann | BEHALTEN | Bauausführung | Der Akteur führte benannte Bauleistungen aus. | [Quelle](https://www.jablonicka.com/work/95,6%25-circular-reconstruction-of-offices-for-awm-m%C3%BCnster-) |
| DE:K029 | AWM Münster – zirkulärer… | Concular | BEHALTEN | Reuse-Konzept | Der Akteur entwickelte das Wiederverwendungskonzept. | [Quelle](https://concular.de/bueroetage-muenster/) |
| DE:K030 | BTU Cottbus | ReCreate project consortium | BEHALTEN | Konsortialpartner | Beide sind als Partner desselben Konsortiums belegt. | [Quelle](https://recreate-project.eu/the-partners/) |
| DE:K031 | Circular Structural Design | Concular | BEHALTEN | Konsortialpartner | Beide sind als Partner desselben Konsortiums belegt. | [Quelle](https://www.green-ai-hub.de/en/pilot-projects/pilotproject-concular) |
| DE:K032 | KIT | Urban Mining Index | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://urban-mining-index.de/initiative/) |
| DE:K033 | KIT | Baukreisel e.V. | BEHALTEN | Kooperationsvereinbarung | Die Quelle belegt eine formalisierte Zusammenarbeit. | [Quelle](https://nb.ieb.kit.edu/index.php/ausbau-stegreif-konrad-kocher-schule-kitzingen/) |
| DE:K034 | Urban Mining Index | Universität Wuppertal | BEHALTEN | Trägerschaft | Die Quelle belegt institutionelle Trägerschaft oder Finanzierung. | [Quelle](https://urban-mining-index.de/initiative/) |
| DE:K035 | Concular | ALBA Berlin | BEHALTEN | Kooperationsvereinbarung | Die Quelle belegt eine formalisierte Zusammenarbeit. | [Quelle](https://www.alba.info/unternehmen/newsroom/pressemitteilungen/detail/urban-mining-hub-berlin-gekommen-um-zu-bleiben/) |
| DE:K036 | Concular | München Bauteilbörse (CirCoFin pilot) | BEHALTEN | Betreiberschaft | Die Quelle belegt, wer die Einrichtung betreibt. | [Quelle](https://concular.de/regionale-knotenpunkte-fuer-ganz-deutschland/) |
| DE:K037 | Bauteilbörse Bremen | bauteilnetz Deutschland | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K038 | bauteilnetz Deutschland | bauteilbörse augsburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K039 | bauteilnetz Deutschland | Bauteilbörse Berlin-Brandenburg (Fläming Antik / Brita Marx) | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K040 | bauteilnetz Deutschland | bauteilbörse giessen | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K041 | bauteilnetz Deutschland | bauteilbörse herzogenrath | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K042 | bauteilnetz Deutschland | bauteilbörse köln | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K043 | bauteilnetz Deutschland | bauteilbörse nordhausen | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K044 | bauteilnetz Deutschland | bauteilbörse oldenburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K045 | bauteilnetz Deutschland | bauteilbörse weißenburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K046 | bauteilnetz Deutschland | gabb-GebrauchtBauMarkt Saarbrücken | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K047 | bauteilnetz Deutschland | Bauteilbörse Bremerhaven (Förderwerk Bremerhaven) | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K048 | Historische Bauelemente (Marwitz) | Unternehmerverband Historische Baustoffe e.V. (UHB) | BEHALTEN | Konsortialpartner | Beide sind als Partner desselben Konsortiums belegt. | [Quelle](https://www.historische-baustoffe.de/en/the-dealers/list-of-dealers/elias/) |
| DE:K049 | Historische Baustoffe Ostalb (Söhnstetten) | Unternehmerverband Historische Baustoffe e.V. (UHB) | BEHALTEN | Konsortialpartner | Beide sind als Partner desselben Konsortiums belegt. | [Quelle](https://www.historische-baustoffe.de/en/the-dealers/list-of-dealers/hbostalb/) |

## Vollständige Entfernungsliste: alle 93 Kanten

Diese Liste beantwortet konkret, was gelöscht wurde. ‚Kein Beleg‘ ist hier eine
abschließende DELETE-Entscheidung, keine noch wartende Prüfung.

| ID | Knoten A | Knoten B | Entscheidung | Entfernungsgrund | Konkreter Befund | Beleg |
|---|---|---|---|---|---|---|
| AT:K007 | Wiener Aufzugmus. | BauKarussell | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.baukarussell.at/vom-luster-bis-zum-kupferkabel/) |
| AT:K016 | BauKarussell | Drees & Sommer (Österreich) | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| AT:K030 | Drees & Sommer (Österreich) | Madaster Austria GmbH | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://madaster.at/neuigkeiten/1625/) |
| BE:K004 | Chiro d’Itterbeek | Rotor | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://rotordb.org/en/projects/sanitary-block-itterbeek-chiro) |
| BE:K014 | Maison Vignette | RotorDC | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| BE:K047 | Opalis | Antique Fireplaces First | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K048 | Opalis | Authentieke Bouwmaterialen Storms nv | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K049 | Opalis | Bois Antique | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K050 | Opalis | De Oude Dakpan | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K051 | Opalis | Eeuwenhout Antoine Verhofstede | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K052 | Opalis | Gunter Bosmans | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K053 | Opalis | Het arduinen hoekje | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K054 | Opalis | Heyns Recycling | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K055 | Opalis | Hofman NV - SA | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K056 | Opalis | Jef Stone | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K057 | Opalis | Joris Van Apers | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K058 | Opalis | Kasseien Kindt | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K059 | Opalis | Kempische Bouwmaterialen | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K060 | Opalis | Labeur Atelier - Labeur | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K061 | Opalis | MVV Afbraakwerken Martin | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K062 | Opalis | Stadshout.be | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K063 | Opalis | Van Dijck | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K064 | Opalis | Van Huele | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K065 | Opalis | Antiek Anresto | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K066 | Opalis | Composil | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K067 | Opalis | De Groene Poort | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K068 | Opalis | Doehetzelf 2dehands bouwmarkt | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K069 | Opalis | Fryns-Boret | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K070 | Opalis | Houtenplaten | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K071 | Opalis | Recupan bvba | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://opalis.eu/en) |
| BE:K083 | CCRI Pilot Flanders | TWG Circular Construction and Buildings (CCRI) | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| CH:K010 | baubüro in situ | Zirkular | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| CH:K014 | Grubenstrasse 29 | Bauteilladen Winterthur | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| DE:K011 | Haus HOS | Seidl + Seidl Architekten | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.seidlarchitekten.de/haus-hos-muehlhausen/) |
| DE:K032 | KIT | Urban Mining Index | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://urban-mining-index.de/initiative/) |
| DE:K037 | Bauteilbörse Bremen | bauteilnetz Deutschland | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K038 | bauteilnetz Deutschland | bauteilbörse augsburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K039 | bauteilnetz Deutschland | Bauteilbörse Berlin-Brandenburg (Fläming Antik / Brita Marx) | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K040 | bauteilnetz Deutschland | bauteilbörse giessen | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K041 | bauteilnetz Deutschland | bauteilbörse herzogenrath | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K042 | bauteilnetz Deutschland | bauteilbörse köln | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K043 | bauteilnetz Deutschland | bauteilbörse nordhausen | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K044 | bauteilnetz Deutschland | bauteilbörse oldenburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K045 | bauteilnetz Deutschland | bauteilbörse weißenburg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K046 | bauteilnetz Deutschland | gabb-GebrauchtBauMarkt Saarbrücken | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DE:K047 | bauteilnetz Deutschland | Bauteilbörse Bremerhaven (Förderwerk Bremerhaven) | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://network.bellona.org/content/uploads/sites/5/2025/10/Bauteilnetz-Deutschland.pdf) |
| DK:K007 | Svanen | Aksel V. Jensen A/S | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.avj.dk/) |
| DK:K026 | Bærebyg | Bolius genbrugsmaterialer directory | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K027 | Bango A/S | Bolius genbrugsmaterialer directory | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K028 | Dem fra Nordlunde | Bolius genbrugsmaterialer directory | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K029 | Den Grønne Genbrugshal | Bolius genbrugsmaterialer directory | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K032 | Bolius genbrugsmaterialer directory | J. Jensen A/S | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K033 | Bolius genbrugsmaterialer directory | jk-genbrug | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K034 | Bolius genbrugsmaterialer directory | KC Nedbrydning A/S | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K035 | Bolius genbrugsmaterialer directory | Klassiske Vinduer | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K036 | Bolius genbrugsmaterialer directory | Nedrivningsselskabet Falster | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K037 | Bolius genbrugsmaterialer directory | PlusByg | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K038 | Bolius genbrugsmaterialer directory | Råt&Godt | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K039 | Bolius genbrugsmaterialer directory | Røde Kors Byggegenbrug | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K040 | Bolius genbrugsmaterialer directory | Sanderum-Otterup Murerforretning | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K041 | Bolius genbrugsmaterialer directory | Skave Nedbrydning | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| DK:K042 | Bolius genbrugsmaterialer directory | Sydhavn Genbrugscenter | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.bolius.dk/her-kan-du-koebe-genbrugsmaterialer-10121) |
| FI:K006 | Härmälänranta | Tampere University | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| FI:K037 | Joensuun Rakennuspurku ja Timanttiurakointi Oy | Sitowise | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| FR:K001 | Bâticycle | Skop Marketplace | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://marketplace.skop.app/) |
| FR:K002 | Cycle Up | Institut National de l'Économie Circulaire (INEC) | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://institut-economie-circulaire.fr/evenement-construction-circulaire-paris/) |
| FR:K003 | Cycle Up | MAISON CARRELLE | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://site.cycle-up.fr/maison-carrelle/) |
| FR:K004 | Cycle Up | METAMO | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://site.cycle-up.fr/annonceurs-partenaires/) |
| FR:K005 | Cycle Up | MOBIOUS | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://site.cycle-up.fr/annonceurs-partenaires/) |
| FR:K007 | Cycle Up | PROCLUS | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://site.cycle-up.fr/annonceurs-partenaires/) |
| FR:K009 | RAEDIFICARE | CSTB | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://raedificare.com/amo/) |
| FR:K043 | Vilogia | CD2E | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://cd2e.com/actualites/un-nouveau-tournant-pour-les-acteurs-du-reemploi-en-hauts-de-france/) |
| GB:K005 | Material Reuse Portal | Warp It | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://materialreuseportal.com/) |
| GB:K006 | Material Reuse Portal | Grosvenor | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://materialreuseportal.com/) |
| GB:K007 | SalvoWEB | Arc Reclamation Ltd | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K008 | SalvoWEB | Frome Reclamation Ltd | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K009 | SalvoWEB | London Reclamation and Salvage Ltd | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K010 | SalvoWEB | Milton Keynes Antiques & Architectural Salvage | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K011 | SalvoWEB | Reclaimed World | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K012 | SalvoWEB | Stax Reclamation | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K013 | SalvoWEB | CS Architectural Salvage | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K014 | SalvoWEB | Wells Reclamation | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| GB:K015 | SalvoWEB | Wilsons Yard | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://www.salvoweb.com/salvo-directory) |
| NL:K008 | Lagemaat Heerde | Ter Velde & Den Besten | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.aannemervak.nl/bouwpraktijk/bouwtrends/circulaire-aanpak-bewijst-kracht-80-materialen-krijgt-tweede-leven/) |
| NO:K009 | Asplan Viak | Ombruk i nord (Remiks) | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.klimapartnere.no/ombruk-i-nord-samarbeid-om-gjenbruk-av-materialer/) |
| NO:K014 | Bodø Kommune | Iris Ombrukssentral / Saltnes ombruk | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| NO:K017 | NTNU | Bevar / Urban Reuse (NG Group) | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| NO:K022 | Donorbygg | Sirken | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | — |
| NO:K023 | byggogbevar directory | Ombruk i nord (Remiks) | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://byggogbevar.no/ressurser/) |
| NO:K024 | byggogbevar directory | OMBYGG | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://byggogbevar.no/ressurser/) |
| NO:K025 | byggogbevar directory | Sirkulær Ressurssentral | ENTFERNT | Verzeichniseintrag | Die Kante beruht nur auf einer Verzeichnislistung. | [Quelle](https://byggogbevar.no/ressurser/) |
| NO:K026 | JCS AS | Materialbanken for bygningsvern | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.jcs-as.no/materialbank) |
| SE:K010 | Business Region Göteborg | Handslag för cirkulärt byggande | ENTFERNT | Kein Beleg für eine Beziehung | Keine Quelle nennt beide Knoten in einer beschriebenen Verbindung. | [Quelle](https://www.businessregiongoteborg.se/naringslivsutveckling/hallbar-utveckling/goteborgs-plattform-klimatneutralt-byggande/handslag-cirkulart-byggande) |

## Offene Punkte

**Keine offenen Kantenentscheidungen.** Die 25 erfolglos recherchierten Kandidaten sind
bewusst entfernt. Eine spätere Wiederaufnahme ist nur mit einer zugänglichen Quelle möglich,
die beide Endpunkte nennt und genau ihre Beziehung beschreibt.
