# Regelwerk Evidence — web-researched connections to the new vocabulary

**Date:** 2026-06-04
**Run:** `regulation_graph_vocab_2026_06_04`
**Method:** web research (WebSearch/WebFetch). Each `Regelwerk` node gets an official/authoritative `source_url`, jurisdiction (`GILT_IN_LAND`), the `Regulierungsfrage` it answers, the `Nachweisforderung` it backs, a `source_quote`, and a confidence.

`evidence_status`: `rule_documented` = the regulation text/official page documents the requirement; `comparative_only` = relevant but outside the project's jurisdiction.

---

## Regelwerk nodes (evidence-backed)

### rw_din_spec_91484 — DIN SPEC 91484
- **Name:** "Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des Anschlussnutzungspotentials vor Abbruch- und Renovierungsarbeiten" (pre-demolition audit), publ. 2023-09.
- **GILT_IN_LAND:** land_deutschland (DACH-relevant, comparative elsewhere)
- **Regulierungsfrage:** rf_reusedokumentationfrage, rf_rueckbau_und_bauteilernte_frage
- **Nachweisforderung:** nf_bauteilidentifikation, nf_herkunfts_und_rueckbaudokumentation, nf_zustands_und_massaufnahme
- **source_quote:** "DIN SPEC 91484 beschreibt das Verfahren, bei dem Bauprodukte hinsichtlich ihres Potentials zur Anschlussnutzung vor Abbruch- und Renovierungsarbeiten (Pre-Demolition-Audit) erfasst werden … Zunächst wird definiert, welche Informationen über die Bauprodukte erfasst werden müssen (Standort, Baujahr, Gebäudeklasse, Nutzungsart)."
- **source_url:** https://din.one/pages/viewpage.action?pageId=160465716
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_din_spec_91525 — DIN SPEC 91525
- **Name:** "Anschlussnutzungskonzept für Bauprodukte aus Bestandsgebäuden / Post-Use Concept (PUC)", publ. 2026-02.
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_reusedokumentationfrage, rf_rueckbau_und_bauteilernte_frage
- **Nachweisforderung:** nf_zustands_und_massaufnahme, nf_dauerhaftigkeit_restlebensdauer
- **source_quote:** "Die DIN SPEC 91525 … etabliert einheitliche, praxisnahe Kriterien für die wirtschaftliche, technische und ökologische Bewertung von Bauteilen für die Wiederverwendung … von der Bestimmung eines Anschlussnutzungspfades über die technische, wirtschaftliche und optionale ökologische Bewertung bis zur Rückbau- und Aufbereitungsplanung."
- **source_url:** https://www.dinmedia.de/en/technical-rule/din-spec-91525/397760893
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_vdi_6210 — VDI 6210 Blatt 1
- **Name:** "Abbruch von baulichen und technischen Anlagen"
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_rueckbau_und_bauteilernte_frage
- **Nachweisforderung:** nf_herkunfts_und_rueckbaudokumentation, nf_genehmigungs_oder_zustimmungsbedarf
- **source_quote:** "Die Richtlinie gilt sowohl für den vollständigen Rückbau baulicher und technischer Anlagen als auch für Abbrucharbeiten im Bestand (Sanierung, Erneuerung, Modernisierung) … beschreibt zudem Prozesse zu Gewinnung, Bereitstellung, Zwischenlagerung, Behandlung und Verbleib der anfallenden Stoffe."
- **source_url:** https://www.vdi.de/richtlinien/details/vdi-6210-blatt-1-abbruch-von-baulichen-und-technischen-anlagen
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_eu_cpr_2024_3110 — EU CPR (EU) 2024/3110
- **Name:** EU-Bauprodukteverordnung 2024/3110 (replaces 305/2011; in force 2025-01-07, binding 2026-01-08)
- **GILT_IN_LAND:** EU-wide (all project countries: DE, AT, BE, NL, FR, DK, etc.)
- **Regulierungsfrage:** rf_bauproduktstatus_frage, rf_reusedokumentationfrage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung, nf_herkunfts_und_rueckbaudokumentation
- **source_quote:** "Der erweiterte Anwendungsbereich umfasst nun auch gebrauchte Produkte … Unternehmen aus Rückbau, Refurbishment und Reuse sind als neue Wirtschaftsakteure betroffen. Der digitale Produktpass muss Informationen für Wiederverwendung und Refurbishment bereitstellen."
- **source_url:** https://www.ressource-deutschland.de/service/rechtlicher-rahmen-zur-ressourceneffizienz/eu-bauprodukte-verordnung-2024/3110/
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_trgs_519 — TRGS 519
- **Name:** "Asbest: Abbruch-, Sanierungs- oder Instandhaltungsarbeiten"
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_schadstoff_frage
- **Nachweisforderung:** nf_asbest_check
- **source_quote:** "TRGS 519 … Schutz der Beschäftigten bei Tätigkeiten mit Asbest … Vor jeder Tätigkeit mit asbesthaltigen Materialien fordert die TRGS 519 systematische Informationsermittlung und Gefährdungsbeurteilung … Tätigkeiten sind der zuständigen Behörde mindestens eine Woche vor Beginn anzuzeigen."
- **source_url:** https://www.baua.de/DE/Angebote/Regelwerk/TRGS/TRGS-519
- **evidence_status:** rule_documented · **confidence:** 0.95

### rw_trgs_521 — TRGS 521
- **Name:** "Abbruch-, Sanierungs- und Instandhaltungsarbeiten mit alter Mineralwolle (KMF)"
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_schadstoff_frage
- **Nachweisforderung:** nf_kmf_check
- **source_quote:** "Produkte aus KMF, die vor 1996 eingebaut wurden, sind nach TRGS 905 als 'krebserzeugend Kategorie 2' eingestuft und werden als 'alte Mineralwolle' bezeichnet … alte Mineralfasern dürfen nur im Rahmen von Abbruch-, Sanierungs- und Instandhaltungsarbeiten gehandhabt werden (Schwarz-Weiß-Bereiche, sorgfältige Entfernung und Verpackung)."
- **source_url:** https://www.baua.de/DE/Angebote/Regelwerk/TRGS/pdf/TRGS-521.pdf
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_gefstoffv — GefStoffV (Gefahrstoffverordnung, Novelle 2024)
- **Name:** Gefahrstoffverordnung, in Kraft 2024-12-05 (risk-based concept for asbestos in existing buildings)
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_schadstoff_frage
- **Nachweisforderung:** nf_asbest_check, nf_schadstoffpruefung
- **source_quote:** "In allen Gebäuden, die vor dem 31.10.1993 errichtet wurden, muss mit Asbest gerechnet werden … Informationspflicht: Eigentümer müssen vor Beginn von Bau-, Instandhaltungs- oder Rückbauarbeiten alle verfügbaren Informationen über das Vorhandensein gefährlicher Stoffe wie Asbest bereitstellen … risikobezogenes Maßnahmenkonzept mit drei Risikobereichen."
- **source_url:** https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_reach_annex_xvii — REACH (EG) 1907/2006, Anhang XVII Eintrag 77
- **Name:** REACH-Verordnung, Formaldehyd-Beschränkung (Reg. (EU) 2023/1464), greift 2026-08-06
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_schadstoff_frage
- **Nachweisforderung:** nf_formaldehyd_oder_emissionsnachweis, nf_schwermetall_oder_bleifarbe_check
- **source_quote:** "Ab dem 6. August 2026 dürfen bestimmte Artikel und Möbel auf Basis von Holzwerkstoffen nicht mehr in Verkehr gebracht werden, wenn sie einen Formaldehyd-Grenzwert von 0,062 mg/m³ in der Innenraumluft überschreiten … für andere Artikel wie Bauprodukte gilt 0,080 mg/m³."
- **source_url:** https://www.reach-clp-biozid-helpdesk.de/SharedDocs/Meldungen/DE/REACH/2023-07-20-Beschr%C3%A4nkung_Formaldehyd_Abspalter
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_pop_2019_1021 — POP-Verordnung (EU) 2019/1021
- **Name:** Verordnung über persistente organische Schadstoffe (POP), in Kraft 2019-07-15
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_schadstoff_frage
- **Nachweisforderung:** nf_pcb_check, nf_pak_check
- **source_quote:** "Die POP-Verordnung legt detaillierte Anforderungen an Herstellung, Inverkehrbringen, Verwendung und Freisetzung persistenter organischer Schadstoffe fest … Beispiele sind PCB (polychlorierte Biphenyle), Dioxine und Furane … Bestimmungen für die Entsorgung von Abfällen, die solche Stoffe enthalten."
- **source_url:** https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=LEGISSUM:4406078
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_krwg — KrWG §6 / §7 / §8 (Kreislaufwirtschaftsgesetz)
- **Name:** Kreislaufwirtschaftsgesetz — Abfallhierarchie (§6) & Verwertungspflicht (§7/§8)
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_reusedokumentationfrage, rf_rueckbau_und_bauteilernte_frage
- **Nachweisforderung:** nf_herkunfts_und_rueckbaudokumentation
- **source_quote:** "Die fünfstufige Abfallhierarchie (§6): Vermeidung, Vorbereitung zur Wiederverwendung, Recycling, sonstige (energetische) Verwertung, Beseitigung … 'Vorbereitung zur Wiederverwendung' ist jedes Verwertungsverfahren der Prüfung, Reinigung oder Reparatur, bei dem Erzeugnisse oder Bauteile so vorbereitet werden, dass sie ohne weitere Vorbehandlung wieder für denselben Zweck verwendet werden können."
- **source_url:** https://www.gesetze-im-internet.de/krwg/__6.html
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_cen_ts_1090_201 — CEN/TS 1090-201:2024
- **Name:** "Execution of steel structures and aluminium structures — Reuse of structural steel" (publ. 2024-10)
- **GILT_IN_LAND:** EU-wide (CEN members)
- **Regulierungsfrage:** rf_tragwerkssicherheit_frage, rf_bauproduktstatus_frage
- **Nachweisforderung:** nf_standsicherheitsnachweis, nf_materialpruefung, nf_befestigungsnachweis (weldability), nf_produktstatus_und_leistungserklaerung
- **source_quote:** "CEN/TS 1090-201 specifies requirements for the reusability assessment of reclaimed structural components and the declaration of mechanical and geometrical properties as well as weldability … properties to be declared: strength (yield and tensile); elongation; tolerances on dimensions and shape; heat treatment delivery conditions; weldability."
- **source_url:** https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_sci_p427 — SCI P427
- **Name:** "Structural Steel Reuse: assessment, testing and design principles" (Steel Construction Institute, UK)
- **GILT_IN_LAND:** land_vereinigtes_koenigreich (comparative elsewhere)
- **Regulierungsfrage:** rf_tragwerkssicherheit_frage, rf_bauproduktstatus_frage
- **Nachweisforderung:** nf_materialpruefung, nf_standsicherheitsnachweis, nf_produktstatus_und_leistungserklaerung
- **source_quote:** "Given appropriate determination of material characteristics and tolerances, (re)fabricated reclaimed steelwork can be fabricated and CE marked in accordance with BS EN 1090 … NDT is appropriate for components with documented provenance, whereas destructive testing (tensile and spectroscopic) is often necessary for legacy or undocumented steel, particularly steel produced prior to the 1970s."
- **source_url:** https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_sia_269 — SIA 269 (Normenreihe)
- **Name:** "Erhaltung von Tragwerken" (Grundlagen + 269/1…/8 für Beton-, Stahl-, Holzbau)
- **GILT_IN_LAND:** land_schweiz
- **Regulierungsfrage:** rf_tragwerkssicherheit_frage
- **Nachweisforderung:** nf_standsicherheitsnachweis, nf_zustands_und_massaufnahme, nf_dauerhaftigkeit_restlebensdauer
- **source_quote:** "Die Norm SIA 269 liefert die Grundsätze und die Vorgehensweise bei der Behandlung bestehender Tragwerke … Bestimmte Aspekte bestehender Tragwerke werden gemäss einem risikobasierten Verfahren behandelt … erlaubt es, Kosten und Nutzen bei Erhaltungsmassnahmen zu berücksichtigen."
- **source_url:** https://www.espazium.ch/de/aktuelles/die-neue-norm-sia-2698
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_eurocodes_en_1990_1999 — Eurocodes EN/DIN EN 1990–1999
- **Name:** Eurocode basis + actions + material codes (EN 1990 basis, 1991 actions, 1992 concrete, 1993 steel, 1995 timber, 1996 masonry…)
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_tragwerkssicherheit_frage
- **Nachweisforderung:** nf_standsicherheitsnachweis
- **source_quote:** "The principles of EN 1990 are applicable for the structural appraisal of existing constructions, the design of repairs and alterations, and the assessment of changes in use … The forthcoming Second Generation Eurocodes promise new provisions for sustainability and the assessment of existing structures."
- **source_url:** https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-basis-structural-design
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_en_1090 — EN/DIN EN 1090
- **Name:** "Ausführung von Stahltragwerken und Aluminiumtragwerken" (EN 1090-1 conformity/CE, EN 1090-2 execution)
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_bauproduktstatus_frage, rf_tragwerkssicherheit_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung, nf_befestigungsnachweis
- **source_quote:** "Seit dem 1. Juli 2014 verlangt die EU-BauPVO, dass tragende Stahl-/Aluminiumbauteile als Bauprodukte ausschließlich mit CE-Kennzeichnung nach DIN EN 1090-1 in Verkehr gebracht werden … die werkseigene Produktionskontrolle (WPK) ist ein zentraler Bestandteil nach EN 1090-1." (Reuse path: reclaimed steel re-fabricated and CE/UKCA marked per CEN/TS 1090-201.)
- **source_url:** https://bauforumstahl.de/wp-content/uploads/2024/02/bfs-CE-Kennzeichnung_nach_EN-1090.pdf
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_dibt_zie_abz — DIBt ZiE / vBG / abZ / aBG
- **Name:** Deutsches Regelungssystem für nicht (CE-)geregelte Bauprodukte/Bauarten — Verwendbarkeits-/Anwendbarkeitsnachweise
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_bauproduktstatus_frage, rf_genehmigungs_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung, nf_genehmigungs_oder_zustimmungsbedarf
- **source_quote:** "Eine Zustimmung im Einzelfall (ZiE) ist ein Verwendbarkeitsnachweis für Bauprodukte … bezieht sich nur auf ein einziges Bauvorhaben; soll das Produkt erneut verwendet werden, ist ein neuer Antrag zu stellen. Vorhandene Prüfergebnisse und Nachweise können anerkannt werden, wenn sie weiterhin dem Stand der Technik entsprechen … Bei absehbarer Mehrfachverwendung wird eine abZ/aBG empfohlen."
- **source_url:** https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg
- **evidence_status:** rule_documented · **confidence:** 0.9 *(directly addresses reuse of building products)*

### rw_din_en_13501 — DIN EN 13501
- **Name:** "Klassifizierung von Bauprodukten und Bauarten zu ihrem Brandverhalten" (Euroklassen A1–F + s/d/fl)
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_brandschutz_frage
- **Nachweisforderung:** nf_brandschutznachweis
- **source_quote:** "DIN EN 13501-1 regelt die Klassifizierung von Baustoffen nach ihrer Entflammbarkeit … sieben Euroklassen A1, A2, B, C, D, E und F, zusätzlich Rauchentwicklung (s1–s3) und brennendes Abtropfen (d0–d2)."
- **source_url:** https://www.baunetzwissen.de/daemmstoffe/fachwissen/normen/din-en-13501-klassifizierung-von-bauprodukten-und-bauarten-zu-ihrem-brandverhalten-1005853
- **evidence_status:** rule_documented · **confidence:** 0.9

### rw_din_4102 — DIN 4102 / 4108 / 4109
- **Name:** Nationale Normen: DIN 4102 (Brandverhalten), DIN 4108 (Wärmeschutz), DIN 4109 (Schallschutz)
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_brandschutz_frage, rf_bauphysik_frage
- **Nachweisforderung:** nf_brandschutznachweis, nf_bauphysiknachweis
- **source_quote:** "Die Baustoffklassen nach DIN 4102 und die europäische DIN EN 13501-1 sind nicht direkt ineinander überführbar, beide Normen werden in Deutschland weiterhin verwendet." (DIN 4108 Wärmeschutz / DIN 4109 Schallschutz liefern die Bauphysik-Nachweisgrundlage.)
- **source_url:** https://www.feuertrutz.de/brandschutzklassen-nach-din-4102-und-en-13501-1-26072017
- **evidence_status:** rule_documented · **confidence:** 0.8

### rw_mbo_lbo — MBO / LBO
- **Name:** Musterbauordnung (MBO) und Landesbauordnungen (LBO)
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_genehmigungs_frage, rf_bauproduktstatus_frage
- **Nachweisforderung:** nf_genehmigungs_oder_zustimmungsbedarf, nf_produktstatus_und_leistungserklaerung
- **source_quote:** "Verwendbarkeitsnachweise sind in den Landesbauordnungen vorgeschriebene Kennzeichnungen für nicht geregelte Bauprodukte … Die LBOs setzen die Anforderungen der MBO auf Landesebene um und haben bindenden Charakter."
- **source_url:** https://www.dgwz.de/gesetze/musterbauordnung-mbo-landesbauordnung-lbo
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_mvv_tb — MVV TB / VV TB
- **Name:** Muster-Verwaltungsvorschrift Technische Baubestimmungen (DIBt), version 2025/1
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_bauproduktstatus_frage, rf_tragwerkssicherheit_frage, rf_brandschutz_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung
- **source_quote:** "Teil C enthält Regelungen für die Verwendung von Bauprodukten, die kein CE-Zeichen nach der Bauproduktenverordnung tragen … Die Technischen Baubestimmungen konkretisieren die Anforderungen an bauliche Anlagen durch Verweise auf Normen und andere technische Regeln."
- **source_url:** https://www.dibt.de/de/wir-bieten/technische-baubestimmungen
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_geg — GEG (Gebäudeenergiegesetz)
- **Name:** Gebäudeenergiegesetz — energetische Anforderungen an Bestand und Neubau
- **GILT_IN_LAND:** land_deutschland
- **Regulierungsfrage:** rf_bauphysik_frage
- **Nachweisforderung:** nf_u_wert_oder_energie_info, nf_bauphysiknachweis
- **source_quote:** "Für jedes Bauteil gelten verbindliche Sanierungsstandards, geregelt über den U-Wert … bei Sanierung der Außenwände oder des Dachs U-Wert 0,24, bei Fenstern max. 1,3 … Nachweis durch Sachverständigen für Wärmeschutz bzw. Unternehmererklärung, Bescheinigung 10 Jahre aufbewahren."
- **source_url:** https://www.gebaeudeforum.de/ordnungsrecht/geg/
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_sia_380_1 — SIA 380/1
- **Name:** "Heizwärmebedarf / Thermische Energie im Hochbau" (CH energy)
- **GILT_IN_LAND:** land_schweiz
- **Regulierungsfrage:** rf_bauphysik_frage
- **Nachweisforderung:** nf_u_wert_oder_energie_info, nf_bauphysiknachweis
- **source_quote:** "SIA 380/1 … verbindliche technische Anforderungen an die Gebäudehülle … gilt für alle beheizten oder gekühlten Gebäude und unterscheidet zwischen Anforderungen für Neubauten und für Umbauten/Sanierungen … Berechnung nach Monatsbilanzverfahren gemäß EN 13790."
- **source_url:** https://shop.sia.ch/normenwerk/architekt/380-1_2016_d/D/Product
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_oib_richtlinien — OIB-Richtlinien
- **Name:** OIB-Richtlinien 1–6 (AT; RL 2 Brandschutz, RL 6 Energieeinsparung)
- **GILT_IN_LAND:** land_oesterreich
- **Regulierungsfrage:** rf_brandschutz_frage, rf_genehmigungs_frage, rf_bauphysik_frage
- **Nachweisforderung:** nf_brandschutznachweis, nf_genehmigungs_oder_zustimmungsbedarf
- **source_quote:** "Die OIB-Richtlinien orientieren sich an den Grundanforderungen der EU-BauPVO … OIB-Richtlinie 2 (Brandschutz) definiert Mindestanforderungen an Feuerwiderstand, Fluchtwege … Anforderungen an das Brandverhalten von Baustoffen nach den europäischen Klassen."
- **source_url:** https://www.oib.or.at/kernaufgaben/oib-richtlinien/
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_nl_bbl — Dutch Bbl (Besluit bouwwerken leefomgeving)
- **Name:** NL Building Decree (Bbl), in force 2024-01-01 — incl. explicit reuse provision
- **GILT_IN_LAND:** land_niederlande
- **Regulierungsfrage:** rf_reusedokumentationfrage, rf_bauproduktstatus_frage, rf_genehmigungs_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung, nf_genehmigungs_oder_zustimmungsbedarf
- **source_quote:** "Article 4.166 of the Bbl facilitates 1-to-1 reuse of building products without quality loss, allowing building products and materials to be directly redeployed in new construction works without loss of quality or function … rules over construction, demolition activity and mobile crushing of construction and demolition waste."
- **source_url:** https://climate-laws.org/document/the-environment-buildings-decree-of-the-netherlands-besluit-bouwwerken-leefomgeving-bbl_1057
- **evidence_status:** rule_documented · **confidence:** 0.9 *(explicit reuse article)*

### rw_be_tracimat_regional — Belgian regional building rules (Tracimat / sloopopvolging)
- **Name:** Flemish demolition-management (Tracimat sloopopvolgingsplan); separate Wallonia/Brussels rules
- **GILT_IN_LAND:** land_belgien
- **Regulierungsfrage:** rf_rueckbau_und_bauteilernte_frage, rf_reusedokumentationfrage
- **Nachweisforderung:** nf_herkunfts_und_rueckbaudokumentation, nf_bauteilidentifikation
- **source_quote:** "Tracimat is currently the only recognised demolition management organisation in the Flemish Region. Demolition monitoring plans can be compiled according to Tracimat, in order to … have [materials] processed into secondary raw materials. The obligation to draw up a demolition follow-up plan only applies in the Flemish Region, with separate rules for Wallonia and Brussels."
- **source_url:** https://vito.be/en/news/demolition-guide-recognizes-building-materials-recycling-or-reuse
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_ukca_ce — UKCA / CE marking
- **Name:** UKCA product marking for construction products (GB), CE recognition transitional
- **GILT_IN_LAND:** land_vereinigtes_koenigreich
- **Regulierungsfrage:** rf_bauproduktstatus_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung
- **source_quote:** "Components or fabricated structures that have been recovered or recycled from sites can be reused on future sites or sold providing they meet the standards laid down in BS EN 1090 provided they are not altered in any way … CE/UKCA marking does not apply retrospectively. Salvaged steel will need to be UKCA marked by the steel fabricator."
- **source_url:** https://www.ssqgroup.com/ukca-marking-to-replace-ce-marking-on-construction-products
- **evidence_status:** rule_documented · **confidence:** 0.85

### rw_eu_cpr_305_2011 — EU CPR 305/2011 *(predecessor, bridge node)*
- **Name:** EU-Bauprodukteverordnung 305/2011 (replaced by 2024/3110; relevant for projects/products pre-2026)
- **GILT_IN_LAND:** EU-wide
- **Regulierungsfrage:** rf_bauproduktstatus_frage
- **Nachweisforderung:** nf_produktstatus_und_leistungserklaerung
- **source_quote:** "For construction products bearing CE marking according to the Construction Products Regulation (Regulation (EU) No. 305/2011), no national usability proofs are issued." (Note: 305/2011 had no dedicated reuse path; see rw_eu_cpr_2024_3110.)
- **source_url:** https://www.maschinenrichtlinie.de/mbt-leitfaden/eu-binnenmarkt/eu-produktvorschriften/bauprodukte-verordnung-eu-nr-305/2011-/-eu-nr-2024/3110/
- **evidence_status:** rule_documented · **confidence:** 0.8

---

## Round-2 research — 15 additional Regelwerke

Full `source_quote` per rule lives in `build_vocabulary_graph.py` (`REGELWERK` list) and is
carried onto every edge in `vocab_edges.csv`. Summary:

| Regelwerk node | Name | Land | Regulierungsfrage | Nachweisforderung | source_url |
|---|---|---|---|---|---|
| `rw_din_68800_altholzv` | DIN 68800 / AltholzV | DE | Schadstoff | HolzschutzmittelCheck | [gesetze-im-internet](https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html) |
| `rw_din_18008` | DIN 18008-4 (Absturzsich. Verglasung) | DE | Tragwerk | SicherheitsglasInfo | [baunormenlexikon](https://www.baunormenlexikon.de/norm/din-18008-4/e87129e6-4c53-4386-852c-b6fd49626b0d) |
| `rw_dguv_v3_vde` | DGUV V3 / DIN VDE 0100-600 / 0105-100 | DE | HygieneElektroFunktion | Elektrosicherheitsnachweis | [elektrofachkraft](https://www.elektrofachkraft.de/pruefung/elektrotechnische-erstpruefung-wiederholungspruefung) |
| `rw_vdi_6023_6022` | VDI 6023 / VDI 6022 (Hygiene) | DE | HygieneElektroFunktion | HygieneUndReinigungsnachweis | [vdi.de](https://www.vdi.de/mitgliedschaft/vdi-richtlinien/unsere-richtlinien-highlights/vdi-6023) |
| `rw_prodhaftg_bgb` | ProdHaftG / BGB §823 | DE | HaftungGewaehrleistung | Herkunftsdok. / Produktstatus | [Produkthaftung (Wikipedia)](https://de.wikipedia.org/wiki/Produkthaftung_(Deutschland)) |
| `rw_vdi_6202` | VDI/GVSS 6202 Blatt 1 | DE | Schadstoff | Schadstoffpruefung / -kataster | [vdi.de](https://www.vdi.de/richtlinie/vdigvss_6202_blatt_1-schadstoffbelastete_bauliche_und_technische_anlagen_abbruch_sanierungs_und/) |
| `rw_ebv` | Ersatzbaustoffverordnung | DE | Umweltvertr./Oekobilanz, Schadstoff | MineralischeErsatzbaustoffGuete | [gesetze-im-internet](https://www.gesetze-im-internet.de/ersatzbaustoffv/) |
| `rw_dafstb_rc_beton` | DAfStb-Richtlinie R-Beton | DE | Tragwerk, Umweltvertr. | RcGesteinskoernungEignung / Materialpruefung | [dinmedia](https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550) |
| `rw_en_15804_15978` | EN 15804 / EN 15978 (EPD/LCA, Modul D) | EU | Umweltvertr./Oekobilanz | OekobilanzEPD | [gebaeudeforum](https://www.gebaeudeforum.de/wissen/nachhaltiges-bauen-und-sanieren/lebenszyklusbetrachtung/oekobilanzierung-lca/) |
| `rw_madaster_grp` | Madaster / Gebäuderessourcenpass | DE, NL | Reusedok., Umweltvertr. | MaterialpassRessourcenpass / Bauteilident. | [DGNB](https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport) |
| `rw_nta_8713` | NTA 8713 (Reuse of structural steel) | NL | Tragwerk, Bauproduktstatus | Standsicherheit / Materialpr. / Produktstatus | [nen.nl](https://www.nen.nl/nta-8713-2023-nl-307691) · **↔ live `bps_nta_8713`** |
| `rw_oenorm_b3151` | ÖNORM B 3151 (Rückbau) | AT | Rückbau, Schadstoff | Herkunftsdok. / Schadstoffkataster | [bmluk.gv.at PDF](https://www.bmluk.gv.at/dam/jcr:b5c6f981-a044-4979-9dd5-76da4bb69477/OeNORM_B3151_2014.pdf) · **↔ actor `baukarussell`** |
| `rw_sia_2032` | SIA 2032 (Graue Energie) | CH | Umweltvertr./Oekobilanz | OekobilanzEPD | [espazium](https://www.espazium.ch/de/aktuelles/graue-energie-oekobilanzierung-fuer-die-erstellung-von-gebaeuden) |
| `rw_fcrbe_reuse_toolkit` | FCRBE Reuse Toolkit / Reclamation Audit | BE, FR, UK, NL | Reusedok., Rückbau | Bauteilident. / Herkunftsdok. | [opalis.eu](https://opalis.eu/en/documentation) · **↔ actors `rotordc`/`salvoweb`/`bellastock`** |
| `rw_qng_dgnb` | QNG / DGNB Zertifizierung | DE | Umweltvertr./Oekobilanz, Reusedok. | OekobilanzEPD / Materialpass | [nachhaltigesbauen.de](https://www.nachhaltigesbauen.de/austausch/beg/) |

### Domains closed in round 2
The previously empty Nachweis/Frage domains are now evidence-backed:
**HolzschutzmittelCheck** (DIN 68800/AltholzV), **SicherheitsglasInfo** (DIN 18008-4),
**Elektrosicherheitsnachweis** (DGUV V3 / VDE 0100-600), **HygieneUndReinigungsnachweis**
(VDI 6023/6022), **HaftungGewaehrleistungFrage** (ProdHaftG — incl. the *Quasi-Hersteller*
rule, directly relevant to reselling reclaimed products). New extension nodes added for
LCA/EPD (Modul D), material passports, recycled-aggregate and mineral-substitute proof.

### Live-graph wiring bonuses (for the anchor-mapping phase)
- `rw_nta_8713` ↔ existing `:Bauproduktstatus {id:'bps_nta_8713'}`
- `rw_oenorm_b3151` explicitly names live actor `baukarussell`
- `rw_fcrbe_reuse_toolkit` partners = live actors `rotordc`, `salvoweb`, `bellastock`

---

## Round-3 research — 15 additional Regelwerke (country mandates + EU frameworks)

| Regelwerk node | Name | Land | Regulierungsfrage | Nachweisforderung | source_url |
|---|---|---|---|---|---|
| `rw_fr_pemd` | France Diagnostic PEMD (loi AGEC) | FR | Rückbau, Reusedok. | Bauteilident. / Herkunftsdok. / Schadstoffkataster | [ecologie.gouv.fr](https://www.ecologie.gouv.fr/politiques-publiques/diagnostic-produits-equipements-materiaux-dechets-pemd) |
| `rw_fr_rep_pmcb` | France REP PMCB | FR | Rückbau, Haftung | Herkunftsdok. | [ecologie.gouv.fr](https://www.ecologie.gouv.fr/politiques-publiques/produits-materiaux-construction-du-secteur-du-batiment-pmcb) |
| `rw_dk_br18` | Denmark BR18 | DK | Bauproduktstatus, Brandschutz, Umweltvertr. | Produktstatus / Brandschutz / OekobilanzEPD | [sbst.dk PDF](https://www.sbst.dk/Media/638442760533494160/Barrierer%20og%20muligheder%20for%20biogene%20og%20genbrugte%20byggematerialer%20i%20BR18.pdf) |
| `rw_no_tek17` | Norway TEK17 (ombrukskartlegging) | NO | Bauproduktstatus, Rückbau | Produktstatus / Bauteilident. / Herkunftsdok. | [dibk.no §9-5](https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-5) |
| `rw_eu_wfd_2008_98` | EU Waste Framework Directive 2008/98/EC | EU | Rückbau, Reusedok. | Herkunftsdok. | [eur-lex](https://eur-lex.europa.eu/legal-content/EN/LSU/?uri=CELEX:32008L0098) |
| `rw_trgs_524` | TRGS 524 (kontaminierte Bereiche) | DE | Schadstoff | Schadstoffkataster / -prüfung | [baua](https://www.baua.de/DE/Angebote/Regelwerk/TRGS/TRGS-524) |
| `rw_pcb_richtlinie` | PCB-Richtlinie (ARGEBAU) | DE | Schadstoff | PCBCheck | [gewerbeaufsicht BW PDF](https://gewerbeaufsicht.baden-wuerttemberg.de/documents/20121/49165/6_1.pdf) |
| `rw_din_4074_en_14081` | DIN 4074 / EN 14081 (Holzsortierung) | EU | Tragwerk | Standsicherheit / Materialpr. / Produktstatus | [holzbau-deutschland PDF](https://www.holzbau-deutschland.de/fileadmin/user_upload/eingebundene_Downloads/2022-12_Information_Sortierung_durch_den_Zimmermeister_01.pdf) |
| `rw_en_771_reclaimed` | EN 771 (reclaimed masonry units) | EU | Tragwerk, Bauproduktstatus | Materialpr. / Produktstatus | [reclaimedbrickcompany](https://reclaimedbrickcompany.co.uk/blogs/yard-display/reclaimed-brick-company-becomes-first-uk-supplier-to-achieve-bs-en-771-1-testing-for-reclaimed-bricks) |
| `rw_en_1992_4` | EN 1992-4 (Befestigungen in Beton) | EU | Tragwerk | Befestigungsnachweis | [fastenerandfixing](https://fastenerandfixing.com/construction-fixings/design-of-fastenings-for-use-in-concrete-en-1992-4-publication-and-the-implication-for-anchor-manufacturers-and-consumers/) |
| `rw_eu_taxonomy` | EU Taxonomy (Circular Economy TSC) | EU | Umweltvertr., Reusedok. | OekobilanzEPD | [ec.europa.eu PDF](https://finance.ec.europa.eu/system/files/2023-06/taxonomy-regulation-delegated-act-2022-environmental_en_0.pdf) · **↔ live `rb_eu_taxonomie`** |
| `rw_eu_levels` | EU Level(s) framework | EU | Umweltvertr. | OekobilanzEPD / Materialpass | [JRC PDF](https://susproc.jrc.ec.europa.eu/product-bureau/sites/default/files/2021-01/UM1_Introduction_to_Level(s)_v1.1_27pp.pdf) |
| `rw_espr_dpp` | ESPR / Digital Product Passport | EU | Bauproduktstatus, Umweltvertr. | Materialpass / Produktstatus | [ec.europa.eu](https://green-forum.ec.europa.eu/implementing-ecodesign-sustainable-products-regulation_en) |
| `rw_strlschg_radon` | StrlSchG (Radon) | DE | Schadstoff | Radonmessung / Schadstoffprüfung | [bfs.de](https://www.bfs.de/DE/themen/ion/umwelt/radon/regelungen/referenzwert.html) · **↔ live `s_radon`** |
| `rw_fib_precast_reuse` | fib Bulletins (precast concrete reuse) | EU | Tragwerk | Standsicherheit / Materialpr. | [fib-international](https://www.fib-international.org/publications/fib-bulletins/special-design-considerations-for-precast-prestress-pdf-detail.html) |

### Cross-jurisdiction pattern found: mandatory pre-demolition reuse audit
A coherent cluster of laws now requires a reuse/pollutant audit *before* demolition — strong
anchors for connecting `Projekt`/`Bauwerk` by country:
**FR** `rw_fr_pemd` (>1000 m², since 2023-07) · **AT** `rw_oenorm_b3151` (all demolition, since 2016; Schadstofferkundung >750 t) ·
**NO** `rw_no_tek17` (>100 m² / >10 t, since 2023-07) · **BE** `rw_be_tracimat_regional` (Flanders) ·
**DE** `rw_din_spec_91484` (voluntary pre-demolition audit).

### Two more live-graph links (round 3)
- `rw_eu_taxonomy` ↔ existing `:RechtlicheBedingung {id:'rb_eu_taxonomie'}`
- `rw_strlschg_radon` ↔ existing `:Schadstoff {id:'s_radon'}`

---

## Round-4 research — 9 Regelwerke (design-for-disassembly, material-specific, country codes)

| Regelwerk node | Name | Land | Regulierungsfrage | Nachweisforderung | Material | source_url |
|---|---|---|---|---|---|---|
| `rw_iso_20887` | ISO 20887 (DfD/DfA) | EU | Rückbau, Reusedok. | Herkunftsdok. | — | [iso.org](https://www.iso.org/standard/69370.html) |
| `rw_en_1090_2_bolts_reuse` | EN 1090-2 / EN 14399 (bolt reuse limits) | EU | Tragwerk, Bauproduktstatus | Befestigung / Materialpr. | mat_stahl | [steelconstruction.info](https://www.steelconstruction.info/Preloaded_bolting) |
| `rw_glas_reuse_igu` | Flat-glass / IGU reuse guidance | EU | Bauphysik, Bauproduktstatus | U-Wert / Sicherheitsglas / Materialpr. | mat_glas | [glassonweb](https://www.glassonweb.com/article/reuse-and-remanufacturing-insulated-glass-units) |
| `rw_naturstein_reuse` | Naturstein-Wiederverwendung | EU | Reusedok., Tragwerk | Dauerhaftigkeit / Materialpr. | mat_naturstein | [zukunftnaturstein.de](https://zukunftnaturstein.de/wiederverwendbarkeit-von-naturstein/) |
| `rw_nen_8700` | NEN 8700-serie (bestaande bouw) | NL | Tragwerk | Standsicherheit / Zustandsaufnahme | — | [nen.nl](https://www.nen.nl/bouw/constructieve-veiligheid/constructieve-veiligheid-bestaande-bouw) · **↔ live `norm_nen_8700`** |
| `rw_vkf_bsv` | VKF Brandschutzvorschriften | CH | Brandschutz | Brandschutznachweis | — | [bsvonline.ch](https://www.bsvonline.ch/de) |
| `rw_uk_adb` | UK Approved Document B | UK | Brandschutz, Tragwerk | Brandschutznachweis | — | [planningportal](https://www.planningportal.co.uk/applications/building-control-applications/building-control/approved-documents/part-b-fire-safety/) |
| `rw_sia_269_2` | SIA 269/2 (Erhaltung Betonbau) | CH | Tragwerk | Standsicherheit / Materialpr. / Zustandsaufnahme | mat_beton, mat_stahlbeton | [cms.sia.ch](https://cms.sia.ch/de/api/getMedia/715) |
| `rw_istructe_reuse` | IStructE reuse guidance / reuse hierarchy | UK | Tragwerk, Reusedok. | Standsicherheit / Zustandsaufnahme | — | [istructe.org](https://www.istructe.org/resources/guidance/circular-economy/) |

### New edge type: `BETRIFFT_MATERIAL` (19 edges)
Round 4 adds rule-level Material relevance, connecting Regelwerke straight to the closed-set
`mat_*` anchors in `mit-bestand` (e.g. `rw_dafstb_rc_beton`→`mat_recyclingbeton`,
`rw_cen_ts_1090_201`/`rw_nta_8713`/`rw_sci_p427`→`mat_stahl`, `rw_en_771_reclaimed`→`mat_ziegel`,
`rw_din_4074_en_14081`→`mat_holz`, `rw_glas_reuse_igu`→`mat_glas`, `rw_naturstein_reuse`→`mat_naturstein`).

### Notable reuse-specific facts captured
- **What may NOT be reused:** EN 1090-2 prohibits reuse of fully-tightened preloaded HV/HR bolts (`rw_en_1090_2_bolts_reuse`).
- **Design-for-disassembly** is now an explicit standard (`rw_iso_20887`) — the upstream lever that makes later reuse possible.
- **6th live-graph link:** `rw_nen_8700` ↔ existing `:Norm {id:'norm_nen_8700'}`.

---

## Round-5 research — 10 Regelwerke (emissions/microbial, waste law, test methods, contract, accessibility)

| Regelwerk node | Name | Land | Regulierungsfrage | Nachweisforderung | Material | source_url |
|---|---|---|---|---|---|---|
| `rw_agbb_voc` | AgBB-Schema / DIN EN 16516 (VOC) | DE | Schadstoff | VOC-Emission / Formaldehyd | — | [umweltbundesamt PDF](https://www.umweltbundesamt.de/system/files/medien/4031/dokumente/agbb_bewertungsschema_2024.pdf) |
| `rw_vdi_3492` | VDI 3492 (Faser-/Asbestmessung REM/EDXA) | DE | Schadstoff | AsbestCheck / KMFCheck | — | [vdi.de](https://www.vdi.de/richtlinien/details/vdi-3492-messen-von-innenraumluftverunreinigungen-messen-von-immissionen-messen-anorganischer-faserfoermiger-partikel-rasterelektronenmikroskopisches-verfahren) |
| `rw_uba_schimmelleitfaden` | UBA-Schimmelleitfaden | DE | Schadstoff | MikrobielleBelastungCheck | — | [umweltbundesamt](https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/schimmel/aktueller-uba-schimmelleitfaden) · **↔ live `s_schimmel`** |
| `rw_gewabfv` | Gewerbeabfallverordnung (§8) | DE | Rückbau | Herkunftsdok. | — | [gesetze-im-internet](https://www.gesetze-im-internet.de/gewabfv_2017/BJNR089600017.html) |
| `rw_eu_cdw_protocol` | EU C&D Waste Management Protocol (2024) | EU | Rückbau, Reusedok., Schadstoff | Bauteilident. / Herkunftsdok. / Schadstoffkataster | — | [op.europa.eu](https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en) |
| `rw_en_13791_12504` | EN 13791 / EN 12504 (In-situ Beton) | EU | Tragwerk | Materialpr. / Standsicherheit | mat_beton, mat_stahlbeton | [iteh.ai](https://standards.iteh.ai/catalog/standards/cen/3209bcc7-df9a-4eb2-904d-e690e79b7452/en-13791-2019) |
| `rw_en_iso_6892` | EN ISO 6892-1 (Zugversuch Metalle) | EU | Tragwerk | Materialpr. | mat_stahl | [iso.org](https://www.iso.org/standard/78322.html) |
| `rw_vob_c_din_18459` | VOB/C ATV DIN 18459 (Abbruch/Rückbau) | DE | Rückbau, Haftung | Herkunftsdok. / Schadstoffkataster | — | [deutscher-abbruchverband](https://www.deutscher-abbruchverband.de/publikationen/handlungshilfen-downloads/atv-din-18459/) |
| `rw_en_408` | EN 408 (Holz mechanische Eigenschaften) | EU | Tragwerk | Materialpr. / Standsicherheit | mat_holz | [dinmedia](https://www.dinmedia.de/en/standard/din-en-408/126881788) |
| `rw_din_18040` | DIN 18040 (Barrierefreies Bauen) | DE | HygieneElektroFunktion | BarrierefreiheitNachweis | — | [baunormenlexikon](https://www.baunormenlexikon.de/norm/din-18040-1/c099c3ee-ecd0-48ed-9d9d-ec0f84970d53) |

### The audit cascade is now complete (EU → national)
`rw_eu_cdw_protocol` (EU pre-demolition audit guidelines) is the umbrella above the national
mandates already captured: **FR** PEMD · **AT** ÖNORM B 3151 · **NO** TEK17 · **BE** Tracimat ·
plus DE's `rw_din_spec_91484` + `rw_gewabfv` (separation/documentation). The new vocabulary now
spans the full chain *EU directive → national waste/audit law → assessment standard → test method*.

### Test methods now back the structural Nachweise
`nf_materialpruefung` / `nf_standsicherheitsnachweis` are now grounded in the concrete procedures:
EN 13791/12504 (concrete cores/rebound), EN ISO 6892-1 (steel tensile), EN 408 (timber) — the
exact tests that SCI P427 / NTA 8713 / CEN-TS 1090-201 call for on reclaimed material.

### 7th live-graph link
- `rw_uba_schimmelleitfaden` ↔ existing `:Schadstoff {id:'s_schimmel'}`

---

## Round-6 research — 4 Regelwerke (national carbon/energy/Ökobilanz, non-DE coverage)

| Regelwerk node | Name | Land | Regulierungsfrage | Nachweisforderung | source_url |
|---|---|---|---|---|---|
| `rw_fr_re2020` | France RE2020 | FR | Umweltvertr./Ökobilanz, Bauphysik | OekobilanzEPD / U-Wert | [ecologie.gouv.fr](https://www.ecologie.gouv.fr/politiques-publiques/reglementation-environnementale-re2020) |
| `rw_nl_mpg` | Netherlands MPG | NL | Umweltvertr./Ökobilanz | OekobilanzEPD | [rvo.nl](https://www.rvo.nl/onderwerpen/wetten-en-regels-gebouwen/milieuprestatie-gebouwen-mpg) |
| `rw_ch_muken` | Switzerland MuKEn | CH | Bauphysik | U-Wert / Bauphysiknachweis | [endk.ch](https://www.endk.ch/de/energiepolitik/muken) |
| `rw_uk_pas2080` | UK PAS 2080:2023 | UK | Umweltvertr./Ökobilanz | OekobilanzEPD | [bsigroup](https://www.bsigroup.com/en-US/insights-and-media/insights/brochures/pas-2080-carbon-management-in-infrastructure-and-built-environment/) |

This completes the **carbon/energy/Ökobilanz** coverage for the non-German project countries
(FR/NL/CH/UK), matching the DE `rw_geg` + `rw_qng_dgnb` and the CH `rw_sia_380_1`/`rw_sia_2032`.

### Recurring reuse incentive found across jurisdictions
**RE2020 (FR), BR18 (DK) and the EU Taxonomy all treat reused components as ~zero environmental
impact** in the LCA — a concrete, evidence-backed lever that makes reuse advantageous, now
attached to every FR/DK project via `rw_fr_re2020` / `rw_dk_br18` / `rw_eu_taxonomy`.

---

## Anchor connections — enriched model (round 6)

The connector (`connect_anchors_to_vocab.py`) now emits **three** evidence-backed edge types per
(anchor, governing rule), so the graph answers not just *which question* but *which proof* and
*which law*:

| edge_type | anchor → target | count |
|---|---|---:|
| `TRIGGERS_REGULIERUNGSFRAGE` | → Regulierungsfrage (the question) | 1 000 |
| `ERFORDERT_NACHWEIS` | → Nachweisforderung (the concrete proof) | 1 597 |
| `UNTERLIEGT_REGELWERK` | → Regelwerk (the governing law) | 1 859 |

**4 456 edges, 352 distinct anchors** — derived from `NUTZT_MATERIAL` (Bauteilgruppe 2 634),
`LIEGT_IN_LAND` (Projekt 1 309), `HAT_BAUTEILTYP` (Bauteiltyp 415), `BETRIFFT_MATERIAL`
(Material 70), `BauwerkEra` (Bauwerk 28). No Huerde/Norm edges used. `apply_to_graph.py`
dry-run validates 100% clean (all 123 nodes / 485 vocab edges / 4 456 anchor edges resolve).
