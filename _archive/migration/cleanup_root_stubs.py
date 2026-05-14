#!/usr/bin/env python3
"""
cleanup_root_stubs.py - Rename/delete/move root-level .md stubs to match schema.

Actions:
  RENAME: old -> new (Tolaria type stubs with wrong filenames)
  DELETE: orphan stubs that don't map to any entity in the ontology
  MOVE:   person entries -> _database/akteur/
  MOVE:   prompts.md -> _migration/
"""
import pathlib, shutil, subprocess, sys

ROOT = pathlib.Path(r'e:/recherche')

RENAMES = {
    # old_name: new_name  (all .md)
    'abbruchmethode.md':        'rueckbauverfahren.md',
    'aufbereitungsmethode.md':  'aufbereitungsverfahren.md',
    'bauteil.md':               'bauteiltyp.md',
    'bauteilboerse.md':         'beschaffungsweg.md',
    'gebaeude.md':              'fallstudie.md',     # fallstudie.md already exists, handled separately
    'huerde.md':                'huerde.md',         # already correct
    'pruefung.md':              'pruefung_nachweis.md',
    'reuse-strategie.md':       'reuse_strategie.md',
    'tragwerkssystem.md':       'tragwerkstyp.md',
    'verbindung.md':            'fuegung_verbindung.md',
}

# These already match or are correct: material.md, methode.md, norm.md, ort.md,
#   projekt.md, prozessphase.md, recht.md, schadstoff.md, software.md, wirtschaft.md,
#   foerderprogramm.md, logistik.md, leistungsanforderung.md, kennwert.md, datenmodell.md,
#   bericht.md, dokument.md, interview.md, tool.md, werkzeug.md

DELETES = [
    # Genuine orphans / types not in the ontology
    'beispiel.md',
    'gastprofessur.md',
    'nachhaltiges-bauen.md',
    'person.md',
    'professur.md',
]

MOVES_TO_MIGRATION = [
    'prompts.md',
]

# Person entries -> _database/akteur/
PERSON_MOVES = {
    'dirk-hebel.md':    '_database/akteur/Dirk_Hebel/index.md',
    'kerstin-mueller.md': '_database/akteur/Kerstin_Muller/index.md',
}

print("=== Root Stub Cleanup ===")
print()

# 1. Renames
print("-- Renames --")
for old, new in sorted(RENAMES.items()):
    src = ROOT / old
    dst = ROOT / new
    if not src.exists():
        print(f"  SKIP (not found): {old}")
        continue
    if src == dst:
        print(f"  OK (unchanged): {old}")
        continue
    if dst.exists():
        print(f"  SKIP (target exists, merging not automated): {old} -> {new}")
        continue
    result = subprocess.run(
        ['git', '-c', 'core.longpaths=true', 'mv', str(src), str(dst)],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode == 0:
        print(f"  RENAMED: {old} -> {new}")
    else:
        print(f"  ERROR: {old} -> {new}: {result.stderr.strip()}")

print()

# 2. Deletes
print("-- Deletes (orphan stubs) --")
for name in DELETES:
    path = ROOT / name
    if not path.exists():
        print(f"  SKIP (not found): {name}")
        continue
    result = subprocess.run(
        ['git', '-c', 'core.longpaths=true', 'rm', str(path)],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode == 0:
        print(f"  DELETED: {name}")
    else:
        print(f"  ERROR: {name}: {result.stderr.strip()}")

print()

# 3. Move prompts.md to _migration
print("-- Moves to _migration --")
for name in MOVES_TO_MIGRATION:
    src = ROOT / name
    dst = ROOT / '_migration' / name
    if not src.exists():
        print(f"  SKIP (not found): {name}")
        continue
    result = subprocess.run(
        ['git', '-c', 'core.longpaths=true', 'mv', str(src), str(dst)],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode == 0:
        print(f"  MOVED: {name} -> _migration/{name}")
    else:
        print(f"  ERROR: {name}: {result.stderr.strip()}")

print()

# 4. Person moves to _database/akteur/
print("-- Person entries -> _database/akteur --")
# Handle kerstin-müller.md (umlaut in filename)
PERSON_SOURCE_MAP = {}
for p in ROOT.iterdir():
    if p.is_file() and p.suffix == '.md':
        name_lower = p.name.lower()
        if 'dirk' in name_lower or 'hebel' in name_lower:
            PERSON_SOURCE_MAP['dirk'] = p
        elif 'kerstin' in name_lower or 'muller' in name_lower or 'm\u00fcller' in name_lower:
            PERSON_SOURCE_MAP['kerstin'] = p

PERSON_TARGETS = {
    'dirk':    ROOT / '_database/akteur/Dirk_Hebel/index.md',
    'kerstin': ROOT / '_database/akteur/Kerstin_Muller/index.md',
}

PERSON_CONTENT = {
    'dirk': '''---
entity: "akteur"
id: "Dirk_Hebel"
title: "Dirk Hebel"
build_status: "promoted_stub_cleanup"
node_kind: "core"
legacy_type: "Person"
---

# Dirk Hebel

## Rolle

Professor für Nachhaltiges Bauen, ETH Zürich.

## Verknüpfungen

- Forschungsschwerpunkt: Bauteilwiederverwendung, zirkuläres Bauen, nachwachsende Rohstoffe.
''',
    'kerstin': '''---
entity: "akteur"
id: "Kerstin_Muller"
title: "Kerstin Müller"
build_status: "promoted_stub_cleanup"
node_kind: "core"
legacy_type: "Person"
---

# Kerstin Müller

## Rolle

<!-- Bitte Rolle und Institution ergänzen. -->

## Verknüpfungen

<!-- Bitte Bezüge zu Fallstudien / Projekten ergänzen. -->
'''
}

for key, target_path in PERSON_TARGETS.items():
    src = PERSON_SOURCE_MAP.get(key)
    if src is None:
        print(f"  SKIP (source not found): {key}")
        continue
    if target_path.exists():
        print(f"  SKIP (target already exists): {target_path.relative_to(ROOT)}")
        # Still remove the root stub
        result = subprocess.run(
            ['git', '-c', 'core.longpaths=true', 'rm', str(src)],
            capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode == 0:
            print(f"    Removed root stub: {src.name}")
        continue
    # Create target dir and index.md with canonical content
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(PERSON_CONTENT[key], encoding='utf-8')
    # Git add the new file and rm the old
    subprocess.run(['git', '-c', 'core.longpaths=true', 'add', str(target_path)], cwd=ROOT)
    result = subprocess.run(
        ['git', '-c', 'core.longpaths=true', 'rm', str(src)],
        capture_output=True, text=True, cwd=ROOT
    )
    if result.returncode == 0:
        print(f"  MOVED: {src.name} -> {target_path.relative_to(ROOT)}")
    else:
        print(f"  ERROR removing source {src.name}: {result.stderr.strip()}")

print()
print("Done. Run: git commit -m 'clean root stubs'")
