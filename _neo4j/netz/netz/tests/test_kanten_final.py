import json
import unittest

from netz.cli import load_network
from netz.mechanisms.connectivity import drawn_edge_nodes
from netz.mechanisms.layout import DEFAULT_FRAME, force_layout
from netz.render.latex.table_grid import load_kanten
from netz.sources import DEFAULT


def _pairs(path):
    with open(path, encoding="utf-8") as handle:
        return {tuple(sorted(pair)) for pair in json.load(handle)}


class FinalKantenActivationTests(unittest.TestCase):
    def test_strict_classification_is_the_latex_model_edge_set(self):
        # The old 477-edge positive list predates the strict node cleanup.
        # The final relationship classification plus strict endpoint set is
        # now authoritative; five relationships exposed only by reviewed
        # project->actor re-types are explicitly pruned as well.
        prune = _pairs(DEFAULT.prune_kanten_final_path)
        profile_prune = _pairs(DEFAULT.prune_beziehungsprofil_final_path)
        with open(DEFAULT.kanten_klassifikation_path, encoding="utf-8") as handle:
            reviewed = json.load(handle)
        self.assertEqual(472, len(reviewed))
        self.assertEqual(103, len(prune))

        network = load_network()
        drawn = {tuple(sorted(pair)) for pair in network.drawn}
        classified = load_kanten(
            DEFAULT.kanten_klassifikation_path, network, DEFAULT.merge_strict_path,
            DEFAULT.expansion_kanten_path,
        )
        visible_reviewed = {
            tuple(sorted(edge["pair"]))
            for rows in classified.values()
            for edge in rows
        }
        self.assertEqual(452, len(drawn))
        self.assertEqual(visible_reviewed, drawn)
        self.assertFalse(prune & drawn)
        self.assertEqual(2, len(profile_prune))
        self.assertFalse(profile_prune & drawn)

        visible = set()
        for panel in network.panels.values():
            nodes = drawn_edge_nodes(panel, min_comp=2)
            _, edges = force_layout(panel, nodes, DEFAULT_FRAME)
            visible.update(tuple(sorted(pair)) for pair in edges)
        self.assertEqual(drawn, visible)

    def test_kassel_country_correction_is_active_in_latex_only(self):
        network = load_network()
        kassel = {
            "4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:906",
            "4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:923",
        }
        self.assertTrue(kassel <= set(network.panels["DE"].actors))
        self.assertFalse(kassel & set(network.panels["BE"].actors))


if __name__ == "__main__":
    unittest.main()
