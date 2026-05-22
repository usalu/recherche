"""Build sidecar evidence layer and regenerate enriched patches."""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from _evidence_claims import CLAIMS, EDGE_CLAIM_MAP
from _generate_evidence_patches import (
    EVIDENCE_BASIS,
    REVIEW_RUN,
    RUN,
    SOURCES,
    main as regenerate_patches,
    phase0,
    phase1,
    phase2,
    phase3,
    write_jsonl,
    PATCHES,
    OUT,
)

SIDECAR = OUT / "sidecar"
NOW = datetime.now(timezone.utc).isoformat()


def sidecar_key_rel(rel_type: str, from_id: str, to_id: str) -> str:
    return f"rel:{rel_type}:{from_id}->{to_id}"


def enrich_rel(props: dict, rel_type: str, from_id: str, to_id: str) -> dict:
    rid = props.get("id", "")
    claim_ids = EDGE_CLAIM_MAP.get(rid, [])
    if not claim_ids:
        return props

    primary = CLAIMS[claim_ids[0]]
    if primary.get("importable_as_graph_fact") is False:
        props["evidence_confidence"] = primary["confidence"]
        props["evidence_basis"] = "interpretive_conclusion_not_sourced_merge"
    else:
        props["evidence_quote"] = primary.get("quote_short", props.get("evidence_quote", ""))[:240]
        props["evidence_excerpt"] = primary.get("quote_verbatim", "")[:500]
        props["evidence_confidence"] = primary["confidence"]

    props["evidence_claim_ids"] = claim_ids
    props["evidence_origin"] = (
        "live_url_capture" if primary.get("capture_method", "").startswith("live_fetch") else "dossier_anchored"
    )
    props["dossier_section"] = primary.get("dossier_section", "")
    props["fact_label"] = primary.get("label", "Fact")

    corroborating = primary.get("corroborating_source_ids", [])
    if corroborating:
        props["secondary_evidence_source_ids"] = corroborating

    props["metadata_sidecar_key"] = sidecar_key_rel(rel_type, from_id, to_id)
    return props


def enrich_phase(rows: list[dict]) -> list[dict]:
    out = []
    for row in rows:
        if row.get("op") != "add_rel":
            out.append(row)
            continue
        props = enrich_rel(
            dict(row["properties"]),
            row["type"],
            row["from"],
            row["to"],
        )
        out.append({**row, "properties": props})
    return out


