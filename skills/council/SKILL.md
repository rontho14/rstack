---
name: council
description: Use when the user says "council" or asks for a council review of a change, plan, or decision.
license: MIT
---

# Council

Before an audit, address outstanding PR comments, fix known issues, and run
relevant checks. Give council the updated implementation; do not defer known
fixes until reviews return. If the user wants to discard the implementation
and explore new ideas, skip fixes to code being replaced.

Bring in three delegates to help with the user's request, usually for review
or feedback. If the user's instructions name council members, use those.
Otherwise start three fresh subagents in parallel, in one message, with the
Agent tool, each with `model: opus` and `effort: medium`. If you cannot start
three delegates, or a named member is unavailable, report it instead of
substituting.

Give each delegate the same request and relevant context. Never show one
delegate another's response. For review or feedback, keep their work
read-only. Collect their responses and summarize the useful findings,
disagreements, and recommended next steps.

For a code review, ask each delegate for a score out of 10.
Count each full review pass as one round.
A fresh review after fixes starts a new round, with three new delegates.

If the work ends in a pull request, put the results in the PR description.
Put this section before the model and harness line at the end:

```markdown
## Council review

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| Opus 5.5 (1) | 7/10 | 9/10 |
| Opus 5.5 (2) | 8/10 | 10/10 |
| Opus 5.5 (3) | 7/10 | 9/10 |
```

If a delegate gives no score, write `no score`. Do not invent one.
If the PR is open, edit the description. Do not post a comment for this.
If there is no PR, put the same results in the final reply only.

If you agree with their recommendations, make the changes and request a fresh
review after. Continue this process until all delegates are satisfied with the
outcome.

Do not let repeated reviews result in scope creep. It is your job to fight to
keep scope limited.

## Source and license

Adapted from Theo Browne's [`council`](https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/skills/council/SKILL.md), licensed under the [MIT License](https://github.com/t3dotgg/tstack/blob/1085050f3baed1ac724caa4a8166145fb2ac88af/LICENSE).
