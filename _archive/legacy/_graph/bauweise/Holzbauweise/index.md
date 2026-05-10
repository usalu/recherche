---
id: "Holzbauweise"
entity: "bauweise"
node_kind: "knot"
migration_status: "migrated_phase2_semantic_corrections"
migration_action: "semantic_split"
title: "Holzbauweise"
legacy_type: "Tragwerkssystem"
legacy_paths:
  - "tragwerkssystem\Aufstockung_in_Holzbauweise.md"
target_primary: "bauweise/Holzbauweise"
target_roles: "phase2_secondary"
risk_flags: "old_type_tragwerkssystem_overgeneralized"
---
# Holzbauweise

## Migration

- Target: bauweise/Holzbauweise
- Legacy source count: 1
- Legacy types: Tragwerkssystem
- Migration actions: semantic_split
- Target roles: phase2_secondary
- Risk flags: old_type_tragwerkssystem_overgeneralized

## Legacy Content: tragwerkssystem\Aufstockung_in_Holzbauweise.md

---
type: Tragwerkssystem
bauteil: ["[[bauteil/Fassade]]"]
projekt: ["[[projekt/Aufstockung]]"]
reuse_strategie: ["[[reuse_strategie/Umnutzung]]"]
verwandt: ["[[tragwerkssystem/Holz_Skelettbau]]", "[[tragwerkssystem/Reversible_Fuegung]]", "[[tragwerkssystem/Skelettbauweise]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Tragwerkssysteme; Bauen im Bestand; Nachverdichtung; Ressourcenschonung durch Bestandserhalt; leichte, vorgefertigte Tragwerke; Design for Disassembly.
- **Verwandte Dateien:** `tragwerkssystem/Holz_Skelettbau.md`; `tragwerkssystem/Skelettbauweise.md`; `tragwerkssystem/Reversible_Fuegung.md`; `bauteil/Dach.md`; `bauteil/Decke.md`; `bauteil/Fassade.md`; `verbindung/Holzverbindungen.md`; `verbindung/Schraubverbindung.md`; `pruefung/Bestandsaufnahme.md`; `pruefung/Tragwerkspruefung.md`; `reuse_strategie/Weiterbauen.md`; `reuse_strategie/Umnutzung.md`; `projekt/Aufstockung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Tragwerksplanung Bestand; Holzbauunternehmen und Modulbauunternehmen; Brandschutzplanung; Bauphysik; Bestandserkundung; statische Nachrechnung; Lignum-Publikationen zu Holz-Aufstockungen; FNR-Forschungsberichte zu Holz in der Aufstockung; ISO 20887:2020; Eurocode 0/1/5; nationale Holzbau-, Brand- und Schallschutzregeln; DGNB-Zirkularitätsindex und Gebäuderessourcenpass; Materialpass / Bauteilpass.

## Kurzdefinition

Aufstockung in Holzbauweise bezeichnet die Erweiterung eines bestehenden Gebäudes um ein oder mehrere Geschosse mit Holz- oder Holz-Hybrid-Systemen. Typische Systeme sind Holzrahmenbau, Holztafelbau, Brettsperrholz- bzw. Massivholzbau, Holz-Skelettbau und Raumzellen- bzw. Modulbau. Im Kontext der Wiederverwendung ist die Aufstockung doppelt relevant: Der vorhandene Baukörper bleibt als Primärressource erhalten, während der neue Aufbau so geplant werden kann, dass seine Bauteile später lösbar, dokumentiert und möglichst sortenrein weiterverwendbar sind.

## Relevanz für Wiederverwendung im Bauwesen

- **Bestandserhalt als höchste ReUse-Strategie:** Aufstockung vermeidet häufig Abriss und Neubau, nutzt vorhandene Fundamente, Erschließung, Anschlüsse und graue Energie weiter und schafft zusätzliche Nutzfläche ohne neue Bodenversiegelung.
- **Geringe Eigenlast:** Holzsysteme sind im Vergleich zu mineralischen Tragwerken leicht. Das ist für Bestandsgebäude mit begrenzten Lastreserven entscheidend und reduziert Eingriffe in Fundament, Stützen, Wände und Aussteifung.
- **Vorfertigung und trockene Montage:** Hohe Vorfertigungsgrade verkürzen Bauzeiten auf bewohnten oder weitergenutzten Gebäuden. Werkseitig hergestellte Elemente lassen sich besser dokumentieren, nummerieren und später rückbauen.
- **Reversible Systemlogik möglich:** Bei mechanisch gefügten Wand-, Decken-, Dach- und Modulbauteilen kann die Aufstockung als spätere Materialbank geplant werden. Entscheidend sind zugängliche Fügungen, lösbare Anschlüsse, getrennte Schichten und dauerhafte Dokumentation.
- **Schnittstelle Bestand/Neu als kritischer Punkt:** Die Holzaufstockung selbst kann demontierbar sein, die Verbindung zum Bestand ist jedoch oft durch Einbauteile, Verguss, Abdichtung, Brandschutzbekleidungen oder Lastverteilungsmaßnahmen schwer reversibel.

## Fachinhalt

### Systemlogik

- **Lastabtrag:** Vertikallasten der Aufstockung werden über neue Holzstützen, Wände, Linienlager oder Lastverteilungsträger in das bestehende Tragwerk eingeleitet. Dabei sind Lastreserven, Fundamente, vorhandene Wandachsen, Deckenplatten und Setzungen zu prüfen.
- **Horizontalaussteifung:** Wind- und Erdbebenlasten werden über aussteifende Holztafeln, Brettsperrholzscheiben, Verbände, Kerne oder den Bestand abgetragen. Die Einleitung horizontaler Kräfte in den Bestand ist häufig nachweisintensiver als der vertikale Lastabtrag.
- **Systemvarianten:**
  - Holzrahmen-/Holztafelbau: leicht, gut vorfertigbar, hohe Integration von Dämmung; ReUse-Potenzial bei lösbaren Schichten und zugänglichen Verbindungsmitteln.
  - Brettsperrholz-/Massivholzbau: hohe Scheibenwirkung, robuste Elemente; Rückbaupotenzial abhängig von Verbindungsmitteln, Oberflächen, Öffnungen und Zuschnitten.
  - Holz-Skelettbau: hohe Grundrissflexibilität, gute Trennung zwischen Tragwerk und Ausbau; geeignet für spätere Nutzungsänderung.
  - Holzmodulbau/Raumzellen: sehr schnelle Montage; ReUse-Potenzial besonders hoch, wenn Module transportgerecht dimensioniert, verschraubt und installationstechnisch lösbar verbunden sind.
  - Holz-Hybrid-Aufstockung: Kombination mit Stahl, Beton, mineralischen Brandschutzschichten oder Verbunddecken; technisch leistungsfähig, aber häufig schlechter sortenrein rückbaubar.

### Fügungsprinzipien

- **Bevorzugt:** Schraub-, Bolzen-, Stabdübel-, Knotenblech-, Auflager- und Klemmverbindungen; sicht- oder zugänglich angeordnet; standardisierte Verbindungsmittel; austauschbare Brandschutzbekleidungen.
- **Problematisch für Wiederverwendung:** Verklebte Schichten, vergossene Anschlussdetails, unzugängliche verdeckte Verbinder, irreversible Abdichtungsanschlüsse, Verbunddecken ohne Trennstrategie, Nassestriche direkt auf Holzbauteilen.
- **Schnittstelle Bestand:** Auflagerbalken, Stahlbeton-Ringanker, Lastverteilungsroste, Durchdringungen und Abdichtungen sollten so geplant werden, dass Holzbauteile vom Bestand getrennt lösbar bleiben. Wenn irreversible Bestandseingriffe unvermeidbar sind, sind sie zu dokumentieren.

### Demontierbarkeit und Bauteilpass

- Bauteile erhalten eindeutige Kennzeichnung, Achsraster, Materialangaben, Verbindungsmittel, Einbaudatum, Festigkeitsklasse, Feuchte- und Brandschutzinformationen.
- Tragsystem, Gebäudehülle und Ausbau sollten als getrennte Schichten geplant werden: Tragwerk vor Witterung geschützt, Fassade lösbar, Installationen zugänglich, Abdichtungen austauschbar.
- Rückbauplanung muss Montagefolge umkehrbar machen: Hebepunkte, temporäre Aussteifung, Kranbarkeit, Demontageöffnungen, Zugang zu Verbindungsmitteln.

### Prüf- und Nachweisfragen

- Vor Aufstockung: Bestandsstatik, Materialfestigkeiten, Schadstoffe, Feuerwiderstand, Schallschutz, Setzungen, Fundamentreserven, Erdbeben- und Windnachweis, Feuchte- und Holzschutzkonzept.
- Für spätere Wiederverwendung: Sichtprüfung, Holzfeuchte, Verformungen, Risse, Bohr- und Schraubenlöcher, Insekten-/Pilzbefall, Klebstoff- und Beschichtungszustand, Brandschutzbekleidung, Resttragfähigkeit.
- Nachweislücken bestehen vor allem bei gebrauchten Holzprodukten ohne durchgängige Klassifizierung, bei veränderten Querschnitten, bei verdeckten Schäden und bei der rechtlichen Einordnung als Bauprodukt.

## Praxisbezug / Beispiele

- **Wohnungsbau-Nachverdichtung:** Mehrgeschossige Wohnbauten der Nachkriegszeit besitzen oft regelmäßige Raster und erschlossene Dachflächen. Holzaufstockungen können hier zusätzliche Wohnungen schaffen, wenn Tragreserven und Brandschutz lösbar geplant werden.
- **Energetische Sanierung gekoppelt mit Aufstockung:** Zusätzliche Nutzfläche kann wirtschaftlich helfen, Fassaden-, Dach- und Haustechnik-Sanierungen des Bestands mitzufinanzieren. Aus ReUse-Sicht sollte die neue Hülle nicht untrennbar mit dem Tragwerk verklebt werden.
- **Modulare Aufstockungen:** Raumzellen oder großformatige Holzmodule erlauben kurze Montagezeiten. Für spätere Wiederverwendung sind Transportabmessungen, Knotenpunkte, Installationskupplungen und zerstörungsfrei lösbare Anschlüsse entscheidend.
- **Bestandsdach als Materialquelle:** Beim Abbruch vorhandener Dachtragwerke können Holzsparren, Pfetten, Stahlträger, Ziegel oder Bleche parallel als ReUse-Potenzial erfasst werden. Die neue Aufstockung sollte diese Materialinventur nicht nur als Abfalllogistik, sondern als Planungsaufgabe behandeln.

## Herausforderungen / offene Fragen

- **Tragreserven des Bestands:** Bestandsunterlagen sind oft unvollständig; Fundament-, Decken- und Wandreserven müssen durch Erkundung und Nachrechnung belastbar nachgewiesen werden.
- **Brandschutz und Schallschutz:** Mehrgeschossige Holzaufstockungen benötigen häufig zusätzliche Bekleidungen, Kapselungen und Schichten, die Rückbau und sortenreine Trennung erschweren können.
- **Feuchte- und Witterungsrisiko:** Dachöffnung und Montagephase sind schadensanfällig. Temporärer Wetterschutz ist für spätere ReUse-Qualität ebenso wichtig wie für den Erstgebrauch.
- **Schnittstellenkomplexität:** Bestandsanschlüsse, Dachabdichtung, haustechnische Durchdringungen, Treppenhaus-/Aufzugserweiterungen und Brandschottungen sind oft nicht reversibel.
- **Produkt- und Haftungsfragen:** Für gebrauchte oder später wiederzuverwendende Holzbauteile fehlen in vielen Ländern routinierte Re-Qualifizierungsverfahren, besonders für tragende Anwendungen.
- **Ökobilanzliche Abwägung:** Eine leichte Holzaufstockung kann ökologisch sehr günstig sein, verliert aber Potenzial, wenn Bauteile verklebt, verkapselt, nicht dokumentiert oder am Lebensende verbrannt statt wiederverwendet werden.

## Quellen

- ISO 20887:2020: *Sustainability in buildings and civil engineering works — Design for disassembly and adaptability — Principles, requirements and guidance*. https://www.iso.org/standard/69370.html
- Lignum: *Holzbau – Aufstocken* (Broschüre, 2020). https://www.lignum.ch/files/images/Downloads_deutsch/Broschuere_Aufstocken_2020.pdf
- Fachagentur Nachwachsende Rohstoffe / Projektbericht: *Holz in der Aufstockung – Bewertung und Umsetzung von Aufstockungsmaßnahmen in Holzbauweise*. https://www.fnr.de/fileadmin/projektdatenbank/2220HV004A.pdf
- Thomschke, O.: *Aufstockung mit Holz im Wohnbau – Bedarf, Potenzial und konstruktive Lösungsansätze*, TU Wien, 2020. https://repositum.tuwien.at/handle/20.500.12708/15005
- Ottenhaus, L.-M. et al.: *Design for adaptability, disassembly and reuse – A review of reversible timber connection systems*, Construction and Building Materials, 2023.
- European Commission: *Level(s) — European framework for sustainable buildings*. https://green-forum.ec.europa.eu/green-business/levels_en
- DGNB: *Circular building / Gebäuderessourcenpass / Zirkularitätsindex*. https://www.dgnb.de/en/sustainable-building/circular-building/
- EN 1990, EN 1991, EN 1995 mit nationalen Anhängen; nationale Brandschutz-, Schallschutz- und Holzschutzregelwerke.

