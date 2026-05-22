# Abbau Aufbau — konkrete, direkt anwendbare Regeln für die Regelprüf-Architektur

**Sprache:** Deutsch  
**Ziel:** Nur Regeln, die in einem Entwurfs-Rule-Checker mit `Komponente → Paket → Repräsentation → Konnektor → Port → Regelprüfung` ein sinnvolles Ergebnis erzeugen.  
**Ausgeschlossen:** Rückbau, Abbruch, Betonsägen im Bestand, Genehmigungs-/Behördenverfahren, Ausschreibung, Kosten, Förderlogik, Abfall-/Entsorgungslogik, reine LCA-Bewertung.  
**Systemannahme:** Die Bauteile liegen bereits als dokumentierte Pool-Komponenten vor.

## Ergebnislogik

- **PASS:** Verbindung/Platzierung ist mit den vorhandenen Daten plausibel zulässig.
- **WARNUNG:** Verbindung/Platzierung ist möglich, aber benötigt Nachweis, Ergänzung, Toleranzprüfung, Reparatur oder Fachplanung.
- **FAIL:** Verbindung/Platzierung ist mit den vorhandenen Daten unzulässig oder nicht prüfbar.

## Minimal benötigte Datenstruktur pro Komponente

Jede Komponente braucht mindestens:

```text
id
typ / elementfamilie
geometrie / bounding box / masse
öffnungen
portliste
paketdaten: tragwerk, energie, tga_oeffnungen, semantik_architektur, logistik, evidenz
quellen / prüfstatus / unsicherheitsgrad
```

---

## 1. Globale Vorprüfungen

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| G-01 | Evidenz + alle Pakete | `daten_vollstaendigkeit` | `komponente.dossier` ↔ `pruefung.start` | Vor jeder Port-Verbindung. | ID, Typ, Maße, Öffnungen, Volumen, Masse, Prüfstatus, Portliste. | Eine Verbindung darf nur geprüft werden, wenn das Bauteil als eindeutige Komponente mit Mindestdaten vorhanden ist. | FAIL, wenn ID/Geometrie/Masse/Portdaten fehlen; WARNUNG, wenn nur Prüfwerte fehlen. |
| G-02 | Evidenz | `identitaets_sicherheit` | `komponente.id_tag` ↔ `bauteilkatalog.eintrag` | Wenn ein Pool-Element in den Entwurf gezogen wird. | ID, Katalogeintrag, Tracking-/Tracing-Status, Zuordnung zur Geometrie. | Die Geometrie muss eindeutig mit dem Katalogeintrag verbunden sein. | FAIL bei ungeklärter Identität; WARNUNG bei manueller, nicht digital gesicherter Zuordnung. |
| G-03 | Logistik + Evidenz | `katalog_aktualitaet` | `komponente.dossier` ↔ `projektstand.aktuell` | Vor Montage-, Transport- oder Anschlussprüfung. | Datum/Version der Prüfwerte, Schadensstatus, Reparaturstatus, Freigaben. | Der Checker benutzt nur aktuelle Bauteildaten; Transport- oder Lagerschäden müssen eingetragen sein. | WARNUNG bei veralteten Daten; FAIL bei bekannten, ungeklärten Schäden an relevanten Zonen. |

**Beleg:** Der Bauteilkatalog soll ID, Maße, Öffnungen, Volumen und Masse enthalten und kann um Beton- und Bewehrungsuntersuchungen erweitert werden; er bildet die Grundlage für Logistik, Lagerung und Wiedereinbau. PDF S. 129–131.

---

## 2. Tragwerk — direkte Anschlussregeln

