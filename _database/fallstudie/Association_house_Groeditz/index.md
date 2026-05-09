---
entity: "fallstudie"
id: "Association_house_Groeditz"
title: "Association house, Gröditz — Fallstudie Direct Reuse / Wiederverwendung von Betonfertigteilen"
build_status: "promoted_phase42"
legacy_paths:
  - "Gebäude\\Association_house_Groeditz.md"
node_kind: "core"
bauobjekt:
  - "Association_house_Groeditz"
projekt:
  - "Association_house_Groeditz"
---

# Association house, Gröditz — Fallstudie Direct Reuse / Wiederverwendung von Betonfertigteilen

## Legacy Content

### Legacy Source: Gebäude\Association_house_Groeditz.md

- Map action: split_into_case_graph
- Primary target: fallstudie/Association_house_Groeditz
- Secondary targets: projekt/Association_house_Groeditz; bauobjekt/<from_content>; reuse_einsatz/<per_component>
- Risk flags: do_not_treat_file_as_single_gebaeude_only

# Association house, Gröditz — Fallstudie Direct Reuse / Wiederverwendung von Betonfertigteilen

**Arbeitsstand:** 2026-05-07  
**Sprache:** Deutsch  
**Regel:** Es werden nur tatsächlich wiederverwendete Bau-, Tragwerks-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente gezählt. Lose Möbel, Dekoration, reine DfD-Strategien und bloßer Bestandserhalt zählen nicht.

## 1. EINORDNUNG

- **Entscheidung:** HAUPTFALL
- **Bewertung:** ★★★★☆
- **Begründung:** Gebauter Vereins-/Sportbau mit großem dokumentiertem Umfang wiederverwendeter Betonfertigteile. Die Literatur nennt 279 Fertigteile aus einer Schule des Typs Dresden sowie 159 WBS70-Elemente aus einem weiteren Gebäude. Damit ist der Fall tragwerks-, raum- und hüllenrelevant. Nicht gezählt werden Möbel oder Dekoration.
- **Vertrauensgrad:** teilweise belegt
- **Warnung Bestandserhalt:** nein
- **Warnung Möbel/Dekoration:** nein
- **Projektstatus:** gebaut

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Association house, Gröditz / Gröditz association house | Untersuchter Reuse-Fall | [S0], [S1] | teilweise belegt | Deutsche offizielle Projektbezeichnung nicht gefunden. |
| Gebäude | Sport-/Vereinshaus | Empfängergebäude | [S1] | teilweise belegt | „new sport-association house“. |
| Ort | Gröditz, Deutschland | Standort Empfängerprojekt | [S1] | belegt | Ca. 2,5 km Distanz laut PRECS-Datenbank. |
| Projekt | Neubau aus wiederverwendeten Betonfertigteilen | Reuse-Projekt | [S1] | belegt | Fallstudienjahr 2007. |
| Bauteil | 279 Betonfertigteile + 159 WBS70-Paneele | Hauptreuse | [S1] | belegt | 438 dokumentierte Teile, Zusammensetzung teils genauer beschrieben. |
| Material | Stahlbetonfertigteile | Hauptmaterial | [S1] | belegt | Precast concrete / CP. |
| Gebäude | Spender: Schule Typ Dresden; weiteres WBS70-Gebäude | Herkunft der Teile | [S1] | belegt | Nutzungen/Adressen unbekannt. |
| Tragwerkssystem | Fertigteil-Wand-/Deckensystem | Reuse-Tragwerk | [S1] | teilweise belegt | Neue Tragwerkslogik nicht detailliert veröffentlicht. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | direkte Wiederverwendung | [S1] | belegt | Kein Downcycling zu RC-Beton oder Schotter. |
| Verbindung | Ziegelschicht zum Höhenausgleich; überlappende Fassaden-Fertigteile | Konstruktive Anpassung | [S1] | belegt | Selten dokumentierter Detailhinweis. |
| Abbruchmethode | selektiver Rückbau/Demontage | nötig für Bauteilgewinnung | [S1], [S6] | teilweise belegt | Projektspezifische Geräte unbekannt. |
| Aufbereitungsmethode | Höhenausgleich durch Ziegelschicht; sonst unbekannt | Anpassung der Wiederverwendung | [S1] | teilweise belegt | Reinigung/Zuschnitt unbekannt. |
| Prüfung | unbekannt | Tragfähigkeit, Materialzustand | unbekannt | unklar | Keine projektspezifischen Prüfberichte gefunden. |
| Logistik | ca. 2,5 km Transportdistanz | kurze lokale Wiederverwendung | [S1] | belegt | Lagerung unbekannt. |
| Hürde | Maßausgleich, unterschiedliche Fertigteilsysteme, Anschlüsse | projektspezifisch teilweise ablesbar | [S1] | teilweise belegt | Zwei Spenderquellen / Systeme. |
| Kennwert | 438 dokumentierte Betonfertigteile; 2,5 km; 2007 | wichtige Fallwerte | [S1] | belegt | Fläche, CO₂, Kosten unbekannt. |
| People | Polony 2008; Mettke/Heyn/Dechantsreiter als Literaturquellen | Quellenbezug | [S1] | teilweise belegt | Konkrete Projektrollen unbekannt. |
| Wirtschaft | unbekannt | Kosten | unbekannt | unklar | Keine öffentlich belastbaren Werte. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Spendergebäude | Mehrere Herkunftsgebäude müssen getrennt erfasst werden | Schule Typ Dresden + WBS70-Gebäude | Gebäude, Bauteil, Logistik |
| Empfängergebäude | Zielgebäude mit neuer Nutzung | Sport-/Vereinshaus Gröditz | Projekt, Fallstudie, Leistungsanforderung |
| Fertigteilsystem | Erfasst systemabhängige Bauteilgeometrien | Dresden-Typ, WBS70 | Tragwerkssystem, Verbindung |
| Ausgleichsschicht | Konstruktive Reuse-Anpassung braucht eigene Erfassung | Ziegelschicht zum Höhenausgleich | Verbindung, Aufbereitungsmethode |

