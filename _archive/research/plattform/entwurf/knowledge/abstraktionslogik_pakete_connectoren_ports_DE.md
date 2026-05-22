# Abstraktionslogik für Pakete, Repräsentationen, Connectoren und Ports  
## Angepasst an das neue Systemmodell

**Zweck**  
Dieses Dokument überführt die bisherige Paketstruktur in eine einheitliche Abstraktionslogik nach dem Muster:

```text
Reales Bauteil
→ paket-spezifische Repräsentation
→ minimale abstrakte Geometrie
→ Eigenschaften
→ Connectoren
→ Ports
→ Regeln / Checks / Berechnungen
```

Das Vorbild ist die Tragwerksabstraktion eines Trägers:

```text
realer Träger
→ 1D-Linienelement
→ Querschnitts- und Materialeigenschaften
→ Knoten / Anschlüsse / Auflager
→ Steifigkeitsgleichung
→ Kräfte, Momente, Verformungen, Reaktionen
```

Diese Logik wird hier auf alle Pakete übertragen.

---

# 1. Quellenbasis und Beispielkomponenten

## 1.1 Abbau/Aufbau DE_1OG_001

**Quelle:** Abbau/Aufbau-Handbuch, Bauteilkatalog.  
Das Handbuch beschreibt den Bauteilkatalog mit ID, Maßen, Öffnungsmaßen, Volumen, Masse und Elementtyp. Als konkretes Beispiel wird die Deckenplatte **DE_1OG_001** verwendet:

```text
Typologie: Deckenplatte
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

Dieses Beispiel steht für ein einzelnes, bereits katalogisiertes wiederverwendetes Stahlbetonbauteil.

Quelle:  
https://abbauaufbau.de/wp-content/uploads/2025/10/231101_AbbauAufbau_Handbuch_AP3.pdf

## 1.2 SlabBeamColumnFragment

**Quelle:** Abbau/Aufbau Masterarbeit 2020.  
Die Masterarbeit beschreibt den Umgang mit zugeschnittenen Stahlbetonfragmenten und räumlich wertvollen Situationen wie:

```text
Stützen vor Fenstern
Nische hinter Stütze
Große Stütze in kleinem Raum
```

Außerdem beschreibt sie, dass zugeschnittene Elemente auf einem Halbfertigteil-Stahlbetonträger ruhen und über einen nachträglichen Bewehrungsanschluss kraftschlüssig verbunden werden.

**Systemtypologie:**  
`SlabBeamColumnFragment` ist kein benanntes Originalobjekt aus der Quelle. Es ist eine abgeleitete Systemtypologie für ein monolithisches Betonfragment mit:

```text
Plattenbereich
integriertem Trägerbereich
Stützenabschnitt
Schnittflächen
räumlicher Fragmentqualität
```

Quelle:  
https://abbauaufbau.de/project/masterarbeit-2020

## 1.3 ReCreate Hollow-Core Slab

**Quelle:** ReCreate-Pilotprojekte Niederlande und Finnland.  
ReCreate wird als Beispiel für wiederverwendete Betonfertigteile genutzt, besonders für Hohlkammerdecken.

Relevante Punkte:

```text
Hohlkammerdecken
tragende Fassaden
Nassverbindungen
Sägen entlang von Längsfugen
Heben und Transport
BIM-Inventarisierung
QR-Tracking
Prüfung und Neuberechnung
```

Quellen:  
https://recreate-project.eu/project-pilots/the-netherlands/  
https://recreate-project.eu/project-pilots/finland/

---

# 2. Grundprinzip des Systems

## 2.1 Minimale Abstraktion

Das System soll nicht die gesamte Realität modellieren.  
Es speichert nur das, was notwendig ist für:

```text
Verbindung
Berechnung
Warnung
Kompatibilität
Entwurfsentscheidung
```

## 2.2 Einheitliches Paketmuster

Jedes Paket folgt derselben Logik:

```text
Reales Objekt
↓
Abstrakte Repräsentation
↓
Minimale Geometrie
↓
Eigenschaften
↓
Connectoren
↓
Ports
↓
Regeln / Berechnungen / Checks
```

## 2.3 Begriffe

| Begriff | Bedeutung |
|---|---|
| **Komponente** | reales wiederverwendetes Bauteil oder Fragment |
| **Paket** | fachliche Sicht auf dieselbe Komponente |
| **Repräsentation** | vereinfachtes Modell der Komponente innerhalb eines Pakets |
| **Eigenschaft** | beschreibender Wert ohne eigene Handlung |
| **Connector** | platzierter, handlungsrelevanter Griffpunkt |
| **Port** | semantischer Kompatibilitätstyp eines Connectors |
| **Regel / Check** | Prüfung, Berechnung oder Warnlogik auf Basis von Connectoren, Ports und Eigenschaften |

## 2.4 Wichtigste Regel

```text
Eigenschaften beschreiben.
Connectoren machen Geometrie handlungsfähig.
Ports definieren Kompatibilität.
Regeln prüfen Connectoren über Ports.
Nachweise verändern Status, Konfidenz, Warnung oder Blockade.
```

---

# 3. Paketübersicht

| Paket | Reales Objekt wird zu | Minimale Geometrie | Ergebnis |
|---|---|---|---|
| Basisgeometrie | neutraler Körper | Solid / Mesh / Flächen / Kanten | Maße, Volumen, rohe Geometrie |
| Tragwerk | Analysemodell | Linie, Platte, Knoten, Auflagerzone | Kräfte, Lastpfade, strukturelle Checks |
| Energie / Gebäudehülle | thermisches Modell | Fläche, Schicht, Kante, Durchdringung | U-Wert-Vorcheck, Wärmebrückenwarnung |
| TGA / Öffnungen | Leitungsmodell | Linie, Öffnung, Bohrzone, Sperrzone | Routen- und Konfliktprüfung |
| Semantik / Architektur | Entwurfsgriffmodell | Ausrichtungslinie, Sichtfläche, Zugangszone | Entwurfs- und Kompatibilitätschecks |
| Logistik / Montage | Handlingmodell | Transporthülle, Schwerpunkt, Hebezone | Hebe-, Lager-, Transportchecks |
| Nachweis-Overlay | Konfidenz- / Risiko-Overlay | Scanfläche, Schadenszone, Prüfpunkt | Statusänderung anderer Connectoren |

---

# 4. Paket 0 — Basisgeometrie

## 4.1 Abstraktionslogik

```text
Reales Bauteil
→ neutraler geometrischer Körper
→ messbare Geometrie
→ keine Connectoren
→ keine Ports
→ geometrische Messungen
```

## 4.2 Minimale Geometrie

```text
Solid / Mesh
Hauptflächen
Hauptkanten
rohe Öffnungen
Bounding Box
lokale Achsen
geometrisches Zentrum
```

## 4.3 Eigenschaften

```text
Typologie
Geometriequelle
Einheiten
Länge
Breite
Höhe / Dicke
Volumen
Flächen
Kanten
Öffnungen
Orientierung
Geometrie-Konfidenz
```

## 4.4 Connectoren und Ports

Keine.  
Basisgeometrie bleibt neutral.

Eine Kante wird erst im Tragwerk zur Auflagerkante.  
Eine Fläche wird erst in Energie zur thermischen Grenzfläche.  
Eine Öffnung wird erst in TGA zur nutzbaren Durchdringung.

## 4.5 Berechnung

```text
Geometrie + Einheiten
↓
Maße
Volumen
Flächen
Bounding Box
Schwerpunkt / geometrisches Zentrum
```

## 4.6 Beispiel A — Abbau/Aufbau DE_1OG_001

Die Deckenplatte wird in der Basisgeometrie als neutraler Plattenkörper gespeichert. Die Eigenschaften sind die Katalogmaße 4500 × 2300 × 180 mm, das Volumen 1.863 m³ und die Masse von ca. 4.1 t. Die Geometrie enthält Oberseite, Unterseite, Seitenflächen sowie lange und kurze Kanten.

Es gibt in diesem Paket keine Connectoren und keine Ports. Die langen Kanten sind noch keine Auflager, Fugen oder Sichtkanten.

## 4.7 Beispiel B — SlabBeamColumnFragment

Das Fragment wird als ein zusammenhängender monolithischer Körper gespeichert. Die Basisgeometrie erkennt rohe Teilregionen: einen Plattenbereich, einen integrierten Trägerbereich, einen Stützenabschnitt und Schnittflächen.

Diese Regionen sind keine getrennten Komponenten. Sie sind Teilgeometrien eines realen Bauteils. Connectoren entstehen erst in den fachlichen Paketen.

## 4.8 Beispiel C — ReCreate Hollow-Core Slab

Die Hohlkammerdecke wird als Fertigteil-Plattenkörper mit Längshohlräumen gespeichert. Die Basisgeometrie kennt Stirnflächen, Längskanten, Hohlräume und Nettovolumen.

Die Hohlräume sind zunächst nur geometrische Eigenschaften. Sie werden erst zu einer TGA-Route, wenn der Entwurf sie tatsächlich als Leitungsführung nutzt.

---

# 5. Paket 1 — Tragwerk

## 5.1 Abstraktionslogik

```text
Reales tragendes Bauteil
→ Tragwerksmodell
→ Linie / Platte / Knoten / Auflagerzone
→ Querschnitts- und Materialeigenschaften
→ strukturelle Connectoren
→ Ports
→ Gleichgewicht, Steifigkeit, Auflager- und Anschlusschecks
```

## 5.2 Minimale Geometrie

| Reale Geometrie | Tragwerksabstraktion |
|---|---|
| Träger | 1D-Linie |
| Stütze | 1D-vertikale Linie |
| Deckenplatte | 2D-Platte |
| Wand | 2D-Wandscheibe |
| lokales Auflager | Knoten oder Auflagerpatch |
| komplexes Fragment | Graph aus Platte, Linien, Knoten und Transferzonen |

## 5.3 Eigenschaften

```text
Querschnitt: Breite, Höhe, Fläche A, Trägheitsmoment I
Material: E-Modul, G-Modul
Dicke
Spannrichtung
Kapazitätsstatus
Bewehrungsstatus
Auflagerbedingung
Schadensrelevanz
```

## 5.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `bearing_support` | `bearing_side` / `support_side` | Last wird über Auflagerung übertragen |
| `joint_connection` | `member_side` | Bauteile werden entlang einer Seite / Fuge verbunden |
| `anchor_connection` | `anchor_side` | Verbindung über Anker, Schrauben, Dübel oder Bohrungen |
| `continuity_connection` | `continuity_side` | Kraftschluss oder Bewehrungskontinuität |
| `support_transfer` | `transfer_side` | Lastübertragung über Zwischenzone oder Transferknoten |

## 5.5 Berechnung / Check

```text
Linie / Platte / Knoten
+ Querschnitts- und Materialeigenschaften
+ Connectoren
+ Lasten
↓
Steifigkeit / Gleichgewicht / Kompatibilität
↓
Kräfte, Momente, Durchbiegung, Reaktionen, Warnungen
```

## 5.6 Beispiel A — Abbau/Aufbau Wand–Decke mit DE_1OG_001

**Komponenten:**  
DE_1OG_001 als Deckenplatte und eine wiederverwendete Wand.

**Repräsentation:**  
Die Decke wird als 2D-Platte repräsentiert. Die Wand wird als Wandscheibe mit Wandkopf-Auflager repräsentiert.

**Eigenschaften der Decke:**  
Dicke 180 mm, Masse ca. 4.1 t, Spannrichtung unbekannt oder abgeleitet, Kapazitätsstatus ingenieurpflichtig, Bewehrungsstatus abhängig von Nachweis.

**Konkrete Connectoren der Decke:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Plattenkante / Auflagerstreifen | Decke kann auf Wand aufliegen |
| `anchor_connection` | `anchor_side` | lokale Zone an Plattenkante | Schraubanker / Flachstahlhalter möglich |
| `continuity_connection` | `continuity_side` | Kantennahe Verguss- oder Bewehrungszone | nachträglicher Bewehrungsanschluss möglich |

**Konkrete Connectoren der Wand:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `support_side` | Wandkopf | Wand kann Decke tragen |
| `anchor_connection` | `support_side` | Ankeraufnahmezone am Wandkopf | Wand nimmt Anker auf |
| `continuity_connection` | `continuity_side` | Anschlusszone am Wandkopf | Kraftschluss über Verguss / Bewehrung |

**Regeln:**  
`bearing_side → support_side` prüft Auflagerüberlappung, Richtung und Mindestauflager.  
`anchor_side → support_side` prüft Randabstand, Bewehrungskonflikt und Ankerbarkeit.  
`continuity_side → continuity_side` prüft Bewehrungskontinuität, Vergussraum und Kraftschluss.

**Abbau/Aufbau-Mapping:**  
Schraubanker und Flachstahlhalter werden über `anchor_connection` abgebildet.  
Nachträglicher Bewehrungsanschluss + Verguss wird über `continuity_connection` abgebildet.

## 5.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Ein monolithisches Fragment aus Plattenbereich, integriertem Trägerbereich und Stützenabschnitt.

**Repräsentation:**  
Nicht als unscharfes `monolithic_structural_fragment`, sondern als kleiner Tragwerksgraph:

```text
Plattenbereich → 2D-Platte
Trägerbereich → 1D-Trägerlinie
Stützenabschnitt → 1D-Stützenlinie
Schnittpunkt Platte / Träger / Stütze → Transferknoten
Schnittfläche → Kontinuitätszone
```

**Eigenschaften:**  
Monolithischer Zusammenhang, unbekannte innere Bewehrung, Schnittflächenstatus, Transferknotenstatus, Kapazitätsstatus ingenieurpflichtig.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Rand des Plattenbereichs | Fragment kann aufliegen |
| `support_transfer` | `transfer_side` | Trägerlinie / Transferknoten | Last läuft durch Trägerregion |
| `bearing_support` | `support_side` | Stützenfuß oder Stützenkopf | Stützenregion nimmt Last auf oder gibt sie ab |
| `continuity_connection` | `continuity_side` | Schnittfläche | kraftschlüssige Verbindung zu neuem Träger / neuer Struktur |

**Regeln:**  
`transfer_side → support_side` prüft den Lastpfad über Trägerlinie und Stützenlinie.  
`continuity_side → continuity_side` prüft Schnittflächengeometrie, Bewehrungsnachweis und Kraftschluss.  
`bearing_side → support_side` prüft lokale Auflagerung und Pressung.

## 5.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Wiedergewonnene Hohlkammerdecke.

**Repräsentation:**  
Einachsig spannende Fertigteilplatte. Die Hohlkammern bleiben Eigenschaften der Geometrie, nicht automatisch Connectoren.

**Eigenschaften:**  
Spannrichtung entlang der Hohlkammern, Endauflagerstatus, Längsfugenstatus, Nassverbindungs- oder Fugenhistorie, Kapazitätsstatus abhängig von Prüfung oder Neuberechnung.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Stirnseite A | erstes Auflager |
| `bearing_support` | `bearing_side` | Stirnseite B | zweites Auflager |
| `joint_connection` | `member_side` | Längsfuge | Verbindung / Toleranz zur Nachbarplatte |

**Regeln:**  
Endauflager prüfen Auflagerlänge, Richtung und Toleranz.  
Längsfugen prüfen Ausrichtung, Fugenbreite und Wiederverbindungsdetail.  
Tragfähigkeit bleibt abhängig von Test oder Neuberechnung.

---

# 6. Paket 2 — Energie / Gebäudehülle

## 6.1 Abstraktionslogik

```text
Reales Hüllenbauteil
→ thermisches Modell
→ Fläche / Schicht / Kante / Durchdringung
→ thermische Eigenschaften
→ Hüllen-Connectoren
→ Ports
→ U-Wert-, Kontinuitäts-, Abdichtungs- und Wärmebrückenchecks
```

## 6.2 Minimale Geometrie

```text
thermische Grenzfläche
Schichtdicke
Innen-/Außenseite
Kanten
Durchdringungsrand
Wärmebrückenzone
```

## 6.3 Eigenschaften

```text
Dicke d
Wärmeleitfähigkeit λ
thermischer Widerstand R
U-Wert-Status
Fläche
Innen-/Außenstatus
Dämmstatus
Feuchterisiko
Luftdichtheitsstatus
```

## 6.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `thermal_continuity` | `thermal_side` | thermische Grenze muss weiterlaufen |
| `insulation_continuity` | `insulation_side` | Dämmschicht muss weiterlaufen |
| `penetration_sealing` | `penetration_side` | Durchdringung muss abgedichtet werden |
| `thermal_bridge_warning` | `bridge_side` | Wärmebrückenrisiko als Warnzone |

## 6.5 Berechnung / Check

```text
Fläche + Dicke + λ
↓
R = d / λ
↓
U = 1 / ΣR
↓
U-Wert-Vorcheck
```

Für Anschlüsse:

```text
thermische Fläche + Rand / Durchdringung
↓
Kontinuitäts-, Abdichtungs- oder Wärmebrückencheck
```

## 6.6 Beispiel A — Abbau/Aufbau 200-mm-Stahlbetonwand

**Komponente:**  
Wiederverwendete 200-mm-Stahlbetonwand als Außenwand.

**Repräsentation:**  
Thermische Grenzfläche mit Innen- und Außenseite.

**Eigenschaften:**  
Dicke 200 mm, Lambda-Status gemessen oder projektseitig angenommen, U-Wert nur als Vorcheck, Dämmstatus abhängig vom Wandaufbau.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | äußere Wandfläche | Dämmung muss anschließen |
| `thermal_continuity` | `thermal_side` | Wandrand / Anschlusskante | thermische Grenze läuft weiter |
| `penetration_sealing` | `penetration_side` | Öffnungsrand, falls vorhanden | Durchdringung muss abgedichtet werden |

**Regeln:**  
Dämmkontinuität prüft Lücken.  
Thermische Kontinuität prüft Grenzflächenanschluss.  
Durchdringungsabdichtung prüft Luftdichtheit und Feuchterisiko.

## 6.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Platten-Träger-Stützen-Fragment.

**Repräsentation:**  
Nur aktiv, wenn das Fragment Teil der Hülle wird. Sonst bleibt das Energiepaket kontextabhängig.

**Eigenschaften:**  
Hüllenkontext unbekannt oder gesetzt, Knotenbereiche als potenzielle Wärmebrücken, Schnittflächen als potenzielle thermische Anschlussflächen.

**Konkrete Connectoren bei Hüllennutzung:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `thermal_continuity` | `thermal_side` | Schnittfläche | thermischer Anschluss |
| `thermal_bridge_warning` | `bridge_side` | Platten-Träger-Stützen-Knoten | Wärmebrückenwarnung |

**Regeln:**  
Thermische Kontinuität prüft Anschluss an Nachbarhüllenelement.  
Wärmebrückenwarnung prüft, ob der monolithische Knoten die thermische Grenze durchstößt.

## 6.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke, wenn als Dach oder außenliegende Decke verwendet.

**Repräsentation:**  
Thermische Grenzfläche mit Hohlräumen als thermisch relevanter Eigenschaft.

**Eigenschaften:**  
Dicke, Hohlkammerstatus, Dämmstatus, Hüllenkontext, U-Wert-Status.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | Oberseite bei Dachnutzung | Dämmschicht läuft über Platte |
| `thermal_bridge_warning` | `bridge_side` | Plattenkante | Wärmebrückenrisiko |
| `penetration_sealing` | `penetration_side` | Öffnungs- oder Durchdringungsrand | Abdichtung erforderlich |

---

# 7. Paket 3 — TGA / Öffnungen

## 7.1 Abstraktionslogik

```text
Reale Öffnung / Leitung / Schacht
→ Routenmodell
→ Linie / Knoten / Öffnung / Bohrzone / Sperrzone
→ Eigenschaften
→ TGA-Connectoren
→ Ports
→ Durchmesser-, Lichtraum-, Konflikt- und Dichtungschecks
```

## 7.2 Minimale Geometrie

```text
Routenlinie
Öffnungsrand
Öffnungsachse
Bohrzentrum
Bohrdurchmesser
Sperrzone
Lichtraum
```

## 7.3 Eigenschaften

```text
Öffnungsgröße
Öffnungstiefe
Leitungsdurchmesser
Randabstand
Lichtraumstatus
Bohrstatus
Bezug zu Tragwerkszonen
Bezug zur Bewehrung
Brandschutz- / Schallschutzstatus
```

## 7.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `route_continuity` | `route_side` | Leitung kann weitergeführt werden |
| `opening_use` | `opening_side` | bestehende Öffnung wird genutzt |
| `drilling_candidate` | `drilling_side` | neue Bohrung wird vorgeschlagen |
| `blocked_conflict` | `blocked_side` | Zone blockiert Route oder Bohrung |

## 7.5 Berechnung / Check

```text
Routenlinie + Öffnung + Durchmesser
↓
passt Durchmesser?
ist Lichtraum frei?
Randabstand ok?
Konflikt mit Tragwerk / Bewehrung?
Brandschutz / Schallschutz nötig?
```

## 7.6 Beispiel A — Abbau/Aufbau Öffnung

**Komponente:**  
Wiederverwendete Platte oder Wand mit katalogisierter Öffnung.

**Repräsentation:**  
Öffnungsmodell.

**Eigenschaften:**  
Öffnungsmaß, Tiefe, Randabstand, Bezug zu Tragwerkszonen, Bewehrungsstatus unbekannt oder nachgewiesen.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `opening_use` | `opening_side` | Öffnungsrand / Öffnungsachse | bestehende Öffnung wird genutzt |
| `route_continuity` | `route_side` | geplante Leitung | Leitung soll durch Öffnung laufen |

**Regeln:**  
`opening_side → route_side` prüft Durchmesser, Randabstand und Tragwerkskonflikt.  
`route_side → route_side` prüft Leitungsflucht und Lichtraum.

## 7.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Platten-Träger-Stützen-Fragment.

**Repräsentation:**  
Bohr- und Sperrzonenmodell.

**Eigenschaften:**  
Träger- und Stützenregion als sensible Lastzonen, Bohrstatus unbekannt, Bewehrungsstatus nachweispflichtig.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `drilling_candidate` | `drilling_side` | plattenartige Region | mögliche neue Bohrung |
| `blocked_conflict` | `blocked_side` | Trägerregion / Stützenregion | Leitung oder Bohrung kritisch |

**Regeln:**  
Bohrkandidat prüft Bewehrung, Tragwerkszone und Randabstand.  
Blockierte Zone erzeugt Konflikt mit Route oder Bohrung.

## 7.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Routen- oder Hohlraummodell.

**Eigenschaften:**  
Hohlkammerachse, Hohlraumgröße, Bohrstatus, strukturelle Konfliktzonen.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `route_continuity` | `route_side` | Hohlkammerachse, falls genutzt | Leitung könnte im Hohlraum laufen |
| `drilling_candidate` | `drilling_side` | geplante Bohrzone | neue Durchdringung möglich |

**Regeln:**  
Hohlraumroute prüft Kontinuität und Durchmesser.  
Bohrkandidat prüft Durchmesser, Bewehrung und Tragwerkskonflikt.

---

# 8. Paket 4 — Semantik / Architektur

## 8.1 Abstraktionslogik

```text
Reales Bauteil als Entwurfselement
→ Design-Handle-Modell
→ Ausrichtungslinie / Sichtfläche / Zugangszone / Seitenbezug
→ architektonische Eigenschaften
→ semantische Connectoren
→ Ports
→ Ausrichtungs-, Sichtbarkeits-, Zugangs- und Raumchecks
```

## 8.2 Minimale Geometrie

```text
Ausrichtungslinie
Fugenlinie
Sichtfläche
Zugangszone
Seitenfläche als Raumbezug
Öffnungsachse
Stapel- oder Niveaufläche
```

## 8.3 Eigenschaften

```text
architektonische Rolle
räumliche Rolle
Sichtbarkeitsstatus
Wiederverwendungsausdruck
Oberflächenzustand
Rasterbezug
Raumbezug
Fassadenbezug
Orientierung
Entwurfspräferenz-Relevanz
```

## 8.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `access_handle` | `access_port` | Zugang / Annäherung / Durchgang |
| `attachment_handle` | `attachment_port` | architektonische Anbindung |
| `stack_handle` | `top_port` / `bottom_port` | Stapelung / vertikale Beziehung |
| `side_handle` | `side_port` | Seite, Raumgrenze, Orientierung |
| `opening_handle` | `opening_port` | architektonische Öffnung |
| `alignment_handle` | `alignment_port` | Raster, Fuge, Datum, Rhythmus |
| `visibility_constraint_handle` | `visibility_port` | Sichtbarkeit / Verdeckung |

## 8.5 Berechnung / Check

```text
Design-Griffe + Platzierung + Zielpräferenzen
↓
Ausrichtung
Sichtbarkeit
Zugang
Raumgrenze
Fassadenrhythmus
Wiederverwendungsausdruck
```

## 8.6 Beispiel A — Abbau/Aufbau DE_1OG_001

**Komponente:**  
Deckenplatte DE_1OG_001.

**Repräsentation:**  
Architektonisches Plattenmodell.

**Eigenschaften:**  
Mögliche Bodenfläche, mögliche sichtbare Deckenuntersicht, Rastermaß, Oberflächenstatus, Wiederverwendungsausdruck.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | lange Plattenkante / Fugenlinie | Fuge oder Raster ausrichten |
| `visibility_constraint_handle` | `visibility_port` | Plattenunterseite, falls sichtbar | Untersicht bleibt sichtbar / wird bewertet |

**Regeln:**  
`alignment_port → alignment_port` prüft Fugen- und Rasterausrichtung.  
`visibility_port` prüft Sichtbarkeit, Verdeckung und Oberflächenwarnung.

## 8.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Monolithisches Fragment mit Platten-, Träger- und Stützenregion.

**Repräsentation:**  
Architektonisches Fragmentmodell.

**Eigenschaften:**  
Nische, Stütze-im-Raum, räumliche Schwelle, sichtbare Wiederverwendungsidentität, Schnittflächencharakter.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `access_handle` | `access_port` | Nischenzugang | Annäherung / Zugang prüfen |
| `side_handle` | `side_port` | Stützenseite zum Raum | Raumbeziehung prüfen |
| `alignment_handle` | `alignment_port` | Schnittkante oder Trägerlinie | Ausrichtung an Raster / Datum |
| `visibility_constraint_handle` | `visibility_port` | sichtbare Fragmentflächen | Lesbarkeit und Wiederverwendungsausdruck |

**Regeln:**  
Zugang prüft Lichtraum und Annäherung.  
Seitenbezug prüft Raumgrenze.  
Ausrichtung prüft Raster, Fuge und Datum.  
Sichtbarkeit prüft Verdeckung und Oberflächenzustand.

## 8.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Architektonisches Fertigteilmodell.

**Eigenschaften:**  
Modulmaß, Längsfuge, mögliche sichtbare Unterseite, Wiederverwendungsausdruck optional.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | Längsfuge | Modul- und Fugenausrichtung |
| `stack_handle` | `top_port` | Oberseite | vertikale Relation / Niveau |
| `stack_handle` | `bottom_port` | Unterseite | Gegenstück zur vertikalen Relation |
| `visibility_constraint_handle` | `visibility_port` | Unterseite, falls sichtbar | sichtbare Wiederverwendung |

**Regeln:**  
Ausrichtung prüft Modul und Fuge.  
`top_port → bottom_port` prüft Niveau und vertikale Ausrichtung.  
Sichtbarkeit prüft Oberfläche und Verdeckung.

---

# 9. Paket 5 — Logistik / Montage

## 9.1 Abstraktionslogik

```text
Reales Bauteil im Prozess
→ Handlingmodell
→ Transporthülle / Schwerpunkt / Hebezone / Lagerauflager
→ Logistik-Eigenschaften
→ Handling-Connectoren
→ Ports
→ Hebe-, Lager-, Transport- und Montagechecks
```

## 9.2 Minimale Geometrie

```text
Transporthülle
Schwerpunkt
Hebekandidaten
Lagerauflager
Montagezugang
Schutzzonen
temporäre Abstützzonen
```

## 9.3 Eigenschaften

```text
Masse
Transportmaße
Schwerpunktstatus
Lagerorientierung
Hebestatus
Zugangsstatus
Schutzstatus
temporäre Abstützung
Transportstatus
```

## 9.4 Minimale Connectoren und Ports

| Connector | Port | Bedeutung |
|---|---|---|
| `lifting_handle` | `lifting_port` | Heben / Kran |
| `storage_handle` | `storage_port` | Lagerung / Lagerauflager |
| `transport_handle` | `transport_port` | Transporthülle / Ladungssicherung |
| `access_handle` | `access_port` | Montagezugang |
| `protection_handle` | `protection_port` | Schutz sensibler Zonen |
| `temporary_bracing_handle` | `temporary_bracing_port` | temporäre Stabilisierung |

## 9.5 Berechnung / Check

```text
Handling-Geometrie + Masse + Prozessbedingungen
↓
Hebbarkeit
Lagerstabilität
Transporthülle
Montagezugang
Schutzbedarf
temporäre Abstützung
```

## 9.6 Beispiel A — Abbau/Aufbau DE_1OG_001

**Komponente:**  
Deckenplatte DE_1OG_001.

**Repräsentation:**  
Handlingmodell.

**Eigenschaften:**  
Masse ca. 4.1 t, Transportmaße 4500 × 2300 × 180 mm, liegende Lagerung empfohlen, Hebestatus nachweispflichtig.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `storage_handle` | `storage_port` | Unterseite / Lagerauflagerzonen | liegende Lagerung |
| `transport_handle` | `transport_port` | Transporthülle | Transport und Ladungssicherung |
| `lifting_handle` | `lifting_port` | Hebekandidatenzone | Hebbarkeit |
| `protection_handle` | `protection_port` | Kanten / Oberflächen | Schutz gegen Schäden / Witterung |

**Regeln:**  
Lagerung prüft Orientierung, Auflagerabstand und Trennhölzer.  
Transport prüft Maße und Ladungssicherung.  
Heben prüft Schwerpunkt und Hebe-Nachweis.  
Schutz prüft Kanten- und Witterungsschutz.

## 9.7 Beispiel B — SlabBeamColumnFragment

**Komponente:**  
Unregelmäßiges monolithisches Fragment.

**Repräsentation:**  
Komplexes Handlingmodell.

**Eigenschaften:**  
Unregelmäßiger Schwerpunkt, Schnittflächen, mögliche Instabilität, Schutzbedarf, Hebestatus ingenieurpflichtig.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | ein oder zwei Hebekandidaten | Fragment heben |
| `storage_handle` | `storage_port` | stabile Lagerauflagerzonen | kippsichere Lagerung |
| `protection_handle` | `protection_port` | Schnittflächen / empfindliche Kanten | Schutz |
| `temporary_bracing_handle` | `temporary_bracing_port` | Stützen- oder Trägerregion | temporäre Stabilisierung |

**Regeln:**  
Heben prüft Schwerpunkt, Hebbarkeit und Kran-Zugang.  
Lagerung prüft Kippstabilität.  
Schutz prüft Schnittflächen und empfindliche Kanten.  
Temporäre Abstützung prüft Montagezugang und Stabilität.

## 9.8 Beispiel C — ReCreate Hollow-Core Slab

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Transport- und Hebemodell.

**Eigenschaften:**  
Transporthistorie, Hebevorgang, Lagerstatus, QR-Tracking als Nachweis, nicht als Logistikconnector.

**Konkrete Connectoren:**

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | Hebezonen | Element heben |
| `transport_handle` | `transport_port` | Transportauflager / Transporthülle | Transport prüfen |
| `storage_handle` | `storage_port` | Lagerauflager | Lagerung prüfen |

**Regeln:**  
Heben prüft Hebbarkeit, Schwerpunkt und Beschädigungsrisiko.  
Transport prüft Ladungssicherung und Transporthülle.  
Lagerung prüft Auflagerabstand und Orientierung.

---

# 10. Paket 6 — Nachweis-Overlay

## 10.1 Abstraktionslogik

```text
Realer Nachweis
→ Konfidenz- / Risiko-Overlay
→ Scanfläche / Schadenszone / Prüfpunkt / unbekannte Zone
→ Nachweiseigenschaften
→ keine Connectoren
→ keine Ports
→ Statusmodifikation anderer Connectoren
```

## 10.2 Minimale Geometrie

```text
Scanbereich
Bewehrungslinie
Schadenszone
Risslinie
Prüfpunkt
Fotozuordnung
unbekannte Zone
Konfidenzzone
```

## 10.3 Eigenschaften

```text
Nachweistyp
Ort
Konfidenz
Quelle
Datum
betroffenes Paket
betroffener Connector
betroffener Port
Effekt
Begründung
```

## 10.4 Connectoren und Ports

Keine.

Nachweise erzeugen keine neuen Connectoren.  
Sie verändern vorhandene Connectoren.

## 10.5 Berechnung / Check

```text
Nachweisgeometrie
+ Connectorgeometrie
↓
Überlappungsprüfung
↓
bestätigt / Warnung / blockiert / Konfidenz reduziert
```

## 10.6 Beispiel A — Abbau/Aufbau Bewehrungsnachweis

**Komponente:**  
Wand oder Deckenplatte mit möglicher Ankerverbindung.

**Repräsentation:**  
Bewehrungs-Overlay.

**Eigenschaften:**  
Scanstatus, Bewehrungslage, Konfidenz, betroffener Connector `anchor_connection`.

**Wirkung:**  
Wenn eine unbekannte Bewehrungszone den Ankerbereich überlagert, wird `anchor_connection` blockiert oder als Warnung markiert. Wenn der Scan eine freie Zone bestätigt, kann die Verbindung zur Ingenieurprüfung weitergehen.

## 10.7 Beispiel B — SlabBeamColumnFragment Schnittfläche

**Komponente:**  
SlabBeamColumnFragment.

**Repräsentation:**  
Schnittflächen-, Rebar- und Schadensoverlay.

**Eigenschaften:**  
Schnittflächenstatus, mögliche freiliegende Bewehrung, Schaden, Konfidenz.

**Betroffene Connectoren:**  
`continuity_connection`, `support_transfer`, `visibility_constraint_handle`.

**Wirkung:**  
Unbekannte Bewehrung an der Schnittfläche macht `continuity_connection` ingenieurpflichtig. Schaden im Lasttransferbereich warnt `support_transfer`. Schaden auf sichtbaren Flächen warnt `visibility_constraint_handle`.

## 10.8 Beispiel C — ReCreate QR / Test / Neuberechnung

**Komponente:**  
Hohlkammerdecke.

**Repräsentation:**  
Tracking-, Test- und Neuberechnungs-Overlay.

**Eigenschaften:**  
QR-ID, BIM-Inventarstatus, Teststatus, Neuberechnungsstatus, betroffene Connectoren.

**Betroffene Connectoren:**  
`bearing_support`, `joint_connection`, `lifting_handle`.

**Wirkung:**  
QR-Tracking bestätigt Identität und Rückverfolgbarkeit. Tests oder Neuberechnung erhöhen strukturelle Konfidenz. Unklare Fugenschäden markieren `joint_connection` als manuell zu prüfen.

---

# 11. Kompatibilitätsregeln kompakt

| Regel | Ports | Checks |
|---|---|---|
| strukturelles Auflager | `bearing_side → support_side` | Überlappung, Richtung, Auflagerlänge |
| strukturelle Verankerung | `anchor_side → support_side` | Randabstand, Bewehrung, Ankerbarkeit |
| strukturelle Kontinuität | `continuity_side → continuity_side` | Bewehrungskontinuität, Verguss, Kraftschluss |
| struktureller Transfer | `transfer_side → support_side / bearing_side` | Lastpfad, lokale Pressung |
| thermische Kontinuität | `thermal_side → thermal_side` | thermische Grenzfortsetzung |
| Dämmkontinuität | `insulation_side → insulation_side` | Schichtfortsetzung, Lücken |
| Hüllendurchdringung | `penetration_side → thermal_side / insulation_side` | Abdichtung, Luftdichtheit, Feuchte |
| TGA-Route | `route_side → route_side` | Leitungsflucht, Lichtraum |
| TGA-Öffnung | `opening_side → route_side` | Durchmesser, Randabstand, Konflikt |
| TGA-Bohrung | `drilling_side → route_side` | Bewehrung, Tragwerkszone, Randabstand |
| architektonischer Zugang | `access_port → access_port` | Lichtraum, Annäherung |
| architektonische Stapelung | `top_port → bottom_port` | Niveau, vertikale Ausrichtung |
| architektonische Ausrichtung | `alignment_port → alignment_port` | Raster, Fuge, Datum |
| Logistik Heben | `lifting_port → Prozessanforderung` | Schwerpunkt, Hebbarkeit |
| Logistik Lagerung | `storage_port → Lagerbedingung` | Orientierung, Auflager, Trennhölzer |

---

# 12. Gesamtabstraktion der drei Beispiele

## 12.1 Abbau/Aufbau DE_1OG_001

| Paket | Repräsentation | Connectoren |
|---|---|---|
| Basisgeometrie | neutraler Plattenkörper | keine |
| Tragwerk | 2D-Platte | `bearing_support`, `anchor_connection`, `continuity_connection` |
| Energie | thermische Grenzfläche, falls Hülle | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Öffnungs- oder Bohrmodell | `opening_use`, `drilling_candidate` |
| Semantik | architektonisches Plattenmodell | `alignment_handle`, `visibility_constraint_handle` |
| Logistik | Handlingmodell | `storage_handle`, `transport_handle`, `lifting_handle`, `protection_handle` |
| Nachweis | Rebar / Material / Schaden | keine; modifiziert andere |

## 12.2 SlabBeamColumnFragment

| Paket | Repräsentation | Connectoren |
|---|---|---|
| Basisgeometrie | monolithischer Körper mit Teilregionen | keine |
| Tragwerk | Platte + Trägerlinie + Stützenlinie + Transferknoten | `bearing_support`, `support_transfer`, `continuity_connection` |
| Energie | nur bei Hüllennutzung | `thermal_continuity`, `thermal_bridge_warning` |
| TGA | Bohr- und Sperrzonenmodell | `drilling_candidate`, `blocked_conflict` |
| Semantik | architektonisches Fragmentmodell | `access_handle`, `side_handle`, `alignment_handle`, `visibility_constraint_handle` |
| Logistik | komplexes Handlingmodell | `lifting_handle`, `storage_handle`, `protection_handle`, `temporary_bracing_handle` |
| Nachweis | Schnittflächen / Rebar / Schaden | keine; modifiziert andere |

## 12.3 ReCreate Hollow-Core Slab

| Paket | Repräsentation | Connectoren |
|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | keine |
| Tragwerk | einachsig spannende Fertigteilplatte | `bearing_support`, `joint_connection` |
| Energie | Hülle, falls Dach / Außenboden | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Hohlraum- oder Bohrmodell | `route_continuity`, `drilling_candidate` |
| Semantik | Modul- und Fugenausrichtungsmodell | `alignment_handle`, `stack_handle`, optional `visibility_constraint_handle` |
| Logistik | Hebe-, Transport- und Lagermodell | `lifting_handle`, `transport_handle`, `storage_handle` |
| Nachweis | BIM / QR / Test / Neuberechnung | keine; modifiziert andere |

---

# 13. Finale Regel

Das Trägerbeispiel ist die Vorlage für alle Pakete:

```text
Träger im Tragwerksmodell
= Linie + Querschnittseigenschaften + Knotenanschlüsse + Steifigkeitsberechnung
```

Analog dazu:

```text
Deckenplatte im Tragwerk
= Platte + Dicke / Material + Auflagerconnectoren + Plattenchecks

Wand in Energie
= thermische Fläche + Schichteigenschaften + Hüllenconnectoren + U-Wert- / Wärmebrückenchecks

Öffnung in TGA
= Öffnungsgeometrie + Durchmesser / Randabstand + Routenconnectoren + Konfliktchecks

Fragment in Semantik
= Designgriffe + räumliche Eigenschaften + Sichtbarkeits- / Ausrichtungsconnectoren + Entwurfschecks

Bauteil in Logistik
= Handlingkörper + Masse / Schwerpunkt + Hebe- / Lagerconnectoren + Prozesschecks

Nachweis
= Overlay + Konfidenz + betroffene Connectoren + Statusmodifikation
```

So bleibt das System minimal, aber jedes Paket wird rechnerisch, prüfbar und anschlussfähig.
