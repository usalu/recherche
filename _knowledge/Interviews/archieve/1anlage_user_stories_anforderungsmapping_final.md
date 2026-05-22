# Anlage: Konsolidierte User Stories und Anforderungsmapping

**Forschungsstelle:** UdK Berlin (KET) · **Arbeitspaket:** AP a, AP-Erfahrung  
**Meilensteinbezug:** Diese Anlage trägt zur Zielerreichung von **Meilenstein a (Monat 4)** bei. Aus dem Erfahrungswissen wurden User-Stories abgeleitet, die als Grundlage für das User-Experience-Design dienen.  
**Projekt:** „Entwerfen mit Bestand", Aktenzeichen 10.08.18.7-25.06



## 1. Einordnung

Die User Stories wurden aus einem erfahrungsbasierten Anforderungsprozess abgeleitet. Ausgangspunkt waren praxisbezogene Anforderungen aus den Perspektiven von Bauteilbörsen, Architekt:innen, Tragwerksplaner:innen und Energieberater:innen. Als qualitative Quellen dienten unter anderem die ausgewerteten Interviews (siehe Anhänge Interview-Auswertung Tom Svilans und Raoul Bunschoten). Über die im Antrag für AP a genannten Gruppen (Architekt:innen sowie Bauingenieur:innen/Tragwerksplaner:innen) hinaus wurden Bauteilbörsen-Mitarbeiter:innen und Energieberater:innen einbezogen, um Anforderungen entlang der gesamten Wiederverwendungs- und Bewertungskette zu erfassen; dies entspricht der Risiko-Gegenmaßnahme, User-Stories breit aus der Praxis abzuleiten und zu vereinheitlichen. Die Bearbeitung dieser Anlage erfolgte federführend durch die UdK Berlin (KET). Die gesammelten Karten wurden sprachlich bereinigt, fachlich abstrahiert und in eine konsistente User-Story-Struktur überführt:

> **Als [Akteur:in] möchte ich [Ziel oder Funktion], damit [fachlicher Nutzen].**

Diese Satzstruktur folgt dem in der agilen Anforderungserhebung etablierten Template; zur Vermeidung typischer sprachlicher Defekte wurden die Formulierungen an den Kriterien des Quality-User-Story-Frameworks ausgerichtet (Lucassen et al. 2016).

Aus ursprünglich **36 gesammelten Karten** wurden **35 fachlich eindeutige User Stories** abgeleitet. Eine Architekt:innen-Karte trat inhaltlich doppelt auf und wurde konsolidiert. Die User Stories sind als konsolidierte Zwischenanforderungen zu verstehen. Sie bilden keine finale technische Spezifikation, sondern eine methodische Grundlage für Human-Interface-Design, Prototypentwicklung und spätere Validierung. Ihre weitere Rückbindung an einzelne Quellen und ihre Überprüfung im Prototyp erfolgen im weiteren Projektverlauf.

Die Erweiterung um Bauteilbörsen und Energieberatung ist erforderlich, weil Entwurfsfähigkeit nicht allein in der Entwurfsumgebung entsteht. Sie hängt bereits von der Qualität der Einspeisung, der Nachweisführung, der ökologischen Bewertbarkeit und der späteren Übertragbarkeit der Daten ab.

| Akteursgruppe | Ursprüngliche Karten | Konsolidierte User Stories |
|---|---:|---:|
| Mitarbeiter:in einer Bauteilbörse | 10 | 10 |
| Architekt:in | 13 | 12 |
| Tragwerksplaner:in | 6 | 6 |
| Energieberater:in | 7 | 7 |
| **Gesamt** | **36** | **35** |

**Terminologische Einordnung:** In dieser Anlage bezeichnet der Begriff **Baukomponente** sowohl einzelne wiederverwendbare Bauteile als auch zusammenhängende Bauteilgruppen oder -pakete, sofern diese für den Entwurfsprozess relevant sind. Der Begriff **Aggregator** bezeichnet die entwurfsbezogene Integrations- und Analyseebene; technisch entspricht diese Ebene dem Aggregator innerhalb des semio-basierten Entwurfswerkzeugs.

