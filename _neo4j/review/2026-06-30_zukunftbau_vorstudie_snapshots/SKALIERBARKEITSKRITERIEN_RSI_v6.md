# Skalierbarkeitskriterien — Reuse-Scalability Index (RSI v6)

**Stand:** 2026-07-01  
**Status:** bereinigte Systemfassung für Recherche, Scoring und Datenbankprüfung  
**Zweck:** Der RSI bewertet, ob ein Ansatz der Bauteil-Wiederverwendung über den Einzelfall hinaus als **wiederholbares, planbares, nachweisbares, beschaffbares und marktfähiges System** skalieren kann.

**Ergänzt:** Forschungsanlage [`ANLAGE_Forschungssynthese_Plattform.md`](ANLAGE_Forschungssynthese_Plattform.md) · v3-Methodik (historisch): [`SKALIERBARKEITSKRITERIEN_RSI_v3.md`](SKALIERBARKEITSKRITERIEN_RSI_v3.md)

---

## Inhaltsübersicht

1. Kurzdefinition
2. Was der RSI misst — und was nicht
3. Systemlogik
4. Gate-System: Mindestbedingungen vor Score
5. Score-Formel und Bewertungsskala
6. Gewichtete Kriterien
7. Detailliertes Scoring
8. N/A-Regeln und Bewertungsprofile
9. RSI-Einstufung
10. Konfidenzsystem
11. Schnelltest
12. Archetypen
13. Datenfelder
14. Plausibilitäts- und Korrekturregeln
15. Referenzfälle zur Kalibrierung
16. Verhältnis zu RSI v3/v4/v5
17. Neo4j-Pflichtprüfung
18. Copy-Paste-Prompt für neue Recherche und Scoring
19. Grenzen des Rahmenwerks
20. Wissenschaftliche und fachliche Verankerung
21. Finaler Merksatz

---

## 1. Kurzdefinition

Ein ReUse-Ansatz ist **skalierbar**, wenn er nicht nur in einem einzelnen Projekt funktioniert, sondern als wiederholbare Prozesskette angewendet werden kann:

```text
Bestand erkennen
→ Bauteile inventarisieren
→ Quelle sichern
→ Qualität und Regelkonformität nachweisen
→ Haftung und Risiken klären
→ ReUse ausschreiben und beschaffen
→ demontieren, lagern, aufbereiten
→ wiedereinbauen
→ Wirkung und Daten dokumentieren
→ Prozess wiederholen
```

Skalierbarkeit bedeutet deshalb nicht einfach „hohe ReUse-Quote“ oder „große CO₂-Einsparung“. Skalierbarkeit bedeutet, dass der Ansatz auch für andere Projekte, Orte, Teams oder Bauteilfamilien zuverlässig wiederholbar wird.

**Merksatz:** ReUse wird skalierbar, wenn es vom spektakulären Einzelfall zur belastbaren Infrastruktur wird.

---

## 2. Was der RSI misst — und was nicht

| Misst der RSI | Misst der RSI nicht |
|---|---|
| Wiederholbarkeit und Übertragbarkeit eines ReUse-Ansatzes | Architektonische Qualität allein |
| Reife von Planung, Inventar, Nachweis, Logistik, Haftung und Beschaffung | CO₂-Einsparung als alleinigen Erfolgswert |
| Skalierbarkeit über Projekte, Regionen, Bauteilfamilien oder Marktakteure hinweg | Recyclingquote ohne Element-ReUse |
| Prozessfähigkeit unter realen Bau-, Markt-, Rechts- und Vergabebedingungen | kurzfristige Rentabilität oder absolute Baukosten |
| Fähigkeit, ReUse unabhängig von Einzelpersonen und Zufallsfunden zu wiederholen | symbolische oder rein dekorative Wiederverwendung |

Der RSI ergänzt klassische Zirkularitäts- und Umweltindikatoren. Diese messen oft Materialkreislauf, Zustand oder Wirkung. Der RSI misst dagegen die **Skalierungsfähigkeit des Ansatzes**.

---

## 3. Systemlogik

Der RSI v6 erzeugt vier getrennte Ergebnisse:

| Ergebnis | Funktion |
|---|---|
| **Gate-Status** | Prüft Mindestbedingungen und K.-o.-Risiken. |
| **RSI-Score** | Bewertet den gewichteten Skalierungsreifegrad von 0–100. |
| **Konfidenz** | Bewertet, wie belastbar die Daten und Quellen sind. |
| **Archetyp** | Ordnet die dominante Skalierungslogik ein. |

Diese Trennung ist zwingend. Ein Projekt kann viele Bauteile wiederverwenden oder große CO₂-Einsparungen zeigen und trotzdem nicht skalierbar sein, wenn Inventar, Qualitätsnachweis, Haftung, Logistik oder Beschaffung ungelöst sind.

---

## 4. Gate-System: Mindestbedingungen vor Score

Die Gates werden **vor** dem Score geprüft. Sie verhindern, dass ein Projekt als skalierbar eingestuft wird, obwohl zentrale Systembedingungen fehlen.

### 4.1 Gate-Skala

| Wert | Bedeutung |
|---:|---|
| 0 | fehlt, nicht belegt oder klar ungelöst |
| 1 | adressiert, aber lückenhaft, projektspezifisch oder nicht wiederholbar |
| 2 | belastbar gelöst, dokumentiert oder wiederholbar organisiert |

### 4.2 Die sechs K.-o.-Gates

| Gate | Mindestbedingung | Leitfrage |
|---:|---|---|
| **G1** | Frühe Planungsintegration | Wurde ReUse vor Entwurfsfixierung, Ausschreibung und zentralen Kosten-/Terminentscheidungen berücksichtigt? |
| **G2** | Materialinventar und Quellobjektdaten | Sind Menge, Maße, Zustand, Herkunft, Verfügbarkeit und Ausbauzeitpunkt dokumentiert? |
| **G3** | Qualitäts- und Sicherheitsnachweis | Gibt es einen Prüfpfad für Statik, Brandschutz, Schadstoffe, Akustik, Dauerhaftigkeit oder andere relevante Anforderungen? |
| **G4** | Haftung, Garantie und Versicherung | Ist geklärt, wer für Zustand, Ausbau, Transport, Wiedereinbau und spätere Mängel verantwortlich ist? |
| **G5** | Reverse-Logistik und Zwischenlagerung | Sind Demontage, Kennzeichnung, Transport, Lagerung, Aufbereitung und Wiedereinbau organisatorisch gelöst? |
| **G6** | Beschaffung, Kosten und Terminmodell | Sind ReUse-Leistungen ausschreibbar, vertraglich abbildbar, kalkuliert und terminlich eingeplant? |

### 4.3 Kappungsregeln

| Befund | Konsequenz |
|---|---|
| Alle Gates ≥ 1 | Score wird normal berechnet. |
| Ein Gate = 0 | RSI final wird bei **59** gekappt; maximal **Pilot / Reallabor**. |
| Zwei oder mehr Gates = 0 | RSI final wird bei **39** gekappt; maximal **Einzelfall / Fallstudie**. |
| G3 oder G4 = 0 bei tragenden Bauteilen | RSI final wird bei **39** gekappt, unabhängig vom Bruttoscore. |
| G5 = 0 bei projektübergreifender Wiederverwendung | RSI final wird bei **59** gekappt. |
| Konfidenz < 0,60 | Einstufung bleibt **vorläufig**, auch bei hohem Score. |

**Begründung:** Ohne frühe Planung, Inventar, Prüfpfad, Haftung, Logistik und Beschaffungsmodell kann ReUse nicht zuverlässig wiederholt werden.

---

## 5. Score-Formel und Bewertungsskala

### 5.1 Formel

Jedes Kriterium wird auf einer Rohskala von **0 bis 4** bewertet und anschließend auf **0–100** normiert.

