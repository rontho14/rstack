---
name: add-design-reference
description: Use only when the user explicitly invokes add-design-reference to adopt or revise a design source that must guide design-affecting work in an initialized OKF bundle.
disable-model-invocation: true
---

# Add Design Reference

Turn a user-approved design source into actionable repository guidance and scoped runtime rules. A citation alone is not guidance.

## Prerequisites

Require an initialized OKF bundle with a selected design category and a runtime-rule convention established by `setup`. Run the missing setup skill before proceeding. Reuse those conventions; do not create another documentation or rule format.

## Process

1. Read the complete source and relevant repository evidence.
2. Inspect adopted design concepts and generated rules for overlap or conflict.
3. Extract the source's principles into actionable design rules, affected scopes, examples, and explicit exceptions.
4. Ask one question at a time only where applicability, interpretation, or conflicts require a user decision.
5. Resolve every conflict before adoption. Never choose precedence silently.
6. Show one preview containing the design concept, affected indexes and logs, and generated runtime-rule changes.
7. Obtain explicit user approval, then apply the full preview.
8. Validate metadata, sources, links, scopes, rule references, indexes, and logs.

## Design concept

Create one focused OKF concept per coherent set of rules. Use the repository's configured metadata profile and design concept type. Require at least one exact source pointing to the adopted external material or repository evidence.

The body states:

- the source and why the repository adopts it;
- actionable design rules;
- affected domains, components, artifact types, and file scopes;
- examples that disambiguate a rule;
- explicit exceptions;
- resolved relationships or precedence with other adopted concepts.

Do not copy explanations owned by another concept. Link to them.

## Automatic application

Every adopted design reference drives all design-affecting work in its declared scope, including planning, architecture, UI/UX, implementation, and review.

Update the runtime rules in the same operation. Use the host runtime's convention established by `setup`. Generate thin scoped routers that:

- match the relevant repository files or artifacts;
- require the agent to read the linked design concepts before deciding, implementing, or reviewing;
- contain no duplicated principle summaries.

Derive scopes from the repository and approved concept. Examples include frontend source paths for UI principles and specification paths such as `PRD.md` or `DESIGN.md` for planning guidance. Do not hard-code these examples when the repository uses different paths.

## Maintenance

Update the design directory's `index.md` and append one concept-level entry to its `log.md`. When a concept changes or is retired, update or remove every generated router that references it in the same approved operation.
