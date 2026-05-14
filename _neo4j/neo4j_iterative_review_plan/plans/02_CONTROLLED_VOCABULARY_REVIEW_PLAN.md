# 02 Controlled Vocabulary Review Plan

## Goal

Normalize shared hub nodes so the graph becomes more connected and easier to query.

## Chunk size

Review **one vocabulary family per run**.

Recommended maximum:
```text
100 controlled nodes per run
250 patch operations per file
```

If a family is larger, split alphabetically or by parent category.

## Families to review

1. Material + Materialgruppe
2. Bauteiltyp + Bauteilebene
3. Huerde + HuerdeKategorie
4. Akteurrolle + Akteurtyp
5. Bauobjektrolle + Bauobjektklasse
6. Status + WiederverwendungsArt
7. Stadt + Land
8. Norm + PruefungNachweis + Leistungsanforderung
9. Methode + Rueckbauverfahren + Aufbereitungsverfahren
10. ZertifizierungBewertungssystem + Programm + Tool + Software

## What to look for

```text
same id, different name
same concept, different ids
too-specific term that should be alias
too-generic term that hides useful distinction
term modeled as property but should be node
term modeled as node but should be scalar property
missing parent relationship
```

## Canonicalization rules

Prefer:
```text
German schema label names
stable lowercase snake_case ids
one canonical display name
aliases for source spelling variants
parent-category links for low-frequency terms
```

Examples:
```json
{"op":"canonicalize_node","id":"mat_textil","canonical_name":"Textil","aliases":["Textil / textile Fasern","Textil / Filz / textile Fasern"],"reason":"normalize textile material names","severity":"LOW"}
{"op":"merge_node","from":"land_uk","to":"land_vereinigtes_koenigreich","reason":"duplicate country term","severity":"MEDIUM"}
{"op":"add_rel","from":"h_schadstoffbelastung","type":"HAT_HUERDEKATEGORIE","to":"hk_umwelt_gesundheit","properties":{},"reason":"hurdle requires parent category","severity":"MEDIUM"}
```

## Output files

```text
controlled_vocabulary_review_<family>.md
patches/controlled_vocabulary_<family>.patch.jsonl
registry/canonical_nodes.patch.jsonl
```

## Human decision categories

```text
ACCEPT
REJECT
NEEDS_SOURCE_CHECK
DEFER
```
