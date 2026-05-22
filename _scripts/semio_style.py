"""Semio visual identity for rendered diagrams — the single source of colour, type and stroke.

Every value here resolves from `_neo4j/diagrams/semio/tokens.json`, a verbatim snapshot
of `E:/semio/ui/styling/tokens.json`. Nothing in a rendered diagram may use a colour,
typeface or stroke width that does not come out of this module. `validate_semio_styling.py`
enforces that on the generated output, and `.claude/skills/semio-styling/SKILL.md` states
the rule.

Paint refs are resolved exactly as `ui/styling/js/theme.ts` does — `token`, `hex`,
`mix: [a, b, ratio]` and `alpha` — so a colour computed here matches the one the semio
runtime paints.

    from semio_style import SEMIO, node_style, DiagramPaint

    SEMIO.token("primary")          # '#FF344F'
    SEMIO.board("nodeFill")         # '#EEEADB'
    SEMIO.font("sans")              # 'Anta'

Identity in one paragraph: a warm near-black-to-cream neutral ramp carries structure;
three accents carry meaning — primary red marks the focal entity (semio paints map
positions with it), secondary teal marks spatial regions (map regions), tertiary orange
marks flow (map routes). Type is Anta throughout, with Share Tech Mono for machine
provenance. Corners are square-ish rounded rectangles, strokes are 2.0, and nothing
glows, gradients or drop-shadows.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]

#: Verbatim snapshot of the semio design tokens. Re-copy with `sync_semio_tokens.py`.
TOKENS_PATH = _REPO / "_neo4j" / "diagrams" / "semio" / "tokens.json"

#: Where the snapshot came from. Drift against this file is a gate failure.
TOKENS_SOURCE = Path("E:/semio/ui/styling/tokens.json")

#: The print half of the identity. `ui/styling/tokens.json` carries screen pixels;
#: `print/tex/semio-tokens.sty` carries the point values semio actually prints with,
#: and those are the ones a PDF must use.
PRINT_TOKENS_PATH = _REPO / "_neo4j" / "diagrams" / "semio" / "print-tokens.sty"
PRINT_TOKENS_SOURCE = Path("E:/semio/print/tex/semio-tokens.sty")

#: The three semio typefaces, installed per-user from E:/semio/dist/assets/fonts.
FONT_FAMILIES = ("Anta", "Kelly Slab", "Share Tech Mono")


class SemioStyleError(RuntimeError):
    """Raised when a token, paint or font is not part of the semio identity."""


@dataclass(frozen=True)
class SemioTokens:
    """Resolved access to the semio token set."""

    colors: dict[str, str]
    strokes: dict[str, float]
    radii: dict[str, float]
    opacities: dict[str, float]
    metrics: dict[str, dict]
    font_stacks: dict[str, str]
    appearances: dict[str, dict]
    appearance: str = "light"

    # -- colours ---------------------------------------------------------

    def token(self, name: str) -> str:
        """Return the hex for a primitive token. Unknown names raise."""
        value = self.colors.get(name)
        if value is None:
            raise SemioStyleError(
                f"'{name}' is not a semio colour token. Allowed: {', '.join(sorted(self.colors))}"
            )
        return value.upper()

    def paint(self, group: str, name: str) -> str:
        """Resolve an appearance paint (board/map/canvas/chrome) to a flat hex.

        Alpha is folded onto the group's own background, because Graphviz fill and
        stroke colours in print have nothing to composite against.
        """
        refs = self.appearances[self.appearance].get(group)
        if refs is None or name not in refs:
            raise SemioStyleError(f"'{group}.{name}' is not a semio paint")
        return self._resolve(refs[name], self._group_backdrop(group))

    def board(self, name: str) -> str:
        return self.paint("board", name)

    def canvas(self, name: str) -> str:
        return self.paint("canvas", name)

    def chrome(self, name: str) -> str:
        return self.paint("chrome", name)

    def mix(self, a: str, b: str, ratio: float) -> str:
        """Blend token `a` toward token `b`; `ratio` is the weight of `a`."""
        return self._resolve({"mix": [a, b, ratio]}, self.token("light"))

    # -- type, stroke, metric --------------------------------------------

    def font(self, stack: str) -> str:
        """First family of a semio font stack — Graphviz takes one family name."""
        raw = self.font_stacks.get(stack)
        if raw is None:
            raise SemioStyleError(f"'{stack}' is not a semio font stack")
        first = raw.split(",")[0].strip().strip('"')
        if first not in FONT_FAMILIES:
            raise SemioStyleError(f"font stack '{stack}' resolved to unexpected family {first!r}")
        return first

    def stroke(self, name: str) -> float:
        if name not in self.strokes:
            raise SemioStyleError(f"'{name}' is not a semio stroke token")
        value = self.strokes[name]
        if not isinstance(value, (int, float)):
            raise SemioStyleError(f"stroke '{name}' is not scalar")
        return float(value)

    def metric(self, group: str, name: str) -> float:
        try:
            value = self.metrics[group][name]
        except KeyError as exc:
            raise SemioStyleError(f"'{group}.{name}' is not a semio metric") from exc
        return float(value)

    def opacity(self, name: str) -> float:
        if name not in self.opacities:
            raise SemioStyleError(f"'{name}' is not a semio opacity token")
        return float(self.opacities[name])

    # -- internals -------------------------------------------------------

    def _group_backdrop(self, group: str) -> str:
        key = {"board": "rasterClear", "canvas": "rasterClear", "map": "surfaceClear", "chrome": "base"}[group]
        ref = self.appearances[self.appearance][group][key]
        return self._resolve(ref, "#FFFFFF")

    def _resolve(self, ref: dict, backdrop: str) -> str:
        alpha = ref.get("alpha", 1.0)
        if "mix" in ref:
            a, b, ratio = ref["mix"]
            b_hex = backdrop if b == "transparent" else self.token(b)
            hex_value = _blend(self.token(a), b_hex, ratio)
            if b == "transparent" and "alpha" not in ref:
                alpha = 1.0
        elif "hex" in ref:
            hex_value = ref["hex"]
        elif "token" in ref:
            hex_value = self.token(ref["token"])
        else:
            raise SemioStyleError(f"paint ref needs token, hex or mix: {ref!r}")
        if alpha >= 1.0:
            return hex_value.upper()
        # Composite onto the backdrop rather than emitting an alpha channel: a printed
        # sheet has no transparency, and Graphviz PDF output would flatten it anyway.
        return _blend(hex_value, backdrop, alpha)


@lru_cache(maxsize=4)
def load_tokens(appearance: str = "light") -> SemioTokens:
    """Load the vendored semio token snapshot."""
    if appearance not in ("light", "dark"):
        raise SemioStyleError(f"appearance must be 'light' or 'dark', got {appearance!r}")
    if not TOKENS_PATH.is_file():
        raise SemioStyleError(
            f"The semio token snapshot is missing at {TOKENS_PATH}. "
            f"Restore it with: python _scripts/sync_semio_tokens.py"
        )
    data = json.loads(TOKENS_PATH.read_text(encoding="utf-8"))
    return SemioTokens(
        colors=data["colors"],
        strokes=data["strokes"],
        radii=data["radii"],
        opacities=data["opacities"],
        metrics=data["metrics"],
        font_stacks=data["fontStacks"],
        appearances=data["appearances"],
        appearance=appearance,
    )


SEMIO = load_tokens("light")


# --------------------------------------------------------------------------
# Print metrics — points, not screen pixels
# --------------------------------------------------------------------------

_STY_DECL = re.compile(r"\\newcommand\{\\semio@([\w@]+)\}\{([^}]*)\}")


@lru_cache(maxsize=1)
def print_metrics() -> dict[str, float]:
    """Point values from the vendored `semio-tokens.sty`.

    `ui/styling/tokens.json` is authored in screen pixels; the LaTeX package is
    where semio states what it prints with. A PDF must follow the latter.
    """
    if not PRINT_TOKENS_PATH.is_file():
        raise SemioStyleError(
            f"The semio print tokens are missing at {PRINT_TOKENS_PATH}. "
            f"Restore with: python _scripts/sync_semio_tokens.py --pull"
        )
    values: dict[str, float] = {}
    for name, raw in _STY_DECL.findall(PRINT_TOKENS_PATH.read_text(encoding="utf-8")):
        match = re.fullmatch(r"([\d.]+)pt", raw.strip())
        if match:
            values[name] = float(match.group(1))
    return values


def print_pt(name: str) -> float:
    """One print token in points, e.g. `stroke@hairline` → 0.75."""
    values = print_metrics()
    if name not in values:
        raise SemioStyleError(
            f"'{name}' is not a semio print token. Available: {', '.join(sorted(values))}"
        )
    return values[name]


# --------------------------------------------------------------------------
# Node painting — colour is state, never kind
# --------------------------------------------------------------------------

#: Semio's board palette carries exactly one `nodeFill` plus state variants
#: (hovered / selected / selectionExit / disabled). There is no per-kind node
#: colour anywhere in the identity, so a diagram must not invent one: the node
#: body stays neutral and the kind is stated typographically, the way semio's
#: window title tabs and heading chips state theirs.
EMPHASIS_STATES = ("normal", "focus", "highlight", "muted")

#: Labels whose nodes carry the focal accent — semio's `nodeFillSelected`.
#: Deliberately tiny: an accent that is everywhere is decoration, not emphasis.
FOCUS_LABELS = frozenset({"Projekt"})

#: Labels that never name a node's kind.
NON_PRIMARY_LABELS = frozenset({"DEPRECATED", "_Migration", "Resource"})


@dataclass(frozen=True)
class DiagramPaint:
    """The complete paint set for one node, all of it token-derived."""

    emphasis: str
    fill: str
    border: str
    font_color: str
    chip_color: str


def primary_label(labels: list[str]) -> str | None:
    """The label a node is named by — shown as its kind chip."""
    usable = [l for l in labels if l not in NON_PRIMARY_LABELS] or list(labels)
    if not usable:
        return None
    focal = [l for l in usable if l in FOCUS_LABELS]
    return sorted(focal)[0] if focal else sorted(usable)[0]


def emphasis_for_labels(labels: list[str]) -> str:
    """Nodes are `normal` unless they are the sheet's subject."""
    return "focus" if any(l in FOCUS_LABELS for l in labels) else "normal"


