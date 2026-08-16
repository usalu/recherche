import json
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


class MissingInfoHuntTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rights = load("MISSING_RIGHTS_INFO_HUNT.json")
        cls.missing = load("MISSING_LOGO_INFO_HUNT.json")
        cls.curated = load("MISSING_LOGO_CURATED_LEADS.json")
        cls.identity = load("CURRENT_LOGO_IDENTITY_AUDIT.json")
        cls.completion = load("MISSING_INFO_COMPLETION.json")
        cls.final_logo = load("MISSING_LOGO_FINAL_RESEARCH_DISPOSITION.json")

    def test_frozen_scope_and_unique_keys(self):
        nodes = self.rights["nodes"]
        self.assertEqual(541, len(nodes))
        self.assertEqual(541, len({row["key"] for row in nodes}))
        self.assertEqual(Counter({"logo": 476, "none": 65}), Counter(row["result"] for row in nodes))
        self.assertEqual({"logo": 476, "none": 65}, self.identity["counts"])

    def test_selected_logos_are_not_marked_cleared(self):
        selected = [row for row in self.rights["nodes"] if row["result"] == "logo"]
        self.assertEqual(476, len(selected))
        self.assertTrue(all(row["publication_clearance"] == "blocked_no_permission_requested" for row in selected))
        self.assertEqual(
            Counter({"blocked_pending_permission": 474, "blocked_pending_legal_review": 1, "conditional": 1}),
            Counter(row["prior_print_clearance"] for row in selected),
        )

    def test_all_missing_logo_rows_are_present(self):
        rows = self.missing["nodes"]
        self.assertEqual(65, len(rows))
        self.assertEqual(65, len({row["key"] for row in rows}))
        self.assertEqual(12, self.missing["counts"]["manual_domain_findings"])
        self.assertEqual(
            Counter({"FR": 21, "CH": 12, "GB": 8, "DE": 7, "BE": 6, "DK": 4,
                     "NL": 3, "NO": 2, "SE": 1, "FI": 1}),
            Counter(row["cc"] for row in rows),
        )

    def test_curated_leads_remain_research_only(self):
        rows = self.curated["nodes"]
        self.assertEqual(19, len(rows))
        self.assertEqual(19, len({row["key"] for row in rows}))
        self.assertTrue(all(row["decision"] == "unreviewed_research_lead" for row in rows))
        self.assertTrue(all(row["publication_clearance"] == "not_cleared" for row in rows))
        self.assertEqual(5, sum(bool(row["minimum_128_ok"]) for row in rows))
        self.assertEqual(
            2,
            sum(row["research_confidence"] == "high" and bool(row["minimum_128_ok"]) for row in rows),
        )
        rights_leads = [row for row in rows if row["rights_research_status"] != "no_explicit_logo_permission_found"]
        self.assertEqual(5, len(rights_leads))
        self.assertTrue(all(row["rights_source_url"] for row in rights_leads))
        self.assertTrue(all(row["publication_clearance"] == "not_cleared" for row in rights_leads))

    def test_completion_has_no_open_research_state(self):
        rows = self.completion["nodes"]
        self.assertEqual(77, len(rows))
        self.assertEqual(77, len({(row["mode"], row["key"]) for row in rows}))
        self.assertEqual(Counter({"rights": 43, "logo": 34}), Counter(row["mode"] for row in rows))
        self.assertEqual({"records": 77, "terminal": 77, "open": 0,
                          "permission_requests_sent": 0, "publication_clearances_inferred": 0},
                         self.completion["completion"])
        self.assertTrue(all(row["research_complete"] for row in rows))
        self.assertFalse(any(row["resolution"].startswith("manual_") for row in rows))
        self.assertTrue(all(row["publication_clearance"] == "not_cleared" for row in rows))

    def test_rights_completion_has_route_or_terminal_no_route(self):
        rows = [row for row in self.completion["nodes"] if row["mode"] == "rights"]
        routed = [row for row in rows if row["emails"] or row["contact_pages"] or row["media_pages"]]
        no_route = [row for row in rows if row not in routed]
        self.assertEqual(41, len(routed))
        self.assertEqual(
            {"CH:U16": "no_current_first_party_contact_route_after_manual_search",
             "FR:U07": "no_verified_rights_route_domain_identity_mismatch"},
            {row["key"]: row["resolution"] for row in no_route},
        )
        self.assertTrue(all(row["evidence_sources"] for row in rows))

    def test_all_65_missing_logos_have_terminal_disposition(self):
        rows = self.final_logo["nodes"]
        self.assertEqual(65, len(rows))
        self.assertEqual(65, len({row["key"] for row in rows}))
        self.assertEqual({row["key"] for row in self.missing["nodes"]}, {row["key"] for row in rows})
        self.assertEqual(Counter({"none": 61, "candidate": 4}), Counter(row["disposition"] for row in rows))
        self.assertEqual({"terminal": 65, "open": 0, "production_changes": 0}, self.final_logo["completion"])
        self.assertTrue(all(row["research_complete"] for row in rows))
        self.assertTrue(all(not row["production_state_changed"] for row in rows))
        self.assertTrue(all(row["publication_clearance"] == "not_cleared" for row in rows))
        self.assertEqual(
            {"CH:U20", "DK:M02", "FI:U04", "FR:M53"},
            {row["key"] for row in rows if row["disposition"] == "candidate"},
        )
        self.assertTrue(all(row["candidate_url"] and row["technical_minimum_ok"]
                            for row in rows if row["disposition"] == "candidate"))

    def test_false_positive_raw_hits_resolve_to_none(self):
        expected = {"CH:M04", "CH:U15", "DE:U32", "DE:U41", "DK:M01", "FR:F01",
                    "FR:M42", "FR:M45", "FR:M58", "GB:M14", "GB:M24", "GB:U04"}
        rows = {row["key"]: row for row in self.final_logo["nodes"]}
        self.assertTrue(all(rows[key]["disposition"] == "none" for key in expected))
        self.assertTrue(all(rows[key]["resolution"] for key in expected))


if __name__ == "__main__":
    unittest.main()
