# Printable diagrams from Neo4j

Cypher in, vector PDF and SVG out. Graphviz does the layout and writes the PDF
directly — no browser, screenshot tool or PDF-conversion library is involved.

Every sheet carries the **semio visual identity**: colours, typefaces and stroke
widths resolve from `_neo4j/diagrams/semio/tokens.json`, a verbatim snapshot of the
semio design system. This is enforced, not encouraged — `validate_semio_styling.py`
fails on any colour or font outside the token set. The rules live in
[`.claude/skills/semio-styling/SKILL.md`](../../.claude/skills/semio-styling/SKILL.md);
read that before changing anything visual.

Neo4j stays the source of truth. Every query here is **read-only**; a query
containing `CREATE`, `MERGE`, `DELETE`, `SET`, `REMOVE`, `DROP`, `FOREACH` or
`LOAD CSV` is rejected before it reaches the driver.

## Prerequisites

```bash
python _scripts/check_neo4j.py         # connection, database, size
python _scripts/check_graphviz.py      # dot, layout engines, SVG/PDF output
python _scripts/sync_semio_tokens.py   # design tokens match the semio source
```

All three must exit `0`. The semio typefaces (Anta, Kelly Slab, Share Tech Mono) must
also be installed — Graphviz resolves fonts through Pango and silently falls back to
Tahoma otherwise. The gate catches that; the skill file has the reinstall command. Connection settings resolve from `NEO4J_URI` /
`NEO4J_USERNAME` / `NEO4J_PASSWORD` / `NEO4J_DATABASE`, falling back to
`.cursor/mcp.json` — see `_scripts/neo4j_env.py`. Graphviz setup and
troubleshooting: `_scripts/GRAPHVIZ_SETUP.md`.

## Render

```bash
python _scripts/render_neo4j_diagram.py --list          # the catalog
python _scripts/render_neo4j_diagram.py --all           # every view
python _scripts/render_neo4j_diagram.py --view huerden  # one view
python _scripts/render_neo4j_diagram.py --view projekt-detail --param name="BedZED"
```

Ad-hoc, without touching the catalog:

```bash
python _scripts/render_neo4j_diagram.py \
  --name materialdepots \
  --cypher "MATCH (m:Materialdepot)-[r]-(x) RETURN m, r, x" \
  --paper A2 --engine auto
```

Output lands in `_neo4j/exports/diagrams/` as three files per view:

| File | Purpose |
|---|---|
| `<view>.pdf` | vector, for printing |
| `<view>.svg` | vector, for editing in Illustrator/Inkscape or embedding |
| `<view>.dot` | the Graphviz source — tracked in git, so any sheet is reproducible |

`.pdf`, `.svg` and `.png` under that folder are gitignored because they are
regenerable; the `.dot` is not. Remove the three lines in `.gitignore` if you
would rather commit the sheets themselves.

## The catalog

`views.json` holds the named views. Each entry carries its query plus the paper
and engine that were measured to keep captions legible on that sheet.

| View | Sheet | What it shows |
|---|---|---|
| `schema-overview` | A1 | Meta-graph of labels and relationship types (≥ `min_count` instances) |
| `programm-landschaft` | A3 | Which projects belong to which programme |
| `geografie` | A1 | Cities grouped by country |
| `software-werkzeuge` | A1 | Who uses which software |
| `bauteiltyp-materialgruppe` | A2 | Component types against material groups, edge weight = number of Bauteilgruppen |
| `regulierungsfragen` | A2 | What triggers which regulatory question |
| `nachweise` | A2 | What requires which proof |
| `schadstoffe` | A1 | Everything attached to a contaminant |
| `projekt-verortung` | A1 | Projects, their cities and programmes |
| `akteur-netzwerk` | A0 | The actor-to-actor network |
| `huerden` | A1 | What carries which barrier |
| `projekt-detail` | A2 | One project and everything one hop away (`--param name=…`) |

### Adding a view

Append an object to `views.json`:

```json
{
  "name": "meine-sicht",
  "title": "Titel auf dem Blatt",
  "subtitle": "Optionaler Untertitel, darf {param} enthalten",
  "description": "One line shown by --list",
  "mode": "graph",
  "engine": "auto",
  "rankdir": "auto",
  "paper": "A2",
  "orientation": "landscape",
  "max_nodes": 200,
  "edge_labels": false,
  "wrap": 18,
  "cypher": "MATCH (a:Label)-[r]->(b) RETURN a, r, b",
  "params": { "name": "Beispiel" }
}
```

Two result shapes are supported:

- **`"mode": "graph"`** — the query returns nodes, relationships or paths. Every
  `Node` and `Relationship` anywhere in the result is collected, including inside
  lists and paths. Relationships whose endpoints were not returned are dropped
  rather than drawn dangling.
- **`"mode": "aggregate"`** — the query returns plain rows with `source` and
  `target` columns, optionally `type`, `count`, `source_label` and
  `target_label`. One drawn edge stands for many real ones and `count` sets its
  thickness. Use `source_label` / `target_label` when the caption is an entity
  name rather than a label name, so the box still gets its domain colour.

## Making it printable

The renderer reports the point size captions will actually have on the chosen
sheet, and warns below 6pt:

```text
OK  huerden   170 nodes  237 edges  fdp   A1 landscape   8.1pt  huerden.pdf …
```

That number is what decides whether a sheet is worth printing. Levers, roughly in
order of effect:

1. **`--engine auto`** — trial-lays out all six engines (and both `dot`
   directions) and keeps whichever stays largest on the page. On dense bipartite
   data this has been worth 4pt → 9pt. `"engine": "auto"` does the same from the
   catalog.
2. **`--paper A2 / A1 / A0`** — each step up is roughly ×1.4 on caption size.
3. **Narrow the query.** A hundred fewer nodes beats a bigger sheet.
4. **`--no-edge-labels`** — above 45 edges these are dropped automatically unless
   `--edge-labels` forces them. When every edge is the same type, the type moves
   into the subtitle and only multiplicities stay on the edges.
5. **`--wrap N`** — narrower captions make rounder nodes and tighter layouts.

Engine choice also carries meaning, so `auto` is not always right: `dot` shows
hierarchy, `circo` and `twopi` show radial structure, `fdp`/`sfdp`/`neato` show
clusters in a network. The catalog pins an engine where the reading matters and
uses `auto` where the data is just a network.

## Putting a diagram in the LaTeX document

The semio document's geometry sets the size, so there are content-box presets for it:

| Preset | Box | Use |
|---|---|---|
| `latex-window` | 148.0 × 249.6 mm | inside a `Figure`/`Image`/`Photo` — the usual one |
| `latex-body` | 152.6 × 254.2 mm | bare in the text block |
| `latex-cover` | 180.7 × 268.0 mm | cover pages |
| `latex-flyer` | 273 × 186 mm | `type=flyer`, with `--orientation landscape` |

```bash
python _scripts/render_neo4j_diagram.py --view programm-landschaft \
    --paper latex-window --orientation portrait --title ""
```

```latex
\begin{Figure}[title=Programme und ihre Projekte]
  \SemioImage[fit=none]{../_neo4j/exports/diagrams/programm-landschaft.pdf}
\end{Figure}
```

`fit=none` keeps it 1:1. Scaling with `\includegraphics[width=...]` would scale the type
too, so the diagram's captions would stop matching the document's body text. Pass
`--title ""` — the window draws its own title tab.

The renderer warns when a content-box preset has to shrink:

```
! latex-window shrinks to 77%, so captions land at 7.4pt against 9.6pt body text
```

The text column is only 148 mm, which holds roughly 20–30 nodes at readable size. Most
views need a narrower query, a full page, or a separate large-format sheet. Details and
measurements: [`semio/VISUAL_LANGUAGE.md`](semio/VISUAL_LANGUAGE.md) §6.

## When a relationship is numbers, not shapes

