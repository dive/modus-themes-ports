#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)

usage() {
  cat <<'USAGE'
Usage:
  scripts/install-modus.sh list
  scripts/install-modus.sh install <tool> [--theme "Name"] [--themes-dir <path>] [--config-dir <path>] [--link|--copy]
  scripts/install-modus.sh uninstall <tool> [--theme "Name"] [--themes-dir <path>]
  scripts/install-modus.sh print-config <tool> [--theme "Name"] [--config-dir <path>]

Tools:
  ghostty
USAGE
}

command_name=${1:-}
if [ -z "$command_name" ]; then
  usage
  exit 1
fi
shift

MODE=link
THEME_NAME=""
THEMES_DIR=""
CONFIG_DIR=""

parse_options() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --link)
        MODE=link
        ;;
      --copy)
        MODE=copy
        ;;
      --theme)
        shift
        THEME_NAME=${1:-}
        ;;
      --themes-dir)
        shift
        THEMES_DIR=${1:-}
        ;;
      --config-dir)
        shift
        CONFIG_DIR=${1:-}
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        break
        ;;
    esac
    shift
  done
}

list_tools() {
  echo "Tools:"
  echo "- ghostty"

  echo ""
  echo "Ghostty themes:"
  if [ -d "$REPO_ROOT/ports/ghostty/themes" ]; then
    found=0
    for f in "$REPO_ROOT/ports/ghostty/themes"/*.theme; do
      [ -e "$f" ] || continue
      found=1
      echo "- $(basename "$f" .theme)"
    done
    if [ $found -eq 0 ]; then
      echo "(none found, run scripts/render-ghostty-themes.sh)"
    fi
  else
    echo "(themes directory missing)"
  fi
}

resolve_ghostty_themes_dir() {
  if [ -n "$THEMES_DIR" ]; then
    echo "$THEMES_DIR"
    return
  fi
  base=${XDG_CONFIG_HOME:-"$HOME/.config"}
  echo "$base/ghostty/themes"
}

resolve_ghostty_config_dir() {
  if [ -n "$CONFIG_DIR" ]; then
    echo "$CONFIG_DIR"
    return
  fi
  if [ -d "$HOME/Library/Application Support/com.mitchellh.ghostty" ]; then
    echo "$HOME/Library/Application Support/com.mitchellh.ghostty"
    return
  fi
  base=${XDG_CONFIG_HOME:-"$HOME/.config"}
  echo "$base/ghostty"
}

find_theme_file() {
  theme_name=$1
  for f in "$REPO_ROOT/ports/ghostty/themes"/*.theme; do
    [ -e "$f" ] || continue
    if [ "$(basename "$f" .theme)" = "$theme_name" ]; then
      echo "$f"
      return
    fi
  done
}

install_ghostty() {
  parse_options "$@"

  src_dir="$REPO_ROOT/ports/ghostty/themes"
  if [ ! -d "$src_dir" ]; then
    echo "Error: theme source directory missing: $src_dir" >&2
    exit 1
  fi

  dest_dir=$(resolve_ghostty_themes_dir)
  mkdir -p "$dest_dir"

  if [ -n "$THEME_NAME" ]; then
    theme_file=$(find_theme_file "$THEME_NAME")
    if [ -z "$theme_file" ]; then
      echo "Error: theme not found: $THEME_NAME" >&2
      exit 1
    fi
    set -- "$theme_file"
  else
    set -- "$src_dir"/*.theme
  fi

  if [ ! -e "$1" ]; then
    echo "Error: no themes found. Run scripts/render-ghostty-themes.sh" >&2
    exit 1
  fi

  for f in "$@"; do
    dest="$dest_dir/$(basename "$f")"
    if [ -e "$dest" ]; then
      if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$f" ]; then
        echo "Already installed: $(basename "$f")"
        continue
      fi
      echo "Skipping existing file: $dest" >&2
      continue
    fi

    if [ "$MODE" = "copy" ]; then
      cp -p "$f" "$dest"
    else
      ln -s "$f" "$dest"
    fi

    echo "Installed: $(basename "$f")"
  done
}

uninstall_ghostty() {
  parse_options "$@"

  if ! command -v trash >/dev/null 2>&1; then
    echo "Error: 'trash' is required for uninstall." >&2
    exit 1
  fi

  dest_dir=$(resolve_ghostty_themes_dir)
  if [ ! -d "$dest_dir" ]; then
    echo "No themes directory found: $dest_dir"
    exit 0
  fi

  if [ -n "$THEME_NAME" ]; then
    set -- "$dest_dir/$THEME_NAME.theme"
  else
    set -- "$dest_dir"/*.theme
  fi

  if [ ! -e "$1" ]; then
    echo "No matching themes to uninstall."
    exit 0
  fi

  for f in "$@"; do
    [ -e "$f" ] || continue
    if [ -L "$f" ]; then
      link_target=$(readlink "$f")
      case "$link_target" in
        "$REPO_ROOT"/ports/ghostty/themes/*)
          trash "$f"
          echo "Removed: $(basename "$f")"
          ;;
        *)
          echo "Skipping non-modus symlink: $f" >&2
          ;;
      esac
    else
      echo "Skipping non-symlink file: $f" >&2
    fi
  done
}

print_config_ghostty() {
  parse_options "$@"

  if [ -z "$THEME_NAME" ]; then
    echo "Error: --theme is required for print-config" >&2
    exit 1
  fi

  config_dir=$(resolve_ghostty_config_dir)

  echo "theme = $THEME_NAME"
  echo "Config directory: $config_dir"
}

case "$command_name" in
  list)
    list_tools
    ;;
  install)
    tool=${1:-}
    shift || true
    case "$tool" in
      ghostty) install_ghostty "$@" ;;
      *) echo "Unknown tool: $tool" >&2; usage; exit 1 ;;
    esac
    ;;
  uninstall)
    tool=${1:-}
    shift || true
    case "$tool" in
      ghostty) uninstall_ghostty "$@" ;;
      *) echo "Unknown tool: $tool" >&2; usage; exit 1 ;;
    esac
    ;;
  print-config)
    tool=${1:-}
    shift || true
    case "$tool" in
      ghostty) print_config_ghostty "$@" ;;
      *) echo "Unknown tool: $tool" >&2; usage; exit 1 ;;
    esac
    ;;
  -h|--help)
    usage
    ;;
  *)
    echo "Unknown command: $command_name" >&2
    usage
    exit 1
    ;;
esac
