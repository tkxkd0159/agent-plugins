from __future__ import annotations

import json
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
PLUGIN_ROOT = REPO_ROOT / "plugins" / "daily-stock-executive-summary"
PLUGIN_MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
SKILL_PATH = (
    PLUGIN_ROOT
    / "skills"
    / "daily-stock-executive-summary"
    / "SKILL.md"
)
SKILL_UI_PATH = (
    PLUGIN_ROOT
    / "skills"
    / "daily-stock-executive-summary"
    / "agents"
    / "openai.yaml"
)


class DailyStockPluginTest(unittest.TestCase):
    def test_marketplace_entry_matches_general_purpose_catalog(self) -> None:
        payload = json.loads(MARKETPLACE_PATH.read_text())

        self.assertEqual(payload["name"], "utility-hub")
        self.assertEqual(payload["interface"]["displayName"], "Utility Hub")

        plugin_entry = next(
            entry
            for entry in payload["plugins"]
            if entry["name"] == "daily-stock-executive-summary"
        )
        self.assertEqual(plugin_entry["source"]["source"], "local")
        self.assertEqual(
            plugin_entry["source"]["path"], "./plugins/daily-stock-executive-summary"
        )
        self.assertEqual(plugin_entry["policy"]["installation"], "AVAILABLE")
        self.assertEqual(plugin_entry["policy"]["authentication"], "ON_INSTALL")
        self.assertEqual(plugin_entry["category"], "Finance")

    def test_plugin_manifest_points_to_skill_bundle(self) -> None:
        payload = json.loads(PLUGIN_MANIFEST_PATH.read_text())

        self.assertEqual(payload["name"], "daily-stock-executive-summary")
        self.assertEqual(payload["skills"], "./skills/")
        self.assertNotIn("mcpServers", payload)
        self.assertNotIn("apps", payload)

        interface = payload["interface"]
        self.assertEqual(interface["displayName"], "Daily Stock Executive Summary")
        self.assertEqual(interface["category"], "Finance")
        self.assertIn("Read", interface["capabilities"])
        self.assertIn("Analysis", interface["capabilities"])
        self.assertLessEqual(len(interface["defaultPrompt"]), 3)

    def test_skill_instructions_cover_required_market_sections(self) -> None:
        content = SKILL_PATH.read_text()

        required_phrases = [
            "most recent completed U.S. trading session",
            "institutional flow",
            "raw material",
            "3-month",
            "2-year",
            "10-year",
            "bullish sectors",
            "bearish sectors",
            "notable stocks",
            "rebalance",
            "pyramid",
            "average down",
            "facts",
            "inference",
            "absolute dates",
        ]

        for phrase in required_phrases:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, content)

    def test_skill_ui_metadata_disables_implicit_invocation(self) -> None:
        content = SKILL_UI_PATH.read_text()

        self.assertIn('display_name: "Daily Stock Executive Summary"', content)
        self.assertIn("allow_implicit_invocation: false", content)
        self.assertIn('default_prompt: "Generate today\'s stock market executive summary."', content)


if __name__ == "__main__":
    unittest.main()
