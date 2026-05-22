# Struktur als Präsentationsfluss

Durch diese Datei wird die aktuelle Gliederungsstruktur von `plattform/entwurf` wie durch eine Präsentation geführt. Jeder Punkt wird als erzählter Argumentationsschritt formuliert, damit nicht nur eine Beschreibung der Struktur, sondern ein nachvollziehbarer Ablauf gelesen werden kann.

## 00 Systemarchitektur

Es wird mit dem Gesamtsystem begonnen: einer Plattform, in der reale Stahlbetonressourcen für die Wiederverwendung in nutzbare Entwurfsintelligenz übersetzt werden. Dabei wird deutlich gemacht, dass nicht nur eine Inventarisierung gemeint ist, sondern ein Arbeitsfluss von unsicheren Bestandsbauteilen zu bewerteten Entwurfsvarianten.

## 1 Schnittstelle 1 - Einspeiseplattform

Zunächst wird die Seite des Systems betreten, auf der reale Bauteile ankommen: Fotos, digitale Aufnahmen, Angebote, grobe Maße und unvollständiges Wissen. Die Unordnung des Wiederverwendens wird hier in eine erste strukturierte Sprache übersetzt.

### 1.1 Bauteil-Seed

Der Bauteil-Seed wird als kleinste sinnvolle Starteinheit des Systems eingeführt. Er wird noch nicht als geprüftes Produkt oder fertiger Bauteilpass verstanden, sondern als Datensatz, der präzise genug ist, damit durch den Generator weitergearbeitet werden kann.

#### 1.1.1 Eingabeprozess

Es wird gezeigt, wie ein reales Bauteil praktisch in die Plattform aufgenommen wird. Eine kurze Beschreibung, ein Foto, eine digitale Aufnahme oder ein importiertes Angebot können dafür ausreichen, ohne dass bereits vollständige technische Unterlagen vorausgesetzt werden müssen.

##### 1.1.1.1 Nutzereingabe

Die Präsentation wird hier konkretisiert: Zum Beispiel werden 18 Stahlbeton-Wandplatten aus einem Rückbau beschrieben, grob vermessen und als mögliche raumbildende oder tragende Elemente eingeordnet. Durch diese menschliche Eingabe wird dem Bildmaterial Kontext hinzugefügt, der aus einem Foto allein nicht zuverlässig abgeleitet werden kann.

##### 1.1.1.2 Schnittstelle / Import aus Bauteilbörse

Der Einstieg wird anschließend über die manuelle Eingabe hinaus erweitert, indem Daten aus Bauteilbörsen einbezogen werden. Angebotsdaten, Verfügbarkeitsstatus, Quellenangaben und Mengen können dadurch Teil des Seeds werden, ohne dass alles manuell übertragen werden muss.

#### 1.1.2 Bedienkonzept

Es wird erklärt, wie durch die Oberfläche ein niedriger Einstieg ermöglicht und trotzdem Nachvollziehbarkeit erzeugt wird. Schnelles Arbeiten wird zugelassen, während Korrekturen, Annahmen und fehlende Nachweise sichtbar gehalten werden.

##### 1.1.2.1 Minimale Eingabe

Es wird betont, dass zu Beginn keine vollständige technische Akte verlangt wird. Wenige Eingaben reichen aus, weil Wiederverwendungsentwürfe häufig begonnen werden, bevor Pläne, Prüfungen und Zertifikate vollständig vorliegen.

##### 1.1.2.2 KI-Erkennung

Es wird gezeigt, was aus Bild und Text abgeleitet werden kann: Typologie, grobe Maße, Materialfamilie, Zustand, Öffnungen, Kanten, Schäden oder mögliche Rollen. Dabei wird die KI als Vorschlagsinstanz verstanden und nicht als endgültige Autorität.

##### 1.1.2.3 Formularoberfläche

Im nächsten Schritt werden die vorgeschlagenen Daten bestätigt, verändert oder ergänzt. Aus einer Erkennung wird dadurch ein geprüfter Seed, statt dass eine unkontrollierte Annahme stehen bleibt.

##### 1.1.2.4 Nachweisbereich

Die Evidenzebene wird früh eingeführt, bevor der Entwurf zu sicher wirkt. Im Nachweisbereich werden Fotos, Dokumente, Materialpassinformationen, Prüfstatus und Lücken wie Bewehrungslage, Betondruckfestigkeit, Brandschutz oder Schadstoffe sichtbar gemacht.

#### 1.1.3 Bauteil-Daten

