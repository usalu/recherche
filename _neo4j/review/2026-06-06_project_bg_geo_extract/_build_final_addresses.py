"""Merge address registry + web enrichment + evidence deep dive; export map-ready CSVs."""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent


def has_street_number(addr: str) -> bool:
    return bool(re.search(r"\b\d", addr))


def geocode(addr: str) -> tuple[float | None, float | None, str]:
    q = urllib.parse.quote(addr)
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "recherche-neo4j-geo-extract/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", "")
    return None, None, ""


def main() -> None:
    draft = json.loads((OUT_DIR / "address_registry_draft.json").read_text(encoding="utf-8"))
    enrichment = json.loads((OUT_DIR / "address_enrichment_web.json").read_text(encoding="utf-8"))
    deep_dive = json.loads((OUT_DIR / "evidence_deep_dive.json").read_text(encoding="utf-8"))
    coord_cache_path = OUT_DIR / "coordinate_cache.json"
    coord_cache = (
        json.loads(coord_cache_path.read_text(encoding="utf-8")) if coord_cache_path.exists() else {}
    )
    bgs = json.loads((OUT_DIR / "bauteilgruppen.json").read_text(encoding="utf-8"))
    orphan_evidence = deep_dive.get("orphan_bauteilgruppen", {})

    final_projects: list[dict] = []
    evidence_notes: list[dict] = []

    for row in draft:
        pid = row["projekt_id"]
        addr = row["address_raw"]
        source = row["address_source"]
        confidence = row["address_quality"]
        lat = lng = None
        source_url = ""
        evidence_status = ""
        notes = ""

        if pid in enrichment:
            e = enrichment[pid]
            addr = e["address"]
            source = "web:" + e.get("source_url", "")
            confidence = e.get("confidence", "medium")
            lat = e.get("latitude")
            lng = e.get("longitude")
            source_url = e.get("source_url", "")
            evidence_status = e.get("evidence_status", "")

        if pid in deep_dive.get("projects", {}):
            d = deep_dive["projects"][pid]
            addr = d["address"]
            confidence = d["confidence"]
            source_url = d["source_url"]
            source = "evidence_deep_dive:" + source_url
            evidence_status = d["evidence_status"]
            notes = d.get("notes", "")
            if lat is None or lng is None:
                lat, lng, _ = geocode(addr.split(";")[0].strip())
                time.sleep(1.1)
        elif addr:
            if has_street_number(addr) and confidence not in ("low",):
                confidence = "high" if confidence in ("verified", "verified_partial") else confidence
            elif confidence == "city_or_area_only":
                confidence = "low"

        if (lat is None or lng is None) and addr:
            lat, lng, _ = geocode(addr.split(";")[0].strip())
            time.sleep(1.1)
        if (lat is None or lng is None) and pid in coord_cache:
            lat = coord_cache[pid].get("latitude")
            lng = coord_cache[pid].get("longitude")

        final_projects.append(
            {
                "projekt_id": pid,
                "projekt_name": row["projekt_name"],
                "staedte": row["staedte"],
                "address": addr,
                "latitude": lat,
                "longitude": lng,
                "confidence": confidence,
                "evidence_status": evidence_status,
                "address_source": source,
                "source_url": source_url,
                "evidence_notes": notes,
            }
        )
        if evidence_status or notes:
            evidence_notes.append(
                {
                    "entity_type": "projekt",
                    "entity_id": pid,
                    "entity_name": row["projekt_name"],
                    "confidence": confidence,
                    "evidence_status": evidence_status,
                    "address": addr,
                    "source_url": source_url,
                    "notes": notes,
                    "action": "upgraded" if confidence == "medium" and evidence_status else "documented_no_street",
                }
            )

    (OUT_DIR / "projekte_addresses.json").write_text(
        json.dumps(final_projects, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    with (OUT_DIR / "projekte_addresses.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "projekt_id",
                "projekt_name",
                "address",
                "latitude",
                "longitude",
                "confidence",
                "evidence_status",
                "staedte",
                "source_url",
                "evidence_notes",
            ]
        )
        for p in final_projects:
            w.writerow(
                [
                    p["projekt_id"],
                    p["projekt_name"],
                    p["address"],
                    p["latitude"] or "",
                    p["longitude"] or "",
                    p["confidence"],
                    p.get("evidence_status", ""),
                    p["staedte"],
                    p["source_url"],
                    p.get("evidence_notes", ""),
                ]
            )

    proj_addr = {p["projekt_id"]: p for p in final_projects}
    bg_rows: list[dict] = []
    for b in bgs:
        bgid = b["bauteilgruppe_id"]
        pid = b["projekt_ids"][0] if b["projekt_ids"] else ""
        pname = b["projekt_names"][0] if b["projekt_names"] else ""
        pa = proj_addr.get(pid, {})

        if not pid and bgid in orphan_evidence:
            oe = orphan_evidence[bgid]
            addr = oe.get("address", "")
            conf = oe.get("confidence", "low")
            est = oe.get("evidence_status", "orphan_no_project")
            lat = lng = None
            if addr:
                lat, lng, _ = geocode(addr.split(";")[0].split(",")[0].strip())
                time.sleep(1.1)
            bg_rows.append(
                {
                    "bauteilgruppe_id": bgid,
                    "bauteilgruppe_name": b["bauteilgruppe_name"],
                    "projekt_id": "",
                    "projekt_name": "",
                    "address": addr,
                    "latitude": lat,
                    "longitude": lng,
                    "confidence": conf,
                    "evidence_status": est,
                    "linked_program": oe.get("linked_program", ""),
                    "donor_staedte": ";".join(b.get("donor_staedte") or []),
                    "receiver_staedte": ";".join(b.get("receiver_staedte") or []),
                    "source_url": oe.get("source_url", ""),
                }
            )
            evidence_notes.append(
                {
                    "entity_type": "bauteilgruppe_orphan",
                    "entity_id": bgid,
                    "entity_name": b["bauteilgruppe_name"],
                    "confidence": conf,
                    "evidence_status": est,
                    "address": addr,
                    "source_url": oe.get("source_url", ""),
                    "notes": oe.get("notes", ""),
                    "action": "orphan_evidence_only" if addr else "orphan_no_address",
                }
            )
            continue

        bg_rows.append(
            {
                "bauteilgruppe_id": bgid,
                "bauteilgruppe_name": b["bauteilgruppe_name"],
                "projekt_id": pid,
                "projekt_name": pname,
                "address": pa.get("address", ""),
                "latitude": pa.get("latitude"),
                "longitude": pa.get("longitude"),
                "confidence": pa.get("confidence", "missing") if pid else "orphan_no_project",
                "evidence_status": pa.get("evidence_status", "") if pid else "orphan_no_project",
                "linked_program": "",
                "donor_staedte": ";".join(b.get("donor_staedte") or []),
                "receiver_staedte": ";".join(b.get("receiver_staedte") or []),
                "source_url": pa.get("source_url", ""),
            }
        )

    with (OUT_DIR / "bauteilgruppe_projekt_addresses.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(bg_rows[0].keys()))
        w.writeheader()
        w.writerows(bg_rows)

    with (OUT_DIR / "evidence_notes.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "entity_type",
                "entity_id",
                "entity_name",
                "confidence",
                "evidence_status",
                "address",
                "source_url",
                "notes",
                "action",
            ],
        )
        w.writeheader()
        w.writerows(evidence_notes)

    low_projects = [p["projekt_id"] for p in final_projects if p["confidence"] == "low"]
    summary = {
        "projects_total": len(final_projects),
        "with_address": sum(1 for p in final_projects if p["address"]),
        "with_coordinates": sum(1 for p in final_projects if p["latitude"] is not None),
        "confidence_high": sum(1 for p in final_projects if p["confidence"] == "high"),
        "confidence_medium": sum(1 for p in final_projects if p["confidence"] == "medium"),
        "confidence_low": sum(1 for p in final_projects if p["confidence"] == "low"),
        "bauteilgruppen_mapped": len(bg_rows),
        "bauteilgruppen_with_address": sum(1 for b in bg_rows if b["address"]),
        "orphan_bgs": sum(1 for b in bg_rows if not b["projekt_id"]),
        "orphan_bgs_with_evidence": sum(1 for b in bg_rows if not b["projekt_id"] and b["address"]),
        "low_confidence_projects": low_projects,
        "evidence_upgrades": [
            p["projekt_id"]
            for p in final_projects
            if p.get("evidence_status") in ("plot_intersection", "multi_site_verified", "street_without_number")
        ],
    }
    (OUT_DIR / "address_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