```text
Normierter Kriterienscore = Rohscore × 25

RSI brutto = Σ (Gewichtᵢ × normierter Kriterienscoreᵢ)
             / Σ (anwendbare Gewichteᵢ)

RSI final = RSI brutto nach Anwendung der Gate-Kappungsregeln
```

### 5.2 Allgemeine Rohscore-Skala

| Rohscore | Normiert | Bedeutung |
|---:|---:|---|
| 0 | 0 | fehlt, nicht belegt oder nicht gelöst |
| 1 | 25 | punktuell, experimentell, stark personengebunden |
| 2 | 50 | teilweise gelöst, aber noch projektspezifisch |
| 3 | 75 | robust gelöst und in ähnlichen Fällen wiederholbar |
| 4 | 100 | standardisiert, marktfähig, dokumentiert und breit übertragbar |

### 5.3 Rundung

- Einzelkriterien: Rohscore als ganze Zahl 0–4.
- RSI brutto und final: eine Dezimalstelle.
- Konfidenz: zwei Dezimalstellen.
- Bei unsicherer Quellenlage immer konservativ bewerten.

---

## 6. Gewichtete Kriterien

| Nr. | Kriterium | Gewicht | Kernfrage |
|---:|---|---:|---|
| **K1** | Frühe Planung, Beschaffung und Projektmandat | 9 % | Ist ReUse von Beginn an verbindlich im Projektauftrag, Entwurf, Terminplan und Beschaffungsprozess verankert? |
| **K2** | Versorgung, Quellensicherheit und Reservierbarkeit | 10 % | Gibt es genügend verlässliche, dokumentierte und reservierbare Materialquellen? |
| **K3** | Inventar, Datenqualität und digitale Rückverfolgbarkeit | 10 % | Sind Bauteile rechtzeitig auffindbar, vergleichbar, prüfbar und digital rückverfolgbar? |
| **K4** | Qualität, Prüfung und regulatorische Konformität | 12 % | Sind Sicherheit, Normen, technische Leistungsfähigkeit und behördliche Anschlussfähigkeit nachweisbar? |
| **K5** | Haftung, Garantie, Versicherung und Risikoallokation | 9 % | Sind Verantwortlichkeiten und Risiken rechtlich, vertraglich und versicherungstechnisch geklärt? |
| **K6** | Reverse-Logistik, Zwischenlagerung und Timing | 9 % | Funktioniert die physische Prozesskette von Ausbau bis Wiedereinbau zuverlässig? |
| **K7** | Ausschreibung, Vertragsfähigkeit und Beschaffbarkeit | 7 % | Kann ReUse in Leistungsverzeichnissen, Vergaben, Verträgen und Einkaufsprozessen abgebildet werden? |
| **K8** | Kosten- und Terminrealismus | 7 % | Sind Such-, Prüf-, Planungs-, Lager-, Transport- und Koordinationsaufwände realistisch eingeplant? |
| **K9** | Zirkuläres Design, Anpassungsfähigkeit und DfD | 8 % | Kann der Entwurf mit verfügbaren Bauteilen umgehen und spätere Demontage ermöglichen? |
| **K10** | Wiederverwendungstiefe, Scope und Bauteilumfang | 6 % | Wie substanziell ist der tatsächliche Element-ReUse, und ist der Scope sauber abgegrenzt? |
| **K11** | Akteurskompetenz, Rollen und Prozessfähigkeit | 5 % | Können normale Projektakteur:innen den Prozess anwenden, oder hängt er an Einzelpersonen? |
| **K12** | Markt-, Netzwerk-, Politik- und Nachfrageunterstützung | 4 % | Gibt es Plattformen, Hubs, Zielquoten, Förderungen, CO₂-Grenzwerte oder institutionelle Nachfrage? |
| **K13** | Replizierbarkeit und Champion-Unabhängigkeit | 3 % | Funktioniert der Ansatz ohne dieselbe außergewöhnliche Bauherrschaft, Architekt:in oder Materialquelle? |
| **K14** | Umwelt- und Ressourcenwirkungsnachweis | 1 % | Ist die ökologische Wirkung nach Transport, Aufbereitung und Wiedereinbau belegt? |
|  | **Summe** | **100 %** |  |

**Hinweis zu K14:** Umweltwirkung ist ein Pflichtnachweis für Legitimation, Förderung und Nachfrage. Sie erhält im RSI aber nur ein geringes Gewicht, weil der RSI Skalierbarkeit misst, nicht Umweltwirkung als solche. Eine hohe CO₂-Einsparung ersetzt keine Nachweise zu Inventar, Qualität, Haftung, Logistik oder Beschaffung.

---

## 7. Detailliertes Scoring

### K1 — Frühe Planung, Beschaffung und Projektmandat · 9 %

**Leitfrage:** Ist ReUse früh genug verankert, damit Entwurf, Quellen, Kosten, Termine und Verträge darauf reagieren können?

| Score | Bewertung |
|---:|---|
| 0 | ReUse wird nachträglich oder nur dekorativ ergänzt. |
| 1 | ReUse wird erwähnt, aber ohne verbindliche Ziele oder Beschaffungspfad. |
| 2 | ReUse ist in der Konzeptphase vorgesehen, aber noch nicht mit Quellen, Ausschreibung oder Terminplan verbunden. |
| 3 | ReUse ist in Vorstudie, Wettbewerb, Projektpflichtenheft, SIA-Frühphase oder Ausschreibung integriert. |
| 4 | ReUse ist verbindlicher Bestandteil des Projektmandats inklusive Zielquoten, Suchfenstern, Inventar-, Nachweis-, Vergabe- und Entscheidungsregeln. |

**Nachweise:** Projektauftrag, Wettbewerbsprogramm, ReUse-Strategie, Pflichtenheft, Ausschreibung, Beschaffungsplan, Terminplan.

### K2 — Versorgung, Quellensicherheit und Reservierbarkeit · 10 %

**Leitfrage:** Gibt es eine Materialpipeline statt einer einmaligen Bauteiljagd?

| Score | Bewertung |
|---:|---|
| 0 | Quellen unbekannt oder rein opportunistisch. |
| 1 | Eine Quelle ist bekannt, aber nicht gesichert. |
| 2 | Eine oder wenige Quellen sind gesichert; starke Einzelfallabhängigkeit. |
| 3 | Mehrere Quellen, Materialdepots, Hubs oder Beschaffungswege sind dokumentiert und teilweise reservierbar. |
| 4 | Portfolio- oder Aggregator-Logik mit mehreren Spenderobjekten, wiederkehrenden Lieferkanälen, Alternativquellen und Reservierungsmechanismus. |

**Mindestdaten:** Anzahl Spenderobjekte, Bauteilfamilien, Mengen, Entfernung, Verfügbarkeit, Reservierungsstatus, Eigentumsübergang, Alternativquellen.

**Aggregator-Schwelle:** Ab **≥ 5 distinkten Spenderquellen** kann von Aggregator- oder Portfolio-Logik gesprochen werden, wenn Inventar, Logistik und Nachweisprozesse ebenfalls belastbar sind.

### K3 — Inventar, Datenqualität und digitale Rückverfolgbarkeit · 10 %

**Leitfrage:** Können Planende, Prüfende, Einkauf und Ausführung die Bauteile rechtzeitig finden, beurteilen, reservieren und dokumentieren?

| Score | Bewertung |
|---:|---|
| 0 | Keine belastbaren Bauteildaten. |
| 1 | Fotos oder Listen vorhanden, aber ohne vollständige Maße, Mengen, Zustand oder Verfügbarkeit. |
| 2 | Inventar mit Grunddaten vorhanden; technische Daten, Zustand oder Zeitfenster bleiben lückenhaft. |
| 3 | Bauteile sind mit IDs, Maßen, Mengen, Zustand, Lage, Ausbauzeitpunkt, Fotos und Verfügbarkeit dokumentiert. |
| 4 | Digitales, interoperables Inventar mit Prüfstatus, BIM-/LCA-Anschluss, Reservierungslogik, Eigentumsstatus und Rückverfolgbarkeit bis zum Wiedereinbau. |