## 3. FALLSTUDIE

- **Name:** Association house, Gröditz / Gröditz association house
- **Ort:** Gröditz, Deutschland
- **Gebäude:** Sport-/Vereinshaus
- **Projekt:** Neubau eines Sport-/Vereinshauses mit wiederverwendeten Betonfertigteilen aus mindestens zwei Spendergebäuden
- **Beteiligte People / Akteure:** unbekannt; Polony 2008 und Mettke/Heyn/Dechantsreiter erscheinen in der Literatur als Quellen
- **Architekt:** unbekannt
- **Tragwerksplaner:** unbekannt
- **Bauherr:** unbekannt
- **Zeitraum:** 2007 laut PRECS-Fallstudienliste
- **Ursprüngliche Nutzung:** Spender 1: Schule Typ Dresden; Spender 2: WBS70-Gebäude, genaue Nutzung unbekannt
- **Neue Nutzung:** Sport-/Vereinshaus
- **Fläche / Maßstab:** Fläche unbekannt; 438 dokumentierte wiederverwendete Betonfertigteile
- **Schutzstatus / Denkmalstatus:** unbekannt
- **Quellenlage:** Wissenschaftliche Sekundärquelle mit Mengen und Konstruktionshinweis; kaum frei zugängliche Projektprimärquellen

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Kombination von Bauteilen aus mehreren Spendergebäuden
- **Hauptniveau:** Tragwerk / Gebäudehülle / räumlicher Ausbau
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Die Elemente wurden aus anderen Gebäuden entnommen und neu montiert. Es handelt sich nicht um Erhalt am Ort und nicht um Zerkleinerung zu Recyclingmaterial.
- **Warum ist der Fall relevant?** Der Fall zeigt eine komplexe, gemischte Bauteilquelle und dokumentiert konstruktive Anpassungen wie Ziegelausgleich und überlappende Fassadenplatten.

