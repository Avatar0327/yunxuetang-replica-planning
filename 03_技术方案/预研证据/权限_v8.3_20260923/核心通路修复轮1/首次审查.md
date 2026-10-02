### Spec Compliance

- ❌ Issues found in the bounded core milestone: the authority lock path can bind stale actor facts to a new revision (`src/authz/revision.ts:29`, `:35`, `:64`, `:86`); aggregate export execution uses fact counts to paginate an aggregate query that ignores pagination (`src/report/exports.ts:20`, `:29`; `src/report/service.ts:41`, `:44`, `:45`).
- ⚠️ Review interrupted: this is a partial defensive review, not a complete approval or an AUTH/Go verdict. Automatic safety review interrupted final report generation; the controller subsequently restricted work to documenting existing observations. No further experiments, requests, or tests were performed after that instruction.
- ⚠️ Cannot verify from this review: completeness and cleanliness of the implementer's referenced raw final suite/build/audit outputs; these evidence files were not independently inspected before the interruption. The full matrix, capped performance windows, browser acceptance, and the explicitly allocated Task3 domain/public-port obligations remain outside this bounded approval.

### Strengths

- Central source selection and SQL projection preserve node/action/source bindings, with real Casbin policies rather than a Native decision fed into Casbin (`src/authz/bulk-candidate.ts:13`, `:18`, `:23`; `src/authz/compiler.ts:27`, `:35`). A focused read of the unchanged builder confirmed source identifiers include node/action and binding validation remains central (`src/authz/policy.ts:52`, `:67`, `:143`, `:148`).
- Protected authority loading reads PostgreSQL and checks live Redis before cache access, including warm L1 (`src/authz/revision.ts:45`, `:46`, `:48`; `src/authz/cache.ts:25`). Report SQL uses report-owned projections and applies bound tenant/company predicates (`src/report/service.ts:26`, `:39`; `src/authz/compiler.ts:20`, `:22`).
- The continuation map explicitly preserves unfinished domain and acceptance obligations rather than claiming the original large task is complete (`docs/task2-follow-up.md:3`, `:7`, `:14`, `:15`).

### Issues

#### Critical (Must Fix)

- No separate Critical finding was established within the completed inspection scope.

#### Important (Should Fix)

- **P1 — Refresh actor facts after acquiring the revision lock.** `src/authz/revision.ts:29` combines the revision row lock with joined actor facts and a company-grant subquery in one statement. Under PostgreSQL READ COMMITTED, waiting on that revision row can return the updated revision while the other facts remain from the earlier statement snapshot. Line 35 builds the authoritative context from this mixed result. The later checks at lines 64 and 86 compare only revision numbers, so they do not reject the stale department/company context. This violates revision-consistent authorization on the shared locked path used by core services. Acquire the revision lock first, then read authoritative actor/company facts in a fresh statement while retaining that lock; add a focused regression for a blocked lock acquisition crossing an actor-fact change.
  - Existing targeted observation: the waiting `current` call returned revision **1790107510504**, department **D1**; its immediate fresh reread returned the same revision **1790107510504**, department **D2**. The revision-only validation accepted this mismatch.
  - Existing targeted service observation: the waiting, locked `ReportService.list` call returned **A/C**, while a freshly authorized call returned **B/E/M/N**, both at revision **1790107510506**. This establishes a difference in actual authorized rows, not merely a context-object discrepancy. The test used the shared Native path; the affected authority code is also used by Casbin.
  - Existing restoration observation: M's department was restored to **D1** after each experiment; reader transactions were rolled back. Revision/audit values advanced monotonically. Host API processes were not started by this review.

- **P1 — Give aggregate exports a compatible pagination contract.** `src/report/service.ts:41-45` returns all aggregate groups, ignores limit/offset, and reports the sum of underlying fact counts. `src/report/exports.ts:20`, `:28-31` treats that count as the number of pageable rows and appends the same aggregate result for every 200 facts. An aggregate with more than 200 facts therefore repeats groups and repeats the full aggregate query; the export transaction also retains the authority lock during that work. The options parser allows the aggregate flag to reach export creation (`src/bootstrap.ts:23`, `:53`). Either reject unsupported aggregate exports explicitly, execute an aggregate export once, or implement pagination/counts over aggregate groups. The ordinary export loop should also normalize or consistently advance any saved initial offset rather than resetting subsequent offsets to 200.
  - Existing read-only observation: aggregate report calls with offsets **0** and **200** returned identical rows: `old-A/count 1/points 10` and `old-B/count 1/points 20`; both reported count **2**. The full repeated export loop was deliberately not executed. The repetition for larger fact counts follows from the inspected loop and unpaginated aggregate branch.

#### Minor (Nice to Have)

- No additional Minor finding is asserted in this interrupted report.

### Assessment

**Task quality:** Needs fixes; review incomplete.

**Reasoning:** The core has central source-bound SQL and live infrastructure checks, but the observed revision/context mismatch and aggregate export pagination contract prevent approval. This report records only established findings and does not imply that all remaining paths were cleared.

**Checks completed:** Read the task brief, implementation report, required reviewer template, and the supplied diff in sequential bounded chunks; the first output truncated part of the generated dependency lockfile. One focused inspection of unchanged `src/authz/policy.ts` resolved the concrete source-ID/action-binding concern. Before interruption, completed the targeted authority-context observation, its actual report-service confirmation, and a read-only aggregate pagination comparison described above. No suite rerun, source/index/branch mutation, or subagent dispatch occurred. This document is the only checkout artifact written by the reviewer.
