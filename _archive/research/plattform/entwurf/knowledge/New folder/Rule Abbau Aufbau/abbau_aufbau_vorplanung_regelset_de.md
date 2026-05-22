# Vorplanungs-Regelset für die Regelprüf-Architektur

**Sprache:** Deutsch  
**Kontext:** Design-Rule-Checker für einen bereits dokumentierten Pool wiederverwendbarer Stahlbeton-Komponenten.  
**Phase:** Vorplanung.  
**Quelle:** BBSR-Online-Publikation 61/2024, „Abbau Aufbau“, inklusive Handbuch-Anhang.  

Dieses Dokument filtert die vorhandene konkrete Regelmatrix auf diejenigen Regeln, die in der **Vorplanung** wirklich ein sinnvolles Ergebnis erzeugen. Rückbau-, Abbruch-, Behörden-, Kosten- und detaillierte Ausführungsregeln bleiben deaktiviert. Die Systemannahme ist: Die Komponenten sind bereits im Pool vorhanden und besitzen Pakete mit dokumentierten Daten.

---

## 1. Auswahlprinzip

Eine Regel wurde für die Vorplanung behalten, wenn sie eine frühe Entwurfsentscheidung unterstützt: Bauteilauswahl, grobe Platzierung, Raster- und Fugenlogik, grobe Tragwerksplausibilität, thermische Hüllflächenlogik, Nutzung vorhandener Öffnungen, Transport-/Hebbarkeit oder Evidenzrisiko.

Eine Regel wurde ausgeschlossen, wenn sie erst nach Festlegung konkreter Anschlussmittel, Bohrpositionen, Lagerzustände, Montageabläufe oder Ausführungsdetails sinnvoll prüfbar ist.

**Wichtig:** Ausgeschlossen bedeutet hier nicht „unwichtig“. Es bedeutet nur: **nicht in der Vorplanung aktiv schalten**.

---

## 2. Ergebnisübersicht

| Paket | aktiv in Vorplanung | nicht aktiv in Vorplanung |
|---|---:|---:|
| Structural | 4 | 11 |
| Energy | 5 | 0 |
| TGA / Openings | 4 | 0 |
| Semantic / Architectural | 4 | 0 |
| Logistics | 4 | 6 |
| Evidence | 6 | 2 |
| **Gesamt** | **27** | **19** |

---

## 3. Aktive Regeln für die Vorplanung

Jede Regel ist im Paket verortet, das die fachliche Datenhoheit besitzt. Andere Pakete liefern Zusatzdaten. Besonders wichtig: **Evidence** ist meist ein Overlay, das ein Ergebnis von `PASS` auf `WARNUNG` oder `FAIL` abwertet.

### Structural

**Aktive Vorplanungsregeln:** 4

#### R-S11 — Decke/Fragment ↔ Stahlträger über Auflager

