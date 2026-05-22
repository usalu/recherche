"""Build donor Bauwerk address registry and merge into BG export maps."""

from __future__ import annotations

import csv
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent


def geocode(addr: str) -> tuple[float | None, float | None]:
    q = urllib.parse.quote(addr)
    url = f"https://nominatim.openstreetmap.org/search?q={q}&format=json&limit=1"
    req = urllib.request.Request(url, headers={"User-Agent": "recherche-neo4j-geo-extract/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None, None


def load_processed_addresses() -> dict[str, str]:
    proc = OUT_DIR.parents[1] / "processed" / "projects" / "records"
    out: dict[str, str] = {}
    for f in proc.glob("*.kg.jsonl"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            o = json.loads(line)
            if o.get("record_type") == "node" and "Bauwerk" in o.get("labels", []):
                p = o.get("properties", {})
                if p.get("adresse"):
                    out[o["id"]] = p["adresse"]
    return out


def main() -> None:
    donors = json.loads((OUT_DIR / "donor_bauwerke_index.json").read_text(encoding="utf-8"))
    raw_links = json.loads((OUT_DIR / "donor_bauwerke_raw.json").read_text(encoding="utf-8"))
    enrichment = json.loads((OUT_DIR / "donor_address_enrichment_web.json").read_text(encoding="utf-8"))
    processed = load_processed_addresses()
    coord_cache_path = OUT_DIR / "donor_coordinate_cache.json"
    coord_cache = (
        json.loads(coord_cache_path.read_text(encoding="utf-8")) if coord_cache_path.exists() else {}
    )

    donor_rows: list[dict] = []
    for bw_id, meta in sorted(donors.items()):
        addr = ""
        confidence = "low"
        evidence_status = "not_researched"
        source_url = ""
        notes = ""

        if bw_id in enrichment:
            e = enrichment[bw_id]
            addr = e["address"]
            confidence = e.get("confidence", "low")
            evidence_status = e.get("evidence_status", "")
            source_url = e.get("source_url", "")
        elif bw_id in processed:
            addr = processed[bw_id]
            confidence = "medium"
            evidence_status = "processed_kg"
            source_url = "processed/kg.jsonl"

        if not addr and meta.get("staedte"):
            addr = f"{meta['staedte'][0]}, {meta['laender'][0] if meta.get('laender') else ''}".strip(", ")
            evidence_status = "city_fallback"
            notes = "No primary source; city from graph LIEGT_IN_STADT only."

        lat = lng = None
        if bw_id in coord_cache:
            lat = coord_cache[bw_id].get("latitude")
            lng = coord_cache[bw_id].get("longitude")
        if (lat is None or lng is None) and addr:
            lat, lng = geocode(addr.split(";")[0].split("(")[0].strip())
            time.sleep(1.1)
            if lat is not None:
                coord_cache[bw_id] = {"latitude": lat, "longitude": lng}

        donor_rows.append(
            {
                "bauwerk_id": bw_id,
                "bauwerk_name": meta["name"],
                "address": addr,
                "latitude": lat,
                "longitude": lng,
                "confidence": confidence,
                "evidence_status": evidence_status,
                "staedte": ";".join(meta.get("staedte") or []),
                "laender": ";".join(meta.get("laender") or []),
                "linked_bauteilgruppen": meta["bg_count"],
                "linked_projekte": ";".join(meta.get("projekt_ids") or []),
                "source_url": source_url,
                "notes": notes,
            }
        )

    coord_cache_path.write_text(json.dumps(coord_cache, indent=2), encoding="utf-8")
    (OUT_DIR / "donor_bauwerke_addresses.json").write_text(
        json.dumps(donor_rows, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    fields = list(donor_rows[0].keys())
    with (OUT_DIR / "donor_bauwerke_addresses.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(donor_rows)

    donor_addr = {r["bauwerk_id"]: r for r in donor_rows}

    # BG-level donor/receiver map from Neo4j AUS_SPENDER edges
    bg_donor_map: dict[str, list[str]] = {}
    for link in raw_links:
        bg_donor_map.setdefault(link["bg_id"], []).append(link["bw_id"])

    receiver_projects = json.loads((OUT_DIR / "projekte_addresses.json").read_text(encoding="utf-8"))
    recv_by_id = {p["projekt_id"]: p for p in receiver_projects}
    bgs = json.loads((OUT_DIR / "bauteilgruppen.json").read_text(encoding="utf-8"))

    chain_rows: list[dict] = []
    for b in bgs:
        bgid = b["bauteilgruppe_id"]
        pid = b["projekt_ids"][0] if b["projekt_ids"] else ""
        recv = recv_by_id.get(pid, {})
        donor_ids = bg_donor_map.get(bgid, [])
        if donor_ids:
            for did in donor_ids:
                d = donor_addr.get(did, {})
                chain_rows.append(
                    {
                        "bauteilgruppe_id": bgid,
                        "bauteilgruppe_name": b["bauteilgruppe_name"],
                        "donor_bauwerk_id": did,
                        "donor_bauwerk_name": d.get("bauwerk_name", ""),
                        "donor_address": d.get("address", ""),
                        "donor_latitude": d.get("latitude"),
                        "donor_longitude": d.get("longitude"),
                        "donor_confidence": d.get("confidence", ""),
                        "donor_evidence_status": d.get("evidence_status", ""),
                        "donor_source_url": d.get("source_url", ""),
                        "receiver_projekt_id": pid,
                        "receiver_projekt_name": recv.get("projekt_name", b["projekt_names"][0] if b["projekt_names"] else ""),
                        "receiver_address": recv.get("address", ""),
                        "receiver_latitude": recv.get("latitude"),
                        "receiver_longitude": recv.get("longitude"),
                        "receiver_confidence": recv.get("confidence", ""),
                    }
                )
        else:
            chain_rows.append(
                {
                    "bauteilgruppe_id": bgid,
                    "bauteilgruppe_name": b["bauteilgruppe_name"],
                    "donor_bauwerk_id": "",
                    "donor_bauwerk_name": "",
                    "donor_address": "",
                    "donor_latitude": None,
                    "donor_longitude": None,
                    "donor_confidence": "",
                    "donor_evidence_status": "no_donor_link",
                    "donor_source_url": "",
                    "receiver_projekt_id": pid,
                    "receiver_projekt_name": recv.get("projekt_name", ""),
                    "receiver_address": recv.get("address", ""),
                    "receiver_latitude": recv.get("latitude"),
                    "receiver_longitude": recv.get("longitude"),
                    "receiver_confidence": recv.get("confidence", ""),
                }
            )

    with (OUT_DIR / "bauteilgruppe_donor_receiver_map.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(chain_rows[0].keys()))
        w.writeheader()
        w.writerows(chain_rows)

    # Update combined BG addresses file with primary donor
    combined_path = OUT_DIR / "bauteilgruppe_projekt_addresses.csv"
    existing = list(csv.DictReader(combined_path.open(encoding="utf-8")))
    for row in existing:
        bgid = row["bauteilgruppe_id"]
        donors_for_bg = bg_donor_map.get(bgid, [])
        if donors_for_bg:
            d = donor_addr.get(donors_for_bg[0], {})
            row["donor_bauwerk_id"] = donors_for_bg[0]
            row["donor_bauwerk_name"] = d.get("bauwerk_name", "")
            row["donor_address"] = d.get("address", "")
            row["donor_latitude"] = d.get("latitude") or ""
            row["donor_longitude"] = d.get("longitude") or ""
            row["donor_confidence"] = d.get("confidence", "")
            row["donor_evidence_status"] = d.get("evidence_status", "")
            row["donor_source_url"] = d.get("source_url", "")
            if len(donors_for_bg) > 1:
                row["donor_notes"] = f"+{len(donors_for_bg)-1} more donors; see bauteilgruppe_donor_receiver_map.csv"
            else:
                row["donor_notes"] = ""
        else:
            row["donor_bauwerk_id"] = ""
            row["donor_bauwerk_name"] = ""
            row["donor_address"] = ""
            row["donor_latitude"] = ""
            row["donor_longitude"] = ""
            row["donor_confidence"] = ""
            row["donor_evidence_status"] = ""
            row["donor_source_url"] = ""
            row["donor_notes"] = ""

    extra_fields = [
        "donor_bauwerk_id",
        "donor_bauwerk_name",
        "donor_address",
        "donor_latitude",
        "donor_longitude",
        "donor_confidence",
        "donor_evidence_status",
        "donor_source_url",
        "donor_notes",
    ]
    all_fields = list(existing[0].keys())
    for ef in extra_fields:
        if ef not in all_fields:
            all_fields.append(ef)
    with combined_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=all_fields)
        w.writeheader()
        w.writerows(existing)

    summary = {
        "donor_bauwerke_total": len(donor_rows),
        "with_address": sum(1 for r in donor_rows if r["address"]),
        "with_coordinates": sum(1 for r in donor_rows if r["latitude"] is not None),
        "confidence_high": sum(1 for r in donor_rows if r["confidence"] == "high"),
        "confidence_medium": sum(1 for r in donor_rows if r["confidence"] == "medium"),
        "confidence_low": sum(1 for r in donor_rows if r["confidence"] == "low"),
        "bauteilgruppen_with_donor_link": sum(1 for r in chain_rows if r["donor_bauwerk_id"]),
        "bauteilgruppen_without_donor_link": sum(1 for r in chain_rows if not r["donor_bauwerk_id"]),
        "donor_receiver_chain_rows": len([r for r in chain_rows if r["donor_bauwerk_id"]]),
    }
    base_summary = json.loads((OUT_DIR / "address_summary.json").read_text(encoding="utf-8"))
    base_summary["donor_bauwerke"] = summary
    (OUT_DIR / "address_summary.json").write_text(json.dumps(base_summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
