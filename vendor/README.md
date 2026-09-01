# vendor

Verbatim upstream imports. Every file here was copied unmodified from its source
at the revision pinned in `SOURCES.md`, with the upstream `LICENSE` and
copyright notice intact. All three sources are MIT.

## Why the copies are committed

These directories are the baseline. Once upstream lands in its own commit,
`git diff <import-commit> -- vendor/<source>` shows exactly what rstack changed
and what came from upstream. Git is the version control; there is no second
mechanism to maintain.

That is also why the imports are **complete** rather than pre-filtered. Skills
rstack ends up rejecting are removed in a later, separate commit, so the
rejection is a recorded decision rather than an absence.

## Editing

Vendored files may be edited freely. `vendor/` is not frozen — it is a
provenance baseline, not a read-only mirror. Keep edits in commits separate from
imports so the two stay distinguishable.

## Re-syncing a source

1. Fetch upstream at its new revision into a scratch directory.
2. Diff old upstream against new upstream to see what changed upstream.
3. Apply the parts that matter on top of rstack's version, resolving against
   local edits.
4. Update the pinned revision in `SOURCES.md`.

## Relationship to rstack

- **pstack** is the source of truth for the harness. Where pstack and rstack
  disagree about how the harness works, rstack moves toward pstack.
- **cursor-team-kit** is cherry-picked, reviewed one skill at a time.
- **mattpocock-skills** is largely untried and under evaluation.

Per-skill decisions are recorded in `notes/`.