| ID | Paket | Konnektor | Port-Paar | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| S-01 | Tragwerk | `schraubankeranschluss` | `fundament.ankerzone_oben` ↔ `bodenplatte.ankerzone_unten` | Wenn Bodenplatte mit Fundament über Schraubanker verbunden wird. | Ankerzone, Betonfestigkeit, Betondeckung, Bewehrungslage, Randabstände, Ankerlasten. | Schraubanker sind nur zulässig, wenn die Ankerzone frei von Bewehrungskonflikten ist und die Lasten in die Tragwerksdaten passen. | PASS bei erfüllten Nachweisen; WARNUNG bei fehlender Bewehrungsgenauigkeit; FAIL bei Konflikt/fehlender Tragfähigkeit. |
| S-02 | Tragwerk | `dornanschluss` | `bodenplatte.dornzone_oben` ↔ `wand.fuss_dornzone` | Wenn Wand auf Bodenplatte über nachträglich montierte Edelstahldorne angeschlossen wird. | Dornpositionen, Bohrzonen, Bewehrungslage, Wandlast, Betongüte, Einbindetiefe. | Dornpositionen dürfen keine kritische Bewehrung treffen und müssen zur Last- und Geometrieachse der Wand passen. | PASS/WARNUNG/FAIL nach Bewehrungskonflikt und Tragfähigkeit. |
| S-03 | Tragwerk + Brandschutz | `winkelverbinderanschluss` | `bodenplatte.winkelzone_oben` ↔ `wand.fuss_winkelzone` | Wenn Wand mit Winkelverbindern an Bodenplatte angeschlossen wird. | Winkelposition, Befestigungsmittel, Brandbekleidung/Fußbodenaufbau, Randabstände, Lasten. | Winkelverbinder sind nur akzeptabel, wenn sie tragfähig befestigt und im geforderten Brandschutzkontext verdeckt/geschützt sind. | PASS bei Tragwerk + Schutz erfüllt; WARNUNG bei fehlendem Brandschutzlayer; FAIL bei fehlender Befestigungszone. |
| S-04 | Tragwerk | `dornanschluss` | `bodenplatte.dornzone_oben` ↔ `stuetze.fuss_dornzone` | Wenn Stütze auf Bodenplatte über Edelstahldorn verbunden wird. | Stützenachse, Dornposition, Punktlast, Bewehrungslage, Betonfestigkeit, Exzentrizität. | Dornanschluss muss Stützenlast und Achslage aufnehmen; Bohrung darf Bewehrung nicht kritisch schneiden. | PASS/WARNUNG/FAIL nach Achse, Last und Bewehrung. |
| S-05 | Tragwerk + Brandschutz | `winkelverbinderanschluss` | `bodenplatte.winkelzone_oben` ↔ `stuetze.fuss_winkelzone` | Wenn Stütze mit Winkelverbindern an Bodenplatte angeschlossen wird. | Winkelposition, Brandschutzabdeckung, Punktlast, Befestigungszonen, Randabstände. | Winkelverbinder bei Stützenfuß brauchen tragfähige Befestigungszonen und brandschutztechnische Verdeckung. | PASS/WARNUNG/FAIL. |
| S-06 | Tragwerk | `bewehrungsanschluss_verguss` | `wand.kopf_bewehrungszone` ↔ `decke.unterseite_vergusszone` | Wenn Wand-Decke über nachträglichen Bewehrungsanschluss und Verguss verbunden wird. | Bewehrungslage, Bohr-/Injektionszonen, Verbundlänge, Vergussfuge, Lastübertragung, Toleranzen. | Der Anschluss ist nur prüfbar, wenn Bewehrungsanschlusszone, Vergussfuge und Lastpfad explizit vorhanden sind. | PASS bei vollständigem Nachweis; WARNUNG bei unvollständiger Bewehrungskarte; FAIL bei Konflikt/fehlender Vergusszone. |
| S-07 | Tragwerk | `schraubanker_flachstahlhalter` | `wand.kopf_ankerzone` ↔ `decke.rand_ankerzone` | Wenn Wand-Decke über Schraubanker mit Flachstahlhalter verbunden wird. | Ankerpunkte, Flachstahlhaltergeometrie, Randabstände, Bewehrungslage, Lasten. | Anker und Halter müssen auf beiden Bauteilen kompatible Ankerzonen treffen. | PASS/WARNUNG/FAIL. |
| S-08 | Tragwerk | `dornanschluss` | `stuetze.kopf_dornzone` ↔ `decke.unterseite_dornzone` | Wenn Stütze-Decke über nachträglich montierten Edelstahldorn verbunden wird. | Stützenkopf, Deckenauflagerzone, Punktlast, Dornposition, Bewehrungslage, Betongüte. | Der Dorn muss in tragfähigen Zonen beider Bauteile liegen und zur Stützenachse passen. | PASS/WARNUNG/FAIL. |
| S-09 | Tragwerk + Brandschutz | `winkelverbinderanschluss` | `stuetze.kopf_winkelzone` ↔ `decke.unterseite_winkelzone` | Wenn Stütze-Decke über Winkelverbinder verbunden wird. | Winkelposition, Befestigungsmittel, Brandschutzbekleidung, Punktlasten, Randabstände. | Winkelverbinder müssen tragfähig befestigt und brandschutztechnisch bekleidet sein. | PASS bei Tragwerk + Bekleidung; WARNUNG bei fehlendem Brandschutznachweis; FAIL bei ungeeigneter Zone. |
| S-10 | Tragwerk | `bewehrungsanschluss_verguss` | `stuetze.kopf_bewehrungszone` ↔ `neuer_stahlbetontraeger.verguss_bewehrungszone` | Wenn Stütze/Deckenelement auf neuen Stahlbetonträger mit nachträglichem Bewehrungsanschluss und Verguss trifft. | Bewehrungsanschluss, Traegerauflager, Vergussfuge, Lasten, Toleranzen, Betongüte. | Der neue Träger muss als kompatibler Aufnahmepartner mit Verguss- und Bewehrungsanschlusszone modelliert sein. | PASS/WARNUNG/FAIL. |
| S-11 | Tragwerk | `stahlauflager` | `decke.auflagerkante_unten` oder `stuetze_decke_fragment.auflagerzone` ↔ `stahltraeger.obergurt_auflager` | Wenn ein Beton-Element auf Stahlträger aufgelagert wird. | Auflagerlänge, Kontaktfläche, Reaktionslast, Stahlträgertragfähigkeit, Toleranzen, Brandschutz. | Auflager auf Stahlträger ist nur zulässig, wenn Auflagerfläche, Last und Trägerkapazität kompatibel sind. | PASS/WARNUNG/FAIL. |
| S-12 | Tragwerk | `auflager_pruefung` | `decke.auflagerkante` ↔ `wand.kopf_auflager` | Wenn eine Decke auf Wand gelagert wird. | Auflagerlänge, Wandtragfähigkeit, Deckenreaktion, Spannrichtung, Kontaktfläche, Ebenheit. | Die Auflagerkante der Decke muss zur Wandkopfzone passen und die Deckenreaktion übertragen können. | PASS/WARNUNG/FAIL. |
| S-13 | Tragwerk | `auflager_pruefung` | `decke.auflagerpunkt` ↔ `stuetze.kopf_auflager` | Wenn eine Decke auf Stütze gelagert wird. | Punkt-/Linienauflager, Deckenreaktion, Stützenkapazität, Exzentrizität, lokale Durchstanz-/Kontaktzone. | Punktauflager auf Stütze benötigt kompatible Kontaktzone und zulässige Exzentrizität. | PASS/WARNUNG/FAIL. |
| S-14 | Tragwerk | `fugenverbinder` | `platte.fugenkante_A` ↔ `platte.fugenkante_B` | Wenn zwei Plattendecken nebeneinander gefügt werden. | Fugenkanten, Ebenheit, Höhenversatz, Verbinderart, Fugenbreite, Last-/Scheibenwirkung. | Bei Plattendecken muss der Fugenverbinder gemäß Ausführungslogik vorhanden und geometrisch möglich sein. | PASS/WARNUNG/FAIL. |
| S-15 | Tragwerk | `aussteifungs_abhaengigkeit` | `reuse_element.aussteifungsbedarf` ↔ `neues_aussteifungselement.aussteifungsangebot` | Wenn ReUse-Elemente keine ausreichende Aussteifung im neuen System liefern. | Aussteifungsrolle, Scheiben-/Wandwirkung, Gebäudestabilität, neue Kerne/Wände/Verbände. | Wenn das Element nicht selbst aussteift, muss ein kompatibles aussteifendes Element vorhanden sein. | PASS, wenn Aussteifung geschlossen; WARNUNG bei unvollständigem Modell; FAIL bei fehlender Aussteifung. |
| S-16 | Tragwerk + Evidenz | `tragwerksfreigabe` | `strukturport` ↔ `evidenz.materialkennwerte` | Vor jeder tragenden Verbindung. | Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chloridgehalt, Schadstoffstatus, Bewehrungsdaten. | Tragende Ports dürfen nur PASS ergeben, wenn Material- und Bewehrungskennwerte ausreichend belegt sind. | WARNUNG bei fehlenden Nebenwerten; FAIL bei fehlender Druckfestigkeit oder unbekannter Bewehrung in Anschlusszone. |

