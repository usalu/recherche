---
id: "Legacy_gebaeude_Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien."
entity: "quelle"
node_kind: "source"
migration_status: "migrated_phase5_legacy_source"
title: "Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur"
legacy_path: "gebaeude\\Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien.md"
migration_action: "archive_as_source"
legacy_type: ""
target_primary: "90_import_rohdaten/Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien"
target_secondary: ""
risk_flags: "contains_multiple_cases_or_schema_notes"
---
# Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur

## Migration

- Legacy path: gebaeude\Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien.md
- Action in migration map: archive_as_source
- Reason: not already consumed by phase 1-4, so preserved as source/meta node.
- Original primary target: 90_import_rohdaten/Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien
- Original secondary targets: 

## Legacy Content

# Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur

**Stand:** 2026-05-06  
**Untersuchte Dateien:** 92 erzeugte Gebäude-`.md`-Dateien im Chat/Arbeitsordner.  
**Nicht als Gebäude-Datei gezählt:** `gebäude4_wiederverwendung_direct_reuse_examples.md` als Prioritäten-/Regeldatei.

---

## 1. Kurzfazit

Die bisherige Entitätenstruktur ist grundsätzlich brauchbar, aber die Gebäude-Fallstudien zeigen fünf wiederkehrende Lücken:

1. **Donor-/Empfängerbeziehungen** sind zu wichtig, um nur als Notiz unter `Gebäude` zu laufen.
2. **Quellenkonflikte, Vertrauensgrad und Projektstatus** brauchen eigene, standardisierte Felder/Entitäten.
3. **Direct Reuse vs. Bestandserhalt vs. Recycling vs. DfD** muss als Bewertungs- und Abgrenzungslogik expliziter modelliert werden.
4. **Prüfung, Zulassung, Haftung und Gewährleistung** kommen in fast allen technischen Fällen vor, sind aber noch zu grob gefasst.
5. **Reuse-Ketten** wie House of Fraser → TBC.London oder donor/receiver streams passen nicht sauber in eine reine Gebäude-Fallstudie.

---

## 2. Auswertung der 92 Gebäude-Dateien

### 2.1 Normalisierte Entscheidung

| Normalisierte Entscheidung | Anzahl |
|---|---:|
| VERGLEICHSFALL | 40 |
| HAUPTFALL | 22 |
| ANHANG / WATCHLIST | 18 |
| VERGLEICHSFALL / ANHANG | 6 |
| HAUPTFALL / VERGLEICHSFALL | 4 |
| ENTFERNEN / DfD-Anhang | 2 |

### 2.2 Normalisierte Bewertung

| Bewertung | Anzahl |
|---|---:|
| ★★★★★ | 8 |
| ★★★★☆ | 30 |
| ★★★☆☆ | 31 |
| ★★☆☆☆ | 22 |
| Remove / appendix | 1 |

### 2.3 Normalisierter Projektstatus

| Projektstatus | Anzahl |
|---|---:|
| gebaut | 68 |
| Prototyp / Demonstrator | 8 |
| geplant | 5 |
| temporär / Pavillon | 5 |
| im Bau | 3 |
| ungebaut / abgebrochen / ersetzt | 2 |
| unklar / verify | 1 |

### 2.4 Häufigste Entitäten im Mapping

| Entität | Häufigkeit in Mappings |
|---|---:|
| People | 291 |
| Bauteil | 275 |
| Kennwert | 196 |
| Gebäude | 104 |
| Fallstudie | 92 |
| Projekt | 90 |
| Ort | 90 |
| Material | 78 |
| Hürde | 70 |
| Reuse-Strategie | 67 |
| Prüfung | 57 |
| Wirtschaft | 43 |
| Norm | 38 |
| Logistik | 31 |
| Methode | 31 |
| Aufbereitungsmethode | 29 |
| Tragwerkssystem | 29 |
| Verbindung | 26 |
| Abbruchmethode | 25 |
| Recht | 23 |

### 2.5 Häufigste neue/ungeklärte Entitätsvorschläge aus den Fallstudien