@lru_cache(maxsize=64)
def paint_for_emphasis(emphasis: str, appearance: str = "light") -> DiagramPaint:
    """Board paints for one emphasis state, straight from the token appearance."""
    if emphasis not in EMPHASIS_STATES:
        raise SemioStyleError(f"'{emphasis}' is not a semio emphasis state {EMPHASIS_STATES}")
    tokens = load_tokens(appearance)
    if emphasis == "focus":
        fill, border = tokens.board("nodeFillSelected"), tokens.board("nodeStrokeSelected")
    elif emphasis == "highlight":
        fill, border = (
            tokens.board("nodeFillSelectionExit"),
            tokens.board("nodeStrokeSelectionExit"),
        )
    elif emphasis == "muted":
        fill, border = tokens.board("nodeFillDisabled"), tokens.board("nodeStrokeDisabled")
    else:
        fill, border = tokens.board("nodeFill"), tokens.board("nodeStroke")
    font_color = contrast_text(fill, appearance)
    return DiagramPaint(
        emphasis=emphasis,
        fill=fill,
        border=border,
        font_color=font_color,
        # The kind chip is muted against its own body, exactly as semio mutes the
        # head of a hierarchy key against its bright tail.
        chip_color=_blend(font_color, fill, 0.55),
    )


def node_style(labels: list[str], appearance: str = "light") -> DiagramPaint:
    return paint_for_emphasis(emphasis_for_labels(labels), appearance)


