[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 01. Product & UX

> Why are we building this, what behavior do we want, and how will we know it worked?

---

## PRD — Product Requirements Document

- **Answers:** Why are we building this, and what product behavior do we want?
- **Use when:** new product, major feature, or high-impact user-facing change.
- **Skip when:** small, local, reversible work — a ticket with acceptance criteria is enough.
- **Owner:** PM.
- **Key contents:** problem statement · goals / non-goals · target users · main flows · **acceptance criteria as concrete examples** · **anti-requirements (explicitly out of scope)** · success metrics · dependencies · open questions · launch criteria.
- **Boundary:** PRD = product *outcomes and intent*. SRS = formal testable shall-statements ([02](02-requirements.md)). BRD = business *justification* (below). Implementation lives in [03](03-architecture-and-design.md), not here.
- **Why it matters:** the acceptance criteria + concrete examples + anti-requirements **are the agent's instruction set** — the part that actually drives autonomous implementation. Prose intent that can't be reduced to a check produces confidently-wrong code (P3). Keep agent *operating instructions* out of the PRD — those belong in the Agent Operating Manual ([07](07-implementation-and-execution.md)).

## Business Case / BRD

- **Answers:** Is this worth funding, and why?
- **Use when:** large, expensive, or cross-org initiatives.
- **Skip when:** small bets — cheap implementation means building-to-test often beats writing a case.
- **Owner:** Business / Product.
- **Key contents:** opportunity · expected impact · cost estimate · risk of not doing it · build / buy / partner · staffing · long-term ownership.
- **Boundary:** BRD = *why fund it*. PRD = *what to build*.
- **Why it matters:** cheap implementation shifts build-vs-buy toward build and answers many questions with a spike, so reserve a full case for genuinely expensive or irreversible commitments (P2).

## UX / Design Spec

- **Answers:** What is the user-facing behavior, in detail?
- **Use when:** UX is complex or uncertain; many interaction states; cross-platform behavior.
- **Skip when:** trivial or pattern-covered UI.
- **Owner:** Design.
- **Key contents:** journeys · wireframes / Figma links · interaction, empty, loading, and error states · accessibility · localization · design-system components.
- **Boundary:** wireframes show the *experience*; requirements (PRD / acceptance criteria) define *required behavior*. Do not treat mockups as the contract.
- **Why it matters:** agents generate UI from prompts, so durable value is a **machine-readable design system + interaction principles + explicit states** that constrain generation (P1), not pixel-perfect handoff.

## Success Metrics

- **Answers:** How will we know it worked?
- **Use when:** any PRD with a measurable goal.
- **Skip when:** no measurable outcome (rare; reconsider the work).
- **Owner:** PM.
- **Key contents:** primary KPI · guardrail metrics · target value + measurement window.
- **Boundary:** Success Metrics = *product outcome* targets. SLOs = *reliability* targets ([06](06-reliability-and-scale.md)). Analytics Spec = how they are *instrumented* (below).
- **Why it matters:** clear targets + cheap variant-building make experimentation the default way to resolve product uncertainty.

## Analytics / Metrics Spec

- **Answers:** What exactly do we log, and how?
- **Use when:** any feature whose success or guardrail metrics must be measured.
- **Skip when:** no measurable goal.
- **Owner:** PM / Data + Engineering.
- **Key contents:** events + schema · funnels · KPIs · guardrail metrics · dashboards · data owners · data-quality checks.
- **Boundary:** Success Metrics = the *targets*; Analytics Spec = the *instrumentation* that produces them.
- **Why it matters:** prefer event schemas **as code** (typed, validated). You cannot run evals or experiments without clean instrumentation (P1).

## Experiment Design

- **Answers:** Does the change causally move the metric?
- **Use when:** A/B tests, feature ramps with uncertain impact.
- **Skip when:** effect is obvious or non-measurable, or rollout is non-experimental.
- **Owner:** PM / Data.
- **Key contents:** hypothesis · population · control / treatment · randomization unit · metrics + guardrails · duration / sample size · ramp plan · decision criteria.
- **Boundary:** Experiment Design = *causal product* validation. AI Eval Plan ([08](08-testing-and-quality.md)) = behavioral correctness of AI output. Test Plan ([08](08-testing-and-quality.md)) = deterministic correctness.
- **Why it matters:** cheap variant generation makes experimentation the primary tool for product decisions (P2: empirical beats predictive).
