# Minimale Paket-Abstraktionen für das Komponentensystem  
## Polierte deutsche Version mit Abbau/Aufbau-, SlabBeamColumnFragment- und ReCreate-Beispielen

**Zweck**  
Dieses Dokument definiert eine minimale, saubere Paketstruktur für das Entwerfen mit wiederverwendeten Bauteilen. Es folgt dem Systemmodell:

```text
Komponente → Paket → Repräsentation → Eigenschaften → Connectoren → Ports → Regeln / Prüfungen
```

Ziel ist es, Übermodellierung zu vermeiden. Das System soll nur jene Abstraktionen speichern, die für **Verbindung, Berechnung, Warnung, Kompatibilität und Entwurfsentscheidung** notwendig sind.

---

# 1. Quellenbasis

## 1.1 Abbau/Aufbau-Handbuch

Das Abbau/Aufbau-Handbuch wird für die Logik des Bauteilkatalogs, die Stahlbeton-Verbindungsbeispiele, Logistik, Energie-Vorprüfungen und Nachweisbedarfe verwendet.

Wichtige verwendete Punkte:

- Der Bauteilkatalog enthält ID, Maße, Öffnungsmaße, Volumen, Masse, Elementtyp und kann um Beton- und Bewehrungsuntersuchungen erweitert werden.
- Das Beispielelement **DE_1OG_001** ist eine Deckenplatte mit **4500 × 2300 × 180 mm**, **1.863 m³** und **ca. 4.1 t**.
- Das Handbuch zeigt Verbindungsbeispiele für Paare wie **Wand–Decke** und **Stütze–Decke**.
- Relevante Anschlussfamilien sind **Schraubanker**, **Edelstahldorn**, **Winkelverbinder**, **nachträglicher Bewehrungsanschluss + Verguss**, **Flachstahlhalter** und **Stahlträger-Auflager**.
- Logistik hängt von ID, Katalog, Transport, Lagerreihenfolge, Witterungsschutz und sicherem Handling ab.
- Energie / Bauphysik wird relevant, wenn wiederverwendete Betonbauteile Teil der Gebäudehülle werden.

Quelle: Abbau/Aufbau, *Handbuch zur Wiederverwendung von Stahlbetonelementen aus dem Rückbau von Gebäuden*, 2023.

## 1.2 Abbau/Aufbau Masterarbeit 2020

Die Masterarbeit 2020 wird für das Beispiel **SlabBeamColumnFragment** verwendet.

Wichtige verwendete Punkte:

- Die Arbeit untersucht, wie ein Stahlbetongebäude in Elemente geschnitten und in einem neuen Gebäude wiederverwendet werden kann.
- Sie identifiziert räumlich wertvolle Fragmente wie **Stützen vor Fenstern**, **Nische hinter Stütze** und **Große Stütze in kleinem Raum**.
- Das finale Projekt verwendet viele geschnittene Betonteile.
- Die verwendeten Teile lagern auf einem Halbfertigteil-Stahlbetonträger und werden über einen nachträglichen Bewehrungsanschluss kraftschlüssig verbunden.

**Wichtiger Hinweis:**  
`SlabBeamColumnFragment` ist kein benanntes Quellobjekt. Es ist eine vorgeschlagene Systemtypologie, die aus der Fragmentlogik abgeleitet wird: ein monolithisches Betonfragment mit Plattenbereich, integriertem Trägerbereich und Stützenabschnitt.

## 1.3 ReCreate

ReCreate wird für das Beispiel der wiederverwendeten Betonfertigteile genutzt.

Wichtige verwendete Punkte:

- Der niederländische Pilot verwendet wiedergewonnene Hohlkammerdecken und vorgefertigte Fassadenelemente aus dem Prinsenhof-Gebäude.
- Das Spendergebäude hatte Hohlkammerdecken, die von tragender Fassade zu tragender Fassade spannten.
- Nasse Verbindungen erforderten Sägeschnitte entlang der Längsfugen; Elemente wurden gehoben und transportiert.
- Ein Mock-up soll Maßtoleranzen und das Wiederverbinden zurückgewonnener Elemente zu einer robusten Struktur testen.
- Der finnische Pilot umfasst Stützen, Träger, Hohlkammerdecken, Sandwich-Fassadenelemente, BIM-Inventarisierung, Codierung / QR-Tracking, Prüfungen und Neuberechnung nach aktuellen Tragwerksnormen.

---

# 2. Kernregel des Systems

## 2.1 Minimale Abstraktion

Nicht jedes reale Detail wird modelliert. Modelliert wird nur, was das System für eine Entscheidung braucht.

Ein Detail gehört ins System, wenn es mindestens eine dieser Funktionen unterstützt:

- Bauteile verbinden
- einen Wert berechnen
- eine Warnung erzeugen
- Kompatibilität prüfen
- eine Entwurfsentscheidung unterstützen

## 2.2 Repräsentation, Eigenschaft, Connector, Port

| Begriff | Bedeutung | Beispiel |
|---|---|---|
| **Repräsentation** | Vereinfachtes Modell der Komponente innerhalb eines Pakets. | Eine Deckenplatte als strukturelle Platte. |
| **Eigenschaft** | Information, die eine Repräsentation beschreibt. | Dicke, Masse, Kapazitätsstatus, Sichtbarkeitsstatus |
| **Connector** | Platzierter, handlungsrelevanter Griffpunkt an einer Repräsentation. | Auflagerkante einer Deckenplatte |
| **Port** | Semantischer Kompatibilitätstyp, auf den ein Connector verweist. | `bearing_side` |

Ein Connector besitzt Geometrie.  
Ein Port besitzt Kompatibilitätsbedeutung.  
Eine Regel prüft kompatible Ports anhand der Connector-Geometrie.

