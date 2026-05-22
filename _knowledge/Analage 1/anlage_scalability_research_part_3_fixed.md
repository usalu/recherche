# Anlage X
# Skalierbarkeitsrecherche zu internationalen ReUse-Projekten
## Teil 3 von 4 — Übertragung der Fallstudienmuster auf ein technologisches ReUse-Ökosystem

**Projektbezug:** *Entwerfen mit Bestand* — offene Plattform für einen KI-unterstützten, performance-optimierten und integrativen Entwurfsprozess mit wiederverwendeten Baukomponenten.

**Quellenbasis:** Dieser Teil nutzt ausschließlich den RSI-v6-Abschlussbericht, die in Teil 1 und Teil 2 verdichtete Projektauswertung sowie den Zukunft-Bau-Zuwendungsantrag als Bezugsrahmen. Es werden keine RSI-Werte neu kalibriert, keine zusätzlichen Projektbehauptungen eingeführt und keine im RSI-Bericht nicht belegten Nachweise erfunden.

**Funktion dieses Teils:** Teil 3 übersetzt die Muster aus der 74-Projekt-Recherche in Anforderungen an ein zukünftiges technologisches ReUse-Ökosystem. Der Text bleibt strategisch und forschungsbezogen. Er ist keine Software-Spezifikation, kein User-Story-Dokument und keine Arbeitspaket-Zuordnung.

---

## 9. Mapping der Fallstudienmuster auf ein technologisches ReUse-Ökosystem

Die folgenden Ökosystemimplikationen sind keine technischen Implementierungsvorgaben. Sie übersetzen wiederkehrende Skalierungshemmnisse in strategische Anforderungen an ein mögliches digitales ReUse-Ökosystem.

Die Fallstudien zeigen, dass die Skalierung von Bauteilwiederverwendung nicht primär an der Idee des ReUse scheitert. Zahlreiche Projekte belegen, dass wiederverwendete Bauteile gestalterisch, konstruktiv und ökologisch relevant eingesetzt werden können. Die wiederkehrenden Brüche liegen vielmehr in der Übersetzung realer Bauteile in verlässliche, vergleichbare und entwurfsrelevante Informationen. Ein technologisches ReUse-Ökosystem sollte deshalb mehr leisten als eine digitale Bauteilliste. Es sollte Unsicherheit, Nachweisstatus, Zeitlichkeit, Verantwortung und Entwurfsrelevanz zusammenführen.

