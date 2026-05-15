"""Round 002 baseline — global technical audit against the post-2026-05-15 corpus.

Replaces `run_neo4j_current_build_review.py`, which reads from the archived
`_neo4j/batch/` tree. The new authoritative inputs are:

  _neo4j/processed/projects/records/p_*.kg.jsonl                  (75 projects)
  _neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl
  _neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl
  _neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl

Outputs (under _neo4j/review/round_002_baseline/ by default):

  global_audit_report.md
  exports_vs_live_db_diff.md
  patches/global_technical.patch.jsonl      # deterministic fixes only
  needs_review.patch.jsonl                  # round-001 items still present in live graph
  patch_manifest.json

Live DB checks run against `mit-bestand` via _scripts/neo4j_env.resolve_connection().
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


NODE_ID_RE = re.compile(r"^[a-z][a-z0-9]*_[a-z0-9_]+$")
REL_ID_RE = re.compile(r"^r_[a-z0-9_]+__[A-Z0-9_]+__[a-z0-9_]+.*$")

# Vocab labels and their canonical id prefixes (round-002 scope).
# Source: ROUND_002_PLAN.md §4.1.
VOCAB_PREFIXES: dict[str, str] = {
    "Akteurrolle": "ar",
    "Akteurtyp": "at",
    "Aufbereitungsverfahren": "av",
    "BauaufgabeIntervention": "bai",
    "Bauobjektklasse": "bok",
    "Bauobjektrolle": "bor",
    "Bausystem": "bsys",
    "Bauteilebene": "be",
    "Bauteiltyp": "bt",
    "Bauweise": "bauw",
    "Beschaffungsweg": "bweg",
    "Funktionswechsel": "fw",
    "Huerde": "h",
    "HuerdeKategorie": "hk",
    "Land": "land",
    "Leistungsanforderung": "la",
    "Logistik": "log",
    "Material": "mat",
    "Materialgruppe": "mg",
    "Methode": "meth",
    "Norm": "norm",
    "Nutzung": "nut",
    "Programm": "prog",
    "Prozessphase": "phase",
    "PruefungNachweis": "pr",
    "RechtlicheBedingung": "rb",
    "Ressourcenquelle": "rq",
    "Rueckbauverfahren": "rv",
    "Schadstoff": "s",
    "Software": "software",
    "Stadt": "stadt",
    "Status": "status",
    "Tool": "tool",
    "Tragwerksprinzip": "tp",
    "Verbindungstechnik": "vt",
    "WiederverwendungsArt": "wva",
    "Wirtschaft": "wi",
    "ZertifizierungBewertungssystem": "zbs",
}

VOCAB_LABELS: frozenset[str] = frozenset(VOCAB_PREFIXES) | {"Datenqualitaet"}

# Round-002 family assignment for each vocab label. Maps to §5 of the plan.
FAMILY_FOR_LABEL: dict[str, str] = {
    "Material": "1_material",
    "Materialgruppe": "1_material",
    "Stadt": "2_stadt_land",
    "Land": "2_stadt_land",
    "Bauteiltyp": "3_bauteiltyp",
    "Bauteilebene": "3_bauteiltyp",
    "Huerde": "4_huerde",
    "HuerdeKategorie": "4_huerde",
    "Akteurrolle": "5_akteur_vocab",
    "Akteurtyp": "5_akteur_vocab",
    "Bauobjektrolle": "6_bauobjekt",
    "Bauobjektklasse": "6_bauobjekt",
    "Status": "7_status_wva",
    "WiederverwendungsArt": "7_status_wva",
    "Norm": "8_norm_pruefung",
    "PruefungNachweis": "8_norm_pruefung",
    "Leistungsanforderung": "8_norm_pruefung",
    "Methode": "9_methode_rueckbau",
    "Rueckbauverfahren": "9_methode_rueckbau",
    "Aufbereitungsverfahren": "9_methode_rueckbau",
    "ZertifizierungBewertungssystem": "10_zertifizierung",
    "Programm": "10_zertifizierung",
    "Tool": "10_zertifizierung",
    "Software": "10_zertifizierung",
}

CONTENT_TRACK: dict[str, str] = {
    "Akteur": "actor_registry",
    "Bauteilgruppe": "round_003",
    "Bauwerk": "round_003",
    "Projekt": "round_003",
    "Quelle": "round_003",
    "Wiederverwendungskette": "round_003",
}


@dataclass
class InputBundle:
    seed: Path
    delta: Path
    actor_registry: Path
    project_records: list[Path] = field(default_factory=list)


def rel(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root()))
    except ValueError:
        return str(path)


def load_contract_enums() -> tuple[set[str], set[str], set[str]]:
    """Return (labels, project_batches_rel_types, actor_registry_rel_types).

    Project records validate against project_batches; the actor registry adds the
    extra rel types declared in the actor_registry_v1_2 schema patch.
    """
    schema_path = (
        repo_root()
        / "_neo4j"
        / "contracts"
        / "project_batches_v1_1"
        / "schemas"
        / "kg_jsonl_record_schema.json"
    )
    data = json.loads(schema_path.read_text(encoding="utf-8"))
    node_schema, rel_schema = data["oneOf"]
    labels = set(node_schema["properties"]["labels"]["items"]["enum"])
    project_rel_types = set(rel_schema["properties"]["type"]["enum"])

    patch_path = (
        repo_root()
        / "_neo4j"
        / "contracts"
        / "actor_registry_v1_2"
        / "schema_patch.actor_registry_v1_2.json"
    )
    actor_rel_types = set(project_rel_types)
    if patch_path.is_file():
        patch = json.loads(patch_path.read_text(encoding="utf-8"))
        actor_rel_types.update(patch.get("add_relationship_types") or [])
    return labels, project_rel_types, actor_rel_types


def gather_inputs() -> InputBundle:
    base = repo_root() / "_neo4j" / "processed"
    bundle = InputBundle(
        seed=base / "projects" / "vocabulary" / "controlled_vocabulary.seed.kg.jsonl",
        delta=base / "projects" / "vocabulary" / "controlled_terms.merged.kg.jsonl",
        actor_registry=base / "actor_registry" / "actor_registry.canonical.kg.jsonl",
        project_records=sorted((base / "projects" / "records").glob("p_*.kg.jsonl")),
    )
    return bundle


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
                parse_errors.append({"file": rel(path), "line": lineno, "error": str(exc)})
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


def property_signature(record: dict) -> tuple:
    props = dict(record.get("properties") or {})
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


def classify_id(node_id: str, label_hint: str | None = None) -> tuple[str, str]:
    """Return (kind, route) where kind in {vocab, content, unknown} and route is
    the family slug or content track slug."""
    if label_hint and label_hint in FAMILY_FOR_LABEL:
        return "vocab", FAMILY_FOR_LABEL[label_hint]
    if label_hint and label_hint in CONTENT_TRACK:
        return "content", CONTENT_TRACK[label_hint]
    prefix = node_id.split("_", 1)[0]
    for label, pref in VOCAB_PREFIXES.items():
        if pref == prefix:
            return "vocab", FAMILY_FOR_LABEL.get(label, "")
    if prefix in {"a", "bg", "bw", "p", "q", "wk"}:
        return "content", {"a": "actor_registry"}.get(prefix, "round_003")
    return "unknown", ""


def query_live_db() -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError:
        return {"available": False, "error": "neo4j driver not installed"}

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        return {"available": False, "error": "missing Neo4j connection settings"}

    result: dict[str, Any] = {"available": False}
    queries = {
        "counts": (
            "MATCH (n) WITH count(n) AS nodes "
            "MATCH ()-[r]->() RETURN nodes, count(r) AS relationships"
        ),
        "forbidden_nodes": "MATCH (n) WHERE n:Fallbeispiel OR n:Kennwert RETURN count(n) AS c",
        "bad_belegt_in": (
            "MATCH ()-[r:BELEGT_IN]->() "
            "WHERE r.datenqualitaet <> 'Belegt' OR r.datenqualitaet IS NULL "
            "RETURN count(r) AS c"
        ),
        "projects": "MATCH (p:Projekt) RETURN count(p) AS c",
        "projects_no_source": "MATCH (p:Projekt) WHERE NOT (p)-[:BELEGT_IN]->(:Quelle) RETURN count(p) AS c",
        "projects_no_component_or_work": (
            "MATCH (p:Projekt) "
            "WHERE NOT ((p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) "
            "OR (p)-[:NUTZT_BAUWERK]->(:Bauwerk)) RETURN count(p) AS c"
        ),
        "bg": "MATCH (bg:Bauteilgruppe) RETURN count(bg) AS c",
        "bg_no_source": "MATCH (bg:Bauteilgruppe) WHERE NOT (bg)-[:BELEGT_IN]->(:Quelle) RETURN count(bg) AS c",
        "bg_no_type": "MATCH (bg:Bauteilgruppe) WHERE NOT (bg)-[:HAT_BAUTEILTYP]->(:Bauteiltyp) RETURN count(bg) AS c",
        "bg_no_material_or_level": (
            "MATCH (bg:Bauteilgruppe) "
            "WHERE NOT ((bg)-[:NUTZT_MATERIAL]->(:Material) "
            "OR (bg)-[:HAT_BAUTEILEBENE]->(:Bauteilebene)) RETURN count(bg) AS c"
        ),
        "direct_bg_no_donor": (
            "MATCH (bg:Bauteilgruppe) "
            "WHERE bg.counts_as_direct_reuse = true "
            "AND NOT (bg)-[:AUS_BAUWERK]->(:Bauwerk) RETURN count(bg) AS c"
        ),
        "direct_bg_no_receiver": (
            "MATCH (bg:Bauteilgruppe) "
            "WHERE bg.counts_as_direct_reuse = true "
            "AND NOT (bg)-[:EINGEBAUT_IN]->(:Bauwerk) RETURN count(bg) AS c"
        ),
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
                "duplicate_names_vocab": [],
                "duplicate_names_content": [],
                "low_degree_non_vocab_nodes": [],
                "node_ids": set(),
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
                    "RETURN label, count(*) AS count ORDER BY count DESC, label"
                )
            ]
            result["relationship_type_counts"] = [
                dict(row)
                for row in session.run(
                    "MATCH ()-[r]->() RETURN type(r) AS type, count(*) AS count "
                    "ORDER BY count DESC, type"
                )
            ]
            result["all_relationship_types"] = [
                row["relationshipType"]
                for row in session.run(
                    "CALL db.relationshipTypes() YIELD relationshipType "
                    "RETURN relationshipType"
                )
            ]
            result["all_node_labels"] = [
                row["label"]
                for row in session.run(
                    "CALL db.labels() YIELD label RETURN label"
                )
            ]

            vocab_list = list(VOCAB_LABELS)
            result["duplicate_names_vocab"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) WHERE n.name IS NOT NULL AND labels(n)[0] IN $vocab "
                    "WITH labels(n)[0] AS label, toLower(toString(n.name)) AS name_key, "
                    "     collect(n.id) AS ids, count(*) AS c "
                    "WHERE c > 1 RETURN label, name_key, ids, c "
                    "ORDER BY c DESC, label, name_key",
                    vocab=vocab_list,
                )
            ]
            result["duplicate_names_content"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) WHERE n.name IS NOT NULL AND NOT labels(n)[0] IN $vocab "
                    "WITH labels(n)[0] AS label, toLower(toString(n.name)) AS name_key, "
                    "     collect(n.id) AS ids, count(*) AS c "
                    "WHERE c > 1 RETURN label, name_key, ids, c "
                    "ORDER BY c DESC, label, name_key",
                    vocab=vocab_list,
                )
            ]

            ld_count = session.run(
                "MATCH (n) WHERE NOT labels(n)[0] IN $vocab "
                "WITH n, COUNT { (n)--() } AS degree "
                "WHERE degree < 2 RETURN count(n) AS c",
                vocab=vocab_list,
            ).single()
            result["checks"]["low_degree_non_vocab_nodes"] = int(ld_count["c"])
            result["low_degree_non_vocab_nodes"] = [
                dict(row)
                for row in session.run(
                    "MATCH (n) WHERE NOT labels(n)[0] IN $vocab "
                    "WITH n, COUNT { (n)--() } AS degree "
                    "WHERE degree < 2 "
                    "RETURN labels(n)[0] AS label, n.id AS id, n.name AS name, degree "
                    "ORDER BY degree ASC, label, id LIMIT 100",
                    vocab=vocab_list,
                )
            ]

            result["node_ids"] = {
                row["id"]
                for row in session.run("MATCH (n) WHERE n.id IS NOT NULL RETURN n.id AS id")
                if row["id"]
            }
    except Exception as exc:  # noqa: BLE001
        result = {"available": False, "error": str(exc)}
    finally:
        driver.close()
    return result


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def load_round001_needs_review() -> list[dict]:
    path = (
        repo_root()
        / "_neo4j"
        / "review"
        / "round_001_apply_test"
        / "needs_review.patch.jsonl"
    )
    if not path.is_file():
        return []
    out: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            f.write("\n")


def run(round_dir: Path) -> dict:
    round_dir = round_dir.resolve()
    round_dir.mkdir(parents=True, exist_ok=True)
    (round_dir / "patches").mkdir(parents=True, exist_ok=True)

    labels, project_rel_types, actor_rel_types = load_contract_enums()
    inputs = gather_inputs()
    # actor registry validates against the patched contract; everything else
    # against the project_batches contract.
    rel_types_by_file: dict[Path, set[str]] = {inputs.actor_registry: actor_rel_types}
    files: list[Path] = [inputs.seed, inputs.delta, inputs.actor_registry] + inputs.project_records
    for path in [inputs.seed, inputs.delta] + inputs.project_records:
        rel_types_by_file[path] = project_rel_types

    parse_errors: list[dict] = []
    schema_errors: list[dict] = []
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

    for path in files:
        if not path.is_file():
            schema_errors.append({"file": rel(path), "error": "expected input file missing"})
            continue
        path_rel_types = rel_types_by_file.get(path, project_rel_types)
        for lineno, record in read_jsonl(path, parse_errors):
            schema_errors.extend(validate_record(record, path, lineno, labels, path_rel_types))
            if record.get("record_type") == "node":
                node_id = record["id"]
                sig = property_signature(record)
                all_node_ids.add(node_id)
                node_variants[node_id].append(record)
                label_counts.update(record.get("labels") or [])
                if node_id in node_defs and node_defs[node_id] != sig:
                    duplicate_node_conflicts.append({"id": node_id, "file": rel(path), "line": lineno})
                node_defs.setdefault(node_id, sig)
                if set(record.get("labels") or []) & {"Fallbeispiel", "Kennwert"}:
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
                    duplicate_rel_conflicts.append({"id": rel_id, "file": rel(path), "line": lineno})
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

    missing_endpoints: list[dict] = []
    for ref in endpoint_refs:
        for side in ("from", "to"):
            if ref[side] not in all_node_ids:
                missing_endpoints.append({**ref, "side": side, "missing_id": ref[side]})

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
    deterministic_patches: list[dict] = []
    for node_id in unique_conflict_ids:
        canonical, aliases = canonical_name(node_variants[node_id])
        if canonical:
            deterministic_patches.append(
                {
                    "op": "canonicalize_node",
                    "id": node_id,
                    "canonical_name": canonical,
                    "aliases": aliases,
                    "reason": (
                        "Duplicate node id appears with conflicting display "
                        "properties across current processed import payloads."
                    ),
                    "severity": "LOW",
                }
            )

    live_db = query_live_db()
    live_ids: set[str] = live_db.get("node_ids") or set() if live_db.get("available") else set()

    # Round-001 needs_review filtered against the current live graph.
    r001_records = load_round001_needs_review()
    needs_review_filtered: list[dict] = []
    for record in r001_records:
        node_id = record.get("id")
        if not node_id:
            continue
        present = node_id in live_ids if live_db.get("available") else None
        kind, route = classify_id(node_id)
        annotated = dict(record)
        annotated["round_002_kind"] = kind
        annotated["round_002_route"] = route
        annotated["round_002_present_in_live_graph"] = present
        if present is not False:
            needs_review_filtered.append(annotated)

    # Persist outputs.
    patch_path = round_dir / "patches" / "global_technical.patch.jsonl"
    write_jsonl(patch_path, deterministic_patches)

    needs_review_path = round_dir / "needs_review.patch.jsonl"
    write_jsonl(needs_review_path, needs_review_filtered)

    severity_counts = Counter(patch.get("severity", "INFO") for patch in deterministic_patches)
    patch_manifest = {
        "review_round": "round_002_baseline",
        "task_type": "GLOBAL_AUDIT",
        "scope": "post-2026-05-15 processed payloads + live mit-bestand graph",
        "input_files": [rel(p) for p in files],
        "output_files": [
            rel(round_dir / "global_audit_report.md"),
            rel(round_dir / "exports_vs_live_db_diff.md"),
            rel(patch_path),
            rel(needs_review_path),
        ],
        "summary": {
            "patch_operations": len(deterministic_patches),
            "blockers": severity_counts.get("BLOCKER", 0),
            "high": severity_counts.get("HIGH", 0),
            "medium": severity_counts.get("MEDIUM", 0),
            "low": severity_counts.get("LOW", 0),
            "info": severity_counts.get("INFO", 0),
        },
        "needs_review": {
            "round_001_count": len(r001_records),
            "still_present_in_live_graph": sum(
                1 for r in needs_review_filtered if r.get("round_002_present_in_live_graph")
            ),
            "unknown_presence": sum(
                1 for r in needs_review_filtered if r.get("round_002_present_in_live_graph") is None
            ),
            "dropped_not_in_live_graph": len(r001_records) - len(needs_review_filtered),
        },
        "apply_order": [rel(patch_path)],
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (round_dir / "patch_manifest.json").write_text(
        json.dumps(patch_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    export_counts = {
        "project_files": len(inputs.project_records),
        "files_scanned": sum(1 for p in files if p.is_file()),
        "nodes_unique": len(node_defs),
        "relationships_unique": len(rel_defs),
    }
    # Per-file schema error breakdown
    schema_errors_by_file: Counter[str] = Counter()
    for err in schema_errors:
        schema_errors_by_file[err.get("file", "?")] += 1

    # Live-graph rel types / labels not in contract
    live_unknown_rel_types: list[str] = []
    live_unknown_labels: list[str] = []
    if live_db.get("available"):
        live_unknown_rel_types = sorted(
            set(live_db.get("all_relationship_types") or []) - (project_rel_types | actor_rel_types)
        )
        live_unknown_labels = sorted(
            set(live_db.get("all_node_labels") or []) - labels
        )

    audit_counts = {
        "parse_errors": len(parse_errors),
        "schema_errors": len(schema_errors),
        "schema_errors_actor_registry": schema_errors_by_file.get(rel(inputs.actor_registry), 0),
        "schema_errors_project_records": sum(
            v for k, v in schema_errors_by_file.items() if k.startswith(rel(repo_root() / "_neo4j" / "processed" / "projects" / "records"))
        ),
        "live_unknown_rel_types": len(live_unknown_rel_types),
        "live_unknown_labels": len(live_unknown_labels),
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
        "low_degree_non_vocab_nodes": (
            live_db.get("checks", {}).get("low_degree_non_vocab_nodes", "n/a")
            if live_db.get("available")
            else "n/a"
        ),
    }

    classified_conflicts: list[list[Any]] = []
    for node_id in unique_conflict_ids[:200]:
        variants = node_variants[node_id]
        cn, aliases = canonical_name(variants)
        node_label = (variants[0].get("labels") or [None])[0]
        kind, route = classify_id(node_id, label_hint=node_label)
        classified_conflicts.append([
            node_id, node_label or "", kind, route, cn or "", ", ".join(aliases),
        ])

    report_lines = [
        "# Round 002 Baseline — Global Technical Audit",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "**Inputs:** post-2026-05-15 processed payloads "
        "(`_neo4j/processed/projects/`, `_neo4j/processed/actor_registry/`) + live `mit-bestand`.",
        "**Supersedes:** `_neo4j/review/round_001/global_audit_report.md` "
        "(the underlying 20-batch tree is archived).",
        "",
        "## Summary",
        "",
        markdown_table(
            ["Metric", "Value"],
            [[key, value] for key, value in {**export_counts, **audit_counts}.items()],
        ),
        "",
        "## Inputs",
        "",
        markdown_table(
            ["File", "Lines (non-empty)"],
            [
                [
                    rel(path),
                    sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
                    if path.is_file()
                    else "missing",
                ]
                for path in [inputs.seed, inputs.delta, inputs.actor_registry]
            ]
            + [["+ project records", len(inputs.project_records)]],
        ),
        "",
        "## Schema Errors by File",
        "",
        markdown_table(
            ["File", "Errors"],
            [[k, v] for k, v in sorted(schema_errors_by_file.items(), key=lambda kv: -kv[1])]
            or [["none", 0]],
        ),
        "",
        "## Contract Drift vs Live Graph",
        "",
        f"- Live rel types not in any contract: {len(live_unknown_rel_types)}"
        + (f" — {', '.join(live_unknown_rel_types)}" if live_unknown_rel_types else ""),
        f"- Live node labels not in any contract: {len(live_unknown_labels)}"
        + (f" — {', '.join(live_unknown_labels)}" if live_unknown_labels else ""),
        "",
        "## Blocking Findings",
        "",
        "- Missing relationship endpoints: "
        + (", ".join(sorted({item["missing_id"] for item in missing_endpoints})) or "none"),
        f"- Forbidden node labels in payloads: {len(forbidden_nodes)}",
        f"- BELEGT_IN without datenqualitaet=Belegt: {len(bad_belegt_in)}",
        f"- Projekt without BELEGT_IN: {len(projects_no_source)}",
        f"- Projekt without component/work links: {len(projects_no_component_or_work)}",
        f"- Bauteilgruppe without BELEGT_IN: {len(bg_no_source)}",
        f"- Bauteilgruppe without HAT_BAUTEILTYP: {len(bg_no_type)}",
        f"- Bauteilgruppe without NUTZT_MATERIAL or HAT_BAUTEILEBENE: {len(bg_no_material_or_level)}",
        "",
        "## Duplicate Node Property Conflicts (payloads)",
        "",
        f"{len(unique_conflict_ids)} unique node ids have conflicting properties across processed payloads.",
        "",
        markdown_table(
            ["Node id", "Label", "Kind", "Round-002 route", "Canonical candidate", "Aliases"],
            classified_conflicts or [["none", "", "", "", "", ""]],
        ),
        "",
        "## Round-001 needs_review Re-routing",
        "",
        f"Round-001 emitted {len(r001_records)} canonicalization candidates. "
        f"{patch_manifest['needs_review']['dropped_not_in_live_graph']} of those reference "
        "ids that no longer exist in the live graph and have been dropped. "
        f"{patch_manifest['needs_review']['still_present_in_live_graph']} remain "
        f"(plus {patch_manifest['needs_review']['unknown_presence']} with unknown "
        "presence because the live DB was unavailable).",
        "",
        markdown_table(
            ["Node id", "Kind", "Route", "Canonical candidate", "Present in live graph"],
            [
                [
                    record.get("id"),
                    record.get("round_002_kind"),
                    record.get("round_002_route") or "—",
                    record.get("canonical_name") or "",
                    record.get("round_002_present_in_live_graph"),
                ]
                for record in needs_review_filtered
            ]
            or [["none", "", "", "", ""]],
        ),
        "",
        "## Patch Output",
        "",
        f"- Deterministic patch: `{rel(patch_path)}`",
        f"- Deterministic patch operations: {len(deterministic_patches)}",
        f"- Round-001 needs_review filtered: `{rel(needs_review_path)}` ({len(needs_review_filtered)} records).",
        "",
    ]
    (round_dir / "global_audit_report.md").write_text("\n".join(report_lines), encoding="utf-8")

    diff_lines = [
        "# Exports vs Live DB Diff (round 002 baseline)",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Counts",
        "",
        markdown_table(
            ["Metric", "Payloads", "Live DB"],
            [
                [
                    "nodes",
                    export_counts["nodes_unique"],
                    (live_db.get("counts") or {}).get("nodes") if live_db.get("available") else "unavailable",
                ],
                [
                    "relationships",
                    export_counts["relationships_unique"],
                    (live_db.get("counts") or {}).get("relationships") if live_db.get("available") else "unavailable",
                ],
                [
                    "projects",
                    label_counts.get("Projekt", 0),
                    live_db.get("checks", {}).get("projects") if live_db.get("available") else "unavailable",
                ],
                [
                    "bauteilgruppen",
                    label_counts.get("Bauteilgruppe", 0),
                    live_db.get("checks", {}).get("bg") if live_db.get("available") else "unavailable",
                ],
            ],
        ),
        "",
    ]
    if live_db.get("available"):
        diff_lines.extend(
            [
                "## Live DB Technical Checks",
                "",
                markdown_table(
                    ["Check", "Count"],
                    [[k, v] for k, v in live_db["checks"].items()],
                ),
                "",
                "## Live DB Label Counts (top 30)",
                "",
                markdown_table(
                    ["Label", "Count"],
                    [[row.get("label"), row.get("count")] for row in live_db["label_counts"][:30]],
                ),
                "",
                "## Duplicate Display-Name Candidates — Vocab",
                "",
                markdown_table(
                    ["label", "name_key", "count", "ids"],
                    [
                        [row.get("label"), row.get("name_key"), row.get("c"), ", ".join(row.get("ids") or [])]
                        for row in live_db["duplicate_names_vocab"]
                    ]
                    or [["none", "", "", ""]],
                ),
                "",
                "## Duplicate Display-Name Candidates — Content",
                "",
                markdown_table(
                    ["label", "name_key", "count", "ids"],
                    [
                        [row.get("label"), row.get("name_key"), row.get("c"), ", ".join(row.get("ids") or [])]
                        for row in live_db["duplicate_names_content"]
                    ]
                    or [["none", "", "", ""]],
                ),
                "",
                "## Low-Degree Non-Vocabulary Nodes (live DB)",
                "",
                markdown_table(
                    ["label", "id", "name", "degree"],
                    [
                        [row.get("label"), row.get("id"), row.get("name"), row.get("degree")]
                        for row in live_db["low_degree_non_vocab_nodes"]
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
        "patch_operations": len(deterministic_patches),
        "needs_review_filtered": len(needs_review_filtered),
        "live_db": live_db.get("counts") if live_db.get("available") else {"available": False, "error": live_db.get("error")},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--round-dir",
        type=Path,
        default=repo_root() / "_neo4j" / "review" / "round_002_baseline",
    )
    args = parser.parse_args()
    result = run(args.round_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