Nachdem die Eingabelogik geklärt ist, wird betrachtet, was im Seed tatsächlich enthalten ist. Dabei wird sichtbar gemacht, welche Informationen direkt eingegeben wurden und welche abgeleitet sind, weil im Wiederverwendungsentwurf zwischen Wissen und Schätzung unterschieden werden muss.

##### 1.1.3.1 Mindestdaten zum Entwerfen

Es werden die Mindestinformationen benannt, bevor ein Bauteil in einer Entwurfsvariante getestet werden kann: Typologie, Menge, Hauptmaße, Material, Quelle, Verfügbarkeit, Zustand, Zielrolle und Datenvertrauen. Dadurch wird die Schwelle zwischen einer vagen Wiederverwendungschance und einem planbaren Objekt markiert.

##### 1.1.3.2 Abgeleitete / angereicherte Daten

Es wird gezeigt, wie der Seed mit berechneten oder geschätzten Planungswerten angereichert wird. Masse, Fläche, Volumen, thermische Relevanz, mögliche Spannrichtung, CO₂-Abschätzung und fehlende Nachweise machen das Bauteil nutzbarer, werden aber weiterhin als vorläufige Angaben erkennbar gehalten.

#### 1.1.4 Ausgabe Bauteil-Seed

Die erste Schnittstelle wird mit einem kompakten, generatorfähigen Seed abgeschlossen. Aus einer groben realen Ressource ist damit eine strukturierte Planungsgrundlage geworden.

##### 1.1.4.1 Seed-Kennung + Typologie + Menge + Geometriehinweis + Material + Quelle + Verfügbarkeit + Zielrolle

Die Nutzlast des Seeds wird hier gebündelt: Identität, Typologie, Menge, Geometriehinweis, Material, Quelle, Verfügbarkeit und Zielrolle. Zugleich werden Unsicherheit und Evidenzstatus mitgeführt, damit spätere Entscheidungen nachvollziehbar bleiben.

### 1.2 Generator

Nun wird von der Einspeisung zur Transformation übergeleitet. Der Seed wird durch den Generator in Planungsebenen übersetzt, durch die ein Bauteil suchbar, platzierbar, verbindbar und prüfbar wird.

#### 1.2.1 Rolle des Generators

Der Generator wird als Übersetzungsschicht zwischen unordentlichem Bestand und Entwurfslogik gerahmt. Es wird kein Bauteil zertifiziert, sondern ein erstes nutzbares Planungsobjekt erzeugt.

##### 1.2.1.1 Konzept

Das Konzept wird an einem Beispiel verständlich gemacht: Aus einem Wandplatten-Seed werden Geometrie, Masse, mögliche Auflager, Anschlusspunkte, fehlende Nachweise und CO₂-Annahmen erzeugt. Dadurch wird gezeigt, dass nicht nur eine 3D-Form, sondern ein Planungsmodell entsteht.

##### 1.2.1.2 Grammatiklogik

Es wird erklärt, warum ein einziger generischer Generator nicht ausreicht. Für Hohlkörperdecken, Stützen, Träger, Wandplatten, Treppen und Ortbeton-Zuschnitte werden jeweils eigene geometrische und semantische Regeln benötigt.

#### 1.2.2 Klassifikationslogik

Die Klassifikationsleiter des Systems wird eingeführt. Typologie, Generatorgrammatik, Typ und Einzelstück werden als vier Ebenen verstanden, durch die Entwurfssprache und physische Realität verbunden werden.

##### 1.2.2.1 Typologie

Mit der Typologie wird die breite Bauteilfamilie benannt: Decke, Träger, Stütze, Wand, Platte, Treppe, Fassaden-Sandwichelement oder ähnliche Kategorien. Durch diese erste Bezeichnung wird festgelegt, welche Grammatik und welche Planungsfragen folgen.

##### 1.2.2.2 Generatorgrammatik

Von der breiten Familie wird zur konkreten Erzeugungslogik übergeleitet. Durch einen Hohlkörperdecken-Generator und einen Stahlbeton-Wandplatten-Generator werden zwar beide Male Stahlbetonobjekte erzeugt, aber unterschiedliche Fragen gestellt und unterschiedliche Planungsmodelle aufgebaut.

##### 1.2.2.3 Typ

Der Typ wird als Ebene eingeführt, auf der Wiederholung und Pakete sichtbar werden. Eine Gruppe wie "Hohlkörperdecke 7,20 m x 1,20 m aus Spendergebäude A" kann dadurch Raster, Mengen und wiederholbare Entwurfsentscheidungen tragen.

