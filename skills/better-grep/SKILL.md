---
name: better-grep
description: MUST use for every repository search for files, code, configuration, documentation, symbols, behavior, or call sites. Skip only when the exact path to read is already known.
---

# Better Grep

Search internally with the fewest high-signal queries and file reads needed to answer the calling task. Do not narrate searches, emit a standalone report, or create an artifact.

## Protocol

1. **Define the evidence target.** Internally classify the question as path/layout, exact text or configuration, syntax shape, resolved symbol, or behavior/concept. Extract only useful identifiers, aliases, data shapes, entry points, and likely owners.
2. **Use repository knowledge narrowly.** If an OKF bundle exists, read its root index and only concepts relevant to the target. Treat concepts as a map, not proof; verify against current source. Continue without OKF when absent. Note stale or missing concepts for a later `docs-sync` decision, but do not edit documentation during search.
3. **Establish scope.** Start at the narrowest repository subtree supported by evidence. Honor repository ignore rules. Exclude generated, vendored, cache, and build output unless the question or a suspicious result implicates one of them.
4. **Choose the tool by evidence type.** Use the table below. Do not begin with broad regex when a semantic or structural operation answers the question directly.
5. **Read around decisive matches.** Read the containing construct and enough surrounding context to understand ownership and flow; do not read whole files when one section is sufficient.
6. **Trace applicable boundaries.** Follow definitions, references/callers, imports/exports and aliases, configuration/build ownership, tests/fixtures, generated inputs, and runtime registration or dispatch. Follow only boundaries relevant to the question.
7. **Widen deliberately.** If results are empty or suspiciously narrow, first verify root, query spelling, tool capability/index/parser, filters, and ignore behavior. Then widen one dimension at a time: path, file population, aliases/re-exports, behavior terms, tests/configuration, generated inputs, or runtime keys.
8. **Stop on evidence.** Stop when current source answers the calling task and expected relevant boundaries are traced or explicitly ruled out. Never convert `not searched`, `unsupported`, `parse mismatch`, or `unresolved` into `does not exist`.

## Tool choice

| Question | First choice | Use instead or next when |
|---|---|---|
| File or directory layout | Filename discovery/glob | Search tracked or ignored populations explicitly only when relevant |
| Exact string, key, flag, route, error, or configuration | Literal search, then regex for known variants | Structural or semantic identity becomes relevant |
| Parsed syntax shape | Structural AST search | Confirm parser/language and a known-positive pattern before treating an empty result as absence |
| Definition, references, implementations, or symbol identity | Language-server navigation when available | Fall back to targeted text/structural search when capability, project context, or index is unavailable |
| User-visible behavior or concept | Narrow text terms and likely entry points, then combine semantic/structural searches | Trace tests, configuration, registration, dispatch, and runtime boundaries |

A match proves only what its mechanism observes: text proves spelling, AST proves parsed shape, and language-server results prove what that server resolves in its current project context. Corroborate across mechanisms only when the question crosses those evidence types.

## Empty-result check

Before widening, classify an empty result:

- **no match:** the intended population was searched successfully;
- **not searched:** filters, ignore rules, root, or file population excluded candidates;
- **unsupported:** the semantic operation or language is unavailable;
- **parse mismatch:** the structural pattern or target did not parse as intended;
- **unresolved:** aliases, generation, reflection, configuration, or runtime ownership remain unknown.

Perform one controlled widening step at a time. Stop with internal uncertainty when further search has no evidence-backed direction; do not scan the repository indiscriminately.

## Internal handoff

Retain only what the calling task needs:

- exact paths, symbols, and relevant ranges;
- the decisive evidence chain;
- boundaries ruled out;
- unresolved uncertainty that changes the task's conclusion.

Do not expose routine queries, search ledgers, negative-result diagnostics, or OKF drift unless the calling task needs them.
