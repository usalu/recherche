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


DEFAULT = Sources()