---

## 2. Konsolidierte User Stories

### 2.1 Mitarbeiter:in einer Bauteilbörse

**BB-01: Baukomponentendaten erfassen**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich wiederverwendbare Baukomponenten mit relevanten technischen, logistischen und qualitativen Informationen erfassen, damit Planungsteams sie als belastbare Grundlage für Entwurfs- und Entscheidungsprozesse nutzen können.

**BB-02: Baukomponenten zu planungsrelevanten Einheiten bündeln**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich einzelne Baukomponenten zu sinnvollen Gruppen oder Paketen zusammenfassen, damit Planungsteams mit verwendbaren Mengen und zusammenhängenden Materialbeständen arbeiten können.

**BB-03: Verfügbarkeit transparent machen**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich zeitliche Verfügbarkeiten von Baukomponenten transparent darstellen, damit Rückbau, Lagerung, Planung und Wiedereinbau besser koordiniert werden können.

**BB-04: Status von Baukomponenten verwalten**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich den aktuellen Status von Baukomponenten verwalten, damit Planungsteams erkennen können, welche Elemente verfügbar, reserviert, in Prüfung oder nicht mehr nutzbar sind.

**BB-05: Bestandsdaten standardisieren**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich Informationen aus Gebäudebeständen in einem einheitlichen Datenformat erfassen, damit sie vergleichbar, auswertbar und in weiteren Planungsschritten nutzbar sind.

**BB-06: Kontextinformationen dokumentieren**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich ergänzende Informationen zum ursprünglichen Einsatz, zur gestalterischen Absicht und zum Nutzungskontext einer Baukomponente dokumentieren, damit Planungsteams deren Wiederverwendung qualifiziert bewerten können.

**BB-07: Baukomponentenhistorie nachvollziehbar machen**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich die Herkunft und Nutzungsgeschichte einer Baukomponente dokumentieren, damit Planungsteams deren Qualität, Eignung und potenzielle Risiken besser einschätzen können.

**BB-08: Informationslücken sichtbar machen**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich fehlende oder noch zu prüfende Informationen sichtbar machen, damit offene Nachweise gezielt an zuständige Fachplaner:innen übergeben werden können.

**BB-09: Kostenstruktur transparent darstellen**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich die relevanten Kostenbestandteile wiederverwendbarer Baukomponenten transparent darstellen, damit Planungsteams wirtschaftliche Auswirkungen realistisch bewerten können.

**BB-10: Zusatzleistungen modular anbieten**  
Als Mitarbeiter:in einer Bauteilbörse möchte ich projektbezogene Zusatzleistungen modular anbieten, damit Planungsteams je nach Projektphase und Informationsbedarf passende Unterstützungsleistungen auswählen können.

BB-09 und BB-10 werden als ergänzende Anforderungen geführt. Sie sind für spätere Anschlussfähigkeit an Bauteilbörsen und Geschäftsprozesse relevant, stehen jedoch nicht im Kern der prototypischen Umsetzung des ersten Projektabschnitts.

---

### 2.2 Architekt:in

**A-01: Verfügbare Baukomponenten frühzeitig einsehen**  
Als Architekt:in möchte ich verfügbare wiederverwendbare Baukomponenten bereits in frühen Planungsphasen einsehen, damit der Entwurf von Beginn an auf realen Materialverfügbarkeiten aufbauen kann.

**A-02: Baukomponentenbasiert entwerfen**  
Als Architekt:in möchte ich Baukomponenten anhand relevanter Eigenschaften suchen und filtern, damit ich Entwurfskonzepte mit vorhandenen Elementen entwickeln und prüfen kann.

