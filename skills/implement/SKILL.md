---
name: implement
description: Use only when the user invokes /implement to deliver a task, a feature, or a TASKS.md through implementation and code-judo review loops.
disable-model-invocation: true
argument-hint: "[task description or path to TASKS.md]"
---

# Implement

Implement the requested work yourself, one task at a time. Gate every task behind an independent `code-judo` review, then review the whole feature before finishing.

## Start

1. When the working tree has staged, unstaged, or untracked changes, stop and ask the user to commit or stash them. Never stash, reset, or discard them yourself.
2. Record `HEAD` as the feature base.
3. Read the work: an existing `TASKS.md`, or the task described in conversation. Without `TASKS.md`, treat the request as one task and do not create a ledger.
4. Read `code-judo` and the authoring gate in `test-audit` before writing code. Write code and tests those reviews would approve on the first pass.

## Write the code

- Follow `AGENTS.md` and `tdd`.
- Never reference the specification, task numbers, or planning text in code, tests, identifiers, file names, or commit messages. Describe the behavior itself.

## Per task

Take tasks in dependency order, one at a time. Never implement tasks in parallel.

1. Implement the task, including any debt carried into it.
2. Produce the `tdd` completion evidence: failing-before, passing-after, relevant adjacent validation, and the coverage bar or the alternative recorded by `setup`. Do not start a review without it.
3. Run the [review loop](#review-loop) with the prompt `Run /code-judo.`
4. When the task passes, set its `Status` to `COMPLETED` and its `Review Rejections` to the number of `[REJECT]` rounds in `TASKS.md`.
5. Commit the task's code and ledger update together, using `commit` when it is installed.

## Review loop

1. Spawn a fresh subagent whose entire prompt is the review prompt. Never resume an earlier reviewer. Add nothing: no specification, task, diff summary, explanation, expectation, or earlier findings.
2. Take the review as returned. Do not argue with the reviewer or ask it to reconsider.
3. Triage every finding:
   - Accept code-quality findings by default. Be strict.
   - Reject a finding only when it contradicts a recorded decision: the specification, an ADR, an explicit user decision, or an established repository pattern. Record a one-line reason naming that decision. Preference is not a reason.
   - Ignore `Debt` unless it is worth fixing. Carry debt worth fixing into the next task, or into the final review when no task remains.
4. Fix the accepted findings, rerun the focused checks, and start a new round.
5. The loop passes when the latest review is `[APPROVE]` or contains only findings rejected with a recorded reason.
6. When a finding returns after two rounds of fixes, set the task's `Status` to `BLOCKED`, stop the run, and ask the user. Do not skip to later tasks.

## Finish

1. After the last task, run the repository's full build and test suite. Discover the commands from CI configuration, build files, and repository guidance. Fix failures inside the feature.
2. Run the [review loop](#review-loop) with the prompt `Run /code-judo <feature base>.` Look for problems that span tasks: duplication, abstractions only visible across the feature, and drifted layering. Keep per-task rejections unless the whole-feature view gives a new reason.
3. Commit the fixes from this review separately from the task commits. Rerun the full build and test suite before each new round.
4. Report completed and blocked tasks, the commits created, every rejected finding with its reason, and the final verification results.
