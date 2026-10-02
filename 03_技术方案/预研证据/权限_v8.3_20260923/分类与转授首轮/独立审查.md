### Spec Compliance

- ❌ Issues found: original-source company revalidation and exact recipient/resource-set semantics remain incorrect in this Task3 milestone; see four Important findings below. This is not whole-spike approval.
- ⚠️ Full 168-case acceptance, independent deployment, browser, production media/export and long performance gates remain unverified, as explicitly recorded in `docs/task3-ports.md:24` and `.superpowers/sdd/2026-09-23-permission-spike/task-3-report.md:89`. Their deferral does not excuse the Task3 behavior defects below.

### Strengths

- Revision-only locking precedes fresh facts and fencing in `src/authz/revision.ts:53`; existing waiting-lock regressions remain evidenced at `evidence/raw/task3-core-regression-final2.txt:11` and `:18`. Facts/projection extraction preserves the same transaction client, and report enumeration uses only report-owned relations (`src/report/public.ts:11`).
- Genuine two-process timeout/recovery/revoke observations exist at `evidence/raw/task3-final-observations2.jsonl:86` through `:96`, with no protected bytes on denial. The report correctly describes HTTP completion as an upper bound on commit time.
- Existing final output records 53/53 core tests and 100/100 domain tests, with zero failures (`evidence/raw/task3-core-regression-final2.txt:54`, `evidence/raw/task3-domains-final2.txt:117`). Read-only verification confirmed all 188 literal observations, the reported SHA256, zero expected/actual mismatches, and all evidence references in the 34-subcase coverage map (`docs/task3-coverage.json:5`). Final typecheck/build/audit output is clean; audit reports zero vulnerabilities.

### Issues

#### Critical (Must Fix)

- None identified in this bounded review.

#### Important (Should Fix)

1. **Recheck can revive a delegation after its original source loses the target company.** `src/authz/role-service.ts:83` reads the original source context, but lines 86–89 reactivate without checking that source's current company cap against the recipient. Line 76 checks only the rechecking actor. For example, M can originally assign a shared-course role to customer-A user X while M has the A company grant; removing that grant freezes the dependent role, but broad administrator Z can recheck it back to active under M's original source. Shared-course object resolution does not apply a company predicate, so it cannot catch this. Require both the acting recheck authorization and the original source's current recipient-company ceiling, persisting `suspended` when the latter fails. Add the company-grant revoke → broad-admin recheck → still suspended regression for both candidates, then a positive restore case. The existing test at `test/task3-role-company.test.ts:12` covers only the rechecking actor's cap.

2. **Recipient-relative scopes are first rejected using the grantor's department/SELF anchor.** `src/authz/role-service.ts:21` calls `assertCanDelegate` with the source context and proposed role scopes before line 27 evaluates the actual recipient. The same ordering appears in edit/add-member/recheck. A source actor in D1 with an explicitly delegable D2 permission cannot assign `ownDept` to a recipient in D2: the preliminary check resolves the proposal as D1 and rejects, even though the recipient's entire D2 set is within the selected source. The unchanged helper confirms this context binding at `src/authz/delegation.ts:41`. Separate level/action/delegability validation from proposed object resolution, and compare each recipient's actual proposed set against the source's actual cap without requiring the grantor-relative proposal to pass as well. Keep empty-set field/action validation. Add positive D1-grantor/D2-cap/D2-recipient coverage alongside the existing expansion-negative test.

3. **One-course custom browse changes require authority over every course.** `src/knowledge/service.ts:24` hardcodes every proposed catalog grant to `scope: {kind:'all'}`; `customBrowse` calls it at line 89 without passing the target course. A source explicitly allowed to maintain and delegate browse for its own uploaded course therefore cannot customize that course when another published course exists outside its SELF cap. This fails the actual-object-set ceiling requirement by comparing unrelated objects. Pass the affected course/category object set into the central subset check and persist the corresponding cap; a custom browse mutation should compare its single course. Add a positive selected-SELF own-course case and a negative other-uploader case for both candidates.

4. **Delegation's course object set disagrees with live maintenance authorization.** `src/knowledge/public.ts:6` always filters `accessible=true`, while `src/knowledge/service.ts:73` intentionally omits that filter for `knowledge.course.maintain`. Consequently, delegating maintenance omits inaccessible courses that the source can maintain; the recipient's persisted cap prevents maintaining or restoring those courses even after a valid recheck. Use identical action-sensitive state predicates in enumeration and the live resource query, preferably via a shared helper. Add an inaccessible-course case proving source and delegated recipient can maintain it while browse/download remain denied.

#### Minor (Nice to Have)

- None needed beyond the corrective coverage above.

### Assessment

**Task quality:** Needs fixes.

**Reasoning:** The ports, transaction ordering and observed regressions are well supported, but the exact-set and source-preservation guarantees still have concrete gaps. The four scenarios above are static code findings, not newly executed test results.

**Checks performed:** Read the packaged diff in manageable passes; decoded its coverage-map addition and cross-checked every referenced raw record; inspected the existing final outputs and the reported RED artifacts. The sole unchanged-code inspection was `src/authz/delegation.ts:17`–`:69`, specifically to determine whether central validation compensates for the missing source-company check and how it binds proposed relative scopes. No Git commands, test reruns, external calls or application mutations were performed. Only this review report was written.

**Report:** `.superpowers/sdd/2026-09-23-permission-spike/task-3-review.md`.
