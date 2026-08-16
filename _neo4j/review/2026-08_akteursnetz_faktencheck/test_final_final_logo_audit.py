import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"
AUDIT = DATA / "FINAL_FINAL_LOGO_AUDIT.json"


class FinalFinalLogoAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(AUDIT.read_text(encoding="utf-8"))
        cls.rows = cls.audit["nodes"]
        cls.by_key = {row["key"]: row for row in cls.rows}

    def test_all_selected_logos_are_present_once(self):
        self.assertEqual(476, len(self.rows))
        self.assertEqual(476, len(self.by_key))
        self.assertTrue(all(row["result"] == "logo" for row in self.rows))

    def test_statuses_are_closed_and_counted(self):
        allowed = {"confirmed_exact", "manual_check", "manual_check_high"}
        self.assertTrue(all(row["audit_status"] in allowed for row in self.rows))
        self.assertEqual(476, sum(self.audit["counts"].values()))
        self.assertEqual(0, self.audit["technical_failures"])

    def test_manual_rows_have_reasons_and_confirmed_rows_do_not(self):
        for row in self.rows:
            if row["audit_status"] == "confirmed_exact":
                self.assertEqual([], row["manual_reasons"], row["key"])
            else:
                self.assertTrue(row["manual_reasons"], row["key"])

    def test_stale_sources_are_high_priority(self):
        high = {row["key"] for row in self.rows if row["audit_status"] == "manual_check_high"}
        self.assertEqual({"FR:M44", "DE:I05"}, high)

    def test_all_recent_additions_are_explicitly_tracked(self):
        recent = {row["key"] for row in self.rows if row["recent_last_three_sessions"]}
        self.assertEqual(20, len(recent))

    def test_every_duplicate_assignment_is_flagged(self):
        for group in self.audit["duplicate_asset_groups"]:
            self.assertGreater(len(group), 1)
            for key in group:
                codes = {reason["code"] for reason in self.by_key[key]["manual_reasons"]}
                self.assertIn("shared_asset_hash", codes, key)

    def test_outputs_and_assets_exist(self):
        for name in (
            "FINAL_FINAL_LOGO_AUDIT.json",
            "FINAL_FINAL_LOGO_AUDIT.csv",
            "FINAL_FINAL_LOGO_AUDIT.md",
            "FINAL_FINAL_LOGO_AUDIT.html",
        ):
            self.assertTrue((DATA / name).is_file(), name)
        for row in self.rows:
            self.assertTrue((DATA / row["asset_path"]).is_file(), row["key"])
            if row.get("dark_asset_path"):
                self.assertTrue((DATA / row["dark_asset_path"]).is_file(), row["key"])

    def test_no_neo4j_write_is_claimed(self):
        self.assertFalse(self.audit["neo4j_write"])


if __name__ == "__main__":
    unittest.main()
