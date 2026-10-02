### Spec Compliance

- ❌ Issues found: the transferred-person add path still silently accepts an existing old-company enrollment as a successful add. This misses the explicit “no silentoldA reuse” requirement in `.superpowers/sdd/2026-09-23-permission-spike/task-5-brief.md:16`; see R1 below.
- ⚠️ Cannot verify overall acceptance: actual browser behavior, four capped 50-client/600-second reference windows, and independent semantic acceptance of all 168 subcases remain controller Task6 work, as recorded at `.superpowers/sdd/2026-09-23-permission-spike/task-5-report.md:66`. The coverage map retains all 168 statuses as incomplete; citation presence and green test totals do not establish those verdicts.
- ⚠️ Performance remains unaccepted: the inspected 3-second/4-client native-hot constrained-history window already records permission p95 63.7845 ms (`evidence/raw/task5-smoke2-native-hot/summary.json:248`), above the unchanged 50 ms threshold. Other constrained smoke windows also exceed it. These observations are a material warning, while the required resource-matched reference measurement remains unexecuted.

### Strengths

- The shared export protocol checks current authority, locks the source epoch before the job, validates revision/epoch/count, hides incomplete artifacts, and bounds stored/claimed chunks to 200 rows (`src/infrastructure/protected-exports.ts:11`, `src/infrastructure/protected-exports.ts:20`). Domain readers retain authorization ownership (`src/report/exports.ts:6`, `src/training/exports.ts:6`, `src/account/service.ts:23`). Worker credentials are domain-bound and persisted jobs supply requester identity (`src/authz/export-worker.ts:6`).
- The enrollment view now uses captured names and stored company; the transfer evidence shows A viewers retaining the old name, B viewers lacking the old enrollment, and B progress/attachment requests denying (`src/training/service.ts:25`, `src/training/exports.ts:13`; `evidence/raw/task5-transfer-final.jsonl:1`, `:5`, `:7`, `:8`, `:9`, with corresponding Casbin records at `:11`, `:15`, `:17`, `:18`, `:19`).
- Signed media binds exact requester/tenant/project/segment/revision/expiry and still invokes current authorization (`src/authz/media-ticket.ts:6`, `src/training/service.ts:66`). Preserved ticket evidence includes successful use before revoke and the next denial afterward for both candidates (`evidence/raw/task5-ticket-final.jsonl:2`, `:9`, `:11`, `:18`).
- The measurement oracle is independent seed arithmetic, retains complete row/field/group results, and rejects extra fields or invalid measurement labels/timings (`scripts/benchmark-truth.ts:17`, `scripts/benchmark-observation.ts:2`). Read-only inspection of all four smoke gzip files found complete candidate/count/rowCount/digest records for every 200 response, both instances represented, and the stated hot/cold labels. The eight EXPLAIN artifacts contain actual endpoint aggregate or list-and-count SQL and bound parameters (`scripts/explain.ts:12`).
- Raw commit timelines distinguish DB and host clocks, identify the revision transaction, and show the later DB authority read observing the new revision with HTTP 403 in the other process (`evidence/raw/task5-final4-timeline.jsonl:1`, `:2`).

### Issues

#### Critical (Must Fix)

- None identified within this bounded review.

#### Important (Should Fix)

- **R1 — Reject an old-company enrollment conflict instead of reporting a new-company add as successful.** `src/training/enrollment-service.ts:33` uses `ON CONFLICT DO NOTHING`, and `:34` unconditionally returns `{changed:true,count:ids.length}`. After X's A enrollment in P is retained and X's current company becomes B, an authorized B project manager can submit `{operation:"add",personIds:["X"]}`. Current-person/company authorization admits X, the existing `(tenant,project,person)` key suppresses insertion, and the response reports success although only the old A enrollment exists. This violates the explicit Task5 requirement at `task-5-brief.md:16`; an automatic new B learning round is not needed to fix it. Under the existing authority transaction, inspect conflicting enrollment facts and reject a company-mismatched existing enrollment with safe business denial, preserving the original company/name and atomic batch behavior. Retain any intended same-company idempotence separately. Add a focused two-candidate regression: transfer X A→B, retain old A enrollment/name, grant Y the legitimate B appointment, add X as Y, expect denial/no changes, and verify A/B roster/progress/attachment/export boundaries afterward. Existing `test/task5-transfer.test.ts:13`–`:25` exercises transfer reads/exports but never this add. This is a static, deterministic finding; no new experiment was run because the controller owns the shared measurement environment.

#### Minor (Nice to Have)

- None necessary for this task gate.

### Assessment

**Task quality: Needs fixes.** The protected export, ticket and measurement work has substantial direct evidence, but the explicit transferred-enrollment contract is incomplete at its existing command call site. Repair and focused review of R1 are required before bounded Task5 approval; neither that approval nor this review establishes overall Go or formal B1.

### Checks and review boundary

- Reviewed the supplied `4851eeb64f77944de9d7028a61277f9682601544..791c478` package in bounded passes. Application commit is `750ab92`; evidence commit is `791c478`. The package's intervening controller rulings/helpers were treated according to their declared provenance, not attributed as unauthorized implementer edits (`review-4851eeb..791c478.diff:3`). The large coverage JSON was structurally decoded and all 168 requirement/status/reference summaries inspected; full per-ID semantic verdicts remain downstream.
- Named unchanged-code checks: source-epoch/lock-order interaction through `TrainingProjectionPort`, `ReportProjectionPort`, `AccountProjectionPort` and the organization mutation call sites; enrollment-snapshot command interaction through `EnrollmentService.change`. Normal owning commands acquire the authority lock before source writes. The latter check exposed R1. No broad repository crawl occurred.
- Output truncation required recovering the missing `Authority.current` diff context and the controller-document segment. No changed source file was reopened outside the supplied diff; the separately requested implementer report was read as claims/evidence guidance.
- Inspected preserved RED outputs for exports, tickets, transfer and benchmark, plus final raw suite outputs: core 53/53 (`evidence/raw/task5-final-core.txt:54`), Task3 118/118 (`task5-final-task3.txt:137`), Task4 82/82 (`task5-final-task4.txt:101`), Task5 46/46 (`task5-final4-task5.txt:57`). Final output files contain no warnings. Inspected final typecheck/build/audit outputs without rerunning commands or suites.
- Read-only parsing found 534 final Task5 literal observations with no expected/actual mismatches, 267 per candidate, and recomputed SHA256 `a14fd15f076d1d31ab027ebd10b6ffd17c5480a9b7bceec9cada9da3ce641a98` for `evidence/raw/task5-final4-task5.jsonl`. Ticket/export-scan/transfer supplements also contain matching literals. These checks validate the supplied observations, not untested behaviors such as R1.
- No API requests, DB mutations, suite reruns, process changes, index/HEAD changes, or subagents. This report is the only file written.
