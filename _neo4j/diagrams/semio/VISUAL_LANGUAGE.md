# The semio visual language

Reference for every visual artifact this repo produces. Compiled by reading the semio
monorepo at `E:/semio`, not by inference. Each rule below cites where it comes from, so a
future reader can check it rather than trust it.

The enforceable subset lives in [`.claude/skills/semio-styling/SKILL.md`](../../../.claude/skills/semio-styling/SKILL.md).
This file explains *why*; the skill states *what* and is checked by
`_scripts/validate_semio_styling.py`.

---

## 1. Where the identity is defined

| Concern | File in `E:/semio` | Role |
|---|---|---|
| Colour, spacing, strokes, radii, metrics | `ui/styling/tokens.json` | **Authoring source.** Screen pixels. |
| Paint resolution (`token` / `hex` / `mix` / `alpha`) | `ui/styling/js/theme.ts` | Reference implementation |
| CSS variables and `@font-face` | `ui/styling/js/palette.css` | Generated |
| Component CSS | `ui/styling/js/ui.css` | Generated, 5,259 lines |
| Python bindings | `ui/styling/py/styling/generated.py` | `STYLING_TOKENS`, `BOARD_LIGHT/DARK`, … |
| Rust / C# bindings | `ui/styling/rs/generated.rs`, `net/` | Same tokens, other runtimes |
| **Print tokens, in points** | `print/tex/semio-tokens.sty` | **What a PDF must use** |
| Print mechanisms | `print/tex/semio-core.sty` | Theme, emphasis, hierarchy keys |
| Print chrome | `print/tex/semio-window.sty` | Windows, tabs, frames |
| Print tables | `print/tex/semio-table.sty` | Registers, headers |
| Alternate theme | `ui/styling/theme/mono.theme.json` | Proves the token contract is a contract |
| This project's brand | `mit-bestand/aggregator/brand.ts` | `locks: { themeId: "semio" }` |

Two token sets, one identity. `tokens.json` is authored in **screen pixels**;
`semio-tokens.sty` states the **point** values semio prints with. A printed sheet follows
the `.sty`. Both are vendored here as `tokens.json` and `print-tokens.sty`.

`mit-bestand/aggregator/brand.ts` matters for this repo specifically: the *Entwerfen mit
Bestand* demonstrator is locked to `themeId: "semio"`, German locale and reuse
terminology. These diagrams belong to the same document family.

---

## 2. Colour

### 2.1 The token set

43 primitives. A warm ramp from near-black `#001117` to cream `#F7F3E3` in 33 steps carries
all structure. Seven accents plus one tint carry meaning.

| Token | Hex | |
|---|---|---|
| `primary` | `#FF344F` | red |
| `secondary` | `#34D1BF` | teal |
| `tertiary` | `#FA9500` | orange |
| `danger` | `#A60009` | deep red |
| `warning` | `#FCCF05` | yellow |
| `info` | `#DBBEA1` | sand |
| `success` | `#7EB77F` | green |
| `indirect-handle` | `#C4E4D5` | pale mint |
| `dark` … `light` | `#001117` … `#F7F3E3` | the ramp |

The same three accents appear in the emblem (`brand.ts`): `#FA9500`, `#FF344F`, `#34D1BF`
on `#001117`, outlined in `#F7F3E3`. The palette and the mark are one thing.

### 2.2 Paint references

An appearance never stores a hex. It stores a reference resolved at build time
(`ui/styling/js/theme.ts`):

```jsonc
{ "token": "primary" }                               // a primitive
{ "token": "gray", "alpha": 0.22 }                   // with opacity
{ "mix": ["primary", "black", 0.9] }                 // blend, ratio = weight of a
{ "mix": ["gray", "transparent", 0.38], "alpha": 0.38 }
```

`_scripts/semio_style.py` reimplements this resolver exactly, including the
`transparent` special case where alpha derives from the mix ratio. Print has no
transparency, so alpha is composited onto the group's own backdrop and a flat hex emitted.