**Beleg:** Die PDF nennt konkrete Anschlussprinzipien für Fundament–Bodenplatte, Bodenplatte–Wand, Bodenplatte–Stütze, Wand–Decke und Stütze–Decke: Schraubanker, Edelstahldorne, Winkelverbinder, nachträglicher Bewehrungsanschluss mit Verguss und Auflager auf Stahlträger. PDF S. 208–218. Zusätzlich werden bei Rohbauarbeiten Auflagerprüfung, Anschlüsse, Fugenverbinder sowie ggf. neue aussteifende Elemente genannt. PDF S. 206, 260–262.

---

## 3. Energie — thermische Entwurfsregeln

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| E-01 | Energie | `thermische_grenze` | `bauteil.aussenflaeche` ↔ `klima.aussenluft` | Wenn ein ReUse-Stahlbetonelement Teil der Außenwand ist. | Bauteildicke, Wärmeleitfähigkeit λ, Schichtenaufbau, Ziel-U-Wert, Dämmung. | Kontakt zur Außenluft aktiviert U-Wert-Prüfung für das gesamte Bauteil. | PASS, wenn Ziel-U-Wert erreicht; WARNUNG bei fehlendem λ; FAIL bei nicht erreichbarem U-Wert. |
| E-02 | Energie | `thermische_grenze` | `bauteil.unterseite` ↔ `klima.baugrund` | Wenn ein ReUse-Element gegen Baugrund eingesetzt wird. | Dicke, λ, Abdichtung/Dämmung, Ziel-U-Wert, Feuchte-/Sockeldetails. | Kontakt zum Baugrund benötigt Wärmeschutzprüfung und passenden Schichtenaufbau. | PASS/WARNUNG/FAIL. |
| E-03 | Energie | `thermische_grenze` | `bauteil.dachflaeche` ↔ `klima.aussenluft` | Wenn ein ReUse-Element Teil des Dachs ist. | Dachaufbau, Abdichtung, Dämmung, λ, Ziel-U-Wert, Durchdringungen. | Dachbauteile aus ReUse-Beton müssen mit Dämm-/Abdichtungsaufbau den Ziel-U-Wert erreichen. | PASS/WARNUNG/FAIL. |
| E-04 | Energie | `u_wert_pruefung` | `bauteil.energie_repraesentation` ↔ `anforderung.geg_u_wert` | Sobald ein ReUse-Element in der thermischen Hülle liegt. | Bauteildicke, λ nach Nachweis/Annahme, Schichtdicken, Wärmeübergang, Zielwert. | U-Wert-Prüfung berechnet, ob die ergänzte Dämmung das Gesamtbauteil auf den geforderten Wert bringt. | PASS/WARNUNG/FAIL. |
| E-05 | Energie | `schichtenaufbau_pruefung` | `reuse_beton.energie_layer` ↔ `daemmung.layer` | Wenn Dämmung an ReUse-Beton ergänzt wird. | Schichtfolge, Dicke, Materialkennwerte, Lage innen/außen, Feuchteschutzstatus. | Dämmung muss als zusammenhängender Layer zum ReUse-Beton modelliert sein. | PASS bei vollständigem Layer; WARNUNG bei fehlender Feuchte-/Dampflogik. |
| E-06 | Energie | `thermische_kontinuitaet` | `element_A.daemmungskante` ↔ `element_B.daemmungskante` | Wenn zwei Hüllbauteile aneinanderstoßen. | Dämmungskanten, Versatz, Fugenbreite, Anschlussdetail, Material. | Dämmungskanten müssen sich geometrisch treffen; sonst entsteht Wärmebrückenwarnung. | PASS bei Kontinuität; WARNUNG bei Unterbrechung. |
| E-07 | Energie | `waermebruecken_warnung` | `betonbauteil.durchlaufzone` ↔ `huelle.daemmebene` | Wenn Stahlbeton die Dämmebene durchdringt oder stark unterbricht. | Betonquerschnitt, Lage zur Dämmebene, Dämmüberdeckung, Innen/Außen-Kontakt. | Durchlaufender Beton an der Hülle erzeugt Wärmebrückenwarnung, bis ein Detail die Unterbrechung löst. | WARNUNG oder FAIL, wenn Ziel-U-Wert/Detail nicht nachweisbar. |

