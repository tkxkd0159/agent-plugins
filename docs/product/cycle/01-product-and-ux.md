[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 01. Product & UX

> Why are we building this, what behavior do we want, and how will we know it worked?

**Badge legend:** `Core` default · `Elevated` higher-leverage with AI · `Conditional` trigger-gated · `Executable` prefer machine-readable form · `Merged` synonym/folded · `AI-native` new in AI-driven workflows. See [AI-era principles](ai-era-principles.md).

---

## PRD — Product Requirements Document `Core` `Elevated`

- **Answers:** Why are we building this, and what product behavior do we want?
- **Use when:** new product, major feature, or high-impact user-facing change.
- **Skip when:** small, local, reversible work — a ticket with acceptance criteria is enough.
- **Owner:** PM.
- **Key contents:** problem statement · goals / non-goals · target users · main flows · **acceptance criteria as concrete examples** · **anti-requirements (explicitly out of scope)** · success metrics · dependencies · open questions · launch criteria.
- **Boundary:** PRD = product *outcomes and intent*. SRS = formal testable shall-statements ([02](02-requirements.md)). BRD = business *justification* (below). Implementation lives in [03](03-architecture-and-design.md), not here.
- **In AI-driven workflows:** the acceptance criteria + concrete examples + anti-requirements are the part that actually drives autonomous implementation; prose intent without testable examples produces confidently-wrong code (P3). Keep agent *operating instructions* out of the PRD — those belong in the Agent Operating Manual ([07](07-implementation-and-execution.md)).

## Business Case / BRD `Conditional`

- **Answers:** Is this worth funding, and why?
- **Use when:** large, expensive, or cross-org initiatives.
- **Skip when:** small bets — cheap implementation means building-to-test often beats writing a case.
- **Owner:** Business / Product.
- **Key contents:** opportunity · expected impact · cost estimate · risk of not doing it · build / buy / partner · staffing · long-term ownership.
- **Boundary:** BRD = *why fund it*. PRD = *what to build*.
- **In AI-driven workflows:** the bar **rises** — lower build cost shifts build-vs-buy toward build and answers many questions with a spike. Reserve for genuinely expensive or irreversible commitments (P2).

## UX / Design Spec `Core` `Conditional`

- **Answers:** What is the user-facing behavior, in detail?
- **Use when:** UX is complex or uncertain; many interaction states; cross-platform behavior.
- **Skip when:** trivial or pattern-covered UI.
- **Owner:** Design.
- **Key contents:** journeys · wireframes / Figma links · interaction, empty, loading, and error states · accessibility · localization · design-system components.
- **Boundary:** wireframes show the *experience*; requirements (PRD / acceptance criteria) define *required behavior*. Do not treat mockups as the contract.
- **In AI-driven workflows:** agents generate UI from prompts, so durable value moves from pixel-perfect handoff to a **machine-readable design system + interaction principles + explicit states** that constrain generation (P1).

## Success Metrics `Core`

- **Answers:** How will we know it worked?
- **Use when:** any PRD with a measurable goal.
- **Skip when:** no measurable outcome (rare; reconsider the work).
- **Owner:** PM.
- **Key contents:** primary KPI · guardrail metrics · target value + measurement window.
- **Boundary:** Success Metrics = *product outcome* targets. SLOs = *reliability* targets ([06](06-reliability-and-scale.md)). Analytics Spec = how they are *instrumented* (below).
- **In AI-driven workflows:** clear targets + cheap variant-building make experimentation the default way to resolve product uncertainty.

## Analytics / Metrics Spec `Elevated` `Executable`

- **Answers:** What exactly do we log, and how?
- **Use when:** any feature whose success or guardrail metrics must be measured.
- **Skip when:** no measurable goal.
- **Owner:** PM / Data + Engineering.
- **Key contents:** events + schema · funnels · KPIs · guardrail metrics · dashboards · data owners · data-quality checks.
- **Boundary:** Success Metrics = the *targets*; Analytics Spec = the *instrumentation* that produces them.
- **In AI-driven workflows:** prefer event schemas **as code** (typed, validated). You cannot run evals or experiments without clean instrumentation (P1).

## Experiment Design `Elevated`

- **Answers:** Does the change causally move the metric?
- **Use when:** A/B tests, feature ramps with uncertain impact.
- **Skip when:** effect is obvious or non-measurable, or rollout is non-experimental.
- **Owner:** PM / Data.
- **Key contents:** hypothesis · population · control / treatment · randomization unit · metrics + guardrails · duration / sample size · ramp plan · decision criteria.
- **Boundary:** Experiment Design = *causal product* validation. AI Eval Plan ([08](08-testing-and-quality.md)) = behavioral correctness of AI output. Test Plan ([08](08-testing-and-quality.md)) = deterministic correctness.
- **In AI-driven workflows:** cheap variant generation makes experimentation the primary tool for product decisions (P2: empirical beats predictive).
