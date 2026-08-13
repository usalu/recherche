# Handoff: node table — Rolle + Reuse-Relevanz columns

**Scope updated 2026-08-13 for the strict-review final cut (was 859 nodes, now 620 +
8 programmes).** `HANDOFF_STRICT_SEMIO_FINAL.md` governs node/edge pruning and figure
integration but does **not** cover this table's column redesign — that recipe is still
this document. Only the node counts and source file below changed; the rest of this
handoff (column layout, two-line row math, the `beleg_zitat`/`begruendung` trap,
escaping, deployment) is unchanged and still applies verbatim.

## Split of work — read this first

The **content** of the Rolle and Relevanz columns is no longer produced here. A separate
classification pass generates it against a controlled taxonomy:

- `KLASSIFIKATION_TAXONOMIE.md` — the controlled role vocabulary (self-contained prompt)
- `batches/` + `results/` — the classification run, all 859 original nodes covered
- `klassifikation.json` — merged output, keyed by `eid`
- `validate_klassifikation.py` — checks returned tables against the vocabulary

**This handoff is the rendering half.** It consumes that pass's output (already merged
into `klassifikation.json`: `{rolle, rollen[], relevanz, actor_degree, beleg_url, ...}`
per eid) and puts it in print.

**Scope for rendering is `klassifikation_actor_project_final.json` (620 eids), not
`klassifikation.json` (859 eids).** Checked directly: all 620 final eids have a
`klassifikation.json` entry, zero gaps — no reclassification needed, this is a pure
filter. `klassifikation.json` still contains the 239 nodes the strict review pruned
plus the 8 reclassified as programmes; **do not render those in the actor table.** The
8 programme eids are listed in `HANDOFF_STRICT_SEMIO_FINAL.md` and get their own block,
built from `programme_strict_final.json`, not from this table at all.

## The job

1. Rebuild `netz/render/latex/table_grid.py` to render **ID | Name | Grad | Rolle(n) | Reuse-Relevanz | Q** (replacing ID | Name | Typ | Rollen), reading the classification output joined on `LAND:tid`.
2. Emit a numbered **Quellen** list per country block.
3. Handle the two-line row layout the widths force (below).

Out of scope: edge tables, figure edge styling, the stale methodology paragraph in `anhang/akteursnetz.tex` (still says 955 nodes/596 edges — being rewritten separately, do not touch).

## The old role vocabulary is superseded

`vocab.py::ROLE_SHORT` and the `rollen` field in `worklist.json` are the **old** 31-category
scheme. The classification pass replaces it with a much finer controlled vocabulary. Do not
render the old tags, and do not try to reconcile the two — the new values arrive ready to
print. `ROLE_SHORT` stays only for whatever still references it elsewhere.

## Why the row must break over two lines

Calibrated from the renderer's own constants (`NAME_MAX=52` chars across `x=8.5…92`, i.e.
1.606 mm/char at 7 pt → 1.42 mm/char at 6.2 pt):

| column | content | width |
|---|---|---|
| ID | `M07` | 8.5 mm |
| Name | 40 chars | 64 mm |
| Grad | `kern`/`bezug` | 10 mm |
| Rolle(n) | up to 3 roles, ~70 chars | 100 mm |
| Relevanz | ≤90 chars (capped in the prompt) | 128 mm |
| Q | source number | 5 mm |

That is **~316 mm against 181 mm of usable width** — a single line cannot hold it even with
the 90-char cap already imposed on the Relevanz text. So: line 1 = `ID | Name | Grad | Rolle(n) | Q`,
line 2 = indented Relevanz. That roughly halves rows/page (66 → ~33) and grows the table
from 16 to ~32 pages. Flag it if that page budget is a problem — the alternative is dropping
Relevanz out of the grid into a separate per-country list.

## Critical field rule (bug already hit once — do not repeat)

- `beleg_zitat` — verbatim quote from the **organization's own page**. The only valid basis for the Relevanz phrase.
- `begruendung` — **our** research narration ("Seite gesperrt", "403 Bot-Block", "nicht auffindbar"). Describes our crawler, not the org. Never surface it in the table. This exact confusion produced nonsense cells like "Seite gesperrt" in an earlier draft.

## Data

