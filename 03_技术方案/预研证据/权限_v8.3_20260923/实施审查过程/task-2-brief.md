### Task 2: Core PostgreSQL, two-instance HTTP, revocation and measurement milestone

**Scope allocation revision:** The original Task2 was too broad for one bounded implementation/review. This task is the completed core milestone; Task3 below retains every remaining domain/coverage obligation. No AUTH group or overall gate is passed by this split. Original requirements remain in Git and the ledger workspace's task-2-original-scope.md. Full authority remains04§9.4 and docs/acceptance-manifest.json (24 groups,168 required subcases).

**Files:** authz revision/cache/compiler/bulk-candidate/registry; infrastructure db; organization public/service; report service/exports; training core service; Nest bootstrap; schema/seed; integration/http/race tests; functional/fault/benchmark/explain runners; Vue shell and README.

**Interfaces:** Consume Task1 central semantics without duplicate source/field logic. Real PostgreSQL17 on55432, Redis7 on56379, two Nest/Fastify processes4311/4312. Synthetic database permission_spike/spike/spike only. Node24. Environment and container caps are controller-owned. API contract is README; continuation map is docs/task2-follow-up.md.

- [ ] Real tenant-qualified SQL schema and 50k/500 people,2000departments/20depth,20roles,1m facts fixtures; actual-count assertions,21depth/cycle/invalidparent negative tests.
- [ ] Central authoritative tenant revision+acting account on every protected request, live Redis check even warmL1, versioned snapshots with before/after check; no DB fallback; actual independent Native/Casbin bulk source selection, no per-row engine calls.
- [ ] Six scopes/role-local overrides/action-bound union and row-source field projection in real parameterized list/count/detail/history SQL. Report queries use own projections and OrganizationPublic permitted sets, not organization private joins. ALL avoids50k enumeration but preserves company/state caps.
- [ ] Core project list/detail/roster/save/media/appointments, current person updates and membership revoke; report export create/execute/claim. Every exposed service path central-authorized; writes/revoke lock ordered. Additional training, account, knowledge and delegation paths are Task3 obligations, not claimed here.
- [ ] Two-instance functional tests both candidates, B oldL1/L2 with PubSub disabled, A commit then B next request/media denial. Real Redis stop/timeout/recovery, DB outage, snapshot race and both high-risk write/revoke orderings. Preserve timelines and initial failures.
- [ ] Benchmark runner separates candidate/cache/scenario/success/denial/infra failures, actual cache states and every sample; includes authority/poolwait/Redis/plan in permission metric, complete list+count and aggregate latency. Controller performs resource-matched full reference runs after Task3.
- [ ] Minimal Vue backend shell reflects central capabilities and safe business errors; browser test remains controller duty after all domain paths stabilize.
- [ ] Typecheck/build and dependency audit; write exact commands, raw paths, limitations, integration ports, and missing subcases in report and continuation map. Do not claim complete Task2 original scope or overall AUTH pass. Do not dispatch subagents.

