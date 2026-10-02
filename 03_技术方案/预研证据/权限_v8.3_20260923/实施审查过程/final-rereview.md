# 全分支终审集中修复：一次限定复审

日期：2026-09-23。基线 `e8c5bf9`，复审 HEAD `d6e2d66`，修复应用/Schema/测试源码提交 `cb72484ed8e7547146920fd4312dd24f8c9e2402`。输入为 `final-review.md`、`final-fix-report.md` 和指定的 `review-e8c5bf9..d6e2d66.diff`（677 行），以及下列已有原始证据。

**限定代码质量判定：PASS with Minor。I1、I2、I3、I4 均 ADDRESSED；未发现本次修复引入新的 Critical 或 Important。保留 M1 的局部可读性余项，不构成代码质量阻断。结合前次全分支审查，本原型在该冻结源码上的代码质量条件已满足。**

**这不是整体 Go。** 本次关闭 I4 指空白页/模板编译缺陷已修复并有真实 Chrome 渲染证据，不代表完整任命浏览器流程通过；四个资源匹配的 50 客户端 × 600 秒参考窗口及独立逐项 168 点语义审计也不由本报告放行。控制器仍须按原门禁完成并裁定。缺失性能结果不在本报告中被写成通过或实测失败。

## 执行边界

只读代码、日志、JSONL、已保存截图；在内存中解析既有证据、重算数量/字面比较/文件 SHA256。未运行产品测试、HTTP、数据库、容器、负载或浏览器，未改源码/HEAD/索引，未派生代理。唯一写入为本报告。

本次逐项检查了全部修复 diff 中的应用、Schema、测试和 UI 改动。读取集中修复报告，对照原始观察及测试源码，不把报告或总通过数当独立语义验收。14 个已修改源码/测试文件的当前 SHA256 全部匹配 `evidence/raw/final-fix-source-identity.json` 中 cb72484 的清单。没有扩大成对冻结版本未改代码的第二次全量审查。

## 逐项裁定

| 原发现 | 裁定 | 修复与证据 | 限定结论 |
| --- | --- | --- | --- |
| I1 任命 ID 碰撞 | **ADDRESSED** | `src/training/service.ts:56–68` 使用 UUID 作为行身份，按准确 `(tenant_id,person_id,project_id)` 冲突更新，并 RETURNING 持久化 id/active；`sql/schema.sql:15` 增加语义唯一约束、person/project 非空。真实 RED2 显示受限 M 不能直接操作第一关系，但旧代码仍因第二关系写入切换第一关系；GREEN 保持第一关系不变、第二关系激活/撤销/重复操作准确且返回同一已存 ID。 | 本次授权目标与实际更新关系一致。授权、权威锁、公司校验未削弱。Schema 属于可重建原型，未冒称完成生产迁移。 |
| I2 合法混合 ID 批次误拒 | **ADDRESSED** | `src/infrastructure/sets.ts:1–8` 对比两边长度、各自唯一性和完整成员集合；`src/training/enrollment-service.ts:35–38`、`src/organization/service.ts:62` 使用该函数。RED2 的两候选项目/团队 add/remove 四种正例及部门移动均误拒，最终 focused 对应全部 200；缺失/越权/重复成员整批 403 且完整 roster 不变，未授权子部门使整树不变。 | 不依赖 JS/PG collation，也没有仅以长度代替授权。请求重复拒绝、公司/对象约束、事务、旧公司报名冲突校验及删除谓词保留。 |
| I3 分类 403/503 存在性泄露 | **ADDRESSED** | `src/knowledge/service.ts:55–62,69–73` 在领域命令边界把当前租户缺失目标/请求父节点转为 Denied，之后才计算有效分类；未改全局异常映射。最终 focused 对 configure、append-preview、append、import、recheck 的不可访问/不存在/仅外租户存在目标给出完全相同 403 安全业务响应；授权正例 200、导入后项缺失整批回滚、实际 Redis timeout 503 及恢复 200 保留。 | 动态 meta 被保留在完整 HTTP 原文，只从安全业务响应等价比较中排除。已存在目标的损坏祖先仍由原 effectiveCategory 抛普通异常；源码和专项函数测试证明未改成 Denied，本次没有把它宣称为新做的 HTTP 故障复现。 |
| I4 Vue in-DOM 空白页 | **ADDRESSED** | `web/index.html:4,6,8,9,11` 所有本次涉及的 el-* 自闭合标签改成显式结束标签；v-if/v-else 成为合法相邻结构，导航逻辑及异步 sequence 防护未改。已保存的 Native/Casbin Chrome 管理页快照和截图均显示 Z 后台导航及 P/Q 项目表，控制台没有 compiler-30；Native 拒绝/返回学习中心快照正确。 | 已修复原空白页并验证两候选真实渲染。完整任命、撤权、剩余角色等浏览器状态转换仍归控制器门禁，不能以 smoke 替代。 |

