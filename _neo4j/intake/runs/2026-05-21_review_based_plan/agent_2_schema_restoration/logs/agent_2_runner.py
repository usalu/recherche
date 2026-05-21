"""Agent 2 runner — R2 (restore 5 demoted labels) and R10 (DeprecatedType seed).

R2 runs in Stage 2 (after Agent 1 R1 is confirmed).
R10 runs in Stage 3 (after R2 fully landed).

Usage:
    python agent_2_runner.py r2
    python agent_2_runner.py r10
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / '_scripts'))
from neo4j_env import resolve_connection  # noqa: E402

RUN_DIR = Path(__file__).resolve().parents[1]
MIG_DIR = RUN_DIR / 'migrations'
LOG_DIR = RUN_DIR / 'logs'
REPORT_DIR = RUN_DIR / 'reports'
FLAGS_DIR = RUN_DIR

DATABASE = 'mit-bestand'

DELETED_DIR = Path(__file__).resolve().parents[6] / '_neo4j' / 'intake' / 'runs' / \
              '2026-05-20_radical_quality_reset' / 'deleted'


def _get_driver():
    uri, user, password, _db = resolve_connection()
    return GraphDatabase.driver(uri, auth=(user, password))


# ─── Journal loading helpers ─────────────────────────────────────────────────

def load_journal(filename: str) -> list[dict]:
    path = DELETED_DIR / filename
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def get_nodes_by_label(nodes: list[dict], label: str) -> list[dict]:
    return [n for n in nodes if label in n.get('labels', [])]


# ─── Cypher execution helpers ─────────────────────────────────────────────────

def run_cypher_file(driver, filename: str, label: str) -> list[dict]:
    """Execute all statements in a Cypher file, return last result records."""
    text = (MIG_DIR / filename).read_text(encoding='utf-8')
    stmts = []
    for s in text.split(';'):
        stripped = s.strip()
        if not stripped:
            continue
        non_comment = [ln for ln in stripped.splitlines()
                       if ln.strip() and not ln.strip().startswith('//')]
        if non_comment:
            stmts.append(stripped)

    audit_jsonl = LOG_DIR / f'{label}_audit.jsonl'
    last_records = []
    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess, \
         audit_jsonl.open('a', encoding='utf-8') as fp:
        for i, stmt in enumerate(stmts):
            t0 = datetime.now(timezone.utc)
            try:
                result = sess.run(stmt)
                records = [r.data() for r in result]
                summary = result.consume()
                entry = {
                    'file': filename,
                    'statement_index': i,
                    'started': t0.isoformat(),
                    'elapsed_ms': round((datetime.now(timezone.utc) - t0).total_seconds() * 1000, 1),
                    'records': records[:10],
                    'counters': {k: v for k, v in summary.counters.__dict__.items() if v},
                }
                fp.write(json.dumps(entry) + '\n')
                if records:
                    print(f'  [{filename}][{i}] → {records[:3]}')
                else:
                    print(f'  [{filename}][{i}] → {entry["counters"]}')
                last_records = records
            except Exception as exc:
                entry = {
                    'file': filename, 'statement_index': i,
                    'error': str(exc), 'statement_preview': stmt[:300],
                }
                fp.write(json.dumps(entry) + '\n')
                print(f'  [{filename}][{i}] ERROR: {exc}')
                raise
    return last_records


def run_parameterized(driver, cypher: str, params: dict, label: str) -> list[dict]:
    """Run a single parameterized Cypher statement."""
    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
        result = sess.run(cypher, params)
        records = [r.data() for r in result]
        summary = result.consume()
        ctr = {k: v for k, v in summary.counters.__dict__.items() if v}
        print(f'  [{label}] → ctr={ctr}, rows={len(records)}')
        audit_jsonl = LOG_DIR / f'{label}_audit.jsonl'
        with audit_jsonl.open('a', encoding='utf-8') as fp:
            fp.write(json.dumps({
                'label': label, 'counters': ctr, 'records': records[:5]
            }) + '\n')
        return records


# ─── Phase R2 ─────────────────────────────────────────────────────────────────

def run_r2(driver):
    nodes = load_journal('phase2_5_demoted_nodes.jsonl')
    print(f'Loaded journal: {len(nodes)} nodes')

    # ── R2.a Layer ──
    print('\n--- R2.a Layer ---')
    run_cypher_file(driver, 'mig_r2_a_restore_layer.cypher', 'r2a')

    # ── R2.b LCAModule (static Cypher) ──
    print('\n--- R2.b LCAModule ---')
    run_cypher_file(driver, 'mig_r2_b_restore_lca_module.cypher', 'r2b')

    # Restore BERECHNET_NACH_MODUL from journal edges_before
    lca_nodes = get_nodes_by_label(nodes, 'LebenszyklusModul')
    bm_cypher = """