Some subgraphs are unreadable as node-link diagrams at any size. A fan-in from a few
sources to many targets is the clearest case: `Bauteilgruppe`/`Projekt` → 11 `Huerde` is
13 nodes and 22 edges, which fits the column numerically but produces nothing but edge
crossings. The same numbers as a table are immediately legible.

```bash
python _scripts/export_neo4j_table.py --list
python _scripts/export_neo4j_table.py --all
```

`tables.json` is the catalogue. Queries return `left` and `right` columns and are
read-only under the same guard as diagrams. Output is a `.tex` fragment using the semio
package's public two-column API inside a `Table` window, so it carries the same hairline
frame, title tab and register entry as any other window:

```latex
\input{../_neo4j/exports/diagrams/huerden-traeger.tex}
```

**Not verified by compilation** — no TeX engine is installed on this machine. The fragment
uses only `\SemioTableTwo`, `\SemioTableHeaderRow` and `\SemioTableRow` from
`print/tex/semio-table.sty`, and cell contents are LaTeX-escaped while the `&` column
separator is not, but it has not been run through XeLaTeX.

## Complete graphs need a plate, and that is arithmetic

Two views draw every node and every edge as a node-link graph:

| View | Nodes | Edges | Sheet | Type |
|---|---|---|---|---|
| `huerden-graph` | 170 | 237 | A0 landscape | 9.6pt |
| `regulierung-graph` | 537 | 1,636 | A0 landscape | 7.2pt |

They do not fit the 148 mm text column, and no layout trick changes that. Measured, on a
full landscape page (254 × 152 mm), drawing the carriers of a single barrier:

| Barrier | Nodes | Type size |
|---|---|---|
| Ausschreibungsproblem | 6 | 9.6pt |
| Akzeptanzproblem | 9 | 7.9pt |
| Fehlende Lagerfläche | 15 | 4.5pt |
| Aufbereitungsaufwand | 23 | 4.8pt |
| Witterung / Feuchte | 40 | 4.5pt |

The budget on a whole landscape page is roughly **9 nodes** at body size. Carrier names
average 20 characters, and a hub with 39 spokes is close to the worst case for a node-link
layout — the leaves fan out and most of the sheet becomes whitespace. Dropping the kind
chips makes it *worse*, not better: the nodes get wider, and width is the binding
constraint.

So the honest split is:

- **In the document**: the matrices (`huerden`, `regulierungsfragen`). Every relationship
  is present, aggregated, at 7.3–9.6pt in the column.
- **As a plate**: the complete graphs above, A0, referenced from the document. Every
  carrier named, every hop drawn.

```latex
Die vollständige Darstellung findet sich in Plate~1 (A0).
```

## Proving nothing was dropped

A figure that quietly loses half its data still renders, still passes the styling gate, and
still looks convincing. So the claim is checked rather than asserted:

```bash
python _scripts/validate_view_coverage.py
```

```text
OK   huerden-graph          237 / 237   HAT_HUERDE relationships          (170 nodes, 237 edges)
OK   regulierung-graph     1636 / 1636  relationships across the whole chain  (537 nodes, 1636 edges)
```

A view opts in by declaring what it should contain:

```json
"coverage": {
  "expect": "MATCH ()-[r:HAT_HUERDE]->() RETURN count(r) AS n",
  "of": "HAT_HUERDE relationships"
}
```

The validator runs the view's own query, counts the distinct relationships that reach the
drawing, and compares. Views without a `coverage` block are skipped — the matrices do not
declare one, because a cross-tabulation legitimately counts a carrier once per component
type, so cell sums are not relationship counts.

**This check earned its keep immediately.** It exposed that edge multiplicity was counting
*result rows* rather than distinct relationships: a multi-hop `OPTIONAL MATCH` returns the
same relationship once per row, so the regulations chain reported 1,381,680 instead of
1,636. Every `×n` edge label on a fan-out view was inflated. Multiplicity is now counted
per relationship element id.

