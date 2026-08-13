# -*- coding: utf-8 -*-
"""
Merge the returned relationship tables into a strict positive list and its
complete complement.

Three removal reasons, all from the project's own rules, are computed here
rather than inferred from an earlier graph grade:

  R-V  `Verzeichniseintrag`            -- a shared listing in a directory is not
       a relationship between the listed actors. This is the fixed directory
       rule the plan states ("directory-only ties EXCLUDED -- same bar we used
       to remove the fan-boxes"), and it is why 63 of the 125 unverified drawn
       edges hang off Opalis, bauteilnetz, SalvoWEB, Bolius and byggogbevar.
  R-K  `Kein Beleg für eine Beziehung` -- research ran and found no source that
       names both nodes in a described connection. Same standard that removed
       the `ohne_beleg` actors.
  R-N  `Beziehung nicht prüfbar`        -- the available source could not be
       checked and no accessible replacement proves the relationship.

The classifier never saw `edge_degree`, so a `Kein Beleg` verdict on an edge the
fact-check graded `belegt` is a real disagreement and lands in the conflict file
for traceability. It is still removed: an earlier grade is not current evidence.

Input : kanten_results/*.md, kanten_batches/_index.json, verdicts.json
Output: kanten_klassifikation.json
        keep_kanten_final.json         (complete positive allowlist)
        prune_kanten_final.json        (eid pairs to drop from the drawing)
        kanten_konflikte.md
"""
import json, os, re, glob, sys, collections, tempfile

import validate_kanten

BASE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(BASE, "kanten_results")
BATCHDIR = os.path.join(BASE, "kanten_batches")

REMOVE_V = "Verzeichniseintrag"
REMOVE_K = "Kein Beleg für eine Beziehung"
NICHT_PRUEFBAR = "Beziehung nicht prüfbar"
REMOVAL_TYPES = {REMOVE_V, REMOVE_K, NICHT_PRUEFBAR}

