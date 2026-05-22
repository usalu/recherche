# Minimale Pakete, Connectoren und Ports  
## Deutsche, konkrete Version mit drei Beispielen pro Paket

**Ziel**  
Dieses Dokument beschreibt das neue Komponentensystem in einer kompakten, aber konkreten Form.

Das allgemeine System bleibt minimal.  
Die Beispiele zeigen dagegen konkret:

```text
Welche Komponente?
Welche Paket-Repräsentation?
Welche Eigenschaften?
Welche Connectoren?
Welche Ports?
Welche Regeln / Checks?
```

Das System folgt dieser Struktur:

```text
Komponente
→ Paket
→ Repräsentation
→ Eigenschaften
→ Connectoren
→ Ports
→ Regeln / Checks
```

---

# 1. Quellenbasis und Beispiele

## 1.1 Abbau/Aufbau DE_1OG_001

**Quelle:** Abbau/Aufbau-Handbuch, Bauteilkatalog.  
Das Handbuch beschreibt den Bauteilkatalog mit ID, Skizze, Maßen, Öffnungsmaßen, Volumen und Masse. Es nennt als Beispiel die Deckenplatte **DE_1OG_001** mit:

```text
Typologie: Deckenplatte
Maße: 4500 × 2300 × 180 mm
Volumen: 1.863 m³
Masse: ca. 4.1 t
```

Dieses Beispiel wird als **einzelnes, katalogisiertes Bauteil** verwendet.

## 1.2 SlabBeamColumnFragment

**Quelle:** Abbau/Aufbau Masterarbeit 2020.  
Die Masterarbeit beschreibt räumlich interessante Fragmente wie:

```text
Stützen vor Fenstern
Nische hinter Stütze
Große Stütze in kleinem Raum
```

Sie beschreibt außerdem, dass zugeschnittene Elemente auf einem Halbfertigteilträger aus Stahlbeton ruhen und über einen nachträglichen Bewehrungsanschluss kraftschlüssig mit dem neuen Träger verbunden werden.

**Systembeispiel:**  
`SlabBeamColumnFragment` ist kein benanntes Originalbauteil aus der Quelle. Es ist eine vorgeschlagene Systemtypologie für ein monolithisches Betonfragment mit:

```text
Plattenbereich
integriertem Trägerbereich
Stützenabschnitt
Schnittflächen
räumlicher Fragmentqualität
```

## 1.3 ReCreate Hollow-Core Slab

**Quelle:** ReCreate-Pilotprojekte Niederlande und Finnland.  
Der niederländische Pilot beschreibt Hohlkammerdecken, tragende Fassaden, Nassverbindungen, Sägen entlang der Längsfugen, Heben, Transport und Wiederverwendung. Der finnische Pilot beschreibt BIM-Inventarisierung, QR-Codes, Lagerung, Tests und Neuberechnung.

Dieses Beispiel wird als **wiedergewonnene Hohlkammerdecke / precast hollow-core slab** verwendet.

---

# 2. Grundregel des Systems

## 2.1 Was wird modelliert?

Nicht jedes Detail wird modelliert.  
Ein Detail wird nur modelliert, wenn es für mindestens eine dieser Funktionen gebraucht wird:

```text
Verbindung
Berechnung
Warnung
Kompatibilität
Entwurfsentscheidung
```

## 2.2 Begriffe

| Begriff | Bedeutung |
|---|---|
| **Komponente** | reales wiederverwendetes Bauteil oder Fragment |
| **Paket** | fachliche Sicht auf die Komponente |
| **Repräsentation** | vereinfachtes Modell der Komponente innerhalb eines Pakets |
| **Eigenschaft** | beschreibender Wert ohne eigene Handlung |
| **Connector** | platzierter, handlungsrelevanter Griffpunkt |
| **Port** | semantischer Kompatibilitätstyp eines Connectors |
| **Regel / Check** | prüft, ob zwei Connectoren mit kompatiblen Ports wirklich funktionieren |

## 2.3 Wichtige Unterscheidung

```text
Eigenschaft:
beschreibt etwas

Connector:
macht etwas prüfbar oder verbindbar

Port:
sagt, womit der Connector kompatibel ist
```

Beispiel:

```text
„Unterseite ist sichtbar“ = Eigenschaft

„Unterseite darf nicht verdeckt werden“ = Connector

„visibility_port“ = Port, über den Sichtbarkeitsregeln laufen
```

---

# 3. Minimale Paketstruktur

