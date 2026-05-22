"""Generate geo import patches and sidecar evidence from reuse_geo_graph.json."""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT_DIR = Path(__file__).resolve().parent
PATCHES = OUT_DIR / "patches"
SIDECAR = OUT_DIR / "sidecar"
RUN = "2026-06-06_project_bg_geo_extract"
NOW = datetime.now(timezone.utc).isoformat()


def load_json(name: str) -> dict | list:
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def is_http_url(url: str) -> bool:
    return bool(url) and url.startswith(("http://", "https://"))


def pick_bauwerk_geo(bw: dict) -> dict | None:
    geo = bw.get("geo") or {}
    donor = geo.get("donor")
    receiver = geo.get("receiver")
    if donor and donor.get("address"):
        return donor
    if receiver and receiver.get("address"):
        return receiver
    return None


def merge_source_urls(existing: list | None, url: str) -> list[str] | None:
    if not is_http_url(url):
        return None
    out: list[str] = []
    seen: set[str] = set()
    for item in list(existing or []) + [url]:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def geo_props(geo: dict, existing_urls: list | None = None) -> dict:
    props: dict = {
        "adresse": geo.get("address") or "",
        "geo_confidence": geo.get("confidence") or "",
        "geo_import_run": RUN,
        "geo_aktualisiert_am_utc": NOW,
    }
    lat = geo.get("latitude")
    lng = geo.get("longitude")
    if lat is not None:
        props["latitude"] = lat
    if lng is not None:
        props["longitude"] = lng
    merged = merge_source_urls(existing_urls, geo.get("source_url") or "")
    if merged:
        props["source_urls"] = merged
    return props


def sidecar_row(
    entity_kind: str,
    node_id: str,
    labels: list[str],
    geo: dict,
    name: str = "",
) -> dict:
    key = f"node:{node_id}"
    return {
        "sidecar_key": key,
        "entity_kind": entity_kind,
        "node_id": node_id,
        "labels": labels,
        "name": name,
        "export_run": RUN,
        "exported_at_utc": NOW,
        "geo_evidence": {
            "address": geo.get("address") or "",
            "confidence": geo.get("confidence") or "",
            "evidence_status": geo.get("evidence_status") or "",
            "source_url": geo.get("source_url") or "",
            "role": geo.get("role") or "",
            "latitude": geo.get("latitude"),
            "longitude": geo.get("longitude"),
        },
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def graph_ids(session, label: str, ids: list[str]) -> set[str]:
    found: set[str] = set()
    for i in range(0, len(ids), 100):
        chunk = ids[i : i + 100]
        for row in session.run(
            f"MATCH (n:{label}) WHERE n.id IN $ids RETURN n.id AS id",
            ids=chunk,
        ):
            found.add(row["id"])
    return found


def source_urls_index(session, label: str, ids: list[str]) -> dict[str, list]:
    out: dict[str, list] = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i : i + 100]
        for row in session.run(
            f"MATCH (n:{label}) WHERE n.id IN $ids RETURN n.id AS id, n.source_urls AS urls",
            ids=chunk,
        ):
            out[row["id"]] = list(row["urls"] or [])
    return out


