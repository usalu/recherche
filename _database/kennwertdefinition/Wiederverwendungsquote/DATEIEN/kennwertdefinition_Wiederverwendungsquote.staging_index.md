---
id: "Wiederverwendungsquote"
entity: "kennwertdefinition"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Wiederverwendungsquote"
legacy_type: "Kennwert"
legacy_paths:
  - "kennwert\Wiederverwendungsquote.md"
target_primary: "kennwertdefinition/Wiederverwendungsquote"
target_secondary: ""
risk_flags: ""
---
# Wiederverwendungsquote

## Migration

- Target: kennwertdefinition/Wiederverwendungsquote
- Legacy source count: 1
- Legacy types: Kennwert
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: kennwert\Wiederverwendungsquote.md

---
type: Kennwert
dokument: ["[[dokument/LCA]]"]
methode: ["[[methode/ReUse_Assessment]]"]
verwandt: ["[[kennwert/CO2_Einsparung]]", "[[kennwert/Demontagegrad]]", "[[kennwert/Graue_Energie]]", "[[kennwert/Materialwert]]"]
---

# Wiederverwendungsquote

## Verknüpfungen

- **Übergeordnete Themen:** Kennwerte; Kreislaufwirtschaft; Ressourceneffizienz; Bestandserhalt; selektiver Rückbau; zirkuläre Beschaffung; Entwerfen mit Bestand.
- **Verwandte Dateien:** `kennwert/Demontagegrad.md`; `kennwert/Materialwert.md`; `kennwert/CO2_Einsparung.md`; `kennwert/Graue_Energie.md`; `methode/ReUse_Assessment.md`; `dokument/LCA.md`; `datenmodell/`; `wirtschaft/`; `standard/`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Level(s) Indikator 2.1 „Bill of quantities“ und 2.2 „Construction and demolition waste“; DIN SPEC 91484; EU Construction & Demolition Waste Management Protocol; Waste Framework Directive; DGNB Building Resource Passport; Madaster Circularity Indicator; Urban Mining Index; K.118 Winterthur; UMAR / NEST; Rotor; Concular; Bauteilbörse; Materialpass; Rückbauinventar; Massenbilanz; Stücklistenbilanz; CO2-gewichtete Quote.

## Kurzdefinition

**Wiederverwendungsquote** bezeichnet den Anteil von Bauteilen, Bauprodukten oder Materialien, die in gleicher oder vergleichbarer Funktion erneut verwendet werden, bezogen auf eine definierte Gesamtmenge. Sie kann als Masse, Volumen, Fläche, Stückzahl, Wert, CO2-Wirkung oder Bauteilanzahl angegeben werden.

Der Kennwert ist nur aussagekräftig, wenn klar benannt wird:

- ob die Quote **inputbezogen** oder **outputbezogen** ist;
- ob **Bauteilwiederverwendung** oder auch Recycling zählt;
- welche Einheit genutzt wird;
- welche Systemgrenze gilt;
- ob geplante oder tatsächlich realisierte Wiederverwendung gemessen wird.

Grundformel:

```text
Wiederverwendungsquote = wiederverwendete Menge / betrachtete Gesamtmenge
```

Ohne Definition von Zähler, Nenner und Einheit ist die Quote nicht vergleichbar.

## Relevanz für Wiederverwendung im Bauwesen

Die Wiederverwendungsquote ist ein leicht kommunizierbarer Kennwert, aber methodisch anfällig. Sie zeigt, wie stark ein Projekt, Rückbau oder Gebäude tatsächlich in Kreisläufen arbeitet. Für ReUse-Forschung und Praxis ist sie wichtig, weil sie den Übergang von Einzelfallbeispielen zu messbaren Anforderungen ermöglicht.

Sie dient:

- als Zielwert in Ausschreibungen und Wettbewerben;
- als Monitoring-Kennwert für Rückbau und Neubau;
- als Grundlage für Zertifizierung, ESG und Ressourcenpässe;
- zur Bewertung von Urban-Mining-Potenzialen;
- zur Erfolgskontrolle von ReUse-Plattformen;
- zur Verbindung von Materialdaten, CO2-Bilanz und Wirtschaftlichkeit.

