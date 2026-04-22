#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CLAUDE_MANIFEST = Path(".claude-plugin/plugin.json")
CODEX_MANIFEST = Path(".codex-plugin/plugin.json")
GEMINI_MANIFEST = Path("gemini-extension.json")

CODEX_SHARED_FIELDS = (
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
)
GEMINI_SHARED_FIELDS = ("name", "version", "description")
UNSUPPORTED_CLAUDE_FIELDS = (
    "dependencies",
    "lspServers",
    "userConfig",
    "experimental",
)


class ManifestError(Exception):
    pass


@dataclass(frozen=True)
class ManifestChange:
    path: Path
    existing_text: str
    desired_text: str

    @property
    def changed(self) -> bool:
        return self.existing_text != self.desired_text


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise ManifestError(f"Missing JSON file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, dict):
        raise ManifestError(f"Expected JSON object in {path}")
    return data


def read_target(path: Path) -> tuple[dict[str, Any], str]:
    if not path.exists():
        return {}, ""
    return load_json_object(path), path.read_text(encoding="utf-8")


def serialize(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def apply_shared_fields(
    target: dict[str, Any], source: dict[str, Any], fields: tuple[str, ...]
) -> dict[str, Any]:
    merged = dict(target)
    for field in fields:
        if field in source:
            merged[field] = source[field]
    return merged


def convert_claude_paths(value: Any) -> Any:
    if isinstance(value, str):
        return value.replace("${CLAUDE_PLUGIN_ROOT}", "${extensionPath}").replace(
            "$CLAUDE_PLUGIN_ROOT", "${extensionPath}"
        )
    if isinstance(value, list):
        return [convert_claude_paths(item) for item in value]
    if isinstance(value, dict):
        return {key: convert_claude_paths(item) for key, item in value.items()}
    return value


def normalize_mcp_servers(payload: Any) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    nested = payload.get("mcpServers")
    if isinstance(nested, dict):
        return nested
    return payload


def load_mcp_servers_from_path(plugin_root: Path, raw_path: str) -> dict[str, Any] | None:
    path = (plugin_root / raw_path).resolve()
    if not path.exists():
        raise ManifestError(f"Referenced MCP file does not exist: {path}")
    return normalize_mcp_servers(load_json_object(path))


def find_claude_mcp_servers(
    plugin_root: Path, claude_manifest: dict[str, Any]
) -> dict[str, Any] | None:
    raw = claude_manifest.get("mcpServers")
    if isinstance(raw, dict):
        return convert_claude_paths(normalize_mcp_servers(raw))
    if isinstance(raw, str):
        servers = load_mcp_servers_from_path(plugin_root, raw)
        return convert_claude_paths(servers) if servers is not None else None
    if isinstance(raw, list):
        merged: dict[str, Any] = {}
        for item in raw:
            if not isinstance(item, str):
                continue
            servers = load_mcp_servers_from_path(plugin_root, item)
            if servers is not None:
                merged.update(servers)
        return convert_claude_paths(merged) if merged else None

    default_mcp = plugin_root / ".mcp.json"
    if default_mcp.exists():
        servers = normalize_mcp_servers(load_json_object(default_mcp))
        return convert_claude_paths(servers) if servers is not None else None

    return None


def build_codex_manifest(
    plugin_root: Path, claude_manifest: dict[str, Any], existing: dict[str, Any]
) -> dict[str, Any]:
    codex = apply_shared_fields(existing, claude_manifest, CODEX_SHARED_FIELDS)
    if (plugin_root / "skills").is_dir():
        codex["skills"] = "./skills/"
    return codex


def build_gemini_manifest(
    plugin_root: Path, claude_manifest: dict[str, Any], existing: dict[str, Any]
) -> dict[str, Any]:
    gemini = apply_shared_fields(existing, claude_manifest, GEMINI_SHARED_FIELDS)
    mcp_servers = find_claude_mcp_servers(plugin_root, claude_manifest)
    if mcp_servers is not None:
        gemini["mcpServers"] = mcp_servers
    return gemini


def find_candidate_roots(cwd: Path) -> list[Path]:
    candidates: list[Path] = []
    for manifest in cwd.rglob(str(CLAUDE_MANIFEST)):
        if any(part in {".git", ".worktrees"} for part in manifest.parts):
            continue
        candidates.append(manifest.parent.parent)
    return sorted(candidates)


def resolve_plugin_root(raw_root: str | None) -> Path:
    if raw_root is not None:
        root = Path(raw_root).expanduser().resolve()
        if not (root / CLAUDE_MANIFEST).is_file():
            raise ManifestError(f"Missing Claude manifest: {root / CLAUDE_MANIFEST}")
        return root

    cwd = Path.cwd().resolve()
    if (cwd / CLAUDE_MANIFEST).is_file():
        return cwd

    candidates = find_candidate_roots(cwd)
    message = "Missing Claude manifest in current directory."
    if candidates:
        message += "\nCandidate plugin roots:"
        for candidate in candidates:
            message += f"\n  {candidate.relative_to(cwd)}"
    raise ManifestError(message)


def build_changes(plugin_root: Path) -> tuple[list[ManifestChange], list[str]]:
    claude_manifest = load_json_object(plugin_root / CLAUDE_MANIFEST)

    codex_path = plugin_root / CODEX_MANIFEST
    codex_existing, codex_text = read_target(codex_path)
    codex_desired = build_codex_manifest(plugin_root, claude_manifest, codex_existing)

    gemini_path = plugin_root / GEMINI_MANIFEST
    gemini_existing, gemini_text = read_target(gemini_path)
    gemini_desired = build_gemini_manifest(plugin_root, claude_manifest, gemini_existing)

    unsupported = [
        field for field in UNSUPPORTED_CLAUDE_FIELDS if field in claude_manifest
    ]
    warnings = []
    if unsupported:
        warnings.append(
            "Unsupported Claude fields not converted: " + ", ".join(unsupported)
        )

    return (
        [
            ManifestChange(codex_path, codex_text, serialize(codex_desired)),
            ManifestChange(gemini_path, gemini_text, serialize(gemini_desired)),
        ],
        warnings,
    )


def diff_change(plugin_root: Path, change: ManifestChange) -> str:
    relative = change.path.relative_to(plugin_root)
    return "".join(
        difflib.unified_diff(
            change.existing_text.splitlines(keepends=True),
            change.desired_text.splitlines(keepends=True),
            fromfile=f"a/{relative}",
            tofile=f"b/{relative}",
        )
    )


def print_warnings(warnings: list[str]) -> None:
    for warning in warnings:
        print(warning, file=sys.stderr)


def run(args: argparse.Namespace) -> int:
    plugin_root = resolve_plugin_root(args.plugin_root)
    changes, warnings = build_changes(plugin_root)
    print_warnings(warnings)

    changed = [change for change in changes if change.changed]
    if args.check:
        if not changed:
            print("Generated manifests are up to date.")
            return 0
        for change in changed:
            print(f"{change.path.relative_to(plugin_root)} is stale.")
            print(diff_change(plugin_root, change), end="")
        return 1

    if args.write:
        for change in changes:
            relative = change.path.relative_to(plugin_root)
            if change.changed:
                change.path.parent.mkdir(parents=True, exist_ok=True)
                change.path.write_text(change.desired_text, encoding="utf-8")
                print(f"Updated {relative}")
            else:
                print(f"Already up to date {relative}")
        return 0

    if not changed:
        print("Generated manifests are up to date.")
        return 0

    for change in changed:
        print(diff_change(plugin_root, change), end="")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Codex plugin.json and Gemini gemini-extension.json "
            "from Claude .claude-plugin/plugin.json."
        )
    )
    parser.add_argument(
        "plugin_root",
        nargs="?",
        help="Plugin root containing .claude-plugin/plugin.json. Defaults to cwd.",
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Write generated manifests.")
    mode.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero when generated manifests are missing or stale.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        return run(args)
    except ManifestError as exc:
        print(str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
