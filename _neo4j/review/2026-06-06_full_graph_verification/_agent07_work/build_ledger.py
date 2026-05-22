#!/usr/bin/env python3
"""Agent 07 ledger builder: join 3,691 regulation/process source_url rels with per-URL verdicts."""
import json, csv, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
RELS = os.path.join(BASE, "rels_dump.json")
VERD = os.path.join(BASE, "url_verdicts.csv")
OUT = os.path.normpath(os.path.join(BASE, "..", "ledger", "agent_07.csv"))

# verdict -> (evidence_label, proposed_action)
VERDICT_MAP = {
    "PROVEN":       ("belegt",            "KEEP"),
    "PARTIAL":      ("teilweise_belegt",  "ADD_SOURCE"),
    "DEAD_LINK":    ("teilweise_belegt",  "RESOURCE"),
    "UNVERIFIABLE": ("unbelegt",          "RESOURCE"),
    "UNSUPPORTED":  ("unbelegt",          "DELETE"),
}

# load per-URL verdicts
verdicts = {}
with open(VERD, encoding="utf-8") as f:
    rdr = csv.reader(f, delimiter="|")
    header = next(rdr)
    for row in rdr:
        if not row or len(row) < 7:
            continue
        url, http_status, fetched, verdict, conf, proof_quote, note = row[:7]
        verdicts[url] = {
            "http_status": http_status, "fetched": fetched, "verdict": verdict,
            "url_conf": conf, "proof_quote": proof_quote, "note": note,
        }

with open(RELS, encoding="utf-8") as f:
    rels = json.load(f)

cols = ["claim_id","claim_kind","element_id","from_id","to_id","rel_type_or_label",
        "asserted_claim","basis_type","basis_ref","fetched","http_status","verdict",
        "confidence","proof_quote","proposed_action","agent_id","notes"]

verdict_counts = collections.Counter()
action_counts = collections.Counter()
type_counts = collections.Counter()
missing_url = 0

rows = []
for i, r in enumerate(rels, start=1):
    url = r.get("url")
    rt = r.get("rt")
    type_counts[rt] += 1
    v = verdicts.get(url)
    if v is None:
        missing_url += 1
        v = {"http_status":"", "fetched":"false", "verdict":"UNVERIFIABLE",
             "url_conf":"niedrig", "proof_quote":"", "note":"url not in verdict cache"}
    verdict = v["verdict"]
    ev_label, action = VERDICT_MAP.get(verdict, ("unbelegt","ESCALATE_HUMAN"))
    verdict_counts[verdict] += 1
    action_counts[action] += 1

    claim = (r.get("quote") or "").strip()
    rg = r.get("rechtsgrundlage")
    asserted = f"{r.get('from_name')} -{rt}-> {r.get('to_name')}"
    if rg:
        asserted += f" [Rechtsgrundlage: {rg}]"
    notes = v["note"]
    if rg:
        notes = f"rechtsgrundlage={rg}; " + notes

    rows.append({
        "claim_id": f"agent07-rel-{i:04d}",
        "claim_kind": "rel",
        "element_id": r.get("eid"),
        "from_id": r.get("from_id"),
        "to_id": r.get("to_id"),
        "rel_type_or_label": rt,
        "asserted_claim": claim or asserted,
        "basis_type": "web",
        "basis_ref": url,
        "fetched": v["fetched"],
        "http_status": v["http_status"],
        "verdict": verdict,
        "confidence": ev_label,
        "proof_quote": v["proof_quote"],
        "proposed_action": action,
        "agent_id": "07",
        "notes": notes,
    })

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, quoting=csv.QUOTE_ALL)
    w.writeheader()
    w.writerows(rows)

print(f"wrote {len(rows)} ledger rows -> {OUT}")
print(f"missing_url (not in cache): {missing_url}")
print("verdicts:", dict(verdict_counts))
print("actions:", dict(action_counts))
print("rel_types:", dict(type_counts.most_common()))