def write_sidecar(rows_by_phase: dict[str, list[dict]]) -> None:
    SIDECAR.mkdir(parents=True, exist_ok=True)

    # claims.jsonl
    claim_rows = []
    for cid, c in CLAIMS.items():
        claim_rows.append({"record_type": "claim", "claim_id": cid, **c})
    (SIDECAR / "claims.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in claim_rows) + "\n",
        encoding="utf-8",
    )

    # url_captures.jsonl — verbatim excerpts tied to source ids
    captures = []
    for url, meta in SOURCES.items():
        claim_match = next(
            (c for c in CLAIMS.values() if c.get("primary_url") == url or c.get("primary_source_id") == meta["id"]),
            None,
        )
        captures.append(
            {
                "record_type": "url_capture",
                "source_id": meta["id"],
                "url": url,
                "name": meta["name"],
                "quote_verbatim": claim_match["quote_verbatim"] if claim_match else meta["quote"],
                "quote_short": claim_match["quote_short"] if claim_match else meta["quote"][:240],
                "confidence": meta["confidence"],
                "capture_method": claim_match.get("capture_method", "dossier_register") if claim_match else "dossier_register",
                "captured_at": NOW,
            }
        )
    (SIDECAR / "url_captures.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in captures) + "\n",
        encoding="utf-8",
    )

    # edge_evidence.jsonl — full dossier per relationship
    edge_rows = []
    for phase, rows in rows_by_phase.items():
        for row in rows:
            if row.get("op") != "add_rel":
                continue
            p = row["properties"]
            rid = p.get("id", "")
            claim_ids = p.get("evidence_claim_ids", EDGE_CLAIM_MAP.get(rid, []))
            claims_payload = [{k: v for k, v in CLAIMS[cid].items()} | {"claim_id": cid} for cid in claim_ids if cid in CLAIMS]
            edge_rows.append(
                {
                    "record_type": "edge_evidence",
                    "phase": phase,
                    "rel_id": rid,
                    "rel_type": row["type"],
                    "from_id": row["from"],
                    "to_id": row["to"],
                    "metadata_sidecar_key": p.get("metadata_sidecar_key"),
                    "graph_properties": {
                        k: p[k]
                        for k in [
                            "evidence_url",
                            "evidence_quote",
                            "evidence_excerpt",
                            "evidence_confidence",
                            "evidence_basis",
                            "evidence_origin",
                            "evidence_claim_ids",
                            "secondary_evidence_source_ids",
                            "dossier_section",
                            "fact_label",
                            "connection_kind",
                        ]
                        if k in p
                    },
                    "claims": claims_payload,
                }
            )
    (SIDECAR / "edge_evidence.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in edge_rows) + "\n",
        encoding="utf-8",
    )

    manifest = {
        "run": RUN,
        "review_run": REVIEW_RUN,
        "evidence_basis": EVIDENCE_BASIS,
        "generated_at": NOW,
        "counts": {
            "claims": len(claim_rows),
            "url_captures": len(captures),
            "edge_evidence": len(edge_rows),
            "interpretive_claims": sum(1 for c in CLAIMS.values() if c.get("label") == "Interpretive_conclusion"),
        },
        "tiers": {
            "tier1_graph": "evidence_quote (≤240) + evidence_confidence on rel",
            "tier2_sidecar_claims": "claims.jsonl atomic facts with corroboration",
            "tier3_sidecar_captures": "url_captures.jsonl verbatim excerpts + fetch metadata",
        },
    }
    (SIDECAR / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    # CLAIM_INDEX.csv
    with (OUT / "CLAIM_INDEX.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(
            [
                "rel_id",
                "rel_type",
                "from_id",
                "to_id",
                "claim_ids",
                "fact_label",
                "confidence",
                "dossier_section",
                "primary_url",
                "corroborating_count",
                "metadata_sidecar_key",
            ]
        )
        for er in edge_rows:
            gp = er["graph_properties"]
            primary_url = er["claims"][0]["primary_url"] if er["claims"] else ""
            w.writerow(
                [
                    er["rel_id"],
                    er["rel_type"],
                    er["from_id"],
                    er["to_id"],
                    ";".join(gp.get("evidence_claim_ids", [])),
                    gp.get("fact_label", ""),
                    gp.get("evidence_confidence", ""),
                    gp.get("dossier_section", ""),
                    primary_url,
                    len(gp.get("secondary_evidence_source_ids", [])),
                    er.get("metadata_sidecar_key", ""),
                ]
            )


def add_corroborating_belegt_in(phase1_rows: list[dict]) -> list[dict]:
    """Second BELEGT_IN URL for Bauteilbörse-pattern marketplace actors."""
    extra = [
        ("useagain_bauteilclick", "q_url_82ad61e4b3672c05a8fedf46e57faee6"),
        ("useagain_bauteilclick", "q_url_9fce1894aaa7455c757369850397e39f"),
        ("salza", "q_url_45d7c6380377a9cec952dbf6c3f2ba8c"),
        ("materiuum", "q_url_56649f37d5b1ee18d083da852797c756"),
        ("bauteilladen_winterthur", "q_url_48e67450f81ae55a6012813987faf31e"),
        ("wick_reuse_roto_baumarkt", "q_url_161aca331467d6b5bd144e83b6837af4"),
    ]
    from _generate_evidence_patches import add_rel

    dossier = "q_research_swiss_reuse_bubble_v2_md"
    rows = list(phase1_rows)
    for actor, sid in extra:
        rows.append(
            add_rel(
                actor,
                sid,
                "BELEGT_IN",
                f"r_{actor}__belegt_in__{sid}",
                sid,
                archive_source_id=dossier,
                evidence_basis="corroborating_first_party_url",
            )
        )
    return rows


def main() -> None:
    from _generate_evidence_patches import add_rel

    p0 = phase0()
    p1 = add_corroborating_belegt_in(phase1())
    p2 = phase2()
    p2.append(
        add_rel(
            "sumami",
            "q_url_422166f604d091d32cff814ca59194f2",
            "BELEGT_IN",
            "r_sumami__belegt_in__q_url_422166f604d091d32cff814ca59194f2",
            "q_url_422166f604d091d32cff814ca59194f2",
            archive_source_id="q_research_swiss_reuse_bubble_v2_md",
            evidence_basis="corroborating_first_party_url",
        )
    )
    p3 = phase3()

    # Upgrade sumami↔useagain to belegt (live ETH capture)
    for row in p3:
        if row.get("op") == "add_rel" and row["properties"].get("id") == "r_sumami__verbunden_mit_akteur__useagain_bauteilclick":
            row["properties"]["evidence_confidence"] = "belegt"
            row["properties"]["evidence_basis"] = "first_party_research_page"
            row["properties"]["evidence_quote"] = CLAIMS["claim_sumami_develops_useagain"]["quote_short"]

    phases = {
        "phase0": enrich_phase(p0),
        "phase1": enrich_phase(p1),
        "phase2": enrich_phase(p2),
        "phase3": enrich_phase(p3),
    }

    PATCHES.mkdir(parents=True, exist_ok=True)
    write_jsonl(PATCHES / "phase0_sources_and_dossier.patch.jsonl", phases["phase0"])
    write_jsonl(PATCHES / "phase1_enrichment_connectivity.patch.jsonl", phases["phase1"])
    write_jsonl(PATCHES / "phase2_new_nodes.patch.jsonl", phases["phase2"])
    write_jsonl(PATCHES / "phase3_supply_chain.patch.jsonl", phases["phase3"])

    write_sidecar(phases)
    print(f"Evidence layer built: {len(CLAIMS)} claims, {SIDECAR}")


if __name__ == "__main__":
    main()
