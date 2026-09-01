# rstack
A portable collection of Agent Skills.

## Writing skill descriptions

The `description` field is routing context sent to the model on every call. Write it as a concise instruction for when to load the skill, not as a summary of what the skill contains.

- Start with `MUST use`, `Use when`, or `Use only when`.
- Use one to three sentences with concrete triggers.
- Keep procedures and implementation details in the skill body.
- Use positive triggers rather than overlap rules.
- Pair `Use only when` with `disable-model-invocation: true` when the host supports that metadata.

Example:

```yaml
description: MUST use whenever producing user-facing prose, including explanations, plans, documentation, reviews, and summaries.
```
