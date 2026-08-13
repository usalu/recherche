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
    # Rolle + Relevanz per surviving actor/project, the strict review's own
    # actor view -- the authority for what the printed table says a node does.
    klassifikation_actor_project_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/klassifikation_actor_project_final.json"
    )
    # Beziehungsart, Richtung, Beschreibung und Beleg je klassifizierter Kante.
    kanten_klassifikation_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/kanten_klassifikation.json"
    )
    # Eight strict-review entries that are programmes, not actors -- rendered
    # as their own report block (render.latex.programme_table), never in the
    # actor figures/tables.
    programme_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/programme_strict_final.json"
    )

    # 762 Organisationen aus der Bildpruefung, davon 343 mit freigegebenem
    # Logo-Asset (256x256 RGBA, 50 % Deckkraft). Bewusst NICHT der Default des
    # `--images-manifest`-Flags: full_image_collection.py `render` baut seine
    # bildlose Kontrolle daraus, dass das Flag fehlt. Hier steht der Pfad, damit
    # er beim Neuerzeugen der Fragmente nicht aus dem Gedaechtnis kommen muss.
    images_manifest_path: str = (
        r"E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/bilder_full/final_image_manifest.json"
    )
    # Wohin die freigegebenen Logos im Bericht liegen, und wie das gesetzte
    # LaTeX sie nennt. Getrennt, weil beides verschiedene Dinge sind: der
    # erste Pfad gehoert dem Dateisystem, der zweite dem TeX-Lauf, dessen
    # Arbeitsverzeichnis das Berichtsverzeichnis ist (`asset/projekt/...`,
    # `asset/logo/...` -- die Fragmente reihen sich hier ein statt absolute
    # E:/recherche-Pfade in einen anderen Repostand zu schreiben).
    report_asset_root: str = (
        r"E:/semio/mit-bestand/bericht/zwischenbericht/asset/akteur"
    )
    report_asset_ref: str = "asset/akteur"
    # Wohin die erzeugten Fragmente im Bericht gehoeren. Es gibt keinen
    # gemeinsamen Build ueber beide Repos, also war das bisher ein Handgriff --
    # und ein vergessener Handgriff laesst den Bericht stillschweigend einen
    # alten Stand drucken, ohne dass irgendein Check anschlaegt.
    # `netz.cli sync-fragments` macht daraus einen benannten Schritt.
    report_anhang_root: str = (
        r"E:/semio/mit-bestand/bericht/zwischenbericht/anhang"
    )
    report_fragments: tuple = (
        ("frag_abb_netz.tex", "akteursnetz-figuren.tex"),
        ("frag_tables_grid.tex", "akteursnetz-tabellen.tex"),
        ("frag_programme.tex", "akteursnetz-programme.tex"),
    )


DEFAULT = Sources()