UNWIND $rows AS row
MATCH (lcm:LCAModule {id: row.lca_id})
MATCH (p:Projekt {id: row.proj_id})
MERGE (p)-[r:BERECHNET_NACH_MODUL]->(lcm)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_b_journal_edge_restore',
              r.evidence_confidence = 'teilweise_belegt',
              r.migration_origin = 'mig_r2_b_restore_lca_module'
"""
    bm_rows = []
    for n in lca_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'BERECHNET_NACH_MODUL' and e['direction'] == 'in':
                bm_rows.append({'lca_id': n['properties']['id'], 'proj_id': e['other_id']})
    if bm_rows:
        run_parameterized(driver, bm_cypher, {'rows': bm_rows}, 'r2b_berechnet')
        print(f'  BERECHNET_NACH_MODUL rows: {len(bm_rows)}')

    # Restore METHODENGRUNDLAGE_NORM from journal edges_before
    norm_cypher = """
UNWIND $rows AS row
MATCH (lcm:LCAModule {id: row.lca_id})
MATCH (norm {id: row.norm_id})
MERGE (lcm)-[r:METHODENGRUNDLAGE_NORM]->(norm)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_source_id = 'r2_b_journal_edge_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_b_restore_lca_module'
"""
    norm_rows = []
    for n in lca_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'METHODENGRUNDLAGE_NORM' and e['direction'] == 'out':
                norm_rows.append({'lca_id': n['properties']['id'], 'norm_id': e['other_id']})
    if norm_rows:
        run_parameterized(driver, norm_cypher, {'rows': norm_rows}, 'r2b_norm')
        print(f'  METHODENGRUNDLAGE_NORM rows: {len(norm_rows)}')

    # ── R2.c RechtlicheBedingung ──
    print('\n--- R2.c RechtlicheBedingung ---')
    rb_nodes = get_nodes_by_label(nodes, 'RechtlicheBedingung')

    # Create nodes from journal (parameterized)
    rb_create_cypher = """
UNWIND $rb_rows AS row
MERGE (rb:RechtlicheBedingung {id: row.id})
ON CREATE SET rb.name = row.name,
              rb.evidence_origin = 'source_curated',
              rb.evidence_basis = 'controlled_vocab',
              rb.evidence_confidence = 'belegt',
              rb.source_scope = 'r2_c_legal_restore',
              rb.migration_origin = 'mig_r2_c_restore_legal',
              rb.is_universal = row.is_universal,
              rb.scope_note = row.scope_note
"""
    rb_rows = []
    for n in rb_nodes:
        p = n['properties']
        rb_rows.append({
            'id': p['id'],
            'name': p.get('name', p['id']),
            'is_universal': p.get('is_universal', False),
            'scope_note': p.get('scope_note', ''),
        })
    run_parameterized(driver, rb_create_cypher, {'rb_rows': rb_rows}, 'r2c_nodes')

    # Run static Cypher (stubs + BELEGT_IN + ANCHORED_BY)
    run_cypher_file(driver, 'mig_r2_c_restore_legal.cypher', 'r2c')

    # Restore HAT_RECHTLICHE_BEDINGUNG from journal
    hrb_cypher = """
UNWIND $rows AS row
MATCH (rb:RechtlicheBedingung {id: row.rb_id})
MATCH (src {id: row.src_id})
MERGE (src)-[r:HAT_RECHTLICHE_BEDINGUNG]->(rb)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_c_journal_edge_restore',
              r.evidence_confidence = 'teilweise_belegt',
              r.migration_origin = 'mig_r2_c_restore_legal'
"""
    hrb_rows = []
    for n in rb_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'HAT_RECHTLICHE_BEDINGUNG' and e['direction'] == 'in':
                hrb_rows.append({'rb_id': n['properties']['id'], 'src_id': e['other_id']})
    if hrb_rows:
        run_parameterized(driver, hrb_cypher, {'rows': hrb_rows}, 'r2c_hrb')

    # Restore GILT_IN_LAND from journal
    gil_cypher = """
UNWIND $rows AS row
MATCH (rb:RechtlicheBedingung {id: row.rb_id})
MATCH (land {id: row.land_id})
MERGE (rb)-[r:GILT_IN_LAND]->(land)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_c_journal_edge_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_c_restore_legal'
"""
    gil_rows = []
    for n in rb_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'GILT_IN_LAND' and e['direction'] == 'out':
                gil_rows.append({'rb_id': n['properties']['id'], 'land_id': e['other_id']})
    if gil_rows:
        run_parameterized(driver, gil_cypher, {'rows': gil_rows}, 'r2c_gil')

    # Restore BELEGT_IN from journal (individual Quelle links per RB node)
    belegt_cypher = """
