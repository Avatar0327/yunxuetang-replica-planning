# Task 1 review — 2d21695..72adfaa

Spec compliance: CHANGES REQUESTED.
Task code quality: CHANGES REQUESTED (one bounded fail-closed defect).

Scope: reviewed the supplied task brief, implementer report, full supplied diff once in chunks, and relevant 04 specification passages. No broader code review, code/index/branch changes, subagents, or existing-suite reruns. One targeted in-memory counterexample was run because the reported tests do not cover missing wallet hard facts.

## Finding

**[P2] Require complete wallet hard facts before applying the company-cap exception — `src/authz/policy.ts:81–82`**

The ownWallet branch authorizes `personId === actor` when `crossCompanyReference` is missing, and never requires `dataCompanyId`. Both properties are optional in the public Resource contract (`src/authz/contracts.ts:112,122`), so this occurs with a valid typed Resource, without forged grant objects or a dishonest organization resolver. An own account whose company identity and reference status are unknown receives an allow result from both candidates. T-07/T-15 permit viewing company-separated own accounts; the binding instruction requires unknown hard facts to fail closed. This exception currently admits an account that cannot even be bound to a company and treats unknown reference status as safe.

Require an authoritative nonempty dataCompanyId and an explicitly safe reference fact before allowing this branch (a discriminated wallet fact type is another option). Preserve the intended ability to view one's known separate accounts outside the current company cap. Add literal positive known-account and negative missing-company/missing-reference cases to both candidates. This request concerns the pure predicate only, not Task2 financial serialization or cross-company accounting implementation.

Targeted evidence: `PATH=/opt/homebrew/opt/node@24/bin:$PATH node --import tsx --input-type=module` with existing ctx/nodes/org fixtures, a normalized SELF wallet membership, and resource `{id:'unbound-account',tenantId:'T1',type:'account',personId:'M',exists:true,enabled:true,deleted:false}`. Both Native and Casbin returned `allowed:true`, source `role:wallet:wallet-own:account.own.view`, rawFields `[]`, revision `7`. No dataCompanyId or crossCompanyReference was supplied. This is outside the reported positive-wallet and `crossCompanyReference:true` tests and confirms the finding directly.

## Other assessment

The implementation carries source identity through matching and only unions fields from matching sources. Role-local overrides, selected membership delegation and create/edit level distinctions are represented directly. Casbin executes an actual model with policy rows and a source scope predicate; it does not consume Native's final allow decision. Bulk planning keeps source-specific resolved scopes/fields and explicitly delegates trusted object/company/status resolution to owning ports. No additional concrete defect was identified within those intended trust boundaries.

The reported semantic/typecheck success is consistent with the supplied tests; it is not independently rerun or promoted to SQL, HTTP, two-instance revocation, UI, performance, or any overall AUTH-Txx pass. The report and kernel contract appropriately reserve those integration claims. Fix the wallet predicate and add focused evidence before accepting Task1's fail-closed semantics.
