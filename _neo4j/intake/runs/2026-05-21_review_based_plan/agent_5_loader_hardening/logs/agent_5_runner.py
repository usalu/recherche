"""Agent 5 runner — R7 (Loader hardening)

R7.a: Merge 16 qu_*_dossier nodes into q_<slug>_md nodes (APOC mergeNodes).
R7.b: Resolve orphan case_markdown Quellen (create missing Programm + BELEGT_IN edges).
R7.d: Populate Quelle.text_content + drift validator (DataIssue nodes).
R7.c: GATED — runs after Agent 4 R4. Not run by this script unless --r7c flag given.

Usage:
    python agent_5_runner.py r7ab    # Runs R7.a + R7.b (Stage 1)
    python agent_5_runner.py r7d     # Runs R7.d (Stage 2, parallel-safe)
    python agent_5_runner.py all     # Runs r7ab + r7d
"""
import json
import re
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
WORKSPACE = Path(__file__).resolve().parents[6]
DATABASE = 'mit-bestand'


def _get_driver():
    uri, user, password, _db = resolve_connection()
    return GraphDatabase.driver(uri, auth=(user, password))


def _write_jsonl(path: Path, entry: dict):
    with path.open('a', encoding='utf-8') as fp:
        fp.write(json.dumps(entry, ensure_ascii=False) + '\n')


def run_cypher_file(driver, filename: str, label: str) -> list[dict]:
    text = (MIG_DIR / filename).read_text(encoding='utf-8')
    stmts = []
    for s in text.split(';'):
        stripped = s.strip()
        non_comment = [ln for ln in stripped.splitlines()
                       if ln.strip() and not ln.strip().startswith('//')]
        if non_comment:
            stmts.append(stripped)
    last = []
    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
        for i, stmt in enumerate(stmts):
            result = sess.run(stmt)
            records = [r.data() for r in result]
            ctr = {k: v for k, v in result.consume().counters.__dict__.items() if v}
            _write_jsonl(LOG_DIR / f'{label}_audit.jsonl',
                         {'file': filename, 'stmt': i, 'counters': ctr, 'records': records[:5]})
            if records:
                print(f'  [{filename}][{i}] {records[:3]}')
            else:
                print(f'  [{filename}][{i}] ctr={ctr}')
            last = records
    return last


def run_write(driver, cypher: str, params: dict, label: str) -> list[dict]:
    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
        result = sess.run(cypher, params)
        records = [r.data() for r in result]
        ctr = {k: v for k, v in result.consume().counters.__dict__.items() if v}
        _write_jsonl(LOG_DIR / f'{label}_audit.jsonl',
                     {'label': label, 'counters': ctr, 'rows': len(records)})
        print(f'  [{label}] ctr={ctr} rows={len(records)}')
        return records


def probe(driver) -> dict:
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        return {
            'total_nodes': s.run('MATCH (n) RETURN count(n) AS c').single()['c'],
            'total_rels':  s.run('MATCH ()-[r]->() RETURN count(r) AS c').single()['c'],
            'case_markdown': s.run("MATCH (q:Quelle {quelltyp:'case_markdown'}) RETURN count(q) AS c").single()['c'],
            'qu_dossier': s.run("MATCH (q:Quelle) WHERE q.id STARTS WITH 'qu_' RETURN count(q) AS c").single()['c'],
            'with_text_content': s.run(
                "MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE q.text_content IS NOT NULL RETURN count(q) AS c"
            ).single()['c'],
            'drift_issues': s.run(
                "MATCH (d:DataIssue {kind:'dossier_uses_retired_type'}) RETURN count(d) AS c"
            ).single()['c'],
        }


# ─── R7.a — Merge qu_* nodes ─────────────────────────────────────────────────