UNWIND $rows AS row
MATCH (rb:RechtlicheBedingung {id: row.rb_id})
MATCH (q:Quelle {id: row.quelle_id})
MERGE (rb)-[r:BELEGT_IN]->(q)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_c_journal_edge_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_c_restore_legal'
"""
    belegt_rb_rows = []
    for n in rb_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'BELEGT_IN' and e['direction'] == 'out':
                belegt_rb_rows.append({'rb_id': n['properties']['id'], 'quelle_id': e['other_id']})
    if belegt_rb_rows:
        run_parameterized(driver, belegt_cypher, {'rows': belegt_rb_rows}, 'r2c_belegt')

    # ── R2.d Zertifizierungssystem ──
    print('\n--- R2.d Zertifizierungssystem ---')
    run_cypher_file(driver, 'mig_r2_d_restore_certifications.cypher', 'r2d')

    # Restore HAT_ZERTIFIZIERUNG from journal
    zbs_nodes = get_nodes_by_label(nodes, 'ZertifizierungBewertungssystem')
    hatz_cypher = """
UNWIND $rows AS row
MATCH (z:Zertifizierungssystem {id: row.zbs_id})
MATCH (p:Projekt {id: row.proj_id})
MERGE (p)-[r:HAT_ZERTIFIZIERUNG]->(z)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_d_journal_edge_restore',
              r.evidence_confidence = 'belegt',
              r.evidence_excerpt = 'Restored from Phase 2.5 deletion journal',
              r.migration_origin = 'mig_r2_d_restore_certifications'
"""
    hatz_rows = []
    for n in zbs_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'HAT_ZERTIFIZIERUNG' and e['direction'] == 'in':
                hatz_rows.append({'zbs_id': n['properties']['id'], 'proj_id': e['other_id']})
    if hatz_rows:
        run_parameterized(driver, hatz_cypher, {'rows': hatz_rows}, 'r2d_hatz')

    # Restore BELEGT_IN from journal (ZBS → Quelle)
    belegt_zbs_cypher = """
