import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "sync_plugin_manifests.py"


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def run_sync(plugin_root=None, *args, cwd=None):
    command = [sys.executable, str(SCRIPT)]
    if plugin_root is not None:
        command.append(str(plugin_root))
    command.extend(args)
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True)


class SyncPluginManifestsTest(unittest.TestCase):
    def make_plugin(self, claude_manifest, codex_manifest=None, gemini_manifest=None):
        temp_dir = tempfile.TemporaryDirectory()
        root = Path(temp_dir.name)
        write_json(root / ".claude-plugin" / "plugin.json", claude_manifest)
        (root / "skills").mkdir()
        if codex_manifest is not None:
            write_json(root / ".codex-plugin" / "plugin.json", codex_manifest)
        if gemini_manifest is not None:
            write_json(root / "gemini-extension.json", gemini_manifest)
        return temp_dir, root

    def test_write_generates_codex_and_gemini_from_claude(self):
        temp_dir, root = self.make_plugin(
            {
                "name": "example",
                "version": "1.2.3",
                "description": "Example plugin.",
                "author": {"name": "Jane Doe"},
                "homepage": "https://example.com",
                "repository": "https://github.com/example/plugin",
                "license": "MIT",
                "keywords": ["example", "plugin"],
            }
        )
        self.addCleanup(temp_dir.cleanup)

        result = run_sync(root, "--write")

        self.assertEqual(result.returncode, 0, result.stderr)
        codex = read_json(root / ".codex-plugin" / "plugin.json")
        self.assertEqual(codex["name"], "example")
        self.assertEqual(codex["version"], "1.2.3")
        self.assertEqual(codex["description"], "Example plugin.")
        self.assertEqual(codex["author"], {"name": "Jane Doe"})
        self.assertEqual(codex["homepage"], "https://example.com")
        self.assertEqual(codex["repository"], "https://github.com/example/plugin")
        self.assertEqual(codex["license"], "MIT")
        self.assertEqual(codex["keywords"], ["example", "plugin"])
        self.assertEqual(codex["skills"], "./skills/")

        gemini = read_json(root / "gemini-extension.json")
        self.assertEqual(
            gemini,
            {
                "name": "example",
                "version": "1.2.3",
                "description": "Example plugin.",
            },
        )

    def test_write_preserves_target_specific_fields_and_absent_shared_values(self):
        temp_dir, root = self.make_plugin(
            {
                "name": "example",
                "description": "New description.",
            },
            codex_manifest={
                "name": "old",
                "version": "9.9.9",
                "description": "Old description.",
                "interface": {"displayName": "Example"},
                "customCodexField": True,
            },
            gemini_manifest={
                "name": "old",
                "version": "8.8.8",
                "description": "Old description.",
                "settings": {"foo": "bar"},
                "contextFileName": "GEMINI.md",
                "keywords": ["preserved"],
            },
        )
        self.addCleanup(temp_dir.cleanup)

        result = run_sync(root, "--write")

        self.assertEqual(result.returncode, 0, result.stderr)
        codex = read_json(root / ".codex-plugin" / "plugin.json")
        self.assertEqual(codex["name"], "example")
        self.assertEqual(codex["version"], "9.9.9")
        self.assertEqual(codex["description"], "New description.")
        self.assertEqual(codex["interface"], {"displayName": "Example"})
        self.assertTrue(codex["customCodexField"])

        gemini = read_json(root / "gemini-extension.json")
        self.assertEqual(gemini["name"], "example")
        self.assertEqual(gemini["version"], "8.8.8")
        self.assertEqual(gemini["description"], "New description.")
        self.assertEqual(gemini["settings"], {"foo": "bar"})
        self.assertEqual(gemini["contextFileName"], "GEMINI.md")
        self.assertEqual(gemini["keywords"], ["preserved"])

    def test_mcp_servers_are_loaded_from_mcp_json_and_paths_are_converted(self):
        temp_dir, root = self.make_plugin(
            {
                "name": "example",
                "version": "1.0.0",
                "description": "Example plugin.",
            }
        )
        self.addCleanup(temp_dir.cleanup)
        write_json(
            root / ".mcp.json",
            {
                "mcpServers": {
                    "example": {
                        "command": "${CLAUDE_PLUGIN_ROOT}/bin/server",
                        "args": ["--root", "${CLAUDE_PLUGIN_ROOT}"],
                    }
                }
            },
        )

        result = run_sync(root, "--write")

        self.assertEqual(result.returncode, 0, result.stderr)
        gemini = read_json(root / "gemini-extension.json")
        self.assertEqual(
            gemini["mcpServers"],
            {
                "example": {
                    "command": "${extensionPath}/bin/server",
                    "args": ["--root", "${extensionPath}"],
                }
            },
        )

    def test_check_reports_stale_without_writing(self):
        temp_dir, root = self.make_plugin(
            {
                "name": "example",
                "version": "1.0.0",
                "description": "Example plugin.",
            }
        )
        self.addCleanup(temp_dir.cleanup)

        stale = run_sync(root, "--check")

        self.assertEqual(stale.returncode, 1)
        self.assertIn("stale", stale.stdout)
        self.assertFalse((root / ".codex-plugin" / "plugin.json").exists())
        self.assertFalse((root / "gemini-extension.json").exists())

        written = run_sync(root, "--write")
        self.assertEqual(written.returncode, 0, written.stderr)

        clean = run_sync(root, "--check")
        self.assertEqual(clean.returncode, 0, clean.stderr)
        self.assertIn("up to date", clean.stdout)

    def test_omitted_root_fails_with_candidate_roots(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = Path(temp_dir)
            plugin_root = workspace / "plugins" / "one"
            write_json(
                plugin_root / ".claude-plugin" / "plugin.json",
                {
                    "name": "one",
                    "description": "One plugin.",
                },
            )

            result = run_sync(cwd=workspace)

            self.assertEqual(result.returncode, 2)
            self.assertIn("plugins/one", result.stderr)

    def test_unsupported_claude_fields_are_reported(self):
        temp_dir, root = self.make_plugin(
            {
                "name": "example",
                "description": "Example plugin.",
                "dependencies": {"node": ">=20"},
                "userConfig": {"token": {"type": "string"}},
            }
        )
        self.addCleanup(temp_dir.cleanup)

        result = run_sync(root, "--write")

        self.assertEqual(result.returncode, 0)
        self.assertIn(
            "Unsupported Claude fields not converted: dependencies, userConfig",
            result.stderr,
        )


if __name__ == "__main__":
    unittest.main()
