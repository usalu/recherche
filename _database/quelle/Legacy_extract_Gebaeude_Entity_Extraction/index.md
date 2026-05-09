---
entity: "quelle"
id: "Legacy_extract_Gebaeude_Entity_Extraction"
title: "Gebaeude Entity Extraction"
build_status: "promoted_phase42"
node_kind: "source"
legacy_type: "\"extraction_report\""
---

# Gebaeude Entity Extraction

## Legacy Content

# Gebaeude Entity Extraction

Diese Datei ist der Markdown-Export der lokalen Extraktion aus den Gebaeude-Quellordnern. Grundlage sind die strukturierten Entitaeten-Mapping-Tabellen, Frontmatter-Wikilinks und Verknuepfungsbloecke der Quelldateien.

## Laufzusammenfassung

| Kennzahl | Wert |
|---|---:|
| Roh-Paare | 1913 |
| Distinkte Roh-Typen | 234 |
| Werte aus `Gebäude` | 1757 |
| Werte aus `gebaeude` | 156 |
| Aktuelle `.md`-Dateien in `reuse_database` | 1724 |

## Dateien Ohne Erkanntes Mapping

- `gebaeude\Elementa.md`
- `gebaeude\gebäude2_wiederverwendung_direct_reuse_examples.md`
- `gebaeude\gebäude3_wiederverwendung_direct_reuse_examples.md`
- `gebaeude\gebäude_wiederverwendung_direct_reuse_examples.md`
- `gebaeude\index.md`

## Angefragte Entitaeten

| Anfrage | kanonischer Typ | Roh-Typen | Roh-Paare | eindeutige Werte | Markdown-Ziel | MD-Dateien |
|---|---|---|---:|---:|---|---:|
| abbruchmethode | `Abbruchmethode` | `Abbruchmethode` | 20 | 20 | `reuse_database/13_Abbruchmethode` | 6 |
| akteur / person | `Akteur` | `Akteur`, `Architekt`, `Bauherr`, `Bauherr / Akteur`, `Tragwerksplaner`, `Lehrstuhl`, `People/Akteure`, `akteure` | 297 | 269 | `reuse_database/05_Akteur` | 328 |
| aufbereitungsmethode | `Aufbereitungsmethode` | `Aufbereitungsmethode` | 25 | 25 | `reuse_database/14_Aufbereitungsmethode` | 15 |
| bauteil | `Bauteil` | `Bauteil` | 232 | 225 | `reuse_database/06_Bauteiltyp` | 34 |
| bauteilboerse | `Bauteilboerse` | `Bauteilboerse` | 11 | 10 | `reuse_database/29_Bauteilboerse` | 7 |
| bericht | `Bericht` | `Bericht`, `Bericht / Dokument` | 6 | 6 | `reuse_database/26_Dokument` | 5 |
| datenmodell | `Datenmodell` | `Datenmodell`, `Software/Datenmodell` | 10 | 10 | `reuse_database/25_Datenmodell` | 11 |
| dokument | `Dokument` | `Bericht`, `Bericht / Dokument` | 6 | 6 | `reuse_database/26_Dokument` | 5 |
| fallstudie | `Fallstudie` | `Fallstudie` | 84 | 82 | `reuse_database/01_Fallstudie` | 154 |
| foerderprogramm | `Foerderprogramm` | `Foerderprogramm` | 13 | 12 | `reuse_database/30_Foerderprogramm` | 9 |
| gebaeude / Gebaeude | `Gebaeude` | `Gebaeude` | 97 | 92 | `reuse_database/03_Gebaeude` | 85 |
| huerde | `Huerde` | `Huerde` | 55 | 55 | `reuse_database/20_Huerde` | 20 |
| kennwert | `Kennwert` | `Kennwert`, `Konzeptkennwert`, `Kennwertkonflikt`, `Quellenkonflikt Kennwert`, `Quellenkonflikt-Kennwert` | 162 | 161 | `reuse_database/23_Kennwertdefinition` | 15 |
| leistungsanforderung | `Leistungsanforderung` | `Leistungsanforderung` | 11 | 11 | `reuse_database/16_Leistungsanforderung` | 14 |
| logistik | `Logistik` | `Logistik` | 26 | 26 | `reuse_database/21_Logistik` | 12 |
| material | `Material` | `Material` | 102 | 86 | `reuse_database/08_Material` | 23 |
| meta | `Meta` | - | 0 | 0 | - |  |
| methode | `Methode` | `Methode` | 64 | 47 | `reuse_database/12_Methode` | 16 |
| norm / recht | `Norm_Recht` | `Norm_Recht` | 55 | 37 | `reuse_database/19_Norm_Recht` | 13 |
| ort | `Ort` | `Ort` | 90 | 86 | `reuse_database/04_Ort` | 67 |
| projekt | `Projekt` | `Projekt` | 90 | 88 | `reuse_database/02_Projekt` | 87 |
| prozessphase | `Prozessphase` | `Prozessphase` | 10 | 10 | `reuse_database/11_Prozessphase` | 12 |
| pruefung | `Pruefung` | `Pruefung` | 47 | 33 | `reuse_database/15_Pruefung` | 15 |
| reuse_strategie | `Reuse_Strategie` | `Reuse_Strategie` | 55 | 43 | `reuse_database/09_ReuseStrategie` | 10 |
| schadstoff | `Schadstoff` | `Schadstoff` | 14 | 6 | `reuse_database/31_Schadstoff` | 7 |
| software / tools / werkzeug | `Werkzeug` | `Werkzeug`, `Software/Tool` | 29 | 15 | `reuse_database/28_Tool_Software` | 12 |
| tragwerkssystem | `Tragwerkssystem` | `Tragwerkssystem` | 38 | 34 | `reuse_database/17_Tragwerkssystem` | 15 |
| verbindung | `Verbindung` | `Verbindung` | 21 | 20 | `reuse_database/18_Verbindung` | 12 |
| wirtschaft | `Wirtschaft` | `Wirtschaft` | 34 | 21 | `reuse_database/22_Wirtschaft` | 15 |

## abbruchmethode

Markdown-Ziel: `reuse_database/13_Abbruchmethode`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Bergung aus Brandruine | 1 | `Abbruchmethode` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| careful deconstruction / Demontage statt Schrott | 1 | `Abbruchmethode` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Deconstruction / Demolition donor site 1 Broadgate | 1 | `Abbruchmethode` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Deconstruction statt demolition | 1 | `Abbruchmethode` | `Gebäude/Boulder_Fire_Station_3.md` |
| Demontage / demolition of I-93 elevated highway components | 1 | `Abbruchmethode` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| keine Gebäudedemontage | 1 | `Abbruchmethode` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| leichte Geräte, Lösen von Knotenpunkten, Durchtrennen von Verbindungsstählen | 1 | `Abbruchmethode` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Rückbau/Demontage | 1 | `Abbruchmethode` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Rückbauprojekte / Bauteiljagd | 1 | `Abbruchmethode` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| sehr begrenzte Demolition / selective deconstruction | 1 | `Abbruchmethode` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| selektive Bauteilernte aus Region | 1 | `Abbruchmethode` | `Gebäude/Recyclinghaus_Hannover.md` |
| selektive Demontage / Heraussägen / Herausheben | 1 | `Abbruchmethode` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| selektive Demontage / schonender Rückbau | 1 | `Abbruchmethode` | `Gebäude/Mehrow_Pilot_House.md` |
| selektiver Rückbau / Demontage | 1 | `Abbruchmethode` | `Gebäude/Association_house_Plauen.md` |
| selektiver Rückbau / Demontage von Platten; Diamantsägen im Pressekontext | 1 | `Abbruchmethode` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| selektiver Rückbau/Demontage | 1 | `Abbruchmethode` | `Gebäude/Association_house_Groeditz.md` |
| sorgfältige Demontage der Reithalle | 1 | `Abbruchmethode` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| stufenweiser, separierender Rückbau | 1 | `Abbruchmethode` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| zerstörungsfreier Rückbau | 1 | `Abbruchmethode` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| zirkuläre Demontage / remolition | 1 | `Abbruchmethode` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |

## akteur / person

Markdown-Ziel: `reuse_database/05_Akteur`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 7 | `Akteur`, `Architekt`, `Bauherr`, `Tragwerksplaner` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md`, `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md`, `Gebäude/Maison_des_Canaux_Paris.md`, `Gebäude/Resource_Rows_Copenhagen.md` |
| Consolis Parma | 3 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md`, `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| LXSY_Architektur | 3 | `Akteur`, `akteure` | `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/Bestandshalle_CRCLR_House.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Ramboll Finland | 3 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md`, `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Umacon | 3 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md`, `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Arup | 2 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md`, `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Bellastock | 2 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md`, `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| BLAF Architecten | 2 | `Akteur` | `Gebäude/Maison_DnA_Asse.md`, `Gebäude/gjG_House_Gentbrugge.md` |
| cepezed | 2 | `Akteur` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md`, `Gebäude/The_Green_House_Utrecht.md` |
| Cleveland Steel and Tubes | 2 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Heyne Tillett Steel / HTS | 2 | `Tragwerksplaner` | `Gebäude/Holbein_Gardens_London.md`, `Gebäude/Timber_Square_London.md` |
| IMd Raadgevende Ingenieurs | 2 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md`, `Gebäude/Montessori_Maassluis.md` |
| Lendager | 2 | `Akteur` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md`, `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Lendager Group / Lendager Architects | 2 | `Akteur`, `Architekt` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Privat | 2 | `Akteur`, `Bauherr` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md`, `Gebäude/Maison_DnA_Asse.md` |
| Rotor | 2 | `Akteur`, `akteure` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md`, `gebaeude/Da_Vinci_Business_District.md` |
| Skanska Finland | 2 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| TRNSFRM_eG | 2 | `akteure` | `gebaeude/Bestandshalle_CRCLR_House.md`, `gebaeude/Kindl_Areal.md` |
| Zirkular GmbH | 2 | `Akteur` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md`, `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| 51N4E | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| A-Kruunu | 1 | `Bauherr` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| A. de Jong Groep | 1 | `Akteur` | `Gebäude/Montessori_Maassluis.md` |
| Abfallwirtschaftsbetriebe Münster, urselmann interior, Concular, Petra Jablonická, Sven Urselmann | 1 | `Akteur` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| ABT + Adviesbureau Lüning | 1 | `Akteur` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Administration des bâtiments publics | 1 | `Akteur` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| AgwA | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| AKT II | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Albert & Co | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Albert & Compagnie | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Alliander / Liander | 1 | `Akteur` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Angelika Mettke / Heyn et al. / Dechantsreiter et al. / Fischer et al. | 1 | `Akteur` | `Gebäude/Association_house_Plauen.md` |
| Anna Hopp, Carsten Wiewiorra / Wiewiorra Hopp Architekten | 1 | `Akteur` | `Gebäude/Plattenpalast_Berlin.md` |
| Art Valens | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Artelia Group | 1 | `Akteur` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| asp_Architekten | 1 | `Akteur` | `gebaeude/BOELL_LAB_Berlin.md` |
| Ballast Nedam | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| Barbara Oelbrandt | 1 | `Akteur` | `Gebäude/gjG_House_Gentbrugge.md` |
| Barr Gazetas | 1 | `Architekt` | `Gebäude/Holbein_Gardens_London.md` |
| baubüro in situ | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Bennetts Associates | 1 | `Architekt` | `Gebäude/Timber_Square_London.md` |
| Bewohnerinitiative, Zayaz, Superuse Studios, Bouwbedrijf Versteegden, Transfarmers, VanNimwegen | 1 | `Akteur` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Bikubenfonden; Pihlmann Architects; Hoffmann A/S; ABC Rådgivende Ingeniører; Sara Martinsen; DTU Kristoffer Negendahl/Negeldahl | 1 | `Akteur` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Bill Dunster / ZEDfactory; BioRegional; Peabody Trust; Arup; Ellis & Moore; Gardiner & Theobald | 1 | `Akteur` | `Gebäude/BedZED_London_Hackbridge.md` |
| BIM_Berlin | 1 | `Akteur` | `gebaeude/BOELL_LAB_Berlin.md` |
| BioPartner Center Leiden | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Bischof Föhn Architektur | 1 | `Architekt` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| BlueCity, Superuse Studios, COUP, Workspot, Floris Schiferli | 1 | `Akteur` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Bonnefrite | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| Bourne Special Projects / Bourne Group | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Bouwbedrijven Jongen | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Brent Cross South Limited Partnership | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Bruxelles-Propreté / Net Brussel | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Bureau Bouwtechniek, Greisch, Daidalos Peutz, Taktyk | 1 | `Akteur` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Bureau Greisch | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| bureau SLA | 1 | `Akteur` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Burobas | 1 | `Akteur` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Camping Design | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| Cantillon | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| CBRE | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| CC Autrement | 1 | `Akteur` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| City of Helsinki | 1 | `Bauherr` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| CITYFÖRSTER architecture + urbanism | 1 | `Architekt` | `Gebäude/Recyclinghaus_Hannover.md` |
| Civic Engineers | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Claus Asam / IEMB | 1 | `Akteur` | `Gebäude/Mehrow_Pilot_House.md` |
| Claus Asam, IEMB/TU Berlin; Architekturbüro Conclus / Hervé Biele bzw. Joel Biele | 1 | `Akteur` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Clayton & Little / Clayton Korte | 1 | `Akteur` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Cleveland Steel | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Commune de Dilbeek | 1 | `Bauherr` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Commune de Molenbeek-Saint-Jean | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Construire | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Contrax Furniture | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Daedalus Engineering | 1 | `Akteur` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Daidalos Peutz, Sixco | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Davis Partnership Architects | 1 | `Akteur` | `Gebäude/Boulder_Fire_Station_3.md` |
| De Groot & Visser | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| De Vries en Verburg | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Deerns | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Depuis 1920 | 1 | `Akteur` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Detlev Lange / Familie Lange | 1 | `Akteur` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Dexia / Lo-Reninge town council | 1 | `Bauherr / Akteur` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Die_Zusammenarbeiter | 1 | `akteure` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| DREWES + SPETH Beratende Ingenieure | 1 | `Tragwerksplaner` | `Gebäude/Recyclinghaus_Hannover.md` |
| dRMM Architects | 1 | `Akteur` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Duncan Baker-Brown / BBM Sustainable Design | 1 | `Architekt` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Duncan Baker-Brown, Cat Fletcher/Freegle, Mears Group, Greater Brighton Metropolitan College, Studierende | 1 | `Akteur` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Dusseldorp | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Dutch Design Foundation | 1 | `Akteur` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Dycore | 1 | `Akteur` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Détang | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| ECE Architecture | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| EK Energiekonzepte | 1 | `Akteur` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Emergis | 1 | `Bauherr` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Encore Heureux | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Encore Heureux Architectes | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| Entra AS | 1 | `Bauherr` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Entra, MAD, FutureBuilt, Asplan Viak, Insenti, Scenario Interiørarkitekter, IWG/Spaces | 1 | `Akteur` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Evangelisches Büro für die Weltausstellung Expo 2000 | 1 | `Akteur` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Evelia Macal | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Fabrix | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| FORE Partnership | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Four Bay Structures | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Frédéric Denise / Archipel Zéro | 1 | `Akteur` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| G-build | 1 | `Akteur` | `Gebäude/gjG_House_Gentbrugge.md` |
| Galldris / Galldris Group | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Gardiner & Theobald | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Gemeinde Kerkrade, IBA Parkstad | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Gillion Construct | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Gladsaxe Municipality / Gladsaxe Kommune | 1 | `Akteur` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| gmp · Architekten von Gerkan, Marg und Partner | 1 | `Akteur` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Graber Pulver Architekt:innen | 1 | `Akteur` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Grand Huit | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Grants of Shoreditch | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Grosvenor | 1 | `Bauherr` | `Gebäude/Holbein_Gardens_London.md` |
| GTD Consulting / GTD Engineering | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Ham & Sybesma | 1 | `Akteur` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Hastings Pier Charity | 1 | `Akteur` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Hawkins\Brown | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| HEEMwonen | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Heinrich_Boell_Stiftung | 1 | `Akteur` | `gebaeude/BOELL_LAB_Berlin.md` |
| Hervé Biele / Architekturbüro Conclus; Claus Asam / IEMB | 1 | `Akteur` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Hervé Biele / Conclus | 1 | `Akteur` | `Gebäude/Mehrow_Pilot_House.md` |
| Hiroshi Nakamura & NAP | 1 | `Akteur` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| IF_DO | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| IMd raadgevende ingenieurs | 1 | `Akteur` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Immobilien Basel-Stadt; Hochbauamt Basel-Stadt; baubüro in situ; S+B; Jauslin Stebler; Pro Engineering; Haustec; Rapp AG; Husner AG Holzbau; Zirkular | 1 | `Akteur` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Impact Hub Berlin, LXSY Architektur, TRNSFRM eG, Die Zusammenarbeiter, ZRS Ingenieure | 1 | `Akteur` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Ingenieurbureau Heierli AG | 1 | `Tragwerksplaner` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Jan Jongert, Jeroen Bergsma, Team Superuse/2012Architecten | 1 | `Akteur` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Jinhee Park | 1 | `Akteur` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| John Hong | 1 | `Akteur` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| John Hong, Jinhee Park, Paul Pedini | 1 | `Akteur` | `Gebäude/Big_Dig_Building_Boston.md` |
| Josef Kolb AG | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Julie Devènes, Jan Brütting, Célia Küpfer, Maléna Bastien-Masse, Corentin Fivet | 1 | `Akteur` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| JZH & Partners | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Kahle Acoustics, Denis Dujardin | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Kamikatsu Town / lokale Einwohner | 1 | `Akteur` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Kampstaal | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| Karbon’ architecture & urbanisme | 1 | `Akteur` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Kilden & Hindby / PFA Ejendomme | 1 | `Bauherr` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Kitajima Corporation | 1 | `Akteur` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| KL&A Engineers and Builders | 1 | `Akteur` | `Gebäude/Boulder_Fire_Station_3.md` |
| Kloster Volkenroda / Jesus-Bruderschaft | 1 | `Akteur` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Kraaijvanger Architects | 1 | `Akteur` | `Gebäude/Montessori_Maassluis.md` |
| Lagemaat Heerde | 1 | `Bauherr` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Landsec | 1 | `Bauherr` | `Gebäude/Timber_Square_London.md` |
| Landsec, Bennetts Associates, HTS, Mace, Hoare Lea, Alinea/T+T Alinea, Opera, Stora Enso, Hybrid Structures, Cleveland Steel & Tubes | 1 | `People/Akteure` | `Gebäude/Timber_Square_London.md` |
| LD2 architecture | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Le WIP | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Lendager / Lendager Group | 1 | `Architekt` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Les Canaux / Ville de Paris / beteiligte Sozialunternehmen | 1 | `Akteur` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Les Marneurs / Janne Saario | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Ligne B.E. | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| LIIKE Oy Arkkitehtistudio | 1 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| London Borough of Barnet | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Maconda | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| MAD arkitekter / Mad as | 1 | `Architekt` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| MAMOUT architectes | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| manoa Landschaftsarchitekten | 1 | `Akteur` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Marc Angst, This Alder, Oliver Zbinden u. a. | 1 | `Akteur` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Mark Young Construction | 1 | `Akteur` | `Gebäude/Boulder_Fire_Station_3.md` |
| Matriciel | 1 | `Akteur` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Maurer United | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| McLaren Construction | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Method | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Metso Oyj | 1 | `Bauherr` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| MOBAT Ingénierie | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| MOE | 1 | `Tragwerksplaner` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Mélanie Devret | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| New Horizon | 1 | `Akteur` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Nico Plukkel | 1 | `Tragwerksplaner` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Nils Nolting / CITYFÖRSTER | 1 | `Akteur` | `Gebäude/Recyclinghaus_Hannover.md` |
| NIRAS | 1 | `Akteur` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| noAarchitecten | 1 | `Akteur` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Normandie Aménagement | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Novaedia / Novædia | 1 | `Akteur` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| NREP / AG Gruppen | 1 | `Bauherr` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| NREP, AG Gruppen, Lendager, MOE, Artelia, BOGL | 1 | `Akteur` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Oberli Ingenieurbau AG | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Opera | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Ouest Architecture | 1 | `Akteur` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Overtreders W | 1 | `Akteur` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Paul Pedini | 1 | `Akteur` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Peabody Trust | 1 | `Bauherr` | `Gebäude/BedZED_London_Hackbridge.md` |
| Philippe Peiger | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Philippe Samyn and Partners; Studio Valle Progettazioni; Buro Happold; Belgian Buildings Agency / Regie der Gebouwen | 1 | `Akteur` | `Gebäude/Europa_Building_Brussels.md` |
| Pierre Stoffel / BESP Stoffel & Partners; Sofiane Boudahri | 1 | `Akteur` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Pieters Bouwtechniek | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| PLP Architecture | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Polony 2008; Mettke/Heyn/Dechantsreiter als Literaturquellen | 1 | `Akteur` | `Gebäude/Association_house_Groeditz.md` |
| Popma ter Steege Architecten / PTSA | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Pouget Consultants | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Pouvoir Organisateur Pluriel / POP | 1 | `Akteur` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| privat; Tjibbe Knol / Ingrid Blans in Architectuurgids genannt | 1 | `Bauherr` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Private owner | 1 | `Bauherr` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Provincie Gelderland | 1 | `Akteur` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| R Creators | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| Ramboll | 1 | `Akteur` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Rarig Construction | 1 | `Akteur` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| RAU Architects | 1 | `Architekt` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| ReCreate Finnish cluster | 1 | `Akteur` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Related Argent | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Rijksvastgoedbedrijf / Central Government Real Estate Agency | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| Rothuizen Architecten / Taco Tuinhof | 1 | `Akteur` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Rotor asbl | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Rotor asbl-vzw | 1 | `Akteur` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Rotor_DC | 1 | `akteure` | `gebaeude/Da_Vinci_Business_District.md` |
| Réhabail | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Satu Huuhka / Tampere University | 1 | `Akteur` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Saxum Vineyards | 1 | `Akteur` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Schmets architectes | 1 | `Akteur` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Scoping | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| SecuriSan | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Seidl + Seidl Architekten; Architekturbüro Hose; Dr. Angelika Mettke / BTU Cottbus | 1 | `Akteur` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Simon Boudvin | 1 | `Akteur` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Single Speed Design | 1 | `Akteur` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Single Speed Design / SsD | 1 | `Akteur` | `Gebäude/Big_Dig_Building_Boston.md` |
| SOCOTEC | 1 | `Akteur` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Solus | 1 | `Akteur` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| SSG Structural Engineers | 1 | `Akteur` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Stadt Zürich / Amt für Hochbauten / Immobilien Stadt Zürich | 1 | `Bauherr` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Stadt Zürich / Amt für Hochbauten; ERZ als Eigentümervertretung/Betreiber | 1 | `Bauherr` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Stadt Zürich, Amt für Hochbauten, Immobilien Stadt Zürich, Bischof Föhn Architektur, Zirkular GmbH, Meili Partner, Heierli, Haerter + Partner, Schmidiger + Rosasco, aik | 1 | `Akteur` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Stadt_Heilbronn | 1 | `Akteur` | `gebaeude/ReUseBox_Heilbronn.md` |
| Stiff + Trevillion | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Stiftung Abendrot / Vorsorgestiftung Abendrot | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Stiftung_Edith_Maryon | 1 | `akteure` | `gebaeude/Kindl_Areal.md` |
| STONE22 | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Strukton Worksphere | 1 | `Akteur` | `Gebäude/The_Green_House_Utrecht.md` |
| Studio PDP | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Stéphanie Paly | 1 | `Akteur` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Stéphanie Willocx architecte | 1 | `Akteur` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Superuse Studios / 2012Architecten | 1 | `Architekt` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Sweco / Sweco Architects | 1 | `Akteur` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Symmetrys | 1 | `Akteur` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Tampere University / Satu Huuhka | 1 | `Akteur` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Tecclem | 1 | `Akteur` | `Gebäude/gjG_House_Gentbrugge.md` |
| technische Dienste der Stadt Paris | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| Terraterre | 1 | `Akteur` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Travail & Vie | 1 | `Akteur` | `Gebäude/Ferme_du_Rail_Paris.md` |
| TRIBU | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| TRNSFRM eG; Die Zusammenarbeiter; LXSY; ZRS; Solares Bauen; eZeit; brandkontrolle; Akustik-Ingenieurbüro Moll | 1 | `Akteur` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Tscherning, Ason A/S, Aksel V. Jensen | 1 | `Akteur` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| TU Berlin / IEMB, Leitung Claus Asam | 1 | `Lehrstuhl` | `Gebäude/Plattenpalast_Berlin.md` |
| TU Berlin Fachgebiet Bauphysik und Baukonstruktionen | 1 | `Lehrstuhl` | `Gebäude/Plattenvereinigung_Berlin.md` |
| University of Brighton | 1 | `Bauherr` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| V+ / Projectiles | 1 | `Akteur` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Van Dijk Maasland B.V. | 1 | `Akteur` | `Gebäude/Montessori_Maassluis.md` |
| VIA Landscape | 1 | `Akteur` | `Gebäude/Montessori_Maassluis.md` |
| Vic Obdam Staalbouw | 1 | `Akteur` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Ville de Mouscron | 1 | `Bauherr` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Ville de Paris – Pavillon de l’Arsenal | 1 | `Akteur` | `Gebäude/Circular_Pavilion_Paris.md` |
| Vintis installatieadviseurs | 1 | `Akteur` | `Gebäude/Montessori_Maassluis.md` |
| Vlieghe | 1 | `Akteur` | `Gebäude/gjG_House_Gentbrugge.md` |
| Volantis | 1 | `Akteur` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Vollgut_eG | 1 | `akteure` | `gebaeude/Kindl_Areal.md` |
| WBM | 1 | `Akteur` | `gebaeude/BOELL_LAB_Berlin.md` |
| Webb Yates Engineers | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Weber + Brönnimann AG | 1 | `Akteur` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Weidlinger Associates | 1 | `Akteur` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Wetter AG | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Whitby Wood | 1 | `Akteur` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Whitewood, Immobel, CONIX RDBM, Cordeel, Rotor, RotorDC, Madaster/EPEA | 1 | `Akteur` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Willmott Dixon | 1 | `Akteur` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Witteveen+Bos | 1 | `Akteur` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Yamada Noriaki Structural Design Office | 1 | `Akteur` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| YIT | 1 | `Akteur` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| ZHAW IKE | 1 | `Akteur` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Zinneke asbl | 1 | `Akteur` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| ZRS_Architekten | 1 | `akteure` | `gebaeude/Bestandshalle_CRCLR_House.md` |

