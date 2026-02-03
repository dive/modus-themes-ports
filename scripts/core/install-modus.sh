#!/bin/sh
set -eu

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
REPO_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)

. "$REPO_ROOT/scripts/common/paths.sh"
. "$REPO_ROOT/scripts/common/themes.sh"

usage() {
  cat <<'USAGE'
Usage:
  scripts/core/install-modus.sh list
  scripts/core/install-modus.sh install <tool> [--theme "Name"] [--themes-dir <path>] [--config-dir <path>] [--link|--copy]
  scripts/core/install-modus.sh uninstall <tool> [--theme "Name"] [--themes-dir <path>]
  scripts/core/install-modus.sh print-config <tool> [--theme "Name"] [--config-dir <path>]

Tools:
  ghostty
  lazygit
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

resolve_themes_dir() {
  default_dir=$1
  if [ -n "$THEMES_DIR" ]; then
    echo "$THEMES_DIR"
  else
    echo "$default_dir"
  fi
}

resolve_config_dir() {
  default_dir=$1
  if [ -n "$CONFIG_DIR" ]; then
    echo "$CONFIG_DIR"
  else
    echo "$default_dir"
  fi
}

list_tools() {
  echo "Tools:"
  echo "- ghostty"
  echo "- lazygit"

  echo ""
  echo "Ghostty themes:"
  list_themes "$REPO_ROOT/ports/ghostty/themes"

  echo ""
  echo "Lazygit themes:"
  list_themes "$REPO_ROOT/ports/lazygit/themes"
}

install_ghostty() {
  parse_options "$@"
  src_dir="$REPO_ROOT/ports/ghostty/themes"
  dest_dir=$(resolve_themes_dir "$(ghostty_themes_dir)")
  install_themes "$src_dir" "$dest_dir" "$MODE" "$THEME_NAME"
}

install_lazygit() {
  parse_options "$@"
  src_dir="$REPO_ROOT/ports/lazygit/themes"
  dest_dir=$(resolve_themes_dir "$(lazygit_themes_dir)")
  install_themes "$src_dir" "$dest_dir" "$MODE" "$THEME_NAME"
}

uninstall_ghostty() {
  parse_options "$@"
  src_dir="$REPO_ROOT/ports/ghostty/themes"
  dest_dir=$(resolve_themes_dir "$(ghostty_themes_dir)")
  uninstall_themes "$dest_dir" "$src_dir" "$THEME_NAME"
}

uninstall_lazygit() {
  parse_options "$@"
  src_dir="$REPO_ROOT/ports/lazygit/themes"
  dest_dir=$(resolve_themes_dir "$(lazygit_themes_dir)")
  uninstall_themes "$dest_dir" "$src_dir" "$THEME_NAME"
}

print_config_ghostty() {
  parse_options "$@"

  if [ -z "$THEME_NAME" ]; then
    echo "Error: --theme is required for print-config" >&2
    exit 1
  fi

  config_dir=$(resolve_config_dir "$(ghostty_config_dir)")
  echo "theme = $THEME_NAME"
  echo "Config directory: $config_dir"
}

print_config_lazygit() {
  parse_options "$@"

  if [ -z "$THEME_NAME" ]; then
    echo "Error: --theme is required for print-config" >&2
    exit 1
  fi

  src_dir="$REPO_ROOT/ports/lazygit/themes"
  theme_file=$(find_theme_file "$src_dir" "$THEME_NAME")
  if [ -z "$theme_file" ]; then
    echo "Error: theme not found: $THEME_NAME" >&2
    exit 1
  fi

  config_dir=$(resolve_config_dir "$(lazygit_config_dir)")
  echo "# Paste into $config_dir/config.yml"
  cat "$theme_file"
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
      lazygit) install_lazygit "$@" ;;
      *) echo "Unknown tool: $tool" >&2; usage; exit 1 ;;
    esac
    ;;
  uninstall)
    tool=${1:-}
    shift || true
    case "$tool" in
      ghostty) uninstall_ghostty "$@" ;;
      lazygit) uninstall_lazygit "$@" ;;
      *) echo "Unknown tool: $tool" >&2; usage; exit 1 ;;
    esac
    ;;
  print-config)
    tool=${1:-}
    shift || true
    case "$tool" in
      ghostty) print_config_ghostty "$@" ;;
      lazygit) print_config_lazygit "$@" ;;
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
