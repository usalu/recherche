---
type: Bauteil
material: ["[[material/Beton]]"]
pruefung: ["[[pruefung/Zustandsbewertung]]"]
reuse_strategie: ["[[reuse_strategie/Direkte_Wiederverwendung]]"]
tragwerkssystem: ["[[tragwerkssystem/Betonfertigteil_System]]"]
verwandt: ["[[bauteil/Deckenplatte]]", "[[bauteil/Wand]]"]
---

## Verknüpfungen

**Übergeordnete Themen**
- Entwerfen mit Bestand / Wiederverwendung von Bauelementen
- Urban Mining, Bauteilernte, Pre-Demolition-Audit, Bauteilpass
- Tragwerksplanung im Bestand, Nachrechnung, Rückbauplanung, Logistik

**Verwandte Dateien**
- `bauteil/Deckenplatte.md` – funktionsbezogene Betrachtung horizontaler Platten; dort auch Ortbeton-Zuschnitte und Hohlplatten als Deckenbauteil
- `bauteil/Wand.md` – Wand als vertikaler Sammeltyp; Betonwandelemente und Sandwichpaneele dort systemspezifisch
- `material/Beton.md`, `material/Bewehrungsstahl.md`, `material/Spannstahl.md`
- `tragwerkssystem/Skelettbau.md`, `tragwerkssystem/Plattenbau.md`, `tragwerkssystem/Fertigteilbau.md`
- `pruefung/Bestandsaufnahme.md`, `pruefung/Betonprüfung.md`, `pruefung/Zustandsbewertung.md`, `pruefung/Tragwerksnachweis.md`
- `verbindung/Einbauteile.md`, `verbindung/Schraubverbindung.md`, `verbindung/Schweissverbindung.md`, `verbindung/Vergussfuge.md`, `verbindung/Schnittverbindung.md`
- `reuse_strategie/Direkte_Wiederverwendung.md`, `reuse_strategie/Design_from_Available_Stock.md`, `reuse_strategie/Selektiver_Rueckbau.md`

**Relevante Akteure / Fallstudien / Materialien / Standards / Methoden**
- Akteure/Forschung: ReCreate EU Horizon 2020, KTH/Tampere University, TU Eindhoven, EPFL Structural Xploration Lab / Atlas of Reused Concrete, 3XN/GXN und Partnerprojekt (P)RECAST, Consolis/Parma, Skanska, Ramboll, Rotor / FCRBE
- Normen/Regelwerke: Eurocode 2 / EN 1992, EN 206, EN 13369:2023, produktbezogene Normen wie EN 1168, EN 14992, EN 13747, EU-Bauproduktenverordnung Regulation (EU) 2024/3110, DIN SPEC 91484:2023-09, nationale Bauordnungen und Verwaltungsvorschriften
- Methoden: Pre-Demolition-Audit, Bewehrungs- und Spanngliedortung, Bohrkernprüfung, Karbonatisierungs- und Chloridprofil, Rückbau- und Hebekonzept, QR-/RFID-Tracking, Dokumenten- und Herkunftsprüfung, probabilistische Restlebensdauerbewertung

## Kurzdefinition

Ein **Betonfertigteil** ist ein industriell oder werkseitig hergestelltes Betonbauteil, das als räumlich abgegrenztes Element auf die Baustelle geliefert und dort montiert wird. Dazu gehören Stützen, Träger, Binder, Treppen, Fassaden- und Wandelemente, Balkonplatten, Hohlplatten, TT-Platten, Unterzüge und Sonderteile. Für die Wiederverwendung ist nicht allein das Material Beton entscheidend, sondern die Bauteilidentität: Geometrie, Bewehrungs- bzw. Spannsystem, Einbauteile, ursprüngliche Bemessung, Herstellwerk, Exposition, Verbindung und Nutzungsgeschichte.

**Abgrenzung zu `bauteil/Deckenplatte.md`:** Betonfertigteil bezeichnet die Herstell- und Bauteilklasse. Deckenplatte bezeichnet die horizontale Trag- oder Raumabschlussfunktion. Eine Hohlplatte ist deshalb zugleich Betonfertigteil und Deckenplatte; in dieser Datei liegt der Schwerpunkt auf der Fertigteilfamilie, Qualitätssicherung, Rückbau und bauteilübergreifender Wiederverwendung.

## Relevanz für Wiederverwendung im Bauwesen

