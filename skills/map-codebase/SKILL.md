---
name: map-codebase
description: Use when the user asks to map a codebase or when another skill needs a complete, source-grounded map of selected repository boundaries.
---

# Map Codebase

Map selected repository boundaries with parallel read-only subagents. Return evidence to the invoking skill; do not write final documentation.

## Decompose

1. Inspect the repository and divide the approved scope by real architectural boundaries: components, services, packages, layers, or responsibilities.
2. Merge tiny related boundaries. Run at most eight boundary agents in one wave.
3. If one boundary is too large, split it recursively by internal architecture and map those slices in another parallel wave.

## Boundary agents

Assign one read-only agent per boundary. Each agent must read every repository-owned file that defines the boundary's behavior:

- production source;
- tests as supporting evidence only;
- configuration, schemas, and scripts that affect behavior.

Exclude generated files, vendored dependencies, caches, and build output. Tests may confirm behavior but do not become documentation subjects.

Each report contains:

- purpose and responsibilities;
- entry points;
- dependencies and outbound contracts;
- important flows;
- public or cross-boundary contracts;
- invariants and non-obvious constraints;
- exact source files and relevant symbols;
- existing OKF concepts classified as confirmed, stale, missing, or conflicting;
- unresolved gaps.

Cite line ranges only when files and symbols do not disambiguate the evidence.

## Integrate

After every boundary report succeeds, run one read-only integration agent over the reports and relevant cross-boundary contracts. It maps end-to-end flows, mismatched assumptions, shared concepts, and relationships between boundaries.

Keep boundary and integration reports separate. Return all reports to the invoking skill. `okf-setup` owns the final concept map and OKF documents.

## Failures

Retry a failed assignment once with a narrower scope. If it remains too large, split it recursively and map the slices in parallel. Fail the mapping instead of silently returning incomplete coverage.

Do not persist intermediate reports in the repository.
