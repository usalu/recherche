import json
import tempfile
import unittest
from pathlib import Path

from netz.data.strict_review import load_strict_review


class StrictReviewActivationTests(unittest.TestCase):
    def test_missing_manifest_is_inactive(self):
        with tempfile.TemporaryDirectory() as d:
            bundle = load_strict_review(
                str(Path(d) / "missing.json"), "x", "y", "z", "k"
            )
        self.assertFalse(bundle.active)
        self.assertEqual(bundle.exclude, frozenset())

    def test_false_approval_is_inactive_even_without_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            manifest = Path(d) / "manifest.json"
            manifest.write_text(json.dumps({"approved_for_render_prune": False}), encoding="utf-8")
            bundle = load_strict_review(str(manifest), "x", "y", "z", "k")
        self.assertFalse(bundle.active)

    def test_approved_but_incomplete_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            manifest = Path(d) / "manifest.json"
            manifest.write_text(json.dumps({"approved_for_render_prune": True}), encoding="utf-8")
            with self.assertRaises(RuntimeError):
                load_strict_review(str(manifest), "x", "y", "z", "k")

    def test_approved_programmes_are_separate_from_actors(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            manifest = root / "manifest.json"
            prune = root / "prune.json"
            redirects = root / "redirects.json"
            overrides = root / "overrides.json"
            classification = root / "classification.json"
            manifest.write_text(json.dumps({"approved_for_render_prune": True}), encoding="utf-8")
            prune.write_text("[]", encoding="utf-8")
            redirects.write_text("{}", encoding="utf-8")
            overrides.write_text("{}", encoding="utf-8")
            classification.write_text(json.dumps({
                "actor": {"report_entity_type": "Organisation"},
                "programme": {"report_entity_type": "Programm"},
            }), encoding="utf-8")
            bundle = load_strict_review(
                str(manifest), str(prune), str(redirects), str(overrides), str(classification)
            )
        self.assertTrue(bundle.active)
        self.assertEqual(bundle.programmes, frozenset({"programme"}))


if __name__ == "__main__":
    unittest.main()