Betonfertigteile sind für Wiederverwendung besonders relevant, weil sie häufig als diskrete, transportierbare und tragende Bauelemente vorliegen. Ihre Herstellung verursacht hohe Primärressourcen- und Treibhausgasaufwände durch Zement, Stahl, Schalung, Vorspannung, Trocknung, Transport und Montage. Direkte Wiederverwendung kann diese Aufwände weitgehend vermeiden, während Recyclingbeton oder Brechen zu Gesteinskörnung nur einen Teil der Wertschöpfung erhält.

Die Wiederverwendungsfähigkeit ist bei Betonfertigteilen im Vergleich zu monolithischem Ortbeton oft günstiger, weil Fertigteile ohnehin elementiert sind und historisch häufig mit Fugen, Auflagern, Vergussmörteln, Schweißplatten, Bolzen, Konsolen oder eingegossenen Anschlüssen montiert wurden. Gleichzeitig wurden viele Bestandsfertigteile nicht für Demontage geplant: Fugen sind vergossen, Aufbeton verbindet Bauteile, Einbauteile sind korrodiert oder verborgen, und ursprüngliche Statikunterlagen fehlen.

In der Praxis ist das größte Potenzial bei großformatigen, seriellen Elementen aus jüngeren Gebäuden mit guter Dokumentation zu erwarten: Büro-, Schul-, Industrie-, Parkhaus- und Wohnungsbauten in Fertigteil- oder Plattenbauweise. Besonders geeignet sind Bauteile mit regelmäßigen Abmessungen, zugänglichen Fugen, geringen Schäden und Belastungen, die im neuen Projekt unterhalb oder nahe der ursprünglichen Bemessung liegen.

## Fachinhalt

### Typen und Wiederverwendungslogik

**Stützen und Träger**
- Hohe Wiederverwendungsrelevanz bei klarer Geometrie, sichtbaren Konsolen, einfachen Lagerdetails und ausreichender Druck-/Biege-/Schubtragfähigkeit.
- Kritisch sind abgeschnittene Anschlussbewehrungen, verdeckte Einbauteile, beschädigte Konsolen, Karbonatisierung im Bereich geringer Betondeckung und unklare Feuerwiderstandsdauer.
- Neue Nutzung sollte bevorzugt gleiche oder geringere Beanspruchungsart haben: Stütze bleibt Stütze, Träger bleibt Träger. Funktionswechsel ist möglich, erhöht aber Prüf- und Nachweisaufwand.

**Wand- und Fassadenelemente**
- Wiederverwendung hängt stark von Anschlüssen, Fassadenalterung, thermischer Schichtung, Befestigungspunkten und Schäden durch Demontage ab.
- Sandwichpaneele können hohe Ressourcenwerte enthalten, sind aber bauphysikalisch schwierig, wenn Dämmstoffe, Verbindungsmittel oder Fugen nicht mehr dem heutigen Standard entsprechen.

**Hohlplatten, TT-Platten und Deckenelemente**
- Großes Potenzial bei serieller Geometrie und hoher Tragfähigkeit, aber kritisch wegen Vorspannung, Aufbeton, Fugenschnitt, Schubtragfähigkeit, Auflagerlängen und Hebepunkten.
- Hohlplatten sind oft gut demontierbar, wenn Aufbeton und Fugen getrennt werden können. Bei monolithischem Verbund ist Rückbau deutlich riskanter.

**Treppen, Podeste, Balkone, Fassadenplatten**
- Teilweise sehr gut wiederverwendbar, wenn Abmessungen in neues Raster passen und Befestigungen zugänglich sind.
- Bei Balkonen sind Karbonatisierung, Chloride, Frost-Tausalz, Geländeranschlüsse und Wärmebrücken besonders zu prüfen.

### Bewertungs- und Entscheidungsparameter

**1. Dokumentation und Identität**
- Bestandspläne, Positionspläne, Montagepläne, Statik, Herstellunterlagen, Betonfestigkeitsklasse, Expositionsklasse, Vorspannart, Bewehrungsangaben, Herstelljahr und Hersteller sind zentrale Entscheidungsgrundlagen.
- Fehlen Unterlagen, müssen Bauteile über Vermessung, zerstörungsfreie Prüfung, Stichprobenöffnung, Bohrkerne und Vergleich mit Typenkatalogen rekonstruiert werden.
- Jedes geerntete Bauteil benötigt eine eindeutige ID mit Herkunftsort, Lage im Gebäude, Ausrichtung, Fotodokumentation, Schäden, Prüfergebnissen, Transportstatus und Lagerort.

