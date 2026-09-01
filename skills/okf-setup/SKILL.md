---
name: okf-setup
description: Use only when the user explicitly invokes okf-setup to establish, migrate, or reorganize the repository's Open Knowledge Format documentation bundle.
disable-model-invocation: true
---

# OKF Setup

Use [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Treat `docs/` as one bundle.

## Process

1. Inspect the repository and existing `docs/` content.
2. Run `grill-me` before writing. Derive repository-specific options, recommend one, and ask the user to settle consumers, granularity, categories, concept types, sources, freshness, and maintenance. When ADRs are selected, also settle their directory and filename convention.
3. On reruns, grill only decisions that are missing or stale.
4. Show the proposed concept map and migration, then obtain approval.
5. Invoke `map-codebase` to map the approved repository sections with parallel subagents. Keep their reports separate until all finish.
6. Synthesize the reports yourself into one coherent concept map; subagents do not write final OKF documents.
7. Classify and migrate existing Markdown without losing useful content.
8. Create only the documentation categories the user selected.
9. Create or update the bundle files and validate them against OKF v0.2.
10. After successful setup, ask whether the user wants to delete this one-time setup skill.

## Bundle rules

- `docs/index.md` declares `okf_version: "0.2"`, links the bundle through progressive disclosure, and records the concise coverage and maintenance policy.
- `docs/` and every selected subdirectory have `index.md` and `log.md`.
- Every concept has `type`, `title`, `description`, `tags`, `generated.by`, `generated.at`, `status`, and at least one `sources` entry.
- Ask the user to choose the repository's concept types and filename convention during setup.
- Concepts start with `status: stable`.
- Every source points to the exact repository files, issues, external material, or other concepts that support it.
- Use source-file changes to trigger freshness review. Use `stale_after` as well when operational or external knowledge has a meaningful review date.
- Logs record concept-level creation, updates, and deprecation with the date, concept link, and one short reason.
- When another concept owns an explanation, link to it instead of copying it: `This section is explained in [authentication flow](../architecture/authentication.md).`
- Keep concepts as granular as the grill session decides. Do not document code exhaustively by default.
- Do not add ownership metadata.
- Do not change the repository README.

## Validation

Fail validation if frontmatter is malformed, required metadata is missing, a reserved file has the wrong structure, or an internal source or concept link does not resolve. Report the resulting coverage and deliberate gaps.
