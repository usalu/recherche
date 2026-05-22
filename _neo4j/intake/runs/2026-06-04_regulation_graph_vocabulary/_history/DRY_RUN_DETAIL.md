# Dry-run detail — anchor connections with evidence

Total anchor edges: 3606 across 349 anchors. Below: the most-connected anchor of each type, full evidence.


## [Material] `mat_beton` — Beton

### TRIGGERS_REGULIERUNGSFRAGE (3)
- **BauproduktstatusFrage** (`rf_bauproduktstatus_frage`) · conf 0.88 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **TragwerkssicherheitFrage** (`rf_tragwerkssicherheit_frage`) · conf 0.88 · 5 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **UmweltvertraeglichkeitOekobilanzFrage** (`rf_umweltvertraeglichkeit_oekobilanz_frage`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_dafstb_rc_beton (DAfStb-Richtlinie R-Beton) geregelt
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550

### ERFORDERT_NACHWEIS (5)
- **Materialpruefung** (`nf_materialpruefung`) · conf 0.88 · 5 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **ProduktstatusUndLeistungserklaerung** (`nf_produktstatus_und_leistungserklaerung`) · conf 0.88 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **Standsicherheitsnachweis** (`nf_standsicherheitsnachweis`) · conf 0.88 · 4 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **RcGesteinskoernungEignung** (`nf_rc_gesteinskoernung_eignung`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_dafstb_rc_beton (DAfStb-Richtlinie R-Beton) geregelt
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550
- **ZustandsUndMassaufnahme** (`nf_zustands_und_massaufnahme`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_sia_269_2 (SIA 269/2 (Erhaltung Betonbau)) geregelt
  - src: https://cms.sia.ch/de/api/getMedia/715

### UNTERLIEGT_REGELWERK (5)
- **EN 1168 (Hohlplatten/Hollow-core slabs)** (`rw_en_1168`) · conf 0.88 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_1168 (EN 1168 (Hohlplatten/Hollow-core slabs)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **DAfStb-Richtlinie R-Beton** (`rw_dafstb_rc_beton`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_dafstb_rc_beton (DAfStb-Richtlinie R-Beton) geregelt
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550
- **EN 13791 / EN 12504 (In-situ Beton)** (`rw_en_13791_12504`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_en_13791_12504 (EN 13791 / EN 12504 (In-situ Beton)) geregelt
  - src: https://standards.iteh.ai/catalog/standards/cen/3209bcc7-df9a-4eb2-904d-e690e79b7452/en-13791-2019
- **SIA 269/2 (Erhaltung Betonbau)** (`rw_sia_269_2`) · conf 0.85 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_sia_269_2 (SIA 269/2 (Erhaltung Betonbau)) geregelt
  - src: https://cms.sia.ch/de/api/getMedia/715
- **fib Bulletins (precast concrete reuse)** (`rw_fib_precast_reuse`) · conf 0.7 · 1 rule(s)
  - why: Material 'mat_beton' wird durch rw_fib_precast_reuse (fib Bulletins (precast concrete reuse)) geregelt
  - src: https://www.fib-international.org/publications/fib-bulletins/special-design-considerations-for-precast-prestress-pdf-detail.html


## [Bauteilgruppe] `bg_mehrere_mehrere_christ_pavilion_complete_ensemble` — Gesamtes transloziertes…

### TRIGGERS_REGULIERUNGSFRAGE (7)
- **BauphysikFrage** (`rf_bauphysik_frage`) · conf 0.82 · 2 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **BauproduktstatusFrage** (`rf_bauproduktstatus_frage`) · conf 0.82 · 6 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **BrandschutzFrage** (`rf_brandschutz_frage`) · conf 0.82 · 1 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **TragwerkssicherheitFrage** (`rf_tragwerkssicherheit_frage`) · conf 0.67 · 9 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **ReuseDokumentationFrage** (`rf_reusedokumentationfrage`) · conf 0.64 · 2 rule(s)
  - why: Verbundbauteil (4 Materialien) -> Trennbarkeit/Rueckbau erforderlich
  - src: https://www.iso.org/standard/69370.html
- **RueckbauUndBauteilernteFrage** (`rf_rueckbau_und_bauteilernte_frage`) · conf 0.64 · 1 rule(s)
  - why: Verbundbauteil (4 Materialien) -> Trennbarkeit/Rueckbau erforderlich
  - src: https://www.iso.org/standard/69370.html
- **UmweltvertraeglichkeitOekobilanzFrage** (`rf_umweltvertraeglichkeit_oekobilanz_frage`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_beton' (live NUTZT_MATERIAL); rw_dafstb_rc_beton regelt 'mat_beton' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550

### ERFORDERT_NACHWEIS (9)
- **ProduktstatusUndLeistungserklaerung** (`nf_produktstatus_und_leistungserklaerung`) · conf 0.82 · 4 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **U_WertOderEnergieInfo** (`nf_u_wert_oder_energie_info`) · conf 0.82 · 2 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **Befestigungsnachweis** (`nf_befestigungsnachweis`) · conf 0.67 · 3 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **Materialpruefung** (`nf_materialpruefung`) · conf 0.67 · 9 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **Standsicherheitsnachweis** (`nf_standsicherheitsnachweis`) · conf 0.67 · 4 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **HerkunftsUndRueckbaudokumentation** (`nf_herkunfts_und_rueckbaudokumentation`) · conf 0.64 · 1 rule(s)
  - why: Verbundbauteil (4 Materialien) -> Trennbarkeit/Rueckbau erforderlich
  - src: https://www.iso.org/standard/69370.html
- **RcGesteinskoernungEignung** (`nf_rc_gesteinskoernung_eignung`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_beton' (live NUTZT_MATERIAL); rw_dafstb_rc_beton regelt 'mat_beton' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550
- **SicherheitsglasInfo** (`nf_sicherheitsglas_info`) · conf 0.52 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_glas' (live NUTZT_MATERIAL); rw_glas_reuse_igu regelt 'mat_glas' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://www.glassonweb.com/article/reuse-and-remanufacturing-insulated-glass-units
  …(+1 more)

### UNTERLIEGT_REGELWERK (12)
- **EN 13830 (Vorhangfassade/Curtain Walling)** (`rw_en_13830`) · conf 0.82 · 1 rule(s)
  - why: Bauteilgruppe ist Bauteiltyp 'bt_fassade' (live HAT_BAUTEILTYP); rw_en_13830 ist die Produktnorm dafuer
  - src: https://www.intertek.com/building/standards/en-13830/
- **CEN/TS 1090-201:2024** (`rw_cen_ts_1090_201`) · conf 0.67 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_cen_ts_1090_201 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024
- **EN 1168 (Hohlplatten/Hollow-core slabs)** (`rw_en_1168`) · conf 0.65 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_beton' (live NUTZT_MATERIAL); rw_en_1168 regelt 'mat_beton' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/e42ae69b-eeba-4f82-b1a2-a0ef748a1752/en-1168-2005a3-2011
- **ISO 20887 (Design for Disassembly/Adaptability)** (`rw_iso_20887`) · conf 0.64 · 1 rule(s)
  - why: Verbundbauteil (4 Materialien) -> Trennbarkeit/Rueckbau erforderlich
  - src: https://www.iso.org/standard/69370.html
- **DAfStb-Richtlinie R-Beton** (`rw_dafstb_rc_beton`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_beton' (live NUTZT_MATERIAL); rw_dafstb_rc_beton regelt 'mat_beton' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://www.dinmedia.de/en/technical-rule/dafstb-beton-rezyklierte-gesteinskoernung/139271550
- **EN/DIN EN 1090** (`rw_en_1090`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_en_1090 regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://bauforumstahl.de/wp-content/uploads/2024/02/bfs-CE-Kennzeichnung_nach_EN-1090.pdf
- **EN 1090-2 / EN 14399 (bolt reuse limits)** (`rw_en_1090_2_bolts_reuse`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_stahl' (live NUTZT_MATERIAL); rw_en_1090_2_bolts_reuse regelt 'mat_stahl' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://www.steelconstruction.info/Preloaded_bolting
- **EN 13791 / EN 12504 (In-situ Beton)** (`rw_en_13791_12504`) · conf 0.63 · 1 rule(s)
  - why: Bauteilgruppe nutzt Material 'mat_beton' (live NUTZT_MATERIAL); rw_en_13791_12504 regelt 'mat_beton' [Verbundbauteil: Material nur Teilfraktion]
  - src: https://standards.iteh.ai/catalog/standards/cen/3209bcc7-df9a-4eb2-904d-e690e79b7452/en-13791-2019
  …(+4 more)


## [Bauteiltyp] `bt_fassadenmodul_mauerwerk` — bt_fassadenmodul_mauerwerk

### TRIGGERS_REGULIERUNGSFRAGE (4)
- **BauphysikFrage** (`rf_bauphysik_frage`) · conf 0.81 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **BauproduktstatusFrage** (`rf_bauproduktstatus_frage`) · conf 0.81 · 2 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **BrandschutzFrage** (`rf_brandschutz_frage`) · conf 0.81 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **TragwerkssicherheitFrage** (`rf_tragwerkssicherheit_frage`) · conf 0.76 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_771_reclaimed ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://reclaimedbrickcompany.co.uk/blogs/yard-display/reclaimed-brick-company-becomes-first-uk-supplier-to-achieve-bs-en-771-1-testing-for-reclaimed-bricks

### ERFORDERT_NACHWEIS (3)
- **ProduktstatusUndLeistungserklaerung** (`nf_produktstatus_und_leistungserklaerung`) · conf 0.81 · 2 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **U_WertOderEnergieInfo** (`nf_u_wert_oder_energie_info`) · conf 0.81 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **Materialpruefung** (`nf_materialpruefung`) · conf 0.76 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_771_reclaimed ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://reclaimedbrickcompany.co.uk/blogs/yard-display/reclaimed-brick-company-becomes-first-uk-supplier-to-achieve-bs-en-771-1-testing-for-reclaimed-bricks

### UNTERLIEGT_REGELWERK (2)
- **EN 13830 (Vorhangfassade/Curtain Walling)** (`rw_en_13830`) · conf 0.81 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_13830 ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://www.intertek.com/building/standards/en-13830/
- **EN 771 (reclaimed masonry units)** (`rw_en_771_reclaimed`) · conf 0.76 · 1 rule(s)
  - why: Bauteiltyp 'bt_fassadenmodul_mauerwerk': rw_en_771_reclaimed ist die Produktnorm fuer diesen Bauteiltyp
  - src: https://reclaimedbrickcompany.co.uk/blogs/yard-display/reclaimed-brick-company-becomes-first-uk-supplier-to-achieve-bs-en-771-1-testing-for-reclaimed-bricks


## [Projekt] `p_awm_muenster_circular_office` — AWM Münster – zirkulärer…

### TRIGGERS_REGULIERUNGSFRAGE (8)
- **ReuseDokumentationFrage** (`rf_reusedokumentationfrage`) · conf 0.9 · 9 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_krwg gilt
  - src: https://www.gesetze-im-internet.de/krwg/__6.html
- **RueckbauUndBauteilernteFrage** (`rf_rueckbau_und_bauteilernte_frage`) · conf 0.9 · 9 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_krwg gilt
  - src: https://www.gesetze-im-internet.de/krwg/__6.html
- **BauphysikFrage** (`rf_bauphysik_frage`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Neubau-/Umbaukontext (['bai_umbau']); rw_geg gilt
  - src: https://www.gebaeudeforum.de/ordnungsrecht/geg/
- **HaftungGewaehrleistungFrage** (`rf_haftung_gewaehrleistung_frage`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_vob_c_din_18459 gilt
  - src: https://www.deutscher-abbruchverband.de/publikationen/handlungshilfen-downloads/atv-din-18459/
- **SchadstoffFrage** (`rf_schadstoff_frage`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_eu_cdw_protocol gilt
  - src: https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- **UmweltvertraeglichkeitOekobilanzFrage** (`rf_umweltvertraeglichkeit_oekobilanz_frage`) · conf 0.85 · 5 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_eu_taxonomy gilt
  - src: https://finance.ec.europa.eu/system/files/2023-06/taxonomy-regulation-delegated-act-2022-environmental_en_0.pdf
- **BauproduktstatusFrage** (`rf_bauproduktstatus_frage`) · conf 0.8 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_espr_dpp gilt
  - src: https://green-forum.ec.europa.eu/implementing-ecodesign-sustainable-products-regulation_en
- **HygieneElektroFunktionFrage** (`rf_hygiene_elektro_funktion_frage`) · conf 0.6 · 1 rule(s)
  - why: Öffentliche Nutzung ['nut_buero'] + Neubau/Umbau -> Barrierefreiheit
  - src: https://www.baunormenlexikon.de/norm/din-18040-1/c099c3ee-ecd0-48ed-9d9d-ec0f84970d53

### ERFORDERT_NACHWEIS (12)
- **Bauteilidentifikation** (`nf_bauteilidentifikation`) · conf 0.9 · 3 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_din_spec_91484 gilt
  - src: https://din.one/pages/viewpage.action?pageId=160465716
- **DauerhaftigkeitRestlebensdauer** (`nf_dauerhaftigkeit_restlebensdauer`) · conf 0.9 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_din_spec_91525 gilt
  - src: https://www.dinmedia.de/en/technical-rule/din-spec-91525/397760893
- **HerkunftsUndRueckbaudokumentation** (`nf_herkunfts_und_rueckbaudokumentation`) · conf 0.9 · 8 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_krwg gilt
  - src: https://www.gesetze-im-internet.de/krwg/__6.html
- **ZustandsUndMassaufnahme** (`nf_zustands_und_massaufnahme`) · conf 0.9 · 2 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_din_spec_91484 gilt
  - src: https://din.one/pages/viewpage.action?pageId=160465716
- **Bauphysiknachweis** (`nf_bauphysiknachweis`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Neubau-/Umbaukontext (['bai_umbau']); rw_geg gilt
  - src: https://www.gebaeudeforum.de/ordnungsrecht/geg/
- **GenehmigungsOderZustimmungsbedarf** (`nf_genehmigungs_oder_zustimmungsbedarf`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_vdi_6210 gilt
  - src: https://www.vdi.de/richtlinien/details/vdi-6210-blatt-1-abbruch-von-baulichen-und-technischen-anlagen
- **OekobilanzEPD** (`nf_oekobilanz_epd`) · conf 0.85 · 3 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_eu_taxonomy gilt
  - src: https://finance.ec.europa.eu/system/files/2023-06/taxonomy-regulation-delegated-act-2022-environmental_en_0.pdf
- **SchadstoffkatasterErkundung** (`nf_schadstoffkataster_erkundung`) · conf 0.85 · 2 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_vob_c_din_18459 gilt
  - src: https://www.deutscher-abbruchverband.de/publikationen/handlungshilfen-downloads/atv-din-18459/
  …(+4 more)

### UNTERLIEGT_REGELWERK (16)
- **DIN SPEC 91484** (`rw_din_spec_91484`) · conf 0.9 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_din_spec_91484 gilt
  - src: https://din.one/pages/viewpage.action?pageId=160465716
- **DIN SPEC 91525** (`rw_din_spec_91525`) · conf 0.9 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_din_spec_91525 gilt
  - src: https://www.dinmedia.de/en/technical-rule/din-spec-91525/397760893
- **EU Waste Framework Directive 2008/98/EC** (`rw_eu_wfd_2008_98`) · conf 0.9 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_eu_wfd_2008_98 gilt
  - src: https://eur-lex.europa.eu/legal-content/EN/LSU/?uri=CELEX:32008L0098
- **KrWG §6/§7/§8** (`rw_krwg`) · conf 0.9 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_krwg gilt
  - src: https://www.gesetze-im-internet.de/krwg/__6.html
- **EU C&D Waste Management Protocol (2024)** (`rw_eu_cdw_protocol`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_eu_cdw_protocol gilt
  - src: https://op.europa.eu/en/publication-detail/-/publication/d63d5a8f-64e8-11ef-a8ba-01aa75ed71a1/language-en
- **EU Taxonomy (Circular Economy TSC)** (`rw_eu_taxonomy`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Reuse-Projekt; rw_eu_taxonomy gilt
  - src: https://finance.ec.europa.eu/system/files/2023-06/taxonomy-regulation-delegated-act-2022-environmental_en_0.pdf
- **GEG** (`rw_geg`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Neubau-/Umbaukontext (['bai_umbau']); rw_geg gilt
  - src: https://www.gebaeudeforum.de/ordnungsrecht/geg/
- **Gewerbeabfallverordnung (GewAbfV)** (`rw_gewabfv`) · conf 0.85 · 1 rule(s)
  - why: Projekt in ['land_deutschland']; Rückbau-/Bestandskontext (['bai_umbau']); rw_gewabfv gilt
  - src: https://www.gesetze-im-internet.de/gewabfv_2017/BJNR089600017.html
  …(+8 more)


## [Bauwerk] `bw_ka13_existing_building` — KA13 Bestandsgebäude…

### TRIGGERS_REGULIERUNGSFRAGE (1)
- **SchadstoffFrage** (`rf_schadstoff_frage`) · conf 0.74 · 1 rule(s)
  - why: Bauwerk-Era ['era_nachkrieg_1945_1970'] -> typische Schadstoffe (graph TYPISCH_BEI_ERA)
  - src: https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024

### ERFORDERT_NACHWEIS (2)
- **AsbestCheck** (`nf_asbest_check`) · conf 0.74 · 1 rule(s)
  - why: Bauwerk-Era ['era_nachkrieg_1945_1970'] -> typische Schadstoffe (graph TYPISCH_BEI_ERA)
  - src: https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024
- **Schadstoffpruefung** (`nf_schadstoffpruefung`) · conf 0.74 · 1 rule(s)
  - why: Bauwerk-Era ['era_nachkrieg_1945_1970'] -> typische Schadstoffe (graph TYPISCH_BEI_ERA)
  - src: https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024

### UNTERLIEGT_REGELWERK (1)
- **GefStoffV (2024)** (`rw_gefstoffv`) · conf 0.74 · 1 rule(s)
  - why: Bauwerk-Era ['era_nachkrieg_1945_1970'] -> typische Schadstoffe (graph TYPISCH_BEI_ERA)
  - src: https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024


## Distributions

### Edges per Projekt (top 10)
- p_awm_muenster_circular_office (AWM Münster – zirkulärer…): 36 edges
- p_christ_pavilion_volkenroda (Christus-Pavillon): 36 edges
- p_crclr_house_impact_hub_berlin (CRCLR House): 36 edges
- p_impact_hub_berlin_crclr_fitout (Impact Hub Berlin): 36 edges
- p_plattenpalast_berlin (Plattenpalast Berlin): 36 edges
- p_plattenvereinigung_berlin (Plattenvereinigung Berlin): 36 edges
- p_bestandverplanzung_pavilion_muenchen (Bestandverplanzung…): 33 edges
- p_haus_hos_mehrfamilienhaus_muehlhausen (Haus HOS): 33 edges
- p_recyclinghaus_hannover (Recyclinghaus Hannover): 33 edges
- p_association_house_groeditz (Vereinshaus Gröditz): 25 edges

### TRIGGERS_REGULIERUNGSFRAGE by question
- BauproduktstatusFrage (rf_bauproduktstatus_frage): 262
- TragwerkssicherheitFrage (rf_tragwerkssicherheit_frage): 185
- BauphysikFrage (rf_bauphysik_frage): 136
- ReuseDokumentationFrage (rf_reusedokumentationfrage): 95
- UmweltvertraeglichkeitOekobilanzFrage (rf_umweltvertraeglichkeit_oekobilanz_frage): 85
- RueckbauUndBauteilernteFrage (rf_rueckbau_und_bauteilernte_frage): 84
- BrandschutzFrage (rf_brandschutz_frage): 79
- SchadstoffFrage (rf_schadstoff_frage): 63
- HygieneElektroFunktionFrage (rf_hygiene_elektro_funktion_frage): 22
- GenehmigungsFrage (rf_genehmigungs_frage): 19
- HaftungGewaehrleistungFrage (rf_haftung_gewaehrleistung_frage): 14

### ERFORDERT_NACHWEIS by proof (top 15)
- ProduktstatusUndLeistungserklaerung (nf_produktstatus_und_leistungserklaerung): 287
- Materialpruefung (nf_materialpruefung): 214
- U_WertOderEnergieInfo (nf_u_wert_oder_energie_info): 136
- Standsicherheitsnachweis (nf_standsicherheitsnachweis): 123
- HerkunftsUndRueckbaudokumentation (nf_herkunfts_und_rueckbaudokumentation): 84
- OekobilanzEPD (nf_oekobilanz_epd): 62
- MaterialpassRessourcenpass (nf_materialpass_ressourcenpass): 51
- Befestigungsnachweis (nf_befestigungsnachweis): 46
- Bauteilidentifikation (nf_bauteilidentifikation): 45
- SicherheitsglasInfo (nf_sicherheitsglas_info): 39
- SchadstoffkatasterErkundung (nf_schadstoffkataster_erkundung): 35
- DauerhaftigkeitRestlebensdauer (nf_dauerhaftigkeit_restlebensdauer): 31
- Bauphysiknachweis (nf_bauphysiknachweis): 25
- RcGesteinskoernungEignung (nf_rc_gesteinskoernung_eignung): 23
- ZustandsUndMassaufnahme (nf_zustands_und_massaufnahme): 23

### UNTERLIEGT_REGELWERK by law (top 15)
- ISO 20887 (Design for Disassembly/Adaptability) (rw_iso_20887): 84
- EN 13830 (Vorhangfassade/Curtain Walling) (rw_en_13830): 74
- ESPR / Digital Product Passport (rw_espr_dpp): 51
- EU Level(s) framework (rw_eu_levels): 51
- EU Taxonomy (Circular Economy TSC) (rw_eu_taxonomy): 51
- EN 1168 (Hohlplatten/Hollow-core slabs) (rw_en_1168): 48
- EN ISO 6892-1 (Zugversuch Metalle) (rw_en_iso_6892): 47
- EN 13791 / EN 12504 (In-situ Beton) (rw_en_13791_12504): 46
- fib Bulletins (precast concrete reuse) (rw_fib_precast_reuse): 46
- EN 771 (reclaimed masonry units) (rw_en_771_reclaimed): 46
- EN/DIN EN 1090 (rw_en_1090): 46
- CEN/TS 1090-201:2024 (rw_cen_ts_1090_201): 45
- EN 1090-2 / EN 14399 (bolt reuse limits) (rw_en_1090_2_bolts_reuse): 45
- EN 14351-1/-2 (Fenster & Türen) (rw_en_14351): 42
- Flat-glass / IGU reuse guidance (Glass for Europe) (rw_glas_reuse_igu): 39