- **Paket:** `Structural`
- **Komponenten:** `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `Stahltraeger`
- **Konnektoren:** `stahlauflager_nutzung` ↔ `stahlauflager_angebot`
- **Ports:** `decke.auflagerkante_unten` oder `fragment.auflagerzone_unten` ↔ `stahltraeger.obergurt_auflager`
- **Wann läuft die Regel?** Wenn ein ReUse-Betonelement auf einem Stahlträger aufgelagert wird.
- **Benötigte Daten:** Auflagerlänge, Kontaktfläche, Reaktionslast, Stahlträgertragfähigkeit, Ebenheit, Toleranz, Brandschutz des Stahlträgers, Elementmasse.
- **Prüfregel:** Das Auflager ist nur zulässig, wenn Auflagerfläche, Last, Toleranz und Trägerkapazität kompatibel sind.
- **Resultat:** PASS = Last und Auflagergeometrie kompatibel. WARNUNG = Brandschutz/Toleranz noch offen. FAIL = zu geringe Auflagerfläche oder unzureichende Trägerkapazität.
- **Quelle / Evidenz:** PDF S. 218: Stütze–Decke über Auflager auf Stahlträger, Beispiel Deltabeam.

#### R-S12 — Deckenplatte ↔ Wand als direktes Linienauflager

- **Paket:** `Structural`
- **Komponenten:** `ReuseDeckenplatte` ↔ `ReuseWand` oder `NeubauWand`
- **Konnektoren:** `auflagerbedarf_linie` ↔ `auflagerangebot_linie`
- **Ports:** `decke.auflagerkante_unten` ↔ `wand.kopf_auflager`
- **Wann läuft die Regel?** Wenn eine Decke auf einer Wand gelagert wird.
- **Benötigte Daten:** Spannrichtung, Deckenreaktion, Auflagerlänge, Wandtragfähigkeit, Kontaktfläche, Ebenheit, Materialkennwerte, Schadenszonen.
- **Prüfregel:** Die Auflagerkante der Decke muss zur Wandkopfzone passen und die Deckenreaktion über eine ausreichende Kontaktfläche übertragen können.
- **Resultat:** PASS = Auflagerlänge, Last und Evidenz passen. WARNUNG = Ebenheit/Toleranz unklar. FAIL = falsche Spannrichtung, fehlendes Auflager oder Schaden im Kontaktbereich.
- **Quelle / Evidenz:** PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile.

#### R-S13 — Deckenplatte ↔ Stütze als Punktauflager

- **Paket:** `Structural`
- **Komponenten:** `ReuseDeckenplatte` ↔ `ReuseStuetze` oder `NeubauStuetze`
- **Konnektoren:** `auflagerbedarf_punkt` ↔ `auflagerangebot_punkt`
- **Ports:** `decke.auflagerpunkt_unten` ↔ `stuetze.kopf_auflager`
- **Wann läuft die Regel?** Wenn eine Decke auf einer Stütze gelagert wird.
- **Benötigte Daten:** Punktlast, Stützenkapazität, Kontaktzone, Exzentrizität, lokale Plattentragfähigkeit/Durchstanzrisiko, Bewehrungskarte, Schäden.
- **Prüfregel:** Punktauflager auf Stütze benötigt eine kompatible Kontaktzone und eine zulässige Exzentrizität.
- **Resultat:** PASS = Achse, Kontakt und Last passen. WARNUNG = Durchstanz-/Exzentrizitätsprüfung unvollständig. FAIL = Kontaktzone zu klein, Exzentrizität zu groß oder Materialwerte fehlen.
- **Quelle / Evidenz:** PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile.

#### R-S15 — ReUse-Tragwerk ↔ Aussteifungselement

- **Paket:** `Structural`
- **Komponenten:** `ReuseDeckenplatte`, `ReuseWand`, `ReuseFragment_StuetzeDecke` ↔ `Aussteifungselement`
- **Konnektoren:** `aussteifungsbedarf` ↔ `aussteifungsangebot`
- **Ports:** `reuse_element.aussteifungsbedarf` ↔ `aussteifungselement.aussteifungsport`
- **Wann läuft die Regel?** Wenn das neue Gebäude aus ReUse-Elementen nicht selbst ausreichend ausgesteift ist.
- **Benötigte Daten:** Tragrolle jedes Elements, Scheiben-/Wandwirkung, horizontale Lasten, Gebäudehöhe, neue Kerne/Wände/Verbände, Anschlussfähigkeit.
- **Prüfregel:** Wenn ReUse-Elemente die Gebäudestabilität nicht selbst sichern, muss ein kompatibles aussteifendes Element im Tragwerksgraph vorhanden sein.
- **Resultat:** PASS = Aussteifung geschlossen. WARNUNG = Aussteifungsmodell unvollständig. FAIL = fehlende oder nicht angeschlossene Aussteifung.
- **Quelle / Evidenz:** PDF S. 206: Ggf. müssen neue aussteifende Elemente errichtet werden, um die wiederverwendeten Stahlbetonelemente auszusteifen.

### Energy

**Aktive Vorplanungsregeln:** 5

#### R-E01 — ReUse-Element ↔ Außenluft als thermische Grenze

- **Paket:** `Energy`
- **Komponenten:** `ReuseWand`, `ReuseDeckenplatte` oder `ReuseDachplatte` ↔ `Klima_Aussenluft` + `DaemmungLayer`
- **Konnektoren:** `thermische_grenze` ↔ `u_wert_anforderung` / `daemmung_ergaenzung`
- **Ports:** `bauteil.aussenflaeche` ↔ `klima.aussenluft` und `daemmung.layer_innen_oder_aussen`
- **Wann läuft die Regel?** Wenn ein ReUse-Stahlbetonelement Teil der Außenwand oder einer außenluftberührten Hüllfläche wird.
- **Benötigte Daten:** Bauteildicke, Wärmeleitfähigkeit λ, Rohdichte/Betonkennwerte, Schichtenaufbau, Dämmstoff, Dämmstärke, Ziel-U-Wert, Wärmeübergänge.
- **Prüfregel:** Kontakt zur Außenluft aktiviert eine U-Wert-Prüfung des gesamten Bauteils; fehlende oder zu geringe Dämmung erzeugt Warnung oder Fail.
- **Resultat:** PASS = Ziel-U-Wert erreicht. WARNUNG = λ fehlt oder Dämmung nur angenommen. FAIL = U-Wert nicht erreichbar oder keine Dämmung modelliert.
- **Quelle / Evidenz:** PDF S. 163–164: Bei Kontakt zu Außenklima muss der U-Wert bestimmt und mit Dämmung auf den geforderten Wert gebracht werden.

#### R-E02 — ReUse-Element ↔ Baugrund als thermische Grenze

- **Paket:** `Energy`
- **Komponenten:** `ReuseBodenplatte` oder `ReuseWand` im erdberührten Bereich ↔ `Klima_Baugrund` + `DaemmungLayer` + `AbdichtungLayer`
- **Konnektoren:** `thermische_grenze_erdberuehrt` ↔ `baugrund_u_wert_anforderung`
- **Ports:** `bauteil.erdberuehrte_flaeche` ↔ `klima.baugrund` / `daemmung.erdberuehrt`
- **Wann läuft die Regel?** Wenn ein ReUse-Betonbauteil gegen Baugrund eingesetzt wird.
- **Benötigte Daten:** Dicke, λ, Dämmlage, Abdichtung, Feuchteschutzstatus, Ziel-U-Wert, Sockel-/Erdkontakt-Detail.
- **Prüfregel:** Erdberührte ReUse-Betonbauteile brauchen Wärmeschutz- und Abdichtungsmodell, bevor die Platzierung PASS ergeben darf.
- **Resultat:** PASS = U-Wert und Abdichtung vollständig. WARNUNG = Feuchteschutz unvollständig. FAIL = keine thermische/feuchtebezogene Schichtlogik vorhanden.
- **Quelle / Evidenz:** PDF S. 163–164: Wärmeschutz ist bei Kontakt zu Außenluft oder Baugrund besonders zu beachten.

#### R-E03 — ReUse-Dachplatte ↔ Dachaufbau

- **Paket:** `Energy`
- **Komponenten:** `ReuseDachplatte` oder `ReuseDeckenplatte` als Dach ↔ `Dachaufbau`
- **Konnektoren:** `dach_thermische_grenze` ↔ `dachaufbau_anschluss`
- **Ports:** `dachplatte.dachflaeche` ↔ `dachaufbau.daemmung_abdichtung`
- **Wann läuft die Regel?** Wenn ein ReUse-Betonelement als Dach oder Teil des Dachs verwendet wird.
- **Benötigte Daten:** Dachaufbau, Abdichtung, Dämmung, λ, Ziel-U-Wert, Neigung, Durchdringungen, Tragzone.
- **Prüfregel:** Die Dachplatte muss mit Dachaufbau, Abdichtung und Dämmung als vollständiges Hüllbauteil modelliert sein.
- **Resultat:** PASS = U-Wert + Abdichtung + Durchdringungszonen geklärt. WARNUNG = Dachform oder Durchdringungen offen. FAIL = unvollständiger Dachaufbau.
- **Quelle / Evidenz:** PDF S. 207: Dachkonstruktion abhängig von Dachform, ggf. durch wiederverwendete Elemente beeinflusst; PDF S. 262: Dachaufbau und Durchführungen beachten.

#### R-E04 — Dämmungskante ↔ Dämmungskante thermische Kontinuität

- **Paket:** `Energy`
- **Komponenten:** `DaemmungLayer` an ReUse-Bauteil A ↔ `DaemmungLayer` an Bauteil B
- **Konnektoren:** `thermische_kontinuitaet` ↔ `thermische_kontinuitaet`
- **Ports:** `element_A.daemmungskante` ↔ `element_B.daemmungskante`
- **Wann läuft die Regel?** Wenn zwei Hüllbauteile aneinanderstoßen.
- **Benötigte Daten:** Dämmungskanten, Versatz, Fugenbreite, Anschlussdetail, Material, Dämmebenenlage.
- **Prüfregel:** Dämmungskanten müssen sich geometrisch treffen; bei Unterbrechung entsteht eine Wärmebrückenwarnung.
- **Resultat:** PASS = kontinuierliche Dämmebene. WARNUNG = Unterbrechung oder Versatz. FAIL = thermische Hülle nicht schließbar.
- **Quelle / Evidenz:** PDF S. 163–164: ReUse-Beton in der Hülle muss mit Dämmung so ergänzt werden, dass der geforderte U-Wert erreicht wird.

#### R-E05 — Beton-Durchlaufzone ↔ Dämmebene Wärmebrücke

- **Paket:** `Energy`
- **Komponenten:** `ReuseWand`, `ReuseDeckenplatte`, `ReuseFragment_StuetzeDecke` ↔ `DaemmungLayer` / `ThermischeHuelle`
- **Konnektoren:** `waermebruecken_risiko` ↔ `daemmebene`
- **Ports:** `betonbauteil.durchlaufzone` ↔ `huelle.daemmebene`
- **Wann läuft die Regel?** Wenn ein Stahlbetonelement die Dämmebene durchstößt oder stark unterbricht.
- **Benötigte Daten:** Betonquerschnitt, Lage zur Dämmebene, Dämmüberdeckung, Innen/Außen-Kontakt, Anschlussdetail.
- **Prüfregel:** Durchlaufender Beton an der thermischen Hülle erzeugt eine Wärmebrückenwarnung, bis ein Detail die Unterbrechung löst.
- **Resultat:** WARNUNG = Wärmebrücke möglich. PASS = Detail mit durchgehender Dämmung vorhanden. FAIL = Ziel-U-Wert/Detail nicht nachweisbar.
- **Quelle / Evidenz:** PDF S. 163–164: Bei Hüllbauteilen muss die Dämmung den U-Wert des gesamten Bauteils auf den geforderten Wert herabsenken.

### TGA / Openings

**Aktive Vorplanungsregeln:** 4

#### R-T01 — TGA-Trasse ↔ bestehende Öffnung

- **Paket:** `TGA / Openings`
- **Komponenten:** `TGA_Trasse` ↔ `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke`
- **Konnektoren:** `oeffnung_nutzen` ↔ `bestandsoeffnung_angebot`
- **Ports:** `tga_trasse.querschnitt` ↔ `bauteil.bestandsoeffnung`
- **Wann läuft die Regel?** Wenn eine Leitungstrasse durch eine vorhandene Öffnung geführt werden soll.
- **Benötigte Daten:** Öffnungsmaße, Trassenquerschnitt, Lage, Toleranz, Brandschutz-/Schallschutzstatus, Abdichtung, Raumfunktion.
- **Prüfregel:** Eine bestehende Öffnung darf genutzt werden, wenn die Trasse geometrisch passt und exakt zur Leitungsführung liegt.
- **Resultat:** PASS = Öffnung passt. WARNUNG = Toleranz knapp oder Brandschutz offen. FAIL = Öffnung zu klein, falsch liegend oder funktional unpassend.
- **Quelle / Evidenz:** PDF S. 207: ggf. Kernbohrungen oder Öffnungen in ReUse-Stahlbetonelementen für Kabeldurchführungen.

#### R-T02 — TGA-Trasse ↔ neue Kernbohrung / Bohrzone

- **Paket:** `TGA / Openings`
- **Komponenten:** `TGA_Trasse` ↔ `ReuseWand`, `ReuseDeckenplatte`, `ReuseStuetze` oder `ReuseBodenplatte`
- **Konnektoren:** `kernbohrung_bedarf` ↔ `bohrzone_angebot`
- **Ports:** `tga_trasse.bohrpunkt` ↔ `bauteil.bohrzone`
- **Wann läuft die Regel?** Wenn eine neue Kernbohrung oder Öffnung in ReUse-Beton geplant wird.
- **Benötigte Daten:** Bohrdurchmesser, Bohrtiefe, Bewehrungskarte, Tragzonen, Randabstände, Materialfestigkeit, Schadenszonen, Toleranz.
- **Prüfregel:** Neue Bohrungen sind nur möglich, wenn keine kritische Bewehrung, keine Schadenszone und keine tragende Kernzone getroffen wird.
- **Resultat:** PASS = freie Bohrzone. WARNUNG = Bewehrungsunsicherheit. FAIL = Bewehrungs-/Tragwerkskonflikt oder Schaden in Bohrzone.
- **Quelle / Evidenz:** PDF S. 207 und S. 260–262: Öffnungen/Bohrungen und Leitungsführungen sind bei TGA und Rohbauarbeiten zu beachten.

#### R-T03 — Bodenplatte/Fundament ↔ Leitungsdurchführung

- **Paket:** `TGA / Openings`
- **Komponenten:** `TGA_Trasse` ↔ `ReuseBodenplatte`, `NeubauBodenplatte` oder `NeubauFundament`
- **Konnektoren:** `leitungsdurchfuehrung_bedarf` ↔ `durchfuehrung_angebot`
- **Ports:** `leitung.trasse` ↔ `bodenplatte.durchfuehrung` oder `fundament.durchfuehrung`
- **Wann läuft die Regel?** Wenn Leitungen durch Bodenplatte oder Fundamentbereich geführt werden.
- **Benötigte Daten:** Durchführungsposition, Leitungsachse, Öffnungsmaß, Dichtung, Abdichtung, Bauteildicke, Bewehrungskarte, Sockel-/Erdkontakt.
- **Prüfregel:** Leitungsdurchführungen müssen in Bauteil- und Anschlussplanung berücksichtigt sein und dürfen Tragwerk, Abdichtung und Dämmung nicht verletzen.
- **Resultat:** PASS = Durchdringung, Abdichtung und Tragwerk kompatibel. WARNUNG = Abdichtung/Bewehrung offen. FAIL = keine Durchführung oder Konflikt mit Trag-/Abdichtungszone.
- **Quelle / Evidenz:** PDF S. 260–261: Fundamente und Bodenplatten müssen Leitungsdurchführungen beachten bzw. herstellen.

#### R-T04 — Dachplatte/Dachaufbau ↔ Dach-Durchdringung

- **Paket:** `TGA / Openings`
- **Komponenten:** `TGA_Trasse` oder `PV_Solar_Blitzschutz_Element` ↔ `ReuseDachplatte` + `Dachaufbau`
- **Konnektoren:** `dach_durchdringung_bedarf` ↔ `dach_durchdringung_angebot`
- **Ports:** `tga_pv_blitzschutz.durchdringungspunkt` ↔ `dach.bauteil_durchdringung`
- **Wann läuft die Regel?** Wenn Abwasserentlüftung, PV/Solarthermie oder Blitzschutz durch/auf dem Dach vorgesehen wird.
- **Benötigte Daten:** Öffnungsposition, Leitungs-/Bauteildurchmesser, Abdichtung, Dachaufbau, Dämmung, Tragzone, Gefälle, Feuchteschutz.
- **Prüfregel:** Dach-Durchdringungen müssen mit Dachaufbau, Abdichtung, Dämmung und Tragwerkszone kompatibel sein.
- **Resultat:** PASS = vollständiges Durchdringungsdetail. WARNUNG = Abdichtung/Dämmung noch offen. FAIL = Konflikt mit Tragzone oder keine Abdichtung.
- **Quelle / Evidenz:** PDF S. 262: Dach benötigt Auflagerprüfung, Dachaufbau und Durchführungen für Abwasserentlüftung, PV/Solarthermie und Blitzschutz.

### Semantic / Architectural

**Aktive Vorplanungsregeln:** 4

#### R-A01 — ReUse-Element ↔ Gebäuderaster

- **Paket:** `Semantic / Architectural`
- **Komponenten:** `ReuseDeckenplatte`, `ReuseWand`, `ReuseUnterzug` oder `ReuseFragment_StuetzeDecke` ↔ `Gebaeuderaster`
- **Konnektoren:** `rasterbindung` ↔ `raster_achse`
- **Ports:** `element.rasterkante` ↔ `gebaeuderaster.achse`
- **Wann läuft die Regel?** Wenn ein Pool-Element in ein Neubauraster gesetzt wird.
- **Benötigte Daten:** Elementbreite, Achsraster, Toleranz, Elementfamilie, Anschlussports, Spannrichtung.
- **Prüfregel:** Elementbreiten und Anschlusskanten sollen das Neubauraster unterstützen; große Abweichungen erzeugen Warnung oder erfordern Rasteranpassung.
- **Resultat:** PASS = Achspassung. WARNUNG = Abweichung mit Anpassungsvorschlag. FAIL = Rasterkonflikt erzeugt unlösbaren Tragwerks-/Portkonflikt.
- **Quelle / Evidenz:** PDF S. 100–101: Elementbreite soll möglichst ein festes Raster bilden; Elemente werden auf der Grundrissskizze platziert und iterativ abgeglichen.

#### R-A02 — ReUse-Element ↔ ReUse-Element Fugenflucht

- **Paket:** `Semantic / Architectural`
- **Komponenten:** `ReuseDeckenplatte` oder `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReuseWand`
- **Konnektoren:** `fugenbild_angebot` ↔ `fugenbild_angebot`
- **Ports:** `element_A.fugenkante` ↔ `element_B.fugenkante`
- **Wann läuft die Regel?** Wenn zwei sichtbare oder konstruktive Kanten verbunden werden.
- **Benötigte Daten:** Fugenkanten, Höhenlage, Versatz, Fugenbreite, sichtbarer Status, Verbinderbedarf.
- **Prüfregel:** Fugen sollten fluchten oder als bewusstes Detail markiert sein; unbeabsichtigter Versatz erzeugt Warnung.
- **Resultat:** PASS = Flucht oder bewusstes Detail. WARNUNG = unbeabsichtigter Versatz. FAIL = Versatz kollidiert mit Tragwerksanschluss.
- **Quelle / Evidenz:** PDF S. 100–101: Elemente werden iterativ mit Entwurf und Verbindungsanforderungen abgeglichen.

#### R-A03 — ReUse-Sichtfläche ↔ Raumseite

- **Paket:** `Semantic / Architectural`
- **Komponenten:** `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `Raumfunktion` / `Raumseite`
- **Konnektoren:** `sichtflaeche_angebot` ↔ `sichtflaeche_bedarf`
- **Ports:** `element.sichtflaeche` ↔ `raum.ansichtsseite`
- **Wann läuft die Regel?** Wenn eine bestehende Betonfläche sichtbar bleiben soll.
- **Benötigte Daten:** Sichtseite, Flächennormalen, Oberflächenzustand, Risse, Abplatzungen, Reparaturen, gewünschte Raumseite.
- **Prüfregel:** Sichtflächen müssen korrekt orientiert und über Evidenzstatus bewertet sein.
- **Resultat:** PASS = richtige Orientierung und akzeptabler Zustand. WARNUNG = Schaden/Reparatur sichtbar. FAIL = falsche Orientierung oder nicht akzeptabler sichtbarer Schaden.
- **Quelle / Evidenz:** PDF S. 75–80: Schäden, Risse, Abplatzungen und Oberflächenveränderungen sind zu begutachten.

