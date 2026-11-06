---
name: create-tasks
description: Use when the user asks to turn an approved specification set into TASKS.md or invokes create-tasks.
user-invocable: true
argument-hint: "Path to spec directory (e.g. specs/001-feature-slug)"
---

# Create tasks from spec (`/create-tasks`)

You read the **human-approved specs** and write **`TASKS.md` as a file** in the spec
directory. You do **not** implement application code and you do **not** create harness
tasks: `TASKS.md` is the ledger **`implement`** drives.

## Pipeline position

```
conversation       → specs written → [human approval gate]
/create-tasks      → writes specs/NNN-…/TASKS.md   ← you are here
/implement         → runs the per-task implement → code-judo loop on TASKS.md
```

`implement` takes tasks one at a time. Each task gets its own implementation pass, a fresh
`code-judo` review loop that repeats until the review approves, and its own commit. That loop
carries a fixed overhead whatever the task's size, which is why sizing is the core of this
skill.

## Inputs

The argument is a **path to a spec directory** (e.g. `specs/001-feature-slug`). If
empty, pick the most recent `specs/NNN-…` by numeric prefix. If ambiguous, ask which
spec to taskify.

## Workflow

### 1. Read the approved specs (read every spec before analysis)

Read the docs in this order. Pass through whatever exists: `DESIGN.md` and
`INTEGRATION.md` are optional.

1. `PRD.md`: narrative, business rules, user stories, **verifiable acceptance
   criteria** (Given/When/Then), out-of-scope
2. `ARCHITECTURE.md`: fit with the existing system, data/contract changes, and the
   **"New files and naming" table**
3. `DESIGN.md`: screen flow, layout, interactions, copy, element ids (only when the user
   interface changes)
4. `INTEGRATION.md`: only when a real cross-layer contract exists
5. Any accepted decisions and unresolved questions the spec directory records

Then read the host repository's code that the specs name, so ordering and `Target Files`
reflect the real code rather than the specs' description of it.

### 2. Find the atoms

