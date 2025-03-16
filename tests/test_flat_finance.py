from unittest.mock import mock_open, patch

from src.multi_task_assistant.kernel_plugins.verbs import Verbs
from src.multi_task_assistant.kernel_plugins.flat_finance import FlatFinance


def test_flat_finance_initialization(test_config):
    flat_finance = FlatFinance(test_config)
    assert flat_finance.config == test_config

def test_flat_finance_system_prompt():
    prompt = FlatFinance.system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0