**A-03: Baukomponenten für Entwurfsvarianten sichern**  
Als Architekt:in möchte ich relevante Baukomponenten temporär für bestimmte Entwurfsvarianten sichern können, damit die Planung auf einer verlässlicheren Materialverfügbarkeit basiert.

**A-04: Entwurfsvarianten vergleichen**  
Als Architekt:in möchte ich unterschiedliche Entwurfsvarianten vergleichen, damit gestalterische, technische, ökologische, wirtschaftliche und organisatorische Auswirkungen fundiert bewertet werden können.

**A-05: Baukomponenten digital in den Entwurf integrieren**  
Als Architekt:in möchte ich wiederverwendbare Baukomponenten als strukturierte digitale Planungsobjekte übernehmen, damit sie direkt in Entwurfs- und Modellierungsprozesse eingebunden werden können.

**A-06: Entwurfsrelevante Risiken erkennen**  
Als Architekt:in möchte ich entwurfsrelevante Risiken und fehlende Informationen zu Baukomponenten erkennen, damit ich deren Eignung als Planungsgrundlage realistisch einschätzen kann.

**A-07: Änderungen an geplanten Baukomponenten nachvollziehen**  
Als Architekt:in möchte ich über relevante Änderungen an eingeplanten Baukomponenten informiert werden, damit ich Entwurf, Termine und Abstimmungen rechtzeitig anpassen kann.

**A-08: Gestalterische Eigenschaften berücksichtigen**  
Als Architekt:in möchte ich ästhetische und materielle Eigenschaften wiederverwendbarer Baukomponenten gezielt berücksichtigen, damit Wiederverwendung als bewusster Bestandteil des Entwurfs eingesetzt werden kann.

**A-09: Phasenbezogene ReUse-Aufgaben steuern**  
Als Architekt:in möchte ich ReUse-relevante Aufgaben entlang der Planungsphasen strukturieren, damit Entscheidungen, Prüfungen und Dokumentationen zum richtigen Zeitpunkt erfolgen.

**A-10: Risiken systematisch bewerten**  
Als Architekt:in möchte ich Risiken zu geplanten Baukomponenten systematisch angezeigt bekommen, damit ich ihre Auswirkungen auf Entwurf, Kosten, Termine und Umsetzbarkeit bewerten kann.

**A-11: Baukomponenten flexibel filtern**  
Als Architekt:in möchte ich Baukomponenten über frei kombinierbare Kriterien filtern, damit ich geeignete Elemente gezielt für unterschiedliche Entwurfsanforderungen auswählen kann.

**A-12: ReUse-Prozesse den Planungsphasen zuordnen**  
Als Architekt:in möchte ich ReUse-relevante Entscheidungen und Aufgaben den jeweiligen Planungsphasen zuordnen, damit der Wiederverwendungsprozess nachvollziehbar in den Planungsablauf integriert wird.

---

### 2.3 Tragwerksplaner:in

**T-01: Tragwerksrelevante Baukomponenten identifizieren**  
Als Tragwerksplaner:in möchte ich wiederverwendbare Baukomponenten anhand strukturell relevanter Eigenschaften suchen und filtern, damit ich geeignete Elemente für tragende Anwendungen schnell identifizieren kann.

**T-02: Fehlende Tragwerksinformationen erkennen**  
Als Tragwerksplaner:in möchte ich fehlende oder unvollständige Tragwerksinformationen erkennen, damit notwendige Prüfungen, Annahmen und Nachweise definiert werden können.

**T-03: Frühes fachliches Feedback geben**  
Als Tragwerksplaner:in möchte ich frühzeitig Rückmeldungen zu vorgeschlagenen Baukomponentenanordnungen geben, damit tragwerksrelevante Fragen vor zentralen Entwurfsentscheidungen geklärt werden können.

**T-04: Konstruktive Lösungsprinzipien dokumentieren**  
Als Tragwerksplaner:in möchte ich mögliche konstruktive Lösungs- und Anschlussprinzipien dokumentieren, damit wiederverwendbare Baukomponenten realistisch in die weitere Planung integriert werden können.

