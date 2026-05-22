# Abbau Aufbau — Detailmatrix für eine Regelprüf-Architektur

**Ziel:** konkrete, systemfähige Regeln für `Komponente → Paket → Repräsentation → Konnektor → Port → Regelprüfung`.

**Auswahlprinzip:** Nur Regeln, die im Entwurfs-Rule-Checker ein sinnvolles Ergebnis `PASS / WARNUNG / FAIL` erzeugen. Rückbau, Abbruch, Behördenverfahren, Ausschreibung, Kosten, Förderlogik, reine LCA-Bilanzierung und allgemeine Prozesshinweise sind ausgeschlossen.

**Systemannahme:** Die Pool-Komponenten sind bereits dokumentiert. Das heißt: ID, Geometrie, Masse, Öffnungen, Bewehrungs-/Materialevidenz, Schadenszonen, Logistikdaten und Ports liegen bereits im Bauteildossier vor.

---

## 0. Komponenten, die im Checker vorkommen dürfen

### 0.1 Pool-Komponenten aus wiederverwendetem Stahlbeton

| Komponententyp | Bedeutung im System | typische Pakete | typische Repräsentation |
|---|---|---|---|
| `ReuseDeckenplatte` | horizontales Plattenelement | Tragwerk, Energie, TGA/Öffnungen, Semantik, Logistik, Evidenz | Platte, Kanten, Auflagerlinien, Öffnungen, Schadensoverlay |
| `ReuseWand` | vertikales Scheibenelement | Tragwerk, Energie, TGA/Öffnungen, Semantik, Logistik, Evidenz | Wandfläche/Scheibe, Kopf-/Fußkante, Öffnungen, Sichtseiten |
| `ReuseStuetze` | vertikales Stabelement | Tragwerk, Logistik, Evidenz, Semantik | Linie/Stab, Kopf-/Fußport, Achse, Querschnitt |
| `ReuseUnterzug` | horizontales Balkenelement | Tragwerk, Logistik, Evidenz, Semantik | Linie/Balken, Auflagerzonen, Anschlusszonen |
| `ReuseDachplatte` | horizontales oder geneigtes Hüll-/Dachelement | Tragwerk, Energie, TGA/Öffnungen, Logistik, Evidenz | Platte, Dachaufbaufläche, Durchdringungen |
| `ReuseFragment_StuetzeDecke` | zusammengesetztes Fragment, z. B. Stützen-Decken-Element | Tragwerk, Semantik, Logistik, Evidenz | Graph aus Stütze + Platte + Auflager-/Knotenports |
| `ReusePlattenfragment` | zugeschnittene Decken-/Bodenplatte | Tragwerk, Energie, Semantik, Logistik, Evidenz | Platte mit Rand-/Fugenkanten |

### 0.2 Ziel-, Kontext- und Neubauteile, die als Gegenpartner gebraucht werden

Diese Gegenpartner sind nicht unbedingt reclaimed pool pieces, aber der Checker braucht sie, weil wiederverwendete Bauteile im Neubau an ihnen anschließen.

| Komponententyp | Bedeutung |
|---|---|
| `NeubauFundament` | neues Fundament / Auflagerbasis |
| `NeubauBodenplatte` | neue oder wiederverwendete Bodenplatte als Anschlussbasis |
| `NeubauStahlbetontraeger` | neu hergestellter Stahlbetonträger mit Verguss-/Bewehrungsanschlusszone |
| `Stahltraeger` | Stahlauflager, z. B. Deltabeam-Prinzip |
| `Aussteifungselement` | neuer Kern, Wand, Verband oder Scheibe für Gebäudestabilität |
| `DaemmungLayer` | Dämmschicht als Energie-Gegenpartner |
| `Dachaufbau` | Abdichtung, Dämmung, Kalt-/Warmdach, Begrünung |
| `TGA_Trasse` | Kabel, Wasser, Sanitär, Lüftung, Abwasserentlüftung usw. |
| `Gebaeuderaster` | Entwurfsraster / Achssystem |
| `Raumfunktion` | Tür-, Fenster-, Sichtflächen- oder TGA-Funktionsanforderung |
| `Transportmittel` | Lkw, Standardtransport, Sondertransport |
| `Kran` | Hebe- und Montagekontext |
| `Lagerplatz` | Zwischenlagerkontext mit Lagerhölzern, Schutz, Reihenfolge |
| `Montageplan` | Bauzeit-/Einbaureihenfolge |

---

## 1. Standard-Port-Vokabular

### 1.1 Tragwerksports

| Port | Vorkommen | Rolle |
|---|---|---|
| `fuss_dornzone` | Wand, Stütze | Anschlusszone für Edelstahldorn am Fuß |
| `kopf_dornzone` | Stütze | Anschlusszone für Edelstahldorn am Kopf |
| `ankerzone_oben` | Fundament, Bodenplatte | Zone für Schraubanker |
| `ankerzone_unten` | Bodenplatte, Decke | Gegen-Zone für Schraubanker |
| `winkelzone_oben` | Bodenplatte | Befestigungszone für Winkelverbinder |
| `fuss_winkelzone` | Wand, Stütze | Gegen-Zone für Winkelverbinder am Fuß |
| `kopf_winkelzone` | Stütze | Gegen-Zone für Winkelverbinder am Kopf |
| `bewehrungszone` | Wand, Stütze, Träger, Decke | Zone für nachträglichen Bewehrungsanschluss |
| `vergusszone` | Decke, Träger, Wand | Fuge/Zone für Verguss |
| `auflagerkante_unten` | Deckenplatte, Dachplatte | untere Kante für Linienauflager |
| `auflagerzone_unten` | Fragment, Decke | Fläche/Zone für Stahl- oder Betonauflager |
| `kopf_auflager` | Wand, Stütze, Träger | tragende Auflagerzone |
| `fugenkante` | Decke, Platte, Wand | Kante für Fugenverbinder oder Fugenbild |
| `support_port` | Wand, Stütze, Träger | allgemeiner tragender Zielport |

### 1.2 Energieports

| Port | Vorkommen | Rolle |
|---|---|---|
| `aussenflaeche` | Wand, Dach, Decke, Bodenplatte | Kontakt zur Außenluft |
| `erdberuehrte_flaeche` | Bodenplatte, Fundamentnahes Element | Kontakt zum Baugrund |
| `energie_layer` | Betonbauteil, Dämmung | Schicht im U-Wert-Modell |
| `daemmungskante` | Dämmschicht, Hüllbauteil | Anschlusskante für thermische Kontinuität |
| `durchlaufzone` | Betonbauteil | potenzielle Wärmebrücke durch Betonquerung |

### 1.3 TGA-/Öffnungsports

| Port | Vorkommen | Rolle |
|---|---|---|
| `bestandsoeffnung` | Wand, Decke, Fragment | bestehende Öffnung für Tür, Fenster oder TGA |
| `bohrzone` | Wand, Decke, Stütze, Bodenplatte | mögliche neue Kernbohrung |
| `durchfuehrung` | Bodenplatte, Fundament, Dach | Leitungsdurchführung |
| `dach_durchdringung` | Dachplatte, Dachaufbau | Durchdringung für Entlüftung, PV/Solarthermie, Blitzschutz |

### 1.4 Semantik-/Architekturports

| Port | Vorkommen | Rolle |
|---|---|---|
| `rasterkante` | Platte, Wand, Unterzug | Bezug auf Entwurfsraster |
| `sichtflaeche` | Wand, Decke, Fragment | bewusst sichtbare Oberfläche |
| `ansichtsseite` | Raumfunktion/Raumseite | gewünschte sichtbare Seite |
| `raumfunktionsport` | Raumfunktion | Tür-, Fenster-, TGA- oder Sichtanforderung |
| `position` | Bauteil | Platzierung im Entwurfsraster |

### 1.5 Logistikports

| Port | Vorkommen | Rolle |
|---|---|---|
| `transport_bbox` | jedes Bauteil | Transporthülle |
| `masse_port` | jedes Bauteil | Gewicht/Masse für Transport und Kran |
| `hebeport` | jedes Bauteil | Hebepunkt / Anschlagpunkt |
| `transport_auflagepunkt` | jedes Bauteil | Auflagepunkt auf Fahrzeug oder Lagerholz |
| `lager_orientierung` | jedes Bauteil | Lage im Zwischenlager |
| `montageport` | jedes Bauteil | Port für Einbau-/Montagefreigabe |
| `montageposition` | Zielposition | Einbauposition im Neubau |

### 1.6 Evidenzports / Overlay-Zonen

| Port / Zone | Bedeutung |
|---|---|
| `schadenszone` | Polygon/Fläche mit Schaden, Abplatzung, Riss, Korrosion |
| `risszone` | Linie/Polygon mit Rissbreite und Rissursache |
| `korrosionsstatus` | Bewehrungskorrosion: unbekannt, ausgeschlossen, bestätigt, repariert |
| `karbonatisierungstiefe` | Karbonatisierungsfront in mm |
| `betondeckung` | Betondeckung in mm |
| `bewehrungskarte` | Lage, Durchmesser und Unsicherheit der Bewehrung |
| `materialpruefung` | Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chlorid, Schadstoffstatus |
| `oberflaechenzustand` | Sichtflächenqualität, Reparaturen, Verfärbungen, Abplatzungen |

---

# 2. Direkt anwendbare Regelmatrix

## 2.1 Tragwerk — Bauteil-zu-Bauteil-Verbindungen

