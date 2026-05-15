"""
LEGACY REVIEW REQUIRED.

Import nodes and relationships from the retired folder-first database layout into Neo4j.

Neo4j is now the source of truth. This script is kept only for controlled review
or archaeology of the former `research/` / `_database` workflow; it is not the
normal current import entry point.

Sources (under repo _database/ by default):
  - _system/node_inventory.csv  -> MERGE nodes keyed by typed_path
  - _edges/clean_confirmed_edges.csv -> MERGE directed relationships (CSV `relation` folded to the five Neo4j types per plan §7.1; see `neo4j_relation_fold.py`)

Nodes with entity `datenmodell` or `tooltyp` are skipped (no `:Datenmodell` / `:Tooltyp` vertices); edges touching
those entities are skipped so MATCH endpoints always exist. Tool categories from `tooltyp/` are represented as
optional `tooltyp` / `softwaretyp` properties on `:Tool` / `:Software` in a dedicated export—not as inventory nodes here.
Rows with `entity=akteur` become `:Person` or a §6.1 organisation-actor label (see `akteur_org_neo4j_label.py`; no `akteurtyp` property).
Rows with `entity=ort` become `:Land` or `:Stadt` from folder `id` (see `ort_geo_label.py`; no `:Ort` label).
Rows with `entity=software_digitaltool` become `:Software` or `:Tool` (see `software_tool_label.py`).

Environment (same as export_visual_attachment_to_neo4j.py):
  NEO4J_URI, NEO4J_USER (or NEO4J_USERNAME as used by Neo4j MCP), NEO4J_DATABASE, NEO4J_PASSWORD

Examples:
  pip install -r requirements-neo4j.txt
  set NEO4J_PASSWORD=...
  python _scripts/import_database_folder_to_neo4j.py
  python _scripts/import_database_folder_to_neo4j.py --edges-only
  python _scripts/import_database_folder_to_neo4j.py --confirm-wipe --wipe
  python _scripts/import_database_folder_to_neo4j.py --confirm-wipe --wipe-only
  python _scripts/import_database_folder_to_neo4j.py --nodes-only --entities material ort
  python _scripts/import_database_folder_to_neo4j.py --nodes-only --entities akteur
  python _scripts/import_database_folder_to_neo4j.py --nodes-only --entities akteur --password-file .neo4j_password
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import defaultdict
from pathlib import Path

from akteur_org_neo4j_label import neo4j_label_for_akteur_folder
from neo4j_relation_fold import NEO4J_REL_TYPES, fold_csv_relation
from ort_geo_label import neo4j_label_for_ort_id
from software_tool_label import neo4j_label_for_software_digitaltool_id

# Inventory `entity` → Neo4j label for rows that do not need custom logic in
# `label_for_inventory_row` (plan `.cursor/plans/neo4j_schema_catalogue_3bc01035.plan.md` §5.2 / §5.4).
ENTITY_LABEL: dict[str, str] = {
    "akteurrolle": "Akteurrolle",
    "aufbereitungsverfahren": "Aufbereitungsverfahren",
    "bauaufgabe_intervention": "BauaufgabeIntervention",
    "bauobjekt": "Bauwerk",
    "bauobjektstatus": "Status",
    "bausystem": "Bausystem",
    "bauteilebene": "Bauteilebene",
    "bauteilgruppe": "Bauteilgruppe",
    "bauteiltyp": "Bauteiltyp",
    "bauteilzustand": "Bauteilzustand",
    "bauweise": "Bauweise",
    "beschaffungsweg": "Beschaffungsweg",
    "bewertungslogik_abgrenzung": "WiederverwendungsArt",
    "datenqualitaet": "Datenqualitaet",
    "fallstudie": "Fallbeispiel",
    "gebaeude": "Fallbeispiel",
    "foerderprogramm": "Programm",
    "fuegung_verbindung": "Verbindungstechnik",
    "funktionswechsel": "Funktionswechsel",
    "huerde": "Huerde",
    "kontextmerkmal": "Programm",
    "leistungsanforderung": "Leistungsanforderung",
    "logistik": "Logistik",
    "material": "Material",
    "methode": "Methode",
    "norm": "Norm",
    "nutzung": "Nutzung",
    "programm_kontext": "Programm",
    "projekt": "Fallbeispiel",
    "person": "Person",
    "prozessphase": "Prozessphase",
    "pruefung_nachweis": "PruefungNachweis",
    "quelle": "Quelle",
    "rechtliche_bedingung": "RechtlicheBedingung",
    "ressourcenquelle": "Ressourcenquelle",
    "reuse_einsatz": "Bauteilgruppe",
    "reuse_einsatzstatus": "Status",
    "reuse_kette": "Wiederverwendungskette",
    "reuse_strategie": "WiederverwendungsArt",
    "rueckbauverfahren": "Rueckbauverfahren",
    "schadstoff": "Schadstoff",
    "tragwerksprinzip": "Tragwerksprinzip",
    "wirtschaft": "Wirtschaft",
    "zertifizierung_bewertungssystem": "ZertifizierungBewertungssystem",
}

# §5.4 — no standalone graph nodes for these inventory `entity` values.
SKIP_NODE_ENTITIES: frozenset[str] = frozenset(
    {
        "akteur_beteiligung",
        "bauobjektklasse",
        "bauobjektrolle",
        "datenpunkt",
        "dokumenttyp",
        "kennwertdefinition",
        "reuse_kettenstation",
        "tragwerkstyp",
    }
)

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

def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_database_dir() -> Path:
    """Legacy default retained only so old calls fail visibly if the tree is absent."""
    return repo_root() / "research"


def label_for_entity(entity: str) -> str:
    if entity not in ENTITY_LABEL:
        raise KeyError(f"Missing ENTITY_LABEL mapping for entity {entity!r}")
    lab = ENTITY_LABEL[entity]
    if not lab.isalnum():
        raise ValueError(f"Label must be alphanumeric: {lab!r}")
    return lab


def label_for_inventory_row(row: dict[str, str], database_dir: Path) -> str:
    """Map inventory `entity` to the Neo4j label name (plan neo4j_schema_catalogue)."""
    ent = row["entity"]
    if ent == "person":
        return label_for_entity("person")
    if ent == "akteur":
        lab = neo4j_label_for_akteur_folder(database_dir, row["id"])
        if not lab.isalnum():
            raise ValueError(f"Label must be alphanumeric: {lab!r}")
        return lab
    if ent == "ort":
        lab = neo4j_label_for_ort_id(row["id"])
        if not lab.isalnum():
            raise ValueError(f"Label must be alphanumeric: {lab!r}")
        return lab
    if ent == "software_digitaltool":
        lab = neo4j_label_for_software_digitaltool_id(row["id"])
        if not lab.isalnum():
            raise ValueError(f"Label must be alphanumeric: {lab!r}")
        return lab
    return label_for_entity(ent)


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
    if rel_type not in NEO4J_REL_TYPES:
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


def row_to_node_props(row: dict[str, str], neo4j_label: str) -> dict:
    """Metadata-only props (plan §4): no build_status / markdown_path; title only on Software/Tool."""
    dfc = int_or_none(row.get("dateien_file_count", ""))
    isc = int_or_none(row.get("imported_source_count", ""))
    props: dict = {"id": row["id"]}
    if neo4j_label in ("Software", "Tool"):
        title = (row.get("title") or "").strip()
        if title:
            props["title"] = title
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
    # Neo4j relationship types include non-ASCII (e.g. GEHÖRT_ZU); avoid mojibake on Windows cp1252 consoles.
    for stream in (sys.stdout, sys.stderr):
        reconf = getattr(stream, "reconfigure", None)
        if reconf is not None:
            try:
                reconf(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass

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
        "--wipe-only",
        action="store_true",
        help="DETACH DELETE all nodes and relationships, then exit (no CSV import). "
        "Requires --confirm-wipe. Does not read node_inventory or edges.",
    )
    ap.add_argument(
        "--confirm-wipe",
        action="store_true",
        help="Required together with --wipe or --wipe-only.",
    )
    ap.add_argument("--batch-size", type=int, default=400)
    ap.add_argument(
        "--entities",
        nargs="+",
        metavar="ENTITY",
        help="Only import inventory rows whose `entity` column is in this list (e.g. material ort akteur).",
    )
    ap.add_argument(
        "--password-file",
        type=Path,
        default=None,
        help="Read Neo4j password from the first non-empty line of this file (UTF-8). "
        "Skipped if NEO4J_PASSWORD is already set.",
    )
    args = ap.parse_args()

    if args.nodes_only and args.edges_only:
        print("Choose at most one of --nodes-only / --edges-only", file=sys.stderr)
        return 1
    if args.wipe and args.wipe_only:
        print("Choose at most one of --wipe / --wipe-only", file=sys.stderr)
        return 1
    if args.wipe and not args.confirm_wipe:
        print("Refusing --wipe without --confirm-wipe", file=sys.stderr)
        return 1
    if args.wipe_only and not args.confirm_wipe:
        print("Refusing --wipe-only without --confirm-wipe", file=sys.stderr)
        return 1
    if args.wipe_only and (args.nodes_only or args.edges_only):
        print("--wipe-only cannot be combined with --nodes-only / --edges-only", file=sys.stderr)
        return 1

    base: Path = args.database_dir
    inv_path = base / "_system" / "node_inventory.csv"
    edge_path = base / "_edges" / "clean_confirmed_edges.csv"
    if not args.wipe_only:
        if not inv_path.is_file():
            print(f"Missing {inv_path}", file=sys.stderr)
            return 1
        if not args.nodes_only and not edge_path.is_file():
            print(f"Missing {edge_path}", file=sys.stderr)
            return 1

    password = (os.environ.get("NEO4J_PASSWORD") or "").strip()
    if not password and args.password_file is not None:
        if not args.password_file.is_file():
            print(f"--password-file not found: {args.password_file}", file=sys.stderr)
            return 1
        for line in args.password_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                password = line
                break
    if not password:
        print(
            "NEO4J_PASSWORD is not set. Export it in the shell or pass --password-file <path> "
            "(first non-empty, non-# line).",
            file=sys.stderr,
        )
        return 1
    uri = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
    user = (os.environ.get("NEO4J_USER") or os.environ.get("NEO4J_USERNAME") or "neo4j").strip()
    database = (os.environ.get("NEO4J_DATABASE") or "neo4j").strip() or "neo4j"

    try:
        from neo4j import GraphDatabase
    except ImportError:
        print("Install the driver: pip install -r requirements-neo4j.txt", file=sys.stderr)
        return 1

    inv_rows: list[dict[str, str]] = []
    if not args.wipe_only:
        inv_rows = load_inventory_rows(inv_path)
        entities_in_file = {r["entity"] for r in inv_rows}
        allowed_entities = (
            set(ENTITY_LABEL.keys())
            | {"ort", "akteur", "software_digitaltool", "datenmodell", "tooltyp"}
            | SKIP_NODE_ENTITIES
        )
        missing_map = entities_in_file - allowed_entities
        if missing_map:
            print(
                f"node_inventory.csv uses unknown entities (add ENTITY_LABEL): {sorted(missing_map)}",
                file=sys.stderr,
            )
            return 1

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        print(f"Connected {uri}  database=`{database}`")

        def session():
            return driver.session(database=database)

        with session() as sess:
            if args.wipe or args.wipe_only:
                sess.execute_write(wipe_graph)
                print("Wiped graph (all nodes and relationships removed).")

            if args.wipe_only:
                rec = sess.run("MATCH (n) RETURN count(n) AS c").single()
                relc = sess.run("MATCH ()-[r]->() RETURN count(r) AS c").single()
                print(f"Totals now: {rec['c']} nodes, {relc['c']} relationships.")
                print("Done (wipe-only).")
                return 0

            if not args.edges_only:
                by_label: dict[str, list[dict]] = defaultdict(list)
                skipped_dm = 0
                skipped_tt = 0
                skipped_plan = 0
                skipped_fuegung = 0
                for row in inv_rows:
                    ent = row["entity"]
                    if args.entities and ent not in args.entities:
                        continue
                    if ent in SKIP_NODE_ENTITIES:
                        skipped_plan += 1
                        continue
                    if ent == "datenmodell":
                        skipped_dm += 1
                        continue
                    if ent == "tooltyp":
                        skipped_tt += 1
                        continue
                    if ent == "fuegung_verbindung" and row["id"] == "Reversible_Fuegung":
                        skipped_fuegung += 1
                        continue
                    lab = label_for_inventory_row(row, base)
                    tp = row["typed_path"]
                    props = row_to_node_props(row, lab)
                    by_label[lab].append({"typed_path": tp, "props": props})

                for lab, rows in sorted(by_label.items(), key=lambda x: x[0]):
                    for i in range(0, len(rows), args.batch_size):
                        chunk = rows[i : i + args.batch_size]
                        sess.execute_write(merge_nodes_batch, lab, chunk)
                    print(f"  Nodes :{lab}  count={len(rows)}")

                print(
                    f"Imported {sum(len(v) for v in by_label.values())} nodes "
                    f"(skipped datenmodell={skipped_dm}, tooltyp={skipped_tt}, "
                    f"plan_dropped_entities={skipped_plan}, reversible_fuegung={skipped_fuegung})."
                )

            if not args.nodes_only:
                edge_rows = load_edge_rows(edge_path)
                skipped_edges = 0
                skipped_fold = 0
                by_rel: dict[str, list[dict]] = defaultdict(list)
                for row in edge_rows:
                    if row["source_entity"] == "datenmodell" or row["target_entity"] == "datenmodell":
                        skipped_edges += 1
                        continue
                    if row["source_entity"] == "tooltyp" or row["target_entity"] == "tooltyp":
                        skipped_edges += 1
                        continue
                    if (
                        row["source_entity"] in SKIP_NODE_ENTITIES
                        or row["target_entity"] in SKIP_NODE_ENTITIES
                    ):
                        skipped_edges += 1
                        continue
                    if (
                        row["source"] == "fuegung_verbindung/Reversible_Fuegung"
                        or row["target"] == "fuegung_verbindung/Reversible_Fuegung"
                    ):
                        skipped_edges += 1
                        continue
                    neo_rel, fold_props = fold_csv_relation(row)
                    if neo_rel is None:
                        skipped_fold += 1
                        continue
                    props = row_to_rel_props(row)
                    props.update(fold_props)
                    by_rel[neo_rel].append(
                        {
                            "source": row["source"],
                            "target": row["target"],
                            "props": props,
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
                    f"(skipped {skipped_edges} datenmodell / tooltyp / skip-entities / reversible_fuegung; "
                    f"skipped {skipped_fold} folded-away CSV rows)."
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
