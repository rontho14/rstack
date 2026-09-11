# rstack plan

## Goal

Turn rstack into a portable collection of Agent Skills that can be installed from GitHub and adapted to the conventions of the repository where they will run.

## Product shape

rstack contains:

- standalone skills for focused jobs;
- an optional planning and delivery pipeline;
- reusable agent roles used by that pipeline;
- lightweight specification templates;
- a `setup` skill that configures the installed collection for its host repository.

Each skill owns one clear behavior. Skills may compose other skills through documented names and contracts.

## Installation experience

The README will offer two installation paths.

### Agent-assisted installation

Users ask their agent to install all of rstack or selected skills directly from the GitHub repository.

Example:

```text
Read the rstack skill catalog from <GitHub repository URL>. Explain the
available skills, ask which ones I want, and install the selected skill
directories into this project's Agent Skills directory. Preserve each skill's
companion files. Then run /setup for this repository.
```

The README must give agents enough information to:

1. locate each skill directory;
2. copy the selected directories into the host's Agent Skills location;
3. preserve `SKILL.md` and any companion files;
4. report which skills were installed;
5. run `setup` when requested.

### Manual installation

Users may clone or download rstack and copy selected directories from `skills/` into their agent's skills directory.

The README will use generic placeholders for the destination because Agent Skills hosts may use different installation paths.

## Repository contract

All maintained skills will follow these conventions:

- one directory per skill;
- `SKILL.md` as the entry point;
- frontmatter `name` matching the directory name;
- frontmatter `description` written as a concise routing instruction: when the model must or should load the skill, including trigger conditions and exclusions where needed; the skill body owns purpose and procedure because `description` is sent to the model on every call;
- repository-relative discovery of files, commands, and conventions;
- declared dependencies on other rstack skills;
- declared external capabilities when a skill needs them;
- examples based on neutral projects;
- companion scripts and references stored inside the owning skill directory;
- observable completion or verification criteria;
- source attribution and license information for adapted third-party work;
- one-time setup skills ask after successful completion whether the user wants to delete the installed skill;

## Skill catalog

### Standalone skills

| Skill | Purpose | Planned work |
|---|---|---|
| `ponytail` | Produce the least code that works without removing necessary safeguards | Refined; acceptance exercise remains |
| `tdd` | Establish a useful executable check before production code changes | Initial skill created; acceptance exercise remains |
| `lazy-plan` | Produce the smallest plan that safely unblocks work | Review wording and portability |
| `unslop` | Remove generic AI writing patterns while preserving meaning and voice | Preserve behavior; add attribution |
| `research` | Investigate primary sources and save cited findings | Make background delegation capability-aware; add attribution |
| `grill-me` | Stress-test an idea through rounds of independent decisions | Preserve frontier-based rounds; add attribution |
| `ask-me` | Explore a design through one dependent question at a time | Clarify its sequential contract |
| `second-opinion` | Prepare an adversarial review of a completed plan or specification | Make referenced documents conditional |
| `debug` | Diagnose runtime failures from evidence | Generalize evidence capture and project discovery |
| `code-review` | Run a thermo-nuclear maintainability review of current Git changes | Rebuilt from Cursor's skill; acceptance exercise remains |
| `create-pr` | Create a pull or merge request from the current repository state | Discover provider, target branch, template, and issue context |
| `get-work-item` | Load an issue or card and turn it into a verified work brief | Generalize the current card-loading behavior and rename it |
| `setup` | Adapt installed rstack skills to the host repository | Initial skill created; acceptance exercise remains |
| `okf-setup` | Establish a focused OKF v0.2 knowledge bundle for the host repository | Initial skill created; acceptance exercise remains |
| `create-adr` | Record or supersede a consequential architecture decision in the repository's OKF bundle | Initial skill created; acceptance exercise remains |
| `add-design-reference` | Adopt actionable design guidance and generate scoped runtime-rule routers | Initial skill created; acceptance exercise remains |
| `better-grep` | Search code efficiently using query planning, repository structure, and OKF | Complete |
| `map-codebase` | Map approved repository sections in parallel for OKF synthesis and codebase navigation | Initial skill created; acceptance exercise remains |
| `docs-sync` | Update affected OKF concepts after code changes | Initial skill created; acceptance exercise remains |
| `fix-maven-vulnerabilities` | Remediate reported Maven dependency vulnerabilities without breaking dependency resolution or builds | Initial skill created; acceptance exercise remains |

