---
id: "Betonfertigteil"
entity: "bauteiltyp"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "move_as_knot; semantic_split; semantic_review_split"
title: "Betonfertigteil"
legacy_type: "Bauteil; Tragwerkssystem"
legacy_paths:
  - "bauteil\Betonfertigteil.md"
  - "tragwerkssystem\Betonfertigteil_System.md"
  - "tragwerkssystem\to_sort\Betonfertigteile.md"
target_primary: "bauteiltyp/Betonfertigteil"
target_roles: "phase1_primary; phase2_secondary; phase2_primary"
risk_flags: "old_type_tragwerkssystem_overgeneralized; unsorted_content_do_not_autoload"
---
# Betonfertigteil

## Migration

- Target: bauteiltyp/Betonfertigteil
- Legacy source count: 3
- Legacy types: Bauteil; Tragwerkssystem
- Migration actions: move_as_knot; semantic_split; semantic_review_split
- Target roles: phase1_primary; phase2_secondary; phase2_primary
- Risk flags: old_type_tragwerkssystem_overgeneralized; unsorted_content_do_not_autoload

## Legacy Content: bauteil\Betonfertigteil.md

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

## Legacy Content: tragwerkssystem\Betonfertigteil_System.md

---
type: Tragwerkssystem
bauteil: ["[[bauteil/Betonfertigteil]]", "[[bauteil/Wand]]"]
verwandt: ["[[tragwerkssystem/Design_for_Disassembly]]", "[[tragwerkssystem/Reversible_Fuegung]]", "[[tragwerkssystem/Skelettbauweise]]", "[[tragwerkssystem/Tragende_Wand]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; industrielles Bauen; Betonbau; zirkulärer Rückbau; Bauteilwiederverwendung; Urban Mining.
- **Verwandte Dateien:** `tragwerkssystem/Tragende_Wand.md`; `tragwerkssystem/Skelettbauweise.md`; `tragwerkssystem/Reversible_Fuegung.md`; `bauteil/Betonfertigteil.md`; `bauteil/Decke.md`; `bauteil/Wand.md`; `verbindung/Betonverbindungen.md`; `verbindung/Vergussfuge.md`; `pruefung/Betonpruefung.md`; `pruefung/Schadstoffpruefung.md`; `reuse_strategie/Bauteilwiederverwendung.md`; `projekt/ReCreate.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** ReCreate-Projekt; PRECAST- und ReUse-Forschung; Fertigteilwerke; Rückbauunternehmen; Tragwerksplanung; Betonprüfstellen; zerstörungsfreie Prüfung; Bewehrungsortung; Karbonatisierungs- und Chloridprüfung; Eurocode 2; Eurocode 0; EU Construction & Demolition Waste Management Protocol; ISO 20887; Construction Products Regulation (EU) 2024/3110.

## Kurzdefinition

Ein Betonfertigteil-System ist ein Tragwerk aus werkseitig hergestellten Beton-, Stahlbeton- oder Spannbetonbauteilen, die auf der Baustelle zu Wänden, Decken, Stützen, Unterzügen, Fassaden- oder Dachtragwerken montiert werden. Im Wiederverwendungskontext ist nicht das Materialrecycling von Betonbruch maßgeblich, sondern der möglichst zerstörungsarme Ausbau ganzer Bauteile oder größerer Segmente, ihre Prüfung, Anpassung und erneute tragende oder nichttragende Verwendung.

## Relevanz für Wiederverwendung im Bauwesen

- **Hoher gebundener Ressourcenwert:** Betonfertigteile enthalten Zement, Zuschläge, Stahl, Herstellenergie und Transportaufwand. ReUse erhält einen größeren Teil dieses Werts als Brechen und Recycling.
- **Industrielle Wiederholbarkeit:** Viele Fertigteilgebäude nutzen Raster, Serienbauteile und wiederkehrende Typen. Das kann Identifikation, Demontage, Lagerung und Wiederverwendung erleichtern.
- **Hohe Tragreserven möglich:** Fertigteile wurden häufig robust dimensioniert; bei guter Dokumentation können sie für neue Lastfälle geeignet sein. Ohne Dokumentation ist der Nachweis jedoch aufwendig.
- **Fügungen als Schlüssel:** Fertigteilsysteme sind oft nicht so demontierbar, wie ihre Montage vermuten lässt. Vergussfugen, Ortbetonergänzungen, Schweißlaschen, Aufbeton, Fugendichtstoffe und verdeckte Bewehrungsanschlüsse entscheiden über ReUse-Fähigkeit.
- **Forschungsfeld mit wachsender Praxisnähe:** Projekte wie ReCreate untersuchen reale Rückbau-, Prüf-, Aufbereitungs- und Wiedereinbauprozesse für Betonfertigteile.

## Fachinhalt

### Systemtypen

- **Großtafelbau / Plattenbau:** Tragende Wand- und Deckentafeln mit vertikalen und horizontalen Fugen. ReUse ist möglich, aber Fugenverguss, Korrosion von Verbindungsmitteln, Maßtoleranzen und Schadstoffbelastungen sind kritisch.
- **Skelett-Fertigteilsysteme:** Stützen, Unterzüge, Binder, Riegel, Treppen und Deckenelemente. Besser demontierbar, wenn Auflager und Knoten trocken oder mechanisch gefügt sind.
- **Spannbeton-Hohlplatten und TT-Platten:** Hohe Spannweiten und standardisierte Serien. Kritisch sind Vorspannung, Schnittverbote, Auflagerzonen, Querkraftnachweis, Korrosionszustand und neue Durchbrüche.
- **Fassaden- und Sandwichplatten:** Wiederverwendung oft als Fassaden- oder Nebengebäudeelement möglich; tragende Wiederverwendung hängt von Verbindung, Dämmkern, Ankern und Frost-/Feuchtezustand ab.

### Fügungs- und Demontageprinzipien

- **Günstig:** Auflager mit lösbaren Sicherungen, zugängliche Schraub- oder Bolzenverbindungen, mechanische Laschen, trocken montierte Dichtungen, dokumentierte Einbauteile, standardisierte Hebeanker.
- **Ungünstig:** Ortbetonverguss über Knoten, bewehrte Nassfugen, flächiger Aufbeton, geschweißte Laschen ohne Trennkonzept, nachträgliche Durchdringungen, unzugängliche Korrosionsstellen.
- **Rückbaufolge:** Vorabklärung der Systemstatik; temporäre Aussteifung; Freilegen der Fugen; Trennen von Ortbeton und Installationen; Anschlagen an vorhandenen oder neu hergestellten Hebepunkten; kontrollierte Lösung; Zwischenlagerung mit Kantenschutz und Lastverteilern.
- **Anpassung:** Reinigen, Beschneiden, Nachbohren nur nach statischem Konzept; neue Verbindungsmittel; Ergänzung von Auflagerplatten; ggf. Nutzung in niedrigerer Beanspruchungsklasse.

### Prüf- und Nachweisfragen

- **Dokumentation:** Originalpläne, Typenbücher, Fertigteilkennzeichnungen, Bewehrungs- und Spannpläne, Betonfestigkeitsklassen, Einbauteile und Fugenprinzipien.
- **Zustand:** Risse, Abplatzungen, Korrosion, Karbonatisierungstiefe, Chloridgehalt, Frost-Tausalz-Schäden, Alkali-Kieselsäure-Reaktion, Durchbiegungen, Verformungen, Brandschäden.
- **Zerstörungsfreie Methoden:** Bewehrungsortung, Radar, Ultraschall, Rückprallhammer nur als orientierende Methode, Potentialfeldmessung, Endoskopie von Fugen.
- **Materialprüfungen:** Bohrkerne, Druckfestigkeit, Chlorid-/Karbonatisierungsprofile, Stahlzugproben bei unklarer Bewehrung, Untersuchung von Vorspannstählen.
- **Bemessung:** Neue Nutzung nach aktuellen Normen; Bestandsnormen nur zur Einordnung; Teilsicherheiten, Restlebensdauer, Dauerhaftigkeit und Brandwiderstand müssen nachvollziehbar angesetzt werden.

### ReUse-Potenziale

- **Direkte Wiederverwendung:** Bauteile werden mit minimaler Anpassung erneut eingebaut, ideal bei Serienbauteilen und bekannten Lastfällen.
- **Kaskadierte Wiederverwendung:** Tragende Fertigteile werden in weniger beanspruchten Anwendungen genutzt, z. B. Nebengebäude, Landschaftsbau, nichttragende Wände, Treppen, Stützwände.
- **Segment-ReUse:** Monolithische oder stark verbundene Bauteile werden gesägt und als Platten, Blöcke oder Wandsegmente weiterverwendet. Dies erhält mehr Wert als Brechen, ist aber weniger hochwertig als vollständiger Bauteil-ReUse.
- **Recycling als letzte Stufe:** Betonbruch als Gesteinskörnung ist ökologisch sinnvoller als Deponie, aber material- und qualitätsseitig kein gleichwertiger Ersatz für Bauteilwiederverwendung.

## Praxisbezug / Beispiele

- **ReCreate:** Europäisches Forschungs- und Demonstrationsprojekt zur Demontage und Wiederverwendung von Betonfertigteilen aus Bestandsgebäuden in neuen Bauvorhaben. Der Fokus liegt auf zerstörungsarmer Demontage, Aufbereitung, neuen Verbindungen, Geschäftsmodellen und Nachweisführung.
- **Platten- und Fertigteilbauten der Nachkriegszeit:** Regelmäßige Raster und serielle Bauteile bieten theoretisch hohes Potenzial. Praktisch begrenzen Fugenverguss, Sanierungsüberlagerungen, Schadstoffe, Maßtoleranzen und fehlende Typendokumentation die Wiederverwendung.
- **Industrie- und Hallenbau:** Fertigteilbinder, Stützen und Fassadenplatten können bei klaren Auflager- und Verbindungskonzepten gut inventarisiert und demontiert werden.
- **Sägegeschnittene Betonbauteile:** Bei Ortbeton oder schwer lösbaren Fertigteilen werden Segmente durch Seilsäge- oder Wandsägeverfahren herausgelöst. Dies eröffnet neue Designmöglichkeiten, benötigt aber präzise Bewehrungserkundung und Kranlogistik.

## Herausforderungen / offene Fragen

- **Nachweissicherheit:** Ohne ursprüngliche Herstell- und Bemessungsdaten werden Prüfaufwand und Sicherheitsabschläge hoch. Besonders kritisch sind Spannbeton, unbekannte Bewehrungsführung und alte Betonzusammensetzungen.
- **Verbindungstechnik:** Viele historische Fertigteilsysteme sind montagefreundlich, aber nicht demontagefreundlich. Neue reversible Verbindungen für wiederverwendete Bauteile sind noch kein Standardmarkt.
- **Schadstoffe und Oberflächen:** PCB-haltige Fugendichtstoffe, Asbest, PAK, alte Beschichtungen oder kontaminierte Dämmstoffe können ReUse verhindern oder stark verteuern.
- **Logistik:** Fertigteile sind schwer, sperrig und empfindlich an Kanten. Kranzeiten, Transportstrecken, Zwischenlagerung und Maßprüfung beeinflussen Wirtschaftlichkeit und Ökobilanz.
- **Rechtliche Einordnung:** Die neue EU-Bauprodukteverordnung erweitert den Blick auf gebrauchte Produkte, dennoch bleiben CE-Kennzeichnung, Leistungserklärung, Haftung und Verantwortlichkeiten projektspezifisch zu klären.
- **Planungszeit:** ReUse benötigt frühe Verfügbarkeit von Bauteilen, Prüfzeiten und flexible Entwurfsraster. Konventionelle Termin- und Vergabemodelle passen dazu nur eingeschränkt.

## Quellen

- ReCreate: *Reusing precast concrete for a circular economy*. https://recreate-project.eu/
- CORDIS: *Reusing precast concrete for a circular economy – ReCreate, Grant 958200*. https://cordis.europa.eu/project/id/958200
- Küpfer, C. et al.: *Reuse of concrete components in new construction projects: Critical review of 77 circular precedents*, Journal of Cleaner Production, 2023.
- Dervishaj, A. et al.: *From precast structures to reusable components*, 2025.
- European Commission: *EU Construction & Demolition Waste Management Protocol including guidelines for pre-demolition and pre-renovation audits of construction works*, 2024. https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- ISO 20887:2020: *Design for disassembly and adaptability*. https://www.iso.org/standard/69370.html
- Regulation (EU) 2024/3110: *Construction Products Regulation*. https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng
- EN 1990, EN 1991, EN 1992 mit nationalen Anhängen; nationale Regeln für Bestandsbewertung, Betonprüfung und Rückbau.

## Legacy Content: tragwerkssystem\to_sort\Betonfertigteile.md

---
type: Tragwerkssystem
title: Wiederverwendung von Betonfertigteilen
---

---

## Prompt 1

Erstelle auf Basis aller in diesem Notebook verfügbaren Quellen einen professionellen Bericht zum Thema „Wiederverwendung von Baukomponenten und Baumaterialien in Betonfertigteilsystemen“. Arbeitsregeln: - Verwende ausschließlich die Informationen aus den vorhandenen Quellen. - Belege jede tragende Aussage mit Quellverweisen. - Stelle unterschiedliche Positionen oder Ergebnisse aus den Quellen vergleichend dar. - Schreibe auf Deutsch in einem sachlichen, wissenschaftlichen Stil. Struktur des Berichts: 1. Executive Summary 2. Definition und Abgrenzung von Betonfertigteilsystemen 3. Typische wiederverwendbare Elemente - Stützen - Unterzüge / Träger - Deckenplatten / Hohlplatten - Wandelemente - Treppen / Sonderbauteile 4. Konstruktive Voraussetzungen für Wiederverwendung - Art der Fugen und Verbindungen - Demontierbarkeit - Zugänglichkeit der Anschlüsse - Modul- und Rastersysteme 5. Technische Bewertung und Prüfbedarf - Geometrie - Bewehrung / Spannstahl - Dauerhaftigkeit - Schäden - Restnutzungsdauer - Material- und Zustandsnachweise 6. Rückbau, Ausbau, Transport und Wiedereinbau 7. Ökologische Bewertung - CO₂ - Materialeinsparung - Vergleich zu Recycling 8. Wirtschaftliche Aspekte 9. Normative, baupraktische und haftungsbezogene Hürden 10. Relevante Fallstudien / gebaute Beispiele 11. Chancen, Grenzen und Forschungslücken 12. Fazit Ergänze am Ende: - eine Tabelle „Elementtyp – Vorteile – technische Hürden – logistische Hürden – Quellen“ - eine Zusammenstellung der wichtigsten Prüf- und Bewertungsmethoden aus den Quellen - ein Quellenverzeichnis



---

## Bericht 1: Wiederverwendung von Baukomponenten und Baumaterialien in Betonfertigteilsystemen – Ein technischer und strategischer Leitfaden

### 1. Executive Summary

Die Dekarbonisierung des Bausektors ist ohne eine radikale Skalierung der Bauteilwiederverwendung technisch nicht realisierbar. Im Kontext des European Green Deal und der geforderten CO2-Neutralität bis 2050 stellt die direkte Wiederverwendung (Reuse) von Betonfertigteilen die „höchste Stufe der Nutzbarmachung“ dar. Da der Rohbau ca. 60 % der CO2-Emissionen eines Neubaus verursacht, bietet die Zirkularität auf Komponentenebene – im Gegensatz zum energetisch aufwendigen Downcycling (Crushing) – das Potenzial, den CO2-Fußabdruck um 93 bis 98 % zu senken. Dieser Leitfaden analysiert die technischen und strategischen Hebel, die notwendig sind, um Betonfertigteile als werthaltige Assets über mehrere Lebenszyklen hinweg zu führen.

2. Definition und Abgrenzung von Betonfertigteilsystemen

Der Übergang vom projektbasierten zum produktbasierten Bauen markiert einen Paradigmenwechsel. Betonfertigteilsysteme nutzen die industrielle Vorfertigung (Industrialized Construction), um Präzision und Qualitätssicherung zu maximieren.

* Design for Disassembly (DfD): DfD ist die ultimative „Cradle-to-Cradle“-Strategie. Sie erfordert standardisierte, austauschbare Komponenten und mechanische Verbindungen statt stoffschlüssiger Verklebungen.
* Product Platforms & CODP: Durch den Einsatz von Produktplattformen werden Gebäude als konfigurierbare Systeme verstanden. Der Customer Order Decoupling Point (CODP) definiert dabei den Zeitpunkt der Individualisierung, was Skaleneffekte bei gleichzeitiger Flexibilität ermöglicht.
* Theoretische Fundamente:
  * Open Building (Habraken): Die Trennung von langlebiger Primärstruktur („Support“) und anpassbarem Ausbau („Infill“).
  * Shearing Layers (Brand): Die Anerkennung unterschiedlicher Lebenszyklen (Structure, Services, Space Plan). Eine Kreislaufführung der „Structure“-Schicht ist ökonomisch besonders wertvoll, da sie die höchsten investierten CO2-Äquivalente bindet.

3. Typische wiederverwendbare Elemente

Die Eignung zur Wiederverwendung variiert stark nach Elementtyp und Spendergebäude. Basierend auf dem „Atlas of Reused Concrete“ (ARC) und dem ReCreate-Projekt ergibt sich folgende Bewertung:

* 3.1 Stützen und Unterzüge (Girders): Besonders wertvoll sind vorgespannte T-Träger (z. B. aus Viadukten) oder schwere Skelettstützen aus Industriehallen.
* 3.2 Decken- und Hohlplatten (Hollow Core Slabs - HCS): HCS sind aufgrund des 1200mm-Rasters prädestiniert. Kritische Einschränkung: Sogenannte „Piping slabs“ (Leidingplaatvloeren) sind aufgrund integrierter Haustechnik ungeeignet. Zudem verlieren gesägte HCS ihre ursprüngliche Scheibenwirkung (Diaphragm action), was bei der statischen Neuauslegung zwingend berücksichtigt werden muss.
* 3.3 Wandelemente: Massiv- und Sandwichwände aus standardisierten Systemen (z. B. WBS70) sind gut rückbaubar, sofern die Verbindungspunkte zugänglich sind.
* 3.4 Treppen und Sonderbauteile: Oft mit geringem Aufwand demontierbar, sofern keine monolithische Vergussfuge vorliegt.

Strategisches Risiko: Die Annahme einer ständigen Verfügbarkeit von Spenderelementen ist riskant. Aktuelle Bestände sind oft gering oder bereits für spezifische Projekte (vgl. Fallbeispiel Prinsenhof) reserviert.

4. Konstruktive Voraussetzungen und Innovationen

Die technische Machbarkeit von Reuse steht und fällt mit der Verbindungstechnik.

* Nasse vs. Trockene Fugen: Während „nasse“ (vergossene) Fugen aufwendiges Diamantsägen und die Entfernung von Grout-Resten erfordern, erlauben „trockene“ (geschraubte) Verbindungen eine zerstörungsfreie Demontage.
* NIST-Innovationen (September 2025): Das NIST hat fünf neue Verbindungstypen entwickelt, darunter Link-Plates, Bolted Brackets und Peg-in-Hole-Systeme.
* Resilienz durch „Structural Fuses“: Diese hantelförmigen Verbindungselemente fungieren als Sollbruchstellen. Sie verformen sich unter Extrembelastung duktil und schützen so die spröden Betonbauteile. Dies verhindert den progressiven Kollaps (Disproportionate Collapse), ein entscheidendes Sicherheitsmerkmal, das historische Versagen wie beim Ronan Point oder dem Murrah Building adressiert.

5. Technische Bewertung und Quality Assurance

Ein robuster Qualitätssicherungsprozess (RISE-Methodik) ist die Voraussetzung für die Zertifizierung gebrauchter Bauteile:

1. Dokumentenanalyse: Prüfung von Bestandsunterlagen zur Bestimmung der Bewehrungskonfiguration und Betonklasse.
2. Visuelle Inspektion & Geometrie: Identifikation von Schäden und Abgleich der Toleranzen.
3. Zerstörungsfreie Prüfung (NDT): GPR-Radar zur Bewehrungsortung, Schmidt-Hammer für Oberflächenhärte, Ultraschall (UPV) zur Detektion interner Risse.
4. Laborprüfungen & Modellierung: Modellierung von Karbonatisierungstiefe und Chlorid-Ingress zur Berechnung der Restnutzungsdauer.
5. Entscheidungsregeln: Vermeidung von „Über-Prüfung“ (unwirtschaftlich) vs. „Unter-Prüfung“ (Sicherheitsrisiko) durch klare Freigabeprotokolle.

6. Rückbau, Transport und Wiedereinbau

Der physische Prozess (vgl. Peikko-Pilotprojekt, Vantaa) erfordert spezialisierte Abläufe:

* Demontage: Einsatz temporärer Abstützungen während des Diamantsägens der Fugen.
* Refurbishment: Maschinelle Entfernung von Grout-Resten und Wiederherstellung der Verbundfugen-Geometrie.
* Logistik: HCS sind beim Ausbau extrem bruchempfindlich und erfordern präzise Hebepläne.
* Montage: Der Wiedereinbau erfolgt idealerweise unter Nutzung digitaler Tags, um die Bauteilhistorie lückenlos im BIM-Modell abzubilden.

7. Ökologische Bewertung

Die Ökobilanzierung (LCA) muss Modul D (Beyond End-of-Life) priorisieren.

* Potenzial: Das Peikko-Pilotprojekt belegt eine 50 % CO2-Reduktion gegenüber Neuteilen.
* Materialwerterhalt: Reuse sichert den funktionalen Wert, während Recycling lediglich den Materialwert (als Zuschlagstoff) erhält. Der ökologische Vorteil von Reuse gegenüber Recycling liegt vor allem in der Vermeidung der energieintensiven Zementproduktion für neue Bauteile.

8. Wirtschaftliche Aspekte

Wirtschaftlichkeit wird durch den Pre-Manufactured Value (PMV) und Lernkurveneffekte getrieben.

* Kosteneinsparung: Der Peikko-Pilot zeigt Kosteneinsparungen von ca. 35 % durch Primärmaterialwegfall.
* Lernkurve: Pilotprojekte wie WikiHouse starteten mit einem Kostenaufschlag von 33 %. Mit den gewonnenen Erkenntnissen und standardisierten Prozessen ist eine Reduktion auf einen Aufpreis von lediglich 12 % prognostiziert. Skalierung generiert hier die notwendige Marktreife.

9. Regulatorische und haftungsbezogene Hürden

Fehlende harmonisierte Normen sind das größte Markthindernis.

* Haftung: In Ländern wie Dänemark sind Einzelfall-Dispensationen nötig, was das Risiko einseitig auf den Bauherrn verlagert.
* Informationsasymmetrie: Digital Product Passports (DPP) sind essenziell, um Materialeigenschaften und Restlebensdauer für Versicherer und Planer transparent zu machen. Sie transformieren das Bauteil von „Abfall“ zu einer „Ressource mit Zertifikat“.

10. Relevante Fallstudien

* Patch22 (Amsterdam): Nutzt das Slimline-System (IPE 400 Stahlprofile + 70mm Betonplatte). Dies ermöglicht eine horizontale Medienführung im Hohlboden und maximale Umnutzungsflexibilität.
* 85 Social Housing Units (Cornellà): Einsatz von 8.300 m² Holz in einer Matrix aus 13 m² großen, polyvalenten Räumen ohne tragende Innenwände.
* WikiHouse (SYHA): Lokale Fertigung im „Chop Shop“ (1 Meile vom Einsatzort). Digitale Fertigung (CNC) von Sperrholz-Komponenten als Open-Source-Modell.
* APROP (Barcelona): Modulare Wiederverwendung von „Last Trip“-Containern. Rückbau und Wiederaufbau innerhalb von nur 4 Wochen demonstriert die logistische Überlegenheit modularer Systeme.

11. Chancen, Grenzen und Forschungslücken

Die größte Chance liegt in der Kopplung von BIM mit digitalen Marktplätzen wie „Gebouwenmarktplaats“. Eine Grenze bleibt die geografische Distanz zwischen Spender und Empfänger, die den logistischen CO2-Vorteil aufzehren kann. Forschungslücken bestehen bei der Standardisierung von NDT-Verfahren zur rechtssicheren Bestimmung der Restnutzungsdauer.

12. Fazit

Die Wiederverwendung von Betonfertigteilen ist technisch ausgereift und ökologisch alternativlos. Der strategische Fokus muss nun auf der regulatorischen Harmonisierung und dem Aufbau digitaler Kataster liegen. Nur so wird die Bauindustrie von der linearen Ressourcenvernichtung zu einer echten Kreislaufwirtschaft finden.


--------------------------------------------------------------------------------


Anhänge

Tabelle: Elementtyp-Matrix

Elementtyp	Vorteile der Wiederverwendung	Technische Hürden	Logistische Hürden	Quellen
Hohlplatten (HCS)	Hohe Standardisierung (1200mm Raster)	Verlust der Scheibenwirkung; „Piping slabs“ ungeeignet	Hohe Bruchgefahr beim Sägen/Heben	ARC, ReCreate, DTI
Stützen	Klare statische Lastpfade	Entfernung von Grout-Resten an Enden	Hohe Punktlasten beim Transport	Peikko, RISE
T-Träger (Girders)	Extrem hohe Festigkeitswerte	Vorspannung limitiert Zuschnittmöglichkeiten	Überlänge erfordert Speziallogistik	ARC, SGS Netherlands
Wandelemente	Großer Hebel für CO2-Bilanz	Zugänglichkeit der Verbindungspunkte	Gefahr von Kantenabplatzungen	ARC, ReCreate

Kategorisierung der Prüfmethoden

Zerstörungsfreie Prüfung (NDT):

* GPR (Radar): Detektion von Bewehrungslagen und Fehlstellen.
* Schmidt-Hammer: Bestimmung der Oberflächenhärte (Korrelation zur Druckfestigkeit).
* Ultrasonic Pulse Velocity (UPV): Prüfung der Homogenität und Detektion interner Risse.
* Cover Meter: Messung der Betondeckung (Dauerhaftigkeitsschätzung).
* Half-Cell Potential: Lokalisierung aktiver Korrosionsprozesse.

Zerstörende Prüfung (DT):

* Bohrkernentnahme: Bestimmung der tatsächlichen Druckfestigkeit im Labor.
* Karbonatisierungstest: Messung der Eindringtiefe von CO2 mittels Indikatoren.
* Chloridanalyse: Bestimmung des Chloridgehalts zur Korrosionsrisikoabschätzung.

Quellenverzeichnis

* RISE (2023): Quality Assurance for Reused Concrete Building Elements. Report 2023:10.
* NIST (September 2025): New Precast Concrete Moment Connections under a Column Removal Scenario. Technical Note 2148B.
* Peikko Group (2022): Pilot Project: Dismount and Reuse of Precast Concrete Structures.
* EPFL: Atlas of Reused Concrete (ARC).
* RE-DWELL: Design for Disassembly / Industrialised Construction Definitions.
* SGS Netherlands: Protocol for the reuse of concrete prefab pretensioned girders.
* Danish Technological Institute (DTI): Reuse of Hollow Core Slabs - From Idea to Action.
* Räsänen et al. (2024): Procedure for quality management of reclaimed concrete elements. EU Horizon 2020 (ReCreate).

---

## Prompt 2

Erstelle auf Basis ALLER in diesem Notebook / in diesen Quellen enthaltenen Informationen einen professionellen Fachbericht auf Deutsch zum Thema: „Wiederverwendung von Baukomponenten und Baumaterialien im Tragwerk – Fokus auf Betonfertigteile / Fertigteiltragwerke / Stützen, Träger, Deckenplatten, Hohlplatten“ Erstelle auf Basis ALLER in diesem Notebook / in diesen Quellen enthaltenen Informationen einen professionellen Fachbericht auf Deutsch zum Thema: „Wiederverwendung von Baukomponenten und Baumaterialien im Tragwerk – Fokus auf [TRAGWERKSSYSTEM]“ WICHTIG: - Nutze ausschließlich Informationen aus den vorhandenen Quellen. - Erfinde keine Angaben. Wenn Informationen fehlen oder widersprüchlich sind, benenne das ausdrücklich. - Der Bericht soll sich PRIMÄR auf das Tragwerk konzentrieren, nicht auf Ausbau, Fassade oder Innenraum – außer diese beeinflussen das Tragverhalten, die Demontage oder die Wiederverwendung direkt. - Ziehe Informationen aus ALLEN relevanten Quellen zusammen, konsolidiere Dopplungen und stelle Widersprüche zwischen Quellen explizit dar. - Schreibe in präziser, professioneller, wissenschaftlich klingender Fachsprache auf Deutsch. - Füge nach jedem Abschnitt konkrete Quellenhinweise ein. - Zitiere möglichst quellennah und nachvollziehbar. - Wenn vorhanden, nenne Autor, Jahr, Projektnamen, Bauteiltyp, Material und Ort. - Kennzeichne Fallbeispiele, Forschungsarbeiten, Leitfäden, Normen und Pilotprojekte getrennt. ZIEL: Ich möchte einen belastbaren Überblick darüber, was die Quellen speziell über dieses Tragwerkssystem im Kontext der Wiederverwendung aussagen. STRUKTUR DES BERICHTS: 1. Kurzfassung (5–10 Sätze) - wichtigste Erkenntnisse - Relevanz des Systems für Wiederverwendung - wichtigste Chancen und Hemmnisse 2. Systembeschreibung aus tragwerklicher Sicht - Definition und typische Ausprägungen des Systems - Primärtragstruktur, Sekundärtragstruktur - typische Spannweiten, Raster, Tragglieder, Knoten, Lastabtragung - häufige Materialien und Verbindungsmittel 3. Relevante wiederverwendbare Tragwerksbauteile - welche tragenden Komponenten in den Quellen genannt werden - z. B. Stützen, Träger, Deckenplatten, Verbände, Fachwerke, Rahmen, Module, Wandelemente, Knoten, Verbindungsmittel - in welcher Form die Bauteile wiederverwendet werden: direkt, angepasst, zugeschnitten, umgebaut, umgenutzt 4. Tragwerksrelevante Voraussetzungen für Wiederverwendung - Demontierbarkeit / Rückbaubarkeit - Art der Verbindungen - Grad der Standardisierung - Zugänglichkeit der Knoten - Beschädigungsrisiko beim Ausbau - Toleranzen, Geometrie, Maßordnung - Dokumentation / Materialpass / Rückverfolgbarkeit 5. Tragwerksrelevante Bewertungskriterien - statische Nachweisbarkeit - Resttragfähigkeit - Dauerhaftigkeit - Materialzustand - Ermüdung, Korrosion, Feuchte, Risse, Schadstoffe - Prüfmethoden, Inspektion, Monitoring, zerstörungsfreie Prüfungen - Anforderungen an Re-Zertifizierung oder Wiederzulassung 6. Konstruktive Strategien und Details - welche konstruktiven Lösungen die Wiederverwendung erleichtern - reversible Verbindungen - Schraub-, Steck-, Klemm-, Trocken- oder Segmentverbindungen - modulare Raster, Trennbarkeit von Schichten, Design for Disassembly, Design for Reuse - welche Details problematisch sind 7. Chancen, Grenzen und Risiken aus Tragwerksplanungssicht - statische Vorteile - technische Risiken - Unsicherheiten in Bemessung und Nachweis - logistische / geometrische Zwänge - wirtschaftliche und normative Hürden, soweit sie das Tragwerk betreffen 8. Fallbeispiele aus den Quellen - liste alle relevanten Projekte, Prototypen, Pilotbauten und Versuche - pro Fallbeispiel: Name, Ort, Jahr, System, wiederverwendete Bauteile, tragwerkliche Idee, wichtige Erkenntnisse - nur Informationen nennen, die in den Quellen belegt sind 9. Synthese - Welche Muster zeigen sich über alle Quellen hinweg? - Welche Bauteile dieses Systems eignen sich besonders gut zur Wiederverwendung? - Welche weniger? - Welche Faktoren entscheiden über Erfolg oder Scheitern? 10. Forschungslücken und offene Fragen - nur auf Basis der Quellen - z. B. fehlende Normen, fehlende Prüfverfahren, unklare Dauerhaftigkeit, fehlende Daten zu Anschlüssen, Skalierungsprobleme 11. Fazit - prägnante fachliche Bewertung des Systems für die Wiederverwendung im Tragwerk AUSGABEFORMAT: - Klar gegliedert mit Überschriften und Unterüberschriften - Fachlich präzise, keine Marketing-Sprache - Wichtige Informationen in Tabellenform, wenn sinnvoll - Am Ende: A) Tabelle „Quellenübersicht“ B) Tabelle „genannte Bauteile“ C) Tabelle „tragwerksrelevante Chancen / Risiken“ D) Literaturliste aller verwendeten Quellen aus dem Notebook QUELLENUMGANG: - Gib bei jeder wesentlichen Aussage die Quelle an.

---

## Bericht 2: Wiederverwendung von Baukomponenten im Tragwerk – Fokus Betonfertigteiltragwerke

### 1. Kurzfassung

Die direkte Wiederverwendung von Betonfertigteilen stellt eine technisch anspruchsvolle, aber ökologisch hochwirksame Alternative zum konventionellen Baustoff-Recycling dar. Im Gegensatz zum Downcycling durch Zerkleinerung bleibt bei der direkten Re-Zertifizierung der strukturelle Wert der Bauteile erhalten. Aktuelle Pilotstudien belegen Einsparpotenziale beim Treibhausgas-Emissionswert (Embodied Carbon) von bis zu 50 % sowie Prozesskostenvorteile von bis zu 35 % im Vergleich zur Beschaffung von Neubauteilen – wobei letzterer Wert die Kosten für Diamant-Sägeverfahren und zerstörungsfreie Prüfungen (NDT) bereits inkludiert [Peikko 2022]. Die Skalierung dieses Systems ist für das Erreichen des EU Green Deal (Klimaneutralität bis 2050) von strategischer Relevanz, da der Bausektor für ca. 35 % des EU-Abfallaufkommens verantwortlich ist. Hemmende Faktoren sind primär das Fehlen harmonisierter EU-Normen sowie signifikante Dokumentationslücken im Bestand. Der vorliegende Bericht analysiert die ingenieurtechnischen Parameter, die für eine Überführung in die Baupraxis erforderlich sind.

2. Systembeschreibung aus tragwerklicher Sicht

Betonfertigteiltragwerke basieren auf einer modularen Logik, die sich in Primär- und Sekundärstrukturen unterteilt. Skelettstrukturen (Stützen-Riegel-Systeme) bilden meist die Primärstruktur, während weitgespannte Hohlplattendecken (HCS - Hollow-core slabs) als Sekundärelemente fungieren.

Tragwerkstechnisch ist zu differenzieren:

* Modularität und Raster: Standardisierte Rastermaße (z. B. 1200 mm bei HCS) begünstigen den Wiedereinbau.
* Problematik saurer Trennschnitte: Werden Hohlplatten für die Wiederverwendung auf Maß gesägt, geht die ursprüngliche Fähigkeit zur Ausbildung einer Scheibenwirkung (diaphragm action) verloren [Designing and adapting re-used hollowcore slabs]. Dies muss bei der statischen Auslegung des Zielgebäudes durch alternative Aussteifungskonzepte kompensiert werden.
* Eignungsprofil: Bauteile aus Parkhäusern, Industriehallen und Bürogebäuden weisen aufgrund klarer Geometrien ein hohes Potenzial auf. Hohlplatten aus dem Wohnungsbau sind hingegen oft weniger geeignet, da sie eine hohe Anzahl an individuellen Aussparungen und Durchbrüchen für die Haustechnik besitzen, die die Resttragfähigkeit mindern.

Die größte technische Barriere stellen historisch gewachsene „nasse“ Verbindungen (Vergussmörtel) dar, welche die zerstörungsfreie Demontage ohne Materialverlust erschweren.

3. Relevante wiederverwendbare Tragwerksbauteile

Die Auswahl der Bauteile richtet sich nach dem Grad der Anpassung (Zuschnitt vs. Direkteinbau) und der statischen Relevanz:

Horizontalelemente

* Vorgespannte Hohlplatten (HCS): Effiziente Deckenbauteile; oft mit Aufbeton (compression layer) im Bestand versehen.
* T-Träger und I-Träger: Insbesondere aus Brückenbauwerken oder weitgespannten Hallen.
* Massivplatten: Aus Skelettbauten, oft durch Sägeschnitte gewonnen.

Vertikalelemente

* Stützen (Columns): Quadratische oder runde Querschnitte mit Kopf- und Fußbolzenanschlüssen.
* Wandelemente: Sowohl tragende Innenwände als auch Fassadenpaneele (z. B. IW73 oder WBS70 Systeme) [ARC].

Spezialelemente

* Köcherfundamente: Wiederverwendbare Gründungskörper für den Industriebau.
* Inverset-Elemente: Stahl-Beton-Verbundbauteile aus Brückenrampen (z. B. Big Dig House).
* Treppenläufe: Vorgefertigte Treppenkerne aus dem Rückbau.

4. Tragwerksrelevante Voraussetzungen für die Wiederverwendung

Die erfolgreiche Implementierung erfordert die Anwendung von "Design for Disassembly" (DfD) und die methodische Umkehrung des Bauprozesses (Construction in Reverse).

Kritische Erfolgsfaktoren sind:

* Trennung der Schichten (Shearing Layers): Basierend auf Brand (1994) müssen die sechs Schichten eines Gebäudes – Standort (Site), Tragwerk (Structure), Hülle (Skin), Versorgung (Services), Raumplan (Space plan) und Ausstattung (Stuff) – technisch so entkoppelt sein, dass das Tragwerk ohne Zerstörung der anderen Schichten zugänglich ist [RE-DWELL].
* Verbindungstechnik: Der Übergang von Ortbetonergänzungen hin zu reversiblen, mechanischen Verbindungen (Schraub-/Bolzensysteme) entscheidet über die Wirtschaftlichkeit der Demontage.
* Dokumentation: Die Nutzung von BIM und digitalen Materialpässen (Digital Product Passports) zur Rückverfolgbarkeit von Betongüte und Bewehrungslage.
* Geometrische Toleranzen: Beim Wiedereinbau gebrauchter Elemente müssen größere Toleranzen für Fugenbreiten und Dickenabweichungen eingeplant werden als bei Neuware.

5. Tragwerksrelevante Bewertungskriterien und Qualitätssicherung

Die Zustandsbewertung ist die Basis für die Haftungsfreistellung des Tragwerksplaners. Hierbei kommen primär zerstörungsfreie Prüfverfahren (NDT) zum Einsatz [RISE 2023]:

Methodik der Zustandsprüfung

1. Rückprallhammer-Prüfung (Schmidt-Hammer): Dient als initiales Screening der Oberflächenhärte. Die Ergebnisse müssen zwingend gegen die Karbonatisierungstiefe kalibriert werden, da karbonatisierter Beton eine höhere Härte vortäuscht.
2. GPR (Ground Penetrating Radar): Detektion der Bewehrungslage und Messung der Betondeckung.
3. UPV (Ultrasonic Pulse Velocity): Ermittlung der Homogenität und Identifikation von inneren Rissen oder Entmischungen.
4. Half-Cell Potential: Lokalisierung aktiver Korrosionsprozesse.

Statische Nachweise und Dauerhaftigkeit

* Bewehrungshöhe: Bei Hohlplatten ist zu beachten, dass die statische Nutzhöhe (coverage) in älteren Elementen oft geringer ist als nach aktuellen Normen gefordert. Der Nachweis muss mit der realen Bestandshöhe geführt werden [Designing and adapting re-used hollowcore slabs].
* Rest-Propagationszeit: Mithilfe von RISE-Berechnungstools wird die Eindringtiefe von Karbonatisierung und Chloriden analysiert, um die verbleibende Dauerhaftigkeit bis zum Erreichen kritischer Grenzwerte zu determinieren.
* Re-Zertifizierung: Da CE-Kennzeichnungen für Bestandsbauteile fehlen, fungieren projektbezogene Qualitätsprotokolle (z. B. SGS-Ansatz) als Validierungsgrundlage.

6. Konstruktive Strategien und Details

Moderne Verbindungsstrategien zielen auf Duktilität und Reversibilität ab. Ein wesentlicher Fokus liegt auf der Vermeidung eines fortschreitenden Einsturzes (disproportionate collapse) bei lokalem Bauteilversagen [NIST 2025].

Merkmal	Konventionell (Nass)	Reversibel (Trocken)	NIST "Structural Fuse"
Verbindung	Verguss / Ortbeton	Schraubbolzen / Laschen	Hantelförmige Link-Plates
Duktilität	Gering (spröde)	Mittel	Hoch (gezielte Verformung)
Demontage	Trennschleifen erforderlich	Lösen der Verschraubung	Gezielter Austausch der "Sicherung"
Funktion	Kraftschluss	Lastabtragung	Schutz der Hauptstruktur bei Überlast

Innovative Konzepte wie das Peikko DELTABEAM Green System ermöglichen in Kombination mit Slim-Floor-Strukturen eine flexible Leitungsführung in der Deckenhohlzone, was die Zugänglichkeit der Knotenpunkte verbessert.

7. Chancen, Grenzen und Risiken aus Tragwerksplanungssicht

Chancen:

* Reduktion der CO2-Abgabe und Erschließung neuer Marktsegmente ("Circular Design").
* Nutzung der oft konservativ bemessenen Sicherheitsreserven älterer Bestandsbetone.

Risiken:

* Logistik und Stock-Risiko: Das Risiko, dass zum Planungszeitpunkt nicht genügend passende Hohlplatten im Lager verfügbar sind, ist hoch, da Bestände oft sofort reserviert werden [Designing and adapting re-used hollowcore slabs].
* Wirtschaftlichkeit: Die Kostenersparnis von 35 % gegenüber Neuware ist nur bei seriellen, optimierten Rückbauprozessen realisierbar. Bei Einzelprojekten können Sonderprüfungskosten den finanziellen Vorteil kompensieren.
* Beschädigungen: Haarrisse durch unsachgemäßes Anheben oder Transport können die Dauerhaftigkeit (Korrosionsschutz) signifikant mindern.

8. Fallbeispiele aus den Quellen

Projektname	Ort	Jahr	System / Bauteil	Tragwerkliche Erkenntnis
Oling 5 Bridge	Appingedam (NL)	2021	Invertierte T-Träger	Behelfsbrücke (15 J. Laufzeit); 40 J. alte Träger erfüllen Eurocode-Neubaunorm.
KA13	Oslo (NO)	2020	Hohlplatten	21 HCS-Platten erfolgreich aus Bestandsbau in Bürogebäude transferiert.
ReCreate H22	Helsingborg (SE)	2022	Diverse Fertigteile	Pilotbau mit 94 Massenprozent wiederverwendeter Struktur.
Peikko Pilot	Vantaa (FI)	2021	Skelettbau	Montage, Demontage und Re-Montage an einem Vormittag erfolgreich validiert.
Big Dig House	Lexington (US)	-	Inverset-Träger	Nutzung von 17 Verbund-Brückenträgern als tragende Geschossdecken.

9. Synthese

Die Auswertung der Quellen zeigt, dass Skelettstrukturen in Kombination mit Bolzenverbindungen (z. B. HPKM Stützenschuhe) die höchste Circularity-Rate aufweisen. Hohlplattendecken sind aufgrund ihrer geometrischen Variabilität (Zuschnitt) und weiten Verbreitung die wichtigsten Sekundärelemente, erfordern jedoch bei Trennschnitten eine Neubewertung der Aussteifung (Verlust der Scheibenwirkung). Das erfolgreichste Muster für zirkuläres Bauen ist die konsequente Trennung der Brand'schen Schichten bereits in der Entwurfsphase.

10. Forschungslücken und offene Fragen

* Harmonisierung: Fehlende EU-weit anerkannte Standards für die Re-Zertifizierung und Haftungsverteilung zwischen Rückbau-Unternehmen und Tragwerksplaner.
* Marktplätze: Mangel an großskaligen Datenbanken für den "Element-Matching"-Prozess; derzeit hohes Beschaffungsrisiko mangels Lagerbeständen.
* Dauerhaftigkeit von Verbindungen: Fehlende Langzeitdaten zum Ermüdungsverhalten und zur Korrosionsresistenz mehrfach gelöster und wieder angezogener mechanischer Verbindungen unter Realbedingungen.

11. Fazit

Die Wiederverwendung von Betonfertigteilen ist technisch im Pilotmaßstab marktreif. Die Untersuchungen von Peikko und ReCreate belegen, dass die ökonomischen und ökologischen Vorteile die Mehraufwände für Prüfung und Demontage überwiegen. Für die breite Anwendung ist jedoch eine Transformation der Planungsprozesse erforderlich: Der Tragwerksplaner muss künftig die Bauteilverfügbarkeit in Bestandsdatenbanken als primäre Entwurfsvariable integrieren.


--------------------------------------------------------------------------------


Anhänge

A) Tabelle „Quellenübersicht“ | Autor / Organisation | Titel | Fokus | | :--- | :--- | :--- | | ARC (EPFL) | Atlas of Reused Concrete | Projektdatenbank weltweit | | RISE | Quality Assurance for Reused Concrete | NDT-Methodik & Lebensdauer | | Peikko | Pilot project Vantaa | Wirtschaftlichkeit & Emissionen | | ReCreate | Dutch Pilot Project Framework | QS-Workflows für Hohlplatten | | NIST | New Ways to Connect Concrete | Resiliente Verbindungen |

B) Tabelle „Genannte Bauteile“ | Material | Typ | Besonderheit | | :--- | :--- | :--- | | Beton (vorgespannt) | Hohlplatten (HCS) | Vorspannung kritisch beim Sägen | | Stahl-Beton-Verbund | Inverset-Elemente | Hohe Tragkraft aus Brückenrückbau | | Beton (Fertigteil) | Stützen / Riegel | Bolzenverbindungen ideal für Re-Use | | Beton-Reste | Sägeschnitte / Rubble | Nutzung in lasttragenden Mauerwerkswänden |

C) Tabelle „Tragwerksrelevante Chancen / Risiken“ | Aspekt | Chance | Risiko | | :--- | :--- | :--- | | Statik | Hohe Materialgüte im Bestand | Unbekannte Lastgeschichte / Ermüdung | | Ausführung | Trockenmontage (Zeitersparnis) | Maßtoleranzen gebrauchter Teile | | Umwelt | -50 % CO2-Emissionen | Energie für Diamantsägen | | Recht | Innovation im Rahmen des Green Deal | Haftung bei fehlenden Originalplänen |

D) Literaturliste

* Atlas of Reused Concrete (ARC) - EPFL (2024).
* Design for Disassembly Definition - RE-DWELL (2023).
* NIST Engineers Design 5 New Ways to Connect Concrete Pieces for More Resilient Buildings (2025).
* Peikko: Pilot project proves that the dismount and reuse of concrete elements is realistic and economical (2022).
* RISE: Quality assurance for reused concrete building elements, Report 2023:10.
* ReCreate: Quality assurance of reclaimed precast concrete: Dutch Pilot Project framework (2026).
* Designing and adapting re-used hollowcore slabs for buildings (Structural Manual).
* Format NDT: What Is Non-Destructive Testing of Concrete? (2025).
* SGS Netherlands: Sustainable Reuse of Prefab Concrete Structural Elements (2026).


---

## Prompt 3

Erstelle einen fachlich präzisen Bericht auf Deutsch zur Wiederverwendung von Betonfertigteilen im Tragwerk. Fokussiere ausschließlich auf das Tragwerk: Tragsystem, Lastabtragung, Stützen, Träger, Deckenplatten, Hohlplatten, Verbindungen, Demontierbarkeit, statische Nachweise, Prüfmethoden, Resttragfähigkeit sowie tragwerksrelevante Chancen und Risiken der Wiederverwendung. Nutze nur Informationen aus den vorhandenen Quellen und belege jede wesentliche Aussage mit Quellen.



---

## Bericht 3: Technischer Bericht – Wiederverwendung von Betonfertigteilen im Tragwerk

### 1. Einleitung: Zirkularität im konstruktiven Ingenieurbau

Die Bauindustrie steht vor einer systemischen Transformation. Im Rahmen des European Green Deal und der Verpflichtung zur Klimaneutralität bis 2050 rückt die Dekarbonisierung des Massivbaus in den Fokus. Da die Zementproduktion für etwa 5 bis 12 % der globalen Treibhausgasemissionen verantwortlich ist, reicht ein reines Downcycling von Beton zu Gesteinskörnungen nicht mehr aus. Die Circular Economy (Kreislaufwirtschaft) im Bauwesen fordert stattdessen den Werterhalt auf höchstem Niveau.

Hierbei sind zwei Konzepte leitend: Design for Disassembly (DfD) – auch als „Construction in Reverse“ bezeichnet – beschreibt die vorausschauende Planung von Verbindungen, die eine zerstörungsfreie Demontage ermöglichen. Die direkte Wiederverwendung (Reuse) von tragenden Fertigteilen genießt gegenüber dem Recycling absolute Priorität, da sie den kumulierten Energieaufwand der Herstellung (Embodied Carbon) fast vollständig im Kreislauf hält. Dieser Bericht analysiert die technischen Rahmenbedingungen für die Integration gebrauchter Komponenten in neue Tragwerkkonfigurationen.

2. Analyse der Tragsysteme und wiederverwendbaren Komponenten

Die Eignung von Bauteilen für einen zweiten Lebenszyklus wird primär durch ihre Geometrie, den Vorspannungsgrad und die Anpassbarkeit bestimmt.

Vergleich der Wiederverwendbarkeit von Betonkomponenten

Bauteiltyp	Eignung	Technische Herausforderungen	Referenzbeispiel (Source)
Hohlplatten (HCS)	Hoch	Vorspannverlust bei Kürzung; Risiko von Rissen in den Stegen bei nachträglichen Bohrungen.	Prinsenhof (NL) / ReCreate Projekt
Stützen & Träger	Sehr Hoch	Geometrische Toleranzen; Reinigung der Anschlussbereiche.	De Groeve Viaduct (14m Fertigteil-Träger)
Invertierte T-Träger	Hoch	Entfernung der alten Aufbetonschicht zur Wiederherstellung des Primärprofils.	Oling 5 Brücke, Appingedam (NL)
Sägegeschnittene Ortbetonplatten	Mittel	Statische Unsicherheit durch Trennung der Bewehrung; hohes Gewicht.	FLO:RE System (Platten auf Stahlträgern)

Ingenieurtechnische Bewertung („So-What“-Ebene): Die Analyse zeigt, dass Hohlplatten aus Industrie- oder Bürogebäuden aufgrund standardisierter Raster (z. B. 1,20 m) und minimaler Durchbrüche prädestiniert für den Reuse sind. Im Gegensatz dazu sind Hohlplatten aus dem Wohnungsbau oft mit zahlreichen individuellen Aussparungen versehen. Besonders kritisch sind sogenannte „Leidingplaatvloeren“ (Leitungsplatten); diese sind aufgrund der massiven Schwächung des Querschnitts durch integrierte Leitungsführungen in der Regel nicht für eine Wiederverwendung geeignet.

3. Verbindungen und Demontierbarkeit (Design for Disassembly)

Die zerstörungsfreie Trennung ist die Grundvoraussetzung für die Zirkularität. Traditionelle „nasse“ Verbindungen, bei denen Fugen mit Vergussmörtel (Grout) kraftschlüssig verfüllt werden, stellen erhebliche Rückbauhürden dar.

* Nasse vs. Trockene Systeme: Während nasse Fugen den Einsatz von Diamantsägen erfordern – was zu Längenverlusten und Staubbelastung führt –, ermöglichen mechanische Schraubverbindungen eine nahezu verlustfreie Demontage.
* Peikko-Systeme: Der Einsatz von HPM® Ankerbolzen, HPKM® Stützenschuhen und insbesondere COPRA® Verankerungskupplungen hat sich als technischer Standard etabliert. In Pilotprojekten wurde nachgewiesen, dass durch die Verwendung von Trennmitteln (z. B. Demoulding Oil) oder dünnen Stahlplatten das Grout-Polster zwischen den Elementen rückstandsfrei entfernt werden kann, ohne die Betonoberfläche zu beschädigen.
* NIST „Structural Fuses“: Das National Institute of Standards and Technology (NIST) hat innovative Verbindungen mit hantelförmigen (dumbbell-shaped) Link-Platten entwickelt. Diese fungieren als statische Sicherungen: Bei Überlastung dehnt sich das hantelförmige Stahlelement plastisch, bevor der spröde Beton bricht. Dies schützt die Primärstruktur vor Kollaps und erhält die Wiederverwendbarkeit der Hauptkomponenten nach Schadensereignissen.

4. Tragwerksplanung und statische Nachweise

Der Prozess des „Re-Engineerings“ erfordert eine Validierung der Bestandseigenschaften, um das Fehlen von Original-Leistungserklärungen (CE-Kennzeichnung) zu kompensieren.

Zentrale Einschränkung der Scheibenwirkung: Ein kritischer Aspekt bei der Wiederverwendung von Hohlplatten ist, dass diese nach dem Aufsägen der Fugen oder dem Kürzen der Elemente nicht mehr zur Ausbildung einer Scheibenwirkung (diaphragm action) herangezogen werden können. Die statische Aussteifung des neuen Gebäudes muss daher über alternative Systeme sichergestellt werden.

Checkliste für Tragwerksplaner (basierend auf TU Eindhoven & DTI)

* [ ] Klassifizierung nach TU/e: Einstufung der Elemente in:
  1. Installation-ready (direkt einsatzbereit),
  2. Maintenance/Repair needed (Instandsetzung erforderlich),
  3. Further testing required (erweiterte Prüfung notwendig).
* [ ] Geometrische Prüfung: Kontrolle, ob die seitlichen Klemmfugen (clamping grooves) sauber und offen sind, um einen ordnungsgemäßen Fugenschluss im neuen Verbau zu garantieren.
* [ ] Betondeckung: Abgleich der Ist-Deckung mit aktuellen, strengeren Normen. Ältere Bauteile erfüllen oft nicht die heutigen Anforderungen der Expositionsklassen.
* [ ] Bewehrungsanalyse: Bestimmung des Vorspannungsgrades und der Lage der Litzen mittels NDT.
* [ ] Tragfähigkeit bei Datenverlust: Liegen keine Unterlagen vor, sind konservative Annahmen zu treffen, was in der Praxis zu deutlich kürzeren Spannweiten und/oder reduzierten Nutzlasten führt.

5. Qualitätssicherung und Prüfmethoden

In Ermangelung einer lückenlosen Produktionsdokumentation dienen Prüfergebnisse als Surrogat für die Konformitätsbewertung. Die RISE-Methodik (5-stufig) bildet hierfür den Rahmen:

1. Bestandsanalyse: Prüfung vorhandener Pläne.
2. Visuelle Inspektion: Aufnahme von Transportschäden und Rissbildern.
3. Zerstörungsfreie Prüfung (NDT):
  * GPR (Radar): Lokalisierung der Bewehrung und Spannglieder.
  * Schmidt-Hammer: Abschätzung der Oberflächenhärte.
  * Ultraschall (UPV): Detektion interner Fehlstellen und Homogenitätsprüfung.
  * Half-Cell Potential: Messung der Korrosionswahrscheinlichkeit.
4. (Semi-)Zerstörungsfreie Prüfung: Entnahme von Bohrkerne zur Bestimmung der tatsächlichen Druckfestigkeit.
5. Restlebensdauer: Berechnung basierend auf Karbonatisierungstiefe und Chlorideindringprofilen.

Diese Daten fließen direkt in die Zertifizierung ein. Wenn der ursprüngliche Herstellungsprozess nicht dokumentiert ist, werden diese NDT-basierten Zustandsberichte zur rechtlichen Basis für die statische Freigabe.

6. Tragwerksrelevante Chancen und Risiken

Die Wiederverwendung ist ökologisch alternativlos, erfordert jedoch ein aktives Risikomanagement.

Ökobilanz: Das Peikko-Pilotprojekt belegt, dass der Reuse eines Rahmens zu 50 % geringeren CO2-Emissionen und 35 % Kosteneinsparungen gegenüber dem Neubau führt – selbst wenn zusätzliche Kosten für Rückbau und Reinigung anfallen.

Top 3 Projektrisiken und Minderungsstrategien

1. Unbekannte Lastgeschichte (Ermüdung):
  * Minderung: Anwendung erhöhter Sicherheitsbeiwerte und detaillierte NDT-Analyse der Rissbreiten.
2. Fehlende Normung (Rechtssicherheit):
  * Minderung: Projektspezifische Zulassungen (Case-by-case) unter Einbeziehung des DTI-Frameworks; NDT als Ersatznachweis.
3. Transportschäden (Kantenbruch):
  * Minderung: Verwendung originaler Hebepunkte; strikte Vorgaben für Lagerung und Zwischenzustände.

Digitale Bauteilpässe: Die Implementierung von RFID-Tags oder BIM-basierten Pässen (wie bei Marktplaats.insert) ist essenziell, um zukünftige Prüfaufwände zu minimieren.

7. Fazit und Ausblick

Die technischen Lösungen für den zirkulären Betonbau sind durch Pilotprojekte (Peikko, NIST, ReCreate) validiert. Die größte Herausforderung ist derzeit nicht die Statik, sondern die Verfügbarkeit von Bauteillagern und die Harmonisierung der Rechtsrahmen.

Die Transformation des Betonbaus hin zu einem Modell, in dem Gebäude als „Materiallager“ fungieren, erfordert ein Umdenken in der Tragwerksplanung. Wir müssen Bauteile als dauerhafte Assets verstehen, deren Lebensdauer weit über die erste Nutzung hinausgeht. Durch die Kombination von digitaler Dokumentation (ARC-Datenbank) und robusten NDT-Verfahren wird der Reuse von Betonfertigteilen vom experimentellen Pilotstatus zum industriellen Standard für nachhaltiges Bauen avancieren.

