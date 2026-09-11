---
name: setup
description: Use after installing rstack, when the user invokes setup, or when material repository workflow changes require installed skills and companions to be adapted.
---

# Setup

Adapt the installed rstack files in place. They belong to the user.

## Process

1. Inspect the repository, every installed rstack skill and companion, adopted design concepts, and the host runtime's rule capabilities.
2. Identify durable constraints or workflow decisions an agent cannot reliably infer from nearby files.
3. When `tdd` is installed, discover how the repository measures line coverage for new and changed code. If it cannot enforce the 80% threshold, make the missing command or alternative a material `grill-me` decision and record the settled policy in the installed guidance.
4. Run `grill-me` to resolve material choices the repository cannot answer.
5. For each adopted design concept, derive the repository files and artifacts it governs.
6. Prepare one concise preview: affected files, evidence, material rewrites, and thin runtime-rule routers.
7. Obtain one approval, then apply the full preview.
8. Validate edited Markdown, skill names, dependencies, companion references, rule scopes, and concept links.
9. After successful setup, ask whether the user wants to delete this one-time setup skill.

## Editing rules

- Change only affected skills, agents, templates, scripts, and rules.
- Use focused rewrites. Preserve purpose, triggers, safety rules, attribution, and unrelated local edits.
- Keep instructions minimal and agent-agnostic. Ordinary paths, tools, and conventions stay discoverable at runtime.
- Embed only durable exceptions and explicit user decisions.
- Reference repository guidance only when indispensable; inline only essential constraints.
- Remove generic branches made irrelevant by proven repository constraints.
- When the runtime supports scoped rules, generate thin routers that require reading applicable design concepts; do not copy their principles into rules.
- Do not edit application code or run its builds and tests.

## Reruns

Treat current installed files as authoritative. Preview and patch only instructions made stale by repository changes. Do not regenerate files or create a second adaptation convention.
