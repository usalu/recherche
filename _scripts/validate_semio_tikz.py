"""validate_semio_tikz.py — the styling gate for semio TikZ source.

TikZ figures compile with fontspec-by-path (a missing font is a hard error, not a
silent fallback) and use named xcolor tokens, so the compliant surface is the
`.tex` source, not a rendered raster. This gate fails on anything outside the
semio identity: raw hex, a colour name that is not a semio token, a rounded or
elliptical form, an off-list stroke width, or italics/bold.

    python _scripts/validate_semio_tikz.py               # gate every figure
    python _scripts/validate_semio_tikz.py --path a.tex

Exit: 0 compliant, 1 violations, 2 token files unusable.
Identity rules: .claude/skills/semio-styling/SKILL.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TIKZ_DIR = REPO / "_neo4j" / "diagrams" / "tikz"
TOKENS_TEX = TIKZ_DIR / "semio-tikz-tokens.tex"
PRINT_TOKENS = REPO / "_neo4j" / "diagrams" / "semio" / "print-tokens.sty"

_DEFINECOLOR = re.compile(r"\\definecolor\{([^}]+)\}")
_STROKE_MACRO = re.compile(r"\\newcommand\{\\(semio\w*)\}\{([\d.]+)pt\}")

_RAW_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:HTML|RGB|rgb|cmyk|Gray)\s*\}?\s*\{")
_COLOR_USE = re.compile(r"(?:draw|fill|text|color)\s*=\s*([A-Za-z][\w\-]*(?:!\d+(?:![A-Za-z][\w\-]*)?)*)")
_TEXTCOLOR = re.compile(r"\\textcolor\{([^}]+)\}")
_LINEWIDTH_PT = re.compile(r"line width\s*=\s*([\d.]+)pt")
_FORBIDDEN = {
    "rounded corners": "semio has no corner radius — use sharp corners",
    "\\textit": "no italic face exists in semio — emphasis is a colour swap",
    "\\itshape": "no italic face exists in semio",
    "\\emph": "standalone \\emph italicises — recolour to semioforeground instead",
    "\\textbf": "Anta ships one weight — do not rely on bold",
}
_ROUND_SHAPE = re.compile(r"\b(circle|ellipse|oval)\b")
NEUTRAL = {"black", "white", "none"}


def load_allowed_colors() -> set[str]:
    names: set[str] = set(NEUTRAL)
    for f in (TOKENS_TEX, PRINT_TOKENS):
        if not f.is_file():
            raise FileNotFoundError(f)
        names |= set(_DEFINECOLOR.findall(f.read_text(encoding="utf-8")))
    return names


#: Only these macros are stroke widths; the size macros (…size) are type, not strokes.
_STROKE_NAMES = {"semiohairline", "semiodefaultstroke", "semiofocuswidth"}


def load_allowed_strokes() -> tuple[set[float], set[str]]:
    widths: set[float] = set()
    macros: set[str] = set()
    for name, val in _STROKE_MACRO.findall(TOKENS_TEX.read_text(encoding="utf-8")):
        if name not in _STROKE_NAMES:
            continue
        macros.add(name)
        widths.add(round(float(val), 3))
    return widths, macros


def color_atoms(value: str) -> list[str]:
    # semionodefill!50!semiobase -> ['semionodefill', 'semiobase']
    return [a for a in re.split(r"!|\d+", value) if a]


def check(path: Path, colors: set[str], strokes: set[float]) -> list[str]:
    out: list[str] = []
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        stripped = line.split("%", 1)[0]  # ignore comments
        if _RAW_HEX.search(stripped):
            out.append(f"{path.name}:{n}: raw colour — every hex must come from a semio token")
        for frag, why in _FORBIDDEN.items():
            if frag in stripped:
                out.append(f"{path.name}:{n}: {frag!r} — {why}")
        for m in _ROUND_SHAPE.findall(stripped):
            out.append(f"{path.name}:{n}: {m!r} — semio draws square forms, not round ones")
        for val in _COLOR_USE.findall(stripped) + [c for g in _TEXTCOLOR.findall(stripped) for c in [g]]:
            for atom in color_atoms(val):
                if atom not in colors:
                    out.append(f"{path.name}:{n}: colour {atom!r} — not a semio token")
        for w in _LINEWIDTH_PT.findall(stripped):
            if round(float(w), 3) not in strokes:
                out.append(f"{path.name}:{n}: line width {w}pt — not a semio print stroke "
                           f"({', '.join(str(s) for s in sorted(strokes))}pt)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--path", nargs="+", type=Path, default=None,
                    help="figure .tex files (default: every standalone figure in the tikz dir)")
    args = ap.parse_args()

    try:
        colors = load_allowed_colors()
        strokes, _ = load_allowed_strokes()
    except FileNotFoundError as exc:
        print(f"FAIL: token file missing: {exc}. Run gen_semio_tikz_tokens.py / sync_semio_tokens.py",
              file=sys.stderr)
        return 2

    if args.path:
        files = [p for p in args.path if p.is_file()]
    else:
        files = [t for t in sorted(TIKZ_DIR.glob("*.tex"))
                 if not t.name.startswith("semio-tikz-tokens")
                 and "\\documentclass" in t.read_text(encoding="utf-8", errors="replace")]
    if not files:
        print("No figure .tex files to gate.", file=sys.stderr)
        return 1

    violations: list[str] = []
    for f in files:
        violations += check(f, colors, strokes)

    if violations:
        print(f"FAIL: {len(violations)} styling violation(s) in {len(files)} figure(s)\n", file=sys.stderr)
        for v in violations[:60]:
            print(f"  {v}", file=sys.stderr)
        print("\nSee .claude/skills/semio-styling/SKILL.md", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} figure(s) compliant with the semio identity "
          f"({len(colors)} colour tokens, strokes {sorted(strokes)}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
