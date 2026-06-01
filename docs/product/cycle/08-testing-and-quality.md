[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 08. Testing & Quality

> How do we prove it works — deterministically, and behaviorally for AI output?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

---

## Test Strategy `Core`

- **Answers:** What is our overall testing approach?
- **Use when:** any non-trivial feature or system change.
- **Skip when:** trivial change covered by existing tests.
- **Owner:** QA / Engineering.
- **Key contents:** unit · integration · end-to-end · contract · load · chaos · security · regression scope · test ownership · environments.
- **Boundary:** Test Strategy = the *approach*; QA Plan / Test Cases = the *specific verifications* (below).
- **In AI-driven workflows:** "we'll add tests" is not a strategy — agents need explicit coverage targets to generate against.

## QA Plan / Acceptance Test Plan `Core` `Executable`

- **Answers:** Does the system meet its acceptance criteria?
- **Use when:** behavior must be validated against the PRD ([01](01-product-and-ux.md)).
- **Skip when:** covered fully by automated tests.
- **Owner:** QA / Engineering.
- **Key contents (as executable scenarios):** test cases · acceptance criteria · test data · edge & negative cases · localization & accessibility checks · release-blocking bugs.
- **Boundary:** Test Plan = *strategy*; Test Cases = *specific behavior*. Acceptance Test Plan verifies PRD acceptance criteria.
- **In AI-driven workflows:** acceptance criteria become **executable scenario tests** (the source of truth), and manual smoke-test plans are **demoted** — agents and automation replace most manual QA (P1, P3).

## Load Test / Benchmark Report `Conditional`

- **Answers:** Were the capacity and performance assumptions correct?
- **Use when:** high-scale or latency-sensitive systems, before launch.
- **Skip when:** low, predictable load.
- **Owner:** Engineering / SRE.
- **Key contents:** test environment · traffic profile · load-generation method · results · bottlenecks · latency percentiles · error rates · saturation points · remediation.
- **Boundary:** feeds Capacity Planning and SLOs ([06](06-reliability-and-scale.md)).
- **In AI-driven workflows:** agents can author load profiles and summarize results, but a human owns the go/no-go call against SLOs.

## AI Eval / Verification Plan `AI-native` `Elevated`

- **Answers:** Does AI-generated or AI-powered behavior hold up across scenarios?
- **Use when:** AI generates substantial code, or the product feature is AI-powered (LLM in the request path).
- **Skip when:** no AI output requiring behavioral assurance.
- **Owner:** Engineering / QA.
- **Key contents:** behavioral assertions · scenario suite · golden/reference cases · regression replays · failure-mode probes · acceptance thresholds · drift monitoring.
- **Boundary:** Test Plan = *deterministic* behavior; AI Eval Plan = *behavioral assertions across scenarios* (non-deterministic output). Experiment Design ([01](01-product-and-ux.md)) = *causal product impact*.
- **In AI-driven workflows:** unit tests passing is **not** sufficient to merge large agent PRs reviewers can't line-read — evals carry the verification load downstream (P3). Don't ship AI behavior without them.
