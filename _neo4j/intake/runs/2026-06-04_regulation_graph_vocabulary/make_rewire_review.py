# coding: utf-8
"""Render REWIRE_REVIEW.md (human sign-off) from rewire_map.csv + Regelwerk evidence."""
import csv
from collections import defaultdict, Counter
from build_vocabulary_graph import REGELWERK, NACHWEISFORDERUNG, REGULIERUNGSFRAGE

RW = {rw["id"]: rw for rw in REGELWERK}
NAME = {**{rw["id"]: rw["name"] for rw in REGELWERK}, **NACHWEISFORDERUNG, **REGULIERUNGSFRAGE}
rows = list(csv.DictReader(open("rewire_map.csv", encoding="utf-8")))
by = defaultdict(list)
for r in rows:
    by[r["old_label"]].append(r)

def nm(t):
    return NAME.get(t, t)

L = ["# REWIRE REVIEW — old labels → new evidenced vocabulary\n",
     "Semantic mapping first (what each old node *means* in the new model), evidence second "
     "(the target Regelwerk's source URL backs it). One row per old node lives in `rewire_map.csv`.\n",
     f"**{len(rows)} old nodes mapped.** Action summary:\n"]
tot = Counter(r["action"] for r in rows)
L.append("| Action | n |")
L.append("|---|--:|")
for a, c in tot.most_common():
    L.append(f"| {a} | {c} |")

# Norm: collapse to target counts
L.append("\n## Norm (103) → Regelwerk  · REPLACE & delete label\n")
L.append("103 Norm nodes (heavy duplication) collapse onto evidenced Regelwerke. Targets:\n")
norm_t = Counter(r["new_target"] for r in by["Norm"])
L.append("| → Regelwerk target | # Norm nodes | evidence |")
L.append("|---|--:|---|")
for t, c in norm_t.most_common():
    url = RW[t]["url"] if t in RW else "— (gap, see §Gaps)"
    L.append(f"| {nm(t)} | {c} | {url} |")

def full_table(lbl, title, note):
    L.append(f"\n## {title}\n{note}\n")
    L.append("| old node | → new target | evidence |")
    L.append("|---|---|---|")
    for r in sorted(by[lbl], key=lambda x: x["old_id"]):
        tgt = " + ".join(nm(t) for t in r["new_target"].split("|"))
        url = r["evidence_url"] or "—"
        L.append(f"| `{r['old_id']}` | {tgt} | {url} |")

full_table("Schadstoff", "Schadstoff (13) → Nachweisforderung + Regelwerk · KEEP",
           "Real pollutant entities kept; wired to their check (Nachweisforderung) and law (Regelwerk).")
full_table("Bauproduktstatus", "Bauproduktstatus (15) → Regelwerk / enum · REWIRE",
           "Conformity routes → Regelwerk; 3 generic statuses kept as enum; US/JP out of scope.")
full_table("RechtlicheBedingung", "RechtlicheBedingung (16) → Regelwerk / Frage · REWIRE & delete label",
           "Legal conditions map to a Regelwerk or a Genehmigung/Haftung question.")

# PruefungNachweis & Leistungsanforderung: collapse to target nf
for lbl, title, note in [
    ("PruefungNachweis", "PruefungNachweis (120) → Nachweisforderung · KEEP as method layer",
     "Concrete test *methods* hung under the proof category via `ERFUELLT_NACHWEIS` (dedup pn_/pr_ pairs)."),
    ("Leistungsanforderung", "Leistungsanforderung (46) → Nachweis/Frage · REWIRE (slim)",
     "Performance requirements mapped to the proof that demonstrates them."),
]:
    L.append(f"\n## {title}\n{note}\n")
    tc = Counter(r["new_target"] for r in by[lbl])
    L.append("| → target Nachweisforderung | # nodes |")
    L.append("|---|--:|")
    for t, c in tc.most_common():
        L.append(f"| {nm(t)} | {c} |")

# Huerde
L.append("\n## Huerde (28) → SPLIT\n")
keep = [r["old_id"] for r in by["Huerde"] if r["action"].startswith("KEEP")]
drop = [r["old_id"] for r in by["Huerde"] if r["action"].startswith("DELETE")]
L.append(f"**KEEP ({len(keep)} market/logistics barriers — distinct axis, not regulatory):** " + ", ".join(keep))
L.append(f"\n**DELETE ({len(drop)} regulatory barriers — now covered by evidenced Frage/Nachweis):** " + ", ".join(drop))

# Gaps
L.append("\n## Gaps / needs your decision (8)\n")
gaps = [r for r in rows if "GAP" in r["new_target"] or "OUT_OF_SCOPE" in r["new_target"]]
L.append("| old node | issue | suggestion |")
L.append("|---|---|---|")
sugg = {"GAP_nl_beton_reuse": "fold to DAfStb R-Beton, or research CROW-CUR 4:2023 (NL)",
        "GAP_ch_barrierefrei": "fold to DIN 18040 (DE analog) or drop", "GAP_ch_baupg": "research Swiss BauPG (1 new Regelwerk)",
        "OUT_OF_SCOPE_usa": "no EU relevance → delete", "OUT_OF_SCOPE_jp": "no EU relevance → delete"}
for r in gaps:
    L.append(f"| `{r['old_id']}` ({r['old_label']}) | {r['new_target']} | {sugg.get(r['new_target'],'review')} |")

L.append("\n## Net result\n")
L.append("- **Delete labels:** `Norm`, `RechtlicheBedingung` (fully rewired to Regelwerk/Frage).")
L.append("- **Mostly delete:** `Bauproduktstatus` (12 → Regelwerk; keep 3 status enums).")
L.append("- **Keep + rewire:** `Schadstoff` (wired to checks/laws), `PruefungNachweis` (method layer under Nachweis), "
         "`Leistungsanforderung` (slim), `Huerde` (11 market barriers only).")
L.append("- **One evidenced law layer** (`Regelwerk`, 90) replaces the 4 overlapping old ones.")
L.append("\n*Next:* on approval I build the migration (idempotent: create rewired edges with evidence, "
         "then delete replaced nodes/edges) as a separate `review_run`, with rollback + a re-audit.")

open("REWIRE_REVIEW.md", "w", encoding="utf-8").write("\n".join(L))
print("wrote REWIRE_REVIEW.md")