# Manual mapping: (old_id, new_id) — established by inspecting live graph
DUAL_NAMING_PAIRS = [
    ('qu_batch1_elementa_dossier',            'q_elementa_walkeweg_basel_md'),
    ('qu_batch1_schaerenmoosstrasse_dossier', 'q_schaerenmoosstrasse_zuerich_projekt_menage_a_trois_md'),
    ('qu_batch1_umar_dossier',                'q_umar_unit_nest_empa_duebendorf_md'),
    ('qu_beware_dossier',                     'q_reallabor_be_ware_md'),
    ('qu_careno_becircular_dossier',          'q_careno_be_circular_brussels_md'),
    ('qu_circl_pavilion_dossier',             'q_circl_pavilion_amsterdam_md'),
    ('qu_eth_mas_dfab_dossier',               'q_eth_circular_construction_programme_md'),
    ('qu_fcrbe_dossier',                      'q_fcrbe_facilitating_circulation_reclaimed_building_elements_md'),
    ('qu_granby_workshop_dossier',            'q_granby_workshop_liverpool_md'),
    ('qu_lysp8_basel_dossier',                'q_lysp8_basel_md'),
    ('qu_meduni_mariannengasse_dossier',      'q_meduni_campus_mariannengasse_wien_md'),
    ('qu_rebridge_dossier',                   'q_rebridge_structural_reuse_md'),
    ('qu_refair_dossier',                     'q_refair_bordeaux_md'),
    ('qu_reusehoefe_dossier',                 'q_re_use_hoefe_wien_md'),
    ('qu_reuselogistics_dossier',             'q_reuse_logistics_md'),
    ('qu_stuttgart210_dossier',               'q_stuttgart_210_md'),
]

MERGE_CYPHER = """
MATCH (q_new:Quelle {id: $new_id}), (q_old:Quelle {id: $old_id})
CALL apoc.refactor.mergeNodes([q_new, q_old], {
  properties: 'discard',
  mergeRels: true
}) YIELD node
SET node.aliases = CASE WHEN node.aliases IS NULL THEN [$old_id]
                        ELSE [x IN node.aliases WHERE x <> $old_id] + [$old_id] END,
    node.migration_origin = coalesce(node.migration_origin, '') + ' | r7_a_dual_naming_merge'
RETURN node.id AS canonical_id, node.aliases AS aliases
"""


def run_r7a(driver):
    print('\n=== R7.a: Merge dual-naming Quelle pairs ===')
    merge_log = []
    for old_id, new_id in DUAL_NAMING_PAIRS:
        print(f'  Merging {old_id} → {new_id}')
        with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
            # Verify both nodes exist first
            check = sess.run(
                'MATCH (a:Quelle {id:$old}) MATCH (b:Quelle {id:$new}) RETURN a.id AS a, b.id AS b',
                old=old_id, new=new_id
            ).single()
            if not check:
                print(f'  SKIP — one or both nodes missing: {old_id} / {new_id}')
                _write_jsonl(LOG_DIR / 'r7a_audit.jsonl',
                             {'old': old_id, 'new': new_id, 'status': 'skipped_missing'})
                continue
            result = sess.run(MERGE_CYPHER, old_id=old_id, new_id=new_id)
            row = result.single()
            if row:
                entry = {'old': old_id, 'new': new_id, 'status': 'merged',
                         'canonical_id': row['canonical_id'], 'aliases': row['aliases']}
                print(f'    merged → {row["canonical_id"]} aliases={row["aliases"]}')
            else:
                entry = {'old': old_id, 'new': new_id, 'status': 'no_result'}
                print(f'    WARNING: merge returned no result')
            merge_log.append(entry)
            _write_jsonl(LOG_DIR / 'r7a_audit.jsonl', entry)
    (LOG_DIR / 'r7a_pairs.json').write_text(json.dumps(merge_log, indent=2, ensure_ascii=False), encoding='utf-8')
    # Run audit queries
    run_cypher_file(driver, 'mig_r7_a_dual_naming_merge.cypher', 'r7a')
    return merge_log


