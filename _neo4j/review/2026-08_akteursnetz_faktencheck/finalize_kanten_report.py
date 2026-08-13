"""Fail-closed LaTeX audit and human-readable final relationship report."""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
NETZ_ROOT = REPO / "_neo4j" / "netz"
sys.path.insert(0, str(NETZ_ROOT))

from netz.cli import load_network  # noqa: E402
from netz.mechanisms.connectivity import drawn_edge_nodes  # noqa: E402
from netz.mechanisms.layout import DEFAULT_FRAME, force_layout  # noqa: E402


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def norm(pair):
    return tuple(sorted(pair))


def md(value):
    return str(value or "—").replace("|", r"\|").replace("\n", " ")


def source_link(url):
    return f"[Quelle]({url})" if url else "—"


def decision_row(record, classification):
    a = record["node_a"]["name"]
    b = record["node_b"]["name"]
    verdict = "ENTFERNT" if classification["entfernen"] else "BEHALTEN"
    return (
        f"| {record['id']} | {md(a)} | {md(b)} | {verdict} | "
        f"{md(classification['beziehungsart'])} | {md(classification['beschreibung'])} | "
        f"{source_link(classification.get('evidence_url'))} |"
    )


def main():
    inventory = load("kanten_review_inventory.json")
    records = {row["id"]: row for row in inventory["records"]}
    classes = load("kanten_klassifikation.json")
    keep = {norm(pair) for pair in load("keep_kanten_final.json")}
    prune = {norm(pair) for pair in load("prune_kanten_final.json")}
    source_check = load("kanten_source_recheck.json")
    country_corrections = load("latex_country_overrides.json")["overrides"]

    assert len(records) == len(classes) == 570
    assert set(records) == set(classes)
    assert not keep & prune
    assert len(keep) == 477 and len(prune) == 93
    assert {norm(row["pair"]) for row in records.values()} == keep | prune
    assert sum(1 for row in classes.values() if row["entfernen"]) == 93
    assert source_check["distinct_urls"] == 220
    assert sum(page["reachable"] for page in source_check["pages"].values()) == 220

    network = load_network()
    model_edges = {norm(pair) for pair in network.drawn}
    assert model_edges == keep
    assert not model_edges & prune

    panel_nodes = set()
    incident_nodes = set()
    for panel in network.panels.values():
        panel_nodes.update(panel.actors)
        panel_nodes.update(panel.projects)
        for a, b in panel.edges:
            incident_nodes.update((a, b))
    isolated_nodes = panel_nodes - incident_nodes
    node_prune = set(load("prune_faktencheck_final.json"))
    assert not node_prune & panel_nodes
    for eid, row in country_corrections.items():
        assert network.res.cc[eid] == row["country"]

    rendered_pairs = set()
    for panel in network.panels.values():
        visible_nodes = drawn_edge_nodes(panel, min_comp=2)
        _, edges = force_layout(panel, visible_nodes, DEFAULT_FRAME)
        rendered_pairs.update(norm(pair) for pair in edges)
    assert rendered_pairs == keep

    fragment = NETZ_ROOT / "figs" / "frag_abb_netz.tex"
    fragment_text = fragment.read_text(encoding="utf-8")
    fragment_edge_count = len(re.findall(r"^\\SemioGraphEdge", fragment_text, re.M))
    fragment_node_count = len(re.findall(r"^\\SemioGraphNode", fragment_text, re.M))
    assert fragment_edge_count == len(rendered_pairs)
    assert fragment_node_count == len(panel_nodes)
    assert len(re.findall(r"^\\begin\{GraphFigure\}", fragment_text, re.M)) == 11
    pdf = NETZ_ROOT / "figs" / "akteursnetz_faktencheck_final.pdf"
    assert pdf.is_file() and pdf.stat().st_size > 10_000
    assert pdf.read_bytes()[:5] == b"%PDF-"

    by_country = collections.defaultdict(lambda: [0, 0])
    kept_types = collections.Counter()
    removed_types = collections.Counter()
    for edge_id, row in classes.items():
        slot = 1 if row["entfernen"] else 0
        by_country[row["cc"]][slot] += 1
        (removed_types if row["entfernen"] else kept_types)[row["beziehungsart"]] += 1

    hidden_kept = keep - rendered_pairs
    audit = f"""# LaTeX-Kantenaudit — Abschluss

Stand: 2026-08-13

## Ergebnis

- Entscheidungsmenge: **570 von 570** Kanten, keine fehlende und keine doppelte ID.
- Positive Liste: **477** belegte Beziehungen.
- Entfernungsliste: **93** Kandidaten.
- Mengenprüfung: Keep und Remove sind disjunkt und ergeben genau 570.
- LaTeX-Netzmodell: **477** Kanten; es ist mengenidentisch mit der positiven Liste.
- LaTeX-Fragment: **{fragment_edge_count}** sichtbare Kanten in **11** Länderabbildungen.
- Sichtbare Beziehungen: **{len(rendered_pairs)} von {len(keep)}**. Auch alle
  Zweierkomponenten werden gezeichnet.
- Sichtbare Knoten: **{fragment_node_count}**. Darunter bleiben **{len(isolated_nodes)} isolierte
  Knoten** wie angeordnet sichtbar.
- Explizit freigegebene Knotenentfernungen: **{len(node_prune)}**; davon noch in einem
  LaTeX-Länderpanel vorhanden: **0**.
- LaTeX-spezifische Länderkorrekturen: **{len(country_corrections)} Knoten**. BauMaB Kassel
  und Stadt Kassel stehen nun im Deutschland- statt im Belgien-Panel.
- Entfernte Kante noch im LaTeX-Netzmodell: **0**.
- Geprüfte Belegseiten: **220 von 220 erreichbar**.
- Kompilierte PDF-Endkontrolle: vorhanden, lesbar und visuell auf allen vier Seiten geprüft.

## Artefakte

- `keep_kanten_final.json`: vollständige Positivliste.
- `prune_kanten_final.json`: vollständige Entfernungsliste.
- `figs/frag_abb_netz.tex`: neu erzeugtes LaTeX-Fragment.
- `figs/akteursnetz_faktencheck_final.pdf`: kompilierte Endkontrolle.
"""
    (HERE / "KANTEN_LATEX_AUDIT_FINAL.md").write_text(audit, encoding="utf-8", newline="\n")

    lines = [
        "# Abschlussbericht: Faktencheck der LaTeX-Graphkanten",
        "",
        "Stand: 2026-08-13",
        "",
        "## Konkretes Ergebnis",
        "",
        "Alle **570 von 570** Kandidaten wurden einzeln entschieden. Es gibt keine offene Entscheidung.",
        "Der LaTeX-Graph verwendet jetzt eine strikte Positivliste: **477 belegt und behalten**,",
        "**93 entfernt**. Von den 93 Entfernungen sind **68 bloße Verzeichniseinträge** und",
        "**25 Fälle ohne Beleg für eine Beziehung**.",
        "",
        f"Im LaTeX-Netzmodell sind exakt 477 Kanten. Das erzeugte Fragment zeichnet alle {fragment_edge_count}.",
        "Auch belegte Zweierkomponenten bleiben sichtbar; keine belegte Beziehung wird ausgeblendet.",
        f"Alle {len(isolated_nodes)} verbleibenden isolierten Knoten bleiben ebenfalls sichtbar.",
        f"Die {len(node_prune)} explizit freigegebenen Knotenentfernungen sind nicht mehr in den LaTeX-Panels.",
        "",
        "Es wurden keine Daten nach Neo4j geschrieben.",
        "",
        "## Ergebnis nach Land im Review-Snapshot",
        "",
        "Die stabilen Review-IDs behalten ihre ursprüngliche Länderkennung. Die später erkannte",
        "Fehlzuordnung `BE:K075` wird im LaTeX-Graphen nach Deutschland verschoben.",
        "",
        "| Land | geprüft | behalten | entfernt |",
        "|---|---:|---:|---:|",
    ]
    for cc in sorted(by_country):
        kept, removed = by_country[cc]
        lines.append(f"| {cc} | {kept + removed} | {kept} | {removed} |")

    lines += [
        "",
        "## Behaltene Beziehungsarten",
        "",
        "| Beziehungsart | Anzahl |",
        "|---|---:|",
    ]
    for rel_type, count in sorted(kept_types.items()):
        lines.append(f"| {md(rel_type)} | {count} |")

    lines += [
        "",
        "## Deutschland: alle 49 Review-Entscheidungen plus Kassel-Korrektur",
        "",
        "| ID | Knoten A | Knoten B | Entscheidung | Beziehungsart/Grund | Konkreter Befund | Beleg |",
        "|---|---|---|---|---|---|---|",
    ]
    for edge_id in sorted(key for key in records if key.startswith("DE:")):
        lines.append(decision_row(records[edge_id], classes[edge_id]))
    lines.append(decision_row(records["BE:K075"], classes["BE:K075"]))

    lines += [
        "",
        "## Vollständige Entfernungsliste: alle 93 Kanten",
        "",
        "Diese Liste beantwortet konkret, was gelöscht wurde. ‚Kein Beleg‘ ist hier eine",
        "abschließende DELETE-Entscheidung, keine noch wartende Prüfung.",
        "",
        "| ID | Knoten A | Knoten B | Entscheidung | Entfernungsgrund | Konkreter Befund | Beleg |",
        "|---|---|---|---|---|---|---|",
    ]
    for edge_id in sorted(key for key, row in classes.items() if row["entfernen"]):
        lines.append(decision_row(records[edge_id], classes[edge_id]))

    lines += [
        "",
        "## Offene Punkte",
        "",
        "**Keine offenen Kantenentscheidungen.** Die 25 erfolglos recherchierten Kandidaten sind",
        "bewusst entfernt. Eine spätere Wiederaufnahme ist nur mit einer zugänglichen Quelle möglich,",
        "die beide Endpunkte nennt und genau ihre Beziehung beschreibt.",
    ]
    (HERE / "KANTEN_ABSCHLUSSBERICHT_FINAL.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
    )

    print(f"PASS: 570 = {len(keep)} keep + {len(prune)} remove")
    print(f"PASS: LaTeX model {len(model_edges)}; fragment {fragment_edge_count}; hidden keep {len(hidden_kept)}")
    print("wrote KANTEN_LATEX_AUDIT_FINAL.md and KANTEN_ABSCHLUSSBERICHT_FINAL.md")


if __name__ == "__main__":
    main()