### M1 — Minor，部分改善、余项保留

报名服务的缩进、try/catch、集合比较和任命 SQL 已比原版本易审阅。`src/authz/company-service.ts:10–23`、既有 Task4 密集测试仍未整理，新专项测试部分行也较密集。本轮无需为此扩大成全库格式修改；建议在后续实际修改相邻逻辑时整理。未发现因此引入行为变化，不新增阻断。

## 新破坏检查

没有发现本次 diff 新增的 Critical/Important：

- 任命保留原事务/权威锁，只改变行身份和冲突对象；返回持久化 ID 避免重复调用拿到未落库 UUID。Schema 语义唯一约束与 upsert 目标一致，不会将不同关系合并。
- 集合比较拒绝任一方重复、缺员或额外成员，保留整批校验；移除顺序敏感性没有放宽权限。部门 SQL 和目标父节点/子树校验未删除。
- 分类预查使用当前租户 facts，不跨租户补查。缺失目标统一 Denied 没有吞掉 Redis/DB 或已有分类祖先结构错误。
- 四个历史测试清理由构造 ID 改为精确 person/project 关系，没有删除行为断言。公共测试 HTTP recorder 为可选写入既有观察，不改变请求、响应或断言。这里的文件写入指被审测试代码，本审查没有执行它。
- UI diff 仅修闭合结构，没有增加客户端授权决定或绕开后端数据校验。
- 旧公司报名冲突的事务内 Denied、既有 snapshot、source/field/company 上限、导出所有者和撤权路径未在 diff 中被削弱。完整功能/故障回归提供支持，但不是对任意未测场景的保证。

## 已核验的原始证据与口径

### 定向 RED/GREEN

直接读取 JSONL 并复算字面比较与 SHA256：

| 文件（均位于 `evidence/raw/`） | 观察数 | 字面差异 | SHA256 |
| --- | ---: | ---: | --- |
| final-fix-red2.jsonl | 110 | 32 | 767dfcb64163ca8bcac4c6f3ed425466357d81aa6e5481d89a2b2e9970a22d17 |
| final-fix-green.jsonl | 130 | 0 | 6831e4b4cc40fa984104dc0c0dc03f44e04d1aeaed594ef954975001d0262251 |
| final-fix-final-focused.jsonl | 130 | 0 | 43c99dfd4a7c72978b6a07eac4ba43080691a1700d9b68c8a6b1e0e1d74c9986 |

对应 Node 日志原文：RED2 53 条测试计数、15 pass / 38 fail；GREEN 和 final-focused 各 53/53，均无 skipped/cancelled/todo。父子测试失败数与 JSONL 比较数不是同一口径，不能当 38 个独立权限缺陷。

重点行：`final-fix-red2.jsonl:4,6,8,10` 为 Native 任命碰撞，`:15–18,43` 为混合 ID 误拒，`:46–51,53` 为分类差异，Casbin 同型观察亦在该文件。`final-fix-final-focused.jsonl:1–65` 是 Native、`:66–130` 是 Casbin，已逐个解析全体预期/实际，均相等；包含自然键与返回 ID、完整 roster/tree 回滚、安全响应三元组和 Redis 故障/恢复。

