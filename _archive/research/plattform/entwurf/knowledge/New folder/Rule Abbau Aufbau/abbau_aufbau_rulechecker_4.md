# Abbau Aufbau — Paketstruktur für konkrete Regelprüfungen

Diese Datei sortiert die konkrete Regelmatrix in die sechs Pakete deines Systems. Die Sortierung folgt einer **Datenhoheit**: Die Regel liegt dort, wo der aktive Konnektor fachlich geprüft wird. Andere Pakete werden nur als Datenquellen gelesen.

**Systemannahme:** Der Rückbau ist abgeschlossen. Der Pool enthält dokumentierte Komponenten mit Paketen, Repräsentationen, Konnektoren, Ports und Evidenzdaten. Rückbau-, Abbruch-, Ausschreibungs-, Kosten- und Behördenregeln sind ausgeschlossen.

**Korrigierte Zählung:** Die konkrete Detailmatrix enthält **46 direkt prüfbare Regeln**. In einer vorherigen Kurzantwort war die Zahl 38 zu niedrig; diese Paketfassung korrigiert das.

---

## 1. Paketlogik / Datenhoheit

| Paket | Regel liegt hier, wenn … | eigene Daten im Komponentenpaket | typische gelesene Zusatzpakete |
|---|---|---|---|
| **Structural** | der aktive Konnektor Last, Auflager, Anker, Dorn, Verguss, Bewehrungsanschluss, Tragfähigkeit oder Aussteifung prüft | Tragwerksrepräsentation, Lastpfad, Portrollen, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen | Evidence; bei Bedarf Semantic oder Logistics |
| **Energy** | der aktive Konnektor thermische Grenze, Dämmebene, U-Wert, Schichtaufbau oder Wärmebrücke prüft | thermische Boundary Surfaces, Layer Stack, Dämmebene, U-Wert, Wärmebrückenzonen | Evidence, TGA/Openings, Semantic |
| **TGA / Openings** | der aktive Konnektor bestehende Öffnungen, neue Bohrungen, Durchführungen oder Trassenkorridore prüft | Öffnungsgeometrie, Bohrzone, Durchmesser, Trassenbedarf, Nutzung | Evidence, Structural, Energy |
| **Semantic / Architectural** | der aktive Konnektor Raster, Fugenbild, Sichtfläche, Raumfunktion oder architektonische Passung prüft | Rasterlinien, Sichtseiten, Raumfunktionsports, Fugenbild, Orientierung | Evidence, Structural, TGA/Openings |
| **Logistics** | der aktive Konnektor Transport, Heben, Lagerung, Montage, Sequenz oder Kran-/Fahrzeug-Kontext prüft | BBox, Masse, Hebepunkte, Lagerlage, Montageposition, Kran/Fahrzeug, Zeitfenster | Evidence, Structural, Semantic |
| **Evidence** | eine Portzone durch Bewehrung, Schaden, Riss, Korrosion, Karbonatisierung, Materialwert oder Unsicherheit bewertet wird | Schadenszonen, Risse, Bewehrungskarte, Materialprüfungen, Betondeckung, Karbonatisierung, Korrosionsstatus | das jeweils betroffene Paket |

**Wichtige Entscheidung:** Evidence ist kein Sammelpaket für alle Regeln mit Nachweisbezug. Ein tragender Dornanschluss bleibt eine `Structural`-Regel. `Evidence` liefert nur Overlay-Daten, die `PASS` zu `WARNUNG` oder `FAIL` abwerten können.

---

## 2. Ausführungsreihenfolge im Checker

1. Ausgewählte Komponenten und Ports lesen.
2. Port-Kompatibilität im zuständigen Primärpaket prüfen.
3. Konnektortyp bestimmen.
4. Primärregel des Pakets ausführen.
5. Relevante `Evidence`-Overlays auf dieselben Portzonen anwenden.
6. Wenn Platzierung, Lieferung, Heben oder Einbau betroffen sind, `Logistics` als nachgelagerte Freigabe prüfen.
7. Ergebnis als `PASS`, `WARNUNG` oder `FAIL` zurückgeben.

---

## 3. Regeln nach korrektem Primärpaket


## Structural

**Anzahl Regeln:** 15


### R-S01 — Fundament ↔ Bodenplatte über Schraubanker

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `NeubauFundament` ↔ `ReuseBodenplatte` oder `NeubauBodenplatte` |
| Konnektoren | `schraubankeraufnahme` ↔ `schraubankeranschluss` |
| Ports | `fundament.ankerzone_oben` ↔ `bodenplatte.ankerzone_unten` |
| Repräsentation | Fundament als Volumen/Auflagerfläche; Bodenplatte als Platte mit Ankerzonen |
| Wann läuft die Regel? | Wenn eine Bodenplatte auf einem Fundament über Schraubanker fixiert werden soll. |
| Daten nach Paket | **Structural:** Komponenten `NeubauFundament` ↔ `ReuseBodenplatte` oder `NeubauBodenplatte`; Konnektoren `schraubankeraufnahme` ↔ `schraubankeranschluss`; Ports `fundament.ankerzone_oben` ↔ `bodenplatte.ankerzone_unten`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Ankerpositionen, Betonfestigkeit beider Zonen, Betondeckung, Bewehrungskarte, Randabstände, Ankerlasten, Schadenszonen. |
| Prüfregel | Der Anschluss darf nur PASS ergeben, wenn beide Ankerzonen vorhanden sind, keine kritische Bewehrung oder Schadenszone getroffen wird und die Lasten durch den Schraubankeranschluss abgetragen werden können. |
| Resultat | PASS = Zonen frei und Nachweise vorhanden. WARNUNG = Bewehrungslage unsicher oder Materialwerte teilweise angenommen. FAIL = fehlende Ankerzone, Bewehrungskonflikt, Schaden im Anschlussbereich oder fehlende Tragfähigkeit. |
| Quelle | PDF S. 208: Fundament–Bodenplatte, Befestigung mit Schraubankern; PDF S. 129–131: Bauteilkatalog mit ID, Maßen, Masse und Prüferweiterungen. |

### R-S02 — Bodenplatte ↔ Wand über Edelstahldorne

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand` |
| Konnektoren | `dornaufnahme` ↔ `dornanschluss` |
| Ports | `bodenplatte.dornzone_oben` ↔ `wand.fuss_dornzone` |
| Repräsentation | Bodenplatte als Platte; Wand als Scheibe mit Fußkante und Achse |
| Wann läuft die Regel? | Wenn eine Wand auf eine Bodenplatte gestellt und über nachträglich montierte Edelstahldorne gehalten wird. |
| Daten nach Paket | **Structural:** Komponenten `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand`; Konnektoren `dornaufnahme` ↔ `dornanschluss`; Ports `bodenplatte.dornzone_oben` ↔ `wand.fuss_dornzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Dornpositionen, Bohrzonen, Bewehrungskarte, Wandlast, Wandachse, Betongüte, Einbindetiefe, Randabstände, Schaden/Risse im Fußbereich. |
| Prüfregel | Dornpositionen müssen zur Wandachse passen, in beiden Bauteilen in freigegebenen Bohrzonen liegen und dürfen keine kritische Bewehrung treffen. |
| Resultat | PASS = Achse, Bohrzone, Tragfähigkeit und Evidenz passen. WARNUNG = Bewehrung unsicher oder Randabstand knapp. FAIL = Bohrung trifft Bewehrung, Wandachse/Port versetzt, fehlender Materialnachweis. |
| Quelle | PDF S. 209: Bodenplatte–Wand, Befestigung über nachträglich montierte Edelstahldorne. |

### R-S03 — Bodenplatte ↔ Wand über Winkelverbinder

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand` |
| Konnektoren | `winkelaufnahme` ↔ `winkelverbinderanschluss` |
| Ports | `bodenplatte.winkelzone_oben` ↔ `wand.fuss_winkelzone` |
| Repräsentation | Bodenplatte als Platte; Wand als Scheibe; Fußbodenaufbau als Brandschutz-/Abdecklayer |
| Wann läuft die Regel? | Wenn Wand und Bodenplatte mit Winkelverbindern verbunden werden. |
| Daten nach Paket | **Structural:** Komponenten `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseWand`; Konnektoren `winkelaufnahme` ↔ `winkelverbinderanschluss`; Ports `bodenplatte.winkelzone_oben` ↔ `wand.fuss_winkelzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Winkelpositionen, Befestigungsmittel, Bewehrungskarte, Randabstände, Lasten, Fußbodenaufbau/Brandschutzabdeckung, Schadenszonen. |
| Prüfregel | Winkelverbinder sind nur zulässig, wenn beide Befestigungszonen tragfähig sind und der Verbinder brandschutztechnisch verdeckt oder bekleidet werden kann. |
| Resultat | PASS = Tragwerk und Brandschutzabdeckung erfüllt. WARNUNG = Brandschutzlayer noch nicht modelliert. FAIL = keine Befestigungszone, Bewehrungskonflikt oder fehlender Brandschutz. |
| Quelle | PDF S. 210: Bodenplatte–Wand über Winkelverbinder; Hinweis, dass Winkelverbinder aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden müssen. |

### R-S04 — Bodenplatte ↔ Stütze über Edelstahldorn

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze` |
| Konnektoren | `dornaufnahme` ↔ `dornanschluss` |
| Ports | `bodenplatte.dornzone_oben` ↔ `stuetze.fuss_dornzone` |
| Repräsentation | Bodenplatte als Platte; Stütze als Linie/Stab mit Fußpunkt und Querschnitt |
| Wann läuft die Regel? | Wenn eine Stütze auf eine Bodenplatte gestellt und mit Edelstahldorn verbunden wird. |
| Daten nach Paket | **Structural:** Komponenten `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze`; Konnektoren `dornaufnahme` ↔ `dornanschluss`; Ports `bodenplatte.dornzone_oben` ↔ `stuetze.fuss_dornzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Stützenachse, Stützenfußgeometrie, Punktlast, Dornposition, Bewehrungskarte, Betonfestigkeit, Exzentrizität, Randabstände, Schäden. |
| Prüfregel | Der Dornanschluss muss zur Stützenachse passen, die Punktlast übertragen und in beiden Bauteilen eine bohrbare, bewehrungsfreie Zone treffen. |
| Resultat | PASS = Achse/Last/Bohrzone passen. WARNUNG = Exzentrizität oder Bewehrungsunsicherheit. FAIL = kritischer Bewehrungstreffer, fehlende Tragfähigkeit oder zu große Exzentrizität. |
| Quelle | PDF S. 211: Bodenplatte–Stütze über nachträglich montierten Edelstahldorn. |

