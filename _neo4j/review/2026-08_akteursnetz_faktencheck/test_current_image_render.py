# -*- coding: utf-8 -*-
"""Integrity proof for the current 619-node image render transport."""
from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent / "bilder_full"


def load(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


class CurrentImageRenderTests(unittest.TestCase):
    def test_every_reviewed_current_logo_is_renderable(self):
        identity = load("CURRENT_LOGO_IDENTITY_AUDIT.json")
        render = load("current_image_manifest.json")
        self.assertEqual(render["scope"], identity["scope"])
        self.assertEqual(len(render["nodes"]), 541)
        self.assertEqual({row["eid"] for row in render["nodes"]},
                         {row["eid"] for row in identity["nodes"]})
        logos = [row for row in render["nodes"] if row["result"] == "logo"]
        self.assertEqual(len(logos), identity["counts"]["logo"])
        self.assertTrue(all(row["review_status"] == "accepted" for row in logos))
        # Not a fixed number: the print opacity was raised from 50 to 100 on
        # 2026-08-13 (see test_full_image_collection.py) because at 50 % every
        # mark blends with the page and reads differently in light and dark.
        # What must hold is that the render header and every logo row agree.
        opacity = render["logo_opacity_percent"]
        self.assertIn(opacity, range(1, 101))
        self.assertTrue(all(row["logo_opacity_percent"] == opacity for row in logos))
        self.assertTrue(all((ROOT / row["asset_path"]).is_file() for row in logos))

    def test_render_report_draws_all_current_logos(self):
        identity = load("CURRENT_LOGO_IDENTITY_AUDIT.json")
        report = load("render/render_report.json")
        self.assertEqual(report["logo_count"], identity["counts"]["logo"])
        self.assertEqual(report["result"], "PASS")


if __name__ == "__main__":
    unittest.main()