**Beleg:** Wärmeschutz wird besonders relevant, wenn wiederverwendete Stahlbetonelemente Kontakt zu Außenluft oder Baugrund haben; dann sind U-Wert und ergänzende Dämmung zu bestimmen. PDF S. 163–164.

---

## 4. TGA / Öffnungen — Nutzungs- und Konfliktregeln

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| T-01 | TGA / Öffnungen | `oeffnungsnutzung` | `tga_trasse.querschnitt` ↔ `bauteil.oeffnung` | Wenn eine Leitungstrasse durch eine bestehende Öffnung geführt wird. | Öffnungsmaße, Trassenquerschnitt, Lage, Toleranz, Brandschutz-/Schallschutzstatus. | Bestehende Öffnung darf genutzt werden, wenn Trasse geometrisch passt und exakt zur Leitungsführung liegt. | PASS bei Passung; WARNUNG bei knapper Toleranz; FAIL bei zu kleiner/falsch liegender Öffnung. |
| T-02 | TGA / Öffnungen + Tragwerk | `kernbohrungsnutzung` | `tga_trasse.bohrpunkt` ↔ `bauteil.bohrzone` | Wenn eine neue Kernbohrung / Öffnung in ReUse-Beton geplant wird. | Bohrdurchmesser, Bewehrungskarte, Tragzonen, Randabstände, Materialfestigkeit. | Neue Bohrung ist nur möglich, wenn keine kritische Bewehrung oder tragende Kernzone getroffen wird. | PASS bei freier Bohrzone; WARNUNG bei unsicherer Bewehrung; FAIL bei Bewehrungs-/Tragwerkskonflikt. |
| T-03 | TGA / Öffnungen | `leitungsdurchfuehrung` | `bodenplatte.durchfuehrung` ↔ `leitung.trasse` | Wenn Leitungen durch Bodenplatte/Fundamentbereich geführt werden. | Durchführungsposition, Leitungsachse, Dichtung, Abdichtung, Öffnung, Bauteildicke. | Leitungsdurchführungen müssen bereits in der Bauteil- und Anschlussplanung berücksichtigt sein. | PASS/WARNUNG/FAIL nach Lage und Abdichtung. |
| T-04 | TGA / Öffnungen + Tragwerk | `installationskonflikt` | `wand_oder_stuetze.oeffnung_bohrzone` ↔ `installation.trasse` | Wenn Installationen vertikale tragende Bauteile kreuzen. | Tragrolle, Bewehrungslage, Öffnungsgröße, Lastzone, Trassenlage. | Öffnungen/Bohrungen in Wänden oder Stützen sind nur akzeptabel, wenn Tragwerks- und Bewehrungspaket sie freigeben. | PASS/WARNUNG/FAIL. |
| T-05 | TGA / Öffnungen | `dach_durchdringung` | `dach.bauteil_durchdringung` ↔ `tga_pv_abwasserentlueftung.blitzschutz_port` | Wenn Dachöffnungen für Abwasserentlüftung, PV/Solarthermie oder Blitzschutz vorgesehen werden. | Öffnungsposition, Abdichtung, Dachaufbau, Leitungsdurchmesser, Tragzone. | Dach-Durchdringungen müssen mit Dachaufbau, Abdichtung und Tragwerksport kompatibel sein. | PASS/WARNUNG/FAIL. |

