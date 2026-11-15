---
name: craft
description: MUST use for every task that builds, fixes, or refactors code, including dependency choices. Use it together with `tdd`.
---

# Craft

Write code that meets four parameters: logic, security, readability, and performance. Size is the tiebreaker among the shapes that meet all four. It is never the goal. A short diff that fails a parameter is wrong. A diff that adds code no parameter needs is also wrong, and that includes a check for something that cannot happen.

Work through the stages in order. Each stage ends with a check. Do not move to the next stage until the check holds.

When two parameters conflict, the earlier one wins: logic, security, readability, performance. Performance ranks with logic when the task or the repository states a budget, such as a time limit, a frame rate, or a memory cap.

The repository's own rules, its recorded decisions, and explicit user requests outrank every default in this skill.

## 1. Understand the change

- Read the task and every file the change touches. Trace the real flow end to end.
- Find every path that reaches the code you will change: callers, constructors, and alternate entry points such as CLI commands, UI runners, scheduled jobs, and scripts.
- For a bug, name the root cause. A report names a symptom.

**Check:** you can list every caller and entry point the change reaches.

## 2. Name the problem

- Restate what the code must do without project terms.
- When the problem has an established name, such as an idempotent write, a debounce, optimistic concurrency, a topological order, or a state machine, write the name, its standard solution, and its known failure modes. Use the standard solution instead of inventing one.
- When several established solutions fit and the repository settles none, stop, run `to-theory` when it is installed, and let the user choose.
- "No named problem, plain glue code" is a valid answer. Do not force a theory onto a simple change.

**Check:** you wrote the name with its failure modes, or said there is none.

## 3. State what is at stake

Before writing production code, write one line for each parameter in your response. Do not create a file for them.

- **Logic.** The inputs the code receives, the invariants it must keep, and the ways each call it makes can fail.
- **Security.** Each trust boundary the change touches and what crosses it.
- **Performance.** How large the data can get, how often the code runs, and which thread or request path runs it.
- **Readability.** Where a reader will look for this code and which existing code it should resemble.

A stake counts only when you can name the real caller or input from stage 1 that produces it. A failure mode from stage 2 counts when this code can reach it. Never invent a stake to look careful. When nothing is at stake on any parameter, write one line that says so and why.

**Check:** each line names a real caller or input, or says nothing is at stake.

## 4. Choose the shape

- Build only what the task requires. When a need is speculative, skip it and say so in one line. When removing code solves the problem, remove it.
- Reuse before writing. Search in this order and stop at the first that covers the need: this repository, the standard library, a native platform feature, a dependency the repository already installs. Never add a dependency for what a few lines can do.
- Match the repository's layering, naming, error handling, configuration, and file layout. Never introduce a new pattern without the user's approval.
- Start from the smallest shape that could work and test it against the stakes from stage 3. When it fails one, take the smallest shape that passes all of them, and say in one line what the extra code buys.
- Add no abstraction without a second use, no scaffolding for later, and no stopgap that a known follow-up will remove.

**Check:** every piece beyond the smallest shape answers a stake from stage 3.

## 5. Write to the parameters

Apply each rule where stage 3 found a stake. Where it found none, the rule adds nothing, so write nothing for it.

### Logic

- Handle each input class a real caller can send: empty, one, many, boundary values, and malformed.
- Handle or propagate the failure of every call that can fail. Write no empty catch, no ignored result, and no fallback value that hides a failure.
- Make changes that belong together in one atomic step. A failure halfway leaves the old state.
- Give shared mutable state one owner.
- Fix a bug once, in the shared function every caller routes through.

### Security

- Validate untrusted input once, where it enters. Inside that boundary, trust the types and do not check again.
- Never build a query, shell command, file path, or markup by joining untrusted text.
- Keep secrets and personal data out of source, logs, and error messages.
- Never weaken an existing safeguard, and add no permission the task does not require.

### Readability

- Name files, functions, types, variables, and tests after what the code does or owns, never after a specification, task number, or ticket. When the change makes a name false, rename it in the same change.
- Give each function one job. Prefer an early return over nesting and boring code over clever code.
- Treat these as tripwires: a function over 40 lines, nesting deeper than 3 levels, more than 4 parameters. When the change crosses one, restructure, or report why the longer form is clearer. Never split code only to get under a number.
- Add no explanatory comments, docstrings, TODOs, or commented-out code. Allow only license headers, tool directives, generated-file markers, and doc comments that the repository's enforced checks require.
- Log the repository's way. Never log a failure and also throw it.

### Performance

These hold by construction and need no measurement:

- The algorithm holds at the data size from stage 3. Nothing is quadratic or worse over data that can grow without bound.
- One batch replaces a query, file read, or network call per item.
- No blocking I/O or heavy computation runs on the UI thread or a request's hot path.
- Memory is bounded. Stream or page data that can grow, and release what you open.

Tuning needs a measurement first: caches, pools, memoization, precomputation, and hand-optimized code. Add one only when a measurement shows the problem.

**Check:** each stake from stage 3 has an answer in the code.

## 6. Prove it

- Use `tdd` for tests when it is installed.
- Cover each stake from stage 3 with a test or an executable check.
- For every guard, validation, and error path you added, name the input that reaches it through a real entry point. When you cannot, the branch is unreachable. Delete it.
- When stage 4 took a larger shape for security or performance, pin the reason with a test that fails if someone simplifies it away. When no cheap test exists, state the reason in the commit message.

**Check:** every added branch has a named input that reaches it.

## 7. Review the diff

- Reread the diff twice: once for a stake the code does not answer, once for code that answers no stake.
- Search for every call site and constructor of each changed function, class, or module. Confirm each one handles the new behavior.
- Hold only the code the change touches to this bar. Report a problem that predates the change. Do not fix it unless the task asks.

Report the stakes and how the code answers each, every tripwire crossed, every parameter traded off against an earlier one, and the problems you left alone. A change with nothing at stake gets a one-line report.

**Check:** the search shows no call site left on the old behavior.
