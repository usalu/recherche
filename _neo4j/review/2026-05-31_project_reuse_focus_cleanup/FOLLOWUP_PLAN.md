# Follow-up plan — post 2026-05-31 project reuse-focus cleanup

Planned 2026-06-01. Three follow-ups left open after the 105-mutation apply
(208 deletes + 8 merges + 6 label strips + 1 rename) on `mit-bestand`:

- **F1.** Rewrite hard-coded `:Projekt` queries so dashboards/audits cover the
  6 newly stripped `:Programm` canonicals (`prog_fcrbe`, `prog_re_use_hoefe`,
  `prog_rebridge`, `prog_stuttgart_210`, `prog_reallabor_be_ware`, `prog_mas_dfab`).
- **F2.** Regenerate `_neo4j/review/2026-05-31_project_direct_topology_export_mit-bestand/`
  (snapshot pre-dates the apply, no generator script in repo).
- **F3.** Add advisory banners to `REVIEW_BASED_PLAN.md` and
  `FINAL_REVIEW_PLAN_AUDIT.md`.

Order: **F1 first** (without it, F2 regeneration shows wrong counts and the
docs we update in F3 cite stale numbers). Estimated total touch: 5 files
edited + 1 new generator script + 1 regenerated artefact + 2 doc edits.

---

## F1 — Query rewrites (16 hits across 6 production scripts)

Source-of-truth row table:
[dependency_fixes/hard_coded_projekt_query_audit.csv](dependency_fixes/hard_coded_projekt_query_audit.csv).
Scratch/baseline-frozen rows are out of scope (annotate-only).

### F1.a — Gap survey: split `:Projekt` checks into `:Projekt` + `:Programm` where applicable

File: [_scripts/_gap_survey.py](../../../_scripts/_gap_survey.py) (lines 55–73 + 71)

Decision per check (KEY: "P-only" = leave on `:Projekt`; "split" = add a
sibling `:Programm` row):

| Line | Check | Decision | Rationale |
|---|---|---|---|
| 55 | `Projekt missing LIEGT_IN_STADT` | **P-only** | Programmes can be multi-city / non-located. |
| 56 | `Projekt missing LIEGT_IN_LAND` | **P-only** | FCRBE spans NWE; "missing land" is not a defect. |
| 57 | `Projekt missing HAT_INTERVENTION` | **P-only** | Intervention is project-level. |
| 58 | `Projekt missing HAT_NUTZUNG` | **P-only** | Building usage is project-level. |
| 59 | `Projekt missing HAT_METHODE` | **split** | Both project and programme can attach methods. |
| 60 | `Projekt missing NUTZT_BAUWERK` | **P-only** | Programme is not a building. |
| 61 | `Projekt missing TEIL_VON_PROGRAMM` | **P-only** by definition. |
| 71 | `Programm missing properties (type)` | **already P-only on `:Programm`** | unchanged. |
| 73 | `Projekt name > 25 chars` | **split** | Naming hygiene applies equally. |

Pattern for "split" rows (add ONE new line below the existing check, do not
touch the existing line):

```python
('Programm missing HAT_METHODE', 'MATCH (p:Programm) WHERE NOT EXISTS { (p)-[:HAT_METHODE]->() } RETURN count(p) AS c', None),
('Programm name > 25 chars',     'MATCH (p:Programm) WHERE size(p.name) > 25 RETURN count(p) AS c',                       None),
```

### F1.b — Build review dashboard: add Programm siblings to coverage counts

File: [_scripts/run_neo4j_current_build_review.py](../../../_scripts/run_neo4j_current_build_review.py) (lines 267–325)

`queries` dict ([line 260](../../../_scripts/run_neo4j_current_build_review.py)):

