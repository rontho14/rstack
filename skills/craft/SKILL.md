---
name: craft
description: MUST use for every task that builds, fixes, or refactors code, including dependency choices. Use it together with `tdd`.
---

# Craft

Write code that meets four parameters: logic, security, readability, and performance. Size is the tiebreaker among the shapes that meet all four. It is never the goal. A short diff that fails a parameter is wrong. A long diff that adds code no parameter needs is also wrong.

Work through the stages in order. Each stage ends with a check. Do not move to the next stage until the check holds.

## Order of the parameters

When two parameters conflict, the earlier one wins:

1. logic;
2. security;
3. readability;
4. performance.

Performance ranks with logic when the task or the repository states a budget, such as a time limit, a frame rate, or a memory cap. Missing a stated budget is a wrong result.

The repository's own rules, its recorded decisions, and explicit user requests outrank every default in this skill.

## 1. Understand the change

- Read the task and every file the change touches. Trace the real flow end to end.
- Find every path that reaches the code you will change: callers, constructors, and alternate entry points such as CLI commands, UI runners, scheduled jobs, and scripts that bypass the main pipeline.
- For a bug, name the root cause. A report names a symptom.

**Check:** you can list every caller and entry point the change reaches.

## 2. State what is at stake

Before writing production code, write one line for each parameter in your response. Do not create a file for them.

- **Logic.** The inputs the code receives, the invariants it must keep, and the ways each call it makes can fail.
- **Security.** Each trust boundary the change touches and what crosses it: user input, files, network, URLs, clipboard, database, another process.
- **Performance.** How large the data can get, how often the code runs, and which thread or request path runs it.
- **Readability.** Where a reader will look for this code and which existing code it should resemble.

"Nothing at stake" is a valid line when you give the reason, such as "no trust boundary, the function only reads its own constants".

**Check:** all four lines exist, and each names something specific to this change.

## 3. Choose the shape

- Build only what the task requires. When a need is speculative, skip it and say so in one line. When removing code solves the problem, remove it.
- Reuse before writing. Search in this order and stop at the first that covers the need: this repository, the standard library, a native platform feature, a dependency the repository already installs. Never add a dependency for what a few lines can do.
- Match the repository's layering, naming, error handling, configuration, and file layout. Never introduce a new pattern without the user's approval. When no pattern fits, stop, run `to-theory` when it is installed, and let the user choose.
- Start from the smallest shape that could work and test it against the four lines from stage 2. When it fails one, take the smallest shape that passes all four, and say in one line what the extra code buys.
- Add no abstraction without a second use, no scaffolding for later, and no stopgap that a known follow-up will remove. When the complete shape does not fit the requested scope, state the limitation and ask the user.

**Check:** every piece beyond the smallest shape serves a named parameter, and no piece serves none.

## 4. Write to the parameters

### Logic

- Handle every input class from stage 2: empty, one, many, boundary values, and malformed. For text, include non-ASCII, combining characters, and very long input.
- Handle or propagate the failure of every call that can fail. Write no empty catch, no ignored result, and no fallback value that hides a failure.
- Make changes that belong together in one transaction or one atomic step. A failure halfway leaves the old state.
- Give shared mutable state one owner. Never check a value and act on it across a suspension point or a thread switch.
- Let the types rule out illegal states when that is cheap: one enum instead of two booleans, a required value instead of an optional the code assumes is present.
- Assume no ordering, uniqueness, locale, time zone, or clock behavior that nothing guarantees.
- Fix a bug once, in the shared function every caller routes through.

### Security

- Validate untrusted input where it enters: type, size, range, and format. Reject bad input. Do not repair it.
- Never build a query, shell command, file path, or markup by joining untrusted text. Use bound parameters, argument arrays, and the platform's escaping.
- Add no permission, entitlement, scope, or network destination the task does not require.
- Keep secrets, tokens, and personal data out of source, logs, error messages, and unprotected storage. Use the platform's key store.
- Make a failed check deny. An error inside an authorization or validation step never grants access.
- Use the platform or an installed dependency for cryptography, authentication, and parsing of hostile formats. Never write your own.
- Never weaken an existing safeguard to make a change fit.

### Readability

- Name files, functions, types, variables, and tests after what the code does or owns, never after a specification, task number, or ticket. When the change makes a name false, rename it in the same change.
- Give each function one job at one level of abstraction.
- Keep control flow straight: an early return instead of nesting, two functions instead of a boolean parameter that switches behavior.
- Prefer boring code over clever code.
- Treat these as tripwires: a function over 40 lines, nesting deeper than 3 levels, more than 4 parameters. When the change crosses one, restructure, or report why the longer form is clearer. Never split code only to get under a number.
- Add no explanatory comments, docstrings, TODOs, or commented-out code. Allow only license headers, tool directives, generated-file markers, and doc comments that the repository's enforced checks require. Leave existing comments alone unless the change makes one false.
- Log the repository's way: its logger, levels, message format, and placement. Never log a failure and also throw it. Add no log-prefix constants.

### Performance

Performance by construction is mandatory and needs no measurement:

- The algorithm and data structure hold at the data size from stage 2. Nothing is quadratic or worse over data that can grow without bound.
- One batch replaces a query, file read, or network call per item.
- Work that can be done once is not repeated inside a loop.
- No blocking I/O or heavy computation runs on the UI thread or a request's hot path.
- Memory is bounded. Data that can grow is streamed or paged. Every cache and collection has a limit. Files, connections, subscriptions, timers, and listeners are released.
- Queries filter and sort on indexed columns.

Performance by tuning needs a measurement first: caches, pools, memoization, precomputation, parallelism added for speed, and hand-optimized code. Add one only when a measurement shows the problem, and name the measurement in the report.

**Check:** each line from stage 2 has an answer in the code.

## 5. Prove it

- Use `tdd` for tests when it is installed.
- Cover each logic claim from stage 2 with a test or an executable check.
- When stage 3 took a larger shape for security or performance, pin the reason with a test that fails if someone simplifies it away. When no cheap test exists, state the reason in the commit message.

**Check:** a later reader can find why each non-obvious choice exists without asking you.

## 6. Review the diff

- Reread the finished diff against each parameter.
- Search for every call site and constructor of each changed function, class, or module. Confirm each one passes any new parameter and handles any new behavior.
- Hold only the code the change touches to this bar. Report a problem that predates the change. Do not fix it unless the task asks.

Report:

- the four lines from stage 2 and how the code answers each;
- every tripwire crossed and why;
- every parameter traded off against an earlier one;
- problems you saw and left alone.

**Check:** the search shows no call site left on the old behavior, and the report covers all four parameters.