```text
0. Basisgeometrie
1. Tragwerk
2. Energie / Gebäudehülle
3. TGA / Öffnungen
4. Semantik / Architektur
5. Logistik / Montage
6. Nachweis-Overlay
```

## 3.1 Minimale Connectoren und Ports

| Paket | Connectoren | Ports |
|---|---|---|
| Basisgeometrie | keine | keine |
| Tragwerk | `bearing_support`, `joint_connection`, `anchor_connection`, `continuity_connection`, `support_transfer` | `bearing_side`, `support_side`, `member_side`, `anchor_side`, `continuity_side`, `transfer_side` |
| Energie / Gebäudehülle | `thermal_continuity`, `insulation_continuity`, `penetration_sealing`, `thermal_bridge_warning` | `thermal_side`, `insulation_side`, `penetration_side`, `bridge_side` |
| TGA / Öffnungen | `route_continuity`, `opening_use`, `drilling_candidate`, `blocked_conflict` | `route_side`, `opening_side`, `drilling_side`, `blocked_side` |
| Semantik / Architektur | `access_handle`, `attachment_handle`, `stack_handle`, `side_handle`, `opening_handle`, `alignment_handle`, `visibility_constraint_handle` | `access_port`, `attachment_port`, `top_port`, `bottom_port`, `side_port`, `opening_port`, `alignment_port`, `visibility_port` |
| Logistik / Montage | `lifting_handle`, `storage_handle`, `transport_handle`, `access_handle`, `protection_handle`, `temporary_bracing_handle` | `lifting_port`, `storage_port`, `transport_port`, `access_port`, `protection_port`, `temporary_bracing_port` |
| Nachweis-Overlay | keine | keine |

---

# 4. Paket 0 — Basisgeometrie

## Allgemein

Die Basisgeometrie ist die neutrale Form der Komponente.  
Sie erzeugt keine Connectoren und keine Ports.

Sie speichert nur:

```text
Typologie
Geometriequelle
Einheiten
lokale Achsen
Bounding Box
Maße
Volumen
Hauptflächen
Hauptkanten
rohe Öffnungen
geometrisches Zentrum
Geometrie-Konfidenz
```

Eine Fläche, Kante oder Öffnung wird erst dann zum Connector, wenn ein anderes Paket ihr eine fachliche Bedeutung gibt.

---

## Beispiel 0A — Abbau/Aufbau DE_1OG_001

| Feld | Inhalt |
|---|---|
| Komponente | DE_1OG_001 |
| Typologie | Deckenplatte |
| Repräsentation | neutraler Plattenkörper |
| Eigenschaften | 4500 × 2300 × 180 mm, 1.863 m³, ca. 4.1 t, Oberseite, Unterseite, Seitenflächen, lange und kurze Kanten |
| Connectoren | keine |
| Ports | keine |
| Regel | Nur prüfen, ob Geometrie, Maße und Volumen vorhanden sind |

**Warum keine Connectoren?**  
Die langen Kanten sind nur geometrische Kanten. Ob sie später Auflagerkante, Fuge, Sichtkante, Transportkante oder Wärmebrücke werden, entscheiden andere Pakete.

---

## Beispiel 0B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Typologie | monolithisches Betonfragment |
| Repräsentation | ein zusammenhängender Körper mit Teilregionen |
| Eigenschaften | Plattenregion, integrierte Trägerregion, Stützenregion, Schnittflächen, rohe Kanten, Schwerpunkt, Gesamtvolumen |
| Connectoren | keine |
| Ports | keine |
| Regel | Nur prüfen, ob die Teilregionen geometrisch identifizierbar sind |

**Wichtig:**  
Das Fragment ist ein Bauteil, nicht drei Bauteile. Die Teilregionen sind nur geometrische Subregionen.

---

## Beispiel 0C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | wiedergewonnene Hohlkammerdecke |
| Typologie | precast hollow-core slab |
| Repräsentation | neutraler Fertigteil-Plattenkörper |
| Eigenschaften | Länge, Breite, Dicke, Längshohlräume, Stirnflächen, Längskanten, Nettovolumen |
| Connectoren | keine |
| Ports | keine |
| Regel | Prüfen, ob Körper, Hohlräume und Stirnflächen erkannt sind |

**Wichtig:**  
Die Hohlräume sind zunächst Eigenschaften. Sie werden erst zu TGA-Connectoren, wenn sie tatsächlich als Leitungsführung genutzt werden.

---

