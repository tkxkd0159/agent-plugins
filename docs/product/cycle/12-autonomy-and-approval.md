[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 12. Autonomy & Approval Policy `AI-native`

> What may an agent do on its own, what requires a human, and what is forbidden?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

This is the single most important governance artifact in an AI-driven workflow, and it is absent from the traditional document catalog. **Autonomy is a policy decision, not a model decision** — a deterministic policy layer decides what runs, never the model itself.

---

## Autonomy & Approval Policy

- **Answers:** For each class of action, what autonomy level applies — and who approves the rest?
- **Use when:** any time agents can take actions or merge code in your workflow.
- **Skip when:** agents are strictly advisory and a human performs every action.
- **Owner:** Engineering leadership + Security.
- **Boundary:** the Agent Operating Manual ([07](07-implementation-and-execution.md)) tells agents *how to work*; this policy defines *what they're allowed to do without a human*. The audit trail ([10](10-operations-and-observability.md)) records what they actually did.

### Autonomy levels

| Level | Meaning | Examples in software development |
|---|---|---|
| **A0** | Observe / advise only | summarize, classify, review, draft a plan or PR description — no changes |
| **A1** | Auto-execute reversible, low-blast-radius actions | open a PR, run tests/linters, apply a formatting or doc fix, low-risk automated remediation behind a flag |
| **A2** | Human approval required | merge to main, schema/data migration, infra or config change, customer-facing release, parameter change on a critical system |
| **A3** | Forbidden (without out-of-band controls) | destructive DDL, data deletion, secret access, cross-region promotion, disabling safety controls or the kill switch |

### Preconditions for autonomous (A1) execution

An action may auto-execute **only if all hold**:

- the playbook/task is approved and versioned;
- the action is classified **A1**;
- blast radius is bounded (single service / reversible scope);
- the action is reversible or low-risk;
- no production write-path or irreversible risk;
- confidence exceeds the configured threshold and novelty is below it;
- no identical failed attempt already occurred;
- the policy layer validates the concrete targets and parameters.

### Required controls

- **Environment gating:** production-affecting actions default to A2 (human approval).
- **Approval workflow:** approvers see the exact plan, blast radius, and rollback before approving; approval/rejection reasons are captured as structured data.
- **Kill switch:** a per-system switch halts autonomous action immediately.
- **Audit trail:** every prompt, tool call, action, and approval is logged ([10](10-operations-and-observability.md)).
- **Typed, allowlisted tools:** agents call bounded, schema-validated tools — never raw shell, arbitrary SQL, or unrestricted control-plane access.

### In AI-driven workflows

This policy is what makes autonomy *safe* rather than reckless. It separates the agent's reasoning (propose) from deterministic authorization (decide) and execution (act). Start narrow — most actions at A0/A1, everything risky at A2 — and promote actions to higher autonomy only after they prove reliable in shadow mode. This repo's `AIOps_DBaaS.md` (§12, §15, §19) is a worked, production-grade instance of this model for database operations.
