---
name: fix-node-vulnerabilities
description: MUST use when the user provides one or more npm/Node dependency vulnerability findings with remediation versions and asks to update dependencies, remediate the findings, or make the Node build secure. Use for dependency-only remediation; stop before application-code changes.
---

# Fix Node Vulnerabilities

Remediate every pasted Node/npm finding through dependency resolution, a frozen install, and a passing full build. Read [REFERENCE.md](REFERENCE.md) before editing.

## Input

Require one or more findings containing:

- the exact vulnerable package name and resolved version;
- remediation guidance listing one or more fixed versions.

Accept scanner-neutral pasted text. Treat its remediation guidance as the fix authority; do not require a scanner API or advisory lookup. If either required field is missing or ambiguous, ask for it before editing. A fixed version is the first fixed release on its line: a higher version on the same line that is outside every affected range the guidance names also fixes the finding.

## Boundary

Change Node dependency configuration only: `package.json` manifests, lockfiles, workspace manifests, `overrides`/`resolutions`, pnpm `pnpm-workspace.yaml` overrides and catalogs, and package-manager config. Never change application or test code, suppress a finding with an audit ignore list, or remove a dependency merely to hide it from the graph.

Apply compatible fixes autonomously when they preserve the current release line or established framework/toolchain contract. Ask before:

- upgrading a framework, major runtime line, or package-manager major version;
- editing the repository's own `engines` field;
- lowering a release-age gate or accepting an auto-added release-age exclusion;
- a local override of an externally owned shared config or catalog, which also requires upstream evidence that the override preserves alignment.

Never run `npm audit fix --force`.

## Workflow

1. Read repository guidance and detect the package manager and its major version: npm, pnpm (note whether it is 11 or later), Yarn Berry, or Yarn 1. Use the lockfile name and format, the `packageManager` field, and the CI configuration. Discover workspaces, Node and engine requirements, registry config, release-age gates, whether the repository publishes packages, and the CI install and full build commands. When none are documented, use the package manager's frozen install plus the `test` and `build` scripts from the workspace root.
2. Normalize all pasted findings into package name, vulnerable resolved version, and guidance-listed fixed versions. Preserve the original text. Stop on a finding with no fixed version, a withdrawn record, or a malware advisory.
3. Capture the pre-edit dependency graph with the full-depth, all-workspace commands in REFERENCE.md. Cover every workspace, optional and peer paths, dev dependencies, and every nested or hoisted copy. Confirm each reported vulnerable version is actually installed.
4. Explain each vulnerable copy back to its owner: direct dependency, workspace manifest, pnpm catalog entry, transitive parent, peer dependency chain, lockfile pin, or existing override.
5. Check reachability: compare the owner's declared range with each fixed version under semver rules, including caret behavior on `0.x` versions.
6. Evaluate guidance-listed versions as candidates. The list is not a ranking, so choose by compatibility evidence: the candidate's `engines`, peer ranges, registry availability, and alignment with the current framework and toolchain. The package manager only warns on `engines` and peer mismatches by default, so check them explicitly.
7. Apply the cheapest owner change in the fix order in REFERENCE.md: a targeted lockfile refresh, then a first-party range or catalog edit, then a third-party parent upgrade, then a narrowly scoped override. Reuse one owner change for several findings when possible. Record why each override was needed.
8. Refresh only the affected lockfile entries with the targeted commands in REFERENCE.md. Never delete the lockfile. Review the lockfile diff for unrelated version moves.
9. Verify the iteration:
   - rerun the full-depth graph commands; the iteration fails if any targeted vulnerable version remains, a new conflicting resolution appears, or a selected version does not fix its finding;
   - run the frozen install from a clean state with the same flags CI uses;
   - run the repository's full build.
   An iteration may contain multiple fixes, but all three checks are mandatory after every iteration.
10. Repeat until every finding is remediated. If an iteration fails, return to the last passing dependency state and bisect its dependency changes as REFERENCE.md describes. Keep independently passing fixes and try other guidance-listed candidates for the blocked finding.
11. If every candidate requires application or test code changes, revert that finding's dependency change, retain other verified fixes, and stop with the evidence described below. Do not edit code.

Only revert changes made by this workflow. Preserve pre-existing user changes.

## Done

Complete only when, for every unblocked finding:

- every installed copy resolves to a version that fixes the finding, and no targeted vulnerable version remains;
- related framework/toolchain/workspace alignment remains coherent;
- the frozen install and the repository's full build pass.

A manifest diff alone is not evidence. A vulnerability-scanner rerun is not required.

Report:

- each finding and final resolved version;
- the declaration that owned each version, the fix-order step used, and the files changed;
- each override added and why no parent upgrade could fix it;
- for a published library, whether consumers receive the fix through the declared `dependencies` range or only the repository's own install is fixed;
- dependency-graph commands and results;
- every frozen-install and full-build command and final result;
- retained fixes and, when blocked, attempted candidates, failure output, and why application-code changes or user approval would be required.
