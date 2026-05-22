import csv
from pathlib import Path
csv.field_size_limit(10_000_000)
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "CLICKABLE_EVIDENCE_BASELINE.csv").open(encoding="utf-8")))
rels = [r for r in rows if r["kind"] == "rel" and r["evidence_status"] in ("QUOTE_MISMATCH", "HOMEPAGE_ONLY", "LINK_DEAD")]
print("rel link failures:", len(rels))
# how many mismatches have a decent score (>=0.5) = possibly correct deep link
strong = [r for r in rels if r["evidence_status"] == "QUOTE_MISMATCH" and float(r["match_score"]) >= 0.5]
print(f"  QUOTE_MISMATCH with score>=0.5 (maybe still right page): {len(strong)}")
print("\n--- sample ---")
for r in rels[:22]:
    print(f"[{r['evidence_status'][:8]:8}|{r['match_score']}|{r['http_status']:3}] {r['type'][:16]:16} {r['subject'][:26]:26} {r['url'][:52]}")