## 2.3 Connector-Regel

Connectoren werden nicht auf jede Fläche oder jede Kante gesetzt.  
Ein Connector wird nur erzeugt, wenn das System ihn für eine Regel, Verbindung, Warnung, Berechnung oder Entwurfsoperation verwendet.

Richtig:

- Plattenkante als Auflager → Connector
- Wandkopf als Auflager → Connector
- Öffnung als mögliche TGA-Führung → Connector
- sichtbare Oberfläche mit Verdeckungsprüfung → Connector

Falsch:

- jede Plattenkante → Connector
- jede sichtbare Fläche → Connector
- jede beschreibende Eigenschaft → Connector

---

# 3. Finale Paketstruktur

Das System nutzt sieben Pakete:

| Nr. | Paket | Kernrepräsentation | Connector-Logik |
|---:|---|---|---|
| 0 | **Basisgeometrie** | neutraler geometrischer Körper | keine Connectoren |
| 1 | **Tragwerk** | Kraftübertragungs-Abstraktion | minimale Tragwerks-Connectoren |
| 2 | **Energie / Gebäudehülle** | thermische / Hüllen-Abstraktion | nur Kontinuität, Abdichtung, Wärmebrücken |
| 3 | **TGA / Öffnungen** | Service- / Öffnungs-Abstraktion | Leitungs- und Durchdringungsconnectoren |
| 4 | **Semantik / Architektur** | Entwurfsgriff-Abstraktion | nur handlungsrelevante Entwurfsgriffe |
| 5 | **Logistik / Montage** | Handling-Abstraktion | Heben, Lagern, Transport, Zugang |
| 6 | **Nachweis-Overlay** | ortsbezogene Nachweisabstraktion | keine Connectoren; modifiziert andere Connectoren |

---

# 4. Minimales Connector- und Port-Vokabular

## 4.1 Tragwerk

| Connector | Port | Bedeutung |
|---|---|---|
| `bearing_support` | `bearing_side` / `support_side` | Last kann über Auflagerung getragen oder übertragen werden. |
| `joint_connection` | `member_side` | Zwei Bauteilseiten müssen ausgerichtet oder gefügt werden. |
| `anchor_connection` | `anchor_side` | Verbindung hängt von Ankern, Schrauben, Dübeln oder Bohrungen ab. |
| `continuity_connection` | `continuity_side` | Kraftschluss oder Bewehrungskontinuität ist erforderlich. |
| `support_transfer` | `transfer_side` | Last wird über ein Zwischen- oder lokales Auflager übertragen. |

## 4.2 Energie / Gebäudehülle

| Connector | Port | Bedeutung |
|---|---|---|
| `thermal_continuity` | `thermal_side` | Thermische Grenze muss fortgeführt werden. |
| `insulation_continuity` | `insulation_side` | Dämmschicht muss fortgeführt werden. |
| `penetration_sealing` | `penetration_side` | Öffnung oder Durchdringung muss abgedichtet werden. |
| `thermal_bridge_warning` | `bridge_side` | Einseitige Warnzone für Wärmebrückenrisiko. |

## 4.3 TGA / Öffnungen

| Connector | Port | Bedeutung |
|---|---|---|
| `route_continuity` | `route_side` | Serviceführung kann weitergeführt werden. |
| `opening_use` | `opening_side` | Bestehende Öffnung kann genutzt werden. |
| `drilling_candidate` | `drilling_side` | Neue Kernbohrung oder Durchdringung kann geprüft werden. |
| `blocked_conflict` | `blocked_side` | Zone kollidiert mit Leitungsführung oder Bohrung. |

## 4.4 Semantik / Architektur

| Connector | Port | Bedeutung |
|---|---|---|
| `access_handle` | `access_port` | Zugang, Annäherung oder räumlicher Durchgang wird geprüft. |
| `attachment_handle` | `attachment_port` | Architektonische Anbindung oder Modulbezug wird geprüft. |
| `stack_handle` | `top_port` / `bottom_port` | Stapelung, vertikale Beziehung oder Niveau wird geprüft. |
| `side_handle` | `side_port` | Seitenbezug, Raumgrenze oder Orientierung wird geprüft. |
| `opening_handle` | `opening_port` | Architektonische Öffnung oder Zugangsflucht wird geprüft. |
| `alignment_handle` | `alignment_port` | Raster, Datum, Rhythmus oder Fuge wird geprüft. |
| `visibility_constraint_handle` | `visibility_port` | Sichtbarkeit, Wiederverwendungsausdruck oder Verdeckung wird geprüft. |

## 4.5 Logistik / Montage

| Connector | Port | Bedeutung |
|---|---|---|
| `lifting_handle` | `lifting_port` | Hebbarkeit oder Kran-Zugang wird geprüft. |
| `storage_handle` | `storage_port` | Lagerorientierung oder Auflagerung im Lager wird geprüft. |
| `transport_handle` | `transport_port` | Transporthülle oder Ladungssicherung wird geprüft. |
| `access_handle` | `access_port` | Montagezugang wird geprüft. |
| `protection_handle` | `protection_port` | Schaden- oder Witterungsschutz wird geprüft. |
| `temporary_bracing_handle` | `temporary_bracing_port` | Temporäre Stabilität wird geprüft. |

## 4.6 Nachweis-Overlay

Nachweise haben **keine Connectoren und keine Ports**.  
Sie modifizieren Connectoren anderer Pakete.

Mögliche Effekte:

- bestätigt
- Warnung
- blockiert
- Vertrauen reduziert
- manuelle Prüfung erforderlich
- Ingenieurnachweis erforderlich

---

# 5. Paket 0 — Basisgeometrie