# 5. Paket 1 — Tragwerk

## Allgemein

Das Tragwerkspaket beschreibt nur, wo Kräfte übertragen, aufgenommen, weitergeleitet oder kraftschlüssig verbunden werden können.

## Repräsentationslogik

| Reale Geometrie | Abstrakte Tragwerksrepräsentation |
|---|---|
| Deckenplatte | Platte |
| Wand | Wandscheibe |
| Träger | Trägerlinie |
| Stütze | Stützenlinie |
| lokales Auflager | Auflagerknoten |
| Schnittfläche mit Anschlussbedarf | Kontinuitätszone |
| komplexes Fragment | Graph aus Platte, Trägerlinie, Stützenlinie, Transferknoten |

## Minimale Connectoren und Ports

| Connector | Port | Wann verwenden? |
|---|---|---|
| `bearing_support` | `bearing_side` oder `support_side` | wenn Last über Auflagerung übertragen wird |
| `joint_connection` | `member_side` | wenn Bauteile entlang einer Fuge oder Seite gefügt werden |
| `anchor_connection` | `anchor_side` | wenn Schrauben, Anker, Dübel oder Bohrungen beteiligt sind |
| `continuity_connection` | `continuity_side` | wenn Kraftschluss oder Bewehrungskontinuität nötig ist |
| `support_transfer` | `transfer_side` | wenn Last über einen Zwischenbereich oder Transferknoten läuft |

## Minimale Regeln

| Port-Verbindung | Checks |
|---|---|
| `bearing_side → support_side` | Überlappung, Richtung, Mindestauflager |
| `member_side → member_side` | Ausrichtung, Fugengeometrie, Kontinuität |
| `anchor_side → support_side` | Randabstand, Bewehrungskonflikt, Ankerbarkeit |
| `continuity_side → continuity_side` | Bewehrungskontinuität, Vergusszone, Kraftschluss |
| `transfer_side → support_side / bearing_side` | Lastpfad, lokale Pressung, Zwischenauflager |

---

## Beispiel 1A — Abbau/Aufbau Wand–Decke mit DE_1OG_001

| Feld | Inhalt |
|---|---|
| Komponente A | DE_1OG_001, Deckenplatte |
| Komponente B | wiederverwendete Wand |
| Abbau/Aufbau-Anschlussfamilien | nachträglicher Bewehrungsanschluss + Verguss; Schraubanker mit Flachstahlhalter |
| Repräsentation Platte | Platte mit Auflagerkante |
| Repräsentation Wand | Wandscheibe mit Wandkopf als Auflager |

### Konkrete Connectoren der Platte

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Plattenkante / Auflagerstreifen | Platte kann auf Wand aufliegen |
| `anchor_connection` | `anchor_side` | lokale Zone an Plattenkante | Schraubanker / Flachstahlhalter möglich |
| `continuity_connection` | `continuity_side` | Kantennahe Verguss- oder Bewehrungszone | nachträglicher Bewehrungsanschluss möglich |

### Konkrete Connectoren der Wand

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `support_side` | Wandkopf / Auflagerstreifen | Wand kann Decke tragen |
| `anchor_connection` | `support_side` | Ankeraufnahmezone am Wandkopf | Wand nimmt Anker auf |
| `continuity_connection` | `continuity_side` | Anschlusszone am Wandkopf | Kraftschluss über Verguss / Bewehrung |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| Platten-`bearing_side` → Wand-`support_side` | Auflagerüberlappung, Richtung, Mindestauflager |
| Platten-`anchor_side` → Wand-`support_side` | Randabstand, Bewehrungslage, Bohrbarkeit |
| Platten-`continuity_side` → Wand-`continuity_side` | Bewehrungskontinuität, Vergussraum, Kraftschluss |

**Wichtig:**  
`Schraubanker`, `Flachstahlhalter` und `Bewehrungsanschluss + Verguss` sind Anschlussfamilien. Sie werden nicht als eigene Connector-Typen dupliziert, sondern über die minimalen Connectoren `anchor_connection` und `continuity_connection` abgebildet.

---

## Beispiel 1B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | Tragwerksgraph |
| Abstraktion | Platte + Trägerlinie + Stützenlinie + Transferknoten + Kontinuitätszone |

### Konkrete Teilrepräsentationen

