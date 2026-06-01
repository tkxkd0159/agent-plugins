[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 03. Architecture & Design

> What is the system's shape, how exactly will we build this slice, and what did we decide?

---

## Architecture Design Doc

- **Answers:** What are the major components and how do they interact?
- **Use when:** new system, new service boundaries, or change to long-term structure.
- **Skip when:** work fits cleanly inside existing architecture.
- **Owner:** Engineering / Architecture.
- **Key contents:** system context · component diagram · service boundaries · data & control flow · trust boundaries · deployment topology · scaling model · failure domains · external integrations.
- **Boundary:** Architecture Doc = system *shape & boundaries* (broad, durable). Technical Design Doc = how *this feature* is implemented (narrow).
- **Why it matters:** this is the stable context that constrains agent work — the invariants and boundaries an agent must not violate. Keep it durable and link it from the Agent Operating Manual ([07](07-implementation-and-execution.md)).

## Technical Design Doc

- **Answers:** How exactly will we build this feature/subsystem?
- **Use when:** implementation is non-trivial, spans systems, has non-obvious trade-offs, or QA can't test from the PRD alone.
- **Skip when:** small/reversible — acceptance criteria + an ADR for any real decision is enough.
- **Owner:** Engineering.
- **Key contents:** background · goals / non-goals · proposed design · API & data-model changes · failure handling, idempotency, retries · caching · migration & backward compatibility · rollout plan · risks & alternatives · test plan · observability plan.
- **Boundary:** ADR captures *one decision*; Technical Design explains *the whole implementation*. Architecture Doc is *broader and more durable*.
- **Why it matters:** for reversible work, prefer **spike-then-thin-design** — let an agent prototype, then capture what survived plus an ADR, rather than a long predictive design up front (P2). Reserve heavy design for irreversible / high-blast-radius / cross-team work.

## RFC — Request for Comments

- **Answers:** What technical direction are we proposing, and what feedback do we need before committing?
- **Use when:** cross-team dependency, durable architecture, breaking change, new platform standard.
- **Skip when:** a single team can decide — prototype the options and record an ADR instead.
- **Owner:** Engineering.
- **Key contents:** proposal · motivation · alternatives · trade-offs · compatibility · migration · feedback requested · decision deadline.
- **Boundary:** RFC helps *decide* (may hold multiple proposals, can be rejected); ADR *records* the decision (one chosen path).
- **Why it matters:** for a single team, "spike both approaches with agents, measure, then ADR" usually beats a written RFC. Keep RFCs for genuinely cross-team or breaking decisions (P2).

## ADR — Architecture Decision Record

- **Answers:** What did we decide, why, and what alternatives did we reject?
- **Use when:** any durable decision — architecture, infra dependency, service boundary, datastore/protocol/framework choice, or anything likely to be questioned later. **Use even within a single team.**
- **Skip when:** trivial, easily reversible choices.
- **Owner:** Engineering / Architecture.
- **Key contents:** context · decision · alternatives considered · consequences · status (proposed / accepted / deprecated / superseded).
- **Boundary:** ADR = *decision rationale*. Technical Design = *implementation*. RFC = *pre-decision discussion*.
- **Why it matters:** **one of the highest-leverage documents.** Agents have no memory and re-litigate every undocumented decision; a cheap ADR ends the re-debate permanently (P4). Supersede ADRs, never silently rewrite them.