Gleichzeitig kann eine hohe Wiederverwendungsquote irreführen. Eine massenbezogene Quote wird von schweren Bauteilen dominiert; eine stückzahlbezogene Quote kann leichte Kleinteile überbewerten; eine wertbezogene Quote bevorzugt teure Bauteile; eine CO2-gewichtete Quote bevorzugt emissionsintensive Produkte. Deshalb sollte die Einheit bewusst gewählt und möglichst ergänzend berichtet werden.

## Fachinhalt

### Haupttypen der Wiederverwendungsquote

#### 1. Inputbezogene Wiederverwendungsquote

Misst den Anteil wiederverwendeter Bauteile an allen im neuen oder umgebauten Projekt eingebauten Bauteilen.

```text
Quote_Input = Menge wiederverwendeter eingebauter Bauteile / Gesamtmenge eingebauter Bauteile
```

Anwendung: Neubau, Umbau, Innenausbau, öffentliche Beschaffung.

Beispiel: 25 % der Fassadenfläche stammen aus wiederverwendeten Elementen.

#### 2. Outputbezogene Wiederverwendungsquote

Misst den Anteil ausgebauter Bauteile, der aus einem Rückbau- oder Umbauprojekt tatsächlich wiederverwendet wird.

```text
Quote_Output = Menge tatsächlich wiederverwendeter ausgebauter Bauteile / Gesamtmenge rückgebauter Bauteile
```

Anwendung: selektiver Rückbau, Pre-demolition Audit, Abfallvermeidung.

Beispiel: 10 % der ausgebauten Innenausbauelemente werden als Bauteile weiterverkauft oder direkt in ein anderes Projekt eingebaut.

#### 3. Erhaltungsquote / In-situ-Wiederverwendungsquote

Misst, welcher Anteil vorhandener Bauteile im Gebäude verbleibt und weiter genutzt wird.

```text
Quote_Erhalt = Menge weitergenutzter Bestandsbauteile / Menge vorhandener Bestandsbauteile vor Eingriff
```

Anwendung: Umbau, Sanierung, Bestandserhalt, Entwerfen mit Bestand.

Diese Quote ist besonders wichtig, weil die hochwertigste Wiederverwendung oft die **Nicht-Demontage** ist: Erhalt in situ vermeidet Rückbau, Transport, Lagerung und Wiedereinbau.

#### 4. Angebots- oder Potenzialquote

Misst, welcher Anteil eines Bestands bei Erfassung als potenziell wiederverwendbar eingestuft wird.

```text
Quote_Potenzial = Menge potenziell wiederverwendbarer Bauteile / betrachtete Bestandsmenge
```

Diese Quote ist keine Erfolgsquote, sondern ein Planungsindikator. Sie muss später mit tatsächlicher Wiederverwendung abgeglichen werden.

#### 5. CO2-gewichtete Wiederverwendungsquote

Misst den Anteil der vermiedenen oder adressierten Klimawirkung statt der reinen Masse.

```text
Quote_CO2 = GWP der wiederverwendeten/substituierten Bauteile / GWP aller betrachteten Bauteile im Referenzszenario
```

Sie ist für Klimaziele aussagekräftiger als Masse, aber methodisch stärker von LCA-Daten und Baseline abhängig.

### Abgrenzung zu Recyclingquote und Verwertungsquote

Wiederverwendung bedeutet, dass ein Produkt oder Bauteil erneut genutzt wird, ohne dass es zu einem Rohstoff zurückgeführt wird. Recycling bedeutet stoffliche Aufbereitung zu Sekundärrohstoffen oder neuen Produkten. Energetische Verwertung bedeutet Nutzung des Energieinhalts, z. B. Verbrennung.