## Zweck

Die Basisgeometrie speichert den neutralen geometrischen Körper. Sie ist die Quelle, aus der andere Pakete ihre eigenen Repräsentationen ableiten.

## Minimale Repräsentation

Die Basisrepräsentation enthält nur:

- Typologie
- Geometriequelle
- Einheiten
- lokale Achsen
- Bounding Box
- Länge, Breite, Höhe oder Dicke
- Volumen
- Hauptflächen
- Hauptkanten
- rohe Öffnungen
- geometrisches Zentrum
- Geometrie-Konfidenz

## Connectoren und Ports

Keine.

Die Basisgeometrie erzeugt niemals Connectoren. Eine Kante, Fläche oder Öffnung der Basisgeometrie wird erst dann zum Connector, wenn ein anderes Paket ihr eine Funktion gibt.

## Prüfungen

- Geometrie vorhanden
- Maße extrahierbar
- Volumen extrahierbar
- Einheiten gültig
- Orientierung bekannt oder als unbekannt markiert

## Beispiel 1 — Abbau/Aufbau DE_1OG_001

Die Deckenplatte **DE_1OG_001** wird als ein neutraler Plattenkörper repräsentiert. Die Basisgeometrie speichert Maße, Volumen, Hauptflächen, Hauptkanten und den Status möglicher Öffnungen. Sie entscheidet noch nicht, ob eine lange Kante tragend, sichtbar, thermisch oder logistisch relevant ist.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment wird als ein durchgehender monolithischer Körper repräsentiert. Die Basisgeometrie erkennt drei rohe Regionen: einen plattenartigen Bereich, einen integrierten trägerartigen Bereich und einen stützenartigen Bereich. Diese Regionen sind keine getrennten Komponenten, sondern Teilbereiche eines einzigen Bauteils.

## Beispiel 3 — ReCreate Hohlkammerdecke

Die ReCreate-Hohlkammerdecke wird als Fertigteilplatte mit Längshohlräumen, Stirnflächen, Längskanten und Nettovolumen repräsentiert. Auf dieser Ebene entsteht kein Connector. Die Längsfuge wird erst im Tragwerks- oder Semantik-Paket relevant.

---

# 6. Paket 1 — Tragwerk

## Zweck

Das Tragwerkspaket speichert die minimale Abstraktion für Kraftübertragung, Auflagerung, Verankerung, Kontinuität und strukturelle Warnungen.

## Minimale Repräsentation

Die Repräsentation wird in einfache strukturelle Abstraktionen zerlegt:

| Reale Geometrie | Strukturelle Abstraktion |
|---|---|
| Plattenbereich | Platte |
| Wandbereich | Wandscheibe |
| Trägerbereich | Trägerlinie |
| Stützenbereich | Stützenlinie |
| lokales Auflagerfeld | Auflagerknoten |
| Fuge / Gussverbindung | Kontinuitätszone |
| komplexes monolithisches Fragment | Graph aus Platte + Trägerlinie + Stützenlinie + Transferknoten |

Dadurch werden unscharfe Bezeichnungen wie `monolithic_structural_fragment` vermieden.  
Eine komplexe Komponente wird zu einem kleinen Tragwerksgraphen.

## Minimale Eigenschaften

- strukturelle Rolle
- Status der Spannrichtung
- mögliche Auflagerbedingungen
- Status der Auflagerzonen
- Kapazitätsstatus
- Status des Bewehrungsnachweises
- Regel für Mindestauflager
- Status struktureller Öffnungen
- Schadensrelevanz

## Minimale Connectoren und Ports

Nur diese verwenden:

- `bearing_support` mit `bearing_side` oder `support_side`
- `joint_connection` mit `member_side`
- `anchor_connection` mit `anchor_side`
- `continuity_connection` mit `continuity_side`
- `support_transfer` mit `transfer_side`

## Minimale Prüfungen

| Regel | Prüfungen |
|---|---|
| `bearing_side → support_side` | Überlappung, Richtung, Mindestauflagerlänge |
| `member_side → member_side` | Ausrichtung, Kontinuität, Fugen-/Stoßgeometrie |
| `anchor_side → support_side` | Randabstand, Bewehrungskonflikt, Ankerbarkeit, Kapazität |
| `continuity_side → continuity_side` | Bewehrungskontinuität, Kraftschluss, Verguss- oder Ortbetonzone |
| `transfer_side → support_side / bearing_side` | Lastpfad, lokale Pressung, Zwischenauflager |

## Was außerhalb bleibt

Das Tragwerkspaket erbringt keinen finalen Standsicherheitsnachweis, keine Durchstanzprüfung, keinen Schubnachweis, keinen Brandschutz und keine Genehmigung. Es erzeugt nur die regelrelevante Tragwerksabstraktion.

## Beispiel 1 — Abbau/Aufbau Wand–Decke

Bei einer wiederverwendeten Deckenplatte, die mit einer wiederverwendeten Wand verbunden wird, nutzt die strukturelle Repräsentation nur drei mögliche plattenspezifische Griffe: ein Auflager an der Plattenkante, eine Ankerzone, falls Schraubanker oder Flachstahlhalter verwendet werden, und eine Kontinuitätszone, falls nachträglicher Bewehrungsanschluss mit Verguss verwendet wird.

Die Wandrepräsentation besitzt einen `support_side`-Connector am Wandkopf. Wenn Anker verwendet werden, empfängt der Wandkopf die Verankerung. Wenn ein nachträglicher Bewehrungsanschluss verwendet wird, wird der Wandkopf Teil einer `continuity_side`-Beziehung.

