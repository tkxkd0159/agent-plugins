---
name: coding-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, preserve existing behavior, and define verifiable success criteria.
user-invocable: false
---

# Coding Guidelines

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment and avoid unnecessary process.

## 1. Think Before Coding

**Don't assume silently. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State material assumptions explicitly.
- If multiple reasonable interpretations exist, identify them.
- If a simpler approach exists, say so.
- Push back when the requested approach appears overcomplicated, risky, or misaligned with the goal.

Clarification rule:
- Ask only when the answer would materially change correctness, API design, data safety, user-visible behavior, or implementation scope.
- If the ambiguity is low-risk and a conventional default exists, state the assumption and proceed.
- Do not block on clarification for routine choices that can be safely reversed.

Examples:
- Ask: "Should this validation reject existing saved records too, or only new writes?"
- Proceed: "Assuming this should follow the existing file's style and remain backward-compatible."

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No configurability that was not requested.
- No new dependencies unless clearly justified.
- No error handling for impossible or irrelevant scenarios.
- Prefer standard library and existing project utilities over new code.
- Prefer small local code over a dependency for trivial logic.
- If you write 200 lines and it could be 50, rewrite it.

Before adding a dependency, consider:
- Whether existing code already solves the problem.
- Build, security, licensing, and maintenance impact.
- Whether the dependency is justified by real complexity.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Do not improve adjacent code, comments, formatting, or structure unless required.
- Do not refactor unrelated code.
- Match existing style, even if you would personally write it differently.
- Preserve existing public APIs, file structure, naming conventions, and behavior unless explicitly asked to change them.
- If a breaking change seems necessary, call it out before implementing.
- If you notice unrelated dead code or bugs, mention them separately instead of fixing them silently.

When your changes create orphans:
- Remove imports, variables, functions, files, or tests that your changes made unused.
- Do not remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" -> "Write tests for invalid inputs, then make them pass."
- "Fix the bug" -> "Write a test that reproduces it, then make it pass."
- "Refactor X" -> "Ensure behavior is unchanged before and after."

For multi-step tasks, state a brief plan:

```text
1. [Step] -> verify: [check]
2. [Step] -> verify: [check]
3. [Step] -> verify: [check]
```

Strong success criteria let you work independently. Weak criteria like "make it work" require clarification or a stated assumption.

## 5. Verification Discipline

**Verify with the narrowest useful check. Do not fake certainty.**

Verification priority:
1. Reproduce the bug or define the expected behavior.
2. Add or update targeted tests when appropriate.
3. Run the smallest relevant test command.
4. Run typecheck or lint if relevant and cheap.
5. Run broader tests only when necessary.

Rules:
- Never claim something is verified unless it was actually checked.
- If tests, typechecks, or linters cannot be run, say exactly what was not run and why.
- If verification fails, determine whether the failure was caused by your change.
- Fix failures caused by your change.
- Report unrelated failures separately.
- Do not broaden the scope silently.

## 6. Failure Handling

**Be explicit when something does not work.**

If implementation or verification fails:
- State the failure clearly.
- Include the relevant error or symptom.
- Explain whether it appears related to the change.
- Propose the smallest next step.
- Do not pretend the task is complete.

If the current approach is wrong, stop and revise the approach instead of layering patches on top.
