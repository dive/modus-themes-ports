#!/bin/sh
set -eu

xdg_config_home() {
  printf '%s\n' "${XDG_CONFIG_HOME:-$HOME/.config}"
}

ghostty_config_dir() {
  printf '%s\n' "$(xdg_config_home)/ghostty"
}

ghostty_themes_dir() {
  printf '%s\n' "$(xdg_config_home)/ghostty/themes"
}

lazygit_config_dir() {
  printf '%s\n' "$(xdg_config_home)/lazygit"
}

lazygit_themes_dir() {
  printf '%s\n' "$(xdg_config_home)/lazygit/themes"
}
