# -*- coding: utf-8 -*-
"""
Validate returned classification tables against the controlled vocabulary and
the batch register, before anything reaches the printed table.

The legal role names are extracted from KLASSIFIKATION_TAXONOMIE.md itself
(every `### \x60Rolle\x60` heading) plus the fallback values and the project-entry
values from the addendum -- so the vocabulary is never maintained twice.

Input: results/<batch>.md files, each holding the agent's markdown table
       (| ID | Name | Rolle(n) | Relevanz |).

Checks, per the prompt's own rules:
  * every batch ID answered exactly once, none invented
  * roles drawn only from the controlled vocabulary
  * project entries (BAUVORHABEN/OBJEKT) use only the Regel-P values, and
    non-projects never use them
  * Relevanz <= 90 chars, non-empty, not a bare copy of the role column
  * at most 3 roles

Usage:  python validate_klassifikation.py
"""
import json, os, re, glob, sys, collections

BASE = os.path.dirname(os.path.abspath(__file__))
TAXONOMIE = os.path.join(BASE, "KLASSIFIKATION_TAXONOMIE.md")
RESULTS = os.path.join(BASE, "results")
BATCHDIR = os.path.join(BASE, "batches")

FALLBACKS = {
    "Unzureichende Informationen",
    "Reuse-Bezug belegt, Rolle unklar",
    "Keine direkte Reuse-Rolle belegt",
}
PROJECT_ROLES = {"Referenzprojekt", "Referenzprojekt, Reuse-Umfang unklar"}
MAX_RELEVANZ = 90
MAX_ROLES = 3


def load_vocab():
    if not os.path.exists(TAXONOMIE):
        sys.exit(f"FEHLT: {TAXONOMIE} -- siehe assemble_klassifikation_prompt.py")
    text = open(TAXONOMIE, encoding="utf-8").read()
    roles = set(re.findall(r"^###\s+`([^`]+)`\s*$", text, re.M))
    if not roles:
        sys.exit("Kein Rollenvokabular in der Taxonomie gefunden "
                 "(erwartet: Ueberschriften der Form '### `Rollenname`').")
    return roles | FALLBACKS | PROJECT_ROLES


def load_batches():
    """id -> (batch, name, is_project)"""
    idx = json.load(open(os.path.join(BATCHDIR, "_index.json"), encoding="utf-8"))
    meta = {}
    for b in idx["batches"]:
        raw = open(os.path.join(BATCHDIR, b["batch"]), encoding="utf-8").read()
        projects = set(re.findall(r"^### (\S+)(?=(?:(?!^### ).)*?BAUVORHABEN/OBJEKT)",
                                  raw, re.M | re.S))
        for tid in b["ids"]:
            meta[tid] = (b["batch"], tid in projects)
    return meta, idx


ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*([^|]*?)\s*\|\s*$")


def parse(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        m = ROW.match(line.rstrip("\n"))
        if not m:
            continue
        rid, name, roles, rel = (g.strip() for g in m.groups())
        if not rid or rid.upper() == "ID" or set(rid) <= set("-: "):
            continue
        rows.append((rid, name, roles, rel))
    return rows


def main():
    vocab = load_vocab()
    meta, idx = load_batches()
    if not os.path.isdir(RESULTS):
        sys.exit(f"Kein Ergebnisordner: {RESULTS}")

    seen, problems = collections.Counter(), []
    for path in sorted(glob.glob(os.path.join(RESULTS, "*.md"))):
        for rid, name, roles, rel in parse(path):
            src = os.path.basename(path)
            seen[rid] += 1
            if rid not in meta:
                problems.append((src, rid, "unbekannte ID (nicht im Batch-Register)"))
                continue
            is_project = meta[rid][1]

            parts = [r.strip() for r in roles.split("/") if r.strip()]
            if not parts:
                problems.append((src, rid, "Rollen-Spalte leer"))
            if len(parts) > MAX_ROLES:
                problems.append((src, rid, f"{len(parts)} Rollen (max {MAX_ROLES})"))
            for r in parts:
                if r not in vocab:
                    problems.append((src, rid, f"Rolle ausserhalb des Vokabulars: {r!r}"))
                if is_project and r not in PROJECT_ROLES:
                    problems.append((src, rid, f"Objekt-Eintrag mit Akteursrolle: {r!r}"))
                if not is_project and r in PROJECT_ROLES:
                    problems.append((src, rid, f"Organisation mit Objekt-Rolle: {r!r}"))

            if not rel:
                problems.append((src, rid, "Relevanz leer"))
            elif len(rel) > MAX_RELEVANZ:
                problems.append((src, rid, f"Relevanz {len(rel)} Zeichen (max {MAX_RELEVANZ})"))
            if rel and rel.rstrip(".").strip().lower() == roles.strip().lower():
                problems.append((src, rid, "Relevanz wiederholt nur die Rollen-Spalte"))

    missing = [i for i in meta if i not in seen]
    dupes = [i for i, c in seen.items() if c > 1]

    print(f"erwartet : {len(meta)} Akteure in {len(idx['batches'])} Batches")
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
