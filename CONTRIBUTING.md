# Contributing to Shotgrid ORM Generator

Thank you for your interest in contributing to Shotgrid ORM Generator! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming and inclusive environment for all contributors. Please be respectful, constructive, and professional in all interactions.

## Getting Started

Before contributing, please:

1. Check existing [issues](https://github.com/johnetran/shotgrid_orm/issues) to see if your bug/feature is already being discussed
2. For major changes, open an issue first to discuss what you would like to change
3. Fork the repository and create a feature branch for your work

## Development Environment Setup

### Prerequisites

- Python 3.7 or higher (Python 3.13 recommended for development)
- Git
- pip (Python package installer)

### Initial Setup

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/YOUR_USERNAME/shotgrid_orm.git
   cd shotgrid_orm
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies:**

   ```bash
   pip install -e ".[dev]"
   ```

   This installs the package in editable mode along with development tools: pytest, black, ruff, and mypy.

4. **Verify installation:**

   ```bash
   python -c "from shotgrid_orm import SGORM; print('Installation successful!')"
   ```

5. **Set up pre-commit hooks (recommended):**

   ```bash
   pre-commit install
   ```

   This will automatically run code quality checks before each commit. To run checks manually:

   ```bash
   pre-commit run --all-files
   ```

### Environment Variables (Optional)

If you need to test with a live Shotgrid connection:

```bash
export SG_URL="https://your-studio.shotgunstudio.com"
export SG_SCRIPT="your_script_name"
export SG_API_KEY="your_api_key_here"
```

**Note:** Never commit credentials to the repository. Use environment variables or `.env` files (which are gitignored).

## Development Workflow

1. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

2. **Make your changes** following the coding standards below

3. **Run tests** to ensure nothing is broken:

   ```bash
   python tests/test_sgorm.py
   python tests/test_createdb.py
   python tests/test_createscript.py
   python tests/test_model.py
   python tests/test_index.py
   ```

4. **Format your code** with Black:

   ```bash
   black src/ tests/
   ```

5. **Lint your code** with Ruff:

   ```bash
   ruff check src/ tests/
   ```

6. **Commit your changes** with descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

   Use prefixes like `Add:`, `Fix:`, `Update:`, `Refactor:`, `Docs:`, etc.

7. **Push to your fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

8. **Open a Pull Request** on GitHub

## Coding Standards

### Code Style

- **Formatting:** Use [Black](https://github.com/psf/black) for code formatting (line length: 120 characters)
- **Linting:** Use [Ruff](https://github.com/astral-sh/ruff) for fast linting
- **Type Hints:** Add type hints where appropriate (especially for public APIs)
- **Naming Conventions:**
  - Classes: `PascalCase` (e.g., `SGORM`, `SchemaType`)
  - Functions/Variables: `snake_case` (e.g., `create_script`, `sg_schema_type`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `SG_URL`)

### Documentation

- Add docstrings to all public modules, classes, and functions
- Use Google-style or NumPy-style docstrings
- Keep README.md and CHANGELOG.md up to date
- Comment complex or non-obvious code sections

### Code Organization

- Keep functions focused and single-purpose
- Avoid deeply nested code (prefer early returns)
- Follow existing patterns in the codebase
- Don't introduce new dependencies without discussion

### Imports

- Use absolute imports from `shotgrid_orm` package
- Group imports in this order:
  1. Standard library
  2. Third-party packages
  3. Local application imports
- Sort imports alphabetically within each group

## Testing

### Running Tests

Currently, tests use direct Python execution:

```bash
python tests/test_sgorm.py
python tests/test_createdb.py
python tests/test_createscript.py
python tests/test_model.py
python tests/test_index.py
```

**Note:** We are migrating to pytest. Future contributions should use pytest conventions.

### Writing Tests

- Write tests for all new functionality
- Ensure tests are deterministic (no random behavior)
- Use descriptive test names: `test_<what>_<condition>_<expected_result>`
- Keep tests focused on one behavior per test function
- Mock external dependencies (Shotgrid API calls) when possible

### Test Coverage

- Aim for at least 80% code coverage on new code
- Critical paths and edge cases must be tested
- Don't sacrifice test quality for coverage numbers

## Pull Request Process

### Before Submitting

- [ ] Code follows the project's coding standards
- [ ] All tests pass
- [ ] Code is formatted with Black
- [ ] New code includes appropriate tests
- [ ] Documentation is updated (README, docstrings, etc.)
- [ ] CHANGELOG.md is updated with your changes
- [ ] Commit messages are clear and descriptive
- [ ] No merge conflicts with `main` branch

### PR Description Template

When opening a PR, please include:

```markdown
## Description
Brief description of what this PR does

## Motivation and Context
Why is this change needed? What problem does it solve?

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
How has this been tested? Please describe the tests you ran.

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] I have updated the CHANGELOG.md
```

### Review Process

1. At least one maintainer must review and approve the PR
2. All CI checks must pass (tests, linting, etc.)
3. Address review feedback promptly
4. Once approved, a maintainer will merge your PR

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Description:** Clear description of the bug
- **Steps to Reproduce:** Minimal steps to reproduce the issue
- **Expected Behavior:** What you expected to happen
- **Actual Behavior:** What actually happened
- **Environment:**
  - Python version
  - shotgrid_orm version
  - Operating system
  - SQLAlchemy version
- **Additional Context:** Error messages, stack traces, screenshots

### Feature Requests

When requesting features, please include:

- **Description:** Clear description of the feature
- **Use Case:** Why is this feature needed? What problem does it solve?
- **Proposed Solution:** (Optional) How might this be implemented?
- **Alternatives:** (Optional) What alternatives have you considered?

### Questions

For general questions:

- Check the [README](README.md) first
- Search existing issues
- If still unclear, open an issue with the "question" label

## Development Tips

### Working with Alembic

If you make database schema changes:

```bash
# Generate a migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Building the Package Locally

```bash
# Build distribution packages
python -m build

# Check package metadata
twine check dist/*
```

### Testing Against Multiple Python Versions

Consider using `tox` or `nox` for testing against Python 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, and 3.13.

## Getting Help

If you need help with contributing:

- Open an issue with your question
- Tag it with the "question" or "help wanted" label
- Be patient and respectful - maintainers are volunteers

## Recognition

Contributors will be recognized in the project. Significant contributions may be acknowledged in release notes.

---

Thank you for contributing to Shotgrid ORM Generator!
