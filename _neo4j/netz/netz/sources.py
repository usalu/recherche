"""All input file paths in one place -- the sole relocation point if this
package ever moves out of the scratchpad. Nothing else in netz/ should
hardcode a path.

Moved out of the temp scratchpad into E:\\recherche (git-tracked) on 2026-08-12,
per the standing recommendation in figs/plan_agent_dump.txt: the package and
its overlay/prune inputs lived only in a session-temp directory subject to
cleanup at any time -- the same failure mode that lost the original
prune-scoring script.
"""
from dataclasses import dataclass, field

_SP = r"E:/recherche/_neo4j/netz"


@dataclass(frozen=True)
class Sources:
    export_path: str = r"E:/recherche/actors_network.json"
    overlay_paths: tuple = (
        f"{_SP}/overlay.json",
        f"{_SP}/overlay2.json",
        f"{_SP}/overlay3.json",
    )
    audit_edges_path: str = f"{_SP}/audit2_peer_edges.json"
    prune_path: str = f"{_SP}/prune_eids.json"
    # 2026-08-13 fact-check (E:\recherche\_neo4j\review\2026-08_akteursnetz_faktencheck):
    # all ohne_beleg nodes + the R1/R3 removal candidates, kept as a separate,
    # separately-auditable list from the legacy FR/BE de-dup prune above.
    prune_faktencheck_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/prune_faktencheck_final.json"
    )
    unklar_edges_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/unklar_edges_final.json"
    )
    # Final keep/remove campaign for the 570 relationships drawn by the
    # LaTeX actor graph.  This is an edge-pair list, not a Neo4j writeback.
    prune_kanten_final_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/prune_kanten_final.json"
    )
    latex_country_overrides_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/latex_country_overrides.json"
    )
    strict_manifest_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/strict_review/input_manifest.json"
    )
    prune_strict_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/prune_strict_final.json"
    )
    merge_strict_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/merge_redirects_strict.json"
    )
    report_overrides_strict_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/report_overrides_strict.json"
    )
    klassifikation_final_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/klassifikation_final.json"
    )


DEFAULT = Sources()
