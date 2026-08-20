"""Build the evidence-gated LaTeX actor-network expansion.

The source is the reviewed FINAL-DATA block in the Semio handoff document.
This script is report-only: it writes derived files below this review folder
and never writes to Neo4j or E:\\semio.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
SOURCE = Path(
    r"E:\semio\mit-bestand\bericht\forschungsbericht\anhang\akteursnetz-erweiterung-kandidaten.md"
)
BASE_CLASSIFICATION = BASE / "klassifikation_actor_project_final.json"
APPROVED = (
    BASE
    / "beziehungsprofil_review"
    / "ERWEITERUNG_KORREKTUREN_FREIGEGEBEN.json"
)
OUT = BASE / "beziehungsprofil_review" / "erweiterung_final"
OUT_DATA = OUT / "akteursnetz_erweiterung_final.json"
OUT_NODES = OUT / "erweiterung_klassifikation.json"
OUT_EDGES = OUT / "erweiterung_kanten.json"
OUT_AUDIT = OUT / "ERWEITERUNG_FINAL_AUDIT.md"

PROFILE = "Vorhabenspezifisch / Vorhaben"
REVIEW_RUN = "2026-08-20_erweiterung_strict_final"

TYPE_MAP = {
    "U": "Unternehmen",
    "M": "Materialhub_Bauteilboerse",
    "F": "Forschung_Lehre",
    "N": "NGO_Verband_Netzwerk",
    "I": "Oeffentliche_Institution",
    "S": "Software_Tool_Anbieter",
    "O": "Organisation",
    "G": "Foerdergeber_Programmtraeger",
}

# The earlier manifest is advisory. These four rows fail the stricter final
# rule: the source must assign a concrete task to the exact actor/project pair.
STRICT_REMOVALS = {
    "candidate-edge:proposal:proj:108:B:3": (
        "Norsk Folkemuseum ist nicht am Spenderprojekt Nedre Sem beteiligt."
    ),
    "candidate-edge:proposal:proj:104:A:1": (
        "Die Liljewall-Quelle betrifft eine andere Ekebäckshöjd-Etappe."
    ),
    "candidate-edge:proposal:proj:115:A:1": (
        "Die Quelle dokumentiert einen Fall, aber keine BTU-Beteiligung."
    ),
    "candidate-edge:proposal:proj:69:A:2": (
        "Die Quelle nennt Cleveland Steel Stock, nicht den geführten Akteur."
    ),
}

EDGE_OVERRIDES = {
    "candidate-edge:proposal:rejected:P41-B03": {
        "type": "Entwurf",
        "description": "Plante den Einbau wiederverwendeter Materialien.",
        "evidence_url": "https://rotordb.org/en/projects/multi-de-brouckere-tower",
        "evidence_quote": (
            "Rotor assisted Conix RDBM and Whitewood during design and "
            "construction by looking for candidate materials."
        ),
    },
    "candidate-edge:proposal:proj:44:B:2": {
        "description": "Montierte als Subunternehmer die Reuse-Holzfassade.",
    },
    "candidate-edge:proposal:proj:72:B:1": {
        "description": "Veranlasste den Rückbau des Stahl-Spendergebäudes.",
    },
    "candidate-edge:proposal:proj:79:B:2": {
        "description": "Beauftragte Checkpoint 90 mit Reuse-Bauteilen.",
    },
}

NODE_OVERRIDES = {
    "proj:95": {"name": "La Caserne de Reuilly"},
    "candidate:proj:41:B:2": {"grade": "bezug"},
    "candidate:proj:102:B:1": {"grade": "bezug"},
    "candidate:proj:112:B:1": {"grade": "bezug"},
}

MERGE_SOURCE = "candidate:proj:79:B:1"
MERGE_TARGET = "candidate:proj:76:B:2"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_final_data() -> dict:
    text = SOURCE.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- FINAL-DATA:START -->\s*```json\s*(.*?)\s*```\s*"
        r"<!-- FINAL-DATA:END -->",
        text,
        flags=re.S,
    )
    if not match:
        raise RuntimeError("FINAL-DATA block not found")
    data = json.loads(match.group(1))
    if not data.get("approved"):
        raise RuntimeError("FINAL-DATA is not approved")
    return data


def clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = re.sub(r"^\*[^*]+\*\s*\([^)]*\):\s*", "", text)
    text = text.rstrip(" ,;:")
    if text:
        text = text[0].upper() + text[1:]
    if text and text[-1] not in ".!?":
        text += "."
    return text


MATERIALS = (
    (r"Eichenfenster|Fensterrahmen", "gebrauchte Fensterrahmen", "gebrauchten Fensterrahmen"),
    (r"Wärmetauscher|Fassadenplatte", "gebrauchte Fassadenplatten", "gebrauchten Fassadenplatten"),
    (r"Pipeline|Rohrleitungsstahl", "gebrauchten Pipeline-Stahl", "Pipeline-Stahl"),
    (r"Betonfertig|Betonplatte|Betonabbruch|Betonelement", "gebrauchte Betonbauteile", "gebrauchten Betonbauteilen"),
    (r"Holz|Balken|Holzkassette|Dachbrett", "gebrauchte Holzbauteile", "gebrauchten Holzbauteilen"),
    (r"Ziegel|Backstein|Mauerstein", "gebrauchte Ziegel", "gebrauchten Ziegeln"),
    (r"Stahl|Stahlskelett|Stahlträger|Stahlprofil", "gebrauchten Stahl", "gebrauchtem Stahl"),
    (r"Blaustein", "geborgenen Blaustein", "geborgenem Blaustein"),
    (r"Granit", "geborgenen Granit", "geborgenem Granit"),
    (r"Pflaster", "gebrauchte Pflastersteine", "gebrauchten Pflastersteinen"),
    (r"Container", "gebrauchte Frachtcontainer", "gebrauchten Frachtcontainern"),
    (r"Fenster", "gebrauchte Fenster", "gebrauchten Fenstern"),
    (r"Fassade", "gebrauchte Fassadenteile", "gebrauchten Fassadenteilen"),
    (r"Bauteil|Material", "gebrauchte Bauteile", "gebrauchten Bauteilen"),
)


def material_terms(text: str) -> tuple[str, str]:
    for pattern, accusative, dative in MATERIALS:
        if re.search(pattern, text, flags=re.I):
            return accusative, dative
    return "gebrauchte Bauteile", "gebrauchten Bauteilen"


def fallback_description(edge_type: str, original: str) -> str:
    acc, dat = material_terms(original)
    templates = {
        "Bauteillieferung": f"Lieferte {acc}.",
        "Bauherrschaft": f"Beauftragte den Einsatz von {dat}.",
        "Entwurf": f"Plante den Einsatz von {dat}.",
        "Reuse-Konzept": f"Entwickelte den Einsatz von {dat}.",
        "Bauausführung": f"Baute {acc} ein.",
        "Fachplanung": f"Plante den Wiedereinsatz von {dat}.",
        "Rückbau": f"Barg {acc} für den Wiedereinbau.",
        "Aufarbeitung": f"Arbeitete {acc} für den Wiedereinbau auf.",
        "Bauteilinventarisierung": f"Erfasste {acc} für den Wiedereinbau.",
        "Logistik": f"Transportierte {acc} zur Baustelle.",
        "Prüfung und Nachweis": f"Prüfte {acc} für den Wiedereinsatz.",
        "Förderung": f"Förderte den Einsatz von {dat}.",
        "Forschungsbegleitung": f"Untersuchte den Einsatz von {dat}.",
        "Projektleitung": "Leitete das konkrete Reuse-Vorhaben.",
    }
    return templates.get(edge_type, f"Erbrachte die belegte Leistung mit {dat}.")


def normalized_description(
    edge: dict, actor_name: str, project_name: str, project_context: str
) -> str:
    key = edge["key"]
    if key in EDGE_OVERRIDES and EDGE_OVERRIDES[key].get("description"):
        result = clean_sentence(EDGE_OVERRIDES[key]["description"])
    else:
        result = clean_sentence(edge.get("description", ""))
        # Endpoint columns already state both names. Remove repeated names at
        # the beginning and repeated project names where this remains clean.
        for name in (actor_name, project_name):
            if name:
                result = re.sub(
                    rf"^{re.escape(name)}\s+", "", result, flags=re.I
                )
        replacements = (
            ("wiederverwendetem", "gebrauchtem"),
            ("wiederverwendeten", "gebrauchten"),
            ("wiederverwendeter", "gebrauchter"),
            ("wiederverwendete", "gebrauchte"),
            ("wiederverwendbare", "wiedereinsetzbare"),
            ("Tragwerksplanung", "Tragwerkplanung"),
            ("Generalunternehmer", "Totalunternehmer"),
            ("gemeinsam mit", "mit"),
            ("rund ", ""),
        )
        for old, new in replacements:
            result = result.replace(old, new)
        result = clean_sentence(result)
        bad_start = bool(
            re.match(
                r"^(\(|Bauherr|Bauherrin|Hauptunternehmer|Generalunternehmer|"
                r"Totalentreprenör|Bauteillieferung|Projektbeitrag)\b",
                result,
                flags=re.I,
            )
        )
        if len(result) > 60 or bad_start:
            result = fallback_description(
                edge.get("type", ""),
                f"{edge.get('description', '')} {project_context}",
            )
    result = clean_sentence(result)
    if len(result) > 60:
        raise RuntimeError(f"description still exceeds 60 characters: {key}: {result}")
    return result


def main() -> None:
    data = load_final_data()
    approved = json.loads(APPROVED.read_text(encoding="utf-8"))
    if not approved.get("approved"):
        raise RuntimeError("correction manifest is not approved")

    baseline = json.loads(BASE_CLASSIFICATION.read_text(encoding="utf-8"))
    baseline_id = {row.get("id"): eid for eid, row in baseline.items() if row.get("id")}
    source_nodes = {row["key"]: row for row in data["nodes"]}

    def normalized_name(value: str) -> str:
        return re.sub(r"[^a-z0-9]+", "", value.casefold())

    baseline_names = {}
    for eid, row in baseline.items():
        key = (row.get("cc"), normalized_name(row.get("name") or ""))
        baseline_names.setdefault(key, []).append(eid)

    nodes = {
        row["key"]: dict(row)
        for row in data["nodes"]
        if row["key"].startswith("candidate:") or row["key"].startswith("proj:")
    }
    for key, values in NODE_OVERRIDES.items():
        if key not in nodes:
            raise RuntimeError(f"node override target absent: {key}")
        nodes[key].update(values)

    # Merge the duplicate BAM identities and retain the stronger reviewed
    # general-practice evidence under the exact BAM Bouw en Techniek name.
    source = nodes.pop(MERGE_SOURCE)
    target = nodes[MERGE_TARGET]
    target["grade"] = "kern"
    target["relevance"] = source["relevance"]
    target["sourceUrl"] = source["sourceUrl"]
    target["roleEvidence"] = (target.get("roleEvidence") or []) + (
        source.get("roleEvidence") or []
    )

    tradlab_key = "project:tradlab-tre"
    nodes[tradlab_key] = {
        "key": tradlab_key,
        "country": "NO",
        "kind": "project",
        "entityType": "P",
        "name": "TradLab TRE",
        "grade": "bezug",
        "roles": ["Referenzprojekt"],
        "roleGroups": ["P"],
        "relevance": "Verwendet Holz der Nedre-Sem-Låve in Tragwerk und Bekleidung.",
        "sourceUrl": "https://norskfolkemuseum.no/handverkstunet",
        "projectStatus": "completed",
        "reuseState": "installed",
        "reuseObjects": ["Holztragwerk", "Holzbekleidung"],
        "state": "focal",
        "actualReuseVerified": True,
    }

    raw_edges = [
        dict(row)
        for row in data["edges"]
        if row["key"].startswith("candidate-edge:")
        and row["key"] not in STRICT_REMOVALS
    ]
    for edge in raw_edges:
        if edge["source"] == MERGE_SOURCE:
            edge["source"] = MERGE_TARGET
        override = EDGE_OVERRIDES.get(edge["key"], {})
        if override.get("type"):
            edge["type"] = override["type"]
        if override.get("evidence_url"):
            edge["evidenceUrl"] = override["evidence_url"]
        if override.get("evidence_quote"):
            edge["evidenceQuote"] = override["evidence_quote"]

    raw_edges.append({
        "key": "candidate-edge:replacement:tradlab-tre:norsk-folkemuseum",
        "source": "candidate:proj:108:B:3",
        "target": tradlab_key,
        "type": "Bauausführung",
        "description": "Baute Holz aus Nedre Sem in Tragwerk und Bekleidung ein.",
        "evidenceUrl": "https://norskfolkemuseum.no/handverkstunet",
        "evidenceQuote": (
            "Håndverkerne ved Norsk Folkemuseum har bygget den tradisjonelle, "
            "bærende konstruksjonen og kledningen."
        ),
        "kind": "normal",
    })

    def endpoint(key: str) -> str:
        if key.startswith("base:"):
            public_id = key.removeprefix("base:")
            source_row = source_nodes.get(key) or {}
            name_key = (
                source_row.get("country"),
                normalized_name(source_row.get("name") or ""),
            )
            candidates = baseline_names.get(name_key, [])
            if len(candidates) == 1:
                return candidates[0]
            # Public table IDs were renumbered by the strict cleanup. They
            # are only a fallback when the name still agrees exactly.
            public_eid = baseline_id.get(public_id)
            if public_eid and normalized_name(baseline[public_eid].get("name") or "") == name_key[1]:
                return public_eid
            raise RuntimeError(
                f"baseline endpoint not uniquely found: {key}; "
                f"name={source_row.get('name')!r}, candidates={candidates}"
            )
        if key not in nodes:
            raise RuntimeError(f"expansion endpoint not found: {key}")
        return key

    final_edges = []
    seen_pairs = set()
    for edge in raw_edges:
        source_key, target_key = edge["source"], edge["target"]
        source_eid, target_eid = endpoint(source_key), endpoint(target_key)
        pair = (source_eid, target_eid)
        if pair in seen_pairs:
            raise RuntimeError(f"duplicate expansion edge pair: {pair}")
        seen_pairs.add(pair)
        source_name = (
            nodes[source_key]["name"]
            if source_key in nodes
            else baseline[source_eid]["name"]
        )
        target_name = nodes[target_key]["name"]
        evidence_url = (edge.get("evidenceUrl") or "").strip()
        original_evidence = re.sub(
            r"\s+", " ", (edge.get("evidenceQuote") or "").strip()
        )
        evidence_text = re.sub(r"^--\s*", "", original_evidence)
        if not evidence_url.startswith(("http://", "https://")):
            raise RuntimeError(f"edge without source URL: {edge['key']}")
        if not evidence_text:
            raise RuntimeError(f"edge without evidence text: {edge['key']}")
        project_row = nodes[target_key]
        project_context = " ".join(
            [
                target_name,
                *(project_row.get("reuseObjects") or []),
                project_row.get("reuseProcess") or "",
            ]
        )
        description = normalized_description(
            edge, source_name, target_name, project_context
        )
        evidence_kind = (
            "review_note"
            if re.match(r"^(--|Beide |Eigene |EPFL-|Quelle |Projektseite )", original_evidence)
            else "source_excerpt"
        )
        final_edges.append({
            "id": edge["key"],
            "cc": nodes[target_key]["country"],
            "kind": "AKTEUR-BAUVORHABEN",
            "pair": [source_eid, target_eid],
            "beziehungsart": edge["type"],
            "richtung": "A→B",
            "beschreibung": description,
            "beleg": "vorhanden",
            "evidence_url": evidence_url,
            "evidence_quote": evidence_text,
            "evidence_text_kind": evidence_kind,
            "evidence_confidence": "belegt",
            "review_status": "reviewed_keep",
            "review_run": REVIEW_RUN,
            "entfernen": False,
            "beziehungsprofil": PROFILE,
            "beziehungsprofil_status": "approved",
        })

    node_rows = {}
    loader_nodes = []
    for key in sorted(nodes):
        row = nodes[key]
        source_url = (row.get("sourceUrl") or "").strip()
        if not source_url.startswith(("http://", "https://")):
            raise RuntimeError(f"node without source URL: {key}")
        is_project = row["kind"] == "project"
        if not is_project and row.get("entityType") not in TYPE_MAP:
            raise RuntimeError(f"unsupported actor type: {key}: {row.get('entityType')}")
        evidence = row.get("roleEvidence") or []
        if is_project and row.get("projectEvidence"):
            evidence = [row["projectEvidence"]]
        if key == tradlab_key:
            evidence = [{
                "url": source_url,
                "quote": (
                    "En stor del av trevirket er ombruk fra en 130 år gammel "
                    "låve fra Nedre Sem i Asker."
                ),
                "reviewedAt": "2026-08-20",
            }]
        node_rows[key] = {
            "id": f"EXP:{key}",
            "cc": row["country"],
            "name": row["name"],
            "rolle": " / ".join(row.get("roles") or []),
            "rollen": row.get("roles") or [],
            "relevanz": clean_sentence(row.get("relevance") or ""),
            "actor_degree": row.get("grade", "bezug"),
            "beleg_url": source_url,
            "evidence": evidence,
            "strict_review": True,
            "expansion_review_run": REVIEW_RUN,
        }
        loader_nodes.append({
            "eid": key,
            "cc": row["country"],
            "kind": row["kind"],
            "type": None if is_project else TYPE_MAP[row["entityType"]],
            "name": row["name"],
            "roles": row.get("roles") or [],
            "source_url": source_url,
        })

    if len(final_edges) != 190:
        raise RuntimeError(f"unexpected final edge count: {len(final_edges)} != 190")
    if len(loader_nodes) != 191:
        raise RuntimeError(f"unexpected final node count: {len(loader_nodes)} != 191")
    if any(len(row["beschreibung"]) > 60 for row in final_edges):
        raise RuntimeError("description length gate failed")

    OUT.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": 1,
        "approved_for_latex": True,
        "neo4j_changed": False,
        "review_run": REVIEW_RUN,
        "source_path": str(SOURCE),
        "source_sha256": sha256(SOURCE),
        "approved_corrections_sha256": sha256(APPROVED),
        "nodes": loader_nodes,
        "edges": final_edges,
        "removed_edges": STRICT_REMOVALS,
        "not_applied": {
            "proposal:proj:106:B:4": (
                "Brukspecialisten–Borås is omitted: the source does not "
                "unambiguously assign the delivery role."
            )
        },
        "merge_redirects": {MERGE_SOURCE: MERGE_TARGET},
    }
    OUT_DATA.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    OUT_NODES.write_text(
        json.dumps(node_rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    OUT_EDGES.write_text(
        json.dumps(
            {row["id"]: row for row in final_edges},
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    countries = Counter(row["cc"] for row in loader_nodes)
    node_kinds = Counter(row["kind"] for row in loader_nodes)
    evidence_kinds = Counter(row["evidence_text_kind"] for row in final_edges)
    lines = [
        "# Finale Erweiterung des LaTeX-Akteursnetzes",
        "",
        "Status: **fachlich freigegeben und lokal aktiviert**",
        "",
        f"- Neue sichtbare Knoten: **{len(loader_nodes)}**",
        f"  - Akteure: **{node_kinds['actor']}**",
        f"  - Projekte: **{node_kinds['project']}**",
        f"- Neue belegte Kanten: **{len(final_edges)}**",
        "- Jede neue Kante mit Quellen-URL: **ja**",
        "- Jede neue Kante mit Belegtext oder Prüfnotiz: **ja**",
        "- Jede Beschreibung höchstens 60 Zeichen: **ja**",
        f"- Profil aller neuen Kanten: **{PROFILE}**",
        "- Neo4j geändert: **nein**",
        "- E:\\semio geändert: **nein**",
        "",
        "## Streng entfernt",
        "",
    ]
    for key, reason in STRICT_REMOVALS.items():
        lines.append(f"- `{key}` – {reason}")
    lines.extend([
        "- `proposal:proj:106:B:4` – Brukspecialisten–Borås wurde nicht "
        "ergänzt; die genaue Lieferrolle bleibt unklar.",
        "",
        "## Korrekturen",
        "",
        "- `Jardin de la Caserne de Reuilly` → `La Caserne de Reuilly`.",
        "- Zwei BAM-Bezeichnungen wurden zu `BAM Bouw en Techniek` zusammengeführt.",
        "- Norsk Folkemuseum wurde mit dem belegten Zielprojekt `TradLab TRE` verbunden.",
        "- CONIX RDBM erhielt den belastbaren Rotor-Beleg.",
        "- Teilbelegte Rollen wurden korrigiert oder konservativ herabgestuft.",
        "",
        "## Belegtext",
        "",
        f"- Quellenzitate/-ausschnitte: **{evidence_kinds['source_excerpt']}**",
        f"- Gespeicherte relationsspezifische Prüfnotizen: **{evidence_kinds['review_note']}**",
        "",
        "## Neue Knoten nach Land",
        "",
    ])
    for cc in sorted(countries):
        lines.append(f"- {cc}: **{countries[cc]}**")
    OUT_AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"PASS: {len(loader_nodes)} expansion nodes, {len(final_edges)} sourced edges, "
        f"descriptions<=60, profiles={PROFILE!r}"
    )


if __name__ == "__main__":
    main()
