# Anforderungsbasiertes Action Framework für ein digitales ReUse-Planungssystem

## 1. Zweck des Dokuments

Dieses Dokument fasst die erarbeiteten User Stories in einer konsolidierten, wissenschaftlich geeigneten Fassung zusammen und übersetzt sie in ein strukturiertes Action Framework für ein digitales Planungssystem zur Wiederverwendung von Bauteilen. Der Fokus liegt auf drei funktionalen Systemmodulen:

1. **Bauteilportal**
2. **Bauteilkatalog**
3. **Design Tool**

Die drei Module beschreiben den Weg von der Erfassung und Qualifizierung wiederverwendbarer Bauteile über deren Sichtbarmachung und Auswahl bis hin zur Integration, Kombination, Analyse und Dokumentation im Entwurfsprozess.

---

## 2. Methodische Grundlage

Die Anforderungsbasis wurde aus einer Sammlung von User-Story-Karten abgeleitet, die vier Akteur:innen im ReUse-Planungsprozess zugeordnet wurden: Mitarbeiter:innen der Bauteilbörse, Architekt:innen, Tragwerksplaner:innen und Energieberater:innen. Die ursprünglichen Karten wurden sprachlich vereinheitlicht, fachlich abstrahiert und in ein konsistentes User-Story-Format überführt:

> **Als [Akteur:in] möchte ich [Funktion bzw. Ziel], damit [fachlicher Nutzen].**

Im Konsolidierungsprozess wurde eine inhaltlich doppelte Architekt:innen-Karte identifiziert. Die ursprüngliche Sammlung umfasst daher 36 Karten; für die Analyse werden 35 fachlich eindeutige User Stories verwendet.

| Kategorie | Anzahl |
|---|---:|
| Ursprünglich gesammelte Karten | 36 |
| Identifiziertes Duplikat | 1 |
| Fachlich eindeutige User Stories | 35 |

Die 35 fachlich eindeutigen User Stories verteilen sich wie folgt:

| Akteur:in | Anzahl User Stories |
|---|---:|
| Mitarbeiter:in der Bauteilbörse | 10 |
| Architekt:in | 12 |
| Tragwerksplaner:in | 6 |
| Energieberater:in | 7 |
| **Gesamt** | **35** |

---

## 3. Konsolidierte User-Story-Basis

### 3.1 Mitarbeiter:in der Bauteilbörse

**BB-01 — Bauteildaten erfassen**  
Als Mitarbeiter:in der Bauteilbörse möchte ich wiederverwendbare Bauteile mit relevanten technischen, logistischen und qualitativen Informationen erfassen, damit Planungsteams sie als belastbare Grundlage für Entwurfs- und Entscheidungsprozesse nutzen können.

**BB-02 — Bauteile zu planungsrelevanten Einheiten bündeln**  
Als Mitarbeiter:in der Bauteilbörse möchte ich einzelne Bauteile zu sinnvollen Gruppen oder Paketen zusammenfassen, damit Planungsteams mit verwendbaren Mengen und zusammenhängenden Materialbeständen arbeiten können.

**BB-03 — Verfügbarkeit transparent machen**  
Als Mitarbeiter:in der Bauteilbörse möchte ich zeitliche Verfügbarkeiten von Bauteilen transparent darstellen, damit Rückbau, Lagerung, Planung und Wiedereinbau besser koordiniert werden können.

**BB-04 — Status von Bauteilen verwalten**  
Als Mitarbeiter:in der Bauteilbörse möchte ich den aktuellen Status von Bauteilen verwalten, damit Planungsteams erkennen können, welche Elemente verfügbar, reserviert, in Prüfung oder nicht mehr nutzbar sind.

**BB-05 — Bestandsdaten standardisieren**  
Als Mitarbeiter:in der Bauteilbörse möchte ich Informationen aus Gebäudebeständen in einem einheitlichen Datenformat erfassen, damit sie vergleichbar, auswertbar und in weiteren Planungsschritten nutzbar sind.

**BB-06 — Kontextinformationen dokumentieren**  
Als Mitarbeiter:in der Bauteilbörse möchte ich ergänzende Informationen zum ursprünglichen Einsatz, zur gestalterischen Absicht und zum Nutzungskontext eines Bauteils dokumentieren, damit Planungsteams dessen Wiederverwendung qualifiziert bewerten können.

**BB-07 — Bauteilhistorie nachvollziehbar machen**  
Als Mitarbeiter:in der Bauteilbörse möchte ich die Herkunft und Nutzungsgeschichte eines Bauteils dokumentieren, damit Planungsteams dessen Qualität, Eignung und potenzielle Risiken besser einschätzen können.

