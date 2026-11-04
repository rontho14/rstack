---
name: second-opinion
description: Use when the user asks for an independent or adversarial review of a finished plan or vision before implementation. Not for reviewing written code.
---

# Second Opinion

A plan reviewed by the agent that wrote it inherits that agent's context and blind spots. Hand the plan to a fresh reviewer that argues against it, checks it against the code, and proposes a different approach. The user decides what changes.

Work through the stages in order. Each stage ends with a check. Do not move to the next stage until the check holds.

## 1. Gather the plan

Resolve the plan in this order and stop at the first that applies:

1. what the user names: a path, folder, link, or pasted text;
2. the plan or vision produced or discussed in the current conversation; say which one;
3. specification folders under `.claude/` and `.cursor/`.

When more than one candidate remains, ask which one. Never guess.

Collect every document the plan consists of and every document, decision record, or work item it references.

**Check:** you hold the full plan, not a paraphrase or subset, and can list its documents.

## 2. Run the review

Spawn a fresh subagent. Use the model the user names; otherwise use the current conversation's model. Its entire prompt is the [review prompt](#review-prompt) with the plan's location filled in, or the plan's text when it lives only in the conversation. Add nothing: no summary, expectation, or defense of the plan.

**Check:** the reviewer returned a report with every category and a verdict.

## 3. Show the review

Show the user the reviewer's report exactly as returned. Do not summarize, filter, or rebut it.

**Check:** the user has seen the unedited report.

## 4. Triage with the user

Walk through the findings one at a time. Give each one state:

- **Accepted**: the plan changes.
- **Rejected**: record the user's reason.
- **Deferred**: the plan stays unchanged for now.

When the user chooses an alternative approach, write the `to-theory` translate-back brief for it in the plan's terms and have the user confirm the brief before editing.

**Check:** every finding has a state.

## 5. Edit what was accepted

Edit the plan's documents only for accepted findings and confirmed briefs. Touch only the sections they affect.

**Check:** every edit maps to an accepted finding or a confirmed brief.

## 6. Report

List every finding with its state: what was edited for each accepted finding, the reason for each rejection, and each deferred finding.

## Review prompt

```markdown
You are reviewing someone else's plan, not your own. You have no stake in it looking good.

Plan: [PLAN_LOCATION_OR_TEXT]

Read every document of the plan and everything it references. Read the code it describes or depends on. Do not edit any file.

Argue against the plan. Do not summarize it back approvingly. Report concrete findings in each category below, citing the document and section and, for code, the file and line. When a category has no findings, say so explicitly. Do not skip a category.

1. **Vision**: for the parts that state the problem, users, scope, and success. Look for the wrong problem, success that cannot be measured, scope without a clear edge, contradictions, and solutions stated as requirements.
2. **Assumptions**: claims about the existing code, data, or environment. Verify each against the code. Report the ones that are false or unverified.
3. **Edge cases**: failure modes, empty and missing data, slow or unavailable dependencies, concurrency, and accessibility that the plan is silent on.
4. **Alignment**: places the plan does more or less than its vision asks, and contradictions between its documents.
5. **Verifiability**: acceptance criteria or tasks that cannot be checked as done.
6. **Different approach**: run `to-theory` on the plan's central design problem with these changes:
   - Confirm the theory gate yourself from the plan and the code. Do not wait for a reply.
   - Record each parameter you cannot establish as an assumption instead of a question.
   - Do the research step yourself against primary sources and cite them inline. Do not run `research` or write a file.
   - Stop after the options and decision criteria. Do not choose an option or write the translate-back brief.
   - List at least one option whose mechanism differs from the plan's.

Propose changes only when tied to a specific finding. End with a verdict, **proceed**, **proceed with fixes**, or **blocked**, and one sentence why.
```

## Failure modes

- **Rubber-stamping**: the report praises the plan instead of hunting for holes. Spawn a new fresh reviewer with the same prompt plus `Your last response was too agreeable. Be adversarial.` Do not argue with the earlier reviewer.
- **Partial plan**: the reviewer saw only part of the plan. Return to stage 1.
- **Silent rewrite**: findings applied without triage. Every edit needs the user's acceptance.
