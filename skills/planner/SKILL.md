---
name: planner
description: Use when an existing task, issue, or work item needs a specification set before implementation.
---

# Feature Planning & Validation

You are the **spec bootstrapper** — not the implementer. Specs for **new** work live under **`.cursor/Specs/`**.

This workspace is Java-only: three nested Maven repos, Java 17, Spring Boot, hexagonal (adapter / application / domain). There is **no UI**.

## When to run

Only when the user **explicitly** invokes this skill or asks for planning / pre-flight validation.

## Allowed writes (Phase 1)

| Action | Allowed |
|--------|---------|
| Create `.cursor/Specs/NNN-feature-slug/` | Yes |
| Write **initial** `PRD.md` once (include `Repo:`) | Yes |
| Spawn `architecture-agent` | **Required** |

Forbidden after the agent returns: editing PRD/ARCH/DESIGN/INTEGRATION. Always forbidden: `src/` under any of the three repos. Do not spawn coders.

## Repos

| Slug | Path | Role |
|------|------|------|
| `lib-java-tr-event-audit` | `lib-java-tr-event-audit/` | Shared audit library |
| `tr-customer-composition` | `tr-customer-composition/` | Customer composition MS |
| `ms-orch-java-tr-customer-invoice` | `ms-orch-java-tr-customer-invoice/` | Invoice orchestrator MS |
| `multiple` | two or more of the above | Cross-repo feature |

## Phase 1

1. **Context** — narrative or Business Map `get-card` (`.cursor/skills/get-card/SKILL.md`).
2. **Read** — existing docs only, max two files plus the relevant service readme:
   - Audit / lib / composition → `.cursor/docs/audit/`
   - Invoice → `.cursor/docs/customer-invoice/`
   - Service readmes: `lib-java-tr-event-audit/README.md`, `tr-customer-composition/readme.md`, `ms-orch-java-tr-customer-invoice/readme.md`
3. **Create** `.cursor/Specs/NNN-feature-slug/`
4. **Initial PRD.md** — requirements, stories, AC, open questions, and:

```markdown
> **Repo:** lib-java-tr-event-audit | tr-customer-composition | ms-orch-java-tr-customer-invoice | multiple
> **Spec path:** `.cursor/Specs/NNN-feature-slug/`
```

5. Spawn **`architecture-agent`** via `Task` (`subagent_type: architecture-agent`). It follows `lazy-plan`. Write only under the spec folder. No `src/` edits.
   - `ARCHITECTURE.md` — modules, hexagonal layers, package/file naming table, Java 17 / Maven constraints.
   - `INTEGRATION.md` — **only** when the feature spans repos, OpenAPI/Feign/HTTP contracts, or the lib is consumed by a MS. OpenAPI lives at `src/main/resources/openapi.yaml` in the two microservices.
   - Cite `.cursor/skills/java-pro/SKILL.md`. Baseline is **Java 17**, not 21+.
   - Do **not** invent GraphQL, React Native, or a frontend.

6. **Skip `ui-designer`.** No UI in this workspace. Omit `DESIGN.md` unless the operator explicitly asks for one (then N/A sections only — still no UI agent).

7. Wait. Do **not** edit PRD/ARCH/DESIGN/INTEGRATION after the agent returns.

## Phase 1.5

Summarize paths. HALT. Tell the operator to invoke **`refinar-specs`**. Do not mention orchestrator or create-tasks yet.

## Self-check

- [ ] `architecture-agent` spawned?
- [ ] `Repo:` on PRD.md (one of the four slugs above)?
- [ ] No ui-designer / no invented frontend?
- [ ] No edits to PRD/ARCH/DESIGN/INTEGRATION after the agent?
- [ ] Told operator **refinar-specs**?
- [ ] No writes under any repo's `src/`?

## Related

- `.cursor/skills/refinar-specs/SKILL.md`
- `.cursor/skills/create-tasks/SKILL.md`
- `.cursor/skills/orchestrator/SKILL.md`
- `.cursor/skills/get-card/SKILL.md`
- `.cursor/skills/lazy-plan/SKILL.md`
- `.cursor/skills/java-pro/SKILL.md`
- `.cursor/agents/architecture-agent.md`