**Beleg:** Die Ausführungsplanung nennt Kernbohrungen oder Öffnungen in wiederverwendeten Stahlbetonelementen für Kabeldurchführungen; bei Erschließung/Leitungen sind bestehende Öffnungen exakt zu nutzen; bei Rohbauarbeiten sind Leitungsdurchführungen, Öffnungen/Bohrungen und Dach-Durchführungen zu beachten. PDF S. 207, 255, 260–262.

---

## 5. Semantik / Architektur — Entwurfsordnung und Lesbarkeit

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| A-01 | Semantik / Architektur | `raster_kontinuitaet` | `element.rasterkante` ↔ `gebaeuderaster.achse` | Wenn ein Element im Neubauraster platziert wird. | Elementbreite, Achsraster, Toleranz, Elementfamilie. | Elementbreite soll das Raster logisch unterstützen; große Abweichungen erzeugen Warnung. | PASS bei Achspassung; WARNUNG bei Abweichung; FAIL nur bei Konflikt mit Tragwerk/Öffnung. |
| A-02 | Semantik / Architektur | `fugen_ausrichtung` | `element_A.fugenkante` ↔ `element_B.fugenkante` | Wenn zwei sichtbare oder konstruktive Kanten verbunden werden. | Fugenkanten, Höhenlage, Versatz, Fugenbreite, sichtbarer Status. | Fugen sollten fluchten oder bewusst als Versatz markiert sein. | PASS bei Flucht/bewusstem Detail; WARNUNG bei unbeabsichtigtem Versatz. |
| A-03 | Semantik / Architektur + Tragwerk | `elementfamilien_passung` | `decke.auflagerkante` ↔ `wand_oder_stuetze_oder_traeger.support_port` | Wenn eine Tragwerksfamilie auf eine andere gesetzt wird. | Elementtyp, Rolle, vertikale/horizontale Lage, Lastpfad. | Platten/Decken verbinden sich mit tragenden Support-Ports, nicht mit beliebigen Sicht-/Randflächen. | PASS/WARNUNG/FAIL. |
| A-04 | Semantik / Architektur | `sichtflaechen_nutzung` | `element.sichtflaeche` ↔ `raum.ansichtsseite` | Wenn eine vorhandene Betonfläche sichtbar bleiben soll. | Sichtseite, Oberflächenzustand, Schäden, Reparaturen, gewünschte Raumseite. | Sichtflächen müssen korrekt orientiert und über Evidenzstatus bewertet sein. | PASS bei sauberer Orientierung; WARNUNG bei Schaden/Reparatur sichtbar; FAIL bei falscher Orientierung. |
| A-05 | Semantik / Architektur + TGA | `oeffnung_semantische_nutzung` | `element.bestandsoeffnung` ↔ `raumfunktion.tuer_fenster_tga` | Wenn eine bestehende Öffnung für Tür, Fenster oder TGA genutzt wird. | Öffnungsmaß, Brüstung/Lage, Raumfunktion, Tragwerksfreigabe, TGA-Route. | Eine vorhandene Öffnung darf semantisch nur genutzt werden, wenn Maße, Lage und Funktion zusammenpassen. | PASS/WARNUNG/FAIL. |
| A-06 | Semantik / Architektur | `zuschnitt_entwurf_iteration` | `element.position` ↔ `grundriss.entwurfsraster` | Wenn ein Pool-Element in einen Grundriss eingesetzt wird. | Elementgeometrie, Raster, Raumprogramm, Toleranz, Anschlussports. | Bei Abweichung zwischen Element und Entwurf muss entweder Position/Raster oder Bauteilauswahl geändert werden. | WARNUNG mit Vorschlag „Raster anpassen“ oder „Element tauschen“; FAIL bei unlösbarem Portkonflikt. |