| what | where |
|---|---|
| verdicts (grades + evidence) | `E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck\verdicts.json` |
| role tags, typ, source urls | `…\worklist.json` → `packets[].nodes[]` |
| Rolle(n) + Relevanz text | output of the classification pass (see split of work above) |
| network object | `netz\netz\model\concepts.py::build_network` |

`verdicts.json` `nodes[]`: `{tid, cc, eid, actor_degree, beleg_url, beleg_zitat, begruendung, name, flags, abrufdatum}`.
`worklist.json` nodes: `{tid, eid, name, typ, rollen: [...], source_urls, is_project, is_isolated}`.

**Join key is `eid` everywhere.** `net.tid[eid]` equals `worklist.json`'s `tid` for the same eid (the fact-check's desk phase called netz's own `build_network`, so the numbering is identical).

**Verified:** all 620 final nodes have a verdict — 0 gaps (re-checked against the strict-review cut, not just the original 859). `ohne_beleg` does not exist in the final set (all deleted before the strict review ran).

- `kern` = org states reuse as part of its own ongoing practice
- `bezug` = named in a specific reuse matter, not its core business

## Already cleaned — nothing to do here

- **Fact-check cleanup (955 → 859 nodes, 641 → 570 edges):** all `ohne_beleg` + R1/R3 candidates removed, `unklar` edges dropped. Superseded by the strict review below but the mechanism (`build_final_prune.py` → `netz/sources.py` → `cli.py::load_network()`) is unchanged.
- **Strict review (859 → 620 nodes, 570 → 268 edges, 8 programmes split out):** three-lane cross-reviewed pass, see `HANDOFF_STRICT_SEMIO_FINAL.md`. The 268 edge figure is a pure consequence of node pruning (an edge only draws if both endpoints survive) — no separate edge reclassification happened.
- The LaTeX **figures** (`frag_abb_netz.tex`) already reflect the 620/268 final cut. The **table** does not — `table_grid.py` is still untouched, ID/Name/Typ/Rollen, that's this handoff's job.

## Quelle format — already decided, don't relitigate

**Numbered reference in the row → numbered Quellen list at the end of each country's block.** Not inline links, not per-page footnotes (a raw TikZ grid can't do real footnotes without roughly tripling the page count).

Unique `beleg_url` per country, recomputed for the 620-node final scope:

    AT 16 · BE 65 · CH 56 · DE 55 · DK 43 · FI 27 · FR 88 · GB 72 · NL 64 · NO 25 · SE 34   (545 total)

Several actors share a URL (a project page evidencing multiple partners) — dedupe per country so the number points at one list entry.

## Renderer you're modifying

`netz\netz\render\latex\table_grid.py` — dense TikZ grid, `ROWS_PER_PAGE = 66`, flat alphabetical per country. Currently reads only `net.raw.types`/`net.raw.roles` from the original Neo4j export; it has **no access to grades or evidence** — wiring that in is part of the job.

Layout budget: rows span **x = 0 … 181 mm**. Current columns `X_NR=0, X_NAME=8.5, X_TYP=92, X_ROLE=104`, `NAME_MAX=52` chars. Dropping Typ frees ~12 mm. Keep the existing TikZ node style (`\SemioMono` / `\SemioSans`, the existing font sizes, `semio-chrome-*` colors).

**Escaping:** use `esc()` / `esct()` from `escape.py` **per field, before joining** — never run an already-joined string containing a LaTeX separator macro back through `esc()`. That bug already shipped once (it corrupted the role separator into a literal backslash-brace).

## Deploying the result

There is **no automated sync** from `E:\recherche` to the report. After regenerating:

```bash
python -m netz.cli tables-grid
```

then copy the fragment into the report yourself:

    E:\recherche\_neo4j\netz\figs\frag_tables_grid.tex
      →  E:\semio\mit-bestand\bericht\zwischenbericht\anhang\akteursnetz-tabellen.tex

(the figures counterpart is `frag_abb_netz.tex` → `anhang\akteursnetz-figuren.tex`, already current at 859/570).

Build the report from `E:\semio`:

```bash
bun run build:mit-bestand:zwischenbericht
```

Two notes: this target is **flaky** — a "tectonic build failed" on the dark variant can pass unchanged on a rerun, and Nx itself flags it. Never run two builds concurrently; they collide over the same output dir. Also, edits to `print/tex/*.sty` are **not** tracked by the Nx cache — if you touch one, add `--skip-nx-cache` or you'll get a cached PDF that silently ignores your change.
