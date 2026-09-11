---
name: code-review
description: Use when the user asks for a code review or when the delivery pipeline reaches the maintainability review gate for an implemented task.
---

# Thermo-nuclear code review

Run an extremely strict review of the current Git changes. Focus on implementation quality, maintainability, abstraction quality, and codebase health.

Push for ambitious structural simplification. Do not stop at local cleanup. Search for "code judo" moves that preserve behavior while making the implementation smaller, more direct, and easier to understand.

## Review boundary

- Run in the current directory and derive the change set from Git.
- Review the current branch plus staged, unstaged, and untracked implementation files. Uncommitted work is the expected input. Never report it as a problem or ask for a commit.
- When the orchestrator supplies a pre-task baseline, judge the implementation agent's complete delta from that baseline. Do not attribute unrelated pre-existing working-tree changes to the task.
- Read changed code, its relevant callers and boundaries, nearby repository guidance, and tests that explain behavior.
- Judge maintainability and structure. The coding agent owns tests and functional verification. Do not run tests or builds, repeat acceptance-criteria checks, or reject based on missing test evidence.
- Do not edit implementation files.

## Core prompt

> Perform a deep code quality audit of the current changes.
> Rethink how to structure and implement the changes to improve code quality without changing behavior.
> Improve abstractions and modularity. Reduce spaghetti code. Make the result succinct and legible.
> Be ambitious. If restructuring part of the codebase gives the change a clearly better shape, require it.
> Be thorough and rigorous. Measure twice, cut once.

## Non-negotiable standards

### Seek structural simplification

- Do not stop at "this could be cleaner."
- Look for ways to remove whole branches, helpers, modes, conditionals, or layers.
- Prefer the design that makes the implementation feel inevitable in hindsight.
- Use the existing architecture to delete complexity instead of rearranging it.

### Stop unjustified file growth

Do not let a change push a file from fewer than 1,000 lines to more than 1,000 lines without a compelling structural reason. Prefer focused helpers, components, or modules. Treat the threshold crossing as a blocker when decomposition would improve the design.

### Reject spaghetti growth

- Treat new ad hoc conditionals, scattered special cases, and one-off branches in unrelated flows as design problems.
- Push logic into a clear abstraction, helper, state machine, policy, or module when that removes tangling.
- Reject changes that make surrounding code harder to reason about even when they work.

### Clean the design

- Do not approve working code that leaves the codebase messier.
- Prefer simplifications that remove moving pieces over refactors that spread the same complexity around.
- Prefer direct, boring code over brittle, ad hoc, or magical behavior.
- Reject generic machinery that hides a simple data shape.
- Reject thin wrappers and pass-through helpers that add indirection without clarity.

### Keep types and boundaries explicit

- Question unnecessary optionality, `unknown`, `any`, and cast-heavy code when a clearer boundary exists.
- Prefer explicit typed models and shared contracts over loose objects.
- Reject silent fallbacks that hide an unclear invariant when the boundary can state it directly.
- Keep logic in its canonical layer and reuse existing helpers.
- Reject feature logic leaking into shared paths or implementation details leaking through APIs.

### Keep orchestration simple and state coherent

- Flag unnecessary sequential work when independent operations can run in parallel and the result is simpler.
- Reject related updates that can leave state half-applied when a clear atomic structure exists.
- Do not turn micro-optimizations into findings.

## Review questions

For every meaningful change, ask:

- Is there a code-judo move that makes this dramatically simpler?
- Can fewer concepts, branches, helpers, or layers express the same behavior?
- Does the change improve or weaken the local architecture?
- Did it add branching where a better model or abstraction should exist?
- Did a cohesive module become more coupled, stateful, or difficult to scan?
- Does the logic live in the right file and layer?
- Did the change push a file or component past a healthy size?
- Do repeated conditionals reveal a missing model or helper?
- Is each abstraction earning its keep?
- Do casts, optional values, or ad hoc shapes obscure the real invariant?
- Did the change duplicate a canonical helper or put logic outside its natural owner?
- Is orchestration more sequential or state less atomic than necessary?

## Findings

Report a finding aggressively when the change introduces or worsens:

- incidental complexity that a clear reframing would delete;
- a file crossing 1,000 lines without strong justification;
- conditionals bolted onto unrelated paths;
- one-off booleans, nullable modes, or flags that tangle control flow;
- feature logic in a general-purpose module;
- magic handling that hides straightforward structure;
- wrappers or abstractions that do not simplify anything;
- unnecessary casts, `any`, `unknown`, or optional parameters;
- copied logic that should use an existing helper;
- edge-case handling buried in an already busy function;
- a refactor that moves complexity without reducing it;
- temporary branching likely to become permanent debt;
- logic in the wrong package, service, module, or layer;
- avoidable sequential flow or non-atomic state changes.

Prefer remedies that remove complexity, clarify ownership, expose invariants, reuse canonical code, or split oversized modules. A rename or cosmetic cleanup is not enough when the problem is structural.

Prefer concrete remedies such as:

- delete a layer of indirection instead of polishing it;
- reframe the state model so conditionals disappear;
- move ownership so the feature naturally extends an existing abstraction;
- turn special-case logic into a default flow with fewer exceptions;
- extract a focused helper, pure function, component, or module;
- replace condition chains with a typed model or explicit dispatcher;
- separate orchestration from business logic;
- collapse duplicate branches;
- delete wrappers that do not clarify the API;
- reuse the canonical helper;
- make the type boundary explicit;
- parallelize independent work when that also simplifies orchestration;
- make related updates atomic.

## Review tone

Be direct, serious, and demanding. Do not be rude, but do not soften a maintainability problem into a suggestion. Say plainly when a change makes the codebase messier or misses a clear simplification.

## Approval bar

Approve only when the change has:

- no clear structural regression;
- no visible path to a dramatically simpler implementation that the author missed;
- no unjustified file-size explosion;
- no spaghetti growth from special cases;
- no hacky or magical abstraction that makes the design harder to understand;
- no unnecessary wrapper, cast, or optionality churn;
- no architecture-boundary leak or canonical-helper duplication;
- no obvious decomposition that would materially improve maintainability.

Every high-confidence finding blocks approval. Do not create an optional category. Omit cosmetic preferences and low-confidence nits.

Mark a bounded, behavior-preserving correction as `FIX NOW`. Structural corrections also block approval even when they need more work. Report at most ten blockers in one pass, ordered by the original thermo-nuclear priority:

1. structural regressions;
2. missed dramatic simplifications;
3. spaghetti and branching growth;
4. boundary, abstraction, and type-contract problems;
5. file-size and decomposition concerns;
6. modularity problems;
7. legibility and maintainability problems.

## Pre-existing debt

Do not block the task for a problem that predates the reviewed delta or that the current change did not worsen. Return each such problem under `Debt` with its path, evidence, and a focused description. The main orchestrator owns deduplicating these entries into the active specification directory's `DEBT.md`.

If the current change worsens pre-existing debt, report the worsened part as a blocker.

## Output

The first line must be exactly one of:

```text
[APPROVE]
```

```text
[REJECT]
```

For `[REJECT]`, add `## Fix now` and list up to ten blockers. Each item must include the file and line, the concrete problem, why it blocks approval, and the smallest acceptable outcome. Prefix bounded behavior-preserving fixes with `FIX NOW`.

Add `## Debt` when pre-existing issues need recording. An approved review may contain debt but no current-change findings. Do not add a preamble or an optional section.

## Source and license

Adapted from Cursor's [`thermo-nuclear-code-quality-review`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md), licensed under the [MIT License](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/cursor-team-kit/LICENSE).
