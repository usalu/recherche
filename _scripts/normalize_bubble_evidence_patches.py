"""Normalize reuse-bubble patches: evidence on node/rel properties only, no Quelle nodes."""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = [
    ROOT / "_neo4j/intake/runs/2026-06-05_swiss_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_germany_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_france_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_netherlands_reuse_bubble",
    ROOT / "_neo4j/intake/runs/2026-06-05_rotor_dc_reuse_bubble",
]

DROP_REL_PROPS = {
    "evidence_source_id",
    "secondary_evidence_source_ids",
    "archive_source_id",
    "metadata_sidecar_key",
    "evidence_claim_ids",
}


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def dump_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + ("\n" if rows else ""),
        encoding="utf-8",
    )


def is_quelle_node(rec: dict) -> bool:
    return rec.get("op") == "add_node" and bool(set(rec.get("labels") or []) & {"Quelle"})


def clean_rel_props(props: dict) -> dict:
    out = dict(props)
    for key in DROP_REL_PROPS:
        out.pop(key, None)
    if out.get("review_status") == "evidence_backed_pending_apply":
        out["review_status"] = "evidence_on_properties"
    return out


def url_from_belegt(rec: dict, quelle_urls: dict[str, str]) -> str | None:
    props = rec.get("properties") or {}
    if props.get("evidence_url"):
        return props["evidence_url"]
    to_id = rec.get("to")
    if to_id and to_id in quelle_urls:
        return quelle_urls[to_id]
    return None


def normalize_rows(rows: list[dict], quelle_urls: dict[str, str]) -> tuple[list[dict], dict]:
    out: list[dict] = []
    node_urls: dict[str, set[str]] = {}
    stats = {"skipped_quelle_nodes": 0, "converted_belegt_in": 0, "kept_rels": 0, "kept_other": 0}

    for rec in rows:
        if is_quelle_node(rec):
            stats["skipped_quelle_nodes"] += 1
            props = rec.get("properties") or {}
            if props.get("url"):
                quelle_urls[rec["id"]] = props["url"]
            continue

        op = rec.get("op")
        if op == "add_rel" and rec.get("type") == "BELEGT_IN":
            node_id = rec.get("from")
            url = url_from_belegt(rec, quelle_urls)
            if node_id and url:
                node_urls.setdefault(node_id, set()).add(url)
            stats["converted_belegt_in"] += 1
            continue

        if op == "add_rel":
            rec = dict(rec)
            rec["properties"] = clean_rel_props(rec.get("properties") or {})
            out.append(rec)
            stats["kept_rels"] += 1
            continue

        if op in {"add_node", "set_node_properties", "delete_rel", "set_rel_properties"}:
            out.append(rec)
            stats["kept_other"] += 1
            continue

        out.append(rec)
        stats["kept_other"] += 1

    return out, {**stats, "node_urls": node_urls}


def prepend_url_props(rows: list[dict], node_urls: dict[str, set[str]]) -> list[dict]:
    if not node_urls:
        return rows
    prepend = []
    for node_id in sorted(node_urls):
        urls = sorted(node_urls[node_id])
        prepend.append(
            {
                "id": node_id,
                "op": "set_node_properties",
                "properties": {"source_urls": urls, "primary_source_url": urls[0]},
            }
        )
    return prepend + rows


def normalize_run(run_dir: Path) -> dict:
    patches = run_dir / "patches"
    quelle_urls: dict[str, str] = {}
    dossiers: dict[str, str] = {}
    report: dict = {"run": run_dir.name, "files": {}}
    all_node_urls: dict[str, set[str]] = {}

    # Load phase0 backup URLs + dossier paths
    for path in sorted(patches.glob("phase0*.patch.jsonl")):
        src = path.with_suffix(path.suffix + ".bak") if path.with_suffix(path.suffix + ".bak").exists() else path
        for rec in load_jsonl(src):
            if not is_quelle_node(rec):
                continue
            props = rec.get("properties") or {}
            if props.get("url"):
                quelle_urls[rec["id"]] = props["url"]
            if props.get("quelltyp") == "research_markdown" and props.get("source_file"):
                dossiers[rec["id"]] = props["source_file"]

    file_rows: dict[Path, list[dict]] = {}
    for path in sorted(patches.glob("*.patch.jsonl")):
        if path.name.endswith(".bak"):
            continue
        if path.name.startswith("phase0"):
            backup = path.with_suffix(path.suffix + ".bak")
            if not backup.exists():
                shutil.copy2(path, backup)
            dump_jsonl(path, [])
            report["files"][path.name] = {"emptied_phase0": True}
            continue
        file_rows[path] = load_jsonl(path)

    for path, rows in file_rows.items():
        out, stats = normalize_rows(rows, quelle_urls)
        for nid, urls in stats.pop("node_urls").items():
            all_node_urls.setdefault(nid, set()).update(urls)
        file_rows[path] = out
        report["files"][path.name] = stats

    # Prepend URL properties to earliest semantic phase file only
    first_semantic = next(
        (p for p in sorted(file_rows) if not p.name.startswith("phase0")),
        None,
    )
    if first_semantic and all_node_urls:
        file_rows[first_semantic] = prepend_url_props(file_rows[first_semantic], all_node_urls)
        report["node_url_properties"] = {k: sorted(v) for k, v in sorted(all_node_urls.items())}

    for path, rows in file_rows.items():
        backup = path.with_suffix(path.suffix + ".bak")
        if not backup.exists():
            shutil.copy2(path, backup)
        dump_jsonl(path, rows)

    report["dossiers_off_graph"] = dossiers
    return report


def main() -> None:
    all_reports = [normalize_run(run_dir) for run_dir in RUNS]
    out = ROOT / "_neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/normalize_patch_report.json"
    out.write_text(json.dumps(all_reports, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
