#!/usr/bin/env bash
set -euo pipefail
cd /Users/peng/Agent本地开发/云学堂权限预研
export PATH=/opt/homebrew/opt/node@24/bin:$PATH
spike_browser_candidate="$1"
case "$spike_browser_candidate" in native|casbin) ;; *) exit 2;; esac
spike_browser_dir="output/playwright/final-$spike_browser_candidate"
mkdir -p "$spike_browser_dir"
if lsof -nP -iTCP:4311 -iTCP:4312 -sTCP:LISTEN >/dev/null 2>&1;then exit 2;fi
git rev-parse HEAD > "$spike_browser_dir/source-commit.txt"
git rev-parse HEAD:src HEAD:sql HEAD:web > "$spike_browser_dir/source-tree-hashes.txt"
PORT=4311 INSTANCE_ID=A CANDIDATE="$spike_browser_candidate" CACHE_MODE=hot node dist/src/bootstrap.js > "$spike_browser_dir/api-a.log" 2>&1 &
spike_browser_a=$!
PORT=4312 INSTANCE_ID=B CANDIDATE="$spike_browser_candidate" CACHE_MODE=hot node dist/src/bootstrap.js > "$spike_browser_dir/api-b.log" 2>&1 &
spike_browser_b=$!
printf '%s\n%s\n' "$spike_browser_a" "$spike_browser_b" > "$spike_browser_dir/pids.txt"
trap 'kill "$spike_browser_a" "$spike_browser_b" 2>/dev/null || true' EXIT INT TERM
printf 'BROWSER_APIS %s %s %s\n' "$spike_browser_candidate" "$spike_browser_a" "$spike_browser_b"
wait