## 5. BAUTEIL-INVENTAR

| Bauteil | Material | Herkunft | alte Funktion | neue Funktion | Menge/Umfang | tragend? | räumlich? | Hülle? | technisch? | Eingriff/Aufbereitung | Verbindung | Prüfung | Leistungsanforderung | Norm/Recht | Hürde | Quelle | unbekannt |
|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|
| Außenwand-Fertigteile | Stahlbetonfertigteil | Schule Typ Dresden | Außenwand | Wand/Fassade | Teil von 279 | wahrscheinlich ja | ja | ja | nein | unbekannt | überlappende Fassaden-Fertigteile erwähnt | unbekannt | Tragfähigkeit, Hülle, Feuchte/Wärme | unbekannt | Maß-/Anschlussdetails | [S1] | genaue Anzahl Außenwand |
| Innenwand-Fertigteile | Stahlbetonfertigteil | Schule Typ Dresden | Innenwand | Wand/Trag-/Raumstruktur | Teil von 279 | wahrscheinlich ja | ja | nein | nein | unbekannt | Ziegelschicht zum Ausgleich erwähnt | unbekannt | Tragfähigkeit, Brandschutz, Schallschutz | unbekannt | Höhenausgleich | [S1] | genaue Anzahl Innenwand |
| Innenwandrahmen | Stahlbetonfertigteil | Schule Typ Dresden | Wand-/Rahmenelement | räumlich/tragend | Teil von 279 | wahrscheinlich ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit | unbekannt | Geometrie | [S1] | Details |
| Deckenelemente | Stahlbetonfertigteil | Schule Typ Dresden | Decke/Boden | Decke/Boden | Teil von 279 | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Brandschutz | unbekannt | Anschluss, Betondeckung | [S1] | genaue Anzahl |
| Sockel-/Plinthenplatten | Stahlbetonfertigteil | Schule Typ Dresden | Sockel/Plinthe | Sockel/Fassade/Wandbereich | Teil von 279 | unbekannt | ja | teilweise | nein | unbekannt | unbekannt | unbekannt | Feuchte/Dauerhaftigkeit | unbekannt | Anschluss | [S1] | genaue Funktion |
| Treppen | Stahlbetonfertigteil | Schule Typ Dresden | Treppen | Erschließung | Teil von 279 | ja | ja | nein | nein | unbekannt | unbekannt | unbekannt | Tragfähigkeit, Brandschutz, Barrierefreiheit | unbekannt | Schall/Brandschutz | [S1] | Anzahl |
| WBS70-Paneele | Stahlbetonfertigteil | weiteres Gebäude | Wand/Decke unbekannt | Wand/Decke/Fassade | 159 | wahrscheinlich ja | ja | teilweise | nein | unbekannt | Ziegelausgleich/Überlappung im Projektkontext erwähnt | unbekannt | Tragfähigkeit/Hülle | unbekannt | Systemmix | [S1] | Bauteilarten |
| Fenster/Türen/Dach/Geländer/Bodenaufbauten/TGA/Dämmung/Sanitär/Beleuchtung/feste Einbauten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | ja |

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Bauteile aus Schule und WBS70-Gebäude erfassen | unbekannt | Bauteilinventar | unbekannt | selektiver Rückbau erforderlich | unbekannt | unbekannt | lokale Quellen | zwei Systeme koordinieren | Bauteile nach Funktion kombinieren | [S1] |
| Bauteilinventar | 279 + 159 Bauteile dokumentiert | unbekannt | PRECS-Dokumentation | unbekannt | unbekannt | unbekannt | unbekannt | ca. 2,5 km | Datenkomplexität | Fallstudienerfassung | [S1] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | mögliche Plattenbau-Schadstoffe | unbekannt | [S5] allgemein |
| Rückbau/Ausbau | Demontage von Fertigteilen | unbekannt | selektive Demontage | Kran/Schneidtechnik unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bruch und Maßabweichung | unbekannt | [S1], [S6] allgemein |
| Transport | Transport nach Gröditz | unbekannt | Schwertransport wahrscheinlich, nicht projektspezifisch belegt | unbekannt | unbekannt | unbekannt | unbekannt | ca. 2,5 km | geringe Distanz, schwere Teile | lokale Beschaffung | [S1] |
| Lagerung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Lagerbedarf | unbekannt | keine Quelle |
| Aufbereitung | Höhenausgleich und Fassadenüberlappung | unbekannt | Ziegelschicht / konstruktive Anpassung | unbekannt | unbekannt | Ziegelschicht zum Nivellement | unbekannt | unbekannt | unterschiedliche Höhen/Geometrien | Ziegel-Ausgleichsschicht | [S1] |
| Planung | Entwurf mit gemischtem Fertigteilbestand | unbekannt | system-/bauteilorientierte Planung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Entwurfsbindung | Bauteile kombinieren | [S1] |
| Genehmigung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Nachweis, Haftung | unbekannt | [S4] allgemein |
| Wiedereinbau | Montage im neuen Vereinshaus | unbekannt | Remontage | Kran wahrscheinlich, nicht belegt | unbekannt | Ziegelausgleich | unbekannt | Neubau Gröditz | Toleranzen/Anschlüsse | überlappende Fassaden-CP | [S1] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Langzeitdaten fehlen | unbekannt | keine Quelle |

