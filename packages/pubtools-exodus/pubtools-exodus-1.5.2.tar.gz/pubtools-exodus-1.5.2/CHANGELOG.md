# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- n/a

## [1.5.2] - 2024-09-27

- Fix pubtools packaging conflicts by moving pubtools-exodus to a src layout

## [1.5.1] - 2023-12-05

- fixed some failing HTTP requests not being retried as intended

## [1.5.0] - 2023-10-20

- pubtools-pulplib integration now uses phase1 commits to ensure correct behavior
  of Pulp fast-forward publish

## [1.4.0] - 2023-09-27

- pubtools-pulplib integration can now be toggled via `EXODUS_PULP_HOOK_ENABLED`
  environment variable

## [1.3.2] - 2022-12-13

- pubtools-exodus-push: Fix exodus-rsync log buffering

## [1.3.1] - 2022-10-25

- pubtools-exodus-push: fixed source directory basename incorrectly included in destination
  path when publishing a directory

## [1.3.0] - 2022-08-19

- When using pubtools-pulplib integration, exodus publishes are now committed at
  `task_stop` (formerly were committed only at `task_pulp_flush`).

## [1.2.0] - 2022-06-27

- Reduce repeated argument parsing in ExodusTask
- pubtools-exodus-push: Exclude *.nfs, .latest_rsync, .lock files for legacy parity

## [1.1.0] - 2022-06-13

### Changed

- Automatically poll commit for completion once published
- Improve logging for commit publishes
- Misc. clean-up, update pre-commit hooks

## [1.0.2] - 2022-04-27

### Fixed

- pubtools-exodus-push: Fix crash when EXODUS_ENABLED is not set or false

## [1.0.1] - 2022-04-05

### Fixed

- Check EXODUS_ENABLED before populating vars from env 

## [1.0.0] - 2022-03-23

### Changed

- pubtools-exodus-push: Load content using the pushsource library

## 0.1.0 - 2022-02-24

- Initial release
- Introduce pubtools-exodus-push entry point task
- Introduce exodus-pulp hook implementers
- Introduce project structure, config, CI

[Unreleased]: https://github.com/release-enineering/pubtools-exodus/compare/v1.5.2...HEAD
[1.5.2]: https://github.com/release-engineering/pubtools-exodus/compare/v1.5.1...v1.5.2
[1.5.1]: https://github.com/release-engineering/pubtools-exodus/compare/v1.5.0...v1.5.1
[1.5.0]: https://github.com/release-engineering/pubtools-exodus/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.com/release-engineering/pubtools-exodus/compare/v1.3.2...v1.4.0
[1.3.2]: https://github.com/release-engineering/pubtools-exodus/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/release-engineering/pubtools-exodus/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/release-engineering/pubtools-exodus/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/release-engineering/pubtools-exodus/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/release-engineering/pubtools-exodus/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/release-engineering/pubtools-exodus/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/release-engineering/pubtools-exodus/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/release-engineering/pubtools-exodus/compare/v0.1.0...v1.0.0