### R-S01 — Fundament ↔ Bodenplatte über Schraubanker

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `NeubauFundament` |
| Komponente B | `ReuseBodenplatte` oder `NeubauBodenplatte` |
| Konnektor A | `schraubankeraufnahme` |
| Konnektor B | `schraubankeranschluss` |
| Port A | `fundament.ankerzone_oben` |
| Port B | `bodenplatte.ankerzone_unten` |
| Repräsentation | Fundament als Volumen/Auflagerfläche; Bodenplatte als Platte mit Ankerzonen |
| Wann läuft die Regel? | Wenn eine Bodenplatte auf einem Fundament über Schraubanker fixiert werden soll. |
| Benötigte Daten | Ankerpositionen, Betonfestigkeit beider Zonen, Betondeckung, Bewehrungskarte, Randabstände, Ankerlasten, Schadenszonen. |
| Regel | Der Anschluss darf nur PASS ergeben, wenn beide Ankerzonen vorhanden sind, keine kritische Bewehrung oder Schadenszone getroffen wird und die Lasten durch den Schraubankeranschluss abgetragen werden können. |
| Ergebnis | PASS = Zonen frei und Nachweise vorhanden. WARNUNG = Bewehrungslage unsicher oder Materialwerte teilweise angenommen. FAIL = fehlende Ankerzone, Bewehrungskonflikt, Schaden im Anschlussbereich oder fehlende Tragfähigkeit. |
| Quelle | PDF S. 208: Fundament–Bodenplatte, Befestigung mit Schraubankern; PDF S. 129–131: Bauteilkatalog mit ID, Maßen, Masse und Prüferweiterungen. |

### R-S02 — Bodenplatte ↔ Wand über Edelstahldorne

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `NeubauBodenplatte` oder `ReuseBodenplatte` |
| Komponente B | `ReuseWand` |
| Konnektor A | `dornaufnahme` |
| Konnektor B | `dornanschluss` |
| Port A | `bodenplatte.dornzone_oben` |
| Port B | `wand.fuss_dornzone` |
| Repräsentation | Bodenplatte als Platte; Wand als Scheibe mit Fußkante und Achse |
| Wann läuft die Regel? | Wenn eine Wand auf eine Bodenplatte gestellt und über nachträglich montierte Edelstahldorne gehalten wird. |
| Benötigte Daten | Dornpositionen, Bohrzonen, Bewehrungskarte, Wandlast, Wandachse, Betongüte, Einbindetiefe, Randabstände, Schaden/Risse im Fußbereich. |
| Regel | Dornpositionen müssen zur Wandachse passen, in beiden Bauteilen in freigegebenen Bohrzonen liegen und dürfen keine kritische Bewehrung treffen. |
| Ergebnis | PASS = Achse, Bohrzone, Tragfähigkeit und Evidenz passen. WARNUNG = Bewehrung unsicher oder Randabstand knapp. FAIL = Bohrung trifft Bewehrung, Wandachse/Port versetzt, fehlender Materialnachweis. |
| Quelle | PDF S. 209: Bodenplatte–Wand, Befestigung über nachträglich montierte Edelstahldorne. |

### R-S03 — Bodenplatte ↔ Wand über Winkelverbinder

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Brandschutz + Evidenz |
| Komponente A | `NeubauBodenplatte` oder `ReuseBodenplatte` |
| Komponente B | `ReuseWand` |
| Konnektor A | `winkelaufnahme` |
| Konnektor B | `winkelverbinderanschluss` |
| Port A | `bodenplatte.winkelzone_oben` |
| Port B | `wand.fuss_winkelzone` |
| Repräsentation | Bodenplatte als Platte; Wand als Scheibe; Fußbodenaufbau als Brandschutz-/Abdecklayer |
| Wann läuft die Regel? | Wenn Wand und Bodenplatte mit Winkelverbindern verbunden werden. |
| Benötigte Daten | Winkelpositionen, Befestigungsmittel, Bewehrungskarte, Randabstände, Lasten, Fußbodenaufbau/Brandschutzabdeckung, Schadenszonen. |
| Regel | Winkelverbinder sind nur zulässig, wenn beide Befestigungszonen tragfähig sind und der Verbinder brandschutztechnisch verdeckt oder bekleidet werden kann. |
| Ergebnis | PASS = Tragwerk und Brandschutzabdeckung erfüllt. WARNUNG = Brandschutzlayer noch nicht modelliert. FAIL = keine Befestigungszone, Bewehrungskonflikt oder fehlender Brandschutz. |
| Quelle | PDF S. 210: Bodenplatte–Wand über Winkelverbinder; Hinweis, dass Winkelverbinder aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden müssen. |

### R-S04 — Bodenplatte ↔ Stütze über Edelstahldorn

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `NeubauBodenplatte` oder `ReuseBodenplatte` |
| Komponente B | `ReuseStuetze` |
| Konnektor A | `dornaufnahme` |
| Konnektor B | `dornanschluss` |
| Port A | `bodenplatte.dornzone_oben` |
| Port B | `stuetze.fuss_dornzone` |
| Repräsentation | Bodenplatte als Platte; Stütze als Linie/Stab mit Fußpunkt und Querschnitt |
| Wann läuft die Regel? | Wenn eine Stütze auf eine Bodenplatte gestellt und mit Edelstahldorn verbunden wird. |
| Benötigte Daten | Stützenachse, Stützenfußgeometrie, Punktlast, Dornposition, Bewehrungskarte, Betonfestigkeit, Exzentrizität, Randabstände, Schäden. |
| Regel | Der Dornanschluss muss zur Stützenachse passen, die Punktlast übertragen und in beiden Bauteilen eine bohrbare, bewehrungsfreie Zone treffen. |
| Ergebnis | PASS = Achse/Last/Bohrzone passen. WARNUNG = Exzentrizität oder Bewehrungsunsicherheit. FAIL = kritischer Bewehrungstreffer, fehlende Tragfähigkeit oder zu große Exzentrizität. |
| Quelle | PDF S. 211: Bodenplatte–Stütze über nachträglich montierten Edelstahldorn. |

### R-S05 — Bodenplatte ↔ Stütze über Winkelverbinder

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Brandschutz + Evidenz |
| Komponente A | `NeubauBodenplatte` oder `ReuseBodenplatte` |
| Komponente B | `ReuseStuetze` |
| Konnektor A | `winkelaufnahme` |
| Konnektor B | `winkelverbinderanschluss` |
| Port A | `bodenplatte.winkelzone_oben` |
| Port B | `stuetze.fuss_winkelzone` |
| Repräsentation | Bodenplatte als Platte; Stütze als Linie/Stab; Fußbodenaufbau als Schutzlayer |
| Wann läuft die Regel? | Wenn eine Stütze mit Winkelverbindern an eine Bodenplatte angeschlossen wird. |
| Benötigte Daten | Winkelposition, Befestigungspunkte, Punktlasten, Randabstände, Bewehrungskarte, Brandschutzabdeckung/Fußbodenaufbau, Schadenszonen. |
| Regel | Der Winkelanschluss darf nur PASS ergeben, wenn die Befestigungszonen tragfähig und brandschutztechnisch verdeckbar sind. |
| Ergebnis | PASS = tragfähige Befestigung + Abdeckung. WARNUNG = Brandschutz noch offen. FAIL = keine geeignete Winkelzone, Schaden, Bewehrungskonflikt oder fehlende Abdeckung. |
| Quelle | PDF S. 212: Bodenplatte–Stütze über Winkelverbinder; Winkelverbinder müssen aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden. |

### R-S06 — Wand ↔ Decke über nachträglichen Bewehrungsanschluss und Verguss

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseWand` |
| Komponente B | `ReuseDeckenplatte` oder `ReusePlattenfragment` |
| Konnektor A | `bewehrungsanschluss` |
| Konnektor B | `vergussaufnahme` |
| Port A | `wand.kopf_bewehrungszone` |
| Port B | `decke.unterseite_vergusszone` oder `decke.rand_vergusszone` |
| Repräsentation | Wand als Scheibe; Decke als Platte; Verbindung als Bewehrungs-/Vergussgraph |
| Wann läuft die Regel? | Wenn eine Decke an eine Wand über nachträglichen Bewehrungsanschluss und Verguss angebunden wird. |
| Benötigte Daten | Bewehrungslage, Bohr-/Injektionszonen, Verbundlänge, Fugenbreite, Vergussraum, Deckenreaktion, Wandtragfähigkeit, Toleranzen, Materialwerte. |
| Regel | Der Anschluss ist nur prüfbar, wenn eine eindeutige Bewehrungsanschlusszone und eine geometrisch ausreichende Vergusszone vorhanden sind und der Lastpfad Wand–Decke geschlossen ist. |
| Ergebnis | PASS = Bewehrung, Vergussfuge und Lastpfad belegt. WARNUNG = unvollständige Bewehrungskarte oder Toleranzrisiko. FAIL = keine Vergusszone, Bewehrungskonflikt oder fehlender Lastpfad. |
| Quelle | PDF S. 213: Wand–Decke über nachträglichen Bewehrungsanschluss und Verguss. |

### R-S07 — Wand ↔ Decke über Schraubanker mit Flachstahlhalter

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseWand` |
| Komponente B | `ReuseDeckenplatte` oder `ReusePlattenfragment` |
| Konnektor A | `schraubankeraufnahme` |
| Konnektor B | `flachstahlhalter_aufnahme` |
| Port A | `wand.kopf_ankerzone` |
| Port B | `decke.rand_ankerzone` |
| Repräsentation | Wand als Scheibe; Decke als Platte; Halter als Anschlussobjekt |
| Wann läuft die Regel? | Wenn eine Wand-Decke-Verbindung über Schraubanker und Flachstahlhalter modelliert wird. |
| Benötigte Daten | Ankerpunkte, Haltergeometrie, Randabstände, Bewehrungskarte, Deckenreaktion, Wandtragfähigkeit, Zug-/Schubkräfte, Schadenszonen. |
| Regel | Anker und Halter müssen auf beiden Bauteilen kompatible, bewehrungs- und schadensfreie Anschlusszonen treffen. |
| Ergebnis | PASS = beide Anschlusszonen frei und tragfähig. WARNUNG = Randabstand/Bewehrung unklar. FAIL = kein kompatibles Port-Paar oder Konflikt in der Ankerzone. |
| Quelle | PDF S. 214: Wand–Decke über Schraubanker mit Flachstahlhalter. |

