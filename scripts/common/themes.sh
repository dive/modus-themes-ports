#!/bin/sh
set -eu

list_themes() {
  src_dir=$1
  if [ ! -d "$src_dir" ]; then
    echo "(themes directory missing)"
    return
  fi

  found=0
  for f in "$src_dir"/*; do
    [ -f "$f" ] || continue
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    found=1
    echo "- $(basename "$f")"
  done

  if [ $found -eq 0 ]; then
    echo "(none found)"
  fi
}

find_theme_file() {
  src_dir=$1
  theme_name=$2
  for f in "$src_dir"/*; do
    [ -f "$f" ] || continue
    if [ "$(basename "$f")" = "$theme_name" ]; then
      echo "$f"
      return
    fi
  done
}

install_themes() {
  src_dir=$1
  dest_dir=$2
  mode=$3
  theme_name=${4:-}

  if [ ! -d "$src_dir" ]; then
    echo "Error: theme source directory missing: $src_dir" >&2
    exit 1
  fi

  mkdir -p "$dest_dir"

  if [ -n "$theme_name" ]; then
    theme_file=$(find_theme_file "$src_dir" "$theme_name")
    if [ -z "$theme_file" ]; then
      echo "Error: theme not found: $theme_name" >&2
      exit 1
    fi
    set -- "$theme_file"
  else
    set -- "$src_dir"/*
  fi

  if [ ! -e "$1" ]; then
    echo "Error: no themes found." >&2
    exit 1
  fi

  for f in "$@"; do
    [ -f "$f" ] || continue
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    dest="$dest_dir/$(basename "$f")"
    if [ -e "$dest" ]; then
      if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$f" ]; then
        echo "Already installed: $(basename "$f")"
        continue
      fi
      echo "Skipping existing file: $dest" >&2
      continue
    fi

    if [ "$mode" = "copy" ]; then
      cp -p "$f" "$dest"
    else
      ln -s "$f" "$dest"
    fi

    echo "Installed: $(basename "$f")"
  done
}

uninstall_themes() {
  dest_dir=$1
  src_dir=$2
  theme_name=${3:-}

  if ! command -v trash >/dev/null 2>&1; then
    echo "Error: 'trash' is required for uninstall." >&2
    exit 1
  fi

  if [ ! -d "$dest_dir" ]; then
    echo "No themes directory found: $dest_dir"
    exit 0
  fi

  if [ -n "$theme_name" ]; then
    set -- "$dest_dir/$theme_name"
  else
    set -- "$dest_dir"/*
  fi

  if [ ! -e "$1" ]; then
    echo "No matching themes to uninstall."
    exit 0
  fi

  for f in "$@"; do
    [ -f "$f" ] || continue
    [ "$(basename "$f")" = ".gitkeep" ] && continue
    if [ -L "$f" ]; then
      link_target=$(readlink "$f")
      case "$link_target" in
        "$src_dir"/*)
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