**T-05: Tragwerksvarianten vergleichen**  
Als Tragwerksplaner:in möchte ich unterschiedliche Tragwerksvarianten vergleichen, damit technische, wirtschaftliche, ökologische und gestalterische Auswirkungen fundiert gegeneinander abgewogen werden können.

**T-06: Nachweisfähige Informationen exportieren**  
Als Tragwerksplaner:in möchte ich relevante Berechnungen, Annahmen, Prüfresultate und Entscheidungen standardisiert exportieren, damit wiederverwendbare Baukomponenten in Bewilligungs-, Ausschreibungs- und Ausführungsprozesse überführt werden können.

---

### 2.4 Energieberater:in

**E-01: Frühe Umweltwirkung abschätzen**  
Als Energieberater:in möchte ich relevante Material-, Herkunfts- und Logistikinformationen zu wiederverwendbaren Baukomponenten erhalten, damit ökologische Auswirkungen bereits in frühen Planungsphasen abgeschätzt werden können.

**E-02: Wiederverwendbare Baukomponenten in Bewertungen integrieren**  
Als Energieberater:in möchte ich wiederverwendbare Baukomponenten mit bewertungsrelevanten Kennwerten verknüpfen, damit unterschiedliche Material- und Konstruktionsvarianten vergleichbar analysiert werden können.

**E-03: Ökologische Wirkung von Varianten vergleichen**  
Als Energieberater:in möchte ich die ökologische Wirkung verschiedener Entwurfsvarianten vergleichen, damit Planungsteams die Auswirkungen von Materialentscheidungen nachvollziehen können.

**E-04: Varianten energetisch prüfen**  
Als Energieberater:in möchte ich Varianten mit relevanten Modellinformationen verknüpfen, damit deren energetische Auswirkungen ohne unverhältnismäßigen Modellierungsaufwand geprüft werden können.

**E-05: Grenzwerte und Zielwerte prüfen**  
Als Energieberater:in möchte ich Projekte mit relevanten ökologischen und energetischen Ziel- oder Grenzwerten vergleichen, damit Wiederverwendungsentscheidungen messbar bewertet werden können.

**E-06: Optimierungsmöglichkeiten aufzeigen**  
Als Energieberater:in möchte ich erkennen, wann wiederverwendbare Baukomponenten durch ergänzende Maßnahmen verbessert werden sollten, damit zirkuläre und energetische Anforderungen gemeinsam erfüllt werden können.

**E-07: Bewertungsergebnisse exportieren**  
Als Energieberater:in möchte ich relevante Kennwerte, Diagramme und Bewertungsergebnisse exportieren, damit Auftraggeber:innen, Planungsteams und Behörden die Entscheidungsgrundlagen nachvollziehen können.

---

## 3. Systematische Zuordnung der User Stories

Die konsolidierten User Stories werden im nächsten Schritt den drei zentralen Bereichen der vorgesehenen Systemarchitektur zugeordnet: **Bauteilportal**, **Bauteilkatalog** und **Aggregator**. Diese drei Bereiche beschreiben keine losen Funktionsgruppen, sondern aufeinander bezogene Ebenen eines durchgängigen digitalen Arbeitsprozesses mit wiederverwendbaren Baukomponenten.

Das **Bauteilportal** bildet die Eingangs- und Qualifizierungsebene des Systems. Hier werden Daten zu Baukomponenten eingegeben, importiert, ergänzt, strukturiert, geprüft und für die weitere Nutzung vorbereitet. Der Fokus liegt auf Datenqualität, Vollständigkeit, Nachweisen, Unsicherheiten, Statusinformationen und Anschlussfähigkeit an bestehende Bauteilbörsen oder externe Datenquellen.