| Muster aus den Fallstudien | RSI-Dimension | Skalierungsproblem | Strategische Ökosystemimplikation |
|---|---|---|---|
| Unzureichende Bauteilmetadaten | K3 Inventar, Datenqualität und Rückverfolgbarkeit; K10 Scope | Bauteile sind vorhanden, aber ohne verlässliche Angaben zu Material, Maßen, Zustand, Quelle, Menge, Verfügbarkeit oder Prüfstatus nicht planbar. | Ein Mindestdatensatz sollte Bauteile als planungs- und nachweisrelevante Datenträger erfassen, nicht nur als Katalogeinträge. |
| Unvollständige Geometrie | K3 Inventar; K9 zirkuläres Design; K4 technische Prüfung | Entwurfsvarianten können nicht belastbar erzeugt oder geprüft werden, wenn Bauteilgeometrie, Toleranzen und Anschlussbedingungen im aktuellen Evidenzregister nicht ausreichend abgebildet sind. | Geometrische Daten sollten in verschiedenen Detaillierungsgraden verfügbar sein: grob für frühe Suche, präziser für Entwurfsintegration und Prüfung. |
| Unsichere Quelle und Verfügbarkeit | G2 Materialinventar und Quellobjektdaten; K2 Versorgung und Quellensicherheit | Ein Bauteil ist nicht skalierungsfähig, wenn Herkunft, Eigentum, Ausbauzeitpunkt oder Reservierbarkeit unklar bleiben. | Das Ökosystem braucht Quellobjektbezug, Verfügbarkeitsfenster, Reservierungsstatus und Statuswechsel zwischen „potenziell“, „gesichert“, „in Prüfung“, „reserviert“ und „verfügbar“. |
| Unklarer Prüfstatus | G3 Qualität und Sicherheit; K4 regulatorische Konformität | Erfolgreiche gebaute Beispiele ersetzen keinen wiederholbaren Prüfpfad. Besonders bei tragenden Bauteilen bleibt Skalierung ohne dokumentierten Prüfstatus begrenzt. | Bauteildaten sollten Prüfbedarf, Prüfstatus, Prüftiefe, technische Freigabegrenzen und offene Risiken abbilden. |
| Unklare Haftung oder Verantwortung | G4 Haftung, Garantie und Versicherung; K5 Risikoallokation | Technischer Nachweis löst nicht automatisch Gewährleistung, Versicherung, Kette der Verantwortung oder Mängelrisiko. | Das Ökosystem sollte verantwortungsrelevante Informationen sichtbar machen: Eigentum, Ausbauverantwortung, Transportverantwortung, Prüfverantwortung, Einbauverantwortung und offene Haftungsfragen. |
| Unklare Logistik und Lagerung | G5 Reverse-Logistik; K6 Zwischenlagerung und Timing | ReUse scheitert, wenn Rückbau, Lagerung, Aufbereitung, Reservierung und Einbau zeitlich nicht zusammenpassen. | Logistikstatus, Lagerort, Handlingaufwand, Transportfenster, Aufbereitungsbedarf und Terminrisiko sollten als Entwurfsparameter mitgeführt werden. |
| Schwache Beschaffungs- und Kosteninformation | G6 Beschaffung/Kosten/Programm; K7 Vertragsfähigkeit; K8 Kosten- und Terminrealismus | ReUse bleibt projektabhängig, wenn Bauteile zwar technisch einsetzbar, aber nicht ausschreibbar, kalkulierbar oder terminlich integrierbar sind. | Das Ökosystem sollte nicht nur Bauteile anzeigen, sondern Beschaffbarkeit, Kostenunsicherheit, Vertragsreife und Terminintegration kenntlich machen. |
| Unsichere LCA-Annahmen | K14 Umwelt- und Ressourcenwirkungsnachweis | CO₂- oder Ressourcenvorteile sind häufig plausibel, aber ohne Systemgrenzen, Transport, Aufbereitung und Vergleichsfall schwer vergleichbar. | Umweltbewertung sollte als frühe Plausibilisierung mit Unsicherheitsstufen verstanden werden, nicht als endgültige LCA-Freigabe. |
| Unklare strukturelle Anwendbarkeit | G3 Qualität/Sicherheit; K4 Prüfung; K9 Entwurfsanpassung | Bauteile können geometrisch passen, aber strukturell, brandschutztechnisch oder anschlusslogisch ungeeignet sein. | Tragfähigkeits- und Anschlussplausibilität sollten früh als Filter und Warnsystem eingebunden werden, ohne technische Zertifizierung vorzutäuschen. |
| Zu viele Entwurfskombinationen | K9 Design und Anpassungsfähigkeit; K3 Datenqualität | Große Bestandspools erzeugen kombinatorische Komplexität, die manuell kaum in konsistente Entwurfsvarianten übersetzbar ist. | Das Ökosystem sollte Suchraumreduktion, Ähnlichkeitslogik, Bauteilgruppenbildung und performancebezogene Vorauswahl ermöglichen. |
| Fragmentierte Akteursnetzwerke | K11 Akteurskompetenz; K12 Markt-/Netzwerkunterstützung | Entwerfende, Rückbauakteure, Händler, Ingenieur:innen, Bauherrschaft, Behörden und Prüfinstanzen arbeiten selten auf einem gemeinsamen Informationsstand. | Das Ökosystem sollte Akteursrollen, Datenzuständigkeiten und Übergabepunkte sichtbar machen, ohne daraus ein starres Prozessmodell abzuleiten. |
| Profilspezifische Prozessunterschiede | Bewertungsprofile; K13 Replizierbarkeit | Struktureller ReUse, Fit-out-ReUse, temporäres Borrowing, Selbstwiederverwendung und öffentliche Beschaffungsmodelle skalieren nach unterschiedlichen Logiken. | Die Plattformlogik sollte Profilansichten erlauben: nicht jedes Bauteil und nicht jeder Prozess braucht dieselbe Nachweisdichte, aber Unterschiede sollten explizit werden. |

