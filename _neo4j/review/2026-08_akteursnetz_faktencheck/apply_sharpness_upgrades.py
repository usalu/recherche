"""One-off application of the confirmed sharpness upgrades (Round 3, item 5).

Registers each upgraded source as a NEW candidate (never overwrites an
existing one, preserving the review file's own provenance guarantee), then
repoints that node's confirmed decision at it. Read from
sharpness_saved.json (already fetched, dimension-checked, and individually
visually confirmed against the currently shipped disc -- see the Round 3
plan, item 5).
"""
import json
import shutil
import datetime as dt
from pathlib import Path

import pilot_images as pilot

BASE = Path(__file__).resolve().parent
FULL = BASE / "bilder_full"
REVIEW_PATH = FULL / "full_asset_review.json"
SC = Path(r"C:/Users/Kinosh/AppData/Local/Temp/claude/E--semio/fd4f9f8b-9f73-4e91-8356-07e8fa5f7401/scratchpad")

saved = json.load(open(SC / "sharpness_saved.json", encoding="utf-8"))
review = json.load(open(REVIEW_PATH, encoding="utf-8"))
decisions = {r["key"]: r for r in review["nodes"]}
confirmed_at = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")

applied = []
for r in saved:
    key = r["key"]
    cc, tid = key.split(":")
    cand_dir = FULL / "kandidaten" / cc / tid
    cj_path = cand_dir / "candidates.json"
    cj = json.load(open(cj_path, encoding="utf-8"))
    assert cj.get("key") == key, f"{key}: stale candidates.json"

    original = next(c for c in cj["candidates"] if c["id"] == r["candidate_id"])
    new_id = f"{r['candidate_id']}_sharp"
    assert not any(c["id"] == new_id for c in cj["candidates"]), f"{key}: {new_id} already exists"

    src_local = Path(r["local_path"])
    ext = src_local.suffix
    dest_rel = f"kandidaten/{cc}/{tid}/{new_id}_{original.get('kind','upgrade')}{ext}"
    dest_path = FULL / dest_rel
    shutil.copyfile(src_local, dest_path)
    preview_sha256 = pilot.sha256_file(dest_path)

    new_candidate = {
        "id": new_id, "priority": original.get("priority", 1), "kind": original.get("kind"),
        "url": r["resolved_url"], "status": "candidate", "review_status": "pending",
        "retrieved_at": pilot.today(), "license_note": original.get("license_note", ""),
        "source_sha256": preview_sha256, "preview_sha256": preview_sha256,
        "reason": "", "final_url": r.get("final_url", r["resolved_url"]),
        "content_type": r.get("content_type", ""), "format": ext.lstrip("."),
        "width": r["new_wh"][0], "height": r["new_wh"][1],
        "preview_path": dest_rel,
        "provenance_note": (f"Sharpness upgrade of {r['candidate_id']} ({r['pattern']} pattern): "
                            f"{r['current_wh'][0]}x{r['current_wh'][1]} -> "
                            f"{r['new_wh'][0]}x{r['new_wh'][1]} ({r['ratio']}x). "
                            "Same mark visually confirmed against the previously shipped disc."),
    }
    cj["candidates"].append(new_candidate)
    json.dump(cj, open(cj_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    d = decisions[key]
    d["candidate_id"] = new_id
    d["candidate_sha256"] = preview_sha256
    d["confirmed_at"] = confirmed_at
    d["notes"] = (d.get("notes", "") +
                 f" | Runde 3, Punkt 5: Quelle durch schärferes Original ersetzt "
                 f"({r['current_wh'][0]}x{r['current_wh'][1]} -> {r['new_wh'][0]}x{r['new_wh'][1]}), "
                 "gleiche Marke einzeln bildlich bestätigt.")
    applied.append(key)

json.dump(review, open(REVIEW_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"applied {len(applied)} sharpness upgrades: {applied}")