### R-S05 — Bodenplatte ↔ Stütze über Winkelverbinder

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze` |
| Konnektoren | `winkelaufnahme` ↔ `winkelverbinderanschluss` |
| Ports | `bodenplatte.winkelzone_oben` ↔ `stuetze.fuss_winkelzone` |
| Repräsentation | Bodenplatte als Platte; Stütze als Linie/Stab; Fußbodenaufbau als Schutzlayer |
| Wann läuft die Regel? | Wenn eine Stütze mit Winkelverbindern an eine Bodenplatte angeschlossen wird. |
| Daten nach Paket | **Structural:** Komponenten `NeubauBodenplatte` oder `ReuseBodenplatte` ↔ `ReuseStuetze`; Konnektoren `winkelaufnahme` ↔ `winkelverbinderanschluss`; Ports `bodenplatte.winkelzone_oben` ↔ `stuetze.fuss_winkelzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Winkelposition, Befestigungspunkte, Punktlasten, Randabstände, Bewehrungskarte, Brandschutzabdeckung/Fußbodenaufbau, Schadenszonen. |
| Prüfregel | Der Winkelanschluss darf nur PASS ergeben, wenn die Befestigungszonen tragfähig und brandschutztechnisch verdeckbar sind. |
| Resultat | PASS = tragfähige Befestigung + Abdeckung. WARNUNG = Brandschutz noch offen. FAIL = keine geeignete Winkelzone, Schaden, Bewehrungskonflikt oder fehlende Abdeckung. |
| Quelle | PDF S. 212: Bodenplatte–Stütze über Winkelverbinder; Winkelverbinder müssen aus Brandschutzgründen durch den Fußbodenaufbau verdeckt werden. |

### R-S06 — Wand ↔ Decke über nachträglichen Bewehrungsanschluss und Verguss

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment` |
| Konnektoren | `bewehrungsanschluss` ↔ `vergussaufnahme` |
| Ports | `wand.kopf_bewehrungszone` ↔ `decke.unterseite_vergusszone` oder `decke.rand_vergusszone` |
| Repräsentation | Wand als Scheibe; Decke als Platte; Verbindung als Bewehrungs-/Vergussgraph |
| Wann läuft die Regel? | Wenn eine Decke an eine Wand über nachträglichen Bewehrungsanschluss und Verguss angebunden wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment`; Konnektoren `bewehrungsanschluss` ↔ `vergussaufnahme`; Ports `wand.kopf_bewehrungszone` ↔ `decke.unterseite_vergusszone` oder `decke.rand_vergusszone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Bewehrungslage, Bohr-/Injektionszonen, Verbundlänge, Fugenbreite, Vergussraum, Deckenreaktion, Wandtragfähigkeit, Toleranzen, Materialwerte. |
| Prüfregel | Der Anschluss ist nur prüfbar, wenn eine eindeutige Bewehrungsanschlusszone und eine geometrisch ausreichende Vergusszone vorhanden sind und der Lastpfad Wand–Decke geschlossen ist. |
| Resultat | PASS = Bewehrung, Vergussfuge und Lastpfad belegt. WARNUNG = unvollständige Bewehrungskarte oder Toleranzrisiko. FAIL = keine Vergusszone, Bewehrungskonflikt oder fehlender Lastpfad. |
| Quelle | PDF S. 213: Wand–Decke über nachträglichen Bewehrungsanschluss und Verguss. |

### R-S07 — Wand ↔ Decke über Schraubanker mit Flachstahlhalter

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment` |
| Konnektoren | `schraubankeraufnahme` ↔ `flachstahlhalter_aufnahme` |
| Ports | `wand.kopf_ankerzone` ↔ `decke.rand_ankerzone` |
| Repräsentation | Wand als Scheibe; Decke als Platte; Halter als Anschlussobjekt |
| Wann läuft die Regel? | Wenn eine Wand-Decke-Verbindung über Schraubanker und Flachstahlhalter modelliert wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReusePlattenfragment`; Konnektoren `schraubankeraufnahme` ↔ `flachstahlhalter_aufnahme`; Ports `wand.kopf_ankerzone` ↔ `decke.rand_ankerzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Ankerpunkte, Haltergeometrie, Randabstände, Bewehrungskarte, Deckenreaktion, Wandtragfähigkeit, Zug-/Schubkräfte, Schadenszonen. |
| Prüfregel | Anker und Halter müssen auf beiden Bauteilen kompatible, bewehrungs- und schadensfreie Anschlusszonen treffen. |
| Resultat | PASS = beide Anschlusszonen frei und tragfähig. WARNUNG = Randabstand/Bewehrung unklar. FAIL = kein kompatibles Port-Paar oder Konflikt in der Ankerzone. |
| Quelle | PDF S. 214: Wand–Decke über Schraubanker mit Flachstahlhalter. |

### R-S08 — Stütze ↔ Decke über Edelstahldorn

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseStuetze` ↔ `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Konnektoren | `dornanschluss` ↔ `dornaufnahme` |
| Ports | `stuetze.kopf_dornzone` ↔ `decke.unterseite_dornzone` |
| Repräsentation | Stütze als Linie/Stab; Decke als Platte mit Punktauflagerzone |
| Wann läuft die Regel? | Wenn eine Decke oder ein Fragment über einen Edelstahldorn an eine Stütze angeschlossen wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseStuetze` ↔ `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke`; Konnektoren `dornanschluss` ↔ `dornaufnahme`; Ports `stuetze.kopf_dornzone` ↔ `decke.unterseite_dornzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Stützenkopf, Deckenauflagerzone, Punktlast, Dornposition, Bewehrungslage, Betongüte, Exzentrizität, Schadenszonen. |
| Prüfregel | Der Dorn muss in tragfähigen Zonen beider Bauteile liegen und die Last in der Stützenachse oder innerhalb zulässiger Exzentrizität übertragen. |
| Resultat | PASS = Achse, Zone und Materialwerte passen. WARNUNG = Exzentrizität knapp oder Bewehrung unsicher. FAIL = Bewehrungskonflikt, zu große Exzentrizität oder fehlende Druckfestigkeit. |
| Quelle | PDF S. 215: Stütze–Decke über nachträglich montierten Edelstahldorn. |