Diese Vorschläge traten mehrfach oder systematisch auf und sollten bereinigt werden:

| Rohvorschlag aus Fallstudien | Problem | Vorschlag |
|---|---|---|
| Spendergebäude / Donorgebäude / Donor-Gebäude / Donor Building | vier Bezeichnungen für denselben Sachverhalt | **Donorgebäude** als Standarddatei |
| Empfängergebäude | noch nicht als klare Entität vorhanden | **Empfängergebäude** ergänzen |
| Donor-Receiver-Kette / Reuse-Kette / Donor-Projekt | Fälle mit mehreren Gebäuden/Materialströmen | **Reuse-Kette** als neue Entität |
| Quellenkonflikt / Quellenkonflikt-Kennwert / Quellenunsicherheit | wiederkehrende Datenqualitätsthemen | **Quellenkonflikt** und **Quellenqualität** ergänzen |
| Materialpass | existiert teils als Dokument/Datenmodell, aber uneinheitlich genutzt | auf **Dokument/Materialpass.md** + **Datenmodell/Materialpass_Schema.md** mappen |
| Fertigteilsystem | teils als neue Entität, teils Tragwerkssystem | unter **Tragwerkssystem/Betonfertigteil_System.md** konsolidieren |
| ReUse-Interior / Circular Workplace | oft grenzwertig wegen Möbeln | als **Reuse-Strategie/Fest_eingebauter_Innenausbau.md** führen |
| Remanufactured Reuse-Bauteil | wichtig für CascadeUp/FLO:RE-ähnliche Fälle | neue Reuse-Strategie oder Bauteilstatus ergänzen |
| Free-Issue-Material / Surplus-Industriebauteil / Material Stockpile | Beschaffungslogik fehlt | unter **Beschaffungsmodell** und **Materialquelle** ergänzen |
| Pilotnummerierung / Doppellisteneintrag | z. B. Schildow-Fälle | **Fall-Deduplikation** als Qualitätsentität ergänzen |

---

## 3. Hauptprobleme der aktuellen Struktur

### 3.1 `People` ist zu breit, Rollen fehlen

In den Gebäude-Dateien wurden `Architekt`, `Bauherr`, `Tragwerksplaner` und ähnliche Rollen teils als eigene Entitäten verwendet. Besser: **Akteur** bleibt die Entität, die Rolle wird als Beziehung gespeichert.

**Empfohlene Rollen:**

- Bauherr / Auftraggeber
- Architekt
- Tragwerksplaner
- Reuse-Beratung
- Rückbauunternehmen
- Stahlbau / Holzbau / Fertigteilbau
- Prüfingenieur / Prüfstelle
- Materialbroker / Bauteilbörse
- Fördergeber
- Genehmigungsbehörde
- Betreiber / Nutzer

### 3.2 `Gebäude` braucht Subrollen

Viele Fälle enthalten mindestens zwei Gebäude: Donor und Empfänger. Bei Reuse-Ketten sogar mehr.

**Neue Rollen innerhalb `Gebäude`:**

- Empfängergebäude
- Donorgebäude
- Donor-Infrastruktur
- Bestand am Ort
- Prototyp / Demonstrator
- transloziertes Gebäude
- abgebrochener / ersetzter Entwurf

### 3.3 `Norm`, `Recht`, `Prüfung`, `Haftung` sind zu wenig getrennt

Bei tragenden Bauteilen reicht eine pauschale Zeile „Norm/Recht unbekannt“ nicht. Für spätere Wissensgraphen sollte unterschieden werden:

- Leistungsanforderung
- Prüfverfahren
- Prüfnachweis
- Zulassungs-/Genehmigungsweg
- Haftungs-/Gewährleistungsmodell
- Versicherbarkeit

### 3.4 `Kennwert` braucht Datenqualität

Viele Werte sind Quellenkonflikte: Fläche, CO₂, Masse, Bauteilanzahl, Kosten. Deshalb sollte jeder Kennwert Pflichtfelder für Datenqualität bekommen:

- Werttyp: gemessen / berechnet / geschätzt / behauptet / sekundär übernommen
- Bezugsgröße: Bauteil / Gebäude / Materialstrom / Projekt / Lebenszyklusphase
- Bilanzgrenze
- Quelle
- Quellenkonflikt ja/nein
- bevorzugter Wert und Begründung

### 3.5 `Bauteil` braucht Lebenslauf statt nur Inventarzeile

Für Direct Reuse ist nicht nur „Bauteil = Träger“ wichtig, sondern der **Bauteilverlauf**:

1. Donorort
2. alte Funktion
3. Ausbau/Rückbau
4. Prüfung
5. Transport
6. Lagerung
7. Aufbereitung
8. neue Funktion
9. neue Verbindung
10. zukünftige Demontierbarkeit

---

## 4. Angepasste Kern-Entitätenstruktur

Die bestehende Struktur sollte nicht ersetzt, sondern erweitert und normalisiert werden.

### 4.1 Bestehende Entitäten beibehalten

Diese Entitäten bleiben sinnvoll:

- Akteur / People
- Abbruchmethode
- Aufbereitungsmethode
- Bauteil
- Bauteilbörse
- Bericht
- Datenmodell
- Dokument
- Fallstudie
- Förderprogramm
- Gebäude
- Hürde
- Kennwert
- Leistungsanforderung
- Logistik
- Material
- Methode
- Norm
- Ort
- Prüfung
- Recht
- Reuse-Strategie
- Schadstoff
- Software
- Tool
- Tragwerkssystem
- Verbindung
- Wirtschaft

### 4.2 Umbenennung / Konsolidierung empfohlen

| Aktuelle Uneinheitlichkeit | Zielstruktur |
|---|---|
| `People`, `akteur`, `Architekt`, `Bauherr`, `Tragwerksplaner` | `Akteur` als Entität, Rolle als Attribut |
| `gebaeude` und `Gebäude` | einheitlich `Gebäude` |
| `Norm/Recht` | aufteilen in `Norm` und `Recht` |
| `Software/Tool` | aufteilen in `Software` und `Tool` |
| `Donorgebäude`, `Spendergebäude`, `Donor Building` | `Donorgebäude` |
| `Quellenkonflikt-Kennwert`, `Quellenunsicherheit` | `Quellenkonflikt` + `Quellenqualität` |

---

## 5. Vorgeschlagene neue Entitätsgruppen und Dateien

### 5.1 Neue Gruppe: `09_reuse_ketten_herkunft`

Diese Gruppe ist nötig, weil viele Fallstudien nicht nur ein Objekt, sondern Materialströme zwischen Donor und Empfänger beschreiben.

| Neue Datei | Warum nötig? | Typische Fälle |
|---|---|---|
| `Donorgebaeude.md` | Herkunftsgebäude standardisieren | BioPartner 5, KA13, K.118, Recypark |
| `Empfaengergebaeude.md` | neues Einbaugebäude standardisieren | fast alle ex-situ-Fälle |
| `Donor_Receiver_Kette.md` | Materialfluss zwischen mehreren Gebäuden | House of Fraser → TBC.London |
| `Reuse_Kette.md` | allgemeiner als Donor-Receiver, auch mehrere Zwischenstationen | Stahlreuse London, Rotor-DC-Fälle |
| `Materialquelle.md` | Quelle kann Gebäude, Börse, Lager, Industrie, Infrastruktur sein | Saxum, Big Dig, Superuse-Fälle |
| `Urban_Mining_Stream.md` | Materialstrom aus Rückbau/Abbruch | ReCreate, PRECS, House of Fraser |
| `Infrastruktur_Donor.md` | Donor ist Brücke, Tunnel, Infrastruktur, nicht Gebäude | Big Dig House, Re:Crete |
| `Surplus_Industriebauteil.md` | Überschuss-/Industriebauteile | Saxum drill-stem pipe, Restposten-Fenster |
| `Free_Issue_Material.md` | Bauherr stellt Gebrauchtmaterial bereit | UK-Stahlreuse-Fälle |
| `Material_Stockpile.md` | Zwischenlager/Materiallager als Wissensobjekt | Baustellenlager, Reuse-Hubs |

