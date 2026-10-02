# Task 1 implementation report

Status: DONE_WITH_CONCERNS (kernel implementation complete; integration/persistence trust and remaining AUTH evidence explicitly not claimed).

Commit: `72adfaa` — `feat(spike): add source-bound authorization kernel and Casbin candidate`.
Base: `2d21695b4293c70a51ad1d7de95b193e41676bcf`; branch `spike/permission-v83`.
Workspace: `/Users/peng/Agent本地开发/云学堂权限预研`.
Completed UTC: 2026-09-22T19:22:45Z verification; local date 2026-09-23.

## Delivered

- `src/authz/contracts.ts`: typed context, registered node semantics, memberships/overrides/provenance, explicit appointments, source-bound grants, scopes, resource facts, subjects, query plan, and bulk OrganizationPublic port.
- `src/authz/policy.ts`: role-local override then exact node/action union inputs; membership-local jurisdiction; hard tenant/company/status/publication caps; explicit appointment project capabilities/backend shell; subject resolver/catalog browse replacement; one-call bulk query planning with source and port binding verification.
- `src/authz/scope.ts`: six scope interpretation; current organization reference resolver; strict direct-manager team; registered SELF anchors; all marker; object-ID intersection; reference hierarchy validation.
- `src/authz/candidates.ts`: genuine Native and Casbin engines with same normalized grants/facts. Casbin executes a real exported model, policy rows and source scope predicate; no Native decision passed to it. Both return actual matching source IDs and source-bound raw fields.
- `src/authz/delegation.ts`: selected membership only, creation vs editing level semantics, registered role mutation action gate, actual resolved business object subset and per-object field subset. `assertGrantSubset` reuses the cap logic for non-role commands without copying role-specific mutation rules.
- `test/fixtures.ts`, `test/semantic.test.ts`: literal truth fixtures and 14 grouped tests, both engines independently compared to expected source IDs/raw fields; 118 helper comparisons in final JSONL with zero mismatches (additional appointment/catalog assertions and pure scope/delegation assertions are in TAP output/test source, not included in that 118).
- `test/kernel-benchmark.ts`: repeatable object-match microtimings and versions, clearly not HTTP/SQL performance.
- `docs/kernel-contract.md`: exact exports, trust boundary, source binding, bulk SQL consumer protocol, case-specific hard constraints, downstream persistence requirements and limitations.
- `package.json`, `package-lock.json`, `tsconfig.json`: Node24 ESM/strict TypeScript and pinned dependency versions.

## TDD and actual command evidence

All Node/npm commands used `PATH=/opt/homebrew/opt/node@24/bin:$PATH` per command; no global PATH edits.

| Evidence path under evidence/raw | Command | Actual result |
|---|---|---|
| task1-red.txt | npm run test:semantic | Exit1; policy module absent; accepted initial RED per brief |
| task1-behavior-red.txt | npm run test:semantic | Exit1; duplicate source identity caused Native to allow L-B unexpectedly |
| task1-bulk-red.txt | npm run test:semantic | Exit1; missing buildQueryPolicy function |
| task1-level-red.txt | npm run test:semantic | Exit1; equal-level creation improperly rejected by initial over-broad level check |
| task1-role-action-red.txt | npm run test:semantic | Exit1; missing rejection when selected membership lacks role create action |
| task1-green.txt | npm run test:semantic | Exit0; 14 tests / 14 pass / 0 fail, 139.340209ms test runner duration |
| task1-typecheck.txt | npm run typecheck | Exit0, no diagnostics |
| task1-cases.jsonl | SEMANTIC_EVIDENCE=evidence/raw/task1-cases.jsonl npm run test:semantic | 118 comparisons, zero expected-source/raw-field mismatches |
| task1-microbenchmark.txt | npm run bench:kernel | Exit0, 200 timed iterations per candidate after 20 warmups |
| task1-audit.txt | npm audit --json | Exit0, zero vulnerabilities |
| task1-versions.txt | npm ls --depth=0 | Exit0, exact top-level versions |

