# Binding global constraints (verbatim from approved execution plan)

- T-05：各角色/节点内先应用人员覆盖，再合并同节点同动作的有效授权；覆盖仅影响对应角色。字段绑定该对象上实际匹配的授权来源。
- T-06：任命项目负责人后可进入管理后台，仅授予培训中心对应功能和任命项目权限。其他合法角色和任命保留。
- T-07：客户甲/乙/内部三类身份；所有角色并集、六范围和项目任命都与公司上限取交集。共享内容不共享名册/学习数据。
- 每个受保护请求从权威数据库读取当前版本及账号有效性。Redis 故障采用 fail closed，不允许 DB fallback。Pub/Sub 不是撤权保证。
- 撤销事务提交后新发起的下一请求必须失效，包括媒体每个新分片、导出执行和领取；高风险写入必须与撤销事务排序。
- PostgreSQL 4 vCPU/8 GB；两个应用实例各2 vCPU/4 GB；独立Redis；50并发客户端、每页50条、持续10分钟。权限额外耗时p95≤50ms，列表含过滤/count p95≤500ms，复杂历史聚合p95≤2s。授权错误0，无N+1。有效/拒绝/基础设施失败与冷热缓存分别统计，快速拒绝不计正常查询性能。
- 任何越租户/越范围/字段泄漏、撤销后新请求仍成功、故障放行、语义未裁定或性能未达门槛均不放行。未执行就是未完成，不得声称通过。
- Input documents 00/01/02 and handoff are read-only. Work only in this local prototype and 03_技术方案 outputs. No formal feature implementation; no production data, no external sends.
- Record literal expected values derived from the spec, RED/GREEN commands and output. Never manufacture timings, fault injection results or human signatures. Prototype reuse credit remains0.