### R-S09 — Stütze ↔ Decke über Winkelverbinder

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseStuetze` ↔ `ReuseDeckenplatte` |
| Konnektoren | `winkelverbinderanschluss` ↔ `winkelaufnahme` |
| Ports | `stuetze.kopf_winkelzone` ↔ `decke.unterseite_winkelzone` |
| Repräsentation | Stütze als Stab; Decke als Platte; Brandschutzbekleidung als Schutzlayer |
| Wann läuft die Regel? | Wenn eine Stütze-Decke-Verbindung über Winkelverbinder hergestellt wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseStuetze` ↔ `ReuseDeckenplatte`; Konnektoren `winkelverbinderanschluss` ↔ `winkelaufnahme`; Ports `stuetze.kopf_winkelzone` ↔ `decke.unterseite_winkelzone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Winkelpositionen, Befestigungsmittel, Punktlasten, Randabstände, Bewehrungskarte, Brandschutzbekleidung, Schadenszonen. |
| Prüfregel | Winkelverbinder müssen tragfähig befestigt und brandschutztechnisch bekleidet sein. |
| Resultat | PASS = Befestigung + Bekleidung erfüllt. WARNUNG = Brandschutzbekleidung fehlt im Modell. FAIL = ungeeignete Befestigungszone oder fehlende Brandschutzlösung. |
| Quelle | PDF S. 216: Stütze–Decke über Winkelverbinder; Winkelverbinder müssen mit Brandschutzbekleidung verdeckt werden. |

### R-S10 — ReUse-Stütze/Decke ↔ neuer Stahlbetonträger über Bewehrungsanschluss und Verguss

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseStuetze`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `NeubauStahlbetontraeger` |
| Konnektoren | `bewehrungsanschluss` ↔ `verguss_bewehrungsaufnahme` |
| Ports | `reuse_element.bewehrungszone` ↔ `neuer_stahlbetontraeger.verguss_bewehrungszone` |
| Repräsentation | ReUse-Element als Platte/Stab/Fragment; neuer Träger als Balken mit Vergusszone |
| Wann läuft die Regel? | Wenn ein ReUse-Element auf oder an einen neuen Stahlbetonträger mit nachträglichem Bewehrungsanschluss und Verguss angebunden wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseStuetze`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `NeubauStahlbetontraeger`; Konnektoren `bewehrungsanschluss` ↔ `verguss_bewehrungsaufnahme`; Ports `reuse_element.bewehrungszone` ↔ `neuer_stahlbetontraeger.verguss_bewehrungszone`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Bewehrungsanschlusszone, Vergussfuge, Trägerauflager, Lasten, Toleranzen, Betonfestigkeit, Bewehrungskarte, Bohrzonen. |
| Prüfregel | Der neue Träger muss als kompatibler Aufnahmepartner mit modellierter Verguss- und Bewehrungsanschlusszone vorhanden sein. |
| Resultat | PASS = beidseitige Anschlusszonen und Vergussfuge vorhanden. WARNUNG = Toleranz oder Bewehrung unklar. FAIL = kein kompatibler Trägerport oder Bohr-/Bewehrungskonflikt. |
| Quelle | PDF S. 217: Stütze–Decke über nachträglichen Bewehrungsanschluss und Verguss auf neu herzustellenden Stahlbetonträger. |

### R-S11 — Decke/Fragment ↔ Stahlträger über Auflager

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `Stahltraeger` |
| Konnektoren | `stahlauflager_nutzung` ↔ `stahlauflager_angebot` |
| Ports | `decke.auflagerkante_unten` oder `fragment.auflagerzone_unten` ↔ `stahltraeger.obergurt_auflager` |
| Repräsentation | Decke/Fragment als Platte; Stahlträger als Linie/Balken mit Obergurtfläche |
| Wann läuft die Regel? | Wenn ein ReUse-Betonelement auf einem Stahlträger aufgelagert wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `Stahltraeger`; Konnektoren `stahlauflager_nutzung` ↔ `stahlauflager_angebot`; Ports `decke.auflagerkante_unten` oder `fragment.auflagerzone_unten` ↔ `stahltraeger.obergurt_auflager`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Auflagerlänge, Kontaktfläche, Reaktionslast, Stahlträgertragfähigkeit, Ebenheit, Toleranz, Brandschutz des Stahlträgers, Elementmasse. |
| Prüfregel | Das Auflager ist nur zulässig, wenn Auflagerfläche, Last, Toleranz und Trägerkapazität kompatibel sind. |
| Resultat | PASS = Last und Auflagergeometrie kompatibel. WARNUNG = Brandschutz/Toleranz noch offen. FAIL = zu geringe Auflagerfläche oder unzureichende Trägerkapazität. |
| Quelle | PDF S. 218: Stütze–Decke über Auflager auf Stahlträger, Beispiel Deltabeam. |

### R-S12 — Deckenplatte ↔ Wand als direktes Linienauflager

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte` ↔ `ReuseWand` oder `NeubauWand` |
| Konnektoren | `auflagerbedarf_linie` ↔ `auflagerangebot_linie` |
| Ports | `decke.auflagerkante_unten` ↔ `wand.kopf_auflager` |
| Repräsentation | Decke als Platte mit Spannrichtung; Wand als Scheibe mit Kopfauflager |
| Wann läuft die Regel? | Wenn eine Decke auf einer Wand gelagert wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseDeckenplatte` ↔ `ReuseWand` oder `NeubauWand`; Konnektoren `auflagerbedarf_linie` ↔ `auflagerangebot_linie`; Ports `decke.auflagerkante_unten` ↔ `wand.kopf_auflager`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Spannrichtung, Deckenreaktion, Auflagerlänge, Wandtragfähigkeit, Kontaktfläche, Ebenheit, Materialkennwerte, Schadenszonen. |
| Prüfregel | Die Auflagerkante der Decke muss zur Wandkopfzone passen und die Deckenreaktion über eine ausreichende Kontaktfläche übertragen können. |
| Resultat | PASS = Auflagerlänge, Last und Evidenz passen. WARNUNG = Ebenheit/Toleranz unklar. FAIL = falsche Spannrichtung, fehlendes Auflager oder Schaden im Kontaktbereich. |
| Quelle | PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile. |

### R-S13 — Deckenplatte ↔ Stütze als Punktauflager

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte` ↔ `ReuseStuetze` oder `NeubauStuetze` |
| Konnektoren | `auflagerbedarf_punkt` ↔ `auflagerangebot_punkt` |
| Ports | `decke.auflagerpunkt_unten` ↔ `stuetze.kopf_auflager` |
| Repräsentation | Decke als Platte; Stütze als Punkt-/Linienauflager mit Achse |
| Wann läuft die Regel? | Wenn eine Decke auf einer Stütze gelagert wird. |
| Daten nach Paket | **Structural:** Komponenten `ReuseDeckenplatte` ↔ `ReuseStuetze` oder `NeubauStuetze`; Konnektoren `auflagerbedarf_punkt` ↔ `auflagerangebot_punkt`; Ports `decke.auflagerpunkt_unten` ↔ `stuetze.kopf_auflager`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Punktlast, Stützenkapazität, Kontaktzone, Exzentrizität, lokale Plattentragfähigkeit/Durchstanzrisiko, Bewehrungskarte, Schäden. |
| Prüfregel | Punktauflager auf Stütze benötigt eine kompatible Kontaktzone und eine zulässige Exzentrizität. |
| Resultat | PASS = Achse, Kontakt und Last passen. WARNUNG = Durchstanz-/Exzentrizitätsprüfung unvollständig. FAIL = Kontaktzone zu klein, Exzentrizität zu groß oder Materialwerte fehlen. |
| Quelle | PDF S. 260–262: Decken benötigen Überprüfung der Auflager und Anschlüsse an vertikale Bauteile. |

### R-S14 — Deckenplatte ↔ Deckenplatte über Fugenverbinder

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte` ↔ `ReuseDeckenplatte` |
| Konnektoren | `fugenverbinder_angebot` ↔ `fugenverbinder_angebot` |
| Ports | `platte_A.fugenkante` ↔ `platte_B.fugenkante` |
| Repräsentation | Beide Platten als Flächen mit Fugenkanten; Fuge als Linienobjekt |
| Wann läuft die Regel? | Wenn zwei Platten nebeneinander gefügt werden. |
| Daten nach Paket | **Structural:** Komponenten `ReuseDeckenplatte` ↔ `ReuseDeckenplatte`; Konnektoren `fugenverbinder_angebot` ↔ `fugenverbinder_angebot`; Ports `platte_A.fugenkante` ↔ `platte_B.fugenkante`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Fugenkanten, Ebenheit, Höhenversatz, Fugenbreite, Verbinderart, Last-/Scheibenwirkung, Sichtstatus. |
| Prüfregel | Bei Plattendecken muss ein Fugenverbinder gemäß Ausführungsplanung geometrisch möglich und bei sichtbaren Fugen gestalterisch kontrolliert sein. |
| Resultat | PASS = Fugenkanten passen und Verbinder möglich. WARNUNG = Höhenversatz oder Sichtfuge nicht gelöst. FAIL = Fuge zu groß/zu klein oder keine Verbinderzone. |
| Quelle | PDF S. 261: Bei Plattendecken sind Fugenverbinder gemäß Ausführungsplanung herzustellen. |

### R-S15 — ReUse-Tragwerk ↔ Aussteifungselement

**Regel liegt im Paket:** `Structural`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte`, `ReuseWand`, `ReuseFragment_StuetzeDecke` ↔ `Aussteifungselement` |
| Konnektoren | `aussteifungsbedarf` ↔ `aussteifungsangebot` |
| Ports | `reuse_element.aussteifungsbedarf` ↔ `aussteifungselement.aussteifungsport` |
| Repräsentation | Tragwerk als Graph: Platten, Wände, Stützen, Kerne/Verbände |
| Wann läuft die Regel? | Wenn das neue Gebäude aus ReUse-Elementen nicht selbst ausreichend ausgesteift ist. |
| Daten nach Paket | **Structural:** Komponenten `ReuseDeckenplatte`, `ReuseWand`, `ReuseFragment_StuetzeDecke` ↔ `Aussteifungselement`; Konnektoren `aussteifungsbedarf` ↔ `aussteifungsangebot`; Ports `reuse_element.aussteifungsbedarf` ↔ `aussteifungselement.aussteifungsport`; Tragwerksrepräsentation, Lastpfad, Auflager-/Anschlussgeometrie, Kräfte, Randabstände, Toleranzen.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Tragrolle jedes Elements, Scheiben-/Wandwirkung, horizontale Lasten, Gebäudehöhe, neue Kerne/Wände/Verbände, Anschlussfähigkeit. |
| Prüfregel | Wenn ReUse-Elemente die Gebäudestabilität nicht selbst sichern, muss ein kompatibles aussteifendes Element im Tragwerksgraph vorhanden sein. |
| Resultat | PASS = Aussteifung geschlossen. WARNUNG = Aussteifungsmodell unvollständig. FAIL = fehlende oder nicht angeschlossene Aussteifung. |
| Quelle | PDF S. 206: Ggf. müssen neue aussteifende Elemente errichtet werden, um die wiederverwendeten Stahlbetonelemente auszusteifen. |

## Energy

**Anzahl Regeln:** 5


### R-E01 — ReUse-Element ↔ Außenluft als thermische Grenze

**Regel liegt im Paket:** `Energy`  
**Liest Daten aus:** `Energy`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand`, `ReuseDeckenplatte` oder `ReuseDachplatte` ↔ `Klima_Aussenluft` + `DaemmungLayer` |
| Konnektoren | `thermische_grenze` ↔ `u_wert_anforderung` / `daemmung_ergaenzung` |
| Ports | `bauteil.aussenflaeche` ↔ `klima.aussenluft` und `daemmung.layer_innen_oder_aussen` |
| Repräsentation | Bauteil als Layer im U-Wert-Modell; Außenklima als Kontext |
| Wann läuft die Regel? | Wenn ein ReUse-Stahlbetonelement Teil der Außenwand oder einer außenluftberührten Hüllfläche wird. |
| Daten nach Paket | **Energy:** Thermische Flächen/Schichten; Konnektoren `thermische_grenze` ↔ `u_wert_anforderung` / `daemmung_ergaenzung`; Ports `bauteil.aussenflaeche` ↔ `klima.aussenluft` und `daemmung.layer_innen_oder_aussen`; Boundary-Typ, Layer Stack, Dämmebene, U-Wert, Wärmebrücke.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Bauteildicke, Wärmeleitfähigkeit λ, Rohdichte/Betonkennwerte, Schichtenaufbau, Dämmstoff, Dämmstärke, Ziel-U-Wert, Wärmeübergänge. |
| Prüfregel | Kontakt zur Außenluft aktiviert eine U-Wert-Prüfung des gesamten Bauteils; fehlende oder zu geringe Dämmung erzeugt Warnung oder Fail. |
| Resultat | PASS = Ziel-U-Wert erreicht. WARNUNG = λ fehlt oder Dämmung nur angenommen. FAIL = U-Wert nicht erreichbar oder keine Dämmung modelliert. |
| Quelle | PDF S. 163–164: Bei Kontakt zu Außenklima muss der U-Wert bestimmt und mit Dämmung auf den geforderten Wert gebracht werden. |

### R-E02 — ReUse-Element ↔ Baugrund als thermische Grenze

**Regel liegt im Paket:** `Energy`  
**Liest Daten aus:** `Energy`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseBodenplatte` oder `ReuseWand` im erdberührten Bereich ↔ `Klima_Baugrund` + `DaemmungLayer` + `AbdichtungLayer` |
| Konnektoren | `thermische_grenze_erdberuehrt` ↔ `baugrund_u_wert_anforderung` |
| Ports | `bauteil.erdberuehrte_flaeche` ↔ `klima.baugrund` / `daemmung.erdberuehrt` |
| Repräsentation | Bauteil als erdberührter Layer mit Feuchte-/Dämmdetail |
| Wann läuft die Regel? | Wenn ein ReUse-Betonbauteil gegen Baugrund eingesetzt wird. |
| Daten nach Paket | **Energy:** Thermische Flächen/Schichten; Konnektoren `thermische_grenze_erdberuehrt` ↔ `baugrund_u_wert_anforderung`; Ports `bauteil.erdberuehrte_flaeche` ↔ `klima.baugrund` / `daemmung.erdberuehrt`; Boundary-Typ, Layer Stack, Dämmebene, U-Wert, Wärmebrücke. |
| Minimal benötigte Rohdaten | Dicke, λ, Dämmlage, Abdichtung, Feuchteschutzstatus, Ziel-U-Wert, Sockel-/Erdkontakt-Detail. |
| Prüfregel | Erdberührte ReUse-Betonbauteile brauchen Wärmeschutz- und Abdichtungsmodell, bevor die Platzierung PASS ergeben darf. |
| Resultat | PASS = U-Wert und Abdichtung vollständig. WARNUNG = Feuchteschutz unvollständig. FAIL = keine thermische/feuchtebezogene Schichtlogik vorhanden. |
| Quelle | PDF S. 163–164: Wärmeschutz ist bei Kontakt zu Außenluft oder Baugrund besonders zu beachten. |

