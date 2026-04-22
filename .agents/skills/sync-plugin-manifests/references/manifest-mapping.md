# Manifest Mapping

Claude source: `.claude-plugin/plugin.json`.

Codex target: `.codex-plugin/plugin.json`.

- Copy shared fields when present: `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`.
- Preserve existing target-only fields, including `interface`.
- Set `skills` to `./skills/` when the plugin root has a `skills/` directory.

Gemini target: `gemini-extension.json`.

- Copy only `name`, `version`, and `description` from Claude when present.
- Preserve existing Gemini-only fields, including `settings`, `contextFileName`, `excludeTools`, `plan`, `themes`.
- Set `mcpServers` only when Claude has inline `mcpServers`, references an MCP JSON file, or the plugin root has `.mcp.json`.
- Convert `${CLAUDE_PLUGIN_ROOT}` and `$CLAUDE_PLUGIN_ROOT` string values to `${extensionPath}` inside Gemini `mcpServers`.

Unsupported Claude fields are reported and left unmapped: `dependencies`, `lspServers`, `userConfig`, and `experimental`.