def run_r7a_gates(driver) -> tuple[dict, bool]:
    gates = {
        'qu_dossier_remaining': (
            "MATCH (q:Quelle) WHERE q.id STARTS WITH 'qu_' AND q.id ENDS WITH '_dossier' RETURN count(q) AS c",
            0, 'zero'
        ),
        'q_md_with_qu_alias': (
            "MATCH (q:Quelle) WHERE q.aliases IS NOT NULL AND any(a IN q.aliases WHERE a STARTS WITH 'qu_') RETURN count(q) AS c",
            16, 'exact'
        ),
        'case_markdown_after_merge': (
            "MATCH (q:Quelle {quelltyp:'case_markdown'}) RETURN count(q) AS c",
            100, 'min'  # was 116, minus 16 = 100
        ),
    }
    return _run_gates(driver, gates)


# ─── R7.b — Resolve orphans ───────────────────────────────────────────────────

# Full mapping: case_markdown Quelle id → existing Projekt/Programm id
# These are the orphans that will still exist after R7.a, plus batch_1.
ORPHAN_LINKS = [
    # These are orphaned AFTER R7.a (the qu_* merge doesn't bring a Projekt/Programm link)
    ('p_architecture_of_reuse_brussels',        'q_architecture_of_reuse_brussels_md'),
    ('p_schaerenmoosstrasse_zuerich',            'q_batch_1_md'),   # batch container → primary project
    ('p_circl_abn_amro',                        'q_circl_abn_amro_urban_mining_md'),
    ('prog_fcrbe',                              'q_fcrbe_facilitating_circulation_reclaimed_building_elements_md'),
    ('p_interreg_nwe_fcrbe',                    'q_interreg_nwe_fcrbe_md'),
    ('p_obk_27',                                'q_obk_27_md'),
    ('p_rcmi_concular',                         'q_rcmi_concular_md'),
    ('p_reallabor_be_ware',                     'q_reallabor_be_ware_md'),
    ('p_refair_bordeaux_reemploi_platform',     'q_refair_bordeaux_md'),
    ('p_vandkunsten_component_reuse',           'q_vandkunsten_component_reuse_programme_md'),
    ('p_reuse_in_construction_zhaw',            'q_zhaw_reuse_in_construction_md'),
    # New Programm p_eth_circular_construction_programme handled in static Cypher
    # Also link the existing student Projekts to it if desired
]

LINK_CYPHER = """
UNWIND $rows AS row
MATCH (e {id: row.entity_id})
MATCH (q:Quelle {id: row.quelle_id, quelltyp: 'case_markdown'})
MERGE (e)-[r:BELEGT_IN]->(q)
ON CREATE SET
  r.evidence_origin = 'topology_synthesized',
  r.evidence_basis = 'slug_match',
  r.evidence_confidence = 'teilweise_belegt',
  r.migration_origin = 'mig_r7_b_resolve_orphans'
"""


def run_r7b(driver):
    print('\n=== R7.b: Resolve orphan dossiers ===')
    # Run static Cypher (new Programm + ETH link)
    run_cypher_file(driver, 'mig_r7_b_resolve_orphans.cypher', 'r7b')
    # Parameterized bulk BELEGT_IN
    rows = [{'entity_id': e_id, 'quelle_id': q_id} for e_id, q_id in ORPHAN_LINKS]
    run_write(driver, LINK_CYPHER, {'rows': rows}, 'r7b_links')
    print(f'  Created BELEGT_IN edges for {len(rows)} orphan pairs')


def run_r7b_gates(driver) -> tuple[dict, bool]:
    gates = {
        'eth_prog_exists': (
            "MATCH (p:Programm {id:'p_eth_circular_construction_programme'}) RETURN count(p) AS c",
            1, 'exact'
        ),
        'case_markdown_still_orphan': (
            "MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE NOT exists{MATCH (n)-[:BELEGT_IN]->(q) WHERE n:Projekt OR n:Programm} RETURN count(q) AS c",
            0, 'zero'
        ),
        'eth_prog_has_belegt_in': (
            "MATCH (p:Programm {id:'p_eth_circular_construction_programme'})-[:BELEGT_IN]->(:Quelle) RETURN count(p) AS c",
            1, 'min'
        ),
    }
    return _run_gates(driver, gates)