| Teilregion | Abstraktion |
|---|---|
| Plattenbereich | Platte |
| integrierter Trägerbereich | Trägerlinie |
| Stützenabschnitt | Stützenlinie |
| Schnittpunkt Platte/Träger/Stütze | Transferknoten |
| Schnittfläche | Kontinuitätszone |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Rand des Plattenbereichs | Fragment kann dort aufliegen |
| `support_transfer` | `transfer_side` | integrierter Trägerbereich / Transferknoten | Last läuft über Trägerregion |
| `bearing_support` | `support_side` | Stützenfuß oder Stützenkopf | Stützenregion nimmt Last auf oder gibt sie ab |
| `continuity_connection` | `continuity_side` | Schnittfläche | Fragment kann kraftschlüssig an neuen Träger / neue Struktur angebunden werden |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `bearing_side → support_side` | lokale Auflagerung, Richtung, Pressung |
| `transfer_side → support_side` | Lastpfad über Trägerlinie zum Stützenbereich |
| `continuity_side → continuity_side` | Bewehrung an Schnittfläche, Verguss, Kraftschluss |

**Wichtig:**  
Das Fragment bleibt monolithisch. Die Zerlegung ist nur eine abstrakte Tragwerksrepräsentation für den Checker.

---

## Beispiel 1C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | wiedergewonnene Hohlkammerdecke |
| Repräsentation | einachsig spannende Fertigteilplatte |
| Quelle | ReCreate Niederlande / Finnland |
| Besondere Geometrie | Stirnauflager, Längsfugen, Hohlkammern |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `bearing_support` | `bearing_side` | Stirnseite A | Decke kann dort aufliegen |
| `bearing_support` | `bearing_side` | Stirnseite B | zweites Auflager |
| `joint_connection` | `member_side` | Längsfuge | Verbindung / Toleranzprüfung zur Nachbarplatte |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| Stirn-`bearing_side` → Auflager-`support_side` | Auflagerlänge, Richtung, Toleranz |
| Längsfugen-`member_side` → Nachbar-`member_side` | Ausrichtung, Fugenbreite, Wiederverbindung |
| Tragfähigkeitsstatus | Test / Neuberechnung erforderlich |

---

# 6. Paket 2 — Energie / Gebäudehülle

## Allgemein

Dieses Paket beschreibt thermische Grenze, Dämmebene, Durchdringung und Wärmebrücken.  
Hier sind Flächen und Schichten oft präziser als Connectoren. Connectoren werden nur gesetzt, wenn eine Hüllenregel geprüft wird.

## Minimale Connectoren und Ports

| Connector | Port | Wann verwenden? |
|---|---|---|
| `thermal_continuity` | `thermal_side` | wenn thermische Grenze weitergeführt wird |
| `insulation_continuity` | `insulation_side` | wenn Dämmschicht fortgeführt werden muss |
| `penetration_sealing` | `penetration_side` | bei Öffnungen / Durchdringungen |
| `thermal_bridge_warning` | `bridge_side` | bei Wärmebrückenrisiko |

---

## Beispiel 2A — Abbau/Aufbau 200-mm-Stahlbetonwand

| Feld | Inhalt |
|---|---|
| Komponente | wiederverwendete 200-mm-Stahlbetonwand |
| Repräsentation | thermische Grenzfläche |
| Eigenschaften | Dicke 200 mm, Lambda-Status, Innen-/Außenseite, U-Wert nur Vorprüfung |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | äußere Wandfläche | Dämmebene muss weiterlaufen |
| `thermal_continuity` | `thermal_side` | Wandrand / Anschlusskante | thermische Grenze muss anschließen |
| `penetration_sealing` | `penetration_side` | Öffnungsrand, falls Öffnung vorhanden | Hüllendurchdringung muss abgedichtet werden |

### Konkrete Regeln

| Regel | Check |
|---|---|
| `insulation_side → insulation_side` | Dämmschichtkontinuität, Lücken |
| `thermal_side → thermal_side` | thermische Kontinuität |
| `penetration_side → thermal_side / insulation_side` | Abdichtung, Luftdichtheit, Feuchte |

---

## Beispiel 2B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | nur aktiv, wenn Fragment Teil der Hülle wird |
| Eigenschaften | Hüllenkontext unbekannt / optional, Knotenbereiche als potenzielle Wärmebrücken |

### Konkrete Connectoren nur bei Hüllennutzung

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `thermal_continuity` | `thermal_side` | Schnittfläche, falls sie Hüllengrenze wird | thermische Grenze muss weitergeführt werden |
| `thermal_bridge_warning` | `bridge_side` | Platten-Träger-Stützen-Knoten | mögliche Wärmebrücke |