## aufbereitungsmethode

Markdown-Ziel: `reuse_database/14_Aufbereitungsmethode`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| abschleifen, restaurieren, lackieren, in Edelstahlrahmen setzen | 1 | `Aufbereitungsmethode` | `Gebäude/Europa_Building_Brussels.md` |
| cleaning, testing, certification, preparation | 1 | `Aufbereitungsmethode` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Demontage, Reinigung, ggf. Zuschnitt | 1 | `Aufbereitungsmethode` | `Gebäude/Mehrow_Pilot_House.md` |
| Demontage, Transport, Beschichtung/Coating, Wiedermontage | 1 | `Aufbereitungsmethode` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Demontage, Zwischenlagerung, Wiedereinbau | 1 | `Aufbereitungsmethode` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Entfernen von Anbauteilen, Löcher füllen, Testen, CE marking | 1 | `Aufbereitungsmethode` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Fensterglas ersetzt, Rahmen ertüchtigt | 1 | `Aufbereitungsmethode` | `Gebäude/Recyclinghaus_Hannover.md` |
| geringe Veränderung / Anpassung; Fassadenreserve angelegt | 1 | `Aufbereitungsmethode` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Höhenausgleich durch Ziegelschicht; sonst unbekannt | 1 | `Aufbereitungsmethode` | `Gebäude/Association_house_Groeditz.md` |
| Kürzen von Hohlkörperdecken; Fassadenelemente schneiden, Brüstungen abtrennen; Lagerung | 1 | `Aufbereitungsmethode` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| möglichst ohne Bearbeitung; Repair/Remanufacturing als Lehre | 1 | `Aufbereitungsmethode` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Prüfung, Verstärkung, Anpassung, Verdopplung einzelner Bögen | 1 | `Aufbereitungsmethode` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Reinigung / Auswahl von Gebrauchtziegeln | 1 | `Aufbereitungsmethode` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Reinigung und Zuschnitt nach Schneidplan | 1 | `Aufbereitungsmethode` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Reinigung, Zuschnitt, Öffnungen/Fittings, Wärmedämmung | 1 | `Aufbereitungsmethode` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Reparieren, Vermessen, Katalogisieren, Anpassen | 1 | `Aufbereitungsmethode` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Reuse largely as found / prefab kit | 1 | `Aufbereitungsmethode` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Sandstrahlen, Fertigung, Beschichtung mit zinkreicher Beschichtung | 1 | `Aufbereitungsmethode` | `Gebäude/BedZED_London_Hackbridge.md` |
| Spenden sammeln, kombinieren, zuschneiden/integrieren | 1 | `Aufbereitungsmethode` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| surface preparation, testing, weld inspection | 1 | `Aufbereitungsmethode` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| unbekannt | 1 | `Aufbereitungsmethode` | `Gebäude/Association_house_Plauen.md` |
| Vorbereitung des Rückbauholzes; Herstellung zu glulamST und CLST | 1 | `Aufbereitungsmethode` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Werksaufbereitung im Consolis-Parma-Werk Kangasala | 1 | `Aufbereitungsmethode` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Zuschneiden / Spalten längerer Stücke | 1 | `Aufbereitungsmethode` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Zuschnitt/Sägen von Platten | 1 | `Aufbereitungsmethode` | `Gebäude/Berlin_Schildow_Pilot_House.md` |

## bauteil

Markdown-Ziel: `reuse_database/06_Bauteiltyp`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Radiatoren | 3 | `Bauteil` | `Gebäude/Grande_Halle_de_Colombelles.md`, `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md`, `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| 200 zugeschnittene Teile aus 60 Decken- und 50 Innenwandplatten | 2 | `Bauteil` | `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Hohlkörperdecken | 2 | `Bauteil` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Sanitär | 2 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md`, `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| wiederverwendete Ziegel | 2 | `Bauteil` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md`, `Gebäude/Musee_de_Folklore_Mouscron.md` |
| wiederverwendeter Stahl | 2 | `Bauteil` | `Gebäude/BlueCity_Offices_Rotterdam.md`, `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| 11,8 t Stahlprofile | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 13 WBS70-Betonfertigteile, v. a. Wand- und Deckenelemente | 1 | `Bauteil` | `Gebäude/Plattenpalast_Berlin.md` |
| 135 m² Straßenpflasterplatten | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 145 Decken-/Bodenplatten, 19 Außenwandelemente, 14 Innenwände, 11 Kellerwände | 1 | `Bauteil` | `Gebäude/Association_house_Plauen.md` |
| 180 Holztüren | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| 1930s steel beams | 1 | `Bauteil` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 2 Stahl-Treppen | 1 | `Bauteil` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| 200 Fenster aus Lagerrestbeständen | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| 22 Wandplatten, 27 Deckenplatten | 1 | `Bauteil` | `Gebäude/Mehrow_Pilot_House.md` |
| 25 Betonblöcke aus Ortbeton-Kellerwänden | 1 | `Bauteil` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| 26 Wandplatten | 1 | `Bauteil` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| 27 Hohlkörperdecken / hollow-core slabs | 1 | `Bauteil` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| 279 Betonfertigteile + 159 WBS70-Paneele | 1 | `Bauteil` | `Gebäude/Association_house_Groeditz.md` |
| 3.750 restaurierte Holzfensterrahmen | 1 | `Bauteil` | `Gebäude/Europa_Building_Brussels.md` |
| 38 Fertigbetonelemente als Rinnen | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 419 m² Gips-Akustikpaneele + 12 Metallpaneele/4,3 m² | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 450 m² Steinwolle-Dämmplatten | 1 | `Bauteil` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| 5 Fensterrahmen | 1 | `Bauteil` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| 50 Deckenplatten | 1 | `Bauteil` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| 50 Holzstühle | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| 58 Stahlbeton-Wand- und Deckenelemente; nach PRECS: 28 Wände, 23 Decken, 7 Treppen | 1 | `Bauteil` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| 61 m² Blech | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 89 salvaged wide-flange steel members | 1 | `Bauteil` | `Gebäude/Boulder_Fire_Station_3.md` |
| Abbruchziegel | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| abgehängte Decke + Leuchten Karreveld | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Akustikelemente | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| alte Shoji-Schirme und Glastüren | 1 | `Bauteil` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Aluminium-Fassadensystem | 1 | `Bauteil` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Aluminium-Trapezblech | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Aluminiumfenster | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| Aluminiumprofile | 1 | `Bauteil` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Aluminiumrohre, Heizkörper, Plattenmaterial, Fensterrahmen, Haustüren, Geländer, Brüstungen, Küche | 1 | `Bauteil` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Armaturen / Beleuchtung / Installationen | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Aufzugsmotoren | 1 | `Bauteil` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Außenkozijnen / Fensterrahmen | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Außentreppe | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Außentüren und Holzfenster | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Azobé-hardwood shingles | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Bau-/Montagelift, später Innenlift | 1 | `Bauteil` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Bestandsfundamente / erste Geschosse | 1 | `Bauteil` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Bestandsgebäude, Innenausbau, ggf. Stahl/Holz/Fassadenmaterial | 1 | `Bauteil` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| bestehende Struktur Print Building | 1 | `Bauteil` | `Gebäude/Timber_Square_London.md` |
| bestehende Treppen, Toiletten, technische Schächte Karreveld | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Beton | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Beton-Inverset panels | 1 | `Bauteil` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Betonblöcke | 1 | `Bauteil` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Betonblöcke, Holz, Sperrholz | 1 | `Bauteil` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Betonfertigteil-Paneele | 1 | `Bauteil` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Betonpfähle / concrete beams | 1 | `Bauteil` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Betonplatten aus dem Kerenzerbergtunnel | 1 | `Bauteil` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Bitumen-/Betonblöcke | 1 | `Bauteil` | `Gebäude/Ferme_du_Rail_Paris.md` |
| blaue Stahlblechfassade | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Blaustein-Fassadenblöcke/-platten | 1 | `Bauteil` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Blausteinplatten | 1 | `Bauteil` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Boden- und Wandfliesen | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Brandschutztüren | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Brettschichtholzbögen / glulam arches | 1 | `Bauteil` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| BTC-Ziegel | 1 | `Bauteil` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| ca. 1.000 m² neue Fassade in Holzrahmenbauweise | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| ca. 30 Stahlträger | 1 | `Bauteil` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| ca. 700 gespendete Fenster | 1 | `Bauteil` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Dach- und Terrassenfliesen Verbiest | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Dachziegel | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Dachziegel / roof tiles / vingetegl | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| dekorative Fliesen Verbiest | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| discarded floorboards / Dinesen offcuts | 1 | `Bauteil` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Double-glazed windows | 1 | `Bauteil` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| drei Wohnungsteile / Betonunits | 1 | `Bauteil` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Drill-Stem-Pipe / Schedule-40-Rohre | 1 | `Bauteil` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Dämmplatten | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| ehemalige Ausstellungspaneele | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| EPS-Dämmung | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| externe Stahltreppe | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Faserzement-/Eternitplatten | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| Fassaden-/Ziegelmaterial | 1 | `Bauteil` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Fassadenbekleidung | 1 | `Bauteil` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Fassadenbekleidung / Holzfassade | 1 | `Bauteil` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Fassadenelemente | 1 | `Bauteil` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Fassadenziegel | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Fenster | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Fenster / Rahmen aus Palast der Republik | 1 | `Bauteil` | `Gebäude/Plattenpalast_Berlin.md` |
| Fenster, Türen | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Fertigbetonteile aus Olympischem Dorf München und PH12-Punkthochhaus Frankfurt/Oder | 1 | `Bauteil` | `Gebäude/Plattenvereinigung_Berlin.md` |
| Filzpaneele | 1 | `Bauteil` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Fliesen/Fayence | 1 | `Bauteil` | `Gebäude/Ferme_du_Rail_Paris.md` |
| gebrauchte Küche | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| gekrümmte Außenmauer / Schale | 1 | `Bauteil` | `Gebäude/gjG_House_Gentbrugge.md` |
| Geländer / Brüstungsgeländer | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Geländer, Fliesen, Steine Verbiest | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Gitterroste/Brüstungsgitter, ehemaliges Garagentor | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Glas-PV-Module | 1 | `Bauteil` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Glasdach | 1 | `Bauteil` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Glasfassade / Kreuzgang / Vitrinen | 1 | `Bauteil` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Glastrennwände und Türen | 1 | `Bauteil` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| glulamST-Tragwerksrahmen; CLST-Wand- und Bodenplatten | 1 | `Bauteil` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Granitbordsteine | 1 | `Bauteil` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Granitplatten, Natursteinplatten | 1 | `Bauteil` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| große Außentreppe | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| großer Stahlträger als Empfangstresen | 1 | `Bauteil` | `Gebäude/Timber_Square_London.md` |
| Heizkörper / Radiatoren | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| historische Bauernhaustür | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| Hohlkörperdecken / hollow-core slabs | 1 | `Bauteil` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Hohlkörperdecken / kanaalplaatvloeren | 1 | `Bauteil` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Holz aus Deckenkonstruktion/Supermarkt/Discounter | 1 | `Bauteil` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Holz aus ehemaliger Bibliothek / Tankstelle / Schule / Kunstakademie | 1 | `Bauteil` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Holz aus Kabeltrommeln | 1 | `Bauteil` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Holz aus Rückbauten / Dachstühlen | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Holz-Alu-Fenster / Außenfenster | 1 | `Bauteil` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Holz-Dachbinder / timber roof trusses / rafters | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Holz-Dachspanten / Brettschichtholz-Kniespanten | 1 | `Bauteil` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Holzdachelemente / Holzwerkstoffe / Türen / Dreischichtplatten | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Holzfenster doppeltverglast | 1 | `Bauteil` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Holzfenster einfachverglast | 1 | `Bauteil` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Holzfensterrahmen | 1 | `Bauteil` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Holzfußböden | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Holzgalerie | 1 | `Bauteil` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Holzlatten aus Tischlereiresten | 1 | `Bauteil` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Holzpfetten / Holzstücke | 1 | `Bauteil` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Holzstruktur | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| Holzständer / softwood walling studs | 1 | `Bauteil` | `Gebäude/BedZED_London_Hackbridge.md` |
| Holzträger | 1 | `Bauteil` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Holzträger / houten balken | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| HSB-binnenbladen | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Infrastrukturträger, Boxbeams, temporäre Straßen-/Rampenteile, Fassaden-/Strukturelemente | 1 | `Bauteil` | `Gebäude/Big_Dig_Building_Boston.md` |
| Innentüren / Hang- und Schließwerk | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Innenwände / Holzfußboden-Bauteile / Dämmmaterialien | 1 | `Bauteil` | `Gebäude/The_Green_House_Utrecht.md` |
| Innenwände / Trennwände | 1 | `Bauteil` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| innerer Holzrahmen | 1 | `Bauteil` | `Gebäude/Maison_DnA_Asse.md` |
| Kabeltrassen | 1 | `Bauteil` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Klinker / Backstein | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| kompletter Lüftungsverbund | 1 | `Bauteil` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Kunststofffenster | 1 | `Bauteil` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Lampen / Fahrradständer / Uhr / Observatoriumskuppel | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Large/Grote Boomse Steen Ziegel | 1 | `Bauteil` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Leuchten | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Leuchten von ROTOR | 1 | `Bauteil` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Marmor-Glas-Hülle | 1 | `Bauteil` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Materialbibliothek / Küchenoberflächen | 1 | `Bauteil` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Messebauplatten | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| Metallblech / Profilblech / Fassadenblech | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| mineralische Dämmung / Steinwolle | 1 | `Bauteil` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| modulare Innenwände Karreveld | 1 | `Bauteil` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Möbel / Sofas / Tische | 1 | `Bauteil` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Naturstein-/Granitplatten | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| neue Brettschichtholzbögen | 1 | `Bauteil` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| perforierte Wellstahlpaneele | 1 | `Bauteil` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Pflaster / Naturstein / Bodenmaterial | 1 | `Bauteil` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Pflasterklinker aus alter Kade in Tiel | 1 | `Bauteil` | `Gebäude/The_Green_House_Utrecht.md` |
| prefab gevelelementen / Fassadenelemente | 1 | `Bauteil` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Pretty Plastic shingles | 1 | `Bauteil` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Profilbauglas | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| Ramps, piers, roadway components | 1 | `Bauteil` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Rauchglas-Fassadenpaneele Knoopkazerne | 1 | `Bauteil` | `Gebäude/The_Green_House_Utrecht.md` |
| reclaimed timber flooring / Gellerup floors | 1 | `Bauteil` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Reclaimed tubular steel columns | 1 | `Bauteil` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| red MDF boards und Ziegel aus anderer Baustelle | 1 | `Bauteil` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Red-cedar-Fensterrahmen / geerntete Fensterrahmen | 1 | `Bauteil` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| reused hollow core slabs | 1 | `Bauteil` | `Gebäude/Montessori_Maassluis.md` |
| salvaged Aluminium-Fassadenplatten | 1 | `Bauteil` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Sanitär, ducts, pipes, office fronts, doors | 1 | `Bauteil` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Sanitär, Türen, Beläge, Fliesen, Holz, feste Ausstattung | 1 | `Bauteil` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Sanitärapparate | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Sanitärapparate / Lavabos / Toiletten | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Sanitärausstattung | 1 | `Bauteil` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Sanitärobjekte | 1 | `Bauteil` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Sanitärobjekte / Toiletten / Waschbecken | 1 | `Bauteil` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Sanitärobjekte, Vorhangfassadenelemente, Blech/Glas, Türen, Bodenplatten | 1 | `Bauteil` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Saunabänke / Holzleisten | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| schwarze MDF-Platten | 1 | `Bauteil` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Stahl | 1 | `Bauteil` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Stahl aus vorhandenem Blackfriars-Bestand | 1 | `Bauteil` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Stahl-U-Profile als Außenstürze | 1 | `Bauteil` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Stahlbauteile für Laubengänge, Treppentürme, Geländer, Gitterroste | 1 | `Bauteil` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Stahlfassadenelemente / façade panels | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Stahlfassadenpaneele | 1 | `Bauteil` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Stahlkonstruktion für Außenraumbeschattung | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Stahlpfetten/-träger aus dem Hallendach | 1 | `Bauteil` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Stahlstruktur der ehemaligen Recyclinghalle Hagenholz | 1 | `Bauteil` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Stahltragwerk / neun kreuzförmige Stützen | 1 | `Bauteil` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Stahlträger / Stahlrahmen / H-Profile | 1 | `Bauteil` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Stahlträger / Stützen | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Stahlträger / Stützen / Profilbleche Verbunddecken | 1 | `Bauteil` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Stahlträger aus Paternoster/Textilmaschine | 1 | `Bauteil` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Stahlträger und Stahlstützen | 1 | `Bauteil` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Steel columns lower floors 318 Oxford Street | 1 | `Bauteil` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Stein-/Mineralwolle | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| Steinwolledämmung aus Restposten / Abfallprodukten | 1 | `Bauteil` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Straßenklinker | 1 | `Bauteil` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Teppichfliesen | 1 | `Bauteil` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Terrakotta-Bodenfliesen | 1 | `Bauteil` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Terrassen-Caillebotis | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| Terrazzo-Arbeitsflächen / Oberflächen | 1 | `Bauteil` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Treppenelemente | 1 | `Bauteil` | `Gebäude/Plattenvereinigung_Berlin.md` |
| tropische Hartholz-Deckbohlen | 1 | `Bauteil` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| TT-Decken / Betondecken | 1 | `Bauteil` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Türen | 1 | `Bauteil` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Türen / Brandschutztüren | 1 | `Bauteil` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Türen, Bordsteine, Natursteinplatten, Gerüstrohre als Geländer/Balustraden | 1 | `Bauteil` | `Gebäude/BedZED_London_Hackbridge.md` |
| vier große Leuchten | 1 | `Bauteil` | `Gebäude/Circular_Pavilion_Paris.md` |
| Vinylbanner | 1 | `Bauteil` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Vordach / Pergola / Holzstützen | 1 | `Bauteil` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| vorkonsumiertes Holz / pre-used wood | 1 | `Bauteil` | `Gebäude/The_Green_House_Utrecht.md` |
| Wandfliesen aus Solvay-Gebäude | 1 | `Bauteil` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Wandverkleidung aus alten Holzstühlen | 1 | `Bauteil` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Waschbecken / Sanitär | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| WC-Trennwände | 1 | `Bauteil` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Wellblech | 1 | `Bauteil` | `Gebäude/Recyclinghaus_Hannover.md` |
| wetternde Stahl-Offcuts an Toren | 1 | `Bauteil` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| wiederverwendete Bodenpflaster / Bruseleye tiles | 1 | `Bauteil` | `Gebäude/Charles_Malis_Molenbeek.md` |
| wiederverwendete Fenster / upcycled windows | 1 | `Bauteil` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Wiederverwendete Stahlprofile | 1 | `Bauteil` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| wiederverwendete Stahlträger | 1 | `Bauteil` | `Gebäude/Timber_Square_London.md` |
| wiederverwendete Stahlträger/-stützen | 1 | `Bauteil` | `Gebäude/Holbein_Gardens_London.md` |
| wiederverwendete Troldtekt-Akustikplatten | 1 | `Bauteil` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| wiederverwendete Ziegelmauern | 1 | `Bauteil` | `Gebäude/Maison_DnA_Asse.md` |
| Wiederverwendeter Baustahl | 1 | `Bauteil` | `Gebäude/BedZED_London_Hackbridge.md` |
| Windturbinenflügel | 1 | `Bauteil` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Ziegel / bricks | 1 | `Bauteil` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Ziegelfassadenmodule / Mauerwerksausschnitte | 1 | `Bauteil` | `Gebäude/Resource_Rows_Copenhagen.md` |