Das System prüft Auflagerüberlappung, Richtung, Mindestauflager, Randabstand, Bewehrungskonflikt und ob ein Kraftschluss hergestellt werden kann. Die konkreten Abbau/Aufbau-Detailnamen bleiben Anschlussfamilien auf Systemebene, nicht eigene Connector-Typen.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment wird nicht als ein unscharfes monolithisches Tragwerksobjekt gespeichert. Es wird in einen kleinen Tragwerksgraphen zerlegt:

- Plattenbereich → Platte
- integrierter Trägerbereich → Trägerlinie
- Stützenabschnitt → Stützenlinie
- Schnittpunkt von Platte, Träger und Stütze → Transferknoten
- Schnittfläche → Kontinuitätszone, falls Kraftschluss erforderlich ist

Es werden nur vier strukturelle Griffe benötigt: ein Auflager dort, wo der Plattenbereich aufliegen kann, ein `support_transfer` am Trägerbereich, ein `support_side` am Stützenfuß und eine `continuity_connection` an der Schnittfläche, falls das Fragment kraftschlüssig mit einem neuen Bauteil verbunden werden muss.

So bleibt die monolithische Realität erhalten, während der Checker klare abstrakte Griffe bekommt.

## Beispiel 3 — ReCreate Hohlkammerdecke

Die Hohlkammerdecke wird als einachsig spannende Platte oder als Plattenmitglied repräsentiert. Sie hat Auflager-Connectoren an beiden Stirnseiten und einen `joint_connection` entlang der Längsfuge. Diese Längsfuge ist wichtig, weil im ReCreate-Niederlande-Pilot entlang der Längsfugen gesägt und später das Wiederverbinden der Elemente in einem Mock-up untersucht wird.

Die strukturellen Prüfungen bleiben minimal: Endauflager, Ausrichtung, Toleranz und Wiederverbindung der Fuge. Die Tragfähigkeit bleibt abhängig von Prüfung oder Neuberechnung.

---

# 7. Paket 2 — Energie / Gebäudehülle

## Zweck

Das Energie-/Hüllenpaket speichert nur, was für thermische Kontinuität, Dämmkontinuität, Durchdringungsabdichtung und Wärmebrückenwarnungen notwendig ist.

## Minimale Repräsentation

Energie bleibt flächen-, schicht- und kantenbasiert. Hier sollte Connector-Sprache nicht erzwungen werden, wenn Oberflächen präziser sind.

Repräsentationstypen:

- thermische Grenzfläche
- Dämmkontinuitätsmodell
- Hüllendurchdringungsmodell
- Wärmebrückenrisikomodell
- Feuchtegrenzmodell

## Minimale Eigenschaften

- thermische Rolle
- Innen-/Außenstatus
- Fläche
- Dicke
- Lambda-Status
- U-Wert-Status
- Dämmstatus
- Feuchterisiko-Status
- Gebäudehüllen-Kontextstatus

## Minimale Connectoren und Ports

Nur diese verwenden:

- `thermal_continuity` mit `thermal_side`
- `insulation_continuity` mit `insulation_side`
- `penetration_sealing` mit `penetration_side`
- `thermal_bridge_warning` mit `bridge_side`

## Minimale Prüfungen

- thermische Grenzkontinuität
- Dämmkontinuität
- Fugen- oder Lückenprüfung
- Abdichtungsbedarf
- Luftdichtheit
- Feuchterisiko
- Wärmebrückenwarnung
- grober U-Wert-Vorcheck

## Was außerhalb bleibt

Das Paket erbringt keinen finalen U-Wert-Nachweis, keinen Feuchteschutznachweis, keinen Energieausweis und keine vollständige Hüllkonformität.

## Beispiel 1 — Abbau/Aufbau 200-mm-Betonwand

Eine wiederverwendete 200-mm-Betonwand als Außenwand wird als thermische Grenzfläche repräsentiert. Das System speichert Betondicke, Lambda-Status und Hüllenkontext. Die Außenseite kann einen Connector für Dämmkontinuität erhalten, der Rand einen Connector für thermische Kontinuität und Öffnungen einen Connector für Durchdringungsabdichtung.

Das System kann mit `R = Dicke / Lambda` einen groben Vorcheck machen. Der finale U-Wert braucht aber den vollständigen Wandaufbau.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment erhält Energie-Connectoren nur dann, wenn es in der Gebäudehülle verwendet wird. Bleibt es im Innenraum, kann das Paket inaktiv bleiben oder als kontextabhängig markiert werden.

Wird es Teil der Hülle, kann die Schnittfläche ein `thermal_continuity`-Connector werden und der Platten-Träger-Stützen-Knoten kann als Wärmebrückenwarnzone markiert werden. Weitere Connectoren sind nicht nötig, solange keine Durchdringung oder Dämmkontinuität geprüft wird.

## Beispiel 3 — ReCreate Hohlkammerdecke

Eine ReCreate-Hohlkammerdecke erhält eine Energierepräsentation nur, wenn sie als Dach, außenliegende Decke oder andere thermische Grenze verwendet wird. Die obere Fläche kann ein Dämmkontinuitätsgriff werden, die Plattenkante eine Wärmebrückenwarnzone und Öffnungen können eine Durchdringungsabdichtung erfordern.

Die Hohlkammern sind Eigenschaften des thermischen Modells, keine eigenen Connectoren, außer sie werden tatsächlich für eine Leitung oder Durchdringung genutzt.

---

# 8. Paket 3 — TGA / Öffnungen

## Zweck

Das TGA-/Öffnungspaket speichert die minimale Abstraktion für Öffnungen, Leitungsführungen, Bohrkandidaten und blockierte Zonen.

## Minimale Repräsentation

Repräsentationstypen:

- Öffnungsmodell
- Leitungsmodell
- Bohrkandidatenmodell
- Sperrzonenmodell
- Durchdringungsmodell