**Beleg:** Die PDF beschreibt, dass Elementbreiten möglichst ein Raster für den Neubau bilden sollen, dass Elemente auf der Grundrissskizze platziert und iterativ mit dem Entwurf abgeglichen werden, und dass Verbindungsanforderungen daraus abzuleiten sind. PDF S. 100–101.

---

## 6. Logistik / Montage — kontextbezogene Regeln

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| L-01 | Logistik | `transporthuelle_pruefung` | `komponente.transport_bbox` ↔ `transport.standardlimit` | Wenn ein Element transportiert werden soll. | Länge, Breite, Höhe, Transportmittel, Sondertransportstatus. | Standardtransport-Passung: Länge ≤ 13 m, Breite ≤ 3 m, Höhe ≤ 3 m. | PASS innerhalb Limit; WARNUNG/Sondertransport außerhalb. |
| L-02 | Logistik | `masse_transport_pruefung` | `komponente.masse` ↔ `fahrzeug.nutzlast` | Wenn Transportfuhre zusammengestellt wird. | Elementmasse, Fahrzeugnutzlast, Ladekombination, Schwerpunkt. | Summe der Massen darf Fahrzeug- und Ladungssicherungslogik nicht überschreiten. | PASS/WARNUNG/FAIL. |
| L-03 | Logistik | `ladungssicherung_pruefung` | `komponente.auflagepunkte_transport` ↔ `fahrzeug.ladeflaeche` | Wenn Element auf Fahrzeug platziert wird. | Auflagepunkte, Lage, Stapelung, Schutzlagen, Ladungssicherung. | Transportplatzierung muss Bauteil schützen und Ladungssicherung ermöglichen. | PASS/WARNUNG/FAIL. |
| L-04 | Logistik | `hebepruefung` | `komponente.hebeport` ↔ `kran.haken` | Wenn ein Element gehoben/montiert wird. | Masse, Hebepunkte, Anschlagmittel, Schwerpunkt, Kranlasttabelle, Reichweite. | Hebepunkte und Kran müssen die Elementmasse an der geplanten Position aufnehmen können. | PASS/WARNUNG/FAIL. |
| L-05 | Logistik | `kranreichweite_pruefung` | `komponente.montageposition` ↔ `kran.stellplatz_ausleger` | Wenn Montageposition gewählt wird. | Kranstandort, Auslegerlänge, Radius, Höhe, Last, Gelände/Platz. | Krantragfähigkeit wird positionsabhängig geprüft; bei zu großem Radius FAIL/WARNUNG. | PASS/WARNUNG/FAIL. |
| L-06 | Logistik | `lagerorientierung_pruefung` | `komponente.lager_orientierung` ↔ `lagerplatz.lagerregel` | Wenn Element im Lager platziert wird. | Elementtyp, ursprüngliche Einbaulage, geplante Lagerlage. | Decken liegend lagern; Wände und Stützen stehend lagern, wenn möglich entsprechend ursprünglicher Lastfälle. | PASS oder WARNUNG/FAIL bei abweichender, nicht nachgewiesener Lagerung. |
| L-07 | Logistik + Evidenz | `witterungsschutz_pruefung` | `komponente.witterungsrisiko` ↔ `lagerplatz.schutzstatus` | Wenn Element gelagert wird. | Risse/Öffnungen, Niederschlagsschutz, Frostperiode, Karbonatisierungsrisiko. | Bei Rissen/Öffnungen und freier Bewitterung erzeugt der Checker Frost-/Karbonatisierungswarnung. | PASS bei Schutz; WARNUNG ohne Schutz; FAIL bei bereits kritischem Schaden. |
| L-08 | Logistik | `lagerkontakt_pruefung` | `komponente.kontaktflaeche` ↔ `lagerholz.auflage` | Wenn Elemente gestapelt/nebeneinander gelagert werden. | Lagerhölzer, Kontaktflächen, Stapelposition, Elementtyp. | Elemente müssen durch schützende Lagerhölzer getrennt sein, um Kontaktbeschädigung zu vermeiden. | PASS/WARNUNG/FAIL. |
| L-09 | Logistik | `einbaureihenfolge_pruefung` | `lagerplatz.stapelposition` ↔ `montageplan.reihenfolge` | Wenn Lagerplatz/Stapelplan erstellt wird. | Montagefolge, Element-ID, Lagerposition, Entnahmerichtung. | Lagerposition muss zur späteren Einbaureihenfolge passen, damit kein unnötiges Umstapeln entsteht. | PASS/WARNUNG. |
| L-10 | Logistik | `lieferreihenfolge_pruefung` | `transport.fuhre` ↔ `baustelle.montagezeitfenster` | Wenn Transportfuhren geplant werden. | Bauzeitplan, Montagezeitpunkt, Baustellenlagerfläche, Element-IDs, Beladung. | Elemente sollen zum richtigen Zeitpunkt geliefert und nicht unnötig auf der Baustelle zwischengelagert werden. | PASS/WARNUNG. |
| L-11 | Logistik + Tragwerk | `montagebereitschaft_pruefung` | `komponente.montageport` ↔ `zielposition.anschlussvorbereitung` | Direkt vor Platzierung im Neubau. | Anschlussdetails, Auflager, Verbinder, Toleranzen, Öffnungen, Freigaben. | Montage darf nur PASS ergeben, wenn Anschlussdetails und Zielposition vorbereitet sind. | PASS/WARNUNG/FAIL. |
| L-12 | Logistik + Semantik | `masskontrolle_zielposition` | `komponente.bbox` ↔ `zielposition.einbauraum` | Wenn Element in Baugrube, Fundamentbereich oder Zielraster gesetzt wird. | Ist-Maße, Planmaße, Toleranzen, Einbauraum, angrenzende Bauteile. | Zielposition muss zu den tatsächlichen Bauteilmaßen passen. | PASS/WARNUNG/FAIL. |

