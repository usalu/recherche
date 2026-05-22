"""
Phase 2 — Batch Markdown normalization + non-reuse-BG filter.

Reads:
  _neo4j/intake/inbox/research/new taxonomy edit/reuse_taxonomy_v9_connection_expansion_batch_*.md

Writes:
  _neo4j/intake/inbox/research/new taxonomy edit/_normalized/<filename>
      Normalized batch with rel-aliases, out-of-vocab target labels,
      and target node ids all mapped to the integration's canonical forms.
      Non-bg_reuse_ rows are removed.

  _neo4j/intake/inbox/research/new taxonomy edit/_filtered_non_reuse_bgs.md
      Every row that anchors on a non-bg_reuse_ Bauteilgruppe, preserved
      with its source batch + line context. For transparency / future
      reclassification under a non-:Bauteilgruppe label.

  _neo4j/review/2026-06-03_taxonomy_integration_plan/phase2_normalization_report.md
      Summary: counts per substitution kind, per filtered prefix, etc.

Originals are NEVER modified.
"""

from __future__ import annotations
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"E:/recherche")
BATCH_DIR = ROOT / "_neo4j/intake/inbox/research/new taxonomy edit"
NORMALIZED_DIR = BATCH_DIR / "_normalized"
FILTERED_FILE = BATCH_DIR / "_filtered_non_reuse_bgs.md"
PLAN_DIR = ROOT / "_neo4j/review/2026-06-03_taxonomy_integration_plan"
REPORT_FILE = PLAN_DIR / "phase2_normalization_report.md"

# ---------------------------------------------------------------------------
# Substitution rules
# ---------------------------------------------------------------------------

# Relationship-type aliases — old name in batches → canonical
REL_MAP = {
    "HAS_METHOD":         "HAT_METHODE",
    "HAS_SOURCE":         "HAT_RESSOURCENQUELLE",
    "HAS_LOCATION":       "HAT_WIEDERVERWENDUNGSORT",
    "HAS_PROCESSING":     "HAT_AUFBEREITUNG",
    "HAS_DISMANTLING":    "HAT_RUECKBAUVERFAHREN",
    "HAS_DECONSTRUCTION": "HAT_RUECKBAUVERFAHREN",
    "HAS_REUSE_RESULT":   "HAT_ERGEBNIS",
    "NUTZT_METHODE":      "HAT_METHODE",
    "HAT_QUELLE":         "HAT_RESSOURCENQUELLE",
}

# target_label column: batch label → canonical live label
TARGET_LABEL_MAP = {
    "Quelle": "Ressourcenquelle",
}

# Out-of-vocab target *names* that the coverage report flagged for normalization.
# These get rewritten in the canonical_taxonomy_target column AND in the target_node
# column (where they appear as the suffix after the q_/wo_/we_/av_/rv_ prefix).
CANONICAL_TARGET_MAP = {
    "Lokal_oder_Regional_importiert":          "Extern_importiert",
    "Sortierung_und_Bergung":                  "Zerstoerungsarme_Bergung",
    "Demontage_von_Modulen":                   "Demontage",
    "Rekonfiguration_und_Vormontage":          "Remanufacturing_und_Upcycling",
    "Zuschnitt_und_Anpassung":                 "Zuschnitt_und_Vereinzelung",
    "Keine_wesentliche_Aufbereitung":          "Pruefung_Sortierung_QS",
    "Auf_demselben_Areal":                     "Auf_demselben_Standort_versetzt",
    "Lager_und_Bauteilboerse":                 "Bauteilmarkt_oder_Lager",
    "Baustellenrest_oder_Ueberproduktion":     "Restposten_Abfall_Unbekannt",
    "Nicht_bestimmbar":                        "Restposten_Abfall_Unbekannt",
    "Design_for_Disassembly":                  "Reversibles_Design",
    # Dekonstruktion_mit_Inventar can be Rueckbau (Selektiver) or Methode
    # (Dokumentation_und_Monitoring). The choice depends on the relationship:
    # in HAT_RUECKBAUVERFAHREN rows it's Rueckbau; in HAT_METHODE rows it's Methode.
    # Handled below by rel-aware post-processing.
}

