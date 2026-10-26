# Node/npm remediation reference

This companion distills the primary-source research into the installed skill's operational contract.

## Resolution facts

- The effective version may come from a direct dependency, workspace manifest, pnpm catalog entry, transitive parent, peer dependency, lockfile pin, or override—not merely the nearest visible `package.json` entry.
- A lockfile entry that still satisfies the manifest range is installed as-is, so an old pin can keep a vulnerable version even when every range admits the fix.
- npm hoists by default and nests a second copy only where needed; pnpm links each package to only what it declares, with versions side by side under `node_modules/.pnpm`; Yarn Berry defaults to plug'n'play, and Yarn 1 hoists into `node_modules`. One package name can be installed at several versions, so check every copy.
- Caret ranges keep the left-most non-zero element: `^1.2.3` is `<2.0.0`, but `^0.2.3` is `<0.3.0`. A prerelease satisfies a range only when a comparator on the same version tuple has a prerelease tag.
- `engines` is advisory unless `engine-strict` is set. npm peer conflicts warn by default and fail only with `strict-peer-deps`; pnpm fails only with `strictPeerDependencies`. pnpm `peerDependencyRules` hide mismatches rather than fix them.
- pnpm `minimumReleaseAge` (default one day in pnpm 11) and Yarn `npmMinimalAgeGate` (default one week) refuse recently published versions, including a just-published fix.

## Package-manager detection

| Manager | Signals | Override location | Frozen install |
|---|---|---|---|
| npm | `package-lock.json` or `npm-shrinkwrap.json` | root `package.json` `overrides` | `npm ci` |
| pnpm 11+ | `pnpm-lock.yaml`, `packageManager: pnpm@11…` | `pnpm-workspace.yaml` `overrides` | `pnpm install --frozen-lockfile` |
| pnpm ≤10 | `pnpm-lock.yaml`, older `packageManager` | where the repository already keeps them, usually root `package.json` `pnpm.overrides` | `pnpm install --frozen-lockfile` |
| Yarn Berry | `yarn.lock` with a `__metadata` header, `.yarnrc.yml` | root `package.json` `resolutions` | `yarn install --immutable` |
| Yarn 1 | `yarn.lock` with a `# yarn lockfile v1` header | root `package.json` `resolutions` | `yarn install --frozen-lockfile` |

Pass the same tree-changing flags CI uses, such as `--legacy-peer-deps`, to the frozen install.

## Graph commands

| Manager | List every copy | Explain a copy | Audit coverage |
|---|---|---|---|
| npm | `npm ls <pkg> --all --workspaces --include-workspace-root`; `--package-lock-only` reads the lockfile | `npm explain <pkg>`, or a `node_modules` path for one copy | `npm audit` without `--omit` |
| pnpm | `pnpm list <pkg> --depth Infinity -r` | `pnpm why <pkg> -r` | `pnpm audit` |
| Yarn Berry | `yarn info -R -A --dependents <pkg>` | `yarn why <pkg> -R`; `yarn why --peers`; `yarn explain peer-requirements` | `yarn npm audit -A -R` |
| Yarn 1 | `yarn why <pkg>`, which also shows where each copy is hoisted | `yarn why <pkg>` | `yarn audit` |

`npm ls` and `pnpm list` default to depth 0 and hide transitive copies. `yarn npm audit` defaults to the active workspace's direct dependencies. `--omit` in npm also drops findings from the audit.

## Fix order

Stop at the first step the evidence supports:

1. **Lockfile refresh.** The owner's declared range already admits a fixed version. Refresh only that entry: `npm install <pkg>@<fixed> --package-lock-only` for a direct dependency or `npm update <pkg>` for a transitive one, `pnpm update <pkg> --no-save` or `pnpm install --lockfile-only`, `yarn up -R <pkg>` with `--mode=update-lockfile`, or Yarn 1 `yarn upgrade <pkg>`. `dedupe` can drop an older duplicate when a newer in-range copy exists; preview it with `npm dedupe --dry-run`, `pnpm dedupe --check`, or `yarn dedupe --check`.
2. **First-party range.** The range excludes the fix and the owner is the project or a workspace: edit that range, or the pnpm catalog entry that owns it.
3. **Third-party parent.** The owner is a dependency: upgrade it to a release whose range admits the fix.
4. **Override.** No parent release admits the fix, or the parent upgrade needs a framework change: add an override scoped to the narrowest parent selector, and record why the parent could not be upgraded.

## Override mechanics

- All three managers read overrides only from the project root. npm ignores overrides in dependencies and workspaces; Yarn Berry warns on `resolutions` outside the root; pnpm reads them only at the root.
- npm: `"foo": "1.0.1"` applies everywhere; `"bar": { "foo": "1.0.1" }` or `"bar@2.0.0": { … }` scopes it to a parent. Overriding a direct dependency with a different spec throws `EOVERRIDE`; reference it as `"foo": "$foo"` and change the direct range instead.
- Yarn Berry: `"parent/foo": "1.0.1"` scopes one level deep. Yarn 1: `"parent/**/foo": "^1.0.1"`; its docs warn that nested paths may not work, so verify in the graph.
- pnpm: `"foo@<1.0.1": "1.0.1"` scopes by vulnerable range; `"parent@2>foo": "1.0.1"` scopes by parent; `foo: "catalog:"` takes the catalog version. pnpm 11 and later no longer read the `pnpm` field of `package.json`.
- Overrides fix only the repository's own install. Consumers of a published library resolve its declared `dependencies`, so a library must also widen that range or report the limitation.

## Automated fixers

- `npm audit fix` runs a full install that can move unrelated packages. Treat its result as a proposal: run it with `--package-lock-only`, review the diff against the fix order, and verify like any other change.
- `npm audit fix --force` installs outside declared ranges, including major versions. Never run it.
- `pnpm audit --fix` writes overrides and, with a release-age gate, adds `minimumReleaseAgeExclude` entries. `pnpm audit --fix=update` (pnpm 11) updates the lockfile instead. Accept neither result without checking it against the fix order and the boundary.
- `yarn npm audit` and Yarn 1 `yarn audit` have no fix mode.

## Loop invariants

At the end of every successful iteration:

1. Every changed package resolves to a version that fixes its finding: at or above a guidance-listed fixed version on the same line and outside every affected range.
2. No targeted vulnerable version remains in any workspace, optional, peer, dev, nested, or hoisted path.
3. One owning declaration controls each changed version; no symptom-only duplicate, removal, or audit suppression was introduced.
4. Related framework, toolchain, and workspace versions remain on an evidence-supported alignment.
5. The frozen install and the complete repository build pass.

The last state satisfying all five invariants is the rollback point for the next iteration. Preserve unrelated user edits when returning to it.

## Candidate evaluation

For each guidance-listed candidate, record:

| Evidence | Question |
|---|---|
| Release line | Does it preserve the current supported framework/toolchain or workspace contract? |
| Reachability | Does the owner's declared range already admit it, or does the range or parent have to change? |
| Package model | Do its `engines`, peer ranges, and optional dependencies fit the repository's Node and framework versions, checked explicitly? |
| Availability | Does the registry serve it under the repository's release-age gate? |
| Alignment | Does upstream framework/toolchain guidance support this member version or local override? |
| Resolution | Does the complete graph select a fixing version everywhere the vulnerable version was selected? |
| Behavior | Do the frozen install and full build pass without application or test code changes? |

The fixed-version list supplies candidates, not a ranking. Do not infer compatibility from version numbers alone.

## Failure isolation

When a multi-fix iteration fails:

1. Restore only this workflow's dependency edits to the last passing state.
2. Split the attempted owner changes into two coherent groups. Keep findings sharing one owner together.
3. Apply one group, refresh the lockfile and graph, and run the frozen install and full build.
4. Retain a passing group; split a failing group again.
5. Once one owner change is isolated, try its other candidates.
6. Stop on that finding when every candidate requires source or test changes. Keep other passing fixes.

