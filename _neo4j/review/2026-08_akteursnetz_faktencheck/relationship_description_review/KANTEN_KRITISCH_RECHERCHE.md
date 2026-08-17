# Nachrecherche zu den 23 kritischen Kanten

Für jeden der 23 Fälle wurde im Web nachgesehen, ob es mehr gibt als die eine
gespeicherte Quelle. Ergebnis: **17 von 23 Akteuren haben nachweislich mehr
Bezug zum Reuse-Feld**, als die eine Kante zeigt — nur bei einem Teil davon
lässt sich das aber als *weitere Kante im aktuellen Netz* fassen (der andere
Endpunkt muss selbst ein Knoten sein). Alles unten ist Rechercheergebnis,
nichts ist angewendet.

---

## Echter Datenfehler, nicht nur eine dünne Kante (2)

**Franck / Franck Bricks — dieselbe Firma, zweimal als Knoten.**
Geprüft: `BE:U04 "Franck"` und `BE:U05 "Franck Bricks"` sind zwei separate
Knoten in den aktuellen Daten. Die Opalis-Händlerseite zeigt: eine Familienfirma
(Jan und Louise Franck, Klein Boom 4, 2580 Putte, USt-ID BE 0443 991 269,
franck.be), mit **drei** dokumentierten Reuse-Projekten: Chiro d'Itterbeek,
Maison Vignette und „Project Violet" in Antwerpen (geborgene Feldbrand-Ziegel).
Das ist kein dünner Fall — es ist ein Knoten, der versehentlich in zwei
gesplittet wurde, jeder mit nur einer der beiden Kanten. Zusammengeführt hätte
der Knoten drei Kanten, nicht eine. → **das ist eine Knotenzusammenführung,
keine Text- oder Löschentscheidung** — separat zu behandeln, nicht im
laufenden Textumbau.

**ABN AMRO → Victory Group ist keine Reuse-Beziehung, sondern ein Immobilienverkauf.**
Der Zuidas-Hauptsitz-Deal (2020/21) war ein reiner Sale-and-Leaseback, ohne
Zirkularitätsbezug. Victory Groups echte Reuse-Referenz ist ein anderes
Gebäude: **Circl**, der ABN-AMRO-Pavillon (80 % Materialwiederverwendung, über
das Joint Venture lCP Circulair = Cepezedprojects + Lagemaat). Circl ist
bereits ein Knoten im Netz (`P3`), mit einer bestehenden Kante
`ABN AMRO → Circl (Betrieb)`. → Vorschlag: die Kante `ABN AMRO — Victory Group`
umtypen oder entfernen (kein Reuse-Bezug), stattdessen `Victory Group → Circl`
neu aufnehmen, sofern belegbar.

**Four Bay Structures — falsches Zielgebäude.**
Die Quelle beschreibt tatsächlich **Tower Bridge Court**, nicht „House of
Fraser" — letzteres war das Abbruchgebäude, aus dem der Stahl geborgen wurde,
nicht der Empfänger. Zusätzlich: die Firma ist seit August 2024 insolvent, und
es fand sich kein weiteres Reuse-Projekt. → Vorschlag: Zielknoten korrigieren
auf Tower Bridge Court; als Reuse-Kante bleibt sie dünn, aber jetzt wenigstens
richtig zugeordnet.

---

## Nachweislich mehr Bezug — Ergänzungskanten möglich (7, sofern die Gegenseite ein Knoten ist)

Geprüft, welche der recherchierten Partner **bereits** Knoten im Netz sind:

