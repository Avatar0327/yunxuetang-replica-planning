# 给 codex 测量会话的指令：第 2 轮整改前基线重跑

> 用法：在执行测量的那台电脑上，新开 codex 会话，整段粘贴。
> 编写：Claude 技术会话（第 2 轮实施方，D-48）。2026-10-03。
> 依据：用户 2026-10-03 裁定"让另一台电脑上的 codex 完成测试"（建议业务侧在审核记录中补记为 D-49，本文件不代记）。

---

你本轮**只做测量执行**，不做整改、不做分析结论、不给 Go/No-Go。整改代码与最终报告由 Claude 技术会话负责。请严格按下面步骤执行；任何一步不满足，停下来告诉用户，不要自行变通。

## 零、运行方式

1. 必须在测量电脑本机运行（Codex CLI，或 Codex 应用的本地模式），**不要用 Codex 云端任务**。云端容器里没有 Colima，也分不出 10 vCPU / 24 GiB。
2. 需要的权限：联网（git clone、npm ci、拉取镜像）、访问 Docker/Colima、写 `~/.colima`。默认的工作区沙箱会拦住这些操作；请让用户为本会话开放完全访问，或逐条批准。不要为了绕开沙箱去改脚本。
3. 每个测量窗口约 11～12 分钟，回归可能更久。如果你的命令执行有时长上限、可能中途杀掉进程，就把第四节每一步的整行命令包进 `nohup bash -c '<原命令整行>' > evidence/raw/round2-baseline-817256b/<hot|cold|regression>.out 2>&1 &` 在后台运行，再轮询对应的 `*-script-exit.txt` 是否生成。`.out` 文件必须放在 `round2-baseline-817256b/` 下，不能放进 `hot/`、`cold/`、`regression/` 子目录，因为脚本发现目标目录已存在时会拒绝运行。一次只跑一个，等前一个结束再开始下一个；不得并行。

## 一、纪律

1. **不改任何文件**：源码、SQL、脚本、Dockerfile、依赖锁、超时、连接池、资源上限、负载参数、门槛都不改。所有窗口脚本要求工作区干净，`git status` 必须为空。
2. 不放宽、不换算任何门槛；不剔除、不删除任何失败样本或失败目录；不为了数字更好而重跑。
3. 窗口如果中途失败（出现 `incomplete.txt`，或脚本在测量开始前以退出码 2 结束）：原目录原样保留，用新目录名加 `-retry1` 重跑一次，两次都上报。只因为门禁未通过而得到的退出码 1 **不算失败**，不要重跑。
4. 测量期间独占机器：接电源，用 `caffeinate -dims` 防止睡眠；不运行其他 codex 任务、浏览器压测、编译或备份。
5. 原站账号凭据不得出现在任何命令、文件、提交或回复中（本测量全部使用合成数据，用不到）。
6. 不修改规划仓库 `yunxuetang-replica-planning`。

## 二、输入

- 仓库：`https://github.com/Avatar0327/yunxuetang-permission-spike`（私有，原型仓库，不是正式 B1 代码）。
- 测量提交：`817256bf1e1fc722aaa5f0c21878e84fe8df1306`（`main`）。这是 codex 第 1 轮的最终交付提交；它的应用代码与候选 2 的测量提交 `dfa6341` 相同，只多了一个只读诊断工具。

## 三、环境准备（记录实际值，不要为了"更像原环境"而调整）

1. 记录硬件与系统：
   ```
   sw_vers; sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize; uname -a
   ```
   原环境参考值：macOS 26.5.1，Apple M5 Pro，18 逻辑 CPU，48 GiB。如果不同，如实记录，**不要停**。
2. Homebrew 安装 `node@24`（脚本写死使用 `/opt/homebrew/opt/node@24/bin`）、`python3`、`colima`、`docker` CLI。记录 `node --version`（原环境为 24.21.0）。
3. Colima 实例名必须是 `yxt-permission`（脚本使用 docker context `colima-yxt-permission`）。
   用户已确认：这台机器上**已经有** `yxt-permission` 实例（已停止，aarch64、10 CPU、24 GiB、35 GiB 磁盘，docker 运行时），大概率就是第 1 轮测量用的那个实例。**直接复用，不要删除，不要重建，不要改 CPU、内存、磁盘参数**：
   ```
   colima start yxt-permission
   colima list
   cat ~/.colima/yxt-permission/colima.yaml          # 记录 vmType（原环境为 vz）、cpu、memory、disk
   docker context ls; docker --context colima-yxt-permission info
   docker --context colima-yxt-permission ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}'
   docker --context colima-yxt-permission volume ls
   ls -d /Users/*/Agent本地开发/云学堂权限预研 2>/dev/null   # 只用来记录是不是第 1 轮的同一台机器，不读、不改里面的内容
   ```
   以上输出全部保存到 `evidence/raw/round2-baseline-817256b/existing-environment.txt`（第 4 步建好目录后再写入；也可以先存到临时文件，再移进去）。
   遇到下面的情况，按对应方式处理：
   - 已有容器 `yxt-api-a` 或 `yxt-api-b`（不论是否在运行）：**先停下告诉用户**。窗口脚本会拒绝运行，而且容器里可能留着第 1 轮的日志，不得自行删除。
   - 已有 `yxt-pg`、`yxt-redis` 容器：先用 `docker --context colima-yxt-permission inspect yxt-pg yxt-redis` 核对。镜像 digest 必须分别是 `postgres@sha256:639ab7ce…b652`、`redis@sha256:c6eabf74…6f`（完整值见 `tools/start-infrastructure.sh`）；资源上限必须是 PG 4 CPU / 8 GiB、Redis 1 CPU / 1 GiB；PG 启动参数必须与脚本一致。全部一致就复用（`start-infrastructure.sh` 会直接 `docker start`）；任何一项不一致，先停下告诉用户。
   - 已有 `yxt-permission-pgdata` 卷：复用。每个窗口的 seed 会重建合成数据 schema，不需要清空卷，也不得删除。
   - `colima.yaml` 里 vmType 不是 vz，或 CPU、内存不是 10 / 24 GiB：先停下告诉用户。
