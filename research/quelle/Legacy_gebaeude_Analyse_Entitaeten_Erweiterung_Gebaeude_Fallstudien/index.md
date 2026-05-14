---
entity: "quelle"
id: "Legacy_gebaeude_Analyse_Entitaeten_Erweiterung_Gebaeude_Fallstudien"
title: "Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur"
build_status: "promoted_phase42"
node_kind: "source"
legacy_type: ""
---

# Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur

## Legacy Content

# Analyse aller Gebäude-`.md`-Fallstudien und Vorschlag für eine angepasste/erweiterte Entitätenstruktur

**Stand:** 2026-05-06  
**Untersuchte Dateien:** 92 erzeugte Gebäude-`.md`-Dateien im Chat/Arbeitsordner.  
**Nicht als Gebäude-Datei gezählt:** `gebäude4_wiederverwendung_direct_reuse_examples.md` als Prioritäten-/Regeldatei.

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

## 10. Priorisierte nächste Schritte

1. **Bestehende Gebäude-Dateien nicht neu schreiben**, sondern beim nächsten Durchgang nur die Felder `Falltyp`, `Donor-Receiver-Logik`, `Quellenkonflikt` und `Zählt als Direct Reuse?` ergänzen.
2. **Neue Entitätsdateien zuerst für Donor/Receiver, Quellenqualität und Prüfung/Nachweis anlegen**, weil sie die meisten Lücken schließen.
3. **Akteur-Rollen normalisieren**, damit `People`, `Architekt`, `Bauherr`, `Tragwerksplaner` nicht als konkurrierende Entitätsklassen entstehen.
4. **Kennwerte mit Konfliktlogik versehen**, statt divergierende CO₂-/Mengen-/Flächenwerte zu glätten.
5. **Watchlist und Entfernen/DfD-Anhang trennen**, damit geplante Projekte und reine DfD-Fälle nicht mit gebauten Direct-Reuse-Fällen vermischt werden.

## 12. Wichtigste Erkenntnis

Die wichtigste Anpassung ist nicht eine größere Bauteilliste, sondern eine **relationale Logik**:

```text
Donor / Materialquelle → Bauteil → Prüfung → Aufbereitung → Logistik → Empfängergebäude → neue Funktion → Kennwert → Quellenqualität
```

Damit lassen sich Hauptfälle, Vergleichsfälle, Prototypen, Reuse-Ketten und DfD-Anhänge sauberer voneinander trennen.