### R-E03 — ReUse-Dachplatte ↔ Dachaufbau

**Regel liegt im Paket:** `Energy`  
**Liest Daten aus:** `Energy`, `TGA / Openings`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDachplatte` oder `ReuseDeckenplatte` als Dach ↔ `Dachaufbau` |
| Konnektoren | `dach_thermische_grenze` ↔ `dachaufbau_anschluss` |
| Ports | `dachplatte.dachflaeche` ↔ `dachaufbau.daemmung_abdichtung` |
| Repräsentation | Dachplatte als Fläche; Dachaufbau als Layer Stack |
| Wann läuft die Regel? | Wenn ein ReUse-Betonelement als Dach oder Teil des Dachs verwendet wird. |
| Daten nach Paket | **Energy:** Thermische Flächen/Schichten; Konnektoren `dach_thermische_grenze` ↔ `dachaufbau_anschluss`; Ports `dachplatte.dachflaeche` ↔ `dachaufbau.daemmung_abdichtung`; Boundary-Typ, Layer Stack, Dämmebene, U-Wert, Wärmebrücke.<br>**TGA / Openings:** Bestehende Öffnungen, neue Kernbohrungen/Durchführungen, Trassenbedarf, Durchmesser und Mindestabstände. |
| Minimal benötigte Rohdaten | Dachaufbau, Abdichtung, Dämmung, λ, Ziel-U-Wert, Neigung, Durchdringungen, Tragzone. |
| Prüfregel | Die Dachplatte muss mit Dachaufbau, Abdichtung und Dämmung als vollständiges Hüllbauteil modelliert sein. |
| Resultat | PASS = U-Wert + Abdichtung + Durchdringungszonen geklärt. WARNUNG = Dachform oder Durchdringungen offen. FAIL = unvollständiger Dachaufbau. |
| Quelle | PDF S. 207: Dachkonstruktion abhängig von Dachform, ggf. durch wiederverwendete Elemente beeinflusst; PDF S. 262: Dachaufbau und Durchführungen beachten. |

### R-E04 — Dämmungskante ↔ Dämmungskante thermische Kontinuität

**Regel liegt im Paket:** `Energy`  
**Liest Daten aus:** `Energy`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `DaemmungLayer` an ReUse-Bauteil A ↔ `DaemmungLayer` an Bauteil B |
| Konnektoren | `thermische_kontinuitaet` ↔ `thermische_kontinuitaet` |
| Ports | `element_A.daemmungskante` ↔ `element_B.daemmungskante` |
| Repräsentation | Dämmebene als Kanten-/Flächennetz |
| Wann läuft die Regel? | Wenn zwei Hüllbauteile aneinanderstoßen. |
| Daten nach Paket | **Energy:** Thermische Flächen/Schichten; Konnektoren `thermische_kontinuitaet` ↔ `thermische_kontinuitaet`; Ports `element_A.daemmungskante` ↔ `element_B.daemmungskante`; Boundary-Typ, Layer Stack, Dämmebene, U-Wert, Wärmebrücke.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Dämmungskanten, Versatz, Fugenbreite, Anschlussdetail, Material, Dämmebenenlage. |
| Prüfregel | Dämmungskanten müssen sich geometrisch treffen; bei Unterbrechung entsteht eine Wärmebrückenwarnung. |
| Resultat | PASS = kontinuierliche Dämmebene. WARNUNG = Unterbrechung oder Versatz. FAIL = thermische Hülle nicht schließbar. |
| Quelle | PDF S. 163–164: ReUse-Beton in der Hülle muss mit Dämmung so ergänzt werden, dass der geforderte U-Wert erreicht wird. |

### R-E05 — Beton-Durchlaufzone ↔ Dämmebene Wärmebrücke

**Regel liegt im Paket:** `Energy`  
**Liest Daten aus:** `Energy`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand`, `ReuseDeckenplatte`, `ReuseFragment_StuetzeDecke` ↔ `DaemmungLayer` / `ThermischeHuelle` |
| Konnektoren | `waermebruecken_risiko` ↔ `daemmebene` |
| Ports | `betonbauteil.durchlaufzone` ↔ `huelle.daemmebene` |
| Repräsentation | Betonquerschnitt im Schnittmodell; Dämmebene als Schichtfläche |
| Wann läuft die Regel? | Wenn ein Stahlbetonelement die Dämmebene durchstößt oder stark unterbricht. |
| Daten nach Paket | **Energy:** Thermische Flächen/Schichten; Konnektoren `waermebruecken_risiko` ↔ `daemmebene`; Ports `betonbauteil.durchlaufzone` ↔ `huelle.daemmebene`; Boundary-Typ, Layer Stack, Dämmebene, U-Wert, Wärmebrücke. |
| Minimal benötigte Rohdaten | Betonquerschnitt, Lage zur Dämmebene, Dämmüberdeckung, Innen/Außen-Kontakt, Anschlussdetail. |
| Prüfregel | Durchlaufender Beton an der thermischen Hülle erzeugt eine Wärmebrückenwarnung, bis ein Detail die Unterbrechung löst. |
| Resultat | WARNUNG = Wärmebrücke möglich. PASS = Detail mit durchgehender Dämmung vorhanden. FAIL = Ziel-U-Wert/Detail nicht nachweisbar. |
| Quelle | PDF S. 163–164: Bei Hüllbauteilen muss die Dämmung den U-Wert des gesamten Bauteils auf den geforderten Wert herabsenken. |

## TGA / Openings

**Anzahl Regeln:** 4


### R-T01 — TGA-Trasse ↔ bestehende Öffnung

**Regel liegt im Paket:** `TGA / Openings`  
**Liest Daten aus:** `Energy`, `TGA / Openings`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `TGA_Trasse` ↔ `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` |
| Konnektoren | `oeffnung_nutzen` ↔ `bestandsoeffnung_angebot` |
| Ports | `tga_trasse.querschnitt` ↔ `bauteil.bestandsoeffnung` |
| Repräsentation | Trasse als Volumen/Korridor; Öffnung als Rechteck/Polygon mit Tiefe |
| Wann läuft die Regel? | Wenn eine Leitungstrasse durch eine vorhandene Öffnung geführt werden soll. |
| Daten nach Paket | **TGA / Openings:** Öffnung/Bohrung/Durchführung/Trasse; Konnektoren `oeffnung_nutzen` ↔ `bestandsoeffnung_angebot`; Ports `tga_trasse.querschnitt` ↔ `bauteil.bestandsoeffnung`; Lage, Durchmesser, Funktion, Korridor und Mindestabstände.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Energy:** Thermische Grenzfläche, Schichtaufbau, Dämmkontinuität, U-Wert-Anforderung, Abdichtung oder Wärmebrückenstatus.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Öffnungsmaße, Trassenquerschnitt, Lage, Toleranz, Brandschutz-/Schallschutzstatus, Abdichtung, Raumfunktion. |
| Prüfregel | Eine bestehende Öffnung darf genutzt werden, wenn die Trasse geometrisch passt und exakt zur Leitungsführung liegt. |
| Resultat | PASS = Öffnung passt. WARNUNG = Toleranz knapp oder Brandschutz offen. FAIL = Öffnung zu klein, falsch liegend oder funktional unpassend. |
| Quelle | PDF S. 207: ggf. Kernbohrungen oder Öffnungen in ReUse-Stahlbetonelementen für Kabeldurchführungen. |

### R-T02 — TGA-Trasse ↔ neue Kernbohrung / Bohrzone