**Kernfelder:** Bauteil-ID, Kategorie, Material, Maße, Menge, Standort, Zustand, Verbindungstyp, Schadstoffhinweise, Ausbauaufwand, Verfügbarkeit, Eigentümer:in, Prüfstatus, Zielobjekt.

### K4 — Qualität, Prüfung und regulatorische Konformität · 12 %

**Leitfrage:** Können wiederverwendete Bauteile die relevanten technischen, rechtlichen und sicherheitsbezogenen Anforderungen erfüllen?

| Score | Bewertung |
|---:|---|
| 0 | Keine technische Prüfung oder Normenklärung. |
| 1 | Sichtprüfung oder Erfahrungswissen, aber kein belastbarer Prüfpfad. |
| 2 | Einzelne Anforderungen geprüft; relevante Lücken bleiben. |
| 3 | Prüfpfad für alle relevanten Risiken ist definiert und projektbezogen angewandt. |
| 4 | Standardisierte Prüf- und Freigabeprozesse mit Zustandsklassen, Dokumentation, behördlicher Anschlussfähigkeit und wiederverwendbaren Nachweisformaten. |

**Prüfbereiche:** Statik, Brandschutz, Akustik, Schadstoffe, Feuchtigkeit, Dauerhaftigkeit, Energie, Hygiene, Korrosion, Oberflächen, Verbindungsmittel, CE-/Normenfragen, Bauteilalterung.

**Strenge Regel:** Bei tragenden Bauteilen ist Score 3 erst möglich, wenn statische Leistungsfähigkeit, Zustand und Wiederverwendungsbedingungen nachvollziehbar geprüft sind.

### K5 — Haftung, Garantie, Versicherung und Risikoallokation · 9 %

**Leitfrage:** Ist geklärt, wer Verantwortung trägt, wenn beim Ausbau, Transport, Wiedereinbau oder Betrieb ein Problem auftritt?

| Score | Bewertung |
|---:|---|
| 0 | Haftung, Garantie und Versicherung ungeklärt. |
| 1 | Risiken werden informell oder individuell getragen. |
| 2 | Verantwortlichkeiten sind teilweise vertraglich geregelt. |
| 3 | Haftung, Gewährleistung, Prüfpflichten, Abnahme und Versicherbarkeit sind projektbezogen geklärt. |
| 4 | Musterverträge, Standardklauseln, Versicherungsoptionen, Zustandsklassen und Verantwortungsmatrix sind wiederverwendbar. |

**Nachweise:** Verantwortungsmatrix, Mustervertrag, Gewährleistungsklauseln, Versicherungsmodell, Prüfprotokolle, Abnahmeprotokolle, Risikoanalyse.

### K6 — Reverse-Logistik, Zwischenlagerung und Timing · 9 %

**Leitfrage:** Funktioniert die physische Kette zwischen Rückbau und Neubau?

| Score | Bewertung |
|---:|---|
| 0 | Keine organisierte Demontage-, Lager- oder Transportlösung. |
| 1 | Ad-hoc-Logistik mit hohem manuellem Koordinationsaufwand. |
| 2 | Einzelne Schritte sind organisiert, aber Timing, Zwischenlager oder Aufbereitung bleiben riskant. |
| 3 | Demontage, Kennzeichnung, Transport, Lagerung, Aufbereitung und Lieferung sind geplant und koordiniert. |
| 4 | Professionelle, wiederholbare Reverse-Logistik mit Hub, Etikettierung, Übergabeprozessen, Qualitätskontrolle und Terminpuffern. |

**Kernfrage:** Passen Rückbauzeitpunkt, Prüfzeitpunkt, Lagerdauer, Aufbereitung und Einbautermin zusammen?

### K7 — Ausschreibung, Vertragsfähigkeit und Beschaffbarkeit · 7 %

**Leitfrage:** Kann ReUse in normalen Planungs-, Vergabe- und Einkaufsprozessen umgesetzt werden?

| Score | Bewertung |
|---:|---|
| 0 | ReUse ist nicht ausschreibbar oder vertraglich nicht abgebildet. |
| 1 | ReUse wird informell oder über Sonderabsprachen beschafft. |
| 2 | Einzelne ReUse-Leistungen sind in Ausschreibung oder Vertrag enthalten, aber mit Lücken. |
| 3 | ReUse ist in Leistungsverzeichnissen, Vergabekriterien, Spezifikationen und Leistungsbildern projektbezogen verankert. |
| 4 | Standardisierte Ausschreibungsbausteine, Vertragsmodelle, Beschaffungswege und Bewertungsmethoden sind wiederverwendbar. |

**Nachweise:** LV-Positionen, Vergabekriterien, Vertragsklauseln, Leistungsbilder, Beschaffungsstrategie, Materialreservierung, Substitutionsregeln.

### K8 — Kosten- und Terminrealismus · 7 %

**Leitfrage:** Ist der zusätzliche Aufwand realistisch eingepreist und eingeplant?

| Score | Bewertung |
|---:|---|
| 0 | Kosten und Zeit für ReUse fehlen vollständig. |
| 1 | ReUse wird als „günstiges Material“ betrachtet; Prozesskosten fehlen. |
| 2 | Mehrkosten und Terminrisiken sind grob erkannt. |
| 3 | Such-, Prüf-, Planungs-, Lager-, Transport-, Anpassungs- und Koordinationsaufwand sind budgetiert. |
| 4 | ReUse ist im Kostenmodell, Terminplan, Risikopuffer und Entscheidungsprozess standardisiert abgebildet. |

**Zu prüfen:** Machbarkeitsstudien, Inventarisierung, Suchaufwand, Ausbau, Transport, Lagerung, Prüfung, Reinigung, Anpassung, Projektverlängerung, Versicherungen, Koordination.

### K9 — Zirkuläres Design, Anpassungsfähigkeit und DfD · 8 %

**Leitfrage:** Kann das Projekt mit verfügbaren Bauteilen entwerfen und spätere Wiederverwendung ermöglichen?

| Score | Bewertung |
|---:|---|
| 0 | Konventioneller Entwurf; ReUse nur als nachträgliche Substitution. |
| 1 | Einzelne gebrauchte Bauteile werden integriert. |
| 2 | Entwurf reagiert auf verfügbare Bauteile, aber mit hohem Sonderaufwand. |
| 3 | Modulare, trockene, reversible oder demontierbare Bauweise ist erkennbar. |
| 4 | Systematisches Design for Disassembly mit reversiblen Verbindungen, zugänglichen Schichten, Austauschbarkeit, Standardisierung und geringer Beschädigung beim Rückbau. |

**Bezugspunkte:** Durmisevic, DGBC/Alba-Concepts Disassembly Potential, Brand Shearing Layers, ISO 20887, EPFL / Brütting-Fivet-Senatore (*form follows availability*).

### K10 — Wiederverwendungstiefe, Scope und Bauteilumfang · 6 %

**Leitfrage:** Wie substanziell ist der tatsächliche Element-ReUse, und worauf bezieht sich die Quote?

| Score | Bewertung |
|---:|---|
| 0 | Keine Element-Wiederverwendung oder nur Recycling. |
| 1 | Einzelne sichtbare oder nicht kritische Elemente. |
| 2 | Mehrere nicht tragende Bauteilgruppen oder ein einzelnes Gewerk. |
| 3 | Substanzieller ReUse über mehrere Bauteilgruppen, Schichten oder Gewerke. |
| 4 | Hohe ReUse-Tiefe auf Gebäude-, Struktur- oder Systemebene mit klarer Scope-Angabe und nachvollziehbarer Berechnung. |

**Pflicht:** Jede ReUse-Quote braucht einen Scope.

