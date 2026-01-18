# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