**BB-08 — Informationslücken sichtbar machen**  
Als Mitarbeiter:in der Bauteilbörse möchte ich fehlende oder noch zu prüfende Informationen sichtbar machen, damit offene Nachweise gezielt an zuständige Fachplaner:innen übergeben werden können.

**BB-09 — Kostenstruktur transparent darstellen**  
Als Mitarbeiter:in der Bauteilbörse möchte ich die relevanten Kostenbestandteile von ReUse-Bauteilen transparent darstellen, damit Planungsteams wirtschaftliche Auswirkungen realistisch bewerten können.

**BB-10 — Zusatzleistungen modular anbieten**  
Als Mitarbeiter:in der Bauteilbörse möchte ich projektbezogene Zusatzleistungen modular anbieten, damit Planungsteams je nach Projektphase und Informationsbedarf passende Unterstützungsleistungen auswählen können.

---

### 3.2 Architekt:in

**A-01 — Verfügbare ReUse-Materialien frühzeitig einsehen**  
Als Architekt:in möchte ich verfügbare ReUse-Bauteile bereits in frühen Planungsphasen einsehen, damit der Entwurf von Beginn an auf realen Materialverfügbarkeiten aufbauen kann.

**A-02 — Bauteilbasiert entwerfen**  
Als Architekt:in möchte ich Bauteile anhand relevanter Eigenschaften suchen und filtern, damit ich Entwurfskonzepte mit vorhandenen Elementen entwickeln und prüfen kann.

**A-03 — Bauteile für Entwurfsvarianten sichern**  
Als Architekt:in möchte ich relevante Bauteile temporär für bestimmte Entwurfsvarianten sichern können, damit die Planung auf einer verlässlicheren Materialverfügbarkeit basiert.

**A-04 — Entwurfsvarianten vergleichen**  
Als Architekt:in möchte ich unterschiedliche Entwurfsvarianten vergleichen, damit gestalterische, technische, ökologische, wirtschaftliche und organisatorische Auswirkungen fundiert bewertet werden können.

**A-05 — ReUse-Bauteile digital in den Entwurf integrieren**  
Als Architekt:in möchte ich ReUse-Bauteile als strukturierte digitale Planungsobjekte übernehmen, damit sie direkt in Entwurfs- und Modellierungsprozesse eingebunden werden können.

**A-06 — Entwurfsrelevante Risiken erkennen**  
Als Architekt:in möchte ich entwurfsrelevante Risiken und fehlende Informationen zu Bauteilen erkennen, damit ich deren Eignung als Planungsgrundlage realistisch einschätzen kann.

**A-07 — Änderungen an geplanten Bauteilen nachvollziehen**  
Als Architekt:in möchte ich über relevante Änderungen an eingeplanten Bauteilen informiert werden, damit ich Entwurf, Termine und Abstimmungen rechtzeitig anpassen kann.

**A-08 — Gestalterische Eigenschaften berücksichtigen**  
Als Architekt:in möchte ich ästhetische und materielle Eigenschaften von ReUse-Bauteilen gezielt berücksichtigen, damit Wiederverwendung als bewusster Bestandteil des Entwurfs eingesetzt werden kann.

**A-09 — Phasenbezogene ReUse-Aufgaben steuern**  
Als Architekt:in möchte ich ReUse-relevante Aufgaben entlang der Planungsphasen strukturieren, damit Entscheidungen, Prüfungen und Dokumentationen zum richtigen Zeitpunkt erfolgen.

**A-10 — Risiken systematisch bewerten**  
Als Architekt:in möchte ich Risiken zu geplanten Bauteilen systematisch angezeigt bekommen, damit ich ihre Auswirkungen auf Entwurf, Kosten, Termine und Umsetzbarkeit bewerten kann.

**A-11 — Bauteile flexibel filtern**  
Als Architekt:in möchte ich Bauteile über frei kombinierbare Kriterien filtern, damit ich geeignete Elemente gezielt für unterschiedliche Entwurfsanforderungen auswählen kann.

**A-12 — ReUse-Prozesse den Planungsphasen zuordnen**  
Als Architekt:in möchte ich ReUse-relevante Entscheidungen und Aufgaben den jeweiligen Planungsphasen zuordnen, damit der Wiederverwendungsprozess nachvollziehbar in den Planungsablauf integriert wird.

---

### 3.3 Tragwerksplaner:in

**T-01 — Tragwerksrelevante Bauteile identifizieren**  
Als Tragwerksplaner:in möchte ich ReUse-Bauteile anhand strukturell relevanter Eigenschaften suchen und filtern, damit ich geeignete Elemente für tragende Anwendungen schnell identifizieren kann.

