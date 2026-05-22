"""Export the main :Projekt list and key project mappings from live Neo4j.

The live graph is the source of truth. This script performs read-only queries
against the configured Neo4j database and writes compact export artefacts:

- main_projects.csv: one ranked row per project with summarized mappings
- project_actor_country_mappings.csv: one row per project-actor edge
- project_mapping_type_counts.csv: relationship-type coverage around projects
- main_projects.json: structured equivalent of the CSV summaries
- README.md: short human-readable report
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402


DEFAULT_OUT_DIR = REPO / "_neo4j" / "exports" / "2026-06-06_main_project_mappings"

MAPPINGS = [
    ("countries", "LIEGT_IN_LAND", "Land"),
    ("cities", "LIEGT_IN_STADT", "Stadt"),
    ("actors", "BETEILIGT_AN", "Akteur"),
    ("programs", "TEIL_VON_PROGRAMM", "Programm"),
    ("funding_programs", "ERHALT_FOERDERUNG_DURCH", "Programm"),
    ("buildings", "HAT_BAUWERK", "Bauwerk"),
    ("component_groups", "HAT_BAUTEILGRUPPE", "Bauteilgruppe"),
    ("component_types", "HAT_BAUTEILTYP", "Bauteiltyp"),
    ("materials", "NUTZT_MATERIAL", "Material"),
    ("methods", "HAT_METHODE", "Methode"),
    ("design_methods", "HAT_ENTWURFSMETHODIK", "Entwurfsmethodik"),
    ("architecture_results", "HAT_ARCHITEKTURERGEBNIS", "Architekturergebnis"),
    ("process_phases", "HAT_PROZESSPHASE", "Prozessphase"),
    ("uses", "HAT_NUTZUNG", "Nutzung"),
    ("procurement_paths", "HAT_BESCHAFFUNGSWEG", "Beschaffungsweg"),
    ("logistics", "HAT_LOGISTIK", "Logistik"),
    ("barriers", "HAT_HUERDE", "Huerde"),
    ("evidence_requirements", "ERFORDERT_NACHWEIS", "Nachweisforderung"),
    ("regulatory_questions", "TRIGGERS_REGULIERUNGSFRAGE", "Regulierungsfrage"),
    ("pollutants", "ERFORDERT_SCHADSTOFFPRUEFUNG", "Schadstoff"),
    ("software", "NUTZT_SOFTWARE", "Software"),
]

SUMMARY_COLUMNS = [
    "rank",
    "project_id",
    "project_name",
    "project_full_name",
    "status",
    "year_completed",
    "degree",
    "country_count",
    "countries",
    "city_count",
    "cities",
    "actor_count",
    "actors",
    "program_count",
    "programs",
    "building_count",
    "buildings",
    "component_group_count",
    "component_groups",
    "component_type_count",
    "component_types",
    "material_count",
    "materials",
    "method_count",
    "methods",
    "process_phase_count",
    "process_phases",
    "use_count",
    "uses",
    "procurement_path_count",
    "procurement_paths",
    "barrier_count",
    "barriers",
    "software_count",
    "software",
    "primary_source_url",
    "source_urls",
]


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (list, tuple)):
        return [to_jsonable(v) for v in value]
    if hasattr(value, "iso_format"):
        return value.iso_format()
    return str(value)


def clean_scalar(value: Any) -> str:
    value = to_jsonable(value)
    if value is None:
        return ""
    if isinstance(value, list):
        return "; ".join(str(v) for v in value if v not in (None, ""))
    return str(value)


def sort_names(values: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen = {}
    for item in values:
        key = item.get("id") or item.get("name") or json.dumps(item, sort_keys=True)
        seen[key] = item
    return sorted(seen.values(), key=lambda x: ((x.get("name") or "").casefold(), x.get("id") or ""))


def names_join(values: list[dict[str, Any]]) -> str:
    names = [v.get("name") or v.get("id") for v in sort_names(values)]
    return "; ".join(v for v in names if v)


def run_export(out_dir: Path) -> dict[str, Any]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")

    exported_at = datetime.now(timezone.utc).isoformat()
    projects: dict[str, dict[str, Any]] = {}
    actor_rows: list[dict[str, Any]] = []
    mapping_counts: list[dict[str, Any]] = []

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as session:
            graph_counts = session.run(
                "MATCH (n) "
                "WITH count(n) AS nodes "
                "MATCH ()-[r]->() "
                "RETURN nodes, count(r) AS relationships"
            ).single()
            retired = session.run(
                "OPTIONAL MATCH (q:Quelle) "
                "WITH count(q) AS quelle "
                "OPTIONAL MATCH (s:Status) "
                "WITH quelle, count(s) AS status "
                "RETURN quelle, 0 AS regelwerk, status"
            ).single()

            project_rows = session.run(
                "MATCH (p:Projekt) "
                "OPTIONAL MATCH (p)-[r]-() "
                "WITH p, count(r) AS degree "
                "RETURN p.id AS id, p.name AS name, properties(p) AS props, degree "
                "ORDER BY degree DESC, coalesce(p.name, p.id)"
            )
            for idx, row in enumerate(project_rows, start=1):
                props = {k: to_jsonable(v) for k, v in dict(row["props"]).items()}
                pid = row["id"]
                projects[pid] = {
                    "rank": idx,
                    "project_id": pid,
                    "project_name": row["name"] or pid,
                    "project_full_name": props.get("name_full") or "",
                    "status": props.get("status") or props.get("projektstatus_text") or "",
                    "year_completed": props.get("year_completed") or "",
                    "degree": row["degree"],
                    "primary_source_url": props.get("primary_source_url") or "",
                    "source_urls": props.get("source_urls") or [],
                    "mappings": defaultdict(list),
                }

            for field, rel_type, label in MAPPINGS:
                rows = session.run(
                    f"MATCH (p:Projekt)-[r:{rel_type}]-(n:{label}) "
                    "RETURN p.id AS project_id, n.id AS id, n.name AS name, "
                    "properties(r) AS rel_props "
                    "ORDER BY project_id, coalesce(n.name, n.id)"
                )
                edge_count = 0
                project_ids = set()
                for row in rows:
                    pid = row["project_id"]
                    if pid not in projects:
                        continue
                    edge_count += 1
                    project_ids.add(pid)
                    item = {
                        "id": row["id"],
                        "name": row["name"] or row["id"],
                    }
                    rel_props = {k: to_jsonable(v) for k, v in dict(row["rel_props"]).items()}
                    if rel_props:
                        item["rel_props"] = rel_props
                    projects[pid]["mappings"][field].append(item)
                mapping_counts.append(
                    {
                        "field": field,
                        "relationship_type": rel_type,
                        "target_label": label,
                        "edge_count": edge_count,
                        "project_count": len(project_ids),
                    }
                )

            rows = session.run(
                "MATCH (a:Akteur)-[r:BETEILIGT_AN]-(p:Projekt) "
                "OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]-(l:Land) "
                "WITH p, a, r, collect(DISTINCT coalesce(l.name, l.id)) AS countries "
                "RETURN p.id AS project_id, p.name AS project_name, "
                "countries, a.id AS actor_id, a.name AS actor_name, "
                "properties(r) AS rel_props "
                "ORDER BY coalesce(p.name, p.id), coalesce(a.name, a.id)"
            )
            for row in rows:
                rel_props = {k: to_jsonable(v) for k, v in dict(row["rel_props"]).items()}
                actor_rows.append(
                    {
                        "project_id": row["project_id"],
                        "project_name": row["project_name"] or row["project_id"],
                        "countries": "; ".join(sorted(v for v in row["countries"] if v)),
                        "actor_id": row["actor_id"],
                        "actor_name": row["actor_name"] or row["actor_id"],
                        "role_text": rel_props.get("rolle_text") or rel_props.get("role") or "",
                        "relationship_id": rel_props.get("id") or "",
                        "evidence_url": rel_props.get("evidence_url") or rel_props.get("source_url") or "",
                        "evidence_confidence": rel_props.get("evidence_confidence")
                        or rel_props.get("confidence")
                        or "",
                        "review_run": rel_props.get("review_run") or "",
                    }
                )

    out_dir.mkdir(parents=True, exist_ok=True)

    summary_rows = []
    json_projects = []
    for project in sorted(projects.values(), key=lambda p: p["rank"]):
        mappings = {k: sort_names(list(v)) for k, v in project["mappings"].items()}
        for field, _, _ in MAPPINGS:
            mappings.setdefault(field, [])

        row = {
            "rank": project["rank"],
            "project_id": project["project_id"],
            "project_name": project["project_name"],
            "project_full_name": project["project_full_name"],
            "status": clean_scalar(project["status"]),
            "year_completed": clean_scalar(project["year_completed"]),
            "degree": project["degree"],
            "country_count": len(mappings["countries"]),
            "countries": names_join(mappings["countries"]),
            "city_count": len(mappings["cities"]),
            "cities": names_join(mappings["cities"]),
            "actor_count": len(mappings["actors"]),
            "actors": names_join(mappings["actors"]),
            "program_count": len(mappings["programs"]) + len(mappings["funding_programs"]),
            "programs": "; ".join(
                v for v in [names_join(mappings["programs"]), names_join(mappings["funding_programs"])] if v
            ),
            "building_count": len(mappings["buildings"]),
            "buildings": names_join(mappings["buildings"]),
            "component_group_count": len(mappings["component_groups"]),
            "component_groups": names_join(mappings["component_groups"]),
            "component_type_count": len(mappings["component_types"]),
            "component_types": names_join(mappings["component_types"]),
            "material_count": len(mappings["materials"]),
            "materials": names_join(mappings["materials"]),
            "method_count": len(mappings["methods"]),
            "methods": names_join(mappings["methods"]),
            "process_phase_count": len(mappings["process_phases"]),
            "process_phases": names_join(mappings["process_phases"]),
            "use_count": len(mappings["uses"]),
            "uses": names_join(mappings["uses"]),
            "procurement_path_count": len(mappings["procurement_paths"]),
            "procurement_paths": names_join(mappings["procurement_paths"]),
            "barrier_count": len(mappings["barriers"]),
            "barriers": names_join(mappings["barriers"]),
            "software_count": len(mappings["software"]),
            "software": names_join(mappings["software"]),
            "primary_source_url": clean_scalar(project["primary_source_url"]),
            "source_urls": clean_scalar(project["source_urls"]),
        }
        summary_rows.append(row)
        json_projects.append(
            {
                **{k: project[k] for k in [
                    "rank",
                    "project_id",
                    "project_name",
                    "project_full_name",
                    "status",
                    "year_completed",
                    "degree",
                    "primary_source_url",
                    "source_urls",
                ]},
                "mappings": mappings,
            }
        )

    with (out_dir / "main_projects.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        writer.writerows(summary_rows)

    actor_columns = [
        "project_id",
        "project_name",
        "countries",
        "actor_id",
        "actor_name",
        "role_text",
        "relationship_id",
        "evidence_url",
        "evidence_confidence",
        "review_run",
    ]
    with (out_dir / "project_actor_country_mappings.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=actor_columns)
        writer.writeheader()
        writer.writerows(actor_rows)

    with (out_dir / "project_mapping_type_counts.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["field", "relationship_type", "target_label", "edge_count", "project_count"],
        )
        writer.writeheader()
        writer.writerows(mapping_counts)

    metadata = {
        "exported_at": exported_at,
        "database": database,
        "source_of_truth": "live Neo4j graph",
        "graph_counts": dict(graph_counts),
        "retired_label_checks": dict(retired),
        "project_count": len(projects),
        "actor_country_mapping_rows": len(actor_rows),
        "mapping_counts": mapping_counts,
    }
    (out_dir / "main_projects.json").write_text(
        json.dumps({"metadata": metadata, "projects": json_projects}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    top_rows = summary_rows[:30]
    lines = [
        "# Main Project Mappings Export",
        "",
        f"- Generated: `{exported_at}`",
        f"- Database: `{database}`",
        "- Source of truth: live Neo4j graph",
        f"- Graph counts: `{graph_counts['nodes']}` nodes / `{graph_counts['relationships']}` relationships",
        (
            "- Retired label checks: "
            f"`Quelle={retired['quelle']}`, `Regelwerk={retired['regelwerk']}`, `Status={retired['status']}`"
        ),
        f"- Projects exported: `{len(projects)}`",
        f"- Project-actor-country rows: `{len(actor_rows)}`",
        "",
        "## Files",
        "",
        "| File | Meaning |",
        "| --- | --- |",
        "| `main_projects.csv` | Ranked project list with summarized key mappings. |",
        "| `project_actor_country_mappings.csv` | Detailed project-to-actor rows with country context and evidence properties where present. |",
        "| `project_mapping_type_counts.csv` | Coverage counts for mapping relationship types around projects. |",
        "| `main_projects.json` | Structured export with full mapping lists. |",
        "",
        "## Top Projects By Graph Degree",
        "",
        "| Rank | Project | Countries | Actors | Components | Materials | Degree |",
        "| ---: | --- | --- | ---: | ---: | ---: | ---: |",
    ]
    for row in top_rows:
        lines.append(
            "| {rank} | {project_name} | {countries} | {actor_count} | "
            "{component_group_count} | {material_count} | {degree} |".format(**row)
        )
    lines.extend(
        [
            "",
            "## Mapping Coverage",
            "",
            "| Field | Relationship | Target | Edges | Projects |",
            "| --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in sorted(mapping_counts, key=lambda r: (-r["edge_count"], r["field"])):
        lines.append(
            f"| {row['field']} | `{row['relationship_type']}` | `{row['target_label']}` | "
            f"{row['edge_count']} | {row['project_count']} |"
        )
    (out_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()
    metadata = run_export(args.out_dir)
    print(f"Wrote export to {args.out_dir}")
    print(f"Database: {metadata['database']}")
    print(
        "Graph counts: "
        f"{metadata['graph_counts']['nodes']} nodes / "
        f"{metadata['graph_counts']['relationships']} relationships"
    )
    print(f"Projects: {metadata['project_count']}")
    print(f"Project-actor-country rows: {metadata['actor_country_mapping_rows']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
