import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from netz.render.latex import graph_tikz


REPO = Path(__file__).resolve().parents[4]
PILOT_DIR = REPO / "_neo4j" / "review" / "2026-08_akteursnetz_faktencheck"
MANIFEST = PILOT_DIR / "bilder_pilot" / "pilot_transport_manifest.json"
SCRIPT = PILOT_DIR / "pilot_images.py"
MISSING_DIR = PILOT_DIR / "bilder_full" / "harvest_missing"
MISSING_SELECTION = MISSING_DIR / "selection.json"
MISSING_MANIFEST = MISSING_DIR / "manifest.json"
MISSING_FREEZE = MISSING_DIR / "freeze_lock.json"
SEMIO_GRAPH = Path(r"E:\semio\print\tex\semio-graph.sty")


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

    def test_image_keeps_each_existing_node_state(self):
        for state in ("focal", "attested", "hypo"):
            with self.subTest(state=state), mock.patch.object(
                graph_tikz, "node_role", return_value=SimpleNamespace(state=state)
            ):
                got = graph_tikz.node_tikz(
                    FakeNet(), "e1", 1.25, 2.5, images={"e1": "E:/assets/U01.png"}
                )
            self.assertIn(f"[state={state},image={{E:/assets/U01.png}}]", got)
            self.assertTrue(got.endswith("{U01}"))

    def test_country_figure_never_assigns_an_image_to_a_project(self):
        panel = SimpleNamespace(actors=["a"], projects=["p"])
        net = SimpleNamespace(
            panels={"AT": panel}, tid={"a": "U01", "p": "P1"}
        )
        positions = {"a": (1.0, 2.0), "p": (3.0, 4.0)}
        with mock.patch.object(graph_tikz, "drawn_edge_nodes", return_value=set()), \
             mock.patch.object(graph_tikz, "force_layout", return_value=(positions, [])), \
             mock.patch.object(graph_tikz, "node_role", return_value=graph_tikz.PLAIN):
            tex, *_ = graph_tikz.country_figure(
                net, "AT", images={"a": "E:/assets/U01.png", "p": "E:/assets/P1.png"}
            )
        self.assertIn(r"\SemioGraphNode[image={E:/assets/U01.png}]{1.00,2.00}{U01}", tex)
        self.assertIn(r"\SemioGraphNode{3.00,4.00}{P1}", tex)
        self.assertNotIn("P1.png", tex)

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

    def test_semio_clip_contour_and_label_order(self):
        sty = SEMIO_GRAPH.read_text(encoding="utf-8")
        image_fn = sty.index(r"\cs_new_protected:Npn \semio_graph_node_image_draw:nn")
        clip = sty.index(r"\clip (#1) circle", image_fn)
        graphic = sty.index(r"\includegraphics", clip)
        draw_fn = sty.index(r"\cs_new_protected:Npn \semio_graph_node_draw:nnn", graphic)
        image_call = sty.index(r"\semio_graph_node_image_draw:nn", draw_fn)
        contour = sty.index("fill=none", image_call)
        label = sty.index(r"\node [ semio~graph~label", contour)
        self.assertLess(clip, graphic)
        self.assertLess(image_call, contour)
        self.assertLess(contour, label)


class PilotArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = load_pilot_module()
        cls.manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_manifest_passes_asset_validator(self):
        self.assertEqual(self.pilot.validate_manifest(self.manifest), [])

    def test_rendered_pdf_keeps_colored_logo_inside_circle(self):
        report = self.pilot.validate_rendered_pdfs(self.manifest)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["logo_count"], 11)
        for theme in ("light", "dark"):
            self.assertEqual(len(report["themes"][theme]), 11)
            for image in report["themes"][theme]:
                self.assertGreater(
                    image["square_corner_radius_pt"], report["circle_radius_pt"]
                )
                self.assertLessEqual(
                    image["visible_radius_pt"], report["circle_radius_pt"] * 0.94
                )

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


class MissingHarvestArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selection = json.loads(MISSING_SELECTION.read_text(encoding="utf-8"))
        cls.manifest = json.loads(MISSING_MANIFEST.read_text(encoding="utf-8"))
        cls.freeze = json.loads(MISSING_FREEZE.read_text(encoding="utf-8"))

    def test_fixed_186_actor_scope(self):
        rows = self.selection["nodes"]
        self.assertEqual(len(rows), 186)
        self.assertEqual(len({row["eid"] for row in rows}), 186)
        self.assertEqual(
            {origin: sum(row["queue_origin"] == origin for row in rows)
             for origin in ("existing_none", "new_actor")},
            {"existing_none": 65, "new_actor": 121},
        )

    def test_current_logo_assets_are_frozen(self):
        self.assertEqual(self.freeze["logo_rows"], 476)
        self.assertEqual(self.freeze["none_rows"], 65)
        self.assertEqual(self.freeze["light_assets"], 476)
        self.assertEqual(self.freeze["dark_assets"], 276)
        self.assertEqual(self.freeze["logo_opacity_percent"], 100)
        self.assertEqual(len(self.freeze["files"]), 755)

    def test_every_actor_has_a_terminal_harvest_outcome(self):
        rows = self.manifest["nodes"]
        self.assertEqual(len(rows), 186)
        self.assertEqual(
            {row["verification_result"] for row in rows},
            {"verified_candidates", "none_found"},
        )
        self.assertFalse(any(row["verification_result"] == "manual_check" for row in rows))
        self.assertTrue(all(row.get("identity_review_basis") for row in rows if row["verification_result"] == "none_found"))
        self.assertEqual(self.manifest.get("validation"), "PASS")

    def test_transport_is_compact_and_contains_no_acceptance(self):
        for row in self.manifest["nodes"]:
            candidates = row.get("verified_candidates", []) + row.get("manual_candidates", [])
            self.assertLessEqual(len(candidates), 3, row["name"])
            self.assertFalse(
                {"preferred_candidate", "suggested_candidate_id", "accepted_candidate_id"} & set(row),
                row["name"],
            )
            for candidate in candidates:
                source = PILOT_DIR / "bilder_full" / candidate["source_path"]
                preview = PILOT_DIR / "bilder_full" / candidate["preview_path"]
                self.assertTrue(source.is_file(), source)
                self.assertTrue(preview.is_file(), preview)

    def test_candidate_dossiers_are_compacted(self):
        dossiers = list((MISSING_DIR / "candidates").rglob("candidates.json"))
        self.assertEqual(len(dossiers), 177)
        for path in dossiers:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(payload.get("transport_compacted"), path)
            self.assertLessEqual(len(payload.get("candidates", [])), 3, path)


if __name__ == "__main__":
    unittest.main()
