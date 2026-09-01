---
name: second-opinion
description: Use when the user asks for an independent or adversarial review of a finished plan or specification before implementation.
---

# Second Opinion

A plan reviewed by the model that wrote it inherits that model's blind spots. This skill is the **prompt you send to a separate LLM** — paste it (with the spec files) into whatever model you use for an independent review. No dispatch, no reviewer selection: the prompt below *is* the second opinion.

## 1. Locate the plan (spec structure)

Find the spec folder under `.omp/Specs/NNN-feature-name/`. If more than one candidate exists, ask which one — don't guess.

Load documents in this order (skip files that don't exist yet):

| Order | File | Role |
|-------|------|------|
| 1 | `PRD.md` | Scope, stories, acceptance criteria, open questions, decisions |
| 2 | `ARCHITECTURE.md` | Modules, paths, data flow, constraints |
| 3 | `DESIGN.md` | Layout, states, tokens, testIDs, copy |
| 4 | `INTEGRATION.md` | External contracts (BFF, WebView, APIs) |
| 5 | `TASKS.md` | Implementation breakdown (if present — post-refine / pre-orchestrator) |

Also grab context the spec references when relevant: linked ADRs in `docs/adr/`, kanban items in `docs/roadmap/items/`, and the original user request if it's not captured in `PRD.md`.

**Completion:** you have the full spec package (at minimum `PRD.md` + whatever sibling files exist), not a paraphrase or subset.

---

## 2. Send this prompt to your second-opinion LLM

Copy the block below verbatim. Replace `[SPEC_FOLDER]` with the folder name (e.g. `006-pulso-grid-tryon`). Attach or paste the spec file contents after the prompt.

```markdown
You are reviewing someone else's plan, not your own. You have no stake in it looking good.

## Spec under review

Folder: `.omp/Specs/[SPEC_FOLDER]/`

Documents attached (in pipeline order):
- PRD.md — scope, stories, acceptance criteria
- ARCHITECTURE.md — modules, paths, data flow
- DESIGN.md — layout, states, tokens, testIDs, copy
- INTEGRATION.md — external contracts (if present)
- TASKS.md — implementation tasks (if present)

## Your job

Argue against this plan. Do not summarize it back approvingly.

Review every attached document and find:

1. **Assumptions** — things taken for granted that might not hold in prod, on the totem, or with the BFF/WebView stack.
2. **Edge cases** — failure modes, empty states, offline/slow BFF, missing data, accessibility, kiosk constraints the spec is silent on.
3. **Spec / scope alignment** — places the plan does more or less than PRD asks for (scope creep or gaps). Cross-check ARCHITECTURE paths vs DESIGN testIDs vs INTEGRATION contracts.
4. **Verifiability** — acceptance criteria or tasks that can't be checked as done; vague "implement X" without a observable outcome.

For each category, list concrete findings with file references (e.g. `PRD.md` H2, `DESIGN.md` § estados). If you find nothing wrong in a category, say so explicitly — do not skip a category.

Do not propose rewrites unless tied to a specific finding. End with a short verdict: **proceed**, **proceed with fixes**, or **blocked** — one sentence why.
```

---

## 3. Triage findings with the user

Walk through the reviewer's findings one at a time. For each:

- **Accepted** — plan/spec changes
- **Rejected** — state why
- **Deferred** — flagged; plan unchanged for now

Every finding gets one of these three states. Nothing is applied silently.

---

## 4. Edit only what was accepted

Update spec files only for accepted findings. Touch only the sections those findings affect — typically `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, `INTEGRATION.md`, or `TASKS.md` in the same folder.

If you edited repo docs (`CONTEXT.md`, `docs/adr/`, etc.), invoke **`sync-doc-hub`** before finishing.

---

## Failure modes

- **Rubber-stamping** — the LLM praises the plan instead of hunting for holes. Re-send the prompt verbatim; add: "Your last response was too agreeable. Be adversarial."
- **Partial spec** — reviewing only `PRD.md` while ignoring `DESIGN.md` or `INTEGRATION.md`. Reload the full spec package from step 1.
- **Silent rewrite** — findings applied without user triage. Defeats the purpose; user must choose accept/reject/defer for each finding.
- **Vague ask** — sending "check this plan" without the fixed prompt in step 2. Produces generic feedback that isn't comparable run to run.
