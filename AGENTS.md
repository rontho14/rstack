# Coding rules

Apply these rules to every task that builds, fixes, or refactors code. Work through the stages in order. Each stage ends with a check. Do not move to the next stage until the check holds.

Use `tdd` for tests when it is installed.

## 1. Understand the change

- Read the task and every file the change touches. Trace the real flow end to end.
- Find every path that reaches the code you will change: callers, constructors, and alternate entry points such as CLI commands, UI runners, scheduled jobs, and scripts that bypass the main pipeline.
- For a bug, name the root cause. A report names a symptom.

**Check:** you can list every caller and entry point the change reaches.

## 2. Decide whether the code needs to exist

- Build only what the task requires. When a need is speculative, skip it and say so in one line.
- When removing code solves the problem, remove it instead of adding code.

**Check:** every planned piece of code maps to a stated requirement.

## 3. Reuse what already exists

Search in this order and stop at the first that covers the need:

1. a helper, type, or pattern already in this repository;
2. the language's standard library;
3. a native platform feature, such as CSS over JavaScript or a database constraint over application code;
4. a dependency the repository already installs.

Never add a dependency for what a few lines can do.

**Check:** you searched the repository for an existing implementation before writing a new one.

## 4. Follow the repository's patterns

- Match the existing layering, naming, error handling, configuration, and file layout.
- Never introduce a new pattern, such as an abstraction, layer, library, convention, or directory structure, without the user's approval.
- When no existing pattern fits, or you are unsure how to build something, stop. Run `to-theory` on the design question and present its options to the user. The user chooses.

**Check:** every structure in the change has a precedent in the repository or the user's approval.

## 5. Write the least code that works

- Add no abstraction without a second use: no interface with one implementation, no factory for one product, no configuration for a value that never changes.
- Add no scaffolding for later and no temporary or stopgap implementation that a known follow-up will remove. When the complete shape does not fit the requested scope, state the limitation and ask the user.
- Use the fewest files and the shortest diff, in the place where the problem lives. Prefer boring code over clever code.
- Fix a bug once, in the shared function every caller routes through, instead of patching only the path the report names.
- When two options are the same size, take the one that is correct on edge cases.

**Check:** removing any line of the change would break a requirement.

## 6. Name things honestly

- Name files, functions, types, variables, and tests after what the code does or owns.
- Never name code after where it came from: a specification, task number, ticket, or planning document.
- When the change makes an existing name false, rename it in the same change.

**Check:** a reader who knows only the code understands every new or changed name.

## 7. Write no comments

- Add no explanatory comments, docstrings, TODOs, or commented-out code. Express intent through names, structure, and types.
- Allow only license headers, tool directives, generated-file markers, and doc comments that the repository's enforced checks require.
- Leave existing comments alone unless the change makes one false.

**Check:** the diff adds no comment outside the allowed list.

## 8. Log the repository's way

- Follow the repository's logger, levels, message format, and placement.
- Never log a failure and also throw it. Do one.
- Add no bracketed log-prefix constants and no constants file that exists only for log prefixes.

**Check:** every new log call matches an existing one in style and level.

## 9. Review the diff

Check the finished diff against each item. Report any item you traded off and why.

- **Performance:** no repeated work inside loops that could be done once, no query or network round trip per item where one batch fits, and an algorithm that holds at the data sizes the code will see. Optimize further only with measured evidence.
- **Memory and resources:** files, connections, subscriptions, timers, and listeners are released. Caches and collections are bounded. Long-lived objects do not hold references they no longer need.
- **Safeguards:** input validation at trust boundaries, error handling that prevents data loss, security measures, accessibility basics, and anything the user explicitly requested all remain.
- **Design patterns:** a pattern appears only when the repository already uses it for the same job or it removes code.
- **Simplicity:** a developer new to the repository can follow the change without explanation.

**Check:** every item holds or appears in your report.

## 10. Verify integration

- Search for every call site and constructor of each changed function, class, or module.
- Confirm each one passes any new parameter and handles any new behavior.

**Check:** the search shows no call site left on the old behavior.
