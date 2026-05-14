import pathlib, sys
sys.path.insert(0, str(pathlib.Path(r'e:/recherche/_migration')))

ROOT = pathlib.Path(r'e:/recherche')
DB = ROOT / '_database'

# Check a sample
p = next((DB / 'reuse_einsatz').rglob('index.md'))
content = p.read_text(encoding='utf-8', errors='replace')

# Simple frontmatter parse
in_fm = False
data = {}
for line in content.splitlines():
    if line.strip() == '---':
        if not in_fm:
            in_fm = True
        else:
            break
    elif in_fm and ':' in line:
        key = line.split(':', 1)[0].strip()
        val = line.split(':', 1)[1].strip().strip('"')
        data[key] = val

print('pruefung_label:', repr(data.get('pruefung_label', 'NOT FOUND')))
print('huerde_label:', repr(data.get('huerde_label', 'NOT FOUND')))
print()
print('All keys:', list(data.keys()))
