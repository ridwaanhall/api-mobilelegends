# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-12

### Added

- Complete project restructuring for better maintainability

- Comprehensive documentation (README, CONTRIBUTING, USAGE, ARCHITECTURE)
- Type hints throughout the codebase
- Pydantic models for request/response validation
- Service layer for business logic separation
- Structured logging with colored output
- Unit tests with pytest
- Health check endpoint
- Custom error handlers
- Migration script for easier transition

### Changed

- Moved from flat structure to modular architecture
- Separated concerns into core, services, models, and utils
- Improved error handling and logging
- Updated dependencies to latest versions
- Enhanced API documentation with detailed descriptions
- Refactored configuration management
- Improved CORS handling

### Fixed

- Better exception handling in HTTP client
- More robust error messages
- Proper type checking throughout

### Security

- Enhanced cryptographic utilities
- Better secret management
- Improved input validation

## [1.0.0] - Previous Version

### Initial Release

- Basic FastAPI application
- MLBB API integration
- Hero endpoints
- Win rate calculator
- Basic documentation

---

For detailed changes, see the [commit history](https://github.com/ridwaanhall/api-mobilelegends/commits).
