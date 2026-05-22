"""F06: export live property keys and write final_cleanup_f06.csv (read-only Neo4j)."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[3]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
LEDGER = OUT / "ledger" / "final_cleanup_f06.csv"

APPROVED_NODE = {
    "id", "name", "name_full", "aliases", "beschreibung", "short_description", "category", "kind", "type",
    "status", "confidence", "created_at", "source_url", "source_urls", "source_titles", "source_quote",
    "evidence_basis", "rechtsbereiche", "reguliert_in_laendern", "reuse_status", "standards_body",
    "wirtschaft", "wirtschaft_aspekte", "akzeptanzfaktoren", "bauobjektklasse", "bauproduktstatus",
    "bauteilebene", "bg_kind", "bilanzgrenze", "brand_layer", "einheit", "fact_index", "funktionswechsel",
    "kennwert", "layer", "lca_modules", "maps_to_nachweisforderung", "method", "matchingqualitaet_geo",
    "matchingqualitaet_spec", "matchingqualitaet_temporal", "nutzung_text", "projektstatus_text", "tragend",
    "tragwerksprinzip", "typische_bauproduktstatus", "wert", "wert_text", "wiederverwendungsort",
    "year_completed", "year_from", "year_to", "zertifizierungssysteme", "alte_funktion", "neue_funktion",
    "area_m2_gross",
}

APPROVED_REL = {
    "id", "confidence", "created_at_utc", "updated_at_utc", "aktualisiert_am_utc", "source_url",
    "source_quote", "evidence_url", "evidence_quote", "evidence_confidence", "evidence_basis",
    "review_run", "metadata_sidecar_key", "intake_run", "role", "rolle_text", "scope_note",
    "semantic_basis", "rechtsgrundlage", "pollutant_basis", "bauteilgruppe_id", "bauteilgruppe_name",
    "actor_id", "actor_name", "basis",
}

DRIFT_NODE = {
    "adresse", "latitude", "longitude", "geo_aktualisiert_am_utc", "geo_confidence", "geo_import_run",
    "country_iso2", "entwurfsbeschreibung", "entwurfsbeschreibung_quelle", "entwurfsqualitaet_am_utc",
    "entwurfsqualitaet_run", "entwurfsqualitaet_vokabular_version", "name_de", "literature_ref",
    "vokabular_version", "intake_run", "deprecated_am_utc", "deprecated_reason", "aktualisiert_am_utc",
    "metadata_sidecar_key", "primary_source_url", "review_run",
}

DRIFT_REL = {
    "connection_kind", "dedup_run", "dedupe_key", "dossier_section", "evidence_excerpt", "evidence_origin",
    "fact_label", "inference_basis", "integration_layer", "integration_phase", "basis_project_edge_id",
    "basis_project_edge_type", "begruendung", "belegkonfidenz", "extraktionsstatus", "kandidatentext",
    "quell_urls", "vokabular_version", "zuordnung_pruefung", "zuordnung_quelle", "reversibility",
    "shared_bauteiltyp_ids", "shared_material_ids", "source_scope", "review_status",
}

DEPRECATE_NODE = {"review_status", "source_scope", "land"}


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    rows: list[dict] = []

    with driver.session(database=database) as session:
        node_keys = {
            r["key"]: r["occ"]
            for r in session.run(
                "MATCH (n) UNWIND keys(n) AS k RETURN k AS key, count(*) AS occ ORDER BY key"
            )
        }
        rel_keys = {
            r["key"]: r["occ"]
            for r in session.run(
                "MATCH ()-[r]->() UNWIND keys(r) AS k RETURN k AS key, count(*) AS occ ORDER BY key"
            )
        }

    driver.close()

    for key in sorted(node_keys):
        if key in DEPRECATE_NODE:
            verdict, reason = "DEPRECATE", "legacy/redundant; A14-LAND-001 / sidecar backlog"
        elif key in DRIFT_NODE:
            verdict, reason = "DOCUMENT_DRIFT", "intentional post-2026-06-05 intake"
        elif key in APPROVED_NODE:
            verdict, reason = "KEEP", "approved manifest 2026-06-05 phase 8"
        else:
            verdict, reason = "DOCUMENT_DRIFT", "live-only post-P6; re-baseline candidate"
        rows.append(
            {
                "claim_id": f"F06-NK-{key}",
                "scope": "node",
                "property_key": key,
                "occurrences": node_keys[key],
                "approved_baseline": "yes" if key in APPROVED_NODE else "no",
                "verdict": verdict,
                "agent_id": "F06",
                "notes": reason,
            }
        )

    for key in sorted(rel_keys):
        if key in DRIFT_REL:
            verdict, reason = "DOCUMENT_DRIFT", "intentional post-P6 (reuse / entwurfsqualitaet / dedup)"
        elif key in APPROVED_REL:
            verdict, reason = "KEEP", "approved manifest 2026-06-05 phase 8"
        else:
            verdict, reason = "DOCUMENT_DRIFT", "live-only post-P6; re-baseline candidate"
        rows.append(
            {
                "claim_id": f"F06-RK-{key}",
                "scope": "rel",
                "property_key": key,
                "occurrences": rel_keys[key],
                "approved_baseline": "yes" if key in APPROVED_REL else "no",
                "verdict": verdict,
                "agent_id": "F06",
                "notes": reason,
            }
        )

    fieldnames = [
        "claim_id", "scope", "property_key", "occurrences", "approved_baseline",
        "verdict", "agent_id", "notes",
    ]
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(json.dumps({"ledger_rows": len(rows), "node_keys": len(node_keys), "rel_keys": len(rel_keys)}, indent=2))


if __name__ == "__main__":
    main()
