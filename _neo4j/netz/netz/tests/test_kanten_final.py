import json
import unittest

from netz.cli import load_network
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


if __name__ == "__main__":
    unittest.main()