## 7. TECHNIK, LEISTUNG, NORMEN

| Thema | Befund | Leistungsanforderung | Norm/Recht | Prüfung | technische Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|
| Tragwerkssystem | Mischsystem aus Schultyp-Dresden- und WBS70-Fertigteilen | Standsicherheit | projektspezifisch unbekannt | unbekannt | Systemmix | konstruktive Anpassung | [S1] |
| Lastabtragung | Wände/Decken/Treppen vermutlich tragend eingesetzt | Tragfähigkeit/Gebrauchstauglichkeit | unbekannt | unbekannt | Lastpfade im neuen Gebäude | unbekannt | [S1] |
| Verbindung | Ziegelschicht zum Höhenausgleich; Fassaden-CP überlappend | kraftschlüssige/gebrauchstaugliche Anschlüsse | unbekannt | unbekannt | unterschiedliche Bauteilhöhen | Höhenausgleich durch Mauerwerk | [S1] |
| Brandschutz | unbekannt | Feuerwiderstand für Vereins-/Sportnutzung | unbekannt | unbekannt | alte Fertigteile/Decken | unbekannt | [S5] allgemein |
| Schallschutz | unbekannt | nutzungsabhängig | unbekannt | unbekannt | Treppen/Wände | unbekannt | keine Quelle |
| Feuchte | Sockel-/Außenwandteile betroffen | Feuchte- und Dauerhaftigkeitsschutz | unbekannt | unbekannt | Altbauteile in neuer Hülle | unbekannt | keine Quelle |
| Wärmeschutz | Außenwand/Fassade betroffen | energetischer Standard 2007 | unbekannt | unbekannt | Wärmebrücken/Systemmix | unbekannt | keine Quelle |
| Luftdichtheit | unbekannt | Gebäudehülle | unbekannt | unbekannt | Fugen/alte Platten | unbekannt | keine Quelle |
| TGA-Integration | unbekannt | Leitungsführung | unbekannt | unbekannt | Durchbrüche/Öffnungen | unbekannt | keine Quelle |
| Zulassung/Haftung | nicht dokumentiert | Nachweis wie Neubauteil | allgemeine heutige Einordnung: Eurocode 2, DIN EN 206-1, DIN 1045-2 | unbekannt | Gewährleistung | unbekannt | [S4] allgemein |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fertigteile aus Dresden-Typ-Schule | 279 | Stück | PRECS-Fallstudienliste | Empfängergebäude | [S1] | belegt |
| WBS70-Paneele aus weiterem Gebäude | 159 | Stück | PRECS-Fallstudienliste | Empfängergebäude | [S1] | belegt |
| dokumentierte Fertigteile gesamt | 438 | Stück | Addition aus [S1] | Empfängergebäude | [S1] | teilweise belegt |
| Transportdistanz | ca. 2,5 | km | PRECS-Fallstudienliste | Spender- zu Empfängerstandort | [S1] | belegt |
| Jahr/Fallstudienstart | 2007 | Jahr | PRECS-Fallstudienliste | Projekt | [S1] | belegt |
| Fläche | unbekannt | m² | unbekannt | unbekannt | keine Quelle | unklar |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine Quelle | unklar |
| Kosten | unbekannt | EUR | unbekannt | unbekannt | keine Quelle | unklar |
| Energiebedarf/U-Wert | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | unklar |