An **atom** is one change the specs name: a row of the naming table, a `DESIGN.md` element,
a change to an existing file, or the code behind an acceptance scenario. The
[decomposition guide](REFERENCE.md#decomposition-guide) lists where to look.

Note which user story each atom serves. When the PRD does not group scenarios into stories,
scenarios that exercise the same capability form one story. When several stories need an
atom, it serves the one the others build on, or when none does, the first in the PRD's order.
When no story needs it, such as a refactor the architecture requires, it serves the story
whose code it touches, or the first story. When the specs have no stories at all, such as a
pure refactor, skip this paragraph: only the size guide and dependency order bound a task.

When an atom adds, changes, or removes a parameter, signature, or behavior of a shared
function, class, or module, search the code for every caller and constructor of it now,
including alternate entry points that bypass the main pipeline: CLI commands, UI runners,
scheduled jobs, and scripts. Each one belongs to that atom and never leaves it. A parameter
that is not threaded through an alternate entry point never reaches the work started there.

### 3. Set the floor: merge every atom that cannot carry a test

Apply the **test viability check** to every atom:

> Is there a test that exercises this atom itself, not only through a consumer, and would
> **fail** if the atom were done wrong: a new or changed test, or an existing test that
> covers the changed code?

- **Yes**: the atom can anchor a task. Step 4 decides what joins it.
- **No**: it is **not a task**. Merge it into the atom whose tests cover it, normally its
  only consumer or the code that first renders or calls it. When no test covers it, merge it
  into an atom of the story it serves (step 2). When no atom of that story passes, merge it
  into the story it builds on, or the nearest story in dependency order. When the specs have
  no stories, merge it into the nearest atom in dependency order.

If no atom passes, stop and tell the user the specs define nothing a task can verify, and
that `/implement` can take the change as a single task without a `TASKS.md`.

Atoms that almost never anchor a task on their own:

| Atom | Merge into |
|---|---|
| Dependency adds/removes, package manifest edits, lockfiles | The first atom that uses the dependency, or for a removal, the atom that stops using it |
| Token/theme/CSS layers, fonts, config constants with no branching | The first component or module that consumes them |
| Thin typed wrappers over an HTTP client or ORM (no logic beyond the URL and the type) | The hook, service, or screen that calls them, where they get exercised end to end |
| Test fixtures, mock handlers, shared test renderers | The first suite that consumes them |
| Copy-only or token-only presentational components | The page whose test asserts their rendered output |

Two rules keep the merge honest:

- **A merge changes no scope.** Every path the specs name is still built and every acceptance
  scenario still has a test: the work moves, it does not vanish. Record what moved in an
  **`Absorbed:`** line on the receiving task, naming the atom and why it could not carry a
  test, so the implementer builds it and a human reader can see nothing was dropped.
- **An atom that can carry a test keeps that test wherever it lands.**

### 4. Pack atoms into tasks up to the size guide

Step 3 sets the floor. The goal of this step is the **fewest tasks that each stay easy to
review**.

A task's **purpose** is normally one user story with all of its acceptance scenarios: the
contract, behavior, caller wiring, and screen that serve it form one **vertical slice**. A
different story starts a new task, whether or not it builds on this one, with one exception:
two or more stories share a task when every story after the first is small (one or two
acceptance scenarios) and the combined task stays under half the size guide below, or under
the full guide when they edit mostly the same `Target Files`. No story in the group may carry
a migration or a security-sensitive change (authentication, authorization, secrets handling,
or a new trust boundary), and no other task may need to sit between them in dependency order.

The **size guide** marks a task too big to review in one pass: more than about 15 files in
`Target Files` (tests included; lockfiles and generated files not counted) or about 500
changed lines. The file count is the main signal; estimate lines roughly from the number of
scenarios. Leave a mechanical change, the same edit repeated at each call site, out of both
counts: it stays easy to read at any size. Treat the numbers as a smell to check, not a hard
limit.

When one story alone crosses the size guide, split it into groups of whole acceptance
scenarios, each a vertical slice of its own, in dependency order. When the story has too few
scenarios to split, keep it whole and report it past the size guide. A shared foundation (a
helper, contract, or schema that several stories use) gets its own task only when it carries
new or changed tests of its own and its story stays past the size guide after that split.

Two rules override the size guide:

- **Every task leaves the repository building and its tests passing.** Callers travel with
  the change that needs them (step 2), even past the size guide.
- **The floor wins.** An atom that cannot carry a test never becomes a task of its own, even
  when keeping it in a task pushes that task past the size guide.

When a task is still past about twice the size guide, ask the user before keeping it, even
when the story cannot be split.

Among the packings the story rule allows, when one larger task and two smaller ones both fit
under the size guide, pick the larger one. Past the size guide, an oversized task risks review
findings that keep coming back, which marks the task `BLOCKED` and stops the whole run.

The signal that you have packed too little: two tasks that serve the same story and together
fit under the size guide, two tasks the small-story exception would have combined, or a task
that exists only to wire up what the task before it built.

### 5. Order the tasks

Order tasks so each one builds only on tasks before it, using the
[dependency rules](REFERENCE.md#dependency-rules). A task that holds a shared atom (step 2)
comes before every task whose story needs it.

### 6. Write TASKS.md

Write **`specs/NNN-feature-slug/TASKS.md`** by copying [TEMPLATE.md](TEMPLATE.md) and filling
in its header, one task block per task, and the dependency graph.

- `Target Files` lists every file the task creates or edits, including its test files and
  the callers step 2 found. Take each path from the specs or from the repository code read in
  step 1, following the repository's existing layout for new and test files. Never write a
  path neither source supports.
- `Tests` names the tests that would fail if the task were done wrong, the same check as
  step 3.
- `Success Criteria` trace back to the task's acceptance scenarios, or, for a foundation task
  or a task with no acceptance scenarios, to the tests it carries. `implement` proves them
  before review; the `code-judo` reviewer never sees `TASKS.md`.
- Every task starts `Status: PENDING` and `Review Rejections: 0`. `implement` owns these
  fields from here on.
- The pre-review gate line names the commands that lint, test, and build the code the
  feature touches. They define what "the repository builds and its tests pass" means for
  every task. Take them from the host repository (its `AGENTS.md`, package manifests, task
  runner, or CI configuration) and never invent one. When the feature spans several projects
  in the repository, name the gate for each.

### 7. Check coverage and report

Before reporting, confirm that every path the specs name for in-scope work appears in some
task's `Target Files`, every acceptance scenario in some task's `Success Criteria`, and every
atom from step 2 in some task's `Description`, `Absorbed` line, or `Success Criteria`. Fix any
gap.

Print the path you wrote and a short summary: total task count, which tasks are
**unblocked now**, what step 3 absorbed and into what, any task past the size guide with the
reason, and any CI/CD or infrastructure work the specs need, as human-only work. Then tell
the operator to commit the spec directory, because `implement` stops on uncommitted changes,
and run **`/implement <path to TASKS.md>`**.

## Rules

- **Stop at 15 tasks.** When more than 15 tasks remain after packing, stop and ask the user
  whether the spec should be split into separate features; never pack past the size guide to
  meet the count.
- **Create no task for excluded work:** anything the PRD or a decision marks out of scope or
  deferred, unresolved questions, CI/CD or infrastructure changes, documentation files the
  specs do not name (the specs are the documentation), and smoke-script or install-check steps
  (`implement` runs the full build and test suite after the last task).
- **Don't overwrite a TASKS.md `implement` is already driving.** If any task block in an
  existing one has a `Status` other than `PENDING` or `Review Rejections` above 0, stop and
  confirm before regenerating.
