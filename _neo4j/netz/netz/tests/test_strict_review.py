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


if __name__ == "__main__":
    unittest.main()
