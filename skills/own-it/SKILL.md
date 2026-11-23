---
name: own-it
description: Use only when the user explicitly invokes /own-it or /own-it done with spec <id> to think through a feature plan, save a work note for /create-spec, and quiz them after implementation.
disable-model-invocation: true
argument-hint: "[done with spec <id>]"
---

# Own it

Run only when the user invokes this skill. `/own-it` starts the feature thinking session. `/own-it done with spec <id>` reviews a finished spec. Do not start this workflow because the user asked to build, change, or demo something.

Do not write product code. Do not write `SPEC.md`, `PRD.md`, `TECHNICAL.md`, or `TASKS.md`. Do not invoke `/implement`. Do not describe how `/second-opinion` works.

Teach in plain language, one question at a time. The user answers in their own words. When an answer is missing, teach that slice with this change as the example, then ask the same question again. Do not supply the answer for them to approve. Do not ask for function names, file names, or line-level detail.

Paths follow the workspace convention (for example, under `.cursor/` or `specs/`):

- Session note: `<own-it-dir>/work/<id>.md`
- Spec: `<spec-dir>/<id>/SPEC.md`
- Second-opinion review: `<own-it-dir>/review/<id>.md`
- Shipped record: `<own-it-dir>/shipped/<id>.md`

In a multi-repo workspace, `<id>` is `<repo>--<feature>` (where `<repo>` is the target repository, such as `billing-api`). In a single-repo workspace, `<id>` is `<feature>`.

## Start

If the invocation is `done`, follow [Done](#done). Otherwise follow [Before](#before).

## Before

1. Ask which repository this change belongs to in a multi-repo workspace, unless they already named it. Ask what the feature is, unless they already named it. Set `<id>`.
2. Ask for a hypothesis in their words. Do not propose an approach until they have stated one.
3. Ask whether they want help thinking, or the thinking done for them. Record the answer in the session note.
4. If they do not know this part of the repo, do a blind-spot pass. Read the repo. Teach the unknowns that would change the approach, in plain language. Then continue.
5. Interview them one question at a time. Ask only questions whose answer would change the approach. Stop when further questions would not change it.
6. When more than one approach is open, describe the options in the chat. Record the one they pick.
7. Walk these four topics, one at a time. Teach the idea when they do not have it yet. Record each answer in their words.
   - Why this approach and not the other.
   - What a malicious actor could do.
   - What data structure is used and why.
   - Where it fails.
8. Ask what would make this wrong.
9. Draft the verified sentence: the evidence that checks the answer from step 8. They edit it until they understand it. Record it in the session note.
10. Write or finalize `<own-it-dir>/work/<id>.md` with their mode, hypothesis, decisions (marking which are confirmed vs. pending stakeholder confirmation), non-repo facts discovered (ticket notes, staging probes, stakeholder answers), the four topics in their words, what would make this wrong, the verified sentence, and open questions.
11. Give the handoff below and stop.

### Handoff

Tell them the pipeline from here with `<id>` and real paths filled in, then stop:

1. Run `/create-spec <id>` in a fresh session to write `<spec-dir>/<id>/SPEC.md` from `<own-it-dir>/work/<id>.md`.
2. Run `/second-opinion` on `<spec-dir>/<id>` and save the unedited review to `<own-it-dir>/review/<id>.md`.
3. After triaging findings and resolving blocking questions, run `/create-tasks <spec-dir>/<id>`, then `/implement` on `<spec-dir>/<id>/TASKS.md`.

## Done

`<id>` is the argument after `done with spec`. It is the spec folder name.

1. Open `<spec-dir>/<id>/SPEC.md` (or `PRD.md` and `TECHNICAL.md` for older specs), `<spec-dir>/<id>/TASKS.md`, `<own-it-dir>/work/<id>.md`, and `<own-it-dir>/review/<id>.md` if present. If the spec is missing, say so and stop.
2. In the target repository, compare the current branch with the branch it came from. If you cannot tell which branch that is, ask. Read that diff before you summarize it.
3. Run the verification commands named in the spec's `Verification oracle` (or the verified sentence in older specs) in that repository. Show each command and its output before any summary. If any evidence requires manual inspection, ask them to bring it and wait.
4. Update the session note at `<own-it-dir>/work/<id>.md` with a `Done review` section. Include the spec path, the branch comparison, the commands and outputs or evidence they brought, where the result differs from the spec, and what the check showed.
5. Quiz them one question at a time. Cover what the check proved, what it did not prove, which decisions were made, and what was missed. Then ask the four topics from `work/<id>.md` again, about the code that was built. When the built result differs from the spec, ask about that difference.
6. The work is done when they can answer. Write the shipped record at `<own-it-dir>/shipped/<id>.md`: the decisions, what the check proved, what it did not prove, their answers, and the spec path.
