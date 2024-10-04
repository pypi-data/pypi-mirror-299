# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.3] - 2024-10-03

### Fixed

- Fixed an issue where `pendulum.DateTime` objects were not properly serialized by `JsonSerializationWriter`. Now, `pendulum.DateTime` objects are correctly recognized as subclasses of `datetime.datetime` and serialized accordingly.

## [1.3.2] - 2024-09-10

### Added

- Fixed numeric strings from being parsed as Datetime objects to being parsed as strings.
- Only parse to Datetime objects that conform to ISO 8601 format.

## [1.3.1] - 2024-08-23

### Added

- Fixed 4-digit numeric strings from being parsed as Datetime objects to being parsed as strings.

## [1.3.0] - 2024-07-26

### Added

- Support `dict[str, Any]` and `list[dict[str, Any]]` when writing additional data.

### Changed

- Fixed a bug where date time deserialization would fail because of empty strings.
- Fixed a bug where float deserialization if the number represented qualified as an int.

## [1.2.0] - 2024-04-09

### Added

### Changed

- Enhanced error handling: Enabled silent failure when an enum key is not available

## [1.1.0] - 2024-02-29

### Added

### Changed

- Support objects and collections when writing additional data.

## [1.0.1] - 2023-12-16

### Added

### Changed

- Bump pendulum to v3.0.0b1 for python 3.12 support.

## [1.0.0] - 2023-10-31

### Added

### Changed

- GA release

## [0.4.2] - 2023-10-11

### Added

### Changed

- Switched from python-dateutil to pendulum for parsing datetime types.

## [0.4.1] - 2023-09-21

### Added

### Changed

- Allow passing of valid strings as values for datetime and UUID fields.

## [0.4.0] - 2023-07-27

### Added

### Changed

- Enabled backing store support

## [0.3.7] - 2023-07-04

### Added

### Changed

- Fixes the key assignment to the writer in write_bytes_value.

## [0.3.6] - 2023-06-27

### Added

### Changed

- Fixed a bug with loading json response in method to get root parse node.

## [0.3.5] - 2023-06-14

### Added

- Added support for composed types (de)serialization.

### Changed

- Fixed a bug with assigning field values.

## [0.3.4] - 2023-05-17

### Added

### Changed

- Fixed a bug with assigning field values.

## [0.3.3] - 2023-04-27

### Added

### Changed

- Fixed a bug with deserializing collection of enum values.

## [0.3.2] - 2023-04-27

### Added

### Changed

- Fixed a bug with deserializing models with additional data.

## [0.3.1] - 2023-03-20

### Added

### Changed

- Fixed a bug with deserializing bytes responses.

## [0.3.0] - 2023-03-09

### Added

### Changed

- Switched from snake casing api response keys to prevent mismatch scenarios.
- Fixed a bug with getting child node using deserializer identifier

## [0.2.2] - 2023-02-21

### Added

### Changed

- Fixed a bug with deserializing 'None' string values in enums.
