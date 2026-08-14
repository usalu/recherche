"""Dry-run and apply the approved strict actor-network cleanup to Neo4j.

The script is fail-closed. Its default mode is read-only and writes a
reconciliation report. Live mutation will only be enabled after the dry-run
contains no blocking identity conflicts and a logical backup is supplied.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "_scripts"
NETZ = ROOT / "_neo4j" / "netz"
REVIEW = ROOT / "_neo4j" / "review" / "2026-08_akteursnetz_faktencheck"
RUN = Path(__file__).resolve().parent
REPORT = RUN / "dry_run_reconciliation.json"
APPLY_REPORT = RUN / "apply_report.json"
CONFIRM = "APPLY STRICT ACTOR CLEANUP TO mit-bestand"
RUN_ID = "2026-08-14_akteursnetz_strict_cleanup"
SAFE_IDENTIFIER = re.compile(r"^[^\W\d]\w*$", re.UNICODE)

for path in (SCRIPTS, NETZ):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from neo4j_env import resolve_connection  # noqa: E402
from netz.data.neo4j_export import load_export  # noqa: E402
from netz.data.overlays import apply_overlays  # noqa: E402
from netz.sources import DEFAULT  # noqa: E402


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def chunks(values: list[Any], size: int = 500) -> list[list[Any]]:
    return [values[index:index + size] for index in range(0, len(values), size)]


def clean_urls(row: dict) -> list[str]:
    values = [row.get("beleg_url")]
    values.extend(evidence.get("url") for evidence in row.get("evidence") or [])
    return sorted({value.strip() for value in values if isinstance(value, str) and value.strip()})


def snapshot_metadata(final: dict, programmes: set[str], overrides: dict) -> dict[str, dict]:
    raw = load_export(DEFAULT.export_path)
    new_eids, new_project_country, _ = apply_overlays(raw, DEFAULT.overlay_paths)
    metadata = {}
    for key, row in final.items():
        if key not in raw.by:
            raise SystemExit(f"Final key absent from frozen export/overlays: {key}")
        source = raw.by[key]
        labels = set(source.get("labels") or [])
        override = overrides.get(key) or {}
        corrected_type = (override.get("corrected_type") or "").strip()
        if key in programmes or corrected_type == "Programm":
            kind = "Programm"
        elif corrected_type in {"Bauvorhaben", "Bauvorhaben/Objekt", "Projekt", "Objekt"}:
            kind = "Projekt"
        elif corrected_type in {
            "Unternehmen", "Materialhub_Bauteilboerse", "Forschung_Lehre",
            "NGO_Verband_Netzwerk", "Oeffentliche_Institution",
            "Software_Tool_Anbieter", "Organisation",
            "Foerdergeber_Programmtraeger", "Unbekannt", "Person",
        }:
            kind = "Akteur"
        elif "Projekt" in labels:
            kind = "Projekt"
        else:
            kind = "Akteur"
        source_id = source.get("properties", {}).get("id")
        token = key.rsplit(":", 1)[-1]
        metadata[key] = {
            "review_key": key,
            "audit_id": row.get("id"),
            "name": row.get("name"),
            "kind": kind,
            "country": row.get("cc"),
            "source_id": source_id,
            "id_aliases": [token, f"prog_{token}", f"p_{token}", f"org_{token}"],
            "urls": clean_urls(row),
            "roles": list(row.get("rollen") or []),
            "actor_type": raw.types.get(key),
            "is_overlay": key in new_eids,
            "overlay_project_country": new_project_country.get(key),
        }
    return metadata


def query_by_element_ids(session, values: list[str]) -> dict[str, dict]:
    found = {}
    query = (
        "UNWIND $ids AS wanted MATCH (n) WHERE elementId(n) = wanted "
        "RETURN wanted, elementId(n) AS eid, labels(n) AS labels, properties(n) AS properties"
    )
    for batch in chunks(values):
        for record in session.run(query, ids=batch):
            found[record["wanted"]] = {
                "eid": record["eid"],
                "labels": record["labels"],
                "properties": dict(record["properties"]),
            }
    return found


def query_overlay_candidates(session, rows: list[dict]) -> dict[str, list[dict]]:
    found: dict[str, list[dict]] = defaultdict(list)
    query = """
    UNWIND $rows AS wanted
    MATCH (n)
    WITH wanted, n,
         n.strict_review_key = wanted.review_key AS key_match,
         n.id = wanted.source_id AS id_match,
         n.id IN wanted.id_aliases AS id_alias_match,
         n.name = wanted.name AS name_match,
         n.primary_source_url IN wanted.urls OR
           any(url IN coalesce(n.source_urls, []) WHERE url IN wanted.urls) AS url_match
    WHERE key_match OR id_match OR id_alias_match OR name_match OR url_match
    RETURN wanted.review_key AS review_key, elementId(n) AS eid,
           labels(n) AS labels, properties(n) AS properties,
           key_match, id_match, id_alias_match, name_match, url_match
    """
    for batch in chunks(rows, 100):
        for record in session.run(query, rows=batch):
            found[record["review_key"]].append({
                "eid": record["eid"],
                "labels": record["labels"],
                "properties": dict(record["properties"]),
                "matches": {
                    "strict_review_key": bool(record["key_match"]),
                    "source_id": bool(record["id_match"]),
                    "source_id_alias": bool(record["id_alias_match"]),
                    "name": bool(record["name_match"]),
                    "evidence_url": bool(record["url_match"]),
                },
            })
    return found


def graph_counts(session) -> dict:
    totals = session.run(
        "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() "
        "RETURN nodes, count(r) AS relationships"
    ).single()
    labels = {
        record["label"]: record["count"]
        for record in session.run(
            "MATCH (n) UNWIND labels(n) AS label "
            "RETURN label, count(*) AS count ORDER BY label"
        )
    }
    return {
        "nodes": int(totals["nodes"]),
        "relationships": int(totals["relationships"]),
        "labels": labels,
    }


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_backup(backup_dir: Path, before: dict) -> dict:
    manifest_path = backup_dir / "backup_manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"Backup manifest missing: {manifest_path}")
    manifest = load(manifest_path)
    if manifest.get("database") != "mit-bestand":
        raise SystemExit("Backup targets a different database")
    counts = manifest.get("counts") or {}
    if counts.get("nodes") != before["nodes"] or counts.get("relationships") != before["relationships"]:
        raise SystemExit("Backup counts do not match the dry-run baseline")
    for name, expected in (manifest.get("checksums_sha256") or {}).items():
        if name == "checksums.sha256":
            continue
        path = backup_dir / name
        if not path.is_file() or sha256_file(path) != expected:
            raise SystemExit(f"Backup checksum mismatch: {path}")
    return manifest


def merge_lists(left: Any, right: Any) -> list:
    result = []
    for values in (left, right):
        if not isinstance(values, list):
            continue
        for value in values:
            if value not in result:
                result.append(value)
    return result


def merge_relationship(tx, start: str, end: str, rel_type: str, properties: dict) -> None:
    if start == end:
        return
    if not SAFE_IDENTIFIER.match(rel_type):
        raise RuntimeError(f"Unsafe relationship type: {rel_type}")
    properties = dict(properties)
    source_relationship_id = properties.pop("id", None)
    if source_relationship_id:
        properties["merged_source_relationship_id"] = source_relationship_id
    query = (
        f"MATCH (a), (b) WHERE elementId(a) = $start AND elementId(b) = $end "
        f"MERGE (a)-[r:`{rel_type}`]->(b) SET r += $properties"
    )
    tx.run(query, start=start, end=end, properties=properties).consume()


def merge_nodes(tx, source: str, target: str, redirects_live: dict[str, str]) -> dict:
    record = tx.run(
        "MATCH (s), (t) WHERE elementId(s) = $source AND elementId(t) = $target "
        "RETURN labels(s) AS source_labels, properties(s) AS source_properties, "
        "labels(t) AS target_labels, properties(t) AS target_properties",
        source=source,
        target=target,
    ).single()
    if not record:
        raise RuntimeError(f"Merge endpoint disappeared: {source} -> {target}")
    source_properties = dict(record["source_properties"])
    target_properties = dict(record["target_properties"])
    merged_properties = dict(source_properties)
    merged_properties.update(target_properties)
    for key in ("aliases", "source_titles", "source_urls"):
        combined = merge_lists(source_properties.get(key), target_properties.get(key))
        if combined:
            merged_properties[key] = combined
    tx.run(
        "MATCH (t) WHERE elementId(t) = $target SET t += $properties",
        target=target,
        properties=merged_properties,
    ).consume()
    target_labels = set(record["target_labels"])
    for label in record["source_labels"]:
        if label not in target_labels:
            if not SAFE_IDENTIFIER.match(label):
                raise RuntimeError(f"Unsafe label during merge: {label}")
            tx.run(
                f"MATCH (t) WHERE elementId(t) = $target SET t:`{label}`",
                target=target,
            ).consume()

    outgoing = list(tx.run(
        "MATCH (s)-[r]->(o) WHERE elementId(s) = $source "
        "RETURN elementId(o) AS other, type(r) AS type, properties(r) AS properties",
        source=source,
    ))
    incoming = list(tx.run(
        "MATCH (o)-[r]->(s) WHERE elementId(s) = $source "
        "RETURN elementId(o) AS other, type(r) AS type, properties(r) AS properties",
        source=source,
    ))
    for relation in outgoing:
        other = redirects_live.get(relation["other"], relation["other"])
        if other != target:
            merge_relationship(tx, target, other, relation["type"], dict(relation["properties"]))
    for relation in incoming:
        other = redirects_live.get(relation["other"], relation["other"])
        if other != target:
            merge_relationship(tx, other, target, relation["type"], dict(relation["properties"]))
    summary = tx.run(
        "MATCH (s) WHERE elementId(s) = $source DETACH DELETE s",
        source=source,
    ).consume()
    return {
        "source": source,
        "target": target,
        "outgoing_rewired": len(outgoing),
        "incoming_rewired": len(incoming),
        "nodes_deleted": summary.counters.nodes_deleted,
    }


def role_evidence(row: dict, role: str) -> dict:
    evidence_rows = row.get("evidence") or []
    selected = next(
        (item for item in evidence_rows if role in (item.get("supports_roles") or [])),
        evidence_rows[0] if evidence_rows else {},
    )
    return {
        "evidence_url": selected.get("url") or row.get("beleg_url"),
        "evidence_quote": selected.get("quote") or "",
        "evidence_confidence": "belegt",
        "evidence_basis": "strict_research_only_review",
        "review_run": RUN_ID,
        "review_status": "approved_applied",
    }


def node_update_properties(key: str, row: dict, meta: dict, created: bool) -> dict:
    evidence_rows = row.get("evidence") or []
    quote = evidence_rows[0].get("quote") if evidence_rows else ""
    properties = {
        "name": row["name"],
        "strict_review_key": key,
        "strict_review_audit_id": row.get("id"),
        "country_iso2": row.get("cc"),
        "primary_source_url": row.get("beleg_url"),
        "source_urls": clean_urls(row),
        "source_quote": quote or "",
        "reuse_relevance": row.get("relevanz") or "",
        "reuse_objects": list(row.get("reuse_objects") or []),
        "reuse_roles": list(row.get("rollen") or []),
        "actor_degree": row.get("actor_degree"),
        "evidence_basis": "strict_research_only_review",
        "review_run": RUN_ID,
        "review_status": "approved_applied",
    }
    if created:
        properties["id"] = meta.get("source_id") or (
            "strict_akteursnetz_" + hashlib.sha256(key.encode("utf-8")).hexdigest()[:20]
        )
    return {key: value for key, value in properties.items() if value is not None}


def set_node_kind(tx, eid: str, kind: str) -> None:
    if kind not in {"Akteur", "Projekt", "Programm"}:
        raise RuntimeError(f"Unsupported final kind: {kind}")
    tx.run(
        f"MATCH (n) WHERE elementId(n) = $eid "
        f"REMOVE n:Akteur, n:Projekt, n:Programm SET n:`{kind}`",
        eid=eid,
    ).consume()


def normalize_node(tx, eid: str, key: str, row: dict, meta: dict, created: bool) -> None:
    tx.run(
        "MATCH (n) WHERE elementId(n) = $eid SET n += $properties",
        eid=eid,
        properties=node_update_properties(key, row, meta, created),
    ).consume()
    set_node_kind(tx, eid, meta["kind"])
    tx.run(
        "MATCH (n) WHERE elementId(n) = $eid "
        "OPTIONAL MATCH (n)-[r:HAT_AKTEURROLLE|HAT_AKTEURTYP|LIEGT_IN_LAND]->() "
        "DELETE r",
        eid=eid,
    ).consume()
    country_names = {
        "AT": "Österreich", "BE": "Belgien", "CH": "Schweiz",
        "DE": "Deutschland", "DK": "Dänemark", "FI": "Finnland",
        "FR": "Frankreich", "GB": "Vereinigtes Königreich",
        "NL": "Niederlande", "NO": "Norwegen", "SE": "Schweden",
    }
    country = meta["country"]
    tx.run(
        "MATCH (n) WHERE elementId(n) = $eid "
        "MERGE (land:Land {country_iso2: $country}) "
        "ON CREATE SET land.id = $land_id, land.name = $country_name "
        "MERGE (n)-[r:LIEGT_IN_LAND]->(land) "
        "SET r.review_run = $run, r.review_status = 'approved_applied'",
        eid=eid,
        country=country,
        country_name=country_names[country],
        land_id="land_" + country.lower(),
        run=RUN_ID,
    ).consume()
    if meta["kind"] != "Akteur":
        return
    actor_type = meta.get("actor_type") or "Organisation"
    tx.run(
        "MATCH (n) WHERE elementId(n) = $eid "
        "MERGE (typ:Akteurtyp {name: $actor_type}) "
        "ON CREATE SET typ.id = $type_id "
        "MERGE (n)-[r:HAT_AKTEURTYP]->(typ) "
        "SET r.review_run = $run, r.review_status = 'approved_applied'",
        eid=eid,
        actor_type=actor_type,
        type_id="akteurtyp_" + re.sub(r"[^a-z0-9]+", "_", actor_type.lower()).strip("_"),
        run=RUN_ID,
    ).consume()
    for role in row.get("rollen") or []:
        tx.run(
            "MATCH (n) WHERE elementId(n) = $eid "
            "MERGE (role:Akteurrolle {name: $role}) "
            "ON CREATE SET role.id = $role_id "
            "MERGE (n)-[r:HAT_AKTEURROLLE]->(role) SET r += $properties",
            eid=eid,
            role=role,
            role_id="akteurrolle_" + hashlib.sha256(role.encode("utf-8")).hexdigest()[:16],
            properties=role_evidence(row, role),
        ).consume()


def edge_orientation(pair: tuple[str, str], edge_id: str, edge: dict,
                     inventory: dict, metadata: dict) -> tuple[str, str, str]:
    left, right = pair
    left_kind = metadata[left]["kind"]
    right_kind = metadata[right]["kind"]
    if left_kind == "Akteur" and right_kind in {"Projekt", "Programm"}:
        return left, right, "BETEILIGT_AN"
    if right_kind == "Akteur" and left_kind in {"Projekt", "Programm"}:
        return right, left, "BETEILIGT_AN"
    source = inventory[edge_id]
    node_a = source["node_a"]["eid"]
    node_b = source["node_b"]["eid"]
    direction = edge.get("richtung")
    if direction == "A→B":
        return node_a, node_b, "VERBUNDEN_MIT_AKTEUR"
    if direction == "B→A":
        return node_b, node_a, "VERBUNDEN_MIT_AKTEUR"
    return left, right, "VERBUNDEN_MIT_AKTEUR"


def execute_migration(tx, dry: dict) -> dict:
    final = load(REVIEW / "klassifikation_final.json")
    programmes = set(load(REVIEW / "programme_strict_final.json"))
    redirects = load(REVIEW / "merge_redirects_strict.json")
    overrides = load(REVIEW / "report_overrides_strict.json")
    prune = set(load(REVIEW / "prune_strict_final.json"))
    metadata = snapshot_metadata(final, programmes, overrides)
    edge_rows = load(REVIEW / "kanten_klassifikation.json")
    inventory = {
        row["id"]: row
        for row in load(REVIEW / "kanten_review_inventory.json")["records"]
    }
    edge_by_pair = {
        tuple(sorted(row["pair"])): (edge_id, row)
        for edge_id, row in edge_rows.items()
    }
    keep_edges = {tuple(sorted(pair)) for pair in load(REVIEW / "keep_kanten_final.json")}
    final_keys = set(final)
    final_edges = sorted(
        pair for pair in keep_edges if pair[0] in final_keys and pair[1] in final_keys
    )

    key_to_eid = {
        key: key for key in final if not key.startswith("NEW:")
    }
    key_to_eid.update({
        key: value["eid"]
        for key, value in dry["reconciled_overlay_nodes"].items()
    })

    live_redirects = {
        source: target
        for source, target in redirects.items()
        if not source.startswith("NEW:")
    }
    merge_reports = []
    for source, target in live_redirects.items():
        exists = tx.run(
            "MATCH (s) WHERE elementId(s) = $source RETURN count(s) AS count",
            source=source,
        ).single()["count"]
        if exists:
            merge_reports.append(merge_nodes(tx, source, target, live_redirects))
        else:
            merge_reports.append({"source": source, "target": target, "already_absent": True})

    delete_eids = sorted(
        {key for key in prune if not key.startswith("NEW:")} - set(live_redirects)
    )
    delete_eids.extend(
        value["eid"] for value in dry.get("reconciled_pruned_overlay_nodes", {}).values()
    )
    delete_summary = tx.run(
        "UNWIND $ids AS eid MATCH (n) WHERE elementId(n) = eid DETACH DELETE n",
        ids=delete_eids,
    ).consume()

    created = []
    for key in dry["overlay_nodes_to_create"]:
        meta = metadata[key]
        label = meta["kind"]
        if label not in {"Akteur", "Projekt", "Programm"}:
            raise RuntimeError(f"Unsafe create label: {label}")
        record = tx.run(
            f"CREATE (n:`{label}`) SET n = $properties RETURN elementId(n) AS eid",
            properties=node_update_properties(key, final[key], meta, True),
        ).single()
        key_to_eid[key] = record["eid"]
        created.append({"review_key": key, "eid": record["eid"], "kind": label})

    if set(key_to_eid) != final_keys:
        missing = sorted(final_keys - set(key_to_eid))
        raise RuntimeError(f"Final identity mapping incomplete: {missing[:10]}")

    for key, row in final.items():
        normalize_node(
            tx, key_to_eid[key], key, row, metadata[key], key in dry["overlay_nodes_to_create"]
        )

    final_eids = list(key_to_eid.values())
    old_edge_summary = tx.run(
        "MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR|BETRIEBEN_VON|BETEILIGT_AN]-(b) "
        "WHERE elementId(a) IN $ids AND elementId(b) IN $ids WITH DISTINCT r DELETE r",
        ids=final_eids,
    ).consume()

    edge_reports = []
    for pair in final_edges:
        edge_id, edge = edge_by_pair[pair]
        start_key, end_key, rel_type = edge_orientation(
            pair, edge_id, edge, inventory, metadata
        )
        properties = {
            "edge_review_id": edge_id,
            "beziehungsart": edge.get("beziehungsart"),
            "beschreibung": edge.get("beschreibung"),
            "review_direction": edge.get("richtung"),
            "evidence_url": edge.get("evidence_url"),
            "evidence_quote": edge.get("evidence_quote"),
            "evidence_confidence": edge.get("evidence_confidence") or "belegt",
            "evidence_basis": edge.get("evidence_basis") or "strict_edge_review",
            "review_run": RUN_ID,
            "review_status": "approved_applied",
        }
        merge_relationship(
            tx, key_to_eid[start_key], key_to_eid[end_key], rel_type,
            {key: value for key, value in properties.items() if value is not None},
        )
        edge_reports.append({
            "edge_review_id": edge_id,
            "pair": list(pair),
            "type": rel_type,
            "start_review_key": start_key,
            "end_review_key": end_key,
        })

    tx.run(
        "MATCH (role:Akteurrolle) WHERE NOT ()-[:HAT_AKTEURROLLE]->(role) DELETE role"
    ).consume()
    tx.run(
        "MATCH (typ:Akteurtyp) WHERE NOT ()-[:HAT_AKTEURTYP]->(typ) DELETE typ"
    ).consume()
    return {
        "merge_reports": merge_reports,
        "nodes_created": len(created),
        "created_nodes": created,
        "prune_nodes_deleted": delete_summary.counters.nodes_deleted,
        "prune_relationships_deleted": delete_summary.counters.relationships_deleted,
        "old_scoped_edges_deleted": old_edge_summary.counters.relationships_deleted,
        "final_edges_written": len(edge_reports),
        "edge_reports": edge_reports,
        "key_to_eid": key_to_eid,
    }


def verify_post_apply(session, key_to_eid: dict) -> dict:
    final = load(REVIEW / "klassifikation_final.json")
    programmes = set(load(REVIEW / "programme_strict_final.json"))
    actor_project = set(load(REVIEW / "klassifikation_actor_project_final.json"))
    rows = list(session.run(
        "MATCH (n) WHERE n.strict_review_key IN $keys "
        "RETURN n.strict_review_key AS key, elementId(n) AS eid, labels(n) AS labels, "
        "n.name AS name, n.country_iso2 AS country, "
        "count { (n)-[:LIEGT_IN_LAND]->() } AS countries, "
        "count { (n)-[:HAT_AKTEURROLLE]->() } AS roles",
        keys=list(final),
    ))
    by_key = {record["key"]: record for record in rows}
    errors = []
    for key, expected in final.items():
        record = by_key.get(key)
        if not record:
            errors.append(f"missing strict node {key}")
            continue
        expected_label = "Programm" if key in programmes else (
            "Projekt" if key not in actor_project or expected.get("rolle", "").startswith("Referenzprojekt")
            else "Akteur"
        )
        if expected_label not in record["labels"]:
            errors.append(f"wrong label {key}: {record['labels']} expected {expected_label}")
        if record["name"] != expected["name"]:
            errors.append(f"wrong name {key}")
        if record["country"] != expected["cc"] or record["countries"] != 1:
            errors.append(f"wrong country {key}")
        if expected_label != "Akteur" and record["roles"] != 0:
            errors.append(f"non-actor has actor roles {key}")
    scoped_edges = session.run(
        "MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR|BETEILIGT_AN|BETRIEBEN_VON]->(b) "
        "WHERE a.strict_review_key IN $keys AND b.strict_review_key IN $keys "
        "RETURN count(r) AS count, count(DISTINCT r.edge_review_id) AS reviewed",
        keys=list(final),
    ).single()
    if scoped_edges["count"] != 278 or scoped_edges["reviewed"] != 278:
        errors.append(
            f"scoped edges {scoped_edges['count']}/{scoped_edges['reviewed']} expected 278/278"
        )
    return {
        "graph": graph_counts(session),
        "strict_nodes": len(by_key),
        "strict_actor_project_nodes": len(actor_project),
        "strict_programmes": len(programmes),
        "strict_scoped_edges": int(scoped_edges["count"]),
        "errors": errors,
    }


def apply_live(dry: dict, backup_dir: Path, confirm: str) -> dict:
    if confirm != CONFIRM:
        raise SystemExit(f"Confirmation must exactly equal: {CONFIRM!r}")
    if not dry.get("ready_for_backup_and_apply"):
        raise SystemExit("Dry-run is not ready for apply")
    manifest = validate_backup(backup_dir, dry["before"])
    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            current = graph_counts(session)
            if current["nodes"] != dry["before"]["nodes"] or current["relationships"] != dry["before"]["relationships"]:
                raise SystemExit("Live graph changed after dry-run/backup; refusing apply")
            applied = session.execute_write(execute_migration, dry)
            verified = verify_post_apply(session, applied["key_to_eid"])
    finally:
        driver.close()
    payload = {
        "schema_version": 1,
        "applied_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "confirmation": confirm,
        "backup": {
            "directory": str(backup_dir),
            "manifest": str(backup_dir / "backup_manifest.json"),
            "restore_confirmation": manifest.get("restore_confirmation"),
        },
        "before": dry["before"],
        "changes": applied,
        "after": verified,
        "success": not verified["errors"],
    }
    write(APPLY_REPORT, payload)
    if verified["errors"]:
        raise SystemExit(f"Post-apply verification failed: {verified['errors'][:10]}")
    return payload


def build_dry_run() -> dict:
    final = load(REVIEW / "klassifikation_final.json")
    original_classification = load(REVIEW / "klassifikation.json")
    actor_project = load(REVIEW / "klassifikation_actor_project_final.json")
    programme_rows = load(REVIEW / "programme_strict_final.json")
    programmes = set(programme_rows)
    prune = set(load(REVIEW / "prune_strict_final.json"))
    redirects = load(REVIEW / "merge_redirects_strict.json")
    overrides = load(REVIEW / "report_overrides_strict.json")
    keep_edges = {tuple(sorted(pair)) for pair in load(REVIEW / "keep_kanten_final.json")}
    prune_edges = {tuple(sorted(pair)) for pair in load(REVIEW / "prune_kanten_final.json")}
    unclear_edges = {tuple(sorted(pair)) for pair in load(REVIEW / "unklar_edges_final.json")}
    edge_rows = load(REVIEW / "kanten_klassifikation.json")

    if len(final) != 628 or len(actor_project) != 619 or len(programmes) != 9:
        raise SystemExit("Frozen final counts no longer match 628 / 619 / 9")
    if len(prune) != 231:
        raise SystemExit(f"Expected 231 removed-or-merged EIDs, got {len(prune)}")

    metadata = snapshot_metadata(final, programmes, overrides)
    live_final_keys = sorted(key for key in final if not key.startswith("NEW:"))
    overlay_final_keys = sorted(key for key in final if key.startswith("NEW:"))
    overlay_prune_keys = sorted(
        key for key in prune
        if key.startswith("NEW:") and key not in redirects
    )
    prune_metadata = snapshot_metadata(
        {key: original_classification[key] for key in overlay_prune_keys},
        set(),
        {},
    )
    live_prune_keys = sorted(key for key in prune if not key.startswith("NEW:"))
    live_redirect_keys = sorted(
        {key for pair in redirects.items() for key in pair if not key.startswith("NEW:")}
    )

    uri, user, password, database = resolve_connection()
    if database != "mit-bestand":
        raise SystemExit(f"Refusing unexpected database: {database}")
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings")

    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            before = graph_counts(session)
            direct = query_by_element_ids(
                session,
                sorted(set(live_final_keys) | set(live_prune_keys) | set(live_redirect_keys)),
            )
            candidate_rows = [metadata[key] for key in overlay_final_keys]
            overlay_hits = query_overlay_candidates(session, candidate_rows)
            prune_overlay_hits = query_overlay_candidates(
                session, [prune_metadata[key] for key in overlay_prune_keys]
            )
    finally:
        driver.close()

    missing_live_final = sorted(set(live_final_keys) - set(direct))
    missing_live_prune = sorted(set(live_prune_keys) - set(direct))
    missing_live_redirect = sorted(set(live_redirect_keys) - set(direct))
    missing_live_redirect_targets = sorted(
        {target for target in redirects.values() if not target.startswith("NEW:")} - set(direct)
    )

    reconciled = {}
    create = []
    ambiguous = {}
    name_only = {}
    for key in overlay_final_keys:
        hits = overlay_hits.get(key, [])
        strong = [
            hit for hit in hits
            if hit["matches"]["strict_review_key"]
            or hit["matches"]["source_id"]
            or hit["matches"]["source_id_alias"]
            or (hit["matches"]["evidence_url"] and hit["matches"]["name"])
        ]
        if len(strong) == 1:
            reconciled[key] = strong[0]
        elif len(strong) > 1:
            ambiguous[key] = strong
        else:
            names = [hit for hit in hits if hit["matches"]["name"]]
            if names:
                name_only[key] = names
            else:
                create.append(key)

    prune_overlay_reconciled = {}
    prune_overlay_ambiguous = {}
    prune_overlay_name_only = {}
    for key in overlay_prune_keys:
        hits = prune_overlay_hits.get(key, [])
        strong = [
            hit for hit in hits
            if hit["matches"]["strict_review_key"]
            or hit["matches"]["source_id"]
            or hit["matches"]["source_id_alias"]
            or (hit["matches"]["evidence_url"] and hit["matches"]["name"])
        ]
        if len(strong) == 1:
            prune_overlay_reconciled[key] = strong[0]
        elif len(strong) > 1:
            prune_overlay_ambiguous[key] = strong
        else:
            names = [hit for hit in hits if hit["matches"]["name"]]
            if names:
                prune_overlay_name_only[key] = names

    final_keys = set(final)
    final_keep_edges = sorted(
        pair for pair in keep_edges if pair[0] in final_keys and pair[1] in final_keys
    )
    final_actor_edges = sorted(
        pair for pair in final_keep_edges
        if pair[0] in actor_project and pair[1] in actor_project
    )
    final_program_edges = sorted(set(final_keep_edges) - set(final_actor_edges))
    edge_by_pair = {}
    duplicate_edge_decisions = []
    for edge_id, row in edge_rows.items():
        pair = tuple(sorted(row["pair"]))
        if pair in edge_by_pair:
            duplicate_edge_decisions.append([edge_by_pair[pair][0], edge_id])
        edge_by_pair[pair] = (edge_id, row)
    missing_edge_decisions = [pair for pair in final_keep_edges if pair not in edge_by_pair]

    blocking = {
        "missing_live_final": missing_live_final,
        "missing_live_redirect_targets": missing_live_redirect_targets,
        "ambiguous_overlay_identity": ambiguous,
        "name_only_overlay_identity": name_only,
        "ambiguous_pruned_overlay_identity": prune_overlay_ambiguous,
        "name_only_pruned_overlay_identity": prune_overlay_name_only,
        "duplicate_edge_decisions": duplicate_edge_decisions,
        "missing_final_edge_decisions": missing_edge_decisions,
    }
    blocking_count = sum(len(value) for value in blocking.values())
    return {
        "schema_version": 1,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "mode": "read_only_dry_run",
        "database": database,
        "connection": {"uri": uri, "user": user},
        "before": before,
        "review_scope": {
            "decisions": 859,
            "final_nodes_including_programmes": len(final),
            "final_actor_project_nodes": len(actor_project),
            "programmes": len(programmes),
            "removed_or_merged": len(prune),
            "reviewed_keep_edges": len(keep_edges),
            "reviewed_prune_edges": len(prune_edges),
            "pre_campaign_unclear_edges": len(unclear_edges),
            "final_edges_including_programmes": len(final_keep_edges),
            "final_actor_project_edges": len(final_actor_edges),
            "final_programme_edges": len(final_program_edges),
        },
        "identity_reconciliation": {
            "live_final_expected": len(live_final_keys),
            "live_final_found": len(live_final_keys) - len(missing_live_final),
            "overlay_final_expected": len(overlay_final_keys),
            "overlay_reconciled_strong": len(reconciled),
            "overlay_to_create": len(create),
            "overlay_name_only_blocked": len(name_only),
            "overlay_ambiguous_blocked": len(ambiguous),
            "pruned_overlay_expected": len(overlay_prune_keys),
            "pruned_overlay_reconciled_strong": len(prune_overlay_reconciled),
            "pruned_overlay_ambiguous_blocked": len(prune_overlay_ambiguous),
            "pruned_overlay_name_only_blocked": len(prune_overlay_name_only),
            "live_prune_expected": len(live_prune_keys),
            "live_prune_found": len(live_prune_keys) - len(missing_live_prune),
            "missing_live_prune_already_absent": missing_live_prune,
        },
        "reconciled_overlay_nodes": reconciled,
        "reconciled_pruned_overlay_nodes": prune_overlay_reconciled,
        "overlay_nodes_to_create": create,
        "blocking": blocking,
        "blocking_count": blocking_count,
        "ready_for_backup_and_apply": blocking_count == 0,
        "kind_counts": dict(Counter(row["kind"] for row in metadata.values())),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--backup-dir", type=Path)
    parser.add_argument("--confirm", default="")
    args = parser.parse_args()
    payload = build_dry_run()
    write(args.report, payload)
    print(json.dumps({
        "report": str(args.report),
        "database": payload["database"],
        "before": payload["before"],
        "review_scope": payload["review_scope"],
        "identity_reconciliation": payload["identity_reconciliation"],
        "blocking_count": payload["blocking_count"],
        "ready_for_backup_and_apply": payload["ready_for_backup_and_apply"],
    }, ensure_ascii=False, indent=2))
    if payload["blocking_count"]:
        return 1
    if args.confirm or args.backup_dir:
        if not args.backup_dir:
            raise SystemExit("--backup-dir is required for live apply")
        applied = apply_live(payload, args.backup_dir, args.confirm)
        print(json.dumps({
            "apply_report": str(APPLY_REPORT),
            "success": applied["success"],
            "before": applied["before"],
            "after": applied["after"],
            "changes": {
                "nodes_created": applied["changes"]["nodes_created"],
                "prune_nodes_deleted": applied["changes"]["prune_nodes_deleted"],
                "final_edges_written": applied["changes"]["final_edges_written"],
            },
        }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
