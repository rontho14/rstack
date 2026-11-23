---
name: create-spec
description: Use only when the user explicitly invokes /create-spec to synthesize a lean backend technical specification (SPEC.md) from a work note or discussion and live repository verification.
disable-model-invocation: true
argument-hint: "<spec-id> or path to work note"
---

# Create spec

Synthesize a clean, agent-ready backend specification (`SPEC.md`) in the workspace's spec directory (`specs/<id>/SPEC.md`, or `.cursor/specs/<id>/SPEC.md` when the workspace keeps specs there). Do not interview the user, do not write product code, and do not generate `TASKS.md`.

`SPEC.md` is a **knowledge-transfer artifact** for downstream agents (`/second-opinion`, `/create-tasks`, `/implement`). Store only what a fresh agent cannot re-derive by reading the repository: decisions, rejected alternatives, external wire deltas, non-repo runtime facts, cross-cutting invariants, behavioral clauses, verification oracles, and open questions.

Work through the stages in order. Satisfy each stage's check before advancing.

## 1. Resolve inputs

Locate the source material in this order and stop at the first match:

1. The path or spec id passed as the argument (when given an id, check the workspace's `own-it/work/<id>.md` if present).
2. The feature work note or plan discussed in the current conversation.

Collect the target repository, spec id (`<feature>` in a single-repo workspace or `<repo>--<feature>` in a multi-repo workspace), ticket/issue reference, and every referenced upstream spec, review report, or supporting data file.

**Check:** You hold the full source work note (or conversation plan), target repository, spec id, and all referenced upstream specs.

## 2. Verify against live code

Inspect the target repository (and any sibling upstream or consumer repository named in the source notes) on disk before drafting.

- Record `base_ref` as `<branch>@<short-sha>` from the target repository. Check sibling consumer or upstream repositories against their default integration branch when verifying downstream contracts.
- Verify every route path, controller/service/model symbol, config key, feature flag, schema definition, and pre-review build command you intend to name.
- Check whether any claim in the work note contradicts live code; note each mismatch to correct in `SPEC.md` or raise as a blocking open question.

**Check:** Every route, symbol, config key, command, and `base_ref` going into `SPEC.md` is verified against live files on disk.

## 3. Synthesize `<spec-dir>/<id>/SPEC.md`

Create `<spec-dir>/<id>/` if needed and write `SPEC.md` using the template below.

Rules:
- **Voice:** Write in crisp third-person technical prose. Keep raw user quotes and learning transcripts in the `own-it` work note.
- **Pointers, not copies:** Name files and symbols with a 1-line responsibility in the Touch map instead of pasting existing repo code or line numbers.
- **Deltas only:** Show only added or changed wire fields, nullability, empty states, and normalization rules in External contracts.
- **Strict gating:** Place confirmed choices in Section 3 and unconfirmed proposals in Section 9. Never write a pending question into Section 3 or Section 7.
- **Status rule:** Set frontmatter `status: blocked-on-questions` whenever Section 9 `Blocking` has at least one row; otherwise set `draft` (or `approved` when the user explicitly approves a spec with zero blocking questions).
- **Prune unused parts:** Delete any subsection or bullet that does not apply instead of writing `"N/A"`.
- **Optional split:** Add `INTEGRATION.md` alongside `SPEC.md` only when two or more independently owned teams must sign off on a shared cross-repo contract.
- **Updating an existing `SPEC.md`:** Promote answered questions to Section 3, delete resolved rows from Section 9 (leave no strikethrough history), refresh `base_ref`, and update `status`.

### Template

```markdown
---
spec_id: <id>
repo: <target-repo>
base_ref: <branch>@<short-sha>
status: draft | blocked-on-questions | approved
card: <ticket-or-issue-id>
upstream_specs: [<optional sibling spec ids>]
---

# <Feature title>

## 1. Problem and goal
<!-- 2-4 sentences: caller/user problem and observable backend outcome. -->

## 2. Scope and non-goals
### In scope
- <Exact endpoints, consumers, events, or jobs changed>

### Non-goals
- <Plausible goal deliberately excluded, plus deferred pre-existing bugs>

## 3. Locked decisions and rejected alternatives
<!-- Confirmed choices only. Governs downstream code-judo review triage. -->
| ID | Decision | Rejected alternative and reason | Owner / Source |
|---|---|---|---|
| D1 | <Active-voice choice> | <Rejected option + concrete trade-off> | <User / Tech lead / ADR> |

## 4. External contracts and data invariants
<!-- Changed or boundary-crossing shapes, types, nullability, empty states, and normalization rules only. -->
| Field | Source / Wire path | Type & nullability | Empty / missing rule | Notes |
|---|---|---|---|---|

### Contract sample (changed slice only)
<!-- Minimal JSON/Avro/SQL snippet showing only new/changed fields plus empty/failure case. Omit if table alone is unambiguous. -->

## 5. Non-repo facts and operational boundaries
<!-- Only facts a fresh agent cannot read from <repo> alone. Delete unused bullets. -->
- **Upstream / downstream runtime facts**: <Staging probes, sibling-repo quirks, consumer expectations>
- **Fault isolation and degradation**: <What fails independently, fallback output, retry/circuit-breaker rules>
- **Caching, state, and concurrency**: <Cache key, TTL, read vs. mutation behavior, known race semantics>
- **Security, PII, and logging**: <Auth boundary, redaction bans, allowed log fields>
- **Observability**: <Structured log keys, metrics, traces, alertable signals>

## 6. Touch map (pointers, not copies)
<!-- Paths, action, and 1-line role only. No repo code blocks or line numbers. -->
| Path | Action | Responsibility |
|---|---|---|
| `<path>` | modify / new | <1-line responsibility or invariant enforced here> |

**Untouched by design**: `<symbols, routes, or controllers explicitly left unchanged>`

## 7. Behavioral requirements and edge cases
<!-- 6-20 numbered, atomic, testable clauses (EARS When/If...Then or Given/When/Then). Cover happy, empty, partial, malformed, flag-off, and failure paths. -->
- **R1 (Happy path)**: When <trigger>, <system> shall <observable outcome>.
- **R2 (Empty / absent)**: When <missing or empty input>, <system> shall <outcome>.
- **R3 (Malformed / fault isolation)**: If <bad payload or partial failure>, then <system> shall <isolated outcome without breaking critical paths>.
- **R4 (Dependency outage)**: If <upstream fails or times out>, then <system> shall <degraded outcome>.
- **R5 (Feature toggle / cache)**: While <state>, when <trigger>, <system> shall <outcome>.
- **R6 (Logging / security)**: <System> shall never log <forbidden data>; on parse failure it shall log only <allowed fields>.

## 8. Verification oracle
- **Pre-review gate**: `<exact repo lint/test/build command>`
- **Required automated proofs**:
  - <Contract / serialization / schema proof>
  - <Fault-isolation and edge-case proofs mapped to R1..Rn>
  - <Log-redaction / security proof naming exact loggers or appenders>
- **Live / end-to-end proof**: <Exact local verification skill or command and expected observable result>

## 9. Open questions
<!-- Delete resolved rows after promoting them to Section 3. -->
### Blocking (must resolve before `/create-tasks` and `/implement`)
| ID | Question | Owner | Evidence / Conflict |
|---|---|---|---|
| Q1 | <Concrete decision needed> | <Role> | <Why repo, ticket, or stakeholders conflict> |

### Non-blocking (can resolve in parallel or post-ship)
| ID | Question | Owner | Default while open |
|---|---|---|---|
```

**Check:**
- Every unconfirmed decision sits in Section 9 and nowhere in Sections 3 or 7.
- Frontmatter `status` matches whether Section 9 `Blocking` has rows.
- Every `R1..Rn` clause maps to a concrete check in Section 8.
- Zero existing repo code blocks, line numbers, raw interview quotes, `"N/A"` placeholders, or strikethrough resolved questions appear in `SPEC.md`.

## 4. Hand off

Report:
- Path written (`<spec-dir>/<id>/SPEC.md`), `base_ref`, and `status`.
- Any factual mismatches found between the work note and live code.
- Any blocking open questions in Section 9.

Then print this exact handoff line (with paths filled in) and stop:

`Next: run /second-opinion on <spec-dir>/<id> and save the report to <own-it-dir>/review/<id>.md.`
