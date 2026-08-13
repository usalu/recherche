# -*- coding: utf-8 -*-
"""
Emit the {{AKTEURSDATEN}} input blocks for the role/relevance classification
prompt, batched by country.

Scope is the DRAWN network only -- the same 859 nodes the figures and tables
show, obtained by calling netz's own build_network() with the fact-check prune
lists applied. Nothing that was already deleted is classified.

Deliberately NOT passed to the classifier:
  * `begruendung` -- our own crawler narration ("Seite gesperrt", "403
    Bot-Block"). It describes the research, not the actor. Leaking it into the
    classifier is the exact bug that once produced "Seite gesperrt" as a
    printed table cell.
  * `actor_degree` (kern/bezug) -- withheld on purpose so the classification is
    an INDEPENDENT second opinion. Comparing it against the grade afterwards is
    a signal (see merge step); pre-showing it would just anchor the answer.

Output: batches/klass_<CC>_b<N>.md, each a ready-to-paste {{AKTEURSDATEN}} block.
"""
import json, os, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
NETZ = r"E:/recherche/_neo4j/netz"
OUTDIR = os.path.join(BASE, "batches")
BATCH_SIZE = 20          # actors per agent call; each needs >=1 live page fetch

sys.path.insert(0, NETZ)
from netz.sources import DEFAULT                      # noqa: E402
from netz.data.prune import load_prune, load_edge_exclude   # noqa: E402
from netz.model.concepts import build_network          # noqa: E402


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def drawn_network():
    exclude = load_prune(DEFAULT.prune_path) | load_prune(DEFAULT.prune_faktencheck_path)
    edge_exclude = load_edge_exclude(DEFAULT.unklar_edges_path)
    return build_network(DEFAULT, exclude=exclude, edge_exclude=edge_exclude)


def block(rec):
    """One actor as a labelled input block. Field names are German because the
    prompt around them is German -- keep them stable, the parser keys on ID."""
    L = [f"### {rec['id']}",
         f"- Name: {rec['name']}",
         f"- Land: {rec['cc']}"]
    if rec["typ"]:
        L.append(f"- Typ (Altdaten, unbestaetigt): {rec['typ']}")
    if rec["is_project"]:
        L.append("- Eintragsart: BAUVORHABEN/OBJEKT (keine Organisation) -- siehe Regel P")
    L.append(f"- Beleg-URL (MUSS geoeffnet werden): {rec['beleg_url']}")
    if rec["source_urls"]:
        for u in rec["source_urls"][:3]:
            if u and u != rec["beleg_url"]:
                L.append(f"- Weitere URL: {u}")
    if rec["rollen"]:
        L.append(f"- Alt-Rollen (Altdaten, NICHT als Beleg verwenden): {' / '.join(rec['rollen'])}")
    z = (rec["zitat"] or "").replace("\n", " ").strip()
    L.append(f"- Gespeichertes Belegzitat (Nachweis-Schnipsel, KEINE Taetigkeitsbeschreibung): \"{z}\"")
    return "\n".join(L)


def main():
    net = drawn_network()
    V = load("verdicts.json")
    W = load("worklist.json")

    vn = {n["eid"]: n for n in V["nodes"] if n.get("eid")}
    wn = {}
    for pkt in W["packets"]:
        for n in pkt.get("nodes", []):
            wn[n["eid"]] = n

    drawn = set()
    for cc, pan in net.panels.items():
        drawn |= set(pan.actors) | set(pan.projects)

    by_cc = collections.defaultdict(list)
    missing = []
    for eid in drawn:
        v = vn.get(eid)
        if not v:
            missing.append(eid)
            continue
        w = wn.get(eid, {})
        cc = v["cc"]
        by_cc[cc].append({
            "id": f"{cc}:{v['tid']}",
            "eid": eid,
            "cc": cc,
            "name": v.get("name") or w.get("name") or v["tid"],
            "typ": w.get("typ"),
            "is_project": bool(w.get("is_project")),
            "beleg_url": v.get("beleg_url", ""),
            "source_urls": w.get("source_urls") or [],
            "rollen": w.get("rollen") or [],
            "zitat": v.get("beleg_zitat", ""),
        })
    if missing:
        print(f"  ! {len(missing)} drawn nodes without a verdict -- NOT classified: {missing[:5]}")

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        if f.startswith("klass_") and f.endswith(".md"):
            os.remove(os.path.join(OUTDIR, f))

    total, nbatch, index = 0, 0, []
    for cc in sorted(by_cc):
        recs = sorted(by_cc[cc], key=lambda r: r["name"].lower())
        for i in range(0, len(recs), BATCH_SIZE):
            chunk = recs[i:i + BATCH_SIZE]
            nbatch += 1
            total += len(chunk)
            name = f"klass_{cc}_b{i // BATCH_SIZE + 1}.md"
            with open(os.path.join(OUTDIR, name), "w", encoding="utf-8", newline="\n") as f:
                f.write("\n\n".join(block(r) for r in chunk) + "\n")
            index.append({"batch": name, "cc": cc, "n": len(chunk),
                          "ids": [r["id"] for r in chunk]})

    with open(os.path.join(OUTDIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump({"batch_size": BATCH_SIZE, "total_actors": total,
                   "batches": index}, f, indent=2, ensure_ascii=False)

    proj = sum(1 for cc in by_cc for r in by_cc[cc] if r["is_project"])
    print(f"actors written : {total}   (davon {proj} Bauvorhaben/Objekte)")
    print(f"batches        : {nbatch}  (<= {BATCH_SIZE} Akteure je Batch)")
    print(f"per country    : {dict(sorted((c, len(v)) for c, v in by_cc.items()))}")
    print(f"written to     : {OUTDIR}")


if __name__ == "__main__":
    main()
