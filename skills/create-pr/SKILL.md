---
name: create-pr
description: Use only when the user explicitly asks to create a pull request, merge request, or PR/MR from the current repository changes.
disable-model-invocation: true
---

# Create Merge Request (BackOffice)

Open a **GitLab merge request** for the BackOffice workspace
(`main-tscript-tr-backoffice` + `ms-bff-java-tr-backoffice`). Tracking lives in
**Business Map**, not Linear. Hosting is **GitLab**, not GitHub.

Say **merge request / MR** in user-facing text. Keep the skill name `create-pr`
as the alias.

## When to use

- User asks to create a PR/MR after committing
- Feature branch is ready to review
- User wants title/description generated from commits + card

## Project map

Detect the git repo from `git remote` / cwd. `.omp/` is **not** a git repo; if
the workspace root is open, inspect **both** application repos.

| Repo | GitLab path | `project-id` | Default target |
|------|-------------|--------------|----------------|
| BFF | `raiadrogasil/rd/tr/backofficetr/ms-bff-java-tr-backoffice` | `67239320` | `develop` |
| Frontend | `raiadrogasil/rd/tr/backofficetr/main-tscript-tr-backoffice` | `67566020` | `develop` |

MCP `id` for `create_merge_request`: project id **or** URL-encoded path.
`list_merge_requests`: pass **exactly one** of `url` or `project_id`.

If the same Business Map card has branches in **both** repos, create **one MR
per repo** (do not mix diffs).

## Prerequisites

- GitLab MCP (`plugin-gitlab-GitLab`) authenticated. If `serverStatus` is
  `needsAuth`, call `mcp_auth` for that server, then retry.
- Current branch is **not** `develop` / `main` / `master`.
- Branch has commits not on the target (`develop` unless the user names another).
- Branch is pushed to `origin`. Push with `git push -u origin HEAD` if needed.
- No open MR already exists for this source branch.

## User input

Honor `$ARGUMENTS` when present:

- Title, description, target branch
- Draft / WIP
- Reviewer GitLab **user ids** (MCP needs numeric `reviewer_ids`; do not invent)
- Labels (comma-separated names that already exist on the project)

If omitted, generate title/description from git + Business Map. Default target:
`develop`.

## MCP (mandatory)

Do **not** use `gh`. Discover schemas with `GetMcpTools`, then `CallMcpTool`.

Server: `plugin-gitlab-GitLab`

| Step | Tool | Purpose |
|------|------|---------|
| 1 | `list_merge_requests` | `state: opened` + search/source branch — abort if one exists |
| 2 | `create_merge_request` | Create the MR |
| 3 | `get_merge_request` | Optional: confirm URL / iid |

`create_merge_request` required args: `id`, `title`, `source_branch`,
`target_branch`. Optional: `description`, `labels` (comma-separated string),
`assignee_ids`, `reviewer_ids`, `draft` if the schema supports it.

If the MCP tool lacks a draft flag, put `Draft:` in the title when the branch
name contains `wip` or the user asked for a draft.

## Workflow

### 1. Git state

In the detected application repo:

```bash
git rev-parse --abbrev-ref HEAD
git log develop..HEAD --oneline
git diff --stat develop..HEAD
git diff --name-only develop..HEAD
```

Stop if: not a git repo, on `develop`/`main`/`master`, or no commits vs target.

### 2. Business Map card

Extract a card id from branch name, commits, or user text:

- `TRCLIENTE-741341` / `FEATURE/TRCLIENTE-741341` / `feature/TRCLIENTE-…`
- `SQ53-597987` / `feat/SQ53-…`
- Numeric id if the user pasted a Business Map URL

Call Business Map MCP **`get-card`** (same as skill `get-card`). Fold the card
id/title into **Resumo** (e.g. `TRCLIENTE-741341`). If `get-card` fails, still
create the MR.

Do **not** write Linear keys (`DMI-NN`) or GitHub `Fixes #123`.

### 3. Title

Prefer, in order:

1. User-provided title
2. `[TRCLIENTE-NNNNNN] <card title or first commit, ≤72 chars>`
3. First meaningful commit subject if it already includes the card id

Rules: no trailing period; Portuguese unless the user writes in another language.

### 4. Description

