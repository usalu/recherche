# -*- coding: utf-8 -*-
"""
Emit the {{KANTENDATEN}} input blocks for the relationship classification,
batched by country.

Scope is the DRAWN edges only -- the 570 the figures actually show, taken from
netz's own build_network() with the fact-check prune lists applied. The 88
`unklar` edges are already excluded there and are not classified again.

Two things this pass has to carry that the actor pass did not:

  * Edge kind. An actor-to-building edge asks "what did this actor contribute
    to this project"; an actor-to-actor edge asks "what is the organisational
    tie". Different vocabularies, so the kind is stated per block.
  * Coverage. Only 445 of the 570 drawn edges were ever graded. The other 125
    entered the drawing from a database relation or a research overlay and
    carry no source at all -- they are marked UNGEPRUEFT and need research from
    scratch. 63 of them hang off directory hubs (Opalis, bauteilnetz, SalvoWEB,
    Bolius, byggogbevar), which the project rules exclude as relationships.

Deliberately NOT passed to the classifier:
  * `edge_degree` (belegt/teilweise_belegt) -- withheld so the classification is
    an independent second opinion, same as the grade was for the actor pass.

Output: kanten_batches/kanten_<CC>_b<N>.md + _index.json
"""
import json, os, sys, collections, hashlib
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
NETZ = r"E:/recherche/_neo4j/netz"
OUTDIR = os.path.join(BASE, "kanten_batches")
BATCH_SIZE = 20
REVIEW_RUN = "2026-08_akteursnetz_faktencheck_kanten"
NODE_KIND_OVERRIDES = "kanten_node_kind_overrides.json"
EVIDENCE_REPLACEMENTS = "kanten_evidence_replacements.json"

sys.path.insert(0, NETZ)
from netz.sources import DEFAULT                              # noqa: E402
from netz.data.prune import load_prune, load_edge_exclude      # noqa: E402
from netz.model.concepts import build_network                  # noqa: E402

TYP_KURZ = {
    "Unternehmen": "Unternehmen", "Materialhub_Bauteilboerse": "Materialhub/Bauteilbörse",
    "Forschung_Lehre": "Forschung/Lehre", "NGO_Verband_Netzwerk": "NGO/Verband/Netzwerk",
    "Oeffentliche_Institution": "Öffentliche Institution",
    "Software_Tool_Anbieter": "Software/Tool-Anbieter", "Organisation": "Organisation",
    "Foerdergeber_Programmtraeger": "Förderträger",
}


def load(name):
    with open(os.path.join(BASE, name), encoding="utf-8") as f:
        return json.load(f)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_record(path):
    repo = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
    return {
        "path": os.path.relpath(path, repo).replace("\\", "/"),
        "sha256": sha256(path),
        "bytes": os.path.getsize(path),
    }


def label(n):
    if not n:
        return "?"
    if n.get("is_project"):
        return f"{n.get('name','?')}  [Bauvorhaben/Objekt]"
    t = TYP_KURZ.get(n.get("typ"))
    return f"{n.get('name','?')}" + (f"  [{t}]" if t else "")


def block(rec):
    L = [f"### {rec['id']}",
         f"- Kantenart: {rec['kind']}",
         f"- Knoten A: {rec['a_label']}",
         f"- Knoten B: {rec['b_label']}",
         f"- Land: {rec['cc']}",
         f"- Belegstatus: {rec['status']}"]
    if rec["status"] == "GEPRUEFT":
        L.append(f"- Beleg-URL (MUSS geoeffnet werden): {rec['beleg_url']}")
    else:
        L.append("- Keine gespeicherte Quelle -- aktiv recherchieren, gefundene URL in Spalte 'Beleg'")
    if rec["relation_ist"]:
        L.append(f"- Bisherige Beschreibung (Altdaten, nur Hinweis): {rec['relation_ist']}")
    if rec["zitat"]:
        z = rec["zitat"].replace("\n", " ").strip()
        L.append(f"- Gespeichertes Belegzitat (Nachweis-Schnipsel): \"{z}\"")
    return "\n".join(L)


