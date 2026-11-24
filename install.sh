#!/usr/bin/env bash
# God Mode manual install (if you don't use the plugin command).
# Shows the categories with a description and size, lets you pick several, copies the core plus your picks
# into your Claude config folder, then sets up OpenWolf automatically in the current project.
#
#   ./install.sh                                   # interactive menu
#   ./install.sh --categories gm-career,gm-video   # no menu
#   ./install.sh --all                             # everything
#   add --force to overwrite skills/agents that already exist, --no-openwolf to skip OpenWolf
set -euo pipefail

FORCE=0; ALL=0; PICK=""; OPENWOLF=1
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE=1 ;;
    --all) ALL=1 ;;
    --categories) PICK="${2:-}"; shift ;;
    --categories=*) PICK="${1#*=}" ;;
    --no-openwolf) OPENWOLF=0 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
  shift
done

SRC="$(cd "$(dirname "$0")" && pwd)"
DST="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
TSV="$SRC/catalog.generated.tsv"

IFS=$'\t' read -r _ VERSION CORE_BYTES CORE_SIZE OW_VER < <(head -n 1 "$TSV")
IDS=(); NAMES=(); SIZES=(); BYTES=(); DESCS=(); EXTRAS=()
while IFS=$'\t' read -r id name size bytes desc extras; do
  IDS+=("$id"); NAMES+=("$name"); SIZES+=("$size"); BYTES+=("$bytes"); DESCS+=("$desc"); EXTRAS+=("${extras:-}")
done < <(tail -n +2 "$TSV")
N=${#IDS[@]}

copy() { if [ -e "$2" ] && [ $FORCE -eq 0 ]; then echo "  skip (exists): $2"; else rm -rf "$2"; cp -r "$1" "$2"; echo "  installed: $2"; fi; }
install_dir() {
  [ -d "$1/skills" ] && for d in "$1"/skills/*/; do copy "${d%/}" "$DST/skills/$(basename "$d")"; done
  [ -d "$1/agents" ] && for f in "$1"/agents/*.md; do copy "$f" "$DST/agents/$(basename "$f")"; done
  return 0
}

# ---- choose ----
CHOSEN=()
if [ $ALL -eq 1 ]; then
  for ((i=0; i<N; i++)); do CHOSEN+=("$i"); done
elif [ -n "$PICK" ]; then
  for want in ${PICK//,/ }; do
    found=0
    for ((i=0; i<N; i++)); do [ "${IDS[$i]}" = "$want" ] && { CHOSEN+=("$i"); found=1; }; done
    [ $found -eq 1 ] || { echo "Unknown category id: $want (valid: ${IDS[*]})" >&2; exit 2; }
  done
else
  echo
  echo "God Mode $VERSION - pick the categories you want (core $CORE_SIZE is always installed)"
  echo
  for ((i=0; i<N; i++)); do
    printf "  [%d] %s  (%s)\n      %s\n" $((i+1)) "${NAMES[$i]}" "${SIZES[$i]}" "${DESCS[$i]}"
    [ -n "${EXTRAS[$i]}" ] && printf "      + %s\n" "${EXTRAS[$i]}"
  done
  echo
  read -r -p "Type numbers separated by spaces or commas (e.g. 1 3 5), 'all', or press Enter for none: " ANS || ANS=""
  if [ "$ANS" = "all" ]; then
    for ((i=0; i<N; i++)); do CHOSEN+=("$i"); done
  else
    for n in ${ANS//,/ }; do
      [[ "$n" =~ ^[0-9]+$ ]] && [ "$n" -ge 1 ] && [ "$n" -le "$N" ] || { echo "Out of range: $n" >&2; exit 2; }
      case " ${CHOSEN[*]:-} " in *" $((n-1)) "*) ;; *) CHOSEN+=("$((n-1))") ;; esac
    done
  fi
fi

TOTAL=$CORE_BYTES; for i in "${CHOSEN[@]:-}"; do [ -n "$i" ] && TOTAL=$((TOTAL + BYTES[$i])); done
echo
echo "Installing core + ${#CHOSEN[@]} categories ($((TOTAL / 1024)) KB) into $DST"

# ---- install ----
mkdir -p "$DST/skills" "$DST/agents"
install_dir "$SRC/plugins/god-mode"   # core: skills/god-mode, skills/setup
for i in "${CHOSEN[@]:-}"; do [ -n "$i" ] || continue; echo "- ${NAMES[$i]}"; install_dir "$SRC/plugins/${IDS[$i]}"; done

# ---- remember the choice (also stops the first-run prompt) ----
mkdir -p "$DST/god-mode"
LIST=""; for i in "${CHOSEN[@]:-}"; do [ -n "$i" ] && LIST="$LIST\"${IDS[$i]}\","; done
OWMODE=auto; [ $OPENWOLF -eq 0 ] && OWMODE=off
printf '{"version": "%s", "categories": [%s], "openwolf": "%s", "updated": "%s", "install": "manual"}\n' \
  "$VERSION" "${LIST%,}" "$OWMODE" "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$DST/god-mode/setup.json"

# ---- OpenWolf (automatic) ----
if [ $OPENWOLF -eq 1 ]; then
  PROJ="$(pwd)"
  if ! command -v node >/dev/null 2>&1; then
    echo "OpenWolf skipped: it needs Node.js 18+. Install Node, then run: npx -y openwolf@$OW_VER init --agent claude"
  elif [ ! -d "$PROJ/.git" ] || [ "$PROJ" = "$HOME" ]; then
    echo "OpenWolf: run this from a project folder (one with .git) to set it up there: npx -y openwolf@$OW_VER init --agent claude"
  elif [ -d "$PROJ/.wolf" ]; then
    echo "OpenWolf: already set up in this project."
  else
    echo "Setting up OpenWolf (openwolf@$OW_VER) in $PROJ ..."
    npx -y "openwolf@$OW_VER" init --agent claude
  fi
fi

echo
echo "Done. Restart Claude Code, then type: /god-mode <your task>. Change categories later by re-running this script."