## bauteilboerse

Markdown-Ziel: `reuse_database/29_Bauteilboerse`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 2 | `Bauteilboerse` | `Gebäude/Maison_des_Canaux_Paris.md`, `Gebäude/Montessori_Maassluis.md` |
| Bauteilladen Winterthur | 1 | `Bauteilboerse` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Cleveland Steel and Tubes / reclaimed stock | 1 | `Bauteilboerse` | `Gebäude/Holbein_Gardens_London.md` |
| Concular | 1 | `Bauteilboerse` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Franck Bricks; Rotor DC; 2emain.be | 1 | `Bauteilboerse` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Franck, RotorDC, Gebruiktebouwmaterialen, Namur Croisade pauvreté, Bouwstocks, kleine Anzeigen | 1 | `Bauteilboerse` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| keine | 1 | `Bauteilboerse` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| keine klassische Bauteilbörse | 1 | `Bauteilboerse` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Kuru Kuru Shop / Reuse Shop | 1 | `Bauteilboerse` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| RotorDC | 1 | `Bauteilboerse` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |

## bericht

Markdown-Ziel: `reuse_database/26_Dokument`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| ArchDaily / NAP / offizielle WHY-Seite | 1 | `Bericht` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| ASBP DISRUPT case study | 1 | `Bericht` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Buch „UN NOUVEAU MUSÉE“ | 1 | `Bericht / Dokument` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| dRMM Insight „Building with reclaimed timber“ | 1 | `Bericht` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| FCRBE 32 detailed project sheets | 1 | `Bericht` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Verbiest. Approximations | 1 | `Bericht` | `Gebäude/Verbiest_Karreveld_Brussels.md` |

## datenmodell

Markdown-Ziel: `reuse_database/25_Datenmodell`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| digitaler Bauteilkatalog | 1 | `Datenmodell` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Eigene Dokumentationsform für zukünftige Reuse-Fähigkeit. | 1 | `Datenmodell` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| INIES | 1 | `Software/Datenmodell` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Madaster Material Passport / Building Circularity Passport | 1 | `Datenmodell` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Material Passport / Turntoo/Madaster-Kontext möglich | 1 | `Datenmodell` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Material passports | 1 | `Datenmodell` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Produkt- und Materialpässe | 1 | `Datenmodell` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Präzisere Erfassung als allgemeines „Datenmodell“ | 1 | `Datenmodell` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Stock list / design list matching | 1 | `Datenmodell` | `Gebäude/Timber_Square_London.md` |
| trennt Datenmodell/Software von konkreter Gebäudedokumentation | 1 | `Datenmodell` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |

## dokument

Markdown-Ziel: `reuse_database/26_Dokument`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| ArchDaily / NAP / offizielle WHY-Seite | 1 | `Bericht` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| ASBP DISRUPT case study | 1 | `Bericht` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Buch „UN NOUVEAU MUSÉE“ | 1 | `Bericht / Dokument` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| dRMM Insight „Building with reclaimed timber“ | 1 | `Bericht` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| FCRBE 32 detailed project sheets | 1 | `Bericht` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Verbiest. Approximations | 1 | `Bericht` | `Gebäude/Verbiest_Karreveld_Brussels.md` |

## fallstudie

Markdown-Ziel: `reuse_database/01_Fallstudie`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| CRCLR_House | 2 | `Fallstudie` | `gebaeude/Bestandshalle_CRCLR_House.md`, `gebaeude/Kindl_Areal.md` |
| Elementa_Walkeweg | 2 | `Fallstudie` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| 55 Great Suffolk Street | 1 | `Fallstudie` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Association house, Gröditz / Gröditz association house | 1 | `Fallstudie` | `Gebäude/Association_house_Groeditz.md` |
| Association house, Plauen / Plauen association house | 1 | `Fallstudie` | `Gebäude/Association_house_Plauen.md` |
| AWM Münster, 3. OG Rösnerstraße | 1 | `Fallstudie` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| BedZED / Beddington Zero Energy Development | 1 | `Fallstudie` | `Gebäude/BedZED_London_Hackbridge.md` |
| Berlin-Schildow 2nd pilot house | 1 | `Fallstudie` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Berlin-Schildow Pilot House / Berlin-Schildow 2nd pilot house | 1 | `Fallstudie` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Bestandverplanzung Pavilion / Bestandverpflanzung? | 1 | `Fallstudie` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Big Dig Building | 1 | `Fallstudie` | `Gebäude/Big_Dig_Building_Boston.md` |
| Big Dig House | 1 | `Fallstudie` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| BioPartner 5 | 1 | `Fallstudie` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| BlueCity Offices / Blue City 010 Offices | 1 | `Fallstudie` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| BOELL_LAB_Berlin | 1 | `Fallstudie` | `gebaeude/BOELL_LAB_Berlin.md` |
| Boulder Fire Station 3 / City of Boulder Fire Rescue, Station #3 | 1 | `Fallstudie` | `Gebäude/Boulder_Fire_Station_3.md` |
| Brent Cross Town Primary Substation | 1 | `Fallstudie` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Brighton Waste House / Brighton Wild House | 1 | `Fallstudie` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Bröthen twin-house | 1 | `Fallstudie` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| CascadeUp / London secondary-timber glulam demonstrator | 1 | `Fallstudie` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Charles Malis / Antenne administrative | 1 | `Fallstudie` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Christus-Pavillon / Christ Pavilion | 1 | `Fallstudie` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Circular Centre Netherlands / Prinsenhof A reuse pilot | 1 | `Fallstudie` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Conversion of two wings of Lycée Michel Lucius | 1 | `Fallstudie` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| CRCLR House / Impact Hub Berlin | 1 | `Fallstudie` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| dnA House / Maison DnA | 1 | `Fallstudie` | `Gebäude/Maison_DnA_Asse.md` |
| ELYS Kultur- & Gewerbehaus | 1 | `Fallstudie` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Europa Building Brussels | 1 | `Fallstudie` | `Gebäude/Europa_Building_Brussels.md` |
| gjG House | 1 | `Fallstudie` | `Gebäude/gjG_House_Gentbrugge.md` |
| Grande Halle de Colombelles / Le WIP | 1 | `Fallstudie` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Grubenstrasse 29 / Werkhof 29 | 1 | `Fallstudie` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Hastings Pier Visitor Centre / Pavilion Cladding | 1 | `Fallstudie` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Haus HOS / Mühlhausen 2-story multi-housing building | 1 | `Fallstudie` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Holbein Gardens | 1 | `Fallstudie` | `Gebäude/Holbein_Gardens_London.md` |
| House of Fraser / 318 Oxford Street → TBC.London | 1 | `Fallstudie` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Härmälänranta / A-Kruunu ReCreate mini-pilot | 1 | `Fallstudie` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Impact Hub Berlin Interior / CRCLR fit-out | 1 | `Fallstudie` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Institut de Botanique de l’ULg | 1 | `Fallstudie` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| K.118 / Kopfbau Halle 118 | 1 | `Fallstudie` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| KA13 / Kristian Augusts gate 13 | 1 | `Fallstudie` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Kamikatsu Zero Waste Center / Hotel WHY | 1 | `Fallstudie` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Kinder- en jeugdkliniek Ithaka / Emergis | 1 | `Fallstudie` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| La Ferme du Rail | 1 | `Fallstudie` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Liander / Alliander HQ Duiven | 1 | `Fallstudie` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Lo-Reninge Town Hall façade / Stadhuis Lo | 1 | `Fallstudie` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Lokomotion Technology Centre mini-pilot | 1 | `Fallstudie` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Maison des Canaux | 1 | `Fallstudie` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Maison Vignette / Vignette House | 1 | `Fallstudie` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Mehrow 1st pilot house | 1 | `Fallstudie` | `Gebäude/Mehrow_Pilot_House.md` |
| Melkinlaituri elementary school and daycare centre | 1 | `Fallstudie` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Montessori Maassluis / Montessorischool Maassluis | 1 | `Fallstudie` | `Gebäude/Montessori_Maassluis.md` |
| MULTI Brussels / Reuse in Multi | 1 | `Fallstudie` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Musée de Folklore / MUSEF Mouscron | 1 | `Fallstudie` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Pavillon Circulaire / Circular Pavilion | 1 | `Fallstudie` | `Gebäude/Circular_Pavilion_Paris.md` |
| People’s Pavilion | 1 | `Fallstudie` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Plattenpalast Berlin | 1 | `Fallstudie` | `Gebäude/Plattenpalast_Berlin.md` |
| Plattenvereinigung Berlin | 1 | `Fallstudie` | `Gebäude/Plattenvereinigung_Berlin.md` |
| PLP Architecture HQ / Circular Studio Fit-out | 1 | `Fallstudie` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Re:Crete footbridge | 1 | `Fallstudie` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Recyclinghaus Hannover | 1 | `Fallstudie` | `Gebäude/Recyclinghaus_Hannover.md` |
| Recyclingzentrum Juch-Areal | 1 | `Fallstudie` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Recypark Anderlecht / Recypark Demets | 1 | `Fallstudie` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Resource Rows | 1 | `Fallstudie` | `Gebäude/Resource_Rows_Copenhagen.md` |
| ReUseBox_Heilbronn | 1 | `Fallstudie` | `gebaeude/ReUseBox_Heilbronn.md` |
| Roots in the Sky / Blackfriars Crown Court | 1 | `Fallstudie` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Résilience / La Ferme des Possibles | 1 | `Fallstudie` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Sanitary block for the Itterbeek Chiro / Pavillon de sanitaires | 1 | `Fallstudie` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Saxum Vineyard Equipment Barn | 1 | `Fallstudie` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| SUPERLOCAL Expogebouw | 1 | `Fallstudie` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Svanen / The Swan / Børnehuset Svanen | 1 | `Fallstudie` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| The Green House Utrecht | 1 | `Fallstudie` | `Gebäude/The_Green_House_Utrecht.md` |
| Thoravej 29 | 1 | `Fallstudie` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Timber Square | 1 | `Fallstudie` | `Gebäude/Timber_Square_London.md` |
| TRÆ High-Rise | 1 | `Fallstudie` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Umbau Kindergarten Mööslistrasse / Kindergarten Manegg | 1 | `Fallstudie` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Upcycle Studios | 1 | `Fallstudie` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Urban_Production_Brussels | 1 | `Fallstudie` | `gebaeude/Da_Vinci_Business_District.md` |
| Verbiest + Karreveld | 1 | `Fallstudie` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Villa Welpeloo | 1 | `Fallstudie` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Vollgut_Areal | 1 | `Fallstudie` | `gebaeude/Kindl_Areal.md` |
| Woongroep Boschgaard / Collectief Ecosysteem Boschgaard | 1 | `Fallstudie` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Zinneke / Feder Masui4ever | 1 | `Fallstudie` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |

## foerderprogramm

Markdown-Ziel: `reuse_database/30_Foerderprogramm`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 2 | `Foerderprogramm` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md`, `Gebäude/The_Green_House_Utrecht.md` |
| Be Exemplary | 1 | `Foerderprogramm` | `Gebäude/Maison_Vignette_Auderghem.md` |
| DBU-Förderung; bpb-Förderung für Programm am Tempelhofer Feld | 1 | `Foerderprogramm` | `Gebäude/Plattenvereinigung_Berlin.md` |
| DISRUPT | 1 | `Foerderprogramm` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| DISRUPT case study | 1 | `Foerderprogramm` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| ERDF / FEDER Brüssel-Hauptstadt | 1 | `Foerderprogramm` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| FEDER und Be.Exemplary | 1 | `Foerderprogramm` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Heritage Lottery Fund / National Lottery Heritage Fund | 1 | `Foerderprogramm` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Holcim Awards Encouragement Prize 2005–2006 North America | 1 | `Foerderprogramm` | `Gebäude/Big_Dig_Building_Boston.md` |
| New European Bauhaus Prize 2024 | 1 | `Foerderprogramm` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Provinz Zeeland / Rabobank Groenprojecten | 1 | `Foerderprogramm` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Urban Innovative Actions / IBA Parkstad | 1 | `Foerderprogramm` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |

## gebaeude / Gebaeude

Markdown-Ziel: `reuse_database/03_Gebaeude`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Einfamilienhaus / Pilotwohnhaus | 2 | `Gebaeude` | `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Mehrow_Pilot_House.md` |
| ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal | 2 | `Gebaeude` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| Lysbuechel_Parkhaus | 2 | `Gebaeude` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| LysP8_Basel_Lysbuechelareal | 2 | `Gebaeude` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| Sport-/Vereinshaus | 2 | `Gebaeude` | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md` |
| 1980er-Jahre Bürogebäude | 1 | `Gebaeude` | `Gebäude/Holbein_Gardens_London.md` |
| 318 Oxford Street / former House of Fraser / The Elephant | 1 | `Gebaeude` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 78 m / 20-geschossiges Holzhochhaus | 1 | `Gebaeude` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Agricultural storage / equipment barn | 1 | `Gebaeude` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| altes Verwaltungsgebäude der awm | 1 | `Gebaeude` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Altes_Hobelwerk_Winterthur | 1 | `Gebaeude` | `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| Areal_Walkeweg_Nord | 1 | `Gebaeude` | `gebaeude/Lysbuechel_Parkhaus.md` |
| Bestandsgebäude am Canal | 1 | `Gebaeude` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Bestandshalle_CRCLR_House | 1 | `Gebaeude` | `gebaeude/Kindl_Areal.md` |
| bestehende Industriehalle Halle 118 | 1 | `Gebaeude` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| bestehender Emergis-Bestand Kloetinge | 1 | `Gebaeude` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Big Dig Building | 1 | `Gebaeude` | `Gebäude/Big_Dig_Building_Boston.md` |
| BioPartner 5 | 1 | `Gebaeude` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Boulder Community Hospital / Boulder Community Health hospital | 1 | `Gebaeude` | `Gebäude/Boulder_Fire_Station_3.md` |
| Büro-/Campuskomplex | 1 | `Gebaeude` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Bürogebäude mit Umbau und Erweiterung | 1 | `Gebaeude` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Christus-Pavillon | 1 | `Gebaeude` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Circulair Centrum Nederland, Heerde | 1 | `Gebaeude` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| CRCLR House, ehemalige Kindl-Brauerei | 1 | `Gebaeude` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Doppelhaus / twin-house | 1 | `Gebaeude` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| ehemalige elektrische Werkstatt der Société Métallurgique de Normandie | 1 | `Gebaeude` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| ehemalige Gladsaxe School | 1 | `Gebaeude` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| ehemalige Lager-/Fassladehalle auf dem Kindl-Areal | 1 | `Gebaeude` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| ehemalige Reithalle / riding arena / horse riding school | 1 | `Gebaeude` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| ehemalige Werkstätten / ehemaliger Gebäudekomplex des Finanzministeriums | 1 | `Gebaeude` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| ehemalige Zigarettenfabrik | 1 | `Gebaeude` | `Gebäude/Charles_Malis_Molenbeek.md` |
| ehemaliger Philips Tower / Brouckère Tower | 1 | `Gebaeude` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| ehemaliges Coop-Verteilzentrum / Großbäckerei | 1 | `Gebaeude` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| ehemaliges Districtskantoor Rijkswaterstaat Terneuzen | 1 | `Gebaeude` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| ehemaliges Fabrik-/Gewerbe-/Schlossereigebäude | 1 | `Gebaeude` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| ehemaliges Gorlaeus-Hochhaus / Gorlaeus laboratory | 1 | `Gebaeude` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| ehemaliges Nachbarschaftszentrum De Patio + neue Wohnbauten | 1 | `Gebaeude` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| ehemaliges subtropisches Schwimmbad Tropicana / Club Tropicana | 1 | `Gebaeude` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Einfamilienhaus | 1 | `Gebaeude` | `Gebäude/gjG_House_Gentbrugge.md` |
| Einfamilienhaus / modernes Wohnhaus | 1 | `Gebaeude` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Einfamilienhaus / Wohnhaus | 1 | `Gebaeude` | `Gebäude/Recyclinghaus_Hannover.md` |
| Einfamilienhaus / Zwei-Generationenhaus mit Satteldach | 1 | `Gebaeude` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Einfamilienhaus in Auderghem | 1 | `Gebaeude` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Einfamilienhaus mit Home Office | 1 | `Gebaeude` | `Gebäude/Maison_DnA_Asse.md` |
| Europa Building mit Residence Palace Block A | 1 | `Gebaeude` | `Gebäude/Europa_Building_Brussels.md` |
| Expogebouw / Superlocal Pavilion | 1 | `Gebaeude` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Fire Station 3 & Fire Administration | 1 | `Gebaeude` | `Gebäude/Boulder_Fire_Station_3.md` |
| Former Blackfriars Crown Court, 1 Pocock Street / Loman Street, Southwark | 1 | `Gebaeude` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Grade II Listed Victorian warehouse | 1 | `Gebaeude` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Grundschule und Kita | 1 | `Gebaeude` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Hastings Pier / Visitor Centre | 1 | `Gebaeude` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Hobelwerk_Haus_D_Oberwinterthur | 1 | `Gebaeude` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| Hochhausflat Ursulastraat | 1 | `Gebaeude` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Härmälänrannan Ernst | 1 | `Gebaeude` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Industrie-/Fabrikgebäude von 1967/1968 | 1 | `Gebaeude` | `Gebäude/Thoravej_29_Copenhagen.md` |
| Institut de Botanique de l’ULg | 1 | `Gebaeude` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| K118_Kopfbau_Halle_118_Winterthur | 1 | `Gebaeude` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md` |
| Kamikatsu Zero Waste Center „WHY“ | 1 | `Gebaeude` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Karreveld | 1 | `Gebaeude` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Kindl_Areal | 1 | `Gebaeude` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| kleiner Technikbau + Personalräume „space within a space“ | 1 | `Gebaeude` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Kleinsthaus / Galerie / experimenteller Wohnraum | 1 | `Gebaeude` | `Gebäude/Plattenpalast_Berlin.md` |
| Lycée Michel Lucius Campus, Flügel 3000 und 6000 | 1 | `Gebaeude` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Mehrfamilienhaus | 1 | `Gebaeude` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Montessorischool Maassluis | 1 | `Gebaeude` | `Gebäude/Montessori_Maassluis.md` |
| Musée de Folklore Vie Frontalière | 1 | `Gebaeude` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Neubau, bioklimatisches Betriebs-/Bürogebäude | 1 | `Gebaeude` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Neubauensemble | 1 | `Gebaeude` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Olympisches Dorf / Bungalows | 1 | `Gebaeude` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| permanentes Forschungs-/Demonstrationsgebäude | 1 | `Gebaeude` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Prinsenhof A, Arnhem | 1 | `Gebaeude` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Print Building und Ink Building | 1 | `Gebaeude` | `Gebäude/Timber_Square_London.md` |
| Rathaus Lo-Reninge / ehemaliges Kloster | 1 | `Gebaeude` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Reihenhausensemble | 1 | `Gebaeude` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Sanitärpavillon neben alter Farm | 1 | `Gebaeude` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Spender: abgerissener Marzahner Elfgeschosser | 1 | `Gebaeude` | `Gebäude/Mehrow_Pilot_House.md` |
| Spender: Berliner Elfgeschosser / Marzahn-Plattenbau | 1 | `Gebaeude` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Spender: Berliner/Marzahner Plattenbau | 1 | `Gebaeude` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Spender: Massenwohnungsbau / Plattenbau | 1 | `Gebaeude` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Spender: Rückbaustelle Leinefelde | 1 | `Gebaeude` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Spender: Schule Typ Dresden; weiteres WBS70-Gebäude | 1 | `Gebaeude` | `Gebäude/Association_house_Groeditz.md` |
| Substation screen / oval steel structure | 1 | `Gebaeude` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Suutarila community centre | 1 | `Gebaeude` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| TBC.London / Tower Bridge Court | 1 | `Gebaeude` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| The Green House | 1 | `Gebaeude` | `Gebäude/The_Green_House_Utrecht.md` |
| The White Chapel Building | 1 | `Gebaeude` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Verbiest | 1 | `Gebaeude` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| vollständig de- und remontierbares Recycling-Gebäude | 1 | `Gebaeude` | `Gebäude/Plattenvereinigung_Berlin.md` |
| Werkhof Mööslistrasse | 1 | `Gebaeude` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Wohn- und Arbeitsquartier | 1 | `Gebaeude` | `Gebäude/BedZED_London_Hackbridge.md` |
| Wohngebäude / Wohnquartier | 1 | `Gebaeude` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Wohnhaus mit Ausstellungs-/Kunstlagerfunktion | 1 | `Gebaeude` | `Gebäude/Villa_Welpeloo_Enschede.md` |

## huerde

