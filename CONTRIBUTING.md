# Contributing

Keep changes focused and independently reviewable. Include relevant tests and
documentation with behaviour changes.

## Branches

Use `<type>/<short-description>` for branch names, for example:

- `fix/platform-variable-overrides`
- `feat/named-rule-blocks`
- `docs/rule-examples`
- `chore/release-conventions`

Use the type that best describes the main purpose of the branch. Supported types
are `feat`, `fix`, `docs`, `style`, `refactor`, `test` and `chore`.

## Commits

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```text
<type>(<scope>): <description>
```

Use a concise scope, an imperative description and a subject shorter than 72
characters. When a body is needed, explain what changed and why, wrapping lines
at fewer than 80 characters.

For example:

```text
fix(vars): honour inventory overrides
```

Mark breaking changes with `!` and include a `BREAKING CHANGE:` footer describing
the impact and required migration:

```text
feat(config)!: preserve unmanaged rules with named blocks

Manage role-owned rules without replacing unrelated configuration.

BREAKING CHANGE: Existing unmarked role-generated rules must be reviewed
and removed when adopting the managed inventory block.
```

## Tests

Install `ansible-core` in your development environment, then run the local test
suite from the repository root:

```sh
ansible-playbook -i tests/inventory.yml tests/main.yml
```

A successful run reports no failed or unreachable hosts. Test failures produce
a non-zero exit status.

Add new test playbooks to `tests/main.yml` so this command continues to run the
complete local suite. Local tests should run without elevated privileges and
must not modify system configuration.

## Changelog

Add user-visible changes to the `Unreleased` section of `CHANGELOG.md` in the
same change that introduces them. Describe the effect on users rather than
repeating commit subjects.

Use these sections as needed, omitting empty sections:

- `Breaking Changes`: incompatible changes and migration instructions.
- `Added`: new features.
- `Changed`: changes to existing behaviour.
- `Deprecated`: features scheduled for removal.
- `Removed`: removed features.
- `Fixed`: bug fixes.
- `Security`: security fixes.

Internal-only refactoring, tests and project maintenance do not require entries
unless they affect users. Do not reconstruct entries for historical releases.

## Releases

Accumulate changes under `Unreleased`. Upon release, rename that section to the
appropriate version and release date, then start a new `Unreleased` section.

Release versions follow Semantic Versioning:

- Patch releases contain backwards-compatible fixes.
- Minor releases introduce backwards-compatible functionality.
- Major releases introduce breaking changes.

Branch prefixes do not determine version increments. Assess the combined
user-visible changes since the previous release, including any breaking changes.
Documentation and maintenance changes do not inherently require a release.
Do not increment the version or create a release tag for each commit.

When preparing a release:

1. Review all changes since the previous release and verify the supported
   platforms and behaviours affected by those changes.
2. Complete the changelog, including any migration instructions.
3. Rename the `Unreleased` heading to the release version and date, using
   `## [X.Y.Z] - YYYY-MM-DD`.
4. Add a new empty `## [Unreleased]` section above the release entry.
5. Commit the release documentation using a Conventional Commit such as
   `chore(release): prepare X.Y.Z`.
6. Tag the release commit with the version, retaining the existing tag style
   without a `v` prefix, using `X.Y.Z`.

Releases and tags are explicit release actions, separate from ordinary changes.