##### 1.2.2.4 Einzelstück

Schließlich wird beim physischen Einzelbauteil gelandet. Herkunft, Zustand, Verfügbarkeit, Nachweise und Unsicherheit werden hier am konkreten Bauteil und nicht nur an einer abstrakten Kategorie geführt.

#### 1.2.3 Bauteil-Seed -> generiertes Bauteilobjekt

An diesem Punkt wird der Seed zu einem generierten Bauteilobjekt mit mehreren parallelen Planungsebenen. Es wird deutlich gemacht, dass Geometrie, Struktur, Energie, Semantik und Evidenz gemeinsam entstehen und nicht als isolierte Dokumente behandelt werden.

##### 1.2.3.1 Geometrisches Planungsmodell

Zuerst wird dem generierten Objekt eine saubere geometrische Darstellung gegeben. Dadurch kann das Bauteil in Zeichnungen oder Modellen erscheinen, auch wenn die reale Ausgangsinformation nur aus einem Foto, Angebot oder groben Maß besteht.

##### 1.2.3.2 Abstraktes Strukturmodell

Danach wird eine strukturelle Abstraktion ergänzt: Achsen, Auflager, Spannrichtung, Lastabtrag und mögliche Rolle. Es wird kein statischer Nachweis ersetzt, aber die zugrunde liegende Tragwerksfrage wird sichtbar gemacht.

##### 1.2.3.3 Abstraktes Energiemodell

Als Nächstes werden energetische und klimatische Aspekte ergänzt: Masse, Flächen, thermische Wirkung, Hüllenrisiko und CO₂-Abschätzung. Wiederverwendung wird dadurch nicht nur nach Materialverfügbarkeit beurteilt, sondern auch nach Betriebsenergie, Transport und Klimaeffekt.

##### 1.2.3.4 Semantisches Modell

Die Semantik wird über Anschlusspunkte, Verbindungselemente, erlaubte Rollen und mögliche Beziehungen eingeführt. Das Bauteil wird dadurch mehr als Geometrie, weil seine möglichen Verbindungen zu anderen Bauteilen lesbar werden.

##### 1.2.3.5 Evidenzverknüpfung

Zum Schluss wird jedes generierte Objekt mit seiner Quelle verbunden gehalten. Fotos, Angebote, Dokumente, Vertrauen, fehlende Nachweise und Verfügbarkeit werden mitgeführt, damit das digitale Modell den Kontakt zum realen Bauteil nicht verliert.

## 2 Schnittstelle 2 - Entwurfswerkzeug

Die zweite Schnittstelle wird begonnen, sobald generierte Objekte für den Entwurf bereitstehen. Der Fokus wird von der Frage, wie ein Bauteil ins System kommt, zur Frage verschoben, wie es Teil eines architektonischen Vorschlags wird.

### 2.1 Bauteilkatalog

Der Bauteilkatalog wird als erste entwurfsseitige Ebene eingeführt. Generierte Bauteile werden hier als auswählbare Entwurfsbausteine sichtbar und nicht mehr nur als rohe Angebote.

#### 2.1.1 Bauteilkarte

In ein einzelnes Katalogobjekt wird nun hineingezoomt: die Bauteilkarte. Reales Foto, generierte Geometrie, Daten, Reifegrad und Prüfstatus werden verbunden, damit entschieden werden kann, ob ein Bauteil weiter getestet werden sollte.

##### 2.1.1.1 Visuelle Ebene

Die visuelle Ebene wird genutzt, um das Bauteil auf einen Blick lesbar zu machen. Bei Stahlbeton werden Oberfläche, Kanten, Schäden, Öffnungen, Schnittflächen, Spannrichtung und sauberes Modell nebeneinander sichtbar gemacht.

##### 2.1.1.2 Datenebene

Danach werden die Planungsdaten gezeigt: Typologie, Typ, Einzelstück-Kennung, Menge, Maße, Materialfamilie, Quelle, Standort, Verfügbarkeit, Zielrolle und Datenvertrauen. Aus einem Bild wird dadurch ein Entscheidungsobjekt.

##### 2.1.1.3 Reifegrad

Es wird gezeigt, dass nicht jedes interessante Bauteil gleich weit ist. Ein Bauteil kann als Idee, entwurfsfähig, prüfbedürftig, ausschreibungsnah oder einbaufähig eingeordnet werden, ohne dass diese Stufen eingeebnet werden.

##### 2.1.1.4 Prüfstatus