# Target-node id prefix rewrites — these turn the batch's draft ids into the
# integration's canonical id format.
ID_PREFIX_REWRITE_RULES = [
    # (old prefix, new prefix) ; applied only when the rest of the id is a known
    # canonical token. Lowercases the suffix.
    ("q_",  "rq_"),    # Quelle → Ressourcenquelle
    ("wo_", "wvo_"),   # Wiederverwendungsort
    ("we_", "wver_"),  # Wiederverwendungsergebnis
]

# New canonical methode ids (target_node values that should become meth_*)
METHODE_CANONICAL = {
    "Urban_Mining_und_Scouting":        "meth_urban_mining_und_scouting",
    "Bestands_und_ReUse_Assessment":    "meth_bestands_und_reuse_assessment",
    "Verfuegbarkeitsbasiertes_Design":  "meth_verfuegbarkeitsbasiertes_design",
    "Reversibles_Design":               "meth_reversibles_design",
    "Zirkulaere_Beschaffung":           "meth_zirkulaere_beschaffung",
    "Dokumentation_und_Monitoring":     "meth_dokumentation_und_monitoring",
}

# Aufbereitungsverfahren canonical
AUFBER_CANONICAL = {
    "Reinigung_und_Oberflaeche":        "av_reinigung_und_oberflaeche",
    "Zuschnitt_und_Vereinzelung":       "av_zuschnitt_und_vereinzelung",
    "Pruefung_Sortierung_QS":           "av_pruefung_sortierung_qs",
    "Reparatur_und_Refurbishment":      "av_reparatur_und_refurbishment",
    "Remanufacturing_und_Upcycling":    "av_remanufacturing_und_upcycling",
    "Verstaerkung_und_Schutz":          "av_verstaerkung_und_schutz",
}

# Rueckbauverfahren canonical — 4 keep existing ids; 2 new
RUECKBAU_CANONICAL = {
    "Selektiver_Rueckbau":              "rv_selektiver_rueckbau",
    "Ausbau_von_Bauteilen":             "rv_ausbau_von_bauteilen",
    "Demontage":                        "rv_demontage",
    "Zerstoerungsarme_Bergung":         "rv_zerstoerungsarme_bergung",
    "Schneidender_Rueckbau":            "rv_schneidender_rueckbau",
    "Integrierter_Rueckbau_und_Lagerung": "rv_integrierter_rueckbau_und_lagerung",
}

# Ressourcenquelle canonical (post Quelle→Ressourcenquelle rewrite)
RESSOURCE_CANONICAL = {
    "Externer_Spenderbau":              "rq_externer_spenderbau",
    "Eigener_Bestand":                  "rq_eigener_bestand",
    "Gleicher_Standort":                "rq_gleicher_standort",
    "Bauteilmarkt_oder_Lager":          "rq_bauteilmarkt_oder_lager",
    "Leihgabe_oder_Service":            "rq_leihgabe_oder_service",
    "Restposten_Abfall_Unbekannt":      "rq_restposten_abfall_unbekannt",
}

# Wiederverwendungsergebnis canonical
WVER_CANONICAL = {
    "Bestandserhalt":                       "wver_bestandserhalt",
    "Wiederverwendung_gleiche_Funktion":    "wver_wv_gleiche_funktion",
    "Wiederverwendung_neue_Funktion":       "wver_wv_neue_funktion",
    "Modul_oder_Abschnittswiederverwendung": "wver_modul_oder_abschnittswv",
    "Material_Reprocessing":                "wver_material_reprocessing",
    "Geplant_oder_Gelagert":                "wver_geplant_oder_gelagert",
}

# Wiederverwendungsort canonical
WVO_CANONICAL = {
    "In_situ":                              "wvo_in_situ",
    "Im_selben_Gebaeude_versetzt":          "wvo_im_selben_gebaeude_versetzt",
    "Auf_demselben_Standort_versetzt":      "wvo_auf_demselben_standort_versetzt",
    "Extern_importiert":                    "wvo_extern_importiert",
    "Temporär_oder_zurueckgegeben":         "wvo_temporaer_oder_zurueckgegeben",
    "Temporaer_oder_zurueckgegeben":        "wvo_temporaer_oder_zurueckgegeben",
    "Gelagert_oder_Unbekannt":              "wvo_gelagert_oder_unbekannt",
}

# Combined: relationship → canonical-id lookup for the target_node column
REL_TO_CANONICAL = {
    "HAT_METHODE":            METHODE_CANONICAL,
    "HAT_AUFBEREITUNG":       AUFBER_CANONICAL,
    "HAT_RUECKBAUVERFAHREN":  RUECKBAU_CANONICAL,
    "HAT_RESSOURCENQUELLE":   RESSOURCE_CANONICAL,
    "HAT_ERGEBNIS":           WVER_CANONICAL,
    "HAT_WIEDERVERWENDUNGSORT": WVO_CANONICAL,
}

