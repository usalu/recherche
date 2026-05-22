# Graphviz setup

Graphviz is the CLI renderer behind the printable Neo4j diagrams. It renders DOT to
SVG **and** PDF directly, so no browser, screenshot tool or PDF-conversion library
is needed or wanted here.

Rendering diagrams from the graph: [`_neo4j/diagrams/README.md`](../_neo4j/diagrams/README.md).
This file covers only the Graphviz install itself.

## What is installed

| | |
|---|---|
| Version | 15.1.0 (20260618.0150) |
| Executable | `C:\Program Files\Graphviz\bin\dot.exe` |
| Installed with | `winget install Graphviz.Graphviz` (Windows 11) |
| Layout engines | `dot`, `neato`, `fdp`, `sfdp`, `circo`, `twopi` |
| Python dependencies | none — the helpers use only the standard library |

The winget installer does **not** put Graphviz on `PATH`. `C:\Program Files\Graphviz\bin`
was appended to the **user** `PATH` (`HKCU:\Environment`) after installing. Existing
shells keep the old `PATH` until they are restarted.

### Installing on another machine

```bash
# Windows
winget install Graphviz.Graphviz

# macOS
brew install graphviz

# Ubuntu / Debian
sudo apt-get update && sudo apt-get install -y graphviz

# Fedora
sudo dnf install graphviz

# Arch Linux
sudo pacman -S graphviz
```

## Verify by hand

```bash
dot -V
neato -V
fdp -V
sfdp -V
circo -V
twopi -V
```

Each prints `… graphviz version 15.1.0 …`. To confirm the output formats:

```bash
dot -Tsvg -o out.svg   # then type the DOT source and press Ctrl+Z, Enter (Ctrl+D on POSIX)
dot -Tpdf -o out.pdf
```

Bare `dot -Tsvg` waits on stdin — use the repo check below instead of guessing.

## Verify with the repo check

```bash
python _scripts/check_graphviz.py
python _scripts/check_graphviz.py --json
```

It reports availability, version, executable path, how the executable was resolved,
every layout engine, and whether SVG and PDF output actually work (rendered into a
throwaway temp directory — nothing is written into the repo).

Exit codes: `0` usable, `1` installed but an engine or format failed, `2` not found.

## Smoke test

```bash
python _scripts/validate_graphviz_smoke.py
```

Renders one small `Neo4j -> Graphviz` graph and checks both artifacts are valid and
non-empty. Output goes to the repo scratch area, which `.gitignore` already excludes:

```text
_tmp/graphviz-smoke-test.svg
_tmp/graphviz-smoke-test.pdf
```

These files are regenerable — they are not fixtures and are never committed.

## Reusable helper

`_scripts/graphviz_env.py` is the shared module, in the same role as `neo4j_env.py`.
Import it instead of shelling out ad hoc:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from graphviz_env import GraphvizNotFoundError, render, run_graphviz, probe_graphviz

render('digraph G { a -> b; }', '_tmp/example.svg', fmt='svg')
render('digraph G { a -> b; }', '_tmp/example.pdf', fmt='pdf', engine='neato')
```

It resolves `dot` in this order: `GRAPHVIZ_DOT` → `PATH` → known install directories.
Graphviz is always invoked as an argument list with `shell=False`; stdout is kept as
bytes so binary formats such as PDF survive, and stderr is captured and decoded.
A missing engine raises `GraphvizNotFoundError` with install instructions.

## Troubleshooting — `dot` is not found on PATH

1. **You installed it in this shell session.** `PATH` is read at process start.
   Open a new terminal, or refresh the current PowerShell session:

   ```powershell
   $env:Path = [Environment]::GetEnvironmentVariable('Path','Machine') + ';' +
               [Environment]::GetEnvironmentVariable('Path','User')
   ```

2. **Confirm where it landed.**

   ```powershell
   Get-ChildItem "C:\Program Files\Graphviz\bin\dot.exe"
   ```

   ```bash
   which dot        # POSIX
   ```

3. **Add it to PATH permanently** (user scope, no admin required):

   ```powershell
   $key = 'HKCU:\Environment'
   $raw = (Get-Item $key).GetValue('Path','',[Microsoft.Win32.RegistryValueOptions]::DoNotExpandEnvironmentNames)
   Set-ItemProperty -Path $key -Name Path -Type ExpandString `
     -Value ($raw.TrimEnd(';') + ';C:\Program Files\Graphviz\bin')
   ```

   Use `-Type ExpandString` and the raw registry value, otherwise entries such as
   `%USERPROFILE%\go\bin` are frozen to their current expansion.

4. **Skip PATH entirely.** Point the helper straight at the executable — this also
   works for a portable or non-standard install:

   ```powershell
   $env:GRAPHVIZ_DOT = 'C:\Program Files\Graphviz\bin\dot.exe'   # or the bin directory
   python _scripts/check_graphviz.py
   ```

5. **`Format: "pdf" not recognized`** means a stripped-down Graphviz build. Reinstall
   from the official package rather than adding a PDF-conversion library.

6. **Plugin/config errors** (`Warning: Could not load … no such file or directory`)
   are fixed by rebuilding the plugin registry once, as Administrator:

   ```powershell
   & 'C:\Program Files\Graphviz\bin\dot.exe' -c
   ```
