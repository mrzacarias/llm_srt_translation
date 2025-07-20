"""
Pytest configuration and fixtures for LLM SRT Translation tests.
"""

import pytest
import tempfile
import os
from pathlib import Path


@pytest.fixture
def sample_srt_file():
    """Create a sample SRT file for testing."""
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Hello, this is a test subtitle.

2
00:00:05,000 --> 00:00:08,000
This is the second subtitle entry.

3
00:00:09,000 --> 00:00:12,000
And this is the third one."""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as f:
        f.write(srt_content)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    os.unlink(temp_file)


@pytest.fixture
def sample_context_srt_file():
    """Create a sample context SRT file for testing."""
    srt_content = """1
00:00:01,000 --> 00:00:04,000
Olá, este é um subtítulo de teste.

2
00:00:05,000 --> 00:00:08,000
Esta é a segunda entrada de subtítulo.

3
00:00:09,000 --> 00:00:12,000
E esta é a terceira."""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.srt', delete=False, encoding='utf-8') as f:
        f.write(srt_content)
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    os.unlink(temp_file)


@pytest.fixture
def temp_output_file():
    """Create a temporary output file path."""
    with tempfile.NamedTemporaryFile(suffix='.srt', delete=False) as f:
        temp_file = f.name
    
    yield temp_file
    
    # Cleanup
    if os.path.exists(temp_file):
        os.unlink(temp_file)


@pytest.fixture
def mock_aws_credentials(monkeypatch):
    """Mock AWS credentials for testing."""
    monkeypatch.setenv('AWS_ACCESS_KEY_ID', 'test-access-key')
    monkeypatch.setenv('AWS_SECRET_ACCESS_KEY', 'test-secret-key')
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-east-1')


@pytest.fixture
def mock_bedrock_client(mocker):
    """Mock AWS Bedrock client for testing."""
    mock_client = mocker.patch('boto3.client')
    mock_bedrock = mocker.MagicMock()
    mock_client.return_value = mock_bedrock
    return mock_bedrock


@pytest.fixture
def sample_srt_entries():
    """Sample SRT entries for testing."""
    return [
        {
            'index': 1,
            'start_time': '00:00:01,000',
            'end_time': '00:00:04,000',
            'text': 'Hello, this is a test subtitle.'
        },
        {
            'index': 2,
            'start_time': '00:00:05,000',
            'end_time': '00:00:08,000',
            'text': 'This is the second subtitle entry.'
        },
        {
            'index': 3,
            'start_time': '00:00:09,000',
            'end_time': '00:00:12,000',
            'text': 'And this is the third one.'
        }
    ]


@pytest.fixture
def sample_translated_entries():
    """Sample translated SRT entries for testing."""
    return [
        {
            'index': 1,
            'start_time': '00:00:01,000',
            'end_time': '00:00:04,000',
            'text': 'Olá, este é um subtítulo de teste.'
        },
        {
            'index': 2,
            'start_time': '00:00:05,000',
            'end_time': '00:00:08,000',
            'text': 'Esta é a segunda entrada de subtítulo.'
        },
        {
            'index': 3,
            'start_time': '00:00:09,000',
            'end_time': '00:00:12,000',
            'text': 'E esta é a terceira.'
        }
    ] 
