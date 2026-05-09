---
entity: "quelle"
id: "Geb_ude_Maison_Vignette_Auderghem_md"
title: "Geb_ude_Maison_Vignette_Auderghem_md"
build_status: "promoted_phase42"
source_filename: "Maison_Vignette_Auderghem.md"
---

# Geb_ude_Maison_Vignette_Auderghem_md

**Recherchezeitpunkt:** 2026-05-06  
**Sprache:** Deutsch  
**Grundregel angewandt:** Gezählt werden nur tatsächlich wiederverwendete Bau-, Hüll-, Raum-, Technik- oder fest eingebaute Konstruktionselemente. Biosourcierte Materialien wie Holz, Stroh, Hanf-Kalk werden dokumentiert, aber **nicht** als Direct Reuse gezählt, wenn sie neu sind.

## 2. ENTITÄTEN-MAPPING

| Entität | Wert | Beziehung zur Fallstudie | Quelle/Beleg | Vertrauensgrad | Anmerkung |
|---|---|---|---|---|---|
| Fallstudie | Maison Vignette / Vignette House | Untersuchter Fall | [S1], [S2], [S3] | belegt | Ausgangsliste und mehrere Projektquellen. |
| Gebäude | Einfamilienhaus in Auderghem | Zielgebäude | [S2], [S3] | belegt | Neubau auf unbebautem Grundstück. |
| Projekt | Neubau mit Reuse + bio-/geobasierten Materialien | Projektlogik | [S2], [S3], [S4] | belegt | Mischung aus Strategien. |
| Ort | Rue de la Vignette, Auderghem, Brüssel, Belgien | Standort | [S2] | belegt | Adresse nur auf Straßenebene veröffentlicht. |
| People | Karbon’ architecture & urbanisme | Architekt | [S2], [S3] | belegt | Entwurf. |
| People | Pierre Stoffel / BESP Stoffel & Partners; Sofiane Boudahri | Tragwerks-/Engineering-Unterstützung | [S2], [S3] | belegt | Unterschiedliche Quellen nennen Pierre Stoffel bzw. BESP/Sofiane Boudahri. |
| Bauherr | Private owner | Bauherr | [S3] | belegt | Privater Auftrag. |
| Bauteil | Large/Grote Boomse Steen Ziegel | Reuse-Fassadenbauteil | [S2], [S3] | belegt | 3.000 Stück / 36 m². |
| Bauteil | Wandfliesen aus Solvay-Gebäude | Reuse-Innenausbau | [S2] | belegt | 21 m². |
| Bauteil | Terrakotta-Bodenfliesen | Reuse-Boden | [S2] | belegt | 13,5 m². |
| Bauteil | Blausteinplatten | Reuse-Boden / Terrasse / Eingang | [S2] | belegt | 40 m² über 2emain.be. |
| Bauteil | Sanitärausstattung | Reuse-Technik/fester Ausbau | [S2] | belegt | Waschbecken/Vasen/Atelierbecken von Rotor DC. |
| Bauteilbörse | Franck Bricks; Rotor DC; 2emain.be | Lieferquellen | [S2] | belegt | Reuse-Markt/Dealer + Kleinanzeigen. |
| Material | Holz, Stroh, Hanf-Kalk, Naturputz | neue bio-/geobasierte Materialien | [S2], [S3] | belegt | Nicht als Direct Reuse gezählt. |
| Reuse-Strategie | ex-situ Bauteilwiederverwendung | zentrale Strategie | [S2], [S3] | belegt | Mehrere Bauteilgruppen. |
| Tragwerkssystem | Holzrahmen / Holzstützen und -träger, Strohballen-Füllung | Haupttragwerk, nicht Reuse | [S2], [S3] | belegt | Neubau-Tragwerk. |
| Verbindung | Ziegel-Claustra ohne zusätzliche metallische Aufhängung | besondere Fassadenlösung | [S2] | belegt | Breiter Ziegeltyp ermöglicht konstruktive Lösung. |
| Förderprogramm | Be Exemplary | Anerkennung / Projektförderkontext | [S2], [S5] | belegt | Projekt als exemplarisch anerkannt. |
| Bericht | FCRBE 32 detailed project sheets | Sekundäranalyse | [S3] | belegt | Enthält Projektfläche, Dauer, Akteure. |
| Kennwert | 3.000 Ziegel / 36 m² Fassade | Mengen | [S2], [S3] | belegt | Zentrales Reuse-Kennwertpaar. |
| Prüfung | unbekannt | Prüf-/Zulassungsdaten | keine Quelle gefunden | unbekannt | Keine Prüfprotokolle. |
| Wirtschaft | unbekannt | Kostenwirkung | keine Quelle gefunden | unbekannt | Keine Kostenkennwerte gefunden. |