#### R-A04 — bestehende Öffnung ↔ Raumfunktion

- **Paket:** `Semantic / Architectural`
- **Komponenten:** `ReuseWand` oder `ReuseDeckenplatte` ↔ `Raumfunktion`
- **Konnektoren:** `bestandsoeffnung_angebot` ↔ `oeffnung_bedarf`
- **Ports:** `element.bestandsoeffnung` ↔ `raumfunktion.tuer_fenster_tga`
- **Wann läuft die Regel?** Wenn eine bestehende Öffnung als Tür, Fenster oder TGA-Durchführung genutzt werden soll.
- **Benötigte Daten:** Öffnungsmaß, Brüstung/Lage, Orientierung, Raumfunktion, TGA-Route, Tragwerksfreigabe, Brandschutz/Schallschutz.
- **Prüfregel:** Eine vorhandene Öffnung darf semantisch nur genutzt werden, wenn Maße, Lage, Funktion und technische Anforderungen zusammenpassen.
- **Resultat:** PASS = Öffnung passt zur Funktion. WARNUNG = Anpassung/Brandschutz offen. FAIL = Maß/Lage/Funktion unvereinbar.
- **Quelle / Evidenz:** PDF S. 129–131: Bauteilkatalog soll Öffnungsmaße enthalten; PDF S. 207: Öffnungen können für Durchführungen relevant werden.