Die Übertragung auf ein technologisches Ökosystem folgt aus einer zentralen Beobachtung der Fallstudien: Skalierbarkeit entsteht nicht durch die bloße Digitalisierung von Bauteilangeboten. Sie entsteht erst, wenn Bauteile als **situierte, unvollständige, zeitgebundene und nachweispflichtige Entwurfsressourcen** behandelt werden.

---

## 10. Zentrale Lernfelder für den Aufbau eines technologischen ReUse-Ökosystems

### 10.1 Mindestdatensatz für wiederverwendete Baukomponenten

Die 74 Projekte zeigen, dass ReUse dort planbar wird, wo Bauteile nicht nur benannt, sondern mit belastbaren Grunddaten beschrieben sind. Wiederkehrend sind Angaben zu Maß, Menge, Zustand, Herkunft, Ausbauzeitpunkt, Verfügbarkeit, Verbindungstyp, Schadstoffverdacht, Prüfstatus und logistischer Lage im source-bound Korpus nicht ausreichend vollständig abgebildet. Ohne diese Angaben bleibt ein Bauteil ein Suchergebnis, aber keine Entwurfsgrundlage.

Für Skalierbarkeit ist der Mindestdatensatz entscheidend, weil Entwerfende, Ingenieur:innen, Liefernde und Bauherrschaften auf dieselbe Informationsbasis zugreifen sollten. Ein Bauteil kann nur dann in frühen Entwurfsvarianten berücksichtigt werden, wenn es nicht erst nachträglich manuell geprüft, vermessen und verhandelt werden sollte.

Für ein technologisches Ökosystem bedeutet dies: Es braucht einen **standardisierten, aber erweiterbaren Bauteildatensatz**. Dieser sollte einfache Objekte ebenso aufnehmen können wie komplexe Bauteilfamilien. Er sollte unvollständige Felder nicht verstecken, sondern sollte Datenreife sichtbar machen.

### 10.2 Evidenz- und Unsicherheitsstufen

Der RSI-v6-Bericht zeigt, dass die verfügbare Evidenz zwischen Projekten stark variiert. Manche Projekte besitzen technische oder ökologische Nachweise, aber keine Haftungs- oder Beschaffungsdaten. Andere sind gestalterisch einflussreich, aber nur über Medien- oder Projektseiten dokumentiert. Diese Unterschiede dürfen nicht geglättet werden.

Für Skalierbarkeit ist die Unterscheidung von Evidenzqualität und Evidenzabdeckung zentral. Ein einzelner hochwertiger technischer Nachweis kann eine strukturelle Prüfung stützen, aber nicht automatisch Kosten, Beschaffung oder Verantwortung belegen. Umgekehrt kann ein gut dokumentierter Beschaffungsprozess ohne technische Prüfung für tragende Bauteile unzureichend sein.

Für ein technologisches Ökosystem folgt daraus: Jede Bauteil- und Projektaussage sollte eine **Evidenzstufe** erhalten und eine **Unsicherheitsstufe**. Die Plattform darf nicht nur Ergebnisse anzeigen, sondern sollte markieren, ob eine Aussage gemessen, geprüft, geschätzt, abgeleitet, geplant oder ungeklärt ist.

### 10.3 Verknüpfung von Entwurf und realer Verfügbarkeit

Die Fallstudien zeigen, dass erfolgreiche ReUse-Projekte nicht erst nach einem fertigen Entwurf nach passenden Bauteilen suchen. Vielmehr beeinflussen verfügbare Bauteile früh Form, Raster, Struktur, Hülle, Ausbau oder Detailstrategie. Dieses Prinzip wird im RSI-v6 über frühe Planungsintegration, Quellensicherheit und zirkuläres Design erfasst.

