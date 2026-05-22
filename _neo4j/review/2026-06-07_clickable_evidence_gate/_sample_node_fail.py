import csv
from pathlib import Path
csv.field_size_limit(10_000_000)
HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader((HERE / "CLICKABLE_EVIDENCE_BASELINE.csv").open(encoding="utf-8")))
nodes = [r for r in rows if r["kind"] == "node" and r["evidence_status"] in ("QUOTE_MISMATCH", "HOMEPAGE_ONLY")]
print("node link failures:", len(nodes))
for r in nodes[:25]:
    print(f"[{r['evidence_status'][:8]:8}|{r['match_score']}] {r['subject'][:30]:30} {r['url'][:62]}")
