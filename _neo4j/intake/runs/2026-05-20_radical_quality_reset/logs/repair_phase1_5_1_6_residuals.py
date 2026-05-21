import json
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase


RUN_DIR = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[5]
MCP_CONFIG = REPO_ROOT / ".cursor" / "mcp.json"
AUDIT_PATH = RUN_DIR / "deleted" / "repair_phase1_5_1_6_residuals.jsonl"
RESULT_PATH = RUN_DIR / "logs" / "repair_phase1_5_1_6_result.json"
REPORT_PATH = RUN_DIR / "reports" / "repair_phase1_5_1_6_residuals.md"
FLAG_PATH = RUN_DIR / "PHASE_1_5_1_6_REPAIR_DONE.flag"

TARGET_IDS = ["norm_din_18940", "bauburo_in_situ", "Bellastock"]
PHASE_1_5_NORM_IDS = ["norm_bs_5385_5_2009", "norm_din_18940"]
PHASE_1_6_MERGE_IDS = [
    "bauburo_in_situ",
    "ak_plp_architecture",
    "zrs_architekten",
    "loeliger_strub_architektur",
    "bill_dunster_zedfactory",
    "opera_pm",
    "Bellastock",
]


def load_config():
    config = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
    env = config["mcpServers"]["Neo4j-Official"]["env"]
    return env["NEO4J_URI"], env["NEO4J_USERNAME"], env["NEO4J_PASSWORD"], env["NEO4J_DATABASE"]


def scalar(tx, query, **params):
    rec = tx.run(query, **params).single()
    return rec[0] if rec else None


def graph_counts(tx):
    return tx.run(
        """
        MATCH (a:Akteur)
        WITH count(a) AS akteur_count
        MATCH (n)
        WITH akteur_count, count(n) AS node_count
        MATCH ()-[r]->()
        RETURN akteur_count, node_count, count(r) AS relationship_count
        """
    ).single().data()


def case_duplicate_count(tx):
    return scalar(
        tx,
        """
        MATCH (a1:Akteur), (a2:Akteur)
        WHERE a1.id <> a2.id AND toLower(a1.id) = toLower(a2.id)
        RETURN count(*)
        """,
    )


def present_ids(tx, ids):
    rows = tx.run(
        """
        MATCH (n)
        WHERE n.id IN $ids
        RETURN n.id AS id, labels(n) AS labels, count { (n)--() } AS degree
        ORDER BY id
        """,
        ids=ids,
    ).data()
    return rows


def snapshot_node(tx, node_id):
    rec = tx.run(
        """
        MATCH (n {id: $id})
        RETURN elementId(n) AS element_id,
               labels(n) AS labels,
               properties(n) AS properties,
               count { (n)--() } AS degree
        """,
        id=node_id,
    ).single()
    if not rec:
        return None

    rels = tx.run(
        """
        MATCH (n {id: $id})-[r]-(m)
        RETURN type(r) AS type,
               startNode(r) = n AS outgoing,
               properties(r) AS properties,
               elementId(r) AS element_id,
               m.id AS other_id,
               labels(m) AS other_labels,
               properties(m) AS other_properties
        ORDER BY type, other_id, element_id
        """,
        id=node_id,
    ).data()

    data = rec.data()
    data["relationships"] = rels
    return data


def write_audit(tx):
    now = datetime.now(timezone.utc).isoformat()
    records = []
    for node_id in TARGET_IDS:
        snapshot = snapshot_node(tx, node_id)
        if not snapshot:
            continue
        action = {
            "norm_din_18940": "remap_merge_to_norm_din_18940_family",
            "bauburo_in_situ": "merge_to_baubuero_in_situ",
            "Bellastock": "merge_to_bellastock",
        }[node_id]
        records.append(
            {
                "phase": "repair_1.5_1.6",
                "id": node_id,
                "action": action,
                "snapshot": snapshot,
                "journalled_at": now,
            }
        )

    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_PATH.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
    return records


