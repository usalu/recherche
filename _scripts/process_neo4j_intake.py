"""Process Neo4j intake packages into cleaned, provenance-bearing outputs.

Neo4j is the source of truth. This script does not replace the graph; it turns
incoming transport packages into reproducible import payloads plus provenance.

Supported adapters:

  projects
      Accepts the older project-batch export layout containing p_*.kg.jsonl
      files and optional controlled_terms.delta.jsonl files.

  actor-registry
      Accepts an actor-registry intake tree that already contains canonical
      chunk files under a canonical/ subtree.

Examples:

  python _scripts/process_neo4j_intake.py projects ^
      --input-root _neo4j/intake/archive/2026-05-15_project_batches_legacy/raw_tree ^
      --output-root _neo4j/processed/projects

  python _scripts/process_neo4j_intake.py actor-registry ^
      --input-root _neo4j/intake/archive/2026-05-15_actor_registry_seed/raw_tree ^
      --output-root _neo4j/processed/actor_registry
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from transform_registry_jsonl_to_canonical import _load_id_map, transform


def _read_jsonl(path: Path) -> list[dict]:
    records: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
    return records


def _write_jsonl(path: Path, records: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _relative_or_posix(path: Path, root: Path) -> str:
    try:
        return _relative(path, root)
    except ValueError:
        return path.as_posix()


def _json_key(record: dict) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _batch_id_from_path(path: Path) -> str | None:
    for part in path.parts:
        if part.startswith("batch_") and len(part) == len("batch_000"):
            return part
    return None


def _preferred_project_source(paths: list[Path]) -> Path:
    """Prefer standalone exports over duplicate packaged snapshots."""
    return sorted(paths, key=lambda p: ("neo4j_complete_repo_package" in p.parts, str(p)))[0]


def process_projects(input_root: Path, output_root: Path) -> None:
    project_files = sorted(input_root.rglob("p_*.kg.jsonl"))
    if not project_files:
        raise SystemExit(f"No project files found under {input_root}")

    by_name: dict[str, list[Path]] = defaultdict(list)
    for path in project_files:
        by_name[path.name].append(path)

    records_dir = output_root / "records"
    vocab_dir = output_root / "vocabulary"
    provenance_dir = output_root / "provenance"
    records_dir.mkdir(parents=True, exist_ok=True)
    vocab_dir.mkdir(parents=True, exist_ok=True)
    provenance_dir.mkdir(parents=True, exist_ok=True)

    provenance_rows: list[dict] = []
    copied = 0
    duplicate_groups = 0
    hash_conflicts: list[dict] = []

    for filename, paths in sorted(by_name.items()):
        chosen = _preferred_project_source(paths)
        target = records_dir / filename
        shutil.copy2(chosen, target)
        copied += 1

        hashes = {_sha256(path) for path in paths}
        if len(paths) > 1:
            duplicate_groups += 1
        if len(hashes) > 1:
            hash_conflicts.append(
                {
                    "project_file": filename,
                    "source_paths": [_relative(path, input_root) for path in paths],
                    "hashes": { _relative(path, input_root): _sha256(path) for path in paths },
                }
            )

        batch_ids = sorted({bid for path in paths if (bid := _batch_id_from_path(path))})
        numeric_batches = [
            int(batch_id.split("_")[1])
            for batch_id in batch_ids
            if batch_id.split("_")[1].isdigit()
        ]
        if numeric_batches and max(numeric_batches) >= 15:
            review_status = "pending_review"
        else:
            review_status = "legacy_review_required"

        provenance_rows.append(
            {
                "record_type": "project_file",
                "dataset": "projects",
                "project_file": filename,
                "chosen_source_path": _relative(chosen, input_root),
                "source_paths": [_relative(path, input_root) for path in paths],
                "source_batches": batch_ids,
                "merge_action": "packaging_dedupe" if len(paths) > 1 else "copied_unique",
                "review_status": review_status,
                "content_hashes_identical": len(hashes) == 1,
            }
        )

    # Preserve the seed if present.
    seed_candidates = sorted(input_root.rglob("controlled_vocabulary.seed.kg.jsonl"))
    if seed_candidates:
        shutil.copy2(_preferred_project_source(seed_candidates), vocab_dir / "controlled_vocabulary.seed.kg.jsonl")

    # Merge all actual delta records, excluding contract templates.
    delta_files = [
        path
        for path in sorted(input_root.rglob("controlled_terms.delta.jsonl"))
        if "templates" not in path.parts
    ]
    merged_delta: dict[str, dict] = {}
    delta_provenance: dict[str, list[str]] = defaultdict(list)
    for path in delta_files:
        for record in _read_jsonl(path):
            key = _json_key(record)
            merged_delta.setdefault(key, record)
            delta_provenance[key].append(_relative(path, input_root))

    _write_jsonl(vocab_dir / "controlled_terms.merged.kg.jsonl", merged_delta.values())

    for key, source_paths in sorted(delta_provenance.items()):
        record = merged_delta[key]
        provenance_rows.append(
            {
                "record_type": "controlled_term_record",
                "dataset": "projects",
                "id": record.get("id"),
                "merge_action": "merged_duplicate" if len(source_paths) > 1 else "copied_unique",
                "source_paths": source_paths,
                "review_status": "legacy_review_required",
            }
        )

    _write_jsonl(provenance_dir / "projects.provenance.jsonl", provenance_rows)

    report = [
        "# Projects processing report",
        "",
        f"- Input root: `{input_root.as_posix()}`",
        f"- Project files discovered: **{len(project_files)}**",
        f"- Project files emitted: **{copied}**",
        f"- Duplicate packaging groups collapsed: **{duplicate_groups}**",
        f"- Merged controlled-term records emitted: **{len(merged_delta)}**",
        f"- Hash conflicts across duplicate project filenames: **{len(hash_conflicts)}**",
        "",
        "## Review note",
        "",
        "The project corpus descends from the retired folder-first workflow. "
        "Files are organized here for review and replay, but remain `legacy_review_required` "
        "until checked against the live Neo4j graph.",
    ]
    if hash_conflicts:
        report += ["", "## Hash conflicts", ""]
        for conflict in hash_conflicts:
            report.append(f"- `{conflict['project_file']}` differs across source packages.")
    (output_root / "merge_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


@dataclass
class ActorRegistryMerge:
    records: list[dict]
    provenance: list[dict]
    node_records: int
    unique_nodes: int
    rel_records: int
    unique_rels: int
    node_conflicts: list[dict]


def _actor_registry_merge(canonical_files: list[Path], input_root: Path) -> ActorRegistryMerge:
    nodes_by_id: dict[str, dict] = {}
    node_sources: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    rels_by_key: dict[tuple, dict] = {}
    rel_sources: dict[tuple, list[tuple[Path, dict]]] = defaultdict(list)
    node_conflicts: list[dict] = []

    node_records = rel_records = 0
    for path in canonical_files:
        for record in _read_jsonl(path):
            if record.get("record_type") == "node":
                node_records += 1
                node_id = record["id"]
                if node_id in nodes_by_id and _json_key(nodes_by_id[node_id]) != _json_key(record):
                    node_conflicts.append(
                        {
                            "id": node_id,
                            "kept_source": _relative_or_posix(node_sources[node_id][0][0], input_root),
                            "conflicting_source": _relative_or_posix(path, input_root),
                        }
                    )
                nodes_by_id.setdefault(node_id, record)
                node_sources[node_id].append((path, record))
            elif record.get("record_type") == "rel":
                rel_records += 1
                props = record.get("properties") or {}
                key = (record["from"], record["type"], record["to"], props.get("scope", ""))
                rels_by_key.setdefault(key, record)
                rel_sources[key].append((path, record))

    merged_records = list(nodes_by_id.values()) + list(rels_by_key.values())
    provenance: list[dict] = []

    conflicted_node_ids = {conflict["id"] for conflict in node_conflicts}

    for node_id, sources in sorted(node_sources.items()):
        provenance.append(
            {
                "record_type": "node_provenance",
                "dataset": "actor_registry",
                "id": node_id,
                "source_files": [_relative_or_posix(path, input_root) for path, _ in sources],
                "source_chunks": sorted({path.parent.name for path, _ in sources}),
                "merge_key": "node:id",
                "merge_action": (
                    "conflict_kept_first"
                    if node_id in conflicted_node_ids
                    else "merged_duplicate" if len(sources) > 1 else "unique"
                ),
                "review_status": "needs_review" if node_id in conflicted_node_ids else "processed_reviewed_structure",
            }
        )

    for key, sources in sorted(rel_sources.items(), key=lambda item: tuple(map(str, item[0]))):
        winner = rels_by_key[key]
        provenance.append(
            {
                "record_type": "rel_provenance",
                "dataset": "actor_registry",
                "id": winner["id"],
                "from": winner["from"],
                "type": winner["type"],
                "to": winner["to"],
                "scope": (winner.get("properties") or {}).get("scope", ""),
                "source_record_ids": [record["id"] for _, record in sources],
                "source_files": [_relative_or_posix(path, input_root) for path, _ in sources],
                "source_chunks": sorted({path.parent.name for path, _ in sources}),
                "merge_key": "from+type+to+scope",
                "merge_action": "merged_duplicate" if len(sources) > 1 else "unique",
                "review_status": "processed_reviewed_structure",
            }
        )

    return ActorRegistryMerge(
        records=merged_records,
        provenance=provenance,
        node_records=node_records,
        unique_nodes=len(nodes_by_id),
        rel_records=rel_records,
        unique_rels=len(rels_by_key),
        node_conflicts=node_conflicts,
    )


def process_actor_registry(input_root: Path, output_root: Path) -> None:
    canonical_files = sorted((input_root / "canonical").rglob("*.canonical.kg.jsonl"))
    if not canonical_files:
        canonical_files = sorted(input_root.rglob("*.canonical.kg.jsonl"))
    if not canonical_files:
        registry_files = sorted(input_root.rglob("*.registry.kg.jsonl"))
        if registry_files:
            id_map = _load_id_map()
            chunks_root = output_root / "chunks"
            for source_path in registry_files:
                batch_name = source_path.parent.name
                stem = source_path.name.replace(".registry.kg.jsonl", "")
                target = chunks_root / batch_name / f"{stem}.canonical.kg.jsonl"
                transform(source_path, target, id_map)
            canonical_files = sorted(chunks_root.rglob("*.canonical.kg.jsonl"))
    if not canonical_files:
        raise SystemExit(f"No canonical actor-registry files found under {input_root}")

    output_root.mkdir(parents=True, exist_ok=True)
    merge = _actor_registry_merge(canonical_files, input_root)

    _write_jsonl(output_root / "actor_registry.canonical.kg.jsonl", merge.records)
    _write_jsonl(output_root / "provenance" / "actor_registry.provenance.jsonl", merge.provenance)
    _write_jsonl(output_root / "conflicts" / "node_conflicts.jsonl", merge.node_conflicts)

    report = [
        "# Actor registry processing report",
        "",
        f"- Input root: `{input_root.as_posix()}`",
        f"- Canonical chunk files read: **{len(canonical_files)}**",
        f"- Node records: **{merge.node_records}** → **{merge.unique_nodes}** unique node IDs",
        f"- Relationship records: **{merge.rel_records}** → **{merge.unique_rels}** unique semantic relationships",
        f"- Node content conflicts encountered: **{len(merge.node_conflicts)}**",
        "",
        "## Merge rules",
        "",
        "- Nodes merge by canonical `id`.",
        "- Relationships merge by `(from, type, to, scope)`.",
        "- Chunks are treated as provenance only, not as durable semantic units.",
    ]
    if merge.node_conflicts:
        report += ["", "## Node conflicts kept for review", ""]
        for conflict in merge.node_conflicts:
            report.append(
                f"- `{conflict['id']}`: kept `{conflict['kept_source']}`, "
                f"also saw `{conflict['conflicting_source']}`"
            )
    (output_root / "merge_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="adapter", required=True)

    for name in ("projects", "actor-registry"):
        sp = sub.add_parser(name)
        sp.add_argument("--input-root", type=Path, required=True)
        sp.add_argument("--output-root", type=Path, required=True)

    args = parser.parse_args()
    input_root = args.input_root.resolve()
    output_root = args.output_root.resolve()

    if not input_root.is_dir():
        raise SystemExit(f"Input root does not exist: {input_root}")

    if args.adapter == "projects":
        process_projects(input_root, output_root)
    elif args.adapter == "actor-registry":
        process_actor_registry(input_root, output_root)


if __name__ == "__main__":
    main()
