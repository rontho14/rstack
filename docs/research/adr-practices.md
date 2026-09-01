# Canonical ADR practices

This note separates **source-backed observations** from a deliberately small **rstack recommendation**. “Canonical” does not mean standardized: the primary sources describe overlapping conventions, not one normative ADR specification.

## Source-backed practices

### What deserves an ADR

Michael Nygard’s original article scopes ADRs to “architecturally significant” decisions: decisions affecting **structure, non-functional characteristics, dependencies, interfaces, or construction techniques**. It also says one ADR records one significant decision for one project, with an effect on how the rest of the project runs. This is narrower than “every technical choice.” ([Nygard, *Documenting Architecture Decisions*](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions))

MADR’s template asks authors to make the decision’s scope explicit, optionally by identifying affected structural elements, and to state the problem, options, and outcome. ([MADR minimal template](https://github.com/adr/madr/blob/main/template/adr-template-minimal.md))

### Minimal content

Nygard’s compact format has five parts: **Title, Context, Decision, Status, and Consequences**. Context records the forces neutrally; Decision states the response in active voice; Consequences includes positive, negative, and neutral effects. He recommends a short, one- or two-page record written for a future developer. ([Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions))

MADR makes a different minimum explicit: **title, Context and Problem Statement, Considered Options, and Decision Outcome**; its minimal template labels Consequences optional. ([MADR minimal template](https://github.com/adr/madr/blob/main/template/adr-template-minimal.md); [MADR README](https://github.com/adr/madr/blob/main/README.md#quick-start)) Its full template additionally offers optional status/date/stakeholder metadata, decision drivers, consequences, confirmation, option analysis, and more information. ([MADR full template](https://github.com/adr/madr/blob/main/template/adr-template.md))

**Disagreement/choice:** Nygard treats Status and Consequences as core fields, while MADR’s declared mandatory sections instead require considered options and omit status; MADR treats consequences as optional. Neither layout is universally required.

### Status and decision history

Nygard names **proposed** and **accepted** states. When a later ADR changes or reverses a decision, the earlier record may become **deprecated** or **superseded**, with a reference to its replacement. He explicitly keeps reversed records rather than deleting them because the historical decision remains relevant. ([Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions))

MADR treats status as optional metadata and suggests an open-ended set including `proposed`, `rejected`, `accepted`, `deprecated`, and `superseded by ADR-0123`; it also records the date “when the decision was last updated.” ([MADR full template](https://github.com/adr/madr/blob/main/template/adr-template.md)) Thus, rejection and update dates are MADR conventions, not requirements inherited from Nygard.

A conservative lifecycle consistent with both sources is `proposed → accepted` or `proposed → rejected`, and `accepted → deprecated` or `accepted → superseded`. “Deprecated” need not identify a replacement; “superseded” should.

### Supersession, links, and amendments

Nygard requires a superseded record to reference its replacement. ([Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)) `adr-tools` automates a **bidirectional** relationship: `adr new -s 9 ...` marks ADR 9 as superseded and links the new ADR to it; its source also supports arbitrary reciprocal links and gives “Amends” / “Amended by” as an example. ([adr-tools README](https://github.com/npryce/adr-tools/blob/master/README.md#quick-start); [`adr-new` source and usage](https://github.com/npryce/adr-tools/blob/master/src/adr-new)) MADR’s optional “More Information” permits links to other decisions and can state when a decision should be revisited. ([MADR full template](https://github.com/adr/madr/blob/main/template/adr-template.md))

**Immutability versus amendments:** the sources do not impose strict byte-level immutability. Nygard’s historical rule is to retain a reversed record and mark it superseded rather than erase it; MADR explicitly allows a last-updated date; `adr-tools` mutates an older ADR’s status/links during supersession and supports amendment links. Therefore “accepted ADRs are never edited” is an optional team policy, not a canonical rule. The history-preserving invariant is stronger and better supported: do not rewrite a past decision to pretend a different decision was made; use a new ADR for a materially different outcome, then cross-link it. Small factual/link/status corrections may amend the existing record and remain visible in version control.

### Numbering and naming

Nygard proposes `adr-NNN.md`, sequential monotonic numbers, and no number reuse. ([Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)) `adr-tools` creates a numbered file, and its implementation derives the next integer from existing numeric prefixes, pads it to four digits, and appends a title slug (`0001-title.md`). ([adr-tools README](https://github.com/npryce/adr-tools/blob/master/README.md#quick-start); [`adr-new` source](https://github.com/npryce/adr-tools/blob/master/src/adr-new)) MADR likewise recommends copying the template to `nnnn-title.md`. ([MADR README](https://github.com/adr/madr/blob/main/README.md#quick-start))

Sequential numbers give stable, compact identifiers and an easy chronological scan; adding a slug makes filenames recognizable. The tradeoff is coordination during concurrent creation and renumbering temptation after abandoned drafts. Since Nygard says numbers are never reused, gaps are harmless historical evidence. Date-based or unnumbered names can reduce allocation conflicts, but they depart from all three cited defaults and make compact cross-references less convenient.

### Repository placement and indexing

Nygard places Markdown ADRs with the project at `doc/arch/adr-NNN.md`, emphasizing visibility through repository links and rendered Markdown. ([Nygard](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions)) `adr-tools` stores Markdown ADRs in a project subdirectory, defaults to `doc/adr`, and permits another directory at initialization. ([adr-tools README](https://github.com/npryce/adr-tools/blob/master/README.md#quick-start)) MADR recommends `docs/decisions`. ([MADR README](https://github.com/adr/madr/blob/main/README.md#quick-start))

**Optional convention:** none of these primary passages mandates a hand-maintained index. The directory itself is the decision log for `adr-tools`, and sortable numeric filenames provide a basic index. A separate `README.md` index can improve discovery and summarize current status, but it introduces duplicate state that must be maintained.

## Settled portable policy for rstack

The repository interview selected this policy after reviewing the tradeoffs above:

1. Create an ADR only for a consequential, durable choice affecting architecture, interfaces, data, security, operations, quality attributes, dependencies, or long-term constraints—not routine implementation detail.
2. Require `okf-setup` to establish the ADR directory and decision concept type instead of imposing a path.
3. Recommend `NNNN-short-kebab-title.md`, allocate the next monotonically increasing number, and never reuse or renumber numbers.
4. Use **Context and Problem**, **Considered Options**, **Decision**, and **Consequences**, plus OKF metadata.
5. Keep OKF `status: stable` separate from `decision_status: proposed | accepted | superseded`. Match the initial decision status; delete a rejected proposal without reusing its number.
6. For a materially changed decision, create a new ADR, mark the old one superseded, and link the old record forward to its replacement. Do not require a reciprocal link.
7. Allow metadata, relationship, typo, and factual corrections in place. Preserve accepted rationale.
8. Update the ADR directory's OKF index and concept log.
