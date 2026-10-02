# Native 撤权与故障时间线

所有日期为UTC。同钟分别比较宿主撤销确认→新请求、PG提交→权威读取；不跨宿主/Colima时钟推断微秒顺序。

| A/B PID | PG提交/xmin | 宿主确认→新请求 | PG权威读取 | revision | 9项检查 |
|---|---|---|---|---|---|
| 51317/51297 | 2026-09-23T06:59:15.759Z / 20340 | 2026-09-23T06:59:15.648Z → 2026-09-23T06:59:15.650Z | 2026-09-23T06:59:15.766Z | 1790146710626 → 1790146710627 | True |

| 阶段 | 首个→末个观察 | 路径数 | 预期状态 | 完整且匹配 |
|---|---|---:|---:|---|
| warm protected controls | 2026-09-23T06:58:51.837Z → 2026-09-23T06:58:52.094Z | 16 | 200 | True |
| Redis timeout warm | 2026-09-23T06:58:52.403Z → 2026-09-23T06:58:57.154Z | 16 | 503 | True |
| Redis timeout cold restarted process | 2026-09-23T06:59:02.949Z → 2026-09-23T06:59:07.723Z | 16 | 503 | True |
| Redis timeout recovery current authority | 2026-09-23T06:59:12.639Z → 2026-09-23T06:59:12.953Z | 16 | 200 | True |
| Redis timeout cold process recovery current authority | 2026-09-23T06:59:12.976Z → 2026-09-23T06:59:13.233Z | 16 | 200 | True |
| Redis disconnected warm | 2026-09-23T06:59:13.406Z → 2026-09-23T06:59:13.493Z | 16 | 503 | True |
| Redis disconnected cold restarted process | 2026-09-23T06:59:13.991Z → 2026-09-23T06:59:14.126Z | 16 | 503 | True |
| Redis reconnected current authority | 2026-09-23T06:59:14.275Z → 2026-09-23T06:59:14.496Z | 16 | 200 | True |
| DB authority unavailable | 2026-09-23T06:59:14.974Z → 2026-09-23T06:59:14.989Z | 16 | 503 | True |
| DB recovered authoritative current state | 2026-09-23T06:59:15.356Z → 2026-09-23T06:59:15.599Z | 16 | 200 | True |

拒绝与故障均不计入正常成功性能。只证明本次原型路径，不补证五项永久缺口或真实媒体网关。源码与所有逐条载荷、票据、N+1、移籍记录同包保留。
