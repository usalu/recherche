# -*- coding: utf-8 -*-
"""Dependency-free integrity tests for the full image collection transport."""
from __future__ import annotations

import json
import hashlib
import gzip
import tempfile
import unittest
from pathlib import Path

import numpy as np
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

    def test_current_network_partition_and_deep_review_boundary(self):
        current = load("CURRENT_SCOPE_COVERAGE.json")
        deep = load("current_deep_review/manifest.json")
        self.assertEqual(current["network_nodes"], 619)
        self.assertEqual(current["organisation_nodes"], 541)
        self.assertEqual(current["project_nodes"], 78)
        self.assertEqual(current["logo_nodes"] + current["none_nodes"], 541)
        self.assertGreaterEqual(current["logo_nodes"], 460)
        self.assertEqual(len(deep["nodes"]), current["none_nodes"])
        self.assertEqual(sum(deep["counts"].values()), current["none_nodes"])
        self.assertTrue(all(row["confirmed"] is False for row in deep["nodes"]))
        gallery = ROOT / "current_deep_review" / "index.html"
        self.assertTrue(gallery.is_file())
        self.assertIn("541 Organisationen", gallery.read_text(encoding="utf-8"))
        preview_dir = ROOT / "current_deep_review" / "previews"
        for row in deep["nodes"]:
            preview = preview_dir / (row["key"].replace(":", "_") + ".png")
            self.assertEqual(preview.is_file(), row["suggested_result"] == "logo", row["key"])

    def test_current_logo_rights_audit_is_complete_and_conservative(self):
        deep = load("current_deep_review/manifest.json")
        for row in deep["nodes"]:
            if row["suggested_result"] != "logo":
                continue
            candidate = next(c for c in row["candidates"]
                             if c["id"] == row["suggested_candidate_id"])
            self.assertTrue(candidate["license_note"], row["key"])

        audit = load("CURRENT_IMAGE_RIGHTS_AUDIT.json")
        current = load("CURRENT_SCOPE_COVERAGE.json")
        expected = current["logo_nodes"] + deep["counts"]["logo"]
        self.assertEqual(audit["counts"]["rows"], expected)
        self.assertEqual(len(audit["nodes"]), expected)
        self.assertEqual(len({row["eid"] for row in audit["nodes"]}), expected)
        self.assertTrue(all(row["source_url"] for row in audit["nodes"]))
        self.assertTrue(all(row["rights_source_url"] for row in audit["nodes"]))
        self.assertTrue(all(row["license_note"] for row in audit["nodes"]))
        self.assertTrue(all(row["print_clearance"] != "cleared" for row in audit["nodes"]))
        self.assertEqual(sum(audit["counts"]["print_clearance"].values()), expected)

    def test_current_541_identity_audit_is_complete_and_assets_are_bounded(self):
        audit = load("CURRENT_LOGO_IDENTITY_AUDIT.json")
        self.assertEqual(audit["scope"], {
            "network_nodes": 619,
            "organisation_nodes": 541,
            "project_nodes_image_free": 78,
        })
        self.assertEqual(len(audit["nodes"]), 541)
        self.assertEqual(len({row["eid"] for row in audit["nodes"]}), 541)
        self.assertEqual(sum(audit["counts"].values()), 541)
        self.assertEqual(audit["open_identity_reviews"], 0)
        self.assertTrue(all(row["result"] in {"logo", "none"} for row in audit["nodes"]))
        self.assertTrue(all(row["reason"] for row in audit["nodes"]))
        gallery = ROOT / "CURRENT_LOGO_IDENTITY_AUDIT.html"
        self.assertTrue(gallery.is_file())
        gallery_text = gallery.read_text(encoding="utf-8")
        self.assertIn("541 Organisationen", gallery_text)
        self.assertEqual(gallery_text.count("<article "), 541)
        for row in audit["nodes"]:
            if row["result"] == "none":
                self.assertIsNone(row["asset_path"])
                continue
            path = ROOT / row["asset_path"]
            self.assertTrue(path.is_file(), row["key"])
            with Image.open(path) as image:
                self.assertEqual((image.format, image.mode, image.size),
                                 ("PNG", "RGBA", (256, 256)), row["key"])
                self.assertLessEqual(pilot.alpha_max_radius(image.convert("RGBA")),
                                     pilot.FINAL_SIZE / 2 + 0.75, row["key"])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),
                             row["asset_sha256"], row["key"])
            self.assertTrue(row["source_url"], row["key"])
            self.assertTrue(row["rights_status"], row["key"])

    def test_last_hunt_exact_marks_and_wrong_assets(self):
        final = {row["key"]: row for row in load("final_image_manifest.json")["nodes"]}
        expected = {
            "DE:U13": "dare-gmbh.de",
            "BE:M18": "hofman.be",
            "BE:M27": "mvvafbraak.be",
            "CH:U22": "srzh.ch",
            "FR:X01": "raedificare.com/wp-content/uploads/2026/04/logo.png",
            "FR:M20": "tailleurdepierre-bretagne.fr/wp-content/uploads/2020/10/logo_grayo2.png",
        }
        for key, source in expected.items():
            self.assertEqual(final[key]["result"], "logo", key)
            self.assertIn(source.lower(), final[key]["source_url"].lower(), key)
        current_verified = {
            "FR:M19": "logo-transparent-chemin",
            "GB:M09": "enviromate_logo_header_2x.png",
            "BE:S03": "sundahus-horisontell-2.png",
        }
        for key, source in current_verified.items():
            self.assertEqual(final[key]["result"], "logo", key)
            self.assertIn(source, final[key]["source_url"].lower(), key)
        self.assertEqual(final["BE:S02"]["result"], "none")

    def test_last_deep_dig_uses_only_verified_marks(self):
        final = {row["key"]: row for row in load("final_image_manifest.json")["nodes"]}
        expected = {
            "CH:S03": "Madaster-BrandmarkLogo-RGB.png",
            "FR:O05": "e755c5_7e60158d97e14b94a7e7ccdbb5ce1022~mv2.png",
            "FR:M57": "cbe7f0_4798aa34439643d0a0e7a89a9a3e91f3~mv2.png",
            "NL:U38": "d312e0_0ba87a49968b437c961f72de0a561fb5~mv2.png",
        }
        for key, source_name in expected.items():
            row = final[key]
            self.assertEqual(row["result"], "logo")
            self.assertTrue(row["source_url"].endswith(source_name), key)
        self.assertIn("Brandenburgische_Technische_Universit", final["DE:F01"]["source_url"])

    def test_final_official_media_pass_keeps_exact_sources_and_rejects_weak_substitutes(self):
        final = {row["key"]: row for row in load("final_image_manifest.json")["nodes"]}
        expected_sources = {
            "DK:F01": "media.adm.dtu.dk/designguide/",
            "FI:I02": "makasiini.hel.fi/helsinki-logos/",
            "BE:F07": "www.utwente.nl/.wh/",
            "DK:U28": "logopakke_realdania_100mm.zip#",
            "FR:M32": "reciprocite.fr/images/reciprocite.svg",
            "FR:M37": "materiauxdantan.fr/img/logo-",
            "FR:U07": "depuis1920.fr/",
            "FR:M39": "e4556a_ec866f8a133b4cb791f901e87ebc3fe3",
            "FR:M60": "45669a_8dd327e12a3a4082bd3525b868955246",
            "FI:U05": "aalto.fi/sites/default/files/favicons/",
            "FI:U10": "aalto.fi/sites/default/files/favicons/",
            "CH:U11": "b-3.ch/userdata/assets/logo/b3-logo-rgb.svg",
            "BE:S01": "madaster.com/app/uploads/sites/6/2023/09/madaster-brandmarklogo-rgb.png",
            "GB:F04": "inline+https://www.uea.ac.uk/",
            "NL:U44": "inline+https://rothuizen-architecten.nl/",
            "BE:N06": "inline+https://rotordb.org/",
            "BE:N05": "inline+https://opalis.eu/en",
            "NO:N03": "inline+https://www.futurebuilt.no/",
            "GB:U06": "inline+https://www.bdp.com/",
            "FR:U09": "grandhuit.eu/wp-content/themes/g8/images/l5.png",
            "DE:U20": "gate21-header.png",
            "FR:I01": "logo-lafab.svg",
            "FR:M33": "logo_final_transp_vect-2.png",
            "FR:U16": "3376b6_1903d6f0f4ce4ff28d4c2803593652de",
            "DE:F01": "brandenburgische_technische_universit",
            "SE:F02": "rise-logo-black.svg",
            "DE:U33": "danish_region_hovedstaden_logo.svg",
            "FI:U18": "inline+https://www.skanska.com/fi/fi",
            "AT:I02": "inline+https://viecycle.wien.gv.at/",
            "BE:F02": "buildwise.zip#svg/buildwise_verticaal_1.svg",
        }
        for key, source_part in expected_sources.items():
            row = final[key]
            self.assertEqual(row["result"], "logo", key)
            self.assertIn(source_part, row["source_url"].lower(), key)
        buildwise = final["BE:F02"]
        self.assertTrue(buildwise["dark_asset_path"].endswith("-dark.png"))
        self.assertIn("_neg.svg", buildwise["dark_source_url"])
        deep = {row["key"]: row for row in load("current_deep_review/manifest.json")["nodes"]}
        # BE:G01 and FR:M42 used to sit in this list too -- wrongly: both
        # had a real own-header-logo candidate that only failed the
        # short-edge floor (see STRUCTURAL_IDENTITY_KINDS' long-edge
        # exception), individually reviewed and confirmed as logo in
        # full_asset_review.json, so they are no longer in this "still
        # none" deep-review pool at all.
        for key in ("BE:I04", "CH:M13", "FR:M53"):
            self.assertEqual(deep[key]["suggested_result"], "none", key)

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
                # A structural/declared-identity kind (never og_image/media_logo/
                # editorial) may pass on the LONG edge alone -- see
                # STRUCTURAL_IDENTITY_KINDS and the wide-wordmark exception in
                # harvest_one. Every other kind keeps the short-edge floor.
                short_edge_ok = min(candidate["width"], candidate["height"]) >= 128
                long_edge_ok = (candidate.get("kind") in collection.STRUCTURAL_IDENTITY_KINDS
                                and max(candidate["width"], candidate["height"]) >= 128)
                self.assertTrue(candidate["format"] == "svg" or short_edge_ok or long_edge_ok)
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
        self.assertTrue(collection.MANUAL_CANDIDATE_REJECTIONS)
        self.assertFalse(any("*" in rules
                             for rules in collection.MANUAL_CANDIDATE_REJECTIONS.values()))
        for key, rules in collection.MANUAL_CANDIDATE_REJECTIONS.items():
            suggestion = suggestions[key]
            self.assertTrue(suggestion["suggested_result"] == "none"
                            or suggestion["suggested_candidate_id"] not in rules)
        for key in collection.MANUAL_DOMAIN_REJECTIONS:
            self.assertEqual(suggestions[key]["suggested_result"], "none")
            self.assertEqual(suggestions[key]["suggested_candidate_id"], "")

    def test_final_suggestion_audit_is_complete_and_clean(self):
        audit = load("final_review/FINAL_SUGGESTION_AUDIT.json")
        self.assertEqual(audit["selection_nodes"], 762)
        self.assertEqual(audit["final_logo_suggestions"] + audit["final_none_suggestions"], 762)
        self.assertEqual(audit["problems"], [])
        self.assertTrue(all(audit["checks"].values()))

    def test_bulk_suggestion_review_records_opacity_and_remains_revisable(self):
        if not (ROOT / "full_asset_review.json").is_file():
            self.skipTest("bulk acceptance has not been run")
        review = load("full_asset_review.json")
        suggestions = {row["key"]: row for row in load("suggestions.json")["nodes"]}
        self.assertEqual(len(review["nodes"]), 762)
        # Not a fixed number: the print opacity was raised from 50 to 100 on
        # 2026-08-13 because at 50 % every mark blends with the page and reads
        # differently in light and dark. What must hold is that the header and
        # every row agree, and that raising it changed nothing else -- same
        # candidate, same result, still provisional.
        opacity = review["logo_opacity_percent"]
        self.assertIn(opacity, range(1, 101))
        self.assertTrue(review["provisional"])
        for decision in review["nodes"]:
            # A row individually reviewed AFTER the bulk pass (source
            # sharpness upgrades, identity or crop corrections -- reviewer
            # is no longer the bulk-acceptance marker) has deliberately
            # moved past this snapshot: its own candidate_id/provisional no
            # longer has to match the frozen suggestion. Every row still
            # from the original bulk pass keeps the strict check.
            if decision.get("reviewer") != "user (bulk suggestion acceptance)":
                continue
            suggestion = suggestions[decision["key"]]
            self.assertEqual(decision["result"], suggestion["suggested_result"])
            self.assertEqual(decision["candidate_id"], suggestion["suggested_candidate_id"])
            self.assertEqual(decision["logo_opacity_percent"], opacity)
            self.assertTrue(decision["provisional"])

    def test_logo_opacity_scales_alpha_only(self):
        canvas = Image.new("RGBA", (2, 1), (20, 40, 60, 200))
        result = collection.apply_logo_opacity(canvas, 50)
        self.assertEqual(result.getpixel((0, 0)), (20, 40, 60, 100))
        self.assertEqual(canvas.getpixel((0, 0)), (20, 40, 60, 200))

    def test_visible_header_logo_outranks_an_app_icon(self):
        node = {"name": "Elliott Wood"}
        icon = {"kind": "apple_touch", "width": 256, "height": 256, "url": "https://example/icon.png"}
        header = {"kind": "header_logo", "width": 512, "height": 128, "url": "https://example/elliott.svg"}
        self.assertGreater(collection.candidate_rank(header, node), collection.candidate_rank(icon, node))

    def test_header_photos_and_generic_interface_icons_are_withheld(self):
        node = {"name": "Bureau Bouwtechniek"}
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "header_logo", "final_url": "https://b-b.be/Portretten/AlexanderS.jpg"}))
        self.assertTrue(collection.candidate_rejection(node, {
            "kind": "header_logo", "final_url": "https://b-b.be/assets/user.svg"}))

    def test_app_store_assets_and_salvo_subbrand_are_withheld(self):
        self.assertTrue(collection.candidate_rejection(
            {"key": "NL:S02", "name": "ReSource Marktplaats"},
            {"id": "c01", "kind": "declared_icon",
             "url": "https://play-lh.googleusercontent.com/icon.png"}))
        self.assertTrue(collection.candidate_rejection(
            {"key": "GB:M19", "name": "SalvoWEB"},
            {"id": "c01", "kind": "header_logo",
             "url": "https://www.salvoweb.com/assets/tr-logo.svg"}))

    def test_print_unidentifiable_visual_audit_files_are_withheld(self):
        # FI:U04's own "durat_logo_1200_x_3390_px_3.png" used to sit in this
        # list -- wrongly: it is Durat's own full-resolution logo, not
        # unidentifiable editorial content, and MANUAL_CANDIDATE_REJECTIONS
        # was corrected to stop blocking it (see full_image_collection.py's
        # own comment there).
        rejected = (
            ("FR:F01", "CSTB",
             "https://www.cstb.fr/getmedia/x/Logo_BATIPEDIA_540x390.jpg"),
            ("FR:M19", "Gauthey Cheminées",
             "https://cheminees-gauthey.fr/wp-content/uploads/2020/06/logo-ECC.jpg"),
        )
        for key, name, url in rejected:
            self.assertTrue(collection.candidate_rejection(
                {"key": key, "name": name},
                {"id": "c99", "kind": "header_logo", "url": url}))

        self.assertFalse(collection.candidate_rejection(
            {"key": "FR:M19", "name": "Gauthey Cheminées"},
            {"id": "c01", "kind": "header_logo",
             "url": "https://cheminees-gauthey.fr/wp-content/uploads/2017/03/"
                    "logo-transparent-chemin%65%CC%81es-gauthey.png"}))

    def test_filename_identified_logo_outranks_unidentified_svg(self):
        node = {"name": "Tscherning"}
        exact = {"kind": "header_logo", "width": 800, "height": 200,
                 "url": "https://tscherning.dk/assets/tscherning-logo.svg"}
        generic = {"kind": "header_logo", "width": 800, "height": 200,
                   "url": "https://tscherning.dk/assets/asset-1.svg"}
        self.assertGreater(collection.candidate_rank(exact, node),
                           collection.candidate_rank(generic, node))

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

    def test_lazy_nav_logo_and_manifest_are_discovered(self):
        parser = pilot.IconParser()
        parser.feed('<link rel="manifest" href="/site.webmanifest">'
                    '<nav><img class="site-brand" data-src="/img/mark.svg" '
                    'srcset="/img/mark-small.png 1x, /img/mark-large.png 2x"></nav>')
        self.assertEqual(parser.manifests, ["/site.webmanifest"])
        self.assertIn((5, "header_logo", "/img/mark.svg"), parser.candidates)
        self.assertIn((5, "header_logo", "/img/mark-large.png"), parser.candidates)

    def test_browser_gzip_pages_can_be_parsed_for_declared_icons(self):
        payload = gzip.compress(b'<html><head><link rel="icon" href="/brand.png"></head></html>')
        self.assertTrue(payload.startswith(b"\x1f\x8b"))
        parser = pilot.IconParser()
        parser.feed(gzip.decompress(payload).decode("utf-8"))
        self.assertIn((2, "declared_icon", "/brand.png"), parser.candidates)

    def test_logo_css_does_not_require_header_selector(self):
        urls = pilot.css_header_logo_candidates(
            '.site-brandmark{background-image:url("/img/brand.svg")}',
            'https://example/assets/app.css')
        self.assertEqual(urls, ['https://example/img/brand.svg'])

    def test_review_ui_requires_an_explicit_post(self):
        html = (ROOT.parent / "full_image_review.html").read_text(encoding="utf-8")
        self.assertIn("/api/decision", html)
        self.assertIn("theme=dark", html)
        self.assertIn("Vorschlag", html)
        self.assertIn('id="logoOpacity" type="range"', html)
        self.assertIn("--logo-opacity", html)
        self.assertIn("akteursnetz.logoOpacity", html)
        self.assertIn("review_settings?.logo_opacity_percent", html)
        self.assertIn("n.decision.provisional?'vorläufig':'bestätigt'", html)
        self.assertIn("logo_opacity_percent:Number($('logoOpacity').value)", html)
        self.assertIn("Nicht vorschlagen", html)
        self.assertIn(".candidate:not(.rejected)", html)
        self.assertNotIn("approveAll", html)

    def test_image_handoff_documents_provisional_boundary(self):
        handoff = (ROOT.parent / "HANDOFF_BILDER_FULL.md").read_text(encoding="utf-8")
        self.assertIn("| `logo` | 525 |", handoff)
        self.assertIn("| korrekte offizielle Logo-Ergebnisse | 476 |", handoff)
        self.assertIn("| begründete `none`-Ergebnisse | 65 |", handoff)
        self.assertIn("| Deckkraft | 50 % |", handoff)
        self.assertIn("keinen Neo4j-Write", handoff)
        self.assertIn("trockene `patch`-Lauf", handoff)
        self.assertIn("412 Graphzeilen und 350 dokumentierte Overlays", handoff)
        self.assertIn("vollständige `render`-Lauf ist bestanden", handoff)
        self.assertIn("Alle 16 Seiten wurden bei 600 dpi", handoff)
        self.assertIn("41/41 Tests bestanden", handoff)
        self.assertIn("schriftliche Erlaubnis erforderlich | 474", handoff)

    def test_completed_render_report_covers_all_variants(self):
        report = json.loads((ROOT / "render" / "render_report.json").read_text(encoding="utf-8"))
        self.assertEqual(report["result"], "PASS")
        self.assertEqual(report["logo_count"], 476)
        self.assertEqual(report["countries"], list(collection.COUNTRY_ORDER))
        self.assertEqual(set(report["renders"]), {
            "images_light", "images_dark", "control_light", "control_dark",
        })
        self.assertTrue(all(item["page_count"] == 4 for item in report["renders"].values()))
        pages = [page for item in report["renders"].values() for page in item["pages"]]
        self.assertEqual(len(pages), 16)
        self.assertTrue(all(len(page["sha256"]) == 64 for page in pages))
        for item in report["renders"].values():
            self.assertTrue((ROOT / item["pdf"]).is_file())
        for page in pages:
            path = ROOT / page["png"]
            self.assertTrue(path.is_file())
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), page["sha256"])

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

    def test_wide_tile_is_extended_not_cut(self):
        # A Van der Wal Sloopwerken analogue: a wide two-tone (red-over-yellow)
        # brand tile whose wordmark reaches almost to both edges. Cover-crop's
        # centred 256x256 window on an 800x200 source keeps only original
        # x=[300,500] -- both marks below sit entirely outside that window and
        # would previously vanish without a trace, not just get thinner.
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "wide-two-tone.png"
            image = Image.new("RGBA", (800, 200), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0, 0, 799, 99), fill=(210, 30, 30, 255))
            draw.rectangle((0, 100, 799, 199), fill=(230, 200, 40, 255))
            draw.rectangle((30, 70, 170, 130), fill=(10, 10, 10, 255))    # far-left mark
            draw.rectangle((630, 70, 770, 130), fill=(10, 10, 10, 255))  # far-right mark
            image.save(source)
            prepared, mode = pilot.prepare_node_canvas(source)

        self.assertEqual(mode, "circle_extend")
        self.assertEqual(prepared.size, (256, 256))
        array = np.asarray(prepared)
        dark = ((array[:, :, 0] < 60) & (array[:, :, 1] < 60)
                & (array[:, :, 2] < 60) & (array[:, :, 3] > 200))
        columns_with_dark = np.nonzero(dark.any(axis=0))[0]
        self.assertGreater(columns_with_dark.size, 0, "no surviving mark pixels at all")
        self.assertTrue((columns_with_dark < 85).any(), "left mark was cut")
        self.assertTrue((columns_with_dark > 170).any(), "right mark was cut")
        self.assertLessEqual(pilot.alpha_max_radius(prepared), pilot.FINAL_SIZE / 2 + 0.75)
        self.assertGreaterEqual(pilot.inner_disc_min_alpha(prepared), 250)

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