ROW = re.compile(r"^\|" + r"\s*([^|]*?)\s*\|" * 6 + r"\s*$")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json_atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".", suffix=".tmp",
                               dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(value, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_text_atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".", suffix=".tmp",
                               dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(value)
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def removal_decision(art, degree):
    remove = art in REMOVAL_TYPES
    conflict = remove and degree in ("belegt", "teilweise_belegt")
    return remove, conflict, remove


def main():
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print(__doc__)
        return 0
    if not os.path.isdir(RESULTS):
        sys.exit(f"Kein Ergebnisordner: {RESULTS}")

    print("Validierung vor Merge:")
    if validate_kanten.main() != 0:
        sys.exit("ABBRUCH: Ergebnisse sind unvollstaendig oder ungueltig; nichts geschrieben.")

    idx = load(os.path.join(BATCHDIR, "_index.json"))
    meta = {e["id"]: e for b in idx["batches"] for e in b["edges"]}

    V = load(os.path.join(BASE, "verdicts.json"))
    W = load(os.path.join(BASE, "worklist.json"))
    key2eid = {}
    for pkt in W["packets"]:
        for n in pkt.get("nodes", []):
            key2eid[(pkt["cc"], n["tid"])] = n["eid"]
    degree = {}
    for e in V["edges"]:
        a = key2eid.get((e["cc"], e["a_tid"]))
        b = key2eid.get((e["cc"], e["b_tid"]))
        if a and b:
            degree[tuple(sorted((a, b)))] = e.get("edge_degree")

    rows = {}
    for path in sorted(glob.glob(os.path.join(RESULTS, "*.md"))):
        for line in open(path, encoding="utf-8"):
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            rid, art, richtung, beschr, beleg, belegzitat = (
                g.strip() for g in m.groups()
            )
            if not rid or rid.upper() == "ID" or set(rid) <= set("-: "):
                continue
            rows[rid] = {"art": art, "richtung": richtung, "beschreibung": beschr,
                         "beleg": beleg, "belegzitat": belegzitat,
                         "batch": os.path.basename(path)}

    out, keep, prune, konflikte, missing = {}, [], [], [], []
    stats = collections.Counter()

    for rid, e in meta.items():
        r = rows.get(rid)
        if not r:
            missing.append(rid)
            continue
        pair = tuple(sorted(e["pair"]))
        art = r["art"]
        stats[art] += 1
        deg = degree.get(pair)

        _, konflikt, entfernen = removal_decision(art, deg)
        if konflikt:
            warum = {
                REMOVE_K: "Früherer Grad positiv; aktuelle Prüfung findet keinen Beleg",
                REMOVE_V: "Früherer Grad positiv; aktuelle Prüfung findet nur eine Verzeichnislistung",
                NICHT_PRUEFBAR: "Früherer Grad positiv; aktuelle Quelle ist nicht prüfbar",
            }[art]
            konflikte.append((rid, art, deg, warum))
        if entfernen:
            prune.append(list(pair))
        else:
            keep.append(list(pair))

        if konflikt:
            review_status = "reviewed_remove_prior_grade_conflict"
        elif entfernen:
            review_status = "reviewed_remove"
        else:
            review_status = "reviewed_keep"

        out[rid] = {
            "id": rid, "cc": e["kind"] and rid.split(":")[0], "kind": e["kind"],
            "pair": list(pair), "status_vorher": e["status"],
            "beziehungsart": art, "richtung": r["richtung"],
            "beschreibung": r["beschreibung"], "beleg": r["beleg"],
            "evidence_url": (r["beleg"] if r["beleg"].startswith(("http://", "https://"))
                             else e.get("evidence_url") or None),
            "evidence_quote": (r["belegzitat"] if r["belegzitat"] != "—" else
                               e.get("evidence_quote") or None),
            "evidence_confidence": ("belegt" if not entfernen else "unklar"),
            "edge_degree_faktencheck": deg,
            "review_run": idx.get("review_run", "2026-08_akteursnetz_faktencheck_kanten"),
            "result_batch": r["batch"],
            "merge_art": "relationship_classification_by_edge_id",
            "review_status": review_status,
            "source_snapshot": idx.get("source_snapshot", {}).get("snapshot_id"),
            "evidence_basis": ("directory_listing_only" if art == REMOVE_V else
                               "no_supporting_source_found" if art == REMOVE_K else
                               "access_not_verifiable" if art == NICHT_PRUEFBAR else
                               "existing_evidence_rechecked" if e["status"] == "GEPRUEFT" else
                               "new_web_research"),
            "entfernen": entfernen,
        }

    if missing:
        sys.exit(f"ABBRUCH: {len(missing)} IDs fehlen trotz Validierung; nichts geschrieben.")

    all_pairs = {tuple(sorted(e["pair"])) for e in meta.values()}
    keep_pairs = {tuple(pair) for pair in keep}
    prune_pairs = {tuple(pair) for pair in prune}
    if keep_pairs & prune_pairs or keep_pairs | prune_pairs != all_pairs:
        sys.exit("ABBRUCH: Keep/Prune bilden keine disjunkte Vollpartition; nichts geschrieben.")

    out_path = os.path.join(BASE, "kanten_klassifikation.json")
    keep_path = os.path.join(BASE, "keep_kanten_final.json")
    prune_path = os.path.join(BASE, "prune_kanten_final.json")
    conflict_path = os.path.join(BASE, "kanten_konflikte.md")

    lines = ["# Kanten — Konflikte mit der Faktenprüfung", "",
             "Die Klassifikation lief ohne Kenntnis des Kantengrads. Wo sie eine Kante",
             "verwirft, die die Faktenprüfung früher als belegt geführt hat, wird der",
             "Widerspruch hier dokumentiert. Nach dem Positivlisten-Prinzip werden diese",
             "Kanten trotzdem entfernt. Nur ein neuer konkreter Beleg und eine erneute",
             "Klassifikation dürfen sie in die Keep-Liste zurückbringen.", "",
             f"**{len(konflikte)} Fälle**", "",
             "| ID | Klassifikation | Grad | Befund |", "|---|---|---|---|"]
    for rid, art, deg, why in sorted(konflikte):
        lines.append(f"| {rid} | {art} | {deg} | {why} |")
    conflict_text = "\n".join(lines) + "\n"

    write_json_atomic(out_path, out)
    write_json_atomic(keep_path, sorted(keep))
    write_json_atomic(prune_path, sorted(prune))
    write_text_atomic(conflict_path, conflict_text)

    print(f"erwartet   : {len(meta)}")
    print(f"gemerged   : {len(out)}")
    print(f"fehlend    : {len(missing)}" + (f"  {missing[:8]}" if missing else ""))
    print(f"entfernen: {len(prune)}  ({stats[REMOVE_V]}x Verzeichniseintrag, "
          f"{stats[REMOVE_K]}x kein Beleg, {stats[NICHT_PRUEFBAR]}x nicht prüfbar)")
    print(f"behalten  : {len(keep)}")
    print(f"Partition : {len(keep)} + {len(prune)} = {len(meta)}")
    print(f"Konflikte  : {len(konflikte)}  -> kanten_konflikte.md")
    print("geschrieben: kanten_klassifikation.json, keep_kanten_final.json, "
          "prune_kanten_final.json, kanten_konflikte.md")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
