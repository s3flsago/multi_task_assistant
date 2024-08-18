import logging
import os
import nest_asyncio

from dotenv import load_dotenv

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    filters,
    MessageHandler,
)

from src.language_practice_assistant.kernel import SemanticKernel

logger = logging.getLogger(__name__)

nest_asyncio.apply()

load_dotenv()

TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")


class TelegramClient:

    def __init__(self, config: dict, semantic_kernel: SemanticKernel):
        self.config = config
        self.application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        self.semantic_kernel = semantic_kernel

        respond_fct = lambda update, context: self.respond(
            update, context, semantic_kernel=self.semantic_kernel
        )
        self.response_handler = MessageHandler(
            filters.TEXT & (~filters.COMMAND), respond_fct
        )

        self.application.add_handler(self.response_handler)

    @staticmethod
    async def respond(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        semantic_kernel,
    ):
        input_text: str = update.message.text
        response_text = semantic_kernel.run(history=input_text)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=response_text
        )

    def run(self):
        self.application.run_polling()

    def shutdown(self) -> None:
        self.application.stop_running()