## Optional planning and delivery pipeline

The retained workflow is:

```text
planner
   ↓
refine-specs
   ↓
create-tasks
   ↓
orchestrator
```

`ask-me`, `grill-me`, and `second-opinion` remain standalone. A user may invoke them before, during, or after specification work.

This pipeline starts from one existing task, issue, or work item. One specification directory represents that one item. The pipeline refines and delivers bounded work; project inception and initial backlog creation will belong to a separate future skill.

### `planner`

Responsibilities:

1. inspect the request and relevant host-repository conventions;
2. choose the host repository's existing specification location, or establish one through `setup`;
3. create the specification directory for the current task or issue;
4. create the documents justified by that item;
5. record unresolved decisions;
6. stop before implementation.

Documents:

- `PRD.md` for the problem, scope, requirements, and acceptance criteria;
- `ARCHITECTURE.md` for affected components, boundaries, data flow, and implementation constraints;
- `DESIGN.md` for user interaction, states, copy, and accessibility when the feature has a user-facing design;
- `INTEGRATION.md` for contracts across components or external systems when such boundaries exist.

### `refine-specs`

Responsibilities:

1. read the active specification set and relevant repository documentation;
2. identify ambiguous behavior, terminology, boundaries, contracts, and acceptance criteria;
3. resolve decisions with the user;
4. update the affected specification documents as decisions settle;
5. finish with a coherent, verifiable specification set.

Normalize the directory and frontmatter name to `refine-specs`.

### `create-tasks`

Responsibilities:

1. consume the approved specification set for the single task or issue;
2. identify implementation units needed to deliver that item from its documented architecture and acceptance criteria;
3. combine units that cannot deliver independently verifiable behavior;
4. order units by real dependencies;
5. create `TASKS.md` as the implementation ledger inside that item's specification directory, with target areas, success criteria, verification, status, and review history.

Task categories come from the feature and host repository rather than a fixed technology list.

### `orchestrator`

Responsibilities:

1. select the next dependency-ready task;
2. assign or perform implementation;
3. require focused verification evidence;
4. run an independent review when the runtime supports suitable agents;
5. route rejected work back for correction;
6. update `TASKS.md` after each completed gate;
7. run final integration verification after all tasks are complete.

The orchestration contract remains stable whether one agent performs the roles sequentially or the runtime provides separate agents.

## `setup` skill

### Purpose

Adapt the installed rstack skills and their required companions to durable conventions of the host repository. Installed copies belong to the user and may be changed directly.

### Workflow

1. Inspect every installed rstack skill and companion alongside the repository.
2. Discover repository guidance, architecture, workflows, and agent capabilities without relying on a fixed file list.
3. Identify only durable exceptions or decisions an agent cannot reliably infer from nearby files.
4. When `tdd` is installed, discover how the repository measures line coverage for new and changed code. If it cannot enforce the 80% threshold, settle and record the alternative through `grill-me`.
5. Run a `grill-me` session to resolve material choices that repository evidence cannot answer.
6. Propose one concise preview listing affected files and material rewrites.
7. Obtain one approval, then apply focused rewrites only to affected skills and companions.
8. Preserve each skill's purpose, triggers, safety rules, attribution, unrelated local edits, and agent-agnostic behavior.
9. Remove generic branches made irrelevant by proven repository constraints.
10. Reference authoritative repository guidance when useful and inline only essential constraints.
11. Validate the edited Markdown, names, dependencies, and companion references.
12. After successful setup, ask whether the user wants to delete this one-time setup skill.

The skill does not execute project builds or test commands. It edits agent guidance, not application code.

### Reruns

Treat current installed files as authoritative. Patch only instructions made stale by repository changes and include those patches in the same one-time preview. Do not regenerate files or create a second adaptation convention.

### Acceptance