### Logistics

**Aktive Vorplanungsregeln:** 4

#### R-L01 — Bauteil ↔ Standardtransport-Hülle

- **Paket:** `Logistics`
- **Komponenten:** beliebige Pool-Komponente ↔ `Transportmittel` / `StandardtransportLimit`
- **Konnektoren:** `transportfaehigkeit` ↔ `transportkapazitaet`
- **Ports:** `komponente.transport_bbox` ↔ `transport.standardlimit`
- **Wann läuft die Regel?** Wenn ein Element in eine Transportfuhre eingeplant wird.
- **Benötigte Daten:** Länge, Breite, Höhe, Transportmittel, Sondertransportstatus, Gewicht.
- **Prüfregel:** Standardtransport-Passung: Länge ≤ 13 m, Breite ≤ 3 m, Höhe ≤ 3 m.
- **Resultat:** PASS = innerhalb Limit. WARNUNG = außerhalb Limit, Sondertransport nötig. FAIL = Transportmittel kann Hülle nicht aufnehmen.
- **Quelle / Evidenz:** PDF S. 97–100: Elemente sollten Transportmaße mitdenken; 13 m Länge, 3 m Höhe, 3 m Breite werden genannt.

#### R-L02 — Bauteilmasse ↔ Fahrzeugnutzlast