## Minimale Eigenschaften

- Öffnungsgröße
- Öffnungsachse
- Öffnungstiefe
- Leitungsdurchmesser
- Randabstand
- Lichtraumstatus
- Bohrstatus
- Sperrstatus
- Bezug zu Tragwerkszonen
- Bezug zum Bewehrungsstatus

## Minimale Connectoren und Ports

Nur diese verwenden:

- `route_continuity` mit `route_side`
- `opening_use` mit `opening_side`
- `drilling_candidate` mit `drilling_side`
- `blocked_conflict` mit `blocked_side`

## Minimale Prüfungen

| Regel | Prüfungen |
|---|---|
| `route_side → route_side` | Leitungsflucht, Durchmesser, Lichtraum |
| `opening_side → route_side` | Durchmesser passt, Randabstand, Führungskontinuität |
| `drilling_side → route_side` | Durchmesser passt, Bewehrungskonflikt, Tragwerkszonenkonflikt, Randabstand |
| `blocked_side` | Konflikt mit Leitung oder Bohrung |

## Was außerhalb bleibt

Dieses Paket genehmigt keinen TGA-Entwurf, keinen Brandschutzverschluss, keinen Schallschutzverschluss und keinen tragwerksrelevanten Bohrnachweis.

## Beispiel 1 — Abbau/Aufbau-Öffnung

Wenn der Bauteilkatalog eine Öffnung erfasst, erzeugt das TGA-Paket nur dann einen `opening_use`-Connector, wenn der Entwurf diese Öffnung für eine Leitung, einen Zugang oder eine Führungsentscheidung nutzt. Wenn keine Leitung diese Öffnung nutzt, bleibt die Öffnung nur eine Eigenschaft.

Das System prüft Größe, Randabstand, Bezug zu Tragwerkszonen und Bewehrungsstatus, bevor eine Führung durch die Öffnung zugelassen wird.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment enthält tragende Bereiche, die Leitungsführung erschweren. Der plattenartige Bereich kann einen `drilling_candidate` bekommen, wenn eine Leitung vorgeschlagen wird. Der Trägerbereich und der Stützenbereich können `blocked_conflict`-Zonen werden, weil sie wahrscheinlich Kraftübertragungsbereiche sind.

Ein Öffnungsconnector entsteht nur, wenn eine reale Öffnung existiert oder eine Leitung vorgeschlagen wird.

## Beispiel 3 — ReCreate Hohlkammerdecke

Eine Hohlkammer kann einen `route_continuity`-Connector entlang des Hohlraums erhalten, aber nur wenn das System diese Hohlkammer tatsächlich als mögliche Führung nutzt. Eine neue Bohrung ist ein eigener `drilling_candidate` und muss gegen Tragwerk, Bewehrung und Hohlraumgeometrie geprüft werden.

Der Hohlraum selbst ist nicht automatisch ein TGA-Connector. Er wird erst einer, wenn er als Führung verwendet wird.

---

# 9. Paket 4 — Semantik / Architektur

## Zweck

Das Semantik-/Architekturpaket speichert handlungsrelevante architektonische Entwurfsgriffe. Es speichert nicht jede sichtbare oder semantische Beschreibung als Connector.

## Minimale Repräsentation

Repräsentationstypen:

- architektonisches Komponentenmodell
- Raumgrenzenmodell
- Fassadenbeziehungsmodell
- Sichtbarkeitsmodell
- Ausrichtungsmodell
- Zugangsmodell
- Stapelungsmodell

## Minimale Eigenschaften

- architektonische Rolle
- räumliche Rolle
- Sichtbarkeitsstatus
- Wiederverwendungsausdruck
- Oberflächenzustand
- Rasterbezug
- Raumbezug
- Fassadenbezug
- Orientierungsstatus

## Minimale Connectoren und Ports

Nur diese verwenden:

- `access_handle` mit `access_port`
- `attachment_handle` mit `attachment_port`
- `stack_handle` mit `top_port` oder `bottom_port`
- `side_handle` mit `side_port`
- `opening_handle` mit `opening_port`
- `alignment_handle` mit `alignment_port`
- `visibility_constraint_handle` mit `visibility_port`

## Minimale Prüfungen

- Zugangsausrichtung
- Lichtraum
- architektonische Anbindung
- Stapelrichtung
- vertikale Ausrichtung
- Seitenbezug
- Raumgrenzenkontinuität
- Öffnungsausrichtung
- Rasterausrichtung
- Datumsausrichtung
- Fugenausrichtung
- Sichtbarkeitsverdeckung
- Oberflächenwarnung

## Was außerhalb bleibt

Das Paket beurteilt keine Schönheit, keine finale Entwurfsabsicht, keine Standsicherheit, keine Energie- oder Brandschutzkonformität.

## Beispiel 1 — Abbau/Aufbau DE_1OG_001

Bei der Deckenplatte kann die obere Fläche eine Eigenschaft wie „mögliche Bodenfläche“ bleiben. Die Unterseite wird nur dann zu einem `visibility_constraint_handle`, wenn der Entwurf sie als sichtbare Deckenuntersicht zeigen will. Eine lange Kante wird nur dann zu einem `alignment_handle`, wenn Raster- oder Fugenausrichtung geprüft wird.

Die Deckenplatte braucht daher wahrscheinlich nur zwei architektonische Connectoren: einen Ausrichtungsgriff an der Fuge und einen Sichtbarkeitsgriff an der Unterseite, falls sichtbare Wiederverwendung Teil des Entwurfs ist.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment ist architektonisch relevant, weil die Kombination aus Platte, Träger und Stütze eine Nische, eine Stütze-im-Raum-Situation oder eine räumliche Schwelle erzeugen kann.