Write in **Portuguese** unless the user asked otherwise. No checklists, no
Tipo/Superfície/Como testar. Group **Mudanças Principais** by theme (not by
file). List concrete files under **Ficheiros / áreas tocadas**.

```markdown
## Resumo
<1–3 frases: o que o MR faz e o efeito observável. Incluir o id do cartão se houver, ex. TRCLIENTE-741341.>

## Objetivos
- <resultado de negócio/técnico 1>
- <resultado 2>
- <cobertura de testes, se aplicável>

## Mudanças Principais
### <tema, ex. Feign / headers outbound>
- <o que mudou e porquê>

### Testes
- <ClasseDeTeste> — <cenários cobertos>

### Build / repo
- <versão no pom, .gitignore, CI — omitir a secção se nada disto mudou>

## Ficheiros / áreas tocadas
- `caminho/Ficheiro.java` — <papel da alteração>
- `pom.xml` — versão x.y.z
```

Example tone (do not copy the content unless the diff matches):

```markdown
## Resumo
Este MR adiciona um interceptor Feign (`UserHeaderInterceptor`) que propaga o
header `username` da requisição inbound como `X-User-Id` nas chamadas outbound
e define `X-Channel` como `backoffice`. O interceptor é registrado no cliente
Feign de periféricos via `FeignClientConfiguration`. Inclui testes unitários
para o interceptor e para `BackofficeAccessService`, bump de versão a 1.0.17 e
ajustes em `.gitignore`.

## Objetivos
- Propagar identidade do usuário nas chamadas Feign ao serviço de periféricos
- Garantir header `X-Channel: backoffice` em requisições outbound
- Cobertura de testes para interceptor e `BackofficeAccessService`

## Mudanças Principais
### Feign / headers outbound
- Novo `UserHeaderInterceptor`: lê `username`, envia `X-User-Id` (com trim) e `X-Channel`
- `FeignClientConfiguration`: registra interceptor no `FeignBuilder` do `PeripheralsApi`

### Testes
- `UserHeaderInterceptorTest` — username presente, trim, blank, sem contexto
- `BackofficeAccessServiceTest` — acesso concedido e negado

### Build / repo
- Versão 1.0.17 no `pom.xml`
- `.gitignore`: `.cursor/` e `scripts/`

## Ficheiros / áreas tocadas
- `src/main/java/.../config/UserHeaderInterceptor.java` — interceptor
- `src/main/java/.../config/FeignClientConfiguration.java` — registro Feign
- `src/test/java/.../config/UserHeaderInterceptorTest.java` — testes interceptor
- `src/test/java/.../BackofficeAccessServiceTest.java` — testes serviço
- `pom.xml` — versão 1.0.17
- `.gitignore` — entradas locais
```

Map files:

- `ms-bff-java-tr-backoffice/**` → BFF
- `main-tscript-tr-backoffice/**` → Frontend
- `.omp/Specs/**`, `.omp/skills/**` → Specs / `.omp` (do not open an MR from
  `.omp` itself; mention in the application-repo MR if those files changed in
  the same card)

### 5. Push

```bash
git push -u origin HEAD
```

### 6. Create MR

Example `create_merge_request` arguments:

```json
{
  "id": "67239320",
  "title": "[TRCLIENTE-741341] Externalizar secrets do BFF",
  "source_branch": "FEATURE/TRCLIENTE-741341",
  "target_branch": "develop",
  "description": "<markdown>"
}
```

Use `67566020` for the frontend repo. Do not set `reviewer_ids` unless the user
gave numeric GitLab user ids.

### 7. After create

Return the GitLab MR URL (`web_url`) to the user.

If a Business Map card id is known, offer (or run if the user already asked)
`businessmap-comment-branches` so the card lists `{repo} -> {branch}`. Do not
duplicate an existing branch comment.

## Errors

| Case | Action |
|------|--------|
| MCP `needsAuth` | Authenticate GitLab MCP, retry |
| Open MR already exists | Show its URL; do not create another |
| Push failed | Stop; do not call `create_merge_request` |
| Wrong repo | Confirm BFF vs frontend before creating |
| On `develop` | Ask the user to switch to a feature branch |

## Out of scope

- Force-push, skip-hooks, or merging the MR unless the user explicitly asks