Für Skalierbarkeit ist diese frühe Verknüpfung entscheidend. Wenn ReUse erst nach Entwurfsfixierung auftritt, wird es zu einer Sonderbeschaffung oder Substitution. Wenn reale Verfügbarkeit früh in den Entwurf einfließt, kann ReUse zur eigentlichen Entwurfslogik werden.

Für ein technologisches Ökosystem bedeutet dies: Der Bauteilkatalog sollte mit Entwurfsräumen verbunden werden. Komponenten dürfen nicht nur gefunden, sondern sollten nach geometrischer, konstruktiver, ökologischer und zeitlicher Passung in Varianten eingebunden werden können. Der Antrag zu *Entwerfen mit Bestand* adressiert genau diesen Übergang von Katalog, Entwurfs- und Performancebeurteilung in einer integrierten Plattform.

### 10.4 Nachweis- und Prüfpfade

Strukturelle, brandschutztechnische, akustische, schadstoffbezogene oder dauerhaftigkeitsbezogene Anforderungen sind in den Fallstudien häufig entscheidende Schwellen. Besonders bei Stahl, Beton, Holztragwerken und Fassadenelementen reicht eine allgemeine Beschreibung des Bauteils nicht aus. Skalierbarkeit hängt davon ab, ob wiederkehrende Prüfpfade entstehen.

Für Skalierbarkeit bedeutet dies: Technische Prüfung sollte vom Einzelfallwissen in dokumentierbare Abläufe überführt werden. Dies umfasst Sichtprüfung, Materialprüfung, Zustandsklassen, Geometrieprüfung, Anschlussprüfung, Restlebensdauer, Normenbezug und behördliche Anschlussfähigkeit. Der RSI-v6 trennt diese technische Nachweisfrage bewusst von Haftung und Versicherung.

Für ein technologisches Ökosystem folgt: Es sollte Prüfbedarfe früh kennzeichnen und keine technische Freigabe suggerieren. Die Funktion eines solchen Systems besteht zunächst in **Nachweisnavigation**: Welche Information ist im aktuellen Evidenzregister nicht ausreichend belegt? Welche Fachprüfung ist erforderlich? Welche Bauteile sind nur für nicht tragende Anwendungen plausibel? Welche sind strukturell potenziell geeignet, aber noch nicht freigegeben?

### 10.5 Logistik, Zeitlichkeit und Reservierung

Mehrere Projektprofile zeigen, dass Bauteilwiederverwendung zeitgebunden ist. Ein Bauteil entsteht als Angebot erst durch Rückbau, Ausbau, Demontage, Lagerung und Aufbereitung. Gleichzeitig sollte es zu einem zukünftigen Projekt passen, dessen Entwurf, Ausschreibung und Bauablauf eigene Zeitlogiken besitzen.

Für Skalierbarkeit ist diese zeitliche Kopplung zentral. Ein vorhandenes Bauteil ist nicht automatisch verfügbar. Es kann zu früh, zu spät, in falscher Menge, ohne Lagerort, ohne Reservierung oder mit unklarem Ausbauzustand vorhanden sein. Logistik ist deshalb nicht nachgelagerte Ausführung, sondern Teil der ReUse-Entwurfsfähigkeit.

Für ein technologisches Ökosystem bedeutet dies: Verfügbarkeit sollte als dynamischer Status modelliert werden. Notwendig sind Angaben zu Rückbauzeitpunkt, Verfügbarkeitsfenster, Lagerstatus, Reservierungsstatus, Transportbedarf, Aufbereitungsbedarf und Wiedereinbautermin. Nur so kann der Entwurf mit realen Zeitfenstern arbeiten.

### 10.6 Verantwortungs- und Rolleninformation

Der RSI-v6-Bericht macht deutlich, dass technische Machbarkeit und Verantwortbarkeit unterschiedliche Probleme sind. Ein Bauteil kann technisch geprüft sein, ohne dass Gewährleistung, Versicherung, Eigentumsübergang, Verantwortung für Ausbau, Transport, Lagerung, Anpassung oder Wiedereinbau geklärt sind.

Für Skalierbarkeit ist dies ein entscheidender Unterschied. Solange Verantwortung informell bei besonders engagierten Akteur:innen liegt, bleibt ReUse ein Sonderprozess. Skalierung erfordert, dass Rollen und Risiken übertragbar beschrieben werden können.

