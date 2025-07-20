#!/usr/bin/env python3
"""
Generic SRT Translation Tool using Amazon Bedrock

This tool translates SRT subtitle files between any language pair using Amazon Bedrock's LLM models.
It automatically detects source and target languages and provides contextual translation guidance.
"""

import boto3
import json
import re
import sys
import os
import argparse
from typing import List, Dict, Tuple, Optional
import logging
from datetime import datetime
from pathlib import Path

# Language detection imports
try:
    from langdetect import detect, DetectorFactory
    from langdetect.lang_detect_exception import LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    logging.warning("langdetect not available. Language detection will be disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set seed for consistent language detection
if LANGDETECT_AVAILABLE:
    DetectorFactory.seed = 0

class LanguageDetector:
    """Detect language of text content."""
    
    @staticmethod
    def detect_language(text: str) -> str:
        """Detect language from text sample."""
        if not LANGDETECT_AVAILABLE:
            return "unknown"
        
        try:
            # Clean text for better detection
            clean_text = re.sub(r'[^\w\s]', '', text)
            if len(clean_text.strip()) < 10:
                return "unknown"
            
            return detect(clean_text)
        except LangDetectException:
            return "unknown"
    
    @staticmethod
    def get_language_name(code: str) -> str:
        """Get language name from ISO code."""
        language_map = {
            'en': 'English',
            'pt': 'Portuguese',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'ru': 'Russian',
            'ja': 'Japanese',
            'ko': 'Korean',
            'zh': 'Chinese',
            'ar': 'Arabic',
            'hi': 'Hindi',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'no': 'Norwegian',
            'da': 'Danish',
            'fi': 'Finnish',
            'pl': 'Polish',
            'tr': 'Turkish',
            'he': 'Hebrew',
            'th': 'Thai',
            'vi': 'Vietnamese',
            'id': 'Indonesian',
            'ms': 'Malay',
            'fa': 'Persian',
            'ur': 'Urdu',
            'bn': 'Bengali',
            'ta': 'Tamil',
            'te': 'Telugu',
            'ml': 'Malayalam',
            'kn': 'Kannada',
            'gu': 'Gujarati',
            'pa': 'Punjabi',
            'mr': 'Marathi',
            'ne': 'Nepali',
            'si': 'Sinhala',
            'my': 'Burmese',
            'km': 'Khmer',
            'lo': 'Lao',
            'ka': 'Georgian',
            'am': 'Amharic',
            'sw': 'Swahili',
            'zu': 'Zulu',
            'af': 'Afrikaans',
            'hr': 'Croatian',
            'cs': 'Czech',
            'sk': 'Slovak',
            'hu': 'Hungarian',
            'ro': 'Romanian',
            'bg': 'Bulgarian',
            'uk': 'Ukrainian',
            'be': 'Belarusian',
            'sl': 'Slovenian',
            'et': 'Estonian',
            'lv': 'Latvian',
            'lt': 'Lithuanian',
            'mt': 'Maltese',
            'ga': 'Irish',
            'cy': 'Welsh',
            'is': 'Icelandic',
            'fo': 'Faroese',
            'sq': 'Albanian',
            'mk': 'Macedonian',
            'sr': 'Serbian',
            'bs': 'Bosnian',
            'me': 'Montenegrin',
            'unknown': 'Unknown'
        }
        return language_map.get(code, code.upper())

class SRTTranslator:
    """Generic SRT translator using Amazon Bedrock."""
    
    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0", 
                 region: str = "us-east-1", max_tokens: int = 1000):
        """
        Initialize the SRT translator.
        
        Args:
            model_id: Bedrock model ID to use
            region: AWS region for Bedrock
            max_tokens: Maximum tokens for response
        """
        self.model_id = model_id
        self.max_tokens = max_tokens
        self.bedrock_runtime = boto3.client(
            service_name='bedrock-runtime',
            region_name=region
        )
        
        # Available models for reference
        self.available_models = {
            "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
            "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0", 
            "claude-3-opus": "anthropic.claude-3-opus-20240229-v1:0",
            "claude-3-5-sonnet": "anthropic.claude-3-5-sonnet-20241022-v2:0"
        }
    
    def read_srt_file(self, file_path: str) -> List[Dict]:
        """Read and parse an SRT file with automatic encoding detection."""
        subtitles = []
        
        # Try different encodings
        encodings = ['utf-8', 'utf-16', 'latin-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    content = file.read()
                logger.debug(f"Successfully read {file_path} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            raise ValueError(f"Could not read {file_path} with any supported encoding")
        
        if len(content.strip()) == 0:
            logger.error(f"File {file_path} appears to be empty")
            return []
        
        # Split by double newlines to separate subtitle blocks
        blocks = content.strip().split('\n\n')
        logger.debug(f"Found {len(blocks)} blocks in {file_path}")
        
        for i, block in enumerate(blocks):
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    if lines[0].isdigit():
                        subtitle = {
                            'index': int(lines[0]),
                            'timestamp': lines[1],
                            'text': '\n'.join(lines[2:])
                        }
                        subtitles.append(subtitle)
                    else:
                        logger.debug(f"Skipping block that doesn't start with a number: {lines[0]}")
                except (ValueError, IndexError) as e:
                    logger.warning(f"Skipping malformed subtitle block: {block[:100]}... Error: {e}")
                    continue
        
        logger.info(f"Loaded {len(subtitles)} subtitle entries from {file_path}")
        return subtitles
    
    def detect_srt_language(self, file_path: str) -> str:
        """Detect the language of an SRT file."""
        subtitles = self.read_srt_file(file_path)
        if not subtitles:
            return "unknown"
        
        # Sample text from first few subtitles
        sample_texts = []
        for subtitle in subtitles[:10]:  # Use first 10 subtitles
            text = subtitle['text'].strip()
            text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
            if text and len(text) > 5:
                sample_texts.append(text)
        
        if not sample_texts:
            return "unknown"
        
        # Combine sample texts and detect language
        combined_text = " ".join(sample_texts[:5])  # Use first 5 samples
        language_code = LanguageDetector.detect_language(combined_text)
        language_name = LanguageDetector.get_language_name(language_code)
        
        logger.info(f"Detected language for {file_path}: {language_name} ({language_code})")
        return language_code
    
    def extract_translation_guide(self, context_srt_path: str, max_entries: int = 100) -> str:
        """Extract text content from context SRT file."""
        subtitles = self.read_srt_file(context_srt_path)
        
        context_texts = []
        for subtitle in subtitles[:max_entries]:
            text = subtitle['text'].strip()
            text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
            if text:
                context_texts.append(text)
        
        guide_text = "\n".join(context_texts)
        logger.info(f"Extracted {len(context_texts)} context text entries")
        return guide_text
    
    def get_contextual_translation_guide(self, context_srt_path: str, current_index: int, 
                                       context_range: int = 20) -> str:
        """Get contextual translation guide with nearby entries."""
        subtitles = self.read_srt_file(context_srt_path)
        
        if not subtitles:
            logger.warning("No context subtitles found")
            return ""
        
        # Calculate start and end indices for context
        start_idx = max(0, current_index - context_range)
        end_idx = min(len(subtitles), current_index + context_range + 1)
        
        # Extract contextual text
        contextual_texts = []
        for i in range(start_idx, end_idx):
            subtitle = subtitles[i]
            text = subtitle['text'].strip()
            text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags
            if text:
                if i < current_index:
                    contextual_texts.append(f"[Previous {current_index - i}]: {text}")
                elif i == current_index:
                    contextual_texts.append(f"[Current]: {text}")
                else:
                    contextual_texts.append(f"[Next {i - current_index}]: {text}")
        
        guide_text = "\n".join(contextual_texts)
        logger.debug(f"Extracted contextual guide for index {current_index}: {len(contextual_texts)} entries")
        return guide_text
    
    def create_translation_prompt(self, source_text: str, source_lang: str, target_lang: str, 
                                translation_guide: str, contextual_guide: str = "") -> str:
        """Create a translation prompt for the LLM."""
        
        source_lang_name = LanguageDetector.get_language_name(source_lang)
        target_lang_name = LanguageDetector.get_language_name(target_lang)
        
        prompt = f"""You are a professional translator specializing in {source_lang_name} to {target_lang_name} translation for subtitles.

IMPORTANT CONTEXT - TRANSLATION GUIDE:
Here are some professional {target_lang_name} translations from the same content to use as reference for style, tone, and terminology:

{translation_guide}

"""

        if contextual_guide:
            prompt += f"""CONTEXTUAL REFERENCE - NEARBY ENTRIES:
Here are {target_lang_name} translations from nearby subtitle entries to help maintain context and consistency:

{contextual_guide}

"""

        prompt += f"""TASK:
Translate the following {source_lang_name} subtitle text to {target_lang_name}. The translation should:
1. Be natural and fluent {target_lang_name}
2. Match the style and tone of the reference translations above
3. Maintain the same meaning and intent as the original
4. Be appropriate for subtitle format (concise but clear)
5. Use proper {target_lang_name} conventions
6. Be consistent with the contextual nearby entries provided

CRITICAL: Return ONLY the {target_lang_name} translation. Do not include any explanations, comments, or additional text.

{source_lang_name.upper()} TEXT TO TRANSLATE:
{source_text}

{target_lang_name.upper()} TRANSLATION:"""

        return prompt
    
    def translate_with_bedrock(self, source_text: str, source_lang: str, target_lang: str, 
                             translation_guide: str, contextual_guide: str = "") -> str:
        """Translate text using Amazon Bedrock."""
        
        prompt = self.create_translation_prompt(source_text, source_lang, target_lang, 
                                              translation_guide, contextual_guide)
        
        try:
            response = self.bedrock_runtime.invoke_model(
                modelId=self.model_id,
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": self.max_tokens,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            response_body = json.loads(response.get('body').read())
            translated_text = response_body['content'][0]['text'].strip()
            
            # Clean up the response - remove explanations and keep only the translation
            target_lang_name = LanguageDetector.get_language_name(target_lang)
            translated_text = re.sub(f'^{target_lang_name.upper()} TRANSLATION:\\s*', '', translated_text)
            
            # Remove any explanations that might follow the translation
            explanation_patterns = [
                r'\n\n.*?Esta tradução.*',
                r'\n\n.*?This translation.*',
                r'\n\n.*?A tradução.*',
                r'\n\n.*?The translation.*',
                r'\n\n.*?pode ser traduzido.*',
                r'\n\n.*?can be translated.*',
                r'\n\n.*?está de acordo.*',
                r'\n\n.*?is in accordance.*',
                r'\n\n.*?mantendo o mesmo.*',
                r'\n\n.*?maintaining the same.*',
                r'\n\n.*?Além disso.*',
                r'\n\n.*?Additionally.*',
                r'\n\n.*?consistente com.*',
                r'\n\n.*?consistent with.*',
                r'\n\n.*?La traduction.*',
                r'\n\n.*?La traducción.*',
                r'\n\n.*?Die Übersetzung.*',
                r'\n\n.*?La traduzione.*',
                r'\n\n.*?Перевод.*',
                r'\n\n.*?翻訳.*',
                r'\n\n.*?번역.*',
                r'\n\n.*?翻译.*',
                r'\n\n.*?الترجمة.*',
                r'\n\n.*?अनुवाद.*'
            ]
            
            for pattern in explanation_patterns:
                translated_text = re.sub(pattern, '', translated_text, flags=re.IGNORECASE | re.DOTALL)
            
            # Clean up any remaining whitespace and newlines
            translated_text = translated_text.strip()
            
            # If the response is empty after cleaning, return the original text
            if not translated_text:
                logger.warning("Translation result was empty after cleaning, using original text")
                return source_text
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            return source_text  # Return original text if translation fails
    
    def translate_srt_file(self, source_srt_path: str, context_srt_path: str, output_path: str, 
                          source_lang: str = None, target_lang: str = None, 
                          max_entries: int = None, context_range: int = 20) -> Dict:
        """
        Translate an SRT file.
        
        Args:
            source_srt_path: Path to source SRT file
            context_srt_path: Path to context SRT file for reference
            output_path: Path for output translated SRT file
            source_lang: Source language code (auto-detected if None)
            target_lang: Target language code (auto-detected if None)
            max_entries: Maximum entries to translate (None = all)
            context_range: Number of context entries to include
            
        Returns:
            Dictionary with translation statistics
        """
        logger.info("Starting SRT translation process...")
        
        # Detect languages if not provided
        if source_lang is None:
            source_lang = self.detect_srt_language(source_srt_path)
        if target_lang is None:
            target_lang = self.detect_srt_language(context_srt_path)
        
        source_lang_name = LanguageDetector.get_language_name(source_lang)
        target_lang_name = LanguageDetector.get_language_name(target_lang)
        
        logger.info(f"Translating from {source_lang_name} to {target_lang_name}")
        
        # Load source subtitles
        source_subtitles = self.read_srt_file(source_srt_path)
        
        # Limit entries for testing if specified
        if max_entries is not None:
            source_subtitles = source_subtitles[:max_entries]
            logger.info(f"TEST MODE: Limiting translation to first {max_entries} entries")
        
        # Extract translation guide
        translation_guide = self.extract_translation_guide(context_srt_path)
        
        # Translate each subtitle
        translated_subtitles = []
        successful_translations = 0
        failed_translations = 0
        
        for i, subtitle in enumerate(source_subtitles):
            logger.info(f"Translating subtitle {i+1}/{len(source_subtitles)}")
            
            # Get contextual guide for this subtitle
            contextual_guide = self.get_contextual_translation_guide(context_srt_path, i, context_range)
            
            # Clean the source text
            source_text = subtitle['text'].strip()
            source_text = re.sub(r'<[^>]+>', '', source_text)  # Remove HTML tags
            
            if source_text:
                # Translate the text
                translated_text = self.translate_with_bedrock(
                    source_text, source_lang, target_lang, translation_guide, contextual_guide
                )
                
                # Check if translation was successful (not same as original)
                if translated_text != source_text:
                    successful_translations += 1
                else:
                    failed_translations += 1
                
                # Create translated subtitle entry
                translated_subtitle = {
                    'index': subtitle['index'],
                    'timestamp': subtitle['timestamp'],
                    'text': translated_text
                }
                translated_subtitles.append(translated_subtitle)
            else:
                # Keep empty subtitles as is
                translated_subtitles.append(subtitle)
        
        # Write the translated SRT file
        self.write_srt_file(translated_subtitles, output_path)
        
        # Return statistics
        stats = {
            'total_entries': len(source_subtitles),
            'successful_translations': successful_translations,
            'failed_translations': failed_translations,
            'success_rate': (successful_translations / len(source_subtitles)) * 100 if source_subtitles else 0,
            'source_language': source_lang_name,
            'target_language': target_lang_name,
            'output_file': output_path
        }
        
        logger.info(f"Translation completed. Success rate: {stats['success_rate']:.1f}%")
        return stats
    
    def write_srt_file(self, subtitles: List[Dict], output_path: str):
        """Write subtitles to an SRT file."""
        with open(output_path, 'w', encoding='utf-8') as file:
            for subtitle in subtitles:
                file.write(f"{subtitle['index']}\n")
                file.write(f"{subtitle['timestamp']}\n")
                file.write(f"{subtitle['text']}\n\n")

def main():
    """Main function to run the SRT translation."""
    parser = argparse.ArgumentParser(
        description="Translate SRT subtitle files using Amazon Bedrock LLM models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic translation with auto language detection
  python srt_translator.py source.srt context.srt output.srt
  
  # Specify languages explicitly
  python srt_translator.py source.srt context.srt output.srt --source-lang en --target-lang pt
  
  # Test mode (translate only first 10 entries)
  python srt_translator.py source.srt context.srt test_output.srt --max-entries 10
  
  # Use different model
  python srt_translator.py source.srt context.srt output.srt --model claude-3-haiku
  
  # Custom AWS region
  python srt_translator.py source.srt context.srt output.srt --region eu-west-1
        """
    )
    
    parser.add_argument('source_srt', help='Path to source SRT file to translate')
    parser.add_argument('context_srt', help='Path to context SRT file for reference')
    parser.add_argument('output_srt', help='Path for output translated SRT file')
    
    parser.add_argument('--source-lang', help='Source language code (auto-detected if not specified)')
    parser.add_argument('--target-lang', help='Target language code (auto-detected if not specified)')
    parser.add_argument('--model', default='claude-3-sonnet', 
                       choices=['claude-3-sonnet', 'claude-3-haiku', 'claude-3-opus', 'claude-3-5-sonnet'],
                       help='Bedrock model to use for translation')
    parser.add_argument('--region', default='us-east-1', help='AWS region for Bedrock')
    parser.add_argument('--max-entries', type=int, help='Maximum entries to translate (for testing)')
    parser.add_argument('--context-range', type=int, default=20, 
                       help='Number of context entries to include (default: 20)')
    parser.add_argument('--max-tokens', type=int, default=1000, 
                       help='Maximum tokens for LLM response (default: 1000)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input files
    for file_path in [args.source_srt, args.context_srt]:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            sys.exit(1)
    
    try:
        # Initialize translator
        translator = SRTTranslator(
            model_id=SRTTranslator().available_models[args.model],
            region=args.region,
            max_tokens=args.max_tokens
        )
        
        # Perform translation
        stats = translator.translate_srt_file(
            source_srt_path=args.source_srt,
            context_srt_path=args.context_srt,
            output_path=args.output_srt,
            source_lang=args.source_lang,
            target_lang=args.target_lang,
            max_entries=args.max_entries,
            context_range=args.context_range
        )
        
        # Print results
        print(f"\n✅ Translation completed successfully!")
        print(f"📁 Output file: {stats['output_file']}")
        print(f"📊 Statistics:")
        print(f"   Total entries: {stats['total_entries']}")
        print(f"   Successful translations: {stats['successful_translations']}")
        print(f"   Failed translations: {stats['failed_translations']}")
        print(f"   Success rate: {stats['success_rate']:.1f}%")
        print(f"   Source language: {stats['source_language']}")
        print(f"   Target language: {stats['target_language']}")
        
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
