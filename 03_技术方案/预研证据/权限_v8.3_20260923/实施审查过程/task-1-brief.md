### Task 1: Central authorization semantics and two genuine candidate engines

**Files:** package.json/package-lock.json/tsconfig.json; `src/authz/contracts.ts`, `policy.ts`, `scope.ts`, `delegation.ts`, `candidates.ts`; `test/semantic.test.ts`, `test/fixtures.ts`; `docs/kernel-contract.md`.

**Interfaces:** Produce typed central policy normalization and `NativeCandidate`/`CasbinCandidate` accepting the same effective grants and resource facts. Async candidate match returns the matching source IDs and field capabilities, not just a boolean. Produce scope expressions that Task2 can resolve in bulk through OrganizationPublic and compile to SQL. Document exact exported signatures in kernel-contract.md for the next task; Task2 must not reinvent role/override/scoping rules. All authorization inputs are server facts, never client-provided grant objects.

- [ ] Read the complete 04 spec, then write independent literal fixtures/tests before implementation. The pure kernel tests do not count as real SQL/two-instance/UI evidence.

Required fixture truth table (add distinct source IDs, tenant/company/node/action and role memberships so matching can be audited):
* Main tenant T1 and T2 same-name objects. Internal I, customer A, customer B. Actor M in dept D1; A in D1 managed by M, B in D2 managed by M, C in D1 managed by N, D in child D11 managed by N, E in D2 managed by A. Team(M)=[A,B], ownDept(M) includes A,C but not B,D,E; subtree includes A,C,D, excludes B,E. Use exact literal expected arrays for fixture IDs.
* Node personal-learning view ALL and node department-report view ownDept remain independent. An edit-ownDept role plus view-all role grants view-all but edits only ownDept. Override first membership to SELF preserves view-all from the other membership. Empty override yields zero grants for that source; deleting restores inheritance. Override cannot create actions/nav/fields. Jurisdiction belongs to membership, no config=>empty. Specified departments descendants default false.
* Source A grants raw phone on dept D1 and source B grants masked viewing D2. D2 raw phone must be absent. Tenant/company/disabled/deleted/unknown node/unknown subject hard failures apply before source union. View grant cannot enlarge edit or download scope.
* Ordinary learner has no backend; P appointment derives shell/training registered capabilities and P only. P+Q then revokeP retainsQ; revoke last removes shell; lawful role preserves its rights. Appointment grants do not confer organization/roles or automatic raw fields/delegation. Company cap still applies; whole-project mutation requires all affected companies.
* Each six-scope parameter boundary has explicit allowed/denied cases. SELF anchors: person-learning/account personId, course uploaderId, project createdBy, face-to-face ownerId. Unsupported node/scope must deny; no universal createdBy shortcut.
* Delegate with selected membership A cannot borrow B's larger powers. Levels2/3 cannot edit equal/higher, ordinary create cannot createlevel1, level1 ordinary edit denied. Proposed actions, actual resolved sets and raw field caps must be subsets of A and explicitly delegable. Appointments not delegable. Provenance inactive/recheck/suspended sources deny; regrant new membership cannot use old override. Compare sets, not enum ranks.
* Category browse/maintain/distribute/download independent; forced ancestry lock applies to creator and course browse override; unlocked custom replaces browse only. Public means authenticated same tenant. SubjectResolver extension uses common grants (mock classroom member) without changing query/matcher code. Unknown resolver fails closed.
* History facts retain dataCompanyId. Current member set filters history; external customer cannot see previous-company history via SELF; own wallet-only path may show own separate company accounts but no cross-company offset/source references.

Example independently specified expectations:
```ts
assert.deepEqual(actual.teamIds, ['A','B']);
assert.equal(actual.editCFromViewAll, false);
assert.deepEqual(actual.rawPhoneSourcesForB, []);
assert.equal(actual.backendAfterLastAppointmentRevoked, false);
```
Use the actual production contract rather than creating an `actual` object of hardcoded expected booleans. Casbin must run a real model/matcher with policy rows and collect source IDs. Do not call Native then feed its final allow result into Casbin. Common semantic normalization/scope resolution is expected; clearly record what Casbin cannot replace.

- [ ] Run semantic test command RED; save full output and timestamp to evidence/raw/task1-red.txt. Missing module is acceptable first RED; add focused behavior RED for later additions.
- [ ] Implement minimal typed policy, scope and delegation functions, plus genuine engines; add only required module structure.
- [ ] Run semantic tests and typecheck; save GREEN outputs. Independently compare both candidate results against literal expected IDs/fields and report mismatches by case. Capture engine versions and small candidate microtimings, clearly separate from HTTP performance.
- [ ] Write kernel-contract.md with interfaces and consumer example; commit task files; report exact commands/results, files, unresolved requirements and limits. Do not claim AUTH-Txx overall pass based on unit tests. Do not dispatch subagents.