Markdown-Ziel: `reuse_database/20_Huerde`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Abgrenzung Bestandserhalt | 1 | `Huerde` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Abgrenzung Möbel vs. Bauteil | 1 | `Huerde` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Abgrenzung Sanierung vs. Wiederverwendung | 1 | `Huerde` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Bauphysik, Schall, Ausführung | 1 | `Huerde` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Bauteilverfügbarkeit / Entwurf nach Bestand | 1 | `Huerde` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Bauvorschriften / Dauerhaftigkeit | 1 | `Huerde` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| begrenzte Längen und Mengen | 1 | `Huerde` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Beschaffung heterogener Kleinmengen | 1 | `Huerde` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Bestandserhalt vs. Direct Reuse | 1 | `Huerde` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Budgetverschiebung nach Sturmschäden | 1 | `Huerde` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Bäume / Lage / Lärm | 1 | `Huerde` | `Gebäude/gjG_House_Gentbrugge.md` |
| Eignung der Abmessungen | 1 | `Huerde` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Einpassung in historischen Kontext | 1 | `Huerde` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| enger Zeitplan | 1 | `Huerde` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| fehlende Gewährleistung/Skalierung/Supply Chain für Sekundärholz | 1 | `Huerde` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| fehlende Industriestandards für Prüfung reclaimed steel | 1 | `Huerde` | `Gebäude/Boulder_Fire_Station_3.md` |
| fire, acoustics, insurance, vibration | 1 | `Huerde` | `Gebäude/Timber_Square_London.md` |
| geringe Grundstücksgröße / keine Lagerfläche | 1 | `Huerde` | `Gebäude/Ferme_du_Rail_Paris.md` |
| geringe Quellenlage | 1 | `Huerde` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Gewährleistung / fehlendes Werkszeugnis | 1 | `Huerde` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Gewährleistung, Prüfung, Logistik, Toleranzen | 1 | `Huerde` | `Gebäude/Association_house_Plauen.md` |
| Großmaßstäblicher, hochkodifizierter Hochbau | 1 | `Huerde` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Heterogenität gespendeter Bauteile | 1 | `Huerde` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| heutige Bauprozesse, Kosten-/Verfahrenslogik | 1 | `Huerde` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| hohe Front-End-Kosten und Logistikunsicherheit | 1 | `Huerde` | `Gebäude/Boulder_Fire_Station_3.md` |
| Holzschädlinge / boktor | 1 | `Huerde` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Instandhaltung der Fenstervitrinen | 1 | `Huerde` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Integration in komplexen Bauablauf | 1 | `Huerde` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Kosten, Programm, verfügbare Bestände | 1 | `Huerde` | `Gebäude/Holbein_Gardens_London.md` |
| laufender Schulbetrieb / Phasierung | 1 | `Huerde` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| logistisch-organisatorische Hindernisse | 1 | `Huerde` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Marktilliquidität / Timing / Zertifizierung | 1 | `Huerde` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Materialverfügbarkeit vor Bauplanung | 1 | `Huerde` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Maßausgleich, unterschiedliche Fertigteilsysteme, Anschlüsse | 1 | `Huerde` | `Gebäude/Association_house_Groeditz.md` |
| nachhaltiger Rückbau als neuer Ausschreibungsprozess | 1 | `Huerde` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Nachweis wiederverwendeter Stahl | 1 | `Huerde` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Normen/Altgebäude/Materialprüfung | 1 | `Huerde` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Passung geernteter Fensterrahmen | 1 | `Huerde` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Planung mit vorhandenen Elementen | 1 | `Huerde` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| pre-1940s steel testing, concrete encasement, rivets | 1 | `Huerde` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Profilverfügbarkeit, Services, Profilhöhen, Zertifizierung | 1 | `Huerde` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Projektabbruch / nicht gebaut | 1 | `Huerde` | `Gebäude/Big_Dig_Building_Boston.md` |
| Regelwerk, Dokumentation, Marktverfügbarkeit, Rückbaukosten | 1 | `Huerde` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Reinigung ölhaltiger Außenfarbe auf Olympiaplatten | 1 | `Huerde` | `Gebäude/Plattenvereinigung_Berlin.md` |
| Remanufacturing auf Neubaustandard | 1 | `Huerde` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Reservation mismatch / design changes | 1 | `Huerde` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Reuse-Ziegel und Energieanforderungen | 1 | `Huerde` | `Gebäude/Maison_DnA_Asse.md` |
| Risiko / aléas / Kontrollbüro | 1 | `Huerde` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Stabilitäts-/Testaufwand bei hohem Reuse-Anteil | 1 | `Huerde` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| variable Rohrdurchmesser / Entwurfsgrenzen | 1 | `Huerde` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Verfügbarkeit passender Profile; lange Vorlaufzeiten; gebogene Profile nicht reused | 1 | `Huerde` | `Gebäude/BedZED_London_Hackbridge.md` |
| Versicherung / assurabilité | 1 | `Huerde` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Zulassung / Brandschutz / Anforderungen | 1 | `Huerde` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| öffentliche Ausschreibung und Bauordnung nicht angepasst | 1 | `Huerde` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| öffentliche Beschaffung vs. Wiederverwendungsflexibilität | 1 | `Huerde` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |

## kennwert

Markdown-Ziel: `reuse_database/23_Kennwertdefinition`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 2 | `Kennwert` | `Gebäude/Institut_de_Botanique_ULg_Liege.md`, `Gebäude/Maison_des_Canaux_Paris.md` |
| $645,000 excl. land / $175/sf / $150/sf | 1 | `Kennwert` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| 1,9 Mio. CHF Objektkredit | 1 | `Kennwert` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| 1.270 m² | 1 | `Kennwert` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| 1.300 m² | 1 | `Kennwert` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| 1.436 m² | 1 | `Kennwert` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| 1.534 m² | 1 | `Kennwert` | `Gebäude/Montessori_Maassluis.md` |
| 10 educational groups + BSO | 1 | `Kennwert` | `Gebäude/Montessori_Maassluis.md` |
| 100 % borrowed | 1 | `Kennwert` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| 100 Arbeitsplätze | 1 | `Kennwert` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| 118 m³; 49 Bauteile; 2005; Bauteilalter ca. 21 Jahre | 1 | `Kennwert` | `Gebäude/Mehrow_Pilot_House.md` |
| 12 % neue Materialien second-hand nach Masse | 1 | `Kennwert` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| 12,67 % Reuse-Anteil | 1 | `Kennwert` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| 120 Stahlträger bis 18 m | 1 | `Kennwert` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| 13,32 t CO₂e / 82 % | 1 | `Kennwert` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| 130.096 kg CO₂e footprint / 170.534 kg waste saved | 1 | `Kennwert` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| 139 t salvaged steel | 1 | `Kennwert` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| 14 % Wiederverwendungsrate nach Gewicht | 1 | `Kennwert` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| 15 Jahre temporäre Nutzung | 1 | `Kennwert` | `Gebäude/The_Green_House_Utrecht.md` |
| 16 t / 20 t / 40 t / up to 100 t | 1 | `Kennwert` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 160 m² Wohnfläche | 1 | `Kennwert` | `Gebäude/Recyclinghaus_Hannover.md` |
| 161 tons salvaged structural steel from hospital | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 165.000 kg wiederverwendeter Stahl | 1 | `Kennwert` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| 17.000 t Material, 12.000 t Beton, 3.500 t CO₂, 92 % Reuse | 1 | `Kennwert` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| 175.78 t CO₂ diverted from landfill | 1 | `Kennwert` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| 189 Fertigteile; ca. 7 km Distanz; 2007; gebaut | 1 | `Kennwert` | `Gebäude/Association_house_Plauen.md` |
| 19 t Abfall vermieden und wiederverwendet | 1 | `Kennwert` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| 190 m² | 1 | `Kennwert` | `Gebäude/gjG_House_Gentbrugge.md` |
| 2 % bzw. 3 % Urban Mining / externe Reuse-Materialien | 1 | `Kennwert` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| 2,6 → 1,9 kg CO₂e/m²a | 1 | `Kennwert` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| 2.300 m² / 1.000 m² gebaut | 1 | `Kennwert` | `Gebäude/Ferme_du_Rail_Paris.md` |
| 2.335 m² site area; 2.936 m² constructed area | 1 | `Kennwert` | `Gebäude/Big_Dig_Building_Boston.md` |
| 2.600 m² | 1 | `Kennwert` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| 2.700 m² | 1 | `Kennwert` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 20 % project steel repurposed | 1 | `Kennwert` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 20 wiederverwendete Bögen | 1 | `Kennwert` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| 20.35 t reused steel | 1 | `Kennwert` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| 200 Teile; 245 m³; ca. 18 Jahre Bauteilalter; 2005 | 1 | `Kennwert` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| 2008; ca. 36 Jahre Bauteilalter | 1 | `Kennwert` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| 205 m² wiederverwendete Ziegel | 1 | `Kennwert` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| 21 other projects reused members from stockpile | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 245 m³; 200 Teile; 33 km; 2005; Bauteilalter ca. 18 Jahre | 1 | `Kennwert` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| 248 kg CO₂-eq/m² embodied carbon | 1 | `Kennwert` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| 24–25 t reused steel; 35/45/60 t CO₂-Einsparung je Quelle | 1 | `Kennwert` | `Gebäude/Holbein_Gardens_London.md` |
| 25 % Anteil Reuse-Ziegel | 1 | `Kennwert` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| 25 tons reused structural steel | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 250 m² | 1 | `Kennwert` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| 250 m² / 200 m² | 1 | `Kennwert` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| 260 m² | 1 | `Kennwert` | `Gebäude/Maison_DnA_Asse.md` |
| 28.300 / 28.370 sq ft | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 285 m² BGF | 1 | `Kennwert` | `Gebäude/Recyclinghaus_Hannover.md` |
| 3.000 Ziegel / 36 m² Fassade | 1 | `Kennwert` | `Gebäude/Maison_Vignette_Auderghem.md` |
| 3.404 t wiederverwendete/recycelte Materialien, 15 % | 1 | `Kennwert` | `Gebäude/BedZED_London_Hackbridge.md` |
| 3.750 Fenster; 374 LED light tubes; 636 solar panels | 1 | `Kennwert` | `Gebäude/Europa_Building_Brussels.md` |
| 30 t Stahl / 74 t CO₂e Einsparung | 1 | `Kennwert` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| 30.000 Ziegel / 8 Quellen | 1 | `Kennwert` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| 300 tons / 600,000+ lb | 1 | `Kennwert` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| 30–50% embodied-carbon reduction | 1 | `Kennwert` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| 32 % CO₂-Reduktion bei Materialien | 1 | `Kennwert` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| 33.46 t reused steel | 1 | `Kennwert` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| 386 kgCO₂e/m² A1-A5 | 1 | `Kennwert` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| 4,000 / 4,027 / 4,300 sq ft | 1 | `Kennwert` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| 4.572,702786 kg CO₂ vermieden | 1 | `Kennwert` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| 41 % Wiederverwendungsrate nach Volumen | 1 | `Kennwert` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| 42 % Altmaterial im Recyclingbeton | 1 | `Kennwert` | `Gebäude/Recyclinghaus_Hannover.md` |
| 42.5 % / around 45 % reused steel | 1 | `Kennwert` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| 438 dokumentierte Betonfertigteile; 2,5 km; 2007 | 1 | `Kennwert` | `Gebäude/Association_house_Groeditz.md` |
| 44.200 / 45.000 / 45.800 m² | 1 | `Kennwert` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| 45 % CO₂-Einsparung über 50 Jahre inkl. Betrieb | 1 | `Kennwert` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| 45 Sortierkategorien / teils 44 in offizieller Beschreibung | 1 | `Kennwert` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| 458–792 t CO₂e Einsparung | 1 | `Kennwert` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 48 t CO₂ | 1 | `Kennwert` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 5.000 m² built surface | 1 | `Kennwert` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| 5.557 m² | 1 | `Kennwert` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| 550 Boden- und 350 Fassadenelemente | 1 | `Kennwert` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| 59 % CO₂-Reduktion / 494 t CO₂ | 1 | `Kennwert` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| 6,9 t wiedergewonnene Materialien | 1 | `Kennwert` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| 6.200 m² / 7.000 m² | 1 | `Kennwert` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| 6.278 t Materialeinsparung / 178 t CO₂ | 1 | `Kennwert` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| 6.500.000 EUR ohne MwSt | 1 | `Kennwert` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 60 % Materialien mit erster Lebensdauer | 1 | `Kennwert` | `Gebäude/Circular_Pavilion_Paris.md` |
| 60 t CO₂ Einsparung | 1 | `Kennwert` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| 60.8 million pounds diverted from landfill | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 66 t / 99.2 t CO₂e saving | 1 | `Kennwert` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| 68 % CO₂-Reduktion | 1 | `Kennwert` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| 69,22 t CO₂e vermieden | 1 | `Kennwert` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| 7.000 t CO₂e durch Erhalt der Tragstruktur | 1 | `Kennwert` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| 7.400 m² / über 8.000 m² | 1 | `Kennwert` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| 70 % CO₂-Einsparung gegenüber aktuellem Baustandard | 1 | `Kennwert` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| 70 % Treibhausgasreduktion | 1 | `Kennwert` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| 70 m² | 1 | `Kennwert` | `Gebäude/Circular_Pavilion_Paris.md` |
| 700 Fenster | 1 | `Kennwert` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| 700.000 € vermiedene zukünftige Umweltschäden | 1 | `Kennwert` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| 72,24 t Reuse-Material | 1 | `Kennwert` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| 75 % diversion requirement | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 75.4 % embodied carbon reduction | 1 | `Kennwert` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| 76 Platten; 2001; ca. 32 Jahre Bauteilalter | 1 | `Kennwert` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| 79 % weniger Abbruchabfall | 1 | `Kennwert` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| 8 Büro-/Gewerbeeinheiten, 70–110 m² je Einheit | 1 | `Kennwert` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| 8,11 Mio. € excl. VAT; 728.000 € für die Halle | 1 | `Kennwert` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| 80 % sustainable/recycled/upcycled | 1 | `Kennwert` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| 80 m² Vertical Farming Greenhouse | 1 | `Kennwert` | `Gebäude/The_Green_House_Utrecht.md` |
| 81.777 m² Bruttogeschossfläche | 1 | `Kennwert` | `Gebäude/Europa_Building_Brussels.md` |
| 830 m² SDP + 1.466 m² nicht spezifiziert | 1 | `Kennwert` | `Gebäude/Ferme_du_Rail_Paris.md` |
| 84 % sekundäre Materialien | 1 | `Kennwert` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| 85 % bzw. Ziel 90 % wiederverwendete/geerntete Materialien | 1 | `Kennwert` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| 89 members | 1 | `Kennwert` | `Gebäude/Boulder_Fire_Station_3.md` |
| 90 % Abfallreduktion | 1 | `Kennwert` | `Gebäude/Thoravej_29_Copenhagen.md` |
| 90 % biosourced und/oder reused, Trockenbauweise | 1 | `Kennwert` | `Gebäude/Ferme_du_Rail_Paris.md` |
| 90 % circular / 90 % reused | 1 | `Kennwert` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| 90 % CO₂-Reduktion für Konstruktion und Fassade | 1 | `Kennwert` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| 90 % Fassadenmaterial wiederverwendet | 1 | `Kennwert` | `Gebäude/Recyclinghaus_Hannover.md` |
| 91 t CO₂ durch Wiederverwendung vermieden | 1 | `Kennwert` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| 914.000 kg waste saved | 1 | `Kennwert` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| 92 % reused/donated, 7 % recycled | 1 | `Kennwert` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| 94 % Gebäudemasse erhalten | 1 | `Kennwert` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| 95 % Materialwiederverwendung | 1 | `Kennwert` | `Gebäude/Thoravej_29_Copenhagen.md` |
| 95 % wiederverwendete Materialien; Maurer United nennt 100 % Material aus Abriss | 1 | `Kennwert` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| 95,6 % c2c-inspiriert oder ReUse | 1 | `Kennwert` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| 98 t wiederverwendeter Stahl | 1 | `Kennwert` | `Gebäude/BedZED_London_Hackbridge.md` |
| >500 beams; ca. 115–125 t reused steel | 1 | `Kennwert` | `Gebäude/Timber_Square_London.md` |
| >85 % Abfallmaterial | 1 | `Kennwert` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| BGF 2.004 m²; BRI 18.548 m³ | 1 | `Kennwert` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| BGF 6.600 m² / 7.603 m² / Größe 4.871 m² | 1 | `Kennwert` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| bis 88 % CO₂-Reduktion gegenüber Neubau | 1 | `Kennwert` | `Gebäude/Thoravej_29_Copenhagen.md` |
| BREEAM / Energiekennwerte publiziert, Direct-Reuse-Mengen unbekannt | 1 | `Kennwert` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| ca. 1,000 m² | 1 | `Kennwert` | `Gebäude/Charles_Malis_Molenbeek.md` |
| ca. 1.508 m² | 1 | `Kennwert` | `Gebäude/Montessori_Maassluis.md` |
| ca. 100 t CO₂ gebunden | 1 | `Kennwert` | `Gebäude/Recyclinghaus_Hannover.md` |
| ca. 160 m² HCS, 21 Elemente | 1 | `Kennwert` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| ca. 190 t wiederverwendete Elemente | 1 | `Kennwert` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| ca. 250 m² Nutzfläche; ca. 300.000 EUR Herstellungskosten; 2008 Fertigstellung | 1 | `Kennwert` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| ca. 30 % graue THG-Einsparung | 1 | `Kennwert` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| ca. 350 m² / fast 400 m² | 1 | `Kennwert` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| ca. 40 % Reduktion embodied carbon | 1 | `Kennwert` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| ca. 50 t CO₂ | 1 | `Kennwert` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| ca. 500 t Primärmaterial eingespart | 1 | `Kennwert` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| ca. 60 % salvaged materials | 1 | `Kennwert` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| ca. 70 % recycled or sustainable | 1 | `Kennwert` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| ca. 70 % reused/recycled/upcycled im Innenausbau | 1 | `Kennwert` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| ca. 75 % Wiederverwendungsgrad Rohbau-Substanz; ca. 25 % Kosteneinsparung | 1 | `Kennwert` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| ca. 87.000–88.700 kWh/a PV-Ertrag | 1 | `Kennwert` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| CO₂-/Materialeinsparungen publiziert, aber hier nicht gesichert | 1 | `Kennwert` | `Gebäude/Resource_Rows_Copenhagen.md` |
| CO₂-Einsparung reused steel 216 oder 276 tCO₂e | 1 | `Kennwert` | `Gebäude/Timber_Square_London.md` |
| Entwurfswerte sind nicht gebaute Betriebs-/Realisierungswerte | 1 | `Konzeptkennwert` | `Gebäude/Big_Dig_Building_Boston.md` |
| EPC A | 1 | `Kennwert` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| fast 600 t CO₂ / gut 40% Reduktion | 1 | `Kennwert` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Fläche ca. 3.700 m² / 3.080 m² / 3.000 m² | 1 | `Kennwert` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Fläche/Kosten unterscheiden sich nach Quelle | 1 | `Quellenkonflikt-Kennwert` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Gesamtfläche 4.297 m² | 1 | `Kennwert` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Karreveld 6.000.000 EUR exkl. MwSt. | 1 | `Kennwert` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Mehrere öffentliche Mengenangaben widersprechen sich | 1 | `Quellenkonflikt-Kennwert` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| mindestens 50 Jahre Nutzungsdauer | 1 | `Kennwert` | `Gebäude/Montessori_Maassluis.md` |
| nahezu/bis 80 % Wiederverwendung | 1 | `Kennwert` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Quellen nennen unterschiedliche CO₂-/Mengenwerte | 1 | `Kennwertkonflikt` | `Gebäude/Holbein_Gardens_London.md` |
| Reuse-Anteile werden unterschiedlich angegeben | 1 | `Quellenkonflikt Kennwert` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Verbiest 610 m² | 1 | `Kennwert` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| weniger als ein Drittel neue Materialien nach Masse | 1 | `Kennwert` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Wiederaufbau August 2001 | 1 | `Kennwert` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| zentrale Mengen variieren zwischen 904 t, 1000 t und 1400 tons | 1 | `Quellenkonflikt Kennwert` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| −71 % Global Warming Potential gegenüber Recyclingbeton-Alternative; −74 % gegenüber Stahl-Alternative; +9 % gegenüber Holz-Alternative | 1 | `Kennwert` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |

## leistungsanforderung

Markdown-Ziel: `reuse_database/16_Leistungsanforderung`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Bibliothek/Leseraum, Rauch-/Wärmespeicher, Akustik/Thermik | 1 | `Leistungsanforderung` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Energieperformance / Luftdichtheit Innenbox | 1 | `Leistungsanforderung` | `Gebäude/Maison_DnA_Asse.md` |
| Fassade als äußere Hülle; akustische und thermische Pufferwirkung laut Sekundärquelle | 1 | `Leistungsanforderung` | `Gebäude/Europa_Building_Brussels.md` |
| Fassaden-/Witterungsschicht | 1 | `Leistungsanforderung` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Kirche / öffentlicher Versammlungsraum | 1 | `Leistungsanforderung` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Marine Außenklima, Dauerhaftigkeit, Brandschutz | 1 | `Leistungsanforderung` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| roof could withstand 18-wheeler / 250 psf | 1 | `Leistungsanforderung` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Schule, Wohnhaus, Atelier | 1 | `Leistungsanforderung` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Strukturautonomie, Akustik, Dachauflager | 1 | `Leistungsanforderung` | `Gebäude/gjG_House_Gentbrugge.md` |
| Tragfähigkeit PV-Dach, Wind/Lateral System | 1 | `Leistungsanforderung` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Tragfähigkeit, Zertifizierung, Brandschutz, Erschließung | 1 | `Leistungsanforderung` | `Gebäude/55_Great_Suffolk_Street_London.md` |

## logistik

Markdown-Ziel: `reuse_database/21_Logistik`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| 52-m-Kran, Trailer, lokale Umsetzung | 1 | `Logistik` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| 8 oder 17 km Distanz laut PRECS | 1 | `Logistik` | `Gebäude/Mehrow_Pilot_House.md` |
| Bauteiljäger*innen, Katalog, städtische Occasionslager | 1 | `Logistik` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Beschaffung in 35-mile-Radius; lokale Materialstrategie | 1 | `Logistik` | `Gebäude/BedZED_London_Hackbridge.md` |
| ca. 2,5 km Transportdistanz | 1 | `Logistik` | `Gebäude/Association_house_Groeditz.md` |
| ca. 33 km Distanz; Transport per Tieflader/Kran im Pressekontext | 1 | `Logistik` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| ca. 6 km Donor–Receiver | 1 | `Logistik` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| ca. 6 km Spender–Empfänger | 1 | `Logistik` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| ca. 7 km Donor–Receiver | 1 | `Logistik` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| ca. 7 km Transportdistanz | 1 | `Logistik` | `Gebäude/Association_house_Plauen.md` |
| Cross-project steel transfer | 1 | `Logistik` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| early engagement with Cleveland Steel | 1 | `Logistik` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Koordination Donor Site–Fabrication–Installation | 1 | `Logistik` | `Gebäude/Holbein_Gardens_London.md` |
| Lagerung in Nivelles | 1 | `Logistik` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| lokale Holzrettung und Holzverwertung | 1 | `Logistik` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| lokale/regionale Bauteilbeschaffung und Lieferanten | 1 | `Logistik` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Materiallager / loods | 1 | `Logistik` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| on-site storage / temporäres Materialdepot | 1 | `Logistik` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| reused steel sourced from Cleveland Steel & Tubes laut Timber Development UK | 1 | `Logistik` | `Gebäude/Timber_Square_London.md` |
| Rückbau, Zuschnitt, Transport, Montage von Modulen | 1 | `Logistik` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Tieflader, Kran, just-in-time-Anlieferung; 33 km laut PRECS | 1 | `Logistik` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Tieflader; 30 km von Leinefelde nach Mühlhausen | 1 | `Logistik` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Transport von Big Dig Bauteilen nach Lexington | 1 | `Logistik` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Urban Mining aus Knoopkazerne und alter Kade | 1 | `Logistik` | `Gebäude/The_Green_House_Utrecht.md` |
| Urban Mining aus öffentlichen Gebäuden | 1 | `Logistik` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Vorausbeschaffung, Lagerung bei Cleveland | 1 | `Logistik` | `Gebäude/55_Great_Suffolk_Street_London.md` |

## material

