import logging

from src.language_practice_assistant.kernel import SemanticKernel
from src.language_practice_assistant.telegram_client import TelegramClient

logger = logging.getLogger(__name__)


class Assistant:

    def __init__(self, config: dict):
        self.semantic_kernel = SemanticKernel(config)
        self.telegram_client = TelegramClient(
            config=config, semantic_kernel=self.semantic_kernel
        )

    def start(self):
        self.telegram_client.run()

    def terminate(self):
        self.telegram_client.shutdown()
        logging.info("Assistant terminated.")