**Beleg:** Transportmaße sollen den Transport mitdenken; Standardwerte 13 m Länge, 3 m Höhe und 3 m Breite werden genannt. Bauteilkatalog, Transport, Lagerung und Wiedereinbau werden über ID/Maße/Masse gesteuert. Einbaureihenfolge, Witterungsschutz, Lagerhölzer und Lagerorientierung werden für das Zwischenlager beschrieben. PDF S. 97, 129–131, 185–186, 235–236.

---

## 7. Evidenz-Overlay — Regeln, die andere Konnektoren beeinflussen

| ID | Paket | Konnektor | Port-Paar / Kontext | Wann läuft die Regel? | Benötigte Daten | Regel | Ergebnis |
|---|---|---|---|---|---|---|---|
| V-01 | Evidenz | `schadensueberlagerung` | `komponente.schadenszone` ↔ `aktiver_port.zone` | Bei jeder Verbindung, deren Port in oder nahe einer Schadenszone liegt. | Schadenspolygone, Risse, Abplatzungen, Korrosion, Portlage, Einflussradius. | Schäden in der Anschluss-/Auflagerzone reduzieren die Freigabe des Ports. | PASS ohne Schaden; WARNUNG bei Abstand/unkritischem Schaden; FAIL bei Schaden im tragenden Kontaktbereich. |
| V-02 | Evidenz + Tragwerk | `riss_korrosionsrisiko` | `komponente.riss` ↔ `tragender_port.zone` | Wenn ein tragender Port in einem gerissenen Bereich liegt. | Rissbreite, Rissursache, Abplatzung, Feuchte, Korrosionsprüfung. | Risse > 0,3 mm oder signifikante Abplatzungen verlangen Korrosionsausschluss vor Wiederverwendung als tragender Port. | WARNUNG bis Nachweis; FAIL bei nicht ausgeschlossener Korrosion. |
| V-03 | Evidenz | `korrosionsnachweis` | `bewehrung.korrosionsstatus` ↔ `tragender_port.freigabe` | Wenn Korrosionsverdacht besteht. | Potentialmessung, Freilegung, Korrosionsbefund, Reparaturstatus. | Tragende Verbindung darf nur PASS sein, wenn Korrosion im relevanten Bereich ausgeschlossen oder behoben ist. | PASS/WARNUNG/FAIL. |
| V-04 | Evidenz | `karbonatisierungsrisiko` | `karbonatisierungstiefe` ↔ `betondeckung` | Wenn Element im Tragwerk oder in feuchte-/witterungsrelevanter Lage verwendet wird. | Karbonatisierungstiefe, Betondeckung, Feuchte-/Lagerstatus, Bewehrungslage. | Wenn Karbonatisierung bis zur Bewehrung reicht oder nahe daran liegt, wird der Port abgewertet. | WARNUNG oder FAIL je nach Abstand und Korrosionsstatus. |
| V-05 | Evidenz + Tragwerk | `materialkennwert_sicherheit` | `materialpruefung` ↔ `tragwerksanschluss` | Vor tragenden Anschlüssen/Auflagern. | Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chlorid, Schadstoffwerte, Prüfmethode. | Tragende Checks dürfen Materialwerte nur nutzen, wenn sie als elementbezogene Prüfwerte vorliegen. | PASS bei belegten Werten; WARNUNG bei Annahmen; FAIL bei fehlender Mindestinformation. |
| V-06 | Evidenz | `rueckprall_validierung` | `rueckprallwert` ↔ `bohrkern_pruefung` | Wenn Druckfestigkeit nur aus Rückprallprüfung kommt. | Rückprallwert, Bohrkernfestigkeit, Prüfdatum. | Rückprallprüfung allein reicht nicht für endgültigen PASS tragender Ports; Bohrkernprüfung muss abgleichen. | WARNUNG bis Bohrkernabgleich; PASS nach Validierung. |
| V-07 | Evidenz + TGA | `bewehrungskonflikt` | `bohrzone` ↔ `bewehrungskarte` | Bei Kernbohrungen, Schraubankern, Dornen und nachträglichen Bewehrungsanschlüssen. | Bewehrungslage, Stabdurchmesser, Betondeckung, Unsicherheit, Bohrdurchmesser. | Bohr-/Ankerzonen dürfen keine kritische Bewehrung treffen. | PASS frei; WARNUNG bei Unsicherheit; FAIL bei Konflikt. |
| V-08 | Evidenz | `bewehrungssicherheit` | `bewehrungsplan` ↔ `scan_daten` | Wenn Bewehrung für einen Port relevant ist. | Plandaten, Ortungsdaten, Abgleichstatus, Genauigkeit. | Vorhandene Bewehrungspläne müssen stichprobenartig/gezielt mit realer Bewehrung abgeglichen sein. | PASS bei Abgleich; WARNUNG bei ungeprüfter Planlage; FAIL bei fehlenden Daten in Anschlusszone. |
| V-09 | Evidenz + Logistik | `transport_lagerschaden` | `komponente.schadensstatus_nach_transport` ↔ `montagefreigabe` | Vor Einbau nach Transport oder Lagerung. | Schadensprüfung, Fotos, Riss-/Abplatzungsstatus, Reparaturstatus. | Neu erkannte Schäden vor Einbau müssen begutachtet und ggf. aufgearbeitet werden. | PASS nach Freigabe; WARNUNG bei unkritischem Befund; FAIL bei ungeklärtem Schaden. |
| V-10 | Evidenz + Semantik | `sichtflaechen_schaden` | `element.sichtflaeche` ↔ `raum.ansicht` | Wenn Oberfläche sichtbar bleiben soll. | Oberflächenzustand, Risse, Abplatzungen, Reparaturen, gewünschte Sichtqualität. | Sichtbarer Schaden erzeugt architektonische Warnung, auch wenn Tragwerk PASS ist. | PASS/WARNUNG. |