Durch den Prüfstatus werden technische Lücken sichtbar gemacht. Bei Stahlbeton betrifft das Geometrie, Bewehrung, Betondruckfestigkeit, Auflager, Brandschutz, Schadstoffe und frühere Nutzung.

#### 2.1.2 Filterstruktur

Nach der Bauteilkarte wird erklärt, wie der Katalog durchsucht wird. Die Filter werden nicht als Einkaufskategorien, sondern als Entwurfsfragen nach Passung, Rolle, Risiko, Zeit, Evidenz und Umweltwirkung verstanden.

##### 2.1.2.1 Typologie / Typ

Zuerst kann nach Typologie und Typ gefiltert werden, um passende Bauteilfamilien zu finden. Wiederholbare Decken, Wandplatten, Träger, Stützen oder Bauteilpakete werden dadurch als Ressource sichtbar.

##### 2.1.2.2 Geometrie

Danach wird der Ressourcenpool durch Geometrie eingegrenzt: Maße, Raster, Spannweite, Öffnungen, Tiefe oder Geschosshöhe. Übrig bleiben Bauteile, die physisch am geplanten System teilnehmen können.

##### 2.1.2.3 Funktion

Durch die Funktion wird die Frage von "was ist es" zu "was kann es hier leisten" verschoben. Je nach Entwurfsziel kann ein Bauteil tragend, raumbildend, hüllend, ausbauend, fassadenbildend oder ästhetisch wirksam werden.

##### 2.1.2.4 Semantik / Kompatibilität

Bei der Kompatibilität wird gefragt, ob Bauteile sinnvoll verbunden werden können. Anschlusspunkte und Verbindungselemente werden deshalb nicht nur nach Größe, sondern nach möglichen Beziehungen gefiltert.

##### 2.1.2.5 Tragwerk

Durch den Tragwerksfilter werden mögliche tragende Rollen und fehlende statische Daten gezeigt. Bauteile für frühe Layoutstudien werden dadurch von Bauteilen unterschieden, die zuerst ernsthaft ingenieurmäßig geprüft werden müssen.

##### 2.1.2.6 Energie

Durch den Energiefilter werden Hüllenrolle, thermische Masse, U-Wert-Annahmen und Betriebsenergie-Risiko in den frühen Entwurf gebracht. Das ist wichtig, weil ein wiederverwendetes Stahlbetonbauteil in einer Rolle sinnvoll und in einer anderen problematisch sein kann.

##### 2.1.2.7 Verfügbarkeit / Menge

Durch Verfügbarkeit und Menge wird der Katalog zurück in die Realität geholt. Ein Entwurf mit 35 Deckenplatten funktioniert nur, wenn genau diese Bauteile rechtzeitig und als zusammenhängendes Paket verfügbar sind.

##### 2.1.2.8 Risiko / Nachweise

Durch Risiko und Nachweise wird gezeigt, welche Bauteile offene technische oder rechtliche Fragen tragen. Unsicherheiten werden dadurch nicht versteckt, sondern bewusst bearbeitbar gemacht.

##### 2.1.2.9 CO₂ / Transport

Durch CO₂ und Transport wird die ökologische Abwägung ergänzt. Der Wert von Wiederverwendung wird nicht nur vom vermiedenen Neubaumaterial abhängig gemacht, sondern auch von Masse, Distanz, Logistik und Zusatzaufwand.

#### 2.1.3 Katalog-Aktionen

Wenn passende Bauteile gefunden sind, müssen im Katalog Handlungen ermöglicht werden. Durch die Aktionen wird vom Vergleichen über das Platzieren bis zur realen Reservierung oder Anfrage geführt.

##### 2.1.3.1 Auswählen / Vergleichen

Zuerst werden Bauteile oder Pakete nach Geometrie, Rolle, Risiko, Reifegrad, Verfügbarkeit und CO₂ verglichen. Aus einer interessanten Ressource wird dadurch eine bewusste Entwurfsentscheidung.

##### 2.1.3.2 Platzieren im Entwurfsraum

Danach wird das ausgewählte Bauteil aus dem Katalog in den Entwurfsraum übergeben. Ab diesem Moment wird es nicht mehr isoliert bewertet, sondern als Teil eines Systems getestet.

##### 2.1.3.3 Reservieren / Anfrage an Bauteilbörse

Zum Schluss kann vom Entwurf wieder zur realen Quelle zurückgegriffen werden, etwa durch Reservierung oder Anfrage. So wird die Schleife zwischen spekulativem Entwerfen und tatsächlicher Materialverfügbarkeit geschlossen.

