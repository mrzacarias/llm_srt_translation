"""
Tests for the srt_translator module.
"""

import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
import sys

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from srt_translator import (
    detect_language,
    parse_srt_file,
    write_srt_file,
    translate_subtitle,
    main
)


class TestLanguageDetection:
    """Test language detection functionality."""
    
    def test_detect_language_english(self):
        """Test detecting English language."""
        text = "Hello, this is a test subtitle."
        result = detect_language(text)
        assert result == "en"
    
    def test_detect_language_portuguese(self):
        """Test detecting Portuguese language."""
        text = "Olá, este é um subtítulo de teste."
        result = detect_language(text)
        assert result == "pt"
    
    def test_detect_language_spanish(self):
        """Test detecting Spanish language."""
        text = "Hola, este es un subtítulo de prueba."
        result = detect_language(text)
        assert result == "es"


class TestSRTParsing:
    """Test SRT file parsing functionality."""
    
    def test_parse_srt_file_valid(self, sample_srt_file):
        """Test parsing a valid SRT file."""
        entries = parse_srt_file(sample_srt_file)
        assert len(entries) == 3
        assert entries[0]['index'] == 1
        assert entries[0]['text'] == "Hello, this is a test subtitle."
        assert entries[0]['start_time'] == "00:00:01,000"
        assert entries[0]['end_time'] == "00:00:04,000"
    
    def test_parse_srt_file_empty(self):
        """Test parsing an empty SRT file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False) as f:
            f.write("")
            temp_file = f.name
        
        try:
            entries = parse_srt_file(temp_file)
            assert entries == []
        finally:
            os.unlink(temp_file)
    
    def test_parse_srt_file_nonexistent(self):
        """Test parsing a nonexistent SRT file."""
        with pytest.raises(FileNotFoundError):
            parse_srt_file("nonexistent_file.srt")


class TestSRTWriting:
    """Test SRT file writing functionality."""
    
    def test_write_srt_file(self, sample_srt_entries, temp_output_file):
        """Test writing SRT entries to a file."""
        write_srt_file(sample_srt_entries, temp_output_file)
        
        # Verify the file was created and contains expected content
        assert os.path.exists(temp_output_file)
        
        with open(temp_output_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "1" in content
        assert "Hello, this is a test subtitle." in content
        assert "00:00:01,000 --> 00:00:04,000" in content


class TestTranslation:
    """Test translation functionality."""
    
    @patch('boto3.client')
    def test_translate_subtitle_success(self, mock_boto_client, mock_aws_credentials):
        """Test successful subtitle translation."""
        # Mock the Bedrock client response
        mock_bedrock = Mock()
        mock_bedrock.invoke_model.return_value = {
            'body': Mock(
                read=lambda: b'{"completion": "Ola, este e um subtitulo de teste."}'
            )
        }
        mock_boto_client.return_value = mock_bedrock
        
        text = "Hello, this is a test subtitle."
        context_entries = [{"text": "Context text"}]
        
        result = translate_subtitle(text, context_entries, "en", "pt", "claude-3-sonnet", "us-east-1")
        
        assert result == "Olá, este é um subtítulo de teste."
        mock_bedrock.invoke_model.assert_called_once()
    
    @patch('boto3.client')
    def test_translate_subtitle_aws_error(self, mock_boto_client, mock_aws_credentials):
        """Test translation with AWS error."""
        # Mock AWS error
        mock_bedrock = Mock()
        mock_bedrock.invoke_model.side_effect = Exception("AWS Error")
        mock_boto_client.return_value = mock_bedrock
        
        text = "Hello, this is a test subtitle."
        context_entries = [{"text": "Context text"}]
        
        with pytest.raises(Exception):
            translate_subtitle(text, context_entries, "en", "pt", "claude-3-sonnet", "us-east-1")


class TestMainFunction:
    """Test the main function."""
    
    @patch('srt_translator.translate_subtitle')
    @patch('srt_translator.parse_srt_file')
    @patch('srt_translator.write_srt_file')
    def test_main_success(self, mock_write, mock_parse, mock_translate, 
                         sample_srt_file, sample_context_srt_file, temp_output_file):
        """Test successful main function execution."""
        # Mock the parse function to return sample entries
        mock_parse.side_effect = [
            [{"index": 1, "start_time": "00:00:01,000", "end_time": "00:00:04,000", "text": "Hello"}],
            [{"index": 1, "start_time": "00:00:01,000", "end_time": "00:00:04,000", "text": "Olá"}]
        ]
        
        # Mock the translate function
        mock_translate.return_value = "Olá"
        
        # Test with minimal arguments
        with patch('sys.argv', ['srt_translator.py', sample_srt_file, sample_context_srt_file, temp_output_file]):
            main()
        
        # Verify functions were called
        assert mock_parse.call_count == 2  # Called for both source and context files
        assert mock_translate.called
        assert mock_write.called


class TestIntegration:
    """Integration tests."""
    
    def test_end_to_end_workflow(self, sample_srt_file, sample_context_srt_file, temp_output_file):
        """Test the complete workflow from file reading to writing."""
        # This test would require actual AWS credentials and would make real API calls
        # For now, we'll just verify the files can be parsed
        source_entries = parse_srt_file(sample_srt_file)
        context_entries = parse_srt_file(sample_context_srt_file)
        
        assert len(source_entries) == 3
        assert len(context_entries) == 3
        assert source_entries[0]['text'] == "Hello, this is a test subtitle."
        assert context_entries[0]['text'] == "Olá, este é um subtítulo de teste."


if __name__ == "__main__":
    pytest.main([__file__]) 
