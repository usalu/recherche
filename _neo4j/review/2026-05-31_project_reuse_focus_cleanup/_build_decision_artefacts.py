"""Build decision_table.csv + Phase A/B/C patch files from the resolved evidence + cascade targets.

Inputs (in the same directory):
  - resolution.jsonl, evidence.jsonl, schema_snapshot.json
  - cascade_targets.json (produced by _collect_cascade_targets.py)

Outputs:
  - decision_table.csv
  - projects.phaseA.patch.jsonl        (delete_node cascade + set_property)
  - projects.phaseB.patch.jsonl        (merge_node)
  - projects.phaseB.merge_targets.txt  (source ids; need pre-merge snapshot)
  - projects.phaseA.delete_targets.txt (ids needing pre-delete snapshot)
  - projects.phaseC_strip_projekt.cypher
"""

from __future__ import annotations
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

resolution = [json.loads(l) for l in (HERE / "resolution.jsonl").open(encoding="utf-8")]
evidence = [json.loads(l) for l in (HERE / "evidence.jsonl").open(encoding="utf-8")]
cascade = json.loads((HERE / "cascade_targets.json").read_text(encoding="utf-8"))
schema = json.loads((HERE / "schema_snapshot.json").read_text(encoding="utf-8"))
allowed_labels = set(schema["live_graph"]["node_labels"])

evidence_by_id: dict[str, dict] = {e["id"]: e for e in evidence if e.get("found")}
cascade_by_project: dict[str, dict] = {c["project_id"]: c for c in cascade}

DECISIONS: list[dict] = []


def evidence_summary(eid: str) -> str:
    e = evidence_by_id.get(eid)
    if not e:
        return ""
    flags = []
    if e["reclaimed_proof"]:
        flags.append("RECLAIMED_PROOF")
    if e["incoming_quellen_count"]:
        flags.append(f"Q={e['incoming_quellen_count']}")
    for key, lbl in (("donor_bauwerks", "donor"), ("receiver_bauwerks", "recv"),
                    ("aufbereitung", "aufb"), ("wva", "wva"),
                    ("nutzt_bauwerk", "nutzt"), ("from_donor", "fdonor"),
                    ("into_receiver", "irecv")):
        if e[key]:
            flags.append(f"{lbl}={len(e[key])}")
    return " ".join(flags) or "none"


def labels_of(eid: str) -> str:
    e = evidence_by_id.get(eid)
    return "+".join(sorted(e["labels"])) if e else ""


def row(name, primary_id, action, target=None, op=None, op_args=None, strip_projekt=False, confidence="high", notes=""):
    return {
        "candidate_name": name,
        "primary_id": primary_id,
        "current_labels": labels_of(primary_id) if primary_id else "",
        "evidence": evidence_summary(primary_id) if primary_id else "",
        "action": action,
        "target": target or "",
        "op": op or "",
        "op_args": json.dumps(op_args, ensure_ascii=False) if op_args else "",
        "strip_projekt": str(strip_projekt).lower(),
        "confidence": confidence,
        "notes": notes,
    }


def cascade_delete_ops(pid: str, project_reason: str) -> list[dict]:
    """Return [delete_node for each cascade aux] + [delete_node for project itself].
    Order: aux first (cleaner semantics), project last. Either order works with DETACH DELETE."""
    ct = cascade_by_project.get(pid)
    if not ct:
        return [{"op": "delete_node", "id": pid, "reason": project_reason, "severity": "MEDIUM"}]
    ops = []
    for aux in ct["cascade"]:
        ops.append({
            "op": "delete_node",
            "id": aux["id"],
            "reason": f"Cascade with {pid}: {aux['reason']}",
            "severity": "LOW",
        })
    ops.append({"op": "delete_node", "id": pid, "reason": project_reason, "severity": "MEDIUM"})
    return ops


def surface_note(pid: str) -> str:
    ct = cascade_by_project.get(pid)
    if not ct or not ct["surface"]:
        return ""
    items = "; ".join(f"{s['id']} ({'+'.join(sorted(s['labels']))})" for s in ct["surface"])
    return f"Real-world neighbours NOT cascaded — surface for review: {items}"


