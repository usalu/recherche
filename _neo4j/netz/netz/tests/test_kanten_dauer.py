import hashlib
import json
import unittest
from pathlib import Path

from netz.cli import load_network
from netz.render.latex.table_grid import load_kanten
from netz.sources import DEFAULT


BASE = Path(DEFAULT.kanten_klassifikation_path).parent
DURATION_PATH = BASE / "kanten_dauer_final.json"
ALLOWED = {
    "dauerhaft",
    "befristeter Verbund",
    "projektgebunden",
    "einmalig",
    "unklar",
}


class CurrentKantenDurationTests(unittest.TestCase):
    def test_duration_review_matches_current_latex_edge_set(self):
        network = load_network()
        by_country = load_kanten(
            DEFAULT.kanten_klassifikation_path,
            network,
            DEFAULT.merge_strict_path,
        )
        visible = {
            row["id"]: row
            for country_rows in by_country.values()
            for row in country_rows
        }

        with open(DEFAULT.kanten_klassifikation_path, encoding="utf-8") as handle:
            canonical = json.load(handle)
        duration_ids = {rid for rid, row in canonical.items() if "dauer" in row}

        self.assertEqual(264, len(network.drawn))
        self.assertEqual(264, len(visible))
        self.assertEqual(set(visible), duration_ids)
        self.assertTrue(all(canonical[rid]["dauer"] in ALLOWED for rid in visible))
        self.assertTrue(all(canonical[rid]["dauer_begruendung"] for rid in visible))
        self.assertTrue(all(canonical[rid]["dauer_review_run"] for rid in visible))
        self.assertFalse(any(
            canonical[rid]["dauer_status"] == "type_conflict" for rid in visible
        ))

        corrections = {
            "BE:K086": (
                "Regulatorische Anerkennung", "A→B",
                "Erkannte Tracimat als Sloopbeheerorganisation an.",
            ),
            "NL:K066": (
                "Bauherrschaft", "A→B", "Entwickelte und baute Circl.",
            ),
            "SE:K001": (
                "Konzernbindung", "A→B",
                "Ist Miteigentümerin von Bygghubben.",
            ),
            "SE:K014": (
                "Konzernbindung", "B→A",
                "Ist Miteigentümerin von Bygghubben.",
            ),
            "SE:K015": (
                "Konzernbindung", "B→A",
                "Ist Miteigentümerin und Mitgründerin von Bygghubben.",
            ),
        }
        for rid, expected in corrections.items():
            self.assertEqual(expected, (
                canonical[rid]["beziehungsart"], canonical[rid]["richtung"],
                canonical[rid]["beschreibung"],
            ))
            self.assertTrue(canonical[rid]["type_correction_reason"])
            self.assertTrue(canonical[rid]["beziehungsart_vor_dauerpruefung"])
            self.assertTrue(canonical[rid]["richtung_vor_dauerpruefung"])
            self.assertTrue(canonical[rid]["beschreibung_vor_dauerpruefung"])

    def test_derived_duration_file_is_complete_and_current(self):
        payload = json.loads(DURATION_PATH.read_text(encoding="utf-8"))
        rows = payload["relationships"]
        ids = {row["id"] for row in rows}

        self.assertEqual(618, payload["visible_nodes"])
        self.assertEqual(264, payload["visible_edges"])
        self.assertEqual(264, len(rows))
        self.assertEqual(264, len(ids))
        self.assertFalse({"BE:K013", "GB:K027", "GB:K057", "NL:K067"} & ids)

        digest = hashlib.sha256(
            Path(DEFAULT.kanten_klassifikation_path).read_bytes()
        ).hexdigest()
        self.assertEqual(payload["classification_sha256_after_apply"], digest)

    def test_latex_relationship_rows_show_duration(self):
        from netz.render.latex.table_grid import _edge_row

        network = load_network()
        by_country = load_kanten(
            DEFAULT.kanten_klassifikation_path,
            network,
            DEFAULT.merge_strict_path,
        )
        rendered = 0
        for rows in by_country.values():
            for row in rows:
                latex = "\n".join(_edge_row(network, row, 0.0, {}))
                self.assertIn(row["dauer"], latex)
                rendered += 1
        self.assertEqual(264, rendered)

        fragment = Path(__file__).resolve().parents[2] / "figs" / "frag_tables_grid.tex"
        text = fragment.read_text(encoding="utf-8")
        self.assertEqual(40, text.count("{dauerhaft}"))
        self.assertEqual(32, text.count("{befristeter Verbund}"))
        self.assertEqual(173, text.count("{projektgebunden}"))
        self.assertEqual(19, text.count("{einmalig}"))


if __name__ == "__main__":
    unittest.main()
