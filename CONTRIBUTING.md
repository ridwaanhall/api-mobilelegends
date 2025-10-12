# Contributing to Mobile Legends API

First off, thank you for considering contributing to Mobile Legends API! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps to reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed and what behavior you expected
* Include logs and error messages if applicable

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a detailed description of the suggested enhancement
* Provide specific examples to demonstrate the enhancement
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Follow the Python style guide (PEP 8)
* Include appropriate test cases
* Update documentation as needed
* End all files with a newline

## Development Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Create a `.env` file based on `.env.example`
5. Run tests to ensure everything is working:
   ```bash
   pytest
   ```

## Style Guide

### Python Style

* Follow PEP 8
* Use type hints for all function parameters and return values
* Maximum line length: 100 characters
* Use docstrings for all modules, classes, and functions
* Format code with `black`
* Sort imports with `isort`

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line

### Testing

* Write tests for all new features
* Ensure all tests pass before submitting PR
* Maintain or improve code coverage
* Use descriptive test names

## Project Structure

```
app/
├── api/           # API endpoints
├── core/          # Core functionality
├── models/        # Pydantic models
├── services/      # Business logic
└── utils/         # Utility functions
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_api/test_main.py
```

## Code Quality Tools

```bash
# Format code
black app/ tests/

# Sort imports
isort app/ tests/

# Check types
mypy app/

# Lint
flake8 app/ tests/
pylint app/
```

## Documentation

* Update README.md if needed
* Update API documentation
* Add docstrings to new code
* Update CHANGELOG.md

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉
