# Scope audit after supranational Land fanout

Date: 2026-05-31

Purpose: check whether the post-migration GILT_IN_LAND links are factually supported by official web sources.

## Query used against Neo4j

```cypher
MATCH (source)-[:GILT_IN_LAND]->(land:Land)
WHERE source.id IN [
  'norm_en_1090','norm_en_1168','norm_en_13162','norm_en_14081',
  'norm_en_1992','norm_en_1993','norm_en_1995','norm_en_1996',
  'norm_en_206','norm_en_771','norm_cen_ts_17440','norm_cen_ts_1090_201_2024',
  'rb_ce_ukca_marking_reused_steel','rb_eu_taxonomie','ak_leed_zertifizierung'
]
OPTIONAL MATCH (source)-[:GILT_IN_LAND]->(land:Land)
RETURN source.id AS source_id, labels(source) AS labels, collect(land.id) AS land_ids
ORDER BY source_id;
```

## Live graph state checked

- norm_en_1090: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_1168: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_13162: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_14081: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_1992: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_1993: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Oesterreich, Portugal
- norm_en_1995: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_1996: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_en_206: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Oesterreich, Portugal
- norm_en_771: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- norm_cen_ts_17440: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Oesterreich, Portugal
- norm_cen_ts_1090_201_2024: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Oesterreich, Portugal
- rb_ce_ukca_marking_reused_steel: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal, Vereinigtes_Koenigreich
- rb_eu_taxonomie: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Oesterreich, Portugal
- ak_leed_zertifizierung: USA

Relevant Land nodes present in graph: Belgien, Daenemark, Deutschland, Finnland, Frankreich, Italien, Luxemburg, Niederlande, Norwegen, Oesterreich, Portugal, Schweiz, Ukraine, USA, Vereinigtes_Koenigreich, Japan.

## Official source findings

### 1. EN standards are not EU-only

Official source: CEN-CENELEC, European Standards

Source URL: https://www.cencenelec.eu/european-standardization/european-standards/

Key wording:

> A European Standard (EN) is implemented by the national CEN and CENELEC Members as a national standard, and therefore is included in the standards catalogue of CEN and CENELEC's Members, the National Standardization Organizations in 34 countries.

Audit implication:

- Generic EN nodes should not have been redistributed only to EU countries.
- In the current graph, UK and Switzerland exist as Land nodes but are missing from all audited EN nodes.
- Norway exists as a Land node but is missing from most audited EN nodes.

### 2. Eurocodes are broader than EU-only and include UK

Official source: JRC Eurocodes portal

Source URL: https://eurocodes.jrc.ec.europa.eu/

Key wording:

> The Eurocodes are adopted in the 31 EU/EFTA Member States and the United Kingdom.

Audit implication:

- EN 1992, EN 1993, EN 1995 and EN 1996 should not be modeled as applying only to the EU subset currently linked.
- At minimum, UK and Switzerland are missing from the current graph.
- Norway should be handled consistently across all Eurocode nodes if GILT_IN_LAND means national applicability.

### 3. Harmonised CPR standards are EU-law / EEA relevant, not a generic country proxy

Official sources:

- European Commission, Harmonised standards: https://single-market-economy.ec.europa.eu/sectors/construction/construction-products-regulation-cpr/harmonised-standards_en
- EUR-Lex, Regulation (EU) 2024/3110: https://eur-lex.europa.eu/eli/reg/2024/3110/oj/eng

Key wording:

> Harmonised European standards provide a technical basis to assess the performance of construction products. They enable manufacturers to draw up the Declaration of Performance as defined in the Construction Products Regulation, and affix the CE marking.

> Regulation (EU) 2024/3110 ... (Text with EEA relevance)

Audit implication:

- CPR / CE scope is a legal-market regime tied to the Union market and EEA relevance.
- That is not the same thing as an EN being a national standard in CEN member countries.
- A single node that mixes CE and UKCA compresses two different territorial regimes.

### 4. UK construction products are not covered by an EU-only assumption

Official sources:

- GOV.UK, Placing UKCA or CE marked products on the market in Great Britain: https://www.gov.uk/guidance/using-the-ukca-marking
- GOV.UK, Construction Products Regulation in Great Britain: https://www.gov.uk/guidance/construction-products-regulation-in-great-britain

Key wording:

> The UK continues to recognise the CE marking, alongside or in place of the UKCA marking, for the Great Britain market.

> Upon EU Exit all existing harmonised European standards became UK designated standards.

> Accepted markings for the GB market ... Construction product being supplied to the GB market: UKCA or CE or CE & UK(NI)

Audit implication:

- UK should not disappear from EN-related construction-product reasoning.
- If the graph wants legal applicability, Great Britain needs explicit handling.
- If the graph wants national-standard presence, UK is also relevant because former harmonised standards became UK designated standards.

### 5. France-specific reuse evidence exists, but it does not justify blanket EU fanout

Official source: CTICM

Source URL: https://www.cticm.com/nouvelle-parution-recommandations-professionnelles-reemploi-delements-structuraux-en-acier/

Key wording:

> Selon la NF EN 1090-2, il est possible d'utiliser des produits de structure en acier ...

> ... l'utilisateur du produit de reemploi ... peut ... le dimensionner avec les methodes definies dans le corpus des Eurocodes.

Audit implication:

- This supports France-specific reuse use of EN 1090-2 and Eurocodes.
- It does not prove that EU-only fanout was the correct model.

### 6. Belgium evidence points to evolving reuse standardization, not automatic country fanout

Official source: Buildwise

Source URL: https://www.buildwise.be/fr/nouvelles/reemploi-des-produits-de-construction/

Key wording:

> Une norme europeenne en cours d'elaboration

> ... definissant des exigences horizontales applicables au reemploi des produits de construction.

Audit implication:

- For reuse-specific CEN work such as CEN/TS 17440, country scope should be proven directly, not inherited from deleted supranational Land nodes.

## Verdict by node group

| Node group | Current graph | Official finding | Verdict | Likely correction |
| --- | --- | --- | --- | --- |
| norm_en_1090, norm_en_1168, norm_en_13162, norm_en_14081, norm_en_206, norm_en_771 | 10 EU countries only | EN is implemented as national standard in 34 countries | Incorrect / incomplete | If GILT_IN_LAND means national standard presence, add at least UK, Switzerland, and likely Norway where relevant; otherwise remodel scope semantics |
| norm_en_1992, norm_en_1993, norm_en_1995, norm_en_1996 | 10 or 11 countries, partial Norway only | Eurocodes adopted in 31 EU/EFTA states and UK | Incorrect / incomplete | Add at least UK and Switzerland; make Norway consistent; consider broader Eurocode country modeling |
| norm_cen_ts_17440, norm_cen_ts_1090_201_2024 | 11 countries including Norway | No official source collected here proving this exact country set | Unproven | Do not keep EU/EEA fanout as if it were demonstrated; gather a dedicated source or remodel as supranational/standardization-scope metadata |
| rb_ce_ukca_marking_reused_steel | EU 10 + UK, no Norway | CPR has EEA relevance; Great Britain accepts CE or UKCA | Mixed and under-modeled | Split into CE/CPR (EU/EEA) and UKCA/GB, or at minimum add Norway if one mixed node is retained |
| rb_eu_taxonomie | 10 EU countries | EU Taxonomy is an EU regulation / EU classification system | Broadly correct for the current EU-country subset in graph | Keep EU-only semantics; only extend if more EU Land nodes are added |
| ak_leed_zertifizierung | USA only | This audit did not get a clean public official LEED scope page, but repo archive and earlier graph state treated LEED as international | User-driven simplification, not proven USA-only | Leave as-is only if the intentional simplification should remain; otherwise restore a non-country international scope model |

## Bottom line

The migration fixed the graph-shape problem of storing EU, EEA and International as Land nodes, but it did not preserve correct applicability semantics.

The strongest proven mismatch is this:

- EN-based nodes are not EU-only.
- Eurocodes are not EU-only and explicitly include UK plus EU/EFTA states.
- CPR / CE scope is a different concept from EN national-standard scope.

Therefore the current post-migration country fanout should not be treated as factually correct.

## Recommended follow-up

1. Keep rb_eu_taxonomie as EU-only.
2. Split rb_ce_ukca_marking_reused_steel into separate legal-scope nodes unless a deliberate mixed abstraction is required.
3. Correct EN and Eurocode nodes so they are not modeled as EU-only.
4. Revisit CEN/TS nodes only after a dedicated source confirms country handling.
5. Prefer a future model that distinguishes:
   - national-standard adoption scope
   - EU/EEA legal market scope
   - UK-specific legal scope
   - international / non-country certification scope