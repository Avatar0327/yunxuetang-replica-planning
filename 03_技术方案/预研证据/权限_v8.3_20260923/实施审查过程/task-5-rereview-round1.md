### Spec Compliance

- ✅ **R1: ADDRESSED.** In `src/training/enrollment-service.ts:36`, the add path now checks existing enrollment company against the current person projection after current target authorization and before any insertion. A mismatch throws `Denied` at `:37`; the existing transaction and tenant authority lock preserve whole-batch rejection. The check is shared by project-appointment and direct-team authorization paths. Existing immutable company/name/progress/attachment are preserved, and same-company idempotence remains at `:39`.
- ✅ The fix satisfies the original Task5 “no silentoldA reuse” requirement without introducing a new learning-round engine or changing the successful same-company response contract (`.superpowers/sdd/2026-09-23-permission-spike/task-5-brief.md:16`; `src/training/enrollment-service.ts:33`).

### Strengths

- `test/task5-enrollment-conflict.test.ts:36` checks both singleton X and mixed W/X/Y requests using a legitimately appointed B manager after X transfers A→B. The expected 403 body is literal and safe; complete original enrollment rows plus unchanged revision/export epoch are asserted. This detects both false success and partial insertion.
- A/B/internal list/count/search/progress/attachment/export outcomes remain literal and exercise the actual HTTP paths (`test/task5-enrollment-conflict.test.ts:45`). Repeated same-company Y/W additions verify one fresh enrollment and preservation of existing snapshots/progress (`:67`).

### Evidence Checked

- **Actual RED2 confirmed:** `evidence/raw/task5-fix-round1-red2.jsonl:8` and `:29` record the singleton's erroneous 200/count1; `:9` and `:30` record erroneous 200/count3, a newly inserted W, and changed revision/epoch. Subsequent B-roster mismatches appear at `:17` and `:38`. The raw Node output reports 10 entries, 2 passing and 8 failing, including parent failures (`evidence/raw/task5-fix-round1-red2.txt:13`). These are concrete behavior failures, not missing-test assertions.
- **Focused GREEN confirmed:** raw output reports **10/10**, zero failures (`evidence/raw/task5-fix-round1-green.txt:13`). Singleton and mixed requests now return 403 with unchanged complete roster/revision/epoch (`task5-fix-round1-green.jsonl:8`, `:9`, `:42`, `:43`). Same-company additions remain successful (`:31`, `:33`, `:65`, `:67`). Read-only parsing checked all **68** literal observations, **34 per candidate**, with zero mismatches.
- **Related campaign confirmed:** `evidence/raw/task5-fix-round1-regressions.txt:43` reports **36/36**, zero failures, covering module boundaries, direct-team paths, two-instance fault/revoke ordering, prior membership/attachment fixes, and transfer behavior. Read-only parsing checked all **164** literal observations, **82 per candidate**, with zero mismatches. The R1 denial observations recur at `task5-fix-round1-regressions.jsonl:84`, `:85`, `:118`, `:119`.
- Recomputed JSONL SHA256 values match the supplied audit: focused GREEN `70eff0002bb2e4cca921779098fecaa25cc426a3c6886ca23d31870c657dd0c9`; related campaign `a6641526aeebc021cebcee5e8afea5417af9be7d9c83d62a4259cafc43a6d883` (`evidence/raw/task5-fix-round1-observation-audit.json:1`). Inspected typecheck/build outputs contain no diagnostics, and the inspected final test outputs contain no warnings.

### Issues

- **New issues introduced by this fix: none identified.** The added comparison is tenant/project/target-bound, runs before writes, and preserves the previously reviewed owning-command lock order (`src/training/enrollment-service.ts:36`). This review does not extend that serialization guarantee to arbitrary raw DB writers.
- ⚠️ **Existing mixed-ID sorting rejection remains unresolved and outside this round**, as explicitly assigned to final whole-branch review. The production comparison at `src/training/enrollment-service.ts:28` is unchanged; the fixture adjustment to uppercase W and the preserved original failure are disclosed in `task-5-fix-round1-report.md:49`. R1 approval does not waive that separate correctness defect.

### Assessment

**Task quality: Approved for the bounded R1 fix.** The original Task5 blocking finding is addressed with direct RED/GREEN evidence and appropriate related regression coverage. No additional fix-introduced blocker was found.

- ⚠️ Overall 168-subcase semantic acceptance, actual browser acceptance, capped 50-client/600-second reference performance, overall Go and formal B1 remain independent and unapproved by this review (`task-5-fix-round1-report.md:63`).
- Review scope: supplied `791c478..4ca6cc4` package, application commit `9fb9975`, and cited raw evidence. No DB/API/test/container commands, HEAD/index/source edits, or subagents were used. This rereview report is the only file written.