**T-02 — Fehlende Tragwerksinformationen erkennen**  
Als Tragwerksplaner:in möchte ich fehlende oder unvollständige Tragwerksinformationen erkennen, damit notwendige Prüfungen, Annahmen und Nachweise definiert werden können.

**T-03 — Frühes fachliches Feedback geben**  
Als Tragwerksplaner:in möchte ich frühzeitig Rückmeldungen zu vorgeschlagenen Bauteilanordnungen geben, damit tragwerksrelevante Fragen vor zentralen Entwurfsentscheidungen geklärt werden können.

**T-04 — Konstruktive Lösungsprinzipien dokumentieren**  
Als Tragwerksplaner:in möchte ich mögliche konstruktive Lösungs- und Anschlussprinzipien dokumentieren, damit ReUse-Bauteile realistisch in die weitere Planung integriert werden können.

**T-05 — Tragwerksvarianten vergleichen**  
Als Tragwerksplaner:in möchte ich unterschiedliche Tragwerksvarianten vergleichen, damit technische, wirtschaftliche, ökologische und gestalterische Auswirkungen fundiert gegeneinander abgewogen werden können.

**T-06 — Nachweisfähige Informationen exportieren**  
Als Tragwerksplaner:in möchte ich relevante Berechnungen, Annahmen, Prüfresultate und Entscheidungen standardisiert exportieren, damit ReUse-Bauteile in Bewilligungs-, Ausschreibungs- und Ausführungsprozesse überführt werden können.

---

### 3.4 Energieberater:in

**E-01 — Frühe Umweltwirkung abschätzen**  
Als Energieberater:in möchte ich relevante Material-, Herkunfts- und Logistikinformationen zu ReUse-Bauteilen erhalten, damit ökologische Auswirkungen bereits in frühen Planungsphasen abgeschätzt werden können.

**E-02 — ReUse-Bauteile in Bewertungen integrieren**  
Als Energieberater:in möchte ich ReUse-Bauteile mit bewertungsrelevanten Kennwerten verknüpfen, damit unterschiedliche Material- und Konstruktionsvarianten vergleichbar analysiert werden können.

**E-03 — Ökologische Wirkung von Varianten vergleichen**  
Als Energieberater:in möchte ich die ökologische Wirkung verschiedener Entwurfsvarianten vergleichen, damit Planungsteams die Auswirkungen von Materialentscheidungen nachvollziehen können.

**E-04 — ReUse-Varianten energetisch prüfen**  
Als Energieberater:in möchte ich ReUse-Varianten mit relevanten Modellinformationen verknüpfen, damit deren energetische Auswirkungen ohne unverhältnismäßigen Modellierungsaufwand geprüft werden können.

**E-05 — Grenzwerte und Zielwerte prüfen**  
Als Energieberater:in möchte ich Projekte mit relevanten ökologischen und energetischen Ziel- oder Grenzwerten vergleichen, damit ReUse-Entscheidungen messbar bewertet werden können.

**E-06 — Optimierungsmöglichkeiten aufzeigen**  
Als Energieberater:in möchte ich erkennen, wann ReUse-Bauteile durch ergänzende Maßnahmen verbessert werden sollten, damit zirkuläre und energetische Anforderungen gemeinsam erfüllt werden können.

**E-07 — Bewertungsergebnisse exportieren**  
Als Energieberater:in möchte ich relevante Kennwerte, Diagramme und Bewertungsergebnisse exportieren, damit Auftraggeber:innen, Planungsteams und Behörden die Entscheidungsgrundlagen nachvollziehen können.

---

## 4. Dreiteilige Systemstruktur

Die konsolidierten User Stories werden in drei funktionale Systemmodule übersetzt. Diese Module bilden die zentrale Struktur des Action Frameworks.

| Systemmodul | Funktion im ReUse-Planungssystem | Leitfrage |
|---|---|---|
| **Bauteilportal** | Erfassung, Standardisierung und Qualifizierung wiederverwendbarer Bauteile | Wie werden Bauteile so dokumentiert, dass sie für spätere Planungsprozesse verwendbar sind? |
| **Bauteilkatalog** | Sichtbarmachung, Suche, Bewertung und Auswahl einzelner Bauteile oder Bauteilpakete | Wie können Planungsteams geeignete Bauteile finden, verstehen und auswählen? |
| **Design Tool** | Integration, Kombination, Analyse und Dokumentation von Bauteilen im Entwurf | Wie werden ausgewählte Bauteile zu Entwurfsvarianten, Systemen und Projekten zusammengeführt? |