## 9. HÜRDEN-MATRIX

| Hürde | Kategorie | Ursache | Auswirkung | betroffene Entitäten | Lösung | übertragbare Lehre | Quelle |
|---|---|---|---|---|---|---|---|
| Kombination zweier Bauteilsysteme | technisch/gestalterisch | Dresden-Typ + WBS70 | Maß- und Anschlussprobleme | Bauteil, Verbindung | Ziegelschicht und Überlappung | Systemmix braucht tolerante Details | [S1] |
| Höhenausgleich | technisch | abweichende Bauteilmaße | Wand-/Fassadenanschlüsse schwierig | Verbindung, Aufbereitung | Ziegel-Ausgleichsschicht | Low-tech-Ausgleich kann Reuse ermöglichen | [S1] |
| Nachweis | rechtlich/technisch | gebrauchte tragende Bauteile | Genehmigungs-/Haftungsrisiko | Norm, Prüfung | unbekannt | Prüfpfad dokumentieren | [S4], [S5] |
| Logistik | logistisch | schwere Fertigteile | Kosten-/Ablaufrisiko | Logistik | kurze Distanz 2,5 km | lokale Quellen sind vorteilhaft | [S1] |
| Quellenlücken | wissenschaftlich | wenig Primärpublikation | viele unbekannte Details | Dokument, People, Wirtschaft | Archiv prüfen | Reuse-Projekte brauchen bessere Publikation | eigene Bewertung |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** unbekannt; direkte Beschaffung aus Rückbau naheliegend, aber nicht belegt
- **Bauteilbörse / Quelle:** keine Bauteilbörse belegt
- **Kostenwirkung:** unbekannt
- **Zeitwirkung:** unbekannt
- **Versicherung / Haftung:** unbekannt
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** wahrscheinlich erhöht durch Auswahl und Systemmix; projektspezifisch unbekannt
- **Lagerung:** unbekannt
- **Marktbarrieren:** Systemmix, Nachweis, Gewährleistung, fehlende Standards, knappe Dokumentation

## 11. GESTALTUNG UND KULTURELLER WERT

- **Sichtbarkeit der Wiederverwendung:** unbekannt; Fassadenüberlappung und Ziegelausgleich könnten sichtbar oder verdeckt sein, aber keine Fotos/Primärdaten gefunden
- **räumliche Transformation:** Schule/Wohnungsbau-Fertigteile werden zu einem Sport-/Vereinshaus transformiert
- **Atmosphäre / Ausdruck:** unbekannt
- **Umgang mit Spuren:** unbekannt
- **sozialer Wert:** Sport-/Vereinsnutzung deutet gemeinschaftlichen Nutzen an
- **Denkmal- oder Bestandswert:** unbekannt
- **Kritik / Grenzen:** Komplexität des Systemmixes und fehlende technische Offenlegung

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Architekt, Tragwerksplaner, Bauherr, Schadstoff, detaillierte Abbruchmethode, Prüfung, Software, Kosten, CO₂, Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Spendergebäude, Fertigteilsystem, Ausgleichsschicht, Bauteilzustand.
- **Welche Daten fehlen?** Projektdokumentation, Bauakte, Planmaterial, Anschlussdetails, Prüfberichte, Energie-/Kosten-/CO₂-Daten.
- **Welche Quellen müssten geprüft werden?** Polony 2008, Mettke 2008/2010, Heyn et al. 2008b, Dechantsreiter et al. 2015, Stadt-/Bauakten Gröditz.

