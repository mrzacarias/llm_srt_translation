# LLM SRT Translation Tool

A powerful, generic tool for translating SRT subtitle files between any language pair using Amazon Bedrock's LLM models. This tool automatically detects languages, provides contextual translation guidance, and maintains subtitle timing.

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

### Prerequisites

1. **AWS Account** with Bedrock access
2. **AWS Credentials** configured
3. **Python 3.7+** installed

### Installation

```bash
# Clone or download the tool
cd llm_srt_translation

# Install dependencies
pip install -r requirements.txt

# Configure AWS credentials
aws configure
```

### Basic Usage

```bash
# Translate with auto language detection
python srt_translator.py source.srt context.srt output.srt

# Test mode (first 10 entries)
python srt_translator.py source.srt context.srt test_output.srt --max-entries 10

# Compare results
python compare_translations.py source.srt test_output.srt context.srt
```

## 📖 Detailed Usage

### Command Line Options

```bash
python srt_translator.py [OPTIONS] source_srt context_srt output_srt
```

#### Required Arguments
- `source_srt`: Path to source SRT file to translate
- `context_srt`: Path to context SRT file for reference
- `output_srt`: Path for output translated SRT file

#### Optional Arguments
- `--source-lang`: Source language code (auto-detected if not specified)
- `--target-lang`: Target language code (auto-detected if not specified)
- `--model`: Bedrock model to use (`claude-3-sonnet`, `claude-3-haiku`, `claude-3-opus`, `claude-3-5-sonnet`)
- `--region`: AWS region for Bedrock (default: `us-east-1`)
- `--max-entries`: Maximum entries to translate (for testing)
- `--context-range`: Number of context entries to include (default: 20)
- `--max-tokens`: Maximum tokens for LLM response (default: 1000)
- `--verbose`: Enable verbose logging

### Examples

#### Basic Translation
```bash
# English to Portuguese
python srt_translator.py english.srt portuguese_context.srt translated.srt

# Spanish to French
python srt_translator.py spanish.srt french_context.srt translated.srt
```

#### Explicit Language Specification
```bash
python srt_translator.py source.srt context.srt output.srt --source-lang en --target-lang pt
```

#### Test Mode
```bash
# Test with 5 entries
python srt_translator.py source.srt context.srt test.srt --max-entries 5

# Use faster/cheaper model for testing
python srt_translator.py source.srt context.srt test.srt --max-entries 10 --model claude-3-haiku
```

#### Custom Configuration
```bash
# Use different AWS region
python srt_translator.py source.srt context.srt output.srt --region eu-west-1

# Increase context range for better consistency
python srt_translator.py source.srt context.srt output.srt --context-range 30

# Use higher quality model
python srt_translator.py source.srt context.srt output.srt --model claude-3-opus
```

## 🔍 Quality Verification

### Using the Comparison Tool

```bash
# Basic comparison
python compare_translations.py source.srt translated.srt

# Compare with reference file
python compare_translations.py source.srt translated.srt reference.srt

# Show more entries
python compare_translations.py source.srt translated.srt --max-entries 20

# Hide similarity scores
python compare_translations.py source.srt translated.srt --no-similarity
```

### Understanding Output

The comparison tool provides:
- **File Statistics**: Entry counts for all files
- **Side-by-side Comparison**: Source vs translated text
- **Similarity Scores**: Jaccard similarity between source and translation
- **Reference Matching**: Finds similar entries in reference file
- **Quality Assessment**: Warnings for very high/low similarity

## 🌍 Supported Languages