def main() -> None:
    unified = load_json("reuse_geo_graph.json")
    staedte = load_json("staedte_geocoded.json")
    pre_apply = load_json("pre_apply_report.json")

    apply_projekt = set(pre_apply["projekte"]["apply"])
    apply_bauwerk = set(pre_apply["bauwerke"]["apply"])

    phase1: list[dict] = []
    phase2: list[dict] = []
    phase3: list[dict] = []
    sidecar_rows: list[dict] = []

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    stadt_ids = [s["stadt_id"] for s in staedte]
    with driver.session(database=database) as session:
        stadt_in_graph = graph_ids(session, "Stadt", stadt_ids)
        projekt_urls = source_urls_index(session, "Projekt", list(apply_projekt))
        bauwerk_urls = source_urls_index(session, "Bauwerk", list(apply_bauwerk))
    driver.close()

    for p in unified["nodes"]["projekte"]:
        pid = p["id"]
        if pid not in apply_projekt:
            continue
        geo = p.get("geo") or {}
        if not geo.get("address"):
            continue
        props = geo_props(geo, projekt_urls.get(pid))
        props["metadata_sidecar_key"] = f"node:{pid}"
        phase1.append(
            {
                "op": "set_node_properties",
                "id": pid,
                "properties": props,
                "reason": "evidence-backed receiver site",
            }
        )
        sidecar_rows.append(
            sidecar_row("node", pid, ["Projekt"], geo, p.get("name", ""))
        )

    for bw in unified["nodes"]["bauwerke"]:
        bid = bw["id"]
        if bid not in apply_bauwerk:
            continue
        geo = pick_bauwerk_geo(bw)
        if not geo or not geo.get("address"):
            continue
        props = geo_props(geo, bauwerk_urls.get(bid))
        props["metadata_sidecar_key"] = f"node:{bid}"
        phase2.append(
            {
                "op": "set_node_properties",
                "id": bid,
                "properties": props,
                "reason": f"evidence-backed bauwerk geo ({geo.get('role', '')})",
            }
        )
        sidecar_rows.append(
            sidecar_row("node", bid, ["Bauwerk"], geo, bw.get("name", ""))
        )

    for s in staedte:
        sid = s["stadt_id"]
        if sid not in stadt_in_graph:
            continue
        lat, lng = s.get("lat"), s.get("lng")
        if lat is None or lng is None:
            continue
        phase3.append(
            {
                "op": "set_node_properties",
                "id": sid,
                "properties": {
                    "latitude": lat,
                    "longitude": lng,
                    "geo_import_run": RUN,
                    "geo_aktualisiert_am_utc": NOW,
                },
                "reason": f"city centroid ({s.get('source', 'nominatim')})",
            }
        )

    PATCHES.mkdir(parents=True, exist_ok=True)
    write_jsonl(PATCHES / "phase1_projekte_geo.patch.jsonl", phase1)
    write_jsonl(PATCHES / "phase2_bauwerke_geo.patch.jsonl", phase2)
    write_jsonl(PATCHES / "phase3_staedte_geo.patch.jsonl", phase3)

    # Phase 4 from NEW_DONOR_CANDIDATES.csv (accepted rows only)
    phase4: list[dict] = []
    candidates_path = OUT_DIR / "NEW_DONOR_CANDIDATES.csv"
    if candidates_path.is_file():
        with candidates_path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                if row.get("status", "").strip().lower() != "accepted":
                    continue
                bw_id = row["bauwerk_id"].strip()
                bg_id = row["bauteilgruppe_id"].strip()
                props = {
                    "id": bw_id,
                    "name": row["bauwerk_name"].strip(),
                    "adresse": row["address"].strip(),
                    "geo_confidence": row.get("confidence", "").strip(),
                    "geo_import_run": RUN,
                    "geo_aktualisiert_am_utc": NOW,
                }
                if row.get("latitude", "").strip():
                    props["latitude"] = float(row["latitude"])
                if row.get("longitude", "").strip():
                    props["longitude"] = float(row["longitude"])
                url = row.get("source_url", "").strip()
                if is_http_url(url):
                    props["source_urls"] = [url]
                phase4.append(
                    {
                        "op": "add_node",
                        "id": bw_id,
                        "labels": ["Bauwerk"],
                        "properties": props,
                        "reason": row.get("reason", "new donor bauwerk from geo research"),
                    }
                )
                rel_id = f"r_{bg_id}__aus_spender__{bw_id}"
                phase4.append(
                    {
                        "op": "add_rel",
                        "from": bg_id,
                        "to": bw_id,
                        "type": "AUS_SPENDER",
                        "properties": {
                            "id": rel_id,
                            "geo_import_run": RUN,
                            "evidence_confidence": row.get("confidence", ""),
                            "evidence_url": url if is_http_url(url) else "",
                        },
                        "reason": "link new donor to bauteilgruppe",
                    }
                )
                stadt_id = row.get("stadt_id", "").strip()
                if stadt_id:
                    phase4.append(
                        {
                            "op": "add_rel",
                            "from": bw_id,
                            "to": stadt_id,
                            "type": "LIEGT_IN_STADT",
                            "properties": {"geo_import_run": RUN},
                            "reason": "donor city link",
                        }
                    )
    write_jsonl(PATCHES / "phase4_new_donor_bauwerke.patch.jsonl", phase4)

    SIDECAR.mkdir(parents=True, exist_ok=True)
    write_jsonl(SIDECAR / "geo_evidence.jsonl", sidecar_rows)
    manifest = {
        "run": RUN,
        "generated_at_utc": NOW,
        "files": ["geo_evidence.jsonl"],
        "entity_count": len(sidecar_rows),
    }
    (SIDECAR / "manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (SIDECAR / "README.md").write_text(
        "# Geo evidence sidecar\n\n"
        "Off-graph geo QA: `evidence_status`, `source_url`, `role`, notes.\n"
        "Graph pointer: `metadata_sidecar_key` on Projekt/Bauwerk nodes.\n",
        encoding="utf-8",
    )

    stats = {
        "phase1_projekte": len(phase1),
        "phase2_bauwerke": len(phase2),
        "phase3_staedte": len(phase3),
        "phase4_new_donors": len([r for r in phase4 if r["op"] == "add_node"]),
        "sidecar_rows": len(sidecar_rows),
    }
    (OUT_DIR / "patch_generation_report.json").write_text(
        json.dumps(stats, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