### 2.2 Entwurfsraum

Der Entwurfsraum wird als Moment gezeigt, in dem aus der Präsentation eine Komposition wird. Einzelne Bauteile für die Wiederverwendung werden hier als Variante mit Regeln, Warnungen, Systemlogik und Rückmeldung getestet.

#### 2.2.1 Idee + Komposition

Im Entwurfsraum wird mit einer Absicht begonnen: einer wiederverwendungsreichen Tragstruktur, einer Fassadenstrategie, einem Deckenraster oder einem hybriden System. Bauteile aus dem Katalog werden nun nicht mehr als Einträge, sondern als Zutaten eines Entwurfs verstanden.

##### 2.2.1.1 Zielentwurf

Durch den Zielentwurf werden die Spielregeln festgelegt: Nutzung, Gebäudetyp, Wiederverwendungsziel, Tragwerksstrategie, Raster, Energieansatz und Projektanforderungen. Ohne dieses Ziel kann nicht beurteilt werden, ob die ausgewählten Bauteile wirklich passen.

##### 2.2.1.2 Kombination mehrerer Bauteile

Danach wird gezeigt, wie mehrere Bauteile zu einem System kombiniert werden. Eine Hohlkörperdecke wird dabei etwa mit Trägern, Auflagern, Spannweite, Menge, Verbindungslösung und fehlenden Nachweisen abgeglichen.

#### 2.2.2 Kompatibilitätsprüfung

Nun wird mit der Bewertung des Vorschlags begonnen. Kompatibilität wird nicht auf kollisionsfreie Geometrie reduziert, sondern über Regeln, Energie, Tragwerk, reale Verfügbarkeit und semantische Verbindung geprüft.

##### 2.2.2.1 Regelquellen

Durch die Regelquellen wird erklärt, woher die Rückmeldung kommt. Normen, Projektziele, energetische Kriterien, Tragwerkslogik, Logistik, Verfügbarkeit und semantische Verbindungsregeln werden miteinander kombiniert.

###### 2.2.2.1.1 Regelbasiert

Bei regelbasierten Prüfungen wird der Entwurf mit Normen, Zielwerten und Projektanforderungen verglichen. Dabei wird entschieden, ob etwas grundsätzlich zulässig, prüfbedürftig oder ausgeschlossen ist.

###### 2.2.2.1.2 Energetisch

Bei energetischen Prüfungen wird gefragt, ob die Wiederverwendungsstrategie thermisch und betrieblich funktioniert. Eine Wandplatte kann innen unkritisch sein, aber als Außenhülle ohne zusätzliche Schichten problematisch werden.

###### 2.2.2.1.3 Tragwerklich

Bei tragwerklichen Prüfungen wird gefragt, ob Lastabtrag, Auflager, Spannweiten und Anschlussannahmen plausibel sind. Lose Montageideen werden dadurch in Fragen übersetzt, die später ingenieurmäßig geprüft werden können.

###### 2.2.2.1.4 Realwelt-basiert

Durch Realwelt-Prüfungen wird der Entwurf an Logistik und Verfügbarkeit gebunden. Eine schöne Wiederverwendungsvariante wird schwach, wenn Bauteile nicht rechtzeitig beschafft, gelagert, transportiert oder reserviert werden können.

###### 2.2.2.1.5 Semantisch

Bei semantischen Prüfungen wird gefragt, ob die gewählten Anschlusspunkte und Verbindungselemente sinnvoll aufeinandertreffen. Eine bloße räumliche Berührung wird so von einem echten Auflager-, Öffnungs-, Fassaden- oder Bodenanschluss unterschieden.

#### 2.2.3 Entwurfsrückmeldung

Aus der Kompatibilitätslogik wird hier ein Entwurfsgespräch gemacht. Statt auf einen Abschlussbericht zu warten, wird während der Variantenbildung gewarnt, bewertet und vorgeschlagen.

##### 2.2.3.1 Direktwarnungen

Direktwarnungen werden angezeigt, sobald der Entwurf riskant oder unvollständig wird. Fehlende Nachweise, Zeitprobleme, riskante Verbindungen, unzureichende Mengen und geringes Datenvertrauen werden sofort sichtbar gemacht.

###### 2.2.3.1.1 Fehlende Nachweise

Durch Warnungen zu fehlenden Nachweisen wird gezeigt, wo der Entwurf noch auf Annahmen beruht. Bei Stahlbeton betrifft das häufig Bewehrung, Betondruckfestigkeit, Brandschutz, Schadstoffe, Auflager oder Anschlussdetails.

