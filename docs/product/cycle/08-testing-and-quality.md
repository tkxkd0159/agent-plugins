[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 08. Testing & Quality

> How do we prove it works — deterministically, and behaviorally for AI output?

---

## Test Strategy

- **Answers:** What is our overall testing approach?
- **Use when:** any non-trivial feature or system change.
- **Skip when:** trivial change covered by existing tests.
- **Owner:** QA / Engineering.
- **Key contents:** unit · integration · end-to-end · contract · load · chaos · security · regression scope · test ownership · environments.
- **Boundary:** Test Strategy = the *approach*; QA Plan / Test Cases = the *specific verifications* (below).
- **Why it matters:** "we'll add tests" is not a strategy — agents need explicit coverage targets to generate against.

## QA Plan / Acceptance Test Plan

- **Answers:** Does the system meet its acceptance criteria?
- **Use when:** behavior must be validated against the PRD ([01](01-product-and-ux.md)).
- **Skip when:** covered fully by automated tests.
- **Owner:** QA / Engineering.
- **Key contents (as executable scenarios):** test cases · acceptance criteria · test data · edge & negative cases · localization & accessibility checks · release-blocking bugs.
- **Boundary:** Test Plan = *strategy*; Test Cases = *specific behavior*. Acceptance Test Plan verifies PRD acceptance criteria.
- **Why it matters:** acceptance criteria become **executable scenario tests** (the source of truth); agents and automation replace most manual QA, so a manual smoke-test plan is a fallback, not the plan (P1, P3).

## Load Test / Benchmark Report

- **Answers:** Were the capacity and performance assumptions correct?
- **Use when:** high-scale or latency-sensitive systems, before launch.
- **Skip when:** low, predictable load.
- **Owner:** Engineering / SRE.
- **Key contents:** test environment · traffic profile · load-generation method · results · bottlenecks · latency percentiles · error rates · saturation points · remediation.
- **Boundary:** feeds Capacity Planning and SLOs ([06](06-reliability-and-scale.md)).
- **Why it matters:** agents can author load profiles and summarize results, but a human owns the go/no-go call against SLOs.

## AI Eval / Verification Plan

- **Answers:** Does AI-generated or AI-powered behavior hold up across scenarios?
- **Use when:** AI generates substantial code, or the product feature is AI-powered (LLM in the request path).
- **Skip when:** no AI output requiring behavioral assurance.
- **Owner:** Engineering / QA.
- **Key contents:** behavioral assertions · scenario suite · golden/reference cases · regression replays · failure-mode probes · acceptance thresholds · drift monitoring.
- **Boundary:** Test Plan = *deterministic* behavior; AI Eval Plan = *behavioral assertions across scenarios* (non-deterministic output). Experiment Design ([01](01-product-and-ux.md)) = *causal product impact*.
- **Why it matters:** passing unit tests is **not** sufficient to merge a large agent PR a reviewer can't line-read — evals carry the verification load downstream (P3). Don't ship AI behavior without them.

## Agent Change Review

- **Answers:** How do humans gate a change an agent generated, when nobody can line-read all of it?
- **Use when:** agents produce non-trivial code a reviewer cannot fully line-read.
- **Skip when:** the diff is small enough to read line-by-line like any human PR.
- **Owner:** Engineering (the human accountable for the merge).
- **What to review, in priority order:**
  - **the spec & plan** — do the task breakdown ([07](07-implementation-and-execution.md)) and acceptance criteria ([01](01-product-and-ux.md)) capture the intent? A correct implementation of a wrong spec is still wrong.
  - **the eval & test evidence** — did the AI Eval Plan (above) and executable tests pass, and do they cover the behavior that matters?
  - **the blast radius** — what does this touch (schemas, auth, prod write-paths, public contracts)? Scrutiny scales with blast radius, not line count.
  - **targeted spot-checks** — line-read the high-risk slices (security paths, migrations, money, deletes), not the whole diff.
- **Merge gates:** tests + evals green · blast radius within the action's autonomy level ([12](12-autonomy-and-approval.md)) · security-relevant paths human-reviewed · rollback tested ([09](09-release-and-rollout.md)).
- **Boundary:** the AI Eval Plan *produces* the behavioral evidence; this review *judges* it and decides the merge. The Autonomy & Approval Policy ([12](12-autonomy-and-approval.md)) sets what may merge without a human at all.
- **Why it matters:** "reviewers can't line-read large agent PRs" is otherwise an open loop. Review shifts from reading every line to judging spec, evidence, and blast radius — with progressive rollout ([09](09-release-and-rollout.md)) as the backstop (P3).