# Non-reuse BG prefixes to filter out
NON_REUSE_PREFIXES = ("bg_retained_", "bg_planned_", "bg_dismantled_", "bg_candidate_")


# ---------------------------------------------------------------------------

class BatchProcessor:
    def __init__(self):
        self.stats = Counter()
        self.filtered_rows: list[tuple[str, str]] = []  # (batch_filename, raw_line)

    def normalize_cell(self, name: str, value: str, row_rel: str) -> tuple[str, list[str]]:
        """Apply substitutions to a single cell. Returns (new_value, list_of_changes_applied)."""
        changes: list[str] = []
        new = value

        if name == "relationship":
            if new in REL_MAP:
                changes.append(f"rel_alias:{new}->{REL_MAP[new]}")
                new = REL_MAP[new]
        elif name in ("target_label", "target_type"):
            if new in TARGET_LABEL_MAP:
                changes.append(f"target_label:{new}->{TARGET_LABEL_MAP[new]}")
                new = TARGET_LABEL_MAP[new]
        elif name == "target_node":
            new, changes = self._normalize_target_node(new, row_rel)
        elif name == "canonical_taxonomy_target" or name == "canonical_target":
            # Apply legacy-label normalization first
            if new in CANONICAL_TARGET_MAP:
                changes.append(f"canon_norm:{new}->{CANONICAL_TARGET_MAP[new]}")
                new = CANONICAL_TARGET_MAP[new]
            # Rel-aware fallback for ambiguous tokens
            if new == "Dekonstruktion_mit_Inventar":
                if row_rel == "HAT_RUECKBAUVERFAHREN":
                    changes.append("canon_norm_rel:Dekonstruktion_mit_Inventar->Selektiver_Rueckbau")
                    new = "Selektiver_Rueckbau"
                elif row_rel == "HAT_METHODE":
                    changes.append("canon_norm_rel:Dekonstruktion_mit_Inventar->Dokumentation_und_Monitoring")
                    new = "Dokumentation_und_Monitoring"

        # Record changes in stats
        for c in changes:
            self.stats[c] += 1
        return new, changes

    def _normalize_target_node(self, value: str, row_rel: str) -> tuple[str, list[str]]:
        changes: list[str] = []
        new = value

        # Strip a draft prefix (q_, wo_, we_) and normalize the suffix using the canonical map
        # for the row's relationship type.
        if row_rel in REL_TO_CANONICAL:
            canon_map = REL_TO_CANONICAL[row_rel]

            # Try direct lookup of the value
            if new in canon_map:
                changes.append(f"id:{new}->{canon_map[new]}")
                new = canon_map[new]
                return new, changes

            # Strip known draft prefixes and lookup the suffix
            for draft, _new_prefix in ID_PREFIX_REWRITE_RULES + [("av_", "av_"), ("rv_", "rv_")]:
                if new.startswith(draft):
                    suffix = new[len(draft):]
                    # Try canonical-token normalization on suffix
                    suffix_norm = CANONICAL_TARGET_MAP.get(suffix, suffix)
                    if suffix_norm != suffix:
                        changes.append(f"canon_norm_in_id:{suffix}->{suffix_norm}")
                    if suffix_norm in canon_map:
                        new_id = canon_map[suffix_norm]
                        changes.append(f"id_via_prefix:{value}->{new_id}")
                        return new_id, changes
                    break

        return new, changes

    def is_non_reuse_row(self, cells: list[str], col_idx: dict[str, int]) -> str | None:
        """Return the offending bg_* slug if the row anchors on a non-bg_reuse_ BG, else None."""
        for name in ("bauteilgruppe", "target_node"):
            i = col_idx.get(name, -1)
            if 0 <= i < len(cells):
                v = cells[i]
                if v.startswith(NON_REUSE_PREFIXES):
                    return v
        return None

    def process_file(self, path: Path) -> str:
        text = path.read_text(encoding="utf-8")
        out_lines: list[str] = []
        col_idx: dict[str, int] | None = None
        rows_in = 0
        rows_kept = 0
        rows_filtered = 0
        file_change_count = 0

        for raw_line in text.splitlines():
            stripped = raw_line.lstrip()

            # Pass-through non-table lines
            if not stripped.startswith("|"):
                out_lines.append(raw_line)
                col_idx = None
                continue

            cells = [c.strip() for c in stripped.strip("|").split("|")]
            # Separator row
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                out_lines.append(raw_line)
                continue
            # Header row
            if "project_id" in cells and ("edge_id" in cells or "id" in cells):
                col_idx = {n: i for i, n in enumerate(cells)}
                if "edge_id" not in col_idx and "id" in col_idx:
                    col_idx["edge_id"] = col_idx["id"]
                out_lines.append(raw_line)
                continue
            # Data row — must have header
            if not col_idx:
                out_lines.append(raw_line)
                continue
            if len(cells) <= max(col_idx.values()):
                out_lines.append(raw_line)
                continue

            edge_id = cells[col_idx["edge_id"]]
            # Accept any of: v10A-001, v10F07-001, v10-001-01, v10-003-01a
            if not re.fullmatch(r"v10[A-Z0-9]*-\d+(?:-\w+)?", edge_id):
                out_lines.append(raw_line)
                continue

            # It's a real data row
            rows_in += 1

            # Filter: if it anchors on a non-bg_reuse_ BG, route to the filtered file
            bad_bg = self.is_non_reuse_row(cells, col_idx)
            if bad_bg:
                self.stats[f"filter:{[p for p in NON_REUSE_PREFIXES if bad_bg.startswith(p)][0]}"] += 1
                rows_filtered += 1
                self.filtered_rows.append((path.name, raw_line))
                continue

            # Normalize cells in-place
            new_cells = list(cells)
            row_rel = ""
            rel_idx = col_idx.get("relationship", -1)
            if 0 <= rel_idx < len(cells):
                row_rel = cells[rel_idx]
                # Normalize the rel cell first so other cells see the new rel
                new_rel, _ = self.normalize_cell("relationship", row_rel, row_rel)
                new_cells[rel_idx] = new_rel
                row_rel = new_rel

            for name in ("target_label", "target_type", "target_node", "canonical_taxonomy_target", "canonical_target"):
                i = col_idx.get(name, -1)
                if 0 <= i < len(cells):
                    new_val, changes = self.normalize_cell(name, cells[i], row_rel)
                    new_cells[i] = new_val
                    if changes:
                        file_change_count += len(changes)

            # Rebuild the line
            normalized_line = "| " + " | ".join(new_cells) + " |"
            # Preserve leading whitespace
            leading = raw_line[: len(raw_line) - len(stripped)]
            out_lines.append(leading + normalized_line)
            rows_kept += 1

        self.stats[f"file:{path.name}:rows_in"] = rows_in
        self.stats[f"file:{path.name}:rows_kept"] = rows_kept
        self.stats[f"file:{path.name}:rows_filtered"] = rows_filtered
        self.stats[f"file:{path.name}:changes"] = file_change_count

        return "\n".join(out_lines) + ("\n" if text.endswith("\n") else "")


