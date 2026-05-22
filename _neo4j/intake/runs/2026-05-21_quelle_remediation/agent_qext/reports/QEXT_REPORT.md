# Q-EXT Run Report — Universal Source Surfacing
**Date:** 2026-05-22  
**Phase ID:** Q-EXT.A / Q-EXT.B / Q-EXT.C  
**Runner:** `agent_qext/logs/qext_runner.py`

---

## Summary

| Phase | Status | Key result |
|---|:---:|---|
| Q-EXT.A — Research folder URL ingestion | ✅ | 3 353 markdown files scanned; **11 612 URLs** ingested → ExternalLink nodes |
| Q-EXT.B — Universal source_urls | ✅ | **54 labels** processed; **2 420 domain nodes** stamped with `source_urls` |
| Q-EXT.C — primary_source_url | ✅ | All nodes with `source_urls > 0` now have `primary_source_url` (0 missing) |
| QE-2 — DataIssue backlog | ✅ | **921 `:DataIssue`** nodes emitted (kind: `node_no_source_url`, severity: low) |

---

## Acceptance Gates

| Gate | Expected | Actual | Pass? |
|---|---|---|:---:|
| ResearchDocument count ≥ 201 | ≥ 201 | **403** | ✅ |
| `MATCH (n:Material) WHERE n.source_urls IS NULL` | 0 | **0** | ✅ |
| `mat_stahl` source_count ≥ 1, primary_source_url non-null | ≥ 1, non-null | **8 sources**, primary set | ✅ |
| nodes with `source_urls > 0` AND `primary_source_url IS NULL` | 0 | **0** | ✅ |

---

## Source Coverage by Label (post Q-EXT.B)

| Label | Nodes with source_urls | avg sources | max |
|---|---|---|---|
| Akteur | 648 | 7.1 | 60 |
| Bauteilgruppe | 369 | 10.0 | 19 |
| Kennwert | 258 | 0 | 0 |
| Bauwerk | 186 | 9.9 | 27 |
| PruefungNachweis | 120 | 9.3 | 23 |
| Norm | 103 | 0.2 | 10 |
| Projekt | 101 | 8.0 | 19 |
| RechtlicheBedingung | 15 | **97** | 107 |
| Zertifizierungssystem | 8 | 11.3 | 32 |
| … (46 more) | | | |

Labels with avg=0 (controlled vocabulary, not cited): Kennwert, Huerde, Akteurrolle, Schadstoff, etc. — tracked via DataIssue backlog.

---

## Spot Check

```
:Material {id: 'mat_stahl'}
  primary_source_url: https://lendager.com/project/resource-rows
  source_count:       8
  source_urls:        [8 URLs including nen.nl/cen-ts-1090, recreate-project.eu, archdaily.com, …]
```

---

## Flags written

- `agent_qext/PHASE_QEXT_A_DONE.flag`
- `agent_qext/PHASE_QEXT_B_DONE.flag`
- `agent_qext/PHASE_QEXT_C_DONE.flag`

---

## Rollback

```cypher
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_b_source_urls'
REMOVE n.source_urls, n.source_count, n.source_urls_updated_at;

MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_c_primary_source_url'
REMOVE n.primary_source_url;

MATCH (e:ExternalLink) WHERE e.migration_origin = 'mig_qext_a_research_urls'
DETACH DELETE e;

MATCH (di:DataIssue) WHERE di.migration_origin = 'mig_qext_b_source_urls'
DETACH DELETE di;
```
