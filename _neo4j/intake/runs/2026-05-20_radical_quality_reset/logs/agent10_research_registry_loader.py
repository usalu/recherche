"""Agent 10 — Wave 4 loader (Phase 4b.2 + Phase 4b.3) for `mit-bestand`.

Scope (per plan §4b.2 + §4b.3, scoped to this agent):

  4b.2 — Research-file ingestion (Level 2, link-only)
    For each of 8 research markdown files under inbox/research/:
      1. MERGE q_<filename>_md :Quelle, quelltyp='research_markdown'.
      2. Extract every URL in the file body. MERGE child :Quelle with
         quelltyp='external_reference', id='q_research_<file>_url_<hash8>',
         then MERGE q_anchor -[:ZITIERT_QUELLE]-> q_url.
      3. Extract every domain-vocab ID embedded in table prose
         (`av_*`, `vt_*`, `pr_*`, `s_*`, `rb_*`, `la_*`). MERGE the
         domain node with its correct label (idempotent for existing
         nodes). Wire a `(domain)-[:BELEGT_IN]->(q_anchor)` edge with
         `evidence_origin='inferred'`, `evidence_basis='research_file_row'`,
         `evidence_confidence='inferiert'` so the research file becomes
         the canonical anchor for the vocab term.
      4. Project edges (only `:Projekt -[HAT_AUFBEREITUNG / HAT_VERBINDUNGSTECHNIK
         / HAT_PRUEFUNG / HAT_SCHADSTOFF / HAT_RECHTLICHE_BEDINGUNG]-> domain`)
         get materialised only for the small conservative whitelist of
         well-known project tokens that appear in the same row as a
         domain ID AND the row's textual evidence column reads BELEGT /
         "directly documents" / similar positive marker. evidence_origin
         is `curated`, basis `cell_citation`, excerpt is the row text,
         source_id is the URL :Quelle if found else the anchor.

  4b.3 — Actor registry (mixed Level 1 / Level 3)
    For every actor_registry_seed/**/*.registry.kg.jsonl batch:
      1. MERGE q_akteursliste_master_md :Quelle (the registry anchor).
      2. Replay every record through MERGE-only writes:
           * Nodes: MERGE by id; preserve labels; merge non-null props.
           * Rels:
             - HAT_AKTEURROLLE / HAT_AKTEURTYP →
               evidence_origin='curated', basis='controlled_vocab',
               source_id='q_akteursliste_master_md',
               confidence='belegt', excerpt=NULL.
             - ASSOZIIERT_MIT_PROJEKT →
               evidence_origin='curated', basis='registry_stub',
               source_id='q_akteursliste_master_md',
               confidence='teilweise_belegt'; preserve needs_verification.
             - Akteur -[BELEGT_IN]-> q_actor_*_NN  (the per-actor URL Quelle)
               evidence_origin='curated', basis='cell_citation',
               source_id=target.id, confidence='belegt'.
             - q_akteursliste_master_md -[ZITIERT_QUELLE]-> q_actor_* (NEW —
               this is the structural fix the plan demands: the registry
               markdown CITES the per-actor URL; previous transform
               wrongly folded it into BELEGT_IN). Evidence: derived /
               case_markdown_sources / unklar.
             - LIEGT_IN_LAND → curated / controlled_vocab / belegt.
             - VERBUNDEN_MIT_AKTEUR → curated / controlled_vocab / belegt.
           * SKIP: any Projekt -[BELEGT_IN]-> q_actor_*  (Agent 8 deleted
             these 176 spurious edges; recreating them violates §4c.3).
           * SKIP: any Projekt -[BELEGT_IN]-> q_akteursliste_master_md
             (same scope).

Idempotency: every write is a MERGE on stable id; re-runs are no-ops on
properties already at the canonical shape.  Counts are recorded into
agent10_result.json and emitted to PHASE_4B_2_DONE.flag /
PHASE_4B_3_DONE.flag.

Boundary respected: this loader does NOT touch the 76 gebaeude/ or
21 batch2/ case-study dossiers (Agent 9 scope). It also does NOT
re-introduce any of the 4c invariants Agent 8 enforced.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = (
    REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-20_radical_quality_reset"
)
LOG_DIR = RUN_ROOT / "logs"
REPORTS_DIR = RUN_ROOT / "reports"
FLAG_4B2 = RUN_ROOT / "PHASE_4B_2_DONE.flag"
FLAG_4B3 = RUN_ROOT / "PHASE_4B_3_DONE.flag"
PROGRESS_LOG = LOG_DIR / "agent10_progress.log"
RESULT_JSON = LOG_DIR / "agent10_result.json"

RESEARCH_DIR = REPO_ROOT / "_neo4j" / "intake" / "inbox" / "research"
REGISTRY_GLOB = (
    REPO_ROOT
    / "_neo4j"
    / "intake"
    / "archive"
    / "2026-05-15_actor_registry_seed"
)


# ---------------------------------------------------------------------------
# Research-file → anchor :Quelle id, primary domain-vocab label, and label
# the research file maps onto when it embeds vocab IDs with that prefix.
# ---------------------------------------------------------------------------
RESEARCH_FILES: dict[str, dict[str, Any]] = {
    "aufbereitungsverfahren_reused_building_elements.md": {
        "anchor_id": "q_aufbereitungsverfahren_reused_building_elements_md",
        "title": "Aufbereitungsverfahren for Reused Building Elements",
        "name": "aufbereitungsverfahren_reused_building_elements.md",
    },
    "connection_techniques_bauteilreuse.md": {
        "anchor_id": "q_connection_techniques_bauteilreuse_md",
        "title": "Connection Techniques in Bauteilreuse",
        "name": "connection_techniques_bauteilreuse.md",
    },
    "testing_verification_bauteilreuse_kg.md": {
        "anchor_id": "q_testing_verification_bauteilreuse_kg_md",
        "title": "Testing and Verification Methods for Reused Building Elements",
        "name": "testing_verification_bauteilreuse_kg.md",
    },
    "bauteilreuse_legal_regime_matrix.md": {
        "anchor_id": "q_bauteilreuse_legal_regime_matrix_md",
        "title": "Legal and regulatory conditions affecting Bauteilreuse",
        "name": "bauteilreuse_legal_regime_matrix.md",
    },
    "schadstoff_reuse_knowledge_graph_research.md": {
        "anchor_id": "q_schadstoff_reuse_knowledge_graph_research_md",
        "title": "Schadstoff research note for circular construction",
        "name": "schadstoff_reuse_knowledge_graph_research.md",
    },
    "circular_construction_reuse_graph_gaps.md": {
        "anchor_id": "q_circular_construction_reuse_graph_gaps_md",
        "title": "Country x Material Graph Gaps for Circular Construction",
        "name": "circular_construction_reuse_graph_gaps.md",
    },
    "circular_construction_economics_kg.md": {
        "anchor_id": "q_circular_construction_economics_kg_md",
        "title": "Economic Dimension of a Circular Construction Knowledge Graph",
        "name": "circular_construction_economics_kg.md",
    },
    "energy_climate_reuse_research.md": {
        "anchor_id": "q_energy_climate_reuse_research_md",
        "title": "Energy and Climate Dimension for Circular Construction",
        "name": "energy_climate_reuse_research.md",
    },
}

# Vocab prefix → (Node label, project-edge relationship type or None).
# The first label is canonical for new MERGE-creations; existing nodes keep
# whatever labels they have because Neo4j MERGE matches on id regardless of
# label. If a domain ID prefix is unknown we silently ignore it.
VOCAB_PREFIX_LABEL: dict[str, tuple[str, str | None]] = {
    "av":   ("Aufbereitungsverfahren",  "HAT_AUFBEREITUNG"),
    "vt":   ("Verbindungstechnik",      "HAT_VERBINDUNGSTECHNIK"),
    "pr":   ("PruefungNachweis",        "HAT_PRUEFUNG"),
    "pn":   ("PruefungNachweis",        "HAT_PRUEFUNG"),
    "s":    ("Schadstoff",              "HAT_SCHADSTOFF"),
    "rb":   ("RechtlicheBedingung",     "HAT_RECHTLICHE_BEDINGUNG"),
    "la":   ("Leistungsanforderung",    None),       # no project edge wiring
    "mat":  ("Material",                None),
    "bt":   ("Bauteiltyp",              None),
}

# Conservative project-name → live projekt id whitelist. Only used to
# materialise project edges from research-file rows. The token must
# appear in the row text AND the row text must contain a positive
# evidence marker (BELEGT / "documents" / "documented" / "documentiert"
# / "bestätigt" / "directly documents") AND no negative marker
# (e.g. "no project-specific BELEGT" / "nicht belegt" / "INFER" / "not
# found" / "no project source"). This is intentionally narrow so that
# silent over-claiming is impossible.
PROJECT_NAME_LOOKUP: dict[str, str] = {
    "K.118":                                  "p_k118_kopfbau_halle_118_winterthur",
    "K118":                                   "p_k118_kopfbau_halle_118_winterthur",
    "Kopfbau Halle 118":                      "p_k118_kopfbau_halle_118_winterthur",
    "Juch-Areal":                             "p_juch_areal_recyclingzentrum_zuerich",
    "Juch Areal":                             "p_juch_areal_recyclingzentrum_zuerich",
    "Villa Welpeloo":                         "p_villa_welpeloo_enschede",
    "CascadeUp":                              "p_cascadeup_london_secondary_timber_glulam_demonstrator",
    "Resource Rows":                          "p_resource_rows_copenhagen",
    "Plattenpalast":                          "p_plattenpalast_berlin",
    "Plattenvereinigung":                     "p_plattenvereinigung_berlin",
    "Recyclinghaus Hannover":                 "p_recyclinghaus_hannover",
    "BedZED":                                 "p_bedzed_london_hackbridge",
    "BioPartner 5":                           "p_biopartner_5_leiden_oegstgeest",
    "Boulder Community Hospital":             "p_boulder_fire_station_3",
    "CRCLR":                                  "p_crclr_house_impact_hub_berlin",
    "Impact Hub Berlin":                      "p_crclr_house_impact_hub_berlin",
    "AWM Münster":                            "p_awm_muenster_circular_office",
    "AWM Muenster":                           "p_awm_muenster_circular_office",
    "Europa Building":                        "p_europa_building_brussels",
    "BlueCity":                               "p_bluecity_offices_rotterdam",
    "Boschgaard":                             "p_woongroep_boschgaard_den_bosch",
    "Hastings Pier":                          "p_hastings_pier_visitor_centre",
    "Big Dig":                                "p_big_dig_house_lexington_massachusetts",
    "Multi Brussels":                         "p_multi_brussels_reuse_in_multi",
    "Superlocal":                             "p_superlocal_expogebouw_bleijerheide",
    "SUPERLOCAL":                             "p_superlocal_expogebouw_bleijerheide",
    "Recypark Anderlecht":                    "p_recypark_demets_anderlecht",
    "Recypark Demets":                        "p_recypark_demets_anderlecht",
    "55 Great Suffolk":                       "p_55_great_suffolk_street_london",
    "Brent Cross":                            "p_brent_cross_town_primary_substation_london",
    "House of Fraser":                        "p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain",
    "KA13":                                   "p_ka13_kristian_augusts_gate_13_oslo",
    "Kristian Augusts":                       "p_ka13_kristian_augusts_gate_13_oslo",
    "Brummen":                                None,    # no live projekt
    "Thoravej":                               "p_thoravej_29_copenhagen",
    "Liander":                                "p_liander_alliander_hq_duiven",
    "Alliander":                              "p_liander_alliander_hq_duiven",
    "Holbein Gardens":                        "p_holbein_gardens_london",
    "Grande Halle":                           "p_grande_halle_de_colombelles",
    "ReCreate Finland":                       "p_harmalanranta_a_kruunu_recreate_mini_pilot_tampere",
    "Prinsenhof":                             "p_circular_centre_netherlands_prinsenhof_a_reuse_pilot",
    "Verbiest":                               "p_verbiest_karreveld_brussels",
    "Karreveld":                              "p_verbiest_karreveld_brussels",
    "Triodos":                                None,
    "Plattenpalast Berlin":                   "p_plattenpalast_berlin",
    "Schildow":                               "p_berlin_schildow_pilot_house",
    "Mouscron":                               "p_musee_de_folklore_mouscron",
    "Folklore":                               "p_musee_de_folklore_mouscron",
}

# Token-level BELEGT markers (case-insensitive sub-string match on row text).
POS_EVIDENCE_TOKENS = (
    "belegt",        # German keyword in research files
    "directly documents",
    "documents",
    "documented",
    "dokumentiert",
    "bestätigt",
    "bestaetigt",
    "evidenced",
    "evidence found",
)
NEG_EVIDENCE_TOKENS = (
    "no project",
    "no specific project",
    "nicht projektbelegt",
    "nicht belegt",
    "no belegt",
    "infer/research",
    "infer-research",
    "infer / research",
    "no project-specific belegt",
    "candidate / `infer`",
    "candidate /",
    "no direct named",
    "no project source",
    "not found",
    "no named",
    "no robust",
)


# Regex toolkit
URL_RE = re.compile(r"(https?://[^\s)>\]\|\}]+)", re.IGNORECASE)
# Domain-vocab token: prefix_ + lowercase/digits/underscore, length 3-90.
# We match inside backticks where most embedded IDs live to avoid false positives.
VOCAB_RE_BACKTICK = re.compile(r"`([a-z]{1,3}_[a-z0-9_]{2,90})`")
TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$", re.MULTILINE)
SLUG_RE = re.compile(r"[^a-z0-9]+")


# Vocab-prefix-set covers what we recognise.
_RECOGNISED_PREFIXES = {p + "_" for p in VOCAB_PREFIX_LABEL.keys()}


def _log(msg: str) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = f"[{stamp}] {msg}"
    try:
        print(line, flush=True)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        print(line.encode(enc, errors="replace").decode(enc), flush=True)
    PROGRESS_LOG.parent.mkdir(parents=True, exist_ok=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def hash8(url: str) -> str:
    return hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]


def slug(s: str) -> str:
    s = s.lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = SLUG_RE.sub("_", s).strip("_")
    if len(s) > 80:
        s = s[:40] + "__" + s[-35:]
    return s


def clean_url(raw: str) -> str:
    """Strip common trailing punctuation/parens/quotes from a URL match."""
    s = raw
    # remove trailing markdown punctuation that should not be in URL
    while s and s[-1] in ".,;:)>\\]\"'":
        s = s[:-1]
    return s


def vocab_label_for(vid: str) -> tuple[str, str | None] | None:
    """Return (Node label, project rel-type) for a domain id, else None."""
    for prefix, val in VOCAB_PREFIX_LABEL.items():
        if vid.startswith(prefix + "_"):
            return val
    return None


def split_table_rows(text: str) -> list[str]:
    """Return raw table-row strings (one row per element). Header / separator
    rows that start with `| ---` are excluded."""
    rows = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        # Separator row: contains only |, -, :, spaces.
        if re.fullmatch(r"\|[\s\-:|]+\|", line.strip()):
            continue
        rows.append(line)
    return rows


def has_pos_evidence(text: str) -> bool:
    low = text.lower()
    if any(t in low for t in POS_EVIDENCE_TOKENS):
        # treat negative markers as overriding
        if any(t in low for t in NEG_EVIDENCE_TOKENS):
            return False
        return True
    return False


def find_named_projects(text: str) -> set[str]:
    """Return set of live projekt ids found in row text via PROJECT_NAME_LOOKUP."""
    found: set[str] = set()
    for token, pid in PROJECT_NAME_LOOKUP.items():
        if pid is None:
            continue
        # case-insensitive plain substring
        if token.lower() in text.lower():
            found.add(pid)
    return found


# ---------------------------------------------------------------------------
# Phase 4b.2 — research-file loader
# ---------------------------------------------------------------------------

def load_research_file(session, path: Path, anchor_id: str, title: str,
                       name: str) -> dict[str, Any]:
    res: dict[str, Any] = {
        "anchor_id": anchor_id,
        "name": name,
        "url_quellen_created_or_merged": 0,
        "zitiert_quelle_edges_merged": 0,
        "vocab_nodes_touched": 0,
        "vocab_belegt_edges_merged": 0,
        "project_edges_merged": 0,
        "project_edge_examples": [],
        "skipped_unknown_projekt": [],
    }

    text = path.read_text(encoding="utf-8")
    relpath = path.relative_to(REPO_ROOT).as_posix()

    # 1. Anchor MERGE
    session.run(
        """
        MERGE (q:Quelle {id:$id})
        ON CREATE SET q.name        = $name,
                      q.title       = $title,
                      q.quelltyp    = 'research_markdown',
                      q.source_file = $relpath,
                      q.source_scope= 'inbox_research',
                      q.url         = NULL,
                      q.created_by  = 'agent10_phase4b_2'
        SET q.last_seen_by = 'agent10_phase4b_2',
            q.quelltyp     = coalesce(q.quelltyp, 'research_markdown'),
            q.source_file  = coalesce(q.source_file, $relpath),
            q.title        = coalesce(q.title, $title)
        """,
        {"id": anchor_id, "name": name, "title": title, "relpath": relpath},
    )

    # 2. URL extraction — per file, deduplicated, MERGE child + ZITIERT_QUELLE
    seen_urls: dict[str, str] = {}     # url -> q_id
    for m in URL_RE.finditer(text):
        url = clean_url(m.group(1))
        if not url or url in seen_urls:
            continue
        qid = f"q_research_{slug(name).rstrip('_md')}_url_{hash8(url)}"
        title_hint = url[-60:]
        session.run(
            """
            MERGE (qe:Quelle {id:$qid})
            ON CREATE SET qe.url        = $url,
                          qe.title      = $title,
                          qe.name       = $title,
                          qe.quelltyp   = 'external_reference',
                          qe.source_scope = 'research_file_url',
                          qe.created_by = 'agent10_phase4b_2'
            SET qe.last_seen_by = 'agent10_phase4b_2',
                qe.url      = coalesce(qe.url, $url),
                qe.quelltyp = coalesce(qe.quelltyp, 'external_reference')
            WITH qe
            MATCH (anchor:Quelle {id:$anchor_id})
            MERGE (anchor)-[r:ZITIERT_QUELLE]->(qe)
            ON CREATE SET r.id = 'r_' + $anchor_id + '__ZITIERT_QUELLE__' + $qid
            SET r.evidence_origin     = 'derived',
                r.evidence_basis      = 'research_file_url',
                r.evidence_source_id  = $anchor_id,
                r.evidence_confidence = 'unklar',
                r.evidence_excerpt    = NULL
            """,
            {"qid": qid, "url": url, "title": title_hint, "anchor_id": anchor_id},
        )
        seen_urls[url] = qid
        res["url_quellen_created_or_merged"] += 1
        res["zitiert_quelle_edges_merged"] += 1

    # 3. Vocab-ID extraction (backtick-wrapped). MERGE node + (node)-[:BELEGT_IN]->(anchor)
    rows = split_table_rows(text)
    seen_vocab: set[str] = set()
    for row in rows:
        for vid in VOCAB_RE_BACKTICK.findall(row):
            label_info = vocab_label_for(vid)
            if label_info is None:
                continue
            label, _ = label_info
            if vid in seen_vocab:
                continue
            seen_vocab.add(vid)
            # MERGE node; ON CREATE set label too. For existing nodes we
            # don't add the research label, only the evidence-of-existence edge.
            session.run(
                f"""
                MERGE (n {{id:$vid}})
                ON CREATE SET n:{label},
                              n.name = $vid,
                              n.source_scope = 'research_file',
                              n.created_by = 'agent10_phase4b_2'
                SET n.last_seen_by = 'agent10_phase4b_2'
                WITH n
                MATCH (anchor:Quelle {{id:$anchor_id}})
                MERGE (n)-[r:BELEGT_IN]->(anchor)
                ON CREATE SET r.id = 'r_' + $vid + '__BELEGT_IN__' + $anchor_id
                SET r.evidence_origin     = 'inferred',
                    r.evidence_basis      = 'research_file_row',
                    r.evidence_source_id  = $anchor_id,
                    r.evidence_confidence = 'inferiert',
                    r.evidence_excerpt    = NULL
                """,
                {"vid": vid, "anchor_id": anchor_id},
            )
            res["vocab_nodes_touched"] += 1
            res["vocab_belegt_edges_merged"] += 1

    # 4. Conservative project edges from rows
    for row in rows:
        if not has_pos_evidence(row):
            continue
        projekt_ids = find_named_projects(row)
        if not projekt_ids:
            continue
        # row's vocab tokens
        row_vocab = [v for v in VOCAB_RE_BACKTICK.findall(row)
                     if vocab_label_for(v) is not None]
        if not row_vocab:
            continue
        # pick first URL in the row as evidence_source_id, else anchor
        row_urls = [clean_url(u) for u in URL_RE.findall(row)]
        evidence_src_id = anchor_id
        for u in row_urls:
            if u in seen_urls:
                evidence_src_id = seen_urls[u]
                break
        excerpt = row.strip()[:480]
        for pid in projekt_ids:
            # Confirm projekt exists; else skip and record
            rec = session.run(
                "MATCH (p:Projekt {id:$pid}) RETURN p.id AS id", {"pid": pid}
            ).single()
            if rec is None:
                if pid not in res["skipped_unknown_projekt"]:
                    res["skipped_unknown_projekt"].append(pid)
                continue
            for vid in row_vocab:
                lbl = vocab_label_for(vid)
                if lbl is None or lbl[1] is None:
                    continue
                rel_type = lbl[1]
                rel_id = f"r_{pid}__{rel_type}__{vid}__research_inferred"
                session.run(
                    f"""
                    MATCH (p:Projekt {{id:$pid}}), (d {{id:$vid}})
                    MERGE (p)-[r:{rel_type}]->(d)
                    ON CREATE SET r.id = $rel_id
                    SET r.evidence_origin     = 'curated',
                        r.evidence_basis      = 'cell_citation',
                        r.evidence_source_id  = $src_id,
                        r.evidence_confidence = 'belegt',
                        r.evidence_excerpt    = $excerpt,
                        r.source_scope        = 'research_file_row'
                    """,
                    {
                        "pid": pid, "vid": vid, "rel_id": rel_id,
                        "src_id": evidence_src_id, "excerpt": excerpt,
                    },
                )
                res["project_edges_merged"] += 1
                if len(res["project_edge_examples"]) < 12:
                    res["project_edge_examples"].append({
                        "projekt": pid, "rel": rel_type, "domain": vid,
                        "evidence_source_id": evidence_src_id,
                    })

    return res


# ---------------------------------------------------------------------------
# Phase 4b.3 — actor-registry loader
# ---------------------------------------------------------------------------

# ID-remap helpers copied from _scripts/transform_registry_jsonl_to_canonical.py
_KNOWN_COLLISIONS: dict[str, str] = {
    "a_patrick_teuffel": "patrick_teuffel",
    "a_dirk_hebel": "Dirk_Hebel",
    "a_werner_sobek": "Werner_Sobek",
    "a_superuse_studios": "Superuse_Studios",
    "a_natural_building_lab": "Natural_Building_Lab",
    "a_zrs_architekten_ingenieure": "ZRS_Architekten_Ingenieure",
    "a_lendager": "Lendager",
    "a_cityfoerster": "CITYFOERSTER",
    "a_bellastock": "Bellastock",
    "a_rotor": "Rotor",
}
_A_SLUG_RE = re.compile(r"a_[a-z0-9_]+")


def _load_id_map() -> dict[str, str]:
    csv_path = REPO_ROOT / "_neo4j" / "contracts" / "actor_registry_v1_2" / "ID_RECONCILIATION.csv"
    if not csv_path.is_file():
        return {}
    import csv as _csv
    out: dict[str, str] = {}
    with csv_path.open(encoding="utf-8") as fh:
        for row in _csv.DictReader(fh):
            out[row["batch_id"]] = row["canonical_id"]
    return out


def canonical_id(batch_id: str, id_map: dict[str, str]) -> str:
    if batch_id in id_map:
        return id_map[batch_id]
    if batch_id in _KNOWN_COLLISIONS:
        return _KNOWN_COLLISIONS[batch_id]
    if batch_id.startswith("a_"):
        return batch_id[2:]
    return batch_id


# Vocab remap tables (mirrored)
AKTEURTYP_REMAP: dict[str, str] = {
    "at_person":                         "at_person",
    "at_organisation":                   "at_organisation",
    "at_unternehmen":                    "at_unternehmen",
    "at_oeffentliche_institution":       "at_oeffentliche_institution",
    "at_forschung_lehre":                "at_forschung_lehre",
    "at_ngo_verband_netzwerk":           "at_ngo_verband_netzwerk",
    "at_materialhub_bauteilboerse":      "at_materialhub_bauteilboerse",
    "at_foerdergeber_programmtraeger":   "at_foerdergeber_programmtraeger",
    "at_software_tool_anbieter":         "at_software_tool_anbieter",
    "at_unbekannt":                      "at_unbekannt",
    "at_ngo_netzwerk":                   "at_ngo_verband_netzwerk",
    "at_verband_kammer":                 "at_ngo_verband_netzwerk",
    "at_architekturburo":                "at_unternehmen",
    "at_ingenieurburo":                  "at_unternehmen",
    "at_bauunternehmen":                 "at_unternehmen",
    "at_rueckbauunternehmen":            "at_unternehmen",
    "at_materiallieferant_hersteller":   "at_unternehmen",
    "at_reuse_consultancy_zirkularitaet":"at_unternehmen",
    "at_developer_immobilien":           "at_unternehmen",
    "at_wohnungsbau_genossenschaft":     "at_organisation",
    "at_universitaet_forschungsinstitut":"at_forschung_lehre",
    "at_kultur_bildung_ausstellung":     "at_organisation",
    "at_betreiber_nutzerorganisation":   "at_organisation",
    "at_zertifizierer_pruefstelle":      "at_organisation",
}

AKTEURROLLE_REMAP: dict[str, str] = {
    "ar_architektur":                           "ar_entwurf_planung",
    "ar_fassade":                               "ar_entwurf_planung",
    "ar_kunst_gestaltung":                      "ar_entwurf_planung",
    "ar_landschaftsplanung":                    "ar_entwurf_planung",
    "ar_entwurf_bauende_praxis":                "ar_entwurf_planung",
    "ar_tragwerksplanung":                      "ar_fachplanung_nachweis",
    "ar_pruefung_qualitaetssicherung":          "ar_fachplanung_nachweis",
    "ar_brandschutz_barrierefreiheit":          "ar_fachplanung_nachweis",
    "ar_tga_gebaeudetechnik":                   "ar_fachplanung_nachweis",
    "ar_bauausfuehrung":                        "ar_bauausfuehrung_fertigung",
    "ar_stahlbau_fertigung":                    "ar_bauausfuehrung_fertigung",
    "ar_produkt_bausystementwicklung":          "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_demontage":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_bauteilernte_materialakquise":          "ar_rueckbau_bauteilernte_logistik",
    "ar_logistik_transport":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferant":                     "ar_materiallieferung_markt",
    "ar_vermittlung_marktplatz":                "ar_materiallieferung_markt",
    "ar_materialhub_bauteilboerse":             "ar_materiallieferung_markt",
    "ar_bauteilboerse_bauteilernte_markt":      "ar_materiallieferung_markt",
    "ar_aufbereitung_refurbishment":            "ar_aufbereitung_refurbishment",
    "ar_reuse_beratung":                        "ar_reuse_zirkularitaetsberatung",
    "ar_nachhaltigkeitsberatung":               "ar_reuse_zirkularitaetsberatung",
    "ar_zertifizierung_bewertung":              "ar_reuse_zirkularitaetsberatung",
    "ar_konzept_future_reuse_system":           "ar_reuse_zirkularitaetsberatung",
    "ar_forschung_dokumentation":               "ar_forschung_dokumentation",
    "ar_technik_forschung_nachweis":            "ar_forschung_dokumentation",
    "ar_materialpass_digitalisierung":          "ar_software_digitalisierung",
    "ar_software_tool":                         "ar_software_digitalisierung",
    "ar_bauherr_auftraggeber":                  "ar_bauherr_auftraggeber",
    "ar_betreiber_nutzer":                      "ar_betrieb_nutzung",
    "ar_oeffentliche_hand":                     "ar_oeffentliche_hand_foerderung",
    "ar_foerderung_programmsteuerung":          "ar_oeffentliche_hand_foerderung",
    "ar_bildung_wissenstransfer":               "ar_bildung_wissenstransfer",
    "ar_organisation_bildung_wissenstransfer":  "ar_bildung_wissenstransfer",
    "ar_ausstellung_kuration":                  "ar_bildung_wissenstransfer",
    "ar_projektmanagement_koordination":        "ar_projektmanagement_koordination",
    "ar_projektbeteiligte_unbestimmt":          "ar_unbestimmt",
    "ar_entwurf_planung":                       "ar_entwurf_planung",
    "ar_fachplanung_nachweis":                  "ar_fachplanung_nachweis",
    "ar_bauausfuehrung_fertigung":              "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_bauteilernte_logistik":        "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferung_markt":               "ar_materiallieferung_markt",
    "ar_reuse_zirkularitaetsberatung":          "ar_reuse_zirkularitaetsberatung",
    "ar_oeffentliche_hand_foerderung":          "ar_oeffentliche_hand_foerderung",
    "ar_betrieb_nutzung":                       "ar_betrieb_nutzung",
    "ar_software_digitalisierung":              "ar_software_digitalisierung",
    "ar_unbestimmt":                            "ar_unbestimmt",
}


# Records we drop on the floor (Agent 8 already deleted them in the live graph)
def _is_dropped_rel(rec: dict) -> bool:
    if rec.get("record_type") != "rel":
        return False
    rel_type = rec.get("type")
    fr = rec.get("from", "")
    to = rec.get("to", "")
    # Projekt -[BELEGT_IN]-> q_actor_* OR q_akteursliste_master_md
    if rel_type == "BELEGT_IN" and fr.startswith("p_") and (
        to.startswith("q_actor_") or to == "q_akteursliste_master_md"
    ):
        return True
    return False


def _evidence_for_rel(rel_type: str, to_id: str) -> dict[str, Any]:
    """Canonical evidence shape for an actor-registry relationship."""
    if rel_type == "HAT_AKTEURROLLE":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "controlled_vocab",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "HAT_AKTEURTYP":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "controlled_vocab",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "ASSOZIIERT_MIT_PROJEKT":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "registry_stub",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "teilweise_belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "LIEGT_IN_LAND":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "controlled_vocab",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "VERBUNDEN_MIT_AKTEUR":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "controlled_vocab",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "BELEGT_IN":
        return {
            "evidence_origin": "curated",
            "evidence_basis": "cell_citation",
            "evidence_source_id": to_id,
            "evidence_confidence": "belegt",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    if rel_type == "ZITIERT_QUELLE":
        return {
            "evidence_origin": "derived",
            "evidence_basis": "case_markdown_sources",
            "evidence_source_id": "q_akteursliste_master_md",
            "evidence_confidence": "unklar",
            "evidence_excerpt": None,
            "source_scope": "actor_registry",
        }
    return {
        "evidence_origin": "curated",
        "evidence_basis": "controlled_vocab",
        "evidence_source_id": "q_akteursliste_master_md",
        "evidence_confidence": "belegt",
        "evidence_excerpt": None,
        "source_scope": "actor_registry",
    }


def _node_label_set(rec: dict) -> str:
    labels = rec.get("labels") or []
    if not labels:
        return ""
    return ":" + ":".join(labels)


def _project_node_props_safe(props: dict) -> dict:
    """Strip the legacy registry-stub status flags from Projekt props.

    The actor-registry JSONLs originally set `actor_registry_mentioned`,
    `source_scope='actor_registry_association'`, `needs_project_file` and
    `import_status='registry_stub_only'`. Today (post Agent 8) we keep
    Projekt nodes that exist, but we do NOT reapply `import_status` so
    Phase 5.3 can use its own quality_tier logic. We DO preserve
    `actor_registry_mentioned=true` because Phase 5 reads it.
    """
    safe = dict(props)
    safe.pop("import_status", None)
    safe.pop("needs_project_file", None)
    return safe


def load_registry_jsonl(session, jsonl_path: Path,
                        id_map: dict[str, str]) -> dict[str, Any]:
    res: dict[str, Any] = {
        "file": jsonl_path.relative_to(REPO_ROOT).as_posix(),
        "nodes_total": 0,
        "nodes_merged": 0,
        "rels_total": 0,
        "rels_merged": 0,
        "rels_dropped_projekt_to_actor_url": 0,
        "rels_dropped_unknown_type": 0,
        "rels_dropped_missing_endpoint": 0,
        "zitiert_quelle_master_to_actor_url_merged": 0,
        "by_rel_type": {},
    }

    lines = jsonl_path.read_text(encoding="utf-8").splitlines()
    records = [json.loads(ln) for ln in lines if ln.strip()]

    nodes = [r for r in records if r.get("record_type") == "node"]
    rels = [r for r in records if r.get("record_type") == "rel"]
    res["nodes_total"] = len(nodes)
    res["rels_total"] = len(rels)

    # Phase A: MERGE nodes
    for n in nodes:
        nid = canonical_id(n["id"], id_map)
        labels = n.get("labels") or []
        props = dict(n.get("properties") or {})
        if "Projekt" in labels:
            props = _project_node_props_safe(props)
        # Drop the leading 'a_' / collision-remapped id property if present in props
        props.pop("id", None)

        label_block = ":".join(labels) if labels else ""
        if label_block:
            # ON CREATE: full label set + name. ON MATCH: only top-up missing props.
            cypher = f"""
            MERGE (n {{id:$id}})
            ON CREATE SET n:{label_block},
                          n += $props,
                          n.id = $id,
                          n.actor_registry_loader_seen = 'agent10'
            ON MATCH SET n.actor_registry_loader_seen = 'agent10'
            SET n.name = coalesce(n.name, $props.name)
            """
        else:
            cypher = """
            MERGE (n {id:$id})
            ON CREATE SET n += $props,
                          n.id = $id,
                          n.actor_registry_loader_seen = 'agent10'
            ON MATCH SET n.actor_registry_loader_seen = 'agent10'
            SET n.name = coalesce(n.name, $props.name)
            """
        session.run(cypher, {"id": nid, "props": props})
        res["nodes_merged"] += 1

    # Phase B: MERGE rels
    for r in rels:
        if _is_dropped_rel(r):
            res["rels_dropped_projekt_to_actor_url"] += 1
            continue

        rel_type = r["type"]
        # Apply ID remap and vocab remap
        fr = canonical_id(r["from"], id_map)
        to = r["to"]
        if rel_type == "HAT_AKTEURTYP":
            to = AKTEURTYP_REMAP.get(to, to)
        elif rel_type == "HAT_AKTEURROLLE":
            to = AKTEURROLLE_REMAP.get(to, to)
        else:
            to = canonical_id(to, id_map)

        rel_id = r.get("id") or f"r_{fr}__{rel_type}__{to}"
        # Rewrite a_-prefix segments in the rel_id text
        rel_id = _A_SLUG_RE.sub(
            lambda m: canonical_id(m.group(0), id_map), rel_id
        )

        # Confirm both endpoints exist. LIMIT 1 keeps `.single()` quiet
        # when the same id appears under multiple labels (e.g. a Quelle that
        # also carries a vocab label after Phase 4b.2 enrichment).
        endp = session.run(
            "MATCH (a {id:$fr}) WITH a LIMIT 1 "
            "MATCH (b {id:$to}) WITH a, b LIMIT 1 "
            "RETURN a IS NOT NULL AS ok",
            {"fr": fr, "to": to},
        ).single()
        if endp is None:
            res["rels_dropped_missing_endpoint"] += 1
            continue

        evidence = _evidence_for_rel(rel_type, to)
        # extra props from JSONL (preserve needs_verification etc.)
        extra = dict(r.get("properties") or {})
        # Drop scope/source-scope clones that would override evidence shape
        # but preserve `scope`, `connection_kind`, `needs_verification`,
        # `not_confirmed_project_participation`, `individual_project_lead_uncertain`.
        extra.pop("evidence_origin", None)
        extra.pop("evidence_basis", None)
        extra.pop("evidence_source_id", None)
        extra.pop("evidence_confidence", None)
        extra.pop("evidence_excerpt", None)
        extra.pop("source_scope", None)
        extra.pop("datenqualitaet", None)

        cypher = f"""
        MATCH (a {{id:$fr}}), (b {{id:$to}})
        MERGE (a)-[r:{rel_type}]->(b)
        ON CREATE SET r.id = $rel_id
        SET r.evidence_origin     = $evidence_origin,
            r.evidence_basis      = $evidence_basis,
            r.evidence_source_id  = $evidence_source_id,
            r.evidence_confidence = $evidence_confidence,
            r.evidence_excerpt    = $evidence_excerpt,
            r.source_scope        = $source_scope,
            r += $extra
        """
        params = {
            "fr": fr, "to": to, "rel_id": rel_id,
            "extra": extra,
            **evidence,
        }
        try:
            session.run(cypher, params)
        except Exception as e:
            _log(f"  WARN rel MERGE failed for {rel_id}: {e}")
            res["rels_dropped_unknown_type"] += 1
            continue
        res["rels_merged"] += 1
        res["by_rel_type"][rel_type] = res["by_rel_type"].get(rel_type, 0) + 1
        if (
            rel_type == "ZITIERT_QUELLE"
            and fr == "q_akteursliste_master_md"
            and to.startswith("q_actor_")
        ):
            res["zitiert_quelle_master_to_actor_url_merged"] += 1

    return res


# ---------------------------------------------------------------------------
# Snapshot helpers
# ---------------------------------------------------------------------------

def snapshot(session) -> dict[str, Any]:
    def _scalar(q: str) -> int:
        return session.run(q).single()[0]

    return {
        "total_nodes": _scalar("MATCH (n) RETURN count(n)"),
        "total_rels": _scalar("MATCH ()-[r]->() RETURN count(r)"),
        "quelle": _scalar("MATCH (q:Quelle) RETURN count(q)"),
        "quelle_research_markdown": _scalar(
            "MATCH (q:Quelle) WHERE q.quelltyp='research_markdown' RETURN count(q)"
        ),
        "quelle_external_reference": _scalar(
            "MATCH (q:Quelle) WHERE q.quelltyp='external_reference' RETURN count(q)"
        ),
        "quelle_actor_external_link": _scalar(
            "MATCH (q:Quelle) WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(q)"
        ),
        "akteur": _scalar("MATCH (a:Akteur) RETURN count(a)"),
        "projekt": _scalar("MATCH (p:Projekt) RETURN count(p)"),
        "akteursliste_master_exists": _scalar(
            "MATCH (q:Quelle {id:'q_akteursliste_master_md'}) RETURN count(q)"
        ),
        "zitiert_quelle": _scalar(
            "MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r)"
        ),
        "zitiert_quelle_from_master_to_actor_url": _scalar(
            "MATCH (q:Quelle {id:'q_akteursliste_master_md'})-[r:ZITIERT_QUELLE]->"
            "(t:Quelle) WHERE t.quelltyp='external_link_from_actor_registry' RETURN count(r)"
        ),
        "assoziiert_mit_projekt": _scalar(
            "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r)"
        ),
        "assoziiert_curated_teilweise_belegt": _scalar(
            "MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() "
            "WHERE r.evidence_origin='curated' AND r.evidence_basis='registry_stub' "
            "  AND r.evidence_confidence='teilweise_belegt' RETURN count(r)"
        ),
        "hat_akteurrolle": _scalar(
            "MATCH ()-[r:HAT_AKTEURROLLE]->() RETURN count(r)"
        ),
        "hat_akteurrolle_curated_belegt": _scalar(
            "MATCH ()-[r:HAT_AKTEURROLLE]->() "
            "WHERE r.evidence_origin='curated' AND r.evidence_confidence='belegt' "
            "RETURN count(r)"
        ),
        "hat_akteurtyp": _scalar(
            "MATCH ()-[r:HAT_AKTEURTYP]->() RETURN count(r)"
        ),
        "akteur_belegt_actor_url": _scalar(
            "MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r)"
        ),
        "projekt_belegt_actor_url_residual": _scalar(
            "MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp='external_link_from_actor_registry' RETURN count(r)"
        ),
        "aufbereitungsverfahren_count": _scalar(
            "MATCH (n:Aufbereitungsverfahren) RETURN count(n)"
        ),
        "verbindungstechnik_count": _scalar(
            "MATCH (n:Verbindungstechnik) RETURN count(n)"
        ),
        "pruefungnachweis_count": _scalar(
            "MATCH (n:PruefungNachweis) RETURN count(n)"
        ),
        "schadstoff_count": _scalar("MATCH (n:Schadstoff) RETURN count(n)"),
        "rechtlichebedingung_count": _scalar(
            "MATCH (n:RechtlicheBedingung) RETURN count(n)"
        ),
        "leistungsanforderung_count": _scalar(
            "MATCH (n:Leistungsanforderung) RETURN count(n)"
        ),
        "domain_belegt_research_anchor": _scalar(
            "MATCH (n)-[r:BELEGT_IN]->(q:Quelle) "
            "WHERE q.quelltyp='research_markdown' "
            "  AND r.evidence_origin='inferred' AND r.evidence_basis='research_file_row' "
            "RETURN count(r)"
        ),
        "project_research_inferred_edges": _scalar(
            "MATCH (p:Projekt)-[r]->(n) "
            "WHERE type(r) IN ['HAT_AUFBEREITUNG','HAT_VERBINDUNGSTECHNIK',"
            "                   'HAT_PRUEFUNG','HAT_SCHADSTOFF','HAT_RECHTLICHE_BEDINGUNG'] "
            "  AND r.source_scope='research_file_row' "
            "RETURN count(r)"
        ),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def write_flag(path: Path, phase: str, before: dict, after: dict, payload: dict) -> None:
    body = {
        "phase": phase,
        "completed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "before": before,
        "after": after,
        "payload": payload,
    }
    path.write_text(
        json.dumps(body, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    _log(f"wrote done flag: {path.name}")


def resolve_connection() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection as _r  # type: ignore

    uri, user, password, database = _r()
    if not uri or not user or not password:
        raise RuntimeError("Neo4j connection missing.")
    if database != "mit-bestand":
        _log(f"WARN: overriding NEO4J_DATABASE='{database}' to 'mit-bestand'")
        database = "mit-bestand"
    return uri, user, password, database


def main() -> int:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    from neo4j import GraphDatabase  # type: ignore

    uri, user, password, database = resolve_connection()
    _log(f"connect to {uri} db='{database}' as user='{user}'")

    started = time.perf_counter()
    started_iso = datetime.now(timezone.utc).isoformat(timespec="seconds")
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as s:
            before = snapshot(s)
        _log(
            f"BEFORE  nodes={before['total_nodes']} rels={before['total_rels']} "
            f"quelle={before['quelle']} akteur={before['akteur']} "
            f"projekt={before['projekt']}  "
            f"master_anchor_exists={before['akteursliste_master_exists']}  "
            f"projekt_belegt_actor_url={before['projekt_belegt_actor_url_residual']}"
        )
        assert before["projekt_belegt_actor_url_residual"] == 0, (
            "Pre-condition violated: Agent 8 should have left 0 "
            "Projekt->BELEGT_IN->actor_registry_url edges, but found "
            f"{before['projekt_belegt_actor_url_residual']}"
        )

        # =================================================================
        # Phase 4b.2 — research files
        # =================================================================
        _log("PHASE 4b.2 — research-file ingestion (link-only) — START")
        research_payload: dict[str, Any] = {}
        with driver.session(database=database) as s:
            for filename, meta in RESEARCH_FILES.items():
                fp = RESEARCH_DIR / filename
                if not fp.is_file():
                    _log(f"  SKIP missing file: {filename}")
                    research_payload[filename] = {"missing": True}
                    continue
                _log(f"  -> {filename}")
                res = load_research_file(
                    s,
                    fp,
                    anchor_id=meta["anchor_id"],
                    title=meta["title"],
                    name=meta["name"],
                )
                research_payload[filename] = res
                _log(
                    f"     anchor={res['anchor_id']}  "
                    f"urls={res['url_quellen_created_or_merged']}  "
                    f"vocab_nodes_touched={res['vocab_nodes_touched']}  "
                    f"vocab_belegt_edges={res['vocab_belegt_edges_merged']}  "
                    f"project_edges={res['project_edges_merged']}"
                )
        _log("PHASE 4b.2 done.")

        with driver.session(database=database) as s:
            after_42 = snapshot(s)
        write_flag(FLAG_4B2, "4b.2", before, after_42, research_payload)

        # =================================================================
        # Phase 4b.3 — actor registry
        # =================================================================
        _log("PHASE 4b.3 — actor-registry replay (MERGE-only) — START")
        # Locate all JSONL batches
        jsonl_files = sorted(
            REGISTRY_GLOB.rglob("registry/**/*.registry.kg.jsonl")
        )
        _log(f"  found {len(jsonl_files)} actor-registry JSONL batches")
        id_map = _load_id_map()

        with driver.session(database=database) as s:
            # MERGE the master anchor once
            s.run(
                """
                MERGE (q:Quelle {id:'q_akteursliste_master_md'})
                ON CREATE SET q.name        = 'akteursliste_master.md',
                              q.title       = 'Actor registry master markdown',
                              q.quelltyp    = 'actor_registry_markdown',
                              q.source_file = 'akteursliste_master.md',
                              q.source_scope= 'actor_registry',
                              q.url         = NULL,
                              q.created_by  = 'agent10_phase4b_3'
                SET q.last_seen_by = 'agent10_phase4b_3',
                    q.quelltyp     = coalesce(q.quelltyp, 'actor_registry_markdown'),
                    q.title        = coalesce(q.title, 'Actor registry master markdown')
                """
            )
        registry_payload: dict[str, Any] = {
            "batches": [],
            "totals": {
                "nodes_merged": 0,
                "rels_merged": 0,
                "rels_dropped_projekt_to_actor_url": 0,
                "rels_dropped_missing_endpoint": 0,
                "rels_dropped_unknown_type": 0,
                "zitiert_quelle_master_to_actor_url_merged": 0,
            },
        }
        with driver.session(database=database) as s:
            for jp in jsonl_files:
                _log(f"  -> {jp.relative_to(REPO_ROOT).as_posix()}")
                rp = load_registry_jsonl(s, jp, id_map)
                registry_payload["batches"].append(rp)
                t = registry_payload["totals"]
                t["nodes_merged"] += rp["nodes_merged"]
                t["rels_merged"] += rp["rels_merged"]
                t["rels_dropped_projekt_to_actor_url"] += rp["rels_dropped_projekt_to_actor_url"]
                t["rels_dropped_missing_endpoint"] += rp["rels_dropped_missing_endpoint"]
                t["rels_dropped_unknown_type"] += rp["rels_dropped_unknown_type"]
                t["zitiert_quelle_master_to_actor_url_merged"] += (
                    rp["zitiert_quelle_master_to_actor_url_merged"]
                )
                _log(
                    f"     nodes_merged={rp['nodes_merged']}  "
                    f"rels_merged={rp['rels_merged']}  "
                    f"dropped_projekt_to_actor_url={rp['rels_dropped_projekt_to_actor_url']}  "
                    f"dropped_missing_endpoint={rp['rels_dropped_missing_endpoint']}"
                )
        _log("PHASE 4b.3 done.")

        with driver.session(database=database) as s:
            after_43 = snapshot(s)

        # Post-condition: Agent 8 invariant must remain
        assert after_43["projekt_belegt_actor_url_residual"] == 0, (
            "Post-condition violated: re-introduced "
            f"{after_43['projekt_belegt_actor_url_residual']} Projekt->actor_url BELEGT_IN edges"
        )
        write_flag(FLAG_4B3, "4b.3", after_42, after_43, registry_payload)

        elapsed = time.perf_counter() - started
        result = {
            "started_at": started_iso,
            "finished_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "elapsed_seconds": elapsed,
            "before": before,
            "after_4b_2": after_42,
            "after_4b_3": after_43,
            "research": research_payload,
            "registry": registry_payload,
        }
        RESULT_JSON.write_text(
            json.dumps(result, ensure_ascii=False, indent=2, default=str),
            encoding="utf-8",
        )
        _log(
            f"DONE   total elapsed={elapsed:.1f}s   "
            f"nodes {before['total_nodes']}->{after_43['total_nodes']}   "
            f"rels  {before['total_rels']}->{after_43['total_rels']}"
        )
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
