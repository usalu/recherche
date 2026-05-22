# REWIRE REVIEW — old labels → new evidenced vocabulary

Semantic mapping first (what each old node *means* in the new model), evidence second (the target Regelwerk's source URL backs it). One row per old node lives in `rewire_map.csv`.

**341 old nodes mapped.** Action summary:

| Action | n |
|---|--:|
| REWIRE->Regelwerk | 123 |
| KEEP+wire->Nachweis(method) | 120 |
| REWIRE->Nachweis/Frage | 46 |
| DELETE (regulatory) | 17 |
| KEEP+wire->Nachweis | 13 |
| KEEP (market/logistics) | 11 |
| DELETE+GAP | 3 |
| REVIEW/OUT | 3 |
| KEEP-ENUM | 3 |
| DELETE+GAP/Frage | 2 |

## Norm (103) → Regelwerk  · REPLACE & delete label

103 Norm nodes (heavy duplication) collapse onto evidenced Regelwerke. Targets:

| → Regelwerk target | # Norm nodes | evidence |
|---|--:|---|
| DIN 4074 / EN 14081 (Holzsortierung) | 13 | https://www.holzbau-deutschland.de/fileadmin/user_upload/eingebundene_Downloads/2022-12_Information_Sortierung_durch_den_Zimmermeister_01.pdf |
| Eurocodes EN/DIN EN 1990-1999 | 13 | https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-basis-structural-design |
| EN 1469/12058/1936 (Naturstein-Produktnormen) | 11 | https://landingpage.bsigroup.com/LandingPage/Undated?UPI=000000000030090410 |
| SIA 269 | 7 | https://www.espazium.ch/de/aktuelles/die-neue-norm-sia-2698 |
| EN 1168 (Hohlplatten/Hollow-core slabs) | 6 | https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011 |
| DIN 18945-18947 (Lehmbaustoffe) | 4 | https://www.baunetzwissen.de/gesund-bauen/fachwissen/regelwerke/normen-fuer-den-lehmbau-3393643 |
| EN/DIN EN 1090 | 4 | https://bauforumstahl.de/wp-content/uploads/2024/02/bfs-CE-Kennzeichnung_nach_EN-1090.pdf |
| EN 15804 / EN 15978 (EPD/LCA) | 4 | https://www.gebaeudeforum.de/wissen/nachhaltiges-bauen-und-sanieren/lebenszyklusbetrachtung/oekobilanzierung-lca/ |
| EN 771 (reclaimed masonry units) | 4 | https://reclaimedbrickcompany.co.uk/blogs/yard-display/reclaimed-brick-company-becomes-first-uk-supplier-to-achieve-bs-en-771-1-testing-for-reclaimed-bricks |
| DIN EN 13501 | 4 | https://www.baunetzwissen.de/daemmstoffe/fachwissen/normen/din-en-13501-klassifizierung-von-bauprodukten-und-bauarten-zu-ihrem-brandverhalten-1005853 |
| SCI P427 | 4 | https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf |
| CEN/TS 1090-201:2024 | 3 | https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024 |
| Dutch Bbl | 2 | https://climate-laws.org/document/the-environment-buildings-decree-of-the-netherlands-besluit-bouwwerken-leefomgeving-bbl_1057 |
| CEN/TS 17440 (Bewertung bestehender Tragwerke) | 2 | https://eurocodes.jrc.ec.europa.eu/news/cents-174402020-assessment-and-retrofitting-existing-structures |
| MVV TB / VV TB | 2 | https://www.dibt.de/de/wir-bieten/technische-baubestimmungen |
| DAfStb-Richtlinie R-Beton | 2 | https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550 |
| Norway TEK17 (ombrukskartlegging) | 2 | https://www.dibk.no/regelverk/byggteknisk-forskrift-tek17/9/9-5 |
| Madaster / Gebaeuderessourcenpass | 1 | https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport |
| GAP_nl_beton_reuse | 1 | — (gap, see §Gaps) |
| DIN 18008 | 1 | https://www.baunormenlexikon.de/norm/din-18008-4/e87129e6-4c53-4386-852c-b6fd49626b0d |
| DIN 68800 / AltholzV | 1 | https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html |
| EN 13162 (Mineralwolle-Dämmstoffe) | 1 | https://www.intertek.com/building/standards/en-13162/ |
| ISO 20887 (Design for Disassembly/Adaptability) | 1 | https://www.iso.org/standard/69370.html |
| NEN 8700-serie (bestaande bouw) | 1 | https://www.nen.nl/bouw/constructieve-veiligheid/constructieve-veiligheid-bestaande-bouw |
| fib Bulletins (precast concrete reuse) | 1 | https://www.fib-international.org/publications/fib-bulletins/special-design-considerations-for-precast-prestress-pdf-detail.html |
| France RE2020 | 1 | https://www.ecologie.gouv.fr/politiques-publiques/reglementation-environnementale-re2020 |
| SIA 269/2 (Erhaltung Betonbau) | 1 | https://cms.sia.ch/de/api/getMedia/715 |
| SIA 380/1 | 1 | https://shop.sia.ch/normenwerk/architekt/380-1_2016_d/D/Product |
| GAP_ch_barrierefrei | 1 | — (gap, see §Gaps) |
| EN 1992-4 (Befestigungen in Beton) | 1 | https://fastenerandfixing.com/construction-fixings/design-of-fastenings-for-use-in-concrete-en-1992-4-publication-and-the-implication-for-anchor-manufacturers-and-consumers/ |
| VKF Brandschutzvorschriften (CH) | 1 | https://www.bsvonline.ch/de |
| GAP_ch_baupg | 1 | — (gap, see §Gaps) |
| UKCA / CE marking | 1 | https://www.ssqgroup.com/ukca-marking-to-replace-ce-marking-on-construction-products |

## Schadstoff (13) → Nachweisforderung + Regelwerk · KEEP
Real pollutant entities kept; wired to their check (Nachweisforderung) and law (Regelwerk).

| old node | → new target | evidence |
|---|---|---|
| `s_asbest` | AsbestCheck | https://www.baua.de/DE/Angebote/Regelwerk/TRGS/TRGS-519 |
| `s_bleifarbe` | SchwermetallOderBleifarbeCheck | https://www.reach-clp-biozid-helpdesk.de/SharedDocs/Meldungen/DE/REACH/2023-07-20-Beschr%C3%A4nkung_Formaldehyd_Abspalter |
| `s_chlorid` | Schadstoffpruefung | https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024 |
| `s_formaldehyd` | FormaldehydOderEmissionsnachweis + VOC_Emissionsnachweis | — |
| `s_holzschutzmittel` | HolzschutzmittelCheck | https://www.gesetze-im-internet.de/altholzv/BJNR330210002.html |
| `s_kmf` | KMFCheck | https://www.baua.de/DE/Angebote/Regelwerk/TRGS/pdf/TRGS-521.pdf |
| `s_mineraloel` | Schadstoffpruefung | https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024 |
| `s_pak` | PAKCheck | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=LEGISSUM:4406078 |
| `s_pcb` | PCBCheck | https://eur-lex.europa.eu/legal-content/DE/TXT/?uri=LEGISSUM:4406078 |
| `s_radon` | Radonmessung | https://www.bfs.de/DE/themen/ion/umwelt/radon/regelungen/referenzwert.html |
| `s_salze` | Schadstoffpruefung | https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024 |
| `s_schimmel` | MikrobielleBelastungCheck | https://www.umweltbundesamt.de/themen/gesundheit/umwelteinfluesse-auf-den-menschen/schimmel/aktueller-uba-schimmelleitfaden |
| `s_schwermetalle` | SchwermetallOderBleifarbeCheck | https://www.reach-clp-biozid-helpdesk.de/SharedDocs/Meldungen/DE/REACH/2023-07-20-Beschr%C3%A4nkung_Formaldehyd_Abspalter |

## Bauproduktstatus (15) → Regelwerk / enum · REWIRE
Conformity routes → Regelwerk; 3 generic statuses kept as enum; US/JP out of scope.

| old node | → new target | evidence |
|---|---|---|
| `bps_abz_abg` | DIBt ZiE/vBG/abZ/aBG | https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg |
| `bps_baupg_ch` | GAP_ch_baupg | — |
| `bps_bestand_no_status` | KEEP_ENUM | — |
| `bps_ce_eta` | EU CPR 2024/3110 | https://www.ressource-deutschland.de/service/rechtlicher-rahmen-zur-ressourceneffizienz/eu-bauprodukte-verordnung-2024/3110/ |
| `bps_ce_hen` | EU CPR 2024/3110 | https://www.ressource-deutschland.de/service/rechtlicher-rahmen-zur-ressourceneffizienz/eu-bauprodukte-verordnung-2024/3110/ |
| `bps_ibc_104_11_alternative` | OUT_OF_SCOPE_usa | — |
| `bps_jis_jas_mlit` | OUT_OF_SCOPE_jp | — |
| `bps_nta_8713` | NTA 8713 (Reuse of structural steel) | https://www.nen.nl/nta-8713-2023-nl-307691 |
| `bps_pemd_fr` | France Diagnostic PEMD (loi AGEC) | https://www.ecologie.gouv.fr/politiques-publiques/diagnostic-produits-equipements-materiaux-dechets-pemd |
| `bps_project_specific` | KEEP_ENUM | — |
| `bps_tracimat_be` | Belgian regional rules / Tracimat | https://vito.be/en/news/demolition-guide-recognizes-building-materials-recycling-or-reuse |
| `bps_ue_zeichen` | MBO/LBO | https://www.dgwz.de/gesetze/musterbauordnung-mbo-landesbauordnung-lbo |
| `bps_ukca` | UKCA / CE marking | https://www.ssqgroup.com/ukca-marking-to-replace-ce-marking-on-construction-products |
| `bps_unbekannt` | KEEP_ENUM | — |
| `bps_zie_vbg` | DIBt ZiE/vBG/abZ/aBG | https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg |

## RechtlicheBedingung (16) → Regelwerk / Frage · REWIRE & delete label
Legal conditions map to a Regelwerk or a Genehmigung/Haftung question.

| old node | → new target | evidence |
|---|---|---|
| `rb_bauordnungsrecht` | MBO/LBO | https://www.dgwz.de/gesetze/musterbauordnung-mbo-landesbauordnung-lbo |
| `rb_bauproduktenverordnung_cpr` | EU CPR 2024/3110 | https://www.ressource-deutschland.de/service/rechtlicher-rahmen-zur-ressourceneffizienz/eu-bauprodukte-verordnung-2024/3110/ |
| `rb_boulder_deconstruction_ordinance_8366` | OUT_OF_SCOPE_usa | — |
| `rb_ce_marking_reused_steel` | EN/DIN EN 1090 | https://bauforumstahl.de/wp-content/uploads/2024/02/bfs-CE-Kennzeichnung_nach_EN-1090.pdf |
| `rb_denkmalschutz` | Denkmalschutz / heritage protection | https://www.region-gestalten.bund.de/Region/DE/Potenzial_Leerstand/Instrumente/Regeln/Denkmalrechtliche_Befugnisse/denkmalrechtliche_befugnisse_node.html |
| `rb_dibt_zustimmung` | DIBt ZiE/vBG/abZ/aBG | https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg |
| `rb_eu_taxonomie` | EU Taxonomy (Circular Economy TSC) | https://finance.ec.europa.eu/system/files/2023-06/taxonomy-regulation-delegated-act-2022-environmental_en_0.pdf |
| `rb_gewaehrleistung` | ProdHaftG / BGB §823 | https://de.wikipedia.org/wiki/Produkthaftung_(Deutschland) |
| `rb_grade_ii_listing` | Denkmalschutz / heritage protection | https://www.region-gestalten.bund.de/Region/DE/Potenzial_Leerstand/Instrumente/Regeln/Denkmalrechtliche_Befugnisse/denkmalrechtliche_befugnisse_node.html |
| `rb_kreislaufwirtschaftsgesetz_krwg` | KrWG §6/§7/§8 | https://www.gesetze-im-internet.de/krwg/__6.html |
| `rb_materialpass` | Madaster / Gebaeuderessourcenpass | https://www.dgnb.de/en/sustainable-building/circular-building/building-resource-passport |
| `rb_produkthaftung` | ProdHaftG / BGB §823 | https://de.wikipedia.org/wiki/Produkthaftung_(Deutschland) |
| `rb_schweizer_bauproduktegesetz` | GAP_ch_baupg | — |
| `rb_ukca_marking_reused_steel` | UKCA / CE marking | https://www.ssqgroup.com/ukca-marking-to-replace-ce-marking-on-construction-products |
| `rb_vergaberecht` | Zirkuläre Beschaffung / Vergaberecht (NKWS) | https://concular.de/leitfaden-fuer-zirkulaeres-planen-und-bauen-fuer-die-oeffentliche-hand-veroeffentlicht/ |
| `rb_zulassung_im_einzelfall` | DIBt ZiE/vBG/abZ/aBG | https://www.dibt.de/de/wir-bieten/zulassungen-etas-und-mehr/zustimmung-im-einzelfall-zie-und-vorhabenbez-bauartgenehmigung-vbg |

## PruefungNachweis (120) → Nachweisforderung · KEEP as method layer
Concrete test *methods* hung under the proof category via `ERFUELLT_NACHWEIS` (dedup pn_/pr_ pairs).

| → target Nachweisforderung | # nodes |
|---|--:|
| Materialpruefung | 55 |
| ZustandsUndMassaufnahme | 17 |
| ProduktstatusUndLeistungserklaerung | 12 |
| Schadstoffpruefung | 12 |
| HerkunftsUndRueckbaudokumentation | 6 |
| Standsicherheitsnachweis | 6 |
| Brandschutznachweis | 5 |
| SicherheitsglasInfo | 3 |
| U_WertOderEnergieInfo | 3 |
| MikrobielleBelastungCheck | 1 |

## Leistungsanforderung (46) → Nachweis/Frage · REWIRE (slim)
Performance requirements mapped to the proof that demonstrates them.

| → target Nachweisforderung | # nodes |
|---|--:|
| ProduktstatusUndLeistungserklaerung | 10 |
| Materialpruefung | 10 |
| Bauphysiknachweis | 7 |
| Brandschutznachweis | 6 |
| AbsturzsicherungNachweis | 4 |
| Schadstoffpruefung | 4 |
| Standsicherheitsnachweis | 3 |
| HerkunftsUndRueckbaudokumentation | 2 |

## Huerde (28) → SPLIT

**KEEP (11 market/logistics barriers — distinct axis, not regulatory):** h_akzeptanzproblem, h_aufbereitungsaufwand, h_ausschreibungsproblem, h_entwurfsbindung, h_fehlende_lagerflaeche, h_heterogenitaet_chargen, h_mengenunsicherheit, h_terminunsicherheit, h_unkonventionelles_material, h_verfuegbarkeitsproblem, h_witterung_feuchte

**DELETE (17 regulatory barriers — now covered by evidenced Frage/Nachweis):** h_anschlussproblem, h_bauproduktstatus, h_brandschutzkonflikt, h_bruch_beschaedigungsrisiko, h_datenluecke, h_dauerhaftigkeit_restlebensdauer, h_fehlende_datenstandards, h_fehlende_standardisierung, h_gewaehrleistung, h_haftung, h_hygieneanforderung, h_kompatibilitaetsproblem, h_materialqualitaet_unklar, h_schadstoffbelastung, h_technische_freigabe, h_toleranzen, h_zustand_unklar

## Gaps / needs your decision (8)

| old node | issue | suggestion |
|---|---|---|
| `norm_crow_cur_4_2023` (Norm) | GAP_nl_beton_reuse | fold to DAfStb R-Beton, or research CROW-CUR 4:2023 (NL) |
| `norm_sia_500` (Norm) | GAP_ch_barrierefrei | fold to DIN 18040 (DE analog) or drop |
| `norm_swiss_baupg` (Norm) | GAP_ch_baupg | research Swiss BauPG (1 new Regelwerk) |
| `bps_baupg_ch` (Bauproduktstatus) | GAP_ch_baupg | research Swiss BauPG (1 new Regelwerk) |
| `bps_ibc_104_11_alternative` (Bauproduktstatus) | OUT_OF_SCOPE_usa | no EU relevance → delete |
| `bps_jis_jas_mlit` (Bauproduktstatus) | OUT_OF_SCOPE_jp | no EU relevance → delete |
| `rb_boulder_deconstruction_ordinance_8366` (RechtlicheBedingung) | OUT_OF_SCOPE_usa | no EU relevance → delete |
| `rb_schweizer_bauproduktegesetz` (RechtlicheBedingung) | GAP_ch_baupg | research Swiss BauPG (1 new Regelwerk) |

## Net result

- **Delete labels:** `Norm`, `RechtlicheBedingung` (fully rewired to Regelwerk/Frage).
- **Mostly delete:** `Bauproduktstatus` (12 → Regelwerk; keep 3 status enums).
- **Keep + rewire:** `Schadstoff` (wired to checks/laws), `PruefungNachweis` (method layer under Nachweis), `Leistungsanforderung` (slim), `Huerde` (11 market barriers only).
- **One evidenced law layer** (`Regelwerk`, 90) replaces the 4 overlapping old ones.

*Next:* on approval I build the migration (idempotent: create rewired edges with evidence, then delete replaced nodes/edges) as a separate `review_run`, with rollback + a re-audit.