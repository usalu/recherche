# Actor reclassification dossier — non-Bauteilbörse actors

Date: 2026-06-04 · DB: `mit-bestand` · Branch: `agent_s4/schema-cleanup`

Purpose: web-verified, multi-dimensional profiles for 13 actors wrongly registered as
(or wrongly reduced from) Bauteilbörse. Every dimension is mapped to the **existing**
controlled vocabularies only:

- **Akteurtyp** (multi): Unternehmen · Person · Materialhub_Bauteilboerse · Forschung_Lehre ·
  Oeffentliche_Institution · Organisation · NGO_Verband_Netzwerk · Software_Tool_Anbieter ·
  Foerdergeber_Programmtraeger · Unbekannt
- **Geschaeftsmodell**: Shop mit Eigenstock · Multi-Vendor-Marktplatz ·
  Netzwerk / Aggregator / Redistribution · Urban-Mining-Dienstleister mit Verkaufskanal ·
  SaaS-Inventarplattform
- **Marktmodell**: Kauf gebraucht · Plattform-Kauf · Spende
- **Methode**: Urban_Mining_und_Scouting · Bestands_und_ReUse_Assessment ·
  Dokumentation_und_Monitoring · Reversibles_Design · Verfuegbarkeitsbasiertes_Design ·
  Zirkulaere_Beschaffung
- **Akteurrolle** (24) · **Bauteiltyp** (23) · **Material** (26) · **Land**

Principle: **nodes stay**; only classification is corrected. A "Bauteilbörse" is defined by
`Akteurtyp = Materialhub_Bauteilboerse AND status <> 'liquidiert'`. Genuine exchanges
(incl. SalvoWEB) are untouched.

---

## 4/5 · Opalis  (`opalis`) — Belgium / NWE
**Self-description:** *"Opalis is a business directory"*; *"facilitate the reuse of materials in construction and renovation projects."* Founded & run by **Rotor** (asbl/vzw), with Bellastock; PREUSE / Interreg NWE funded (2024–2027).
- **CORRECTION:** currently typed `Software_Tool_Anbieter` — **wrong**. It is an **NGO/research network**, not a software vendor.
- Akteurtyp → **NGO_Verband_Netzwerk** (remove Software_Tool_Anbieter)
- Akteurrolle → Forschung_Dokumentation · Bildung_Wissenstransfer · Reuse_Zirkularitaetsberatung · Materialbroker (directory, non-transactional)
- Geschaeftsmodell → Netzwerk / Aggregator / Redistribution
- Marktmodell → **none** (remove `Plattform-Kauf`; no transactions — users contact dealers directly)
- Methode → Dokumentation_und_Monitoring · Urban_Mining_und_Scouting
- Bauteiltyp → Ausbau, Boden, Dach, Daemmung, Fassade, Fenster, Technik, Traeger, Tuer, Wand (keep)
- Material → Daemmstoff, Glas, Holz, Keramik, Naturstein, Stahl, Ziegel (keep)
- Status: active · **Not a Bauteilbörse** (directory)

## 13 · ReUse and Trade  (`reuse_and_trade`) — Germany
B2B online trading platform; *"Verkauf für Firmen – Einkaufen für Jedermann"*. Operated by **ReUse and Trade GmbH** (Paderborn). General surplus goods (industrial surplus, overstock, B-ware, Restposten, office furniture), **not building-component-specific**.
- Akteurtyp → **Unternehmen** (add)
- Akteurrolle → Materialbroker/Reuse-Marketplace-Betreiber · Materiallieferung_Markt · Software_Digitalisierung
- Geschaeftsmodell → Multi-Vendor-Marktplatz
- Marktmodell → Plattform-Kauf
- Material → Mehrere · Bauteiltyp → Mehrere (general goods)
- Status: active · **Marketplace, but not a *Bauteil*börse** (general surplus, no Materialhub type)