Die Zuordnung folgt einer funktionalen Abgrenzung:

- Das **Bauteilportal** umfasst alle Anforderungen, die sich auf die Erfassung, Strukturierung, Qualifizierung und Bereitstellung von Bauteildaten beziehen.
- Der **Bauteilkatalog** umfasst alle Anforderungen, die einzelne Bauteile oder Bauteilpakete auffindbar, vergleichbar, bewertbar und auswählbar machen.
- Das **Design Tool** umfasst alle Anforderungen, bei denen ausgewählte Bauteile im Entwurfsprozess platziert, kombiniert, analysiert, koordiniert oder dokumentiert werden.

Als Abgrenzungsprinzip gilt:

> Sobald mehrere Bauteile räumlich, konstruktiv, funktional oder analytisch kombiniert werden, wird die entsprechende Anforderung dem **Design Tool** zugeordnet.

---

## 5. Mapping der User Stories auf Systemmodule

Für das Mapping werden die konsolidierten User Stories in abgeleitete funktionale Anforderungen überführt und den drei Systemmodulen **Bauteilportal**, **Bauteilkatalog** und **Design Tool** zugeordnet. Dadurch bleibt die Struktur kompakt, nachvollziehbar und für eine spätere Systementwicklung nutzbar.

Die Zuordnung folgt der Logik:

> **User Story → abgeleitete funktionale Anforderung → Systemmodul**

| ID | Abgeleitete funktionale Anforderung | Primäres Systemmodul | Zugeordnete User Stories |
|---|---|---|---|
| **REQ-01** | Bauteildaten erfassen und standardisieren | Bauteilportal | BB-01, BB-05 |
| **REQ-02** | Bauteile gruppieren und zu planungsrelevanten Einheiten bündeln | Bauteilportal | BB-02 |
| **REQ-03** | Verfügbarkeit und Status verwalten | Bauteilportal / Bauteilkatalog | BB-03, BB-04, A-03, A-07 |
| **REQ-04** | Kontext, Herkunft und Bauteilhistorie dokumentieren | Bauteilportal | BB-06, BB-07 |
| **REQ-05** | Nachweise, Risiken und Informationslücken verwalten | Bauteilportal / Bauteilkatalog | BB-08, A-06, A-10, T-02 |
| **REQ-06** | Kosten und ergänzende Leistungen transparent machen | Bauteilportal / Bauteilkatalog | BB-09, BB-10 |
| **REQ-07** | Bauteile suchen, filtern und auswählen | Bauteilkatalog | A-01, A-02, A-11, T-01 |
| **REQ-08** | Gestalterische und materielle Eigenschaften bewerten | Bauteilkatalog | A-08 |
| **REQ-09** | Ökologische, energetische und leistungsbezogene Bewertungen ermöglichen | Bauteilkatalog / Design Tool | E-01, E-02, E-03, E-04, E-05, E-06 |
| **REQ-10** | Digitale Bauteilobjekte in den Entwurfsprozess überführen | Bauteilkatalog / Design Tool | A-05 |
| **REQ-11** | Entwurfs- und Tragwerksvarianten entwickeln und vergleichen | Design Tool | A-04, T-05, E-03 |
| **REQ-12** | Konstruktive Integration und fachliches Feedback unterstützen | Design Tool | T-03, T-04 |
| **REQ-13** | ReUse-Prozesse phasenbezogen koordinieren | Design Tool | A-09, A-12 |
| **REQ-14** | Dokumentation, Berichte und exportierbare Nachweise erzeugen | Design Tool | T-06, E-07 |

---

## 6. Vollständigkeit und Nachverfolgbarkeit

Alle 35 fachlich eindeutigen User Stories wurden in das Mapping aufgenommen. Die folgende Kontrollmatrix zeigt die vollständige Abdeckung nach Akteur:innen:

| Akteur:in | User Stories | Im Mapping enthalten |
|---|---:|---:|
| Mitarbeiter:in der Bauteilbörse | 10 | 10 |
| Architekt:in | 12 | 12 |
| Tragwerksplaner:in | 6 | 6 |
| Energieberater:in | 7 | 7 |
| **Gesamt** | **35** | **35** |

Einige User Stories sind für mehr als ein Systemmodul relevant. Das Mapping ist daher nicht als strikt exklusive Zuordnung zu verstehen, sondern als Nachverfolgbarkeitsmatrix zwischen User Stories, funktionalen Anforderungen und Systemmodulen. Dies betrifft insbesondere Anforderungen, die eine Schnittstelle zwischen Auswahl und Entwurfsintegration bilden. Ein Beispiel ist:

- **A-05 — ReUse-Bauteile digital in den Entwurf integrieren**

Diese User Story verbindet den **Bauteilkatalog** mit dem **Design Tool**. Im Bauteilkatalog werden digitale Bauteilobjekte bereitgestellt; im Design Tool werden sie im Entwurf verwendet, kombiniert und analysiert. Die Story bleibt fachlich eine einzelne Anforderung, wird im Mapping jedoch als Schnittstellenanforderung sichtbar.

---

## 7. Interpretation der Systemmodule

### 7.1 Bauteilportal

Das Bauteilportal bildet die Datengrundlage des digitalen ReUse-Planungssystems. Es stellt sicher, dass wiederverwendbare Bauteile nicht nur physisch verfügbar sind, sondern als strukturierte, vergleichbare und planungsrelevante Datensätze vorliegen. Die zugeordneten Anforderungen zeigen, dass ReUse-Planung neben technischen und geometrischen Informationen auch Verfügbarkeit, Status, Herkunft, Nutzungskontext, Informationslücken, Nachweise, Kosten und ergänzende Dienstleistungen berücksichtigen muss.

Das Bauteilportal übernimmt damit eine qualifizierende und vorbereitende Funktion: Es erzeugt die Datenbasis, auf der Katalog-, Entwurfs- und Analyseprozesse aufbauen.

### 7.2 Bauteilkatalog

Der Bauteilkatalog macht die im Bauteilportal bereitgestellten Informationen für Planungsteams zugänglich. Er dient nicht nur als Datenbank, sondern als Auswahl- und Entscheidungsoberfläche. Die zugeordneten Anforderungen zeigen, dass Bauteile gesucht, gefiltert, verglichen und hinsichtlich technischer, gestalterischer, ökologischer sowie risikobezogener Kriterien bewertet werden müssen.

Der Bauteilkatalog bildet damit die Schnittstelle zwischen verfügbarer Materialrealität und frühen Planungsentscheidungen.

### 7.3 Design Tool

Das Design Tool ist die Ebene, auf der ausgewählte Bauteile in konkrete Entwurfszusammenhänge überführt werden. Während der Bauteilkatalog einzelne Bauteile sichtbar und bewertbar macht, unterstützt das Design Tool deren räumliche, konstruktive, ökologische und prozessuale Integration.

Die zugeordneten Anforderungen betreffen insbesondere Variantenbildung, konstruktive Prinzipien, fachliches Feedback, Risiko- und Änderungsbewertung, energetisch-ökologische Analyse, phasenbezogene Koordination sowie Export- und Dokumentationsfunktionen.

---

## 8. Action Framework

Aus dem Mapping ergibt sich ein dreistufiges Action Framework. Die drei Module können als aufeinander aufbauende Arbeitspakete für die weitere Systementwicklung verstanden werden.

| Schritt | Systemmodul | Schwerpunkt | Mögliche Umsetzung |
|---|---|---|---|
| 1 | **Bauteilportal** | Bauteildaten erfassen, standardisieren und qualifizieren | Datenmodell, Eingabeformulare, Statuslogik, Nachweislogik |
| 2 | **Bauteilkatalog** | Bauteile sichtbar, suchbar, bewertbar und auswählbar machen | Katalogoberfläche, Filterlogik, Bauteilprofile, Risiko- und Kennwertanzeigen |
| 3 | **Design Tool** | Bauteile im Entwurf kombinieren, analysieren und dokumentieren | Variantenwerkzeug, Regel- und Plausibilitätsprüfung, Analysefunktionen, Exportmodule |

Dieses Framework übersetzt die Stakeholder-Anforderungen in funktionale Systemmodule und schafft eine Grundlage für die Ableitung von Prototypen, Arbeitspaketen und Evaluationskriterien.

---

## 9. Zusammenfassende Einordnung

Aus den erhobenen User-Story-Karten wurde ein konsolidiertes Set von 35 fachlich eindeutigen Anforderungen abgeleitet. Diese Anforderungen wurden in drei funktionale Systemmodule übersetzt: ein **Bauteilportal** zur standardisierten Erfassung und Qualifizierung von Bauteildaten, ein **Bauteilkatalog** zur Sichtbarmachung, Bewertung und Auswahl einzelner Komponenten sowie ein **Design Tool** zur Integration, Kombination, Analyse und Dokumentation von ReUse-Bauteilen im Entwurfsprozess.

Das resultierende Action Framework bildet eine strukturierte Grundlage für die Entwicklung, prototypische Umsetzung und spätere Evaluation digitaler Workflows für die Wiederverwendung von Bauteilen in der Architekturplanung.
