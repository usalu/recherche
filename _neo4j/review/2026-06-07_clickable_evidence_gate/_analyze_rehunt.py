import csv
from collections import Counter
from pathlib import Path
csv.field_size_limit(10_000_000)
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "REHUNT_LEDGER.csv").open(encoding="utf-8")))
print("total:", len(rows))
print("result:", dict(Counter(r["result"] for r in rows)))
print("candidates_tried distribution:", dict(Counter(r["candidates_tried"] for r in rows)))
zero = [r for r in rows if r["candidates_tried"] == "0"]
print(f"claims with ZERO candidates (no source_urls + DDG empty): {len(zero)}")
print("\n=== RECOVERED ===")
for r in rows:
    if r["result"] == "RECOVERED":
        print(f"  [{r['match']}] {r['type']} {r['subject'][:28]:28} -> {r['new_url'][:60]}")
print("\n=== sample STILL_UNVERIFIED with candidates>0 ===")
n = 0
for r in rows:
    if r["result"] == "STILL_UNVERIFIED" and r["candidates_tried"] != "0":
        print(f"  cand={r['candidates_tried']} {r['type']:14} {r['subject'][:26]:26} old={r['old_url'][:45]}")
        n += 1
        if n >= 12:
            break
