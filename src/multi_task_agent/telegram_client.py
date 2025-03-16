import logging
import os
import nest_asyncio

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    filters,
    MessageHandler,
)

from src.multi_task_agent.kernel import SemanticKernel

logger = logging.getLogger(__name__)

nest_asyncio.apply()


class TelegramClient:

    def __init__(self, config: dict, semantic_kernel: SemanticKernel, telegram_token: str):
        self.config = config

        self.telegram_token = telegram_token
        self.application = ApplicationBuilder().token(self.telegram_token).build()
        self.semantic_kernel = semantic_kernel

        respond_fct = lambda update, context: self.respond(
            update, context, semantic_kernel=self.semantic_kernel
        )
        self.response_handler = MessageHandler(
            (filters.PHOTO | filters.TEXT) & (~filters.COMMAND), respond_fct
        )

        self.application.add_handler(self.response_handler)

    @staticmethod
    async def respond(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        semantic_kernel,
    ):
        input_text: str = update.message.text
        if update.message.photo:
            input_image = update.message.photo[-1]
            input_image_file = await input_image.get_file()
            input_image_bytes = await input_image_file.download_as_bytearray()
        else:
            input_image_bytes = None


        response_text = semantic_kernel.run(input_text=input_text, input_image=input_image_bytes)

        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=response_text
        )

    def run(self):
        self.application.run_polling()

    def shutdown(self) -> None:
        self.application.stop_running()

