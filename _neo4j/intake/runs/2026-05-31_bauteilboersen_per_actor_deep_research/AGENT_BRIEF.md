# Bauteilbörsen Deep Research — Agent Brief

**Date:** 2026-05-31 · **Graph DB:** `mit-bestand` · **39 anchors** already exist; this pass is additive.

---

## 1. Mission

Per anchor: visit operator URLs, propose evidence-backed links to **Material**, **Bauteiltyp**, **PruefungNachweis**, **Aufbereitungsverfahren**, **Rueckbauverfahren**. Country, Akteurtyp, Akteurrolle and base URLs are already in the graph — do not redo. **Coverage of Material + Bauteiltyp + PruefungNachweis = success metric.**

## 2. Rules

- One URL per claim. No URL → no claim. Operator-controlled sources beat third-party.
- Use the German IDs in §3 *exactly*. Nothing fits → `new_vocab_candidates`; do not invent IDs.
- Additive only. Validate HTTP status.

---

## 3. Primary targets

### 3.1 Material — `(:Akteur)-[:NUTZT_MATERIAL]->(:Material {id: "mat_*"})`
**Closed set (15):** `mat_aluminium`, `mat_beton`, `mat_daemmstoff`, `mat_glas`, `mat_gusseisen`, `mat_holz`, `mat_keramik`, `mat_kunststoff`, `mat_lehm`, `mat_naturstein`, `mat_recyclingbeton`, `mat_stahl`, `mat_stahlbeton`, `mat_stroh`, `mat_ziegel`.

### 3.2 Bauteiltyp — `(:Akteur)-[:HAT_BAUTEILTYP]->(:Bauteiltyp {id: "bt_*"})`
**Key IDs (Brand layer):** `bt_ausbau` *(space_plan)*, `bt_boden` *(space_plan)*, `bt_dach` *(skin)*, `bt_daemmung` *(structure)*, `bt_decke` *(structure)*, `bt_fassade` *(skin)*, `bt_fenster` *(skin)*, `bt_fundament` *(structure)*, `bt_gelaender` *(space_plan)*, `bt_stuetze` *(structure)*, `bt_technik` *(services)*, `bt_traeger` *(structure)*, `bt_treppe` *(space_plan)*, `bt_tuer` *(space_plan)*, `bt_wand` *(structure)*. Use `bt_mehrere` only for explicit batches.

### 3.3 PruefungNachweis — `(:Akteur)-[:HAT_PRUEFUNG]->(:PruefungNachweis)`
120 live nodes; **Cypher-lookup first** before linking:
```cypher
MATCH (p:PruefungNachweis) WHERE toLower(p.name) CONTAINS toLower($keyword) RETURN p.id, p.name
```
Triggers on operator pages:

| Operator copy says… | Search keyword(s) |
|---|---|
| Pre-Demolition Audit / Diagnose Ressource / Inventory | `audit`, `diagnose`, `inventory` |
| Material Passport / Materialpass / Madaster integration | `material_pass`, `madaster` |
| Annahmeprüfung / Foto-Prüfung / intake QA | `annahme`, `intake` |
| CE marking / CPR / Bauproduktegesetz | `ce`, `cpr` |
| Brandschutz / fire rating | `brandschutz`, `fire` |
| Statik / Tragfähigkeitsnachweis / EN 1090 reuse | `statik`, `tragfähigkeit` |
| Elektroprüfung / electrical safety / PAT | `elektro`, `electrical` |
| CO2 / LCA report from the platform | `co2`, `lca` |
| Reconditioning inspection | `reconditioned`, `refurb` |

### 3.4 Aufbereitungsverfahren — `(:Akteur)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)` (62 live)
Link only when operator describes a concrete process: sanding, repainting, sanitising, glass replacement, gasket renewal, radiator stripping/repaint, electrical testing.

### 3.5 Rueckbauverfahren — `(:Akteur)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren)` (5 live)
Only for operators that actually perform on-site demontage.

### 3.6 Cross-walk — site copy → Bauteiltyp + Material

| Site text | Bauteiltyp | Material (only if material explicitly named) |
|---|---|---|
| Türen, doors, portes, deuren | `bt_tuer` | varies — `mat_holz` / `mat_stahl` / `mat_glas` |
| Fenster, windows, fenêtres | `bt_fenster` | `mat_holz` / `mat_aluminium` / `mat_glas` |
| Bodenbeläge, flooring, parquet, decking | `bt_boden` | `mat_holz` / `mat_keramik` / `mat_naturstein` |
| Fliesen, tiles, carrelage | `bt_boden` / `bt_wand` | `mat_keramik` |
| Ziegel/Backstein, bricks, briques | `bt_wand` / `bt_fassade` | `mat_ziegel` |
| Dachziegel, roof tiles, tuiles | `bt_dach` | `mat_keramik` |
| Sanitär, plumbing, sanitaire | `bt_technik` | `mat_keramik` / `mat_kunststoff` |
| Heizkörper, radiators, Gussradiatoren | `bt_technik` | `mat_stahl` / `mat_gusseisen` |
| Leuchten, lighting, luminaires | `bt_technik` | (mixed) |
| Treppen, stairs, escaliers | `bt_treppe` | `mat_holz` / `mat_stahl` / `mat_naturstein` |
| Beschläge, fittings, ferrures, brassware | `bt_ausbau` | `mat_stahl` |
| Dämmung, insulation, isolation | `bt_daemmung` | `mat_daemmstoff` |
| Trockenbau, plasterboard | `bt_wand` | *(`mg_mineralisch` candidate — not in mat\_\*)* |
| Naturstein, stone, pierre | `bt_boden` / `bt_fassade` | `mat_naturstein` |
| Holz allgemein, timber, bois, Altholz | (depends on use) | `mat_holz` |
| Stahlträger, steel beams, lintels | `bt_traeger` | `mat_stahl` / `mat_beton` |
| Concrete blocks, aggregates | `bt_wand` / `bt_fundament` | `mat_beton` |
| Tapeten, wallpaper | `bt_ausbau` | (n/a) |

**Rule:** Material at `belegt` only if site explicitly names the material. Component-only mention (e.g. "Türen") → record `bt_tuer`, leave Material as `wahrscheinlich`+`unsicher` candidates rather than guessing.

---

## 4. Secondary (link only if it leaps off the page)

`Marktmodell` · `Logistik` (`log_*`) · `Methode` (Urban Mining, Material Passport, Harvest Map) · `Stadt` · `BETRIEBEN_VON` (only when operator clearly named *and* you searched for an existing node).

---

## 5. Output

One JSON per anchor → `<anchor_id>.enrichment.json`:

```json
{
  "anchor_id": "bauteilboerse_bremen",
  "sources_visited":  [{"url": "...", "http_status": 200, "first_party": true}],
  "materials":        [{"target_id": "mat_holz", "evidence_urls": ["..."], "evidence_quote": "≤240 chars", "confidence": "belegt|wahrscheinlich|unsicher"}],
  "bauteiltypen":     [{"target_id": "bt_tuer",  "evidence_urls": ["..."], "evidence_quote": "...",         "confidence": "..."}],
  "pruefung":         [{"target_id": "pn_...",   "evidence_urls": ["..."], "evidence_quote": "...",         "confidence": "..."}],
  "aufbereitung":     [{"target_id": "auf_...",  "evidence_urls": ["..."], "evidence_quote": "...",         "confidence": "..."}],
  "rueckbau":         [{"target_id": "rbv_...",  "evidence_urls": ["..."], "evidence_quote": "...",         "confidence": "..."}],
  "secondary_links":  [{"rel_type": "HAT_MARKTMODELL", "target_id": "...", "evidence_urls": ["..."], "evidence_quote": "...", "confidence": "..."}],
  "operator_chain":   {"operator_name": "...", "operator_anchor_id_guess": null, "evidence_urls": ["..."]},
  "new_vocab_candidates":  [{"intended_label": "Marktmodell", "intended_id_proposal": "mkt_aggregator", "rationale": "...", "evidence_urls": ["..."]}],
  "conflicts_with_archive":[{"field": "Betreiber", "archive": "...", "live": "...", "evidence_url": "..."}],
  "gaps": [{"topic": "...", "reason": "..."}]
}
```

Plus `INDEX.json` and `NEW_VOCAB_PROPOSALS.md`.

---

## 6. The 39 anchors

Format: **anchor** (Land, Stadt) · *platform* · **likely-hit IDs** (your starting target list from the archive — confirm against live) · URLs.

| # | Anchor (Land) · platform | Likely-hit IDs — verify on live site | URLs |
|---|---|---|---|
| 1 | **articonnex** (FR) · Anti-Gaspi | broad / vague — verify live | https://articonnex.com/ · /collections/reemploi · https://www.jaimelesstartups.fr/articonnex-economie-circulaire-anti-gaspi-materieux-bricolage/ |
| 2 | **backacia** (FR) · B2B + Beratung | broad B2B · **PN:** pre-demolition-audit candidate (consulting role) | https://backacia.com/ · https://opalis.eu/en/dealers/backacia · https://app.dealroom.co/companies/backacia |
| 3 | **baticycle** (FR, Paris/IDF) · second œuvre | **bt:** `bt_tuer`, `bt_boden`, `bt_wand`, `bt_technik` · **auf:** reconditioned (verify) | https://baticycle.fr/ · /materiaux-second-oeuvre/ · https://marketplace.skop.app/baticycle |
| 4 | **batiterre** (BE, Brüssel + Lüttich) · Shop + Reuse-Läden + Demontage | **mat:** `mat_naturstein`, `mat_keramik`, `mat_holz`, `mat_gusseisen` · **bt:** `bt_boden`, `bt_wand`, `bt_technik`, `bt_ausbau` · **auf:** Sanitär-/Holz-/Gussradiator-reconditioning · **rbv:** Demontage | https://www.batiterre.be/ · /shop · /vente-et-preparation-au-reemploi · https://opalis.eu/fr/fournisseurs/batiterre |
| 5 | **batrecup** (FR, Baskenland) · Community-App | P2P — vague; verify live | https://www.batrecup.com/ · https://play.google.com/store/apps/details?id=com.batrecup · /batrecup-lappli-cest-parti/ |
| 6 | **baukarussell** (AT) · Social-Urban-Mining + Katalog | projektabhängig · **PN:** pre-demolition-audit · **rbv:** selektiver Rückbau | https://www.baukarussell.at/ · /services/ · https://www.nabe.gv.at/baukarussell-social-urban-mining/ |
| 7 | **bauteilboerse_bremen** (DE, Bremen) · regionale Börse + Katalog | **mat:** `mat_holz`, `mat_glas`, `mat_stahl`, `mat_gusseisen`, `mat_keramik` · **bt:** `bt_fenster`, `bt_tuer`, `bt_boden`, `bt_treppe`, `bt_wand`, `bt_technik`, `bt_ausbau`, `bt_gelaender` · **PN:** Annahmeprüfung-per-Foto; flag "Elektro nicht als geprüft verkauft" | https://www.bauteilboerse-bremen.de/start · /katalog · /katalog/suche · /die-idee · /katalog/tueren |
| 8 | **bauteilladen_winterthur** (CH, Winterthur) · Marktplatz + Laden | **bt:** `bt_boden`, `bt_wand`, `bt_fenster`, `bt_technik`, `bt_treppe`, `bt_tuer`, `bt_decke`, `bt_dach`, `bt_ausbau` · mat: verify per category page | https://bauteilladen.ch/ · /ueber-uns/ · https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/bauteilladen-winterthur/ · /shop/ |
| 9 | **bauteilnetz_deutschland** (DE) · Netzwerk *(NGO type — not material hub)* | **bt:** `bt_fenster`, `bt_tuer`, `bt_treppe`, `bt_dach`, `bt_technik` · **mat:** `mat_holz`, `mat_keramik`, `mat_gusseisen`/`mat_stahl` · caveat: NGO — most links inherit via member-Börsen | https://www.bauteilnetz.de/ · https://www.dbu.de/projektbeispiele/das-bauteilnetz-deutschland/ · https://www.baunetzwissen.de/nachhaltig-bauen/tipps/linkliste/bauteilnetz-deutschland-3081855 |
| 10 | **building_spares_market** (UK) · Kleinanzeigen | **mat:** `mat_ziegel`, `mat_beton` · **bt:** `bt_wand`, `bt_fassade`, `bt_traeger` (lintels) | https://buildingsparesmarket.co.uk/ · /about/ · /sell-spare-and-second-hand-building-supplies-uk/ · /advert-category/general-building-materials/ |
| 11 | **cornermat_retrival** (BE, Charleroi) · Materialbörse | vague — verify live (social-enterprise context) | https://www.cornermat.be/ · /shop · https://advitam-material.be/nl/actor/cornermat/ |
| 12 | **cycle_up** (FR) · B2B + Audit | broad · **PN:** Diagnose Ressource / pre-demolition-audit | https://www.cycle-up.fr/ · https://www.climate-chance.org/en/best-pratices/cycle-up/ · https://www.innovation-transformations.ecologie.gouv.fr/actualites/visite-apprenante-de-cycle-up-acteur-de-leconomie-circulaire-du-batiment · https://opalis.eu/fr/fournisseurs/cycle |
| 13 | **cycle_zero** (FR, IDF) · App (kostenlose Bergung) | vague salvage — verify live | https://cyclezero.fr/ · https://play.google.com/store/apps/details?id=com.cycle0.cycle0app · https://apps.apple.com/fr/app/cycle-z%C3%A9ro/id6443607769 |
| 14 | **enviromate** (UK) · Marketplace (Kauf/Verkauf/Spende) | **mat:** `mat_holz`, `mat_ziegel`, `mat_daemmstoff`, `mat_keramik` · **bt:** `bt_tuer`, `bt_treppe`, `bt_daemmung`, `bt_wand`, `bt_boden` | https://www.enviromate.co.uk/ · /marketplace · /how-it-works |
| 15 | **gebruiktebouwmaterialen** (NL) · Online-Shop | **mat:** `mat_ziegel`, `mat_holz` · **bt:** `bt_dach`, `bt_fassade`, `bt_ausbau` · **PN:** Madaster material-passport cooperation | https://gebruiktebouwmaterialen.com/ · /over-ons · /assortiment.html · https://madaster.com/inspiration/madaster-and-gebruiktebouwmaterialen-com-collaborate-on-the-reuse-of-building-materials/ |
| 16 | **genbyg** (DK) · Webshop + Lager | **mat:** `mat_holz`, `mat_ziegel`, `mat_keramik` · **bt:** `bt_tuer`, `bt_fenster`, `bt_boden`, `bt_technik`, `bt_ausbau` | https://genbyg.dk/ · https://pub.norden.org/temanord2021-508/ · https://www.salvoweb.com/directory/24044-genbyg-as |
| 17 | **globechain** (UK, intl.) · ESG-Marketplace, Construction-Vertical | mostly fit-out / furniture · **bt:** `bt_ausbau` candidate · verify Bau-relevanz | https://globechain.com/ · https://marketplace.globechain.com/business/construction · https://ukgbc.org/resources/esg-reuse-marketplace/ · https://www.clustercollaboration.eu/content/online-reuse-platform-globechain |
| 18 | **insert_marketplace** (NL) · Bau + öff. Raum | first-party site missing — find it · broad once located | https://www.cinderela.eu/Cinderela-One-Stop-Shop/Database/Insert-Marketplace · https://www.interregeurope.eu/good-practices/insert-platform-for-sharing-re-useable-building-materials |
| 19 | **loopfront** (NO, Nordics) · Reuse-Plattform | broad · **PN:** CO2/LCA report; material-tracking · Software-node candidate | https://www.loopfront.com/ · /2024 · https://businessnorway.com/solutions/loopfront-digital-platform-makes-reuse-simple · https://ukgbc.org/resources/digital-reuse-platform/ · /product |
| 20 | **material_index** (UK) · B2B + Audits + Materialpässe | **bt:** `bt_tuer`, `bt_wand` (partitions), `bt_ausbau` · **PN:** material-passport, audit, refund/return policy · **auf:** refurbish | https://material-index.co.uk/ · https://material-index.exchange/edits · https://www.material-index.co.uk/materials/material-specification · https://asbp.org.uk/member/material-index · https://material-index.exchange/terms-and-conditions |
| 21 | **material_reuse_portal** (UK, London) · Aggregator | inherits from connected sources — verify | https://materialreuseportal.com/ · /About · https://relondon.gov.uk/built-environment · https://ukgbc.org/resources/aggregated-material-reuse-marketplace/ |
| 22 | **materialenbank_leuven_atelier_circuler** (BE, Leuven) · Materialbank + Lager | **mat:** `mat_holz`, `mat_naturstein`, `mat_daemmstoff` · **bt:** `bt_traeger` (Konstruktionsholz), `bt_wand` (Plattenmaterial), `bt_ausbau` (Schreinerei), `bt_daemmung`, `bt_technik` (Sanitär) · **rbv:** active dismantling | https://ateliercirculer.be/materialenbank/ · / · /materialenbank/catalogus · https://www.vvsg.be/kennis/praktijken/praktijkendatabank/materialenbank-leuven · https://pers.leuven.be/de-leuvense-materialenbank-redt-470-ton-materialen-in-2025-recordjaar-voor-circulaire-economie |
| 23 | **materialrest24** (DE/DACH) · Marktplatz für Restbestände | **mat:** `mat_holz`, `mat_keramik`, `mat_stahl` · **bt:** `bt_dach`, `bt_wand` (Trockenbau), `bt_technik` (Sanitär/Heizung), `bt_ausbau` (Bauelemente) · find first-party site | https://www.handwerk-magazin.de/materialrest24de-restbestaende-clever-verwerten-183318/ · https://nachhaltiges-handwerk.de/gute-beispiele/materialrest24 · https://www.instagram.com/materialrest24.de/ |
| 24 | **new_horizon** (NL) · Harvest Map *(Oogstkaart)* | broad urban-mining · **PN:** harvest-mapping method · **rbv:** active | https://www.superuse-studios.com/publication/oogstkaart-nl-adopted-by-new-horizon/ · /publication/harvest-collect-re-use/ · https://knowledge-hub.circle-economy.com/article/4067 |
| 25 | **r_place** (FR, Occitanie) · B2B-Plattform | broad B2B — verify live | https://r-place.fr/ · https://www.cycl-op.org/initiative/h/r-place-plateforme-b2b-du-reemploi-des-materiaux-de-construction.html · https://www.envirobat-oc.fr/R-Place |
| 26 | **raedificare** (FR) · BTP + Landschaft | broad — verify live (BTP + Landschaftsbau scope) | https://raedificare.com/marketplace/ · / · https://www.climate-chance.org/bonne-pratique/plateforme-raedificare/ |
| 27 | **re_store_harvestmap_vienna** (AT, Wien) · Online-Store + Urban Mining | **bt:** `bt_ausbau` · **PN:** HarvestMAP method · BETRIEBEN_VON `materialnomaden` already linked | https://www.restore.or.at/ · /impressum/ · https://www.materialnomaden.at/about/ |
| 28 | **reempro** (FR, Hauts-de-France/IDF + BE) · Marketplace | vague — verify live | https://www.reempro.com/marketplace/ · /marketplace-reempro/ · /on-parle-de-nous-sur-france-3/ |
| 29 | **resource_marktplaats** (NL) · App | vague; **operator unknown** — Play Store pkg `com.pss.resource` → find publisher | https://play.google.com/store/apps/details?id=com.pss.resource · https://apps.apple.com/nl/app/resource-marktplaats/id6743317802 |
| 30 | **software_restado** *(Software label)* (DE/DACH) · B2B-Marktplatz, `BETRIEBEN_VON concular` | **mat:** `mat_holz` (Altholz), `mat_keramik` (Fliesen/Klinker), `mat_ziegel` (Klinker), `mat_naturstein` (Steine) · **bt:** `bt_tuer`, `bt_fenster`, `bt_boden`/`bt_wand` (Fliesen), `bt_dach`, `bt_fassade`, `bt_technik` (Haustechnik/Sanitär), `bt_ausbau` (Innenausbau) | https://restado.de/ · /ueber-restado/ · /materialreste/ · /hilfe/impressum/ · /haendler-auf-restado-werden/ |
| 31 | **reuse_and_trade** (DE) · digitale Reuse-Börse | broad + Möbel — **verify whether `at_materialhub_bauteilboerse` type still fits** | https://www.reuseandtrade.de/ · /artikeluebersicht/Schnaeppchen-fuer-Privatkunden.aspx · https://www.facebook.com/ReUseandTrade/ |
| 32 | **rotordc** (BE, Brüssel/Evere) · Webshop + Lager + Demontage | **mat:** `mat_naturstein`, `mat_keramik`, `mat_holz` · **bt:** `bt_tuer`, `bt_boden`, `bt_technik` (Leuchten + Sanitär), `bt_ausbau` (Beschläge + Tapeten) · **auf:** refurbish (Deposit Sale / Konsignation) · **rbv:** active | https://rotordc.com/ · /service/depositsale · /shop · /about-us |
| 33 | **salvoweb** (UK, intl.) · Marketplace + Händlerverzeichnis | **mat:** `mat_ziegel`, `mat_naturstein`, `mat_holz` · **bt:** `bt_boden`, `bt_wand` (bricks/stone) · Methode: Architectural Salvage · BETRIEBEN_VON `salvo_ltd` already linked | https://www.salvoweb.com/ · /antique-reclaimed · https://www.thehousedirectory.com/salvo-truly-reclaimed-sustainability/ |
| 34 | **salza** (CH, Zürich) · Bauteildatenbank + Beratung | vague — extract Bauteilkategorien live | https://salza.ch/ · /bauteil-plattform · /how-it-works |
| 35 | **skop_marketplace** (FR) · Marketplace Reuse + Reconditioned | **auf:** reconditioned process · multi-vendor — cross-link to `baticycle` (vendor) | https://marketplace.skop.app/ · https://www.skop.app/marketplace-materiaux-reemploi · https://www.francenum.gouv.fr/activateurs/skop |
| 36 | **surplus_building_and_plumbing_materials** (UK) · Surplus-Marketplace | **mat:** `mat_ziegel`, `mat_beton`, `mat_keramik`, `mat_holz` (decking), `mat_stahl` (brassware), `mat_kunststoff` (guttering) · **bt:** `bt_dach` (roofing tiles), `bt_wand` (plasterboard/bricks), `bt_technik` (electrical/lighting/kitchens/bathrooms/guttering), `bt_boden` (paving/decking) | https://surplusbuildingsupplies.co.uk/ · /how-it-works/ · /building-materials.html |
| 37 | **sustainability_yard** (UK) · App-/Web-Marketplace | **mat:** `mat_holz`, `mat_keramik`, `mat_naturstein` · **bt:** `bt_boden`, `bt_wand` (tiles) · **PN:** CO2 report (laut Quelle geplant — verify) | https://sustainabilityyard.com/ · /docs/sell-on-sustainability-yard · /docs/sell-on-sustainability-yard-business · https://materialreuseportal.com/Marketplace-Providers |
| 38 | **useagain_bauteilclick** (CH) · eBKP-H-Vermittlungsplattform | **mat:** `mat_stahl` (Stahlträger), `mat_holz` · **bt:** `bt_tuer`, `bt_fenster`, `bt_traeger`, `bt_technik` (Sanitär), `bt_ausbau`, `bt_fassade` (Gebäudehülle) · **Norm:** eBKP-H / SN 506 511 (link via `Norm` if node exists) | https://www.useagain.ch/de/ · https://library-of-reuse.ch/pioneers/useagain · https://www.bauwende.tools/en/werkzeuge/use-again · /de/kaufen |
| 39 | **warp_it** (UK) · Org. Resource-Redistribution (NHS, Unis) | mostly stuff layer · **verify whether `at_materialhub_bauteilboerse` type still fits** | https://www.warp-it.co.uk/ · /report-guide · https://www.gla.ac.uk/myglasgow/sustainability/wasterecyclingreuse/warpit-furniturerecycling/ · /benefits |

---

## 7. Stop-and-ask

Pause for human review when: operator chain is ambiguous · >5 new vocab candidates from one actor · all operator URLs unreachable · archive contradicts live materially (operator changed, platform sunset, wrong country).

**Start with #7 (`bauteilboerse_bremen`) — richest category list, cleanest calibration target for Material + Bauteiltyp + PruefungNachweis.**
