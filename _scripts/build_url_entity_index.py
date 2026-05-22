"""Build a url->entity index from processed records and classify live orphans.

Round 2, Phase G/H groundwork. The orphaned source nodes (degree-0 Quelle /
ExternalLink) carry real URLs but lost the provenance that said which entity they
support. That provenance still lives in the processed source-of-truth records
(`_neo4j/processed/**/*.kg.jsonl`) as `external_sources` arrays on the case /
actor markdown Quelle nodes, plus direct `url` properties.

This tool (read-only w.r.t. the DB):
  1. Indexes every URL found in processed records -> the anchor Quelle node that
     owns it (the case/actor markdown the URL belongs to).
  2. Pulls every live orphan source node (degree 0) and every connected Quelle URL.
  3. Classifies each orphan:
       - duplicate_of_connected : same normalized URL already on a connected Quelle
       - reconnectable          : URL maps to an anchor Quelle that exists & is
                                   connected in the live graph
       - unrecoverable          : URL not found in processed records
  4. Emits a report + a reconnection patch (add_rel HAS_SOURCE_LINK from the
     anchor case Quelle to the orphan source) for review/apply.

Outputs under --out-dir.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402

URL_RE = re.compile(r"https?://[^\s\]\)\"'<>]+", re.IGNORECASE)
_TRACK = re.compile(r"^(utm_|fbclid$|gclid$)", re.IGNORECASE)


def normalize_url(url: str) -> str:
    if not url:
        return ""
    u = url.strip().strip(".,;")
    u = u.split("#", 1)[0]
    m = re.match(r"^(https?)://([^/]+)(.*)$", u, re.IGNORECASE)
    if not m:
        return u.rstrip("/").lower()
    scheme, host, rest = m.group(1).lower(), m.group(2).lower(), m.group(3)
    host = re.sub(r":(80|443)$", "", host)
    if host.startswith("www."):
        host = host[4:]
    path, _, query = rest.partition("?")
    if query:
        kept = [
            kv for kv in query.split("&")
            if kv and not _TRACK.match(kv.split("=", 1)[0])
        ]
        rest = path + ("?" + "&".join(kept) if kept else "")
    else:
        rest = path
    rest = rest.rstrip("/")
    return f"{scheme}://{host}{rest}"


def iter_processed_nodes(root: Path):
    for path in sorted(root.glob("**/*.kg.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("record_type") != "node":
                continue
            yield path, rec


def build_index(root: Path) -> dict:
    # norm_url -> {"anchors": set(node_id), "owners": set(node_id)}
    index: dict[str, dict] = defaultdict(lambda: {"anchors": set(), "owners": set()})
    for _path, rec in iter_processed_nodes(root):
        node_id = rec.get("id")
        props = rec.get("properties") or {}
        ext = props.get("external_sources")
        if isinstance(ext, list):
            for entry in ext:
                for url in URL_RE.findall(str(entry)):
                    n = normalize_url(url)
                    if n:
                        index[n]["anchors"].add(node_id)
        url = props.get("url")
        if isinstance(url, str) and url.startswith("http"):
            n = normalize_url(url)
            if n:
                index[n]["owners"].add(node_id)
    return index


def fetch_live(session) -> dict:
    orphans = list(
        session.run(
            "MATCH (n) WHERE NOT (n)--() AND (n:Quelle OR n:ExternalLink) "
            "RETURN n.id AS id, n.url AS url, n.quelltyp AS quelltyp, "
            "n.source_file AS source_file"
        )
    )
    connected_urls = {
        normalize_url(r["url"]): r["id"]
        for r in session.run(
            "MATCH (q:Quelle) WHERE q.url IS NOT NULL AND EXISTS { (q)--() } "
            "RETURN q.id AS id, q.url AS url"
        )
        if r["url"]
    }
    existing_anchor_ids = {
        r["id"]
        for r in session.run(
            "MATCH (q:Quelle) WHERE EXISTS { (q)--() } RETURN q.id AS id"
        )
    }
    return {
        "orphans": [dict(r) for r in orphans],
        "connected_urls": connected_urls,
        "connected_anchor_ids": existing_anchor_ids,
    }


def run(out_dir: Path) -> dict:
    from neo4j import GraphDatabase

    processed_root = repo_root() / "_neo4j" / "processed"
    index = build_index(processed_root)

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            live = fetch_live(session)
    finally:
        driver.close()

    connected_urls = live["connected_urls"]
    anchor_ids = live["connected_anchor_ids"]

    classified = {"duplicate_of_connected": [], "reconnectable": [], "unrecoverable": []}
    patch_lines: list[dict] = []
    for o in live["orphans"]:
        nurl = normalize_url(o.get("url") or "")
        rec = {"id": o["id"], "url": o.get("url"), "norm": nurl, "quelltyp": o.get("quelltyp")}
        if nurl and nurl in connected_urls:
            rec["duplicate_target"] = connected_urls[nurl]
            classified["duplicate_of_connected"].append(rec)
            continue
        hit = index.get(nurl) if nurl else None
        anchors = sorted((hit["anchors"] if hit else set()) & anchor_ids)
        if anchors:
            anchor = anchors[0]
            rec["anchor"] = anchor
            rec["all_anchors"] = anchors
            classified["reconnectable"].append(rec)
            patch_lines.append({
                "op": "add_rel",
                "from": anchor,
                "type": "HAS_SOURCE_LINK",
                "to": o["id"],
                "properties": {"id": f"r_{anchor}__HAS_SOURCE_LINK__{o['id']}"},
            })
        else:
            classified["unrecoverable"].append(rec)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "url_entity_index.json").write_text(
        json.dumps(
            {k: {"anchors": sorted(v["anchors"]), "owners": sorted(v["owners"])}
             for k, v in sorted(index.items())},
            ensure_ascii=False, indent=2,
        ) + "\n",
        encoding="utf-8",
    )
    (out_dir / "orphan_classification.json").write_text(
        json.dumps(classified, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    patch_path = out_dir / "reconnect_sources.patch.jsonl"
    with patch_path.open("w", encoding="utf-8", newline="\n") as f:
        for line in patch_lines:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    summary = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "indexed_urls": len(index),
        "orphans_total": len(live["orphans"]),
        "duplicate_of_connected": len(classified["duplicate_of_connected"]),
        "reconnectable": len(classified["reconnectable"]),
        "unrecoverable": len(classified["unrecoverable"]),
        "reconnect_patch_lines": len(patch_lines),
    }
    (out_dir / "SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or (
        repo_root() / "_neo4j" / "review" / "2026-06-01_source_reconnection"
    )
    summary = run(out_dir)
    print(json.dumps(summary, indent=2))
    print(f"\nWrote reconnection analysis to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