Markdown-Ziel: `reuse_database/08_Material`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| ReUse_Fenster | 3 | `Material` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md`, `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Stahl | 3 | `Material` | `Gebäude/Boulder_Fire_Station_3.md`, `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md`, `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Ziegel / Backstein | 3 | `Material` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md`, `Gebäude/Maison_DnA_Asse.md`, `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Baustahl | 2 | `Material` | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/Holbein_Gardens_London.md` |
| Beton | 2 | `Material` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| Holz | 2 | `Material` | `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/Bestandshalle_CRCLR_House.md` |
| PV | 2 | `Material` | `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| ReUse_Bauteile | 2 | `Material` | `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/Da_Vinci_Business_District.md` |
| ReUse_Innenausbau | 2 | `Material` | `gebaeude/Altes_Hobelwerk_Winterthur.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| ReUse_Stahl | 2 | `Material` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Stahl und Beton | 2 | `Material` | `Gebäude/Big_Dig_Building_Boston.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Stahlbetonfertigteile | 2 | `Material` | `Gebäude/Association_house_Groeditz.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| WBS70-Stahlbetonfertigteile | 2 | `Material` | `Gebäude/Berlin_Schildow_Pilot_House_2.md`, `Gebäude/Mehrow_Pilot_House.md` |
| alte Fliesen | 1 | `Material` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Altholz | 1 | `Material` | `gebaeude/ReUseBox_Heilbronn.md` |
| Beton / Spannbeton vermutlich | 1 | `Material` | `Gebäude/Montessori_Maassluis.md` |
| Beton / Stahlbetonfertigteile | 1 | `Material` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Beton, Aluminium, Holz/Fensterrahmen, Metall, Plattenmaterial | 1 | `Material` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Betonbestand | 1 | `Material` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| CLT und Stahl | 1 | `Material` | `Gebäude/Timber_Square_London.md` |
| Dachbegruenung | 1 | `Material` | `gebaeude/BOELL_LAB_Berlin.md` |
| Denim jeans | 1 | `Material` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Dämmung, Betonblöcke, Holzrahmen | 1 | `Material` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Eiche oder ähnliche Holzarten; Glas/Stahl/Edelstahlrahmen | 1 | `Material` | `Gebäude/Europa_Building_Brussels.md` |
| europäisches Konstruktionsholz | 1 | `Material` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Fahrradschläuche, Polystyrol, Kaffeesatz | 1 | `Material` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Fertigbeton | 1 | `Material` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Glas- und Keramikscherben | 1 | `Material` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Hanf | 1 | `Material` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| Hanfkalksteine, Lehm, Akustikbaffeln, Teppich | 1 | `Material` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Holz / Brettschichtholz | 1 | `Material` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Holz, Fliesen/Keramik, Metall, Sanitärkeramik, Textil/Beläge | 1 | `Material` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Holz, massive Holzbalken/Platten Verbiest | 1 | `Material` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Holz, Stroh, Erde, BTC, Granit, Gussradiatoren | 1 | `Material` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Holz, Stroh, Hanf-Kalk, Naturputz | 1 | `Material` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Holz, Stroh, Lehm | 1 | `Material` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Holz, tropisches Hartholz / Pier decking | 1 | `Material` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Holz, vermutlich reclaimed timber | 1 | `Material` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Holzbau | 1 | `Material` | `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| Jutedämmung aus Kakaosäcken | 1 | `Material` | `Gebäude/Recyclinghaus_Hannover.md` |
| Laminatfurnierplatten | 1 | `Material` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| Lehm | 1 | `Material` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Lehmestrich_Oxacrete | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| Mauerwerkspuin / Abbruchschutt | 1 | `Material` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Mineralwolle_Sekundaermaterial | 1 | `Material` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md` |
| PET-Filz, Textilien, Papiergranulat, Hanf/Seegras | 1 | `Material` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| recycled/upcycled concrete from Copenhagen Metro | 1 | `Material` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Recyclingbeton | 1 | `Material` | `Gebäude/Recyclinghaus_Hannover.md` |
| ReUse_Betonfertigteile | 1 | `Material` | `gebaeude/Areal_Walkeweg_Nord.md` |
| ReUse_Blech | 1 | `Material` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| ReUse_Brettschichtholz | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_Dachziegel | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_Fassade | 1 | `Material` | `gebaeude/ReUseBox_Heilbronn.md` |
| ReUse_Fensterlaeden | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_Holz | 1 | `Material` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md` |
| ReUse_Kuechen | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_Mauerwerk | 1 | `Material` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| ReUse_MDF | 1 | `Material` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| ReUse_Sanitaerkeramik | 1 | `Material` | `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_Tueren | 1 | `Material` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Rezyklate | 1 | `Material` | `gebaeude/BOELL_LAB_Berlin.md` |
| rezyklierter Beton-Zuschlag | 1 | `Material` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| sekundäres Abbruchholz / reclaimed solid timber | 1 | `Material` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Sekundärmaterialien / oogstmaterialen | 1 | `Material` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Spannbeton | 1 | `Material` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Spannbeton / Fertigbeton | 1 | `Material` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Spannbeton/Fertigbeton | 1 | `Material` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Stahl, Beton, Holz, Glas, Ausbau-/TGA-Materialien | 1 | `Material` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Stahl, Holz, Polystyrol, Werbetafeln, weitere lokale Reststoffe | 1 | `Material` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Stahl, Holz, Stein, Glas, Recyclingmaterialien | 1 | `Material` | `Gebäude/BedZED_London_Hackbridge.md` |
| Stahl, Sichtbeton, Glas, Marmor | 1 | `Material` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Stahlbeton / Ortbeton | 1 | `Material` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Stahlbetonfertigteile / P2-PC-System | 1 | `Material` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Stahlbetonfertigteile / precast concrete | 1 | `Material` | `Gebäude/Association_house_Plauen.md` |
| Stahlbetonfertigteile / WBS70 | 1 | `Material` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Stahlbetonfertigteile / WBS70-Plattenbauteile | 1 | `Material` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Stahlrohr, reclaimt | 1 | `Material` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Stahlrohre | 1 | `Material` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Stroh | 1 | `Material` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Strohplatten | 1 | `Material` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| Videokassetten, DVDs, Floppy Discs | 1 | `Material` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| wiederverwendete ost- und westdeutsche Plattenbauteile / Fertigbetonteile | 1 | `Material` | `Gebäude/Plattenvereinigung_Berlin.md` |
| wiederverwendete Ziegel | 1 | `Material` | `Gebäude/gjG_House_Gentbrugge.md` |
| Wände des alten Rathauses | 1 | `Material` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Zahnbürsten | 1 | `Material` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Ziegel / Mauerwerk; Holz sekundär möglich | 1 | `Material` | `Gebäude/Resource_Rows_Copenhagen.md` |

## meta

Keine direkten Rohwerte in den Gebaeude-Dateien gefunden.

## methode

Markdown-Ziel: `reuse_database/12_Methode`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Design_for_Disassembly | 7 | `Methode` | `gebaeude/Altes_Hobelwerk_Winterthur.md`, `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/Bestandshalle_CRCLR_House.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Bauteiljagd | 4 | `Methode` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md`, `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| ReUse_LCA | 3 | `Methode` | `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md`, `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| Bauteilernte | 2 | `Methode` | `Gebäude/Recyclinghaus_Hannover.md`, `gebaeude/Da_Vinci_Business_District.md` |
| Bauteilkatalog | 2 | `Methode` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| Bauteilkatalogisierung | 2 | `Methode` | `gebaeude/Areal_Walkeweg_Nord.md` |
| Low_Tech | 2 | `Methode` | `gebaeude/BOELL_LAB_Berlin.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Materialpass | 2 | `Methode` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| Rueckbauplanung | 2 | `Methode` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| Archivrecherche, Berechnung, destruktive Untersuchung | 1 | `Methode` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Bauteiljagd / component hunting | 1 | `Methode` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Bauteillager | 1 | `Methode` | `gebaeude/ReUseBox_Heilbronn.md` |
| Bauteilpass | 1 | `Methode` | `gebaeude/ReUseBox_Heilbronn.md` |
| Betonsägen, Heben, Transport, Reassemblage | 1 | `Methode` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Brick Wall City / Big Brick | 1 | `Methode` | `Gebäude/gjG_House_Gentbrugge.md` |
| CCTP à variantes / „à trous“ | 1 | `Methode` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Circular Design / Materialwiederverwendung / adaptive reuse | 1 | `Methode` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Circular economy / urban mining | 1 | `Methode` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Co-design / Co-execution mit technischer Crew | 1 | `Methode` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Demolition audit / pre-demolition audit | 1 | `Methode` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Design for Disassembly | 1 | `Methode` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Erbbaurecht | 1 | `Methode` | `gebaeude/Kindl_Areal.md` |
| frühe Reuse-Beschaffungsentscheidung | 1 | `Methode` | `Gebäude/Holbein_Gardens_London.md` |
| Gebaeuderessourcenpass | 1 | `Methode` | `gebaeude/BOELL_LAB_Berlin.md` |
| Gebaeudesimulation | 1 | `Methode` | `gebaeude/BOELL_LAB_Berlin.md` |
| Gemeinwohlorientierte_Projektentwicklung | 1 | `Methode` | `gebaeude/Kindl_Areal.md` |
| Harvest Map / Materialscouting | 1 | `Methode` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| harvesting / Oogstkaart-Logik | 1 | `Methode` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Katalogisieren, Prüfen, Lagermanagement | 1 | `Methode` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Kit-of-parts, demontierbare modulare Struktur | 1 | `Methode` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| LEAN-Planung | 1 | `Methode` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Material mapping vor Abbruch | 1 | `Methode` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Materialenpaspoort | 1 | `Methode` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Materialjagd, Materialpässe, reversible Fügung, sichtbare TGA | 1 | `Methode` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Materiallager | 1 | `Methode` | `gebaeude/Da_Vinci_Business_District.md` |
| Materialsammlung vor/parallel zur Planung | 1 | `Methode` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Minimalinvasiver_Umbau | 1 | `Methode` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| Pioniernutzung | 1 | `Methode` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| Prototype / prefabricated system from salvaged components | 1 | `Methode` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Pruefung_gebrauchter_Bauteile | 1 | `Methode` | `gebaeude/Lysbuechel_Parkhaus.md` |
| recyclinggerechte Bauweise | 1 | `Methode` | `Gebäude/Recyclinghaus_Hannover.md` |
| Relocate and reuse/recycle infrastructural materials as building components | 1 | `Methode` | `Gebäude/Big_Dig_Building_Boston.md` |
| ReUse first / Design follows availability | 1 | `Methode` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| ReUse_Logistik | 1 | `Methode` | `gebaeude/Da_Vinci_Business_District.md` |
| Urban Mining / elementweises Ausschneiden | 1 | `Methode` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Zwischenlagerung | 1 | `Methode` | `gebaeude/Lysbuechel_Parkhaus.md` |
| „intelligent ruin“ | 1 | `Methode` | `Gebäude/Maison_DnA_Asse.md` |

## norm / recht

Markdown-Ziel: `reuse_database/19_Norm_Recht`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 19 | `Norm_Recht` | `Gebäude/Association_house_Plauen.md`, `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Berlin_Schildow_Pilot_House_2.md`, `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Boulder_Fire_Station_3.md`, `Gebäude/Brighton_Waste_House_Brighton.md`, `Gebäude/Broethen_Twin_House_Hoyerswerda.md`, `Gebäude/Ferme_du_Rail_Paris.md`, `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md`, `Gebäude/Institut_de_Botanique_ULg_Liege.md`, `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md`, `Gebäude/Mehrow_Pilot_House.md`, `Gebäude/Montessori_Maassluis.md`, `Gebäude/Upcycle_Studios_Copenhagen.md`, `Gebäude/Villa_Welpeloo_Enschede.md`, `Gebäude/Woongroep_Boschgaard_Den_Bosch.md`, `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Baubewilligung / Normen | 1 | `Norm_Recht` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Bauordnung/Zulassung | 1 | `Norm_Recht` | `Gebäude/Recyclinghaus_Hannover.md` |
| Belgische / Brüsseler Bauvorschriften, Schulbau, Brandschutz | 1 | `Norm_Recht` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Boulder Deconstruction Ordinance 8366 / 2020 | 1 | `Norm_Recht` | `Gebäude/Boulder_Fire_Station_3.md` |
| BREEAM Excellent | 1 | `Norm_Recht` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| CE/UKCA marked | 1 | `Norm_Recht` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Conservation Area / listed context near Tower Bridge | 1 | `Norm_Recht` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| CROW-CUR Guideline 4:2023 | 1 | `Norm_Recht` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Denkmal / listed monument | 1 | `Norm_Recht` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| DGBC / NIBE Paris Proof embodied | 1 | `Norm_Recht` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| EN 1090 | 1 | `Norm_Recht` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| EN 1168 + A3 / CROW-CUR Guideline 4:2023 als Fachbezug | 1 | `Norm_Recht` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| EPB | 1 | `Norm_Recht` | `Gebäude/gjG_House_Gentbrugge.md` |
| EPB / Energieperformance-Kontext | 1 | `Norm_Recht` | `Gebäude/Maison_DnA_Asse.md` |
| ERP / öffentlich zugängliches Gebäude | 1 | `Norm_Recht` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Eurocode 2, DIN EN 206-1, DIN 1045-2 | 1 | `Norm_Recht` | `Gebäude/Association_house_Plauen.md` |
| Grade II listing / Heritage at Risk | 1 | `Norm_Recht` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Grade-II-Listed Pier / Heritage-Kontext | 1 | `Norm_Recht` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Historic Sections Book | 1 | `Norm_Recht` | `Gebäude/BedZED_London_Hackbridge.md` |
| Japanisches Baurecht / Hotelbetrieb | 1 | `Norm_Recht` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| keine konkrete Normnummer öffentlich | 1 | `Norm_Recht` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Kunstintegration in öffentlichen Gebäuden | 1 | `Norm_Recht` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Nachweis technische Reusability für building authorities | 1 | `Norm_Recht` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Nordic Swan Ecolabel / Svanemærket | 1 | `Norm_Recht` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| NS 3682 für reuse of hollow-core slabs | 1 | `Norm_Recht` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Regelwerksarbeit / regulatorische Anpassung | 1 | `Norm_Recht` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| RT 2012 | 1 | `Norm_Recht` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| SCI P427 protocol | 1 | `Norm_Recht` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| SCI P427/P440; EN 1090 im allgemeinen Stahlreuse-Kontext | 1 | `Norm_Recht` | `Gebäude/Holbein_Gardens_London.md` |
| Southwark Planning / neue Planung 25/AP/2203 | 1 | `Norm_Recht` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Teile des Residence Palace 2004 gelistet | 1 | `Norm_Recht` | `Gebäude/Europa_Building_Brussels.md` |
| UKGBC Net Zero Carbon Buildings Framework; BREEAM Outstanding, WELL Platinum, NABERS 5 target | 1 | `Norm_Recht` | `Gebäude/Timber_Square_London.md` |
| unbekannt / pre-1970s protocol gap | 1 | `Norm_Recht` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| öffentliche Ausschreibung, building code | 1 | `Norm_Recht` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| öffentliche Vergabe / public procurement | 1 | `Norm_Recht` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| öffentlicher Markt / public procurement | 1 | `Norm_Recht` | `Gebäude/Grande_Halle_de_Colombelles.md` |

## ort

Markdown-Ziel: `reuse_database/04_Ort`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Basel | 2 | `Ort` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| Berlin_Neukoelln | 2 | `Ort` | `gebaeude/Bestandshalle_CRCLR_House.md`, `gebaeude/Kindl_Areal.md` |
| Hobelwerk_Areal_Oberwinterthur | 2 | `Ort` | `gebaeude/Altes_Hobelwerk_Winterthur.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| Lysbuechelareal_Basel | 2 | `Ort` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| 10 Whitechapel High St, London E1 8QS | 1 | `Ort` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| 2 bis rue de l’Ourcq, 75019 Paris | 1 | `Ort` | `Gebäude/Ferme_du_Rail_Paris.md` |
| 25 Lavington Street / Bankside, Southwark, London SE1 | 1 | `Ort` | `Gebäude/Timber_Square_London.md` |
| 29 Rue d’Amiens, 93240 Stains | 1 | `Ort` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Aarhus, Dänemark | 1 | `Ort` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Arnhem / Heerde, Niederlande | 1 | `Ort` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Asse, Belgien | 1 | `Ort` | `Gebäude/Maison_DnA_Asse.md` |
| Berlin-Neukölln | 1 | `Ort` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Berlin-Neukölln, Rollbergstraße 26 / 28a | 1 | `Ort` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Berlin_Mitte | 1 | `Ort` | `gebaeude/BOELL_LAB_Berlin.md` |
| Bleijerheide, Kerkrade, Niederlande | 1 | `Ort` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Boston / Cambridge / North Cambridge, MA, USA | 1 | `Ort` | `Gebäude/Big_Dig_Building_Boston.md` |
| Boulder, Colorado, USA | 1 | `Ort` | `Gebäude/Boulder_Fire_Station_3.md` |
| Boulevard Anspach / De Brouckère, Brüssel | 1 | `Ort` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Brent Cross, London, UK | 1 | `Ort` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Bruessel | 1 | `Ort` | `gebaeude/Da_Vinci_Business_District.md` |
| Bröthen / Hoyerswerda, Deutschland | 1 | `Ort` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Copenhagen / Ørestad, Dänemark | 1 | `Ort` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Den Bosch / ’s-Hertogenbosch, NL | 1 | `Ort` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Duiven, Niederlande | 1 | `Ort` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Elsässerstrasse 209/215 bzw. 215, Basel, Lysbüchel/Volta Nord | 1 | `Ort` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Evere | 1 | `Ort` | `gebaeude/Da_Vinci_Business_District.md` |
| Gentbrugge / Ghent, Belgien | 1 | `Ort` | `Gebäude/gjG_House_Gentbrugge.md` |
| Gladsaxe, Dänemark | 1 | `Ort` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Grubenstrasse 29, 8045 Zürich, Binz | 1 | `Ort` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Gröditz, Deutschland | 1 | `Ort` | `Gebäude/Association_house_Groeditz.md` |
| Hackbridge / Wallington, London Borough of Sutton, UK | 1 | `Ort` | `Gebäude/BedZED_London_Hackbridge.md` |
| Hannover EXPO 2000; Kloster Volkenroda, Thüringen | 1 | `Ort` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Hannover-Kronsberg / ehemaliges Expo-Areal | 1 | `Ort` | `Gebäude/Recyclinghaus_Hannover.md` |
| Hastings, United Kingdom | 1 | `Ort` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Heilbronn | 1 | `Ort` | `gebaeude/ReUseBox_Heilbronn.md` |
| Jätkäsaari, Helsinki, Finnland | 1 | `Ort` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Kamikatsu, Tokushima Prefecture, Japan | 1 | `Ort` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Karl_Marx_Allee_Berlin | 1 | `Ort` | `gebaeude/BOELL_LAB_Berlin.md` |
| Ketelhuisplein, Eindhoven, NL | 1 | `Ort` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Kloetinge, Zeeland, Niederlande | 1 | `Ort` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Kristian Augusts gate 13, Oslo, Norwegen | 1 | `Ort` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Lagerplatz / Winterthur, Schweiz | 1 | `Ort` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Lahdesjärvi, Tampere, Finnland | 1 | `Ort` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Lexington, Massachusetts, USA | 1 | `Ort` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Limes 7 / Leiden Bio Science Park, Oegstgeest/Leiden | 1 | `Ort` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Liège / Lüttich, Belgien | 1 | `Ort` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| London, UK | 1 | `Ort` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| London; UCL Festival of Engineering 2024, London Design Festival 2024, Futurebuild 2025 | 1 | `Ort` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Luxembourg-Limpertsberg, Luxemburg | 1 | `Ort` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Maassluis, Zuid-Holland, Niederlande | 1 | `Ort` | `Gebäude/Montessori_Maassluis.md` |
| Markt 1, 8647 Lo-Reninge, Belgien | 1 | `Ort` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Mehrow, Brandenburg, Deutschland | 1 | `Ort` | `Gebäude/Mehrow_Pilot_House.md` |
| Mühlhausen, Thüringen, Deutschland | 1 | `Ort` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| München, Deutschland | 1 | `Ort` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Münster, Rösnerstraße | 1 | `Ort` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Oberwinterthur | 1 | `Ort` | `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| Paris, Frankreich | 1 | `Ort` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Parvis de l’Hôtel de Ville, Paris | 1 | `Ort` | `Gebäude/Circular_Pavilion_Paris.md` |
| Paso Robles / Templeton Gap, Kalifornien, USA | 1 | `Ort` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Peter-Behrens-Halle TU Berlin; Tempelhofer Feld Berlin | 1 | `Ort` | `Gebäude/Plattenvereinigung_Berlin.md` |
| Place Masui / Rue des Palais, Brüssel | 1 | `Ort` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Plankenstraat 23, 1701 Dilbeek, Belgien | 1 | `Ort` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Plauen, Deutschland | 1 | `Ort` | `Gebäude/Association_house_Plauen.md` |
| Potkurinkatu, Härmälänranta, Tampere | 1 | `Ort` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Quai Fernand Demets 22, 1070 Anderlecht, Brüssel | 1 | `Ort` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Rollbergviertel | 1 | `Ort` | `gebaeude/Kindl_Areal.md` |
| Roombeek, Enschede, Niederlande | 1 | `Ort` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Rotterdam, Maasboulevard | 1 | `Ort` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Royal Borough of Kensington and Chelsea / Chelsea, London | 1 | `Ort` | `Gebäude/Holbein_Gardens_London.md` |
| Rue Charles Malis, Molenbeek-Saint-Jean, Brüssel | 1 | `Ort` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Rue de la Loi / Wetstraat, Brussels | 1 | `Ort` | `Gebäude/Europa_Building_Brussels.md` |
| Rue de la Vignette, Auderghem, Brüssel, Belgien | 1 | `Ort` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Rue des Ateliers, 14460 Colombelles | 1 | `Ort` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Rue des Brasseurs 3, 7700 Mouscron, Belgien | 1 | `Ort` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Schildow, Brandenburg, nördlich von Berlin | 1 | `Ort` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Schildow, Brandenburg/Berliner Umland, Deutschland | 1 | `Ort` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Sint-Jans-Molenbeek / Brüssel | 1 | `Ort` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Southwark, London, UK | 1 | `Ort` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Sulzerareal_Winterthur | 1 | `Ort` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Thoravej 29, 2400 København NV, Copenhagen | 1 | `Ort` | `Gebäude/Thoravej_29_Copenhagen.md` |
| University of Brighton City Campus, Grand Parade, Brighton | 1 | `Ort` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Utrecht, Croeselaan / Knoopkazerne-Areal | 1 | `Ort` | `Gebäude/The_Green_House_Utrecht.md` |
| Wolliner Straße 50, Berlin | 1 | `Ort` | `Gebäude/Plattenpalast_Berlin.md` |
| Zürich-Altstetten, Juch-Areal | 1 | `Ort` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Zürich-Wollishofen, Werkhof Mööslistrasse | 1 | `Ort` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Ørestad, Copenhagen, DK | 1 | `Ort` | `Gebäude/Upcycle_Studios_Copenhagen.md` |

## projekt

