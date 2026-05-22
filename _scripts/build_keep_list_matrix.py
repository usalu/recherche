"""Build the per-node-label keep-list decision matrix for the extreme
property-minimization goal (target ~4 properties per label).

Read-only: consumes the minimal-property audit CSV and emits a complete
decision matrix (CSV + Markdown). Every label/property pair gets exactly one
verdict so the matrix can later drive patch generation.

Verdicts:
  keep_core            id / name (identity + human caption)
  keep_semantic        domain property that survives (counts to the budget)
  drop                 bookkeeping / cache / provenance already on edges -> safe remove
  migrate_then_drop    provenance is the ONLY copy (no BELEGT_IN) -> migrate first
  move_to_relationship topology duplicate w/ full edge coverage -> remove after confirm
  migrate_edge_then_drop topology duplicate w/ gaps -> create missing edges, then remove
  meta_separate        audit/meta label handled as its own decision (DataIssue etc.)

Usage:
  python _scripts/build_keep_list_matrix.py \
      --audit-dir _neo4j/review/2026-06-01_minimal_property_audit_current_mit-bestand
"""

from __future__ import annotations

import argparse
import csv
import collections
from pathlib import Path

# ---- Label groups -----------------------------------------------------------

META_LABELS = {"DataIssue", "DossierEntityTarget", "DeprecatedType", "ReuseRule", "OntologyAnchor"}
SOURCE_LABELS = {"Quelle", "ExternalLink", "ResearchDocument", "SectionRef", "Dossier"}

# Properties kept as identity / human caption everywhere.
CORE = {"id", "name"}

# Labels whose reason-to-exist IS their attribute set (facts / reference data):
# they are allowed to exceed 4 survivors and keep their semantic fields.
JUSTIFIED_OVER_BUDGET = {"Kennwert", "Land", "BauwerkEra", "Geltungsbereich", "LCAModule", "Norm"}

# Per-label CORE semantic properties that survive (count toward the budget).
# Surplus domain fields not listed here fall to `domain_review` (you decide).
SEMANTIC = {
    # rich entities -> tight core; the rest -> domain_review
    "Bauteilgruppe": {"bg_kind", "reuse_status"},
    "Projekt": {"name_full", "year_completed"},
    "Programm": {"name_full", "type"},
    "Bauwerk": {"name_full", "nutzung_text"},
    "Materialdepot": {"name_full", "nutzung_text"},
    "Software": {"kind"},
    "Tool": {"kind"},
    "Wiederverwendungskette": {"name_full"},
    "RechtlicheBedingung": {"is_universal"},
    "Schadstoff": {"standards_body"},
    "Zertifizierungssystem": {"scheme_kind"},
    "Beschaffungsweg": {"beschreibung"},
    "Ressourcenquelle": {"beschreibung"},
    "Bausystem": {"definition"},
    "Status": {"kind"},
    "WiederverwendungsArt": {"facet"},
    "Bauteiltyp": {"brand_layer"},
    "Layer": {"brand_position"},
    # justified fact / reference labels keep their full attribute set
    "Kennwert": {"kennwert", "wert", "wert_text", "einheit", "category", "method", "bilanzgrenze", "fact_index"},
    "Land": {"country_iso2", "asbest_verbot_jahr", "pcb_verbot_jahr", "kmf_grenzwert_jahr"},
    "BauwerkEra": {"year_from", "year_to"},
    "LCAModule": {"en15978_code"},
    "Geltungsbereich": {"scope_system", "scope_type"},
    "Norm": {"name_full", "country_short"},
}
# scope_note kept wherever it carries a real definition (most vocab labels).
SCOPE_NOTE_KEEP_DEFAULT = True
# name_full kept where present and distinct, but only counts if the label is
# in this set (otherwise treated as drop to protect the budget).
NAME_FULL_KEEP = {
    "Bauproduktstatus", "Akzeptanz", "MatchingQualitaet", "ZustandsKlasse",
    "Marktmodell", "Defekt", "Projekt", "Programm", "Bauwerk", "Materialdepot",
    "Norm", "Wiederverwendungskette",
}

# Source layer keep-list (provenance node identity + locator).
SOURCE_KEEP = {
    "Quelle": {"id", "url", "quelltyp", "title"},
    "ExternalLink": {"id", "url", "quelltyp", "title"},
    "ResearchDocument": {"id", "name", "quelltyp", "source_file"},
    "SectionRef": {"id", "name", "url"},
    "Dossier": {"id", "name", "quelltyp"},
}

