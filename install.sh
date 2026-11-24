#!/usr/bin/env bash
# Manual install (if you don't use the plugin command). Copies skills and agents into ~/.claude.
# Existing skills/agents with the same name are skipped unless you pass --force.
set -euo pipefail
FORCE=0; [ "${1:-}" = "--force" ] && FORCE=1
SRC="$(cd "$(dirname "$0")" && pwd)"; DST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$DST/skills" "$DST/agents"
copy() { if [ -e "$2" ] && [ $FORCE -eq 0 ]; then echo "skip (exists): $2"; else rm -rf "$2"; cp -r "$1" "$2"; echo "installed: $2"; fi; }
for d in "$SRC"/skills/*/; do copy "${d%/}" "$DST/skills/$(basename "$d")"; done
for f in "$SRC"/agents/*.md; do copy "$f" "$DST/agents/$(basename "$f")"; done
echo "Done. Restart Claude Code, then type: /god-mode <your task>"