### 2.3 Appearances and groups

Two appearances (`light`, `dark`) × four groups (`board`, `map`, `canvas`, `chrome`).
`parseUiTheme` throws if any group is missing, so all four always exist.

- **`board`** — node-link graphs. **This is the group a diagram belongs to.**
- **`map`** — geographic rendering
- **`canvas`** — raster and icon surfaces
- **`chrome`** — window furniture: panels, borders, foreground, accent

### 2.4 The load-bearing rule: colour is state, never kind

`board` defines exactly **one** `nodeFill`, plus `nodeFillHovered`, `nodeFillSelected`,
`nodeFillSelectionExit` and `nodeFillDisabled`. Same for `nodeStroke`, `edgeStroke`,
`wireStroke`, `handleFill`, `labelFill`. Confirmed identically in `tokens.json`,
`generated.py`, `generated.rs` and `infinite/board/port/directed/rs/lib.rs`.

**There is no per-kind colour anywhere in the semio identity.**

A node is neutral. It turns `primary` when selected, `secondary` on selection-exit, and
dims when disabled. Painting node kinds in eleven different colours — as an earlier
version of these diagrams did — is not a semio diagram with semio colours in it; it is a
different visual language borrowing the palette.

What replaces it is in §5.2.

### 2.5 What the accents mean

Read off `map`, the only group that assigns accents to content rather than state:

| Paint | Token | Meaning |
|---|---|---|
| `positionFill` | `primary` | *this specific thing, here* |
| `regionFill` / `regionStroke` | `secondary` | *an area, a containment* |
| `routeStroke` | `tertiary` | *a path, a movement* |

Accents are scarce by construction. An accent everywhere is decoration.

---

## 3. Type

### 3.1 The three families

| Stack | Family | Use |
|---|---|---|
| `sans` | **Anta** | everything by default |
| `serif` | **Kelly Slab** | available, unused here |
| `mono` | **Share Tech Mono** | machine output — provenance, counts, identifiers |

Each stack chains ~12 Noto Emoji subsets after the Latin family. Graphviz takes one family
name, so only the head is used.

### 3.2 Anta has one weight, and no italic

`semio-window.sty:70` — Anta ships **Regular only**, so `\bfseries` is a no-op. Where
semio genuinely needs bold it synthesises it: `\newfontfamily\SemioSansBold[FakeBold=2.5]`.

`semio-core.sty:95` states the consequence directly:

> Emphasis is a color swap, never italics — the print font stack has no italic face.

So: **no italics, no real bold.** Emphasis moves text from `mutedForeground` to
`foreground`. That is the whole mechanism.

### 3.3 Print sizes

From `print/tex/semio-tokens.sty`:

| Token | Value | Use |
|---|---|---|
| `chrome@font@body` | **9.6pt** | body text, node captions |
| `chrome@font@chip` | **7.2pt** | chips, tabs, edge labels, provenance |

`semio-window.sty` narrows body to 7.2pt inside windows for its own documents. The
diagrams use 9.6pt for captions and 7.2pt for chips.

The screen metrics (`metrics.typography.text2xsPx` 9.6 … `textLgPx` 16.0, and
`metrics.label.dagDefaultPx` 11.0) are **pixels for the UI**. Using them in a PDF was an
error in an earlier version.

### 3.4 Fonts must be installed

Graphviz resolves through Pango/Win32. A file path in `fontname` does not work — verified:
it falls back to Tahoma with a `Pango-WARNING`, and the sheet still renders, silently
wrong. The gate treats a fallback family in the output as a violation.

Only the `latin.ttf` subset of each family covers German umlauts plus `– — · × °`; the
`latin-ext`, `math`, `symbols` and `cyrillic` subsets do not. All subsets declare the same
internal family name, so exactly one file per family may be installed.

---

## 4. Form

### 4.1 Nothing is rounded