An added regression test initially contained a missing `]` in a test array (parser/typecheck failure); it was fixed before assertions ran. This syntax error is not presented as a behavior RED. Initial install audit reported two moderate entries through Casbin's csv-parse dependency; csv-parse is now explicitly overridden to 7.0.2, audit is zero and exercised model paths remain green. No file/CSV adapter is exercised.

Observed versions: Node v24.21.0, casbin5.38.0, TypeScript5.9.3, tsx4.20.6, @types/node24.10.1; darwin arm64. Microbenchmark p50/p95/p99 in ms: Native 0.001709/0.003250/0.008500; Casbin 0.028750/0.066750/0.205250. These include per-call model construction for Casbin, use one small synthetic object, and are **not a production performance comparison or AUTH-T18 evidence**.

## Self-review against requirements

- Team literal A/B differs from own department A/C and subtree A/C/D; indirect E excluded. Six scopes include positive and negative object matches and missing/default parameter boundaries. Tenant/revision mismatch denied by organization resolution.
- View-all does not extend edit-ownDept or download. Own-role SELF/null/delete overrides preserve unrelated role rights; old membership overrides do not attach to a new membership. Raw phone in D1 is absent on D2 rows from the masked source.
- Hard tenant, external current-company, disabled/deleted/nonexistent/current business state restrictions precede source union. Current dataCompanyId limits historical rows independently of SELF and historical department snapshots. Narrow own-wallet exception denies another person and cross-company reference flags.
- Appointment P/Q matches only those projects, grants no organization node/raw/delegation, and revocation normalization retains Q/other role capabilities. A restricted company cap refuses whole-project affected companies and a foreign company's project.
- Node-specific SELF anchors are exercised for learning/account/course/project/face-to-face, including misleading createdBy negatives.
- Delegation compares selected membership A rather than larger B; fields and actual object sets cannot be borrowed. Provenance inactive/recheck/suspended deny. During review, I corrected an initial extra restriction on **creation**: spec only limits new roles to2/3; equal/higher restriction applies to **editing**. Controller confirmed this interpretation. Role create/update action remains required from the same selected context.
- Catalog lock prevents custom browse even for creator. Custom replaces browse only; public is same-tenant authenticated; unknown subject denies. A classroom_member resolver produces common source grants without matcher/query changes.
- Duplicate source IDs were a real ambiguity found by focused RED and now fail normalization closed.
- Bulk planner selects node/action, verifies grant/source/scope/company/revision bindings, invokes OrganizationPublic once and returns source-local resolved scopes and fields. It does not do row filtering or SQL.
- Exact file staging excluded controller-owned Docker/tools/environment/acceptance files. Planning sources in iCloud were only read; no production/original site was accessed. No subagents/reviewers were dispatched. `git diff --cached --check` passed before commit.

## Concerns and handoff requirements (do not mark as passed)

1. The kernel trusts server facts. TypeScript types and revision numbers do not prove HTTP input provenance, live account/object states, DB freshness or trustworthy company lists. Task2 must obtain/validate these through authoritative ports on every protected request and fail closed on infrastructure failure. No AUTH-Txx overall pass is asserted here.
2. `assertGrantSubset`/`assertCanDelegate` compare current resolved object sets. The owning port must resolve actual business object IDs **including company/status caps**, not use person IDs for courses. Task2 must persist provenance/cap snapshots and transactionally freeze/recheck on organization/source changes; cycle rejection, dynamic propagation and revoked-source races are not implemented in Task1.
3. Catalog inputs must be authoritative effective ancestry grants plus lock origin. This task tests normalization/locked course override, not DB ancestry inheritance, parent append, depth10 mutation checks, concurrent imports or creator mutation APIs. Those commands must enforce own mutation actions, lock checks and shared `assertGrantSubset` before writes.
4. Scope resolution is a small in-memory **reference** OrganizationPublic implementation. Reports must use the real bulk port then source-bound parameterized SQL before pagination/count/aggregate; never invoke either candidate per row. No PostgreSQL query, 50k/1M fixture, EXPLAIN, N+1, export/download projection or UI evidence exists yet.
5. Team relation resolution does not by itself authorize project enrollment. Task2 must enforce registered action, project switch, affected target companies, current states and commit ordering. Appointment capability registry must remain explicit and limited; no wildcard training grants.
6. `ownWallet` is deliberately a separate node mode; SQL and serialization must preserve company-separated accounts and reject cross-company offsets/source references. A resource boolean test is not financial integration proof.
7. Casbin is an actual object rule matcher, not an alternate implementation of all business semantics. Per-object enforcer construction is acceptable for this reference candidate but must not become a list-query strategy. Bulk SQL stays centralized; candidate microtimings do not satisfy any latency/SLA gate.
8. Raw evidence and this report are intentionally in ignored paths per existing repository setup. Controller must retain/copy them into final evidence delivery. The code commit contains tests and reproduction scripts; it does not contain raw output.

