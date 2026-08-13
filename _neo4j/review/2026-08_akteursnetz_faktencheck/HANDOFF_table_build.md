# Handoff: node table — Rolle + Reuse-Relevanz columns

## Split of work — read this first

The **content** of the Rolle and Relevanz columns is no longer produced here. A separate
classification pass generates it against a controlled taxonomy:

- `KLASSIFIKATION_ADDENDUM.md` — project rules (input contract, Regel P for building
  entries, output format, length caps)
- `KLASSIFIKATION_TAXONOMIE.md` — the controlled role vocabulary
- `batches/` — 49 batches × ≤20 actors, all 859 covered
- `validate_klassifikation.py` — checks returned tables against the vocabulary

**This handoff is the rendering half.** It consumes that pass's output (a 4-column table
`ID | Name | Rolle(n) | Relevanz`, ID in `LAND:tid` form) and puts it in print.

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

**Verified:** all 859 drawn nodes have a verdict — 0 gaps. Grades: **485 kern, 374 bezug**. `ohne_beleg` no longer exists in the drawn set (all deleted).

- `kern` = org states reuse as part of its own ongoing practice
- `bezug` = named in a specific reuse matter, not its core business

## Already cleaned — nothing to do here

- **Nodes:** 93 eids deleted (`prune_faktencheck_final.json`) = all 86 `ohne_beleg` + R1 duplicates + R3 wrong-country. Plus 3 cascade drops (Tecclem, G-build, Vlieghe — lost their only country signal when a fabricated-evidence project was removed; approved). **955 → 859 drawn nodes.**
- **Edges:** 71 of the 88 `unklar` edges dropped from drawing (`unklar_edges_final.json`, via `partition()`'s `edge_exclude`). **641 → 570 drawn edges.** `teilweise_belegt` edges were deliberately **kept** (they are evidenced, just one-sided) — they're to be marked, not removed, in the separate edge work.
- Both lists regenerate from `build_final_prune.py`. Wired through `netz/sources.py` → `cli.py::load_network()`.

## Quelle format — already decided, don't relitigate

**Numbered reference in the row → numbered Quellen list at the end of each country's block.** Not inline links, not per-page footnotes (a raw TikZ grid can't do real footnotes without roughly tripling the page count).

Unique `beleg_url` per country (list length to expect):

    AT 18 · BE 82 · CH 67 · DE 75 · DK 54 · FI 29 · FR 96 · GB 92 · NL 86 · NO 27 · SE 38   (664 total)

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
