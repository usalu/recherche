import json
from pathlib import Path

donors = json.loads(
    Path(__file__).resolve().parent.joinpath("donor_bauwerke_index.json").read_text(encoding="utf-8")
)
for k in sorted(donors):
    v = donors[k]
    print(f"{k}\t{v['name']}\t{','.join(v['staedte'])}\t{v['bg_count']}")