| Akteur | gefundene weitere Bezüge | bereits Knoten? |
|---|---|---|
| DBU (Förderung Plattenvereinigung) | förderte auch **bauteilnetz Deutschland** (2006–2015) | **ja** — `DE:N02`, hat schon 11 Kanten (alle „Verzeichniseintrag") |
| Dusseldorp (Lieferung SUPERLOCAL) | Mitgründer von **Insert**, zirkulärer Rückbau bei Erasmus MC, Borne, Vroondaal | **ja** — `NL:M10 „Insert Marketplace"`, dort aktuell **null** Kanten |
| a:gain (Lieferung Upcycle Studios) | 64 benannte Projekte, Partnerschaft mit **DOVISTA/KRONE** und VELUX am Produkt „Viddø" | DOVISTA/KRONE ist derselbe kritische Fall nebenan — beide stützen sich gegenseitig |
| DOVISTA/KRONE (Lieferung TRÆ) | gemeinsame Produktentwicklung mit VELUX und a:gain, ausgeliefert auch an Nest House, Skovhuset | teilweise — a:gain ja, VELUX/Nest House/Skovhuset zu prüfen |
| Rijkswaterstaat (Lieferung Ithaka) | Konsortium für einen zirkulären Viadukt mit **Madaster**, Strukton, Antea Group | zu prüfen |
| Réavie (Lieferung Résilience) | Partnerschaft mit der Fondation Eiffage zum Bauabfall-Recycling | zu prüfen |
| Lindner SE (Lieferung UMAR) | dokumentiertes Referenzprojekt mit **Schaeffler**-Doppelbodenplatten, Madaster-Anbindung | zu prüfen |

→ Diese sieben sind die eigentliche Antwort auf die Ausgangsfrage: **nicht
löschen**, sondern ihnen fehlt schlicht eine zweite Kante, die die Recherche
jetzt beigebracht hat.

## Bestätigt: großer, aktiver Akteur — die eine Kante ist nur die Spitze (5)

Diese vier/fünf sind selbst keine neuen Kanten, aber die Recherche zeigt klar:
das sind keine Nebenfiguren, sondern zentrale Akteure des Feldes, bei denen
im Netz bislang nur ein einziger Treffer erfasst wurde.

- **ERDF/FEDER Brüssel** — over €195 Mio. in zirkuläre Projekte in Brüssel
  investiert, dokumentiert bei mehreren weiteren Reuse-Vorhaben (BBSM,
  Woodpark, ReUse Park).
- **Embuild → Buildwise** — mehrjährige, institutionelle Partnerschaft
  (Charter Biocirculair Bouwen, „Build Circular" mit 650+ Firmen), keine
  einmalige Sache.
- **OVAM → Tracimat** — OVAM ist die flämische Aufsichtsbehörde, die die
  gesamte Abbruch-Nachverfolgung in Flandern reguliert; entwickelt zusätzlich
  mit Bureau Bouwtechniek den „Bouwwerkpaspoort".
- **National Lottery Heritage Fund** — fördert auch Birnbeck Pier
  (Holzbergung durch Somerset Wood Recycling), also ein wiederkehrender
  Förderer im Reuse-Bereich, nicht nur bei Hastings Pier.
- **Claus Asam** — leitete das Mehrow-Forschungsvorhaben, baut inzwischen ein
  Fertigteil-Archiv bei der BBSR mit der Hochschule Potsdam auf.

→ Empfehlung: behalten. Der Beleg ist stärker, als eine einzelne Kante zeigt,
auch wenn (noch) kein zweiter Knoten im Netz existiert, an dem man das
festmachen könnte.

## Zirkular — Verwechslungsgefahr aufgeklärt, kein Duplikat

Der kritische Fall war `Zirkular → ELYS Kultur- und Gewerbezentrum Basel`.
Die Recherche vermutete, Zirkular könnte fälschlich isoliert sein, weil ihr
bekanntestes Projekt K.118 fehlt. Gegenprobe in den Daten: **K.118 ist bereits
verknüpft** (`CH:K026 Zirkular → K.118 Winterthur`), zusammen mit sieben
weiteren Zirkular-Kanten (Grubenstrasse 29, Kindergarten Mööslistrasse, RE-WIN,
Studio Trachsler Hoffmann, Bauteilkatalog Basel u. a.). Zirkular ist also
längst gut vernetzt — der ELYS-Fall war nur deshalb „kritisch" markiert, weil
**ELYS selbst** (das Gebäude) keine zweite Kante hat, nicht weil Zirkular
isoliert wäre. Auffällig: Zirkulars Rolle steht bei ELYS *und* bei K.118
gleichermaßen als „Aufgabe unklar" — das ist eher eine Lücke in der
Rollenbeschreibung als ein Zeichen für einen Fehlknoten.

→ Empfehlung: Kante bleibt, Einstufung als kritisch war durch die ELYS-Seite
korrekt (das Gebäude hängt wirklich nur an dieser einen Kante), aber kein
Hinweis auf einen Datenfehler.

## Wirklich dünn, nichts Neues gefunden — Streichkandidaten (2)

- **2emain.be → Maison Vignette.** Eine allgemeine Kleinanzeigen-Website
  (vergleichbar Marktplaats), keine Reuse-Organisation. Kein weiterer Bezug
  zum Feld gefunden.
- **Cat Fletcher / Freegle → Brighton Waste House.** Sie selbst ist eine
  bekannte Figur der britischen Reuse-Szene (Freegle-Mitgründerin, Autorin,
  kommunale Reuse-Programme) — aber kein **weiteres benanntes Bauprojekt**
  gefunden, das als zweite Kante im Netz taugen würde. Die Person ist relevant,
  die Kante bleibt trotzdem die einzige belegbare.

→ Diese beiden sind die einzigen, bei denen die Recherche **nichts** ergeben
hat, das für „bleiben" spricht.

---

## Unverändert kritisch, keine Klärung möglich

- **UK CLT → CascadeUp**: Identität geklärt (Timber-Firma, nicht Community
  Land Trust), CascadeUp selbst hat weitere Partner (Portakabin, UCL) — aber
  UK CLT bleibt einzeln.

---

## Zusammenfassung

| Befund | Anzahl | Fälle |
|---|---:|---|
| Knoten-Duplikat / Datenfehler | 2 | Franck/Franck Bricks, Four Bay Structures |
| Beziehung falsch typisiert | 1 | ABN AMRO – Victory Group (kein Reuse) |
| Weitere Kante recherchiert, Partner ist Knoten | 7 | DBU, Dusseldorp, a:gain, DOVISTA/KRONE, Rijkswaterstaat, Réavie, Lindner |
| Bestätigt zentraler Akteur, aber (noch) keine zweite Kante im Netz | 5 | ERDF/FEDER, Embuild, OVAM, NLHF, Claus Asam |
| Geklärt, kein Fehler (Zirkular) | 1 | Zirkular/ELYS |
| Nichts gefunden — Streichkandidat | 2 | 2emain.be, Cat Fletcher/Freegle |
| Unverändert kritisch | 5 | restliche Fälle ohne neuen Befund |

Nichts hiervon ist angewendet. Sag, welche Kanten bleiben, welche weg sollen,
und ob die zwei Datenfehler (Franck-Zusammenführung, Victory-Group-Umtypung)
in einem eigenen Schritt behandelt werden sollen — das sind Graphänderungen,
keine reinen Textänderungen, und fallen damit außerhalb dessen, was der
laufende Textumbau vorsieht.