**Regel liegt im Paket:** `TGA / Openings`  
**Liest Daten aus:** `Structural`, `TGA / Openings`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `TGA_Trasse` ↔ `ReuseWand`, `ReuseDeckenplatte`, `ReuseStuetze` oder `ReuseBodenplatte` |
| Konnektoren | `kernbohrung_bedarf` ↔ `bohrzone_angebot` |
| Ports | `tga_trasse.bohrpunkt` ↔ `bauteil.bohrzone` |
| Repräsentation | Bohrung als Zylinder; Bauteil als Volumen mit Bewehrungs- und Schadensoverlay |
| Wann läuft die Regel? | Wenn eine neue Kernbohrung oder Öffnung in ReUse-Beton geplant wird. |
| Daten nach Paket | **TGA / Openings:** Öffnung/Bohrung/Durchführung/Trasse; Konnektoren `kernbohrung_bedarf` ↔ `bohrzone_angebot`; Ports `tga_trasse.bohrpunkt` ↔ `bauteil.bohrzone`; Lage, Durchmesser, Funktion, Korridor und Mindestabstände.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Bohrdurchmesser, Bohrtiefe, Bewehrungskarte, Tragzonen, Randabstände, Materialfestigkeit, Schadenszonen, Toleranz. |
| Prüfregel | Neue Bohrungen sind nur möglich, wenn keine kritische Bewehrung, keine Schadenszone und keine tragende Kernzone getroffen wird. |
| Resultat | PASS = freie Bohrzone. WARNUNG = Bewehrungsunsicherheit. FAIL = Bewehrungs-/Tragwerkskonflikt oder Schaden in Bohrzone. |
| Quelle | PDF S. 207 und S. 260–262: Öffnungen/Bohrungen und Leitungsführungen sind bei TGA und Rohbauarbeiten zu beachten. |

### R-T03 — Bodenplatte/Fundament ↔ Leitungsdurchführung

**Regel liegt im Paket:** `TGA / Openings`  
**Liest Daten aus:** `Structural`, `Energy`, `TGA / Openings`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `TGA_Trasse` ↔ `ReuseBodenplatte`, `NeubauBodenplatte` oder `NeubauFundament` |
| Konnektoren | `leitungsdurchfuehrung_bedarf` ↔ `durchfuehrung_angebot` |
| Ports | `leitung.trasse` ↔ `bodenplatte.durchfuehrung` oder `fundament.durchfuehrung` |
| Repräsentation | Leitung als Korridor; Bodenplatte/Fundament als Platte/Volumen mit Öffnung und Abdichtung |
| Wann läuft die Regel? | Wenn Leitungen durch Bodenplatte oder Fundamentbereich geführt werden. |
| Daten nach Paket | **TGA / Openings:** Öffnung/Bohrung/Durchführung/Trasse; Konnektoren `leitungsdurchfuehrung_bedarf` ↔ `durchfuehrung_angebot`; Ports `leitung.trasse` ↔ `bodenplatte.durchfuehrung` oder `fundament.durchfuehrung`; Lage, Durchmesser, Funktion, Korridor und Mindestabstände.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Energy:** Thermische Grenzfläche, Schichtaufbau, Dämmkontinuität, U-Wert-Anforderung, Abdichtung oder Wärmebrückenstatus.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Durchführungsposition, Leitungsachse, Öffnungsmaß, Dichtung, Abdichtung, Bauteildicke, Bewehrungskarte, Sockel-/Erdkontakt. |
| Prüfregel | Leitungsdurchführungen müssen in Bauteil- und Anschlussplanung berücksichtigt sein und dürfen Tragwerk, Abdichtung und Dämmung nicht verletzen. |
| Resultat | PASS = Durchdringung, Abdichtung und Tragwerk kompatibel. WARNUNG = Abdichtung/Bewehrung offen. FAIL = keine Durchführung oder Konflikt mit Trag-/Abdichtungszone. |
| Quelle | PDF S. 260–261: Fundamente und Bodenplatten müssen Leitungsdurchführungen beachten bzw. herstellen. |

### R-T04 — Dachplatte/Dachaufbau ↔ Dach-Durchdringung

**Regel liegt im Paket:** `TGA / Openings`  
**Liest Daten aus:** `Structural`, `Energy`, `TGA / Openings`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `TGA_Trasse` oder `PV_Solar_Blitzschutz_Element` ↔ `ReuseDachplatte` + `Dachaufbau` |
| Konnektoren | `dach_durchdringung_bedarf` ↔ `dach_durchdringung_angebot` |
| Ports | `tga_pv_blitzschutz.durchdringungspunkt` ↔ `dach.bauteil_durchdringung` |
| Repräsentation | Dachplatte als Fläche; Dachaufbau als Layer; Durchdringung als Zylinder/Objekt |
| Wann läuft die Regel? | Wenn Abwasserentlüftung, PV/Solarthermie oder Blitzschutz durch/auf dem Dach vorgesehen wird. |
| Daten nach Paket | **TGA / Openings:** Öffnung/Bohrung/Durchführung/Trasse; Konnektoren `dach_durchdringung_bedarf` ↔ `dach_durchdringung_angebot`; Ports `tga_pv_blitzschutz.durchdringungspunkt` ↔ `dach.bauteil_durchdringung`; Lage, Durchmesser, Funktion, Korridor und Mindestabstände.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Energy:** Thermische Grenzfläche, Schichtaufbau, Dämmkontinuität, U-Wert-Anforderung, Abdichtung oder Wärmebrückenstatus.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Öffnungsposition, Leitungs-/Bauteildurchmesser, Abdichtung, Dachaufbau, Dämmung, Tragzone, Gefälle, Feuchteschutz. |
| Prüfregel | Dach-Durchdringungen müssen mit Dachaufbau, Abdichtung, Dämmung und Tragwerkszone kompatibel sein. |
| Resultat | PASS = vollständiges Durchdringungsdetail. WARNUNG = Abdichtung/Dämmung noch offen. FAIL = Konflikt mit Tragzone oder keine Abdichtung. |
| Quelle | PDF S. 262: Dach benötigt Auflagerprüfung, Dachaufbau und Durchführungen für Abwasserentlüftung, PV/Solarthermie und Blitzschutz. |

## Semantic / Architectural

**Anzahl Regeln:** 4


### R-A01 — ReUse-Element ↔ Gebäuderaster

**Regel liegt im Paket:** `Semantic / Architectural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte`, `ReuseWand`, `ReuseUnterzug` oder `ReuseFragment_StuetzeDecke` ↔ `Gebaeuderaster` |
| Konnektoren | `rasterbindung` ↔ `raster_achse` |
| Ports | `element.rasterkante` ↔ `gebaeuderaster.achse` |
| Repräsentation | Element als Bounding Box/Kantenmodell; Raster als Achsnetz |
| Wann läuft die Regel? | Wenn ein Pool-Element in ein Neubauraster gesetzt wird. |
| Daten nach Paket | **Semantic / Architectural:** Raster, Fuge, Sichtfläche oder Raumfunktion; Konnektoren `rasterbindung` ↔ `raster_achse`; Ports `element.rasterkante` ↔ `gebaeuderaster.achse`; Orientierung, Sichtanforderung und Entwurfsbezug.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Elementbreite, Achsraster, Toleranz, Elementfamilie, Anschlussports, Spannrichtung. |
| Prüfregel | Elementbreiten und Anschlusskanten sollen das Neubauraster unterstützen; große Abweichungen erzeugen Warnung oder erfordern Rasteranpassung. |
| Resultat | PASS = Achspassung. WARNUNG = Abweichung mit Anpassungsvorschlag. FAIL = Rasterkonflikt erzeugt unlösbaren Tragwerks-/Portkonflikt. |
| Quelle | PDF S. 100–101: Elementbreite soll möglichst ein festes Raster bilden; Elemente werden auf der Grundrissskizze platziert und iterativ abgeglichen. |

### R-A02 — ReUse-Element ↔ ReUse-Element Fugenflucht

