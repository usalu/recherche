# -*- coding: utf-8 -*-
"""
Validate returned relationship tables against the controlled vocabulary and the
edge register.

The legal relation types are extracted from KANTEN_TAXONOMIE.md itself (every
`### \x60Art\x60` heading), so prompt and validator cannot drift apart. Which
vocabulary is legal depends on the edge kind, so the two blocks are read
separately: section 3 applies to AKTEUR-BAUVORHABEN, section 4 to
AKTEUR-AKTEUR, section 5 (fallbacks) to both.

Input: kanten_results/*.md
       (| ID | Beziehungsart | Richtung | Beschreibung | Beleg | Belegzitat |)

Usage:  python validate_kanten.py
"""
import json, os, re, glob, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
TAXONOMIE = os.path.join(BASE, "KANTEN_TAXONOMIE.md")
RESULTS = os.path.join(BASE, "kanten_results")
BATCHDIR = os.path.join(BASE, "kanten_batches")

MAX_BESCHREIBUNG = 90
MAX_BELEGZITAT = 240
RICHTUNGEN = {"A→B", "B→A", "—"}

# Arten, die laut Abschnitt 7 immer symmetrisch sind
SYMMETRISCH = {
    "Konsortialpartner", "Kooperationsvereinbarung", "Gemeinsames Bauvorhaben",
    "Personelle Verflechtung", "Verzeichniseintrag", "Zusammenarbeit, Art unklar",
}

GERICHTET_AKTEUR_AKTEUR = {
    "Gründung", "Übernahme", "Konzernbindung", "Betreiberschaft",
    "Mitgliedschaft", "Trägerschaft", "Lieferbeziehung",
    "Dienstleistungsbeziehung",
}


