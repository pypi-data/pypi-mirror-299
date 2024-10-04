# Changelog

All notable changes to this project will be documented in this file.

<!--
## [Unreleased]

### Added

### Fixed

### Changed

### Removed
-->

## [0.1.2] - 2024-10-03

### Added

- Created the changelog to track changes in the project.
- Handle certain client errors better and display an error message.
- New `--version` flag to display the current version.
- New `--port` flag for controlling which port number to use.

### Changed

- The server now uses the machine's private IP address instead of
`127.0.0.1`, which allows clients on the local network to connect.
- Reworked the CLI interface to parse subcommands:
  - `bestow start` replaces `--server`.
  - `bestow connect` replaces `--client`.

## [0.1.1] - 2024-10-02

### Added

- Created PyPI package metadata.
- Implemented a simple async client/server interface:
  - `bestow --server` runs the server, which listens for a message.
  - `bestow --client` runs the client, which sends a message.

## [0.1.0] - 2024-10-02

### Added

- Basic project layout.
- The foundation upon which **Bestow** will be built!

[unreleased]: https://codeberg.org/ViteByte/bestow/compare/v0.1.2...HEAD
[0.1.2]: https://codeberg.org/ViteByte/bestow/compare/v0.1.1...v0.1.2
[0.1.1]: https://codeberg.org/ViteByte/bestow/compare/v0.1.0...v0.1.1
[0.1.0]: https://codeberg.org/ViteByte/bestow/src/tag/v0.1.0