### R-S08 — Stütze ↔ Decke über Edelstahldorn

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseStuetze` |
| Komponente B | `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Konnektor A | `dornanschluss` |
| Konnektor B | `dornaufnahme` |
| Port A | `stuetze.kopf_dornzone` |
| Port B | `decke.unterseite_dornzone` |
| Repräsentation | Stütze als Linie/Stab; Decke als Platte mit Punktauflagerzone |
| Wann läuft die Regel? | Wenn eine Decke oder ein Fragment über einen Edelstahldorn an eine Stütze angeschlossen wird. |
| Benötigte Daten | Stützenkopf, Deckenauflagerzone, Punktlast, Dornposition, Bewehrungslage, Betongüte, Exzentrizität, Schadenszonen. |
| Regel | Der Dorn muss in tragfähigen Zonen beider Bauteile liegen und die Last in der Stützenachse oder innerhalb zulässiger Exzentrizität übertragen. |
| Ergebnis | PASS = Achse, Zone und Materialwerte passen. WARNUNG = Exzentrizität knapp oder Bewehrung unsicher. FAIL = Bewehrungskonflikt, zu große Exzentrizität oder fehlende Druckfestigkeit. |
| Quelle | PDF S. 215: Stütze–Decke über nachträglich montierten Edelstahldorn. |

### R-S09 — Stütze ↔ Decke über Winkelverbinder

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Brandschutz + Evidenz |
| Komponente A | `ReuseStuetze` |
| Komponente B | `ReuseDeckenplatte` |
| Konnektor A | `winkelverbinderanschluss` |
| Konnektor B | `winkelaufnahme` |
| Port A | `stuetze.kopf_winkelzone` |
| Port B | `decke.unterseite_winkelzone` |
| Repräsentation | Stütze als Stab; Decke als Platte; Brandschutzbekleidung als Schutzlayer |
| Wann läuft die Regel? | Wenn eine Stütze-Decke-Verbindung über Winkelverbinder hergestellt wird. |
| Benötigte Daten | Winkelpositionen, Befestigungsmittel, Punktlasten, Randabstände, Bewehrungskarte, Brandschutzbekleidung, Schadenszonen. |
| Regel | Winkelverbinder müssen tragfähig befestigt und brandschutztechnisch bekleidet sein. |
| Ergebnis | PASS = Befestigung + Bekleidung erfüllt. WARNUNG = Brandschutzbekleidung fehlt im Modell. FAIL = ungeeignete Befestigungszone oder fehlende Brandschutzlösung. |
| Quelle | PDF S. 216: Stütze–Decke über Winkelverbinder; Winkelverbinder müssen mit Brandschutzbekleidung verdeckt werden. |

### R-S10 — ReUse-Stütze/Decke ↔ neuer Stahlbetonträger über Bewehrungsanschluss und Verguss

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseStuetze`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Komponente B | `NeubauStahlbetontraeger` |
| Konnektor A | `bewehrungsanschluss` |
| Konnektor B | `verguss_bewehrungsaufnahme` |
| Port A | `reuse_element.bewehrungszone` |
| Port B | `neuer_stahlbetontraeger.verguss_bewehrungszone` |
| Repräsentation | ReUse-Element als Platte/Stab/Fragment; neuer Träger als Balken mit Vergusszone |
| Wann läuft die Regel? | Wenn ein ReUse-Element auf oder an einen neuen Stahlbetonträger mit nachträglichem Bewehrungsanschluss und Verguss angebunden wird. |
| Benötigte Daten | Bewehrungsanschlusszone, Vergussfuge, Trägerauflager, Lasten, Toleranzen, Betonfestigkeit, Bewehrungskarte, Bohrzonen. |
| Regel | Der neue Träger muss als kompatibler Aufnahmepartner mit modellierter Verguss- und Bewehrungsanschlusszone vorhanden sein. |
| Ergebnis | PASS = beidseitige Anschlusszonen und Vergussfuge vorhanden. WARNUNG = Toleranz oder Bewehrung unklar. FAIL = kein kompatibler Trägerport oder Bohr-/Bewehrungskonflikt. |
| Quelle | PDF S. 217: Stütze–Decke über nachträglichen Bewehrungsanschluss und Verguss auf neu herzustellenden Stahlbetonträger. |

### R-S11 — Decke/Fragment ↔ Stahlträger über Auflager

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Brandschutz + Logistik |
| Komponente A | `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Komponente B | `Stahltraeger` |
| Konnektor A | `stahlauflager_nutzung` |
| Konnektor B | `stahlauflager_angebot` |
| Port A | `decke.auflagerkante_unten` oder `fragment.auflagerzone_unten` |
| Port B | `stahltraeger.obergurt_auflager` |
| Repräsentation | Decke/Fragment als Platte; Stahlträger als Linie/Balken mit Obergurtfläche |
| Wann läuft die Regel? | Wenn ein ReUse-Betonelement auf einem Stahlträger aufgelagert wird. |
| Benötigte Daten | Auflagerlänge, Kontaktfläche, Reaktionslast, Stahlträgertragfähigkeit, Ebenheit, Toleranz, Brandschutz des Stahlträgers, Elementmasse. |
| Regel | Das Auflager ist nur zulässig, wenn Auflagerfläche, Last, Toleranz und Trägerkapazität kompatibel sind. |
| Ergebnis | PASS = Last und Auflagergeometrie kompatibel. WARNUNG = Brandschutz/Toleranz noch offen. FAIL = zu geringe Auflagerfläche oder unzureichende Trägerkapazität. |
| Quelle | PDF S. 218: Stütze–Decke über Auflager auf Stahlträger, Beispiel Deltabeam. |

