[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 06. Reliability & Scale

> How reliable must it be, can it handle the load, and how does it recover from disaster?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

---

## SLO / SLA / Error Budget `Elevated` `Executable`

- **Answers:** How reliable must the system be, and what happens when it isn't?
- **Use when:** any production-grade service where reliability matters.
- **Skip when:** throwaway or internal-only tooling with no reliability expectation.
- **Owner:** Service owner / SRE.
- **Key contents (as config + alerts):** SLIs · SLOs · SLAs (external commitments) · error budget · measurement method & window · alerting thresholds · exclusions · budget-exhaustion policy.
- **Definitions:** **SLI** = the measured indicator; **SLO** = the internal target; **SLA** = the external/contractual commitment; **error budget** = allowed unreliability before release/risk policy changes.
- **Boundary:** SLOs = *reliability* targets; Success Metrics ([01](01-product-and-ux.md)) = *product outcome* targets.
- **In AI-driven workflows:** machine-checkable SLOs are exactly the guardrails agents and AIOps loops consume (burn-rate signals drive incident detection — cf. `AIOps_DBaaS.md`). Express as config, not prose (P1).

## Capacity Planning `Conditional`

- **Answers:** Can the system handle expected (and peak) scale?
- **Use when:** scale is a real risk — high QPS, large storage growth, cost-sensitive footprints.
- **Skip when:** low, predictable load.
- **Owner:** Engineering / SRE.
- **Key contents:** expected & peak traffic · growth assumptions · QPS/RPS · storage/bandwidth · CPU/memory · DB/cache capacity · queue depth · cost projection · load-test results · scaling limits.
- **Boundary:** Capacity Plan = *can it handle the load*; Performance Design (below) = *is the critical path fast*.
- **In AI-driven workflows:** derive capacity numbers from Load Test results ([08](08-testing-and-quality.md)) rather than hand-guessing; agents can generate the load profiles and summarize results.

## Performance Design `Merged`

> **Merged** into Technical Design ([03](03-architecture-and-design.md)) + SLOs (above) + Load Test ([08](08-testing-and-quality.md)). Keep standalone only for extreme high-QPS / low-latency systems.

- **Answers:** Will the critical path meet its latency budget?
- **Key contents (when standalone):** latency budget · critical-path analysis · caching · query optimization · hot-key mitigation · connection pooling · backpressure · benchmark results.
- **Boundary:** Performance = *latency of the critical path*; Capacity = *throughput at scale*.
- **In AI-driven workflows:** encode latency budgets as SLO assertions and benchmark gates so they are verifiable, not aspirational (P1).

## Disaster Recovery / Business Continuity `Conditional`

- **Answers:** How does the system recover from major failure or data loss?
- **Use when:** business-critical systems.
- **Skip when:** non-critical, easily rebuilt systems.
- **Owner:** Engineering / SRE.
- **Key contents:** RTO · RPO · backup strategy · restore procedure · regional failover · dependency-failure scenarios · manual fallback · data-corruption recovery · DR test schedule.
- **Definitions:** **RTO** = how fast you must recover; **RPO** = how much data loss is tolerable.
- **Boundary:** DR/BCP = *catastrophic recovery*; Runbook ([10](10-operations-and-observability.md)) = *routine operational recovery*.
- **In AI-driven workflows:** unchanged in principle; ensure recovery procedures are executable runbooks, not prose (P1).
