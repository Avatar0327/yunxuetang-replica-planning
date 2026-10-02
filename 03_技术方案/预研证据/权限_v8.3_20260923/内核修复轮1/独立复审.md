# Task 1 fix round 1 re-review — 72adfaa..b7e31f6

**Finding verdict: ADDRESSED.** `src/authz/policy.ts:81-84` now admits the `ownWallet` company-cap exception only when the account belongs to the actor, `dataCompanyId` is a nonempty string after trimming, and `crossCompanyReference` is explicitly `false`. Missing company or reference facts therefore fail closed. The ordinary company cap is still bypassed for a known safe own account from an old company, as T-15 requires.

The fix adds literal cases for both Native and Casbin at `test/semantic.test.ts:267-285`: the known CA account is allowed for a customer currently in CB; missing, empty and blank company IDs, missing reference status, and the original unbound account are denied. The earlier old-company fixture also now supplies `crossCompanyReference: false` at `test/semantic.test.ts:149`. The implementer report records focused RED (2 pass, 10 fail), focused GREEN (12 pass), full semantic (26 pass), and typecheck success in `evidence/raw/task1-fix-round1-{red,green,semantic,typecheck}.txt`. I did not rerun these commands, per the scoped review instruction.

**New breakage in the fix diff:** none identified. Only the wallet predicate, corresponding test facts/cases, and contract wording changed. The predicate continues to reject cross-company references and preserves the known old-company account path.

**Out of scope:** The kernel still relies on authoritative account-company and reference facts supplied by its caller. SQL/serialization separation of accounts and prevention of cross-company offsets, as well as HTTP, two-instance, UI and performance evidence, remain Task 2/integration concerns; this re-review makes no overall AUTH-Txx claim. The unrelated untracked Docker, acceptance and tools files visible in the workspace were not changed or assessed.

**Round verdict: ACCEPT this bounded fix.** Read the supplied fix diff once and inspected only the relevant current lines; no branch, index or code changes, test reruns, or subagents.
