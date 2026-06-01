[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 10. Operations & Observability

> How do we see what the system is doing, operate it, recover it, and audit what agents did?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

---

## Observability Specification `Elevated`

- **Answers:** How will we detect and debug problems?
- **Use when:** any production system. **Design it, don't add it later.**
- **Skip when:** throwaway tooling.
- **Owner:** Service owner / SRE.
- **Key contents:** metrics · logs · traces · dashboards · alert rules, severity & owners · **golden signals** (latency, traffic, errors, saturation) · debugging dimensions (region, tenant, endpoint, version).
- **Boundary:** Observability Spec = *what we emit and watch*; Runbook = *what to do when an alert fires* (below).
- **In AI-driven workflows:** observability is both how you operate the system **and** how you verify agent-built systems behave in production — elevate it (P3).

## Runbook `Elevated` `Executable`

- **Answers:** What does an on-call engineer do during a known operational situation?
- **Use when:** any production-critical service or operational process.
- **Skip when:** no production operations.
- **Owner:** Service owner / SRE.
- **Key contents (prefer machine-readable):** alert meaning & impact · diagnosis steps · dashboards & logs to inspect · mitigation & rollback steps · escalation path · known false positives.
- **Boundary:** Runbook = *service-specific* recovery; Incident Playbook = *process* for any incident (below); DR Plan ([06](06-reliability-and-scale.md)) = *catastrophic* recovery.
- **In AI-driven workflows:** agent-executable runbooks (machine-readable, with verification windows) let an AIOps loop diagnose and remediate within policy — see `AIOps_DBaaS.md` §11 for the pattern (P1). A good runbook lets a tired on-call engineer **or an agent** act correctly at 3 a.m.

## Incident Response Playbook `Core`

- **Answers:** How do we run *any* incident?
- **Use when:** any team operating production systems.
- **Skip when:** no production responsibility.
- **Owner:** Engineering / SRE.
- **Key contents:** severity levels · incident-commander role · comms channels · escalation rules · customer comms / status page · mitigation process · postmortem requirement.
- **Agent participation:** define how agents act during incidents and at what autonomy level — tie directly to the Autonomy & Approval Policy ([12](12-autonomy-and-approval.md)).
- **Boundary:** Playbook = *process* (severity, roles, comms); Runbook = *service-specific actions*.

## Operational Readiness Review `Core`

- **Answers:** Is this service actually operable before it launches?
- **Use when:** before a service becomes production-critical (a launch gate).
- **Skip when:** non-production work.
- **Owner:** Service owner.
- **Key contents (checklist):** dashboards · alerts · runbooks · SLOs · useful logs · tested rollback · feature flags · trained on-call · documented dependencies · accepted known risks.
- **Boundary:** the gate that confirms [06](06-reliability-and-scale.md), Observability, Runbook, and Rollback ([09](09-release-and-rollout.md)) all exist before go-live.

## Agent Action Audit / Provenance Trail `AI-native`

- **Answers:** What did the agents actually do, and can we reconstruct it?
- **Use when:** agents take actions or generate code/decisions in production paths.
- **Skip when:** no autonomous agent actions.
- **Owner:** Engineering / SRE.
- **Key contents:** logged prompts, tool calls, actions, and approvals · who/what authorized each action · linkage to the Autonomy & Approval Policy ([12](12-autonomy-and-approval.md)).
- **Boundary:** feeds Postmortems ([11](11-governance-and-learning.md)) and Compliance evidence ([05](05-security-privacy-compliance.md)); part of Observability for the agent layer.
- **In AI-driven workflows:** non-negotiable for debugging, incident analysis, and compliance — you must be able to answer "why did the agent do that?" after the fact (P4, P5).