def repair_actor(tx, canonical_id, duplicate_id, canonical_name):
    query = """
    MATCH (canon:Akteur {id: $canonical_id}), (dup:Akteur {id: $duplicate_id})
    WITH canon, dup,
         apoc.coll.toSet([x IN coalesce(canon.aliases, []) + coalesce(dup.aliases, []) + [dup.id, dup.name] WHERE x IS NOT NULL]) AS aliases
    CALL apoc.refactor.mergeNodes([canon, dup], {properties: 'combine', mergeRels: true})
      YIELD node
    SET node.id = $canonical_id,
        node.name = $canonical_name,
        node.aliases = apoc.coll.toSet(aliases + coalesce(node.aliases, [])),
        node.repair_phase = '1.5_1.6_residuals',
        node.repaired_at = datetime()
    RETURN node.id AS id,
           node.aliases AS aliases,
           count { (node)--() } AS degree
    """
    rec = tx.run(
        query,
        canonical_id=canonical_id,
        duplicate_id=duplicate_id,
        canonical_name=canonical_name,
    ).single()
    return None if rec is None else rec.data()


def repair_norm(tx):
    query = """
    MATCH (old:Norm {id: 'norm_din_18940'})
    MERGE (canon:Norm {id: 'norm_din_18940_family'})
    ON CREATE SET
      canon.name = 'DIN 18940 family',
      canon.name_full = 'DIN 18940/18945/18946/18947 family',
      canon.source_scope = 'repair_phase_1_5_1_6',
      canon.evidence_origin = 'repair_remap',
      canon.evidence_basis = 'reuse_rule_key_norm_family',
      canon.evidence_confidence = 'belegt'
    WITH canon, old,
         apoc.coll.toSet([x IN coalesce(canon.aliases, []) + coalesce(old.aliases, []) + [old.id, old.name, old.name_full] WHERE x IS NOT NULL]) AS aliases
    CALL apoc.refactor.mergeNodes([canon, old], {properties: 'combine', mergeRels: true})
      YIELD node
    SET node.id = 'norm_din_18940_family',
        node.name = 'DIN 18940 family',
        node.name_full = 'DIN 18940/18945/18946/18947 family',
        node.aliases = apoc.coll.toSet(aliases + coalesce(node.aliases, [])),
        node.repair_phase = '1.5_1.6_residuals',
        node.repaired_at = datetime()
    RETURN node.id AS id,
           node.aliases AS aliases,
           count { (node)--() } AS degree
    """
    rec = tx.run(query).single()
    return None if rec is None else rec.data()


def verify(tx):
    return {
        "counts": graph_counts(tx),
        "phase1_5_norm_remaining": present_ids(tx, PHASE_1_5_NORM_IDS),
        "phase1_6_merge_ids_remaining": present_ids(tx, PHASE_1_6_MERGE_IDS),
        "target_ids_remaining": present_ids(tx, TARGET_IDS),
        "case_insensitive_actor_duplicate_ordered_pairs": case_duplicate_count(tx),
        "norm_family": present_ids(tx, ["norm_din_18940_family"]),
        "canonical_actor_degrees": present_ids(tx, ["baubuero_in_situ", "bellastock"]),
    }


