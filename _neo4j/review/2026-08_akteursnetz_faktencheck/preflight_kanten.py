# -*- coding: utf-8 -*-
"""Fail-closed preflight for the edge-classification corpus."""
import hashlib
import json
import os
import re
import sys

import validate_kanten
import merge_kanten

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
BATCHDIR = os.path.join(BASE, "kanten_batches")
PROMPTDIR = os.path.join(BASE, "kanten_prompts")
INDEX = os.path.join(BATCHDIR, "_index.json")
TAXONOMY = os.path.join(BASE, "KANTEN_TAXONOMIE.md")

EXPECTED_A = {
    "Bauherrschaft", "Entwurf", "Fachplanung", "Reuse-Konzept",
    "Bauteilinventarisierung", "Rückbau", "Bauteillieferung", "Aufarbeitung",
    "Logistik", "Bauausführung", "Prüfung und Nachweis", "Forschungsbegleitung",
    "Förderung", "Betrieb", "Projektbeteiligung, Aufgabe unklar",
    "Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar",
}
EXPECTED_B = {
    "Konsortialpartner", "Kooperationsvereinbarung", "Gemeinsames Bauvorhaben",
    "Gründung", "Übernahme", "Konzernbindung", "Betreiberschaft", "Mitgliedschaft",
    "Trägerschaft", "Lieferbeziehung", "Dienstleistungsbeziehung",
    "Personelle Verflechtung", "Verzeichniseintrag", "Zusammenarbeit, Art unklar",
    "Kein Beleg für eine Beziehung", "Beziehung nicht prüfbar",
}
EXPECTED_REMOVAL_TYPES = {
    "Verzeichniseintrag", "Kein Beleg für eine Beziehung",
    "Beziehung nicht prüfbar",
}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    problems = []
    with open(INDEX, encoding="utf-8") as f:
        idx = json.load(f)
    with open(TAXONOMY, encoding="utf-8") as f:
        taxonomy = f.read()

    vocab, _ = validate_kanten.load_vocab()
    if vocab["AKTEUR-BAUVORHABEN"] != EXPECTED_A:
        problems.append("Vokabular A weicht vom freigegebenen Vertrag ab")
    if vocab["AKTEUR-AKTEUR"] != EXPECTED_B:
        problems.append("Vokabular B weicht vom freigegebenen Vertrag ab")
    if merge_kanten.REMOVAL_TYPES != EXPECTED_REMOVAL_TYPES:
        problems.append("Merge setzt die radikale Entfernungsregel nicht vollständig um")

    edges = [e for b in idx["batches"] for e in b["edges"]]
    ids = [e["id"] for e in edges]
    pairs = [tuple(sorted(e["pair"])) for e in edges]
    if idx["total_edges"] != len(edges):
        problems.append("total_edges stimmt nicht mit dem Register überein")
    if len(ids) != len(set(ids)):
        problems.append("doppelte Kanten-IDs")
    if len(pairs) != len(set(pairs)):
        problems.append("doppelte Kantenpaare")
    if sum(b["n"] for b in idx["batches"]) != len(edges):
        problems.append("Batchsummen stimmen nicht")
    if any(b["n"] > idx["batch_size"] for b in idx["batches"]):
        problems.append("Batch ist größer als batch_size")

    for e in edges:
        project_count = int(e.get("a_is_project", False)) + int(e.get("b_is_project", False))
        expected = "AKTEUR-BAUVORHABEN" if project_count == 1 else "AKTEUR-AKTEUR"
        if project_count > 1 or e["kind"] != expected:
            problems.append(f"Kantenart inkonsistent: {e['id']}")

    expected_batches = {b["batch"] for b in idx["batches"]}
    actual_batches = {n for n in os.listdir(BATCHDIR) if n.startswith("kanten_") and n.endswith(".md")}
    expected_prompts = {n.replace("kanten_", "prompt_") for n in expected_batches}
    actual_prompts = {n for n in os.listdir(PROMPTDIR) if n.startswith("prompt_") and n.endswith(".md")}
    if actual_batches != expected_batches:
        problems.append("Batchdateien stimmen nicht mit dem Register überein")
    if actual_prompts != expected_prompts:
        problems.append("Promptdateien stimmen nicht mit dem Register überein")

    for b in idx["batches"]:
        batch_path = os.path.join(BATCHDIR, b["batch"])
        with open(batch_path, encoding="utf-8") as f:
            batch_text = f.read()
        found_ids = re.findall(r"^###\s+([^\s]+)\s*$", batch_text, re.M)
        expected_ids = [e["id"] for e in b["edges"]]
        if found_ids != expected_ids:
            problems.append(f"ID-Reihenfolge stimmt nicht: {b['batch']}")
        prompt_name = b["batch"].replace("kanten_", "prompt_")
        with open(os.path.join(PROMPTDIR, prompt_name), encoding="utf-8") as f:
            prompt_text = f.read()
        expected_prompt = taxonomy.replace("{{KANTENDATEN}}", batch_text.rstrip() + "\n")
        if prompt_text != expected_prompt:
            problems.append(f"Prompt ist nicht reproduzierbar: {prompt_name}")

    snapshot = idx.get("source_snapshot", {})
    if not snapshot.get("snapshot_id") or not snapshot.get("inputs"):
        problems.append("Quell-Snapshot fehlt")
    for rec in snapshot.get("inputs", []):
        path = os.path.join(REPO, rec["path"])
        if not os.path.isfile(path):
            problems.append(f"Snapshot-Quelle fehlt: {rec['path']}")
        elif sha256(path) != rec["sha256"]:
            problems.append(f"Snapshot-Quelle hat sich geändert: {rec['path']}")

    print(f"Kanten: {len(edges)} | Batches: {len(idx['batches'])} | Prompts: {len(actual_prompts)}")
    print(f"Snapshot: {snapshot.get('snapshot_id', 'FEHLT')}")
    if problems:
        print(f"PREFLIGHT FEHLGESCHLAGEN: {len(problems)} Problem(e)")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("PREFLIGHT OK — Klassifikationsbatches dürfen gestartet werden.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
