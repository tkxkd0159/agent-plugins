[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 02. Requirements

> What must the system do, precisely and testably — when formality is actually required.

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

---

## SRS — Software Requirements Specification `Conditional`

- **Answers:** What must the software do, precisely and testably, with traceability?
- **Use when:** audit, regulatory, contractual, or safety-critical work that needs requirement-to-test traceability.
- **Skip when:** no compliance/contract pressure — acceptance criteria in the PRD ([01](01-product-and-ux.md)) plus executable tests ([08](08-testing-and-quality.md)) cover the same ground with less overhead.
- **Owner:** Product / Systems / Engineering.
- **Key contents:** functional requirements · non-functional requirements · business rules · input/output behavior · edge & error conditions · permission rules · compliance requirements · acceptance criteria · **traceability matrix** (requirement → design → test → evidence).
- **Boundary:** PRD defines product *outcomes*; SRS defines formal *shall-statements* with traceability. Acceptance criteria are testable scenarios *inside* a PRD; an SRS is the heavyweight, audited form.
- **In AI-driven workflows:** do **not** adopt SRS to fix AI ambiguity — that is what sharpened acceptance criteria and evals are for. SRS earns its place only when an auditor or contract demands the traceability matrix (P3).

## Non-Functional Requirements `Merged`

> **Merged.** In this system, NFRs are expressed as **SLOs + capacity targets + acceptance criteria**, not a standalone prose document. A separate NFR doc survives only under SRS-style compliance pressure.

- **Answers:** How fast / available / durable / scalable / secure must it be?
- **Where it lives now:** latency, throughput, availability, durability → SLOs ([06](06-reliability-and-scale.md)); scale → Capacity Plan ([06](06-reliability-and-scale.md)); security/privacy → [05](05-security-privacy-compliance.md); per-feature limits → PRD acceptance criteria ([01](01-product-and-ux.md)).
- **Boundary:** an NFR phrased as prose ("should be fast") is unusable by an agent; the same NFR phrased as `p99 < 300ms, verified by load test X` is executable and verifiable.
- **In AI-driven workflows:** always render NFRs as machine-checkable assertions (P1). The standalone prose NFR doc is the lowest-leverage artifact in the catalog unless compliance forces it.
