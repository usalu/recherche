import pathlib, collections

ROOT = pathlib.Path(r'e:/recherche')
DB = ROOT / '_database'

field_counts = collections.Counter()
sample_values = collections.defaultdict(list)

for p in (DB / 'reuse_einsatz').rglob('index.md'):
    content = p.read_text(encoding='utf-8', errors='replace')
    in_fm = False
    for line in content.splitlines():
        if line.strip() == '---':
            if not in_fm:
                in_fm = True
            else:
                break
        elif in_fm and ':' in line and not line.startswith(' '):
            key = line.split(':', 1)[0].strip()
            val = line.split(':', 1)[1].strip().strip('"')
            field_counts[key] += 1
            if len(sample_values[key]) < 2:
                sample_values[key].append(val)

print('Frontmatter fields in reuse_einsatz nodes:')
for key, count in sorted(field_counts.items(), key=lambda x: -x[1]):
    examples = ' | '.join(sample_values[key][:2])
    print(f'  [{count:3}] {key}: {examples[:80]}')
