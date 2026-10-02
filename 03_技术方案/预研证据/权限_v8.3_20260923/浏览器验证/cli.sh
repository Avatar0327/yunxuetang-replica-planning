#!/usr/bin/env bash
set -euo pipefail
cd /Users/peng/Agent本地开发/云学堂权限预研
export PATH=/opt/homebrew/opt/node@24/bin:$PATH
spike_cli_candidate="$1"
spike_cli_label="$2"
shift 2
spike_cli_out="output/playwright/final-$spike_cli_candidate/$spike_cli_label.txt"
if [ -e "$spike_cli_out" ];then echo 'Refuse overwrite';exit 2;fi
node /Users/peng/.npm-cache/_npx/31e32ef8478fbf80/node_modules/@playwright/cli/playwright-cli.js "-s=yxt-permission-final-$spike_cli_candidate" "$@" > "$spike_cli_out" 2>&1
cat "$spike_cli_out"