`final-fix-red2-http.jsonl` 与 `final-fix-final-focused-http.jsonl` 各保存 104 条完整响应（每候选 52），已解析并抽读具体请求/响应及其 meta。前者 source 为 e8c5bf9，后者诚实标注 pre-commit working tree；后续 cb72484 文件清单和冻结回归是额外来源绑定，未把预提交观察伪称为提交后执行。第一次 `final-fix-red.*` 中 I3 的外租户 creator 夹具失败被修复报告明确排除；本裁定使用真实 RED2，不把夹具失败充作产品 I3 证据。

### 冻结源码回归及归档

读取 `final-fix-full-campaign/commands.json`，其顺序与报告一致：cleanseed/core，再依次重置并跑 Native HTTP、Casbin HTTP、Task3、Task4、Task5；各命令 exit 0。直接读取各阶段测试摘要：55 + 2 + 2 + 118 + 82 + 58 = **317 passing Node entries**，无 skipped/cancelled/todo。这不是独立接受点数。

解析保存的全部相关 JSONL，复算而非仅相信汇总：Task3/4/5 分别 **322 / 290 / 616** 个 expected/actual，字面差异 0；各文件 SHA256 与 observation-audit 清单一致。完整 HTTP 文件计数 **288 / 310 / 690 / 14 / 14 = 1,316**，每项保留 status/body，source 均为 cb72484。这只是完整响应记录数；本复审没有逐条独立证明 1,316 个响应业务正确，也没有据此机械裁定 168 点通过。

`final-fix-full-campaign/task2-fix1-observations.jsonl:1–4,9–12` 的 **8 条全记录字面差异仍存在**：actual 多出 revision，全部指定 expected 业务字段相等。作为 partial-fields 结果保留；不能写作全记录等价。现有测试对 revision 的独立权威检查未改。本次没有运行新的权威读。

重新按 copy manifest 核对全部 **35 对 original/archived** 文件：size 和 SHA256 均一致。清单自身 SHA256 为 `1d401e1ede4ee395b84d0b212c925594c4c46d07f6ec1f6cd368ea53df79a8b5`；归档 `commands.json` 为 `1c45a5f0788767bef626752596f0ad22461132a0759db88147c7e0210f9a27ad`。读取已有 typecheck/build/diffcheck 输出；未重新执行这些命令。

### 浏览器证据

读取 `output/playwright/final-fix-smoke/` 中 `native-admin.txt`、`casbin-admin.txt`、`native-denial.txt`、`native-return.txt`、两份 console 和 close 记录，以及复制后的 CLI 快照：`page-2026-09-23T00-13-03-389Z.yml`、`00-13-21-441Z.yml`、`00-14-59-815Z.yml`、`00-16-02-783Z.yml`（完整文件名均以前缀 page-2026-09-23T 开始）。本审查还亲自读取已有 `native-admin.png`、`casbin-admin.png`，确认均不是空白，具有后台导航及 P/Q 表。

后续 Native console 为空，Casbin console 仅 favicon 404；未发现 compiler-30。Native 拒绝快照为通用提示，返回快照为学习中心。上述均是别人已执行并保存的真实 Chrome smoke，本审查没有打开浏览器，也没有读取或裁定控制器仍在进行的 `output/playwright/final-native` 完整活动。

## 最终限定结论及余项

- I1–I4：全部 **ADDRESSED**。原全分支审查的四个 Important 在本次已审冻结源码关闭。
- 新增 Critical 0、Important 0；保留原 M1 可读性余项 1，不阻断限定代码质量。
- **代码质量：PASS with Minor（cb72484 源码 / d6e2d66 复审 HEAD）。整体 Go：未由本报告授予。** 完整浏览器、四个正式参考窗口、独立 168 点语义证据审计和最终交付/文档门禁仍需完成并有独立结论。
- 原型范围不扩大；保留 G01/G02/G04/G05/G06、D42/T10 我方定义/原站未验证、七宣读/四最简/两已承担风险及复用折抵 0。无用户签字、正式 AC 完成或生产就绪的新增声称。
