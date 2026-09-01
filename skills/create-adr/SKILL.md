---
name: create-adr
description: Use only when the user explicitly invokes create-adr to record or supersede a consequential, durable architecture decision in an initialized OKF documentation bundle.
disable-model-invocation: true
---

# Create ADR

Record one decision that materially affects architecture, interfaces, data, security, operations, quality attributes, dependencies, or long-term constraints and is costly to reverse. Do not create ADRs for routine implementation choices.

## Prerequisite

Require an initialized OKF bundle and documentation policy. If either is missing, run `okf-setup` first. Reuse the configured ADR directory, concept type, and filename convention; do not create a second convention.

Recommend `NNNN-short-kebab-title.md` during setup. Allocate the next monotonically increasing number. Never reuse numbers, renumber records, or close gaps.

## Process

1. Inspect the request, repository evidence, issues, existing concepts, and related ADRs.
2. Ask one question at a time only for context, considered options, outcome, or consequences that evidence cannot establish.
3. Determine whether the decision is already settled. Use `decision_status: accepted` when settled and `decision_status: proposed` otherwise.
4. Show one preview containing the ADR, status and relationship changes, directory index update, and directory log entry.
5. Obtain one approval, then apply the full preview.
6. Validate frontmatter, sources, links, numbering, index state, and log state.

## Record

Every ADR is an OKF concept. Keep the bundle lifecycle field `status: stable` separate from ADR lifecycle in `decision_status`.

Use the repository's configured metadata profile and require at least:

- `type`, using the configured decision concept type;
- `title` and `description`;
- `tags`;
- `generated.by` and `generated.at`;
- `status: stable`;
- `decision_status: proposed | accepted | superseded`;
- at least one exact `sources` entry pointing to decision inputs such as repository files, issues, external constraints, or related concepts.

Use these body sections:

1. Context and Problem
2. Considered Options
3. Decision
4. Consequences

Link to concepts that own supporting explanations instead of copying their content.

## Lifecycle

Delete an unaccepted proposed ADR only when the user rejects it. Never reuse its number.

When a new accepted ADR replaces an old one:

- preserve the old rationale;
- set the old record to `decision_status: superseded`;
- add `Superseded by` to the old record, linking to the replacement.

Do not require a reciprocal `Supersedes` link in the new record.

Allow in-place changes to metadata, relationship links, typos, and factual corrections. A materially different decision or rationale requires a new ADR.

## Navigation and history

Add or update the ADR's link and decision status in the ADR directory's `index.md`. Append one concept-level creation or status-change entry to that directory's `log.md` with the date, concept link, and one short reason.