The tool supports 80+ languages including:

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Portuguese | `pt` |
| Spanish | `es` | French | `fr` |
| German | `de` | Italian | `it` |
| Russian | `ru` | Japanese | `ja` |
| Korean | `ko` | Chinese | `zh` |
| Arabic | `ar` | Hindi | `hi` |
| Dutch | `nl` | Swedish | `sv` |
| Norwegian | `no` | Danish | `da` |
| Finnish | `fi` | Polish | `pl` |
| Turkish | `tr` | Hebrew | `he` |
| Thai | `th` | Vietnamese | `vi` |
| Indonesian | `id` | Malay | `ms` |
| Persian | `fa` | Urdu | `ur` |
| Bengali | `bn` | Tamil | `ta` |
| Telugu | `te` | Malayalam | `ml` |
| Kannada | `kn` | Gujarati | `gu` |
| Punjabi | `pa` | Marathi | `mr` |
| Nepali | `ne` | Sinhala | `si` |
| Burmese | `my` | Khmer | `km` |
| Lao | `lo` | Georgian | `ka` |
| Amharic | `am` | Swahili | `sw` |
| Zulu | `zu` | Afrikaans | `af` |
| Croatian | `hr` | Czech | `cs` |
| Slovak | `sk` | Hungarian | `hu` |
| Romanian | `ro` | Bulgarian | `bg` |
| Ukrainian | `uk` | Belarusian | `be` |
| Slovenian | `sl` | Estonian | `et` |
| Latvian | `lv` | Lithuanian | `lt` |
| Maltese | `mt` | Irish | `ga` |
| Welsh | `cy` | Icelandic | `is` |
| Faroese | `fo` | Albanian | `sq` |
| Macedonian | `mk` | Serbian | `sr` |
| Bosnian | `bs` | Montenegrin | `me` |

## 🤖 Available Models

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| `claude-3-haiku` | Fast | Low | Good | Testing, quick translations |
| `claude-3-sonnet` | Medium | Medium | Very Good | Production, balanced |
| `claude-3-opus` | Slow | High | Excellent | High-quality translations |
| `claude-3-5-sonnet` | Medium | Medium | Very Good | Latest features |

## 💰 Cost Considerations

- **Claude 3 Haiku**: ~$0.25 per 1M input tokens
- **Claude 3 Sonnet**: ~$3 per 1M input tokens  
- **Claude 3 Opus**: ~$15 per 1M input tokens
- **Claude 3.5 Sonnet**: ~$3 per 1M input tokens

For a typical movie (1000+ subtitles):
- **Haiku**: $1-3
- **Sonnet**: $5-15
- **Opus**: $25-75

## 🔧 Configuration

### AWS Setup

1. **Install AWS CLI**:
   ```bash
   pip install awscli
   ```

2. **Configure credentials**:
   ```bash
   aws configure
   ```

3. **Enable Bedrock access** in your AWS account

### Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

## 📁 File Formats

### Input Requirements

- **Source SRT**: File to translate (any language)
- **Context SRT**: Reference file in target language
- **Encoding**: UTF-8, UTF-16, Latin-1, or CP1252

### Output Format

- **Encoding**: UTF-8
- **Format**: Standard SRT with preserved timestamps
- **Structure**: Index, timestamp, text

## 🛠️ Troubleshooting

### Common Issues

#### AWS Credentials Error
```
botocore.exceptions.NoCredentialsError
```
**Solution**: Configure AWS credentials using `aws configure`

#### Bedrock Access Denied
```
botocore.exceptions.ClientError: An error occurred (AccessDeniedException)
```
**Solution**: Enable Bedrock access in your AWS account

#### Model Not Found
```
botocore.exceptions.ClientError: An error occurred (ValidationException)
```
**Solution**: Check model availability in your AWS region

#### File Encoding Issues
**Solution**: Tool automatically tries multiple encodings

#### Language Detection Fails
**Solution**: Specify languages explicitly with `--source-lang` and `--target-lang`

### Debug Mode

Enable verbose logging for troubleshooting:
```bash
python srt_translator.py source.srt context.srt output.srt --verbose
```

## 📊 Performance Tips

1. **Use Test Mode**: Always test with `--max-entries 10` first
2. **Choose Right Model**: Use Haiku for testing, Sonnet for production
3. **Optimize Context**: Adjust `--context-range` based on content type
4. **Batch Processing**: Process multiple files in sequence
5. **Monitor Costs**: Use AWS Cost Explorer to track usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Amazon Bedrock for LLM access
- Anthropic for Claude models
- The open-source community for language detection libraries

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Enable verbose logging for debugging
4. Open an issue on GitHub

---

**Happy Translating! 🌍✨** 
