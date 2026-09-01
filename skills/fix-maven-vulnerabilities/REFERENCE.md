# Maven remediation reference

This companion distills the primary-source research into the installed skill's operational contract.

## Resolution facts

- The effective version may come from inheritance, a property, an active profile, dependency management, an imported BOM, plugin management, or a plugin dependency—not the nearest visible dependency element.
- Maven mediates transitive versions by nearest definition, then first declaration at equal depth. Dependency management can control transitive versions.
- Imported BOM order and coordinated framework versions matter. Maven version ordering does not prove API compatibility.
- Project dependency management does not automatically control a plugin's classpath.
- `help:effective-pom -Dverbose` identifies effective inputs and their origins. `dependency:tree -Dverbose` shows selected and omitted dependency paths.

## Loop invariants

At the end of every successful iteration:

1. Every changed coordinate resolves to a version explicitly allowed by the pasted guidance.
2. No targeted vulnerable version remains in any relevant module, profile, scope, classifier, type, or plugin path.
3. One owning declaration controls each changed version; no symptom-only duplicate, exclusion, or suppression was introduced.
4. Related parent, BOM, framework, and plugin versions remain on an evidence-supported alignment.
5. The complete repository Maven build passes.

The last state satisfying all five invariants is the rollback point for the next iteration. Preserve unrelated user edits when returning to it.

## Candidate evaluation

For each guidance-listed candidate, record:

| Evidence | Question |
|---|---|
| Release line | Does it preserve the current supported parent/BOM/framework or plugin line? |
| Maven model | Does it satisfy hard ranges, repository availability, Maven/JDK prerequisites, profiles, and mediation? |
| Alignment | Does upstream parent/BOM/framework guidance support this member version or local override? |
| Resolution | Does the complete graph select the candidate everywhere the vulnerable version was selected? |
| Behavior | Does the full Maven build pass without application or test code changes? |

The fixed-version list supplies candidates, not a ranking. Do not infer compatibility from version numbers alone.

## Failure isolation

When a multi-fix iteration fails:

1. Restore only this workflow's dependency edits to the last passing state.
2. Split the attempted owner changes into two coherent groups. Keep findings sharing one owner together.
3. Apply one group, regenerate the graph, and run the full build.
4. Retain a passing group; split a failing group again.
5. Once one owner change is isolated, try its other safe candidates.
6. Stop on that finding when every safe candidate requires source or test changes. Keep other passing fixes.

A repository/infrastructure failure unrelated to the dependency diff is not proof of incompatibility. Report it with the exact command and output instead of guessing.

## Stop conditions

Stop and report evidence when:

- the reported coordinate/version is not present in the effective graph;
- the pasted coordinate or fixed-version guidance is missing or ambiguous;
- every guidance-listed candidate violates Maven or platform constraints;
- changing an external parent/BOM lacks upstream alignment evidence;
- verification requires application or test code changes;
- the complete graph cannot be produced or the full build cannot run.

## Acceptance exercise

Given two pasted findings where one property controls two vulnerable artifacts and another artifact is managed by an imported BOM, a conforming run:

1. identifies the property and BOM as the two owners;
2. applies compatible dependency-only updates, asking before a BOM-line upgrade;
3. proves all relevant resolved paths use guidance-listed safe versions;
4. runs the full Maven build after each iteration;
5. bisects the two owner changes if the combined build fails;
6. retains the passing property update and reports the reverted BOM finding if all safe BOM candidates require application-code changes.

## Primary sources

- [Apache Maven POM Reference](https://maven.apache.org/pom.html)
- [Apache Maven dependency mechanism](https://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html)
- [Apache Maven Help Plugin: `help:effective-pom`](https://maven.apache.org/plugins/maven-help-plugin/effective-pom-mojo.html)
- [Apache Maven Dependency Plugin: `dependency:tree`](https://maven.apache.org/plugins/maven-dependency-plugin/tree-mojo.html)
- [MojoHaus Versions Maven Plugin](https://www.mojohaus.org/versions/versions-maven-plugin/)
- [OSV schema](https://ossf.github.io/osv-schema/)
