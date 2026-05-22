# Quality Pass Q01 — Schema & Structural

**Agent:** Q1 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Patch:** [`patches/quality_pass_q01.patch.jsonl`](../patches/quality_pass_q01.patch.jsonl)
**Apply report:** [`apply_reports/quality_pass_q01.patch.apply_report.json`](../apply_reports/quality_pass_q01.patch.apply_report.json)
**Ledger:** [`ledger/quality_pass_q01.csv`](../ledger/quality_pass_q01.csv)

---

## Summary

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 2,289 | 2,281 | −8 |
| Relationships | 15,324 | 15,289 | −35 |

**Scope items:** 14 applied + 1 deferred (unsafe FIX_PROPERTY)

| Group | Items | Result |
|---|---:|---|
| EP02 schema fix | 1 | `delete_rel` duplicate Stadt→`HAT_AKTEURTYP` |
| EP08 vocab deprecate | 8 | `merge_node` into curated targets |
| FIX_PROPERTY (safe) | 5 | Already live via `fix_property.patch.jsonl`; ledger reconciled |
| FIX_PROPERTY (unsafe) | 1 | `A10-N-058` deferred — name/source mismatch |

Evidence gate unchanged: no new URLs, no `BELEGT_IN` / synthetic quellen.

---

## 1. EP02 — `stadt_zuerich` domain violation

**Claim:** `EP02-rel-00562` — `stadt_zuerich` —[`HAT_AKTEURTYP`]→ `at_oeffentliche_institution`

**Fix:** Deleted the edge. The canonical classification already exists on `:Akteur` `stadt_zuerich_amt_hochbauten` (`EP02-rel-00563`, PROVEN).

**Rationale:** `HAT_AKTEURTYP` domain is `:Akteur` only; geographic `:Stadt` nodes must not carry actor-type edges (Agent 12 / EP-02).

---

## 2. EP08 — eight orphan vocab stubs

Regulation edges were redirected via `merge_node` before stub deletion (per R05 / EP-08).

| Stub | Merge target | R05 rationale |
|---|---|---|
| `bt_fassadenelement` | `bt_fassade` | 100% reg duplicate |
| `bt_fassadenmodul_mauerwerk` | `bt_fassade` | Best curated sibling (71% overlap) |
| `bt_glasscheibe` | `bt_verglasung` → then `bt_verglasung` → `bt_fenster` | Pairwise duplicate then canonical glazing parent |
| `bt_hohlkoerperdecke` | `bt_decke` | Semantic parent (hollow-core slab) |
| `bt_mauerstein` | `bt_fassade` | Best curated sibling |
| `bt_verglasung` | `bt_fenster` | Canonical glazing Bauteiltyp |
| `mat_drahtglas` | `mat_glas` | Wired-glass subtype → parent material |
| `mat_spannbeton` | `mat_beton` | 100% reg subset |

**Net effect:** 8 nodes removed; duplicate regulation paths collapsed onto curated anchors. Aliases preserved on survivors (e.g. `Glasscheibe`, `Spannbeton`).

**Follow-up (off-graph):** Update `build_vocabulary_graph.py` `TYPE_BY_RW` / `MAT_BY_RW` to drop deprecated stub ids when that script is next touched.

---

## 3. FIX_PROPERTY — element-proof backlog

Five safe fixes were already applied on 2026-06-06 via [`fix_property.patch.jsonl`](../patches/fix_property.patch.jsonl). Q01 reconciled ledger verdicts:

| claim_id | Fix | New verdict |
|---|---|---|
| `A14-RELKEY-001` | `nutzung_role` → `role` | PROVEN |
| `A14-RELKEY-002` | `bauwerk_role` → `role` | PROVEN |
| `A14-NODEKEY-002` | Drop TODO marker keys on `mobius_reemploi` | PROVEN |
| `09-node-0191` | `land_liechtenstein.country_iso2=LI` | PROVEN |
| `09-node-0342` | Paso Robles lat/lng | PROVEN |

**Deferred:** `A10-N-058` (`prog_mas_dfab`) — cited URL describes Catherine De Wolf's course, not MAS DFAB/Gramazio Kohler. Requires evidence realignment, not property-only patch.

---

## 4. Post-apply checks

- `stadt_zuerich` —[`HAT_AKTEURTYP`]→ * : **0** edges
- `stadt_zuerich_amt_hochbauten` —[`HAT_AKTEURTYP`]→ `at_oeffentliche_institution` : **1** edge
- All eight stub node ids: **absent** from live graph
- `VERIFICATION_LEDGER_ELEMENT.csv`: **14** scope rows updated to `REMEDIATED` / `PROVEN` + `APPLIED`

---

## Apply command (executed)

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/quality_pass_q01.patch.jsonl \
  --confirm "APPLY quality_pass_q01.patch.jsonl TO mit-bestand"
```

Dry-run was clean (0 load errors, 0 rejected ops) before live apply.
