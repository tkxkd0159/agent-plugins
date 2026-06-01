[← Back to index & glossary](../PRODUCT_CYCLE.md)

# 09. Release & Rollout

> How do we ship it safely, expose it gradually, and get back out if it breaks?

---

## Launch Plan

- **Answers:** How does this go live?
- **Use when:** customer-facing, risky, or multi-team release.
- **Skip when:** small internal change behind existing flags.
- **Owner:** PM / Release / Engineering.
- **Key contents:** launch phases (dogfood → beta → GA) · target users · launch owner & date · dependencies · support plan · success metrics · **go/no-go criteria**.
- **Boundary:** Launch Plan = *coordination & comms*; Rollout Plan = *technical exposure mechanics* (below).
- **Why it matters:** go/no-go should reference SLOs ([06](06-reliability-and-scale.md)) and eval results ([08](08-testing-and-quality.md)).

## Rollout / Migration Plan

- **Answers:** How do we expose the change progressively and migrate data safely?
- **Use when:** risky releases, data migrations, or large blast radius.
- **Skip when:** trivial, instantly reversible change.
- **Owner:** Engineering / SRE.
- **Key contents:** feature flags · canary / percentage / region-by-region rollout · backward compatibility · DB migration & backfill · monitoring during rollout · **stop conditions**.
- **Boundary:** Rollout = forward exposure; Rollback (below) = reverse path. Schema *design* lives in [04](04-interfaces-and-data.md).
- **Why it matters:** progressive delivery is how you safely ship agent-generated code you cannot fully line-read — the rollout, not the code review, is the primary safety net (P3).

## Rollback Plan

- **Answers:** How do we get back to a known-good state, fast?
- **Use when:** any change with production impact.
- **Skip when:** trivially and automatically reversible.
- **Owner:** Engineering / SRE.
- **Key contents:** rollback trigger conditions · exact revert steps · data-rollback/forward-fix strategy · verification that rollback worked.
- **Boundary:** part of safe rollout; distinct because an untested rollback fails when you need it most.
- **Why it matters:** automate it and **test it** — fast automated rollback is the counterweight to fast, less-scrutinized AI delivery (P3).

## Release Notes

- **Answers:** What changed, for whom?
- **Use when:** users, support, or API consumers need change visibility.
- **Skip when:** no external-visible change.
- **Owner:** PM / Eng.
- **Key contents:** changes by audience (users / support / developers / API consumers).
- **Why it matters:** generate from merged PRs/commits, then human-edit for audience — low manual effort (P1).

## Deprecation Plan

- **Answers:** How do we remove an API, feature, field, or service without breaking consumers?
- **Use when:** removing public/consumed surface.
- **Skip when:** purely internal, no consumers.
- **Owner:** Engineering / PM.
- **Key contents:** what & why · who's affected · replacement path · timeline · comms · compatibility period · enforcement date · rollback option.
- **Boundary:** Deprecation = *removal*; Rollout = *introduction*.
- **Why it matters:** without a deprecation plan, systems accumulate permanent technical debt agents must keep working around — record the sunset explicitly (P4).
