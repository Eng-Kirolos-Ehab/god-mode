#!/bin/sh
# God Mode session hook. Prints text for Claude only: it installs, downloads and changes nothing itself.
# 1) First run (no setup.json): tell Claude to run the category picker.
# 2) OpenWolf set to "auto" and this git project has no .wolf/: tell Claude to initialize it.
CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
MARK="$CFG/god-mode/setup.json"
ROOT="${CLAUDE_PLUGIN_ROOT:-$(dirname "$0")/..}"
OW_VER=$(cat "$ROOT/openwolf.version" 2>/dev/null | tr -d ' \r\n')
[ -n "$OW_VER" ] || OW_VER="2.5.3"

if [ ! -f "$MARK" ]; then
  echo "[God Mode] First run: setup is pending. Before anything else in your first reply, invoke the skill god-mode:setup. It asks the user which God Mode categories to install (multi-select, with a description and size for each), installs them, and sets up OpenWolf. If the user's first message is urgent, answer it briefly first, then run setup."
  exit 0
fi

DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
if grep -q '"openwolf": *"auto"' "$MARK" 2>/dev/null \
   && [ -d "$DIR/.git" ] && [ ! -d "$DIR/.wolf" ] && [ "$DIR" != "$HOME" ]; then
  echo "[God Mode] OpenWolf is set to auto, but this project has no .wolf/ yet. In the project root, run: npx -y openwolf@$OW_VER init --agent claude (skip it if Node isn't installed). Then tell the user in one line that OpenWolf was added (.wolf/, hooks in .claude/settings.json, a header in CLAUDE.md; their own settings are kept)."
fi
exit 0