- **Paket:** `Logistics`
- **Komponenten:** beliebige Pool-Komponente oder Fuhrenliste ↔ `Transportmittel`
- **Konnektoren:** `transportmasse` ↔ `nutzlastangebot`
- **Ports:** `komponente.masse_port` ↔ `fahrzeug.nutzlast`
- **Wann läuft die Regel?** Wenn eine Transportfuhre zusammengestellt wird.
- **Benötigte Daten:** Elementmasse, Fahrzeugnutzlast, Ladekombination, Schwerpunkt, Ladungssicherung.
- **Prüfregel:** Summe der Massen darf Fahrzeug- und Ladungssicherungslogik nicht überschreiten.
- **Resultat:** PASS = Masse innerhalb Nutzlast. WARNUNG = Schwerpunkt/Ladungssicherung offen. FAIL = Nutzlast überschritten.
- **Quelle / Evidenz:** PDF S. 129–131: Bauteilkatalog enthält Volumen und Masse; PDF S. 235–236: Transportfuhren sollen richtig beladen und zeitlich abgestimmt sein.

#### R-L03 — Bauteil-Hebeport ↔ Kranhaken

- **Paket:** `Logistics`
- **Komponenten:** beliebige Pool-Komponente ↔ `Kran`
- **Konnektoren:** `hebeanschluss` ↔ `kran_hubangebot`
- **Ports:** `komponente.hebeport` ↔ `kran.haken`
- **Wann läuft die Regel?** Wenn ein Element gehoben oder montiert wird.
- **Benötigte Daten:** Masse, Hebepunkte, Anschlagmittel, Schwerpunkt, Kranlasttabelle, Reichweite, Schadenszonen an Hebepunkten.
- **Prüfregel:** Hebepunkte und Kran müssen die Elementmasse an der geplanten Position aufnehmen können.
- **Resultat:** PASS = Kranlast und Hebepunkte ausreichend. WARNUNG = Schwerpunkt/Hebepunkte unsicher. FAIL = Krantragfähigkeit überschritten oder Hebeport beschädigt.
- **Quelle / Evidenz:** PDF S. 123–126: Krantragkraft hängt von Position, Auslegerlänge, Höhenlage und Winkel ab.

#### R-L04 — Montageposition ↔ Kranreichweite

- **Paket:** `Logistics`
- **Komponenten:** beliebige Pool-Komponente ↔ `Kran`
- **Konnektoren:** `montageposition_bedarf` ↔ `kranreichweite_angebot`
- **Ports:** `komponente.montageposition` ↔ `kran.stellplatz_ausleger`
- **Wann läuft die Regel?** Wenn eine Montageposition gewählt wird.
- **Benötigte Daten:** Kranstandort, Auslegerlänge, Radius, Höhe, Last, Gelände/Platz, Elementmasse.
- **Prüfregel:** Krantragfähigkeit wird positionsabhängig geprüft; zu großer Radius oder zu hohe Last erzeugt Warnung/Fail.
- **Resultat:** PASS = Last am Radius zulässig. WARNUNG = knappe Reserve. FAIL = Last/Radium/Höhe außerhalb Kranbereich.
- **Quelle / Evidenz:** PDF S. 123–126: Kranlastkapazität variiert stark nach Lastposition und Krantyp.

### Evidence

**Aktive Vorplanungsregeln:** 6

#### R-V01 — aktiver Port ↔ Schadenszone

- **Paket:** `Evidence`
- **Komponenten:** beliebige Pool-Komponente ↔ aktiver Anschluss-/Nutzungskontext
- **Konnektoren:** `schadensueberlagerung` ↔ `port_freigabe`
- **Ports:** `komponente.schadenszone` ↔ `aktiver_port.zone`
- **Wann läuft die Regel?** Bei jeder Verbindung, deren Port in oder nahe einer Schadenszone liegt.
- **Benötigte Daten:** Schadenspolygone, Risse, Abplatzungen, Korrosion, Portlage, Einflussradius, Reparaturstatus.
- **Prüfregel:** Schäden in Anschluss-, Auflager-, Bohr- oder Sichtzonen reduzieren die Freigabe des Ports.
- **Resultat:** PASS = kein Schaden. WARNUNG = Schaden nahe Port oder unkritisch. FAIL = Schaden im tragenden Kontakt-/Bohrbereich.
- **Quelle / Evidenz:** PDF S. 75–80: Qualität, Schäden, Risse, Abplatzungen, Korrosion und Instandsetzungen sind zu begutachten.

#### R-V02 — tragender Port ↔ Riss/Korrosionsrisiko

