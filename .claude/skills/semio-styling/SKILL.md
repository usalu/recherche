---
name: semio-styling
description: Strict styling gate for every generated diagram, sheet, figure or export in this repo. Load this BEFORE writing or changing any code that emits a colour, typeface, stroke width, shape or page — Graphviz DOT, SVG, PDF, matplotlib, HTML, or a Neo4j Browser stylesheet. Colour, type, stroke and form come only from the vendored semio design tokens; hand-picked hex values, system fonts, rounded corners and ellipses are violations, not preferences.
---

# Semio visual identity — strict gate

Every visual artifact this repo produces belongs to the **semio** design system, the same
one that paints the *Entwerfen mit Bestand* demonstrator (`mit-bestand/aggregator/brand.ts`
locks `themeId: "semio"`). A diagram is either compliant or it is broken.

Full reference with citations: [`_neo4j/diagrams/semio/VISUAL_LANGUAGE.md`](../../../_neo4j/diagrams/semio/VISUAL_LANGUAGE.md).
Read it before changing anything visual. This file is the enforceable subset.

## The gate

Any change touching visual output MUST end with all three exiting `0`:

```bash
python _scripts/sync_semio_tokens.py          # tokens match the semio source
python _scripts/render_neo4j_diagram.py --all # everything re-renders
python _scripts/validate_semio_styling.py     # nothing outside the identity
python _scripts/validate_view_coverage.py     # no view silently drops data
```

The gate reads the rendered `.dot` and `.svg`, not the source, because that is what a
reader sees. Do not claim compliance without running it.

## Sources of truth

| What | Where | Rule |
|---|---|---|
| Screen tokens | `_neo4j/diagrams/semio/tokens.json` | Verbatim from `E:/semio/ui/styling/tokens.json`. **Never hand-edit.** |
| **Print tokens** | `_neo4j/diagrams/semio/print-tokens.sty` | Verbatim from `E:/semio/print/tex/semio-tokens.sty`. **A PDF uses these.** |
| Resolver | `_scripts/semio_style.py` | The only module allowed to produce a colour string. |
| Gate | `_scripts/validate_semio_styling.py` | The only definition of "compliant". |
| Sync | `_scripts/sync_semio_tokens.py` | `--pull` after upstream changes, then re-render. |

Colour changes belong upstream in the semio monorepo, never here.

## The three rules that matter most

### 1. Colour is state, never kind

`board` defines one `nodeFill` plus `nodeFillHovered` / `Selected` / `SelectionExit` /
`Disabled`. There is **no per-kind colour anywhere in semio** — confirmed in
`tokens.json`, `generated.py`, `generated.rs` and the board renderer.

- **MUST** paint node bodies with `board.nodeFill` and borders with `board.nodeStroke`.
- **MUST NOT** map a Neo4j label, category or domain to a colour. Kind is stated
  typographically, as a muted chip above the caption — semio's own device for window
  titles and hierarchy keys.
- Encoding a **quantity** is allowed, but only on the neutral ramp (`MAGNITUDE_RAMP`,
  six steps). Hue would read as a category. Zero takes the sheet surface, and a summary
  column counting something other than the cells goes in `plain_cols`, unshaded.
- Accents mark state only. `focus` (`nodeFillSelected`) is reserved for the entity a
  sheet is about — currently `:Projekt`, in `FOCUS_LABELS`.

### 2. Nothing is rounded

`ui.css` has no non-zero `border-radius` in 5,259 lines; `semio-window.sty` sets
`arc=0mm`; `radii.chrome` is `0.0`.

- **MUST** use `shape=box` with square corners.
- **MUST NOT** use `style="rounded"`, `ellipse`, `circle`, `oval`, or `rx`/`ry` on a rect.
- `radii.nodeDefault` / `nodeRectDefault` are world-space canvas geometry, **not** a UI
  corner radius. Do not read them as permission to round anything.

### 3. Print points, not screen pixels

`tokens.json` is authored in screen px; `print-tokens.sty` states what semio prints with.

| | Print | Screen |
|---|---|---|
| hairline | **0.75pt** | 1.0 |
| default | **1.5pt** | 2.0 |
| focus | **2.25pt** | 3.0 |
| body | **9.6pt** | — |
| chip | **7.2pt** | — |

- **MUST** take stroke and type sizes from `print_pt(...)`.
- **MUST NOT** use `metrics.typography.*Px` or `metrics.label.*Px` in a PDF — those are
  UI pixels.

### 4. A diagram is sized by the document, not by a sheet

Diagrams go into the semio LaTeX document. Its geometry decides the size — measured from
`semio.cls` and the compiled report log, not guessed.

| Preset | Content box | Use |
|---|---|---|
| `latex-window` | **148.0 × 249.6 mm** | inside a `Figure`/`Image`/`Photo` — the usual one |
| `latex-body` | 152.6 × 254.2 mm | bare in the text block |
| `latex-cover` | 180.7 × 268.0 mm | cover pages (`\newgeometry{1.5cm}`) |
| `latex-flyer` | 273 × 186 mm | `type=flyer`, `--orientation landscape` |