Die semantische Repräsentation braucht keinen eigenen Connector für jede Fläche. Sie braucht nur die Griffe, die geprüft werden können: einen Zugang für den Nischeneingang, einen Seitenbezug für die Stütze-Raum-Beziehung, einen Ausrichtungsgriff für Schnittkante oder Trägerlinie und einen Sichtbarkeitsgriff, falls das Fragment lesbar bleiben soll.

## Beispiel 3 — ReCreate Hohlkammerdecke

Bei einer wiederverwendeten Hohlkammerdecke sind die wichtigsten semantischen Griffe meist Modul- und Fugenausrichtung. Eine Längsfuge kann ein `alignment_handle` werden. Ober- und Unterseite werden nur dann zu `stack_handle`, wenn das System vertikale Anordnung, Niveaukontinuität oder Modulstapelung prüft.

Sichtbarkeit ist optional und sollte nur modelliert werden, wenn die Plattenuntersicht oder die Wiederverwendungsidentität Teil der architektonischen Absicht ist.

---

# 10. Paket 5 — Logistik / Montage

## Zweck

Das Logistik-/Montagepaket speichert nur die Handling-Abstraktion für Heben, Lagern, Transport, Schutz, Zugang und temporäre Montagezustände.

## Minimale Repräsentation

Repräsentationstypen:

- Handlingmodell
- Transportmodell
- Lagermodell
- Hebemodell
- Montagezugangsmodell
- Temporärabstützungsmodell
- Schutzmodell

## Minimale Eigenschaften

- Masse
- Transportmaße
- Schwerpunktstatus
- Lagerorientierung
- Hebestatus
- Zugangsstatus
- Schutzstatus
- Status temporärer Abstützung
- Transportstatus

## Minimale Connectoren und Ports

Nur diese verwenden:

- `lifting_handle` mit `lifting_port`
- `storage_handle` mit `storage_port`
- `transport_handle` mit `transport_port`
- `access_handle` mit `access_port`
- `protection_handle` mit `protection_port`
- `temporary_bracing_handle` mit `temporary_bracing_port`

## Minimale Prüfungen

- Hebbarkeit
- Schwerpunkt
- Kran-Zugang
- Hebe-Nachweis erforderlich
- Lagerorientierung
- Auflagerabstand
- Trennhölzer erforderlich
- Transporthülle
- Ladungssicherung
- Routenbeschränkungen
- Montagezugang
- Zugang zu Connectoren
- Witterungsschutz
- Kantenschutz
- temporäre Stabilität

## Was außerhalb bleibt

Das Paket erzeugt keinen finalen Hebeplan, keine Kranauslegung, keine Transportgenehmigung, keine vollständige Baustellenlogistik und keine finale Montagesequenz.

## Beispiel 1 — Abbau/Aufbau DE_1OG_001

Die Deckenplatte braucht einen Lagergriff für liegende Lagerung, einen Transportgriff für Ladungssicherung und Transporthülle, einen Hebegriff, falls sie gehoben wird, und einen Schutzgriff, wenn Kanten oder Oberflächen während der Lagerung geschützt werden müssen.

Die Katalogmasse von ca. 4.1 t unterstützt Logistik-Vorprüfungen. Der Hebe-Nachweis braucht aber eigene Evidenz.

## Beispiel 2 — SlabBeamColumnFragment

Das Fragment ist im Handling komplexer, weil Platten-, Träger- und Stützenregionen einen unregelmäßigen Schwerpunkt und empfindliche Schnittflächen erzeugen. Es braucht einen Hebegriff, einen Lagergriff, einen Schutzgriff für Schnittflächen und schadenssensible Kanten sowie möglicherweise einen temporären Abstützgriff, falls es während der Montage instabil ist.

Es sollte keine generischen Hebeconnectoren auf jeder Region erhalten. Ein oder zwei Hebekandidaten reichen, bis ein Hebekonzept geplant ist.

## Beispiel 3 — ReCreate Hohlkammerdecke

Die ReCreate-Hohlkammerdecke braucht Hebe-, Transport- und Lagergriffe. Das entspricht der Pilotlogik: Elemente wurden gehoben, transportiert, codiert beziehungsweise rückverfolgt und gelagert. QR-Tracking gehört zu Nachweis / Identität, nicht zum Logistikconnector selbst.

Das Logistikpaket prüft Transportmaße, Ladungssicherung, Lagerauflager und ob Hebedaten vollständig sind.

---

# 11. Paket 6 — Nachweis-Overlay

## Zweck

Das Nachweis-Overlay speichert, wo Nachweise lokalisiert sind und wie sie Connectoren anderer Pakete beeinflussen.

Nachweise erzeugen niemals Connectoren.  
Nachweise modifizieren Connectoren.

## Minimale Repräsentation

Repräsentationstypen:

- Scan-Overlay
- Schadens-Overlay
- Prüfpunkt-Overlay
- Fotoannotations-Overlay
- Konfidenz-Overlay
- Unbekannte-Zone-Overlay

## Minimale Eigenschaften

- Nachweistyp
- Ort
- Konfidenz
- Quelle
- Datum
- betroffenes Paket
- betroffener Connector
- betroffener Port
- Effekt
- Begründung
- Nachweisstatus

## Connectoren und Ports

Keine.

## Minimale Effekte

- bestätigt
- Warnung
- blockiert
- Vertrauen reduziert
- manuelle Prüfung erforderlich
- Ingenieurnachweis erforderlich

## Minimale Prüfungen