**Regel liegt im Paket:** `Semantic / Architectural`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseDeckenplatte` oder `ReuseWand` ↔ `ReuseDeckenplatte` oder `ReuseWand` |
| Konnektoren | `fugenbild_angebot` ↔ `fugenbild_angebot` |
| Ports | `element_A.fugenkante` ↔ `element_B.fugenkante` |
| Repräsentation | Kantenmodell mit Sichtstatus und Fugenbreite |
| Wann läuft die Regel? | Wenn zwei sichtbare oder konstruktive Kanten verbunden werden. |
| Daten nach Paket | **Semantic / Architectural:** Raster, Fuge, Sichtfläche oder Raumfunktion; Konnektoren `fugenbild_angebot` ↔ `fugenbild_angebot`; Ports `element_A.fugenkante` ↔ `element_B.fugenkante`; Orientierung, Sichtanforderung und Entwurfsbezug.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Fugenkanten, Höhenlage, Versatz, Fugenbreite, sichtbarer Status, Verbinderbedarf. |
| Prüfregel | Fugen sollten fluchten oder als bewusstes Detail markiert sein; unbeabsichtigter Versatz erzeugt Warnung. |
| Resultat | PASS = Flucht oder bewusstes Detail. WARNUNG = unbeabsichtigter Versatz. FAIL = Versatz kollidiert mit Tragwerksanschluss. |
| Quelle | PDF S. 100–101: Elemente werden iterativ mit Entwurf und Verbindungsanforderungen abgeglichen. |

### R-A03 — ReUse-Sichtfläche ↔ Raumseite

**Regel liegt im Paket:** `Semantic / Architectural`  
**Liest Daten aus:** `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand`, `ReuseDeckenplatte` oder `ReuseFragment_StuetzeDecke` ↔ `Raumfunktion` / `Raumseite` |
| Konnektoren | `sichtflaeche_angebot` ↔ `sichtflaeche_bedarf` |
| Ports | `element.sichtflaeche` ↔ `raum.ansichtsseite` |
| Repräsentation | Oberfläche als orientierte Fläche mit Schadens-/Reparaturoverlay |
| Wann läuft die Regel? | Wenn eine bestehende Betonfläche sichtbar bleiben soll. |
| Daten nach Paket | **Semantic / Architectural:** Raster, Fuge, Sichtfläche oder Raumfunktion; Konnektoren `sichtflaeche_angebot` ↔ `sichtflaeche_bedarf`; Ports `element.sichtflaeche` ↔ `raum.ansichtsseite`; Orientierung, Sichtanforderung und Entwurfsbezug.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Sichtseite, Flächennormalen, Oberflächenzustand, Risse, Abplatzungen, Reparaturen, gewünschte Raumseite. |
| Prüfregel | Sichtflächen müssen korrekt orientiert und über Evidenzstatus bewertet sein. |
| Resultat | PASS = richtige Orientierung und akzeptabler Zustand. WARNUNG = Schaden/Reparatur sichtbar. FAIL = falsche Orientierung oder nicht akzeptabler sichtbarer Schaden. |
| Quelle | PDF S. 75–80: Schäden, Risse, Abplatzungen und Oberflächenveränderungen sind zu begutachten. |

### R-A04 — bestehende Öffnung ↔ Raumfunktion

**Regel liegt im Paket:** `Semantic / Architectural`  
**Liest Daten aus:** `Structural`, `TGA / Openings`, `Semantic / Architectural`

| Feld | Inhalt |
|---|---|
| Komponenten | `ReuseWand` oder `ReuseDeckenplatte` ↔ `Raumfunktion` |
| Konnektoren | `bestandsoeffnung_angebot` ↔ `oeffnung_bedarf` |
| Ports | `element.bestandsoeffnung` ↔ `raumfunktion.tuer_fenster_tga` |
| Repräsentation | Öffnung als Polygon/Volumen; Raumfunktion als Nutzungsanforderung |
| Wann läuft die Regel? | Wenn eine bestehende Öffnung als Tür, Fenster oder TGA-Durchführung genutzt werden soll. |
| Daten nach Paket | **Semantic / Architectural:** Raster, Fuge, Sichtfläche oder Raumfunktion; Konnektoren `bestandsoeffnung_angebot` ↔ `oeffnung_bedarf`; Ports `element.bestandsoeffnung` ↔ `raumfunktion.tuer_fenster_tga`; Orientierung, Sichtanforderung und Entwurfsbezug.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**TGA / Openings:** Bestehende Öffnungen, neue Kernbohrungen/Durchführungen, Trassenbedarf, Durchmesser und Mindestabstände. |
| Minimal benötigte Rohdaten | Öffnungsmaß, Brüstung/Lage, Orientierung, Raumfunktion, TGA-Route, Tragwerksfreigabe, Brandschutz/Schallschutz. |
| Prüfregel | Eine vorhandene Öffnung darf semantisch nur genutzt werden, wenn Maße, Lage, Funktion und technische Anforderungen zusammenpassen. |
| Resultat | PASS = Öffnung passt zur Funktion. WARNUNG = Anpassung/Brandschutz offen. FAIL = Maß/Lage/Funktion unvereinbar. |
| Quelle | PDF S. 129–131: Bauteilkatalog soll Öffnungsmaße enthalten; PDF S. 207: Öffnungen können für Durchführungen relevant werden. |

## Logistics

**Anzahl Regeln:** 10


### R-L01 — Bauteil ↔ Standardtransport-Hülle

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Transportmittel` / `StandardtransportLimit` |
| Konnektoren | `transportfaehigkeit` ↔ `transportkapazitaet` |
| Ports | `komponente.transport_bbox` ↔ `transport.standardlimit` |
| Repräsentation | Bounding Box des Bauteils; Transportlimit als Hüllkörper |
| Wann läuft die Regel? | Wenn ein Element in eine Transportfuhre eingeplant wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `transportfaehigkeit` ↔ `transportkapazitaet`; Ports `komponente.transport_bbox` ↔ `transport.standardlimit`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Länge, Breite, Höhe, Transportmittel, Sondertransportstatus, Gewicht. |
| Prüfregel | Standardtransport-Passung: Länge ≤ 13 m, Breite ≤ 3 m, Höhe ≤ 3 m. |
| Resultat | PASS = innerhalb Limit. WARNUNG = außerhalb Limit, Sondertransport nötig. FAIL = Transportmittel kann Hülle nicht aufnehmen. |
| Quelle | PDF S. 97–100: Elemente sollten Transportmaße mitdenken; 13 m Länge, 3 m Höhe, 3 m Breite werden genannt. |

### R-L02 — Bauteilmasse ↔ Fahrzeugnutzlast

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Structural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente oder Fuhrenliste ↔ `Transportmittel` |
| Konnektoren | `transportmasse` ↔ `nutzlastangebot` |
| Ports | `komponente.masse_port` ↔ `fahrzeug.nutzlast` |
| Repräsentation | Masse als Skalar; Fuhre als Liste/Graph |
| Wann läuft die Regel? | Wenn eine Transportfuhre zusammengestellt wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `transportmasse` ↔ `nutzlastangebot`; Ports `komponente.masse_port` ↔ `fahrzeug.nutzlast`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Elementmasse, Fahrzeugnutzlast, Ladekombination, Schwerpunkt, Ladungssicherung. |
| Prüfregel | Summe der Massen darf Fahrzeug- und Ladungssicherungslogik nicht überschreiten. |
| Resultat | PASS = Masse innerhalb Nutzlast. WARNUNG = Schwerpunkt/Ladungssicherung offen. FAIL = Nutzlast überschritten. |
| Quelle | PDF S. 129–131: Bauteilkatalog enthält Volumen und Masse; PDF S. 235–236: Transportfuhren sollen richtig beladen und zeitlich abgestimmt sein. |

### R-L03 — Bauteil-Hebeport ↔ Kranhaken

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Kran` |
| Konnektoren | `hebeanschluss` ↔ `kran_hubangebot` |
| Ports | `komponente.hebeport` ↔ `kran.haken` |
| Repräsentation | Bauteil als Volumen mit Schwerpunkt; Kran als Last-Radius-Modell |
| Wann läuft die Regel? | Wenn ein Element gehoben oder montiert wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `hebeanschluss` ↔ `kran_hubangebot`; Ports `komponente.hebeport` ↔ `kran.haken`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Masse, Hebepunkte, Anschlagmittel, Schwerpunkt, Kranlasttabelle, Reichweite, Schadenszonen an Hebepunkten. |
| Prüfregel | Hebepunkte und Kran müssen die Elementmasse an der geplanten Position aufnehmen können. |
| Resultat | PASS = Kranlast und Hebepunkte ausreichend. WARNUNG = Schwerpunkt/Hebepunkte unsicher. FAIL = Krantragfähigkeit überschritten oder Hebeport beschädigt. |
| Quelle | PDF S. 123–126: Krantragkraft hängt von Position, Auslegerlänge, Höhenlage und Winkel ab. |

### R-L04 — Montageposition ↔ Kranreichweite

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Kran` |
| Konnektoren | `montageposition_bedarf` ↔ `kranreichweite_angebot` |
| Ports | `komponente.montageposition` ↔ `kran.stellplatz_ausleger` |
| Repräsentation | Montageort als Punkt/Volumen; Kran als Radius-Höhen-Last-Modell |
| Wann läuft die Regel? | Wenn eine Montageposition gewählt wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `montageposition_bedarf` ↔ `kranreichweite_angebot`; Ports `komponente.montageposition` ↔ `kran.stellplatz_ausleger`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Kranstandort, Auslegerlänge, Radius, Höhe, Last, Gelände/Platz, Elementmasse. |
| Prüfregel | Krantragfähigkeit wird positionsabhängig geprüft; zu großer Radius oder zu hohe Last erzeugt Warnung/Fail. |
| Resultat | PASS = Last am Radius zulässig. WARNUNG = knappe Reserve. FAIL = Last/Radium/Höhe außerhalb Kranbereich. |
| Quelle | PDF S. 123–126: Kranlastkapazität variiert stark nach Lastposition und Krantyp. |

### R-L05 — Bauteil ↔ Lagerorientierung

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Lagerplatz` |
| Konnektoren | `lagerlage_bedarf` ↔ `lagerregel_angebot` |
| Ports | `komponente.lager_orientierung` ↔ `lagerplatz.lagerregel` |
| Repräsentation | Bauteil mit ursprünglicher Einbaulage; Lager als Stell-/Liegeposition |
| Wann läuft die Regel? | Wenn ein Element im Lager platziert wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `lagerlage_bedarf` ↔ `lagerregel_angebot`; Ports `komponente.lager_orientierung` ↔ `lagerplatz.lagerregel`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Elementtyp, ursprüngliche Einbaulage, geplante Lagerlage, Auflagerpunkte, Schadensrisiko. |
| Prüfregel | Decken liegend lagern; Wände und Stützen stehend lagern, wenn möglich entsprechend ursprünglicher Lastfälle. |
| Resultat | PASS = Lagerung entspricht Regel. WARNUNG = abweichende Lagerung mit Nachweis nötig. FAIL = abweichende Lagerung ohne Nachweis und Schadensrisiko. |
| Quelle | PDF S. 186: Elemente sollten möglichst in gleicher Ausrichtung wie im Bestandsgebäude gelagert werden; Decken liegend, Wände/Stützen stehend. |

### R-L06 — Bauteil ↔ Witterungsschutz im Lager

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Lagerplatz` |
| Konnektoren | `witterungsempfindlichkeit` ↔ `witterungsschutz_angebot` |
| Ports | `komponente.witterungsrisiko` ↔ `lagerplatz.schutzstatus` |
| Repräsentation | Bauteil mit Riss-/Öffnungszonen; Lager als Schutzstatus |
| Wann läuft die Regel? | Wenn ein Element gelagert wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `witterungsempfindlichkeit` ↔ `witterungsschutz_angebot`; Ports `komponente.witterungsrisiko` ↔ `lagerplatz.schutzstatus`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Risse/Öffnungen, Niederschlagsschutz, Frostperiode, Feuchtestatus, Karbonatisierungsrisiko. |
| Prüfregel | Bei Rissen/Öffnungen und freier Bewitterung erzeugt der Checker Frost-/Karbonatisierungswarnung. |
| Resultat | PASS = Schutz vorhanden. WARNUNG = freie Bewitterung. FAIL = kritischer Schaden plus fehlender Schutz. |
| Quelle | PDF S. 185–186: Witterungsschutz erhält Zustand; Regenwasser in Rissen/Öffnungen kann Frostsprengungen verursachen; Feuchte kann Karbonatisierung beschleunigen. |

