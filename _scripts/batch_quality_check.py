import os, json, glob
from collections import Counter

base = r'e:\recherche\_neo4j\neo4j batch'
results = []

for batch_dir in sorted(os.listdir(base)):
    if not batch_dir.startswith('neo4j_batch_') or not batch_dir[12:15].isdigit():
        continue
    batch_num = int(batch_dir[12:15])
    full_path = os.path.join(base, batch_dir)
    jsonl_files = glob.glob(os.path.join(full_path, '**', '*.jsonl'), recursive=True)

    nodes, rels, bad = 0, 0, 0
    missing_id, missing_label = 0, 0
    no_props = 0
    rel_types = Counter()
    node_labels = Counter()
    has_bewertung = 0
    missing_endpoints = 0

    for f in jsonl_files:
        with open(f, encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    rt = obj.get('record_type')
                    if rt == 'node':
                        nodes += 1
                        if not obj.get('id'):
                            missing_id += 1
                        lbls = obj.get('labels', [])
                        if not lbls:
                            missing_label += 1
                        for l in lbls:
                            node_labels[l] += 1
                        props = obj.get('properties', {})
                        if not props:
                            no_props += 1
                        if props.get('bewertung'):
                            has_bewertung += 1
                    elif rt == 'rel':
                        rels += 1
                        if not obj.get('id'):
                            missing_id += 1
                        if not obj.get('from') or not obj.get('to'):
                            missing_endpoints += 1
                        rel_types[obj.get('type', '?')] += 1
                    else:
                        bad += 1
                except Exception:
                    bad += 1

    results.append({
        'batch': batch_num, 'files': len(jsonl_files),
        'nodes': nodes, 'rels': rels, 'bad': bad,
        'miss_id': missing_id, 'miss_label': missing_label,
        'no_props': no_props, 'w_bewertung': has_bewertung,
        'miss_endpoints': missing_endpoints,
        'unique_labels': len(node_labels), 'unique_rel_types': len(rel_types),
        'top_labels': node_labels.most_common(3),
        'top_rel_types': rel_types.most_common(3)
    })

# Print summary table
hdr = f"{'B':>2}  {'Files':>5}  {'Nodes':>6}  {'Rels':>6}  {'Bad':>3}  {'MissID':>6}  {'MissLbl':>7}  {'NoProps':>7}  {'UniLbl':>6}  {'UniRel':>6}  {'Bew%':>5}"
print(hdr)
print('-' * len(hdr))
for r in results:
    bew_pct = f"{100*r['w_bewertung']//r['nodes'] if r['nodes'] else 0}%"
    print(f"{r['batch']:>2}  {r['files']:>5}  {r['nodes']:>6}  {r['rels']:>6}  {r['bad']:>3}  {r['miss_id']:>6}  {r['miss_label']:>7}  {r['no_props']:>7}  {r['unique_labels']:>6}  {r['unique_rel_types']:>6}  {bew_pct:>5}")

print()
print("Detail per batch:")
for r in results:
    print(f"  Batch {r['batch']:02d}: top_labels={r['top_labels']}  top_rels={r['top_rel_types']}")
    if r['miss_endpoints']:
        print(f"           WARNING: {r['miss_endpoints']} rels missing from/to endpoints!")