### R-S12 — Deckenplatte ↔ Wand als direktes Linienauflager

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseDeckenplatte` |
| Komponente B | `ReuseWand` oder `NeubauWand` |
| Konnektor A | `auflagerbedarf_linie` |
| Konnektor B | `auflagerangebot_linie` |
| Port A | `decke.auflagerkante_unten` |
| Port B | `wand.kopf_auflager` |
| Repräsentation | Decke als Platte mit Spannrichtung; Wand als Scheibe mit Kopfauflager |
| Wann läuft die Regel? | Wenn eine Decke auf einer Wand gelagert wird. |
| Benötigte Daten | Spannrichtung, Deckenreaktion, Auflagerlänge, Wandtragfähigkeit, Kontaktfläche, Ebenheit, Materialkennwerte, Schadenszonen. |
| Regel | Die Auflagerkante der Decke muss zur Wandkopfzone passen und die Deckenreaktion über eine ausreichende Kontaktfläche übertragen können. |
| Ergebnis | PASS = Auflagerlänge, Last und Evidenz passen. WARNUNG = Ebenheit/Toleranz unklar. FAIL = falsche Spannrichtung, fehlendes Auflager oder Schaden im Kontaktbereich. |
| Quelle | PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile. |

### R-S13 — Deckenplatte ↔ Stütze als Punktauflager

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Evidenz |
| Komponente A | `ReuseDeckenplatte` |
| Komponente B | `ReuseStuetze` oder `NeubauStuetze` |
| Konnektor A | `auflagerbedarf_punkt` |
| Konnektor B | `auflagerangebot_punkt` |
| Port A | `decke.auflagerpunkt_unten` |
| Port B | `stuetze.kopf_auflager` |
| Repräsentation | Decke als Platte; Stütze als Punkt-/Linienauflager mit Achse |
| Wann läuft die Regel? | Wenn eine Decke auf einer Stütze gelagert wird. |
| Benötigte Daten | Punktlast, Stützenkapazität, Kontaktzone, Exzentrizität, lokale Plattentragfähigkeit/Durchstanzrisiko, Bewehrungskarte, Schäden. |
| Regel | Punktauflager auf Stütze benötigt eine kompatible Kontaktzone und eine zulässige Exzentrizität. |
| Ergebnis | PASS = Achse, Kontakt und Last passen. WARNUNG = Durchstanz-/Exzentrizitätsprüfung unvollständig. FAIL = Kontaktzone zu klein, Exzentrizität zu groß oder Materialwerte fehlen. |
| Quelle | PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile. |

### R-S14 — Deckenplatte ↔ Deckenplatte über Fugenverbinder

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Semantik |
| Komponente A | `ReuseDeckenplatte` |
| Komponente B | `ReuseDeckenplatte` |
| Konnektor A | `fugenverbinder_angebot` |
| Konnektor B | `fugenverbinder_angebot` |
| Port A | `platte_A.fugenkante` |
| Port B | `platte_B.fugenkante` |
| Repräsentation | Beide Platten als Flächen mit Fugenkanten; Fuge als Linienobjekt |
| Wann läuft die Regel? | Wenn zwei Platten nebeneinander gefügt werden. |
| Benötigte Daten | Fugenkanten, Ebenheit, Höhenversatz, Fugenbreite, Verbinderart, Last-/Scheibenwirkung, Sichtstatus. |
| Regel | Bei Plattendecken muss ein Fugenverbinder gemäß Ausführungsplanung geometrisch möglich und bei sichtbaren Fugen gestalterisch kontrolliert sein. |
| Ergebnis | PASS = Fugenkanten passen und Verbinder möglich. WARNUNG = Höhenversatz oder Sichtfuge nicht gelöst. FAIL = Fuge zu groß/zu klein oder keine Verbinderzone. |
| Quelle | PDF S. 261: Bei Plattendecken sind Fugenverbinder gemäß Ausführungsplanung herzustellen. |

### R-S15 — ReUse-Tragwerk ↔ Aussteifungselement

| Feld | Inhalt |
|---|---|
| Paket | Tragwerk + Semantik |
| Komponente A | `ReuseDeckenplatte`, `ReuseWand`, `ReuseFragment_StuetzeDecke` |
| Komponente B | `Aussteifungselement` |
| Konnektor A | `aussteifungsbedarf` |
| Konnektor B | `aussteifungsangebot` |
| Port A | `reuse_element.aussteifungsbedarf` |
| Port B | `aussteifungselement.aussteifungsport` |
| Repräsentation | Tragwerk als Graph: Platten, Wände, Stützen, Kerne/Verbände |
| Wann läuft die Regel? | Wenn das neue Gebäude aus ReUse-Elementen nicht selbst ausreichend ausgesteift ist. |
| Benötigte Daten | Tragrolle jedes Elements, Scheiben-/Wandwirkung, horizontale Lasten, Gebäudehöhe, neue Kerne/Wände/Verbände, Anschlussfähigkeit. |
| Regel | Wenn ReUse-Elemente die Gebäudestabilität nicht selbst sichern, muss ein kompatibles aussteifendes Element im Tragwerksgraph vorhanden sein. |
| Ergebnis | PASS = Aussteifung geschlossen. WARNUNG = Aussteifungsmodell unvollständig. FAIL = fehlende oder nicht angeschlossene Aussteifung. |
| Quelle | PDF S. 206: Ggf. müssen neue aussteifende Elemente errichtet werden, um die wiederverwendeten Stahlbetonelemente auszusteifen. |

---

## 2.2 Energie — Hüll- und Schichtenregeln

### R-E01 — ReUse-Element ↔ Außenluft als thermische Grenze

| Feld | Inhalt |
|---|---|
| Paket | Energie |
| Komponente A | `ReuseWand`, `ReuseDeckenplatte` oder `ReuseDachplatte` |
| Komponente B | `Klima_Aussenluft` + `DaemmungLayer` |
| Konnektor A | `thermische_grenze` |
| Konnektor B | `u_wert_anforderung` / `daemmung_ergaenzung` |
| Port A | `bauteil.aussenflaeche` |
| Port B | `klima.aussenluft` und `daemmung.layer_innen_oder_aussen` |
| Repräsentation | Bauteil als Layer im U-Wert-Modell; Außenklima als Kontext |
| Wann läuft die Regel? | Wenn ein ReUse-Stahlbetonelement Teil der Außenwand oder einer außenluftberührten Hüllfläche wird. |
| Benötigte Daten | Bauteildicke, Wärmeleitfähigkeit λ, Rohdichte/Betonkennwerte, Schichtenaufbau, Dämmstoff, Dämmstärke, Ziel-U-Wert, Wärmeübergänge. |
| Regel | Kontakt zur Außenluft aktiviert eine U-Wert-Prüfung des gesamten Bauteils; fehlende oder zu geringe Dämmung erzeugt Warnung oder Fail. |
| Ergebnis | PASS = Ziel-U-Wert erreicht. WARNUNG = λ fehlt oder Dämmung nur angenommen. FAIL = U-Wert nicht erreichbar oder keine Dämmung modelliert. |
| Quelle | PDF S. 163–164: Bei Kontakt zu Außenklima muss der U-Wert bestimmt und mit Dämmung auf den geforderten Wert gebracht werden. |

### R-E02 — ReUse-Element ↔ Baugrund als thermische Grenze

| Feld | Inhalt |
|---|---|
| Paket | Energie + Bauphysik |
| Komponente A | `ReuseBodenplatte` oder `ReuseWand` im erdberührten Bereich |
| Komponente B | `Klima_Baugrund` + `DaemmungLayer` + `AbdichtungLayer` |
| Konnektor A | `thermische_grenze_erdberuehrt` |
| Konnektor B | `baugrund_u_wert_anforderung` |
| Port A | `bauteil.erdberuehrte_flaeche` |
| Port B | `klima.baugrund` / `daemmung.erdberuehrt` |
| Repräsentation | Bauteil als erdberührter Layer mit Feuchte-/Dämmdetail |
| Wann läuft die Regel? | Wenn ein ReUse-Betonbauteil gegen Baugrund eingesetzt wird. |
| Benötigte Daten | Dicke, λ, Dämmlage, Abdichtung, Feuchteschutzstatus, Ziel-U-Wert, Sockel-/Erdkontakt-Detail. |
| Regel | Erdberührte ReUse-Betonbauteile brauchen Wärmeschutz- und Abdichtungsmodell, bevor die Platzierung PASS ergeben darf. |
| Ergebnis | PASS = U-Wert und Abdichtung vollständig. WARNUNG = Feuchteschutz unvollständig. FAIL = keine thermische/feuchtebezogene Schichtlogik vorhanden. |
| Quelle | PDF S. 163–164: Wärmeschutz ist bei Kontakt zu Außenluft oder Baugrund besonders zu beachten. |

### R-E03 — ReUse-Dachplatte ↔ Dachaufbau

| Feld | Inhalt |
|---|---|
| Paket | Energie + TGA/Öffnungen |
| Komponente A | `ReuseDachplatte` oder `ReuseDeckenplatte` als Dach |
| Komponente B | `Dachaufbau` |
| Konnektor A | `dach_thermische_grenze` |
| Konnektor B | `dachaufbau_anschluss` |
| Port A | `dachplatte.dachflaeche` |
| Port B | `dachaufbau.daemmung_abdichtung` |
| Repräsentation | Dachplatte als Fläche; Dachaufbau als Layer Stack |
| Wann läuft die Regel? | Wenn ein ReUse-Betonelement als Dach oder Teil des Dachs verwendet wird. |
| Benötigte Daten | Dachaufbau, Abdichtung, Dämmung, λ, Ziel-U-Wert, Neigung, Durchdringungen, Tragzone. |
| Regel | Die Dachplatte muss mit Dachaufbau, Abdichtung und Dämmung als vollständiges Hüllbauteil modelliert sein. |
| Ergebnis | PASS = U-Wert + Abdichtung + Durchdringungszonen geklärt. WARNUNG = Dachform oder Durchdringungen offen. FAIL = unvollständiger Dachaufbau. |
| Quelle | PDF S. 207: Dachkonstruktion abhängig von Dachform, ggf. durch wiederverwendete Elemente beeinflusst; PDF S. 262: Dachaufbau und Durchführungen beachten. |

### R-E04 — Dämmungskante ↔ Dämmungskante thermische Kontinuität

| Feld | Inhalt |
|---|---|
| Paket | Energie |
| Komponente A | `DaemmungLayer` an ReUse-Bauteil A |
| Komponente B | `DaemmungLayer` an Bauteil B |
| Konnektor A | `thermische_kontinuitaet` |
| Konnektor B | `thermische_kontinuitaet` |
| Port A | `element_A.daemmungskante` |
| Port B | `element_B.daemmungskante` |
| Repräsentation | Dämmebene als Kanten-/Flächennetz |
| Wann läuft die Regel? | Wenn zwei Hüllbauteile aneinanderstoßen. |
| Benötigte Daten | Dämmungskanten, Versatz, Fugenbreite, Anschlussdetail, Material, Dämmebenenlage. |
| Regel | Dämmungskanten müssen sich geometrisch treffen; bei Unterbrechung entsteht eine Wärmebrückenwarnung. |
| Ergebnis | PASS = kontinuierliche Dämmebene. WARNUNG = Unterbrechung oder Versatz. FAIL = thermische Hülle nicht schließbar. |
| Quelle | PDF S. 163–164: ReUse-Beton in der Hülle muss mit Dämmung so ergänzt werden, dass der geforderte U-Wert erreicht wird. |

### R-E05 — Beton-Durchlaufzone ↔ Dämmebene Wärmebrücke

| Feld | Inhalt |
|---|---|
| Paket | Energie + Tragwerk |
| Komponente A | `ReuseWand`, `ReuseDeckenplatte`, `ReuseFragment_StuetzeDecke` |
| Komponente B | `DaemmungLayer` / `ThermischeHuelle` |
| Konnektor A | `waermebruecken_risiko` |
| Konnektor B | `daemmebene` |
| Port A | `betonbauteil.durchlaufzone` |
| Port B | `huelle.daemmebene` |
| Repräsentation | Betonquerschnitt im Schnittmodell; Dämmebene als Schichtfläche |
| Wann läuft die Regel? | Wenn ein Stahlbetonelement die Dämmebene durchstößt oder stark unterbricht. |
| Benötigte Daten | Betonquerschnitt, Lage zur Dämmebene, Dämmüberdeckung, Innen/Außen-Kontakt, Anschlussdetail. |
| Regel | Durchlaufender Beton an der thermischen Hülle erzeugt eine Wärmebrückenwarnung, bis ein Detail die Unterbrechung löst. |
| Ergebnis | WARNUNG = Wärmebrücke möglich. PASS = Detail mit durchgehender Dämmung vorhanden. FAIL = Ziel-U-Wert/Detail nicht nachweisbar. |
| Quelle | PDF S. 163–164: Bei Hüllbauteilen muss die Dämmung den U-Wert des gesamten Bauteils auf den geforderten Wert herabsenken. |

---

## 2.3 TGA / Öffnungen — Öffnungs- und Bohrzonenregeln

### R-T01 — TGA-Trasse ↔ bestehende Öffnung

| Feld | Inhalt |
|---|---|
| Paket | TGA / Öffnungen + Semantik |
| Komponente A | `TGA_Trasse` |
| Komponente B | `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Konnektor A | `oeffnung_nutzen` |
| Konnektor B | `bestandsoeffnung_angebot` |
| Port A | `tga_trasse.querschnitt` |
| Port B | `bauteil.bestandsoeffnung` |
| Repräsentation | Trasse als Volumen/Korridor; Öffnung als Rechteck/Polygon mit Tiefe |
| Wann läuft die Regel? | Wenn eine Leitungstrasse durch eine vorhandene Öffnung geführt werden soll. |
| Benötigte Daten | Öffnungsmaße, Trassenquerschnitt, Lage, Toleranz, Brandschutz-/Schallschutzstatus, Abdichtung, Raumfunktion. |
| Regel | Eine bestehende Öffnung darf genutzt werden, wenn die Trasse geometrisch passt und exakt zur Leitungsführung liegt. |
| Ergebnis | PASS = Öffnung passt. WARNUNG = Toleranz knapp oder Brandschutz offen. FAIL = Öffnung zu klein, falsch liegend oder funktional unpassend. |
| Quelle | PDF S. 207: ggf. Kernbohrungen oder Öffnungen in ReUse-Stahlbetonelementen für Kabeldurchführungen. |

