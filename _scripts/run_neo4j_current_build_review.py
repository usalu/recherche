"""Run the Round 001 technical review for the current Neo4j JSONL build.

DEPRECATED 2026-05-15: superseded by `run_neo4j_round002_baseline.py`.
This script still reads from the archived `_neo4j/batch/` tree and reflects the
pre-cleanup 20-batch corpus. It is preserved as the reproducible record of the
round-001 audit. Do not run it against the current state.

This script is intentionally read-only for published batch exports. It writes
review outputs under `_neo4j/review/round_001/`:

  global_audit_report.md
  exports_vs_live_db_diff.md
  patch_manifest.json
  patches/global_technical.patch.jsonl
  placeholders/... for missing manifests/delta files
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


NODE_ID_RE = re.compile(r"^[a-z][a-z0-9]*_[a-z0-9_]+$")
REL_ID_RE = re.compile(r"^r_[a-z0-9_]+__[A-Z0-9_]+__[a-z0-9_]+.*$")
BATCH_RE = re.compile(r"batch_(\d{3})$")

# Labels that are controlled-vocabulary seed nodes; expected to have few
# relationships and are excluded from the low-degree check (Check 13).
VOCAB_LABELS: frozenset[str] = frozenset(
    {
        "Material", "Land", "Stadt", "Akteurrolle", "Akteurtyp",
        "Bauobjektklasse", "Bauobjektrolle", "BauaufgabeIntervention",
        "Bauweise", "Bausystem", "Tragwerksprinzip", "Nutzung", "Status",
        "Bauteiltyp", "Bauteilebene", "Bauteilzustand", "Materialgruppe",
        "WiederverwendungsArt", "Ressourcenquelle", "Beschaffungsweg",
        "Methode", "Prozessphase", "Rueckbauverfahren", "Aufbereitungsverfahren",
        "Logistik", "Funktionswechsel", "Verbindungstechnik", "HuerdeKategorie",
        "Leistungsanforderung", "PruefungNachweis", "Norm", "RechtlicheBedingung",
        "Schadstoff", "Wirtschaft", "ZertifizierungBewertungssystem",
        "Software", "Tool", "Programm", "Datenqualitaet",
    }
)


@dataclass
class BatchInfo:
    batch_id: str
    path: Path
    project_files: list[Path]
    manifest_exists: bool
    delta_exists: bool
    delta_nonempty_lines: int


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(repo_root()))


def load_contract_enums() -> tuple[set[str], set[str]]:
    schema_path = (
        repo_root() / "_neo4j" / "batch" / "contract" / "schemas" / "kg_jsonl_record_schema.json"
    )
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    node_schema, rel_schema = data["oneOf"]
    labels = set(node_schema["properties"]["labels"]["items"]["enum"])
    rel_types = set(rel_schema["properties"]["type"]["enum"])
    return labels, rel_types


def choose_current_batches() -> list[BatchInfo]:
    base = repo_root() / "_neo4j" / "batch"
    candidates: dict[str, tuple[int, Path]] = {}
    for path in base.glob("neo4j_batch_*_exports/**/batches/batch_*"):
        if not path.is_dir() or not list(path.glob("p_*.kg.jsonl")):
            continue
        match = BATCH_RE.search(path.name)
        if not match:
            continue
        batch_id = match.group(1)
        priority = 0 if "neo4j_complete_repo_package" in str(path) else 1
        if batch_id not in candidates or priority > candidates[batch_id][0]:
            candidates[batch_id] = (priority, path)

    batches: list[BatchInfo] = []
    for batch_id in sorted(candidates):
        path = candidates[batch_id][1]
        delta = path / "controlled_terms.delta.jsonl"
        delta_lines = 0
        if delta.exists():
            delta_lines = sum(1 for line in delta.read_text(encoding="utf-8").splitlines() if line.strip())
        batches.append(
            BatchInfo(
                batch_id=batch_id,
                path=path,
                project_files=sorted(path.glob("p_*.kg.jsonl")),
                manifest_exists=(path / "manifest.json").exists(),
                delta_exists=delta.exists(),
                delta_nonempty_lines=delta_lines,
            )
        )
    return batches


def read_jsonl(path: Path, parse_errors: list[dict]) -> list[tuple[int, dict]]:
    out: list[tuple[int, dict]] = []
    with path.open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                out.append((lineno, json.loads(line)))
            except json.JSONDecodeError as exc:
                parse_errors.append(
                    {"file": rel(path), "line": lineno, "error": str(exc)}
                )
    return out


def validate_record(record: dict, path: Path, lineno: int, labels: set[str], rel_types: set[str]) -> list[dict]:
    errors: list[dict] = []
    record_type = record.get("record_type")
    if record_type == "node":
        required = {"record_type", "id", "labels", "properties"}
        missing = sorted(required - set(record))
        if missing:
            errors.append({"file": rel(path), "line": lineno, "error": f"missing {missing}"})
        if not NODE_ID_RE.match(str(record.get("id", ""))):
            errors.append({"file": rel(path), "line": lineno, "error": "invalid node id"})
        node_labels = record.get("labels")
        if not isinstance(node_labels, list) or len(node_labels) != 1:
            errors.append({"file": rel(path), "line": lineno, "error": "node must have exactly one label"})
        elif node_labels[0] not in labels:
            errors.append({"file": rel(path), "line": lineno, "error": f"unexpected label {node_labels[0]}"})
        if not isinstance(record.get("properties"), dict):
            errors.append({"file": rel(path), "line": lineno, "error": "properties must be object"})
    elif record_type == "rel":
        required = {"record_type", "id", "from", "type", "to", "properties"}
        missing = sorted(required - set(record))
        if missing:
            errors.append({"file": rel(path), "line": lineno, "error": f"missing {missing}"})
        if not REL_ID_RE.match(str(record.get("id", ""))):
            errors.append({"file": rel(path), "line": lineno, "error": "invalid relationship id"})
        if not NODE_ID_RE.match(str(record.get("from", ""))) or not NODE_ID_RE.match(str(record.get("to", ""))):
            errors.append({"file": rel(path), "line": lineno, "error": "invalid relationship endpoint id"})
        if record.get("type") not in rel_types:
            errors.append({"file": rel(path), "line": lineno, "error": f"unexpected relationship type {record.get('type')}"})
        if not isinstance(record.get("properties"), dict):
            errors.append({"file": rel(path), "line": lineno, "error": "properties must be object"})
    else:
        errors.append({"file": rel(path), "line": lineno, "error": f"unexpected record_type {record_type!r}"})
    return errors


def validate_manifest(path: Path) -> list[dict]:
    errors: list[dict] = []
    if not path.exists():
        return [{"file": rel(path), "error": "manifest missing"}]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [{"file": rel(path), "error": f"manifest JSON error: {exc}"}]
    required = {
        "batch_id",
        "schema_version",
        "source_files",
        "project_files",
        "controlled_vocabulary_seed",
        "controlled_terms_delta",
        "validation_report",
    }
    missing = sorted(required - set(data))
    if missing:
        errors.append({"file": rel(path), "error": f"manifest missing {missing}"})
    if data.get("schema_version") != "neo4j_reuse_graph_v1_1":
        errors.append({"file": rel(path), "error": "manifest schema_version mismatch"})
    return errors


def property_signature(record: dict) -> tuple:
    props = dict(record.get("properties") or {})
    # Some later batches redundantly include id inside properties. That is still
    # a conflict for MERGE+SET semantics, but it is low-risk and classified.
    return (
        tuple(record.get("labels") or []),
        json.dumps(props, ensure_ascii=False, sort_keys=True),
    )


def canonical_name(variants: list[dict]) -> tuple[str | None, list[str]]:
    names: list[str] = []
    for variant in variants:
        name = (variant.get("properties") or {}).get("name")
        if isinstance(name, str) and name not in names:
            names.append(name)
    if not names:
        return None, []
    canonical = sorted(names, key=lambda n: (len(n), n.casefold()))[0]
    aliases = [name for name in names if name != canonical]
    return canonical, aliases


def add_missing_endpoint_patches(missing: list[dict]) -> list[dict]:
    missing_ids = sorted({item["missing_id"] for item in missing})
    patches: list[dict] = []
    if "bweg_lager" in missing_ids:
        patches.append(
            {
                "op": "add_node",
                "id": "bweg_lager",
                "labels": ["Beschaffungsweg"],
                "properties": {"name": "Lager", "review_status": "proposed"},
                "reason": "Missing endpoint referenced by HAT_BESCHAFFUNGSWEG in batch_016.",
                "severity": "BLOCKER",
            }
        )
    if "ar_materialhub_bauteilboerse" in missing_ids:
        patches.append(
            {
                "op": "add_node",
                "id": "ar_materialhub_bauteilboerse",
                "labels": ["Akteurrolle"],
                "properties": {
                    "name": "Materialhub / Bauteilbörse",
                    "review_status": "proposed",
                },
                "reason": "Missing endpoint referenced by HAT_AKTEURROLLE in batch_019.",
                "severity": "BLOCKER",
            }
        )
    return patches


def query_live_db() -> tuple[dict, list[str]]:
    notices: list[str] = []
    result: dict[str, Any] = {"available": False}
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return {"available": False, "error": "neo4j driver not installed"}, notices

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        return {"available": False, "error": "missing Neo4j connection settings"}, notices

    queries = {
        "counts": (
            "MATCH (n) WITH count(n) AS nodes "
            "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
        ),
        "forbidden_nodes": "MATCH (n) WHERE n:Fallbeispiel OR n:Kennwert OR n:Datenqualitaet RETURN count(n) AS c",
        "bad_belegt_in": "MATCH ()-[r:BELEGT_IN]->() WHERE r.datenqualitaet <> 'Belegt' OR r.datenqualitaet IS NULL RETURN count(r) AS c",
        "projects": "MATCH (p:Projekt) RETURN count(p) AS c",
        "programmes": "MATCH (p:Programm) RETURN count(p) AS c",
        "projects_no_source": "MATCH (p:Projekt) WHERE NOT (p)-[:BELEGT_IN]->(:Quelle) RETURN count(p) AS c",
        "programmes_no_source": "MATCH (p:Programm) WHERE NOT (p)-[:BELEGT_IN]->(:Quelle) RETURN count(p) AS c",
        "projects_no_component_or_work": "MATCH (p:Projekt) WHERE NOT ((p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) OR (p)-[:NUTZT_BAUWERK]->(:Bauwerk)) RETURN count(p) AS c",
        "bg": "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS c",
        "bg_no_source": "MATCH (bg:Bauteilgruppe) WHERE NOT (bg)-[:BELEGT_IN]->(:Quelle) RETURN count(bg) AS c",
        "bg_no_type": "MATCH (bg:Bauteilgruppe) WHERE NOT (bg)-[:HAT_BAUTEILTYP]->(:Bauteiltyp) RETURN count(bg) AS c",
        "bg_no_material_or_level": "MATCH (bg:Bauteilgruppe) WHERE NOT ((bg)-[:NUTZT_MATERIAL]->(:Material) OR (bg)-[:HAT_BAUTEILEBENE]->(:Bauteilebene)) RETURN count(bg) AS c",
        "direct_bg_no_donor": "MATCH (bg:Bauteilgruppe) WHERE bg.counts_as_direct_reuse = true AND NOT (bg)-[:AUS_BAUWERK]->(:Bauwerk) RETURN count(bg) AS c",
        "direct_bg_no_receiver": "MATCH (bg:Bauteilgruppe) WHERE bg.counts_as_direct_reuse = true AND NOT (bg)-[:EINGEBAUT_IN]->(:Bauwerk) RETURN count(bg) AS c",
    }

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            result = {
                "available": True,
                "database": database,
                "uri": uri,
                "checks": {},
                "label_counts": [],
                "relationship_type_counts": [],
                "projects_without_component_or_work": [],
                "direct_reuse_without_donor": [],
                "direct_reuse_without_receiver": [],
                "duplicate_names": [],
                "low_degree_non_vocab_nodes": [],
            }
            for name, cypher in queries.items():
                rec = session.run(cypher).single()
                if name == "counts":
                    result["counts"] = {
                        "nodes": int(rec["nodes"]),
                        "relationships": int(rec["relationships"]),
                    }
                else:
                    result["checks"][name] = int(rec["c"])

            result["label_counts"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) UNWIND labels(n) AS label "
                    "RETURN label, count(*) AS count ORDER BY count DESC, label LIMIT 20"
                )
            ]
            result["relationship_type_counts"] = [
                dict(row)
                for row in session.run(
                    "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count "
                    "ORDER BY count DESC, type LIMIT 20"
                )
            ]
            result["projects_without_component_or_work"] = [
                dict(row)
                for row in session.run(
                    "MATCH (p:Projekt) "
                    "WHERE NOT ((p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) "
                    "OR (p)-[:NUTZT_BAUWERK]->(:Bauwerk)) "
                    "RETURN p.id AS id, p.name AS name ORDER BY id LIMIT 25"
                )
            ]
            result["direct_reuse_without_donor"] = [
                dict(row)
                for row in session.run(
                    "MATCH (bg:Bauteilgruppe) "
                    "WHERE bg.counts_as_direct_reuse = true "
                    "AND NOT (bg)-[:AUS_BAUWERK]->(:Bauwerk) "
                    "RETURN bg.id AS id, bg.name AS name ORDER BY id LIMIT 25"
                )
            ]
            result["direct_reuse_without_receiver"] = [
                dict(row)
                for row in session.run(
                    "MATCH (bg:Bauteilgruppe) "
                    "WHERE bg.counts_as_direct_reuse = true "
                    "AND NOT (bg)-[:EINGEBAUT_IN]->(:Bauwerk) "
                    "RETURN bg.id AS id, bg.name AS name ORDER BY id LIMIT 25"
                )
            ]
            result["duplicate_names"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) WHERE n.name IS NOT NULL "
                    "WITH labels(n)[0] AS label, toLower(toString(n.name)) AS name_key, collect(n.id) AS ids, count(*) AS c "
                    "WHERE c > 1 RETURN label, name_key, ids, c ORDER BY c DESC, label LIMIT 25"
                )
            ]
            # Check 13: low-degree non-vocabulary nodes.
            _vocab = list(VOCAB_LABELS)
            _ld_count = session.run(
                "MATCH (n) "
                "WHERE NOT labels(n)[0] IN $vocab "
                "WITH n, COUNT { (n)--() } AS degree "
                "WHERE degree < 2 "
                "RETURN count(n) AS c",
                vocab=_vocab,
            ).single()
            result["checks"]["low_degree_non_vocab_nodes"] = int(_ld_count["c"])
            result["low_degree_non_vocab_nodes"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) "
                    "WHERE NOT labels(n)[0] IN $vocab "
                    "WITH n, COUNT { (n)--() } AS degree "
                    "WHERE degree < 2 "
                    "RETURN labels(n)[0] AS label, n.id AS id, n.name AS name, degree "
                    "ORDER BY degree ASC, label, id LIMIT 50",
                    vocab=_vocab,
                )
            ]
    except Exception as exc:  # noqa: BLE001
        result = {"available": False, "error": str(exc)}
    finally:
        driver.close()
    return result, notices


def write_placeholders(round_dir: Path, batches: list[BatchInfo]) -> list[str]:
    written: list[str] = []
    root = round_dir / "placeholders"
    for batch in batches:
        target = root / f"batch_{batch.batch_id}"
        target.mkdir(parents=True, exist_ok=True)
        if not batch.manifest_exists:
            manifest = {
                "batch_id": f"batch_{batch.batch_id}",
                "schema_version": "neo4j_reuse_graph_v1_1",
                "source_files": [],
                "project_files": [p.name for p in batch.project_files],
                "controlled_vocabulary_seed": "../../contract/controlled_vocabulary.seed.kg.jsonl",
                "controlled_terms_delta": "controlled_terms.delta.jsonl",
                "validation_report": "validation_report.md",
                "notes": (
                    "Review placeholder generated by run_neo4j_current_build_review.py; "
                    "do not treat as published batch manifest until accepted."
                ),
            }
            path = target / "manifest.json"
            path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            written.append(rel(path))
        if not batch.delta_exists:
            path = target / "controlled_terms.delta.jsonl"
            path.write_text("", encoding="utf-8")
            written.append(rel(path))
    return written


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def read_patch_overlay(paths: list[Path]) -> tuple[list[dict], list[dict]]:
    records: list[dict] = []
    errors: list[dict] = []
    for path in paths:
        with path.open(encoding="utf-8") as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    errors.append({"file": rel(path), "line": lineno, "error": str(exc)})
                    continue
                records.append({**record, "_overlay_file": rel(path), "_overlay_line": lineno})
    return records, errors


def run(round_dir: Path, accepted_patch_paths: list[Path] | None = None) -> dict:
    round_dir = round_dir.resolve()
    labels, rel_types = load_contract_enums()
    accepted_patch_paths = [path.resolve() for path in (accepted_patch_paths or [])]
    batches = choose_current_batches()
    seed = repo_root() / "_neo4j" / "batch" / "contract" / "controlled_vocabulary.seed.kg.jsonl"
    files: list[Path] = [seed]
    for batch in batches:
        delta = batch.path / "controlled_terms.delta.jsonl"
        if delta.exists():
            files.append(delta)
        files.extend(batch.project_files)

    parse_errors: list[dict] = []
    schema_errors: list[dict] = []
    manifest_errors: list[dict] = []
    forbidden_nodes: list[dict] = []
    bad_belegt_in: list[dict] = []
    node_defs: dict[str, tuple] = {}
    rel_defs: dict[str, tuple] = {}
    node_variants: dict[str, list[dict]] = defaultdict(list)
    duplicate_node_conflicts: list[dict] = []
    duplicate_rel_conflicts: list[dict] = []
    all_node_ids: set[str] = set()
    endpoint_refs: list[dict] = []
    label_counts: Counter[str] = Counter()
    rel_counts: Counter[str] = Counter()
    out_by_from: dict[str, list[tuple[str, str]]] = defaultdict(list)
    overlay_records, overlay_errors = read_patch_overlay(accepted_patch_paths)

    for batch in batches:
        manifest_errors.extend(validate_manifest(batch.path / "manifest.json"))

    for path in files:
        for lineno, record in read_jsonl(path, parse_errors):
            schema_errors.extend(validate_record(record, path, lineno, labels, rel_types))
            if record.get("record_type") == "node":
                node_id = record["id"]
                sig = property_signature(record)
                all_node_ids.add(node_id)
                node_variants[node_id].append(record)
                label_counts.update(record.get("labels") or [])
                if node_id in node_defs and node_defs[node_id] != sig:
                    duplicate_node_conflicts.append(
                        {"id": node_id, "file": rel(path), "line": lineno}
                    )
                node_defs.setdefault(node_id, sig)
                if set(record.get("labels") or []) & {"Fallbeispiel", "Kennwert", "Datenqualitaet"}:
                    forbidden_nodes.append({"id": node_id, "file": rel(path), "line": lineno})
            elif record.get("record_type") == "rel":
                rel_id = record["id"]
                sig = (
                    record.get("from"),
                    record.get("type"),
                    record.get("to"),
                    json.dumps(record.get("properties") or {}, ensure_ascii=False, sort_keys=True),
                )
                if rel_id in rel_defs and rel_defs[rel_id] != sig:
                    duplicate_rel_conflicts.append(
                        {"id": rel_id, "file": rel(path), "line": lineno}
                    )
                rel_defs.setdefault(rel_id, sig)
                rel_counts.update([record.get("type")])
                out_by_from[record["from"]].append((record["type"], record["to"]))
                endpoint_refs.append(
                    {
                        "file": rel(path),
                        "line": lineno,
                        "rel_id": rel_id,
                        "from": record["from"],
                        "to": record["to"],
                    }
                )
                if record.get("type") == "BELEGT_IN" and (record.get("properties") or {}).get("datenqualitaet") != "Belegt":
                    bad_belegt_in.append({"id": rel_id, "file": rel(path), "line": lineno})

    overlay_node_count = 0
    overlay_rel_count = 0
    for record in overlay_records:
        op = record.get("op")
        if op == "add_node":
            node_id = record.get("id")
            node_labels = record.get("labels") or []
            if not node_id or not node_labels:
                overlay_errors.append(
                    {
                        "file": record.get("_overlay_file"),
                        "line": record.get("_overlay_line"),
                        "error": "add_node overlay missing id/labels",
                    }
                )
                continue
            synthetic_record = {
                "record_type": "node",
                "id": node_id,
                "labels": node_labels,
                "properties": {"id": node_id, **dict(record.get("properties") or {})},
            }
            sig = property_signature(synthetic_record)
            all_node_ids.add(node_id)
            node_variants[node_id].append(synthetic_record)
            label_counts.update(node_labels)
            if node_id in node_defs and node_defs[node_id] != sig:
                duplicate_node_conflicts.append(
                    {
                        "id": node_id,
                        "file": record.get("_overlay_file"),
                        "line": record.get("_overlay_line"),
                    }
                )
            node_defs.setdefault(node_id, sig)
            overlay_node_count += 1
        elif op == "add_rel":
            endpoint_refs.append(
                {
                    "file": record.get("_overlay_file"),
                    "line": record.get("_overlay_line"),
                    "rel_id": record.get("id"),
                    "from": record.get("from"),
                    "to": record.get("to"),
                }
            )
            out_by_from[record.get("from")].append((record.get("type"), record.get("to")))
            rel_counts.update([record.get("type")])
            overlay_rel_count += 1

    missing_endpoints: list[dict] = []
    for ref in endpoint_refs:
        for side in ("from", "to"):
            if ref[side] not in all_node_ids:
                missing_endpoints.append({**ref, "side": side, "missing_id": ref[side]})

    # Check 8 & 9: tally unexpected labels / rel types already captured in schema_errors.
    unexpected_labels_counter: Counter[str] = Counter()
    unexpected_rel_types_counter: Counter[str] = Counter()
    for err in schema_errors:
        msg = err.get("error", "")
        if msg.startswith("unexpected label "):
            unexpected_labels_counter[msg[len("unexpected label "):]] += 1
        elif msg.startswith("unexpected relationship type "):
            unexpected_rel_types_counter[msg[len("unexpected relationship type "):]] += 1

    projects_no_source: list[str] = []
    projects_no_component_or_work: list[str] = []
    bg_no_source: list[str] = []
    bg_no_type: list[str] = []
    bg_no_material_or_level: list[str] = []
    for node_id, (node_labels, _) in node_defs.items():
        outs = out_by_from.get(node_id, [])
        if node_labels == ("Projekt",):
            if not any(t == "BELEGT_IN" for t, _ in outs):
                projects_no_source.append(node_id)
            if not any(t in {"HAT_BAUTEILGRUPPE", "NUTZT_BAUWERK"} for t, _ in outs):
                projects_no_component_or_work.append(node_id)
        if node_labels == ("Bauteilgruppe",):
            if not any(t == "BELEGT_IN" for t, _ in outs):
                bg_no_source.append(node_id)
            if not any(t == "HAT_BAUTEILTYP" for t, _ in outs):
                bg_no_type.append(node_id)
            if not any(t in {"NUTZT_MATERIAL", "HAT_BAUTEILEBENE"} for t, _ in outs):
                bg_no_material_or_level.append(node_id)

    unique_conflict_ids = sorted({item["id"] for item in duplicate_node_conflicts})
    patches = add_missing_endpoint_patches(missing_endpoints)
    for node_id in unique_conflict_ids:
        canonical, aliases = canonical_name(node_variants[node_id])
        if canonical:
            patches.append(
                {
                    "op": "canonicalize_node",
                    "id": node_id,
                    "canonical_name": canonical,
                    "aliases": aliases,
                    "reason": "Duplicate node id appears with conflicting display properties across current exports.",
                    "severity": "LOW",
                }
            )

    live_db, _ = query_live_db()
    round_dir.mkdir(parents=True, exist_ok=True)
    patch_dir = round_dir / "patches"
    patch_dir.mkdir(parents=True, exist_ok=True)
    placeholder_files = write_placeholders(round_dir, batches)

    patch_path = patch_dir / "global_technical.patch.jsonl"
    patch_path.write_text(
        "".join(json.dumps(patch, ensure_ascii=False, sort_keys=True) + "\n" for patch in patches),
        encoding="utf-8",
    )

    severity_counts = Counter(patch.get("severity", "INFO") for patch in patches)
    patch_manifest = {
        "review_round": "round_001",
        "task_type": "GLOBAL_AUDIT",
        "scope": "current Neo4j JSONL exports + live DB",
        "input_files": [rel(path) for path in files],
        "output_files": [
            rel(round_dir / "global_audit_report.md"),
            rel(round_dir / "exports_vs_live_db_diff.md"),
            rel(patch_path),
        ]
        + placeholder_files,
        "summary": {
            "patch_operations": len(patches),
            "blockers": severity_counts.get("BLOCKER", 0),
            "high": severity_counts.get("HIGH", 0),
            "medium": severity_counts.get("MEDIUM", 0),
            "low": severity_counts.get("LOW", 0),
            "info": severity_counts.get("INFO", 0),
        },
        "apply_order": [rel(patch_path)],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (round_dir / "patch_manifest.json").write_text(
        json.dumps(patch_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    export_counts = {
        "batches": len(batches),
        "project_files": sum(len(batch.project_files) for batch in batches),
        "files_scanned": len(files),
        "nodes_unique": len(node_defs),
        "relationships_unique": len(rel_defs),
    }
    audit_counts = {
        "parse_errors": len(parse_errors),
        "schema_errors": len(schema_errors),
        "manifest_errors": len(manifest_errors),
        "overlay_errors": len(overlay_errors),
        "overlay_nodes": overlay_node_count,
        "overlay_relationships": overlay_rel_count,
        "missing_endpoints": len(missing_endpoints),
        "duplicate_node_conflicts": len(duplicate_node_conflicts),
        "duplicate_node_conflict_ids": len(unique_conflict_ids),
        "duplicate_relationship_conflicts": len(duplicate_rel_conflicts),
        "forbidden_nodes": len(forbidden_nodes),
        "bad_belegt_in": len(bad_belegt_in),
        "projects_no_source": len(projects_no_source),
        "projects_no_component_or_work": len(projects_no_component_or_work),
        "bg_no_source": len(bg_no_source),
        "bg_no_type": len(bg_no_type),
        "bg_no_material_or_level": len(bg_no_material_or_level),
        "unexpected_label_types": len(unexpected_labels_counter),
        "unexpected_label_occurrences": sum(unexpected_labels_counter.values()),
        "unexpected_rel_type_types": len(unexpected_rel_types_counter),
        "unexpected_rel_type_occurrences": sum(unexpected_rel_types_counter.values()),
        "low_degree_non_vocab_nodes": (
            live_db.get("checks", {}).get("low_degree_non_vocab_nodes", "n/a")
            if live_db.get("available") else "n/a"
        ),
    }

    batch_rows = [
        [
            f"batch_{b.batch_id}",
            rel(b.path),
            len(b.project_files),
            "yes" if b.manifest_exists else "no",
            "yes" if b.delta_exists else "no",
            b.delta_nonempty_lines,
        ]
        for b in batches
    ]
    report = [
        "# Round 001 Global Technical Audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Summary",
        "",
        markdown_table(
            ["Metric", "Value"],
            [[key, value] for key, value in {**export_counts, **audit_counts}.items()],
        ),
        "",
        "## Current Batch Selection",
        "",
        markdown_table(
            ["Batch", "Path", "Projects", "Manifest", "Delta", "Delta rows"],
            batch_rows,
        ),
        "",
        "## Accepted Patch Overlay",
        "",
        "- Overlay patches: "
        + (", ".join(rel(path) for path in accepted_patch_paths) or "none"),
        f"- Overlay nodes: {overlay_node_count}",
        f"- Overlay relationships: {overlay_rel_count}",
        f"- Overlay errors: {len(overlay_errors)}",
        "",
        "## Blocking Findings",
        "",
        "- Missing relationship endpoints: "
        + (", ".join(sorted({item["missing_id"] for item in missing_endpoints})) or "none"),
        "- Missing manifests: "
        + (", ".join(f"batch_{b.batch_id}" for b in batches if not b.manifest_exists) or "none"),
        "- Missing controlled term delta files: "
        + (", ".join(f"batch_{b.batch_id}" for b in batches if not b.delta_exists) or "none"),
        "",
        "## Missing Endpoint Details",
        "",
        markdown_table(
            ["Missing id", "Side", "Relationship", "File", "Line"],
            [
                [item["missing_id"], item["side"], item["rel_id"], item["file"], item["line"]]
                for item in missing_endpoints
            ]
            or [["none", "", "", "", ""]],
        ),
        "",
        "## Duplicate Node Property Conflicts",
        "",
        f"{len(unique_conflict_ids)} unique node ids have conflicting properties across export files.",
        "",
        markdown_table(
            ["Node id", "Canonical candidate", "Aliases"],
            [
                [
                    node_id,
                    canonical_name(node_variants[node_id])[0] or "",
                    ", ".join(canonical_name(node_variants[node_id])[1]),
                ]
                for node_id in unique_conflict_ids[:50]
            ]
            or [["none", "", ""]],
        ),
        "",
        "## Schema And Integrity Notes",
        "",
        f"- JSON parse errors: {len(parse_errors)}",
        f"- Record schema errors: {len(schema_errors)}",
        f"- Manifest errors: {len(manifest_errors)}",
        f"- Overlay errors: {len(overlay_errors)}",
        f"- Forbidden nodes: {len(forbidden_nodes)}",
        f"- BELEGT_IN without datenqualitaet=Belegt: {len(bad_belegt_in)}",
        f"- Projekt without BELEGT_IN: {len(projects_no_source)}",
        f"- Bauteilgruppe without BELEGT_IN: {len(bg_no_source)}",
        f"- Bauteilgruppe without HAT_BAUTEILTYP: {len(bg_no_type)}",
        "",
        "## Check 8: Unexpected Node Labels in Exports",
        "",
        f"{sum(unexpected_labels_counter.values())} occurrence(s) across "
        f"{len(unexpected_labels_counter)} unexpected label type(s).",
        "",
        (
            markdown_table(
                ["Label", "Occurrences"],
                [[lbl, cnt] for lbl, cnt in unexpected_labels_counter.most_common()],
            )
            if unexpected_labels_counter
            else "_None — all labels conform to schema._"
        ),
        "",
        "## Check 9: Unexpected Relationship Types in Exports",
        "",
        f"{sum(unexpected_rel_types_counter.values())} occurrence(s) across "
        f"{len(unexpected_rel_types_counter)} unexpected relationship type(s).",
        "",
        (
            markdown_table(
                ["Relationship type", "Occurrences"],
                [[rt, cnt] for rt, cnt in unexpected_rel_types_counter.most_common()],
            )
            if unexpected_rel_types_counter
            else "_None — all relationship types conform to schema._"
        ),
        "",
        "## Check 13: Low-Degree Non-Vocabulary Nodes (Live DB)",
        "",
        (
            (
                f"{live_db['checks']['low_degree_non_vocab_nodes']} non-vocabulary node(s) "
                "with degree\u00a0< 2."
            )
            if live_db.get("available") and "low_degree_non_vocab_nodes" in live_db.get("checks", {})
            else "_Live DB unavailable — check skipped._"
        ),
        "",
        (
            markdown_table(
                ["Label", "id", "name", "degree"],
                [
                    [row.get("label"), row.get("id"), row.get("name"), row.get("degree")]
                    for row in live_db.get("low_degree_non_vocab_nodes", [])
                ],
            )
            if live_db.get("available") and live_db.get("low_degree_non_vocab_nodes")
            else "_No low-degree non-vocabulary nodes found._"
        ),
        "",
        "## Patch Output",
        "",
        f"- Patch file: `{rel(patch_path)}`",
        f"- Patch operations: {len(patches)}",
        "- Generated placeholders live under `"
        + rel(round_dir / "placeholders")
        + "` and are review outputs only.",
        "",
    ]
    (round_dir / "global_audit_report.md").write_text("\n".join(report), encoding="utf-8")

    diff_lines = [
        "# Exports vs Live DB Diff",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Counts",
        "",
        markdown_table(
            ["Metric", "Exports", "Live DB"],
            [
                ["nodes", export_counts["nodes_unique"], (live_db.get("counts") or {}).get("nodes") if live_db.get("available") else "unavailable"],
                ["relationships", export_counts["relationships_unique"], (live_db.get("counts") or {}).get("relationships") if live_db.get("available") else "unavailable"],
                ["projects", label_counts.get("Projekt", 0), live_db.get("checks", {}).get("projects") if live_db.get("available") else "unavailable"],
                ["bauteilgruppen", label_counts.get("Bauteilgruppe", 0), live_db.get("checks", {}).get("bg") if live_db.get("available") else "unavailable"],
            ],
        ),
        "",
        "## Live DB Technical Checks",
        "",
    ]
    if live_db.get("available"):
        diff_lines.append(markdown_table(["Check", "Count"], [[k, v] for k, v in live_db["checks"].items()]))
        diff_lines.extend(
            [
                "",
                "## Live DB Samples",
                "",
                "### Projects without component/work links",
                "",
                markdown_table(
                    ["id", "name"],
                    [[row.get("id"), row.get("name")] for row in live_db.get("projects_without_component_or_work", [])]
                    or [["none", ""]],
                ),
                "",
                "### Direct-reuse Bauteilgruppen without donor",
                "",
                markdown_table(
                    ["id", "name"],
                    [[row.get("id"), row.get("name")] for row in live_db.get("direct_reuse_without_donor", [])]
                    or [["none", ""]],
                ),
                "",
                "### Direct-reuse Bauteilgruppen without receiver",
                "",
                markdown_table(
                    ["id", "name"],
                    [[row.get("id"), row.get("name")] for row in live_db.get("direct_reuse_without_receiver", [])]
                    or [["none", ""]],
                ),
                "",
                "### Duplicate display-name candidates",
                "",
                markdown_table(
                    ["label", "name_key", "count", "ids"],
                    [
                        [row.get("label"), row.get("name_key"), row.get("c"), ", ".join(row.get("ids") or [])]
                        for row in live_db.get("duplicate_names", [])
                    ]
                    or [["none", "", "", ""]],
                ),
                "",
                "### Check 13: Low-degree non-vocabulary nodes",
                "",
                markdown_table(
                    ["label", "id", "name", "degree"],
                    [
                        [row.get("label"), row.get("id"), row.get("name"), row.get("degree")]
                        for row in live_db.get("low_degree_non_vocab_nodes", [])
                    ]
                    or [["none", "", "", ""]],
                ),
                "",
            ]
        )
    else:
        diff_lines.append(f"Live DB unavailable: {live_db.get('error')}")
    (round_dir / "exports_vs_live_db_diff.md").write_text("\n".join(diff_lines), encoding="utf-8")

    return {
        "round_dir": str(round_dir),
        "export_counts": export_counts,
        "audit_counts": audit_counts,
        "patch_operations": len(patches),
        "accepted_patch_overlays": [str(path) for path in accepted_patch_paths],
        "live_db": live_db.get("counts") if live_db.get("available") else live_db,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--round-dir",
        type=Path,
        default=repo_root() / "_neo4j" / "review" / "round_001",
    )
    parser.add_argument(
        "--accepted-patch",
        action="append",
        type=Path,
        default=[],
        help="Patch JSONL to treat as an accepted staging overlay during export audit.",
    )
    args = parser.parse_args()
    result = run(args.round_dir, args.accepted_patch)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
