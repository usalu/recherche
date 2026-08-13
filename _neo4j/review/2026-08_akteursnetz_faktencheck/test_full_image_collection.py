# -*- coding: utf-8 -*-
"""Dependency-free integrity tests for the full image collection transport."""
from __future__ import annotations

import json
import hashlib
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

import full_image_collection as collection
import pilot_images as pilot


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

    def test_suggestions_exclude_photos_partner_marks_and_wrong_media_logos(self):
        node = {"name": "FORE Partnership"}
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "media_logo", "url": "https://fore.example/logos/logo_nzero.png"}))
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "og_image", "url": "https://fore.example/team/photo.jpg"}))
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "media_logo", "url": "https://fore.example/logo_other-company.svg"}))
        self.assertFalse(collection.candidate_rejection(node, {
            "kind": "media_logo", "url": "https://fore.example/FORE-logo.svg"}))

    def test_media_logo_identity_comes_from_filename_not_parent_path(self):
        node = {"name": "BioRegional"}
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "media_logo",
            "url": "https://storage.example/www.bioregional.com/Abstrakt-Logo.svg",
        }))

    def test_final_visual_audit_rejections_stay_withheld(self):
        suggestions = {row["key"]: row for row in load("suggestions.json")["nodes"]}
        rejected = set(collection.MANUAL_CANDIDATE_REJECTIONS) | set(collection.MANUAL_DOMAIN_REJECTIONS)
        self.assertTrue(rejected)
        self.assertTrue(all(suggestions[key]["suggested_result"] == "none" for key in rejected))
        self.assertTrue(all(suggestions[key]["suggested_candidate_id"] == "" for key in rejected))

    def test_visible_header_logo_outranks_an_app_icon(self):
        node = {"name": "Elliott Wood"}
        icon = {"kind": "apple_touch", "width": 256, "height": 256, "url": "https://example/icon.png"}
        header = {"kind": "header_logo", "width": 512, "height": 128, "url": "https://example/elliott.svg"}
        self.assertGreater(collection.candidate_rank(header, node), collection.candidate_rank(icon, node))

    def test_ambiguous_automated_domains_are_withheld(self):
        mace = {"name": "Mace"}
        restaurant = {"status": "accepted", "basis": "individual_official_web_research",
                      "official_url": "https://mace-restaurant.de/",
                      "research_candidates": [{"url": "https://mace-restaurant.de/",
                                                 "page_title": "MACE Restaurant"}]}
        self.assertTrue(collection.domain_suggestion_rejection(mace, restaurant))
        fore = {"name": "FORE Partnership"}
        official = {"status": "accepted", "basis": "individual_identity_check",
                    "official_url": "https://www.forepartnership.com/",
                    "page_title": "FORE Partnership | Sustainable Real Estate"}
        self.assertFalse(collection.domain_suggestion_rejection(fore, official))

    def test_json_ld_organisation_logo_is_discovered(self):
        parser = pilot.IconParser()
        parser.feed('<script type="application/ld+json">'
                    '{"@type":"Organization","name":"FORE Partnership",'
                    '"logo":{"url":"https://example/FORE-logo.jpg"}}'
                    '</script>')
        self.assertIn((4, "structured_logo", "https://example/FORE-logo.jpg"), parser.candidates)

    def test_css_header_mask_logo_is_discovered(self):
        urls = pilot.css_header_logo_candidates(
            '.header__logo{mask-image:url("../img/ewood-black.svg")}',
            'https://example/assets/css/final.css')
        self.assertEqual(urls, ['https://example/assets/img/ewood-black.svg'])

    def test_review_ui_requires_an_explicit_post(self):
        html = (ROOT.parent / "full_image_review.html").read_text(encoding="utf-8")
        self.assertIn("/api/decision", html)
        self.assertIn("theme=dark", html)
        self.assertIn("Vorschlag", html)
        self.assertIn('id="logoOpacity" type="range"', html)
        self.assertIn("--logo-opacity", html)
        self.assertIn("akteursnetz.logoOpacity", html)
        self.assertIn("Nicht vorschlagen", html)
        self.assertIn(".candidate:not(.rejected)", html)
        self.assertNotIn("approveAll", html)

    def test_review_state_blocks_rejected_candidates(self):
        state = collection.review_state()
        by_key = {row["key"]: row for row in state["nodes"]}
        fore = by_key["GB:U26"]
        self.assertFalse(next(row for row in fore["candidates"] if row["id"] == "c04")["suggestion_rejection"])
        self.assertTrue(next(row for row in fore["candidates"] if row["id"] == "c05")["suggestion_rejection"])
        self.assertTrue(all(row["suggestion_rejection"] for row in by_key["GB:U39"]["candidates"]))

    def test_coloured_rectangle_is_preserved_as_a_full_circle_crop(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "blue-tile.png"
            image = Image.new("RGBA", (400, 200), (12, 88, 170, 255))
            ImageDraw.Draw(image).ellipse((180, 80, 220, 120), fill=(255, 255, 255, 255))
            image.save(source)
            prepared, mode = pilot.prepare_node_canvas(source)

        self.assertEqual(mode, "circle_cover")
        self.assertEqual(prepared.size, (256, 256))
        self.assertGreater(prepared.getpixel((128, 2))[3], 240)
        self.assertEqual(prepared.getpixel((0, 0))[3], 0)
        self.assertEqual(prepared.getpixel((255, 255))[3], 0)
        self.assertEqual(prepared.getpixel((128, 20))[:3], (12, 88, 170))

    def test_freestanding_mark_remains_fully_contained_inside_circle(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "transparent-mark.png"
            image = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
            ImageDraw.Draw(image).rectangle((10, 10, 389, 89), fill=(220, 30, 60, 255))
            image.save(source)
            prepared, mode = pilot.prepare_node_canvas(source)
            wrapper_prepared = collection.prepared_canvas(source)

        self.assertEqual(mode, "safe_contain")
        self.assertLessEqual(pilot.alpha_max_radius(prepared), pilot.SAFE_RADIUS + 0.75)
        self.assertEqual(prepared.getpixel((0, 0))[3], 0)
        self.assertEqual(wrapper_prepared.size, (256, 256))

    def test_neutral_rectangle_is_knocked_out_and_ink_is_theme_tokenised(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "wordmark-on-white.png"
            image = Image.new("RGBA", (400, 160), (255, 255, 255, 255))
            ImageDraw.Draw(image).rectangle((70, 50, 330, 110), fill=(30, 30, 30, 255))
            image.save(source)
            backdrop = pilot.neutral_edge_backdrop(image)
            light_separated = pilot.neutral_backdrop_to_transparency(image, "light", backdrop)
            dark_separated = pilot.neutral_backdrop_to_transparency(image, "dark", backdrop)
            light, light_mode = pilot.prepare_node_canvas(source, theme="light")
            dark, dark_mode = pilot.prepare_node_canvas(source, theme="dark")

        self.assertIsNotNone(backdrop)
        self.assertEqual(light_separated.getpixel((10, 10))[3], 0)
        self.assertEqual(dark_separated.getpixel((10, 10))[3], 0)
        self.assertEqual(light_separated.getpixel((200, 80))[:3], pilot.SEMIO_DARK)
        self.assertEqual(dark_separated.getpixel((200, 80))[:3], pilot.SEMIO_LIGHT)
        self.assertEqual(light_mode, "neutral_knockout")
        self.assertEqual(dark_mode, "neutral_knockout")
        self.assertEqual(light.getchannel("A").getbbox(), dark.getchannel("A").getbbox())

    def test_transparent_white_mark_is_visible_in_both_themes(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "white-wordmark.png"
            image = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
            ImageDraw.Draw(image).rectangle((20, 20, 380, 80), fill=(255, 255, 255, 255))
            image.save(source)
            light, _ = pilot.prepare_node_canvas(source, theme="light")
            dark, _ = pilot.prepare_node_canvas(source, theme="dark")
        light_colours = {rgba[:3] for _count, rgba in light.getcolors(light.width * light.height)
                         if rgba[3] > 240}
        dark_colours = {rgba[:3] for _count, rgba in dark.getcolors(dark.width * dark.height)
                        if rgba[3] > 240}
        self.assertIn(pilot.SEMIO_DARK, light_colours)
        self.assertIn(pilot.SEMIO_LIGHT, dark_colours)


if __name__ == "__main__":
    unittest.main(verbosity=2)
