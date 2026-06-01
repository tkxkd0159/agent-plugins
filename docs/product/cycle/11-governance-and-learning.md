[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 11. Governance & Learning

> Who owns what, what depends on what, and how do we learn from what happened?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

> Autonomy & Approval — the most important AI-era governance artifact — has its own file: [12. Autonomy & Approval](12-autonomy-and-approval.md).

---

## Ownership / RACI `Core`

- **Answers:** Who owns, approves, and is informed about this system?
- **Use when:** many teams touch one system, or accountability is unclear.
- **Skip when:** single owner, obvious accountability — don't build a matrix for its own sake.
- **Owner:** Eng lead / TPM.
- **Key contents (kept light):** service / product / on-call / security / data owners · **approvers** · consulted & informed teams. (RACI = Responsible, Accountable, Consulted, Informed.)
- **Boundary:** Ownership = *who is accountable*; Dependency Map = *what connects to what* (below).
- **In AI-driven workflows:** the part that actually matters is **accountability + approval authority** — who is on the hook for agent actions and who approves high-risk ones (ties to [12](12-autonomy-and-approval.md)). Heavy RACI matrices are demoted as human-org overhead (P2).

## Dependency Map `Elevated`

- **Answers:** What does this system depend on, and what depends on it?
- **Use when:** non-trivial upstream/downstream dependencies.
- **Skip when:** standalone system with no real dependencies.
- **Owner:** Service owner.
- **Key contents:** services consumed · services depending on this · data dependencies · team owners · SLAs · failure impact · contact paths · version compatibility.
- **Boundary:** Dependency Map = the *inventory*; Integration Spec ([04](04-interfaces-and-data.md)) = the *contract* for one dependency.
- **In AI-driven workflows:** explicit dependency context lets agents reason about blast radius and avoid breaking downstreams; can be auto-generated and kept current (P4).

## Postmortem `Elevated`

- **Answers:** What failed technically, why, and what fixes prevent recurrence?
- **Use when:** any significant incident.
- **Skip when:** no incident.
- **Owner:** Incident owner / service owner (engineer).
- **Form:** **asynchronous and technical, written right after the incident while it's fresh — no meeting.** Highly technical.
- **Key contents:** summary · impact · timeline · root cause · detection & response gaps · code/system fixes · action items with owners & due dates.
- **Boundary:** Postmortem = the *async technical artifact about the system*. Retrospective (below) = the *periodic synchronous meeting about the human/process side* that **reviews** postmortems. Blameless but precise — it must produce concrete prevention work.
- **In AI-driven workflows:** feed findings back into runbooks ([10](10-operations-and-observability.md)), eval cases ([08](08-testing-and-quality.md)), and agent memory. Draft can be assembled from the incident timeline + agent audit trail ([10](10-operations-and-observability.md)), but an engineer must verify it — never auto-generate-and-forget (P5).

## Retrospective `Core`

- **Answers:** How did we (the team and process) do, and what should we change?
- **Use when:** on a standard periodic cadence (e.g., per sprint or after major launches).
- **Skip when:** nothing meaningful to review since the last one.
- **Owner:** Team lead / EM (facilitator).
- **Form:** **synchronous team meeting on a regular cadence.** Reviews the postmortems written since the last retro and discusses the human side — coordination, communication, process gaps.
- **Key contents:** review of recent postmortems · what went well / poorly on the human/process axis · process changes · follow-up actions.
- **Boundary:** Retrospective = *people & process, periodic, synchronous, reviews postmortems*. Postmortem = *system & technical, immediate, asynchronous*.
- **In AI-driven workflows:** the retro is where you tune the **workflow itself** — adjust autonomy levels ([12](12-autonomy-and-approval.md)), the Agent Operating Manual ([07](07-implementation-and-execution.md)), acceptance-criteria rigor, and eval coverage based on what the postmortems revealed.
