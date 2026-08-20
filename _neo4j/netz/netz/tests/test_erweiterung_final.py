import json
import unittest

from netz.cli import load_network
from netz.render.latex.table_grid import load_kanten
from netz.sources import DEFAULT


class FinalExpansionTests(unittest.TestCase):
    def setUp(self):
        with open(DEFAULT.expansion_final_path, encoding="utf-8") as handle:
            self.data = json.load(handle)
        with open(DEFAULT.expansion_klassifikation_path, encoding="utf-8") as handle:
            self.nodes = json.load(handle)
        with open(DEFAULT.expansion_kanten_path, encoding="utf-8") as handle:
            self.edges = json.load(handle)

    def test_expansion_is_complete_and_source_gated(self):
        self.assertTrue(self.data["approved_for_latex"])
        self.assertFalse(self.data["neo4j_changed"])
        self.assertEqual(191, len(self.data["nodes"]))
        self.assertEqual(190, len(self.data["edges"]))
        self.assertEqual(191, len(self.nodes))
        self.assertEqual(190, len(self.edges))
        self.assertTrue(all(row["beleg_url"] for row in self.nodes.values()))
        self.assertTrue(all(row["evidence_url"] for row in self.edges.values()))
        self.assertTrue(all(row["evidence_quote"] for row in self.edges.values()))
        self.assertTrue(all(len(row["beschreibung"]) <= 60 for row in self.edges.values()))
        self.assertTrue(all(
            row["beziehungsprofil"] == "Vorhabenspezifisch / Vorhaben"
            for row in self.edges.values()
        ))

    def test_strict_removals_and_corrections_are_active(self):
        removed = {
            "candidate-edge:proposal:proj:108:B:3",
            "candidate-edge:proposal:proj:104:A:1",
            "candidate-edge:proposal:proj:115:A:1",
            "candidate-edge:proposal:proj:69:A:2",
        }
        self.assertFalse(removed & set(self.edges))
        self.assertNotIn("proposal:proj:106:B:4", self.edges)
        self.assertIn(
            "candidate-edge:replacement:tradlab-tre:norsk-folkemuseum",
            self.edges,
        )
        self.assertEqual("La Caserne de Reuilly", self.nodes["proj:95"]["name"])
        self.assertIn("candidate:proj:76:B:2", self.nodes)
        self.assertNotIn("candidate:proj:79:B:1", self.nodes)

    def test_graph_table_and_expansion_are_identical(self):
        network = load_network()
        by_country = load_kanten(
            DEFAULT.kanten_klassifikation_path,
            network,
            DEFAULT.merge_strict_path,
            DEFAULT.expansion_kanten_path,
        )
        table_pairs = {
            tuple(sorted(row["pair"]))
            for rows in by_country.values()
            for row in rows
        }
        self.assertEqual(809, sum(
            len(panel.actors) + len(panel.projects)
            for panel in network.panels.values()
        ))
        self.assertEqual(452, len(network.drawn))
        self.assertEqual(452, len(table_pairs))
        self.assertEqual(
            {tuple(sorted(pair)) for pair in network.drawn},
            table_pairs,
        )


if __name__ == "__main__":
    unittest.main()