| Scope | Bedeutung |
|---|---|
| `whole_building` | bezogen auf Gesamtgebäude |
| `structural` | bezogen auf tragende Bauteile |
| `facade` | bezogen auf Gebäudehülle |
| `single_trade` | bezogen auf ein Gewerk, z. B. Stahl, Türen, Leuchten |
| `interior_fitout` | bezogen auf Ausbau / Innenausbau |
| `temporary_borrowed` | geliehen oder temporär genutzt |
| `platform_volume` | bezogen auf Transaktionsvolumen eines Hubs oder Marktplatzes |
| `unknown` | nicht vergleichbar; konservativ bewerten |

**Abgrenzung:** 97 % Stahl-ReUse ist nicht 97 % Gebäude-ReUse. Recyclingbeton ist kein Bauteil-ReUse.

### K11 — Akteurskompetenz, Rollen und Prozessfähigkeit · 5 %

**Leitfrage:** Können die beteiligten Akteur:innen ReUse praktisch umsetzen?

| Score | Bewertung |
|---:|---|
| 0 | Keine nachweisbare ReUse-Kompetenz. |
| 1 | Kompetenz liegt bei Einzelpersonen. |
| 2 | Mehrere Akteur:innen haben Erfahrung, aber kein standardisierter Prozess. |
| 3 | Rollen, Schnittstellen, Verantwortlichkeiten und Kompetenzen sind klar verteilt. |
| 4 | Wiederholbare Prozesskette mit geschulten Planenden, Rückbauunternehmen, Prüfstellen, Logistik, Beschaffung, Behördenkontakt und Ausführung. |

**Akteursgruppen:** Bauherrschaft, Architekt:innen, Ingenieur:innen, Rückbauunternehmen, Lieferant:innen, Materialhubs, Behörden, Versicherer, Bauunternehmen, Betreiber:innen, digitale Plattformen.

### K12 — Markt-, Netzwerk-, Politik- und Nachfrageunterstützung · 4 %

**Leitfrage:** Wird ReUse durch Nachfrage, Regulierung oder Marktinfrastruktur getragen?

| Score | Bewertung |
|---:|---|
| 0 | Keine erkennbare Nachfrage oder politische Unterstützung. |
| 1 | Einzelne motivierte Bauherrschaft oder Pilotförderung. |
| 2 | Lokale Netzwerke, Plattformen oder Förderinstrumente vorhanden. |
| 3 | ReUse ist in Beschaffungskriterien, Zielquoten, CO₂-Grenzwerten, Programmen oder Netzwerken verankert. |
| 4 | Stabile Marktinfrastruktur mit Nachfrage, Standards, Förderlogik, Plattformen, Hubs und institutioneller Unterstützung. |

**Infrastrukturbeispiele:** Bauteilbörsen, Materialhubs, digitale Inventare, Cirkla-ähnliche Netzwerke, öffentliche Beschaffung, Förderprogramme, CO₂-Anforderungen, Branchenstandards.

### K13 — Replizierbarkeit und Champion-Unabhängigkeit · 3 %

**Leitfrage:** Funktioniert der Ansatz auch ohne dieselbe außergewöhnliche Bauherrschaft, Architekt:in, Materialquelle oder Förderkonstellation?

| Score | Bewertung |
|---:|---|
| 0 | Vollständig abhängig von Sonderfall, Einzelperson oder einmaliger Quelle. |
| 1 | Übertragbarkeit behauptet, aber nicht belegt. |
| 2 | Teile des Ansatzes sind in ähnlichen Projekten übertragbar. |
| 3 | Prozess, Werkzeuge oder Details sind dokumentiert und für ähnliche Kontexte wiederholbar. |
| 4 | Ansatz wurde mehrfach angewandt oder ist als System, Plattform, Regelwerk oder Geschäftsmodell unabhängig vom Einzelfall nutzbar. |

**Prüffrage:** Könnte ein anderes kompetentes Projektteam den Ansatz mit vertretbarem Aufwand wiederholen?

### K14 — Umwelt- und Ressourcenwirkungsnachweis · 1 %

**Leitfrage:** Ist die ökologische Wirkung belastbar belegt?

| Score | Bewertung |
|---:|---|
| 0 | Keine Umweltangaben. |
| 1 | Plausible qualitative Aussage. |
| 2 | Grobe CO₂- oder Ressourcenschätzung. |
| 3 | Projektbezogene LCA oder nachvollziehbare CO₂-Bilanz. |
| 4 | Vergleichende LCA mit Transport, Aufbereitung, Substitutionseffekt, Lebensdauer, Systemgrenzen und Sensitivitäten. |

**Hinweis:** Umweltwirkung stützt Legitimation und Nachfrage. Sie ersetzt aber nicht Inventar, Qualität, Haftung, Logistik oder Beschaffbarkeit.

---

## 8. N/A-Regeln und Bewertungsprofile

### 8.1 N/A-Regel

Ein Kriterium darf nur als **nicht anwendbar** markiert werden, wenn es für den bewerteten Ansatz sachlich nicht relevant ist.

N/A darf nicht verwendet werden, um fehlende Informationen zu kaschieren. Fehlende Information ist **Score 0 oder 1 mit niedriger Evidenz**, nicht N/A.

**Strenge Regeln:**

- Bei tragendem ReUse dürfen **K4 Qualität** und **K5 Haftung** nie N/A sein.
- Bei projektübergreifendem ReUse darf **K6 Logistik** nie N/A sein.
- Bei Gebäudebewertungen darf **K10 Scope** nie N/A sein.
- Wenn mehr als 25 % der Gewichte N/A sind, muss die Bewertung ausdrücklich als **Profilbewertung** markiert werden.

### 8.2 Bewertungsprofile

| Profil | Typische Anwendung | Besondere Bewertungslogik |
|---|---|---|
| `whole_building_project` | Gebäude mit mehreren ReUse-Bauteilgruppen | alle Kriterien relevant; Scope besonders prüfen |
| `interior_fitout_reuse` | Türen, Möbel, Leuchten, Ausbau, Sanitär | meist geringere regulatorische Hürde; Logistik, Beschaffung und Marktinterface zentral |
| `structural_reuse` | Stahl, Beton, tragende Elemente | Qualität, Haftung und Genehmigung streng; G3/G4 nie N/A |
| `material_hub_platform` | Rotor-DC-ähnlicher Hub oder Händler | Gebäudequote nicht zentral; Versorgung, Inventar, Logistik, Markt und Beschaffung zentral |
| `network_ecosystem` | Cirkla-ähnliches Netzwerk | ReUse-Tiefe einzelner Gebäude N/A; Wirkung über Infrastruktur, Standards und Akteurskoordination |
| `digital_inventory_tool` | Inventar-, Matching- oder Materialpass-System | Datenqualität, Interoperabilität, Reservierung und Beschaffungsanschluss zentral |
| `temporary_or_exhibition` | temporäre Pavillons, Ausstellungen | DfD und Rückbau stark; langfristige Marktübertragbarkeit kritisch prüfen |

---

## 9. RSI-Einstufung

| RSI final | Einstufung | Interpretation |
|---:|---|---|
| 0–39 | **Einzelfall / Fallstudie** | ReUse ist sichtbar, aber zentrale Skalierungsbedingungen fehlen. |
| 40–59 | **Pilot / Reallabor** | Hoher Lernwert; noch nicht robust wiederholbar. |
| 60–74 | **bedingt skalierbar** | In ähnlichen Kontexten wiederholbar, aber mit Systemlücken. |
| 75–89 | **skalierbar** | Prozess, Nachweise, Logistik, Beschaffung und Akteursrollen sind weitgehend robust. |
| 90–100 | **systemisch skalierbar** | ReUse funktioniert als Infrastruktur, Plattform, Beschaffungsmodell oder breit übertragbares Verfahren. |

**Wichtig:** Die Einstufung gilt nur zusammen mit Gate-Status, Konfidenz und Archetyp.

---

## 10. Konfidenzsystem

### 10.1 Evidenzqualität pro Kriterium

