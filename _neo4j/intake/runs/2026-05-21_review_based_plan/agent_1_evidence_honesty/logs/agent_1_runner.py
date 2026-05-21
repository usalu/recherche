"""Agent 1 runner — R1 (evidence_origin split) and R8 (DataIssue seed).

R1 is run in Stage 1. R8 is run in Stage 4 (orchestrator gates it).

Usage:
    python agent_1_runner.py r1
    python agent_1_runner.py r8
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


def _get_driver():
    uri, user, password, _db = resolve_connection()
    return GraphDatabase.driver(uri, auth=(user, password))


def probe_pre(driver):
    pre = {}
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        pre['total_rels'] = s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
        pre['total_nodes'] = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
        pre['origin_distribution'] = {
            row['origin']: row['c']
            for row in s.run(
                'MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL '
                'RETURN r.evidence_origin AS origin, count(r) AS c ORDER BY c DESC'
            )
        }
        pre['confidence_distribution'] = {
            row['conf']: row['c']
            for row in s.run(
                'MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL '
                'RETURN r.evidence_confidence AS conf, count(r) AS c ORDER BY c DESC'
            )
        }
        pre['is_bookkeeping_count'] = s.run(
            "MATCH ()-[r {is_bookkeeping:true}]->() RETURN count(r) AS c"
        ).single()['c']
    return pre


def probe_post(driver):
    post = {}
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        post['total_rels'] = s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c']
        post['total_nodes'] = s.run('MATCH (n) RETURN count(n) AS c').single()['c']
        post['origin_distribution'] = {
            row['origin']: row['c']
            for row in s.run(
                'MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL '
                'RETURN r.evidence_origin AS origin, count(r) AS c ORDER BY c DESC'
            )
        }
        post['confidence_distribution'] = {
            row['conf']: row['c']
            for row in s.run(
                'MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL '
                'RETURN r.evidence_confidence AS conf, count(r) AS c ORDER BY c DESC'
            )
        }
        post['is_bookkeeping_count'] = s.run(
            "MATCH ()-[r {is_bookkeeping:true}]->() RETURN count(r) AS c"
        ).single()['c']
    return post


def execute_migration(driver, migration_filename: str, phase: str):
    """Execute all statements in the migration file and log each to audit JSONL."""
    migration_text = (MIG_DIR / migration_filename).read_text(encoding='utf-8')
    # Split on semicolons, filter empty/comment-only blocks
    raw_stmts = migration_text.split(';')
    statements = []
    for s in raw_stmts:
        stripped = s.strip()
        if not stripped:
            continue
        # Keep if it has at least one non-comment line
        non_comment = [ln for ln in stripped.splitlines() if ln.strip() and not ln.strip().startswith('//')]
        if non_comment:
            statements.append(stripped)

    audit_jsonl = LOG_DIR / f'{phase}_audit.jsonl'
    print(f'[{phase}] Executing {len(statements)} statements from {migration_filename}')
    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess, \
         audit_jsonl.open('w', encoding='utf-8') as audit_fp:
        for i, stmt in enumerate(statements):
            t0 = datetime.now(timezone.utc)
            try:
                result = sess.run(stmt)
                records = [r.data() for r in result]
                summary = result.consume()
                entry = {
                    'statement_index': i,
                    'started': t0.isoformat(),
                    'elapsed_ms': round((datetime.now(timezone.utc) - t0).total_seconds() * 1000, 1),
                    'records': records[:10],
                    'counters': {k: v for k, v in summary.counters.__dict__.items() if v},
                }
                audit_fp.write(json.dumps(entry) + '\n')
                if records:
                    print(f'  stmt[{i}] → {records[:3]}')
                else:
                    ctr = entry['counters']
                    print(f'  stmt[{i}] → {ctr}')
            except Exception as exc:
                entry = {
                    'statement_index': i,
                    'error': str(exc),
                    'statement_preview': stmt[:300],
                }
                audit_fp.write(json.dumps(entry) + '\n')
                print(f'  stmt[{i}] ERROR: {exc}')
                raise


def run_r1_gates(driver) -> dict:
    gates = {
        'old_curated_remaining': {
            'cypher': "MATCH ()-[r]->() WHERE r.evidence_origin='curated' RETURN count(r) AS violations",
            'expect_zero': True,
        },
        'bookkeeping_in_confidence': {
            'cypher': "MATCH ()-[r]->() WHERE r.evidence_confidence='bookkeeping' RETURN count(r) AS violations",
            'expect_zero': True,
        },
        'origin_enum_violation': {
            'cypher': (
                "MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL "
                "AND NOT r.evidence_origin IN ['source_curated','topology_synthesized',"
                "'registry_derived','inferred','external_unfolded'] "
                "RETURN count(r) AS violations"
            ),
            'expect_zero': True,
        },
        'confidence_enum_violation': {
            'cypher': (
                "MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL "
                "AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert'] "
                "RETURN count(r) AS violations"
            ),
            'expect_zero': True,
        },
        'is_bookkeeping_count': {
            'cypher': "MATCH ()-[r {is_bookkeeping:true}]->() RETURN count(r) AS c",
            'expect_min': 698,  # 703 ±5
        },
        'topology_synthesized_count': {
            'cypher': "MATCH ()-[r]->() WHERE r.evidence_origin='topology_synthesized' RETURN count(r) AS c",
            'expect_min': 254,
        },
        'registry_derived_count': {
            'cypher': "MATCH ()-[r]->() WHERE r.evidence_origin='registry_derived' RETURN count(r) AS c",
            'expect_min': 1500,
        },
        'reuse_rule_contradiction': {
            'cypher': (
                "MATCH (rule:ReuseRule)-[r]->() "
                "WHERE r.evidence_origin='inferred' AND r.evidence_confidence='belegt' "
                "RETURN count(r) AS violations"
            ),
            'expect_zero': True,
        },
    }
    results = {}
    passed = True
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        for gate_name, gate in gates.items():
            row = s.run(gate['cypher']).single()
            val = dict(row) if row else {}
            results[gate_name] = val
            if gate.get('expect_zero'):
                v = val.get('violations', val.get('c', 0))
                ok = (v == 0)
            elif gate.get('expect_min') is not None:
                v = val.get('c', 0)
                ok = (v >= gate['expect_min'])
            else:
                ok = True
            results[gate_name]['_pass'] = ok
            if not ok:
                passed = False
                print(f'  FAIL  {gate_name}: {val}')
            else:
                print(f'  PASS  {gate_name}: {val}')
    return results, passed


def run_r8_gates(driver) -> tuple[dict, bool]:
    gates = {
        'data_issue_total': {
            'cypher': "MATCH (i:DataIssue) RETURN count(i) AS c",
            'expect_min': 1000,
        },
        'q1_topology_synthesis': {
            'cypher': "MATCH (i:DataIssue {kind:'q1_topology_synthesis'}) RETURN count(i) AS c",
            'expect_min': 200,
        },
        'pollutant_inference': {
            'cypher': "MATCH (i:DataIssue {kind:'pollutant_inference'}) RETURN count(i) AS c",
            'expect_min': 500,
        },
        'severity_distribution': {
            'cypher': "MATCH (i:DataIssue) RETURN i.severity AS severity, count(i) AS c ORDER BY i.severity",
            'expect_zero': False,
        },
    }
    results = {}
    passed = True
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        for gate_name, gate in gates.items():
            rows = list(s.run(gate['cypher']))
            if rows and len(rows) == 1:
                val = dict(rows[0])
            else:
                val = [dict(r) for r in rows]
            results[gate_name] = val
            if gate.get('expect_min') is not None and isinstance(val, dict):
                v = val.get('c', 0)
                ok = (v >= gate['expect_min'])
                results[gate_name]['_pass'] = ok
                if not ok:
                    passed = False
                    print(f'  FAIL  {gate_name}: {val}')
                else:
                    print(f'  PASS  {gate_name}: {val}')
            else:
                print(f'  INFO  {gate_name}: {val}')
    return results, passed


def run_phase(phase: str):
    driver = _get_driver()
    try:
        print(f'\n=== Agent 1 — Phase {phase.upper()} ===')
        print('Pre-flight probe...')
        pre = probe_pre(driver)
        (LOG_DIR / f'{phase}_probe_pre.json').write_text(json.dumps(pre, indent=2), encoding='utf-8')
        print(f'  total_rels={pre["total_rels"]}, total_nodes={pre["total_nodes"]}')
        print(f'  origin_distribution={pre["origin_distribution"]}')
        print(f'  confidence_distribution={pre["confidence_distribution"]}')

        if phase == 'r1':
            execute_migration(driver, 'mig_r1_evidence_origin_split.cypher', phase)
        elif phase == 'r8':
            execute_migration(driver, 'mig_r8_data_issue_seed.cypher', phase)
        else:
            raise SystemExit(f'Unknown phase: {phase}')

        print('Post-flight probe...')
        post = probe_post(driver)
        (LOG_DIR / f'{phase}_probe_post.json').write_text(json.dumps(post, indent=2), encoding='utf-8')
        print(f'  total_rels={post["total_rels"]} (delta={post["total_rels"]-pre["total_rels"]})')
        print(f'  origin_distribution={post["origin_distribution"]}')

        print('Acceptance gates...')
        if phase == 'r1':
            gate_results, verified = run_r1_gates(driver)
        else:
            gate_results, verified = run_r8_gates(driver)

        (LOG_DIR / f'{phase}_gates.json').write_text(json.dumps(gate_results, indent=2), encoding='utf-8')

        flag_data = {
            'phase': phase,
            'agent': 'agent_1_evidence_honesty',
            'completed_at_utc': datetime.now(timezone.utc).isoformat(),
            'verified': verified,
            'pre_total_rels': pre['total_rels'],
            'post_total_rels': post['total_rels'],
            'pre_origin_distribution': pre['origin_distribution'],
            'post_origin_distribution': post['origin_distribution'],
            'pre_confidence_distribution': pre['confidence_distribution'],
            'post_confidence_distribution': post['confidence_distribution'],
            'is_bookkeeping_count': post['is_bookkeeping_count'],
            'gate_results': gate_results,
        }
        (FLAGS_DIR / f'PHASE_{phase.upper()}_DONE.flag').write_text(
            json.dumps(flag_data, indent=2), encoding='utf-8'
        )

        status = 'PASS' if verified else 'FAIL'
        print(f'\n=== Phase {phase.upper()} {status} ===')
        if not verified:
            raise SystemExit(f'Phase {phase} verification FAILED — see logs/{phase}_gates.json')
    finally:
        driver.close()


if __name__ == '__main__':
    phase = sys.argv[1].lower() if len(sys.argv) > 1 else 'r1'
    run_phase(phase)
