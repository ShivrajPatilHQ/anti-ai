#!/usr/bin/env bash
# Package the skill as anti-ai.skill for upload through the Claude settings UI.
# Output goes to dist/anti-ai.skill. Requires zip; nothing else.
set -euo pipefail

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
build="$(mktemp -d)"
out="$root/dist/anti-ai.skill"
trap 'rm -rf "$build"' EXIT

# Only what the skill needs at runtime. SKILL.md points at references/ and
# scripts/scan.py; tests and examples are for the repo, not the bundle.
mkdir -p "$build/anti-ai/scripts" "$build/anti-ai/references"
cp "$root/SKILL.md" "$root/LICENSE" "$build/anti-ai/"
cp "$root/scripts/scan.py" "$build/anti-ai/scripts/"
cp "$root/references/"*.md "$build/anti-ai/references/"

mkdir -p "$root/dist"
rm -f "$out"
(cd "$build" && zip -qr "$out" anti-ai -x '*.DS_Store' '*__pycache__*')

echo "built $out ($(du -h "$out" | awk '{print $1}'))"
unzip -Z1 "$out" | sed 's/^/  /'
