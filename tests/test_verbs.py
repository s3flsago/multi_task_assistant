from unittest.mock import mock_open, patch

from src.multi_task_assistant.kernel_plugins.verbs import Verbs
from src.multi_task_assistant.kernel_plugins.flat_finance import FlatFinance


def test_verbs_initialization(test_config):
    with patch("builtins.open", mock_open(read_data='{"verbs": []}')):
        verbs = Verbs(test_config)
        assert verbs.verb_data

def test_verbs_system_prompt():
    prompt = Verbs.system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 0

def test_verbs_initiate_quiz(test_config):
    with patch("builtins.open", mock_open(read_data='{"verbs": []}')):
        verbs = Verbs(test_config)
        result = verbs.initiate_quiz("test input")
        assert isinstance(result, str)

