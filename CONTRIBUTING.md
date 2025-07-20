# Contributing to LLM SRT Translation

Thank you for your interest in contributing to the LLM SRT Translation project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Release Process](#release-process)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Provide environment information
- Attach relevant files (anonymized if needed)

### Suggesting Enhancements

- Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Describe the use case clearly
- Consider implementation complexity
- Check existing issues first

### Pull Requests

- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Make your changes
- Add tests if applicable
- Ensure all tests pass
- Update documentation
- Submit a pull request

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- AWS account with Bedrock access (for testing)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/mrzacarias/llm_srt_translation.git
   cd llm_srt_translation
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Configure AWS credentials**
   ```bash
   aws configure
   ```

5. **Run tests**
   ```bash
   pytest
   ```

## Code Style

We use several tools to maintain code quality:

### Formatting

- **Black**: Code formatting
  ```bash
  black .
  ```

- **isort**: Import sorting
  ```bash
  isort .
  ```

### Linting

- **flake8**: Style guide enforcement
  ```bash
  flake8 .
  ```

- **bandit**: Security linting
  ```bash
  bandit -r .
  ```

### Pre-commit Hooks

Install pre-commit hooks to automatically format and lint your code:

```bash
pip install pre-commit
pre-commit install
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=srt_translator --cov=compare_translations

# Run specific test file
pytest tests/test_srt_translator.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies (AWS, file I/O)
- Use fixtures for common setup

### Test Structure

```
tests/
├── test_srt_translator.py
├── test_compare_translations.py
├── conftest.py
└── fixtures/
    └── sample_srt_files/
```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following the style guidelines
   - Add tests for new functionality
   - Update documentation if needed

3. **Run quality checks**
   ```bash
   black .
   isort .
   flake8 .
   bandit -r .
   pytest
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a pull request**
   - Use a descriptive title
   - Fill out the PR template
   - Link related issues
   - Request reviews from maintainers

### Commit Message Format

We follow the [Conventional Commits](https://www.conventionalcommits.org/) format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

## Release Process

### For Maintainers

1. **Update version**
   - Update version in `pyproject.toml`
   - Update `__version__` in main modules

2. **Create a release branch**
   ```bash
   git checkout -b release/v1.0.0
   ```

3. **Update changelog**
   - Add release notes to `CHANGELOG.md`
   - Document breaking changes
   - List new features and bug fixes

4. **Create a tag**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

5. **GitHub Actions will automatically**
   - Run tests
   - Build the package
   - Create a GitHub release
   - Upload assets

## Project Structure

```
llm_srt_translation/
├── .github/                 # GitHub configuration
│   ├── workflows/          # GitHub Actions
│   └── ISSUE_TEMPLATE/     # Issue templates
├── tests/                  # Test files
├── srt_translator.py       # Main translation module
├── compare_translations.py # Comparison utility
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── pyproject.toml         # Modern Python packaging
├── README.md              # Project documentation
├── CONTRIBUTING.md        # This file
├── SECURITY.md            # Security policy
└── LICENSE                # MIT License
```

## Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check the README.md for usage examples

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing to LLM SRT Translation! 🚀 
