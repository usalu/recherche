import csv
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10000000)
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "CLICKABLE_EVIDENCE_BASELINE.csv", encoding="utf-8")))
print("total claims with URL:", len(rows))
print("\n=== by status ===")
for k, v in Counter(r["evidence_status"] for r in rows).most_common():
    print(f"  {k:20} {v}")

print("\n=== rels vs nodes ===")
for kind in ("rel", "node"):
    sub = [r for r in rows if r["kind"] == kind]
    c = Counter(r["evidence_status"] for r in sub)
    print(f"  {kind}: {len(sub)} total | VERIFIED {c['CLICKABLE_VERIFIED']} "
          f"MISMATCH {c['QUOTE_MISMATCH']} HOMEPAGE {c['HOMEPAGE_ONLY']} DEAD {c['LINK_DEAD']}")

print("\n=== rel type breakdown ===")
byt = defaultdict(Counter)
for r in rows:
    if r["kind"] == "rel":
        byt[r["type"]][r["evidence_status"]] += 1
for t, c in sorted(byt.items(), key=lambda x: -sum(x[1].values())):
    tot = sum(c.values())
    print(f"  {t:28} {c['CLICKABLE_VERIFIED']:3}/{tot:3} ok | "
          f"mismatch {c['QUOTE_MISMATCH']} home {c['HOMEPAGE_ONLY']} dead {c['LINK_DEAD']}")

print("\n=== dead links (sample) ===")
for r in [r for r in rows if r["evidence_status"] == "LINK_DEAD"][:15]:
    print(f"  [{r['http_status']}] {r['type']} {r['subject'][:28]} -> {r['url'][:60]}")

print("\n=== homepage-only domains (sample) ===")
home = Counter(r["url"] for r in rows if r["evidence_status"] == "HOMEPAGE_ONLY")
for u, n in home.most_common(12):
    print(f"  {n:3}  {u[:70]}")