### Konkrete Regeln

| Regel | Check |
|---|---|
| `thermal_side → thermal_side` | thermischer Anschluss |
| `bridge_side` | einseitige Warnung bei Hüllennutzung |

---

## Beispiel 2C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | Hohlkammerdecke |
| Repräsentation | thermische Grenzfläche, falls Dach oder außenliegende Decke |
| Eigenschaften | Dicke, Hohlkammern als thermisch relevante Eigenschaft, Hüllenkontext |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `insulation_continuity` | `insulation_side` | Oberseite bei Dachnutzung | Dämmschicht läuft über Platte |
| `thermal_bridge_warning` | `bridge_side` | Plattenkante | Wärmebrückenrisiko |
| `penetration_sealing` | `penetration_side` | Durchdringung, falls vorhanden | Abdichtung erforderlich |

---

# 7. Paket 3 — TGA / Öffnungen

## Allgemein

Dieses Paket beschreibt Leitungsführung, Öffnungsnutzung, Bohrungen und blockierte Zonen.

## Minimale Connectoren und Ports

| Connector | Port | Wann verwenden? |
|---|---|---|
| `route_continuity` | `route_side` | wenn eine Leitung weitergeführt wird |
| `opening_use` | `opening_side` | wenn eine bestehende Öffnung genutzt wird |
| `drilling_candidate` | `drilling_side` | wenn eine neue Bohrung vorgeschlagen wird |
| `blocked_conflict` | `blocked_side` | wenn eine Zone Leitungen / Bohrungen blockiert |

---

## Beispiel 3A — Abbau/Aufbau Öffnung

| Feld | Inhalt |
|---|---|
| Komponente | Platte oder Wand mit katalogisierter Öffnung |
| Repräsentation | Öffnungsmodell |
| Eigenschaften | Öffnungsmaß, Tiefe, Randabstand, Bezug zu Tragwerkszonen |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `opening_use` | `opening_side` | Öffnungsrand / Öffnungsachse | bestehende Öffnung kann genutzt werden |
| `route_continuity` | `route_side` | geplante Leitung | Leitung soll durch Öffnung geführt werden |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `opening_side → route_side` | Durchmesser passt, Randabstand, Tragwerkskonflikt |
| `route_side → route_side` | Leitungsflucht, Lichtraum |

---

## Beispiel 3B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | Bohr- und Sperrzonenmodell |
| Eigenschaften | Träger- und Stützenregion als sensible Lastzonen, Bohrstatus unbekannt |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `drilling_candidate` | `drilling_side` | plattenartige Region | mögliche neue Bohrung |
| `blocked_conflict` | `blocked_side` | Trägerregion / Stützenregion | Leitungsführung dort blockiert oder kritisch |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `drilling_side → route_side` | Bewehrung, Tragwerkszone, Randabstand |
| `blocked_side` | Konflikt mit Leitung oder Bohrung |

---

## Beispiel 3C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | Hohlkammerdecke |
| Repräsentation | Leitungs- oder Hohlraum-Modell |
| Eigenschaften | Hohlkammerachse, Durchmesser / Hohlraumgröße, Bohrstatus |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `route_continuity` | `route_side` | Hohlkammerachse, nur wenn als Führung genutzt | Leitung könnte im Hohlraum laufen |
| `drilling_candidate` | `drilling_side` | geplante Bohrzone | neue Durchdringung möglich |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `route_side → route_side` | Leitungsflucht, Kontinuität |
| `drilling_side → route_side` | Durchmesser, Bewehrung, Tragwerkskonflikt |

---

# 8. Paket 4 — Semantik / Architektur

## Allgemein

Dieses Paket speichert nur architektonische Griffe, wenn sie prüfbar oder entscheidungsrelevant sind.

## Minimale Connectoren und Ports

| Connector | Port | Wann verwenden? |
|---|---|---|
| `access_handle` | `access_port` | Zugang / Annäherung / Nische |
| `attachment_handle` | `attachment_port` | architektonische Anbindung |
| `stack_handle` | `top_port` / `bottom_port` | Stapelung / vertikale Beziehung |
| `side_handle` | `side_port` | Raumseite / Fassadenseite / Orientierung |
| `opening_handle` | `opening_port` | Öffnungsbezug |
| `alignment_handle` | `alignment_port` | Raster, Fuge, Datum |
| `visibility_constraint_handle` | `visibility_port` | Sichtbarkeit / Verdeckung |