Für ein technologisches Ökosystem folgt: Es braucht keine rechtliche Bewertung im engeren Sinne, aber verantwortungsrelevante Metadaten. Dazu gehören Akteursrollen, Eigentumsstatus, Zuständigkeit für Prüfung, Zuständigkeit für Demontage, Zuständigkeit für Transport, Abnahmezustand und offene Haftungsfragen. Solche Angaben erhöhen nicht automatisch die rechtliche Sicherheit, machen aber die Skalierungsrisiken sichtbar.

### 10.7 Profilabhängige ReUse-Workflows

Die Fallstudien zeigen, dass unterschiedliche ReUse-Profile nicht mit denselben Maßstäben bewertet werden können. Struktureller Komponenten-ReUse benötigt andere Nachweise als Innenausbau. Temporäres Borrowing ist anders zu interpretieren als permanente Gebäudeintegration. Same-site Urban Mining unterscheidet sich von projektübergreifender Materialaggregation.

Für Skalierbarkeit bedeutet dies: Ein generischer Workflow ist zu grob. Er würde entweder tragende Bauteile unterprüfen oder einfache Finish-Bauteile überlasten. Der RSI-v6 reagiert darauf mit Projektprofilen und profilrelativem Lernwert.

Für ein technologisches Ökosystem folgt: Es sollte profilabhängige Ansichten und Anforderungen ermöglichen. Ein Stahlträger, eine Fassadenplatte, ein Türblatt, ein Sanitärbauteil, eine temporär geliehene Komponente und ein on-site wiederverwendeter Betonabschnitt benötigen unterschiedliche Datenfelder, Prüfpfade und Warnlogiken.

### 10.8 Datenbasierte Entscheidungsunterstützung

Der Zukunft-Bau-Antrag benennt die kombinatorische Komplexität großer Bestandspools als zentrales Problem: Viele mögliche Bauteilkombinationen lassen sich manuell kaum mit traditioneller Performancebeurteilung zusammenführen. Die Fallstudien bestätigen diese Herausforderung aus praktischer Sicht: ReUse-Projekte benötigen laufend Entscheidungen unter unvollständiger Information.

Für Skalierbarkeit ist datenbasierte Entscheidungsunterstützung wichtig, weil sie Such-, Vergleichs- und Bewertungsprozesse verkürzen kann. Dabei darf sie jedoch Unsicherheit nicht in scheinbar präzise Ergebnisse verwandeln. Frühe Unterstützung sollte plausibilisieren, priorisieren und Warnungen ausgeben, nicht technische oder rechtliche Freigaben ersetzen.

Für ein technologisches Ökosystem bedeutet dies: Entscheidungsunterstützung sollte mehrkriteriell und unsicherheitssensibel sein. Sie sollte Bauteilpassung, Entwurfslogik, ökologische Annahmen, konstruktive Plausibilität, Verfügbarkeit, Logistik und Evidenzniveau zusammenführen. Damit wird die Plattform nicht nur zum Katalog, sondern zu einem Instrument der **verantwortbaren Entwurfsraumerkundung**.

---

## 11. Strukturierte Ökosystemanforderungen aus der Fallstudienanalyse

Die folgenden Anforderungen sind keine Implementierungsspezifikation. Sie beschreiben forschungsgeleitete Strukturmerkmale, die aus den Fallstudien und dem RSI-v6-Rahmen für ein technologisches ReUse-Ökosystem abgeleitet werden. Entscheidend ist, dass jedes Merkmal eine konkrete Skalierungsfunktion besitzt.