**2. Tragfähigkeit**
- Nachweis im neuen Bauwerk erfolgt nicht durch pauschale Anerkennung der früheren Nutzung, sondern durch projektspezifische Bemessung nach geltenden Anforderungen oder begründetem Bestandnachweis.
- Wichtige Parameter: Betonfestigkeit, Bewehrungs- und Spanngliedlage, Betondeckung, Korrosionszustand, Rissbreiten, Auflagerzonen, Schubtragfähigkeit, Druckzonen, Ermüdung bei Verkehrsbauten/Parkhäusern, Brandbeanspruchung und frühere Überlasten.
- Bei Spannbeton sind Spanngliedtyp, Spannrichtung, Verankerungszonen, mögliche Querschnittsschwächungen und Schnittverbote besonders kritisch. Unkontrolliertes Sägen kann Tragfähigkeit und Sicherheit zerstören.

**3. Dauerhaftigkeit und Restlebensdauer**
- Prüfen: Karbonatisierungstiefe im Verhältnis zur Betondeckung, Chloridprofil, Sulfat-/chemische Angriffe, Frost-Tausalz-Schäden, Alkali-Kieselsäure-Reaktion, Feuchteeinwirkung, Rissbild, Abplatzungen, Korrosion, biologische Bewachsung und Oberflächenbeschichtungen.
- Reuse ist besonders plausibel, wenn die neue Exposition gleich oder weniger aggressiv ist als die alte. Ein ehemals innenliegendes Bauteil sollte nicht ohne zusätzlichen Nachweis außen oder in chloridhaltiger Umgebung eingesetzt werden.
- Restlebensdauer ist kein fester Materialwert. Sie entsteht aus Zustand, Exposition, Schutzmaßnahmen, Sicherheitskonzept und Instandhaltungsplan.

**4. Verbindung und Demontierbarkeit**
- Rückbaugeeignet sind mechanische, zugängliche oder trennbare Verbindungen. Schwieriger sind Ortbetonergänzungen, verschweißte Platten, vergossene Fugen, verdeckte Dübel, nachträglich eingebaute Leitungen und kraftschlüssige Verbundschichten.
- Rückbauplanung muss Reihenfolge, Lastumlagerung, temporäre Abstützung, Schnittführung, Anschlagpunkte, Hebezeuge, Zwischenlagerung und Arbeitsschutz festlegen.
- Alte Transportanker dürfen nicht ungeprüft wiederverwendet werden. Hebepunkte können korrodiert, überlastet oder für heutige Hebeprozesse unzulässig sein.

**5. Maßhaltigkeit und Passfähigkeit**
- Fertigteile besitzen Toleranzen aus Herstellung, Montage, Verformung und Rückbau. Wiederverwendung benötigt ein neues Entwurfsraster, das diese Toleranzen aufnimmt.
- Günstig sind additive, toleranzfreundliche Fügungen: trockene Lager, einstellbare Stahlteile, Schraubverbindungen, Verguss nur dort, wo spätere Demontage nicht wesentlich beeinträchtigt wird.
- Nachbearbeitung wie Schneiden, Bohren oder Abschleifen reduziert oft Tragfähigkeit, Betondeckung oder Brandschutz und muss nachgewiesen werden.

### Prüf- und Nachweiskette

1. **Vorprüfung / Bestandssichtung**: Gebäudealter, Nutzung, Typologie, Pläne, Schadstoffverdacht, Rückbauzugang, wirtschaftliche Menge.
2. **Bauteilkartierung**: Elementraster, Typenfamilien, Lage, Fotodokumentation, Fugen- und Anschlussarten.
3. **Zustandsprüfung**: visuell, klopfend, Vermessung, Risskartierung, Feuchte, Korrosion, Karbonatisierung, Chloride, Betonfestigkeit, Bewehrungslage.
4. **Strukturelle Bewertung**: Bauteilklasse, Lastgeschichte, Tragreserven, Nachweisfähigkeit, neue Nutzungsszenarien.
5. **Rückbauversuch / Pilotentnahme**: Demontage eines Musterbauteils zur Prüfung von Fugen, Schäden und Aufwand.
6. **Qualitätssicherung nach Entnahme**: erneute Sichtprüfung, Dokumentation von Abplatzungen/Schnittkanten, Lagerfreigabe, Reparaturkonzept.
7. **Projektbezogener Nachweis**: Bemessung im Empfängerprojekt, neue Verbindung, Brandschutz, Schall, Bauphysik, Montagezustände.
8. **Einbau und Übergabe**: As-built-Dokumentation, Bauteilpass, Wartungs- und Inspektionsplan.