Der **Bauteilkatalog** bildet die standardisierte Sicht- und Auswahlebene. Hier werden die im Bauteilportal erfassten oder importierten Baukomponenten in einer einheitlichen Struktur sichtbar, suchbar, filterbar und vergleichbar gemacht. Der Fokus liegt auf der Entscheidungsvorbereitung: Nutzer:innen sollen einzelne Baukomponenten hinsichtlich Eigenschaften, Verfügbarkeit, Eignung, Risiken, Nachweisen und weiteren planungsrelevanten Informationen bewerten können.

Der **Aggregator** bildet die entwurfsbezogene Integrations- und Analyseebene. Hier werden ausgewählte Baukomponenten in Entwurfsszenarien platziert, kombiniert, verbunden und bewertet. Der Fokus liegt auf Situationen, in denen mehrere Komponenten räumlich, konstruktiv, gestalterisch oder performativ zusammenwirken. Dazu zählen Variantenbildung, Kombinationslogiken, Anschlussfragen, Zielkonflikte, ökologische und tragwerksbezogene Annahmen sowie Feedback aus der Entwurfs- und Performancebewertung.

Die Zuordnung der User Stories erfolgt nach der jeweiligen Hauptfunktion. Anforderungen zur Datenerfassung und Qualifizierung werden primär dem Bauteilportal zugeordnet. Anforderungen zur Sichtbarkeit, Suche, Auswahl und Bewertung einzelner Komponenten werden dem Bauteilkatalog zugeordnet. Anforderungen, die die Kombination mehrerer Komponenten, Entwurfsvarianten oder performancebezogene Auswertungen betreffen, werden dem Aggregator zugeordnet.

Das Mapping ist damit nicht als finale technische Spezifikation zu verstehen. Es dient der systematischen Übersetzung der User Stories in funktionale Anforderungscluster und bildet eine Grundlage für die weitere Ausarbeitung von Human-Interface-Design, Prototyp und Validierung.

---
## 4. Anforderungsmapping der User Stories

Für das Mapping werden die User Stories in funktionale Anforderungscluster übersetzt und einem primären Systembereich zugeordnet. Dadurch bleibt die Struktur kompakt, nachvollziehbar und für die weitere Systementwicklung nutzbar.

Die Zuordnung folgt der Logik:

> **User Story → funktionaler Anforderungscluster → primärer Systembereich**

Einige Anforderungen erzeugen Schnittstellen zwischen den Systembereichen. Diese Schnittstellen werden nicht als Doppelzählung verstanden, sondern als Übergaben zwischen den Systembereichen: vom Bauteilportal in den Bauteilkatalog und vom Bauteilkatalog in den Aggregator.