## 13. ABSCHLUSS

- **Soll der Fall in die Hauptliste?** ja
- **5 wichtigste Fakten:**
  1. Gebauter Reuse-Fall in Gröditz.
  2. Neues Sport-/Vereinshaus.
  3. 279 Fertigteile aus einer Dresden-Typ-Schule.
  4. 159 zusätzliche WBS70-Paneele aus einem weiteren Gebäude.
  5. Kurze Transportdistanz von ca. 2,5 km.
- **5 wichtigste Bauteile:**
  1. Außenwand-Fertigteile.
  2. Innenwand-Fertigteile.
  3. Deckenelemente.
  4. Sockel-/Plinthenplatten.
  5. Treppen.
- **5 wichtigste Hürden:**
  1. Systemmix.
  2. Höhenausgleich.
  3. Anschlussdetails.
  4. Tragwerksnachweis.
  5. Fehlende öffentliche Primärdaten.
- **5 wichtigste übertragbare Erkenntnisse:**
  1. Reuse kann mehrere Spendergebäude kombinieren.
  2. Kurze lokale Transporte sind wichtig.
  3. Einfache Ausgleichslösungen können Wiederverwendung ermöglichen.
  4. Systematisches Bauteilinventar ist zentral.
  5. Sport-/Vereinsbauten eignen sich als robuste Empfängerprogramme.
- **5 offene Fragen:**
  1. Wer plante und baute das Projekt?
  2. Welche Prüfungen wurden ausgeführt?
  3. Wie genau funktionieren die Anschlüsse?
  4. Welche Teile sind sichtbar?
  5. Welche Kosten- und CO₂-Wirkung hatte der Reuse?

## Quellen und Links

- [S0] Hochgeladene Prioritätenliste: gebäude4_wiederverwendung_direct_reuse_examples.md
- [S1] Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse of concrete components in new construction projects: Critical review of 77 circular precedents, Journal of Cleaner Production 383, 135235. DOI: https://doi.org/10.1016/j.jclepro.2022.135235
- [S2] ScienceDirect / Journal of Cleaner Production article page: https://www.sciencedirect.com/science/article/pii/S0959652622048090
- [S3] ResearchGate PDF/record for the same article: https://www.researchgate.net/publication/365763750_Reuse_of_concrete_components_in_new_construction_projectscritical_review_of_77_circular_precedents
- [S4] BauStatik-Wiki, Wiederverwendung von Stahlbetonbauteilen: https://baustatik-wiki.fiw.hs-wismar.de/mediawiki/index.php/Wiederverwendung_von_Stahlbetonbauteilen
- [S5] InNoWest Brandenburg, Bachelorarbeit zur Wiederverwendung von WBS70-Fertigteilen: https://innowest-brandenburg.de/beitraege/Bachelorarbeit-plattenbautyp-wbs-70
- [S6] BFT International, Wiederverwendung von Betonfertigteilplatten: https://www.bft-international.com/de/artikel/wiederverwendung-von-betonfertigteilplatten-4095412.html
- [S7] Sächsische.de / Polony 2008 wird in Küpfer et al. als Quelle genannt: https://www.saechsische.de/plus/fassade-vom-groeditzer-vereinshaus-wird-gemauert-1921018.html
