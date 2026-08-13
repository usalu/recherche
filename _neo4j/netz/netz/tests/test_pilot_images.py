import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from netz.render.latex import graph_tikz


REPO = Path(__file__).resolve().parents[4]
PILOT_DIR = REPO / "_neo4j" / "review" / "2026-08_akteursnetz_faktencheck"
MANIFEST = PILOT_DIR / "bilder_pilot" / "pilot_transport_manifest.json"
SCRIPT = PILOT_DIR / "pilot_images.py"


def load_pilot_module():
    spec = importlib.util.spec_from_file_location("pilot_images_test_target", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeNet:
    tid = {"e1": "U01"}


class GraphImageRendererTests(unittest.TestCase):
    def test_no_image_keeps_historical_node_call(self):
        with mock.patch.object(graph_tikz, "node_role", return_value=graph_tikz.PLAIN):
            got = graph_tikz.node_tikz(FakeNet(), "e1", 1.25, 2.5)
        self.assertEqual(got, r"\SemioGraphNode{1.25,2.50}{U01}")

    def test_image_is_optional_key_and_label_is_unchanged(self):
        with mock.patch.object(graph_tikz, "node_role", return_value=graph_tikz.PLAIN):
            got = graph_tikz.node_tikz(
                FakeNet(), "e1", 1.25, 2.5, images={"e1": "E:/assets/U01.png"}
            )
        self.assertEqual(
            got,
            r"\SemioGraphNode[image={E:/assets/U01.png}]{1.25,2.50}{U01}",
        )

    def test_manifest_loader_uses_only_existing_accepted_logos(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            (td / "ok.png").write_bytes(b"png")
            payload = {
                "nodes": [
                    {"eid": "yes", "result": "logo", "review_status": "accepted", "asset_path": "ok.png"},
                    {"eid": "none", "result": "none", "review_status": "accepted", "asset_path": None},
                    {"eid": "pending", "result": "logo", "review_status": "candidate", "asset_path": "ok.png"},
                    {"eid": "missing", "result": "logo", "review_status": "accepted", "asset_path": "missing.png"},
                ]
            }
            path = td / "manifest.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            got = graph_tikz.load_image_manifest(path)
        self.assertEqual(set(got), {"yes"})
        self.assertTrue(got["yes"].replace("\\", "/").endswith("/ok.png"))


class PilotArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = load_pilot_module()
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_passes_asset_validator(self):
        self.assertEqual(self.pilot.validate_manifest(self.manifest), [])

    def test_fixed_pilot_distribution_and_outcomes(self):
        rows = self.manifest["nodes"]
        self.assertEqual(len(rows), 48)
        self.assertEqual(
            {cc: sum(r["cc"] == cc for r in rows) for cc in ("GB", "NL", "AT")},
            {"GB": 16, "NL": 16, "AT": 16},
        )
        self.assertEqual(sum(r["result"] == "logo" for r in rows), 11)
        self.assertEqual(sum(r["result"] == "none" for r in rows), 37)
        self.assertTrue(all(r["review_status"] == "accepted" for r in rows))


if __name__ == "__main__":
    unittest.main()
