---
name: code-test
description: MUST use when implementing a code change that needs behavioral verification, when a task requires tests, or when the user asks to add or improve tests.
---

# Code Test

Write and run tests for **one** task in the same pass as the production change.

Pick the stack from **Target Files** (both, if the task spans both):

| Target Files | Stack | Command (repo cwd) | Pass line |
|--------------|-------|--------------------|-----------|
| Maven repo (`*.java`, `pom.xml`, OpenAPI) | Java | `mvn test` | `mvn test: PASS` |
| `mfe-part-tscript-tr-customer-invoice/` | TS/React | `npm test` | `npm test: PASS` |

CI: **≥80% new-code coverage** (Sonar on Java). Behavioral tests, not padding.

## You do

1. Read the current task (Success Criteria, Target Files).
2. Implement production + tests together. Match neighbors in that repo.
3. Map each Success Criteria item to at least one test name.
4. Run the command(s) above. Failures → fix; do not return to the orchestrator. The reviewer will not re-run tests.

## Shared rules

- **State over interaction** — assert outcomes, not `verify()` / `toHaveBeenCalled` call order (URL/body at an HTTP boundary is fine).
- **DAMP over DRY** — self-contained tests.
- **Real > fake > stub > mock** — mock ports, HTTP clients, and browser APIs at the edge.
- **Arrange–Act–Assert** — one concept per test.
- **Ponytail** — one test per branch the task introduced; skip trivial one-liners; bug fix → one reproduction test.
- No log-text asserts, snapshots, mega-fixtures, `@Disabled` / `xtest` / skipped tests.
- Do not test framework/library behavior or untouched code.

## Java

Tests under `src/test/java`, mirroring the class under test.

| Layer | How |
|-------|-----|
| `application/domain` | Unit, `@ExtendWith(MockitoExtension.class)`, mock ports only |
| `adapter/out` | Unit, mock Feign/client |
| `adapter/in` | Only if the task changes the controller contract |

Skip `@SpringBootTest` unless the task needs it or a neighbor already uses it.

- Class: `{ProductionClass}Test`
- Method: `given{Context}_when{Action}_then{Outcome}`
- `@DisplayName`: Portuguese Given / When / Then

```java
@Test
@DisplayName("Dado cupom inválido Quando validar Então lança BusinessException")
void givenInvalidCoupon_whenValidate_thenThrows() {
    var input = InvoiceInbound.builder().couponNumber(-1L).build();
    Assertions.assertThrows(BusinessException.class, () -> service.run(true, input));
}
```

No private-method tests, no Feign call-order verifies, no SQL-string asserts.

## TS / React (MFE)

Colocate `{name}.spec.ts` / `{name}.spec.tsx` next to the file (existing MFE pattern). Jest + Testing Library. Do not add Vitest.

| Kind | How |
|------|-----|
| helper / mapper / rule | `describe` + `it('should …')` + `expect` |
| BFF use case | mock HTTP client; assert URL/body/result |
| hook | Testing Library hooks neighbor style |
| component | `@testing-library/react` — user-visible behavior, not internals |

Match neighboring specs (jest.mock of logger/hooks, `@/` imports). No new snapshot files. No Playwright/Cypress (smoke is the validator).

## Done when

- Required command(s) pass in the repo cwd
- Every Success Criteria item maps to a test name (or one-line skip why)
- New tests follow neighbors in that module

## Output

No preamble:

```text
mvn test: PASS
npm test: PASS

Coverage map:
- Success Criteria 1 → givenValidRequest_whenValidate_thenReturnsWithoutErrors
- Success Criteria 2 → should call fetchHttpClient.post with the correct URL
```

Emit only the pass lines for stacks this task touched.
