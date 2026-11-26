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

# 3) Updated since the user last saw a note: show what's new once and offer the new categories.
NEW_VER=$(grep -o '"version": *"[^"]*"' "$ROOT/.claude-plugin/plugin.json" 2>/dev/null | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
OLD_VER=$(grep -o '"version": *"[^"]*"' "$MARK" 2>/dev/null | head -1 | sed 's/.*"\([^"]*\)"$/\1/')
NOTES="$ROOT/whats-new.txt"
if [ -n "$NEW_VER" ] && [ -f "$NOTES" ] && [ "$NEW_VER" != "$OLD_VER" ]; then
  NEWER=$(printf '%s\n%s\n' "${OLD_VER:-0}" "$NEW_VER" | sort -t. -k1,1n -k2,2n -k3,3n | tail -1)
  if [ "$NEWER" = "$NEW_VER" ]; then
    INSTALLED="$CFG/plugins/installed_plugins.json"
    ADD=""
    for id in $(sed -n 2p "$NOTES" | tr -d '\r'); do
      grep -q "\"$id@god-mode\"" "$INSTALLED" 2>/dev/null || ADD="$ADD $id"
    done
    echo "[God Mode] Updated from ${OLD_VER:-an older version} to $NEW_VER. What's new:"
    sed -n '3,$p' "$NOTES" | tr -d '\r'
    if [ -n "$ADD" ]; then
      echo "New categories the user doesn't have yet:$ADD. In your first reply, tell the user in 2-3 short lines (their language) what's new, then ask with AskUserQuestion (multiSelect, one option per new category with its description and size from the god-mode:setup catalog, plus 'Not now') which to add. Install each pick with: claude plugin install <id>@god-mode."
    else
      echo "In your first reply, tell the user in 2-3 short lines (their language) what's new."
    fi
    echo "Then set \"version\" to \"$NEW_VER\" in $MARK (keep its other keys), even if they pick nothing, so this note is shown only once. If the user's first message is urgent, answer it first."
  fi
fi

DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
if grep -q '"openwolf": *"auto"' "$MARK" 2>/dev/null \
   && [ -d "$DIR/.git" ] && [ ! -d "$DIR/.wolf" ] && [ "$DIR" != "$HOME" ]; then
  echo "[God Mode] OpenWolf is set to auto, but this project has no .wolf/ yet. In the project root, run: npx -y openwolf@$OW_VER init --agent claude (skip it if Node isn't installed). Then tell the user in one line that OpenWolf was added (.wolf/, hooks in .claude/settings.json, a header in CLAUDE.md; their own settings are kept)."
fi
exit 0