Die EU-Abfallpolitik verwendet teilweise kombinierte Ziele für Vorbereitung zur Wiederverwendung, Recycling und sonstige stoffliche Verwertung. Diese Ziele dürfen nicht als reine Wiederverwendungsquote interpretiert werden. Gerade im Bausektor können hohe Verwertungsquoten vor allem durch mineralisches Recycling entstehen, während Bauteilwiederverwendung gering bleibt.

### Einheiten

| Einheit | Vorteil | Risiko |
|---|---|---|
| Masse | einfach, kompatibel mit Abfallstatistik | schwere mineralische Stoffe dominieren |
| Volumen | relevant für Lager und Transport | niedrige Aussage zu Umweltwirkung |
| Fläche | gut für Fassaden, Böden, Ausbau | nicht materialübergreifend vergleichbar |
| Stückzahl | geeignet für Türen, Fenster, Leuchten | Kleinteile können übergewichtet werden |
| Materialwert | ökonomisch relevant | Marktpreise volatil |
| CO2e | klimawirksam | abhängig von LCA-Methode und Referenz |
| Bauteilgruppenquote | fachlich differenziert | komplexer zu berichten |

Für Forschung und Planung empfiehlt sich eine Kombination aus Massenquote, bauteilgruppenspezifischer Quote und CO2-gewichteter Wirkung.

### Typische Datenquellen

- Level(s) 2.1 Bill of Quantities: Materialmengen und Lebensdauern.
- Level(s) 2.2 Construction and Demolition Waste: Bau- und Abbruchabfallmengen.
- Rückbauinventare und Pre-demolition Audits.
- DIN SPEC 91484-Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten.
- BIM-Modell und Bauteillisten.
- Materialpass / Gebäuderessourcenpass.
- Lieferscheine, Wiegescheine, Entsorgungsnachweise.
- ReUse-Plattformdaten und Verkaufsnachweise.
- Montage- und Abnahmeprotokolle.
- LCA-Datenbanken für CO2-gewichtete Quoten.

### Mindestanforderungen an die Dokumentation

Eine Wiederverwendungsquote sollte immer angeben:

- Projektphase: Planung, Rückbau, Einbau, Abschluss.
- Quoteart: Input, Output, Erhalt, Potenzial, CO2-gewichtet.
- Einheit und Bezugsgröße.
- betrachtete Bauteilgruppen.
- Ausschlüsse, z. B. Erdreich, Aushub, technische Anlagen, Möbel.
- Umgang mit Verschnitt, Bruch, Ausschuss und Lagerverlusten.
- Definition von „wiederverwendet“.
- Nachweisquelle: geplant, ausgeschrieben, geliefert, eingebaut, verkauft oder geprüft.
- Bezug zu Recycling und Entsorgung.

### Anwendung im ReUse Assessment

In `methode/ReUse_Assessment.md` sollte die Wiederverwendungsquote nicht allein als Erfolgskennwert stehen. Sinnvoll ist ein Kennwertsatz:

- Potenzialquote aus Voruntersuchung.
- Demontagefähigkeitsquote.
- geplante ReUse-Quote.
- realisierte ReUse-Quote.
- Ausschussquote.
- CO2-Wirkung je Quote.
- Netto-Materialwert je Quote.

So kann sichtbar werden, wo ReUse verloren geht: im Bestand, bei Demontage, in der Lagerung, in der Planung, in der Zulassung oder auf dem Markt.

## Praxisbezug / Beispiele