### 5.2 Neue Gruppe: `10_status_bewertung_quellenqualitaet`

| Neue Datei | Zweck |
|---|---|
| `Projektstatus.md` | gebaut / im Bau / geplant / Prototyp / ungebaut / ersetzt normalisieren |
| `Fallentscheidung.md` | Hauptfall / Vergleichsfall / Anhang / Entfernen normalisieren |
| `Bewertungsstufe.md` | Sternebewertung und Regeln dokumentieren |
| `Vertrauensgrad.md` | belegt / teilweise belegt / unklar standardisieren |
| `Quellenqualitaet.md` | Primärquelle, Sekundärquelle, Datenbank, Presse, ungeprüfter Claim |
| `Quellenkonflikt.md` | widersprüchliche Werte erfassen |
| `Datenluecke.md` | fehlende Daten strukturiert sammeln |
| `Fall_Deduplikation.md` | doppelte/unscharfe Fälle markieren, z. B. Schildow |
| `Watchlist.md` | geplante oder noch nicht fertiggestellte Fälle |
| `Entfernen_DfD_Anhang.md` | reine DfD-/future-reuse-Fälle getrennt halten |

### 5.3 Neue Gruppe: `11_pruefung_nachweis_zulassung`

| Neue Datei | Zweck |
|---|---|
| `Reuse_Pruefdossier.md` | Sammelobjekt für Prüfung, Nachweis, Freigabe |
| `Tragfaehigkeitsnachweis_Bestandsbauteil.md` | wiederverwendete tragende Bauteile |
| `Materialpruefung_Bestandsstahl.md` | Stahlfälle wie BioPartner 5, Holbein, 55 GSS |
| `Holzpruefung_Bestandsbauteil.md` | Recypark, Svanen, CascadeUp |
| `Betonpruefung_Bestandsfertigteil.md` | WBS70, PRECS, ReCreate |
| `Sichtpruefung.md` | häufige Erstprüfung |
| `Destruktive_Pruefung.md` | Probenahme, Zugprobe, Materialtest |
| `Lastversuch.md` | FLO:RE, Re:Crete, Prototypen |
| `Schadstoffscreening.md` | Altbauteile vor Ausbau |
| `Reuse_Freigabe.md` | projektspezifische technische Freigabe |
| `Zulassung_im_Einzelfall.md` | wenn Standardnachweis fehlt |
| `Pruefzeugnis.md` | Dokumenttyp für Bauteilprüfung |

### 5.4 Neue Gruppe: `12_recht_haftung_gewaehrleistung`

| Neue Datei | Zweck |
|---|---|
| `Bauproduktstatus_Gebrauchtbauteil.md` | Neuware vs. Gebrauchtbauteil |
| `Haftungsmodell_Reuse.md` | Verantwortlichkeiten erfassen |
| `Gewaehrleistungsmodell_Reuse.md` | Gewährleistung bei Gebrauchtbauteilen |
| `Versicherung_Reuse.md` | Versicherbarkeit / Risiko |
| `Ausschreibung_Reuse_Bauteile.md` | Vergabe und Leistungsverzeichnis |
| `Beschaffungsrisiko.md` | Verfügbarkeit, Timing, Qualität |
| `Eigentumsuebergang_Bauteil.md` | wem gehört das Bauteil wann? |
| `Bauaufsichtliche_Genehmigung_Reuse.md` | Genehmigungsbezug ohne konkrete Normnummern zu erfinden |

### 5.5 Neue Gruppe: `13_beschaffung_logistik_lagerung`

