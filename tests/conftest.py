import pytest
import os
from src.multi_task_assistant.assistant import Assistant
from src.multi_task_assistant.kernel import SemanticKernel
from src.multi_task_assistant.telegram_client import TelegramClient

@pytest.fixture
def test_config():
    return {
        "absolute_data_path": "data",
        "openai": {
            "api_key": "test-key",
            "model": "gpt-4"
        },
        "telegram": {
            "token": "test-token"
        },
        "data_path": "test_data",
        "logging": {
            "level": "INFO"
        }
    }

@pytest.fixture
def assistant_name():
    return "test_assistant"

@pytest.fixture
def assistant(test_config, assistant_name):
    return Assistant(test_config, assistant_name)

@pytest.fixture
def semantic_kernel(test_config, assistant_name):
    return SemanticKernel(test_config, assistant_name)

@pytest.fixture
def telegram_client(test_config, semantic_kernel):
    return TelegramClient(test_config, semantic_kernel, test_config["telegram"]["token"])