Jedes Kriterium erhält zusätzlich einen Evidenzwert.

| Evidenzwert | Bedeutung |
|---:|---|
| 0 | keine Quelle / reine Annahme |
| 1 | Presse, Website, Selbstdarstellung oder Sekundärquelle |
| 2 | Projektunterlagen, Inventar, Ausschreibung, LCA, Plan, Prüfbericht oder Fachquelle |
| 3 | Primärquelle plus externe Verifikation oder mehrere unabhängige belastbare Quellen |

### 10.2 Konfidenzformel

```text
Konfidenz = Σ (Gewichtᵢ × Evidenzwertᵢ / 3)
            / Σ (anwendbare Gewichteᵢ)
```

### 10.3 Konfidenzklassen

| Konfidenz | Klasse | Bedeutung |
|---:|---|---|
| < 0,60 | **C** | Vorläufig; keine belastbare Skalierbarkeitsaussage. |
| 0,60–0,79 | **B** | Brauchbar, aber mit relevanten Lücken. |
| ≥ 0,80 | **A** | Belastbar und vergleichsfähig. |

**Regel:** Ein Projekt mit Konfidenz C darf nicht ohne Zusatz **„vorläufig“** als skalierbar bezeichnet werden.

---

## 11. Schnelltest

Ein Ansatz ist nur dann realistisch skalierbar, wenn die meisten Antworten **ja** sind:

1. Wurde ReUse früh genug in Planung, Wettbewerb oder Projektauftrag integriert?
2. Gibt es gesicherte und mengenmäßig ausreichende Materialquellen?
3. Sind Bauteile mit Maßen, Zustand, Verfügbarkeit und Herkunft inventarisiert?
4. Gibt es einen Prüfpfad für technische und regulatorische Anforderungen?
5. Sind Haftung, Garantie, Versicherung und Risikoallokation geklärt?
6. Funktionieren Demontage, Transport, Lagerung, Aufbereitung und Wiedereinbau?
7. Ist ReUse ausschreibbar, vertraglich abbildbar und beschaffbar?
8. Sind Zusatzkosten, Suchaufwand, Prüfaufwand und Terminrisiken eingeplant?
9. Kann der Entwurf mit verfügbaren Bauteilen umgehen, ohne jedes Detail neu zu erfinden?
10. Ist klar, ob die ReUse-Quote für Gebäude, Struktur, Fassade, Gewerk oder Innenausbau gilt?
11. Können mehrere Akteur:innen den Prozess anwenden, oder hängt er an Einzelpersonen?
12. Gibt es Marktkanäle, Hubs, Netzwerke, Förderungen, Zielquoten oder politische Nachfrage?

**Faustregel:**

- 0–2 Nein-Antworten: Detailbewertung durchführen; Skalierung möglich.
- 3–5 Nein-Antworten: wahrscheinlich Pilotstatus.
- 6 oder mehr Nein-Antworten: wahrscheinlich Einzelfall, Fallstudie oder Reallabor.

---

## 12. Archetypen

Archetypen ordnen Projekte nach ihrer **Skalierungslogik**, nicht nach Architekturpreis oder CO₂-Einsparung.

| Priorität | Archetyp | Regel | Skalierungsbedeutung |
|---:|---|---|---|
| 1 | **Systemischer Aggregator** | K2 ≥ 3, K3 ≥ 3, K6 ≥ 3, K12 ≥ 3, K13 ≥ 3 | ReUse wird Infrastruktur und nicht nur Projektleistung. |
| 2 | **Professioneller ReUse-Hub / Plattform** | Materialfluss, Katalog, Lager, Reservierung, Verkauf oder Vermittlung belegt | Skaliert Versorgung, Sichtbarkeit, Beschaffung und Verfügbarkeit. |
| 3 | **Regulatorisch reifer Struktur-ReUse** | tragende Bauteile + K4 ≥ 3 + K5 ≥ 3 + K6 ≥ 3 | Hohes systemisches Potenzial bei hoher technischer Hürde. |
| 4 | **DfD-Systemreferenz** | K9 = 4 oder sehr stark belegte reversible Bauweise | Stark als Entwurfsmodell; nur skalierbar, wenn Versorgung und Nachweis mitziehen. |
| 5 | **Großmaßstab-Demonstrator** | ≥ 5.000 m² und substanzieller ReUse oder LCA-Nachweis | Belegt Machbarkeit jenseits des Reallabors. |
| 6 | **Tiefen-Pilot** | sehr hohe ReUse-Tiefe, aber wenige Quellen oder starker Sonderprozess | Zeigt maximale ReUse-Tiefe; nicht automatisch übertragbar. |
| 7 | **Innenausbau-/Finish-ReUse** | Türen, Leuchten, Böden, Möbel, Sanitär, Ausbau | Oft leichter skalierbar wegen geringerer regulatorischer Risiken. |
| 8 | **Netzwerk-/Ökosystem-Enabler** | Akteurskoordination, Standards, Wissen, Tools oder Marktstimulation | Skaliert Rahmenbedingungen statt einzelner Bauteile. |
| 9 | **Klein-Pilot / Reallabor** | Kleinmaßstab, temporär oder viele Gates offen | Hoher Lernwert, begrenzte Übertragbarkeit. |
| 10 | **Fallstudie** | dünn dokumentiert oder zentrale Kriterien offen | Aussagekraft begrenzt. |

---

## 13. Datenfelder

| Feldgruppe | Mindestfelder |
|---|---|
| Projekt | Name, Ort, Jahr, Nutzung, Neubau/Umbau, Fläche, temporär/permanent, Bewertungsprofil |
| ReUse-Ziel | ReUse-Strategie, Zielquote, Bauteilfamilien, Scope, Projektmandat |
| Quellen | Anzahl Spenderobjekte, Art der Quelle, Reservierungsstatus, Entfernung, Eigentum, Alternativquellen |
| Inventar | Bauteil-ID, Maße, Menge, Zustand, Fotos, Verbindung, Schadstoffe, Verfügbarkeit, Prüfstatus |
| Qualität | Prüfungen, Normen, Zustandsklassen, Zertifikate, behördliche Freigaben, Restlebensdauer |
| Risiko | Haftung, Gewährleistung, Versicherung, Verantwortungsmatrix, Abnahmeprozess |
| Logistik | Ausbau, Kennzeichnung, Transport, Lager, Aufbereitung, Wiedereinbau, Timing, Puffer |
| Beschaffung | Ausschreibung, Vertrag, Leistungsbild, Vergabekriterium, Beschaffungsweg, Substitutionsregeln |
| Kosten/Zeit | Zusatzplanung, Suche, Prüfung, Lagerung, Transport, Anpassung, Terminpuffer, Risikoaufschläge |
| Design | reversible Verbindungen, Demontagezugänglichkeit, Schichtentrennung, Adaptivität, Standardisierung |
| Akteure | Rollen, Kompetenzen, Schnittstellen, Wiederholungserfahrung, Schulungen |
| Markt/Politik | Plattformen, Hubs, Netzwerke, Förderungen, Zielquoten, CO₂-Grenzwerte, öffentliche Nachfrage |
| Wirkung | CO₂, Ressourcen, Abfallvermeidung, LCA-Grenzen, Vergleichsfall, Transport, Aufbereitung |
| Evidenz | Primärquellen, Projektberichte, Pläne, LCA, Inventare, externe Verifikation, Datenqualität |
| Neo4j | Projektknoten, Bauteilknoten, Quellenknoten, Evidenzknoten, Scoreknoten, Gateknoten, Beziehungen und Zeitstempel |

---

## 14. Plausibilitäts- und Korrekturregeln