| Neue Datei | Zweck |
|---|---|
| `Selektiver_Rueckbau.md` | kontrollierte Gewinnung wiederverwendbarer Bauteile |
| `Bauteilernte.md` | Harvesting als Prozess |
| `Zwischenlager.md` | häufige Hürde |
| `Just_in_Time_Reuse.md` | direkte Donor-zu-Empfänger-Logistik |
| `Transportdistanz.md` | Kennwert + Logistik |
| `Materialbroker.md` | Rolle / Akteurstyp |
| `Reuse_Beschaffungsmodell.md` | Börse, Direktbeschaffung, Free Issue, Self-Harvesting |
| `Bauteilreservierung.md` | frühzeitige Sicherung verfügbarer Bauteile |
| `Rueckbauzeitfenster.md` | Timing-Risiko |
| `Bauteilkennzeichnung.md` | IDs, QR-Codes, Inventar |

### 5.6 Neue Gruppe: `14_reuse_strategien_spezifisch`

| Neue Datei | Zweck |
|---|---|
| `Ex_situ_Bauteilwiederverwendung.md` | Kernstrategie vieler Hauptfälle |
| `In_situ_transformierte_Wiederverwendung.md` | Thoravej, Bestandselemente mit neuer Funktion |
| `Gebaeudeversetzung.md` | Christus-Pavillon, ggf. Pavillons |
| `Fest_eingebauter_Innenausbau.md` | Innenausbau zählt nur, wenn fest/räumlich/technisch |
| `Tragende_Bauteilwiederverwendung.md` | Bewertungsanker für ★★★★★ |
| `Envelope_Reuse.md` | Fenster, Fassaden, Dach, Cladding |
| `TGA_Reuse.md` | Radiatoren, Lüftung, Sanitär, Leuchten, Kabeltrassen |
| `Remanufactured_Reuse.md` | CascadeUp: Rückbauholz zu neuen Holzbauteilen |
| `Materialwiederverwendung_vs_Recycling.md` | saubere Abgrenzung |
| `Design_for_Disassembly_ohne_Direct_Reuse.md` | Brummen/Moringa-artige Anhangsfälle |

### 5.7 Neue/erweiterte Bauteil-Dateien

| Neue Datei | Fälle / Begründung |
|---|---|
| `Hohlkoerperdecke.md` | KA13, ReCreate, Montessori, Melkinlaituri |
| `Brettschichtholzbogen.md` | Recypark Demets |
| `Stahlprofil_Bestandsstahl.md` | BioPartner 5, Holbein, 55 GSS, Timber Square |
| `Drill_Stem_Pipe.md` | Saxum Vineyard |
| `Betonblock_Zuschnitt.md` | Re:Crete, Superlocal Expogebouw |
| `WBS70_Wandplatte.md` | deutsche PRECS-Fälle |
| `P2_Wandplatte.md` | Bröthen/Hoyerswerda |
| `Recover_Brick_Module.md` | Resource Rows, De Schilders |
| `Holzfensterrahmen.md` | Europa Building |
| `Fassadenpaneel_Second_Life.md` | TRÆ, Upcycle, The Green House |
| `Radiator.md` | ELYS, Grande Halle, Verbiest/Karreveld |
| `Lueftungsgeraet.md` | Zinneke, Verbiest/Karreveld |
| `Sanitaerobjekt_Gebraucht.md` | BioPartner 5, Grande Halle, Werkhof 29 |
| `Feuerschutztuer_Gebraucht.md` | Zinneke, Colombelles |
| `Treppenanlage_Gebraucht.md` | Mööslistrasse, Grubenstrasse, WBS70-Fälle |

---

## 6. Angepasstes Entity-Mapping für künftige Gebäude-Dateien

Die bisherige Tabelle sollte erweitert werden, damit Beziehungen klarer auswertbar werden.

### Neue Mapping-Tabelle