### Vorgeschlagene neue Entität

| Neue Entität | Warum nötig? | Beispiel aus dem Fall | Beziehung zu bestehenden Entitäten |
|---|---|---|---|
| Materialallianz | Der Fall kombiniert Reuse mit bio-/geobasierten neuen Materialien; die Reuse-Bewertung muss beides trennen. | Reuse-Ziegel + neue Holz-/Stroh-/Hanfkalk-Konstruktion. | Verknüpft Material, Reuse-Strategie, Tragwerkssystem und Bewertung. |
| Privatkleinanzeige / informeller Reuse-Markt | 2emain.be ist keine klassische Bauteilbörse, aber reale Beschaffungsquelle. | 40 m² Blausteinplatten über 2emain.be. | Unterform von Bauteilbörse / Beschaffung. |

## 4. REUSE-STRATEGIE

- **Art der Wiederverwendung:** partiell; ex-situ; Bauteilwiederverwendung; Materialwiederverwendung; Neubau mit Direct Reuse
- **Hauptniveau:** Gebäudehülle + räumlicher Innenausbau + Sanitär/feste Technik
- **Unterschied zu Sanierung, Recycling oder Bestandserhalt:** Es handelt sich nicht um Bestandserhalt, sondern um Neubau. Ziegel, Fliesen, Platten und Sanitär werden als Bauteile wieder eingebaut, nicht zu Recyclinggranulat verarbeitet.
- **Warum ist der Fall relevant?** Er zeigt, dass in einem kleinen privaten Neubau mehrere Reuse-Lieferketten kombiniert werden können, ohne dass das Haupttragwerk selbst reuse-basiert sein muss.

## 6. PROZESS UND LOGISTIK

| Prozessphase | Handlung | Akteure | Methode | Werkzeug/Tool/Software | Abbruchmethode | Aufbereitungsmethode | Prüfung | Logistik | Hürde | Lösung | Quelle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Bestandsaufnahme | Kein Gebäudebestand; Suche nach Reuse-Bauteilen | Bauherrschaft, Karbon | Materialsuche parallel zum Entwurf | unbekannt | entfällt | unbekannt | unbekannt | mehrere Lieferketten | Verfügbarkeit kleiner Mengen | kleine Projektgröße erlaubt spezifische Lots | [S2], [S3] |
| Bauteilinventar | Auswahl verfügbarer Ziegel, Fliesen, Platten, Sanitär | Karbon, Händler | komponentenbasierte Planung | unbekannt | unbekannt | Sortierung/Reinigung unbekannt | unbekannt | Händler + Kleinanzeigen | Mengen- und Maßbindung | Entwurf an verfügbare Bauteile anpassen | [S2] |
| Schadstoffprüfung | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Sanitär/Fliesen-Herkunft | unbekannt | keine Quelle |
| Rückbau | durch vorgelagerte Lieferanten/Quellen | Franck, Rotor DC, unbekannte Vorbesitzer | selektive Demontage unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | ex-situ | Herkunft nicht komplett publiziert | Händler übernehmen Teile der Kette | [S2] |
| Ausbau | unbekannt | Lieferanten | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Transport | Lieferung der Reuse-Bauteile zur Baustelle | Lieferanten / Bauunternehmen | Kleinmengenlogistik | unbekannt | unbekannt | unbekannt | unbekannt | Auderghem | Koordination mehrerer Quellen | Projektgröße reduziert Risiko | [S2] |
| Lagerung | unbekannt | Bauunternehmen | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Bruch/Sortierung | unbekannt | keine Quelle |
| Aufbereitung | mögliche Reinigung/Zuschnitt/Sortierung | Händler/Ausführende | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | Qualitätsschwankung | robuste Bauteile wählen | [S2] |
| Planung | Reuse-Ziegel als Claustra; bio-/geobasierte Struktur | Karbon, Ingenieure | Entwurf nach Materialeigenschaften | unbekannt | entfällt | unbekannt | unbekannt | Abstimmung auf verfügbare Maße | Fassadenlösung ohne Metallaufhängung | breiter Ziegeltyp gewählt | [S2] |
| Genehmigung | Bau eines privaten Einfamilienhauses | Bauherrschaft/Behörde | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |
| Wiedereinbau | Einbau von Ziegeln, Belägen, Sanitär | Gauthier Nagant, 3ALJ Construct | traditionelle Bauprozesse mit Reuse-Bauteilen | unbekannt | entfällt | unbekannt | unbekannt | Baustelle | Passgenauigkeit / Restmengen | Restziegel im Garten weitergenutzt | [S2], [S3] |
| Monitoring | unbekannt | unbekannt | unbekannt | unbekannt | entfällt | unbekannt | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle |

## 8. KENNWERTE

| Kennwert | Wert | Einheit | Methode/Datenmodell/Software | Bilanzgrenze | Quelle | Vertrauensgrad |
|---|---:|---|---|---|---|---|
| wiederverwendete Ziegel | 3.000 | Stück | Projektangabe | Fassadenclaustra | [S2], [S3] | belegt |
| wiederverwendete Ziegelfläche | 36 | m² | Projektangabe | Fassade | [S2], [S3] | belegt |
| Wandfliesen Reuse | 21 | m² | Projektangabe | Innenausbau | [S2] | belegt |
| Bodenfliesen Reuse | 13,5 | m² | Projektangabe | Boden | [S2] | belegt |
| Blausteinplatten Reuse | 40 | m² | Projektangabe | Eingang/Terrasse | [S2] | belegt |
| Fläche | 255 | m² | FCRBE case sheet | Gebäude | [S3] | belegt |
| Fläche alternative Quelle | 213 | m² | Presse/Be Exemplary | Gebäude | [S5] | teilweise belegt |
| Projektzeitraum | 2018–2020 | Jahre | FCRBE | Projekt | [S3] | belegt |
| CO₂-Einsparung | unbekannt | kg CO₂e | unbekannt | unbekannt | keine Quelle | unbekannt |
| Kosten | unbekannt | € | unbekannt | unbekannt | keine Quelle | unbekannt |
| Transportdistanz | unbekannt | km | unbekannt | unbekannt | keine Quelle | unbekannt |
| U-Wert / Energiebedarf | unbekannt | unbekannt | unbekannt | unbekannt | keine Quelle | unbekannt |

## 10. WIRTSCHAFT UND BESCHAFFUNG

- **Beschaffungsmodell:** privates Projekt mit mehreren Reuse-Lieferquellen.
- **Bauteilbörse / Quelle:** Franck Bricks für Ziegel; Rotor DC für Fliesen/Sanitär; 2emain.be für Blausteinplatten.
- **Kostenwirkung:** unbekannt
- **Zeitwirkung:** unbekannt
- **Versicherung / Haftung:** unbekannt
- **Gewährleistung:** unbekannt
- **Arbeitsaufwand:** vermutlich erhöht durch Materialsuche und Anpassung; nicht quantifiziert.
- **Lagerung:** unbekannt
- **Marktbarrieren:** kleinteilige Verfügbarkeit, Kompatibilität von Maßen, unbekannte Prüf-/Gewährleistungslogik.

## 12. OFFENE ENTITÄTEN UND DATENLÜCKEN

- **Welche bestehenden Entitäten wurden nicht gefunden?** Abbruchmethode, Bericht zu Prüfungen, Normen, Schadstoffprüfung, Software, detaillierte Wirtschaft, Versicherung, Gewährleistung, Monitoring.
- **Welche neuen Entitäten wären sinnvoll?** Materialallianz; informeller Reuse-Markt; Kleinmengenlogistik.
- **Welche Daten fehlen?** Herkunftsgebäude der Ziegel, exakte Stückzahl der Sanitärteile, Prüf- und Zulassungsdetails, Kosten, Transportdistanzen, CO₂-Bilanz, U-Werte.
- **Welche Quellen müssten geprüft werden?** Original-Bauakten, Karbon-Ausführungsdetails, Händlerrechnungen, Bruxelles Environnement Reportage, FCRBE-Voll-PDF.

## Quellen und Links

- [S1] Interne Ausgangsliste: `gebäude4_wiederverwendung_direct_reuse_examples.md`, Priorität 54.
- [S2] Opalis – Maison Vignette: https://opalis.eu/fr/projets/maison-vignette
- [S3] FCRBE / Bruxelles Environnement – 32 detailed project sheets, #07 Maison Vignette: https://gidsduurzamegebouwen.brussels/sites/default/files/documents/2024-06/dt4_2_2_project-sheets_041023_lr.pdf
- [S4] Opalis – Maison Vignette, Karbon’ architecture et urbanisme: https://opalis.eu/fr/projets/maison-vignette-karbon-architecture-et-urbanisme
- [S5] Architectura.be – Be.Exemplary 3, Projekt Vignette: https://www.architectura.be/fr/actualite/voici-les-laureats-de-l-appel-a-projets-beexemplary-3/
