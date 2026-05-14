# 04 Query-Driven Review Plan

## Goal

Use graph queries to find cross-project inconsistencies that are invisible inside individual files.

## Chunk size

Run **one query theme per agent run**.

Limit output to:
```text
top 25 suspicious rows
max 250 patch operations
```

## Query themes

### Theme 1 — Direct structural reuse

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
WHERE bg.counts_as_direct_reuse = true
  AND bt.id IN ["bt_traeger","bt_stuetze","bt_decke","bt_wand","bt_fundament"]
RETURN p.id, p.name, bg.id, bg.name, collect(bt.name) AS types
ORDER BY p.name;
```

### Theme 2 — Material hub consistency

```cypher
MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
OPTIONAL MATCH (m)-[:HAT_MATERIALGRUPPE]->(mg:Materialgruppe)
RETURN m.id, m.name, collect(DISTINCT mg.name) AS groups, count(DISTINCT bg) AS bg_count
ORDER BY bg_count DESC;
```

### Theme 3 — Huerde consistency

```cypher
MATCH (bg:Bauteilgruppe)-[:HAT_HUERDE]->(h:Huerde)
OPTIONAL MATCH (h)-[:HAT_HUERDEKATEGORIE]->(hk:HuerdeKategorie)
RETURN h.id, h.name, collect(DISTINCT hk.name) AS categories, count(DISTINCT bg) AS bg_count
ORDER BY bg_count DESC;
```

### Theme 4 — Donor / receiver completeness

```cypher
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WHERE bg.counts_as_direct_reuse = true
OPTIONAL MATCH (bg)-[:AUS_BAUWERK]->(donor:Bauwerk)
OPTIONAL MATCH (bg)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
RETURN p.id, bg.id, donor.id AS donor, receiver.id AS receiver
ORDER BY p.id;
```

### Theme 5 — Planned vs realized reuse

```cypher
MATCH (p:Projekt)-[:HAT_STATUS]->(s:Status)
OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN p.id, p.name, collect(DISTINCT s.name) AS status, count(bg) AS component_groups
ORDER BY p.id;
```

## Output files

```text
query_review_<theme>.md
patches/query_<theme>.patch.jsonl
```

## Rule

Patch only clear inconsistencies. If the query indicates possible content error, mark as `SOURCE_CHECK`.
