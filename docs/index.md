# LLM SRT Translation

A powerful, generic tool for translating SRT subtitle files between any language pair using Amazon Bedrock's LLM models.

## 🌟 Features

- ✅ **Multi-language Support**: Translate between any language pair
- ✅ **Automatic Language Detection**: Detects source and target languages automatically
- ✅ **Contextual Translation**: Uses nearby subtitle entries for better consistency
- ✅ **Multiple LLM Models**: Support for Claude 3 Sonnet, Haiku, Opus, and 3.5 Sonnet
- ✅ **Encoding Detection**: Automatically handles UTF-8, UTF-16, Latin-1, and CP1252
- ✅ **Test Mode**: Limit translations for testing and cost control
- ✅ **Quality Comparison**: Built-in tools to compare translation quality
- ✅ **Comprehensive Logging**: Detailed progress and error reporting
- ✅ **Configurable**: Customizable context range, token limits, and AWS regions

## 🚀 Quick Start

```bash
# Install the package
pip install llm-srt-translation

# Basic translation
srt-translator source.srt context.srt output.srt

# Test mode (first 10 entries)
srt-translator source.srt context.srt test_output.srt --max-entries 10
```

## 📖 Documentation

- [Installation Guide](installation.md) - How to install and configure the tool
- [Quick Start Guide](quickstart.md) - Get up and running in minutes
- [Usage Guide](usage.md) - Detailed usage instructions and examples
- [API Reference](api.md) - Complete API documentation
- [Examples](examples.md) - Real-world usage examples
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](contributing.md) for details.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- Amazon Bedrock for LLM access
- Anthropic for Claude models
- The open-source community for language detection libraries

---

**Happy Translating! 🌍✨** 
