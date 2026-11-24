#!/usr/bin/env bash
# God Mode one-line installer (macOS / Linux / Git Bash):
#   curl -fsSL https://raw.githubusercontent.com/Eng-Kirolos-Ehab/god-mode/main/get.sh | bash
# Options (after `bash -s --`): --all | --categories gm-career,gm-video | --no-openwolf
# What it does: adds the God Mode marketplace to Claude Code, installs the core plugin, lets you pick
# categories (menu with description + size), installs them, then sets up OpenWolf in the current git project.
# It uses only the `claude` CLI, curl and npx. Read it first if you like: it's short.
set -euo pipefail

REPO="Eng-Kirolos-Ehab/god-mode"
SOURCE="${GM_SOURCE:-$REPO}"                                    # override for local testing
RAW="${GM_RAW:-https://raw.githubusercontent.com/$REPO/main}"   # override for local testing
ALL=0; PICK=""; OPENWOLF=1
while [ $# -gt 0 ]; do
  case "$1" in
    --all) ALL=1 ;;
    --categories) PICK="${2:-}"; shift ;;
    --categories=*) PICK="${1#*=}" ;;
    --no-openwolf) OPENWOLF=0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

command -v claude >/dev/null 2>&1 || { echo "Claude Code CLI not found. Install it first: https://claude.com/claude-code" >&2; exit 1; }

echo "==> Adding the God Mode marketplace"
claude plugin marketplace add "$SOURCE" >/dev/null 2>&1 || claude plugin marketplace update god-mode >/dev/null 2>&1 || true
echo "==> Installing the core (router, rules, setup)"
claude plugin install god-mode@god-mode

TSV="$(curl -fsSL "$RAW/catalog.generated.tsv")"
IFS=$'\t' read -r _ VERSION CORE_BYTES CORE_SIZE OW_VER <<< "$(printf '%s\n' "$TSV" | head -n 1)"
IDS=(); NAMES=(); SIZES=(); DESCS=(); EXTRAS=()
while IFS=$'\t' read -r id name size _bytes desc extras; do
  IDS+=("$id"); NAMES+=("$name"); SIZES+=("$size"); DESCS+=("$desc"); EXTRAS+=("${extras:-}")
done <<< "$(printf '%s\n' "$TSV" | tail -n +2)"
N=${#IDS[@]}

CHOSEN=()
if [ $ALL -eq 1 ]; then
  for ((i=0; i<N; i++)); do CHOSEN+=("${IDS[$i]}"); done
elif [ -n "$PICK" ]; then
  for want in ${PICK//,/ }; do
    ok=0; for id in "${IDS[@]}"; do [ "$id" = "$want" ] && ok=1; done
    [ $ok -eq 1 ] || { echo "Unknown category: $want (valid: ${IDS[*]})" >&2; exit 2; }
    CHOSEN+=("$want")
  done
else
  echo
  echo "God Mode $VERSION - pick the categories you want (core $CORE_SIZE is installed)"
  echo
  for ((i=0; i<N; i++)); do
    printf "  [%d] %s  (%s)\n      %s\n" $((i+1)) "${NAMES[$i]}" "${SIZES[$i]}" "${DESCS[$i]}"
    [ -n "${EXTRAS[$i]}" ] && printf "      + %s\n" "${EXTRAS[$i]}"
  done
  echo
  ANS=""
  if [ -r /dev/tty ]; then
    read -r -p "Numbers separated by spaces (e.g. 1 3 5), 'all', or Enter for none: " ANS < /dev/tty || ANS=""
  fi
  if [ "$ANS" = "all" ]; then
    CHOSEN=("${IDS[@]}")
  else
    for n in ${ANS//,/ }; do
      [[ "$n" =~ ^[0-9]+$ ]] && [ "$n" -ge 1 ] && [ "$n" -le "$N" ] || { echo "Out of range: $n" >&2; exit 2; }
      case " ${CHOSEN[*]:-} " in *" ${IDS[$((n-1))]} "*) ;; *) CHOSEN+=("${IDS[$((n-1))]}") ;; esac
    done
  fi
fi

for id in "${CHOSEN[@]:-}"; do
  [ -n "$id" ] || continue
  echo "==> Installing $id"
  claude plugin install "$id@god-mode"
done

CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
mkdir -p "$CFG/god-mode"
PREV=""
if [ -f "$CFG/god-mode/setup.json" ]; then PREV="$( (grep -o '"gm-[a-z0-9-]*"' "$CFG/god-mode/setup.json" || true) | tr -d '"' | tr -s '[:space:]' ' ')"; fi
LIST=""; SEEN=" "
for id in $PREV "${CHOSEN[@]:-}"; do
  [ -n "$id" ] || continue
  case "$SEEN" in *" $id "*) ;; *) SEEN="$SEEN$id "; LIST="$LIST\"$id\"," ;; esac
done
OWMODE=auto; [ $OPENWOLF -eq 0 ] && OWMODE=off
printf '{"version": "%s", "categories": [%s], "openwolf": "%s", "updated": "%s", "install": "get.sh"}\n' \
  "$VERSION" "${LIST%,}" "$OWMODE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$CFG/god-mode/setup.json"

if [ $OPENWOLF -eq 1 ]; then
  PROJ="$(pwd)"
  if ! command -v node >/dev/null 2>&1; then
    echo "OpenWolf skipped: it needs Node.js 18+."
  elif [ -d "$PROJ/.git" ] && [ "$PROJ" != "$HOME" ] && [ ! -d "$PROJ/.wolf" ]; then
    echo "==> Setting up OpenWolf $OW_VER in $PROJ"
    npx -y "openwolf@$OW_VER" init --agent claude
  else
    echo "OpenWolf: will be set up automatically the next time you open Claude Code in a git project."
  fi
fi

echo
echo "Done. Restart Claude Code. Type /god-mode <task>, or /god-mode:setup to change categories."