---

## Beispiel 4A — Abbau/Aufbau DE_1OG_001

| Feld | Inhalt |
|---|---|
| Komponente | Deckenplatte DE_1OG_001 |
| Repräsentation | architektonisches Plattenmodell |
| Eigenschaften | mögliche Bodenfläche, mögliche Deckenuntersicht, Rastermaß, Oberflächenstatus |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | lange Plattenkante / Fugenlinie | Fuge oder Raster soll ausgerichtet werden |
| `visibility_constraint_handle` | `visibility_port` | Plattenunterseite, falls sichtbar | Untersicht soll nicht verdeckt oder bewertet werden |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `alignment_port → alignment_port` | Fugenausrichtung, Rasterausrichtung |
| `visibility_port` | Sichtbarkeitsprüfung, Oberflächenwarnung |

---

## Beispiel 4B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | architektonisches Fragmentmodell |
| Eigenschaften | Nische, Stütze-im-Raum, räumliche Schwelle, sichtbare Wiederverwendungsidentität |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `access_handle` | `access_port` | Nischenzugang | Zugang / Annäherung wird geprüft |
| `side_handle` | `side_port` | Stützenseite zum Raum | Raumbeziehung wird geprüft |
| `alignment_handle` | `alignment_port` | Schnittkante oder Trägerlinie | Fragment wird an Raster / Datum ausgerichtet |
| `visibility_constraint_handle` | `visibility_port` | sichtbare Gesamtflächen | Fragment soll lesbar bleiben |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `access_port → access_port` | Lichtraum, Annäherung |
| `side_port → side_port` | Raumgrenze, Seitenbezug |
| `alignment_port → alignment_port` | Raster, Fuge, Datum |
| `visibility_port` | Sichtbarkeit, Verdeckung, Oberflächenzustand |

---

## Beispiel 4C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | Hohlkammerdecke |
| Repräsentation | architektonisches Fertigteilmodell |
| Eigenschaften | Modulmaß, Längsfuge, mögliche sichtbare Unterseite |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `alignment_handle` | `alignment_port` | Längsfuge | Modul- oder Fugenausrichtung |
| `stack_handle` | `top_port` | Oberseite | vertikale Relation / Niveau |
| `stack_handle` | `bottom_port` | Unterseite | vertikale Relation / Niveau |
| `visibility_constraint_handle` | `visibility_port` | Unterseite, falls sichtbar | sichtbare Wiederverwendung |

### Konkrete Regeln

| Verbindung | Check |
|---|---|
| `alignment_port → alignment_port` | Fugen- und Modulausrichtung |
| `top_port → bottom_port` | vertikale Ausrichtung, Niveau |
| `visibility_port` | Sichtbarkeit / Oberflächenzustand |

---

# 9. Paket 5 — Logistik / Montage

## Allgemein

Dieses Paket beschreibt Handling, Heben, Lagerung, Transport, Schutz, Zugang und temporäre Montagezustände.

## Minimale Connectoren und Ports

| Connector | Port | Wann verwenden? |
|---|---|---|
| `lifting_handle` | `lifting_port` | Heben / Kran |
| `storage_handle` | `storage_port` | Lagerung / Auflager im Lager |
| `transport_handle` | `transport_port` | Transporthülle / Ladungssicherung |
| `access_handle` | `access_port` | Montagezugang |
| `protection_handle` | `protection_port` | Schutz sensibler Kanten / Flächen |
| `temporary_bracing_handle` | `temporary_bracing_port` | temporäre Stabilisierung |

---

## Beispiel 5A — Abbau/Aufbau DE_1OG_001

| Feld | Inhalt |
|---|---|
| Komponente | DE_1OG_001 |
| Repräsentation | Handlingmodell |
| Eigenschaften | 4.1 t, 4500 × 2300 × 180 mm, liegende Lagerung empfohlen, Hebestatus offen |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `storage_handle` | `storage_port` | Unterseite / Lagerauflagerzonen | liegende Lagerung prüfen |
| `transport_handle` | `transport_port` | Transporthülle | Transport und Ladungssicherung prüfen |
| `lifting_handle` | `lifting_port` | Hebekandidatenzone | Hebbarkeit prüfen |
| `protection_handle` | `protection_port` | Kanten / Oberflächen | Schutz prüfen |

### Konkrete Regeln

