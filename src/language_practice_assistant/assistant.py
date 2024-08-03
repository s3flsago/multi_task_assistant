import logging

from src.language_practice_assistant.kernel import SemanticKernel
from src.language_practice_assistant.telegram import TelegramClient

logger = logging.getLogger(__name__)


class Assistant:

    def __init__(self):
        self.kernel = SemanticKernel()
        self.telegram_client = TelegramClient()

    def start(self):
        self.telegram_client.run()
