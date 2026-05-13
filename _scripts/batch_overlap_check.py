"""
Analyze batches 015-019: overlaps, duplicates, inconsistencies vs 001-014.
"""
import sys, io, os, json, glob
from collections import defaultdict, Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'e:\recherche\_neo4j\neo4j batch'

def iter_batch(batch_num):
    """Yield all parsed JSONL records from a batch (skip batch_006 cumulative package)."""
    batch_dir = os.path.join(BASE, f'neo4j_batch_{batch_num:03d}_exports')
    if not os.path.isdir(batch_dir):
        return
    # Skip the cumulative neo4j_complete_repo_package subfolder in batch 006
    for f in sorted(glob.glob(os.path.join(batch_dir, '**', '*.jsonl'), recursive=True)):
        if 'neo4j_complete_repo_package' in f:
            continue
        with open(f, encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    yield json.loads(line), f
                except Exception:
                    pass

# ── Build baseline index from batches 001-014 ────────────────────────────────
print("Loading batches 001-014 as baseline …")
baseline_nodes = {}      # id -> {labels, properties, batch}
baseline_rels  = {}      # id -> {type, from, to, properties, batch}
baseline_ct_nodes = defaultdict(set)   # label -> set of ids

for b in range(1, 15):
    for obj, fpath in iter_batch(b):
        rt = obj.get('record_type')
        oid = obj.get('id')
        if rt == 'node' and oid:
            baseline_nodes[oid] = {'labels': obj.get('labels', []), 'props': obj.get('properties', {}), 'batch': b}
            for lbl in obj.get('labels', []):
                baseline_ct_nodes[lbl].add(oid)
        elif rt == 'rel' and oid:
            baseline_rels[oid] = {'type': obj.get('type'), 'from': obj.get('from'), 'to': obj.get('to'), 'props': obj.get('properties', {}), 'batch': b}

print(f"  Baseline: {len(baseline_nodes):,} nodes, {len(baseline_rels):,} rels\n")

# ── Analyze batches 015-019 ───────────────────────────────────────────────────
SEP = '=' * 64

for b in range(15, 20):
    print(f"\n{SEP}")
    print(f"  BATCH {b:03d}")
    print(SEP)

    new_nodes, new_rels = {}, {}
    dup_nodes, dup_rels = [], []
    conflict_nodes = []   # same id, different labels or key props
    missing_from, missing_to = [], []
    bad_records = 0

    for obj, fpath in iter_batch(b):
        rt = obj.get('record_type')
        oid = obj.get('id')
        if not oid:
            bad_records += 1
            continue

        if rt == 'node':
            new_nodes[oid] = {'labels': obj.get('labels', []), 'props': obj.get('properties', {}), 'file': os.path.basename(fpath)}
            # Check against baseline
            if oid in baseline_nodes:
                base = baseline_nodes[oid]
                same_labels = set(base['labels']) == set(obj.get('labels', []))
                base_name = base['props'].get('name')
                new_name  = obj.get('properties', {}).get('name')
                if not same_labels or (base_name and new_name and base_name != new_name):
                    conflict_nodes.append({
                        'id': oid,
                        'base_batch': base['batch'],
                        'base_labels': base['labels'],
                        'new_labels': obj.get('labels', []),
                        'base_name': base_name,
                        'new_name': new_name
                    })
                else:
                    dup_nodes.append(oid)

        elif rt == 'rel':
            new_rels[oid] = {'type': obj.get('type'), 'from': obj.get('from'), 'to': obj.get('to'), 'props': obj.get('properties', {})}
            if oid in baseline_rels:
                dup_rels.append(oid)
            # Check dangling endpoints (not in baseline AND not in this batch)
            frm = obj.get('from')
            to  = obj.get('to')
            if frm and frm not in baseline_nodes and frm not in new_nodes:
                missing_from.append({'rel_id': oid, 'missing': frm})
            if to and to not in baseline_nodes and to not in new_nodes:
                missing_to.append({'rel_id': oid, 'missing': to})
        else:
            bad_records += 1

    # Intra-batch duplicate node IDs
    # (already handled above since new_nodes dedups — check file count)
    node_label_dist = Counter()
    rel_type_dist   = Counter()
    for n in new_nodes.values():
        for lbl in n['labels']:
            node_label_dist[lbl] += 1
    for r in new_rels.values():
        rel_type_dist[r['type']] += 1

    # Cross-batch dup within 015-019
    cross_dup = {}
    if b > 15:
        # Already accumulated in new_nodes from current batch — check against prior new batches
        # (This is done via baseline below since we add to baseline after each batch)
        pass

    print(f"  Records   : {len(new_nodes):>4} nodes  {len(new_rels):>5} rels  {bad_records} bad")
    print(f"  Dup nodes (already in 001-{b-1:03d}): {len(dup_nodes)}")
    print(f"  Dup rels  (already in 001-{b-1:03d}): {len(dup_rels)}")
    print(f"  Conflicting nodes (same id, diff label/name): {len(conflict_nodes)}")
    print(f"  Dangling rel endpoints (missing from+to): {len(missing_from)+len(missing_to)}")

    if dup_nodes:
        # sample
        sample = dup_nodes[:10]
        print(f"\n  Duplicate node IDs (sample of {min(10,len(dup_nodes))}):")
        for nid in sample:
            bl = baseline_nodes[nid]
            print(f"    {nid}  (first in batch {bl['batch']:03d}, labels={bl['labels']})")

    if dup_rels:
        sample = dup_rels[:5]
        print(f"\n  Duplicate rel IDs (sample of {min(5,len(dup_rels))}):")
        for rid in sample:
            bl = baseline_rels[rid]
            print(f"    {rid}  (first in batch {bl['batch']:03d})")

    if conflict_nodes:
        print(f"\n  CONFLICTS:")
        for c in conflict_nodes[:10]:
            print(f"    {c['id']}")
            print(f"      base (batch {c['base_batch']:03d}): labels={c['base_labels']} name={c['base_name']}")
            print(f"      new  (batch {b:03d}): labels={c['new_labels']} name={c['new_name']}")

    if missing_from or missing_to:
        all_missing = missing_from[:5] + missing_to[:5]
        print(f"\n  Dangling endpoints (sample):")
        for m in all_missing[:8]:
            print(f"    rel {m['rel_id']}  -> missing node: {m['missing']}")

    print(f"\n  Node labels in this batch:")
    for lbl, cnt in node_label_dist.most_common():
        net_new = cnt - sum(1 for nid in new_nodes if lbl in new_nodes[nid]['labels'] and nid in baseline_nodes)
        print(f"    {lbl:<35} {cnt:>4} total  ({net_new} genuinely new)")

    print(f"\n  Rel types in this batch:")
    for t, cnt in rel_type_dist.most_common(15):
        print(f"    {t:<40} {cnt:>4}")

    # Check for Projekt nodes: property consistency (must have name, bewertung)
    projekt_nodes = {nid: nd for nid, nd in new_nodes.items() if 'Projekt' in nd['labels']}
    if projekt_nodes:
        print(f"\n  Projekt nodes: {len(projekt_nodes)}")
        for nid, nd in sorted(projekt_nodes.items()):
            bew = nd['props'].get('bewertung', 'MISSING')
            nm  = nd['props'].get('name', 'MISSING')
            status = nd['props'].get('projektstatus_text', 'MISSING')
            flag = '⚠' if bew == 'MISSING' or nm == 'MISSING' else ''
            print(f"    {nid:<60} bew={bew} {flag}")

    # Extend baseline for cross-batch dup detection in subsequent iterations
    for nid, nd in new_nodes.items():
        if nid not in baseline_nodes:
            baseline_nodes[nid] = {'labels': nd['labels'], 'props': nd['props'], 'batch': b}
    for rid, rd in new_rels.items():
        if rid not in baseline_rels:
            baseline_rels[rid] = {'type': rd['type'], 'from': rd['from'], 'to': rd['to'], 'props': rd['props'], 'batch': b}

print(f"\n{SEP}")
print("  CROSS-BATCH SUMMARY 015-019")
print(SEP)
print("  (Each batch's duplicates counted against all prior batches 001–N-1)")
print(f"\n  Final cumulative: {len(baseline_nodes):,} unique node IDs, {len(baseline_rels):,} unique rel IDs")
