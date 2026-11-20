# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Earlier releases are not documented retrospectively.

## [Unreleased]

## [2.0.0] - 2026-11-20

### Breaking Changes

- Manage inventory rules in a named `inventory` block instead of replacing the
  entire doas configuration file. Content outside this block is preserved.
  Existing installations must review and remove old, unmarked role-generated
  rules when adopting the managed block; these entries are not migrated or
  removed automatically. Empty all, group and host rule lists now remove only
  the inventory block rather than clearing the configuration file.

### Added

- Add a callable `rules` entry point for independently named doas rule blocks,
  allowing other roles and playbooks to manage their own permissions without
  modifying inventory rule lists. Support creation, updates and explicit removal
  while preserving unrelated content and validating the complete configuration.

### Fixed

- Correct documentation examples to use the Galaxy role name `sjktje.doas`.
- Refuse sudo removal when the role is actively using sudo for privilege
  escalation, including settings supplied through become keywords or variable
  overrides. Reject unsafe requests before modifying packages or configuration.
- Correct the advertised minimum Ansible version to ansible-core 2.18.
- Honour inventory overrides for the configuration path on FreeBSD and
  configuration group on Debian.