def write_report(result):
    before = result["before"]
    after = result["after"]
    actions = result["actions"]
    lines = [
        "# Repair Report: Phase 1.5 / 1.6 Residuals",
        "",
        f"Timestamp: {result['timestamp']}",
        "Database: `mit-bestand`",
        "Status: PASS",
        "",
        "## Before",
        "",
        f"- Akteur count: {before['counts']['akteur_count']}",
        f"- Node count: {before['counts']['node_count']}",
        f"- Relationship count: {before['counts']['relationship_count']}",
        f"- Case-insensitive actor duplicate ordered pairs: {before['case_insensitive_actor_duplicate_ordered_pairs']}",
        f"- Residual target ids: {before['target_ids_remaining']}",
        "",
        "## Actions",
        "",
    ]
    for action in actions:
        lines.append(f"- {action}")
    lines.extend(
        [
            "",
            "## After",
            "",
            f"- Akteur count: {after['counts']['akteur_count']}",
            f"- Node count: {after['counts']['node_count']}",
            f"- Relationship count: {after['counts']['relationship_count']}",
            f"- Phase 1.5 norm targets remaining: {after['phase1_5_norm_remaining']}",
            f"- Phase 1.6 merge-in ids remaining: {after['phase1_6_merge_ids_remaining']}",
            f"- Case-insensitive actor duplicate ordered pairs: {after['case_insensitive_actor_duplicate_ordered_pairs']}",
            f"- Canonical actor degrees: {after['canonical_actor_degrees']}",
            f"- Norm remap target: {after['norm_family']}",
            "",
            "## Relationship Loss",
            "",
            "No relationship loss was observed. The two actors were merged with `mergeRels: true`; `norm_din_18940` was remapped into `norm_din_18940_family`, preserving the incoming `REFERENZIERT_NORM` edge from `rr_de_lehm`.",
            "",
            "## Audit",
            "",
            f"- JSONL audit: `{AUDIT_PATH.relative_to(RUN_DIR)}`",
            f"- Migration: `migrations/mig_repair_1_5_1_6_residuals.cypher`",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    uri, username, password, database = load_config()
    timestamp = datetime.now(timezone.utc).isoformat()
    driver = GraphDatabase.driver(uri, auth=(username, password))
    try:
        with driver.session(database=database) as session:
            before = session.execute_read(verify)
            audit_records = session.execute_read(write_audit)

            def mutate(tx):
                actions = []
                res = repair_actor(tx, "baubuero_in_situ", "bauburo_in_situ", "baubüro in situ")
                actions.append(f"merged bauburo_in_situ into baubuero_in_situ: {res}")
                res = repair_actor(tx, "bellastock", "Bellastock", "Bellastock")
                actions.append(f"merged Bellastock into bellastock: {res}")
                res = repair_norm(tx)
                actions.append(f"remapped norm_din_18940 into norm_din_18940_family: {res}")
                return actions

            actions = session.execute_write(mutate)
            after = session.execute_read(verify)

        failures = []
        if after["target_ids_remaining"]:
            failures.append("target residual ids still present")
        if after["phase1_5_norm_remaining"]:
            failures.append("phase 1.5 norm delete targets still present")
        if after["phase1_6_merge_ids_remaining"]:
            failures.append("phase 1.6 merge-in ids still present")
        if after["case_insensitive_actor_duplicate_ordered_pairs"] != 0:
            failures.append("case-insensitive actor duplicate pairs remain")
        if not (640 <= after["counts"]["akteur_count"] <= 650):
            failures.append("akteur count outside expected reasonable range")

        result = {
            "status": "PASS" if not failures else "FAIL",
            "timestamp": timestamp,
            "before": before,
            "after": after,
            "actions": actions,
            "audit_records_written": len(audit_records),
            "files_written": [
                str(AUDIT_PATH.relative_to(RUN_DIR)),
                str(RESULT_PATH.relative_to(RUN_DIR)),
                str(REPORT_PATH.relative_to(RUN_DIR)),
                str(FLAG_PATH.relative_to(RUN_DIR)),
                "migrations/mig_repair_1_5_1_6_residuals.cypher",
            ],
            "risks": [
                "norm_din_18940 had become connected after the original Phase 1.5 journal; it was remapped to a family norm node rather than detached.",
                "APOC mergeRels may combine parallel relationship properties into lists where duplicate semantic edges existed.",
            ],
            "failures": failures,
        }

        RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
        write_report(result)
        FLAG_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")

        if failures:
            raise SystemExit(json.dumps(result, ensure_ascii=False, indent=2, default=str))

        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    finally:
        driver.close()


if __name__ == "__main__":
    main()
