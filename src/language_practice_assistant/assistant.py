import logging

from src.language_practice_assistant.kernel import SemanticKernel
from src.language_practice_assistant.telegram_client import TelegramClient

logger = logging.getLogger(__name__)


class Assistant:

    def __init__(self):
        self.semantic_kernel = SemanticKernel()
        self.telegram_client = TelegramClient(self.semantic_kernel)

    def start(self):
        self.telegram_client.run()
