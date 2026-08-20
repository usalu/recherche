import hashlib
import json
import unittest
from pathlib import Path

from netz.cli import load_network
from netz.render.latex.escape import esc
from netz.render.latex.table_grid import load_kanten
from netz.sources import DEFAULT


BASE = Path(DEFAULT.kanten_klassifikation_path).parent
PROFILE_PATH = BASE / "beziehungsprofil_final.json"
ALLOWED = {
    "Projektübergreifend / institutionell",
    "Projektübergreifend / strategisch",
    "Projektübergreifend / operativ",
    "Vorhabenspezifisch / Vorhaben",
    "Vorhabenspezifisch / Leistung",
    "Vorhabenspezifisch / Ereignis",
}


class CurrentKantenProfileTests(unittest.TestCase):
    def test_profile_review_matches_current_latex_edge_set(self):
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
        profile_ids = {
            rid for rid, row in canonical.items() if "beziehungsprofil" in row
        }

        self.assertEqual(262, len(network.drawn))
        self.assertEqual(262, len(visible))
        self.assertEqual(set(visible), profile_ids)
        self.assertTrue(all(
            canonical[rid]["beziehungsprofil"] in ALLOWED for rid in visible
        ))
        self.assertTrue(all(
            canonical[rid]["beziehungsprofil_begruendung"] for rid in visible
        ))
        self.assertTrue(all(
            canonical[rid]["profile_review_run"] for rid in visible
        ))
        self.assertFalse(any("dauer" in row for row in canonical.values()))

        corrections = {
            "AT:K023": (
                "Soziale Rückbauarbeit", "B→A",
                "Beschäftigte mit DRZ 25 Personen beim Rückbau.",
            ),
            "CH:K007": (
                "Gründungsimpuls", "A→B", "Gab den Impuls zur Gründung.",
            ),
            "CH:K026": (
                "Gründungsimpuls", "A→B", "Gab den Impuls zur Gründung.",
            ),
            "CH:K036": (
                "Plattformzugehörigkeit", "A→B",
                "Umfasst UMAR als Forschungsunit.",
            ),
            "DE:K002": (
                "Testbau", "B→A",
                "Errichtete mit Biele drei Testbauten aus Platten.",
            ),
            "DE:K005": (
                "Projektleitung", "A→B",
                "Leitete und initiierte das Pilotprojekt.",
            ),
            "SE:K023": (
                "Konsortialpartnerschaft", "—",
                "Arbeiteten im schwedischen ReCreate-Pilot zusammen.",
            ),
        }
        for rid, expected in corrections.items():
            self.assertEqual(expected, (
                canonical[rid]["beziehungsart"],
                canonical[rid]["richtung"],
                canonical[rid]["beschreibung"],
            ))
            self.assertTrue(canonical[rid]["type_correction_reason"])

        for rid in {"AT:K004", "NL:K019"}:
            self.assertTrue(canonical[rid]["entfernen"])
            self.assertTrue(canonical[rid]["removal_reason"])
            self.assertNotIn(rid, visible)

    def test_derived_profile_file_is_complete_and_current(self):
        payload = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
        rows = payload["relationships"]
        ids = {row["id"] for row in rows}

        self.assertEqual(618, payload["visible_nodes"])
        self.assertEqual(262, payload["visible_edges"])
        self.assertEqual(262, len(rows))
        self.assertEqual(262, len(ids))
        self.assertFalse({"AT:K004", "NL:K019"} & ids)
        self.assertTrue(all(row["evidence_url"] for row in rows))
        self.assertTrue(all(row["evidence_quote"] for row in rows))
        self.assertTrue(all(len(row["beschreibung"]) <= 60 for row in rows))

        digest = hashlib.sha256(
            Path(DEFAULT.kanten_klassifikation_path).read_bytes()
        ).hexdigest()
        self.assertEqual(payload["classification_sha256"], digest)

    def test_latex_relationship_rows_show_profile(self):
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
                self.assertIn(esc(row["beziehungsprofil"]), latex)
                rendered += 1
        self.assertEqual(262, rendered)

        fragment = Path(__file__).resolve().parents[2] / "figs" / "frag_tables_grid.tex"
        text = fragment.read_text(encoding="utf-8")
        self.assertIn(r"\section{Akteursbeziehungen}", text)
        self.assertIn("{Beziehungsprofil};", text)
        for profile in ALLOWED:
            self.assertIn(esc(profile), text)


if __name__ == "__main__":
    unittest.main()
