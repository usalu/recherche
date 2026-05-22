"""sync_semio_tokens.py — copy the semio design tokens into this repo and detect drift.

`_neo4j/diagrams/semio/tokens.json` is a verbatim snapshot of the semio design system.
It is vendored so diagrams render identically whether or not the semio checkout is
mounted, and so a change over there is a visible, reviewable diff over here.

    python _scripts/sync_semio_tokens.py            # check for drift (read-only)
    python _scripts/sync_semio_tokens.py --pull     # re-copy from the semio checkout
    python _scripts/sync_semio_tokens.py --source D:/semio/ui/styling/tokens.json

Exit codes: 0 = in sync (or pulled), 1 = drifted, 2 = source unavailable.
Identity rules: .claude/skills/semio-styling/SKILL.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from semio_style import TOKENS_PATH, TOKENS_SOURCE  # noqa: E402


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    return (
        f"v{data.get('version')} · {len(data.get('colors', {}))} colours · "
        f"{len(data.get('strokes', {}))} strokes · {len(data.get('fontStacks', {}))} font stacks"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--pull", action="store_true", help="Overwrite the snapshot from the source")
    ap.add_argument("--source", type=Path, default=TOKENS_SOURCE, help="Path to semio tokens.json")
    args = ap.parse_args()

    print(f"snapshot: {TOKENS_PATH}")
    print(f"source:   {args.source}")
    print()

    if not args.source.is_file():
        print(f"Source not available: {args.source}", file=sys.stderr)
        if TOKENS_PATH.is_file():
            print(f"Snapshot is present and usable ({summarize(TOKENS_PATH)}).")
            print("Diagrams will render; drift cannot be checked without the semio checkout.")
        return 2

    if args.pull:
        TOKENS_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(args.source, TOKENS_PATH)
        print(f"pulled  {summarize(TOKENS_PATH)}")
        print(f"sha256  {digest(TOKENS_PATH)}")
        print("\nRe-render every diagram so the sheets match the new tokens:")
        print("  python _scripts/render_neo4j_diagram.py --all")
        return 0

    if not TOKENS_PATH.is_file():
        print("Snapshot missing. Run with --pull.", file=sys.stderr)
        return 1

    source_hash = digest(args.source)
    snapshot_hash = digest(TOKENS_PATH)
    print(f"snapshot {snapshot_hash}  {summarize(TOKENS_PATH)}")
    print(f"source   {source_hash}  {summarize(args.source)}")
    print()
    if source_hash == snapshot_hash:
        print("OK: in sync with the semio design system.")
        return 0

    print("DRIFT: the semio tokens changed. Run with --pull, then re-render.", file=sys.stderr)
    _report_color_diff(args.source, TOKENS_PATH)
    return 1


def _report_color_diff(source: Path, snapshot: Path) -> None:
    a = json.loads(source.read_text(encoding="utf-8")).get("colors", {})
    b = json.loads(snapshot.read_text(encoding="utf-8")).get("colors", {})
    for key in sorted(set(a) | set(b)):
        if a.get(key) != b.get(key):
            print(f"  colors.{key}: snapshot {b.get(key)!r} -> source {a.get(key)!r}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