###### 2.2.3.1.2 Zeitkonflikte

Durch Zeitwarnungen wird gezeigt, wenn Rückbau, Lagerung, Transport, Reservierung und Planungsphase nicht zusammenpassen. Das ist zentral, weil Bauteile für die Wiederverwendung oft nur in engen Zeitfenstern verfügbar sind.

###### 2.2.3.1.3 Riskante Verbindungen

Durch Warnungen zu riskanten Verbindungen werden Anschlüsse markiert, die möglich aussehen, aber noch nicht belastbar sind. Beispiele sind unklare Auflager, fehlende Verbindungselemente, unpassende Spannweiten oder ungeprüfter Lastabtrag.

###### 2.2.3.1.4 Unvollständige Mengen

Durch Mengenwarnungen wird gezeigt, wenn im Entwurf mehr Bauteile benötigt werden, als verfügbar sind. Das System kann dann zu hybriden Ergänzungen, kleineren Varianten, anderem Raster oder anderer Paketlogik führen.

###### 2.2.3.1.5 Risiko / Datenvertrauen

Durch Risiko und Datenvertrauen wird erklärt, wie sicher die Informationen hinter einer Entscheidung sind. So kann weiter entworfen werden, ohne dass behauptet wird, jedes Bauteil sei schon vollständig bewiesen.

##### 2.2.3.2 Visuelle Statuslogik

Durch die visuelle Statuslogik werden komplexe Prüfungen in lesbare Zustände übersetzt. Mit Grün, Gelb, Orange, Rot und Grau wird gezeigt, ob eine Variante vielversprechend, unsicher, riskant, blockiert oder datenarm ist.

##### 2.2.3.3 Variantenbewertung

Mit der Variantenbewertung wird ein Schritt zurückgetreten und der gesamte Vorschlag beurteilt. Es wird gefragt, ob das System kohärent, ressourcenschonend, CO₂-arm, verfügbar und noch anpassbar ist.

###### 2.2.3.3.1 Wiederverwendungsanteil

Durch den Wiederverwendungsanteil wird gezeigt, wie viel des Entwurfs tatsächlich von wiederverwendeten Bauteilen getragen wird. Er kann nach Stückzahl, Masse, Fläche oder funktionaler Rolle gelesen werden.

###### 2.2.3.3.2 CO₂-Vergleich

Durch den CO₂-Vergleich wird der Variante ein ökologisches Gegenbild gegeben. Es wird gezeigt, wie die Wiederverwendungsoption gegenüber einer konventionellen Neubaustrategie abschneidet, während Annahmen sichtbar bleiben.

###### 2.2.3.3.3 System-Kompatibilität

Bei der System-Kompatibilität wird gefragt, ob die ausgewählten Bauteile als architektonisches und konstruktives System funktionieren. Eine Variante kann gute Einzelteile enthalten und trotzdem scheitern, wenn Raster, Auflager, Mengen oder Semantik nicht zusammenpassen.

###### 2.2.3.3.4 Regelbasierte Alternativvorschläge

Wenn Probleme auftreten, sollen nicht nur Warnungen, sondern Alternativen angeboten werden. Andere Bauteile, ein anderes Raster, neue Ergänzungsteile oder eine veränderte Verbindungsstrategie können vorgeschlagen werden.

###### 2.2.3.3.5 Umgang mit unvollständigen Mengen

Unvollständige Mengen werden als Entwurfsproblem behandelt und nicht nur als Fehler. Strategien wie hybride Ergänzung, Umverteilung, reduzierter Umfang oder neue Paketlogik können aufgezeigt werden.

#### 2.2.4 Export

Die Erzählung endet mit dem Export: einer dokumentierten Entwurfsvariante und keinem fertigen Ausführungspaket. Entwurfsidee, Bauteilliste, Evidenzlücken, Prüfpfade, Wiederverwendungsanteil und CO₂-Bewertung werden in die nächste Phase mitgenommen.

##### 2.2.4.1 Entwurfsvariante + Bauteilliste + offene Nachweise + Prüfpfade + Auswertung zu Wiederverwendung und CO₂

In der finalen Ausgabefassung wird dem nächsten Team gezeigt, was entworfen wurde, von welchen realen Bauteilen es abhängt und was noch geprüft werden muss. Dadurch wird der Entwurfswert der Wiederverwendungsidee erhalten, ohne dass ihre Unsicherheiten versteckt werden.
