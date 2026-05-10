#!/usr/bin/env python3
"""
archive_legacy_folders.py - Move all root-level legacy folders to _archive/legacy/.

Exclusions:
  - Gebäude/ (canonical source, user keeps it)
  - gebaeude/ (user will update separately)
  - _database/, _migration/, _archive/, .git, .ralph-tui, .gemini, node_modules
"""
import pathlib, subprocess, sys

ROOT = pathlib.Path(r'e:/recherche')
ARCHIVE = ROOT / '_archive' / 'legacy'

SKIP = {
    '_database', '_migration', '_archive', '_system',
    '.git', '.ralph-tui', '.gemini', 'node_modules',
    'Gebäude', 'gebaeude',
}

# Also skip folders that start with _ but should be archived separately
UNDERSCORE_ARCHIVE = {'_extract', '_graph', '_manual_review'}

folders_to_archive = []
for p in sorted(ROOT.iterdir()):
    if not p.is_dir():
        continue
    if p.name in SKIP:
        continue
    if p.name.startswith('.'):
        continue
    folders_to_archive.append(p)

print(f"Will archive {len(folders_to_archive)} folders to {ARCHIVE.relative_to(ROOT)}/")
print()

# Create archive directory
ARCHIVE.mkdir(parents=True, exist_ok=True)

errors = []
for folder in folders_to_archive:
    target = ARCHIVE / folder.name
    if target.exists():
        print(f"  SKIP (target exists): {folder.name}/")
        continue

    result = subprocess.run(
        ['git', '-c', 'core.longpaths=true', 'mv', str(folder), str(target)],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    if result.returncode == 0:
        print(f"  MOVED: {folder.name}/ -> _archive/legacy/{folder.name}/")
    else:
        err = result.stderr.strip()
        print(f"  ERROR: {folder.name}/: {err}")
        errors.append((folder.name, err))

print()
if errors:
    print(f"Errors: {len(errors)}")
    for name, err in errors:
        print(f"  {name}: {err}")
else:
    print("All moves succeeded.")

print()
print("Run: git commit -m 'archive legacy root folders'")