def sections(text):
    """Split the taxonomy into its top-level '# n. ...' sections."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        m = re.match(r"^#\s+(\d+)\.", line)
        if m:
            if cur:
                out[cur] = "\n".join(buf)
            cur, buf = m.group(1), [line]
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf)
    return out


def load_vocab():
    if not os.path.exists(TAXONOMIE):
        sys.exit(f"FEHLT: {TAXONOMIE}")
    sec = sections(open(TAXONOMIE, encoding="utf-8").read())
    heads = lambda s: set(re.findall(r"^###\s+`([^`]+)`\s*$", sec.get(s, ""), re.M))
    fallback = {"Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar"}
    vok_a, vok_b = heads("3"), heads("4")
    if not vok_a or not vok_b:
        sys.exit("Vokabular A (Abschnitt 3) oder B (Abschnitt 4) nicht gefunden.")
    return {"AKTEUR-BAUVORHABEN": vok_a | fallback,
            "AKTEUR-AKTEUR": vok_b | fallback}, fallback


def load_edges():
    idx = json.load(open(os.path.join(BATCHDIR, "_index.json"), encoding="utf-8"))
    meta = {}
    for b in idx["batches"]:
        for e in b["edges"]:
            meta[e["id"]] = e
    return meta, idx


ROW = re.compile(r"^\|" + r"\s*([^|]*?)\s*\|" * 6 + r"\s*$")


def direction_error(kind, art, richtung, fallback):
    if richtung not in RICHTUNGEN:
        return f"Richtung ungueltig: {richtung!r}"
    if art in SYMMETRISCH and richtung != "—":
        return f"{art} ist symmetrisch, Richtung muss '—' sein"
    if art in fallback and richtung != "—":
        return "Rueckfallwert muss Richtung '—' tragen"
    if art in GERICHTET_AKTEUR_AKTEUR and richtung not in ("A→B", "B→A"):
        return f"{art} braucht A→B oder B→A"
    if kind == "AKTEUR-BAUVORHABEN" and art not in fallback \
            and richtung not in ("A→B", "B→A"):
        return "Akteur-Bauvorhaben braucht eine gerichtete Angabe"
    return None


def main():
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print(__doc__)
        return 0
    vocab, fallback = load_vocab()
    meta, idx = load_edges()
    if not os.path.isdir(RESULTS):
        sys.exit(f"Kein Ergebnisordner: {RESULTS}")

    expected_files = {b["batch"] for b in idx["batches"]}
    actual_files = {
        os.path.basename(p) for p in glob.glob(os.path.join(RESULTS, "*.md"))
    }
    seen, problems = collections.Counter(), []
    for name in sorted(expected_files - actual_files):
        problems.append((name, "—", "Ergebnisdatei fehlt"))
    for name in sorted(actual_files - expected_files):
        problems.append((name, "—", "unerwartete Ergebnisdatei"))

    expected_file_for_id = {
        e["id"]: b["batch"] for b in idx["batches"] for e in b["edges"]
    }
    for path in sorted(glob.glob(os.path.join(RESULTS, "*.md"))):
        src = os.path.basename(path)
        for line in open(path, encoding="utf-8"):
            m = ROW.match(line.rstrip("\n"))
            if not m:
                continue
            rid, art, richtung, beschr, beleg, belegzitat = (
                g.strip() for g in m.groups()
            )
            if not rid or rid.upper() == "ID" or set(rid) <= set("-: "):
                continue
            seen[rid] += 1
            e = meta.get(rid)
            if not e:
                problems.append((src, rid, "unbekannte ID (nicht im Kanten-Register)"))
                continue
            if src != expected_file_for_id[rid]:
                problems.append((src, rid,
                                 f"ID gehoert in {expected_file_for_id[rid]}"))

            legal = vocab[e["kind"]]
            if art not in legal:
                other = "AKTEUR-AKTEUR" if e["kind"] == "AKTEUR-BAUVORHABEN" else "AKTEUR-BAUVORHABEN"
                hint = "  (gehoert zum anderen Vokabular)" if art in vocab[other] else ""
                problems.append((src, rid, f"Art unzulaessig fuer {e['kind']}: {art!r}{hint}"))

            dir_problem = direction_error(e["kind"], art, richtung, fallback)
            if dir_problem:
                problems.append((src, rid, dir_problem))

            if not beschr:
                problems.append((src, rid, "Beschreibung leer"))
            elif len(beschr) > MAX_BESCHREIBUNG:
                problems.append((src, rid, f"Beschreibung {len(beschr)} Zeichen (max {MAX_BESCHREIBUNG})"))

            if art in fallback:
                if beleg != "—":
                    problems.append((src, rid, "Rueckfallwert muss Beleg '—' tragen"))
                if belegzitat != "—":
                    problems.append((src, rid, "Rueckfallwert muss Belegzitat '—' tragen"))
            elif e["status"] == "UNGEPRUEFT":
                if not re.fullmatch(r"https?://\S+", beleg):
                    problems.append((src, rid, "UNGEPRUEFT klassifiziert, aber keine Beleg-URL angegeben"))
            else:
                if beleg.lower() != "vorhanden":
                    problems.append((src, rid, "GEPRUEFT muss Beleg 'vorhanden' tragen"))
                if not re.fullmatch(r"https?://\S+", e.get("evidence_url", "")):
                    problems.append((src, rid,
                                     "GEPRUEFT positiv, aber Register enthält keine Beleg-URL"))
            if art not in fallback:
                if not belegzitat or belegzitat == "—":
                    problems.append((src, rid, "Positive Kante braucht ein Belegzitat"))
                elif len(belegzitat) > MAX_BELEGZITAT:
                    problems.append((src, rid,
                                     f"Belegzitat {len(belegzitat)} Zeichen "
                                     f"(max {MAX_BELEGZITAT})"))

    missing = [i for i in meta if i not in seen]
    dupes = [i for i, c in seen.items() if c > 1]

    print(f"erwartet : {len(meta)} Kanten in {len(idx['batches'])} Batches")
    print(f"erhalten : {len(seen)} eindeutige IDs")
    print(f"fehlend  : {len(missing)}" + (f"  {missing[:10]}" if missing else ""))
    print(f"doppelt  : {len(dupes)}" + (f"  {dupes[:10]}" if dupes else ""))
    print(f"Regelverstoesse: {len(problems)}")
    for src, rid, why in problems[:40]:
        print(f"  {src} {rid}: {why}")
    if len(problems) > 40:
        print(f"  ... und {len(problems)-40} weitere")
    return 1 if (problems or missing or dupes) else 0


if __name__ == "__main__":
    sys.exit(main())
