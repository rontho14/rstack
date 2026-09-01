---
name: nuke
description: Use only when the user explicitly invokes nuke for a final pre-push audit of the completed local implementation.
disable-model-invocation: true
---

# Nuke (pre-push implementation audit)

Maintainability check at the **end of the pipeline** — after orchestrator, reviewers, and tests, **before commit/push** in the nested git repo (`miniapp-beleza` or `bff-java-concept-store`).

**Philosophy:** judge the **feature implementation the team just built**, not whether files are already committed. Do not fix what is not broken. Judge only what **this feature introduced or worsened**. Pre-existing debt is out of scope unless the new work made it harder to reason about.

---

## When to run

| Run | Do not run |
|-----|------------|
| Human explicitly requests `nuke` or `/nuke` (optional: `@.cursor/specs/NNN-feature`) | `feature-planning-validation`, `feature-orchestrator`, per-task review |
| Feature work finished locally; tests/typecheck green | Mid-task or “while implementing” |
| Immediately before commit/push | To block or replace `code-reviewer` / `ux-reviewer` |

---

## Scope — implementation delta, not git hygiene

Nuke answers: **“Is this feature’s code ready to ship?”** — not **“Is everything committed?”**

### What counts as in scope

1. **Active spec** (when provided) — read `.cursor/specs/NNN-feature/` (`PRD.md`, `ARCHITECTURE.md`, `TASKS.md` target files). Those paths define the implementation surface.
2. **Working tree** — include **all** local implementation artifacts:
   - committed on the branch
   - staged
   - unstaged
   - **untracked** — if they are part of the feature work (new components, assets, test mocks, etc.), they are **in scope** and **not** a blocker merely for being untracked.
3. **Git diff** (branch vs `main` / `origin/main`, operator may override base) — useful signal, **not** the sole source of truth. If diff lags behind the working tree, **prefer reading the files on disk**.

## Git

`app-farma` is not a git repo. Nuke and commit **inside** `miniapp-beleza` (vs `main`) or `bff-java-concept-store` (vs `master`).

```text
1. Operator spec path → ARCHITECTURE paths + TASKS.md Target Files + POOP.md
2. git status + git diff inside the nested repo
3. Read touched files on disk (including untracked)
```

### Out of scope

- Repo-wide refactors, “while we’re here” cleanups, untouched modules.
- **Never** flag `untracked`, `not staged`, or “push without commit” as blockers — the expected order is **nuke → commit → push**.
- Spec-compliance gate — use spec only for **intent/context**, not to `[REJECT]` missing TASKS checkboxes.

---

## Primary questions (implementation delta)

For each meaningful file in the feature surface, ask:

1. Did this feature add **spaghetti** in shared paths (`src/components/`, global hooks, `src/services/apiClient`)?
2. Did any **touched** file cross **1000 lines** because of this feature?
3. Did **feature logic leak** (business rules in presentational components, kiosk logic scattered outside `features/` or `src/services/kiosk.ts`)?
4. Did the work add **unsafe types**, unstable hook/effect dependencies, or **duplicate helpers**?
5. Did the work add avoidable sequential orchestration or non-atomic Redux updates?

---

## Project rules (new violations only)

| Area | Check |
|------|--------|
| `src/` | `.cursor/docs/05-quality/typescript-strict.md`, `error-handling-performance.md` on **new lines** |
| Features | New code under `src/features/<name>/` per `.cursor/docs/01-architecture/directory-structure.md` |
| Hooks / effects | Unstable deps; kiosk auto-start side effects documented |
| `android/` | Minimal native surface; no UI logic in Kotlin/Java unless spec requires |
| Theme | No hardcoded hex; use `src/theme/` tokens |

Do **not** block on pre-existing violations in untouched lines.

---

## Explicit non-goals

- No ambitious architecture rewrite.
- No demand to refactor unrelated, pre-existing code.
- Do **not** run the full test suite unless the human asks (`npx tsc --noEmit` is enough for a quick type sanity check).
- Do **not** edit application code; produce a report only.
- Do **not** treat missing `git add` / uncommitted files as `FIX BEFORE PUSH`.

---

## Output format

Start with exactly one verdict line:

```text
SHIP
```

or

```text
FIX BEFORE PUSH
```

Then:

### Blockers (max 5)

Each bullet: file path, what changed, why it’s a regression, minimal fix direction.

**Valid blockers:** spaghetti, logic leak, unsafe types, duplicate consent flows, missing assets referenced in code, broken imports, new hardcoded theme violations, files >1000 lines from this feature.

**Invalid blockers:** untracked status, “commit before push”, diff empty while working tree has the feature.

### Optional (max 3)

Prefix each with `Optional:`.

### Pre-existing debt ignored

One short line if debt was correctly excluded.

---

## Relationship to the pipeline

Human workflow: Plan → orchestrate → review loop → tests green → **nuke** → **commit** → **create-pr**

Nuke runs on the **implementation as built**; commit packages it afterward.
