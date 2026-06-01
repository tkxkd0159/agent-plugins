[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 04. Interfaces & Data

> How do systems communicate, and how is data stored — as machine-readable contracts.

**Badge legend:** `Core` · `Elevated` · `Conditional` · `Executable` · `Merged` · `AI-native`. See [AI-era principles](ai-era-principles.md).

This whole phase is **`Executable` by default**: the contract *is* the artifact (OpenAPI, proto, schema, migrations). Prose shrinks to intent + a pointer to the machine-readable source of truth (P1).

---

## API Specification `Core` `Executable`

- **Answers:** How do systems communicate over this interface?
- **Use when:** any internal or external API is exposed or changed.
- **Skip when:** purely internal function calls with no cross-team/process boundary.
- **Owner:** API owner / Engineering.
- **Key contents (as OpenAPI / proto / GraphQL):** endpoints/methods · request & response schema · error codes · auth(n/z) · rate limits · pagination · idempotency keys · versioning & backward-compatibility rules.
- **Boundary:** API Spec = the *contract*. Technical Design ([03](03-architecture-and-design.md)) = how the service behind it is built. Integration Spec (below) = how *you* consume someone else's contract.
- **In AI-driven workflows:** the machine-readable spec is the source of truth — agents generate clients, servers, mocks, and contract tests from it. A prose-only API doc is a liability (P1).

## Data Model / Schema Design `Core` `Executable`

- **Answers:** How is data stored, indexed, and governed?
- **Use when:** non-trivial data model, or any schema change.
- **Skip when:** trivial, well-patterned storage.
- **Owner:** Engineering / Data owner.
- **Key contents (as migrations / DDL):** entities & relationships · indexes · partitioning / sharding · retention · consistency model · ownership · backup/restore behavior · migration strategy.
- **Boundary:** schema design affects latency, cost, and operability — it is not just "fields." Migration mechanics live in the Rollout/Migration Plan ([09](09-release-and-rollout.md)).
- **In AI-driven workflows:** schema-as-code (migrations) is the durable, agent-consumable artifact; agents read and generate against it (P1). Schema changes are high-blast-radius — favor heavy review (P2 exception).

## Event / Messaging Specification `Conditional` `Executable`

- **Answers:** How do producers and consumers exchange events safely?
- **Use when:** the system uses queues, streams, webhooks, or event sourcing.
- **Skip when:** no asynchronous messaging.
- **Owner:** Engineering.
- **Key contents (as AsyncAPI / schema registry):** event names · producers / consumers · payload schema · ordering guarantees · delivery semantics · retry & dead-letter handling · deduplication · schema evolution · replay/backfill.
- **Boundary:** Event Spec = async contracts; API Spec = sync contracts.
- **In AI-driven workflows:** register schemas in a machine-readable registry so agents and compatibility checks can enforce evolution rules (P1).

## Integration Specification `Conditional` `Merged`

> Often **merged** into API Spec + Dependency Map ([11](11-governance-and-learning.md)). Keep standalone only for complex external/third-party contracts.

- **Answers:** How do we depend on this other system, safely?
- **Use when:** integrating an external or internal system with non-trivial contract, auth, or failure behavior.
- **Owner:** Engineering.
- **Key contents:** integration owner · protocol · auth · data mapping · timeout/retry/fallback behavior · rate limits · SLAs · test-environment details.
- **Boundary:** Integration Spec = how *we consume* a dependency; API Spec = the contract a dependency *publishes*; Dependency Map = the *inventory* of all dependencies.
- **In AI-driven workflows:** capture failure/fallback behavior explicitly — agents otherwise assume happy paths and ship brittle integrations (P3).
