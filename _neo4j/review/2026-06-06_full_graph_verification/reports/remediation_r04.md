# Remediation R04 — Madaster / RAU Identity (Wave 2)

**Agent:** R04 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Input:** Agent 03/05/06b/14 ledger rows · **Output ledger:** [`ledger/remediation_r04.csv`](../ledger/remediation_r04.csv)
**Patch:** [`patches/remediation_r04_madaster_rau_harvestmap.patch.jsonl`](../patches/remediation_r04_madaster_rau_harvestmap.patch.jsonl)

## Executive answer

**Is `rau` the same as `thomas_rau`?** **No.** Web evidence (strict gate) shows they are **distinct entities**:

| Node | Graph type | Web identity |
|---|---|---|
| `thomas_rau` | `at_person` | Thomas Rau, architect and Madaster co-initiator |
| `rau` | `at_unternehmen` | RAU — architectural firm operating since 1992 |

The prior campaign treated `rau` as a shorthand duplicate of the person because the node sourced `thomasrau.eu/en` (personal homepage) and carried `source_titles: Thomas Rau`. That conflation blocked safe bidirectional-edge dedup for the two remaining `madaster↔*` pairs.

## Summary

| Metric | Count |
|---|---:|
| Ledger rows | 10 |
| PROVEN (apply-ready) | 8 |
| ESCALATE_HUMAN (deferred) | 1 |
| Patch ops | 7 |
| `delete_rel` | 4 |
| `set_rel_properties` | 1 |
| `set_node_properties` | 1 |
| `merge_node` | 1 |

## Evidence fetches (strict gate)

| URL | HTTP | Used for |
|---|---|---|
| `https://thomasrau.eu/en` | 200 | Person identity; Madaster founded 2017 |
| `https://thomasrau.eu/en/initiatives/rau` | 200 | RAU architectural firm (since 1992) |
| `https://thomasrau.eu/en/initiatives/madaster` | 200 | Thomas + Sabine initiated Madaster registry |
| `https://madaster.com/inspiration/from-material-passport-to-building-passport-and-what-about-a-product-passport` | 200 | Founder names Thomas Rau + Sabine Oberhuber |
| `https://madaster.com/about/` | 404 | Not used |
| `https://circulareconomy.europa.eu/.../madaster` | 200 | Platform description (no founder detail) |
| `https://www.materialnomaden.at/about` | 200 | HarvestMAP Vienna operates re:store |
| `https://www.oogstkaart.nl/` | login wall | NL Superuse tool is separate (`tool_oogstkaart_harvest_map`) |

## Decisions

### 1. Identity: `rau` vs `thomas_rau` → **KEEP separate**

- **Verdict:** CONTRADICTION of duplicate hypothesis (PROVEN distinct).
- **Action:** No `merge_node`. Fix `rau` sourcing to firm page.
- **Deferred:** `rau` vs `rau_architects` — both `at_unternehmen`; human should confirm whether to merge (R04-escalate-001).

### 2. Bidirectional pairs `madaster↔rau` and `madaster↔thomas_rau`

| Edge | Verdict | Action |
|---|---|---|
| `madaster→rau` | UNSUPPORTED | **DELETE** — evidence names Thomas Rau (person), not RAU firm |
| `rau→madaster` | UNSUPPORTED | **DELETE** — reverse leg |
| `madaster→thomas_rau` | SCHEMA_VIOLATION (bidirectional) | **DELETE** reverse leg |
| `thomas_rau→madaster` | PROVEN | **KEEP** + add `evidence_*` from Madaster initiatives page |

After apply: one canonical `thomas_rau→madaster` edge with on-graph evidence.

### 3. `rau→thomas_rau` edge

- **Verdict:** UNSUPPORTED as `VERBUNDEN_MIT_AKTEUR` (wrong semantics; no URL names both as affiliated peers).
- **Action:** **DELETE**. Proper founder↔firm relationship is out of scope for auto-patch → ESCALATE_HUMAN.

### 4. `harvestmap` stub

- **Verdict:** CONTRADICTION — stub is **not** the NL Superuse Oogstkaart (`tool_oogstkaart_harvest_map` already exists).
- **Proof:** materialnomaden.at/about — *"Der re:store – Plattform & online store wird von **HarvestMAP Vienna** betrieben"*.
- **Action:** **MERGE_DUPLICATE** `harvestmap` → `re_store_harvestmap_vienna` (canonical AT node with `restore.or.at` sources and proven `BETRIEBEN_VON materialnomaden`).

## Apply result

**Live apply 2026-06-06:** 7 ops · **0 errors** · graph **2 295 nodes / 15 327 rels** (was 2 296 / 15 338).

Apply report: [`apply_reports/remediation_r04_madaster_rau_harvestmap.patch.apply_report.md`](../apply_reports/remediation_r04_madaster_rau_harvestmap.patch.apply_report.md)

## Patch (unambiguous — dry-run passed)

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r04_madaster_rau_harvestmap.patch.jsonl
```

Live apply requires:

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r04_madaster_rau_harvestmap.patch.jsonl \
  --confirm "APPLY remediation_r04_madaster_rau_harvestmap.patch.jsonl TO mit-bestand"
```

## Post-apply expectations

- **0** bidirectional `madaster↔rau` / `madaster↔thomas_rau` pairs remain.
- **1** evidenced `thomas_rau→madaster` edge.
- `harvestmap` node absorbed into `re_store_harvestmap_vienna` (incident edges redirected).
- `rau` remains as firm node with corrected `primary_source_url`.

Generated 2026-06-06 (Remediation Wave 2, Agent R04).