#: Quantity ramp, light to dark, drawn entirely from the neutral scale.
#:
#: Encoding magnitude is not encoding kind, so this does not break the
#: colour-is-state rule — but it must stay on the neutral ramp. Hue would read as
#: a category, and semio has no categorical hue. Six steps is what a reader can
#: still rank by eye; more just looks like noise.
MAGNITUDE_RAMP = ("l-l-l-g", "light-7-9", "light-5-7", "l-g-g-g", "light-4-7", "gray")


def magnitude_fill(value: float, maximum: float, appearance: str = "light") -> tuple[str, str]:
    """Fill and text colour for a quantity, as (fill, fontcolor).

    Zero returns the sheet surface so an empty cell reads as absence, not as a
    lowest-rank value.
    """
    tokens = load_tokens(appearance)
    if value <= 0 or maximum <= 0:
        surface = tokens.board("rasterClear")
        return surface, tokens.board("labelFill")
    # Rank on a square root so the common small values stay distinguishable
    # instead of collapsing into the first step.
    fraction = (value / maximum) ** 0.5
    index = min(len(MAGNITUDE_RAMP) - 1, int(fraction * len(MAGNITUDE_RAMP)))
    fill = tokens.token(MAGNITUDE_RAMP[index])
    return fill, contrast_text(fill, appearance)


def contrast_text(background: str, appearance: str = "light") -> str:
    """Caption colour: semio `dark` or `light`, whichever stays readable in print."""
    tokens = load_tokens(appearance)
    r, g, b = _rgb(background)
    luminance = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255
    return tokens.token("dark") if luminance > 0.55 else tokens.token("light")


def allowed_colors(appearance: str = "light") -> set[str]:
    """Every hex a compliant diagram may contain, uppercase.

    Primitive tokens, every resolved appearance paint, and the caption/chip
    colours derived from them. Nothing else.
    """
    tokens = load_tokens(appearance)
    allowed = {value.upper() for value in tokens.colors.values()}
    for group in ("board", "map", "canvas", "chrome"):
        for name in tokens.appearances[appearance][group]:
            allowed.add(tokens.paint(group, name))
    for emphasis in EMPHASIS_STATES:
        paint = paint_for_emphasis(emphasis, appearance)
        allowed.update({paint.fill, paint.border, paint.font_color, paint.chip_color})
    return allowed


@lru_cache(maxsize=1)
def tokens_digest() -> str:
    """Short hash of the token snapshot, stamped into generated diagrams."""
    import hashlib

    if not TOKENS_PATH.is_file():
        return "missing"
    return hashlib.sha256(TOKENS_PATH.read_bytes()).hexdigest()[:12]


def _blend(a: str, b: str, weight_a: float) -> str:
    weight = max(0.0, min(1.0, weight_a))
    ar, ag, ab = _rgb(a)
    br, bg, bb = _rgb(b)
    return "#%02X%02X%02X" % (
        round(ar * weight + br * (1 - weight)),
        round(ag * weight + bg * (1 - weight)),
        round(ab * weight + bb * (1 - weight)),
    )


def _rgb(hex_color: str) -> tuple[int, int, int]:
    value = str(hex_color).strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", value):
        raise SemioStyleError(f"{hex_color!r} is not a 6-digit hex colour")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))