# --- DELETE candidates (cascade + project) ---
DECISIONS.append(row(
    "Circle House", "p_circle_house",
    action="delete_cascade",
    op="delete_node[+cascade]",
    op_args={"cascade_ops": cascade_delete_ops("p_circle_house",
        "User rule 1: non-reuse, non-reclaimed. Evidence: no donor/receiver/wva/nutzt/aufbereitung. Quellen=0.")},
    confidence="high",
    notes=surface_note("p_circle_house")))

DECISIONS.append(row(
    "OBK 27", "p_obk_27",
    action="delete_cascade",
    op="delete_node[+cascade]",
    op_args={"cascade_ops": cascade_delete_ops("p_obk_27",
        "User explicit conditional: delete unless graph evidence proves reclaimed components. None found.")},
    confidence="high",
    notes=surface_note("p_obk_27")))

DECISIONS.append(row(
    "Careno Be.Circular (REMOVE per user 2026-05-31)", "p_careno_becircular",
    action="delete_cascade",
    op="delete_node[+cascade]",
    op_args={"cascade_ops": cascade_delete_ops("p_careno_becircular",
        "User instruction 2026-05-31: remove Careno completely with all related project-scoped aux nodes (Bauteilgruppe, etc.). No donor/receiver/wva/nutzt — does not meet reclaimed-component criteria.")},
    confidence="high",
    notes=surface_note("p_careno_becircular")))

DECISIONS.append(row(
    "Eggshell Pavilion (REMOVE per user 2026-05-31)", "p_eggshell_pavilion",
    action="delete_cascade",
    op="delete_node[+cascade]",
    op_args={"cascade_ops": cascade_delete_ops("p_eggshell_pavilion",
        "User instruction 2026-05-31: remove Eggshell completely with all related project-scoped aux nodes. No donor/receiver/wva/nutzt — does not meet reclaimed-component criteria.")},
    confidence="high",
    notes=surface_note("p_eggshell_pavilion")))

DECISIONS.append(row(
    "Granby Workshop Liverpool (REMOVE per user 2026-05-31 — override)", "p_granby_workshop",
    action="delete_cascade",
    op="delete_node[+cascade]",
    op_args={"cascade_ops": cascade_delete_ops("p_granby_workshop",
        "User instruction 2026-05-31: remove Granby Workshop with all relations including Bauteilgruppe. Overrides prior keep-decision (graph had NUTZT_BAUWERK=1 + HAT_BAUTEILGRUPPE=4 reclaimed evidence).")},
    confidence="high",
    notes="EXPLICIT USER OVERRIDE — graph evidence proved reclaimed components, but user instructs removal. " + surface_note("p_granby_workshop")))

# --- Must-keep regardless of status ---
DECISIONS.append(row(
    "Big Dig Building", "p_big_dig_building_boston",
    action="keep",
    op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "p_big_dig_building_boston",
             "reason": "User rule 2: status=[status_prototyp, status_verworfen, status_vorgeschlagen] but reclaimed_proof=true (wva=2, nutzt=2). Keep.",
             "severity": "LOW"},
    confidence="high",
    notes="Has matching p_big_dig_building_boston.kg.jsonl source record."))

DECISIONS.append(row(
    "Roots in the Sky / Blackfriars", "p_roots_in_the_sky_blackfriars_crown_court",
    action="keep",
    op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "p_roots_in_the_sky_blackfriars_crown_court",
             "reason": "User rule 2: status=[status_geplant, status_verworfen] but reclaimed_proof=true (wva=3, nutzt=1, 92 outgoing BELEGT_IN). Keep — flagship planned-reuse case.",
             "severity": "LOW"},
    confidence="high"))

