# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2026-02-25

### Changed
- **Breaking**: `entity` and `multi_entity` fields now generate columns conditionally based on the number of valid target types:
  - `entity` with **1 valid type**: generates `{field}_id` with a `ForeignKey` constraint to `{target}.id`; no `{field}_type` column
  - `entity` with **0 or >1 valid types**: generates `{field}_id` (BigInteger) + `{field}_type` (String) for runtime disambiguation (polymorphic ref)
  - `multi_entity` with **1 valid type**: generates only `{field}_ids` (String); no `{field}_type` column
  - `multi_entity` with **0 or >1 valid types**: generates `{field}_ids` (String) + `{field}_type` (String) for disambiguation
- Missing or null `valid_types` falls back to the multi-type (polymorphic) path as a safe default

### Added
- FK constraints on single-target `entity` fields, enabling referential integrity in the database
- New test fields `entity_source` and `task_assignees` in the example schema to cover multi-type entity/multi_entity paths
- Tests: `test_entity_field_single_valid_type_fk`, `test_entity_field_single_valid_type_no_type_col`, `test_entity_field_multi_valid_type_keeps_type_col`, `test_entity_field_multi_valid_type_no_fk`, `test_multi_entity_field_single_valid_type_no_type_col`, `test_multi_entity_field_multi_valid_type_keeps_type_col`, `test_entity_field_fk_enforced_in_db`

## [0.2.0] - 2026-02-24

### Added
- Safe multiple instantiation: each `SGORM` instance now gets its own `DeclarativeBase`, preventing SQLAlchemy `SAWarning` about duplicate class names when creating more than one instance in the same process
- `pytest` pre-commit hook to catch regressions before commits
- Regression tests for entity and multi-entity column naming conventions

### Changed
- **Breaking**: Uniform column generation for `entity` and `multi_entity` fields — all columns are now added to the source table regardless of v_table count:
  - `entity` fields produce `{field}_id` (BigInteger) and `{field}_type` (String)
  - `multi_entity` fields produce `{field}_ids` (String) and `{field}_type` (String)
  - Removes the previous behaviour of injecting a `{v_table}_{field}_id` column for single-v_table entity fields and a cross-table `{SourceTable}_{field}_id` column for multi_entity fields
- Primary key `id` columns changed from `Integer` to `BigInteger` to match Shotgrid's 64-bit IDs
- Updated documentation and examples to reflect new column naming convention

## [0.1.1] - 2026-01-17

### Changed
- Fixed tests

## [0.1.0] - 2026-01-17

### Added
- Initial beta release of Shotgrid ORM Generator
- Support for generating SQLAlchemy ORM models from Shotgrid schemas
- Multiple schema source types: JSON file, JSON text, SG user authentication, SG script authentication, existing connection
- Dynamic class generation with proper type hints using SQLAlchemy 2.0 syntax
- Support for all Shotgrid field types including entity relationships, multi-entity fields, and custom types
- Automatic handling of polymorphic entity relationships via _id and _type fields
- Script generation capability to create standalone Python ORM files
- Alembic integration for database migrations
- Non-auto-increment primary keys to preserve Shotgrid native IDs
- Comprehensive test suite covering model creation, database operations, and script generation

### Changed
- Improved documentation with clear notes on foreign key handling and type limitations
- Enhanced type mapping documentation explaining design decisions for complex types
- Version bumped to 0.1.0 for initial public release

### Technical Notes
- ForeignKey constraints intentionally not generated to allow maximum flexibility for data transfer
- Entity and multi-entity types stored as integers/strings rather than full relationship objects
- Serializable and URL types stored as strings (JSON serialization available for complex cases)
- Compatible with Python 3.7+
- Requires SQLAlchemy 2.0.22+, shotgun-api3 3.4.0+, sqlacodegen-v2 0.1.4+, alembic 1.12.1+

## [Unreleased]

### Future Enhancements
- Optional SQLAlchemy relationship() support for entity fields
- JSON column type support for serializable fields in compatible databases
- Additional type validators and custom SQLAlchemy types for Shotgrid-specific fields
- Enhanced documentation with more examples and use cases
