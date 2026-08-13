# -*- coding: utf-8 -*-
"""Dependency-free integrity tests for the full image collection transport."""
from __future__ import annotations

import json
import hashlib
import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent / "bilder_full"


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class FullImageCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = load("selection.json")
        cls.domains = load("domains_review.json")
        cls.manifest = load("collection_manifest.json")

    def test_final_network_partition(self):
        self.assertEqual(self.selection["drawn_network_nodes"], 859)
        self.assertEqual(self.selection["organisation_nodes"], 762)
        self.assertEqual(self.selection["project_nodes_excluded"], 97)

    def test_all_transport_keys_are_unique_and_complete(self):
        selected = [row["key"] for row in self.selection["nodes"]]
        self.assertEqual(len(selected), 762)
        self.assertEqual(len(set(selected)), 762)
        self.assertEqual(set(selected), {row["key"] for row in self.domains["nodes"]})
        self.assertEqual(set(selected), {row["key"] for row in self.manifest["nodes"]})

    def test_domain_states_are_explicit(self):
        allowed = {"accepted", "needs_review", "no_candidate", "resolved_none"}
        self.assertTrue(all(row["status"] in allowed for row in self.domains["nodes"]))
        self.assertTrue(all(row.get("official_url") for row in self.domains["nodes"] if row["status"] == "accepted"))

    def test_candidate_previews_match_metadata_and_quality_rule(self):
        checked = 0
        for row in self.manifest["nodes"]:
            rel = row.get("candidate_metadata")
            if not rel:
                continue
            meta = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            for candidate in meta.get("candidates", []):
                if candidate.get("status") != "candidate":
                    continue
                preview = ROOT / candidate["preview_path"]
                self.assertTrue(preview.is_file(), preview)
                with Image.open(preview) as image:
                    self.assertEqual(image.format, "PNG")
                    self.assertEqual(image.size, (candidate["width"], candidate["height"]))
                self.assertEqual(hashlib.sha256(preview.read_bytes()).hexdigest(), candidate["preview_sha256"])
                self.assertRegex(candidate["source_sha256"], r"^[0-9a-f]{64}$")
                self.assertRegex(candidate["retrieved_at"], r"^\d{4}-\d{2}-\d{2}$")
                self.assertEqual(candidate["review_status"], "pending")
                self.assertTrue(candidate["format"] == "svg" or min(candidate["width"], candidate["height"]) >= 128)
                checked += 1
        self.assertGreater(checked, 0)

    def test_manifest_counts_are_consistent(self):
        actual = {}
        for row in self.manifest["nodes"]:
            actual[row["collection_result"]] = actual.get(row["collection_result"], 0) + 1
        self.assertEqual(actual, self.manifest["counts"])
        self.assertEqual(sum(actual.values()), 762)

    def test_transport_does_not_claim_neo4j_import(self):
        self.assertIs(self.manifest["transport_only"], True)

    def test_suggestions_are_complete_but_never_confirmed(self):
        suggestions = load("suggestions.json")
        self.assertEqual(len(suggestions["nodes"]), 762)
        self.assertEqual({r["key"] for r in suggestions["nodes"]},
                         {r["key"] for r in self.selection["nodes"]})
        self.assertTrue(all(r["suggested_result"] in {"logo", "none"} for r in suggestions["nodes"]))
        self.assertTrue(all(r["confirmed"] is False for r in suggestions["nodes"]))

    def test_review_ui_requires_an_explicit_post(self):
        html = (ROOT.parent / "full_image_review.html").read_text(encoding="utf-8")
        self.assertIn("/api/decision", html)
        self.assertIn("Vorschlag", html)
        self.assertNotIn("approveAll", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
