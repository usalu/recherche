import csv
from pathlib import Path

ledger = Path(r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\VERIFICATION_LEDGER_ELEMENT.csv")
rows = []
with ledger.open(encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["verdict"] == "MISSING_EVIDENCE" and row["rel_type_or_label"] == "Akteur" and row["claim_kind"] == "node":
            bt, br = row.get("basis_type", ""), row.get("basis_ref", "") or ""
            if not (br.startswith("http") or bt in ("web", "candidate")):
                rows.append(row)

bad = [r for r in rows if r["element_id"].startswith("4:")]
print("total", len(rows))
print("bad element_id (neo4j id)", len(bad))
for r in bad[:5]:
    print(r["element_id"], r.get("from_id"), r.get("claim_id"), r.get("graph_element_id"))