## Matrix mode — when the graph is dense

`"mode": "matrix"` renders a cross-tabulation as one HTML-table node. No layout engine
runs, so no space is spent on edge routing and every millimetre carries a cell.

Use it when a relationship is **dense**: `Huerde` × `Bauteiltyp` is 88 relationships over
11 rows and 15 columns — 53% fill. Drawn as edges that is an unreadable hairball at any
size; drawn as cells it is 110 mm tall at full column width.

The query returns `row`, `col`, `value`, plus optionally:

| Column | Effect |
|---|---|
| `row_group` | groups rows under a shaded band; rows are sorted by group, so a `UNION` is safe |
| `col_order` | sorts columns by rank then name, instead of first-seen order |

View options: `"totals": false` suppresses the automatic sum column (use it when the query
supplies its own), and `"plain_cols": [...]` renders those columns unshaded.

```json
{
  "name": "huerden",
  "mode": "matrix",
  "paper": "latex-window",
  "totals": false,
  "plain_cols": ["Bauteilgr.", "Projekte"],
  "cypher": "… RETURN name AS row, category AS row_group, typ AS col, n AS value, 1 AS col_order"
}
```

**Quantity is encoded on the neutral ramp**, six steps, ranked on a square root so common
small values stay apart. Hue stays reserved for state — see the identity rules. An empty
cell takes the sheet surface, so absence reads as absence rather than as the lowest rank.

A summary column counts something different from the matrix cells, so put it in
`plain_cols`: shading it on their scale would invite a comparison that is wrong.

Column headers set their column's width, and Graphviz cannot rotate text in an HTML label,
so a long header must be shortened or broken. Put a `|` in the header where it should
break:

```cypher
WHEN 'Bauteilgruppe' THEN 'Bauteil|gruppen'   -- renders on two lines
```

The break point is explicit because German compounds have to split at a syllable the
author picks — `Bauteil|gruppen`, never `Bauteilg|ruppen`. Without a `|`, wrapping only
happens at whitespace: a long single word simply makes its column wide, which is a signal
to shorten the header rather than mutilate it. Names in `plain_cols` must include the `|`.

### Two worked examples

| View | Rows × cols | Relationships shown | Size in the column |
|---|---|---|---|
| `huerden` | 11 × 17 | 237 | 148 × 110 mm, 7.3pt |
| `regulierungsfragen` | 11 × 9 | 1,455 | 143 × 105 mm, 9.6pt |

`regulierungsfragen` is the more interesting one: it follows the whole regulatory chain in
one grid. The left columns are the six trigger types
(`TRIGGERS_REGULIERUNGSFRAGE`, 1,101 edges); the right three follow
`ERFORDERT_NACHWEIS` → `GESTUETZT_AUF_REGELWERK` → `GILT_IN_LAND` to count the
Nachweisforderungen, Regelwerke and jurisdictions each question reaches.

That last join is a **real 2-hop path**, not the name similarity between
`BauproduktstatusFrage` and `Bauproduktrecht`. The graph has no direct
Frage↔Rechtsgebiet edge, and inventing one to make a tidier figure would be fabricating a
relationship.

## Reducing a view until it fits

`huerden` is the worked example. Raw, it is `(x)-[:HAT_HUERDE]->(h:Huerde)` — 170 nodes,
237 edges, **1.9pt** in the text column. The 159 individual carriers are the bulk and say
nothing as separate boxes.

Every `:Huerde` carries a `category` property, so aggregating to the taxonomy gives 19
nodes and 11 edges at **9.0pt** — above the 7.2pt body text inside a window, on a
116 × 250 mm page inside the 148 × 250 mm column. The carrier counts ride on the edges as
`×n`; the Bauteilgruppe/Projekt split moved to the companion table.

The order to try, when a view does not fit:

1. **Find a grouping property** on the target (`category` here) and aggregate to it.
2. **Check whether the source side collapses** to a handful of labels — if so it is a
   table, not a graph.
3. Only then reach for a bigger sheet.