- **Bestandserhalt im Umbau:** Wenn Tragstruktur, Fassade oder Innenausbau weiter genutzt werden, kann die Erhaltungsquote die wichtigste ReUse-Quote sein. Sie sollte getrennt von extern zugekauften ReUse-Bauteilen ausgewiesen werden.
- **K.118 Winterthur:** Das Projekt wird oft über CO2- und Materialeinsparungen kommuniziert. Für eine Wiederverwendungsquote müsste zusätzlich klar sein, welche Bezugsgröße gilt: Masse der neuen Aufstockung, Bauteilgruppen, Materialwert oder CO2-Wirkung.
- **UMAR / NEST:** Das Projekt zeigt, dass hohe künftige Wiederverwendungsfähigkeit nicht mit aktueller Wiederverwendungsquote verwechselt werden darf. Ein Gebäude kann heute aus neuen, aber vollständig demontierbaren Komponenten bestehen und damit eine hohe zukünftige ReUse-Potenzialquote haben.
- **Innenausbauprojekte:** Türen, Leuchten, Doppelböden, Trennwände oder Sanitärobjekte lassen sich oft gut zählen. Stückzahlquoten sind hier verständlich, sollten aber mit Wert oder CO2 ergänzt werden.
- **Mineralischer Rückbau:** Eine hohe Recycling- oder Verwertungsquote von Beton und Mauerwerk bedeutet nicht, dass Bauteile wiederverwendet wurden. ReUse-Quote muss Recycling klar ausschließen oder separat ausweisen.

## Herausforderungen / offene Fragen

- **Uneinheitliche Definition:** In Praxisberichten werden ReUse, Recycling, Upcycling, Weiterverwertung und Wiederverwendung oft vermischt.
- **Nennerproblem:** Die Quote ändert sich stark je nachdem, ob Gebäudemasse, Kostengruppe, Bauteilgruppe oder Projektumfang als Nenner dient.
- **Massenverzerrung:** Beton, Mauerwerk und Erdstoffe dominieren massenbezogene Quoten. Leichte, aber klimatisch oder wirtschaftlich wichtige Bauteile verschwinden.
- **Planung vs. Realität:** Geplante ReUse-Quoten sinken oft durch Schäden, Zeitdruck, fehlende Käufer, Normprobleme oder Logistik.
- **In-situ-Erhalt wird unterschätzt:** Viele Quoten zählen nur ausgebaute und wiedereingebaute Bauteile; das Weiterverwenden im Bestand wird nicht erfasst.
- **Doppelte Zählung:** Ein Bauteil kann bei abgebendem und aufnehmendem Projekt gezählt werden. Für systemweite Statistiken braucht es eindeutige Bilanzregeln.
- **Qualitätsdimension fehlt:** Eine Quote sagt nichts darüber, ob hochwertige Wiederverwendung oder minderwertige Zweitnutzung stattfindet.
- **Zeitliche Lücke:** Bauteile, die eingelagert werden, sind noch nicht wiederverwendet. Sie sollten als „zur Wiederverwendung vorbereitet“ separat geführt werden.
- **Regulatorische Anschlussfähigkeit:** Abfallrechtliche Begriffe, Produktrecht und Gebäudebewertung verwenden unterschiedliche Systemgrenzen.

## Quellen

- European Commission / Joint Research Centre: Level(s) indicator 2.1, Bill of Quantities, materials and lifespans. https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2021-01/UM3_Indicator_2.1_v1.1_34pp.pdf
- European Commission / Joint Research Centre: Level(s), EU framework for sustainable buildings. https://green-forum.ec.europa.eu/green-business/levels_en
- European Commission: EU construction & demolition waste management protocol including guidelines for pre-demolition and pre-renovation audits of construction works, updated edition 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- Directive 2008/98/EC on waste, as amended: Waste Framework Directive.
- DIN SPEC 91484: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen vor Abbruch- und Renovierungsarbeiten.
- DGNB: Building Resource Passport. https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport
- Madaster Documentation: Madaster Circularity Indicator. https://docs.madaster.com/us/en/platform-pages/building/circularity.html
- Madaster: Material passport. https://madaster.com/material-passport/
- ÖKOBAUDAT: Datenbank für ökologische Gebäudebewertungen. https://www.oekobaudat.de/en.html
- baubüro in situ: K.118 – Kopfbau Halle 118. https://www.insitu.ch/projekte/196-k118-kopfbau-halle-118
- Werner Sobek: NEST Unit UMAR. https://www.wernersobek.com/projects/nest-unit-umar/
- Heisel, F.; Rau-Oberhuber, S.: Calculation and evaluation of circularity indicators for the built environment using the case studies of UMAR and Madaster, Journal of Cleaner Production, 2020.