def main():
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print(__doc__)
        return 0
    exclude = load_prune(DEFAULT.prune_path) | load_prune(DEFAULT.prune_faktencheck_path)
    net = build_network(DEFAULT, exclude=exclude,
                        edge_exclude=load_edge_exclude(DEFAULT.unklar_edges_path))

    V, W = load("verdicts.json"), load("worklist.json")
    evidence_replacements = load(EVIDENCE_REPLACEMENTS)
    override_rows = load(NODE_KIND_OVERRIDES).get("overrides", [])
    overrides = {row["eid"]: row for row in override_rows}
    if len(overrides) != len(override_rows):
        print("ABBRUCH: doppelte eid in kanten_node_kind_overrides.json")
        return 1
    key2eid = {}
    for pkt in W["packets"]:
        for n in pkt.get("nodes", []):
            key2eid[(pkt["cc"], n["tid"])] = n["eid"]

    # Node kind/name/country come from the freshly built network, not from the
    # older fact-check worklist. The worklist is only a verdict-ID bridge.
    eid2n = {}
    for eid, node in net.raw.by.items():
        if eid not in net.aset and eid not in net.res.proj_cc:
            continue
        override = overrides.get(eid, {})
        eid2n[eid] = {
            "eid": eid,
            "name": node.get("properties", {}).get("name", "?"),
            "typ": override.get("typ", net.raw.types.get(eid)),
            "is_project": override.get("is_project", eid in net.res.proj_cc),
            "cc": net.res.proj_cc.get(eid) or net.res.cc.get(eid),
        }

    graded = {}
    for e in V["edges"]:
        a = key2eid.get((e["cc"], e["a_tid"]))
        b = key2eid.get((e["cc"], e["b_tid"]))
        if a and b:
            graded[tuple(sorted((a, b)))] = e

    by_cc = collections.defaultdict(list)
    seq = collections.Counter()
    kind_errors = []
    for pair in sorted({tuple(sorted(k)) for k in net.drawn}):
        a, b = pair
        na, nb = eid2n.get(a, {}), eid2n.get(b, {})
        if not na or not nb:
            kind_errors.append(f"fehlende Knotenmetadaten: {a} | {b}")
            continue
        cc = na.get("cc") or nb.get("cc") or "??"
        g = graded.get(pair)
        project_count = sum(bool(n.get("is_project")) for n in (na, nb))
        if project_count > 1:
            kind_errors.append(
                f"Projekt-Projekt-Kante ohne Vokabular: {na.get('name')} | {nb.get('name')}"
            )
            continue
        seq[cc] += 1
        by_cc[cc].append({
            "id": f"{cc}:K{seq[cc]:03d}",
            "pair": list(pair),
            "cc": cc,
            "kind": "AKTEUR-BAUVORHABEN" if project_count == 1 else "AKTEUR-AKTEUR",
            "a_label": label(na), "b_label": label(nb),
            "a_is_project": bool(na.get("is_project")),
            "b_is_project": bool(nb.get("is_project")),
            "status": "GEPRUEFT" if g else "UNGEPRUEFT",
            "beleg_url": (g or {}).get("beleg_url", ""),
            "relation_ist": (g or {}).get("relation_ist", ""),
            "zitat": (g or {}).get("beleg_zitat", ""),
        })

    emitted_ids = {r["id"] for rows in by_cc.values() for r in rows}
    unknown_replacements = sorted(set(evidence_replacements) - emitted_ids)
    if unknown_replacements:
        print(f"ABBRUCH: unbekannte IDs in {EVIDENCE_REPLACEMENTS}: {unknown_replacements}")
        return 1
    for rows in by_cc.values():
        for row in rows:
            replacement = evidence_replacements.get(row["id"])
            if replacement:
                row["beleg_url"] = replacement["evidence_url"]
                row["zitat"] = replacement["evidence_quote"]

    if kind_errors:
        print("ABBRUCH: Kantenart nicht eindeutig:")
        for msg in kind_errors[:20]:
            print(f"  {msg}")
        if len(kind_errors) > 20:
            print(f"  ... und {len(kind_errors) - 20} weitere")
        return 1

    os.makedirs(OUTDIR, exist_ok=True)
    for f in os.listdir(OUTDIR):
        if f.startswith("kanten_") and f.endswith(".md"):
            os.remove(os.path.join(OUTDIR, f))

    total = nbatch = 0
    index = []
    for cc in sorted(by_cc):
        recs = by_cc[cc]
        for i in range(0, len(recs), BATCH_SIZE):
            chunk = recs[i:i + BATCH_SIZE]
            nbatch += 1
            total += len(chunk)
            name = f"kanten_{cc}_b{i // BATCH_SIZE + 1}.md"
            with open(os.path.join(OUTDIR, name), "w", encoding="utf-8", newline="\n") as f:
                f.write("\n\n".join(block(r) for r in chunk) + "\n")
            index.append({"batch": name, "cc": cc, "n": len(chunk),
                          "edges": [{"id": r["id"], "pair": r["pair"], "kind": r["kind"],
                                     "status": r["status"],
                                     "a_is_project": r["a_is_project"],
                                     "b_is_project": r["b_is_project"],
                                     "evidence_url": r["beleg_url"],
                                     "evidence_quote": r["zitat"]} for r in chunk]})

    source_paths = [
        DEFAULT.export_path, *DEFAULT.overlay_paths, DEFAULT.audit_edges_path,
        DEFAULT.prune_path, DEFAULT.prune_faktencheck_path, DEFAULT.unklar_edges_path,
        os.path.join(BASE, "verdicts.json"), os.path.join(BASE, "worklist.json"),
        os.path.join(BASE, NODE_KIND_OVERRIDES),
        os.path.join(BASE, EVIDENCE_REPLACEMENTS),
        os.path.join(BASE, "KANTEN_TAXONOMIE.md"),
        os.path.join(BASE, "build_kanten_batches.py"),
        os.path.join(BASE, "assemble_kanten_prompt.py"),
        os.path.join(BASE, "validate_kanten.py"),
        os.path.join(BASE, "merge_kanten.py"),
        os.path.join(BASE, "preflight_kanten.py"),
        os.path.join(BASE, "recheck_kanten_sources.py"),
        os.path.join(BASE, "build_kanten_review_inventory.py"),
        os.path.join(BASE, "build_kanten_results.py"),
        os.path.join(NETZ, "netz", "data", "overlays.py"),
    ]
    export_meta = json.load(open(DEFAULT.export_path, encoding="utf-8")).get("meta", {})
    snapshot = {
        "snapshot_id": f"actors_network_{export_meta.get('exported_at', 'unknown')}",
        "neo4j_exported_at": export_meta.get("exported_at"),
        "neo4j_source": export_meta.get("source"),
        "inputs": [source_record(p) for p in source_paths],
    }
    with open(os.path.join(OUTDIR, "_index.json"), "w", encoding="utf-8") as f:
        json.dump({"review_run": REVIEW_RUN,
                   "generated_at": datetime.now(timezone.utc).isoformat(),
                   "source_snapshot": snapshot,
                   "batch_size": BATCH_SIZE, "total_edges": total, "batches": index},
                  f, indent=2, ensure_ascii=False)

    kinds = collections.Counter((r["kind"], r["status"]) for cc in by_cc for r in by_cc[cc])
    print(f"Kanten geschrieben : {total}")
    print(f"Batches            : {nbatch}  (<= {BATCH_SIZE} je Batch)")
    for k, v in sorted(kinds.items()):
        print(f"  {k[0]:20} {k[1]:11} {v}")
    print(f"je Land            : {dict(sorted((c, len(v)) for c, v in by_cc.items()))}")
    print(f"geschrieben nach   : {OUTDIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
