### Finding Verdicts

- **Stale actor facts after a revision-lock wait — ADDRESSED.** `src/authz/revision.ts:29-36` now acquires only the tenant revision row lock, then reads revision and actor/company facts in a subsequent statement. `src/infrastructure/db.ts:10-12`, `:17-18`, `:28` restrict the locking path to an active client owned by the shared READ COMMITTED transaction boundary and remove that authorization when the transaction ends. The second statement therefore obtains a fresh snapshot after lock acquisition; pool and bare autocommit clients fail closed. Existing production locking callers inspected in the original diff use this transaction helper (`src/organization/service.ts:8`, `:26`; `src/training/service.ts:24`, `:36`; `src/report/exports.ts:10`, `:18`).
- **Aggregate export repetition and ordinary initial-offset handling — ADDRESSED.** `src/report/exports.ts:9-13` removes UI limit/offset from persisted filters; `:22` explicitly starts execution and reauthorization at offset zero, including for previously saved options. `:33-35` paginates only ordinary rows; aggregate results are stored once. The existing aggregate query returns all groups (`src/report/service.ts:41-45`), so the revised export loop now matches its contract. Ordinary rows advance in 200-row pages without inheriting or restarting from a UI offset.

### New Breakage in the Fix Diff

- None found. The transaction guard is removed in `finally`, and lock acquisition, fresh facts, and protected operations use the same transaction client (`src/infrastructure/db.ts:16-29`; `src/authz/revision.ts:30-36`). Export changes preserve tenant/owner lookup, export-action reauthorization, revision equality, protected payload storage, and claim-state checks (`src/report/exports.ts:19-28`, `:37`).
- The added regressions exercise real waiting transactions for both candidates, assert literal current departments/company-permitted row sets and disabled/deleted rejection, verify aggregate group values and all 206 ordinary export IDs, and reject unsupported lock clients (`test/review-regressions.test.ts:16-57`, `:58-85`, `:87-120`). They are behavior assertions rather than implementation-only assertions.

### Existing Evidence Checked Read-Only

| Existing file | Observed content |
|---|---|
| `evidence/raw/task2-final-integration.txt:5` | Five SQL integration tests pass; Native/Casbin source-bound fields, company history, six scopes and membership override, actual scale/FK checks; zero failures. |
| `evidence/raw/task2-final-races.txt:1` | Four tests pass; both candidates cover snapshot/revoke and write/revoke sequencing; zero failures. |
| `evidence/raw/task2-final-build.txt:2` and `task2-final-typecheck.txt:2` | Build and typecheck command output is present with no diagnostics. These files do not independently embed shell exit codes. |
| `evidence/raw/task2-final-audit.json:3` | Empty vulnerabilities object; metadata total is zero. |
| `evidence/raw/task2-fix1-final-green.txt:1` | All 17 focused regressions pass; zero failures, skipped, cancelled or todo cases. |
| `evidence/raw/task2-fix1-races.txt:1` | Four existing race regressions pass after the fix. |
| `evidence/raw/task2-fix1-integration.txt:5` | Five existing SQL integration tests pass after the fix. |
| `evidence/raw/task2-fix1-typecheck.txt:2` and `task2-fix1-build.txt:2` | Command output is present with no diagnostics; no embedded shell exit codes. |
| `evidence/raw/task2-native/faults.jsonl:1` | Native A/B observations: B warmed; A revoke completed; B's subsequent request returned 403; actual runner Redis disconnect/timeout and DB outage observations returned 503 without the media fragment; recovery returned 200. |
| `evidence/raw/task2-casbin-fixed/faults.jsonl:1` | Corresponding Casbin A/B observations show the same denial/failure/recovery behavior and `pubsub:false`. |

- The fault observations were assessed alongside the previously inspected runner's real service stop/start and Redis pause operations (`scripts/run-faults.ts:25`, `:35-38`, `:42`). They predate this fix; this round did not replay them. The fix does not alter the Redis availability/cache implementation or the nonlocking media query path.
- No warnings or unexplained noise appeared in the checked final outputs. This round read existing evidence only; it executed no tests, experiments, application requests, database statements, or Git commands.

### Core Review Completion and Scope

- **Spec compliance: ✅ Approved for the revised bounded Task2 core milestone.** This conclusion combines the original source inspection, the now-closed findings, and the evidence checks above; it is not inferred solely from the 17 new tests.
- Original static inspection covered the supplied core source diff: tenant-qualified schema/seed and hierarchy constraints (`sql/schema.sql:6-25`, `:35-50`); independent bulk candidates and source-local field SQL (`src/authz/bulk-candidate.ts:13-26`; `src/authz/compiler.ts:20-36`); authoritative revisions/live Redis/version checks (`src/authz/revision.ts:43-90` in the original package; `src/authz/cache.ts:17-38`); OrganizationPublic scope resolution (`src/organization/public.ts:6-20`); report list/count/detail/history SQL (`src/report/service.ts:20-58`); all exposed training, organization and export service methods; HTTP identity binding and safe errors (`src/bootstrap.ts:24-55`); functional/fault/race/benchmark/explain runners and the minimal Vue shell.
- The original metric inspection included token lookup, authority/cache/candidate/scope work, SQL compilation, complete list plus count timing, and distinct benchmark outcome/cache distributions (`src/bootstrap.ts:26-32`; `src/authz/revision.ts:77-88` in the original package; `src/report/service.ts:25-55`; `scripts/benchmark.ts:45-98`). No full performance gate was evaluated or passed.
- The one focused unchanged-code inspection resolved the concrete source-binding concern: central normalized source identifiers include node/action, and the query builder validates tenant/actor/revision/scope bindings (`src/authz/policy.ts:52`, `:67`, `:143-157`). No broad unchanged-code crawl occurred.
- **No remaining unreviewed core application-source area is identified within the supplied packages.** The first original tool output truncated a portion of generated `package-lock.json`; this review did not manually audit every transitive dependency entry. Top-level dependency changes and the existing zero-vulnerability audit were inspected. This limitation does not represent an unreviewed authorization implementation path.
- Remaining evidence limitations are explicit: not every historical raw functional/semantic/EXPLAIN/sample artifact was independently reread, and build logs omit explicit shell return-code records. The directly inspected integration, race, fix-regression and fault outputs substantiate the focused core behaviors; they do not establish all 168 acceptance points.

### Out-of-Scope Observations

- No additional code defect is asserted outside the fix diff. Previously documented private-port coupling, membership-local fixture policy persistence, remaining knowledge/delegation/team/wallet paths, durable/chunked exports, broader matrix coverage, and full browser/resource-matched performance acceptance remain allocated follow-up work (`docs/task2-follow-up.md:5-25`). This review does not upgrade any AUTH group or grant formal B1/overall Go.

### Verdict

**Fix round:** All findings addressed, no new Critical/Important breakage.

**Core task quality:** Approved for completion of the revised bounded core milestone at `6f1e75a4c4fca597b23cc86e321756f142460680`. The earlier interrupted report remains a preserved historical record; this completed static/evidence continuation supplies the current core verdict. Full domain, browser and performance acceptance remain unpassed.
