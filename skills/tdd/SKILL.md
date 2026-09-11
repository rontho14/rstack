---
name: tdd
description: MUST use together with `ponytail` for every task that builds, fixes, or refactors code. Also use when the user asks to add, change, or improve tests.
license: MIT
---

# TDD

Establish the smallest useful executable check before changing production code, then prove the change with focused tests. Test behavior without building a second implementation inside the test suite.

## Choose a useful check

A new unit test is useful when it:

- fails when an observable behavior, contract, invariant, or boundary is wrong;
- has a focused, stable target already supported by the repository's test structure;
- needs less setup than the behavior it protects;
- adds a distinct signal that existing tests do not already provide.

Do not add a unit test for trivial delegation, declarations, generated code, framework behavior, private implementation details, or an already-covered outcome. Reject tests dominated by mocks, timing, broad infrastructure, unrelated fixtures, or setup churn.

When a useful unit test is unavailable, choose the cheapest executable check that can catch the likely failure. Use the coverage-tool decision recorded by `setup`; do not invent a new dependency or policy during implementation.

## Workflow

1. Read the task, affected code, nearby tests, and repository test commands and conventions.
2. State the observable behavior that the check must protect.
3. Choose an existing test, a new focused test, or the closest executable check using the usefulness rules above.
4. Before editing production code:
   - for a bug fix or new behavior, write and run the focused check and confirm that it fails for the intended reason;
   - for a refactor, run the existing focused tests first; when they do not pin the behavior, add a characterization test before refactoring.
5. Apply `ponytail` and make the smallest production change that satisfies the check.
6. Rerun the focused check and confirm it passes.
7. Run adjacent tests, type checks, lint, or integration checks only when the changed boundary makes them relevant.
8. Measure coverage using the repository policy established by `setup`.

If a new test passes before the production change or fails for an unrelated reason, fix the test or choose a better check before coding. Never change a test merely to accept wrong behavior, weaken a valid assertion, or hide a regression.

## Avoid over-testing

- Cover each distinct behavior and meaningful branch once. Do not target every line or permutation.
- Prefer outcome assertions over interaction order. Assert an external request shape only when that request is the boundary contract.
- Keep tests readable and self-contained. Reuse small established fixtures, but do not create a fixture framework for one case.
- Prefer real collaborators, then fakes, then stubs, and mock only at boundaries.
- Do not assert log text, create snapshots without a repository reason, skip tests, or add coverage padding.
- Keep a focused regression test after a bug fix. Do not delete it after proving the change.

## Coverage

Require at least 80% line coverage of new and changed production code. Use the command and measurement method selected during `setup`.

If the repository cannot measure new and changed coverage, follow the alternative recorded by `setup`. Do not substitute whole-repository coverage, add tooling, or silently waive the threshold during the coding task.

## Completion evidence

Report:

- the failing-before test or executable check and its intended failure;
- the passing-after result;
- relevant adjacent validation;
- measured new-and-changed-code coverage, or the configured alternative;
- a short map from each changed behavior to the test or check that protects it.

Do not prescribe a universal command or number of tests. Repository evidence owns the framework, file placement, naming, and commands.

## Source and license

Adapted from pstack's [`tdd`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/tdd/SKILL.md), licensed under the [MIT License](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/LICENSE).
