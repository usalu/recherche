---
entity: "quelle"
id: "Geb_ude_Multi_Brussels_Reuse_in_MULTI_md"
title: "Geb_ude_Multi_Brussels_Reuse_in_MULTI_md"
build_status: "promoted_phase42"
source_filename: "Multi_Brussels_Reuse_in_MULTI.md"
---

# Geb_ude_Multi_Brussels_Reuse_in_MULTI_md

**Projekt:** MULTI / ehemaliger Philips- bzw. Brouckère Tower, Brüssel  
**Bearbeitung:** Deutsch, kompakt, quellenbasiert  
**Grundregel:** Gezählt werden nur wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Bestandserhalt und lose Möbel werden nicht als Direct Reuse gewertet.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | MULTI Brussels / Reuse in Multi | Umbau mit Reuse-/Urban-Mining-Strategie | S1, S2, S5 | belegt | ehem. Brouckère/Philips Tower |
| Gebäude | ehemaliger Philips Tower / Brouckère Tower | Bestandsgebäude, 1969 | S1, S5 | belegt | Bestandserhalt nur als Kontext |
| Ort | Boulevard Anspach / De Brouckère, Brüssel | Standort | S3, S5 | belegt | genaue Adresse teils Boulevard Anspachlaan |
| Projekt | großmaßstäbliche Büro-/Mixed-use-Rekonversion | Reuse-Fall im Hochhausumbau | S1, S3 | belegt | 44.200–45.800 m² je nach Quelle |
| People | Whitewood, Immobel, CONIX RDBM, Cordeel, Rotor, RotorDC, Madaster/EPEA | Bauherr/Entwickler, Architektur, Ausführung, Reuse-Beratung, Materialpass | S1–S6 | belegt | Rollen je Quelle |
| Bauteil | Blaustein-Fassadenblöcke/-platten | in situ bzw. transformierte Wiederverwendung | S2, S6 | belegt | Naturstein aus ursprünglicher Fassade |
| Bauteil | Granitplatten, Natursteinplatten | Boden/Terrasse/Treppenpodest | S3, S5 | belegt | teils externe Herkunft |
| Bauteil | Aluminiumprofile | Balustraden und Lichtarmaturen | S3, S4 | belegt | ca. 1.300 m |
| Bauteil | Aufzugsmotoren | demontiert und eine Etage höher wieder eingebaut | S5 | belegt | technisches Bauteil |
| Material | Betonbestand | 89 % bestehender Beton erhalten | S4, S7 | belegt | nach Grundregel überwiegend Bestandserhalt, nicht Direct Reuse |
| Datenmodell | Madaster Material Passport / Building Circularity Passport | Materialdokumentation | S4 | belegt | Digitaler Materialpass |
| Bauteilbörse | RotorDC | urban mining / Vermittlung / Wiederverwendung | S5, S8 | belegt | direkte Beschaffung nicht für jedes Bauteil einzeln belegbar |
| Prozessphase | Demontage / Remanufacturing / Wiedereinbau | Naturstein und weitere Bauteile | S2, S6 | belegt | technische Details begrenzt |
| Hürde | Großmaßstäblicher, hochkodifizierter Hochbau | Reuse-Integration in formalisierte Prozesse | S5 | belegt | Qualitäts-/Prozesshürden |
| Kennwert | 44.200 / 45.000 / 45.800 m² | Fläche je Quelle | S1, S4, S5 | teilweise belegt | Quellenkonflikt |
| Kennwert | 2 % bzw. 3 % Urban Mining / externe Reuse-Materialien | Anteil externer Reuse-Komponenten | S4, S7 | teilweise belegt | Quellenkonflikt |
| Recht | BREEAM Excellent | Nachhaltigkeitszertifizierung | S1, S3 | belegt | kein Reuse-Normnachweis |
| Software | Madaster | Materialpass | S4 | belegt | digitale Dokumentation |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Materialpass | trennt Datenmodell/Software von konkreter Gebäudedokumentation | Madaster / Building Circularity Passport | Datenmodell, Software, Kennwert, Bauteil |
| Reuse-Beratung | spezifische Planungsrolle zwischen Entwurf, Beschaffung und Prüfung | Rotor als Design-Assistance | People, Prozessphase, Methode |
| In-situ-Transformation | Bauteil bleibt aus demselben Gebäude, erhält aber neue Funktion | Blaustein-Fassade zu Terrasse/Wandbekleidung | Bauteil, Reuse-Strategie, Prozessphase |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; in-situ transformiert; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; adaptive reuse
- **Hauptniveau:** Gebäudehülle; räumlicher Innenausbau; technische Gebäudeausrüstung; Material; nicht primär Tragwerk
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Der erhaltene Beton des Bestandsgebäudes zählt hier nicht als Direct Reuse, weil er überwiegend am Ort bleibt und dieselbe tragende Funktion behält. Gezählt werden transformierte und neu eingesetzte Reuse-Bauteile wie Blaustein, Granit, Aluminiumprofile und Aufzugstechnik.
- **Warum ist der Fall relevant?** Er zeigt, wie Reuse in einem großen kommerziellen Bürohochhaus mit Materialpass, Urban Mining und Reuse-Beratung versucht wurde, auch wenn der direkte Bauteilanteil relativ klein blieb.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Ermittlung nutzbarer Bauteile im Bestandsgebäude | Whitewood, Immobel, CONIX RDBM, Rotor | Reuse-Beratung, Materialanalyse | unbekannt | selektive Demontage geplant | unbekannt | unbekannt | unbekannt | Hochhaus mit formalen Prozessen | frühe Einbindung Reuse-Partner | S5 |
| Bauteilinventar | Materialpass für Gebäude | Madaster, EPEA, Projektteam | Digitaler Materialpass | Madaster, Building Circularity Passport | nicht zutreffend | nicht zutreffend | Datenprüfung unbekannt | digital | Langzeitdokumentation | Materialpass | S4 |
| Schadstoffprüfung | Altgebäude prüfen | Projektteam | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Quellen nennen Asbest als Renovierungshürde allgemein | unbekannt | S7 |
| Rückbau / Ausbau | Blaustein-Fassade demontieren | Cordeel, De Meuter, Rotor | selektiver Rückbau | unbekannt | schonende Demontage / Sägen | Palettierung, Lagerung | unbekannt | Lagerung bei RotorDC | Bruchrisiko | chirurgische Präzision, Sandbett, Paletten | S6 |
| Transport | Bauteile zu Werkstatt / Lager / Projekt | RotorDC, Carrière de Maffle, Projektteam | just-in-time / Materiallogistik | unbekannt | nicht zutreffend | unbekannt | unbekannt | enges innerstädtisches Baufeld | geringe Lagerfläche | just-in-time-Lieferungen | S3 |
| Aufbereitung | Blaustein remanufacturing | Carrière de Maffle | Sägen, Umformatieren | Steinwerkstatt | nicht zutreffend | Remanufacturing | unbekannt | Rücktransport | schwere 800-kg-Blöcke | Fachbetrieb | S2 |
| Planung | Design aus verfügbaren Reuse-Bauteilen | CONIX RDBM, Rotor | Design assistance | unbekannt | nicht zutreffend | nicht zutreffend | unbekannt | Materialverfügbarkeit | Reuse muss in High-End-Projekt passen | begrenzte Materialpalette | S5 |
| Genehmigung | Integration in BREEAM / Hochhausumbau | Projektteam | Zertifizierung | BREEAM | unbekannt | unbekannt | unbekannt | unbekannt | formale Anforderungen | BREEAM Excellent angestrebt/erreicht je Quelle | S1, S3 |
| Wiedereinbau | Naturstein, Aluminium, Aufzugsmotoren | Cordeel, Fachunternehmen | Wiedereinbau / Umnutzung | unbekannt | nicht zutreffend | je Bauteil | unbekannt | richtige Mengen je Geschoss | Puzzlearbeit | just-in-time und Etagenlogistik | S3 |
| Monitoring | Materialdaten dokumentieren | Madaster/EPEA | Materialpass | Madaster | nicht zutreffend | nicht zutreffend | unbekannt | digital | langfristige Aktualität | digitaler Gebäudepass | S4 |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| Fläche | 44.200 | m² | Projektangabe Cordeel | Gebäude | S3 | belegt |
| Fläche | 45.000 | m² | Projektangabe CONIX/Rotor | Gebäude | S1, S5 | belegt |
| Fläche | 45.800 | m² | Immobel/Madaster-Angabe | Gebäude | S4 | belegt |
| vorhandener Beton erhalten | 89 | % | Building Circularity Passport / Projektangabe | Bestand | S4, S7 | belegt, aber Bestandserhalt |
| Abfall vermieden durch Betonerhalt | 20.000 | t | Projektangabe | Bestandserhalt | S7 | belegt, nicht Direct-Reuse-Kernwert |
| Embodied Carbon durch Betonerhalt | 3.259 | t CO₂e | Projektangabe | Bestandserhalt | S7 | belegt, nicht Direct-Reuse-Kernwert |
| Blaustein demontiert | ca. 280 / 140 | m² / t | Rotor Salvage-Bericht | Naturstein-Fassade | S6 | teilweise belegt |
| Blausteinblöcke | 82 | Stück | Rotor | Naturstein | S2 | belegt |
| Aluminiumprofile | 1.300 | m | Projektangabe | Reuse-Bauteile | S3, S4 | belegt |
| Granitfliesen Terrasse | 400 | Stück | Cordeel | Reuse-Bodenbelag | S3 | belegt |
| externer Reuse-/Urban-Mining-Anteil | 2 bzw. 3 | % | Materialpass/Projektangaben | neue Materialien / Gesamtprojekt | S4, S7 | Quellenkonflikt |
| Kosten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** Urban Mining, in-situ Materialtransformation und externe Reuse-Materialien über Reuse-Netzwerke; Rotor/RotorDC als Reuse-Akteur.
- **Bauteilbörse / Quelle:** RotorDC / Reuse-Sektor; Madaster als Dokumentationsplattform, keine Bauteilbörse.
- **Kostenwirkung:** unbekannt.
- **Zeitwirkung:** Wiederverwendung erforderte sechsjährige Zusammenarbeit bzw. langen Prozess nach Rotor; konkrete Mehrzeit unbekannt.
- **Versicherung / Haftung:** unbekannt.
- **Gewährleistung:** unbekannt.
- **Arbeitsaufwand:** hoch bei Natursteinrückbau, Sortierung, Anpassung, Etagenlogistik; genaue Stunden unbekannt.
- **Lagerung:** Naturstein wurde gelagert / über RotorDC bzw. Werkstattprozesse geführt; Details unbekannt.
- **Marktbarrieren:** Formalisierte Hochbauprozesse, ausreichende Mengen, gleiche Qualität, Lieferzeiten, technische Freigaben.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Tragwerksplaner, konkrete Prüfberichte, Normen, Versicherungsmodell, Gewährleistung, Kosten, detaillierte Leistungsanforderungen.
- **Welche neuen Entitäten wären sinnvoll?** Materialpass; Reuse-Beratung; In-situ-Transformation.
- **Welche Daten fehlen?** geprüfte Mengen je Reuse-Bauteil, Einbauorte, Befestigungsdetails, Prüfmethoden, CO₂ nur für Direct-Reuse-Bauteile, Kosten und Bauzeitwirkung.
- **Welche Quellen müssten geprüft werden?** Buch „Working with MULTI“, Madaster-/EPEA-Pass, Rotor-Projektunterlagen, Ausschreibungs-/Bauakten, technische Prüfberichte.

## Quellen und Links

- **S1** CONIX RDBM, „Multi“ – https://www.conixrdbm.com/project/multi/
- **S2** Rotor, „Reuse of blue limestone in Multi“ – https://rotordb.org/en/news/reuse-blue-limestone-multi
- **S3** Cordeel, „Multi - Brouckère“ – https://cordeel.eu/en/projects/multi-brouckere
- **S4** Immobel, „The materials passport used for the first time in a major renovation project“ – https://www.immobelgroup.com/en/news/the-materials-passport-used-for-the-first-time-in-a-major-renovation-project
- **S5** Rotor, „Reuse in the Multi project“ / „Multi - De Brouckère Tower“ – https://rotordb.org/en/projects/multi-de-brouckere-tower
- **S6** Rotor, „Reclaiming blue limestone slabs“ – https://rotordb.org/en/news/reclaiming-blue-limestone-slabs
- **S7** Whitewood / Drees & Sommer Projektangaben zu Multi – https://www.whitewood.eu/multibrussels ; https://www.dreso.com/de/en/company-2/press/press-releases/details/ressourcen-neu-gedacht-urban-mining-transformiert-bruessels-skyline
- **S8** RotorDC / circlemade Profil – https://circlemade.brussels/en/members/rotordc/