### R-L07 — Bauteilkontakt ↔ Lagerholz

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Lagerplatz` / `Lagerholz` |
| Konnektoren | `lagerkontakt` ↔ `schutzauflage` |
| Ports | `komponente.transport_auflagepunkt` oder `kontaktflaeche` ↔ `lagerholz.auflage` |
| Repräsentation | Kontaktflächen als Punkte/Linien/Flächen; Lagerholz als Schutzkörper |
| Wann läuft die Regel? | Wenn Elemente gestapelt oder nebeneinander gelagert werden. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `lagerkontakt` ↔ `schutzauflage`; Ports `komponente.transport_auflagepunkt` oder `kontaktflaeche` ↔ `lagerholz.auflage`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Lagerhölzer, Kontaktflächen, Stapelposition, Elementtyp, Elementmasse. |
| Prüfregel | Elemente müssen durch schützende Lagerhölzer getrennt werden, damit Kontaktbeschädigungen vermieden werden. |
| Resultat | PASS = Lagerhölzer korrekt. WARNUNG = Lagerholzposition unvollständig. FAIL = direkter schädigender Bauteilkontakt. |
| Quelle | PDF S. 186: Elemente sollen voneinander durch schützende Lagerhölzer getrennt werden. |

### R-L08 — Lagerposition ↔ Einbaureihenfolge

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Montageplan` / `Lagerplatz` |
| Konnektoren | `einbauzeit_bedarf` ↔ `lagerzugriff_angebot` |
| Ports | `komponente.id` / `komponente.montageport` ↔ `lagerplatz.stapelposition` / `montageplan.reihenfolge` |
| Repräsentation | Element-ID in Liste; Lager als Graph/Stapel |
| Wann läuft die Regel? | Wenn Lagerplan oder Stapelplan erstellt wird. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `einbauzeit_bedarf` ↔ `lagerzugriff_angebot`; Ports `komponente.id` / `komponente.montageport` ↔ `lagerplatz.stapelposition` / `montageplan.reihenfolge`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Montagefolge, Element-ID, Lagerposition, Stapelreihenfolge, Entnahmerichtung. |
| Prüfregel | Lagerposition muss zur späteren Einbaureihenfolge passen, damit kein unnötiges Umstapeln entsteht. |
| Resultat | PASS = Zugriff in Reihenfolge möglich. WARNUNG = Umstapeln nötig. FAIL = Element nicht rechtzeitig erreichbar. |
| Quelle | PDF S. 185: Lagerplan soll Positionen entsprechend späterer Einbaureihenfolge vorsehen. |

### R-L09 — Transportfuhre ↔ Montagezeitfenster

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | `Transportmittel` mit Elementliste ↔ `Montageplan` / `Baustelle` |
| Konnektoren | `lieferung_angebot` ↔ `montagezeitfenster_bedarf` |
| Ports | `transport.fuhre` ↔ `baustelle.montagezeitfenster` |
| Repräsentation | Fuhre als Liste von IDs; Montageplan als Zeitachse |
| Wann läuft die Regel? | Wenn Transportfuhren geplant werden. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `lieferung_angebot` ↔ `montagezeitfenster_bedarf`; Ports `transport.fuhre` ↔ `baustelle.montagezeitfenster`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen. |
| Minimal benötigte Rohdaten | Bauzeitplan, Montagezeitpunkt, Baustellenlagerfläche, Element-IDs, Beladung, Entladefolge. |
| Prüfregel | Transporte sollen die jeweils benötigten Elemente zum richtigen Zeitpunkt bringen und zugleich optimal beladen sein, ohne unnötige Baustellenzwischenlagerung. |
| Resultat | PASS = Lieferung passt zur Montage. WARNUNG = Zwischenlagerung/Umstapeln nötig. FAIL = Element fehlt im Zeitfenster oder Baustelle kann Fuhre nicht aufnehmen. |
| Quelle | PDF S. 235–236: Bauzeitplan und Logistik müssen die Einbaureihenfolge berücksichtigen; Fuhren sollen richtige Elemente zum richtigen Zeitpunkt bringen und optimal beladen sein. |

### R-L10 — Bauteil ↔ Zielposition / Anschlussvorbereitung

**Regel liegt im Paket:** `Logistics`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ Zielposition im Neubau, z. B. `NeubauFundament`, `Wand`, `Stuetze`, `Traeger`, `Decke` |
| Konnektoren | `montagebereitschaft` ↔ `anschlussvorbereitung` |
| Ports | `komponente.montageport` ↔ `zielposition.anschlussvorbereitung` |
| Repräsentation | Bauteil mit Ports; Zielposition mit vorbereitetem Anschlussdetail |
| Wann läuft die Regel? | Direkt vor Platzierung im Neubau oder bei digitaler Montageprüfung. |
| Daten nach Paket | **Logistics:** Transport-/Hebe-/Lager-/Montagekontext; Konnektoren `montagebereitschaft` ↔ `anschlussvorbereitung`; Ports `komponente.montageport` ↔ `zielposition.anschlussvorbereitung`; Masse, Hüllmaß, Hebepunkt, Kran/Fahrzeug, Lagerlage, Sequenz.<br>**Evidence:** Bewehrungskarte, Betondeckung, Materialkennwerte, Schadens-/Riss-/Korrosionszonen, Karbonatisierung, Prüfstatus und Unsicherheit genau für die betroffenen Portzonen.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Anschlussdetails, Auflager, Verbinder, Toleranzen, Öffnungen, Ist-Maße, Freigaben, Schadensstatus. |
| Prüfregel | Montage darf nur PASS ergeben, wenn Zielposition, Anschlussdetail, Toleranz und Elementfreigabe zusammenpassen. |
| Resultat | PASS = montagebereit. WARNUNG = Toleranz/Freigabe offen. FAIL = Anschluss nicht vorbereitet, falsche Maße oder ungeklärter Schaden. |
| Quelle | PDF S. 260–262: Rohbauarbeiten verlangen Anschlüsse, Auflager und Leitungsdurchführungen je Bauteil; Schäden vor Einbau müssen begutachtet und aufgearbeitet werden. |

## Evidence

**Anzahl Regeln:** 8


