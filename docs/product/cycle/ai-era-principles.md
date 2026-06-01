[← Back to index & glossary](../PRODUCT_CYCLE.md)

# AI-Era Documentation Principles

> The reasoning behind every verdict in this system. Read this once to understand *why* each document is treated the way it is.

This system assumes a world where AI agents do substantial implementation. Implementation and rework are cheap, so building-to-learn often beats predicting on paper. The binding constraint is no longer *"can we build it"* but *"did it do the right thing, and can we verify that."* Documentation exists to sharpen intent, externalize decisions, and make verification possible — not to coordinate large human teams. Everything below follows from that.

---

## The five principles

Every document's `Why it matters` note derives from one of these.

### P1 — Prefer executable artifacts over prose
Where a document can be machine-readable (OpenAPI, schema migrations, test-as-spec, eval suites, SLO-as-config, runbook-as-YAML, devcontainer), **that** is the source of truth; the prose shrinks to intent plus a pointer. Agents consume and generate from executable artifacts and can be *verified* against them. Prose drifts, and an agent cannot check itself against it.

### P2 — Bias to empirical iteration over predictive design (for reversible work)
Implementation and rework are cheap, so **spike with an agent, then capture what survived** in a thin design plus an ADR — this beats heavy upfront design. Reserve heavy design for irreversible, high-blast-radius, or cross-team work. Prediction is expensive and often wrong; iteration is cheap.

### P3 — Tighten intent upstream, verify hard downstream
Vague intent becomes confidently-wrong code *fast*. The upstream spec is the agent's actual **instruction set** — treat it as such, not as background prose:

- **acceptance criteria as concrete examples** — the behavior the agent must produce, written as checks;
- **anti-requirements** — what is explicitly out of scope, fencing off the confident over-building agents do by default;
- **executable interface and data contracts** (OpenAPI, migrations) — the boundaries the implementation must satisfy.

Anything in the spec that cannot be reduced to a check is a wish, not a requirement, and produces plausible-but-wrong output. Downstream, **evals, scenario replays, and progressive rollout** carry the assurance that prose specs and manual QA once did. Ambiguity is the earliest and most expensive defect.

### P4 — Externalize decisions and conventions; agents have no memory
Agents start every session blank. Anything not written down is invisible and gets re-derived, often wrongly. Two artifacts carry the load, and context is a third discipline:

- **ADRs** record durable decisions so they are never re-litigated;
- the **Agent Operating Manual** holds repo conventions — the standing context every task inherits;
- **context is engineered per task** — deliberately assemble the relevant ADRs, contracts, and code into the agent's working set rather than hoping it rediscovers them, and keep that memory retrievable as the system grows.

Undocumented context is not "tribal knowledge" here; it simply does not exist for the agent.

### P5 — Watch for generated-documentation theater
Agents mass-produce plausible, wrong, unmaintained docs cheaply. Every document still needs an owner who *verifies* it. Never auto-generate-and-forget. This is the guardrail that keeps the system from bloating itself with documentation nobody trusts.

---

## The economics this system assumes

- **Implementation is cheap and fast** — vagueness becomes confidently-wrong artifacts, not slow progress.
- **Rework is cheap** — empirical iteration with crisp acceptance criteria beats heavy upfront prediction.
- **Ambiguity is the binding constraint** — its cost moved upstream and grew.
- **Agents have no memory** — anything undocumented is re-derived every session.
- **Large agent-generated PRs cannot be line-read** — evals and progressive rollout carry verification.
- **Teams are smaller and agent-assisted** — less coordination paperwork is needed; the question that matters is "did it do the right thing, and can we verify that?"

## Where to invest

PRD acceptance criteria + anti-requirements · ADRs · [Agent Operating Manual](07-implementation-and-execution.md) · [AI Eval / Verification Plan](08-testing-and-quality.md) · executable test cases · [Observability Spec](10-operations-and-observability.md) · [Threat Model](05-security-privacy-compliance.md) (AI-extended) · progressive [Rollout + Rollback](09-release-and-rollout.md) · [Autonomy & Approval Policy](12-autonomy-and-approval.md).

## Use sparingly

Long-form prose specifications · standalone prose Non-Functional Requirements · heavyweight SRS without compliance pressure · manual QA smoke-test plans · status / activity reports · heavy RACI matrices · heavy static execution plans.

## Enduring rules

- Business case, launch plan, runbook, incident review, and postmortem still matter.
- Empirical iteration beats prediction — but disciplined intent and verification still gate it.
- Document boundaries stay sharp: PRD ≠ SRS ≠ Technical Design; Postmortem ≠ Retrospective; Threat Model ≠ Security Review.

## Common anti-patterns

- Adopting SRS to solve AI ambiguity. SRS solves audit traceability; acceptance criteria + evals solve ambiguity.
- Treating long Markdown as agent context. Length is not rigor.
- Skipping the Agent Operating Manual when agents operate in the codebase.
- Merging agent-generated code with no eval plan just because unit tests pass.
- Mixing agent operating instructions into the PRD.
- Letting agents auto-generate docs nobody owns or verifies (P5).
- Giving agents autonomy without an Autonomy & Approval Policy and audit trail.

---

## The default flow

```text
PRD with acceptance criteria + anti-requirements
→ ADR for durable decisions
→ Agent Operating Manual at the repo root
→ Autonomy & Approval Policy (if agents take actions)
→ Technical Design Doc if implementation is non-trivial
→ Executable interface/data contracts (OpenAPI, migrations)
→ Agent-executable task plan (atomic + verifiable)
→ Test cases as executable specification
→ AI Eval Plan if AI generates substantial code or powers the feature
→ Progressive Rollout + tested Rollback
→ Observability Spec + Runbook for production-critical work
→ Postmortem (async, technical) → Retrospective (periodic, human/process)
```

Add SRS, heavyweight NFR docs, or heavy execution plans only when audit, compliance, contract, or program scale requires them. Drop the middle stages when the work is small, local, and reversible.
