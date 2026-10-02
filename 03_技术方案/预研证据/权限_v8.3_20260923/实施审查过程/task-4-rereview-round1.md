### Finding Verdicts

- **R1 — Membership revocation ignores its action's target-person cap — ADDRESSED.** `src/authz/revision.ts:36` builds the target-person resource and line 45 requires a match in the actual `administration/authz.membership.revoke` plan before either target/dependent update. The existing target company check and revision-first locked plan remain in place. `test/task4-review-regressions.test.ts:24` gives M an explicitly B-capped revoke source while retaining M's broader report source; lines 31–46 verify C denies without changing C or C-child, and B succeeds with its dependent frozen. Final Native observations at `evidence/raw/task4-fix1-final-observations.jsonl:83`–87 and Casbin observations at lines 95–99 confirm those specific outcomes.
- **R2 — Attachment bytes bypass independent download capability — ADDRESSED.** `src/training/service.ts:32` now requires `training.project.download` through the existing exact-project authorization path for attachments, before the roster validation and byte read. Progress retains the existing view path; person/company/current-state checks still run. `test/task4-review-regressions.test.ts:63` checks view-only progress success and attachment denial, line 70 rejects a download source capped to Q for an attachment in P, line 76 confirms matching P-download success, and line 80 verifies download-only revocation through instance A denies instance B's next attachment request while progress remains accessible. Final Native observations at `evidence/raw/task4-fix1-final-observations.jsonl:88`–94 and Casbin observations at lines 100–106 confirm the action, project-scope, positive-control, and next-request cases.

### New Breakage in the Fix Diff

- **None identified.** The production diff is limited to the pre-mutation target-cap guard in `src/authz/revision.ts:36` and the attachment-specific action check in `src/training/service.ts:32`. The fixes reuse central scope matching and project authorization, preserve the existing transaction/Redis authority paths, and do not weaken company predicates or change progress authorization.
- **Tests meaningfully cover the repairs.** `test/task4-review-regressions.test.ts:33` compares full target/dependent data and source records after denied revocation, then checks literal lifecycle values. Its R2 controls separate view and download memberships and preserve view access after revoking only download; the tests do not mask a blanket-deny implementation.

### Out-of-Scope Observations

- **No new observations.** The previous Minor dense-formatting note remains nonblocking and deferred; no broad cleanup was required by this fix round.
- **Prior cannot-verify boundaries retained.** Full 168-subcase semantic acceptance, remaining protected/chunked exports and export/cache/log sweeps, full fault/race and exact commit-timestamp campaigns, UI/browser, independent deployment, and resource-matched performance remain Tasks5/6 (`docs/task4-ports.md:15`). This re-review neither closes nor waives them. The original 168 checklist entries remain marked incomplete.

### Evidence Checks

- **Scope checked:** supplied fix package for `9252b46af14039207b894b8bd5ac021ec64f057e` → `4851eeb64f77944de9d7028a61277f9682601544`, appended fix report, original Task4 requirements/global constraints, and original R1/R2 findings. The package's controller-only ADR-note commit `a14098d` is not treated as an implementer scope violation. No untouched code was re-reviewed.
- **Actual RED retained:** `evidence/raw/task4-fix1-red.txt` reports 18 test nodes, 4 passing and 14 failing including parent nodes. The raw RED JSONL contains 20 observations and 10 mismatches: B-only revoke succeeds incorrectly against C and changes target/dependent state, and view-only/other-project/revoked-download attachments return bytes, in both candidates. Existing positive controls pass. These are defect reproductions, not inferred failures.
- **Focused GREEN confirmed from saved output:** `evidence/raw/task4-fix1-green.txt:23` reports 18/18, with 24 JSONL observations and zero differences. The later affected-domain run at `evidence/raw/task4-fix1-domains.txt:49` reports 40/40 and exercises the repair tests plus adjacent person/company-source, mixed-company project, two-instance download/revoke, and real Redis timeout paths. Counts are evidence indexing, not acceptance denominators.
- **Ordering regression evidence confirmed:** `evidence/raw/task4-fix1-core.txt:1`–17 names snapshot/revoke checks, both write/revoke orders, waiting readers seeing fresh department/company/disabled/deleted facts, and rejection of unmarked transaction clients; the saved summary reports 17/17. No suite was rerun by this reviewer.
- **Literal observations checked:** all 108 final rows compare equal between expected and actual (Native 54, Casbin 54). Independently computed SHA256 is `af88a28e40287be66d73089e0373b7f92c4096cdb1ab11cdb828bf9605df41eb`, matching the appended report. The 24 focused coverage references resolve to the exact candidate/name at the stated final JSONL line; the original 266-reference map and all 168 incomplete checklist entries remain present.
- **Build/audit output inspected:** `evidence/raw/task4-fix1-typecheck.txt:2` and `task4-fix1-build.txt:2` contain the reported commands without diagnostics; `task4-fix1-audit.json` reports zero vulnerabilities. The checked RED/GREEN/covering/build logs contain no warning or unhandled-error lines. `task4-fix1-api-processes.txt` is empty, consistent with the reported no-listener check; the reviewer did not start or inspect live APIs.
- **Timing interpretation preserved:** the next-request test compares B's request time with A's completed HTTP response (`test/task4-review-regressions.test.ts:84`); this establishes the tested request follows acknowledgment and is not represented as an exact DB commit-timestamp measurement.
- **Read-only boundary observed:** no tests, APIs, DB mutations, settings changes, code/index/branch changes, git commands, or subagents. This re-review artifact is the only reviewer write.

### Verdict

**Fix round:** All findings addressed, no new Critical/Important breakage. R1 and R2 are closed for this bounded Task4 milestone.

**Bounded spec compliance:** Approved, with the prior Tasks5/6 cannot-verify obligations explicitly retained.

**Task quality:** Approved for this fix round and bounded Task4 milestone. This is not full-168 acceptance, an overall permission Go, or formal B1 authorization.
