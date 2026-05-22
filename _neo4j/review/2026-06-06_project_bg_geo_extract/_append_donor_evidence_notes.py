import csv
import json
from pathlib import Path

out = Path(__file__).resolve().parent
donors = json.loads((out / "donor_bauwerke_addresses.json").read_text(encoding="utf-8"))
notes_path = out / "evidence_notes.csv"
existing = list(csv.DictReader(notes_path.open(encoding="utf-8")))
for d in donors:
    existing.append(
        {
            "entity_type": "donor_bauwerk",
            "entity_id": d["bauwerk_id"],
            "entity_name": d["bauwerk_name"],
            "confidence": d["confidence"],
            "evidence_status": d["evidence_status"],
            "address": d["address"],
            "source_url": d["source_url"],
            "notes": d.get("notes", "") or f"linked to {d['linked_bauteilgruppen']} Bauteilgruppen",
            "action": "donor_address_researched" if d["confidence"] != "low" else "donor_city_or_pool_only",
        }
    )
with notes_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=existing[0].keys())
    w.writeheader()
    w.writerows(existing)
print(len(existing))