| Connector | Check |
|---|---|
| `storage_handle` | Lagerorientierung, Trennhölzer, Auflagerabstand |
| `transport_handle` | Transportmaße, Ladungssicherung |
| `lifting_handle` | Schwerpunkt, Hebe-Nachweis |
| `protection_handle` | Kanten- und Witterungsschutz |

---

## Beispiel 5B — SlabBeamColumnFragment

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | komplexes Handlingmodell |
| Eigenschaften | unregelmäßiger Schwerpunkt, Schnittflächen, mögliche Instabilität |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | ein oder zwei Hebekandidaten | Heben des Fragments |
| `storage_handle` | `storage_port` | stabile Lagerauflagerzonen | Lagerung ohne Kippen |
| `protection_handle` | `protection_port` | Schnittflächen / empfindliche Kanten | Schutz |
| `temporary_bracing_handle` | `temporary_bracing_port` | Stützen- oder Trägerregion | temporäre Stabilisierung |

### Konkrete Regeln

| Connector | Check |
|---|---|
| `lifting_handle` | Schwerpunkt, Hebbarkeit, Kran-Zugang |
| `storage_handle` | Kippstabilität, Auflagerung |
| `protection_handle` | Schnittflächenschutz |
| `temporary_bracing_handle` | temporäre Stabilität, Montagezugang |

---

## Beispiel 5C — ReCreate Hollow-Core Slab

| Feld | Inhalt |
|---|---|
| Komponente | Hohlkammerdecke |
| Repräsentation | Transport- und Hebemodell |
| Eigenschaften | Transporthistorie, Hebevorgang, QR-Tracking, Lagerung |

### Konkrete Connectoren

| Connector | Port | Geometrie | Bedeutung |
|---|---|---|---|
| `lifting_handle` | `lifting_port` | Hebezonen | Element heben |
| `transport_handle` | `transport_port` | Transportauflager / Hülle | Transport prüfen |
| `storage_handle` | `storage_port` | Lagerauflager | Lagerung prüfen |

### Konkrete Regeln

| Connector | Check |
|---|---|
| `lifting_handle` | Hebbarkeit, Schwerpunkt, Beschädigungsrisiko |
| `transport_handle` | Ladungssicherung, Transporthülle |
| `storage_handle` | Lagerorientierung, Auflagerabstand |

---

# 10. Paket 6 — Nachweis-Overlay

## Allgemein

Das Nachweis-Overlay beschreibt, wo Nachweise liegen und welche Connectoren sie beeinflussen.

Nachweise erzeugen keine Connectoren und keine Ports.  
Sie modifizieren Connectoren anderer Pakete.