| Problem | Korrekturregel |
|---|---|
| ReUse-Quote ohne Scope | Nicht mit Gebäude-ReUse gleichsetzen; konservativ bewerten. |
| Biosourced, Recycling und Element-ReUse vermischt | Element-ReUse separat ausweisen; Recycling nicht als ReUse zählen. |
| Design-Behauptung ohne Rückbau-Nachweis | K9 maximal Score 2. |
| CO₂-Wert ohne Systemgrenze | K14 maximal Score 2. |
| Nur Presse- oder Marketingquelle | Evidenzwert maximal 1; Konfidenz reduzieren. |
| Einmalige Sonderlösung | K2, K8, K11 und K13 abwerten. |
| Einzelne Expert:in als Haupttreiber | K11 und K13 abwerten. |
| Spenderquelle nicht gesichert | K2 maximal Score 2. |
| Haftung ungeklärt | Gate-Kappung anwenden; bei tragenden Bauteilen maximal Einzelfall/Fallstudie. |
| Fehlende Lagerlösung | K6 maximal Score 1; bei projektübergreifendem ReUse Gate-Kappung prüfen. |
| Plattform ohne Transaktions- oder Reservierungsfunktion | K3 und K12 nicht automatisch hoch bewerten. |
| Hohe CO₂-Einsparung, aber schlechte Prozessreife | K14 nicht als Ersatz für Skalierung verwenden. |
| Neo4j widerspricht Quellen | Nicht finalisieren; Diskrepanzliste erstellen und Daten korrigieren. |
| Neo4j enthält Score ohne Evidenzlink | Score als nicht verifiziert markieren; Evidenzwert maximal 1. |

---

## 15. Referenzfälle zur Kalibrierung

Diese Einordnung dient der Kalibrierung. Sie ersetzt keine vollständige Punktbewertung.

### 15.1 Rotor DC

**Profil:** `material_hub_platform`  
**Stärken:** Versorgung, Inventar, Reverse-Logistik, Lager, Marktinterface, Katalog, Wiederholbarkeit.  
**Grenze:** Besonders stark bei Innenausbau, Finish und nicht tragenden Komponenten; tragende Bauteile benötigen zusätzliche Prüf-, Normen- und Haftungslogik.  
**Archetyp:** Professioneller ReUse-Hub / Plattform; potenziell systemischer Aggregator.

### 15.2 Cirkla

**Profil:** `network_ecosystem`  
**Stärken:** Netzwerk, Wissensinfrastruktur, Marktstimulation, Sichtbarkeit, Werkzeuge, Akteurskoordination.  
**Grenze:** Kein einzelnes Bauprojekt; Qualität, Haftung und Logistik müssen auf Projekt- oder Bauteilebene zusätzlich gelöst werden.  
**Archetyp:** Netzwerk-/Ökosystem-Enabler.

### 15.3 Halle 118 / baubüro in situ

**Profil:** `whole_building_project`  
**Stärken:** frühe Planung, Entwerfen mit Verfügbarkeit, mehrere Bauteilgruppen, ökologische Beweiskraft, hoher Demonstrationswert.  
**Grenze:** Hoher Know-how- und Koordinationsbedarf; Skalierung hängt von Inventaren, Beschaffung, Nachweisprozessen, Haftung und Logistik ab.  
**Archetyp:** Großmaßstab-Demonstrator und Design-/Prozessreferenz.

### 15.4 Abbau Aufbau

**Profil:** `structural_reuse`  
**Stärken:** adressiert tragende Stahlbetonbauteile mit hohem Ressourcen- und CO₂-Potenzial; entwickelt digitale Inventar- und Schnittlogik.  
**Grenze:** Skalierung hängt stark von Geometrie, Statik, Genehmigung, Prüfpfad, Transport, Haftung und standardisierten Details ab.  
**Archetyp:** Struktureller ReUse-Pilot mit hohem Skalierungspotenzial für geeignete Gebäudetypologien.

---

## 16. Verhältnis zu RSI v3/v4/v5

### 16.1 Ausgangspunkt aus RSI v3

RSI v3 enthielt sechs Hauptdimensionen:

1. Bezug & Reverse-Logistik
2. Wiederverwendungstiefe & -umfang
3. Maßstab
4. Zirkuläres Design / Transformationskapazität
5. Informationsreife & Nachweis
6. Umweltwirkungs-Nachweis

Diese Logik bleibt in RSI v6 erkennbar, wird aber in praktischere Skalierungsbedingungen aufgelöst.

### 16.2 Ergänzungen in RSI v6

RSI v6 ergänzt und schärft:

- Gate-System mit Kappungsregeln,
- frühe Planungsintegration,
- Beschaffungs- und Vertragsfähigkeit,
- Qualitäts- und regulatorische Nachweise,
- Haftung, Garantie und Versicherung,
- Zwischenlagerung und Reverse-Logistik,
- Kosten- und Terminrealismus,
- Akteurskompetenz,
- Markt- und Politikunterstützung,
- Replizierbarkeit und Champion-Unabhängigkeit,
- Konfidenzsystem,
- Bewertungsprofile,
- verpflichtende Neo4j-Graphprüfung.

### 16.3 Vergleichbarkeit

Alte RSI-v3-, RSI-v4- oder RSI-v5-Werte bleiben als historische Vergleichswerte nutzbar, sind aber **nicht direkt** mit RSI-v6-Scores vergleichbar. Für Vergleichsstudien müssen alle Projekte mit derselben Version neu recherchiert und neu bewertet werden.

---

## 17. Neo4j-Pflichtprüfung

Die Neo4j-Graphdatenbank ist nicht nur ein Ablageort, sondern ein Prüfwerkzeug. Jede neue RSI-Bewertung muss gegen den Graphen geprüft werden.

### 17.1 Grundregel

**Keine finale RSI-Bewertung ohne Neo4j-Double-Check.**

Vor jeder finalen Bewertung müssen folgende drei Ebenen abgeglichen werden:

```text
Quellenrecherche ↔ extrahierte Datentabelle ↔ Neo4j-Graph ↔ RSI-Berechnung
```

Wenn eine Aussage in der Recherche, in der Datentabelle und im Graph widersprüchlich ist, wird sie nicht final gewertet, bevor die Diskrepanz dokumentiert oder korrigiert wurde.

### 17.2 Pflichtprüfungen im Graph

| Prüfung | Zweck |
|---|---|
| Projektknoten eindeutig vorhanden | Dubletten und Namensvarianten erkennen. |
| Bewertungsprofil gespeichert | Verhindert falsche N/A-Logik. |
| Gates gespeichert und mit Evidenz verknüpft | Kappungsregeln korrekt anwenden. |
| Alle K1–K14-Scores gespeichert | Vollständigkeit des Scorings prüfen. |
| Jeder Score hat mindestens eine Evidenzbeziehung | Keine unbelegte Punktvergabe. |
| Bauteile, Quellen und Spenderobjekte sind verbunden | Materialfluss und Quellensicherheit prüfen. |
| Inventar- und Logistikdaten sind zeitlich plausibel | Rückbau, Lagerung und Einbau abgleichen. |
| ReUse-Quote hat Scope | Verzerrung durch Einzelgewerk-Quoten vermeiden. |
| LCA- oder CO₂-Werte haben Systemgrenzen | Umweltwirkung nicht überbewerten. |
| Berechneter RSI im Graph entspricht externer Kontrollrechnung | Rechenfehler und alte Versionen erkennen. |

### 17.3 Empfohlene Graph-Struktur

Die konkrete Neo4j-Schema-Bezeichnung kann abweichen. Inhaltlich sollten mindestens diese Objekte abbildbar sein:

```text
(:Project)
(:ReuseComponent)
(:DonorSource)
(:MaterialHub)
(:Actor)
(:Evidence)
(:RSIAssessment {version: "v6"})
(:RSICriterionScore)
(:RSIGate)
(:ImpactClaim)
(:ProcurementDocument)
(:LogisticsStep)
```

Empfohlene Beziehungen:

```text
(Project)-[:HAS_ASSESSMENT]->(RSIAssessment)
(RSIAssessment)-[:HAS_SCORE]->(RSICriterionScore)
(RSIAssessment)-[:HAS_GATE]->(RSIGate)
(RSICriterionScore)-[:SUPPORTED_BY]->(Evidence)
(RSIGate)-[:SUPPORTED_BY]->(Evidence)
(Project)-[:USES_COMPONENT]->(ReuseComponent)
(ReuseComponent)-[:ORIGINATES_FROM]->(DonorSource)
(Project)-[:INVOLVES_ACTOR]->(Actor)
(Project)-[:USES_HUB_OR_PLATFORM]->(MaterialHub)
(Project)-[:HAS_IMPACT_CLAIM]->(ImpactClaim)
(Project)-[:USES_PROCUREMENT_DOCUMENT]->(ProcurementDocument)
(Project)-[:HAS_LOGISTICS_STEP]->(LogisticsStep)
```

### 17.4 Schema-agnostische Cypher-Prüfungen

Die folgenden Abfragen sind bewusst allgemein gehalten. Label und Property-Namen können an das tatsächliche Schema angepasst werden.

**1. Projekt und mögliche Dubletten finden**

```cypher
MATCH (p)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
RETURN labels(p) AS labels, p
LIMIT 25;
```

**2. RSI-v6-Bewertung finden**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
RETURN p.name AS project, a.version AS version, a.rsi_brutto AS brutto,
       a.rsi_final AS final, a.confidence AS confidence,
       a.profile AS profile, a.archetype AS archetype;
```

**3. Gates prüfen**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)-[:HAS_GATE]->(g)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
RETURN g.code AS gate, g.score AS score, g.status AS status,
       g.reason AS reason
ORDER BY g.code;
```

**4. Kriterien und Evidenz prüfen**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)-[:HAS_SCORE]->(s)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
OPTIONAL MATCH (s)-[:SUPPORTED_BY]->(e)
RETURN s.code AS criterion, s.raw_score AS raw_score,
       s.weight AS weight, s.evidence_quality AS evidence_quality,
       collect(coalesce(e.title, e.url, e.id))[0..5] AS evidence
ORDER BY s.code;
```

**5. Scores ohne Evidenz finden**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)-[:HAS_SCORE]->(s)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
OPTIONAL MATCH (s)-[:SUPPORTED_BY]->(e)
WITH s, count(e) AS evidence_count
WHERE evidence_count = 0
RETURN s.code AS criterion, s.raw_score AS raw_score, s.reason AS reason;
```

**6. Materialfluss prüfen**

```cypher
MATCH (p)-[:USES_COMPONENT]->(c)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
OPTIONAL MATCH (c)-[:ORIGINATES_FROM]->(d)
RETURN c.id AS component_id, c.category AS category, c.material AS material,
       c.quantity AS quantity, c.condition AS condition,
       d.name AS donor_source, d.location AS donor_location
ORDER BY category, component_id;
```

**7. ReUse-Quote und Scope prüfen**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
RETURN a.reuse_share AS reuse_share, a.reuse_scope AS reuse_scope,
       a.reuse_scope_note AS scope_note;
```

**8. Kontrollrechnung prüfen**

```cypher
MATCH (p)-[:HAS_ASSESSMENT]->(a)-[:HAS_SCORE]->(s)
WHERE toLower(coalesce(p.name, p.title, "")) CONTAINS toLower($project_name)
  AND coalesce(a.version, "") = "v6"
WITH a,
     sum(toFloat(s.weight) * toFloat(s.raw_score) * 25) AS weighted_sum,
     sum(toFloat(s.weight)) AS weight_sum
RETURN a.rsi_brutto AS stored_brutto,
       round(weighted_sum / weight_sum, 1) AS recalculated_brutto,
       a.rsi_final AS stored_final,
       a.confidence AS stored_confidence;
```

### 17.5 Umgang mit Graph-Diskrepanzen

| Diskrepanz | Vorgehen |
|---|---|
| Graph enthält höhere Scores als Quellen belegen | Score senken oder Evidenz ergänzen. |
| Quelle nennt neue Daten, Graph ist veraltet | Graph aktualisieren und Änderung dokumentieren. |
| Mehrere Projektknoten für dasselbe Projekt | Dubletten markieren und Master-Knoten festlegen. |
| Score vorhanden, Evidenz fehlt | Evidenzwert maximal 1; keine finale A-Konfidenz. |
| ReUse-Quote im Graph ohne Scope | K10 konservativ bewerten und Scope nachrecherchieren. |
| Gate fehlt | Gate als 0 oder 1 bewerten, bis Evidenz vorliegt. |
| Externe Kontrollrechnung weicht > 1 RSI-Punkt ab | Berechnung prüfen, Gewichtung korrigieren, Version klären. |

---

## 18. Copy-Paste-Prompt für neue Recherche und Scoring

Der folgende Prompt ist für erneute Recherche, Datenextraktion, Neo4j-Prüfung und RSI-v6-Scoring gedacht. Er soll in Research- oder Agenten-Workflows vollständig übernommen werden.

```text
Du bist Research- und Scoring-Assistent:in für den Reuse-Scalability Index (RSI v6).

Ziel:
Bewerte das folgende ReUse-Projekt oder ReUse-System nach RSI v6 neu. Führe die Recherche, Datenextraktion, Neo4j-Graphprüfung, Gate-Bewertung, Kriterienbewertung, Konfidenzbewertung und finale Einstufung vollständig und nachvollziehbar durch.

Projekt / System:
[PROJEKTNAME]

Pflichtregeln:
1. Arbeite nicht aus Erinnerung. Recherchiere neu und bevorzuge Primärquellen: Projektberichte, Inventare, Ausschreibungen, Pläne, LCA, Prüfberichte, Betreiber-/Hubdaten, Behörden- oder Förderberichte.
2. Trenne strikt Element-ReUse, Recycling, biobasierte Materialien und Bestandserhalt.
3. Jede ReUse-Quote braucht einen Scope: whole_building, structural, facade, single_trade, interior_fitout, temporary_borrowed, platform_volume oder unknown.
4. Bewerte fehlende Information nicht als N/A. Fehlende Information ist Score 0 oder 1 mit niedriger Evidenz.
5. Bei tragenden Bauteilen dürfen Qualität/Regulatorik und Haftung/Versicherung nie N/A sein.
6. Wende alle Gate-Kappungsregeln an, bevor du die finale RSI-Einstufung formulierst.
7. DOUBLE-CHECK IMMER DEN NEO4J-GRAPHEN. Keine finale Bewertung ohne Abgleich zwischen Quellen, extrahierten Daten, Graphdaten und Kontrollrechnung.
8. Wenn Neo4j und Quellen widersprechen, erstelle eine Diskrepanzliste. Verwende die besser belegte Quelle und markiere den Graph als zu aktualisieren.
9. Ein Score ohne Evidenzlink darf nicht als belastbar gelten. Evidenzwert maximal 1, bis eine Quelle verknüpft ist.
10. Gib keine höhere Konfidenzklasse als die Quellenlage erlaubt.

Arbeitsablauf:

A. Projektprofil bestimmen
- Wähle genau ein Hauptprofil:
  whole_building_project, interior_fitout_reuse, structural_reuse,
  material_hub_platform, network_ecosystem, digital_inventory_tool,
  temporary_or_exhibition.
- Begründe die Profilwahl in 2–3 Sätzen.

B. Recherche neu durchführen
- Sammle belastbare Quellen zu:
  Projektauftrag, ReUse-Ziel, Bauteilquellen, Inventar, Prüfungen,
  Haftung, Logistik, Ausschreibung, Kosten/Zeit, Design, Akteure,
  Markt/Politik, Umweltwirkung.
- Extrahiere Fakten nur mit Quellenbezug.
- Markiere unklare, widersprüchliche oder unbelegte Angaben.

