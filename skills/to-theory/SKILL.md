---
name: to-theory
description: Use only when the user explicitly invokes to-theory to reframe a concrete technical or engineering-organization problem as a known theoretical problem and compare source-backed options.
disable-model-invocation: true
---

# To Theory

Strip business terminology and personal context from a problem, name the known problem class it belongs to, and present the approaches that theory and practice have established for it. The user decides. Never recommend an option.

## Scope

Accept software and system design problems, and delivery or team-process problems with established theory behind them. Decline personal, product-only, and business-only decisions in one sentence instead of forcing a theory onto them.

## Process

1. Read the pasted material and the code it points to. Follow references as far as needed to establish the parameters that could change which approach fits, such as data size, frequency of the special case, round-trip cost, and component ownership.
2. Present the theory gate and wait for the user's reply.
3. Correct the mapping, framing, and parameters until the user confirms them.
4. Run `research` on the confirmed abstract problem and its candidate problem classes. The saved note contains only abstract theory: no user terms, mapping, or parameter values.
5. Present the options and decision criteria.
6. When the user chooses, write the translate-back brief and stop.

## Theory gate

1. **Mapping.** A two-column table, *user term → abstract role*, covering every business or project term the abstraction replaces.
2. **Abstract problem.** The problem restated in the abstract roles only.
3. **Problem class.** Its established names and a brief explanation of the theory, enough for the user to judge whether it matches the real problem.
4. **Parameters.** Each parameter that discriminates between approaches, marked found (with its source) or unknown.
5. **Questions.** Only for unknown parameters that could change the choice.

Do not start research before the user confirms the gate.

## Options

List at most five. Admit an option only when:

- a primary source describes it;
- its mechanism differs from every other listed option; fold variants into their parent;
- it violates no invariant the user confirmed.

List options that exceed the user's current scope or ownership, and flag what they require. List fewer than five when fewer qualify; never pad.

For each option give:

- its established name and mechanism;
- its cost profile along the confirmed parameters;
- when it wins;
- risks and failure modes;
- links to its sources in the research note.

Close with decision criteria: which parameters separate the options, and how the confirmed parameters score against each. Do not rank the options or name a preferred one.

## Translate-back

Map the chosen option back through the confirmed mapping into a short brief:

- what changes, in the user's terms;
- affected components or files;
- the invariant it protects;
- done criteria.

Do not plan or implement.

When the decision sets repo-wide or cross-component direction and `create-adr` is installed, offer it in one line, citing the research note as a decision input. Offer nothing for code changes or feature-local implementation decisions.
