[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 07. Implementation & Execution

> How do we turn design into work, and how do agents operate safely in the codebase?

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

---

## Engineering / Execution Plan `Conditional`

- **Answers:** What work, in what order, by whom, by when?
- **Use when:** large, multi-team programs with real sequencing risk.
- **Skip when:** single-team work — a live task list is enough.
- **Owner:** Eng lead / TPM.
- **Key contents:** milestones · work breakdown · owners · dependencies · sequencing · critical path · delivery phases.
- **Boundary:** Engineering Plan = *delivery sequencing*; Technical Design ([03](03-architecture-and-design.md)) = *how it's built*.
- **In AI-driven workflows:** sequencing is more fluid when agents parallelize work — prefer a maintained live plan over a heavy static one (P2).

## Task Breakdown / Implementation Plan `Elevated` `Executable`

- **Answers:** What are the concrete, verifiable units of work?
- **Use when:** any non-trivial implementation, especially agent-driven.
- **Skip when:** a single small ticket covers it.
- **Owner:** Engineering.
- **Key contents:** atomic tasks · per-task acceptance check · interface dependencies · migration / test / cleanup tasks.
- **Boundary:** this is the *executable plan*, not the design ([03](03-architecture-and-design.md)) and not the product intent ([01](01-product-and-ux.md)).
- **In AI-driven workflows:** this becomes high-leverage — the plan that drives autonomous agents must be **atomic and independently verifiable**, so each task has a clear pass/fail check an agent (and reviewer) can confirm (P3).

## Code Structure / Repository Guide `Merged`

> **Merged** into the Agent Operating Manual (below) — same audience, same purpose now. Maintain one file at the repo root, not two.

- **Covers:** repository layout · module boundaries · naming conventions · dependency rules · build/test commands · local setup pointers · ownership.

## Development Environment Setup `Conditional` `Executable`

- **Answers:** How does a contributor (human or agent) get a working environment?
- **Use when:** many contributors, or non-trivial local setup.
- **Skip when:** setup is a single documented command.
- **Owner:** Engineering.
- **Key contents (as code):** devcontainer / Makefile / scripts · prerequisites · secrets · DB & mock services · test data · debugging notes.
- **Boundary:** setup *mechanics* live here; conventions live in the Agent Operating Manual.
- **In AI-driven workflows:** prefer **setup-as-code** an agent can run and verify over prose an agent can only read (P1). Keep it ruthlessly current.

## Agent Operating Manual `AI-native` `Elevated`

- **Answers:** How should AI agents behave in *this* repository?
- **Use when:** any time AI agents operate in the codebase.
- **Skip when:** no agents touch the repo (rare, and shrinking).
- **Owner:** Engineering.
- **Where:** repo root — `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, etc.
- **Key contents:** repo conventions & layout · build/test/lint commands · dependency & style rules · what to do / never do · links to Architecture Doc, key ADRs, and the Autonomy & Approval Policy ([12](12-autonomy-and-approval.md)) · reusable prompt/context templates.
- **Boundary:** Agent Operating Manual = *repo-scoped conventions for agents*; Technical Design = *how one feature is built*; Autonomy Policy ([12](12-autonomy-and-approval.md)) = *what agents may do without approval*.
- **In AI-driven workflows:** load-bearing. Agents have no memory and cannot absorb tribal knowledge — anything not written here is invisible to them and gets re-derived (often wrongly) every session (P4).