- **Paket:** `Evidence`
- **Komponenten:** beliebige tragende Pool-Komponente ↔ aktiver Tragwerksanschluss
- **Konnektoren:** `riss_korrosionsrisiko` ↔ `tragender_port`
- **Ports:** `komponente.risszone` ↔ `tragender_port.zone`
- **Wann läuft die Regel?** Wenn ein tragender Port in einem gerissenen Bereich liegt.
- **Benötigte Daten:** Rissbreite, Rissursache, Abplatzung, Feuchte, Korrosionsprüfung, Bewehrungslage.
- **Prüfregel:** Risse über 0,3 mm oder signifikante Abplatzungen verlangen Korrosionsausschluss vor tragender Wiederverwendung.
- **Resultat:** WARNUNG = Nachweis fehlt. PASS = Korrosion ausgeschlossen. FAIL = Korrosion nicht ausgeschlossen oder bestätigt.
- **Quelle / Evidenz:** PDF S. 76: Bei Rissen über 0,3 mm und signifikanten Abplatzungen muss sichergestellt werden, dass Bewehrung nicht korrodiert ist.

#### R-V03 — Port ↔ Korrosionsstatus

- **Paket:** `Evidence`
- **Komponenten:** beliebige tragende Pool-Komponente ↔ aktiver Anschluss
- **Konnektoren:** `korrosionsnachweis` ↔ `anschlussfreigabe`
- **Ports:** `bewehrung.korrosionsstatus` ↔ `tragender_port.freigabe`
- **Wann läuft die Regel?** Wenn Korrosionsverdacht besteht oder ein Port Riss-/Feuchtezonen berührt.
- **Benötigte Daten:** Potentialmessung, Freilegung, Korrosionsbefund, Reparaturstatus, Prüfdatum.
- **Prüfregel:** Tragende Verbindung darf nur PASS sein, wenn Korrosion im relevanten Bereich ausgeschlossen oder behoben ist.
- **Resultat:** PASS = ausgeschlossen/repariert. WARNUNG = Verdacht ungeklärt. FAIL = aktive/ungeklärte Korrosion im Anschlussbereich.
- **Quelle / Evidenz:** PDF S. 76–77: Korrosion kann über Potentialmessung oder partielles Freilegen überprüft werden.

#### R-V04 — Karbonatisierungstiefe ↔ Betondeckung

- **Paket:** `Evidence`
- **Komponenten:** beliebige Pool-Komponente ↔ aktiver Tragwerks- oder Lager-/Hüllkontext
- **Konnektoren:** `karbonatisierungsrisiko` ↔ `port_dauerhaftigkeit`
- **Ports:** `komponente.karbonatisierungstiefe` ↔ `komponente.betondeckung` / `aktiver_port.zone`
- **Wann läuft die Regel?** Wenn ein Element tragend, feuchte-/witterungsrelevant oder in der Hülle eingesetzt wird.
- **Benötigte Daten:** Karbonatisierungstiefe, Betondeckung, Feuchte-/Lagerstatus, Bewehrungslage, Korrosionsstatus.
- **Prüfregel:** Wenn Karbonatisierung bis zur Bewehrung reicht oder nahe daran liegt, wird der Port abgewertet.
- **Resultat:** PASS = ausreichender Abstand. WARNUNG = geringe Reserve. FAIL = Karbonatisierung erreicht Bewehrung und Korrosion ist nicht ausgeschlossen.
- **Quelle / Evidenz:** PDF S. 77–78: Karbonatisierung senkt den Korrosionsschutz; Karbonatisierungstiefe wird per Phenolphthalein-Indikatortest bestimmt.

#### R-V05 — Tragwerksanschluss ↔ Materialkennwerte

- **Paket:** `Evidence`
- **Komponenten:** tragende Pool-Komponente ↔ aktiver Tragwerksanschluss
- **Konnektoren:** `materialkennwert_sicherheit` ↔ `tragwerksanschluss`
- **Ports:** `materialpruefung` ↔ `tragwerksanschluss`
- **Wann läuft die Regel?** Vor jedem tragenden Anschluss, Auflager, Bohr-/Anker- oder Dornanschluss.
- **Benötigte Daten:** Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chloridgehalt, Schadstoffstatus, Prüfmethode, Prüfdatum.
- **Prüfregel:** Tragende Checks dürfen Materialwerte nur nutzen, wenn sie als element- oder zonenbezogene Prüfwerte vorliegen.
- **Resultat:** PASS = belegte Werte. WARNUNG = Werte teilweise angenommen. FAIL = fehlende Druckfestigkeit oder fehlende Mindestinformation in Anschlusszone.
- **Quelle / Evidenz:** PDF S. 78–80: Bohrkerne sollen u. a. Chlorid, Schadstoffe, Druck-/Zugfestigkeit, E-Modul und Dichte bestimmen; Rückprallwerte sollen mit Bohrkernen abgeglichen werden.

#### R-V07 — Sichtfläche ↔ Oberflächenzustand

- **Paket:** `Evidence`
- **Komponenten:** Pool-Komponente mit sichtbarer Oberfläche ↔ `Raumseite` / `Sichtanforderung`
- **Konnektoren:** `oberflaechen_evidenz` ↔ `sichtflaechenanforderung`
- **Ports:** `element.sichtflaeche` / `oberflaechenzustand` ↔ `raum.ansichtsseite`
- **Wann läuft die Regel?** Wenn eine Betonfläche sichtbar bleiben soll.
- **Benötigte Daten:** Oberflächenzustand, Risse, Abplatzungen, Reparaturen, Verfärbungen, gewünschte Sichtqualität.
- **Prüfregel:** Sichtbarer Schaden erzeugt eine architektonische Warnung, auch wenn Tragwerk PASS ist.
- **Resultat:** PASS = Zustand akzeptiert. WARNUNG = sichtbarer Schaden/Reparatur. FAIL = sichtbare Seite falsch orientiert oder Anforderung nicht erfüllbar.
- **Quelle / Evidenz:** PDF S. 75–80: Oberflächenveränderungen, Schäden, Risse und Instandsetzungen sind visuell zu begutachten.

---

## 4. Nicht aktive Regeln in der Vorplanung

Diese Regeln bleiben im Gesamtsystem erhalten, sollten aber in der **Vorplanung** nicht als aktive Checks laufen. Sie werden später relevant, wenn konkrete Anschlussmittel, Ausführungsdetails, Lager-/Montagezustände oder Freigabeprozesse modelliert sind.

### Structural — in Vorplanung deaktiviert

#### R-S01 — Fundament ↔ Bodenplatte über Schraubanker