# Source layer: source_file kept only for these (research provenance identity).
SOURCE_FILE_KEEP_LABELS = {"ResearchDocument", "OntologyAnchor"}

# Topology duplicates with full edge coverage -> drop after confirm.
MOVE_TO_REL = {("Bauteilgruppe", "primary_bauteiltyp_id")}
# Topology duplicates with edge gaps -> create edges first.
MIGRATE_EDGE = {("Bauteilgruppe", "primary_material_id"), ("Akteur", "land"),
                ("Bauwerk", "land"), ("Materialdepot", "land")}
# Provenance with no BELEGT_IN coverage -> migrate then drop.
MIGRATE_PROV_LABELS = {"Kennwert", "Norm"}

# Global bookkeeping/provenance/cache drop rules (apply to all non-meta labels).
DROP_EXACT = {
    "source_scope", "source_resolution_status", "source_freshness_summary",
    "source_quality_summary", "source_trust_score", "source_count",
    "source_url", "source_urls", "primary_source_url", "source_url_node_ids",
    "invalid_candidate_source_urls", "invalid_source_url",
    "strict_source_url_cleanup", "strict_invalid_url_cleanup",
    "strict_candidate_url_array_cleanup", "strict_node_url_array_cleanup",
    "review_status", "review_run", "repair_phase", "repaired_at",
    "text_content_chars_pre_strip", "text_content_retry_result",
    "text_content_loaded_at", "text_content_stripped_at",
    "text_content_retry_attempted_at", "access_date", "migration_origin",
    "actor_registry_loader_seen", "actor_registry_order",
    "actor_registry_mentioned", "_archive", "_created_at", "_created_by",
    "created_at", "created_by", "last_seen_by", "extracted_at", "loader",
    "node_role", "original_label", "import_status",
    "needs_project_file", "needs_dossier_extraction", "classified_reason",
    "source_id",
}
DROP_PREFIX = ("url_", "source_trace_", "evidence_", "quality_tier",
               "legal_condition", "demoted_legal_condition", "candidate_source_",
               "co2_facts", "cost_facts", "reuse_share_facts", "raw_role_evidence")
# url itself is kept on source nodes (handled before prefix check).


# Semantic decisions for the surplus domain fields (user-directed pass):
# keep only meaningful, human-readable content / genuine entity attributes.
DOMAIN_KEEP = {
    ("Akteurrolle", "aliases"), ("Akteurtyp", "aliases"), ("Status", "aliases"),
    ("Land", "aliases"), ("Programm", "aliases"),
    ("Bauteilgruppe", "alte_funktion"), ("Bauteilgruppe", "neue_funktion"),
    ("Bauteilgruppe", "tragend"),
    ("BauwerkEra", "notes"),
    ("Land", "asbest_neshap_year"), ("Land", "asbest_note"),
    ("Programm", "short_description"),
    ("Projekt", "area_m2_gross"), ("Projekt", "nutzung_text"),
    ("Projekt", "projektstatus_text"),
}


