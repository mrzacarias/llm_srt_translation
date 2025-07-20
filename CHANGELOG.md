# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD workflow
- Automated release process
- Issue templates for bug reports and feature requests
- Security policy
- Contributing guidelines
- Modern Python packaging with pyproject.toml
- Code quality tools (black, isort, flake8, bandit)

### Changed
- Improved project structure for GitHub deployment
- Enhanced documentation

## [1.0.0] - 2024-01-XX

### Added
- Initial release of LLM SRT Translation Tool
- Support for Amazon Bedrock LLM models (Claude 3 Sonnet, Haiku, Opus, 3.5 Sonnet)
- Multi-language translation support (80+ languages)
- Automatic language detection
- Contextual translation using nearby subtitle entries
- Multiple encoding support (UTF-8, UTF-16, Latin-1, CP1252)
- Test mode for cost control
- Quality comparison tool
- Comprehensive logging and error handling
- Configurable parameters (context range, token limits, AWS regions)

### Features
- Command-line interface for easy usage
- Support for any language pair
- Maintains subtitle timing and formatting
- Built-in quality verification tools
- Cost-effective translation options
- Detailed progress reporting

### Technical Details
- Python 3.8+ compatibility
- AWS Bedrock integration
- Robust error handling
- Comprehensive documentation
- MIT License

---

## Version History

- **1.0.0**: Initial release with core translation functionality
- **Future versions**: Will follow semantic versioning for features, fixes, and breaking changes

## Migration Guide

### From Pre-1.0 versions
This is the initial release, so no migration is needed.

## Deprecation Policy

- Deprecated features will be marked with warnings for at least one major version
- Breaking changes will only occur in major version releases
- Security updates may be backported to previous versions

## Support

- **Current version**: 1.0.0
- **Supported Python versions**: 3.8, 3.9, 3.10, 3.11
- **Supported AWS regions**: All regions with Bedrock access
- **Supported models**: Claude 3 Sonnet, Haiku, Opus, 3.5 Sonnet

---

For detailed information about each release, see the [GitHub releases page](https://github.com/mrzacarias/llm_srt_translation/releases). 