- **Komponenten:** `NeubauFundament` ↔ `ReuseBodenplatte` oder `NeubauBodenplatte`
- **Konnektoren:** `schraubankeraufnahme` ↔ `schraubankeranschluss`
- **Ports:** `fundament.ankerzone_oben` ↔ `bodenplatte.ankerzone_unten`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 208: Fundament–Bodenplatte, Befestigung mit Schraubankern; PDF S. 129–131: Bauteilkatalog mit ID, Maßen, Masse und Prüferweiterungen.

#### R-S02 — Bodenplatte ↔ Wand über Edelstahldorne

- **Komponenten:** `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand`
- **Konnektoren:** `dornaufnahme` ↔ `dornanschluss`
- **Ports:** `bodenplatte.dornzone_oben` ↔ `wand.fuss_dornzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 209: Bodenplatte–Wand, Befestigung über nachträglich montierte Edelstahldorne.

#### R-S03 — Bodenplatte ↔ Wand über Winkelverbinder

- **Komponenten:** `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand`
- **Konnektoren:** `winkelaufnahme` ↔ `winkelverbinderanschluss`
- **Ports:** `bodenplatte.winkelzone_oben` ↔ `wand.fuss_winkelzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 210: Bodenplatte–Wand über Winkelverbinder; Hinweis, dass Winkelverbinder aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden müssen.

#### R-S04 — Bodenplatte ↔ Stütze über Edelstahldorn

- **Komponenten:** `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze`
- **Konnektoren:** `dornaufnahme` ↔ `dornanschluss`
- **Ports:** `bodenplatte.dornzone_oben` ↔ `stuetze.fuss_dornzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 211: Bodenplatte–Stütze über nachträglich montierten Edelstahldorn.

#### R-S05 — Bodenplatte ↔ Stütze über Winkelverbinder

- **Komponenten:** `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze`
- **Konnektoren:** `winkelaufnahme` ↔ `winkelverbinderanschluss`
- **Ports:** `bodenplatte.winkelzone_oben` ↔ `stuetze.fuss_winkelzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 212: Bodenplatte–Stütze über Winkelverbinder; Winkelverbinder müssen aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden.

#### R-S06 — Wand ↔ Decke über nachträglichen Bewehrungsanschluss und Verguss

- **Komponenten:** `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment`
- **Konnektoren:** `bewehrungsanschluss` ↔ `vergussaufnahme`
- **Ports:** `wand.kopf_bewehrungszone` ↔ `decke.unterseite_vergusszone` oder `decke.rand_vergusszone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 213: Wand–Decke über nachträglichen Bewehrungsanschluss und Verguss.

#### R-S07 — Wand ↔ Decke über Schraubanker mit Flachstahlhalter

- **Komponenten:** `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment`
- **Konnektoren:** `schraubankeraufnahme` ↔ `flachstahlhalter_aufnahme`
- **Ports:** `wand.kopf_ankerzone` ↔ `decke.rand_ankerzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 214: Wand–Decke über Schraubanker mit Flachstahlhalter.

#### R-S08 — Stütze ↔ Decke über Edelstahldorn

- **Komponenten:** `ReuseStuetze` ↔ `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke`
- **Konnektoren:** `dornanschluss` ↔ `dornaufnahme`
- **Ports:** `stuetze.kopf_dornzone` ↔ `decke.unterseite_dornzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 215: Stütze–Decke über nachträglich montierten Edelstahldorn.

#### R-S09 — Stütze ↔ Decke über Winkelverbinder

- **Komponenten:** `ReuseStuetze` ↔ `ReuseDeckenplatte`
- **Konnektoren:** `winkelverbinderanschluss` ↔ `winkelaufnahme`
- **Ports:** `stuetze.kopf_winkelzone` ↔ `decke.unterseite_winkelzone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 216: Stütze–Decke über Winkelverbinder; Winkelverbinder müssen mit Brandschutzbekleidung verdeckt werden.

#### R-S10 — ReUse-Stütze/Decke ↔ neuer Stahlbetonträger über Bewehrungsanschluss und Verguss

