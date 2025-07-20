#!/usr/bin/env python3
"""
Example script demonstrating how to use the SRT translator programmatically.
"""

from srt_translator import SRTTranslator, LanguageDetector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Example usage of the SRT translator."""
    
    # Initialize translator
    translator = SRTTranslator(
        model_id="anthropic.claude-3-sonnet-20240229-v1:0",
        region="us-east-1",
        max_tokens=1000
    )
    
    # Example 1: Basic translation with auto language detection
    print("🌍 Example 1: Basic translation with auto language detection")
    print("=" * 60)
    
    try:
        stats = translator.translate_srt_file(
            source_srt_path="example_source.srt",
            context_srt_path="example_context.srt", 
            output_path="example_output.srt",
            max_entries=5  # Test with 5 entries
        )
        
        print(f"✅ Translation completed!")
        print(f"📊 Statistics: {stats}")
        
    except FileNotFoundError:
        print("⚠️  Example files not found. This is expected if you haven't created them yet.")
        print("   Create example_source.srt and example_context.srt to test this example.")
    
    # Example 2: Language detection
    print("\n🔍 Example 2: Language detection")
    print("=" * 60)
    
    # Sample texts for language detection
    sample_texts = [
        "Hello, how are you today?",
        "Hola, ¿cómo estás hoy?",
        "Bonjour, comment allez-vous aujourd'hui?",
        "Olá, como você está hoje?",
        "Hallo, wie geht es dir heute?"
    ]
    
    for text in sample_texts:
        lang_code = LanguageDetector.detect_language(text)
        lang_name = LanguageDetector.get_language_name(lang_code)
        print(f"Text: {text[:30]}... → {lang_name} ({lang_code})")
    
    # Example 3: Custom configuration
    print("\n⚙️  Example 3: Custom configuration")
    print("=" * 60)
    
    # Show available models
    translator_instance = SRTTranslator()
    print("Available models:")
    for model_name, model_id in translator_instance.available_models.items():
        print(f"  - {model_name}: {model_id}")
    
    # Example 4: Translation with explicit languages
    print("\n🎯 Example 4: Translation with explicit languages")
    print("=" * 60)
    
    try:
        stats = translator.translate_srt_file(
            source_srt_path="example_source.srt",
            context_srt_path="example_context.srt",
            output_path="example_output_explicit.srt",
            source_lang="en",  # Explicitly specify English
            target_lang="pt",  # Explicitly specify Portuguese
            max_entries=3,     # Test with 3 entries
            context_range=10   # Use 10 context entries
        )
        
        print(f"✅ Translation with explicit languages completed!")
        print(f"📊 Statistics: {stats}")
        
    except FileNotFoundError:
        print("⚠️  Example files not found. This is expected if you haven't created them yet.")
    
    print("\n🎉 Examples completed!")
    print("\nTo use this tool with your own files:")
    print("1. Prepare your source SRT file")
    print("2. Prepare a context SRT file in the target language")
    print("3. Run: python srt_translator.py source.srt context.srt output.srt")
    print("4. Use --max-entries 10 for testing first")

if __name__ == "__main__":
    main() 