### R-V01 — aktiver Port ↔ Schadenszone

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `TGA / Openings`, `Semantic / Architectural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ aktiver Anschluss-/Nutzungskontext |
| Konnektoren | `schadensueberlagerung` ↔ `port_freigabe` |
| Ports | `komponente.schadenszone` ↔ `aktiver_port.zone` |
| Repräsentation | Schadenspolygone auf Geometrie; Portzone als Einflussbereich |
| Wann läuft die Regel? | Bei jeder Verbindung, deren Port in oder nahe einer Schadenszone liegt. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `schadensueberlagerung` ↔ `port_freigabe`; Ports `komponente.schadenszone` ↔ `aktiver_port.zone`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**TGA / Openings:** Bestehende Öffnungen, neue Kernbohrungen/Durchführungen, Trassenbedarf, Durchmesser und Mindestabstände.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant.<br>**Logistics:** Masse, Transporthülle, Hebe-/Montagezustand, Lagerorientierung, Kran-/Fahrzeug-/Zeitfensterdaten falls relevant. |
| Minimal benötigte Rohdaten | Schadenspolygone, Risse, Abplatzungen, Korrosion, Portlage, Einflussradius, Reparaturstatus. |
| Prüfregel | Schäden in Anschluss-, Auflager-, Bohr- oder Sichtzonen reduzieren die Freigabe des Ports. |
| Resultat | PASS = kein Schaden. WARNUNG = Schaden nahe Port oder unkritisch. FAIL = Schaden im tragenden Kontakt-/Bohrbereich. |
| Quelle | PDF S. 75–80: Qualität, Schäden, Risse, Abplatzungen, Korrosion und Instandsetzungen sind zu begutachten. |

### R-V02 — tragender Port ↔ Riss/Korrosionsrisiko

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige tragende Pool-Komponente ↔ aktiver Tragwerksanschluss |
| Konnektoren | `riss_korrosionsrisiko` ↔ `tragender_port` |
| Ports | `komponente.risszone` ↔ `tragender_port.zone` |
| Repräsentation | Risslinie/Polygon mit Breite; Portzone als Bereich |
| Wann läuft die Regel? | Wenn ein tragender Port in einem gerissenen Bereich liegt. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `riss_korrosionsrisiko` ↔ `tragender_port`; Ports `komponente.risszone` ↔ `tragender_port.zone`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Rissbreite, Rissursache, Abplatzung, Feuchte, Korrosionsprüfung, Bewehrungslage. |
| Prüfregel | Risse über 0,3 mm oder signifikante Abplatzungen verlangen Korrosionsausschluss vor tragender Wiederverwendung. |
| Resultat | WARNUNG = Nachweis fehlt. PASS = Korrosion ausgeschlossen. FAIL = Korrosion nicht ausgeschlossen oder bestätigt. |
| Quelle | PDF S. 76: Bei Rissen über 0,3 mm und signifikanten Abplatzungen muss sichergestellt werden, dass Bewehrung nicht korrodiert ist. |

### R-V03 — Port ↔ Korrosionsstatus

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige tragende Pool-Komponente ↔ aktiver Anschluss |
| Konnektoren | `korrosionsnachweis` ↔ `anschlussfreigabe` |
| Ports | `bewehrung.korrosionsstatus` ↔ `tragender_port.freigabe` |
| Repräsentation | Korrosionsstatus als Attribut/Overlay auf Bewehrung |
| Wann läuft die Regel? | Wenn Korrosionsverdacht besteht oder ein Port Riss-/Feuchtezonen berührt. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `korrosionsnachweis` ↔ `anschlussfreigabe`; Ports `bewehrung.korrosionsstatus` ↔ `tragender_port.freigabe`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone. |
| Minimal benötigte Rohdaten | Potentialmessung, Freilegung, Korrosionsbefund, Reparaturstatus, Prüfdatum. |
| Prüfregel | Tragende Verbindung darf nur PASS sein, wenn Korrosion im relevanten Bereich ausgeschlossen oder behoben ist. |
| Resultat | PASS = ausgeschlossen/repariert. WARNUNG = Verdacht ungeklärt. FAIL = aktive/ungeklärte Korrosion im Anschlussbereich. |
| Quelle | PDF S. 76–77: Korrosion kann über Potentialmessung oder partielles Freilegen überprüft werden. |

### R-V04 — Karbonatisierungstiefe ↔ Betondeckung

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ aktiver Tragwerks- oder Lager-/Hüllkontext |
| Konnektoren | `karbonatisierungsrisiko` ↔ `port_dauerhaftigkeit` |
| Ports | `komponente.karbonatisierungstiefe` ↔ `komponente.betondeckung` / `aktiver_port.zone` |
| Repräsentation | Karbonatisierungsfront als Tiefe; Betondeckung als Bewehrungsattribut |
| Wann läuft die Regel? | Wenn ein Element tragend, feuchte-/witterungsrelevant oder in der Hülle eingesetzt wird. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `karbonatisierungsrisiko` ↔ `port_dauerhaftigkeit`; Ports `komponente.karbonatisierungstiefe` ↔ `komponente.betondeckung` / `aktiver_port.zone`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Logistics:** Masse, Transporthülle, Hebe-/Montagezustand, Lagerorientierung, Kran-/Fahrzeug-/Zeitfensterdaten falls relevant. |
| Minimal benötigte Rohdaten | Karbonatisierungstiefe, Betondeckung, Feuchte-/Lagerstatus, Bewehrungslage, Korrosionsstatus. |
| Prüfregel | Wenn Karbonatisierung bis zur Bewehrung reicht oder nahe daran liegt, wird der Port abgewertet. |
| Resultat | PASS = ausreichender Abstand. WARNUNG = geringe Reserve. FAIL = Karbonatisierung erreicht Bewehrung und Korrosion ist nicht ausgeschlossen. |
| Quelle | PDF S. 77–78: Karbonatisierung senkt den Korrosionsschutz; Karbonatisierungstiefe wird per Phenolphthalein-Indikatortest bestimmt. |

### R-V05 — Tragwerksanschluss ↔ Materialkennwerte

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `TGA / Openings`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | tragende Pool-Komponente ↔ aktiver Tragwerksanschluss |
| Konnektoren | `materialkennwert_sicherheit` ↔ `tragwerksanschluss` |
| Ports | `materialpruefung` ↔ `tragwerksanschluss` |
| Repräsentation | Materialwerte als Attributpaket pro Bauteil/Zone |
| Wann läuft die Regel? | Vor jedem tragenden Anschluss, Auflager, Bohr-/Anker- oder Dornanschluss. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `materialkennwert_sicherheit` ↔ `tragwerksanschluss`; Ports `materialpruefung` ↔ `tragwerksanschluss`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**TGA / Openings:** Bestehende Öffnungen, neue Kernbohrungen/Durchführungen, Trassenbedarf, Durchmesser und Mindestabstände.<br>**Logistics:** Masse, Transporthülle, Hebe-/Montagezustand, Lagerorientierung, Kran-/Fahrzeug-/Zeitfensterdaten falls relevant. |
| Minimal benötigte Rohdaten | Druckfestigkeit, Zugfestigkeit, E-Modul, Dichte, Chloridgehalt, Schadstoffstatus, Prüfmethode, Prüfdatum. |
| Prüfregel | Tragende Checks dürfen Materialwerte nur nutzen, wenn sie als element- oder zonenbezogene Prüfwerte vorliegen. |
| Resultat | PASS = belegte Werte. WARNUNG = Werte teilweise angenommen. FAIL = fehlende Druckfestigkeit oder fehlende Mindestinformation in Anschlusszone. |
| Quelle | PDF S. 78–80: Bohrkerne sollen u. a. Chlorid, Schadstoffe, Druck-/Zugfestigkeit, E-Modul und Dichte bestimmen; Rückprallwerte sollen mit Bohrkernen abgeglichen werden. |

### R-V06 — Bohr-/Anker-/Dornzone ↔ Bewehrungskarte

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `TGA / Openings`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente mit Bohr-/Anker-/Dornzone ↔ aktiver Connector: Schraubanker, Dorn, Bewehrungsanschluss oder Kernbohrung |
| Konnektoren | `bewehrungskonflikt` ↔ `bohr_anker_dorn_bedarf` |
| Ports | `bauteil.bewehrungskarte` ↔ `bohrzone` / `ankerzone` / `dornzone` / `bewehrungszone` |
| Repräsentation | Bewehrung als Linien-/Rasteroverlay; Bohr-/Ankerzone als Volumen |
| Wann läuft die Regel? | Bei Kernbohrungen, Schraubankern, Dornen und nachträglichen Bewehrungsanschlüssen. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `bewehrungskonflikt` ↔ `bohr_anker_dorn_bedarf`; Ports `bauteil.bewehrungskarte` ↔ `bohrzone` / `ankerzone` / `dornzone` / `bewehrungszone`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**TGA / Openings:** Bestehende Öffnungen, neue Kernbohrungen/Durchführungen, Trassenbedarf, Durchmesser und Mindestabstände. |
| Minimal benötigte Rohdaten | Bewehrungslage, Stabdurchmesser, Betondeckung, Ortungsunsicherheit, Bohrdurchmesser, Bohrtoleranz, Tragzonen. |
| Prüfregel | Bohr-, Anker- und Dornzonen dürfen keine kritische Bewehrung treffen. |
| Resultat | PASS = Zone frei. WARNUNG = Bewehrung unsicher. FAIL = kritischer Bewehrungskonflikt. |
| Quelle | PDF S. 79–84: Bewehrungslage, Betondeckung, Durchmesser und Abstände sind zu untersuchen; Ortungsverfahren werden beschrieben. |

### R-V07 — Sichtfläche ↔ Oberflächenzustand

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `Semantic / Architectural`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | Pool-Komponente mit sichtbarer Oberfläche ↔ `Raumseite` / `Sichtanforderung` |
| Konnektoren | `oberflaechen_evidenz` ↔ `sichtflaechenanforderung` |
| Ports | `element.sichtflaeche` / `oberflaechenzustand` ↔ `raum.ansichtsseite` |
| Repräsentation | Sichtfläche als orientierte Fläche; Schaden/Reparatur als Overlay |
| Wann läuft die Regel? | Wenn eine Betonfläche sichtbar bleiben soll. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `oberflaechen_evidenz` ↔ `sichtflaechenanforderung`; Ports `element.sichtflaeche` / `oberflaechenzustand` ↔ `raum.ansichtsseite`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Semantic / Architectural:** Rasterbezug, Raum-/Sichtanforderung, Fugenbild, Lage im Entwurf, Brandschutz-/Bekleidungs- oder Fußbodenaufbau-Information falls relevant. |
| Minimal benötigte Rohdaten | Oberflächenzustand, Risse, Abplatzungen, Reparaturen, Verfärbungen, gewünschte Sichtqualität. |
| Prüfregel | Sichtbarer Schaden erzeugt eine architektonische Warnung, auch wenn Tragwerk PASS ist. |
| Resultat | PASS = Zustand akzeptiert. WARNUNG = sichtbarer Schaden/Reparatur. FAIL = sichtbare Seite falsch orientiert oder Anforderung nicht erfüllbar. |
| Quelle | PDF S. 75–80: Oberflächenveränderungen, Schäden, Risse und Instandsetzungen sind visuell zu begutachten. |

### R-V08 — Bauteil nach Transport/Lagerung ↔ Montagefreigabe

**Regel liegt im Paket:** `Evidence`  
**Liest Daten aus:** `Structural`, `Logistics`, `Evidence`

| Feld | Inhalt |
|---|---|
| Komponenten | beliebige Pool-Komponente ↔ `Montageplan` / Zielanschluss |
| Konnektoren | `transport_lagerschaden` ↔ `montagefreigabe` |
| Ports | `komponente.schadensstatus_nach_transport` ↔ `komponente.montageport` |
| Repräsentation | Schadensstatus als Versionsstand vor Einbau |
| Wann läuft die Regel? | Direkt vor Montage nach Transport oder Lagerung. |
| Daten nach Paket | **Evidence:** Overlay-/Prüfdaten; Konnektoren `transport_lagerschaden` ↔ `montagefreigabe`; Ports `komponente.schadensstatus_nach_transport` ↔ `komponente.montageport`; Schadenszone, Riss, Korrosion, Karbonatisierung, Bewehrung, Materialwerte, Unsicherheit/Freigabe.<br>**Structural:** Tragende Portrolle, Lastpfad, Anschluss-/Auflagerkräfte, Tragfähigkeit, Randabstände und Strukturrelevanz der betroffenen Zone.<br>**Logistics:** Masse, Transporthülle, Hebe-/Montagezustand, Lagerorientierung, Kran-/Fahrzeug-/Zeitfensterdaten falls relevant. |
| Minimal benötigte Rohdaten | Schadensprüfung, Fotos, Riss-/Abplatzungsstatus, Reparaturstatus, Freigabe, betroffene Ports. |
| Prüfregel | Neu erkannte Schäden vor Einbau müssen begutachtet, eingeschätzt und ggf. aufgearbeitet werden. |
| Resultat | PASS = Freigabe nach Begutachtung. WARNUNG = unkritischer Schaden dokumentiert. FAIL = ungeklärter Schaden in Anschluss-/Tragzone. |
| Quelle | PDF S. 262: Werden vor Einbau Schäden aus Zwischenlagerung oder Transport festgestellt, müssen diese begutachtet, eingeschätzt und aufgearbeitet werden. |

---

## 4. Paket-Zusammenfassung

- **Structural (15):** R-S01, R-S02, R-S03, R-S04, R-S05, R-S06, R-S07, R-S08, R-S09, R-S10, R-S11, R-S12, R-S13, R-S14, R-S15
- **Energy (5):** R-E01, R-E02, R-E03, R-E04, R-E05
- **TGA / Openings (4):** R-T01, R-T02, R-T03, R-T04
- **Semantic / Architectural (4):** R-A01, R-A02, R-A03, R-A04
- **Logistics (10):** R-L01, R-L02, R-L03, R-L04, R-L05, R-L06, R-L07, R-L08, R-L09, R-L10
- **Evidence (8):** R-V01, R-V02, R-V03, R-V04, R-V05, R-V06, R-V07, R-V08