### Rechtliche und normative Einordnung

- In der EU regelt die Bauproduktenverordnung die Bereitstellung harmonisierter Bauprodukte am Markt. Für wiederverwendete Bauprodukte ist in vielen Ländern weiterhin unklar, wann ein geerntetes Bauteil als Bauprodukt neu „in Verkehr gebracht“ wird und welche Leistungserklärungen, CE-Kennzeichnungen oder nationalen Nachweise erforderlich sind.
- EN 13369 enthält gemeinsame Regeln für Betonfertigteile; produktspezifische Normen wie EN 1168, EN 14992 und EN 13747 sind für neue Produkte entwickelt, liefern aber wichtige Prüf- und Leistungsparameter für wiederverwendete Fertigteile.
- DIN SPEC 91484 ist im deutschsprachigen Kontext relevant, weil sie ein Verfahren zur Erfassung von Bauprodukten vor Abbruch- und Renovierungsarbeiten beschreibt. Sie ersetzt keine Tragwerksprüfung, schafft aber eine einheitlichere Datentiefe für Anschlussnutzung.
- Tragwerksnachweise müssen mit qualifizierten Tragwerksplanenden, Prüfingenieurinnen/Prüfingenieuren und Behörden abgestimmt werden. Regionale Unterschiede sind erheblich.

## Praxisbezug / Beispiele

**ReCreate, Finnland / Tampere**
- Das EU-Projekt ReCreate untersucht Rückbau und Wiederverwendung von Betonfertigteilen aus Gebäuden, die ursprünglich nicht für Demontage geplant waren.
- In Tampere wurden Hohlplatten, Stützen und Träger aus einem Bürogebäude demontiert. Bei einem finnischen Mini-Pilot wurden zunächst 25 wiedergewonnene Hohlplatten in einem Wohngebäude eingesetzt; ein weiterer Mini-Pilot umfasste 55 wiederverwendete Elemente, darunter 35 Hohlplatten, 13 Stützen und 7 Träger.
- Praxisrelevante Lehren: Aufbeton/Fugen müssen entfernt oder geschnitten werden, Bauteile brauchen Rückverfolgbarkeit, und verantwortliche Tragwerksplanung sowie Qualitätssicherung sind zentrale Skalierungsbedingungen.

**ReCreate, Niederlande / Qualitätssicherung**
- Der niederländische Cluster betont, dass Wiederverwendung von Betonfertigteilen nur skalierbar ist, wenn Qualität so nachvollziehbar nachgewiesen werden kann wie bei neuen Produkten.
- Daraus folgt: Reuse benötigt nicht nur gute Bauteile, sondern ein prüfbares System aus Dokumentation, Prüfplan, Verantwortlichkeiten, Klassifizierung und Marktkommunikation.

**Historische und neuere Fallstudien**
- Schwedische Beispiele aus dem frühen 21. Jahrhundert zeigen Wiederverwendung von Wand-, Decken- und Treppenelementen aus Plattenbau-Beständen; einzelne Bauteile wurden druck- bzw. lastgeprüft.
- EPFL und Partner dokumentieren mit dem Atlas of Reused Concrete internationale Beispiele für direkte Wiederverwendung von Betonbauteilen, darunter Hohlplatten, Wandstücke und zugeschnittene Ortbetonplatten.
- (P)RECAST in Dänemark arbeitet an der direkten Wiederverwendung ganzer Betonfertigteile als tragende Bauteile und entwickelt dafür interdisziplinäre Methoden zwischen Architektur, Ingenieurwesen, Abbruch, Prüfung und Markt.

## Herausforderungen / offene Fragen

