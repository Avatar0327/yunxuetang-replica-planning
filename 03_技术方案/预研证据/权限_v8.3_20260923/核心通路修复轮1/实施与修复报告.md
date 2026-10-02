# Task 2 core milestone report — 2026-09-23

Status: core implementation milestone, **not full Task2 / 168-point acceptance complete**. Controller formally preserved remaining obligations as Task3; formal B1 is not started. No subagents used. No planning input documents, controller Docker/tools or controller plan files edited by this worker. Final source commit: `b707efb7528007af7467b9a45ce54d6006c3092d`.

## Implemented core

- Real PostgreSQL synthetic schema, tenant-qualified FK relationships, revision triggers and audit events, immutable history data company, current report person projection, seeded 50000 T1/500 T2/2000 departments/depth20/20 roles/1000000 load facts plus2 focused history facts. Report facts now reference the report-owned unique tenant/person projection. Invalid depth21/cycle/parent/category11 are rejected. General populated-subtree moves are conservatively rejected, not implemented.
- Central Task1 normalization, bulk scope port and parameterized SQL compiler, source-local fields, matched source evidence, list/count/search/detail/history grouping. ALL/SELF avoid full people enumeration. Constrained scopes resolve central department semantics then fetch relevant people once. Reports never query organization private tables.
- Genuine Casbin static source selection via actual policy/model/enforce before shared SQL scope/field compilation. Native results are never supplied to Casbin. No per-returned-row enforce. Both candidates preserve node/action/tenant/actor/revision/source bindings.
- Every protected service loads current authoritative account/revision and checks live Redis. Tenant/person/revision snapshots, before/after and pre-plan-use revision checks; changed version fails closed. Every write service locks authority revision FOR UPDATE until commit. New requests after revoke must reauthorize. Pub/Sub deliberately absent; responses expose pubsub=false.
- Minimal NestJS11.2.5 + Fastify5.12.1 HTTP bootstrap and local Vue3/ElementPlus shell. Server session lookup establishes actor/tenant. Shared project configuration remains tenant content; roster is company-bound; whole-project writes require every affected company. Appointment-derived backend capabilities, source revoke, target user changes, report export create/execute/claim, controlled synthetic project media segment.
- Functional/fault/EXPLAIN/benchmark runners. Raw JSONL records literal expected/actual observations. Benchmark saves every request compressed, exact classifications, query counts, actual cache states and candidate/instance metadata. No600-second reference window was run by this worker.

## TDD and verification actually performed

Initial RED: `node --import tsx --test test/integration.test.ts` -> missing db module (`evidence/raw/task2-red.txt`). Initial HTTP RED: `node --import tsx --test test/http.test.ts` -> connection refused (`task2-http-red.txt`). These initial REDs do not establish RED for every later expanded case. Six-scope and lock tests were later audits, not pre-implementation RED; this limitation is explicit.

Final focused suites recorded so far:

| Command | Observed result | Raw output |
|---|---|---|
| npm run test:integration | 5/5 pass, real SQL, both candidates; source-local raw values, literal IDs/count, own history company boundary, six scopes, subtree options, overrides, scale/FK | evidence/raw/task2-final-integration.txt |
| node --import tsx --test test/races.test.ts | 4/4 pass, both candidates; real blocked snapshot construction crossed revoke ->503; write lock first commits, revoke next then fresh write403 | evidence/raw/task2-final-races.txt; task2-races.jsonl |
| npm run test:semantic | all existing Task1 semantic tests pass; exact count in raw output | evidence/raw/task2-final-semantic.txt |
| npm run test:http | 2/2 pass, appointment shell/revoke and export recheck; this command revokes M broad membership and requires reseed | evidence/raw/task2-http-green-attempt1.txt |
| EVIDENCE_DIR=evidence/raw/task2-native npm run functional | focused observations passed, fullAcceptance=incomplete | task2-functional-native.txt; task2-native/functional.jsonl |
| EVIDENCE_DIR=evidence/raw/task2-casbin npm run functional | focused observations passed, fullAcceptance=incomplete | task2-functional-casbin.txt; task2-casbin/functional.jsonl |
| npm run faults (each candidate, A/B separate processes) | actual Redis stop, CLIENT PAUSE1000ms, Redis recovery, PG stop/recovery, A revoke/B warm next media403; no payload on503 | task2-faults-native.txt; task2-faults-casbin.txt; each candidate faults.jsonl |
| npm run explain | PostgreSQL EXPLAIN ANALYZE BUFFERS produced for broad/constrained list/history | evidence/raw/explain/*.json; task2-explain.txt |
| npm run build / npm run typecheck | passed during implementation; final output refreshed below | evidence/raw/task2-final-build.txt (pending final capture) |
| npm audit --json | zero vulnerabilities after Nest11.2.5 and explicit Fastify5.12.1 patch override | evidence/raw/task2-final-audit.json |

Six-scope actual IDs/revisions/source IDs: `evidence/raw/task2-scope-observations.jsonl`. Warm HTTP page20/50/200 queries were exactly8 on both instances/candidates, not linear with page size. See per-candidate query-count.jsonl. Cold requests add membership/appointment SQL (10 for scoped list).

### Observed failure and repair (retain all raw output)

Casbin cold process smoke `smoke-casbin-cold-list` recorded2 infrastructure503 and781 successes, no authorization errors. Its command failed; the subsequent history smoke succeeded separately. Cause: redis.isOpen becomes true before handshake, so concurrent first requests skipped awaiting the shared connect promise. A real Redis20-concurrent-check test was added and run RED:1 fulfilled/19 rejected (`task2-cache-race-red.txt`). Repair waits for the same connecting promise on every first concurrent request, verifies isReady, and still performs individual live PING. GREEN20/20 (`task2-cache-race-green.txt`). No cached allow or fallback introduced. Post-repair HTTP cold smoke/fault regression passed; exact results are in the final supplement below.

Metrics were also corrected before freeze to include token database lookup and actual SQL compilation inside permission overhead. Earlier smoke timings are therefore diagnostic only, not the final metric implementation. Native early hot smoke included4 initial cold snapshots; later hot runner prewarms each instance and retains actual cache states. These samples are not relabeled or discarded.

## API / runner handoff

Full contract is README.md. Bootstrap: `npm run build` writes `dist/src/bootstrap.js`; `npm run start` runs it. Environment: PORT4311/4312, INSTANCE_ID A/B, CANDIDATE native/casbin, CACHE_MODE hot/cold, PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD/PGPOOL, REDIS_HOST/REDIS_PORT/REDIS_TIMEOUT_MS. Host defaults PG127.0.0.1:55432 / permission_spike/spike/spike and Redis127.0.0.1:56379. Container hosts yxt-pg:5432 and yxt-redis:6379. Controller Docker assets untouched.

Synthetic bearer tokens: spike-M broad internal, spike-X customer self history, spike-Y customer learner, spike-L plain learner, spike-Z registered fixture administrator, spike-disabled/spike-deleted negative accounts. GET /auth/me; GET /report; GET /report?node=department-report; GET /history (M broad or X constrained); project list/detail/roster/media; POST appointments, source revoke, people changes; report export create/execute/claim. Browser UI `/` uses local bundled assets. API subject cannot be changed by query/body self-assertions.

Benchmark runner (set matching env on servers): `CANDIDATE=casbin CACHE_MODE=cold SCENARIO=list-constrained CONCURRENCY=4 DURATION_SECONDS=3 OUTPUT=evidence/raw/unique-name npm run benchmark`. SCENARIO supports list-broad/list-constrained/history-broad/history-constrained; defaults50clients600seconds, page50. API_A/API_B override base URLs. PHASE success/denial/redisfault keeps independent histograms. Redisfault only labels measurement; controller must inject/maintain actual fault. Cold **report/history** requests skip cache read after DEL, still DB-authority/PING/build/revalidate; other routes use normal caching. Phase/process/PG-page-cache cold are not equivalent. Mixed four-scenario reference runner is assigned to follow-up Task3, not implemented here.

Seed resets schemas and initializes a unique time-derived revision to prevent stale Redis key reuse. Do not seed or run mutating functional/race tests while measuring. Functional runner expects freshly seeded fixture and hot-mode servers. Final seeded fixture and stopped host API state will be confirmed below.

## Precise remaining work and architectural limits

`docs/task2-follow-up.md` maps each gap to existing contracts, tables and minimal next implementation: knowledge persistence/import/locks/publication; selected-membership delegation create/edit/recheck/cycle/cap snapshots; actual team enrollment; own-wallet partition/offset/ref paths; customer-company grant mutation; company attachments/progress/search/project exports; full168-point truth matrix and negative fuzz/log/cache scan; durable limited export worker and streaming output; cold-fault/export-fault and missing races; browser/capped long windows.

Remaining static coupling is stated, not hidden: central Authority reads trusted organization/training facts directly; organization command writes report projection synchronously; training appointment reads organization company directly. Public port extraction and module privilege/splitability enforcement remain work. Reports themselves only query report-owned tables. Historical fixtures currently preserve data company and historical department, not the full historical job/state snapshot shape. Same-name second-tenant objects are not yet present (IDs only). Export stores protected JSON and accumulates output in memory; safe conservative version invalidation does not establish production queue/streaming readiness.

Per-run gaps.json retains the immutable manifest plus incomplete status. Early functional observation IDs AUTH-T14-03 actually checked disabled **actor**, not disabled target report filtering; current runner renamed that observation actor-disabled-denied. This correction is recorded without editing old evidence. All168 full acceptance statuses remain incomplete until controller audit; do not infer a complete AUTH-Txx pass from these observations.

## Final regression supplement

- `CANDIDATE=casbin CACHE_MODE=cold DURATION_SECONDS=3 CONCURRENCY=4 SCENARIO=list-constrained OUTPUT=evidence/raw/smoke-casbin-cold-list-fixed npm run benchmark`: exit0;1872/1872 success,0 denial,0 infrastructure failures,0 authorization errors,1872 actual cold snapshots. Both instances used; referenceWindow=false. All samples retained gzip. Final SQL-compilation + token timing boundaries are present in this repaired run. This is still a short uncapped smoke, not a performance gate.
- `EVIDENCE_DIR=evidence/raw/task2-casbin-fixed npm run faults`: repaired cache real Redis disconnect/timeout/recovery and PostgreSQL failure/recovery regression passed. See task2-faults-casbin-fixed.txt and task2-casbin-fixed/faults.jsonl.
- `npm run typecheck`, `npm run build`, `git diff --check`: passed after final repair; task2-final-typecheck.txt, task2-final-build.txt.
- Existing semantic tests26/26, integration5/5, races4/4; real concurrent Redis connection regression1/1 (20 calls). Native functional49 observations and Casbin55 observations passed; count difference is six additional explicit page-query-count assertions added after the native run, not candidate disagreement.

Controller can continue from the core services and documented gaps. Source policy fixtures currently persist membership-local NodePolicy JSON; role table holds IDs, and complete role-policy mutation/fanout remains follow-up work. Raw process completion times bound revoke commit above; race tests also preserve explicit transaction COMMIT completion. Precise in-transaction commit instrumentation is not claimed.

Final handoff: source commit b707efb7528007af7467b9a45ce54d6006c3092d; host API processes on4311/4312 stopped. Fresh seed complete with actual counts50000/500/2000/1000000 and0 active appointments; see evidence/raw/task2-handoff-state.json. Controller-only .gitignore/plan/tools changes remain uncommitted by this worker. This report is local under ignored .superpowers; source README and follow-up map are committed.

## Defensive review fix round 1 — 2026-09-23

Read both `task-2-review-interruption.md` and the subsequently preserved `task-2-review.md`. The independent review is explicitly partial/interrupted, not approval. This round repairs only its known locking-facts and export-pagination defects; no Task3 domain work, controller plans/tools or Docker files were changed.

1. `Authority.current(lock=true)` now requires a client owned by the shared active transaction boundary. Pool and bare autocommit clients fail closed503. That boundary explicitly begins READ COMMITTED. The authority call first acquires only the tenant revision row lock, then reads revision + actor + current company/company-grant/account facts in a separate, fresh statement while holding the lock until transaction completion. Every current production locking call is inside that shared transaction helper; nonlocking reads retain their existing path.
2. Export means the complete authorized filtered result independently of UI offset/limit. Creation strips UI pagination; execution explicitly starts offset0 (including old saved jobs). Nonaggregate exports advance200 rows normally. Aggregated export rows already contain all groups, so execution stores them once and does not loop against the underlying fact count. Tenant/company/action/source-field rules, revision rechecks and fail-closed behavior remain unchanged.

### Genuine focused RED/GREEN

Command: `PATH=/opt/homebrew/opt/node@24/bin:$PATH node --import tsx --test test/review-regressions.test.ts`.

- `evidence/raw/task2-fix1-red.txt`: initial11 checks,7 failures. Both candidates returned old departmentD1 instead ofD2 or companyA instead ofB after actually waiting on the DB lock; grouped206-fact export emitted6 rows instead of3; pool lock request did not reject.
- `evidence/raw/task2-fix1-expanded-red.txt`: added waiting ReportService-entry variants, retaining actual authorized row mismatch alongside direct-context evidence.
- `evidence/raw/task2-fix1-complete-red.txt`: added client offset150/limit3 ordinary export regression. Full17 checks,13 failures and4 account-state passes before the repair. Failures are retained unchanged.
- `evidence/raw/task2-fix1-green.txt`:17/17 pass after repair, both candidates. Context and direct locked ReportService paths return current department/company facts and literal permitted sets (`B/E/M/N` afterD2 move; only`h-X-B` after customerX moves toB). Waiting disabled/deleted actor reads deny403. Revision equality is checked against a fresh authoritative read. Real SQL group truth: `fix-group-A/count201/points402`, `fix-group-B/count4/points8`, `old-A/count1/points10`, each exactly once. Ordinary export independently checks all206 IDs, including with initial UI pagination, and excludes old companyB facts for customerA.
- Structured actual/expected records, candidate, revision where available and UTC timestamps append to `evidence/raw/task2-fix1-observations.jsonl`. Fixtures are restored in finally blocks; revisions/audit advance monotonically. No API host processes started in this round.

Scoped regression commands: `node --import tsx --test test/races.test.ts` ->4/4 (`task2-fix1-races.txt`); `npm run test:integration` ->5/5 (`task2-fix1-integration.txt`); `npm run typecheck` / `npm run build` ->pass (`task2-fix1-typecheck.txt`, `task2-fix1-build.txt`); `git diff --check` ->clean. These focused fixes do not establish complete review or full acceptance. Source SHA is appended after the defensive commit.

Fix-round1 source commit: `6f1e75a4c4fca597b23cc86e321756f142460680` (4 files only: revision transaction guard/read, DB transaction boundary, export pagination, focused regressions). Final focused rerun after formatting:17/17 pass in `evidence/raw/task2-fix1-final-green.txt`. Controller plan change remains outside this commit. Await independent scoped review; do not mark interrupted review as passed.
