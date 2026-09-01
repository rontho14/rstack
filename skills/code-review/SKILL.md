---
name: code-review
description: Use when the user asks for a code review or when the delivery pipeline reaches the review gate for an implemented task.
---

# Code Review

Review **one orchestrator task**. Judge only what **this diff introduced or worsened**. Untouched lines are out of scope.

**Do not run the test suite.** The coder already did. Trust the Coverage map; reject if it is missing or not `PASS`. Broken tests must never reach this gate.

## You do

1. Read the current task in `TASKS.md` (description, Success Criteria, Target Files).
2. `git diff` on Target Files plus tests for the same repo (`src/test/java` or colocated `*.spec.ts(x)`). Empty production diff → `[REJECT]`.
3. Read changed hunks plus enough context for layers and callers.
4. Check the Coder's output: must include `mvn test: PASS` and/or `npm test: PASS` (stacks this task touched) and a Coverage map. Missing or `FAIL` → `[REJECT]` (send it back; do not run the suite yourself).
5. Check tests against `.cursor/skills/code-test/SKILL.md` rules and the Coverage map (read the test source — do not execute).
6. Write `[APPROVE]` or `[REJECT]` and a short report.

Read-only on source. Do not edit code, `pom.xml`, OpenAPI, or tests. Do not spawn a shell to run Maven/npm tests.

## Reject on

**Gate**

- Coder did not report `mvn test: PASS` / `npm test: PASS` for the stacks this task touched, or Coverage map is missing
- Success Criteria not met
- Files changed outside Target Files without task justification
- Success Criteria item with no mapped test (see Coder's Coverage map or diff)
- New/changed production code likely below **70% new-code coverage** — untested branches, no test file for a new service/adapter

**Scope & quality**

- Stubs, `TODO`, empty implementations
- Unrequested refactors, renames, or drive-by changes
- Spaghetti: special cases or feature logic in shared/generic paths
- Duplication: new util/helper when the repo already has one
- Bloat: new dependency, interface-with-one-impl, factory, or config for a fixed value
- Speculative code not required by the task
- Symptom fix at one caller when a guard in the shared path would fix all callers
- Log-prefix constant files; log + throw for the same failure

**Layers (Java 17, hexagonal)** — only if Target Files are Maven

- HTTP/JSON mapping, Spring wiring, or adapter types in `domain/` / `application/domain`
- Business rules in REST controllers instead of application layer
- REST surface changed in `ms-orch-java-tr-customer-invoice` without matching `openapi.yaml` update
- Swallowed exceptions; catches that don't match neighboring adapters

**Tests** (violations of `code-test` rules — by reading the diff, not running)

- Interaction tests (`verify()` without outcome assertion), log-text asserts, snapshots, `@Disabled`
- Empty tests or coverage-padding with no behavioral assertion
- Tests for code outside this task's diff

## Approve when

- Coder reported the required `*: PASS` line(s) with a complete Coverage map
- Success Criteria met and mapped to tests
- Diff is minimal and task-scoped
- No reject triggers above in **new/changed lines**

Do not soften blockers. Do not nit untouched code.

## Report format

First line — exactly one of:

```text
[APPROVE]
```

```text
[REJECT]
```

Then:

**Blockers** (max 5) — path, what the diff did, why it blocks, minimal fix. Prefix ponytail issues with `Ponytail:`.

**Optional** (max 3) — only files already in this diff. Prefix with `Optional:`.

**Coder test result** — `mvn test: PASS` / `npm test: PASS` (as reported) or why rejected.

Skip sections with nothing to say. No preamble.