- Wenn Nachweis einen Connector überlagert, wird der Connector-Status modifiziert.
- Wenn eine unbekannte Zone einen Connector überlagert, wird Warnung oder Blockade gesetzt.
- Wenn Schaden einen Connector überlagert, wird Warnung oder manuelle Prüfung gesetzt.
- Wenn ein Bewehrungsscan eine Ankerzone freigibt, kann die Verbindung zur Ingenieurprüfung weitergegeben werden.
- Wenn Prüfdaten eine Materialeigenschaft bestätigen, steigt die Konfidenz.

## Beispiel 1 — Abbau/Aufbau Bewehrungsnachweis

Wenn die Bewehrungslage unbekannt ist, markiert das Nachweis-Overlay betroffene Ankerverbindungen als Warnung oder blockiert. Wenn ein Scan eine freie Ankerzone bestätigt, kann die Ankerverbindung zur Ingenieurprüfung weitergehen.

Das Nachweis-Overlay erzeugt keinen Ankerconnector. Es modifiziert nur den strukturellen Ankerconnector.

## Beispiel 2 — SlabBeamColumnFragment Schnittflächen-Nachweis

Die Schnittfläche des Fragments kann Bewehrung freilegen oder unterbrechen. Das Nachweis-Overlay kann die Kontinuitätsverbindung als ingenieurpflichtig markieren, das Vertrauen in die Lastübertragung reduzieren oder warnen, wenn ein Schaden einen sichtbaren architektonischen Griff überlagert.

Nachweis verknüpft die strukturellen, semantischen und logistischen Konsequenzen, ohne neue Connectoren zu erfinden.

## Beispiel 3 — ReCreate Prüfung und QR-Nachweis

BIM-Inventarisierung, Codierung, QR-Tracking, Prüfungen und Neuberechnungen aus ReCreate können die Konfidenz von Basisgeometrie, Rückverfolgbarkeit und Tragfähigkeitsstatus erhöhen.

QR-Nachweis bestätigt Identität und Rückverfolgbarkeit. Belastungsprüfungen oder Neuberechnungen können die strukturelle Konfidenz erhöhen. Unbekannte Fugenschäden können Verbindungen weiterhin als manuell zu prüfen markieren.

---

# 12. Kompakte globale Kompatibilitätsregeln

Die globale Regelliste bleibt kurz.

| Regel | Kompatible Ports | Minimale Prüfungen |
|---|---|---|
| strukturelles Auflager | `bearing_side → support_side` | Überlappung, Richtung, Auflagerlänge |
| strukturelle Verankerung | `anchor_side → support_side` | Randabstand, Bewehrungskonflikt, Machbarkeit |
| strukturelle Kontinuität | `continuity_side → continuity_side` | Ausrichtung, Bewehrungskontinuität, Kraftschluss |
| strukturelle Lastübertragung | `transfer_side → support_side / bearing_side` | Lastpfad, lokale Pressung |
| thermische Kontinuität | `thermal_side → thermal_side` | Grenzkontinuität |
| Dämmkontinuität | `insulation_side → insulation_side` | Schichtkontinuität, Lücke |
| Hüllendurchdringung | `penetration_side → thermal_side / insulation_side` | Abdichtung, Luftdichtheit, Feuchte |
| TGA-Leitungsführung | `route_side → route_side` | Leitungsflucht, Lichtraum |
| TGA-Öffnung | `opening_side → route_side` | Durchmesser, Randabstand, Tragwerkskonflikt |
| TGA-Bohrung | `drilling_side → route_side` | Durchmesser, Bewehrungskonflikt, Tragwerkskonflikt |
| architektonischer Zugang | `access_port → access_port` | Lichtraum, Annäherung |
| architektonische Stapelung | `top_port → bottom_port` | vertikale Ausrichtung, Höhendifferenz |
| architektonische Ausrichtung | `alignment_port → alignment_port` | Raster, Fuge, Datum |
| Logistik Heben | `lifting_port → Prozessanforderung` | Hebbarkeit, Schwerpunkt |
| Logistik Lagerung | `storage_port → Lagerbedingung` | Orientierung, Auflager, Trennhölzer |

---

# 13. Komplettes Beispiel A — Abbau/Aufbau DE_1OG_001

Die Deckenplatte **DE_1OG_001** ist das saubere Beispiel für ein einzelnes Bauteil.

## Minimale Komponentendaten

- Typologie: Deckenplatte
- Material: Stahlbeton
- Maße: 4500 × 2300 × 180 mm
- Volumen: 1.863 m³
- Masse: ca. 4.1 t

## Paketabstraktionen

Die Basisgeometrie speichert die Platte als neutralen Körper mit Maßen, Volumen, Flächen, Kanten und Öffnungsstatus.

Das Tragwerk repräsentiert sie als Platte mit Auflager an relevanten Kanten. Anker- und Kontinuitätsconnectoren werden nur ergänzt, wenn der Entwurf eine Abbau/Aufbau-Anschlussfamilie wie Schraubanker, Flachstahlhalter oder nachträglichen Bewehrungsanschluss mit Verguss nutzt.

Energie / Gebäudehülle bleibt inaktiv, solange die Platte nicht Dach, Außenboden oder Hüllenbauteil wird. Erst dann entstehen Connectoren für Dämmkontinuität, Wärmebrückenwarnung oder Durchdringungsabdichtung.

TGA / Öffnungen ergänzt Öffnungs- oder Bohrconnectoren nur, wenn eine Öffnung existiert oder eine Leitung vorgeschlagen wird.

Semantik / Architektur ergänzt Ausrichtungs- oder Sichtbarkeitsconnectoren nur, wenn Plattenkante, Untersicht oder Raster Teil der Entwurfslogik werden.

Logistik / Montage ergänzt Lager-, Transport-, Hebe- und Schutzgriffe, weil Masse, Lagerung und Handling für reale wiederverwendete Betonbauteile immer relevant sind.