### R-T02 — TGA-Trasse ↔ neue Kernbohrung / Bohrzone

| Feld | Inhalt |
|---|---|
| Paket | TGA / Öffnungen + Tragwerk + Evidenz |
| Komponente A | `TGA_Trasse` |
| Komponente B | `ReuseWand`, `ReuseDeckenplatte`, `ReuseStuetze` oder `ReuseBodenplatte` |
| Konnektor A | `kernbohrung_bedarf` |
| Konnektor B | `bohrzone_angebot` |
| Port A | `tga_trasse.bohrpunkt` |
| Port B | `bauteil.bohrzone` |
| Repräsentation | Bohrung als Zylinder; Bauteil als Volumen mit Bewehrungs- und Schadensoverlay |
| Wann läuft die Regel? | Wenn eine neue Kernbohrung oder Öffnung in ReUse-Beton geplant wird. |
| Benötigte Daten | Bohrdurchmesser, Bohrtiefe, Bewehrungskarte, Tragzonen, Randabstände, Materialfestigkeit, Schadenszonen, Toleranz. |
| Regel | Neue Bohrungen sind nur möglich, wenn keine kritische Bewehrung, keine Schadenszone und keine tragende Kernzone getroffen wird. |
| Ergebnis | PASS = freie Bohrzone. WARNUNG = Bewehrungsunsicherheit. FAIL = Bewehrungs-/Tragwerkskonflikt oder Schaden in Bohrzone. |
| Quelle | PDF S. 207 und S. 260–262: Öffnungen/Bohrungen und Leitungsführungen sind bei TGA und Rohbauarbeiten zu beachten. |

### R-T03 — Bodenplatte/Fundament ↔ Leitungsdurchführung

| Feld | Inhalt |
|---|---|
| Paket | TGA / Öffnungen + Energie/Bauphysik + Tragwerk |
| Komponente A | `TGA_Trasse` |
| Komponente B | `ReuseBodenplatte`, `NeubauBodenplatte` oder `NeubauFundament` |
| Konnektor A | `leitungsdurchfuehrung_bedarf` |
| Konnektor B | `durchfuehrung_angebot` |
| Port A | `leitung.trasse` |
| Port B | `bodenplatte.durchfuehrung` oder `fundament.durchfuehrung` |
| Repräsentation | Leitung als Korridor; Bodenplatte/Fundament als Platte/Volumen mit Öffnung und Abdichtung |
| Wann läuft die Regel? | Wenn Leitungen durch Bodenplatte oder Fundamentbereich geführt werden. |
| Benötigte Daten | Durchführungsposition, Leitungsachse, Öffnungsmaß, Dichtung, Abdichtung, Bauteildicke, Bewehrungskarte, Sockel-/Erdkontakt. |
| Regel | Leitungsdurchführungen müssen in Bauteil- und Anschlussplanung berücksichtigt sein und dürfen Tragwerk, Abdichtung und Dämmung nicht verletzen. |
| Ergebnis | PASS = Durchdringung, Abdichtung und Tragwerk kompatibel. WARNUNG = Abdichtung/Bewehrung offen. FAIL = keine Durchführung oder Konflikt mit Trag-/Abdichtungszone. |
| Quelle | PDF S. 260–261: Fundamente und Bodenplatten müssen Leitungsdurchführungen beachten bzw. herstellen. |

### R-T04 — Dachplatte/Dachaufbau ↔ Dach-Durchdringung

| Feld | Inhalt |
|---|---|
| Paket | TGA / Öffnungen + Energie/Bauphysik + Tragwerk |
| Komponente A | `TGA_Trasse` oder `PV_Solar_Blitzschutz_Element` |
| Komponente B | `ReuseDachplatte` + `Dachaufbau` |
| Konnektor A | `dach_durchdringung_bedarf` |
| Konnektor B | `dach_durchdringung_angebot` |
| Port A | `tga_pv_blitzschutz.durchdringungspunkt` |
| Port B | `dach.bauteil_durchdringung` |
| Repräsentation | Dachplatte als Fläche; Dachaufbau als Layer; Durchdringung als Zylinder/Objekt |
| Wann läuft die Regel? | Wenn Abwasserentlüftung, PV/Solarthermie oder Blitzschutz durch/auf dem Dach vorgesehen wird. |
| Benötigte Daten | Öffnungsposition, Leitungs-/Bauteildurchmesser, Abdichtung, Dachaufbau, Dämmung, Tragzone, Gefälle, Feuchteschutz. |
| Regel | Dach-Durchdringungen müssen mit Dachaufbau, Abdichtung, Dämmung und Tragwerkszone kompatibel sein. |
| Ergebnis | PASS = vollständiges Durchdringungsdetail. WARNUNG = Abdichtung/Dämmung noch offen. FAIL = Konflikt mit Tragzone oder keine Abdichtung. |
| Quelle | PDF S. 262: Dach benötigt Auflagerprüfung, Dachaufbau und Durchführungen für Abwasserentlüftung, PV/Solarthermie und Blitzschutz. |

---

## 2.4 Semantik / Architektur — Raster, Fugen, Sicht und Nutzung

### R-A01 — ReUse-Element ↔ Gebäuderaster

| Feld | Inhalt |
|---|---|
| Paket | Semantik / Architektur + Tragwerk |
| Komponente A | `ReuseDeckenplatte`, `ReuseWand`, `ReuseUnterzug` oder `ReuseFragment_StuetzeDecke` |
| Komponente B | `Gebaeuderaster` |
| Konnektor A | `rasterbindung` |
| Konnektor B | `raster_achse` |
| Port A | `element.rasterkante` |
| Port B | `gebaeuderaster.achse` |
| Repräsentation | Element als Bounding Box/Kantenmodell; Raster als Achsnetz |
| Wann läuft die Regel? | Wenn ein Pool-Element in ein Neubauraster gesetzt wird. |
| Benötigte Daten | Elementbreite, Achsraster, Toleranz, Elementfamilie, Anschlussports, Spannrichtung. |
| Regel | Elementbreiten und Anschlusskanten sollen das Neubauraster unterstützen; große Abweichungen erzeugen Warnung oder erfordern Rasteranpassung. |
| Ergebnis | PASS = Achspassung. WARNUNG = Abweichung mit Anpassungsvorschlag. FAIL = Rasterkonflikt erzeugt unlösbaren Tragwerks-/Portkonflikt. |
| Quelle | PDF S. 100–101: Elementbreite soll möglichst ein festes Raster bilden; Elemente werden auf der Grundrissskizze platziert und iterativ abgeglichen. |

### R-A02 — ReUse-Element ↔ ReUse-Element Fugenflucht

| Feld | Inhalt |
|---|---|
| Paket | Semantik / Architektur + Tragwerk |
| Komponente A | `ReuseDeckenplatte` oder `ReuseWand` |
| Komponente B | `ReuseDeckenplatte` oder `ReuseWand` |
| Konnektor A | `fugenbild_angebot` |
| Konnektor B | `fugenbild_angebot` |
| Port A | `element_A.fugenkante` |
| Port B | `element_B.fugenkante` |
| Repräsentation | Kantenmodell mit Sichtstatus und Fugenbreite |
| Wann läuft die Regel? | Wenn zwei sichtbare oder konstruktive Kanten verbunden werden. |
| Benötigte Daten | Fugenkanten, Höhenlage, Versatz, Fugenbreite, sichtbarer Status, Verbinderbedarf. |
| Regel | Fugen sollten fluchten oder als bewusstes Detail markiert sein; unbeabsichtigter Versatz erzeugt Warnung. |
| Ergebnis | PASS = Flucht oder bewusstes Detail. WARNUNG = unbeabsichtigter Versatz. FAIL = Versatz kollidiert mit Tragwerksanschluss. |
| Quelle | PDF S. 100–101: Elemente werden iterativ mit Entwurf und Verbindungsanforderungen abgeglichen. |

