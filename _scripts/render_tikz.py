"""Render semio TikZ figures to PDF with Tectonic.

Compiles a standalone `.tex` from `_neo4j/diagrams/tikz/` into a cropped PDF in
`_neo4j/exports/diagrams/`, ready to drop into a semio `Figure` window with
`\\SemioImage[fit=none]{...}`. Regenerates the token file and runs the source
styling gate around the build.

Engine: Tectonic (the same self-contained XeTeX the semio print system uses).
Found on PATH, else the semio cache at E:/semio/.repo/cache/tectonic/*/tectonic.exe.
No system TeX install is required.

Usage:
  python _scripts/render_tikz.py huerden-baum      # one figure (name without .tex)
  python _scripts/render_tikz.py --all             # every standalone .tex in the dir
  python _scripts/render_tikz.py --list            # what would build
"""
from __future__ import annotations

import argparse
import glob
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "_scripts"
TIKZ_DIR = REPO / "_neo4j" / "diagrams" / "tikz"
OUT_DIR = REPO / "_neo4j" / "exports" / "diagrams"
TECTONIC_CACHE_GLOB = "E:/semio/.repo/cache/tectonic/*/tectonic.exe"


def find_tectonic() -> str | None:
    from shutil import which
    found = which("tectonic")
    if found:
        return found
    cands = sorted(glob.glob(TECTONIC_CACHE_GLOB))
    return cands[-1] if cands else None


def standalone_docs() -> list[str]:
    names = []
    for tex in sorted(TIKZ_DIR.glob("*.tex")):
        if tex.name.startswith("semio-tikz-tokens"):
            continue
        if "\\documentclass" in tex.read_text(encoding="utf-8", errors="replace"):
            names.append(tex.stem)
    return names


def run(cmd: list[str], **kw) -> int:
    return subprocess.run(cmd, **kw).returncode


def compile_one(name: str, tectonic: str) -> bool:
    tex = TIKZ_DIR / f"{name}.tex"
    if not tex.is_file():
        print(f"[skip] {tex} not found", file=sys.stderr)
        return False
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        tectonic, "--outdir", str(OUT_DIR), "--keep-logs",
        "--chatter", "minimal",
        "-Z", f"search-path={TIKZ_DIR}",
        str(tex),
    ]
    print(f"[tectonic] {name}.tex -> _neo4j/exports/diagrams/{name}.pdf")
    rc = run(cmd, cwd=str(TIKZ_DIR))
    if rc != 0:
        log = OUT_DIR / f"{name}.log"
        print(f"[FAIL] tectonic exit {rc}. Log: {log}", file=sys.stderr)
        return False
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("names", nargs="*", help="figure names (without .tex)")
    ap.add_argument("--all", action="store_true", help="build every standalone figure")
    ap.add_argument("--list", action="store_true", help="list buildable figures and exit")
    args = ap.parse_args()

    docs = standalone_docs()
    if args.list:
        print("\n".join(docs) or "(none)")
        return 0

    targets = docs if args.all else args.names
    if not targets:
        print("Nothing to build. Pass a figure name or --all. Available:", file=sys.stderr)
        print("  " + ", ".join(docs), file=sys.stderr)
        return 1

    tectonic = find_tectonic()
    if not tectonic:
        print("FAIL: Tectonic not found.", file=sys.stderr)
        print("  Expected on PATH or at E:/semio/.repo/cache/tectonic/<ver>/tectonic.exe.", file=sys.stderr)
        print("  Get it via the semio build once:  bun E:/semio/print/script.ts fonts", file=sys.stderr)
        print("  or install:  winget install TectonicProject.Tectonic", file=sys.stderr)
        return 2
    print(f"[engine] {tectonic}")

    # keep the generated tokens fresh before compiling
    if run([sys.executable, str(SCRIPTS / "gen_semio_tikz_tokens.py")]) != 0:
        return 1

    ok = all(compile_one(n, tectonic) for n in targets)
    if not ok:
        return 1

    # source styling gate on the compiled figures
    gate = SCRIPTS / "validate_semio_tikz.py"
    if gate.is_file():
        rc = run([sys.executable, str(gate), "--path", *[str(TIKZ_DIR / f"{n}.tex") for n in targets]])
        if rc != 0:
            return 1
    print(f"OK: {len(targets)} figure(s) rendered to _neo4j/exports/diagrams/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
