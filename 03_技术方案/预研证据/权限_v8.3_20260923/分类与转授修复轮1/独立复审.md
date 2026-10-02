### Finding Verdicts

- **R1 — Original source loses recipient company:** ADDRESSED. `src/authz/role-service.ts:86` now checks the original source's company cap inside the suspension/recheck path, in addition to the acting administrator's check. Fresh final observations record suspended after removal and active after restoration for Native at `evidence/raw/task3-fix1-final-observations.jsonl:185`/`:186` and Casbin at `:217`/`:218`.
- **R2 — Recipient-relative proposal evaluated as grantor:** ADDRESSED. `src/authz/role-service.ts:21` now checks capabilities without enumerating a grantor-relative proposal; `src/authz/delegation-caps.ts:10` supplies the actual recipient context to the shared subset check. Create/edit/add/recheck and literal D2 caps pass, with empty-set field/action/delegability negatives retained (`test/task3-review-regressions.test.ts:30`; final observations `:187`–`:195` and `:219`–`:227`).
- **R3 — One-course custom browse requires every course:** ADDRESSED for the reported defect. `src/knowledge/service.ts:95` supplies the single affected course ID, and `src/authz/delegation.ts:88` returns the validated proposal cap rather than the broader source cap. Own-course success, other-uploader denial, exact persisted IDs and explicit recheck are evidenced at final observations `:196`–`:200` and `:228`–`:232`. The accompanying category generalization introduces N1 below.
- **R4 — Maintenance enumeration excludes inaccessible courses:** ADDRESSED. `src/knowledge/public.ts:5` defines the action-sensitive predicate shared by enumeration and `src/knowledge/service.ts:79`. Source/delegate maintenance and accessibility restoration succeed while browse/download deny, including after recheck (final observations `:206`–`:214` and `:238`–`:246`).

### New Breakage in the Fix Diff

- **Important N1 — Child inheritance changes can expand an ancestor's newly narrowed permission beyond its saved source cap.** `src/knowledge/service.ts:34` validates only courses whose *new* effective policy owner equals the category being edited. When a child switches from local policy to `inheritParent:true`, its courses now belong to the parent's policy, so they disappear from this validation; line 57 nevertheless commits the switch. Example: M owns parent P and child C; P contains a course uploaded by M, C contains an existing course uploaded by Z, and C initially does not inherit. This fix now correctly lets M save P's browse grant to L using a SELF-only source with a cap containing just P's course. M can then update C with `inheritParent:true`, `grants:[]` and that active source: the proposal is empty, but L immediately acquires browse through P for Z's course. There is no automatic validation/freezing of P's enlarged effective set, and catalog normalization does not intersect the saved category snapshot (`src/authz/revision.ts:123`; `src/knowledge/public.ts:21`). This is introduced by admitting narrow parent caps without protecting subsequent changes of effective policy ownership.
- **N1 correction / regression:** Before committing an inheritance/force-policy ownership change, identify every source policy whose effective object set expands and revalidate its stored original source, or freeze it atomically until explicit recheck; applying persisted caps during normalization should also prevent silent expansion. Add a real API test for both candidates: save a narrow parent policy, toggle an existing other-uploader child to inherit, then request that child's course as L immediately, without a second parent save. The current new test at `test/task3-review-regressions.test.ts:71` checks only that a *later parent save* rejects the expanded set, leaving the intervening access untested. This scenario is a static finding; it was not executed during re-review.

### Out-of-Scope Observations

- None. Intervening controller audit/helper changes remain distinct from the application fix; they are not evidence that whole-spike gates passed.

### Checks

- Read the fix package in bounded passes and the appended round-1 report. Existing RED output shows all four original child scenarios fail in both candidates (`evidence/raw/task3-fix1-red.txt:2` and `:8`), followed by 10/10 focused GREEN (`evidence/raw/task3-fix1-green1.txt:13`), 53/53 core (`evidence/raw/task3-fix1-core.txt:54`) and 112/112 domain checks (`evidence/raw/task3-fix1-domains.txt:131`). Final typecheck/build/audit output is clean; the audit reports zero vulnerabilities.
- Independently read/compared all 252 final JSONL observations: Native125/Casbin125/shared2, zero mismatches, exact SHA256 `de4c077594240616589771b5b6270568b567e84dc8a39f0b4c8764b268e6123c`; all 64 round-1 coverage-map references match their line/candidate/name. No suite or Git command was rerun.
- The only focused unchanged-code check was the N1 enforcement seam: `src/authz/revision.ts:109`–`:134`, category-related trigger declarations in `sql/schema.sql:68`–`:76`, and revision-trigger registration at `scripts/seed.ts:23`. It confirms that category flag changes bump revision but neither freeze the affected ancestor policy nor enforce its stored object snapshot. No application/DB mutation or external call was performed; only this review report was written.

### Verdict

**Fix round:** All four original findings addressed; new Important N1 remains open.

**Bounded Task3 Spec:** Issues found. **Quality:** Needs fixes. Full168/browser/performance and other deferred whole-spike gates remain pending regardless of this round.

**Report:** `.superpowers/sdd/2026-09-23-permission-spike/task-3-rereview-round1.md`.
