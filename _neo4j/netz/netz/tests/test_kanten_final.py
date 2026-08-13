import json
import unittest

from netz.cli import load_network
from netz.mechanisms.connectivity import drawn_edge_nodes
from netz.mechanisms.layout import DEFAULT_FRAME, force_layout
from netz.sources import DEFAULT


def _pairs(path):
    with open(path, encoding="utf-8") as handle:
        return {tuple(sorted(pair)) for pair in json.load(handle)}


class FinalKantenActivationTests(unittest.TestCase):
    def test_final_positive_list_is_the_latex_model_edge_set(self):
        keep_path = DEFAULT.prune_kanten_final_path.replace(
            "prune_kanten_final.json", "keep_kanten_final.json"
        )
        keep = _pairs(keep_path)
        prune = _pairs(DEFAULT.prune_kanten_final_path)

        self.assertEqual(570, len(keep | prune))
        self.assertFalse(keep & prune)
        self.assertEqual(477, len(keep))
        self.assertEqual(93, len(prune))

        network = load_network()
        drawn = {tuple(sorted(pair)) for pair in network.drawn}
        self.assertEqual(keep, drawn)
        self.assertFalse(prune & drawn)

        visible = set()
        for panel in network.panels.values():
            nodes = drawn_edge_nodes(panel, min_comp=2)
            _, edges = force_layout(panel, nodes, DEFAULT_FRAME)
            visible.update(tuple(sorted(pair)) for pair in edges)
        self.assertEqual(keep, visible)

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
