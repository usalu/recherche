# Element-Proof Agent EP-02 — Actor-type & role-adjacent vocab

**Database:** `mit-bestand` (READ-ONLY)
**Date:** 2026-06-06
**Scope:** `HAT_AKTEURTYP`, `HAT_BAUOBJEKTROLLE`, `HAT_NUTZUNG`, `HAT_GESCHAEFTSMODELL`
**Ledger rows:** 1239 (live scope enumeration; plan target was 1238)

---

## 1. Scope recap

| rel_type | live count |
|---|---:|
| `HAT_AKTEURTYP` | 682 |
| `HAT_BAUOBJEKTROLLE` | 225 |
| `HAT_NUTZUNG` | 235 |
| `HAT_GESCHAEFTSMODELL` | 97 |
| **Σ** | **1239** |

Method: per-edge contract check (domain/range vs `get-schema` + controlled vocabulary seed). Tier-C mechanical proof — no web fetch. Each row attests **this specific edge**.

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | 1238 |
| SCHEMA_VIOLATION | 1 |

## 3. Domain/range rules enforced

| rel_type | domain (allowed) | range |
|---|---|---|
| `HAT_AKTEURTYP` | :Akteur | `:Akteurtyp` |
| `HAT_BAUOBJEKTROLLE` | :Bauwerk, :Materialdepot, :Projekt | `:Bauobjektrolle` |
| `HAT_NUTZUNG` | :Bauwerk, :Materialdepot, :Projekt | `:Nutzung` |
| `HAT_GESCHAEFTSMODELL` | :Akteur, :Software | `:Geschaeftsmodell` |

## 4. Worst findings

- **SCHEMA_VIOLATION** `stadt_zuerich` —[`HAT_AKTEURTYP`]→ `at_oeffentliche_institution` (domain labels ['Stadt']); cite A12-rel-0003 pattern for Stadt→Akteurtyp.

### name==id vocab stubs on targets

Zero in-scope targets with `name==id`. The eight A12 orphan stubs (bt_fassadenelement, …, mat_spannbeton) have **no** incoming classification edges in this shard.

## 5. Proposed actions summary

| proposed_action | Count |
|---|---:|
| KEEP | 1238 |
| ESCALATE_HUMAN | 1 |

## 6. Summary

Emitted **1239** element-level rows (`coverage_level=element`, `graph_element_id=elementId(r)`). **1238** edges fully domain/range-valid; **1** schema violations (1× `Stadt`→`HAT_AKTEURTYP`, remainder none). No aggregate rows. Prior A12 aggregate conclusions cited only in methodology; each row states its own edge claim.