| Ökosystemanforderung | Herleitung aus Projekten | Relevante RSI-Dimension | Zweck für Skalierbarkeit |
|---|---|---|---|
| Komponentenidentität | Viele Fälle zeigen, dass ReUse ohne eindeutige Bauteilzuordnung zwischen Quelle, Inventar, Prüfung, Lagerung und Wiedereinbau unscharf bleibt. | G2, K3, K10 | Eindeutige Zuordnung jedes Bauteils über Projektphasen hinweg; Grundlage für Vergleich, Reservierung und Dokumentation. |
| Quellenrückverfolgbarkeit | Mehrquellen-Aggregation, öffentliche Stockpile-Modelle und donorbasierte Strukturwiederverwendung benötigen Herkunfts- und Spenderobjektbezug. | G2, K2, K3 | Sicherung von Herkunft, Eigentum, Materialgeschichte und Verantwortungsübergängen. |
| Geometrie- und Maßdaten | Entwurfsintegration scheitert, wenn Bauteile nur textlich beschrieben sind. Raster, Toleranzen, Querschnitte und Anschlussgeometrie beeinflussen Varianten. | K3, K9, K4 | Ermöglicht Suche, Passung, Platzierung, Variantenbildung und frühe technische Plausibilisierung. |
| Zustand und Qualitätsstatus | Projekte mit tragendem oder sicherheitsrelevantem ReUse benötigen Zustandsangaben und Prüfpfade. | G3, K4 | Trennung zwischen „verfügbar“, „prüfbedürftig“, „eingeschränkt nutzbar“ und „nachgewiesen geeignet“. |
| Evidenzniveau | Die RSI-Auswertung zeigt starke Unterschiede zwischen Primärnachweis, Projektseite, Medienbericht und unvollständiger Dokumentation. | Evidenzmodell, Konfidenz, K3–K14 | Verhindert, dass schwach belegte Annahmen wie geprüfte Tatsachen behandelt werden. |
| Unsicherheitsniveau | Viele Angaben zu CO₂, Mengen, Scope, Kosten oder Nachweisstatus sind projektabhängig und unvollständig. | K14, K10, K8, Konfidenz | Macht frühe Entscheidung unter Unsicherheit möglich, ohne Überpräzision vorzutäuschen. |
| Prüfstatus | Strukturelle und regulatorische Einsetzbarkeit ist häufig der Engpass zwischen Bauteilfund und Wiederverwendung. | G3, K4 | Kennzeichnet technische Freigaben, offene Prüfbedarfe und fachliche Zuständigkeiten. |
| Verfügbarkeit und Timing | Rückbau- und Neubauzeitpunkte stimmen häufig nicht automatisch überein. | G5, K6, K8 | Verbindet Entwurf mit Rückbauzeitpunkt, Lagerdauer, Lieferfenster und Einbauplanung. |
| Lager- und Logistikstatus | Bauteile benötigen Demontage, Kennzeichnung, Transport, Lagerung und Aufbereitung. | G5, K6 | Verhindert, dass Bauteile als verfügbar erscheinen, obwohl Transport, Lager oder Aufbereitung ungeklärt sind. |
| Reservierungsstatus | ReUse scheitert, wenn Entwürfe auf Bauteilen beruhen, die nicht gesichert sind. | G2, K2, K7 | Ermöglicht Unterscheidung zwischen Suche, Option, Reservierung und beschaffbarer Komponente. |
| Umweltannahmen | Umweltvorteile hängen von Systemgrenzen, Transport, Aufbereitung, Lebensdauer und Substitution ab. | K14 | Unterstützt frühe ökologische Plausibilisierung mit transparenten Annahmen. |
| Strukturelle Plausibilität | Besonders bei Stahl, Beton, Holztragwerken und Fassadenteilen ist strukturelle Eignung nicht allein aus Geometrie ableitbar. | G3, K4, K9 | Führt Tragfähigkeits- und Anschlussfragen früh in die Entwurfsraumerkundung ein. |
| Verantwortungsrelevante Information | G4 ist im Korpus einer der häufigsten Blocker; technische Prüfung ersetzt keine Haftungs- oder Gewährleistungslogik. | G4, K5 | Macht Rollen, Zuständigkeiten und offene Risikoübergänge sichtbar. |
| Akteursrollen-Sichtbarkeit | ReUse-Projekte verknüpfen Bauherrschaft, Rückbau, Händler, Planende, Ingenieur:innen, Behörden und Prüfinstanzen. | K11, K12 | Unterstützt koordinierte Prozessketten und verhindert Informationsabbrüche zwischen Akteursgruppen. |
| Profilabhängige Ansichten | Temporäre Systeme, Fit-outs, tragende Komponenten und adaptive Selbstwiederverwendung benötigen unterschiedliche Daten- und Prüfintensitäten. | Profile, K13, K9 | Verhindert falsche Vergleichbarkeit und ermöglicht angemessene Workflows je ReUse-Profil. |
| Scope-Kennzeichnung | ReUse-Quoten vermischen häufig Gebäude-, Struktur-, Fassaden-, Innenausbau-, Recycling- und Retentionsanteile. | K10, K14 | Sichert Vergleichbarkeit und verhindert Überbewertung nicht vergleichbarer ReUse-Anteile. |
| Beschaffungsreife | Viele Projekte bleiben unterevidenziert, weil Ausschreibung, Kosten, Vertrag und Programm nicht publiziert sind. | G6, K7, K8 | Kennzeichnet, ob ein Bauteil oder Bauteilpaket planbar, ausschreibbar und terminlich integrierbar ist. |
| Entwurfsregel- und Anschlussinformation | ReUse erfordert nicht nur Bauteildaten, sondern Regeln der Kombination, Anpassung und Fügung. | K9, K4, K13 | Unterstützt Variantenbildung und vermeidet rein additive Bauteilsuche ohne konstruktive Logik. |