- Only affected installed skills and companions change.
- Every repository-specific instruction represents a durable exception or explicit user decision.
- Skills remain concise and capable of discovering ordinary repository facts at runtime.
- Installed TDD guidance records the repository's coverage command or its user-approved alternative.
- Existing local changes outside the focused rewrite remain intact.
- The user approves one preview before edits apply.
- Re-running `setup` cleanly patches stale guidance.
- The skill offers to delete itself after successful setup.

## OKF knowledge layer

rstack will use [Open Knowledge Format v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md) as its repository knowledge format. OKF concepts are UTF-8 Markdown files with YAML frontmatter; `type` is the only universally required field. Bundles may add hierarchical directories, `index.md` files for progressive disclosure, `log.md` files, standard Markdown links, provenance, trust, freshness, lifecycle, and attested-computation metadata.

The repository's `docs/` tree is one OKF bundle. Its root `index.md` provides progressive disclosure and stores the concise, repository-specific coverage and maintenance policy. The root and each selected subdirectory have `index.md` and `log.md`.

The bundle favors useful knowledge over exhaustive code narration. During setup, the agent inspects the repository, presents repository-specific granularity options, recommends one, and lets the user decide which knowledge and categories belong under `docs/`.

### `okf-setup`

Purpose: establish or revise the repository's OKF v0.2 bundle.

Workflow:

1. Run only when the user explicitly invokes it.
2. Read the [OKF v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md), inspect the repository and existing `docs/`, and treat the entire `docs/` tree as one bundle.
3. Run `grill-me` before writing. Let the model derive and recommend repository-specific choices, then ask the user to settle consumers, granularity, concept types, filename convention, categories, sources, freshness, and maintenance.
4. On reruns, grill only decisions that are missing or made stale.
5. Ask which categories the user wants. Create directories such as `adr/`, `research/`, and `design/` only when selected.
6. After approval, invoke `map-codebase` to map the selected repository sections with parallel subagents.
7. Keep subagent findings separate until all finish, then have `okf-setup` synthesize them into one coherent concept map and the final OKF documents.
8. Classify and migrate existing Markdown: preserve useful content, add conformant frontmatter, place concepts in approved categories, and update links.
9. Create or update `docs/index.md` with the bundle version, progressive-disclosure links, and concise coverage policy.
10. Create and maintain `index.md` and `log.md` in `docs/` and every selected documentation directory.
11. Require every concept to carry `type`, `title`, `description`, `tags`, `generated.by`, `generated.at`, `status`, and at least one `sources` entry.
12. Start concepts as stable, omit ownership metadata, and point sources to exact supporting files.
13. Review freshness when a source file changes and use `stale_after` when operational or external knowledge has a meaningful review date.
14. Record concept-level creation, updates, and deprecation in directory logs.
15. Keep body references maintainable: point readers to the other concept instead of copying its explanation, for example, `This section is explained in [authentication flow](../architecture/authentication.md).`
16. Fail validation when required metadata is missing or an internal source or concept link does not resolve.
17. After successful setup, ask whether the user wants to delete the one-time `okf-setup` skill.

The skill does not change the host repository README.

Acceptance:

- `docs/` is one conformant OKF v0.2 bundle.
- Every concept has the required repository metadata profile and at least one source.
- Root and selected-directory indexes support progressive disclosure.
- The root and every selected directory maintain `log.md`.
- Existing documentation is classified and migrated without losing useful content.
- Bundle coverage and granularity match the completed `grill-me` decisions.
- Re-running the skill asks only about changed decisions and updates the existing bundle cleanly.
- The setup skill itself synthesizes parallel mapping reports; subagents do not write final OKF documents.
- Internal sources and concept links resolve.

Reference material:

- [Open Knowledge Format v0.2 specification](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- [OKF v0.2 trust signals](https://cloud.google.com/blog/products/data-analytics/okf-v0-2-adds-trust-signals)
- [Open Knowledge Format overview](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)

### `better-grep`

Purpose: give agents an internal, token-efficient search protocol for locating repository evidence without broad queries or unnecessary file reads.

Use it for every repository search, including code, configuration, documentation, symbols, behavior, and call sites. Skip it only when the exact path to read is already known.

Workflow:

1. Internally classify the question as path/layout, exact text or configuration, syntax shape, resolved symbol, or behavior/concept; derive the smallest useful set of identifiers, aliases, data shapes, entry points, and likely owners.
2. Read the OKF root index and only relevant concepts when present. Treat them as a map, verify against source, continue without OKF when absent, and internally flag stale or missing concepts for `docs-sync` without editing documentation.
3. Match the tool to the evidence: filename discovery for layout, language-server definition/references/implementation for symbols, structural search for syntax, and literal or regex search for text, configuration, and behavior.
4. Honor repository ignore rules and exclude generated, vendored, cache, and build output by default. Include a population only when the question or a suspiciously narrow result implicates it.
5. Start narrow. When results are empty or suspicious, validate the search root, tool capability/index/parser, filters, ignore rules, and query spelling, then widen one dimension at a time to aliases, re-exports, tests, configuration, generated inputs, or runtime registration keys.
6. Follow the evidence through the applicable definition, references/callers, imports/exports, configuration/build ownership, tests/fixtures, and runtime boundaries.
7. Stop when source evidence answers the parent task's question and expected boundaries are traced or explicitly ruled out. Never turn “not searched,” unsupported, or unresolved into “does not exist.”

The skill produces no standalone user-facing report, search narration, or artifact. It keeps routine queries and widening internal and supplies only the exact paths, symbols, decisive evidence, and uncertainty needed by the calling task.

Research basis: `docs/research/repository-search-practices.md`.

### `docs-sync`

Purpose: keep the repository's OKF bundle aligned with code changes.

Workflow:

1. Have the main orchestrator run it after implementation passes focused tests and independent review, then run one final audit after all tasks.
2. Inspect every added, modified, renamed, and deleted repository code change from the delivery baseline through the current working tree, including changes outside the current task.
3. Include tracked generated, vendored, and build files. Exclude only disposable untracked or ignored output; use tests as behavioral evidence rather than documentation targets.
4. Identify affected concepts through exact sources, links, terminology, contracts, behavior, invariants, and the bundle's coverage policy.
5. Update only concepts whose current meaning or source references changed. Create concepts only for durable knowledge selected by the coverage policy.
6. Keep concept bodies as present-tense descriptions of current code. Remove obsolete concepts and repair links and indexes instead of retaining deprecation or migration commentary.
7. Update affected directory logs with concept creation, updates, moves, and removal.
8. Set `generated.by` and `generated.at` on meaningful edits. Do not add or retain `verified` on touched concepts.
9. Make evidence-supported decisions without human approval or review.
10. Validate required metadata, reserved files, internal sources, concept links, and support for affected current-state claims.

A code change completes only after `docs-sync` has updated the affected OKF concepts or established from the configured coverage policy that no documentation update is needed.

## Agent roles

Keep generic, thin role definitions under `agents/`:

| Agent | Contract |
|---|---|
| `developer` | Implement one task, follow host conventions, run focused verification, and report evidence |
| `code-reviewer` | Apply the thermo-nuclear maintainability gate without editing implementation and return actionable approval or rejection |
| `build-validator` | Run the host repository's integration build and smoke path and report exact outcomes |
| `bug-reviewer` | Diagnose failed verification from evidence and produce a focused failure report |
| `architecture-agent` | Create architecture and integration specifications from repository evidence |

Agent definitions refer to skills by name. Model selection remains a host-runtime concern.

## Specification templates

Populate the existing templates with short prompts and instructions to remove unused sections.

### `PRD.md`

- problem;
- goal;
- scope;
- requirements;
- acceptance criteria;
- unresolved decisions.

### `ARCHITECTURE.md`

- current structure;
- proposed changes;
- affected components and files;
- data and control flow;
- constraints;
- verification approach.

### `DESIGN.md`

- user flow;
- interaction states;
- failure and empty states;
- copy;
- accessibility;
- design references;
- screen sketches or ASCII layouts when useful.

### `INTEGRATION.md`

- participating systems or components;
- contract ownership;
- request, event, or data shapes;
- compatibility behavior;
- failure behavior;
- rollout or migration constraints;
- connections with other services or components.

## Attribution and licensing

The README will credit adapted skills with links to the actual upstream skill and its repository.

Confirmed or likely sources to verify during implementation:

- `unslop`: [cursor/plugins — `pstack/skills/unslop/SKILL.md`](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md)
- `grill-me`: [mattpocock/skills — `batch-grill-me/SKILL.md`](https://github.com/mattpocock/skills/blob/main/skills/in-progress/batch-grill-me/SKILL.md)
- `research`: compare the local file with [mattpocock/skills research workflow](https://github.com/mattpocock/skills/blob/main/docs/engineering/research.md) and record the exact upstream revision
- `ponytail`: [DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail), MIT; rstack keeps its own permanent intensity and local coding rules
- `tdd`: [cursor/plugins — `pstack/skills/tdd/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/pstack/skills/tdd/SKILL.md)
- `code-review`: [cursor/plugins — `cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md`](https://github.com/cursor/plugins/blob/23a56e2dac2efd54788056db8eced26e371d7b5e/cursor-team-kit/skills/thermo-nuclear-code-quality-review/SKILL.md)

## Repository validation

Add one small validation command that checks:

- skill directories contain `SKILL.md`;
- frontmatter parses successfully;
- frontmatter names match directory names;
- referenced rstack skills exist;
- referenced companion files exist;
- the README catalog matches maintained skill directories;
- specification templates contain content;
- attribution entries point to canonical source URLs;
- examples use neutral placeholders;
- repository-local configuration follows the schema expected by `setup`;
- OKF concepts and reserved files conform to OKF v0.2.

Use an existing repository language or the standard library of a commonly available runtime. Keep the validator dependency-free.

## Collaborative task sequence

We will complete the work below together in order. Every task begins with an `ask-me` session: one question at a time, repository evidence answered without asking, and a recommended answer with each user decision. The settled answers become that task's acceptance criteria before implementation starts.

1. **Define rstack installation and repository contract — interview complete**
   - Default to guided, goals-first selection.
   - Recommend the smallest matching skill set, automatically include required dependencies and companions, explain them, and obtain approval for the final set.
   - Install project-locally from the GitHub default branch.
   - Before copying, the agent researches its own current guidance for installing skills, rules, agents, templates, scripts, and related artifacts.
   - Install selected skills plus only their required compatible companions.
   - When a selected skill already exists, compare it with the source, identify local changes, and ask whether to replace, keep, or merge it.
   - Run `setup` automatically after copying.
   - Write no installation manifest and add no per-installation metadata.
   - On success, return exactly: `Skills installed. Happy coding! — rontho14`
   - On failure, report the failed step and error instead of printing the success message.
2. **Design the `setup` skill — interview complete**
   - Rewrite installed skills and companions directly; installed copies belong to their user.
   - Inspect all installed artifacts and change only affected ones.
   - Keep rewrites focused: preserve purpose, triggers, safety, attribution, agnostic behavior, and unrelated local edits.
   - Embed only durable exceptions or explicit workflow decisions that agents cannot infer reliably.
   - Use repository guidance as a source and retain only indispensable references and essential constraints.
   - Resolve unanswered material decisions through `grill-me`.
   - Show one concise preview and obtain one approval before applying all edits.
   - On reruns, preserve current files and patch only stale instructions.
   - Adapt required skills, agents, templates, scripts, and rules under the same policy.
   - Discover new-and-changed-code coverage tooling for `tdd`; when the repository cannot enforce 80%, settle and record an alternative through `grill-me`.
   - Perform Markdown and reference checks; do not run project builds or tests.
   - Ask after successful setup whether the user wants to delete the one-time skill.
3. **Normalize skill routing descriptions — complete**
   - Use direct routing instructions of one to three sentences.
   - Use `MUST use` for mandatory matching activities, `Use when` for semantic triggers, and `Use only when` plus `disable-model-invocation: true` for human-only skills.
   - Keep routing positive; put procedures and feature summaries in the skill body.
   - Require `unslop` for all user-facing prose, `ponytail` and `tdd` together for coding, `lazy-plan` for planning, `better-grep` for codebase search, and `docs-sync` after code changes when OKF is installed.
   - Keep `refine-specs` and `create-pr` human-only.
   - Apply the convention to every current skill and document it in the README.
   - Apply the same convention when creating future skills and validate it during repository checks.
4. **Design the `okf-setup` skill — complete**
   - Use only by explicit human invocation.
   - Treat `docs/` as one OKF v0.2 bundle with its policy in `docs/index.md`.
   - Run `grill-me` before writing and revisit only missing or stale decisions on reruns.
   - Let the model inspect the repository, propose granularity and category options, recommend one, and let the user decide.
   - Classify and migrate existing documentation while preserving useful content.
   - Create only user-selected categories; the root and each selected directory have `index.md` and `log.md`.
   - Require practical concept metadata, including generation time, status, and at least one source.
   - Link to concepts that own explanations instead of duplicating their content.
   - Keep the host README unchanged.
   - Map approved codebase sections in parallel through `map-codebase`, synthesize the reports itself, and ask after success whether to delete `okf-setup`.
5. **Design the OKF bundle policy — complete**
   - Ask the user to choose concept types and filename conventions during setup.
   - Point every repository source to exact supporting files.
   - Review concepts when source files change and use `stale_after` for operational or external knowledge with a meaningful review date.
   - Record no ownership metadata.
   - Start concepts as stable.
   - Record concept-level changes in every directory log.
   - Fail validation for missing required metadata, internal sources, or concept links.
6. **Design the `map-codebase` skill — complete**
   - Decompose approved scope by real architectural boundaries.
   - Assign one read-only subagent per boundary, merge tiny boundaries, and cap each wave at eight agents.
   - Read every repository-owned production, test, configuration, schema, and script file that defines behavior; exclude generated, vendored, cache, and build output.
   - Use tests as evidence without documenting tests themselves.
   - Recursively split oversized boundaries and retry failed assignments with narrower scope.
   - Require reports covering purpose, entry points, responsibilities, dependencies, flows, contracts, invariants, exact files and symbols, OKF drift, and unresolved gaps.
   - Run a second-wave integration agent for cross-boundary flows and conflicts.
   - Return separate reports without writing intermediate or final documentation.
   - Let `okf-setup` synthesize all reports into the coherent bundle.
7. **Research ADR practice and design `create-adr` — complete**
   - Base the workflow on primary guidance from Nygard, adr-tools, and MADR, recorded in `docs/research/adr-practices.md`.
   - Record only consequential, durable decisions; inspect evidence first and ask one missing question at a time.
   - Require `okf-setup` first so the user selects the ADR directory, decision concept type, and filename policy.
   - Recommend monotonically increasing `NNNN-short-kebab-title.md` names without number reuse or renumbering.
   - Use context and problem, considered options, decision, and consequences.
   - Keep OKF `status: stable` separate from `decision_status: proposed | accepted | superseded`.
   - Delete rejected proposals only after the user rejects them and never reuse their numbers.
   - For supersession, preserve the old rationale, mark the old ADR superseded, and link it forward to the replacement.
   - Permit metadata, relationship, typo, and factual corrections in place; require a new ADR for a materially different decision or rationale.
   - Require exact decision-input sources, link to concepts instead of duplicating them, and update the ADR directory index and concept log.
   - Show one complete preview and obtain approval before writing.
8. **Design documentation references — complete**
   - Create explicit-only `add-design-reference`; require initialized OKF design policy and a runtime-rule convention established by `setup`.
   - Capture user-approved principles and external references as focused OKF concepts with exact sources.
   - Extract actionable rules, scopes, examples, exceptions, and resolved precedence; a citation alone never implies adoption.
   - Apply every adopted concept to planning, architecture, UI/UX, implementation, and review work inside its declared scope.
   - Resolve conflicts with existing concepts before adoption and obtain one approval for the complete change.
   - Generate or update thin runtime-specific rule routers in the same operation. Routers match repository files or artifacts and require reading linked concepts without duplicating their guidance.
   - Update design indexes and logs, and remove or revise routers when concepts change or retire.
9. **Design the `better-grep` skill — complete**
   - Use `docs/research/repository-search-practices.md` as the primary-source basis for search modes, ignore behavior, blind spots, controlled widening, and stopping criteria.
   - Load for every repository search except a direct read of an already-known path.
   - Keep the search contract, queries, and routine widening internal; create no report or artifact and emit no standalone user-facing text.
   - Use OKF opportunistically as a narrowing map, verify it against source, continue when it is absent, and internally flag stale or missing concepts for `docs-sync`.
   - Match tools to query semantics: filename discovery for paths, language-server navigation for resolved symbols, structural search for syntax, and literal/regex search for text, configuration, and behavior.
   - Honor repository ignore rules and exclude generated, vendored, cache, and build output by default; widen into them only when evidence implicates them.
   - Stop when evidence closes the parent task's question across applicable callers, configuration, tests, and runtime boundaries; retain only the paths, symbols, decisive evidence, and unresolved uncertainty the calling task needs.
10. **Design the `docs-sync` skill — complete**
    - Inspect every repository code change from a supplied delivery baseline, or discover the target branch merge base when no baseline is supplied.
    - Include added, modified, renamed, and deleted repository-owned code, configuration, schemas, and scripts, including tracked generated, vendored, and build files.
    - Exclude only disposable untracked or ignored output and use tests as behavioral evidence rather than documentation targets.
    - Map changes through exact sources, links, terminology, contracts, behavior, invariants, and the bundle coverage policy.
    - Update concepts only when their current meaning or source references require it; create concepts only for durable knowledge selected by policy.
    - Keep concept bodies focused on current code, remove obsolete concepts, repair links and indexes, and retain history only in Git and `log.md`.
    - Have the main orchestrator run synchronization after review approval and once more after all tasks.
    - Maintain `generated.by` and `generated.at`, omit `verified`, and require no human review or approval.
    - Complete only after the affected concepts are synchronized or ruled out by policy and OKF validation passes.
11. **Rebuild the `code-review` skill — complete**
    - Adapt Cursor's thermo-nuclear code-quality rubric as the single maintainability review gate.
    - Derive the review from Git in the current directory, including branch, staged, unstaged, and untracked changes; never treat uncommitted work as a problem.
    - Review the implementation agent's full task delta without attributing unrelated pre-existing changes to it.
    - Keep tests, builds, functional acceptance, and implementation edits outside the reviewer's role.
    - Make every high-confidence finding a blocker, mark bounded behavior-preserving corrections `FIX NOW`, omit optional findings, and cap each pass at ten blockers.
    - Return `[APPROVE]` or `[REJECT]`, required fixes, and separately identified pre-existing debt.
    - Have the main orchestrator route every blocker to a coding agent, rerun the full review, and deduplicate pre-existing debt into the active specification's `DEBT.md`.
    - Preserve Cursor's MIT attribution at the vendored upstream revision.
12. **Refine standalone skills — in progress**
    - `ponytail` refined as a permanent YAGNI-extremist coding skill for building, fixing, and refactoring code. It preserves the local hardware and logging rules, forbids unnecessary comments, requires honest filenames, and always pairs with `tdd`.
    - `tdd` owns testing. It establishes a useful test or executable check before production changes, avoids over-testing, requires 80% line coverage of new and changed code when configured, and defers missing coverage-tool policy to `setup`.
    - Remaining: review `lazy-plan`, `unslop`, `research`, `grill-me`, `ask-me`, `second-opinion`, and `debug` for purpose, portability, dependencies, and attribution.
13. **Refine delivery skills**
    - Generalize `create-pr` and `get-work-item` around repository discovery and `setup` configuration.
14. **Refine the issue-to-delivery pipeline**
    - Align `planner`, `refine-specs`, `create-tasks`, and `orchestrator` around one existing task or issue per specification directory.
15. **Refine generic agent roles**
    - Settle the contracts for developer, reviewer, validator, bug investigator, and architecture roles.
16. **Design specification templates**
    - Finalize the minimal content and creation rules for `PRD.md`, `ARCHITECTURE.md`, `DESIGN.md`, and `INTEGRATION.md`.
17. **Verify attribution and licenses**
    - Identify canonical sources, compare local adaptations, preserve required notices, and write README credits.
18. **Build repository validation**
    - Validate skills, routing descriptions, references, templates, setup configuration, README catalog, attribution links, and OKF conformance.
19. **Run installation and workflow acceptance**
    - Test clean GitHub installation, `setup`, `okf-setup`, parallel codebase mapping, OKF-assisted search, docs synchronization, ADR creation, design references, and the complete issue-to-delivery pipeline.
20. **Research Maven vulnerability remediation and design `fix-maven-vulnerabilities` — initial skill created; acceptance exercise remains**
    - Use `docs/research/maven-vulnerability-remediation.md` as the primary-source basis for Maven ownership, effective-model, dependency-graph, BOM, plugin, mediation, and verification behavior.
    - Accept one or more pasted, scanner-neutral findings containing an exact vulnerable Maven coordinate/current version and remediation guidance with one or more fixed versions; do not require GitLab or advisory lookup, and treat the supplied guidance as the fix authority.
    - Map each resolved version to its real owner: direct declaration, property, parent, dependency management, imported BOM, plugin, or plugin management. Edit the owner rather than adding duplicate overrides, exclusions, or suppressions.
    - Evaluate listed versions as compatibility candidates rather than choosing the lowest, current-line, or newest version automatically. Apply dependency-only fixes that preserve the current release line or established BOM/framework contract; ask before parent, BOM, framework, or major-line upgrades.
    - Allow a local override of an externally owned parent or BOM only when upstream alignment guidance supports it and the resolved graph plus full build verify it; otherwise stop with ownership evidence.
    - Process all findings in a remediation loop. An iteration may contain multiple compatible fixes, but it must regenerate the complete relevant dependency graph and run the repository's full Maven build before continuing.
    - If a multi-fix iteration fails, restore the last passing dependency state and bisect the dependency changes with full builds. Keep independently passing fixes and continue until every finding is fixed or isolated as blocked.
    - Try other safe, guidance-listed candidates when a fix fails. If every safe candidate requires application-code changes, revert that dependency change, leave other verified fixes in place, stop without editing application code, and report the remaining vulnerable coordinate and failure evidence.
    - Complete only when every unblocked finding resolves to a guidance-listed safe version in the Maven graph and the full build passes. A `pom.xml` edit alone and vulnerability-scanner execution are not completion evidence.
    - The skill owns concise companion guidance derived from the research note, including input parsing, candidate evaluation, safety boundaries, retained evidence, loop invariants, stopping conditions, and an acceptance exercise.

The future project-inception skill is tracked as a product boundary, not implemented in this plan. It will turn a new project idea into initial tasks or issues that can enter this pipeline.

## Completion criteria

- The README enables agent-assisted GitHub installation and manual copying.
- Every maintained skill has a documented purpose and valid Agent Skills structure.
- Every skill description tells the model when to load the skill and contains no procedure better kept in the skill body.
- `setup` configures installed skills from evidence in the host repository.
- The planning pipeline takes one existing task or issue through specifications, implementation tasks, review, documentation sync, and final verification.
- `ask-me`, `grill-me`, and `second-opinion` remain independently invocable.
- All cross-skill and companion-file references resolve.
- The four specification templates are usable.
- Third-party skills have verified source links and license treatment.
- Repository validation passes.
- `okf-setup` produces a focused, conformant OKF v0.2 bundle after a `grill-me` session.
- `better-grep` uses OKF to narrow searches and verifies findings against the repository.
- `docs-sync` keeps affected OKF concepts aligned with code changes.
- `fix-maven-vulnerabilities` uses researched remediation practice to remove reported vulnerable Maven resolutions and proves the resulting dependency graph and relevant build behavior.
- Every collaborative implementation task begins with a completed `ask-me` session.
- A clean installation, adaptation run, and end-to-end pipeline exercise succeed.

## Decisions to refine

- Final GitHub repository URL and the exact installation prompt shown in the README.
- Name and location of the repository-local adaptation configuration file.
- Whether `setup` may edit installed skills or only generate shared configuration and recommendations.
- Whether `get-work-item` replaces `get-card` immediately or remains a separate generic skill.
- Which git providers `create-pr` supports in its first portable revision.
- The minimum runtime capabilities rstack promises beyond the Agent Skills file format.
- Whether an adapted skill records its local changes inside the host repository or only in the adaptation report.