## 21 · La Fab Bordeaux  (`la_fabrique_de_bordeaux_metropole`) — France
Public urban-development body (*aménageur*) of Bordeaux Métropole. **REFAIR** (since 2017) is its reuse initiative: a website (*"vitrine des matériaux"* — showcase) + a physical hub (*Base du Réemploi Métropolitaine*, Mérignac). 51 t collected 2019–21 across 9 sites.
- Akteurtyp → **Oeffentliche_Institution** (keep — correct)
- Akteurrolle → Bauherr_Auftraggeber · Projektmanagement_Koordination · Oeffentliche_Hand_Foerderung · Reuse_Zirkularitaetsberatung
- Methode → Dokumentation_und_Monitoring · Urban_Mining_und_Scouting
- `NUTZT_SOFTWARE` → REFAIR · `NUTZT_BAUWERK` → Base du Réemploi
- Status: active · **Not a Bauteilbörse** (REFAIR = showcase/hub platform, not La Fab; even REFAIR is non-transactional)

## 22 · Mobius Réemploi  (`mobius_reemploi`) — France/BE/EU
*"not an open marketplace."* Two divisions: **Conseil** (reuse consulting, diagnostics, site oversight) + **Industrie** (reconditioning supplier; flooring/raised access floors; 10-yr product liability).
- Akteurtyp → **Unternehmen** (remove `Materialhub_Bauteilboerse`)
- Akteurrolle → Aufbereitung_Refurbishment · Rueckbau_Bauteilernte_Logistik · Materiallieferung_Markt · Fachplanung_Nachweis · Reuse_Zirkularitaetsberatung · Nachhaltigkeitsberatung
- Geschaeftsmodell → Urban-Mining-Dienstleister mit Verkaufskanal (keep)
- Marktmodell → Kauf gebraucht
- Methode → Urban_Mining_und_Scouting · Bestands_und_ReUse_Assessment · Dokumentation_und_Monitoring
- Bauteiltyp → Boden, Technik · Status: active (`needs_evidence_urls`) · **Not a Bauteilbörse** (reconditioning supplier)

## 30 · Madaster  (`madaster`) — Netherlands (+ DE/AT/CH/BE/NO/UK chapters)
*"digital SaaS platform for material documentation… not a marketplace."* Dual structure: **Madaster Services** (company) + **Madaster Foundation** ("planet-over-profit"). Material passports, materials register, circularity & residual-value, EU-Taxonomy/ESG/CSRD reporting, 100+ EPD databases.
- Akteurtyp → **Software_Tool_Anbieter** (keep) + Unternehmen
- Akteurrolle → Software_Digitalisierung · Forschung_Dokumentation · Reuse_Zirkularitaetsberatung · Nachhaltigkeitsberatung (remove Materialbroker — does not sell)
- Geschaeftsmodell → SaaS-Inventarplattform (add)
- Marktmodell → none · Methode → Dokumentation_und_Monitoring · Bestands_und_ReUse_Assessment
- Material/Bauteiltyp → Mehrere · Status: active · **Not a Bauteilbörse** (material-passport SaaS)

## 31 · New Horizon  (`new_horizon`) — Netherlands
Urban-mining company, **subsidiary of JAJO**. 360° gebouwscan, material inventory (Oogstkaart), circular harvesting, supply of harvested materials; **Oogst Collectief** = supply/demand network (not an open marketplace). *"As kennispartner we bring data, knowledge and chain together."*
- Akteurtyp → **Unternehmen** (keep)
- Akteurrolle → Rueckbau_Bauteilernte_Logistik · Aufbereitung_Refurbishment · Materiallieferung_Markt · Reuse_Zirkularitaetsberatung · Projektmanagement_Koordination · Forschung_Dokumentation
- Geschaeftsmodell → Urban-Mining-Dienstleister mit Verkaufskanal
- Marktmodell → Kauf gebraucht · Methode → Urban_Mining_und_Scouting · Bestands_und_ReUse_Assessment · Dokumentation_und_Monitoring
- Status: active · **Not a Bauteilbörse** (urban-mining service; network not open exchange)

## 32 · New Horizon UM  (`new_horizon_urban_mining`) — Netherlands
**Duplicate** of #31 (urban-mining arm; holds the Circl project/Bauteilgruppe links).
- Akteurtyp → **Unternehmen** (remove `Materialhub_Bauteilboerse`; align with #31)
- Add `DataIssue` duplicate flag → recommend later merge into `new_horizon` (keep node for now per "nodes stay")
- **Not a Bauteilbörse**

## 34 · Loopfront  (`loopfront`) — Norway
Reuse-management **SaaS** (inventory, surveying, QR/floorplans, CO₂/cost analytics) **with an integrated** internal/external marketplace feature — not an open classic exchange.
- Akteurtyp → **Software_Tool_Anbieter** (add)
- Akteurrolle → Software_Digitalisierung · Bestands_und_ReUse_Assessment(role: Reuse_Zirkularitaetsberatung) · Materiallieferung_Markt
- Geschaeftsmodell → SaaS-Inventarplattform (add); Marktmodell → Plattform-Kauf (optional — integrated marketplace)
- Methode → Bestands_und_ReUse_Assessment · Dokumentation_und_Monitoring
- Material/Bauteiltyp → Mehrere (building materials + furniture) · Status: active · **Not a classic Bauteilbörse**

## 51 · Syphon AG  (`syphon_ag_bauteilboerse_biel_bruegg`) — Switzerland
**Genuinely WAS a Bauteilbörse** (since 2008; cleaned/repaired/tested & resold components; social integration). **Bankruptcy opened 2024-08-26 → "Syphon AG in Liquidation"** (collocation plan 2025).
- **STRICT route (no new property keys):** Akteurtyp `Materialhub_Bauteilboerse` → **`Unternehmen`** (remove Bauteilbörse type, like the other defunct/supplier cases). No `status` field is added — it does not exist in the schema.
- The liquidation remains recorded **only via existing `BELEGT_IN` evidence** (Moneyhouse / SHAB sources already attached).
- Geschaeftsmodell → Shop mit Eigenstock · Urban-Mining-Dienstleister mit Verkaufskanal (keep, historical)
- Marktmodell → Kauf gebraucht · **Former Bauteilbörse, now defunct** (node stays; dropped from active set via retype)

## 55 · Cleveland Steel & Tubes  (`cleveland_steel_tubes`) — UK
*"steel reuse experts."* Steel-tube **stockholder** (84,000 t, founder member of Bianco Group). Buys surplus/reclaimed steel, tests/certifies, reprocesses (coating removal, cutting, welding, shot-blast, paint), resells from own stock. **Steel only.**
- Akteurtyp → **Unternehmen** (remove `Materialhub_Bauteilboerse`)
- Akteurrolle → Materiallieferung_Markt · Aufbereitung_Refurbishment · Stahlbau_Fertigung · Bauausfuehrung_Fertigung · Reuse_Zirkularitaetsberatung
- Geschaeftsmodell → Shop mit Eigenstock (keep) · Marktmodell → Kauf gebraucht
- Methode → Urban_Mining_und_Scouting · Bestands_und_ReUse_Assessment
- Bauteiltyp → Traeger, Stuetze · Material → **Stahl** only · Status: active · **Not a general Bauteilbörse** (steel-specialist stockholder)

## 58 · HTS Reused Steel Stockmatcher — UK
*"free web-based selection tool for the procurement of reclaimed steel"* (Python; matches reused-steel stock lists to Revit design lists). Developed by **Heyne Tillett Steel** (structural engineers).
- **No change** — already modeled as a `Software`/`Tool` node, `NUTZT_SOFTWARE` from `heyne_tillett_steel`. Not an Akteur, not a Bauteilbörse. ✓
- Parent `heyne_tillett_steel` → Akteurtyp Unternehmen; Akteurrolle Tragwerksplanung · Fachplanung_Nachweis · Reuse_Zirkularitaetsberatung (correct).

## 60 · Material Reuse Portal  (`material_reuse_portal`) — UK
CIRCuIT (Horizon 2020) proof-of-concept **aggregator/meta-portal**; **managed by ReLondon**, tech partner **Dsposal**. Integrates listings from Globechain + eBay; find-a-marketplace; save items as digital passport; service-provider directory. No own inventory.
- Akteurtyp → **Software_Tool_Anbieter** (add) [operated by ReLondon, a public-funded body]
- Akteurrolle → Software_Digitalisierung · Materialbroker (aggregator/directory) · Reuse_Zirkularitaetsberatung
- Geschaeftsmodell → Netzwerk / Aggregator / Redistribution (add)
- Marktmodell → none (redirects to source marketplaces) · Methode → Dokumentation_und_Monitoring
- Material → Glas, Stahl, Ziegel, Naturstein · Status: active (PoC) · **Not a Bauteilbörse** (meta-aggregator)

## 61 · Salvo Ltd  (`salvo_ltd`) — UK (+ global directory)
*"Salvo does not hold stock, buy or sell."* Non-trading promotion/network body (since 1991). Runs: **Salvo Directory**, **SalvoNEWS** (publishing), **Salvo Code** + **Truly Reclaimed®** (standards), theft-alert/anti-theft register, **futuREuse** (research/consultancy), advocacy. **The marketplace is `salvoweb` (since 1994), a separate node.**
- Akteurtyp → **NGO_Verband_Netzwerk** + Organisation (remove `Materialhub_Bauteilboerse`)
- Remove Geschaeftsmodell `Multi-Vendor-Marktplatz`, `Netzwerk/Aggregator`(→ keep only network), Marktmodell `Plattform-Kauf` — **these belong on SalvoWEB**
- Akteurrolle → Bildung_Wissenstransfer · Forschung_Dokumentation · Reuse_Zirkularitaetsberatung · Materialbroker (directory/standards)
- Geschaeftsmodell → Netzwerk / Aggregator / Redistribution (directory/network)
- Methode → Dokumentation_und_Monitoring · Status: active · **Not a Bauteilbörse** (the exchange is SalvoWEB)
- **`salvoweb` — NO CHANGE**: keep Materialhub_Bauteilboerse + Multi-Vendor-Marktplatz + Plattform-Kauf; `BETRIEBEN_VON` → Salvo Ltd. ✓ (the real, retained exchange)

## 66 · materialnomaden  (`materialnomaden`) — Austria (Vienna)
Circular-design & architecture / urban-mining firm. Building & material-flow assessment, circular design, planning→implementation. **Operates a reuse store, `re:store`** (restore.or.at/store) — so a real sales channel exists, but it is *not* an open exchange platform.
- Akteurtyp → **Unternehmen** (remove `Materialhub_Bauteilboerse`)
- Akteurrolle → Reuse_Zirkularitaetsberatung · Entwurf_Planung · Rueckbau_Bauteilernte_Logistik · Aufbereitung_Refurbishment · Materiallieferung_Markt · Bildung_Wissenstransfer · Forschung_Dokumentation
- Geschaeftsmodell → Urban-Mining-Dienstleister mit Verkaufskanal **+ Shop mit Eigenstock** (re:store) — **keep both** (earlier "remove Shop" reversed: re:store confirms a shop)
- Marktmodell → Kauf gebraucht · Methode → Urban_Mining_und_Scouting · Bestands_und_ReUse_Assessment · Dokumentation_und_Monitoring
- Status: active · **Not an open Bauteilbörse** (service firm + own reuse store)

---

## Summary of Materialhub_Bauteilboerse changes
- **Remove** (6): Mobius, New Horizon UM, Cleveland, Salvo Ltd, materialnomaden, **Syphon** (retype → Unternehmen)
- **Type correction only** (1): Opalis (`Software_Tool_Anbieter` → `NGO_Verband_Netzwerk`) — was never typed Bauteilbörse
- **Untouched genuine exchange**: SalvoWEB
- **Export anchor rule** → `Akteurtyp = Materialhub_Bauteilboerse` (no status filter needed)

## Taxonomy-compliance guarantee (validated against live DB 2026-06-04)
- All proposed values exist: Akteurtyp 6 · Geschaeftsmodell 5 · Marktmodell 2 · Methode 3 · Akteurrolle 17 · Bauteiltyp 12 · Material 8 — **no new taxonomy nodes created** (MERGE onto existing only).
- **No new property keys.** Writes touch only existing keys; the `status:'liquidiert'` idea is **dropped** (Syphon handled by retype instead). Existing Akteur keys remain: `additional_marktmodelle, evidence_urls_target, id, name, needs_evidence_urls, source_scope`.

## Cross-cutting note
`Akteurrolle "Materialbroker / Reuse-Marketplace-Betreiber"` is currently attached to nearly
every actor above (incl. Madaster, La Fab, Loopfront) — it is noise. Detach from all non-marketplace
actors so role-based queries stop mislabelling directories/SaaS/suppliers as marketplace operators.