def main() -> int:
    NORMALIZED_DIR.mkdir(parents=True, exist_ok=True)

    proc = BatchProcessor()
    summary_per_file = []

    # Batches 07-09 use a free-text component_or_scope/scope_component column
    # with NO bg_* slug ids. They cannot be slug-linked to live BGs without a
    # separate manual mapping pass. Per FINAL_PLAN: defer these batches to a
    # future integration round.
    DEFERRED_BATCHES = {
        "reuse_taxonomy_v9_connection_expansion_batch_07.md",
        "reuse_taxonomy_v9_connection_expansion_batch_08.md",
        "reuse_taxonomy_v9_connection_expansion_batch_09.md",
    }

    for md in sorted(BATCH_DIR.glob("reuse_taxonomy_v9_connection_expansion_batch_*.md")):
        if "open_questions" in md.name:
            continue
        if md.name in DEFERRED_BATCHES:
            summary_per_file.append((md.name, "deferred", "—", "—", "—"))
            continue
        normalized = proc.process_file(md)
        out_path = NORMALIZED_DIR / md.name
        out_path.write_text(normalized, encoding="utf-8")
        summary_per_file.append((
            md.name,
            proc.stats[f"file:{md.name}:rows_in"],
            proc.stats[f"file:{md.name}:rows_kept"],
            proc.stats[f"file:{md.name}:rows_filtered"],
            proc.stats[f"file:{md.name}:changes"],
        ))

    # ---------------- write filtered file ----------------
    lines = [
        "# Filtered non-bg_reuse_ batch rows",
        "",
        "Rows below were removed from the import set in Phase 2.5 because they anchor on",
        "a `bg_retained_*` / `bg_planned_*` / `bg_dismantled_*` / `bg_candidate_*` Bauteilgruppe.",
        "Per FINAL_PLAN decision #8 (2026-06-03), these prefixes do not semantically belong",
        "to `:Bauteilgruppe` and are excluded from the integration scope.",
        "",
        "Preserved here as transparent historical record. Future research/cleanup passes can",
        "reclassify these findings under a dedicated label (`:Bestand`, `:GeplantesBauteil`,",
        "`:Dekonstruktion`, etc.) if desired.",
        "",
        f"Total rows: {len(proc.filtered_rows)}",
        "",
        "## Rows",
        "",
    ]
    current_file = None
    for batch_name, raw_line in proc.filtered_rows:
        if batch_name != current_file:
            lines.append("")
            lines.append(f"### {batch_name}")
            lines.append("")
            current_file = batch_name
        lines.append(raw_line)
    FILTERED_FILE.write_text("\n".join(lines), encoding="utf-8")

    # ---------------- write report ----------------
    rep = [
        "# Phase 2 normalization report",
        "",
        f"Generated by `phase2_normalize_and_filter.py` over batches in `{BATCH_DIR.relative_to(ROOT)}`.",
        "",
        "## Output",
        "",
        f"- Normalized batches written to `{NORMALIZED_DIR.relative_to(ROOT)}/`",
        f"- Filtered non-reuse rows written to `{FILTERED_FILE.relative_to(ROOT)}`",
        "",
        "## Per-file summary",
        "",
        "| Batch | rows in | rows kept | rows filtered | substitutions applied |",
        "|---|---:|---:|---:|---:|",
    ]
    total_in = total_kept = total_filtered = total_changes = 0
    for name, rin, rkept, rfilt, rchanges in summary_per_file:
        rep.append(f"| `{name}` | {rin} | {rkept} | {rfilt} | {rchanges} |")
        if isinstance(rin, int):
            total_in += rin
            total_kept += rkept
            total_filtered += rfilt
            total_changes += rchanges
    rep.append(f"| **TOTAL (importable)** | **{total_in}** | **{total_kept}** | **{total_filtered}** | **{total_changes}** |")
    rep.append("")
    rep.append("## Deferred batches")
    rep.append("")
    rep.append("Batches 07, 08, 09 use a free-text `component_or_scope` column with no `bg_*` slug ids.")
    rep.append("They cannot be slug-linked to live :Bauteilgruppe nodes without a separate manual")
    rep.append("mapping pass. Per FINAL_PLAN decision (skip manual resolver), these batches are")
    rep.append("deferred to a future integration round. Total deferred row count: ~96+158+251 = 505 rows.")
    rep.append("")

    rep.append("## Substitutions by kind")
    rep.append("")
    rep.append("| Kind | Count |")
    rep.append("|---|---:|")
    by_kind: Counter = Counter()
    for k, v in proc.stats.items():
        if k.startswith("file:"):
            continue
        if k.startswith("filter:"):
            continue
        # Group by the first segment of the change key
        kind = k.split(":", 1)[0]
        by_kind[kind] += v
    for k, v in by_kind.most_common():
        rep.append(f"| `{k}` | {v} |")
    rep.append("")

    rep.append("## Filtered rows by BG prefix")
    rep.append("")
    rep.append("| Prefix | Rows |")
    rep.append("|---|---:|")
    for k, v in sorted([(k, v) for k, v in proc.stats.items() if k.startswith("filter:")], key=lambda x: -x[1]):
        rep.append(f"| `{k[len('filter:'):]}` | {v} |")
    rep.append("")

    REPORT_FILE.write_text("\n".join(rep), encoding="utf-8")

    print(f"Phase 2 normalization complete.")
    print(f"  Normalized batches: {NORMALIZED_DIR}")
    print(f"  Filtered rows file: {FILTERED_FILE}")
    print(f"  Report:             {REPORT_FILE}")
    print()
    print(f"  Rows in : {total_in}")
    print(f"  Kept    : {total_kept}")
    print(f"  Filtered: {total_filtered}")
    print(f"  Substitutions applied: {total_changes}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
