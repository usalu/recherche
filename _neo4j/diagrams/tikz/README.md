# semio TikZ figures

Author hand-drawn diagrams (trees, networks, schemas) that carry the **semio**
visual identity and drop straight into the semio LaTeX report — same colours,
strokes and type as the Graphviz sheets. Governed by
[`.claude/skills/semio-styling`](../../../.claude/skills/semio-styling/SKILL.md).

## What's here

| File | Role |
|---|---|
| `semio-tikz.sty` | the style package — node/edge/chip/focus/hub/register styles + `\SemioNode` |
| `semio-tikz-tokens.tex` | **generated** colours + strokes + sizes (do not hand-edit) |
| `fonts/` | vendored Anta + Share Tech Mono (OFL) so it compiles anywhere |
| `template.tex` | blank starter — copy it to begin a figure |
| `huerden-baum.tex` | worked example (a branch of the Hürden taxonomy) |

Scripts (in `_scripts/`): `render_tikz.py` (compile), `gen_semio_tikz_tokens.py`
(regenerate tokens), `validate_semio_tikz.py` (styling gate).

## Author a figure

1. `cp template.tex myfigure.tex` and edit the `tikzpicture`.
2. Use only the semio styles below — no raw hex, no rounded corners, no italics.

| Style | Use |
|---|---|
| `semio node` | a leaf/entity: neutral fill, hairline border, square corners, Anta caption |
| `semio hub` | a category/parent (lighter body) |
| `semio focus` | the **one** focal entity — semio's red accent, `2.25pt` border. Use sparingly |
| `semio edge` / `semio edge strong` / `semio arrow` | hairline / `1.5pt` / arrowed connector |
| `semio chip` / `semio mono` | kind chip (muted) / machine text (Share Tech Mono) |
| `semio register` | a legend box |
| `\SemioNode{Kind}{Caption}` | kind chip above a caption, left-aligned (node label) |

Colour is **state, never kind** — do not map a label/domain to a hue. State the
kind with the chip. Encode a quantity only on the neutral ramp.

## Compile

```bash
python _scripts/render_tikz.py huerden-baum     # -> _neo4j/exports/diagrams/huerden-baum.pdf
python _scripts/render_tikz.py --all            # every figure here
python _scripts/render_tikz.py --list           # what would build
```

Engine is **Tectonic** (the same self-contained XeTeX the semio print system
uses) — found on `PATH` or the semio cache at
`E:/semio/.repo/cache/tectonic/*/tectonic.exe`. No system TeX install needed.
`render_tikz.py` regenerates the tokens and runs the styling gate around the build.

## Embed in the semio report

The output is a cropped PDF. Put it in a semio `Figure` window at 1:1:

```latex
\begin{Figure}[title=Hürden-Taxonomie]
  \SemioImage[fit=none]{../../recherche/_neo4j/exports/diagrams/huerden-baum.pdf}
\end{Figure}
```

Include at `fit=none` (1:1) so the figure's 9.6pt type matches the document; the
window supplies the title and border, so don't draw your own frame.

## The gate (run after any change)

```bash
python _scripts/gen_semio_tikz_tokens.py --check   # tokens match the semio source
python _scripts/render_tikz.py --all               # everything re-renders
python _scripts/validate_semio_tikz.py             # nothing outside the identity
```

The TikZ gate reads the **source** (not a raster): fontspec-by-path makes a
missing font a hard compile error rather than a silent fallback, and every colour
is a named semio token — so the source is the honest surface. It fails on raw
hex, a non-semio colour name, a rounded/elliptical form, an off-list stroke, or
italics/bold.

## Notes

- Only three faces exist in print: **Anta** (text), **Share Tech Mono** (machine),
  Noto Emoji. No italic face — emphasis is a colour swap.
- `semio-tikz-tokens.tex` is generated from `_neo4j/diagrams/semio/tokens.json`;
  after an upstream token change run `sync_semio_tokens.py --pull` then
  `gen_semio_tikz_tokens.py`.
- Dark appearance is not wired yet (v1 is light-only).