A window costs 12.5pt per side: `boxrule` 0.75pt + `\semio@window@bodypad` 5.5pt.

- **MUST** render at a `latex-*` preset for anything embedded. These are content boxes;
  the page margin is forced to zero because the document owns the margins.
- **MUST** include at 1:1 — `\SemioImage[fit=none]{...}`. Scaling with
  `\includegraphics[width=...]` scales the glyphs too, and the diagram's type stops
  matching the document's.
- **MUST** pass `--title ""` when embedding: the window supplies the title tab, and a
  second title is double chrome.
- **MUST NOT** draw a border around the drawing — the window's frame is the border.
- Type must land at **9.6pt** against body text, **7.2pt** inside a window. The renderer
  warns whenever a content-box preset has to shrink; a diagram at 20% is not a small
  figure, it is an unreadable one. Narrow the query, give it a full page, or keep it as a
  separate large-format sheet.

## Remaining hard rules

4. **MUST NOT** write a hex literal in any file producing visual output. Call
   `SEMIO.token(...)`, `SEMIO.board/canvas/chrome(...)` or `node_style(...)`. The gate
   tolerates only `#000000` and `#FFFFFF`, which Graphviz emits itself.
5. **MUST NOT** name a typeface other than `Anta`, `Kelly Slab` or `Share Tech Mono`.
   `Helvetica`, `Arial`, `Times`, `Tahoma`, `sans-serif` in output means a font failed to
   resolve — a failure even though the file still renders.
6. **MUST NOT** use italics or rely on bold. Anta ships Regular only and has no italic
   face; semio's own rule is *"emphasis is a color swap, never italics"*. Move text from
   `mutedForeground` to `foreground` instead.
7. **MUST NOT** add gradients, drop shadows, glows or bevels. Glass-blur tokens are
   screen-only compositing with no print counterpart.
8. **MUST NOT** invent a colour for an unmapped label — every node body is neutral anyway,
   so there is nothing to invent.
9. **MUST** re-render every sheet after any token or code change. A stale `.pdf` beside a
   new `.dot` is the same class of violation.
10. **MUST NOT** reintroduce `_neo4j/neo4j_style.grass` as a colour source. It stays the
    Neo4j **Browser** stylesheet only; the two are allowed to disagree.

## Type

| Use | Family | Size |
|---|---|---|
| Node captions, titles | `Anta` | `chrome@font@body` 9.6pt |
| Kind chips, edge labels, legend | `Anta` | `chrome@font@chip` 7.2pt |
| Provenance, counts, identifiers | `Share Tech Mono` | 7.2pt |

`Kelly Slab` is available and unused. Do not reach for it without a reason.

Fonts must be **installed** — Graphviz resolves through Pango/Win32 and a file path in
`fontname` silently falls back to Tahoma. Only the `latin.ttf` subset covers German plus
`– — · × °`, and all subsets share one internal family name, so install exactly one file
per family:

```powershell
$dest = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
$key  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
Copy-Item E:\semio\dist\assets\fonts\anta\latin.ttf "$dest\semio-anta.ttf" -Force
New-ItemProperty -Path $key -Name "Anta (TrueType)" -Value "$dest\semio-anta.ttf" -PropertyType String -Force
```

Verify with `dot -v`: it prints `fontname: "Anta" resolved to: … "Anta"`. A
`Pango-WARNING` means the font is missing.

## Form

- **Node**: `shape=box`, `style=filled`, hairline border, square corners. Kind chip above
  the caption, both left-aligned.
- **Edge**: hairline, `board.edgeStroke`, one colour for the whole sheet. Multiplicity
  steps to `default` then `focus` — never a fourth width.
- **Register** (the legend): hairline frame, `chrome.canvas` fill, title tab on
  `chrome.panel` sitting *on* the frame and sharing its top rule, counts in mono.
- **Appearance**: `light` by default. `dark` resolves the same names against the dark
  appearance; both must pass.

## When the gate fails

| Symptom | Cause | Fix |
|---|---|---|
| `colour '#XXXXXX' not a semio token` | a hand-picked hex reached the output | route it through `semio_style` |
| `style 'rounded'` / `shape 'ellipse'` | rounded or elliptical form | square it |
| `penwidth '1.6' not a semio print stroke` | a width outside 0.75 / 1.5 / 2.25 | use `print_pt(...)` |
| `font 'Tahoma' — Graphviz fallback` | the semio font is not installed | reinstall, re-render |
| `DRIFT: the semio tokens changed` | upstream edited the design system | `--pull`, re-render, re-gate |

If the semio checkout is not mounted, the vendored snapshots still render everything; only
drift detection is unavailable. That is a warning, not a failure.
