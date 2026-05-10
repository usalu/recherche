---
id: "Material_Index"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Material Index"
source_count: 2
legacy_paths:
  - "bauteilboerse\\material-index.md"
  - "werkzeug\\Material_Index.md"
raw_targets:
  - "software_digitaltool/Material_Index"
migration_actions:
  - "semantic_move"
  - "split_platform_profile"
risk_flags:
  - "duplicate_with_akteur_or_werkzeug"
  - "may_duplicate_bauteilboerse_or_akteur"
---
# Material Index

## Migration

- Canonical target: software_digitaltool/Material_Index
- Legacy source count: 2
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: bauteilboerse\material-index.md

- Map action: split_platform_profile
- Target role in map: primary
- Raw mapped target: software_digitaltool/material_index
- Original primary target: software_digitaltool/material_index
- Original secondary targets: akteur/<operator_if_named>; beschaffungsweg/Digitale_Plattform; ressourcenquelle/Bauteilboerse; plattformfunktion/Material_Matching

---
type: Bauteilbörse
---

# Material Index

## Kurzbeschreibung
Material Index ist ein(e) professionelle Reuse-Plattform mit Audits, Inventar, Materialpässen, Brokerage und B2B-Marketplace mit Bezug zu Vereinigtes Königreich. Im Reuse-Kontext liegt der Schwerpunkt auf: Audit und Inventarisierung vorhandener Materialien.

## Land / Region
Vereinigtes Königreich

## Betreiber
Material Index

## Zielgruppe
Bauherrschaft, Immobilienwirtschaft, Bauunternehmen, Planende, Rückbau-/Fit-out-Projekte

## Plattformtyp
professionelle Reuse-Plattform mit Audits, Inventar, Materialpässen, Brokerage und B2B-Marketplace

## Bauteilkategorien
reclaimed/refurbished components, building materials, interior fit-out, furniture, partitions, doors, site setup items und weitere Bau-/Ausstattungsteile

## Art der Wiederverwendung
Audit und Inventarisierung vorhandener Materialien; Aufbereitung/Brokerage; Verkauf/Beschaffung über Marketplace

## Funktionen
Gebäudeaudits; Inventory Management; Material Tracking; Marketplace; Reports zu Kosten/CO2/Abfall; Spezifikation/Brokerage

## Daten je Bauteil
Produkt- und Materialdaten aus Audits und Listings; genaue öffentliche Felder je Marketplace/Projekt

## Qualität / Prüfung
Quelle nennt quality refurbished/reclaimed components; Rückgabe bei fehlerhaften/nicht spezifikationsgemäßen Materialien in AGB erwähnt; Details je Handelspartner

## Logistik / Lagerung
end-to-end workflow; Lieferung/Rückgabe je Marketplace-Bedingungen; Lagerung nicht allgemein angegeben

## Geschäftsmodell
B2B-Plattform und Dienstleistungen; Marketplace-Verkauf; Gebühren nicht vollständig öffentlich angegeben

## Ökologische Bewertung
soll Abfall, CO2 und Kosten reduzieren; quantifizierte Reduktionen projekt-/berichtabhängig, nicht je öffentlichem Listing angegeben

## Stärken
starke professionelle Daten- und Auditbasis; gute Passung für große Bau-/Fit-out-Projekte; Markt und Materialinventar verbunden

## Schwächen / Hemmnisse
weniger niedrigschwellig für Privatkunden; Zugang teils service- oder partnerabhängig

## Relevanz für zirkuläres Bauen
sehr hoch für datenbasiertes zirkuläres Bauen und professionelle Reuse-Beschaffung im UK-Markt.

## Quellen und Links
- https://material-index.co.uk/
- https://material-index.exchange/edits
- https://www.material-index.co.uk/materials/material-specification
- https://asbp.org.uk/member/material-index
- https://material-index.exchange/terms-and-conditions

---
Hinweis: Verfügbarkeit, Zustand, Maße, Normen- und Brandschutzanforderungen müssen vor Spezifikation oder Kauf direkt mit Anbieter/Betreiber geprüft werden.

### Legacy Source: werkzeug\Material_Index.md

- Map action: semantic_move
- Target role in map: primary
- Raw mapped target: software_digitaltool/Material_Index
- Original primary target: software_digitaltool/Material_Index
- Original secondary targets: 

---
type: Werkzeug
dokument: ["[[dokument/Pre_Demolition_Audit]]"]
verwandt: ["[[werkzeug/BIM]]", "[[werkzeug/Concular_Plattform]]", "[[werkzeug/IFC_Viewer]]", "[[werkzeug/Madaster_Plattform]]", "[[werkzeug/Materialdatenbank]]"]
---

# Material Index

## Verknüpfungen

- **Übergeordnete Themen:** digitale Materialinventare; Pre-Demolition-Audits; Material Brokerage; Reuse-Marktplätze; Materialpass; Portfolio-Management; zirkuläre Bauwirtschaft.
- **Verwandte Dateien:** `werkzeug/Madaster_Plattform.md`; `werkzeug/Concular_Plattform.md`; `werkzeug/Materialdatenbank.md`; `werkzeug/BIM.md`; `werkzeug/IFC_Viewer.md`; `dokument/Pre_Demolition_Audit.md`; `datenmodell/Materialpass.md`; `methode/Selektiver_Rueckbau.md`; `logistik/Materialflussplanung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Material Index; UK-Immobilien- und Bauwirtschaft; BREEAM; Greater London Authority Circular Economy Statements; Rückbauaudits; Materialpass; Reuse Brokerage; Portfolio-Lösungen.

## Kurzdefinition

**Material Index** ist eine britische Circular-Construction-Plattform, die digitale Materialinventare, Pre-Demolition- und Deconstruction-Audits, Materialpässe, Berichte, Austausch- und Vermittlungsfunktionen sowie Material Brokerage verbindet. Die Plattform unterstützt die Erfassung von Materialien vor Umbau, Sanierung oder Rückbau und soll ihre Wiederverwendung in Projekten oder Portfolios erleichtern.

## Relevanz für Wiederverwendung im Bauwesen

Material Index ist besonders relevant, weil es einen kritischen Übergang digitalisiert: **vom Bestand zum wiederverwendbaren Materialangebot**. Während klassische Marktplätze erst bei vorhandenen Produkten ansetzen, beginnt Material Index bereits bei der Vor-Ort-Erfassung im Gebäude. Dadurch werden Materialien sichtbar, bevor sie als Abfall anfallen.

Relevante Beiträge zur Wiederverwendung:

- **Frühe Identifikation:** Materialien können vor Rückbau oder Sanierung inventarisiert werden.
- **Bewertung und Priorisierung:** Wiederverwendungspfade, Demontagehinweise, Materialwert und Embodied-Carbon-Daten können in Entscheidungen einfließen.
- **Berichtsfähigkeit:** Audits können Anforderungen aus BREEAM oder Circular Economy Statements unterstützen.
- **Materialpass-Logik:** Daten können projekt- oder portfoliobezogen gepflegt werden.
- **Vermittlung:** Durch Marketplace- und Brokerage-Funktionen wird aus Inventardaten ein potenzieller Sekundärmarkt.

## Fachinhalt

### Funktionsweise

Die Material-Index-Plattform ist auf Desktop und mobilen Geräten nutzbar und dient der schnellen Erfassung von Materialien auf der Baustelle oder im Bestand. Sie unterstützt Verwaltung, Reporting und Austausch der aufgenommenen Materialien.

Typische Prozesslogik:

1. **Audit-Setup:** Gebäude, Projekt, Flächen, Rückbauabschnitte und Nutzerrollen werden angelegt.
2. **Vor-Ort-Erfassung:** Auditor:innen katalogisieren Materialien, Bauteile und Ausstattung digital.
3. **Datenanreicherung:** Mengen, Zustand, Demontierbarkeit, Wiederverwendungspfad, Materialwert und CO₂-Daten werden ergänzt.
4. **Reporting:** Ergebnisse werden für Kund:innen, Planungsteams, Zertifizierungen oder Genehmigungsprozesse aufbereitet.
5. **Transferplanung:** Materialien werden intern wiederverwendet, verkauft, vermittelt oder an externe Abnehmer:innen gegeben.
6. **Portfolio-Auswertung:** Über mehrere Liegenschaften lassen sich wiederkehrende Materialströme erkennen.

### Datentypen

- Gebäudestandort, Projektphase und Rückbauzeitpunkt;
- Material- oder Produkttyp;
- Bauteilkategorie und Einsatzort im Gebäude;
- Menge, Abmessungen, Volumen, Gewicht;
- Zustand, Wiederverwendbarkeit und Demontageaufwand;
- Fotos, Notizen, Prüf- und Dokumentationsdaten;
- Wiederverwendungspfad: intern, extern, Recycling, Entsorgung;
- Materialwert oder Wiederverkaufswert;
- Embodied-Carbon-Daten;
- Reuse- und Deconstruction-Empfehlungen;
- Berichtsdaten für BREEAM, GLA oder interne ESG-Ziele.

### Einsatzszenarien

- **Pre-Demolition Audit:** Bestände werden vor Abbruch systematisch erfasst.
- **Pre-Redevelopment Audit:** Umbauten und Sanierungen werden als Materialquelle analysiert.
- **Material Reclamation Audit:** Fokus auf rückgewinnbare Produkte und Bauelemente.
- **Contractor Licence:** Bauunternehmen nutzen die Plattform für eigene Projekte.
- **Material Passports:** erfasste Produkte werden als wiederverwendungsrelevante Datensätze dokumentiert.
- **Portfolio Solution:** Eigentümer:innen identifizieren wiederkehrende Materialströme und interne Austauschoptionen.

### Abgrenzung

Material Index ist stärker audit- und datengetrieben als einfache Marketplace-Tools. Gegenüber reinen BIM- oder IFC-Werkzeugen liegt der Schwerpunkt nicht auf Geometrie, sondern auf Materialidentifikation, Reuse-Entscheidung, Reporting und Transfer. Gegenüber Materialpass-Plattformen ist Material Index stärker auf Rückbau- und Umbauprozesse sowie Brokerage ausgerichtet.

## Praxisbezug / Beispiele

Material Index beschreibt sich selbst als britische Circular-Construction-Plattform mit Marketplace, Pre-Demolition-Audit-Service und digitaler Plattform zur Reduktion von Embodied Carbon, Abfallvermeidung und Erfüllung von BREEAM- bzw. GLA-Anforderungen. Die Geovation-Darstellung betont, dass die Plattform Materialien in Gebäuden katalogisiert und vor Renovierung oder Abriss zum höchsten Wert verkauft. Wates kündigte 2026 den landesweiten Roll-out der Material-Index-Plattform an, um Materialwiederverwendung über Projekte und Portfolio hinweg zu ermöglichen.

Für Forschung und Repo ist Material Index vor allem als Beispiel für die Verbindung von **digitalem Audit, Materialpass, Marktplatz und professionellem Brokerage** relevant.

## Herausforderungen / offene Fragen

- **Auditqualität:** Der Nutzen hängt stark von der Genauigkeit der Vor-Ort-Erfassung ab.
- **Datenvollständigkeit:** Ohne technische Dokumente bleiben viele Bauteile nur eingeschränkt wiederverwendbar.
- **Zeitfenster:** Materialien müssen vor Rückbau erfasst und rechtzeitig vermittelt werden.
- **Bewertungsmethodik:** Materialwert, CO₂-Einsparung und Wiederverwendungspfad beruhen auf Annahmen, die transparent sein müssen.
- **Interoperabilität:** Schnittstellen zu BIM, IFC, LCA, Ausschreibung und ERP sind entscheidend, aber nicht automatisch gegeben.
- **Marktverfügbarkeit:** Ein gutes Inventar garantiert noch keinen Abnehmer.
- **Regionale Regulierung:** BREEAM/GLA-Bezüge sind UK-spezifisch; Übertragung auf DACH erfordert Anpassung.

## Quellen

- Material Index, offizielle Website: https://www.material-index.co.uk/
- Material Index Platform: https://material-index.exchange/platform
- Material Index, Platform / Audits / Material Passports: https://www.material-index.co.uk/platform/our-platform
- Material Index, Audits und Datenfelder: https://material-index.co/subscribe
- Geovation, Material Index Startup-Profil: https://geovation.uk/startups/material-index/
- Wates, Roll-out Circular Economy Platform: https://www.wates.co.uk/news/sustainability-services/culture/we-pioneer-nationwide-rollout-of-circular-economy-platform/
- ASBP, Digital Platforms, Physical Hubs and Facilitators for Reuse: https://asbp.org.uk/article/reuse-digital-platforms-and-physical-hubs
