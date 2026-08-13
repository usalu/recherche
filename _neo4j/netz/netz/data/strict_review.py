"""Inactive-by-default loader and applier for the report-only strict review.

Neo4j remains untouched.  The layer becomes active only when the frozen
review manifest explicitly contains ``approved_for_render_prune: true`` and
all finalized artifacts exist.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from ._identity import ISO_INV


@dataclass(frozen=True)
class StrictReviewBundle:
    active: bool = False
    exclude: frozenset = frozenset()
    programmes: frozenset = frozenset()
    redirects: dict = field(default_factory=dict)
    overrides: dict = field(default_factory=dict)
    classification: dict = field(default_factory=dict)


def _load(path: str):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def load_strict_review(manifest_path: str, prune_path: str, redirects_path: str,
                       overrides_path: str, classification_path: str) -> StrictReviewBundle:
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        return StrictReviewBundle()
    manifest = _load(manifest_path)
    if not manifest.get("approved_for_render_prune"):
        return StrictReviewBundle()

    required = [prune_path, redirects_path, overrides_path, classification_path]
    missing = [p for p in required if not Path(p).exists()]
    if missing:
        raise RuntimeError(f"approved strict review is incomplete; missing {missing}")

    exclude = frozenset(_load(prune_path))
    redirects = _load(redirects_path)
    overrides = _load(overrides_path)
    classification = _load(classification_path)
    programmes = frozenset(
        eid for eid, row in classification.items()
        if row.get("report_entity_type") == "Programm"
    )
    if set(redirects) - exclude:
        raise RuntimeError("every merge source must also be excluded")
    if set(classification) & exclude:
        raise RuntimeError("strict classification contains excluded EIDs")
    return StrictReviewBundle(
        active=True,
        exclude=exclude,
        programmes=programmes,
        redirects=redirects,
        overrides=overrides,
        classification=classification,
    )


def apply_strict_review(raw, new_proj_cc: dict, bundle: StrictReviewBundle) -> None:
    """Apply report-only redirects and overrides to an in-memory RawGraph."""
    if not bundle.active:
        return

    # The approved strict classification, not legacy graph roles, drives the
    # report. Every kept EID must be covered.
    for eid, row in bundle.classification.items():
        if eid not in raw.by:
            raise RuntimeError(f"strict classification EID absent: {eid}")
        raw.roles[eid] = set(row.get("rollen") or [])

    # Redirect semantic duplicates before removing their source nodes.
    for source, target in bundle.redirects.items():
        if source not in raw.by or target not in raw.by:
            raise RuntimeError(f"strict merge endpoint absent: {source} -> {target}")
        for eid in list(raw.part):
            if source in raw.part[eid]:
                raw.part[eid].discard(source)
                if eid != target:
                    raw.part[eid].add(target)
        for eid in list(raw.peers):
            if source in raw.peers[eid]:
                raw.peers[eid].discard(source)
                if eid != target:
                    raw.peers[eid].add(target)
                    raw.peers[target].add(eid)
        raw.peers.pop(source, None)
        raw.part.pop(source, None)

    # Report-only identity/type/country corrections.
    for eid, override in bundle.overrides.items():
        if eid not in raw.by:
            raise RuntimeError(f"strict override EID absent: {eid}")
        if override.get("corrected_name"):
            raw.by[eid]["properties"]["name"] = override["corrected_name"]

        corrected_type_raw = (override.get("corrected_type") or "").strip()
        corrected_type = corrected_type_raw.lower()
        is_actor = any(a["eid"] == eid for a in raw.actors)
        is_project = eid in raw.projects
        actor_type = None
        if corrected_type_raw in {
            "Unternehmen", "Materialhub_Bauteilboerse", "Forschung_Lehre",
            "NGO_Verband_Netzwerk", "Oeffentliche_Institution",
            "Software_Tool_Anbieter", "Organisation",
            "Foerdergeber_Programmtraeger", "Unbekannt", "Person",
        }:
            actor_type = corrected_type_raw
        if (corrected_type in {"actor", "akteur", "organisation", "organization"}
                or actor_type) and is_project:
            raw.projects = [x for x in raw.projects if x != eid]
            raw.actors.append(raw.by[eid])
            raw.by[eid]["labels"] = ["Akteur"]
            # Former incoming project participation becomes an actor tie.
            for actor in raw.actors:
                aid = actor["eid"]
                if eid in raw.part[aid]:
                    raw.part[aid].discard(eid)
                    if aid != eid:
                        raw.peers[aid].add(eid)
                        raw.peers[eid].add(aid)
        if actor_type:
            raw.types[eid] = actor_type
        elif corrected_type in {"project", "projekt", "bauvorhaben", "objekt"} and is_actor:
            peers = set(raw.peers.get(eid, ()))
            for peer in peers:
                raw.peers[peer].discard(eid)
                if peer != eid:
                    raw.part[peer].add(eid)
            raw.peers.pop(eid, None)
            raw.part.pop(eid, None)
            raw.actors = [a for a in raw.actors if a["eid"] != eid]
            raw.projects = sorted(set(raw.projects) | {eid}, key=lambda x: (raw.name(x), x))
            raw.by[eid]["labels"] = ["Projekt"]

        corrected_country = override.get("corrected_country")
        if corrected_country:
            if eid in raw.projects:
                new_proj_cc[eid] = corrected_country
            else:
                country_name = ISO_INV.get(corrected_country)
                if not country_name:
                    raise RuntimeError(f"unsupported country override {corrected_country} for {eid}")
                raw.land[eid] = country_name

    # Excluded EIDs remain in raw.by for endpoint/name lookups but cannot be
    # reached by an active peer/participation relationship.
    for source in bundle.exclude:
        for eid in list(raw.part):
            raw.part[eid].discard(source)
        for eid in list(raw.peers):
            raw.peers[eid].discard(source)
        raw.peers.pop(source, None)
        raw.part.pop(source, None)

    # Fail closed: the approved classification is the complete report
    # universe. Legacy graph nodes not represented there (for example a
    # partner-list-only Arup node) must not leak back into the actor view.
    allowed = set(bundle.classification)
    raw.actors = [actor for actor in raw.actors if actor["eid"] in allowed]
    raw.projects = [eid for eid in raw.projects if eid in allowed]