| Entität | Datei / Zielknoten | Wert | Rolle | Beziehung zur Fallstudie | Belegstatus | Quelle | Vertrauensgrad | Datenlücke |
|---|---|---|---|---|---|---|---|---|
| Gebäude | `Gebäude/Donorgebaeude.md` | z. B. Gorlaeus-Hochhaus | Donor | liefert Stahltragwerk | belegt | [Sx] | belegt | Prüfwerte unbekannt |
| Gebäude | `Gebäude/Empfaengergebaeude.md` | BioPartner 5 | Empfänger | nimmt Stahltragwerk auf | belegt | [Sx] | belegt | — |
| Akteur | `Akteur/Reuse_Beratung.md` | Rotor | Reuse-Beratung | Materialsuche / Prozess | belegt | [Sx] | belegt | Leistungsumfang unbekannt |
| Bauteil | `Bauteil/Stahlprofil_Bestandsstahl.md` | Stahlträger | tragend | neue Tragstruktur | belegt | [Sx] | belegt | Profilanzahl unbekannt |
| Prüfung | `Pruefung/Tragfaehigkeitsnachweis_Bestandsbauteil.md` | Nachweis | technischer Nachweis | ermöglicht Wiedereinbau | teilweise belegt | [Sx] | teilweise belegt | Prüfprotokoll nicht öffentlich |
| Quellenqualität | `Status/Quellenkonflikt.md` | 24/25 t Stahl | Kennwertkonflikt | widersprüchliche Mengenangabe | belegt | [Sx], [Sy] | teilweise belegt | Originaldokument prüfen |

---

## 7. Erweiterte Gebäude-Fallstudienvorlage

Diese Version ist besser auf die analysierten Fälle zugeschnitten.

```markdown
# [GEBÄUDE / PROJEKT] — Fallstudie Direct Reuse / Wiederverwendung

## 0. METADATEN
- Datei:
- Fall-ID:
- Land:
- Stadt / Ort:
- Falltyp: Gebäude / Infrastruktur / Pavillon / Prototyp / Reuse-Kette / DfD-Anhang
- Projektstatus: gebaut / im Bau / geplant / Prototyp / ungebaut / ersetzt / unbekannt
- letzte Prüfung:
- Quellenstand:

## 1. EINORDNUNG
- Entscheidung: HAUPTFALL / VERGLEICHSFALL / ANHANG / WATCHLIST / ENTFERNEN
- Bewertung: ★ bis ★★★★★
- Zählt als Direct Reuse? ja / teilweise / nein
- Hauptgrund für Bewertung:
- Vertrauensgrad: belegt / teilweise belegt / unklar
- Warnung Bestandserhalt: ja/nein + Begründung
- Warnung Möbel/Dekoration: ja/nein + Begründung
- Warnung Recycling/DfD: ja/nein + Begründung
- Fallgrenze: was wird gezählt / was wird ausgeschlossen?

## 2. DONOR-RECEIVER-LOGIK
| Rolle | Name | Ort | alte Nutzung | neue Nutzung | Beziehung | Status | Quelle | Vertrauensgrad |
|---|---|---|---|---|---|---|---|---|
| Donorgebäude / Donor-Infrastruktur |  |  |  |  | liefert Bauteil(e) |  |  |  |
| Empfängergebäude |  |  |  |  | nimmt Bauteil(e) auf |  |  |  |
| Zwischenlager / Bauteilbörse / Broker |  |  |  |  | vermittelt / lagert |  |  |  |

## 3. ENTITÄTEN-MAPPING
| Entität | Datei / Zielknoten | Wert | Rolle | Beziehung zur Fallstudie | Belegstatus | Quelle/Beleg | Vertrauensgrad | Datenlücke |
|---|---|---|---|---|---|---|---|---|

## 4. FALLSTUDIE
- Name:
- Ort:
- Gebäude:
- Projekt:
- Beteiligte Akteure + Rollen:
- Architekt:
- Tragwerksplaner:
- Bauherr:
- Reuse-Beratung:
- Rückbau / Ausbau:
- Zeitraum:
- Ursprüngliche Nutzung:
- Neue Nutzung:
- Fläche / Maßstab:
- Schutzstatus / Denkmalstatus:
- Quellenlage:

## 5. REUSE-STRATEGIE UND ABGRENZUNG
- Art der Wiederverwendung:
- Hauptniveau: Tragwerk / Hülle / Innenausbau / TGA / Material / Gesamtgebäude
- Wiederverwendungsmodus: ex-situ / in-situ transformiert / remanufactured / transloziert / Reuse-Kette
- Unterschied zu Sanierung:
- Unterschied zu Recycling:
- Unterschied zu DfD/future reuse:
- Warum ist der Fall relevant?

## 6. BAUTEIL-LEBENSLAUF / BAUTEIL-INVENTAR
| Bauteil | Material | Donor / Herkunft | alte Funktion | Ausbauart | Prüfung | Aufbereitung | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Verbindung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | Datenlücke |
|---|---|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|

## 7. PROZESS UND LOGISTIK
| Prozessphase | Handlung | Akteure/Rollen | Methode | Werkzeug/Software | Rückbau-/Ausbaumethode | Aufbereitung | Prüfung | Lagerung | Transport | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|---|

## 8. TECHNIK, LEISTUNG, PRÜFUNG, NORMEN
| Thema | Befund | Leistungsanforderung | Prüfung/Nachweis | Norm/Recht | Zulassung/Genehmigung | Haftung/Gewährleistung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|

## 9. KENNWERTE UND QUELLENKONFLIKTE
| Kennwert | Wert | Einheit | Werttyp | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad | Quellenkonflikt? | bevorzugter Wert / Begründung |
|---|---:|---|---|---|---|---|---|---|---|

## 10. HÜRDEN-MATRIX
| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|

## 11. WIRTSCHAFT UND BESCHAFFUNG
- Beschaffungsmodell:
- Materialquelle / Bauteilbörse / Donor:
- Eigentumsübergang:
- Kostenwirkung:
- Zeitwirkung:
- Versicherung / Haftung:
- Gewährleistung:
- Prüfkosten:
- Arbeitsaufwand:
- Lagerung:
- Marktbarrieren:

## 12. GESTALTUNG UND KULTURELLER WERT
- Sichtbarkeit der Wiederverwendung:
- räumliche Transformation:
- Atmosphäre / Ausdruck:
- Umgang mit Spuren / Patina:
- sozialer Wert:
- Denkmal- oder Bestandswert:
- Kritik / Grenzen:

## 13. OFFENE ENTITÄTEN UND DATENLÜCKEN
- Welche bestehenden Entitäten wurden nicht gefunden?
- Welche neuen Entitäten wären sinnvoll?
- Welche Daten fehlen?
- Welche Quellen müssten geprüft werden?
- Welche Primärquellen fehlen?

## 14. ABSCHLUSS
- Soll der Fall in die Hauptliste? ja/nein/Anhang/Watchlist
- 5 wichtigste Fakten:
- 5 wichtigste Bauteile:
- 5 wichtigste Hürden:
- 5 wichtigste übertragbare Erkenntnisse:
- 5 offene Fragen:

## 15. QUELLEN
- [S1]
- [S2]
```

