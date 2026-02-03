# Changelog

All notable changes to GRD will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.3] - 2026-02-02

### Fixed
- Brownfield detection now ignores all hidden directories (`.git`, `.venv`, `.planning`, etc.)

## [1.3.2] - 2026-02-02

### Fixed
- Gemini CLI agent validation error for `AskUserQuestion` tool (now filtered during conversion)

## [1.3.1] - 2026-02-02

### Changed
- Updated documentation terminology from GSD to GRD throughout
- Fixed package name and repository URLs in CONTRIBUTING.md and MAINTAINERS.md
- Removed testimonial quotes from README.md

## [1.3.0] - 2026-02-02

### Added
- Gemini CLI support with TOML agent conversion (`--gemini` flag)
- Multi-runtime installer (`--claude`, `--opencode`, `--gemini`, `--all` flags)
- Context bar scaling fix (shows 100% at 80% token limit)
- Branching strategy options (squash merge, preserve history, delete branch)
- Attribution commit settings (respect `attribution.commit` config)

### Changed
- Visual branding updated to GRD identity (research teal #4FB3D4 color palette)
- Logo assets renamed (`grd-logo-2000.svg/png`)
- Terminal preview shows v1.3.0 branding

## [1.2.0] - 2026-02-02

### Added
- Recursive validation loop with Critic agent for automated skeptical review
- Data-first philosophy with Explorer agent for data reconnaissance
- Hypothesis synthesis with Architect agent for testable experiment design
- Human-in-the-loop evaluation gates for final validation decisions
- Notebook graduation workflow for production script conversion
- Multi-runtime support (Claude Code, OpenCode)

## [1.1.0] - 2026-02-01

### Added
- Quick explore command (`/grd:quick-explore`) with Rich console output
- Accessible insights (`/grd:insights`) with plain English explanations
- Study-centric terminology (experiment/study vocabulary)

### Changed
- Renamed 6 lifecycle commands to research terminology
- GSD legacy commands removed or repurposed

## [1.0.0] - 2026-01-30

### Added
- Initial release: recursive ML experimentation framework
- Explorer agent with data profiling and leakage detection
- Architect agent with hypothesis synthesis
- Researcher/Critic/Evaluator recursive validation loop
- Human evaluation gate with evidence packages
- Notebook graduation workflow (papermill execution)
- 27 CLI commands for research workflow
- Multi-runtime support (Claude Code, OpenCode)

[Unreleased]: https://github.com/ulmentflam/get-research-done/compare/v1.3.2...HEAD
[1.3.2]: https://github.com/ulmentflam/get-research-done/compare/v1.3.1...v1.3.2
[1.3.1]: https://github.com/ulmentflam/get-research-done/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.com/ulmentflam/get-research-done/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/ulmentflam/get-research-done/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/ulmentflam/get-research-done/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/ulmentflam/get-research-done/releases/tag/v1.0.0
