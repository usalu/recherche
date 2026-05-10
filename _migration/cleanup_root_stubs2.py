#!/usr/bin/env python3
"""Finish umlaut stubs that the first script couldn't find due to encoding."""
import pathlib, subprocess

ROOT = pathlib.Path(r'e:/recherche')

# Map: find file containing this string in name -> rename/delete action
# action: ('rename', new_name) or ('delete',)
ACTIONS = []

for p in ROOT.iterdir():
    if not (p.is_file() and p.suffix == '.md'):
        continue
    n = p.name.lower()
    # gebäude.md -> already have fallstudie.md, gebäude is the old name -> delete it
    if 'geb' in n and not 'geb' in p.name[3:]:
        ACTIONS.append((p, 'delete', None))
    # bauteilbörse.md -> beschaffungsweg.md
    elif 'b' in n and 'rse' in n and 'bauteil' in n:
        ACTIONS.append((p, 'rename', 'beschaffungsweg.md'))
    # förder -> foerderprogramm.md (already correct entity name)
    elif 'rder' in n or 'rderprogramm' in n:
        ACTIONS.append((p, 'rename', 'foerderprogramm.md'))
    # hürde -> huerde.md
    elif n.startswith('h') and 'rde' in n and len(n) < 12:
        ACTIONS.append((p, 'rename', 'huerde.md'))
    # prüfung -> pruefung_nachweis.md
    elif n.startswith('pr') and 'fung' in n and 'nachweis' not in n:
        ACTIONS.append((p, 'rename', 'pruefung_nachweis.md'))
    # gebäude -> delete (fallstudie.md already exists)

for src, action, new_name in ACTIONS:
    if action == 'rename':
        dst = ROOT / new_name
        if dst.exists():
            print(f'SKIP rename (target exists): {src.name} -> {new_name}')
            # delete the source since the target already exists
            r = subprocess.run(['git', '-c', 'core.longpaths=true', 'rm', str(src)],
                               capture_output=True, text=True, cwd=ROOT)
            if r.returncode == 0:
                print(f'  Removed duplicate: {src.name}')
            continue
        r = subprocess.run(['git', '-c', 'core.longpaths=true', 'mv', str(src), str(dst)],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0:
            print(f'RENAMED: {src.name} -> {new_name}')
        else:
            print(f'ERROR: {src.name}: {r.stderr.strip()}')
    elif action == 'delete':
        r = subprocess.run(['git', '-c', 'core.longpaths=true', 'rm', str(src)],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode == 0:
            print(f'DELETED: {src.name}')
        else:
            print(f'ERROR deleting {src.name}: {r.stderr.strip()}')

# Also delete stubs that map to no canonical entity:
# tool.md -> tooltyp exists but 'tool' isn't a registered entity; keep as is
# interview.md -> not in ontology
# werkzeug.md -> not in ontology
# kennwert -> kennwertdefinition (rename)
# bericht -> dokument (or delete if dokument.md exists)
EXTRAS = [
    ('interview.md', 'delete'),
    ('werkzeug.md', 'delete'),
    ('kennwert.md', 'rename', 'kennwertdefinition.md'),
    ('bericht.md', 'delete'),   # use dokument.md instead
    ('tool.md', 'rename', 'tooltyp.md'),
    ('software.md', 'rename', 'software_digitaltool.md'),
    ('recht.md', 'rename', 'rechtliche_bedingung.md'),
]
for item in EXTRAS:
    name = item[0]
    action = item[1]
    src = ROOT / name
    if not src.exists():
        print(f'SKIP (not found): {name}')
        continue
    if action == 'delete':
        r = subprocess.run(['git', '-c', 'core.longpaths=true', 'rm', str(src)],
                           capture_output=True, text=True, cwd=ROOT)
        print(f'DELETED: {name}' if r.returncode == 0 else f'ERROR: {name}: {r.stderr.strip()}')
    elif action == 'rename':
        new_name = item[2]
        dst = ROOT / new_name
        if dst.exists():
            r = subprocess.run(['git', '-c', 'core.longpaths=true', 'rm', str(src)],
                               capture_output=True, text=True, cwd=ROOT)
            print(f'REMOVED DUPLICATE: {name}')
        else:
            r = subprocess.run(['git', '-c', 'core.longpaths=true', 'mv', str(src), str(dst)],
                               capture_output=True, text=True, cwd=ROOT)
            print(f'RENAMED: {name} -> {new_name}' if r.returncode == 0 else f'ERROR: {name}: {r.stderr.strip()}')

print()
print('Done.')