# --- Reclassify via existing canonical + merge ---
DECISIONS.append(row(
    "FCRBE (canonical exists)", "prog_fcrbe",
    action="keep",
    op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_fcrbe",
             "reason": "Already :Programm (status=concluded). Merge target for p_interreg_nwe_fcrbe.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "Interreg NWE FCRBE (stub)", "p_interreg_nwe_fcrbe",
    action="merge", target="prog_fcrbe",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_interreg_nwe_fcrbe", "to": "prog_fcrbe",
             "reason": "User reclassify: FCRBE → Programm. Canonical exists.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))

# REFAIR / RCMI — absent at :Projekt level
DECISIONS.append(row(
    "REFAIR Bordeaux", "software_refair",
    action="absent_from_graph",
    op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "software_refair",
             "reason": "No :Projekt for REFAIR. Already :Software (software_refair) + :Akteur (refair_bordeaux). No action.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "RCMI / Concular blueprint", "tool_rcmi",
    action="absent_from_graph",
    op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "tool_rcmi",
             "reason": "No :Projekt. Already :Tool+:Software (tool_rcmi), :Software (software_concular), :Akteur (concular). No action.",
             "severity": "LOW"}, confidence="high"))

# RE-USE Höfe
DECISIONS.append(row(
    "RE-USE Höfe (canonical)", "prog_re_use_hoefe",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_re_use_hoefe",
             "reason": "Already :Programm (status=published_2025). Merge target for p_re_use_hoefe.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "RE-USE Höfe (stub)", "p_re_use_hoefe",
    action="merge", target="prog_re_use_hoefe",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_re_use_hoefe", "to": "prog_re_use_hoefe",
             "reason": "User reclassify: RE-USE Höfe → Programm.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))

# REBRIDGE
DECISIONS.append(row(
    "REBRIDGE (canonical)", "prog_rebridge",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_rebridge",
             "reason": "Already :Programm (status=active). Merge target for p_rebridge_structural_reuse_project.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "REBRIDGE (stub)", "p_rebridge_structural_reuse_project",
    action="merge", target="prog_rebridge",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_rebridge_structural_reuse_project", "to": "prog_rebridge",
             "reason": "User reclassify: REBRIDGE → reuse research/prototype Programm.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))

# MedUni
DECISIONS.append(row(
    "MedUni Campus Mariannengasse", "",
    action="absent_from_graph", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "MEDUNI_NO_PROJEKT",
             "reason": "No :Projekt node found. Only :Quelle/:Dossier (q_meduni_campus_mariannengasse_wien_md/_s1). No graph anchor to relabel.",
             "severity": "LOW"}, confidence="high",
    notes="Open: should a stub :Bauwerk/:Projekt be created? Deferred."))

# Stuttgart 210
DECISIONS.append(row(
    "Stuttgart 210 (canonical)", "prog_stuttgart_210",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_stuttgart_210",
             "reason": "Already :Programm (status=active). Merge target for p_stuttgart_210.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "Stuttgart 210 (stub)", "p_stuttgart_210",
    action="merge", target="prog_stuttgart_210",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_stuttgart_210", "to": "prog_stuttgart_210",
             "reason": "User reclassify: Stuttgart 210 → research/living-lab Programm.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))

# Reallabor B(e) Ware
DECISIONS.append(row(
    "Reallabor B(e) Ware (canonical)", "prog_reallabor_be_ware",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_reallabor_be_ware",
             "reason": "Already :Programm. Merge target for both p_reallabor_be_ware AND p_reallabor_b_e_ware.",
             "severity": "LOW"}, confidence="high"))
DECISIONS.append(row(
    "Reallabor B(e) Ware (stub 1)", "p_reallabor_be_ware",
    action="merge", target="prog_reallabor_be_ware",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_reallabor_be_ware", "to": "prog_reallabor_be_ware",
             "reason": "User reclassify+dedup.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))
DECISIONS.append(row(
    "Reallabor B(e) Ware (stub 2)", "p_reallabor_b_e_ware",
    action="merge", target="prog_reallabor_be_ware",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_reallabor_b_e_ware", "to": "prog_reallabor_be_ware",
             "reason": "User reclassify+dedup: second duplicate.", "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))

# UMAR Unit
DECISIONS.append(row(
    "UMAR Unit", "p_umar_unit",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "p_umar_unit",
             "reason": "Reclaimed_proof=true (NUTZT_BAUWERK=1, HAT_BAUTEILGRUPPE=8, HAT_METHODE=4). Keep.",
             "severity": "LOW"}, confidence="high"))

# B4: ETH Circular Construction student → merge into prog_mas_dfab
DECISIONS.append(row(
    "ETH Circular Construction student (B4: merge per user 2026-05-31)", "p_eth_circular_construction_student_reuse_project",
    action="merge", target="prog_mas_dfab",
    op="merge_node",
    op_args={"op": "merge_node",
             "from": "p_eth_circular_construction_student_reuse_project",
             "to": "prog_mas_dfab",
             "reason": "User decision 2026-05-31 (B4): merge student reuse project into the MAS DFAB ETH programme canonical. The student project IS a MAS DFAB output.",
             "severity": "MEDIUM"},
    strip_projekt=True, confidence="high"))
DECISIONS.append(row(
    "MAS DFAB ETH (canonical for B4 merge)", "prog_mas_dfab",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "prog_mas_dfab",
             "reason": "Already :Programm (status=active). Merge target for B4.", "severity": "LOW"},
    confidence="high"))

# LYSP8 rename
DECISIONS.append(row(
    "LYSP8 → canonical name", "p_lysp8",
    action="rename_canonical", op="set_property",
    op_args={"op": "set_property", "id": "p_lysp8", "property": "name",
             "value": "LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel",
             "reason": "User dedup intent: only one node exists; rename to canonical form.",
             "severity": "LOW"}, confidence="high"))

# Pavilion Circl Amsterdam → Circl ABN AMRO
DECISIONS.append(row(
    "Pavilion Circl Amsterdam → Circl", "p_pavilion_circl_amsterdam",
    action="merge", target="p_circl_abn_amro",
    op="merge_node",
    op_args={"op": "merge_node", "from": "p_pavilion_circl_amsterdam", "to": "p_circl_abn_amro",
             "reason": "User dedup intent. p_circl_abn_amro is canonical (reclaimed_proof=true).",
             "severity": "MEDIUM"},
    strip_projekt=False, confidence="high"))
DECISIONS.append(row(
    "Circl ABN AMRO (canonical)", "p_circl_abn_amro",
    action="keep", op="noop_reviewed",
    op_args={"op": "noop_reviewed", "id": "p_circl_abn_amro",
             "reason": "Merge target. Reclaimed_proof=true.", "severity": "LOW"},
    confidence="high"))


# --- Write decision_table.csv ---
csv_path = HERE / "decision_table.csv"
with csv_path.open("w", encoding="utf-8", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=[
        "candidate_name", "primary_id", "current_labels", "evidence",
        "action", "target", "op", "op_args", "strip_projekt", "confidence", "notes",
    ])
    writer.writeheader()
    writer.writerows(DECISIONS)
print(f"Wrote {csv_path} ({len(DECISIONS)} rows)")

# --- Build Phase A / B / C ops ---
phaseA_ops: list[dict] = []
phaseB_ops: list[dict] = []
merge_targets: list[str] = []
delete_targets: list[str] = []
strip_targets: list[str] = []

for d in DECISIONS:
    op_blob = json.loads(d["op_args"]) if d["op_args"] else None
    if not op_blob:
        continue
    if "cascade_ops" in op_blob:
        # delete cascade — emit each op and record project id for snapshot
        for sub in op_blob["cascade_ops"]:
            phaseA_ops.append(sub)
        # Snapshot the project + all cascade ids
        delete_targets.append(d["primary_id"])
        for sub in op_blob["cascade_ops"]:
            if sub["id"] != d["primary_id"]:
                delete_targets.append(sub["id"])
        continue
    op_name = op_blob["op"]
    if op_name in ("set_property", "delete_node"):
        phaseA_ops.append(op_blob)
    elif op_name == "merge_node":
        phaseB_ops.append(op_blob)
        merge_targets.append(op_blob["from"])
        if d["strip_projekt"] == "true":
            strip_targets.append(op_blob["to"])
    # noop_reviewed not emitted as patch op

phaseA = HERE / "projects.phaseA.patch.jsonl"
phaseB = HERE / "projects.phaseB.patch.jsonl"
delete_targets_path = HERE / "projects.phaseA.delete_targets.txt"
merge_targets_path = HERE / "projects.phaseB.merge_targets.txt"
phaseC = HERE / "projects.phaseC_strip_projekt.cypher"

phaseA.write_text("\n".join(json.dumps(o, ensure_ascii=False) for o in phaseA_ops) + ("\n" if phaseA_ops else ""), encoding="utf-8")
print(f"Wrote {phaseA} ({len(phaseA_ops)} ops)")
phaseB.write_text("\n".join(json.dumps(o, ensure_ascii=False) for o in phaseB_ops) + ("\n" if phaseB_ops else ""), encoding="utf-8")
print(f"Wrote {phaseB} ({len(phaseB_ops)} ops)")
delete_targets_path.write_text("\n".join(delete_targets) + ("\n" if delete_targets else ""), encoding="utf-8")
print(f"Wrote {delete_targets_path} ({len(delete_targets)} ids)")
merge_targets_path.write_text("\n".join(merge_targets) + ("\n" if merge_targets else ""), encoding="utf-8")
print(f"Wrote {merge_targets_path} ({len(merge_targets)} ids)")

# Phase C cypher
strip_ids = sorted(set(strip_targets))
cypher_lines = [
    "// Phase C — Strip :Projekt label from canonical :Programm nodes that received",
    "// merge contributions from :Projekt stubs in Phase B. Mirrors the prior",
    "// phase_batch2_v2_23_strip_projekt_label.cypher pattern.",
    "//",
    "// User rule (verbatim from phase_batch2_v2_23):",
    "//   \"if they are not a project remove project otherwise its okay to connect to",
    "//    both. projects are related to a mission of building with Reuse whether",
    "//    planning, research, or engineering, etc. what not a project is Baubörse,",
    "//    software or organisazion.\"",
    "//",
    "// PRECONDITION: Phase A + Phase B applied AND R1 (hard-coded :Projekt queries",
    "// in _scripts/) resolved per dependency_fixes/hard_coded_projekt_query_audit.csv.",
    "// do_not_apply_until=R1_resolved",
    "",
    "MATCH (n:Programm:Projekt) WHERE n.id IN [",
]
for sid in strip_ids:
    cypher_lines.append(f"  '{sid}',")
if cypher_lines[-1].endswith(","):
    cypher_lines[-1] = cypher_lines[-1].rstrip(",")
cypher_lines += [
    "]",
    "REMOVE n:Projekt",
    "RETURN n.id AS id, labels(n) AS remaining_labels;",
    "",
    "// === Verification ===",
    "// MATCH (n:Programm:Projekt) WHERE n.id IN [...above ids] RETURN n.id;",
    "// EXPECTED: 0 rows.",
]
phaseC.write_text("\n".join(cypher_lines) + "\n", encoding="utf-8")
print(f"Wrote {phaseC} ({len(strip_ids)} canonicals targeted)")

# --- Validate against SUPPORTED_OPS ---
import sys
sys.path.insert(0, str(HERE.parents[2] / "_scripts"))
from apply_neo4j_review_patch import SUPPORTED_OPS  # type: ignore
bad = []
for path in (phaseA, phaseB):
    for ln, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if obj["op"] not in SUPPORTED_OPS:
            bad.append((path.name, ln, obj["op"]))
if bad:
    for b in bad:
        print(f"BAD OP: {b}")
    raise SystemExit(2)
print(f"Validation OK against SUPPORTED_OPS ({len(SUPPORTED_OPS)} known ops).")

# Summary of what was generated
n_cascade_deletes = sum(1 for o in phaseA_ops if o["op"] == "delete_node")
n_set_prop = sum(1 for o in phaseA_ops if o["op"] == "set_property")
print()
print(f"Phase A: {n_cascade_deletes} delete_node + {n_set_prop} set_property = {len(phaseA_ops)} total")
print(f"Phase B: {len(phaseB_ops)} merge_node")
print(f"Phase C: REMOVE :Projekt on {len(strip_ids)} canonicals")
print(f"Delete targets (for pre-apply snapshot): {len(delete_targets)} ids")
print(f"Merge targets (for pre-apply snapshot): {len(merge_targets)} ids")