UNWIND $rows AS row
MATCH (z:Zertifizierungssystem {id: row.zbs_id})
MATCH (q:Quelle {id: row.quelle_id})
MERGE (z)-[r:BELEGT_IN]->(q)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_d_journal_edge_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_d_restore_certifications'
"""
    belegt_zbs_rows = []
    for n in zbs_nodes:
        for e in n.get('edges_before', []):
            if e['type'] == 'BELEGT_IN' and e['direction'] == 'out':
                belegt_zbs_rows.append({'zbs_id': n['properties']['id'], 'quelle_id': e['other_id']})
    if belegt_zbs_rows:
        run_parameterized(driver, belegt_zbs_cypher, {'rows': belegt_zbs_rows}, 'r2d_belegt')

    # ── R2.e Tool secondary label ──
    print('\n--- R2.e Tool secondary label ---')
    run_cypher_file(driver, 'mig_r2_e_restore_tool_label.cypher', 'r2e')


# ─── Phase R2 gates ───────────────────────────────────────────────────────────

def run_r2_gates(driver) -> tuple[dict, bool]:
    gates = {
        'layer_count':              ("MATCH (l:Layer) RETURN count(l) AS c", 6, 'exact'),
        'teilt_layer_count':        ("MATCH ()-[r:TEILT_LAYER]->() RETURN count(r) AS c", 15, 'min'),
        'lca_module_count':         ("MATCH (lcm:LCAModule) RETURN count(lcm) AS c", 5, 'exact'),
        'berechnet_nach_modul':     ("MATCH ()-[r:BERECHNET_NACH_MODUL]->() RETURN count(r) AS c", 5, 'min'),
        'rb_count':                 ("MATCH (rb:RechtlicheBedingung) RETURN count(rb) AS c", 9, 'min'),
        'hat_rb_count':             ("MATCH ()-[r:HAT_RECHTLICHE_BEDINGUNG]->() RETURN count(r) AS c", 5, 'min'),
        'rb_gilt_in_land':          ("MATCH (:RechtlicheBedingung)-[r:GILT_IN_LAND]->(:Land) RETURN count(r) AS c", 3, 'min'),
        'cert_count':               ("MATCH (z:Zertifizierungssystem) RETURN count(z) AS c", 8, 'exact'),
        'hat_zert_count':           ("MATCH ()-[r:HAT_ZERTIFIZIERUNG]->() RETURN count(r) AS c", 5, 'min'),
        'tool_count':               ("MATCH (t:Tool) RETURN count(t) AS c", 8, 'exact'),
        'tool_without_software':    ("MATCH (t:Tool) WHERE NOT 'Software' IN labels(t) RETURN count(t) AS violations", 0, 'zero'),
        'layer_no_edge_violations': (
            "MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL AND NOT exists{(bt)-[:TEILT_LAYER]->(:Layer)} RETURN count(bt) AS violations",
            0, 'zero'
        ),
    }
    results = {}
    passed = True
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        for gate_name, (cypher, threshold, mode) in gates.items():
            row = s.run(cypher).single()
            val = dict(row) if row else {}
            v = val.get('c', val.get('violations', 0))
            if mode == 'exact':
                ok = (v == threshold)
            elif mode == 'min':
                ok = (v >= threshold)
            elif mode == 'zero':
                ok = (v == 0)
            else:
                ok = True
            val['_pass'] = ok
            results[gate_name] = val
            status = 'PASS' if ok else 'FAIL'
            print(f'  {status}  {gate_name}: {val} (expected {mode}={threshold})')
            if not ok:
                passed = False
    return results, passed


# ─── Phase R10 gates ──────────────────────────────────────────────────────────

def run_r10_gates(driver) -> tuple[dict, bool]:
    gates = {
        'deprecated_type_count':  ("MATCH (d:DeprecatedType) RETURN count(d) AS c", 12, 'min'),
        'distinct_kinds':         ("MATCH (d:DeprecatedType) RETURN d.kind AS kind, count(d) AS c ORDER BY kind", None, 'info'),
    }
    results = {}
    passed = True
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        for gate_name, (cypher, threshold, mode) in gates.items():
            rows = list(s.run(cypher))
            if len(rows) == 1:
                val = dict(rows[0])
                v = val.get('c', 0)
                if mode == 'min':
                    ok = (v >= threshold)
                    val['_pass'] = ok
                    if not ok:
                        passed = False
                else:
                    ok = True
                    val['_pass'] = True
            else:
                val = [dict(r) for r in rows]
                ok = True
            results[gate_name] = val
            status = 'PASS' if ok else 'FAIL'
            print(f'  {status}  {gate_name}: {val}')
    return results, passed


# ─── Phase probe ─────────────────────────────────────────────────────────────

def probe(driver) -> dict:
    state = {}
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        state['total_nodes'] = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
        state['total_rels'] = s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
        for label in ('Layer', 'LCAModule', 'RechtlicheBedingung', 'Zertifizierungssystem', 'Tool', 'DeprecatedType'):
            state[f'count_{label}'] = s.run(f'MATCH (n:{label}) RETURN count(n) AS c').single()['c']
    return state


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_phase(phase: str):
    driver = _get_driver()
    try:
        print(f'\n=== Agent 2 — Phase {phase.upper()} ===')
        pre = probe(driver)
        (LOG_DIR / f'{phase}_probe_pre.json').write_text(json.dumps(pre, indent=2), encoding='utf-8')
        print(f'Pre: {pre}')

        if phase == 'r2':
            run_r2(driver)
            gate_results, verified = run_r2_gates(driver)
        elif phase == 'r10':
            run_cypher_file(driver, 'mig_r10_deprecated_type_seed.cypher', 'r10')
            gate_results, verified = run_r10_gates(driver)
        else:
            raise SystemExit(f'Unknown phase: {phase}')

        post = probe(driver)
        (LOG_DIR / f'{phase}_probe_post.json').write_text(json.dumps(post, indent=2), encoding='utf-8')
        (LOG_DIR / f'{phase}_gates.json').write_text(json.dumps(gate_results, indent=2), encoding='utf-8')
        print(f'Post: {post}')

        flag_data = {
            'phase': phase,
            'agent': 'agent_2_schema_restoration',
            'completed_at_utc': datetime.now(timezone.utc).isoformat(),
            'verified': verified,
            'pre': pre,
            'post': post,
            'gate_results': gate_results,
        }
        (FLAGS_DIR / f'PHASE_{phase.upper()}_DONE.flag').write_text(
            json.dumps(flag_data, indent=2), encoding='utf-8'
        )

        status = 'PASS' if verified else 'FAIL'
        print(f'\n=== Phase {phase.upper()} {status} ===')
        if not verified:
            raise SystemExit(f'Phase {phase} FAILED — see logs/{phase}_gates.json')
    finally:
        driver.close()


if __name__ == '__main__':
    phase = sys.argv[1].lower() if len(sys.argv) > 1 else 'r2'
    run_phase(phase)