- `ui.css`, 5,259 lines: every `border-radius` is `0` or `inherit`. There is no non-zero
  radius in the stylesheet.
- `semio-window.sty` `tcbset{semio~window}`: **`arc=0mm`**.
- `radii.chrome` = `0.0`.

`radii.nodeDefault` (24), `nodeMin` (28) and `nodeRectDefault` (40) are **world-space
geometry for the interactive canvas**, in board coordinates — not a UI corner radius, and
not applicable to a printed sheet. Reading them as "semio rounds things" was the mistake
that produced rounded rectangles.

**Every corner is square. Every node is a rectangle. No ellipses, no circles.**

### 4.2 Strokes

| Print (`.sty`) | Screen (`tokens.json`) | Use |
|---|---|---|
| `stroke@hairline` **0.75pt** | `chromeBorderHairline` 1.0 | frames, node borders, edges |
| `stroke@default` **1.5pt** | `chromeBorderDefault` 2.0 | emphasis |
| `stroke@focus` **2.25pt** | `chromeBorderFocus` 3.0 | focal element |

Print points are screen pixels × 0.75. A printed sheet uses the point column. Three widths
exist; a fourth is a violation.

### 4.3 The window

The signature construction, from `semio-window.sty`:

```
┌ Titel ─────────────────────────┬─ 1.2.a ┐   ← tabs sit ON the frame,
│                                          │     sharing its top rule
│  content, inset 5.5pt                    │
│                                          │
└──────────────────────────────────────────┘   ← hairline, arc=0mm
```

- `boxrule` = hairline, `colframe` = `chrome.borderNormal`, `colback` = `chrome.canvas`
- Title tab **flush left**, number tab **flush right**, both anchored so growth never
  moves the frame's borders
- `toprule=0pt` — the tab's baseline *is* the frame's top rule. One shared stroke, never
  two parallel ones. The source is emphatic: *"the tab must SIT ON the component, not
  float above it."*
- Body inset `5.5pt`, matching table cell padding so all content sits the same distance
  from its borders document-wide
- Tab inset: `5.5pt` horizontal, **70%** of that vertical

### 4.4 Spacing

`spacing.compact` `0.2rem`, `spacing.touch` `0.275rem`; print `spacing@unit` `0.2em`,
`double` `0.4em`. Blocks emit exactly one max-merging unit before themselves and nothing
after, so paragraph↔block and block↔block junctions land on one unit.

### 4.5 Hierarchy keys

`semio-core.sty` renders composed identifiers (`1.2.3`, `BB.M`, `SB.B.1`) with everything
up to the last `.` **muted** and the final segment **bright**. One separator per level.
The same muted-head / bright-tail device carries kind labels and window numbers.

### 4.6 What does not exist

No gradients on content, no drop shadows, no bevels, no glow, no rounded anything, no
italics, no real bold. The glass blur tokens (`glassPanelAlpha`, `glassBlurPx`) are
screen-only compositing and have no print counterpart.

---

## 5. Applying it to graph diagrams

### 5.1 Surface and frame

| Element | Paint |
|---|---|
| Sheet background | `board.rasterClear` |
| Node fill | `board.nodeFill` |
| Node border | `board.nodeStroke`, hairline |
| Focal node | `board.nodeFillSelected` / `nodeStrokeSelected`, focus stroke |
| Edge | `board.edgeStroke`, hairline |
| Edge label | `board.labelFill` |
| Title | `canvas.labelFill` |
| Register frame / fill / tab | `chrome.borderNormal` / `chrome.canvas` / `chrome.panel` |

### 5.2 Kind is typographic

Since colour cannot encode kind (§2.4), each node states its own kind the way a semio
window states its title — a muted chip above the caption:

```
┌──────────────────────┐
│ Akteur               │  ← kind chip, 7.2pt, chip colour
│ Cleveland Steel &    │  ← caption, 9.6pt, foreground
│ Tubes                │
└──────────────────────┘
```

