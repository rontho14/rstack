# Reference — create-tasks skill

Where to find atoms in the specs (`PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`,
`INTEGRATION.md`), how to order them, and a worked sizing example. The `TASKS.md` shape lives
in [TEMPLATE.md](TEMPLATE.md).

## Decomposition guide

The categories below are how you *find* atoms, not how you *package* them: SKILL.md steps 3
and 4 decide the tasks. Tests are not a category.

### Category 1: Config & constants

Source: `ARCHITECTURE.md` data model and contracts, and the naming table's config rows.

- New configuration values, limits, timeouts, and feature flags
- Enum or union extensions and the branches that read them

### Category 2: Pure helpers & data contracts

Source: `ARCHITECTURE.md` contracts (naming rules, formats, grammars, schemas).

- Name/path generators, command or query builders
- Serialization / encoding / format utilities
- Merge and dedup helpers
- Shared types, schemas, and validation models

### Category 3: Core behavior

Source: `ARCHITECTURE.md` system context and the naming-table rows for the feature's
services, modules, or pipeline stages.

- New services, handlers, jobs, processors, I/O adapters
- Changes to existing flows that implement a business rule
- Persistence and migration changes

### Category 4: User interface

Source: `DESIGN.md` (screen flow, layout, interactions, copy, element ids).

- New screens, pages, or components
- Behavior changes on existing screens (new states, interactions, copy)
- Element-id additions needed for tests

## Dependency rules

These rules order atoms. When both atoms land in the same task, the rule only orders the
work inside it. When they land in different tasks, it becomes a task dependency.

- Config and constants come before everything that reads them
- Schemas and shared types come before any code that builds or validates that data
- Helpers come before the core behavior that uses them
- Core behavior comes before the integration and wiring that call it
- A screen comes before the screen that navigates to it

Encode task dependencies in each task's `Dependencies` field and in the `## Dependency graph`
block at the bottom of `TASKS.md`.

## Sizing example

A feature has two user stories. **Export:** a user exports a report as CSV from the report
screen or from the CLI. **Nightly export:** every report is exported to storage each night,
with retries and an alert on failure. The specs name: a `CsvFormat` config constant, a
`formatCsvRow` helper with escaping rules, an `ExportService.exportCsv` method, an export
endpoint, a `--format csv` flag on the existing CLI `report` command, an Export button on the
report screen, a new CSV library dependency, and a scheduled job with its retry and alert
handling.

**Too fine: eight tasks**, one per atom. The constant and the dependency each burn a full
review loop on a diff no test can fail, and the helper, service, endpoint, flag, and button
each repeat the loop for pieces of one story.

**Too coarse: one task** with both stories. Neither story is small, and the export task alone
is already past half the size guide, so they cannot share a task.

**Packed: two tasks.**

1. *Export a report as CSV from the screen and the CLI.* Constant, dependency, helper,
   service method, endpoint, CLI flag, and button, with tests for the escaping rules, the
   endpoint, the flag, and the button. `Absorbed:` the constant and the dependency. One story,
   all of its scenarios, across every layer: about 12 files counting tests, under the size
   guide.
2. *Export every report nightly.* The scheduled job with its retry and alert handling,
   calling the service from task 1. Another story, so it starts a new task even though it
   builds on task 1.

If the escaping rules were a large grammar that other export formats share, the helper would
still go into task 1, the first slice that uses it. It would become its own task only if it
carries its own tests and task 1 stayed past the size guide even after splitting the export
story by scenarios.