C. Daten extrahieren
Erstelle eine Datentabelle mit diesen Feldern:
- Projekt: Name, Ort, Jahr, Nutzung, Fläche, temporär/permanent, Profil.
- ReUse: Strategie, Zielquote, reale Quote, Scope, Bauteilfamilien.
- Quellen: Spenderobjekte, Materialhubs, Reservierungsstatus, Entfernung, Timing.
- Inventar: IDs, Maße, Mengen, Zustand, Verbindung, Schadstoffe, Verfügbarkeit.
- Qualität: Prüfungen, Normen, Zustandsklassen, Freigaben, Zertifikate.
- Risiko: Haftung, Gewährleistung, Versicherung, Verantwortungsmatrix.
- Logistik: Ausbau, Kennzeichnung, Transport, Lager, Aufbereitung, Einbau.
- Beschaffung: Ausschreibung, Vertrag, LV, Vergabekriterien, Substitutionsregeln.
- Kosten/Zeit: Zusatzaufwände, Risikopuffer, Terminpuffer, Kalkulationslogik.
- Design: DfD, reversible Verbindungen, Adaptivität, Schichten, Standardisierung.
- Akteure: Bauherrschaft, Planende, Rückbau, Prüfstellen, Hubs, Behörden.
- Markt/Politik: Netzwerke, Förderungen, Zielquoten, öffentliche Nachfrage.
- Wirkung: CO₂, Ressourcen, LCA-Grenzen, Vergleichsfall, Transport, Aufbereitung.

D. Neo4j-Graph doppelt prüfen
- Suche den Projektknoten und mögliche Dubletten.
- Prüfe, ob eine RSI-v6-Bewertung existiert.
- Prüfe Gates, K1–K14-Scores, Evidenzlinks, Bauteilquellen, Materialfluss, ReUse-Scope, Impact Claims und gespeicherte Berechnung.
- Führe eine externe Kontrollrechnung des RSI brutto und final durch.
- Dokumentiere alle Abweichungen zwischen Quellen, extrahierter Tabelle und Neo4j.
- Liste notwendige Graph-Updates als konkrete Änderungen auf.

E. Gates bewerten
Bewerte G1–G6 jeweils mit 0, 1 oder 2:
G1 frühe Planungsintegration
G2 Materialinventar und Quellobjektdaten
G3 Qualitäts- und Sicherheitsnachweis
G4 Haftung, Garantie und Versicherung
G5 Reverse-Logistik und Zwischenlagerung
G6 Beschaffung, Kosten und Terminmodell

Für jedes Gate angeben:
- Score
- Begründung
- Evidenz
- offene Unsicherheit

F. Kriterien bewerten
Bewerte K1–K14 jeweils mit Rohscore 0–4 und Evidenzwert 0–3:
K1 frühe Planung, Beschaffung und Projektmandat
K2 Versorgung, Quellensicherheit und Reservierbarkeit
K3 Inventar, Datenqualität und digitale Rückverfolgbarkeit
K4 Qualität, Prüfung und regulatorische Konformität
K5 Haftung, Garantie, Versicherung und Risikoallokation
K6 Reverse-Logistik, Zwischenlagerung und Timing
K7 Ausschreibung, Vertragsfähigkeit und Beschaffbarkeit
K8 Kosten- und Terminrealismus
K9 zirkuläres Design, Anpassungsfähigkeit und DfD
K10 Wiederverwendungstiefe, Scope und Bauteilumfang
K11 Akteurskompetenz, Rollen und Prozessfähigkeit
K12 Markt-, Netzwerk-, Politik- und Nachfrageunterstützung
K13 Replizierbarkeit und Champion-Unabhängigkeit
K14 Umwelt- und Ressourcenwirkungsnachweis

Für jedes Kriterium angeben:
- Rohscore 0–4
- normierter Score
- Gewicht
- gewichteter Beitrag
- Evidenzwert 0–3
- Begründung
- Quellen / Graph-Evidenz
- Unsicherheit / Korrekturbedarf

G. RSI berechnen
Berechne:
- RSI brutto
- Gate-Kappung
- RSI final
- Konfidenz
- Konfidenzklasse A/B/C
- Einstufung: Einzelfall/Fallstudie, Pilot/Reallabor, bedingt skalierbar, skalierbar, systemisch skalierbar
- Archetyp

H. Ergebnis ausgeben
Strukturiere die Antwort so:
1. Kurzurteil in 3–5 Sätzen
2. Profil und Archetyp
3. Gate-Matrix
4. Kriterien-Scoring-Tabelle K1–K14
5. Berechnung RSI brutto/final und Konfidenz
6. Neo4j-Double-Check: gefunden, fehlend, widersprüchlich, zu aktualisieren
7. Stärkste Skalierungsfaktoren
8. Kritische Blocker
9. Konkrete nächste Schritte zur Verbesserung des RSI
10. Quellenliste

Qualitätsstandard:
- Bewerte konservativ.
- Behaupte keine Skalierbarkeit ohne Gates, Evidenz und Neo4j-Abgleich.
- Trenne klar zwischen belegten Fakten, plausiblen Annahmen und offenen Fragen.
- Wenn Daten fehlen, sage genau, welche Daten fehlen und wie sie erhoben werden müssen.
```

---

## 19. Grenzen des Rahmenwerks

1. **Kein Ersatz für technische Prüfung:** Der RSI zeigt Skalierungsreife, ersetzt aber keine Statik-, Brandschutz-, Schadstoff- oder Genehmigungsprüfung.
2. **Profilabhängigkeit:** Ein Ansatz kann für Innenausbau hoch skalierbar sein und für tragende Bauteile nicht.
3. **Datenabhängigkeit:** Ohne Primärquellen, Inventare und Prüfunterlagen sinkt die Konfidenz.
4. **Kosten sind Umsetzbarkeit, nicht Rendite:** Der RSI bewertet, ob Kosten und Zeit realistisch behandelt werden, nicht ob ein Geschäftsmodell profitabel ist.
5. **Politik und Markt ändern sich:** Zielquoten, CO₂-Grenzwerte, Förderinstrumente und Normen können die Skalierbarkeit schnell verändern.
6. **ReUse ist nicht immer die beste Lösung:** Bestandserhalt, Umbau und Weiternutzung können zirkulär vorrangig sein.
7. **Graphdaten sind prüfpflichtig:** Neo4j ist nur so belastbar wie die eingepflegten Quellen, Relationen und Versionen.
8. **Score ist kein Freifahrtschein:** Ein hoher RSI zeigt Systemreife, aber nicht automatisch architektonische, soziale oder wirtschaftliche Qualität.

---

## 20. Wissenschaftliche und fachliche Verankerung

**Design / DfD:** Durmisevic — Transformation Capacity und reversibles Bauen; DGBC/Alba-Concepts — Disassembly Potential; Brand — Shearing Layers; ISO 20887 — Design for Disassembly and Adaptability.

**Zirkularität / Bewertung:** Ellen MacArthur Foundation — Material Circularity Indicator; EU Level(s); Küpfer/Brütting/Fivet — MCDA; Reuse Viability Index; BCR-Feasibility.

**Skalierung / Transition:** Geels — Multi-Level-Perspective; ReUse Market Dynamics; Chalmers — upscaling reuse in construction; BaselCircular/Cirkla/Intep — ReUse in der Bauindustrie stärken.

**Entwurfspraxis:** Brütting, Fivet, Senatore — *form follows availability*.

---

## 21. Finaler Merksatz

Ein ReUse-Projekt ist skalierbar, wenn es nicht nur Bauteile wiederverwendet, sondern eine wiederholbare und belegbare Kette aus **Quelle, Inventar, Nachweis, Risiko, Logistik, Beschaffung, Design, Kosten, Kompetenz, Nachfrage und Datenprüfung** aufbaut.

**Skalierbarkeit ist keine Eigenschaft eines spektakulären Einzelfalls, sondern die Fähigkeit eines ReUse-Ansatzes, von anderen Akteur:innen unter realen Markt-, Rechts-, Bauprozess- und Datenbedingungen wiederholt zu werden.**

---

*Ende der RSI-v6-Systemfassung.*