A registry or network failure, or a release-age gate refusing a new version, is not proof of incompatibility. Report it with the exact command and output instead of guessing.

## Stop conditions

Stop and report evidence when:

- the reported package/version is not present in the installed graph;
- the pasted package or fixed-version guidance is missing or ambiguous;
- the finding has no fixed version, its record is withdrawn, or it is a malware advisory;
- every candidate violates engine, peer, or platform constraints;
- a release-age gate blocks every candidate;
- changing a shared external config or catalog lacks upstream alignment evidence;
- verification requires application or test code changes;
- the complete graph cannot be produced, or the frozen install or full build cannot run.

## Acceptance exercise

Given two pasted findings where one direct dependency controls two vulnerable packages and another package is pinned only through a transitive lockfile path whose parent range already admits the fix, a conforming run:

1. identifies the direct dependency and the lockfile pin as the two owners;
2. refreshes only the pinned lockfile entry and applies a compatible direct-dependency update, asking before a framework-line upgrade;
3. proves with full-depth graph commands that every installed copy resolves to a fixing version;
4. runs the frozen install and full build after each iteration;
5. bisects the two owner changes if the combined build fails;
6. retains the passing change and reports the reverted finding if every candidate requires application-code changes.

## Primary sources

- npm: [package.json](https://docs.npmjs.com/cli/v11/configuring-npm/package-json) (`overrides`, `engines`, peer and optional dependencies), [npm install](https://docs.npmjs.com/cli/v11/commands/npm-install), [npm ci](https://docs.npmjs.com/cli/v11/commands/npm-ci), [npm ls](https://docs.npmjs.com/cli/v11/commands/npm-ls), [npm explain](https://docs.npmjs.com/cli/v11/commands/npm-explain), [npm audit](https://docs.npmjs.com/cli/v11/commands/npm-audit), [npm update](https://docs.npmjs.com/cli/v11/commands/npm-update), [npm dedupe](https://docs.npmjs.com/cli/v11/commands/npm-dedupe)
- pnpm: [dependency resolution settings](https://pnpm.io/settings/dependency-resolution), [peer dependency settings](https://pnpm.io/settings/peer-dependencies), [catalogs](https://pnpm.io/catalogs), [package.json](https://pnpm.io/package_json), [install](https://pnpm.io/cli/install), [update](https://pnpm.io/cli/update), [audit](https://pnpm.io/cli/audit), [why](https://pnpm.io/cli/why), [list](https://pnpm.io/cli/list), [dedupe](https://pnpm.io/cli/dedupe)
- Yarn Berry: [manifest](https://yarnpkg.com/configuration/manifest), [yarnrc](https://yarnpkg.com/configuration/yarnrc), [install](https://yarnpkg.com/cli/install), [up](https://yarnpkg.com/cli/up), [why](https://yarnpkg.com/cli/why), [info](https://yarnpkg.com/cli/info), [npm audit](https://yarnpkg.com/cli/npm/audit), [dedupe](https://yarnpkg.com/cli/dedupe)
- Yarn 1: [selective version resolutions](https://classic.yarnpkg.com/en/docs/selective-version-resolutions), [install](https://classic.yarnpkg.com/en/docs/cli/install), [upgrade](https://classic.yarnpkg.com/en/docs/cli/upgrade), [why](https://classic.yarnpkg.com/en/docs/cli/why), [audit](https://classic.yarnpkg.com/en/docs/cli/audit)
- [node-semver](https://github.com/npm/node-semver)
- [OSV schema](https://ossf.github.io/osv-schema/)
- [About the GitHub Advisory Database](https://docs.github.com/en/code-security/security-advisories/working-with-global-security-advisories-from-the-github-advisory-database/about-the-github-advisory-database)
