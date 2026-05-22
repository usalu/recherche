"""validate_semio_styling.py — the styling gate. Fails on anything outside the semio identity.

Checks the rendered artifacts, not the source, because that is what a reader actually
sees. A diagram passes only if every colour literal resolves to a semio token or a
token-derived paint, and every typeface is one of the three semio families.

    python _scripts/validate_semio_styling.py                 # gate the whole diagrams dir
    python _scripts/validate_semio_styling.py --path a.dot b.svg
    python _scripts/validate_semio_styling.py --list-allowed

Exit codes: 0 = compliant, 1 = violations found, 2 = the token snapshot is unusable.
Identity rules: .claude/skills/semio-styling/SKILL.md
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from semio_style import (  # noqa: E402
    FONT_FAMILIES,
    SemioStyleError,
    allowed_colors,
    load_tokens,
    print_metrics,
)

DEFAULT_DIR = _REPO / "_neo4j" / "exports" / "diagrams"
CHECKED_SUFFIXES = (".dot", ".svg")

_HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
_DOT_FONT = re.compile(r'font(?:name)?\s*=\s*"([^"]+)"', re.IGNORECASE)
_SVG_FONT = re.compile(r'font-family\s*[:=]\s*"?([^";,)]+)', re.IGNORECASE)
_HTML_FACE = re.compile(r'FACE\s*=\s*"([^"]+)"', re.IGNORECASE)

#: Graphviz emits these itself; they are not authored colour choices.
NEUTRAL_LITERALS = {"#000000", "#FFFFFF"}

#: Graphviz's own fallback when a family is missing — its presence means a font
#: failed to resolve, which is a gate failure even though the file looks fine.
FORBIDDEN_FONTS = {"Times", "Times New Roman", "Helvetica", "Arial", "Tahoma", "Sans", "serif", "sans-serif"}

#: semio sets tcolorbox `arc=0mm` and its stylesheet holds no non-zero radius.
#: Nothing in this identity is rounded, and nothing is an ellipse.
FORBIDDEN_STYLES = {"rounded", "diagonals", "striped", "wedged", "radial"}
ALLOWED_SHAPES = {"box", "rect", "rectangle", "none", "plaintext", "plain", "square", "point"}

_DOT_STYLE = re.compile(r'\bstyle\s*=\s*"([^"]*)"')
_DOT_SHAPE = re.compile(r'\bshape\s*=\s*"?([A-Za-z]+)"?')
_DOT_PENWIDTH = re.compile(r'\bpenwidth\s*=\s*([\d.]+)')
_SVG_ROUNDED = re.compile(r'<rect[^>]*\br[xy]\s*=\s*"(?!0*\.?0*")')
_SVG_ROUND_SHAPE = re.compile(r"<(ellipse|circle)\b")


class Violation:
    def __init__(self, path: Path, line: int, kind: str, value: str, detail: str):
        self.path, self.line, self.kind, self.value, self.detail = path, line, kind, value, detail

    def __str__(self) -> str:
        rel = self.path.relative_to(_REPO) if _REPO in self.path.parents else self.path
        return f"{rel}:{self.line}: {self.kind} {self.value!r} — {self.detail}"


def normalize(hex_value: str) -> str:
    """Uppercase and expand to #RRGGBB; drop any alpha byte pair."""
    value = hex_value.lstrip("#")
    if len(value) in (4, 8):
        value = value[: len(value) - len(value) // 4]
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    return "#" + value.upper()


def check_file(path: Path, allowed: set[str], strokes: set[float]) -> list[Violation]:
    violations: list[Violation] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    stroke_list = ", ".join(f"{s}pt" for s in sorted(strokes))

    for number, line in enumerate(text.splitlines(), start=1):
        # -- form: nothing in semio is rounded, and every stroke is a print token
        if path.suffix == ".dot":
            for style in _DOT_STYLE.findall(line):
                for part in (p.strip() for p in style.split(",")):
                    if part in FORBIDDEN_STYLES:
                        violations.append(
                            Violation(path, number, "style", part,
                                      "semio sets arc=0mm everywhere — nothing is rounded")
                        )
            for shape in _DOT_SHAPE.findall(line):
                if shape.lower() not in ALLOWED_SHAPES:
                    violations.append(
                        Violation(path, number, "shape", shape,
                                  f"only square forms are semio {sorted(ALLOWED_SHAPES)}")
                    )
            for width in _DOT_PENWIDTH.findall(line):
                if round(float(width), 3) not in strokes:
                    violations.append(
                        Violation(path, number, "penwidth", width,
                                  f"not a semio print stroke ({stroke_list})")
                    )
        else:
            if _SVG_ROUNDED.search(line):
                violations.append(
                    Violation(path, number, "shape", "rounded rect",
                              "rx/ry on a rect — semio has no corner radius")
                )
            for element in _SVG_ROUND_SHAPE.findall(line):
                violations.append(
                    Violation(path, number, "shape", f"<{element}>",
                              "semio draws square forms, not ellipses")
                )

        for raw in _HEX.findall(line):
            value = normalize(raw)
            if value in NEUTRAL_LITERALS or value in allowed:
                continue
            violations.append(
                Violation(path, number, "colour", raw, "not a semio token or token-derived paint")
            )

        families: list[str] = []
        if path.suffix == ".dot":
            families += _DOT_FONT.findall(line) + _HTML_FACE.findall(line)
        else:
            families += _SVG_FONT.findall(line)
        for family in families:
            name = family.strip().strip("'\"")
            if name in FONT_FAMILIES:
                continue
            if name in FORBIDDEN_FONTS:
                violations.append(
                    Violation(path, number, "font", name, "Graphviz fallback — the semio font is not installed")
                )
            else:
                violations.append(
                    Violation(path, number, "font", name, f"not a semio family {FONT_FAMILIES}")
                )
    return violations


def collect(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            for suffix in CHECKED_SUFFIXES:
                files.extend(sorted(path.glob(f"*{suffix}")))
        elif path.suffix in CHECKED_SUFFIXES:
            files.append(path)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--path", nargs="+", type=Path, default=[DEFAULT_DIR],
                    help=f"Files or directories to gate (default: {DEFAULT_DIR})")
    ap.add_argument(
        "--appearance", choices=("light", "dark", "both"), default="both",
        help="Palette to gate against. 'both' (default) accepts either appearance's "
             "paints, since both are semio; pick one to enforce a single appearance.",
    )
    ap.add_argument("--list-allowed", action="store_true", help="Print the allowed palette and exit")
    args = ap.parse_args()

    appearances = ("light", "dark") if args.appearance == "both" else (args.appearance,)
    try:
        allowed: set[str] = set()
        for appearance in appearances:
            allowed |= allowed_colors(appearance)
        tokens = load_tokens(appearances[0])
    except SemioStyleError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 2

    if args.list_allowed:
        print(f"{len(allowed)} colours allowed in the {args.appearance} appearance:\n")
        for name, value in sorted(tokens.colors.items(), key=lambda kv: kv[1]):
            print(f"  {value.upper()}  {name}")
        print(f"\nfonts: {', '.join(FONT_FAMILIES)}")
        return 0

    files = collect(args.path)
    if not files:
        print(f"No .dot or .svg files found under {', '.join(str(p) for p in args.path)}",
              file=sys.stderr)
        return 1

    strokes = {
        round(value, 3)
        for name, value in print_metrics().items()
        if name.startswith("stroke@")
    }
    violations: list[Violation] = []
    for path in files:
        violations.extend(check_file(path, allowed, strokes))

    if violations:
        print(f"FAIL: {len(violations)} styling violation(s) in {len(files)} file(s)\n",
              file=sys.stderr)
        for violation in violations[:60]:
            print(f"  {violation}", file=sys.stderr)
        if len(violations) > 60:
            print(f"  … and {len(violations) - 60} more", file=sys.stderr)
        print("\nEvery colour must be a semio token from _neo4j/diagrams/semio/tokens.json "
              "and every typeface one of " + ", ".join(FONT_FAMILIES) + ".", file=sys.stderr)
        print("See .claude/skills/semio-styling/SKILL.md", file=sys.stderr)
        return 1

    print(f"OK: {len(files)} file(s) compliant with the semio identity "
          f"({len(allowed)} allowed colours, {args.appearance} appearance).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