| Line | Existing key | Decision |
|---|---|---|
| 267 | `projects` | **add sibling** `programmes` query |
| 268 | `projects_no_source` | **add sibling** `programmes_no_source` |
| 269 | `projects_no_component_or_work` | **P-only** (programmes don't carry components) |
| 322 | `projects_without_component_or_work` listing | **P-only** (same reason) |

Concrete additions (insert next to each existing key, do not rewrite the
existing ones):

```python
"programmes":           "MATCH (p:Programm) RETURN count(p) AS c",
"programmes_no_source": "MATCH (p:Programm) WHERE NOT (p)-[:BELEGT_IN]->(:Quelle) RETURN count(p) AS c",
```

The downstream consumer reads `result["checks"]` as a flat dict; no schema
change needed.

### F1.c — Page/link/image generation: include Programmes

Three near-identical scripts each have a `MATCH (p:Projekt)` query around
line 28–44 that drives page generation. After the cleanup, programmes are
legitimate page content (FCRBE, ReBridge, Stuttgart 210 etc. each merit a
page). All three queries should be expanded with a label union.

Files + line numbers:
- [_scripts/generate_page_links.py:36](../../../_scripts/generate_page_links.py)
- [_scripts/generate_project_links.py:28](../../../_scripts/generate_project_links.py)
- [_scripts/generate_review_lists.py:36](../../../_scripts/generate_review_lists.py)

Rewrite pattern (same delta in all three):

```cypher
// old
MATCH (p:Projekt) WHERE p.name IS NOT NULL ...

// new
MATCH (p) WHERE (p:Projekt OR p:Programm) AND p.name IS NOT NULL ...
```

The downstream consumers only read `p.id`, `p.name`, and the OPTIONAL
MATCH'd `(s:Stadt)`, `(l:Land)`, `(a:Akteur)`, `(n:Nutzung)` — programmes
don't always have `(s:Stadt)`/`(l:Land)` but the OPTIONAL pattern already
handles that (returns nulls). Page sanitizer (`sanitize_filename`) handles
the new ids cleanly.

### F1.d — Image harvester: include Programmes

File: [_scripts/harvest_project_images.py:44](../../../_scripts/harvest_project_images.py)

Same rewrite as F1.c. Programmes can have hero images (FCRBE has a logo;
Stuttgart 210 has pavilion photos). Run the harvester after the rewrite
lands to populate images for the 6 new programme pages.

### F1 — Acceptance

After all four sub-fixes, run the following sanity check (read-only):

```powershell
$env:NEO4J_DATABASE='mit-bestand'
python _scripts/_gap_survey.py
python _scripts/run_neo4j_current_build_review.py --out /tmp/post_cleanup_review.json
```

Expected: `projects` count = 86, `programmes` count = 29; `programmes_no_source`
should be a small number (most programmes have at least their own dossier).

---

## F2 — Topology export regeneration

The 2026-05-31 snapshot was generated ad-hoc; there is no generator script
in the repo. The README documents the format (elementId + labels for nodes;
elementId + type + source/target for edges, no property bags).

### F2.a — Add the generator script (NEW file)

Create `_scripts/export_projekt_programm_topology.py`. Pattern matches
`_scripts/export_neo4j_schema.py` for connection handling (reuses
[`neo4j_env.resolve_connection`](../../../_scripts/neo4j_env.py)).

Scope change vs the 2026-05-31 export: anchor on `:Projekt|:Programm` (not
just `:Projekt`) so the export covers the relabeled programmes and any
future label additions.

Cypher (parameterised, READ access):

```cypher
// All anchor nodes
MATCH (p) WHERE p:Projekt OR p:Programm
WITH collect(elementId(p)) AS anchor_ids

// All directly-adjacent nodes + edges
MATCH (a)-[r]-(b) WHERE elementId(a) IN anchor_ids
RETURN
  collect(DISTINCT {id: elementId(a), labels: labels(a)}) AS anchors,
  collect(DISTINCT {id: elementId(b), labels: labels(b)}) AS neighbours,
  collect(DISTINCT {id: elementId(r), type: type(r),
                    source: elementId(startNode(r)), target: elementId(endNode(r))}) AS edges
```

Output JSON shape matches the existing `project_direct_topology.nodes_edges_only.json`
exactly (so downstream readers don't need code changes).

### F2.b — Regenerate the artefact

Create new dated directory:
`_neo4j/review/2026-06-01_projekt_programm_topology_export_mit-bestand/`

Run:

```powershell
$env:NEO4J_DATABASE='mit-bestand'
python _scripts/export_projekt_programm_topology.py `
  --out _neo4j/review/2026-06-01_projekt_programm_topology_export_mit-bestand/topology.nodes_edges_only.json
```

Write a fresh `README.md` that:
- States the scope is `:Projekt|:Programm` (changed from prior `:Projekt`-only).
- Lists counts + apply date (2026-05-31).
- Links to this follow-up plan and to the snapshot rollback location.

### F2.c — Mark the 2026-05-31 export as superseded

Edit [_neo4j/review/2026-05-31_project_direct_topology_export_mit-bestand/README.md](2026-05-31_project_direct_topology_export_mit-bestand/README.md) — single sentence at the top:

```markdown
> **SUPERSEDED 2026-06-01.** This snapshot pre-dates the project reuse-focus
> cleanup applied 2026-05-31. 7 projects deleted + 8 merged + 6 :Projekt
> labels stripped to :Programm. See
> [_neo4j/review/2026-06-01_projekt_programm_topology_export_mit-bestand/](../2026-06-01_projekt_programm_topology_export_mit-bestand/)
> for the current snapshot.
```

Do NOT delete or rewrite the old snapshot — it remains a valid 2026-05-31
historical reference.

### F2 — Acceptance

The new JSON contains:
- Anchor count = 86 (Projekt) + 29 (Programm) = 115.
- No node has the id `4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:<X>` matching
  any of the 7 deleted projects' element ids from the 2026-05-31 snapshot
  (verifies the regeneration is post-cleanup).
- Edges referencing the deleted ids do not appear.

---

## F3 — Doc banners on REVIEW_BASED_PLAN + FINAL_REVIEW_PLAN_AUDIT

Both docs predate this cleanup and treat `:Projekt` counts as authoritative.
Draft already exists at
[dependency_fixes/docs_audit_note.md](dependency_fixes/docs_audit_note.md).

### F3.a — Add advisory at top of REVIEW_BASED_PLAN.md

File: [_neo4j/REVIEW_BASED_PLAN.md](../../REVIEW_BASED_PLAN.md)

Insert directly under the existing `**Replaces:** ...` line (around line 7):

```markdown
> **2026-06-01 advisory (post project reuse-focus cleanup):** project-level
> entities are now split across `:Projekt` (86 nodes — built reuse projects),
> `:Programm` (29 nodes — research / funded programmes; gained 6 from a
> 2026-05-31 strip), `:Tool` / `:Software` (reclamation tools), and
> `:Marktmodell` (component-exchange marketplaces / Baubörsen). All counts
> and gap-audits below that say "projects" are scoped to `:Projekt` ONLY.
> For a holistic view, add a sibling `:Programm` count. Cleanup ledger:
> [`_neo4j/review/2026-05-31_project_reuse_focus_cleanup/MANUAL_REVIEW_CHECKPOINT.md`](review/2026-05-31_project_reuse_focus_cleanup/MANUAL_REVIEW_CHECKPOINT.md).
```

### F3.b — Same advisory on FINAL_REVIEW_PLAN_AUDIT.md

File: [_neo4j/FINAL_REVIEW_PLAN_AUDIT.md](../../FINAL_REVIEW_PLAN_AUDIT.md)

Insert near the top (after the title/metadata block). Same advisory; one
addition specific to the audit doc:

```markdown
> Audit gates that test `MATCH (p:Projekt)` continue to be valid as-is for
> built-reuse coverage. For programme coverage, run sibling queries with
> `MATCH (p:Programm)`.
```

### F3 — Acceptance

`grep -n "2026-06-01 advisory" _neo4j/REVIEW_BASED_PLAN.md _neo4j/FINAL_REVIEW_PLAN_AUDIT.md`
returns 2 hits (one per file).

---

## Apply order (recap)

1. **F1.a** + **F1.b** + **F1.c** + **F1.d** — edit 6 scripts.
2. **F1 acceptance check** — `_gap_survey.py` + `run_neo4j_current_build_review.py`.
3. **F2.a** — write `_scripts/export_projekt_programm_topology.py`.
4. **F2.b** — run, produce `2026-06-01_projekt_programm_topology_export_mit-bestand/`.
5. **F2.c** — annotate the 2026-05-31 export README.
6. **F3.a** + **F3.b** — add advisory banners.
7. **Final sanity** — `git status` should show: 6 edited `_scripts/*.py`,
   1 new generator script, 1 new export directory, 2 edited `*.md` plus the
   2026-05-31 README annotation.

## Out of scope

- Re-running the 2026-05-28 source/actor/Bauteilboersen hygiene runs.
- Touching the `dependency_fixes/` CSV (it is the source-of-truth for F1
  per-line decisions; this plan distils it into action).
- Resolving prior-pass open issues (Q1 Reuse Story inflation, Layer demotion,
  ReuseRule edges, Quelle citation verification) — those have their own R1–R10
  phases in `REVIEW_BASED_PLAN.md`.
- Creating donor `:Bauwerk` stubs for MedUni Campus Mariannengasse (still
  open per [MANUAL_REVIEW_CHECKPOINT.md U2](MANUAL_REVIEW_CHECKPOINT.md)).
