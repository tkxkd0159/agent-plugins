---
name: sync-plugin-manifests
description: Generate or check Codex CLI .codex-plugin/plugin.json and Gemini CLI gemini-extension.json manifests from a Claude Code .claude-plugin/plugin.json source manifest. Use when maintaining one plugin across Claude Code, Codex CLI, and Gemini CLI, syncing plugin metadata, preserving platform-specific manifest fields, or validating cross-platform plugin manifests before release.
argument-hint: "[PLUGIN_ROOT_PATH]"
---

# Sync Plugin Manifests

## Overview

Use the bundled script to derive Codex and Gemini manifests from the Claude plugin manifest while preserving target-platform fields that Claude does not know about.

## Workflow

1. Start at the plugin root, or pass the plugin root explicitly.
2. Run a dry preview first:

   ```bash
   python3 .agents/skills/sync-plugin-manifests/scripts/sync_plugin_manifests.py <plugin-root>
   ```

3. Write the generated manifests when the preview is correct:

   ```bash
   python3 .agents/skills/sync-plugin-manifests/scripts/sync_plugin_manifests.py <plugin-root> --write
   ```

4. Use check mode in verification or CI:

   ```bash
   python3 .agents/skills/sync-plugin-manifests/scripts/sync_plugin_manifests.py <plugin-root> --check
   ```

## Behavior

- Treat `.claude-plugin/plugin.json` as the source of shared plugin metadata.
- Preserve existing Codex-only and Gemini-only fields in target manifests.
- Generate `.codex-plugin/plugin.json` and `gemini-extension.json` with stable 2-space JSON.
- Convert `${CLAUDE_PLUGIN_ROOT}` to `${extensionPath}` inside Gemini `mcpServers`.
- Report unsupported Claude fields instead of inventing target-platform equivalents.

Read `references/manifest-mapping.md` when changing mappings or reviewing platform-specific behavior.