---

## 8. Migrationsregeln für die bereits erstellten Gebäude-Dateien

| Bisher in Dateien gefunden | Künftig mappen auf |
|---|---|
| `People`, `Architekt`, `Bauherr`, `Tragwerksplaner` | `Akteur` + Rolle |
| `Spendergebäude`, `Donor-Gebäude`, `Donor Building` | `Donorgebäude` |
| `Empfängergebäude` | `Empfaengergebaeude` |
| `Quellenkonflikt-Kennwert`, `Quellenunsicherheit` | `Quellenkonflikt` |
| `Norm/Recht` | getrennt: `Norm` + `Recht` |
| `Software/Tool` | getrennt: `Software` + `Tool` |
| `Reuse-vs-Recycling-Abgrenzung` | `Materialwiederverwendung_vs_Recycling.md` |
| `ReUse-Interior`, `Circular Workplace` | `Fest_eingebauter_Innenausbau.md` |
| `Doppellisteneintrag`, `Pilotnummerierung` | `Fall_Deduplikation.md` |
| `Materialpass` | `Dokument/Materialpass.md` und/oder `Datenmodell/Materialpass_Schema.md` |
| `Fertigteilsystem` | `Tragwerkssystem/Betonfertigteil_System.md` |
| `Remanufactured Reuse-Bauteil` | `Remanufactured_Reuse.md` |

---

