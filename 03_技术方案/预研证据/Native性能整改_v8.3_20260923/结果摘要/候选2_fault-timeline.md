# Native 撤权与故障时间线

所有日期为UTC。同钟分别比较宿主撤销确认→新请求、PG提交→权威读取；不跨宿主/Colima时钟推断微秒顺序。

| A/B PID | PG提交/xmin | 宿主确认→新请求 | PG权威读取 | revision | 9项检查 |
|---|---|---|---|---|---|
| 54954/54934 | 2026-09-23T08:03:26.027Z / 21137 | 2026-09-23T08:03:26.012Z → 2026-09-23T08:03:26.014Z | 2026-09-23T08:03:26.033Z | 1790150561706 → 1790150561707 | True |

| 阶段 | 首个→末个观察 | 路径数 | 预期状态 | 完整且匹配 |
|---|---|---:|---:|---|
| warm protected controls | 2026-09-23T08:03:01.988Z → 2026-09-23T08:03:02.215Z | 16 | 200 | True |
| Redis timeout warm | 2026-09-23T08:03:02.523Z → 2026-09-23T08:03:07.270Z | 16 | 503 | True |
| Redis timeout cold restarted process | 2026-09-23T08:03:13.009Z → 2026-09-23T08:03:17.725Z | 16 | 503 | True |
| Redis timeout recovery current authority | 2026-09-23T08:03:22.819Z → 2026-09-23T08:03:23.090Z | 16 | 200 | True |
| Redis timeout cold process recovery current authority | 2026-09-23T08:03:23.117Z → 2026-09-23T08:03:23.373Z | 16 | 200 | True |
| Redis disconnected warm | 2026-09-23T08:03:23.619Z → 2026-09-23T08:03:23.701Z | 16 | 503 | True |
| Redis disconnected cold restarted process | 2026-09-23T08:03:24.173Z → 2026-09-23T08:03:24.269Z | 16 | 503 | True |
| Redis reconnected current authority | 2026-09-23T08:03:24.633Z → 2026-09-23T08:03:24.857Z | 16 | 200 | True |
| DB authority unavailable | 2026-09-23T08:03:25.336Z → 2026-09-23T08:03:25.352Z | 16 | 503 | True |
| DB recovered authoritative current state | 2026-09-23T08:03:25.727Z → 2026-09-23T08:03:25.959Z | 16 | 200 | True |

拒绝与故障均不计入正常成功性能。只证明本次原型路径，不补证五项永久缺口或真实媒体网关。源码与所有逐条载荷、票据、N+1、移籍记录同包保留。
