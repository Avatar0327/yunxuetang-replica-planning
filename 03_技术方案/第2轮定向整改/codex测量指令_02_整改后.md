# 第 2 轮整改后测量指令（用户在"终端"执行，codex 打包证据）

> 编写：Claude 技术会话，2026-10-03。
> 依据：基线测量的执行经验。codex 的后台进程会被结束，所以测量改由用户在 macOS"终端"App 中执行；codex 只负责打包和推送证据。
> 本次测量的提交：`91683df702182724dbe9025afa5726606ba3d340`（原型仓库 `Avatar0327/yunxuetang-permission-spike`，分支 `round2/remediation`）。

与基线完全相同的条件：同一台机器、同一个 Colima 实例、复用同一套 `yxt-pg` 和 `yxt-redis`、50 客户端 × 600 秒、四场景等比轮转、热窗和冷窗各一个，外加同一套 Native 选定回归。门槛、超时、资源上限、负载和脚本都不改。

## 第 1 步：用户在"终端"中准备代码（约 2 分钟）

```bash
cd "/Users/peng/Documents/ChatGPT/【新版】云学堂LXP复刻项目/yunxuetang-permission-spike"
export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
git status --porcelain
git fetch origin round2/remediation
git checkout --detach 91683df702182724dbe9025afa5726606ba3d340
npm ci
git status --porcelain
git rev-parse HEAD
```

- 两次 `git status --porcelain` 都必须没有输出。
- 最后一行必须是 `91683df702182724dbe9025afa5726606ba3d340`。
- 任何一项不满足就停下，把输出发给 Claude。

## 第 2 步：写入并运行测量脚本（约 45 分钟）

先粘贴下面整段，回车。这一步只写出脚本文件，不开始测量：

```bash
cd "/Users/peng/Documents/ChatGPT/【新版】云学堂LXP复刻项目/yunxuetang-permission-spike" && mkdir -p evidence/raw/round2-remediation-91683df && cat > evidence/raw/round2-remediation-91683df/run-remediation.sh <<'EOF'
#!/usr/bin/env bash
set -u
cd "/Users/peng/Documents/ChatGPT/【新版】云学堂LXP复刻项目/yunxuetang-permission-spike"
export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
E=evidence/raw/round2-remediation-91683df
[ "$(git rev-parse HEAD)" = 91683df702182724dbe9025afa5726606ba3d340 ] || { echo "停止：HEAD 不是 91683df702182724dbe9025afa5726606ba3d340"; exit 2; }
[ -z "$(git status --porcelain)" ] || { echo "停止：工作区不干净"; exit 2; }
docker --context colima-yxt-permission exec yxt-pg pg_isready -U spike -d permission_spike > "$E/pg-ready.txt" 2>&1 || { echo "停止：PG 未就绪，见 $E/pg-ready.txt"; exit 2; }
docker --context colima-yxt-permission exec yxt-pg psql -U spike -d permission_spike -X -A -t -c 'SHOW track_commit_timestamp' > "$E/track-commit-timestamp-check.txt" 2>&1
for w in hot cold; do
  [ ! -e "$E/$w" ] || { echo "停止：$E/$w 已存在"; exit 2; }
  echo "开始 $w 窗口（约 13 分钟）"; date -u +%FT%TZ > "$E/$w-start-utc.txt"
  bash tools/run-native-window.sh "$E/$w" candidate "$w" > "$E/$w-run.out" 2>&1; echo $? > "$E/$w-script-exit.txt"
  date -u +%FT%TZ > "$E/$w-end-utc.txt"
  if [ -f "$E/$w/incomplete.txt" ] || [ ! -f "$E/$w/runner-exit.txt" ]; then echo "停止：$w 窗口未完整执行，见 $E/$w-run.out"; exit 3; fi
  echo "$w 窗口结束，脚本退出码 $(cat "$E/$w-script-exit.txt")（0 为门禁通过，1 为门禁未通过）"
done
echo "开始回归"; date -u +%FT%TZ > "$E/regression-start-utc.txt"
bash tools/run-native-regressions.sh "$E/regression" > "$E/regression-run.out" 2>&1; echo $? > "$E/regression-script-exit.txt"
date -u +%FT%TZ > "$E/regression-end-utc.txt"
python3 tools/summarize-native-regressions.py "$E/regression" "$E/regression-summary" > "$E/regression-summary-run.out" 2>&1; echo $? > "$E/regression-summary-exit.txt"
docker --context colima-yxt-permission ps -a > "$E/final-docker-ps.txt"
git rev-parse HEAD > "$E/final-head.txt"; git status --porcelain > "$E/final-git-status.txt"
echo "全部完成，回归脚本退出码 $(cat "$E/regression-script-exit.txt")"
EOF
echo "脚本已写好"
```

看到"脚本已写好"后，再执行下面这行，测量从这里开始：

```bash
caffeinate -dims bash "evidence/raw/round2-remediation-91683df/run-remediation.sh"
```

运行期间：

- 不关这个终端窗口，不合盖。
- 不让 codex 或其他程序操作 Docker、Colima 和这个仓库。

## 第 3 步：交给 codex 打包（把下面这段转给 codex）

> 第 2 轮整改后的测量已由用户在"终端"App 中执行完毕。证据目录是 `evidence/raw/round2-remediation-91683df`，执行脚本是其中的 `run-remediation.sh`，测量提交是 `91683df702182724dbe9025afa5726606ba3d340`。
>
> 请按《codex测量指令_01_整改前基线》第五节的同样方式交回证据，其中证据目录、分支名、完整包名里的 `round2-baseline-817256b` 一律换成 `round2-remediation-91683df`：
>
> 1. 写 `ENVIRONMENT.md`、`MANIFEST.json` 和 `ARCHIVE.json`。
> 2. 打完整包并计算 SHA-256。
> 3. 推送孤儿分支 `evidence/round2-remediation-91683df`。
>
> 不要重跑任何窗口或回归，不要修改已生成的文件，也不要给出性能结论。最后回复以下内容：
>
> - 证据分支提交号；
> - 完整包的大小和 SHA-256；
> - 全部 `*-exit.txt` 文件的原文；
> - 两个 `window-gate.json` 的原文；
> - `regression-summary.json` 中 `complete`、`observations`、`issues` 三个字段的原文。
