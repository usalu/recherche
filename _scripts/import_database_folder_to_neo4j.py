"""
Import nodes and relationships from _database into Neo4j.

Sources (under repo _database/ by default):
  - _system/node_inventory.csv  → MERGE nodes keyed by typed_path
  - _edges/clean_confirmed_edges.csv → MERGE directed relationships

Nodes with entity `datenmodell` are skipped (no :Datenmodell vertices); edges touching
`datenmodell` are skipped so MATCH endpoints always exist.

Environment (same as export_visual_attachment_to_neo4j.py):
  NEO4J_URI, NEO4J_USER, NEO4J_DATABASE, NEO4J_PASSWORD

Examples:
  pip install -r requirements-neo4j.txt
  set NEO4J_PASSWORD=...
  python _scripts/import_database_folder_to_neo4j.py
  python _scripts/import_database_folder_to_neo4j.py --edges-only
  python _scripts/import_database_folder_to_neo4j.py --confirm-wipe --wipe
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

# Entity slug (SQLite / CSV) → single Neo4j label (PascalCase, ASCII).
ENTITY_LABEL: dict[str, str] = {
    "akteur": "Akteur",
    "akteur_beteiligung": "AkteurBeteiligung",
    "akteurrolle": "Akteurrolle",
    "aufbereitungsverfahren": "Aufbereitungsverfahren",
    "bauaufgabe_intervention": "BauaufgabeIntervention",
    "bauobjekt": "Bauobjekt",
    "bauobjektklasse": "Bauobjektklasse",
    "bauobjektrolle": "Bauobjektrolle",
    "bauobjektstatus": "Bauobjektstatus",
    "bausystem": "Bausystem",
    "bauteilebene": "Bauteilebene",
    "bauteiltyp": "Bauteiltyp",
    "bauteilzustand": "Bauteilzustand",
    "bauweise": "Bauweise",
    "beschaffungsweg": "Beschaffungsweg",
    "bewertungslogik_abgrenzung": "BewertungslogikAbgrenzung",
    "datenpunkt": "Messpunkt",
    "datenqualitaet": "Datenqualitaet",
    "dokumenttyp": "Dokumenttyp",
    "fallstudie": "Fallstudie",
    "foerderprogramm": "Foerderprogramm",
    "fuegung_verbindung": "FuegungVerbindung",
    "funktionswechsel": "Funktionswechsel",
    "huerde": "Huerde",
    "kennwertdefinition": "Kennwertdefinition",
    "kontextmerkmal": "Kontextmerkmal",
    "leistungsanforderung": "Leistungsanforderung",
    "logistik": "Logistik",
    "material": "Material",
    "methode": "Methode",
    "norm": "Norm",
    "nutzung": "Nutzung",
    "ort": "Ort",
    "programm_kontext": "ProgrammKontext",
    "projekt": "Projekt",
    "prozessphase": "Prozessphase",
    "pruefung_nachweis": "PruefungNachweis",
    "quelle": "Quelle",
    "rechtliche_bedingung": "RechtlicheBedingung",
    "ressourcenquelle": "Ressourcenquelle",
    "reuse_einsatz": "ReuseEinsatz",
    "reuse_einsatzstatus": "ReuseEinsatzstatus",
    "reuse_kette": "ReuseKette",
    "reuse_kettenstation": "ReuseKettenstation",
    "reuse_strategie": "ReuseStrategie",
    "rueckbauverfahren": "Rueckbauverfahren",
    "schadstoff": "Schadstoff",
    "software_digitaltool": "SoftwareDigitaltool",
    "tooltyp": "Tooltyp",
    "tragwerksprinzip": "Tragwerksprinzip",
    "tragwerkstyp": "Tragwerkstyp",
    "wirtschaft": "Wirtschaft",
    "zertifizierung_bewertungssystem": "ZertifizierungBewertungssystem",
}

REL_PROP_KEYS = (
    "field",
    "raw_label",
    "confidence",
    "resolution_rule",
    "legacy_path",
    "original_source",
    "original_relation",
    "original_target",
    "edge_cleaning",
)

VALID_REL_TYPE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_database_dir() -> Path:
    return repo_root() / "_database"


def label_for_entity(entity: str) -> str:
    if entity not in ENTITY_LABEL:
        raise KeyError(f"Missing ENTITY_LABEL mapping for entity {entity!r}")
    lab = ENTITY_LABEL[entity]
    if not lab.isalnum():
        raise ValueError(f"Label must be alphanumeric: {lab!r}")
    return lab


def int_or_none(s: str) -> int | None:
    s = (s or "").strip()
    if not s:
        return None
    return int(s)


def merge_nodes_batch(tx, label: str, rows: list[dict]):
    q = f"""
    UNWIND $rows AS row
    MERGE (n:`{label}` {{typed_path: row.typed_path}})
    SET n += row.props
    """
    tx.run(q, rows=rows)


def merge_edges_batch(tx, rel_type: str, rows: list[dict]):
    if not VALID_REL_TYPE.match(rel_type):
        raise ValueError(f"Unsafe relationship type {rel_type!r}")
    q = f"""
    UNWIND $rows AS row
    MATCH (a {{typed_path: row.source}}), (b {{typed_path: row.target}})
    MERGE (a)-[r:`{rel_type}`]->(b)
    SET r += row.props
    """
    tx.run(q, rows=rows)


def wipe_graph(tx):
    tx.run("MATCH (n) DETACH DELETE n")


def load_inventory_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_edge_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def row_to_node_props(row: dict[str, str]) -> dict:
    dfc = int_or_none(row.get("dateien_file_count", ""))
    isc = int_or_none(row.get("imported_source_count", ""))
    props: dict = {
        "entity": row["entity"],
        "id": row["id"],
        "title": row.get("title") or "",
        "build_status": row.get("build_status") or "",
        "markdown_path": row.get("markdown_path") or "",
    }
    if dfc is not None:
        props["dateien_file_count"] = dfc
    if isc is not None:
        props["imported_source_count"] = isc
    return props


def row_to_rel_props(row: dict[str, str]) -> dict:
    out: dict = {}
    for k in REL_PROP_KEYS:
        v = (row.get(k) or "").strip()
        if v:
            out[k] = v
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--database-dir",
        type=Path,
        default=default_database_dir(),
        help="Path to _database folder",
    )
    ap.add_argument("--nodes-only", action="store_true")
    ap.add_argument("--edges-only", action="store_true")
    ap.add_argument(
        "--wipe",
        action="store_true",
        help="DETACH DELETE all nodes before import (destructive).",
    )
    ap.add_argument(
        "--confirm-wipe",
        action="store_true",
        help="Required together with --wipe.",
    )
    ap.add_argument("--batch-size", type=int, default=400)
    args = ap.parse_args()

    if args.nodes_only and args.edges_only:
        print("Choose at most one of --nodes-only / --edges-only", file=sys.stderr)
        return 1
    if args.wipe and not args.confirm_wipe:
        print("Refusing --wipe without --confirm-wipe", file=sys.stderr)
        return 1

    base: Path = args.database_dir
    inv_path = base / "_system" / "node_inventory.csv"
    edge_path = base / "_edges" / "clean_confirmed_edges.csv"
    if not inv_path.is_file():
        print(f"Missing {inv_path}", file=sys.stderr)
        return 1
    if not args.nodes_only and not edge_path.is_file():
        print(f"Missing {edge_path}", file=sys.stderr)
        return 1

    password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if not password:
        print("NEO4J_PASSWORD is not set.", file=sys.stderr)
        return 1
    uri = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
    user = os.environ.get("NEO4J_USER", "neo4j").strip()
    database = (os.environ.get("NEO4J_DATABASE") or "neo4j").strip() or "neo4j"

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("Install the driver: pip install neo4j", file=sys.stderr)
        return 1

    inv_rows = load_inventory_rows(inv_path)
    entities_in_file = {r["entity"] for r in inv_rows}
    missing_map = entities_in_file - set(ENTITY_LABEL.keys()) - {"datenmodell"}
    if missing_map:
        print(f"node_inventory.csv uses unknown entities (add ENTITY_LABEL): {sorted(missing_map)}", file=sys.stderr)
        return 1

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        print(f"Connected {uri}  database=`{database}`")

        def session():
            return driver.session(database=database)

        with session() as sess:
            if args.wipe:
                sess.execute_write(wipe_graph)
                print("Wiped graph (all nodes and relationships removed).")

            if not args.edges_only:
                by_label: dict[str, list[dict]] = defaultdict(list)
                skipped_dm = 0
                for row in inv_rows:
                    ent = row["entity"]
                    if ent == "datenmodell":
                        skipped_dm += 1
                        continue
                    lab = label_for_entity(ent)
                    tp = row["typed_path"]
                    by_label[lab].append({"typed_path": tp, "props": row_to_node_props(row)})

                for lab, rows in sorted(by_label.items(), key=lambda x: x[0]):
                    for i in range(0, len(rows), args.batch_size):
                        chunk = rows[i : i + args.batch_size]
                        sess.execute_write(merge_nodes_batch, lab, chunk)
                    print(f"  Nodes :{lab}  count={len(rows)}")

                print(f"Imported {sum(len(v) for v in by_label.values())} nodes (skipped datenmodell rows: {skipped_dm}).")

            if not args.nodes_only:
                edge_rows = load_edge_rows(edge_path)
                skipped_edges = 0
                by_rel: dict[str, list[dict]] = defaultdict(list)
                for row in edge_rows:
                    if row["source_entity"] == "datenmodell" or row["target_entity"] == "datenmodell":
                        skipped_edges += 1
                        continue
                    rt = row["relation"]
                    if not VALID_REL_TYPE.match(rt):
                        print(f"Skipping edge with invalid relation type {rt!r}", file=sys.stderr)
                        skipped_edges += 1
                        continue
                    by_rel[rt].append(
                        {
                            "source": row["source"],
                            "target": row["target"],
                            "props": row_to_rel_props(row),
                        }
                    )

                for rt in sorted(by_rel.keys()):
                    rows = by_rel[rt]
                    for i in range(0, len(rows), args.batch_size):
                        chunk = rows[i : i + args.batch_size]
                        sess.execute_write(merge_edges_batch, rt, chunk)
                    print(f"  Edges :{rt}  count={len(rows)}")

                print(
                    f"Imported {sum(len(v) for v in by_rel.values())} relationships "
                    f"(skipped {skipped_edges} datenmodell / invalid rows)."
                )

            rec = sess.run("MATCH (n) RETURN count(n) AS c").single()
            relc = sess.run("MATCH ()-[r]->() RETURN count(r) AS c").single()
            print(f"Totals now: {rec['c']} nodes, {relc['c']} relationships.")
    finally:
        driver.close()

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