4. 克隆并检出：
   ```
   git clone https://github.com/Avatar0327/yunxuetang-permission-spike.git
   cd yunxuetang-permission-spike
   git checkout --detach 817256bf1e1fc722aaa5f0c21878e84fe8df1306
   export PATH="/opt/homebrew/opt/node@24/bin:$PATH"
   npm ci
   git status --porcelain   # 必须为空
   mkdir -p evidence/raw/round2-baseline-817256b   # 然后把第 3 步的输出存入 existing-environment.txt
   ```
5. 预构建 API 镜像（只在需要时）：`tools/run-native-window.sh` 构建镜像时使用代理 `http://192.168.5.2:7890`。如果这台机器上没有这个代理，请**不要改脚本**，先手工构建同名、同标签的镜像，脚本检测到后会直接复用：
   ```
   docker --context colima-yxt-permission build \
     --tag yxt-permission:spike-817256bf1e1f \
     --label org.opencontainers.image.revision=817256bf1e1fc722aaa5f0c21878e84fe8df1306 \
     [按本机情况加 --build-arg HTTP_PROXY=... HTTPS_PROXY=... NO_PROXY=localhost,127.0.0.1,yxt-pg,yxt-redis] .
   ```
   构建日志保存为 `evidence/raw/round2-baseline-817256b/prebuild.txt`，并记录实际使用的构建参数。
6. 启动 PG/Redis（固定镜像 digest 与资源上限都已写在脚本里）：
   ```
   bash tools/start-infrastructure.sh > evidence/raw/round2-baseline-817256b/start-infrastructure.txt 2>&1
   ```

## 四、测量（顺序固定）

`evidence/raw/` 已被 `.gitignore` 忽略，写在里面不会弄脏工作区。

1. 热窗（50 客户端 × 600 秒，四场景等比轮转，脚本内自动重新 seed）：
   ```
   caffeinate -dims bash tools/run-native-window.sh evidence/raw/round2-baseline-817256b/hot candidate hot; echo $? > evidence/raw/round2-baseline-817256b/hot-script-exit.txt
   ```
2. 冷窗：
   ```
   caffeinate -dims bash tools/run-native-window.sh evidence/raw/round2-baseline-817256b/cold candidate cold; echo $? > evidence/raw/round2-baseline-817256b/cold-script-exit.txt
   ```
3. 权限/撤权/故障选定回归（会自己起停两个宿主 API 进程，并对 `yxt-redis`、`yxt-pg` 注入故障；必须在两个窗口结束、4311/4312 端口空闲后执行）：
   ```
   caffeinate -dims bash tools/run-native-regressions.sh evidence/raw/round2-baseline-817256b/regression; echo $? > evidence/raw/round2-baseline-817256b/regression-script-exit.txt
   python3 tools/summarize-native-regressions.py evidence/raw/round2-baseline-817256b/regression evidence/raw/round2-baseline-817256b/regression-summary
   ```
   第 1 轮的参考结果：55 项测试通过，456/456 条字面观察匹配，10 个故障阶段 × 16 条路径，下一请求时序检查 9/9。如果这次结果不同，**原样上报，不要修**。
4. 收尾：
   ```
   docker --context colima-yxt-permission ps -a > evidence/raw/round2-baseline-817256b/final-docker-ps.txt
   git rev-parse HEAD > evidence/raw/round2-baseline-817256b/final-head.txt
   git status --porcelain > evidence/raw/round2-baseline-817256b/final-git-status.txt
   ```

## 五、交回证据

1. 在 `evidence/raw/round2-baseline-817256b/ENVIRONMENT.md` 中写：第三节记录的全部实际值、每个窗口的开始和结束时间（UTC）、是否预构建了镜像及所用参数、与原环境的所有差异，以及任何异常。只写事实，不写判断。
2. 生成完整文件指纹 `MANIFEST.json`：列出 `round2-baseline-817256b/` 下每个文件的相对路径、字节数和 SHA-256。
3. 把整个目录打包为 `round2-baseline-817256b.tar.gz`，记录大小和 SHA-256。完整包留在本机，交给用户保管。
4. 推送到原型仓库的**独立孤儿分支** `evidence/round2-baseline-817256b`。分支里只放证据，不含代码：
   - 单文件超过 50 MB 的（例如 API 日志），先用 gzip 压缩后再提交；压缩后仍超过 95 MB 的不提交，只在 `MANIFEST.json` 中保留它的指纹，并标注"未入库"。
   - 分支根目录放 `ENVIRONMENT.md`、`MANIFEST.json`，以及完整包的大小和 SHA-256。
5. 最后回复用户以下内容，用户会转给 Claude 技术会话：
   - 证据分支名与提交号；
   - 热窗、冷窗各自的 `runner-exit.txt`、`audit-exit.txt`、`gate-exit.txt` 和 `*-script-exit.txt`；
   - 两个 `window-gate.json` 的原文；
   - 回归的 `test-exit.txt` 和 `regression-summary.json` 中 `complete`、`observations`、`issues` 三个字段的原文；
   - 完整包的文件名、大小和 SHA-256；
   - 与原环境的差异，以及任何偏离本指令的地方。

不要附加性能结论或 Go/No-Go 判断。
