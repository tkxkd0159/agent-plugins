#!/usr/bin/env python3
"""Interactively bump the version across plugin manifests for all three CLIs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"

MANIFEST_FILES = {
    "claude": ".claude-plugin/plugin.json",
    "codex": ".codex-plugin/plugin.json",
    "gemini": "gemini-extension.json",
}

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
# Surgical text-level edit preserves the file's existing formatting.
VERSION_LINE_RE = re.compile(r'("version"\s*:\s*)"[^"]*"')


def discover_plugins() -> list[tuple[str, dict[str, Path]]]:
    plugins: list[tuple[str, dict[str, Path]]] = []
    if not PLUGINS_DIR.is_dir():
        return plugins
    for plugin_dir in sorted(p for p in PLUGINS_DIR.iterdir() if p.is_dir()):
        manifests = {
            label: plugin_dir / rel
            for label, rel in MANIFEST_FILES.items()
            if (plugin_dir / rel).is_file()
        }
        if manifests:
            plugins.append((plugin_dir.name, manifests))
    return plugins


def read_version(path: Path) -> str:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh).get("version", "")


def format_plugin_line(idx: int, name: str, manifests: dict[str, Path]) -> str:
    versions = {label: read_version(path) for label, path in manifests.items()}
    labels = ",".join(sorted(manifests))
    unique = set(versions.values())
    if len(unique) == 1:
        return f"  {idx}. {name}  v{next(iter(unique))}  ({labels})"
    parts = ", ".join(f"{label}={ver or '-'}" for label, ver in sorted(versions.items()))
    return f"  {idx}. {name}  MISMATCH: {parts}"


def prompt_plugin(
    plugins: list[tuple[str, dict[str, Path]]],
) -> tuple[str, dict[str, Path]]:
    print("Plugins:")
    for idx, (name, manifests) in enumerate(plugins, 1):
        print(format_plugin_line(idx, name, manifests))
    while True:
        raw = input(f"\nSelect plugin [1-{len(plugins)}] (empty to cancel): ").strip()
        if not raw:
            print("Cancelled.")
            sys.exit(0)
        if raw.isdigit() and 1 <= int(raw) <= len(plugins):
            return plugins[int(raw) - 1]
        print("Invalid selection. Try again.")


def prompt_new_version(manifests: dict[str, Path]) -> str:
    versions = {label: read_version(path) for label, path in manifests.items()}
    unique = set(versions.values())
    display = (
        next(iter(unique))
        if len(unique) == 1
        else ", ".join(f"{label}={v}" for label, v in sorted(versions.items()))
    )
    while True:
        raw = input(f"New version (current: {display}, empty to cancel): ").strip()
        if not raw:
            print("Cancelled.")
            sys.exit(0)
        if SEMVER_RE.match(raw):
            return raw
        print("Version must be semver X.Y.Z (e.g. 0.3.0). Try again.")


def update_version(path: Path, new_version: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, n = VERSION_LINE_RE.subn(rf'\1"{new_version}"', text, count=1)
    if n == 0:
        raise RuntimeError(f"No version field found in {path}")
    path.write_text(new_text, encoding="utf-8")


def main() -> None:
    plugins = discover_plugins()
    if not plugins:
        print(f"No plugins found under {PLUGINS_DIR}", file=sys.stderr)
        sys.exit(1)

    name, manifests = prompt_plugin(plugins)
    new_version = prompt_new_version(manifests)

    print()
    for label, path in sorted(manifests.items()):
        update_version(path, new_version)
        print(f"  updated {label:7s} {path.relative_to(REPO_ROOT)}")
    print(f"\n{name} -> v{new_version}")


if __name__ == "__main__":
    main()