**Beleg:** Die PDF fordert visuelle Begutachtung von Qualität, Schäden, Rissen, Korrosion und Instandsetzungen; Risse über 0,3 mm und Abplatzungen benötigen Korrosionsausschluss. Betonkennwerte, Karbonatisierung, Druckfestigkeit und Bewehrungslage sollen geprüft bzw. dokumentiert werden. Bei Schäden nach Lagerung/Transport müssen Elemente vor Einbau begutachtet und aufgearbeitet werden. PDF S. 75–80, 262.

---

## Nicht in diese Systemstufe übernommen

Diese Regelarten wurden bewusst ausgeschlossen, weil sie für einen Port-zu-Port-Entwurfschecker kein direktes, vernünftiges PASS/WARNUNG/FAIL-Ergebnis erzeugen:

- Rückbau- und Abbruchstatik des Spendergebäudes.
- Betonsägeabfolge und Entnahme aus dem Bestand.
- Abbruchanzeige, Bauvoranfrage, ZiE/vBG-Behördenverfahren als Prozess.
- Ausschreibung, Vergabe, Vertrags- und Gewährleistungsregeln.
- Kostenaufteilung zwischen Spender- und Neubauprojekt.
- Abfallrecht, Entsorgung und Schadstoffrückbau.
- Vollständige LCA-/CO₂-Bilanz als Anschlussregel.
- Allgemeine Gebäudezertifizierung.