- **Nachweis und Haftung:** Wer übernimmt Verantwortung für ein Bauteil mit alter Produktion, unbekannter Lastgeschichte und neuer Nutzung? Herstellerhaftung, Planerhaftung und Betreiberverantwortung sind nicht einheitlich geklärt.
- **CE und Bauproduktstatus:** Für wiederverwendete Fertigteile fehlen vielerorts praxistaugliche Routinen zur Leistungserklärung. Die neue EU-Bauproduktenverordnung stärkt Digitalisierung, Umweltinformationen und Kreislaufbezüge, löst aber die praktische Re-Zertifizierung gebrauchter Bauteile nicht automatisch.
- **Datenlücken:** Viele Bestandsgebäude besitzen unvollständige Pläne. Ohne Bewehrungs- und Spanninformationen wird der Nachweis teuer oder unmöglich.
- **Demontageschäden:** Abplatzungen, Risse, beschädigte Kanten, geschnittene Anschlüsse oder verlorene Betondeckung können den Wert schnell reduzieren.
- **Wirtschaftlichkeit:** Rückbau, Prüfung, Lagerung und Transport konkurrieren mit günstigen Neuprodukten. Wiederverwendung lohnt sich besonders bei Serien, kurzen Transportwegen, hohem CO₂-Preis/CO₂-Budget, frühem Zugriff auf Spendergebäude und passendem Entwurfsraster.
- **Planungslogik:** Reuse verlangt Design-from-Stock. Der Bestand bestimmt Raster, Spannweiten, Lasten und Detailausbildung stärker als bei Neubau aus Katalogprodukten.
- **Restlebensdauer:** Für Betonfertigteile gibt es keine allgemein akzeptierte Standardmethode, mit der eine zusätzliche Nutzungsdauer von z. B. 50 oder 100 Jahren einfach bestätigt werden kann. Forschung entwickelt hier Frameworks, aber die Praxis bleibt projektbezogen.

## Quellen

- European Commission: Construction Products Regulation (CPR). https://single-market-economy.ec.europa.eu/sectors/construction/construction-products-regulation-cpr_en
- Regulation (EU) 2024/3110 of the European Parliament and of the Council. Official Journal of the European Union, 2024. https://www.eota.eu/sites/default/files/files/OJ_L_202403110_EN_TXT.pdf
- DIN SPEC 91484:2023-09: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten. DIN Media. https://www.dinmedia.de/de/technische-regel/din-spec-91484/371235753
- FCRBE: A guide for identifying the reuse potential of construction products, 2020. https://vb.nweurope.eu/media/10132/en-fcrbe_wpt2_d12_a_guide_for_identifying_the_reuse_potential_of_construction_products.pdf
- FCRBE / Bellastock et al.: Reuse in practice: from deconstruction to implementation, 2023. https://opalis.eu/sites/default/files/2023-10/en_id2023_fcrbe_finition_web.pdf
- ReCreate Project: Reusing precast concrete for a circular economy. https://recreate-project.eu/
- ReCreate: Real-life deconstruction pilots of the ReCreate project, Zenodo, 2024. https://zenodo.org/records/13828855
- ReCreate: Quality assurance of reclaimed precast concrete: Dutch pilot project framework, 2026. https://recreate-project.eu/2026/03/23/quality-assurance-of-reclaimed-precast-concrete-dutch-pilot-project-framework/
- ReCreate: A third reuse mini-pilot implemented in Finland, 2026. https://recreate-project.eu/2026/04/20/a-third-reuse-mini-pilot-implemented-in-finland/
- EN 13369:2023: Common rules for precast concrete products. https://standards.iteh.ai/catalog/standards/cen/7488f236-67c6-4f66-b17e-b61d469f5530/en-13369-2023
- EN 1168:2005+A3:2011: Precast concrete products – Hollow core slabs. https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- EN 14992:2007+A1:2012: Precast concrete products – Wall elements. https://standards.iteh.ai/catalog/standards/cen/cafce02a-7bee-4f74-b785-4adb8ddf0346/en-14992-2007a1-2012
- EN 13747: Precast concrete products – Floor plates for floor systems. https://www.concrete.org.uk/fingertips/floor-plates-for-floor-systems-bs-en/
- Küpfer, C. et al.: Reuse of concrete components in new construction projects: critical review of 77 circular precedents. Journal of Cleaner Production, 2023. https://www.sciencedirect.com/science/article/pii/S0959652622048090
- Devènes, J. et al.: Reusability assessment of reinforced concrete components prior to deconstruction from obsolete buildings. Developments in the Built Environment, 2024. https://www.sciencedirect.com/science/article/pii/S2352710224001529
- EPFL Structural Xploration Lab: Atlas of Reused Concrete. https://concrete-reuse.epfl.ch/
- KTH: New study enables safe reuse of concrete, 2026. https://www.kth.se/en/om/nyheter/centrala-nyheter/new-study-enables-safe-reuse-of-concrete-1.1453932
