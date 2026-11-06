# Tasks: {feature name}

Pre-review gate: `{the repository's lint, test, and build commands for the code this feature touches}`

## Task 1: {imperative verb + what}
- **Description**: {what to implement, naming each atom the task builds, and which spec file governs it}
- **Absorbed**: {atoms merged in and why each could not carry a test — omit the line when nothing was merged}
- **Dependencies**: {task numbers, or —}
- **Target Files**: [{every file the task creates or edits, including tests and callers}]
- **Tests**: {the tests that would fail if this task were done wrong, and what they prove}
- **Success Criteria**:
  - {Verifiable goal 1, traced to an acceptance scenario, that the verification skill can prove}
  - {Verifiable goal 2}
- **Status**: PENDING
- **Review Rejections**: 0

## Dependency graph

```
#1 ──→ #2 ──→ #4
  └──→ #3 ──┘
```
