---
name: fix-maven-vulnerabilities
description: MUST use when the user provides one or more Maven dependency vulnerability findings with remediation versions and asks to update dependencies, remediate the findings, or make the Maven build secure. Use for dependency-only remediation; stop before application-code changes.
---

# Fix Maven Vulnerabilities

Remediate every pasted Maven finding through dependency resolution and a passing full build. Read [REFERENCE.md](REFERENCE.md) before editing.

## Input

Require one or more findings containing:

- the exact vulnerable Maven coordinate and resolved version;
- remediation guidance listing one or more fixed versions.

Accept scanner-neutral pasted text. Treat its remediation guidance as the fix authority; do not require a scanner API or advisory lookup. If either required field is missing or ambiguous, ask for it before editing.

## Boundary

Change Maven dependency configuration only: POMs, version properties, parents, imported BOMs, dependency management, plugins, and plugin management. Never change application or test code, suppress a finding, or exclude an artifact merely to remove it from the graph.

Apply compatible fixes autonomously when they preserve the current release line or established BOM/framework contract. Ask before upgrading a parent, BOM, framework, or major release line. A local override of an externally owned parent or BOM also requires upstream evidence that the override preserves alignment.

## Workflow

1. Read repository guidance and discover the Maven wrapper or executable, reactor modules, active profiles, JDK/Maven requirements, repositories, and the repository's full Maven build command. Prefer `./mvnw`; when no repository command exists, use `verify` from the reactor root.
2. Normalize all pasted findings into coordinate, vulnerable resolved version, and guidance-listed candidate versions. Preserve the original text.
3. Capture the pre-edit effective model and complete relevant dependency graph. Use `help:effective-pom -Dverbose` and `dependency:tree`; include every affected module/profile and plugin path. Confirm each reported vulnerable version is actually resolved.
4. Trace the selected version to its owner: direct dependency, property, parent, local or inherited dependency management, imported BOM, plugin, plugin dependency, or plugin management.
5. Evaluate guidance-listed versions as candidates. Do not assume the lowest, current-line, or newest candidate is compatible. Reject candidates that violate Maven requirements, repository constraints, or platform alignment. Prefer the smallest candidate whose release line is supported by the current parent/BOM/framework evidence.
6. Edit the owning declaration. Reuse one owner change for multiple findings when possible. Do not add duplicate direct overrides; allow a local managed override only under the external-owner rule above.
7. Regenerate the complete relevant dependency graph. The iteration fails if any targeted vulnerable version remains, a new conflicting resolution appears, or the selected version is not one listed as safe by the pasted guidance.
8. Run the repository's full Maven build. An iteration may contain multiple fixes, but graph verification and the full build are mandatory after every iteration.
9. Repeat until every finding is remediated. If an iteration fails, return to the last passing dependency state and bisect its dependency changes with full builds. Keep independently passing fixes and try other safe guidance-listed candidates for the blocked finding.
10. If every safe candidate requires application or test code changes, revert that finding's dependency change, retain other verified fixes, and stop with the evidence described below. Do not edit code.

Only revert changes made by this workflow. Preserve pre-existing user changes.

## Done

Complete only when, for every unblocked finding:

- the effective Maven graph resolves a guidance-listed safe version and no targeted vulnerable version;
- related BOM/framework/plugin alignment remains coherent;
- the repository's full Maven build passes.

A POM diff alone is not evidence. A vulnerability-scanner rerun is not required.

Report:

- each finding and final resolved version;
- the declaration that owned each version and the files changed;
- effective-model and dependency-graph commands and results;
- every full-build command and final result;
- retained fixes and, when blocked, attempted candidates, failure output, and why application-code changes would be required.