Das Nachweis-Overlay modifiziert Tragwerks- und Logistikconnectoren, wenn Bewehrung, Schaden oder Hebedaten fehlen.

---

# 14. Komplettes Beispiel B — SlabBeamColumnFragment

Das **SlabBeamColumnFragment** ist eine vorgeschlagene Systemtypologie, abgeleitet aus der Fragmentlogik der Abbau/Aufbau-Masterarbeit.

## Minimale Bauteilidee

Es ist ein monolithisches wiederverwendetes Betonfragment mit:

- einem plattenartigen Bereich
- einem integrierten trägerartigen Bereich
- einem stützenartigen Bereich
- Schnittflächen und räumlich besonderen Qualitäten

## Korrekte abstrakte Repräsentation

Nicht als ein unscharfes `monolithic_structural_fragment` modellieren.

Stattdessen als kleinen Graphen:

- Plattenbereich → Platte
- Trägerbereich → Trägerlinie
- Stützenbereich → Stützenlinie
- Schnittpunkt Platte-Träger-Stütze → Transferknoten
- Schnittfläche → Kontinuitätszone, falls Kraftschluss erforderlich ist

## Paketabstraktionen

Die Basisgeometrie speichert das Fragment als einen durchgehenden Körper mit Teilregionen, nicht als getrennte Bauteile.

Das Tragwerk zerlegt es in Platte, Trägerlinie, Stützenlinie, Transferknoten und Kontinuitätszone. Die minimalen Connectoren sind Auflager, Lastübertragung und Kontinuitätsverbindung.

Energie / Gebäudehülle aktiviert sich nur, wenn das Fragment Teil der Hülle wird. Der Platten-Träger-Stützen-Knoten kann dann zur Wärmebrückenwarnung werden.

TGA / Öffnungen behandelt Träger- und Stützenbereiche als wahrscheinlich blockierte Zonen. Ein Bohrkandidat entsteht nur, wenn eine Leitungsführung vorgeschlagen wird.

Semantik / Architektur ist besonders wichtig: Das Fragment kann eine Nische, eine Stütze-im-Raum-Situation, eine räumliche Schwelle oder eine sichtbare Wiederverwendungsidentität erzeugen. Benötigt werden nur Zugangs-, Seiten-, Ausrichtungs- und Sichtbarkeitsgriffe.

Logistik / Montage nutzt Hebe-, Lager-, Schutz- und temporäre Abstützgriffe, weil das Fragment unregelmäßig und schwierig zu handhaben ist.

Das Nachweis-Overlay modifiziert die Konfidenz von Kontinuität und Lastübertragung, wenn Bewehrung an Schnittflächen, Schäden oder Materialzustand unbekannt sind.

---

# 15. Komplettes Beispiel C — ReCreate Hohlkammerdecke

Das ReCreate-Beispiel verwendet eine wiedergewonnene Hohlkammerdecke.

## Minimale Bauteilidee

Es handelt sich um eine einachsig spannende Betonfertigteildecke mit:

- Endauflagerzonen
- Längsfugen
- Hohlkammern
- Transport- und Trackinghistorie
- Prüf- oder Neuberechnungsnachweisen

## Paketabstraktionen

Die Basisgeometrie speichert Plattenkörper, Längshohlräume, Stirnflächen, Kanten und Nettovolumen.

Das Tragwerk repräsentiert sie als einachsig spannende Platte. Es benötigt Auflagerconnectoren an beiden Enden und einen Fugenconnector entlang der Längskante. Die Tragfähigkeit hängt von Prüfung oder Neuberechnung ab.

Energie / Gebäudehülle aktiviert sich nur, wenn die Platte als Dach oder außenliegende Decke verwendet wird. Dann können Dämmkontinuität, Wärmebrückenwarnung oder Durchdringungsabdichtung entstehen.

TGA / Öffnungen kann eine Hohlkammer nur dann als Leitungsführung behandeln, wenn der Entwurf dies ausdrücklich nutzt. Sonst bleiben Hohlkammern Eigenschaften.

Semantik / Architektur nutzt vor allem Ausrichtungsgriffe für Modul- und Fugenausrichtung. Stapelgriffe werden nur ergänzt, wenn Niveau oder vertikale Stapellogik geprüft wird.

Logistik / Montage nutzt Hebe-, Transport- und Lagergriffe, weil die ReCreate-Piloten Heben, Transport, Lagerung und Rückverfolgung beinhalten.

Das Nachweis-Overlay speichert BIM-Inventar, QR- oder Codierungsdaten, Prüfungen, Belastungstests und Neuberechnungsstatus. Es modifiziert strukturelle Konfidenz und Rückverfolgbarkeit, erzeugt aber keine Connectoren.

---

# 16. Finale saubere Regel

Beschreibungen werden als Eigenschaften gespeichert.  
Handlungsrelevante Griffe werden als Connectoren gespeichert.  
Kompatibilität wird über Ports beschrieben.  
Nachweise modifizieren Konfidenz, Warnungen oder Blockaden.

Das minimale System vermeidet lange Connector-Vokabulare und hält jedes Paket klein:

- Basisgeometrie: keine Connectoren
- Tragwerk: 5 Connector-Typen
- Energie / Gebäudehülle: 4 Connector-Typen
- TGA / Öffnungen: 4 Connector-Typen
- Semantik / Architektur: 7 Connector-Typen
- Logistik / Montage: 6 Connector-Typen
- Nachweis-Overlay: keine Connectoren

Das reicht aus, um Entwerfen mit wiederverwendeten Bauteilen zu unterstützen, ohne jede Fläche, Kante oder Projektdetail zu übermodellieren.