The chip colour is the caption colour blended 55% toward the node fill — the same
muted-against-bright relationship as a hierarchy key's head against its tail.

This is strictly more informative than colour coding: it scales past the ~8 categories a
palette can carry, survives greyscale printing and photocopying, and needs no legend
lookup.

### 5.3 The legend is a register, not a key

With one neutral fill there is nothing to key. What remains useful is a count of what is
on the sheet, which is what semio prints as a *Verzeichnis*: a hairline frame, a title tab
sitting on it, kind names left, counts right in Share Tech Mono, and a provenance line.

### 5.4 Quantity rides the neutral ramp

Encoding a magnitude is not encoding a kind, so a shaded matrix cell does not break the
colour-is-state rule — but the shading must stay on the **neutral ramp**. Hue would read as
a category, and semio has no categorical hue to lend.

`MAGNITUDE_RAMP` is six steps of the neutral scale, `l-l-l-g` through `gray`. Six is what a
reader can still rank by eye. Values are ranked on a square root so the common small counts
stay distinguishable instead of collapsing into the first step, and zero takes the sheet
surface so an empty cell reads as absence rather than as the lowest rank.

This is also why a matrix is often the right form for a dense relationship: it spends its
area on data rather than on edge routing, and it needs no colour beyond the ramp the
identity already owns.

### 5.5 Emphasis states