## Minimale Eigenschaften

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
Nachweisstatus
```

## Mögliche Effekte

```text
bestätigt
Warnung
blockiert
Konfidenz reduziert
manuelle Prüfung erforderlich
Ingenieurnachweis erforderlich
```

---

## Beispiel 6A — Abbau/Aufbau Bewehrung / Material

| Feld | Inhalt |
|---|---|
| Komponente | Wand oder Deckenplatte |
| Repräsentation | Bewehrungs- oder Materialnachweis-Overlay |
| Betroffener Connector | z. B. `anchor_connection` im Tragwerk |
| Betroffener Port | z. B. `anchor_side` oder `support_side` |
| Effekt | Warnung oder Blockade, wenn Bewehrungslage unbekannt ist |

### Konkrete Wirkung

Wenn ein Ankerbereich in einer unbekannten Bewehrungszone liegt, wird der Connector `anchor_connection` blockiert oder als Warnung markiert. Wenn ein Scan die Zone freigibt, darf die Verbindung zur Ingenieurprüfung weitergehen.

---

## Beispiel 6B — SlabBeamColumnFragment Schnittfläche

| Feld | Inhalt |
|---|---|
| Komponente | SlabBeamColumnFragment |
| Repräsentation | Schnittflächen-, Schaden- und Rebar-Overlay |
| Betroffene Connectoren | `continuity_connection`, `support_transfer`, `visibility_constraint_handle` |
| Effekt | Ingenieurnachweis, Warnung, reduzierte Konfidenz |

### Konkrete Wirkung

Wenn die Bewehrung an der Schnittfläche unbekannt ist, wird die `continuity_connection` als ingenieurpflichtig markiert. Wenn Schaden im Lasttransferbereich liegt, wird `support_transfer` gewarnt. Wenn Schaden auf einer sichtbaren Fläche liegt, erhält der Architektur-Connector eine Oberflächenwarnung.

---

## Beispiel 6C — ReCreate QR / Test / Neuberechnung

| Feld | Inhalt |
|---|---|
| Komponente | Hohlkammerdecke |
| Repräsentation | Tracking-, Test- und Neuberechnungs-Overlay |
| Betroffene Connectoren | `bearing_support`, `joint_connection`, `lifting_handle` |
| Effekt | bestätigt, manuelle Prüfung oder Ingenieurnachweis |

### Konkrete Wirkung

QR-Tracking bestätigt Identität und Rückverfolgbarkeit. Belastungstests oder Neuberechnungen erhöhen die Tragwerkskonfidenz. Unklare Fugen- oder Transportschäden können `joint_connection` oder `lifting_handle` als manuell zu prüfen markieren.

---

# 11. Zusammenfassung der drei Beispielkomponenten

## 11.1 Abbau/Aufbau DE_1OG_001

| Paket | Repräsentation | wichtigste Connectoren |
|---|---|---|
| Basisgeometrie | Plattenkörper | keine |
| Tragwerk | Platte | `bearing_support`, `anchor_connection`, `continuity_connection` |
| Energie | thermische Grenzfläche, falls Hülle | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Öffnungs-/Bohrmodell, falls gebraucht | `opening_use`, `drilling_candidate` |
| Semantik | architektonisches Plattenmodell | `alignment_handle`, `visibility_constraint_handle` |
| Logistik | Handlingmodell | `storage_handle`, `transport_handle`, `lifting_handle`, `protection_handle` |
| Nachweis | Bewehrung / Material / Schaden | keine; modifiziert andere |

---

## 11.2 SlabBeamColumnFragment

| Paket | Repräsentation | wichtigste Connectoren |
|---|---|---|
| Basisgeometrie | monolithischer Körper mit Teilregionen | keine |
| Tragwerk | Platte + Trägerlinie + Stützenlinie + Transferknoten | `bearing_support`, `support_transfer`, `continuity_connection` |
| Energie | nur bei Hüllennutzung | `thermal_continuity`, `thermal_bridge_warning` |
| TGA | Bohr- und Sperrzonenmodell | `drilling_candidate`, `blocked_conflict` |
| Semantik | architektonisches Fragmentmodell | `access_handle`, `side_handle`, `alignment_handle`, `visibility_constraint_handle` |
| Logistik | komplexes Handlingmodell | `lifting_handle`, `storage_handle`, `protection_handle`, `temporary_bracing_handle` |
| Nachweis | Schnittfläche / Rebar / Schaden | keine; modifiziert andere |

---

## 11.3 ReCreate Hollow-Core Slab

| Paket | Repräsentation | wichtigste Connectoren |
|---|---|---|
| Basisgeometrie | Hohlkammer-Plattenkörper | keine |
| Tragwerk | einachsig spannende Fertigteilplatte | `bearing_support`, `joint_connection` |
| Energie | Hülle, falls Dach / Außenboden | `insulation_continuity`, `thermal_bridge_warning`, `penetration_sealing` |
| TGA | Hohlraum- / Bohrmodell | `route_continuity`, `drilling_candidate` |
| Semantik | Modul- und Fugenausrichtungsmodell | `alignment_handle`, `stack_handle`, optional `visibility_constraint_handle` |
| Logistik | Hebe-, Transport- und Lagermodell | `lifting_handle`, `transport_handle`, `storage_handle` |
| Nachweis | BIM / QR / Test / Neuberechnung | keine; modifiziert andere |

---

# 12. Finale Regel

Allgemein bleibt das System minimal.  
Konkret werden die Beispiele präzise.

```text
Eigenschaften beschreiben.
Connectoren machen etwas handlungsfähig.
Ports definieren Kompatibilität.
Regeln prüfen Connectoren über Ports.
Nachweise verändern Status, Konfidenz, Warnung oder Blockade.
```

Das System soll keine langen projektspezifischen Connector-Listen erzeugen.  
Projektbegriffe wie Schraubanker, Edelstahldorn, Flachstahlhalter oder Verguss bleiben Anschlussfamilien oder Detailoptionen. Sie werden über die minimalen Connectoren abgebildet:

```text
Schraubanker / Edelstahldorn → anchor_connection
Bewehrungsanschluss + Verguss → continuity_connection
Stahlträger-Auflager → support_transfer
Winkelverbinder → anchor_connection oder joint_connection, je nach Detail
```

So bleibt das System abstrakt genug für viele Projekte, aber konkret genug für echte ReUse-Bauteile.