Diese Anforderungen bilden eine methodische Brücke zwischen Fallstudienanalyse und zukünftiger Systemgestaltung. Sie zeigen, welche Informationen ein technologisches Ökosystem tragen sollte, damit Wiederverwendung nicht nur beschrieben, sondern im Entwurf verantwortlich operationalisiert werden kann.

---

## 12. Synthese: Vom Fallbeispiel zur Ökosystemanforderung

Die Analyse der 74 Projekte führt von einzelnen ReUse-Fällen zu wiederkehrenden Systemanforderungen. Der zentrale Erkenntnisschritt besteht darin, ReUse nicht als isolierten Materialakt zu betrachten, sondern als Kette aus Daten, Nachweis, Verantwortung, Logistik, Beschaffung und Entwurf.

```text
74 ReUse-Projekte
        ↓
Fallstudienrecherche + Evidenzregister
        ↓
RSI-v6 Skalierbarkeitsanalyse
        ↓
Muster: Daten / Nachweis / Logistik / Beschaffung / Verantwortung / Entwurf
        ↓
Ökosystemanforderungen
        ↓
Datenmodell + Schnittstellen + Entwurfsintegration + Performance-Plausibilisierung + Unsicherheitskommunikation
        ↓
Technologisches ReUse-Ökosystem
```

Die 74 Projekte zeigen, dass Skalierbarkeit davon abhängt, reale Bauteile in vergleichbare, bewertbare und entwurfsrelevante Informationen zu übersetzen. Ein technologisches ReUse-Ökosystem sollte daher nicht nur Komponenten sichtbar machen. Es sollte ihren Status, ihre Unsicherheit, ihre Quelle, ihre technische Prüfbarkeit, ihre logistische Zeitlichkeit, ihre Verantwortungsbezüge und ihre Entwurfsanschlüsse erfassbar machen.

Für *Entwerfen mit Bestand* bedeutet dies: Der zukünftige technologische Beitrag liegt nicht allein in einem größeren Bauteilkatalog oder in automatisierter Variantenbildung. Der entscheidende Beitrag liegt in der Verbindung von **Bestandsdaten, Entwurfsoperation, Performance-Plausibilisierung und Evidenzkommunikation**. Erst dadurch können wiederverwendete Baukomponenten in frühen Entwurfsprozessen nicht nur gefunden, sondern verantwortbar ausgewählt, kombiniert, bewertet und weiterqualifiziert werden.

Damit wird aus der Fallstudienrecherche eine strategische Ökosystemanforderung: ReUse wird skalierbar, wenn reale, heterogene und unvollständige Bauteilbestände in einen gemeinsamen Informationsraum überführt werden, der Entwurf, Nachweis, Logistik, Beschaffung und Verantwortung zugleich berücksichtigt.