### R-A03 — ReUse-Sichtfläche ↔ Raumseite

| Feld | Inhalt |
|---|---|
| Paket | Semantik / Architektur + Evidenz |
| Komponente A | `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Komponente B | `Raumfunktion` / `Raumseite` |
| Konnektor A | `sichtflaeche_angebot` |
| Konnektor B | `sichtflaeche_bedarf` |
| Port A | `element.sichtflaeche` |
| Port B | `raum.ansichtsseite` |
| Repräsentation | Oberfläche als orientierte Fläche mit Schadens-/Reparaturoverlay |
| Wann läuft die Regel? | Wenn eine bestehende Betonfläche sichtbar bleiben soll. |
| Benötigte Daten | Sichtseite, Flächennormalen, Oberflächenzustand, Risse, Abplatzungen, Reparaturen, gewünschte Raumseite. |
| Regel | Sichtflächen müssen korrekt orientiert und über Evidenzstatus bewertet sein. |
| Ergebnis | PASS = richtige Orientierung und akzeptabler Zustand. WARNUNG = Schaden/Reparatur sichtbar. FAIL = falsche Orientierung oder nicht akzeptabler sichtbarer Schaden. |
| Quelle | PDF S. 75–80: Schäden, Risse, Abplatzungen und Oberflächenveränderungen sind zu begutachten. |

### R-A04 — bestehende Öffnung ↔ Raumfunktion

| Feld | Inhalt |
|---|---|
| Paket | Semantik / Architektur + TGA/Öffnungen + Tragwerk |
| Komponente A | `ReuseWand` oder `ReuseDeckenplatte` |
| Komponente B | `Raumfunktion` |
| Konnektor A | `bestandsoeffnung_angebot` |
| Konnektor B | `oeffnung_bedarf` |
| Port A | `element.bestandsoeffnung` |
| Port B | `raumfunktion.tuer_fenster_tga` |
| Repräsentation | Öffnung als Polygon/Volumen; Raumfunktion als Nutzungsanforderung |
| Wann läuft die Regel? | Wenn eine bestehende Öffnung als Tür, Fenster oder TGA-Durchführung genutzt werden soll. |
| Benötigte Daten | Öffnungsmaß, Brüstung/Lage, Orientierung, Raumfunktion, TGA-Route, Tragwerksfreigabe, Brandschutz/Schallschutz. |
| Regel | Eine vorhandene Öffnung darf semantisch nur genutzt werden, wenn Maße, Lage, Funktion und technische Anforderungen zusammenpassen. |
| Ergebnis | PASS = Öffnung passt zur Funktion. WARNUNG = Anpassung/Brandschutz offen. FAIL = Maß/Lage/Funktion unvereinbar. |
| Quelle | PDF S. 129–131: Bauteilkatalog soll Öffnungsmaße enthalten; PDF S. 207: Öffnungen können für Durchführungen relevant werden. |

---

## 2.5 Logistik / Montage — Transport, Lager, Heben, Einbau

### R-L01 — Bauteil ↔ Standardtransport-Hülle

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Transportmittel` / `StandardtransportLimit` |
| Konnektor A | `transportfaehigkeit` |
| Konnektor B | `transportkapazitaet` |
| Port A | `komponente.transport_bbox` |
| Port B | `transport.standardlimit` |
| Repräsentation | Bounding Box des Bauteils; Transportlimit als Hüllkörper |
| Wann läuft die Regel? | Wenn ein Element in eine Transportfuhre eingeplant wird. |
| Benötigte Daten | Länge, Breite, Höhe, Transportmittel, Sondertransportstatus, Gewicht. |
| Regel | Standardtransport-Passung: Länge ≤ 13 m, Breite ≤ 3 m, Höhe ≤ 3 m. |
| Ergebnis | PASS = innerhalb Limit. WARNUNG = außerhalb Limit, Sondertransport nötig. FAIL = Transportmittel kann Hülle nicht aufnehmen. |
| Quelle | PDF S. 97–100: Elemente sollten Transportmaße mitdenken; 13 m Länge, 3 m Höhe, 3 m Breite werden genannt. |

### R-L02 — Bauteilmasse ↔ Fahrzeugnutzlast

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | beliebige Pool-Komponente oder Fuhrenliste |
| Komponente B | `Transportmittel` |
| Konnektor A | `transportmasse` |
| Konnektor B | `nutzlastangebot` |
| Port A | `komponente.masse_port` |
| Port B | `fahrzeug.nutzlast` |
| Repräsentation | Masse als Skalar; Fuhre als Liste/Graph |
| Wann läuft die Regel? | Wenn eine Transportfuhre zusammengestellt wird. |
| Benötigte Daten | Elementmasse, Fahrzeugnutzlast, Ladekombination, Schwerpunkt, Ladungssicherung. |
| Regel | Summe der Massen darf Fahrzeug- und Ladungssicherungslogik nicht überschreiten. |
| Ergebnis | PASS = Masse innerhalb Nutzlast. WARNUNG = Schwerpunkt/Ladungssicherung offen. FAIL = Nutzlast überschritten. |
| Quelle | PDF S. 129–131: Bauteilkatalog enthält Volumen und Masse; PDF S. 235–236: Transportfuhren sollen richtig beladen und zeitlich abgestimmt sein. |

### R-L03 — Bauteil-Hebeport ↔ Kranhaken

| Feld | Inhalt |
|---|---|
| Paket | Logistik + Tragwerk + Evidenz |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Kran` |
| Konnektor A | `hebeanschluss` |
| Konnektor B | `kran_hubangebot` |
| Port A | `komponente.hebeport` |
| Port B | `kran.haken` |
| Repräsentation | Bauteil als Volumen mit Schwerpunkt; Kran als Last-Radius-Modell |
| Wann läuft die Regel? | Wenn ein Element gehoben oder montiert wird. |
| Benötigte Daten | Masse, Hebepunkte, Anschlagmittel, Schwerpunkt, Kranlasttabelle, Reichweite, Schadenszonen an Hebepunkten. |
| Regel | Hebepunkte und Kran müssen die Elementmasse an der geplanten Position aufnehmen können. |
| Ergebnis | PASS = Kranlast und Hebepunkte ausreichend. WARNUNG = Schwerpunkt/Hebepunkte unsicher. FAIL = Krantragfähigkeit überschritten oder Hebeport beschädigt. |
| Quelle | PDF S. 123–126: Krantragkraft hängt von Position, Auslegerlänge, Höhenlage und Winkel ab. |

### R-L04 — Montageposition ↔ Kranreichweite

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Kran` |
| Konnektor A | `montageposition_bedarf` |
| Konnektor B | `kranreichweite_angebot` |
| Port A | `komponente.montageposition` |
| Port B | `kran.stellplatz_ausleger` |
| Repräsentation | Montageort als Punkt/Volumen; Kran als Radius-Höhen-Last-Modell |
| Wann läuft die Regel? | Wenn eine Montageposition gewählt wird. |
| Benötigte Daten | Kranstandort, Auslegerlänge, Radius, Höhe, Last, Gelände/Platz, Elementmasse. |
| Regel | Krantragfähigkeit wird positionsabhängig geprüft; zu großer Radius oder zu hohe Last erzeugt Warnung/Fail. |
| Ergebnis | PASS = Last am Radius zulässig. WARNUNG = knappe Reserve. FAIL = Last/Radium/Höhe außerhalb Kranbereich. |
| Quelle | PDF S. 123–126: Kranlastkapazität variiert stark nach Lastposition und Krantyp. |

### R-L05 — Bauteil ↔ Lagerorientierung

| Feld | Inhalt |
|---|---|
| Paket | Logistik + Evidenz |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Lagerplatz` |
| Konnektor A | `lagerlage_bedarf` |
| Konnektor B | `lagerregel_angebot` |
| Port A | `komponente.lager_orientierung` |
| Port B | `lagerplatz.lagerregel` |
| Repräsentation | Bauteil mit ursprünglicher Einbaulage; Lager als Stell-/Liegeposition |
| Wann läuft die Regel? | Wenn ein Element im Lager platziert wird. |
| Benötigte Daten | Elementtyp, ursprüngliche Einbaulage, geplante Lagerlage, Auflagerpunkte, Schadensrisiko. |
| Regel | Decken liegend lagern; Wände und Stützen stehend lagern, wenn möglich entsprechend ursprünglicher Lastfälle. |
| Ergebnis | PASS = Lagerung entspricht Regel. WARNUNG = abweichende Lagerung mit Nachweis nötig. FAIL = abweichende Lagerung ohne Nachweis und Schadensrisiko. |
| Quelle | PDF S. 186: Elemente sollten möglichst in gleicher Ausrichtung wie im Bestandsgebäude gelagert werden; Decken liegend, Wände/Stützen stehend. |

### R-L06 — Bauteil ↔ Witterungsschutz im Lager

| Feld | Inhalt |
|---|---|
| Paket | Logistik + Evidenz |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Lagerplatz` |
| Konnektor A | `witterungsempfindlichkeit` |
| Konnektor B | `witterungsschutz_angebot` |
| Port A | `komponente.witterungsrisiko` |
| Port B | `lagerplatz.schutzstatus` |
| Repräsentation | Bauteil mit Riss-/Öffnungszonen; Lager als Schutzstatus |
| Wann läuft die Regel? | Wenn ein Element gelagert wird. |
| Benötigte Daten | Risse/Öffnungen, Niederschlagsschutz, Frostperiode, Feuchtestatus, Karbonatisierungsrisiko. |
| Regel | Bei Rissen/Öffnungen und freier Bewitterung erzeugt der Checker Frost-/Karbonatisierungswarnung. |
| Ergebnis | PASS = Schutz vorhanden. WARNUNG = freie Bewitterung. FAIL = kritischer Schaden plus fehlender Schutz. |
| Quelle | PDF S. 185–186: Witterungsschutz erhält Zustand; Regenwasser in Rissen/Öffnungen kann Frostsprengungen verursachen; Feuchte kann Karbonatisierung beschleunigen. |