## 9. Empfohlene Pflichtfelder pro Gebäude-Datei

Diese Pflichtfelder reduzieren spätere Nacharbeit:

1. **Falltyp**: Gebäude / Infrastruktur / Pavillon / Prototyp / Reuse-Kette / DfD-Anhang.
2. **Zählt als Direct Reuse?** ja / teilweise / nein.
3. **Gezählte Bauteile** und **ausgeschlossene Elemente** getrennt aufführen.
4. **Donor-Receiver-Logik** separat vor dem Entitäten-Mapping.
5. **Belegstatus pro Bauteil**: belegt / teilweise belegt / unbekannt.
6. **Quellenkonflikt pro Kennwert**: ja/nein.
7. **Projektstatus normalisiert**: gebaut / im Bau / geplant / Prototyp / ungebaut / ersetzt / unbekannt.
8. **Reuse-Modus**: ex-situ / in-situ transformiert / transloziert / remanufactured / Reuse-Kette.
9. **Rechts-/Haftungsstatus**: öffentlich belegt / nicht belegt / unbekannt.
10. **Datenlücken** nicht nur am Ende, sondern auch je Tabelle.

---

## 10. Priorisierte nächste Schritte

1. **Bestehende Gebäude-Dateien nicht neu schreiben**, sondern beim nächsten Durchgang nur die Felder `Falltyp`, `Donor-Receiver-Logik`, `Quellenkonflikt` und `Zählt als Direct Reuse?` ergänzen.
2. **Neue Entitätsdateien zuerst für Donor/Receiver, Quellenqualität und Prüfung/Nachweis anlegen**, weil sie die meisten Lücken schließen.
3. **Akteur-Rollen normalisieren**, damit `People`, `Architekt`, `Bauherr`, `Tragwerksplaner` nicht als konkurrierende Entitätsklassen entstehen.
4. **Kennwerte mit Konfliktlogik versehen**, statt divergierende CO₂-/Mengen-/Flächenwerte zu glätten.
5. **Watchlist und Entfernen/DfD-Anhang trennen**, damit geplante Projekte und reine DfD-Fälle nicht mit gebauten Direct-Reuse-Fällen vermischt werden.

---

## 11. Minimaler Patch für dein Obsidian-System

Falls du nur wenige Dateien ergänzen willst, wären diese 15 Dateien der beste Start:

```text
09_reuse_ketten_herkunft/Donorgebaeude.md
09_reuse_ketten_herkunft/Empfaengergebaeude.md
09_reuse_ketten_herkunft/Donor_Receiver_Kette.md
09_reuse_ketten_herkunft/Materialquelle.md
09_reuse_ketten_herkunft/Urban_Mining_Stream.md
10_status_bewertung_quellenqualitaet/Projektstatus.md
10_status_bewertung_quellenqualitaet/Fallentscheidung.md
10_status_bewertung_quellenqualitaet/Vertrauensgrad.md
10_status_bewertung_quellenqualitaet/Quellenqualitaet.md
10_status_bewertung_quellenqualitaet/Quellenkonflikt.md
11_pruefung_nachweis_zulassung/Reuse_Pruefdossier.md
11_pruefung_nachweis_zulassung/Tragfaehigkeitsnachweis_Bestandsbauteil.md
12_recht_haftung_gewaehrleistung/Bauproduktstatus_Gebrauchtbauteil.md
13_beschaffung_logistik_lagerung/Zwischenlager.md
14_reuse_strategien_spezifisch/Direct_Reuse_vs_Bestandserhalt_Recycling_DfD.md
```

---

## 12. Wichtigste Erkenntnis

Die wichtigste Anpassung ist nicht eine größere Bauteilliste, sondern eine **relationale Logik**:

```text
Donor / Materialquelle → Bauteil → Prüfung → Aufbereitung → Logistik → Empfängergebäude → neue Funktion → Kennwert → Quellenqualität
```

Damit lassen sich Hauptfälle, Vergleichsfälle, Prototypen, Reuse-Ketten und DfD-Anhänge sauberer voneinander trennen.