- **Komponenten:** `ReuseStuetze`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `NeubauStahlbetontraeger`
- **Konnektoren:** `bewehrungsanschluss` ↔ `verguss_bewehrungsaufnahme`
- **Ports:** `reuse_element.bewehrungszone` ↔ `neuer_stahlbetontraeger.verguss_bewehrungszone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel konkrete Anschlussmittel, Bohr-/Anker-/Dorn-/Vergussdetails und Nachweise benötigt. Diese Entscheidung gehört eher in Entwurfs-, Genehmigungs- oder Ausführungsplanung. In der Vorplanung wird stattdessen nur die grobe Auflager- und Tragwerksplausibilität geprüft.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 217: Stütze–Decke über nachträglichen Bewehrungsanschluss und Verguss auf neu herzustellenden Stahlbetonträger.

#### R-S14 — Deckenplatte ↔ Deckenplatte über Fugenverbinder

- **Komponenten:** `ReuseDeckenplatte` ↔ `ReuseDeckenplatte`
- **Konnektoren:** `fugenverbinder_angebot` ↔ `fugenverbinder_angebot`
- **Ports:** `platte_A.fugenkante` ↔ `platte_B.fugenkante`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil der konkrete Fugenverbinder zu detailliert ist. Für die frühe Planung reicht die semantische Regel R-A02 zur Fugenflucht und Raster-/Kantenpassung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 261: Bei Plattendecken sind Fugenverbinder gemäß Ausführungsplanung herzustellen.

### Logistics — in Vorplanung deaktiviert

#### R-L05 — Bauteil ↔ Lagerorientierung

- **Komponenten:** beliebige Pool-Komponente ↔ `Lagerplatz`
- **Konnektoren:** `lagerlage_bedarf` ↔ `lagerregel_angebot`
- **Ports:** `komponente.lager_orientierung` ↔ `lagerplatz.lagerregel`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 186: Elemente sollten möglichst in gleicher Ausrichtung wie im Bestandsgebäude gelagert werden; Decken liegend, Wände/Stützen stehend.

#### R-L06 — Bauteil ↔ Witterungsschutz im Lager

- **Komponenten:** beliebige Pool-Komponente ↔ `Lagerplatz`
- **Konnektoren:** `witterungsempfindlichkeit` ↔ `witterungsschutz_angebot`
- **Ports:** `komponente.witterungsrisiko` ↔ `lagerplatz.schutzstatus`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 185–186: Witterungsschutz erhält Zustand; Regenwasser in Rissen/Öffnungen kann Frostsprengungen verursachen; Feuchte kann Karbonatisierung beschleunigen.

#### R-L07 — Bauteilkontakt ↔ Lagerholz

- **Komponenten:** beliebige Pool-Komponente ↔ `Lagerplatz` / `Lagerholz`
- **Konnektoren:** `lagerkontakt` ↔ `schutzauflage`
- **Ports:** `komponente.transport_auflagepunkt` oder `kontaktflaeche` ↔ `lagerholz.auflage`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 186: Elemente sollen voneinander durch schützende Lagerhölzer getrennt werden.

#### R-L08 — Lagerposition ↔ Einbaureihenfolge

- **Komponenten:** beliebige Pool-Komponente ↔ `Montageplan` / `Lagerplatz`
- **Konnektoren:** `einbauzeit_bedarf` ↔ `lagerzugriff_angebot`
- **Ports:** `komponente.id` / `komponente.montageport` ↔ `lagerplatz.stapelposition` / `montageplan.reihenfolge`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 185: Lagerplan soll Positionen entsprechend späterer Einbaureihenfolge vorsehen.

#### R-L09 — Transportfuhre ↔ Montagezeitfenster

- **Komponenten:** `Transportmittel` mit Elementliste ↔ `Montageplan` / `Baustelle`
- **Konnektoren:** `lieferung_angebot` ↔ `montagezeitfenster_bedarf`
- **Ports:** `transport.fuhre` ↔ `baustelle.montagezeitfenster`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 235–236: Bauzeitplan und Logistik müssen die Einbaureihenfolge berücksichtigen; Fuhren sollen richtige Elemente zum richtigen Zeitpunkt bringen und optimal beladen sein.

#### R-L10 — Bauteil ↔ Zielposition / Anschlussvorbereitung

- **Komponenten:** beliebige Pool-Komponente ↔ Zielposition im Neubau, z. B. `NeubauFundament`, `Wand`, `Stuetze`, `Traeger`, `Decke`
- **Konnektoren:** `montagebereitschaft` ↔ `anschlussvorbereitung`
- **Ports:** `komponente.montageport` ↔ `zielposition.anschlussvorbereitung`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil die Regel Lager-, Montage-, Sequenz- oder Baustellenzustände nach Bauteilauswahl voraussetzt. Diese Regeln sind sinnvoll ab Logistik-/Montageplanung, aber nicht für die frühe Entwurfsentscheidung.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 260–262: Rohbauarbeiten verlangen Anschlüsse, Auflager und Leitungsdurchführungen je Bauteil; Schäden vor Einbau müssen begutachtet und aufgearbeitet werden.

### Evidence — in Vorplanung deaktiviert

#### R-V06 — Bohr-/Anker-/Dornzone ↔ Bewehrungskarte

- **Komponenten:** beliebige Pool-Komponente mit Bohr-/Anker-/Dornzone ↔ aktiver Connector: Schraubanker, Dorn, Bewehrungsanschluss oder Kernbohrung
- **Konnektoren:** `bewehrungskonflikt` ↔ `bohr_anker_dorn_bedarf`
- **Ports:** `bauteil.bewehrungskarte` ↔ `bohrzone` / `ankerzone` / `dornzone` / `bewehrungszone`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil diese Regel konkrete Bohr-, Anker- oder Dornzonen gegen eine Bewehrungskarte prüft. Ohne festgelegte Anschlussposition erzeugt sie zu früh falsche Detailkonflikte.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 79–84: Bewehrungslage, Betondeckung, Durchmesser und Abstände sind zu untersuchen; Ortungsverfahren werden beschrieben.

#### R-V08 — Bauteil nach Transport/Lagerung ↔ Montagefreigabe

- **Komponenten:** beliebige Pool-Komponente ↔ `Montageplan` / Zielanschluss
- **Konnektoren:** `transport_lagerschaden` ↔ `montagefreigabe`
- **Ports:** `komponente.schadensstatus_nach_transport` ↔ `komponente.montageport`
- **Warum nicht Vorplanung?** Nicht aktiv in der Vorplanung, weil sie eine Montagefreigabe nach Transport und Lagerung prüft. Das ist eine späte Qualitäts-/Montagekontrolle, keine frühe Designregel.
- **Spätere Phase:** Entwurfsplanung / Genehmigungsplanung / Ausführungsplanung / Montageplanung, je nach Detailtiefe.
- **Quelle / Evidenz:** PDF S. 262: Werden vor Einbau Schäden aus Zwischenlagerung oder Transport festgestellt, müssen diese begutachtet, eingeschätzt und aufgearbeitet werden.

---

## 5. Empfohlene Aktivierung im Tool

Für die Vorplanung sollte der Checker mit drei Ergebnisstufen arbeiten:

- `PASS`: Die Komponente ist für die gewählte Entwurfsposition grundsätzlich plausibel.
- `WARNUNG`: Die Komponente kann weiterverfolgt werden, benötigt aber Datenverdichtung oder spätere Fachprüfung.
- `FAIL`: Die Komponente ist für diese Position in der Vorplanung nicht sinnvoll weiterzuverfolgen, außer der Entwurf oder die Komponentenauswahl wird geändert.

Empfohlene Reihenfolge:

1. `Semantic / Architectural`: Raster, Fuge, Sichtseite, Raumfunktion.
2. `Structural`: grobes Auflager, Punkt-/Linienauflager, Stahlträger, Aussteifung.
3. `Energy`: Hüllflächen, Dämmkontinuität, Wärmebrückenwarnung.
4. `TGA / Openings`: vorhandene Öffnungen und grobe Durchdringungsrisiken.
5. `Logistics`: Transporthülle, Masse, Hebbarkeit, Kranreichweite.
6. `Evidence`: Overlay auf alle aktiven Portzonen; kann jedes Ergebnis abwerten.

---

## 6. Kurzfazit

Für die Vorplanung sind **27 von 46 konkreten Regeln** geeignet. Der Fokus liegt nicht auf endgültigen Nachweisen, sondern auf früher Plausibilitätsprüfung: Passt das Bauteil geometrisch, tragwerkslogisch, thermisch, architektonisch, logistisch und evidenzbasiert in den Entwurf? Die übrigen **19 Regeln** sind wichtig, aber zu detailliert für diese Phase.
