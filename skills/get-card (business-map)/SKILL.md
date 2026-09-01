---
name: get-card
description: Use when the user provides a Business Map card ID or link, invokes get-card, or asks to begin work from a Business Map card.
---

# Get Card

Load a Business Map card into context and reconcile it with what the user actually wants to build. Cards are often AI-generated or stale — treat the card as a **starting hypothesis**, not the source of truth.

## When to use

- User invokes **`/get-card`** or **`get-card`**
- User shares a Business Map card ID or link and wants to start planning or implementation
- User says the card description may be wrong, incomplete, or AI-written

Do **not** use for posting comments back to the card — use the `businessmap-comment-*` skills instead.

## Phase 1: Resolve the card

1. Extract the card ID from the user message (numeric ID or URL fragment). If missing, ask once: **"Qual é o ID do cartão Business Map?"**
2. Do not guess or invent a card ID.

## Phase 2: Load via Business Map MCP

Use the Business Map MCP tools in this order:

1. **`get-card`** — primary source. Load title, description, custom fields, labels, links, and any acceptance criteria present on the card.
2. **`get-card-comments`** — secondary context. Skim recent human comments for corrections, scope notes, branch names, env vars, or feature-flag details that the card body missed.

If `get-card` fails, report the error and stop. Do not proceed with a fabricated summary.

## Phase 3: Build the working brief

Present a concise brief in the chat (do not write spec files unless the user asks):

```markdown
## Card [ID] — [Title]

**From the card**
- Goal: …
- Acceptance / requirements: …
- Custom fields / labels: …
- Notable comments: …

**Assumptions & smells** (flag anything that looks AI-generated, vague, or contradictory)
- …

**Open gaps** (missing from the card but needed to implement)
- …
```

Rules for this section:

- Quote or paraphrase the card faithfully — separate **what the card says** from **your interpretation**.
- Call out boilerplate, generic language, duplicated AC, scope that does not match the title, or requirements that contradict comments.
- If a question can be answered by exploring the codebase, explore first and note findings in the brief instead of asking the user.

## Phase 4: Light clarification (ask-me lite)

Run a **short** reconciliation interview. This is **not** full `ask-me` or `refinar-specs` — stop once scope and intent are aligned, not when every design branch is resolved.

### Rules

- Ask **one question at a time**. Wait for the answer before the next.
- Cap at **5 questions** unless the user explicitly wants to go deeper.
- Every question must include your **recommended answer** based on the card, comments, and codebase.
- Prefer questions that correct card drift:
  - What is **in scope** vs **out of scope** for this task?
  - What did the card get **wrong** or **overstate**?
  - What **must** ship vs what is **nice-to-have**?
  - Any **constraints** (deadline, env, flag, branch, compliance) not on the card?
  - What does **done** look like — one observable outcome the card does not state clearly?
- If the user confirms the card as-is with no corrections after the brief, **skip** the interview and state: *"Card accepted as working brief."*
- If the user says "just load it" or "no questions", respect that and carry the card brief forward unchanged.

### Stop condition

End the skill when you can state a **Reconciled working brief** in 3–6 bullets:

```markdown
## Reconciled working brief

- **Goal**: …
- **In scope**: …
- **Out of scope**: …
- **Done when**: …
- **Corrections vs card**: … (or "None — card accepted")
```

Carry this brief into whatever the user does next (planning, coding, `lazy-plan`, `backoffice-feature-planning-validation`, etc.). Do not start implementation unless asked.

## Failure modes

- **Rubber-stamping the card** — summarizing without flagging smells or gaps. Always include the Assumptions & smells section.
- **Full grill** — asking about architecture, folder structure, or spec file layout. That belongs in `refinar-specs` or planning skills, not here.
- **Skipping MCP** — inventing card content from memory or the user's paraphrase. Always call `get-card` first.
- **Silent scope change** — applying user corrections without restating them in the Reconciled working brief.
