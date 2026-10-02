### Finding Verdicts

- **Important N1 — 子分类继承使父分类窄授权越过原来源对象上限：ADDRESSED。** `src/knowledge/service.ts:38` 比较变更前后有效策略拥有者，在同一事务内冻结范围扩大的既有分类策略及解锁后重新生效的 custom 策略（`:52`、`:53`）；`:75` 在层级更新前调用它。当前编辑策略已按变更后的完整对象集验证，其他策略保留原 source/snapshot 等待明确重验。`src/knowledge/public.ts:17` 将真正策略拥有者的 cap 沿继承链传递；`src/authz/policy.ts:128` 按分类或 custom 来源选择 cap，并在 `:129` 同时检查 node/action/course。来源绑定但缺失快照时使用空 cap，custom 失败不会恢复已被替换的分类浏览权（`src/authz/revision.ts:123`）。
- **N1 实测核证：ADDRESSED。** 原始 RED 两候选均出现实际200、期望403（`evidence/raw/task3-fix2-red.txt:18`、`:36`）。最终真实 HTTP 观察在子分类切换后、没有再次保存父策略的情况下立即403（`evidence/raw/task3-fix2-final-observations.jsonl:107`、`:120`），且父策略被冻结并保留原 cap（`:108`、`:121`）。测试故意将父策略恢复 active 后，越界课程仍403、原课程仍200（`:109`–`:110`、`:122`–`:123`），独立证明运行时 cap 生效。原 SELF 来源重验 suspended；明确扩大同一来源后再重验才恢复（`:111`–`:113`、`:124`–`:126`）。

### New Breakage in the Fix Diff

- **Critical：无。Important：无。Minor：无。** 本轮应用修复未发现新的可操作缺陷。
- **相邻路径核证通过：** 导入失败回滚层级变更和父策略冻结（最终观察`:104`–`:105`、`:117`–`:118`）；分类/custom 的动作、对象及缺失快照拒绝与独立维护权限保留（`:127`–`:148`）；取消强制继承后分类/custom 均冻结，分别明确重验后恢复（`:149`–`:170`）。`test/task3-inheritance-caps.test.ts:19`、`:28`、`:47`、`:72` 对这些行为有直接断言。

### Out-of-Scope Observations

- 无。本轮未重新打开已解决的 R1–R4。包内 `51a72aa`、`0d3acb0`、`f70a87c` 为 controller 文档/辅助提交，已与 `146073b` 的 N1 应用修复区分；它们不构成完整门禁通过证据。

### Checks

- 分段读取修复包、任务 brief、上轮报告及实现报告末尾 round2。独立读取既有 RED/GREEN 和最终输出：定向6/6（`evidence/raw/task3-fix2-green2.txt:7`），核心53/53（`evidence/raw/task3-fix2-core.txt:54`），领域118/118（`evidence/raw/task3-fix2-domains.txt:137`）；typecheck/build 输出无警告，audit 为0漏洞（`evidence/raw/task3-fix2-final-audit.json:11`）。未重跑测试。
- 独立比较最终322条 JSONL：Native160、Casbin160、shared2，expected/actual 差异0；SHA256为 `2a8aff2ef84a38c2ab23897fdb93e4f06fa97448d4c62769a1ee6d626d5032f0`。`docs/task3-coverage.json.reviewFixRound2` 的70条引用均与原始行号、候选和名称一致。
- 本轮无需额外查看无改动代码。未执行 Git、外部调用、应用或数据库变更；只写本复审报告。

### Verdict

**Fix round：All findings addressed, no new Critical/Important breakage。** N1 已解决。

**限定 Task3 Spec：通过本轮限定复审。Quality：Approved。** 此结论仅覆盖已审 Task3 里程碑及本轮修复；完整168项、浏览器、长基准、生产媒体/导出与独立部署仍待后续验证，不构成全预研 Go 或正式 B1 放行。

**Report：** `.superpowers/sdd/2026-09-23-permission-spike/task-3-rereview-round2.md`。