def verdict_for(label: str, prop: str, coverage: float) -> tuple[str, str]:
    lower = prop.lower()

    if label in META_LABELS:
        if prop in ("id", "name"):
            return "keep_core", "identity (meta label, separate decision)"
        return "meta_separate", "audit/meta label; handled in the meta-node decision"

    # Source layer has its own keep-list.
    if label in SOURCE_LABELS:
        keep = SOURCE_KEEP.get(label, {"id", "name", "url", "quelltyp"})
        if prop in keep:
            tag = "keep_core" if prop in CORE else "keep_semantic"
            return tag, "source identity / retrieval locator"
        if prop == "name" and prop not in keep:
            return "drop", "redundant with title"
        return "drop", "source/url probe/cache/provenance bookkeeping (re-derivable)"

    # Identity + caption everywhere.
    if prop == "id":
        return "keep_core", "identity handle (constraint-backed)"
    if prop == "name":
        return "keep_core", "human caption"

    # Topology-duplicate handling.
    if (label, prop) in MOVE_TO_REL:
        return "move_to_relationship", "full edge coverage confirmed; drop after re-confirm"
    if (label, prop) in MIGRATE_EDGE:
        return "migrate_edge_then_drop", "edge gaps exist; create missing edges first"

    # scope_note: keep where it is a real definition.
    if prop == "scope_note":
        if SCOPE_NOTE_KEEP_DEFAULT and coverage >= 5:
            return "keep_semantic", "controlled-vocabulary definition"
        return "drop", "sparse scope_note"
    if prop == "name_full":
        if label in NAME_FULL_KEEP or label in SEMANTIC and "name_full" in SEMANTIC.get(label, set()):
            return "keep_semantic", "distinct full caption"
        return "drop", "redundant with name (protect budget)"

    # Per-label semantic keep set.
    if prop in SEMANTIC.get(label, set()):
        # provenance-bearing exceptions are not in SEMANTIC, so this is domain.
        return "keep_semantic", "domain-essential value for this label"

    # Provenance-only labels: their source_* must be migrated, not dropped blind.
    if label in MIGRATE_PROV_LABELS and (
        prop in {"source_id", "source_urls", "source_url", "primary_source_url"}
        or lower.startswith("evidence_")
    ):
        return "migrate_then_drop", "only provenance copy (no BELEGT_IN); migrate to edges first"

    # Global drop rules.
    if prop in DROP_EXACT:
        return "drop", "bookkeeping/provenance already on edges or re-derivable"
    if lower.startswith(DROP_PREFIX):
        return "drop", "generated/provenance/cache/derived metadata"

    # Semantic decision on surplus domain fields (human-readable target).
    if (label, prop) in DOMAIN_KEEP:
        return "keep_semantic", "meaningful human-readable domain content (semantic pass)"
    if coverage < 5:
        return "drop", "sparse residue (<5% coverage); verify no unique value"
    return "drop", "machine flag/code/derived/relational-better field (semantic pass)"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit-dir", type=Path, required=True)
    args = ap.parse_args()

    src = args.audit_dir / "node_property_minimization.csv"
    rows = list(csv.DictReader(open(src, encoding="utf-8")))

    out_rows = []
    per_label = collections.defaultdict(lambda: collections.Counter())
    keep_props = collections.defaultdict(list)
    counts = {}
    for r in rows:
        label = r["group"]
        prop = r["property"]
        cov = float(r["coverage_pct"])
        counts[label] = int(r["total_in_group"])
        verdict, reason = verdict_for(label, prop, cov)
        per_label[label][verdict] += 1
        if verdict in ("keep_core", "keep_semantic"):
            keep_props[label].append(prop)
        out_rows.append({
            "label": label,
            "property": prop,
            "nodes": counts[label],
            "coverage_pct": r["coverage_pct"],
            "types": r["types"],
            "verdict": verdict,
            "reason": reason,
            "sample": (r["sample_values"] or "")[:80].replace("\n", " "),
        })

    # Write matrix CSV.
    fields = ["label", "property", "nodes", "coverage_pct", "types", "verdict", "reason", "sample"]
    with open(args.audit_dir / "KEEP_LIST_DECISION_MATRIX.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(out_rows, key=lambda x: (-x["nodes"], x["label"], x["property"])))

    # Markdown summary: per-label keep count + budget flag.
    review_props = collections.defaultdict(list)
    for r in out_rows:
        if r["verdict"] == "domain_review":
            review_props[r["label"]].append(r["property"])

    md = ["# Keep-list decision matrix summary", "",
          "Target: ~4 properties per label. `keep_core`+`keep_semantic` = core survivors.",
          "`domain_review` = surplus domain fields you decide to keep or drop.",
          "Fact/reference labels may justifiably exceed 4.", "",
          "| Label | Nodes | Core survivors | Keep list | domain_review | Flag |",
          "|---|---:|---:|---|---|---|"]
    over = []
    for label in sorted(counts, key=lambda l: -counts[l]):
        ks = sorted(set(keep_props[label]))
        nkeep = len(ks)
        rv = sorted(set(review_props[label]))
        flag = ""
        if label in META_LABELS:
            flag = "meta (separate)"
        elif label in JUSTIFIED_OVER_BUDGET and nkeep > 4:
            flag = "justified (fact/reference)"
        elif nkeep > 4:
            flag = "OVER (trim)"
            over.append(label)
        md.append(
            f"| {label} | {counts[label]} | {nkeep} | "
            f"{', '.join('`'+k+'`' for k in ks)} | "
            f"{', '.join('`'+k+'`' for k in rv) if rv else '-'} | {flag} |"
        )

    md += ["", "## Verdict totals", "", "| Verdict | Pairs |", "|---|---:|"]
    tot = collections.Counter()
    for label in per_label:
        tot.update(per_label[label])
    for v, c in tot.most_common():
        md.append(f"| `{v}` | {c} |")
    md += ["", f"Labels over the 4-property budget: {', '.join(over) if over else 'none'}"]
    (args.audit_dir / "KEEP_LIST_DECISION_MATRIX_SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print("matrix rows:", len(out_rows))
    print("verdict totals:", dict(tot))
    print("labels over budget:", over)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