`normal` → `focus` (the sheet's subject) → `highlight` → `muted`. These map onto
`nodeFill` / `nodeFillSelected` / `nodeFillSelectionExit` / `nodeFillDisabled`. Only
`focus` is currently used, for `:Projekt`.

---

## 6. Fitting the LaTeX document

Diagrams are not standalone posters. They are placed into the semio LaTeX document, so the
document's geometry — not a paper size someone picked — decides how big a diagram may be.

### 6.1 Measured geometry

From `semio.cls` and confirmed against the compiled Zukunft Bau report
(`print/dist/_cur/zwischenbericht.log`, geometry verbose output):

| Document | Page | Margins | Text block |
|---|---|---|---|
| `type=report` (forschungsbericht) | A4 portrait | 2.5 cm + 8 mm binding | **432.48 × 720.46 pt = 152.6 × 254.2 mm** |
| `type=paper` (zwischen-/kompaktbericht) | A4 portrait | same | same |
| `type=flyer` | A4 **landscape** | 1.2 cm | 273 × 186 mm |
| Cover pages (`semio-components.sty:148`) | A4 portrait | `\newgeometry{1.5cm}` | 512.15 × 759.69 pt = 180.7 × 268.0 mm |

The log records two geometry passes. The second is the cover-page `\newgeometry`, undone
by `\restoregeometry` — the body geometry is the first.

### 6.2 What a window costs

A diagram normally sits inside a `Figure`, `Image` or `Photo` window, which is a tcolorbox
at `width=\linewidth`. It subtracts, per side:

- `boxrule` = `stroke@hairline` = **0.75 pt**
- `\semio@window@bodypad` = **5.5 pt**

So **12.5 pt total**, leaving `432.48 − 12.5 = 419.98 pt = 148.0 mm` of usable width in a
report body window.

### 6.3 Content-box presets

`PAPER_SIZES` carries these as real presets. They are content boxes, not sheets: the page
margin is forced to zero, because the document already owns the margins.

| Preset | Box | Use |
|---|---|---|
| `latex-window` | 148.0 × 249.6 mm | inside a `Figure`/`Image`/`Photo` — **the usual one** |
| `latex-body` | 152.6 × 254.2 mm | bare in the text block, no window |
| `latex-cover` | 180.7 × 268.0 mm | cover pages |
| `latex-flyer` | 273 × 186 mm | `type=flyer`, with `--orientation landscape` |

```bash
python _scripts/render_neo4j_diagram.py --view programm-landschaft \
    --paper latex-window --orientation portrait
```

### 6.4 The 1:1 rule

A diagram rendered at a content-box preset drops in **without scaling**. That matters
because Graphviz bakes type size into the drawing: `\includegraphics[width=...]` would
scale the glyphs along with the geometry, and the diagram's 9.6 pt captions would no longer
be the document's 9.6 pt body text.

```latex
\begin{Figure}[title=Programme und ihre Projekte]
  \SemioImage[fit=none]{../_neo4j/exports/diagrams/programm-landschaft.pdf}
\end{Figure}
```

`fit=none` passes `\includegraphics` with no width, preserving 1:1. `contain` (the default)
also preserves aspect but will shrink to the box — acceptable only if the diagram is
already smaller than the column.

Type targets: **9.6 pt** against body text, **7.2 pt** inside a window
(`semio-window.sty` narrows body to the chip size there). The renderer reports the size
captions actually land at and warns whenever a content-box preset has to shrink:

```
! latex-window shrinks to 77%, so captions land at 7.4pt against 9.6pt body text
```

### 6.5 The window already supplies the chrome

A `Figure` draws its own hairline frame, title tab and number tab. A diagram placed inside
one must not draw a second set:

- **Pass `--title ""`** — the window's title tab is the title.
- Keep or drop the register (`--no-legend`) as the sheet needs; it is content, not chrome.
- Never add a border around the drawing. The window's frame is the border.

### 6.6 Tables are part of the identity

`print/tex/semio-table.sty` is as much a part of the visual language as the window. When a
relationship is a set of numbers rather than a shape — a fan-in from a few sources to many
targets — the table is the correct form, and forcing it into a node-link diagram produces
edge crossings that carry no meaning.

Public two-column API: `\SemioTableTwo{ … }` with `\SemioTableHeaderRow{a & b}` and
`\SemioTableRow{a & b}`, inside a `Table` window. Header cells get a synthetic bold
(`FakeBold=2.5`) because Anta has no bold face; cells are otherwise plain, set apart by the
shaded header row. `_scripts/export_neo4j_table.py` emits fragments in this form.

### 6.7 The consequence worth stating plainly

The report text column is **148 mm**. At 9.6 pt captions that holds roughly 20–30 nodes.
Most of the catalogue does not fit and should not be forced to: a graph that shrinks to
20% is not a small figure, it is an unreadable one.

Three honest options, in order of preference:

1. **Narrow the query** until it fits the column. A 25-node figure that can be read beats a
   170-node figure that cannot.
2. **Give it a full page** — `--paper latex-cover`, or a landscape plate via
   `\begin{landscape}`, and accept it interrupts the reading flow.
3. **Keep it as a separate sheet** at A2/A1/A0 for the wall, referenced from the document
   rather than embedded in it.

---

## 7. Fidelity notes

Two places where a print medium cannot mirror the runtime, and what is done instead:

**Alpha.** Board paints carry opacity; PDF fills do not composite against a live canvas.
Alpha is resolved against the group's own backdrop (`board.rasterClear` for board paints)
and a flat hex emitted. Identical result, no transparency in the file.

**Interaction.** `hovered`, `selectionExit`, `handle*` and `selectionPreview*` describe
states a sheet cannot have. They stay in the allowed palette — they are semio colours —
but nothing emits them.

---

## 8. Keeping it honest

```bash
python _scripts/sync_semio_tokens.py        # snapshot vs E:/semio, per-colour diff on drift
python _scripts/validate_semio_styling.py   # gate the rendered .dot and .svg
```

The gate reads rendered output rather than source, because that is what a reader sees. It
fails on: a colour outside the token set, a typeface outside the three families, a
Graphviz fallback family, `rounded` or any non-square shape, `rx`/`ry` on an SVG rect, an
`<ellipse>` or `<circle>`, and any `penwidth` that is not 0.75 / 1.5 / 2.25.

Each rendered `.dot` carries its provenance in the first two lines:

```
// semio-appearance: light
// semio-tokens: 93453c301839
```