### German naming

The graph stores ASCII-folded names and English snake_case categories
(`Heterogenitaet_Chargen`, `procurement_regulatory`). The `huerden` view and the
`huerden-traeger` table both carry a `CASE` display map so print reads correctly in
German. This is display-only — Neo4j is untouched, so there is no provenance impact, and
the underlying inconsistency stays visible as a known data issue. **Keep the two maps in
step**; if the naming should become permanent it belongs in a reviewed patch under
`_neo4j/intake/`, not in these views.

## Printing

The PDF page is the drawing's own bounding box plus the margin, capped at the
chosen sheet — not a fixed A-series page. So `programm-landschaft` on A3 comes out
228 × 297 mm rather than a full 420 × 297: it uses the sheet's height and only as
much width as it needs. `--orientation` sets the *bounds* the layout must fit
inside, so a tall drawing can still produce a tall page on a landscape setting.

Print **at 100% / actual size** on the sheet named in the table above and the
margin comes out as specified. "Fit to page" also works and will simply centre
the trimmed page. Nothing is rasterised at any point — the PDF and SVG are
vector all the way down, so enlarging on a plotter costs no quality.

## Options

```text
--view NAME | --all | --cypher TEXT | --cypher-file PATH | --list
--name NAME              output basename for an ad-hoc query
--mode graph|aggregate   result shape
--param key=value        Cypher parameter, repeatable
--database NAME          override the configured database

--paper A5..A0|letter|legal|tabloid
--orientation portrait|landscape
--engine auto|dot|neato|fdp|sfdp|circo|twopi
--rankdir auto|LR|TB|RL|BT
--margin INCHES          page margin, default 0.4
--wrap N                 caption wrap width, default 22
--max-nodes N            printable budget, default 300
--ratio compress|fill|…  raw Graphviz ratio
--title / --subtitle
--no-legend / --no-edge-labels / --edge-labels

--format pdf svg png     default: pdf svg
--dpi N                  raster DPI for png, default 300
--out-dir PATH           default _neo4j/exports/diagrams
```

## Troubleshooting

**`GraphTooLargeError`** — the query returned more nodes than `--max-nodes`. That
guard exists because past a few hundred nodes captions stop being legible at any
sheet size. Narrow the query, or raise the budget and print on A0.

**`Query contains the write clause …`** — intended. Use the intake and patch
tooling in `_neo4j/` for anything that changes the graph.

**A node is grey when it should not be** — its label is missing from `LABEL_ROLES` in
`_scripts/semio_style.py`. Map it to an existing role. Do not add a new colour: grey
means unmapped, and that is meant to be visible rather than disguised.

**The gate fails** — `python _scripts/validate_semio_styling.py` names the file, line,
offending colour or font, and why. See the skill file's failure table.

**Type looks like Tahoma** — the semio fonts are not installed for this user. The gate
reports it as a font violation. Reinstall per the skill file, then re-render.

**`dot` not found** — see `_scripts/GRAPHVIZ_SETUP.md`.

## Modules

| File | Role |
|---|---|
| `_scripts/neo4j_env.py` | connection settings (existing) |
| `_scripts/graphviz_env.py` | locates and runs Graphviz, no shell |
| `_scripts/semio_style.py` | semio tokens → every colour, typeface and stroke |
| `_scripts/neo4j_to_dot.py` | Cypher result → DOT, paper sizing, layout fitting |
| `_scripts/render_neo4j_diagram.py` | CLI |
| `_scripts/check_neo4j.py` | connection check |
| `_scripts/check_graphviz.py` | Graphviz check |
| `_scripts/sync_semio_tokens.py` | vendors the token snapshot, detects drift |
| `_scripts/validate_semio_styling.py` | the styling gate |
| `_neo4j/diagrams/semio/tokens.json` | the token snapshot itself |

`_neo4j/neo4j_style.grass` is no longer a colour source. It remains the Neo4j **Browser**
stylesheet; the printed sheets and the Browser view are allowed to differ.
