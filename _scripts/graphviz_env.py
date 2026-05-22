"""Shared Graphviz discovery and invocation helpers (env override + PATH + known install dirs).

Mirrors the role of `neo4j_env.py`: a thin, dependency-free module other scripts
import instead of shelling out ad hoc. Graphviz is invoked as a plain argument
list without a shell, and both stdout and stderr are captured.

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from graphviz_env import probe_graphviz, render, require_engine

Environment override:
    GRAPHVIZ_DOT  full path to the `dot` executable, or the directory holding it
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

DOT_ENV_VAR = "GRAPHVIZ_DOT"

#: Layout engines shipped with Graphviz that this repo relies on.
LAYOUT_ENGINES = ("dot", "neato", "fdp", "sfdp", "circo", "twopi")

#: Searched when the engine is installed but not exported on PATH.
_FALLBACK_BIN_DIRS = (
    r"C:\Program Files\Graphviz\bin",
    r"C:\Program Files (x86)\Graphviz\bin",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Graphviz", "bin"),
    "/opt/homebrew/bin",
    "/usr/local/bin",
    "/usr/bin",
)

_VERSION = re.compile(r"version\s+(\S+)", re.IGNORECASE)


class GraphvizNotFoundError(RuntimeError):
    """Raised when a Graphviz layout engine cannot be located."""


@dataclass(frozen=True)
class GraphvizRun:
    """Result of one Graphviz invocation. `stdout` stays bytes so -Tpdf works."""

    argv: list[str]
    returncode: int
    stdout: bytes
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def find_engine(engine: str = "dot") -> str | None:
    """Return the absolute path to `engine`, or None if it cannot be found."""
    if engine == "dot":
        override = os.environ.get(DOT_ENV_VAR, "").strip().strip('"')
        if override:
            candidate = Path(override)
            if candidate.is_dir():
                candidate = candidate / _exe_name("dot")
            if candidate.is_file():
                return str(candidate)

    found = shutil.which(engine)
    if found:
        return found

    for directory in _FALLBACK_BIN_DIRS:
        if not directory:
            continue
        candidate = Path(directory) / _exe_name(engine)
        if candidate.is_file():
            return str(candidate)
    return None


def require_engine(engine: str = "dot") -> str:
    """Return the path to `engine` or raise GraphvizNotFoundError with install hints."""
    path = find_engine(engine)
    if path:
        return path
    raise GraphvizNotFoundError(
        f"Graphviz '{engine}' was not found on PATH, in {DOT_ENV_VAR}, or in the known "
        f"install directories.\n"
        f"Install it (Windows: `winget install Graphviz.Graphviz`; Debian/Ubuntu: "
        f"`sudo apt-get install -y graphviz`; macOS: `brew install graphviz`), then reopen "
        f"the shell so PATH is refreshed, or set {DOT_ENV_VAR} to the full path of the "
        f"executable.\n"
        f"See _scripts/GRAPHVIZ_SETUP.md."
    )


def run_graphviz(
    args: list[str],
    *,
    engine: str = "dot",
    source: str | None = None,
    timeout: int = 60,
) -> GraphvizRun:
    """Run `engine` with `args`, feeding `source` on stdin. No shell, no globbing."""
    executable = require_engine(engine)
    argv = [executable, *args]
    proc = subprocess.run(
        argv,
        input=source.encode("utf-8") if source is not None else None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        timeout=timeout,
    )
    return GraphvizRun(
        argv=argv,
        returncode=proc.returncode,
        stdout=proc.stdout or b"",
        stderr=(proc.stderr or b"").decode("utf-8", errors="replace").strip(),
    )


def engine_version(engine: str = "dot") -> str:
    """Return the version string reported by `engine -V` (Graphviz prints it on stderr)."""
    run = run_graphviz(["-V"], engine=engine)
    banner = run.stderr or run.stdout.decode("utf-8", errors="replace").strip()
    if not run.ok and not banner:
        raise GraphvizNotFoundError(f"'{engine} -V' failed with exit code {run.returncode}.")
    match = _VERSION.search(banner)
    return match.group(1) if match else banner


def render(
    source: str,
    out_path: Path | str,
    *,
    fmt: str,
    engine: str = "dot",
    extra_args: list[str] | None = None,
    timeout: int = 300,
) -> Path:
    """Render DOT `source` to `out_path` in `fmt`. Raises RuntimeError on engine failure."""
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    args = [f"-T{fmt}", *(extra_args or []), "-o", str(out)]
    run = run_graphviz(args, engine=engine, source=source, timeout=timeout)
    if not run.ok:
        raise RuntimeError(
            f"{engine} -T{fmt} failed with exit code {run.returncode}: {run.stderr or '(no stderr)'}"
        )
    return out


def probe_graphviz() -> dict:
    """Report availability, version, executable path and per-engine status."""
    dot_path = find_engine("dot")
    report: dict = {
        "available": dot_path is not None,
        "dot_path": dot_path,
        "version": None,
        "engines": {},
        "source": _which_source(dot_path),
    }
    if dot_path is None:
        return report

    report["version"] = engine_version("dot")
    for engine in LAYOUT_ENGINES:
        path = find_engine(engine)
        report["engines"][engine] = {
            "available": path is not None,
            "path": path,
            "version": engine_version(engine) if path else None,
        }
    return report


def _exe_name(engine: str) -> str:
    return f"{engine}.exe" if sys.platform == "win32" else engine


def _which_source(dot_path: str | None) -> str:
    if dot_path is None:
        return "not found"
    if os.environ.get(DOT_ENV_VAR, "").strip():
        return f"{DOT_ENV_VAR} environment variable"
    return "PATH" if shutil.which("dot") else "known install directory"
