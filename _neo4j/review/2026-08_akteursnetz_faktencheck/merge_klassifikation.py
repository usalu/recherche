# -*- coding: utf-8 -*-
"""
Merge the returned classification tables into one machine-readable file keyed
by eid, and surface the disagreements with the fact-check.

The classifier never saw the `kern`/`bezug` grade -- it was withheld so the
classification would be an independent second opinion. This script is where
that pays off: a classifier that lands on a fallback value for an actor the
fact-check graded `kern` is a genuine flag, either

  * the fact-check grade rests on a thin or over-read quote, or
  * the cited page really does not describe an activity (only proves a name).

Neither is auto-resolved here. Both land in klassifikation_konflikte.md for a
human pass -- the same discipline the removal rules follow: compute the list,
never let a model silently decide.

Input : results/*.md            (agent output, 4-column markdown tables)
        batches/_index.json     (ID register)
        verdicts.json           (eid + grade)
Output: klassifikation.json           eid -> {rolle, rollen[], relevanz, ...}
        klassifikation_konflikte.md   review list
"""
import json, os, re, glob, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "results")
BATCHDIR = os.path.join(BASE, "batches")

FALLBACKS = {
    "Unzureichende Informationen",
    "Reuse-Bezug belegt, Rolle unklar",
    "Keine direkte Reuse-Rolle belegt",
}
UNCLEAR_PROJECT = "Referenzprojekt, Reuse-Umfang unklar"

ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$")


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def parse_results():
    rows = {}
    for path in sorted(glob.glob(os.path.join(RESULTS, "*.md"))):
        for line in open(path, encoding="utf-8"):
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            rid, name, roles, rel = (g.strip() for g in m.groups())
            if not rid or rid.upper() == "ID" or set(rid) <= set("-: "):
                continue
            rows[rid] = {"name": name, "rolle": roles, "relevanz": rel,
                          "quelle_batch": os.path.basename(path)}
    return rows


def main():
    if not os.path.isdir(RESULTS):
        sys.exit(f"Kein Ergebnisordner: {RESULTS}")

    rows = parse_results()
    idx = load(os.path.join("batches", "_index.json"))
    V = load("verdicts.json")

    # (cc,tid) -> node, to recover eid + the withheld grade
    by_key = {(n["cc"], n["tid"]): n for n in V["nodes"]}
    expected = [i for b in idx["batches"] for i in b["ids"]]

    out, konflikte, missing = {}, [], []
    fallback_count = collections.Counter()

    for rid in expected:
        r = rows.get(rid)
        if not r:
            missing.append(rid)
            continue
        cc, tid = rid.split(":", 1)
        node = by_key.get((cc, tid))
        if not node:
            konflikte.append((rid, r["name"], "-", "ID nicht in verdicts.json"))
            continue

        rollen = [x.strip() for x in r["rolle"].split("/") if x.strip()]
        grade = node.get("actor_degree")
        is_fallback = any(x in FALLBACKS for x in rollen) or r["rolle"] == UNCLEAR_PROJECT

        if is_fallback:
            fallback_count[r["rolle"]] += 1
            if grade == "kern":
                konflikte.append((rid, r["name"], grade,
                                  f"als 'kern' belegt, Klassifikation: {r['rolle']}"))
            elif grade == "bezug" and r["rolle"] == "Keine direkte Reuse-Rolle belegt":
                konflikte.append((rid, r["name"], grade,
                                  "als 'bezug' belegt, Klassifikation verneint Reuse-Bezug"))

        out[node["eid"]] = {
            "id": rid, "cc": cc, "tid": tid,
            "name": node.get("name") or r["name"],
            "rolle": r["rolle"], "rollen": rollen, "relevanz": r["relevanz"],
            "actor_degree": grade,
            "beleg_url": node.get("beleg_url", ""),
            "fallback": is_fallback,
        }

    with open(os.path.join(BASE, "klassifikation.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    lines = ["# Klassifikation — Konflikte mit der Faktenprüfung", "",
             "Die Klassifikation lief ohne Kenntnis des Reuse-Grads. Wo sie auf einen",
             "Rückfallwert fällt, obwohl die Faktenprüfung einen Beleg vergeben hat, ist",
             "eines von beidem zu dünn. Nichts davon ist automatisch geändert worden.", "",
             f"**{len(konflikte)} Fälle**", "",
             "| ID | Name | Grad | Befund |", "|---|---|---|---|"]
    for rid, name, grade, why in sorted(konflikte):
        lines.append(f"| {rid} | {name.replace('|','\\|')} | {grade} | {why} |")
    with open(os.path.join(BASE, "klassifikation_konflikte.md"), "w",
              encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")

    print(f"erwartet     : {len(expected)}")
    print(f"gemerged     : {len(out)}")
    print(f"fehlend      : {len(missing)}" + (f"  {missing[:8]}" if missing else ""))
    print(f"Rückfallwerte: {sum(fallback_count.values())}  {dict(fallback_count)}")
    print(f"Konflikte    : {len(konflikte)}  -> klassifikation_konflikte.md")
    print("geschrieben  : klassifikation.json")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
