---
name: docs-sync
description: MUST use after repository code changes when an initialized OKF bundle is present, before the code-changing task is marked complete.
---

# Docs sync

Keep the repository's OKF bundle aligned with the current code. Concepts describe what exists now. Git and the bundle logs retain history.

Do not initialize an OKF bundle. When `docs/index.md` does not declare an OKF bundle and its coverage policy, report that `docs-sync` does not apply.

## Ownership and timing

The main orchestrator runs this skill after implementation has passed focused tests and independent review. Individual implementation and review agents do not run it. The orchestrator runs it again after all tasks to catch effects that span tasks.

Do not request a preview, approval, or human review. Finish the synchronization before the orchestrator marks the task complete.

## Establish the change set

1. Use the pre-task or delivery baseline supplied by the caller. Inspect every repository change from that baseline through `HEAD`, plus all staged, unstaged, and untracked changes.
2. If the caller supplies no baseline, discover the target or upstream branch from repository evidence and use its merge base. If neither exists, use the repository's root commit.
3. Include added, modified, renamed, and deleted repository-owned production code, configuration, schemas, and scripts, even when a file is outside the current task's stated scope.
4. Include tracked generated, vendored, and build files. They may expose a current contract or lead to the source input that owns it.
5. Exclude only untracked or ignored files that repository evidence identifies as disposable generated output, vendored dependencies, caches, or build products. Do not exclude an untracked source file merely because it is untracked.
6. Use tests as evidence of behavior, contracts, and edge cases. Do not create concepts that document tests themselves.

Use `better-grep` for repository discovery and evidence tracing.

## Map changes to concepts

Read `docs/index.md` first, then only the relevant indexes and concepts. Map changed code through:

- exact `sources[].resource` paths;
- concept links and resources;
- affected terminology, contracts, behavior, and invariants;
- the bundle's coverage and granularity policy.

A source-file change triggers review, not an automatic concept edit. When no concept maps directly, create one only if the current change introduces durable knowledge selected by the coverage policy.

## Synchronize the current state

- Rewrite a concept when current behavior, contracts, invariants, terminology, examples, lifecycle, or sources make it inaccurate or incomplete.
- Make a metadata-only edit when a source moved or was replaced without changing the concept's meaning.
- Make no concept edit for formatting, internal refactoring, or test-only changes that leave documented meaning unchanged.
- Treat current code as authoritative for implemented behavior. Make the smallest complete statement supported by repository evidence.
- Remove an obsolete concept when its subject no longer exists. Repair its incoming links and remove it from indexes. Do not retain it with `status: deprecated`.
- Keep concept bodies in the present tense. Do not add migration notes, drift warnings, before-and-after explanations, or commentary about removed behavior.
- Preserve explanations owned by other concepts as links instead of copying them.
- Keep every source entry exact and supported. Do not invent `author`, `usage_count`, `last_modified`, or other credibility signals.
- On every meaningful concept change, set `generated.by` to the executing agent's actor identity when the runtime exposes one, otherwise use `process:docs-sync`. Set `generated.at` to the current ISO 8601 timestamp with an explicit UTC offset.
- Do not add or retain `verified` on a concept touched by this skill.
- Record concept creation, update, move, and removal in the affected directory's `log.md`. Logs may describe the change; concept bodies may not.
- Update affected indexes after creating, moving, or removing concepts.

When evidence disproves existing text but does not support a replacement claim, remove the unsupported claim. Do not preserve stale text, speculate, or ask the user to decide.

## Validate and finish

Validate the bundle after editing. Fail completion when:

- required repository-profile metadata is absent or malformed;
- an internal source does not resolve;
- an internal concept link does not resolve;
- a reserved index or log has the wrong structure;
- an affected current-state claim lacks supporting repository evidence.

Return the baseline used, the code changes assessed, concepts created, updated, moved, or removed, the no-update decisions justified by the coverage policy, and validation results. A code-changing task is not complete until this result passes.