Next consumer must read `docs/kernel-contract.md` before extending contracts. No unresolved business question is raised by this task; the concerns are explicit implementation/evidence boundaries for Task2 and controller review.

## Fix round 1 — wallet unknown hard facts fail closed

Status: DONE. Commit `b7e31f6` (`fix(authz): require complete own-wallet hard facts`), based on `72adfaa`. Addressed the one P2 request in task-1-review.md; no subagents dispatched.

Verified the counterexample before changing production code. Both Native and Casbin allowed the reviewer's typed unbound account lacking dataCompanyId and crossCompanyReference. Added separate literal tests for each candidate: known separate old-company account (allow), missing company (deny), empty company (deny), whitespace-only company (deny), missing reference status (deny), and the exact unbound shape (deny). The focused RED had 2 positive passes and 10 negative failures. Tests did not infer expected decisions from production code.

Changed `hardAllowed` ownWallet branch to require personId equal to actor, a string dataCompanyId with nonempty trimmed content, and crossCompanyReference **exactly false**. No ordinary company-cap check was introduced for this exception, so a known, safe own account from company CA still passes for a customer currently in CB. Updated the earlier known-wallet fixture to explicitly provide its safe reference fact and documented the required facts in kernel-contract.md. Only those three fix files were committed.

Commands all prepend `PATH=/opt/homebrew/opt/node@24/bin:$PATH`. Original evidence files were preserved; new full timestamped outputs:

| Round1 evidence under evidence/raw | Command | Actual output summary |
|---|---|---|
| task1-fix-round1-red.txt | node --import tsx --test --test-name-pattern='wallet hard facts' test/semantic.test.ts | Exit1; 12 tests, 2 pass, 10 fail. Both candidates returned source role:wallet:wallet-own:account.own.view for unbound account and missing-hard-fact cases. |
| task1-fix-round1-green.txt | node --import tsx --test --test-name-pattern='wallet hard facts' test/semantic.test.ts | Exit0; 12 tests, 12 pass, 0 fail; 128.749125ms. |
| task1-fix-round1-semantic.txt | npm run test:semantic | Exit0; 26 tests, 26 pass, 0 fail; 129.086625ms. |
| task1-fix-round1-typecheck.txt | npm run typecheck | Exit0; tsc --noEmit, no diagnostics. |

Last verification timestamp: 2026-09-22T19:29:23.266882Z. `git diff --cached --check` also passed before the fix commit. The local report/evidence remain in previously ignored paths, ready for controller evidence collection.

Self-review: the new predicate distinguishes unknown from explicitly safe and requires an account-company identity before applying the exception. Both missing fields are optional on the general Resource contract, so this runtime guard is necessary. It preserves the approved T-15 known old-company own-account exception. It does not prove that supplied facts came from authoritative DB sources or that financial serialization/SQL prohibits cross-company offsets; those remain Task2 integration responsibilities. No HTTP/SQL/two-instance/UI/performance or overall AUTH gate is asserted by this fix.
