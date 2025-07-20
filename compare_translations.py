#!/usr/bin/env python3
"""
Generic SRT Translation Comparison Tool

This tool compares source, translated, and reference SRT files to help verify translation quality.
"""

import sys
import re
import argparse
import logging
from typing import List, Dict
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def read_srt_file(file_path: str) -> List[Dict]:
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
    
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
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
            except (ValueError, IndexError):
                continue
    
    return subtitles

def clean_text(text: str) -> str:
    """Clean text by removing HTML tags and extra whitespace."""
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts."""
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1 & words2
    union = words1 | words2
    
    return len(intersection) / len(union) if union else 0.0

def compare_translations(source_file: str, translated_file: str, reference_file: str = None, 
                        max_entries: int = 10, show_similarity: bool = True):
    """Compare translations side by side."""
    
    print("🔍 COMPARING TRANSLATIONS")
    print("=" * 80)
    
    # Read files
    source_subs = read_srt_file(source_file)
    translated_subs = read_srt_file(translated_file)
    
    print(f"📊 File Statistics:")
    print(f"   Source: {len(source_subs)} entries")
    print(f"   Translated: {len(translated_subs)} entries")
    
    if reference_file:
        reference_subs = read_srt_file(reference_file)
        print(f"   Reference: {len(reference_subs)} entries")
    else:
        reference_subs = []
        print(f"   Reference: Not provided")
    
    print()
    
    # Limit for display
    max_entries = min(max_entries, len(source_subs), len(translated_subs))
    
    print(f"📋 Showing first {max_entries} entries:")
    print("=" * 80)
    
    total_similarity = 0.0
    entries_with_similarity = 0
    
    for i in range(max_entries):
        if i >= len(source_subs) or i >= len(translated_subs):
            break
            
        source_sub = source_subs[i]
        trans_sub = translated_subs[i]
        
        print(f"\n🎬 Entry {i+1} (Index: {source_sub['index']})")
        print(f"⏰ Timestamp: {source_sub['timestamp']}")
        print(f"📝 Source: {clean_text(source_sub['text'])}")
        print(f"🔄 Translated: {clean_text(trans_sub['text'])}")
        
        # Calculate similarity between source and translation
        source_text = clean_text(source_sub['text'])
        trans_text = clean_text(trans_sub['text'])
        similarity = calculate_similarity(source_text, trans_text)
        
        if show_similarity:
            print(f"📊 Similarity: {similarity:.2f} ({similarity*100:.1f}%)")
            total_similarity += similarity
            entries_with_similarity += 1
        
        # Try to find similar reference entry
        if reference_subs:
            source_text_lower = source_text.lower()
            best_match = None
            best_score = 0
            
            for ref_sub in reference_subs[:50]:  # Check first 50 reference entries
                ref_text = clean_text(ref_sub['text'])
                ref_text_lower = ref_text.lower()
                
                # Simple similarity check
                common_words = set(source_text_lower.split()) & set(ref_text_lower.split())
                if len(common_words) > best_score:
                    best_score = len(common_words)
                    best_match = ref_sub
            
            if best_match and best_score > 0:
                print(f"📖 Reference: {clean_text(best_match['text'])}")
                print(f"   (Similarity score: {best_score} common words)")
        
        print("-" * 60)
    
    # Print summary statistics
    if show_similarity and entries_with_similarity > 0:
        avg_similarity = total_similarity / entries_with_similarity
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   Average similarity: {avg_similarity:.2f} ({avg_similarity*100:.1f}%)")
        print(f"   Entries compared: {entries_with_similarity}")
        
        if avg_similarity < 0.3:
            print("   ⚠️  Low similarity - translations may be too different from source")
        elif avg_similarity > 0.8:
            print("   ⚠️  High similarity - translations may be too similar to source")
        else:
            print("   ✅ Good similarity range")

def main():
    parser = argparse.ArgumentParser(
        description="Compare SRT translation files to verify quality",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare source and translated files
  python compare_translations.py source.srt translated.srt
  
  # Compare with reference file
  python compare_translations.py source.srt translated.srt reference.srt
  
  # Show more entries
  python compare_translations.py source.srt translated.srt --max-entries 20
  
  # Hide similarity scores
  python compare_translations.py source.srt translated.srt --no-similarity
        """
    )
    
    parser.add_argument('source_file', help='Path to source SRT file')
    parser.add_argument('translated_file', help='Path to translated SRT file')
    parser.add_argument('reference_file', nargs='?', help='Path to reference SRT file (optional)')
    
    parser.add_argument('--max-entries', type=int, default=10, 
                       help='Maximum entries to compare (default: 10)')
    parser.add_argument('--no-similarity', action='store_true', 
                       help='Hide similarity scores')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Validate input files
    for file_path in [args.source_file, args.translated_file]:
        if not Path(file_path).exists():
            logger.error(f"File not found: {file_path}")
            sys.exit(1)
    
    if args.reference_file and not Path(args.reference_file).exists():
        logger.error(f"Reference file not found: {args.reference_file}")
        sys.exit(1)
    
    try:
        compare_translations(
            source_file=args.source_file,
            translated_file=args.translated_file,
            reference_file=args.reference_file,
            max_entries=args.max_entries,
            show_similarity=not args.no_similarity
        )
    except Exception as e:
        logger.error(f"Comparison failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