### R-L07 — Bauteilkontakt ↔ Lagerholz

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Lagerplatz` / `Lagerholz` |
| Konnektor A | `lagerkontakt` |
| Konnektor B | `schutzauflage` |
| Port A | `komponente.transport_auflagepunkt` oder `kontaktflaeche` |
| Port B | `lagerholz.auflage` |
| Repräsentation | Kontaktflächen als Punkte/Linien/Flächen; Lagerholz als Schutzkörper |
| Wann läuft die Regel? | Wenn Elemente gestapelt oder nebeneinander gelagert werden. |
| Benötigte Daten | Lagerhölzer, Kontaktflächen, Stapelposition, Elementtyp, Elementmasse. |
| Regel | Elemente müssen durch schützende Lagerhölzer getrennt werden, damit Kontaktbeschädigungen vermieden werden. |
| Ergebnis | PASS = Lagerhölzer korrekt. WARNUNG = Lagerholzposition unvollständig. FAIL = direkter schädigender Bauteilkontakt. |
| Quelle | PDF S. 186: Elemente sollen voneinander durch schützende Lagerhölzer getrennt werden. |

### R-L08 — Lagerposition ↔ Einbaureihenfolge

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Montageplan` / `Lagerplatz` |
| Konnektor A | `einbauzeit_bedarf` |
| Konnektor B | `lagerzugriff_angebot` |
| Port A | `komponente.id` / `komponente.montageport` |
| Port B | `lagerplatz.stapelposition` / `montageplan.reihenfolge` |
| Repräsentation | Element-ID in Liste; Lager als Graph/Stapel |
| Wann läuft die Regel? | Wenn Lagerplan oder Stapelplan erstellt wird. |
| Benötigte Daten | Montagefolge, Element-ID, Lagerposition, Stapelreihenfolge, Entnahmerichtung. |
| Regel | Lagerposition muss zur späteren Einbaureihenfolge passen, damit kein unnötiges Umstapeln entsteht. |
| Ergebnis | PASS = Zugriff in Reihenfolge möglich. WARNUNG = Umstapeln nötig. FAIL = Element nicht rechtzeitig erreichbar. |
| Quelle | PDF S. 185: Lagerplan soll Positionen entsprechend späterer Einbaureihenfolge vorsehen. |

### R-L09 — Transportfuhre ↔ Montagezeitfenster

| Feld | Inhalt |
|---|---|
| Paket | Logistik |
| Komponente A | `Transportmittel` mit Elementliste |
| Komponente B | `Montageplan` / `Baustelle` |
| Konnektor A | `lieferung_angebot` |
| Konnektor B | `montagezeitfenster_bedarf` |
| Port A | `transport.fuhre` |
| Port B | `baustelle.montagezeitfenster` |
| Repräsentation | Fuhre als Liste von IDs; Montageplan als Zeitachse |
| Wann läuft die Regel? | Wenn Transportfuhren geplant werden. |
| Benötigte Daten | Bauzeitplan, Montagezeitpunkt, Baustellenlagerfläche, Element-IDs, Beladung, Entladefolge. |
| Regel | Transporte sollen die jeweils benötigten Elemente zum richtigen Zeitpunkt bringen und zugleich optimal beladen sein, ohne unnötige Baustellenzwischenlagerung. |
| Ergebnis | PASS = Lieferung passt zur Montage. WARNUNG = Zwischenlagerung/Umstapeln nötig. FAIL = Element fehlt im Zeitfenster oder Baustelle kann Fuhre nicht aufnehmen. |
| Quelle | PDF S. 235–236: Bauzeitplan und Logistik müssen die Einbaureihenfolge berücksichtigen; Fuhren sollen richtige Elemente zum richtigen Zeitpunkt bringen und optimal beladen sein. |

### R-L10 — Bauteil ↔ Zielposition / Anschlussvorbereitung

| Feld | Inhalt |
|---|---|
| Paket | Logistik + Tragwerk + Semantik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | Zielposition im Neubau, z. B. `NeubauFundament`, `Wand`, `Stuetze`, `Traeger`, `Decke` |
| Konnektor A | `montagebereitschaft` |
| Konnektor B | `anschlussvorbereitung` |
| Port A | `komponente.montageport` |
| Port B | `zielposition.anschlussvorbereitung` |
| Repräsentation | Bauteil mit Ports; Zielposition mit vorbereitetem Anschlussdetail |
| Wann läuft die Regel? | Direkt vor Platzierung im Neubau oder bei digitaler Montageprüfung. |
| Benötigte Daten | Anschlussdetails, Auflager, Verbinder, Toleranzen, Öffnungen, Ist-Maße, Freigaben, Schadensstatus. |
| Regel | Montage darf nur PASS ergeben, wenn Zielposition, Anschlussdetail, Toleranz und Elementfreigabe zusammenpassen. |
| Ergebnis | PASS = montagebereit. WARNUNG = Toleranz/Freigabe offen. FAIL = Anschluss nicht vorbereitet, falsche Maße oder ungeklärter Schaden. |
| Quelle | PDF S. 260–262: Rohbauarbeiten verlangen Anschlüsse, Auflager und Leitungsdurchführungen je Bauteil; Schäden vor Einbau müssen begutachtet und aufgearbeitet werden. |

---

## 2.6 Evidenz-Overlay — Regeln, die andere Verbindungen überschreiben oder abwerten

Diese Regeln sind keine eigenen baulichen Verbindungen. Sie laufen als Overlay über alle aktiven Ports und Konnektoren. Ein Tragwerks-PASS kann durch Evidenz zu WARNUNG oder FAIL werden.

### R-V01 — aktiver Port ↔ Schadenszone

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + betroffenes Paket |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | aktiver Anschluss-/Nutzungskontext |
| Konnektor A | `schadensueberlagerung` |
| Konnektor B | `port_freigabe` |
| Port A | `komponente.schadenszone` |
| Port B | `aktiver_port.zone` |
| Repräsentation | Schadenspolygone auf Geometrie; Portzone als Einflussbereich |
| Wann läuft die Regel? | Bei jeder Verbindung, deren Port in oder nahe einer Schadenszone liegt. |
| Benötigte Daten | Schadenspolygone, Risse, Abplatzungen, Korrosion, Portlage, Einflussradius, Reparaturstatus. |
| Regel | Schäden in Anschluss-, Auflager-, Bohr- oder Sichtzonen reduzieren die Freigabe des Ports. |
| Ergebnis | PASS = kein Schaden. WARNUNG = Schaden nahe Port oder unkritisch. FAIL = Schaden im tragenden Kontakt-/Bohrbereich. |
| Quelle | PDF S. 75–80: Qualität, Schäden, Risse, Abplatzungen, Korrosion und Instandsetzungen sind zu begutachten. |

### R-V02 — tragender Port ↔ Riss/Korrosionsrisiko

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Tragwerk |
| Komponente A | beliebige tragende Pool-Komponente |
| Komponente B | aktiver Tragwerksanschluss |
| Konnektor A | `riss_korrosionsrisiko` |
| Konnektor B | `tragender_port` |
| Port A | `komponente.risszone` |
| Port B | `tragender_port.zone` |
| Repräsentation | Risslinie/Polygon mit Breite; Portzone als Bereich |
| Wann läuft die Regel? | Wenn ein tragender Port in einem gerissenen Bereich liegt. |
| Benötigte Daten | Rissbreite, Rissursache, Abplatzung, Feuchte, Korrosionsprüfung, Bewehrungslage. |
| Regel | Risse über 0,3 mm oder signifikante Abplatzungen verlangen Korrosionsausschluss vor tragender Wiederverwendung. |
| Ergebnis | WARNUNG = Nachweis fehlt. PASS = Korrosion ausgeschlossen. FAIL = Korrosion nicht ausgeschlossen oder bestätigt. |
| Quelle | PDF S. 76: Bei Rissen über 0,3 mm und signifikanten Abplatzungen muss sichergestellt werden, dass Bewehrung nicht korrodiert ist. |

### R-V03 — Port ↔ Korrosionsstatus

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Tragwerk |
| Komponente A | beliebige tragende Pool-Komponente |
| Komponente B | aktiver Anschluss |
| Konnektor A | `korrosionsnachweis` |
| Konnektor B | `anschlussfreigabe` |
| Port A | `bewehrung.korrosionsstatus` |
| Port B | `tragender_port.freigabe` |
| Repräsentation | Korrosionsstatus als Attribut/Overlay auf Bewehrung |
| Wann läuft die Regel? | Wenn Korrosionsverdacht besteht oder ein Port Riss-/Feuchtezonen berührt. |
| Benötigte Daten | Potentialmessung, Freilegung, Korrosionsbefund, Reparaturstatus, Prüfdatum. |
| Regel | Tragende Verbindung darf nur PASS sein, wenn Korrosion im relevanten Bereich ausgeschlossen oder behoben ist. |
| Ergebnis | PASS = ausgeschlossen/repariert. WARNUNG = Verdacht ungeklärt. FAIL = aktive/ungeklärte Korrosion im Anschlussbereich. |
| Quelle | PDF S. 76–77: Korrosion kann über Potentialmessung oder partielles Freilegen überprüft werden. |

### R-V04 — Karbonatisierungstiefe ↔ Betondeckung

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Tragwerk + Logistik |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | aktiver Tragwerks- oder Lager-/Hüllkontext |
| Konnektor A | `karbonatisierungsrisiko` |
| Konnektor B | `port_dauerhaftigkeit` |
| Port A | `komponente.karbonatisierungstiefe` |
| Port B | `komponente.betondeckung` / `aktiver_port.zone` |
| Repräsentation | Karbonatisierungsfront als Tiefe; Betondeckung als Bewehrungsattribut |
| Wann läuft die Regel? | Wenn ein Element tragend, feuchte-/witterungsrelevant oder in der Hülle eingesetzt wird. |
| Benötigte Daten | Karbonatisierungstiefe, Betondeckung, Feuchte-/Lagerstatus, Bewehrungslage, Korrosionsstatus. |
| Regel | Wenn Karbonatisierung bis zur Bewehrung reicht oder nahe daran liegt, wird der Port abgewertet. |
| Ergebnis | PASS = ausreichender Abstand. WARNUNG = geringe Reserve. FAIL = Karbonatisierung erreicht Bewehrung und Korrosion ist nicht ausgeschlossen. |
| Quelle | PDF S. 77–78: Karbonatisierung senkt den Korrosionsschutz; Karbonatisierungstiefe wird per Phenolphthalein-Indikatortest bestimmt. |

### R-V05 — Tragwerksanschluss ↔ Materialkennwerte

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Tragwerk |
| Komponente A | tragende Pool-Komponente |
| Komponente B | aktiver Tragwerksanschluss |
| Konnektor A | `materialkennwert_sicherheit` |
| Konnektor B | `tragwerksanschluss` |
| Port A | `materialpruefung` |
| Port B | `tragwerksanschluss` |
| Repräsentation | Materialwerte als Attributpaket pro Bauteil/Zone |
| Wann läuft die Regel? | Vor jedem tragenden Anschluss, Auflager, Bohr-/Anker- oder Dornanschluss. |
| Benötigte Daten | Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chloridgehalt, Schadstoffstatus, Prüfmethode, Prüfdatum. |
| Regel | Tragende Checks dürfen Materialwerte nur nutzen, wenn sie als element- oder zonenbezogene Prüfwerte vorliegen. |
| Ergebnis | PASS = belegte Werte. WARNUNG = Werte teilweise angenommen. FAIL = fehlende Druckfestigkeit oder fehlende Mindestinformation in Anschlusszone. |
| Quelle | PDF S. 78–80: Bohrkerne sollen u. a. Chlorid, Schadstoffe, Druck-/Zugfestigkeit, E-Modul und Dichte bestimmen; Rückprallwerte sollen mit Bohrkernen abgeglichen werden. |

### R-V06 — Bohr-/Anker-/Dornzone ↔ Bewehrungskarte

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Tragwerk + TGA/Öffnungen |
| Komponente A | beliebige Pool-Komponente mit Bohr-/Anker-/Dornzone |
| Komponente B | aktiver Connector: Schraubanker, Dorn, Bewehrungsanschluss oder Kernbohrung |
| Konnektor A | `bewehrungskonflikt` |
| Konnektor B | `bohr_anker_dorn_bedarf` |
| Port A | `bauteil.bewehrungskarte` |
| Port B | `bohrzone` / `ankerzone` / `dornzone` / `bewehrungszone` |
| Repräsentation | Bewehrung als Linien-/Rasteroverlay; Bohr-/Ankerzone als Volumen |
| Wann läuft die Regel? | Bei Kernbohrungen, Schraubankern, Dornen und nachträglichen Bewehrungsanschlüssen. |
| Benötigte Daten | Bewehrungslage, Stabdurchmesser, Betondeckung, Ortungsunsicherheit, Bohrdurchmesser, Bohrtoleranz, Tragzonen. |
| Regel | Bohr-, Anker- und Dornzonen dürfen keine kritische Bewehrung treffen. |
| Ergebnis | PASS = Zone frei. WARNUNG = Bewehrung unsicher. FAIL = kritischer Bewehrungskonflikt. |
| Quelle | PDF S. 79–84: Bewehrungslage, Betondeckung, Durchmesser und Abstände sind zu untersuchen; Ortungsverfahren werden beschrieben. |

### R-V07 — Sichtfläche ↔ Oberflächenzustand

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Semantik / Architektur |
| Komponente A | Pool-Komponente mit sichtbarer Oberfläche |
| Komponente B | `Raumseite` / `Sichtanforderung` |
| Konnektor A | `oberflaechen_evidenz` |
| Konnektor B | `sichtflaechenanforderung` |
| Port A | `element.sichtflaeche` / `oberflaechenzustand` |
| Port B | `raum.ansichtsseite` |
| Repräsentation | Sichtfläche als orientierte Fläche; Schaden/Reparatur als Overlay |
| Wann läuft die Regel? | Wenn eine Betonfläche sichtbar bleiben soll. |
| Benötigte Daten | Oberflächenzustand, Risse, Abplatzungen, Reparaturen, Verfärbungen, gewünschte Sichtqualität. |
| Regel | Sichtbarer Schaden erzeugt eine architektonische Warnung, auch wenn Tragwerk PASS ist. |
| Ergebnis | PASS = Zustand akzeptiert. WARNUNG = sichtbarer Schaden/Reparatur. FAIL = sichtbare Seite falsch orientiert oder Anforderung nicht erfüllbar. |
| Quelle | PDF S. 75–80: Oberflächenveränderungen, Schäden, Risse und Instandsetzungen sind visuell zu begutachten. |

### R-V08 — Bauteil nach Transport/Lagerung ↔ Montagefreigabe

| Feld | Inhalt |
|---|---|
| Paket | Evidenz + Logistik + Tragwerk |
| Komponente A | beliebige Pool-Komponente |
| Komponente B | `Montageplan` / Zielanschluss |
| Konnektor A | `transport_lagerschaden` |
| Konnektor B | `montagefreigabe` |
| Port A | `komponente.schadensstatus_nach_transport` |
| Port B | `komponente.montageport` |
| Repräsentation | Schadensstatus als Versionsstand vor Einbau |
| Wann läuft die Regel? | Direkt vor Montage nach Transport oder Lagerung. |
| Benötigte Daten | Schadensprüfung, Fotos, Riss-/Abplatzungsstatus, Reparaturstatus, Freigabe, betroffene Ports. |
| Regel | Neu erkannte Schäden vor Einbau müssen begutachtet, eingeschätzt und ggf. aufgearbeitet werden. |
| Ergebnis | PASS = Freigabe nach Begutachtung. WARNUNG = unkritischer Schaden dokumentiert. FAIL = ungeklärter Schaden in Anschluss-/Tragzone. |
| Quelle | PDF S. 262: Werden vor Einbau Schäden aus Zwischenlagerung oder Transport festgestellt, müssen diese begutachtet, eingeschätzt und aufgearbeitet werden. |

---

# 3. Umsetzung als maschinenlesbares Regelobjekt

Beispiel für R-S06:

```yaml
id: R-S06
name: Wand-Decke über Bewehrungsanschluss und Verguss
packages: [Tragwerk, Evidenz]
components:
  A: ReuseWand
  B: ReuseDeckenplatte|ReusePlattenfragment
representations:
  A: wall_plate
  B: slab_plate
connectors:
  A: bewehrungsanschluss
  B: vergussaufnahme
ports:
  A: wand.kopf_bewehrungszone
  B: decke.unterseite_vergusszone|decke.rand_vergusszone
trigger: user_connects_ports
required_data:
  - bewehrungslage
  - bohr_injektionszonen
  - verbundlaenge
  - fugenbreite
  - vergussraum
  - deckenreaktion
  - wandtragfaehigkeit
  - toleranzen
  - materialwerte
checks:
  - both_ports_exist
  - connector_roles_compatible
  - rebar_zone_free_or_approved
  - grout_zone_geometrically_sufficient
  - load_path_closed
  - evidence_overlay_passes
result:
  pass: Anschlusszone, Vergussfuge und Lastpfad belegt
  warning: Bewehrungskarte oder Toleranz unvollständig
  fail: keine Vergusszone, Bewehrungskonflikt oder fehlender Lastpfad
source: PDF S. 213
```

---

# 4. Was bewusst nicht übernommen wurde

Nicht übernommen, weil es im aktuellen Design-Rule-Checker kein direktes Port-zu-Port-Ergebnis erzeugt:

- Rückbau- und Abbruchstatik des Spendergebäudes.
- Betonsäge- und Entnahmesequenzen.
- Abbruchanzeige, Bauvoranfrage, ZiE/vBG als Behördenprozess.
- Ausschreibung, Vergabe, Vertrags- und Gewährleistungsregeln.
- Kostenaufteilung zwischen Spender- und Neubauprojekt.
- Abfallrecht, Entsorgung, Schadstoffrückbau.
- Vollständige LCA-/CO₂-Bilanz als Anschlussregel.
- Allgemeine Gebäudezertifizierung.