Markdown-Ziel: `reuse_database/02_Projekt`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Hobelwerk_Winterthur | 2 | `Projekt` | `gebaeude/Altes_Hobelwerk_Winterthur.md`, `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md` |
| Volta_Nord | 2 | `Projekt` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md` |
| 19 soziale Mietwohnungen + Nachbarschaftszentrum | 1 | `Projekt` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| 20 row houses / terraced houses | 1 | `Projekt` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| 318 Oxford Street retrofit | 1 | `Projekt` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| 80 MVA Substation für Brent Cross Town | 1 | `Projekt` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| A-Kruunu Mietwohnungsbau | 1 | `Projekt` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Alliander HQ / Liander office | 1 | `Projekt` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Anculus B.V. | 1 | `Projekt` | `Gebäude/Montessori_Maassluis.md` |
| Aufstockung Grubenstrasse | 1 | `Projekt` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Aufstockung um 3 Etagen | 1 | `Projekt` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Beddington Zero Energy Development | 1 | `Projekt` | `Gebäude/BedZED_London_Hackbridge.md` |
| Berlin_Global_Village | 1 | `Projekt` | `gebaeude/Kindl_Areal.md` |
| BioPartner Center Leiden, fünftes Gebäude | 1 | `Projekt` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| BOELL_LAB_Berlin | 1 | `Projekt` | `gebaeude/BOELL_LAB_Berlin.md` |
| Büroflügel im ehemaligen Discobereich | 1 | `Projekt` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Circular daycare / kindergarten | 1 | `Projekt` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| City of Boulder | 1 | `Projekt` | `Gebäude/Boulder_Fire_Station_3.md` |
| Coworking- und Community-Space | 1 | `Projekt` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Demontage und Wiederaufbau des gesamten Ensembles | 1 | `Projekt` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Fabrix Roots in the Sky | 1 | `Projekt` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Ferme des Possibles | 1 | `Projekt` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Forschungs- und Bildungsprojekt zur Recyclingkultur | 1 | `Projekt` | `Gebäude/Plattenvereinigung_Berlin.md` |
| Gebäude aus über 85 % Abfall-/Überschussmaterial | 1 | `Projekt` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| gekrümmte Ziegelschale mit Innenstruktur | 1 | `Projekt` | `Gebäude/gjG_House_Gentbrugge.md` |
| großmaßstäbliche Büro-/Mixed-use-Rekonversion | 1 | `Projekt` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Gundlach GmbH & Co. KG Wohnungsunternehmen | 1 | `Projekt` | `Gebäude/Recyclinghaus_Hannover.md` |
| Hastings Pier Regeneration | 1 | `Projekt` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Impact_Hub_Berlin_CRCLR | 1 | `Projekt` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| iQ Student Accommodation / Former Blackfriars Crown Court redevelopment | 1 | `Projekt` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Karreveld 1/2 | 1 | `Projekt` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Kindergarten mit Betreuung für Schule Manegg | 1 | `Projekt` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| KINDL_Zentrum_fuer_zeitgenoessische_Kunst | 1 | `Projekt` | `gebaeude/Kindl_Areal.md` |
| Kultur-/Ausstellungs-/Debattenpavillon | 1 | `Projekt` | `Gebäude/Circular_Pavilion_Paris.md` |
| Lagerplatz_Winterthur | 1 | `Projekt` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Maison des économies solidaires et innovantes / Les Canaux | 1 | `Projekt` | `Gebäude/Maison_des_Canaux_Paris.md` |
| Masui4Ever | 1 | `Projekt` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Meeting space during DDW 2017 | 1 | `Projekt` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Metso Lokomotion Technology Centre Phase 1 | 1 | `Projekt` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| moderne Arbeitswelt aus gebrauchten Materialien | 1 | `Projekt` | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Modissa Immobilien AG / HANUVER AG | 1 | `Projekt` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Net-zero / hybrid timber office redevelopment | 1 | `Projekt` | `Gebäude/Timber_Square_London.md` |
| Neubau aus wiederverwendeten Betonfertigteilen | 1 | `Projekt` | `Gebäude/Association_house_Groeditz.md` |
| Neubau eines Mehrfamilienhauses aus demontierten Plattenbauteilen | 1 | `Projekt` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Neubau mit gebrauchten Betonfertigteilen | 1 | `Projekt` | `Gebäude/Association_house_Plauen.md` |
| Neubau mit Reuse + bio-/geobasierten Materialien | 1 | `Projekt` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Neubau/Extension + Renovation-Kontext | 1 | `Projekt` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| neues PLP Studio | 1 | `Projekt` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Neues Recyclingzentrum ERZ Juch-Areal | 1 | `Projekt` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| New Boulder Fire-Rescue Station 3 | 1 | `Projekt` | `Gebäude/Boulder_Fire_Station_3.md` |
| new construction of Montessori School Maassluis | 1 | `Projekt` | `Gebäude/Montessori_Maassluis.md` |
| Pilotprojekt zur Wiederverwendung von WBS70-Platten | 1 | `Projekt` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| PV-überdachter Gerätebau | 1 | `Projekt` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Recyclinghaus Hanover/Hannover | 1 | `Projekt` | `Gebäude/Recyclinghaus_Hannover.md` |
| Recyclingzentrum und öffentlicher Raum | 1 | `Projekt` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Refurbishment plus 1-/2-geschossige Aufstockung | 1 | `Projekt` | `Gebäude/Holbein_Gardens_London.md` |
| Renovation and extension; neuer Museumsbau im Blockinneren | 1 | `Projekt` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Resource Rows | 1 | `Projekt` | `Gebäude/Resource_Rows_Copenhagen.md` |
| Restoration and extension of a former convent to create a town hall | 1 | `Projekt` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Retrofit + Extension zu Arbeitsplatznutzung | 1 | `Projekt` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Reuse and transformation / KA13 | 1 | `Projekt` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Reuse of Big Dig steel and concrete | 1 | `Projekt` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| ReUseBox_Heilbronn | 1 | `Projekt` | `gebaeude/ReUseBox_Heilbronn.md` |
| RotorDC_Da_Vinci_Site | 1 | `Projekt` | `gebaeude/Da_Vinci_Business_District.md` |
| Réinventer Paris 1 / Ourcq-Jaurès | 1 | `Projekt` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Schildow-Pilot / Wiederverwendung WBS70 | 1 | `Projekt` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| selektiver Rückbau Block 3000, Umbau Block 6000, Neugestaltung Außenanlagen | 1 | `Projekt` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Sitz Europäischer Rat / Rat der EU | 1 | `Projekt` | `Gebäude/Europa_Building_Brussels.md` |
| Stichting Montessorischolen Monton / Stichting Montessorischolen Midden-Nederland (Monton) | 1 | `Projekt` | `Gebäude/Montessori_Maassluis.md` |
| SUPERLOCAL – Super Circular Estate | 1 | `Projekt` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| TBC.London retrofit + extension | 1 | `Projekt` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| temporärer Stopgap / circular pavilion | 1 | `Projekt` | `Gebäude/The_Green_House_Utrecht.md` |
| Transformation zu Community-/Kultur-/Arbeitsgebäude | 1 | `Projekt` | `Gebäude/Thoravej_29_Copenhagen.md` |
| TRÆ | 1 | `Projekt` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| UCL Circular Economy Lab + UK CLT Pilot | 1 | `Projekt` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Umbau, Aufstockung und Impact Hub-Ausbau | 1 | `Projekt` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Umnutzung zu kommunaler Verwaltungsstelle | 1 | `Projekt` | `Gebäude/Charles_Malis_Molenbeek.md` |
| Umnutzung zu Kultur- und Gewerbehaus | 1 | `Projekt` | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Umwandlung in Tiers-lieu der Kreislaufwirtschaft | 1 | `Projekt` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Verbiest transformation | 1 | `Projekt` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Villa Welpeloo | 1 | `Projekt` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| VOLLGUT_eG | 1 | `Projekt` | `gebaeude/Kindl_Areal.md` |
| Wiederverwendung von Big-Dig-Infrastrukturmaterialien | 1 | `Projekt` | `Gebäude/Big_Dig_Building_Boston.md` |
| Wiederverwendung von P2-Plattenbauteilen | 1 | `Projekt` | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Wiederverwendung von Paneelen aus Olympiadorf-Bungalows | 1 | `Projekt` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Wiederverwendung von WBS70-Platten im Wohnhaus | 1 | `Projekt` | `Gebäude/Mehrow_Pilot_House.md` |
| Wohnbauprogramm_1000plus_Basel | 1 | `Projekt` | `gebaeude/Areal_Walkeweg_Nord.md` |
| Zero-Waste-Zentrum und Hotel | 1 | `Projekt` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |

## prozessphase

Markdown-Ziel: `reuse_database/11_Prozessphase`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| alle klassischen Neubauphasen durchgeführt | 1 | `Prozessphase` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Bauvertrag unterzeichnet | 1 | `Prozessphase` | `Gebäude/Montessori_Maassluis.md` |
| Beschaffung / Ausschreibung | 1 | `Prozessphase` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Demontage / Remanufacturing / Wiedereinbau | 1 | `Prozessphase` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Materialinventar / selektiver Rückbau | 1 | `Prozessphase` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Renovierung / Fassadenerneuerung | 1 | `Prozessphase` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Rückbau 2023, Refurbishment, Einbau 2025 | 1 | `Prozessphase` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Rückbau Herbst 2023, Einbau Oktober/Herbst 2024 | 1 | `Prozessphase` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Rückbau, Transport, Wiedereinbau | 1 | `Prozessphase` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Umbau, Rückbau, Aufbereitung, Wiedereinbau | 1 | `Prozessphase` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |

## pruefung

Markdown-Ziel: `reuse_database/15_Pruefung`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 15 | `Pruefung` | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md`, `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Broethen_Twin_House_Hoyerswerda.md`, `Gebäude/Institut_de_Botanique_ULg_Liege.md`, `Gebäude/Lo_Reninge_Town_Hall_Facade.md`, `Gebäude/Maison_DnA_Asse.md`, `Gebäude/Maison_Vignette_Auderghem.md`, `Gebäude/Montessori_Maassluis.md`, `Gebäude/Recyclinghaus_Hannover.md`, `Gebäude/Upcycle_Studios_Copenhagen.md`, `Gebäude/Verbiest_Karreveld_Brussels.md`, `Gebäude/Woongroep_Boschgaard_Den_Bosch.md`, `Gebäude/gjG_House_Gentbrugge.md` |
| Auswahl gemeinsam mit Statiker | 1 | `Pruefung` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Auswahl, Dokumentation, Testing/Verification von reclaimed steel | 1 | `Pruefung` | `Gebäude/Boulder_Fire_Station_3.md` |
| Bauteilkatalog mit Herkunft, Qualität, Montageanleitung | 1 | `Pruefung` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Belastungs-/Festigkeitsprüfung allgemein im IEMB-Kontext | 1 | `Pruefung` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| CST testing nach SCI P427; zerstörende und zerstörungsfreie Prüfungen | 1 | `Pruefung` | `Gebäude/Holbein_Gardens_London.md` |
| Dokumentation nach TEK; Tests/SINTEF für HCS laut Thesisquellen | 1 | `Pruefung` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Festigkeitstests / Belastungs-, Schneid-, Bohrversuche im IEMB-Kontext | 1 | `Pruefung` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Finite-Elemente-Modell, Lastversuch, nicht-destruktive Untersuchung | 1 | `Pruefung` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| fire testing, acoustics, insurance, vibration performance at scale | 1 | `Pruefung` | `Gebäude/Timber_Square_London.md` |
| Full-scale fire tests / DBI-Tests | 1 | `Pruefung` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Funktionsfähigkeit, Materialqualität, Umweltverträglichkeit, Energiebilanz, Wiederverwertbarkeit | 1 | `Pruefung` | `Gebäude/Plattenpalast_Berlin.md` |
| Independent testing + weld inspection | 1 | `Pruefung` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| konstruktive Analyse / RISA-3D | 1 | `Pruefung` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Laborversuche / mechanische Prüfung | 1 | `Pruefung` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Materialzustand / Eignung für Außenbekleidung | 1 | `Pruefung` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Monitoring / living laboratory | 1 | `Pruefung` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| nicht-destruktive Bewertung / Biegeversuche in Begleitforschung zu CLST | 1 | `Pruefung` | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Qualitätssicherung, Werksaufbereitung, Zulassungsdokumentation | 1 | `Pruefung` | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Sichtprüfung, Herstellungsdatum, Zustand, vorhandene Verbindungen, Fabrikationseignung | 1 | `Pruefung` | `Gebäude/BedZED_London_Hackbridge.md` |
| sorgfältige Qualitätssicherung | 1 | `Pruefung` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| tensile test, chemical analysis, metallographic examination | 1 | `Pruefung` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Testing + CE marking | 1 | `Pruefung` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Testing und recertification von Reuse-Stahl | 1 | `Pruefung` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Tests und Stabilitätsberechnungen berührt | 1 | `Pruefung` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Tragwerksberechnung mit schlechtester Stahlqualität aus Baujahr der Maschine | 1 | `Pruefung` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| unabhängiges Bauadviesbureau prüfte technische/finanzielle/prozessuale Machbarkeit | 1 | `Pruefung` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| unbekannt / IEMB-Forschungskontext | 1 | `Pruefung` | `Gebäude/Mehrow_Pilot_House.md` |
| Vermessung, Inventarisierung, Katalogisierung | 1 | `Pruefung` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| visuelle Analyse, Risikobewertung durch Bureau de contrôle | 1 | `Pruefung` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Werksprüfungen; Anforderungen klar erfüllt | 1 | `Pruefung` | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Zugversuche / chemische Analysen für Stahl | 1 | `Pruefung` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Zugversuche, chemische Analyse, Schweißbarkeit, Korrosionsschutz | 1 | `Pruefung` | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |

## reuse_strategie

Markdown-Ziel: `reuse_database/09_ReuseStrategie`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| ex-situ Bauteilwiederverwendung | 10 | `Reuse_Strategie` | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Boulder_Fire_Station_3.md`, `Gebäude/Broethen_Twin_House_Hoyerswerda.md`, `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md`, `Gebäude/Maison_Vignette_Auderghem.md`, `Gebäude/Mehrow_Pilot_House.md`, `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Bauteilwiederverwendung / Materialwiederverwendung | 2 | `Reuse_Strategie` | `Gebäude/Maison_DnA_Asse.md`, `Gebäude/gjG_House_Gentbrugge.md` |
| Ex-situ Bauteilwiederverwendung | 2 | `Reuse_Strategie` | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/BedZED_London_Hackbridge.md` |
| ex-situ Bauteilwiederverwendung; Zuschnitt; Remontage | 2 | `Reuse_Strategie` | `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Abfall als Ressource / on-site reuse / living lab | 1 | `Reuse_Strategie` | `Gebäude/Brighton_Waste_House_Brighton.md` |
| adaptive reuse + begrenzte Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Charles_Malis_Molenbeek.md` |
| adaptive reuse + partielle Bauteil-/Materialwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Bauteil- und Materialwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Bauteil- und Materialwiederverwendung, temporärer demontabler Neubau | 1 | `Reuse_Strategie` | `Gebäude/The_Green_House_Utrecht.md` |
| Bauteilsuche + Entwurf aus Verfügbarkeit | 1 | `Reuse_Strategie` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Bauteilwiederverwendung + adaptive reuse | 1 | `Reuse_Strategie` | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Bauteilwiederverwendung + in-situ Transformation + adaptive reuse | 1 | `Reuse_Strategie` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Bauteilwiederverwendung + Materialwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Bauteilwiederverwendung + Recyclingmaterial + recyclinggerechte Konstruktion | 1 | `Reuse_Strategie` | `Gebäude/Recyclinghaus_Hannover.md` |
| Borrowed building / reversible construction | 1 | `Reuse_Strategie` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Circular building site / on-site depot | 1 | `Reuse_Strategie` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| circular fit-out / reuse-first | 1 | `Reuse_Strategie` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Donorskelet / ex-situ structural reuse | 1 | `Reuse_Strategie` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| ex-situ / Gebäudeversetzung / Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Ex-situ auf demselben Standort / Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| ex-situ Bauteil-/Materialwiederverwendung in Gebäudehülle | 1 | `Reuse_Strategie` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| ex-situ Bauteilwiederverwendung / salvaged structural steel | 1 | `Reuse_Strategie` | `Gebäude/Holbein_Gardens_London.md` |
| ex-situ Bauteilwiederverwendung / strukturelle Wiederverwendung geplant | 1 | `Reuse_Strategie` | `Gebäude/Montessori_Maassluis.md` |
| ex-situ Bauteilwiederverwendung von Stahl + Bestandserhalt + DfD | 1 | `Reuse_Strategie` | `Gebäude/Timber_Square_London.md` |
| ex-situ Remontage | 1 | `Reuse_Strategie` | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Ex-situ steel reuse + in-project self-reuse | 1 | `Reuse_Strategie` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Ex-situ Wiederverwendung einer Hallenstruktur | 1 | `Reuse_Strategie` | `Gebäude/Recypark_Demets_Anderlecht.md` |
| ex-situ Wiederverwendung von Ziegeln in Fassade | 1 | `Reuse_Strategie` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| ex-situ; Infrastruktur-zu-Gebäude; Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Big_Dig_Building_Boston.md` |
| Gebäudeversetzung / komplett / ex-situ | 1 | `Reuse_Strategie` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Großmaßstäbliche Bauteilwiederverwendung + Transformation | 1 | `Reuse_Strategie` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| in-situ transformiert / Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| integrierter Re-Use-Pilot / Bauteiljäger*innen | 1 | `Reuse_Strategie` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Lot 01 „Réemploi“ | 1 | `Reuse_Strategie` | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Material- und Bauteilwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Materialgetriebener Entwurf / Superuse | 1 | `Reuse_Strategie` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| on-site selective deconstruction and reuse | 1 | `Reuse_Strategie` | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Oogsten / material harvesting, bauen mit Restmaterialien | 1 | `Reuse_Strategie` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| partielle Bauteil- und Materialwiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Maison_des_Canaux_Paris.md` |
| partielle Hüllbauteil-Wiederverwendung | 1 | `Reuse_Strategie` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Reuse von Stahlrohren / stockholder procurement | 1 | `Reuse_Strategie` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Upcycling / reuse of existing materials | 1 | `Reuse_Strategie` | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Ziegelwand-Module aus Rückbau | 1 | `Reuse_Strategie` | `Gebäude/Resource_Rows_Copenhagen.md` |

## schadstoff

Markdown-Ziel: `reuse_database/31_Schadstoff`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 9 | `Schadstoff` | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Boulder_Fire_Station_3.md`, `Gebäude/Brent_Cross_Town_Primary_Substation_London.md`, `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md`, `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md`, `Gebäude/Montessori_Maassluis.md`, `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md`, `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Asbest in Fensterrahmen | 1 | `Schadstoff` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| chemische Anforderungen des Nordic Swan Ecolabel | 1 | `Schadstoff` | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Faserzement/Eternit potenziell relevant | 1 | `Schadstoff` | `Gebäude/Recyclinghaus_Hannover.md` |
| Rost/Scaling/Materialzustand geprüft | 1 | `Schadstoff` | `Gebäude/BedZED_London_Hackbridge.md` |
| toxische Bahnschwellen/-platten als verworfene Option | 1 | `Schadstoff` | `Gebäude/Villa_Welpeloo_Enschede.md` |

## software / tools / werkzeug

Markdown-Ziel: `reuse_database/28_Tool_Software`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 14 | `Software/Tool`, `Werkzeug` | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/BedZED_London_Hackbridge.md`, `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Brent_Cross_Town_Primary_Substation_London.md`, `Gebäude/Brighton_Waste_House_Brighton.md`, `Gebäude/Grande_Halle_de_Colombelles.md`, `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md`, `Gebäude/Montessori_Maassluis.md`, `Gebäude/Recyclinghaus_Hannover.md`, `Gebäude/Upcycle_Studios_Copenhagen.md`, `Gebäude/Woongroep_Boschgaard_Den_Bosch.md`, `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Qflow | 2 | `Werkzeug` | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Concular / Restado | 1 | `Werkzeug` | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Diamant-Schneidemaschine | 1 | `Werkzeug` | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| digitale Tools / BIM | 1 | `Werkzeug` | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Entscheidungshilfe-Tool | 1 | `Werkzeug` | `Gebäude/Ferme_du_Rail_Paris.md` |
| Harvestmap / Oogstkaart | 1 | `Werkzeug` | `Gebäude/Villa_Welpeloo_Enschede.md` |
| HTS Reused Steel Stockmatcher | 1 | `Werkzeug` | `Gebäude/Timber_Square_London.md` |
| HTS Stockmatcher | 1 | `Werkzeug` | `Gebäude/Holbein_Gardens_London.md` |
| Madaster | 1 | `Werkzeug` | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| RISA-3D | 1 | `Werkzeug` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Seilsäge, Bohrungen, Hebekette, Spezial-Setup zum Kürzen | 1 | `Werkzeug` | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Smart measuring system | 1 | `Werkzeug` | `Gebäude/The_Green_House_Utrecht.md` |
| stockpile catalog / member identification | 1 | `Software/Tool` | `Gebäude/Boulder_Fire_Station_3.md` |
| Track-and-trace / Materialdatenbank / QR-Code / STABU-Code | 1 | `Werkzeug` | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |

## tragwerkssystem

Markdown-Ziel: `reuse_database/17_Tragwerkssystem`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| Holzbau | 3 | `Tragwerkssystem` | `gebaeude/Hobelwerk_Haus_D_Oberwinterthur.md`, `gebaeude/LysP8_Basel_Lysbuechelareal.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Stahlskelett | 2 | `Tragwerkssystem` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`, `gebaeude/ReUseBox_Heilbronn.md` |
| Stützen_Träger_System | 2 | `Tragwerkssystem` | `gebaeude/Areal_Walkeweg_Nord.md`, `gebaeude/Lysbuechel_Parkhaus.md` |
| 10-m-spannender, nachgespannter segmentierter Bogen | 1 | `Tragwerkssystem` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Aufstockung | 1 | `Tragwerkssystem` | `gebaeude/K118_Kopfbau_Halle_118_Winterthur.md` |
| autonome äußere Ziegelstruktur + innerer Holzrahmen | 1 | `Tragwerkssystem` | `Gebäude/Maison_DnA_Asse.md` |
| Bestand + verstärktes Stützenraster + neue Holz-/Stroh-/Lehm-Aufstockung | 1 | `Tragwerkssystem` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Bestandsstruktur | 1 | `Tragwerkssystem` | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| bestehende Gebäude + neue Überdachung / Verbindung | 1 | `Tragwerkssystem` | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| bestehendes Stahlstützensystem + donor HCS/Steel | 1 | `Tragwerkssystem` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| demontables Stahlrahmen-System aus galvanisierten Profilen | 1 | `Tragwerkssystem` | `Gebäude/The_Green_House_Utrecht.md` |
| Fertigteil-Wand-/Deckensystem | 1 | `Tragwerkssystem` | `Gebäude/Association_house_Groeditz.md` |
| formaktive, gekrümmte Ziegelschale + Stahl-/Holz-Infill | 1 | `Tragwerkssystem` | `Gebäude/gjG_House_Gentbrugge.md` |
| Holzaufstockung | 1 | `Tragwerkssystem` | `gebaeude/Bestandshalle_CRCLR_House.md` |
| Holzbau mit lokalem Holz | 1 | `Tragwerkssystem` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Holzrahmen / Holzstützen und -träger, Strohballen-Füllung | 1 | `Tragwerkssystem` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Holzstruktur im Neubau | 1 | `Tragwerkssystem` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Holztragwerk | 1 | `Tragwerkssystem` | `gebaeude/BOELL_LAB_Berlin.md` |
| Hybrid aus Glulam-Timber Columns und reclaimed steel beams | 1 | `Tragwerkssystem` | `Gebäude/Boulder_Fire_Station_3.md` |
| Hybrid aus Holzstützen und reused hollow core slabs | 1 | `Tragwerkssystem` | `Gebäude/Montessori_Maassluis.md` |
| Industriehalle | 1 | `Tragwerkssystem` | `gebaeude/Altes_Hobelwerk_Winterthur.md` |
| Infrastrukturbauteile als hoch belastbare Gebäudestruktur | 1 | `Tragwerkssystem` | `Gebäude/Big_Dig_Building_Boston.md` |
| Massivholzstützen, CLT-Decken, Betonkerne | 1 | `Tragwerkssystem` | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Modern pole barn / post-frame, Rohrtragwerk | 1 | `Tragwerkssystem` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| modulares, demontier- und wieder zusammensetzbares System | 1 | `Tragwerkssystem` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Neubau-Tragwerk; Reuse-Fassade nicht als Haupttragwerk | 1 | `Tragwerkssystem` | `Gebäude/Resource_Rows_Copenhagen.md` |
| neues CLT-Besucherzentrum | 1 | `Tragwerkssystem` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Parkhaus_Tragwerk | 1 | `Tragwerkssystem` | `gebaeude/Lysbuechel_Parkhaus.md` |
| Plattenbau-/Wandbau-System mit Fertigteilplatten | 1 | `Tragwerkssystem` | `Gebäude/Association_house_Plauen.md` |
| Rastertragwerk | 1 | `Tragwerkssystem` | `gebaeude/BOELL_LAB_Berlin.md` |
| Skelettbau | 1 | `Tragwerkssystem` | `gebaeude/Areal_Walkeweg_Nord.md` |
| Stahl- und Betontragwerk aus Big-Dig-Komponenten | 1 | `Tragwerkssystem` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Stahlbetonskelett | 1 | `Tragwerkssystem` | `gebaeude/ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md` |
| vorhandene Betonstützen/-balken/-Binder | 1 | `Tragwerkssystem` | `Gebäude/Charles_Malis_Molenbeek.md` |

## verbindung

Markdown-Ziel: `reuse_database/18_Verbindung`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 2 | `Verbindung` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md`, `Gebäude/Maison_DnA_Asse.md` |
| Anschlussdetails mit Toleranzen für verschiedene Profile | 1 | `Verbindung` | `Gebäude/BedZED_London_Hackbridge.md` |
| demontierbar detaillierte Stahlkonstruktion | 1 | `Verbindung` | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| demontierbare/modulare Fügung | 1 | `Verbindung` | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Fassadenmontage auf Neubau | 1 | `Verbindung` | `Gebäude/Resource_Rows_Copenhagen.md` |
| geneigte Fensterrahmen / Trennwandsystem | 1 | `Verbindung` | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| geschweißt | 1 | `Verbindung` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| heterogene Fenster in Holzrahmen | 1 | `Verbindung` | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Holzbekleidung auf neuem Visitor Centre | 1 | `Verbindung` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Kalkmörtel / traditioneller Lime mortar | 1 | `Verbindung` | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Nachspannung / post-tensioning | 1 | `Verbindung` | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| reversible joints / non-composite structural design | 1 | `Verbindung` | `Gebäude/Timber_Square_London.md` |
| Spannbänder / Metall-Umreifungsbänder | 1 | `Verbindung` | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Stabkreuzverbände, vertikale Zug-Kreuzverbände | 1 | `Verbindung` | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Stahlbauverbindungen | 1 | `Verbindung` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Stahllaschen und Bolzen; reversible Stahl-/Dübelverbindungen | 1 | `Verbindung` | `Gebäude/Plattenpalast_Berlin.md` |
| trockene / demontierbare Montage | 1 | `Verbindung` | `Gebäude/The_Green_House_Utrecht.md` |
| WBS70-Knoten / neue Anschlüsse unbekannt | 1 | `Verbindung` | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Ziegel-Claustra ohne zusätzliche metallische Aufhängung | 1 | `Verbindung` | `Gebäude/Maison_Vignette_Auderghem.md` |
| Ziegelschicht zum Höhenausgleich; überlappende Fassaden-Fertigteile | 1 | `Verbindung` | `Gebäude/Association_house_Groeditz.md` |