# ─── R7.d — text_content + drift validator ────────────────────────────────────

RETIRED_TYPES = [
    'LebenszyklusModul', 'ZertifizierungBewertungssystem',
    'AUS_BAUWERK', 'EINGEBAUT_IN', 'HAT_SCHADSTOFF',
    'NUTZT_TOOL',
]

SET_TEXT_CYPHER = """
MATCH (q:Quelle {id: $quelle_id})
SET q.text_content = $text_content,
    q.text_content_loaded_at = date(),
    q.migration_origin = coalesce(q.migration_origin, '') + ' | r7_d_text_content'
"""

DRIFT_CYPHER = """
MERGE (d:DataIssue {id: $issue_id})
ON CREATE SET
  d.kind = 'dossier_uses_retired_type',
  d.severity = 'medium',
  d.ref_label = $retired_type,
  d.ref_id = $dossier_path,
  d.found_at = date(),
  d.found_by = 'r7_d_drift_validator',
  d.status = 'open',
  d.resolution_note = $note,
  d.migration_origin = 'mig_r7_d_drift_validator'
"""


def resolve_file_path(source_file: str) -> Path | None:
    """Try workspace-relative path first, then path substitutions."""
    candidates = [
        WORKSPACE / source_file,
        # inbox → archive substitution for qu_* (post-merge the q_*_md source_file is used)
        WORKSPACE / source_file.replace(
            '_neo4j/intake/inbox/projects/',
            '_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/'
        ),
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def run_r7d(driver):
    print('\n=== R7.d: Populate text_content + drift validator ===')
    # Fetch all case_markdown Quellen with their source_file
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        rows = [r.data() for r in s.run(
            "MATCH (q:Quelle {quelltyp:'case_markdown'}) RETURN q.id AS qid, q.source_file AS src"
        )]

    populated = 0
    missing = []
    drift_findings = []

    for row in rows:
        qid = row['qid']
        src = row.get('src') or ''
        path = resolve_file_path(src) if src else None

        if path:
            try:
                text = path.read_text(encoding='utf-8', errors='replace')
            except Exception as e:
                print(f'  READ ERROR {qid}: {e}')
                missing.append({'qid': qid, 'src': src, 'reason': str(e)})
                continue
            with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
                sess.run(SET_TEXT_CYPHER, quelle_id=qid, text_content=text)
            populated += 1
            # Drift check
            for retired_type in RETIRED_TYPES:
                if retired_type in text:
                    dossier_slug = re.sub(r'[^a-z0-9]', '_', qid.lower())
                    issue_id = f'di_dossier_drift__{retired_type.lower()}__{dossier_slug}'
                    note = (f'Dossier references retired type "{retired_type}".'
                            f' Translate to new name before next ingestion.')
                    with driver.session(database=DATABASE, default_access_mode='WRITE') as sess:
                        sess.run(DRIFT_CYPHER,
                                 issue_id=issue_id,
                                 retired_type=retired_type,
                                 dossier_path=str(path),
                                 note=note)
                    drift_findings.append({'qid': qid, 'retired_type': retired_type})
        else:
            missing.append({'qid': qid, 'src': src, 'reason': 'file_not_found'})

    print(f'  Populated text_content: {populated}')
    print(f'  Missing files: {len(missing)}')
    print(f'  Drift findings: {len(drift_findings)}')
    if missing:
        print('  Missing (first 10):')
        for m in missing[:10]:
            print(f'    {m["qid"]} -> {m["src"]}: {m["reason"]}')
    if drift_findings:
        print('  Drift (first 10):')
        for d in drift_findings[:10]:
            print(f'    {d["qid"]}: {d["retired_type"]}')
    (LOG_DIR / 'r7d_missing_files.json').write_text(
        json.dumps(missing, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    (LOG_DIR / 'r7d_drift_findings.json').write_text(
        json.dumps(drift_findings, indent=2, ensure_ascii=False), encoding='utf-8'
    )
    run_cypher_file(driver, 'mig_r7_d_text_content.cypher', 'r7d')


def run_r7d_gates(driver) -> tuple[dict, bool]:
    gates = {
        'with_text_content': (
            "MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE q.text_content IS NOT NULL RETURN count(q) AS c",
            20, 'min'  # ~21 files confirmed in archive; accept anything above 20
        ),
        'drift_issues_created': (
            "MATCH (d:DataIssue {kind:'dossier_uses_retired_type'}) RETURN count(d) AS c",
            0, 'info'
        ),
    }
    return _run_gates(driver, gates)


# ─── Gate runner ─────────────────────────────────────────────────────────────

def _run_gates(driver, gates: dict) -> tuple[dict, bool]:
    results = {}
    passed = True
    with driver.session(database=DATABASE, default_access_mode='READ') as s:
        for name, (cypher, threshold, mode) in gates.items():
            rows = list(s.run(cypher))
            if len(rows) == 1:
                val = dict(rows[0])
                v = val.get('c', val.get('violations', 0))
                if mode == 'exact':
                    ok = (v == threshold)
                elif mode == 'min':
                    ok = (v >= threshold)
                elif mode == 'zero':
                    ok = (v == 0)
                elif mode == 'info':
                    ok = True
                else:
                    ok = True
                val['_pass'] = ok
                if not ok:
                    passed = False
            else:
                val = [dict(r) for r in rows]
                ok = True
                if isinstance(val, list) and val:
                    val = {'rows': val, '_pass': True}
            results[name] = val
            status = 'PASS' if (val.get('_pass', True) if isinstance(val, dict) else True) else 'FAIL'
            print(f'  {status}  {name}: {val}')
    return results, passed


# ─── Main ─────────────────────────────────────────────────────────────────────

def run_phase(phase: str):
    driver = _get_driver()
    try:
        print(f'\n=== Agent 5 — Phase {phase.upper()} ===')
        pre = probe(driver)
        (LOG_DIR / f'{phase}_probe_pre.json').write_text(json.dumps(pre, indent=2), encoding='utf-8')
        print(f'Pre: {pre}')

        all_gates = {}
        verified = True

        if phase in ('r7ab', 'all'):
            merge_log = run_r7a(driver)
            g_a, ok_a = run_r7a_gates(driver)
            all_gates['r7a'] = g_a
            if not ok_a:
                verified = False
            run_r7b(driver)
            g_b, ok_b = run_r7b_gates(driver)
            all_gates['r7b'] = g_b
            if not ok_b:
                verified = False

        if phase in ('r7d', 'all'):
            run_r7d(driver)
            g_d, ok_d = run_r7d_gates(driver)
            all_gates['r7d'] = g_d
            if not ok_d:
                verified = False

        post = probe(driver)
        (LOG_DIR / f'{phase}_probe_post.json').write_text(json.dumps(post, indent=2), encoding='utf-8')
        (LOG_DIR / f'{phase}_gates.json').write_text(json.dumps(all_gates, indent=2, ensure_ascii=False), encoding='utf-8')
        print(f'Post: {post}')

        flag_name = f'PHASE_{phase.upper()}_DONE.flag'
        flag_data = {
            'phase': phase, 'agent': 'agent_5_loader_hardening',
            'completed_at_utc': datetime.now(timezone.utc).isoformat(),
            'verified': verified, 'pre': pre, 'post': post,
        }
        (RUN_DIR / flag_name).write_text(json.dumps(flag_data, indent=2), encoding='utf-8')

        status = 'PASS' if verified else 'FAIL'
        print(f'\n=== Phase {phase.upper()} {status} ===')
        if not verified:
            raise SystemExit(f'Phase {phase} FAILED — see logs/{phase}_gates.json')
    finally:
        driver.close()


if __name__ == '__main__':
    phase = sys.argv[1].lower() if len(sys.argv) > 1 else 'r7ab'
    run_phase(phase)
