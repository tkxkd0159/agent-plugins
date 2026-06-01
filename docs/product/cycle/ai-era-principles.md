[← Back to index & glossary](../PRODUCT_CYCLE.md)

# AI-Era Documentation Principles

> The reasoning behind every verdict in this system. Read this to understand *why* the catalog is treated the way it is.

The traditional 44-document catalog is priced for a world of large human teams and slow, expensive implementation. AI changes both inputs: implementation and rework are cheap, cross-human coordination paperwork is less necessary, and the binding constraint moves from *"can we build it"* to *"did it do the right thing, and can we verify that."* Much of the catalog is coordination overhead, not value. These principles reprice it.

---

## The five reframes

Every document's badges and `In AI-driven workflows` note derive from these.

### P1 — Prefer executable artifacts over prose
Where a document can be machine-readable (OpenAPI, schema migrations, test-as-spec, eval suites, SLO-as-config, runbook-as-YAML, devcontainer), **that** is the source of truth; the prose shrinks to intent + a pointer. Agents consume and generate from executable artifacts and can be *verified* against them. Prose drifts, and agents cannot check themselves against it.

### P2 — Bias to empirical iteration over predictive design (for reversible work)
Cheap implementation + cheap rework means **spike with an agent, then capture what survived** in a thin design + ADR, beating heavy upfront design. Reserve heavy design for irreversible, high-blast-radius, or cross-team work. Prediction is expensive and often wrong; iteration is now cheap.

### P3 — Tighten intent upstream, verify hard downstream
Vague intent becomes confidently-wrong code *fast*. Acceptance criteria + concrete examples + anti-requirements (upstream) and evals + scenario replays + progressive rollout (downstream) carry the load that prose specs and manual QA used to. The cost of ambiguity moved earlier and got bigger.

### P4 — Externalize decisions and conventions; agents have no memory
ADRs and the Agent Operating Manual are load-bearing, not optional. Anything undocumented is invisible to agents and gets re-derived — often wrongly — every session.

### P5 — Watch for generated-documentation theater
Agents mass-produce plausible, wrong, unmaintained docs cheaply. Every document still needs an owner who *verifies* it. Never auto-generate-and-forget. This is a new failure mode the old catalog never had to guard against — and the guardrail against this system bloating itself.

---

## What changed

| Cost vector | Pre-AI | Post-AI |
|---|---|---|
| Implementation | Slow; vagueness was forgiving | Fast; vagueness becomes confidently-wrong artifacts |
| Iteration / rework | Expensive; favored heavy upfront design | Cheap; favors empirical iteration with crisp acceptance criteria |
| Tribal knowledge | Survived via human onboarding | Invisible to agents; must be externalized |
| Code review | Reviewers could line-read small PRs | Reviewers can't line-read large agent PRs; evals required |
| Decision durability | Watercooler memory often sufficed | Agents re-litigate every undocumented decision |
| Coordination | Many docs existed to align humans | Smaller teams + agents need less coordination paperwork |

## Higher-leverage documents

PRD acceptance criteria + anti-requirements · ADRs · [Agent Operating Manual](07-implementation-and-execution.md) · [AI Eval / Verification Plan](08-testing-and-quality.md) · executable test cases · [Observability Spec](10-operations-and-observability.md) · [Threat Model](05-security-privacy-compliance.md) (AI-extended) · progressive [Rollout + Rollback](09-release-and-rollout.md) · [Autonomy & Approval Policy](12-autonomy-and-approval.md).

## Lower-leverage documents

Long-form prose specifications · standalone prose Non-Functional Requirements · heavyweight SRS without compliance pressure · manual QA smoke-test plans · status/activity reports · heavy RACI matrices · heavy static execution plans.

## What does not change

- Business case, launch plan, runbook, incident review, postmortem still matter.
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

## AI-augmented default flow

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

Skip SRS, heavyweight NFR docs, and heavy execution plans unless audit, compliance, contract, or program scale requires them.