## wirtschaft

Markdown-Ziel: `reuse_database/22_Wirtschaft`

| Wert | Vorkommen | Roh-Typen | Quellen-Dateien |
|---|---:|---|---|
| unbekannt | 13 | `Wirtschaft` | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md`, `Gebäude/BioPartner_5_Leiden_Oegstgeest.md`, `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md`, `Gebäude/Liander_Alliander_HQ_Duiven.md`, `Gebäude/Lo_Reninge_Town_Hall_Facade.md`, `Gebäude/Maison_DnA_Asse.md`, `Gebäude/Maison_Vignette_Auderghem.md`, `Gebäude/Maison_des_Canaux_Paris.md`, `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md`, `Gebäude/Timber_Square_London.md`, `Gebäude/Villa_Welpeloo_Enschede.md`, `Gebäude/gjG_House_Gentbrugge.md` |
| Kostenwirkung | 2 | `Wirtschaft` | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| 55.000 € Bau-/Renovierungskosten; 15 m² | 1 | `Wirtschaft` | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| 80,000 € HT | 1 | `Wirtschaft` | `Gebäude/Circular_Pavilion_Paris.md` |
| 840 EUR/m² berichtet; ca. 1.100 EUR/m² Vergleich laut Biele | 1 | `Wirtschaft` | `Gebäude/Mehrow_Pilot_House.md` |
| Baukosten 3,072 Mio. € / 3,1 Mio. € HT | 1 | `Wirtschaft` | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Budget Kunstintervention 55.788 €; Architektur 2.976.107 € | 1 | `Wirtschaft` | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Budget sozialer Wohnungsbau | 1 | `Wirtschaft` | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| CHF 33,1 Mio. Ausführungskredit / CHF 18 Mio. frühere Schätzung / CHF 25 Mio. Perita-Bausumme | 1 | `Wirtschaft` | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Circulair bouwen nicht unbedingt billiger | 1 | `Wirtschaft` | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| free materials minus transport / lower cost claims | 1 | `Wirtschaft` | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| HCS 5–6× teurer als neue HCS laut Thesis | 1 | `Wirtschaft` | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Kosten etwa vergleichbar mit ähnlichem Neubau | 1 | `Wirtschaft` | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| kostenneutrale Re-Use-Einsparung / 9 % Kosteneinsparung Re-Use-Bauteile, 18 % Mehrhonorar Planung | 1 | `Wirtschaft` | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Materialkosten niedriger, aber keine Gesamteinsparung | 1 | `Wirtschaft` | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Miet-/Leasingmodelle für Licht/Möbel | 1 | `Wirtschaft` | `Gebäude/The_Green_House_Utrecht.md` |
| Projektkosten £180m | 1 | `Wirtschaft` | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Reclaimed steel ca. 4 % günstiger; mit Zusatzaufwand effektiv kostenneutral | 1 | `Wirtschaft` | `Gebäude/BedZED_London_Hackbridge.md` |
| wirtschaftlicher Einsatz von Reuse dort, wo sinnvoll | 1 | `Wirtschaft` | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| £12.6 Mio. / £11.4 Mio. HLF-Förderung | 1 | `Wirtschaft` | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| £64/sq ft; 68 % günstiger / 32 % Standard-Fit-out | 1 | `Wirtschaft` | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |

## Neue Oder Nicht Zugeordnete Entitaetstypen

Diese Typen standen in den Mapping-Tabellen, passen aber nicht direkt in die angefragte Liste oder wurden dort nicht explizit genannt. Sie sind als Kandidaten fuer neue Entitaeten, Untertypen oder spaetere Normalisierung zu lesen.

| Entitaetstyp | Roh-Paare | eindeutige Werte | Kandidaten n>=3 | Beispielwerte | Quellen-Dateien |
|---|---:|---:|---:|---|---|
| Spendergebäude | 7 | 7 | 0 | Herkunft der Bauteile muss dokumentiert werden; Herkunft der Platten ist nicht ausreichend erfasst; Herkunft der WBS70-Platten ist entscheidend; Herkunft und Entfernung bestimmen Machbarkeit; Mehrere Herkunftsgebäude müssen getrennt erfasst werden | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Berlin_Schildow_Pilot_House_2.md`, `Gebäude/Broethen_Twin_House_Hoyerswerda.md`, `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Donor-Gebäude | 3 | 3 | 0 | bestehende Entität „Gebäude“ reicht, aber Rolle als Bauteilquelle sollte explizit sein; Reuse braucht Herkunftsobjekt als eigene Entität; Rolle als Bauteilquelle ist zentral | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md`, `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Fertigteilsystem | 3 | 3 | 0 | Erfasst systemabhängige Bauteilgeometrien; P2-System ist für die Demontierbarkeit entscheidend; Plattenbautyp bestimmt Geometrie, Verbindung und Wiederverwendbarkeit | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md`, `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Quellenkonflikt | 3 | 3 | 0 | Mehrere belastbare Quellen geben unterschiedliche Flächen/Umfänge an.; mehrere Flächen-/Zeitangaben; Werte 60 % vs. 80 % müssen dokumentiert werden | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md`, `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md`, `Gebäude/Circular_Pavilion_Paris.md` |
| Reuse-vs-Recycling-Abgrenzung | 3 | 3 | 0 | Das Projekt mischt Direct Reuse, Recyclingmaterial und DfD.; Projekt kombiniert direkte Wiederverwendung und RC-Beton; Viele Materialien können reuse, recycled oder biosourced sein | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md`, `Gebäude/Maison_des_Canaux_Paris.md`, `Gebäude/Recyclinghaus_Hannover.md` |
| Bauteilzuschnitt | 2 | 2 | 0 | Wiederverwendung erfolgt durch kontrolliertes Zerschneiden; Wiederverwendung erfolgt nicht nur 1:1, sondern durch Maßanpassung | `Gebäude/Berlin_Schildow_Pilot_House.md`, `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Donor Building | 2 | 2 | 0 | Mehrere externe Gebäude liefern Bauteile; Reuse-Ketten brauchen ein Herkunftsgebäude als eigene Entität. | `Gebäude/Boulder_Fire_Station_3.md`, `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Donor-Projekt | 2 | 2 | 0 | Herkunft muss separat vom Receiver verwaltet werden; Stahl stammt aus einem anderen Projekt, nicht aus dem Empfängergebäude. | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md`, `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Donorgebäude | 2 | 2 | 0 | Das Projekt hängt stark von einem konkreten Spendergebäude ab.; Wiederverwendung hängt stark vom Herkunftsgebäude ab | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md`, `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Empfängergebäude | 2 | 2 | 0 | Erlaubt klare Zuordnung der neuen Nutzung und Anforderungen; Zielgebäude mit neuer Nutzung | `Gebäude/Association_house_Groeditz.md`, `Gebäude/Association_house_Plauen.md` |
| Materialgetriebener Entwurf | 2 | 2 | 0 | Bauteilmaße bestimmen räumliches Konzept; Der Entwurf folgt vorhandenen Querschnitten/Materialien | `Gebäude/BlueCity_Offices_Rotterdam.md`, `Gebäude/Villa_Welpeloo_Enschede.md` |
| Projektstatus | 2 | 2 | 0 | Bauzeit 2026–2027, Fertigstellung Q4 2027 geplant; completion scheduled end 2026; use early 2027 | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md`, `Gebäude/Montessori_Maassluis.md` |
| Reuse-Kette | 2 | 2 | 0 | Fall verbindet zwei oder mehr Projekte; Verknüpft Rückbauprojekt, Lagerung, Prüfung, neues Projekt | `Gebäude/55_Great_Suffolk_Street_London.md`, `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| As-built-Verifikation | 1 | 1 | 0 | Die Bewertung muss nach Fertigstellung überprüft werden. | `Gebäude/Montessori_Maassluis.md` |
| As-found-Komponente | 1 | 1 | 0 | Reuse mit minimaler Bearbeitung und Entwurf um vorhandene Teile | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Ausgleichsschicht | 1 | 1 | 0 | Konstruktive Reuse-Anpassung braucht eigene Erfassung | `Gebäude/Association_house_Groeditz.md` |
| Auszeichnung | 1 | 1 | 0 | Belgian Timber Construction Awards 2024 | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Bauteil-Archiv / Herkunftsmix | 1 | 1 | 0 | Bauteile stammen aus vielen Ländern und Quellen, nicht aus einem einzelnen Donor-Gebäude. | `Gebäude/Europa_Building_Brussels.md` |
| Bauteil-Ernte | 1 | 1 | 0 | „Harvesting“ ist hier operativ zentral | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Bauteilernte | 1 | 1 | 0 | Beschreibt aktive Gewinnung gebrauchter Bauteile aus der Region. | `Gebäude/Recyclinghaus_Hannover.md` |
| Bauteiljagd-Team | 1 | 1 | 0 | Die Beschaffung gebrauchter Bauteile ist eine eigenständige Projektrolle. | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Bauteiljäger / component hunting | 1 | 1 | 0 | beschreibt aktive Suche nach verfügbaren Bauteilen | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Bauteiljäger*in | 1 | 1 | 0 | beschreibt spezialisierte Suche nach verfügbaren Bauteilen | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Bauteilkatalog / Bauteilpass | 1 | 1 | 0 | dokumentiert Herkunft, Qualität und Montageanleitung | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Bauteilpool öffentlicher Bestand | 1 | 1 | 0 | Der Wettbewerb nutzte städtische Bestandsbauteile als Ressource. | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Bestandserhalt-Abzug | 1 | 1 | 0 | Verhindert Überbewertung von Umbauprojekten | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Bestandserhalt-Anteil | 1 | 1 | 0 | Hilft Sanierung von Wiederverwendung zu trennen | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Bestandserhalt-Ausschluss | 1 | 1 | 0 | Um Sanierung von Direct Reuse zu trennen | `Gebäude/Charles_Malis_Molenbeek.md` |
| Bestandserhalt-Warnung | 1 | 1 | 0 | Retention darf nicht als Direct Reuse gezählt werden | `Gebäude/Holbein_Gardens_London.md` |
| Bestandsintegration-Denkmal | 1 | 1 | 0 | Historische Bausubstanz wird einbezogen, darf aber nicht mit Direct Reuse verwechselt werden. | `Gebäude/Europa_Building_Brussels.md` |
| Betriebs-Reuse-System | 1 | 1 | 0 | Kuru Kuru Shop ist Teil der Nutzung, aber nicht automatisch Bau-Reuse | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Betriebszirkularität | 1 | 1 | 0 | Circularity umfasst Restaurantbetrieb, Leasing, Menü; nicht alles ist Bauteil-Reuse | `Gebäude/The_Green_House_Utrecht.md` |
| Bewohner-Selbstbau / Selbstwerkzaamheid | 1 | 1 | 0 | Beteiligung der künftigen Nutzer ist prozessprägend | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Bildungs-/Lehrbaustelle | 1 | 1 | 0 | Der Prozess war ausdrücklich als Ausbildung und Öffentlichkeit organisiert. | `Gebäude/Plattenvereinigung_Berlin.md` |
| Bildungs-/Partizipationsbezug | 1 | 1 | 0 | Schüler gestalten Fassadenbleche künstlerisch | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Bio-/Geo-/Reuse-Hybrid | 1 | 1 | 0 | Fall kombiniert mehrere Kreislaufstrategien; Direct Reuse muss trennscharf bleiben. | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Brandereignis | 1 | 1 | 0 | Direkter Auslöser und Materialquelle | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Campus-interner Kreislauf | 1 | 1 | 0 | Reuse findet zwischen Gebäudeteilen desselben Campus statt | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| CCTP-Variante / „CCTP à trous“ | 1 | 1 | 0 | Spezifische Ausschreibungstechnik für Reuse | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Circular building site | 1 | 1 | 0 | Prozess ist nicht linearer Abriss + Neubau | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Circular Workplace | 1 | 1 | 0 | Nutzungstyp kombiniert Reuse-Innenausbau und zirkuläre Unternehmen | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| CO₂-Budget / Paris-Proof-Bilanz | 1 | 1 | 0 | relevant für Bewertung, aber kein einzelner Kennwert | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Dauerhafte Außenruine | 1 | 1 | 0 | beschreibt eine bewusst langfristige, autonome Reuse-Schale | `Gebäude/Maison_DnA_Asse.md` |
| Deconstruction Ordinance | 1 | 1 | 0 | Lokales Recht kann Reuse auslösen. | `Gebäude/Boulder_Fire_Station_3.md` |
| Demonstrator-Station | 1 | 1 | 0 | Der Pilot wurde mehrfach ausgestellt und bleibt nicht eindeutig an einem Gebäudeort. | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Design-Build-Reuse | 1 | 1 | 0 | Entwurf und Ausführung liegen bei einer reuse-erfahrenen Organisation; wichtig für Haftung/Koordination. | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Donor Building unbekannt | 1 | 1 | 0 | Für strukturelle Hohlkörperdecken ist die Herkunft entscheidend. | `Gebäude/Montessori_Maassluis.md` |
| Donor-/Empfängerquartier | 1 | 1 | 0 | Materialströme bleiben im Quartier und sind nicht nur objektbezogen | `Gebäude/Superlocal_Expogebouw_Bleijerheide.md` |
| Donor-Gebäudegruppe | 1 | 1 | 0 | Herkunft ist oft mehrere Abbruchgebäude | `Gebäude/Resource_Rows_Copenhagen.md` |
| Donor-Industrie | 1 | 1 | 0 | Herkunft nicht aus Gebäude, sondern aus regionaler Ölindustrie | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Donor-Infrastruktur | 1 | 1 | 0 | Herkunft ist kein Gebäude, sondern Verkehrsinfrastruktur | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Donor-Receiver-Kette | 1 | 1 | 0 | Trennt Demontageerfolg vom tatsächlichen Wiedereinbau | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Donor-Site-Stahl | 1 | 1 | 0 | Stahlelemente stammen aus mehreren Quellen | `Gebäude/Holbein_Gardens_London.md` |
| Donorgebäude-Serie | 1 | 1 | 0 | Serien-/Systembauten sind bei Fertigteil-Reuse zentral | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Donorskelet | 1 | 1 | 0 | präziser als Bauteil, weil ein ganzes Tragwerksraster übertragen wird | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Donorstruktur | 1 | 1 | 0 | nicht nur Einzelbauteil, sondern zusammenhängende Halle | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Doppellisteneintrag | 1 | 1 | 0 | Die Fallnummerierung in der Ausgangsliste ist nicht mit den Quellen deckungsgleich | `Gebäude/Berlin_Schildow_Pilot_House_2.md` |
| Embodied-Carbon-Wertekonflikt | 1 | 1 | 0 | Quellen nennen 216 und 276 tCO₂e Einsparung | `Gebäude/Timber_Square_London.md` |
| Energie-Nebenfunktion | 1 | 1 | 0 | PV-Dach ist primäre Nutzungslogik, aber kein Reuse-Bauteil | `Gebäude/Saxum_Vineyard_Equipment_Barn_Paso_Robles.md` |
| Erinnerungsbauteil | 1 | 1 | 0 | kultureller Wert zählt getrennt von technischer Reuse | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Essential Facility / Risk Category | 1 | 1 | 0 | Feuerwachen haben höhere Anforderungen als normale Gebäude. | `Gebäude/Boulder_Fire_Station_3.md` |
| Fest eingebauter Innenausbau | 1 | 1 | 0 | Notwendig zur Abgrenzung gegenüber Möbel/Deko. | `Gebäude/Recyclinghaus_Hannover.md` |
| Fest installierte technische Ausstattung | 1 | 1 | 0 | Leuchten sind nur relevant, wenn fest verbaut | `Gebäude/Charles_Malis_Molenbeek.md` |
| Fit-out-Komponente | 1 | 1 | 0 | Für feste Innenausbau-Elemente zwischen Möbel und Bauteil | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Fit-out-Reuse | 1 | 1 | 0 | Innenausbau hat eigene Logik zwischen Möbel und Bauwerk | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Formaktive Reuse-Schale | 1 | 1 | 0 | erklärt, dass Stabilität durch Geometrie entsteht | `Gebäude/gjG_House_Gentbrugge.md` |
| Free-Issue-Material | 1 | 1 | 0 | Wiederverwendete Bauteile wurden vom Construction Manager im Auftrag des Clients beschafft | `Gebäude/BedZED_London_Hackbridge.md` |
| Gebäude-recycelt-sich-selbst | 1 | 1 | 0 | Der Fall beruht auf in-situ umgenutzten eigenen Bauteilen. | `Gebäude/Thoravej_29_Copenhagen.md` |
| Gemeindespende | 1 | 1 | 0 | Bauteile stammen von Einwohnern, nicht von klassischer Baustoffbörse | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| Geplanter Reuse-Einbau | 1 | 1 | 0 | Im Bau befindliche Projekte dürfen nicht wie gebaute Direct-Reuse-Fälle behandelt werden. | `Gebäude/Montessori_Maassluis.md` |
| Gewährleistungsersatzfonds | 1 | 1 | 0 | Bei Reuse-Fenstern kann Garantie durch Reparaturfonds ersetzt werden. | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Harvest Map / Oogstkaart | 1 | 1 | 0 | bildet Herkunft und Verfügbarkeit von Reuse-Material ab | `Gebäude/BlueCity_Offices_Rotterdam.md` |
| Heritage-Konflikt / Schutzstatuskonflikt | 1 | 1 | 0 | Quellen nennen unterschiedlich Grade II bzw. Grade 1 | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Herkunftsnarrativ | 1 | 1 | 0 | Die Herkunft der Bauteile ist Teil der baulichen Aussage. | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Historische Einbettung / Kontextanpassung | 1 | 1 | 0 | Der Fall ist weniger technisch als kultur-/ortsbezogen; Reuse-Ziegel dienen der Kontinuität mit dem Kloster. | `Gebäude/Lo_Reninge_Town_Hall_Facade.md` |
| Historische Profilbemessung | 1 | 1 | 0 | Wiederverwendeter Stahl hat oft andere historische Profileigenschaften | `Gebäude/BedZED_London_Hackbridge.md` |
| In-situ-Reuse-Kette | 1 | 1 | 0 | Bauteile verlassen das Gebäude nicht, werden aber neu zugeordnet | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| In-situ-Transformation | 1 | 1 | 0 | Bauteil bleibt aus demselben Gebäude, erhält aber neue Funktion | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Infrastruktur-Donor | 1 | 1 | 0 | Donor ist kein Gebäude, sondern Straßen-/Brücken-/Tunnelbau | `Gebäude/Big_Dig_Building_Boston.md` |
| Infrastruktur-Prototyp | 1 | 1 | 0 | Der Fall ist keine Gebäude-Fallstudie, zeigt aber tragende Direct-Reuse-Technik. | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Infrastrukturbauteil | 1 | 1 | 0 | Bauteile wie ramps, piers, Inverset panels passen nicht sauber in Hochbau-Kategorien | `Gebäude/Big_Dig_House_Lexington_Massachusetts.md` |
| Innere Nutzungsbox | 1 | 1 | 0 | trennt Energiehülle/Nutzung von der Reuse-Tragstruktur | `Gebäude/Maison_DnA_Asse.md` |
| Kommerzielle Replikation | 1 | 1 | 0 | Unterscheidet Marktreife von Forschungsmini-Pilot | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Kontrollierte Risikoprävention | 1 | 1 | 0 | Die Rolle des Kontrollbüros ist zentral für Aléas und Versicherbarkeit. | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Kulturhistorisches Reuse-Bauteil | 1 | 1 | 0 | Bauteile haben auch symbolische Herkunft. | `Gebäude/Plattenpalast_Berlin.md` |
| Kunstintegration als Reuse-Träger | 1 | 1 | 0 | Der Reuse-Einsatz entsteht aus einem Kunst-am-Bau-Prozess, bleibt aber baulich/fassadenrelevant. | `Gebäude/Musee_de_Folklore_Mouscron.md` |
| Leihmodell | 1 | 1 | 0 | Normale Bauteilbörse erfasst Eigentum/Rückgabe nicht | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Living Laboratory | 1 | 1 | 0 | Gebäude bleibt Forschungsplattform und wird weiter verändert | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Marine Exposition | 1 | 1 | 0 | Spezifische Leistungsumgebung für wiederverwendetes Holz | `Gebäude/Hastings_Pier_Visitor_Centre.md` |
| Matching-Algorithmus | 1 | 1 | 0 | Reuse-Stahl wurde digital mit Designanforderungen abgeglichen | `Gebäude/Timber_Square_London.md` |
| Material Stockpile | 1 | 1 | 0 | Geborgene Bauteile werden katalogisiert und später mehreren Projekten zugeordnet. | `Gebäude/Boulder_Fire_Station_3.md` |
| Materialallianz | 1 | 1 | 0 | Der Fall kombiniert Reuse mit bio-/geobasierten neuen Materialien; die Reuse-Bewertung muss beides trennen. | `Gebäude/Maison_Vignette_Auderghem.md` |
| Materialdepot / Lagerverwaltung | 1 | 1 | 0 | Lagerung ist planungsrelevant | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Materialeffizienz-Versprechen | 1 | 1 | 0 | Beschaffung/Vertrag kann Reuse auslösen | `Gebäude/Melkinlaituri_Primary_School_Daycare_Centre_Helsinki.md` |
| Materialherkunftsseite / QR-Materialatlas | 1 | 1 | 0 | projektspezifische Material-Herkunftsdokumentation | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Materialherkunftstyp | 1 | 1 | 0 | Unterscheidung Baustellenrest, Fehlbestellung, Lagerbestand, Rückbau | `Gebäude/Circular_Pavilion_Paris.md` |
| Materiallager / Zwischenlager | 1 | 1 | 0 | Für Reuse-Beschaffung zentral und nicht nur Transport | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Materialscout | 1 | 1 | 0 | Das Projekt begann mit aktiver Suche nach Bauteilen, nicht mit konventioneller Spezifikation | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Materialspuren / Patina | 1 | 1 | 0 | kulturelle Wirkung wiederverwendeter Bauteile | `Gebäude/BioPartner_5_Leiden_Oegstgeest.md` |
| Materialökosystem | 1 | 1 | 0 | TRÆ kombiniert biogene, recycelte und wiederverwendete Materialien als Strategie. | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Mauerwerksmodul | 1 | 1 | 0 | Kein einzelner Ziegel, sondern ausgeschnittenes Wandstück | `Gebäude/Resource_Rows_Copenhagen.md` |
| Mehrfachleben | 1 | 1 | 0 | Einige Bauteile haben schon drittes Leben. | `Gebäude/Jeugdkliniek_Ithaka_Emergis_Kloetinge.md` |
| Mobiles Recyclinggebäude | 1 | 1 | 0 | Der Fall ist weder Dauergebäude noch reine Baustelle; Mobilität ist zentral. | `Gebäude/Plattenvereinigung_Berlin.md` |
| Nicht gebauter Reuse-Vorschlag | 1 | 1 | 0 | direkte Wiederverwendung wurde geplant, aber nicht realisiert | `Gebäude/Big_Dig_Building_Boston.md` |
| Nicht-zählbare Möbelreuse | 1 | 1 | 0 | Im Projekt werden Türen zu Tischplatten; laut Grundregel zählt loses Mobiliar nicht. | `Gebäude/Thoravej_29_Copenhagen.md` |
| Nutzer-Crew / Eigenleistungsteam | 1 | 1 | 0 | Die technische Crew der Nutzerorganisation war Teil von Co-design / Co-execution. | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |
| Occasionslager | 1 | 1 | 0 | kommunaler Lager-/Beschaffungspfad für vorhandene Gegenstände | `Gebäude/Kindergarten_Moeoeslistrasse_Manegg_Zuerich.md` |
| Offcut-Verwertung | 1 | 1 | 0 | Reststücke sind keine klassischen Bauteile, können aber feste Bauteile bilden | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Ombruksgrad / Reuse-by-weight | 1 | 1 | 0 | Wiederverwendungsanteil als norwegischer Kennwert | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Oogstmaterial / geerntetes Material | 1 | 1 | 0 | Niederländische Praxis benennt Bauteile als „geerntet“, nicht nur gekauft | `Gebäude/Woongroep_Boschgaard_Den_Bosch.md` |
| Opportunitäts-Gisement | 1 | 1 | 0 | Materialverfügbarkeit war kurzfristig und ortsabhängig. | `Gebäude/Ferme_du_Rail_Paris.md` |
| Ortbeton-Bauteilernte | 1 | 1 | 0 | Reuse stammt nicht aus Fertigteilen, sondern aus gesägten Ortbetonwänden. | `Gebäude/ReCrete_footbridge_reused_concrete_blocks.md` |
| Parallelbetrieb | 1 | 1 | 0 | Umbau bei laufender Nutzung beeinflusst Reuse und Phasing | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Pilotnummerierung | 1 | 1 | 0 | Quellen widersprechen sich bei „1st/2nd“ | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Pilotserie | 1 | 1 | 0 | Mehrow und Schildow gehören zu einer frühen Pilotreihe | `Gebäude/Mehrow_Pilot_House.md` |
| Plattenbau-Typologie | 1 | 1 | 0 | WBS70/P2/PH12 usw. sind für Reuse von Großtafelbau wesentlich. | `Gebäude/Plattenpalast_Berlin.md` |
| Privatkleinanzeige / informeller Reuse-Markt | 1 | 1 | 0 | 2emain.be ist keine klassische Bauteilbörse, aber reale Beschaffungsquelle. | `Gebäude/Maison_Vignette_Auderghem.md` |
| Produktpass | 1 | 1 | 0 | Objektbezogene Dokumentation für Innenausbau | `Gebäude/Impact_Hub_Berlin_CRCLR_Fitout.md` |
| Projektabbruch / Strategiewechsel | 1 | 1 | 0 | Die Fallstudie ist als Reuse-Projekt relevant, aber nach aktuellem Stand ersetzt. | `Gebäude/Roots_in_the_Sky_Blackfriars_Crown_Court.md` |
| Projektübergreifender Materialtransfer | 1 | 1 | 0 | Bauteile stammen von anderer AgwA-/Baustelle | `Gebäude/Verbiest_Karreveld_Brussels.md` |
| Pufferraum-Fassade | 1 | 1 | 0 | Reuse-Fenster werden durch unbeheizte Pufferzone technisch möglich. | `Gebäude/Resilience_La_Ferme_des_Possibles_Stains.md` |
| Pädagogisches Bauprojekt | 1 | 1 | 0 | Studierende und Auszubildende bauten mit | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Quellenqualität | 1 | 1 | 0 | Fall ist hauptsächlich über Sekundärdatenbank belegt | `Gebäude/Broethen_Twin_House_Hoyerswerda.md` |
| Quellenunsicherheit | 1 | 1 | 0 | viele ältere Kleinprojekte sind nur über Sekundärdatenbanken greifbar | `Gebäude/Bestandverplanzung_Pavilion_Muenchen.md` |
| Quellgebäude | 1 | 1 | 0 | Reuse-Material stammt gezielt aus benachbartem Umbau | `Gebäude/The_Green_House_Utrecht.md` |
| Reaktivierung | 1 | 1 | 0 | technische/gestalterische Wiederinbetriebnahme gebrauchter Elemente | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Receiver-Projekt | 1 | 1 | 0 | Einbauort des Bauteils | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Reclaim-Manager / Materialbeschaffer | 1 | 1 | 0 | Direct Reuse erforderte aktive Suche, Fristen und Beschaffungskoordination | `Gebäude/BedZED_London_Hackbridge.md` |
| Refurbishing Plan | 1 | 1 | 0 | Zwischen Planung, Aufbereitung und Qualitätssicherung | `Gebäude/Circular_Centre_Netherlands_Prinsenhof_A_reuse_pilot.md` |
| Regelwerks-Pilot | 1 | 1 | 0 | Projekt erzeugt Lernwissen für neue Norm-/Regelarbeit | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Remanufactured Reuse-Bauteil | 1 | 1 | 0 | Der Fall ist nicht 1:1-Bauteilwiederverwendung, sondern Abbruchholz wird zu neuen tragenden Mass-Timber-Produkten verarbeitet. | `Gebäude/CascadeUp_London_secondary_timber_glulam_demonstrator.md` |
| Remanufacturing | 1 | 1 | 0 | Upcycle Studios nutzt gebrauchte/restliche Produkte, die für Neubaustandard aufbereitet werden | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Remontage | 1 | 1 | 0 | Wiederaufbauprozess ist nicht nur „Einbau“ | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Reserve-/Ersatzteillager | 1 | 1 | 0 | Bei Sonder-Bauteilen ist spätere Wartung problematisch | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Restlebensdauer-Erhalt | 1 | 1 | 0 | Fenster bleiben in alter Funktion wegen Restlebensdauer erhalten, zählen aber nicht als Direct Reuse. | `Gebäude/Thoravej_29_Copenhagen.md` |
| Restposten/Überschussprodukt | 1 | 1 | 0 | Nicht alle Second-Life-Elemente stammen aus Rückbau; Überschüsse können fest eingebaut werden, sind aber anders zu bewerten. | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Retained-Structure-Anteil | 1 | 1 | 0 | Methodisch abgrenzen von Direct Reuse | `Gebäude/Timber_Square_London.md` |
| Reuse vs. Recycling-Bilanz | 1 | 1 | 0 | nötig zur sauberen Bewertung | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Reuse-Beratung | 1 | 1 | 0 | spezifische Planungsrolle zwischen Entwurf, Beschaffung und Prüfung | `Gebäude/Multi_Brussels_Reuse_in_MULTI.md` |
| Reuse-Fassade als Bauteilsystem | 1 | 1 | 0 | Viele heterogene Bauteile bilden zusammen eine neue Hülle. | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Reuse-Forschungsreihe | 1 | 1 | 0 | mehrere BLAF-Häuser untersuchen Ziegelreuse | `Gebäude/gjG_House_Gentbrugge.md` |
| Reuse-Gewährleistung | 1 | 1 | 0 | Für geprüfte Altbauteile fehlt oft ein eindeutiger Rechts-/Haftungsrahmen. | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Reuse-Inszenierung | 1 | 1 | 0 | Architektur vermittelt Zero-Waste-Pädagogik sichtbar | `Gebäude/Kamikatsu_Zero_Waste_Center_Hotel_WHY.md` |
| ReUse-Interior | 1 | 1 | 0 | feste Innenausbau-Bauteile zwischen Möbel und Bauwerk | `Gebäude/AWM_Muenster_Circular_Office.md` |
| Reuse-Konformität | 1 | 1 | 0 | Zertifizierungsstatus wiederverwendeter Profile | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Reuse-Koordinator | 1 | 1 | 0 | Koordination zwischen Rückbau, Planung, Markt und Genehmigung | `Gebäude/KA13_Kristian_Augusts_gate_13_Oslo.md` |
| Reuse-Lieferkette | 1 | 1 | 0 | Erfasst Lieferanten, Rückbauunternehmen und Bauteilbörsen gemeinsam. | `Gebäude/Grubenstrasse_29_Werkhof_29_Zuerich.md` |
| Reuse-Los / Lot réemploi | 1 | 1 | 0 | Klassische Entitäten erfassen nicht, dass Wiederverwendung als eigenes Bau-/Beschaffungslos organisiert wurde. | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Reuse-Nachweisgrad | 1 | 1 | 0 | Unterscheidet belastbar belegte Reuse-Daten von sekundären Listenangaben | `Gebäude/Institut_de_Botanique_ULg_Liege.md` |
| Reuse-Pilotprojekt | 1 | 1 | 0 | markiert Forschungs-/Demonstratorrolle eines gebauten Falls | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Reuse-Protokoll | 1 | 1 | 0 | Prüfpfad ist zentral und kein klassisches Normfeld | `Gebäude/Holbein_Gardens_London.md` |
| Reuse-Quote mit Quellenkonflikt | 1 | 1 | 0 | Unterschiedliche Quellen nennen 42.5 %, 45 % und ca. 50 % | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Reuse-Rate nach Gewicht/Volumen | 1 | 1 | 0 | klassische Massenbilanz unterschätzt Leichtbauteile | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Reuse-Roadmap | 1 | 1 | 0 | nötig, weil kein Standardverfahren existierte | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Reuse-Screen | 1 | 1 | 0 | Bauwerkstyp zwischen Hülle, Tragwerk und technischer Infrastruktur | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Reuse-Stockholder | 1 | 1 | 0 | Spezifischer Akteur zwischen Rückbau und Wiedereinbau | `Gebäude/55_Great_Suffolk_Street_London.md` |
| Reuse-Testbau | 1 | 1 | 0 | Forschung erzeugt Prototyp-/Pilotstatus | `Gebäude/Berlin_Schildow_Pilot_House.md` |
| Reuse-Werkstatt auf Baustelle | 1 | 1 | 0 | verbindet Logistik, Aufbereitung und Beschäftigung | `Gebäude/Grande_Halle_de_Colombelles.md` |
| Reversible Verbindung | 1 | 1 | 0 | Zentrale technische Kategorie | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Risikobasierte Freigabe | 1 | 1 | 0 | Viele Bauteile wurden nicht über ATEx, sondern über Einzelfallrisiko bewertet. | `Gebäude/Ferme_du_Rail_Paris.md` |
| Rohbaukostenvorteil | 1 | 1 | 0 | Wirtschaftlicher Nutzen ist Kernargument | `Gebäude/Mehrow_Pilot_House.md` |
| Same-site urban mining | 1 | 1 | 0 | Donor und Empfänger sind dasselbe Grundstück | `Gebäude/Svanen_Kindergarten_Gladsaxe.md` |
| Self-Harvesting | 1 | 1 | 0 | Bauteile stammen aus dem eigenen Bestandsrückbau und werden im selben Projekt neu eingesetzt. | `Gebäude/CRCLR_House_Impact_Hub_Berlin.md` |
| Self-Reuse | 1 | 1 | 0 | Bauteile werden ausgebaut, refabriziert und im selben Projekt neu eingesetzt | `Gebäude/House_of_Fraser_318_Oxford_Street_TBC_London_reuse_chain.md` |
| Sozial-zirkulärer Akteur | 1 | 1 | 0 | Der Fall verbindet Reuse mit sozialer/solidarischer Wirtschaft | `Gebäude/Maison_des_Canaux_Paris.md` |
| Sozialer Baustellenprozess | 1 | 1 | 0 | Reuse und Low-Tech wurden mit Eingliederungsarbeit verbunden. | `Gebäude/Ferme_du_Rail_Paris.md` |
| Spende/Weitergabe | 1 | 1 | 0 | Reuse-Zahlen umfassen auch donation, nicht nur Einbau | `Gebäude/PLP_London_HQ_Circular_Studio_Fitout.md` |
| Stockholder / Reuse-Lieferant | 1 | 1 | 0 | Stahlreuse hängt an konkreten Lager-/Lieferantenbeständen | `Gebäude/Timber_Square_London.md` |
| Suffizienz-Umbau | 1 | 1 | 0 | Bewusste Beschränkung auf notwendige Eingriffe wirkt stark, ist aber nicht Direct Reuse. | `Gebäude/ELYS_Kultur_Gewerbehaus_Basel.md` |
| Surplus-/Restpostenmaterial | 1 | 1 | 0 | Viele eingesetzte Bauteile sind keine gebrauchten Bauteile, sondern Baustellen-/Produktionsüberschüsse. | `Gebäude/Chiro_d_Itterbeek_Dilbeek.md` |
| Surplus-Industriebauteil | 1 | 1 | 0 | Herkunft ist kein Gebäudeabbruch, sondern ungenutzte Pipeline-Projekte | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Symbolische Reuse-Fassade | 1 | 1 | 0 | Wiederverwendung erfüllt technische und repräsentative Funktion. | `Gebäude/Europa_Building_Brussels.md` |
| Temporäre Wiederaufbaubarkeit | 1 | 1 | 0 | Das Gebäude ist auf Ortswechsel nach 15 Jahren ausgelegt | `Gebäude/The_Green_House_Utrecht.md` |
| Temporäre Wiederaufstellung | 1 | 1 | 0 | Pavillon wird nach Demontage versetzt | `Gebäude/Circular_Pavilion_Paris.md` |
| Temporärer Demonstrator | 1 | 1 | 0 | Andere Bewertung als permanentes Gebäude | `Gebäude/Peoples_Pavilion_Eindhoven.md` |
| Temporärer Erstnutzer | 1 | 1 | 0 | Expo-Pavillon war von Beginn an für spätere Versetzung gedacht | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Traceability | 1 | 1 | 0 | Herkunft und Prüfung jedes Elements müssen verbunden bleiben | `Gebäude/Harmalanranta_A_Kruunu_ReCreate_mini_pilot_Tampere.md` |
| Translozierung | 1 | 1 | 0 | Wiederverwendung des ganzen Gebäudes durch Ortsversetzung | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Umgekehrter Entwurfsprozess | 1 | 1 | 0 | Entwurf folgt Bauteilfund, nicht umgekehrt | `Gebäude/K118_Kopfbau_Halle_118_Winterthur.md` |
| Upcycled product stream | 1 | 1 | 0 | mehrere Bauteile sind nicht direkt aus einem Gebäude übernommen, sondern industriell aufbereitet | `Gebäude/Upcycle_Studios_Copenhagen.md` |
| Upcycling-Produkt | 1 | 1 | 0 | Viele Elemente sind nicht einfache Direct-Reuse-Bauteile, sondern remanufactured/upcycled Produkte. | `Gebäude/TRAE_High_Rise_Aarhus.md` |
| Verpasste Reuse-Chance | 1 | 1 | 0 | Dokumentiert nicht nur Erfolg, sondern nicht realisierte Einsparung | `Gebäude/Brent_Cross_Town_Primary_Substation_London.md` |
| Versetzte Hallenkonstruktion | 1 | 1 | 0 | Reuse betrifft ein ganzes Tragwerks-/Hallensystem, nicht nur Einzelbauteile. | `Gebäude/Juch_Areal_Recyclingzentrum_Zuerich.md` |
| Verworfenes Reuse-Bauteil | 1 | 1 | 0 | Für Forschung wichtig, weil nicht jedes gefundene Bauteil nutzbar ist | `Gebäude/Villa_Welpeloo_Enschede.md` |
| Vorabkauf / öffentlicher Direktkauf | 1 | 1 | 0 | entscheidend für Reuse bei öffentlichem Auftrag | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Warnung Möbel | 1 | 1 | 0 | Bibliotheksmöbel aus gleichem Gebäude | `Gebäude/Lycee_Michel_Lucius_Conversion_Luxembourg.md` |
| Waste-as-infill | 1 | 1 | 0 | viele Materialien funktionieren als Hohlraumfüllung/Dämmexperiment, nicht als klassisches Bauteil | `Gebäude/Brighton_Waste_House_Brighton.md` |
| Wiederaufbau in gleicher Fügung | 1 | 1 | 0 | wichtig für Direct Reuse kompletter Gebäude | `Gebäude/Christ_Pavilion_Volkenroda.md` |
| Wiederverwendungsgrad Rohbau | 1 | 1 | 0 | Quantifiziert Anteil wiederverwendeter Rohbausubstanz | `Gebäude/Haus_HOS_Mehrfamilienhaus_Muehlhausen.md` |
| Worst-Case-Design | 1 | 1 | 0 | Entwurfs-/Nachweisstrategie für heterogene Gebrauchtteile | `Gebäude/Recypark_Demets_Anderlecht.md` |
| Zirkularitätsstrategie | 1 | 1 | 0 | Reuse-Fall enthält viele nicht direkt bauteilbezogene Strategien | `Gebäude/Liander_Alliander_HQ_Duiven.md` |
| Zulassungspfad / standortspezifische Genehmigung | 1 | 1 | 0 | Bei reused Tragbauteilen ist der Nachweisweg oft wichtiger als eine einzelne Norm | `Gebäude/Lokomotion_Technology_Centre_mini_pilot_Tampere.md` |
| Öffentliche Beschaffung / Procurement-Mechanik | 1 | 1 | 0 | Die Wiederverwendung hing stark an Ausschreibungs- und Vergabelogik, nicht nur an Bautechnik. | `Gebäude/Zinneke_Feder_Masui4ever_Brussels.md` |

## Abgeleitete Entitaeten

Neben den Roh-Typen wurden aus den Daten zusaetzlich abgeleitete Knoten erzeugt.

| Typ | CSV-Zeilen | CSV | Markdown-Ziel | Anzahl MD-Dateien |
|---|---:|---|---|---:|
| `Bauteilposition` | 175 | `_extract/derived/bauteilposition.csv` | `reuse_database/07_Bauteilposition` | 175 |
| `ReuseKette` | 70 | `_extract/derived/reusekette.csv` | `reuse_database/10_ReuseKette` | 70 |
| `Datenpunkt` | 170 | `_extract/derived/datenpunkt.csv` | `reuse_database/24_Datenpunkt` | 169 |
| `Quelle` | 191 | `_extract/derived/quelle.csv` | `reuse_database/27_Quelle` | 191 |
| `Quellenkonflikt` | 17 | `_extract/derived/quellenkonflikt.csv` | `reuse_database/33_Quellenkonflikt` | 17 |
| `Offene_Frage` | 86 | `_extract/derived/offene_frage.csv` | `reuse_database/34_Offene_Frage` | 83 |