| ID | Funktionaler Anforderungscluster | Primärer Systembereich | Schnittstelle / Übergabe | Zugeordnete User Stories | Priorität | Prototypstatus |
|---|---|---|---|---|---|---|
| **REQ-01** | Baukomponentendaten erfassen und standardisieren | Bauteilportal | Grundlage für Bauteilkatalog | BB-01, BB-05 | Muss | in Bearbeitung |
| **REQ-02** | Baukomponenten gruppieren und zu planungsrelevanten Einheiten bündeln | Bauteilportal | Darstellung als Pakete im Bauteilkatalog | BB-02 | Soll | konzeptionell |
| **REQ-03** | Verfügbarkeit und Status verwalten | Bauteilportal | Statusanzeige und Reservierungslogik im Bauteilkatalog | BB-03, BB-04, A-03, A-07 | Muss | konzeptionell / in Bearbeitung |
| **REQ-04** | Kontext, Herkunft und Baukomponentenhistorie dokumentieren | Bauteilportal | Anzeige im Baukomponentenprofil des Bauteilkatalogs | BB-06, BB-07 | Soll | konzeptionell |
| **REQ-05** | Nachweise, Risiken und Informationslücken verwalten | Bauteilportal | Sichtbarkeit und Bewertung im Bauteilkatalog | BB-08, A-06, A-10, T-02 | Muss | konzeptionell |
| **REQ-06** | Kosten und ergänzende Leistungen transparent machen | Bauteilportal | Vergleichs- und Entscheidungsinformation im Bauteilkatalog | BB-09, BB-10 | Kann | außerhalb des ersten Prototyps |
| **REQ-07** | Baukomponenten suchen, filtern und auswählen | Bauteilkatalog | Übergabe geeigneter Komponenten an den Aggregator | A-01, A-02, A-11, T-01 | Muss | in Bearbeitung |
| **REQ-08** | Gestalterische und materielle Eigenschaften bewerten | Bauteilkatalog | Grundlage für gestalterische Auswahl im Entwurf | A-08 | Soll | konzeptionell |
| **REQ-09** | Ökologische, energetische und leistungsbezogene Kennwerte pro Baukomponente bereitstellen | Bauteilkatalog | Grundlage für spätere Variantenbewertung im Aggregator | E-01, E-02 | Soll | konzeptionell |
| **REQ-10** | Digitale Baukomponenten in Entwurfsworkflows überführen | Bauteilkatalog | Übergabe strukturierter Planungsobjekte an den Aggregator | A-05 | Muss | in Bearbeitung |
| **REQ-11** | Entwurfs- und Tragwerksvarianten entwickeln und vergleichen | Aggregator | Nutzung ausgewählter Katalogkomponenten | A-04, T-05 | Muss | in Bearbeitung |
| **REQ-12** | Ökologische und energetische Variantenbewertung unterstützen | Aggregator | Rückgriff auf Kennwerte und Annahmen aus Bauteilportal und Bauteilkatalog | E-03, E-04, E-05, E-06 | Soll | konzeptionell |
| **REQ-13** | Konstruktive Integration und fachliches Feedback unterstützen | Aggregator | Rückkopplung offener Nachweise in Bauteilportal und Bauteilkatalog | T-03, T-04 | Soll | konzeptionell |
| **REQ-14** | ReUse-Prozesse phasenbezogen koordinieren | Aggregator | Verbindung zu Prüf-, Nachweis- und Dokumentationsständen | A-09, A-12 | Kann | konzeptionell |
| **REQ-15** | Dokumentation, Berichte und exportierbare Nachweise erzeugen | Aggregator | Export aus Entwurfs-, Bewertungs- und Nachweisprozessen | T-06, E-07 | Soll | konzeptionell |

---


## 5. Kurze Schlussfolgerung

Diese Anlage fasst die konsolidierten User Stories als strukturierte Grundlage für die weitere Ausarbeitung des Human-Interface-Designs zusammen. Das Mapping zeigt, wie die Anforderungen unterschiedlicher Akteursgruppen in funktionale Anforderungscluster übersetzt und den drei Systembereichen **Bauteilportal**, **Bauteilkatalog** und **Aggregator** zugeordnet werden können.

Die Trennung der drei Bereiche macht deutlich, dass das Projekt unterschiedliche Aufgabenebenen adressiert: die Qualifizierung von Baukomponentendaten, ihre standardisierte Sichtbarkeit und Auswahl sowie ihre spätere entwurfsbezogene Kombination und Bewertung. Die Anlage ist daher nicht als finale technische Spezifikation zu verstehen, sondern als nachvollziehbare Zwischenebene zwischen Anforderungserhebung, User-Experience-Design, prototypischer Entwicklung und späterer Validierung.


## Literatur

Lucassen, G., Dalpiaz, F., van der Werf, J. M. E. M. & Brinkkemper, S. (2016): Improving agile requirements: the Quality User Story framework and tool. Requirements Engineering 21(3), S. 383–403. DOI: 10.1007/s00766-016-0250-x.

Lucassen, G., Dalpiaz, F., van der Werf, J. M. E. M. & Brinkkemper, S. (2016): The Use and Effectiveness of User Stories in Practice. In: Requirements Engineering: Foundation for Software Quality (REFSQ 2016), LNCS 9619, S. 205–222.
