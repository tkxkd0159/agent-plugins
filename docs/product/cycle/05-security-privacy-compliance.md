[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 05. Security, Privacy & Compliance

> How can the system be attacked or abused, what sensitive data does it touch, and what is legally required?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

Security, privacy, and risk are **design-time** concerns, not final-stage checklist items.

---

## Threat Model `Elevated`

- **Answers:** How can the system be attacked or abused?
- **Use when:** payments, identity, messaging, user data, admin tools, public APIs, **and any AI/agent system**.
- **Skip when:** no meaningful attack surface or sensitive asset.
- **Owner:** Engineering / Security.
- **Key contents:** assets to protect · trust boundaries · attack surfaces · auth(n/z) risks · data-exposure & abuse scenarios · dependency risks · mitigations · residual risks.
- **AI-specific extensions (required for agent systems):** prompt injection · tool / effector scoping and over-permissioning · treating logs, SQL, telemetry, and user content as **untrusted input** that must never be interpreted as instructions · supply-chain risk of agent-generated dependencies. (See this repo's `AIOps_DBaaS.md` §15 for a worked example.)
- **Boundary:** Threat Model = the *analysis*; Security Review = the *approval process* (below).
- **In AI-driven workflows:** the attack surface **grows** — agents add new, non-obvious threats. Elevate and extend the threat model accordingly (P4).

## Security Review `Core` `Conditional`

- **Answers:** Are the security controls adequate and approved?
- **Use when:** auth, permissions, sensitive data, external access, or abuse risk exists.
- **Skip when:** no security-relevant surface.
- **Owner:** Security + Engineering.
- **Key contents:** authn/authz design · secrets management · encryption in transit & at rest · sensitive-data logging · dependency & supply-chain review · abuse prevention · pen-test plan.
- **Boundary:** Threat Model analyzes; Security Review approves.
- **In AI-driven workflows:** routine review shifts to **automated** SAST/DAST/dependency scanning in CI; manual review concentrates on high-risk surfaces and on **reviewing agent-generated code** that humans can't line-read at volume (P3). Never merge unreviewed agent code into security-relevant paths.

## Privacy / Data Protection Review `Conditional`

- **Answers:** What personal data do we collect, and is it handled lawfully and safely?
- **Use when:** personal or sensitive data is processed.
- **Skip when:** no personal data.
- **Owner:** Privacy / Legal + Engineering.
- **Key contents:** data collected · purpose · legal basis · retention & deletion · consent · sharing · access controls · anonymization/pseudonymization · regional residency · audit logging.
- **AI-specific extensions:** what user data flows into LLM **prompts/context**, model-call **data residency**, and whether any data is retained or used for training.
- **Boundary:** Privacy Review = personal-data obligations; Security Review = controls; Compliance Doc = regulatory mapping.
- **In AI-driven workflows:** the prompt/context pipeline is a new privacy surface — review what PII reaches the model (P4).

## Compliance Document `Conditional`

- **Answers:** Does system behavior meet the applicable regulations?
- **Use when:** regulated domains (SOC 2, ISO 27001, GDPR, HIPAA, PCI DSS, financial controls).
- **Skip when:** unregulated work.
- **Owner:** Compliance / Security.
- **Key contents:** mapping of system behavior → each control · evidence pointers · audit trail.
- **Boundary:** this is the one place SRS-style requirement-to-evidence traceability ([02](02-requirements.md)) legitimately survives.
- **In AI-driven workflows:** add **provenance** for AI-generated code/decisions and the agent action audit trail ([10](10-operations-and-observability.md)) as compliance evidence.
